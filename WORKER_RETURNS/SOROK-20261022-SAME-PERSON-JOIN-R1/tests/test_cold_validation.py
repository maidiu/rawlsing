"""Cold validation of the persisted B-event binding and genuine legacy reopen."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from joined.assertion import positive
from joined.closure import source_manifest_sha256
from joined.session import JoinedSession
from r30a.first_session import SessionRefusal
from r31j.build import product as build_product
from r31j.scenarios import evaluated

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
J_SOURCE_REF = "64fec28c374d8f77fb0b412d0c934d798ede03e8"
E_SOURCE_REF = "a2760d3687b063513fe0a5b9589c56c998d4ccb5"


def _meta_path(state: Path) -> Path:
    return state / "session.json"


def _read_meta(state: Path) -> dict:
    return json.loads(_meta_path(state).read_text(encoding="utf8"))


def _write_meta(state: Path, meta: dict) -> None:
    _meta_path(state).write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf8")


def _legacy_start(state: Path, perform: str = "omit") -> JoinedSession:
    """Build a genuine pre-B-event session through the old construction path."""
    state = state.resolve()
    state.mkdir(parents=True, exist_ok=True)
    scenario = evaluated(share=True, e2=perform == "e2")
    product, built, producer = build_product(
        state, gm01=scenario["gm01"], case=scenario["case"],
        variant="A_REPAIR_LONG")
    producer.close()
    if perform == "e2":
        product.material_inspect()
    else:
        product.record_omission()
    session = JoinedSession._attach_new(
        product, state, scenario="available", attention="focused",
        variant="A_REPAIR_LONG")
    seed = product.seed.public()
    session.meta.update(
        schema="SOROK_SAME_PERSON_JOIN@1",
        grade="TEST_ONLY_SOURCEFREE_NOT_NATIVE",
        material_performance=perform,
        root_branch_id="root",
        branch_lineage=None,
        j_source_ref=J_SOURCE_REF,
        e_source_ref=E_SOURCE_REF,
        j_source=dict(product.source),
        j_c8_state_digest=built["c8_state_digest"],
        j_e1_event_hash=built["e1_event_hash"],
        j_target_id=built["target_id"],
        source_actor_map={
            "TEST_ONLY_R31J_A": seed["actor_a"],
            "TEST_ONLY_R31J_B": seed["actor_b"],
        },
        source_manifest_sha256=source_manifest_sha256(),
        expression_port="R31E_EXPRESSION_PORT@1",
        actor_model="LIVE_ACTOR_MODEL_NOT_RUN",
    )
    session._save_join_meta()
    return session


def _cold_process(state: Path) -> dict:
    code = """
import json, sys
from joined.session import JoinedSession
try:
    session = JoinedSession.open(sys.argv[1])
    try:
        result = {
            "ok": True,
            "verify": session.verify()["ok"],
            "binding_episodes": [
                row["kind"] for row in session.episodes()
                if row["kind"] == "B_EVENT_BINDING"
            ],
            "branch_id": session.branch_id,
            "root": str(session.product.root),
        }
    finally:
        session.close()
except Exception as exc:
    result = {
        "ok": False,
        "code": getattr(exc, "code", ""),
        "error": type(exc).__name__ + ":" + str(exc),
    }
