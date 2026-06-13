# Ethiopian Crop Price Predictor

## For the Frontend Developer

### Step 1 — Install Git LFS and Clone
```bash
git lfs install
git clone https://github.com/npholy/ethio-crop-price-predictor.git
cd ethio-crop-price-predictor
```

### Step 2 — Run the Backend
```bash
cd api
pip install -r requirements.txt
python app.py
```
API runs at `http://localhost:5000`

### Step 3 — Start the Frontend
```bash
cd ..
npx create-react-app frontend
cd frontend
npm install axios
npm start
```

### Step 4 — Connect to the API
Use these 3 endpoints:

| Method | Endpoint | Use for |
|--------|----------|---------|
| GET | `/crops` | Populate crop dropdown |
| GET | `/markets` | Populate market dropdown |
| POST | `/predict` | Get predicted price |

POST request body:
```json
{
  "commodity": "Teff",
  "admin": "Oromia",
  "month": 7,
  "year": 2023
}
```

Build a form with: **crop, market, month, year** → submit → show predicted price.