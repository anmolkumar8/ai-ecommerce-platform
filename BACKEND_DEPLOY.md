# 🔧 ANUFA Backend Deployment Guide

Your ANUFA frontend is live! Now let's deploy the backend services to make it fully functional.

## 🎯 What We're Deploying

1. **Flask API** (`backend/java-api/`) - Main REST API for products, users, authentication
2. **FastAPI AI Service** (`backend/python-ai/`) - AI-powered product recommendations

## 🚀 Deploy Flask API (Main Backend)

### Step 1: Create Flask Web Service

1. **Go to Render Dashboard**:
   - Visit [render.com](https://render.com)
   - Click "New +" → "Web Service"

2. **Connect Repository**:
   - Select your `ai-ecommerce-platform` repository
   - Click "Connect"

3. **Configure Service Settings**:
   ```
   Name: anufa-backend
   Root Directory: backend/java-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
   ```

4. **Environment Variables**:
   Click "Advanced" → "Add Environment Variable":
   ```
   FLASK_ENV = production
   PORT = 10000
   SECRET_KEY = anufa-super-secret-key-change-in-production
   ```

5. **Create Service**:
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - You'll get a URL like: `https://anufa-backend.onrender.com`

### Step 2: Test Flask API

Once deployed, test these endpoints:
- **Health Check**: `https://anufa-backend.onrender.com/actuator/health`
- **Products**: `https://anufa-backend.onrender.com/products`
- **Categories**: `https://anufa-backend.onrender.com/categories`

## 🤖 Deploy FastAPI AI Service

### Step 1: Create FastAPI Web Service

1. **Create New Service**:
   - Click "New +" → "Web Service"
   - Select same repository
   - Click "Connect"

2. **Configure AI Service Settings**:
   ```
   Name: anufa-ai-service
   Root Directory: backend/python-ai
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**:
   ```
   PORT = 10000
   ```

4. **Create Service**:
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - You'll get a URL like: `https://anufa-ai-service.onrender.com`

### Step 2: Test AI Service

Test these endpoints:
- **Health Check**: `https://anufa-ai-service.onrender.com/health`
- **API Docs**: `https://anufa-ai-service.onrender.com/docs`

## 🔗 Connect Frontend to Backends

### Update Frontend Environment Variables

1. **Go to Frontend Service**:
   - In Render dashboard, find your `anufa-ecommerce` service
   - Click on it

2. **Update Environment Variables**:
   - Click "Environment" tab
   - Update or add these variables:
   ```
   VITE_API_BASE_URL = https://anufa-backend.onrender.com
   VITE_AI_API_BASE_URL = https://anufa-ai-service.onrender.com
   ```
   *(Replace with your actual backend URLs)*

3. **Redeploy Frontend**:
   - Go to "Manual Deploy" section
   - Click "Deploy latest commit"
   - Wait for frontend to rebuild and redeploy

## ✅ Verification Checklist

After all services are deployed:

### Backend API Tests
- [ ] `https://anufa-backend.onrender.com/actuator/health` returns `{"status": "UP"}`
- [ ] `https://anufa-backend.onrender.com/products` returns product list
- [ ] `https://anufa-backend.onrender.com/categories` returns categories
- [ ] `https://anufa-backend.onrender.com/products/featured` returns featured products

### AI Service Tests  
- [ ] `https://anufa-ai-service.onrender.com/health` returns `{"status": "healthy"}`
- [ ] `https://anufa-ai-service.onrender.com/docs` shows FastAPI documentation

### Frontend Integration Tests
- [ ] Visit `https://ai-ecommerce-platform.onrender.com`
- [ ] Products load from backend (not demo data)
- [ ] Search functionality works
- [ ] Featured products display correctly
- [ ] User registration works
- [ ] User login works

## 🔧 Your Service URLs

Once deployed, your complete ANUFA platform will have:

- **Frontend**: `https://ai-ecommerce-platform.onrender.com`
- **Main API**: `https://anufa-backend.onrender.com`
- **AI Service**: `https://anufa-ai-service.onrender.com`

## 🐛 Troubleshooting

### Backend Won't Start
- Check build logs for Python/dependency errors
- Ensure `requirements.txt` files are correct
- Verify start commands are exact

### Frontend Can't Connect to Backend
- Check environment variables are set correctly
- Ensure backend URLs are accessible
- Look for CORS issues in browser console

### Database Issues
- Flask API creates SQLite database automatically
- Sample data is inserted on first run
- Check logs for database creation errors

## 📞 Next Steps

After successful deployment:

1. **Test Complete User Flow**:
   - Register a new account
   - Browse products
   - Search functionality
   - View AI recommendations

2. **Monitor Performance**:
   - Check service logs in Render dashboard
   - Monitor response times
   - Set up alerts for downtime

3. **Optional Enhancements**:
   - Add environment-specific configurations
   - Set up monitoring and logging
   - Configure custom domains

---

🎉 **Congratulations!** Your complete ANUFA platform is now live with:
- Beautiful, responsive frontend
- Fully functional REST API
- AI-powered recommendations
- Real user authentication
- Product search and filtering

**Your Live Platform**: https://ai-ecommerce-platform.onrender.com
