# How to Run Evaluation with Advanced Metrics

## 🎯 Overview

The evaluation system now supports **two modes**:

1. **Standard Mode** - Basic metrics (MRR, Faithfulness, Relevancy)
2. **Advanced Mode** - Includes BERTScore, ROUGE-L, and BLEU

---

## 🚀 Quick Start

### **Option 1: Standard Evaluation (Fast)**
```powershell
python run_evaluation.py
```

**Output includes:**
- MRR (Mean Reciprocal Rank)
- Hit@10, Hit@5
- Faithfulness Score
- Relevancy Score
- Response Length

**Time:** ~30 seconds for 15 queries

---

### **Option 2: Advanced Evaluation (With BERTScore, ROUGE-L, BLEU)**
```powershell
python run_evaluation.py --advanced
```

**Output includes everything from Standard Mode PLUS:**
- **BERTScore F1** - Semantic similarity
- **ROUGE-L F1** - Sequence matching
- **BLEU** - N-gram overlap

**Time:** ~2-3 minutes for 15 queries (slower due to BERT calculations)

---

## 📊 Sample Output

### Standard Mode:
```
==================================================================================================
EVALUATION RESULTS - RAG SYSTEM PERFORMANCE
==================================================================================================
Query ID     MRR        Hit@10     Faithfulness    Relevancy       Length    
--------------------------------------------------------------------------------------------------
Q1           1.0000     1.0000     0.8500          0.7200          145       
Q2           0.5000     1.0000     0.7800          0.8100          132       
Q3           0.3333     1.0000     0.6900          0.7500          118       
...
AVERAGE      0.6667     1.0000     0.7733          0.7600          131       
==================================================================================================
```

### Advanced Mode (Additional Table):
```
========================================================================================================================
ADVANCED METRICS - NLG EVALUATION
========================================================================================================================
Query ID     BERTScore F1    ROUGE-L F1      BLEU       Faithfulness    Relevancy      
------------------------------------------------------------------------------------------------------------------------
Q1           0.8756          0.6543          0.3521     0.8500          0.7200         
Q2           0.8923          0.7012          0.4123     0.7800          0.8100         
Q3           0.8645          0.6234          0.3012     0.6900          0.7500         
...
AVERAGE      0.8775          0.6596          0.3552     0.7733          0.7600         
========================================================================================================================

DETAILED STATISTICS
==================================================================================================
Advanced NLG Metrics:
  Average BERTScore F1: 0.8775 ± 0.0234
  Average ROUGE-L F1:   0.6596 ± 0.0412
  Average BLEU:         0.3552 ± 0.0567
==================================================================================================
```

---

## 📦 Installation

Before using advanced metrics, install the required packages:

```powershell
pip install bert-score rouge-score nltk
```

Or install all test requirements:

```powershell
pip install -r test_requirements.txt
```

---

## 🎓 What Do These Scores Mean?

### BERTScore F1 (Semantic Similarity)
- **> 0.85** = Excellent - Answer has correct meaning
- **0.75-0.85** = Good - Answer is mostly correct
- **< 0.75** = Needs improvement - Meaning differs

### ROUGE-L F1 (Text Overlap)
- **> 0.70** = Excellent - Strong factual overlap
- **0.50-0.70** = Good - Adequate overlap
- **< 0.50** = Needs improvement - Different wording

### BLEU (Exact Matching)
- **> 0.40** = Excellent - Very similar phrasing
- **0.25-0.40** = Good - Some matching phrases
- **< 0.25** = Needs improvement - Different phrasing

### Faithfulness (Grounding in Context)
- **> 0.80** = Excellent - Well-grounded, no hallucination
- **0.65-0.80** = Good - Mostly grounded
- **< 0.65** = Needs improvement - May hallucinate

### Relevancy (Addresses Query)
- **> 0.75** = Excellent - Directly answers question
- **0.60-0.75** = Good - Mostly relevant
- **< 0.60** = Needs improvement - May miss the point

