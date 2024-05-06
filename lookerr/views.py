from flask_login import login_user, login_required, logout_user, current_user

from flask import Flask, redirect, url_for, render_template, Blueprint


views = Blueprint("views", __name__, url_prefix='/views')

@views.route("/")
@login_required
def home():
        return render_template("home.html", user=current_user)