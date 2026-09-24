#!/usr/bin/env python3
"""Merge verifier for two independently measured FIABC source-local blocks.

This does NOT recreate or replace the governed six-cell S17 verifier.
It verifies compatibility and completeness of one LiTS A/B/C block plus one
WVS7 A/B/C block and returns them to HQ for split-court adjudication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

EXPECTED_EXECUTION_HEAD = "3d8f2ad62600b6777dcb23a28404a067502e77a0"
EXPECTED_SOURCES = ("LITS_I", "WVS7")
EXPECTED_CANDIDATES = ("A", "B", "C")
TERMINAL_SCHEMA = "RAWLSING_FIABC_SOURCE_LOCAL_TERMINAL@1.0.0"
MERGE_SCHEMA = "RAWLSING_FIABC_SOURCE_SPLIT_MERGE@1.0.0"


class SplitMergeError(RuntimeError):
    pass


def _canon(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
    ).encode("utf-8")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _load_root(root: Path) -> tuple[Mapping[str, Any], Path]:
    root = root.resolve()
    terminal_path = root / "court" / "source_local_terminal.json"
    if not terminal_path.is_file():
        raise SplitMergeError(f"source-local terminal missing: {terminal_path}")
    try:
        doc = json.loads(terminal_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SplitMergeError(f"malformed terminal receipt: {terminal_path}") from exc
    if not isinstance(doc, Mapping):
        raise SplitMergeError("source-local terminal must be a mapping")
    material = {k: v for k, v in doc.items() if k != "receipt_identity"}
    observed_identity = hashlib.sha256(_canon(material)).hexdigest()
    if doc.get("receipt_identity") != observed_identity:
        raise SplitMergeError(f"source-local terminal identity drift: {terminal_path}")
    return doc, terminal_path


def _host_key(doc: Mapping[str, Any]) -> Mapping[str, Any]:
    host = doc.get("host")
    if not isinstance(host, Mapping):
        raise SplitMergeError("source-local terminal host fingerprint missing")
    runtime = host.get("governed_runtime")
    if not isinstance(runtime, Mapping):
        raise SplitMergeError("governed runtime fingerprint missing")
    return {
        "hardware_model": host.get("hardware_model"),
        "cpu_brand": host.get("cpu_brand"),
        "memory_bytes": host.get("memory_bytes"),
        "implementation": runtime.get("implementation"),
        "python": runtime.get("python"),
        "system": runtime.get("system"),
        "machine": runtime.get("machine"),
        "dependency_versions": runtime.get("dependency_versions"),
    }


def _validate_terminal(doc: Mapping[str, Any], expected_source: str) -> None:
    if doc.get("schema") != TERMINAL_SCHEMA:
        raise SplitMergeError(f"{expected_source}: source-local terminal schema drift")
    if doc.get("source") != expected_source:
        raise SplitMergeError(f"{expected_source}: terminal source mismatch")
    if doc.get("execution_head") != EXPECTED_EXECUTION_HEAD:
        raise SplitMergeError(f"{expected_source}: execution head drift")
    if tuple(doc.get("candidate_order", ())) != EXPECTED_CANDIDATES:
        raise SplitMergeError(f"{expected_source}: candidate order drift")
    if doc.get("six_cell_s17_executed") is not False:
        raise SplitMergeError(f"{expected_source}: source-local runner falsely claims S17")
    if doc.get("six_cell_completion_claimed") is not False:
        raise SplitMergeError(f"{expected_source}: source-local runner overclaims six-cell completion")
    if doc.get("measured_synthesis_performed") is not False:
        raise SplitMergeError(f"{expected_source}: measured synthesis occurred before merge")
    terminals = doc.get("candidate_terminals")
    if not isinstance(terminals, Mapping) or tuple(terminals) != EXPECTED_CANDIDATES:
        raise SplitMergeError(f"{expected_source}: candidate terminal inventory drift")
    common = doc.get("common_blockers")
    if not isinstance(common, list):
        raise SplitMergeError(f"{expected_source}: common blocker inventory malformed")


def merge(lits_root: Path, wvs_root: Path) -> Mapping[str, Any]:
    lits, lits_path = _load_root(lits_root)
    wvs, wvs_path = _load_root(wvs_root)
    _validate_terminal(lits, "LITS_I")
    _validate_terminal(wvs, "WVS7")

    if lits.get("current_execution_manifest") != wvs.get("current_execution_manifest"):
        raise SplitMergeError("source blocks were not measured against the same execution manifest")

    lits_host = _host_key(lits)
    wvs_host = _host_key(wvs)
    same_hardware = lits_host == wvs_host

    lits_os = lits.get("host", {}).get("macos_version")
    wvs_os = wvs.get("host", {}).get("macos_version")
    same_os = lits_os == wvs_os

    if not same_hardware:
        raise SplitMergeError(
            "source-block hardware/runtime fingerprints differ; candidate effects would be confounded"
        )

    common_blockers = {
        "LITS_I": list(lits.get("common_blockers", ())),
        "WVS7": list(wvs.get("common_blockers", ())),
    }
    candidate_failures = {
        "LITS_I": list(lits.get("candidate_failure_cells", ())),
        "WVS7": list(wvs.get("candidate_failure_cells", ())),
    }

    status = (
        "READY_FOR_HQ_SPLIT_COURT_ADJUDICATION"
        if not common_blockers["LITS_I"] and not common_blockers["WVS7"]
        else "BLOCKED__SOURCE_LOCAL_COMMON_AUTHORITY"
    )

    payload = {
        "schema": MERGE_SCHEMA,
        "status": status,
        "execution_head": EXPECTED_EXECUTION_HEAD,
        "sources": list(EXPECTED_SOURCES),
        "candidate_order_within_each_source": list(EXPECTED_CANDIDATES),
        "source_terminals": {
            "LITS_I": {
                "path": str(lits_path),
                "sha256": _sha256_file(lits_path),
                "receipt_identity": lits.get("receipt_identity"),
                "candidate_terminals": lits.get("candidate_terminals"),
            },
            "WVS7": {
                "path": str(wvs_path),
                "sha256": _sha256_file(wvs_path),
                "receipt_identity": wvs.get("receipt_identity"),
                "candidate_terminals": wvs.get("candidate_terminals"),
            },
        },
        "host_comparison": {
            "same_hardware_and_governed_runtime": same_hardware,
            "same_macos_version": same_os,
            "LITS_I_macos_version": lits_os,
            "WVS7_macos_version": wvs_os,
            "hardware_runtime_fingerprint": lits_host,
            "cross_source_absolute_physical_metric_comparison_allowed": False,
            "within_source_abc_comparison_preserved": True,
            "note": (
                "Host is nested within source in the split design. Absolute LiTS-vs-WVS "
                "physical timings are never treated as host-neutral, even when macOS "
                "versions match. The admissible physical comparison unit is A/B/C within "
                "each source; HQ synthesizes the two source-local comparisons afterward."
            ),
        },
        "candidate_failures": candidate_failures,
        "common_blockers": common_blockers,
        "six_cell_s17_executed": False,
        "governed_s17_replaced": False,
        "p2_synthesis_authorized": False,
        "architecture_selection_authorized": False,
        "next_required_action": "HQ_ADJUDICATE_SPLIT_COURT_AND_DECIDE_P2_ADMISSIBILITY",
    }
    payload["merge_identity"] = hashlib.sha256(_canon(payload)).hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--lits-root", type=Path, required=True)
    p.add_argument("--wvs-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    payload = merge(args.lits_root, args.wvs_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, sort_keys=True, indent=2))
    return 0 if payload["status"] == "READY_FOR_HQ_SPLIT_COURT_ADJUDICATION" else 3


if __name__ == "__main__":
    raise SystemExit(main())
