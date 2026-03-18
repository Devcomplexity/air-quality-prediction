import pandas as pd

def preprocess_raw_data(input_file="data/air_quality.csv", output_file="data/processed_data.csv"):
    df = pd.read_csv(input_file)

    # Keep only required columns
    df = df[["Date","AQI","PM2.5","PM10","NO2","SO2","CO","O3"]]

    # Handle missing values
    df = df.fillna(0)

    # Ensure Date is datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop invalid rows
    df = df.dropna(subset=["Date"])

    df.to_csv(output_file, index=False)
    print(f"✅ Processed dataset saved to {output_file}")
    return df

if __name__ == "__main__":
    preprocess_raw_data()
