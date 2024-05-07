from flask_login import login_user, login_required, logout_user, current_user
from flask import Flask, redirect, url_for, render_template, Blueprint, request, flash
from database import User, db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(email, password):
     user = User(email=email, password=generate_password_hash(password, method="scrypt"))
     db.session.add(user)
     db.session.commit()
     


auth = Blueprint("auth", __name__, url_prefix='/auth')

@auth.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        email = request.form.get("email_input")
        password = request.form.get("password_input")
        

        user = User.query.filter_by(email=email).first()
        if user:
             if check_password_hash(user.password, password):
                  login_user(user, remember=True)
                  return redirect("/")
        

    return render_template("login.html")

@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
        
        if request.method == "POST":
            email = request.form.get("email_input")
            password1 = request.form.get("password_confirm1")  
            password2 = request.form.get("password_confirm2")

        
            user = User.query.filter_by(email=email).first()

            if user:
                flash("User already exists!", category="error")
            elif password1 != password2:
                flash("Passwords don't match!", category="error")
            elif len(email) < 1:
                 flash("email too short!", category="error")
            elif len(password1) < 3:
                 flash("password too short!", category="error")
            else:
                create_user(email, password1)
                return redirect("/login")
                 

        return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
     logout_user()
     return redirect("/login")