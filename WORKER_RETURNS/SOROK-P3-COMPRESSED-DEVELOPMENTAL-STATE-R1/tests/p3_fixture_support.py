"""Actual-P2 fixture support for the P3 vertical proof harness.

This module is TEST_ONLY model transport/test construction. It does not
implement a state store, owner, rule, projection or event engine. The durable
normalized store is imported only by the banked P3Owner; when absent, the
harness is not executed.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT.parent / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
PROJECTION_ROOT = ROOT.parent / "SOROK-S45-S47-PROJECTION-20261105-R1"
for _path in (ROOT, ENGINE_ROOT, PROJECTION_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RecursionRefusal,
    StateIdentity,
    canonical,
    detached,
    digest,
)
from developmental_recursion.engine import BatchEngine  # noqa: E402
from developmental_recursion.model_cycle import RecursionCycle  # noqa: E402
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from p3 import compression, p3_owner, projections, test_rules  # noqa: E402

STORE_MISSING = "DEPENDENT_EXECUTION_NOT_RUN_MISSING_RETURNED_STATE_STORE"
PROJECT = "vertical:project"
COUNTERPART = "vertical:counterpart"
HISTORY_OUTCOMES = ("recognized_plan", "imposed_plan")


def seal(body: Mapping[str, Any]) -> dict:
    return dict(detached(body), hash=digest(body))


def source_document(identity: Mapping[str, Any], *, source_ref: str) -> dict:
    body = {
        "grade": test_rules.GRADE,
        "root": identity["root"],
        "actor": identity["actor"],
        "branch": identity["branch"],
        "source_ref": source_ref,
        "base_source_ref": source_ref,
        "purpose": "P3 vertical actual-P2 sourcefree proof",
    }
    return body


def history_rows(identity: Mapping[str, Any], source_hash: str,
                 outcomes: tuple[str, ...] = HISTORY_OUTCOMES) -> list[dict]:
    rows: list[dict] = []
    for index, outcome in enumerate(outcomes):
        row = {key: identity[key] for key in ("root", "actor", "branch")}
        row.update(
            grade=test_rules.GRADE,
            source_hash=source_hash,
            episode_id=f"vertical:history:{index}",
            project=PROJECT,
            counterpart=COUNTERPART,
            time=int(identity["clock"]) - 4 + index,
            activity="compare_plans_in_task",
            outcome=outcome,
            parent_refs=[rows[-1]["hash"]] if rows else [],
        )
        rows.append(seal(row))
    return rows


def proposal(event_id: str, event_time: int, *, interval: Mapping[str, Any] | None = None) -> EventProposal:
    return EventProposal(
        event_id=event_id,
        event_time=event_time,
        operation="ADMIT_EVENT",
        source_refs=("P2_INPUT_PLACEHOLDER",),
        participants=("actor", "counterpart"),
        circumstances={},
        interval=interval,
    )


def plan_for(identity: Mapping[str, Any], proposal_doc: Mapping[str, Any],
             source_hash: str, phase: str, *, counterpart: str = COUNTERPART,
             project: str = PROJECT, role: str = "peer") -> dict:
    registry = test_rules.make_registry(source_hash)
    body = {key: identity[key] for key in ("root", "actor", "branch")}
    body.update(
        grade=test_rules.GRADE,
        source_hash=source_hash,
        registry_hash=registry["hash"],
        proposal_hash=digest(proposal_doc),
        event_id=proposal_doc["event_id"],
        permitted_rules=test_rules.rule_descriptors(),
        phase=phase,
        project=project,
        counterpart=counterpart,
        activation_roles=[role],
        relation_refs=["vertical:relation"],
        obligation_refs=[],
        interlocutor_role=role,
    )
    return seal(body)


def standpoint(identity: Mapping[str, Any], source_hash: str, *, role: str,
               permissions: list[str], interlocutor_ref: str,
               suffix: str) -> dict:
    body = {key: identity[key] for key in ("root", "actor", "branch", "clock")}
    body.update(
        interlocutor_ref=interlocutor_ref,
        role=role,
        permissions=list(permissions),
        source_refs=[source_hash],
        grade=test_rules.GRADE,
        label=f"vertical:standpoint:{suffix}",
    )
    return seal(body)


def _source_catalog(identity: Mapping[str, Any], event_times: Mapping[str, int]) -> dict:
    clock = int(identity["clock"])
    docs = {
        "vertical:participation": {
            "kind": "ACTOR_PARTICIPATION", "from_clock": clock - 20, "to_clock": clock - 1,
            "data": {"scope": "actual sourcefree participation source"},
        },
        "vertical:recurrence": {
            "kind": "RECURRING_RELATION", "from_clock": clock - 20, "to_clock": clock - 1,
            "data": {"scope": "separately sourced recurring relation"},
        },
        "vertical:material": {
            "kind": "MATERIAL_RELATION", "from_clock": clock - 20, "to_clock": clock - 1,
            "data": {"scope": "material relation source"},
        },
        "vertical:bounded": {
            "kind": "BOUNDED_INTERVAL",
            "from_clock": event_times["formed"] - 6,
            "to_clock": event_times["formed"] - 2,
            "data": {"scope": "bounded actual interval evidence"},
        },
        "vertical:historical": {
            "kind": "HISTORICAL_SOURCE", "from_clock": clock - 30, "to_clock": clock - 20,
            "data": {"scope": "fixed historical source"},
        },
    }
    result = {}
    for ref, body in docs.items():
        result[ref] = seal({
            "grade": "SOURCEFREE_TEST_ONLY",
            "root": identity["root"],
            "actor": identity["actor"],
            "branch": identity["branch"],
            **body,
        })
    return result


def _compression_specs(identity: Mapping[str, Any], proposals: list[Mapping[str, Any]],
                       catalog: Mapping[str, Mapping[str, Any]]) -> dict:
    event_times = {"formed": proposals[0]["event_time"]}
    clock = int(identity["clock"])
    # The four declared forms are exercised by the first four actual events.
    return {
        proposals[0]["event_id"]: {
            "envelope_id": "vertical:singular",
            "proposal_hash": digest(proposals[0]),
            "representation_form": "SINGULAR_OCCURRENCE",
            "represented_window": {"from_clock": clock, "to_clock": proposals[0]["event_time"],
                                   "coverage_basis": "actual-participation"},
            "recurrence_basis_refs": [],
            "participation_refs": ["vertical:participation"],
            "material_relation_refs": ["vertical:material"],
            "observed": ["current actual event"], "unobserved": ["unrepresented history"],
            "selection_basis": "vertical proof singular event",
        },
        proposals[1]["event_id"]: {
            "envelope_id": "vertical:representative",
            "proposal_hash": digest(proposals[1]),
            "representation_form": "REPRESENTATIVE_EPISODE",
            "represented_window": {"from_clock": clock - 20, "to_clock": clock - 1,
                                   "coverage_basis": "recurring-relation"},
            "recurrence_basis_refs": ["vertical:recurrence"],
            "participation_refs": ["vertical:participation"],
            "material_relation_refs": ["vertical:material"],
            "observed": ["representative actual event"], "unobserved": ["other episodes"],
            "selection_basis": "vertical proof representative episode",
        },
        proposals[2]["event_id"]: {
            "envelope_id": "vertical:accumulated",
            "proposal_hash": digest(proposals[2]),
            "representation_form": "ACCUMULATED_INTERVAL",
            "represented_window": {"from_clock": proposals[0]["event_time"] - 6,
                                   "to_clock": proposals[0]["event_time"] - 2,
                                   "coverage_basis": "bounded-interval"},
            "recurrence_basis_refs": ["vertical:bounded"],
            "participation_refs": ["vertical:participation"],
            "material_relation_refs": ["vertical:material"],
            "observed": ["bounded actual interval"], "unobserved": ["outside interval"],
            "selection_basis": "vertical proof accumulated interval",
        },
        proposals[3]["event_id"]: {
            "envelope_id": "vertical:retrospective",
            "proposal_hash": digest(proposals[3]),
            "representation_form": "RETROSPECTIVE_CRYSTALLIZATION",
            "represented_window": {"from_clock": clock - 30, "to_clock": clock - 20,
                                   "coverage_basis": "fixed-history"},
            "recurrence_basis_refs": ["vertical:historical"],
            "participation_refs": ["vertical:participation"],
            "material_relation_refs": ["vertical:material"],
            "observed": ["later actual trigger"], "unobserved": ["analyst-only history"],
            "selection_basis": "vertical proof retrospective crystallization",
        },
    }


@dataclass
class VerticalCase:
    base_owner: Any
    owner: Any
    initial: StateIdentity
    source_hash: str
    source: Mapping[str, Any]
    history: list[dict]
    proposals: list[EventProposal]
    plans: list[dict]
    catalog: Mapping[str, Any]
    compression_specs: Mapping[str, Any]
    standpoints: list[dict]
    provider: "ScriptedProvider"
    cycle: Any
    journal_path: Path
    cycle_store_path: Path


class ScriptedProvider:
    """TEST_ONLY CallProvider transport; all state effects are owner-computed."""

    def __init__(self, proposals: list[EventProposal]) -> None:
        if len(proposals) != 6:
            raise ValueError("vertical proof requires two three-event batches")
        self.batches = [proposals[:3], proposals[3:]]
        self.calls: list[dict] = []
        self.context_bytes = 0
        self._batch_index = 0

    @staticmethod
    def _retrospective(previous: Mapping[str, Any]) -> dict:
        return {
            "batch_id": previous["batch_id"],
            "history_hash": previous["history_hash"],
            "event_ids": [row["event_id"] for row in previous["events"]],
            "impressions": [{"fixture": "TEST_ONLY_PROVIDER", "not_canonical_report": True}],
        }

    def call(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        request = detached(request)
        self.calls.append(request)
        self.context_bytes += len(canonical(request).encode("utf-8"))
        mode = request["mode"]
        if mode == "BOOTSTRAP":
            if self._batch_index != 0:
                raise RecursionRefusal("TEST_ONLY_PROVIDER_BOOTSTRAP_ORDER")
            self._batch_index = 1
            return {"retrospective": None,
                    "prospective": [p.document() for p in self.batches[0]]}
        previous = request["previous"]
        if mode == "ORDINARY":
            if self._batch_index != 1:
                raise RecursionRefusal("TEST_ONLY_PROVIDER_ORDINARY_ORDER")
            self._batch_index = 2
            return {"retrospective": self._retrospective(previous),
                    "prospective": [p.document() for p in self.batches[1]]}
        if mode == "TERMINAL":
            if self._batch_index != 2:
                raise RecursionRefusal("TEST_ONLY_PROVIDER_TERMINAL_ORDER")
            self._batch_index = 3
            return {"retrospective": self._retrospective(previous),
                    "prospective": None}
        raise RecursionRefusal("TEST_ONLY_PROVIDER_MODE")


def build_case(tmp_path: Path, *, history_outcomes: tuple[str, ...] = HISTORY_OUTCOMES,
               interval_modes: Mapping[int, str] | None = None,
               include_compression: bool = True,
               standpoints: bool = True) -> VerticalCase:
    """Construct actual P2 and banked P3 owners; the store must be returned."""
    fanin = load_p2().start(tmp_path / "actual-p2")
    case = fanin.deps["case_for"](True)
    base = P2Owner(
        fanin, case=case, source=fanin.deps["source_for"](case),
        participants=tuple(fanin.session.read_root()["actor_ids"]),
    )
    try:
        initial = base.snapshot()
        source = source_document(initial.document(), source_ref=base.source_ref)
        source_hash = digest(source)
        history = history_rows(initial.document(), source_hash, history_outcomes)
        modes = {0: "ACTUAL", 1: "ACTUAL", 2: "ACTUAL", 3: "ACTUAL",
                 4: "ACTUAL", 5: "ACTUAL"}
        if interval_modes:
            modes.update(interval_modes)
        event_ids = [f"vertical:event:{index}" for index in range(1, 7)]
        proposals = []
        for index, event_id in enumerate(event_ids):
            interval = None
            if index == 2:
                interval = {"mode": modes[index], "span": 4}
            if index == 1:
                interval = {"mode": modes[index], "span": 2}
            proposals.append(EventProposal(
                event_id=event_id,
                event_time=initial.clock + 6 * (index + 1),
                operation="ADMIT_EVENT",
                source_refs=(base.source_ref,),
                participants=base.participants,
                circumstances={},
                interval=interval,
            ))
        phases = ["FORMATION", "RECRUIT", "STABILITY", "RECRUIT", "STABILITY", "STABILITY"]
        plans = [
            plan_for(initial.document(), proposals[index].document(), source_hash,
                     phases[index])
            for index in range(6)
        ]
        event_times = {"formed": proposals[0].event_time}
        catalog = _source_catalog(initial.document(), event_times) if include_compression else {}
        specs = (_compression_specs(initial.document(), [p.document() for p in proposals],
                                    catalog) if include_compression else {})
        stand = []
        if standpoints:
            stand = [
                standpoint(initial.document(), source_hash, role="peer",
                           permissions=["OBSERVE_PUBLIC_ACTION", "READ_PUBLIC_DIALOGUE"],
                           interlocutor_ref="vertical:trusted-peer", suffix="trusted"),
                standpoint(initial.document(), source_hash, role="official",
                           permissions=["READ_PUBLIC_DIALOGUE"],
                           interlocutor_ref="vertical:official", suffix="official"),
            ]
        owner = p3_owner.P3Owner(
            base, source=source, history=history, plans=plans, catalog=catalog,
            compression_specs=specs, standpoints=stand, mode="TEST_ONLY",
        )
        provider = ScriptedProvider(proposals)
        journal = tmp_path / "vertical-journal.sqlite"
        cycle_store = tmp_path / "vertical-cycle.json"
        engine = BatchEngine(owner, journal)
        cycle = RecursionCycle(engine, provider, cycle_store)
        return VerticalCase(
            base_owner=base, owner=owner, initial=initial, source_hash=source_hash,
            source=source, history=history, proposals=proposals, plans=plans,
            catalog=catalog, compression_specs=specs, standpoints=stand,
            provider=provider, cycle=cycle, journal_path=journal,
            cycle_store_path=cycle_store,
        )
    except BaseException:
        base.close()
        raise


def reopen_owner(case: VerticalCase):
    """Reopen the exact actual P2 root and the banked P3 owner."""
    fanin = load_p2().open(Path(case.base_owner.fanin.session.state_root))
    actual_case = fanin.deps["case_for"](True)
    base = P2Owner(
        fanin, case=actual_case, source=fanin.deps["source_for"](actual_case),
        participants=tuple(fanin.session.read_root()["actor_ids"]),
    )
    owner = p3_owner.P3Owner(
        base, source=case.source, history=case.history, plans=case.plans,
        catalog=case.catalog, compression_specs=case.compression_specs,
        standpoints=case.standpoints, mode="TEST_ONLY",
    )
    return base, owner


def run_chain(case: VerticalCase) -> dict:
    first = case.cycle.bootstrap(context={"fixture": "vertical-bootstrap"})
    second = case.cycle.advance(context={"fixture": "vertical-ordinary"})
    final = case.cycle.finish(context={"fixture": "vertical-terminal"})
    return {"bootstrap": first, "ordinary": second, "terminal": final}


def workflow_records(owner: Any, max_clock: int) -> list[dict]:
    return owner.store.query(project=PROJECT, counterpart=COUNTERPART, as_of=max_clock)


def batch_events(result: Mapping[str, Any]) -> list[dict]:
    return list(result.get("records") or [])


def cpu_latency(fn: Any) -> tuple[Any, float]:
    import time
    started = time.perf_counter()
    value = fn()
    return value, time.perf_counter() - started


def file_metrics(paths: list[Path]) -> dict:
    return {
        str(path): ({
            "bytes": path.stat().st_size,
        } if path.exists() else {"bytes": 0})
        for path in paths
    }


def measure_case(case: VerticalCase, results: Mapping[str, Any]) -> dict:
    pr = case.provider
    files = [case.journal_path, case.cycle_store_path,
             Path(case.base_owner.fanin.session.state_root) / "recursion_owner.sqlite",
             Path(case.base_owner.fanin.session.state_root) / "p3_psyche.sqlite3",
             Path(case.base_owner.fanin.session.state_root) / "p3_owner_config.json"]
    for base in list(files):
        for suffix in ("-wal", "-shm"):
            files.append(Path(str(base) + suffix))
    head = case.owner.store.head()
    return {
        "schema": "SOROK_P3_VERTICAL_METRICS@1",
        "provider_calls": len(pr.calls),
        "provider_modes": [row["mode"] for row in pr.calls],
        "provider_context_bytes": pr.context_bytes,
        "p3_record_head": detached(head),
        "file_bytes": file_metrics(files),
        "logical_cycle_store_bytes": (case.cycle_store_path.stat().st_size
                                       if case.cycle_store_path.exists() else 0),
        "retrospective_count": len(json.loads(
            case.cycle_store_path.read_text(encoding="utf-8")
        ).get("retrospectives", [])) if case.cycle_store_path.exists() else 0,
        "batch_counts": [len(batch_events(results["bootstrap"])),
                         len(batch_events(results["ordinary"]))],
        "source_config_bytes": len(canonical(case.owner.config).encode("utf-8")),
        "b1_historical_comparison": {
            "label": "E1 B1 measured historical 3-event baseline; not this runtime",
            "note": "E1 reported 94,208 DB bytes, 98,304 journal bytes and 15,220 state bytes for 3 events; not used as a current guarantee.",
        },
    }
