#!/usr/bin/env python3
"""
PANDA WEB3 - Multi-Blockchain Security Auditor

Supports smart contract security analysis for:
- Ethereum (Solidity)
- Solana (Rust/Anchor) 
- Binance Smart Chain (Solidity)
- Polygon (Solidity)
- Avalanche (Solidity)

DISCLAIMER: This tool is designed for EDUCATIONAL PURPOSES ONLY and authorized 
security assessments. It should NOT be used to exploit smart contracts without 
explicit permission. Always follow responsible disclosure practices.

Author: Security Education Project
License: MIT (Educational Use)
"""

import os
import sys
import json
import hashlib
import requests
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse

try:
    import pyperclip
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
except ImportError as e:
    print(f"❌ Missing required dependencies: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

from detectors import VulnerabilityDetector, Finding
from reporter import SecurityReporter
from blockchain_detectors import MultiBlockchainDetector, BlockchainType, BlockchainContext
from contract_fetcher import ContractSourceFetcher, ContractInfo
from verified_contracts import get_example_contracts, suggest_contract
from api_config import api_config


class MultiBlockchainAuditor:
    """
    Main CLI interface for the Multi-Blockchain Security Auditor.
    
    This class provides an interactive menu system for analyzing smart contracts
    across multiple blockchains. Supports Ethereum, Solana, BSC, Polygon, and 
    Avalanche. Designed for educational purposes to help developers learn about 
    blockchain-specific security vulnerabilities.
    """
    
    def __init__(self):
        self.console = Console()
        self.detector = VulnerabilityDetector()  # Legacy Solidity detector
        self.multi_detector = MultiBlockchainDetector()  # New multi-blockchain detector
        self.contract_fetcher = ContractSourceFetcher()  # Contract address fetcher
        self.reporter = SecurityReporter()
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        # Analysis history for session
        self.analysis_history: List[Dict] = []
        
    def display_banner(self) -> None:
        """Display the application banner with ethical disclaimer."""
        from rich.align import Align
        from rich.text import Text
        
        # Panda ASCII Art
        panda_art = """[bright_white]
                            ░░░░░░░░░░░░░░░░░░░░░░░░░░
                        ░░██████░░░░░░░░░░░░██████░░
                      ░░██░░░░░░██░░░░░░░░██░░░░░░██░░
                    ░░██░░░░░░░░░░██░░░░██░░░░░░░░░░██░░
                  ░░██░░░░░░░░░░░░░░████░░░░░░░░░░░░░░██░░
                  ░░██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░
                ░░██░░░░[bold black]●●[/bold black]░░░░░░░░░░░░░░░░░░░░[bold black]●●[/bold black]░░░░██░░
                ░░██░░░░░░░░░░░░░░░░[bold black]▲[/bold black]░░░░░░░░░░░░░░░░██░░
                ░░██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░
                  ░░██░░░░░░░░░░[bold black]▲▲▲▲▲▲[/bold black]░░░░░░░░░░░░██░░
                    ░░██░░░░░░░░░░░░░░░░░░░░░░░░██░░
                      ░░██████████████████████░░
                          ░░░░░░░░░░░░░░░░░░░░[/bright_white]
        """
        
        # PANDA WEB3 ASCII Art Title
        title_text = """[bold yellow]
    ██████╗  █████╗ ███╗   ██╗██████╗  █████╗ 
    ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗
    ██████╔╝███████║██╔██╗ ██║██║  ██║███████║
    ██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██╔══██║
    ██║     ██║  ██║██║ ╚████║██████╔╝██║  ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝
    
    ██╗    ██╗███████╗██████╗ ██████╗ 
    ██║    ██║██╔════╝██╔══██╗╚════██╗
    ██║ █╗ ██║█████╗  ██████╔╝ █████╔╝
    ██║███╗██║██╔══╝  ██╔══██╗ ╚═══██╗
    ╚███╔███╔╝███████╗██████╔╝██████╔╝
     ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═════╝
[/bold yellow]"""
        
        # Display panda art centered
        self.console.print(Align.center(panda_art))
        
        # Display title centered
        self.console.print(Align.center(title_text))
        
        # Centered subtitle
        subtitle = "[bold white]🐼 Smart Contract Security Auditor 🐼[/bold white]"
        self.console.print(Align.center(subtitle))
        self.console.print()
        
        # Ethical disclaimer prominently displayed
        disclaimer = Panel(
            "[bold red]⚠️  ETHICAL USE ONLY ⚠️[/bold red]\n"
            "[dim]Educational and authorized security assessments only.\n"
            "Always follow responsible disclosure practices.[/dim]",
            title="[yellow]Important Notice[/yellow]",
            border_style="yellow"
        )
        self.console.print(disclaimer)
        self.console.print()
        
        # Tips section
        tips_text = """[dim]
Tips for getting started:
1. Analyze smart contracts from multiple blockchains (Ethereum, Solana, BSC, Polygon).
2. Supports Solidity and Rust/Anchor contracts.  
3. Use URLs from GitHub, Etherscan, BSCScan, PolygonScan, Solana Explorer.
4. Create PANDA.md files to customize your security analysis.
[/dim]"""
        
        self.console.print(tips_text)
        
        # Command prompt style
        self.console.print("\n[cyan]>[/cyan] cd panda-web3-auditor")
        self.console.print()
    
    def display_menu(self) -> None:
        """Display the main menu options with responsive design."""
        from rich.box import SQUARE, MINIMAL
        
        console_width = self.console.size.width
        
        self.console.print("[green]• I'm now in the panda-web3-auditor directory.[/green]")
        self.console.print()
        self.console.print("[cyan]>[/cyan] ls")
        self.console.print()
        
        # Responsive menu design
        if console_width >= 100:
            # Wide screen - full descriptions
            menu_content = """[bright_cyan]📁 SecurityAuditor[/bright_cyan] panda-web3-auditor
            
Listed 6 option(s).

[cyan]• Option 1:[/cyan] [white]📄 Analyze contract from clipboard[/white]
[cyan]• Option 2:[/cyan] [white]📁 Analyze local contract file[/white]  
[cyan]• Option 3:[/cyan] [white]🌐 Analyze from Address/URL (Multi-blockchain)[/white]
[cyan]• Option 4:[/cyan] [white]📊 View analysis history[/white]
[cyan]• Option 5:[/cyan] [white]🔗 Blockchain information[/white]
[cyan]• Option 6:[/cyan] [white]❌ Exit[/white]"""
            box_style = SQUARE
            title = "[bright_green]PANDA WEB3 Analysis Options[/bright_green]"
            
        elif console_width >= 70:
            # Medium screen - shorter descriptions
            menu_content = """[bright_cyan]📁[/bright_cyan] panda-web3-auditor
            
[cyan]1.[/cyan] [white]📄 Analyze clipboard contract[/white]
[cyan]2.[/cyan] [white]📁 Local file analysis[/white]  
[cyan]3.[/cyan] [white]🌐 Address/URL analysis[/white]
[cyan]4.[/cyan] [white]📊 Analysis history[/white]
[cyan]5.[/cyan] [white]🔗 Blockchain info[/white]
[cyan]6.[/cyan] [white]❌ Exit[/white]"""
            box_style = MINIMAL
            title = "[bright_green]Options[/bright_green]"
            
        else:
            # Small screen - minimal layout
            menu_content = """[cyan]1.[/cyan] [white]📄 File[/white]    [cyan]4.[/cyan] [white]📊 History[/white]
[cyan]2.[/cyan] [white]📋 Clip[/white]    [cyan]5.[/cyan] [white]🔗 Chains[/white]  
[cyan]3.[/cyan] [white]🌐 Addr[/white]    [cyan]6.[/cyan] [white]❌ Exit[/white]"""
            box_style = MINIMAL
            title = "[bright_green]PANDA WEB3[/bright_green]"
        
        menu_panel = Panel(
            menu_content,
            box=box_style,
            padding=(1, 2),
            title=title,
            border_style="green"
        )
        
        self.console.print(menu_panel)
        
        # Responsive help text
        if console_width >= 70:
            self.console.print("\n[dim]• Choose an option to analyze smart contracts for security vulnerabilities.[/dim]")
        else:
            self.console.print("\n[dim]• Select option (1-6):[/dim]")
        self.console.print()
    
    def get_user_choice(self) -> str:
        """Get and validated user menu choice."""
        self.console.print("[cyan]>[/cyan] [dim]Select option (1-6):[/dim]", end=" ")
        return Prompt.ask(
            "",
            choices=["1", "2", "3", "4", "5", "6"],
            default="1",
            show_choices=False
        )
    
    def analyze_file(self) -> None:
        """Analyze a smart contract - direct clipboard analysis."""
        self.console.print("\n[cyan]📄 Smart Contract Analysis[/cyan]")
        self.console.print("[yellow]💡 This option analyzes code from your clipboard[/yellow]")
        self.console.print("[dim]Make sure you have copied your smart contract code before continuing[/dim]")
        
        self.console.print("\n[cyan]>[/cyan] [dim]Press Enter to analyze clipboard content:[/dim]")
        Prompt.ask("", default="")
        
        try:
            code = pyperclip.paste()
            if not code.strip():
                self.console.print("[red]❌ Clipboard is empty[/red]")
                self.console.print("[yellow]💡 Please copy your smart contract code to clipboard first[/yellow]")
                self.console.print("[dim]Then try selecting Option 1 again[/dim]")
                return
            
            # Basic validation
            if len(code) < 50:
                self.console.print("[yellow]⚠️  Clipboard content seems very short for a smart contract[/yellow]")
                if not Confirm.ask("Continue with analysis anyway?", default=True):
                    return
            
            self.console.print("[green]✅ Analyzing clipboard content...[/green]")
            self.console.print(f"[dim]📊 Code length: {len(code)} characters[/dim]")
            
            # Detect code type
            if 'pragma solidity' in code.lower():
                self.console.print("[dim]🔍 Detected: Solidity smart contract[/dim]")
            elif 'contract' in code or 'function' in code:
                self.console.print("[dim]🔍 Detected: Smart contract code[/dim]")
            else:
                self.console.print("[dim]🔍 Analyzing as smart contract code[/dim]")
            
            self._analyze_code(code, "Clipboard content", "")
            
        except Exception as e:
            self.console.print(f"[red]❌ Error reading clipboard: {e}[/red]")
            self.console.print("[yellow]💡 Try copying your code again and selecting Option 1[/yellow]")
    
    def analyze_clipboard(self) -> None:
        """Analyze local Solidity file."""
        self.console.print("\n[cyan]📁 Local File Analysis[/cyan]")
        self.console.print("[dim]Enter the path to your smart contract file[/dim]")
        
        self.console.print("\n[cyan]>[/cyan] [dim]File path:[/dim]")
        file_path = Prompt.ask("").strip()
        
        if not file_path:
            self.console.print("[red]❌ No file path provided[/red]")
            return
            
        if not os.path.exists(file_path):
            self.console.print(f"[red]❌ File not found: {file_path}[/red]")
            return
        
        if not file_path.endswith('.sol') and not file_path.endswith('.rs'):
            if not Confirm.ask("File doesn't have .sol or .rs extension. Continue anyway?"):
                return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.console.print(f"[green]✅ Analyzing file: {file_path}[/green]")
            self.console.print(f"[dim]📊 Code length: {len(code)} characters[/dim]")
            
            # Detect code type
            if 'pragma solidity' in code.lower():
                self.console.print("[dim]🔍 Detected: Solidity smart contract[/dim]")
            elif 'contract' in code or 'function' in code:
                self.console.print("[dim]🔍 Detected: Smart contract code[/dim]")
            else:
                self.console.print("[dim]🔍 Analyzing as smart contract code[/dim]")
            
            self._analyze_code(code, f"File: {file_path}", "")
            
        except Exception as e:
            self.console.print(f"[red]❌ Error reading file: {e}[/red]")
    
    def analyze_from_url(self) -> None:
        """Analyze smart contract from URL or contract address."""
        self.console.print("\n[cyan]>[/cyan] [dim]Enter contract URL or address:[/dim]")
        self.console.print("[dim]  • URLs: GitHub, Etherscan, BSCScan, PolygonScan[/dim]")
        self.console.print("[dim]  • Addresses: 0x... (EVM) or base58 (Solana)[/dim]")
        input_value = Prompt.ask("")
        
        self.console.print(f"[yellow]🔍 Processing input: {input_value}[/yellow]")
        
        try:
            # Check if input is a contract address or URL
            if self._is_contract_address(input_value):
                # Handle contract address directly
                self._analyze_contract_address(input_value)
            else:
                # Handle as URL (existing functionality)
                self._analyze_contract_url(input_value)
                    
        except Exception as e:
            self.console.print(f"[red]❌ Error analyzing contract: {e}[/red]")
    
    def _is_contract_address(self, input_value: str) -> bool:
        """Check if input looks like a contract address."""
        # EVM address (0x + 40 hex chars)
        if len(input_value) == 42 and input_value.startswith('0x'):
            return True
        # Solana address (base58, 32-44 chars)
        if 32 <= len(input_value) <= 44 and not input_value.startswith('http'):
            import re
            if re.match(r'^[1-9A-HJ-NP-Za-km-z]+$', input_value):
                return True
        return False
    
    def _analyze_contract_address(self, address: str) -> None:
        """Analyze contract directly from its address."""
        self.console.print(f"[yellow]📍 Fetching contract source for address: {address}[/yellow]")
        
        # Fetch contract information
        contract_info = self.contract_fetcher.fetch_contract_source(address)
        
        if not contract_info:
            self.console.print("[red]❌ Could not fetch contract source code[/red]")
            self.console.print("[dim]Note: Contract must be verified on the blockchain explorer[/dim]")
            
            # Show helpful suggestions and allow selection
            selected_address, explorer_url = self._show_contract_suggestions()
            if selected_address and explorer_url:
                # Use the explorer URL as context for blockchain detection
                self.console.print(f"\n[yellow]🔄 Now analyzing selected contract...[/yellow]")
                # Call _analyze_contract_url with the proper URL context
                self._analyze_contract_url(explorer_url)
            return
        
        if not contract_info.source_code:
            self.console.print("[red]❌ Contract source code not available[/red]")
            self.console.print("[dim]This contract may not be verified or source may not be public[/dim]")
            return
        
        # Perform analysis
        source_description = f"{contract_info.contract_name} ({contract_info.blockchain.value.title()})"
        self._analyze_code(contract_info.source_code, source_description, contract_info.explorer_url)
    
    def _analyze_contract_url(self, url: str) -> None:
        """Analyze contract from URL (existing functionality)."""
        try:
            # Determine the source type and fetch accordingly
            parsed_url = urlparse(url.lower())
            domain = parsed_url.netloc
            
            code = None
            source_description = url
            
            if 'etherscan' in domain:
                code, source_description = self._fetch_from_etherscan(url)
            elif 'bscscan' in domain:
                code, source_description = self._fetch_from_bscscan(url)
            elif 'polygonscan' in domain:
                code, source_description = self._fetch_from_polygonscan(url)
            elif 'github' in domain:
                code, source_description = self._fetch_from_github(url)
            elif 'raw.githubusercontent' in domain:
                code, source_description = self._fetch_raw_content(url)
            else:
                # Try to fetch as raw content
                code, source_description = self._fetch_raw_content(url)
            
            if code:
                self._analyze_code(code, source_description, url)
            else:
                self.console.print("[red]❌ Could not fetch contract code from URL[/red]")
                
        except Exception as e:
            self.console.print(f"[red]❌ Error fetching from URL: {e}[/red]")
    
    def _fetch_from_etherscan(self, url: str) -> Tuple[Optional[str], str]:
        """
        Fetch contract source code from Etherscan.
        
        Args:
            url: Etherscan contract URL
            
        Returns:
            Tuple of (source_code, description)
        """
        try:
            # Extract contract address from URL
            # Format: https://etherscan.io/address/0x...#code
            match = re.search(r'address/(0x[a-fA-F0-9]{40})', url)
            if not match:
                self.console.print("[red]❌ Invalid Etherscan URL format[/red]")
                return None, url
            
            contract_address = match.group(1)
            
            # Note: For production, you'd need an Etherscan API key
            # This is a simplified version for educational purposes
            self.console.print(f"[yellow]📥 Fetching contract {contract_address} from Etherscan...[/yellow]")
            
            # Try to fetch the page and extract source code
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Simple extraction - in production, use Etherscan API
                # Look for contract code in the page
                code_match = re.search(r'<pre[^>]*id="editor"[^>]*>(.*?)</pre>', 
                                      response.text, re.DOTALL)
                if code_match:
                    source_code = code_match.group(1)
                    # Clean HTML entities
                    source_code = source_code.replace('&lt;', '<').replace('&gt;', '>')
                    source_code = source_code.replace('&amp;', '&').replace('&quot;', '"')
                    return source_code, f"Etherscan Contract: {contract_address}"
                else:
                    # Try API approach (requires API key in production)
                    self.console.print("[yellow]ℹ️  Note: For better Etherscan integration, use API key[/yellow]")
                    return None, url
            else:
                self.console.print(f"[red]❌ Failed to fetch from Etherscan: HTTP {response.status_code}[/red]")
                return None, url
                
        except Exception as e:
            self.console.print(f"[red]❌ Error fetching from Etherscan: {e}[/red]")
            return None, url
    
    def _fetch_from_bscscan(self, url: str) -> Tuple[Optional[str], str]:
        """Fetch contract from BSCScan."""
        try:
            # Extract contract address from BSCScan URL
            # Format: https://bscscan.com/address/0x...#code
            if '/address/' in url:
                address = url.split('/address/')[1].split('#')[0].split('?')[0]
                
                # Note: BSCScan API requires API key for source code
                # For demo purposes, we'll try to parse the web page
                self.console.print(f"[yellow]📥 Fetching BSC contract: {address}[/yellow]")
                
                # Try to get source code (would need API key in production)
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # This is a simplified approach - in production, use BSCScan API
                    return None, f"BSCScan: {address} (API key required for full support)"
                else:
                    return None, f"Failed to fetch from BSCScan: {url}"
            
            return None, f"Invalid BSCScan URL format: {url}"
            
        except Exception as e:
            return None, f"BSCScan fetch error: {e}"
    
    def _fetch_from_polygonscan(self, url: str) -> Tuple[Optional[str], str]:
        """Fetch contract from PolygonScan."""
        try:
            # Extract contract address from PolygonScan URL
            # Format: https://polygonscan.com/address/0x...#code
            if '/address/' in url:
                address = url.split('/address/')[1].split('#')[0].split('?')[0]
                
                self.console.print(f"[yellow]📥 Fetching Polygon contract: {address}[/yellow]")
                
                # Try to get source code (would need API key in production)
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # This is a simplified approach - in production, use PolygonScan API
                    return None, f"PolygonScan: {address} (API key required for full support)"
                else:
                    return None, f"Failed to fetch from PolygonScan: {url}"
            
            return None, f"Invalid PolygonScan URL format: {url}"
            
        except Exception as e:
            return None, f"PolygonScan fetch error: {e}"
    
    def _fetch_from_github(self, url: str) -> Tuple[Optional[str], str]:
        """
        Fetch Solidity code from GitHub.
        
        Args:
            url: GitHub URL to .sol file
            
        Returns:
            Tuple of (source_code, description)
        """
        try:
            # Convert GitHub URL to raw content URL
            if 'github.com' in url and '/blob/' in url:
                raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
            else:
                raw_url = url
            
            return self._fetch_raw_content(raw_url)
            
        except Exception as e:
            self.console.print(f"[red]❌ Error fetching from GitHub: {e}[/red]")
            return None, url
    
    def _fetch_raw_content(self, url: str) -> Tuple[Optional[str], str]:
        """
        Fetch raw content from any URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            Tuple of (source_code, description)
        """
        try:
            self.console.print(f"[yellow]📥 Fetching content from: {url}[/yellow]")
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text
                
                # Check if it looks like Solidity code
                if 'pragma solidity' in content or 'contract ' in content:
                    return content, f"URL: {url}"
                else:
                    self.console.print("[red]❌ Content doesn't appear to be Solidity code[/red]")
                    return None, url
            else:
                self.console.print(f"[red]❌ Failed to fetch: HTTP {response.status_code}[/red]")
                return None, url
                
        except Exception as e:
            self.console.print(f"[red]❌ Error fetching content: {e}[/red]")
            return None, url
    
    def _analyze_code(self, code: str, source: str, url: str = "") -> None:
        """
        Perform multi-blockchain security analysis on smart contract code.
        
        Args:
            code: The smart contract source code to analyze
            source: Description of the code source (file path, clipboard, etc.)
            url: Optional URL context for blockchain detection
        """
        self.console.print(f"\n[yellow]🔍 Analyzing: {source}[/yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Running security analysis...", total=None)
            
            # Generate code hash for tracking
            code_hash = hashlib.sha256(code.encode()).hexdigest()[:16]
            
            # Perform multi-blockchain analysis
            findings, blockchain_context = self.multi_detector.analyze(code, url)
            
            progress.update(task, description="Analysis complete!")
        
        # Display results with blockchain context
        self._display_analysis_results(findings, source, code_hash, blockchain_context)
        
        # Save to history
        analysis_record = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'code_hash': code_hash,
            'findings_count': len(findings),
            'critical_count': len([f for f in findings if f.severity == 'Critical']),
            'high_count': len([f for f in findings if f.severity == 'High']),
            'findings': [f.to_dict() for f in findings]
        }
        self.analysis_history.append(analysis_record)
        
        # Offer to generate report
        if findings:
            if Confirm.ask("\n📄 Generate detailed security report?", default=True):
                self._generate_report(code, findings, source, code_hash)
    
    def _display_analysis_results(self, findings: List[Finding], source: str, code_hash: str, 
                                 blockchain_context: Optional[BlockchainContext] = None) -> None:
        """Display analysis results with blockchain context in a responsive formatted table."""
        console_width = self.console.size.width
        
        self.console.print(f"\n[bold]📊 Analysis Results[/bold]")
        
        # Display blockchain context if available
        if blockchain_context:
            blockchain_info = self.multi_detector.get_blockchain_info(blockchain_context.blockchain)
            blockchain_name = blockchain_info.get('name', blockchain_context.blockchain.value)
            language = blockchain_context.language.title()
            
            if console_width >= 80:
                self.console.print(f"Blockchain: [cyan]{blockchain_name}[/cyan] | Language: [yellow]{language}[/yellow]")
            else:
                self.console.print(f"[cyan]{blockchain_name}[/cyan] ({language})")
        
        # Responsive source display
        if console_width >= 80:
            self.console.print(f"Source: {source}")
            self.console.print(f"Code Hash: {code_hash}")
        else:
            # Truncate long sources for small screens
            short_source = source[:30] + "..." if len(source) > 33 else source
            self.console.print(f"Source: {short_source}")
            self.console.print(f"Hash: {code_hash[:8]}...")
        self.console.print()
        
        if not findings:
            self.console.print("[green]✅ No security issues detected![/green]")
            return
        
        # Summary statistics
        severity_counts = {}
        for finding in findings:
            severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
        
        severity_colors = {
            'Critical': 'red',
            'High': 'orange_red1',
            'Medium': 'yellow',
            'Low': 'blue',
            'Info': 'cyan'
        }
        
        # Responsive summary display
        if console_width >= 80:
            # Full table for wide screens
            summary_table = Table(title="🚨 Vulnerability Summary", show_header=True)
            summary_table.add_column("Severity", style="bold")
            summary_table.add_column("Count", justify="center")
            
            for severity in ['Critical', 'High', 'Medium', 'Low', 'Info']:
                count = severity_counts.get(severity, 0)
                if count > 0:
                    color = severity_colors.get(severity, 'white')
                    summary_table.add_row(
                        f"[{color}]{severity}[/{color}]",
                        f"[{color}]{count}[/{color}]"
                    )
            
            self.console.print(summary_table)
            
        else:
            # Compact summary for small screens
            self.console.print("[bold]🚨 Summary:[/bold]")
            summary_line = ""
            for severity in ['Critical', 'High', 'Medium', 'Low', 'Info']:
                count = severity_counts.get(severity, 0)
                if count > 0:
                    color = severity_colors.get(severity, 'white')
                    summary_line += f"[{color}]{severity[:4]}: {count}[/{color}] "
            self.console.print(summary_line)
        
        self.console.print()
        
        # Responsive detailed findings
        if console_width >= 100:
            # Full details for wide screens
            findings_table = Table(title="🔍 Detailed Findings", show_header=True)
            findings_table.add_column("Severity", width=10)
            findings_table.add_column("Type", width=20)
            findings_table.add_column("Line", width=6, justify="center")
            findings_table.add_column("Description", width=50)
            
            for finding in sorted(findings, key=lambda x: ['Critical', 'High', 'Medium', 'Low', 'Info'].index(x.severity)):
                color = severity_colors.get(finding.severity, 'white')
                findings_table.add_row(
                    f"[{color}]{finding.severity}[/{color}]",
                    finding.vulnerability_type,
                    str(finding.line_number) if finding.line_number else "N/A",
                    finding.description[:47] + "..." if len(finding.description) > 50 else finding.description
                )
            
            self.console.print(findings_table)
            
        elif console_width >= 70:
            # Medium detail for medium screens  
            findings_table = Table(title="🔍 Findings", show_header=True)
            findings_table.add_column("Sev", width=5)
            findings_table.add_column("Type", width=15)
            findings_table.add_column("Line", width=5, justify="center")
            findings_table.add_column("Description", width=35)
            
            for finding in sorted(findings, key=lambda x: ['Critical', 'High', 'Medium', 'Low', 'Info'].index(x.severity)):
                color = severity_colors.get(finding.severity, 'white')
                findings_table.add_row(
                    f"[{color}]{finding.severity[:4]}[/{color}]",
                    finding.vulnerability_type[:12] + "..." if len(finding.vulnerability_type) > 15 else finding.vulnerability_type,
                    str(finding.line_number) if finding.line_number else "N/A",
                    finding.description[:32] + "..." if len(finding.description) > 35 else finding.description
                )
            
            self.console.print(findings_table)
            
        else:
            # Minimal list for small screens
            self.console.print("[bold]🔍 Issues:[/bold]")
            for i, finding in enumerate(sorted(findings, key=lambda x: ['Critical', 'High', 'Medium', 'Low', 'Info'].index(x.severity))[:5], 1):
                color = severity_colors.get(finding.severity, 'white')
                line_info = f"L{finding.line_number}" if finding.line_number else "N/A"
                self.console.print(f"{i}. [{color}]{finding.severity[:4]}[/{color}] {finding.vulnerability_type[:15]} ({line_info})")
            
            if len(findings) > 5:
                self.console.print(f"... and {len(findings) - 5} more issues")
    
    def _generate_report(self, code: str, findings: List[Finding], source: str, code_hash: str) -> None:
        """Generate and save a detailed security report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"security_report_{code_hash}_{timestamp}.md"
        report_path = self.reports_dir / report_filename
        
        try:
            report_content = self.reporter.generate_report(code, findings, source, code_hash)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.console.print(f"[green]✅ Report saved: {report_path}[/green]")
            
            # Also save as JSON
            json_filename = f"security_report_{code_hash}_{timestamp}.json"
            json_path = self.reports_dir / json_filename
            
            json_data = {
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'source': source,
                    'code_hash': code_hash,
                    'tool_version': '1.0.0'
                },
                'findings': [f.to_dict() for f in findings],
                'summary': {
                    'total_findings': len(findings),
                    'by_severity': {
                        severity: len([f for f in findings if f.severity == severity])
                        for severity in ['Critical', 'High', 'Medium', 'Low', 'Info']
                    }
                }
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            
            self.console.print(f"[green]✅ JSON report saved: {json_path}[/green]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Error generating report: {e}[/red]")
    
    def view_history(self) -> None:
        """Display analysis history for the current session."""
        if not self.analysis_history:
            self.console.print("[yellow]📊 No analysis history available[/yellow]")
            return
        
        history_table = Table(title="📊 Analysis History", show_header=True)
        history_table.add_column("Timestamp", width=20)
        history_table.add_column("Source", width=30)
        history_table.add_column("Hash", width=16)
        history_table.add_column("Total", justify="center", width=8)
        history_table.add_column("Critical", justify="center", width=8)
        history_table.add_column("High", justify="center", width=8)
        
        for record in self.analysis_history:
            timestamp = datetime.fromisoformat(record['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            history_table.add_row(
                timestamp,
                record['source'][:27] + "..." if len(record['source']) > 30 else record['source'],
                record['code_hash'],
                str(record['findings_count']),
                str(record['critical_count']),
                str(record['high_count'])
            )
        
        self.console.print(history_table)
    
    def _show_contract_suggestions(self) -> Optional[str]:
        """Show suggestions for verified contracts to try and allow selection."""
        from rich.panel import Panel
        from rich.prompt import Prompt, Confirm
        
        # Define available contracts with numbers and blockchain hints
        contracts = [
            ("0xA0b86a33E6441F8C23b5C0B9F2E3D6c96C5F6E98", "USDC Token", "Ethereum", "https://etherscan.io/address/0xA0b86a33E6441F8C23b5C0B9F2E3D6c96C5F6E98"),
            ("0x6B175474E89094C44Da98b954EedeAC495271d0F", "DAI Token", "Ethereum", "https://etherscan.io/address/0x6B175474E89094C44Da98b954EedeAC495271d0F"),
            ("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", "Uniswap Token", "Ethereum", "https://etherscan.io/address/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
            ("0x55d398326f99059fF775485246999027B3197955", "USDT BSC", "BSC", "https://bscscan.com/address/0x55d398326f99059fF775485246999027B3197955"),
            ("0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56", "BUSD Token", "BSC", "https://bscscan.com/address/0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"),
            ("0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619", "WETH Polygon", "Polygon", "https://polygonscan.com/address/0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"),
            ("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", "USDC Polygon", "Polygon", "https://polygonscan.com/address/0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"),
        ]
        
        suggestion_text = """[yellow]💡 Try these verified contracts instead:[/yellow]

