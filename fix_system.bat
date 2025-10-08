@echo off
chcp 65001 >nul
echo Starting system fix...

echo Checking gcloud...
gcloud --version

echo Checking project...
gcloud config get-value project

echo Checking App Engine services...
gcloud app services list

echo Checking versions...
gcloud app versions list

echo Checking logs...
gcloud app logs read --service=default --limit=10

echo Checking accessibility...
curl -I https://my-claude-drive.uc.r.appspot.com

echo Fix completed
pause
