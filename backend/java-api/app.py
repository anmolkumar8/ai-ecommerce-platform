from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import hashlib
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'anufa-secret-key-2024')

# Database file path
DATABASE = 'ecommerce.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category_id INTEGER,
            sku TEXT UNIQUE NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            is_featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    # Insert sample data
    categories = [
        (1, 'Electronics', 'Electronic devices and gadgets'),
        (2, 'Clothing', 'Fashion and apparel'),
        (3, 'Books', 'Books and educational materials'),
        (4, 'Home & Garden', 'Home improvement supplies'),
        (5, 'Sports', 'Sports and fitness equipment')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO categories (id, name, description) VALUES (?, ?, ?)', categories)
    
    products = [
        (1, 'Smartphone Pro Max', 'Latest flagship smartphone', 999.99, 1, 'PHONE-001', 50, 1),
        (2, 'Wireless Headphones', 'Premium noise-cancelling headphones', 299.99, 1, 'AUDIO-001', 25, 1),
        (3, 'Ultra-Slim Laptop', 'High-performance laptop', 1299.99, 1, 'LAPTOP-001', 15, 1),
        (4, 'Smart Watch', 'Advanced smartwatch', 399.99, 1, 'WATCH-001', 30, 0),
        (5, 'Organic Cotton T-Shirt', 'Comfortable organic cotton t-shirt', 29.99, 2, 'SHIRT-001', 100, 0),
        (6, 'Designer Jeans', 'Premium denim jeans', 89.99, 2, 'JEANS-001', 75, 0),
        (7, 'Running Shoes Pro', 'Professional running shoes', 149.99, 2, 'SHOES-001', 60, 1),
        (8, 'Programming Book', 'Learn modern programming', 49.99, 3, 'BOOK-001', 40, 0),
        (9, 'AI Guide', 'Complete AI guide', 59.99, 3, 'BOOK-002', 35, 0),
        (10, 'Garden Tools Set', 'Professional gardening tools', 129.99, 4, 'GARDEN-001', 20, 0)
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO products 
        (id, name, description, price, category_id, sku, stock_quantity, is_featured) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', products)
    
    # Insert sample users
    users = [
        (1, 'johndoe', 'john@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'John', 'Doe'),
        (2, 'janesmit', 'jane@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'Jane', 'Smith')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO users 
        (id, username, email, password_hash, first_name, last_name) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', users)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Initialize database on startup
init_db()

def get_db():
    return sqlite3.connect(DATABASE)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# API Routes
@app.route('/actuator/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'UP',
        'service': 'ecommerce-java-api',
        'timestamp': datetime.datetime.now().isoformat(),
        'database': 'SQLite'
    })

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[2] == hashlib.sha256(password.encode()).hexdigest():
        token = generate_token(user[0])
        return jsonify({
            'token': token,
            'user': {
                'id': user[0],
                'username': user[1]
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    if not all([username, email, password, first_name, last_name]):
        return jsonify({'error': 'All fields required'}), 400
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, first_name, last_name))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        token = generate_token(user_id)
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': user_id,
                'username': username
            }
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 409

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.stock_quantity > 0
    ''')
    products = cursor.fetchall()
    conn.close()
    
    product_list = []
    for product in products:
        product_list.append({
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'category_id': product[4],
            'sku': product[5],
            'stock_quantity': product[6],
            'is_featured': bool(product[7]),
            'category_name': product[9] if len(product) > 9 else None
        })
    
    return jsonify({'products': product_list})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id = ?
    ''', (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({
        'product': {
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'category_id': product[4],
            'sku': product[5],
            'stock_quantity': product[6],
            'is_featured': bool(product[7]),
            'category_name': product[9] if len(product) > 9 else None
        }
    })

@app.route('/categories', methods=['GET'])
def get_categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()
    
    category_list = []
    for category in categories:
        category_list.append({
            'id': category[0],
            'name': category[1],
            'description': category[2]
        })
    
    return jsonify({'categories': category_list})

@app.route('/products/featured', methods=['GET'])
def get_featured_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.is_featured = 1 AND p.stock_quantity > 0
        LIMIT 10
    ''')
    products = cursor.fetchall()
    conn.close()
    
    product_list = []
    for product in products:
        product_list.append({
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'category_id': product[4],
            'sku': product[5],
            'stock_quantity': product[6],
            'is_featured': bool(product[7]),
            'category_name': product[9] if len(product) > 9 else None
        })
    
    return jsonify({'featured_products': product_list})

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'products': []})
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.name LIKE ? OR p.description LIKE ?
        AND p.stock_quantity > 0
    ''', (f'%{query}%', f'%{query}%'))
    products = cursor.fetchall()
    conn.close()
    
    product_list = []
    for product in products:
        product_list.append({
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'category_id': product[4],
            'sku': product[5],
            'stock_quantity': product[6],
            'is_featured': bool(product[7]),
            'category_name': product[9] if len(product) > 9 else None
        })
    
    return jsonify({'products': product_list, 'query': query})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host=host, port=port, debug=debug)
