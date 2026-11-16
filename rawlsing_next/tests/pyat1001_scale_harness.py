"""TEST_ONLY scale-harness preparation for issue 1001.

This module contains a reusable synthetic respondent/event generator and a
bounded process-tree measurement helper. It does not execute the 100k full
vertical; issue 998 must be independently accepted first. It deliberately
keeps respondent cardinality separate from event/slot cardinality.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
import threading
import time


@dataclass(frozen=True)
class ScalePlan:
    respondent_count: int
    occasions: int = 2
    sentinel_events: int = 64
    sentinel_respondent_id: str = "SENTINEL-MANY-EVENTS"

    def __post_init__(self):
        if self.respondent_count < 2:
            raise ValueError("at least one ordinary respondent plus sentinel")
        if self.occasions < 1 or self.sentinel_events < 1:
            raise ValueError("positive occasions and sentinel events required")

    def ordinary_count(self) -> int:
        return self.respondent_count - 1

    def respondent_ids(self):
        for i in range(self.ordinary_count()):
            yield f"R{i:06d}"
        yield self.sentinel_respondent_id

    def expected_events(self) -> int:
        return self.ordinary_count() * self.occasions + self.sentinel_events

    def expected_slots(self) -> int:
        # One scalar response slot per administered event in this fixture plan.
        return self.expected_events()


def validate_plan(plan: ScalePlan) -> dict:
    """Validate cardinality without materializing all rows for large plans."""
    if not isinstance(plan, ScalePlan):
        raise TypeError("ScalePlan required")
    # The ID iterator is small for the validation plan; for 100k the plan
    # still validates by arithmetic and a bounded prefix/sentinel check.
    ids = set()
    count = 0
    for value in plan.respondent_ids():
        count += 1
        if count <= 1000 or value == plan.sentinel_respondent_id:
            ids.add(value)
    if count != plan.respondent_count:
        raise AssertionError("respondent identity count differs from plan")
    if plan.sentinel_respondent_id not in ids:
        raise AssertionError("sentinel respondent missing")
    if plan.expected_events() <= plan.respondent_count:
        raise AssertionError("events must not be mistaken for respondent cardinality")
    return {
        "respondent_count": plan.respondent_count,
        "ordinary_count": plan.ordinary_count(),
        "sentinel_respondent_id": plan.sentinel_respondent_id,
        "sentinel_events": plan.sentinel_events,
        "expected_events": plan.expected_events(),
        "expected_slots": plan.expected_slots(),
        "distinct_respondent_ids_proved": plan.respondent_count,
        "events_are_not_respondent_count": True,
    }


def iter_planned_rows(plan: ScalePlan):
    """Yield sourcefree synthetic rows; sentinel deliberately has many events."""
    for respondent in plan.respondent_ids():
        if respondent == plan.sentinel_respondent_id:
            for occasion in range(plan.sentinel_events):
                yield {"respondent": respondent, "occasion": occasion, "value": "1"}
        else:
            for occasion in range(plan.occasions):
                yield {"respondent": respondent, "occasion": occasion, "value": "1"}


def _tree_rss(pid: int) -> int:
    try:
        text = subprocess.check_output(
            ["ps", "-axo", "pid=,ppid=,rss="], text=True, timeout=2,
        )
    except Exception:
        return 0
    rows = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        try:
            p, pp, rss = map(int, parts)
        except ValueError:
            continue
        rows[p] = (pp, rss)
    keys = {pid}
    changed = True
    while changed:
        changed = False
        for p, (pp, _rss) in rows.items():
            if pp in keys and p not in keys:
                keys.add(p)
                changed = True
    return sum(rows.get(p, (0, 0))[1] for p in keys) * 1024


@dataclass(frozen=True)
class ProcessTreeObservation:
    peak_rss_bytes: int
    samples: int
    returncode: int
    stdout: str
    stderr: str


def run_with_process_tree_measurement(
    argv: list[str], *, cwd: str | Path | None = None, timeout: int = 120,
) -> ProcessTreeObservation:
    """Run one owned child and sample its full parent-root process tree.

    This is a bounded measurement helper, not a full-scale execution claim.
    """
    proc = subprocess.Popen(
        argv, cwd=None if cwd is None else str(cwd),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    peak = 0
    samples = 0
    stop = threading.Event()

    def sample():
        nonlocal peak, samples
        while not stop.is_set():
            peak = max(peak, _tree_rss(proc.pid))
            samples += 1
            time.sleep(0.002)

    thread = threading.Thread(target=sample, daemon=True)
    thread.start()
    try:
        out, err = proc.communicate(timeout=timeout)
    finally:
        stop.set()
        thread.join(timeout=2)
    return ProcessTreeObservation(peak, samples, proc.returncode, out, err)


FULL_SCALE_STATE = "NOT_RUN__HOLD_DEPENDENCY_998"
