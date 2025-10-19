// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

/**
 * @title VulnerableBank - Educational Smart Contract
 * @dev THIS CONTRACT CONTAINS INTENTIONAL VULNERABILITIES FOR EDUCATIONAL PURPOSES
 * 
 * ⚠️  WARNING: This contract is INTENTIONALLY VULNERABLE and should NEVER be deployed
 * to mainnet or used with real funds. It is designed for educational purposes only
 * to demonstrate common smart contract security vulnerabilities.
 * 
 * Educational Purpose: Learn about smart contract security by analyzing these vulnerabilities
 * 
 * Vulnerabilities demonstrated:
 * 1. Reentrancy attack vector
 * 2. Unchecked external call return values
 * 3. Integer overflow/underflow (pre-0.8.0 Solidity)
 * 4. Access control issues
 * 5. Use of tx.origin for authentication
 * 6. Weak randomness source
 * 7. Uninitialized storage pointers
 * 8. Use of deprecated functions
 * 
 * Based on: Damn Vulnerable DeFi style educational contracts
 * 
 * ETHICAL DISCLAIMER: This code is for learning purposes only. Do not use these
 * patterns in production code or attempt to exploit real contracts.
 */

contract VulnerableBank {
    mapping(address => uint256) public balances;
    mapping(address => bool) public authorized;
    address public owner;
    uint256 public totalDeposits;
    
    // Events for transparency
    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    event AdminAction(address indexed admin, string action);
    
    constructor() {
        owner = msg.sender;
        authorized[msg.sender] = true;
    }
    
    /**
     * VULNERABILITY 1: REENTRANCY
     * This function is vulnerable to reentrancy attacks because it:
     * 1. Calls external contract (msg.sender.call) before updating state
     * 2. Updates balance after the external call
     * 3. No reentrancy guard
     * 
     * Attack scenario: Malicious contract can call withdraw() again during
     * the external call, draining more funds than deposited.
     */
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // VULNERABILITY: External call before state update
        (bool success, ) = msg.sender.call{value: amount}("");
        // VULNERABILITY: Not checking return value
        
        // State update happens AFTER external call - allows reentrancy
        balances[msg.sender] -= amount;
        totalDeposits -= amount;
        
        emit Withdrawal(msg.sender, amount);
    }
    
    /**
     * VULNERABILITY 2: UNCHECKED EXTERNAL CALL
     * The call to external contract doesn't check return value
     */
    function emergencyWithdraw() public {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "No balance");
        
        balances[msg.sender] = 0;
        
        // VULNERABILITY: Unchecked external call - might fail silently
        msg.sender.call{value: balance}("");
        
        emit Withdrawal(msg.sender, balance);
    }
    
    /**
     * VULNERABILITY 3: ACCESS CONTROL ISSUES
     * This function lacks proper access control - anyone can call it
     */
    function adminWithdraw(uint256 amount) public {
        // VULNERABILITY: No access control modifier or require statement
        // Anyone can drain the contract!
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        emit AdminAction(msg.sender, "Emergency withdrawal");
    }
    
    /**
     * VULNERABILITY 4: TX.ORIGIN AUTHENTICATION
     * Using tx.origin instead of msg.sender for authentication
     */
    function authorizeUser(address user) public {
        // VULNERABILITY: Using tx.origin - vulnerable to phishing attacks
        require(tx.origin == owner, "Only owner can authorize");
        authorized[user] = true;
    }
    
    /**
     * VULNERABILITY 5: INTEGER OVERFLOW/UNDERFLOW
     * Pre-Solidity 0.8.0 doesn't have built-in overflow protection
     */
    function deposit() public payable {
        require(msg.value > 0, "Must deposit something");
        
        // VULNERABILITY: Potential overflow with large values
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
        
        // VULNERABILITY: Multiplication without SafeMath
        uint256 bonus = msg.value * 110 / 100; // 10% bonus
        balances[msg.sender] += bonus;
        
        emit Deposit(msg.sender, msg.value);
    }
    
    /**
     * VULNERABILITY 6: WEAK RANDOMNESS
     * Using blockchain data for randomness
     */
    function luckyWithdraw() public {
        require(balances[msg.sender] > 0, "No balance");
        
        // VULNERABILITY: Predictable randomness using block data
        uint256 random = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.difficulty,
            msg.sender
        ))) % 100;
        
        if (random > 50) {
            // Lucky! Get double withdrawal
            uint256 amount = balances[msg.sender] * 2;
            balances[msg.sender] = 0;
            
            (bool success, ) = msg.sender.call{value: amount}("");
            if (success) {
                emit Withdrawal(msg.sender, amount);
            }
        }
    }
    
    /**
     * VULNERABILITY 7: DEPRECATED FUNCTIONS
     * Using deprecated Solidity functions
     */
    function legacyFunction() public {
        // VULNERABILITY: Using deprecated sha3 instead of keccak256
        bytes32 hash = sha3(abi.encodePacked(msg.sender));
        
        if (hash[0] == 0x00) {
            // VULNERABILITY: Using deprecated throw instead of revert
            throw;
        }
    }
    
    /**
     * VULNERABILITY 8: UNINITIALIZED STORAGE POINTER
     * Dangerous use of storage pointers
     */
    struct UserData {
        uint256 amount;
        bool active;
    }
    
    mapping(address => UserData) userData;
    
    function updateUserData() public {
        // VULNERABILITY: Uninitialized storage pointer
        UserData storage user; // Points to storage slot 0!
        user.amount = 1000;
        user.active = true;
        // This might overwrite critical contract storage!
    }
    
    /**
     * Additional helper functions for testing
     */
    function getBalance(address user) public view returns (uint256) {
        return balances[user];
    }
    
    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }
    
    // Fallback function to receive Ether
    receive() external payable {
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
    }
    
    /**
     * VULNERABILITY 9: DELEGATECALL DANGER
     * Dangerous use of delegatecall
     */
    function executeDelegate(address target, bytes memory data) public {
        // VULNERABILITY: Uncontrolled delegatecall
        // This allows arbitrary code execution in the context of this contract
        (bool success, ) = target.delegatecall(data);
        require(success, "Delegatecall failed");
    }
}

