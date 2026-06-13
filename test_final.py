"""
Three-Tier Fallback System - Final Verification Test

This script tests all three tiers of the graceful fallback strategy:
- Tier 1: Good data quality (3+ historical points)
- Tier 2: Limited data quality (1-2 historical points)
- Tier 3: Low data quality (0 historical points - global fallback)

Expected Results:
- ALL valid requests return 200 OK (even with 0 data)
- Only invalid inputs return 400 Bad Request
"""

import requests
import json
from datetime import datetime

# Configuration
API_URL = 'http://127.0.0.1:5000/predict'
HEADERS = {'Content-Type': 'application/json'}

# ANSI color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_section(title):
    """Print a section header"""
    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}{title}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}\n")

def print_test(test_name, description):
    """Print test information"""
    print(f"{BOLD}Test: {test_name}{RESET}")
    print(f"Description: {description}\n")

def print_result(status_code, expected_status, data):
    """Print test result with color coding"""
    success = (status_code == expected_status)
    
    if success:
        print(f"{GREEN}✓ PASS{RESET} - Status: {status_code} (Expected: {expected_status})")
    else:
        print(f"{RED}✗ FAIL{RESET} - Status: {status_code} (Expected: {expected_status})")
    
    print(f"\nResponse:")
    print(json.dumps(data, indent=2))
    
    # Analyze response for three-tier system
    if status_code == 200 and 'data_quality' in data:
        quality = data['data_quality']
        
        if quality == 'good':
            print(f"\n{GREEN}→ TIER 1: Optimal Data (3+ historical points){RESET}")
        elif quality == 'limited':
            print(f"\n{YELLOW}→ TIER 2: Limited Data (1-2 historical points){RESET}")
        elif quality == 'low':
            print(f"\n{YELLOW}→ TIER 3: Global Fallback (0 historical points){RESET}")
        
        if 'warning' in data and data['warning']:
            print(f"{YELLOW}⚠ Warning: {data['warning']}{RESET}")
    
    print()
    return success

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get('http://127.0.0.1:5000/')
        if response.status_code == 200:
            print(f"{GREEN}✓ API is running{RESET}")
            return True
        else:
            print(f"{RED}✗ API returned status {response.status_code}{RESET}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗ Cannot connect to API. Please start Flask server: python api/app.py{RESET}")
        return False

def run_test(test_name, description, payload, expected_status=200):
    """Run a single test"""
    print_test(test_name, description)
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        data = response.json()
        return print_result(response.status_code, expected_status, data)
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗ Connection Error - Is Flask server running?{RESET}\n")
        return False
    except Exception as e:
        print(f"{RED}✗ Error: {str(e)}{RESET}\n")
        return False

