from dataclasses import FrozenInstanceError
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import pytest

from actor_reader import ReaderHeld, load_candidate, read_actor_snapshot, read_surface, gate_second_half

SOURCE = Path(os.environ.get("C9_READER_SOURCE", "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/syn02-c9-r3-isolated-r2/SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL"))


@pytest.fixture
def actor(tmp_path):
    candidate = load_candidate(SOURCE)
    obj = candidate.ActorAuthority(tmp_path / "actor.sqlite", actor_id="A")
    yield candidate, obj
    obj.conn.close()


def publish(candidate, obj, key, *, text="I received help", memory="ACTOR_ACCESSIBLE", held=False, surface=None):
    obj.add_world_receipt(world_receipt_hash="world-" + key, world_event_id="event-" + key,
                          c8_branch_id="c8", c8_root_hash="root", c8_head_hash="head", effective_us=10)
    common = dict(event_key=key, idempotency_key=key, source_cut_hash=obj.source_cut_hash,
                  source_scope_hash="scope", settled_scope_hash="settled", world_receipt_hash="world-" + key,
                  memory_evidence=memory)
    if held:
        request = candidate.PublishRequest(**common, decision_kind="HELD_MISSING_RULE", actor_presence="NOT_PRESENT", actor_reception="NOT_WITNESSED")
    else:
        obj.add_rule(rule_hash="T-" + key, rule_kind="T", issuer_ref="TEST_ONLY", source_cut_hash=obj.source_cut_hash)
        request = candidate.PublishRequest(**common, decision_kind="COMMITTED_CHANGE", rule_t_hash="T-" + key,
            rule_t_status="COMMITTED_CHANGE", evaluation_basis="ISSUED_RULE_T_EVALUATED", evaluated_readset_hash="readset",
            semantic_payload={"actor_surface": surface if surface is not None else {"text": text}})
    return obj.publish(request)


def read(obj, **overrides):
    arguments = dict(actor_id=obj.actor_id, branch_id=obj.branch_id, branch_epoch=obj.branch_epoch, source_cut=obj.source_cut_hash)
    arguments.update(overrides)
    return read_actor_snapshot(SOURCE, obj.path, **arguments)


def logical_dump(obj):
    return "\n".join(obj.conn.iterdump())


def test_verified_multiple_received_events_and_cold_read_are_pure(actor):
    c, a = actor
    publish(c, a, "first", text="I received help")
    publish(c, a, "second", text="I practiced", memory="PARTIAL_TRACE")
    before = logical_dump(a)
    first = read(a)
    second = read(a)
    assert first == second
    assert logical_dump(a) == before
    assert first.delivery_status == "SYNC_HELD"
    assert json.loads(read_surface(first).to_json())["records"] == [
        {"text": "I received help", "epistemic_kind": "received_account"},
        {"text": "I practiced", "epistemic_kind": "partial_trace"}]
    with pytest.raises(FrozenInstanceError):
        first.delivery_status = "CLEAN"


def test_empty_and_objective_unseen_care_have_identical_actor_bytes(actor):
    c, a = actor
    before = read_surface(read(a)).to_json()
    publish(c, a, "hidden-care", held=True, memory="ACTOR_UNKNOWN")
    assert read_surface(read(a)).to_json() == before
    assert "hidden-care" not in before


def test_analyst_only_material_does_not_leak_id_count_gap_or_digest(actor):
    c, a = actor
    publish(c, a, "visible", text="A remembered account")
    before = read_surface(read(a)).to_json()
    for name in ("secret-world-7", "secret-world-8"):
        publish(c, a, name, text="HIDDEN_SECRET", memory="ANALYST_ONLY")
    after = read_surface(read(a)).to_json()
    assert after == before
    assert not any(x in after for x in ("HIDDEN_SECRET", "secret-world", "receipt", "digest", "actor_id", "source_cut"))


def test_belief_is_labelled_belief_not_objective_truth(actor):
    c, a = actor
    publish(c, a, "belief", text="I think help may arrive", memory="BELIEF_WITH_SOURCE")
    assert json.loads(read_surface(read(a)).to_json())["records"][0]["epistemic_kind"] == "sourced_belief"


def test_tampered_head_reader_refuses_existing_reproducer(actor):
    _, a = actor
    a.conn.execute("UPDATE actor_head SET head_semantic_hash='tampered'")
    before = logical_dump(a)
    with pytest.raises(ReaderHeld, match="ACTOR_INTEGRITY_HELD"):
        read(a)
    assert logical_dump(a) == before


@pytest.mark.parametrize("field,value", [("actor_id", "B"), ("branch_epoch", "other"), ("source_cut", "other")])
def test_scope_mismatch_refuses_without_writes(actor, field, value):
    _, a = actor
    before = logical_dump(a)
    with pytest.raises(ReaderHeld):
        read(a, **{field: value})
    assert logical_dump(a) == before


def test_unknown_surface_keys_are_refused_not_passed_through(actor):
    c, a = actor
    publish(c, a, "bad", surface={"text": "visible", "narrator": "hidden"})
    with pytest.raises(ReaderHeld, match="ACTOR_SURFACE_ALLOWLIST_HELD"):
        read(a)


def test_sci05_missing_explicit_dependencies_does_not_prove_independence():
    proposals = ({"proposal": "a"}, {"proposal": "b"}, {"proposal": "c"})
    assert gate_second_half("DENIED", proposals) == ("HELD_SCI05_FIRST_HALF",) * 3
    assert gate_second_half("HELD", proposals) == ("HELD_SCI05_FIRST_HALF",) * 3
    assert gate_second_half("ADMITTED", proposals) == ("PROPOSED_ONLY",) * 3
    with pytest.raises(ReaderHeld):
        gate_second_half("ADMITTED", proposals[:2])


