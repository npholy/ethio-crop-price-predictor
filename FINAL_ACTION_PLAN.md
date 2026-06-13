# 🎯 Final Action Plan - Resolve Render 404 Issue

**Date:** June 13, 2026  
**Status:** Ready to Deploy  
**Issue:** Service shows "Live" but returns 404

---

## ✅ SUMMARY OF FIXES APPLIED

### **1. Path Configuration Fixed**

**Changed in `api/app.py`:**

```python
# OLD (WRONG - looking in parent directory):
PROJECT_ROOT = os.path.dirname(BASE_DIR)
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'wfp_food_prices_eth.csv')

# NEW (CORRECT - looking in api/ directory):
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'wfp_food_prices_eth.csv')
```

**This assumes your structure is:**
```
api/
├── app.py
├── models/          ← models moved here
└── data/            ← data moved here
    └── raw/
        └── wfp_food_prices_eth.csv
```

---

## 📋 PRE-DEPLOYMENT VERIFICATION

### **Step 1: Verify File Structure**

Run the verification script:

```bash
verify_structure.bat
```

**Expected output:**
```
[CHECKING] api/app.py
  ✅ Found
[CHECKING] api/requirements.txt
  ✅ Found
[CHECKING] api/Procfile
  ✅ Found
[CHECKING] api/runtime.txt
  ✅ Found
[CHECKING] api/models/ folder
  ✅ Folder exists
    ✅ crop_price_model.pkl
    ✅ le_commodity.pkl
    ✅ le_admin.pkl
    ✅ le_season.pkl
[CHECKING] api/data/ folder
  ✅ Folder exists
    ✅ wfp_food_prices_eth.csv
```

---

### **Step 2: If Data Folder is Missing**

**You mentioned you moved it, but I don't see it. If needed:**

```bash
# Option 1: Copy (keeps original)
xcopy data api\data\ /E /I /Y

# Option 2: Move (removes original)
move data api\data

# Verify
dir api\data\raw
```

**Should show:**
```
api\data\raw\wfp_food_prices_eth.csv
```

---

### **Step 3: Verify Files Are in Git**

```bash
git status
```

**Should show:**
```
modified:   api/app.py
```

**Check models and data are tracked:**
```bash
git ls-files api/models/
git ls-files api/data/
```

**If models show up but data doesn't:**
```bash
git add api/data/
git status
```

**Should now show:**
```
new file:   api/data/raw/wfp_food_prices_eth.csv
```

---

## 🚀 DEPLOYMENT SEQUENCE

### **Step 1: Commit Path Fix**

```bash
git add api/app.py
git commit -m "Fix: Update paths to use BASE_DIR - models and data in api/ directory"
```

### **Step 2: Add Data Folder (If Not Already Committed)**

```bash
git add api/data/
git commit -m "Add: Move data folder into api/ directory"
```

### **Step 3: Push to GitHub**

```bash
git push origin master
```

**Expected:**
```
Counting objects: X, done.
Writing objects: 100% (X/X), done.
To https://github.com/npholy/ethio-crop-price-predictor.git
   7d4e468..XXXXXXX  master -> master
```

---

## 🔍 RENDER SETTINGS VERIFICATION

### **Go to Render Dashboard → Your Service → Settings**

**Verify these EXACT values:**

```
┌─────────────────────────────────────────┐
│ Build & Development Settings            │
├─────────────────────────────────────────┤
│                                         │
│ Root Directory:                         │
│ ┌─────────────────────────────────────┐ │
│ │ api                                 │ │ ← Exactly "api"
│ └─────────────────────────────────────┘ │
│                                         │
│ Build Command:                          │
│ ┌─────────────────────────────────────┐ │
│ │ pip install -r requirements.txt     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Start Command:                          │
│ ┌─────────────────────────────────────┐ │
│ │ gunicorn app:app                    │ │ ← NO --bind flag
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

**If Start Command shows:**
```
gunicorn app:app --bind 0.0.0.0:$PORT  ← WRONG
```

**Change to:**
```
gunicorn app:app  ← CORRECT
```

**Why:** Render sets `$PORT` automatically, and Gunicorn binds to it by default.

---

## 📊 MONITORING DEPLOYMENT

### **Step 1: Watch Render Logs**

**Go to:** Render Dashboard → Your Service → **Logs** tab

**Look for this sequence:**

```
==> Building
-----> Python app detected
-----> Installing dependencies
       Successfully installed flask-3.0.0 flask-cors-4.0.0 gunicorn-21.2.0 ...
