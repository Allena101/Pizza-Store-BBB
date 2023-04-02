from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from os import path
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# from flask_bcrypt import Bcrypt



db = SQLAlchemy()
DB_NAME = "database444.db"

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret secret key key' # generate one later
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .stock import stock

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(stock, url_prefix='/')

    from .models import User, Pizza, PizzaPrice, Topping

    create_database(app)

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')

