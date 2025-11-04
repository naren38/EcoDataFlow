
# ECO DATA FLOW – TREND ANALYSIS & VISUALIZATION


import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure outputs folder exists
os.makedirs('../outputs', exist_ok=True)

# 1️ Read data from database
conn = sqlite3.connect('../database/waste_data.db')
df = pd.read_sql_query("SELECT * FROM waste_records", conn)
conn.close()

# 2️ Calculate monthly and city averages
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M').astype(str)
city_avg = df.groupby('City')['Recycling_Percentage'].mean().sort_values(ascending=False)
month_avg = df.groupby(['Month', 'City'])['Recycling_Percentage'].mean().reset_index()

# 3️ Bar chart – Top Cities by Average Recycling
plt.figure(figsize=(8, 5))
sns.barplot(x=city_avg.index, y=city_avg.values, palette='viridis')
plt.title('Top Indian Cities by Average Recycling Efficiency (%)')
plt.ylabel('Average Recycling %')
plt.xlabel('City')
plt.tight_layout()
plt.savefig('../outputs/top_cities.png')
plt.close()

# 4️ Line chart – Monthly Trends
plt.figure(figsize=(10, 6))
sns.lineplot(data=month_avg, x='Month', y='Recycling_Percentage', hue='City', marker='o')
plt.title('Monthly Recycling Trends for Indian Cities')
plt.ylabel('Recycling %')
plt.xlabel('Month')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('../outputs/monthly_trends.png')
plt.close()

print(" Trend analysis completed – charts saved in /outputs folder.")
