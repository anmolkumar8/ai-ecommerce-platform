import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShoppingCart, 
  Search, 
  Star, 
  Heart, 
  User, 
  LogOut, 
  Package, 
  Sparkles,
  TrendingUp,
  Filter,
  Grid,
  ArrowRight,
  Plus
} from 'lucide-react';
import axios from 'axios';
import Home from './components/Home';
import Cart from './components/Cart';
import './App.css';

// API configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';
const AI_API_BASE_URL = import.meta.env.VITE_AI_API_BASE_URL || 'http://localhost:8001';

// API service
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

const aiApi = axios.create({
  baseURL: AI_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Utility function to format currency
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(amount));
};

// Header component
function Header({ user, onLogout }) {
  return (
    <motion.header 
      className="header"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="header-content">
        <Link to="/" style={{ textDecoration: 'none' }}>
          <motion.h1 
            className="anufa-logo"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.2 }}
          >
            ANUFA
          </motion.h1>
        </Link>
        <nav className="nav-links">
          <Link to="/" className="nav-link">
            <Package size={18} style={{ marginRight: '0.5rem' }} />
            Home
          </Link>
          <Link to="/products" className="nav-link">
            <Grid size={18} style={{ marginRight: '0.5rem' }} />
            Products
          </Link>
          {user && (
            <Link to="/cart" className="nav-link cart-link">
              <ShoppingCart size={18} style={{ marginRight: '0.5rem' }} />
              Cart
            </Link>
          )}
          <div className="user-actions">
            {user ? (
              <>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <User size={18} />
                  Welcome, {user.username}!
                </span>
                <motion.button 
                  onClick={onLogout} 
                  className="logout-btn"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <LogOut size={16} style={{ marginRight: '0.5rem' }} />
                  Logout
                </motion.button>
              </>
            ) : (
              <>
                <Link to="/login" className="nav-link">Login</Link>
                <Link to="/register" className="nav-link">Register</Link>
              </>
            )}
          </div>
        </nav>
      </div>
    </motion.header>
  );
}

// Home page component
function HomePage() {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadData = async () => {
      try {
        // Load featured products
        const featuredResponse = await api.get('/products/featured');
        setFeaturedProducts(featuredResponse.data.featured_products || []);

        // Load AI recommendations
        const aiResponse = await aiApi.post('/recommendations', {
          limit: 8
        });
        setRecommendations(aiResponse.data.recommendations || []);
      } catch (error) {
        console.error('Error loading data:', error);
        // Add some demo data for now
        setFeaturedProducts([
          { id: 1, name: 'Premium Headphones', description: 'High-quality wireless headphones with noise cancellation', price: 199.99, is_featured: true },
          { id: 2, name: 'Smart Watch', description: 'Advanced smartwatch with health monitoring', price: 299.99, is_featured: true },
          { id: 3, name: 'Laptop Pro', description: 'High-performance laptop for professionals', price: 1299.99, is_featured: true }
        ]);
        setRecommendations([
          { id: 4, name: 'Wireless Mouse', description: 'Ergonomic wireless mouse for productivity', price: 49.99 },
          { id: 5, name: 'Keyboard Mechanical', description: 'RGB mechanical keyboard for gaming', price: 129.99 },
          { id: 6, name: 'Monitor 4K', description: '27-inch 4K monitor with HDR support', price: 399.99 }
        ]);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p>Loading amazing products...</p>
      </div>
    );
  }

  return (
    <AnimatePresence>
      {/* Hero Section */}
      <motion.section 
        className="hero-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <div className="hero-content">
          <motion.h1 
            className="hero-title"
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
          >
            Welcome to <span style={{ color: '#f59e0b' }}>ANUFA</span>
          </motion.h1>
          <motion.p 
            className="hero-subtitle"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.6 }}
          >
            Discover premium products curated by AI technology
          </motion.p>
          <motion.div
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.6 }}
          >
            <Link to="/products" className="cta-button">
              Explore Products
              <ArrowRight size={20} />
            </Link>
          </motion.div>
        </div>
      </motion.section>

      <div className="container">
        {/* Featured Products */}
        {featuredProducts.length > 0 && (
          <motion.section 
            className="section"
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.8, duration: 0.6 }}
          >
            <h2 className="section-title">
              <Star size={28} />
              Featured Products
            </h2>
            <p className="section-subtitle">
              Hand-picked premium products just for you
            </p>
            <div className="products-grid">
              {featuredProducts.map((product, index) => (
                <motion.div
                  key={product.id}
                  initial={{ y: 30, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.9 + index * 0.1, duration: 0.5 }}
                >
                  <ProductCard product={product} />
                </motion.div>
              ))}
            </div>
          </motion.section>
        )}

        {/* AI Recommendations */}
        {recommendations.length > 0 && (
          <motion.section 
            className="section"
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 1.0, duration: 0.6 }}
          >
            <h2 className="section-title">
              <Sparkles size={28} />
              AI Recommendations
            </h2>
            <p className="section-subtitle">
              Personalized suggestions powered by advanced AI
            </p>
            <div className="products-grid">
              {recommendations.map((product, index) => (
                <motion.div
                  key={product.id}
                  initial={{ y: 30, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 1.1 + index * 0.1, duration: 0.5 }}
                >
                  <ProductCard product={product} />
                </motion.div>
              ))}
            </div>
          </motion.section>
        )}
      </div>
    </AnimatePresence>
  );
}

