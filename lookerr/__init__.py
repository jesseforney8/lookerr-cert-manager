from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from database import db, User

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.secret_key = "kjg[pioj$%^l332]"

    login_manager = LoginManager()
    login_manager.login_view = "/login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    #Puts flask app in database
    db.init_app(app)

    #creates all tables in db
    with app.app_context():
        db.create_all()

    from auth import auth
    from views import views
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")




    return app