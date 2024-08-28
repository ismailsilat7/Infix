import sqlite3
import os

# Connect to the database
conn = sqlite3.connect('data/infix.db')
cursor = conn.cursor()

# Fetch course data and corresponding topics
cursor.execute("""
    SELECT c.name AS course_name, c.course_code, c.path_id, t.title AS topic_name 
    FROM courses c 
    LEFT JOIN topics t ON c.id = t.course_id 
    ORDER BY CASE WHEN c.path_id = 2 THEN 0 ELSE 1 END, c.name ASC, t.seq_num ASC
""")
data = cursor.fetchall()

# Define base directory
base_dir = 'templates'

# Track existing directories to avoid redundant creation
existing_dirs = set()

# Function to replace special characters with ASCII equivalents
def replace_special_characters(text):
    replacements = {
        "‘": "'", "’": "'", "“": '"', "”": '"', "—": "-", "–": "-", "…": "...",
        "é": "e", "è": "e", "ê": "e", "ë": "e", "á": "a", "à": "a", "â": "a",
        "ä": "a", "í": "i", "ì": "i", "î": "i", "ï": "i", "ó": "o", "ò": "o",
        "ô": "o", "ö": "o", "ú": "u", "ù": "u", "û": "u", "ü": "u", "ç": "c",
        "ñ": "n", "ß": "ss", "ÿ": "y"
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

# Process each course and its topics
for course_name, course_code, path_id, topic_name in data:
    # Define path based on path_id
    path = 'A Levels' if path_id == 2 else 'O Levels'
    
    # Create folder name using course name and course code
    folder_name = f"{course_name} {course_code}"
    folder_path = os.path.join(base_dir, path, folder_name)
    
    # Check if directory already exists
    if folder_path not in existing_dirs:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created directory: {folder_path}")
        existing_dirs.add(folder_path)
    
    if topic_name:
        # Generate HTML file name based on the topic name
        file_name = f"{replace_special_characters(topic_name)}.html".replace(" ", "_").lower()
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file already exists to avoid overwriting
        if not os.path.exists(file_path):
            # Define the content of the topic HTML file using the template
            topic_content = f"""
            {{% extends 'topic_base.html' %}}

            {{% block topic_detail %}}
                <div id="title">
                    <h2>{replace_special_characters(topic_name)}<p>{course_code}</p></h2> 
                    <a href="/bookmark" class="bookmark-icon"><i class="ri-bookmark-fill"></i></a>
                </div>

                <div id="learning-outcomes" class="toc-item">
                    <h2>Learning Outcomes</h2>
                    <ul>
                        <li>Outcome 1: Describe key concepts of {replace_special_characters(topic_name)}.</li>
                        <li>Outcome 2: Understand and apply principles of {replace_special_characters(topic_name)} in practice.</li>
                        <li>Outcome 3: Analyze real-world examples related to {replace_special_characters(topic_name)}.</li>
                    </ul>
                </div>

                <div class="subtopic toc-item" id="subtopic-1">
                    <h3>Subtopic 1: Subtopic 1 Title</h3>
                    <p>
                        Explanation of Subtopic 1. This is where contributors will write about specific parts of the topic in detail. They can include examples, equations, and 
                        other relevant information to explain the subtopic clearly.
                    </p>
                </div>

                <div class="subtopic toc-item" id="subtopic-2">
                    <h3>Subtopic 2: Subtopic 2 Title</h3>
                    <p>
                        Explanation of Subtopic 2. Contributors should break down complex ideas into simple explanations, ensuring clarity and comprehension for students.
                    </p>
                </div>

                <div class="subtopic toc-item" id="subtopic-3">
                    <h3>Subtopic 3: Subtopic 3 Title</h3>
                    <p>
                        Explanation of Subtopic 3. Depending on the depth of the topic, there could be multiple subtopics, so contributors can add as many as necessary.
                    </p>
                </div>
            {{% endblock %}}
            """
            
            # Write the content to the HTML file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(topic_content.strip())
                print(f"Created file: {file_path}")
        else:
            print(f"File already exists: {file_path}")

# Close the connection
conn.close()
