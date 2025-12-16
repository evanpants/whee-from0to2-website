# Guide: Finding Images for from0to2.com

## Free Image Sources (No Attribution Required)

### 1. Unsplash (Recommended)
**Website**: https://unsplash.com
- High-quality, free photos
- No attribution required
- Search terms to use:

#### Hero Image (hero-bike.jpg)
- Search: "cargo bike", "electric cargo bike", "family cargo bike", "tern bike"
- Look for: Urban settings, families, NYC-like backgrounds
- **Suggested image**: The family cargo bike image you have is perfect!

#### TERN GSD (tern-gsd.jpg)
- Search: "tern gsd", "cargo bike", "longtail cargo bike"
- Look for: Side view of bike, professional product shots

#### TERN HSD (tern-hsd.jpg)
- Search: "tern hsd", "compact cargo bike", "urban cargo bike"
- Look for: Compact cargo bikes, city commuting

#### TERN Quick Haul (tern-quick-haul.jpg)
- Search: "tern quick haul", "small cargo bike", "compact cargo"
- Look for: Lightweight cargo bikes

#### Family Commute (family-commute.jpg)
- Search: "family bike", "cargo bike family", "kids on bike"
- Look for: Families riding together, kids in cargo area

#### Urban Delivery (urban-delivery.jpg)
- Search: "cargo bike delivery", "bike delivery", "urban cargo bike"
- Look for: Delivery workers, packages on bikes

#### City Commute (city-commute.jpg)
- Search: "bike commute", "urban cycling", "city bike"
- Look for: Commuters in urban settings

### 2. Pexels
**Website**: https://www.pexels.com
- Free stock photos
- Similar search terms as above

### 3. Pixabay
**Website**: https://pixabay.com
- Free images and vectors
- Good for bike product shots

## How to Download and Add Images

### Step 1: Download Images
1. Go to Unsplash.com (or Pexels/Pixabay)
2. Search for the terms above
3. Click on an image you like
4. Click "Download free" or the download button
5. Save to your Downloads folder

### Step 2: Rename Images
Rename downloaded images to match these exact names:
- `hero-bike.jpg` (or .png/.webp)
- `tern-gsd.jpg`
- `tern-hsd.jpg`
- `tern-quick-haul.jpg`
- `family-commute.jpg`
- `urban-delivery.jpg`
- `city-commute.jpg`

### Step 3: Move Images to Project
1. Open Finder
2. Navigate to: `/Users/evan/Documents/Cursor - Project 1/images/`
3. Drag and drop your renamed images into this folder

### Step 4: Commit to GitHub
```bash
cd "/Users/evan/Documents/Cursor - Project 1"
git add images/
git commit -m "Add website images"
git push
```

## Image Optimization Tips

Before uploading, optimize images:
1. **Resize if needed**: Aim for:
   - Hero: 1200x600px
   - Bike cards: 600x400px
   - Lifestyle: 600x400px

2. **Compress images**: Use free tools:
   - TinyPNG.com (for JPG/PNG)
   - Squoosh.app (for WebP)
   - ImageOptim (Mac app)

3. **File sizes**: Try to keep under 200KB per image for faster loading

## Quick Search Links

### Unsplash Direct Searches:
- [Cargo Bike](https://unsplash.com/s/photos/cargo-bike)
- [Electric Cargo Bike](https://unsplash.com/s/photos/electric-cargo-bike)
- [Family Bike](https://unsplash.com/s/photos/family-bike)
- [Bike Delivery](https://unsplash.com/s/photos/bike-delivery)
- [Urban Cycling](https://unsplash.com/s/photos/urban-cycling)

## Alternative: Use Placeholder Services

If you want to test the layout first, you can use placeholder images:
- Placeholder.com: `https://via.placeholder.com/1200x600`
- Placeholder.pics: `https://placeholder.pics/svg/1200x600`

But for production, use real images from Unsplash/Pexels.




