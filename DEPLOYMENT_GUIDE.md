# Complete Deployment Guide for from0to2.com

This guide will walk you through deploying your website to GitHub Pages and connecting it to your domain (from0to2.com) via Cloudflare.

## 📋 Prerequisites

- A GitHub account
- Your domain from0to2.com purchased on Ionos
- A Cloudflare account (free tier is fine)
- Git installed on your computer (we'll check this)

---

## Step 1: Initialize Git Repository (If Not Already Done)

### 1.1 Check if Git is Installed
Open Terminal (on Mac) or Command Prompt (on Windows) and type:
```bash
git --version
```

If you see a version number, you're good! If not, install Git from: https://git-scm.com/downloads

### 1.2 Initialize Git in Your Project
Navigate to your project folder in Terminal:
```bash
cd "/Users/evan/Documents/Cursor - Project 1"
```

Initialize git (if not already done):
```bash
git init
```

---

## Step 2: Create GitHub Repository

### 2.1 Create New Repository on GitHub
1. Go to https://github.com
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in:
   - **Repository name**: `from0to2-website` (or any name you like)
   - **Description**: "Website for from0to2.com"
   - **Visibility**: Choose **Public** (required for free GitHub Pages)
   - **DO NOT** check "Initialize with README" (we already have files)
5. Click **"Create repository"**

### 2.2 Connect Your Local Project to GitHub
After creating the repository, GitHub will show you commands. Run these in your Terminal:

```bash
# Add all files
git add .

# Commit the files
git commit -m "Initial commit: website for from0to2.com"

# Add the GitHub repository as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/from0to2-website.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: You'll be asked for your GitHub username and password (or personal access token).

---

## Step 3: Enable GitHub Pages

### 3.1 Configure GitHub Pages Settings
1. Go to your repository on GitHub
2. Click on **"Settings"** (top menu)
3. Scroll down to **"Pages"** in the left sidebar
4. Under **"Source"**, select:
   - **Branch**: `main`
   - **Folder**: `/ (root)`
5. Click **"Save"**

### 3.2 Wait for Deployment
- GitHub will show you a URL like: `https://YOUR_USERNAME.github.io/from0to2-website/`
- It may take 1-2 minutes for the site to be live
- You can check the deployment status under **"Actions"** tab

---

## Step 4: Set Up Cloudflare Account

### 4.1 Create Cloudflare Account
1. Go to https://www.cloudflare.com
2. Click **"Sign Up"** (it's free!)
3. Create an account with your email
4. Verify your email address

### 4.2 Add Your Domain to Cloudflare
1. Once logged in, click **"Add a Site"**
2. Enter your domain: `from0to2.com`
3. Click **"Add site"**
4. Select the **Free** plan (click "Continue with Free plan")
5. Cloudflare will scan your domain's DNS records

---

## Step 5: Update DNS Nameservers in Ionos

### 5.1 Get Cloudflare Nameservers
After adding your domain to Cloudflare, you'll see two nameservers that look like:
- `alice.ns.cloudflare.com`
- `bob.ns.cloudflare.com`

**Copy these nameservers** - you'll need them in the next step.

### 5.2 Update Nameservers in Ionos
1. Log in to your Ionos account: https://www.ionos.com
2. Go to **"Domains & SSL"** or **"Domain Management"**
3. Find your domain `from0to2.com` and click on it
4. Look for **"Nameservers"** or **"DNS Settings"**
5. Change from "Ionos Nameservers" to **"Custom Nameservers"**
6. Enter the two Cloudflare nameservers you copied:
   - First nameserver: `alice.ns.cloudflare.com` (or whatever Cloudflare gave you)
   - Second nameserver: `bob.ns.cloudflare.com` (or whatever Cloudflare gave you)
7. Click **"Save"** or **"Update"**

**Important**: DNS changes can take 24-48 hours to propagate, but usually happen within a few hours.

---

## Step 6: Configure DNS in Cloudflare

### 6.1 Add DNS Records
Once your nameservers are updated (Cloudflare will show "Active" status):

1. In Cloudflare dashboard, go to **"DNS"** > **"Records"**
2. You'll see some existing records - **keep the important ones** (like MX records for email if you use email)
3. Add a new record for your website:
   - **Type**: `CNAME`
   - **Name**: `@` (or `from0to2.com`)
   - **Target**: `YOUR_USERNAME.github.io` (replace with your actual GitHub username)
   - **Proxy status**: Click the orange cloud to make it **Proxied** (orange)
   - Click **"Save"**

4. Add another record for www:
   - **Type**: `CNAME`
   - **Name**: `www`
   - **Target**: `YOUR_USERNAME.github.io` (same as above)
   - **Proxy status**: **Proxied** (orange)
   - Click **"Save"**

### 6.2 Configure Page Rules (Optional but Recommended)
1. In Cloudflare, go to **"Rules"** > **"Page Rules"**
2. Click **"Create Page Rule"**
3. Set:
   - **URL**: `www.from0to2.com/*`
   - **Setting**: **Forwarding URL** (301 Permanent Redirect)
   - **Destination URL**: `https://from0to2.com/$1`
4. Click **"Save and Deploy"**

This ensures `www.from0to2.com` redirects to `from0to2.com`.

---

## Step 7: Configure Custom Domain in GitHub Pages

### 7.1 Add Custom Domain to GitHub
1. Go to your GitHub repository
2. Click **"Settings"** > **"Pages"**
3. Under **"Custom domain"**, enter: `from0to2.com`
4. Click **"Save"**

### 7.2 Add CNAME File (Alternative Method)
GitHub may create a `CNAME` file automatically. If not, create it:

1. In your repository, click **"Add file"** > **"Create new file"**
2. Name the file: `CNAME` (all caps, no extension)
3. In the file, type: `from0to2.com`
4. Click **"Commit new file"**

---

## Step 8: Enable SSL/HTTPS in Cloudflare

### 8.1 SSL/TLS Settings
1. In Cloudflare dashboard, go to **"SSL/TLS"**
2. Set encryption mode to **"Full"** (or **"Full (strict)"** if you have SSL on GitHub)
3. GitHub Pages automatically provides SSL, so **"Full"** should work

### 8.2 Always Use HTTPS
1. Go to **"SSL/TLS"** > **"Edge Certificates"**
2. Enable **"Always Use HTTPS"** (toggle it on)

---

## Step 9: Verify Everything Works

### 9.1 Check DNS Propagation
Visit: https://www.whatsmydns.net
- Enter your domain: `from0to2.com`
- Check if it shows Cloudflare's IP addresses

### 9.2 Test Your Website
1. Wait 10-30 minutes after completing all steps
2. Visit: `https://from0to2.com`
3. Your website should load!

---

## Step 10: Future Updates

Whenever you want to update your website:

1. Make changes to your files locally
2. In Terminal, run:
   ```bash
   git add .
   git commit -m "Update website"
   git push
   ```
3. GitHub Pages will automatically rebuild (takes 1-2 minutes)
4. Your changes will be live on from0to2.com!

---

## 🆘 Troubleshooting

### Website Not Loading?
1. **Check DNS**: Visit https://www.whatsmydns.net - make sure nameservers point to Cloudflare
2. **Check GitHub Pages**: Visit your GitHub Pages URL directly (YOUR_USERNAME.github.io/from0to2-website)
3. **Check Cloudflare Status**: Make sure domain shows "Active" in Cloudflare
4. **Wait**: DNS changes can take up to 48 hours (usually much faster)

### SSL Certificate Issues?
- Make sure "Always Use HTTPS" is enabled in Cloudflare
- Set SSL mode to "Full" (not "Flexible")
- Wait a few minutes for SSL to provision

### Can't Push to GitHub?
- Make sure you're authenticated: `git config --global user.name "Your Name"`
- Use a Personal Access Token instead of password: https://github.com/settings/tokens

### Need Help?
- GitHub Pages Docs: https://docs.github.com/en/pages
- Cloudflare Docs: https://developers.cloudflare.com/
- Check your repository's "Actions" tab for deployment errors

---

## ✅ Checklist

- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] GitHub Pages enabled
- [ ] Cloudflare account created
- [ ] Domain added to Cloudflare
- [ ] Nameservers updated in Ionos
- [ ] DNS records configured in Cloudflare
- [ ] Custom domain added in GitHub
- [ ] SSL/HTTPS enabled
- [ ] Website loads at from0to2.com

---

**Congratulations!** Your website should now be live at https://from0to2.com 🎉

