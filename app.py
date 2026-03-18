import streamlit as st, joblib, numpy as np, pandas as pd
from tensorflow.keras.models import load_model
from src.fetch_data import fetch_pollutants
from src.alert import send_alert_email, send_sms_alert
import folium
from streamlit_folium import st_folium

st.title("🌍 Delhi Air Quality Prediction System")

# Load models
rf_model = joblib.load("src/aqi_model.pkl")
lstm_model = load_model("src/lstm_aqi_model.h5", compile=False)
scaler = joblib.load("src/lstm_scaler.pkl")

# Load pollutant data
pollutants = fetch_pollutants()
st.header("📊 Latest Pollutant Data")
st.write(pollutants)

# --- Prediction ---
st.header("🔮 Predicted AQI (RandomForest)")
required_features = ["PM2.5","PM10","NO2","SO2","CO","O3"]

if not pollutants.empty and all(f in pollutants.columns for f in required_features):
    X = pollutants[required_features]
    aqi_pred = rf_model.predict(X)[0]
    st.success(f"Predicted AQI: {aqi_pred:.2f}")

    # --- Forecast ---
    st.header("📈 3-Day AQI Forecast")
    df = pd.read_csv("data/processed_data.csv")
    last_values = df["AQI"].values[-7:].reshape(-1,1)
    scaled = scaler.transform(last_values)
    X_input = scaled.reshape((1,7,1))
    forecast = []
    for _ in range(3):
        pred = lstm_model.predict(X_input)
        forecast.append(scaler.inverse_transform(pred)[0][0])
        X_input = np.append(X_input[:,1:,:], pred.reshape(1,1,1), axis=1)
    st.success(f"Next 3 Days AQI Forecast: {forecast}")

    # --- Alerts ---
    if aqi_pred > 300 or any(f > 300 for f in forecast):
        st.error("⚠️ Hazardous AQI detected! Authorities notified.")
        send_alert_email("Delhi", aqi_pred)
        send_sms_alert("Delhi", aqi_pred)

    # --- Heatmap ---
    st.header("🗺️ AQI Heatmap")
    m = folium.Map(location=[28.61, 77.23], zoom_start=11)

    locations = {
        "Rohini": [28.75, 77.12],
        "Dwarka": [28.58, 77.03],
        "Noida": [28.57, 77.32],
        "Gurugram": [28.46, 77.03]
    }

    # Assign AQI values from last 4 days
    recent_aqi = df["AQI"].tail(4).values
    area_aqi = dict(zip(locations.keys(), recent_aqi))

    sorted_areas = sorted(area_aqi.items(), key=lambda x: x[1], reverse=True)

    for area, value in sorted_areas:
        coords = locations[area]
        color = "green"
        if value > 300: color = "red"
        elif value > 200: color = "orange"
        elif value > 100: color = "yellow"

        folium.CircleMarker(
            location=coords,
            radius=10,
            popup=f"{area} AQI: {value:.2f}",
            color=color,
            fill=True,
        ).add_to(m)

    st_folium(m, width=700, height=500)

else:
    st.warning("Pollutant data unavailable. Cannot predict AQI.")

# --- Model Info ---
st.header("ℹ️ Model Information")
st.write("RandomForest → pollutant-based AQI prediction")
st.write("LSTM → time-series AQI forecasting")
