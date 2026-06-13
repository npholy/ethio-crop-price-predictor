# 🔍 Render Deployment Diagnostic Guide

**Issue:** Service shows "Live" but returns 404 errors  
**Current Structure:** All files (app.py, models/, data/) inside `api/` directory

---

## ✅ PART 1: Verify Your Structure is Correct

### **Expected Directory Structure:**

```
ethio-crop-price-predictor/
├── api/                           ← Root Directory in Render
│   ├── app.py                     ← Main Flask application
│   ├── requirements.txt           ← Python dependencies
│   ├── Procfile                   ← Gunicorn start command
│   ├── runtime.txt                ← Python version
│   ├── models/                    ← Model files (MOVED HERE)
│   │   ├── crop_price_model.pkl
│   │   ├── le_commodity.pkl
│   │   ├── le_admin.pkl
│   │   └── le_season.pkl
│   └── data/                      ← Data files (MOVED HERE)
│       └── raw/
│           └── wfp_food_prices_eth.csv
└── web/                           ← Vercel frontend (not on Render)
```

### **✅ Your Render Settings Should Be:**

| Setting | Correct Value | Why |
|---------|--------------|-----|
| **Root Directory** | `api` | Tells Render to use `api/` as the base |
| **Build Command** | `pip install -r requirements.txt` | Installs dependencies |
| **Start Command** | `gunicorn app:app` | Starts Flask with Gunicorn |
| **Environment** | `PORT` (auto-set by Render) | Gunicorn binds to this |

### **❌ Common Mistakes:**

| Wrong | Correct |
|-------|---------|
| Root Directory: *(empty)* | Root Directory: `api` |
| Root Directory: `/api` | Root Directory: `api` |
| Root Directory: `./api` | Root Directory: `api` |
| Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT` | Start Command: `gunicorn app:app` |
| Start Command: `python app.py` | Start Command: `gunicorn app:app` |

---

## 🔍 PART 2: Understanding "Live but 404" Issue

### **What "Live" Means:**

When Render shows "Live", it means:
1. ✅ Build completed successfully
2. ✅ Start command executed
3. ✅ Process is running
4. ✅ Render's proxy is active

### **Why You Still Get 404:**

```
┌─────────────────────────────────────────────────────────────┐
│                     REQUEST FLOW                             │
└─────────────────────────────────────────────────────────────┘

Browser Request:
   https://your-app.onrender.com/crops
              ↓
Render's Reverse Proxy (NGINX):
   - Receives request
   - Checks if Gunicorn is listening
              ↓
Gunicorn (WSGI Server):
   - Should be listening on 0.0.0.0:$PORT
   - Forwards to Flask app
              ↓
Flask Application:
   - Should have route defined
   - Returns response
```

**404 happens when:**
1. ❌ Gunicorn not binding to correct port
2. ❌ Flask app crashed during startup (but Gunicorn still runs)
3. ❌ Routes not registered properly
4. ❌ Render proxy can't reach Gunicorn

---

## 📊 PART 3: Render Log Analysis

### **What to Look For in Logs:**

#### **✅ GOOD LOGS (App Starting Successfully):**

```
=== Building Application ===
-----> Installing dependencies
       Successfully installed flask-3.0.0 flask-cors-4.0.0 ...
-----> Build completed

=== Starting Service ===
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000 (12345)  ← KEY: Port number
[INFO] Using worker: sync
[INFO] Booting worker with pid: 12346
```

**Key Success Indicators:**
- ✅ "Listening at: http://0.0.0.0:XXXXX" - Shows Gunicorn started
- ✅ "Booting worker with pid: XXXXX" - Shows worker started
- ✅ No Python errors or tracebacks

---

#### **❌ BAD LOGS (Startup Failures):**

**Issue 1: Missing Files**
```
FileNotFoundError: [Errno 2] No such file or directory: '/opt/render/project/src/models/crop_price_model.pkl'
```

**Solution:**
- Models are not in the right location
- Should be in `api/models/` not root `models/`

---

**Issue 2: Import Errors**
```
ModuleNotFoundError: No module named 'flask_cors'
```

**Solution:**
- Missing dependency in `requirements.txt`
- Add the missing package

---

**Issue 3: Port Binding Issues**
```
[ERROR] Connection in use: ('0.0.0.0', 5000)
```

**Solution:**
- Don't hardcode port 5000
- Use `gunicorn app:app` (Render sets $PORT automatically)

---

**Issue 4: Silent Crash (No Errors but Routes Don't Work)**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Booting worker with pid: 12346
(nothing else - no routes registered)
```

