# 🔒 Solidity Security Auditor

**Educational Smart Contract Security Analysis Tool**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Educational Use](https://img.shields.io/badge/Purpose-Educational-green.svg)](#)

## ⚠️ CRITICAL ETHICAL DISCLAIMER

### 🚨 EDUCATIONAL AND AUTHORIZED USE ONLY 🚨

**This tool is designed EXCLUSIVELY for:**
- ✅ **Educational purposes** - Learning about smart contract security
- ✅ **Authorized security assessments** - Auditing contracts you own or have permission to test
- ✅ **Academic research** - Understanding blockchain security concepts
- ✅ **Responsible disclosure** - Following ethical security research practices

**This tool must NEVER be used for:**
- ❌ **Exploiting vulnerabilities** in smart contracts without explicit permission
- ❌ **Attacking or compromising** blockchain networks or applications
- ❌ **Financial gain** through unauthorized exploitation
- ❌ **Any malicious activities** that could harm users or protocols

### 🔐 Responsible Disclosure Policy

If you discover vulnerabilities in deployed smart contracts using this tool:

1. **DO NOT EXPLOIT** the vulnerability for personal gain
2. **CONTACT** the contract owners or development team immediately
3. **ALLOW REASONABLE TIME** for the issue to be addressed (typically 90 days)
4. **FOLLOW COORDINATED DISCLOSURE** practices
5. **DOCUMENT YOUR FINDINGS** professionally and constructively

**Remember: The goal of security research is to make the blockchain ecosystem safer for everyone.**

### ⚖️ Legal Notice

Users are **solely responsible** for ensuring their use of this tool complies with applicable laws and regulations in their jurisdiction. The developers assume **no responsibility** for misuse of this tool. Always obtain proper authorization before testing smart contracts you do not own.

---

## 📋 Overview

The Solidity Security Auditor is an educational tool designed to help developers, security researchers, and students learn about smart contract security by identifying common vulnerabilities in Solidity code. The tool provides detailed explanations of each vulnerability type, potential exploitation scenarios (without executable exploit code), and remediation recommendations.

### 🎯 Features

- **🔍 Comprehensive Analysis**: Detects 10+ common vulnerability patterns
- **🎨 Beautiful CLI Interface**: Rich terminal UI with progress indicators and tables
- **📊 Professional Reports**: Generates detailed Markdown and JSON audit reports
- **📚 Educational Content**: Includes explanations and learning resources for each vulnerability
- **🔧 Multiple Input Methods**: Analyze local files, clipboard, or **URLs** 
- **🌐 URL Analysis**: Fetch and analyze contracts directly from:
  - GitHub repositories (automatic raw URL conversion)
  - Etherscan/BSCScan/PolygonScan (limited without API key)
  - Any direct .sol file URL
- **📈 Analysis History**: Track multiple analyses in a session
- **🚀 Extensible Design**: Supports both regex patterns and Slither integration

### 🔍 Detected Vulnerabilities

| Vulnerability Type | Severity | Description |
|-------------------|----------|-------------|
| **Reentrancy** | Critical | External calls before state updates allowing recursive exploitation |
| **Unchecked External Calls** | High | Missing return value validation for external calls |
| **Access Control Issues** | High | Missing or weak access controls on sensitive functions |
| **Integer Overflow/Underflow** | High | Arithmetic errors in pre-Solidity 0.8.0 contracts |
| **tx.origin Authentication** | Medium | Vulnerable authentication using tx.origin instead of msg.sender |
| **Weak Randomness** | Medium | Using predictable blockchain data for randomness |
| **Deprecated Functions** | Low | Usage of outdated Solidity language features |
| **Uninitialized Storage** | Medium | Dangerous uninitialized storage pointer usage |
| **Delegatecall Dangers** | High | Unrestricted or dangerous delegatecall usage |

---

## 🚀 Installation

### Prerequisites

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Install Git](https://git-scm.com/downloads)
- **Optional**: [Slither](https://github.com/crytic/slither) for advanced analysis

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/solidity-security-auditor.git
cd solidity-security-auditor
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Optional - Install Slither

For enhanced analysis capabilities, install Slither:

```bash
# Option 1: Using pip
pip install slither-analyzer

# Option 2: Using homebrew (macOS)
brew install slither

# Option 3: From source
git clone https://github.com/crytic/slither.git
cd slither
python setup.py install
```

**Note**: Slither requires additional system dependencies. See [Slither Installation Guide](https://github.com/crytic/slither#installation) for detailed instructions.

---

## 🎮 Usage

### Starting the Application

```bash
cd src
python auditor.py
```

### Interactive Menu Options

The tool provides an intuitive menu interface:

```
🔒 SOLIDITY SECURITY AUDITOR 🔒
Educational Smart Contract Security Analysis Tool

⚠️  ETHICAL USE ONLY ⚠️

🔍 Analysis Options
┌────────────────────────────────────────────────┐
│ 1  │ 📄 Analyze local Solidity file            │
│ 2  │ 📋 Analyze code from clipboard             │
│ 3  │ 📊 View analysis history                   │
│ 4  │ ℹ️  About vulnerability types              │
│ 5  │ ❌ Exit                                    │
└────────────────────────────────────────────────┘
```

### Example Workflow

1. **Analyze a Local File**:
   ```bash
   Select option: 1
   Enter the path to the Solidity file: examples/vulnerable_contract.sol
   ```

2. **View Results**: The tool displays a summary table with vulnerability counts and detailed findings

3. **Generate Report**: Choose to generate a professional audit report in Markdown format

4. **Review Findings**: Each finding includes:
   - Vulnerability type and severity
   - Line number and code snippet
   - Technical explanation
   - Remediation recommendations
   - References to CWE/SWC classifications

---

## 📖 Example Analysis

### Testing with the Provided Example

The repository includes a vulnerable smart contract for testing:

```bash
# Navigate to source directory
cd src

# Run the auditor
python auditor.py

# Select option 1 (Analyze local Solidity file)
# Enter path: ../examples/vulnerable_contract.sol
```

### Expected Output

The tool will detect multiple vulnerabilities including:

- **Critical**: Reentrancy vulnerabilities in withdraw functions
- **High**: Unchecked external calls and access control issues
- **Medium**: Use of tx.origin and weak randomness
- **Low**: Deprecated function usage

### Sample Report Structure

```markdown
# Smart Contract Security Audit Report

## Executive Summary
🔴 **CRITICAL RISK** - Critical vulnerabilities detected

## Findings
### 🔴 Critical Severity Findings
#### Finding #1: Reentrancy
**Severity:** Critical
**Line:** 45
**Description:** External call before state update...
**Recommendation:** Use ReentrancyGuard modifier...
```

---

## 🎓 Educational Resources

### Learning Platforms

- **[Ethernaut](https://ethernaut.openzeppelin.com/)** - Interactive smart contract hacking challenges
- **[Damn Vulnerable DeFi](https://www.damnvulnerabledefi.xyz/)** - DeFi security challenges and attack scenarios
- **[Capture The Ether](https://capturetheether.com/)** - Ethereum security puzzles and games

### Documentation and Standards

- **[SWC Registry](https://swcregistry.io/)** - Smart Contract Weakness Classification and Registry
- **[CWE](https://cwe.mitre.org/)** - Common Weakness Enumeration database
- **[Consensys Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)**
- **[OpenZeppelin Security Documentation](https://docs.openzeppelin.com/contracts/4.x/security)**

### Security Tools

- **[Slither](https://github.com/crytic/slither)** - Static analysis framework for Solidity
- **[MythX](https://mythx.io/)** - Comprehensive security analysis platform
- **[Mythril](https://github.com/ConsenSys/mythril)** - Security analysis tool for EVM bytecode
- **[Securify](https://securify.chainsecurity.com/)** - Formal verification and security analysis

---

## 🔧 Configuration

### Environment Variables

You can configure the tool using environment variables:

```bash
# Set custom reports directory
export AUDITOR_REPORTS_DIR="/path/to/reports"

# Enable debug logging
export AUDITOR_DEBUG=true

# Disable Slither integration
export AUDITOR_DISABLE_SLITHER=true
```

### Custom Patterns

Advanced users can extend the detection patterns by modifying `src/detectors.py`:

```python
# Add custom vulnerability pattern
'custom_pattern': {
    'pattern': r'your_regex_pattern',
    'severity': 'Medium',
    'description': 'Description of the vulnerability',
    'explanation': 'How this could be exploited...',
    'recommendation': 'How to fix this issue...'
}
```

---

## 📁 Project Structure

```
solidity-security-auditor/
├── src/
│   ├── auditor.py          # Main CLI application
│   ├── detectors.py        # Vulnerability detection engine
│   └── reporter.py         # Report generation system
├── examples/
│   └── vulnerable_contract.sol  # Educational vulnerable contract
├── tests/
│   └── test_*.py          # Unit tests (optional)
├── reports/               # Generated audit reports
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🧪 Development and Testing

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-detector`)
3. Make changes following the coding standards
4. Add tests for new functionality
5. Submit a pull request

**Note**: All contributions must maintain the educational and ethical focus of the project.

---

## ⚠️ Limitations

### What This Tool **DOES**:
- ✅ Detects common vulnerability patterns using static analysis
- ✅ Provides educational explanations and remediation guidance
- ✅ Generates professional audit reports
- ✅ Integrates with advanced tools like Slither

### What This Tool **DOES NOT**:
- ❌ Detect all possible vulnerabilities (manual review still required)
- ❌ Analyze external contract dependencies
- ❌ Test runtime behavior or gas optimization
- ❌ Verify economic model security
- ❌ Provide exploit code or attack scenarios

### Recommendations:
- **Always** conduct manual code review by experienced auditors
- **Consider** professional security audits for production contracts
- **Test** thoroughly on testnets before mainnet deployment
- **Implement** comprehensive unit and integration tests
- **Monitor** deployed contracts for suspicious activity

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- Rich: BSD License
- Slither: AGPL-3.0 License (optional dependency)

---

## 🤝 Support and Community

### Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/your-username/solidity-security-auditor/issues)
- **Discussions**: [Join community discussions](https://github.com/your-username/solidity-security-auditor/discussions)
- **Documentation**: [Read the full documentation](https://github.com/your-username/solidity-security-auditor/wiki)

### Contributing to Security Research

This tool is part of the broader effort to improve smart contract security through education and tooling. Consider contributing to:

- **Bug Reports**: Help improve the tool by reporting issues
- **New Detectors**: Add detection patterns for new vulnerability types
- **Educational Content**: Improve explanations and learning resources
- **Integration**: Help integrate with other security tools

---

## 🙏 Acknowledgments

- **OpenZeppelin** - For security standards and educational resources
- **ConsenSys** - For smart contract best practices and security tools
- **Trail of Bits** - For the Slither static analysis framework
- **Ethereum Security Community** - For continuous research and education
- **Damn Vulnerable DeFi** - For inspiration on educational vulnerable contracts

---
      --PASO PARA PROBARLO--

 Para probar el Solidity Security Auditor, sigue estos pasos:

  🚀 Guía de Instalación y Prueba

  1️⃣ Instalar dependencias

  cd /Users/thewizard/Desktop/Panda/solidity-security-auditor
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

  2️⃣ Ejecutar el auditor

  cd src
  python3 auditor.py

  3️⃣ Opciones del menú interactivo

  Verás este menú:
  🔍 Analysis Options
  1 │ 📄 Analyze local Solidity file
  2 │ 📋 Analyze code from clipboard
  3 │ 🌐 Analyze contract from URL (Etherscan/etc)
  4 │ 📊 View analysis history
  5 │ ℹ️  About vulnerability types
  6 │ ❌ Exit

  4️⃣ Probar con el contrato vulnerable de ejemplo

  1. Selecciona opción 1
  2. Ingresa la ruta: ../examples/vulnerable_contract.sol
  3. El auditor detectará múltiples vulnerabilidades
  4. Te preguntará si quieres generar un reporte - responde y (yes)

  5️⃣ Probar análisis desde URL

  1. Selecciona opción 3 (🌐 Analyze contract from URL)
  2. Ingresa una URL, por ejemplo:
     - GitHub: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol
     - Raw GitHub: https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/master/contracts/token/ERC20/ERC20.sol
     - Etherscan: https://etherscan.io/address/0x... (limitado sin API key)
  3. El auditor descargará y analizará el contrato automáticamente

  6️⃣ Prueba rápida alternativa

  Si prefieres una prueba directa sin menú interactivo:

  cd /Users/thewizard/Desktop/Panda/solidity-security-auditor/src
  python3 test_simple.py

  Esto analizará automáticamente el contrato vulnerable y generará un
  reporte en reports/test_report.md

  📊 Resultado esperado

  El auditor debería detectar ~13 vulnerabilidades incluyendo:
  - Critical: Reentrancy
  - High: Access control issues, unchecked calls
  - Medium: tx.origin, weak randomness
  - Low: Deprecated functions

  📄 Ver el reporte generado

  Los reportes se guardan en:
  cd /Users/thewizard/Desktop/Panda/solidity-security-auditor/reports
  cat test_report.md  # o abre con cualquier editor

## 📞 Contact

For questions about this educational tool or security research:

- **Project Maintainer**: [Your Name](mailto:your.email@example.com)
- **Security Issues**: Please follow responsible disclosure practices
- **Educational Partnerships**: Contact us for academic collaborations

---

**Remember: Use this tool responsibly and ethically. The goal is to make the blockchain ecosystem more secure for everyone. Happy learning! 🚀**
