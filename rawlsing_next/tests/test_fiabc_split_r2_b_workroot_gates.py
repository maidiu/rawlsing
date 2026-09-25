"""Source-free hostile qualification for FIABC split R2 Worker B.

No raw LiTS/WVS path is accepted by these tests. They exercise only control
gates, temporary Git repositories, and exact protected lock mechanics.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
HELPER_PATH = ROOT / "HQ_HANDOFF" / "launchers" / "FIABC_SPLIT_R2_WORKROOT_GATES.py"
DRIVER_PATH = ROOT / "HQ_HANDOFF" / "launchers" / "FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py"
SHELL_PATH = ROOT / "HQ_HANDOFF" / "launchers" / "RUN_FIABC_SOURCE_LOCAL_SPLIT.sh"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


GATES = _load("fiabc_split_r2_b_workroot_gates_test", HELPER_PATH)


def _run(root: Path, *args: str) -> str:
    proc = subprocess.run(
        list(args), cwd=root, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return proc.stdout.strip()


def _git(root: Path, *args: str) -> str:
    return _run(root, "git", *args)


def _init_repo(root: Path) -> None:
    _git(root, "init")
    _git(root, "config", "user.email", "split-r2-b@example.invalid")
    _git(root, "config", "user.name", "Split R2 B Test")


def _commit_all(root: Path, message: str = "fixture") -> None:
    _git(root, "add", "-A")
    _git(root, "commit", "-m", message)


def _signed_readiness(source: str, *, memory=16_000_000_000, macos="13.2.1"):
    runtime = dict(GATES.EXPECTED_RUNTIME)
    doc = {
        "schema": GATES.READINESS_SCHEMA,
        "status": "PASS",
        "assigned_source": source,
        "canonical_source_sha256": GATES.SOURCE_SHA256[source],
        "source_bytes_opened": 0,
        "source_hash_passes": 0,
        "decoder_calls": 0,
        "candidate_process_launches": 0,
        "fresh_work_root": {"path": f"/synthetic/{source}", "state": "ABSENT", "fresh": True},
        "protected_execution": {
            "branch": GATES.EXPECTED_EXECUTION_BRANCH,
            "head": GATES.EXPECTED_EXECUTION_HEAD,
        },
        "qualified_control": {
            "head": "f" * 40,
            "launcher_sha256": "1" * 64,
            "driver_sha256": "2" * 64,
            "workroot_gates_sha256": "3" * 64,
        },
        "runtime": runtime,
        "combined_import_gate": {
            "status": "PASS",
            "observed": runtime,
            "combined_imports": {},
            "single_interpreter": True,
        },
        "hardware": {
            "hardware_model": "MacBookProSynthetic",
            "cpu_brand": "Synthetic Intel",
            "memory_bytes": memory,
            "architecture": "x86_64",
            "macos_version": macos,
        },
    }
    doc["receipt_identity"] = GATES._semantic_hash(doc)
    return doc


class SplitR2BWorkrootGateTests(unittest.TestCase):
    def test_combined_import_gate_blocks_even_when_metadata_would_be_pinned(self):
        def import_side_effect(name):
            if name == "pyarrow":
                raise ImportError("synthetic ABI loader failure")
            return types.SimpleNamespace(__name__=name, __version__="synthetic")

        with mock.patch.object(GATES.importlib, "import_module", side_effect=import_side_effect), \
             mock.patch.object(
                 GATES.importlib.metadata, "version",
                 side_effect=lambda name: GATES.EXPECTED_RUNTIME[name],
             ):
            with self.assertRaisesRegex(GATES.SplitR2GateError, "combined import/ABI gate failed"):
                GATES.combined_import_abi_gate()

    def test_pair_compatibility_binds_hw_memsize_but_records_macos_separately(self):
        lits = _signed_readiness("LITS_I", macos="13.2.1")
        wvs = _signed_readiness("WVS7", macos="13.6.7")
        pair = GATES.pair_compatibility(lits, wvs)
        self.assertEqual(pair["status"], "PASS__PAIR_COMPATIBLE_BEFORE_MEASUREMENT")
        self.assertFalse(pair["same_macos_version"])
        self.assertFalse(pair["absolute_cross_source_physical_metric_comparison_authorized"])

        wvs_bad = _signed_readiness("WVS7", memory=32_000_000_000)
        with self.assertRaisesRegex(GATES.SplitR2GateError, "memory_bytes"):
            GATES.pair_compatibility(lits, wvs_bad)

    def test_wvs_preprovision_is_code_bytes_only_and_lits_prestate_is_empty(self):
        synthetic = [
            {
                "class": "IMMUTABLE_CANDIDATE_NEUTRAL_SUPPORT",
                "source_path": "rawlsing_next/support.py",
                "destination": "_be1_immutable/deadbeef/rawlsing_next/support.py",
                "git_blob_sha1": "a" * 40,
                "sha256": GATES._sha256_bytes(b"support"),
                "bytes": b"support",
            },
            {
                "class": "EXACT_OWNER_CODE_BYTES",
                "candidate": "A",
                "source_path": "rawlsing_next/owner_a.py",
                "destination": "_exact_owner_modules/deadbeef/A/owner_a.py",
                "git_blob_sha1": "b" * 40,
                "sha256": GATES._sha256_bytes(b"owner"),
                "bytes": b"owner",
            },
        ]
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            repo, work = base / "repo", base / "work"
            repo.mkdir()
            work.mkdir()
            with mock.patch.object(
                GATES, "exact_repo_identity",
                return_value={"branch": GATES.EXPECTED_EXECUTION_BRANCH, "head": GATES.EXPECTED_EXECUTION_HEAD},
            ), mock.patch.object(GATES, "_prestate_material", return_value=synthetic):
                wvs = GATES.provision_joined_prestate(
                    source="WVS7", repo_root=repo, work_root=work,
                    output=work / "court" / "joined_prestate_receipt.json",
                )
                self.assertEqual(wvs["preprovisioned_object_count"], 2)
                self.assertFalse((work / "_be1_lits_projection").exists())
                self.assertFalse((work / "_lits_common_representation").exists())
                self.assertFalse((work / "cells").exists())
                self.assertTrue((work / synthetic[0]["destination"]).is_file())
                self.assertTrue((work / synthetic[1]["destination"]).is_file())
                self.assertFalse(wvs["candidate_owned_semantic_state_prebuilt"])
                self.assertFalse(wvs["candidate_owned_carrier_state_prebuilt"])
                receipt = work / "court" / "joined_prestate_receipt.json"
                GATES.verify_joined_prestate(
                    source="WVS7", repo_root=repo, work_root=work, receipt_path=receipt
                )
                rogue = work / "_be1_immutable" / "rogue.py"
                rogue.parent.mkdir(parents=True, exist_ok=True)
                rogue.write_text("ROGUE = True\n", encoding="utf-8")
                with self.assertRaisesRegex(GATES.SplitR2GateError, "missing/extra files"):
                    GATES.verify_joined_prestate(
                        source="WVS7", repo_root=repo, work_root=work, receipt_path=receipt
                    )

            work2 = base / "work-lits"
            work2.mkdir()
            with mock.patch.object(
                GATES, "exact_repo_identity",
                return_value={"branch": GATES.EXPECTED_EXECUTION_BRANCH, "head": GATES.EXPECTED_EXECUTION_HEAD},
            ):
                lits = GATES.provision_joined_prestate(
                    source="LITS_I", repo_root=repo, work_root=work2,
                    output=work2 / "court" / "joined_prestate_receipt.json",
                )
                self.assertEqual(lits["preprovisioned_object_count"], 0)

    def test_preprovision_refuses_candidate_or_lits_semantic_root(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            repo, work = base / "repo", base / "work"
            repo.mkdir()
            work.mkdir()
            (work / "cells").mkdir()
            with mock.patch.object(
                GATES, "exact_repo_identity",
                return_value={"branch": GATES.EXPECTED_EXECUTION_BRANCH, "head": GATES.EXPECTED_EXECUTION_HEAD},
            ):
                with self.assertRaisesRegex(GATES.SplitR2GateError, "candidate/source semantic state"):
                    GATES.provision_joined_prestate(
                        source="WVS7", repo_root=repo, work_root=work,
                        output=work / "receipt.json",
                    )

    def test_linked_worktree_lock_identity_is_checkout_scoped_not_workroot_scoped(self):
        from rawlsing_next import ee_p2x_darwin_court_driver as protected

        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            main, wt = base / "main", base / "linked"
            main.mkdir()
            _init_repo(main)
            (main / "seed.txt").write_text("seed\n", encoding="utf-8")
            _commit_all(main)
            _git(main, "worktree", "add", "-b", "linked-fixture", str(wt))

            lock_root = GATES.worktree_lock_root(wt)
            self.assertNotEqual(lock_root, wt)
            self.assertTrue(lock_root.is_dir())
            first = protected.DriverInstanceLock(lock_root)
            first.__enter__()
            try:
                with self.assertRaises(protected.RuntimeGateError):
                    protected.DriverInstanceLock(GATES.worktree_lock_root(wt)).__enter__()
            finally:
                first.__exit__(None, None, None)
            with protected.DriverInstanceLock(lock_root):
                pass

    def test_head_baseline_is_distinct_from_selected_source_live_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            repo.mkdir()
            _init_repo(repo)
            (repo / ".gitignore").write_text("__pycache__/\nignored/\n", encoding="utf-8")
            live = repo / GATES.LIVE_EVIDENCE_REL
            (live / "cells").mkdir(parents=True)
            (live / "cells" / "LITS_I__A.json").write_text(
                '{"stage":"LITS_I/A/S01"}\n', encoding="utf-8"
            )
            (repo / "governed.py").write_text("VALUE = 1\n", encoding="utf-8")
            _commit_all(repo)

            work = Path(td) / "work"
            work.mkdir()
            baseline_path = work / "baseline.json"
            identity = {"branch": GATES.EXPECTED_EXECUTION_BRANCH, "head": GATES.EXPECTED_EXECUTION_HEAD}
            with mock.patch.object(GATES, "exact_repo_identity", return_value=identity):
                baseline = GATES.capture_repo_prestate_baseline(
                    repo_root=repo, work_root=work, source="LITS_I", output=baseline_path
                )
            head_rel = (GATES.LIVE_EVIDENCE_REL / "cells" / "LITS_I__A.json").as_posix()
            head_sha = baseline["head_tracked_live_evidence"][head_rel]["sha256"]

            (live / "cells" / "LITS_I__A.json").write_text(
                '{"stage":"LITS_I/A/S16","terminal":true}\n', encoding="utf-8"
            )
            (live / "learned").mkdir()
            (live / "learned" / "LITS_I__A.json").write_text(
                '{"stage":"LITS_I/A/S05"}\n', encoding="utf-8"
            )
            cache = repo / "rawlsing_next" / "__pycache__"
            cache.mkdir(parents=True)
            (cache / "fixture.cpython-311.pyc").write_bytes(b"synthetic-pyc")

            out = work / "postrun.json"
            with mock.patch.object(GATES, "exact_repo_identity", return_value=identity):
                post = GATES.verify_postrun_checkout(
                    repo_root=repo, work_root=work, source="LITS_I",
                    baseline_path=baseline_path, output=out,
                )
            self.assertEqual(post["status"], "PASS__ONLY_CLASSIFIED_POSTRUN_MUTATIONS")
            self.assertTrue(post["head_tracked_baseline_distinguished_from_live_state"])
            self.assertTrue(any(x["change"] == "MODIFIED" for x in post["live_evidence_delta"]))
            self.assertTrue(post["python_cache_delta"])
            self.assertEqual(baseline["head_tracked_live_evidence"][head_rel]["sha256"], head_sha)

    def test_postrun_rejects_nonselected_code_and_ignored_arbitrary_mutation(self):
        for case in ("nonselected", "governed", "ignored"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as td:
                repo = Path(td) / "repo"
                repo.mkdir()
                _init_repo(repo)
                (repo / ".gitignore").write_text("ignored/\n__pycache__/\n", encoding="utf-8")
                live = repo / GATES.LIVE_EVIDENCE_REL
                (live / "cells").mkdir(parents=True)
                (live / "cells" / "LITS_I__A.json").write_text(
                    '{"stage":"LITS_I/A/S01"}\n', encoding="utf-8"
                )
                (live / "cells" / "WVS7__A.json").write_text(
                    '{"stage":"WVS7/A/S01"}\n', encoding="utf-8"
                )
                (repo / "governed.py").write_text("VALUE = 1\n", encoding="utf-8")
                _commit_all(repo)
                work = Path(td) / "work"
                work.mkdir()
                baseline_path = work / "baseline.json"
                identity = {"branch": GATES.EXPECTED_EXECUTION_BRANCH, "head": GATES.EXPECTED_EXECUTION_HEAD}
                with mock.patch.object(GATES, "exact_repo_identity", return_value=identity):
                    GATES.capture_repo_prestate_baseline(
                        repo_root=repo, work_root=work, source="LITS_I", output=baseline_path
                    )

                if case == "nonselected":
                    (live / "cells" / "WVS7__A.json").write_text(
                        '{"stage":"WVS7/A/S16"}\n', encoding="utf-8"
                    )
                    pattern = "not classified for selected source"
                elif case == "governed":
                    (repo / "governed.py").write_text("VALUE = 2\n", encoding="utf-8")
                    pattern = "outside live evidence"
                else:
                    ignored = repo / "ignored"
                    ignored.mkdir()
                    (ignored / "surprise.bin").write_bytes(b"not a runtime cache")
                    pattern = "unclassified ignored-file mutation"

                with mock.patch.object(GATES, "exact_repo_identity", return_value=identity):
                    with self.assertRaisesRegex(GATES.SplitR2GateError, pattern):
                        GATES.verify_postrun_checkout(
                            repo_root=repo, work_root=work, source="LITS_I",
                            baseline_path=baseline_path, output=work / "postrun.json",
                        )

    def test_driver_and_launcher_bind_all_worker_b_gates(self):
        driver = DRIVER_PATH.read_text(encoding="utf-8")
        shell = SHELL_PATH.read_text(encoding="utf-8")
        self.assertIn("split_gates.worktree_lock_root(repo_root)", driver)
        self.assertIn("split_gates.capture_repo_prestate_baseline(", driver)
        self.assertIn("split_gates.verify_postrun_checkout(", driver)
        self.assertIn("split_gates.verify_joined_prestate(", driver)
        self.assertIn("allow_postrun_classification=args.verify_only", driver)

        self.assertIn('"$PYTHON_BIN" "$WORKROOT_GATES" runtime-gate', shell)
        self.assertIn("FIABC_READINESS_ONLY", shell)
        self.assertIn('--pair "$FIABC_PAIR_COMPATIBILITY_RECEIPT"', shell)
        self.assertIn('--work-root "$WORK_ROOT"', shell)
        self.assertIn('"$WORKROOT_GATES" preprovision', shell)
        self.assertIn("--verify-only", shell)
        readiness = shell.index("FIABC_READINESS_ONLY")
        source_required = shell.index("$" + "{SOURCE_PATH:?set SOURCE_PATH")
        source_hash = shell.index("hashlib.sha256()")
        self.assertLess(readiness, source_required)
        self.assertLess(readiness, source_hash)


if __name__ == "__main__":
    unittest.main(verbosity=2)
