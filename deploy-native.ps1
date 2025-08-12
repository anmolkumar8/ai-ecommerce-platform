# AI E-commerce Platform - Native Deployment Script (No Docker Required)
# This script will deploy the platform using native Windows services

Write-Host "🚀 Starting AI E-commerce Platform Native Deployment..." -ForegroundColor Green

# Check prerequisites
Write-Host "`n📋 Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found. It should come with Node.js installation." -ForegroundColor Red
    exit 1
}

Write-Host "`n🏗️  Setting up native deployment..." -ForegroundColor Yellow

# Create logs directory
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
Write-Host "✅ Created logs directory" -ForegroundColor Green

# Setup Backend API (Flask)
Write-Host "`n🔧 Setting up Backend API..." -ForegroundColor Yellow
Set-Location "backend\java-api"

# Install Python dependencies for backend
Write-Host "Installing Python dependencies for backend API..."
try {
    pip install -r requirements.txt
    Write-Host "✅ Backend API dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install backend dependencies" -ForegroundColor Red
    Set-Location "..\..\"
    exit 1
}

Set-Location "..\..\"

# Setup AI Service
Write-Host "`n🤖 Setting up AI Service..." -ForegroundColor Yellow
Set-Location "backend\python-ai"

# Install Python dependencies for AI service
Write-Host "Installing Python dependencies for AI service..."
try {
    pip install -r requirements.txt
    Write-Host "✅ AI Service dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install AI service dependencies" -ForegroundColor Red
    Set-Location "..\..\"
    exit 1
}

Set-Location "..\..\"

# Setup Frontend
Write-Host "`n⚛️  Setting up React Frontend..." -ForegroundColor Yellow
Set-Location "frontend"

# Install npm dependencies
Write-Host "Installing npm dependencies for frontend..."
try {
    npm install
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install frontend dependencies" -ForegroundColor Red
    Set-Location "..\"
    exit 1
}

Set-Location "..\"

# Create environment configuration
Write-Host "`n🌍 Creating environment configuration..." -ForegroundColor Yellow

# Create .env files
@"
DATABASE_URL=sqlite:///ecommerce.db
FLASK_ENV=development
HOST=127.0.0.1
PORT=8080
"@ | Out-File -FilePath "backend\java-api\.env" -Encoding UTF8

@"
ENVIRONMENT=development
DATABASE_URL=sqlite:///ai_ecommerce.db
JAVA_API_BASE_URL=http://localhost:8080
HOST=127.0.0.1
PORT=8001
"@ | Out-File -FilePath "backend\python-ai\.env" -Encoding UTF8

@"
VITE_API_BASE_URL=http://localhost:8080
VITE_AI_API_BASE_URL=http://localhost:8001
"@ | Out-File -FilePath "frontend\.env" -Encoding UTF8

Write-Host "✅ Environment files created" -ForegroundColor Green

# Initialize SQLite database
Write-Host "`n💾 Initializing database..." -ForegroundColor Yellow
Write-Host "Creating SQLite database with sample data..."

# Create a simple database initialization script
@"
import sqlite3
import hashlib
import json
from datetime import datetime

