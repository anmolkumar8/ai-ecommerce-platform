from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import hashlib
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'anufa-secret-key-2024')

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'anufa_ecommerce'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Anmol@123'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True
}

# Initialize MySQL database
def init_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                category_id INT,
                sku VARCHAR(255) UNIQUE NOT NULL,
                stock_quantity INT DEFAULT 0,
                is_featured BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
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
        
        cursor.executemany('INSERT IGNORE INTO categories (id, name, description) VALUES (%s, %s, %s)', categories)
        
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
            INSERT IGNORE INTO products 
            (id, name, description, price, category_id, sku, stock_quantity, is_featured) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', products)
        
        # Insert sample users
        users = [
            (1, 'johndoe', 'john@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'John', 'Doe'),
            (2, 'janesmit', 'jane@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'Jane', 'Smith')
        ]
        
        cursor.executemany('''
            INSERT IGNORE INTO users 
            (id, username, email, password_hash, first_name, last_name) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', users)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
        
    except Error as e:
        print(f"Error initializing database: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Initialize database on startup
init_db()

# Helper functions
def get_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise

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
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password_hash FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
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
        
    except Error as e:
        return jsonify({'error': 'Database error'}), 500

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
            VALUES (%s, %s, %s, %s, %s)
        ''', (username, email, password_hash, first_name, last_name))
        user_id = cursor.lastrowid
        conn.commit()
        cursor.close()
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
        
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 409
    except Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/products', methods=['GET'])
def get_products():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.stock_quantity > 0
        ''')
        products = cursor.fetchall()
        cursor.close()
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
    
    except Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.id = %s
        ''', (product_id,))
        product = cursor.fetchone()
        cursor.close()
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
    
    except Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        
        category_list = []
        for category in categories:
            category_list.append({
                'id': category[0],
                'name': category[1],
                'description': category[2]
            })
        
        return jsonify({'categories': category_list})
    
    except Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/products/featured', methods=['GET'])
def get_featured_products():
    try:
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
        cursor.close()
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
    
    except Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'products': []})
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE (p.name LIKE %s OR p.description LIKE %s)
            AND p.stock_quantity > 0
        ''', (f'%{query}%', f'%{query}%'))
        products = cursor.fetchall()
        cursor.close()
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
    
    except Error as e:
        return jsonify({'error': 'Database error'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host=host, port=port, debug=debug)
