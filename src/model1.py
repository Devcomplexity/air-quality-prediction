import pandas as pd
import joblib

# Load trained model
model = joblib.load("src/aqi_model.pkl")

# Example: load new data for prediction
data = pd.read_csv("data/air_quality.csv")
X = data.drop("AQI", axis=1)

predictions = model.predict(X)
data["Predicted_AQI"] = predictions

print(data.head())
