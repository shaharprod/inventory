@echo off
echo ========================================
echo SETTING UP GITHUB + GOOGLE CLOUD
echo ========================================

echo.
echo Step 1: Preparing files...
copy Dockerfile.github Dockerfile
copy app_github.yaml app.yaml

echo.
echo Step 2: Initializing Git...
git init
git add .
git commit -m "Initial commit - Inventory System"

echo.
echo Step 3: Creating GitHub repository...
echo Go to: https://github.com/new
echo Repository name: inventory-system
echo Description: Inventory Management System
echo Make it PUBLIC
echo Click "Create repository"

echo.
echo Step 4: Pushing to GitHub...
echo Replace YOUR_USERNAME with your GitHub username
echo git remote add origin https://github.com/YOUR_USERNAME/inventory-system.git
echo git branch -M main
echo git push -u origin main

echo.
echo Step 5: Setting up Google Cloud Build...
echo Go to: https://console.cloud.google.com/cloud-build/triggers
echo Click "Create Trigger"
echo Name: inventory-system-trigger
echo Source: GitHub
echo Repository: your-username/inventory-system
echo Branch: main
echo Build Configuration: Cloud Build configuration file
echo Location: /cloudbuild.yaml
echo Click "Create"

echo.
echo Step 6: Testing deployment...
echo Go to your GitHub repository
echo Make a small change (like adding a comment)
echo Commit and push
echo Watch the build in Google Cloud Console

echo.
echo ========================================
echo GITHUB + GOOGLE CLOUD SETUP COMPLETED
echo ========================================
echo.
echo Your site will be available at:
echo https://my-claude-drive.uc.r.appspot.com
echo.
echo Login: admin / admin123
echo.
echo Benefits of this method:
echo 1. Automatic deployment from GitHub
echo 2. No timeout issues
echo 3. Easy to update
echo 4. Version control
echo.
pause
