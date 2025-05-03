#!/bin/bash
echo "⚙️ Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing requirements..."
pip install -r requirements.txt

echo "🏥 Starting Health Predictor..."
streamlit run predict.py