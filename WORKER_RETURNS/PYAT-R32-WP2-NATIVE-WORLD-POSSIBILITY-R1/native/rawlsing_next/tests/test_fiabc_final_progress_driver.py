from __future__ import annotations

import io
import json
from pathlib import Path
from types import SimpleNamespace

from rawlsing_next import ee_p2x_darwin_court_driver as d
from rawlsing_next import ee_p2x_darwin_stage_backend as backend


def _stage(source: str, candidate: str, sid: str, disposition: str, next_stage: str) -> d.StageSpec:
    return d.StageSpec(
        source=source,
        candidate=candidate,
        stage_id=sid,
        disposition=disposition,
        evidence_or_stop_law_ref=None,
        empirical_source_access_required=False,
        physical_host_measurement_required=False,
        next_stage_on_pass=next_stage,
        executable_prerequisite="TEST",
        expected_output_receipt="TEST",
        next_stage_on_candidate_local_failure=next_stage,
    )


def _machine(
    cells: list[tuple[str, str, list[tuple[str, str]]]],
    *,
    first_unfinished: str,
) -> d.StateMachine:
    stage_catalog: list[str] = []
    doc_cells = []
    stages: dict[str, d.StageSpec] = {}
    for source, candidate, cell_stages in cells:
        for sid, _ in cell_stages:
            if sid not in stage_catalog:
                stage_catalog.append(sid)
        sm = {}
        doc_cells.append({"source": source, "candidate": candidate, "stages": sm})
        for i, (sid, disposition) in enumerate(cell_stages):
            next_stage = (
                f"{source}/{candidate}/{cell_stages[i + 1][0]}"
                if i + 1 < len(cell_stages)
                else "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"
            )
            sm[sid] = [disposition, None, False, False, next_stage]
            spec = _stage(source, candidate, sid, disposition, next_stage)
            stages[spec.address] = spec
    final = _stage(
        "COURT",
        "ALL",
        "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        "READY__RUN_LOCALLY",
        "__COURT_COMPLETE__",
    )
    stages[final.address] = final
    source_order = list(dict.fromkeys(source for source, _, _ in cells))
    candidate_order = list(dict.fromkeys(candidate for _, candidate, _ in cells))
    doc = {
        "schema": d.CURRENT_EXECUTION_MANIFEST_SCHEMA,
        "source_order": source_order,
        "candidate_order": candidate_order,
        "sources": {source: {"display_name": source.replace("_", "-")} for source in source_order},
        "stage_catalog": stage_catalog,
        "cells": doc_cells,
        "entry_guard": {"first_unfinished_court_stage": first_unfinished},
        "final_stage": {"stage_id": final.stage_id},
    }
    ident = d.MapIdentity(d.CURRENT_EXECUTION_MANIFEST_SCHEMA, "a" * 64, "b" * 40)
    return d.StateMachine(doc, ident, stages, first_unfinished, final.address)


def _six_cell_machine() -> d.StateMachine:
    cells = []
    for source in ("LITS_I", "WVS7"):
        for candidate in ("A", "B", "C"):
            cells.append(
                (
                    source,
                    candidate,
                    [
                        ("S00_PREFLIGHT", "DONE__PRESERVE"),
                        ("S01_BUILD", "READY__RUN_LOCALLY"),
                    ],
                )
            )
    return _machine(cells, first_unfinished="LITS_I/A/S01_BUILD")


def test_progress_counts_and_ordinals_derive_from_arbitrary_manifest_shape():
    machine = _machine(
        [
            ("SRC1", "A", [("S00_ZERO", "DONE__PRESERVE"), ("S01_ONE", "READY__RUN_LOCALLY")]),
            (
                "SRC2",
                "B",
                [
                    ("S00_ZERO", "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW"),
                    ("S01_ONE", "READY__RUN_LOCALLY"),
                    ("S02_TWO", "DONE__PRESERVE"),
                ],
            ),
        ],
        first_unfinished="SRC1/A/S01_ONE",
    )
    plan = d.ManifestProgressPlan(machine)
    assert plan.overall_total == 5
    assert plan.executable_total == 3
    assert plan.cell_total == 2

    pos = plan.position("SRC2/B/S00_ZERO")
    assert (pos.overall_index, pos.overall_total) == (2, 5)
    assert pos.executable_index is None
    assert (pos.cell_index, pos.cell_total) == (2, 2)
    assert (pos.stage_index, pos.stage_total) == (1, 3)

    final = plan.position(machine.final_stage_id)
    assert final.is_court_final is True
    assert final.overall_index == final.overall_total == 5
    assert final.executable_index == final.executable_total == 3


