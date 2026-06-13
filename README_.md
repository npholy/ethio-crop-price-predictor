# 🌾 EthioPrice - AI-Powered Crop Price Prediction for Ethiopia

<div align="center">

![Status](https://img.shields.io/badge/status-production--ready-success)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

**A full-stack AI application providing intelligent crop price forecasting for the Ethiopian agricultural market.**

[Live Demo](#) • [Documentation](PRODUCTION_DEPLOYMENT_GUIDE.md) • [API Reference](api/FALLBACK_QUICK_REFERENCE.md)

</div>

---

## 📖 Overview

**EthioPrice** is an enterprise-grade, production-ready crop price prediction system designed specifically for the Ethiopian agricultural market. Built with a **three-tier graceful fallback strategy**, the application ensures predictions are always available—even with limited or zero historical data—making it robust enough for real-world deployment where data availability varies significantly across regions and commodities.

### The Problem

Agricultural stakeholders in Ethiopia often lack reliable price forecasting tools, leading to:
- Suboptimal planting decisions
- Unfavorable selling timing
- Market information asymmetry
- Economic losses for farmers and traders

### The Solution

EthioPrice combines machine learning with intelligent fallback mechanisms to provide:
- **Always-available predictions** (never fails due to missing data)
- **Transparent data quality indicators** (users know prediction reliability)
- **Premium user experience** (Stripe/Apple Finance-inspired design)
- **Responsive accessibility** (works on desktop, tablet, and mobile)

---

## ✨ Key Features

### 🎨 **Premium User Interface**
- **Glassmorphism Design**: Modern, Apple-inspired aesthetic with backdrop blur effects
- **Layered Shadows**: 8-level shadow system for depth perception
- **Smooth Micro-interactions**: Cubic-bezier animations on all interactive elements
- **Responsive Layout**: Fluid typography with `clamp()`, mobile-first design
- **Accessibility**: WCAG-compliant touch targets (min 44px), semantic HTML

### 🧠 **Three-Tier Fallback Intelligence**
- **Tier 1 (Good)**: Uses full lag features with 3+ historical data points → 80% confidence
- **Tier 2 (Limited)**: Proxies missing lags with 1-2 data points → 60% confidence + amber warning
- **Tier 3 (Low)**: Falls back to global commodity average with 0 data points → 40% confidence + amber warning
- **Critical**: Always returns 200 OK for valid inputs; never crashes on missing data

### 🤖 **Machine Learning Backend**
- **Algorithm**: Random Forest Regressor with engineered features
- **Features**: Lag prices (1-3 months), rolling averages, seasonal encoding
- **Robustness**: Handles missing data gracefully via intelligent fallback
- **Performance**: Sub-second prediction response times

### 📱 **Fully Responsive Design**
- **Desktop**: Two-column layout with side-by-side form and chart
- **Tablet**: Single-column stacked layout (< 1024px)
- **Mobile**: Optimized spacing, larger touch targets, 16px inputs (prevents iOS zoom)
- **Fluid Scaling**: Typography and charts scale naturally across all screen sizes

### 📊 **Interactive Visualizations**
- **Chart.js Integration**: Smooth bezier curves with historical + predicted data
- **Market Insights**: Trend analysis, volatility index, market positioning
- **Real-time Updates**: Live API status indicator and form validation

---

## 🏗️ Architecture

### Tech Stack

#### **Backend (Flask API)**
```
Python 3.11+
├── Flask 3.0          # Web framework
├── Flask-CORS 4.0     # Cross-origin resource sharing
├── Scikit-learn 1.3   # Machine learning (Random Forest)
├── Pandas 2.1         # Data manipulation
├── NumPy 1.26         # Numerical computing
└── Gunicorn 21.2      # Production WSGI server
```

**Key Backend Features:**
- RESTful API with 4 endpoints (`/`, `/crops`, `/markets`, `/predict`)
- Production-ready CORS configuration with environment variables
- Three-tier fallback strategy for missing data
- Absolute path resolution (Windows/Linux compatible)
- Comprehensive error handling and logging

#### **Frontend (Static Web App)**
```
Vanilla JavaScript (ES6+)
├── HTML5              # Semantic markup
├── CSS3               # Grid, Flexbox, CSS Variables
├── Chart.js 4.4       # Interactive data visualization
└── Inter Font         # Premium typography
```

**Key Frontend Features:**
- No framework dependencies (lightweight, fast)
- Environment-aware API URL detection
- Responsive CSS with media queries (1024px, 768px, 480px)
- Form validation and error handling
- Amber warning system for data quality transparency

#### **Machine Learning Pipeline**
```
Data → Feature Engineering → Model Training → Prediction
  ↓            ↓                    ↓             ↓
CSV File   Lag Features      Random Forest    JSON API
           Rolling Avg       (80% Accuracy)   Response
           Seasonal
```

### System Architecture

```
┌─────────────────┐         HTTPS          ┌──────────────────┐
│   Vercel CDN    │ ◄───────────────────► │   Render Cloud   │
│   (Frontend)    │      CORS Enabled      │   (Flask API)    │
└────────┬────────┘                        └────────┬─────────┘
         │                                          │
         │                                          │
    ┌────▼────┐                               ┌────▼─────┐
    │ Browser │                               │  Model   │
    │  User   │                               │  Pickle  │
    └─────────┘                               └──────────┘
                                                    │
                                               ┌────▼─────┐
                                               │   CSV    │
                                               │   Data   │
                                               └──────────┘
```

### Deployment Strategy

**Dual-Deployment Model:**

| Component | Platform | Purpose | Configuration |
|-----------|----------|---------|---------------|
| **Backend** | Render | Flask API with ML models | `api/Procfile`, `requirements.txt` |
| **Frontend** | Vercel | Static web dashboard | `web/vercel.json` |

**Why Two Platforms?**
1. **Separation of Concerns**: Backend logic isolated from frontend presentation
2. **Scalability**: Each component scales independently based on demand
3. **Security**: API can implement rate limiting, authentication without affecting frontend
4. **Cost Efficiency**: Vercel excels at static hosting (fast, free); Render handles Python well
5. **CI/CD**: Both platforms offer automatic deployment on Git push

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Web Browser** (Chrome, Firefox, Edge, or Safari)

### Local Development Setup

#### **Step 1: Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/ethio-crop-price-predictor.git
cd ethio-crop-price-predictor
```

#### **Step 2: Set Up Backend (Flask API)**

```bash
# Navigate to API directory
cd api

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the model (if models not present)
cd ..
python train_model.py

# Start Flask API
cd api
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

✅ **Backend is now running at** `http://127.0.0.1:5000`

#### **Step 3: Serve Frontend (Dashboard)**

**Option A: Python HTTP Server** (Recommended)

```bash
# Open a NEW terminal window
cd web
python -m http.server 8080
```

**Option B: Direct File Access**

Navigate to `web/index.html` in your file explorer and open with your browser.

⚠️ *Note: Some features may be limited with `file://` protocol due to CORS restrictions.*

#### **Step 4: Open Dashboard**

Open your browser to:
```
http://localhost:8080/
```

You should see the EthioPrice dashboard with:
- ✅ Green "EthioPrice" header
- ✅ Status indicator (should show "Connected to API")
- ✅ Form with commodity, market, month, year dropdowns
- ✅ Chart visualization area

---

## 🎯 Usage

### Making Predictions

1. **Select Parameters:**
   - Choose a commodity (e.g., Maize, Wheat, Sorghum)
   - Choose a market region (e.g., Addis Ababa, Tigray)
   - Select month and year

2. **Generate Prediction:**
   - Click "Generate Prediction" button
   - Wait 1-2 seconds for API response

3. **View Results:**
   - Predicted price displayed prominently
   - Confidence score with color-coded indicator
   - Historical trend chart
   - Market insights (trend, volatility, position)
   - Data quality warnings (if applicable)

### Understanding Data Quality

| Quality | Confidence | Meaning | Warning |
|---------|-----------|---------|---------|
| **Good** | 80%+ | 3+ historical data points available | None |
| **Limited** | ~60% | 1-2 historical data points; using proxy | Amber alert shown |
| **Low** | ~40% | 0 historical data points; using global average | Amber alert shown |

### API Usage

**Base URL (Local):** `http://127.0.0.1:5000`

#### **Endpoints:**

**1. Health Check**
```bash
GET /
```
Response:
```json
{"message": "EthioPrice API is running"}
```

**2. List Available Commodities**
```bash
GET /crops
```
Response:
```json
{
  "crops": ["Maize", "Wheat", "Sorghum", "Barley", ...]
}
```

**3. List Available Markets**
```bash
GET /markets
```
Response:
```json
{
  "markets": ["Addis Ababa", "Tigray", "Afar", ...]
}
```

**4. Predict Price**
```bash
POST /predict
Content-Type: application/json

{
  "commodity": "Maize",
  "admin": "Addis Ababa",
  "month": 6,
  "year": 2024
}
```
Response:
```json
{
  "predicted_price": 4250.75,
  "data_quality": "good",
  "commodity": "Maize",
  "market": "Addis Ababa",
  "month": 6,
  "year": 2024,
  "season": "kiremt",
  "currency": "ETB",
  "unit": "100kg",
  "warning": null
}
```

---

## 🌐 Production Deployment

### Overview

Deploy the backend and frontend to separate platforms for optimal performance and scalability.

### Quick Deployment Steps

#### **1. Prepare Repository**

```bash
# Commit all changes
git add .
git commit -m "Production ready"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/ethioprice.git
git push -u origin main
```

#### **2. Deploy Backend to Render**

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ethioprice-api`
   - **Root Directory**: `api`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**:
     ```
     FRONTEND_URL=https://your-app.vercel.app
     FLASK_ENV=production
     ```
5. Click **"Create Web Service"**
6. **Save your Render URL**: `https://ethioprice-api.onrender.com`

#### **3. Deploy Frontend to Vercel**

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: `Other`
   - **Root Directory**: `web`
   - **Build Command**: *(leave empty)*
   - **Output Directory**: `./`
   - **Environment Variables**:
     ```
     API_URL=https://ethioprice-api.onrender.com
     ```
5. Click **"Deploy"**
6. **Save your Vercel URL**: `https://ethioprice.vercel.app`

#### **4. Update CORS Configuration**

1. Return to Render dashboard
2. Go to **Environment** tab
3. Update `FRONTEND_URL` with your actual Vercel URL
4. Click **"Save"** and manually redeploy

#### **5. Verify Deployment**

```bash
# Test backend
curl https://ethioprice-api.onrender.com/

# Test frontend
Open: https://ethioprice.vercel.app
```

### Detailed Deployment Guide

For comprehensive deployment instructions, see:
- **[PRODUCTION_DEPLOYMENT_GUIDE.md](PRODUCTION_DEPLOYMENT_GUIDE.md)** - Full step-by-step guide
- **[DEPLOYMENT_QUICK_REFERENCE.md](DEPLOYMENT_QUICK_REFERENCE.md)** - Quick command reference

---

## 📁 Project Structure

```
ethio-crop-price-predictor/
│
├── api/                              # Backend (Flask API) - Deploy to Render
│   ├── app.py                        # Main Flask application with three-tier fallback
│   ├── requirements.txt              # Python dependencies
│   ├── Procfile                      # Gunicorn configuration for Render
│   ├── runtime.txt                   # Python version specification
│   ├── .env.example                  # Environment variable template
│   ├── FALLBACK_QUICK_REFERENCE.md   # API documentation
│   └── .venv/                        # Virtual environment (local only, not deployed)
│
├── web/                              # Frontend (Static App) - Deploy to Vercel
│   ├── index.html                    # Main dashboard with premium responsive CSS
│   ├── script.js                     # Frontend logic with environment-aware API calls
│   ├── vercel.json                   # Vercel deployment configuration
│   ├── .env.example                  # Environment variable template
│   ├── README.md                     # Frontend documentation
│   ├── DESIGN_SPEC.md                # Design requirements
│   ├── PREMIUM_DESIGN_IMPLEMENTATION.md  # Design system details
│   └── QUICKSTART.md                 # Quick setup guide
│
├── data/                             # Data files
│   └── raw/
│       └── wfp_food_prices_eth.csv   # Historical price data (World Food Programme)
│
├── models/                           # Machine learning models
│   ├── crop_price_model.pkl          # Trained Random Forest model
│   ├── le_admin.pkl                  # LabelEncoder for markets
│   ├── le_commodity.pkl              # LabelEncoder for commodities
│   └── le_season.pkl                 # LabelEncoder for seasons
│
├── notebooks/                        # Jupyter notebooks for exploration
│   └── 01_data_exploration.ipynb     # Exploratory data analysis
│
├── train_model.py                    # Model training script
├── test_final.py                     # Comprehensive test suite (7 tests)
├── diagnose_404.py                   # HTTP server diagnostic tool
│
├── README.md                         # Main project documentation (this file)
├── PRODUCTION_DEPLOYMENT_GUIDE.md    # Comprehensive deployment guide
├── DEPLOYMENT_QUICK_REFERENCE.md     # Quick deployment commands
├── PRODUCTION_READY_SUMMARY.md       # Production readiness overview
├── PROJECT_COMPLETION_SUMMARY.md     # Complete feature documentation
├── QUICK_REFERENCE.md                # Local development reference
├── TRAINING_GUIDE.md                 # Model training instructions
├── THREE_TIER_FALLBACK_IMPLEMENTATION.md  # Fallback strategy details
│
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
└── .git/                             # Git repository
```

---

## 🧪 Testing

### Manual Testing

#### **Test Backend Locally:**

```bash
# Health check
curl http://127.0.0.1:5000/

# Get available crops
curl http://127.0.0.1:5000/crops

# Get available markets
curl http://127.0.0.1:5000/markets

# Test prediction
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "commodity": "Maize",
    "admin": "Addis Ababa",
    "month": 6,
    "year": 2024
  }'
```

#### **Test Frontend:**

1. Open `http://localhost:8080/` in browser
2. Open DevTools (F12) and check Console for errors
3. Test form submission with different commodities and markets
4. Verify charts render correctly
5. Test on mobile viewport (DevTools → Toggle Device Toolbar)

### Automated Testing

Run the comprehensive test suite:

```bash
python test_final.py
```

**Test Coverage:**
- ✅ Tier 1: Common commodities with good data
- ✅ Tier 2: Uncommon combinations with limited data
- ✅ Tier 3: Rare combinations with zero data (global fallback)
- ✅ Invalid inputs (returns 400 errors)

**Expected Output:** 7/7 tests pass (100%)

---

## 🐛 Troubleshooting

### Common Issues

#### **Issue 1: "API Offline" Status**

**Symptom:** Frontend shows red "API Offline" indicator

**Solutions:**
1. Verify Flask API is running: `curl http://127.0.0.1:5000/`
2. Check API URL in `web/script.js` (line 4-8)
3. Ensure no firewall blocking port 5000
4. Check Flask terminal for error messages

#### **Issue 2: CORS Errors in Browser**

**Symptom:** Console shows "blocked by CORS policy"

**Solutions:**
1. Verify `flask-cors` is installed: `pip install flask-cors`
2. Check `FRONTEND_URL` environment variable in production
3. Ensure Render app has been redeployed after updating env vars
4. Verify no trailing slashes in URLs

#### **Issue 3: 404 Error on Frontend**

**Symptom:** Browser shows "404 Not Found"

**Solutions:**
1. Ensure HTTP server is running from `web/` directory:
   ```bash
   cd web
   python -m http.server 8080
   ```
2. Check current directory: `cd` (should show `/web`)
3. Verify `index.html` exists: `dir index.html` (Windows) or `ls index.html` (Linux/macOS)
4. Try different port: `python -m http.server 8081`

**Detailed troubleshooting:** See [404_FIX_SUMMARY.md](404_FIX_SUMMARY.md)

#### **Issue 4: Predictions Return 500 Error**

**Symptom:** API returns 500 Internal Server Error

**Solutions:**
1. Check Flask logs for error details
2. Verify model files exist in `models/` directory
3. Ensure data file exists: `data/raw/wfp_food_prices_eth.csv`
4. Check all dependencies installed: `pip install -r requirements.txt`
5. Retrain model if needed: `python train_model.py`

#### **Issue 5: Mobile Layout Broken**

**Symptom:** Horizontal scroll or overlapping elements on mobile

**Solutions:**
1. Clear browser cache: Ctrl + Shift + R (hard refresh)
2. Check viewport meta tag is present in HTML
3. Test in browser DevTools mobile emulation
4. Verify no `min-width` constraints on containers

---

## 📊 Performance

### Benchmarks

| Metric | Development | Production (Render + Vercel) |
|--------|-------------|------------------------------|
| **Backend Response Time** | <200ms | <500ms (warm), ~30s (cold start) |
| **Frontend Load Time** | <1s | <2s (global CDN) |
| **Prediction Latency** | <300ms | <600ms |
| **Time to Interactive** | <1s | <3s |

**Note:** Render free tier has cold starts after 15 minutes of inactivity. Upgrade to paid plan for always-on performance.

### Optimization Tips

**Backend:**
- Use Render's paid plan to avoid cold starts
- Implement Redis caching for frequently accessed predictions
- Consider batch prediction endpoints for bulk requests

**Frontend:**
- Assets are automatically cached by Vercel's CDN
- Chart.js loads from CDN with caching
- Consider adding service worker for offline support

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** with clear, descriptive commits
4. **Test thoroughly**: Run `python test_final.py` and manual tests
5. **Update documentation** if adding features
6. **Submit a pull request** with a clear description

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions focused and modular

**JavaScript:**
- Use ES6+ features
- Follow Airbnb JavaScript Style Guide
- Add JSDoc comments for functions
- Use meaningful variable names

**CSS:**
- Follow BEM naming convention
- Use CSS variables for theming
- Mobile-first responsive design
- Comment complex selectors

### Reporting Issues

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, browser, Python version)

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
Copyright (c) 2026 EthioPrice Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

### Data Source
- **World Food Programme (WFP)** - Historical crop price data for Ethiopia
  - [WFP Data Portal](https://data.humdata.org/organization/wfp)

### Technologies & Libraries
- **[Flask](https://flask.palletsprojects.com/)** - Python web framework
- **[Scikit-learn](https://scikit-learn.org/)** - Machine learning library
- **[Chart.js](https://www.chartjs.org/)** - JavaScript charting library
- **[Inter Font](https://rsms.me/inter/)** - Premium typography by Rasmus Andersson

### Design Inspiration
- **[Stripe Dashboard](https://stripe.com/)** - Clean, modern UI patterns
- **[Apple Finance](https://www.apple.com/)** - Glassmorphism effects
- **[Linear](https://linear.app/)** - Smooth animations
- **[Vercel](https://vercel.com/)** - Layered shadows and spacing

### Deployment Platforms
- **[Render](https://render.com/)** - Flask API hosting
- **[Vercel](https://vercel.com/)** - Frontend static hosting

---

## 📞 Support

### Documentation

- **[Full Deployment Guide](PRODUCTION_DEPLOYMENT_GUIDE.md)** - Comprehensive deployment instructions
- **[Quick Reference](QUICK_REFERENCE.md)** - Common commands and tasks
- **[API Reference](api/FALLBACK_QUICK_REFERENCE.md)** - API endpoint documentation
- **[Training Guide](TRAINING_GUIDE.md)** - Model training instructions

### Get Help

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/ethio-crop-price-predictor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/ethio-crop-price-predictor/discussions)

### Project Status

- **Version**: 2.0 (Production Ready)
- **Status**: ✅ Active Development
- **Deployment**: Render (Backend) + Vercel (Frontend)
- **Last Updated**: June 13, 2026

---

## 🗺️ Roadmap

### Completed ✅
- [x] Three-tier graceful fallback system
- [x] Premium responsive UI with glassmorphism
- [x] Random Forest model with lag features
- [x] Production deployment guides
- [x] Comprehensive documentation
- [x] Automated test suite

### Planned 🚧
- [ ] User authentication and saved predictions
- [ ] Historical data export (CSV/Excel)
- [ ] Multi-commodity comparison view
- [ ] Real-time price alerts
- [ ] Mobile native app (React Native)
- [ ] Admin dashboard for data management
- [ ] Dark mode theme
- [ ] Multi-language support (Amharic, Tigrinya, Oromo)

---

## 💎 Project Highlights

### Why This Project Stands Out

1. **Production-Ready**: Not a proof-of-concept; fully deployable with CI/CD
2. **Robust Error Handling**: Never crashes on missing data (three-tier fallback)
3. **User-Focused Design**: Premium UI/UX with transparent data quality indicators
4. **Comprehensive Documentation**: 15+ markdown files covering every aspect
5. **Modern Best Practices**: Environment variables, CORS, responsive design, accessibility
6. **Test Coverage**: Automated tests verify all three fallback tiers
7. **Dual-Platform Deployment**: Optimized for both Render and Vercel

### Technical Achievements

- **Glassmorphism Effects**: `backdrop-filter` with fallbacks
- **Fluid Typography**: `clamp()` for responsive text scaling
- **Layered Shadows**: 8-level depth system
- **WCAG Compliant**: Minimum 44px touch targets, semantic HTML
- **Sub-Second Predictions**: Optimized ML inference
- **Zero-Data Predictions**: Global fallback ensures 100% availability

---

<div align="center">

**Built with ❤️ for Ethiopian Agriculture**

[⬆ Back to Top](#-ethioprice---ai-powered-crop-price-prediction-for-ethiopia)

</div>
