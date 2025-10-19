#!/usr/bin/env python3
"""
Simple test for Polygon contract detection
"""

import sys
sys.path.insert(0, '/Users/thewizard/Desktop/Panda/solidity-security-auditor/src')

from contract_fetcher import ContractSourceFetcher, BlockchainNetwork

def test_polygon_detection():
    """Test that Polygon contracts are detected correctly."""
    fetcher = ContractSourceFetcher()
    
    # Test USDC Polygon address with URL hint
    address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    url_hint = "https://polygonscan.com/address/0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    
    print(f"🔍 Testing network detection:")
    print(f"📍 Address: {address}")
    print(f"🌐 URL hint: {url_hint}")
    
    # Test the internal detection method
    detected_network = fetcher._detect_network_from_address(address, url_hint)
    
    print(f"🎯 Detected network: {detected_network}")
    print(f"✅ Expected: {BlockchainNetwork.POLYGON_MAINNET}")
    
    if detected_network == BlockchainNetwork.POLYGON_MAINNET:
        print("🎉 SUCCESS: Polygon network correctly detected!")
        return True
    else:
        print("❌ FAILURE: Wrong network detected!")
        return False

if __name__ == "__main__":
    test_polygon_detection()