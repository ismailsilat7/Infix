-- Insert topics for Pure Mathematics 3
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Algebra', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Logarithmic and Exponential Functions', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Trigonometry', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Differentiation', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Integration', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Numerical Solution of Equations', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Vectors', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Differential Equations', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Complex Numbers', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3'))
ON CONFLICT DO NOTHING;

-- Insert topics for Mechanics
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Forces and Equilibrium', (SELECT id FROM categories WHERE name = 'Mechanics')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Kinematics of Motion in a Straight Line', (SELECT id FROM categories WHERE name = 'Mechanics')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Momentum', (SELECT id FROM categories WHERE name = 'Mechanics')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Newton’s Laws of Motion', (SELECT id FROM categories WHERE name = 'Mechanics')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Energy, Work and Power', (SELECT id FROM categories WHERE name = 'Mechanics'))
ON CONFLICT DO NOTHING;

-- Insert topics for Probability & Statistics 2
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'The Poisson Distribution', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Linear Combinations of Random Variables', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Continuous Random Variables', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Sampling and Estimation', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Hypothesis Tests', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2'))
ON CONFLICT DO NOTHING;

-- Insert topics for Physical Chemistry
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Chemical Energetics', (SELECT id FROM categories WHERE name = 'Physical Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Electrochemistry', (SELECT id FROM categories WHERE name = 'Physical Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Equilibria', (SELECT id FROM categories WHERE name = 'Physical Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Reaction Kinetics', (SELECT id FROM categories WHERE name = 'Physical Chemistry'))
ON CONFLICT DO NOTHING;

-- Insert topics for Inorganic Chemistry
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Group 2', (SELECT id FROM categories WHERE name = 'Inorganic Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Chemistry of Transition Elements', (SELECT id FROM categories WHERE name = 'Inorganic Chemistry'))
ON CONFLICT DO NOTHING;

-- Insert topics for Organic Chemistry
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'An Introduction to A Level Organic Chemistry', (SELECT id FROM categories WHERE name = 'Organic Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Hydrocarbons', (SELECT id FROM categories WHERE name = 'Organic Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Halogen Compounds', (SELECT id FROM categories WHERE name = 'Organic Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Hydroxy Compounds', (SELECT id FROM categories WHERE name = 'Organic Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Carboxylic Acids and Derivatives', (SELECT id FROM categories WHERE name = 'Organic Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Nitrogen Compounds', (SELECT id FROM categories WHERE name = 'Organic Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Polymerisation', (SELECT id FROM categories WHERE name = 'Organic Chemistry')),
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Organic Synthesis', (SELECT id FROM categories WHERE name = 'Organic Chemistry'))
ON CONFLICT DO NOTHING;

-- Insert topics for Analysis
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9701-A2' AND name = 'Chemistry'), 'Analytical Techniques', (SELECT id FROM categories WHERE name = 'Analysis'))
ON CONFLICT DO NOTHING;

-- Insert topics for Physics A2 without categories
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Motion in a Circle', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Gravitational Fields', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Temperature', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Ideal Gases', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Thermodynamics', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Oscillations', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Electric Fields', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Capacitance', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Magnetic Fields', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Alternating Currents', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Quantum Physics', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Nuclear Physics', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Medical Physics', NULL),
((SELECT id FROM courses WHERE course_code = '9702-A2' AND name = 'Physics'), 'Astronomy and Cosmology', NULL)
ON CONFLICT DO NOTHING;

-- Insert topics for Data Representation
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'User-defined Data Types', (SELECT id FROM categories WHERE name = 'Data Representation')),
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'File Organisation and Access', (SELECT id FROM categories WHERE name = 'Data Representation')),
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Floating-point Numbers, Representation and Manipulation', (SELECT id FROM categories WHERE name = 'Data Representation'))
ON CONFLICT DO NOTHING;

-- Insert topics for Communication and Internet Technologies
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Protocols', (SELECT id FROM categories WHERE name = 'Communication and Internet Technologies')),
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Circuit Switching and Packet Switching', (SELECT id FROM categories WHERE name = 'Communication and Internet Technologies'))
ON CONFLICT DO NOTHING;

-- Insert topics for Hardware and Virtual Machines
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Processors, Parallel Processing, and Virtual Machines', (SELECT id FROM categories WHERE name = 'Hardware and Virtual Machines')),
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Boolean Algebra and Logic Circuits', (SELECT id FROM categories WHERE name = 'Hardware and Virtual Machines'))
ON CONFLICT DO NOTHING;

-- Insert topics for System Software
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Purposes of an Operating System (OS)', (SELECT id FROM categories WHERE name = 'System Software')),
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Translation Software', (SELECT id FROM categories WHERE name = 'System Software'))
ON CONFLICT DO NOTHING;

-- Insert topics for Security
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Encryption, Encryption Protocols, and Digital Certificates', (SELECT id FROM categories WHERE name = 'Security'))
ON CONFLICT DO NOTHING;

-- Insert topics for Artificial Intelligence (AI)
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Artificial Intelligence', (SELECT id FROM categories WHERE name = 'Artificial Intelligence (AI)'))
ON CONFLICT DO NOTHING;

-- Insert topics for Computational Thinking and Problem-solving
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Algorithms', (SELECT id FROM categories WHERE name = 'Computational Thinking and Problem-solving')),
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Recursion', (SELECT id FROM categories WHERE name = 'Computational Thinking and Problem-solving'))
ON CONFLICT DO NOTHING;

-- Insert topics for Further Programming
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'Programming Paradigms', (SELECT id FROM categories WHERE name = 'Further Programming')),
((SELECT id FROM courses WHERE course_code = '9618-A2' AND name = 'Computer Science'), 'File Processing and Exception Handling', (SELECT id FROM categories WHERE name = 'Further Programming'))
ON CONFLICT DO NOTHING;