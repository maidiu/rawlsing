"""RRIF R2 focused C12 preimage tamper/restore and independent verifier test."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from joined.session import JoinedSession
from r30a.first_session import SessionRefusal


def _episode_rows(db_path: Path):
    db = sqlite3.connect(str(db_path))
    try:
        return list(db.execute(
            "SELECT branch_id,seq,body FROM episode ORDER BY branch_id,seq"))
    finally:
        db.close()


def _rewrite_body(db_path: Path, branch_id: str, seq: int, body: str) -> None:
    db = sqlite3.connect(str(db_path))
    try:
        # Model a raw-DB attacker: the append-only trigger is not a real
        # security boundary when the process can write the file directly.
        db.execute("DROP TRIGGER IF EXISTS episode_no_update")
        db.execute("UPDATE episode SET body=? WHERE branch_id=? AND seq=?",
                   (body, branch_id, seq))
        db.commit()
    finally:
        db.close()


def test_c12_episode_preimage_tamper_is_detected_and_restores(tmp_path):
    state = tmp_path / "c12"
    session = JoinedSession.start(state, perform="omit")
    product_root = session.product.root
    session.close()

    db_path = product_root / "c12.sqlite"
    rows = _episode_rows(db_path)
    assert rows
    branch_id, seq, original = rows[0]
    parsed = json.loads(original)
    parsed["body"]["tampered_for_rrif_proof"] = True
    tampered = json.dumps(parsed, sort_keys=True, separators=(",", ":"))
    assert tampered != original

    _rewrite_body(db_path, branch_id, seq, tampered)
    with pytest.raises(SessionRefusal) as exc:
        JoinedSession.open(state)
    assert exc.value.code in {"ROOT_C12_VERIFY_FAILED", "BRANCH_C12_VERIFY_FAILED", "C12_VERIFY_FAILED"}
    assert "body_hash_mismatch" in str(exc.value) or "C12" in str(exc.value)

    _rewrite_body(db_path, branch_id, seq, original)
    restored = JoinedSession.open(state)
    try:
        assert restored.verify()["ok"] is True
        assert restored.product.c12_verify("root")["ok"] is True
    finally:
        restored.close()


def test_independent_c12_verifier_rejects_forged_episode_hash(tmp_path):
    state = tmp_path / "forged"
    session = JoinedSession.start(state, perform="omit")
    product_root = session.product.root
    session.close()

    from bp2p4.c12_verify import verify_branch_chain
    db_path = product_root / "c12.sqlite"
    rows = _episode_rows(db_path)
    branch_id, seq, original = rows[0]
    parsed = json.loads(original)
    parsed["body"]["forged_episode_source"] = "authors-claim"
    forged = json.dumps(parsed, sort_keys=True, separators=(",", ":"))
    _rewrite_body(db_path, branch_id, seq, forged)

    store = session.product.store
    # Re-open the qualified store directly for the independent verifier.
    from r26e.c12_integrity import QualifiedC12Store
    independent = QualifiedC12Store(db_path)
    try:
        result = independent.verify(branch_id)
        assert result["ok"] is False
        assert any("body_hash_mismatch" in e for e in result["errors"])
        # The reconciliation-side verifier sees the same broken chain.
        assert verify_branch_chain(independent, branch_id)["ok"] is False
    finally:
        independent.close()
