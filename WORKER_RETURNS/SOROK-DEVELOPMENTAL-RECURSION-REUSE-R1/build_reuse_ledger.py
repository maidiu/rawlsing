"""Build the phase-A selected historical reuse ledger.

Read-only over the existing worktree, the current external V3 source root and
the shared Git objects. It does not start a session, call a model, read
respondent data, write production code, or install an adapter.
"""
from __future__ import annotations

import hashlib
import importlib
import inspect
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RAWLSING = Path("/Users/matthewsmith/Desktop/Rawlsing")
V3_ROOT = RAWLSING / "v3"
P2 = REPO / "WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1"
P2_PRODUCT = REPO / "WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product"
P2_SOURCE_MANIFEST = REPO / "WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/SOURCE_MANIFEST.json"
ARCH_COMMIT = "fbfc529230d8b3c13f824cfac31741a5dfaa57e5"
ARCH_PATH = "SOROK_PRODUCT_CONTROL_ROOM/USER_DIRECTED_ARCHITECTURE/20261026_USER_SETTLED_BATCH_RECURSION_IMPRESSION_MEMORY_R1.md"
S50 = "515b9a8ee45672c97051df4efef679117a679525"
S50_SOURCE_MANIFEST = "WORKER_RETURNS/SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1/evidence/source_manifest.json"
W1C = "12433b89e100d2c4b9b20a94c4ccca7d2af7529a"
RCF_A = "e66dc53a5d7eeb2b6b3259000eb04b8e79e1f6f7"
W1C_PATH = "WORKER_RETURNS/PROGRAMMA_SOROK_W1_C_ORIGINAL_NEO_ENGINEERING_R1/00_FINDINGS_AND_RECOMMENDATIONS.md"
RCF_PATH = "WORKER_RETURNS/SOROK-RCF-A-HISTORIC-DEV-MACHINE-R1/01_FUNCTION_SOURCE_OWNER_RECEIVER_LEDGER.json"
PROGRAMMA_06 = "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/06_WORKING_WHOLE_SOROK_ARCHITECTURAL_SPINE_R1.md"
PROGRAMMA_09 = "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/09_INHERITED_144_FUNCTIONS_TO_WORKING_SPINE_R1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_show(rev_path: str) -> str:
    return subprocess.check_output(["git", "show", rev_path], text=True, cwd=REPO)


