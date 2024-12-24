from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder = "../templates", static_folder='../static')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

    UPLOAD_FOLDER = 'recordings'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from recipe.models import User

    @login_manager.user_loader
    def user_loader(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('recipe.login'))

    # Register blueprints
    from recipe.routes import recipe
    app.register_blueprint(recipe)

    migrate = Migrate(app, db)
    return app


