"""Source-free qualification tests for the FIABC source-local split runner.

These tests use synthetic manifests, temporary receipt files, and fake backends.
They never open LiTS-I or WVS7 and never start a candidate process.
"""
from __future__ import annotations

import ast
import contextlib
import dataclasses
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock


CONTROL_ROOT = Path(__file__).resolve().parents[2]
LAUNCHERS = CONTROL_ROOT / "HQ_HANDOFF" / "launchers"
DRIVER_PATH = LAUNCHERS / "FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py"
MERGE_PATH = LAUNCHERS / "FIABC_SOURCE_LOCAL_SPLIT_MERGE.py"
SHELL_PATH = LAUNCHERS / "RUN_FIABC_SOURCE_LOCAL_SPLIT.sh"
EXECUTION_HEAD = "16f5e7d5f691e908d85dc1dd26b8a59a29f668f4"
CONTROL_BRANCH = "agent/vozhd-fiabc-split-r2-fanin-r1"
EXECUTION_BRANCH = "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
SOURCES = ("LITS_I", "WVS7")
CANDIDATES = ("A", "B", "C")


def _load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load qualification target: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


DRIVER = _load_script("fiabc_source_local_split_driver_qualification", DRIVER_PATH)
MERGE = _load_script("fiabc_source_local_split_merge_qualification", MERGE_PATH)
D_TEST_PATH = CONTROL_ROOT / "rawlsing_next" / "tests" / "test_fiabc_split_r2_d_merge_portable_evidence.py"
D_FIXTURES = _load_script("fiabc_split_r2_d_merge_portable_evidence_fixtures", D_TEST_PATH)


@dataclasses.dataclass(frozen=True)
class Identity:
    schema: str = "SYNTHETIC-MANIFEST@1"
    sha256: str = "a" * 64
    git_blob_sha1: str = "b" * 40


@dataclasses.dataclass(frozen=True)
class Stage:
    source: str
    candidate: str
    stage_id: str = "S01"
    disposition: str = "READY__RUN_LOCALLY"
    empirical_source_access_required: bool = True
    physical_host_measurement_required: bool = False
    next_stage_on_pass: str = "__NEXT__"
    next_stage_on_candidate_local_failure: str = "__NEXT__"
    evidence_or_stop_law_ref: str = "SYNTHETIC-LAW"

    @property
    def address(self) -> str:
        return f"{self.source}/{self.candidate}/{self.stage_id}"


@dataclasses.dataclass(frozen=True)
class StageContext:
    contract: str
    stage: Stage
    work_root: Path
    roots: object
    source_path: Path | None
    source_sha256: str
    manifest_identity: Identity
    branch: str
    head: str
    input_identity: str


@dataclasses.dataclass(frozen=True)
class BackendResult:
    terminal_disposition: str
    receipt: dict
    output_artifacts: dict = dataclasses.field(default_factory=dict)
    verifier_complete: bool = True


class CandidateLocalFailure(Exception):
    def __init__(self, message="synthetic candidate failure"):
        super().__init__(message)
        self.receipt = {"synthetic": True}


class CommonAuthorityBlocker(Exception):
    def __init__(self, scope="COURT"):
        super().__init__(f"synthetic {scope} blocker")
        self.scope = scope
        self.receipt = {"synthetic": True, "scope": scope}


class FakeMachine:
    def __init__(self, stages: list[Stage]):
        self.stages = {stage.address: stage for stage in stages}
        self.identity = Identity()
        stage_catalog = list(dict.fromkeys(stage.stage_id for stage in stages))
        self.document = {
            "source_order": list(SOURCES),
            "sources": {source: {"sha256": "c" * 64} for source in SOURCES},
            "stage_catalog": stage_catalog,
            "cells": [
                {"source": source, "candidate": candidate,
                 "stages": {stage_id: {} for stage_id in stage_catalog
                            if f"{source}/{candidate}/{stage_id}" in self.stages}}
                for source in SOURCES
                for candidate in CANDIDATES
            ],
        }

    def get(self, address: str) -> Stage:
        return self.stages[address]


class FakeLedger:
    def __init__(self, root: Path):
        self.work_root = root
        self.entries: dict[str, dict] = {}
        self._source_identity = {"sha256": "c" * 64, "size": 17}
        self.events: list[tuple] = []

    def stage_entry(self, address: str):
        return self.entries.get(address)

    def begin(self, stage: Stage, input_identity: str) -> None:
        self.events.append(("begin", stage.address))
        self.entries[stage.address] = {
            "state": "RUNNING",
            "terminal_disposition": None,
            "input_identity_hash": input_identity,
        }

    def revalidate_terminal(self, address: str):
        self.events.append(("revalidate", address))
        return self.entries[address]

    def source_identity(self, source: str):
        return self._source_identity

    def hash(self) -> str:
        return "d" * 64


class FakeProgress:
    def __init__(self):
        self.events: list[tuple] = []
        self.counter = 0

    def now_ns(self) -> int:
        self.counter += 1
        return self.counter

    def emit_stage(self, stage, state, **kwargs):
        self.events.append((stage.address, state, kwargs.get("terminal_disposition")))

    def emit_completed_cells(self):
        return None


