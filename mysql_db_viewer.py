#!/usr/bin/env python3
"""
ANUFA MySQL Database Viewer
View users, their accounts, and order history in table format
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tabulate import tabulate
import json

# Your MySQL credentials
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'ecommerce_db',
    'user': 'root',          # Your username
    'password': 'Anmol@123', # Your password
    'port': 3306
}

class MySQLViewer:
    def __init__(self):
        self.conn = None
        
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.conn = mysql.connector.connect(**DATABASE_CONFIG)
            return True
        except Error as e:
            print(f"❌ Connection failed: {e}")
            print(f"💡 Make sure MySQL is running with:")
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
    
    def show_users_and_orders(self):
        """Show all users who created accounts and their order history"""
        cursor = self.conn.cursor(dictionary=True)
        
        print("\n" + "="*100)
        print("👥 USERS WHO CREATED ACCOUNTS AND THEIR ORDERS")
        print("="*100)
        
        try:
            # Get all users with their order summary
            query = """
            SELECT 
                u.id,
                u.username,
                u.email,
                u.first_name,
                u.last_name,
                u.phone,
                u.created_at as account_created,
                COUNT(DISTINCT o.id) as total_orders,
                COALESCE(SUM(o.total_amount), 0) as total_spent,
                MAX(o.created_at) as last_order_date
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id, u.username, u.email, u.first_name, u.last_name, u.phone, u.created_at
            ORDER BY u.created_at DESC
            """
            
            cursor.execute(query)
            users = cursor.fetchall()
            
            if not users:
                print("❌ No users found in database!")
                return
            
            # Prepare data for table
            table_data = []
            for user in users:
                table_data.append([
                    user['id'],
                    user['username'],
                    f"{user['first_name']} {user['last_name']}",
                    user['email'],
                    user['phone'] or 'N/A',
                    user['account_created'].strftime('%Y-%m-%d'),
                    user['total_orders'],
                    f"₹{user['total_spent']:,.2f}",
                    user['last_order_date'].strftime('%Y-%m-%d') if user['last_order_date'] else 'No orders'
                ])
            
            headers = ['ID', 'Username', 'Full Name', 'Email', 'Phone', 'Joined', 'Orders', 'Total Spent', 'Last Order']
            
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
            
            print(f"\n📊 Summary:")
            print(f"   👥 Total Users: {len(users)}")
            total_users_with_orders = sum(1 for user in users if user['total_orders'] > 0)
            print(f"   🛒 Users with Orders: {total_users_with_orders}")
            total_revenue = sum(user['total_spent'] for user in users)
            print(f"   💰 Total Revenue: ₹{total_revenue:,.2f}")
            
        except Error as e:
            print(f"❌ Error fetching data: {e}")
        finally:
            cursor.close()
    
    def show_detailed_orders(self):
        """Show detailed order information with items"""
        cursor = self.conn.cursor(dictionary=True)
        
        print("\n" + "="*120)
        print("📋 DETAILED ORDER HISTORY")
        print("="*120)
        
        try:
            query = """
            SELECT 
                o.id as order_id,
                o.order_number,
                u.username,
                u.first_name,
                u.last_name,
                u.email,
                o.total_amount,
                o.status,
                o.payment_method,
                o.payment_status,
                o.created_at as order_date,
                GROUP_CONCAT(
                    CONCAT(oi.product_name, ' (Qty: ', oi.quantity, ', ₹', oi.unit_price, ')')
                    SEPARATOR '; '
                ) as items
            FROM orders o
            JOIN users u ON o.user_id = u.id
            LEFT JOIN order_items oi ON o.id = oi.order_id
            GROUP BY o.id, o.order_number, u.username, u.first_name, u.last_name, u.email, 
                     o.total_amount, o.status, o.payment_method, o.payment_status, o.created_at
            ORDER BY o.created_at DESC
            """
            
            cursor.execute(query)
            orders = cursor.fetchall()
            
            if not orders:
                print("❌ No orders found in database!")
                return
            
            # Prepare data for table
            table_data = []
            for order in orders:
                table_data.append([
                    order['order_number'],
                    order['username'],
                    f"{order['first_name']} {order['last_name']}",
                    f"₹{order['total_amount']:,.2f}",
                    order['status'].upper(),
                    order['payment_method'].upper(),
                    order['payment_status'].upper(),
                    order['order_date'].strftime('%Y-%m-%d %H:%M'),
                    order['items'][:80] + '...' if len(order['items']) > 80 else order['items']
                ])
            
            headers = ['Order #', 'Customer', 'Name', 'Amount', 'Status', 'Payment', 'Pay Status', 'Date', 'Items']
            
            print(tabulate(table_data, headers=headers, tablefmt='grid', maxcolwidths=[12, 12, 15, 12, 10, 12, 10, 16, 80]))
            
            print(f"\n📊 Order Summary:")
            print(f"   📋 Total Orders: {len(orders)}")
            total_revenue = sum(order['total_amount'] for order in orders)
            print(f"   💰 Total Revenue: ₹{total_revenue:,.2f}")
            
            # Status breakdown
            status_count = {}
            for order in orders:
                status = order['status']
                status_count[status] = status_count.get(status, 0) + 1
            
            print(f"   📈 Order Status Breakdown:")
            for status, count in status_count.items():
                print(f"      • {status.capitalize()}: {count}")
                
        except Error as e:
            print(f"❌ Error fetching orders: {e}")
        finally:
            cursor.close()
    
    def show_popular_products(self):
        """Show most popular products by order frequency"""
        cursor = self.conn.cursor(dictionary=True)
        
        print("\n" + "="*80)
        print("🔥 MOST POPULAR PRODUCTS")
        print("="*80)
        
        try:
            query = """
            SELECT 
                p.name as product_name,
                p.price,
                COUNT(oi.id) as times_ordered,
                SUM(oi.quantity) as total_quantity,
                SUM(oi.total_price) as total_revenue
            FROM products p
            JOIN order_items oi ON p.id = oi.product_id
            GROUP BY p.id, p.name, p.price
            ORDER BY times_ordered DESC, total_quantity DESC
            LIMIT 10
            """
            
            cursor.execute(query)
            products = cursor.fetchall()
            
            if not products:
                print("❌ No product orders found!")
                return
            
            # Prepare data for table
            table_data = []
            for i, product in enumerate(products, 1):
                table_data.append([
                    i,
                    product['product_name'],
                    f"₹{product['price']:,.2f}",
                    product['times_ordered'],
                    product['total_quantity'],
                    f"₹{product['total_revenue']:,.2f}"
                ])
            
            headers = ['Rank', 'Product Name', 'Price', 'Orders', 'Qty Sold', 'Revenue']
            
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
            
        except Error as e:
            print(f"❌ Error fetching products: {e}")
        finally:
            cursor.close()
    
    def show_all_tables(self):
        """Show all database tables with data"""
        cursor = self.conn.cursor(dictionary=True)
        
        print("\n" + "="*80)
        print("🗄️  DATABASE TABLES OVERVIEW")
        print("="*80)
        
        try:
            # Get all tables
            cursor.execute("SHOW TABLES")
            tables = [row[f'Tables_in_{DATABASE_CONFIG["database"]}'] for row in cursor.fetchall()]
            
            for table_name in tables:
                print(f"\n📋 {table_name.upper()} TABLE")
                print("-" * 50)
                
                # Get table structure
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                
                print("Structure:")
                for col in columns:
                    null_info = "NULL" if col['Null'] == 'YES' else "NOT NULL"
                    key_info = f" [{col['Key']}]" if col['Key'] else ""
                    default_info = f" DEFAULT {col['Default']}" if col['Default'] else ""
                    print(f"  • {col['Field']} ({col['Type']}) {null_info}{key_info}{default_info}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = cursor.fetchone()['count']
                print(f"Total rows: {count}")
                
                if count > 0 and count <= 5:
                    # Show sample data for small tables
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                    rows = cursor.fetchall()
                    
                    if rows:
                        print("\nSample data:")
                        headers = list(rows[0].keys())
                        table_data = []
                        for row in rows:
                            formatted_row = []
                            for key, value in row.items():
                                if isinstance(value, str) and len(value) > 30:
                                    formatted_row.append(value[:30] + "...")
                                elif value is None:
                                    formatted_row.append("NULL")
                                else:
                                    formatted_row.append(str(value))
                            table_data.append(formatted_row)
                        
                        print(tabulate(table_data, headers=headers, tablefmt='grid', maxcolwidths=25))
                        
        except Error as e:
            print(f"❌ Error viewing tables: {e}")
        finally:
            cursor.close()

def main():
    print("🗄️  ANUFA MYSQL DATABASE VIEWER")
    print("="*60)
    print(f"🔗 Host: {DATABASE_CONFIG['host']}")
    print(f"👤 Username: {DATABASE_CONFIG['user']}")
    print(f"🗄️ Database: {DATABASE_CONFIG['database']}")
    
    db = MySQLViewer()
    
    if not db.connect():
        print("\n💡 To fix connection issues:")
        print("1. Make sure MySQL is running")
        print("2. Check MySQL Workbench connection")
        print("3. Verify database 'ecommerce_db' exists")
        print("4. Ensure user 'root' can connect")
        return
    
    print("✅ Connected successfully!")
    
    while True:
        print("\n" + "="*60)
        print("🗄️  MYSQL DATABASE VIEWER MENU")
        print("="*60)
        print("1. 👥 Show Users & Their Order Summary")
        print("2. 📋 Show Detailed Order History")
        print("3. 🔥 Show Popular Products")
        print("4. 🗂️  Show All Database Tables")
        print("5. 📊 Quick Database Stats")
        print("0. ❌ Exit")
        
        choice = input("\nSelect option (0-5): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            db.show_users_and_orders()
        elif choice == '2':
            db.show_detailed_orders()
        elif choice == '3':
            db.show_popular_products()
        elif choice == '4':
            db.show_all_tables()
        elif choice == '5':
            show_quick_stats(db)
        else:
            print("❌ Invalid option!")
    
    db.disconnect()
    print("\n👋 Disconnected from MySQL!")

def show_quick_stats(db):
    """Show quick database statistics"""
    cursor = db.conn.cursor(dictionary=True)
    
    print("\n📊 QUICK DATABASE STATISTICS")
    print("="*50)
    
    try:
        # Users count
        cursor.execute("SELECT COUNT(*) as count FROM users")
        users_count = cursor.fetchone()['count']
        
        # Products count
        cursor.execute("SELECT COUNT(*) as count FROM products")
        products_count = cursor.fetchone()['count']
        
        # Orders count and total revenue
        cursor.execute("SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as revenue FROM orders")
        orders_data = cursor.fetchone()
        
        # Cart items count
        cursor.execute("SELECT COUNT(*) as count FROM cart")
        cart_count = cursor.fetchone()['count']
        
        print(f"👥 Total Users: {users_count}")
        print(f"📦 Total Products: {products_count}")
        print(f"📋 Total Orders: {orders_data['count']}")
        print(f"💰 Total Revenue: ₹{orders_data['revenue']:,.2f}")
        print(f"🛒 Items in Cart: {cart_count}")
        
        # Latest user
        cursor.execute("SELECT username, created_at FROM users ORDER BY created_at DESC LIMIT 1")
        latest_user = cursor.fetchone()
        if latest_user:
            print(f"👤 Latest User: {latest_user['username']} ({latest_user['created_at'].strftime('%Y-%m-%d')})")
        
        # Latest order
        cursor.execute("SELECT order_number, created_at FROM orders ORDER BY created_at DESC LIMIT 1")
        latest_order = cursor.fetchone()
        if latest_order:
            print(f"📋 Latest Order: {latest_order['order_number']} ({latest_order['created_at'].strftime('%Y-%m-%d')})")
            
    except Error as e:
        print(f"❌ Error fetching stats: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    # Install required package if not present
    try:
        import tabulate
    except ImportError:
        print("📦 Installing required package...")
        import subprocess
        subprocess.check_call(["pip", "install", "tabulate"])
        import tabulate
    
    main()
