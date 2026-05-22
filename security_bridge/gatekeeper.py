#!/usr/bin/env python3
import hmac
import hashlib
import time
import sys

class SecurityBridge:
    def __init__(self, secret_key: str):
        # Enforce zero-trust: initialize with a strict master signature key
        self.secret_key = secret_key.encode('utf-8')
        print("[INIT] Zero-Trust Gatekeeper Engine Active. Default state: NO TRUST.")

    def generate_state_token(self, payload: str) -> tuple:
        """Generates a strictly timed, cryptographic state token for transactions."""
        timestamp = str(int(time.time()))
        message = f"{timestamp}:{payload}".encode('utf-8')
        
        # Create a secure SHA-256 HMAC signature string
        signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
        return timestamp, signature

    def verify_handshake(self, payload: str, timestamp: str, incoming_signature: str, max_age_seconds: int = 30) -> bool:
        """Verifies transaction tokens. Assumes malicious intent until mathematically proven clean."""
        try:
            # Rule 1: Check for token expiration (prevent replay vectors)
            current_time = int(time.time())
            token_time = int(timestamp)
            
            if current_time - token_time > max_age_seconds:
                print(f"[REJECT] Duality Paradox Detected: Token has expired by {current_time - token_time}s.")
                return False
                
            # Rule 2: Recalculate signature to ensure zero-tampering
            message = f"{timestamp}:{payload}".encode('utf-8')
            expected_signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
            
            # Use constant-time comparison to completely prevent side-channel timing analysis
            if hmac.compare_digest(expected_signature, incoming_signature):
                print(f"[SUCCESS] Handshake Authenticated. Payload validated cleanly.")
                return True
            else:
                print("[REJECT] Cryptographic signature mismatch! Intrusion vector dropped.")
                return False
                
        except Exception as e:
            print(f"[CRITICAL] Handshake execution failed: {str(e)}")
            return False

if __name__ == "__main__":
    # Test execution harness simulating a cross-node transaction handshake
    print("--- Testing Security Bridge Gatekeeper Handshake Pipeline ---")
    
    # 1. Instantiate the bridge with your environment key
    bridge = SecurityBridge(secret_key="#33577N1Gh73E3")
    
    # 2. Simulate generating a secure sync token package
    test_action = "SYNC_SOVEREIGN_VAULT_STATE"
    ts, sig = bridge.generate_state_token(payload=test_action)
    print(f"[TOKEN CREATED] TS: {ts} | SIG: {sig[:12]}...")
    
    # 3. Process the validation pass
    print("\n[VERIFYING INCOMING TRANSACTION]...")
    authenticated = bridge.verify_handshake(payload=test_action, timestamp=ts, incoming_signature=sig)
    
    print(f"\n[FINAL STATUS] Transmission allowed: {authenticated}")
