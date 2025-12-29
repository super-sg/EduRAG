"""
Test queries dataset similar to Table I in the paper.
These queries test various aspects of the RAG system with NCERT-level Physics questions.
"""

# NCERT-level Physics queries for testing retrieval and generation
TEST_QUERIES = [
    {
        "id": "Q1",
        "query": "What is Newton's first law of motion? Explain with examples from daily life.",
        "category": "laws_of_motion",
        "expected_topics": ["newton", "inertia", "motion", "force", "examples"]
    },
    {
        "id": "Q2",
        "query": "Define work done by a force. What are the conditions for work to be done?",
        "category": "work_energy_power",
        "expected_topics": ["work", "force", "displacement", "conditions"]
    },
    {
        "id": "Q3",
        "query": "Explain the difference between distance and displacement with suitable examples.",
        "category": "kinematics",
        "expected_topics": ["distance", "displacement", "scalar", "vector", "examples"]
    },
    {
        "id": "Q4",
        "query": "What is the law of conservation of energy? Provide examples to illustrate this law.",
        "category": "energy",
        "expected_topics": ["conservation", "energy", "law", "examples", "transformation"]
    },
    {
        "id": "Q5",
        "query": "Derive the equations of motion for uniformly accelerated motion using graphical method.",
        "category": "kinematics",
        "expected_topics": ["equations", "motion", "acceleration", "velocity", "graph"]
    },
    {
        "id": "Q6",
        "query": "What is gravitational force? State the universal law of gravitation.",
        "category": "gravitation",
        "expected_topics": ["gravity", "gravitational force", "universal law", "newton"]
    },
    {
        "id": "Q7",
        "query": "Explain Archimedes' principle and its applications in daily life.",
        "category": "fluid_mechanics",
        "expected_topics": ["archimedes", "buoyancy", "upthrust", "applications", "floating"]
    },
    {
        "id": "Q8",
        "query": "What is the difference between heat and temperature? Explain with examples.",
        "category": "thermodynamics",
        "expected_topics": ["heat", "temperature", "difference", "energy", "measurement"]
    },
    {
        "id": "Q9",
        "query": "State and explain Ohm's law. What are the factors affecting the resistance of a conductor?",
        "category": "electricity",
        "expected_topics": ["ohm", "law", "resistance", "current", "voltage", "factors"]
    },
    {
        "id": "Q10",
        "query": "What is the principle of conservation of momentum? Derive it from Newton's laws of motion.",
        "category": "laws_of_motion",
        "expected_topics": ["momentum", "conservation", "newton", "collision", "derivation"]
    },
    {
        "id": "Q11",
        "query": "Explain the phenomenon of refraction of light. State the laws of refraction.",
        "category": "optics",
        "expected_topics": ["refraction", "light", "snell's law", "bending", "medium"]
    },
    {
        "id": "Q12",
        "query": "What is kinetic energy and potential energy? Derive the expression for kinetic energy.",
        "category": "work_energy_power",
        "expected_topics": ["kinetic", "potential", "energy", "expression", "derivation"]
    },
    {
        "id": "Q13",
        "query": "Explain the concept of power. What is the SI unit of power?",
        "category": "work_energy_power",
        "expected_topics": ["power", "work", "time", "unit", "watt"]
    },
    {
        "id": "Q14",
        "query": "What are the three methods of heat transfer? Explain each with examples.",
        "category": "thermodynamics",
        "expected_topics": ["conduction", "convection", "radiation", "heat transfer", "examples"]
    },
    {
        "id": "Q15",
        "query": "State Fleming's left-hand rule and explain its application in electric motors.",
        "category": "electromagnetism",
        "expected_topics": ["fleming", "left hand rule", "magnetic field", "current", "motor"]
    }
]

def get_test_queries():
    """Returns the list of test queries."""
    return TEST_QUERIES

def get_query_by_id(query_id):
    """Returns a specific test query by ID."""
    for query in TEST_QUERIES:
        if query["id"] == query_id:
            return query
    return None

def get_queries_by_category(category):
    """Returns all queries of a specific category."""
    return [q for q in TEST_QUERIES if q["category"] == category]
