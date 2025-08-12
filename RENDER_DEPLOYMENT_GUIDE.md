# 🚀 Deploy AI E-commerce Platform to Render

This guide will help you deploy your AI-powered e-commerce platform to Render cloud platform.

## 📋 Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Render Account** - Sign up for free at https://render.com
3. **Git** - To push your code to GitHub

## 🔄 Step 1: Push Code to GitHub

### 1.1 Initialize Git Repository
```bash
cd C:\Users\Anmol\ai-ecommerce-platform
git init
git add .
git commit -m "Initial commit - AI E-commerce Platform"
```

### 1.2 Create GitHub Repository
1. Go to https://github.com
2. Click "New Repository"
3. Name it: `ai-ecommerce-platform`
4. Keep it public (or private if you prefer)
5. Don't initialize with README (we already have files)

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-ecommerce-platform.git
git branch -M main
git push -u origin main
```

## 🏗️ Step 2: Deploy Backend API to Render

### 2.1 Create Web Service
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your `ai-ecommerce-platform` repository

### 2.2 Configure Backend Service
- **Name**: `ai-ecommerce-backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Root Directory**: `backend/java-api`

### 2.3 Environment Variables
Add these environment variables:
- `FLASK_ENV` = `production`
- `HOST` = `0.0.0.0`
- `PORT` = `10000`

### 2.4 Deploy
- Click "Create Web Service"
- Wait for deployment (3-5 minutes)
- Note the URL (e.g., `https://ai-ecommerce-backend.onrender.com`)

## 🤖 Step 3: Deploy AI Service to Render

### 3.1 Create Another Web Service
1. Click "New +" → "Web Service"
2. Connect the same GitHub repository
3. Select `ai-ecommerce-platform` repository

### 3.2 Configure AI Service
- **Name**: `ai-ecommerce-ai-service`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
- **Root Directory**: `backend/python-ai`

### 3.3 Environment Variables
Add these environment variables:
- `ENVIRONMENT` = `production`
- `HOST` = `0.0.0.0`
- `PORT` = `10000`

### 3.4 Deploy
- Click "Create Web Service"
- Wait for deployment (3-5 minutes)
- Note the URL (e.g., `https://ai-ecommerce-ai-service.onrender.com`)

## ⚛️ Step 4: Deploy Frontend to Render

### 4.1 Create Static Site
1. Click "New +" → "Static Site"
2. Connect the same GitHub repository
3. Select `ai-ecommerce-platform` repository

### 4.2 Configure Frontend
- **Name**: `ai-ecommerce-frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`
- **Root Directory**: `frontend`

### 4.3 Environment Variables
**IMPORTANT**: Update these with your actual backend URLs from steps 2 and 3:
- `VITE_API_BASE_URL` = `https://ai-ecommerce-backend.onrender.com`
- `VITE_AI_API_BASE_URL` = `https://ai-ecommerce-ai-service.onrender.com`

### 4.4 Deploy
- Click "Create Static Site"
- Wait for deployment (2-3 minutes)
- Note the URL (e.g., `https://ai-ecommerce-frontend.onrender.com`)

## 🔧 Step 5: Update CORS Settings

### 5.1 Update Backend CORS
Since your frontend URL will be different, you need to update the CORS settings.

Edit `backend/java-api/app.py`:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://ai-ecommerce-frontend.onrender.com", "http://localhost:3000"])
```

Edit `backend/python-ai/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-ecommerce-frontend.onrender.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5.2 Commit and Push Changes
```bash
git add .
git commit -m "Update CORS for production URLs"
git push origin main
```

Render will automatically redeploy your backend services.

## 🌐 Step 6: Access Your Live Application

After all deployments are complete:

### Your Live URLs:
- **Frontend**: https://ai-ecommerce-frontend.onrender.com
- **Backend API**: https://ai-ecommerce-backend.onrender.com
- **AI Service**: https://ai-ecommerce-ai-service.onrender.com

### Test Your APIs:
- **Backend Health**: https://ai-ecommerce-backend.onrender.com/actuator/health
- **AI Health**: https://ai-ecommerce-ai-service.onrender.com/health
- **Products**: https://ai-ecommerce-backend.onrender.com/products

## 🎯 Step 7: Testing Your Live Platform

### 7.1 Test Frontend
1. Visit your frontend URL
2. Browse products
3. Test user registration/login
4. Check if AI recommendations work

### 7.2 Test APIs Directly
```bash
# Test backend health
curl https://ai-ecommerce-backend.onrender.com/actuator/health

# Test products API
curl https://ai-ecommerce-backend.onrender.com/products

# Test AI service
curl https://ai-ecommerce-ai-service.onrender.com/health
```

### 7.3 Sample Login Credentials
- Username: `johndoe` | Password: `password123`
- Username: `janesmit` | Password: `password123`

## 📊 Monitoring Your Deployment

### Render Dashboard Features:
1. **Logs** - View real-time application logs
2. **Metrics** - Monitor CPU, memory usage
3. **Deployments** - Track deployment history
4. **Environment** - Manage environment variables
5. **Domains** - Add custom domains (paid plans)

## 💰 Cost Considerations

### Free Tier Limits:
- **Web Services**: 750 hours/month (sleeps after 15min inactivity)
- **Static Sites**: Unlimited
- **Build Time**: 500 minutes/month

### Performance Notes:
- Free services "sleep" after 15 minutes of inactivity
- First request after sleeping may take 10-30 seconds
- Consider upgrading to paid plans for production use

## 🔄 Continuous Deployment

Your platform now has automatic deployment:
1. Push changes to your `main` branch
2. Render automatically detects changes
3. Rebuilds and redeploys affected services
4. Zero-downtime deployment

## 🐛 Troubleshooting

### Common Issues:

1. **Build Failure**
   - Check build logs in Render dashboard
   - Ensure all dependencies are in requirements.txt/package.json

2. **Service Won't Start**
   - Check start logs
   - Verify environment variables
   - Ensure correct start command

3. **CORS Errors**
   - Update CORS origins in backend code
   - Redeploy backend services

4. **Frontend Not Loading**
   - Check if API URLs in environment variables are correct
   - Verify backend services are running

### Support Resources:
- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

## 🎉 Congratulations!

Your AI E-commerce Platform is now live on the cloud! 

**Share your live URLs:**
- 🌐 **Frontend**: Your-Frontend-URL.onrender.com
- 🔧 **API**: Your-Backend-URL.onrender.com
- 🤖 **AI Service**: Your-AI-Service-URL.onrender.com

The platform includes:
✅ Live REST APIs
✅ AI-powered recommendations
✅ User authentication
✅ Product catalog
✅ Responsive React frontend
✅ Automatic deployments
✅ Cloud database storage

## 📈 Next Steps

1. **Custom Domain** - Add your own domain name
2. **Database** - Upgrade to PostgreSQL for production
3. **Monitoring** - Set up alerts and monitoring
4. **Analytics** - Add user analytics tracking
5. **Performance** - Optimize for better performance
6. **Security** - Implement rate limiting and security headers
