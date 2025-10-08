# 🚀 GitHub + Google Cloud Deployment

## 📋 שלבים להפעלת המערכת דרך GitHub

### **שלב 1: הכנת הקבצים**
```bash
setup_github_cloud.bat
```

### **שלב 2: יצירת Repository ב-GitHub**
1. **לך ל** - https://github.com/new
2. **שם Repository** - `inventory-system`
3. **תיאור** - `Inventory Management System`
4. **הפוך ל-PUBLIC** - חשוב!
5. **לחץ** - "Create repository"

### **שלב 3: העלאת הקוד ל-GitHub**
```bash
git remote add origin https://github.com/YOUR_USERNAME/inventory-system.git
git branch -M main
git push -u origin main
```

### **שלב 4: הגדרת Google Cloud Build**
1. **לך ל** - https://console.cloud.google.com/cloud-build/triggers
2. **לחץ** - "Create Trigger"
3. **שם** - `inventory-system-trigger`
4. **מקור** - GitHub
5. **Repository** - `your-username/inventory-system`
6. **Branch** - `main`
7. **Build Configuration** - Cloud Build configuration file
8. **Location** - `/cloudbuild.yaml`
9. **לחץ** - "Create"

### **שלב 5: בדיקת הפריסה**
1. **לך ל-Repository** - ב-GitHub
2. **עשה שינוי קטן** - הוסף הערה
3. **Commit ו-Push** - השינוי
4. **צפה ב-Build** - ב-Google Cloud Console

## 🎯 **יתרונות השיטה הזו:**
- ✅ **פריסה אוטומטית** - מ-GitHub
- ✅ **אין בעיות timeout** - Google Cloud Build מטפל
- ✅ **קל לעדכון** - פשוט push ל-GitHub
- ✅ **בקרת גרסאות** - עם Git
- ✅ **אמין יותר** - מ-פריסה ידנית

## 📱 **מה תקבל:**
- **מערכת מלאה** - ניהול מלאי, מכירות, דוחות
- **Admin מוכן** - `admin` / `admin123`
- **זמינות 24/7** - Google Cloud
- **עדכונים אוטומטיים** - מ-GitHub

## 🔧 **איך לעדכן את המערכת:**
1. **ערוך קבצים** - במחשב שלך
2. **Commit** - `git commit -m "Update"`
3. **Push** - `git push origin main`
4. **המערכת תתעדכן אוטומטית** - תוך כמה דקות

## 🌐 **כתובת המערכת:**
**https://my-claude-drive.uc.r.appspot.com**

## 🔑 **התחברות:**
- **שם משתמש** - `admin`
- **סיסמה** - `admin123`

## 📞 **תמיכה:**
אם יש בעיות, בדוק:
1. **Google Cloud Console** - Cloud Build logs
2. **GitHub** - Repository settings
3. **App Engine** - Service status
