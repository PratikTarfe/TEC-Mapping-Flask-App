import pandas as pd

# Load the hourly average TEC file
df = pd.read_csv("hourly_avg_tec.csv")

# Group by date and calculate the daily average TEC
daily_avg_df = df.groupby('Date')['AvgTEC'].mean().reset_index()
daily_avg_df.rename(columns={'AvgTEC': 'DailyAvgTEC'}, inplace=True)

# Save to CSV
daily_avg_df.to_csv("daily_avg_tec.csv", index=False)

print("daily_avg_tec.csv created successfully!")
