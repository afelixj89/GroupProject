from flask_app import app
from flask import render_template, redirect, request, session, flash
# Import your models
from flask_app.models import user
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

# / roote route for showing the login/registration page
@app.route("/")
def index():
    return render_template("login.html")

# /dashboard - shows the dashboard - but you must be logged in 
@app.route("/dashboard")
def dashboard():
    pass
#this is backlog if given more t ime


# /register (INVISIBLE POST route) - handles registering a new user 
@app.route("/register", methods=["POST"])
def register():
    if not user.User.validate_registration(request.form):
        return redirect("/")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session["user_id"] = user.User.register_user(data) 
    session["first_name"] = user.User.register_user(data)
    return redirect("/flights")


# /login (INVISIBLE POST route) - logs a user in 
@app.route("/login", methods=["POST"])
def login():
    if not user.User.validate_login(request.form):
        return redirect("/")
    data = {
        "email": request.form["email"]
    }
    logged_in_user = user.User.get_by_email(data)
    session["user_id"] = logged_in_user.id
    return redirect("/flights")

# /logout (INVISIBLE route) - clears session, sends the user back to login/registration page. 
@app.route("/logout")
def logout():
    session.clear() 
    return redirect("/")