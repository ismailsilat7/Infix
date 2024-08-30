import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import re
from oauthlib.oauth2 import WebApplicationClient
import requests
from dotenv import load_dotenv
import json
from flask import Flask
from flask_mail import Mail, Message
import random
import string
from datetime import datetime, timedelta, timezone

# JUST FOR LOCAL
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
load_dotenv()

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure app with Google OAuth credentials
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID")
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET")
app.config['GOOGLE_DISCOVERY_URL'] = "https://accounts.google.com/.well-known/openid-configuration"

# Initialize OAuth client
client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

# Configure app with smtp
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# Initialize database connection
db = SQL("sqlite:///data/infix.db")
db.execute('PRAGMA foreign_keys = ON')
from functools import wraps
def non_google_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        google_id = db.execute(""" 
            SELECT google_id FROM users
            WHERE id = ?
        """, user_id)
        
        # Ensure google_id is being checked correctly
        if google_id and google_id[0]["google_id"] is not None:
            return redirect("/invalid")
        
        return f(*args, **kwargs)
    return decorated_function


# Ensures responses aren't cached to keep info for users up to date
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response

# Other routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form.get("email"):
            flash("Please enter email!","warning")
        if not request.form.get("pwd"):
            flash("Please enter password","warning")
        email = request.form.get("email")
        rows = db.execute (
            "SELECT * from users WHERE email = ?", email
        )
        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("pwd")):
            flash("Invalid email and/or password", "warning")
        else:
            # remember user and redirect to index page
            session["user_id"] = rows[0]["id"]
            # flash("Log In Successfull", "success")
            return redirect('/dashboard')

    return render_template('log-in.html')

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    """Register user"""
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if request.method == "POST":
        # Validate form input
        if not request.form.get("name"):
            flash("Must enter name", "warning")
        elif not request.form.get("username"):
            flash("Must enter username", "warning")
        elif len(request.form.get("username")) < 3:
            flash("Username must include at least 3 characters", "warning")
        elif len(request.form.get("name")) < 5:
            flash("Name must include at least 5 characters", "warning")
        elif not request.form.get("email"):
            flash("Must enter email", "warning")
        elif not re.match(email_regex, request.form.get("email")):
            flash("Invalid email format", category="warning")
        elif not request.form.get("path") and request.form.get('path') not in ['O Levels','A Levels']:
            flash("Must select valid path!", "warning")
        elif not request.form.get("pwd"):
            flash("Must enter password", "warning")
        elif not request.form.get("confirm-pwd"):
            flash("Please confirm password", "warning")
        elif len(request.form.get("pwd")) < 8:
            flash("Password must include at least 8 characters", "warning")
        elif request.form.get("confirm-pwd") != request.form.get("pwd"):
            flash("Passwords don't match", "warning")
        else:
            unique = True
            fullname = request.form.get("name")
            
            # Ensure username doesn't already exist
            username = request.form.get("username")
            if db.execute("SELECT username FROM users WHERE username = ?", username):
                unique = False
                flash("Whoa, someone already has that username, please choose a different one", "warning")
            else:
                # Ensure email doesn't already exist
                email = request.form.get("email")
                path = request.form.get("path")
                if db.execute("SELECT email FROM users WHERE email = ?", email):
                    unique = False
                    flash("This email is already registered", "warning")
                else:
                    # Generate hash for password
                    hash = generate_password_hash(request.form.get("pwd"))
                    
                    if unique:
                        # Store user in database
                        db.execute(
                            "INSERT INTO users (fullname, username, email, hash) VALUES (?,?,?,?)",
                            fullname, username, email, hash
                        )
                        # Add user's path
                        user_rows = db.execute(
                            "SELECT id FROM users WHERE email = ?", email
                        )
                        path_rows = db.execute(
                            "SELECT id FROM paths WHERE name = ?", path
                        )
                        db.execute (
                            "INSERT INTO user_paths (user_id, path_id) VALUES (?,?)", user_rows[0]["id"], path_rows[0]["id"]
                        )
                        flash("Your account has been successfully registered, Please log in", "success")
    
    # If the method is GET or if validation fails, render the sign-up page
    return render_template("sign-up.html")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def change_password():
    user_id = session.get('user_id')
    
    result = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
    
    # Redirect user to set new password if they have no password set
    if "GOOGLE_OAUTH" == result[0]['hash']:
        return redirect('/setnewpassword')

    if request.method == 'POST':
        # Validate form inputs
        if not request.form.get("email"):
            flash("Must enter email", "warning")
            return render_template("change-password.html")
        elif not request.form.get("prev-password"):
            flash("Must enter previous password", "warning")
            return render_template("change-password.html")
        elif not request.form.get("new-pwd"):
            flash("Must enter password", "warning")
            return render_template("change-password.html")
        elif not request.form.get("confirm-new-pwd"):
            flash("Please confirm password", "warning")
            return render_template("change-password.html")
        elif len(request.form.get("new-pwd")) < 8:
            flash("Password must include at least 8 characters", "warning")
            return render_template("change-password.html")
        elif request.form.get("confirm-new-pwd") != request.form.get("new-pwd"):
            flash("Passwords don't match", "warning")
            return render_template("change-password.html")

        # Check previous password
        email = request.form.get("email")
        prev_password = request.form.get("prev-password")
        rows = db.execute("SELECT hash FROM users WHERE email = ?", email)

        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], prev_password):
            flash("Invalid email and/or password", "warning")
            return render_template("change-password.html")

        # Check if the email belongs to the logged-in user
        user_email = db.execute("SELECT email FROM users WHERE id = ?", user_id)[0]['email']
        if user_email != email:
            flash("Please enter your own email/username", "warning")
            return render_template("change-password.html")

        # Check if new password is same as old password
        newpwd = request.form.get("new-pwd")
        if check_password_hash(rows[0]["hash"], newpwd):
            flash("New password cannot be same as old password", "warning")
            return render_template("change-password.html")

        # Update password
        hash = generate_password_hash(newpwd)
        db.execute("UPDATE users SET hash = ? WHERE email = ?", hash, email)

        # Clear session and redirect to login
        session.clear()
        flash("Password Updated, Please Login", "success")
        return redirect('/login')

    return render_template("change-password.html")


