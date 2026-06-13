from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Production-ready CORS configuration
# Uses environment variable for frontend URL, with fallback for local development
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://ethio-crop-price-predictor.vercel.app')
ALLOWED_ORIGINS = [
    'https://ethio-crop-price-predictor.vercel.app',
    'http://localhost:3000',
    'http://localhost:8080',
    'http://127.0.0.1:5000',
    'http://127.0.0.1:8080'
]

# Apply CORS globally with explicit configuration
CORS(app, 
     resources={r"/*": {
         "origins": ALLOWED_ORIGINS,
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True,
         "expose_headers": ["Content-Type"]
     }})

# Paths
# Get the absolute path to the api/ directory (where this file is)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Since models/ and data/ are now INSIDE api/ directory, use BASE_DIR directly
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'wfp_food_prices_eth.csv')

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

# Three-Tier Graceful Fallback Strategy
def get_lag_features_with_fallback(commodity, admin, month, year):
    """
    THREE-TIER FALLBACK STRATEGY:
    
    Tier 1 (BEST): 3+ historical data points
        → Use full lag features (lag1, lag2, lag3, rolling_mean_3)
        → data_quality: 'good'
        → No warning
    
    Tier 2 (LIMITED): 1-2 historical data points
        → Use most recent price as proxy for missing lags
        → data_quality: 'limited'
        → Warning: explains data limitation
    
    Tier 3 (FALLBACK): 0 historical data points for combination
        → Use global average for that commodity across all markets
        → data_quality: 'low'
        → Warning: explains using global average
    
    CRITICAL: Never return error for missing data - always provide estimate
    """
    
    # Filter data for the specific commodity/market combination
    filtered = df[
        (df['commodity'] == commodity) &
        (df['admin1'] == admin)
    ].copy()

    # Get rows before the requested date
    target_date = pd.Timestamp(year=year, month=month, day=1)
    past = filtered[filtered['date'] < target_date].sort_values('date')

    # Count available historical data points
    num_prices = len(past)
    
    # ========================================================================
    # TIER 1: 3+ Historical Data Points (BEST CASE)
    # ========================================================================
    if num_prices >= 3:
        prices = past['price'].values  # oldest to newest
        price_lag1 = float(prices[-1])
        price_lag2 = float(prices[-2])
        price_lag3 = float(prices[-3])
        rolling_mean_3 = float(np.mean([price_lag1, price_lag2, price_lag3]))
        
        return {
            'price_lag1': price_lag1,
            'price_lag2': price_lag2,
            'price_lag3': price_lag3,
            'rolling_mean_3': rolling_mean_3,
            'data_quality': 'good',
            'warning': None
        }
    
    # ========================================================================
    # TIER 2: 1-2 Historical Data Points (LIMITED DATA)
    # ========================================================================
    elif num_prices >= 1:
        prices = past['price'].values
        price_lag1 = float(prices[-1])  # Most recent available
        
        if num_prices == 2:
            price_lag2 = float(prices[-2])
            price_lag3 = price_lag2  # Use lag2 as proxy for lag3
            rolling_mean_3 = float(np.mean([price_lag1, price_lag2]))
            warning = f'Limited data: Only 2 historical prices found for {commodity} in {admin}. Using most recent prices with intelligent fallback.'
        else:  # num_prices == 1
            price_lag2 = price_lag1  # Use same price as proxy
            price_lag3 = price_lag1
            rolling_mean_3 = price_lag1
            warning = f'Limited data: Only 1 historical price found for {commodity} in {admin}. Using {price_lag1:.2f} ETB as baseline estimate.'
        
        return {
            'price_lag1': price_lag1,
            'price_lag2': price_lag2,
            'price_lag3': price_lag3,
            'rolling_mean_3': rolling_mean_3,
            'data_quality': 'limited',
            'warning': warning
        }
    
    # ========================================================================
    # TIER 3: 0 Historical Data Points (GLOBAL FALLBACK)
    # ========================================================================
    else:
        # Calculate global average for this commodity across ALL markets
        global_commodity_data = df[df['commodity'] == commodity]
        
        if len(global_commodity_data) > 0:
            # Use global average for this commodity
            global_avg_price = float(np.mean(global_commodity_data['price'].values))
            
            warning = f'No historical data for {commodity} in {admin}. Using global average price ({global_avg_price:.2f} ETB) across all markets as fallback estimate.'
            
            return {
                'price_lag1': global_avg_price,
                'price_lag2': global_avg_price,
                'price_lag3': global_avg_price,
                'rolling_mean_3': global_avg_price,
                'data_quality': 'low',
                'warning': warning
            }
        else:
            # Extremely rare: commodity exists in encoder but not in dataset
            # Use overall dataset average as last resort
            overall_avg_price = float(np.mean(df['price'].values))
            
            warning = f'Critical fallback: No data for {commodity} anywhere. Using dataset-wide average ({overall_avg_price:.2f} ETB) as rough estimate.'
            
            return {
                'price_lag1': overall_avg_price,
                'price_lag2': overall_avg_price,
                'price_lag3': overall_avg_price,
                'rolling_mean_3': overall_avg_price,
                'data_quality': 'low',
                'warning': warning
            }

