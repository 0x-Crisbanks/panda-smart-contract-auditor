#!/usr/bin/env python3
"""
Demo script for URL-based contract analysis
Shows how the new URL analysis feature works
"""

print("🌐 DEMO: Análisis de Contratos desde URL")
print("=" * 60)

print("\n📋 Nueva funcionalidad agregada:")
print("✅ Análisis automático de contratos desde URLs")
print("✅ Soporte para múltiples fuentes:")
print("   • GitHub (conversión automática a raw)")
print("   • Etherscan/BSCScan/PolygonScan")
print("   • URLs directas a archivos .sol")

print("\n📦 Instalación de dependencias adicionales:")
print("pip install requests")

print("\n🚀 Cómo usar la nueva funcionalidad:")
print("-" * 40)

demo_steps = """
1. Ejecuta el auditor:
   cd solidity-security-auditor/src
   python3 auditor.py

2. Selecciona la nueva opción 3:
   🌐 Analyze contract from URL (Etherscan/etc)

3. Ingresa una URL, ejemplos:
   
   GitHub (se convierte automáticamente):
   https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol
   
   Raw GitHub (directo):
   https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/master/contracts/token/ERC20/ERC20.sol
   
   Etherscan (limitado sin API key):
   https://etherscan.io/address/0x...#code

4. El auditor:
   • Descarga el código automáticamente
   • Lo analiza en busca de vulnerabilidades
   • Genera un reporte completo
"""

print(demo_steps)

print("\n💡 Características técnicas implementadas:")
print("-" * 40)
features = [
    "• Detección automática del tipo de URL",
    "• Conversión de URLs de GitHub a raw",
    "• Parsing básico de Etherscan (mejorable con API key)",
    "• Validación de contenido Solidity",
    "• Manejo de errores y timeouts",
    "• Integración completa con el flujo existente"
]

for feature in features:
    print(feature)

print("\n📊 Ejemplo de análisis de URL:")
print("-" * 40)

example_output = """
🌐 Fetching contract from: https://github.com/...
📥 Fetching content from: https://raw.githubusercontent.com/...
✅ Successfully fetched Solidity code

🔍 Analyzing: URL: https://github.com/...
Running security analysis... Analysis complete!

📊 Analysis Results
Source: URL: https://github.com/OpenZeppelin/...
Code Hash: a3f4b2c1d5e6f7g8

🚨 Vulnerability Summary
━━━━━━━━━━━━━━━━━━━━━━━
Critical: 0
High:     3
Medium:   1
Low:      2
━━━━━━━━━━━━━━━━━━━━━━━

📄 Generate detailed security report? (y/n)
"""

print(example_output)

print("\n🔧 Archivos modificados:")
print("-" * 40)
files_modified = [
    "• auditor.py - Nueva opción de menú y funciones de fetch",
    "• requirements.txt - Agregada dependencia 'requests'",
    "• README.md - Documentación actualizada"
]

for file in files_modified:
    print(file)

print("\n✅ La funcionalidad está lista para usar!")
print("\n⚠️ Notas importantes:")
print("• Para Etherscan completo, necesitas API key")
print("• Respeta los rate limits de las APIs")
print("• Siempre verifica la fuente del contrato")
print("• Uso educativo y ético únicamente")

print("\n" + "=" * 60)
print("🎉 Nueva funcionalidad agregada con éxito!")