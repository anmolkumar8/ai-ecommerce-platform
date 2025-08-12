from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'anufa-secret-key-2024')

# PostgreSQL Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://ecommerce_user:password123@localhost:5432/ecommerce_db')

def get_db():
    """Get database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize PostgreSQL database with tables and sample data"""
    conn = get_db()
    if not conn:
        print("❌ Could not connect to PostgreSQL database!")
        print("💡 Make sure PostgreSQL is running with the correct credentials:")
        print("   Username: ecommerce_user")
        print("   Password: password123")
        print("   Database: ecommerce_db")
        return False
        
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                category_id INTEGER REFERENCES categories(id),
                sku VARCHAR(50) UNIQUE NOT NULL,
                stock_quantity INTEGER DEFAULT 0,
                is_featured BOOLEAN DEFAULT FALSE,
                image_url VARCHAR(500) DEFAULT 'https://via.placeholder.com/300x300?text=Product',
                rating DECIMAL(3,2) DEFAULT 4.0,
                review_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create cart table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                product_id INTEGER NOT NULL REFERENCES products(id),
                quantity INTEGER DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                total_amount DECIMAL(10,2) NOT NULL,
                status VARCHAR(50) DEFAULT 'pending',
                payment_method VARCHAR(50),
                payment_status VARCHAR(50) DEFAULT 'pending',
                shipping_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(id),
                product_id INTEGER NOT NULL REFERENCES products(id),
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
        ''')
        
        # Create AI recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_recommendations (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                product_id INTEGER NOT NULL REFERENCES products(id),
                recommendation_type VARCHAR(50) NOT NULL,
                confidence_score DECIMAL(5,4) DEFAULT 0.0,
                reasoning TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
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
                ('Smartphone Pro Max', 'Latest flagship smartphone', 999.99, 1, 'PHONE-001', 50, True),
                ('Wireless Headphones', 'Premium noise-cancelling headphones', 299.99, 1, 'AUDIO-001', 25, True),
                ('Ultra-Slim Laptop', 'High-performance laptop', 1299.99, 1, 'LAPTOP-001', 15, True),
                ('Smart Watch', 'Advanced smartwatch', 399.99, 1, 'WATCH-001', 30, False),
                ('Organic Cotton T-Shirt', 'Comfortable organic cotton t-shirt', 29.99, 2, 'SHIRT-001', 100, False),
                ('Designer Jeans', 'Premium denim jeans', 89.99, 2, 'JEANS-001', 75, False),
                ('Running Shoes Pro', 'Professional running shoes', 149.99, 2, 'SHOES-001', 60, True),
                ('Programming Book', 'Learn modern programming', 49.99, 3, 'BOOK-001', 40, False),
                ('AI Guide', 'Complete AI guide', 59.99, 3, 'BOOK-002', 35, False),
                ('Garden Tools Set', 'Professional gardening tools', 129.99, 4, 'GARDEN-001', 20, False)
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
                ('johndoe', 'john@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'John', 'Doe'),
                ('janesmit', 'jane@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'Jane', 'Smith')
            ]
            
            cursor.executemany('''
                INSERT INTO users 
                (username, email, password_hash, first_name, last_name) 
                VALUES (%s, %s, %s, %s, %s)
            ''', users)
        
        conn.commit()
        print("✅ PostgreSQL database initialized successfully!")
        print(f"🔗 Connected to: {DATABASE_URL}")
        print("👤 Username: ecommerce_user")
        print("🗄️ Database: ecommerce_db")
        return True
        
    except Exception as e:
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
            'database': 'PostgreSQL',
            'message': 'Connected successfully'
        })
    else:
        return jsonify({
            'status': 'DOWN',
            'database': 'PostgreSQL',
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
        
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
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
                'user': dict(user)
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute('''
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id 
            ORDER BY p.created_at DESC
        ''')
        products = cursor.fetchall()
        
        return jsonify({
            'products': [dict(product) for product in products]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/products/featured', methods=['GET'])
def get_featured_products():
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
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
            'featured_products': [dict(product) for product in products]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/categories', methods=['GET'])
def get_categories():
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute('SELECT * FROM categories ORDER BY name')
        categories = cursor.fetchall()
        
        return jsonify({
            'categories': [dict(category) for category in categories]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("🚀 Starting ANUFA E-commerce API with PostgreSQL...")
    print("="*50)
    
    if init_db():
        print("✅ Database ready!")
        print("🌐 API starting on http://localhost:8080")
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        print("❌ Failed to initialize database. Please check your PostgreSQL setup.")
        print("\n💡 To fix this:")
        print("1. Make sure PostgreSQL is running")
        print("2. Run: docker-compose up postgres")
        print("3. Or install PostgreSQL locally with:")
        print("   - Username: ecommerce_user")
        print("   - Password: password123")
        print("   - Database: ecommerce_db")
