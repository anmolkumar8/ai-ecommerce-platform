#!/usr/bin/env python3
"""
ANUFA PostgreSQL Database Manager
Tool to manage your PostgreSQL database with username/password
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
import json
from datetime import datetime

# Database connection details (your username/password!)
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'ecommerce_db',
    'user': 'ecommerce_user',  # Your username!
    'password': 'password123', # Your password!
    'port': 5432
}

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

class PostgreSQLManager:
    def __init__(self):
        self.conn = None
        
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                host=DATABASE_CONFIG['host'],
                database=DATABASE_CONFIG['database'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                port=DATABASE_CONFIG['port']
            )
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print(f"💡 Make sure PostgreSQL is running with:")
            print(f"   🏠 Host: {DATABASE_CONFIG['host']}")
            print(f"   👤 Username: {DATABASE_CONFIG['user']}")
            print(f"   🔑 Password: {DATABASE_CONFIG['password']}")
            print(f"   🗄️ Database: {DATABASE_CONFIG['database']}")
            print(f"   📡 Port: {DATABASE_CONFIG['port']}")
            return False
    
    def disconnect(self):
        """Close connection"""
        if self.conn:
            self.conn.close()
    
    def view_all_tables(self):
        """Display all tables and their data"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        print("\n🗄️  ANUFA POSTGRESQL DATABASE")
        print("="*60)
        print(f"🔗 Connected to: {DATABASE_URL}")
        print(f"👤 Username: {DATABASE_CONFIG['user']}")
        print(f"🔑 Using password authentication")
        
        try:
            # Get all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = [row['table_name'] for row in cursor.fetchall()]
            
            print(f"📊 Tables: {', '.join(tables)}")
            
            for table_name in tables:
                print(f"\n📋 {table_name.upper()}")
                print("-" * 40)
                
                # Get table structure
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                
                print("Structure:")
                for col in columns:
                    nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                    default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
                    print(f"  • {col['column_name']} ({col['data_type']}) {nullable}{default}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()['count']
                print(f"Total rows: {count}")
                
                if count > 0 and count <= 10:
                    # Show data for small tables
                    cursor.execute(f"SELECT * FROM {table_name} ORDER BY id LIMIT 10;")
                    rows = cursor.fetchall()
                    
                    print("Data:")
                    for i, row in enumerate(rows, 1):
                        # Format long text fields
                        formatted_row = {}
                        for key, value in row.items():
                            if isinstance(value, str) and len(value) > 50:
                                formatted_row[key] = value[:50] + "..."
                            else:
                                formatted_row[key] = value
                        print(f"  {i}. {formatted_row}")
                        
        except Exception as e:
            print(f"❌ Error viewing tables: {e}")
        finally:
            cursor.close()
    
    def run_query(self, query):
        """Execute a custom SQL query"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                
                print(f"\n📊 Query Results ({len(results)} rows):")
                print("-" * 50)
                
                if results:
                    # Get column names
                    columns = list(results[0].keys())
                    print(f"Columns: {', '.join(columns)}")
                    
                    for i, row in enumerate(results, 1):
                        print(f"{i:3d}. {dict(row)}")
                        if i >= 20:  # Limit output
                            print(f"... and {len(results) - 20} more rows")
                            break
                else:
                    print("No results returned.")
            else:
                self.conn.commit()
                print("✅ Query executed successfully!")
                
        except Exception as e:
            print(f"❌ Query error: {e}")
            self.conn.rollback()
        finally:
            cursor.close()
    
    def export_data(self, filename=None):
        """Export all data to JSON"""
        if not filename:
            filename = f"postgres_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        export_data = {}
        
        try:
            # Get all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = [row['table_name'] for row in cursor.fetchall()]
            
            for table in tables:
                cursor.execute(f"SELECT * FROM {table} ORDER BY id;")
                rows = cursor.fetchall()
                export_data[table] = [dict(row) for row in rows]
            
            # Save to file
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            print(f"✅ Data exported to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Export error: {e}")
        finally:
            cursor.close()

def main():
    print("🐘 POSTGRESQL DATABASE MANAGER")
    print("="*50)
    
    db = PostgreSQLManager()
    
    if not db.connect():
        print("\n💡 To fix connection issues:")
        print("1. Start PostgreSQL with Docker:")
        print("   docker-compose up -d postgres")
        print("")
        print("2. Or install PostgreSQL locally and create:")
        print("   - Database: ecommerce_db")
        print("   - User: ecommerce_user (password: password123)")
        print("")
        print("3. Check if PostgreSQL is running:")
        print("   docker ps | grep postgres")
        return
    
    print("✅ Connected successfully!")
    
    while True:
        print("\n" + "="*60)
        print("🐘 POSTGRESQL DATABASE MANAGER")
        print("="*60)
        print("1. 📊 View all tables and data")
        print("2. 🔍 Run custom SQL query")
        print("3. 📤 Export data to JSON")
        print("4. 💾 Connection info")
        print("5. 🧪 Sample queries")
        print("0. ❌ Exit")
        
        choice = input("\nSelect option (0-5): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            db.view_all_tables()
        elif choice == '2':
            query = input("\nEnter SQL query: ").strip()
            if query:
                db.run_query(query)
        elif choice == '3':
            filename = input("Export filename (press Enter for auto): ").strip()
            db.export_data(filename if filename else None)
        elif choice == '4':
            print(f"\n🔗 Database URL: {DATABASE_URL}")
            print(f"🏠 Host: {DATABASE_CONFIG['host']}")
            print(f"📡 Port: {DATABASE_CONFIG['port']}")
            print(f"🗄️ Database: {DATABASE_CONFIG['database']}")
            print(f"👤 Username: {DATABASE_CONFIG['user']}")
            print(f"🔑 Password: {'*' * len(DATABASE_CONFIG['password'])}")
        elif choice == '5':
            print("\n🔍 Sample SQL Queries:")
            print("="*40)
            print("-- View all users")
            print("SELECT * FROM users;")
            print("")
            print("-- View products with categories")
            print("SELECT p.name, p.price, c.name as category")
            print("FROM products p")
            print("JOIN categories c ON p.category_id = c.id;")
            print("")
            print("-- View cart contents")
            print("SELECT u.username, p.name, c.quantity")
            print("FROM cart c")
            print("JOIN users u ON c.user_id = u.id")
            print("JOIN products p ON c.product_id = p.id;")
        else:
            print("❌ Invalid option!")
    
    db.disconnect()
    print("\n👋 Disconnected from PostgreSQL!")

if __name__ == "__main__":
    main()
