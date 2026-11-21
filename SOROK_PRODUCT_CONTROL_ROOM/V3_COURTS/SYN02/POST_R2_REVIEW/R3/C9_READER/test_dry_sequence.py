from copy import deepcopy
from dataclasses import FrozenInstanceError
import pytest
from actor_reader import ReaderHeld
from dry_sequence import parse_proposals, run_dry_sequence, run_world_sequence


def proposals(count=3):
    return [{"proposal_id": str(i), "conditioning_ref": "actor-snapshot-ref",
             "source_ref": "world-source-request-not-occurrence", "interval_start": 10 + i,
             "interval_end": 11 + i} for i in range(count)]


@pytest.mark.parametrize("count", [3, 4, 5])
def test_complete_dry_runs_are_conditional_with_no_actual_events_or_calls(count):
    rows = proposals(count)
    before = deepcopy(rows)
    result = run_dry_sequence(rows, first_half_status="ADMITTED")
    assert result.status == "DRY_RUN"
    assert len(result.proposals) == count
    assert all(row.status == "CONDITIONAL_NOT_OCCURRED" for row in result.proposals)
    assert result.actual_events == () and result.world_calls == result.model_calls == 0
    assert result.partial_policy == "UNSELECTED"
    assert rows == before
    with pytest.raises(FrozenInstanceError):
        result.status = "COMMITTED"


@pytest.mark.parametrize("count", [0, 1, 2, 6])
def test_incomplete_or_oversized_batches_refuse_without_fallback(count):
    with pytest.raises(ReaderHeld, match="BATCH_PROPOSAL_COUNT_HELD"):
        run_dry_sequence(proposals(count), first_half_status="ADMITTED")


def test_duplicate_and_premerged_delta_fields_refuse():
    rows = proposals()
    rows[1]["proposal_id"] = rows[0]["proposal_id"]
    with pytest.raises(ReaderHeld, match="DUPLICATE_PROPOSAL_HELD"):
        parse_proposals(rows)
    rows = proposals()
    rows[0]["capacity_delta"] = 50
    with pytest.raises(ReaderHeld, match="PROPOSAL_SHAPE_HELD"):
        parse_proposals(rows)


def test_missing_independent_source_does_not_create_phantom_prefix_or_suffix():
    rows = proposals(5)
    rows[2]["source_ref"] = ""
    with pytest.raises(ReaderHeld, match="PROPOSAL_SOURCE_OR_CONDITIONING_HELD"):
        run_dry_sequence(rows, first_half_status="ADMITTED")
    # Nothing committed before refusal: there is no effect-capable port here.
    assert len(rows) == 5


def test_denied_half_one_holds_every_implicit_half_two_dependency():
    result = run_dry_sequence(proposals(5), first_half_status="DENIED")
    assert result.status == "HELD"
    assert len(result.proposals) == 5
    assert all(row.status == "HELD_SCI05_FIRST_HALF" for row in result.proposals)
    assert result.actual_events == ()


def test_real_world_request_remains_held_before_callback_or_policy_selection():
    calls = []
    result = run_world_sequence(proposals(), world=lambda: calls.append("WORLD"), partial_policy="PREFIX")
    assert result.status == "HELD_WORLD_PERFORMANCE_UNAUTHORIZED"
    assert result.partial_policy == "UNSELECTED"
    assert calls == [] and result.actual_events == ()


def test_actual_interval_qualifiers_are_required_not_synthesized():
    rows = proposals()
    rows[1]["interval_end"] = rows[1]["interval_start"]
    with pytest.raises(ReaderHeld, match="PROPOSAL_INTERVAL_HELD"):
        parse_proposals(rows)
