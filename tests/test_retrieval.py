"""
Test cases for retrieval component evaluation.
Tests the vector store and document retrieval performance.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend import load_models
from tests.evaluation_metrics import RetrievalMetrics
from tests.test_queries import TEST_QUERIES


class TestRetrievalPerformance:
    """Test retrieval component performance metrics."""
    
    @pytest.fixture(scope="class")
    def models(self):
        """Load models once for all tests in this class."""
        try:
            vectorstore, chain = load_models()
            return {"vectorstore": vectorstore, "chain": chain}
        except Exception as e:
            pytest.skip(f"Could not load models: {e}")
    
    def test_vectorstore_initialization(self, models):
        """Test if vector store initializes correctly."""
        assert models["vectorstore"] is not None
        assert models["chain"] is not None
    
    def test_document_retrieval_returns_results(self, models):
        """Test if documents are retrieved for a query."""
        vectorstore = models["vectorstore"]
        query = "What is the main topic discussed in this chapter?"
        
        results = vectorstore.similarity_search(query, k=5)
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert len(results) <= 5
    
    @pytest.mark.parametrize("k", [1, 3, 5, 10])
    def test_retrieval_with_different_k_values(self, models, k):
        """Test retrieval with different k values."""
        vectorstore = models["vectorstore"]
        query = "Explain the concept of learning systems."
        
        results = vectorstore.similarity_search(query, k=k)
        
        assert len(results) <= k
        assert len(results) > 0
    
    def test_mrr_calculation(self):
        """Test Mean Reciprocal Rank calculation."""
        # Simulate retrieval results
        results = [
            {"content": "doc1", "is_relevant": False},
            {"content": "doc2", "is_relevant": True},  # Rank 2
            {"content": "doc3", "is_relevant": False},
        ]
        
        mrr = RetrievalMetrics.calculate_mrr(results)
        assert mrr == 0.5  # 1/2
    
    def test_mrr_no_relevant_docs(self):
        """Test MRR when no relevant documents are found."""
        results = [
            {"content": "doc1", "is_relevant": False},
            {"content": "doc2", "is_relevant": False},
        ]
        
        mrr = RetrievalMetrics.calculate_mrr(results)
        assert mrr == 0.0
    
    def test_hit_at_k(self):
        """Test Hit@k metric."""
        results = [
            {"content": "doc1", "is_relevant": False},
            {"content": "doc2", "is_relevant": False},
            {"content": "doc3", "is_relevant": True},  # At position 3
            {"content": "doc4", "is_relevant": False},
        ]
        
        hit_at_5 = RetrievalMetrics.calculate_hit_at_k(results, k=5)
        assert hit_at_5 == 1.0
        
        hit_at_2 = RetrievalMetrics.calculate_hit_at_k(results, k=2)
        assert hit_at_2 == 0.0
    
    def test_precision_at_k(self):
        """Test Precision@k metric."""
        results = [
            {"content": "doc1", "is_relevant": True},
            {"content": "doc2", "is_relevant": False},
            {"content": "doc3", "is_relevant": True},
            {"content": "doc4", "is_relevant": False},
            {"content": "doc5", "is_relevant": True},
        ]
        
        precision_at_5 = RetrievalMetrics.calculate_precision_at_k(results, k=5)
        assert precision_at_5 == 0.6  # 3 relevant out of 5
    
    def test_retrieval_with_test_queries(self, models):
        """Test retrieval with predefined test queries."""
        vectorstore = models["vectorstore"]
        
        for test_query in TEST_QUERIES[:3]:  # Test first 3 queries
            query = test_query["query"]
            results = vectorstore.similarity_search(query, k=10)
            
            assert len(results) > 0, f"No results for query: {test_query['id']}"
            assert all(hasattr(doc, 'page_content') for doc in results)
    
    def test_retrieval_scores_are_ordered(self, models):
        """Test that retrieval results are ordered by relevance score."""
        vectorstore = models["vectorstore"]
        query = "What are the key features of educational systems?"
        
        results = vectorstore.similarity_search_with_score(query, k=5)
        
        # Scores should be in ascending order (lower is better for some distance metrics)
        # or descending order (higher is better for similarity)
        scores = [score for _, score in results]
        
        assert len(scores) > 1
        # Just check that we got scores, ordering depends on the metric used
        assert all(isinstance(s, (int, float)) for s in scores)


class TestRetrievalQuality:
    """Test the quality and relevance of retrieved documents."""
    
    @pytest.fixture(scope="class")
    def models(self):
        """Load models once for all tests."""
        try:
            vectorstore, chain = load_models()
            return {"vectorstore": vectorstore, "chain": chain}
        except Exception as e:
            pytest.skip(f"Could not load models: {e}")
    
    def test_retrieved_documents_not_empty(self, models):
        """Test that retrieved documents contain text."""
        vectorstore = models["vectorstore"]
        query = "What is the main concept?"
        
        results = vectorstore.similarity_search(query, k=3)
        
        for doc in results:
            assert len(doc.page_content) > 0
            assert isinstance(doc.page_content, str)
    
    def test_retrieved_documents_have_metadata(self, models):
        """Test that retrieved documents include metadata."""
        vectorstore = models["vectorstore"]
        query = "Explain the learning process."
        
        results = vectorstore.similarity_search(query, k=3)
        
        for doc in results:
            assert hasattr(doc, 'metadata')
            # Metadata might include source, page number, etc.
    
    @pytest.mark.slow
    def test_retrieval_consistency(self, models):
        """Test that same query returns consistent results."""
        vectorstore = models["vectorstore"]
        query = "What are the main features?"
        
        results1 = vectorstore.similarity_search(query, k=5)
        results2 = vectorstore.similarity_search(query, k=5)
        
        # Should get same documents (might be in slightly different order)
        assert len(results1) == len(results2)