[cyan]Popular Ethereum Contracts:[/cyan]
• [white]1.[/white] [white]0xA0b86a33E6441F8C23b5C0B9F2E3D6c96C5F6E98[/white] - USDC Token
• [white]2.[/white] [white]0x6B175474E89094C44Da98b954EedeAC495271d0F[/white] - DAI Token  
• [white]3.[/white] [white]0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984[/white] - Uniswap Token

[cyan]BSC Contracts:[/cyan]
• [white]4.[/white] [white]0x55d398326f99059fF775485246999027B3197955[/white] - USDT BSC
• [white]5.[/white] [white]0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56[/white] - BUSD Token

[cyan]Polygon Contracts:[/cyan]
• [white]6.[/white] [white]0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619[/white] - WETH Polygon
• [white]7.[/white] [white]0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174[/white] - USDC Polygon

[dim]💡 These are popular, verified contracts safe for testing[/dim]"""
        
        panel = Panel(
            suggestion_text,
            title="[bold yellow]🔍 Verified Contract Examples[/bold yellow]",
            border_style="yellow"
        )
        self.console.print(panel)
        
        # Also show API setup info if using free keys
        has_valid_api = any(api_config.has_valid_key(service) 
                           for service in ['etherscan', 'bscscan', 'polygonscan'])
        
        if not has_valid_api:
            self.console.print("\n[dim]⚠️  Using free API keys with rate limits[/dim]")
            self.console.print("[dim]💡 For better performance, set up your own API keys[/dim]")
            self.console.print("[dim]📖 Run: python3 -c \"from api_config import api_config; print(api_config.get_setup_instructions())\"[/dim]")
        
        # Ask if user wants to select one of these contracts
        self.console.print()
        if Confirm.ask("[cyan]🎯 Would you like to analyze one of these verified contracts?[/cyan]", default=True):
            
            choice = Prompt.ask(
                "[cyan]📍 Select a contract (1-7) or press Enter to return to menu[/cyan]",
                choices=[str(i) for i in range(1, 8)] + [""],
                default=""
            )
            
            if choice and choice.isdigit():
                contract_index = int(choice) - 1
                if 0 <= contract_index < len(contracts):
                    selected_address, selected_name, selected_blockchain, explorer_url = contracts[contract_index]
                    self.console.print(f"[green]✅ Selected: {selected_name} ({selected_blockchain})[/green]")
                    self.console.print(f"[dim]📍 Address: {selected_address}[/dim]")
                    # Return both address and URL hint for blockchain detection
                    return selected_address, explorer_url
        
        return None, None

    def show_blockchain_info(self) -> None:
        """Display information about supported blockchains and their specific vulnerabilities."""
        info_text = """
