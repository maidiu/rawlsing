#!/usr/bin/env python3
"""Verify the external control binding on a clean docs descendant checkout."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


PACKET_ROOT = Path(__file__).resolve().parent
CONTROL_ROOT = PACKET_ROOT.parents[1]
EXPECTED_BRANCH = "agent/vozhd-fiabc-split-r2-fanin-r1"
EXPECTED_QUALIFIED_HEAD = "ed8dabf015d1fd4b4ade9b55816a420b0bc1811e"


def main() -> None:
    helper_path = CONTROL_ROOT / "HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py"
    spec = importlib.util.spec_from_file_location("fiabc_clean_control_binding_verify", helper_path)
    if spec is None or spec.loader is None:
        raise SystemExit("source-local evidence helper unavailable")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    branch = helper._git(CONTROL_ROOT, "branch", "--show-current").stdout.strip()
    head = helper._git(CONTROL_ROOT, "rev-parse", "HEAD").stdout.strip()
    if branch != EXPECTED_BRANCH or len(head) != 40:
        raise SystemExit("wrong branch or malformed evidence/docs head")
    proof = helper.verify_control_binding(
        binding_path=PACKET_ROOT / "CONTROL_BINDING.json",
        control_root=CONTROL_ROOT,
        require_clean=True,
    )
    if proof.get("qualified_implementation_head") != EXPECTED_QUALIFIED_HEAD:
        raise SystemExit("control binding names the wrong qualified implementation head")
    if proof.get("observed_control_checkout_head") != head or proof.get("control_checkout_clean") is not True:
        raise SystemExit("control binding clean-descendant proof is incomplete")
    document = {
        "schema": "RAWLSING_FIABC_SOURCE_SPLIT_R2_CONTROL_BINDING_CLEAN_VERIFICATION@1.0.0",
        "status": "PASS__QUALIFIED_CODE_HASHES_MATCH_ON_CLEAN_EVIDENCE_DESCENDANT",
        "checkout_branch": branch,
        "observed_clean_evidence_docs_head": head,
        "qualified_implementation_head": EXPECTED_QUALIFIED_HEAD,
        **proof,
    }
    target = PACKET_ROOT / "CONTROL_BINDING_CLEAN_VERIFY.json"
    target.write_text(json.dumps(document, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": document["status"], "observed_head": head, "receipt_identity": proof["binding_receipt_identity"]}, sort_keys=True))


if __name__ == "__main__":
    main()
