"""
Test if crop images are available
"""

from pathlib import Path

IMAGES_DIR = Path("static/images/crops")
REQUIRED_CROPS = ['rice', 'wheat', 'maize', 'tomato', 'potato']

print("\n" + "="*60)
print("CROP IMAGES TEST")
print("="*60)

if not IMAGES_DIR.exists():
    print("\n❌ Images directory doesn't exist!")
    print(f"   Expected: {IMAGES_DIR.absolute()}")
    print("\n💡 Run: python create_placeholder_images.py")
else:
    images = list(IMAGES_DIR.glob("*.jpg")) + list(IMAGES_DIR.glob("*.png"))
    
    print(f"\n📊 Found {len(images)} images")
    
    if len(images) == 0:
        print("\n❌ No images found!")
        print("\n💡 Quick fix:")
        print("   1. Double-click: QUICK_ADD_IMAGES.bat")
        print("   2. Or run: python create_placeholder_images.py")
    else:
        print("\n✅ Images directory has files!")
        
        # Check for some key crops
        print("\nChecking key crops:")
        for crop in REQUIRED_CROPS:
            exists = (IMAGES_DIR / f"{crop}.jpg").exists()
            status = "✓" if exists else "✗"
            print(f"  {status} {crop}.jpg")
        
        if len(images) < 20:
            print(f"\n⚠️  Only {len(images)} images found")
            print("   You need 100+ for all crops")
            print("\n💡 Run: python download_crop_images.py")
        else:
            print(f"\n✅ Good! You have {len(images)} images")

print("\n" + "="*60)
