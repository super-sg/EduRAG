"""
Evaluation metrics for RAG system testing.
Implements metrics from the research paper:
- MRR (Mean Reciprocal Rank)
- Hit@k
- Faithfulness Score
- Relevancy Score
"""

import re
from typing import List, Dict, Any
import numpy as np


class RetrievalMetrics:
    """Metrics for evaluating retrieval performance."""
    
    @staticmethod
    def calculate_mrr(results: List[Dict[str, Any]], relevant_key: str = "is_relevant") -> float:
        """
        Calculate Mean Reciprocal Rank (MRR).
        
        Args:
            results: List of retrieval results with relevance information
            relevant_key: Key in the dict that indicates relevance (boolean)
            
        Returns:
            MRR score between 0 and 1
        """
        for rank, result in enumerate(results, start=1):
            if result.get(relevant_key, False):
                return 1.0 / rank
        return 0.0
    
    @staticmethod
    def calculate_hit_at_k(results: List[Dict[str, Any]], k: int = 10, 
                          relevant_key: str = "is_relevant") -> float:
        """
        Calculate Hit@k - whether any relevant document appears in top k results.
        
        Args:
            results: List of retrieval results
            k: Number of top results to consider
            relevant_key: Key indicating relevance
            
        Returns:
            1.0 if hit, 0.0 otherwise
        """
        top_k = results[:k]
        for result in top_k:
            if result.get(relevant_key, False):
                return 1.0
        return 0.0
    
    @staticmethod
    def calculate_precision_at_k(results: List[Dict[str, Any]], k: int = 10,
                                 relevant_key: str = "is_relevant") -> float:
        """
        Calculate Precision@k.
        
        Args:
            results: List of retrieval results
            k: Number of top results to consider
            relevant_key: Key indicating relevance
            
        Returns:
            Precision score between 0 and 1
        """
        if not results or k == 0:
            return 0.0
        
        top_k = results[:k]
        relevant_count = sum(1 for r in top_k if r.get(relevant_key, False))
        return relevant_count / len(top_k)


