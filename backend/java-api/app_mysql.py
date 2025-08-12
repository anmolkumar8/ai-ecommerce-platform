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

# MySQL Database connection - Your credentials!
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'ecommerce_db',
    'user': 'root',          # Your username
    'password': 'Anmol@123', # Your password
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def get_db():
    """Get MySQL database connection"""
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize MySQL database with tables and sample data"""
    conn = get_db()
    if not conn:
        print("❌ Could not connect to MySQL database!")
        print("💡 Make sure MySQL is running with the correct credentials:")
        print(f"   Host: {DATABASE_CONFIG['host']}")
        print(f"   Username: {DATABASE_CONFIG['user']}")
        print(f"   Password: {DATABASE_CONFIG['password']}")
        print(f"   Database: {DATABASE_CONFIG['database']}")
        return False
        
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                category_id INT,
                sku VARCHAR(50) UNIQUE NOT NULL,
                stock_quantity INT DEFAULT 0,
                is_featured BOOLEAN DEFAULT FALSE,
                image_url VARCHAR(500) DEFAULT 'https://via.placeholder.com/300x300?text=Product',
                rating DECIMAL(3,2) DEFAULT 4.0,
                review_count INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Create cart table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Create orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                order_number VARCHAR(50) UNIQUE NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                status VARCHAR(50) DEFAULT 'pending',
                payment_method VARCHAR(50),
                payment_status VARCHAR(50) DEFAULT 'pending',
                shipping_address TEXT,
                billing_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Create order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                product_name VARCHAR(200) NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                total_price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Insert sample categories
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            categories = [
                ('Electronics', 'Electronic devices and gadgets'),
                ('Clothing', 'Fashion and apparel'),
                ('Books', 'Books and educational materials'),
                ('Home & Garden', 'Home improvement supplies'),
                ('Sports', 'Sports and fitness equipment')
            ]
            
            cursor.executemany(
                'INSERT INTO categories (name, description) VALUES (%s, %s)', 
                categories
            )
        
        # Insert sample products
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            products = [
                ('Smartphone Pro Max', 'Latest flagship smartphone with AI camera', 84999.99, 1, 'PHONE-001', 50, True),
                ('Wireless Headphones', 'Premium noise-cancelling headphones', 16500.99, 1, 'AUDIO-001', 25, True),
                ('Ultra-Slim Laptop', 'High-performance laptop for professionals', 107999.99, 1, 'LAPTOP-001', 15, True),
                ('Smart Watch', 'Advanced smartwatch with health monitoring', 24999.99, 1, 'WATCH-001', 30, False),
                ('Organic Cotton T-Shirt', 'Comfortable 100% organic cotton t-shirt', 1299.99, 2, 'SHIRT-001', 100, False),
                ('Designer Jeans', 'Premium denim jeans with perfect fit', 4599.99, 2, 'JEANS-001', 75, False),
                ('Running Shoes Pro', 'Professional running shoes with advanced cushioning', 8999.99, 2, 'SHOES-001', 60, True),
                ('Programming Guide', 'Complete guide to modern programming languages', 2499.99, 3, 'BOOK-001', 40, False),
                ('AI & Machine Learning', 'Comprehensive guide to artificial intelligence', 2999.99, 3, 'BOOK-002', 35, False),
                ('Garden Tools Set', 'Professional gardening tools set', 6499.99, 4, 'GARDEN-001', 20, False)
            ]
            
            cursor.executemany('''
                INSERT INTO products 
                (name, description, price, category_id, sku, stock_quantity, is_featured) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', products)
        
        # Insert sample users
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            users = [
                ('johndoe', 'john@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'John', 'Doe', '9876543210'),
                ('janesmit', 'jane@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'Jane', 'Smith', '9876543211'),
                ('anmolkumar', 'anmol@example.com', hashlib.sha256('Anmol@123'.encode()).hexdigest(), 'Anmol', 'Kumar', '9876543212')
            ]
            
            cursor.executemany('''
                INSERT INTO users 
                (username, email, password_hash, first_name, last_name, phone) 
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', users)
        
        # Insert sample orders for demonstration
        cursor.execute("SELECT COUNT(*) FROM orders")
        if cursor.fetchone()[0] == 0:
            orders = [
                (1, 'ORD-001', 101499.98, 'completed', 'credit_card', 'paid', '123 Main St, New Delhi, India', '123 Main St, New Delhi, India'),
                (2, 'ORD-002', 107999.99, 'pending', 'upi', 'pending', '456 Oak Ave, Mumbai, India', '456 Oak Ave, Mumbai, India'),
                (3, 'ORD-003', 33499.97, 'shipped', 'debit_card', 'paid', '789 Pine Rd, Bangalore, India', '789 Pine Rd, Bangalore, India')
            ]
            
            cursor.executemany('''
                INSERT INTO orders 
                (user_id, order_number, total_amount, status, payment_method, payment_status, shipping_address, billing_address) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', orders)
            
            # Insert order items
            order_items = [
                # Order 1 items
                (1, 1, 'Smartphone Pro Max', 1, 84999.99, 84999.99),
                (1, 2, 'Wireless Headphones', 1, 16500.99, 16500.99),
                # Order 2 items  
                (2, 3, 'Ultra-Slim Laptop', 1, 107999.99, 107999.99),
                # Order 3 items
                (3, 1, 'Smartphone Pro Max', 1, 24999.99, 24999.99),
                (3, 7, 'Running Shoes Pro', 1, 8999.99, 8999.99)
            ]
            
            cursor.executemany('''
                INSERT INTO order_items 
                (order_id, product_id, product_name, quantity, unit_price, total_price) 
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', order_items)
        
        conn.commit()
        print("✅ MySQL database initialized successfully!")
        print(f"🔗 Connected to: mysql://{DATABASE_CONFIG['user']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}")
        print(f"👤 Username: {DATABASE_CONFIG['user']}")
        print(f"🗄️ Database: {DATABASE_CONFIG['database']}")
        return True
        
    except Error as e:
        print(f"❌ Database initialization error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# JWT Token verification decorator
def verify_token(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = payload['user_id']
            return f(current_user_id, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    
    decorator.__name__ = f.__name__
    return decorator

# API Routes
@app.route('/actuator/health', methods=['GET'])
def health_check():
    conn = get_db()
    if conn:
        conn.close()
        return jsonify({
            'status': 'UP',
            'database': 'MySQL',
            'message': 'Connected successfully'
        })
    else:
        return jsonify({
            'status': 'DOWN',
            'database': 'MySQL',
            'message': 'Database connection failed'
        }), 503

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            'SELECT id, username, email, first_name, last_name FROM users WHERE username = %s AND password_hash = %s',
            (username, password_hash)
        )
        
        user = cursor.fetchone()
        
        if user:
            token = generate_token(user['id'])
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': user
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute('''
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id 
            ORDER BY p.created_at DESC
        ''')
        products = cursor.fetchall()
        
        return jsonify({
            'products': products
        })
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/products/featured', methods=['GET'])
def get_featured_products():
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute('''
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id 
            WHERE p.is_featured = TRUE
            ORDER BY p.created_at DESC
        ''')
        products = cursor.fetchall()
        
        return jsonify({
            'featured_products': products
        })
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("🚀 Starting ANUFA E-commerce API with MySQL...")
    print("="*50)
    
    if init_db():
        print("✅ Database ready!")
        print("🌐 API starting on http://localhost:8080")
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        print("❌ Failed to initialize database. Please check your MySQL setup.")
        print("\n💡 To fix this:")
        print("1. Make sure MySQL is running")
        print("2. Check MySQL Workbench connection")
        print("3. Verify database 'ecommerce_db' exists")
        print("4. Ensure user 'root' has proper permissions")
