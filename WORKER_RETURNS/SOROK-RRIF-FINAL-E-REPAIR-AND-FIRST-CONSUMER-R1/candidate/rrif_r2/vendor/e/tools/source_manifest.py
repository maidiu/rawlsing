#!/usr/bin/env python3
"""Write R31E source and expression-port manifests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = next(p for p in ROOT.parents if (p / ".git").exists())
VENDOR = ROOT / "vendor" / "r30a"
R30A_REF = "ce0dfc67ef5058338f4d7161d32a8cb5bdf733a6"
R29P_REF = "001b506fa26ae879ff5b6e57138fc2696e12b538"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main():
    vendor_files = {}
    for path in sorted(VENDOR.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            vendor_files[str(path.relative_to(VENDOR))] = sha(path)
    port_files = {}
    for path in sorted((ROOT / "r31e").glob("*.py")):
        port_files[path.name] = sha(path)
    live = {}
    for rel in ("rawlsing_next/m6_actor_safe_expression.py",
                "rawlsing_next/v3_psepf_zero_positive_guard.py"):
        path = REPO / rel
        live[rel] = {"blob": blob(path), "sha256": sha(path)}
    source = {
        "schema": "R31E_SOURCE_MANIFEST@1",
        "r30a_ref": R30A_REF,
        "r30a_return": "WORKER_RETURNS/SOROK-20261021-R30A-FIRST-NEIGHBOR-SESSION-R1",
        "r29p_ref": R29P_REF,
        "vendor_root": "vendor/r30a",
        "vendor_file_count": len(vendor_files),
        "vendor_files": vendor_files,
        "port_files": port_files,
        "live_module_pins": live,
        "note": "R30A/R29P code is copied read-only; no upstream byte was edited.",
    }
    (ROOT / "evidence/source_manifest.json").write_text(
        json.dumps(source, indent=2, sort_keys=True) + "\n", encoding="utf8")
    # Import expression for template/port counts (setup path first).
    import sys
    sys.path.insert(0, str(ROOT))
    from r31e import expression
    port = {
        "schema": "R31E_EXPRESSION_PORT@1",
        "version": 1,
        "contract_schema": expression.CONTRACT_SCHEMA,
        "candidate_schema": expression.CANDIDATE_SCHEMA,
        "admission_schema": expression.ADMISSION_SCHEMA,
        "grade": expression.GRADE,
        "template_count": len(expression.TEMPLATES),
        "strategy_families": [
            "BOUNDARY_WITHDRAW", "BOUNDARY_COERCION", "PRIVATE_BOUNDARY",
            "INTIMACY_BOUNDARY", "CONTACT_GRANT", "CONTACT_DEFER",
            "CONTACT_REFUSE", "HELP_ACCEPT", "HELP_REFUSE", "HELP_INVITE",
            "EXPLAIN_WORK", "RECALL_WORK", "DEFER_WORK", "RECIPROCATE",
            "RECALL", "UNKNOWN_B", "OBSERVED_B", "PRESENT_B",
            "DECLINE_INVITATION", "DEFER_UNKNOWN", "UNSUPPORTED_MEMORY",
            "ACKNOWLEDGE", "INITIATE", "DEPART", "DEPART_RECALL", "MESSAGE",
            "RETURN", "SILENCE_TASK", "LAWFUL_SILENCE",
        ],
        "actor_source": R29P_REF,
        "live_actor_model": "LIVE_ACTOR_MODEL_NOT_RUN",
        "provider_calls": 0,
        "port_files": port_files,
    }
    (ROOT / "evidence/port_receipt.json").write_text(
        json.dumps(port, indent=2, sort_keys=True) + "\n", encoding="utf8")
    print(json.dumps({"vendor_files": len(vendor_files),
                      "templates": len(expression.TEMPLATES),
                      "port_files": len(port_files)}, indent=1))


if __name__ == "__main__":
    main()
