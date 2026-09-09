from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from rawlsing_next.as4 import loader
from rawlsing_next.as4.bounded_fixture import build_bounded_source
from rawlsing_next.as4.protocol import prepare, result_identity_receipt
from rawlsing_next.as4.run_candidate import run_candidate
from rawlsing_next.as4.run_all import run_all


def _semantic(candidate: str, tmp_path: Path):
    manifest = loader.load_hb04_manifest()
    source = build_bounded_source(candidate, tmp_path / f"source-{candidate}")
    session = prepare(
        candidate,
        source,
        manifest,
        tmp_path / f"session-{candidate}",
        allow_bounded_fixture=True,
    )
    try:
        i03 = session.run_i03()
        i05 = session.run_i05()
        identity = result_identity_receipt(candidate, i03, i05)
        measurements = session.measurements
    finally:
        cleanup = session.close()
    assert cleanup["status"] == "PASS_CLOSED_AND_SCRATCH_REMOVED"
    assert cleanup["persistent_transformed_payload_file_count"] == 0
    assert measurements["semantic_identity_effect"] == "NONE_DESCRIPTIVE_ONLY"
    return identity


def test_hb04_exact_loader_reconstructs_current_successor_package_without_remints():
    manifest = loader.load_hb04_manifest()
    assert manifest.intake_sha256 == loader.FREEZE_SHA256
    assert len(manifest.role_predicates) == 19
    assert len(manifest.distinct_predicates) == 18
    assert len(manifest.query_templates) == 3
    assert manifest.role_predicates["A000"] is manifest.role_predicates["A1RAPP"]
    aliases = {}
    for role, obj in manifest.role_predicates.items():
        aliases.setdefault(obj.content_hash, []).append(role)
    assert sorted(tuple(sorted(v)) for v in aliases.values() if len(v) > 1) == [
        ("A000", "A1RAPP")
    ]
    assert manifest.discovery_authority.content_hash == loader.DISCOVERY_AUTHORITY_HASH
    assert manifest.official_frontier_ref.content_hash == loader.OFFICIAL_FRONTIER_HASH
    assert manifest.replay_closure_ref.content_hash == loader.REPLAY_CLOSURE_HASH
    assert manifest.runtime_binding_ref.content_hash == loader.RUNTIME_BINDING_HASH
    assert manifest.zero_remints is True
    assert manifest.successor_identity_receipt["zero_remints"] is True


def test_hb04_bounded_common_session_semantic_identity_parity_across_a_b_c(tmp_path):
    identities = {candidate: _semantic(candidate, tmp_path) for candidate in ("A", "B", "C")}
    projections = {
        candidate: {
            "i03_fact_refs": value["i03_fact_refs"],
            "i05_evaluated_frontier_ref": value["i05_evaluated_frontier_ref"],
            "i05_receipt_refs": value["i05_receipt_refs"],
            "candidate_count": value["candidate_count"],
            "covered_candidate_count": value["covered_candidate_count"],
        }
        for candidate, value in identities.items()
    }
    assert projections["A"] == projections["B"] == projections["C"]
    assert all(value["ranking_fields_present"] is False for value in identities.values())
    assert all(value["selection_fields_present"] is False for value in identities.values())


@pytest.mark.parametrize("candidate", ["A", "B", "C"])
def test_run_candidate_emits_closed_machine_receipt(candidate, tmp_path):
    receipt = run_candidate(
        candidate=candidate,
        workdir=tmp_path / candidate,
        bounded_fixture=True,
    )
    assert receipt["status"] == "PASS"
    assert receipt["candidate"] == candidate
    assert receipt["session_closed"] is True
    assert receipt["cleanup"]["status"] == "PASS_CLOSED_AND_SCRATCH_REMOVED"
    assert receipt["cleanup"]["result_cache_present"] is False
    assert receipt["ranking_logic_count"] == 0
    assert receipt["selection_logic_count"] == 0
    assert receipt["real_lits1_open_count"] == 0
    assert receipt["real_wvs7_open_count"] == 0
    assert receipt["c09_execution_count"] == 0


def test_run_all_is_exactly_three_fresh_sequential_children_a_b_c(tmp_path):
    receipt = run_all(workdir=tmp_path / "all", bounded_fixture=True)
    assert receipt["status"] == "PASS"
    assert receipt["order"] == ["A", "B", "C"]
    assert receipt["process_count"] == 3
    assert receipt["distinct_process_count"] == 3
    assert receipt["sequential_no_overlap"] is True
    assert len({x["process_id"] for x in receipt["children"]}) == 3
    assert [x["candidate"] for x in receipt["children"]] == ["A", "B", "C"]
    assert all(x["exit_code"] == 0 for x in receipt["children"])
    assert all(x["session_closed"] for x in receipt["children"])
    assert all(x["cleanup"]["status"] == "PASS_CLOSED_AND_SCRATCH_REMOVED" for x in receipt["children"])
    assert receipt["ranking_logic_count"] == 0
    assert receipt["selection_logic_count"] == 0
    assert receipt["comparative_early_stop_count"] == 0
    assert receipt["real_lits1_open_count"] == 0
    assert receipt["real_wvs7_open_count"] == 0
    assert receipt["c09_execution_count"] == 0
    for left, right in zip(receipt["children"], receipt["children"][1:]):
        assert left["finished_monotonic_ns"] <= right["started_monotonic_ns"]


