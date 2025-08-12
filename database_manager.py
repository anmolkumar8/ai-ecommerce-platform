#!/usr/bin/env python3
"""
ANUFA E-commerce Database Manager
Complete tool to manage, view, and interact with your database
"""

import sqlite3
import os
import json
from datetime import datetime
import hashlib

DATABASE_PATH = 'backend/java-api/ecommerce.db'

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to the database"""
        try:
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
    
    def create_missing_tables(self):
        """Create any missing tables"""
        print("🔧 Creating missing tables...")
        
        tables = [
            # Cart table
            """
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
            """,
            
            # Orders table
            """
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
            """,
            
            # Order items table
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
            """,
            
            # AI Recommendations table
            """
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
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
                self.conn.commit()
            except Exception as e:
                print(f"Warning: {e}")
        
        print("✅ Tables checked/created successfully!")
    
    def view_all_tables(self):
        """Display all tables and their data"""
        print("\n🗄️  ANUFA DATABASE OVERVIEW")
        print("="*60)
        
        # Get all tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in self.cursor.fetchall() if not t[0].startswith('sqlite_')]
        
        print(f"📊 Tables: {', '.join(tables)}")
        
        for table_name in tables:
            print(f"\n📋 {table_name.upper()}")
            print("-" * 40)
            
            # Get table structure
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [(col[1], col[2]) for col in self.cursor.fetchall()]
            
            print("Structure:")
            for col_name, col_type in columns:
                print(f"  • {col_name} ({col_type})")
            
            # Get row count
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = self.cursor.fetchone()[0]
            print(f"Total rows: {count}")
            
            if count > 0 and count <= 10:
                # Show all data for small tables
                column_names = [col[0] for col in columns]
                self.cursor.execute(f"SELECT * FROM {table_name};")
                rows = self.cursor.fetchall()
                
                print("Data:")
                for i, row in enumerate(rows, 1):
                    data = dict(zip(column_names, row))
                    # Format the output nicely
                    formatted_data = {}
                    for k, v in data.items():
                        if isinstance(v, str) and len(v) > 50:
                            formatted_data[k] = v[:50] + "..."
                        else:
                            formatted_data[k] = v
                    print(f"  {i}. {formatted_data}")
    
    def add_sample_data(self):
        """Add sample cart items and orders for testing"""
        print("🧪 Adding sample test data...")
        
        try:
            # Add sample cart items
            cart_items = [
                (1, 1, 2),  # User 1, Product 1, Quantity 2
                (1, 2, 1),  # User 1, Product 2, Quantity 1
                (2, 3, 1),  # User 2, Product 3, Quantity 1
            ]
            
            self.cursor.executemany(
                "INSERT OR IGNORE INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                cart_items
            )
            
            # Add sample orders
            orders = [
                (1, 1599.98, 'completed', 'credit_card', 'paid', '123 Main St, City, Country'),
                (2, 1299.99, 'pending', 'paypal', 'pending', '456 Oak Ave, Town, Country'),
            ]
            
            for order in orders:
                self.cursor.execute("""
                    INSERT OR IGNORE INTO orders 
                    (user_id, total_amount, status, payment_method, payment_status, shipping_address) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, order)
            
            # Add sample AI recommendations
            ai_recs = [
                (1, 4, 'similar_product', 0.85, 'Users who bought smartphones also liked smartwatches'),
                (1, 5, 'content_based', 0.72, 'Based on electronics preference'),
                (2, 6, 'collaborative', 0.90, 'Users with similar profiles liked this'),
            ]
            
            self.cursor.executemany("""
                INSERT OR IGNORE INTO ai_recommendations 
                (user_id, product_id, recommendation_type, confidence_score, reasoning) 
                VALUES (?, ?, ?, ?, ?)
            """, ai_recs)
            
            self.conn.commit()
            print("✅ Sample data added successfully!")
            
        except Exception as e:
            print(f"❌ Error adding sample data: {e}")
    
    def run_query(self, query):
        """Execute a custom SQL query"""
        try:
            self.cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                
                print(f"\n📊 Query Results ({len(results)} rows):")
                print(f"Columns: {', '.join(columns)}")
                print("-" * 50)
                
                for i, row in enumerate(results, 1):
                    print(f"{i:3d}. {dict(zip(columns, row))}")
                    if i >= 20:  # Limit output
                        print(f"... and {len(results) - 20} more rows")
                        break
            else:
                self.conn.commit()
                print("✅ Query executed successfully!")
                
        except Exception as e:
            print(f"❌ Query error: {e}")
    
    def export_data(self, filename=None):
        """Export all data to JSON"""
        if not filename:
            filename = f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {}
        
        # Get all tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in self.cursor.fetchall() if not t[0].startswith('sqlite_')]
        
        for table in tables:
            # Get column names
            self.cursor.execute(f"PRAGMA table_info({table});")
            columns = [col[1] for col in self.cursor.fetchall()]
            
            # Get data
            self.cursor.execute(f"SELECT * FROM {table};")
            rows = self.cursor.fetchall()
            
            # Convert to list of dictionaries
            export_data[table] = [dict(zip(columns, row)) for row in rows]
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"✅ Data exported to: {filename}")
        return filename

def main():
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Database not found: {DATABASE_PATH}")
        print("💡 Make sure to run the backend server first to create the database!")
        return
    
    db = DatabaseManager()
    
    if not db.connect():
        return
    
    while True:
        print("\n" + "="*60)
        print("🗄️  ANUFA DATABASE MANAGER")
        print("="*60)
        print("1. 📊 View all tables and data")
        print("2. 🔧 Create missing tables")
        print("3. 🧪 Add sample test data")
        print("4. 🔍 Run custom SQL query")
        print("5. 📤 Export data to JSON")
        print("6. 💾 Database info")
        print("0. ❌ Exit")
        
        choice = input("\nSelect option (0-6): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            db.view_all_tables()
        elif choice == '2':
            db.create_missing_tables()
        elif choice == '3':
            db.add_sample_data()
        elif choice == '4':
            query = input("\nEnter SQL query: ").strip()
            if query:
                db.run_query(query)
        elif choice == '5':
            filename = input("Export filename (press Enter for auto): ").strip()
            db.export_data(filename if filename else None)
        elif choice == '6':
            size = os.path.getsize(DATABASE_PATH)
            print(f"\n📁 Database file: {os.path.abspath(DATABASE_PATH)}")
            print(f"📏 File size: {size:,} bytes ({size/1024:.1f} KB)")
            print(f"🕒 Last modified: {datetime.fromtimestamp(os.path.getmtime(DATABASE_PATH))}")
        else:
            print("❌ Invalid option!")
    
    db.disconnect()
    print("\n👋 Database manager closed!")

if __name__ == "__main__":
    main()
