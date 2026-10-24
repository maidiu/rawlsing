"""Focused regressions for actual C9 row identity and S35 semantic binding."""
from __future__ import annotations

import json
import sqlite3

import pytest

from s37.bootstrap import install

install()

from candidate import seal  # noqa: E402
from s37.harness import start_session  # noqa: E402
from s37.reader import (  # noqa: E402
    S37ReadRefusal,
    _validate_s35_consistency,
)
from s37.session import S37IntegratedSession  # noqa: E402


def _tamper_row(c9_path, table, row_key, **changes):
    conn = sqlite3.connect(c9_path)
    try:
        row = conn.execute(
            f"SELECT body FROM {table} WHERE hash=?", (row_key,)
        ).fetchone()
        assert row is not None
        body = json.loads(row[0])
        body.update(changes)
        body = seal({key: value for key, value in body.items() if key != "hash"})
        conn.execute(
            f"UPDATE {table} SET body=? WHERE hash=?",
            (json.dumps(body), row_key),
        )
        conn.commit()
    finally:
        conn.close()


def _start_and_close(state):
    session = start_session(state, share=True)
    try:
        read = session.read_s36()
        return read, session._c9_path()
    finally:
        session.close()


def test_resealed_response_status_tamper_is_refused_cold(tmp_path):
    state = tmp_path / "status-tamper"
    read, c9_path = _start_and_close(state)
    _tamper_row(
        c9_path,
        "response",
        read["response_ref"],
        status="RESPONSE_EFFECTS_VALID_EMPTY",
    )
    with pytest.raises(Exception) as exc:
        S37IntegratedSession.open(state)
    assert "C9_RESPONSE_ROW_KEY_MISMATCH" in str(exc.value)


def test_resealed_receipt_body_tamper_is_refused_cold(tmp_path):
    state = tmp_path / "receipt-tamper"
    read, c9_path = _start_and_close(state)
    _tamper_row(
        c9_path,
        "receipt",
        read["c9_receipt_hash"],
        target_reason="FAKE_TARGET_REASON",
    )
    with pytest.raises(Exception) as exc:
        S37IntegratedSession.open(state)
    assert "C9_RECEIPT_ROW_KEY_MISMATCH" in str(exc.value)


def test_legitimate_c9_serialized_format_still_reads(tmp_path):
    state = tmp_path / "legitimate"
    read, c9_path = _start_and_close(state)
    conn = sqlite3.connect(c9_path)
    try:
        response_body = json.loads(
            conn.execute(
                "SELECT body FROM response WHERE hash=?", (read["response_ref"],)
            ).fetchone()[0]
        )
        receipt_body = json.loads(
            conn.execute(
                "SELECT body FROM receipt WHERE hash=?", (read["c9_receipt_hash"],)
            ).fetchone()[0]
        )
    finally:
        conn.close()
    assert "hash" not in response_body
    assert "hash" not in receipt_body
    cold = S37IntegratedSession.open(state)
    try:
        cold_read = cold.read_s36()
        assert cold_read["response_ref"] == read["response_ref"]
        assert cold_read["status"] == "OK"
        assert cold_read["outcome"] == read["outcome"]
    finally:
        cold.close()


def test_status_and_route_must_agree_with_sealed_s35_outcome(tmp_path):
    state = tmp_path / "semantic"
    session = start_session(state, share=True)
    try:
        read = session.read_s36()
    finally:
        session.close()
    s35 = dict(read["s35_receipt"])
    assert s35["outcome"] == "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
    response = dict(read["response"])
    response["status"] = "RESPONSE_EFFECTS_VALID_EMPTY"
    with pytest.raises(S37ReadRefusal) as exc:
        _validate_s35_consistency(response, s35, read)
    assert exc.value.code == "C9_RESPONSE_STATUS_OUTCOME_MISMATCH"

    response = dict(read["response"])
    response["candidate_route"] = "S35_VALID_EMPTY_UNKNOWN_RECEIVABILITY"
    with pytest.raises(S37ReadRefusal) as exc:
        _validate_s35_consistency(response, s35, read)
    assert exc.value.code == "C9_RESPONSE_ROUTE_OUTCOME_MISMATCH"
