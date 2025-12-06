-- Extended Crops Database with 100+ crops for recommendation
-- All crops can be recommended based on conditions
-- Only popular crops shown in browse menu

USE crop_recommendation_db;

-- Add columns to distinguish browsing vs recommendation
ALTER TABLE crops ADD COLUMN IF NOT EXISTS show_in_browse BOOLEAN DEFAULT TRUE;
ALTER TABLE crops ADD COLUMN IF NOT EXISTS popularity_score INT DEFAULT 50;

-- Update existing crops
UPDATE crops SET show_in_browse = TRUE, popularity_score = 80;

-- Insert many more crops (all can be recommended)
INSERT INTO crops (name, description, ideal_temperature, ideal_humidity, ideal_ph, ideal_rainfall, growing_season, image_url, show_in_browse, popularity_score) VALUES

-- High-value vegetables (show in browse)
('Tomato', 'Versatile vegetable rich in lycopene and vitamins. Widely cultivated worldwide.', '20-30°C', '60-70%', '6.0-7.0', '600-1000', 'Year-round', 'tomato.jpg', TRUE, 95),
('Potato', 'Major tuber crop and staple food. Fourth most important food crop globally.', '15-25°C', '70-80%', '5.0-6.5', '500-700', 'Rabi (Oct-Mar)', 'potato.jpg', TRUE, 95),
('Onion', 'Essential bulb vegetable used in cuisines worldwide. High market demand.', '15-25°C', '60-70%', '6.0-7.0', '400-600', 'Rabi (Oct-Mar)', 'onion.jpg', TRUE, 90),
('Cabbage', 'Leafy vegetable rich in vitamins C and K. Cool-season crop.', '15-20°C', '60-70%', '6.0-7.5', '600-800', 'Winter (Oct-Mar)', 'cabbage.jpg', TRUE, 75),
('Cauliflower', 'Premium vegetable requiring consistent moisture and cool weather.', '15-20°C', '70-80%', '6.0-7.0', '600-800', 'Winter (Oct-Feb)', 'cauliflower.jpg', TRUE, 75),
('Carrot', 'Root vegetable high in beta-carotene. Grows best in loose, sandy soil.', '15-20°C', '60-70%', '6.0-7.0', '400-600', 'Winter (Oct-Mar)', 'carrot.jpg', TRUE, 80),
('Brinjal', 'Eggplant - warm-season vegetable with high nutritional value.', '22-30°C', '60-70%', '6.0-7.0', '600-1000', 'Year-round', 'brinjal.jpg', TRUE, 85),
('Okra', 'Ladyfinger - warm-season vegetable rich in fiber and antioxidants.', '25-35°C', '60-70%', '6.0-7.0', '600-1000', 'Summer (Mar-Jun)', 'okra.jpg', TRUE, 80),
('Chili Pepper', 'Spicy vegetable with high market value. Used fresh and dried.', '20-30°C', '60-70%', '6.0-7.0', '600-1000', 'Year-round', 'chili.jpg', TRUE, 90),
('Bell Pepper', 'Sweet pepper variety rich in vitamin C. Premium vegetable crop.', '20-30°C', '60-70%', '6.0-7.0', '600-1000', 'Year-round', 'bellpepper.jpg', TRUE, 70),

