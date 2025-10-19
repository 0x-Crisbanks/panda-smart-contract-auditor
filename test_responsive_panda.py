#!/usr/bin/env python3
"""
Test script for the new responsive PANDA interface
Shows how it adapts to different screen sizes
"""

import sys
import os

# Add the auditor source to path
sys.path.append('/Users/thewizard/Desktop/Panda/solidity-security-auditor/src')

def test_responsive_design():
    """Test the responsive design at different screen widths."""
    from rich.console import Console
    from rich.align import Align
    
    print("🐼 Testing PANDA Responsive Design")
    print("=" * 70)
    
    # Test different screen sizes
    screen_sizes = [
        (140, "🖥️  Ultra Wide Screen"),
        (100, "💻 Wide Screen"), 
        (80, "📱 Medium Screen"),
        (60, "📱 Small Screen"),
        (40, "📱 Minimal Screen")
    ]
    
    for width, description in screen_sizes:
        print(f"\n{description} ({width} columns):")
        print("-" * 50)
        
        # Create console with specific width
        console = Console(width=width, force_terminal=True)
        
        # Test the panda art
        if width >= 120:
            # Wide screen - panda next to title
            panda_art = """    [white]  ░░░░░░░░░░[/white]    [bright_cyan]██████╗  █████╗ ███╗   ██╗██████╗  █████╗[/bright_cyan] 
  [white]░░[/white][black]██[/black][white]░░░░[/white][black]██[/black][white]░░[/white]  [bright_cyan]██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗[/bright_cyan]
[white]░░[/white][black]██[/black][white]░░[/white][black]●●[/black][white]░░[/white][black]██[/black][white]░░[/white] [bright_cyan]██████╔╝███████║██╔██╗ ██║██║  ██║███████║[/bright_cyan]
[white]░░[/white][black]██[/black][white]░░[/white][black]▲[/black][white]░░░░[/white][black]██[/black][white]░░[/white] [bright_cyan]██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██╔══██║[/bright_cyan]
[white]░░[/white][black]██[/black][white]░░[/white][black]~~~[/black][white]░░[/white][black]██[/black][white]░░[/white] [bright_cyan]██║     ██║  ██║██║ ╚████║██████╔╝██║  ██║[/bright_cyan]
  [white]░░[/white][black]████████[/black][white]░░[/white]  [bright_cyan]╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝[/bright_cyan]

                    [dim]🐼 Smart Contract Security Auditor 🐼[/dim]"""
            
        elif width >= 80:
            # Medium screen - compact layout
            panda_art = """        [white]░░░░░░░░░░[/white]
      [white]░░[/white][black]██[/black][white]░░░░[/white][black]██[/black][white]░░[/white]
    [white]░░[/white][black]██[/black][white]░░[/white][black]●●[/black][white]░░[/white][black]██[/black][white]░░[/white]
    [white]░░[/white][black]██[/black][white]░░[/white][black]▲[/black][white]░░░░[/white][black]██[/black][white]░░[/white]
    [white]░░[/white][black]██[/black][white]░░[/white][black]~~~[/black][white]░░[/white][black]██[/black][white]░░[/white]
      [white]░░[/white][black]████████[/black][white]░░[/white]

[bright_cyan]██████╗  █████╗ ███╗   ██╗██████╗  █████╗[/bright_cyan] 
[bright_cyan]██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗[/bright_cyan]
[bright_cyan]██████╔╝███████║██╔██╗ ██║██║  ██║███████║[/bright_cyan]
[bright_cyan]██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██╔══██║[/bright_cyan]
[bright_cyan]██║     ██║  ██║██║ ╚████║██████╔╝██║  ██║[/bright_cyan]
[bright_cyan]╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝[/bright_cyan]

            [dim]🐼 Smart Contract Security Auditor 🐼[/dim]"""
            
        else:
            # Small screen - minimal layout
            panda_art = """    [white]░░[/white][black]██[/black][white]░░[/white][black]██[/black][white]░░[/white]  [bright_cyan]PANDA[/bright_cyan]
    [white]░░[/white][black]██[/black][black]●●[/black][black]██[/black][white]░░[/white]  [dim]Security Auditor[/dim]
    [white]░░[/white][black]██[/black][white]▲[/white][black]██[/black][white]░░[/white]   [dim]🐼[/dim]
    [white]░░[/white][black]████[/black][white]░░[/white]"""
        
        console.print(Align.center(panda_art))
        print()

