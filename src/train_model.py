import pandas as pd, joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def train_rf_pipeline(input_file="data/processed_data.csv", model_file="src/aqi_model.pkl"):
    df = pd.read_csv(input_file)
    X = df[["PM2.5","PM10","NO2","SO2","CO","O3"]]
    y = df["AQI"]

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    pipeline.fit(X, y)
    joblib.dump(pipeline, model_file)
    print(f"✅ RandomForest pipeline saved to {model_file}")

if __name__ == "__main__":
    train_rf_pipeline()
