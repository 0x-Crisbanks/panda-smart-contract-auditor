"""
Contract Source Code Fetcher

This module fetches smart contract source code directly from blockchain explorers
using contract addresses. Supports multiple blockchains with their respective APIs.

EDUCATIONAL PURPOSE: This tool helps analyze deployed contracts for security research.
Use only for authorized security assessments and educational purposes.
"""

import requests
import json
import time
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
from enum import Enum
import re
from api_config import api_config


class BlockchainNetwork(Enum):
    """Supported blockchain networks for contract fetching."""
    ETHEREUM_MAINNET = "ethereum"
    BSC_MAINNET = "bsc" 
    POLYGON_MAINNET = "polygon"
    AVALANCHE_MAINNET = "avalanche"
    SOLANA_MAINNET = "solana"


@dataclass
class ContractInfo:
    """Information about a fetched contract."""
    address: str
    source_code: str
    contract_name: str
    compiler_version: str
    blockchain: BlockchainNetwork
    is_verified: bool
    explorer_url: str
    abi: Optional[str] = None
    constructor_args: Optional[str] = None


class ContractSourceFetcher:
    """Fetches contract source code from various blockchain explorers."""
    
    def __init__(self):
        # Use API configuration
        self.api_config = api_config
        
        # API endpoints for different networks (from config)
        self.api_endpoints = {
            BlockchainNetwork.ETHEREUM_MAINNET: self.api_config.get_endpoint('etherscan'),
            BlockchainNetwork.BSC_MAINNET: self.api_config.get_endpoint('bscscan'),
            BlockchainNetwork.POLYGON_MAINNET: self.api_config.get_endpoint('polygonscan'),
            BlockchainNetwork.AVALANCHE_MAINNET: self.api_config.get_endpoint('snowtrace')
        }
        
        # Service names for API keys
        self.service_names = {
            BlockchainNetwork.ETHEREUM_MAINNET: 'etherscan',
            BlockchainNetwork.BSC_MAINNET: 'bscscan',
            BlockchainNetwork.POLYGON_MAINNET: 'polygonscan',
            BlockchainNetwork.AVALANCHE_MAINNET: 'snowtrace'
        }
        
        # Explorer URLs for reference
        self.explorer_urls = {
            BlockchainNetwork.ETHEREUM_MAINNET: "https://etherscan.io/address/",
            BlockchainNetwork.BSC_MAINNET: "https://bscscan.com/address/",
            BlockchainNetwork.POLYGON_MAINNET: "https://polygonscan.com/address/",
            BlockchainNetwork.AVALANCHE_MAINNET: "https://snowtrace.io/address/",
            BlockchainNetwork.SOLANA_MAINNET: "https://explorer.solana.com/address/"
        }
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 200ms between requests
    
    def _rate_limit(self):
        """Implement rate limiting to respect API limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def _detect_network_from_address(self, address: str, url_hint: str = "") -> BlockchainNetwork:
        """Detect blockchain network from address format and URL hints."""
        
        # Check URL hints first
        url_lower = url_hint.lower()
        if 'bscscan' in url_lower or 'bsc' in url_lower:
            return BlockchainNetwork.BSC_MAINNET
        elif 'polygonscan' in url_lower or 'polygon' in url_lower:
            return BlockchainNetwork.POLYGON_MAINNET  
        elif 'snowtrace' in url_lower or 'avalanche' in url_lower:
            return BlockchainNetwork.AVALANCHE_MAINNET
        elif 'solana' in url_lower:
            return BlockchainNetwork.SOLANA_MAINNET
        
        # Solana addresses are base58 and typically 32-44 characters
        if len(address) >= 32 and len(address) <= 44 and not address.startswith('0x'):
            # Basic check for base58 characters
            if re.match(r'^[1-9A-HJ-NP-Za-km-z]+$', address):
                return BlockchainNetwork.SOLANA_MAINNET
        
        # EVM addresses start with 0x and are 42 characters
        if address.startswith('0x') and len(address) == 42:
            # Default to Ethereum if no other indicators
            return BlockchainNetwork.ETHEREUM_MAINNET
        
        # Fallback to Ethereum
        return BlockchainNetwork.ETHEREUM_MAINNET
    
    def fetch_contract_source(self, address: str, url_hint: str = "") -> Optional[ContractInfo]:
        """
        Fetch contract source code from blockchain explorer.
        
        Args:
            address: Contract address
            url_hint: Optional URL hint to help detect the blockchain
            
        Returns:
            ContractInfo object if successful, None otherwise
        """
        
        # Detect blockchain network
        network = self._detect_network_from_address(address, url_hint)
        
        if network == BlockchainNetwork.SOLANA_MAINNET:
            return self._fetch_solana_contract(address)
        else:
            return self._fetch_evm_contract(address, network)
    
    def _fetch_evm_contract(self, address: str, network: BlockchainNetwork) -> Optional[ContractInfo]:
        """Fetch contract source from EVM-compatible networks (Ethereum, BSC, Polygon, etc)."""
        
        api_url = self.api_endpoints.get(network)
        service_name = self.service_names.get(network)
        
        if not api_url or not service_name:
            print(f"❌ API endpoint not configured for {network.value}")
            return None
        
        # Get API key from configuration
        api_key = self.api_config.get_api_key(service_name)
        has_valid_key = self.api_config.has_valid_key(service_name)
        
        if not has_valid_key:
            print(f"⚠️  Using free API key for {network.value} - rate limited")
            print(f"💡 Configure your own API key for better performance")
        
        self._rate_limit()
        
        try:
            # API parameters for getting contract source
            params = {
                'module': 'contract',
                'action': 'getsourcecode',
                'address': address,
                'apikey': api_key
            }
            
            # Add chain ID for V2 APIs
            chain_id = self.api_config.get_chain_id(service_name)
            if chain_id:
                params['chainid'] = chain_id
            
            print(f"🔍 Fetching contract source from {network.value}...")
            print(f"📍 Address: {address}")
            
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != '1':
                error_msg = data.get('message', 'Unknown error')
                result = data.get('result', '')
                
                # Provide specific error messages
                if ('Invalid API Key' in error_msg or 'Missing/Invalid API Key' in error_msg or 
                    'Invalid API Key' in result or 'Missing/Invalid API Key' in result):
                    if network == BlockchainNetwork.POLYGON_MAINNET:
                        print(f"❌ Polygon API requires valid API key (V2 migration)")
                        print(f"💡 Get a free API key from https://etherscan.io/apis")
                        print(f"🔧 Set environment: export POLYGONSCAN_API_KEY=\"your_key\"")
                        print(f"📋 Polygon now uses Etherscan V2 API with chain ID 137")
                    else:
                        print(f"❌ Invalid API key for {network.value}")
                        print(f"💡 Get a free API key from {self.explorer_urls[network].replace('/address/', '/apis')}")
                elif 'Contract source code not verified' in error_msg or result == 'Contract source code not verified':
                    print(f"❌ Contract source code not verified on {network.value}")
                    print(f"📋 This contract is not open source or hasn't been verified")
                    print(f"🔗 Check: {self.explorer_urls[network]}{address}")
                elif 'rate limit' in error_msg.lower():
                    print(f"❌ Rate limit exceeded for {network.value}")
                    print(f"⏳ Please wait a moment and try again")
                elif 'NOTOK' in data.get('status', ''):
                    print(f"❌ API request failed for {network.value}")
                    print(f"📋 Possible reasons:")
                    print(f"   • Contract not verified on explorer")
                    print(f"   • Invalid contract address")
                    print(f"   • API service temporarily unavailable")
                    print(f"🔗 Verify contract at: {self.explorer_urls[network]}{address}")
                else:
                    print(f"❌ API Error: {error_msg}")
                
                return None
            
            result = data.get('result', [])
            if not result or not result[0]:
                print("❌ Contract not verified or not found")
                return None
            
            contract_data = result[0]
            source_code = contract_data.get('SourceCode', '')
            
            if not source_code:
                print("❌ No source code available (contract not verified)")
                return None
            
            # Handle different source code formats
            if source_code.startswith('{{'):
                # JSON format (multiple files)
                try:
                    # Remove outer braces and parse JSON
                    source_json = json.loads(source_code[1:-1])
                    if 'sources' in source_json:
                        # Combine all source files
                        combined_source = ""
                        for file_path, file_data in source_json['sources'].items():
                            combined_source += f"// File: {file_path}\n"
                            combined_source += file_data.get('content', '') + "\n\n"
                        source_code = combined_source
                except json.JSONDecodeError:
                    # If JSON parsing fails, use as is
                    pass
            
            contract_info = ContractInfo(
                address=address,
                source_code=source_code,
                contract_name=contract_data.get('ContractName', 'Unknown'),
                compiler_version=contract_data.get('CompilerVersion', 'Unknown'),
                blockchain=network,
                is_verified=True,
                explorer_url=self.explorer_urls[network] + address,
                abi=contract_data.get('ABI'),
                constructor_args=contract_data.get('ConstructorArguments')
            )
            
            print(f"✅ Successfully fetched contract: {contract_info.contract_name}")
            print(f"📊 Source code length: {len(source_code)} characters")
            print(f"🔧 Compiler: {contract_info.compiler_version}")
            
            return contract_info
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error fetching contract: {e}")
            return None
    
    def _fetch_solana_contract(self, address: str) -> Optional[ContractInfo]:
        """Fetch Solana program information."""
        
        try:
            print(f"🔍 Analyzing Solana program: {address}")
            
            # For Solana, we'll use the RPC API to get account info
            rpc_url = "https://api.mainnet-beta.solana.com"
            
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getAccountInfo",
                "params": [
                    address,
                    {
                        "encoding": "base64"
                    }
                ]
            }
            
            self._rate_limit()
            response = requests.post(rpc_url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('error'):
                print(f"❌ Solana RPC Error: {data['error']}")
                return None
            
            result = data.get('result')
            if not result or not result.get('value'):
                print("❌ Solana account not found")
                return None
            
            account_info = result['value']
            
            # Check if it's a program account
            owner = account_info.get('owner')
            if owner == 'BPFLoaderUpgradeab1e11111111111111111111111':
                # This is a BPF program
                source_code = "// Solana BPF Program\n// Binary analysis not available - source code verification needed\n// Address: " + address
            else:
                source_code = "// Solana Account\n// Address: " + address + "\n// Owner: " + owner
            
            contract_info = ContractInfo(
                address=address,
                source_code=source_code,
                contract_name="Solana Program",
                compiler_version="Unknown",
                blockchain=BlockchainNetwork.SOLANA_MAINNET,
                is_verified=False,  # Solana programs are not verified in the same way
                explorer_url=self.explorer_urls[BlockchainNetwork.SOLANA_MAINNET] + address
            )
            
            print(f"✅ Solana program found")
            print(f"👤 Owner: {owner}")
            
            return contract_info
            
        except Exception as e:
            print(f"❌ Error fetching Solana program: {e}")
            return None
    
    def get_supported_networks(self) -> Dict[str, str]:
        """Get list of supported networks with their descriptions."""
        return {
            "Ethereum": "Mainnet smart contracts via Etherscan API",
            "BSC": "Binance Smart Chain contracts via BSCScan API", 
            "Polygon": "Polygon PoS contracts via PolygonScan API",
            "Avalanche": "Avalanche C-Chain contracts via SnowTrace API",
            "Solana": "Solana programs via RPC API"
        }
    
    def validate_address(self, address: str, network: BlockchainNetwork) -> bool:
        """Validate if address format is correct for the given network."""
        
        if network == BlockchainNetwork.SOLANA_MAINNET:
            # Solana addresses are base58, 32-44 characters
            return (len(address) >= 32 and len(address) <= 44 and 
                   re.match(r'^[1-9A-HJ-NP-Za-km-z]+$', address) is not None)
        else:
            # EVM addresses are hex, 42 characters starting with 0x
            return (address.startswith('0x') and len(address) == 42 and
                   re.match(r'^0x[a-fA-F0-9]{40}$', address) is not None)


# Example usage and testing functions
def demo_contract_fetching():
    """Demonstrate contract fetching capabilities."""
    
    fetcher = ContractSourceFetcher()
    
    print("🔗 Contract Source Fetcher Demo")
    print("=" * 50)
    
    # Example addresses for different networks
    examples = {
        "Ethereum": "0xA0b86a33E6441F8C23b5C0B9F2E3D6c96C5F6E98",  # Example
        "BSC": "0x55d398326f99059fF775485246999027B3197955",      # USDT on BSC
        "Polygon": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",  # WETH on Polygon
    }
    
    for network, address in examples.items():
        print(f"\n📍 Testing {network} address: {address}")
        try:
            contract_info = fetcher.fetch_contract_source(address)
            if contract_info:
                print(f"✅ Success: {contract_info.contract_name}")
            else:
                print("❌ Failed to fetch contract")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    demo_contract_fetching()