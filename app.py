from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import re

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize database connection
db = SQL("sqlite:///data/infix.db")
db.execute('PRAGMA foreign_keys = ON')
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
        elif not request.form.get("nickname"):
            flash("Must enter nickname", "warning")
        elif len(request.form.get("nickname")) < 3:
            flash("Nickname must include at least 3 characters", "warning")
        elif len(request.form.get("name")) < 7:
            flash("Name must include at least 7 characters", "warning")
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
            nickname = request.form.get("nickname")
            if db.execute("SELECT nickname FROM users WHERE nickname = ?", nickname):
                unique = False
                flash("Whoa, someone already has that nickname, please choose a different one", "warning")
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
                            "INSERT INTO users (fullname, nickname, email, hash) VALUES (?,?,?,?)",
                            fullname, nickname, email, hash
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
def change_password():
    if request.method == 'POST':
        if not request.form.get("email"):
                flash("Must enter email", "warning")
        elif not request.form.get("nickname"):
            flash("Must enter nickname", "warning")
        elif not request.form.get("new-pwd"):
                flash("Must enter password", "warning")
        elif not request.form.get("confirm-new-pwd"):
            flash("Please confirm password", "warning")
        elif len(request.form.get("new-pwd")) < 8:
            flash("Password must include at least 8 characters", "warning")
        elif request.form.get("confirm-new-pwd") != request.form.get("new-pwd"):
            flash("Passwords don't match", "warning")
        else:
            email = request.form.get("email")
            nickname = request.form.get("nickname")
            rows = db.execute (
                "SELECT nickname from users WHERE email = ?", email
            )
            # Ensure email exists and nickname is correct
            if len(rows) != 1 or nickname.lower() != rows[0]["nickname"].lower():
                flash("Invalid email and/or nickname", "warning")
            else:
                newpwd = request.form.get("new-pwd")
                hash = generate_password_hash(newpwd)
                # check if new password same as old password
                rows = db.execute(
                    "SELECT hash FROM users WHERE email = ?", email
                )
                if check_password_hash(rows[0]["hash"], newpwd):
                    flash("New password cannot be same as old password", "warning")
                else:
                    # update password
                    id = db.execute(
                        "UPDATE users SET hash = ? WHERE email = ?", hash, email
                    )
                    if id:
                        # forget user
                        flash("Password Updated, Please Login again", "success")
                        session.clear()
                         
    
    return render_template("change-password.html")

@login_required
@app.route("/logout")
def log_out():
    session.clear()
    return redirect("/")

@app.route("/selectpath", methods = ['POST'])
def select_path():
    if not session.get('user_id'):
        return render_template('sign-up.html')

    return redirect('/dashboard')


@app.route('/dashboard')
@login_required 
def dashboard():
    user_id = session['user_id']

    # Get user's name
    user_info = db.execute("SELECT fullname FROM users WHERE id = ?", user_id)
    fullname = user_info[0]['fullname'] if user_info else None
    first_name = fullname.split()[0] if fullname else None

    # Get the user's selected path id
    user_path_id = db.execute("SELECT path_id FROM user_paths WHERE user_id = ?", user_id)
    path_id = user_path_id[0]['path_id'] if user_path_id else None

    # Get path name based on path_id
    user_path_name = db.execute("SELECT name FROM paths WHERE id = ?", path_id)
    path_name = user_path_name[0]['name'] if user_path_name else None

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

    return render_template('dashboard.html', path_name = path_name, enrolled_courses = enrolled_courses, first_name = first_name, bookmarks = bookmarks)


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

    db.execute("""
        INSERT INTO user_courses (user_id, course_id)
        VALUES
        (?,?)
    """, user_id, course_id)
    flash("Course Enrolled!")
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

    db.execute("""
        DELETE FROM user_courses
        WHERE user_id = ? AND course_id = ?
    """, user_id, course_id)
    flash("Course Deleted!")
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
        return redirect('/dashboard')
    else:
        path_id = result[0]["id"]
    db.execute("""
        UPDATE user_paths
        SET path_id = ?
        WHERE user_id = ?
    """, path_id, user_id)
    return redirect('/dashboard')

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    user_id = session["user_id"]
    
    if request.method == "POST":
        fullname = request.form.get("fullname")
        nickname = request.form.get("nickname")
        email = request.form.get("email")
        
        current_user = db.execute("SELECT fullname, nickname, email FROM users WHERE id = ?", user_id)[0]
        current_fullname = current_user['fullname']
        current_nickname = current_user['nickname']
        current_email = current_user['email']

        # Validate input
        if not fullname:
            flash("Must enter name", "warning")
        elif not nickname or len(nickname) < 3:
            flash("Nickname must include at least 3 characters", "warning")
        elif not email or not re.match(email_regex, email):
            flash("Invalid email format", "warning")
        else:
            if (fullname == current_fullname and 
                nickname == current_nickname and 
                email == current_email):
                flash("No updated changes made", "info")
            else:
                existing_user = db.execute("SELECT * FROM users WHERE (nickname = ? OR email = ?) AND id != ?", nickname, email, user_id)
                if existing_user:
                    flash("Nickname and/or Email already exists", "warning")
                else:
                    db.execute("UPDATE users SET fullname = ?, nickname = ?, email = ? WHERE id = ?", fullname, nickname, email, user_id)
                    flash("Settings updated successfully", "success")
    

    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
    return render_template("settings.html", user=user)

@app.route("/delete-confirmation", methods=["GET", "POST"])
@login_required
def delete_account():
    user_id = session["user_id"]
    user = db.execute("SELECT nickname FROM users WHERE id = ?", user_id)[0]
    user_name = user['nickname']
    if request.method == "POST":
        db.execute("DELETE FROM users WHERE id = ?", user_id)
        session.clear()
        return redirect("/")
    return render_template("delete_confirmation.html", user_name = user_name)

@app.route("/reset-confirmation", methods=["GET", "POST"])
@login_required
def reset_progress():
    user_id = session["user_id"]
    user = db.execute("SELECT nickname FROM users WHERE id = ?", user_id)[0]
    user_name = user['nickname']
    if request.method == "POST":
        user = db.execute("SELECT fullname, nickname, email, password_hash, path FROM users WHERE id = ?", user_id)[0]
        db.execute("DELETE FROM users WHERE id = ?", user_id)
        new_user_id = db.execute(
            "INSERT INTO users (fullname, nickname, email, password_hash, path) VALUES (?, ?, ?, ?, ?)",
            user['fullname'], user['nickname'], user['email'], user['password_hash'], user['path']
        )
        session["user_id"] = new_user_id
        return redirect("/dashboard")
    return render_template("reset_confirmation.html", user_name = user_name)



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





if __name__ == "__main__":
    app.run(debug=True)