def test_six_cell_manifest_order_is_manifest_derived_and_includes_wvs7_c():
    machine = _six_cell_machine()
    plan = d.ManifestProgressPlan(machine)
    pos = plan.position("WVS7/C/S01_BUILD")
    assert (pos.cell_index, pos.cell_total) == (6, 6)
    assert (pos.stage_index, pos.stage_total) == (2, 2)
    assert pos.overall_index == 11
    assert plan.overall_total == 12


def test_resume_progress_is_append_only_and_retains_total_context(tmp_path: Path):
    machine = _machine(
        [
            (
                "SRC",
                "A",
                [
                    ("S00_FIRST", "READY__RUN_LOCALLY"),
                    ("S01_SECOND", "READY__RUN_LOCALLY"),
                ],
            )
        ],
        first_unfinished="SRC/A/S00_FIRST",
    )
    ledger = d.StageLedger(tmp_path / "work", machine, tmp_path)
    first_stream = io.StringIO()
    first = d.ProgressReporter(machine, ledger, stream=first_stream, clock=lambda: 10)
    stage0 = machine.get("SRC/A/S00_FIRST")
    first.emit_stage(stage0, "START", next_stage=None, elapsed_stage_ns=None)
    first.emit_stage(stage0, "PASS", next_stage="SRC/A/S01_SECOND", elapsed_stage_ns=7, terminal_disposition="PASS")
    before = first.path.read_text(encoding="utf-8").splitlines()

    resumed_stream = io.StringIO()
    resumed = d.ProgressReporter(machine, ledger, stream=resumed_stream, clock=lambda: 20)
    resumed.emit_stage(stage0, "START", next_stage=None, elapsed_stage_ns=None)
    resumed.emit_stage(stage0, "PASS", next_stage="SRC/A/S01_SECOND", elapsed_stage_ns=99, terminal_disposition="PASS")
    stage1 = machine.get("SRC/A/S01_SECOND")
    resumed.emit_stage(stage1, "START", next_stage=None, elapsed_stage_ns=None)

    after = resumed.path.read_text(encoding="utf-8").splitlines()
    assert len(after) == len(before) + 1
    event = json.loads(after[-1])
    assert event["address"] == "SRC/A/S01_SECOND"
    assert event["state"] == "START"
    assert event["overall"] == {"index": 2, "total": 3}
    assert event["executable"] == {"index": 2, "total": 3, "is_executable": True}


def test_progress_distinguishes_preserve_skip_and_executable(tmp_path: Path):
    machine = _machine(
        [
            (
                "SRC",
                "A",
                [
                    ("S00_PRESERVE", "DONE__PRESERVE"),
                    ("S01_SKIP", "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW"),
                    ("S02_RUN", "READY__RUN_LOCALLY"),
                ],
            )
        ],
        first_unfinished="SRC/A/S00_PRESERVE",
    )
    ledger = d.StageLedger(tmp_path / "work", machine, tmp_path)
    stream = io.StringIO()
    reporter = d.ProgressReporter(machine, ledger, stream=stream, clock=lambda: 100)
    reporter.emit_stage(machine.get("SRC/A/S00_PRESERVE"), "PRESERVE", next_stage="SRC/A/S01_SKIP", elapsed_stage_ns=1, terminal_disposition="PRESERVED")
    reporter.emit_stage(machine.get("SRC/A/S01_SKIP"), "SKIP", next_stage="SRC/A/S02_RUN", elapsed_stage_ns=2, terminal_disposition="SKIPPED_BY_FROZEN_LAW")
    reporter.emit_stage(machine.get("SRC/A/S02_RUN"), "START", next_stage=None, elapsed_stage_ns=None)
    reporter.emit_stage(machine.get("SRC/A/S02_RUN"), "PASS", next_stage=machine.final_stage_id, elapsed_stage_ns=3, terminal_disposition="PASS")

    events = [json.loads(line) for line in reporter.path.read_text(encoding="utf-8").splitlines()]
    assert [event["state"] for event in events] == ["PRESERVE", "SKIP", "START", "PASS"]
    assert events[0]["executable"]["index"] is None
    assert events[1]["executable"]["index"] is None
    assert events[2]["executable"]["index"] == 1
    assert "PRESERVE" in stream.getvalue()
    assert "SKIP" in stream.getvalue()