// Products page component
function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [productsResponse, categoriesResponse] = await Promise.all([
          api.get('/products'),
          api.get('/categories')
        ]);
        
        setProducts(productsResponse.data.products || []);
        setCategories(categoriesResponse.data.categories || []);
      } catch (error) {
        console.error('Error loading products:', error);
        // Add demo data for now
        setProducts([
          { id: 1, name: 'Premium Headphones', description: 'High-quality wireless headphones with noise cancellation', price: 199.99, is_featured: true },
          { id: 2, name: 'Smart Watch', description: 'Advanced smartwatch with health monitoring', price: 299.99, is_featured: false },
          { id: 3, name: 'Laptop Pro', description: 'High-performance laptop for professionals', price: 1299.99, is_featured: true },
          { id: 4, name: 'Wireless Mouse', description: 'Ergonomic wireless mouse for productivity', price: 49.99, is_featured: false },
          { id: 5, name: 'Keyboard Mechanical', description: 'RGB mechanical keyboard for gaming', price: 129.99, is_featured: false },
          { id: 6, name: 'Monitor 4K', description: '27-inch 4K monitor with HDR support', price: 399.99, is_featured: true },
          { id: 7, name: 'Smartphone Pro', description: 'Latest flagship smartphone with AI camera', price: 899.99, is_featured: true },
          { id: 8, name: 'Tablet Ultra', description: 'Professional tablet with stylus support', price: 699.99, is_featured: false }
        ]);
        setCategories([
          { id: 1, name: 'Electronics' },
          { id: 2, name: 'Computers' },
          { id: 3, name: 'Audio' },
          { id: 4, name: 'Mobile' }
        ]);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchTerm.trim()) return;
    
    try {
      setLoading(true);
      const response = await api.get(`/search?q=${encodeURIComponent(searchTerm)}`);
      setProducts(response.data.products || []);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredProducts = selectedCategory 
    ? products.filter(product => product.category_id === parseInt(selectedCategory))
    : products;

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p>Loading products...</p>
      </div>
    );
  }

  return (
    <motion.div 
      className="container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <motion.section 
        className="section"
        initial={{ y: 30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.1, duration: 0.5 }}
      >
        <h1 className="section-title">
          <TrendingUp size={32} />
          All Products
        </h1>
        <p className="section-subtitle">
          Discover our complete collection of premium products
        </p>

        {/* Search and Filter Bar */}
        <motion.div 
          className="search-filter-bar"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          <form onSubmit={handleSearch} className="search-form">
            <div style={{ position: 'relative', flex: 1 }}>
              <Search 
                size={18} 
                style={{
                  position: 'absolute',
                  left: '0.75rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  color: 'var(--text-secondary)'
                }}
              />
              <input
                type="text"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
                style={{ paddingLeft: '2.5rem' }}
              />
            </div>
            <motion.button 
              type="submit" 
              className="search-button"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Search
            </motion.button>
          </form>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Filter size={18} color="var(--text-secondary)" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="category-select"
            >
              <option value="">All Categories</option>
              {categories.map(category => (
                <option key={category.id} value={category.id}>{category.name}</option>
              ))}
            </select>
          </div>
        </motion.div>

        {/* Products Grid */}
        {filteredProducts.length > 0 ? (
          <motion.div 
            className="products-grid"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
          >
            <AnimatePresence>
              {filteredProducts.map((product, index) => (
                <motion.div
                  key={product.id}
                  initial={{ y: 30, opacity: 0, scale: 0.9 }}
                  animate={{ y: 0, opacity: 1, scale: 1 }}
                  exit={{ y: -30, opacity: 0, scale: 0.9 }}
                  transition={{ delay: index * 0.05, duration: 0.4 }}
                  layout
                >
                  <ProductCard product={product} />
                </motion.div>
              ))}
            </AnimatePresence>
          </motion.div>
        ) : (
          <motion.div 
            style={{ textAlign: 'center', padding: '4rem 2rem' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <Package size={64} color="var(--text-secondary)" style={{ marginBottom: '1rem' }} />
            <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-primary)' }}>No products found</h3>
            <p style={{ color: 'var(--text-secondary)' }}>Try adjusting your search or filter criteria</p>
          </motion.div>
        )}
      </motion.section>
    </motion.div>
  );
}