-- Additional vegetables (can be recommended, less prominent in browse)
('Radish', 'Fast-growing root vegetable. Ready in 25-30 days.', '15-25°C', '60-70%', '6.0-7.0', '400-600', 'Winter (Oct-Mar)', 'radish.jpg', FALSE, 60),
('Pumpkin', 'Large vine crop with nutritious fruits. Good for storage.', '20-30°C', '60-70%', '6.0-7.0', '500-800', 'Winter (Oct-Mar)', 'pumpkin.jpg', FALSE, 65),
('Cucumber', 'Refreshing vegetable crop. High water content.', '20-30°C', '60-70%', '6.0-7.0', '500-800', 'Summer (Mar-Jun)', 'cucumber.jpg', FALSE, 70),
('Bitter Gourd', 'Medicinal vegetable with anti-diabetic properties.', '25-35°C', '60-70%', '6.0-7.0', '600-1000', 'Summer (Mar-Jun)', 'bittergourd.jpg', FALSE, 55),
('Bottle Gourd', 'Climbing vegetable with light, nutritious fruits.', '25-35°C', '60-70%', '6.0-7.0', '600-1000', 'Summer (Mar-Jun)', 'bottlegourd.jpg', FALSE, 55),
('Spinach', 'Leafy green rich in iron. Fast-growing cool-season crop.', '15-25°C', '60-70%', '6.5-7.5', '400-600', 'Winter (Oct-Mar)', 'spinach.jpg', FALSE, 70),
('Lettuce', 'Salad crop requiring cool weather. Multiple varieties available.', '15-20°C', '60-70%', '6.0-7.0', '400-600', 'Winter (Oct-Mar)', 'lettuce.jpg', FALSE, 60),
('Peas', 'Cool-season legume rich in protein. Nitrogen-fixing crop.', '15-20°C', '60-70%', '6.0-7.0', '400-600', 'Winter (Oct-Mar)', 'peas.jpg', FALSE, 65),
('Green Beans', 'Warm-season legume with edible pods. Quick-growing.', '20-30°C', '60-70%', '6.0-7.0', '500-800', 'Year-round', 'greenbeans.jpg', FALSE, 65),
('Garlic', 'Bulb crop with medicinal properties. High market value.', '15-25°C', '60-70%', '6.0-7.0', '400-600', 'Rabi (Oct-Mar)', 'garlic.jpg', FALSE, 75),
('Beetroot', 'Root vegetable rich in folate and manganese.', '15-25°C', '60-70%', '6.0-7.5', '400-600', 'Winter (Oct-Mar)', 'beetroot.jpg', FALSE, 60),
('Turnip', 'Fast-growing root vegetable. Both roots and leaves edible.', '15-20°C', '60-70%', '6.0-7.0', '400-600', 'Winter (Oct-Mar)', 'turnip.jpg', FALSE, 50),
('Leek', 'Mild-flavored allium vegetable. Cool-season crop.', '15-25°C', '60-70%', '6.0-7.0', '400-600', 'Winter (Oct-Mar)', 'leek.jpg', FALSE, 45),
('Celery', 'Aromatic vegetable requiring consistent moisture.', '15-25°C', '70-80%', '6.0-7.0', '600-800', 'Winter (Oct-Mar)', 'celery.jpg', FALSE, 50),
('Asparagus', 'Perennial vegetable with high market value.', '15-25°C', '60-70%', '6.5-7.5', '500-800', 'Spring', 'asparagus.jpg', FALSE, 55),

-- Popular fruits (show in browse)
('Pineapple', 'Tropical fruit with sweet-tangy flavor. High vitamin C content.', '22-32°C', '70-80%', '5.5-6.5', '1000-1500', 'Year-round', 'pineapple.jpg', TRUE, 80),
('Guava', 'Tropical fruit extremely rich in vitamin C. Hardy and productive.', '23-28°C', '60-70%', '6.0-7.0', '1000-2000', 'Year-round', 'guava.jpg', TRUE, 85),
('Strawberry', 'Premium berry crop with high market value. Cool-season fruit.', '15-25°C', '60-70%', '5.5-6.5', '500-800', 'Winter (Oct-Mar)', 'strawberry.jpg', TRUE, 75),
('Litchi', 'Subtropical fruit with sweet, aromatic flesh. High demand.', '20-30°C', '70-80%', '6.0-7.0', '1200-1500', 'Summer (May-Jun)', 'litchi.jpg', TRUE, 70),