/**
 * EDUCATIONAL NOTES:
 * 
 * This contract demonstrates multiple vulnerabilities commonly found in smart contracts:
 * 
 * 1. REENTRANCY: The withdraw() function calls external contracts before updating state,
 *    allowing attackers to call withdraw() multiple times before balance is updated.
 *    
 * 2. UNCHECKED CALLS: External calls don't check return values, leading to silent failures.
 * 
 * 3. ACCESS CONTROL: Critical functions lack proper access control mechanisms.
 * 
 * 4. TX.ORIGIN: Using tx.origin instead of msg.sender enables phishing attacks.
 * 
 * 5. INTEGER OVERFLOW: Pre-0.8.0 Solidity lacks overflow protection.
 * 
 * 6. WEAK RANDOMNESS: Block data is predictable and manipulable by miners.
 * 
 * 7. DEPRECATED FUNCTIONS: Using outdated language features that may be removed.
 * 
 * 8. STORAGE POINTERS: Uninitialized storage pointers can corrupt contract state.
 * 
 * 9. DELEGATECALL: Unrestricted delegatecall allows arbitrary code execution.
 * 
 * REMEDIATION STRATEGIES:
 * 
 * - Use ReentrancyGuard from OpenZeppelin
 * - Always check external call return values
 * - Implement proper access control (Ownable, AccessControl)
 * - Use msg.sender instead of tx.origin
 * - Upgrade to Solidity 0.8.0+ or use SafeMath
 * - Use secure randomness sources (Chainlink VRF)
 * - Avoid deprecated functions
 * - Initialize storage pointers properly
 * - Restrict delegatecall usage and validate targets
 * 
 * LEARNING RESOURCES:
 * - Ethernaut: https://ethernaut.openzeppelin.com/
 * - Damn Vulnerable DeFi: https://www.damnvulnerabledefi.xyz/
 * - SWC Registry: https://swcregistry.io/
 * - OpenZeppelin Security: https://docs.openzeppelin.com/contracts/security
 */