@app.route("/logout")
@login_required
def log_out():
    session.clear()
    return redirect("/")

@app.route("/selectpath", methods = ['POST', 'GET'])
def select_path():
    if not session.get('user_id'):
        return render_template('sign-up.html')
    return redirect('/dashboard')

@app.route('/dashboard')
@login_required 
def dashboard():
    user_id = session['user_id']
    result = db.execute("""
        SELECT hash FROM users
        WHERE id = ?
    """, user_id)
    if "GOOGLE_OAUTH" == result[0]['hash']:
        no_password = True
    else:
        no_password = False
    # Get user's name
    user_info = db.execute("SELECT fullname FROM users WHERE id = ?", user_id)
    fullname = user_info[0]['fullname'] if user_info else None
    first_name = fullname.split()[0] if fullname else None

    # Get the user's selected path id
    user_path_id = db.execute("SELECT path_id FROM user_paths WHERE user_id = ?", user_id)
    path_id = user_path_id[0]['path_id'] if user_path_id else None

    # Get path name based on path_id
    user_path_name = db.execute("SELECT name FROM paths WHERE id = ?", path_id)
    path_name = user_path_name[0]['name'] if user_path_name else 'A Levels'

    # Get the user's enrolled courses
    enrolled_courses = db.execute("""
        SELECT courses.name, courses.course_code
        FROM courses
        JOIN user_courses ON courses.id = user_courses.course_id
        JOIN user_paths ON user_paths.user_id = user_courses.user_id
        WHERE user_courses.user_id = ?
        AND courses.path_id = user_paths.path_id
    """, user_id)  


    # Get the user's bookmarks along with topic and course names
    bookmarks = db.execute("""
        SELECT t.title, t.id AS topic_id, c.name AS course_name
        FROM bookmarks b
        JOIN topics t ON b.topic_id = t.id
        JOIN courses c ON t.course_id = c.id
        WHERE b.user_id = ?
    """, user_id)

    return render_template('dashboard.html', path_name = path_name, enrolled_courses = enrolled_courses, first_name = first_name, bookmarks = bookmarks, no_password = no_password)


@app.route('/courses')
@login_required
def courses():
    user_id = session['user_id']
    # Get the user's path
    result = db.execute("""
        SELECT paths.name AS user_path
        FROM paths
        JOIN user_paths ON paths.id = user_paths.path_id
        WHERE user_paths.user_id = ?
    """, user_id)
    if result:
        path = result[0]["user_path"]
    else:
        flash("Please select a path to view courses")
        return redirect("/selectpath")
    user_path_id = db.execute("SELECT path_id FROM user_paths WHERE user_id = ?", user_id)[0]["path_id"]
    # Get the user's enrolled courses
    enrolled_courses = db.execute("""
        SELECT courses.name, courses.course_code
        FROM courses
        JOIN user_courses ON courses.id = user_courses.course_id
        JOIN user_paths ON user_paths.user_id = user_courses.user_id
        WHERE user_courses.user_id = ?
        AND courses.path_id = user_paths.path_id
    """, user_id)

    #boolean to check if there are any enrolled courses
    enrolled = len(enrolled_courses) > 0

    other_courses = db.execute("""
        SELECT courses.name, courses.course_code
        FROM courses
        WHERE courses.id NOT IN (
            SELECT user_courses.course_id
            FROM user_courses
            WHERE user_courses.user_id = ?
        ) AND courses.path_id = ?
    """, user_id, user_path_id)
    # boolean to check if there are any courses to add
    to_add = len(other_courses) > 0

    user_name = db.execute("SELECT fullname FROM users WHERE id = ?", user_id)[0]['fullname']
    user_email = db.execute("SELECT email FROM users WHERE id = ?", user_id)[0]['email']

    return render_template('courses.html', enrolled_courses=enrolled_courses, other_courses=other_courses, path=path, enrolled = enrolled, to_add = to_add, user_name=user_name, user_email=user_email)

