# 🛒 ANUFA AI E-commerce Platform

🤖 **Complete AI-Powered E-commerce Solution** - A modern, intelligent e-commerce platform featuring zero-latency loading, personalized AI recommendations, and seamless user experience.

## ⚡ Key Highlights

- **🚀 Zero Latency Loading**: Instant product display with background data fetching
- **🧠 AI-Powered Recommendations**: Smart product suggestions using machine learning
- **🔐 Secure Authentication**: JWT-based user registration and login system
- **📱 Responsive Design**: Mobile-first, modern UI/UX
- **🗄️ Complete Database Solution**: Single-file database setup and management

## 🏗️ Project Structure

```
ai-ecommerce-platform/
├── frontend/                 # React.js Frontend
│   ├── src/
│   │   ├── App.jsx          # Main application component
│   │   └── App.css          # Styling
│   ├── index.html           # HTML template
│   └── package.json         # Dependencies
├── backend/
│   └── java-api/
│       ├── app_sqlite.py    # Main Flask API server
│       ├── requirements_sqlite.txt  # Python dependencies
│       └── ecommerce.db     # SQLite database (auto-created)
└── database_setup.py        # 🔧 Single database management tool
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/your-username/ai-ecommerce-platform.git
cd ai-ecommerce-platform
```

### 2. Setup Database (Required First)
```bash
python database_setup.py
# Choose option 1 to initialize database
```

### 3. Start Backend API
```bash
cd backend/java-api
pip install -r requirements_sqlite.txt
python app_sqlite.py
# Server runs on http://localhost:8080
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
# Development server runs on http://localhost:5173
```

## 🗄️ Database Management

**Single Command Database Setup:**

```bash
python database_setup.py
```

### Available Options:
1. **🔧 Initialize/Setup Database** - Create all tables with sample data
2. **📊 View Database Summary** - See record counts and database info
3. **👀 View All Data** - Browse all table contents
4. **🔍 View Specific Table** - Examine individual tables
5. **🔄 Reset Database** - Complete database reset and reinitialize

### Database Features:
- ✅ Complete table creation (users, products, categories, cart, orders, AI recommendations)
- 📦 Comprehensive sample data insertion
- 👥 Test users with authentication (password: `password123`)
- 🛍️ Sample products across multiple categories
- 🧠 AI recommendation examples
- 📊 Order and cart sample data

## 🌐 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Products & Categories  
- `GET /products` - All products
- `GET /products/{id}` - Specific product
- `GET /products/featured` - Featured products
- `GET /categories` - All categories
- `GET /search?q={query}` - Product search

### System
- `GET /actuator/health` - Health check

## 🧪 Test Data

### Sample Users (Password: `password123`)
- **johndoe** (john@example.com)
- **janesmit** (jane@example.com)  
- **bobwilson** (bob@example.com)

### Sample Products
- Smartphones, Laptops, Headphones (Electronics)
- T-shirts, Jeans, Shoes (Clothing)
- Programming Books, AI Guides (Books)
- Garden Tools, Security Systems (Home & Garden)
- Yoga Mats, Dumbbells (Sports)

## 💻 Technology Stack

### Frontend
- **React.js** with **Vite** (Fast development)
- **Modern CSS** (Responsive design)
- **JavaScript ES6+**

### Backend
- **Python Flask** (REST API)
- **SQLite** (Local database)
- **JWT** (Authentication)
- **SHA256** (Password hashing)

### Database
- **SQLite** (Zero-configuration)
- **Foreign Keys** (Data integrity)
- **Comprehensive Schema** (All e-commerce entities)

## 🔧 Development

### Database Management
```bash
# Initialize fresh database
python database_setup.py
# Select option 1

# View database contents
python database_setup.py  
# Select option 3

# Reset everything
python database_setup.py
# Select option 5
```

### Running Services
```bash
# Backend API
cd backend/java-api && python app_sqlite.py

# Frontend Development  
cd frontend && npm run dev
```

## ⚡ Zero Latency Feature

The platform implements **instant loading** by:
1. **Immediate UI Rendering** - Demo data displays instantly
2. **Background Data Fetching** - Real data loads seamlessly
3. **No Loading Spinners** - Eliminates perceived wait time
4. **Smooth Transitions** - Demo to real data updates transparently

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push branch (`git push origin feature/NewFeature`)
5. Open Pull Request

## 📄 License

MIT License - See LICENSE file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/ai-ecommerce-platform/issues)
- **Documentation**: Check code comments and this README
- **Database Problems**: Use `database_setup.py` to reset/reinitialize

---

⭐ **Star this repository if it helps you!**

*Built with ❤️ for modern e-commerce development*