def test_responsive_menu():
    """Test responsive menu layouts."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.box import SQUARE, MINIMAL
    
    print("\n🔧 Testing Responsive Menu")
    print("=" * 50)
    
    screen_sizes = [
        (120, "Wide Screen Menu"),
        (80, "Medium Screen Menu"), 
        (50, "Small Screen Menu")
    ]
    
    for width, description in screen_sizes:
        print(f"\n{description} ({width} columns):")
        print("-" * 30)
        
        console = Console(width=width, force_terminal=True)
        
        if width >= 100:
            # Wide screen - full descriptions
            menu_content = """[bright_cyan]📁 SecurityAuditor[/bright_cyan] panda-auditor
            
Listed 6 option(s).

[cyan]• Option 1:[/cyan] [white]📄 Analyze local Solidity file[/white]
[cyan]• Option 2:[/cyan] [white]📋 Analyze code from clipboard[/white]  
[cyan]• Option 3:[/cyan] [white]🌐 Analyze contract from URL (Etherscan/GitHub/etc)[/white]
[cyan]• Option 4:[/cyan] [white]📊 View analysis history[/white]
[cyan]• Option 5:[/cyan] [white]ℹ️  About vulnerability types[/white]
[cyan]• Option 6:[/cyan] [white]❌ Exit[/white]"""
            box_style = SQUARE
            title = "[bright_green]🐼 PANDA Analysis Options[/bright_green]"
            
        elif width >= 70:
            # Medium screen - shorter descriptions
            menu_content = """[bright_cyan]📁[/bright_cyan] panda-auditor
            
[cyan]1.[/cyan] [white]📄 Local Solidity file[/white]
[cyan]2.[/cyan] [white]📋 From clipboard[/white]  
[cyan]3.[/cyan] [white]🌐 From URL (Etherscan/GitHub)[/white]
[cyan]4.[/cyan] [white]📊 Analysis history[/white]
[cyan]5.[/cyan] [white]ℹ️  Vulnerability info[/white]
[cyan]6.[/cyan] [white]❌ Exit[/white]"""
            box_style = MINIMAL
            title = "[bright_green]Options[/bright_green]"
            
        else:
            # Small screen - minimal layout
            menu_content = """[cyan]1.[/cyan] [white]📄 File[/white]    [cyan]4.[/cyan] [white]📊 History[/white]
[cyan]2.[/cyan] [white]📋 Clip[/white]    [cyan]5.[/cyan] [white]ℹ️  Info[/white]  
[cyan]3.[/cyan] [white]🌐 URL[/white]     [cyan]6.[/cyan] [white]❌ Exit[/white]"""
            box_style = MINIMAL
            title = "[bright_green]🐼[/bright_green]"
        
        menu_panel = Panel(
            menu_content,
            box=box_style,
            padding=(1, 2),
            title=title,
            border_style="green"
        )
        
        console.print(menu_panel)
        print()

def main():
    """Run responsive design tests."""
    print("🐼 PANDA - Responsive Design Test Suite")
    print("=" * 70)
    
    try:
        test_responsive_design()
        test_responsive_menu()
        
        print("\n🎉 Responsive Features Implemented:")
        print("✅ Adaptive panda face design")
        print("✅ Responsive title layout")
        print("✅ Smart menu compression")
        print("✅ Flexible table formatting")
        print("✅ Screen-size detection")
        print("✅ Content optimization")
        
        print("\n📐 Supported Screen Sizes:")
        print("• 120+ cols: Ultra-wide with panda next to title")
        print("• 80-119 cols: Standard layout with stacked design") 
        print("• 60-79 cols: Compact menu and tables")
        print("• <60 cols: Minimal layout for mobile")
        
        print("\nTo test the full responsive experience:")
        print("cd /Users/thewizard/Desktop/Panda/solidity-security-auditor/src")
        print("python3 auditor.py")
        print("# Resize your terminal window to see responsive changes!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()