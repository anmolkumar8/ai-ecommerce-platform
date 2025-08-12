#!/usr/bin/env python3
"""
Launch Web-based Database Viewer for ANUFA E-commerce
"""

import os
import subprocess
import webbrowser
import time
from threading import Timer

DATABASE_PATH = 'backend/java-api/ecommerce.db'

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:8080')

if __name__ == "__main__":
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Database not found: {DATABASE_PATH}")
        print("💡 Make sure your backend server has run at least once!")
        exit(1)
    
    print("🌐 Starting SQLite Web Viewer...")
    print("📁 Database:", os.path.abspath(DATABASE_PATH))
    print("🔗 URL: http://localhost:8080")
    print("💡 Press Ctrl+C to stop the server")
    print("\n" + "="*50)
    
    # Schedule browser to open
    timer = Timer(2, open_browser)
    timer.start()
    
    try:
        # Start the web viewer
        subprocess.run([
            'python', '-m', 'sqlite_web', 
            DATABASE_PATH, 
            '--host', '0.0.0.0',
            '--port', '8080'
        ])
    except KeyboardInterrupt:
        print("\n👋 Database viewer stopped!")
    except Exception as e:
        print(f"❌ Error starting viewer: {e}")
        print("💡 Try: python -m sqlite_web backend/java-api/ecommerce.db")
