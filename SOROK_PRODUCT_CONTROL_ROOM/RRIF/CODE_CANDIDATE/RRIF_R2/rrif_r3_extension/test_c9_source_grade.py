"""RRIF-R3 sourcefree reader classification negatives.

These do not supply an actor database, authorized science or owner anchor.
They only prove that failed reader causes do not collapse into source absence.
Run with the actual R3 extension's c9c12_reader import path.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

import c9c12_consumer as consumer


@pytest.fixture
def stub_c12_path(monkeypatch):
    monkeypatch.setattr(consumer, "_c12_path", lambda root: Path("not-used.sqlite"))


@pytest.mark.parametrize(
    ("failure", "expected_status", "expected_code"),
    [
        (sqlite3.OperationalError("no such table: actor_meta"), "C9_SOURCE_MISSING", "C9_ACTOR_META_ABSENT"),
        (sqlite3.OperationalError("no such table: actor_head"), "C9_SCHEMA_READ_FAILURE", "C9_SQL_OPERATIONAL_ERROR"),
        (sqlite3.DatabaseError("database disk image is malformed"), "C9_SCHEMA_READ_FAILURE", "C9_SQL_DATABASE_ERROR"),
        (consumer.c9c12_reader.C9C12Refusal("C9_WRITER_SCHEMA_UNSUPPORTED", "BAD@1"), "C9_SOURCE_REFUSED", "C9_WRITER_SCHEMA_UNSUPPORTED"),
        (consumer.c9c12_reader.C9C12Refusal("C9_BRANCH_EPOCH_MISMATCH"), "C9_SOURCE_REFUSED", "C9_BRANCH_EPOCH_MISMATCH"),
        (consumer.c9c12_reader.C9C12Refusal("C9_SOURCE_MISSING"), "C9_SOURCE_MISSING", "C9_SOURCE_MISSING"),
    ],
)
def test_failed_reader_is_typed_without_fabricating_actor(
    stub_c12_path, monkeypatch, failure, expected_status, expected_code
):
    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(consumer.c9c12_reader, "read_actor_snapshot", fail)
    result = consumer.read_r2_c9_snapshot("any-root", actor_id="A")
    assert result["status"] == expected_status
    assert result["refusal_code"] == expected_code
    assert result["actor_id"] == "A"
    assert result["sourcefree"] is True
    assert result["consumer"] == "C9C12_R2_ACTOR_SNAPSHOT"
    assert result["status"] != "ACTOR_SNAPSHOT_OK"


def test_success_passes_actual_reader_result_without_inventing_one(stub_c12_path, monkeypatch):
    observed = {"status": "ACTOR_SNAPSHOT_OK", "actor_id": "A", "head_version_no": 0}
    monkeypatch.setattr(
        consumer.c9c12_reader, "read_actor_snapshot", lambda *args, **kwargs: dict(observed)
    )
    result = consumer.read_r2_c9_snapshot("any-root", actor_id="A")
    assert result == {**observed, "consumer": "C9C12_R2_ACTOR_SNAPSHOT"}
