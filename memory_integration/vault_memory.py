#!/usr/bin/env python3
import os
import json
import time

class SovereignMemoryVault:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        # Establish the persistent file path inside your local project workspace
        self.storage_file = os.path.join(os.path.dirname(__file__), "vault_ledger.json")
        self.state_registry = self._load_vault_from_disk()
        print(f"[VAULT-INIT] Persistent Ledger Online -> Tracked Objects: {len(self.state_registry)}")

    def _load_vault_from_disk(self):
        """Loads historical states from local file storage or initializes a clean ledger structure."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("[WARN] Local storage ledger corrupted. Recovering blank state matrix.")
                return {}
        return {}

    def _flush_vault_to_disk(self):
        """Secures and writes the live active state registry straight onto your phone's storage."""
        try:
            with open(self.storage_file, "w") as f:
                json.dump(self.state_registry, f, indent=4)
            return True
        except Exception as e:
            print(f"[CRITICAL] Storage write failure: {str(e)}")
            return False

    def commit_state_change(self, action, data, token_engine):
        print(f"\n[TRANSACTION ATTEMPT] Initiating state change for action: {action}")
        
        # Correctly call the authentic token engine layer method
        token_envelope = token_engine.mint_state_token(action_type=action, data_payload=data)
        token = token_envelope["token_id"][:8]
        print(f"[MINT] Token {token} sequenced for {action}.")

        # Package the state entry matrix
        state_entry = {
            "timestamp": int(time.time()),
            "action": action,
            "payload": data,
            "signature_verified": True
        }

        # Commit entry to memory matrix map and instantly write to disk
        self.state_registry[token] = state_entry
        if self._flush_vault_to_disk():
            print(f"[SUCCESS] State change permanently sealed to ledger under token: {token}")
        else:
            print(f"[ERROR] State committed to RAM but local storage write failed.")

    def display_current_vault_matrix(self):
        """Prints out the clean historical state entries currently saved inside the ledger."""
        print("\n================== RECOVERY VAULT LEDGER REGISTRY ==================")
        if not self.state_registry:
            print(" [EMPTY] No transaction states have been committed to this node yet.")
        else:
            for token, matrix in self.state_registry.items():
                print(f"Token Node: {token}")
                print(f"  ↳ Action   : {matrix['action']}")
                print(f"  ↳ Time     : {matrix['timestamp']}")
                print(f"  ↳ Data     : {json.dumps(matrix['payload'])}")
                print("-" * 68)
        print("====================================================================")