@app.route('/course-recommendation', methods=["POST", "GET"])
@login_required
def get_course_recommendation():
    if request.method == "POST":
        name = request.form.get('name')
        path = request.form.get('path')
        email = request.form.get('email')
        course_name = request.form.get('course_name')
        if not name or not path or not email or not course_name:
            flash("Incomplete response, please try again", "warning")
            return redirect('/courses')
        
        result = db.execute("""
            SELECT id FROM users
            WHERE fullname = ? AND email = ?
        """, name, email)
        if not result:
            flash("Invalid response, please try again", "warning")
            return redirect('/courses')
        user_id = result[0]['id']
        result = db.execute("""
            SELECT id FROM paths
            WHERE name = ?
        """, path)
        if not result:
            flash("Invalid response, please try again", "warning")
            return redirect('/courses')
        name = name.split(' ')[0]
        subject = "Course Suggestion Received"
        message_body = f"Dear {name},\n\nThank you for sharing your course suggestion! We’ve received your input for the course '{course_name}' for {path} path, and it’s awesome to see you contributing to making Infix better.\n\nKeep up the hard work with your studies, and feel free to send us more ideas anytime!\n\nBest Regards,"
        # Send the appropriate email
        msg = Message(subject, recipients=[email, "connect.infix@gmail.com"])
        msg.body = message_body + f"\n\n--\nInfix Team\nExcel Beyond\n🌐 www.infix.com\n📞+92-333-2498905, + 92-334-2087247\n"
        mail.send(msg)

        flash("Suggestion received", "success")
        return redirect('/courses')
    return redirect('/courses')
        

@app.route('/course/<course_code>')
@login_required
def course_detail(course_code):
    
    # Get the course details using the course name
    course = db.execute("SELECT * FROM courses WHERE course_code = ?", course_code)
    if not course:
        flash('Course not found.', 'warning')
        return redirect('/dashboard')

    course_id = course[0]['id']
    topics = db.execute("SELECT * FROM topics WHERE course_id = ?", course_id)

    # Fetch topics and their category names using a JOIN
    topics_with_categories = db.execute("""
        SELECT topics.id, topics.title, categories.name AS category, categories.id AS category_id
        FROM topics
        LEFT JOIN categories ON topics.category_id = categories.id
        WHERE topics.course_id = ?
    """, course_id)

    return render_template('course_detail.html', course=course[0], topics=topics_with_categories)

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

@app.route('/course/<course_code>/<topic>')
@login_required
def topic_detail(course_code, topic):
    # Fetch course details
    course = db.execute("SELECT * FROM courses WHERE course_code = ?", course_code)
    
    if not course:
        flash("Course not found.", "warning")
        return redirect('/dashboard')
    
    course = course[0]  # Get the first result
    
    # Fetch topic details
    topic_details = db.execute("""
        SELECT t.title, c.name as course_name, c.course_code, t.id as topic_id, t.category_id, t.seq_num, c.id as course_id
        FROM topics t
        JOIN courses c ON t.course_id = c.id
        WHERE t.title = ? AND c.course_code = ?
    """, topic, course_code)
    
    if not topic_details:
        flash("Topic not found.", "error")
        return redirect(url_for('index'))  # Redirect to a suitable page if the topic is not found
    
    topic_details = topic_details[0]  # Get the first result
    print(topic_details)
    
    # Fetch the next topic based on the sequence number - currently doing based on topic num
    next_topic = db.execute("""
        SELECT title FROM topics
        WHERE course_id = ? AND seq_num > ?
        ORDER BY seq_num ASC
        LIMIT 1
    """, topic_details['course_id'], topic_details['seq_num'])

    next_topic = next_topic[0]['title'] if next_topic else None
    
    # Fetch categories and their respective topics
    categories = db.execute("""
        SELECT * FROM categories
        WHERE id IN (
                        SELECT DISTINCT t.category_id FROM topics t
                        JOIN courses c ON t.course_id = c.id
                        WHERE c.course_code = ?
                    )
    """, course_code)
    topics_data = {}
    if categories:
        current_category = db.execute("""
            SELECT name FROM categories WHERE id = ?
        """, topic_details['category_id'])[0]['name']
        for category in categories:
            category_name = category['name']
            topics_in_category = db.execute("""
                SELECT title FROM topics
                WHERE category_id = ?
            """, category['id'])
            
            if topics_in_category:
                topics_data[category_name] = topics_in_category
            else:
                print(f"No topics found for category: {category_name}")
    else:
        print("No categories found, defaulting to 'Topics'")
        current_category = "Topics"
        course_id = db.execute("""
            SELECT id FROM courses
            WHERE course_code = ?
        """, topic_details['course_code'])[0]['id']

        topics_in_category = db.execute("""
            SELECT title FROM topics WHERE course_id = ?
        """, course_id)
        
        if topics_in_category:
            topics_data[current_category] = topics_in_category
        else:
            print(f"No topics found for course: {course_code}")
    
    # Extract necessary details
    topic_name = topic_details['title']
    course_name = topic_details['course_name']
    topic_id = topic_details['topic_id']
    
    result = db.execute("""
        SELECT * FROM bookmarks
        WHERE user_id = ? AND topic_id = ?
    """, session['user_id'], topic_id)

    bookmarked = bool(result)

    result = db.execute("""
        SELECT * FROM user_topics
        WHERE user_id = ? AND topic_id = ?
    """, session['user_id'], topic_id)
    
    completed = bool(result)

    # Determine the path (O Levels or A Levels)
    path = "A Levels" if 'A' in course_code else "O Levels"
    
    # Format topic for file path with special character replacement
    formatted_topic = replace_special_characters(topic.lower().replace(' ', '_'))
    
    # Generate the file path
    template_path = f"{path}/{course_name} {course_code}/{formatted_topic}.html"
    
    # Render the template with the appropriate context
    return render_template(
        template_path, 
        topic_name=topic_name, 
        course_name=course_name,
        course_code=course_code, 
        topic_id=topic_id, 
        topics_data=topics_data,  # Structured topics and categories
        current_topic=topic_name,  # Current topic
        current_category=current_category,  # Current category
        formatted_topic=formatted_topic,
        bookmarked=bookmarked,
        completed=completed,
        next_topic=next_topic  # Add the next topic to the context
    )



