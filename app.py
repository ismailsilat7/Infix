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
            return render_template('index.html')

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

@app.route("/logout")
def log_out():
    session.clear()
    return redirect("/")


























if __name__ == "__main__":
    app.run(debug=True)