def test_wrong_freeze_sha_fails_closed(tmp_path):
    root = loader.repository_root()
    original = json.loads((root / loader._FREEZE).read_text(encoding="utf-8"))
    original["route_c"]["qualified_intake_identity"] = "0" * 64
    path = tmp_path / "bad-freeze.json"
    path.write_text(json.dumps(original), encoding="utf-8")
    with pytest.raises(loader.HB04FreezeError, match="freeze SHA"):
        loader.load_hb04_manifest(freeze_path=path)


def test_wrong_route_a_implementation_blob_fails_closed(monkeypatch):
    original = loader._git_blob
    def fake(path):
        if path.name == "pre553_r5_source_backed_adapter.py":
            return "0" * 40
        return original(path)
    monkeypatch.setattr(loader, "_git_blob", fake)
    with pytest.raises(loader.HB04FreezeError, match="Route-A implementation"):
        loader.load_hb04_manifest()


def test_wrong_b16_seal_or_driver_pin_fails_closed(monkeypatch):
    original = loader._json
    def fake(path):
        value = original(path)
        if path.name == "14_C05R2B_FINAL_PRODUCTION_SEAL.json":
            value = copy.deepcopy(value)
            value["qualifying_driver_commit"] = "0" * 40
        return value
    monkeypatch.setattr(loader, "_json", fake)
    with pytest.raises(loader.HB04FreezeError, match="B16 qualifying driver"):
        loader.load_hb04_manifest()


@pytest.mark.parametrize(
    "filename,mutator,match",
    [
        (
            "02_SUCCESSOR_RUNTIME_CATALOG_BINDING.json",
            lambda x: x.__setitem__("sole_alias", ["A000", "A2RAPP"]),
            "sole alias",
        ),
        (
            "03_SUCCESSOR_DISCOVERY_AUTHORITY.json",
            lambda x: x.__setitem__("content_hash", "0" * 64),
            "content_hash",
        ),
        (
            "05_SUCCESSOR_CANDIDATE_GRAMMAR.json",
            lambda x: x.__setitem__("candidate_grammar_hash", "0" * 64),
            "candidate grammar",
        ),
        (
            "06_SUCCESSOR_82_CANDIDATE_FRONTIER_MANIFEST.json",
            lambda x: x["official_frontier_ref"].__setitem__("content_hash", "0" * 64),
            "official frontier",
        ),
        (
            "12_SUCCESSOR_DISCOVERY_AUTHORITY_FRONTIER_REPLAY_SEAL.json",
            lambda x: x["successor_preexecution_replay_closure_ref"].__setitem__(
                "content_hash", "0" * 64
            ),
            "replay closure",
        ),
    ],
)
def test_stale_or_predecessor_successor_package_material_fails_closed(
    monkeypatch, filename, mutator, match
):
    original = loader._json
    def fake(path):
        value = original(path)
        if path.name == filename:
            value = copy.deepcopy(value)
            mutator(value)
        return value
    monkeypatch.setattr(loader, "_json", fake)
    with pytest.raises((loader.HB04FreezeError, Exception), match=match):
        loader.load_hb04_manifest()


@pytest.mark.parametrize("carrier_name", ["CANONICAL_PREDICATE_MANIFEST.json", "03_CANONICAL_QUERY_REPRESENTATIONS.json"])
def test_missing_runtime_object_carrier_fails_closed(monkeypatch, carrier_name):
    original = loader._json
    def fake(path):
        if path.name == carrier_name:
            raise loader.HB04FreezeError("missing exact runtime object carrier")
        return original(path)
    monkeypatch.setattr(loader, "_json", fake)
    with pytest.raises(loader.HB04FreezeError, match="missing exact runtime object carrier"):
        loader.load_hb04_manifest()


def test_alias_cardinality_violation_fails_closed(monkeypatch):
    original = loader._json
    def fake(path):
        value = original(path)
        if path.name == "02_SUCCESSOR_RUNTIME_CATALOG_BINDING.json":
            value = copy.deepcopy(value)
            value["predicate_role_mapping_count"] = 18
        return value
    monkeypatch.setattr(loader, "_json", fake)
    with pytest.raises(loader.HB04FreezeError, match="predicate role count"):
        loader.load_hb04_manifest()


@pytest.mark.parametrize("candidate", ["", "D", "a", "ABC"])
def test_non_abc_candidate_fails_closed(candidate, tmp_path):
    manifest = loader.load_hb04_manifest()
    source = build_bounded_source("A", tmp_path / "source")
    with pytest.raises(loader.HB04FreezeError, match="candidate"):
        prepare(candidate, source, manifest, tmp_path / "session", allow_bounded_fixture=True)


def test_source_sha_mismatch_fails_before_semantic_execution(tmp_path):
    with pytest.raises(loader.HB04FreezeError, match="source SHA mismatch"):
        run_candidate(
            candidate="B",
            workdir=tmp_path / "bad-source",
            bounded_fixture=True,
            expected_source_sha256="0" * 64,
        )


@pytest.mark.parametrize(
    "directive",
    [
        {"ranking": "fastest"},
        {"selection": "best"},
        {"score": "latency"},
        {"recommend": "winner"},
        {"stop_early": True},
        {"extra_accelerator": "CACC3"},
        {"cacc3": True},
    ],
)
def test_ranking_selection_and_extra_accelerator_directives_fail_closed(directive):
    with pytest.raises(loader.HB04FreezeError, match="forbids"):
        loader.reject_ungoverned_directive(directive)