print(json.dumps(result, sort_keys=True))
"""
    env = {
        **os.environ,
        "PYTHONPATH": str(RETURN),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    run = subprocess.run(
        [sys.executable, "-B", "-c", code, str(state)],
        cwd=str(REPO), env=env, text=True, capture_output=True, timeout=120,
    )
    assert run.returncode == 0, run.stderr[-2000:]
    return json.loads(run.stdout.strip().splitlines()[-1])


def _assert_legacy_positive(session: JoinedSession) -> None:
    assert session.do_help()["accepted"] is True
    assert positive(session, help_result={"accepted": True})["ok"] is True
    assert session.verify()["ok"] is True
    assert not [row for row in session.episodes()
                if row["kind"] == "B_EVENT_BINDING"]


def test_intact_new_session_has_persisted_binding_and_cold_positive(tmp_path):
    state = tmp_path / "new"
    session = JoinedSession.start(state, perform="omit")
    try:
        binding = [row for row in session.episodes()
                   if row["kind"] == "B_EVENT_BINDING"]
        assert len(binding) == 1
        assert binding[0]["body"]["b_event_contract"] == "R31J_B_EVENT_UPSTREAM@1"
        assert binding[0]["body"]["b_performer_receipt_hash"] == (
            session.meta["b_performer_receipt"]["receipt_hash"])
        assert session.do_help()["accepted"] is True
        assert session.verify()["ok"] is True
    finally:
        session.close()

    cold = JoinedSession.open(state)
    try:
        assert cold.meta["b_event_contract"] == "R31J_B_EVENT_UPSTREAM@1"
        assert cold.meta["b_performer_receipt"]
        assert cold.do_help()["accepted"] is True
        assert positive(cold, help_result={"accepted": True})["ok"] is True
        assert cold.verify()["ok"] is True
    finally:
        cold.close()

    fresh = _cold_process(state)
    assert fresh["ok"] is True
    assert fresh["verify"] is True
    assert fresh["binding_episodes"] == ["B_EVENT_BINDING"]
    assert fresh["branch_id"] == "first_session"


def test_genuine_legacy_cold_reopen_remains_positive(tmp_path):
    state = tmp_path / "legacy"
    session = _legacy_start(state)
    try:
        _assert_legacy_positive(session)
        assert "b_event_contract" not in session.meta
        assert "b_performer_receipt" not in session.meta
    finally:
        session.close()

    cold = JoinedSession.open(state)
    try:
        _assert_legacy_positive(cold)
    finally:
        cold.close()

    fresh = _cold_process(state)
    assert fresh["ok"] is True
    assert fresh["verify"] is True
    assert fresh["binding_episodes"] == []
    assert fresh["branch_id"] == "first_session"


@pytest.mark.parametrize(
    "delete",
    [
        ("b_event_contract",),
        ("b_performer_receipt",),
        ("b_event_contract", "b_performer_receipt"),
    ],
)
def test_deleting_metadata_cannot_regress_new_session_to_legacy(tmp_path, delete):
    state = tmp_path / ("cut_" + "_".join(delete))
    session = JoinedSession.start(state, perform="omit")
    session.close()
    original = _read_meta(state)

    mutated = json.loads(json.dumps(original))
    for field in delete:
        mutated.pop(field, None)
    _write_meta(state, mutated)

    with pytest.raises(SessionRefusal) as exc:
        JoinedSession.open(state)
    assert exc.value.code == "J_PROVENANCE_MISMATCH"

    fresh = _cold_process(state)
    assert fresh["ok"] is False
    assert fresh["code"] == "J_PROVENANCE_MISMATCH"

    _write_meta(state, original)
    restored = JoinedSession.open(state)
    try:
        assert restored.do_help()["accepted"] is True
        assert restored.verify()["ok"] is True
    finally:
        restored.close()


def test_binding_episode_tamper_is_typed_and_targetless_still_opens(tmp_path):
    state = tmp_path / "binding_tamper"
    session = JoinedSession.start(state, perform="omit")
    session.close()
    original = _read_meta(state)

    mutant = json.loads(json.dumps(original))
    mutant["b_performer_receipt"]["receipt_hash"] = "0" * 64
    _write_meta(state, mutant)
    with pytest.raises(SessionRefusal) as exc:
        JoinedSession.open(state)
    assert exc.value.code == "J_PROVENANCE_MISMATCH"
    _write_meta(state, original)

    from joined.refusal import RefusalSession

    refusal = RefusalSession.start(tmp_path / "refusal")
    try:
        assert refusal.meta["target_id"] == ""
        assert refusal.do_help()["accepted"] is False
        assert refusal.verify()["ok"] is True
    finally:
        refusal.close()
    cold_refusal = RefusalSession.open(tmp_path / "refusal")
    try:
        assert cold_refusal.do_help()["accepted"] is False
        assert cold_refusal.verify()["ok"] is True
    finally:
        cold_refusal.close()
