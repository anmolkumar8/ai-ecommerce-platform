# 🚀 ANUFA - GenAI-Driven E-commerce Platform for Personalized Customer Experience

ANUFA is a cutting-edge e-commerce platform powered by advanced Generative AI technologies, specifically designed for research in "GenAI-Driven Java Framework for Personalized Customer Experience in E-Commerce". This platform combines modern web technologies with sophisticated AI algorithms to deliver highly personalized customer experiences.

## 🧠 GenAI Features (Research Focus)

### Advanced AI Personalization
- **Natural Language Processing**: Real-time sentiment analysis and intent recognition
- **Conversational AI**: Context-aware, empathetic customer interactions
- **Dynamic Customer Profiling**: AI-driven personality trait inference and behavioral analysis
- **Emotional Intelligence**: Emotion-aware responses and engagement strategies
- **Predictive Analytics**: Churn risk prediction and customer lifetime value estimation
- **Dynamic Pricing**: AI-driven personalized pricing based on customer profiles

### Real-time AI Processing
- **Multi-factor Personalization Scoring**: Behavioral, sentiment, and context analysis
- **Adaptive Recommendation Engine**: Collaborative filtering + content-based + hybrid algorithms
- **Customer Journey Orchestration**: Lifecycle stage tracking and targeted interventions
- **Real-time Profile Updates**: Continuous learning from customer interactions

## 🌟 Core Platform Features

- **Premium Design**: Modern, interactive UI with smooth animations and ANUFA branding
- **AI-Powered Recommendations**: Multi-algorithm recommendation system with confidence scoring
- **Responsive Design**: Optimized for all devices (desktop, tablet, mobile)
- **Currency Formatting**: Professional money display in USD format
- **Interactive Elements**: Hover effects, animations, and micro-interactions
- **User Authentication**: Secure JWT-based login and registration system
- **Advanced Search & Filtering**: AI-enhanced search with category and preference filters
- **Modern Icons**: Beautiful lucide-react icons throughout the interface

## 🚀 Technology Stack

- **Frontend**: React 18 with Vite
- **Styling**: CSS Variables with modern design system
- **Animations**: Framer Motion for smooth transitions
- **Icons**: Lucide React
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Currency**: Intl.NumberFormat API for proper money formatting

## 💰 Currency Features

- Professional USD formatting (e.g., $1,299.99)
- Consistent money display across all components
- Proper number formatting with commas and decimal places
- Responsive price displays on product cards

## 🎨 Design Highlights

### ANUFA Branding
- Gradient logo with modern typography
- Purple and orange color scheme
- Premium visual identity
- Consistent brand application

### Interactive UI
- Smooth page transitions
- Product card hover effects
- Button animations
- Loading spinners
- Form validation feedback

### Home vs Products Pages
- **Home Page**: Hero section, featured products, AI recommendations
- **Products Page**: Complete catalog with search and filters
- Different layouts optimized for their specific purposes

## 🚀 Deployment on Render

The project is ready for deployment on Render with the included `render.yaml` configuration.

### Quick Deploy
1. Push your code to GitHub
2. Connect repository to Render
3. Create new Static Site with these settings:
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Environment Variables**: Configure your API endpoints

### Live URL
Once deployed: `https://anufa-ecommerce.onrender.com`

---

**ANUFA** - Where premium meets technology. 🚀✨

# 🛒 AI-Powered E-commerce Platform

A full-stack e-commerce platform with AI-driven product recommendations, built with React, Flask, and FastAPI.

## 🌟 Features

- **🤖 AI Recommendations** - Machine learning-powered product suggestions
- **👤 User Authentication** - Secure login and registration
- **📦 Product Catalog** - Browse and search products
- **🏷️ Categories** - Organized product categories
- **📱 Responsive Design** - Works on desktop and mobile
- **🔍 Search & Filter** - Find products easily
- **🛡️ Secure API** - JWT-based authentication

## 🏗️ Architecture

### Backend Services
- **Flask API** (`backend/java-api/`) - Main REST API for products, users, auth
- **FastAPI AI Service** (`backend/python-ai/`) - ML-powered recommendations

### Frontend
- **React App** (`frontend/`) - Modern SPA with Vite build tool

### Database
- **SQLite** - Lightweight database with sample data

## 🚀 Live Demo

**🌐 Frontend**: [Your-Frontend-URL.onrender.com](https://your-frontend-url.onrender.com)  
**🔧 Backend API**: [Your-Backend-URL.onrender.com](https://your-backend-url.onrender.com)  
**🤖 AI Service**: [Your-AI-Service-URL.onrender.com](https://your-ai-service-url.onrender.com)

## 👥 Sample Accounts

- **Username**: `johndoe` | **Password**: `password123`
- **Username**: `janesmit` | **Password**: `password123`

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Setup & Run
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ai-ecommerce-platform.git
cd ai-ecommerce-platform

# Backend API
cd backend/java-api
pip install -r requirements.txt
python app.py

# AI Service (in new terminal)
cd backend/python-ai
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8001

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

**Access locally:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- AI Service: http://localhost:8001

## 📡 API Endpoints

### Backend API (`/api`)
- `GET /actuator/health` - Health check
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /products` - List all products
- `GET /products/{id}` - Get product details
- `GET /categories` - List categories
- `GET /search?q={query}` - Search products

### AI Service (`/ai`)
- `GET /health` - Health check
- `POST /recommendations` - Get AI recommendations
- `GET /products` - List products for AI
- `POST /track-interaction` - Track user interactions

### GenAI Personalization Endpoints (`/genai`)
- `POST /genai/customer-interaction` - Process customer messages with full AI analysis
- `POST /genai/personalized-recommendations` - Generate AI-driven product recommendations with reasoning
- `POST /genai/sentiment-analysis` - Analyze customer sentiment using NLP
- `POST /genai/conversational-ai` - Generate empathetic, context-aware responses
- `GET /genai/customer-profile/{user_id}` - Get comprehensive customer profile with AI insights
- `POST /genai/dynamic-pricing` - Calculate personalized pricing based on customer profile

## 🏗️ Tech Stack

### Backend
- **Flask** - Python web framework
- **FastAPI** - Modern Python API framework
- **SQLite** - Database
- **JWT** - Authentication
- **CORS** - Cross-origin requests

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **CSS3** - Styling

### AI/ML
- **Scikit-learn** - Machine learning
- **Pandas** - Data processing
- **Asyncio** - Async processing

### Deployment
- **Render** - Cloud hosting
- **GitHub** - Version control
- **Git** - Source control

## 📦 Project Structure

```
ai-ecommerce-platform/
├── backend/
│   ├── java-api/           # Flask REST API
│   │   ├── app.py
│   │   └── requirements.txt
│   └── python-ai/          # FastAPI AI Service
│       ├── main.py
│       └── requirements.txt
├── frontend/               # React Frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── database/
│   └── init.sql           # Database schema
├── deployment/
│   └── nginx.conf         # Nginx config
└── README.md
```

## 🚀 Deployment

### Deploy to Render (Free)
1. Fork this repository
2. Connect to [Render](https://render.com)
3. Follow the [Deployment Guide](RENDER_DEPLOYMENT_GUIDE.md)

### Deploy with Docker
```bash
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Flask and FastAPI communities
- React and Vite teams
- Render for free hosting
- Open source AI/ML libraries

## 📧 Contact

**Developer**: Anmol  
**Project**: AI E-commerce Platform  
**Repository**: [GitHub](https://github.com/YOUR_USERNAME/ai-ecommerce-platform)

---

⭐ Star this repository if you found it helpful!
