-- Create Database
CREATE DATABASE IF NOT EXISTS crop_recommendation_db;
USE crop_recommendation_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crops Information Table
CREATE TABLE IF NOT EXISTS crops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    ideal_temperature VARCHAR(50),
    ideal_humidity VARCHAR(50),
    ideal_ph VARCHAR(50),
    ideal_rainfall VARCHAR(50),
    growing_season VARCHAR(100),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions History Table
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    nitrogen FLOAT NOT NULL,
    phosphorus FLOAT NOT NULL,
    potassium FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    ph FLOAT NOT NULL,
    rainfall FLOAT NOT NULL,
    predicted_crop VARCHAR(50) NOT NULL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert Crop Information
INSERT INTO crops (name, description, ideal_temperature, ideal_humidity, ideal_ph, ideal_rainfall, growing_season, image_url) VALUES
('Rice', 'Rice is a staple food crop grown in flooded fields. Requires high water availability and warm climate.', '20-35°C', '80-90%', '5.5-7.0', '1500-2000mm', 'Kharif (June-November)', 'rice.jpg'),
('Maize', 'Maize or corn is a versatile cereal crop used for food, feed, and industrial purposes.', '18-27°C', '60-70%', '5.5-7.5', '500-800mm', 'Kharif & Rabi', 'maize.jpg'),
('Jute', 'Jute is a fiber crop grown in warm, humid climates. Known as the golden fiber.', '24-37°C', '70-90%', '6.0-7.5', '1500-2000mm', 'March-June', 'jute.jpg'),
('Cotton', 'Cotton is a major fiber crop requiring warm climate and moderate rainfall.', '21-30°C', '50-70%', '6.0-8.0', '500-1000mm', 'Kharif (April-October)', 'cotton.jpg'),
('Coconut', 'Coconut palm thrives in tropical coastal regions with high rainfall and humidity.', '27-32°C', '70-80%', '5.5-7.0', '1500-2500mm', 'Year-round', 'coconut.jpg'),
('Papaya', 'Papaya is a tropical fruit crop that grows year-round in warm climates.', '22-32°C', '60-80%', '6.0-7.0', '1000-2000mm', 'Year-round', 'papaya.jpg'),
('Orange', 'Orange is a citrus fruit crop requiring subtropical to tropical climate.', '15-30°C', '60-70%', '6.0-7.5', '1000-1500mm', 'Winter harvest', 'orange.jpg'),
('Apple', 'Apple requires temperate climate with cold winters for proper fruit development.', '15-25°C', '60-70%', '5.5-7.0', '1000-1200mm', 'Summer-Autumn', 'apple.jpg'),
('Muskmelon', 'Muskmelon is a summer fruit crop requiring warm weather and moderate water.', '25-35°C', '60-70%', '6.0-7.0', '400-600mm', 'Summer (March-June)', 'muskmelon.jpg'),
('Watermelon', 'Watermelon thrives in hot weather with plenty of sunshine and moderate rainfall.', '25-35°C', '60-70%', '6.0-7.0', '400-600mm', 'Summer (March-June)', 'watermelon.jpg'),
('Grapes', 'Grapes require warm, dry climate during growing season and cool winters.', '15-30°C', '60-70%', '6.0-7.5', '500-900mm', 'Winter-Spring', 'grapes.jpg'),
('Mango', 'Mango is the king of fruits, requiring tropical to subtropical climate.', '24-30°C', '60-70%', '5.5-7.5', '750-2500mm', 'Summer (March-June)', 'mango.jpg'),
('Banana', 'Banana requires warm, humid tropical climate with consistent moisture.', '25-35°C', '75-85%', '6.0-7.5', '1500-3000mm', 'Year-round', 'banana.jpg'),
('Pomegranate', 'Pomegranate adapts to semi-arid climate and requires hot, dry summers.', '25-35°C', '50-60%', '6.5-7.5', '500-700mm', 'Winter harvest', 'pomegranate.jpg'),
('Lentil', 'Lentil is a pulse crop grown in cool season, requiring moderate rainfall.', '18-25°C', '60-70%', '6.0-7.5', '400-600mm', 'Rabi (October-March)', 'lentil.jpg'),
('Blackgram', 'Blackgram is a protein-rich pulse crop suitable for various climatic conditions.', '25-35°C', '60-70%', '6.5-7.5', '600-1000mm', 'Kharif & Rabi', 'blackgram.jpg'),
('Mungbean', 'Mungbean is a short-duration pulse crop with high nutritional value.', '25-35°C', '60-70%', '6.5-7.5', '600-1000mm', 'Kharif (June-September)', 'mungbean.jpg'),
('Mothbeans', 'Mothbeans are drought-resistant pulse crops suitable for arid regions.', '25-35°C', '50-60%', '7.0-8.0', '300-500mm', 'Kharif (July-October)', 'mothbeans.jpg'),
('Pigeonpeas', 'Pigeonpeas are perennial pulse crops with deep root system for drought tolerance.', '20-30°C', '60-70%', '6.0-7.5', '600-1000mm', 'Kharif (June-March)', 'pigeonpeas.jpg'),
('Kidneybeans', 'Kidneybeans are popular pulse crops requiring cool climate and moderate water.', '15-25°C', '60-70%', '6.0-7.0', '500-800mm', 'Rabi (October-March)', 'kidneybeans.jpg'),
('Chickpea', 'Chickpea is a major pulse crop grown in cool, dry season with moderate rainfall.', '20-30°C', '60-70%', '6.0-7.5', '400-600mm', 'Rabi (October-March)', 'chickpea.jpg'),
('Coffee', 'Coffee requires tropical highland climate with well-distributed rainfall.', '15-28°C', '70-80%', '6.0-6.5', '1500-2500mm', 'Year-round', 'coffee.jpg');
