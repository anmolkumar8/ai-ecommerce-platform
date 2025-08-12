import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowRight, 
  TrendingUp, 
  Sparkles, 
  ShoppingCart,
  Star,
  Users,
  Award,
  Zap
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
});

export default function Home() {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [aiRecommendations, setAiRecommendations] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHomeData();
  }, []);

  const loadHomeData = async () => {
    try {
      // Load featured products
      const featuredResponse = await api.get('/products/featured');
      setFeaturedProducts(featuredResponse.data.featured_products || []);

      // Load AI recommendations
      const aiResponse = await api.get('/ai/recommendations?limit=4');
      setAiRecommendations(aiResponse.data.recommendations || []);

      // Load analytics for research
      const analyticsResponse = await api.get('/ai/analytics/user-behavior');
      setAnalytics(analyticsResponse.data);

    } catch (error) {
      console.error('Error loading home data:', error);
      // Set demo data on error
      setFeaturedProducts([
        { id: 1, name: 'Smartphone Pro Max', price: 999.99, description: 'Latest flagship smartphone' },
        { id: 2, name: 'Wireless Headphones', price: 299.99, description: 'Premium noise-cancelling headphones' },
        { id: 3, name: 'Ultra-Slim Laptop', price: 1299.99, description: 'High-performance laptop' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p>Loading ANUFA Experience...</p>
      </div>
    );
  }

  return (
    <div className="home-page">
      {/* Hero Section */}
      <motion.section 
        className="hero-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <div className="hero-content">
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="hero-text"
          >
            <h1 className="hero-title">
              Welcome to <span className="brand-highlight">ANUFA</span>
              <Sparkles className="sparkle-icon" size={32} />
            </h1>
            <p className="hero-subtitle">
              Experience the future of e-commerce with AI-powered personalization and intelligent product recommendations
            </p>
            <div className="hero-stats">
              <div className="stat-item">
                <Users size={20} />
                <span>{analytics?.user_behavior?.total_users || '1000+'} Users</span>
              </div>
              <div className="stat-item">
                <Award size={20} />
                <span>85% Accuracy</span>
              </div>
              <div className="stat-item">
                <TrendingUp size={20} />
                <span>34% Engagement</span>
              </div>
            </div>
            <div className="hero-actions">
              <Link to="/products" className="cta-button primary">
                <ShoppingCart size={20} />
                Shop Now
                <ArrowRight size={16} />
              </Link>
              <Link to="/ai-insights" className="cta-button secondary">
                <Zap size={20} />
                AI Insights
              </Link>
            </div>
          </motion.div>
          
          <motion.div
            initial={{ x: 50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            className="hero-visual"
          >
            <div className="ai-visualization">
              <div className="ai-node active">
                <Sparkles size={24} />
                <span>AI Engine</span>
              </div>
              <div className="ai-node">
                <Users size={20} />
                <span>User Behavior</span>
              </div>
              <div className="ai-node">
                <TrendingUp size={20} />
                <span>Predictions</span>
              </div>
              <div className="connection-lines">
                <div className="line line-1"></div>
                <div className="line line-2"></div>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.section>

      {/* AI Recommendations Section */}
      <motion.section 
        className="recommendations-section"
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.6, duration: 0.6 }}
      >
        <div className="container">
          <div className="section-header">
            <h2>
              <Zap className="section-icon" />
              AI-Powered Recommendations
            </h2>
            <p>Discover products tailored just for you using advanced machine learning algorithms</p>
          </div>
          
          <div className="products-grid">
            {aiRecommendations.map((product) => (
              <motion.div
                key={product.id}
                className="product-card ai-recommended"
                whileHover={{ y: -5, boxShadow: "0 10px 25px rgba(0,0,0,0.1)" }}
                transition={{ duration: 0.2 }}
              >
                <div className="ai-badge">
                  <Sparkles size={14} />
                  AI Pick
                </div>
                <div className="product-image">
                  <div className="placeholder-image">
                    <ShoppingCart size={32} />
                  </div>
                </div>
                <div className="product-info">
                  <h3>{product.name}</h3>
                  <p>{product.description}</p>
                  <div className="product-rating">
                    <Star size={16} fill="gold" />
                    <span>{product.rating || 4.5}</span>
                  </div>
                  <div className="product-price">
                    {formatCurrency(product.price)}
                  </div>
                </div>
                <Link to={`/products/${product.id}`} className="product-link">
                  View Details
                  <ArrowRight size={16} />
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Featured Products Section */}
      <motion.section 
        className="featured-section"
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.6 }}
      >
        <div className="container">
          <div className="section-header">
            <h2>
              <Award className="section-icon" />
              Featured Products
            </h2>
            <p>Handpicked premium products with the highest ratings and user satisfaction</p>
          </div>
          
          <div className="products-grid">
            {featuredProducts.map((product) => (
              <motion.div
                key={product.id}
                className="product-card featured"
                whileHover={{ y: -5, boxShadow: "0 10px 25px rgba(0,0,0,0.1)" }}
                transition={{ duration: 0.2 }}
              >
                <div className="featured-badge">Featured</div>
                <div className="product-image">
                  <div className="placeholder-image">
                    <ShoppingCart size={32} />
                  </div>
                </div>
                <div className="product-info">
                  <h3>{product.name}</h3>
                  <p>{product.description}</p>
                  <div className="product-price">
                    {formatCurrency(product.price)}
                  </div>
                </div>
                <Link to={`/products/${product.id}`} className="product-link">
                  Shop Now
                  <ArrowRight size={16} />
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Research Insights Section */}
      {analytics && (
        <motion.section 
          className="insights-section"
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1.0, duration: 0.6 }}
        >
          <div className="container">
            <div className="section-header">
              <h2>
                <TrendingUp className="section-icon" />
                Platform Analytics
              </h2>
              <p>Real-time insights powered by AI for research and optimization</p>
            </div>
            
            <div className="analytics-grid">
              <div className="analytics-card">
                <div className="metric-value">{analytics.user_behavior.total_users}</div>
                <div className="metric-label">Active Users</div>
              </div>
              <div className="analytics-card">
                <div className="metric-value">{formatCurrency(analytics.user_behavior.avg_order_value)}</div>
                <div className="metric-label">Avg. Order Value</div>
              </div>
              <div className="analytics-card">
                <div className="metric-value">{analytics.ai_insights.recommendation_accuracy}</div>
                <div className="metric-label">AI Accuracy</div>
              </div>
              <div className="analytics-card">
                <div className="metric-value">{analytics.ai_insights.conversion_rate_increase}</div>
                <div className="metric-label">Conversion Boost</div>
              </div>
            </div>
          </div>
        </motion.section>
      )}
    </div>
  );
}
