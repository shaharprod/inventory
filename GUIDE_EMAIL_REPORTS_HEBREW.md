# 📧 מדריך מלא - הגדרת שליחת דוחות במייל

## 📋 תוכן עניינים
1. [שיטה 1: Console Backend (מומלץ לפיתוח)](#שיטה-1-console-backend)
2. [שיטה 2: Gmail SMTP (לייצור)](#שיטה-2-gmail-smtp)
3. [איך להגדיר דוחות יומיים](#איך-להגדיר-דוחות-יומיים)
4. [שליחת דוח מיידי](#שליחת-דוח-מיידי)
5. [פתרון בעיות](#פתרון-בעיות)

---

## שיטה 1: Console Backend (מומלץ לפיתוח)

### ✅ יתרונות:
- **קל להגדרה** - לא צריך סיסמאות או הגדרות SMTP
- **מהיר** - לא צריך להתחבר לשרת מייל
- **מושלם לפיתוח ובדיקות**

### 🔧 איך זה עובד?
הדוחות מודפסים בטרמינל (חלון השרת) במקום נשלחים למייל.

### 📝 הגדרה:

#### שלב 1: וודא שזה מופעל (כבר הופעל!)
הקובץ `.env` צריך להיות **בלי** `EMAIL_BACKEND` או עם הערה (`#`):

```bash
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

#### שלב 2: הגדר הגדרות במערכת
1. פתח דפדפן: http://localhost:8000/settings/
2. גלול ל**"הגדרות דוחות יומיים במייל"**
3. מלא:
   - ✅ **הפעל שליחת מיילים**: סמן את התיבה
   - ✅ **מייל יומי מופעל**: סמן את התיבה
   - ✅ **מייל לקבלת דוחות**: `admin@inventory.local` (יכול להיות כל דבר)
   - ✅ **זמן שליחה**: `09:00:00`
4. לחץ **"שמור הגדרות"**

#### שלב 3: בדיקה
1. לך ל-Dashboard: http://localhost:8000/
2. גלול למטה ללחץ **"שלח דוח מיידי"**
3. תקבל הודעה: **"✅ הדוח נשלח בהצלחה!"**
4. **בדוק בטרמינל** (חלון השרת) - תראה:

```
Content-Type: text/html; charset="utf-8"
Subject: ⚡ דוח מיידי - 06/10/2025 19:00
From: noreply@inventory.local
To: admin@inventory.local

<!DOCTYPE html>
...דוח מלא...
```

---

## שיטה 2: Gmail SMTP (לייצור)

### ✅ יתרונות:
- **מיילים אמיתיים** - נשלחים ל-Gmail
- **מתאים לייצור**

### ⚠️ חשוב לדעת:
Gmail דורש **App Password** (לא סיסמה רגילה!)

---

### 📝 הגדרה צעד אחר צעד:

#### שלב 1: הפעל 2FA ב-Gmail
1. לך ל: https://myaccount.google.com/security
2. לחץ על **"2-Step Verification"**
3. עקוב אחרי ההוראות להפעלת אימות דו-שלבי

#### שלב 2: צור App Password
1. לך ל: https://myaccount.google.com/apppasswords
2. בחר:
   - **Select app**: Mail
   - **Select device**: Other (Custom name)
   - שם: `Inventory System`
3. לחץ **"Generate"**
4. **העתק את ה-16 ספרות** (לדוגמה: `abcd efgh ijkl mnop`)

#### שלב 3: עדכן את קובץ .env
פתח את הקובץ `.env` (בתיקיית הראשית של הפרויקט) ועדכן:

```bash
# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=shaharprod@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=shaharprod@gmail.com
```

**החלף**:
- `shaharprod@gmail.com` → המייל שלך
- `abcd efgh ijkl mnop` → App Password שיצרת (עם הרווחים!)

#### שלב 4: אתחל את השרת
עצור והפעל מחדש את Django:
```bash
# לחץ Ctrl+C בטרמינל
# ואז:
python manage.py runserver
```

#### שלב 5: הגדר במערכת
1. לך ל: http://localhost:8000/settings/
2. גלול ל**"הגדרות דוחות יומיים במייל"**
3. מלא:
   - ✅ **הפעל שליחת מיילים**: סמן
   - ✅ **מייל יומי מופעל**: סמן
   - ✅ **מייל לקבלת דוחות**: המייל שלך (לדוגמה: `shaharprod@gmail.com`)
   - ✅ **זמן שליחה**: `09:00:00`
4. לחץ **"שמור הגדרות"**

#### שלב 6: בדיקה
1. לך ל-Dashboard: http://localhost:8000/
2. לחץ **"שלח דוח מיידי"**
3. תקבל הודעה: **"✅ הדוח נשלח בהצלחה!"**
4. **בדוק ב-Gmail** - תקבל מייל עם הדוח!

---

## איך להגדיר דוחות יומיים

### Windows (PowerShell):

#### שלב 1: צור Task Scheduler
```powershell
cd C:\Users\User\Downloads\inventory
.\scripts\schedule_daily_report.ps1
```

#### או ידנית:
1. פתח **Task Scheduler**
2. **Create Basic Task**
3. שם: `Inventory Daily Report`
4. Trigger: **Daily** → בחר שעה (לדוגמה: 09:00)
5. Action: **Start a program**
   - Program: `C:\Users\User\Downloads\inventory\venv\Scripts\python.exe`
   - Arguments: `manage.py send_daily_report --email=שליך@gmail.com`
   - Start in: `C:\Users\User\Downloads\inventory`
6. **Finish**

---

## שליחת דוח מיידי

### מהדפדפן:
1. לך ל: http://localhost:8000/
2. גלול למטה
3. לחץ **"שלח דוח מיידי"**

### מהטרמינל:
```bash
python manage.py send_daily_report --email=shaharprod@gmail.com
```

---

## פתרון בעיות

### ❌ שגיאה: "Username and Password not accepted"

**סיבה**: App Password לא נכון או חסר

**פתרון**:
1. ודא שהפעלת 2FA ב-Gmail
2. צור App Password חדש
3. העתק **עם הרווחים**: `abcd efgh ijkl mnop`
4. עדכן ב-`.env`
5. אתחל את השרת

---

### ❌ שגיאה: "not a valid JSON"

**סיבה**: השרת מחזיר HTML במקום JSON (בעיה בהגדרות)

**פתרון**:
```bash
# עבור ל-Console Backend (מומלץ):
# ערוך .env:
#EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

---

### ❌ המייל לא מגיע ב-Gmail

**בדיקות**:
1. ✅ App Password נכון ב-`.env`?
2. ✅ השרת אותחל מחדש?
3. ✅ המייל ב-Settings נכון?
4. ✅ בדוק ב-**Spam/Junk** folder

---

## 📊 מה כולל הדוח?

הדוח היומי כולל:
- ✅ סטטיסטיקות כלליות (מוצרים, מלאי, ערכים)
- ✅ מכירות היום
- ✅ מוצרים במלאי נמוך
- ✅ התראות קריטיות
- ✅ תנועות מלאי
- ✅ קובץ Excel מצורף

---

## 🎯 סיכום מהיר

### Console Backend (פיתוח):
```bash
# .env
#EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# Settings במערכת
מייל לקבלת דוחות: admin@inventory.local
```

### Gmail SMTP (ייצור):
```bash
# .env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Settings במערכת
מייל לקבלת דוחות: your-email@gmail.com
```

---

**🚀 מוכן לשימוש!**

