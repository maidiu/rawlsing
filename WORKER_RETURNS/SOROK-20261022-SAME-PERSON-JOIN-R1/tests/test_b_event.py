"""Focused upstream B-event contrast for the sourcefree JOIN-E cut."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from joined.assertion import b_event_positive
from joined.b_event import (
    OMITTED,
    PERFORMED,
    REFUSED,
    BSourceUnavailable,
    disposition_from_source,
    receipt_for_case,
)
from joined.refusal import RefusalSession
from joined.session import JoinedSession
from r30a.first_session import SessionRefusal
from r31j.scenarios import A, case as r31j_case
from generative_resource import sha

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]


def _c8_event(session) -> dict:
    from c8_readonly_consumer import C8ReadOnlyConsumer

    product = session.product
    if hasattr(product, "artifacts"):
        journal = product.artifacts.journal_path
        occurrence = product.artifacts.occurrence_id
    else:
        binding = product.c8_binding
        journal = binding["journal_path"]
        occurrence = binding["occurrence_id"]
    view = C8ReadOnlyConsumer(str(journal)).load()
    event = view.get(occurrence)
    assert event, "C8 occurrence absent"
    return event


def _episode_kinds(session) -> list[str]:
    return [row["kind"] for row in session.episodes()]


def _meta_path(state: Path) -> Path:
    return state / "session.json"


def _read_meta(state: Path) -> dict:
    return json.loads(_meta_path(state).read_text(encoding="utf8"))


def _write_meta(state: Path, meta: dict) -> None:
    _meta_path(state).write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf8")


def _cli(*args: str, state: Path) -> dict:
    env = {
        **os.environ,
        "PYTHONPATH": str(RETURN),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    run = subprocess.run(
        [sys.executable, "-B", "-m", "joined.cli", *args, "--state", str(state)],
        cwd=str(REPO), env=env, text=True, capture_output=True, timeout=120,
    )
    assert run.returncode == 0, run.stderr[-2000:]
    return json.loads(run.stdout)


def test_b_performed_receipt_source_c8_c9_c12_help_and_cold(tmp_path):
    state = tmp_path / "performed"
    session = JoinedSession.start(state, perform="omit")
    try:
        source = session.product.source
        receipt = session.meta["b_performer_receipt"]
        assert session.meta["j_b_disposition"] == PERFORMED
        assert receipt["schema"] == "SOROK_JOIN_E_B_PERFORMER_RECEIPT@1"
        assert receipt["disposition"] == PERFORMED
        assert receipt["event_hash"] == source["b_event_hash"]
        assert receipt["clock"] == source["b_clock"] == 5
        assert source["b_operation"] == "SHARE_TOOL"
        assert source["b_performed"] is True
        assert source["b_quantity"] == 1
        assert source["b_to_actor"] == "TEST_ONLY_R31J_A"
        assert disposition_from_source(source) == PERFORMED

        event = _c8_event(session)
        payload = event["payload"]
        assert payload["gm01_pre_c9_source"] == source
        assert payload["world"]["material_ref"] == (
            "TEST_ONLY_R31J_GM01_MATERIAL_" + source["b_event_hash"][:16])
        assert payload["world"]["material_receipt_id"] == source["b_event_hash"]

        assert session.meta["j_target_id"]
        episodes = session.episodes()
        gm01 = [row for row in episodes if row["kind"] == "GM01_SOURCE"]
        assert len(gm01) == 1
        assert gm01[0]["body"]["gm01_source"] == source
        assert gm01[0]["body"]["c9_target_id"] == session.meta["j_target_id"]
        assert session.branch_id == "first_session"
        assert Path(session.product.root).resolve() == (state / "product").resolve()

        helped = session.do_help()
        assert helped["accepted"] is True
        assert helped["strategy"] == "HELP_ACCEPT"
        assert session.world().actor_state["A"]["tools_remaining"] == 1
        frozen = b_event_positive(session, help_result=helped)
        assert frozen["ok"] is True, frozen
        assert frozen["checks"]["b_receipt_matches_source"] is True
        assert session.verify()["ok"] is True
    finally:
        session.close()

    cold = JoinedSession.open(state)
    try:
        assert cold.product.source == source
        assert cold.meta["j_b_disposition"] == PERFORMED
        helped = cold.do_help()
        assert helped["accepted"] is True
        assert b_event_positive(cold, help_result=helped)["ok"] is True
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_b_omitted_receipt_source_c8_targetless_c12_help_and_cold(tmp_path):
    state = tmp_path / "omitted"
    session = RefusalSession.start(state, b_disposition=OMITTED)
    try:
        source = session.product.source
        receipt = session.meta["b_performer_receipt"]
        assert session.meta["j_b_disposition"] == OMITTED
        assert session.meta["material_performance"] == "omitted"
        assert receipt["disposition"] == OMITTED
        assert receipt["event_hash"] == source["b_event_hash"]
        assert receipt["clock"] == source["b_clock"] == 5
        assert source["b_operation"] == "SHARE_TOOL"
        assert source["b_performed"] is False
        assert source["b_quantity"] == 1
        assert source["b_to_actor"] == "TEST_ONLY_R31J_A"
        assert disposition_from_source(source) == OMITTED

        event = _c8_event(session)
        payload = event["payload"]
        assert payload["gm01_pre_c9_source"] == source
        assert payload["world"]["material_ref"] == (
            "TEST_ONLY_R31J_GM01_MATERIAL_" + source["b_event_hash"][:16])
        assert payload["world"]["material_receipt_id"] == source["b_event_hash"]

        kinds = _episode_kinds(session)
        assert "GM01_OMISSION" in kinds
        assert "GM01_REFUSAL" not in kinds
        assert session.meta["c9"]["target_branch"] == "NO_CHANGE"
        assert session.meta["c9"]["target_reason"] == "NO_PROPOSAL"
        assert session.meta["c9"]["target_id"] == ""
        assert session.meta["target_id"] == ""
        assert session.status()["targetless"] is True
        assert session.branch_id == "first_session"
        assert Path(session.product.root).resolve() == (state / "product").resolve()

        refused = session.do_help()
        assert refused["accepted"] is False
        assert refused["strategy"] == "HELP_REFUSE"
        assert session.world().actor_state["A"]["tools_remaining"] == 0
        cut_assertion = b_event_positive(session, help_result=refused)
        assert cut_assertion["ok"] is False
        assert cut_assertion["checks"]["b_disposition_performed"] is False
        assert cut_assertion["checks"]["target_present"] is False
        assert cut_assertion["checks"]["help_admitted"] is False
        assert session.verify()["ok"] is True
    finally:
        session.close()

    cold = RefusalSession.open(state)
    try:
        assert cold.product.source == source
        assert cold.meta["j_b_disposition"] == OMITTED
        refused = cold.do_help()
        assert refused["accepted"] is False
        assert b_event_positive(cold, help_result=refused)["ok"] is False
        assert cold.meta["target_id"] == ""
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_b_refusal_omission_and_unavailable_source_are_distinct(tmp_path):
    performed = JoinedSession.start(tmp_path / "performed", perform="omit")
    refused = RefusalSession.start(tmp_path / "refused", b_disposition=REFUSED)
    omitted = RefusalSession.start(tmp_path / "omitted", b_disposition=OMITTED)
    try:
        receipts = {
            REFUSED: refused.meta["b_performer_receipt"],
            OMITTED: omitted.meta["b_performer_receipt"],
            PERFORMED: performed.meta["b_performer_receipt"],
        }
        assert {key: value["disposition"] for key, value in receipts.items()} == {
            REFUSED: REFUSED, OMITTED: OMITTED, PERFORMED: PERFORMED}
        assert receipts[REFUSED]["operation"] == "REFUSE_TOOL"
        assert receipts[REFUSED]["performed"] is True
        assert receipts[OMITTED]["operation"] == "SHARE_TOOL"
        assert receipts[OMITTED]["performed"] is False
        assert receipts[PERFORMED]["operation"] == "SHARE_TOOL"
        assert receipts[PERFORMED]["performed"] is True
        assert len({value["event_hash"] for value in receipts.values()}) == 3
        assert "GM01_REFUSAL" in _episode_kinds(refused)
        assert "GM01_OMISSION" in _episode_kinds(omitted)
        assert "GM01_OMISSION" not in _episode_kinds(refused)
        assert "GM01_REFUSAL" not in _episode_kinds(omitted)
        assert performed.do_help()["accepted"] is True
        assert refused.do_help()["accepted"] is False
        assert omitted.do_help()["accepted"] is False
        assert refused.meta["target_id"] == omitted.meta["target_id"] == ""
        assert performed.meta["j_target_id"]
        c8_digests = {key: value["j_c8_state_digest"] for key, value in (
            (REFUSED, refused.meta), (OMITTED, omitted.meta),
            (PERFORMED, performed.meta))}
        assert len(set(c8_digests.values())) == 3
        assert refused.verify()["ok"] is True
        assert omitted.verify()["ok"] is True
        assert performed.verify()["ok"] is True
    finally:
        performed.close()
        refused.close()
        omitted.close()

    unavailable = tmp_path / "unavailable"
    with pytest.raises(BSourceUnavailable) as exc:
        RefusalSession.start(unavailable, b_disposition="UNAVAILABLE")
    assert exc.value.code == "B_SOURCE_OCCURRENCE_ABSENT"
    assert not (unavailable / "session.json").exists()
    assert not (unavailable / "product").exists()

    case = r31j_case(share=True, e2=False)
    record = dict(case["records"][1])
    record["subject"] = A
    record["content_hash"] = sha(
        {key: value for key, value in record.items() if key != "content_hash"})
    bad = dict(case)
    bad["records"] = list(case["records"])
    bad["records"][1] = record
    with pytest.raises(BSourceUnavailable) as exc:
        receipt_for_case(bad, PERFORMED)
    assert exc.value.code == "B_SOURCE_SUBJECT_NOT_B"


def test_unchanged_b_event_assertion_red_on_upstream_cut_green_on_restore_cold(
        tmp_path):
    performed_state = tmp_path / "performed"
    performed = JoinedSession.start(performed_state, perform="omit")
    try:
        help_result = performed.do_help()
        baseline = b_event_positive(performed, help_result=help_result)
        assert baseline["ok"] is True, baseline
        assert baseline["observed"]["help_strategy"] == "HELP_ACCEPT"
    finally:
        performed.close()

    cut_state = tmp_path / "cut"
    cut = RefusalSession.start(cut_state, b_disposition=OMITTED)
    try:
        help_result = cut.do_help()
        cut_assertion = b_event_positive(cut, help_result=help_result)
        assert cut_assertion["ok"] is False
        assert cut_assertion["checks"]["b_source_is_performed_share"] is False
        assert cut_assertion["checks"]["help_admitted"] is False
        assert cut_assertion["observed"]["b_operation"] == "SHARE_TOOL"
        assert cut.verify()["ok"] is True
    finally:
        cut.close()

    cold_cut = RefusalSession.open(cut_state)
    try:
        help_result = cold_cut.do_help()
        assert b_event_positive(cold_cut, help_result=help_result)["ok"] is False
        assert cold_cut.verify()["ok"] is True
    finally:
        cold_cut.close()

    restored_state = tmp_path / "restored"
    restored = JoinedSession.start(restored_state, perform="omit")
    try:
        help_result = restored.do_help()
        restored_assertion = b_event_positive(restored, help_result=help_result)
        assert restored_assertion["ok"] is True, restored_assertion
        assert restored_assertion["observed"]["help_strategy"] == "HELP_ACCEPT"
        assert restored.verify()["ok"] is True
    finally:
        restored.close()

    cold_restored = JoinedSession.open(restored_state)
    try:
        help_result = cold_restored.do_help()
        assert b_event_positive(
            cold_restored, help_result=help_result)["ok"] is True
        assert cold_restored.verify()["ok"] is True
    finally:
        cold_restored.close()


def test_b_performer_receipt_and_disposition_tamper_are_rejected(tmp_path):
    state = tmp_path / "performed"
    session = JoinedSession.start(state, perform="omit")
    session.close()
    original = _read_meta(state)

    receipt_tamper = json.loads(json.dumps(original))
    receipt_tamper["b_performer_receipt"]["event_hash"] = "0" * 64
    _write_meta(state, receipt_tamper)
    with pytest.raises(SessionRefusal) as exc:
        JoinedSession.open(state)
    assert exc.value.code == "J_PROVENANCE_MISMATCH"

    disposition_tamper = json.loads(json.dumps(original))
    disposition_tamper["j_b_disposition"] = OMITTED
    _write_meta(state, disposition_tamper)
    with pytest.raises(SessionRefusal) as exc:
        JoinedSession.open(state)
    assert exc.value.code == "J_PROVENANCE_MISMATCH"

    _write_meta(state, original)
    reopened = JoinedSession.open(state)
    try:
        assert reopened.meta["j_b_disposition"] == PERFORMED
        assert reopened.verify()["ok"] is True
    finally:
        reopened.close()

    omitted_state = tmp_path / "omitted"
    omitted = RefusalSession.start(omitted_state, b_disposition=OMITTED)
    omitted.close()
    omitted_meta = _read_meta(omitted_state)
    omitted_meta["b_performer_receipt"]["clock"] = 6
    _write_meta(omitted_state, omitted_meta)
    with pytest.raises(SessionRefusal) as exc:
        RefusalSession.open(omitted_state)
    assert exc.value.code == "J_PROVENANCE_MISMATCH"


def test_lawful_refusal_and_incompatible_root_are_still_preserved(tmp_path):
    refused = RefusalSession.start(tmp_path / "refused")
    performed = JoinedSession.start(tmp_path / "performed", perform="omit")
    try:
        assert refused.product.source["b_operation"] == "REFUSE_TOOL"
        assert refused.product.source["b_performed"] is True
        assert refused.meta["c9"]["target_branch"] == "NO_CHANGE"
        assert refused.meta["target_id"] == ""
        assert refused.do_help()["strategy"] == "HELP_REFUSE"
        assert refused.verify()["ok"] is True
        performed.close()
        performed = None

        meta = _read_meta(tmp_path / "performed")
        meta["product_root"] = str(
            (tmp_path / "refused" / "product").resolve())
        _write_meta(tmp_path / "performed", meta)
        with pytest.raises(SessionRefusal) as exc:
            JoinedSession.open(tmp_path / "performed")
        assert exc.value.code == "FOREIGN_PRODUCT_ROOT"
    finally:
        if performed is not None:
            performed.close()
        refused.close()


def test_cli_b_contrast_runs_cut_and_restore_interface(tmp_path):
    result = _cli("b-contrast", state=tmp_path / "contrast")
    assert result["schema"] == "SOROK_JOIN_E_B_EVENT_CONTRAST@1"
    assert result["assertion"] == "SOROK_JOIN_E_B_EVENT_UPSTREAM_P01"
    assert result["performed"]["assertion"]["ok"] is True
    assert result["omitted"]["assertion"]["ok"] is False
    assert result["performed"]["help"] == {
        "accepted": True, "strategy": "HELP_ACCEPT"}
    assert result["omitted"]["help"] == {
        "accepted": False, "strategy": "HELP_REFUSE"}
    assert result["performed"]["j_b_disposition"] == PERFORMED
    assert result["omitted"]["j_b_disposition"] == OMITTED
    assert result["performed"]["target_id"]
    assert result["omitted"]["target_id"] == ""
    assert result["cut_restore"]["cut_assertion_ok"] is False
    assert result["cut_restore"]["restored_assertion_ok"] is True
    assert result["performed"]["branch_id"] == "first_session"
    assert result["omitted"]["branch_id"] == "first_session"
    assert result["performed"]["session_verify"]["ok"] is True
    assert result["omitted"]["session_verify"]["ok"] is True
