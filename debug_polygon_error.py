#!/usr/bin/env python3
"""
Debug Polygon API error response
"""

import requests

def debug_polygon_api():
    """Debug the exact error response from Polygon V2 API."""
    
    address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    api_url = "https://api.etherscan.io/v2/api"
    
    params = {
        'chainid': '137',
        'module': 'contract',
        'action': 'getsourcecode',
        'address': address,
        'apikey': 'YourApiKeyToken'
    }
    
    print(f"🔍 Debugging Polygon V2 API response:")
    
    try:
        response = requests.get(api_url, params=params, timeout=10)
        data = response.json()
        
        print(f"📄 Full response: {data}")
        print(f"📊 Status: {data.get('status')}")
        print(f"📊 Message: {data.get('message')}")
        print(f"📊 Result: {data.get('result')}")
        
        # Check the exact conditions
        status = data.get('status')
        message = data.get('message', '')
        result = data.get('result', '')
        
        print(f"\n🔍 Analysis:")
        print(f"   status != '1': {status != '1'}")
        print(f"   'Invalid API Key' in message: {'Invalid API Key' in message}")
        print(f"   'Missing/Invalid API Key' in message: {'Missing/Invalid API Key' in message}")
        print(f"   message == 'NOTOK': {message == 'NOTOK'}")
        
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_polygon_api()