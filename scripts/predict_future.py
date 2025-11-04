
# ECO DATA FLOW – PREDICTION & FUTURE FORECAST


import pandas as pd
import sqlite3
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure output folder exists
os.makedirs('../outputs', exist_ok=True)

# 1️⃣ Read data from database
conn = sqlite3.connect('../database/waste_data.db')
df = pd.read_sql_query("SELECT * FROM waste_records", conn)
conn.close()

# 2️⃣ Prepare data
df['Date'] = pd.to_datetime(df['Date'])
df['Timestamp'] = df['Date'].map(pd.Timestamp.toordinal)

# We'll predict each city's future recycling % for next 3 months
future_predictions = []

for city in df['City'].unique():
    city_data = df[df['City'] == city].sort_values('Date')
    X = city_data[['Timestamp']]
    y = city_data['Recycling_Percentage']

    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next 3 months
    future_dates = pd.date_range(df['Date'].max(), periods=4, freq='M')[1:]
    future_timestamps = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
    preds = model.predict(future_timestamps)

    city_future = pd.DataFrame({
        'City': city,
        'Date': future_dates,
        'Predicted_Recycling_Percentage': preds
    })
    future_predictions.append(city_future)

# Combine all
pred_df = pd.concat(future_predictions)
pred_df.to_csv('../outputs/future_predictions.csv', index=False)

# 3️⃣ Visualization
plt.figure(figsize=(10,6))
for city in pred_df['City'].unique():
    city_data = pred_df[pred_df['City'] == city]
    plt.plot(city_data['Date'], city_data['Predicted_Recycling_Percentage'], marker='o', label=city)

plt.title('Predicted Future Recycling Trends (Next 3 Months)')
plt.xlabel('Date')
plt.ylabel('Predicted Recycling %')
plt.legend()
plt.tight_layout()
plt.savefig('../outputs/future_forecast.png')
plt.close()

print("🤖 Future prediction completed – forecast chart & CSV saved in /outputs folder.")
