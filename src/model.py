import streamlit as st
import pandas as pd
import joblib

st.title("🌍 Air Quality Prediction Dashboard")

model = joblib.load("src/aqi_model.pkl")

uploaded_file = st.file_uploader("Upload Air Quality Data (CSV)", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:", data.head())

    if "AQI" in data.columns:
        X = data.drop("AQI", axis=1)
        predictions = model.predict(X)
        data["Predicted_AQI"] = predictions
        st.write("Predictions:", data)

        st.line_chart(data[["AQI", "Predicted_AQI"]])
