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
INSERT INTO topics (course_id, title)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Algebra'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Logarithmic and Exponential Functions'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Trigonometry'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Differentiation'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Integration'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Numerical Solution of Equations'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Vectors'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Differential Equations'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Complex Numbers');

-- Mechanics
INSERT INTO topics (course_id, title)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Forces and Equilibrium'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Kinematics of Motion in a Straight Line'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Momentum'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Newton’s Laws of Motion'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Energy, Work and Power');

-- Probability & Statistics 2
INSERT INTO topics (course_id, title)
VALUES 
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'The Poisson Distribution'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Linear Combinations of Random Variables'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Continuous Random Variables'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Sampling and Estimation'),
((SELECT id FROM courses WHERE course_code = '9709-A2' AND name = 'Mathematics'), 'Hypothesis Tests');