-- Additional fruits
('Avocado', 'Nutrient-dense fruit rich in healthy fats. Growing demand.', '20-30°C', '60-70%', '6.0-7.0', '1000-1500', 'Year-round', 'avocado.jpg', FALSE, 65),
('Dragon Fruit', 'Exotic cactus fruit. Drought-tolerant and profitable.', '25-35°C', '60-70%', '6.0-7.0', '500-1000', 'Year-round', 'dragonfruit.jpg', FALSE, 60),
('Passion Fruit', 'Tropical vine fruit with aromatic pulp. High juice content.', '20-30°C', '70-80%', '6.0-7.0', '1000-1500', 'Year-round', 'passionfruit.jpg', FALSE, 55),
('Kiwi', 'Temperate fruit rich in vitamin C. Requires support structure.', '15-25°C', '60-70%', '6.0-7.0', '1000-1500', 'Winter harvest', 'kiwi.jpg', FALSE, 50),
('Peach', 'Stone fruit requiring cold winters. Sweet and juicy.', '15-25°C', '60-70%', '6.0-7.0', '800-1200', 'Summer (May-Jul)', 'peach.jpg', FALSE, 60),
('Plum', 'Stone fruit with sweet to tart flavor. Multiple varieties.', '15-25°C', '60-70%', '6.0-7.0', '800-1200', 'Summer (May-Jul)', 'plum.jpg', FALSE, 55),
('Cherry', 'Premium stone fruit. Requires cold winters for dormancy.', '15-25°C', '60-70%', '6.0-7.5', '800-1200', 'Summer (May-Jun)', 'cherry.jpg', FALSE, 55),
('Fig', 'Drought-tolerant fruit. Sweet and nutritious.', '20-30°C', '50-60%', '6.0-7.5', '500-800', 'Summer-Autumn', 'fig.jpg', FALSE, 50),
('Dates', 'Desert fruit requiring hot, dry climate. High sugar content.', '25-40°C', '40-50%', '7.0-8.0', '200-400', 'Summer harvest', 'dates.jpg', FALSE, 60),
('Persimmon', 'Sweet fruit for temperate regions. Rich in vitamins.', '15-25°C', '60-70%', '6.0-7.0', '800-1200', 'Autumn', 'persimmon.jpg', FALSE, 45),
('Mulberry', 'Fast-growing fruit tree. Fruits used fresh or dried.', '20-30°C', '60-70%', '6.0-7.0', '800-1200', 'Summer', 'mulberry.jpg', FALSE, 50),

-- Major cereals (show in browse)
('Wheat', 'Major cereal crop and staple food. Second most produced grain globally.', '15-25°C', '60-70%', '6.0-7.5', '400-600', 'Rabi (Nov-Apr)', 'wheat.jpg', TRUE, 95),
('Barley', 'Versatile cereal for food, feed, and brewing. Drought-tolerant.', '15-20°C', '60-70%', '6.0-7.5', '400-600', 'Rabi (Nov-Apr)', 'barley.jpg', TRUE, 70),
('Sorghum', 'Drought-tolerant cereal for semi-arid regions. Gluten-free grain.', '25-35°C', '50-60%', '6.0-7.5', '400-600', 'Kharif (Jun-Oct)', 'sorghum.jpg', TRUE, 75),
('Millet', 'Small-seeded cereal with high nutritional value. Climate-resilient.', '25-35°C', '50-60%', '6.0-7.5', '400-600', 'Kharif (Jun-Oct)', 'millet.jpg', TRUE, 75),

