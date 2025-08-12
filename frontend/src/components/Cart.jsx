import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShoppingCart, 
  Trash2, 
  Plus, 
  Minus, 
  CreditCard,
  Truck,
  Shield,
  CheckCircle,
  ArrowRight
} from 'lucide-react';
import axios from 'axios';
import { useCart } from '../App'; // Import the cart context from App

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
});

export default function Cart({ user }) {
  // Try to use cart context, fallback to local state
  const cartContext = useCart();
  const [localCartItems, setLocalCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processingPayment, setProcessingPayment] = useState(false);
  const [orderComplete, setOrderComplete] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState('card');
  const [shippingAddress, setShippingAddress] = useState('');

  // Use cart context items if available, otherwise use local state
  const cartItems = cartContext?.cartItems || localCartItems;
  const removeFromCart = cartContext?.removeFromCart || removeFromCartLocal;
  const updateQuantity = cartContext?.updateQuantity || updateQuantityLocal;
  const clearCart = cartContext?.clearCart || (() => setLocalCartItems([]));
  const getCartTotal = cartContext?.getCartTotal || (() => calculateTotal());
  const cartCount = cartContext?.cartCount || 0;

  useEffect(() => {
    // If we have cart context, use it directly, otherwise load from API
    if (cartContext && cartContext.cartItems !== undefined) {
      setLoading(false);
    } else if (user?.id) {
      loadCart();
    } else {
      setLoading(false);
    }
  }, [user, cartContext]);

  const loadCart = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await api.get('/cart', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLocalCartItems(response.data.cart_items || []);
    } catch (error) {
      console.error('Error loading cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeFromCartLocal = async (cartId) => {
    try {
      const token = localStorage.getItem('token');
      await api.delete(`/cart/remove/${cartId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLocalCartItems(cartItems.filter(item => item.id !== cartId));
    } catch (error) {
      console.error('Error removing item:', error);
    }
  };

  const updateQuantityLocal = async (productId, newQuantity) => {
    if (newQuantity < 1) return;
    
    try {
      const token = localStorage.getItem('token');
      await api.post('/cart/add', {
        product_id: productId,
        quantity: newQuantity - cartItems.find(item => item.product_id === productId).quantity
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setLocalCartItems(cartItems.map(item => 
        item.product_id === productId 
          ? { ...item, quantity: newQuantity, item_total: newQuantity * item.price }
          : item
      ));
    } catch (error) {
      console.error('Error updating quantity:', error);
    }
  };

  const processPayment = async () => {
    if (!shippingAddress.trim()) {
      alert('Please enter a shipping address');
      return;
    }

    setProcessingPayment(true);
    
    try {
      // Simulate payment processing with better UX
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // In a real implementation, you would integrate with:
      // - Stripe, PayPal, Razorpay, or other payment gateways
      // - Send order data to backend
      // - Handle payment confirmation
      
      const orderData = {
        items: cartItems,
        total: getCartTotal(),
        paymentMethod,
        shippingAddress,
        timestamp: new Date().toISOString()
      };
      
      console.log('Order processed:', orderData);
      
      setOrderComplete(true);
      clearCart();
      
    } catch (error) {
      console.error('Payment error:', error);
      alert('Payment failed. Please try again.');
    } finally {
      setProcessingPayment(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(Number(amount));
  };

  const calculateTotal = () => {
    return cartItems.reduce((total, item) => {
      // Handle both context items (price * quantity) and API items (item_total)
      const itemTotal = item.item_total || (item.price * item.quantity);
      return total + itemTotal;
    }, 0);
  };

  if (!user) {
    return (
      <div className="cart-page">
        <div className="container">
          <div className="empty-state">
            <ShoppingCart size={64} />
            <h2>Please log in to view your cart</h2>
            <p>Sign in to access your saved items and complete your purchase</p>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p>Loading your cart...</p>
      </div>
    );
  }

  if (orderComplete) {
    return (
      <motion.div 
        className="cart-page order-complete"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="container">
          <div className="success-message">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
            >
              <CheckCircle size={80} color="green" />
            </motion.div>
            <h1>Order Successful!</h1>
            <p>Thank you for your purchase. Your order has been confirmed and will be processed shortly.</p>
            <motion.button
              className="cta-button primary"
              onClick={() => {
                setOrderComplete(false);
                setShippingAddress('');
              }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Continue Shopping
              <ArrowRight size={16} />
            </motion.button>
          </div>
        </div>
      </motion.div>
    );
  }

  if (cartItems.length === 0) {
    return (
      <div className="cart-page">
        <div className="container">
          <div className="empty-state">
            <ShoppingCart size={64} />
            <h2>Your cart is empty</h2>
            <p>Add some products to get started!</p>
            <motion.a 
              href="/products" 
              className="cta-button"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Browse Products
              <ArrowRight size={16} />
            </motion.a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <div className="container">
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="page-title">
            <ShoppingCart size={32} />
            Shopping Cart ({cartItems.length})
          </h1>
        </motion.div>

        <div className="cart-layout">
          <div className="cart-items">
            <AnimatePresence>
              {cartItems.map((item, index) => (
                <motion.div
                  key={item.id}
                  className="cart-item"
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: 20, opacity: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="item-image">
                    <div className="placeholder-image">
                      <ShoppingCart size={24} />
                    </div>
                  </div>
                  
                  <div className="item-details">
                    <h3>{item.name}</h3>
                    <p className="item-price">{formatCurrency(item.price)}</p>
                  </div>
                  
                  <div className="quantity-controls">
                    <button
                      onClick={() => updateQuantity(item.product_id || item.id, item.quantity - 1)}
                      disabled={item.quantity <= 1}
                      className="quantity-btn"
                    >
                      <Minus size={16} />
                    </button>
                    <span className="quantity">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.product_id || item.id, item.quantity + 1)}
                      className="quantity-btn"
                    >
                      <Plus size={16} />
                    </button>
                  </div>
                  
                  <div className="item-total">
                    {formatCurrency(item.item_total || (item.price * item.quantity))}
                  </div>
                  
                  <button
                    onClick={() => removeFromCart(item.id)}
                    className="remove-btn"
                  >
                    <Trash2 size={16} />
                  </button>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          <motion.div
            className="checkout-sidebar"
            initial={{ x: 20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="order-summary">
              <h3>Order Summary</h3>
              
              <div className="summary-line">
                <span>Subtotal</span>
                <span>{formatCurrency(calculateTotal())}</span>
              </div>
              
              <div className="summary-line">
                <span>Shipping</span>
                <span>Free</span>
              </div>
              
              <div className="summary-line total">
                <span>Total</span>
                <span>{formatCurrency(calculateTotal())}</span>
              </div>

              <div className="payment-section">
                <h4>Payment Method</h4>
                <div className="payment-options">
                  <label className="payment-option">
                    <input
                      type="radio"
                      value="card"
                      checked={paymentMethod === 'card'}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    />
                    <CreditCard size={16} />
                    Credit Card
                  </label>
                  <label className="payment-option">
                    <input
                      type="radio"
                      value="paypal"
                      checked={paymentMethod === 'paypal'}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    />
                    <Shield size={16} />
                    PayPal
                  </label>
                </div>
              </div>

              <div className="shipping-section">
                <h4>Shipping Address</h4>
                <textarea
                  value={shippingAddress}
                  onChange={(e) => setShippingAddress(e.target.value)}
                  placeholder="Enter your complete shipping address..."
                  className="address-input"
                  rows={3}
                />
              </div>

              <motion.button
                className="checkout-btn"
                onClick={processPayment}
                disabled={processingPayment || !shippingAddress.trim()}
                whileHover={{ scale: processingPayment ? 1 : 1.02 }}
                whileTap={{ scale: processingPayment ? 1 : 0.98 }}
              >
                {processingPayment ? (
                  <>
                    <div className="loading-spinner small"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    <CreditCard size={16} />
                    Complete Purchase
                  </>
                )}
              </motion.button>

              <div className="trust-badges">
                <div className="trust-item">
                  <Shield size={16} />
                  <span>Secure Checkout</span>
                </div>
                <div className="trust-item">
                  <Truck size={16} />
                  <span>Free Shipping</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
