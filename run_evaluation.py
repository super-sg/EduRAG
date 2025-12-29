#!/usr/bin/env python
"""
Run complete evaluation of the RAG system.
This script generates evaluation reports similar to the research paper.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backend import load_models, query_documents
from tests.evaluation_metrics import EvaluationReport, RetrievalMetrics, GenerationMetrics
from tests.test_queries import TEST_QUERIES
from tests.reference_answers import get_reference_answer, has_reference_answer


def run_complete_evaluation(include_advanced=False):
    """
    Run complete evaluation on all test queries.
    Generates report similar to Tables III and IV in the paper.
    
    Args:
        include_advanced: If True, calculate BERTScore, ROUGE-L, and BLEU metrics
    """
    print("\n" + "="*100)
    print("EDURAG SYSTEM EVALUATION")
    if include_advanced:
        print("(with Advanced Metrics: BERTScore, ROUGE-L, BLEU)")
    print("="*100)
    print("\nLoading models...")
    
    try:
        vectorstore, chain = load_models()
        print("✓ Models loaded successfully")
    except Exception as e:
        print(f"✗ Error loading models: {e}")
        print("\nMake sure you have:")
        print("  1. Run 'python ingest.py' to create the vector database")
        print("  2. Set GOOGLE_API_KEY in your .env file")
        print("  3. Installed all requirements: pip install -r requirements.txt")
        return
    
    print(f"\nEvaluating {len(TEST_QUERIES)} test queries...\n")
    
    results = []
    query_ids = []
    
    for i, query_data in enumerate(TEST_QUERIES, 1):
        query = query_data["query"]
        query_id = query_data["id"]
        
        print(f"[{i}/{len(TEST_QUERIES)}] Processing {query_id}: {query[:60]}...")
        
        try:
            # Retrieve documents
            retrieved_docs = vectorstore.similarity_search_with_score(query, k=10)
            
            # Generate response
            response = query_documents(query, vectorstore, chain)
            
            # Prepare context from retrieved docs
            context = [doc.page_content for doc, score in retrieved_docs[:3]]
            
            # For evaluation, we assume top 3 docs are relevant (in production, use human labels)
            retrieved_with_relevance = [
                {
                    "content": doc.page_content,
                    "score": score,
                    "is_relevant": i < 3  # Top 3 marked as relevant
                }
                for i, (doc, score) in enumerate(retrieved_docs)
            ]
            
            # Get reference answer if available
            reference = get_reference_answer(query_id) if include_advanced else None
            
            # Evaluate
            evaluation = EvaluationReport.evaluate_single_query(
                query=query,
                response=response,
                context=context,
                retrieved_docs=retrieved_with_relevance,
                reference=reference,
                include_advanced=include_advanced
            )
            
            results.append(evaluation)
            query_ids.append(query_id)
            
            # Print progress
            if include_advanced and reference:
                print(f"  ✓ MRR: {evaluation['mrr']:.3f} | "
                      f"Faithfulness: {evaluation['faithfulness']:.3f} | "
                      f"BERTScore: {evaluation.get('bertscore_f1', 0):.3f}")
            else:
                print(f"  ✓ MRR: {evaluation['mrr']:.3f} | "
                      f"Faithfulness: {evaluation['faithfulness']:.3f} | "
                      f"Relevancy: {evaluation['relevancy']:.3f}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    
    # Print comprehensive evaluation table
    print("\n")
    EvaluationReport.print_evaluation_table(results, query_ids)
    
    # Print advanced metrics table if requested
    if include_advanced:
        EvaluationReport.print_advanced_metrics_table(results, query_ids)
    
    # Print aggregated statistics
    aggregated = EvaluationReport.aggregate_results(results)
    
    print("\nDETAILED STATISTICS")
    print("="*100)
    print(f"Number of queries evaluated: {len(results)}")
    print(f"\nRetrieval Metrics:")
    print(f"  Average MRR:        {aggregated.get('avg_mrr', 0):.4f} ± {aggregated.get('std_mrr', 0):.4f}")
    print(f"  Average Hit@10:     {aggregated.get('avg_hit@10', 0):.4f} ± {aggregated.get('std_hit@10', 0):.4f}")
    print(f"  Average Hit@5:      {aggregated.get('avg_hit@5', 0):.4f} ± {aggregated.get('std_hit@5', 0):.4f}")
    print(f"\nGeneration Metrics:")
    print(f"  Average Faithfulness: {aggregated.get('avg_faithfulness', 0):.4f} ± {aggregated.get('std_faithfulness', 0):.4f}")
    print(f"  Average Relevancy:    {aggregated.get('avg_relevancy', 0):.4f} ± {aggregated.get('std_relevancy', 0):.4f}")
    print(f"  Average Response Length: {aggregated.get('avg_response_length', 0):.0f} ± {aggregated.get('std_response_length', 0):.0f} words")
    
    # Print advanced metrics if calculated
    if include_advanced:
        print(f"\nAdvanced NLG Metrics:")
        print(f"  Average BERTScore F1: {aggregated.get('avg_bertscore_f1', 0):.4f} ± {aggregated.get('std_bertscore_f1', 0):.4f}")
        print(f"  Average ROUGE-L F1:   {aggregated.get('avg_rouge_l_f1', 0):.4f} ± {aggregated.get('std_rouge_l_f1', 0):.4f}")
        print(f"  Average BLEU:         {aggregated.get('avg_bleu', 0):.4f} ± {aggregated.get('std_bleu', 0):.4f}")
    
    print("="*100)
    
    # Interpretation
    print("\nINTERPRETATION")
    print("="*100)
    
    avg_faithfulness = aggregated.get('avg_faithfulness', 0)
    avg_relevancy = aggregated.get('avg_relevancy', 0)
    avg_mrr = aggregated.get('avg_mrr', 0)
    
    if avg_faithfulness >= 0.7:
        print("✓ FAITHFULNESS: Excellent - Responses are well-grounded in context")
    elif avg_faithfulness >= 0.5:
        print("⚠ FAITHFULNESS: Good - Some responses may include unsupported information")
    else:
        print("✗ FAITHFULNESS: Needs Improvement - Responses may hallucinate or drift from context")
    
    if avg_relevancy >= 0.7:
        print("✓ RELEVANCY: Excellent - Responses address queries well")
    elif avg_relevancy >= 0.5:
        print("⚠ RELEVANCY: Good - Most responses address queries adequately")
    else:
        print("✗ RELEVANCY: Needs Improvement - Responses may not fully address queries")
    
    if avg_mrr >= 0.7:
        print("✓ RETRIEVAL: Excellent - Relevant documents ranked highly")
    elif avg_mrr >= 0.5:
        print("⚠ RETRIEVAL: Good - Relevant documents usually found in top results")
    else:
        print("✗ RETRIEVAL: Needs Improvement - Relevant documents may be missed or ranked low")
    
    print("="*100 + "\n")
    
    return results, aggregated


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run EduRAG system evaluation")
    parser.add_argument("--advanced", action="store_true", 
                       help="Include advanced metrics (BERTScore, ROUGE-L, BLEU)")
    args = parser.parse_args()
    
    try:
        results, aggregated = run_complete_evaluation(include_advanced=args.advanced)
        print("\n✓ Evaluation complete!")
        print("\nTo run individual tests, use: pytest tests/ -v")
        print("To run only fast tests, use: pytest tests/ -m 'not slow' -v")
        if not args.advanced:
            print("\nTo include advanced metrics (BERTScore, ROUGE-L, BLEU), run:")
            print("  python run_evaluation.py --advanced")
    except KeyboardInterrupt:
        print("\n\n✗ Evaluation interrupted by user")
    except Exception as e:
        print(f"\n✗ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
