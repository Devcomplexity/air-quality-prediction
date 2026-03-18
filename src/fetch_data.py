import pandas as pd

def fetch_pollutants():
    try:
        df = pd.read_csv("data/processed_data.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        latest = df.sort_values("Date").tail(1)
        return latest
    except Exception as e:
        print("❌ Error loading processed data:", e)
        return pd.DataFrame()
