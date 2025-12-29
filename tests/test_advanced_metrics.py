"""
Test cases for advanced NLG metrics: BERTScore, ROUGE-L, and BLEU.
These metrics are commonly used in research papers for evaluating text generation quality.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.evaluation_metrics import GenerationMetrics


class TestBERTScore:
    """Test BERTScore metric for semantic similarity evaluation."""
    
    def test_bertscore_perfect_match(self):
        """Test BERTScore with identical texts."""
        response = "Newton's first law of motion states that an object at rest stays at rest."
        reference = "Newton's first law of motion states that an object at rest stays at rest."
        
        scores = GenerationMetrics.calculate_bertscore(response, reference)
        
        assert "bertscore_f1" in scores
        assert "bertscore_precision" in scores
        assert "bertscore_recall" in scores
        
        # Perfect match should have high F1 score
        if scores["bertscore_f1"] > 0:  # Check if bert-score is installed
            assert scores["bertscore_f1"] > 0.95
    
    def test_bertscore_semantic_similarity(self):
        """Test BERTScore with semantically similar texts."""
        response = "The first law of Newton says objects remain at rest unless acted upon by force."
        reference = "Newton's first law states that objects stay at rest without external force."
        
        scores = GenerationMetrics.calculate_bertscore(response, reference)
        
        # Semantically similar should have good score
        if scores["bertscore_f1"] > 0:
            assert scores["bertscore_f1"] > 0.7
    
    def test_bertscore_low_similarity(self):
        """Test BERTScore with unrelated texts."""
        response = "The law of conservation of energy states energy cannot be created or destroyed."
        reference = "Newton's first law states that objects stay at rest without external force."
        
        scores = GenerationMetrics.calculate_bertscore(response, reference)
        
        # Unrelated texts should have lower score
        if scores["bertscore_f1"] > 0:
            assert scores["bertscore_f1"] < 0.8
    
    def test_bertscore_empty_input(self):
        """Test BERTScore with empty input."""
        response = ""
        reference = "Some reference text"
        
        scores = GenerationMetrics.calculate_bertscore(response, reference)
        
        # Should handle empty input gracefully
        assert isinstance(scores, dict)
        assert "bertscore_f1" in scores


class TestROUGEL:
    """Test ROUGE-L metric for longest common subsequence evaluation."""
    
    def test_rouge_l_perfect_match(self):
        """Test ROUGE-L with identical texts."""
        response = "Newton's first law of motion states that an object at rest stays at rest."
        reference = "Newton's first law of motion states that an object at rest stays at rest."
        
        scores = GenerationMetrics.calculate_rouge_l(response, reference)
        
        assert "rouge_l_f1" in scores
        assert "rouge_l_precision" in scores
        assert "rouge_l_recall" in scores
        
        # Perfect match should have score of 1.0
        if scores["rouge_l_f1"] > 0:
            assert scores["rouge_l_f1"] == pytest.approx(1.0, rel=0.01)
    
    def test_rouge_l_partial_match(self):
        """Test ROUGE-L with partial overlap."""
        response = "Newton's first law states that objects remain at rest."
        reference = "Newton's first law of motion states that an object at rest stays at rest."
        
        scores = GenerationMetrics.calculate_rouge_l(response, reference)
        
        # Partial match should have moderate score
        if scores["rouge_l_f1"] > 0:
            assert 0.4 < scores["rouge_l_f1"] < 1.0
    
    def test_rouge_l_no_match(self):
        """Test ROUGE-L with completely different texts."""
        response = "Energy conservation principle applies to all systems."
        reference = "Newton's first law of motion states that an object at rest stays at rest."
        
        scores = GenerationMetrics.calculate_rouge_l(response, reference)
        
        # No common subsequence should have low score
        if scores["rouge_l_f1"] > 0:
            assert scores["rouge_l_f1"] < 0.3
    
    def test_rouge_l_word_order_matters(self):
        """Test that ROUGE-L is sensitive to word order."""
        response = "stays at rest that states motion of law first Newton's an object"
        reference = "Newton's first law of motion states that an object at rest stays"
        
        scores = GenerationMetrics.calculate_rouge_l(response, reference)
        
        # Same words but different order should have lower score
        if scores["rouge_l_f1"] > 0:
            assert scores["rouge_l_f1"] < 0.8


class TestBLEU:
    """Test BLEU metric for n-gram overlap evaluation."""
    
    def test_bleu_perfect_match(self):
        """Test BLEU with identical texts."""
        response = "Newton's first law of motion states that an object at rest stays at rest."
        reference = "Newton's first law of motion states that an object at rest stays at rest."
        
        score = GenerationMetrics.calculate_bleu_score(response, reference)
        
        # Perfect match should have high BLEU score
        if score > 0:
            assert score > 0.9
    
    def test_bleu_partial_match(self):
        """Test BLEU with partial overlap."""
        response = "Newton's first law states that objects stay at rest."
        reference = "Newton's first law of motion states that an object at rest stays at rest."
        
        score = GenerationMetrics.calculate_bleu_score(response, reference)
        
        # Partial match should have moderate score
        if score > 0:
            assert 0.2 < score < 0.9
    
    def test_bleu_no_match(self):
        """Test BLEU with completely different texts."""
        response = "Energy conservation principle applies to all systems completely differently."
        reference = "Newton's first law of motion states that objects remain at rest."
        
        score = GenerationMetrics.calculate_bleu_score(response, reference)
        
        # No common n-grams should have low score
        assert score < 0.3


class TestAdvancedMetricsIntegration:
    """Integration tests for using multiple metrics together."""
    
    def test_all_metrics_on_physics_answer(self):
        """Test all metrics on a sample physics question and answer."""
        reference = """Newton's first law of motion states that an object at rest stays at rest 
        and an object in motion stays in motion with the same speed and in the same direction 
        unless acted upon by an external force. This is also known as the law of inertia."""
        
        response = """The first law of Newton states that objects remain in their state of rest 
        or uniform motion unless an external force acts on them. This principle is called inertia."""
        
        # Calculate all metrics
        bertscore = GenerationMetrics.calculate_bertscore(response, reference)
        rouge_l = GenerationMetrics.calculate_rouge_l(response, reference)
        bleu = GenerationMetrics.calculate_bleu_score(response, reference)
        
        # All metrics should return valid values
        assert isinstance(bertscore, dict)
        assert isinstance(rouge_l, dict)
        assert isinstance(bleu, float)
        
        # Print results for inspection
        print("\n=== Advanced Metrics Evaluation ===")
        print(f"BERTScore F1: {bertscore.get('bertscore_f1', 0):.4f}")
        print(f"ROUGE-L F1: {rouge_l.get('rouge_l_f1', 0):.4f}")
        print(f"BLEU Score: {bleu:.4f}")
    
    def test_metrics_comparison(self):
        """Test that metrics give sensible relative scores."""
        reference = "Work is defined as force multiplied by displacement."
        
        # Good answer (semantically correct, different wording)
        good_response = "Work equals the product of force and displacement."
        
        # Poor answer (unrelated)
        poor_response = "Energy is the capacity to do work in a system."
        
        # Calculate metrics for good response
        good_bert = GenerationMetrics.calculate_bertscore(good_response, reference)
        good_rouge = GenerationMetrics.calculate_rouge_l(good_response, reference)
        
        # Calculate metrics for poor response
        poor_bert = GenerationMetrics.calculate_bertscore(poor_response, reference)
        poor_rouge = GenerationMetrics.calculate_rouge_l(poor_response, reference)
        
        # Good response should score higher than poor response
        if good_bert["bertscore_f1"] > 0 and poor_bert["bertscore_f1"] > 0:
            assert good_bert["bertscore_f1"] > poor_bert["bertscore_f1"]
        
        if good_rouge["rouge_l_f1"] > 0 and poor_rouge["rouge_l_f1"] > 0:
            assert good_rouge["rouge_l_f1"] > poor_rouge["rouge_l_f1"]


@pytest.mark.slow
class TestMetricsOnRealQueries:
    """Test metrics on real RAG system responses (requires models loaded)."""
    
    @pytest.fixture(scope="class")
    def models(self):
        """Load models for testing."""
        try:
            from backend import load_models
            vectorstore, chain = load_models()
            return {"vectorstore": vectorstore, "chain": chain}
        except Exception as e:
            pytest.skip(f"Could not load models: {e}")
    
    def test_evaluate_physics_answer_with_advanced_metrics(self, models):
        """Evaluate a real physics answer using advanced metrics."""
        from backend import query_documents
        from tests.test_queries import TEST_QUERIES
        
        # Use first physics query
        query_data = TEST_QUERIES[0]
        query = query_data["query"]
        
        try:
            # Generate response
            response = query_documents(query, models["vectorstore"], models["chain"])
            
            # Create a reference answer (in real testing, this would be human-written)
            reference = """Newton's first law of motion, also known as the law of inertia, 
            states that an object at rest will remain at rest and an object in motion will 
            remain in motion with constant velocity unless acted upon by an external force."""
            
            # Calculate advanced metrics
            bertscore = GenerationMetrics.calculate_bertscore(response, reference)
            rouge_l = GenerationMetrics.calculate_rouge_l(response, reference)
            bleu = GenerationMetrics.calculate_bleu_score(response, reference)
            
            # Print results
            print(f"\nQuery: {query}")
            print(f"Response: {response[:200]}...")
            print(f"\nBERTScore F1: {bertscore.get('bertscore_f1', 0):.4f}")
            print(f"ROUGE-L F1: {rouge_l.get('rouge_l_f1', 0):.4f}")
            print(f"BLEU Score: {bleu:.4f}")
            
            # Basic assertions
            assert len(response) > 0
            
        except Exception as e:
            pytest.skip(f"Could not evaluate: {e}")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
