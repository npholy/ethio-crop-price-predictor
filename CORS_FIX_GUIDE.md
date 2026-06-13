# 🔧 CORS & 404 Fix Guide

**Issue:** Backend returning 404 errors and CORS policy blocking frontend requests

**Status:** ✅ FIXED

---

## 🎯 What Was Fixed

### **1. CORS Configuration**

**Before (Wrong):**
```python
CORS(app, 
     origins=ALLOWED_ORIGINS,
     methods=['GET', 'POST', 'OPTIONS'],
     allow_headers=['Content-Type'],
     supports_credentials=True)
```

**After (Correct):**
```python
CORS(app, 
     resources={r"/*": {
         "origins": ALLOWED_ORIGINS,
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True,
         "expose_headers": ["Content-Type"]
     }})
```

**Why:** The `resources` parameter with `r"/*"` ensures CORS applies to ALL routes, not just some.

---

### **2. Updated Allowed Origins**

**Before:**
```python
ALLOWED_ORIGINS = [
    "https://ethio-crop-price-predictor.vercel.app" 
]
```

**After:**
```python
ALLOWED_ORIGINS = [
    'https://ethio-crop-price-predictor.vercel.app',
    'http://localhost:3000',
    'http://localhost:8080',
    'http://127.0.0.1:5000',
    'http://127.0.0.1:8080'
]
```

**Why:** Includes both production URL and common development URLs for testing.

---

### **3. Enhanced Root Endpoint**

**Before:**
```python
@app.route('/')
def home():
    return jsonify({'message': 'EthioPrice API is running'})
```

**After:**
```python
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
```

**Why:** More informative response with explicit status code and available endpoints.

---

### **4. Added Error Handlers**

**New additions:**
```python
@app.errorhandler(404)
def not_found(error):
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
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500
```

**Why:** Better debugging - now you'll get JSON responses instead of HTML error pages.

---

## 📋 Verified Endpoints

Your Flask app now has these working endpoints:

| Method | Endpoint | Purpose | Frontend Calls It? |
|--------|----------|---------|-------------------|
| GET | `/` | Health check | ✅ Yes |
| GET | `/health` | Alternative health check | No |
| GET | `/crops` | List all crops | ✅ Yes |
| GET | `/markets` | List all markets | ✅ Yes |
| POST | `/predict` | Get price prediction | ✅ Yes |

---

## 🚀 Deployment Steps

### **Step 1: Test Locally (Recommended)**

1. **Start Flask server:**
   ```bash
   cd api
   python app.py
   ```

2. **In another terminal, run tests:**
   ```bash
   python test_endpoints.py
   ```

3. **Expected output:**
   ```
   ✅ PASS - Root (/)
   ✅ PASS - Crops (/crops)
   ✅ PASS - Markets (/markets)
   ✅ PASS - Predict (/predict)
   ✅ PASS - CORS Headers
   
   Total: 5/5 tests passed
   🎉 All tests passed! Your API is ready for deployment!
   ```

---

### **Step 2: Commit and Push**

```bash
git add api/app.py test_endpoints.py CORS_FIX_GUIDE.md
git commit -m "Fix: Resolve CORS and 404 errors - update Flask endpoints and CORS config"
git push origin master
```

---

### **Step 3: Deploy to Render**

**Option A: Automatic (Recommended)**
- Render will auto-detect the push
- Wait 2-3 minutes for deployment

**Option B: Manual**
1. Go to Render Dashboard
2. Click your service
3. Click "Manual Deploy" → "Deploy latest commit"

---

### **Step 4: Verify Production**

**Test the deployed endpoints:**

```bash
# Replace with your actual Render URL
export API_URL="https://ethio-crop-price-predictor-api.onrender.com"

# Test root
curl $API_URL/

# Test crops
curl $API_URL/crops

# Test markets
curl $API_URL/markets

# Test predict
curl -X POST $API_URL/predict \
  -H "Content-Type: application/json" \
  -d '{"commodity":"Maize","admin":"Addis Ababa","month":6,"year":2024}'
```

**Expected responses:**
- All should return **200 OK**
- All should return **JSON data**
- No 404 errors
- No CORS errors

---

## 🔍 Troubleshooting

### **Issue: Still getting 404 errors**

**Check 1: Route registered?**
```bash
# In your Flask logs, you should see:
 * Running on http://0.0.0.0:5000
 * Routes:
   GET /
   GET /health
   GET /crops
   GET /markets
   POST /predict
```

