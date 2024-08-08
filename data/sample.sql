-- users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    nickname TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

-- paths table
CREATE TABLE IF NOT EXISTS paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- user_paths table
CREATE TABLE IF NOT EXISTS user_paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    path_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (path_id) REFERENCES paths(id)
);

-- course table
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    course_code INTEGER NOT NULL,
    FOREIGN KEY (path_id) REFERENCES paths(id)
);

-- topics table
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- bookmarks table
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (topic_id) REFERENCES topics(id)
);

-- progress table
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (topic_id) REFERENCES topics(id)
);

-- Mark topics as completed
INSERT INTO progress (user_id, topic_id, completed, completed_at)
VALUES 
    (1, 101, TRUE, CURRENT_TIMESTAMP),
    (1, 102, TRUE, CURRENT_TIMESTAMP),
    (1, 103, TRUE, CURRENT_TIMESTAMP)
ON CONFLICT(user_id, topic_id) DO UPDATE SET
    completed = TRUE,
    completed_at = CURRENT_TIMESTAMP;

-- Calculate progress percentage directly
SELECT 
    COUNT(CASE WHEN completed = TRUE THEN 1 END) AS completed_topics,
    COUNT(*) AS total_topics,
    (COUNT(CASE WHEN completed = TRUE THEN 1 END) * 100.0 / COUNT(*)) AS progress_percentage
FROM progress
WHERE user_id = 1;