def init_database():
    # Create database connection
    conn = sqlite3.connect('backend/java-api/ecommerce.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(200) NOT NULL,
        description TEXT,
        price DECIMAL(10,2) NOT NULL,
        category_id INTEGER,
        stock_quantity INTEGER DEFAULT 0,
        image_url VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    ''')
    
    # Insert sample data
    # Categories
    categories = [
        ('Electronics', 'Electronic devices and gadgets'),
        ('Fashion', 'Clothing and accessories'),
        ('Home & Garden', 'Home improvement and garden supplies'),
        ('Books', 'Books and educational materials'),
        ('Sports', 'Sports equipment and gear')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)', categories)
    
    # Users
    admin_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    user_hash = hashlib.sha256('user123'.encode()).hexdigest()
    
    users = [
        ('admin', 'admin@example.com', admin_hash, 'Admin', 'User'),
        ('user', 'user@example.com', user_hash, 'Test', 'User'),
        ('john_doe', 'john@example.com', user_hash, 'John', 'Doe')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO users (username, email, password_hash, first_name, last_name) VALUES (?, ?, ?, ?, ?)', users)
    
    # Products
    products = [
        ('Smartphone Pro', 'Latest smartphone with advanced features', 799.99, 1, 50, 'https://via.placeholder.com/300x200'),
        ('Laptop Ultra', 'High-performance laptop for professionals', 1299.99, 1, 30, 'https://via.placeholder.com/300x200'),
        ('Wireless Earbuds', 'Premium wireless earbuds with noise cancellation', 199.99, 1, 100, 'https://via.placeholder.com/300x200'),
        ('Designer T-Shirt', 'Comfortable cotton t-shirt with modern design', 29.99, 2, 200, 'https://via.placeholder.com/300x200'),
        ('Running Shoes', 'Lightweight running shoes for athletes', 89.99, 2, 75, 'https://via.placeholder.com/300x200'),
        ('Coffee Maker', 'Programmable coffee maker with timer', 149.99, 3, 25, 'https://via.placeholder.com/300x200'),
        ('Programming Book', 'Complete guide to modern programming', 49.99, 4, 60, 'https://via.placeholder.com/300x200'),
        ('Yoga Mat', 'Non-slip yoga mat for home workouts', 39.99, 5, 80, 'https://via.placeholder.com/300x200')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO products (name, description, price, category_id, stock_quantity, image_url) VALUES (?, ?, ?, ?, ?, ?)', products)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_database()
"@ | Out-File -FilePath "init_db.py" -Encoding UTF8

python init_db.py
Remove-Item "init_db.py"

Write-Host "✅ Database initialized with sample data" -ForegroundColor Green

Write-Host "`n🎉 Setup completed! Starting all services..." -ForegroundColor Green

# Start services using PowerShell jobs
Write-Host "`n🚀 Starting Backend API (Port 8080)..." -ForegroundColor Yellow
Start-Job -Name "BackendAPI" -ScriptBlock {
    Set-Location "C:\Users\Anmol\ai-ecommerce-platform\backend\java-api"
    python app.py 2>&1 | Tee-Object -FilePath "..\..\logs\backend-api.log"
} | Out-Null

Start-Sleep -Seconds 3

Write-Host "🤖 Starting AI Service (Port 8001)..." -ForegroundColor Yellow
Start-Job -Name "AIService" -ScriptBlock {
    Set-Location "C:\Users\Anmol\ai-ecommerce-platform\backend\python-ai"
    python -m uvicorn main:app --host 127.0.0.1 --port 8001 2>&1 | Tee-Object -FilePath "..\..\logs\ai-service.log"
} | Out-Null

Start-Sleep -Seconds 3

Write-Host "⚛️  Starting Frontend (Port 3000)..." -ForegroundColor Yellow
Start-Job -Name "Frontend" -ScriptBlock {
    Set-Location "C:\Users\Anmol\ai-ecommerce-platform\frontend"
    npm run dev 2>&1 | Tee-Object -FilePath "..\logs\frontend.log"
} | Out-Null

# Wait for services to start
Write-Host "`n⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if services are running
Write-Host "`n📊 Checking service status..." -ForegroundColor Yellow
Get-Job | Format-Table

Write-Host "`n🎊 Deployment completed!" -ForegroundColor Green
Write-Host "`n📱 Access your application:" -ForegroundColor Cyan
Write-Host "   🌐 Frontend App:     http://localhost:3000" -ForegroundColor White
Write-Host "   🔧 Backend API:      http://localhost:8080" -ForegroundColor White
Write-Host "   🤖 AI Service:       http://localhost:8001" -ForegroundColor White

Write-Host "`n🛠️  Service Management:" -ForegroundColor Cyan
Write-Host "   View all jobs:       Get-Job" -ForegroundColor White
Write-Host "   Stop all services:   Get-Job | Stop-Job" -ForegroundColor White
Write-Host "   View job output:     Receive-Job -Name 'BackendAPI'" -ForegroundColor White
Write-Host "   View logs:           Get-Content logs\backend-api.log -Wait" -ForegroundColor White

Write-Host "`n🔍 Testing services..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/actuator/health" -Method Get -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend API is responding" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Backend API not ready yet - check logs: Get-Content logs\backend-api.log" -ForegroundColor Yellow
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -Method Get -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ AI Service is responding" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  AI Service not ready yet - check logs: Get-Content logs\ai-service.log" -ForegroundColor Yellow
}

Write-Host "`n🎉 Your AI E-commerce Platform is now running natively!" -ForegroundColor Green
Write-Host "Visit http://localhost:3000 to start using your application!" -ForegroundColor Cyan

Write-Host "`n📝 Sample login credentials:" -ForegroundColor Cyan
Write-Host "   Username: admin | Password: admin123" -ForegroundColor White
Write-Host "   Username: user  | Password: user123" -ForegroundColor White
