#!/usr/bin/env python3
"""
Test the simplified option 1 functionality
"""

import sys
sys.path.insert(0, '/Users/thewizard/Desktop/Panda/solidity-security-auditor/src')

import pyperclip
from auditor import MultiBlockchainAuditor

def test_option1_simple():
    """Test that option 1 now works with clipboard correctly."""
    
    print("🎯 Testing PANDA WEB3 - Option 1 Simplified Fix")
    print("=" * 80)
    
    # Sample vulnerable contract
    sample_contract = '''pragma solidity ^0.8.0;

contract VulnerableContract {
    address public owner;
    mapping(address => uint) public balances;
    
    constructor() {
        owner = msg.sender;
    }
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw() public {
        uint balance = balances[msg.sender];
        require(balance > 0, "No balance");
        
        // Vulnerability: Reentrancy attack possible
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] = 0; // State change after external call
    }
    
    function unsafeTransfer(address to, uint amount) public {
        // Vulnerability: No access control
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}'''
    
    print(f"\n📋 Setting up clipboard with sample contract...")
    print(f"Contract length: {len(sample_contract)} characters")
    
    # Set clipboard content
    pyperclip.copy(sample_contract)
    
    print("✅ Contract copied to clipboard")
    
    # Test the analysis
    auditor = MultiBlockchainAuditor()
    
    print(f"\n🔍 Testing clipboard analysis...")
    
    try:
        # Test reading clipboard
        clipboard_content = pyperclip.paste()
        if clipboard_content == sample_contract:
            print("✅ Clipboard content matches")
        else:
            print("❌ Clipboard content mismatch")
            return False
            
        # Test the analysis method
        auditor._analyze_code(clipboard_content, "Clipboard Test", "")
        print("✅ SUCCESS: Contract analysis executed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_option1_simple()
    
    if success:
        print("\n🎉 OPTION 1 SIMPLIFIED FIX SUCCESSFUL!")
        print("\n📋 INSTRUCTIONS FOR USER:")
        print("1. Copy your smart contract to clipboard")
        print("2. Run PANDA WEB3")
        print("3. Select Option 1")
        print("4. Press Enter (for clipboard)")
        print("5. See analysis results!")
    else:
        print("\n❌ Option 1 still needs work")