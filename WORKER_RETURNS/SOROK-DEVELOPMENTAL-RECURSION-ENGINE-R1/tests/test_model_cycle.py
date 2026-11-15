"""Contract-level tests for the durable recursive batch coordinator.

The batch engine and owner here are deliberately small software fixtures. They
exercise custody, ordering and durable state; they do not encode a
psychological theory, fixed questions, actor names or workshop content.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RealizedEvent,
    RecursionRefusal,
    StateIdentity,
    detached,
    digest,
)
from developmental_recursion.model_cycle import (  # noqa: E402
    AmbiguousModelCall,
    CycleStoreError,
    RecursionCycle,
)


# ---------------------------------------------------------------------------
# Generic test owner / engine. No fixed narrative or human psychology.
# ---------------------------------------------------------------------------


class StubOwner:
    def __init__(self) -> None:
        self.root = "root:fixture"
        self.actor = "actor:fixture"
        self.branch = "branch:fixture"
        self.clock = 0
        self.state_hash = digest({"clock": 0})
        self.allowed_sources = {"source:ok"}
        self.validated: list[str] = []
        self.realized: list[str] = []
        self.mutation_count = 0

    def snapshot(self) -> StateIdentity:
        return StateIdentity(
            root=self.root,
            actor=self.actor,
            branch=self.branch,
            clock=self.clock,
            state_hash=self.state_hash,
        )

    def validate_proposal(self, proposal: EventProposal) -> None:
        self.validated.append(proposal.event_id)
        for source in proposal.source_refs:
            if source not in self.allowed_sources:
                raise RecursionRefusal(f"source not admissible: {source}")
        if isinstance(proposal.event_time, bool) or not isinstance(proposal.event_time, int):
            raise RecursionRefusal("event_time must be an integer")
        if not proposal.participants:
            raise RecursionRefusal("at least one participant is required")

    def realize(
        self, operation_id: str, proposal: EventProposal, expected: StateIdentity
    ) -> RealizedEvent:
        before = self.snapshot()
        if detached(before.document()) != detached(expected.document()):
            raise RecursionRefusal("owner identity changed before realize")
        self.clock += 1
        self.state_hash = digest(
            {"clock": self.clock, "event_id": proposal.event_id, "operation": operation_id}
        )
        self.realized.append(proposal.event_id)
        self.mutation_count += 1
        after = self.snapshot()
        return RealizedEvent(
            operation_id=operation_id,
            proposal_hash=digest(proposal.document()),
            before=before,
            after=after,
            status="REALIZED",
            objective={"fixture_event": proposal.event_id},
            accessible={"marker": f"accessible:{proposal.event_id}"},
            consequences={"fixture_status": "REALIZED"},
            readset=tuple(proposal.source_refs),
            receipt_ref=f"receipt:{operation_id}",
        )

    def mutate_outside_cycle(self) -> None:
        self.clock += 1
        self.state_hash = digest({"clock": self.clock, "outside": True})
        self.mutation_count += 1


class StubEngine:
    """Minimal BatchEngine-compatible surface for coordinator tests."""

    def __init__(self, owner: StubOwner) -> None:
        self.owner = owner
        self._history: dict[str, dict[str, Any]] = {}
        self.run_calls: list[str] = []
        self.fail_on_batch: str | None = None

    def run_batch(self, batch_id: str, proposals: list[EventProposal]) -> dict[str, Any]:
        self.run_calls.append(batch_id)
        if self.fail_on_batch == batch_id:
            raise RuntimeError("fixture engine failure")
        if batch_id in self._history:
            return detached(self._history[batch_id])
        if not isinstance(proposals, list) or not 3 <= len(proposals) <= 5:
            raise RecursionRefusal("fixture engine received an invalid proposal count")
        event_ids = [p.event_id for p in proposals]
        if len(set(event_ids)) != len(event_ids):
            raise RecursionRefusal("fixture engine received duplicate event ids")
        expected = self.owner.snapshot()
        records: list[dict[str, Any]] = []
        for proposal in proposals:
            self.owner.validate_proposal(proposal)
            realized = self.owner.realize(f"op:{batch_id}:{proposal.event_id}", proposal, expected)
            record = realized.document()
            record["event_id"] = proposal.event_id
            records.append(record)
            expected = self.owner.snapshot()
        result = {
            "batch_id": batch_id,
            "history_hash": digest(records),
            "records": records,
        }
        self._history[batch_id] = detached(result)
        return detached(result)

    def history(self, batch_id: str) -> dict[str, Any]:
        try:
            return detached(self._history[batch_id])
        except KeyError as exc:
            raise RecursionRefusal(f"fixture history missing: {batch_id}") from exc

    def verify(self) -> bool:
        return all(
            digest(result["records"]) == result["history_hash"]
            for result in self._history.values()
        )

    def tamper_history(self, batch_id: str) -> None:
        self._history[batch_id]["records"][0]["accessible"]["marker"] = "tampered"


def proposal(prefix: str, index: int, *, source: str = "source:ok",
             extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
    doc = {
        "event_id": f"{prefix}:event:{index}",
        "event_time": index,
        "operation": f"{prefix}:operation:{index}",
        "source_refs": [source],
        "participants": ["participant:fixture"],
        "circumstances": {"fixture": prefix, "ordinal": index},
        "interval": None,
    }
    if extra:
        doc.update(dict(extra))
    return doc


def proposals(prefix: str, count: int = 3, *, source: str = "source:ok",
              extra: Mapping[str, Any] | None = None) -> list[dict[str, Any]]:
    return [proposal(prefix, i, source=source, extra=extra) for i in range(1, count + 1)]


def retrospective(previous: Mapping[str, Any], *, event_ids: list[str] | None = None,
                  extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
    doc = {
        "batch_id": previous["batch_id"],
        "history_hash": previous["history_hash"],
        "event_ids": list(previous["events"][i]["event_id"] for i in range(len(previous["events"])))
        if event_ids is None else list(event_ids),
        "impressions": [
            {"proposal_id": "impression:fixture", "fixture": "not_canonical"}
        ],
    }
    if extra:
        doc.update(dict(extra))
    return doc


class StubProvider:
    def __init__(self, store_path: Path | None = None) -> None:
        self.store_path = store_path
        self.calls: list[dict[str, Any]] = []
        self.before_call = None
        self.raise_on_call: int | None = None
        self.response_extra: Mapping[str, Any] | None = None
        self.bootstrap_retrospective: Any = None
        self.bootstrap_count = 3
        self.bootstrap_proposal_extra: Mapping[str, Any] | None = None
        self.bootstrap_source = "source:ok"
        self.ordinary_retrospective_override = None
        self.ordinary_retrospective_none = False
        self.ordinary_event_ids: list[str] | None = None
        self.ordinary_count = 3
        self.ordinary_proposal_extra: Mapping[str, Any] | None = None
        self.ordinary_source = "source:ok"
        self.ordinary_proposals_override: Any = None
        self.terminal_proposals_override: Any = None

    def call(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        request_doc = detached(request)
        self.calls.append(request_doc)
        if self.before_call is not None:
            self.before_call(request_doc)
        if self.raise_on_call is not None and len(self.calls) == self.raise_on_call:
            raise RuntimeError("fixture provider exception")
        mode = request_doc["mode"]
        if mode == "BOOTSTRAP":
            if self.bootstrap_retrospective is not None:
                return {
                    "retrospective": self.bootstrap_retrospective,
                    "prospective": proposals(
                        "bootstrap", self.bootstrap_count,
                        source=self.bootstrap_source,
                        extra=self.bootstrap_proposal_extra,
                    ),
                }
            response = {
                "retrospective": None,
                "prospective": proposals(
                    "bootstrap", self.bootstrap_count,
                    source=self.bootstrap_source,
                    extra=self.bootstrap_proposal_extra,
                ),
            }
        elif mode == "ORDINARY":
            previous = request_doc["previous"]
            retro = self.ordinary_retrospective_override
            if self.ordinary_retrospective_none:
                retro = None
            elif retro is None:
                retro = retrospective(previous, event_ids=self.ordinary_event_ids)
            if self.ordinary_proposals_override is not None:
                prospective = self.ordinary_proposals_override
            else:
                prospective = proposals(
                    "ordinary", self.ordinary_count,
                    source=self.ordinary_source,
                    extra=self.ordinary_proposal_extra,
                )
            response = {"retrospective": retro, "prospective": prospective}
        elif mode == "TERMINAL":
            previous = request_doc["previous"]
            response = {
                "retrospective": retrospective(previous),
                "prospective": self.terminal_proposals_override,
            }
        else:
            raise RecursionRefusal(f"unexpected mode: {mode}")
        if self.response_extra:
            response.update(dict(self.response_extra))
        return response


def make_cycle(tmp_path: Path) -> tuple[StubOwner, StubEngine, StubProvider, RecursionCycle, Path]:
    owner = StubOwner()
    engine = StubEngine(owner)
    store = tmp_path / "cycle-store.json"
    provider = StubProvider(store)
    cycle = RecursionCycle(engine, provider, store)
    return owner, engine, provider, cycle, store


def read_store(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Happy path and boundary sequencing.
# ---------------------------------------------------------------------------


def test_full_cycle_single_provider_call_per_batch_and_terminal(tmp_path: Path) -> None:
    owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    context = {"fixture": {"nested": 1}}

    first = cycle.bootstrap(context=context)
    first_id = first["batch_id"]
    store = read_store(store_path)
    assert first_id == "batch-000001"
    assert len(first["records"]) == 3
    assert store["phase"] == "PENDING_BATCH"
    assert store["pending"]["batch_id"] == first_id
    assert store["model_call"] is None
    assert provider.calls[0]["mode"] == "BOOTSTRAP"
    assert provider.calls[0]["previous"] is None
    assert engine.run_calls == [first_id]

    second = cycle.advance(context={"fixture": {"nested": 2}})
    second_id = second["batch_id"]
    store = read_store(store_path)
    assert second_id == "batch-000002"
    assert len(second["records"]) == 3
    assert [c["mode"] for c in provider.calls] == ["BOOTSTRAP", "ORDINARY"]
    assert provider.calls[1]["previous"]["batch_id"] == first_id
    assert provider.calls[1]["previous"]["history_hash"] == first["history_hash"]
    assert [x["event_id"] for x in provider.calls[1]["previous"]["events"]] == [
        x["event_id"] for x in first["records"]
    ]
    assert all(
        set(event) == {"event_id", "accessible"}
        and "objective" not in event
        and "consequences" not in event
        for event in provider.calls[1]["previous"]["events"]
    )
    assert len(store["retrospectives"]) == 1
    assert store["retrospectives"][0]["batch_id"] == first_id
    assert store["proposed_impressions"][0]["batch_id"] == first_id
    assert store["pending"]["batch_id"] == second_id
    assert engine.run_calls == [first_id, second_id]

    final = cycle.finish(context={"fixture": {"nested": 3}})
    store = read_store(store_path)
    assert final["batch_id"] == second_id
    assert [c["mode"] for c in provider.calls] == ["BOOTSTRAP", "ORDINARY", "TERMINAL"]
    assert provider.calls[2]["previous"]["batch_id"] == second_id
    assert store["phase"] == "COMPLETE"
    assert store["pending"] is None
    assert len(store["retrospectives"]) == 2
    assert len(store["proposed_impressions"]) == 2
    assert len(engine.run_calls) == 2
    assert owner.validated  # owner performed source/order admission
    with pytest.raises(RecursionRefusal):
        cycle.advance()
    with pytest.raises(RecursionRefusal):
        cycle.finish()
    assert len(provider.calls) == 3


def test_store_reopen_resumes_pending_batch(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    first = cycle.bootstrap()
    reopened = RecursionCycle(engine, provider, store_path)
    second = reopened.advance()
    assert second["batch_id"] == "batch-000002"
    assert provider.calls[-1]["previous"]["batch_id"] == first["batch_id"]
    assert engine.run_calls == [first["batch_id"], second["batch_id"]]


# ---------------------------------------------------------------------------
# Prospective shape, exact keys and owner-admissibility.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("count", [2, 6])
def test_bootstrap_requires_three_to_five_proposals(tmp_path: Path, count: int) -> None:
    owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    provider.bootstrap_count = count
    with pytest.raises(AmbiguousModelCall):
        cycle.bootstrap()
    assert engine.run_calls == []
    assert read_store(store_path)["phase"] == "HELD"
    assert provider.calls and provider.calls[0]["mode"] == "BOOTSTRAP"


def test_prospective_extra_keys_and_invalid_source_are_held(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    provider.bootstrap_proposal_extra = {"unexpected": True}
    with pytest.raises(AmbiguousModelCall):
        cycle.bootstrap()
    assert engine.run_calls == []
    assert read_store(store_path)["phase"] == "HELD"
    assert provider.calls[0]["mode"] == "BOOTSTRAP"

    owner2, engine2, provider2, cycle2, store2 = make_cycle(tmp_path / "second")
    provider2.bootstrap_source = "source:not-admissible"
    with pytest.raises(AmbiguousModelCall):
        cycle2.bootstrap()
    assert engine2.run_calls == []
    assert read_store(store2)["phase"] == "HELD"
    assert owner2.validated == ["bootstrap:event:1"]


def test_bootstrap_rejects_fictitious_memory(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    provider.bootstrap_retrospective = {
        "batch_id": "invented",
        "history_hash": "invented",
        "event_ids": [],
        "impressions": [],
    }
    with pytest.raises(AmbiguousModelCall):
        cycle.bootstrap()
    assert engine.run_calls == []
    store = read_store(store_path)
    assert store["phase"] == "HELD"
    assert store["pending"] is None


def test_response_top_level_extra_keys_are_held(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    provider.response_extra = {"unexpected": True}
    with pytest.raises(AmbiguousModelCall):
        cycle.bootstrap()
    assert engine.run_calls == []
    assert read_store(store_path)["phase"] == "HELD"


# ---------------------------------------------------------------------------
# History binding and terminal sequencing.
# ---------------------------------------------------------------------------


def test_ordinary_requires_both_halves(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, _store_path = make_cycle(tmp_path)
    cycle.bootstrap()
    provider.ordinary_retrospective_none = True
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    assert engine.run_calls == ["batch-000001"]


def test_retrospective_event_order_is_bound(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, _store_path = make_cycle(tmp_path)
    cycle.bootstrap()
    provider.ordinary_event_ids = ["wrong:event"]
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    assert engine.run_calls == ["batch-000001"]


def test_terminal_rejects_next_batch_and_preserves_pending(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    first = cycle.bootstrap()
    provider.terminal_proposals_override = proposals("terminal", 3)
    with pytest.raises(AmbiguousModelCall):
        cycle.finish()
    store = read_store(store_path)
    assert store["phase"] == "HELD"
    assert store["pending"]["batch_id"] == first["batch_id"]
    assert len(store["retrospectives"]) == 0
    assert engine.run_calls == [first["batch_id"]]
    assert len(provider.calls) == 2


def test_history_rewrite_refused_before_provider_call(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    first = cycle.bootstrap()
    engine.tamper_history(first["batch_id"])
    calls_before = len(provider.calls)
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    store = read_store(store_path)
    assert store["phase"] == "HELD"
    assert store["pending"]["batch_id"] == first["batch_id"]
    assert len(provider.calls) == calls_before
    assert engine.run_calls == [first["batch_id"]]


def test_missing_preceding_batch_and_bootstrap_exactly_once(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    with pytest.raises(CycleStoreError):
        cycle.advance()
    with pytest.raises(CycleStoreError):
        cycle.finish()
    assert provider.calls == []
    first = cycle.bootstrap()
    calls = len(provider.calls)
    with pytest.raises(RecursionRefusal):
        cycle.bootstrap()
    assert len(provider.calls) == calls
    assert first["batch_id"] == "batch-000001"


# ---------------------------------------------------------------------------
# Owner snapshot, reservations and ambiguous custody.
# ---------------------------------------------------------------------------


def test_provider_mutation_is_held_without_engine_or_retrospective(tmp_path: Path) -> None:
    owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    cycle.bootstrap()
    provider.before_call = lambda _request: owner.mutate_outside_cycle()
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    store = read_store(store_path)
    assert store["phase"] == "HELD"
    assert store["model_call"]["status"] == "PROVIDER_MUTATED_OWNER"
    assert store["retrospectives"] == []
    assert engine.run_calls == ["batch-000001"]
    calls = len(provider.calls)
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    assert len(provider.calls) == calls


def test_provider_exception_is_ambiguous_and_not_retried(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    cycle.bootstrap()
    provider.raise_on_call = 2
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    store = read_store(store_path)
    assert store["phase"] == "HELD"
    assert store["model_call"]["status"] == "AMBIGUOUS_PROVIDER_CALL"
    assert store["retrospectives"] == []
    assert engine.run_calls == ["batch-000001"]
    calls = len(provider.calls)
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    assert len(provider.calls) == calls


def test_previous_recursion_completes_before_next_batch_even_if_next_fails(tmp_path: Path) -> None:
    _owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    first = cycle.bootstrap()
    engine.fail_on_batch = "batch-000002"
    run_batch = engine.run_batch

    def check_boundary(batch_id, proposals):
        saved = read_store(store_path)
        assert saved["retrospectives"][0]["batch_id"] == first["batch_id"]
        assert saved["model_call"]["status"] == "RETROSPECTED_PENDING_REALIZATION"
        return run_batch(batch_id, proposals)

    engine.run_batch = check_boundary
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    store = read_store(store_path)
    assert store["phase"] == "HELD"
    assert store["model_call"]["status"] == "ENGINE_ERROR"
    assert len(store["retrospectives"]) == 1
    assert store["retrospectives"][0]["batch_id"] == first["batch_id"]
    assert store["pending"]["batch_id"] == first["batch_id"]
    assert engine.run_calls == ["batch-000001", "batch-000002"]
    calls = len(provider.calls)
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    assert len(provider.calls) == calls


@pytest.mark.parametrize("change", ["root", "clock"])
def test_owner_root_or_clock_change_is_held_before_provider(tmp_path: Path, change: str) -> None:
    owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    cycle.bootstrap()
    if change == "root":
        owner.root = "root:changed"
    else:
        owner.clock = -1
    calls = len(provider.calls)
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    assert len(provider.calls) == calls
    assert engine.run_calls == ["batch-000001"]
    assert read_store(store_path)["phase"] == "HELD"


def test_reservation_is_durable_before_provider_call_and_expected_state_is_checked(tmp_path: Path) -> None:
    owner, engine, provider, cycle, store_path = make_cycle(tmp_path)
    initial_state = cycle._snapshot()
    observed: list[dict[str, Any]] = []

    def before_call(_request: Mapping[str, Any]) -> None:
        raw = read_store(store_path)
        observed.append(raw["model_call"])

    provider.before_call = before_call
    cycle.bootstrap()
    assert observed and observed[0]["status"] == "RESERVED"
    assert observed[0]["mode"] == "BOOTSTRAP"
    assert observed[0]["expected_owner_state"] == initial_state

    owner.mutate_outside_cycle()
    calls = len(provider.calls)
    with pytest.raises(AmbiguousModelCall):
        cycle.advance()
    assert len(provider.calls) == calls
    assert read_store(store_path)["phase"] == "HELD"


def test_context_is_detached_and_impressions_are_not_canonical_state(tmp_path: Path) -> None:
    owner, engine, provider, cycle, _store_path = make_cycle(tmp_path)
    context = {"fixture": {"nested": 1}}
    seen: list[dict[str, Any]] = []

    def before_call(request: Mapping[str, Any]) -> None:
        seen.append(detached(request))
        if request["context"] is not None:
            request["context"]["fixture"]["nested"] = 99

    provider.before_call = before_call
    cycle.bootstrap(context=context)
    assert context == {"fixture": {"nested": 1}}
    assert seen[0]["context"]["fixture"]["nested"] == 1
    assert owner.mutation_count == 3  # only the engine's three fixture realizes

    second = cycle.advance()
    store = read_store(_store_path)
    assert len(store["proposed_impressions"]) == 1
    assert store["proposed_impressions"][0]["impressions"] == [
        {"proposal_id": "impression:fixture", "fixture": "not_canonical"}
    ]
    assert all("impression:fixture" not in json.dumps(record, sort_keys=True) for record in second["records"])
    assert owner.mutation_count == 6
