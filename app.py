from flask import Flask, render_template, request, redirect, url_for, flash, session

import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong secret key

# --------- Database Setup ----------
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            email TEXT,
            phone TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --------- Language Setting Route ----------
@app.route('/set_language', methods=['POST'])
def set_language():
    session['lang'] = request.form.get('language', 'en')
    # Return no content; frontend reloads page after form submit
    return '', 204

# --------- Register Route ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = session.get('lang', 'en')
    if request.method == 'POST':
        role = request.form['role']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (role, email, phone, password) VALUES (?, ?, ?, ?)",
                       (role, email, phone, password))
        conn.commit()
        conn.close()
        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', lang=lang)

# --------- Login Route ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('lang', 'en')
    if request.method == 'POST':
        email_or_phone = request.form['email_or_phone']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE (email=? OR phone=?) AND password=?", 
                       (email_or_phone, email_or_phone, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            flash("Login successful!", "success")
            return "Welcome " + user[1]  # Here you can redirect to dashboard
        else:
            flash("Invalid credentials", "error")

    return render_template('login.html', lang=lang)

# --------- Root Route redirects to login ----------
@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
