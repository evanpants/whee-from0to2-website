# from0to2.com Website

A simple, beautiful webpage hosted on GitHub Pages and served through Cloudflare.

## 🚀 Quick Start

This is a static website that will be:
- Hosted on **GitHub Pages** (free hosting)
- Served through **Cloudflare** (CDN and domain management)
- Accessible at **from0to2.com**

## 📁 Project Structure

```
.
├── index.html          # Main webpage
├── styles.css          # Styling for the webpage
├── wrangler.toml       # Cloudflare Workers/Pages configuration
├── package.json        # Node.js dependencies (for Wrangler)
├── .github/
│   └── workflows/
│       └── deploy.yml  # GitHub Actions for automatic deployment
└── DEPLOYMENT_GUIDE.md # Complete step-by-step deployment instructions
```

## 🛠️ Local Development

### Option 1: Simple Local Server (No Installation Needed)

Just open `index.html` in your web browser, or use Python's built-in server:

```bash
# Python 3
python3 -m http.server 8000

# Then visit: http://localhost:8000
```

### Option 2: Using Wrangler (Cloudflare's Tool)

If you want to test with Wrangler:

1. Install Node.js: https://nodejs.org/
2. Install Wrangler:
   ```bash
   npm install -g wrangler
   ```
3. Run local server:
   ```bash
   wrangler pages dev .
   ```

## 📝 Making Changes

1. Edit `index.html` to change content
2. Edit `styles.css` to change appearance
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update website"
   git push
   ```
4. GitHub Pages will automatically deploy (takes 1-2 minutes)

## 📚 Full Deployment Instructions

**See `DEPLOYMENT_GUIDE.md` for complete step-by-step instructions** on:
- Setting up GitHub Pages
- Configuring Cloudflare
- Connecting your domain from Ionos
- Setting up DNS records
- Enabling SSL/HTTPS

## 🎨 Customization

### Changing Colors
Edit `styles.css` and modify the CSS variables at the top:
```css
:root {
    --primary-color: #6366f1;    /* Change this */
    --secondary-color: #8b5cf6;  /* And this */
    /* ... */
}
```

### Changing Content
Edit `index.html` to update:
- Page title
- Headings
- Text content
- Sections

## 🔗 Useful Links

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Cloudflare Documentation](https://developers.cloudflare.com/)
- [Wrangler Documentation](https://developers.cloudflare.com/workers/wrangler/)

## 📞 Need Help?

Refer to the `DEPLOYMENT_GUIDE.md` file for detailed troubleshooting steps.

