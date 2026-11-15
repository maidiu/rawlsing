"""Fresh-process cold consumer runner for the S2-F durable closure.

This file is both a pytest module (it intentionally defines no test function) and
a CLI used by ``test_pyat940_s2f_durable_closure.py``.  The fresh process:

1. installs an ``open`` audit hook;
2. opens the durable closure with an *external* root pin;
3. reconstructs the exact native objects;
4. invokes the actual existing M1 composer and descriptive Field Forge reader;
5. reports exact identities and the number of original-source opens.

It never imports the synthetic source fixture, never receives a repository or a
native in-memory object, and never opens a `.sav/.dta/.parquet/.csv` source file.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import resource
import sys
import time

from rawlsing_next.pre553_durable_empirical_closure import (
    RIGHTS_STATE,
    open_empirical_closure,
)

SOURCE_EXTENSIONS = (
    ".sav",
    ".dta",
    ".parquet",
    ".csv",
    ".rdata",
    ".rds",
    ".feather",
    ".arrow",
    ".por",
)


def _path_text(value) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return str(value)


def run_cold_consumer(
    closure_path: str,
    expected_root: str,
    expected_path: str | None = None,
) -> dict:
    counts = {
        "total_opens": 0,
        "closure_opens": 0,
        "source_opens": 0,
        "source_candidates": [],
    }
    closing = Path(closure_path).resolve()
    cas_root = closing.parent.parent

    def _audit(event: str, args) -> None:
        if event != "open" or not args:
            return
        path = Path(_path_text(args[0])).resolve()
        counts["total_opens"] += 1
        try:
            path.relative_to(closing)
            counts["closure_opens"] += 1
            return
        except ValueError:
            pass
        try:
            path.relative_to(cas_root)
            counts["closure_opens"] += 1
            return
        except ValueError:
            pass
        text = str(path).lower()
        if text.endswith(SOURCE_EXTENSIONS):
            counts["source_opens"] += 1
            if len(counts["source_candidates"]) < 20:
                counts["source_candidates"].append(str(path))

    sys.addaudithook(_audit)
    started = time.monotonic()
    closure = open_empirical_closure(
        closing, expected_root=expected_root
    ).require_trusted()
    bundle = closure.m1_bundle_from_declared_binding()
    profile = closure.field_forge_profile_from_declared_consumer()
    elapsed = time.monotonic() - started
    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    max_rss_bytes = int(max_rss) if sys.platform == "darwin" else int(max_rss) * 1024

    fact_refs = [fact.ref.as_dict() for fact in closure.object_graph.empirical_facts]
    receipt_refs = [
        receipt.ref.as_dict() for receipt in closure.object_graph.discovery_receipts
    ]
    observed = {
        "root_identity": closure.root_identity,
        "closure_identity": closure.closure_identity,
        "trust_state": closure.trust_state,
        "rights_state": closure.manifest["core"]["rights_state"],
        "release_view_type": type(closure.m01_replay_view().c11_release).__name__,
        "m1_bundle_content_hash": bundle.content_hash,
        "m1_bundle_object_id": bundle.object_id,
        "ff_profile_content_hash": profile.content_hash,
        "ff_profile_object_id": profile.object_id,
        "fact_refs": fact_refs,
        "receipt_refs": receipt_refs,
        "source_opens": counts["source_opens"],
        "source_candidates": counts["source_candidates"],
        "closure_opens": counts["closure_opens"],
        "total_opens": counts["total_opens"],
        "elapsed_seconds": elapsed,
        "process_tree_peak_rss_bytes": max_rss_bytes,
        "expected_matched": None,
    }
    if expected_path is not None:
        expected = json.loads(Path(expected_path).read_text(encoding="utf-8"))
        checks = {
            "root_identity": observed["root_identity"],
            "closure_identity": observed["closure_identity"],
            "m1_bundle_content_hash": observed["m1_bundle_content_hash"],
            "m1_bundle_object_id": observed["m1_bundle_object_id"],
            "ff_profile_content_hash": observed["ff_profile_content_hash"],
            "ff_profile_object_id": observed["ff_profile_object_id"],
            "fact_refs": observed["fact_refs"],
            "receipt_refs": observed["receipt_refs"],
        }
        observed["expected_matched"] = all(
            observed[key] == expected[key] for key in checks
        )
    if observed["rights_state"] != RIGHTS_STATE:
        raise SystemExit("cold closure reissued a non-historical rights state")
    return observed


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 4):
        raise SystemExit(
            "usage: test_pyat940_s2f_fresh_process.py <closure> <expected_root> [expected.json]"
        )
    observed = run_cold_consumer(
        argv[1],
        argv[2],
        argv[3] if len(argv) == 4 else None,
    )
    print(json.dumps(observed, sort_keys=True))
    if observed["expected_matched"] is False:
        raise SystemExit("cold consumer identities do not match the native expectation")
    if observed["source_opens"] != 0:
        raise SystemExit("cold consumer opened an original source file")
    return 0


def test_cold_runner_module_import_has_no_side_effects():
    """The CLI helper is importable by pytest without opening any closure."""

    assert callable(run_cold_consumer)
    assert callable(main)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
