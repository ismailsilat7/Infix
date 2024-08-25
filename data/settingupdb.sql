-- YOU SHOULD RUN THIS FILE WHEN YOU ARE CREATING A NEW DB
-- YOU MUST RUN THIS FILE AFTER YOU HAVE ALREADY CREATED RELEVANT TABLES FROM schema.sql
-- TOPICS INSERTED IN FILE inserttopics.sql

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

-- Insert categories
INSERT INTO categories (name) VALUES 
('Pure Mathematics 3'), 
('Probability and Statistics 2'), 
('Mechanics'),
('Physical Chemistry'),
('Inorganic Chemistry'),
('Organic Chemistry'),
('Analysis'),
('Data Representation'),
('Communication and Internet Technologies'),
('Hardware and Virtual Machines'),
('System Software'),
('Security'),
('Artificial Intelligence (AI)'),
('Computational Thinking and Problem-solving'),
('Further Programming')
ON CONFLICT DO NOTHING;

-- TOPICS INSERTED IN FILE inserttopics.sql

-- Inserting Data into study_guides
INSERT INTO study_guides (title, author) VALUES 
('Mastering Calculus for A Levels', 'John Doe'),
('Physics Made Easy', 'Jane Smith'),
('Comprehensive Chemistry Guide', 'Dr. Albert Einstein'),
('A* in Computer Science', 'Isaac Newton'),
('Exam Techniques for A Levels', 'Marie Curie')
ON CONFLICT DO NOTHING;

-- Inserting Data into labels
INSERT INTO labels (name) VALUES 
('Mathematics'),
('Physics'),
('Chemistry'),
('Computer Science'),
('Exam Preparation')
ON CONFLICT DO NOTHING;

-- Inserting into study_guides_laveks
INSERT INTO study_guides_labels (study_guide_id, label_id) VALUES 
(1, 1), -- Mastering Calculus for A Levels -> Mathematics
(2, 2), -- Physics Made Easy -> Physics
(3, 3), -- Comprehensive Chemistry Guide -> Chemistry
(4, 4), -- A* in Computer Science -> Computer Science
(5, 5) -- Exam Techniques for A Levels -> Exam Preparation
ON CONFLICT DO NOTHING;