// Product card component
function ProductCard({ product }) {
  const [isLiked, setIsLiked] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  // Select appropriate emoji based on product name
  const getProductEmoji = (name) => {
    const lowerName = name.toLowerCase();
    if (lowerName.includes('headphone') || lowerName.includes('audio')) return '🎧';
    if (lowerName.includes('watch') || lowerName.includes('time')) return '⌚';
    if (lowerName.includes('laptop') || lowerName.includes('computer')) return '💻';
    if (lowerName.includes('mouse')) return '🖱️';
    if (lowerName.includes('keyboard')) return '⌨️';
    if (lowerName.includes('monitor') || lowerName.includes('screen')) return '🗺️';
    if (lowerName.includes('phone') || lowerName.includes('mobile')) return '📱';
    if (lowerName.includes('tablet')) return '📱';
    return '📦'; // Default package emoji
  };

  return (
    <motion.div 
      className="product-card"
      whileHover={{ y: -4 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      layout
    >
      <div className="product-image">
        <motion.div
          animate={{ 
            scale: isHovered ? 1.1 : 1,
            rotate: isHovered ? 5 : 0 
          }}
          transition={{ duration: 0.2 }}
        >
          {getProductEmoji(product.name)}
        </motion.div>
        <motion.button
          className="heart-btn"
          style={{
            position: 'absolute',
            top: '0.5rem',
            right: '0.5rem',
            background: 'rgba(255, 255, 255, 0.9)',
            border: 'none',
            borderRadius: '50%',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            backdropFilter: 'blur(10px)'
          }}
          whileTap={{ scale: 0.8 }}
          onClick={() => setIsLiked(!isLiked)}
        >
          <Heart 
            size={16} 
            fill={isLiked ? '#ef4444' : 'none'} 
            color={isLiked ? '#ef4444' : '#6b7280'}
          />
        </motion.button>
      </div>
      
      <div className="product-content">
        <h3 className="product-title">{product.name}</h3>
        <p className="product-description">{product.description}</p>
        
        <div className="product-meta">
          <span className="product-price">
            {formatCurrency(product.price)}
          </span>
          {product.is_featured && (
            <span className="featured-badge">
              <Star size={12} style={{ marginRight: '0.25rem' }} />
              Featured
            </span>
          )}
        </div>
        
        <motion.button 
          className="add-to-cart-btn"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => {
            // Add to cart logic here
            console.log('Added to cart:', product.name);
          }}
        >
          <ShoppingCart size={16} />
          Add to Cart
        </motion.button>
      </div>
    </motion.div>
  );
}

// Login component
function LoginPage({ onLogin }) {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.post('/auth/login', formData);
      onLogin(response.data.user, response.data.token);
      navigate('/');
    } catch (error) {
      setError(error.response?.data?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <motion.div 
        className="form-container"
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <motion.h1 
            className="anufa-logo"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.4 }}
          >
            ANUFA
          </motion.h1>
        </div>
        
        <h2 className="form-title">Welcome Back</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">
              <User size={18} style={{ marginRight: '0.5rem', verticalAlign: 'middle' }} />
              Username
            </label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
              className="form-input"
              placeholder="Enter your username"
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label">
              <span style={{ marginRight: '0.5rem' }}>🔒</span>
              Password
            </label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              className="form-input"
              placeholder="Enter your password"
              required
            />
          </div>
          
          {error && (
            <motion.div 
              className="error-message"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              {error}
            </motion.div>
          )}
          
          <motion.button 
            type="submit" 
            disabled={loading}
            className="form-button"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            style={{
              background: loading ? 'var(--text-secondary)' : 'var(--primary-color)'
            }}
          >
            {loading ? (
              <>
                <div className="loading-spinner" style={{ width: '16px', height: '16px', marginRight: '0.5rem' }}></div>
                Signing In...
              </>
            ) : (
              'Sign In'
            )}
          </motion.button>
        </form>
        
        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-secondary)' }}>
          Don't have an account?{' '}
          <Link 
            to="/register" 
            style={{ 
              color: 'var(--primary-color)', 
              textDecoration: 'none', 
              fontWeight: 600 
            }}
          >
            Create Account
          </Link>
        </p>
      </motion.div>
    </div>
  );
}

