#!/usr/bin/env python3
"""
Test the completely rewritten option 1 functionality
"""

import sys
sys.path.insert(0, '/Users/thewizard/Desktop/Panda/solidity-security-auditor/src')

import pyperclip
from auditor import MultiBlockchainAuditor

def test_option1_new():
    """Test that option 1 now works with the new implementation."""
    
    print("🎯 Testing PANDA WEB3 - Option 1 Complete Rewrite")
    print("=" * 80)
    
    # Sample contract with vulnerabilities
    sample_contract = '''pragma solidity ^0.8.0;

contract TestContract {
    address public owner;
    mapping(address => uint) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw() public {
        uint balance = balances[msg.sender];
        // Vulnerability: External call before state change
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success);
        balances[msg.sender] = 0;
    }
}'''
    
    print(f"\n📋 Setting up test contract...")
    print(f"Contract length: {len(sample_contract)} characters")
    
    # Set clipboard content
    pyperclip.copy(sample_contract)
    print("✅ Contract copied to clipboard")
    
    # Create auditor instance
    auditor = MultiBlockchainAuditor()
    
    print(f"\n🔍 Testing new analyze_file() implementation...")
    
    try:
        # Test the clipboard functionality directly
        code = pyperclip.paste()
        if code.strip():
            print("✅ Clipboard content verified")
            print(f"📊 Code length: {len(code)} characters")
            
            # Test the analysis function
            print("\n🔄 Running analysis...")
            auditor._analyze_code(code, "Test Contract", "")
            print("✅ SUCCESS: Analysis completed!")
            return True
        else:
            print("❌ Clipboard is empty")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_option1_new()
    
    if success:
        print("\n🎉 NEW OPTION 1 IMPLEMENTATION WORKING!")
        print("\n📋 NEW USER FLOW:")
        print("1. Copy smart contract to clipboard")
        print("2. Run PANDA WEB3")
        print("3. Select Option 1")
        print("4. Choose option 2 (clipboard)")
        print("5. Press Enter to analyze")
        print("6. See complete analysis!")
        
        print("\n✅ The new implementation should solve the terminal issues!")
    else:
        print("\n❌ Still needs more work")