def test_progress_emission_does_not_mutate_ledger_semantic_state(tmp_path: Path):
    machine = _machine(
        [("SRC", "A", [("S00_RUN", "READY__RUN_LOCALLY")])],
        first_unfinished="SRC/A/S00_RUN",
    )
    ledger = d.StageLedger(tmp_path / "work", machine, tmp_path)
    before_data = json.dumps(ledger.data, sort_keys=True)
    before_hash = ledger.hash()
    reporter = d.ProgressReporter(machine, ledger, stream=io.StringIO(), clock=lambda: 1)
    reporter.emit_stage(machine.get("SRC/A/S00_RUN"), "START", next_stage=None, elapsed_stage_ns=None)
    assert json.dumps(ledger.data, sort_keys=True) == before_data
    assert ledger.hash() == before_hash


def test_final_s17_progress_and_exact_court_terminal_are_emitted(tmp_path: Path):
    machine = _machine(
        [("SRC", "A", [("S00_RUN", "READY__RUN_LOCALLY")])],
        first_unfinished="SRC/A/S00_RUN",
    )
    ledger = d.StageLedger(tmp_path / "work", machine, tmp_path)
    stream = io.StringIO()
    reporter = d.ProgressReporter(machine, ledger, stream=stream, clock=lambda: 1)
    final = machine.get(machine.final_stage_id)
    reporter.emit_stage(final, "START", next_stage=None, elapsed_stage_ns=None)
    reporter.emit_stage(final, "PASS", next_stage="__COURT_COMPLETE__", elapsed_stage_ns=4, terminal_disposition="PASS")
    reporter.emit_court_terminal(
        status="COURT_SEQUENCE_COMPLETE__S17_VERIFIED",
        next_stage="__COURT_COMPLETE__",
        ledger_sha256=ledger.hash(),
    )
    events = [json.loads(line) for line in reporter.path.read_text(encoding="utf-8").splitlines()]
    assert [(e["event_type"], e["state"]) for e in events] == [
        ("STAGE", "START"),
        ("STAGE", "PASS"),
        ("COURT_TERMINAL", "PASS"),
    ]
    assert events[-1]["terminal"] == "COURT_SEQUENCE_COMPLETE__S17_VERIFIED"
    assert "COURT STAGE S17_FINAL_COMPLETENESS_AND_VERIFICATION" in stream.getvalue()
    assert "COURT TERMINAL COURT_SEQUENCE_COMPLETE__S17_VERIFIED" in stream.getvalue()


def test_human_progress_stays_on_stderr_so_stdout_json_remains_parseable(tmp_path: Path, capsys):
    machine = _machine(
        [("SRC", "A", [("S00_RUN", "READY__RUN_LOCALLY")])],
        first_unfinished="SRC/A/S00_RUN",
    )
    ledger = d.StageLedger(tmp_path / "work", machine, tmp_path)
    reporter = d.ProgressReporter(machine, ledger, clock=lambda: 1)
    reporter.emit_stage(machine.get("SRC/A/S00_RUN"), "START", next_stage=None, elapsed_stage_ns=None)
    print(json.dumps({"machine_result": "PASS"}))
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {"machine_result": "PASS"}
    assert "FIABC P2" in captured.err


