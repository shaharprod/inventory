#!/bin/bash
# סקריפט פריסה ל-Google Cloud Platform
# Deploy Script to Google Cloud Platform

echo "🚀 מתחיל פריסה ל-Google Cloud Platform..."

# בדיקת Google Cloud SDK
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK לא מותקן!"
    echo "📥 הורד מ: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# בדיקת התחברות
echo "🔐 בדיקת התחברות ל-Google Cloud..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1; then
    echo "❌ לא מחובר ל-Google Cloud!"
    echo "🔑 התחבר עם: gcloud auth login"
    exit 1
fi

# הגדרת פרויקט
echo "📁 הגדרת פרויקט..."
read -p "הזן ID של הפרויקט: " PROJECT_ID
gcloud config set project $PROJECT_ID

# הפעלת שירותים נדרשים
echo "⚙️ הפעלת שירותים נדרשים..."
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable container.googleapis.com

# יצירת App Engine application
echo "🏗️ יצירת App Engine application..."
gcloud app create --region=us-central1

# בניית תמונה
echo "📦 בניית תמונה..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/inventory-system .

# פריסה ל-App Engine
echo "🚀 פריסה ל-App Engine..."
gcloud app deploy app.yaml --image-url=gcr.io/$PROJECT_ID/inventory-system

# בדיקת סטטוס
echo "✅ בדיקת סטטוס..."
gcloud app services list

# הצגת URL
echo "🌐 המערכת זמינה ב:"
gcloud app browse

echo "🎉 הפריסה הושלמה בהצלחה!"
