import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Heart Disease Risk Predictor", page_icon="❤️", layout="centered")

st.title("Heart Disease Prediction Frontend")
st.write(
    "Enter the patient data below to predict whether they are likely to have heart disease using the trained model."
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "heart_disease_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "heart_disease_scaler.pkl")
COLUMNS_PATH = os.path.join(os.path.dirname(__file__), "heart_disease_columns.pkl")

@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    columns = joblib.load(COLUMNS_PATH)
    return model, scaler, list(columns)

model, scaler, encoded_columns = load_artifacts()

numeric_cols = ["Age", "RestingBP", "Cholesterol", "FastingBS", "MaxHR", "Oldpeak"]
cat_cols = {
    "Sex": ["Female", "Male"],
    "Chest Pain Type": ["ATA", "NAP", "TA", "ASY"],
    "Resting ECG": ["Normal", "ST", "LVH"],
    "Exercise Angina": ["No", "Yes"],
    "ST Slope": ["Up", "Flat", "Down"],
}

with st.form(key="prediction_form"):
    age = st.number_input("Age", min_value=1, max_value=120, value=54)
    resting_bp = st.number_input("Resting Blood Pressure", min_value=50, max_value=250, value=130)
    cholesterol = st.number_input("Cholesterol", min_value=50, max_value=500, value=250)
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1], index=0)
    max_hr = st.number_input("Max Heart Rate Achieved", min_value=60, max_value=250, value=150)
    oldpeak = st.number_input("Oldpeak (ST depression)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    sex = st.selectbox("Sex", cat_cols["Sex"], index=0)
    chest_pain = st.selectbox("Chest Pain Type", cat_cols["Chest Pain Type"], index=0)
    resting_ecg = st.selectbox("Resting ECG", cat_cols["Resting ECG"], index=0)
    exercise_angina = st.selectbox("Exercise Induced Angina", cat_cols["Exercise Angina"], index=0)
    st_slope = st.selectbox("ST Slope", cat_cols["ST Slope"], index=0)

    submit_button = st.form_submit_button("Predict Heart Disease")

if submit_button:
    data = {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,
        "Sex_M": 1 if sex == "Male" else 0,
        "ChestPainType_ATA": 1 if chest_pain == "ATA" else 0,
        "ChestPainType_NAP": 1 if chest_pain == "NAP" else 0,
        "ChestPainType_TA": 1 if chest_pain == "TA" else 0,
        "RestingECG_Normal": 1 if resting_ecg == "Normal" else 0,
        "RestingECG_ST": 1 if resting_ecg == "ST" else 0,
        "ExerciseAngina_Y": 1 if exercise_angina == "Yes" else 0,
        "ST_Slope_Flat": 1 if st_slope == "Flat" else 0,
        "ST_Slope_Up": 1 if st_slope == "Up" else 0,
    }

    feature_columns = [c for c in encoded_columns if c != "HeartDisease"]
    input_df = pd.DataFrame([data], columns=feature_columns)
    X_scaled = scaler.transform(input_df)
    prediction = model.predict(X_scaled)[0]

    st.subheader("Prediction")
    if prediction == 1:
        st.error("The model predicts that this patient is likely to have heart disease.")
    else:
        st.success("The model predicts that this patient is unlikely to have heart disease.")

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X_scaled)[0]
        st.write(f"Prediction probability: {proba[1]*100:.2f}% chance of heart disease")

    st.write("---")
    st.write("### Submitted input")
    st.json(data)
