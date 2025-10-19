"""
API Configuration for Blockchain Explorers

This module handles API keys and configuration for various blockchain explorers.
For production use, configure your own API keys to avoid rate limits.

EDUCATIONAL PURPOSE: This tool helps with authorized security analysis.
"""

import os
from typing import Dict, Optional


class APIConfig:
    """Configuration manager for blockchain explorer APIs."""
    
    def __init__(self):
        # Default free API keys (rate limited)
        self.api_keys = {
            'etherscan': os.getenv('ETHERSCAN_API_KEY', 'YourApiKeyToken'),
            'bscscan': os.getenv('BSCSCAN_API_KEY', 'YourApiKeyToken'),
            'polygonscan': os.getenv('POLYGONSCAN_API_KEY', 'YourApiKeyToken'),
            'snowtrace': os.getenv('SNOWTRACE_API_KEY', 'YourApiKeyToken'),
        }
        
        # API endpoints
        self.endpoints = {
            'etherscan': 'https://api.etherscan.io/api',
            'bscscan': 'https://api.bscscan.com/api',
            'polygonscan': 'https://api.etherscan.io/v2/api',  # Updated to V2 API
            'snowtrace': 'https://api.snowtrace.io/api',
        }
        
        # Chain IDs for V2 API
        self.chain_ids = {
            'etherscan': None,  # No chain ID needed for mainnet
            'bscscan': None,    # BSC still uses V1
            'polygonscan': '137',  # Polygon chain ID for V2
            'snowtrace': None,     # Avalanche still uses V1
        }
        
        # Rate limits (requests per second)
        self.rate_limits = {
            'etherscan': 0.2,  # 5 req/sec with free key
            'bscscan': 0.2,
            'polygonscan': 0.2,
            'snowtrace': 0.2,
        }
    
    def get_api_key(self, service: str) -> str:
        """Get API key for a service."""
        return self.api_keys.get(service, 'YourApiKeyToken')
    
    def get_endpoint(self, service: str) -> Optional[str]:
        """Get API endpoint for a service."""
        return self.endpoints.get(service)
    
    def get_rate_limit(self, service: str) -> float:
        """Get rate limit for a service."""
        return self.rate_limits.get(service, 0.2)
    
    def get_chain_id(self, service: str) -> Optional[str]:
        """Get chain ID for V2 API services."""
        return self.chain_ids.get(service)
    
    def has_valid_key(self, service: str) -> bool:
        """Check if service has a valid API key configured."""
        key = self.get_api_key(service)
        return key != 'YourApiKeyToken' and len(key) > 10
    
    def get_setup_instructions(self) -> str:
        """Get instructions for setting up API keys."""
        return """
🔑 API Key Setup Instructions:

To avoid rate limits and access more contracts, set up your own API keys:

1. 🌐 Etherscan (ethereum):
   • Visit: https://etherscan.io/apis
   • Create account and get free API key
   • Export: export ETHERSCAN_API_KEY="your_key_here"

2. 🟡 BSCScan (binance smart chain):
   • Visit: https://bscscan.com/apis
   • Create account and get free API key
   • Export: export BSCSCAN_API_KEY="your_key_here"

3. 🟪 PolygonScan (polygon):
   • Visit: https://polygonscan.com/apis
   • Create account and get free API key
   • Export: export POLYGONSCAN_API_KEY="your_key_here"

4. 🔵 SnowTrace (avalanche):
   • Visit: https://snowtrace.io/apis
   • Create account and get free API key
   • Export: export SNOWTRACE_API_KEY="your_key_here"

Then restart PANDA WEB3 to use your keys.

💡 Benefits of API Keys:
   • Higher rate limits (5+ requests/second)
   • Access to more contract data
   • Better reliability
   • Premium features access
        """


# Global configuration instance
api_config = APIConfig()


def check_api_setup() -> Dict[str, bool]:
    """Check which APIs have valid keys configured."""
    services = ['etherscan', 'bscscan', 'polygonscan', 'snowtrace']
    return {service: api_config.has_valid_key(service) for service in services}