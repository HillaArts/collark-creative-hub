from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
import db  # Assuming you have a module named db.py for handling database interactions

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a real secret key for production

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/static/style.css')
def serve_css():
    return send_from_directory('static', 'style.css')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.validate_user(username, password):  # Assume a function that validates the user
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if db.register_user(username, email, password):  # Assume a function that handles user registration
            return redirect(url_for('login'))
        else:
            return "Registration Failed"
    return render_template('register.html')

@app.route('/product_list')
def product_list():
    products = db.get_products()  # Assume a function that fetches product data
    return render_template('product_list.html', products=products)

@app.route('/product_detail/<int:product_id>')
def product_detail(product_id):
    product = db.get_product_by_id(product_id)  # Assume a function that fetches a single product
    return render_template('product_detail.html', product=product)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)