# Testing Guide for EduRAG

This guide explains how to run tests and evaluations for the EduRAG system, similar to the evaluation framework described in the research paper.

## Overview

The testing framework includes:
- **Retrieval Metrics**: MRR (Mean Reciprocal Rank), Hit@k, Precision@k
- **Generation Metrics**: Faithfulness, Relevancy, Response Length
- **Test Queries**: 10 predefined queries covering various question types
- **Evaluation Reports**: Similar to Tables III and IV in the paper

## Setup

1. Install test dependencies:
```bash
pip install -r test_requirements.txt
```

2. Make sure you have ingested documents:
```bash
python ingest.py
```

3. Set up your `.env` file with API keys:
```
GOOGLE_API_KEY=your_key_here
```

## Running Tests

### Quick Start - Run All Tests
```bash
pytest
```

### Run Specific Test Categories

**Unit tests only:**
```bash
pytest -m unit
```

**Integration tests only:**
```bash
pytest -m integration
```

**Exclude slow tests:**
```bash
pytest -m "not slow"
```

### Run Specific Test Files

**Test retrieval component:**
```bash
pytest tests/test_retrieval.py -v
```

**Test generation component:**
```bash
pytest tests/test_generation.py -v
```

**Test complete system:**
```bash
pytest tests/test_system_integration.py -v
```

### Run with Coverage Report

```bash
pytest --cov=backend --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the coverage report.

## Complete Evaluation (Like the Paper)

Run the complete evaluation script to generate reports similar to the research paper:

```bash
python run_evaluation.py
```

This will:
1. Load all models and the vector database
2. Run all test queries through the system
3. Calculate retrieval and generation metrics
4. Generate a comprehensive evaluation table
5. Print interpretation of results

### Sample Output

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

## Understanding the Metrics

### Retrieval Metrics

**MRR (Mean Reciprocal Rank)**
- Range: 0.0 to 1.0
- Higher is better
- 1.0 = most relevant document is ranked first
- 0.5 = most relevant document is ranked second
- Good score: > 0.7

**Hit@k**
- Range: 0.0 or 1.0
- 1.0 = at least one relevant document in top k results
- 0.0 = no relevant documents in top k
- Good score: > 0.9 for Hit@10

### Generation Metrics

**Faithfulness**
- Range: 0.0 to 1.0
- Measures if response is grounded in retrieved context
- 1.0 = fully grounded, no hallucination
- 0.0 = response contains unsupported information
- Good score: > 0.7

**Relevancy**
- Range: 0.0 to 1.0
- Measures if response addresses the query
- 1.0 = perfectly relevant
- 0.0 = completely irrelevant
- Good score: > 0.7

## Test Structure

```
tests/
├── __init__.py                  # Test suite initialization
├── conftest.py                  # Pytest configuration and fixtures
├── test_queries.py              # Test query dataset (Table I)
├── evaluation_metrics.py        # Metric calculations
├── test_retrieval.py           # Retrieval component tests
├── test_generation.py          # Generation component tests
└── test_system_integration.py  # End-to-end tests
```

## Adding Custom Test Queries

Edit `tests/test_queries.py` and add your queries:

```python
TEST_QUERIES.append({
    "id": "Q11",
    "query": "Your question here?",
    "category": "your_category",
    "expected_topics": ["topic1", "topic2"]
})
```

## Continuous Integration

To run tests in CI/CD:

```bash
# Fast tests only
pytest -m "not slow" --cov --cov-report=xml

# All tests with timeout
pytest --timeout=300 --cov
```

## Troubleshooting

**Error: "Chroma database not found"**
- Run `python ingest.py` first to create the vector database

**Error: "GOOGLE_API_KEY not set"**
- Create a `.env` file with your Google API key

**Tests are too slow**
- Run with `-m "not slow"` to skip slow tests
- Use `-n auto` for parallel execution: `pip install pytest-xdist && pytest -n auto`

**Import errors**
- Make sure all dependencies are installed: `pip install -r requirements.txt -r test_requirements.txt`

## Comparing with Paper Results

The paper reports:
- MRR: 1.00 (perfect retrieval)
- Faithfulness: 0.67-1.00 (depending on model)
- Relevancy: 0.60-0.93 (depending on model)

Your results may vary based on:
- Quality and quantity of ingested documents
- LLM model used (Gemini vs GPT)
- Embedding model configuration
- Chunk size and overlap settings

## Next Steps

1. **Improve Retrieval**: Adjust chunk size, overlap, or embedding model
2. **Improve Generation**: Fine-tune prompts or use better LLM
3. **Add More Queries**: Expand test coverage with domain-specific questions
4. **Human Evaluation**: Replace automated relevance judgments with human annotations
5. **A/B Testing**: Compare different model configurations

## References

See the research paper for detailed methodology and baseline comparisons.
