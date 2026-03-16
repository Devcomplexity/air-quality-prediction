import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

st.title("🌍 Air Quality Prediction Dashboard")

uploaded_file = st.file_uploader("Upload Air Quality Data (CSV)", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:", data.head())

    if "AQI" in data.columns:
        X = data.drop("AQI", axis=1)
        y = data["AQI"]

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        st.success("Model trained successfully!")

        st.subheader("Predict AQI")
        user_input = []
        for col in X.columns:
            val = st.number_input(f"Enter {col}", value=float(data[col].mean()))
            user_input.append(val)

        prediction = model.predict([user_input])[0]
        st.write(f"Predicted AQI: {prediction:.2f}")

        if prediction > 200:
            st.error("⚠️ Poor Air Quality Alert!")
        else:
            st.success("✅ Air Quality is Safe")
