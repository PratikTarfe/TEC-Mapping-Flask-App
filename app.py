from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# File paths
hourly_file = "hourly_avg_tec.csv"
daily_file = "daily_avg_tec.csv"

# Ensure static folder exists
os.makedirs("static", exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_graphs():
    selected_date = request.form.get("selected_date")
    if not selected_date:
        return render_template("index.html", error="Please select a valid date.")

    # Load the CSV files
    hourly_df = pd.read_csv(hourly_file)
    daily_df = pd.read_csv(daily_file)

    # Format date strings
    selected_datetime = datetime.strptime(selected_date, "%Y-%m-%d")
    selected_str = selected_datetime.strftime("%Y-%m-%d")

    # === 1. Hourly Variation (24 hrs of selected date) ===
    hourly_data = hourly_df[hourly_df["Date"] == selected_str]

    if not hourly_data.empty:
        plt.figure(figsize=(8, 4))
        plt.plot(hourly_data["Hour"], hourly_data["AvgTEC"], marker='o', color='blue')
        plt.title(f"Hourly TEC Variation - {selected_str}")
        plt.xlabel("Hour")
        plt.ylabel("Avg TEC")
        plt.xticks(rotation=45)  # ✅ Fix for overlapping X-axis labels
        plt.grid(True)
        plt.tight_layout()  # ✅ Adjust layout to fit rotated labels
        hourly_path = f"static/hourly_{selected_str}.png"
        plt.savefig(hourly_path)
        plt.close()
    else:
        hourly_path = None

    # === 2. Weekly Variation (7 days including selected) ===
    start_week = selected_datetime - timedelta(days=6)
    week_data = daily_df[
        (daily_df["Date"] >= start_week.strftime("%Y-%m-%d")) &
        (daily_df["Date"] <= selected_str)
    ]

    if not week_data.empty:
        plt.figure(figsize=(8, 4))
        plt.plot(week_data["Date"], week_data["DailyAvgTEC"], marker='o', color='green')
        plt.title(f"Weekly TEC Variation - {start_week.strftime('%Y-%m-%d')} to {selected_str}")
        plt.xlabel("Date")
        plt.ylabel("Avg TEC")
        plt.xticks(rotation=45)
        plt.grid(True)
        weekly_path = f"static/weekly_{selected_str}.png"
        plt.tight_layout()
        plt.savefig(weekly_path)
        plt.close()
    else:
        weekly_path = None

    # === 3. 15-Day Variation ===
    start_15 = selected_datetime - timedelta(days=14)
    fortnight_data = daily_df[
        (daily_df["Date"] >= start_15.strftime("%Y-%m-%d")) &
        (daily_df["Date"] <= selected_str)
    ]

    if not fortnight_data.empty:
        plt.figure(figsize=(8, 4))
        plt.plot(fortnight_data["Date"], fortnight_data["DailyAvgTEC"], marker='o', color='orange')
        plt.title(f"15-Day TEC Variation - {start_15.strftime('%Y-%m-%d')} to {selected_str}")
        plt.xlabel("Date")
        plt.ylabel("Avg TEC")
        plt.xticks(rotation=45)
        plt.grid(True)
        fortnight_path = f"static/fortnight_{selected_str}.png"
        plt.tight_layout()
        plt.savefig(fortnight_path)
        plt.close()
    else:
        fortnight_path = None

    # === 4. Monthly Variation ===
    month_str = selected_datetime.strftime("%Y-%m")
    monthly_data = daily_df[daily_df["Date"].str.startswith(month_str)]

    if not monthly_data.empty:
        plt.figure(figsize=(8, 4))
        plt.plot(monthly_data["Date"], monthly_data["DailyAvgTEC"], marker='o', color='purple')
        plt.title(f"Monthly TEC Variation - {month_str}")
        plt.xlabel("Date")
        plt.ylabel("Avg TEC")
        plt.xticks(rotation=45)
        plt.grid(True)
        monthly_path = f"static/monthly_{month_str}.png"
        plt.tight_layout()
        plt.savefig(monthly_path)
        plt.close()
    else:
        monthly_path = None

    return render_template("index.html",
                           selected_date=selected_str,
                           hourly_graph=os.path.basename(hourly_path) if hourly_path else None,
                           weekly_graph=os.path.basename(weekly_path) if weekly_path else None,
                           fortnight_graph=os.path.basename(fortnight_path) if fortnight_path else None,
                           monthly_graph=os.path.basename(monthly_path) if monthly_path else None)

if __name__ == "__main__":
    app.run(debug=True)