def test_wvs7_c_failure_receipt_serializes_with_manifest_sequence_index(tmp_path: Path, monkeypatch):
    machine = _six_cell_machine()
    monkeypatch.setattr(d, "load_current_execution_manifest", lambda _path: machine)
    manifest_path = tmp_path / "current_manifest.json"
    manifest_path.write_text("{}\n", encoding="utf-8")
    monkeypatch.setenv("RAWLSING_FIABC_T5_CURRENT_EXECUTION_MANIFEST", str(manifest_path))

    repo = tmp_path / "repo"
    expectations = repo / "WORKER_RETURNS/EE-P2X/09_LOCAL_COURT_FROZEN_EXPECTATIONS.json"
    expectations.parent.mkdir(parents=True, exist_ok=True)
    expectations.write_text(
        json.dumps(
            {
                "hq": {"handoff_commit": "hq"},
                "lock1": {"manifest_json_git_blob_sha1": "lock1"},
                "lock2": {
                    "hash": "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
                },
                "candidates": {"C": {"owner_blob": "owner-c"}},
                "execution_seam": {"git_blob_sha1": "seam"},
            }
        ),
        encoding="utf-8",
    )
    runtime = repo / backend.R6S_RUNTIME_PACKAGE
    runtime.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_text(
        json.dumps(
            {
                "lock2": backend.WVS_LOCK2,
                "replay": backend.WVS_LOCK2_REPLAY,
                "discovery_authority_hash": backend.WVS_DISCOVERY_AUTHORITY,
            }
        ),
        encoding="utf-8",
    )

    roots = SimpleNamespace(durable=tmp_path / "durable")
    roots.durable.mkdir(parents=True)
    stage = machine.get("WVS7/C/S01_BUILD")
    ctx = SimpleNamespace(
        stage=stage,
        roots=roots,
        source_sha256="c" * 64,
        input_identity_hash="d" * 64,
    )
    services = SimpleNamespace(repo_root=repo)
    state = backend._new_state(ctx)
    result = backend._failure(ctx, services, state, backend.BackendStop("typed failure"))

    assert result["terminal_disposition"] == "CANDIDATE_LOCAL_FAILURE"
    cell_receipt = Path(result["output_artifacts"]["cell_receipt"])
    cell = json.loads(cell_receipt.read_text(encoding="utf-8"))
    assert cell["source"] == "WVS7"
    assert cell["candidate"] == "C"
    assert cell["sequence_index"] == 5
    assert cell["authority"]["lock2_hash"] == backend.WVS_LOCK2
    assert cell["authority"]["lock2_replay_hash"] == backend.WVS_LOCK2_REPLAY
    assert cell["authority"]["discovery_authority"] == backend.WVS_DISCOVERY_AUTHORITY
    assert cell["authority"]["lock2_hash"] != "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
    assert cell["authority"]["discovery_authority"] != "24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab"
    assert len(backend._current_manifest_cell_order()) == 6


def test_lits_failure_metadata_keeps_lock1_owner_and_seam_but_not_predecessor_lock2(tmp_path: Path, monkeypatch):
    machine = _six_cell_machine()
    monkeypatch.setattr(d, "load_current_execution_manifest", lambda _path: machine)
    manifest_path = tmp_path / "current_manifest.json"
    manifest_path.write_text("{}\n", encoding="utf-8")
    monkeypatch.setenv("RAWLSING_FIABC_T5_CURRENT_EXECUTION_MANIFEST", str(manifest_path))

    repo = tmp_path / "repo"
    expectations = repo / "WORKER_RETURNS/EE-P2X/09_LOCAL_COURT_FROZEN_EXPECTATIONS.json"
    expectations.parent.mkdir(parents=True, exist_ok=True)
    expectations.write_text(
        json.dumps(
            {
                "hq": {"handoff_commit": "hq"},
                "lock1": {"manifest_json_git_blob_sha1": "lock1"},
                "lock2": {
                    "hash": "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
                },
                "candidates": {"A": {"owner_blob": "owner-a"}},
                "execution_seam": {"git_blob_sha1": "seam"},
            }
        ),
        encoding="utf-8",
    )
    runtime = repo / backend.R6S_RUNTIME_PACKAGE
    runtime.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_text(
        json.dumps(
            {
                "lock2": backend.WVS_LOCK2,
                "replay": backend.WVS_LOCK2_REPLAY,
                "discovery_authority_hash": backend.WVS_DISCOVERY_AUTHORITY,
            }
        ),
        encoding="utf-8",
    )

    roots = SimpleNamespace(durable=tmp_path / "durable")
    roots.durable.mkdir(parents=True)
    stage = machine.get("LITS_I/A/S01_BUILD")
    ctx = SimpleNamespace(
        stage=stage,
        roots=roots,
        source_sha256="c" * 64,
        input_identity_hash="d" * 64,
    )
    services = SimpleNamespace(repo_root=repo)
    state = backend._new_state(ctx)
    result = backend._failure(ctx, services, state, backend.BackendStop("typed failure"))
    cell = json.loads(Path(result["output_artifacts"]["cell_receipt"]).read_text(encoding="utf-8"))

    assert cell["sequence_index"] == 0
    assert cell["authority"] == {
        "hq_handoff_commit": "hq",
        "lock1_manifest_blob": "lock1",
        "lock2_hash": backend.WVS_LOCK2,
        "lock2_replay_hash": backend.WVS_LOCK2_REPLAY,
    }
    assert cell["bindings"]["candidate_owner_blob"] == "owner-a"
    assert cell["bindings"]["execution_seam_blob"] == "seam"


