"""
Simple Placeholder Image Creator
Creates colored placeholder images for crops
"""

import os
from pathlib import Path

# Create directory
IMAGES_DIR = Path("static/images/crops")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Crop list
CROPS = [
    'rice', 'maize', 'jute', 'cotton', 'coconut', 'papaya', 'orange', 'apple',
    'muskmelon', 'watermelon', 'grapes', 'mango', 'banana', 'pomegranate',
    'lentil', 'blackgram', 'mungbean', 'mothbeans', 'pigeonpeas', 'kidneybeans',
    'chickpea', 'coffee', 'tomato', 'potato', 'onion', 'cabbage', 'cauliflower',
    'carrot', 'radish', 'brinjal', 'okra', 'pumpkin', 'cucumber', 'bittergourd',
    'bottlegourd', 'spinach', 'lettuce', 'peas', 'greenbeans', 'chili',
    'bellpepper', 'garlic', 'beetroot', 'turnip', 'wheat', 'barley', 'sorghum',
    'millet', 'oats', 'pineapple', 'guava', 'strawberry', 'litchi', 'avocado',
    'dragonfruit', 'kiwi', 'peach', 'plum', 'cherry', 'fig', 'dates',
    'soybean', 'peanut', 'sugarcane', 'tea', 'turmeric', 'ginger', 'sunflower',
    'mustard', 'rubber', 'cardamom', 'blackpepper', 'coriander', 'cumin',
    'fennel', 'sesame', 'safflower', 'castor', 'hemp', 'alfalfa', 'berseem'
]

try:
    from PIL import Image, ImageDraw, ImageFont
    
    print("Creating placeholder images...")
    colors = ['#4CAF50', '#8BC34A', '#CDDC39', '#FFC107', '#FF9800', '#FF5722']
    
    for i, crop in enumerate(CROPS):
        img = Image.new('RGB', (800, 600), color=colors[i % len(colors)])
        draw = ImageDraw.Draw(img)
        
        text = crop.upper().replace('_', ' ')
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((800-w)//2, (600-h)//2), text, fill='white', font=font)
        
        img.save(IMAGES_DIR / f"{crop}.jpg", 'JPEG')
        print(f"✓ {crop}")
    
    print(f"\n✅ Created {len(CROPS)} placeholder images!")
    
except ImportError:
    print("❌ PIL not installed. Install with: pip install Pillow")
