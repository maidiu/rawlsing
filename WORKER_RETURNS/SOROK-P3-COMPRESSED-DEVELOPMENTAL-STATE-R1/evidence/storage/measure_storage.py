"""Storage measurements for the P3 normalized sidecar.

This is evidence, not runtime code.  It records logical rows, SQLite bytes after
a WAL checkpoint, targeted-query row reads, O(1) head reads and one full verify
for increasing record counts.  It makes no timing guarantee.
"""
from __future__ import annotations

import json
from pathlib import Path
import sqlite3
import sys
import tempfile

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
ENGINE_ROOT = PACKAGE_ROOT.parent / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for entry in (str(PACKAGE_ROOT), str(ENGINE_ROOT)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from developmental_recursion.contracts import digest  # noqa: E402
from p3.state_store import PsycheStore  # noqa: E402


BINDING = {"root": "measure-root", "actor": "measure-actor", "branch": "measure-branch"}
REGISTRY_HASH = "measure-registry-test-only"
SOURCE_HASH = "measure-source-test-only"
GRADE = "TEST_ONLY_SOURCEFREE_STORAGE_MEASURE"
RULE = {"rule_id": "measure.rule", "rule_version": "1", "rule_hash": "measure-rule-hash"}
PLAN = {
    "root": BINDING["root"],
    "actor": BINDING["actor"],
    "branch": BINDING["branch"],
    "source_hash": SOURCE_HASH,
    "authority": "TEST_ONLY",
    "grade": GRADE,
    "permitted_rules": [dict(RULE)],
}


def state(clock: int, tag: str) -> dict:
    return {
        "root": BINDING["root"],
        "actor": BINDING["actor"],
        "branch": BINDING["branch"],
        "clock": clock,
        "state_hash": digest({"tag": tag, "clock": clock}),
    }


def event_hash(event_id: str) -> str:
    return "measure-event-hash:" + event_id


def add_record(store: PsycheStore, clock: int) -> None:
    operation_id = f"op-{clock}"
    event_id = f"event-{clock}"
    expected = state(clock - 1, "combined-before:" + operation_id)
    base_before = state(clock - 1, "base-before:" + event_id)
    store.reserve(
        operation_id,
        proposal_hash="proposal:" + operation_id,
        expected=expected,
        plan_hash=digest(PLAN),
        base_before=base_before,
        psyche_before=store.head(),
        plan=PLAN,
    )
    base = {
        "root": BINDING["root"],
        "actor": BINDING["actor"],
        "branch": BINDING["branch"],
        "event_id": event_id,
        "event_hash": event_hash(event_id),
        "clock": clock,
        "before": base_before,
        "after": state(clock, "base-after:" + event_id),
        "objective": {
            "event": {
                "e1_event_id": event_id,
                "e1_event_hash": event_hash(event_id),
            }
        },
        "receipt_ref": "P2_EVENT:" + event_hash(event_id),
    }
    store.save_world(operation_id, base)
    record = {
        "root": BINDING["root"],
        "actor": BINDING["actor"],
        "branch": BINDING["branch"],
        "project": f"project-{clock % 3}",
        "counterpart": f"counterpart-{clock % 2}",
        "record_id": f"record-{clock}",
        "kind": ("MEDIATOR", "TENSION", "PRACTICE")[clock % 3],
        "payload": {"clock": clock, "label": f"record-{clock}"},
        "rule_id": RULE["rule_id"],
        "rule_version": RULE["rule_version"],
        "rule_hash": RULE["rule_hash"],
        "registry_hash": REGISTRY_HASH,
        "source_hash": SOURCE_HASH,
        "effective_from": clock,
        "causal_parents": [event_hash(event_id)],
        "grade": GRADE,
    }
    receipt = store.commit_effects(
        operation_id,
        records=[record],
        response={"status": "MEASURE_ONLY", "clock": clock},
        event_binding={
            "root": BINDING["root"],
            "actor": BINDING["actor"],
            "branch": BINDING["branch"],
            "event_id": event_id,
            "event_hash": event_hash(event_id),
            "clock": clock,
        },
    )
    store.finish(
        operation_id,
        {
            "operation_id": operation_id,
            "proposal_hash": "proposal:" + operation_id,
            "before": expected,
            "after": state(clock, "combined-after:" + operation_id),
            "status": "REALIZED",
            "objective": {"event": {"event_id": event_id}},
            "accessible": {"event_id": event_id},
            "consequences": {"effects_receipt_hash": receipt["receipt_hash"]},
            "readset": [event_hash(event_id)],
            "receipt_ref": "MEASURE:" + operation_id,
        },
    )


def measure(store: PsycheStore, n: int) -> dict:
    store._connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    before = store.stats()
    head = store.head()
    head_after = store.stats()
    targeted_before = store.stats()
    matched = store.query(project="project-1", counterpart="counterpart-1", as_of=n)
    targeted_after = store.stats()
    full_before = store.stats()
    store.verify()
    full_after = store.stats()
    stats = store.stats()
    connection = sqlite3.connect(store.path)
    try:
        record_rows = connection.execute("SELECT COUNT(*) FROM p3_records").fetchone()[0]
        operation_rows = connection.execute("SELECT COUNT(*) FROM p3_operations").fetchone()[0]
    finally:
        connection.close()
    db_bytes = stats["db_bytes"]
    return {
        "records_requested": n,
        "record_rows": record_rows,
        "operation_rows": operation_rows,
        "head_count": head["count"],
        "head_hash": head["hash"],
        "db_bytes": db_bytes,
        "wal_bytes": stats["wal_bytes"],
        "bytes_per_record": round(db_bytes / n, 2) if n else None,
        "head_row_reads": head_after["row_reads"] - before["row_reads"],
        "targeted_query": {
            "returned": len(matched),
            "row_reads": targeted_after["row_reads"] - targeted_before["row_reads"],
            "query_count_delta": targeted_after["targeted_queries"] - targeted_before["targeted_queries"],
            "full_scans_delta": targeted_after["full_scans"] - targeted_before["full_scans"],
        },
        "full_verify_row_reads": full_after["row_reads"] - full_before["row_reads"],
        "full_scans_delta": full_after["full_scans"] - full_before["full_scans"],
    }


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="sorok-p3-storage-measure-") as directory:
        path = Path(directory) / "psyche.sqlite"
        store = PsycheStore(
            path,
            binding=BINDING,
            registry_hash=REGISTRY_HASH,
            source_hash=SOURCE_HASH,
        )
        measurements = []
        current = 0
        for target in (0, 1, 5, 10, 25, 50, 100):
            while current < target:
                current += 1
                add_record(store, current)
            measurements.append(measure(store, target))
        store.close()
    payload = {
        "schema": "SOROK_P3_STORAGE_MEASUREMENTS@1",
        "scope": "TEST_ONLY mechanical SQLite sidecar; no timing guarantee",
        "targeted_scope": {"project": "project-1", "counterpart": "counterpart-1"},
        "measurements": measurements,
    }
    output = Path(__file__).with_name("STORAGE_MEASUREMENTS.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
