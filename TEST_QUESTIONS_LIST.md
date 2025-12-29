# NCERT Physics Test Questions

This document lists all test queries used for evaluating the EduRAG system.

---

## 📚 Test Query Dataset

**Total Questions:** 15  
**Subject:** Physics (NCERT Level)  
**Categories:** Laws of Motion, Kinematics, Work Energy Power, Gravitation, Fluid Mechanics, Thermodynamics, Electricity, Optics, Electromagnetism

---

## 📝 Complete Question List

### **Q1: Newton's First Law**
**Category:** Laws of Motion  
**Question:** What is Newton's first law of motion? Explain with examples from daily life.  
**Expected Topics:** newton, inertia, motion, force, examples

---

### **Q2: Work Done**
**Category:** Work, Energy & Power  
**Question:** Define work done by a force. What are the conditions for work to be done?  
**Expected Topics:** work, force, displacement, conditions

---

### **Q3: Distance vs Displacement**
**Category:** Kinematics  
**Question:** Explain the difference between distance and displacement with suitable examples.  
**Expected Topics:** distance, displacement, scalar, vector, examples

---

### **Q4: Conservation of Energy**
**Category:** Energy  
**Question:** What is the law of conservation of energy? Provide examples to illustrate this law.  
**Expected Topics:** conservation, energy, law, examples, transformation

---

### **Q5: Equations of Motion**
**Category:** Kinematics  
**Question:** Derive the equations of motion for uniformly accelerated motion using graphical method.  
**Expected Topics:** equations, motion, acceleration, velocity, graph

---

### **Q6: Gravitational Force**
**Category:** Gravitation  
**Question:** What is gravitational force? State the universal law of gravitation.  
**Expected Topics:** gravity, gravitational force, universal law, newton

---

### **Q7: Archimedes' Principle**
**Category:** Fluid Mechanics  
**Question:** Explain Archimedes' principle and its applications in daily life.  
**Expected Topics:** archimedes, buoyancy, upthrust, applications, floating

---

### **Q8: Heat vs Temperature**
**Category:** Thermodynamics  
**Question:** What is the difference between heat and temperature? Explain with examples.  
**Expected Topics:** heat, temperature, difference, energy, measurement

---

### **Q9: Ohm's Law**
**Category:** Electricity  
**Question:** State and explain Ohm's law. What are the factors affecting the resistance of a conductor?  
**Expected Topics:** ohm, law, resistance, current, voltage, factors

---

### **Q10: Conservation of Momentum**
**Category:** Laws of Motion  
**Question:** What is the principle of conservation of momentum? Derive it from Newton's laws of motion.  
**Expected Topics:** momentum, conservation, newton, collision, derivation

---

### **Q11: Refraction of Light**
**Category:** Optics  
**Question:** Explain the phenomenon of refraction of light. State the laws of refraction.  
**Expected Topics:** refraction, light, snell's law, bending, medium

---

### **Q12: Kinetic and Potential Energy**
**Category:** Work, Energy & Power  
**Question:** What is kinetic energy and potential energy? Derive the expression for kinetic energy.  
**Expected Topics:** kinetic, potential, energy, expression, derivation

---

### **Q13: Power**
**Category:** Work, Energy & Power  
**Question:** Explain the concept of power. What is the SI unit of power?  
**Expected Topics:** power, work, time, unit, watt

---

### **Q14: Heat Transfer Methods**
**Category:** Thermodynamics  
**Question:** What are the three methods of heat transfer? Explain each with examples.  
**Expected Topics:** conduction, convection, radiation, heat transfer, examples

---

### **Q15: Fleming's Left-Hand Rule**
**Category:** Electromagnetism  
**Question:** State Fleming's left-hand rule and explain its application in electric motors.  
**Expected Topics:** fleming, left hand rule, magnetic field, current, motor

---

## 📊 Question Distribution by Category

| Category | Number of Questions |
|----------|---------------------|
| **Work, Energy & Power** | 3 questions (Q2, Q12, Q13) |
| **Laws of Motion** | 2 questions (Q1, Q10) |
| **Kinematics** | 2 questions (Q3, Q5) |
| **Thermodynamics** | 2 questions (Q8, Q14) |
| **Gravitation** | 1 question (Q6) |
| **Fluid Mechanics** | 1 question (Q7) |
| **Electricity** | 1 question (Q9) |
| **Optics** | 1 question (Q11) |
| **Electromagnetism** | 1 question (Q15) |
| **Energy (General)** | 1 question (Q4) |

