import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, flash, jsonify
from db import init_app, validate_user, register_user, Product
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_default_secret_key')
csrf = CSRFProtect(app)

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collark_hub.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
# Initialize the database with the app
init_app(app)

# Setup loggings
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[RotatingFileHandler('app.log', maxBytes=10000, backupCount=3),
                              logging.StreamHandler()])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/static/css/style.css')
def serve_css():
    return send_from_directory('static', 'css/style.css')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if validate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            logging.warning(f"Login attempt failed for user: {username}")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if register_user(form.username.data, form.email.data, form.password.data):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. User might already exist.')
            logging.warning(f"Registration failed for user: {form.username.data}")
    return render_template('register.html', form=form)

@app.route('/product_list')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@app.route('/product_detail/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/filtered_products')
def filtered_products():
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    query = Product.query
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    products = query.all()
    product_dicts = [{'name': product.name, 'description': product.description, 'price': product.price, 'category': product.category} for product in products]
    return jsonify(product_dicts)

@app.errorhandler(404)
def page_not_found(e):
    logging.error(f"404 Error: {e}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"500 Error: {e}")
    return render_template('500.html'), 500

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])  # Use DateField in a real app with appropriate validators
    description = TextAreaField('Project Description', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

@app.route('/submit-booking', methods=['GET', 'POST'])
def submit_booking():
    form = BookingForm()
    if form.validate_on_submit():
        # Process the data, save to database, send email, etc.
        return redirect(url_for('success'))
    return render_template('booking.html', form=form)

@app.route('/success')
def success():
    return 'Booking successful!'

if __name__ == '__main__':
    app.run(debug=True)