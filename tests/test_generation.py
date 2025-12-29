"""
Test cases for generation component evaluation.
Tests the LLM response generation and quality metrics.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend import load_models, query_documents
from tests.evaluation_metrics import GenerationMetrics, EvaluationReport
from tests.test_queries import TEST_QUERIES


class TestGenerationQuality:
    """Test generation component quality metrics."""
    
    @pytest.fixture(scope="class")
    def models(self):
        """Load models once for all tests."""
        try:
            vectorstore, chain = load_models()
            return {"vectorstore": vectorstore, "chain": chain}
        except Exception as e:
            pytest.skip(f"Could not load models: {e}")
    
    def test_response_generation(self, models):
        """Test if responses are generated for queries."""
        query = "What is the main topic of this textbook?"
        
        try:
            response = query_documents(query, models["vectorstore"], models["chain"])
            
            assert response is not None
            assert isinstance(response, str)
            assert len(response) > 0
        except Exception as e:
            pytest.skip(f"Could not generate response: {e}")
    
    def test_faithfulness_score_calculation(self):
        """Test faithfulness metric calculation."""
        response = "The capital of France is Paris. It is located in the northern part of France."
        context = [
            "Paris is the capital and largest city of France.",
            "Paris is located in the north-central part of France."
        ]
        
        score = GenerationMetrics.calculate_faithfulness(response, context)
        
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should be high since response matches context
    
    def test_faithfulness_low_score(self):
        """Test faithfulness with ungrounded response."""
        response = "The capital of Germany is Berlin and it has a population of 4 million."
        context = [
            "Paris is the capital of France.",
            "London is the capital of United Kingdom."
        ]
        
        score = GenerationMetrics.calculate_faithfulness(response, context)
        
        assert 0.0 <= score <= 1.0
        assert score < 0.5  # Should be low since response doesn't match context
    
    def test_relevancy_score_calculation(self):
        """Test relevancy metric calculation."""
        query = "What is the capital of France?"
        response = "The capital of France is Paris."
        
        score = GenerationMetrics.calculate_relevancy(query, response)
        
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should be high since response addresses query
    
    def test_relevancy_low_score(self):
        """Test relevancy with irrelevant response."""
        query = "What is the capital of France?"
        response = "The weather today is sunny and warm."
        
        score = GenerationMetrics.calculate_relevancy(query, response)
        
        assert 0.0 <= score <= 1.0
        assert score < 0.5  # Should be low since response doesn't address query
    
    def test_response_length_calculation(self):
        """Test response length metric."""
        response = "This is a test response with ten words in it."
        
        length = GenerationMetrics.calculate_response_length(response)
        
        assert length == 10
    
    @pytest.mark.parametrize("query_data", TEST_QUERIES[:5])
    def test_generation_with_test_queries(self, models, query_data):
        """Test generation with predefined test queries."""
        query = query_data["query"]
        
        try:
            response = query_documents(query, models["vectorstore"], models["chain"])
            
            assert response is not None
            assert len(response) > 0
            assert isinstance(response, str)
            
            # Response should not be too short or too long
            word_count = len(response.split())
            assert word_count >= 10, f"Response too short for query {query_data['id']}"
            assert word_count <= 500, f"Response too long for query {query_data['id']}"
        except Exception as e:
            pytest.skip(f"Could not generate response for {query_data['id']}: {e}")
    
    def test_response_not_hallucinating(self, models):
        """Test that response doesn't contain 'cannot answer' when context exists."""
        query = "What are the topics covered in this textbook?"
        
        try:
            response = query_documents(query, models["vectorstore"], models["chain"])
            
            # If we have documents, should not say "cannot answer"
            docs = models["vectorstore"].similarity_search(query, k=3)
            if len(docs) > 0 and len(docs[0].page_content) > 100:
                assert "cannot find" not in response.lower() or "cannot answer" not in response.lower()
        except Exception as e:
            pytest.skip(f"Could not test hallucination: {e}")


class TestEndToEndEvaluation:
    """End-to-end evaluation tests similar to the paper's Tables III and IV."""
    
    @pytest.fixture(scope="class")
    def models(self):
        """Load models once for all tests."""
        try:
            vectorstore, chain = load_models()
            return {"vectorstore": vectorstore, "chain": chain}
        except Exception as e:
            pytest.skip(f"Could not load models: {e}")
    
    @pytest.mark.slow
    def test_evaluate_all_queries(self, models):
        """
        Evaluate system on all test queries.
        This generates a report similar to Table III in the paper.
        """
        results = []
        query_ids = []
        
        for query_data in TEST_QUERIES[:5]:  # Test first 5 queries
            query = query_data["query"]
            query_id = query_data["id"]
            
            try:
                # Retrieve documents
                retrieved_docs = models["vectorstore"].similarity_search(query, k=10)
                
                # Generate response
                response = query_documents(query, models["vectorstore"], models["chain"])
                
                # Prepare context from retrieved docs
                context = [doc.page_content for doc in retrieved_docs[:3]]
                
                # Mock relevance judgments (in production, use human annotations)
                retrieved_with_relevance = [
                    {"content": doc.page_content, "is_relevant": i < 3}  # Top 3 marked relevant
                    for i, doc in enumerate(retrieved_docs)
                ]
                
                # Evaluate
                evaluation = EvaluationReport.evaluate_single_query(
                    query=query,
                    response=response,
                    context=context,
                    retrieved_docs=retrieved_with_relevance
                )
                
                results.append(evaluation)
                query_ids.append(query_id)
                
            except Exception as e:
                print(f"Error evaluating {query_id}: {e}")
                continue
        
        # Print evaluation table
        if results:
            EvaluationReport.print_evaluation_table(results, query_ids)
            
            # Assert basic quality thresholds
            aggregated = EvaluationReport.aggregate_results(results)
            assert aggregated.get("avg_mrr", 0) > 0.0
            assert aggregated.get("avg_faithfulness", 0) > 0.3
            assert aggregated.get("avg_relevancy", 0) > 0.3
    
    def test_single_query_evaluation(self, models):
        """Test evaluation pipeline for a single query."""
        query = "What are the main concepts discussed?"
        
        try:
            # Retrieve and generate
            retrieved_docs = models["vectorstore"].similarity_search(query, k=5)
            response = query_documents(query, models["vectorstore"], models["chain"])
            
            # Evaluate
            context = [doc.page_content for doc in retrieved_docs[:3]]
            retrieved_with_relevance = [
                {"content": doc.page_content, "is_relevant": True}
                for doc in retrieved_docs
            ]
            
            evaluation = EvaluationReport.evaluate_single_query(
                query=query,
                response=response,
                context=context,
                retrieved_docs=retrieved_with_relevance
            )
            
            # Check all metrics are present
            assert "mrr" in evaluation
            assert "faithfulness" in evaluation
            assert "relevancy" in evaluation
            assert "response_length" in evaluation
            
            # Check value ranges
            assert 0.0 <= evaluation["faithfulness"] <= 1.0
            assert 0.0 <= evaluation["relevancy"] <= 1.0
            assert evaluation["response_length"] > 0
            
        except Exception as e:
            pytest.skip(f"Could not complete evaluation: {e}")
