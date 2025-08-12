# 🚀 AI E-commerce Platform Deployment Guide

## Prerequisites

### Install Docker Desktop
1. Download Docker Desktop for Windows from: https://www.docker.com/products/docker-desktop
2. Run the installer as Administrator
3. Restart your computer when installation completes
4. Start Docker Desktop and wait for it to initialize

### Verify Installation
Open PowerShell and run:
```powershell
docker --version
docker-compose --version
```

## Deployment Options

### Option 1: Automated Deployment (Recommended)
Run the automated deployment script:
```powershell
.\deploy.ps1
```

### Option 2: Manual Deployment
If you prefer to deploy manually:

1. **Clean up any existing containers:**
   ```powershell
   docker-compose down -v
   ```

2. **Build and start all services:**
   ```powershell
   docker-compose up -d --build
   ```

3. **Check service status:**
   ```powershell
   docker-compose ps
   ```

4. **View logs:**
   ```powershell
   docker-compose logs -f
   ```

## Services Overview

| Service | Port | Description | URL |
|---------|------|-------------|-----|
| Nginx Proxy | 80 | Reverse proxy & load balancer | http://localhost |
| React Frontend | 3000 | User interface | http://localhost:3000 |
| Java API (Flask) | 8080 | Backend REST API | http://localhost:8080 |
| Python AI Service | 8001 | ML recommendations | http://localhost:8001 |
| PostgreSQL | 5432 | Primary database | localhost:5432 |
| Redis | 6379 | Cache & sessions | localhost:6379 |

## Access Points

- **🌐 Main Application:** http://localhost
- **🔧 API Documentation:** http://localhost:8080/actuator/health
- **🤖 AI Health Check:** http://localhost:8001/health

## Useful Commands

### Service Management
```powershell
# View all running services
docker-compose ps

# Stop all services
docker-compose down

# Stop and remove all data
docker-compose down -v

# Restart specific service
docker-compose restart frontend

# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f java-api
```

### Debugging
```powershell
# Execute command in container
docker-compose exec java-api bash

# View container resource usage
docker stats

# Inspect container
docker-compose exec postgres psql -U ecommerce_user -d ecommerce_db
```

## Database Access

### PostgreSQL
- **Host:** localhost
- **Port:** 5432
- **Database:** ecommerce_db
- **Username:** ecommerce_user
- **Password:** password123

Connect using:
```powershell
docker-compose exec postgres psql -U ecommerce_user -d ecommerce_db
```

### Redis
- **Host:** localhost
- **Port:** 6379

Connect using:
```powershell
docker-compose exec redis redis-cli
```

## Troubleshooting

### Common Issues

1. **Port conflicts:**
   - Ensure ports 80, 3000, 5432, 6379, 8001, 8080 are available
   - Stop other services using these ports

2. **Docker daemon not running:**
   - Start Docker Desktop
   - Wait for the Docker icon to appear in system tray

3. **Service fails to start:**
   - Check logs: `docker-compose logs [service-name]`
   - Restart specific service: `docker-compose restart [service-name]`

4. **Database connection issues:**
   - Wait for PostgreSQL to fully initialize (may take 1-2 minutes)
   - Check health: `docker-compose exec postgres pg_isready -U ecommerce_user`

### Performance Tips

1. **Increase Docker resources:**
   - Open Docker Desktop settings
   - Allocate more RAM (minimum 4GB recommended)
   - Allocate more CPU cores

2. **Clean up unused Docker resources:**
   ```powershell
   docker system prune -f
   docker volume prune -f
   ```

## Development Workflow

1. **Make code changes** in `backend/`, `frontend/`, or `database/` directories
2. **Rebuild specific service:**
   ```powershell
   docker-compose up -d --build [service-name]
   ```
3. **View logs** to verify changes:
   ```powershell
   docker-compose logs -f [service-name]
   ```

## Production Considerations

For production deployment:
1. Change default passwords in `docker-compose.yml`
2. Use environment variables for sensitive data
3. Set up SSL/TLS certificates
4. Configure backup strategies for PostgreSQL
5. Set up monitoring and alerting
6. Use Docker Swarm or Kubernetes for orchestration

## Sample Data

The platform includes sample data:
- **Users:** admin/admin123, user/user123
- **Products:** Various sample products across categories
- **Categories:** Electronics, Fashion, Home & Garden

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout

### Products
- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get product details
- `GET /api/categories` - List categories

### AI Recommendations
- `GET /ai/recommendations/{userId}` - Get user recommendations
- `POST /ai/recommendations/similar` - Find similar products

## Support

For issues or questions:
1. Check the logs: `docker-compose logs -f`
2. Verify all services are running: `docker-compose ps`
3. Restart problematic services: `docker-compose restart [service-name]`
4. For complete reset: `docker-compose down -v && docker-compose up -d --build`
