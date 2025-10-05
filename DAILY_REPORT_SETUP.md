# 📧 הגדרת דוח יומי אוטומטי במייל

## 📋 סקירה
מערכת זו שולחת דוח יומי מפורט במייל כל יום בשעה 19:30 הכולל:
- ✅ סטטיסטיקות כלליות (מוצרים, ערך מלאי, מלאי נמוך)
- 💰 מכירות היום (כמות, סכום, לקוחות)
- ⚠️ התראות קריטיות
- 📉 מוצרים במלאי נמוך (TOP 10)
- 📎 קבצי CSV מצורפים

---

## 🚀 הדרכה למתחילים - שלב אחר שלב

### שלב 1: הגדרת Gmail (מומלץ)

#### 1.1 - הפעלת אימות דו-שלבי
1. לך ל: https://myaccount.google.com/security
2. בחר **"2-Step Verification"**
3. עקוב אחרי ההוראות להפעלה

#### 1.2 - יצירת App Password
1. אחרי הפעלת אימות דו-שלבי, חזור ל: https://myaccount.google.com/security
2. חפש **"App passwords"** (או **"סיסמאות אפליקציות"**)
3. בחר **"Other (Custom name)"** ושם **"Inventory System"**
4. לחץ **"Generate"**
5. **שמור את הסיסמה שנוצרה!** (16 תווים)

---

### שלב 2: עדכון הגדרות ב-settings.py

פתח את הקובץ: `inventory_project/settings.py`

מצא את הקטע:
```python
# הגדרות Email (SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # <-- שנה כאן
EMAIL_HOST_PASSWORD = 'your-app-password'  # <-- שנה כאן
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # <-- שנה כאן
DAILY_REPORT_EMAIL = 'your-email@gmail.com'  # <-- שנה כאן
```

**החלף:**
- `your-email@gmail.com` → כתובת ה-Gmail שלך
- `your-app-password` → ה-App Password שיצרת (16 תווים, ללא רווחים)

**דוגמה:**
```python
EMAIL_HOST_USER = 'mystore@gmail.com'
EMAIL_HOST_PASSWORD = 'abcdwxyzabcdwxyz'  # App Password
DEFAULT_FROM_EMAIL = 'mystore@gmail.com'
DAILY_REPORT_EMAIL = 'mystore@gmail.com'  # או כתובת אחרת לקבלת הדוחות
```

---

### שלב 3: בדיקה ידנית (לפני תזמון)

פתח PowerShell בתיקיית הפרויקט והרץ:

```powershell
# הפעל את הסביבה הווירטואלית
.\venv\Scripts\Activate.ps1

# שלח דוח בדיקה
python manage.py send_daily_report
```

**אם הכל עובד, תקבל:**
```
✅ הדוח נשלח בהצלחה ל-youremail@gmail.com!
📎 נשלחו 2 קבצים מצורפים
```

**אם יש שגיאה:**
- ✅ ודא שהגדרות ה-SMTP נכונות
- ✅ בדוק את ה-App Password (ללא רווחים)
- ✅ ודא שאימות דו-שלבי פעיל ב-Gmail

---

### שלב 4: תזמון אוטומטי ב-Windows

#### 4.1 - הרצת סקריפט התזמון

**פתח PowerShell כמנהל** (Right-click → Run as Administrator) והרץ:

```powershell
cd C:\Users\User\Downloads\inventory
.\scripts\schedule_daily_report.ps1
```

הסקריפט ישאל:
1. ✅ אם למחוק משימה קיימת (אם יש)
2. ✅ אם להריץ דוח עכשיו לבדיקה

#### 4.2 - אישור המשימה

המשימה נוצרה! כעת היא תרוץ **אוטומטית כל יום בשעה 19:30**.

**לצפייה במשימה:**
1. פתח **Task Scheduler** (חפש ב-Start)
2. בחר **Task Scheduler Library**
3. מצא **"InventoryDailyReport"**

---

## 🔧 אפשרויות מתקדמות

### שינוי השעה
רוצה לשנות את השעה? ערוך ב-`scripts/schedule_daily_report.ps1`:
```powershell
$TriggerTime = "08:00"  # שנה לשעה הרצויה
```
ואז הרץ מחדש את הסקריפט.

### שליחה לכמה מיילים
ערוך את `inventory/management/commands/send_daily_report.py`:
```python
to=[recipient_email, 'email2@example.com', 'email3@example.com'],
```

### שינוי תוכן הדוח
כל התוכן נמצא ב-`inventory/management/commands/send_daily_report.py`.
ערוך את ה-HTML או הוסף סטטיסטיקות נוספות.

---

## 🌐 שרתי Email נוספים

### Outlook / Hotmail
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### Yahoo Mail
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### שרת SMTP מותאם אישית
```python
EMAIL_HOST = 'mail.yourdomain.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True  # במקום TLS
```

---

## 🐛 פתרון בעיות

### "Authentication failed"
- ✅ ודא שה-App Password נכון
- ✅ בדוק שאימות דו-שלבי פעיל
- ✅ נסה ליצור App Password חדש

### "Connection refused" או "Timeout"
- ✅ בדוק חיבור אינטרנט
- ✅ ודא שפורט 587 לא חסום בחומת אש
- ✅ נסה עם פורט 465 + `EMAIL_USE_SSL = True`

### המייל לא מגיע
- ✅ בדוק תיקיית Spam
- ✅ ודא שכתובת המייל נכונה
- ✅ בדוק את הלוג: `logs\daily_report.log`

### המשימה המתוזמנת לא רצה
- ✅ פתח Task Scheduler ובדוק סטטוס
- ✅ Right-click על המשימה → **"Run"** לבדיקה
- ✅ בדוק **"History"** לראות שגיאות
- ✅ ודא שהנתיב לסקריפט נכון

---

## 📝 לוגים

כל הרצה נשמרת בלוג:
```
logs\daily_report.log
```

דוגמה ללוג:
```
[2025-10-06 19:30:01] Starting daily report...
[2025-10-06 19:30:02] Virtual environment activated
[2025-10-06 19:30:05] Daily report sent successfully
[2025-10-06 19:30:05] Daily report task completed
```

---

## ✅ רשימת בדיקה

לפני שתסמוך על המערכת:

- [ ] הגדרת App Password ב-Gmail
- [ ] עדכון הגדרות ב-`settings.py`
- [ ] בדיקה ידנית: `python manage.py send_daily_report`
- [ ] הרצת סקריפט התזמון כמנהל
- [ ] בדיקה ב-Task Scheduler שהמשימה קיימת
- [ ] המתן ל-19:30 לבדיקה אוטומטית (או הרץ ידנית)
- [ ] בדיקה שהמייל הגיע
- [ ] בדיקת קבצים מצורפים

---

## 🎉 סיימת!

כעת המערכת תשלח לך דוח יומי אוטומטי כל יום בשעה 19:30!

**שאלות?** בדוק את הלוג או הרץ את הפקודה הידנית לבדיקה.

---

**📧 נוצר עבור מערכת ניהול מלאי | © 2024**

