# Advanced Evaluation Metrics Guide

## 📊 Overview

This guide explains the advanced NLG (Natural Language Generation) evaluation metrics implemented in the EduRAG testing framework:

- **BERTScore** - Semantic similarity using BERT embeddings
- **ROUGE-L** - Longest Common Subsequence matching
- **BLEU** - N-gram overlap scoring

---

## 🎯 BERTScore

### What is BERTScore?

BERTScore uses contextual embeddings from BERT to compute semantic similarity between generated text and reference text.

### How it Works:
1. Embeds each word using BERT
2. Computes cosine similarity between embeddings
3. Finds optimal word-to-word matching
4. Returns Precision, Recall, and F1 scores

### Score Range: **0.0 to 1.0** (higher is better)

### Interpretation:
| Score | Meaning |
|-------|---------|
| **0.9 - 1.0** | Excellent - Nearly identical semantic meaning |
| **0.8 - 0.9** | Good - Strong semantic similarity |
| **0.7 - 0.8** | Fair - Moderate semantic overlap |
| **< 0.7** | Poor - Different semantic meaning |

### Example:

```python
reference = "Newton's first law states that objects remain at rest unless acted upon by force."
response = "The first law of Newton says things stay still without external force."

# BERTScore F1 ≈ 0.85 (Good - same meaning, different words)
```

### When to Use:
- ✅ Evaluating paraphrasing quality
- ✅ Semantic similarity assessment
- ✅ When word-for-word matching is too strict
- ❌ When you need exact word matching

---

## 📏 ROUGE-L

### What is ROUGE-L?

ROUGE-L (Longest Common Subsequence) measures the longest sequence of words that appears in both texts (not necessarily consecutive).

### How it Works:
1. Finds the longest common subsequence (LCS)
2. Calculates based on LCS length
3. Returns Precision, Recall, and F1 scores

### Score Range: **0.0 to 1.0** (higher is better)

### Interpretation:
| Score | Meaning |
|-------|---------|
| **1.0** | Perfect - Identical text |
| **0.7 - 0.9** | Good - Strong overlap with preserved order |
| **0.4 - 0.7** | Fair - Moderate overlap |
| **< 0.4** | Poor - Little common text |

### Example:

```python
reference = "Force equals mass times acceleration"
response1 = "Force equals mass times acceleration"  # ROUGE-L = 1.0
response2 = "Force is mass times acceleration"      # ROUGE-L ≈ 0.83
response3 = "Acceleration times mass equals force"  # ROUGE-L ≈ 0.67 (order matters!)
```

### When to Use:
- ✅ Evaluating text summarization
- ✅ When word order matters
- ✅ Measuring text coherence
- ❌ When semantic meaning matters more than exact words

---

## 🔤 BLEU Score

### What is BLEU?

BLEU (Bilingual Evaluation Understudy) measures n-gram precision between generated text and reference text.

### How it Works:
1. Extracts 1-grams, 2-grams, 3-grams, 4-grams
2. Counts matching n-grams
3. Applies brevity penalty for short responses
4. Returns single score

### Score Range: **0.0 to 1.0** (higher is better)

### Interpretation:
| Score | Meaning |
|-------|---------|
| **> 0.5** | Excellent - High n-gram overlap |
| **0.3 - 0.5** | Good - Moderate overlap |
| **0.1 - 0.3** | Fair - Some overlap |
| **< 0.1** | Poor - Minimal overlap |

### Example:

```python
reference = "The object accelerates due to applied force"
response1 = "The object accelerates due to applied force"    # BLEU ≈ 1.0
response2 = "The object accelerates because of force"        # BLEU ≈ 0.45
response3 = "Objects speed up when pushed"                   # BLEU ≈ 0.05
```

### When to Use:
- ✅ Machine translation evaluation
- ✅ Text generation quality
- ✅ When exact phrasing matters
- ❌ When multiple valid phrasings exist

---

## 🆚 Metric Comparison