**Solution:**
- Flask app crashed during import/initialization
- Check for errors when loading models or data files

---

## 🛠️ PART 4: Step-by-Step Diagnostic Process

### **Step 1: Verify Render Settings**

1. **Go to Render Dashboard** → Your Service → Settings
2. **Check these exact values:**

```
┌────────────────────────────────────────┐
│ Build & Deploy                         │
├────────────────────────────────────────┤
│ Root Directory:                        │
│ ┌────────────────────────────────────┐ │
│ │ api                                │ │ ← MUST BE "api"
│ └────────────────────────────────────┘ │
│                                        │
│ Build Command:                         │
│ ┌────────────────────────────────────┐ │
│ │ pip install -r requirements.txt    │ │
│ └────────────────────────────────────┘ │
│                                        │
│ Start Command:                         │
│ ┌────────────────────────────────────┐ │
│ │ gunicorn app:app                   │ │ ← NO --bind flag needed
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘
```

**If any are wrong:**
- Click "Edit"
- Update the value
- Click "Save"
- Service will auto-redeploy

---

### **Step 2: Check Logs During Startup**

1. **Go to Render Dashboard** → Your Service → **Logs** tab
2. **Look for startup sequence:**

```
Expected successful startup:
┌─────────────────────────────────────────┐
│ ==> Starting service...                 │
│ [INFO] Starting gunicorn 21.2.0         │
│ [INFO] Listening at: http://0.0.0.0:... │ ← MUST SEE THIS
│ [INFO] Booting worker with pid: ...     │ ← MUST SEE THIS
│ (no errors after this)                  │
└─────────────────────────────────────────┘
```

**If you DON'T see "Listening at:":**
- Gunicorn didn't start
- Check Start Command is exactly: `gunicorn app:app`

**If you see Python errors:**
- Copy the full error
- It tells you exactly what's wrong (missing file, import error, etc.)

---

### **Step 3: Test Routes After Startup**

**Wait 30 seconds after "Live" status, then:**

```bash
# Test root endpoint
curl -v https://your-app.onrender.com/

# -v flag shows full HTTP response including headers
```

**Expected Response:**
```
< HTTP/2 200 
< content-type: application/json
< access-control-allow-origin: https://ethio-crop-price-predictor.vercel.app
<
{
  "status": "healthy",
  "message": "EthioPrice API is running",
  "version": "1.0.0",
  "endpoints": {...}
}
```

**If you get 404:**
```
< HTTP/2 404
< content-type: text/html
<
<html>
  <head><title>404 Not Found</title></head>
  ...
</html>
```

**This means:**
- Render proxy is working (you got a response)
- But Flask routes are NOT registered
- App likely crashed during startup

---

### **Step 4: Add Debug Logging**

If logs show "Listening" but routes don't work, add this to `app.py`:

```python
# Add this RIGHT BEFORE your routes
print("=" * 60)
print("FLASK APP STARTING")
print(f"BASE_DIR: {BASE_DIR}")
print(f"MODELS_DIR: {MODELS_DIR}")
print(f"DATA_PATH: {DATA_PATH}")
print("=" * 60)

# Try to load models with error handling
try:
    model = pickle.load(open(os.path.join(MODELS_DIR, 'crop_price_model.pkl'), 'rb'))
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ ERROR loading model: {e}")
    raise

# After route definitions, add:
print("=" * 60)
print("REGISTERED ROUTES:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.methods} {rule.rule}")
print("=" * 60)
```

This will show in Render logs:
- Where Flask is looking for files
- If models loaded successfully
- Which routes are registered

---

## 🎯 PART 5: Action Plan for "Logs Say Success, But 404 Persists"

### **Scenario: Logs show this:**

```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Booting worker with pid: 12346
```

**But browser shows 404**

### **Action Plan:**

#### **Action 1: Verify Service URL**