-- Additional cereals
('Oats', 'Nutritious cereal rich in fiber. Cool-season crop.', '15-25°C', '60-70%', '6.0-7.0', '500-800', 'Rabi (Oct-Mar)', 'oats.jpg', FALSE, 65),
('Rye', 'Hardy cereal tolerant to poor soils. Used for bread and feed.', '10-20°C', '60-70%', '5.5-7.0', '400-600', 'Rabi (Oct-Apr)', 'rye.jpg', FALSE, 50),
('Quinoa', 'Protein-rich pseudo-cereal. Gluten-free superfood.', '15-25°C', '60-70%', '6.0-7.5', '400-600', 'Cool season', 'quinoa.jpg', FALSE, 60),
('Amaranth', 'Ancient grain with complete protein. Drought-tolerant.', '20-30°C', '60-70%', '6.0-7.0', '400-600', 'Warm season', 'amaranth.jpg', FALSE, 50),
('Buckwheat', 'Pseudo-cereal with short growing season. Gluten-free.', '15-25°C', '60-70%', '6.0-7.0', '400-600', 'Cool season', 'buckwheat.jpg', FALSE, 50),

-- Major pulses (show in browse)
('Soybean', 'Major oilseed and protein crop. Nitrogen-fixing legume.', '20-30°C', '60-70%', '6.0-7.0', '600-1000', 'Kharif (Jun-Oct)', 'soybean.jpg', TRUE, 90),
('Peanut', 'Groundnut - oilseed legume with high protein. Versatile crop.', '25-35°C', '60-70%', '6.0-7.0', '500-800', 'Kharif (Jun-Oct)', 'peanut.jpg', TRUE, 85),

-- Additional pulses
('Cowpea', 'Drought-tolerant pulse for marginal lands. Quick-growing.', '25-35°C', '60-70%', '6.0-7.0', '500-800', 'Kharif (Jun-Sep)', 'cowpea.jpg', FALSE, 60),
('Faba Bean', 'Broad bean - cool-season pulse rich in protein.', '15-25°C', '60-70%', '6.0-7.5', '400-600', 'Rabi (Oct-Mar)', 'fababean.jpg', FALSE, 55),
('Lima Bean', 'Butter bean - warm-season pulse with large seeds.', '20-30°C', '60-70%', '6.0-7.0', '500-800', 'Warm season', 'limabean.jpg', FALSE, 50),

-- Cash crops & spices (show popular ones)
('Sugarcane', 'Major cash crop for sugar production. High water requirement.', '20-35°C', '70-80%', '6.0-7.5', '1500-2500', 'Year-round', 'sugarcane.jpg', TRUE, 90),
('Tea', 'Plantation crop for beverage. Requires acidic soil and high rainfall.', '20-30°C', '70-90%', '4.5-5.5', '1500-3000', 'Year-round', 'tea.jpg', TRUE, 80),
('Turmeric', 'Rhizome spice with medicinal properties. High market value.', '20-30°C', '70-80%', '6.0-7.5', '1500-2500', 'Kharif (Jun-Mar)', 'turmeric.jpg', TRUE, 85),
('Ginger', 'Rhizome spice crop. Requires warm, humid climate.', '20-30°C', '70-80%', '6.0-7.0', '1500-3000', 'Kharif (Jun-Mar)', 'ginger.jpg', TRUE, 85),
('Sunflower', 'Oilseed crop with large, showy flowers. Drought-tolerant.', '20-30°C', '60-70%', '6.0-7.5', '500-800', 'Kharif & Rabi', 'sunflower.jpg', TRUE, 80),
('Mustard', 'Oilseed crop with pungent seeds. Cool-season crop.', '15-25°C', '60-70%', '6.0-7.5', '400-600', 'Rabi (Oct-Mar)', 'mustard.jpg', TRUE, 75),

