#!/usr/bin/env python3
"""
Setup MySQL Database for ANUFA E-commerce
Initialize tables and sample data with your credentials
"""

import mysql.connector
from mysql.connector import Error
import hashlib

# Your MySQL credentials
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'ecommerce_db',
    'user': 'root',          # Your username
    'password': 'Anmol@123', # Your password
    'port': 3306
}

def setup_database():
    """Setup complete database with tables and sample data"""
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        print("✅ Connected to MySQL successfully!")
        print(f"🗄️ Database: {DATABASE_CONFIG['database']}")
        print(f"👤 User: {DATABASE_CONFIG['user']}")
        
        # Drop existing tables to start fresh (optional)
        print("\n🧹 Cleaning existing tables...")
        tables_to_drop = ['order_items', 'orders', 'cart', 'products', 'categories', 'users']
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"   Dropped {table}")
            except Error as e:
                print(f"   Warning dropping {table}: {e}")
        
        print("\n🏗️ Creating tables...")
        
        # Create users table
        cursor.execute('''
            CREATE TABLE users (
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
        print("   ✅ Users table created")
        
        # Create categories table
        cursor.execute('''
            CREATE TABLE categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        print("   ✅ Categories table created")
        
        # Create products table
        cursor.execute('''
            CREATE TABLE products (
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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        print("   ✅ Products table created")
        
        # Create cart table
        cursor.execute('''
            CREATE TABLE cart (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        print("   ✅ Cart table created")
        
        # Create orders table
        cursor.execute('''
            CREATE TABLE orders (
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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        print("   ✅ Orders table created")
        
        # Create order items table
        cursor.execute('''
            CREATE TABLE order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                product_name VARCHAR(200) NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                total_price DECIMAL(10,2) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        print("   ✅ Order items table created")
        
        print("\n📊 Inserting sample data...")
        
        # Insert categories
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
        print(f"   ✅ Inserted {len(categories)} categories")
        
        # Insert products
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
        print(f"   ✅ Inserted {len(products)} products")
        
        # Insert users
        users = [
            ('johndoe', 'john@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'John', 'Doe', '9876543210'),
            ('janesmit', 'jane@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'Jane', 'Smith', '9876543211'),
            ('anmolkumar', 'anmol@example.com', hashlib.sha256('Anmol@123'.encode()).hexdigest(), 'Anmol', 'Kumar', '9876543212'),
            ('rajeshgupta', 'rajesh@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'Rajesh', 'Gupta', '9876543213'),
            ('priyasharma', 'priya@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'Priya', 'Sharma', '9876543214')
        ]
        
        cursor.executemany('''
            INSERT INTO users 
            (username, email, password_hash, first_name, last_name, phone) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', users)
        print(f"   ✅ Inserted {len(users)} users")
        
        # Insert sample orders
        orders = [
            (1, 'ORD-20250101-001', 101499.98, 'completed', 'credit_card', 'paid', 
             '123 Main St, New Delhi, India - 110001', '123 Main St, New Delhi, India - 110001'),
            (2, 'ORD-20250102-001', 107999.99, 'shipped', 'upi', 'paid', 
             '456 Oak Ave, Mumbai, India - 400001', '456 Oak Ave, Mumbai, India - 400001'),
            (3, 'ORD-20250103-001', 33499.97, 'pending', 'debit_card', 'pending', 
             '789 Pine Rd, Bangalore, India - 560001', '789 Pine Rd, Bangalore, India - 560001'),
            (4, 'ORD-20250104-001', 27299.98, 'completed', 'net_banking', 'paid',
             '321 Cedar St, Chennai, India - 600001', '321 Cedar St, Chennai, India - 600001'),
            (5, 'ORD-20250105-001', 12999.99, 'shipped', 'upi', 'paid',
             '654 Birch Ave, Hyderabad, India - 500001', '654 Birch Ave, Hyderabad, India - 500001')
        ]
        
        cursor.executemany('''
            INSERT INTO orders 
            (user_id, order_number, total_amount, status, payment_method, payment_status, shipping_address, billing_address) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', orders)
        print(f"   ✅ Inserted {len(orders)} orders")
        
        # Insert order items
        order_items = [
            # Order 1 (John Doe) - Smartphone + Headphones
            (1, 1, 'Smartphone Pro Max', 1, 84999.99, 84999.99),
            (1, 2, 'Wireless Headphones', 1, 16500.99, 16500.99),
            
            # Order 2 (Jane Smith) - Laptop
            (2, 3, 'Ultra-Slim Laptop', 1, 107999.99, 107999.99),
            
            # Order 3 (Anmol Kumar) - Watch + Shoes
            (3, 4, 'Smart Watch', 1, 24999.99, 24999.99),
            (3, 7, 'Running Shoes Pro', 1, 8999.99, 8999.99),
            
            # Order 4 (Rajesh Gupta) - T-Shirt + Jeans + Books
            (4, 5, 'Organic Cotton T-Shirt', 2, 1299.99, 2599.98),
            (4, 6, 'Designer Jeans', 1, 4599.99, 4599.99),
            (4, 8, 'Programming Guide', 8, 2499.99, 19999.92),
            
            # Order 5 (Priya Sharma) - AI Book + Garden Tools
            (5, 9, 'AI & Machine Learning', 2, 2999.99, 5999.98),
            (5, 10, 'Garden Tools Set', 1, 6499.99, 6499.99)
        ]
        
        cursor.executemany('''
            INSERT INTO order_items 
            (order_id, product_id, product_name, quantity, unit_price, total_price) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', order_items)
        print(f"   ✅ Inserted {len(order_items)} order items")
        
        # Insert sample cart items
        cart_items = [
            (1, 4, 1),  # John has Smart Watch in cart
            (2, 7, 2),  # Jane has 2 Running Shoes in cart
            (3, 8, 1),  # Anmol has Programming Guide in cart
        ]
        
        cursor.executemany(
            'INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)',
            cart_items
        )
        print(f"   ✅ Inserted {len(cart_items)} cart items")
        
        # Commit all changes
        conn.commit()
        print("\n🎉 Database setup completed successfully!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        orders_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(total_amount) FROM orders")
        total_revenue = cursor.fetchone()[0] or 0
        
        print(f"\n📊 Database Summary:")
        print(f"   👥 Users: {users_count}")
        print(f"   📦 Products: {products_count}")
        print(f"   📋 Orders: {orders_count}")
        print(f"   💰 Total Revenue: ₹{total_revenue:,.2f}")
        
        print(f"\n✅ Ready to use MySQL database with your credentials!")
        print(f"   🗄️ Database: {DATABASE_CONFIG['database']}")
        print(f"   👤 Username: {DATABASE_CONFIG['user']}")
        print(f"   🔑 Password: {DATABASE_CONFIG['password']}")
        
    except Error as e:
        print(f"❌ Database setup error: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    
    return True

if __name__ == "__main__":
    print("🗄️  ANUFA MYSQL DATABASE SETUP")
    print("="*50)
    
    if setup_database():
        print(f"\n🚀 Next steps:")
        print(f"1. Run the database viewer: python mysql_db_viewer.py")
        print(f"2. Start the MySQL backend: python backend/java-api/app_mysql.py")
        print(f"3. View data in MySQL Workbench with your credentials")
    else:
        print(f"\n💡 Please check:")
        print(f"1. MySQL server is running")
        print(f"2. Database 'ecommerce_db' exists in MySQL Workbench")
        print(f"3. User 'root' has proper permissions")
        print(f"4. Password 'Anmol@123' is correct")
