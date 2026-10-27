import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# 1. Load your actual dataset
# Replace 'city_day.csv' or 'air_quality.csv' with your actual filename
df = pd.read_csv("city_day.csv")

# 2. Select the feature columns present in your dataset and drop rows with missing AQI values
features = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3']

# Drop rows where target AQI or core features are null
df = df.dropna(subset=['AQI'] + features)

X = df[features]
y = df['AQI']

# 3. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate Model
predictions = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, predictions):.2f}")
print(f"R² Score: {r2_score(y_test, predictions):.2f}")

# 6. Save Model
joblib.dump(model, "vayu_rf_model.pkl")
print("✅ Model trained successfully on real pollutant columns and saved!")