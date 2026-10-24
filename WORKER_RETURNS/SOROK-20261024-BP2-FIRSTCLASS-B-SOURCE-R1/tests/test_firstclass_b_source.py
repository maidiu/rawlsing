"""First-class B material source through BP2/C8/C9 and the existing E consumer."""
from __future__ import annotations

import pytest
from c8_readonly_consumer import C8ReadOnlyConsumer

import firstclass
from firstclass import MaterialSourceRefusal
from joined.assertion import positive, refusal_no_target
from joined.refusal import RefusalSession
from joined.session import JoinedSession
from r31j.scenarios import evaluated


def _share_state(tmp_path):
    return tmp_path / "share"


def _refusal_state(tmp_path):
    return tmp_path / "refusal"


def _share_c8_source(session):
    artifacts = session.product.artifacts
    view = C8ReadOnlyConsumer(str(artifacts.journal_path)).load()
    event = view.get(artifacts.occurrence_id)
    assert event, "C8 occurrence absent"
    payload = event.get("payload") or {}
    return payload, payload.get("gm01_pre_c9_source")


def _refusal_c8_source(session):
    binding = session.product.c8_binding
    view = C8ReadOnlyConsumer(str(binding["journal_path"])).load()
    event = view.get(binding["occurrence_id"])
    assert event, "C8 occurrence absent"
    payload = event.get("payload") or {}
    return payload, payload.get("gm01_pre_c9_source")


def _tools(session):
    return session.product._world(session.branch_id).actor_state["A"]["tools_remaining"]


def _admitted_material_inspect(session):
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == "DO"
        and (row.get("body") or {}).get("action") == "material_inspect"
        and (row.get("body") or {}).get("admitted") is True
    ]


def test_source_is_derived_from_b_operation_not_the_gm01_boolean(tmp_path):
    scenario = evaluated(share=True, e2=False)
    partial, producer = firstclass.c9_only(
        tmp_path / "derive",
        gm01={"material_feasible_after": False},
        case=scenario["case"],
    )
    try:
        assert partial["gm01_source"]["b_operation"] == "SHARE_TOOL"
        assert partial["gm01_source"]["b_quantity"] == 1
        assert partial["gm01_source"]["b_performed"] is True
        assert partial["material_access"] == "granted"
        assert producer.historical_life.a_snapshot["state"]["tools_remaining"] == 1
        assert partial["c9"]["target_branch"] == "CREATE"
        assert partial["c9"]["target_id"]
    finally:
        producer.close()


def test_source_rejects_missing_owner_quantity_recipient_and_clock(tmp_path):
    case = evaluated(share=True, e2=False)["case"]
    source = firstclass.source_from_case(case)
    mutations = (
        ("b_owner", ""),
        ("b_quantity", 0),
        ("b_to_actor", "TEST_ONLY_NOT_A"),
        ("b_clock", -1),
        ("b_performed", False),
        ("material_feasible_after", True),
    )
    for index, (field, value) in enumerate(mutations):
        mutated = dict(source)
        mutated[field] = value
        root = tmp_path / f"invalid-{index}"
        with pytest.raises(MaterialSourceRefusal):
            firstclass.build_product(root, case=case, source=mutated,
                                     need_e2=False)
        assert not (root / "bp2").exists(), field