class FakeBackend:
    def __init__(self, *, failure_address: str | None = None, blocker_address: str | None = None, blocker_scope="COURT"):
        self.failure_address = failure_address
        self.blocker_address = blocker_address
        self.blocker_scope = blocker_scope
        self.calls: list[StageContext] = []
        self.processes_started = 0
        self.stop_requests: list[tuple[Stage, str]] = []

    def run_stage(self, context: StageContext, services):
        self.calls.append(context)
        if context.stage.address == self.failure_address:
            raise CandidateLocalFailure()
        if context.stage.address == self.blocker_address:
            raise CommonAuthorityBlocker(self.blocker_scope)
        return BackendResult("PASS", {"synthetic": True})

    def stop_after_outer_nonpass(self, stage, *, reason):
        self.stop_requests.append((stage, reason))
        return {"status": "STOPPED", "reason": reason}


class FakeBase:
    COMPLETE_LEDGER_DISPOSITIONS = {
        "PASS", "PRESERVED", "SKIPPED_BY_FROZEN_LAW", "CANDIDATE_LOCAL_FAILURE",
        "BLOCKED_BY_COMMON_SOURCE_AUTHORITY", "BLOCKED_BY_COMMON_COURT_AUTHORITY",
    }
    BACKEND_CONTRACT = "SYNTHETIC-BACKEND-CONTRACT"
    P2X_BRANCH = "synthetic-protected-branch"
    StageContext = StageContext
    BackendResult = BackendResult
    CandidateLocalFailure = CandidateLocalFailure
    CommonAuthorityBlocker = CommonAuthorityBlocker
    OWNER_COMMIT = "e" * 40
    OWNER_SPECS = {
        candidate: {"path": f"owners/{candidate}.py", "blob": ""}
        for candidate in CANDIDATES
    }

    def __init__(self):
        self.events: list[tuple] = []
        self.outer_disposition_override: str | None = None
        for candidate, spec in self.OWNER_SPECS.items():
            body = f"synthetic owner {candidate}".encode()
            spec["blob"] = hashlib.sha1(f"blob {len(body)}\0".encode() + body).hexdigest()

    @staticmethod
    def _manifest_ordered_stage_ids(document, cell):
        return tuple(sid for sid in document.get("stage_catalog", ()) if sid in cell.get("stages", {}))

    def _candidate_roots(self, work_root, source, candidate):
        self.events.append(("roots", source, candidate))
        return types.SimpleNamespace(source=source, candidate=candidate)

    @staticmethod
    def _input_identity(machine, stage, source_sha, head):
        return f"{stage.address}:{source_sha}:{head}"

    @staticmethod
    def _git_show_bytes(repo_root, commit, path):
        candidate = Path(path).stem
        return f"synthetic owner {candidate}".encode()

    @staticmethod
    def _git_blob_sha1(data):
        return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

    @staticmethod
    def _atomic_write_json(path, payload):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def validate_frozen_upstream_for_machine(machine, path):
        return {"status": "PASS"}

    @staticmethod
    def _token(stage, receipt_hash, ledger_hash, head):
        return {
            "schema": "SYNTHETIC_SUPERVISOR_TOKEN@1",
            "action": "COMMIT_AND_PUSH_EXISTING_P2X_BRANCH_BOUNDED_STAGE_EVIDENCE",
            "stage_id": stage.address,
            "terminal_receipt_sha256": receipt_hash,
            "ledger_sha256": ledger_hash,
            "observed_p2x_head": head,
        }

    def _backend_terminal(self, machine, ledger, stage, head, source_sha, result):
        disposition = {
            "PASS": "PASS",
            "CANDIDATE_LOCAL_FAILURE": "CANDIDATE_LOCAL_FAILURE",
            "COMMON_SOURCE_BLOCKER": "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
            "COMMON_COURT_BLOCKER": "BLOCKED_BY_COMMON_COURT_AUTHORITY",
        }[result.terminal_disposition]
        next_stage = {
            "PASS": stage.next_stage_on_pass,
            "CANDIDATE_LOCAL_FAILURE": stage.next_stage_on_candidate_local_failure,
            "COMMON_SOURCE_BLOCKER": "__SOURCE_BLOCKED__",
            "COMMON_COURT_BLOCKER": "__COMMON_COURT_BLOCKER__",
        }[result.terminal_disposition]
        if result.terminal_disposition == "PASS" and self.outer_disposition_override:
            disposition = self.outer_disposition_override
            next_stage = "__COMMON_COURT_BLOCKER__"
        self.events.append(("backend-terminal", stage.address, disposition))
        old = ledger.stage_entry(stage.address) or {}
        old.update({"state": "TERMINAL", "terminal_disposition": disposition,
                    "receipt_hash": hashlib.sha256(stage.address.encode()).hexdigest(),
                    "next_stage": next_stage})
        ledger.entries[stage.address] = old
        return next_stage, old["receipt_hash"], disposition

    def _stop_backend_after_posthook_nonpass(self, backend, stage, backend_terminal, ledger_disposition):
        self.events.append(("posthook-stop", stage.address, backend_terminal, ledger_disposition))
        if backend_terminal != "PASS" or ledger_disposition == "PASS":
            return None
        stop = getattr(backend, "stop_after_outer_nonpass", None)
        if not callable(stop):
            raise AssertionError("outer non-PASS did not stop the retained backend")
        return stop(stage, reason=f"OUTER_TYPED_NONPASS::{stage.address}::{ledger_disposition}")

    @staticmethod
    def _candidate_stop(machine, ledger, *, source, candidate, head, source_sha, blocker):
        catalog = list(machine.document.get("stage_catalog", ()))
        blocker_id = blocker.rsplit("/", 1)[-1]
        for stage_id in catalog[catalog.index(blocker_id) + 1:]:
            address = f"{source}/{candidate}/{stage_id}"
            if ledger.stage_entry(address) is None:
                ledger.entries[address] = {
                    "state": "TERMINAL",
                    "terminal_disposition": "CANDIDATE_LOCAL_FAILURE",
                    "receipt_hash": hashlib.sha256(address.encode()).hexdigest(),
                }

    @staticmethod
    def _mark_source_blocked(machine, ledger, *, source, observed_head, source_sha256, blocker_stage):
        for cell in machine.document["cells"]:
            if cell["source"] == source:
                for stage_id in machine.document["stage_catalog"]:
                    address = f"{source}/{cell['candidate']}/{stage_id}"
                    if ledger.stage_entry(address) is None:
                        ledger.entries[address] = {
                            "state": "TERMINAL",
                            "terminal_disposition": "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
                            "receipt_hash": "f" * 64,
                        }


