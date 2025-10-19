#!/usr/bin/env python3
"""
Test PolygonScan V2 API call
"""

import requests

def test_polygonscan_v2_api():
    """Test direct call to PolygonScan V2 API."""
    
    # USDC Polygon contract
    address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    
    # PolygonScan V2 API endpoint (via Etherscan)
    api_url = "https://api.etherscan.io/v2/api"
    
    params = {
        'chainid': '137',  # Polygon chain ID
        'module': 'contract',
        'action': 'getsourcecode',
        'address': address,
        'apikey': 'YourApiKeyToken'  # Free API key
    }
    
    print(f"🔍 Testing PolygonScan V2 API call:")
    print(f"📍 Address: {address}")
    print(f"🌐 API URL: {api_url}")
    print(f"📋 Params: {params}")
    
    try:
        response = requests.get(api_url, params=params, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Response status: {data.get('status')}")
            print(f"📄 Response message: {data.get('message', 'No message')}")
            
            if data.get('status') == '1':
                result = data.get('result', [])
                if result and result[0]:
                    contract_data = result[0]
                    print(f"✅ Contract found: {contract_data.get('ContractName', 'Unknown')}")
                    print(f"📝 Source code length: {len(contract_data.get('SourceCode', ''))}")
                    print(f"🔧 Compiler: {contract_data.get('CompilerVersion', 'Unknown')}")
                    return True
                else:
                    print("❌ No contract data in result")
            else:
                print(f"❌ API Status: {data.get('status')}")
                print(f"❌ Message: {data.get('message', 'Unknown error')}")
                print(f"❌ Result: {data.get('result', 'No result')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"❌ Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return False

if __name__ == "__main__":
    success = test_polygonscan_v2_api()
    if success:
        print("\n🎉 SUCCESS: V2 API is working!")
    else:
        print("\n❌ FAILURE: V2 API call failed")