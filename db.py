from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import logging

db = SQLAlchemy()
migrate = None  # Don't initialize here as no app instance is available yet

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float)
    category = db.Column(db.String(100), nullable=False)

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collark_hub.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    global migrate
    migrate = Migrate(app, db)

def validate_user(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return True
        return False
    except Exception as e:
        logging.exception("Error validating user: %s", e)
        return False

def register_user(username, email, password):
    try:
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return False
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        logging.exception("Failed to register user: %s", e)
        return False

def get_products():
    try:
        return Product.query.all()
    except Exception as e:
        logging.exception("Failed to fetch products: %s", e)
        return []

def get_product_by_id(product_id):
    try:
        return Product.query.get(product_id)
    except Exception as e:
        logging.exception("Failed to fetch product by ID: %s", e)
        return None