| Metric | Measures | Strengths | Limitations |
|--------|----------|-----------|-------------|
| **BERTScore** | Semantic similarity | Captures meaning, robust to paraphrasing | Slower, requires transformers |
| **ROUGE-L** | Sequential overlap | Order-aware, interpretable | Ignores semantics |
| **BLEU** | N-gram precision | Fast, widely used | Strict, multiple references needed |
| **Faithfulness** | Grounding in context | RAG-specific, detects hallucination | Heuristic-based |
| **Relevancy** | Query alignment | Task-specific | Simple implementation |

---

## 🚀 Usage in EduRAG

### 1. Install Dependencies

```bash
pip install bert-score rouge-score nltk
```

### 2. Run Tests

```bash
# Test individual metrics
pytest tests/test_advanced_metrics.py -v

# Test BERTScore only
pytest tests/test_advanced_metrics.py::TestBERTScore -v

# Test ROUGE-L only
pytest tests/test_advanced_metrics.py::TestROUGEL -v
```

### 3. Use in Evaluation

```python
from tests.evaluation_metrics import GenerationMetrics

# Calculate BERTScore
scores = GenerationMetrics.calculate_bertscore(response, reference)
print(f"BERTScore F1: {scores['bertscore_f1']:.4f}")

# Calculate ROUGE-L
scores = GenerationMetrics.calculate_rouge_l(response, reference)
print(f"ROUGE-L F1: {scores['rouge_l_f1']:.4f}")

# Calculate BLEU
score = GenerationMetrics.calculate_bleu_score(response, reference)
print(f"BLEU: {score:.4f}")
```

### 4. Include in Full Evaluation

You need reference answers to use advanced metrics. Create a reference file:

```python
REFERENCE_ANSWERS = {
    "Q1": "Newton's first law states that objects remain at rest...",
    "Q2": "Work is defined as force multiplied by displacement...",
    # ... more references
}
```

Then evaluate:

```python
from tests.evaluation_metrics import EvaluationReport

evaluation = EvaluationReport.evaluate_single_query(
    query=query,
    response=response,
    context=context,
    retrieved_docs=docs,
    reference=reference,  # Add reference answer
    include_advanced=True  # Enable advanced metrics
)
```

---

## 📖 Research Paper Context

The original paper likely used these metrics because:

1. **BERTScore** - Captures semantic correctness of answers
2. **ROUGE-L** - Measures factual overlap with ground truth
3. **BLEU** - Standard baseline for text generation
4. **Faithfulness** - RAG-specific: prevents hallucination
5. **Relevancy** - Task-specific: ensures answer addresses query

---

## 🎯 Recommended Thresholds

### For Physics Q&A (NCERT-level):

| Metric | Excellent | Good | Needs Improvement |
|--------|-----------|------|-------------------|
| BERTScore F1 | > 0.85 | 0.75 - 0.85 | < 0.75 |
| ROUGE-L F1 | > 0.70 | 0.50 - 0.70 | < 0.50 |
| BLEU | > 0.40 | 0.25 - 0.40 | < 0.25 |
| Faithfulness | > 0.80 | 0.65 - 0.80 | < 0.65 |
| Relevancy | > 0.75 | 0.60 - 0.75 | < 0.60 |

---

## 🔧 Troubleshooting

### BERTScore is slow
- Use smaller BERT model: `model_type="distilbert-base-uncased"`
- Reduce batch size
- Use GPU if available

### ROUGE-L gives unexpected scores
- Check for preprocessing differences
- Verify text is properly tokenized
- Consider stemming options

### BLEU scores are very low
- BLEU is strict - consider multiple references
- Add smoothing for short texts
- Check if answers are truly similar

---

## 📚 References

- **BERTScore Paper**: Zhang et al. (2020) - "BERTScore: Evaluating Text Generation with BERT"
- **ROUGE Paper**: Lin (2004) - "ROUGE: A Package for Automatic Evaluation of Summaries"
- **BLEU Paper**: Papineni et al. (2002) - "BLEU: a Method for Automatic Evaluation of Machine Translation"

---

## 🎓 Next Steps

1. **Generate reference answers** for all test queries
2. **Run advanced evaluation**: `python run_evaluation.py --advanced`
3. **Compare with paper results** to benchmark your system
4. **Iterate on prompts/models** to improve scores
5. **Consider human evaluation** for final validation
