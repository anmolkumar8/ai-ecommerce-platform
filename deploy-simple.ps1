# Simple AI E-commerce Platform Deployment
Write-Host "Starting AI E-commerce Platform deployment..." -ForegroundColor Green

# Create logs directory
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
python --version
node --version
npm --version

Write-Host "Installing dependencies..." -ForegroundColor Yellow

# Install backend dependencies
Write-Host "Installing backend API dependencies..." -ForegroundColor Cyan
Set-Location "backend\java-api"
pip install flask flask-cors sqlite3
Set-Location "..\..\"

# Install AI service dependencies  
Write-Host "Installing AI service dependencies..." -ForegroundColor Cyan
Set-Location "backend\python-ai"
pip install fastapi uvicorn pandas scikit-learn
Set-Location "..\..\"

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
Set-Location "frontend"
npm install
Set-Location "..\"

Write-Host "Dependencies installed successfully!" -ForegroundColor Green
Write-Host "Ready to start services manually..." -ForegroundColor Yellow
Write-Host ""
Write-Host "To start the services, open 3 separate PowerShell windows and run:" -ForegroundColor Cyan
Write-Host "1. Backend API:   cd backend\java-api && python app.py" -ForegroundColor White
Write-Host "2. AI Service:    cd backend\python-ai && python -m uvicorn main:app --host 127.0.0.1 --port 8001" -ForegroundColor White
Write-Host "3. Frontend:      cd frontend && npm run dev" -ForegroundColor White
