"""
Vulnerability Detection Engine for Solidity Smart Contracts

This module implements pattern-based detection of common smart contract vulnerabilities.
It uses both regex patterns and optional Slither integration for comprehensive analysis.

EDUCATIONAL PURPOSE: This tool is designed to help developers learn about smart contract
security by identifying potential vulnerabilities. It should only be used for authorized
security assessments and educational purposes.
"""

import re
import logging
import subprocess
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import tempfile
import os


@dataclass
class Finding:
    """
    Represents a security finding from the analysis.
    
    Attributes:
        vulnerability_type: The type of vulnerability (e.g., "Reentrancy")
        severity: Severity level (Critical, High, Medium, Low, Info)
        line_number: Line number where the issue was found (1-indexed)
        code_snippet: The problematic code snippet
        description: Human-readable description of the issue
        explanation: Educational explanation of how this could be exploited
        recommendation: How to fix the issue
        cwe_id: Common Weakness Enumeration ID if applicable
        swc_id: Smart Contract Weakness Classification ID if applicable
    """
    vulnerability_type: str
    severity: str
    line_number: Optional[int]
    code_snippet: str
    description: str
    explanation: str
    recommendation: str
    cwe_id: Optional[str] = None
    swc_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert finding to dictionary for JSON serialization."""
        return asdict(self)


class VulnerabilityDetector:
    """
    Main vulnerability detection engine.
    
    This class implements both basic regex-based pattern matching and optional
    integration with the Slither static analysis tool for comprehensive
    smart contract security analysis.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.slither_available = self._check_slither_availability()
        
        # Define vulnerability patterns
        self.patterns = self._initialize_patterns()
    
    def _check_slither_availability(self) -> bool:
        """Check if Slither is installed and available."""
        try:
            result = subprocess.run(['slither', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    def _initialize_patterns(self) -> Dict[str, Dict]:
        """
        Initialize regex patterns for vulnerability detection.
        
        Returns:
            Dictionary of vulnerability patterns with their metadata
        """
        return {
            'reentrancy': {
                'pattern': r'(?:\.call(?:\.value)?\s*\(|\.send\s*\(|\.transfer\s*\()(?:[^;]*?)(?:before|prior to)(?:[^;]*?)(?:balance|state)',
                'severity': 'Critical',
                'cwe_id': 'CWE-841',
                'swc_id': 'SWC-107',
                'description': 'Potential reentrancy vulnerability detected',
                'explanation': 'Reentrancy occurs when a contract calls an external contract before updating its internal state. An attacker can exploit this by implementing a fallback function that calls back into the original contract, potentially draining funds or manipulating state.',
                'recommendation': 'Use the Checks-Effects-Interactions pattern: perform all checks first, update state variables second, and interact with external contracts last. Consider using OpenZeppelin\'s ReentrancyGuard modifier.'
            },
            'reentrancy_simple': {
                'pattern': r'(?:\.call\s*\((?:[^)]*)\)\s*;(?:[^}]*?)(?:balance|amount|value)\s*(?:-=|\+=|=))',
                'severity': 'Critical',
                'cwe_id': 'CWE-841',
                'swc_id': 'SWC-107',
                'description': 'External call before state update (potential reentrancy)',
                'explanation': 'Making external calls before updating state variables can lead to reentrancy attacks where the called contract can call back and exploit the unchanged state.',
                'recommendation': 'Update state variables before making external calls. Use the Checks-Effects-Interactions pattern or reentrancy guards.'
            },
            'unchecked_call': {
                'pattern': r'(?:\.call|\.send|\.transfer)\s*\([^)]*\)\s*;(?!\s*(?:require|assert|if))',
                'severity': 'High',
                'cwe_id': 'CWE-252',
                'swc_id': 'SWC-104',
                'description': 'Unchecked external call return value',
                'explanation': 'External calls can fail silently. Not checking return values can lead to unexpected behavior where the contract assumes an operation succeeded when it actually failed.',
                'recommendation': 'Always check return values of external calls using require() statements or conditional logic. Consider using transfer() instead of send() for Ether transfers as it automatically reverts on failure.'
            },
            'access_control': {
                'pattern': r'function\s+\w+\s*\([^)]*\)\s*(?:public|external)(?!\s+(?:view|pure))(?![^{]*(?:onlyOwner|require\s*\(.*msg\.sender|modifier\s+\w+))',
                'severity': 'High',
                'cwe_id': 'CWE-284',
                'swc_id': 'SWC-105',
                'description': 'Public/external function without access control',
                'explanation': 'Functions that modify state or perform sensitive operations should have proper access controls to prevent unauthorized access by malicious actors.',
                'recommendation': 'Add appropriate access control modifiers (e.g., onlyOwner) or require statements to restrict function access to authorized users only.'
            },
            'integer_overflow': {
                'pattern': r'pragma\s+solidity\s+[^;]*[0-6]\.[0-7]\.\d+(?:[^{]*(?:\+\+|--|\+=|-=|\*=|/=))',
                'severity': 'High',
                'cwe_id': 'CWE-190',
                'swc_id': 'SWC-101',
                'description': 'Potential integer overflow in pre-0.8.0 Solidity',
                'explanation': 'Solidity versions before 0.8.0 do not have built-in overflow protection. Arithmetic operations can wrap around, potentially leading to unexpected behavior or vulnerabilities.',
                'recommendation': 'Upgrade to Solidity 0.8.0+ for built-in overflow protection, or use SafeMath library for arithmetic operations in older versions.'
            },
            'tx_origin': {
                'pattern': r'tx\.origin\s*(?:==|!=)',
                'severity': 'Medium',
                'cwe_id': 'CWE-346',
                'swc_id': 'SWC-115',
                'description': 'Use of tx.origin for authorization',
                'explanation': 'Using tx.origin for authorization is vulnerable to phishing attacks where a malicious contract can trick users into executing transactions that appear to come from the original sender.',
                'recommendation': 'Use msg.sender instead of tx.origin for authorization checks. tx.origin should only be used when you specifically need the original transaction sender.'
            },
            'deprecated_functions': {
                'pattern': r'(?:suicide\s*\(|throw\s*;|block\.blockhash|sha3\s*\()',
                'severity': 'Low',
                'cwe_id': None,
                'swc_id': 'SWC-111',
                'description': 'Use of deprecated Solidity functions',
                'explanation': 'These functions are deprecated and may be removed in future Solidity versions, potentially breaking contract functionality.',
                'recommendation': 'Replace deprecated functions: use selfdestruct() instead of suicide(), revert() instead of throw, blockhash() instead of block.blockhash, and keccak256() instead of sha3().'
            },
            'weak_randomness': {
                'pattern': r'(?:block\.timestamp|block\.number|block\.difficulty|blockhash\s*\([^)]*\))(?:[^;]*?)(?:random|rand|seed)',
                'severity': 'Medium',
                'cwe_id': 'CWE-338',
                'swc_id': 'SWC-120',
                'description': 'Weak source of randomness',
                'explanation': 'Using blockchain data for randomness is predictable and can be manipulated by miners or other actors, making it unsuitable for security-critical random number generation.',
                'recommendation': 'Use a commit-reveal scheme, oracle services like Chainlink VRF, or other secure randomness solutions instead of blockchain data for random number generation.'
            },
            'uninitialized_storage': {
                'pattern': r'(?:struct|mapping)(?:[^;]*?)(?:storage)(?:[^;=]*?)(?:;)',
                'severity': 'Medium',
                'cwe_id': 'CWE-909',
                'swc_id': 'SWC-109',
                'description': 'Potential uninitialized storage pointer',
                'explanation': 'Uninitialized storage pointers can point to unexpected storage slots, potentially corrupting contract state or allowing unauthorized access to sensitive data.',
                'recommendation': 'Always explicitly initialize storage pointers or use memory for local variables when appropriate.'
            },
            'delegatecall_danger': {
                'pattern': r'delegatecall\s*\(',
                'severity': 'High',
                'cwe_id': 'CWE-470',
                'swc_id': 'SWC-112',
                'description': 'Use of delegatecall',
                'explanation': 'delegatecall executes code in the context of the calling contract, which can lead to unintended state changes or vulnerabilities if the called contract is malicious or contains bugs.',
                'recommendation': 'Carefully validate the target address and consider using regular call() instead. If delegatecall is necessary, implement strict access controls and code validation.'
            }
        }
    
    def analyze(self, code: str) -> List[Finding]:
        """
        Perform comprehensive security analysis on Solidity code.
        
        Args:
            code: The Solidity source code to analyze
            
        Returns:
            List of security findings
        """
        findings = []
        
        # Run regex-based detection
        regex_findings = self._detect_with_regex(code)
        findings.extend(regex_findings)
        
        # Run Slither if available
        if self.slither_available:
            try:
                slither_findings = self._detect_with_slither(code)
                findings.extend(slither_findings)
            except Exception as e:
                self.logger.warning(f"Slither analysis failed: {e}")
        
        # Remove duplicates and sort by severity
        findings = self._deduplicate_findings(findings)
        findings = self._sort_by_severity(findings)
        
        return findings
    
    def _detect_with_regex(self, code: str) -> List[Finding]:
        """
        Detect vulnerabilities using regex patterns.
        
        Args:
            code: Solidity source code
            
        Returns:
            List of findings from regex analysis
        """
        findings = []
        lines = code.split('\n')
        
        for pattern_name, pattern_data in self.patterns.items():
            pattern = pattern_data['pattern']
            compiled_pattern = re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            
            # Search in full code for complex patterns
            matches = compiled_pattern.finditer(code)
            
            for match in matches:
                # Find line number
                line_number = code[:match.start()].count('\n') + 1
                
                # Extract code snippet
                start_line = max(0, line_number - 2)
                end_line = min(len(lines), line_number + 2)
                snippet_lines = lines[start_line:end_line]
                
                # Highlight the problematic line
                if line_number - 1 < len(lines):
                    snippet_lines[line_number - start_line - 1] = f">>> {snippet_lines[line_number - start_line - 1]}"
                
                code_snippet = '\n'.join(snippet_lines)
                
                finding = Finding(
                    vulnerability_type=pattern_name.replace('_', ' ').title(),
                    severity=pattern_data['severity'],
                    line_number=line_number,
                    code_snippet=code_snippet,
                    description=pattern_data['description'],
                    explanation=pattern_data['explanation'],
                    recommendation=pattern_data['recommendation'],
                    cwe_id=pattern_data.get('cwe_id'),
                    swc_id=pattern_data.get('swc_id')
                )
                
                findings.append(finding)
        
        return findings
    
    def _detect_with_slither(self, code: str) -> List[Finding]:
        """
        Detect vulnerabilities using Slither static analysis tool.
        
        Args:
            code: Solidity source code
            
        Returns:
            List of findings from Slither analysis
        """
        findings = []
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sol', delete=False) as tmp_file:
                tmp_file.write(code)
                tmp_file_path = tmp_file.name
            
            # Run Slither
            result = subprocess.run([
                'slither', tmp_file_path, '--json', '-'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout:
                slither_data = json.loads(result.stdout)
                
                # Parse Slither results
                if 'results' in slither_data:
                    for detector_result in slither_data['results']['detectors']:
                        # Map Slither severity to our severity levels
                        slither_impact = detector_result.get('impact', 'Informational')
                        severity_map = {
                            'High': 'High',
                            'Medium': 'Medium', 
                            'Low': 'Low',
                            'Informational': 'Info'
                        }
                        severity = severity_map.get(slither_impact, 'Info')
                        
                        # Extract location information
                        elements = detector_result.get('elements', [])
                        line_number = None
                        code_snippet = ""
                        
                        if elements:
                            first_element = elements[0]
                            if 'source_mapping' in first_element:
                                lines_info = first_element['source_mapping'].get('lines', [])
                                if lines_info:
                                    line_number = lines_info[0]
                                    
                                    # Extract code snippet around the line
                                    code_lines = code.split('\n')
                                    start_line = max(0, line_number - 2)
                                    end_line = min(len(code_lines), line_number + 2)
                                    snippet_lines = code_lines[start_line:end_line]
                                    code_snippet = '\n'.join(snippet_lines)
                        
                        finding = Finding(
                            vulnerability_type=f"Slither: {detector_result.get('check', 'Unknown')}",
                            severity=severity,
                            line_number=line_number,
                            code_snippet=code_snippet,
                            description=detector_result.get('description', 'Slither detected an issue'),
                            explanation="This issue was detected by Slither static analysis. Review the specific detector documentation for detailed exploitation scenarios.",
                            recommendation="Follow Slither's recommendations and consult smart contract security best practices.",
                            swc_id=None,
                            cwe_id=None
                        )
                        
                        findings.append(finding)
        
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            self.logger.warning(f"Slither analysis error: {e}")
        
        finally:
            # Clean up temporary file
            try:
                if 'tmp_file_path' in locals():
                    os.unlink(tmp_file_path)
            except:
                pass
        
        return findings
    
    def _deduplicate_findings(self, findings: List[Finding]) -> List[Finding]:
        """
        Remove duplicate findings based on vulnerability type and line number.
        
        Args:
            findings: List of findings that may contain duplicates
            
        Returns:
            Deduplicated list of findings
        """
        seen = set()
        deduplicated = []
        
        for finding in findings:
            # Create a key for deduplication
            key = (finding.vulnerability_type, finding.line_number, finding.description[:50])
            
            if key not in seen:
                seen.add(key)
                deduplicated.append(finding)
        
        return deduplicated
    
    def _sort_by_severity(self, findings: List[Finding]) -> List[Finding]:
        """
        Sort findings by severity level.
        
        Args:
            findings: List of findings to sort
            
        Returns:
            Sorted list of findings (Critical -> Info)
        """
        severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3, 'Info': 4}
        
        return sorted(findings, key=lambda x: severity_order.get(x.severity, 4))
    
    def get_detector_info(self) -> Dict[str, Dict]:
        """
        Get information about available detectors.
        
        Returns:
            Dictionary with detector information
        """
        info = {
            'regex_detectors': {
                name: {
                    'severity': data['severity'],
                    'description': data['description'],
                    'cwe_id': data.get('cwe_id'),
                    'swc_id': data.get('swc_id')
                }
                for name, data in self.patterns.items()
            },
            'slither_available': self.slither_available
        }
        
        return info