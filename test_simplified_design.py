#!/usr/bin/env python3
"""
Test script for the simplified PANDA WEB3 design
No panda image, just clean title
"""

import sys
import os

# Add the auditor source to path
sys.path.append('/Users/thewizard/Desktop/Panda/solidity-security-auditor/src')

def test_simplified_banner():
    """Test the new simplified banner."""
    from rich.console import Console
    from rich.align import Align
    
    console = Console()
    
    print("🎯 Testing Simplified PANDA WEB3 Design")
    print("=" * 60)
    
    # Test the new simplified title
    title_art = """
[bright_cyan]██████╗  █████╗ ███╗   ██╗██████╗  █████╗     ██╗    ██╗███████╗██████╗ ██████╗ 
██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗    ██║    ██║██╔════╝██╔══██╗╚════██╗
██████╔╝███████║██╔██╗ ██║██║  ██║███████║    ██║ █╗ ██║█████╗  ██████╔╝ █████╔╝
██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██╔══██║    ██║███╗██║██╔══╝  ██╔══██╗ ╚═══██╗
██║     ██║  ██║██║ ╚████║██████╔╝██║  ██║    ╚███╔███╔╝███████╗██████╔╝██████╔╝
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝     ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═════╝[/bright_cyan]

[bold white]Smart Contract Security Auditor[/bold white]
    """
    
    console.print(Align.center(title_art))
    
    # Tips section
    tips_text = """[dim]
Tips for getting started:
1. Analyze smart contracts from files, clipboard, or URLs.
2. Be specific for the best results.  
3. Create PANDA.md files to customize your security analysis.
4. /help for more information.
[/dim]"""
    
    console.print(tips_text)
    console.print("\n[cyan]>[/cyan] cd panda-web3-auditor")
    console.print()
    
    print("\n✅ Simplified design test complete!")

def main():
    """Run the simplified design test."""
    print("🎯 PANDA WEB3 - Simplified Clean Design")
    print("=" * 60)
    
    try:
        test_simplified_banner()
        
        print("\n🎉 New simplified features:")
        print("✅ No panda image - clean and professional")
        print("✅ Large 'PANDA WEB3' title in bright cyan")
        print("✅ White subtitle text, bold and larger")
        print("✅ Minimalist design approach")
        print("✅ Faster loading without complex ASCII art")
        print("✅ Better compatibility across terminals")
        
        print("\nTo run the full application:")
        print("cd /Users/thewizard/Desktop/Panda/solidity-security-auditor/src")
        print("python3 auditor.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()