@echo off
echo ========================================
echo DEPLOYING TO RENDER
echo ========================================

echo.
echo Step 1: Go to https://render.com
echo Step 2: Sign up with GitHub
echo Step 3: Connect your GitHub repository
echo Step 4: Select "Web Service"
echo Step 5: Use these settings:
echo.
echo Build Command: pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
echo Start Command: gunicorn inventory_project.wsgi:application --bind 0.0.0.0:$PORT
echo.
echo Environment Variables:
echo DJANGO_SETTINGS_MODULE=inventory_project.settings_appengine
echo DEBUG=False
echo ALLOWED_HOSTS=*
echo.
echo ========================================
echo RENDER DEPLOYMENT READY
echo ========================================
echo.
echo Your site will be available at:
echo https://your-project-name.onrender.com
echo.
echo Login: admin / admin123
echo.
echo Render is very simple and free!
echo.
pause