def isenrolled(course_code, user_id):
    """Checks if the user is enrolled in the course."""
    try:
        # Get course ID based on the course code
        result = db.execute("SELECT id FROM courses WHERE course_code = ?", course_code)
        if result:
            course_id = result[0]['id']
            # Check if the user is enrolled in the course
            enrollment = db.execute("SELECT * FROM user_courses WHERE course_id = ? AND user_id = ?", course_id, user_id)
            return bool(enrollment)  # Return True if the enrollment exists
    except Exception as e:
        print(f"Error in isenrolled: {e}")
    return False

def determine_path(course_code):
    """Determines the path (O Levels or A Levels) based on the course code."""
    return "A Levels" if 'A' in course_code else "O Levels"

@app.route('/add-bookmark', methods=['POST'])
@login_required
def addBookmark():
    course_code = request.form.get('course_code')
    topic_id = request.form.get('topic_id')
    topic_name = request.form.get('topic_name')
    user_id = session.get('user_id')

    if not course_code or not topic_id or not topic_name:
        flash("Error encountered, please try again", "warning")
        return redirect(request.referrer)

    redirect_route = f"/course/{course_code}/{topic_name}"
    
    if isenrolled(course_code, user_id):
        try:
            result = db.execute("SELECT id FROM bookmarks WHERE topic_id = ? AND user_id = ?", topic_id, user_id)
            if result:
                flash(f"{topic_name} is already bookmarked.", "warning")
            else:
                db.execute("INSERT INTO bookmarks (topic_id, user_id) VALUES (?, ?)", topic_id, user_id)
                flash(f"{topic_name} bookmarked!", "success")
        except Exception as e:
            flash(f"Error encountered, please try again. {str(e)}", "warning")
    else:
        flash(f"Please enroll in {course_code} first.", "warning")
    return redirect(redirect_route)

@app.route('/remove-bookmark', methods=['POST'])
@login_required
def removeBookmark():
    course_code = request.form.get('course_code')
    topic_id = request.form.get('topic_id')
    topic_name = request.form.get('topic_name')
    user_id = session.get('user_id')

    if not course_code or not topic_id or not topic_name:
        flash("Error encountered, please try again", "warning")
        return redirect(request.referrer)

    redirect_route = f"/course/{course_code}/{topic_name}"
    
    if isenrolled(course_code, user_id):
        try:
            result = db.execute("SELECT id FROM bookmarks WHERE topic_id = ? AND user_id = ?", topic_id, user_id)
            if not result:
                flash(f"{topic_name} wasn't already bookmarked.", "warning")
            else:
                db.execute("DELETE FROM bookmarks WHERE id = ?", result[0]['id'])
                flash(f"Bookmark for {topic_name} removed!", "success")
        except Exception as e:
            flash(f"Error encountered, please try again. {str(e)}", "warning")
    else:
        flash(f"Please enroll in {course_code} first.", "warning")
    return redirect(redirect_route)

@app.route('/markascomplete', methods=['POST'])
@login_required
def markComplete():
    course_code = request.form.get('course_code')
    topic_id = request.form.get('topic_id')
    topic_name = request.form.get('topic_name')
    user_id = session.get('user_id')

    if not course_code or not topic_id or not topic_name:
        flash("Error encountered, please try again", "warning")
        return redirect(request.referrer)

    redirect_route = f"/course/{course_code}/{topic_name}"
    
    if isenrolled(course_code, user_id):
        try:
            result = db.execute("SELECT id FROM user_topics WHERE topic_id = ? AND user_id = ?", topic_id, user_id)
            if result:
                flash(f"{topic_name} already marked as complete.", "warning")
            else:
                db.execute("INSERT INTO user_topics (topic_id, user_id) VALUES (?, ?)", topic_id, user_id)
                flash(f"{topic_name} marked as complete.", "success")
        except Exception as e:
            flash(f"Error encountered, please try again. {str(e)}", "warning")
    else:
        flash(f"Please enroll in {course_code} first.", "warning")
    return redirect(redirect_route)

@app.route('/marknotcomplete', methods=['POST'])
@login_required
def markNotComplete():
    course_code = request.form.get('course_code')
    topic_id = request.form.get('topic_id')
    topic_name = request.form.get('topic_name')
    user_id = session.get('user_id')

    if not course_code or not topic_id or not topic_name:
        flash("Error encountered, please try again", "warning")
        return redirect(request.referrer)

    redirect_route = f"/course/{course_code}/{topic_name}"
    
    if isenrolled(course_code, user_id):
        try:
            result = db.execute("SELECT id FROM user_topics WHERE topic_id = ? AND user_id = ?", topic_id, user_id)
            if result:
                db.execute("DELETE FROM user_topics WHERE id = ?", result[0]['id'])
                flash(f"{topic_name} marked as not complete.", "success")
            else:
                flash(f"{topic_name} was not marked complete.", "warning")
        except Exception as e:
            flash(f"Error encountered, please try again. {str(e)}", "warning")
    else:
        flash(f"Please enroll in {course_code} first.", "warning")
    return redirect(redirect_route)


