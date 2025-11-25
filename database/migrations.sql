-- ==============================================
-- FreshRoute Logistics Database Migrations
-- CLI-Based Delivery Route & Package Tracking System
-- ==============================================

-- 0. Create Database
DROP DATABASE IF EXISTS freshroutelogistics;
CREATE DATABASE freshroutelogistics;
USE freshroutelogistics;

-- 1. users Table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin','dispatcher','driver','manager') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 3. routes Table
DROP TABLE IF EXISTS routes;
CREATE TABLE routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(150) NOT NULL,
    route_date DATE NOT NULL,
    user_id INT,
    fuel_estimate DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 4. packages Table
DROP TABLE IF EXISTS packages;
CREATE TABLE packages (
    package_id INT AUTO_INCREMENT PRIMARY KEY,
    sender VARCHAR(150) NOT NULL,
    recipient_name VARCHAR(150) NOT NULL,
    recipient_address TEXT NOT NULL,
    phone VARCHAR(20),
    weight DECIMAL(10,2),
    category VARCHAR(50),
    status ENUM('Pending','Out for Delivery','Delivered') DEFAULT 'Pending',
    current_route_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (current_route_id) REFERENCES routes(route_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 5. route_packages Table
DROP TABLE IF EXISTS route_packages;
CREATE TABLE route_packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_id INT NOT NULL,
    package_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE,
    FOREIGN KEY (package_id) REFERENCES packages(package_id) ON DELETE CASCADE,
    UNIQUE KEY uq_route_package (route_id, package_id)
) ENGINE=InnoDB;

-- 6. delivery_updates Table
DROP TABLE IF EXISTS delivery_updates;
CREATE TABLE delivery_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    status ENUM('Pending','Out for Delivery','Delivered') NOT NULL,
    note TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (package_id) REFERENCES packages(package_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ==============================================
-- Indexes for faster queries
-- ==============================================

CREATE INDEX idx_routes_date ON routes(route_date);
CREATE INDEX idx_packages_status ON packages(status);
CREATE INDEX idx_delivery_updates_package ON delivery_updates(package_id);

-- ==============================================
-- Sample seed data (optional)
-- ==============================================

/* 

-- Users
INSERT INTO users (full_name, username, password_hash, role) VALUES
('Henry Moreno', 'henry', 'password_hash_here', 'manager'),
('John Dispatcher', 'john', 'password_hash_here', 'dispatcher'),
('Alice Driver', 'alice', 'password_hash_here', 'driver');

-- Drivers
INSERT INTO drivers (user_id, license_number, phone) VALUES
(3, 'DL123456', '09171234567');

-- Routes
INSERT INTO routes (route_name, route_date, driver_id, fuel_estimate) VALUES
('Route A', CURDATE(), 1, 50.00);

-- Packages
INSERT INTO packages (sender, recipient_name, recipient_address, phone, weight, category) VALUES
('Shop A', 'Customer A', '123 Street, City', '09170000000', 2.5, 'Electronics'),
('Shop B', 'Customer B', '456 Avenue, City', '09171111111', 1.2, 'Pharmacy');

-- Assign packages to route
INSERT INTO route_packages (route_id, package_id) VALUES
(1, 1),
(1, 2);

-- Delivery updates (optional)
INSERT INTO delivery_updates (package_id, status, note) VALUES
(1, 'Pending', 'Package registered'),
(2, 'Pending', 'Package registered');

 */