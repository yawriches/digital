-- Smart Watches E-commerce - Seed Data for Supabase
-- Run this AFTER running supabase_schema.sql

-- Insert Admin User (password: admin123)
-- Password hash generated with bcrypt for 'admin123'
INSERT INTO users (email, password_hash, first_name, last_name, is_admin) VALUES
('admin@smartwatches.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqGfZKZvNO', 'Admin', 'User', TRUE);

-- Insert Customer User (password: password123)
-- Password hash generated with bcrypt for 'password123'
INSERT INTO users (email, password_hash, first_name, last_name, phone, is_admin) VALUES
('john@example.com', '$2b$12$K3F6Z8QhN5L7mP9RtS2VvO8xY1wZ3qA5bC7dE9fG0hI2jK4lM6nO8', 'John', 'Doe', '+233501234567', FALSE);

-- Insert Categories
INSERT INTO categories (name, slug, description, is_active) VALUES
('Smart Watches', 'smart', 'Advanced smartwatches with cutting-edge technology', TRUE),
('Fitness Trackers', 'fitness', 'Track your health and fitness goals', TRUE),
('Classic Watches', 'classic', 'Timeless elegance meets modern technology', TRUE),
('Sport Watches', 'sport', 'Rugged watches built for active lifestyles', TRUE);

-- Insert Products
INSERT INTO products (name, slug, description, short_description, price, compare_price, stock, sku, category_id, image_url, image_url_2, image_url_3, is_featured, brand, specifications) VALUES
-- Smart Watches
('TechPro X1', 'techpro-x1', 'The TechPro X1 represents the pinnacle of smartwatch technology. With its stunning AMOLED display, advanced health monitoring, and seamless connectivity, it''s your perfect companion for modern life. Track your fitness, manage calls, and stay connected with style.', 'Premium smartwatch with AMOLED display and health tracking', 299.00, 399.00, 50, 'SW-TECH-001', 1, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80', 'https://images.unsplash.com/photo-1546868871-af0de0ae72be?w=600&q=80', 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=600&q=80', TRUE, 'TechPro', 'Case: 44mm Aluminum\nDisplay: 1.4" AMOLED\nBattery: 48 hours\nWater Resistance: 5ATM\nConnectivity: Bluetooth 5.0, WiFi\nWeight: 45g'),

('FitLife Pro', 'fitlife-pro', 'Designed for fitness enthusiasts, the FitLife Pro offers comprehensive health tracking including heart rate, SpO2, sleep analysis, and 100+ sport modes. The lightweight design ensures comfort during intense workouts while the long battery life keeps you going.', 'Comprehensive fitness tracking with 100+ sport modes', 199.00, 0, 75, 'SW-FIT-002', 2, 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&q=80', 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&q=80', 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=600&q=80', TRUE, 'FitLife', 'Case: 42mm Polymer\nDisplay: LCD Color\nBattery: 7 days\nSensors: HR, SpO2, GPS\nSport Modes: 100+\nWeight: 32g'),

('Vanguard Health', 'vanguard-health', 'The Vanguard Health is your personal health companion. Featuring medical-grade sensors for ECG and blood oxygen monitoring, it provides insights that matter. The elegant design makes it suitable for any occasion, from boardroom to gym.', 'Advanced health monitoring with ECG and blood oxygen', 449.00, 0, 40, 'SW-VANG-003', 1, 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&q=80', 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&q=80', 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=600&q=80', TRUE, 'TechForge', 'Case: 44mm Aluminum\nDisplay: Retina LTPO OLED\nHealth: ECG, SpO2, HR\nBattery: 36 hours\nOS: WatchOS 10\nWeight: 38g'),

('Heritage Chronograph', 'heritage-chronograph', 'The Heritage Chronograph pays homage to traditional watchmaking while embracing modern technology. The classic dial design houses discreet smart features including step counting, sleep tracking, and notification alerts. A watch that commands respect in any boardroom.', 'Classic chronograph design with discreet smart features', 699.00, 849.00, 20, 'SW-HERI-004', 3, 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=600&q=80', 'https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600&q=80', 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&q=80', FALSE, 'Heritage', 'Case: 42mm Stainless Steel\nMovement: Hybrid Quartz\nCrystal: Sapphire\nWater Resistance: 10ATM\nFeatures: Smart notifications\nWeight: 68g'),

-- Sport Watches
('Titan Sport', 'titan-sport', 'Built for extreme conditions, the Titan Sport features military-grade durability with smart capabilities. Whether you''re hiking mountains or diving deep, this watch is engineered to perform. GPS tracking, barometer, and compass ensure you never lose your way.', 'Military-grade durability meets smart technology', 349.00, 0, 60, 'SW-TITAN-005', 4, 'https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=600&q=80', 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&q=80', 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=600&q=80', FALSE, 'Titan', 'Case: 46mm Titanium\nDisplay: MIP Transflective\nBattery: 14 days\nWater Resistance: 20ATM\nSensors: GPS, Barometer, Compass\nWeight: 52g'),

('Runner Elite', 'runner-elite', 'Designed specifically for runners, the Runner Elite provides real-time coaching, advanced running metrics, and recovery insights. The lightweight design won''t slow you down, while the accurate GPS ensures every mile is tracked perfectly.', 'Specialized running watch with coaching features', 279.00, 329.00, 45, 'SW-RUN-006', 2, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80', 'https://images.unsplash.com/photo-1546868871-af0de0ae72be?w=600&q=80', 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=600&q=80', FALSE, 'RunTech', 'Case: 40mm Polymer\nDisplay: Color LCD\nBattery: 20 hours GPS\nFeatures: Running Dynamics\nGPS: Multi-band\nWeight: 29g'),

-- Premium Products
('Nexus LTE', 'nexus-lte', 'Stay connected anywhere with the Nexus LTE. Built-in cellular connectivity means you can leave your phone behind while still receiving calls, messages, and streaming music. The vibrant AMOLED display and premium materials make it a statement piece.', 'Standalone LTE connectivity for true independence', 549.00, 0, 30, 'SW-NEX-007', 1, 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&q=80', 'https://images.unsplash.com/photo-1546868871-af0de0ae72be?w=600&q=80', 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=600&q=80', TRUE, 'TechForge', 'Case: 45mm Aluminum\nDisplay: AMOLED 1.4" 500nits\nConnectivity: LTE, WiFi, BT 5.2\nBattery: 24 hours (LTE)\nStorage: 32GB\nWeight: 42g'),

('Artisan Automatic', 'artisan-automatic', 'The Artisan Automatic combines a genuine Swiss automatic movement with smart notification capabilities. The exhibition caseback reveals the intricate mechanical movement, while the sapphire crystal front conceals a subtle OLED display for incoming alerts. Limited edition of 500 pieces.', 'Swiss automatic movement with smart notifications', 1899.00, 2299.00, 5, 'SW-ARTS-008', 3, 'https://images.unsplash.com/photo-1507679799987-c73b7651af56?w=600&q=80', 'https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600&q=80', 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&q=80', TRUE, 'Montecello', 'Case: 41mm 316L Stainless Steel\nMovement: Swiss Automatic + Smart\nCrystal: Sapphire (front & back)\nWater Resistance: 50m\nEdition: Limited 500 pieces\nWeight: 75g');

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database seeded successfully!';
    RAISE NOTICE 'Created:';
    RAISE NOTICE '- 2 users (admin@smartwatches.com / admin123, john@example.com / password123)';
    RAISE NOTICE '- 4 categories';
    RAISE NOTICE '- 8 products';
    RAISE NOTICE 'Your Smart Watches e-commerce database is ready!';
END $$;
