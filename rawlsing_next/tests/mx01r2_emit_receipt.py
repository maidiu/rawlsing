#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.pre553_recursive_handoff import replay_recursive_branch_membership, write_recursive_handoff_bundle
from rawlsing_next.tests.test_pre553_recursive_handoff import _fixture, _generation_one


def main() -> None:
    source, qauth = _fixture()
    parent, g1, g1_registry = _generation_one(source, qauth)
    child = g1.handoffs[0]
    child_members = replay_recursive_branch_membership(
        repository=source["repo"], handoff=child, authority_registry=g1_registry
    )
    with tempfile.TemporaryDirectory(prefix="mx01r2-") as td:
        td_path = Path(td)
        child_bundle = td_path / "child.bundle.json"
        child_bundle_ref = write_recursive_handoff_bundle(child_bundle, g1.handoffs)
        process_payloads = []
        for index in (1, 2):
            out = td_path / f"fresh-{index}.json"
            subprocess.run(
                [sys.executable, "-m", "rawlsing_next.tests.mx01r2_fresh_process_runner", str(child_bundle), str(out)],
                check=True,
            )
            process_payloads.append(json.loads(out.read_text(encoding="utf-8")))
        if process_payloads[0] != process_payloads[1]:
            raise AssertionError("fresh-process semantic receipts diverged")
        fresh = process_payloads[0]
        receipt = canonicalize({
            "experiment": "MX01_R2_RECURSIVE_HANDOFF_CLOSURE_R1",
            "status": "PASS",
            "ci_run_id": os.environ.get("GITHUB_RUN_ID", "LOCAL"),
            "ci_head_sha": os.environ.get("GITHUB_SHA", "LOCAL"),
            "fresh_process_count": 2,
            "fresh_process_outputs_identical": True,
            "parent_predicate_ref": parent.ref,
            "generation_1": {
                "discovery_receipt_refs": tuple(r.ref for r in g1.discovery_result.receipts),
                "frontier_replay_ref": g1.discovery_result.replay_ref,
                "child_bundle_ref": child_bundle_ref,
                "child_handoff_ref": child.ref,
                "child_predicate_ref": child.winning_predicate.ref,
                "child_immediate_parent_ref": child.immediate_parent_branch_ref,
                "child_member_refs": child_members,
            },
            "fresh_process_replay": fresh,
            "fresh_process_semantic_hash": semantic_hash(fresh),
        })
        print("MX01R2_RECEIPT_JSON=" + json.dumps(receipt, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
