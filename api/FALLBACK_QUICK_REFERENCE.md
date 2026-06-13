# Three-Tier Fallback - Quick Reference Card

## 🎯 Core Principle

**NEVER return 400 for missing data. ALWAYS provide an estimate with transparency.**

---

## 📊 Three Tiers At-A-Glance

```
┌─────────────────────────────────────────────────────────────┐
│                    TIER 1: OPTIMAL                          │
│  Data: 3+ historical points                                 │
│  Method: Full lag calculation                               │
│  Status: 200 OK                                             │
│  data_quality: "good"                                       │
│  warning: null                                              │
│  Confidence: 80-95%                                         │
│  Frontend: Green/No warning                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    TIER 2: LIMITED                          │
│  Data: 1-2 historical points                                │
│  Method: Use recent price as proxy for missing lags        │
│  Status: 200 OK                                             │
│  data_quality: "limited"                                    │
│  warning: "Limited data: Only X points found..."           │
│  Confidence: 60-75%                                         │
│  Frontend: Amber warning                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    TIER 3: FALLBACK                         │
│  Data: 0 points for combo                                   │
│  Method: Global average for commodity across all markets   │
│  Status: 200 OK (NOT 400!)                                  │
│  data_quality: "low"                                        │
│  warning: "Using global average as fallback..."            │
│  Confidence: 55-70%                                         │
│  Frontend: Amber warning with fallback notice              │
└─────────────────────────────────────────────────────────────┘
```

---

## ❌ When 400 IS Returned

```
┌─────────────────────────────────────────────────────────────┐
│                    INVALID INPUTS ONLY                      │
│  • Unknown commodity (not in /crops)                        │
│  • Unknown market (not in /markets)                         │
│  • Month < 1 or > 12                                        │
│  • Year < 2000 or > 2050                                    │
│  • Missing required fields                                  │
│  • Invalid data types (month/year not integers)            │
│                                                             │
│  Status: 400 Bad Request                                    │
│  Frontend: Red error alert                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Response Structure

### **Success (200 OK) - ALL Tiers**
```json
{
  "predicted_price": 1250.75,        // float, always present
  "commodity": "Maize",              // string, always present
  "market": "Addis Ababa",           // string, always present
  "month": 6,                        // int, always present
  "year": 2024,                      // int, always present
  "season": "kiremt",                // string, always present
  "currency": "ETB",                 // string, always present
  "unit": "100kg",                   // string, always present
  "data_quality": "good|limited|low", // string, always present
  "warning": "Optional message"      // string or null
}
```

### **Error (400 Bad Request) - Invalid Input**
```json
{
  "error": "Descriptive error message"
}
```

---

## 🧪 Quick Test Commands

### **Tier 1 Test (Expected: good quality)**
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"commodity":"Maize","admin":"Addis Ababa","month":6,"year":2024}'
```

### **Tier 3 Test (Expected: low quality with global avg)**
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"commodity":"Sorghum","admin":"Afar","month":1,"year":2024}'
```

### **Invalid Input Test (Expected: 400 error)**
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"commodity":"InvalidCrop","admin":"Addis Ababa","month":6,"year":2024}'
```

---

## 🎨 Frontend Display

| data_quality | Confidence | Alert | Message |
|--------------|------------|-------|---------|
| `"good"` | 80-95% | None | - |
| `"limited"` | 60-75% | Amber ℹ️ | Shows warning |
| `"low"` | 55-70% | Amber ℹ️ | Shows fallback notice |

---

## 🔑 Key Function

```python
def get_lag_features_with_fallback(commodity, admin, month, year):
    """
    Returns lag features for ALL cases (never returns None/error)
    
    Returns dict with:
    - price_lag1, price_lag2, price_lag3, rolling_mean_3
    - data_quality: 'good' | 'limited' | 'low'
    - warning: string or None
    """
```

---

## ✅ Success Criteria

- [ ] 3+ points → Returns `data_quality: "good"`
- [ ] 1-2 points → Returns `data_quality: "limited"` + warning
- [ ] 0 points → Returns `data_quality: "low"` + global avg warning
- [ ] Invalid input → Returns 400 error
- [ ] Frontend shows amber for limited/low
- [ ] Frontend shows red ONLY for 400 errors
- [ ] Confidence adjusts based on data_quality

---

## 📞 Quick Debugging

**If you see 400 errors:**
1. Check if commodity is in `/crops` response
2. Check if market is in `/markets` response
3. Verify month is 1-12
4. Verify all required fields present

**If predictions seem wrong:**
1. Check `data_quality` field in response
2. If `"low"`, it's using global average (expected for sparse data)
3. If `"limited"`, it's using 1-2 historical points only

---

**Print this card and keep it handy during development!** 📋
