# Image Guide for from0to2.com

This guide explains where to add your images and what file names to use.

## Image Directory Structure

Create an `images` folder in your project root and add the following images:

```
/images
  ├── logo.svg (or logo.png)
  ├── hero-bike.jpg
  ├── tern-gsd.jpg
  ├── tern-hsd.jpg
  ├── tern-quick-haul.jpg
  ├── family-commute.jpg
  ├── urban-delivery.jpg
  └── city-commute.jpg
```

## Required Images

### 1. Logo
- **File**: `images/logo.svg` or `images/logo.png`
- **Location**: Navigation bar (top left)
- **Recommended size**: Height 40px, width auto
- **Format**: SVG (preferred) or PNG with transparent background

### 2. Hero Image
- **File**: `images/hero-bike.jpg`
- **Location**: Hero section (main banner)
- **Recommended size**: 1200x600px or larger
- **Format**: JPG or WebP
- **Content**: TERN cargo bike in NYC setting

### 3. Bike Product Images

#### TERN GSD
- **File**: `images/tern-gsd.jpg`
- **Location**: Bike showcase section
- **Recommended size**: 600x400px or larger
- **Format**: JPG or WebP

#### TERN HSD
- **File**: `images/tern-hsd.jpg`
- **Location**: Bike showcase section
- **Recommended size**: 600x400px or larger
- **Format**: JPG or WebP

#### TERN Quick Haul
- **File**: `images/tern-quick-haul.jpg`
- **Location**: Bike showcase section
- **Recommended size**: 600x400px or larger
- **Format**: JPG or WebP

### 4. Lifestyle Images

#### Family Commute
- **File**: `images/family-commute.jpg`
- **Location**: Lifestyle section
- **Recommended size**: 600x400px or larger
- **Format**: JPG or WebP
- **Content**: Family using cargo bike in NYC

#### Urban Delivery
- **File**: `images/urban-delivery.jpg`
- **Location**: Lifestyle section
- **Recommended size**: 600x400px or larger
- **Format**: JPG or WebP
- **Content**: Cargo bike used for deliveries

#### City Commute
- **File**: `images/city-commute.jpg`
- **Location**: Lifestyle section
- **Recommended size**: 600x400px or larger
- **Format**: JPG or WebP
- **Content**: Commuter using cargo bike in NYC

## Image Optimization Tips

1. **Compress images** before uploading:
   - Use tools like TinyPNG, Squoosh, or ImageOptim
   - Aim for file sizes under 200KB for web images

2. **Use appropriate formats**:
   - **JPG**: For photos with many colors
   - **PNG**: For logos and images with transparency
   - **WebP**: Best compression (modern browsers)
   - **SVG**: For logos and simple graphics

3. **Responsive images**:
   - The site automatically handles responsive sizing
   - Use high-resolution images (2x) for retina displays

## How to Add Images

1. Create the `images` folder in your project root:
   ```bash
   mkdir images
   ```

2. Add your images to the `images` folder with the exact file names listed above

3. Commit and push to GitHub:
   ```bash
   git add images/
   git commit -m "Add website images"
   git push
   ```

4. The images will automatically appear on your live site!

## Fallback Behavior

If an image is missing, the site will automatically show a styled placeholder with instructions. This helps you see what images are needed.

## Image Sources

You can source images from:
- TERN Bikes official website (with permission)
- Stock photo sites (Unsplash, Pexels, etc.)
- Professional photography
- Your own photos

Make sure you have proper rights to use all images!




