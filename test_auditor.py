#!/usr/bin/env python3
"""
Test script for the Solidity Security Auditor
"""

import sys
import os
sys.path.append('solidity-security-auditor/src')

from detectors import VulnerabilityDetector, Finding
from reporter import SecurityReporter

def test_detector():
    """Test the vulnerability detector with sample code."""
    print("🔍 Testing Vulnerability Detector...")
    
    detector = VulnerabilityDetector()
    
    # Test code with multiple vulnerabilities
    test_code = '''
pragma solidity ^0.7.0;

contract VulnerableTest {
    mapping(address => uint256) public balances;
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    // Reentrancy vulnerability
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // External call before state update - VULNERABLE!
        (bool success, ) = msg.sender.call{value: amount}("");
        
        // State update after external call - allows reentrancy
        balances[msg.sender] -= amount;
    }
    
    // Access control issue
    function adminWithdraw(uint256 amount) public {
        // No access control - anyone can call this!
        payable(msg.sender).transfer(amount);
    }
    
    // tx.origin vulnerability
    function authorize(address user) public {
        require(tx.origin == owner, "Only owner");
        // ... authorize user
    }
    
    // Integer overflow (pre-0.8.0)
    function deposit() public payable {
        balances[msg.sender] += msg.value;
        // Potential overflow without SafeMath
        uint256 bonus = msg.value * 200; // Could overflow
        balances[msg.sender] += bonus;
    }
    
    // Deprecated function
    function legacy() public {
        bytes32 hash = sha3(abi.encodePacked(msg.sender));
        if (hash[0] == 0x00) {
            throw; // Deprecated
        }
    }
}
    '''
    
    findings = detector.analyze(test_code)
    
    print(f"✅ Found {len(findings)} vulnerabilities:")
    
    severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Info': 0}
    for finding in findings:
        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
        print(f"   - {finding.severity}: {finding.vulnerability_type} (Line {finding.line_number})")
    
    print(f"\n📊 Severity Breakdown:")
    for severity, count in severity_counts.items():
        if count > 0:
            print(f"   {severity}: {count}")
    
    return findings, test_code

def test_reporter(findings, code):
    """Test the report generator."""
    print("\n📄 Testing Report Generator...")
    
    reporter = SecurityReporter()
    
    # Generate Markdown report
    report = reporter.generate_report(
        code=code,
        findings=findings,
        source="Test Script",
        code_hash="test123abc"
    )
    
    # Save test report
    os.makedirs('solidity-security-auditor/reports', exist_ok=True)
    with open('solidity-security-auditor/reports/test_report.md', 'w') as f:
        f.write(report)
    
    print("✅ Markdown report generated successfully!")
    
    # Generate JSON report
    json_report = reporter.generate_json_report(
        code=code,
        findings=findings,
        source="Test Script", 
        code_hash="test123abc"
    )
    
    print(f"✅ JSON report generated with {len(json_report['findings'])} findings")
    
    return report

def test_integration():
    """Test the complete workflow."""
    print("\n🔧 Testing Complete Integration...")
    
    # Test with the provided vulnerable contract
    try:
        with open('solidity-security-auditor/examples/vulnerable_contract.sol', 'r') as f:
            contract_code = f.read()
        
        detector = VulnerabilityDetector()
        findings = detector.analyze(contract_code)
        
        print(f"✅ Analyzed vulnerable_contract.sol: {len(findings)} vulnerabilities found")
        
        # Generate report for the contract
        reporter = SecurityReporter()
        report = reporter.generate_report(
            code=contract_code,
            findings=findings,
            source="examples/vulnerable_contract.sol",
            code_hash="vulnerable_example"
        )
        
        with open('solidity-security-auditor/reports/vulnerable_contract_report.md', 'w') as f:
            f.write(report)
        
        print("✅ Full report generated for vulnerable contract example")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Solidity Security Auditor Tests...\n")
    
    try:
        # Test 1: Basic detector functionality
        findings, code = test_detector()
        
        # Test 2: Report generation
        test_reporter(findings, code)
        
        # Test 3: Integration with example contract
        integration_success = test_integration()
        
        if integration_success:
            print("\n🎉 All tests passed! The Solidity Security Auditor is working correctly.")
            print("\n📋 Next steps:")
            print("1. Run: cd solidity-security-auditor/src && python auditor.py")
            print("2. Select option 1 to analyze the vulnerable contract")
            print("3. Path: ../examples/vulnerable_contract.sol")
            print("4. Review the generated reports in the reports/ directory")
        else:
            print("\n⚠️ Some tests failed. Please check the error messages above.")
            
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()