# Storage Images Setup Guide

## Required Images

The storage options page requires 4 images to be placed in the `images` folder:

1. **storage-1.jpg** - Modern bike storage units on urban street (three grey storage units)
2. **storage-2.jpg** - OONEE bike storage unit with planter (black cylindrical unit)
3. **storage-3.jpg** - Cargo e-bike next to storage unit (person with cargo bike)
4. **storage-4.jpg** - Indoor bicycle parking facility (concrete parking area)

## Supported File Formats

The code currently expects `.jpg` files, but you can use any of these formats:
- `.jpg` or `.jpeg` (recommended)
- `.png`
- `.webp`

## How to Add Images

1. Save your 4 storage images to the `images` folder in the project root
2. Name them exactly as listed above: `storage-1.jpg`, `storage-2.jpg`, `storage-3.jpg`, `storage-4.jpg`
3. If using different formats (e.g., `.png`), update the file extensions in `storage-options.html`:
   - Find all instances of `images/storage-X.jpg` and change to your format
   - Example: `images/storage-1.png`

## Current Status

The page is set up with:
- ✅ Lightbox functionality (click to enlarge)
- ✅ Close button (X) in top-right corner
- ✅ Click outside to close
- ✅ Responsive design
- ⚠️ Images need to be added to display properly

Once the images are added, they will automatically display and the lightbox will work when clicked.