**Check you're using the correct URL:**
- ✅ Correct: `https://ethio-crop-price-predictor-api.onrender.com/crops`
- ❌ Wrong: `https://ethio-crop-price-predictor-api.onrender.com/api/crops`
- ❌ Wrong: `http://ethio-crop-price-predictor-api.onrender.com/crops` (http not https)

---

#### **Action 2: Check Route Registration**

Add debug logging (see Step 4 above), then check logs for:

```
REGISTERED ROUTES:
  {'GET', 'HEAD', 'OPTIONS'} /
  {'GET', 'HEAD', 'OPTIONS'} /health
  {'GET', 'HEAD', 'OPTIONS'} /crops
  {'GET', 'HEAD', 'OPTIONS'} /markets
  {'POST', 'OPTIONS'} /predict
```

**If you DON'T see routes:**
- Flask app crashed during import
- Look for Python errors BEFORE the Gunicorn startup messages

---

#### **Action 3: Test Gunicorn Locally**

On your local machine:

```bash
cd api
gunicorn app:app
```

**Expected output:**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://127.0.0.1:8000
```

**Then test:**
```bash
curl http://127.0.0.1:8000/
```

**If this works locally but not on Render:**
- File paths might be different
- Check BASE_DIR logging

**If this FAILS locally:**
- Fix it locally first
- Then deploy to Render

---

#### **Action 4: Check File Permissions**

Render logs might show:

```
PermissionError: [Errno 13] Permission denied: '/opt/render/project/src/api/models/crop_price_model.pkl'
```

**Solution:**
- This is rare but can happen
- Make sure files are committed to git (not .gitignored)
- Check `.gitignore` doesn't exclude `*.pkl` files

---

#### **Action 5: Force Clean Redeploy**

Sometimes Render's cache causes issues:

1. **Go to Render Dashboard** → Your Service
2. **Click "Manual Deploy"**
3. **Select "Clear build cache & deploy"**
4. **Wait for deployment**

This forces a completely fresh build.

---

## 📋 PART 6: Pre-Deployment Checklist

### **Before You Deploy, Verify:**

#### **File Structure:**
```bash
# Run this in your project root
ls -la api/
```

**Should show:**
```
api/
├── app.py                    ✅
├── requirements.txt          ✅
├── Procfile                  ✅
├── runtime.txt               ✅
├── models/                   ✅
│   ├── crop_price_model.pkl
│   ├── le_commodity.pkl
│   ├── le_admin.pkl
│   └── le_season.pkl
└── data/                     ✅
    └── raw/
        └── wfp_food_prices_eth.csv
