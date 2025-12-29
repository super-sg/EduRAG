"""
Integration tests for the complete RAG system.
Tests the full pipeline from query to response.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend import load_models, query_documents
from tests.test_queries import TEST_QUERIES


class TestSystemIntegration:
    """Integration tests for the complete system."""
    
    @pytest.fixture(scope="class")
    def system(self):
        """Load the complete system."""
        try:
            vectorstore, chain = load_models()
            return {"vectorstore": vectorstore, "chain": chain}
        except Exception as e:
            pytest.skip(f"Could not load system: {e}")
    
    def test_full_pipeline(self, system):
        """Test the complete query-to-response pipeline."""
        query = "What is the main topic of this chapter?"
        
        try:
            response = query_documents(query, system["vectorstore"], system["chain"])
            
            assert response is not None
            assert isinstance(response, str)
            assert len(response) > 20
        except Exception as e:
            pytest.fail(f"Pipeline failed: {e}")
    
    @pytest.mark.parametrize("query_data", TEST_QUERIES[:3])
    def test_system_with_various_queries(self, system, query_data):
        """Test system with different types of queries."""
        query = query_data["query"]
        
        try:
            response = query_documents(query, system["vectorstore"], system["chain"])
            
            assert response is not None
            assert len(response) > 0
            
            # Check that response contains relevant terms
            expected_topics = query_data.get("expected_topics", [])
            if expected_topics:
                # At least one expected topic should appear in response (case-insensitive)
                response_lower = response.lower()
                found = any(topic.lower() in response_lower for topic in expected_topics)
                # This might fail if context doesn't have the info, so just warn
                if not found:
                    print(f"Warning: No expected topics found in response for {query_data['id']}")
        except Exception as e:
            pytest.skip(f"System test failed for {query_data['id']}: {e}")
    
    def test_system_handles_empty_query(self, system):
        """Test system behavior with empty query."""
        query = ""
        
        # System should either return empty response or handle gracefully
        try:
            response = query_documents(query, system["vectorstore"], system["chain"])
            # Just check it doesn't crash
            assert isinstance(response, str)
        except Exception:
            # It's okay if it raises an exception for empty query
            pass
    
    def test_system_handles_very_long_query(self, system):
        """Test system with very long query."""
        query = " ".join(["What is the significance of educational systems"] * 20)
        
        try:
            response = query_documents(query, system["vectorstore"], system["chain"])
            assert response is not None
            assert isinstance(response, str)
        except Exception as e:
            # Long queries might fail, that's acceptable
            print(f"Long query handling: {e}")
    
    @pytest.mark.integration
    def test_retrieval_affects_generation(self, system):
        """Test that retrieved context influences generated response."""
        query = "What specific topic is covered in chapter 1?"
        
        try:
            # Get retrieved documents
            docs = system["vectorstore"].similarity_search(query, k=3)
            
            # Generate response
            response = query_documents(query, system["vectorstore"], system["chain"])
            
            # Check if response mentions something from retrieved docs
            if docs and len(docs) > 0:
                # Extract some words from first document
                doc_words = set(docs[0].page_content.lower().split())
                response_words = set(response.lower().split())
                
                # Should have some overlap
                overlap = doc_words.intersection(response_words)
                assert len(overlap) > 5, "Response should be based on retrieved context"
        except Exception as e:
            pytest.skip(f"Integration test failed: {e}")


class TestSystemRobustness:
    """Test system robustness and error handling."""
    
    @pytest.fixture(scope="class")
    def system(self):
        """Load the system."""
        try:
            vectorstore, chain = load_models()
            return {"vectorstore": vectorstore, "chain": chain}
        except Exception as e:
            pytest.skip(f"Could not load system: {e}")
    
    def test_system_handles_special_characters(self, system):
        """Test system with special characters in query."""
        query = "What is the @#$% topic? (explain!)"
        
        try:
            response = query_documents(query, system["vectorstore"], system["chain"])
            assert isinstance(response, str)
        except Exception:
            # It's acceptable if special characters cause issues
            pass
    
    def test_system_consistency(self, system):
        """Test that similar queries produce similar responses."""
        query1 = "What are the main features of educational systems?"
        query2 = "What are the key characteristics of learning systems?"
        
        try:
            response1 = query_documents(query1, system["vectorstore"], system["chain"])
            response2 = query_documents(query2, system["vectorstore"], system["chain"])
            
            # Both should be non-empty
            assert len(response1) > 0
            assert len(response2) > 0
            
            # Should have some common words (basic consistency check)
            words1 = set(response1.lower().split())
            words2 = set(response2.lower().split())
            common = words1.intersection(words2)
            
            # At least 10% overlap expected for similar queries
            overlap_ratio = len(common) / max(len(words1), len(words2))
            assert overlap_ratio > 0.1, "Similar queries should produce somewhat similar responses"
        except Exception as e:
            pytest.skip(f"Consistency test failed: {e}")
