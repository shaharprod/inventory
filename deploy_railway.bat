@echo off
echo ========================================
echo DEPLOYING TO RAILWAY
echo ========================================

echo.
echo Step 1: Installing Railway CLI...
npm install -g @railway/cli

echo.
echo Step 2: Logging in to Railway...
railway login

echo.
echo Step 3: Creating new project...
railway init

echo.
echo Step 4: Deploying to Railway...
railway up

echo.
echo ========================================
echo RAILWAY DEPLOYMENT COMPLETED
echo ========================================
echo.
echo Your site will be available at:
echo https://your-project-name.railway.app
echo.
echo Login: admin / admin123
echo.
echo Railway is very simple and reliable!
echo.
pause