@app.route('/', methods=['GET'])
def home():
    """Root endpoint - health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'EthioPrice API is running',
        'version': '1.0.0',
        'endpoints': {
            'health': '/',
            'crops': '/crops',
            'markets': '/markets',
            'predict': '/predict (POST)'
        }
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Alternative health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'EthioPrice API is running'
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    THREE-TIER GRACEFUL FALLBACK PREDICTION ENDPOINT
    
    Returns 200 OK for ALL valid inputs, even with zero historical data.
    Only returns 400 for INVALID inputs (bad commodity, missing fields, etc.)
    
    Response always includes:
    - predicted_price: float (always present)
    - data_quality: 'good' | 'limited' | 'low'
    - warning: string (optional, present when data_quality != 'good')
    """
    try:
        # ====================================================================
        # VALIDATION PHASE: Only return 400 for INVALID inputs
        # ====================================================================
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided in request body'}), 400

        # Extract and validate required fields
        required_fields = ['commodity', 'admin', 'month', 'year']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        commodity = data['commodity']
        admin = data['admin']
        
        # Validate month and year are integers
        try:
            month = int(data['month'])
            year = int(data['year'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Month and year must be valid integers'}), 400

        # Validate month range
        if not (1 <= month <= 12):
            return jsonify({'error': 'Month must be between 1 and 12'}), 400

        # Validate year range (reasonable bounds)
        if not (2000 <= year <= 2050):
            return jsonify({'error': 'Year must be between 2000 and 2050'}), 400

        # Validate commodity exists in trained model
        if commodity not in le_commodity.classes_:
            available = ', '.join(le_commodity.classes_[:5])
            return jsonify({
                'error': f'Unknown commodity: "{commodity}". Available: {available}... (use /crops endpoint for full list)'
            }), 400

        # Validate market exists in trained model
        if admin not in le_admin.classes_:
            available = ', '.join(le_admin.classes_[:5])
            return jsonify({
                'error': f'Unknown market: "{admin}". Available: {available}... (use /markets endpoint for full list)'
            }), 400

        # ====================================================================
        # PREDICTION PHASE: Always return 200 OK with intelligent estimate
        # ====================================================================
        
        # Apply three-tier fallback strategy
        lag_features = get_lag_features_with_fallback(commodity, admin, month, year)
        
        # Encode inputs for model
        commodity_encoded = le_commodity.transform([commodity])[0]
        admin_encoded = le_admin.transform([admin])[0]
        season = get_season(month)
        season_encoded = le_season.transform([season])[0]

        # Build feature array for prediction
        features = np.array([[
            commodity_encoded, 
            admin_encoded, 
            month, 
            year,
            lag_features['price_lag1'], 
            lag_features['price_lag2'], 
            lag_features['price_lag3'],
            lag_features['rolling_mean_3'], 
            season_encoded
        ]])

        # Generate prediction using trained model
        prediction = model.predict(features)[0]

        # ====================================================================
        # RESPONSE CONSTRUCTION: Consistent structure for all cases
        # ====================================================================
        
        response = {
            'predicted_price': round(float(prediction), 2),
            'commodity': commodity,
            'market': admin,
            'month': month,
            'year': year,
            'season': season,
            'currency': 'ETB',
            'unit': '100kg',
            'data_quality': lag_features['data_quality']
        }

        # Add warning if data quality is not optimal
        if lag_features['warning']:
            response['warning'] = lag_features['warning']

        # Return 200 OK even with limited or low quality data
        return jsonify(response), 200

    # ========================================================================
    # ERROR HANDLING: Only for unexpected errors, not missing data
    # ========================================================================
    
    except KeyError as e:
        return jsonify({
            'error': f'Missing or invalid field: {str(e)}'
        }), 400
    
    except ValueError as e:
        return jsonify({
            'error': f'Value error: {str(e)}'
        }), 400
    
    except Exception as e:
        # Log unexpected errors (use proper logging in production)
        print(f"[ERROR] Unexpected error in /predict: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': 'An unexpected server error occurred. Please try again or contact support.',
            'details': str(e) if app.debug else None
        }), 500

@app.route('/crops', methods=['GET'])
def get_crops():
    """Get list of all available crops/commodities"""
    try:
        crops = le_commodity.classes_.tolist()
        return jsonify({
            'crops': crops,
            'count': len(crops)
        }), 200
    except Exception as e:
        print(f"[ERROR] Error in /crops: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve crops list',
            'details': str(e) if app.debug else None
        }), 500

@app.route('/markets', methods=['GET'])
def get_markets():
    """Get list of all available markets"""
    try:
        markets = le_admin.classes_.tolist()
        return jsonify({
            'markets': markets,
            'count': len(markets)
        }), 200
    except Exception as e:
        print(f"[ERROR] Error in /markets: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve markets list',
            'details': str(e) if app.debug else None
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested URL was not found on this server',
        'available_endpoints': {
            'health': 'GET /',
            'crops': 'GET /crops',
            'markets': 'GET /markets',
            'predict': 'POST /predict'
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    # Production-ready configuration
    # debug=False for production, use environment variable PORT
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=port,
        debug=debug_mode  # False by default, True only if FLASK_ENV=development
    )