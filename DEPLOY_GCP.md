# 🚀 פריסה ל-Google Cloud Platform
# Deploy to Google Cloud Platform

## 📋 תוכן עניינים
- [הקדמה](#הקדמה)
- [התקנה](#התקנה)
- [הגדרה](#הגדרה)
- [פריסה](#פריסה)
- [בדיקה](#בדיקה)
- [ניהול](#ניהול)

## 🚀 הקדמה

מדריך מלא לפריסת מערכת המלאי ל-Google Cloud Platform עם App Engine.

## 🔧 התקנה

### 1. התקנת Google Cloud SDK
```bash
# Windows
# הורד מ: https://cloud.google.com/sdk/docs/install

# Linux/Mac
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 2. התחברות
```bash
# התחברות
gcloud auth login

# הגדרת פרויקט
gcloud config set project YOUR_PROJECT_ID
```

## ⚙️ הגדרה

### 1. יצירת פרויקט
```bash
# יצירת פרויקט חדש
gcloud projects create YOUR_PROJECT_ID

# הגדרת פרויקט
gcloud config set project YOUR_PROJECT_ID
```

### 2. הפעלת שירותים
```bash
# הפעלת שירותים נדרשים
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable container.googleapis.com
```

### 3. יצירת App Engine
```bash
# יצירת App Engine application
gcloud app create --region=us-central1
```

## 🚀 פריסה

### 1. פריסה אוטומטית
```bash
# הפעלת סקריפט פריסה
chmod +x deploy_to_gcp.sh
./deploy_to_gcp.sh
```

### 2. פריסה ידנית
```bash
# בניית תמונה
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/inventory-system .

# פריסה ל-App Engine
gcloud app deploy app.yaml --image-url=gcr.io/YOUR_PROJECT_ID/inventory-system
```

### 3. פריסה עם Docker Compose
```bash
# פריסה עם Docker Compose
docker-compose -f docker-compose.gcp.yml up -d
```

## ✅ בדיקה

### 1. בדיקת סטטוס
```bash
# בדיקת שירותים
gcloud app services list

# בדיקת גרסאות
gcloud app versions list

# בדיקת לוגים
gcloud app logs tail
```

### 2. בדיקת נגישות
```bash
# קבלת URL
gcloud app browse

# בדיקת בריאות
curl https://YOUR_PROJECT_ID.appspot.com/health/
```

## 🔧 ניהול

### 1. עדכון
```bash
# עדכון גרסה
gcloud app deploy app.yaml --version=V2

# החלפת גרסה
gcloud app services set-traffic default --splits=V2=1
```

### 2. גיבוי
```bash
# גיבוי מסד נתונים
gcloud sql export sql YOUR_INSTANCE gs://YOUR_BUCKET/backup.sql

# גיבוי קבצים
gsutil cp -r gs://YOUR_BUCKET/media/ gs://YOUR_BUCKET/backup/
```

### 3. ניטור
```bash
# לוגים בזמן אמת
gcloud app logs tail -s default

# מדדי ביצועים
gcloud app services describe default
```

## 🛡️ אבטחה

### 1. SSL Certificate
```bash
# הגדרת SSL
gcloud app domain-mappings create your-domain.com
```

### 2. Firewall
```bash
# הגדרת Firewall
gcloud compute firewall-rules create allow-app-engine \
    --allow tcp:8080 \
    --source-ranges 0.0.0.0/0
```

### 3. Environment Variables
```bash
# הגדרת משתני סביבה
gcloud app deploy app.yaml --set-env-vars="DEBUG=False,SECRET_KEY=your-key"
```

## 📊 ניטור

### 1. Cloud Monitoring
```bash
# הפעלת ניטור
gcloud services enable monitoring.googleapis.com
```

### 2. Alerts
```bash
# יצירת התראות
gcloud alpha monitoring policies create --policy-from-file=alert-policy.yaml
```

## 🔄 CI/CD

### 1. GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to GCP
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to GCP
        run: |
          gcloud builds submit --tag gcr.io/$PROJECT_ID/inventory-system .
          gcloud app deploy app.yaml
```

### 2. Cloud Build
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/inventory-system', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/inventory-system']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['app', 'deploy', '--image-url=gcr.io/$PROJECT_ID/inventory-system']
```

## 💰 עלויות

### 1. App Engine
- **F1 Instance:** $0.05/שעה
- **F2 Instance:** $0.10/שעה
- **F4 Instance:** $0.20/שעה

### 2. Cloud Build
- **Build Time:** $0.003/דקה
- **Storage:** $0.026/GB/חודש

### 3. Cloud Storage
- **Standard:** $0.020/GB/חודש
- **Nearline:** $0.010/GB/חודש

## 🎯 סיכום

**המערכת מוכנה לפריסה ל-Google Cloud Platform!**

### יתרונות:
- ✅ **סקיילינג אוטומטי** - התאמה לעומס
- ✅ **ניהול אוטומטי** - ללא התערבות ידנית
- ✅ **אבטחה מובנית** - SSL, Firewall
- ✅ **ניטור מתקדם** - Cloud Monitoring
- ✅ **גיבויים אוטומטיים** - Cloud Storage

### שלבים:
1. **התקנה** - Google Cloud SDK
2. **הגדרה** - פרויקט ושירותים
3. **פריסה** - App Engine
4. **בדיקה** - נגישות ובריאות
5. **ניהול** - עדכונים וגיבויים

**המערכת מוכנה ל-Google Cloud!** 🚀
