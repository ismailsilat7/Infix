-- THIS IS SCHEMA, USED TO CREATE TABLES
-- TO RUN, TYPE .read schema.sql IN THE SQLite3 TERMINAL
-- THEN RUN settingupdb.sql TO CREATE TEST USERS (.read settingupdb.sql)

-- users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    google_id TEXT
);

-- paths table
CREATE TABLE IF NOT EXISTS paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- user_paths table
CREATE TABLE IF NOT EXISTS user_paths (
    user_id INTEGER NOT NULL UNIQUE,
    path_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, path_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (path_id) REFERENCES paths(id) ON DELETE CASCADE
);

-- course table
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    course_code INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (path_id) REFERENCES paths(id) ON DELETE CASCADE
);

-- user_courses table
CREATE TABLE IF NOT EXISTS user_courses (
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- topics table
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);
-- Add a category column to the topics table
ALTER TABLE topics ADD COLUMN category TEXT;

-- bookmarks table
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

-- progress table
CREATE TABLE IF NOT EXISTS user_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

-- otps table
CREATE TABLE IF NOT EXISTS otps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    otp_hash TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Pure Mathematics 3
INSERT INTO topics (course_id, title, category)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Algebra', 'Pure Mathematics 3'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Logarithmic and Exponential Functions', 'Pure Mathematics 3'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Trigonometry', 'Pure Mathematics 3'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Differentiation', 'Pure Mathematics 3'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Integration', 'Pure Mathematics 3'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Numerical Solution of Equations', 'Pure Mathematics 3'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Vectors', 'Pure Mathematics 3'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Differential Equations', 'Pure Mathematics 3'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Complex Numbers', 'Pure Mathematics 3');

-- Mechanics
INSERT INTO topics (course_id, title, category)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Forces and Equilibrium', 'Mechanics'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Kinematics of Motion in a Straight Line', 'Mechanics'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Momentum', 'Mechanics'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Newton’s Laws of Motion', 'Mechanics'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Energy, Work and Power', 'Mechanics');

-- Probability & Statistics 2
INSERT INTO topics (course_id, title)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'The Poisson Distribution', 'Probability & Statistics 2'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Linear Combinations of Random Variables', 'Probability & Statistics 2'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Continuous Random Variables', 'Probability & Statistics 2'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Sampling and Estimation', 'Probability & Statistics 2'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Hypothesis Tests', 'Probability & Statistics 2');