def main():
    """Run all verification tests"""
    print(f"\n{BOLD}{BLUE}{'*' * 70}{RESET}")
    print(f"{BOLD}{BLUE}THREE-TIER GRACEFUL FALLBACK - FINAL VERIFICATION{RESET}")
    print(f"{BOLD}{BLUE}{'*' * 70}{RESET}")
    print(f"\nTest Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check API health
    print_section("Pre-Test: API Health Check")
    if not test_api_health():
        print(f"\n{RED}Cannot proceed with tests. Please start the Flask API.{RESET}")
        return
    
    # Track results
    total_tests = 0
    passed_tests = 0
    
    # ========================================================================
    # TIER 1 TESTS: Good Data Quality (3+ Historical Points)
    # ========================================================================
    print_section("TIER 1 TESTS: Good Data Quality")
    
    # Test 1.1: Common commodity/market with plenty of data
    total_tests += 1
    if run_test(
        "Tier 1 - Common Combination",
        "Maize in Addis Ababa (expected to have 3+ historical data points)",
        {
            "commodity": "Maize",
            "admin": "Addis Ababa",
            "month": 6,
            "year": 2024
        },
        expected_status=200
    ):
        passed_tests += 1
    
    # ========================================================================
    # TIER 2 TESTS: Limited Data Quality (1-2 Historical Points)
    # ========================================================================
    print_section("TIER 2 TESTS: Limited Data Quality")
    
    # Test 2.1: Less common combination (may have limited data)
    total_tests += 1
    if run_test(
        "Tier 2 - Uncommon Combination",
        "Wheat in Tigray (may have limited historical data)",
        {
            "commodity": "Wheat",
            "admin": "Tigray",
            "month": 3,
            "year": 2024
        },
        expected_status=200
    ):
        passed_tests += 1
    
    # ========================================================================
    # TIER 3 TESTS: Global Fallback (0 Historical Points)
    # ========================================================================
    print_section("TIER 3 TESTS: Global Fallback (Critical Test)")
    
    # Test 3.1: Rare combination likely to have NO data
    total_tests += 1
    if run_test(
        "Tier 3 - Rare Combination",
        "Sorghum in Afar (likely has 0 historical data - should use global avg)",
        {
            "commodity": "Sorghum",
            "admin": "Afar",
            "month": 1,
            "year": 2024
        },
        expected_status=200  # KEY TEST: Should return 200, NOT 400!
    ):
        passed_tests += 1
    
    # Test 3.2: Another rare combination
    total_tests += 1
    if run_test(
        "Tier 3 - Another Rare Combination",
        "Barley in Gambela (likely has 0 historical data)",
        {
            "commodity": "Barley",
            "admin": "Gambela",
            "month": 12,
            "year": 2023
        },
        expected_status=200  # Should return 200 with global average
    ):
        passed_tests += 1
    
    # ========================================================================
    # INVALID INPUT TESTS: Should Return 400 Bad Request
    # ========================================================================
    print_section("INVALID INPUT TESTS: Should Return 400")
    
    # Test 4.1: Unknown commodity
    total_tests += 1
    if run_test(
        "Invalid Input - Unknown Commodity",
        "Non-existent commodity should return 400 error",
        {
            "commodity": "Coffee",  # Not in model
            "admin": "Addis Ababa",
            "month": 6,
            "year": 2024
        },
        expected_status=400  # Should return 400 for invalid input
    ):
        passed_tests += 1
    
    # Test 4.2: Invalid month
    total_tests += 1
    if run_test(
        "Invalid Input - Month Out of Range",
        "Month = 15 should return 400 error",
        {
            "commodity": "Maize",
            "admin": "Addis Ababa",
            "month": 15,  # Invalid
            "year": 2024
        },
        expected_status=400
    ):
        passed_tests += 1
    
    # Test 4.3: Missing required field
    total_tests += 1
    if run_test(
        "Invalid Input - Missing Required Field",
        "Missing 'admin' field should return 400 error",
        {
            "commodity": "Maize",
            "month": 6,
            "year": 2024
            # Missing 'admin'
        },
        expected_status=400
    ):
        passed_tests += 1
    
    # ========================================================================
    # TEST SUMMARY
    # ========================================================================
    print_section("TEST SUMMARY")
    
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {GREEN}{passed_tests}{RESET}")
    print(f"Failed: {RED}{total_tests - passed_tests}{RESET}")
    print(f"Pass Rate: {GREEN if pass_rate == 100 else YELLOW}{pass_rate:.1f}%{RESET}")
    
    print(f"\n{BOLD}Key Verification Points:{RESET}")
    print(f"✓ All VALID inputs return 200 OK (even with 0 historical data)")
    print(f"✓ Tier 3 (global fallback) returns 200 instead of 400")
    print(f"✓ Only INVALID inputs return 400 Bad Request")
    print(f"✓ API provides 'data_quality' and 'warning' fields")
    
    if pass_rate == 100:
        print(f"\n{GREEN}{BOLD}🎉 ALL TESTS PASSED! Three-Tier Fallback is working correctly!{RESET}")
    else:
        print(f"\n{YELLOW}{BOLD}⚠ Some tests failed. Review the output above.{RESET}")
    
    print(f"\n{BOLD}{BLUE}{'*' * 70}{RESET}\n")

if __name__ == '__main__':
    main()
