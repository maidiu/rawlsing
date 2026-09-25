#!/usr/bin/env python3
"""Hostile merge verifier for FIABC independently measured source-local blocks.

This verifier does not recreate governed S17. It independently revalidates the
terminal, ledger, every selected-source stage receipt, portable repo-live
artifacts, canonical source identity, qualified split-control identity, and
host/runtime compatibility before returning both source blocks to HQ.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE import (
    EXPECTED_CANDIDATES,
    EXPECTED_EXECUTION_HEAD,
    EXPECTED_SOURCE_SHA256,
    EXPECTED_SOURCES,
    PORTABLE_CLOSURE_SCHEMA,
    EvidenceClosureError,
    _canon,
    _identity_checked,
    _load_ledger,
    _sha256_file,
    _stage_receipt_index,
    _validate_terminal,
    validate_control_compatibility_receipt,
    verify_control_binding,
)

MERGE_SCHEMA = "RAWLSING_FIABC_SOURCE_SPLIT_MERGE@2.0.0"
PORTABLE_REL = Path("court/portable_source_evidence_closure.json")
TERMINAL_REL = Path("court/source_local_terminal.json")


class SplitMergeError(RuntimeError):
    pass


def _raise_from_evidence(exc: EvidenceClosureError) -> None:
    raise SplitMergeError(str(exc)) from exc


def _host_key(doc: Mapping[str, Any]) -> Mapping[str, Any]:
    host = doc.get("host")
    if not isinstance(host, Mapping):
        raise SplitMergeError(
            "source-local terminal host fingerprint missing"
        )
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


def _load_portable(root: Path, expected_source: str) -> dict[str, Any]:
    root = root.resolve()
    closure_path = root / PORTABLE_REL
    terminal_path = root / TERMINAL_REL
    if not closure_path.is_file():
        raise SplitMergeError(
            f"{expected_source}: portable evidence closure missing"
        )
    if not terminal_path.is_file():
        raise SplitMergeError(
            f"{expected_source}: source-local terminal missing"
        )

    try:
        closure = _identity_checked(
            closure_path,
            label=f"{expected_source} portable closure",
        )
        terminal = _identity_checked(
            terminal_path,
            label=f"{expected_source} terminal",
        )
        _validate_terminal(terminal, expected_source)
        ledger, ledger_path = _load_ledger(root)
        stage_receipts, repo_artifacts = _stage_receipt_index(
            root, expected_source, ledger, terminal
        )
    except EvidenceClosureError as exc:
        _raise_from_evidence(exc)

    if closure.get("schema") != PORTABLE_CLOSURE_SCHEMA:
        raise SplitMergeError(
            f"{expected_source}: portable closure schema drift"
        )
    if (
        closure.get("status")
        != "PASS__PORTABLE_SOURCE_LOCAL_EVIDENCE_CLOSED"
    ):
        raise SplitMergeError(
            f"{expected_source}: portable closure is not PASS"
        )
    if closure.get("source") != expected_source:
        raise SplitMergeError(
            f"{expected_source}: portable closure source mismatch"
        )
    if (
        closure.get("source_sha256")
        != EXPECTED_SOURCE_SHA256[expected_source]
    ):
        raise SplitMergeError(
            f"{expected_source}: portable canonical source SHA drift"
        )
    if closure.get("execution_head") != EXPECTED_EXECUTION_HEAD:
        raise SplitMergeError(
            f"{expected_source}: portable protected head drift"
        )
    if tuple(closure.get("candidate_order", ())) != EXPECTED_CANDIDATES:
        raise SplitMergeError(
            f"{expected_source}: portable candidate inventory drift"
        )

    for key, expected in (
        ("source_local_only", True),
        ("six_cell_s17_executed", False),
        ("six_cell_completion_claimed", False),
        ("measured_synthesis_performed", False),
        ("p2_synthesis_authorized", False),
        ("nonselected_source_evidence_included", False),
        (
            "all_repo_live_mutations_attributable_to_selected_source_ledger",
            True,
        ),
        (
            "portable_packaging_performed_after_source_terminal",
            True,
        ),
        ("portable_packaging_is_measured_candidate_work", False),
        ("raw_source_bytes_copied", False),
    ):
        if closure.get(key) is not expected:
            raise SplitMergeError(
                f"{expected_source}: portable invariant drift: {key}"
            )

    terminal_binding = closure.get("source_terminal")
    if not isinstance(terminal_binding, Mapping):
        raise SplitMergeError(
            f"{expected_source}: portable terminal binding missing"
        )
    if terminal_binding.get("path") != TERMINAL_REL.as_posix():
        raise SplitMergeError(
            f"{expected_source}: portable terminal path drift"
        )
    if terminal_binding.get("sha256") != _sha256_file(terminal_path):
        raise SplitMergeError(
            f"{expected_source}: portable terminal hash drift"
        )
    if (
        terminal_binding.get("receipt_identity")
        != terminal.get("receipt_identity")
    ):
        raise SplitMergeError(
            f"{expected_source}: terminal identity disagrees with closure"
        )

    ledger_binding = closure.get("stage_ledger")
    if not isinstance(ledger_binding, Mapping):
        raise SplitMergeError(
            f"{expected_source}: portable ledger binding missing"
        )
    observed_ledger_sha = _sha256_file(ledger_path)
    if ledger_binding.get("sha256") != observed_ledger_sha:
        raise SplitMergeError(
            f"{expected_source}: portable ledger hash drift"
        )
    if terminal.get("stage_ledger_sha256") != observed_ledger_sha:
        raise SplitMergeError(
            f"{expected_source}: terminal ledger hash drift"
        )
    if (
        ledger_binding.get("stage_count")
        != len(ledger.get("stages", {}))
    ):
        raise SplitMergeError(
            f"{expected_source}: portable ledger stage-count drift"
        )

    if (
        closure.get("current_execution_manifest")
        != terminal.get("current_execution_manifest")
    ):
        raise SplitMergeError(
            f"{expected_source}: closure/terminal manifest mismatch"
        )
    if (
        terminal.get("current_execution_manifest")
        != ledger.get("continuation_map")
    ):
        raise SplitMergeError(
            f"{expected_source}: terminal/ledger manifest mismatch"
        )

    if closure.get("stage_receipts") != stage_receipts:
        raise SplitMergeError(
            f"{expected_source}: portable stage-receipt index does not "
            "match independently verified ledger"
        )

    portable_repo = closure.get("repo_live_evidence")
    if not isinstance(portable_repo, list):
        raise SplitMergeError(
            f"{expected_source}: portable repo-live evidence index malformed"
        )
    expected_repo = {
        item["repo_relative_path"]: item
        for item in repo_artifacts
    }
    observed_repo: dict[str, Mapping[str, Any]] = {}
    for item in portable_repo:
        if not isinstance(item, Mapping):
            raise SplitMergeError(
                f"{expected_source}: portable repo-live entry malformed"
            )
        rel = item.get("repo_relative_path")
        if not isinstance(rel, str) or rel not in expected_repo:
            raise SplitMergeError(
                f"{expected_source}: portable repo-live artifact is "
                f"not ledger-bound: {rel}"
            )
        if rel in observed_repo:
            raise SplitMergeError(
                f"{expected_source}: duplicate portable repo-live artifact: "
                f"{rel}"
            )
        expected = expected_repo[rel]
        if item.get("sha256") != expected["sha256"]:
            raise SplitMergeError(
                f"{expected_source}: repo-live ledger hash disagreement: "
                f"{rel}"
            )
        path_raw = item.get("portable_path")
        if not isinstance(path_raw, str):
            raise SplitMergeError(
                f"{expected_source}: portable copy path missing: {rel}"
            )
        copy_path = (root / path_raw).resolve()
        if root != copy_path and root not in copy_path.parents:
            raise SplitMergeError(
                f"{expected_source}: portable copy escapes source root: "
                f"{rel}"
            )
        if not copy_path.is_file():
            raise SplitMergeError(
                f"{expected_source}: portable copy missing: {rel}"
            )
        observed = _sha256_file(copy_path)
        if (
            observed != expected["sha256"]
            or item.get("portable_sha256") != observed
        ):
            raise SplitMergeError(
                f"{expected_source}: portable copy hash drift: {rel}"
            )
        observed_repo[rel] = item
    if set(observed_repo) != set(expected_repo):
        missing = sorted(set(expected_repo) - set(observed_repo))
        raise SplitMergeError(
            f"{expected_source}: portable repo-live closure omits "
            f"ledger artifacts: {missing}"
        )

    delta = closure.get("repo_live_delta_paths")
    if not isinstance(delta, list):
        raise SplitMergeError(
            f"{expected_source}: repo-live delta inventory malformed"
        )
    delta_set = set(str(x) for x in delta)
    included_changed = {
        rel
        for rel, item in observed_repo.items()
        if item.get("change_type") in {"CREATED", "MODIFIED"}
    }
    if delta_set != included_changed:
        raise SplitMergeError(
            f"{expected_source}: repo-live changed-path inventory "
            "disagrees with portable copies"
        )

    binding = closure.get("control_binding")
    if not isinstance(binding, Mapping):
        raise SplitMergeError(
            f"{expected_source}: portable control binding missing"
        )
    binding_rel = binding.get("portable_path")
    if not isinstance(binding_rel, str):
        raise SplitMergeError(
            f"{expected_source}: portable control binding path missing"
        )
    binding_path = (root / binding_rel).resolve()
    if root != binding_path and root not in binding_path.parents:
        raise SplitMergeError(
            f"{expected_source}: portable control binding escapes root"
        )
    if not binding_path.is_file():
        raise SplitMergeError(
            f"{expected_source}: portable control binding file missing"
        )
    if binding.get("portable_sha256") != _sha256_file(binding_path):
        raise SplitMergeError(
            f"{expected_source}: portable control binding hash drift"
        )
    try:
        binding_doc = _identity_checked(
            binding_path,
            label=f"{expected_source} control binding",
        )
    except EvidenceClosureError as exc:
        _raise_from_evidence(exc)
    if (
        binding.get("binding_receipt_identity")
        != binding_doc.get("receipt_identity")
    ):
        raise SplitMergeError(
            f"{expected_source}: control-binding identity disagreement"
        )
    if (
        binding.get("qualified_implementation_head")
        != binding_doc.get("qualified_implementation_head")
    ):
        raise SplitMergeError(
            f"{expected_source}: qualified-control identity disagreement"
        )
    if (
        binding.get("protected_execution_head")
        != EXPECTED_EXECUTION_HEAD
    ):
        raise SplitMergeError(
            f"{expected_source}: control binding protected head drift"
        )

    return {
        "root": root,
        "closure_path": closure_path,
        "closure": closure,
        "terminal_path": terminal_path,
        "terminal": terminal,
        "ledger_path": ledger_path,
        "ledger": ledger,
        "binding_path": binding_path,
        "binding_doc": binding_doc,
    }


def _validate_control_pair(
    lits: Mapping[str, Any],
    wvs: Mapping[str, Any],
    *,
    control_root: Path,
    compatibility_receipt: Path | None,
) -> Mapping[str, Any]:
    lits_q = lits["binding_doc"].get(
        "qualified_implementation_head"
    )
    wvs_q = wvs["binding_doc"].get(
        "qualified_implementation_head"
    )
    lits_terminal_head = lits["closure"].get(
        "terminal_control_head"
    )
    wvs_terminal_head = wvs["closure"].get(
        "terminal_control_head"
    )

    default_compatible = (
        lits_q == wvs_q
        and lits_terminal_head == lits_q
        and wvs_terminal_head == wvs_q
        and _sha256_file(lits["binding_path"])
        == _sha256_file(wvs["binding_path"])
    )

    compatibility = None
    if not default_compatible:
        if compatibility_receipt is None:
            raise SplitMergeError(
                "source halves do not share one exact qualified control "
                "identity; explicit compatibility receipt required"
            )
        try:
            compatibility = validate_control_compatibility_receipt(
                path=compatibility_receipt,
                lits_qualified_head=str(lits_q),
                wvs_qualified_head=str(wvs_q),
                wvs_terminal_control_head=(
                    str(wvs_terminal_head)
                    if wvs_terminal_head is not None
                    else None
                ),
            )
        except EvidenceClosureError as exc:
            _raise_from_evidence(exc)
        if lits_terminal_head != lits_q:
            raise SplitMergeError(
                "LiTS control mismatch cannot be grandfathered"
            )
        if (
            compatibility.get("source_exception")
            != "WVS7_LEGACY_RUN5_ONLY"
        ):
            raise SplitMergeError(
                "compatibility receipt is not scoped to legacy WVS RUN5"
            )

    try:
        verified = verify_control_binding(
            binding_path=lits["binding_path"],
            control_root=control_root,
            require_clean=True,
        )
    except EvidenceClosureError as exc:
        _raise_from_evidence(exc)
    if verified["qualified_implementation_head"] != lits_q:
        raise SplitMergeError(
            "current merge verifier is not bound to LiTS qualified control"
        )

    return {
        "default_same_qualified_control": default_compatible,
        "explicit_compatibility_receipt_used": (
            compatibility is not None
        ),
        "compatibility_receipt_sha256": (
            _sha256_file(compatibility_receipt)
            if compatibility_receipt is not None
            else None
        ),
        "qualified_control": verified,
        "LITS_I_terminal_control_head": lits_terminal_head,
        "WVS7_terminal_control_head": wvs_terminal_head,
        "LITS_I_qualified_control_head": lits_q,
        "WVS7_qualified_control_head": wvs_q,
    }


def merge(
    lits_root: Path,
    wvs_root: Path,
    *,
    control_root: Path,
    compatibility_receipt: Path | None = None,
) -> Mapping[str, Any]:
    lits = _load_portable(lits_root, "LITS_I")
    wvs = _load_portable(wvs_root, "WVS7")

    if (
        lits["terminal"].get("current_execution_manifest")
        != wvs["terminal"].get("current_execution_manifest")
    ):
        raise SplitMergeError(
            "source blocks were not measured against the same exact "
            "execution manifest"
        )

    control = _validate_control_pair(
        lits,
        wvs,
        control_root=control_root,
        compatibility_receipt=compatibility_receipt,
    )

    lits_host = _host_key(lits["terminal"])
    wvs_host = _host_key(wvs["terminal"])
    same_hardware = lits_host == wvs_host
    if not same_hardware:
        raise SplitMergeError(
            "source-block hardware/runtime fingerprints differ; "
            "within-source candidate effects cannot be combined under "
            "current split-host law"
        )

    lits_os = lits["terminal"].get("host", {}).get(
        "macos_version"
    )
    wvs_os = wvs["terminal"].get("host", {}).get(
        "macos_version"
    )
    same_os = lits_os == wvs_os

    common_blockers = {
        "LITS_I": list(
            lits["terminal"].get("common_blockers", ())
        ),
        "WVS7": list(
            wvs["terminal"].get("common_blockers", ())
        ),
    }
    candidate_failures = {
        "LITS_I": list(
            lits["terminal"].get("candidate_failure_cells", ())
        ),
        "WVS7": list(
            wvs["terminal"].get("candidate_failure_cells", ())
        ),
    }

    status = (
        "READY_FOR_HQ_SPLIT_COURT_ADJUDICATION"
        if (
            not common_blockers["LITS_I"]
            and not common_blockers["WVS7"]
        )
        else "BLOCKED__SOURCE_LOCAL_COMMON_AUTHORITY"
    )

    payload = {
        "schema": MERGE_SCHEMA,
        "status": status,
        "execution_head": EXPECTED_EXECUTION_HEAD,
        "sources": list(EXPECTED_SOURCES),
        "candidate_order_within_each_source": list(
            EXPECTED_CANDIDATES
        ),
        "source_evidence": {
            "LITS_I": {
                "portable_closure_path": str(
                    lits["closure_path"]
                ),
                "portable_closure_sha256": _sha256_file(
                    lits["closure_path"]
                ),
                "portable_closure_identity": lits[
                    "closure"
                ].get("receipt_identity"),
                "source_terminal_sha256": _sha256_file(
                    lits["terminal_path"]
                ),
                "stage_ledger_sha256": _sha256_file(
                    lits["ledger_path"]
                ),
                "stage_receipt_count": len(
                    lits["closure"].get(
                        "stage_receipts", ()
                    )
                ),
                "portable_repo_live_artifact_count": len(
                    lits["closure"].get(
                        "repo_live_evidence", ()
                    )
                ),
            },
            "WVS7": {
                "portable_closure_path": str(
                    wvs["closure_path"]
                ),
                "portable_closure_sha256": _sha256_file(
                    wvs["closure_path"]
                ),
                "portable_closure_identity": wvs[
                    "closure"
                ].get("receipt_identity"),
                "source_terminal_sha256": _sha256_file(
                    wvs["terminal_path"]
                ),
                "stage_ledger_sha256": _sha256_file(
                    wvs["ledger_path"]
                ),
                "stage_receipt_count": len(
                    wvs["closure"].get(
                        "stage_receipts", ()
                    )
                ),
                "portable_repo_live_artifact_count": len(
                    wvs["closure"].get(
                        "repo_live_evidence", ()
                    )
                ),
            },
        },
        "control_compatibility": control,
        "host_comparison": {
            "same_hardware_and_governed_runtime": same_hardware,
            "same_macos_version": same_os,
            "LITS_I_macos_version": lits_os,
            "WVS7_macos_version": wvs_os,
            "hardware_runtime_fingerprint": lits_host,
            "cross_source_absolute_physical_metric_comparison_allowed": False,
            "within_source_abc_comparison_preserved": True,
            "note": (
                "Host remains nested within source. Absolute LiTS-vs-WVS "
                "physical measurements are permanently non-comparable "
                "even on nominally identical hardware/runtime. "
                "Admissible physical comparison remains A/B/C within "
                "each source, subject to HQ adjudication."
            ),
        },
        "candidate_failures": candidate_failures,
        "common_blockers": common_blockers,
        "portable_evidence_independently_verified": True,
        "no_nonselected_source_evidence_verified": True,
        "six_cell_s17_executed": False,
        "governed_s17_replaced": False,
        "six_cell_completion_claimed": False,
        "measured_synthesis_performed": False,
        "p2_synthesis_authorized": False,
        "architecture_selection_authorized": False,
        "next_required_action": (
            "HQ_ADJUDICATE_SPLIT_COURT_AND_DECIDE_P2_ADMISSIBILITY"
        ),
    }
    payload["merge_identity"] = hashlib.sha256(
        _canon(payload)
    ).hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--lits-root", type=Path, required=True)
    p.add_argument("--wvs-root", type=Path, required=True)
    p.add_argument("--control-root", type=Path, required=True)
    p.add_argument("--compatibility-receipt", type=Path)
    p.add_argument("--output", type=Path, required=True)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    payload = merge(
        args.lits_root,
        args.wvs_root,
        control_root=args.control_root,
        compatibility_receipt=args.compatibility_receipt,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, sort_keys=True, indent=2))
    return (
        0
        if payload["status"]
        == "READY_FOR_HQ_SPLIT_COURT_ADJUDICATION"
        else 3
    )


if __name__ == "__main__":
    raise SystemExit(main())
