-- users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    nickname TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

INSERT INTO users (fullname,nickname,email, hash)
VALUES
('Mr Khan', 'admin123', 'khan@gmail.com', 'dkjsdkasjdkajsdksjahdkjas'), ('Ali Kashif', 'ali.kashif', 'alikashif5917@gmail.com', 'hdbasdbsajhbdasbdjashbdhjsadjhas'), ('Ismail Silat', 'ismail.silat', 'ismailsilat7@gmail.com', 'hdbasdbsajhbdasbdjashbdhjsadjhas')
ON CONFLICT DO NOTHING;

-- paths table
CREATE TABLE IF NOT EXISTS paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

INSERT INTO paths (name)
VALUES
('O Levels'), ('A Levels')
ON CONFLICT(name) DO NOTHING;

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

-- path_id for O Levels is 1, A Levels is 2
INSERT INTO courses (path_id, name, course_code)
VALUES
(2,'Chemistry', '9701-AS'),(2,'Chemistry', '9701-A2'),(2,'Computer Science', '9618-AS'),(2,'Computer Science', '9618-A2'),(2,'Mathematics', '9709-AS'),(2,'Mathematics', '9709-A2'),(2,'Physics', '9702-AS'),(2,'Physics', '9702-A2'),(1,'Biology','5090'),(1,'Chemistry','5070'),(1,'Computer Science','2210'),(1,'English Language','1123'),(1,'Islamiyat','2058'),(1,'Mathematics (Syllabus D)','4024'),(1,'Pakistan Studies','2059'),(1,'Physics','5054'),(1,'Urdu','3248')
ON CONFLICT DO NOTHING;

-- user_courses table
CREATE TABLE IF NOT EXISTS user_courses (
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

INSERT INTO user_courses (user_id, course_id)
VALUES
(2,4),(2,2),(2,6),(2,8),(1,4),(1,2),(1,6),(1,8)
ON CONFLICT DO NOTHING;

-- topics table
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
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

-- progress table
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);