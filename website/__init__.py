# start importing

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
from random import sample
from string import ascii_letters, punctuation

# end importing


# Creating an list of all characters we will use this two genrate key
all_chars = list(ascii_letters) + list(punctuation) + [str(num) for num in range(10)]


# Creating istance of SQLAlchemy Class
db = SQLAlchemy()


def create_app():
    # Creating an app instance of Flask
    app = Flask(__name__)

    # Genearting secret key
    app.config["SECRET_KEY"] = "".join(sample(all_chars, 58))

    # loading database informations from environnement variables file
    load_dotenv(os.path.join(os.path.dirname(__file__), "DB_INFO.env"))

    # configuring SQLALCHEMY Data base and changing the default sqlconnector to pymysql
    SQLALCHEMY_DATABASE_URI = f"{os.getenv('DB_URI')}"
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = SQLALCHEMY_DATABASE_URI  # Uniform Resource Identifier
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initializing Database
    db.init_app(app)

    # Importing Blueprints
    from .views import views
    from .auth import auth
    from .admin import admin

    # Protecting Blueprints against CSRF Attacks
    csrf = CSRFProtect(app)
    csrf.exempt(views)
    csrf.exempt(auth)

    # Registering blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/admin")

    # importing models
    from .models import User, Todo

    return app


# Creating database and tables
app = create_app()

with app.app_context():  # Create the database in app context
    db.create_all()
