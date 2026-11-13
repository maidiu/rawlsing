"""Issue 1001 harness preparation: cardinality and full-scale hold only.

No 100k execution is performed. The test proves the generator's 1,000 distinct
respondent identities and many-occurrence sentinel are not event/slot counts,
and that a 100,000 distinct-respondent plan is accepted without materializing
the full vertical.
"""
from __future__ import annotations

import pytest

from rawlsing_next.tests.pyat1001_scale_harness import (
    FULL_SCALE_STATE,
    ScalePlan,
    iter_planned_rows,
    validate_plan,
)


def test_1000_distinct_respondents_and_many_occurrence_sentinel():
    plan = ScalePlan(respondent_count=1000, occasions=2, sentinel_events=257)
    result = validate_plan(plan)
    assert result["respondent_count"] == 1000
    assert result["distinct_respondent_ids_proved"] == 1000
    assert result["sentinel_events"] == 257
    assert result["expected_events"] == 999 * 2 + 257
    assert result["expected_events"] > result["respondent_count"]
    rows = list(iter_planned_rows(plan))
    assert len(rows) == result["expected_events"]
    assert len({row["respondent"] for row in rows}) == 1000
    assert sum(
        1 for row in rows if row["respondent"] == plan.sentinel_respondent_id
    ) == 257


def test_100000_distinct_plan_is_prepared_without_full_execution():
    plan = ScalePlan(respondent_count=100000, occasions=3, sentinel_events=1000)
    result = validate_plan(plan)
    assert result["respondent_count"] == 100000
    assert result["expected_events"] > result["respondent_count"]
    assert FULL_SCALE_STATE == "NOT_RUN__HOLD_DEPENDENCY_998"
    assert "NOT_RUN" in FULL_SCALE_STATE