// Register component
function RegisterPage({ onLogin }) {
  const [formData, setFormData] = useState({
    username: '', email: '', password: '', first_name: '', last_name: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.post('/auth/register', formData);
      onLogin(response.data.user, response.data.token);
      navigate('/');
    } catch (error) {
      setError(error.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <motion.div 
        className="form-container"
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
        style={{ maxWidth: '450px' }}
      >
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <motion.h1 
            className="anufa-logo"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.4 }}
          >
            ANUFA
          </motion.h1>
        </div>
        
        <h2 className="form-title">Create Account</h2>
        
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
            <div className="form-group">
              <label className="form-label">
                <span style={{ marginRight: '0.5rem' }}>👤</span>
                First Name
              </label>
              <input
                type="text"
                value={formData.first_name}
                onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                className="form-input"
                placeholder="First name"
                required
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">
                <span style={{ marginRight: '0.5rem' }}>👤</span>
                Last Name
              </label>
              <input
                type="text"
                value={formData.last_name}
                onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                className="form-input"
                placeholder="Last name"
                required
              />
            </div>
          </div>
          
          <div className="form-group">
            <label className="form-label">
              <User size={18} style={{ marginRight: '0.5rem', verticalAlign: 'middle' }} />
              Username
            </label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
              className="form-input"
              placeholder="Choose a username"
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label">
              <span style={{ marginRight: '0.5rem' }}>📧</span>
              Email
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="form-input"
              placeholder="Enter your email"
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label">
              <span style={{ marginRight: '0.5rem' }}>🔒</span>
              Password
            </label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              className="form-input"
              placeholder="Create a password"
              required
            />
          </div>
          
          {error && (
            <motion.div 
              className="error-message"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              {error}
            </motion.div>
          )}
          
          <motion.button 
            type="submit" 
            disabled={loading}
            className="form-button"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            style={{
              background: loading ? 'var(--text-secondary)' : 'var(--accent-color)'
            }}
          >
            {loading ? (
              <>
                <div className="loading-spinner" style={{ width: '16px', height: '16px', marginRight: '0.5rem' }}></div>
                Creating Account...
              </>
            ) : (
              'Create Account'
            )}
          </motion.button>
        </form>
        
        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-secondary)' }}>
          Already have an account?{' '}
          <Link 
            to="/login" 
            style={{ 
              color: 'var(--primary-color)', 
              textDecoration: 'none', 
              fontWeight: 600 
            }}
          >
            Sign In
          </Link>
        </p>
      </motion.div>
    </div>
  );
}

// Main App component
function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      // Add token to API requests
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // Here you could verify the token and get user info
    }
  }, [token]);

  const handleLogin = (userData, userToken) => {
    setUser(userData);
    setToken(userToken);
    localStorage.setItem('token', userToken);
    api.defaults.headers.common['Authorization'] = `Bearer ${userToken}`;
  };

  const handleLogout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
  };

  return (
    <Router>
      <div style={{ minHeight: '100vh', background: '#f5f5f5' }}>
        <Header user={user} onLogout={handleLogout} />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/cart" element={<Cart user={user} />} />
            <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
            <Route path="/register" element={<RegisterPage onLogin={handleLogin} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
