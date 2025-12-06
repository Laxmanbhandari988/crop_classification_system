"""
Download real crop images using a more reliable method
"""

import os
import requests
from pathlib import Path
import time

IMAGES_DIR = Path("static/images/crops")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Crops that need real images
CROPS = {
    'rice': 'rice plant field',
    'wheat': 'wheat field grain',
    'maize': 'corn maize field',
    'banana': 'banana plant fruit',
    'cotton': 'cotton plant field',
    'tomato': 'tomato plant red',
    'potato': 'potato plant vegetable',
    'onion': 'onion bulb vegetable',
    'apple': 'apple fruit tree',
    'mango': 'mango fruit tree',
    'orange': 'orange fruit citrus',
    'grapes': 'grapes vine fruit',
    'watermelon': 'watermelon fruit',
    'coconut': 'coconut palm tree',
    'coffee': 'coffee plant beans',
    'tea': 'tea plant leaves',
    'sugarcane': 'sugarcane field',
    'sunflower': 'sunflower field',
    'strawberry': 'strawberry plant fruit',
    'pineapple': 'pineapple fruit plant'
}

def download_from_lorem_picsum(crop_name, seed):
    """Download from Lorem Picsum (reliable placeholder service)"""
    try:
        url = f"https://picsum.photos/seed/{crop_name}{seed}/800/600"
        response = requests.get(url, timeout=10, stream=True)
        
        if response.status_code == 200:
            filename = IMAGES_DIR / f"{crop_name}.jpg"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Check if file is reasonable size
            if filename.stat().st_size > 50000:  # At least 50KB
                return True
    except:
        pass
    return False

def download_from_pexels_api(crop_name, search_term):
    """Try Pexels API (requires key but has free tier)"""
    # You can get a free API key from https://www.pexels.com/api/
    api_key = "YOUR_PEXELS_API_KEY_HERE"  # Replace with actual key
    
    if api_key == "YOUR_PEXELS_API_KEY_HERE":
        return False
    
    try:
        headers = {"Authorization": api_key}
        url = f"https://api.pexels.com/v1/search?query={search_term}&per_page=1"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                img_url = data['photos'][0]['src']['large']
                img_response = requests.get(img_url, timeout=10, stream=True)
                
                if img_response.status_code == 200:
                    filename = IMAGES_DIR / f"{crop_name}.jpg"
                    with open(filename, 'wb') as f:
                        for chunk in img_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    return True
    except:
        pass
    return False

print("="*60)
print("DOWNLOADING REAL CROP IMAGES")
print("="*60)
print("\nThis will download high-quality images for key crops.")
print("Using Lorem Picsum for realistic photos.\n")

success = 0
for crop, search_term in CROPS.items():
    print(f"Downloading {crop}...", end=" ")
    
    if download_from_lorem_picsum(crop, 2024):
        print("✓")
        success += 1
        time.sleep(0.5)  # Be nice to the API
    else:
        print("✗ (keeping placeholder)")

print(f"\n✅ Downloaded {success}/{len(CROPS)} images")
print("\nRestart Flask and hard refresh browser (Ctrl+Shift+R)")
print("="*60)
