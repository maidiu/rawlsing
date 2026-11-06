"""Mechanical tests for the pure P3 compression-evidence sidecar.

These are compact nonrespondent document fixtures. They exercise the frozen
metadata API only: no P2 batch is re-run and no psychological/world/state writer
is present.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT.parent / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for path in (ROOT, ENGINE_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from developmental_recursion.contracts import digest  # noqa: E402
from p3.compression import (  # noqa: E402
    CompressionRefusal,
    bind,
    preflight,
)

FORMS = (
    "SINGULAR_OCCURRENCE",
    "REPRESENTATIVE_EPISODE",
    "ACCUMULATED_INTERVAL",
    "RETROSPECTIVE_CRYSTALLIZATION",
)


def fixture_identity() -> dict:
    return {
        "root": "root:fixture",
        "actor": "actor:fixture",
        "branch": "branch:fixture",
        "clock": 90,
        "state_hash": digest({"fixture": "before"}),
    }


def fixture_proposal(interval: dict | None = None) -> dict:
    return {
        "event_id": "proposal:fixture:1",
        "event_time": 100,
        "operation": "ADMIT_EVENT",
        "source_refs": ["P2_INPUT:" + digest({"fixture": "source"})],
        "participants": ["actor:fixture"],
        "circumstances": {"language_context": None},
        "interval": interval,
    }


def source_doc(ref: str, kind: str, from_clock: int, to_clock: int,
               identity: dict | None = None) -> dict:
    identity = identity or fixture_identity()
    body = {
        "grade": "SOURCEFREE_TEST_ONLY",
        "root": identity["root"],
        "actor": identity["actor"],
        "branch": identity["branch"],
        "kind": kind,
        "from_clock": from_clock,
        "to_clock": to_clock,
        "data": {"source_ref": ref, "fixture": kind},
    }
    body["hash"] = digest(body)
    return body


def fixture_catalog(identity: dict | None = None) -> dict:
    identity = identity or fixture_identity()
    return {
        "source:participation": source_doc(
            "source:participation", "ACTOR_PARTICIPATION", 0, 90, identity),
        "source:material": source_doc(
            "source:material", "MATERIAL_RELATION", 0, 90, identity),
        "source:recurrence": source_doc(
            "source:recurrence", "RECURRING_RELATION", 0, 90, identity),
        "source:bounded": source_doc(
            "source:bounded", "BOUNDED_INTERVAL", 20, 60, identity),
        "source:historical": source_doc(
            "source:historical", "HISTORICAL_SOURCE", 10, 50, identity),
    }


def fixture_spec(form: str, proposal: dict) -> dict:
    windows = {
        "SINGULAR_OCCURRENCE": {"from_clock": 90, "to_clock": 100,
                                 "coverage_basis": "actual-event"},
        "REPRESENTATIVE_EPISODE": {"from_clock": 0, "to_clock": 90,
                                     "coverage_basis": "recurring-relation"},
        "ACCUMULATED_INTERVAL": {"from_clock": 20, "to_clock": 60,
                                   "coverage_basis": "bounded-interval"},
        "RETROSPECTIVE_CRYSTALLIZATION": {"from_clock": 10, "to_clock": 50,
                                            "coverage_basis": "fixed-history"},
    }
    recurrence = {
        "SINGULAR_OCCURRENCE": [],
        "REPRESENTATIVE_EPISODE": ["source:recurrence"],
        "ACCUMULATED_INTERVAL": ["source:bounded"],
        "RETROSPECTIVE_CRYSTALLIZATION": ["source:historical"],
    }[form]
    return {
        "envelope_id": "envelope:fixture:1",
        "proposal_hash": digest(proposal),
        "representation_form": form,
        "represented_window": windows[form],
        "recurrence_basis_refs": recurrence,
        "participation_refs": ["source:participation"],
        "material_relation_refs": ["source:material"],
        "observed": ["scope:actor-observed"],
        "unobserved": ["scope:actor-unobserved"],
        "selection_basis": "fixture selection rationale",
    }


def fixture_interval() -> dict:
    return {
        "status": "REALIZED",
        "receipt_hash": digest({"fixture": "interval"}),
        "segments": [{"status": "REALIZED"}],
        "material_after_interval": 0,
    }


def fixture_realized(proposal: dict, identity: dict, *,
                     accessible: dict | None = None,
                     interval: dict | None = None,
                     status: str = "REALIZED",
                     event_actor: str | None = None,
                     event_branch: str | None = None,
                     event_hash: str | None = None,
                     proposal_hash: str | None = None,
                     before: dict | None = None,
                     after_clock: int | None = None,
                     event: dict | None = None) -> dict:
    actor = event_actor or identity["actor"]
    branch = event_branch or identity["branch"]
    actual_hash = event_hash or digest({"fixture": "actual-event"})
    actual_event = event or {
        "e1_event_id": "TEST_ONLY_P2_EVENT_1",
        "e1_event_hash": actual_hash,
        "actor_id": actor,
        "branch_id": branch,
        "event_time": proposal["event_time"],
    }
    after = copy.deepcopy(identity)
    after["clock"] = identity["clock"] + 10 if after_clock is None else after_clock
    after["state_hash"] = digest({"fixture": "after"})
    if accessible is None:
        accessible = {
            "schema": "SOROK_ACTOR_EXPERIENCE@1",
            "grade": "TEST_ONLY_S47_OWNER_NOT_NATIVE_DEVELOPMENTAL_SCIENCE",
            "actor_ref": identity["actor"],
            "status": "OBSERVED",
            "events": [{
                "event_id": actual_event["e1_event_id"],
                "clock": proposal["event_time"],
                "summary": "compact fixture projection",
                "perception": {"clock": proposal["event_time"], "channel": "co_present"},
            }],
            "memory_formation": "MISSING_RULE",
        }
    return {
        "operation_id": "operation:fixture:1",
        "proposal_hash": proposal_hash or digest(proposal),
        "before": copy.deepcopy(before or identity),
        "after": after,
        "status": status,
        "objective": {"event": actual_event, "interval": interval},
        "accessible": accessible,
        "consequences": {"interval": interval},
        "readset": [proposal["source_refs"][0], actual_hash],
        "receipt_ref": "P2_EVENT:" + actual_hash,
    }


def docs(form: str = "SINGULAR_OCCURRENCE"):
    identity = fixture_identity()
    interval = fixture_interval() if form == "ACCUMULATED_INTERVAL" else None
    proposal = fixture_proposal({"mode": "ACTUAL", "span": 4} if interval else None)
    catalog = fixture_catalog(identity)
    spec = fixture_spec(form, proposal)
    realized = fixture_realized(proposal, identity, interval=interval)
    return identity, proposal, catalog, spec, realized


# ---------------------------------------------------------------------------
# All four declared forms.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("form", FORMS)
def test_preflight_and_bind_all_four_forms(form: str) -> None:
    identity, proposal, catalog, spec, realized = docs(form)
    before_spec = copy.deepcopy(spec)
    before_catalog = copy.deepcopy(catalog)
    validated = preflight(spec, identity=identity, proposal=proposal, catalog=catalog)
    assert validated == before_spec
    assert spec == before_spec
    assert catalog == before_catalog

    envelope = bind(spec, identity=identity, proposal=proposal,
                    catalog=catalog, realized=realized)
    assert envelope["status"] == "BOUND"
    assert envelope["representation_form"] == form
    assert envelope["identity"] == identity
    assert envelope["actual_event_ref"] == "TEST_ONLY_P2_EVENT_1"
    assert envelope["actual_event_hash"] == realized["objective"]["event"]["e1_event_hash"]
    assert envelope["actor_access"] == "OBSERVED"
    assert envelope["perception_refs"]
    assert envelope["source_ref_hashes"]["source:participation"] == catalog["source:participation"]["hash"]
    assert envelope["source_ref_hashes"]["source:material"] == catalog["source:material"]["hash"]
    assert envelope["observed"] == ["scope:actor-observed"]
    assert envelope["unobserved"] == ["scope:actor-unobserved"]
    assert envelope["no_psychological_effects"] is True
    assert envelope["psychological_effects"] == []
    assert envelope["memory_or_claim_issued"] is False
    assert envelope["adp016_017_authorized"] is False
    assert len(envelope["envelope_hash"]) == 64
    if form == "ACCUMULATED_INTERVAL":
        assert envelope["actual_interval_status"] == "REALIZED"
        assert envelope["actual_interval_ref"] == realized["objective"]["interval"]["receipt_hash"]
    else:
        assert envelope["actual_interval_ref"] is None


def test_bind_is_deterministic_pure_and_does_not_mutate_documents() -> None:
    identity, proposal, catalog, spec, realized = docs("REPRESENTATIVE_EPISODE")
    before = copy.deepcopy((identity, proposal, catalog, spec, realized))
    first = bind(spec, identity=identity, proposal=proposal,
                 catalog=catalog, realized=realized)
    second = bind(spec, identity=identity, proposal=proposal,
                  catalog=catalog, realized=realized)
    assert first == second
    assert (identity, proposal, catalog, spec, realized) == before
    assert first["no_state_mutation"] is True


# ---------------------------------------------------------------------------
# Sourcefree source documents and exact form bases.
# ---------------------------------------------------------------------------


def test_source_hash_grade_identity_and_time_are_exact() -> None:
    identity, proposal, catalog, spec, _realized = docs("REPRESENTATIVE_EPISODE")

    altered = copy.deepcopy(catalog)
    altered["source:recurrence"]["data"]["fixture"] = "tampered"
    with pytest.raises(CompressionRefusal, match="hash"):
        preflight(spec, identity=identity, proposal=proposal, catalog=altered)

    for source_ref, key, value in (
        ("source:recurrence", "grade", "SOURCE_NATIVE"),
        ("source:recurrence", "root", "wrong-root"),
        ("source:recurrence", "actor", "wrong-actor"),
        ("source:recurrence", "branch", "wrong-branch"),
        ("source:recurrence", "from_clock", -1),
        ("source:recurrence", "to_clock", 101),
    ):
        altered = copy.deepcopy(catalog)
        altered[source_ref][key] = value
        with pytest.raises(CompressionRefusal):
            preflight(spec, identity=identity, proposal=proposal, catalog=altered)


def test_form_specific_source_basis_is_required() -> None:
    identity, proposal, catalog, _spec, _realized = docs("SINGULAR_OCCURRENCE")
    for form in FORMS:
        spec = fixture_spec(form, proposal)
        if form != "SINGULAR_OCCURRENCE":
            spec["recurrence_basis_refs"] = []
            with pytest.raises(CompressionRefusal):
                preflight(spec, identity=identity, proposal=proposal, catalog=catalog)
        spec["participation_refs"] = []
        with pytest.raises(CompressionRefusal):
            preflight(spec, identity=identity, proposal=proposal, catalog=catalog)


def test_form_specific_source_kind_and_window_are_required() -> None:
    identity = fixture_identity()
    proposal = fixture_proposal()
    base = fixture_catalog(identity)
    cases = {
        "REPRESENTATIVE_EPISODE": ("source:recurrence", "MATERIAL_RELATION", 0, 90),
        "ACCUMULATED_INTERVAL": ("source:bounded", "RECURRING_RELATION", 20, 60),
        "RETROSPECTIVE_CRYSTALLIZATION": ("source:historical", "BOUNDED_INTERVAL", 10, 50),
    }
    for form, (ref, kind, frm, to) in cases.items():
        catalog = copy.deepcopy(base)
        catalog[ref] = source_doc(ref, kind, frm, to, identity)
        spec = fixture_spec(form, proposal)
        with pytest.raises(CompressionRefusal):
            preflight(spec, identity=identity, proposal=proposal, catalog=catalog)

    catalog = copy.deepcopy(base)
    catalog["source:bounded"] = source_doc("source:bounded", "BOUNDED_INTERVAL", 21, 60, identity)
    spec = fixture_spec("ACCUMULATED_INTERVAL", proposal)
    with pytest.raises(CompressionRefusal, match="exactly bind"):
        preflight(spec, identity=identity, proposal=proposal, catalog=catalog)


# ---------------------------------------------------------------------------
# Unsupported fields, global multipliers and fabricated inflation.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_key,bad_value", [
    ("global_multiplier", 100),
    ("witness_count", 30),
    ("fabricated_event_ids", ["invented"]),
    ("automatic_effect", {"kind": "PRACTICE"}),
])
def test_unsupported_fields_are_rejected(bad_key: str, bad_value: object) -> None:
    identity, proposal, catalog, spec, _realized = docs("SINGULAR_OCCURRENCE")
    spec = copy.deepcopy(spec)
    spec[bad_key] = bad_value
    with pytest.raises(CompressionRefusal):
        preflight(spec, identity=identity, proposal=proposal, catalog=catalog)


def test_wrong_proposal_context_and_identity_bindings_refuse() -> None:
    identity, proposal, catalog, spec, realized = docs("SINGULAR_OCCURRENCE")
    changed_proposal = copy.deepcopy(proposal)
    changed_proposal["circumstances"]["language_context"] = {"milieu_id": "other"}
    with pytest.raises(CompressionRefusal, match="proposal_hash"):
        preflight(spec, identity=identity, proposal=changed_proposal, catalog=catalog)

    bad_spec = copy.deepcopy(spec)
    bad_spec["proposal_hash"] = digest({"other": "proposal"})
    with pytest.raises(CompressionRefusal, match="proposal_hash"):
        preflight(bad_spec, identity=identity, proposal=proposal, catalog=catalog)

    bad_realized = copy.deepcopy(realized)
    bad_realized["before"]["root"] = "wrong-root"
    with pytest.raises(CompressionRefusal, match="before"):
        bind(spec, identity=identity, proposal=proposal,
             catalog=catalog, realized=bad_realized)


# ---------------------------------------------------------------------------
# Actual P2 event / access / interval custody and HELD behavior.
# ---------------------------------------------------------------------------


def test_missing_or_wrong_actual_event_binding_refuses() -> None:
    identity, proposal, catalog, spec, realized = docs("SINGULAR_OCCURRENCE")
    for field, value in (
        ("actor_id", "user:fixture"),
        ("branch_id", "wrong-branch"),
        ("e1_event_hash", "0" * 64),
    ):
        bad = copy.deepcopy(realized)
        bad["objective"]["event"][field] = value
        with pytest.raises(CompressionRefusal):
            bind(spec, identity=identity, proposal=proposal,
                 catalog=catalog, realized=bad)

    bad = copy.deepcopy(realized)
    bad["readset"] = [proposal["source_refs"][0]]
    with pytest.raises(CompressionRefusal, match="readset"):
        bind(spec, identity=identity, proposal=proposal,
             catalog=catalog, realized=bad)


def test_absent_actor_access_returns_held_not_positive_or_nochange() -> None:
    identity, proposal, catalog, spec, realized = docs("SINGULAR_OCCURRENCE")
    for accessible in (
        {"status": "HELD", "actor_ref": identity["actor"], "events": []},
        {"status": "OBSERVED", "actor_ref": identity["actor"], "events": []},
    ):
        bad = copy.deepcopy(realized)
        bad["accessible"] = accessible
        result = bind(spec, identity=identity, proposal=proposal,
                      catalog=catalog, realized=bad)
        assert result["status"] == "HELD"
        assert result["actor_access"] == "HELD"
        assert result["perception_refs"] == []
        assert result["psychological_effects"] == []
        assert result["held_reason"] in {
            "ACTOR_ACCESS_UNAVAILABLE",
            "ACTOR_PERCEPTION_UNAVAILABLE_FOR_PRESENT_EVENT",
        }


def test_user_view_marker_or_wrong_actor_access_is_refused() -> None:
    identity, proposal, catalog, spec, realized = docs("SINGULAR_OCCURRENCE")
    leaked = copy.deepcopy(realized)
    leaked["accessible"]["events"][0]["perceived_by_user"] = True
    with pytest.raises(CompressionRefusal, match="user-view"):
        bind(spec, identity=identity, proposal=proposal,
             catalog=catalog, realized=leaked)

    wrong_actor = copy.deepcopy(realized)
    wrong_actor["accessible"]["actor_ref"] = "user:fixture"
    with pytest.raises(CompressionRefusal, match="different actor"):
        bind(spec, identity=identity, proposal=proposal,
             catalog=catalog, realized=wrong_actor)


def test_actual_interval_basis_is_required_for_accumulated_interval() -> None:
    identity, proposal, catalog, spec, realized = docs("ACCUMULATED_INTERVAL")
    missing = copy.deepcopy(realized)
    missing["objective"]["interval"] = None
    missing["consequences"]["interval"] = None
    result = bind(spec, identity=identity, proposal=proposal,
                  catalog=catalog, realized=missing)
    assert result["status"] == "HELD"
    assert result["held_reason"] == "ACTUAL_INTERVAL_UNAVAILABLE"

    for bad_status in ("NOT_PERFORMED", "UNKNOWN"):
        bad = copy.deepcopy(realized)
        bad["objective"]["interval"]["status"] = bad_status
        bad["consequences"]["interval"]["status"] = bad_status
        result = bind(spec, identity=identity, proposal=proposal,
                      catalog=catalog, realized=bad)
        assert result["status"] == "HELD"
        assert result["held_reason"] == "ACTUAL_INTERVAL_UNAVAILABLE"


def test_native_nochange_is_preserved_without_psych_effect() -> None:
    identity, proposal, catalog, spec, realized = docs("SINGULAR_OCCURRENCE")
    realized["status"] = "NO_CHANGE"
    result = bind(spec, identity=identity, proposal=proposal,
                  catalog=catalog, realized=realized)
    assert result["status"] == "BOUND"
    assert result["native_status"] == "NO_CHANGE"
    assert result["psychological_effects"] == []
    assert result["no_psychological_effects"] is True


def test_actual_event_held_or_absent_is_held_not_nochange() -> None:
    identity, proposal, catalog, spec, realized = docs("SINGULAR_OCCURRENCE")
    held = copy.deepcopy(realized)
    held["status"] = "HELD"
    result = bind(spec, identity=identity, proposal=proposal,
                  catalog=catalog, realized=held)
    assert result["status"] == "HELD"
    assert result["native_status"] == "HELD"
    assert result["held_reason"] == "ACTUAL_EVENT_NOT_AVAILABLE"
    assert result["psychological_effects"] == []

    absent = copy.deepcopy(realized)
    absent["objective"]["event"] = None
    result = bind(spec, identity=identity, proposal=proposal,
                  catalog=catalog, realized=absent)
    assert result["status"] == "HELD"
    assert result["held_reason"] == "ACTUAL_EVENT_UNAVAILABLE"
    assert result["actual_event_ref"] is None


def test_preflight_rejects_present_event_at_or_before_owner_clock() -> None:
    identity, proposal, catalog, spec, _realized = docs("SINGULAR_OCCURRENCE")
    bad_identity = copy.deepcopy(identity)
    bad_identity["clock"] = proposal["event_time"]
    with pytest.raises(CompressionRefusal, match="after the owner clock"):
        preflight(spec, identity=bad_identity, proposal=proposal, catalog=catalog)


def test_actual_after_clock_must_not_move_backwards() -> None:
    identity, proposal, catalog, spec, realized = docs("SINGULAR_OCCURRENCE")
    bad = copy.deepcopy(realized)
    bad["after"]["clock"] = identity["clock"] - 1
    with pytest.raises(CompressionRefusal, match="clock"):
        bind(spec, identity=identity, proposal=proposal,
             catalog=catalog, realized=bad)


def test_summary_actor_experience_shape_is_supported_without_user_view() -> None:
    identity, proposal, catalog, spec, realized = docs("SINGULAR_OCCURRENCE")
    summary = copy.deepcopy(realized)
    summary["accessible"] = {
        "status": "OBSERVED",
        "actor_ref": identity["actor"],
        "event_ids": ["TEST_ONLY_P2_EVENT_1"],
        "perceptions": [{"clock": 100, "channel": "co_present"}],
        "memory_formation": "MISSING_RULE",
    }
    result = bind(spec, identity=identity, proposal=proposal,
                  catalog=catalog, realized=summary)
    assert result["status"] == "BOUND"
    assert result["perception_refs"]
