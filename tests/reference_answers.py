"""
Reference answers for NCERT Physics test queries.
These are used for calculating advanced metrics (BERTScore, ROUGE-L, BLEU).
"""

REFERENCE_ANSWERS = {
    "Q1": """Newton's first law of motion states that an object at rest will remain at rest 
    and an object in motion will continue in motion with the same velocity (speed and direction) 
    unless acted upon by an external unbalanced force. This property of objects to resist changes 
    in their state of motion is called inertia. For example, a book lying on a table stays at 
    rest unless someone picks it up, and a moving ball continues rolling until friction stops it.""",
    
    "Q2": """Work is said to be done when a force applied on an object causes a displacement in 
    the direction of the force. The work done by a force is defined as the product of the force 
    and the displacement in the direction of the force. Work = Force × Displacement × cos(θ), 
    where θ is the angle between force and displacement. For work to be done, two conditions must 
    be satisfied: (1) A force must be applied, and (2) The object must be displaced in the direction 
    of the force.""",
    
    "Q3": """Distance is the actual length of the path traveled by an object between two points, 
    regardless of direction. It is a scalar quantity and is always positive. Displacement is the 
    shortest straight-line distance between the initial and final positions of an object, measured 
    in a particular direction. It is a vector quantity and can be positive, negative, or zero. 
    For example, if you walk 3 meters east and then 4 meters north, the distance traveled is 7 meters, 
    but the displacement is 5 meters in the northeast direction.""",
    
    "Q4": """The law of conservation of energy states that energy can neither be created nor destroyed; 
    it can only be transformed from one form to another. The total energy of an isolated system remains 
    constant. For example, in a pendulum, potential energy converts to kinetic energy and back. When 
    you drop a ball, its gravitational potential energy converts to kinetic energy as it falls. In 
    hydroelectric dams, the potential energy of water is converted to kinetic energy and then to 
    electrical energy.""",
    
    "Q5": """The three equations of motion for uniformly accelerated motion can be derived using 
    velocity-time graphs. First equation: v = u + at, derived from the slope of v-t graph (acceleration). 
    Second equation: s = ut + ½at², derived from the area under the v-t graph representing displacement. 
    Third equation: v² = u² + 2as, derived by eliminating time from the first two equations. Here, 
    u is initial velocity, v is final velocity, a is acceleration, t is time, and s is displacement.""",
    
    "Q6": """Gravitational force is the force of attraction between any two objects in the universe. 
    The universal law of gravitation, stated by Newton, says that every object in the universe attracts 
    every other object with a force that is directly proportional to the product of their masses and 
    inversely proportional to the square of the distance between their centers. Mathematically: 
    F = G(m₁m₂)/r², where G is the universal gravitational constant (6.67 × 10⁻¹¹ Nm²/kg²).""",
    
    "Q7": """Archimedes' principle states that when a body is partially or completely immersed in a 
    fluid, it experiences an upward force called buoyant force (or upthrust), which is equal to the 
    weight of the fluid displaced by the body. Applications include: (1) Ships float because the 
    buoyant force equals their weight, (2) Submarines control buoyancy by adjusting water in tanks, 
    (3) Hydrometers measure liquid density using buoyancy, (4) Hot air balloons rise because hot air 
    is less dense than surrounding air.""",
    
    "Q8": """Heat is a form of energy that flows from a body at higher temperature to a body at lower 
    temperature. It is measured in joules (J) or calories (cal). Temperature is the degree of hotness 
    or coldness of a body, measured in degrees Celsius (°C), Kelvin (K), or Fahrenheit (°F). The main 
    difference is that heat is energy in transit, while temperature is a measure of the average kinetic 
    energy of molecules. For example, a cup of water at 50°C has less heat than a bucket of water at 
    50°C, though both have the same temperature.""",
    
    "Q9": """Ohm's law states that the electric current flowing through a conductor is directly 
    proportional to the potential difference (voltage) applied across its ends, provided the physical 
    conditions (temperature, etc.) remain constant. Mathematically: V = IR, where V is voltage, I is 
    current, and R is resistance. The resistance of a conductor depends on: (1) Length - resistance 
    increases with length, (2) Cross-sectional area - resistance decreases with larger area, 
    (3) Material - different materials have different resistivities, (4) Temperature - for most 
    conductors, resistance increases with temperature.""",
    
    "Q10": """The principle of conservation of momentum states that the total momentum of a system 
    remains constant if no external force acts on it. This can be derived from Newton's second and 
    third laws. When two objects collide, the force exerted by object A on object B is equal and 
    opposite to the force exerted by object B on object A (Newton's third law). Since F = ma = m(Δv/Δt), 
    and forces are equal and opposite, the change in momentum of A equals the negative change in momentum 
    of B. Therefore, total momentum before collision equals total momentum after collision.""",
    
    "Q11": """Refraction of light is the bending of light when it passes from one transparent medium 
    to another due to change in its speed. The laws of refraction are: (1) The incident ray, refracted 
    ray, and normal to the interface at the point of incidence all lie in the same plane. (2) The ratio 
    of sine of angle of incidence to the sine of angle of refraction is constant for a given pair of 
    media. This is known as Snell's law: sin(i)/sin(r) = n₂/n₁, where n is the refractive index.""",
    
    "Q12": """Kinetic energy is the energy possessed by a body due to its motion. Potential energy is 
    the energy possessed by a body due to its position or configuration. The expression for kinetic 
    energy can be derived: Consider a body of mass m at rest. A force F is applied, causing acceleration a 
    over distance s. Work done W = F × s = ma × s. Using v² = u² + 2as (with u = 0), we get s = v²/2a. 
    Therefore, W = ma × v²/2a = ½mv². This work done is stored as kinetic energy, so KE = ½mv².""",
    
    "Q13": """Power is the rate at which work is done or energy is transferred. It measures how quickly 
    work is performed. Mathematically: Power = Work done / Time taken, or P = W/t. The SI unit of power 
    is the watt (W), named after James Watt. One watt is defined as the power of an agent which does work 
    at the rate of 1 joule per second. 1 W = 1 J/s. Other units include kilowatt (kW = 1000 W) and 
    horsepower (1 hp ≈ 746 W).""",
    
    "Q14": """There are three methods of heat transfer: (1) Conduction - heat transfer through direct 
    contact between molecules in solids. Example: A metal spoon becomes hot when placed in hot tea. 
    (2) Convection - heat transfer through the actual movement of fluid (liquid or gas). Example: Water 
    in a pot heats up as hot water rises and cool water sinks, creating convection currents. 
    (3) Radiation - heat transfer through electromagnetic waves without requiring a medium. Example: 
    Heat from the Sun reaches Earth through radiation across empty space.""",
    
    "Q15": """Fleming's left-hand rule helps determine the direction of force on a current-carrying 
    conductor in a magnetic field. The rule states: Stretch the thumb, forefinger, and middle finger 
    of your left hand mutually perpendicular to each other. If the forefinger points in the direction 
    of the magnetic field, and the middle finger points in the direction of current, then the thumb 
    points in the direction of force (motion). This principle is used in electric motors, where a 
    current-carrying coil in a magnetic field experiences force and rotates, converting electrical 
    energy to mechanical energy."""
}

def get_reference_answer(query_id: str) -> str:
    """Get reference answer for a query ID."""
    return REFERENCE_ANSWERS.get(query_id, "")

def has_reference_answer(query_id: str) -> bool:
    """Check if reference answer exists for a query ID."""
    return query_id in REFERENCE_ANSWERS
