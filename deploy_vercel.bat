@echo off
echo ========================================
echo DEPLOYING TO VERCEL
echo ========================================

echo.
echo Step 1: Installing Vercel CLI...
npm install -g vercel

echo.
echo Step 2: Logging in to Vercel...
vercel login

echo.
echo Step 3: Deploying to Vercel...
vercel --prod

echo.
echo ========================================
echo VERCEL DEPLOYMENT COMPLETED
echo ========================================
echo.
echo Your site will be available at:
echo https://your-project-name.vercel.app
echo.
echo Login: admin / admin123
echo.
echo Vercel is much simpler than Google Cloud!
echo.
pause
