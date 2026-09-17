#!/usr/bin/env python3
"""Verify the source-free EE-P2F0 blocker receipt."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
receipt = json.loads((root / "05_WVS7_P2_LOCK2_RECEIPT.json").read_text())
assert receipt["status"] == "BLOCKED__NO_ACCEPTED_CURRENT_PRE553_WVS7_DISCOVERY_AUTHORITY_AND_OBJECT_BINDING_CLOSURE"
assert receipt["frozen_workload"]["required_candidate_count"] == 46
assert receipt["consumed_authority"]["routing_positive_or_known_count"] == 0
assert all(not value for value in receipt["prohibitions_observed"].values())
print("PASS__EE_P2F0_SOURCE_FREE_BLOCKER_RECEIPT_VERIFIED")
