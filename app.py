from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

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
    """Ensure responses aren't cached"""
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
    return render_template('log-in.html')

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        return redirect("/login")
    return render_template("sign-up.html")

@app.route("/changepassword", methods=["GET", "POST"])
def change_password():
    return render_template("change-password.html")





























if __name__ == "__main__":
    app.run(debug=True)