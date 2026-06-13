# EthioPrice Web Frontend

## 🎨 Enterprise-Grade Crop Price Intelligence Dashboard

A premium, production-ready web interface for the Ethiopian Crop Price Predictor API. Built with modern web standards, Apple/Stripe-inspired design principles, and enterprise UX patterns.

---

## ✨ Features

### Design & UX
- **Premium Visual Design**: Clean, modern aesthetic with generous whitespace and subtle shadows
- **Financial Green Palette**: Professional color scheme (#1D9E75) with sophisticated off-white backgrounds
- **Responsive Layout**: Mobile-first CSS Grid/Flexbox implementation
- **Smooth Animations**: CSS transitions for loading states and result reveals
- **Professional Typography**: Inter font family with carefully calibrated weights

### Functionality
- **Real-time API Integration**: Seamless connection to Flask backend at `http://127.0.0.1:5000`
- **Dynamic Dropdowns**: Auto-populated commodity and market selections from API
- **Interactive Chart**: Chart.js visualization with historical trends and predictions
- **Market Insights**: AI-powered trend analysis, volatility assessment, and market positioning
- **Confidence Scoring**: Visual progress bar showing model confidence levels
- **Error Handling**: Graceful error states with user-friendly messaging
- **API Status Indicator**: Live connection monitoring with pulse animation

### Technical Highlights
- **Pure Vanilla JavaScript**: No framework dependencies, ultra-fast performance
- **Chart.js Integration**: Professional data visualization with custom styling
- **Form Validation**: Client-side validation before API requests
- **Loading States**: Button spinners and opacity changes during async operations
- **Accessibility Ready**: Semantic HTML with proper ARIA considerations

---

## 🚀 Getting Started

### Prerequisites

1. **Flask API Running**: Ensure your Flask backend is running at `http://127.0.0.1:5000`
   ```bash
   cd api
   python app.py
   ```

2. **Model Trained**: Make sure `crop_price_model.pkl` exists in the `models/` directory
   ```bash
   python train_model.py  # If not already trained
   ```

### Quick Start

1. **Navigate to the web directory**:
   ```bash
   cd web
   ```

2. **Open in browser** (any of these methods):
   
   **Method A: Simple file open**
   ```bash
   # Just double-click index.html
   ```
   
   **Method B: Python HTTP Server** (Recommended)
   ```bash
   python -m http.server 8080
   # Then visit: http://localhost:8080
   ```
   
   **Method C: VS Code Live Server**
   - Install "Live Server" extension
   - Right-click `index.html` → "Open with Live Server"

3. **Verify API Connection**:
   - Check the status indicator in the top-right corner
   - Should show green pulse dot + "Connected to API"
   - If offline, ensure Flask is running on port 5000

---

## 📐 Architecture

### File Structure
```
web/
├── index.html       # Main HTML structure, styles, and layout
├── script.js        # Application logic, API integration, chart handling
└── README.md        # This file
```

### API Integration Points

#### Endpoint: `GET /crops`
- **Purpose**: Load commodity dropdown options
- **Response**: `{ "crops": ["Maize", "Wheat", ...] }`

#### Endpoint: `GET /markets`
- **Purpose**: Load market region dropdown options
- **Response**: `{ "markets": ["Addis Ababa", "Tigray", ...] }`

#### Endpoint: `POST /predict`
- **Purpose**: Generate price predictions
- **Request Body**:
  ```json
  {
    "commodity": "Maize",
    "admin": "Addis Ababa",
    "month": 6,
    "year": 2024
  }
  ```
- **Response**:
  ```json
  {
    "predicted_price": 1250.75,
    "commodity": "Maize",
    "market": "Addis Ababa",
    "month": 6,
    "year": 2024,
    "season": "kiremt",
    "currency": "ETB",
    "unit": "100kg"
  }
  ```

---

## 🎨 Design System

### Color Palette
```css
--primary-green: #1D9E75        /* Brand, success, growth */
--primary-green-hover: #178866  /* Interactive states */
--primary-green-light: rgba(29, 158, 117, 0.1)  /* Backgrounds */
--background: #F5F5F0           /* Page background */
--card-bg: #FFFFFF              /* Card surfaces */
--text-primary: #2C3E50         /* Headings, primary text */
--text-secondary: #64748B       /* Secondary text */
--text-muted: #94A3B8           /* Placeholders, labels */
--error-red: #EF4444            /* Error states */
--warning-amber: #F59E0B        /* Predictions, warnings */
```

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300 (Light), 400 (Regular), 500 (Medium), 600 (Semi-Bold), 700 (Bold)
- **Scale**: 
  - Headings: 1.5rem → 1.25rem
  - Body: 0.9375rem (15px)
  - Small: 0.875rem (14px)
  - Micro: 0.75rem (12px)

### Spacing System
- **Card Padding**: 2rem (32px)
- **Form Groups**: 1.5rem margin-bottom
- **Section Gaps**: 2rem grid gap
- **Element Gaps**: 0.5rem → 1rem

### Shadow Elevation
```css
--shadow-sm:  0 1px 2px rgba(0,0,0,0.05)          /* Subtle hover */
--shadow-md:  0 4px 6px rgba(0,0,0,0.1)           /* Cards */
--shadow-lg:  0 10px 15px rgba(0,0,0,0.1)         /* Elevated cards */
--shadow-xl:  0 20px 25px rgba(0,0,0,0.1)         /* Modals */
```

---

## 🔧 Customization

### Changing API Endpoint
Edit the `API_BASE_URL` in `script.js`:
```javascript
const API_BASE_URL = 'http://your-api-url:5000';
```

### Adjusting Chart Colors
Modify the chart initialization in `script.js`:
```javascript
borderColor: '#1D9E75',           // Line color
backgroundColor: 'rgba(29, 158, 117, 0.1)',  // Fill color
```

### Modifying Confidence Calculation
Update the `calculateConfidence()` function in `script.js`:
```javascript
function calculateConfidence(data) {
    let confidence = 75;  // Base confidence
    // Add your custom logic here
    return confidence;
}
```

---

## 📊 Features in Detail

### 1. Price Prediction Form
- **Commodity Selection**: Dynamically loaded from `/crops` endpoint
- **Market Selection**: Dynamically loaded from `/markets` endpoint
- **Month Picker**: 12-month dropdown (January → December)
- **Year Input**: Number field with min/max validation (2020-2030)
- **Submit Button**: Loading state with spinner during API calls

### 2. Price Forecast Visualization
- **Chart.js Line Chart**: Smooth bezier curves with historical + predicted data
- **6-Month Historical View**: Synthetic data generation for context
- **Prediction Marker**: Dashed line with amber color (#F59E0B)
- **Minimalist Tooltips**: Clean design matching overall aesthetic
- **No Grid Lines**: Removed for cleaner, more professional look

### 3. Price Display Card
- **Large Price Value**: 3rem font, Financial Green (#1D9E75)
- **Currency & Unit**: ETB per 100kg from API response
- **Gradient Background**: Subtle green gradient for emphasis

### 4. Model Confidence Score
- **Percentage Display**: 70-95% range (simulated)
- **Progress Bar**: Animated fill with 1s transition
- **Visual Indicator**: Green gradient progress fill

### 5. Market Insights
Three insight cards with icons:

**📈 Price Trend**
- Rising (↗): > +5% change
- Stable (→): -5% to +5% change
- Falling (↘): < -5% change

**📊 Volatility Index**
- Low: CV < 10%
- Moderate: CV 10-20%
- High: CV > 20%

**🌍 Market Position**
- Relative to regional average (simulated)
- Positive % = above average
- Negative % = below average

---

## 🐛 Troubleshooting

### Issue: "API Offline" Status
**Solution**:
1. Check Flask is running: `cd api && python app.py`
2. Verify port 5000 is not blocked
3. Check browser console for CORS errors

### Issue: Empty Dropdowns
**Solution**:
1. Ensure `/crops` and `/markets` endpoints return data
2. Check if label encoders are loaded correctly
3. Verify CORS is enabled in Flask (`flask_cors`)

### Issue: "Not enough historical data" Error
**Solution**:
1. Try different commodity/market combinations
2. Ensure dataset has sufficient historical records
3. Check if `data/raw/wfp_food_prices_eth.csv` is loaded

### Issue: Chart Not Displaying
**Solution**:
1. Check browser console for Chart.js errors
2. Verify Chart.js CDN is accessible
3. Ensure canvas element has proper height

### Issue: Predictions Seem Incorrect
**Solution**:
1. Verify model is trained: `python train_model.py`
2. Check feature encoding matches training
3. Review lag feature calculations in Flask API

---

## 🚢 Production Deployment

### Optimization Checklist
- [ ] Minify CSS and JavaScript
- [ ] Host Chart.js locally instead of CDN
- [ ] Add service worker for offline support
- [ ] Implement proper error logging
- [ ] Add analytics tracking
- [ ] Set up HTTPS for API calls
- [ ] Compress images (if added)
- [ ] Enable gzip compression

### Security Considerations
- Update CORS settings in Flask for production domains
- Implement rate limiting on API endpoints
- Add input sanitization on both frontend and backend
- Use environment variables for API URLs
- Enable HTTPS for all traffic

---

## 📝 Browser Support

- ✅ Chrome 90+ (Recommended)
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**Note**: Uses modern CSS Grid, Flexbox, and ES6+ JavaScript. IE11 not supported.

---

## 🎯 Future Enhancements

Potential features for future versions:
- [ ] Multi-language support (Amharic, Tigrinya)
- [ ] Export predictions to PDF/Excel
- [ ] Historical data comparison view
- [ ] Weather integration for better predictions
- [ ] User authentication and saved predictions
- [ ] Mobile native app (React Native/Flutter)
- [ ] Real-time price alerts via WebSocket
- [ ] Batch prediction upload (CSV)

---

## 📄 License

This frontend is part of the EthioPrice project. Refer to the main project README for licensing information.

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Test thoroughly with the Flask API
2. Follow the existing design system
3. Maintain accessibility standards
4. Document any new features

---

## 📞 Support

For issues or questions:
1. Check this README first
2. Review browser console for errors
3. Test API endpoints directly (Postman/cURL)
4. Verify Flask backend logs

---

**Built with ❤️ for Ethiopian agricultural market intelligence**
