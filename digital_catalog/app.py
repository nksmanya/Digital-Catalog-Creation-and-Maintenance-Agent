from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'agri-secret'

# ----------------- Database Setup -----------------

def init_db():
    conn = sqlite3.connect('agri.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def init_product_table():
    conn = sqlite3.connect('agri.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database tables
init_db()
init_product_table()

# ----------------- Routes -----------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('agri.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user'] = user[1]  # Save user's name in session
        return redirect('/catalog')
    else:
        flash("Invalid credentials!")
        return redirect('/')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register-user', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('agri.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        ''', (name, email, password))
        conn.commit()
        flash("Registration successful! Please login.")
        return redirect('/')
    except sqlite3.IntegrityError:
        flash("Email already exists!")
        return redirect('/register')
    finally:
        conn.close()

@app.route('/catalog')
def catalog():
    if 'user' not in session:
        flash("Please login first.")
        return redirect('/')

    conn = sqlite3.connect('agri.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('catalog.html', products=products)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if 'user' not in session:
        flash("Please login first.")
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        description = request.form['description']

        conn = sqlite3.connect('agri.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, category, price, description) VALUES (?, ?, ?, ?)",
                       (name, category, price, description))
        conn.commit()
        conn.close()
        return redirect('/catalog')

    return render_template('add_product.html')

@app.route('/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if 'user' not in session:
        flash("Please login first.")
        return redirect('/')

    conn = sqlite3.connect('agri.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        description = request.form['description']

        cursor.execute('''
            UPDATE products
            SET name=?, category=?, price=?, description=?
            WHERE id=?
        ''', (name, category, price, description, id))
        conn.commit()
        conn.close()
        return redirect('/catalog')

    cursor.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/delete-product/<int:id>')
def delete_product(id):
    if 'user' not in session:
        flash("Please login first.")
        return redirect('/')

    conn = sqlite3.connect('agri.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/catalog')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%B %d, %Y'):
    try:
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)
    except:
        return value

if __name__ == "__main__":
    app.run(debug=True)