@app.route('/enrollcourse/<course_code>')
@login_required
def enroll_course(course_code):
    user_id = session['user_id']
    # Get the course details using the course name
    course = db.execute("SELECT * FROM courses WHERE course_code = ?", course_code)
    if not course:
        return "Course not found", 404

    course_id = course[0]['id']
    course_name = db.execute("""
        SELECT name FROM courses
        WHERE course_code = ?
    """, course_code)[0]['name']
    db.execute("""
        INSERT INTO user_courses (user_id, course_id)
        VALUES
        (?,?)
    """, user_id, course_id)
    flash(f"You have enrolled in {course_name + ' ' + course_code}", "success")
    return redirect('/courses')

@app.route('/dropcourse/<course_code>')
@login_required
def drop_course(course_code):
    user_id = session['user_id']
    # Get the course details using the course name
    course = db.execute("SELECT * FROM courses WHERE course_code = ?", course_code)
    if not course:
        return "Course not found", 404

    course_id = course[0]['id']
    course_name = db.execute("""
        SELECT name FROM courses
        WHERE course_code = ?
    """, course_code)[0]['name']
    db.execute("""
        DELETE FROM user_courses
        WHERE user_id = ? AND course_id = ?
    """, user_id, course_id)
    flash(f"You have dropped {course_name + ' ' + course_code}", "success")
    return redirect('/courses')


@app.route('/dropcourseconfirmation/<course_code>')
@login_required
def dropcourse_confirmation(course_code):
    course_name = db.execute("""
        SELECT name FROM courses
        WHERE course_code = ?
    """, course_code)[0]["name"]
    return render_template('dropcourse-confirmation.html', course_code=course_code, course_name=course_name)

@app.route("/changepath")
@login_required
def change_path():
    user_id = session['user_id']
    user_path_id = db.execute("""
        SELECT path_id FROM user_paths
        WHERE user_id = ?
    """, user_id)[0]["path_id"]
    current_path_name = db.execute("""
        SELECT name FROM paths 
        WHERE id = ?
    """, user_path_id)[0]["name"]
    other_path_name = db.execute("""
        SELECT name FROM paths
        WHERE NOT id = ?
    """, user_path_id)[0]["name"]
    return render_template('change-path.html', user_path_id = user_path_id, current_path_name = current_path_name, other_path_name = other_path_name)

@app.route('/changepath/<path_name>')
@login_required
def change_to_path(path_name):
    user_id = session['user_id']
    result = db.execute("""
        SELECT id FROM paths
        WHERE name = ?
    """, path_name)
    if not result:
        flash(f"Invalid path", "warning")
        return redirect('/dashboard')
    else:
        path_id = result[0]["id"]
    db.execute("""
        UPDATE user_paths
        SET path_id = ?
        WHERE user_id = ?
    """, path_id, user_id)
    flash(f"Changed path to {path_name}", "success")
    return redirect('/dashboard')

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    user_id = session["user_id"]
    result = db.execute("""
        SELECT google_id FROM users
        WHERE id = ?
    """, user_id)
    if None == result[0]['google_id']:
        with_google = False
    else:
        with_google = True
    result = db.execute("""
        SELECT hash FROM users
        WHERE id = ?
    """, user_id)
    if "GOOGLE_OAUTH" == result[0]['hash']:
        no_password = True
    else:
        no_password = False
    if request.method == "POST":
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        if not with_google:
            email = request.form.get("email")
        
        current_user = db.execute("SELECT fullname, username, email FROM users WHERE id = ?", user_id)[0]
        current_fullname = current_user['fullname']
        current_username = current_user['username']
        current_email = current_user['email']

        # Validate input
        if not fullname or len(fullname) < 5:
            flash("Fullname must include at least 5 characters", "warning")
        elif not username or len(username) < 3:
            flash("Username must include at least 3 characters", "warning")
        elif not with_google and (not email or not re.match(email_regex, email)):
            flash("Invalid email format", "warning")
        else:
            if (fullname == current_fullname and 
                username == current_username):
                if with_google:
                    flash("No changes made", "info")
                elif email == current_email:
                    flash("No changes made", "info")
            else:
                query = "SELECT * FROM users WHERE username = ? AND id != ?"
                params = [username, user_id]
                
                if not with_google:
                    query = "SELECT * FROM users WHERE (username = ? OR email = ?) AND id != ?"
                    params = [username, email, user_id]
                
                existing_user = db.execute(query, *params)
                if existing_user:
                    flash("Username and/or Email already exists", "warning")
                else:
                    update_query = "UPDATE users SET fullname = ?, username = ?"
                    update_params = [fullname, username, user_id]
                    if not with_google:
                        update_query += ", email = ?"
                        update_params.insert(2, email)  # Insert email before user_id
                    # Finalize the query and update the user information
                    db.execute(update_query + " WHERE id = ?", *update_params)
                    flash("Changes made!", "success")
    

    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
    return render_template("settings.html", user=user,  with_google = with_google, no_password = no_password)

