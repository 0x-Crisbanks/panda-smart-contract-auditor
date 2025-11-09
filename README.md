# 🐼 PANDA - Smart Contract Security Auditor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Educational Use](https://img.shields.io/badge/Purpose-Educational-green.svg)](#)
[![Multi-Blockchain](https://img.shields.io/badge/Blockchain-Multi--Platform-purple.svg)](#)


**PANDA** es una herramienta educativa avanzada para el análisis de seguridad de contratos inteligentes que soporta múltiples blockchains. Diseñada para ayudar a desarrolladores, investigadores de seguridad y estudiantes a aprender sobre vulnerabilidades en contratos inteligentes.

## ⚠️ IMPORTANTE: USO ÉTICO Y EDUCACIONAL

**🚨 SOLO PARA FINES EDUCATIVOS Y AUTORIZADOS 🚨**

Esta herramienta está diseñada EXCLUSIVAMENTE para:
- ✅ **Propósitos educativos** - Aprender sobre seguridad de contratos inteligentes
- ✅ **Evaluaciones de seguridad autorizadas** - Auditar contratos que posees o tienes permiso para probar
- ✅ **Investigación académica** - Comprender conceptos de seguridad blockchain
- ✅ **Divulgación responsable** - Seguir prácticas éticas de investigación en seguridad

**NUNCA debe usarse para:**
- ❌ Explotar vulnerabilidades sin autorización explícita
- ❌ Atacar o comprometer redes blockchain o aplicaciones
- ❌ Obtener beneficios financieros mediante explotación no autorizada
- ❌ Cualquier actividad maliciosa que pueda dañar usuarios o protocolos

## 🌟 Características Principales

### 🔍 Análisis Integral Multi-Blockchain
- **Ethereum** (Solidity) - Análisis completo de vulnerabilidades EVM
- **Binance Smart Chain** (BSC) - Detectores específicos para el ecosistema BSC
- **Polygon** (MATIC) - Análisis optimizado para la red Polygon
- **Avalanche** (AVAX) - Soporte para contratos en C-Chain
- **Solana** (Rust/Anchor) - Detección de patrones específicos de Solana

### 🎨 Interfaz de Usuario Avanzada
- **Terminal Hermosa**: Interfaz rica con colores y ASCII art del panda
- **Menús Interactivos**: Navegación intuitiva y fácil de usar
- **Indicadores de Progreso**: Barras de progreso y spinners durante análisis
- **Reportes Profesionales**: Generación de reportes en Markdown y JSON

### 🔧 Métodos de Análisis Flexibles
1. **Archivos Locales**: Analiza archivos .sol desde tu sistema
2. **Portapapeles**: Análisis directo desde código copiado
3. **URLs**: Soporte para GitHub, Etherscan, BSCScan, PolygonScan
4. **Direcciones de Contrato**: Análisis directo desde direcciones blockchain
5. **Historial**: Seguimiento de múltiples análisis en una sesión

### 🛡️ Detectores de Vulnerabilidades

| Tipo de Vulnerabilidad | Severidad | Blockchains Soportadas |
|------------------------|-----------|------------------------|
| **Reentrancy** | Crítica | Todas las EVM |
| **Access Control** | Alta | Todas |
| **Integer Overflow/Underflow** | Alta | Pre-Solidity 0.8.0 |
| **Unchecked External Calls** | Alta | Todas las EVM |
| **tx.origin Authentication** | Media | Todas las EVM |
| **Weak Randomness** | Media | Todas |
| **Deprecated Functions** | Baja | Solidity |
| **Delegatecall Dangers** | Alta | Todas las EVM |
| **Uninitialized Storage** | Media | Solidity |
| **MEV Vulnerabilities** | Alta | Ethereum, BSC |

### 📊 Sistema de Reportes
- **Reportes Markdown**: Documentos profesionales con formato
- **Reportes JSON**: Datos estructurados para integración
- **Clasificación CWE/SWC**: Referencias a estándares de seguridad
- **Recomendaciones**: Guías específicas para remediar vulnerabilidades
- **Ejemplos de Código**: Código seguro de reemplazo

## 🚀 Instalación y Configuración

### Prerrequisitos
- **Python 3.9+** - [Descargar Python](https://www.python.org/downloads/)
- **Git** - [Instalar Git](https://git-scm.com/downloads)

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/panda-web3.git
cd panda-web3

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias del auditor principal
cd solidity-security-auditor
pip install -r requirements.txt

# Ejecutar el auditor
cd src
python3 auditor.py
```

### Instalación Completa con Slither (Opcional)

```bash
# Instalar Slither para análisis avanzado
pip install slither-analyzer

# O usando homebrew en macOS
brew install slither
```

## 🎮 Uso del Sistema

### Inicio Rápido

```bash
cd solidity-security-auditor/src
python3 auditor.py
```

### Opciones del Menú Principal

```
🔒 PANDA SECURITY AUDITOR 🔒
🐼 Smart Contract Security Analysis Tool 🐼

⚠️  ETHICAL USE ONLY ⚠️

🔍 Analysis Options
┌────────────────────────────────────────────────┐
│ 1  │ 📄 Analyze local Solidity file            │
│ 2  │ 📋 Analyze code from clipboard             │
│ 3  │ 🌐 Analyze contract from URL              │
│ 4  │ 📊 View analysis history                   │
│ 5  │ ℹ️  About vulnerability types              │
│ 6  │ ❌ Exit                                    │
└────────────────────────────────────────────────┘
```

### Ejemplos de Uso

#### 1. Análisis de Archivo Local
```bash
# Opción 1: Archivo local
Ruta: examples/vulnerable_contract.sol
```

#### 2. Análisis desde URL
```bash
# Opción 3: URL
GitHub: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol
Etherscan: https://etherscan.io/address/0x...
BSCScan: https://bscscan.com/address/0x...
PolygonScan: https://polygonscan.com/address/0x...
```

#### 3. Análisis con Detección Multi-Blockchain
El sistema detecta automáticamente la blockchain basándose en:
- URL del explorador (etherscan.io → Ethereum, bscscan.com → BSC)
- Patrones de código específicos
- Contexto del contrato

### Prueba Rápida con Contrato de Ejemplo

```bash
# Ejecutar prueba directa
cd solidity-security-auditor/src
python3 test_simple.py

# Ver reporte generado
cat ../reports/test_report.md
```

## 📁 Estructura del Proyecto

```
panda-web3/
├── README.md                          # Este archivo
├── solidity-security-auditor/         # Motor principal de análisis
│   ├── src/
│   │   ├── auditor.py                 # Aplicación CLI principal
│   │   ├── detectors.py               # Motor de detección de vulnerabilidades
│   │   ├── blockchain_detectors.py    # Detectores específicos por blockchain
│   │   ├── contract_fetcher.py        # Sistema de obtención de contratos
│   │   ├── reporter.py                # Sistema de generación de reportes
│   │   ├── verified_contracts.py      # Base de datos de contratos verificados
│   │   └── api_config.py             # Configuración de APIs
│   ├── examples/
│   │   ├── vulnerable_contract.sol    # Contrato vulnerable educativo
│   │   └── solana_vulnerable.rs       # Ejemplo vulnerable de Solana
│   ├── reports/                       # Reportes generados
│   ├── requirements.txt               # Dependencias Python
│   └── README.md                      # Documentación detallada
├── demo_*.py                          # Scripts de demostración
├── test_*.py                          # Scripts de prueba
└── SOLUCION_FINAL_OPCION1.py         # Implementación final
```

## 🧪 Desarrollo y Contribución

### Ejecutar Pruebas

```bash
# Instalar dependencias de desarrollo
pip install pytest pytest-cov black flake8

# Ejecutar pruebas unitarias
pytest tests/

# Ejecutar con cobertura
pytest --cov=src tests/
```

### Estándares de Código

```bash
# Formatear código
black src/

# Lint código
flake8 src/
```

### Cómo Contribuir

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Haz** commits siguiendo los estándares del proyecto
4. **Añade** pruebas para nueva funcionalidad
5. **Envía** un pull request

#### Áreas de Contribución Prioritarias

- 🔍 **Nuevos Detectores**: Añadir patrones de detección para nuevas vulnerabilidades
- 🌐 **Soporte de Blockchains**: Expandir soporte a más redes (Fantom, Arbitrum, etc.)
- 📊 **Mejoras de UI**: Mejorar la experiencia de usuario en terminal
- 🧪 **Tests**: Aumentar cobertura de pruebas
- 📚 **Documentación**: Mejorar guías y tutoriales
- 🔧 **Integración**: APIs y webhooks para herramientas externas

### Reportar Bugs

Usa las [GitHub Issues](https://github.com/tu-usuario/panda-web3/issues) para reportar:
- 🐛 **Bugs**: Comportamientos inesperados
- 💡 **Feature Requests**: Nuevas funcionalidades
- 📚 **Documentación**: Mejoras en documentación
- 🔒 **Vulnerabilidades**: Usando divulgación responsable

## 📚 Recursos Educativos

### Plataformas de Aprendizaje
- **[Ethernaut](https://ethernaut.openzeppelin.com/)** - Desafíos interactivos de hacking
- **[Damn Vulnerable DeFi](https://www.damnvulnerabledefi.xyz/)** - Escenarios de seguridad DeFi
- **[Capture The Ether](https://capturetheether.com/)** - Puzzles de seguridad Ethereum

### Documentación y Estándares
- **[SWC Registry](https://swcregistry.io/)** - Registro de Debilidades de Smart Contracts
- **[CWE](https://cwe.mitre.org/)** - Base de datos de Debilidades Comunes
- **[OpenZeppelin Security](https://docs.openzeppelin.com/contracts/4.x/security)**
- **[Consensys Best Practices](https://consensys.github.io/smart-contract-best-practices/)**

### Herramientas Complementarias
- **[Slither](https://github.com/crytic/slither)** - Framework de análisis estático
- **[MythX](https://mythx.io/)** - Plataforma de análisis de seguridad
- **[Mythril](https://github.com/ConsenSys/mythril)** - Herramienta de análisis EVM
- **[Securify](https://securify.chainsecurity.com/)** - Verificación formal

## ⚙️ Configuración Avanzada

### Variables de Entorno

```bash
# Directorio personalizado para reportes
export PANDA_REPORTS_DIR="/path/to/reports"

# Habilitar logging de debug
export PANDA_DEBUG=true

# Deshabilitar integración con Slither
export PANDA_DISABLE_SLITHER=true

# APIs de exploradores blockchain
export ETHERSCAN_API_KEY="tu-api-key"
export BSCSCAN_API_KEY="tu-api-key"
export POLYGONSCAN_API_KEY="tu-api-key"
```

### Configuración de Detectores Personalizados

```python
# En src/detectors.py - Añadir patrones personalizados
'mi_patron_custom': {
    'pattern': r'tu_regex_pattern',
    'severity': 'Medium',
    'description': 'Descripción de la vulnerabilidad',
    'explanation': 'Como podría ser explotado...',
    'recommendation': 'Como arreglar el problema...'
}
```

## 🚀 Roadmap de Desarrollo

### Version 2.0 (Q2 2024)
- [ ] **Soporte Solana Completo**: Análisis nativo de programas Solana
- [ ] **API REST**: Endpoints para integración con herramientas externas
- [ ] **Dashboard Web**: Interfaz web complementaria
- [ ] **Análisis en Batch**: Procesamiento de múltiples contratos

### Version 2.1 (Q3 2024)
- [ ] **Machine Learning**: Detección de patrones usando ML
- [ ] **Integración CI/CD**: Plugins para GitHub Actions, GitLab CI
- [ ] **Reportes Avanzados**: PDF y visualizaciones interactivas
- [ ] **Base de Datos**: Almacenamiento persistente de análisis

### Version 2.2 (Q4 2024)
- [ ] **Soporte Layer 2**: Optimism, Arbitrum, Polygon zkEVM
- [ ] **Cross-chain Analysis**: Análisis de protocolos multi-chain
- [ ] **Community Features**: Sharing y colaboración de hallazgos
- [ ] **Enterprise Tools**: Features para empresas y equipos

## 📄 Licencia y Responsabilidad

### Licencia MIT
Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

### Descargo de Responsabilidad Legal
- Los usuarios son **únicamente responsables** de asegurar que el uso de esta herramienta cumple con las leyes aplicables
- Los desarrolladores **no asumen responsabilidad** por el mal uso de esta herramienta
- Siempre obtén autorización adecuada antes de probar contratos que no posees

### Limitaciones de la Herramienta

**Lo que SÍ hace:**
- ✅ Detecta patrones comunes de vulnerabilidad usando análisis estático
- ✅ Proporciona explicaciones educativas y guías de remediación
- ✅ Genera reportes profesionales de auditoría
- ✅ Se integra con herramientas avanzadas como Slither

**Lo que NO hace:**
- ❌ No detecta todas las vulnerabilidades posibles (revisión manual aún requerida)
- ❌ No analiza dependencias de contratos externos
- ❌ No prueba comportamiento en tiempo de ejecución
- ❌ No verifica seguridad de modelos económicos
- ❌ No proporciona código de explotación

## 🤝 Comunidad y Soporte

### Obtener Ayuda
- **GitHub Issues**: [Reportar bugs o solicitar features](https://github.com/tu-usuario/panda-web3/issues)
- **Discussions**: [Unirse a discusiones de la comunidad](https://github.com/tu-usuario/panda-web3/discussions)
- **Wiki**: [Leer documentación completa](https://github.com/tu-usuario/panda-web3/wiki)

### Contacto del Proyecto
- **Mantenedor Principal**: [Tu Nombre](mailto:tu.email@ejemplo.com)
- **Reportes de Seguridad**: Por favor sigue prácticas de divulgación responsable
- **Colaboraciones Educativas**: Contáctanos para colaboraciones académicas

## 🙏 Agradecimientos

- **OpenZeppelin** - Por estándares de seguridad y recursos educativos
- **ConsenSys** - Por mejores prácticas y herramientas de seguridad
- **Trail of Bits** - Por el framework de análisis estático Slither
- **Ethereum Security Community** - Por investigación continua y educación
- **Damn Vulnerable DeFi** - Por inspiración en contratos vulnerables educativos

---

**🐼 Recuerda: Usa esta herramienta responsable y éticamente. El objetivo es hacer el ecosistema blockchain más seguro para todos. ¡Feliz aprendizaje! 🚀**