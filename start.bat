@echo off
chcp 65001 >nul
echo.
echo 🚀 מפעיל את מערכת ניהול המלאי...
echo.

REM הפעלת virtual environment
call venv\Scripts\activate.bat

REM בדיקת מערכת
echo 🔍 בודק את המערכת...
python manage.py check
if errorlevel 1 (
    echo.
    echo ❌ יש בעיות במערכת
    pause
    exit /b 1
)

echo ✅ המערכת תקינה
echo.
echo ====================================
echo 📊 מידע על המערכת:
echo    • שרת: http://127.0.0.1:8000
echo    • מנהל: http://127.0.0.1:8000/admin
echo.
echo 💡 לעצירה: Ctrl+C
echo ====================================
echo.
echo 🌐 מפעיל שרת Django...
echo.

REM הפעלת השרת
python manage.py runserver

pause

