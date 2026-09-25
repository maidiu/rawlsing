"""Source-free hostile tests for FIABC split R2 Worker D evidence/merge law.

No raw LiTS/WVS source is opened or hashed. No candidate process is imported or
launched. Fixtures contain only synthetic ledger/receipt/control-plane objects.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


CONTROL_ROOT = Path(__file__).resolve().parents[2]
LAUNCHERS = CONTROL_ROOT / "HQ_HANDOFF" / "launchers"
EVIDENCE_PATH = LAUNCHERS / "FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py"
MERGE_PATH = LAUNCHERS / "FIABC_SOURCE_LOCAL_SPLIT_MERGE.py"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


EVIDENCE = _load("fiabc_split_r2_d_evidence", EVIDENCE_PATH)
sys.modules["FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE"] = EVIDENCE
MERGE = _load("fiabc_split_r2_d_merge", MERGE_PATH)


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _manifest_identity():
    return {
        "schema": (
            "RAWLSING_FIABC_CURRENT_SIX_CELL_EXECUTION_MANIFEST@1.0.0"
        ),
        "sha256": "a" * 64,
        "git_blob_sha1": EVIDENCE.EXPECTED_MANIFEST_GIT_BLOB_SHA1,
    }


def _host(os_version="13.2.1", hardware="MacBookPro15,1"):
    return {
        "governed_runtime": {
            "implementation": "CPython",
            "python": "3.11.3",
            "system": "Darwin",
            "machine": "x86_64",
            "dependency_versions": {
                "pyreadstat": "1.3.6",
                "pyarrow": "25.0.1",
                "pandas": "2.3.1",
                "numpy": "2.3.2",
            },
        },
        "macos_version": os_version,
        "hardware_model": hardware,
        "cpu_brand": "Intel synthetic",
        "memory_bytes": 17179869184,
    }


def _make_control_repo(tmp: Path):
    root = tmp / "control"
    for rel in EVIDENCE.CONTROL_PATHS:
        src = CONTROL_ROOT / rel
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    _git(root, "init")
    _git(root, "config", "user.email", "worker-d@example.invalid")
    _git(root, "config", "user.name", "Worker D")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "qualified control fixture")
    head = _git(root, "rev-parse", "HEAD")
    binding = tmp / "control_binding.json"
    EVIDENCE.create_control_binding(
        control_root=root,
        qualified_implementation_head=head,
        output_path=binding,
        qualification_return_ref="SYNTHETIC_SOURCE_FREE_QUALIFICATION",
    )
    return root, head, binding


def _make_source_root(
    root: Path,
    source: str,
    binding_path: Path,
    binding_summary,
    *,
    terminal_control_head: str,
    os_version="13.2.1",
    hardware="MacBookPro15,1",
):
    root.mkdir(parents=True, exist_ok=True)
    stages = {}
    for address in EVIDENCE._expected_stage_addresses(source):
        parts = address.split("/")
        receipt_rel = (
            f"cells/{parts[0]}/{parts[1]}/receipts/"
            f"{parts[2].lower()}.json"
        )
        receipt_path = root / receipt_rel
        _write_json(
            receipt_path,
            {"stage": address, "synthetic": True},
        )
        stages[address] = {
            "stage_id": parts[2],
            "source": source,
            "candidate": parts[1],
            "input_identity_hash": "b" * 64,
            "state": "TERMINAL",
            "output_artifact_hashes": {},
            "receipt_path": receipt_rel,
            "receipt_hash": _sha(receipt_path),
            "verifier_completion": True,
            "terminal_disposition": "PASS",
            "next_stage": "__SYNTHETIC_NEXT__",
        }
    ledger = {
        "schema": EVIDENCE.LEDGER_SCHEMA,
        "continuation_map": _manifest_identity(),
        "p2x_branch": EVIDENCE.EXPECTED_EXECUTION_BRANCH,
        "p2x_resume_head": "c" * 40,
        "source_order": list(EVIDENCE.EXPECTED_SOURCES),
        "candidate_order": list(EVIDENCE.EXPECTED_CANDIDATES),
        "source_identities": {
            source: {
                "sha256": EVIDENCE.EXPECTED_SOURCE_SHA256[source],
                "size": 123,
            }
        },
        "stages": stages,
    }
    ledger_path = root / "ee_p2x_stage_ledger.json"
    _write_json(ledger_path, ledger)
    ledger_sha = _sha(ledger_path)

    candidate_terminals = {}
    for candidate in EVIDENCE.EXPECTED_CANDIDATES:
        address = (
            f"{source}/{candidate}/"
            f"{EVIDENCE.STAGE_CATALOG[-1]}"
        )
        candidate_terminals[candidate] = {
            "address": address,
            "terminal_disposition": "PASS",
            "receipt_hash": stages[address]["receipt_hash"],
        }
    terminal = {
        "schema": EVIDENCE.TERMINAL_SCHEMA,
        "status": (
            "SOURCE_BLOCK_SEQUENCE_COMPLETE__ALL_THREE_CELLS_TERMINAL"
        ),
        "source": source,
        "source_sha256": EVIDENCE.EXPECTED_SOURCE_SHA256[source],
        "candidate_order": list(EVIDENCE.EXPECTED_CANDIDATES),
        "candidate_terminals": candidate_terminals,
        "candidate_failure_cells": [],
        "common_blockers": [],
        "incomplete_stages": [],
        "stage_ledger_sha256": ledger_sha,
        "execution_branch": EVIDENCE.EXPECTED_EXECUTION_BRANCH,
        "execution_head": EVIDENCE.EXPECTED_EXECUTION_HEAD,
        "current_execution_manifest": _manifest_identity(),
        "host": _host(
            os_version=os_version,
            hardware=hardware,
        ),
        "control_runner": {
            "control_head": terminal_control_head,
            "launcher_sha256": binding_summary[
                "bound_files"
            ][EVIDENCE.CONTROL_PATHS[0]],
            "source_local_driver_sha256": binding_summary[
                "bound_files"
            ][EVIDENCE.CONTROL_PATHS[1]],
        },
        "source_local_only": True,
        "six_cell_s17_executed": False,
        "six_cell_completion_claimed": False,
        "measured_synthesis_performed": False,
        "p2_synthesis_authorized": False,
        "next_required_action": (
            "MERGE_WITH_OTHER_SOURCE_BLOCK__HQ_ADJUDICATION_REQUIRED"
        ),
    }
    terminal_path = (
        root / "court" / "source_local_terminal.json"
    )
    terminal = EVIDENCE._write_identified_json(
        terminal_path,
        terminal,
    )

    stage_receipts, repo_artifacts = (
        EVIDENCE._stage_receipt_index(
            root, source, ledger, terminal
        )
    )
    assert repo_artifacts == []

    portable = root / "court" / "portable_evidence"
    portable.mkdir(parents=True, exist_ok=True)
    binding_copy = portable / "control_binding.json"
    shutil.copyfile(binding_path, binding_copy)
    baseline_path = portable / "repo_live_baseline.json"
    baseline = EVIDENCE._write_identified_json(
        baseline_path,
        {
            "schema": EVIDENCE.REPO_BASELINE_SCHEMA,
            "status": "PASS__EXACT_HEAD_LIVE_EVIDENCE_BASELINE",
            "source": source,
            "execution_branch": EVIDENCE.EXPECTED_EXECUTION_BRANCH,
            "execution_head": EVIDENCE.EXPECTED_EXECUTION_HEAD,
            "live_evidence_root": (
                EVIDENCE.LIVE_EVIDENCE_REL.as_posix()
            ),
            "tracked_head_inventory": {},
            "worktree_inventory": {},
            "nonselected_source_mutations_present": False,
            "raw_source_access_performed": False,
            "candidate_processes_started": 0,
            "measured_execution_performed": False,
        },
    )
    closure = {
        "schema": EVIDENCE.PORTABLE_CLOSURE_SCHEMA,
        "status": (
            "PASS__PORTABLE_SOURCE_LOCAL_EVIDENCE_CLOSED"
        ),
        "source": source,
        "source_sha256": EVIDENCE.EXPECTED_SOURCE_SHA256[source],
        "execution_branch": EVIDENCE.EXPECTED_EXECUTION_BRANCH,
        "execution_head": EVIDENCE.EXPECTED_EXECUTION_HEAD,
        "current_execution_manifest": _manifest_identity(),
        "candidate_order": list(EVIDENCE.EXPECTED_CANDIDATES),
        "source_terminal": {
            "path": "court/source_local_terminal.json",
            "sha256": _sha(terminal_path),
            "receipt_identity": terminal["receipt_identity"],
            "status": terminal["status"],
        },
        "stage_ledger": {
            "path": "ee_p2x_stage_ledger.json",
            "sha256": ledger_sha,
            "stage_count": len(stages),
        },
        "stage_receipts": stage_receipts,
        "repo_live_baseline": {
            "path": str(baseline_path.relative_to(root)),
            "sha256": _sha(baseline_path),
            "receipt_identity": baseline["receipt_identity"],
        },
        "repo_live_evidence": [],
        "repo_live_delta_paths": [],
        (
            "all_repo_live_mutations_attributable_to_"
            "selected_source_ledger"
        ): True,
        "nonselected_source_evidence_included": False,
        "control_binding": {
            **binding_summary,
            "portable_path": str(
                binding_copy.relative_to(root)
            ),
            "portable_sha256": _sha(binding_copy),
        },
        "terminal_control_head": terminal_control_head,
        "terminal_control_legacy_allowed_for_packaging": (
            terminal_control_head
            != binding_summary["observed_control_checkout_head"]
        ),
        "host": terminal["host"],
        "source_local_only": True,
        "six_cell_s17_executed": False,
        "six_cell_completion_claimed": False,
        "measured_synthesis_performed": False,
        "p2_synthesis_authorized": False,
        "portable_packaging_performed_after_source_terminal": True,
        "portable_packaging_is_measured_candidate_work": False,
        "raw_source_bytes_copied": False,
    }
    EVIDENCE._write_identified_json(
        (
            root
            / "court"
            / "portable_source_evidence_closure.json"
        ),
        closure,
    )
    return root


class WorkerDPortableEvidenceTests(unittest.TestCase):
    def test_exact_source_stage_universe_is_51_and_never_crosses_source_or_s17(
        self,
    ):
        for source in EVIDENCE.EXPECTED_SOURCES:
            addresses = EVIDENCE._expected_stage_addresses(
                source
            )
            self.assertEqual(len(addresses), 51)
            self.assertTrue(
                all(
                    a.startswith(source + "/")
                    for a in addresses
                )
            )
            self.assertFalse(
                any(
                    "S17" in a or a.startswith("COURT/")
                    for a in addresses
                )
            )

    def test_stage_receipt_index_rejects_foreign_running_and_hash_drift(
        self,
    ):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = "LITS_I"
            binding = {
                "schema": EVIDENCE.TERMINAL_SCHEMA,
                "status": "BLOCKED__COMMON_COURT_AUTHORITY",
                "source": source,
                "source_sha256": (
                    EVIDENCE.EXPECTED_SOURCE_SHA256[source]
                ),
                "candidate_order": list(
                    EVIDENCE.EXPECTED_CANDIDATES
                ),
                "candidate_terminals": {
                    c: {
                        "address": (
                            f"{source}/{c}/"
                            f"{EVIDENCE.STAGE_CATALOG[-1]}"
                        ),
                        "terminal_disposition": (
                            "INCOMPLETE_DUE_COMMON_COURT_BLOCKER"
                        ),
                        "receipt_hash": None,
                    }
                    for c in EVIDENCE.EXPECTED_CANDIDATES
                },
                "candidate_failure_cells": [],
                "common_blockers": [],
                "incomplete_stages": list(
                    EVIDENCE._expected_stage_addresses(
                        source
                    )
                ),
            }
            ledger = {
                "stages": {
                    (
                        "WVS7/A/"
                        "S01_CANDIDATE_PREPARATION_BUILD"
                    ): {}
                }
            }
            with self.assertRaisesRegex(
                EVIDENCE.EvidenceClosureError,
                "foreign stages",
            ):
                EVIDENCE._stage_receipt_index(
                    root, source, ledger, binding
                )

            address = (
                "LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY"
            )
            receipt = (
                root
                / "cells/LITS_I/A/receipts/s00.json"
            )
            _write_json(receipt, {"stage": address})
            ledger = {
                "stages": {
                    address: {
                        "state": "RUNNING",
                        "terminal_disposition": None,
                        "verifier_completion": False,
                        "receipt_path": str(
                            receipt.relative_to(root)
                        ),
                        "receipt_hash": _sha(receipt),
                        "output_artifact_hashes": {},
                    }
                }
            }
            binding["incomplete_stages"] = [
                x
                for x in EVIDENCE._expected_stage_addresses(
                    source
                )
                if x != address
            ]
            with self.assertRaisesRegex(
                EVIDENCE.EvidenceClosureError,
                "RUNNING",
            ):
                EVIDENCE._stage_receipt_index(
                    root, source, ledger, binding
                )

            ledger["stages"][address].update({
                "state": "TERMINAL",
                "terminal_disposition": "PASS",
                "verifier_completion": True,
                "receipt_hash": "0" * 64,
            })
            with self.assertRaisesRegex(
                EVIDENCE.EvidenceClosureError,
                "receipt hash drift",
            ):
                EVIDENCE._stage_receipt_index(
                    root, source, ledger, binding
                )

    def test_control_binding_is_non_circular_and_rejects_hash_drift_and_dirty_checkout(
        self,
    ):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            root, head, binding = _make_control_repo(
                tmp
            )
            verified = EVIDENCE.verify_control_binding(
                binding_path=binding,
                control_root=root,
                require_clean=True,
            )
            self.assertEqual(
                verified["qualified_implementation_head"],
                head,
            )
            self.assertEqual(
                set(verified["bound_files"]),
                set(EVIDENCE.CONTROL_PATHS),
            )

            target = root / EVIDENCE.CONTROL_PATHS[1]
            original = target.read_text(encoding="utf-8")
            target.write_text(
                original + "\n# drift\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                EVIDENCE.EvidenceClosureError,
                "hash drift",
            ):
                EVIDENCE.verify_control_binding(
                    binding_path=binding,
                    control_root=root,
                    require_clean=False,
                )
            target.write_text(
                original,
                encoding="utf-8",
            )
            (root / "untracked.txt").write_text(
                "dirty\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                EVIDENCE.EvidenceClosureError,
                "dirty",
            ):
                EVIDENCE.verify_control_binding(
                    binding_path=binding,
                    control_root=root,
                    require_clean=True,
                )

            _git(root, "checkout", "-b", "wrong-control-branch")
            with self.assertRaisesRegex(
                EVIDENCE.EvidenceClosureError,
                "wrong control branch",
            ):
                EVIDENCE.verify_control_binding(
                    binding_path=binding,
                    control_root=root,
                    require_clean=False,
                )

    def test_orchestration_failure_receipt_is_fail_closed_and_never_candidate_local(
        self,
    ):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            control, _, binding = _make_control_repo(
                tmp
            )
            work = tmp / "work"
            work.mkdir()
            _write_json(
                work / "ee_p2x_stage_ledger.json",
                {
                    "stages": {
                        (
                            "LITS_I/A/"
                            "S01_CANDIDATE_PREPARATION_BUILD"
                        ): {
                            "state": "RUNNING"
                        }
                    }
                },
            )
            (
                work / "fiabc_driver_progress.jsonl"
            ).write_text(
                '{"state":"START"}\n',
                encoding="utf-8",
            )
            receipt = (
                EVIDENCE.write_orchestration_failure_receipt(
                    work_root=work,
                    source="LITS_I",
                    measured_driver_exit_code=1,
                    control_root=control,
                    control_binding_path=binding,
                )
            )
            self.assertEqual(
                receipt["measured_driver_exit_code"],
                1,
            )
            self.assertTrue(
                receipt[
                    "candidate_stage_ledger_entry_exists"
                ]
            )
            self.assertFalse(
                receipt[
                    "candidate_failure_inferred_from_process_exit"
                ]
            )
            self.assertFalse(
                receipt["automatic_retry_authorized"]
            )
            self.assertEqual(
                receipt["PRESERVE_WORK_ROOT"],
                str(work.resolve()),
            )
            self.assertFalse(
                receipt["source_local_terminal_present"]
            )

    def test_merge_revalidates_full_ledger_and_accepts_only_same_qualified_control_by_default(
        self,
    ):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            control, head, binding = _make_control_repo(
                tmp
            )
            summary = EVIDENCE.verify_control_binding(
                binding_path=binding,
                control_root=control,
                require_clean=True,
            )
            lits = _make_source_root(
                tmp / "lits",
                "LITS_I",
                binding,
                summary,
                terminal_control_head=head,
            )
            wvs = _make_source_root(
                tmp / "wvs",
                "WVS7",
                binding,
                summary,
                terminal_control_head=head,
                os_version="13.6.7",
            )
            merged = MERGE.merge(
                lits,
                wvs,
                control_root=control,
            )
            self.assertEqual(
                merged["status"],
                "READY_FOR_HQ_SPLIT_COURT_ADJUDICATION",
            )
            self.assertTrue(
                merged[
                    "portable_evidence_independently_verified"
                ]
            )
            self.assertTrue(
                merged["host_comparison"][
                    "same_hardware_and_governed_runtime"
                ]
            )
            self.assertFalse(
                merged["host_comparison"][
                    "same_macos_version"
                ]
            )
            self.assertFalse(
                merged["host_comparison"][
                    "cross_source_absolute_physical_metric_"
                    "comparison_allowed"
                ]
            )
            self.assertFalse(
                merged["six_cell_s17_executed"]
            )
            self.assertFalse(
                merged["p2_synthesis_authorized"]
            )

            receipt = next(
                (
                    lits
                    / "cells/LITS_I/A/receipts"
                ).glob("*.json")
            )
            receipt.write_text(
                '{"tampered":true}\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                MERGE.SplitMergeError,
                "receipt hash drift",
            ):
                MERGE.merge(
                    lits,
                    wvs,
                    control_root=control,
                )

    def test_merge_rejects_canonical_source_drift_running_stage_and_hardware_mismatch(
        self,
    ):
        for mode in ("source", "running", "hardware"):
            with self.subTest(mode=mode):
                with tempfile.TemporaryDirectory() as td:
                    tmp = Path(td)
                    control, head, binding = (
                        _make_control_repo(tmp)
                    )
                    summary = (
                        EVIDENCE.verify_control_binding(
                            binding_path=binding,
                            control_root=control,
                            require_clean=True,
                        )
                    )
                    lits = _make_source_root(
                        tmp / "lits",
                        "LITS_I",
                        binding,
                        summary,
                        terminal_control_head=head,
                    )
                    wvs = _make_source_root(
                        tmp / "wvs",
                        "WVS7",
                        binding,
                        summary,
                        terminal_control_head=head,
                        hardware=(
                            "OtherMac"
                            if mode == "hardware"
                            else "MacBookPro15,1"
                        ),
                    )
                    if mode == "source":
                        path = (
                            lits
                            / "court"
                            / "source_local_terminal.json"
                        )
                        doc = json.loads(
                            path.read_text(
                                encoding="utf-8"
                            )
                        )
                        doc["source_sha256"] = (
                            "0" * 64
                        )
                        doc.pop(
                            "receipt_identity",
                            None,
                        )
                        EVIDENCE._write_identified_json(
                            path,
                            doc,
                        )
                        with self.assertRaisesRegex(
                            MERGE.SplitMergeError,
                            "canonical source SHA",
                        ):
                            MERGE.merge(
                                lits,
                                wvs,
                                control_root=control,
                            )
                    elif mode == "running":
                        path = (
                            lits
                            / "ee_p2x_stage_ledger.json"
                        )
                        doc = json.loads(
                            path.read_text(
                                encoding="utf-8"
                            )
                        )
                        key = next(
                            iter(doc["stages"])
                        )
                        doc["stages"][key][
                            "state"
                        ] = "RUNNING"
                        _write_json(path, doc)
                        with self.assertRaisesRegex(
                            MERGE.SplitMergeError,
                            "RUNNING",
                        ):
                            MERGE.merge(
                                lits,
                                wvs,
                                control_root=control,
                            )
                    else:
                        with self.assertRaisesRegex(
                            MERGE.SplitMergeError,
                            "hardware/runtime",
                        ):
                            MERGE.merge(
                                lits,
                                wvs,
                                control_root=control,
                            )

    def test_merge_requires_explicit_legacy_wvs_compatibility_and_never_silent_grandfathers(
        self,
    ):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            control, head, binding = _make_control_repo(
                tmp
            )
            summary = EVIDENCE.verify_control_binding(
                binding_path=binding,
                control_root=control,
                require_clean=True,
            )
            lits = _make_source_root(
                tmp / "lits",
                "LITS_I",
                binding,
                summary,
                terminal_control_head=head,
            )
            wvs = _make_source_root(
                tmp / "wvs",
                "WVS7",
                binding,
                summary,
                terminal_control_head=(
                    EVIDENCE.LEGACY_WVS_RUN5_CONTROL_HEAD
                ),
            )
            with self.assertRaisesRegex(
                MERGE.SplitMergeError,
                "explicit compatibility receipt required",
            ):
                MERGE.merge(
                    lits,
                    wvs,
                    control_root=control,
                )

            compat_path = (
                tmp / "compatibility.json"
            )
            EVIDENCE._write_identified_json(
                compat_path,
                {
                    "schema": (
                        EVIDENCE.CONTROL_COMPATIBILITY_SCHEMA
                    ),
                    "status": (
                        "PASS__EXPLICIT_CONTROL_COMPATIBILITY_"
                        "ADJUDICATED"
                    ),
                    "source_exception": (
                        "WVS7_LEGACY_RUN5_ONLY"
                    ),
                    "LITS_I_qualified_control_head": (
                        head
                    ),
                    "WVS7_qualified_control_head": (
                        head
                    ),
                    "WVS7_terminal_control_head": (
                        EVIDENCE.LEGACY_WVS_RUN5_CONTROL_HEAD
                    ),
                    (
                        "candidate_execution_semantics_"
                        "unchanged"
                    ): True,
                    "portable_evidence_reverified": True,
                    (
                        "physical_metric_admissibility_"
                        "explicitly_adjudicated"
                    ): True,
                    "silent_grandfathering": False,
                },
            )
            merged = MERGE.merge(
                lits,
                wvs,
                control_root=control,
                compatibility_receipt=compat_path,
            )
            self.assertTrue(
                merged["control_compatibility"][
                    "explicit_compatibility_receipt_used"
                ]
            )

    def test_legacy_wvs_framework_is_hold_not_admission(
        self,
    ):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            _, _, binding = _make_control_repo(
                tmp
            )
            wvs = tmp / "wvs"
            (wvs / "court").mkdir(parents=True)
            out = EVIDENCE.legacy_wvs_run5_framework(
                wvs_root=wvs,
                current_binding_path=binding,
                output_path=(
                    tmp / "framework.json"
                ),
            )
            self.assertEqual(
                out["status"],
                (
                    "HOLD__EXPLICIT_COMPATIBILITY_"
                    "ADJUDICATION_REQUIRED"
                ),
            )
            self.assertFalse(
                out["automatic_grandfathering_allowed"]
            )
            self.assertFalse(
                out["rerun_automatically_required"]
            )
            self.assertIn(
                (
                    "PHYSICAL_METRIC_ADMISSIBILITY_"
                    "EXPLICITLY_ADJUDICATED"
                ),
                out["required_findings"],
            )

    def test_static_worker_d_code_has_no_raw_source_or_candidate_execution_surface(
        self,
    ):
        helper = EVIDENCE_PATH.read_text(
            encoding="utf-8"
        )
        merge = MERGE_PATH.read_text(
            encoding="utf-8"
        )
        banned = (
            "pyreadstat.read_",
            "backend.run_stage",
            "source_path.open",
            "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        )
        for text in (helper, merge):
            for token in banned:
                self.assertNotIn(token, text)
        self.assertIn(
            "raw_source_bytes_copied",
            helper,
        )
        self.assertIn(
            (
                "cross_source_absolute_physical_metric_"
                "comparison_allowed"
            ),
            merge,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