class GenerationMetrics:
    """Metrics for evaluating generation quality."""
    
    @staticmethod
    def calculate_bertscore(response: str, reference: str) -> Dict[str, float]:
        """
        Calculate BERTScore for response quality.
        BERTScore uses BERT embeddings to measure semantic similarity.
        
        Args:
            response: Generated response text
            reference: Reference/ground truth text
            
        Returns:
            Dictionary with precision, recall, and F1 scores
        """
        try:
            from bert_score import score
            
            # Calculate BERTScore
            P, R, F1 = score([response], [reference], lang="en", verbose=False)
            
            return {
                "bertscore_precision": P.item(),
                "bertscore_recall": R.item(),
                "bertscore_f1": F1.item()
            }
        except ImportError:
            print("Warning: bert-score not installed. Install with: pip install bert-score")
            return {
                "bertscore_precision": 0.0,
                "bertscore_recall": 0.0,
                "bertscore_f1": 0.0
            }
        except Exception as e:
            print(f"Warning: BERTScore calculation failed: {e}")
            return {
                "bertscore_precision": 0.0,
                "bertscore_recall": 0.0,
                "bertscore_f1": 0.0
            }
    
    @staticmethod
    def calculate_rouge_l(response: str, reference: str) -> Dict[str, float]:
        """
        Calculate ROUGE-L score for response quality.
        ROUGE-L measures longest common subsequence between response and reference.
        
        Args:
            response: Generated response text
            reference: Reference/ground truth text
            
        Returns:
            Dictionary with ROUGE-L precision, recall, and F1 scores
        """
        try:
            from rouge_score import rouge_scorer
            
            scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
            scores = scorer.score(reference, response)
            
            return {
                "rouge_l_precision": scores['rougeL'].precision,
                "rouge_l_recall": scores['rougeL'].recall,
                "rouge_l_f1": scores['rougeL'].fmeasure
            }
        except ImportError:
            print("Warning: rouge-score not installed. Install with: pip install rouge-score")
            return {
                "rouge_l_precision": 0.0,
                "rouge_l_recall": 0.0,
                "rouge_l_f1": 0.0
            }
        except Exception as e:
            print(f"Warning: ROUGE-L calculation failed: {e}")
            return {
                "rouge_l_precision": 0.0,
                "rouge_l_recall": 0.0,
                "rouge_l_f1": 0.0
            }
    
    @staticmethod
    def calculate_bleu_score(response: str, reference: str) -> float:
        """
        Calculate BLEU score for response quality.
        BLEU measures n-gram overlap between response and reference.
        
        Args:
            response: Generated response text
            reference: Reference/ground truth text
            
        Returns:
            BLEU score between 0 and 1
        """
        try:
            from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
            
            reference_tokens = [reference.split()]
            response_tokens = response.split()
            
            smoothing = SmoothingFunction().method1
            score = sentence_bleu(reference_tokens, response_tokens, 
                                smoothing_function=smoothing)
            
            return score
        except ImportError:
            print("Warning: nltk not installed. Install with: pip install nltk")
            return 0.0
        except Exception as e:
            print(f"Warning: BLEU calculation failed: {e}")
            return 0.0
    
    @staticmethod
    def calculate_faithfulness(response: str, context: List[str]) -> float:
        """
        Calculate faithfulness score - how well the response is grounded in context.
        
        A faithfulness score of 1.0 means the response is fully grounded in the context.
        A score of 0.0 means the response contains information not in the context.
        
        This is a simplified implementation. For production, use more sophisticated
        methods like NLI models or LLM-based evaluation.
        
        Args:
            response: Generated response text
            context: List of context passages
            
        Returns:
            Faithfulness score between 0 and 1
        """
        if not response or not context:
            return 0.0
        
        # Simplified approach: Check if key phrases from response appear in context
        response_lower = response.lower()
        context_text = " ".join(context).lower()
        
        # Extract significant words (ignore common stop words)
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
                     "of", "with", "is", "are", "was", "were", "be", "been", "being",
                     "have", "has", "had", "do", "does", "did", "will", "would", "could",
                     "should", "may", "might", "can", "this", "that", "these", "those"}
        
        # Tokenize and filter
        response_words = [w for w in re.findall(r'\b\w+\b', response_lower) 
                         if w not in stop_words and len(w) > 3]
        
        if not response_words:
            return 0.5  # Neutral score for very short responses
        
        # Count how many significant words from response appear in context
        grounded_words = sum(1 for word in response_words if word in context_text)
        faithfulness_score = grounded_words / len(response_words)
        
        return min(faithfulness_score, 1.0)
    
    @staticmethod
    def calculate_relevancy(query: str, response: str) -> float:
        """
        Calculate relevancy score - how well the response addresses the query.
        
        A relevancy score of 1.0 means the response fully addresses the query.
        A score of 0.0 means the response is completely irrelevant.
        
        This is a simplified implementation. For production, use semantic similarity
        or LLM-based evaluation.
        
        Args:
            query: User's query
            response: Generated response
            
        Returns:
            Relevancy score between 0 and 1
        """
        if not query or not response:
            return 0.0
        
        query_lower = query.lower()
        response_lower = response.lower()
        
        # Extract key terms from query
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
                     "of", "with", "is", "are", "was", "were", "be", "been", "being",
                     "what", "how", "why", "when", "where", "who", "which", "explain",
                     "describe", "discuss", "provide"}
        
        query_terms = [w for w in re.findall(r'\b\w+\b', query_lower) 
                      if w not in stop_words and len(w) > 3]
        
        if not query_terms:
            return 0.5
        
        # Count how many query terms appear in the response
        matching_terms = sum(1 for term in query_terms if term in response_lower)
        relevancy_score = matching_terms / len(query_terms)
        
        # Bonus for response length (not too short, not too verbose)
        length_penalty = 1.0
        if len(response) < 50:
            length_penalty = 0.7
        elif len(response) > 1000:
            length_penalty = 0.9
        
        final_score = relevancy_score * length_penalty
        return min(final_score, 1.0)
    
    @staticmethod
    def calculate_response_length(response: str) -> int:
        """Calculate response length in words."""
        return len(response.split())


