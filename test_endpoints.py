"""
Test script to verify all Flask endpoints are working
Run this after starting your Flask server locally
"""
import requests
import json

# Base URL - change this if testing production
BASE_URL = "http://127.0.0.1:5000"
# For production testing, use:
# BASE_URL = "https://ethio-crop-price-predictor-api.onrender.com"

def test_root():
    """Test GET / endpoint"""
    print("\n" + "="*60)
    print("Testing GET / (root/health check)")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_crops():
    """Test GET /crops endpoint"""
    print("\n" + "="*60)
    print("Testing GET /crops")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/crops")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Number of crops: {data.get('count', 'N/A')}")
        print(f"First 5 crops: {data.get('crops', [])[:5]}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_markets():
    """Test GET /markets endpoint"""
    print("\n" + "="*60)
    print("Testing GET /markets")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/markets")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Number of markets: {data.get('count', 'N/A')}")
        print(f"First 5 markets: {data.get('markets', [])[:5]}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_predict():
    """Test POST /predict endpoint"""
    print("\n" + "="*60)
    print("Testing POST /predict")
    print("="*60)
    try:
        payload = {
            "commodity": "Maize",
            "admin": "Addis Ababa",
            "month": 6,
            "year": 2024
        }
        print(f"Request payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/predict",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_cors_headers():
    """Test CORS headers are present"""
    print("\n" + "="*60)
    print("Testing CORS Headers")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/crops")
        print("Response Headers:")
        cors_headers = {k: v for k, v in response.headers.items() if 'Access-Control' in k}
        for header, value in cors_headers.items():
            print(f"  {header}: {value}")
        return len(cors_headers) > 0
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 ETHIOPRICE API ENDPOINT TESTS")
    print("="*60)
    print(f"Testing Base URL: {BASE_URL}")
    print("Make sure your Flask server is running!")
    print("Run: python api/app.py")
    
    results = {}
    
    results['Root (/)'] = test_root()
    results['Crops (/crops)'] = test_crops()
    results['Markets (/markets)'] = test_markets()
    results['Predict (/predict)'] = test_predict()
    results['CORS Headers'] = test_cors_headers()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your API is ready for deployment!")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
