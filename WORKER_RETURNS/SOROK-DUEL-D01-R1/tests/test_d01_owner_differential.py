"""Actual-owner changed-value differential at identical P2 event identity.

A's rule-level isolation is honest but weaker than necessary.  A same-path,
same-seed deterministic restart of the actual P2 fixture reproduces the exact
P2 event hashes; only the frozen P3 history outcome differs.  The actual
P3Owner then forms different mediator records and its later actual P3 consumer
reads exactly its own record.  This is an owner-level, same-P2-event
differential, not a hand-built rule fixture.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

D01_ROOT = Path(__file__).resolve().parents[1]
WORKER_RETURNS = D01_ROOT.parent
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (D01_ROOT, P3_ROOT, ENGINE_ROOT, P3_ROOT / "tests"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import d01_reuse  # noqa: E402
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from p3_fixture_support import (  # noqa: E402
    COUNTERPART,
    PROJECT,
    build_case,
)


def _run(path: Path, outcome: str, operation_prefix: str) -> dict:
    if path.exists():
        shutil.rmtree(path)
    case = build_case(path, history_outcomes=(outcome,))
    try:
        base_before = case.base_owner.snapshot().document()
        formation = case.owner.realize(
            operation_prefix + "-formation",
            case.proposals[0],
            case.owner.snapshot(),
        )
        read = d01_reuse.read_sourcefree_records(
            case.owner, project=PROJECT, counterpart=COUNTERPART,
            as_of=formation.after.clock,
        )
        later = d01_reuse.later_consumer(
            case.owner,
            operation_prefix + "-later",
            case.proposals[1],
            require_record_hashes=read["hashes"],
        )
        return {
            "base_before": base_before,
            "base_after": case.base_owner.snapshot().document(),
            "formation_event": formation.objective["event"]["e1_event_hash"],
            "later_event": later["response"]["event_ref"],
            "record_hashes": list(read["hashes"]),
            "record_modes": [row["payload"]["mode"] for row in read["records"]],
            "response": later["response"],
            "response_modes": [row["mode"] for row in later["response"]["streams"]],
            "readset": list(later["readset"]),
            "head": dict(case.owner.store.head()),
            "history_outcome": outcome,
        }
    finally:
        case.owner.close()


def test_actual_owner_changed_value_with_identical_p2_event_identity(
    tmp_path: Path,
) -> None:
    root = tmp_path / "same-p2-root"
    recognized = _run(root, "recognized_plan", "recognized")
    imposed = _run(root, "imposed_plan", "imposed")

    assert recognized["base_before"] == imposed["base_before"]
    assert recognized["formation_event"] == imposed["formation_event"]
    assert recognized["later_event"] == imposed["later_event"]
    assert recognized["response"]["event_ref"] == imposed["response"]["event_ref"]

    assert recognized["history_outcome"] != imposed["history_outcome"]
    assert recognized["record_modes"] == ["joint_check"]
    assert imposed["record_modes"] == ["private_check"]
    assert recognized["response_modes"] == ["joint_check"]
    assert imposed["response_modes"] == ["private_check"]
    assert recognized["record_hashes"] != imposed["record_hashes"]

    own_recognized = set(recognized["record_hashes"])
    own_imposed = set(imposed["record_hashes"])
    assert own_recognized <= set(recognized["readset"])
    assert own_imposed <= set(imposed["readset"])
    assert own_imposed.isdisjoint(recognized["readset"])
    assert own_recognized.isdisjoint(imposed["readset"])

    for branch in (recognized, imposed):
        assert branch["response"]["native_rule"] == "MISSING_RULE"
        assert branch["response"]["native_action"] == "NOT_ISSUED_BY_P3_RULE"
        assert branch["response"]["memory_formation"] == "MISSING_RULE"
        assert branch["head"]["count"] == 1
        assert all(row["native_action_performed"] is False
                   for row in branch["response"]["streams"])