class EvaluationReport:
    """Generate evaluation reports similar to Tables III and IV in the paper."""
    
    @staticmethod
    def evaluate_single_query(query: str, response: str, context: List[str],
                            retrieved_docs: List[Dict[str, Any]], 
                            reference: str = None, include_advanced: bool = False) -> Dict[str, Any]:
        """
        Evaluate a single query-response pair.
        
        Args:
            query: The user query
            response: Generated response
            context: Retrieved context passages
            retrieved_docs: List of retrieved documents with relevance info
            reference: Optional reference answer for BERTScore/ROUGE-L
            include_advanced: Whether to calculate BERTScore, ROUGE-L, BLEU
        
        Returns:
            Dictionary with all evaluation metrics
        """
        results = {
            "mrr": RetrievalMetrics.calculate_mrr(retrieved_docs),
            "hit@10": RetrievalMetrics.calculate_hit_at_k(retrieved_docs, k=10),
            "hit@5": RetrievalMetrics.calculate_hit_at_k(retrieved_docs, k=5),
            "faithfulness": GenerationMetrics.calculate_faithfulness(response, context),
            "relevancy": GenerationMetrics.calculate_relevancy(query, response),
            "response_length": GenerationMetrics.calculate_response_length(response)
        }
        
        # Add advanced metrics if requested and reference is provided
        if include_advanced and reference:
            bertscore = GenerationMetrics.calculate_bertscore(response, reference)
            rouge_l = GenerationMetrics.calculate_rouge_l(response, reference)
            bleu = GenerationMetrics.calculate_bleu_score(response, reference)
            
            results.update({
                "bertscore_f1": bertscore.get("bertscore_f1", 0.0),
                "rouge_l_f1": rouge_l.get("rouge_l_f1", 0.0),
                "bleu": bleu
            })
        
        return results
    
    @staticmethod
    def aggregate_results(results: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Aggregate results across multiple queries.
        
        Returns:
            Dictionary with averaged metrics
        """
        if not results:
            return {}
        
        # Standard metrics
        metrics = ["mrr", "hit@10", "hit@5", "faithfulness", "relevancy", "response_length"]
        
        # Add advanced metrics if present
        if results and "bertscore_f1" in results[0]:
            metrics.extend(["bertscore_f1", "rouge_l_f1", "bleu"])
        
        aggregated = {}
        
        for metric in metrics:
            values = [r[metric] for r in results if metric in r and r[metric] > 0]
            if values:
                aggregated[f"avg_{metric}"] = np.mean(values)
                aggregated[f"std_{metric}"] = np.std(values)
        
        return aggregated
    
    @staticmethod
    def print_evaluation_table(results: List[Dict[str, Any]], query_ids: List[str] = None):
        """
        Print evaluation results in a table format similar to Table III in the paper.
        """
        if not results:
            print("No results to display.")
            return
        
        print("\n" + "="*100)
        print("EVALUATION RESULTS - RAG SYSTEM PERFORMANCE")
        print("="*100)
        print(f"{'Query ID':<12} {'MRR':<10} {'Hit@10':<10} {'Faithfulness':<15} {'Relevancy':<15} {'Length':<10}")
        print("-"*100)
        
        for i, result in enumerate(results):
            qid = query_ids[i] if query_ids and i < len(query_ids) else f"Q{i+1}"
            print(f"{qid:<12} "
                  f"{result.get('mrr', 0):<10.4f} "
                  f"{result.get('hit@10', 0):<10.4f} "
                  f"{result.get('faithfulness', 0):<15.4f} "
                  f"{result.get('relevancy', 0):<15.4f} "
                  f"{result.get('response_length', 0):<10.0f}")
        
        print("-"*100)
        
        # Print averages
        aggregated = EvaluationReport.aggregate_results(results)
        print(f"{'AVERAGE':<12} "
              f"{aggregated.get('avg_mrr', 0):<10.4f} "
              f"{aggregated.get('avg_hit@10', 0):<10.4f} "
              f"{aggregated.get('avg_faithfulness', 0):<15.4f} "
              f"{aggregated.get('avg_relevancy', 0):<15.4f} "
              f"{aggregated.get('avg_response_length', 0):<10.0f}")
        print("="*100 + "\n")
    
    @staticmethod
    def print_advanced_metrics_table(results: List[Dict[str, Any]], query_ids: List[str] = None):
        """
        Print evaluation results including advanced metrics (BERTScore, ROUGE-L, BLEU).
        """
        if not results:
            print("No results to display.")
            return
        
        # Check if advanced metrics are present
        has_advanced = any("bertscore_f1" in r for r in results)
        if not has_advanced:
            print("No advanced metrics found. Use include_advanced=True in evaluation.")
            return
        
        print("\n" + "="*120)
        print("ADVANCED METRICS - NLG EVALUATION")
        print("="*120)
        print(f"{'Query ID':<12} {'BERTScore F1':<15} {'ROUGE-L F1':<15} {'BLEU':<10} "
              f"{'Faithfulness':<15} {'Relevancy':<15}")
        print("-"*120)
        
        for i, result in enumerate(results):
            qid = query_ids[i] if query_ids and i < len(query_ids) else f"Q{i+1}"
            print(f"{qid:<12} "
                  f"{result.get('bertscore_f1', 0):<15.4f} "
                  f"{result.get('rouge_l_f1', 0):<15.4f} "
                  f"{result.get('bleu', 0):<10.4f} "
                  f"{result.get('faithfulness', 0):<15.4f} "
                  f"{result.get('relevancy', 0):<15.4f}")
        
        print("-"*120)
        
        # Print averages
        metrics = ["bertscore_f1", "rouge_l_f1", "bleu", "faithfulness", "relevancy"]
        aggregated = {}
        for metric in metrics:
            values = [r[metric] for r in results if metric in r and r[metric] > 0]
            if values:
                aggregated[f"avg_{metric}"] = np.mean(values)
        
        print(f"{'AVERAGE':<12} "
              f"{aggregated.get('avg_bertscore_f1', 0):<15.4f} "
              f"{aggregated.get('avg_rouge_l_f1', 0):<15.4f} "
              f"{aggregated.get('avg_bleu', 0):<10.4f} "
              f"{aggregated.get('avg_faithfulness', 0):<15.4f} "
              f"{aggregated.get('avg_relevancy', 0):<15.4f}")
        print("="*120 + "\n")
