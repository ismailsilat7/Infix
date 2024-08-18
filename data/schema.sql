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
    category_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- user_topics table
CREATE TABLE IF NOT EXISTS user_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- bookmarks table
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
