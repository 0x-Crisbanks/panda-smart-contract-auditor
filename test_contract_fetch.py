#!/usr/bin/env python3
"""
Test contract fetching specifically for Polygon
"""

import sys
sys.path.insert(0, '/Users/thewizard/Desktop/Panda/solidity-security-auditor/src')

from contract_fetcher import ContractSourceFetcher

def test_polygon_contract_fetch():
    """Test fetching USDC Polygon contract."""
    fetcher = ContractSourceFetcher()
    
    # Test USDC Polygon address with URL hint
    address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    url_hint = "https://polygonscan.com/address/0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    
    print(f"🔍 Testing contract fetching:")
    print(f"📍 Address: {address}")
    print(f"🌐 URL hint: {url_hint}")
    
    # Test actual contract fetching
    contract_info = fetcher.fetch_contract_source(address, url_hint)
    
    if contract_info:
        print("🎉 SUCCESS: Contract fetched successfully!")
        print(f"📝 Contract name: {contract_info.contract_name}")
        print(f"🌐 Blockchain: {contract_info.blockchain}")
        print(f"✅ Verified: {contract_info.is_verified}")
        return True
    else:
        print("❌ FAILURE: Could not fetch contract!")
        return False

if __name__ == "__main__":
    test_polygon_contract_fetch()