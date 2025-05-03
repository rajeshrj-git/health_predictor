import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib

# Load model and feature columns
model = load_model('models/health_model.h5')
feature_columns = joblib.load('models/feature_columns.pkl')

st.title("Health Risk Prediction System")

with st.form("health_form"):
    st.header("Patient Information")
    
    col1, col2 = st.columns(2)
    age = col1.number_input("Age", 18, 100, 45)
    gender = col2.selectbox("Gender", ["Male", "Female"])
    
    col3, col4 = st.columns(2)
    bmi = col3.number_input("BMI", 10.0, 50.0, 25.0)
    heart_rate = col4.number_input("Resting Heart Rate", 40, 120, 72)
    
    col5, col6 = st.columns(2)
    bp = col5.number_input("Blood Pressure (systolic)", 70, 200, 120)
    glucose = col6.number_input("Glucose (mg/dL)", 70, 300, 100)
    
    cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 400, 200)
    smoker = st.checkbox("Current Smoker")
    hyp = st.checkbox("History of Hypertension")
    
    if st.form_submit_button("Predict Risks"):
        # Prepare input
        input_data = pd.DataFrame([[
            age, bmi, heart_rate, bp, 
            glucose, cholesterol,
            1 if smoker else 0,
            1 if hyp else 0
        ]], columns=feature_columns)
        
        # Predict
        risks = model.predict(input_data)[0]
        
        # Display results
        st.subheader("Predicted Risks")
        col1, col2, col3 = st.columns(3)
        col1.metric("Heart Disease", f"{risks[0]*100:.1f}%")
        col2.metric("Diabetes", f"{risks[1]*100:.1f}%")
        col3.metric("Metabolic Risk", f"{risks[2]*100:.1f}%")
        
        # Recommendations
        st.subheader("Recommendations")
        if any(r > 0.7 for r in risks):
            st.error("High risk detected - Consult a doctor immediately")
        elif any(r > 0.4 for r in risks):
            st.warning("Moderate risk - Recommended lifestyle changes")
        else:
            st.success("Low risk - Maintain current habits")

if __name__ == '__main__':
    st.write("Run with: `streamlit run predict.py`")