#!/usr/bin/env python3
import os
import sys

# Validate active secure environment variables
if "SOVEREIGN_KEY" not in os.environ:
    print("[CRITICAL] SOVEREIGN_KEY environment variable missing!")
    print("Please run: export SOVEREIGN_KEY='your_key' before launching.\n")
    sys.exit(1)

# Import our custom engineering modules
from system_tokens.token_engine import TokenEngine
from memory_integration.vault_memory import SovereignMemoryVault
from analytics.state_analytics import SovereignTelemetryEngine

def main():
    secret_key = os.environ.get("SOVEREIGN_KEY")
    
    # Initialize the core sub-system engines
    token_engine = TokenEngine(secret_key)
    vault = SovereignMemoryVault(secret_key=secret_key)
    telemetry = SovereignTelemetryEngine()

    while True:
        print("\n=== SOVEREIGN VAULT MATRIX CONTROL ===")
        print("1. Commit New State Entry to Vault")
        print("2. Run Perimeter Health & Telemetry Audit")
        print("3. View Storage Memory Registry")
        print("4. Exit Console")
        print("======================================")
        
        try:
            choice = input("Select operation node [1-4]: ").strip()
        except KeyboardInterrupt:
            print("\n\n[SHUTDOWN] Securing peripheral locks. Exiting A-team console.")
            break

        if choice == "1":
            action = input("\nEnter transaction action tag (e.g., SYNC_LOG): ").strip().upper()
            payload_key = input("Enter metadata payload key: ").strip()
            payload_val = input("Enter metadata payload value: ").strip()
            
            if action and payload_key and payload_val:
                data_matrix = {payload_key: payload_val}
                vault.commit_state_change(action=action, data=data_matrix, token_engine=token_engine)
            else:
                print("[ERROR] Input parameters cannot be blank.")

        elif choice == "2":
            # Fire the brand new network telemetry array module
            telemetry.run_perimeter_ping_audit()

        elif choice == "3":
            vault.display_current_vault_matrix()

        elif choice == "4":
            print("\n[SHUTDOWN] Securing peripheral locks. Exiting A-team console.")
            break
        else:
            print("[INVALID] Unrecognized signature input code.")

if __name__ == "__main__":
    main()

