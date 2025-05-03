@echo off
echo ⚙️ Setting up Python environment...
python -m venv venv
call venv\Scripts\activate.bat

echo 📦 Installing requirements...
pip install -r requirements.txt

echo 🏥 Starting Health Predictor...
streamlit run predict.py
pause