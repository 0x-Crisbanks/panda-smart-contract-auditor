"""
Multi-Blockchain Contract Security Detector

This module provides specialized vulnerability detection for different blockchain platforms:
- Solana (Rust/Anchor)
- Binance Smart Chain (Solidity)
- Polygon (Solidity)
- Ethereum (Solidity)

EDUCATIONAL PURPOSE: This tool helps developers learn about blockchain-specific security issues.
Use only for authorized security assessments and educational purposes.
"""

import re
import logging
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

from detectors import Finding, VulnerabilityDetector


class BlockchainType(Enum):
    """Supported blockchain types."""
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    BSC = "binance_smart_chain"
    POLYGON = "polygon"
    AVALANCHE = "avalanche"
    FANTOM = "fantom"


@dataclass
class BlockchainContext:
    """Context information for blockchain-specific analysis."""
    blockchain: BlockchainType
    language: str  # e.g., "solidity", "rust", "anchor"
    version: Optional[str] = None
    framework: Optional[str] = None


class SolanaDetector:
    """Specialized detector for Solana programs (Rust/Anchor)."""
    
    def __init__(self):
        self.patterns = self._initialize_solana_patterns()
    
    def _initialize_solana_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize Solana-specific vulnerability patterns."""
        return {
            "missing_signer_check": {
                "pattern": r"(?:instruction|ctx)\.accounts\.(?!.*\.is_signer).*\.key(?!\s*==\s*ctx\.accounts\.signer\.key)",
                "severity": "High",
                "description": "Missing signer verification",
                "explanation": "Solana programs must verify that accounts are properly signed",
                "recommendation": "Add is_signer checks for account validation",
                "cwe_id": "CWE-306",
                "type": "Access Control"
            },
            "unchecked_account_ownership": {
                "pattern": r"(?:instruction|ctx)\.accounts\..*\.owner(?!\s*==)",
                "severity": "High", 
                "description": "Unchecked account ownership",
                "explanation": "Account ownership should be verified to prevent unauthorized access",
                "recommendation": "Verify account.owner == expected_program_id",
                "cwe_id": "CWE-284",
                "type": "Access Control"
            },
            "integer_overflow_rust": {
                "pattern": r"(?:checked_add|checked_sub|checked_mul|checked_div)\s*\(",
                "severity": "Medium",
                "description": "Potential integer operation without overflow check",
                "explanation": "Rust requires explicit overflow handling in financial operations",
                "recommendation": "Use checked arithmetic operations",
                "cwe_id": "CWE-190",
                "type": "Integer Overflow"
            },
            "unsafe_deserialization": {
                "pattern": r"(?:try_from_slice_unchecked|from_bytes_unchecked)",
                "severity": "High",
                "description": "Unsafe deserialization",
                "explanation": "Unchecked deserialization can lead to memory corruption",
                "recommendation": "Use safe deserialization methods with proper validation",
                "cwe_id": "CWE-502",
                "type": "Unsafe Deserialization"
            },
            "missing_rent_exemption": {
                "pattern": r"AccountInfo.*new.*rent",
                "severity": "Medium",
                "description": "Potential rent exemption issue",
                "explanation": "Accounts should be rent-exempt to avoid being cleaned up",
                "recommendation": "Ensure accounts have sufficient balance for rent exemption",
                "type": "Resource Management"
            },
            "uninitialized_account": {
                "pattern": r"\.data\.borrow\(\).*is_empty\(\)",
                "severity": "High",
                "description": "Uninitialized account access",
                "explanation": "Accessing uninitialized accounts can lead to undefined behavior",
                "recommendation": "Check account initialization before use",
                "type": "Initialization"
            },
            "missing_bump_validation": {
                "pattern": r"find_program_address.*seeds",
                "severity": "Medium",
                "description": "Potential missing bump seed validation",
                "explanation": "PDA bump seeds should be validated to ensure canonical addresses",
                "recommendation": "Validate bump seed in account derivation",
                "type": "Validation"
            }
        }
    
    def analyze(self, code: str) -> List[Finding]:
        """Analyze Rust/Anchor code for Solana-specific vulnerabilities."""
        findings = []
        lines = code.split('\n')
        
        for pattern_name, pattern_data in self.patterns.items():
            pattern = re.compile(pattern_data["pattern"], re.IGNORECASE | re.MULTILINE)
            
            for line_num, line in enumerate(lines, 1):
                if pattern.search(line):
                    finding = Finding(
                        vulnerability_type=pattern_data["type"],
                        severity=pattern_data["severity"],
                        line_number=line_num,
                        code_snippet=line.strip(),
                        description=pattern_data["description"],
                        explanation=pattern_data["explanation"],
                        recommendation=pattern_data["recommendation"],
                        cwe_id=pattern_data.get("cwe_id"),
                        swc_id=None  # SWC is Solidity-specific
                    )
                    findings.append(finding)
        
        return findings


class MultiBlockchainDetector:
    """Multi-blockchain vulnerability detector that combines platform-specific detectors."""
    
    def __init__(self):
        self.solidity_detector = VulnerabilityDetector()
        self.solana_detector = SolanaDetector()
        self.blockchain_specific_patterns = self._initialize_blockchain_patterns()
    
    def _initialize_blockchain_patterns(self) -> Dict[BlockchainType, Dict[str, Any]]:
        """Initialize blockchain-specific vulnerability patterns."""
        return {
            BlockchainType.BSC: {
                "patterns": {
                    "pancakeswap_rug": {
                        "pattern": r"PancakeSwap.*rugpull|removeLiquidity.*onlyOwner",
                        "severity": "Critical",
                        "description": "Potential rug pull mechanism",
                        "explanation": "Contract may allow owner to remove liquidity unexpectedly",
                        "recommendation": "Implement timelocks and community governance",
                        "type": "Rug Pull"
                    },
                    "bep20_issues": {
                        "pattern": r"function\s+transfer.*returns\s*\(\s*bool\s*\)(?!.*require)",
                        "severity": "Medium", 
                        "description": "BEP-20 transfer without checks",
                        "explanation": "BEP-20 transfers should include proper validation",
                        "recommendation": "Add require statements for transfer validation",
                        "type": "Token Standard"
                    }
                }
            },
            BlockchainType.POLYGON: {
                "patterns": {
                    "matic_bridge_issues": {
                        "pattern": r"(?:deposit|withdraw).*Matic.*(?!.*checkpoint)",
                        "severity": "High",
                        "description": "Potential bridge operation without checkpoint",
                        "explanation": "Polygon bridge operations should include checkpoint validation",
                        "recommendation": "Implement proper checkpoint validation",
                        "type": "Bridge Security"
                    },
                    "gas_optimization": {
                        "pattern": r"for\s*\(.*length.*\+\+\)",
                        "severity": "Low",
                        "description": "Gas inefficient loop",
                        "explanation": "Polygon gas costs can be optimized with better loop patterns",
                        "recommendation": "Cache array length and use unchecked increments",
                        "type": "Gas Optimization"
                    }
                }
            },
            BlockchainType.AVALANCHE: {
                "patterns": {
                    "avalanche_consensus": {
                        "pattern": r"block\.timestamp.*finality",
                        "severity": "Medium",
                        "description": "Avalanche consensus timing issue",
                        "explanation": "Avalanche has different finality guarantees than Ethereum",
                        "recommendation": "Account for Avalanche's consensus mechanism",
                        "type": "Consensus"
                    }
                }
            }
        }
    
    def detect_blockchain_type(self, code: str, url: str = "") -> BlockchainContext:
        """Detect the blockchain type and language from code and context."""
        code_lower = code.lower()
        url_lower = url.lower()
        
        # Check for Solana/Rust indicators
        if any(keyword in code_lower for keyword in ['use anchor', 'program!', 'declare_id', 'solana_program']):
            return BlockchainContext(
                blockchain=BlockchainType.SOLANA,
                language="rust",
                framework="anchor" if "anchor" in code_lower else "native"
            )
        
        # Check URL for blockchain hints
        if any(domain in url_lower for domain in ['bscscan.com', 'bsc']):
            return BlockchainContext(
                blockchain=BlockchainType.BSC,
                language="solidity"
            )
        elif any(domain in url_lower for domain in ['polygonscan.com', 'polygon']):
            return BlockchainContext(
                blockchain=BlockchainType.POLYGON,
                language="solidity"
            )
        elif any(domain in url_lower for domain in ['snowtrace.io', 'avalanche']):
            return BlockchainContext(
                blockchain=BlockchainType.AVALANCHE,
                language="solidity"
            )
        
        # Check for blockchain-specific code patterns
        if any(keyword in code_lower for keyword in ['pancakeswap', 'bep-20', 'bep20']):
            return BlockchainContext(
                blockchain=BlockchainType.BSC,
                language="solidity"
            )
        elif any(keyword in code_lower for keyword in ['matic', 'polygon']):
            return BlockchainContext(
                blockchain=BlockchainType.POLYGON,
                language="solidity"
            )
        
        # Default to Ethereum if Solidity
        if 'pragma solidity' in code_lower:
            return BlockchainContext(
                blockchain=BlockchainType.ETHEREUM,
                language="solidity"
            )
        
        # Default fallback
        return BlockchainContext(
            blockchain=BlockchainType.ETHEREUM,
            language="unknown"
        )
    
    def analyze(self, code: str, url: str = "") -> Tuple[List[Finding], BlockchainContext]:
        """
        Analyze code using appropriate blockchain-specific detectors.
        
        Returns:
            Tuple of (findings, blockchain_context)
        """
        context = self.detect_blockchain_type(code, url)
        findings = []
        
        # Use appropriate detector based on blockchain type
        if context.blockchain == BlockchainType.SOLANA:
            findings.extend(self.solana_detector.analyze(code))
        else:
            # Use Solidity detector for EVM-compatible chains
            findings.extend(self.solidity_detector.analyze(code))
            
            # Add blockchain-specific patterns
            if context.blockchain in self.blockchain_specific_patterns:
                blockchain_findings = self._analyze_blockchain_specific(
                    code, 
                    self.blockchain_specific_patterns[context.blockchain]
                )
                findings.extend(blockchain_findings)
        
        return findings, context
    
    def _analyze_blockchain_specific(self, code: str, patterns: Dict[str, Any]) -> List[Finding]:
        """Analyze code using blockchain-specific patterns."""
        findings = []
        lines = code.split('\n')
        
        for pattern_name, pattern_data in patterns["patterns"].items():
            pattern = re.compile(pattern_data["pattern"], re.IGNORECASE | re.MULTILINE)
            
            for line_num, line in enumerate(lines, 1):
                if pattern.search(line):
                    finding = Finding(
                        vulnerability_type=pattern_data["type"],
                        severity=pattern_data["severity"],
                        line_number=line_num,
                        code_snippet=line.strip(),
                        description=pattern_data["description"],
                        explanation=pattern_data["explanation"],
                        recommendation=pattern_data["recommendation"],
                        cwe_id=pattern_data.get("cwe_id"),
                        swc_id=pattern_data.get("swc_id")
                    )
                    findings.append(finding)
        
        return findings
    
    def get_blockchain_info(self, blockchain: BlockchainType) -> Dict[str, str]:
        """Get information about a specific blockchain."""
        info = {
            BlockchainType.ETHEREUM: {
                "name": "Ethereum",
                "language": "Solidity",
                "explorer": "Etherscan",
                "consensus": "Proof of Stake",
                "description": "Original smart contract platform"
            },
            BlockchainType.SOLANA: {
                "name": "Solana",
                "language": "Rust/Anchor",
                "explorer": "Solana Explorer",
                "consensus": "Proof of History",
                "description": "High-performance blockchain with Rust programs"
            },
            BlockchainType.BSC: {
                "name": "Binance Smart Chain",
                "language": "Solidity",
                "explorer": "BSCScan",
                "consensus": "Proof of Authority",
                "description": "Binance's EVM-compatible blockchain"
            },
            BlockchainType.POLYGON: {
                "name": "Polygon",
                "language": "Solidity", 
                "explorer": "PolygonScan",
                "consensus": "Proof of Stake",
                "description": "Ethereum scaling solution"
            },
            BlockchainType.AVALANCHE: {
                "name": "Avalanche",
                "language": "Solidity",
                "explorer": "SnowTrace",
                "consensus": "Avalanche Consensus",
                "description": "Fast, low-cost blockchain platform"
            }
        }
        
        return info.get(blockchain, {})