```

---

#### **Files Are Committed:**
```bash
git ls-files api/models/
git ls-files api/data/
```

**Should show:**
```
api/models/crop_price_model.pkl
api/models/le_commodity.pkl
api/models/le_admin.pkl
api/models/le_season.pkl
api/data/raw/wfp_food_prices_eth.csv
```

**If empty:**
```bash
git add api/models/*.pkl
git add api/data/raw/*.csv
git commit -m "Add model and data files to api directory"
git push origin master
```

---

#### **Paths in app.py:**
```python
# Should be EXACTLY:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'wfp_food_prices_eth.csv')
```

**NOT:**
```python
# WRONG - Don't use PROJECT_ROOT anymore
PROJECT_ROOT = os.path.dirname(BASE_DIR)
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
```

---

#### **Render Settings:**
```
Root Directory: api
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

---

## 🚀 PART 7: Deployment & Monitoring Steps

### **Step 1: Deploy with Corrected Paths**

```bash
# Commit the path fix
git add api/app.py
git commit -m "Fix: Update paths to use BASE_DIR (models and data in api/)"
git push origin master
```

---

### **Step 2: Monitor Deployment (Live)**

1. **Open Render Dashboard** → Your Service → **Logs** tab
2. **Watch for:**

```
==> Building...
-----> Installing dependencies
       ✅ Successfully installed ...

==> Starting service
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:XXXXX  ← WAIT FOR THIS
[INFO] Booting worker with pid: XXXXX      ← AND THIS
```

3. **If you added debug logging, look for:**

```
============================================================
FLASK APP STARTING
BASE_DIR: /opt/render/project/src/api
MODELS_DIR: /opt/render/project/src/api/models
DATA_PATH: /opt/render/project/src/api/data/raw/wfp_food_prices_eth.csv
============================================================
✅ Model loaded successfully
============================================================
REGISTERED ROUTES:
  {'GET', 'HEAD', 'OPTIONS'} /
  {'GET', 'HEAD', 'OPTIONS'} /crops
  {'GET', 'HEAD', 'OPTIONS'} /markets
  {'POST', 'OPTIONS'} /predict
============================================================
```

---

### **Step 3: Test Immediately After "Live" Status**

**Wait 30 seconds**, then:

```bash
curl -v https://ethio-crop-price-predictor-api.onrender.com/
```

**Expected:**
```
< HTTP/2 200 
< content-type: application/json
{
  "status": "healthy",
  "message": "EthioPrice API is running",
  ...
}
```

**If you get 404:**
- Go back to logs
- Look for Python errors
- Check route registration output

---

### **Step 4: Test All Endpoints**

```bash
# Root
curl https://ethio-crop-price-predictor-api.onrender.com/

# Crops
curl https://ethio-crop-price-predictor-api.onrender.com/crops

# Markets
curl https://ethio-crop-price-predictor-api.onrender.com/markets

# Predict
curl -X POST https://ethio-crop-price-predictor-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"commodity":"Maize","admin":"Addis Ababa","month":6,"year":2024}'
```

**All should return 200 OK with JSON data!**

---

## 🔧 PART 8: Common Issues & Solutions

### **Issue 1: Gunicorn Worker Timeout**

**Logs show:**
```
[CRITICAL] WORKER TIMEOUT (pid:12346)
[WARNING] Worker with pid 12346 was terminated due to signal 9
```

**Cause:**
- Loading models/data takes too long
- Worker times out before responding

**Solution:**
```bash
# Update Start Command to:
gunicorn app:app --timeout 120
```

---

### **Issue 2: Memory Errors**

**Logs show:**
```
MemoryError: Unable to allocate array
```

**Cause:**
- Free tier has limited RAM
- Models + data too large

**Solution:**
- Upgrade Render plan
- OR optimize model size

---

### **Issue 3: Module Not Found**

**Logs show:**
```
ModuleNotFoundError: No module named 'sklearn'
```

**Cause:**
- Missing or misspelled in requirements.txt

**Solution:**
```
# requirements.txt should have:
scikit-learn==1.3.2
# NOT:
sklearn==1.3.2
```

---

### **Issue 4: File Not Found (Even Though Files Exist)**

**Logs show:**
```
FileNotFoundError: [Errno 2] No such file or directory: '...models/crop_price_model.pkl'
```

**Cause:**
- Files not committed to git
- OR path is wrong

**Solution:**
```bash
# Check files are in git
git ls-files api/models/

# If empty, add them:
git add api/models/*.pkl
git commit -m "Add model files"
git push origin master
```

---

## ✅ PART 9: Success Checklist

After deployment, verify:

### **Render Dashboard:**
- [ ] Status shows "Live" (green dot)
- [ ] Latest deployment succeeded
- [ ] Logs show "Listening at: http://0.0.0.0:XXXXX"
- [ ] Logs show "Booting worker with pid: XXXXX"
- [ ] No Python errors in logs

### **API Testing:**
- [ ] `curl https://your-api.onrender.com/` returns 200 OK
- [ ] `curl https://your-api.onrender.com/crops` returns JSON array
- [ ] `curl https://your-api.onrender.com/markets` returns JSON array
- [ ] POST to `/predict` returns prediction

### **Frontend Integration:**
- [ ] Open https://ethio-crop-price-predictor.vercel.app
- [ ] Press F12 → Console is clean
- [ ] Status shows 🟢 Online
- [ ] Dropdowns populate
- [ ] Predictions work

---

## 📞 Quick Reference

### **Render Settings:**
```
Root Directory:  api
Build Command:   pip install -r requirements.txt
Start Command:   gunicorn app:app
```

### **Test Commands:**
```bash
# Health check
curl https://ethio-crop-price-predictor-api.onrender.com/

# Expected: 200 OK with JSON
```

### **Debug Command:**
```bash
# Verbose output shows full HTTP response
curl -v https://ethio-crop-price-predictor-api.onrender.com/
```

---

**This guide covers all common "Live but 404" scenarios. Follow the diagnostic steps in order!**

