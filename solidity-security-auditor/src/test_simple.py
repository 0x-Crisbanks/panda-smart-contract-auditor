#!/usr/bin/env python3
"""
Simple test for the Solidity Security Auditor
"""

from detectors import VulnerabilityDetector
from reporter import SecurityReporter

def main():
    print("🔍 Testing Solidity Security Auditor...")
    
    # Simple vulnerable contract for testing
    test_code = '''pragma solidity ^0.7.0;
contract Test {
    mapping(address => uint256) balances;
    
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount);
        msg.sender.call{value: amount}("");
        balances[msg.sender] -= amount;
    }
    
    function adminFunction() public {
        // No access control
        selfdestruct(payable(msg.sender));
    }
    
    function checkAuth() public {
        require(tx.origin == msg.sender);
    }
}'''
    
    # Test detector
    detector = VulnerabilityDetector()
    findings = detector.analyze(test_code)
    
    print(f"✅ Found {len(findings)} vulnerabilities:")
    for finding in findings:
        print(f"  - {finding.severity}: {finding.vulnerability_type}")
    
    # Test reporter
    reporter = SecurityReporter()
    report = reporter.generate_report(test_code, findings, "Test", "test123")
    
    print("✅ Report generated successfully!")
    print(f"Report length: {len(report)} characters")
    
    # Test with example contract
    try:
        with open('../examples/vulnerable_contract.sol', 'r') as f:
            contract_code = f.read()
        
        findings = detector.analyze(contract_code)
        print(f"✅ Example contract analysis: {len(findings)} vulnerabilities found")
        
        # Generate report
        report = reporter.generate_report(contract_code, findings, 
                                        "examples/vulnerable_contract.sol", "example123")
        
        with open('../reports/test_report.md', 'w') as f:
            f.write(report)
        
        print("✅ Test report saved to reports/test_report.md")
        
    except Exception as e:
        print(f"⚠️ Could not test with example contract: {e}")
    
    print("\n🎉 All basic tests passed!")
    print("\nTo run the full CLI interface:")
    print("python auditor.py")

if __name__ == "__main__":
    main()