---

## 🎯 Question Types

### **Conceptual Questions** (40%)
- Q1, Q2, Q3, Q4, Q6, Q8

### **Law/Principle Questions** (33%)
- Q4, Q6, Q7, Q9, Q11

### **Derivation Questions** (20%)
- Q5, Q10, Q12

### **Application Questions** (27%)
- Q7, Q14, Q15

### **Explanation with Examples** (53%)
- Q1, Q3, Q4, Q7, Q8, Q14

---

## 🔍 Question Complexity Levels

| Level | Questions | Description |
|-------|-----------|-------------|
| **Basic** | Q1, Q2, Q3, Q6, Q8, Q13 | Definition and basic concepts |
| **Intermediate** | Q4, Q7, Q9, Q11, Q14, Q15 | Explanations and applications |
| **Advanced** | Q5, Q10, Q12 | Derivations and proofs |

---

## 💡 Usage in Testing

These questions are used in:

1. **Retrieval Testing** (`test_retrieval.py`)
   - Tests if relevant documents are retrieved
   - Measures MRR, Hit@k, Precision@k

2. **Generation Testing** (`test_generation.py`)
   - Tests response quality
   - Measures Faithfulness, Relevancy

3. **Advanced Metrics** (`test_advanced_metrics.py`)
   - Tests semantic similarity (BERTScore)
   - Tests sequence matching (ROUGE-L)
   - Tests n-gram overlap (BLEU)

4. **Full Evaluation** (`run_evaluation.py`)
   - Runs all 15 questions through the system
   - Generates comprehensive report

---

## 🚀 How to Use

### Run evaluation on all questions:
```powershell
python run_evaluation.py
```

### Test specific question:
```python
from tests.test_queries import get_query_by_id

query = get_query_by_id("Q1")
print(query["query"])
# Output: "What is Newton's first law of motion? Explain with examples from daily life."
```

### Filter by category:
```python
from tests.test_queries import get_queries_by_category

motion_queries = get_queries_by_category("laws_of_motion")
print(f"Found {len(motion_queries)} questions about laws of motion")
```

---

## 📖 NCERT Chapters Covered

These questions cover topics from:
- **Class 9 Physics**: Force and Laws of Motion, Work and Energy, Gravitation, Sound
- **Class 10 Physics**: Light, Electricity, Magnetic Effects of Electric Current
- **Class 11 Physics**: Motion, Laws of Motion, Work Energy and Power, Mechanical Properties of Fluids
- **Class 12 Physics**: Electromagnetism, Optics

---

## ✅ Expected Answer Quality

For each question, a good answer should:
- ✓ Directly address the question
- ✓ Provide clear explanation
- ✓ Include examples (when asked)
- ✓ State relevant laws/principles
- ✓ Show derivations (when asked)
- ✓ Use correct scientific terminology
- ✓ Be grounded in provided textbook context

---

## 📊 Evaluation Metrics Applied

Each question's answer is evaluated using:

| Metric | Range | Good Score |
|--------|-------|------------|
| MRR (Retrieval) | 0-1 | > 0.80 |
| Hit@10 (Retrieval) | 0 or 1 | 1.0 |
| Faithfulness | 0-1 | > 0.75 |
| Relevancy | 0-1 | > 0.70 |
| BERTScore F1 | 0-1 | > 0.80 |
| ROUGE-L F1 | 0-1 | > 0.65 |
| BLEU | 0-1 | > 0.30 |

---

## 🎓 Adding More Questions

To add new questions, edit `tests/test_queries.py`:

```python
TEST_QUERIES.append({
    "id": "Q16",
    "query": "Your physics question here?",
    "category": "your_category",
    "expected_topics": ["topic1", "topic2", "topic3"]
})
```

---

## 📝 Notes

- Questions are designed to test different aspects of RAG system
- Mix of easy, medium, and hard questions
- Cover breadth of NCERT Physics curriculum
- Include both theory and application questions
- Some require derivations/mathematical explanations
- Others focus on conceptual understanding

---

**For detailed testing instructions, see:**
- `README_TESTING.md` - Complete testing guide
- `TESTING_QUICKSTART.md` - Quick start guide
- `ADVANCED_METRICS_GUIDE.md` - Metrics explanation
