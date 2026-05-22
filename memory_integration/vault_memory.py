#!/usr/bin/env python3
import sys
import os

# Adjust pathing dynamically to allow cross-module simulation imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from system_tokens.token_engine import TokenEngine
from security_bridge.gatekeeper import SecurityBridge

class SovereignMemoryVault:
    def __init__(self, secret_key: str):
        # Initialize internal state database tracking dictionary
        self.state_registry = {}
        # Instantiate the security bridge locally to handle zero-trust checks
        self.bridge = SecurityBridge(secret_key=secret_key)
        print("[VAULT-INIT] Sovereign Memory Storage Container Online and Locked.")

    def commit_state_change(self, action: str, data: dict, token_engine: TokenEngine):
        """
        Processes a secure state change transaction.
        Enforces the complete end-to-end integration loop.
        """
        print(f"\n[TRANSACTION ATTEMPT] Initiating state change for action: {action}")
        
        # 1. Mint a unique, bottleneck-resolved sequence token envelope
        token_envelope = token_engine.mint_state_token(action_type=action, data_payload=data)
        serialized_data = token_engine.serialize_for_bridge(token_envelope)
        
        # 2. Derive a valid validation signature for the tracking pass
        ts, sig = self.bridge.generate_state_token(payload=serialized_data)
        
        print("[GATEKEEPER CHALLENGE] Submitting token sequence to verification layer...")
        
        # 3. Intercept and verify data integrity via the security bridge
        is_valid = self.bridge.verify_handshake(
            payload=serialized_data, 
            timestamp=ts, 
            incoming_signature=sig
        )
        
        # 4. Enforce strict logic boundary conditions
        if is_valid:
            token_id = token_envelope["token_id"][:8]
            self.state_registry[action] = {
                "status": "COMMITTED",
                "token_ref": token_id,
                "timestamp": ts,
                "payload": data
            }
            print(f"[SUCCESS] State change successfully registered in vault under token: {token_id}")
        else:
            print("[CRITICAL FAILURE] Unauthorized transaction dropped at the perimeter.")

    def display_current_vault_matrix(self):
        print("\n=== CURRENT SOVEREIGN STORAGE REGISTRY STATUS ===")
        if not self.state_registry:
            print("Vault is currently empty.")
        for action, record in self.state_registry.items():
            print(f"Action: {action} | Token: {record['token_ref']} | Status: {record['status']}")
        print("================================================")

if __name__ == "__main__":
    print("--- Testing Full System Memory Integration Pipeline ---")
    
    # Define our consistent testing key signature
    master_key = "#6933UNLQ!ck3357"
    
    # Instantiate the system components
    vault = SovereignMemoryVault(secret_key=master_key)
    node_engine = TokenEngine(node_id="PIXEL-10-CORE-NODE")
    
    # Execute a sample secure data state commit
    sample_payload = {"duality_paradox_status": "BALANCED", "emotional_bridge_lock": True}
    vault.commit_state_change(action="COMMIT_CORE_MEMORY", data=sample_payload, token_engine=node_engine)
    
    # Display the updated storage map tracking data
    vault.display_current_vault_matrix()