@app.route("/delete-confirmation", methods=["GET", "POST"])
@login_required
def delete_account():
    action = "Delete"
    user_id = session["user_id"]
    user = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]
    user_name = user['username']
    google_id = db.execute(""" 
        SELECT google_id FROM users
        WHERE id = ?
    """, user_id)[0]['google_id']
    with_google = False
    if google_id == None:
        with_google = False
    elif len(google_id) > 0:
        with_google = True
    
    if request.method == "POST":
        if not with_google:
            email = request.form.get("email")
            password = request.form.get("pwd")
            
            if not email:
                flash("Please enter your email!", "warning")
                return render_template('delete_confirmation.html', user_name=user_name, action=action, verification_purpose="delete-confirmation", with_google = with_google)
            
            if not password:
                flash("Please enter your password!", "warning")
                return render_template('delete_confirmation.html', user_name=user_name, action=action, verification_purpose="delete-confirmation", with_google = with_google)
            
            user_email = db.execute("SELECT email FROM users WHERE id = ?", user_id)[0]['email']
            user_hash = db.execute("SELECT hash FROM users WHERE id = ?", user_id)[0]['hash']
            
            if not (user_email == email and check_password_hash(user_hash, password)):
                flash("Incorrect email or password", "warning")
                return render_template('delete_confirmation.html', user_name=user_name, action=action, verification_purpose="delete-confirmation", with_google = with_google)
        
        # Delete user account
        db.execute("DELETE FROM users WHERE id = ?", user_id)
        session.clear()
        
        flash("Your account has been deleted", "success")
        return redirect("/")
    
    return render_template("delete_confirmation.html", user_name=user_name, action=action, verification_purpose="delete-confirmation", with_google = with_google)


@app.route("/reset-confirmation", methods=["GET", "POST"])
@login_required
def reset_progress():
    action = "Reset"
    user_id = session["user_id"]
    user = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]
    user_name = user['username']
    google_id = db.execute(""" 
        SELECT google_id FROM users
        WHERE id = ?
    """, user_id)[0]["google_id"]
    with_google = False
    if google_id == None:
        with_google = False
    elif len(google_id) > 0:
        with_google = True
    
    if request.method == "POST":
        if not with_google:
            email = request.form.get("email")
            password = request.form.get("pwd")
            
            if not email:
                flash("Please enter email!", "warning")
                return render_template('reset_confirmation.html', user_name=user_name, action=action, verification_purpose="reset-confirmation", with_google = with_google)
            
            if not password:
                flash("Please enter password", "warning")
                return render_template('reset_confirmation.html', user_name=user_name, action=action, verification_purpose="reset-confirmation", with_google = with_google)
            
            user_email = db.execute("SELECT email FROM users WHERE id = ?", user_id)[0]['email']
            user_hash = db.execute("SELECT hash FROM users WHERE id = ?", user_id)[0]['hash']
            
            if not (user_email == email and check_password_hash(user_hash, password)):
                flash("Incorrect email or password", "warning")
                return render_template('reset_confirmation.html', user_name=user_name, action=action, verification_purpose="reset-confirmation", with_google = with_google)
        
        user = db.execute("SELECT fullname, username, email, hash FROM users WHERE id = ?", user_id)[0]
        path_id = db.execute("SELECT path_id FROM user_paths WHERE user_id = ?", user_id)[0]['path_id']
        if with_google:
            google_id = db.execute("SELECT google_id FROM users WHERE id = ?", user_id)[0]['google_id']
        db.execute("DELETE FROM users WHERE id = ?", user_id)
        if with_google:
            db.execute(
                "INSERT INTO users (id, fullname, username, email, hash, google_id) VALUES (?, ?, ?, ?, ?, ?)",
                user_id , user['fullname'], user['username'], user['email'], user['hash'], google_id
            )
        else:
            db.execute(
                "INSERT INTO users (id, fullname, username, email, hash) VALUES (?, ?, ?, ?, ?)",
                user_id , user['fullname'], user['username'], user['email'], user['hash']
            )
        db.execute("""
            INSERT INTO user_paths (user_id, path_id)
            VALUES
            (?,?)
        """, user_id, path_id )
        session["user_id"] = user_id
        flash("Your account has been reset", "success")
        return redirect("/dashboard")
    
    return render_template("reset_confirmation.html", user_name=user_name, action=action, verification_purpose="reset-confirmation", with_google = with_google)




@app.errorhandler(404)
def page_not_found(e):
    user_id = session.get('user_id')
    if user_id:
        result = db.execute("""
            SELECT fullname FROM users 
            WHERE id = ?
        """, (user_id,))
        fullname = result[0]['fullname'] if result else None
        name = fullname.split()[0] if fullname else None
    else:
        name = None
    return render_template('404.html', user_id=user_id, name=name), 404


@app.route('/auth/google', methods=["GET"])
def google_login():
    # Get Google's provider configuration
    google_provider_cfg = requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    # Create the request URL for Google login
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route('/auth/google/callback')
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get('code')

    # Get Google's provider configuration
    google_provider_cfg = requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    try:
        token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
    )
    except:
        return "An error occurred during the authentication process.", 500

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Get user info from Google
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Get the user’s information
    try:
        user_info = userinfo_response.json()
        email = user_info["email"]
        fullname = user_info["name"]
        google_id = user_info["sub"]
        username = email.split('@')[0]
    except:
        return "An error occurred during the authentication process.", 500

    # Check if the user exists in the database
    existing_user = db.execute("SELECT * FROM users WHERE google_id = ?", (google_id))
    if len(existing_user) == 0:
        db.execute(
            "INSERT INTO users (google_id, email, fullname, hash, username) VALUES (?, ?, ?, ?, ?)",
            google_id, email, fullname, "GOOGLE_OAUTH", username
        )
        existed = False
    else:
        existed = True
    rows = db.execute (
            "SELECT * from users WHERE email = ?", email
            )
    session['user_id'] = rows[0]['id']
    if existed:
        return redirect('/dashboard')
    else:
        return redirect('/selectpathoauth')