class FakeDriver:
    def __init__(
        self,
        root: Path,
        backend: FakeBackend | None = None,
        *,
        source: str = "LITS_I",
    ):
        self.work_root = root
        (root / "court").mkdir(parents=True, exist_ok=True)
        (root / "court" / "joined_prestate_receipt.json").write_text("{}\n", encoding="utf-8")
        (root / "court" / "repo_prestate_baseline.json").write_text("{}\n", encoding="utf-8")
        preflight = {
            "schema": DRIVER.SOURCE_PREFLIGHT_SCHEMA,
            "status": "PASS",
            "source": source,
            "split_only_mechanical_closure": (
                list(DRIVER.WVS_SPLIT_ONLY_MECHANICAL_CLOSURE)
                if source == "WVS7"
                else []
            ),
            "split_only_mechanical_closure_law": {
                "source_free": True,
                "candidate_processes_started": 0,
                "physical_measurement_performed": False,
                "empirical_source_access_performed": False,
                "authorized_addresses": list(
                    DRIVER.WVS_SPLIT_ONLY_MECHANICAL_CLOSURE
                ),
            },
        }
        preflight["receipt_identity"] = hashlib.sha256(
            DRIVER._canon(preflight)
        ).hexdigest()
        (root / "court" / "source_local_preflight.json").write_text(
            json.dumps(preflight, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        self.repo_root = root / "execution"
        self.repo = types.SimpleNamespace(branch=EXECUTION_BRANCH, head=EXECUTION_HEAD)
        self.host = {"synthetic": True}
        self.ledger = FakeLedger(root)
        self.progress = FakeProgress()
        self.backend = backend or FakeBackend()
        self.services = object()
        self.source_paths = {
            source: Path(
                "/synthetic/source/LiTS-I.dta"
                if source == "LITS_I"
                else "/synthetic/source/WVS7.sav"
            )
        }
        self.verified_sources: list[str] = []

    def verify_static_gates(self):
        return None

    def ensure_source_verified(self, source):
        self.verified_sources.append(source)
        return "c" * 64


def _synthetic_stages(source="LITS_I", *, empirical=True, physical=False):
    stages = []
    for candidate in CANDIDATES:
        stages.extend([
            Stage(source, candidate, "S01", empirical_source_access_required=empirical,
                  physical_host_measurement_required=physical),
            Stage(source, candidate, "S02", empirical_source_access_required=empirical,
                  physical_host_measurement_required=physical),
        ])
    return stages


def _write_terminal(root: Path, source: str, *, os_version="13.2.1", memory=16 * 1024**3,
                    hardware="MacBookPro15,1", blockers=None, failures=None, overrides=None):
    doc = {
        "schema": DRIVER.SOURCE_TERMINAL_SCHEMA,
        "status": "SOURCE_BLOCK_SEQUENCE_COMPLETE__ALL_THREE_CELLS_TERMINAL",
        "source": source,
        "source_sha256": "1" * 64,
        "candidate_order": list(CANDIDATES),
        "candidate_terminals": {
            candidate: {"address": f"{source}/{candidate}/S01", "terminal_disposition": "PASS",
                        "receipt_hash": hashlib.sha256(candidate.encode()).hexdigest()}
            for candidate in CANDIDATES
        },
        "candidate_failure_cells": list(failures or []),
        "common_blockers": list(blockers or []),
        "incomplete_stages": [],
        "stage_ledger_sha256": "2" * 64,
        "execution_branch": EXECUTION_BRANCH,
        "execution_head": EXECUTION_HEAD,
        "current_execution_manifest": {"identity": "same-exact-manifest"},
        "host": {
            "governed_runtime": {
                "implementation": "CPython", "python": "3.11.3", "system": "Darwin",
                "machine": "x86_64", "dependency_versions": {
                    "pyreadstat": "1.3.6", "pyarrow": "25.0.1",
                    "pandas": "2.3.1", "numpy": "2.3.2",
                },
            },
            "hardware_model": hardware,
            "cpu_brand": "Intel(R) Core(TM) i9-9880H CPU @ 2.30GHz",
            "memory_bytes": memory,
            "macos_version": os_version,
        },
        "source_local_only": True,
        "six_cell_s17_executed": False,
        "six_cell_completion_claimed": False,
        "measured_synthesis_performed": False,
    }
    if overrides:
        doc.update(overrides)
    doc["receipt_identity"] = hashlib.sha256(MERGE._canon(doc)).hexdigest()
    court = root / "court"
    court.mkdir(parents=True, exist_ok=True)
    (court / "source_local_terminal.json").write_text(
        json.dumps(doc, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )


class SourceLocalSplitQualificationTests(unittest.TestCase):
    def setUp(self):
        cache_gate = mock.patch.object(
            DRIVER, "_assert_cache_neutral_work_root", return_value={}
        )
        receipt_gate = mock.patch.object(
            DRIVER,
            "_verify_cache_neutral_receipt",
            return_value={"receipt_identity": "e" * 64},
        )
        cache_gate.start()
        receipt_gate.start()
        self.addCleanup(cache_gate.stop)
        self.addCleanup(receipt_gate.stop)

    def _fake_driver(self, backend=None, *, source="LITS_I"):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return FakeDriver(Path(temp.name), backend, source=source)

    def _run_worker_d_test(self, method: str) -> None:
        case = D_FIXTURES.WorkerDPortableEvidenceTests(method)
        getattr(case, method)()

    def _exact_execution_root(self) -> Path:
        raw = os.environ.get("FIABC_SOURCE_SPLIT_EXECUTION_ROOT")
        if not raw:
            self.skipTest("qualification runner must supply the exact protected execution checkout")
        root = Path(raw).resolve()
        self.assertEqual(
            subprocess.run(["git", "-C", str(root), "branch", "--show-current"],
                           capture_output=True, text=True, check=True).stdout.strip(),
            EXECUTION_BRANCH,
        )
        self.assertEqual(
            subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                           capture_output=True, text=True, check=True).stdout.strip(),
            EXECUTION_HEAD,
        )
        self.assertEqual(
            subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"],
                           capture_output=True, text=True, check=True).stdout.strip(),
            "",
        )
        return root

    def test_syntax_and_standalone_packaging(self):
        shell = subprocess.run(["bash", "-n", str(SHELL_PATH)], capture_output=True, text=True)
        self.assertEqual(shell.returncode, 0, shell.stderr)
        for path in (DRIVER_PATH, MERGE_PATH):
            compile(path.read_bytes(), str(path), "exec")
        for path in (DRIVER_PATH, MERGE_PATH):
            result = subprocess.run([sys.executable, "-B", str(path), "--help"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_control_and_execution_identity_are_pinned(self):
        self.assertIn(CONTROL_BRANCH, SHELL_PATH.read_text(encoding="utf-8"))
        self.assertIn(EXECUTION_BRANCH, DRIVER_PATH.read_text(encoding="utf-8"))
        self.assertIn(EXECUTION_HEAD, DRIVER_PATH.read_text(encoding="utf-8"))
        self.assertIn("base.ISOLATED_BACKEND_MODULE", DRIVER_PATH.read_text(encoding="utf-8"))
        self.assertIn('args.backend_module != base.ISOLATED_BACKEND_MODULE', DRIVER_PATH.read_text(encoding="utf-8"))

    def test_outer_posthook_nonpass_stops_retained_backend_before_block_propagation(self):
        stage = Stage(
            "LITS_I", "A", "S05_I05_LEARNED_PRODUCTION",
            empirical_source_access_required=True,
        )
        machine = FakeMachine([stage])
        backend = FakeBackend()
        driver = self._fake_driver(backend)
        base = FakeBase()
        base.outer_disposition_override = "BLOCKED_BY_COMMON_COURT_AUTHORITY"
        with mock.patch.object(DRIVER, "_hardware_fingerprint", return_value={"synthetic": True}), \
             mock.patch.object(
                 DRIVER,
                 "_write_source_terminal",
                 return_value={"status": "BLOCKED__COMMON_COURT_AUTHORITY"},
             ), \
             mock.patch.dict(os.environ, {
                 "RAWLSING_FIABC_SPLIT_CONTROL_HEAD": "f" * 40,
                 "RAWLSING_FIABC_SPLIT_CONTROL_CHECKOUT_HEAD": "f" * 40,
                 "RAWLSING_FIABC_SPLIT_CONTROL_BINDING_IDENTITY": "a" * 64,
                 "RAWLSING_FIABC_SPLIT_RUNNER_SHA256": "0" * 64,
             }):
            terminal = DRIVER._run_source_block(
                base=base, driver=driver, machine=machine, source="LITS_I"
            )
        self.assertEqual(terminal["status"], "BLOCKED__COMMON_COURT_AUTHORITY")
        self.assertEqual(len(backend.stop_requests), 1)
        self.assertIn(
            ("posthook-stop", stage.address, "PASS", "BLOCKED_BY_COMMON_COURT_AUTHORITY"),
            base.events,
        )
        source = DRIVER_PATH.read_text(encoding="utf-8")
        dispatch = source.index("base._backend_terminal(")
        stop = source.index("base._stop_backend_after_posthook_nonpass(")
        propagation = source.index('if disposition == "CANDIDATE_LOCAL_FAILURE":')
        self.assertLess(dispatch, stop)
        self.assertLess(stop, propagation)

    def test_loader_accepts_only_module_origin_inside_exact_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "protected"
            package = root / "rawlsing_next"
            package.mkdir(parents=True)
            (package / "__init__.py").write_text("", encoding="utf-8")
            (package / "ee_p2x_darwin_court_driver.py").write_text("ORIGIN='protected'\n", encoding="utf-8")
            saved = {key: sys.modules.get(key) for key in ("rawlsing_next", "rawlsing_next.ee_p2x_darwin_court_driver")}
            for key in saved:
                sys.modules.pop(key, None)
            try:
                loaded = DRIVER._load_base(root)
                self.assertEqual(Path(loaded.__file__).resolve(), (package / "ee_p2x_darwin_court_driver.py").resolve())
                outsider = Path(tmp) / "outside.py"
                outsider.write_text("ORIGIN='outside'\n", encoding="utf-8")
                parent = sys.modules["rawlsing_next"]
                if hasattr(parent, "ee_p2x_darwin_court_driver"):
                    delattr(parent, "ee_p2x_darwin_court_driver")
                fake = types.ModuleType("rawlsing_next.ee_p2x_darwin_court_driver")
                fake.__file__ = str(outsider)
                sys.modules["rawlsing_next.ee_p2x_darwin_court_driver"] = fake
                with self.assertRaisesRegex(DRIVER.SourceLocalRunnerError, "imported outside protected checkout"):
                    DRIVER._load_base(root)
            finally:
                for key in ("rawlsing_next", "rawlsing_next.ee_p2x_darwin_court_driver"):
                    sys.modules.pop(key, None)
                for key, value in saved.items():
                    if value is not None:
                        sys.modules[key] = value

    def test_single_driver_lock_encloses_dispatch_and_is_exclusive(self):
        tree = ast.parse(DRIVER_PATH.read_text(encoding="utf-8"))
        main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
        lock_nodes = [node for node in ast.walk(main) if isinstance(node, ast.With)
                      and any("DriverInstanceLock" in ast.unparse(item.context_expr) for item in node.items)]
        self.assertEqual(len(lock_nodes), 1)
        guarded = "\n".join(ast.unparse(node) for node in ast.walk(lock_nodes[0]))
        for required in ("DarwinCourtDriver", "_source_preflight", "_verify_source_block", "_run_source_block"):
            self.assertIn(required, guarded)

    def test_exact_protected_manifest_partitions_to_current_source_A_B_C(self):
        execution_root = self._exact_execution_root()
        base = DRIVER._load_base(execution_root)
        self.assertTrue(Path(base.__file__).resolve().is_relative_to(execution_root))
        manifest_path = execution_root / "WORKER_RETURNS" / "FIABC-T2" / "01_SIX_CELL_EXECUTION_MANIFEST.json"
        machine = base.load_current_execution_manifest(manifest_path)
        self.assertEqual(tuple(machine.document["source_order"]), SOURCES)
        for source in SOURCES:
            cells = DRIVER._cells_for_source(machine, source)
            self.assertEqual(tuple(cell["candidate"] for cell in cells), CANDIDATES)
            observed = DRIVER._stage_addresses(base, machine, source)
            expected = [
                f"{source}/{cell['candidate']}/{stage_id}"
                for cell in cells
                for stage_id in base._manifest_ordered_stage_ids(machine.document, cell)
            ]
            self.assertEqual(observed, expected)
            self.assertTrue(all(address.startswith(f"{source}/") for address in observed))
            self.assertTrue(all("S17" not in address and not address.startswith("COURT/")
                                for address in observed))

    def test_exact_protected_lock_rejects_a_second_driver_and_releases_cleanly(self):
        execution_root = self._exact_execution_root()
        base = DRIVER._load_base(execution_root)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = base.DriverInstanceLock(root)
            first.__enter__()
            try:
                with self.assertRaises(base.RuntimeGateError):
                    base.DriverInstanceLock(root).__enter__()
            finally:
                first.__exit__(None, None, None)
            with base.DriverInstanceLock(root):
                pass

    def test_candidate_stage_call_surface_matches_protected_driver(self):
        execution_root = self._exact_execution_root()
        protected_path = execution_root / "rawlsing_next" / "ee_p2x_darwin_court_driver.py"
        protected_tree = ast.parse(protected_path.read_text(encoding="utf-8"))
        control_tree = ast.parse(DRIVER_PATH.read_text(encoding="utf-8"))
        def method(tree, owner, name):
            cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == owner)
            return next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == name)
        canonical_run = method(protected_tree, "DarwinCourtDriver", "run")
        split_run = next(node for node in control_tree.body if isinstance(node, ast.FunctionDef)
                         and node.name == "_run_source_block")
        def calls(node):
            return {ast.unparse(child.func) for child in ast.walk(node) if isinstance(child, ast.Call)}
        canonical_calls = calls(canonical_run)
        split_calls = calls(split_run)
        for required in ("backend.run_stage", "StageContext", "_backend_terminal", "_token",
                         "_candidate_stop", ".ledger.begin"):
            self.assertTrue(any(required in call for call in canonical_calls), required)
            self.assertTrue(any(required in call for call in split_calls), required)
        self.assertIn("base._mark_source_blocked", split_calls)
        self.assertIn("_source_stop", canonical_calls)

    def test_source_filter_enforces_A_B_C_and_excludes_nonlocal_source(self):
        stages = _synthetic_stages("LITS_I") + _synthetic_stages("WVS7")
        machine = FakeMachine(stages)
        base = FakeBase()
        for source in SOURCES:
            cells = DRIVER._cells_for_source(machine, source)
            self.assertEqual(tuple(cell["candidate"] for cell in cells), CANDIDATES)
            addresses = DRIVER._stage_addresses(base, machine, source)
            self.assertEqual(addresses, [f"{source}/{candidate}/{stage_id}"
                                         for candidate in CANDIDATES
                                         for stage_id in ("S01", "S02")])
            self.assertTrue(all(address.startswith(source + "/") for address in addresses))
            self.assertFalse(any("S17" in address or address.startswith("COURT/") for address in addresses))

    def test_candidate_lifecycle_uses_same_backend_contract_and_selected_source_only(self):
        stages = _synthetic_stages("LITS_I") + _synthetic_stages("WVS7")
        machine = FakeMachine(stages)
        backend = FakeBackend()
        driver = self._fake_driver(backend)
        base = FakeBase()
        with mock.patch.object(DRIVER, "_hardware_fingerprint", return_value={"synthetic": True}), \
             mock.patch.dict(os.environ, {"RAWLSING_FIABC_SPLIT_CONTROL_HEAD": "f" * 40,
                                          "RAWLSING_FIABC_SPLIT_RUNNER_SHA256": "0" * 64}):
            terminal = DRIVER._run_source_block(base=base, driver=driver, machine=machine, source="LITS_I")
        self.assertEqual([ctx.stage.address for ctx in backend.calls], [
            f"LITS_I/{candidate}/{stage_id}" for candidate in CANDIDATES for stage_id in ("S01", "S02")
        ])
        self.assertEqual([ctx.source_path for ctx in backend.calls], [driver.source_paths["LITS_I"]] * 6)
        self.assertEqual([event[1] for event in driver.ledger.events if event[0] == "begin"],
                         [f"LITS_I/{candidate}/{stage_id}" for candidate in CANDIDATES
                          for stage_id in ("S01", "S02")])
        self.assertEqual(backend.processes_started, 0)
        self.assertEqual(terminal["candidate_order"], list(CANDIDATES))
        self.assertFalse(terminal["six_cell_s17_executed"])
        self.assertFalse(terminal["six_cell_completion_claimed"])
        self.assertFalse(terminal["measured_synthesis_performed"])
        material = {key: value for key, value in terminal.items() if key != "receipt_identity"}
        self.assertEqual(terminal["receipt_identity"], hashlib.sha256(DRIVER._canon(material)).hexdigest())

    def test_source_free_split_orchestration_all_passes_for_both_sources(self):
        for source in SOURCES:
            with self.subTest(source=source):
                machine = FakeMachine(_synthetic_stages(source))
                backend = FakeBackend()
                driver = self._fake_driver(backend, source=source)
                with mock.patch.object(
                    DRIVER, "_hardware_fingerprint", return_value={"synthetic": True}
                ), mock.patch.dict(os.environ, {
                    "RAWLSING_FIABC_SPLIT_CONTROL_HEAD": "f" * 40,
                    "RAWLSING_FIABC_SPLIT_CONTROL_CHECKOUT_HEAD": "f" * 40,
                    "RAWLSING_FIABC_SPLIT_CONTROL_BINDING_IDENTITY": "a" * 64,
                    "RAWLSING_FIABC_SPLIT_RUNNER_SHA256": "0" * 64,
                }):
                    terminal = DRIVER._run_source_block(
                        base=FakeBase(),
                        driver=driver,
                        machine=machine,
                        source=source,
                    )
                self.assertEqual(
                    terminal["status"],
                    "SOURCE_BLOCK_SEQUENCE_COMPLETE__ALL_THREE_CELLS_TERMINAL",
                )
                self.assertEqual(
                    [context.stage.address for context in backend.calls],
                    [
                        f"{source}/{candidate}/{stage_id}"
                        for candidate in CANDIDATES
                        for stage_id in ("S01", "S02")
                    ],
                )
                self.assertTrue(
                    all(context.source_path == driver.source_paths[source]
                        for context in backend.calls)
                )
                self.assertEqual(backend.processes_started, 0)
                self.assertFalse(terminal["six_cell_s17_executed"])
                self.assertFalse(terminal["measured_synthesis_performed"])

    def test_source_local_candidate_failure_matrix_covers_a_b_c_for_both_sources(self):
        for source in SOURCES:
            for failed_candidate in CANDIDATES:
                with self.subTest(source=source, failed_candidate=failed_candidate):
                    machine = FakeMachine(_synthetic_stages(source))
                    failure_address = f"{source}/{failed_candidate}/S01"
                    backend = FakeBackend(failure_address=failure_address)
                    driver = self._fake_driver(backend, source=source)
                    with mock.patch.object(
                        DRIVER, "_hardware_fingerprint", return_value={"synthetic": True}
                    ), mock.patch.dict(os.environ, {
                        "RAWLSING_FIABC_SPLIT_CONTROL_HEAD": "f" * 40,
                        "RAWLSING_FIABC_SPLIT_CONTROL_CHECKOUT_HEAD": "f" * 40,
                        "RAWLSING_FIABC_SPLIT_CONTROL_BINDING_IDENTITY": "a" * 64,
                        "RAWLSING_FIABC_SPLIT_RUNNER_SHA256": "0" * 64,
                    }):
                        terminal = DRIVER._run_source_block(
                            base=FakeBase(),
                            driver=driver,
                            machine=machine,
                            source=source,
                        )
                    self.assertEqual(
                        terminal["candidate_failure_cells"],
                        [f"{source}/{failed_candidate}"],
                    )
                    calls = [context.stage.address for context in backend.calls]
                    self.assertIn(failure_address, calls)
                    self.assertNotIn(
                        f"{source}/{failed_candidate}/S02", calls
                    )
                    later_candidates = CANDIDATES[
                        CANDIDATES.index(failed_candidate) + 1:
                    ]
                    for candidate in later_candidates:
                        self.assertIn(f"{source}/{candidate}/S01", calls)
                    self.assertEqual(backend.processes_started, 0)

    def test_source_local_common_blocker_matrices_cover_both_sources_and_scopes(self):
        for source in SOURCES:
            for scope in ("SOURCE", "COURT"):
                for blocker_candidate in CANDIDATES:
                    with self.subTest(
                        source=source,
                        scope=scope,
                        blocker_candidate=blocker_candidate,
                    ):
                        machine = FakeMachine(_synthetic_stages(source))
                        blocker_address = f"{source}/{blocker_candidate}/S01"
                        backend = FakeBackend(
                            blocker_address=blocker_address,
                            blocker_scope=scope,
                        )
                        driver = self._fake_driver(backend, source=source)
                        with mock.patch.object(
                            DRIVER,
                            "_hardware_fingerprint",
                            return_value={"synthetic": True},
                        ), mock.patch.dict(os.environ, {
                            "RAWLSING_FIABC_SPLIT_CONTROL_HEAD": "f" * 40,
                            "RAWLSING_FIABC_SPLIT_CONTROL_CHECKOUT_HEAD": "f" * 40,
                            "RAWLSING_FIABC_SPLIT_CONTROL_BINDING_IDENTITY": "a" * 64,
                            "RAWLSING_FIABC_SPLIT_RUNNER_SHA256": "0" * 64,
                        }):
                            terminal = DRIVER._run_source_block(
                                base=FakeBase(),
                                driver=driver,
                                machine=machine,
                                source=source,
                            )
                        expected = (
                            "BLOCKED__COMMON_SOURCE_AUTHORITY"
                            if scope == "SOURCE"
                            else "BLOCKED__COMMON_COURT_AUTHORITY"
                        )
                        self.assertEqual(terminal["status"], expected)
                        calls = [context.stage.address for context in backend.calls]
                        self.assertEqual(calls[-1], blocker_address)
                        self.assertEqual(len(calls), CANDIDATES.index(blocker_candidate) * 2 + 1)
                        self.assertEqual(backend.processes_started, 0)

    def test_candidate_local_failure_is_retained_without_stopping_other_candidates(self):
        machine = FakeMachine(_synthetic_stages("LITS_I"))
        first_address = "LITS_I/A/S01"
        backend = FakeBackend(failure_address=first_address)
        driver = self._fake_driver(backend)
        with mock.patch.object(DRIVER, "_hardware_fingerprint", return_value={"synthetic": True}), \
             mock.patch.dict(os.environ, {"RAWLSING_FIABC_SPLIT_CONTROL_HEAD": "f" * 40,
                                          "RAWLSING_FIABC_SPLIT_RUNNER_SHA256": "0" * 64}):
            terminal = DRIVER._run_source_block(base=FakeBase(), driver=driver, machine=machine, source="LITS_I")
        self.assertEqual([ctx.stage.address for ctx in backend.calls], [
            "LITS_I/A/S01", "LITS_I/B/S01", "LITS_I/B/S02", "LITS_I/C/S01", "LITS_I/C/S02",
        ])
        self.assertEqual(terminal["candidate_failure_cells"], ["LITS_I/A"])
        self.assertEqual(terminal["candidate_terminals"]["A"]["terminal_disposition"], "CANDIDATE_LOCAL_FAILURE")
        self.assertEqual(driver.ledger.stage_entry("LITS_I/A/S02")["terminal_disposition"],
                         "CANDIDATE_LOCAL_FAILURE")

    def test_common_source_and_court_blockers_stop_the_block_and_remain_explicit(self):
        for scope, expected, blocker in (
            ("SOURCE", "BLOCKED__COMMON_SOURCE_AUTHORITY", "BLOCKED_BY_COMMON_SOURCE_AUTHORITY"),
            ("COURT", "BLOCKED__COMMON_COURT_AUTHORITY", "BLOCKED_BY_COMMON_COURT_AUTHORITY"),
        ):
            with self.subTest(scope=scope):
                machine = FakeMachine(_synthetic_stages("LITS_I"))
                backend = FakeBackend(blocker_address="LITS_I/A/S01", blocker_scope=scope)
                driver = self._fake_driver(backend)
                with mock.patch.object(DRIVER, "_hardware_fingerprint", return_value={"synthetic": True}), \
                     mock.patch.dict(os.environ, {"RAWLSING_FIABC_SPLIT_CONTROL_HEAD": "f" * 40,
                                                  "RAWLSING_FIABC_SPLIT_RUNNER_SHA256": "0" * 64}):
                    terminal = DRIVER._run_source_block(base=FakeBase(), driver=driver,
                                                        machine=machine, source="LITS_I")
                self.assertEqual([ctx.stage.address for ctx in backend.calls], ["LITS_I/A/S01"])
                self.assertEqual(terminal["status"], expected)
                self.assertTrue(any(entry.get("terminal_disposition") == blocker
                                    for entry in driver.ledger.entries.values()))
                self.assertFalse(terminal["six_cell_s17_executed"])

    def test_source_preflight_banks_only_court_receipts_and_zero_candidate_state(self):
        machine = FakeMachine(_synthetic_stages("LITS_I") + _synthetic_stages("WVS7"))
        driver = self._fake_driver()
        base = FakeBase()
        live = types.ModuleType("rawlsing_next.fiabc_live_terminal_control")
        calls = []
        live.validate_current_court_contract_file = lambda *args: calls.append(("contract", args[0]))
        live.load_frozen_source_oracle = lambda **kwargs: calls.append(("oracle", kwargs["source"]))
        def preflight(**kwargs):
            calls.append(("t5", kwargs["repo_head"]))
            kwargs["output_path"].parent.mkdir(parents=True, exist_ok=True)
            kwargs["output_path"].write_text('{"status":"PASS"}\n', encoding="utf-8")
            return {"status": "PASS", "source": "LITS_I"}
        live.run_live_succession_preflight = preflight
        package = types.ModuleType("rawlsing_next")
        package.__path__ = []
        saved = {key: sys.modules.get(key) for key in ("rawlsing_next", "rawlsing_next.fiabc_live_terminal_control")}
        try:
            sys.modules["rawlsing_next"] = package
            sys.modules["rawlsing_next.fiabc_live_terminal_control"] = live
            with mock.patch.object(DRIVER, "_hardware_fingerprint", return_value={"synthetic": True}):
                receipt = DRIVER._source_preflight(
                    base=base, driver=driver, machine=machine, source="LITS_I",
                    source_path=Path("/synthetic/source/LiTS-I.dta"), repo_root=driver.repo_root,
                    court_contract_path=Path("/synthetic/court-contract.json"),
                    succession_manifest=Path("/synthetic/succession.json"),
                    succession_lifecycle_context=Path("/synthetic/lifecycle.json"),
                    freeze_path=Path("/synthetic/freeze.json"),
                )
        finally:
            for key in ("rawlsing_next", "rawlsing_next.fiabc_live_terminal_control"):
                sys.modules.pop(key, None)
            for key, value in saved.items():
                if value is not None:
                    sys.modules[key] = value
        self.assertEqual(driver.verified_sources, ["LITS_I"])
        self.assertEqual([name for name, _ in calls], ["contract", "oracle", "t5"])
        self.assertEqual(receipt["candidate_processes_started"], 0)
        self.assertEqual(receipt["candidate_outputs_seen"], 0)
        self.assertTrue(receipt["source_local_only"])
        self.assertFalse(receipt["six_cell_s17_authorized"])
        self.assertFalse((driver.work_root / "cells").exists())
        self.assertTrue((driver.work_root / "court" / "source_local_preflight.json").is_file())

    def test_preflight_receipt_identity_and_selected_source_are_bound(self):
        parser = DRIVER._parser()
        choices = next(action.choices for action in parser._actions if action.dest == "source")
        self.assertEqual(tuple(choices), SOURCES)
        main = next(node for node in ast.walk(ast.parse(DRIVER_PATH.read_text(encoding="utf-8")))
                    if isinstance(node, ast.FunctionDef) and node.name == "main")
        found = any(isinstance(node, ast.Assign)
                    and isinstance(node.value, ast.Dict)
                    and any(isinstance(key, ast.Attribute) and key.attr == "source" for key in node.value.keys if key)
                    for node in ast.walk(main))
        self.assertTrue(found, "driver must expose only args.source in source_paths")
        self.assertTrue(SHELL_PATH.read_text(encoding="utf-8").find('LITS_I) EXPECTED_SOURCE_SHA256=') >= 0)
        self.assertTrue(SHELL_PATH.read_text(encoding="utf-8").find('WVS7) EXPECTED_SOURCE_SHA256=') >= 0)

    def test_runtime_gate_pins_pandas_numpy_and_merge_rejects_dependency_drift(self):
        driver_source = DRIVER_PATH.read_text(encoding="utf-8")
        gate_source = (LAUNCHERS / "FIABC_SPLIT_R2_WORKROOT_GATES.py").read_text(encoding="utf-8")
        self.assertIn('"pandas": "2.3.1"', gate_source)
        self.assertIn('"numpy": "2.3.2"', gate_source)
        self.assertIn('importlib.metadata.version("pandas")', driver_source)
        self.assertIn('importlib.metadata.version("numpy")', driver_source)
        self._run_worker_d_test(
            "test_merge_rejects_canonical_source_drift_running_stage_and_hardware_mismatch"
        )

    def test_supervisor_token_matches_protected_backend_contract(self):
        text = DRIVER_PATH.read_text(encoding="utf-8")
        self.assertIn("base._token(", text)
        self.assertIn("base._backend_terminal(", text)
        self.assertIn("base.StageContext(", text)
        self.assertIn("driver.backend.run_stage(context, driver.services)", text)
        self.assertIn('"RAWLSING_LOCAL_SUPERVISOR_ACTION "', text)
        stage = Stage("LITS_I", "A")
        token = DRIVER._load_base(self._exact_execution_root())._token(
            stage, "1" * 64, "2" * 64, EXECUTION_HEAD
        )
        self.assertEqual(token["action"], "COMMIT_AND_PUSH_EXISTING_P2X_BRANCH_BOUNDED_STAGE_EVIDENCE")
        self.assertEqual(token["stage_id"], "LITS_I/A/S01")

    def test_alternate_runner_never_invokes_s17_or_authorizes_synthesis(self):
        driver_source = DRIVER_PATH.read_text(encoding="utf-8")
        shell_source = SHELL_PATH.read_text(encoding="utf-8")
        self.assertNotIn("fiabc_p2_terminal_verifier", driver_source)
        self.assertNotIn("--s17", driver_source.lower())
        self.assertIn('"six_cell_s17_executed": False', driver_source)
        self.assertIn('"p2_synthesis_authorized": False', driver_source)
        self.assertIn("SIX_CELL_S17_NOT_EXECUTED", shell_source)
        self.assertNotIn("fiabc_p2_terminal_verifier", shell_source)

    def test_merge_accepts_source_local_terminals_with_os_version_mismatch(self):
        self._run_worker_d_test(
            "test_merge_revalidates_full_ledger_and_accepts_only_same_qualified_control_by_default"
        )

    def test_merge_rejects_false_s17_claims_tampering_and_hardware_mismatch(self):
        self._run_worker_d_test(
            "test_merge_rejects_canonical_source_drift_running_stage_and_hardware_mismatch"
        )

    def test_merge_preserves_common_blockers_and_candidate_failures(self):
        self._run_worker_d_test(
            "test_merge_preserves_common_blockers_and_candidate_failures"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
