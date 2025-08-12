-- AI E-commerce Platform Database Schema
-- Initialize database with tables and sample data

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE
);

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id BIGINT REFERENCES categories(id),
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id BIGINT REFERENCES categories(id),
    sku VARCHAR(50) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    compare_price DECIMAL(10,2),
    stock_quantity INTEGER DEFAULT 0,
    weight DECIMAL(8,2),
    dimensions VARCHAR(50),
    brand VARCHAR(100),
    tags TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product images table
CREATE TABLE IF NOT EXISTS product_images (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    alt_text VARCHAR(200),
    sort_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE
);

-- Shopping cart table
CREATE TABLE IF NOT EXISTS cart_items (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    subtotal DECIMAL(10,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    shipping_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_status VARCHAR(50) DEFAULT 'pending',
    shipping_address JSONB,
    billing_address JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
    product_id BIGINT REFERENCES products(id),
    product_name VARCHAR(200) NOT NULL,
    product_sku VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL
);

-- Product reviews table
CREATE TABLE IF NOT EXISTS product_reviews (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200),
    review_text TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User interactions for AI recommendations
CREATE TABLE IF NOT EXISTS user_interactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    interaction_type VARCHAR(50) NOT NULL, -- 'view', 'add_to_cart', 'purchase', 'review'
    session_id VARCHAR(100),
    interaction_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI recommendations cache
CREATE TABLE IF NOT EXISTS ai_recommendations (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    recommendation_type VARCHAR(50), -- 'similar', 'collaborative', 'content_based'
    confidence_score DECIMAL(5,4),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(is_active);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_cart_user ON cart_items(user_id);
CREATE INDEX IF NOT EXISTS idx_interactions_user ON user_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_interactions_product ON user_interactions(product_id);

-- Insert sample data
INSERT INTO categories (name, description) VALUES 
('Electronics', 'Electronic devices and gadgets'),
('Clothing', 'Fashion and apparel'),
('Books', 'Books and educational materials'),
('Home & Garden', 'Home improvement and garden supplies'),
('Sports', 'Sports and fitness equipment')
ON CONFLICT DO NOTHING;

-- Insert sample products
INSERT INTO products (name, description, category_id, sku, price, stock_quantity, is_featured, tags) VALUES 
('Smartphone Pro Max', 'Latest flagship smartphone with AI-powered camera and 5G connectivity', 1, 'PHONE-001', 999.99, 50, true, ARRAY['smartphone', 'technology', 'mobile', '5G']),
('Wireless Noise-Cancelling Headphones', 'Premium over-ear headphones with active noise cancellation', 1, 'AUDIO-001', 299.99, 25, true, ARRAY['audio', 'wireless', 'headphones', 'noise-cancelling']),
('Ultra-Slim Laptop', 'High-performance laptop with 16GB RAM and SSD storage', 1, 'LAPTOP-001', 1299.99, 15, true, ARRAY['laptop', 'computer', 'technology', 'productivity']),
('Smart Watch Series X', 'Advanced smartwatch with health monitoring and GPS', 1, 'WATCH-001', 399.99, 30, false, ARRAY['smartwatch', 'fitness', 'health', 'wearable']),
('Organic Cotton T-Shirt', 'Comfortable 100% organic cotton t-shirt', 2, 'SHIRT-001', 29.99, 100, false, ARRAY['clothing', 'cotton', 'casual', 'organic']),
('Designer Jeans', 'Premium denim jeans with perfect fit', 2, 'JEANS-001', 89.99, 75, false, ARRAY['clothing', 'denim', 'jeans', 'designer']),
('Running Shoes Pro', 'Professional running shoes with advanced cushioning', 2, 'SHOES-001', 149.99, 60, true, ARRAY['shoes', 'running', 'sports', 'fitness']),
('Programming Fundamentals', 'Complete guide to modern programming languages', 3, 'BOOK-001', 49.99, 40, false, ARRAY['book', 'programming', 'education', 'technology']),
('AI and Machine Learning', 'Comprehensive guide to artificial intelligence', 3, 'BOOK-002', 59.99, 35, false, ARRAY['book', 'AI', 'machine learning', 'education']),
('Garden Tools Professional Set', 'Complete set of professional gardening tools', 4, 'GARDEN-001', 129.99, 20, false, ARRAY['garden', 'tools', 'outdoor', 'professional']),
('Smart Home Security System', 'Complete home security system with AI detection', 4, 'SECURITY-001', 299.99, 25, true, ARRAY['security', 'smart home', 'AI', 'technology']),
('Yoga Mat Premium', 'Non-slip premium yoga mat for all exercises', 5, 'YOGA-001', 39.99, 80, false, ARRAY['yoga', 'fitness', 'exercise', 'wellness']),
('Dumbbells Set', 'Adjustable dumbbells set for home workouts', 5, 'WEIGHTS-001', 199.99, 45, false, ARRAY['fitness', 'weights', 'home gym', 'strength training'])
ON CONFLICT (sku) DO NOTHING;

-- Insert sample users (password is 'password123' hashed with bcrypt)
INSERT INTO users (username, email, password_hash, first_name, last_name, email_verified) VALUES 
('johndoe', 'john@example.com', '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewTwT2/jkZ8e8aBi', 'John', 'Doe', true),
('janesmit', 'jane@example.com', '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewTwT2/jkZ8e8aBi', 'Jane', 'Smith', true),
('bobwilson', 'bob@example.com', '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewTwT2/jkZ8e8aBi', 'Bob', 'Wilson', true)
ON CONFLICT (username) DO NOTHING;

-- Insert sample product images
INSERT INTO product_images (product_id, image_url, alt_text, is_primary) VALUES 
(1, 'https://via.placeholder.com/400x400?text=Smartphone+Pro', 'Smartphone Pro Max', true),
(2, 'https://via.placeholder.com/400x400?text=Headphones', 'Wireless Headphones', true),
(3, 'https://via.placeholder.com/400x400?text=Laptop', 'Ultra-Slim Laptop', true),
(4, 'https://via.placeholder.com/400x400?text=Smart+Watch', 'Smart Watch Series X', true),
(5, 'https://via.placeholder.com/400x400?text=T-Shirt', 'Organic Cotton T-Shirt', true)
ON CONFLICT DO NOTHING;

-- Insert sample user interactions for AI training
INSERT INTO user_interactions (user_id, product_id, interaction_type, session_id) VALUES 
(1, 1, 'view', 'session_001'),
(1, 2, 'view', 'session_001'),
(1, 1, 'add_to_cart', 'session_001'),
(2, 3, 'view', 'session_002'),
(2, 4, 'view', 'session_002'),
(2, 3, 'add_to_cart', 'session_002'),
(3, 5, 'view', 'session_003'),
(3, 6, 'view', 'session_003')
ON CONFLICT DO NOTHING;

-- Insert sample reviews
INSERT INTO product_reviews (user_id, product_id, rating, title, review_text, is_verified_purchase, is_approved) VALUES 
(1, 1, 5, 'Excellent smartphone!', 'This phone exceeded my expectations. Great camera and battery life.', true, true),
(2, 3, 4, 'Great laptop for work', 'Perfect for programming and daily tasks. Very fast and lightweight.', true, true),
(3, 5, 5, 'Very comfortable', 'Love the quality of this organic cotton t-shirt. Fits perfectly.', true, true)
ON CONFLICT DO NOTHING;

-- Create a function to generate order numbers
CREATE OR REPLACE FUNCTION generate_order_number() RETURNS TEXT AS $$
BEGIN
    RETURN 'ORD-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || LPAD(NEXTVAL('orders_id_seq')::TEXT, 6, '0');
END;
$$ LANGUAGE plpgsql;

-- Add a trigger to auto-generate order numbers
CREATE OR REPLACE FUNCTION set_order_number()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.order_number IS NULL THEN
        NEW.order_number := generate_order_number();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_order_number
    BEFORE INSERT ON orders
    FOR EACH ROW
    EXECUTE FUNCTION set_order_number();

COMMIT;
