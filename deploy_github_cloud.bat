@echo off
echo ========================================
echo DEPLOYING VIA GITHUB TO GOOGLE CLOUD
echo ========================================

echo.
echo Step 1: Creating GitHub repository...
echo Go to: https://github.com/new
echo Repository name: inventory-system
echo Make it PUBLIC
echo Click "Create repository"

echo.
echo Step 2: Pushing code to GitHub...
git init
git add .
git commit -m "Initial commit - Inventory System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/inventory-system.git
git push -u origin main

echo.
echo Step 3: Setting up Google Cloud Build...
echo Go to: https://console.cloud.google.com/cloud-build/triggers
echo Click "Create Trigger"
echo Source: GitHub
echo Repository: your-username/inventory-system
echo Branch: main
echo Build Configuration: Cloud Build configuration file
echo Location: /cloudbuild.yaml

echo.
echo Step 4: Creating cloudbuild.yaml...
echo This file will be created automatically

echo.
echo ========================================
echo GITHUB + GOOGLE CLOUD SETUP READY
echo ========================================
echo.
echo Your site will be available at:
echo https://my-claude-drive.uc.r.appspot.com
echo.
echo Login: admin / admin123
echo.
echo This method is much more reliable!
echo.
pause