@app.route("/selectpathoauth", methods=["GET", "POST"])
@login_required
def select_path_oauth():
    if request.method == "POST":
        path_id = request.form.get('path_id')
        selected_path = request.form.get('selected_path')

        if path_id and selected_path:
            user_id = session["user_id"]
            db.execute("INSERT INTO user_paths (user_id, path_id) VALUES (?, ?)", 
                       user_id, path_id)

            return redirect(url_for('dashboard'))
    return render_template('select-path.html')


def generate_random_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(6))  # Generate a 6-character code

@app.route('/setnewpassword', methods=["GET", "POST"])
def send_email():
    if session.get('user_id'):
        # Check if the user logged in via Google OAuth
        hash = db.execute("""
            SELECT hash FROM users
            WHERE id = ?
        """, session.get('user_id'))[0]['hash']
        
        # If the user has a password, redirect to change password
        if hash != "GOOGLE_OAUTH":
            return redirect("/changepassword")

    if request.method == "POST":
        email = request.form.get('email')
        
        # Ensure email is provided
        if not email:
            flash("Please enter email", "warning")
            return render_template("set-new-password.html")
        
        # Fetch the logged-in user's ID
        if session.get("user_id"):
            logged_in_user_email = db.execute("""
                SELECT email FROM users
                WHERE id = ?
            """, session.get("user_id"))[0]['email']

            # Ensure the entered email matches the logged-in user's email
            if email != logged_in_user_email:
                flash("Please enter your own email", "warning")
                return render_template("set-new-password.html")

        # Verify that the email exists in the database
        user_record = db.execute("""
            SELECT id, hash FROM users
            WHERE email = ?
        """, email)
        
        if not user_record:
            flash("Email not found", "warning")
            return render_template("set-new-password.html")

        # Check if the user needs to reset their password or set up a new password
        user_hash = user_record[0]['hash']

        # Generate OTP and store it in the database
        otp = generate_random_code()
        db.execute("""
            INSERT INTO otps (user_id, otp_hash)
            VALUES (?,?)
        """, user_record[0]['id'], generate_password_hash(otp))

        # Get user full name
        user_name = db.execute("""
            SELECT fullname FROM users
            WHERE email = ?
        """, email)[0]['fullname']
        user_name = user_name.split(' ')[0]

        if user_hash == "GOOGLE_OAUTH":
            # This is a password setup scenario
            subject = "Password Setup Code - Infix"
            message_body = f"Dear {user_name},\n\nWe have received a request to set up a new password for your Infix account. Please use the following one-time code to complete the setup process:\n\nCode: {otp}\n\nThis code is valid for 20 minutes. If you did not initiate this request, please disregard this message. Your account remains secure.\n\nThank you for using Infix.\n\nBest Regards,"
        else:
            # This is a password reset scenario
            subject = "Password Reset Code - Infix"
            message_body = f"Dear {user_name},\n\nWe have received a request to reset the password for your Infix account. Please use the following one-time code to complete the setup process:\n\nCode: {otp}\n\nThis code is valid for 20 minutes. If you did not initiate this request, please disregard this message. Your account remains secure.\n\nThank you for using Infix.\n\nBest Regards,"

        # Send the appropriate email
        msg = Message(subject, recipients=[email])
        msg.body = message_body + f"\n\n--\nInfix Team\nExcel Beyond\n🌐 www.infix.com\n📞+92-333-2498905, + 92-334-2087247\n"
        mail.send(msg)

        # Flash message and redirect
        flash("OTP sent to your email", "info")
        session['email'] = email
        return redirect('/OTPverification')

    return render_template("set-new-password.html")

