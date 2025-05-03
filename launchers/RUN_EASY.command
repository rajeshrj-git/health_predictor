#!/bin/bash
echo "⏳ Downloading Health Predictor..."
curl -L https://github.com/rajeshrj-git/health_predictor/archive/main.zip -o health_predictor.zip

echo "🔄 Unzipping..."
unzip -q -o health_predictor.zip

echo "🚀 Starting..."
cd health_predictor-main
chmod +x predict.sh
./predict.sh