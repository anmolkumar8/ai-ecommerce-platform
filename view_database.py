#!/usr/bin/env python3
"""
Database Viewer for ANUFA E-commerce Platform
View tables and data in the SQLite database
"""

import sqlite3
import os
from datetime import datetime

# Database path
DATABASE_PATH = 'backend/java-api/ecommerce.db'

def view_database():
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Database file not found: {DATABASE_PATH}")
        return
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        print("🗄️  ANUFA E-COMMERCE DATABASE VIEWER")
        print("="*50)
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📊 Found {len(tables)} tables:")
        for table in tables:
            print(f"  • {table[0]}")
        
        print("\n" + "="*50)
        
        # Display data from each table
        for table_name in [t[0] for t in tables]:
            print(f"\n📋 TABLE: {table_name.upper()}")
            print("-" * 30)
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            print("Columns:", ", ".join(column_names))
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"Total rows: {count}")
            
            if count > 0:
                # Show sample data (first 5 rows)
                limit = min(5, count)
                cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
                rows = cursor.fetchall()
                
                print(f"\nSample data (showing {limit} rows):")
                for i, row in enumerate(rows, 1):
                    print(f"  Row {i}: {dict(zip(column_names, row))}")
            
            print()
        
        # Show some useful queries
        print("\n🔍 USEFUL QUERIES:")
        print("-" * 30)
        
        # Users count
        try:
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            print(f"👥 Total Users: {user_count}")
        except:
            pass
            
        # Products count
        try:
            cursor.execute("SELECT COUNT(*) FROM products;")
            product_count = cursor.fetchone()[0]
            print(f"📦 Total Products: {product_count}")
        except:
            pass
            
        # Featured products
        try:
            cursor.execute("SELECT COUNT(*) FROM products WHERE is_featured = 1;")
            featured_count = cursor.fetchone()[0]
            print(f"⭐ Featured Products: {featured_count}")
        except:
            pass
            
        # Cart items
        try:
            cursor.execute("SELECT COUNT(*) FROM cart;")
            cart_count = cursor.fetchone()[0]
            print(f"🛒 Cart Items: {cart_count}")
        except:
            pass
            
        # Orders
        try:
            cursor.execute("SELECT COUNT(*) FROM orders;")
            order_count = cursor.fetchone()[0]
            print(f"📋 Total Orders: {order_count}")
        except:
            pass
            
        conn.close()
        print(f"\n✅ Database viewed successfully!")
        print(f"📁 Database file: {os.path.abspath(DATABASE_PATH)}")
        
    except Exception as e:
        print(f"❌ Error viewing database: {e}")

def run_custom_query():
    """Run a custom SQL query"""
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Database file not found: {DATABASE_PATH}")
        return
        
    print("\n🔍 CUSTOM QUERY MODE")
    print("="*30)
    print("Enter SQL queries (type 'exit' to quit):")
    print("Examples:")
    print("  SELECT * FROM users;")
    print("  SELECT name, price FROM products WHERE is_featured = 1;")
    print("  SELECT * FROM cart;")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    while True:
        query = input("\nSQL> ").strip()
        
        if query.lower() == 'exit':
            break
            
        if not query:
            continue
            
        try:
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                
                # Get column names
                column_names = [description[0] for description in cursor.description]
                print(f"\nColumns: {', '.join(column_names)}")
                print(f"Results ({len(results)} rows):")
                
                for i, row in enumerate(results, 1):
                    print(f"  {i}: {dict(zip(column_names, row))}")
                    if i >= 10:  # Limit display to 10 rows
                        print(f"  ... and {len(results) - 10} more rows")
                        break
            else:
                conn.commit()
                print("✅ Query executed successfully!")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "query":
        run_custom_query()
    else:
        view_database()
        print("\n💡 Tip: Run 'python view_database.py query' for interactive query mode!")