@app.route('/OTPverification', methods=['POST', 'GET'])
def verify_otp():
    email = session.get('email')
    if not email:
        flash("Error occurred with email verification, please try again", "warning")
        return redirect('/setnewpassword')

    user_id = session.get('user_id')
    if user_id:
        hash_record = db.execute("""
            SELECT hash FROM users
            WHERE id = ?
        """, user_id)

        if not hash_record or hash_record[0]['hash'] != "GOOGLE_OAUTH":
            return redirect("/changepassword")

    if request.method == "POST":
        otp = request.form.get('otp')
        password = request.form.get('new-pwd')
        confirm_password = request.form.get('confirm-new-pwd')

        if not otp:
            flash("Please enter OTP", "warning")
            return render_template('enter-otp.html', email=email)

        if len(otp) != 6:
            flash("OTP only has 6 characters", "warning")
            return render_template('enter-otp.html', email=email)

        if not password or not confirm_password:
            flash("Please enter the password in both fields", "warning")
            return render_template('enter-otp.html', email=email)

        if len(password) < 8:
            flash("Password must contain at least 8 characters", "warning")
            return render_template('enter-otp.html', email=email)

        if password != confirm_password:
            flash("Both password fields must be the same", "warning")
            return render_template('enter-otp.html', email=email)

        if not user_id:
            result = db.execute("""
                SELECT id FROM users
                WHERE email = ?
            """, email)
            if len(result) == 0:
                flash("Error occurred with email verification, please try again", "warning")
                session.clear()
                return redirect("/setnewpassword")
            else:
                user_id = result[0]["id"]

        # Retrieve the OTP record
        otp_record = db.execute("""
            SELECT otp_hash, generated_at FROM otps
            WHERE user_id = ?
            ORDER BY generated_at DESC
            LIMIT 1
        """, user_id)

        if len(otp_record) == 0:
            flash("Error occurred during the verification process. Please try again.", "warning")
            return redirect('/setnewpassword')

        # Convert the `generated_at` to a datetime object (assuming stored in UTC)
        generated_at = datetime.strptime(otp_record[0]["generated_at"], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

        # Calculate the expiry time
        time_limit = generated_at + timedelta(minutes=20)

        # Check if the OTP has expired
        if time_limit < datetime.now(timezone.utc):
            flash("OTP expired, please try again", "warning")
            return render_template('enter-otp.html', email=email)

        # Verify the OTP hash
        if not check_password_hash(otp_record[0]["otp_hash"], otp):
            flash("Incorrect OTP, make sure you are using the most recent one", "warning")
            return render_template('enter-otp.html', email=email)

        # Update password
        hash = generate_password_hash(password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)

        # Clear session and redirect to login
        session.clear()
        flash("Password updated. Please log in.", "success")
        return redirect('/login')

    return render_template('enter-otp.html', email=email)

@app.route('/studyguides', methods=["GET", "POST"])
@login_required
def study_guides():
    if request.method == 'POST':
        search_query = request.form.get('search')
        if search_query:
            if len(search_query) >= 21:
                flash('Search query must be less than 20 characters', "warning")
                return render_template('study-guides.html')
            return redirect(url_for('search_study_guides', q=search_query))
    else:
        return render_template('study-guides.html')

@app.route('/studyguides/search')
@login_required
def search_study_guides():
    search_query = request.args.get('q')
    if not search_query:
        flash("Please provide a search term.", "warning")
        return redirect(url_for('study_guides'))

    query = """
        SELECT sg.id, sg.title, sg.author, DATE(sg.created_at) AS created_date, 
            GROUP_CONCAT(l.name) AS labels
        FROM study_guides sg
        LEFT JOIN study_guides_labels sgl ON sg.id = sgl.study_guide_id
        LEFT JOIN labels l ON sgl.label_id = l.id
        WHERE sg.title LIKE ? OR sg.author LIKE ? OR l.name LIKE ?
        GROUP BY sg.id
        ORDER BY sg.created_at DESC;
        """
    search_param = f'%{search_query}%'
    
    try:
        result = db.execute(query, search_param, search_param, search_param)
        study_guides = []
        for row in result:
            study_guide = {
                'id': row['id'],
                'title': row['title'],
                'author': row['author'],
                'created_at': row['created_date'],
                # Split the 'labels' string into an array
                'labels': row['labels'].split(',') if row['labels'] else []  # Handle case when labels is None
            }
            print(study_guide)
            study_guides.append(study_guide)
    except Exception as e:
        flash("There was an error retrieving the study guides.", "warning")
        return redirect(url_for('study_guides'))
    
    return render_template('study-guides-list.html', study_guides=study_guides, search_query=search_query)

@app.route('/allstudyguides')
@login_required
def all_guides():
    try:
        query = """
        SELECT sg.id, sg.title, sg.author, DATE(sg.created_at) AS created_date, 
            GROUP_CONCAT(l.name) AS labels
        FROM study_guides sg
        LEFT JOIN study_guides_labels sgl ON sg.id = sgl.study_guide_id
        LEFT JOIN labels l ON sgl.label_id = l.id
        GROUP BY sg.id
        ORDER BY created_at DESC
        """
        result = db.execute(query)
        study_guides = []
        for row in result:
            study_guide = {
                'id': row['id'],
                'title': row['title'],
                'author': row['author'],
                'created_at': row['created_date'],
                # Split the 'labels' string into an array
                'labels': row['labels'].split(',') if row['labels'] else []  # Handle case when labels is None
            }
            study_guides.append(study_guide)
    except Exception as e:
        flash("There was an error retrieving the study guides.", "warning")
        return redirect(url_for('study_guides'))

    return render_template('study-guides-list.html', study_guides=study_guides, search_query='all')

@app.route('/progress')
def progress():
    user_id = session.get('user_id')
    user_info = db.execute("SELECT fullname FROM users WHERE id = ?", (user_id,))
    fullname = user_info[0]['fullname'] if user_info else 'User'
    firstname = fullname.split()[0]

    courses = db.execute("""
        SELECT c.id, c.name, course_code
        FROM courses c
        JOIN user_courses uc ON c.id = uc.course_id
        WHERE uc.user_id = ?
    """, user_id,)
    
    topics_by_course = {}
    completion_data = {}
    
    for course in courses:
        topics = db.execute("""
            SELECT t.id, t.title,
                CASE WHEN ut.id IS NOT NULL THEN 1 ELSE 0 END AS completed
            FROM topics t
            LEFT JOIN user_topics ut ON t.id = ut.topic_id AND ut.user_id = ?
            WHERE t.course_id = ?
        """, user_id, course['id'])
        
        topics_by_course[course['id']] = topics

        total_topics = len(topics)
        completed_topics = sum(topic['completed'] for topic in topics)
        completion_percentage = (completed_topics / total_topics) * 100 if total_topics > 0 else 0

        completion_data[course['id']] = {
            'total': total_topics,
            'completed': completed_topics,
            'percentage': completion_percentage
        }

    return render_template('progress.html', courses=courses, topics_by_course=topics_by_course, completion_data=completion_data, firstname=firstname)


















if __name__ == "__main__":
    app.run(debug=True)