---

## 🔍 Understanding the Reference Answers

Advanced metrics require **reference answers** to compare against. We've created reference answers for all 15 NCERT Physics questions in `tests/reference_answers.py`.

**Example:**
```python
Query: "What is Newton's first law of motion?"

Reference Answer (from reference_answers.py):
"Newton's first law of motion states that an object at rest will remain 
at rest and an object in motion will continue in motion with the same 
velocity unless acted upon by an external unbalanced force..."

Generated Answer (from your RAG system):
"The first law of Newton says objects stay at rest or in motion unless 
an external force acts on them. This is called inertia."

BERTScore: 0.87 (High - same meaning)
ROUGE-L: 0.62 (Good - some word overlap)
BLEU: 0.32 (Fair - different phrasing)
```

---

## 🛠️ Command Line Options

```powershell
# Standard evaluation
python run_evaluation.py

# Advanced evaluation with all metrics
python run_evaluation.py --advanced

# See help
python run_evaluation.py --help
```

---

## 📈 Comparing Your Results

### Research Paper Benchmarks:
| Metric | Paper Result | Your Goal |
|--------|--------------|-----------|
| MRR | 1.00 | > 0.80 |
| Faithfulness | 0.67-1.00 | > 0.75 |
| Relevancy | 0.60-0.93 | > 0.70 |
| BERTScore | N/A | > 0.85 |
| ROUGE-L | N/A | > 0.65 |

---

## 🎯 Tips for Better Scores

### To Improve BERTScore (Semantic Correctness):
- ✅ Improve prompt engineering
- ✅ Use better LLM (e.g., GPT-4 vs GPT-3.5)
- ✅ Retrieve more relevant context

### To Improve ROUGE-L (Factual Overlap):
- ✅ Ensure textbook content is ingested properly
- ✅ Improve chunk size and overlap
- ✅ Use better retrieval strategy

### To Improve BLEU (Exact Matching):
- ✅ Fine-tune the model on NCERT text
- ✅ Include more examples in prompt
- ✅ Use temperature = 0 for deterministic output

### To Improve Faithfulness (No Hallucination):
- ✅ Add "stick to the context" instructions
- ✅ Lower LLM temperature
- ✅ Improve retrieval relevance

### To Improve Relevancy:
- ✅ Better query understanding
- ✅ Improve retrieval with query expansion
- ✅ Add examples of good answers in prompt

---

## 🧪 Testing Individual Queries

To test a specific query with advanced metrics:

```python
from backend import load_models, query_documents
from tests.evaluation_metrics import EvaluationReport
from tests.reference_answers import get_reference_answer

vectorstore, chain = load_models()

query = "What is Newton's first law of motion?"
response = query_documents(query, vectorstore, chain)
reference = get_reference_answer("Q1")

docs = vectorstore.similarity_search(query, k=10)
context = [doc.page_content for doc in docs[:3]]

retrieved_with_relevance = [
    {"content": doc.page_content, "is_relevant": i < 3}
    for i, doc in enumerate(docs)
]

evaluation = EvaluationReport.evaluate_single_query(
    query=query,
    response=response,
    context=context,
    retrieved_docs=retrieved_with_relevance,
    reference=reference,
    include_advanced=True
)

print(f"BERTScore F1: {evaluation['bertscore_f1']:.4f}")
print(f"ROUGE-L F1: {evaluation['rouge_l_f1']:.4f}")
print(f"BLEU: {evaluation['bleu']:.4f}")
```

---

## 📝 Summary

| Command | Metrics | Time | Use Case |
|---------|---------|------|----------|
| `python run_evaluation.py` | Standard | ~30s | Quick testing |
| `python run_evaluation.py --advanced` | All metrics | ~2-3min | Full evaluation |
| `pytest tests/test_advanced_metrics.py` | Test suite | ~1min | Development |

---

**Ready to go!** Run `python run_evaluation.py --advanced` to see all metrics in action! 🚀
