import pandas as pd, numpy as np, joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def train_lstm(input_file="data/processed_data.csv", model_file="src/lstm_aqi_model.h5", scaler_file="src/lstm_scaler.pkl"):
    df = pd.read_csv(input_file)
    values = df["AQI"].values.reshape(-1,1)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(values)

    X, y = [], []
    # Use 7-day sequences
    for i in range(len(scaled)-7):
        X.append(scaled[i:i+7])
        y.append(scaled[i+7])
    X, y = np.array(X), np.array(y)

    model = Sequential([
        LSTM(50, activation="relu", input_shape=(7,1)),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=20, verbose=1)

    model.save(model_file)
    joblib.dump(scaler, scaler_file)
    print(f"✅ LSTM model saved to {model_file}, scaler saved to {scaler_file}")

if __name__ == "__main__":
    train_lstm()
