#!/usr/bin/env python3
import os
import sys

from system_tokens.token_engine import TokenEngine
from security_bridge.gatekeeper import SecurityBridge
from memory_integration.vault_memory import SovereignMemoryVault
from analytics.state_analytics import VaultAnalytics

def main():
    # Enforce environmental security check
    master_key = os.environ.get("SOVEREIGN_KEY")
    if not master_key:
        print("[CRITICAL] SOVEREIGN_KEY environment variable missing!")
        print("Please run: export SOVEREIGN_KEY='your_key' before launching.")
        sys.exit(1)

    # Initialize full core matrix stacks
    node_engine = TokenEngine(node_id="TERMUX-MASTER-CONSOLE")
    vault = SovereignMemoryVault(secret_key=master_key)
    telemetry = VaultAnalytics(target_vault=vault)

    while True:
        print("\n=== SOVEREIGN VAULT MATRIX CONTROL ===")
        print("1. Commit New State Entry to Vault")
        print("2. Run Perimeter Health & Telemetry Audit")
        print("3. View Storage Memory Registry")
        print("4. Exit Console")
        print("======================================")
        
        choice = input("Select operation node [1-4]: ").strip()

        if choice == "1":
            action = input("\nEnter transaction action tag (e.g., SYNC_LOG): ").strip().upper()
            payload_key = input("Enter metadata payload key: ").strip()
            payload_val = input("Enter metadata payload value: ").strip()
            
            if action and payload_key:
                data = {payload_key: payload_val}
                vault.commit_state_change(action=action, data=data, token_engine=node_engine)
            else:
                print("[ERROR] Invalid entries. Transaction aborted.")

        elif choice == "2":
            report = telemetry.run_health_audit()
            telemetry.display_telemetry_dashboard(report)

        elif choice == "3":
            vault.display_current_vault_matrix()

        elif choice == "4":
            print("\n[SHUTDOWN] Securing peripheral locks. Exiting A-team console.")
            break
        else:
            print("[INVALID] Operation out of bounds.")

if __name__ == "__main__":
    main()
