# AI E-commerce Platform Deployment Script
# This script will deploy the entire platform using Docker Compose

Write-Host "🚀 Starting AI E-commerce Platform Deployment..." -ForegroundColor Green

# Check if Docker is running
Write-Host "`n📋 Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
    exit 1
}

try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose not found. It should come with Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if Docker daemon is running
Write-Host "`n🔍 Checking if Docker daemon is running..." -ForegroundColor Yellow
try {
    docker info > $null 2>&1
    Write-Host "✅ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker daemon is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Clean up any existing containers (optional)
Write-Host "`n🧹 Cleaning up any existing containers..." -ForegroundColor Yellow
docker-compose down -v 2>$null
Write-Host "✅ Cleanup completed" -ForegroundColor Green

# Build and start all services
Write-Host "`n🏗️  Building and starting all services..." -ForegroundColor Yellow
Write-Host "This may take several minutes on first run..." -ForegroundColor Cyan

try {
    docker-compose up -d --build
    Write-Host "✅ All services started successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to start services. Check the error above." -ForegroundColor Red
    exit 1
}

# Wait for services to be ready
Write-Host "`n⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service status
Write-Host "`n📊 Checking service status..." -ForegroundColor Yellow
docker-compose ps

Write-Host "`n🎉 Deployment completed!" -ForegroundColor Green
Write-Host "`n📱 Access your application:" -ForegroundColor Cyan
Write-Host "   🌐 Main Application: http://localhost" -ForegroundColor White
Write-Host "   🌐 Direct Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "   🔧 Backend API:      http://localhost:8080" -ForegroundColor White
Write-Host "   🤖 AI Service:       http://localhost:8001" -ForegroundColor White
Write-Host "   🗄️  Database:        localhost:5432" -ForegroundColor White
Write-Host "   📊 Redis Cache:      localhost:6379" -ForegroundColor White

Write-Host "`n🛠️  Useful Commands:" -ForegroundColor Cyan
Write-Host "   View logs:           docker-compose logs -f" -ForegroundColor White
Write-Host "   Stop services:       docker-compose down" -ForegroundColor White
Write-Host "   Restart services:    docker-compose restart" -ForegroundColor White
Write-Host "   View status:         docker-compose ps" -ForegroundColor White

Write-Host "`n🔍 Testing API endpoints..." -ForegroundColor Yellow
try {
    Start-Sleep -Seconds 5
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8080/actuator/health" -Method Get -TimeoutSec 10
    Write-Host "✅ Backend API is responding" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend API not yet ready - may need more time to start" -ForegroundColor Yellow
}

try {
    $aiHealthResponse = Invoke-RestMethod -Uri "http://localhost:8001/health" -Method Get -TimeoutSec 10
    Write-Host "✅ AI Service is responding" -ForegroundColor Green
} catch {
    Write-Host "⚠️  AI Service not yet ready - may need more time to start" -ForegroundColor Yellow
}

Write-Host "`n🎊 Your AI E-commerce Platform is now running!" -ForegroundColor Green
Write-Host "Visit http://localhost to start using your application!" -ForegroundColor Cyan