def test_original_source_hash_mismatch_refuses_before_import(tmp_path):
    (tmp_path / "c9_actor_r3.py").write_text("raise RuntimeError('MUST_NOT_EXECUTE')")
    with pytest.raises(ReaderHeld, match="SOURCE_CHANGED_BEFORE_IMPORT"):
        load_candidate(tmp_path)


def test_missing_database_is_not_created(tmp_path):
    database = tmp_path / "absent.sqlite"
    with pytest.raises(sqlite3.OperationalError):
        read_actor_snapshot(SOURCE, database, actor_id="A", branch_id="b0", branch_epoch="e0", source_cut="x")
    assert not database.exists()


def test_verification_and_projection_share_snapshot_during_concurrent_commit(actor, monkeypatch):
    import actor_reader
    candidate, a = actor
    original = candidate.ActorAuthority.verify
    def verify_then_external_commit(obj):
        result = original(obj)
        a.conn.execute("UPDATE actor_head SET head_semantic_hash='concurrent-tamper'")
        a.conn.commit()
        return result
    monkeypatch.setattr(candidate.ActorAuthority, "verify", verify_then_external_commit)
    with monkeypatch.context() as local:
        local.setattr(actor_reader, "load_candidate", lambda source: candidate)
        snapshot = read(a)
        assert snapshot.semantic_hash != "concurrent-tamper"
    with pytest.raises(ReaderHeld, match="ACTOR_INTEGRITY_HELD"):
        read(a)


def test_cli_consumes_the_real_candidate_fixture_and_emits_only_surface(actor):
    import subprocess
    import sys
    candidate, a = actor
    publish(candidate, a, "cli-visible", text="Remembered help")
    command = [sys.executable, "-B", str(Path(__file__).with_name("actor_reader.py")),
               "--source", str(SOURCE), "--database", str(a.path), "--actor", "A",
               "--branch", "b0", "--epoch", "e0", "--source-cut", a.source_cut_hash]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"schema": "ActorVisibleSurfaceV1", "records": [
        {"text": "Remembered help", "epistemic_kind": "received_account"}]}
    assert "cli-visible" not in result.stdout
    assert "source_cut" not in result.stdout


def test_pure_view_is_consumed_by_surface_and_preserves_full_snapshot(actor):
    from dataclasses import asdict
    from copy import deepcopy
    from actor_reader import compute_view, DerivedViewRequestV1
    c, a = actor
    publish(c, a, "view", text="A received account")
    snapshot = read(a)
    before = deepcopy(asdict(snapshot))
    result = compute_view(snapshot, DerivedViewRequestV1("ACTOR_RECEIVED_SURFACE_TESTONLY@1", "A", a.source_cut_hash))
    assert result.status == "OK" and result.source_version_ref == snapshot.version_hash
    assert result.source_fact_ids == ()  # No invented owner-frozen fact identifiers.
    assert result.value.records == read_surface(snapshot).records
    assert asdict(snapshot) == before


@pytest.mark.parametrize("view_id,actor_id,cut,reason", [
    ("unknown", "A", "TEST_ONLY_SOURCE_CUT", "UNKNOWN_VIEW"),
    ("ACTOR_RECEIVED_SURFACE_TESTONLY@1", "B", "TEST_ONLY_SOURCE_CUT", "ACTOR_SCOPE_MISMATCH"),
    ("ACTOR_RECEIVED_SURFACE_TESTONLY@1", "A", "other", "SOURCE_CUT_MISMATCH")])
def test_pure_view_refuses_unknown_view_or_source_without_best_effort(actor, view_id, actor_id, cut, reason):
    from actor_reader import compute_view, DerivedViewRequestV1
    _, a = actor
    result = compute_view(read(a), DerivedViewRequestV1(view_id, actor_id, cut))
    assert result.status == "HELD" and result.value is None and result.warnings == (reason,)


def test_unknown_observation_is_not_zero_or_hopeful_or_valid_empty(actor):
    from dataclasses import replace
    from actor_reader import compute_view, DerivedViewRequestV1
    _, a = actor
    unknown = replace(read(a), visible_records=None)
    result = compute_view(unknown, DerivedViewRequestV1("ACTOR_RECEIVED_SURFACE_TESTONLY@1", "A", a.source_cut_hash))
    assert result.status == "UNKNOWN" and result.value is None
    with pytest.raises(ReaderHeld, match="DERIVED_VIEW_UNKNOWN"):
        read_surface(unknown)


def test_full_snapshot_guard_detects_hidden_write_and_preserves_original(actor, monkeypatch):
    from dataclasses import asdict
    import actor_reader
    _, a = actor
    snapshot = read(a)
    before = asdict(snapshot)
    def old_mutating_view(work):
        object.__setattr__(work, "state_json", '{"registers":{"hidden_write":1},"metabolic_style":"changed"}')
        return actor_reader.SurfacePacketV1(())
    monkeypatch.setattr(actor_reader, "build_surface_packet", old_mutating_view)
    with pytest.raises(ReaderHeld, match="DERIVED_VIEW_MUTATION:state_json"):
        actor_reader.compute_view(snapshot, actor_reader.DerivedViewRequestV1("ACTOR_RECEIVED_SURFACE_TESTONLY@1", "A", a.source_cut_hash))
    assert asdict(snapshot) == before