🔗 SUPPORTED BLOCKCHAINS:

[bold cyan]Ethereum[/bold cyan] (Solidity)
• Original smart contract platform
• Explorer: Etherscan.io
• Common vulnerabilities: Reentrancy, Access Control, Gas optimization

[bold magenta]Solana[/bold magenta] (Rust/Anchor)  
• High-performance blockchain with Rust programs
• Explorer: Solana Explorer
• Specific checks: Signer validation, Account ownership, PDA security

[bold yellow]Binance Smart Chain[/bold yellow] (Solidity)
• EVM-compatible with BEP-20 tokens
• Explorer: BSCScan.com
• Focus areas: Rug pull prevention, BEP-20 compliance

[bold purple]Polygon[/bold purple] (Solidity)
• Ethereum scaling solution
• Explorer: PolygonScan.com  
• Bridge security and gas optimization

[bold blue]Avalanche[/bold blue] (Solidity)
• Fast, low-cost blockchain
• Explorer: SnowTrace.io
• Consensus-specific timing issues

[dim]Multi-blockchain analysis automatically detects the platform and applies appropriate security checks.[/dim]
        """
        
        panel = Panel(
            info_text,
            title="[bold cyan]Supported Blockchains[/bold cyan]",
            border_style="cyan"
        )
        self.console.print(panel)
    
    def run(self) -> None:
        """Main application loop."""
        self.display_banner()
        
        while True:
            try:
                self.display_menu()
                choice = self.get_user_choice()
                
                if choice == "1":
                    self.analyze_file()
                elif choice == "2":
                    self.analyze_clipboard()
                elif choice == "3":
                    self.analyze_from_url()
                elif choice == "4":
                    self.view_history()
                elif choice == "5":
                    self.show_blockchain_info()
                elif choice == "6":
                    self.console.print("[yellow]👋 Thanks for using PANDA WEB3 Multi-Blockchain Auditor![/yellow]")
                    self.console.print("[dim]Remember: Always practice responsible disclosure![/dim]")
                    break
                
                # Wait for user before continuing
                if choice in ["1", "2", "3", "4", "5"]:
                    self.console.print()
                    self.console.print("[cyan]>[/cyan] [dim]Press Enter to continue...[/dim]", end="")
                    Prompt.ask("", default="")
                    self.console.clear()
                    self.display_banner()
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]❌ Unexpected error: {e}[/red]")


def main():
    """Entry point for the application."""
    try:
        auditor = MultiBlockchainAuditor()
        auditor.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()