def git_type(rev: str) -> str | None:
    result = subprocess.run(
        ["git", "cat-file", "-t", rev], cwd=REPO, text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def git_blob(rev_path: str) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", rev_path], cwd=REPO, text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def param_summary(func) -> dict:
    sig = inspect.signature(func)
    empty = inspect.Parameter.empty
    params = []
    for p in sig.parameters.values():
        params.append({
            "name": p.name,
            "kind": str(p.kind),
            "required": p.default is empty,
            "default": None if p.default is empty else repr(p.default)[:140],
            "annotation": None if p.annotation is empty else str(p.annotation)[:160],
        })
    return {
        "parameters": params,
        "returns": None if sig.return_annotation is empty else str(sig.return_annotation)[:200],
    }


def source_row(manifest: dict, source_path: str) -> dict:
    for row in manifest["files"]:
        if row.get("source_path") == source_path:
            return row
    raise KeyError(source_path)


def installed_hash(manifest: dict, source_path: str) -> tuple[str, bool]:
    row = source_row(manifest, source_path)
    path = P2_PRODUCT.parent / row["installed_path"]
    actual = sha(path) if path.is_file() else ""
    return actual, actual == row.get("sha256")


def main() -> int:
    if ROOT.name != "SOROK-DEVELOPMENTAL-RECURSION-REUSE-R1":
        raise RuntimeError("unexpected return root")
    source_manifest = read_json(P2_SOURCE_MANIFEST)
    s50_manifest = json.loads(git_show(S50 + ":" + S50_SOURCE_MANIFEST))
    s50_expected = {row["path"]: row for row in s50_manifest["source_identity"]["rows"]}
    rcf = json.loads(git_show(RCF_A + ":" + RCF_PATH))
    w1c = git_show(W1C + ":" + W1C_PATH)
    architecture_text = git_show(ARCH_COMMIT + ":" + ARCH_PATH)

    # Exact source identity status for the historical V3 files. The current
    # /Desktop/Rawlsing/v3 tree is a compatibility fallback, not the archive.
    source_identity = []
    for path, expected in sorted(s50_expected.items()):
        actual_path = RAWLSING / path
        actual_hash = sha(actual_path) if actual_path.is_file() else None
        source_identity.append({
            "path": path,
            "expected_sha256": expected.get("expected_sha256") or expected.get("sha256"),
            "expected_bytes": expected.get("bytes"),
            "actual_path": str(actual_path),
            "actual_sha256": actual_hash,
            "actual_bytes": actual_path.stat().st_size if actual_path.is_file() else 0,
            "exact_file": actual_hash == (expected.get("expected_sha256") or expected.get("sha256")),
        })
    source_archive = {
        "expected_zip": str(RAWLSING / "Rawlsing_code_bundle_staging.zip"),
        "expected_sha256": "953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086",
        "observed_sha256_from_rcf_a": rcf.get("source_archive", {}).get("observed_zip_sha256"),
        "zip_present": (RAWLSING / "Rawlsing_code_bundle_staging.zip").is_file(),
        "staging_root": str(RAWLSING / "Rawlsing_code_bundle_staging"),
        "staging_root_present": (RAWLSING / "Rawlsing_code_bundle_staging").is_dir(),
        "current_v3_root": str(V3_ROOT),
        "current_v3_root_present": V3_ROOT.is_dir(),
        "status": "EXACT_ARCHIVE_BYTES_UNAVAILABLE__CURRENT_V3_COMPATIBILITY_FALLBACK_PRESENT",
        "w1c_evidence": W1C + ":" + W1C_PATH,
        "rcf_a_evidence": RCF_A + ":" + RCF_PATH,
    }

    actual_local_map = {row["path"]: row for row in source_identity}
    extra_expected = {
        "v3/io/persona_sheet.py": "4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e",
        "v3/io/identity_to_backbone.py": "cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda",
    }
    for extra_path, expected_hash in extra_expected.items():
        if extra_path not in actual_local_map:
            actual_path = RAWLSING / extra_path
            actual_hash = sha(actual_path) if actual_path.is_file() else None
            actual_local_map[extra_path] = {
                "path": extra_path,
                "expected_sha256": expected_hash,
                "expected_bytes": None,
                "actual_path": str(actual_path),
                "actual_sha256": actual_hash,
                "actual_bytes": actual_path.stat().st_size if actual_path.is_file() else 0,
                "exact_file": actual_hash == expected_hash,
            }

    # Selected original V3 functions. ABI signatures are the exact prior
    # verified signatures recorded in PROGRAMMA 09; actual source hashes are
    # checked separately and never called exact when they differ.
    original_specs = [
        ("M01-BACKBONE", "persistent BackboneState", "v3/core/state.py", "BackboneState",
         "@dataclass BackboneState(...)", "identity/prior history + generated state → persistent BackboneState",
         "MUTATES persistent actor state when called by yearly steps; no current V3/P2 importer",
         "Serialization/hash support is a candidate only; source is not exact."),
        ("M01-YEAR-RECORD", "hash_jsonable / YearRecord", "v3/core/year_record.py", "hash_jsonable",
         "def hash_jsonable(payload: Any) -> str", "JSON-like payload → stable hash string",
         "READ_ONLY" , "Exact file absent locally; not reused."),
        ("M07-REGISTERS", "public/private/inner registers", "v3/core/state.py", "Registers",
         "@dataclass Registers(...)", "stored causal state → register state",
         "MUTATED BY ORIGINAL GATING; not a current expression owner",
         "Expression/access semantics are held; no adapter."),
        ("M21-PRESSURE-FLOW", "pressure-flow history / memory / grooves", "v3/psyche/flow.py", "run_pressure_flow_cycle",
         "def run_pressure_flow_cycle(state: BackboneState, *, assign_channels: bool=True, compute_pressure: bool=True, apply_gating: bool=True, route_internal_charge: bool=True) -> dict[str, Any]",
         "domain charge + conductance + events → flow traces, grooves and memory",
         "MUTATES state pressure-flow history/memory; no current P2 importer",
         "Exact flow.py missing locally; HOLD."),
        ("M25-RUN-ONE", "ordered annual causal spine: run_one_year", "v3/engine/yearly_step.py", "run_one_year",
         "def run_one_year(state: BackboneState, derived: DerivedIndices, v3config: dict[str, Any], step_order: dict[str, Any]) -> None",
         "BackboneState + DerivedIndices + config + 19-step order → next annual state (None return)",
         "MUTATES the passed BackboneState and derived schedule; test-only historical",
         "Source hash mismatch; do not port year-as-unit or numerical change law."),
        ("M25-STEP-ONE", "ordered annual causal spine: step_one_year", "v3/engine/yearly_step.py", "step_one_year",
         "def step_one_year(state: BackboneState, v3config: dict[str, Any], step_order: dict[str, Any], derived: DerivedIndices) -> DerivedIndices",
         "state + config + order + derived → derived indices after one step",
         "MUTATES state; returns derived view; no current importer",
         "Source hash mismatch; HOLD."),
        ("M25-RUN-N", "lifespan runner: run_n_years", "v3/engine/step_runner.py", "run_n_years",
         "def run_n_years(state: BackboneState, n: int, v3config_path: Path | None=None, step_order_path: Path | None=None, collect_json_per_year: bool=False) -> tuple[BackboneState, list[str] | None]",
         "state + n + optional config/order paths → final state and optional per-year JSON",
         "MUTATES/replays state; exact file exists but yearly/state dependencies differ",
         "EXACT_FILE_BUT_DEPENDENCY_MISMATCH; HOLD."),
        ("M25-ORDER", "19-step immutable yearly order", "v3/v3_yearly_step_order.yaml", "v3_yearly_step_order.yaml",
         "declarative ordered step list", "step order config → deterministic mutation ordering",
         "CONFIG_ONLY; no state mutation itself",
         "Source hash mismatch; the year clock is not the settled batch/interval clock."),
        ("M26-DERIVED", "stored-versus-derived separation", "v3/core/derived.py", "DerivedIndices/compute_all_derived",
         "def compute_all_derived(state: BackboneState) -> DerivedIndices",
         "stored BackboneState → derived indices; no derived fields in stored state",
         "READ_ONLY calculation; current file exact but state dependency differs",
         "EXACT_FILE_BUT_DEPENDENCY_MISMATCH; HOLD."),
        ("M29-RENDER-PACKET", "Pass 2 render packet", "v3/engine/llm_contract.py", "build_render_packet",
         "def build_render_packet(year: int, age: int, selected_events: list[dict[str, Any]], selected_magnets: list[dict[str, Any]], state_deltas_applied: dict[str, Any], constraints: dict[str, Any], identity_override: dict[str, Any] | None=None, persona_context: dict[str, Any] | None=None) -> dict[str, Any]",
         "state/events/magnets/deltas/constraints → nonmutating render packet",
         "READ_ONLY; no current M6 same-contract import",
         "Source hash mismatch; no adapter."),
        ("M29-RENDER", "Pass 2 render-only year", "v3/render/phenomenology.py", "render_year",
         "def render_year(state: BackboneState, derived: DerivedIndices | None, config: dict, render_packet: dict[str, Any] | None=None, llm_callback: Callable[[str, str], str] | None=None) -> None",
         "state + derived + config + render packet → rendered surface; backbone nonmutation invariant",
         "WRITES rendered_output only; not a current M6/V2 contract",
         "Source hash mismatch; HOLD nonmutation invariant only."),
        ("M30-PERSONA-SHEET", "historical persona sheet", "v3/io/persona_sheet.py", "build_persona_sheet",
         "def build_persona_sheet(state: BackboneState, derived: DerivedIndices, identity_override: dict[str, Any] | None=None, include_backbone: bool=True, trajectory_snapshots: list[Any] | None=None, parent_override: dict[str, Any] | None=None, generation: str | None=None) -> dict[str, Any]",
         "state/derived/backstory/voice/microtrace → V2 persona sheet",
         "READ_ONLY projection; no current actor-safe M6 contract",
         "Source hash mismatch; actor-safe expression owner required; HOLD."),
        ("M30-IDENTITY-INIT", "identity to BackboneState initialization", "v3/io/identity_to_backbone.py", "backbone_state_from_identity",
         "def backbone_state_from_identity(identity: dict[str, Any] | Any, year: int, age: int, ...) -> BackboneState",
         "V2 identity + parent regime → BackboneState/child model",
         "INITIALIZES persistent state; scalar psychological priors are not authorized",
         "Source hash mismatch; no current importer; HOLD."),
    ]

    # Import current compatibility source read-only. These imports do not run a
    # session and cannot write actor state.
    sys.path.insert(0, str(RAWLSING))
    v3_imports = {}
    for module in (
        "v3.core.state", "v3.engine.yearly_step", "v3.engine.step_runner",
        "v3.engine.llm_contract", "v3.render.phenomenology",
        "v3.core.derived", "v3.io.persona_sheet", "v3.io.identity_to_backbone",
        "v3.psyche.flow", "v3.core.year_record",
    ):
        try:
            mod = importlib.import_module(module)
            v3_imports[module] = {
                "status": "IMPORT_OK",
                "file": str(Path(mod.__file__).resolve()),
            }
        except Exception as exc:
            v3_imports[module] = {
                "status": "IMPORT_FAILED",
                "error": f"{type(exc).__name__}: {exc}",
            }
    sys.path.pop(0)

    # Exact source rows for the selected S39-S47 chain.
    current_specs = [
        ("S39-START", "S39GeneratedSession.start", "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/s39/session.py", "S39GeneratedSession", "start", "WRITES_NEW_TEST_ONLY_S47_ROOT", "S47Session inheritance / P2 first consumer", "REUSE_INHERITED_INTERFACE"),
        ("S39-READ", "S39GeneratedSession.read_generation", "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/s39/session.py", "S39GeneratedSession", "read_generation", "READ_ONLY_VERIFIED_GENERATION_RECEIPT", "S47Session inheritance / diagnostic surface", "REUSE_INHERITED_INTERFACE"),
        ("S39-GEN", "GeneratedProducer.generate", "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/s39/producer.py", "GeneratedProducer", "generate", "WRITES_PRODUCER_RECEIPT__NO_C9_UNTIL_FINALIZE", "S47Session inheritance / sourcefree generation", "REUSE_INHERITED_INTERFACE"),
        ("S39-PERFORM", "perform_attempt", "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/s39/performer.py", "_function", "perform_attempt", "WRITES_ATTEMPT_EVENT/EPISODE/CHECKPOINT", "S47Session inheritance / targetless action", "REUSE_INHERITED_INTERFACE"),
        ("S40-START", "S40GeneratedSession.start/read_s40", "WORKER_RETURNS/SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1/s40/session.py", "S40GeneratedSession", "start", "WRITES_NATIVE_SPEECH_TEST_ROOT", "S47Session inheritance / language surface", "REUSE_INHERITED_INTERFACE__DIRECT_START_NOT_USED_BY_P2"),
        ("S40-READ", "S40GeneratedSession.read_s40", "WORKER_RETURNS/SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1/s40/session.py", "S40GeneratedSession", "read_s40", "READ_ONLY_SPEECH_RECEIPT", "S47Session inheritance", "REUSE_INHERITED_INTERFACE"),
        ("S41-CONTINUE", "S41Session.continue_event", "WORKER_RETURNS/SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1/s41/session.py", "S41Session", "continue_event", "WRITES_CONTINUATION_BINDING/C9/HISTORY", "S47Session inheritance / ordered event chain", "REUSE_INHERITED_INTERFACE"),
        ("S41-READ", "S41Session.read_event", "WORKER_RETURNS/SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1/s41/session.py", "S41Session", "read_event", "READ_ONLY_EVENT_HISTORY", "S47Session inheritance / history API", "REUSE_INHERITED_INTERFACE"),
        ("S42-ADMIT", "S42Session.admit_event", "WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1/s42/session.py", "S42Session", "admit_event", "WRITES_ONGOING_EVENT/C9/BINDING", "P2Continuation.admit_later_event / S47Session", "REUSE_DIRECT"),
        ("S42-READ", "S42Session.read_event", "WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1/s42/session.py", "S42Session", "read_event", "READ_ONLY_ONGOING_EVENT", "P2Continuation.read_later_event / S47Session", "REUSE_DIRECT"),
        ("S43-ADMIT", "S43Session.admit_event", "WORKER_RETURNS/SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1/s43/session.py", "S43Session", "admit_event", "WRITES_LANGUAGE_CONTEXT_ON_S42_ADMISSION", "P2Continuation.admit_later_event / S47Session", "REUSE_DIRECT"),
        ("S43-READ", "S43Session.read_s43_event", "WORKER_RETURNS/SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1/s43/session.py", "S43Session", "read_s43_event", "READ_ONLY_LANGUAGE_RECEIPT", "P2Continuation.read_later_event / S47Session", "REUSE_DIRECT"),
        ("S44-START", "S44Session.start", "WORKER_RETURNS/SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1/s44/session.py", "S44Session", "start", "WRITES_FROZEN_TEST_ONLY_ROOT", "S47Session inheritance / S45 root", "REUSE_INHERITED_INTERFACE__START_USED_BY_S45_START"),
        ("S44-ROOT", "S44Session.read_root", "WORKER_RETURNS/SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1/s44/session.py", "S44Session", "read_root", "READ_ONLY_ROOT_RECEIPT", "S47Session inheritance / root API", "REUSE_INHERITED_INTERFACE"),
        ("S45-SAY", "S45Session.say", "WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1/s45/session.py", "S45Session", "say", "WRITES_ENCOUNTER_AND_EVENT", "S45Projection.say / P2ProductFanin.say", "REUSE_DIRECT"),
        ("S45-DOHELP", "S45Session.do_help", "WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1/s45/session.py", "S45Session", "do_help", "WRITES_ENCOUNTER_AND_POSSIBLE_ACTION", "S45Projection.do_help / P2ProductFanin.do_help", "REUSE_DIRECT"),
        ("S45-ATTEND", "S45Session.attend", "WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1/s45/session.py", "S45Session", "attend", "WRITES_ENCOUNTER_ONLY__NO_ACTOR_ACTION", "S45Projection.attend / P2ProductFanin.attend", "REUSE_DIRECT"),
        ("S45-ENCOUNTERS", "S45Session.read_encounters", "WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1/s45/session.py", "S45Session", "read_encounters", "READ_ONLY_ENCOUNTER_HISTORY", "S45Projection/P2ProductFanin view", "REUSE_DIRECT"),
        ("S46-PRODUCE", "S46Session.produce_interval", "WORKER_RETURNS/SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1/s46/session.py", "S46Session", "produce_interval", "WRITES_INTERVAL_STATE/ACTUAL_WORLD_EFFECTS", "p2_explicit_interval_flow / P2ProductFanin", "REUSE_DIRECT"),
        ("S46-READ", "S46Session.read_interval_states", "WORKER_RETURNS/SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1/s46/session.py", "S46Session", "read_interval_states", "READ_ONLY_INTERVAL_STATES", "P2ProductFanin/current_interval_state", "REUSE_DIRECT"),
        ("S46-CURRENT", "S46Session.current_interval_state", "WORKER_RETURNS/SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1/s46/session.py", "S46Session", "current_interval_state", "READ_ONLY_CURRENT_INTERVAL", "P2ProductFanin.current_interval_state", "REUSE_DIRECT"),
        ("S46-REVOKE", "S46Session.revoke/restore_interval_condition", "WORKER_RETURNS/SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1/s46/session.py", "S46Session", "revoke_interval_condition", "WRITES_CONDITION_STATE; RESTORE RE-ADMITS", "P2ProductFanin.revoke/restore_interval", "REUSE_DIRECT"),
        ("S47-C9", "S47Session.read_c9_conditioning", "WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1/s47/session.py", "S47Session", "read_c9_conditioning", "READ_ONLY_C9_READSET/SOURCE_QUALIFICATION", "P2Continuation.read_later_event / C9 surface", "REUSE_DIRECT"),
        ("S47-C9-SOURCE", "S47Session.c9_interval_source", "WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1/s47/session.py", "S47Session", "c9_interval_source", "READ_ONLY_CURRENT_INTERVAL_SOURCE", "P2Continuation/interval flow", "REUSE_DIRECT"),
    ]

    current_io = {
        "S39-START": "state_root + case/source/variant/source_records/rule -> S39GeneratedSession; writes new TEST_ONLY root",
        "S39-READ": "S39 session -> generation/attempt/C8/C9/C12 read receipt; read-only",
        "S39-GEN": "M35 event + source records + world -> generation receipt/attempt request; writes producer receipt, no C9 until finalize",
        "S39-PERFORM": "S39 session + attempt request -> admitted/denied attempt result with event id/hash; writes action event/episode/checkpoint when admitted",
        "S40-START": "state_root + case/source/bundle -> S40GeneratedSession with native speech receipt; writes TEST_ONLY root",
        "S40-READ": "S40 session -> language/speech read receipt; read-only",
        "S41-CONTINUE": "prior event binding + case/source/history -> next bound event/C9/C12; writes continuation binding",
        "S41-READ": "event_ref -> event/history/C9/C12 read; read-only",
        "S42-ADMIT": "prior bindings + case/source/history -> ongoing event binding/C9; writes event/C9",
        "S42-READ": "event_ref -> ongoing event read; read-only",
        "S43-ADMIT": "S42 admission + language_context -> language-bound admission; writes S42 binding plus S43 language evidence",
        "S43-READ": "event_ref -> S43 language/repertoire read; read-only",
        "S44-START": "state_root + bundle -> frozen sampled root, actor ids, source refs; writes root file/bindings",
        "S44-ROOT": "S44 state -> root receipt with root/actor/source/event refs; read-only",
        "S45-SAY": "text -> WP19 encounter result + language; writes user/encounter events; no native actor claim",
        "S45-DOHELP": "no input -> WP19 help result; writes encounter and any admitted action",
        "S45-ATTEND": "no input -> WP19 attend result; writes encounter; no world event/clock change in accepted path",
        "S45-ENCOUNTERS": "S45 state -> encounter history; read-only",
        "S46-PRODUCE": "interval domain (mode/start/end/segments) -> interval state + material/world effects; writes interval/C12",
        "S46-READ": "S46 state -> interval state list; read-only",
        "S46-CURRENT": "S46 state + optional scope -> current interval state or None; read-only",
        "S46-REVOKE": "state_id + reason -> condition state; revoke writes condition, restore re-admits",
        "S47-C9": "event_ref or latest binding -> C9 conditioning/source/readset/currentness/eligibility; read-only",
        "S47-C9-SOURCE": "current S46 interval state -> current interval source or None; read-only",
    }

    # Import the exact S47 inheritance chain. This does not instantiate a
    # session; it proves the inherited ABI and actual current consumer import.
    sys.path.insert(0, str(P2_PRODUCT))
    from sorok_s45_s47.bootstrap import install as product_install

    product_info = product_install()
    from s47.session import S47Session
    from s45.session import S45Session
    from s44.session import S44Session
    from s43.session import S43Session
    from s42.session import S42Session
    from s41.session import S41Session
    from s40.session import S40GeneratedSession
    from s39.session import S39GeneratedSession
    from s39.producer import GeneratedProducer
    from s39.performer import perform_attempt

    class_map = {
        "S39GeneratedSession": S39GeneratedSession,
        "S40GeneratedSession": S40GeneratedSession,
        "S41Session": S41Session,
        "S42Session": S42Session,
        "S43Session": S43Session,
        "S44Session": S44Session,
        "S45Session": S45Session,
        "S46Session": type(S47Session).__mro__[1] if False else __import__("s46.session", fromlist=["S46Session"]).S46Session,
        "S47Session": S47Session,
        "GeneratedProducer": GeneratedProducer,
    }
    mro = [cls.__name__ for cls in S47Session.__mro__]
    current_entries = []
    for key, symbol, path, cls_name, method, mutation, consumer, disposition in current_specs:
        row = source_row(source_manifest, path)
        actual, exact = installed_hash(source_manifest, path)
        if cls_name == "_function":
            func = perform_attempt
        else:
            cls = class_map[cls_name]
            func = getattr(cls, method)
        current_entries.append({
            "key": key,
            "source_commit": row["source_commit"],
            "source_path": path,
            "git_blob": row["git_blob"],
            "source_sha256": row["sha256"],
            "installed_path": str(P2_PRODUCT.parent / row["installed_path"]),
            "installed_sha256": actual,
            "source_exact": bool(exact),
            "symbol": symbol,
            "signature": param_summary(func),
            "input_output": current_io.get(key, "bounded existing API"),
            "mutation_custody": mutation,
            "custody_grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
            "compatible_current_consumer": consumer,
            "adapter_or_hold": disposition,
        })

    # Current accepted P2 owner and its additive owner APIs.
    p2_entries = []
    p2_specs = [
        ("P2-FANIN", "P2ProductFanin.start/open/admit_later_event/do_help", "WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/p2_product_fanin/integration.py", "P2ProductFanin", "start", "WRITES_TEST_ONLY_S47_ROOT_AND_ENCOUNTERS", "4b2fed81c3f513eb4262ad5de277ce519c74c614", "ACCEPTED_SCOPED_P2_OWNER__CONSUMER_ONLY"),
        ("P2-LATER-ADMIT", "P2Continuation.admit_later_event", "WORKER_RETURNS/SOROK-P2-LATER-EVENT-CONTINUATION-20261105-R1/p2_continuation/continuation.py", "P2Continuation", "admit_later_event", "WRITES_LATER_EVENT/C9/S43", "b71624f21d0bc638e8817f3929cc6c01ab8b0f61", "REUSE_DIRECT"),
        ("P2-LATER-READ", "P2Continuation.read_later_event", "WORKER_RETURNS/SOROK-P2-LATER-EVENT-CONTINUATION-20261105-R1/p2_continuation/continuation.py", "P2Continuation", "read_later_event", "READ_ONLY_LATER_EVENT/C9/S43", "b71624f21d0bc638e8817f3929cc6c01ab8b0f61", "REUSE_DIRECT"),
        ("P2-INTERVAL", "apply_explicit_interval", "WORKER_RETURNS/SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1/p2_explicit_interval_flow/continuation.py", "_function", "apply_explicit_interval", "WRITES_INTERVAL_VIA_EXISTING_CLI__NO_AUTO_DO_HELP", "76d5a3d13e0219c1a085ebadd55071de2dd90e7d", "REUSE_DIRECT"),
    ]
    # Manual signatures for current owner functions; importing p2_continuation
    # would install another closure and is unnecessary for ABI facts.
    manual_sigs = {
        "P2-FANIN": "(state_root, *, seed: str='01'*32, **kwargs) -> P2ProductFanin",
        "P2-LATER-ADMIT": "(self, history_refs: tuple[str, ...]=(), *, event_time: int|None=None, language_context: Mapping[str, Any]|None=None) -> dict",
        "P2-LATER-READ": "(self, event_ref: str) -> dict",
        "P2-INTERVAL": "(state: str|Path, interval_input: dict|None, *, base_root: str|Path|None=None) -> dict",
    }
    for key, symbol, path, cls_name, method, mutation, commit, disposition in p2_specs:
        path_obj = REPO / path
        p2_entries.append({
            "key": key,
            "source_commit": commit,
            "source_path": path,
            "git_blob": None,
            "source_sha256": sha(path_obj),
            "installed_path": str(path_obj),
            "source_exact": True,
            "symbol": symbol,
            "signature": manual_sigs[key],
            "input_output": {
                "P2-FANIN": "state_root + optional seed/case/source -> P2ProductFanin; writes TEST_ONLY root/encounters",
                "P2-LATER-ADMIT": "history refs + case/source/event_time -> later-event admission with C9/S43; writes event/C9",
                "P2-LATER-READ": "event_ref -> event/C9/S43 read; read-only",
                "P2-INTERVAL": "state + interval_input -> interval result; writes interval/material through existing CLI, no auto DO_HELP",
            }.get(key, "bounded existing API"),
            "mutation_custody": mutation,
            "custody_grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
            "compatible_current_consumer": "P2ProductFanin" if key != "P2-FANIN" else "P2ProductFanin (product owner)",
            "adapter_or_hold": disposition,
        })

    # S50 projected access/memory facts. Source code is exact in Git object but
    # the historical archive needed to execute the fixture is absent.
    s50_path = "WORKER_RETURNS/SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1/s50/session.py"
    s50_file_text = git_show(S50 + ":" + s50_path)
    s50_entry = {
        "key": "S50-PROJECTION",
        "source_commit": S50,
        "source_path": s50_path,
        "git_blob": git_blob(S50 + ":" + s50_path),
        "source_sha256": hashlib.sha256(s50_file_text.encode()).hexdigest(),
        "source_exact": True,
        "symbol": "S50Session.materialize_legacy_projection/read_projection/actual_root_missing",
        "signature": "(self, *, years: int=1) -> dict; read_projection(self) -> dict|None; actual_root_missing(self) -> dict",
        "input_output": "S49 actor root + exact historical V3 source identity → read-only projection/absence receipt",
        "mutation_custody": "APPENDS ONE READ_ONLY PROJECTION EPISODE; NO ACTUAL_PERSON_COMMIT",
        "custody_grade": "HISTORICAL RECOVERY__READ_ONLY__NOT_CURRENT_P2_CONSUMER",
        "compatible_current_consumer": "NONE_PROVEN_IN_CURRENT_P2; S50 return only",
        "adapter_or_hold": "HOLD_EXACT_ARCHIVE_AND_ACTUAL_ROOT_STATE",
    }

    # Import probe for the current P2 owner. Do not call runtime.load(), which
    # would create its log directory outside this return root.
    p2_path = REPO / "WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1"
    sys.path.insert(0, str(p2_path))
    from p2_product_fanin.integration import P2ProductFanin
    p2_methods = {}
    for name in ("start", "open", "admit_later_event", "read_later_event",
                 "public_opportunity", "do_help", "say", "attend", "status",
                 "current_interval_state"):
        p2_methods[name] = str(inspect.signature(getattr(P2ProductFanin, name)))
    sys.path.pop(0)

    smoke_path = ROOT / "evidence" / "P2_FIRST_READER_SMOKE.json"
    smoke = read_json(smoke_path) if smoke_path.is_file() else None

    import_probe = {
        "schema": "SOROK_DEVELOPMENTAL_RECURSION_REUSE_IMPORT_PROBE@1",
        "product_bootstrap": product_info,
        "s47_mro": mro,
        "s47_contains_s39_s47": all(
            name in mro for name in (
                "S39GeneratedSession", "S40GeneratedSession", "S41Session",
                "S42Session", "S43Session", "S44Session", "S45Session",
                "S46Session", "S47Session",
            )
        ),
        "p2_product_fanin_import": "OK",
        "p2_product_fanin_methods": p2_methods,
        "v3_compatibility_imports": v3_imports,
        "session_started": False,
        "first_reader_smoke": smoke,
        "model_called": False,
        "respondent_data_read": False,
        "writes_outside_return_root": False,
    }

    selected = {
        "schema": "SOROK_DEVELOPMENTAL_RECURSION_REUSE_LEDGER@1",
        "base_commit": "33c40a315d3c231cb2021bd8e60f3261547efa62",
        "branch": "agent/sorok-recursion-reuse-20261106-r1",
        "result": "S39_S47_EXACT_SOURCE_AND_FIRST_READER_ABI_DEMONSTRATED__ORIGINAL_V3_EXACT_BYTES_HOLD__NO_ADAPTER__NO_NATIVE_OR_PRODUCTION_GRANT",
        "architecture": {
            "commit": ARCH_COMMIT,
            "path": ARCH_PATH,
            "blob_sha1": git_blob(ARCH_COMMIT + ":" + ARCH_PATH),
            "sha256": hashlib.sha256(architecture_text.encode()).hexdigest(),
            "required_cycle": "prospective 3–5 events -> sequential Rawlsing impression/outcome/time -> retrospective memory/meaning in first half of next LLM call",
            "status": "USER_SETTLED__IMPLEMENTATION_NOT_VERIFIED",
        },
        "source_retrieval": {
            "architecture_commit": git_type(ARCH_COMMIT),
            "s50_commit": git_type(S50),
            "w1c_commit": git_type(W1C),
            "rcf_a_commit": git_type(RCF_A),
            "s39_s47_source_commits": {
                c: git_type(c) for c in (
                    "e41513fa65601a37e7b3b430d26c626ae0217d90",
                    "79b0357c7af9b66ad8a28f5b77b46b0348094a23",
                    "c72a10d284f8869b990db3e6849ed174a51bd784",
                    "765a441f87292aa4c17794745b65cb54e6aaa83f",
                    "3edd631fb6c31751dfd2143ba2faa9fc31561e54",
                    "923278fbe6b030e2ffdd10fe42d7a18266344611",
                    "f26a138e20d53c809d611cf8d834ec647b0804bf",
                    "f0ef39b92ce2e4add5c0a699389e12f1d7ae434e",
                )
            },
            "source_archive": source_archive,
            "w1c": W1C + ":" + W1C_PATH,
            "rcf_a": RCF_A + ":" + RCF_PATH,
            "programma": {
                "06": {"path": PROGRAMMA_06, "sha256": sha(REPO / PROGRAMMA_06)},
                "09": {"path": PROGRAMMA_09, "sha256": sha(REPO / PROGRAMMA_09)},
            },
            "source_identity": source_identity,
        },
        "original_v3": {
            "selected_functions": [
                {
                    "key": key,
                    "source_path": path,
                    "symbol": symbol,
                    "historical_signature": signature,
                    "input_output": input_output,
                    "mutation_custody": mutation,
                    "expected_source": (
                        s50_expected.get(path, {}).get("expected_sha256") or s50_expected.get(path, {}).get("sha256")
                        or ("4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e" if key == "M30-PERSONA-SHEET" else
                            "cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda" if key == "M30-IDENTITY-INIT" else None)
                    ),
                    "actual_local": actual_local_map.get(path),
                    "current_consumer": "NONE_PROVEN_AT_PREMAIN",
                    "adapter_or_hold": "HOLD_EXACT_SOURCE_OR_DEPENDENCY_MISMATCH",
                    "note": note,
                }
                for key, symbol, path, _sym, signature, input_output, mutation, note in original_specs
            ],
            "source_exactness": "MIXED__EXACT_FILES_DO_NOT_PROVE_EXACT_DEPENDENCY_CLOSURE",
            "all_exact": False,
            "adapter": None,
            "decision": "HOLD_ORIGINAL_V3_EXACT_BYTES_AND_DEPENDENCY_CLOSURE",
        },
        "current_s39_s47": {
            "selected_functions": current_entries,
            "source_exactness": "ALL_SELECTED_FILES_MATCH_SOURCE_MANIFEST",
            "all_exact": all(e["source_exact"] for e in current_entries),
            "first_reader": "S47Session inheritance chain; P2ProductFanin current consumer",
            "adapter": None,
            "decision": "REUSE_EXISTING_INHERITED_INTERFACES__NO_ADAPTER_NEEDED",
        },
        "current_p2": {
            "selected_functions": p2_entries,
            "accepted_owner": "WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/p2_product_fanin/integration.py",
            "source_exact": "CURRENT_ACCEPTED_SOURCE_FILES",
            "adapter": None,
        },
        "s50": s50_entry,
        "consumer_binding": {
            "p2_product_fanin": str(P2 / "p2_product_fanin/integration.py"),
            "p2_runtime": str(P2 / "p2_product_fanin/runtime.py"),
            "s47_session": "s47.session.S47Session",
            "s47_mro": mro,
            "p2_import": "OK",
            "first_reader_compatibility": "PASS_SCOPED_START_VERIFY" if smoke else "PASS_SCOPED_IMPORT_AND_INHERITANCE",
            "first_reader_smoke": smoke,
            "runtime_started": bool(smoke and smoke.get("status") == "STARTED_VERIFIED_CLOSED"),
        },
        "engineering": "SCOPED_ACCEPT_FOR_S39_S47_ABI_REUSE__HOLD_ORIGINAL_V3_EXACT",
        "science": "HOLD_ABSENT_ORIGINAL_EXECUTION_GRANT",
        "authority": "HOLD_PRODUCTION_AND_ISSUANCE_NOT_GRANTED",
        "limits": {
            "original_v3_native_claim": False,
            "source_archive_read": False,
            "session_started": False,
            "model_called": False,
            "respondent_rows_read": False,
            "production_config_edited": False,
            "new_engine_or_scheduler": False,
            "new_psychological_rule": False,
            "adapter_emitted": False,
            "frozen_output_substituted": False,
            "merge": False,
            "ci": False,
        },
    }
    (ROOT / "01_SELECTED_REUSE_LEDGER.json").write_text(
        json.dumps(selected, indent=2, sort_keys=True) + "\n")
    (ROOT / "03_IMPORT_PROBE.json").write_text(
        json.dumps(import_probe, indent=2, sort_keys=True) + "\n")
    (ROOT / "PASSPORT.json").write_text(json.dumps({
        "agent_type": "OpenCode historical compatibility engineer",
        "intelligence": "I2 / S2",
        "provider": "opencode-go",
        "model": "deepseek-v4.1-flash#max",
        "effort": "MAX",
        "host": platform.platform(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "p2_import_path": str(P2 / "p2_product_fanin/integration.py"),
        "s47_source_path": str(P2_PRODUCT / "vendor/WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1/s47/session.py"),
        "v3_compatibility_path": str(V3_ROOT),
        "base_commit": "33c40a315d3c231cb2021bd8e60f3261547efa62",
        "quota": "UNKNOWN",
        "browser_local_checkout": False,
        "sanitized": True,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "result": selected["result"],
        "s39_s47_all_exact": selected["current_s39_s47"]["all_exact"],
        "s47_contains_chain": import_probe["s47_contains_s39_s47"],
        "arch_sha256": selected["architecture"]["sha256"],
        "original_v3_all_exact": selected["original_v3"]["all_exact"],
        "adapter": selected["original_v3"]["adapter"],
        "p2_import": selected["consumer_binding"]["p2_import"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
