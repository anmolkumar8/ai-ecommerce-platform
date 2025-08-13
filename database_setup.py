#!/usr/bin/env python3
"""
ANUFA AI E-commerce Platform - Database Setup & Management
Complete database initialization and management tool
"""

import sqlite3
import os
import hashlib
import json
from datetime import datetime

# Database configuration
DATABASE_PATH = 'backend/java-api/ecommerce.db'

class DatabaseSetup:
    def __init__(self):
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to the database"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
            self.conn = sqlite3.connect(DATABASE_PATH)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def init_database(self):
        """Initialize complete database with all tables and sample data"""
        print("🚀 Initializing ANUFA AI E-commerce Database...")
        
        # Create all tables
        self._create_tables()
        
        # Insert sample data
        self._insert_sample_data()
        
        print("✅ Database initialized successfully!")
        self.show_summary()
    
    def _create_tables(self):
        """Create all required tables"""
        tables = [
            # Users table
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            
            # Categories table
            '''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            
            # Products table
            '''
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
            ''',
            
            # Cart table
            '''
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
            ''',
            
            # Orders table
            '''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                payment_method TEXT,
                payment_status TEXT DEFAULT 'pending',
                shipping_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''',
            
            # Order items table
            '''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
            ''',
            
            # AI Recommendations table
            '''
            CREATE TABLE IF NOT EXISTS ai_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER NOT NULL,
                recommendation_type TEXT NOT NULL,
                confidence_score REAL DEFAULT 0.0,
                reasoning TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
            '''
        ]
        
        for table_sql in tables:
            self.cursor.execute(table_sql)
        
        self.conn.commit()
        print("✅ All tables created successfully!")
    
    def _insert_sample_data(self):
        """Insert comprehensive sample data"""
        print("📦 Inserting sample data...")
        
        # Categories
        categories = [
            (1, 'Electronics', 'Electronic devices and gadgets'),
            (2, 'Clothing', 'Fashion and apparel'),
            (3, 'Books', 'Books and educational materials'),
            (4, 'Home & Garden', 'Home improvement supplies'),
            (5, 'Sports', 'Sports and fitness equipment')
        ]
        
        self.cursor.executemany('INSERT OR IGNORE INTO categories (id, name, description) VALUES (?, ?, ?)', categories)
        
        # Products
        products = [
            (1, 'Smartphone Pro Max', 'Latest flagship smartphone with AI-powered camera', 999.99, 1, 'PHONE-001', 50, 1),
            (2, 'Wireless Headphones', 'Premium noise-cancelling headphones', 299.99, 1, 'AUDIO-001', 25, 1),
            (3, 'Ultra-Slim Laptop', 'High-performance laptop for professionals', 1299.99, 1, 'LAPTOP-001', 15, 1),
            (4, 'Smart Watch', 'Advanced smartwatch with health monitoring', 399.99, 1, 'WATCH-001', 30, 0),
            (5, 'Organic Cotton T-Shirt', 'Comfortable organic cotton t-shirt', 29.99, 2, 'SHIRT-001', 100, 0),
            (6, 'Designer Jeans', 'Premium denim jeans with perfect fit', 89.99, 2, 'JEANS-001', 75, 0),
            (7, 'Running Shoes Pro', 'Professional running shoes', 149.99, 2, 'SHOES-001', 60, 1),
            (8, 'Programming Guide', 'Complete guide to modern programming', 49.99, 3, 'BOOK-001', 40, 0),
            (9, 'AI & ML Handbook', 'Comprehensive AI and Machine Learning guide', 59.99, 3, 'BOOK-002', 35, 0),
            (10, 'Garden Tools Set', 'Professional gardening tools set', 129.99, 4, 'GARDEN-001', 20, 0)
        ]
        
        self.cursor.executemany('''
            INSERT OR IGNORE INTO products 
            (id, name, description, price, category_id, sku, stock_quantity, is_featured) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)
        
        # Sample users (password: "password123")
        password_hash = hashlib.sha256('password123'.encode()).hexdigest()
        users = [
            (1, 'johndoe', 'john@example.com', password_hash, 'John', 'Doe'),
            (2, 'janesmit', 'jane@example.com', password_hash, 'Jane', 'Smith'),
            (3, 'bobwilson', 'bob@example.com', password_hash, 'Bob', 'Wilson')
        ]
        
        self.cursor.executemany('''
            INSERT OR IGNORE INTO users 
            (id, username, email, password_hash, first_name, last_name) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', users)
        
        # Sample cart items
        cart_items = [
            (1, 1, 2),  # John has 2 smartphones
            (1, 2, 1),  # John has 1 headphones
            (2, 3, 1),  # Jane has 1 laptop
        ]
        
        self.cursor.executemany(
            "INSERT OR IGNORE INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
            cart_items
        )
        
        # Sample orders
        orders = [
            (1, 1599.98, 'completed', 'credit_card', 'paid', '123 Main St, New York, NY'),
            (2, 1299.99, 'pending', 'paypal', 'pending', '456 Oak Ave, Los Angeles, CA'),
        ]
        
        for order in orders:
            self.cursor.execute("""
                INSERT OR IGNORE INTO orders 
                (user_id, total_amount, status, payment_method, payment_status, shipping_address) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, order)
        
        # Sample AI recommendations
        ai_recommendations = [
            (1, 4, 'similar_product', 0.85, 'Users who bought smartphones also liked smartwatches'),
            (1, 5, 'content_based', 0.72, 'Based on electronics preference'),
            (2, 6, 'collaborative', 0.90, 'Users with similar profiles liked this'),
            (3, 7, 'trending', 0.78, 'Currently trending in sports category'),
        ]
        
        self.cursor.executemany("""
            INSERT OR IGNORE INTO ai_recommendations 
            (user_id, product_id, recommendation_type, confidence_score, reasoning) 
            VALUES (?, ?, ?, ?, ?)
        """, ai_recommendations)
        
        self.conn.commit()
        print("✅ Sample data inserted successfully!")
    
    def show_summary(self):
        """Display database summary"""
        print("\n" + "="*60)
        print("🗄️  DATABASE SUMMARY")
        print("="*60)
        
        tables = ['users', 'categories', 'products', 'cart', 'orders', 'order_items', 'ai_recommendations']
        
        for table in tables:
            try:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = self.cursor.fetchone()[0]
                print(f"📊 {table.capitalize()}: {count} records")
            except:
                print(f"❌ {table.capitalize()}: Table not found")
        
        print(f"\n📁 Database location: {os.path.abspath(DATABASE_PATH)}")
        if os.path.exists(DATABASE_PATH):
            size = os.path.getsize(DATABASE_PATH)
            print(f"📏 Database size: {size:,} bytes ({size/1024:.1f} KB)")
    
    def view_data(self, table_name=None):
        """View data from specific table or all tables"""
        if table_name:
            tables = [table_name]
        else:
            tables = ['users', 'categories', 'products', 'cart', 'orders', 'ai_recommendations']
        
        for table in tables:
            try:
                print(f"\n📋 {table.upper()} TABLE")
                print("-" * 40)
                
                self.cursor.execute(f"SELECT * FROM {table} LIMIT 5")
                rows = self.cursor.fetchall()
                
                if rows:
                    # Get column names
                    self.cursor.execute(f"PRAGMA table_info({table})")
                    columns = [col[1] for col in self.cursor.fetchall()]
                    
                    for i, row in enumerate(rows, 1):
                        data = dict(zip(columns, row))
                        print(f"{i}. {data}")
                else:
                    print("No data found")
                    
            except Exception as e:
                print(f"❌ Error viewing {table}: {e}")
    
    def reset_database(self):
        """Reset database by dropping all tables and recreating"""
        print("🔄 Resetting database...")
        
        tables = ['ai_recommendations', 'order_items', 'orders', 'cart', 'products', 'categories', 'users']
        
        for table in tables:
            try:
                self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
            except:
                pass
        
        self.conn.commit()
        print("✅ Database reset complete!")
        
        # Reinitialize
        self.init_database()

def main():
    print("🚀 ANUFA AI E-commerce Platform - Database Setup")
    print("="*60)
    
    db = DatabaseSetup()
    
    if not db.connect():
        return
    
    while True:
        print("\n" + "="*40)
        print("DATABASE MANAGEMENT OPTIONS")
        print("="*40)
        print("1. 🔧 Initialize/Setup Database")
        print("2. 📊 View Database Summary") 
        print("3. 👀 View All Data")
        print("4. 🔍 View Specific Table")
        print("5. 🔄 Reset Database")
        print("0. ❌ Exit")
        
        choice = input("\nSelect option (0-5): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            db.init_database()
        elif choice == '2':
            db.show_summary()
        elif choice == '3':
            db.view_data()
        elif choice == '4':
            table = input("Enter table name: ").strip().lower()
            if table:
                db.view_data(table)
        elif choice == '5':
            confirm = input("⚠️  Reset database? This will delete ALL data! (yes/no): ").strip().lower()
            if confirm == 'yes':
                db.reset_database()
            else:
                print("❌ Reset cancelled")
        else:
            print("❌ Invalid option!")
    
    db.disconnect()
    print("\n👋 Database management closed!")

if __name__ == "__main__":
    main()
