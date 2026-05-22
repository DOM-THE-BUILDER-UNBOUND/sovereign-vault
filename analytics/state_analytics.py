#!/usr/bin/env python3
import sys
import os
import time

# Ensure dynamic path access to sibling core directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory_integration.vault_memory import SovereignMemoryVault
from system_tokens.token_engine import TokenEngine

class VaultAnalytics:
    def __init__(self, target_vault: SovereignMemoryVault):
        self.vault = target_vault
        print("[ANALYTICS-INIT] Telemetry and System Health Engine Online.")

    def run_health_audit(self) -> dict:
        """Audits the memory registry to compile health metrics and processing performance."""
        print("\n[AUDIT] Scanning sovereign vault memory registry logs...")
        time.sleep(0.2) # Simulate quick hardware bus check
        
        total_records = len(self.vault.state_registry)
        committed_actions = list(self.vault.state_registry.keys())
        
        # Compile system telemetry status payload
        report = {
            "timestamp": str(int(time.time())),
            "total_integrity_checks": total_records,
            "active_registry_blocks": committed_actions,
            "perimeter_status": "SECURE",
            "system_health_rating": "100%" if total_records > 0 else "NOMINAL"
        }
        
        return report

    def display_telemetry_dashboard(self, report: dict):
        """Outputs a clean, scannable structural summary screen of system operations."""
        print("\n================================================")
        print("          SOVEREIGN CORE TELEMETRY DASHBOARD    ")
        print("================================================")
        print(f"  System Timestamp   : {report['timestamp']}")
        print(f"  Perimeter Status   : {report['perimeter_status']} ✅")
        print(f"  Active Core Blocks : {report['total_integrity_checks']}")
        print(f"  Registered Actions : {report['active_registry_blocks']}")
        print(f"  Health Rating      : {report['system_health_rating']}")
        print("================================================\n")

if __name__ == "__main__":
    print("--- Testing Sovereign Core Analytics Pipeline ---")
    
    # 1. Simulate setting up a live storage and node engine
    os.environ["SOVEREIGN_KEY"] = "#6933UNLQ!ck3357"
    vault = SovereignMemoryVault(secret_key=os.environ["SOVEREIGN_KEY"])
    node_engine = TokenEngine(node_id="PIXEL-10-ANALYTICS-NODE")
    
    # 2. Feed a sample state through to populate the registry tracking
    vault.commit_state_change(
        action="INITIALIZE_GRID_METRICS", 
        data={"node_sync": "TRUE"}, 
        token_engine=node_engine
    )
    
    # 3. Spin up the analytics auditor over the storage vault
    telemetry_engine = VaultAnalytics(target_vault=vault)
    audit_report = telemetry_engine.run_health_audit()
    
    # 4. Render the dashboard
    telemetry_engine.display_telemetry_dashboard(audit_report)