def test_preentry_prefix_does_not_synthesize_current_ready_stage(tmp_path: Path, monkeypatch):
    machine = _machine(
        [
            (
                "LITS_I",
                "A",
                [
                    ("S00_PREFLIGHT", "DONE__PRESERVE"),
                    ("S01_BUILD", "READY__RUN_LOCALLY"),
                ],
            )
        ],
        first_unfinished="LITS_I/A/S01_BUILD",
    )
    machine.document["sources"]["LITS_I"]["sha256"] = "e" * 64
    calls = []
    monkeypatch.setattr(
        d,
        "_preserve",
        lambda machine, ledger, stage, repo, head, source_sha: calls.append(stage.address)
        or (stage.next_stage_on_pass, "receipt"),
    )
    driver = d.DarwinCourtDriver(
        machine=machine,
        work_root=tmp_path / "work",
        repo_root=tmp_path,
        source_paths={},
        host=SimpleNamespace(),
        repo=SimpleNamespace(head="f" * 40),
        backend=None,
    )
    driver.bind_initial_manifest_prefix()
    assert calls == ["LITS_I/A/S00_PREFLIGHT"]
    assert "LITS_I/A/S01_BUILD" not in calls


def test_sealed_current_manifest_reports_derived_102_89_6_17_shape():
    root = Path(__file__).resolve().parents[2]
    manifest = root / "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json"
    machine = d.load_current_execution_manifest(manifest)
    plan = d.ManifestProgressPlan(machine)

    assert plan.overall_total == 102
    assert plan.executable_total == 89
    assert plan.cell_total == 6
    first = plan.position(machine.first_unfinished)
    assert first.overall_index == 1
    assert (first.cell_index, first.cell_total) == (1, 6)
    assert (first.stage_index, first.stage_total) == (2, 17)
    wvs_c = plan.position("WVS7/C/S16_TERMINAL_METRIC_VECTOR_COMPLETENESS")
    assert (wvs_c.cell_index, wvs_c.cell_total) == (6, 6)
    assert (wvs_c.stage_index, wvs_c.stage_total) == (17, 17)


def test_current_six_cell_candidate_failure_stops_before_success_only_s17():
    machine = _six_cell_machine()
    entries = {}
    for cell in machine.document["cells"]:
        for sid in machine.document["stage_catalog"]:
            address = f"{cell['source']}/{cell['candidate']}/{sid}"
            entries[address] = {
                "state": "TERMINAL",
                "verifier_completion": True,
                "terminal_disposition": "PASS",
            }
    entries["WVS7/C/S01_BUILD"]["terminal_disposition"] = "CANDIDATE_LOCAL_FAILURE"

    class Ledger:
        def stage_entry(self, address):
            return entries.get(address)

        def revalidate_terminal(self, address):
            return entries[address]

    try:
        d._final_ready(machine, Ledger())
    except d.CandidateLocalFailure as exc:
        assert exc.receipt["candidate_failure_cells"] == ["WVS7/C"]
    else:
        raise AssertionError("success-only S17 gate admitted a candidate-local failure")
