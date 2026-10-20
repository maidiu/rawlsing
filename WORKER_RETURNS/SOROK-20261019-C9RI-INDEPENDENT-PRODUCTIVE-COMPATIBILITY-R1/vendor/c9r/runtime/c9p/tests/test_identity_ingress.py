"""(a) Actor identity, activation and standing-state ingress tests."""
from __future__ import annotations

from conftest import ACTOR_ID, build_actor_record
from candidate.canon import seal
from candidate.identity import (
    ACTOR_RECORD_SCHEMA,
    IngressReason,
    IngressStatus,
    ingress_actor,
)


def test_admitted_actor_binds_exact_source_readset() -> None:
    record = build_actor_record()
    result = ingress_actor(record, as_of=20)
    assert result.status is IngressStatus.ADMITTED
    assert result.reason is IngressReason.OK
    assert result.actor_id == ACTOR_ID
    assert result.readset_refs == (record["source_ref"],)
    assert result.record_hash == record["hash"]


def test_inactive_actor_is_refused() -> None:
    record = build_actor_record(activation_status="INACTIVE")
    result = ingress_actor(record, as_of=20)
    assert result.status is IngressStatus.REFUSED
    assert result.reason is IngressReason.ACTOR_NOT_ACTIVE
    assert result.actor_id == ""


def test_stale_standing_state_is_refused() -> None:
    record = build_actor_record(currentness_as_of=25)
    result = ingress_actor(record, as_of=20)
    assert result.status is IngressStatus.REFUSED
    assert result.reason is IngressReason.STANDING_STATE_STALE


def test_psychology_claim_at_ingress_is_refused() -> None:
    record = build_actor_record()
    record = seal(dict(record, beliefs=["trusts_counterpart"]))
    result = ingress_actor(record, as_of=20)
    assert result.status is IngressStatus.REFUSED
    assert result.reason is IngressReason.ACTOR_PSYCHOLOGY_CLAIM_AT_INGRESS


def test_unsealed_record_is_refused() -> None:
    record = dict(build_actor_record())
    record["hash"] = "0" * 64
    result = ingress_actor(record, as_of=20)
    assert result.status is IngressStatus.REFUSED
    assert result.reason is IngressReason.RECORD_INTEGRITY_FAILURE


def test_missing_source_ref_is_refused() -> None:
    record = seal(
        {
            "schema": ACTOR_RECORD_SCHEMA,
            "actor_id": ACTOR_ID,
            "activation_status": "ACTIVE",
            "standing_state": "STANDING_CURRENT",
            "currentness_as_of": 10,
            "source_ref": "",
            "source_hash": "abc",
        }
    )
    result = ingress_actor(record, as_of=20)
    assert result.status is IngressStatus.REFUSED
    assert result.reason is IngressReason.SOURCE_REF_MISSING


def test_schema_mismatch_is_refused() -> None:
    record = seal({"schema": "OTHER_SCHEMA@9", "actor_id": ACTOR_ID})
    result = ingress_actor(record, as_of=20)
    assert result.status is IngressStatus.REFUSED
    assert result.reason is IngressReason.SCHEMA_MISMATCH
