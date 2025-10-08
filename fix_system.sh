#!/bin/bash
echo "🔧 מתחיל תיקון המערכת..."

echo "📋 בדיקת gcloud..."
gcloud --version

echo "📋 בדיקת פרויקט..."
gcloud config get-value project

echo "📋 בדיקת סטטוס App Engine..."
gcloud app services list

echo "📋 בדיקת גרסאות..."
gcloud app versions list

echo "📋 בדיקת לוגים..."
gcloud app logs read --service=default --limit=10

echo "📋 בדיקת נגישות..."
curl -I https://my-claude-drive.uc.r.appspot.com

echo "✅ סיום בדיקות"
