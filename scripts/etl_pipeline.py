import pandas as pd
import sqlite3
import os

print(" Starting ETL...")

# make sure folders exist
os.makedirs('../database', exist_ok=True)
print("Database folder ready.")

# 1️ Extract
print("Reading CSV file...")
csv_path = '../data/city_waste_data.csv'
print("🔹 File path:", csv_path)
data = pd.read_csv(csv_path)
print("Data extracted:", len(data), "rows")

# 2️ Transform
print("Transforming data...")
data.dropna(inplace=True)
data['Date'] = pd.to_datetime(data['Date'])
data['Recycling_Percentage'] = (data['Recycled_Tons'] / data['Waste_Collected_Tons']) * 100
print("Data transformed successfully.")

# 3️ Load
print("Loading into database...")
conn = sqlite3.connect('../database/waste_data.db')
data.to_sql('waste_records', conn, if_exists='replace', index=False)
conn.close()
print("Data loaded into SQLite DB.")

# optional: save cleaned data
data.to_csv('../data/cleaned_city_waste_data.csv', index=False)
print("ETL pipeline executed successfully!")
