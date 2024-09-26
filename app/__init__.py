from flask import Flask
from . import routes
from .models import db, User, bcrypt
from flask_login import LoginManager
login_manager = LoginManager()
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Import and register blueprints (if needed)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    db.init_app(app)
    bcrypt.init_app(app)


    login_manager.init_app(app)
    login_manager.login_view = 'main.signin'  # Redirect to login page if not logged in
    # login_manager.login_message_category = 'info'
    from . import routes
    app.register_blueprint(routes.bp)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app