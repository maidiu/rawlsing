#!/usr/bin/env python3
"""Typed-state entrypoint for the bounded Section 85 diagnostic smoke matrix.

The pre-G2 diagnostic implementation is preserved byte-for-byte in
`_legacy_run_section85_diagnostic_smoke_matrix.py` so its inventory, privacy,
packaging and database-diagnostic behavior does not drift during W01-B. This
entrypoint replaces only the obsolete V551J readiness-boolean gate with the
shared typed producer-state contract.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from section85_typed_state import typed_stage_gate  # noqa: E402

LEGACY_IMPLEMENTATION = CODE_DIR / "_legacy_run_section85_diagnostic_smoke_matrix.py"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def current_v551j_gate(v551j_root: Path) -> dict[str, Any]:
    """Consume only typed V551J producer state as executable acceptance.

    Legacy counts and validation reports remain diagnostic context. They cannot
    establish run integrity or downstream permission. Until W03-B merges a
    rawlsing_pipeline_boundary_v1 V551J manifest, this gate fails closed with an
    explicit G3B hook requirement.
    """
    manifest = _load_json(v551j_root / "manifest/manifest.json")
    readiness = _load_json(v551j_root / "manifest/v551j_readiness_report.json")
    validation = _load_json(v551j_root / "manifest/v551j_packet_contract_validation_report.json")
    typed = typed_stage_gate(manifest, stage="v551j")

    candidate_count = readiness.get("candidate_packet_count", manifest.get("row_counts", {}).get("candidate", 0))
    component_count = readiness.get("component_row_count", manifest.get("row_counts", {}).get("component", 0))
    certified_count = readiness.get("certified_packet_count", manifest.get("row_counts", {}).get("certified", 0))
    issues_json = validation.get("issues_json", "[]")
    return {
        **typed,
        "hook_status": "ACTIVE_TYPED_PRODUCER_CONTRACT" if typed["typed_contract_valid"] else "AWAITING_G3B_PRODUCER_HOOK",
        "candidate_packet_count": candidate_count,
        "component_row_count": component_count,
        "certified_packet_count": certified_count,
        "review_required_packet_count": readiness.get("review_required_packet_count", 0),
        "blocked_packet_count": readiness.get("blocked_packet_count", 0),
        "issues_json": issues_json,
        "legacy_diagnostics": {
            "final_status": readiness.get("final_status") or manifest.get("final_status", ""),
            "candidate_contract_valid": readiness.get("candidate_contract_valid", validation.get("candidate_contract_valid", False)),
            "component_contract_valid": readiness.get("component_contract_valid", validation.get("component_contract_valid", False)),
            "issues_json": issues_json,
        },
    }


def load_implementation():
    spec = importlib.util.spec_from_file_location("section85_diagnostic_legacy", LEGACY_IMPLEMENTATION)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"SECTION85_DIAGNOSTIC_IMPLEMENTATION_UNLOADABLE:{LEGACY_IMPLEMENTATION}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.current_v551j_gate = current_v551j_gate
    return module


def main() -> int:
    return int(load_implementation().main())


if __name__ == "__main__":
    raise SystemExit(main())