-- Additional spices and cash crops
('Rubber', 'Plantation crop for latex production. Tropical regions only.', '25-35°C', '75-85%', '5.0-6.0', '2000-3000', 'Year-round', 'rubber.jpg', FALSE, 70),
('Cardamom', 'High-value spice grown in shade. Requires high rainfall.', '10-25°C', '70-80%', '5.0-6.5', '1500-4000', 'Year-round', 'cardamom.jpg', FALSE, 75),
('Black Pepper', 'Climbing spice crop. King of spices.', '20-30°C', '70-80%', '5.5-6.5', '2000-3000', 'Year-round', 'blackpepper.jpg', FALSE, 75),
('Coriander', 'Aromatic herb used as spice and garnish. Quick-growing.', '15-25°C', '60-70%', '6.5-7.5', '400-600', 'Rabi (Oct-Mar)', 'coriander.jpg', FALSE, 70),
('Cumin', 'Spice crop for cool, dry climate. High market value.', '15-25°C', '50-60%', '6.5-8.0', '300-500', 'Rabi (Nov-Mar)', 'cumin.jpg', FALSE, 65),
('Fennel', 'Aromatic crop used as spice and vegetable.', '15-25°C', '60-70%', '6.5-8.0', '400-600', 'Rabi (Oct-Mar)', 'fennel.jpg', FALSE, 60),
('Sesame', 'Ancient oilseed crop. Drought-tolerant.', '25-35°C', '50-60%', '6.0-7.5', '400-600', 'Kharif (Jun-Oct)', 'sesame.jpg', FALSE, 70),
('Safflower', 'Oilseed crop for dry regions. Deep-rooted.', '20-30°C', '50-60%', '6.0-7.5', '400-600', 'Rabi (Oct-Mar)', 'safflower.jpg', FALSE, 60),
('Castor', 'Industrial oilseed crop. Drought-tolerant.', '20-30°C', '60-70%', '6.0-7.5', '500-800', 'Kharif (Jun-Oct)', 'castor.jpg', FALSE, 60),
('Linseed', 'Flax oilseed crop. Cool-season crop.', '15-25°C', '60-70%', '6.0-7.5', '500-800', 'Rabi (Oct-Mar)', 'linseed.jpg', FALSE, 55),
('Niger', 'Oilseed crop for marginal lands. Drought-tolerant.', '20-30°C', '60-70%', '6.0-7.0', '500-800', 'Kharif (Jun-Oct)', 'niger.jpg', FALSE, 50),

-- Fiber crops
('Jute', 'Golden fiber crop. Requires warm, humid climate.', '24-37°C', '70-90%', '6.0-7.5', '1500-2000', 'Mar-Jun', 'jute.jpg', TRUE, 70),
('Cotton', 'Major fiber crop. Requires warm climate and moderate rainfall.', '21-30°C', '50-70%', '6.0-8.0', '500-1000', 'Kharif (Apr-Oct)', 'cotton.jpg', TRUE, 85),
('Hemp', 'Versatile fiber crop with multiple uses. Fast-growing.', '15-25°C', '60-70%', '6.0-7.5', '500-800', 'Kharif (Jun-Oct)', 'hemp.jpg', FALSE, 50),

-- Fodder crops
('Alfalfa', 'High-protein perennial fodder. Nitrogen-fixing.', '15-25°C', '60-70%', '6.5-7.5', '500-800', 'Year-round', 'alfalfa.jpg', FALSE, 55),
('Berseem', 'Winter fodder crop rich in protein. Quick-growing.', '15-25°C', '60-70%', '6.5-7.5', '400-600', 'Rabi (Oct-Apr)', 'berseem.jpg', FALSE, 55),
('Napier Grass', 'Perennial fodder grass. High biomass production.', '25-35°C', '60-70%', '6.0-7.0', '800-1200', 'Year-round', 'napiergrass.jpg', FALSE, 50);

-- Update original 22 crops to have high popularity
UPDATE crops SET popularity_score = 90, show_in_browse = TRUE WHERE name IN (
    'Rice', 'Maize', 'Coconut', 'Papaya', 'Orange', 'Apple',
    'Muskmelon', 'Watermelon', 'Grapes', 'Mango', 'Banana', 'Pomegranate',
    'Lentil', 'Blackgram', 'Mungbean', 'Mothbeans', 'Pigeonpeas', 'Kidneybeans',
    'Chickpea', 'Coffee'
);
