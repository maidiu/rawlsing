"""Repaired JOIN-E C12 fork: equal counts must not mask substituted perceptions.

Bounded SOURCEFREE cross-version negative, NOT native person/actor grant.
This deliberately does not modify the original writer-era fork oracle.
"""
from __future__ import annotations
import os
from pathlib import Path
import pytest

from actor_reader import load_candidate, load_c12_source, ReaderHeld


def test_repaired_c12_fork_equal_count_substitution_refuses(tmp_path):
    writer_root = os.environ.get("C9_READER_SOURCE")
    c12_root = os.environ.get("C12_READER_SOURCE")
    if not writer_root or not c12_root:
        pytest.fail("SOURCE_CLOSURE_ENV_MISSING__NO_TEST_SKIP")
    candidate = load_candidate(Path(writer_root))  # SHA256 pins exact B writer.
    c12 = load_c12_source(Path(c12_root))  # Four exact later C12 source pins.
    store_class = c12["qualified"]
    grade = c12["store"].GRADE
    seal = c12["canon"].seal
    db = tmp_path / "repaired-fork.sqlite"
    store = store_class(db)

    def event(branch: str, name: str, clock: int) -> dict:
        return seal({
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": branch,
            "event_id": name, "clock": clock, "body": {},
            "grade": grade, "native": False,
        })

    try:
        store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
        for name in ("ev1", "ev2"):
            store.append_world_event("root", event("root", name, 10))
        store.record_perception("root", actor_id="A", event_id="ev1", clock=10, channel="direct")
        store.record_perception("root", actor_id="A", event_id="ev2", clock=11, channel="direct")
        parent_pre = candidate.c12_fork_guard(db, "root")
        assert parent_pre["state"] == "FORK_HELD"
        assert parent_pre["code"] == "C12_PERCEPTION_ONLY_SUFFIX"
        assert parent_pre["base_perception_count"] == 2
        # New repaired C12 legitimately forks the verified perception suffix at 11,
        # unlike the historical 7bf2 writer-era fork at world-only clock 10.
        store.fork("root", "child")
        assert store.verify("child")["ok"] is True
        assert len(store.perceptions("child")) == 2

        # Different post-fork actual events on parent and child, same resulting
        # number of perceptions. Counts alone can no longer prove identity.
        store.append_world_event("root", event("root", "parent-later", 12))
        store.record_perception("root", actor_id="A", event_id="parent-later",
                                clock=12, channel="own")
        store.append_world_event("child", event("child", "child-later", 12))
        store.record_perception("child", actor_id="A", event_id="child-later",
                                clock=12, channel="own")
        assert store.verify("root")["ok"] is True
        assert store.verify("child")["ok"] is True
        assert len(store.perceptions("root")) == 3
        assert len(store.perceptions("child")) == 3
        assert store.perceptions("root") != store.perceptions("child")

        # The existing C9 writer guard must reject a same-count different
        # *source-visible* cut by identity, not by exception or count mismatch.
        child = candidate.c12_fork_guard(
            db, "child",
            expected_base_perception_hash=parent_pre["base_perception_hash"],
        )
        assert child["state"] == "FORK_HELD"
        assert child["code"] == "C12_BASE_PERCEPTION_IDENTITY_MISMATCH"
        assert child["base_perception_count"] == 3
        assert child["base_perception_hash"] != parent_pre["base_perception_hash"]
    finally:
        store.close()
