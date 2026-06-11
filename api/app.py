from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')
DATA_PATH = os.path.join(BASE_DIR, '..', 'Data', 'raw', 'wfp_food_prices_eth.csv')

# Load model and encoders
model = pickle.load(open(os.path.join(MODELS_DIR, 'crop_price_model.pkl'), 'rb'))
le_commodity = pickle.load(open(os.path.join(MODELS_DIR, 'le_commodity.pkl'), 'rb'))
le_admin = pickle.load(open(os.path.join(MODELS_DIR, 'le_admin.pkl'), 'rb'))
le_season = pickle.load(open(os.path.join(MODELS_DIR, 'le_season.pkl'), 'rb'))

# Load historical data once at startup
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.lower()  # normalize column names
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Season logic
def get_season(month):
    if month in [6, 7, 8, 9]:
        return 'kiremt'
    elif month in [3, 4, 5]:
        return 'belg'
    elif month in [10, 11, 12]:
        return 'harvest'
    else:
        return 'dry'

# Get lag features from historical data
def get_lag_features(commodity, admin, month, year):
    filtered = df[
        (df['commodity'] == commodity) &
        (df['admin1'] == admin)
    ].copy()

    if len(filtered) < 3:
        return None, "Not enough historical data for this crop/market combination"

    # Get rows before the requested date
    target_date = pd.Timestamp(year=year, month=month, day=1)
    past = filtered[filtered['date'] < target_date].tail(3)

    if len(past) < 3:
        return None, "Not enough past data before the selected date"

    prices = past['price'].values  # oldest to newest
    price_lag1 = prices[-1]
    price_lag2 = prices[-2]
    price_lag3 = prices[-3]
    rolling_mean_3 = np.mean([price_lag1, price_lag2, price_lag3])

    return {
        'price_lag1': price_lag1,
        'price_lag2': price_lag2,
        'price_lag3': price_lag3,
        'rolling_mean_3': rolling_mean_3
    }, None

@app.route('/')
def home():
    return jsonify({'message': 'EthioPrice API is running'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        commodity = data['commodity']
        admin = data['admin']
        month = int(data['month'])
        year = int(data['year'])

        # Auto-calculate lag features
        lags, error = get_lag_features(commodity, admin, month, year)
        if error:
            return jsonify({'error': error}), 400

        # Encode inputs
        commodity_encoded = le_commodity.transform([commodity])[0]
        admin_encoded = le_admin.transform([admin])[0]
        season = get_season(month)
        season_encoded = le_season.transform([season])[0]

        # Build feature array
        features = np.array([[
            commodity_encoded, admin_encoded, month, year,
            lags['price_lag1'], lags['price_lag2'], lags['price_lag3'],
            lags['rolling_mean_3'], season_encoded
        ]])

        prediction = model.predict(features)[0]

        return jsonify({
            'predicted_price': round(float(prediction), 2),
            'commodity': commodity,
            'market': admin,
            'month': month,
            'year': year,
            'season': season,
            'currency': 'ETB',
            'unit': '100kg'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/crops', methods=['GET'])
def get_crops():
    crops = le_commodity.classes_.tolist()
    return jsonify({'crops': crops})

@app.route('/markets', methods=['GET'])
def get_markets():
    markets = le_admin.classes_.tolist()
    return jsonify({'markets': markets})

if __name__ == '__main__':
    app.run(debug=True, port=5000)