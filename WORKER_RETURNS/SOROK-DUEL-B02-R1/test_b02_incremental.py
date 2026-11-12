"""B02 counterstrike: incremental dated periods interleaved with a P3 owner cycle."""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
B02 = Path(__file__).resolve().parent
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3 = RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for _path in (B02, P6, ENGINE, P3):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import historical_period as hp  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    EventProposal, RecursionRefusal, digest,
)


def run_cmd(state, command, **args):
    return run_p6.experience(state, Namespace(command=command, request_id=None, **args))


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def counts(session):
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
    }


def p3_interleave_proposal(owner):
    initial_clock = int(owner.history[0]["time"]) + 4
    proposal = EventProposal(
        "vertical:event:2", initial_clock + 12, "ADMIT_EVENT",
        (owner.base_owner.source_ref,), owner.base_owner.participants, {},
        {"mode": "ACTUAL", "span": 2},
    )
    assert digest(proposal.document()) == owner.plans[1]["proposal_hash"]
    return proposal


def test_incremental_period_advance_interleaves_p3_and_employment(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        anchor = session.clock()
        hp.establish_period_plan(session)
        first = hp.materialize_to(session, "2026-01-02")
        assert first["status"] == "MATERIALIZED"
        assert first["produced_states"] == 1
        assert first["clock"] == anchor + 1
        progress = hp.period_progress(session, "period:2026-h1")
        assert progress["status"] == "PARTIAL"
        assert progress["elapsed_ticks"] == 1
        assert progress["b02_coverage"] == [[anchor, anchor + 1]]
        assert hp.p3_interval_span(session, "period:2026-h1")["span"] == 180

        proposal = p3_interleave_proposal(owner)
        result = owner.realize("b02-incremental-p3-event-2", proposal, owner.snapshot())
        assert result.status == "REALIZED"
        assert result.before.clock == anchor + 1
        assert result.after.clock == anchor + 4
        assert result.receipt_ref.startswith("P3_PSYCH:")
        assert result.consequences["durable_psychological_transition"] == "MISSING_RULE"
        assert owner.store.get_operation(
            "b02-incremental-p3-event-2")["phase"] == "COMPLETE"
        assert session.clock() == anchor + 4
        p3_records = owner.store.query(
            project=owner.plans[1]["project"],
            counterpart=owner.plans[1]["counterpart"],
            as_of=result.after.clock,
        )
        assert len(p3_records) >= 1

        progress = hp.period_progress(session, "period:2026-h1")
        assert progress["clock"] == anchor + 4
        assert progress["elapsed_ticks"] == 4
        assert progress["b02_coverage"] == [[anchor, anchor + 1]]
        assert progress["state_coverage"] == [[anchor, anchor + 3]]
        assert progress["uncovered"] == [[anchor + 3, anchor + 4]]
        assert progress["other_state_ids"]
        early_after_p3 = hp.read_material_period(session, "2026-01-02")
        assert early_after_p3["as_of_relation"] == "PAST"
        assert early_after_p3["interval_status"] == "MATERIALIZED"
        assert early_after_p3["interval_status_detail"] == "ELAPSED_BY_OTHER_OWNER"
        assert early_after_p3["interval"]["mode"] == "ACTUAL"
        assert early_after_p3["interval"]["b02_materialized"] is False
        assert early_after_p3["employment"]["term_id"] == "employment:workshop-cooperative"
        assert early_after_p3["current_employment"]["term_id"] == (
            "employment:workshop-cooperative"
        )

        second = hp.materialize_to(session, "2026-02-01")
        assert second["status"] == "MATERIALIZED"
        assert second["produced_states"] == 1
        assert second["clock"] == anchor + 31
        past_jan31 = hp.read_material_period(session, "2026-01-31")
        assert past_jan31["as_of_relation"] == "PAST"
        assert past_jan31["interval_status"] == "MATERIALIZED"
        assert past_jan31["interval_status_detail"] == "MATERIALIZED_RETROSPECTIVELY"
        assert past_jan31["retrospective"] is True
        assert past_jan31["state_available_at_as_of"] is False
        assert past_jan31["employment"]["term_id"] == "employment:workshop-cooperative"
        current_boundary = hp.read_material_period(session, "2026-02-01")
        assert current_boundary["as_of_relation"] == "CURRENT"
        assert current_boundary["interval_status"] == "NOT_MATERIALIZED"
        assert current_boundary["interval_status_detail"] == "CURRENT_NOT_MATERIALIZED"
        future_april = hp.read_material_period(session, "2026-04-01")
        assert future_april["as_of_relation"] == "FUTURE"
        assert future_april["interval_status"] == "NOT_MATERIALIZED"
        assert future_april["interval_status_detail"] == "FUTURE_NOT_MATERIALIZED"
        assert future_april["employment"]["term_id"] == "employment:civic-works"
        assert future_april["current_employment"]["term_id"] == (
            "employment:workshop-cooperative"
        )
        assert future_april["employment"] != future_april["current_employment"]

        third = hp.materialize_to(session, "2026-08-01")
        assert third["status"] == "MATERIALIZED"
        assert third["produced_states"] == 2
        assert third["clock"] == anchor + 212
        first_period = hp.period_progress(session, "period:2026-h1")
        assert first_period["status"] == "COMPLETE"
        assert first_period["elapsed_ticks"] == 181
        assert first_period["remaining_ticks"] == 0
        second_period = hp.period_progress(session, "period:2026-h2")
        assert second_period["elapsed_ticks"] == 31
        assert second_period["remaining_ticks"] == 153
        assert hp.p3_interval_span(session, "period:2026-h1")["span"] == 0
        assert hp.p3_interval_span(session, "period:2026-h2")["span"] == 153

        past_april = hp.read_material_period(session, "2026-04-01")
        assert past_april["as_of_relation"] == "PAST"
        assert past_april["interval_status"] == "MATERIALIZED"
        assert past_april["interval_status_detail"] == "MATERIALIZED_RETROSPECTIVELY"
        assert past_april["retrospective"] is True
        assert past_april["employment"]["term_id"] == "employment:civic-works"
        assert past_april["current_employment"]["term_id"] == "employment:civic-works"

        before_retry = counts(session)
        retry = hp.materialize_to(session, "2026-08-01")
        assert retry["status"] == "ALREADY_CURRENT"
        assert retry["produced_states"] == 0
        assert counts(session) == before_retry
        with pytest.raises(RecursionRefusal, match="P6_PERIOD_CLOCK_IN_PAST"):
            hp.materialize_to(session, "2026-01-15")
        with pytest.raises(RecursionRefusal, match="P6_PERIOD_OUTSIDE_PLAN"):
            hp.materialize_to(session, "2027-02-01")

        cold_counts = counts(session)
        p3_head = owner.store.head()
        plan_source = hp.read_period_plan(session)["source"]
        employment_source = hp.read_employment(session)["source"]
    finally:
        owner.close()

    script = (
        "import json, sys\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "sys.path.insert(0, sys.argv[2])\n"
        "sys.path.insert(0, sys.argv[3])\n"
        "sys.path.insert(0, sys.argv[4])\n"
        "import run_p6\n"
        "import historical_period as hp\n"
        "state = Path(sys.argv[5])\n"
        "owner = run_p6.open_owner(state / 'actual-p2')\n"
        "try:\n"
        "    session = owner.base_owner.fanin.session\n"
        "    print(json.dumps({\n"
        "        'jan31': hp.read_material_period(session, '2026-01-31'),\n"
        "        'april': hp.read_material_period(session, '2026-04-01'),\n"
        "        'first': hp.period_progress(session, 'period:2026-h1'),\n"
        "        'second': hp.period_progress(session, 'period:2026-h2'),\n"
        "        'plan': hp.read_period_plan(session),\n"
        "        'employment': hp.read_employment(session),\n"
        "        'p3_head': owner.store.head(),\n"
        "        'counts': {\n"
        "            'episodes': len(session.product.store.episodes(session.branch_id)),\n"
        "            'checkpoints': len(session.product.store.checkpoints(session.branch_id)),\n"
        "            'world_events': len(session.product.store.world_events(session.branch_id)),\n"
        "            'perceptions': len(session.product.store.perceptions(session.branch_id)),\n"
        "        },\n"
        "    }, sort_keys=True))\n"
        "finally:\n"
        "    owner.close()\n"
    )
    cold = subprocess.run(
        [sys.executable, "-B", "-c", script, str(B02), str(P6), str(ENGINE), str(P3), str(state)],
        capture_output=True, text=True, timeout=180,
    )
    assert cold.returncode == 0, cold.stdout + cold.stderr
    reopened = json.loads(cold.stdout)
    assert reopened["jan31"]["interval_status_detail"] == "MATERIALIZED_RETROSPECTIVELY"
    assert reopened["april"]["interval_status_detail"] == "MATERIALIZED_RETROSPECTIVELY"
    assert reopened["first"]["status"] == "COMPLETE"
    assert reopened["second"]["elapsed_ticks"] == 31
    assert reopened["plan"]["source"] == plan_source
    assert reopened["employment"]["source"] == employment_source
    assert reopened["p3_head"] == p3_head
    assert reopened["counts"] == cold_counts


def test_crash_after_state_before_receipt_recovers_once(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        plan = hp.read_period_plan(session)
        employment = hp.read_employment(session)
        domains = hp._period_domains(session, plan, employment)
        produced = session.produce_interval(domains[0]["domain"])
        assert produced["domain_hash"] == domains[0]["domain"]["domain_hash"]
        assert hp._receipt_rows(
            session, plan["source"], "period:2026-h1") == []
        result = hp.materialize_to(session, "2026-07-01")
        assert result["status"] == "RECOVERED"
        assert result["produced_states"] == 0
        assert result["recovered_receipts"] == 1
        assert result["clock"] == session.clock() == 429
        receipts = hp._receipt_rows(
            session, plan["source"], "period:2026-h1")
        assert len(receipts) == 1
        assert receipts[0]["status"] == "RECOVERED"
        assert receipts[0]["state_id"] == produced["state_id"]
        assert hp.period_progress(
            session, "period:2026-h1")["b02_coverage"] == [[248, 429]]
        before = counts(session)
        retry = hp.materialize_to(session, "2026-07-01")
        assert retry["status"] == "ALREADY_CURRENT"
        assert retry["recovered_receipts"] == 0
        assert len(hp._receipt_rows(
            session, plan["source"], "period:2026-h1")) == 1
        assert counts(session) == before
    finally:
        owner.close()
