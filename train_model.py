"""
Training script for Ethiopian Crop Price Predictor
This script trains a Random Forest model and saves it along with label encoders.
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'wfp_food_prices_eth.csv')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

# Ensure models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)

print("=" * 60)
print("Ethiopian Crop Price Predictor - Model Training")
print("=" * 60)

# Load the data
print(f"\n1. Loading data from: {DATA_PATH}")
try:
    df = pd.read_csv(DATA_PATH)
    print(f"   ✓ Loaded {len(df)} rows")
except FileNotFoundError:
    print(f"   ✗ ERROR: Data file not found at {DATA_PATH}")
    print(f"\n   Please ensure the dataset exists at the correct location.")
    print(f"   Expected path: data/raw/wfp_food_prices_eth.csv")
    exit(1)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()
print(f"   ✓ Columns: {list(df.columns)}")

# Parse dates and sort
print("\n2. Preprocessing data...")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Season logic function
def get_season(month):
    if month in [6, 7, 8, 9]:
        return 'kiremt'
    elif month in [3, 4, 5]:
        return 'belg'
    elif month in [10, 11, 12]:
        return 'harvest'
    else:
        return 'dry'

# Extract month, year, and season
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df['season'] = df['month'].apply(get_season)

# Create lag features (price_lag1, price_lag2, price_lag3, rolling_mean_3)
print("   • Creating lag features...")
df = df.sort_values(['commodity', 'admin1', 'date'])

# Group by commodity and admin1 to calculate lags
df['price_lag1'] = df.groupby(['commodity', 'admin1'])['price'].shift(1)
df['price_lag2'] = df.groupby(['commodity', 'admin1'])['price'].shift(2)
df['price_lag3'] = df.groupby(['commodity', 'admin1'])['price'].shift(3)
df['rolling_mean_3'] = df.groupby(['commodity', 'admin1'])['price'].rolling(window=3, min_periods=1).mean().reset_index(0, drop=True)

# Drop rows with NaN lag features (first few rows per group)
df = df.dropna(subset=['price_lag1', 'price_lag2', 'price_lag3'])
print(f"   ✓ After creating lags: {len(df)} rows")

# Encode categorical variables
print("\n3. Encoding categorical features...")
le_commodity = LabelEncoder()
le_admin = LabelEncoder()
le_season = LabelEncoder()

df['commodity_encoded'] = le_commodity.fit_transform(df['commodity'])
df['admin_encoded'] = le_admin.fit_transform(df['admin1'])
df['season_encoded'] = le_season.fit_transform(df['season'])

print(f"   ✓ Commodities: {len(le_commodity.classes_)} unique")
print(f"   ✓ Markets (Admin1): {len(le_admin.classes_)} unique")
print(f"   ✓ Seasons: {len(le_season.classes_)} unique")

# Define features and target
print("\n4. Preparing training data...")
feature_columns = [
    'commodity_encoded', 'admin_encoded', 'month', 'year',
    'price_lag1', 'price_lag2', 'price_lag3', 'rolling_mean_3', 'season_encoded'
]

X = df[feature_columns].values
y = df['price'].values

print(f"   ✓ Features shape: {X.shape}")
print(f"   ✓ Target shape: {y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   ✓ Train size: {len(X_train)}, Test size: {len(X_test)}")

# Train Random Forest model
print("\n5. Training Random Forest Regressor...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

model.fit(X_train, y_train)
print("   ✓ Model training complete")

# Evaluate the model
print("\n6. Evaluating model performance...")
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

train_mae = mean_absolute_error(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_r2 = r2_score(y_train, y_train_pred)

test_mae = mean_absolute_error(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_r2 = r2_score(y_test, y_test_pred)

print("\n   Training Set:")
print(f"   • MAE:  {train_mae:.2f} ETB")
print(f"   • RMSE: {train_rmse:.2f} ETB")
print(f"   • R²:   {train_r2:.4f}")

print("\n   Test Set:")
print(f"   • MAE:  {test_mae:.2f} ETB")
print(f"   • RMSE: {test_rmse:.2f} ETB")
print(f"   • R²:   {test_r2:.4f}")

# Save the model and encoders
print("\n7. Saving model and encoders...")
model_path = os.path.join(MODELS_DIR, 'crop_price_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
print(f"   ✓ Model saved: {model_path}")

le_commodity_path = os.path.join(MODELS_DIR, 'le_commodity.pkl')
with open(le_commodity_path, 'wb') as f:
    pickle.dump(le_commodity, f)
print(f"   ✓ Commodity encoder saved: {le_commodity_path}")

le_admin_path = os.path.join(MODELS_DIR, 'le_admin.pkl')
with open(le_admin_path, 'wb') as f:
    pickle.dump(le_admin, f)
print(f"   ✓ Admin encoder saved: {le_admin_path}")

le_season_path = os.path.join(MODELS_DIR, 'le_season.pkl')
with open(le_season_path, 'wb') as f:
    pickle.dump(le_season, f)
print(f"   ✓ Season encoder saved: {le_season_path}")

print("\n" + "=" * 60)
print("Training complete! Your Flask API should now work.")
print("=" * 60)
print(f"\nNext steps:")
print(f"1. Run: cd api")
print(f"2. Run: python app.py")
print(f"3. Test the API at: http://localhost:5000")
print("=" * 60)
