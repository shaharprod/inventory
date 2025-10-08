@echo off
echo ========================================
echo DEPLOYING TO GITHUB PAGES
echo ========================================

echo.
echo Step 1: Creating GitHub repository...
echo This will create a new repository on GitHub

echo.
echo Step 2: Pushing code to GitHub...
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main

echo.
echo Step 3: Setting up GitHub Pages...
echo Go to: https://github.com/your-username/inventory-system/settings/pages
echo Select "Deploy from a branch"
echo Select "main" branch
echo Click "Save"

echo.
echo ========================================
echo GITHUB PAGES DEPLOYMENT READY
echo ========================================
echo.
echo Your site will be available at:
echo https://your-username.github.io/inventory-system
echo.
echo Login: admin / admin123
echo.
pause
