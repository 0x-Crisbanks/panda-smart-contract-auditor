"""
Verified Contract Examples

This module provides examples of verified contracts across different blockchains
that can be used for testing PANDA WEB3 analysis functionality.

EDUCATIONAL PURPOSE: These contracts are public and verified for educational analysis.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class VerifiedContract:
    """Information about a verified contract for testing."""
    address: str
    name: str
    blockchain: str
    description: str
    explorer_url: str
    is_popular: bool = False


class VerifiedContractDatabase:
    """Database of verified contracts for testing purposes."""
    
    def __init__(self):
        self.contracts = self._load_verified_contracts()
    
    def _load_verified_contracts(self) -> List[VerifiedContract]:
        """Load database of verified contracts."""
        return [
            # Ethereum Popular Contracts
            VerifiedContract(
                address="0xA0b86a33E6441F8C23b5C0B9F2E3D6c96C5F6E98",
                name="USDC Token",
                blockchain="Ethereum",
                description="USD Coin - popular stablecoin",
                explorer_url="https://etherscan.io/address/0xA0b86a33E6441F8C23b5C0B9F2E3D6c96C5F6E98",
                is_popular=True
            ),
            VerifiedContract(
                address="0x6B175474E89094C44Da98b954EedeAC495271d0F",
                name="DAI Token",
                blockchain="Ethereum",
                description="Dai Stablecoin - decentralized stablecoin",
                explorer_url="https://etherscan.io/address/0x6B175474E89094C44Da98b954EedeAC495271d0F",
                is_popular=True
            ),
            VerifiedContract(
                address="0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
                name="Uniswap Token",
                blockchain="Ethereum", 
                description="UNI - Uniswap governance token",
                explorer_url="https://etherscan.io/address/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
                is_popular=True
            ),
            VerifiedContract(
                address="0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",
                name="Matic Token",
                blockchain="Ethereum",
                description="MATIC - Polygon's native token",
                explorer_url="https://etherscan.io/address/0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",
                is_popular=True
            ),
            
            # BSC Popular Contracts
            VerifiedContract(
                address="0x55d398326f99059fF775485246999027B3197955",
                name="USDT BSC",
                blockchain="BSC",
                description="Tether USD on Binance Smart Chain",
                explorer_url="https://bscscan.com/address/0x55d398326f99059fF775485246999027B3197955",
                is_popular=True
            ),
            VerifiedContract(
                address="0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
                name="BUSD",
                blockchain="BSC",
                description="Binance USD - BSC stablecoin",
                explorer_url="https://bscscan.com/address/0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
                is_popular=True
            ),
            VerifiedContract(
                address="0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
                name="PancakeSwap Token",
                blockchain="BSC",
                description="CAKE - PancakeSwap governance token",
                explorer_url="https://bscscan.com/address/0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
                is_popular=True
            ),
            
            # Polygon Popular Contracts
            VerifiedContract(
                address="0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
                name="WETH Polygon",
                blockchain="Polygon",
                description="Wrapped Ethereum on Polygon",
                explorer_url="https://polygonscan.com/address/0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
                is_popular=True
            ),
            VerifiedContract(
                address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
                name="USDC Polygon",
                blockchain="Polygon",
                description="USD Coin on Polygon network",
                explorer_url="https://polygonscan.com/address/0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
                is_popular=True
            ),
            
            # Additional Examples for Testing
            VerifiedContract(
                address="0x514910771AF9Ca656af840dff83E8264EcF986CA",
                name="Chainlink Token",
                blockchain="Ethereum",
                description="LINK - Chainlink oracle token",
                explorer_url="https://etherscan.io/address/0x514910771AF9Ca656af840dff83E8264EcF986CA",
                is_popular=False
            ),
            VerifiedContract(
                address="0xBB0E17EF65F82Ab018d8EDd776e8DD940327B28b",
                name="Axie Infinity",
                blockchain="Ethereum",
                description="AXS - Axie Infinity governance token",
                explorer_url="https://etherscan.io/address/0xBB0E17EF65F82Ab018d8EDd776e8DD940327B28b",
                is_popular=False
            )
        ]
    
    def get_popular_contracts(self) -> List[VerifiedContract]:
        """Get list of popular verified contracts for testing."""
        return [c for c in self.contracts if c.is_popular]
    
    def get_contracts_by_blockchain(self, blockchain: str) -> List[VerifiedContract]:
        """Get contracts for a specific blockchain."""
        return [c for c in self.contracts if c.blockchain.lower() == blockchain.lower()]
    
    def get_random_contract(self, blockchain: str = None) -> VerifiedContract:
        """Get a random verified contract for testing."""
        import random
        
        if blockchain:
            candidates = self.get_contracts_by_blockchain(blockchain)
        else:
            candidates = self.contracts
        
        if not candidates:
            # Fallback to popular Ethereum contract
            return self.contracts[0]
        
        return random.choice(candidates)
    
    def get_examples_text(self) -> str:
        """Get formatted text with contract examples."""
        popular = self.get_popular_contracts()
        
        text = "🔍 VERIFIED CONTRACT EXAMPLES FOR TESTING:\n"
        text += "=" * 60 + "\n\n"
        
        blockchains = {}
        for contract in popular:
            if contract.blockchain not in blockchains:
                blockchains[contract.blockchain] = []
            blockchains[contract.blockchain].append(contract)
        
        for blockchain, contracts in blockchains.items():
            text += f"🌐 {blockchain}:\n"
            for contract in contracts:
                text += f"   📍 {contract.address}\n"
                text += f"   📝 {contract.name} - {contract.description}\n"
                text += f"   🔗 {contract.explorer_url}\n\n"
        
        text += "💡 Tips:\n"
        text += "   • Copy any address above to test PANDA WEB3\n"
        text += "   • These contracts are verified and publicly available\n"
        text += "   • Use Option 3 in PANDA WEB3 menu to analyze\n"
        
        return text


# Global instance
verified_db = VerifiedContractDatabase()


def get_example_contracts() -> str:
    """Get example contracts for user reference."""
    return verified_db.get_examples_text()


def suggest_contract(blockchain: str = "Ethereum") -> VerifiedContract:
    """Suggest a verified contract for testing."""
    return verified_db.get_random_contract(blockchain)