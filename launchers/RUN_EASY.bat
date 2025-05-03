@echo off
echo ⏳ Downloading Health Predictor...
powershell -command "Invoke-WebRequest -Uri 'https://github.com/rajeshrj-git/health_predictor/archive/main.zip' -OutFile 'health_predictor.zip'"

echo 🔄 Unzipping...
powershell -command "Expand-Archive -Path 'health_predictor.zip' -DestinationPath . -Force"

echo 🚀 Starting...
cd health_predictor-main
start predict.bat