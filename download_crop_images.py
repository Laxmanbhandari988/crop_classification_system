"""
Automatic Crop Image Downloader
Downloads images for all crops from free image sources
"""

import os
import requests
from pathlib import Path
import time

# Create images directory if it doesn't exist
IMAGES_DIR = Path("static/images/crops")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# List of all crops that need images
CROPS = [
    # Original 22 crops
    'rice', 'maize', 'jute', 'cotton', 'coconut', 'papaya', 'orange', 'apple',
    'muskmelon', 'watermelon', 'grapes', 'mango', 'banana', 'pomegranate',
    'lentil', 'blackgram', 'mungbean', 'mothbeans', 'pigeonpeas', 'kidneybeans',
    'chickpea', 'coffee',
    
    # Vegetables
    'tomato', 'potato', 'onion', 'cabbage', 'cauliflower', 'carrot', 'radish',
    'brinjal', 'okra', 'pumpkin', 'cucumber', 'bittergourd', 'bottlegourd',
    'spinach', 'lettuce', 'peas', 'greenbeans', 'chili', 'bellpepper', 'garlic',
    'beetroot', 'turnip', 'leek', 'celery', 'asparagus',
    
    # Fruits
    'pineapple', 'guava', 'strawberry', 'litchi', 'avocado', 'dragonfruit',
    'passionfruit', 'kiwi', 'peach', 'plum', 'cherry', 'fig', 'dates',
    'persimmon', 'mulberry',
    
    # Cereals
    'wheat', 'barley', 'sorghum', 'millet', 'oats', 'rye', 'quinoa',
    'amaranth', 'buckwheat',
    
    # Pulses
    'soybean', 'peanut', 'cowpea', 'fababean', 'limabean',
    
    # Cash crops & Spices
    'sugarcane', 'tea', 'turmeric', 'ginger', 'sunflower', 'mustard',
    'rubber', 'cardamom', 'blackpepper', 'coriander', 'cumin', 'fennel',
    'sesame', 'safflower', 'castor', 'linseed', 'niger',
    
    # Fiber
    'hemp',
    
    # Fodder
    'alfalfa', 'berseem', 'napiergrass'
]

def download_from_unsplash(crop_name):
    """Download image from Unsplash (free, high-quality images)"""
    try:
        # Unsplash Source API - provides random images
        url = f"https://source.unsplash.com/800x600/?{crop_name},crop,agriculture"
        
        response = requests.get(url, timeout=10, stream=True)
        if response.status_code == 200:
            filename = IMAGES_DIR / f"{crop_name}.jpg"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"  ⚠️  Unsplash failed: {e}")
    return False

def download_from_pixabay(crop_name, api_key=None):
    """Download from Pixabay (requires free API key)"""
    if not api_key:
        return False
    
    try:
        url = f"https://pixabay.com/api/?key={api_key}&q={crop_name}&image_type=photo&per_page=3"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['hits']:
                image_url = data['hits'][0]['webformatURL']
                img_response = requests.get(image_url, timeout=10, stream=True)
                
                if img_response.status_code == 200:
                    filename = IMAGES_DIR / f"{crop_name}.jpg"
                    with open(filename, 'wb') as f:
                        for chunk in img_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    return True
    except Exception as e:
        print(f"  ⚠️  Pixabay failed: {e}")
    return False

def create_placeholder_image(crop_name):
    """Create a simple placeholder SVG image"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple colored image with text
        img = Image.new('RGB', (800, 600), color=(76, 175, 80))
        draw = ImageDraw.Draw(img)
        
        # Add crop name text
        text = crop_name.upper()
        # Use default font
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((800 - text_width) // 2, (600 - text_height) // 2)
        
        draw.text(position, text, fill='white', font=font)
        
        filename = IMAGES_DIR / f"{crop_name}.jpg"
        img.save(filename, 'JPEG')
        return True
    except ImportError:
        print("  ⚠️  PIL not installed, skipping placeholder")
        return False

def download_all_images(use_pixabay=False, pixabay_key=None):
    """Download images for all crops"""
    print("="*60)
    print("🌾 CROP IMAGE DOWNLOADER")
    print("="*60)
    print(f"\nDownloading images for {len(CROPS)} crops...")
    print(f"Saving to: {IMAGES_DIR.absolute()}\n")
    
    success_count = 0
    failed_crops = []
    
    for i, crop in enumerate(CROPS, 1):
        # Check if image already exists
        existing_file = IMAGES_DIR / f"{crop}.jpg"
        if existing_file.exists():
            print(f"[{i}/{len(CROPS)}] ✓ {crop.ljust(20)} (already exists)")
            success_count += 1
            continue
        
        print(f"[{i}/{len(CROPS)}] ⬇️  {crop.ljust(20)}", end=" ")
        
        # Try Unsplash first (no API key needed)
        if download_from_unsplash(crop):
            print("✓ Downloaded")
            success_count += 1
            time.sleep(1)  # Be nice to the API
            continue
        
        # Try Pixabay if API key provided
        if use_pixabay and pixabay_key:
            if download_from_pixabay(crop, pixabay_key):
                print("✓ Downloaded (Pixabay)")
                success_count += 1
                time.sleep(1)
                continue
        
        # Create placeholder if download failed
        if create_placeholder_image(crop):
            print("⚠️  Placeholder created")
            success_count += 1
        else:
            print("❌ Failed")
            failed_crops.append(crop)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✓ Success: {success_count}/{len(CROPS)}")
    print(f"❌ Failed: {len(failed_crops)}")
    
    if failed_crops:
        print(f"\nFailed crops: {', '.join(failed_crops)}")
        print("\nYou can manually download images for these crops")
        print("and save them as: static/images/crops/[cropname].jpg")
    
    print("\n✅ Done! Restart your Flask app to see the images.")
    print("="*60)

def main():
    print("\n" + "="*60)
    print("CROP IMAGE DOWNLOADER")
    print("="*60)
    print("\nThis script will download images for all crops.")
    print("\nOptions:")
    print("1. Use Unsplash (free, no API key needed)")
    print("2. Use Pixabay (requires free API key)")
    print("3. Create placeholders only")
    print("\nRecommended: Option 1 (Unsplash)")
    
    choice = input("\nEnter choice (1-3) [1]: ").strip() or "1"
    
    if choice == "2":
        print("\nTo use Pixabay:")
        print("1. Go to https://pixabay.com/api/docs/")
        print("2. Sign up for free")
        print("3. Get your API key")
        api_key = input("\nEnter Pixabay API key: ").strip()
        if api_key:
            download_all_images(use_pixabay=True, pixabay_key=api_key)
        else:
            print("No API key provided, using Unsplash instead...")
            download_all_images()
    elif choice == "3":
        print("\nCreating placeholder images...")
        for crop in CROPS:
            create_placeholder_image(crop)
        print("✅ Placeholders created!")
    else:
        download_all_images()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
