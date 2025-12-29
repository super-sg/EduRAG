# Quick Start Guide for Testing

## 1. Install Dependencies
```powershell
pip install -r test_requirements.txt
```

## 2. Run Tests

### Option A: Run All Tests with pytest
```powershell
pytest
```

### Option B: Run Complete Evaluation (Paper-style Report)
```powershell
python run_evaluation.py
```

This will generate output similar to Tables III & IV in the research paper:
- Retrieval metrics (MRR, Hit@k)
- Generation metrics (Faithfulness, Relevancy)
- Comprehensive evaluation table

### Option C: Run Specific Tests

**Just retrieval tests:**
```powershell
pytest tests/test_retrieval.py -v
```

**Just generation tests:**
```powershell
pytest tests/test_generation.py -v
```

**Skip slow tests:**
```powershell
pytest -m "not slow"
```

## 3. View Coverage Report
```powershell
pytest --cov=backend --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Expected Output

When you run `python run_evaluation.py`, you'll see:

```
==================================================================================================
EDURAG SYSTEM EVALUATION
==================================================================================================

Loading models...
✓ Models loaded successfully

Evaluating 10 test queries...

[1/10] Processing Q1: Discuss the challenges and setbacks faced during the...
  ✓ MRR: 1.000 | Faithfulness: 0.850 | Relevancy: 0.720

[2/10] Processing Q2: Explain the significance of technology in the develop...
  ✓ MRR: 0.500 | Faithfulness: 0.780 | Relevancy: 0.810

...

==================================================================================================
EVALUATION RESULTS - RAG SYSTEM PERFORMANCE
==================================================================================================
Query ID     MRR        Hit@10     Faithfulness    Relevancy       Length    
--------------------------------------------------------------------------------------------------
Q1           1.0000     1.0000     0.8500          0.7200          145       
Q2           0.5000     1.0000     0.7800          0.8100          132       
...
AVERAGE      0.6667     1.0000     0.7733          0.7600          131       
==================================================================================================
```

## Metrics Explained

- **MRR (Mean Reciprocal Rank)**: How highly relevant documents are ranked (0-1, higher is better)
- **Hit@k**: Whether relevant documents appear in top k results (0 or 1)
- **Faithfulness**: How well response is grounded in retrieved context (0-1)
- **Relevancy**: How well response addresses the query (0-1)
- **Length**: Response length in words

## Troubleshooting

**"Chroma database not found"**
→ Run `python ingest.py` first

**"GOOGLE_API_KEY not set"**
→ Create `.env` file with your API key

**Tests fail**
→ Check `README_TESTING.md` for detailed troubleshooting
