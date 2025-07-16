from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import requests
import os
from texts import translations
import os
import requests
from flask import session, render_template
from texts import translations
from flask import Flask, render_template, session
from werkzeug.utils import secure_filename
import base64
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# ------------------------ Init DBs ------------------------

def init_user_db():
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

def init_catalog_db():
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            stock INTEGER,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_user_db()
init_catalog_db()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
products = []

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = float(data.get('price') or 0)
    stock = int(data.get('stock') or 0)
    category = data.get('category')
    image_base64 = data.get('imageBase64')  # base64 string or None

    image_filename = None
    if image_base64:
        # image_base64 format: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
        header, encoded = image_base64.split(",", 1)  # separate metadata from actual base64
        file_ext = header.split(";")[0].split("/")[1]  # get file extension like png, jpg

        # Generate a unique filename
        image_filename = f"{uuid.uuid4()}.{file_ext}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)

        # Ensure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Decode and save the image file
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(encoded))

    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, description, price, stock, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, description, price, stock, category))
    conn.commit()

    # If you want to save image filename in DB, add a column 'image' in products table
    # and insert it here. For now, this example skips that.

    conn.close()

    return jsonify({"message": "Product added successfully."}), 200
# ------------------------ Language ------------------------

@app.route('/set_language', methods=['POST'])
def set_language():
    data = request.get_json()
    session['lang'] = data.get('lang', 'en')
    return jsonify({"status": "ok"})


# ------------------------ Auth Routes ------------------------

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get("lang", "en")
    text = translations.get(lang, translations["en"])

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user[2]  # email
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html", text=text, lang=lang)


@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = session.get("lang", "en")
    text = translations.get(lang, translations["en"])

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

    return render_template("register.html", text=text, lang=lang)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ------------------------ Dashboard ------------------------

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    lang = session.get("lang", "en")
    text = translations.get(lang, translations["en"])
    user = session.get("user", "Guest")
    return render_template("dashboard.html", text=text, lang=lang, user=user)


# ------------------------ Product APIs ------------------------

# Rename this one to avoid conflict:
@app.route('/get_products')
def get_products_route():
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()

    products = []
    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "stock": row[4],
            "category": row[5]
        })
    return jsonify(products)


@app.route('/api/products')
def api_products():
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, price, stock, category FROM products ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    products = []
    for row in rows:
        products.append({
            "name": row[0],
            "description": row[1],
            "price": row[2],
            "stock": row[3],
            "category": row[4]
        })
    return jsonify({"products": products})


@app.route("/delete_product/<int:id>", methods=["DELETE"])
def delete_product(id):
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})


@app.route("/auto_description", methods=["POST"])
def auto_description():
    data = request.get_json()
    prompt = f"Write a product description for a {data['category']} named {data['name']}."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "API key not set."}), 500

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    try:
        openai_res = response.json()
        desc = openai_res["choices"][0]["message"]["content"]
        return jsonify({"description": desc})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    res = requests.post("https://libretranslate.de/translate", data={
        "q": data["text"], "source": "en", "target": data["target"]
    }).json()
    return jsonify({"translated": res["translatedText"]})

@app.route("/chatbot")
def chatbot():
    lang = session.get("lang", "en")
    text = translations.get(lang, translations["en"])
    return render_template("chatbot.html", text=text, lang=lang)

# ------------------------ Run ------------------------

if __name__ == "__main__":
    app.run(debug=True)
