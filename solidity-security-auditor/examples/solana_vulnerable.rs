// Solana Program with Security Vulnerabilities (Educational Example)
// DISCLAIMER: This code contains intentional vulnerabilities for educational purposes.
// DO NOT use in production. Practice responsible disclosure.

use anchor_lang::prelude::*;
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    pubkey::Pubkey,
    program_pack::{Pack, IsInitialized},
    sysvar::{rent::Rent, Sysvar},
};

declare_id!("11111111111111111111111111111112");

#[program]
pub mod vulnerable_program {
    use super::*;

    // VULNERABILITY 1: Missing signer check
    pub fn transfer_tokens(ctx: Context<TransferTokens>, amount: u64) -> Result<()> {
        let from_account = &ctx.accounts.from_account;
        let to_account = &ctx.accounts.to_account;
        
        // BUG: Not checking if from_account is a signer
        // Should verify: from_account.is_signer
        
        // Unsafe transfer without proper validation
        **from_account.try_borrow_mut_lamports()? -= amount;
        **to_account.try_borrow_mut_lamports()? += amount;
        
        Ok(())
    }

    // VULNERABILITY 2: Unchecked account ownership
    pub fn update_metadata(ctx: Context<UpdateMetadata>, new_data: String) -> Result<()> {
        let metadata_account = &ctx.accounts.metadata_account;
        
        // BUG: Not verifying account ownership
        // Should check: metadata_account.owner == &id()
        
        // Unsafe deserialization
        let mut data = metadata_account.data.borrow_mut();
        let metadata = unsafe { 
            // VULNERABILITY 3: Unsafe deserialization
            std::mem::transmute::<&mut [u8], &mut Metadata>(&mut data[..])
        };
        
        metadata.content = new_data;
        
        Ok(())
    }

    // VULNERABILITY 4: Integer overflow without checks
    pub fn calculate_rewards(ctx: Context<CalculateRewards>, multiplier: u64) -> Result<()> {
        let user_account = &ctx.accounts.user_account;
        let mut user_data = user_account.data.borrow_mut();
        
        let current_balance = u64::from_le_bytes([
            user_data[0], user_data[1], user_data[2], user_data[3],
            user_data[4], user_data[5], user_data[6], user_data[7],
        ]);
        
        // BUG: Potential integer overflow
        // Should use: current_balance.checked_mul(multiplier)
        let new_balance = current_balance * multiplier;
        
        user_data[..8].copy_from_slice(&new_balance.to_le_bytes());
        
        Ok(())
    }

    // VULNERABILITY 5: Missing rent exemption check
    pub fn create_account(ctx: Context<CreateAccount>) -> Result<()> {
        let new_account = &ctx.accounts.new_account;
        let rent = Rent::get()?;
        
        // BUG: Not checking if account is rent exempt
        // Should verify: rent.is_exempt(new_account.lamports(), new_account.data_len())
        
        let mut data = new_account.data.borrow_mut();
        
        // VULNERABILITY 6: Accessing potentially uninitialized account
        // Should check: data.is_empty()
        data[0] = 1; // Mark as initialized
        
        Ok(())
    }

    // VULNERABILITY 7: Missing bump validation for PDA
    pub fn create_pda_account(ctx: Context<CreatePdaAccount>, seed: String) -> Result<()> {
        let pda_account = &ctx.accounts.pda_account;
        
        // BUG: Not validating bump seed
        let (expected_pda, _bump) = Pubkey::find_program_address(
            &[seed.as_bytes()],
            &id(),
        );
        
        // Should verify: pda_account.key() == expected_pda
        
        Ok(())
    }
}

#[derive(Accounts)]
pub struct TransferTokens<'info> {
    #[account(mut)]
    pub from_account: AccountInfo<'info>,
    #[account(mut)]
    pub to_account: AccountInfo<'info>,
}

#[derive(Accounts)]
pub struct UpdateMetadata<'info> {
    #[account(mut)]
    pub metadata_account: AccountInfo<'info>,
}

#[derive(Accounts)]
pub struct CalculateRewards<'info> {
    #[account(mut)]
    pub user_account: AccountInfo<'info>,
}

#[derive(Accounts)]
pub struct CreateAccount<'info> {
    #[account(mut)]
    pub new_account: AccountInfo<'info>,
}

#[derive(Accounts)]
pub struct CreatePdaAccount<'info> {
    #[account(mut)]
    pub pda_account: AccountInfo<'info>,
}

#[repr(C)]
pub struct Metadata {
    pub content: String,
    pub is_initialized: bool,
}

// Additional vulnerable patterns for educational purposes

// VULNERABILITY 8: Unsafe account validation
pub fn unsafe_account_validation(account: &AccountInfo) -> bool {
    // BUG: Weak validation - should do comprehensive checks
    account.data_len() > 0
}

// VULNERABILITY 9: Missing error handling
pub fn risky_operation(accounts: &[AccountInfo]) -> ProgramResult {
    let account = next_account_info(&mut accounts.iter())?;
    
    // BUG: No error handling for potential failures
    let data = account.try_borrow_data().unwrap();
    let value = u64::from_le_bytes([
        data[0], data[1], data[2], data[3],
        data[4], data[5], data[6], data[7],
    ]);
    
    // Risky operation without bounds checking
    let result = value / (value - 100); // Potential division by zero
    
    Ok(())
}

// Educational note about secure practices:
// 1. Always verify account signers with .is_signer
// 2. Check account ownership with .owner comparisons  
// 3. Use checked arithmetic operations
// 4. Validate rent exemption for persistent accounts
// 5. Verify PDA bump seeds for canonical addresses
// 6. Check account initialization before use
// 7. Handle errors gracefully without panicking
// 8. Use safe deserialization methods