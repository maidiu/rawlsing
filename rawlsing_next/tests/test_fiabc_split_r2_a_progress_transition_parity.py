"""R2 Worker A source-free progress/prefix/transition parity qualification.

Requires FIABC_SOURCE_SPLIT_EXECUTION_ROOT to point at the exact protected
execution checkout.  No raw survey source is opened or hashed and no candidate
process is launched.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest


CONTROL_ROOT = Path(__file__).resolve().parents[2]
DRIVER_PATH = CONTROL_ROOT / "HQ_HANDOFF" / "launchers" / "FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py"
EXECUTION_BRANCH = "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
EXECUTION_HEAD = "3d8f2ad62600b6777dcb23a28404a067502e77a0"
SOURCES = ("LITS_I", "WVS7")
CANDIDATES = ("A", "B", "C")
LITS_PREFIX = "LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY"
WVS_C_S00 = "WVS7/C/S00_SOURCE_PREFLIGHT_IDENTITY"


def _load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load test target: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CONTROL = _load_script("fiabc_split_r2_a_driver", DRIVER_PATH)


class ProgressTransitionParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = os.environ.get("FIABC_SOURCE_SPLIT_EXECUTION_ROOT")
        if not raw:
            raise unittest.SkipTest(
                "FIABC_SOURCE_SPLIT_EXECUTION_ROOT must point at exact protected execution checkout"
            )
        cls.execution_root = Path(raw).resolve()
        branch = subprocess.run(
            ["git", "-C", str(cls.execution_root), "branch", "--show-current"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        head = subprocess.run(
            ["git", "-C", str(cls.execution_root), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "-C", str(cls.execution_root), "status", "--porcelain", "--untracked-files=all"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if branch != EXECUTION_BRANCH or head != EXECUTION_HEAD or dirty:
            raise AssertionError(
                f"protected checkout drift branch={branch} head={head} dirty={bool(dirty)}"
            )
        cls.base = CONTROL._load_base(cls.execution_root)
        manifest = (
            cls.execution_root
            / "WORKER_RETURNS"
            / "FIABC-T2"
            / "01_SIX_CELL_EXECUTION_MANIFEST.json"
        )
        cls.machine = cls.base.load_current_execution_manifest(manifest)

    def _ledger(self, root: Path):
        return self.base.StageLedger(root, self.machine, self.execution_root)

    def _terminal(
        self,
        ledger,
        stage,
        *,
        disposition: str,
        next_stage: str,
        source_sha: str,
        begin: bool,
    ):
        identity = self.base._input_identity(
            self.machine, stage, source_sha, EXECUTION_HEAD
        )
        if begin:
            ledger.begin(stage, identity)
        roots = self.base._candidate_roots(
            ledger.work_root, stage.source, stage.candidate
        )
        receipt = self.base._write_receipt(
            roots,
            stage,
            {
                "schema": "FIABC_SPLIT_R2_A_SOURCE_FREE_SIMULATION@1.0.0",
                "stage": stage.address,
                "source_free": True,
                "candidate_process_launched": False,
            },
        )
        ledger.complete(
            stage,
            input_identity_hash=identity,
            terminal_disposition=disposition,
            receipt_path=receipt,
            output_artifact_hashes={},
            verifier_complete=True,
            next_stage=next_stage,
        )

    def _mechanical(self, ledger, stage, source_sha):
        disposition = (
            "PRESERVED"
            if stage.disposition == "DONE__PRESERVE"
            else "SKIPPED_BY_FROZEN_LAW"
        )
        self._terminal(
            ledger,
            stage,
            disposition=disposition,
            next_stage=stage.next_stage_on_pass,
            source_sha=source_sha,
            begin=False,
        )

    def _materialize_joined_prefix(self, ledger, source):
        source_sha = self.machine.document["sources"][source]["sha256"]
        for address in CONTROL._joined_preflight_prefix(self.base, self.machine):
            if not address.startswith(source + "/"):
                continue
            self._mechanical(ledger, self.machine.get(address), source_sha)

    def _simulate_joined(self, source: str, outcome: tuple[str, str] | None):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        ledger = self._ledger(Path(temp.name))
        self._materialize_joined_prefix(ledger, source)
        source_sha = self.machine.document["sources"][source]["sha256"]
        calls: list[str] = []
        trace = [
            address
            for address in CONTROL._joined_all_pass_trace(self.machine)
            if address.startswith(source + "/")
        ]
        address = trace[0]
        visited: set[str] = set()
        while address.startswith(source + "/"):
            if address in visited:
                raise AssertionError(f"joined simulation cycle at {address}")
            visited.add(address)
            stage = self.machine.get(address)
            if stage.disposition == "DONE__PRESERVE" or stage.disposition == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW":
                self._mechanical(ledger, stage, source_sha)
                address = stage.next_stage_on_pass
                continue
            self.assertEqual(stage.disposition, "READY__RUN_LOCALLY")
            calls.append(address)
            kind = outcome[0] if outcome and outcome[1] == address else "PASS"
            if kind == "CANDIDATE":
                self._terminal(
                    ledger, stage,
                    disposition="CANDIDATE_LOCAL_FAILURE",
                    next_stage=stage.next_stage_on_candidate_local_failure,
                    source_sha=source_sha, begin=True,
                )
                self.base._candidate_stop(
                    self.machine, ledger,
                    source=source, candidate=stage.candidate,
                    head=EXECUTION_HEAD, source_sha=source_sha, blocker=address,
                )
                address = stage.next_stage_on_candidate_local_failure
            elif kind == "SOURCE":
                self._terminal(
                    ledger, stage,
                    disposition="BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
                    next_stage="__COMMON_SOURCE_BLOCKER__",
                    source_sha=source_sha, begin=True,
                )
                address = self.base._source_stop(
                    self.machine, ledger, source=source, head=EXECUTION_HEAD,
                    source_sha=source_sha, blocker=stage.address,
                )
                break
            elif kind == "COURT":
                self._terminal(
                    ledger, stage,
                    disposition="BLOCKED_BY_COMMON_COURT_AUTHORITY",
                    next_stage="__COMMON_COURT_BLOCKER__",
                    source_sha=source_sha, begin=True,
                )
                break
            else:
                self._terminal(
                    ledger, stage, disposition="PASS",
                    next_stage=stage.next_stage_on_pass,
                    source_sha=source_sha, begin=True,
                )
                address = stage.next_stage_on_pass
        return calls, dict(ledger.data["stages"])

    def _simulate_split(self, source: str, outcome: tuple[str, str] | None):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        ledger = self._ledger(Path(temp.name))
        self._materialize_joined_prefix(ledger, source)
        source_sha = self.machine.document["sources"][source]["sha256"]
        calls: list[str] = []
        for address in CONTROL._stage_addresses(self.base, self.machine, source):
            old = ledger.stage_entry(address)
            if old and old.get("terminal_disposition") in self.base.COMPLETE_LEDGER_DISPOSITIONS:
                ledger.revalidate_terminal(address)
                continue
            stage = self.machine.get(address)
            if stage.disposition == "DONE__PRESERVE" or stage.disposition == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW":
                self._mechanical(ledger, stage, source_sha)
                continue
            self.assertEqual(stage.disposition, "READY__RUN_LOCALLY")
            calls.append(address)
            kind = outcome[0] if outcome and outcome[1] == address else "PASS"
            if kind == "CANDIDATE":
                self._terminal(
                    ledger, stage,
                    disposition="CANDIDATE_LOCAL_FAILURE",
                    next_stage=stage.next_stage_on_candidate_local_failure,
                    source_sha=source_sha, begin=True,
                )
                self.base._candidate_stop(
                    self.machine, ledger,
                    source=source, candidate=stage.candidate,
                    head=EXECUTION_HEAD, source_sha=source_sha, blocker=address,
                )
            elif kind == "SOURCE":
                self._terminal(
                    ledger, stage,
                    disposition="BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
                    next_stage="__COMMON_SOURCE_BLOCKER__",
                    source_sha=source_sha, begin=True,
                )
                self.base._source_stop(
                    self.machine, ledger, source=source, head=EXECUTION_HEAD,
                    source_sha=source_sha, blocker=stage.address,
                )
                break
            elif kind == "COURT":
                self._terminal(
                    ledger, stage,
                    disposition="BLOCKED_BY_COMMON_COURT_AUTHORITY",
                    next_stage="__COMMON_COURT_BLOCKER__",
                    source_sha=source_sha, begin=True,
                )
                break
            else:
                self._terminal(
                    ledger, stage, disposition="PASS",
                    next_stage=stage.next_stage_on_pass,
                    source_sha=source_sha, begin=True,
                )
        return calls, dict(ledger.data["stages"])

    def test_run5_lits_progress_crash_reproduced_then_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = self._ledger(Path(tmp))
            reporter = self.base.ProgressReporter(
                self.machine, ledger, stream=io.StringIO()
            )
            with self.assertRaisesRegex(
                self.base.StageStateError,
                "progress address precedes current manifest entry",
            ):
                reporter.plan.position(LITS_PREFIX)

            local = CONTROL.SourceLocalManifestProgressPlan(
                self.base, self.machine, "LITS_I"
            )
            reporter.plan = local
            position = reporter.plan.position(LITS_PREFIX)
            self.assertEqual(position.overall_index, 1)
            self.assertEqual(position.overall_total, 51)
            self.assertEqual(position.cell_index, 1)
            self.assertEqual(position.cell_total, 3)
            reporter.emit_stage(
                self.machine.get(LITS_PREFIX),
                "PRESERVE",
                next_stage="LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD",
                elapsed_stage_ns=0,
                terminal_disposition="PRESERVED",
            )
            event = json.loads(
                (Path(tmp) / "fiabc_driver_progress.jsonl")
                .read_text(encoding="utf-8")
                .strip()
            )
            self.assertTrue(event["court_administration_only"])
            self.assertFalse(event["evidentiary_measurement"])
            self.assertEqual(event["address"], LITS_PREFIX)

    def test_exact_source_local_progress_universes(self):
        expected = {
            "LITS_I": {"ready": 44, "preserve": 5, "skip": 2},
            "WVS7": {"ready": 44, "preserve": 3, "skip": 4},
        }
        for source in SOURCES:
            with self.subTest(source=source):
                plan = CONTROL.SourceLocalManifestProgressPlan(
                    self.base, self.machine, source
                )
                self.assertEqual(plan.overall_total, 51)
                self.assertEqual(plan.executable_total, 44)
                self.assertEqual(plan.cell_total, 3)
                self.assertTrue(
                    all(a.startswith(source + "/") for a in plan.governed_addresses)
                )
                self.assertFalse(
                    any(a.startswith("COURT/") or "/S17_" in a for a in plan.governed_addresses)
                )
                counts = {"ready": 0, "preserve": 0, "skip": 0}
                for address in plan.governed_addresses:
                    disposition = self.machine.get(address).disposition
                    if disposition == "READY__RUN_LOCALLY":
                        counts["ready"] += 1
                    elif disposition == "DONE__PRESERVE":
                        counts["preserve"] += 1
                    elif disposition == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW":
                        counts["skip"] += 1
                self.assertEqual(counts, expected[source])

    def test_joined_split_exact_all_pass_differential(self):
        lits = CONTROL._assert_transition_parity(
            self.base, self.machine, "LITS_I"
        )
        self.assertEqual(lits["joined_preflight"], [LITS_PREFIX])
        self.assertEqual(len(lits["joined_run"]), 50)
        self.assertEqual(len(lits["split_run"]), 50)
        self.assertEqual(lits["split_extra_addresses"], [])
        self.assertTrue(lits["candidate_backend_addresses_identical"])
        self.assertEqual(len(lits["joined_candidate_backend_addresses"]), 44)

        wvs = CONTROL._assert_transition_parity(
            self.base, self.machine, "WVS7"
        )
        self.assertEqual(wvs["joined_preflight"], [])
        self.assertEqual(len(wvs["joined_run"]), 50)
        self.assertEqual(len(wvs["split_run"]), 51)
        self.assertEqual(wvs["split_extra_addresses"], [WVS_C_S00])
        self.assertEqual(wvs["approved_mechanical_extra_addresses"], [WVS_C_S00])
        self.assertTrue(wvs["candidate_backend_addresses_identical"])
        self.assertEqual(len(wvs["joined_candidate_backend_addresses"]), 44)
        extra = self.machine.get(WVS_C_S00)
        self.assertEqual(extra.disposition, "DONE__PRESERVE")
        self.assertFalse(extra.empirical_source_access_required)
        self.assertFalse(extra.physical_host_measurement_required)

    def test_lits_preflight_prefix_uses_actual_preserve_mechanics_source_free(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = self._ledger(Path(tmp))
            driver = types.SimpleNamespace(
                ledger=ledger,
                repo_root=self.execution_root,
                repo=types.SimpleNamespace(head=EXECUTION_HEAD),
            )
            prefix = CONTROL._materialize_source_preflight_prefix(
                base=self.base,
                driver=driver,
                machine=self.machine,
                source="LITS_I",
                source_sha=self.machine.document["sources"]["LITS_I"]["sha256"],
            )
            self.assertEqual(prefix, (LITS_PREFIX,))
            entry = ledger.revalidate_terminal(LITS_PREFIX)
            self.assertEqual(entry["terminal_disposition"], "PRESERVED")
            receipt = json.loads(
                (ledger.work_root / entry["receipt_path"]).read_text(encoding="utf-8")
            )
            self.assertFalse(receipt["execution_performed"])
            self.assertFalse(receipt["measurement_performed"])
            self.assertFalse(receipt["source_access_performed"])

    def test_failure_and_blocker_differential_uses_actual_state_machine_and_ledger(self):
        candidate_cases = [
            ("CANDIDATE", f"{source}/{candidate}/{stage}")
            for source in SOURCES
            for candidate in CANDIDATES
            for stage in (
                "S01_CANDIDATE_PREPARATION_BUILD",
                "S05_I05_LEARNED_PRODUCTION",
                "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS",
            )
        ]
        blocker_cases = [
            (kind, f"{source}/{candidate}/{stage}")
            for source in SOURCES
            for kind in ("SOURCE", "COURT")
            for candidate, stage in (
                ("A", "S01_CANDIDATE_PREPARATION_BUILD"),
                ("B", "S08_WARM_REPEATED_RESEARCH"),
                ("C", "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS"),
            )
        ]
        cases = [(source, None) for source in SOURCES]
        cases.extend((address.split("/", 1)[0], (kind, address)) for kind, address in candidate_cases)
        cases.extend((address.split("/", 1)[0], (kind, address)) for kind, address in blocker_cases)

        for source, outcome in cases:
            with self.subTest(source=source, outcome=outcome):
                joined_calls, joined_ledger = self._simulate_joined(source, outcome)
                split_calls, split_ledger = self._simulate_split(source, outcome)
                self.assertEqual(
                    split_calls,
                    joined_calls,
                    "candidate backend call addresses/order must be identical",
                )
                self.assertTrue(all(a.startswith(source + "/") for a in split_calls))
                self.assertFalse(any(a.startswith("COURT/") for a in split_calls))

                shared = set(joined_ledger) & set(split_ledger)
                for address in shared:
                    self.assertEqual(
                        split_ledger[address]["terminal_disposition"],
                        joined_ledger[address]["terminal_disposition"],
                        address,
                    )
                split_only = set(split_ledger) - set(joined_ledger)
                if source == "WVS7" and outcome is None:
                    self.assertEqual(split_only, {WVS_C_S00})
                    self.assertEqual(
                        split_ledger[WVS_C_S00]["terminal_disposition"],
                        "PRESERVED",
                    )
                else:
                    self.assertTrue(
                        split_only <= {WVS_C_S00},
                        f"unapproved split-only terminal rows: {split_only}",
                    )

    def test_split_source_cut_never_contains_other_source_or_s17(self):
        for source in SOURCES:
            with self.subTest(source=source):
                addresses = CONTROL._stage_addresses(self.base, self.machine, source)
                self.assertEqual(len(addresses), 51)
                self.assertTrue(all(a.startswith(source + "/") for a in addresses))
                self.assertFalse(any(a.startswith("COURT/") or "/S17_" in a for a in addresses))


if __name__ == "__main__":
    unittest.main(verbosity=2)
