#!/usr/bin/env python3
"""
Demo script showing how to use the Solidity Security Auditor
"""

print("🚀 Solidity Security Auditor - Complete Project Demo")
print("=" * 60)

print("\n📁 Project Structure:")
import os
for root, dirs, files in os.walk("solidity-security-auditor"):
    level = root.replace("solidity-security-auditor", "").count(os.sep)
    indent = " " * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 2 * (level + 1)
    for file in files:
        if not file.startswith('.') and not file.startswith('__pycache__'):
            print(f"{subindent}{file}")

print("\n🔍 Running Security Analysis Test...")

# Run the test
import subprocess
import sys

try:
    result = subprocess.run([
        sys.executable, 
        "/Users/thewizard/Desktop/Panda/solidity-security-auditor/src/test_simple.py"
    ], 
    env={**os.environ, "PYTHONPATH": "/Users/thewizard/Desktop/Panda/solidity-security-auditor/src"},
    capture_output=True, 
    text=True
    )
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
        
    print(f"Exit code: {result.returncode}")
    
except Exception as e:
    print(f"Error running test: {e}")

print("\n📋 Quick Start Guide:")
print("1. cd solidity-security-auditor")
print("2. python3 -m venv venv")
print("3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
print("4. pip install -r requirements.txt")
print("5. cd src")
print("6. python auditor.py")
print("7. Select option 1 and analyze: ../examples/vulnerable_contract.sol")

print("\n🎯 Educational Features:")
print("✅ Interactive CLI with beautiful terminal interface")
print("✅ Detects 10+ common smart contract vulnerabilities")
print("✅ Generates professional security audit reports")
print("✅ Includes educational vulnerable contract example")
print("✅ Educational explanations for each vulnerability type")
print("✅ Ethical disclaimers and responsible disclosure guidance")
print("✅ Supports both regex patterns and Slither integration")

print("\n⚠️ Ethical Use Reminder:")
print("This tool is for EDUCATIONAL and AUTHORIZED security research ONLY!")
print("Always follow responsible disclosure practices.")

print("\n🎉 Project Complete!")
print("The Solidity Security Auditor is ready for educational use.")