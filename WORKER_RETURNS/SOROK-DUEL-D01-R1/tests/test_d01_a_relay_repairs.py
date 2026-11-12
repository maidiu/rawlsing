"""A relay counterstrike: chain-consistent record deletion must not pass verify.

B bound every surviving record row to its operation receipt.  A deletion of a
record followed by a consistent rewrite of the remaining chain and head still
left the receipt intact, and B's one-way row check accepted it.  The repair
compares the full receipt record list with the operation's rows.
"""
from __future__ import annotations

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
from developmental_recursion.contracts import RecursionRefusal, digest  # noqa: E402
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from p3 import p3_owner  # noqa: E402
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


def _delete_first_record_with_consistent_chain(path: Path, store_kwargs: dict) -> None:
    store = PsycheStore(path, **store_kwargs)
    try:
        genesis = store._genesis()
    finally:
        store.close()
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            "SELECT * FROM p3_records ORDER BY seq").fetchall()
        first, second = rows[0], rows[1]
        chain = digest({
            "previous": genesis,
            "record_id": second["record_id"],
            "record_hash": second["hash"],
        })
        connection.execute(
            "DELETE FROM p3_records WHERE record_id=?", (first["record_id"],))
        connection.execute(
            "UPDATE p3_records SET previous_chain=?, chain_hash=? "
            "WHERE record_id=?",
            (genesis, chain, second["record_id"]),
        )
        connection.execute(
            "UPDATE p3_meta SET head_hash=?, record_count=1, "
            "head_record_id=?, head_record_hash=? WHERE id=1",
            (chain, second["record_id"], second["hash"]),
        )
        connection.commit()
    finally:
        connection.close()


def test_chain_consistent_record_deletion_is_refused(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    first = case.owner.realize(
        "a-relay-formation", case.proposals[0], case.owner.snapshot())
    records = case.owner.store.query(
        project=PROJECT, counterpart=COUNTERPART, as_of=first.after.clock)
    assert len(records) == 2
    deleted_hash = records[0]["hash"]
    store_kwargs = {
        "binding": {
            "root": case.owner.snapshot().root,
            "actor": case.owner.snapshot().actor,
            "branch": case.owner.snapshot().branch,
        },
        "registry_hash": case.owner.registry["hash"],
        "source_hash": case.owner.source_hash,
    }
    case.owner.close()

    path = Path(case.state_root) / p3_owner.STORE_FILE
    _delete_first_record_with_consistent_chain(path, store_kwargs)

    raw = PsycheStore(path, **store_kwargs)
    try:
        assert raw.head()["count"] == 1
        assert raw.query(project=PROJECT, counterpart=COUNTERPART,
                         as_of=first.after.clock)[0]["hash"] != deleted_hash
        with pytest.raises(
            RecursionRefusal, match="JOURNAL_INTEGRITY:RECORD_RECEIPT_MISMATCH"):
            raw.verify()
    finally:
        raw.close()

    base = _open_base(case)
    try:
        with pytest.raises(
            RecursionRefusal, match="JOURNAL_INTEGRITY:RECORD_RECEIPT_MISMATCH"):
            d01_reuse.open_cold_owner(base, state_root=case.state_root)
    finally:
        base.close()

    base = _open_base(case)
    try:
        with pytest.raises(
            RecursionRefusal, match="JOURNAL_INTEGRITY:RECORD_RECEIPT_MISMATCH"):
            p3_owner.P3Owner(
                base, source=case.source, history=case.history,
                plans=case.plans, catalog=case.catalog,
                compression_specs=case.compression_specs,
                standpoints=case.standpoints, mode="TEST_ONLY",
            )
    finally:
        base.close()
