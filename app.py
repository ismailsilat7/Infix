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

    return render_template('courses.html', enrolled_courses=enrolled_courses, other_courses=other_courses, path=path, enrolled = enrolled, to_add = to_add)



@app.route('/course/<course_code>')
@login_required
def course_detail(course_code):
    
    # Get the course details using the course name
    course = db.execute("SELECT * FROM courses WHERE course_code = ?", course_code)
    if not course:
        return "Course not found", 404

    course_id = course[0]['id']
    topics = db.execute("SELECT * FROM topics WHERE course_id = ?", course_id)

    return render_template('course_detail.html', course=course[0], topics=topics)

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



# Configure your app with Google OAuth credentials
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID")
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET")
app.config['GOOGLE_DISCOVERY_URL'] = "https://accounts.google.com/.well-known/openid-configuration"

# Initialize OAuth client
client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

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



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')


mail = Mail(app)

def generate_random_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(6))  # Generate a 6-character code

@app.route('/setnewpassword', methods = ["GET", "POST"])
def send_email():
    if session.get('user_id'):
        hash = db.execute("""
            SELECT hash FROM users
            WHERE id = ?
        """, session.get('user_id'))[0]['hash']
        if hash != "GOOGLE_OAUTH":
            return redirect("/changepassword")
    if request.method == "POST":
        email = request.form.get('email')
        if not email:
            flash("Please enter email", "warning")
            return render_template("set-new-password.html")
        id = db.execute("""
            SELECT id FROM users
            WHERE email = ?
        """, email)
        if not id:
            flash("Email not found", "warning")
            return render_template("set-new-password.html")
        otp = generate_random_code()
        db.execute("""
            INSERT INTO otps (user_id, otp_hash)
            VALUES (?,?)
        """, id[0]['id'], generate_password_hash(otp))
        if session.get("user_id"):
            google_id = db.execute("""
                SELECT google_id FROM users
                WHERE id = ?
            """, session.get("user_id"))[0]['google_id']
            if google_id != None:
                msg = Message("Password Setup Code - Infix", recipients=[email])
                msg.body = f"""
                Dear User,

                We have received a request to set up a new password for your Infix account. Please use the following one-time code to complete the setup process:

                Code: {otp}

                This code is valid for 20 minutes. If you did not initiate this request, please disregard this message. Your account remains secure.

                Thank you for using Infix.

                Best regards,
                The Infix Team
                """
            else:
                return redirect('/changepassword')
        else:
            msg = Message("Password Reset Code - Infix", recipients=[email])
            msg.body = f"""
            Dear User,

            We have received a request to reset the password for your Infix account. Please use the following one-time code to complete the reset process:

            Code: {otp}

            This code is valid for 20 minutes. If you did not initiate this request, please disregard this message. Your account remains secure.

            Thank you for using Infix.

            Best regards,
            The Infix Team
            """
        msg.body += f"\n\n--\nInfix Team\nExcel Beyond\n🌐 www.infix.com\n📞+92-333-2498905, + 92-334-2087247\n"
        mail.send(msg)

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
            return render_template('enter-otp.html', email=email)

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





if __name__ == "__main__":
    app.run(debug=True)