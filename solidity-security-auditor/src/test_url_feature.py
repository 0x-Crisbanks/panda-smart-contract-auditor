#!/usr/bin/env python3
"""
Test script for URL-based contract analysis feature
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detectors import VulnerabilityDetector
from reporter import SecurityReporter
import requests

def test_url_fetching():
    """Test fetching and analyzing contracts from URLs."""
    
    print("🌐 Testing URL-based Contract Analysis Feature")
    print("=" * 60)
    
    # Test URLs (these are example URLs - replace with actual ones)
    test_urls = [
        {
            'url': 'https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/master/contracts/token/ERC20/ERC20.sol',
            'description': 'OpenZeppelin ERC20 (Safe Contract)',
            'expected': 'Should find minimal or no vulnerabilities'
        },
        {
            'url': 'https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol',
            'description': 'Chainlink Aggregator Interface',
            'expected': 'Interface only, minimal findings'
        }
    ]
    
    detector = VulnerabilityDetector()
    reporter = SecurityReporter()
    
    for test_case in test_urls:
        print(f"\n📥 Testing: {test_case['description']}")
        print(f"URL: {test_case['url'][:60]}...")
        print(f"Expected: {test_case['expected']}")
        
        try:
            # Convert GitHub URL to raw if needed
            url = test_case['url']
            if 'github.com' in url and '/blob/' in url:
                url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
            
            # Fetch the contract
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                code = response.text
                
                # Check if it's Solidity code
                if 'pragma solidity' in code or 'contract ' in code or 'interface ' in code:
                    print("✅ Successfully fetched Solidity code")
                    
                    # Analyze the code
                    findings = detector.analyze(code)
                    
                    print(f"🔍 Analysis Results:")
                    print(f"   Total findings: {len(findings)}")
                    
                    severity_counts = {}
                    for finding in findings:
                        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
                    
                    for severity in ['Critical', 'High', 'Medium', 'Low', 'Info']:
                        count = severity_counts.get(severity, 0)
                        if count > 0:
                            print(f"   {severity}: {count}")
                else:
                    print("❌ Content doesn't appear to be Solidity code")
            else:
                print(f"❌ Failed to fetch: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ URL Analysis Feature Test Complete!")
    print("\nHow to use in the main application:")
    print("1. Run: python auditor.py")
    print("2. Select option 3: '🌐 Analyze contract from URL'")
    print("3. Enter a URL to a Solidity contract")
    print("   - GitHub raw URLs (raw.githubusercontent.com)")
    print("   - Direct .sol file URLs")
    print("   - Etherscan contract URLs (limited without API key)")

def test_github_url_conversion():
    """Test GitHub URL conversion."""
    print("\n🔧 Testing GitHub URL Conversion")
    print("-" * 40)
    
    test_cases = [
        {
            'input': 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol',
            'expected': 'https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/master/contracts/token/ERC20/ERC20.sol'
        }
    ]
    
    for test in test_cases:
        url = test['input']
        if 'github.com' in url and '/blob/' in url:
            converted = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        else:
            converted = url
        
        print(f"Input:    {test['input'][:50]}...")
        print(f"Output:   {converted[:50]}...")
        print(f"✅ Match: {converted == test['expected']}")

def main():
    """Run all tests."""
    print("🚀 Solidity Security Auditor - URL Feature Test\n")
    
    test_url_fetching()
    test_github_url_conversion()
    
    print("\n🎉 All tests completed!")
    print("\nNote: For production use with Etherscan:")
    print("- You'll need an Etherscan API key")
    print("- Update the code to use Etherscan's API endpoint")
    print("- API docs: https://docs.etherscan.io/")

if __name__ == "__main__":
    main()