-----> Build completed

==> Starting service
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000 (12345)  ← CRITICAL: Must see this
[INFO] Using worker: sync
[INFO] Booting worker with pid: 12346               ← CRITICAL: Must see this
```

---

### **Step 2: Interpret Logs**

#### **✅ SUCCESS: Logs show this:**

```
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Booting worker with pid: 12346
(no errors after this)
```

**Action:** Proceed to testing!

---

#### **❌ FAILURE 1: FileNotFoundError**

```
FileNotFoundError: [Errno 2] No such file or directory: 
'/opt/render/project/src/api/models/crop_price_model.pkl'
```

**Cause:** Models not in git or wrong path

**Solution:**
```bash
git ls-files api/models/
# If empty:
git add api/models/*.pkl
git commit -m "Add model files"
git push origin master
```

---

#### **❌ FAILURE 2: FileNotFoundError (Data)**

```
FileNotFoundError: [Errno 2] No such file or directory:
'/opt/render/project/src/api/data/raw/wfp_food_prices_eth.csv'
```

**Cause:** Data not moved to api/ folder

**Solution:**
```bash
# Move data into api
move data api\data
git add api\data/
git commit -m "Move data folder into api directory"
git push origin master
```

---

#### **❌ FAILURE 3: No "Listening at" Message**

**Logs show:**
```
==> Starting service
(nothing else)
```

**Cause:** Start command wrong or Gunicorn not installed

**Solution:**
1. Check Start Command: Should be `gunicorn app:app`
2. Check requirements.txt has: `gunicorn==21.2.0`
3. Manual Deploy → Clear cache & deploy

---

#### **❌ FAILURE 4: Import Error**

```
ModuleNotFoundError: No module named 'flask_cors'
```

**Cause:** Missing dependency

**Solution:**
```bash
# Check api/requirements.txt has all these:
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
numpy==1.26.2
pandas==2.1.4
scikit-learn==1.3.2
```

---

## ✅ TESTING AFTER DEPLOYMENT

### **Wait 30 seconds after "Live" status**

Then run these tests:

---

### **Test 1: Root Endpoint**

```bash
curl https://ethio-crop-price-predictor-api.onrender.com/
```

**Expected Response (200 OK):**
```json
{
  "status": "healthy",
  "message": "EthioPrice API is running",
  "version": "1.0.0",
  "endpoints": {
    "health": "/",
    "crops": "/crops",
    "markets": "/markets",
    "predict": "/predict (POST)"
  }
}
```

**If you get 404:**
```html
<html>
  <head><title>404 Not Found</title></head>
  ...
</html>
```

**Action:**
1. Go back to Render Logs
2. Look for Python errors
3. Check if "Listening at" message appeared
4. See RENDER_DIAGNOSTIC_GUIDE.md for full troubleshooting

---

### **Test 2: Crops Endpoint**

```bash
curl https://ethio-crop-price-predictor-api.onrender.com/crops
```

**Expected Response (200 OK):**
```json
{
  "crops": ["Maize", "Wheat", "Sorghum", ...],
  "count": XX
}
```

---

### **Test 3: Markets Endpoint**

```bash
curl https://ethio-crop-price-predictor-api.onrender.com/markets
```

**Expected Response (200 OK):**
```json
{
  "markets": ["Addis Ababa", "Dire Dawa", ...],
  "count": XX
}
```

---

### **Test 4: Predict Endpoint**

```bash
curl -X POST https://ethio-crop-price-predictor-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"commodity":"Maize","admin":"Addis Ababa","month":6,"year":2024}'
```

**Expected Response (200 OK):**
```json
{
  "predicted_price": 1234.56,
  "commodity": "Maize",
  "market": "Addis Ababa",
  "month": 6,
  "year": 2024,
  "season": "kiremt",
  "currency": "ETB",
  "unit": "100kg",
  "data_quality": "good"
}
```

---

## 🎯 RENDER SETTINGS - 100% CORRECT CONFIGURATION

### **For Your Structure:**

```
ethio-crop-price-predictor/
└── api/                    ← This is your "root"
    ├── app.py
    ├── requirements.txt
    ├── Procfile
    ├── runtime.txt
    ├── models/
    │   └── *.pkl
    └── data/
        └── raw/
            └── *.csv
```

### **Render Settings:**

| Setting | Value | Why |
|---------|-------|-----|
| **Root Directory** | `api` | Makes Render treat `api/` as the project root |
| **Build Command** | `pip install -r requirements.txt` | Installs Python dependencies |
| **Start Command** | `gunicorn app:app` | Starts Flask with Gunicorn WSGI server |
| **Python Version** | Auto-detected from `runtime.txt` | Uses Python 3.11.7 |

### **Environment Variables:**

| Variable | Value | Required |
|----------|-------|----------|
| `FRONTEND_URL` | `https://ethio-crop-price-predictor.vercel.app` | Yes (for CORS) |
| `FLASK_ENV` | `production` | Optional |
| `PORT` | *(auto-set by Render)* | Don't set this |

---

## 🔧 IF "LIVE BUT 404" PERSISTS

### **Diagnostic Checklist:**

1. **Check Render Logs for "Listening at"**
   - [ ] YES → Flask started, routes might not be registered
   - [ ] NO → Gunicorn didn't start, check Start Command

2. **If "Listening at" appears, check for Python errors BEFORE it**
   - [ ] FileNotFoundError → Files not in git or wrong paths
   - [ ] ModuleNotFoundError → Missing dependency in requirements.txt
   - [ ] No errors → Routes might not be registered (rare)

3. **Test with verbose curl**
   ```bash
   curl -v https://your-app.onrender.com/
   ```
   - Look at HTTP status code in response
   - Look at Content-Type header
   - If HTML response: Flask routes not working
   - If JSON response: Everything working!

4. **Check Render Settings**
   - [ ] Root Directory = `api` (not empty, not `/api`)
   - [ ] Start Command = `gunicorn app:app` (no extra flags)

5. **Force Clean Deploy**
   - Render Dashboard → Manual Deploy → Clear cache & deploy
   - This forces a fresh build

6. **Read Full Diagnostic Guide**
   - See RENDER_DIAGNOSTIC_GUIDE.md
   - Covers all "Live but 404" scenarios
   - Step-by-step troubleshooting

---

## 📞 QUICK REFERENCE

### **Structure Verification:**
```bash
verify_structure.bat
```

### **Commit and Deploy:**
```bash
git add api/app.py
git commit -m "Fix: Update paths for api/ directory structure"
git push origin master
```

### **Test Deployed API:**
```bash
curl https://ethio-crop-price-predictor-api.onrender.com/
```

### **View Render Logs:**
```
Render Dashboard → Your Service → Logs
```

---

## ✅ SUCCESS CRITERIA

After deployment, you should have:

### **Render Dashboard:**
- ✅ Status: Live (green dot)
- ✅ Latest deployment succeeded
- ✅ Logs show: "Listening at: http://0.0.0.0:XXXXX"
- ✅ Logs show: "Booting worker with pid: XXXXX"
- ✅ No Python errors in logs

### **API Endpoints:**
- ✅ `curl /` returns 200 OK with JSON
- ✅ `curl /crops` returns 200 OK with crops array
- ✅ `curl /markets` returns 200 OK with markets array
- ✅ `curl -X POST /predict` returns 200 OK with prediction

### **Frontend:**
- ✅ https://ethio-crop-price-predictor.vercel.app loads
- ✅ Browser console clean (no errors)
- ✅ Status: 🟢 Online
- ✅ Dropdowns populate
- ✅ Predictions work

---

## 🎊 FINAL NOTES

### **Key Points:**

1. **Root Directory = `api`** is critical
   - This makes Render use `api/` as the base
   - All paths in Flask become relative to `api/`

2. **Start Command = `gunicorn app:app`** is correct
   - No `--bind` flag needed
   - Render handles port automatically

3. **Files must be in git**
   - Models: `api/models/*.pkl`
   - Data: `api/data/raw/*.csv`
   - Use `git ls-files` to verify

4. **Logs are your friend**
   - "Listening at" = Gunicorn started
   - "Booting worker" = Worker started
   - Python errors = Something failed during import

### **If Everything Fails:**

1. **Read RENDER_DIAGNOSTIC_GUIDE.md** - Comprehensive troubleshooting
2. **Check Render Status Page** - Service outages
3. **Try Free Alternative** - Test on Railway.app or Fly.io

---

**You're ready! Run verification, commit, push, and monitor the logs!** 🚀