def test_share_source_is_sealed_before_c8_and_cold_reopens(tmp_path):
    state = _share_state(tmp_path)
    session = JoinedSession.start(state, perform="omit")
    try:
        source = session.product.source
        payload, c8_source = _share_c8_source(session)
        assert source["schema"] == "BP2_FIRSTCLASS_B_MATERIAL_SOURCE@1"
        assert source["b_operation"] == "SHARE_TOOL"
        assert source["b_quantity"] == 1
        assert source["b_performed"] is True
        assert source["b_owner"]
        assert source["b_to_actor"] == "TEST_ONLY_R31J_A"
        assert source["b_clock"] == 5
        assert c8_source == source
        assert payload["world"]["material_ref"] == source["b_event_ref"]
        assert payload["world"]["material_receipt_id"] == source["b_event_hash"]
        assert session.meta["j_target_id"]
        world = session.product._world(session.branch_id)
        assert world.actor_state["A"]["tools_remaining"] == 1
        helped = session.do_help()
        assert helped["accepted"] is True
        assert helped["strategy"] == "HELP_ACCEPT"
        assert positive(session, help_result=helped)["ok"] is True
        assert _admitted_material_inspect(session) == []
    finally:
        session.close()

    cold = JoinedSession.open(state)
    try:
        assert cold.product.source == source
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_refusal_source_is_sealed_before_c8_and_targetless_e_refuses(tmp_path):
    share_state = _share_state(tmp_path)
    share = JoinedSession.start(share_state, perform="omit")
    try:
        share_payload, share_source = _share_c8_source(share)
        share_digest = share.meta["j_c8_state_digest"]
        share_target = share.meta["j_target_id"]
        share_help = share.do_help()
        assert share_help["accepted"] is True
    finally:
        share.close()

    state = _refusal_state(tmp_path)
    session = RefusalSession.start(state)
    try:
        source = session.product.source
        payload, c8_source = _refusal_c8_source(session)
        assert source["b_operation"] == "REFUSE_TOOL"
        assert source["b_quantity"] == 0
        assert source["b_performed"] is True
        assert source["b_actor"] == "TEST_ONLY_R31J_B"
        assert source["b_to_actor"] == "TEST_ONLY_R31J_A"
        assert c8_source == source
        assert payload["world"]["material_ref"] == source["b_event_ref"]
        assert payload["world"]["material_receipt_id"] == source["b_event_hash"]
        assert session.meta["j_c8_state_digest"] != share_digest
        assert share_payload["gm01_pre_c9_source"] != c8_source
        assert session.meta["c9"]["target_branch"] == "NO_CHANGE"
        assert session.meta["c9"]["target_reason"] == "NO_PROPOSAL"
        assert session.meta["target_id"] == ""
        refused = session.do_help()
        assert refused["accepted"] is False
        assert refused["strategy"] == "HELP_REFUSE"
        assert _admitted_material_inspect(session) == []
        assert session.verify()["ok"] is True
        restored = JoinedSession.start(tmp_path / "restored", perform="omit")
        try:
            assert restored.product.source["b_operation"] == "SHARE_TOOL"
            assert restored.do_help()["accepted"] is True
        finally:
            restored.close()
    finally:
        session.close()

    cold = RefusalSession.open(state)
    try:
        assert cold.product.source == source
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_refusal_probe_keeps_no_target_and_no_ghost_performed_inspection(tmp_path):
    probe = JoinedSession.probe_refusal(tmp_path / "probe")
    frozen = refusal_no_target(probe)
    assert frozen["ok"] is True, frozen
    assert probe["source"]["b_operation"] == "REFUSE_TOOL"
    assert probe["source"]["b_quantity"] == 0
    assert probe["c9"]["target_branch"] == "NO_CHANGE"
    assert probe["c9"]["target_reason"] == "NO_PROPOSAL"
    assert probe["target_id"] == ""

    session = RefusalSession.start(tmp_path / "refusal")
    try:
        assert _admitted_material_inspect(session) == []
        assert "a_performed" not in session.product.source
        assert "material_feasible_after" not in session.product.source
    finally:
        session.close()


def test_share_e2_is_a_separate_performed_action(tmp_path):
    session = JoinedSession.start(tmp_path / "e2", perform="e2")
    try:
        assert session.product.source["b_operation"] == "SHARE_TOOL"
        assert session.product.source["b_performed"] is True
        assert _tools(session) == 0
        inspects = _admitted_material_inspect(session)
        assert len(inspects) == 1
        body = inspects[0]["body"]
        assert body["action"] == "material_inspect"
        assert body["admitted"] is True
        assert body["gm01_b_event_hash"] == session.product.source["b_event_hash"]
        helped = session.do_help()
        assert helped["accepted"] is False
        assert helped["strategy"] == "HELP_REFUSE"
    finally:
        session.close()
