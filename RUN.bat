@echo off
chcp 65001 >nul
title מערכת ניהול מלאי
color 0A

echo.
echo ================================================
echo    🚀 מערכת ניהול מלאי - הפעלה מהירה
echo ================================================
echo.

echo 📦 מפעיל virtual environment...
call venv\Scripts\activate.bat

echo.
echo 🔍 בודק את המערכת...
python manage.py check
if errorlevel 1 (
    echo.
    echo ❌ יש בעיה במערכת!
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ המערכת תקינה!
echo.
echo ================================================
echo 📊 מידע על המערכת:
echo ================================================
echo.
echo 🌐 שרת: http://127.0.0.1:8000
echo 👤 מנהל: http://127.0.0.1:8000/admin
echo.
echo 🔑 התחברות:
echo    שם משתמש: admin
echo    סיסמה: admin123
echo.
echo 📋 דפים עיקריים:
echo    • מוצרים: /products/
echo    • מכירות: /sales/add/
echo    • חשבוניות: /sales/
echo    • דוחות: /reports/
echo    • לקוחות: /crm/customers/
echo.
echo ================================================
echo.
echo 🚀 מפעיל שרת...
echo 💡 לעצירה: Ctrl+C
echo.

python manage.py runserver

echo.
echo 👋 המערכת נסגרה
pause
