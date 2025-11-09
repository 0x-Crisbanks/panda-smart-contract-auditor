# 🐼 PANDA WEB3 - Smart Contract Security Auditor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Educational Use](https://img.shields.io/badge/Purpose-Educational-green.svg)](#)
[![Multi-Blockchain](https://img.shields.io/badge/Blockchain-Multi--Platform-purple.svg)](#)

```
                            ░░░░░░░░░░░░░░░░░░░░░░░░░░
                        ░░██████░░░░░░░░░░░░██████░░
                      ░░██░░░░░░██░░░░░░░░██░░░░░░██░░
                    ░░██░░░░░░░░░░██░░░░██░░░░░░░░░░██░░
                  ░░██░░░░░░░░░░░░░░████░░░░░░░░░░░░░░██░░
                  ░░██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░
                ░░██░░░░●●░░░░░░░░░░░░░░░░░░░░●●░░░░██░░
                ░░██░░░░░░░░░░░░░░░░▲░░░░░░░░░░░░░░░░██░░
                ░░██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░
                  ░░██░░░░░░░░░░▲▲▲▲▲▲░░░░░░░░░░░░██░░
                    ░░██░░░░░░░░░░░░░░░░░░░░░░░░██░░
                      ░░██████████████████████░░
                          ░░░░░░░░░░░░░░░░░░░░
```

**PANDA WEB3** is an advanced educational tool for smart contract security analysis that supports multiple blockchains. Designed to help developers, security researchers, and students learn about smart contract vulnerabilities.

## ⚠️ IMPORTANT: ETHICAL AND EDUCATIONAL USE

**🚨 EDUCATIONAL AND AUTHORIZED USE ONLY 🚨**

This tool is designed EXCLUSIVELY for:
- ✅ **Educational purposes** - Learn about smart contract security
- ✅ **Authorized security assessments** - Audit contracts you own or have permission to test
- ✅ **Academic research** - Understand blockchain security concepts
- ✅ **Responsible disclosure** - Follow ethical security research practices

**NEVER use this for:**
- ❌ Exploiting vulnerabilities without explicit authorization
- ❌ Attacking or compromising blockchain networks or applications
- ❌ Financial gain through unauthorized exploitation
- ❌ Any malicious activities that could harm users or protocols

## 🌟 Key Features

### 🔍 Comprehensive Multi-Blockchain Analysis
- **Ethereum** (Solidity) - Complete EVM vulnerability analysis
- **Binance Smart Chain** (BSC) - BSC ecosystem-specific detectors
- **Polygon** (MATIC) - Optimized analysis for Polygon network
- **Avalanche** (AVAX) - Support for C-Chain contracts
- **Solana** (Rust/Anchor) - Solana-specific pattern detection

### 🎨 Advanced User Interface
- **Beautiful Terminal**: Rich interface with colors and panda ASCII art
- **Interactive Menus**: Intuitive and easy-to-use navigation
- **Progress Indicators**: Progress bars and spinners during analysis
- **Professional Reports**: Markdown and JSON report generation

### 🔧 Flexible Analysis Methods
1. **Local Files**: Analyze .sol files from your system
2. **Clipboard**: Direct analysis from copied code
3. **URLs**: Support for GitHub, Etherscan, BSCScan, PolygonScan
4. **Contract Addresses**: Direct analysis from blockchain addresses
5. **History**: Track multiple analyses in a session

### 🛡️ Vulnerability Detectors

| Vulnerability Type | Severity | Supported Blockchains |
|-------------------|----------|----------------------|
| **Reentrancy** | Critical | All EVM |
| **Access Control** | High | All |
| **Integer Overflow/Underflow** | High | Pre-Solidity 0.8.0 |
| **Unchecked External Calls** | High | All EVM |
| **tx.origin Authentication** | Medium | All EVM |
| **Weak Randomness** | Medium | All |
| **Deprecated Functions** | Low | Solidity |
| **Delegatecall Dangers** | High | All EVM |
| **Uninitialized Storage** | Medium | Solidity |
| **MEV Vulnerabilities** | High | Ethereum, BSC |

### 📊 Reporting System
- **Markdown Reports**: Professional formatted documents
- **JSON Reports**: Structured data for integration
- **CWE/SWC Classification**: References to security standards
- **Recommendations**: Specific guides to remediate vulnerabilities
- **Code Examples**: Safe replacement code

## 🚀 Installation and Setup

### Prerequisites
- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Install Git](https://git-scm.com/downloads)

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/your-username/panda-web3.git
cd panda-web3

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install main auditor dependencies
cd solidity-security-auditor
pip install -r requirements.txt

# Run the auditor
cd src
python3 auditor.py
```

### Complete Installation with Slither (Optional)

```bash
# Install Slither for advanced analysis
pip install slither-analyzer

# Or using homebrew on macOS
brew install slither
```

## 🎮 System Usage

### Quick Start

```bash
cd solidity-security-auditor/src
python3 auditor.py
```

### Main Menu Options

```
🔒 PANDA WEB3 SECURITY AUDITOR 🔒
🐼 Smart Contract Security Analysis Tool 🐼

⚠️  ETHICAL USE ONLY ⚠️

🔍 Analysis Options
┌────────────────────────────────────────────────┐
│ 1  │ 📄 Analyze clipboard contract              │
│ 2  │ 📁 Analyze local contract file             │
│ 3  │ 🌐 Analyze from Address/URL               │
│ 4  │ 📊 View analysis history                   │
│ 5  │ 🔗 Blockchain information                  │
│ 6  │ ❌ Exit                                    │
└────────────────────────────────────────────────┘
```

### Usage Examples

#### 1. Local File Analysis
```bash
# Option 2: Local file
Path: examples/vulnerable_contract.sol
```

#### 2. URL Analysis
```bash
# Option 3: URL
GitHub: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol
Etherscan: https://etherscan.io/address/0x...
BSCScan: https://bscscan.com/address/0x...
PolygonScan: https://polygonscan.com/address/0x...
```

#### 3. Multi-Blockchain Detection Analysis
The system automatically detects the blockchain based on:
- Explorer URL (etherscan.io → Ethereum, bscscan.com → BSC)
- Specific code patterns
- Contract context

### Quick Test with Example Contract

```bash
# Run direct test
cd solidity-security-auditor/src
python3 test_simple.py

# View generated report
cat ../reports/test_report.md
```

## 📁 Project Structure

```
panda-web3/
├── README.md                          # This file
├── solidity-security-auditor/         # Main analysis engine
│   ├── src/
│   │   ├── auditor.py                 # Main CLI application
│   │   ├── detectors.py               # Vulnerability detection engine
│   │   ├── blockchain_detectors.py    # Blockchain-specific detectors
│   │   ├── contract_fetcher.py        # Contract fetching system
│   │   ├── reporter.py                # Report generation system
│   │   ├── verified_contracts.py      # Verified contracts database
│   │   └── api_config.py             # API configuration
│   ├── examples/
│   │   ├── vulnerable_contract.sol    # Educational vulnerable contract
│   │   └── solana_vulnerable.rs       # Solana vulnerable example
│   ├── reports/                       # Generated reports
│   ├── requirements.txt               # Python dependencies
│   └── README.md                      # Detailed documentation
├── demo_*.py                          # Demo scripts
├── test_*.py                          # Test scripts
└── SOLUCION_FINAL_OPCION1.py         # Final implementation
```

## 🧪 Development and Contributing

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov black flake8

# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Code Standards

```bash
# Format code
black src/

# Lint code
flake8 src/
```

### How to Contribute

1. **Fork** the repository
2. **Create** a branch for your feature (`git checkout -b feature/new-functionality`)
3. **Make** commits following project standards
4. **Add** tests for new functionality
5. **Submit** a pull request

#### Priority Contribution Areas

- 🔍 **New Detectors**: Add detection patterns for new vulnerabilities
- 🌐 **Blockchain Support**: Expand support to more networks (Fantom, Arbitrum, etc.)
- 📊 **UI Improvements**: Enhance terminal user experience
- 🧪 **Tests**: Increase test coverage
- 📚 **Documentation**: Improve guides and tutorials
- 🔧 **Integration**: APIs and webhooks for external tools

### Reporting Bugs

Use [GitHub Issues](https://github.com/your-username/panda-web3/issues) to report:
- 🐛 **Bugs**: Unexpected behaviors
- 💡 **Feature Requests**: New functionalities
- 📚 **Documentation**: Documentation improvements
- 🔒 **Vulnerabilities**: Using responsible disclosure

## 📚 Educational Resources

### Learning Platforms
- **[Ethernaut](https://ethernaut.openzeppelin.com/)** - Interactive hacking challenges
- **[Damn Vulnerable DeFi](https://www.damnvulnerabledefi.xyz/)** - DeFi security scenarios
- **[Capture The Ether](https://capturetheether.com/)** - Ethereum security puzzles

### Documentation and Standards
- **[SWC Registry](https://swcregistry.io/)** - Smart Contract Weakness Registry
- **[CWE](https://cwe.mitre.org/)** - Common Weakness Enumeration Database
- **[OpenZeppelin Security](https://docs.openzeppelin.com/contracts/4.x/security)**
- **[Consensys Best Practices](https://consensys.github.io/smart-contract-best-practices/)**

### Complementary Tools
- **[Slither](https://github.com/crytic/slither)** - Static analysis framework
- **[MythX](https://mythx.io/)** - Security analysis platform
- **[Mythril](https://github.com/ConsenSys/mythril)** - EVM analysis tool
- **[Securify](https://securify.chainsecurity.com/)** - Formal verification

## ⚙️ Advanced Configuration

### Environment Variables

```bash
# Custom reports directory
export PANDA_REPORTS_DIR="/path/to/reports"

# Enable debug logging
export PANDA_DEBUG=true

# Disable Slither integration
export PANDA_DISABLE_SLITHER=true

# Blockchain explorer APIs
export ETHERSCAN_API_KEY="your-api-key"
export BSCSCAN_API_KEY="your-api-key"
export POLYGONSCAN_API_KEY="your-api-key"
```

### Custom Detector Configuration

```python
# In src/detectors.py - Add custom patterns
'my_custom_pattern': {
    'pattern': r'your_regex_pattern',
    'severity': 'Medium',
    'description': 'Vulnerability description',
    'explanation': 'How this could be exploited...',
    'recommendation': 'How to fix this issue...'
}
```

## 🚀 Development Roadmap

### Version 2.0 (Q2 2025)
- [ ] **Complete Solana Support**: Native Solana program analysis
- [ ] **REST API**: Endpoints for external tool integration
- [ ] **Web Dashboard**: Complementary web interface
- [ ] **Batch Analysis**: Multiple contract processing

### Version 2.1 (Q3 2025)
- [ ] **Machine Learning**: Pattern detection using ML
- [ ] **CI/CD Integration**: GitHub Actions, GitLab CI plugins
- [ ] **Advanced Reports**: PDF and interactive visualizations
- [ ] **Database**: Persistent analysis storage

### Version 2.2 (Q4 2025)
- [ ] **Layer 2 Support**: Optimism, Arbitrum, Polygon zkEVM
- [ ] **Cross-chain Analysis**: Multi-chain protocol analysis
- [ ] **Community Features**: Finding sharing and collaboration
- [ ] **Enterprise Tools**: Features for companies and teams

## 📄 License and Responsibility

### MIT License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Legal Disclaimer
- Users are **solely responsible** for ensuring their use of this tool complies with applicable laws
- Developers assume **no responsibility** for misuse of this tool
- Always obtain proper authorization before testing contracts you do not own

### Tool Limitations

**What it DOES:**
- ✅ Detects common vulnerability patterns using static analysis
- ✅ Provides educational explanations and remediation guides
- ✅ Generates professional audit reports
- ✅ Integrates with advanced tools like Slither

**What it does NOT do:**
- ❌ Does not detect all possible vulnerabilities (manual review still required)
- ❌ Does not analyze external contract dependencies
- ❌ Does not test runtime behavior
- ❌ Does not verify economic model security
- ❌ Does not provide exploitation code

## 🤝 Community and Support

### Getting Help
- **GitHub Issues**: [Report bugs or request features](https://github.com/your-username/panda-web3/issues)
- **Discussions**: [Join community discussions](https://github.com/your-username/panda-web3/discussions)
- **Wiki**: [Read complete documentation](https://github.com/your-username/panda-web3/wiki)

### Project Contact
- **Main Maintainer**: [Your Name](mailto:your.email@example.com)
- **Security Reports**: Please follow responsible disclosure practices
- **Educational Collaborations**: Contact us for academic collaborations

## 🙏 Acknowledgments

- **OpenZeppelin** - For security standards and educational resources
- **ConsenSys** - For best practices and security tools
- **Trail of Bits** - For the Slither static analysis framework
- **Ethereum Security Community** - For continuous research and education
- **Damn Vulnerable DeFi** - For inspiration in educational vulnerable contracts

---

**🐼 Remember: Use this tool responsibly and ethically. The goal is to make the blockchain ecosystem safer for everyone. Happy learning! 🚀**