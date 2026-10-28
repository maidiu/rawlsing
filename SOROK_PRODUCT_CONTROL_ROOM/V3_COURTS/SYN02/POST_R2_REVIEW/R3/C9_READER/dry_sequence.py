"""F3 sourcefree conditional proposal shell; never performs a world event.

No LLM, world callback, storage port, stochastic policy or partial-commit choice
is available in this dry-run boundary. Proposal refs are technical, not memory.
"""
from dataclasses import dataclass
import json
from actor_reader import ReaderHeld, gate_second_half


@dataclass(frozen=True)
class ProspectiveSpecV1:
    proposal_id: str
    conditioning_ref: str
    source_ref: str
    interval_start: int
    interval_end: int


@dataclass(frozen=True)
class DryProposalOutcomeV1:
    proposal: ProspectiveSpecV1
    status: str
    reason: str


@dataclass(frozen=True)
class EventSequenceShellV1:
    status: str
    proposals: tuple[DryProposalOutcomeV1, ...]
    actual_events: tuple = ()
    world_calls: int = 0
    model_calls: int = 0
    partial_policy: str = "UNSELECTED"
    grade: str = "SOURCEFREE_DRY_RUN_NOT_WORLD_ADMISSION"


def parse_proposals(rows: list[dict]) -> tuple[ProspectiveSpecV1, ...]:
    """Parse literal proposal fields; deltas, narrator effects and unknown keys refuse."""
    if not isinstance(rows, list) or not 3 <= len(rows) <= 5:
        raise ReaderHeld("BATCH_PROPOSAL_COUNT_HELD")
    expected = {"proposal_id", "conditioning_ref", "source_ref", "interval_start", "interval_end"}
    parsed = []
    identifiers = set()
    previous_start = None
    for row in rows:
        if not isinstance(row, dict) or set(row) != expected:
            raise ReaderHeld("PROPOSAL_SHAPE_HELD")
        if any(type(row[key]) is not str or not row[key] for key in ("proposal_id", "conditioning_ref", "source_ref")):
            raise ReaderHeld("PROPOSAL_SOURCE_OR_CONDITIONING_HELD")
        if row["proposal_id"] in identifiers:
            raise ReaderHeld("DUPLICATE_PROPOSAL_HELD")
        identifiers.add(row["proposal_id"])
        start, end = row["interval_start"], row["interval_end"]
        if type(start) is not int or type(end) is not int or end <= start or (previous_start is not None and start < previous_start):
            raise ReaderHeld("PROPOSAL_INTERVAL_HELD")
        previous_start = start
        parsed.append(ProspectiveSpecV1(**row))
    return tuple(parsed)


def run_dry_sequence(rows: list[dict], *, first_half_status: str) -> EventSequenceShellV1:
    proposals = parse_proposals(rows)
    gating = gate_second_half(first_half_status, proposals)
    outcomes = tuple(DryProposalOutcomeV1(proposal, "CONDITIONAL_NOT_OCCURRED" if state == "PROPOSED_ONLY" else state,
        "SOURCE_REF_IS_NOT_OCCURRED_EVENT" if state == "PROPOSED_ONLY" else "FIRST_HALF_NOT_ADMITTED_NO_INDEPENDENCE_INFERRED")
        for proposal, state in zip(proposals, gating))
    status = "DRY_RUN" if first_half_status == "ADMITTED" else "HELD"
    return EventSequenceShellV1(status, outcomes)


def run_world_sequence(*args, **kwargs) -> EventSequenceShellV1:
    """No argument, callback or claimed policy can enable original world authority."""
    return EventSequenceShellV1("HELD_WORLD_PERFORMANCE_UNAUTHORIZED", ())


if __name__ == "__main__":
    import argparse
    from dataclasses import asdict
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposals", type=Path)
    parser.add_argument("--first-half-status", required=True)
    options = parser.parse_args()
    try:
        rows = json.loads(options.proposals.read_text())
        result = run_dry_sequence(rows, first_half_status=options.first_half_status)
        print(json.dumps(asdict(result), indent=2))
    except (ReaderHeld, ValueError, OSError):
        raise SystemExit("DRY_SEQUENCE_HELD")
