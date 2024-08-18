-- YOU SHOULD RUN THIS FILE WHEN YOU ARE CREATING A NEW DB
-- YOU MUST RUN THIS FILE AFTER YOU HAVE ALREADY CREATED RELEVANT TABLES FROM schema.sql


-- CREATING 3 USERS - DON'T FORGET TO RESET HASH VIA FORGET PASSWORD FEATURE
INSERT INTO users (fullname,username,email, hash)
VALUES
('Mr Khan', 'admin123', 'khan@gmail.com', 'dkjsdkasjdkajsdksjahdkjas'), ('Ali Kashif', 'ali.kashif', 'alikashif5917@gmail.com', 'hdbasdbsajhbdasbdjashbdhjsadjhas'), ('Ismail Silat', 'ismail.silat', 'ismailsilat7@gmail.com', 'hdbasdbsajhbdasbdjashbdhjsadjhas')
ON CONFLICT DO NOTHING;

-- INSERTING PATHS INTO paths TABLE - paths : 'O Levels' & 'A Levels' as of yet
INSERT INTO paths (name)
VALUES
('O Levels'), ('A Levels')
ON CONFLICT(name) DO NOTHING;

-- ASSIGNING EACH USER A PATH - path_id 1 is for 'O Levels' & path_id 2 is for 'A Levels' 
-- users with id 1,2 & 3 are in A Levels, user with id 4 is in O Levels
INSERT INTO user_paths (user_id, path_id)
VALUES
(1,2),(2,2),(3,2),(4,1) 
ON CONFLICT DO NOTHING;

-- INSERTING COURSES IN TABLE courses IN ASC ORDER WITH RESPECT TO COURSE NAME, A LEVEL COURSES ARE ADDED FIRST WHILE O LEVEL COURSES SECOND
INSERT INTO courses (path_id, name, course_code)
VALUES
(2,'Chemistry', '9701-AS'),(2,'Chemistry', '9701-A2'),(2,'Computer Science', '9618-AS'),(2,'Computer Science', '9618-A2'),(2,'Mathematics', '9709-AS'),(2,'Mathematics', '9709-A2'),(2,'Physics', '9702-AS'),(2,'Physics', '9702-A2'),(1,'Biology','5090'),(1,'Chemistry','5070'),(1,'Computer Science','2210'),(1,'English Language','1123'),(1,'Islamiyat','2058'),(1,'Mathematics (Syllabus D)','4024'),(1,'Pakistan Studies','2059'),(1,'Physics','5054'),(1,'Urdu','3248')
ON CONFLICT DO NOTHING;

-- ENROLLING users WITH ID 1 & 2 (A Levels) IN A2 SCIENCE COURSES - users WITH ID 3 (A Levels) & 4 (O Levels) ARE CURRENTLY NOT IN ANY COURSE
INSERT INTO user_courses (user_id, course_id)
VALUES
(2,4),(2,2),(2,6),(2,8),(1,4),(1,2),(1,6),(1,8)
ON CONFLICT DO NOTHING;

-- INSERTING TOPICS IN TABLE topics IN OFFICIAL SYLLABUS ORDER
-- Insert categories
INSERT INTO categories (name) VALUES 
('Pure Mathematics 3'), 
('Probability and Statistics 2'), 
('Mechanics');

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
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Complex Numbers', (SELECT id FROM categories WHERE name = 'Pure Mathematics 3'));

-- Insert topics for Mechanics
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Forces and Equilibrium', (SELECT id FROM categories WHERE name = 'Mechanics')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Kinematics of Motion in a Straight Line', (SELECT id FROM categories WHERE name = 'Mechanics')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Momentum', (SELECT id FROM categories WHERE name = 'Mechanics')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Newton’s Laws of Motion', (SELECT id FROM categories WHERE name = 'Mechanics')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Energy, Work and Power', (SELECT id FROM categories WHERE name = 'Mechanics'));

-- Insert topics for Probability & Statistics 2
INSERT INTO topics (course_id, title, category_id)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'The Poisson Distribution', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Linear Combinations of Random Variables', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Continuous Random Variables', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Sampling and Estimation', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2')),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Hypothesis Tests', (SELECT id FROM categories WHERE name = 'Probability and Statistics 2'));