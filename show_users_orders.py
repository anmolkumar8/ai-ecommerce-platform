#!/usr/bin/env python3
"""
Show Users and Their Orders in Table Format
"""

import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

# Your MySQL credentials  
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'ecommerce_db', 
    'user': 'root',
    'password': 'Anmol@123',
    'port': 3306
}

def show_users_and_orders():
    """Show all users who created accounts and their order history"""
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print('\n' + '='*100)
        print('👥 USERS WHO CREATED ACCOUNTS AND THEIR ORDERS')
        print('='*100)
        
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
        
        # Prepare data for table
        table_data = []
        for user in users:
            total_spent = float(user['total_spent'])
            table_data.append([
                user['id'],
                user['username'],
                f"{user['first_name']} {user['last_name']}",
                user['email'],
                user['phone'] or 'N/A',
                user['account_created'].strftime('%Y-%m-%d'),
                user['total_orders'],
                f"₹{total_spent:,.2f}",
                user['last_order_date'].strftime('%Y-%m-%d') if user['last_order_date'] else 'No orders'
            ])
        
        headers = ['ID', 'Username', 'Full Name', 'Email', 'Phone', 'Joined', 'Orders', 'Total Spent', 'Last Order']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        
        print(f'\n📊 Summary:')
        print(f'   👥 Total Users: {len(users)}')
        total_users_with_orders = sum(1 for user in users if user['total_orders'] > 0)
        print(f'   🛒 Users with Orders: {total_users_with_orders}')
        total_revenue = sum(float(user['total_spent']) for user in users)
        print(f'   💰 Total Revenue: ₹{total_revenue:,.2f}')
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f'❌ Error: {e}')

def show_detailed_orders():
    """Show detailed order information"""
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print('\n' + '='*120)
        print('📋 DETAILED ORDER HISTORY')
        print('='*120)
        
        query = """
        SELECT 
            o.id as order_id,
            o.order_number,
            u.username,
            u.first_name,
            u.last_name,
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
        GROUP BY o.id, o.order_number, u.username, u.first_name, u.last_name, 
                 o.total_amount, o.status, o.payment_method, o.payment_status, o.created_at
        ORDER BY o.created_at DESC
        """
        
        cursor.execute(query)
        orders = cursor.fetchall()
        
        # Prepare data for table
        table_data = []
        for order in orders:
            total_amount = float(order['total_amount'])
            items = order['items'] or 'No items'
            table_data.append([
                order['order_number'],
                order['username'],
                f"{order['first_name']} {order['last_name']}",
                f"₹{total_amount:,.2f}",
                order['status'].upper(),
                order['payment_method'].upper() if order['payment_method'] else 'N/A',
                order['payment_status'].upper() if order['payment_status'] else 'N/A',
                order['order_date'].strftime('%Y-%m-%d %H:%M'),
                items[:80] + '...' if len(items) > 80 else items
            ])
        
        headers = ['Order #', 'Customer', 'Name', 'Amount', 'Status', 'Payment', 'Pay Status', 'Date', 'Items']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        
        print(f'\n📊 Order Summary:')
        print(f'   📋 Total Orders: {len(orders)}')
        total_revenue = sum(float(order['total_amount']) for order in orders)
        print(f'   💰 Total Revenue: ₹{total_revenue:,.2f}')
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    print("🗄️  ANUFA MYSQL DATABASE VIEWER")
    print("="*60)
    print(f"🔗 Host: {DATABASE_CONFIG['host']}")
    print(f"👤 Username: {DATABASE_CONFIG['user']}")
    print(f"🗄️ Database: {DATABASE_CONFIG['database']}")
    
    show_users_and_orders()
    show_detailed_orders()
