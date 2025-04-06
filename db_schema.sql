-- Database Schema for Celestial Insights Astrology
-- Generated for deployment

-- Admin table
CREATE TABLE admin (
  id SERIAL PRIMARY KEY,
  username VARCHAR(64) UNIQUE NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password_hash VARCHAR(256) NOT NULL
);

-- BlogPost table
CREATE TABLE blog_post (
  id SERIAL PRIMARY KEY,
  title VARCHAR(120) NOT NULL,
  slug VARCHAR(120) UNIQUE NOT NULL,
  content TEXT NOT NULL,
  summary VARCHAR(200),
  image_url VARCHAR(256),
  published BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Service table
CREATE TABLE service (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  description TEXT NOT NULL,
  short_description VARCHAR(200),
  price FLOAT NOT NULL,
  duration INTEGER NOT NULL,
  image_url VARCHAR(256),
  is_available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Booking table
CREATE TABLE booking (
  id SERIAL PRIMARY KEY,
  service_id INTEGER REFERENCES service(id) NOT NULL,
  customer_name VARCHAR(100) NOT NULL,
  customer_email VARCHAR(120) NOT NULL,
  customer_phone VARCHAR(20),
  booking_date DATE NOT NULL,
  booking_time TIME NOT NULL,
  notes TEXT,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CartItem table
CREATE TABLE cart_item (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(64) NOT NULL,
  service_id INTEGER REFERENCES service(id) NOT NULL,
  quantity INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order table
CREATE TABLE "order" (
  id SERIAL PRIMARY KEY,
  order_number VARCHAR(20) UNIQUE NOT NULL,
  customer_name VARCHAR(100) NOT NULL,
  customer_email VARCHAR(120) NOT NULL,
  customer_phone VARCHAR(20),
  total_amount FLOAT NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- OrderItem table
CREATE TABLE order_item (
  id SERIAL PRIMARY KEY,
  order_id INTEGER REFERENCES "order"(id) NOT NULL,
  service_id INTEGER REFERENCES service(id) NOT NULL,
  service_name VARCHAR(100) NOT NULL,
  price FLOAT NOT NULL,
  quantity INTEGER DEFAULT 1
);

-- Contact table
CREATE TABLE contact (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL,
  subject VARCHAR(200),
  message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_read BOOLEAN DEFAULT FALSE
);

-- Sample admin user (username: admin, password: password)
INSERT INTO admin (username, email, password_hash) 
VALUES ('admin', 'admin@example.com', 'pbkdf2:sha256:260000$abc123yoursecurehashhere');

-- Instructions for deployment:
-- 1. Create a new PostgreSQL database
-- 2. Run this SQL script to create the schema
-- 3. Update the DATABASE_URL environment variable in your app configuration
