"""B repairs over A's D01 retention boundary.

1. A cold open must verify the durable record chain, not only each row hash and
   the head pointer: a rewritten non-head record otherwise survives and is
   consumed by the later actual P3 consumer.
2. A missing owner config over a nonempty store is recoverable only when the
   durable last-completed operation proves the exact candidate config.  The
   normal P3Owner guard and the cold loader still refuse unproven regeneration.
3. The same provenance anchor now lives in P3Owner itself, so a direct owner
   reopen cannot accept a substituted config merely because it bypasses the
   D01 loader.  A verified recovery can still preserve a pending operation for
   P3Owner's own crash-recovery path.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import pytest

D01_ROOT = Path(__file__).resolve().parents[1]
WORKER_RETURNS = D01_ROOT.parent
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (D01_ROOT, P3_ROOT, ENGINE_ROOT, P3_ROOT / "tests"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import d01_reuse  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    RecursionRefusal,
    detached,
    digest,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from p3 import p3_owner, test_rules  # noqa: E402
from p3.state_store import PsycheStore  # noqa: E402
from p3_fixture_support import (  # noqa: E402
    COUNTERPART,
    PROJECT,
    build_case,
)


def _open_base(case):
    fanin = load_p2().open(Path(case.state_root))
    try:
        actual = fanin.deps["case_for"](True)
        return P2Owner(
            fanin,
            case=actual,
            source=fanin.deps["source_for"](actual),
            participants=tuple(fanin.session.read_root()["actor_ids"]),
        )
    except BaseException:
        fanin.close()
        raise


def _cold_open(case):
    base = _open_base(case)
    try:
        owner = d01_reuse.open_cold_owner(base, state_root=case.state_root)
    except BaseException:
        base.close()
        raise
    return base, owner


def _read(case, clock):
    return d01_reuse.read_sourcefree_records(
        case.owner, project=PROJECT, counterpart=COUNTERPART, as_of=clock,
    )


def _config_document(case) -> dict:
    path = Path(case.state_root) / p3_owner.CONFIG_FILE
    return json.loads(path.read_text(encoding="utf-8"))


def _store_kwargs(case) -> dict:
    return {
        "binding": {"root": case.owner.snapshot().root,
                    "actor": case.owner.snapshot().actor,
                    "branch": case.owner.snapshot().branch},
        "registry_hash": case.owner.registry["hash"],
        "source_hash": case.owner.source_hash,
    }


def _tamper_first_record(path: Path) -> str:
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            "SELECT * FROM p3_records ORDER BY seq").fetchall()
        first_row = rows[0]
        record = json.loads(first_row["record_json"])
        old_mode = record["payload"]["mode"]
        record["payload"]["mode"] = (
            "private_check" if old_mode == "joint_check" else "joint_check")
        body = {key: value for key, value in record.items() if key != "hash"}
        record["hash"] = digest(body)
        connection.execute(
            "UPDATE p3_records SET payload_json=?, record_json=?, hash=? "
            "WHERE record_id=?",
            (
                json.dumps(record["payload"], sort_keys=True,
                           separators=(",", ":")),
                json.dumps(record, sort_keys=True, separators=(",", ":")),
                record["hash"],
                record["record_id"],
            ),
        )
        connection.commit()
        return old_mode
    finally:
        connection.close()


def test_cold_open_refuses_rewritten_nonhead_record(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    first = case.owner.realize(
        "tamper-formation", case.proposals[0], case.owner.snapshot())
    read = _read(case, first.after.clock)
    assert len(read["hashes"]) == 2
    head_before = dict(case.owner.store.head())
    store_kwargs = _store_kwargs(case)
    case.owner.close()

    path = Path(case.state_root) / p3_owner.STORE_FILE
    old_mode = _tamper_first_record(path)

    raw = PsycheStore(path, **store_kwargs)
    try:
        assert raw.head() == head_before
        tampered = raw.query(project=PROJECT, counterpart=COUNTERPART,
                             as_of=first.after.clock)
        assert tampered[0]["payload"]["mode"] != old_mode
    finally:
        raw.close()

    base = _open_base(case)
    try:
        with pytest.raises(RecursionRefusal,
                           match="JOURNAL_INTEGRITY:RECORD_CHAIN"):
            d01_reuse.open_cold_owner(base, state_root=case.state_root)
    finally:
        base.close()

    verify = PsycheStore(path, **store_kwargs)
    try:
        with pytest.raises(RecursionRefusal,
                           match="JOURNAL_INTEGRITY:RECORD_CHAIN"):
            verify.verify()
    finally:
        verify.close()


def _tamper_first_record_with_consistent_chain(path: Path) -> None:
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            "SELECT * FROM p3_records ORDER BY seq").fetchall()
        first, second = rows[0], rows[1]
        record = json.loads(first["record_json"])
        record["payload"]["mode"] = (
            "private_check" if record["payload"]["mode"] == "joint_check"
            else "joint_check")
        body = {key: value for key, value in record.items() if key != "hash"}
        record["hash"] = digest(body)
        first_chain = digest({
            "previous": first["previous_chain"],
            "record_id": record["record_id"],
            "record_hash": record["hash"],
        })
        connection.execute(
            "UPDATE p3_records SET payload_json=?, record_json=?, hash=?, "
            "chain_hash=? WHERE record_id=?",
            (
                json.dumps(record["payload"], sort_keys=True,
                           separators=(",", ":")),
                json.dumps(record, sort_keys=True, separators=(",", ":")),
                record["hash"],
                first_chain,
                record["record_id"],
            ),
        )
        second_chain = digest({
            "previous": first_chain,
            "record_id": second["record_id"],
            "record_hash": second["hash"],
        })
        connection.execute(
            "UPDATE p3_records SET previous_chain=?, chain_hash=? "
            "WHERE record_id=?",
            (first_chain, second_chain, second["record_id"]),
        )
        connection.execute(
            "UPDATE p3_meta SET head_hash=? WHERE id=1",
            (second_chain,),
        )
        connection.commit()
    finally:
        connection.close()


def test_cold_open_refuses_chain_consistent_record_receipt_divergence(
    tmp_path: Path,
) -> None:
    case = build_case(tmp_path)
    first = case.owner.realize(
        "receipt-formation", case.proposals[0], case.owner.snapshot())
    read = _read(case, first.after.clock)
    store_kwargs = _store_kwargs(case)
    case.owner.close()

    path = Path(case.state_root) / p3_owner.STORE_FILE
    _tamper_first_record_with_consistent_chain(path)
    raw = PsycheStore(path, **store_kwargs)
    try:
        with pytest.raises(RecursionRefusal,
                           match="JOURNAL_INTEGRITY:RECORD_RECEIPT_MISMATCH"):
            raw.verify()
    finally:
        raw.close()

    base = _open_base(case)
    try:
        with pytest.raises(RecursionRefusal,
                           match="JOURNAL_INTEGRITY:RECORD_RECEIPT_MISMATCH"):
            d01_reuse.open_cold_owner(base, state_root=case.state_root)
    finally:
        base.close()


def test_live_owner_terminal_consumer_refuses_record_chain_tamper(
    tmp_path: Path,
) -> None:
    case = build_case(tmp_path)
    try:
        first = case.owner.realize(
            "live-tamper-formation", case.proposals[0], case.owner.snapshot())
        read = _read(case, first.after.clock)
        head_before = dict(case.owner.store.head())
        _tamper_first_record(Path(case.state_root) / p3_owner.STORE_FILE)
        with pytest.raises(RecursionRefusal,
                           match="JOURNAL_INTEGRITY:RECORD_CHAIN"):
            d01_reuse.later_consumer(
                case.owner, "live-tamper-later", case.proposals[1],
                require_record_hashes=read["hashes"],
            )
        with pytest.raises(RecursionRefusal,
                           match="JOURNAL_INTEGRITY:RECORD_CHAIN"):
            d01_reuse.read_sourcefree_records(
                case.owner, project=PROJECT, counterpart=COUNTERPART,
                as_of=first.after.clock,
            )
        assert case.owner.store.head() == head_before
        assert case.owner.store.get_operation("live-tamper-later") is None
    finally:
        case.owner.close()


def test_recovery_accepts_only_durable_provenance_and_restores_exact_bytes(
    tmp_path: Path,
) -> None:
    case = build_case(tmp_path)
    first = case.owner.realize(
        "recovery-formation", case.proposals[0], case.owner.snapshot())
    read = _read(case, first.after.clock)
    config_path = Path(case.state_root) / p3_owner.CONFIG_FILE
    original = config_path.read_bytes()
    document = _config_document(case)
    head_before = dict(case.owner.store.head())
    case.owner.close()

    config_path.unlink()
    with pytest.raises(RecursionRefusal, match="D01_COLD_CONFIG_MISSING"):
        _cold_open(case)

    tampered = json.loads(json.dumps(document))
    plan = tampered["config"]["plans"][1]
    plan["counterpart"] = "attacker-counterpart"
    plan["hash"] = digest({key: value for key, value in plan.items()
                           if key != "hash"})
    tampered["config_hash"] = digest(tampered["config"])
    with pytest.raises(RecursionRefusal,
                       match="D01_RECOVERY_PROVENANCE_MISMATCH"):
        d01_reuse.recover_missing_config(case.state_root, tampered)
    assert not config_path.exists()

    receipt = d01_reuse.recover_missing_config(case.state_root, document)
    assert receipt["mode"] == "VERIFIED_COMPLETED_ANCHOR"
    assert receipt["config_hash"] == document["config_hash"]
    assert receipt["store_head"] == head_before
    assert config_path.read_bytes() == original

    base, cold = _cold_open(case)
    try:
        assert cold.store.head() == head_before
        reread = d01_reuse.read_sourcefree_records(
            cold, project=PROJECT, counterpart=COUNTERPART,
            as_of=first.after.clock,
        )
        assert reread["hashes"] == read["hashes"]
        later = d01_reuse.later_consumer(
            cold, "recovery-later", case.proposals[1],
            require_record_hashes=read["hashes"],
        )
        assert set(later["record_hashes"]) == set(read["hashes"])
    finally:
        cold.close()

    document = _config_document(case)
    plan = document["config"]["plans"][0]
    plan["phase"] = "RECRUIT"
    plan["hash"] = digest({key: value for key, value in plan.items()
                           if key != "hash"})
    document["config_hash"] = digest(document["config"])
    config_path.write_text(json.dumps(document), encoding="utf-8")
    base = _open_base(case)
    try:
        with pytest.raises(RecursionRefusal,
                           match="P3_CONFIG_PROVENANCE_MISMATCH"):
            p3_owner.P3Owner(
                base,
                source=document["config"]["source"],
                history=document["config"]["history"],
                plans=document["config"]["plans"],
                catalog=document["config"]["catalog"],
                compression_specs=document["config"]["compression_specs"],
                standpoints=document["config"]["standpoints"],
                mode="TEST_ONLY",
            )
    finally:
        base.close()


def test_exact_response_refuses_unknown_affirmative_claim_key() -> None:
    with pytest.raises(RecursionRefusal, match="D01_RESPONSE_SCHEMA_KEYS"):
        d01_reuse.validate_sourcefree_response({
            "status": "COMPUTED_TEST_ONLY_RESPONSE",
            "native_rule": "MISSING_RULE",
            "native_action": "NOT_ISSUED_BY_P3_RULE",
            "memory_formation": "MISSING_RULE",
            "first_person_claims": [],
            "can_008": "ACQUIRED",
        }, exact=True)
    with pytest.raises(RecursionRefusal, match="D01_RESPONSE_STREAM_KEYS"):
        d01_reuse.validate_sourcefree_response({
            "status": "COMPUTED_TEST_ONLY_RESPONSE",
            "native_rule": "MISSING_RULE",
            "native_action": "NOT_ISSUED_BY_P3_RULE",
            "memory_formation": "MISSING_RULE",
            "first_person_claims": [],
            "streams": [{
                "mode": "joint_check",
                "candidate_activity": "joint_check:vertical:counterpart",
                "material_eligible": True,
                "native_action_performed": False,
                "native_memory": "I remember the plan.",
            }],
            "rule": {"rule_id": "r", "rule_version": "1", "rule_hash": "0" * 64},
            "contradictions": [],
            "event_ref": "0" * 64,
            "grade": d01_reuse.GRADE,
            "hash": "0" * 64,
        }, exact=True)


def test_record_read_refuses_severed_rule_source_cleanly(
    tmp_path: Path, monkeypatch,
) -> None:
    case = build_case(tmp_path)
    first = case.owner.realize(
        "source-formation", case.proposals[0], case.owner.snapshot())
    read = _read(case, first.after.clock)
    missing = Path(tmp_path) / "missing-bfirst.py"
    with monkeypatch.context() as scoped:
        scoped.setattr(test_rules, "B1_PATH", missing)
        with pytest.raises(RecursionRefusal,
                           match="P3_B1_SOURCE_SEVERED"):
            d01_reuse.read_sourcefree_records(
                case.owner, project=PROJECT, counterpart=COUNTERPART,
                as_of=first.after.clock,
            )
    restored = d01_reuse.read_sourcefree_records(
        case.owner, project=PROJECT, counterpart=COUNTERPART,
        as_of=first.after.clock,
    )
    assert restored["hashes"] == read["hashes"]
    case.owner.close()


def test_recovery_empty_store_is_unambiguous(tmp_path: Path) -> None:
    case = build_case(tmp_path / "empty")
    document = _config_document(case)
    original = (Path(case.state_root) / p3_owner.CONFIG_FILE).read_bytes()
    case.owner.close()
    (Path(case.state_root) / p3_owner.CONFIG_FILE).unlink()

    receipt = d01_reuse.recover_missing_config(case.state_root, document)
    assert receipt["mode"] == "EMPTY_STORE"
    assert receipt["last_completed_operation_id"] is None
    assert receipt["store_head"]["count"] == 0
    assert (Path(case.state_root) / p3_owner.CONFIG_FILE).read_bytes() == original

    base, cold = _cold_open(case)
    try:
        first = cold.realize(
            "empty-recovery-formation", case.proposals[0], cold.snapshot())
        read = d01_reuse.read_sourcefree_records(
            cold, project=PROJECT, counterpart=COUNTERPART,
            as_of=first.after.clock,
        )
        assert read["head"]["count"] == 2
    finally:
        cold.close()


def test_recovery_preserves_verified_pending_operation(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    first = case.owner.realize(
        "pending-formation", case.proposals[0], case.owner.snapshot())
    read = _read(case, first.after.clock)
    plan = case.plans[1]
    case.owner.store.reserve(
        "pending-later",
        proposal_hash=digest(case.proposals[1].document()),
        expected=case.owner.snapshot().document(),
        plan_hash=plan["hash"],
        base_before=case.base_owner.snapshot().document(),
        psyche_before=case.owner.store.head(),
        plan=plan,
    )
    document = _config_document(case)
    head_before = dict(case.owner.store.head())
    assert case.owner.store.pending()[0]["operation_id"] == "pending-later"
    case.owner.close()
    (Path(case.state_root) / p3_owner.CONFIG_FILE).unlink()

    receipt = d01_reuse.recover_missing_config(case.state_root, document)
    assert receipt["mode"] == "VERIFIED_COMPLETED_ANCHOR"
    assert receipt["pending_operation_ids"] == ["pending-later"]
    assert receipt["last_completed_operation_id"] is not None

    base = _open_base(case)
    owner = None
    try:
        with pytest.raises(RecursionRefusal,
                           match="D01_COLD_OPERATION_PENDING"):
            d01_reuse.open_cold_owner(base, state_root=case.state_root)
        config = d01_reuse.load_cold_config(case.state_root)
        owner = p3_owner.P3Owner(
            base,
            source=config["source"],
            history=config["history"],
            plans=config["plans"],
            catalog=config["catalog"],
            compression_specs=config["compression_specs"],
            standpoints=config["standpoints"],
            mode="TEST_ONLY",
        )
        recovered = owner.realize(
            "pending-later", case.proposals[1], owner.snapshot())
        assert recovered.consequences["durable_psychological_transition"] == (
            "MISSING_RULE")
        assert owner.store.get_operation("pending-later")["phase"] == "COMPLETE"
        assert owner.store.head() == head_before
        record_hashes = [
            stream["record_hash"] for stream
            in recovered.consequences["test_only_psychological"]["streams"]
            if stream.get("record_hash")
        ]
        assert set(record_hashes) == set(read["hashes"])
    finally:
        if owner is not None:
            owner.close()
        else:
            base.close()