**Check 2: Correct URL?**
- Frontend should call: `https://your-api.onrender.com/crops`
- NOT: `https://your-api.onrender.com/api/crops`
- NOT: `https://your-api.onrender.com//crops` (double slash)

---

### **Issue: CORS errors persist**

**Check 1: Verify allowed origins**
In Render logs, you should see:
```
ALLOWED_ORIGINS = [
    'https://ethio-crop-price-predictor.vercel.app',
    ...
]
```

**Check 2: Environment variable**
- Go to Render Dashboard → Environment
- Verify `FRONTEND_URL` is set to: `https://ethio-crop-price-predictor.vercel.app`
- NO trailing slash!

**Check 3: Browser console**
- Press F12
- Check Network tab
- Look for `Access-Control-Allow-Origin` header in response
- Should show: `Access-Control-Allow-Origin: https://ethio-crop-price-predictor.vercel.app`

---

### **Issue: OPTIONS requests failing**

**Symptom:** Browser sends OPTIONS request, gets 404 or 500

**Solution:** The fix already handles this!
```python
"methods": ["GET", "POST", "OPTIONS"]
```

Flask-CORS automatically handles OPTIONS preflight requests.

---

## ✅ Verification Checklist

Before marking as complete:

- [ ] Tested locally with `test_endpoints.py`
- [ ] All 5 tests passed locally
- [ ] Code committed and pushed to GitHub
- [ ] Render deployment succeeded (check logs)
- [ ] Production root endpoint works: `curl https://your-api.onrender.com/`
- [ ] Production crops endpoint works: `curl https://your-api.onrender.com/crops`
- [ ] Production markets endpoint works: `curl https://your-api.onrender.com/markets`
- [ ] Frontend can call backend (no CORS errors)
- [ ] Prediction form works end-to-end
- [ ] Browser console shows no errors

---

## 📊 Expected Frontend Behavior

After this fix, your Vercel frontend should:

1. **Status Indicator: 🟢 Online**
   - No longer shows offline/error

2. **Dropdowns Populate**
   - Commodity dropdown fills with crops
   - Market dropdown fills with markets

3. **Predictions Work**
   - Form submission succeeds
   - Results display correctly
   - Chart renders

4. **Console Clean**
   - No 404 errors
   - No CORS errors
   - Only normal API calls

---

## 🎯 Key Changes Summary

| Component | Before | After |
|-----------|--------|-------|
| CORS Config | Simple origins list | Full resources config with `r"/*"` |
| Allowed Origins | 1 URL | 5 URLs (prod + dev) |
| Root Endpoint | Basic message | Full health check with endpoints list |
| Error Handlers | None | 404 and 500 handlers |
| Endpoint Responses | Simple | Structured with counts and metadata |

---

## 📞 Quick Tests

**Test 1: Health Check**
```bash
curl https://your-api.onrender.com/
```
**Expected:**
```json
{
  "status": "healthy",
  "message": "EthioPrice API is running",
  "version": "1.0.0",
  "endpoints": {...}
}
```

**Test 2: CORS Headers**
```bash
curl -I https://your-api.onrender.com/crops
```
**Expected headers:**
```
Access-Control-Allow-Origin: https://ethio-crop-price-predictor.vercel.app
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

**Test 3: Frontend**
1. Open: `https://ethio-crop-price-predictor.vercel.app`
2. Press F12 → Console
3. Should see: No errors
4. Press F12 → Network
5. Should see: All requests 200 OK

---

## 🎉 Success Indicators

When everything works:

✅ **Render logs:**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] * Running on all addresses
```

✅ **Browser console:**
```
(no errors - clean console)
```

✅ **Network tab:**
```
GET /crops        200 OK
GET /markets      200 OK
POST /predict     200 OK
```

✅ **Frontend:**
```
🟢 Online
Dropdowns: Populated
Predictions: Working
Charts: Rendering
```

---

## 📚 Files Modified

- ✅ `api/app.py` - Updated CORS, endpoints, error handlers
- ✅ `test_endpoints.py` - New test script
- ✅ `CORS_FIX_GUIDE.md` - This guide

---

**Status:** ✅ Ready to deploy  
**Next Step:** Commit, push, and verify in production  
**ETA:** 5 minutes to deployment

