"""Focused S47 interval-to-C9 conditioning over the accepted S46 person."""
from __future__ import annotations

from copy import deepcopy

import pytest

from s47.bootstrap import install

install()

from s45.fixtures import root_bundle  # noqa: E402
from s46.errors import S46Refusal  # noqa: E402
from s46.model import make_domain  # noqa: E402
from s47.conditioning import SOURCE_CLASS, qualify_source  # noqa: E402
from s47.errors import S47Refusal  # noqa: E402
from s47.session import S47Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _start(state, seed="01" * 32):
    case = case_for(True)
    return S47Session.start(
        state,
        bundle=root_bundle(seed),
        case=case,
        source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )


def _admit(session):
    first = session.read_events()[0]
    return session.admit_event(
        case=case_for(True),
        source=source_for(case_for(True)),
        history_event_refs=(first["e1_event_id"],),
        event_time=session.clock() + 1,
    )


@pytest.mark.parametrize("mode,material", [("ACTUAL", False), ("SCHEDULED_ONLY", True)])
def test_real_c9_consumes_interval_material_and_keeps_targetless(tmp_path, mode, material):
    state = tmp_path / mode.lower()
    session = _start(state)
    try:
        root_hash = session.read_root()["root_hash"]
        before_b = dict(session.world().actor_state["B"])
        produced = session.produce_interval(
            make_domain(mode=mode, start=session.clock(), end=session.clock() + 4)
        )
        source = session.c9_interval_source()
        assert source["source_class"] == SOURCE_CLASS
        assert source["content"]["currentness"] == "CURRENT"
        assert source["content"]["coverage"] == produced["coverage"]
        assert source["content"]["interval_receipt_hash"] == produced["receipt_hash"]
        result = _admit(session)
        assert result["status"] == "OK"
        read = session.read_c9_conditioning()
        assert read["s47_source_in_readset"] is True
        assert read["s47_source_ref"] == source["source_ref"]
        assert read["objective_material_eligible"] is material
        if material:
            assert read["objective_material_refs"] == [source["source_ref"]]
        else:
            assert read["objective_material_refs"] == []
        assert read["target_branch"] == "NO_CHANGE"
        assert read["target_reason"] == "NO_PROPOSAL"
        assert read["target_proposals"] == []
        assert read["s47_source"]["content"]["private_b_motive_included"] is False
        assert read["s47_source"]["content"]["actor_knowledge_inferred"] is False
        assert session.world().actor_state["B"] == before_b
        assert session.read_root()["root_hash"] == root_hash
        assert session.verify()["ok"] is True
    finally:
        session.close()


@pytest.mark.parametrize("mode", ["BLOCKED", "UNKNOWN"])
def test_no_mutation_modes_are_current_conditioning_but_not_material_claims(tmp_path, mode):
    session = _start(tmp_path / mode.lower())
    try:
        before = session.world().actor_state["A"]["material_remaining"]
        produced = session.produce_interval(
            make_domain(mode=mode, start=session.clock(), end=session.clock() + 2)
        )
        assert produced["status"] == ("NOT_PERFORMED" if mode == "BLOCKED" else "UNKNOWN")
        assert session.world().actor_state["A"]["material_remaining"] == before
        source = session.c9_interval_source()
        assert source["content"]["status"] == produced["status"]
        assert source["content"]["actor_knowledge_inferred"] is False
        _admit(session)
        read = session.read_c9_conditioning()
        assert read["s47_source_in_readset"] is True
        assert read["target_branch"] == "NO_CHANGE"
        assert read["target_reason"] == "NO_PROPOSAL"
    finally:
        session.close()


def test_condition_cut_refuses_and_restore_reconstructs_same_c9_source(tmp_path):
    state = tmp_path / "condition"
    session = _start(state)
    closed = False
    try:
        produced = session.produce_interval(
            make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        )
        earlier_hash = session.c9_interval_source()["source_hash"]
        session.revoke_interval_condition(produced["state_id"], reason="TEST_ONLY_CUT")
        with pytest.raises(S46Refusal) as exc:
            _admit(session)
        assert exc.value.code == "S46_INTERVAL_CONDITION_REVOKED"
        session.restore_interval_condition(produced["state_id"], reason="TEST_ONLY_RESTORE")
        assert session.c9_interval_source()["source_hash"] == earlier_hash
        _admit(session)
        read = session.read_c9_conditioning()
        assert read["s47_source_in_readset"] is True
        assert read["objective_material_eligible"] is False
        assert read["s47_source"]["content"]["coverage"] == produced["coverage"]
        session.close()
        closed = True
        cold = S47Session.open(state)
        try:
            cold_source = cold.c9_interval_source()
            assert cold_source["source_hash"] == earlier_hash
            assert cold_source["content"]["interval_receipt_hash"] == produced["receipt_hash"]
            cold_read = cold.read_c9_conditioning()
            assert cold_read["s47_source_ref"] == cold_source["source_ref"]
            assert cold_read["s47_source_in_readset"] is True
            assert cold_read["target_branch"] == "NO_CHANGE"
            assert cold.verify()["ok"] is True
        finally:
            cold.close()
    finally:
        if not closed:
            session.close()


@pytest.mark.parametrize("field,value,code", [
    ("actor_id", "WRONG_ACTOR", "S47_SOURCE_ACTOR_ID_MISMATCH"),
    ("branch_id", "wrong_branch", "S47_SOURCE_BRANCH_ID_MISMATCH"),
    ("coverage", [[1, 2]], "S47_SOURCE_COVERAGE_MISMATCH"),
    ("currentness", "SUPERSEDED", "S47_SOURCE_CURRENTNESS_MISMATCH"),
    ("access", "granted", "S47_SOURCE_ACCESS_MISMATCH"),
    ("as_of", 0, "S47_SOURCE_AS_OF_MISMATCH"),
    ("material_after_interval", True, "S47_SOURCE_MATERIAL_AFTER_INTERVAL_MISMATCH"),
])
def test_forged_conditioning_source_is_refused_then_original_remains(tmp_path, field, value, code):
    session = _start(tmp_path / ("forge-" + field))
    try:
        session.produce_interval(
            make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        )
        real = session.c9_interval_source()
        forged = deepcopy(real)
        forged["content"][field] = value
        from candidate.conditioning import make_conditioning_source
        rebuilt = make_conditioning_source(
            source_ref=forged["source_ref"], source_class=forged["source_class"],
            subject=forged["subject"], body=forged["content"],
        )
        forged["source_hash"] = rebuilt["source_hash"]
        with pytest.raises(S47Refusal) as exc:
            qualify_source(session, forged)
        assert exc.value.code == code
        assert qualify_source(session, real)["source_hash"] == real["source_hash"]
        assert session.c9_interval_source()["source_hash"] == real["source_hash"]
    finally:
        session.close()


def test_no_interval_preserves_accepted_c9_path(tmp_path):
    session = _start(tmp_path / "no-interval")
    try:
        assert session.c9_interval_source() is None
        _admit(session)
        read = session.read_c9_conditioning()
        assert read["s47_source"] is None
        assert read["s47_source_in_readset"] is False
        assert read["target_branch"] == "NO_CHANGE"
        assert read["target_reason"] == "NO_PROPOSAL"
        assert session.verify()["ok"] is True
    finally:
        session.close()
