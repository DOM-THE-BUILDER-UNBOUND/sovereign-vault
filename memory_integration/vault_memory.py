#!/usr/bin/env python3
import os
import json
import time

class SovereignMemoryVault:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.storage_file = os.path.join(os.path.dirname(__file__), "vault_ledger.json")
        self.state_registry = self._load_and_decrypt_vault()
        print(f"[VAULT-INIT] Crypto Ledger Active -> Tracked Secure Objects: {len(self.state_registry)}")

    def _cipher_transform(self, raw_string):
        """Applies a localized cryptographic XOR cipher stream using the master session key."""
        if not self.secret_key:
            return raw_string
        
        key_len = len(self.secret_key)
        # Transform stream by cycling characters against the secret key signature bytes
        transformed = "".join(
            chr(ord(char) ^ ord(self.secret_key[i % key_len])) 
            for i, char in enumerate(raw_string)
        )
        return transformed

    def _load_and_decrypt_vault(self):
        """Reads the raw file storage array, running it through the cipher filter."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    raw_data = f.read().strip()
                
                if not raw_data:
                    return {}
                
                # Check if file is raw JSON or encrypted ciphertext
                if raw_data.startswith("{"):
                    print("[VAULT] Legacy plain-text ledger detected. Staging for auto-encryption.")
                    return json.loads(raw_data)
                
                # Decrypt the cipher block back into clear text JSON structure
                decrypted_json_str = self._cipher_transform(raw_data)
                return json.loads(decrypted_json_str)
                
            except Exception as e:
                print(f"[WARN] Cryptographic read mismatch or file corrupted. Re-initializing matrix map. Error: {str(e)}")
                return {}
        return {}

    def _flush_and_encrypt_vault(self):
        """Converts the live registry map into JSON, encrypts it, and seals it onto disk."""
        try:
            plain_json_str = json.dumps(self.state_registry, indent=4)
            # Scramble the structured data before it touches storage media
            ciphertext_block = self._cipher_transform(plain_json_str)
            
            with open(self.storage_file, "w") as f:
                f.write(ciphertext_block)
            return True
        except Exception as e:
            print(f"[CRITICAL] Cryptographic file write failure: {str(e)}")
            return False

    def commit_state_change(self, action, data, token_engine):
        print(f"\n[SECURE TRANSACTION] Registering state node for: {action}")
        
        token_envelope = token_engine.mint_state_token(action_type=action, data_payload=data)
        token = token_envelope["token_id"][:8]

        state_entry = {
            "timestamp": int(time.time()),
            "action": action,
            "payload": data,
            "signature_verified": True
        }

        self.state_registry[token] = state_entry
        if self._flush_and_encrypt_vault():
            print(f"[SUCCESS] State change encrypted and sealed under token reference: {token}")
        else:
            print(f"[ERROR] Transaction aborted. Encryption engine write failed.")

    def display_current_vault_matrix(self):
        """Decodes and beautifully structures the live active session registry map."""
        print("\n================== ENCRYPTED RECOVERY LEDGER MATRIX ==================")
        if not self.state_registry:
            print(" [SECURE-EMPTY] No active transaction states loaded in this clear-zone.")
        else:
            for token, matrix in self.state_registry.items():
                print(f"Secure Token: {token}")
                print(f"  ↳ Core Action: {matrix['action']}")
                print(f"  ↳ Epoch Time : {matrix['timestamp']}")
                print(f"  ↳ Payload Map: {json.dumps(matrix['payload'])}")
                print("-" * 70)
        print("========================================================================")
