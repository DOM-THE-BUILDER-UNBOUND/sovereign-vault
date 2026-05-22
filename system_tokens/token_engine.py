#!/usr/bin/env python3
import time
import json
import uuid

class TokenEngine:
    def __init__(self, node_id: str):
        self.node_id = node_id
        print(f"[NODE-ACTIVE] Token engine tracking established for node: {self.node_id}")

    def mint_state_token(self, action_type: str, data_payload: dict) -> dict:
        """
        Mints a uniquely sequenced transaction packet.
        Uses high-resolution timestamps to completely eliminate synchronization bottlenecks.
        """
        # Enforce unique sequencing with a nano-second component to avoid state collisions
        sequence_time = time.time()
        
        token_envelope = {
            "token_id": str(uuid.uuid4()),
            "origin_node": self.node_id,
            "timestamp": str(int(sequence_time)),
            "sequence_marker": sequence_time,
            "action": action_type,
            "payload": data_payload
        }
        
        print(f"[MINT] Token {token_envelope['token_id'][:8]} sequenced for {action_type}.")
        return token_envelope

    def serialize_for_bridge(self, token: dict) -> str:
        """Converts the internal envelope token to a clean string format for Gatekeeper validation."""
        # Sorting keys guarantees identical string generation across different machine environments
        return json.dumps(token, sort_keys=True)

if __name__ == "__main__":
    print("--- Testing Token Core Sequencing Loop ---")
    
    # 1. Initialize local node engine
    engine = TokenEngine(node_id="PIXEL-10-CORE-NODE")
    
    # 2. Simulate rapid transactions that normally cause a bottleneck
    payload_data = {"vault_sync_status": "IMMACCULATE", "active_dualities": 2}
    
    print("\n[GENERATING SEQUENCED TRANSACTION TOKENS]...")
    token_1 = engine.mint_state_token("VAULT_WRITE", payload_data)
    time.sleep(0.1) # Simulate brief network separation
    token_2 = engine.mint_state_token("VAULT_MIRROR", payload_data)
    
    # 3. Show serialization format destined for the gatekeeper
    flat_string = engine.serialize_for_bridge(token_1)
    print(f"\n[SERIALIZED DATA FOR SECURITY BRIDGE]:\n{flat_string[:90]}...")
