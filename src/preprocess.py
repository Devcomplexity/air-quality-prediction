import pandas as pd

# Load dataset
df = pd.read_csv("data/air_quality.csv")

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# Drop rows with missing values
df = df.dropna()

# Save cleaned dataset
df.to_csv("data/air_quality_clean.csv", index=False)
print("✅ Cleaned dataset saved to data/air_quality_clean.csv")
