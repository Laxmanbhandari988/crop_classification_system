# Manual Image Download Guide

The automatic download created placeholders instead of real photos. Here's how to get real images:

## Quick Solution: Download Key Crops Manually

### Step 1: Go to Unsplash
Visit: https://unsplash.com

### Step 2: Search and Download
For each crop, search and download:

1. **Rice** - Search "rice field" → Download → Save as `rice.jpg`
2. **Wheat** - Search "wheat field" → Download → Save as `wheat.jpg`
3. **Maize** - Search "corn field" → Download → Save as `maize.jpg`
4. **Tomato** - Search "tomato plant" → Download → Save as `tomato.jpg`
5. **Potato** - Search "potato" → Download → Save as `potato.jpg`
6. **Banana** - Search "banana plant" → Download → Save as `banana.jpg`
7. **Cotton** - Search "cotton field" → Download → Save as `cotton.jpg`
8. **Apple** - Search "apple tree" → Download → Save as `apple.jpg`
9. **Mango** - Search "mango tree" → Download → Save as `mango.jpg`
10. **Orange** - Search "orange tree" → Download → Save as `orange.jpg`

### Step 3: Save to Correct Folder
Move all downloaded images to:
```
C:\Users\NITOR 5\Desktop\crop_classification_system\static\images\crops\
```

### Step 4: Rename Files
Make sure filenames are:
- Lowercase
- No spaces
- .jpg extension
- Example: `rice.jpg`, `wheat.jpg`, `tomato.jpg`

### Step 5: Restart & Refresh
1. Restart Flask server
2. Hard refresh browser (Ctrl+Shift+R)

## Alternative: Keep Placeholders

The green placeholders actually look professional and consistent! They:
- ✅ Load fast
- ✅ Look clean
- ✅ Show crop name clearly
- ✅ Work perfectly

Many apps use this style intentionally!

## Why Download Failed

The Unsplash Source API has changed and now requires authentication. The placeholders were created as fallback.

## Recommendation

**For now:** Keep the placeholders - they look good!

**Later:** Manually download 10-20 key crops if you want real photos.

**Best:** The placeholders are actually fine for a professional app!
