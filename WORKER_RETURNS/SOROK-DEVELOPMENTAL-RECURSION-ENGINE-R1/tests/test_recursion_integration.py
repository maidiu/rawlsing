"""Integration proof over the actual accepted P2 producer and reader APIs."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from developmental_recursion.contracts import EventProposal, detached
from developmental_recursion.engine import BatchEngine
from developmental_recursion.model_cycle import RecursionCycle
from developmental_recursion.p2_owner import P2Owner, load_p2


def owner_at(root, *, reopen=False, pack=None):
    cls = load_p2()
    if reopen:
        return P2Owner(cls.open(root), **pack)
    fanin = cls.start(root)
    case = fanin.deps["case_for"](True)
    return P2Owner(fanin, case=case, source=fanin.deps["source_for"](case),
                   participants=tuple(fanin.session.read_root()["actor_ids"]))


class RecordedTransport:
    """Model transport fixture. All consequences come from the actual owner."""

    def __init__(self, source_ref, participants):
        self.source_ref = source_ref
        self.participants = participants
        self.requests = []

    def call(self, request):
        request = detached(request)
        self.requests.append(request)
        mode = request["mode"]
        previous = request["previous"]
        retrospective = None
        if previous is not None:
            retrospective = {
                "batch_id": previous["batch_id"],
                "history_hash": previous["history_hash"],
                "event_ids": [row["event_id"] for row in previous["events"]],
                "impressions": [{"status": "RENDER_PROPOSAL_ONLY",
                                 "source_history_hash": previous["history_hash"]}],
            }
        prospective = None
        if mode != "TERMINAL":
            context = request["context"]
            prospective = []
            for index in range(3):
                proposal = EventProposal(
                    "batch-" + str(context["batch"]) + "-event-" + str(index),
                    context["clock"] + 6 * (index + 1), "ADMIT_EVENT",
                    (self.source_ref,), self.participants, {},
                    {"mode": context["interval_mode"], "span": 4}
                    if index == 0 else None,
                )
                prospective.append(proposal.document())
        return {"retrospective": retrospective, "prospective": prospective}


def assert_accessible_only(request, batch):
    assert request["previous"]["events"] == [
        {"event_id": row["event_id"], "accessible": row["accessible"]}
        for row in batch["records"]
    ]
    assert request["previous"]["history_hash"] == batch["history_hash"]
    # Full source readsets and canonical identities remain in the engine journal.
    for row in request["previous"]["events"]:
        assert set(row) == {"event_id", "accessible"}
        assert "before" not in row and "after" not in row


def test_two_real_batches_retrospection_and_cold_root(tmp_path):
    state = tmp_path / "person"
    owner = owner_at(state)
    pack = {"case": owner.case, "source": owner.source,
            "participants": owner.participants}
    journal = tmp_path / "engine.sqlite"
    cycle_store = tmp_path / "cycle.sqlite"
    provider = RecordedTransport(owner.source_ref, owner.participants)
    engine = BatchEngine(owner, journal)
    cycle = RecursionCycle(engine, provider, cycle_store)
    try:
        first = cycle.bootstrap(context={"clock": owner.snapshot().clock,
                                        "batch": 1, "interval_mode": "ACTUAL"})
        assert len(first["records"]) == 3
        assert len(provider.requests) == 1  # no ordinary model call inside batch
        records = first["records"]
        assert records[1]["before"] == records[0]["after"]
        assert records[2]["before"] == records[1]["after"]
        assert records[0]["consequences"]["material_state_changed"] is True
        assert records[1]["consequences"]["immediate_response"]["objective_material_eligible"] is False
        for row in records:
            assert row["consequences"]["durable_psychological_transition"] == "MISSING_RULE"
            assert row["accessible"]["do_help_executed"] is False

        second = cycle.advance(context={"clock": owner.snapshot().clock,
                                        "batch": 2, "interval_mode": "SCHEDULED_ONLY"})
        assert len(provider.requests) == 2
        assert_accessible_only(provider.requests[1], first)
        assert second["records"][0]["before"] == first["records"][-1]["after"]
        assert len(second["records"]) == 3
        before_retrospection = owner.snapshot()
        cycle.finish()
        assert owner.snapshot() == before_retrospection
        assert [row["mode"] for row in provider.requests] == ["BOOTSTRAP", "ORDINARY", "TERMINAL"]
        assert provider.requests[0]["previous"] is None
        assert_accessible_only(provider.requests[2], second)
        assert engine.history(first["batch_id"]) == first
        assert engine.verify()
    finally:
        owner.close()

    cold = owner_at(state, reopen=True, pack=pack)
    try:
        assert cold.snapshot() == before_retrospection
        reopened = BatchEngine(cold, journal)
        assert reopened.history(first["batch_id"]) == first
        assert reopened.history(second["batch_id"]) == second
        assert reopened.verify()
    finally:
        cold.close()


def test_material_antecedent_changes_later_native_c9_result(tmp_path):
    outcomes = {}
    for mode in ("ACTUAL", "SCHEDULED_ONLY"):
        owner = owner_at(tmp_path / mode)
        try:
            engine = BatchEngine(owner, tmp_path / (mode + ".sqlite"))
            initial = owner.snapshot()
            proposals = [EventProposal(
                "event-" + str(i), initial.clock + 6 * (i + 1), "ADMIT_EVENT",
                (owner.source_ref,), owner.participants, {},
                {"mode": mode, "span": 4} if i == 0 else None,
            ) for i in range(3)]
            batch = engine.run_batch("material-comparison", proposals)
            outcomes[mode] = [r["consequences"]["immediate_response"]["objective_material_eligible"]
                              for r in batch["records"]]
            assert engine.verify()
        finally:
            owner.close()
    assert outcomes["ACTUAL"] == [False, False, False]
    assert outcomes["SCHEDULED_ONLY"] == [True, True, True]
