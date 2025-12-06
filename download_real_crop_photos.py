"""
Download REAL crop photos from Pexels
Requires free API key from https://www.pexels.com/api/
"""

import requests
from pathlib import Path
import time

# GET YOUR FREE API KEY FROM: https://www.pexels.com/api/
PEXELS_API_KEY = "YOUR_API_KEY_HERE"  # Replace this with your actual key

IMAGES_DIR = Path("static/images/crops")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Crop names with search terms for better results
CROPS = {
    'rice': 'rice paddy field',
    'wheat': 'wheat field golden',
    'maize': 'corn field agriculture',
    'tomato': 'tomato plant red',
    'potato': 'potato harvest',
    'onion': 'onion bulb',
    'banana': 'banana plantation',
    'cotton': 'cotton field white',
    'apple': 'apple orchard tree',
    'mango': 'mango tree fruit',
    'orange': 'orange tree citrus',
    'grapes': 'grape vineyard',
    'watermelon': 'watermelon field',
    'coconut': 'coconut palm tree',
    'coffee': 'coffee plantation beans',
    'tea': 'tea plantation leaves',
    'sugarcane': 'sugarcane field',
    'sunflower': 'sunflower field',
    'strawberry': 'strawberry plant',
    'pineapple': 'pineapple plant',
    'cabbage': 'cabbage field',
    'cauliflower': 'cauliflower vegetable',
    'carrot': 'carrot harvest',
    'cucumber': 'cucumber plant',
    'pumpkin': 'pumpkin field',
    'spinach': 'spinach leaves',
    'lettuce': 'lettuce field',
    'brinjal': 'eggplant plant',
    'okra': 'okra plant',
    'chili': 'chili pepper plant',
    'garlic': 'garlic bulb',
    'ginger': 'ginger root',
    'turmeric': 'turmeric root',
    'soybean': 'soybean field',
    'peanut': 'peanut plant',
    'chickpea': 'chickpea plant',
    'lentil': 'lentil plant',
    'peas': 'pea plant',
    'barley': 'barley field',
    'oats': 'oat field',
    'millet': 'millet grain',
    'sorghum': 'sorghum field',
    'papaya': 'papaya tree fruit',
    'guava': 'guava tree',
    'avocado': 'avocado tree',
    'kiwi': 'kiwi fruit vine',
    'peach': 'peach tree',
    'plum': 'plum tree',
    'cherry': 'cherry tree',
    'mustard': 'mustard field yellow',
    'sesame': 'sesame plant',
    'jute': 'jute plant fiber',
}

def download_from_pexels(crop_name, search_term):
    """Download real crop photo from Pexels"""
    
    if PEXELS_API_KEY == "YOUR_API_KEY_HERE":
        print("\n❌ ERROR: You need to add your Pexels API key!")
        print("\n📝 Steps to get API key:")
        print("   1. Go to: https://www.pexels.com/api/")
        print("   2. Click 'Get Started'")
        print("   3. Sign up (free)")
        print("   4. Copy your API key")
        print("   5. Paste it in this script at line 11")
        print("\n   Replace: PEXELS_API_KEY = 'YOUR_API_KEY_HERE'")
        print("   With:    PEXELS_API_KEY = 'your-actual-key-here'")
        return False
    
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={search_term}&per_page=1&orientation=landscape"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['photos']:
                # Get large image URL
                img_url = data['photos'][0]['src']['large']
                
                # Download image
                img_response = requests.get(img_url, timeout=15, stream=True)
                
                if img_response.status_code == 200:
                    filename = IMAGES_DIR / f"{crop_name}.jpg"
                    
                    with open(filename, 'wb') as f:
                        for chunk in img_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    file_size = filename.stat().st_size
                    return True, file_size
        
        return False, 0
    
    except Exception as e:
        return False, 0

def main():
    print("\n" + "="*70)
    print("DOWNLOADING REAL CROP PHOTOS FROM PEXELS")
    print("="*70)
    
    if PEXELS_API_KEY == "YOUR_API_KEY_HERE":
        print("\n❌ ERROR: API key not configured!")
        print("\n📝 To use this script:")
        print("   1. Go to: https://www.pexels.com/api/")
        print("   2. Sign up for free")
        print("   3. Get your API key")
        print("   4. Edit this file and replace 'YOUR_API_KEY_HERE' with your key")
        print("\n   It's on line 11 of this file.")
        print("="*70 + "\n")
        return
    
    print(f"\nDownloading {len(CROPS)} crop photos...")
    print("This will take 5-10 minutes...\n")
    
    success_count = 0
    failed_crops = []
    
    for i, (crop, search_term) in enumerate(CROPS.items(), 1):
        print(f"[{i:2d}/{len(CROPS)}] {crop:20s}", end=" ", flush=True)
        
        success, file_size = download_from_pexels(crop, search_term)
        
        if success:
            print(f"✓ ({file_size//1024}KB)")
            success_count += 1
        else:
            print("✗")
            failed_crops.append(crop)
        
        time.sleep(1)  # Respect API rate limits
    
    print("\n" + "="*70)
    print(f"✅ Downloaded: {success_count}/{len(CROPS)} real crop photos")
    
    if failed_crops:
        print(f"❌ Failed: {len(failed_crops)} crops")
    
    print("\n🎉 Done! Restart Flask and refresh browser to see real photos!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
