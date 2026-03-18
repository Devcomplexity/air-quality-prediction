import requests
import pandas as pd

def download_delhi_data(limit=500):
    pollutants = ["pm25","pm10","no2","so2","co","o3"]
    dfs = []

    for p in pollutants:
        url = f"https://api.openaq.org/v3/measurements?city=Delhi&parameter={p}&limit={limit}"
        response = requests.get(url).json()
        results = response.get("results", [])
        if not results:
            continue

        df = pd.DataFrame([{
            "datetime": r.get("date", {}).get("utc"),
            p: r.get("value")
        } for r in results if "date" in r])
        dfs.append(df)

    if not dfs:
        print("❌ No data returned")
        return

    # Merge all pollutant columns on datetime
    merged = dfs[0]
    for d in dfs[1:]:
        merged = pd.merge(merged, d, on="datetime", how="outer")

    merged.to_csv("data/raw_data.csv", index=False)
    print("✅ Raw pollutant data saved to data/raw_data.csv")

if __name__ == "__main__":
    download_delhi_data()
