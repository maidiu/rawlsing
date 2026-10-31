"""Durable source-free historical projection ledger.

This ledger is not C9 and not a canonical actor store. It records only the
source facts consumed by the historical adapter and the adapter's material
accounting. It never writes to the I1/C12 database.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from v3.core.state import BackboneState
from v3.io.json_codec import state_from_dict, state_to_dict

from .contracts import (
    ActorAccess,
    ActorResponse,
    ActorWorldEvent,
    ClockDomain,
    EventDisposition,
    MaterialDelta,
    Provenance,
    SourceActorSnapshot,
    Status,
    StepOutcome,
    YearRecord,
)
from .provenance import canonical_state_hash, digest, record_to_dict
from .quarantine import restore_unset_after_codec


LEDGER_SCHEMA = "SOROK_V3CORE_R1_HISTORICAL_PROJECTION@1"


class LedgerRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _provenance_from_dict(value: dict[str, Any]) -> Provenance:
    return Provenance(
        source_system=str(value["source_system"]),
        source_ref=str(value["source_ref"]),
        source_commit=str(value["source_commit"]),
        source_branch=str(value["source_branch"]),
        source_path=str(value["source_path"]),
        source_sha256=str(value["source_sha256"]),
        source_record_id=str(value["source_record_id"]),
        captured_by=str(value["captured_by"]),
        captured_at=str(value["captured_at"]),
        native=bool(value.get("native", False)),
        authority=str(value.get("authority", "TEST_ONLY_SOURCEFREE")),
    )


def _snapshot_from_dict(value: dict[str, Any]) -> SourceActorSnapshot:
    return SourceActorSnapshot(
        actor_id=str(value["actor_id"]),
        world_id=str(value["world_id"]),
        source_clock_domain=ClockDomain(value["source_clock_domain"]),
        source_clock=int(value["source_clock"]),
        position=str(value["position"]),
        cash=float(value["cash"]),
        material_remaining=float(value["material_remaining"]),
        free_hours=float(value["free_hours"]),
        completed_units=float(value["completed_units"]),
        skill=float(value["skill"]),
        debt_units=float(value["debt_units"]),
        tools_remaining=float(value["tools_remaining"]),
        projects=tuple(str(x) for x in value.get("projects", [])),
        provenance=_provenance_from_dict(value["provenance"]),
    )


def _event_from_dict(value: dict[str, Any]) -> ActorWorldEvent:
    return ActorWorldEvent(
        event_id=str(value["event_id"]),
        actor_id=str(value["actor_id"]),
        world_id=str(value["world_id"]),
        kind=str(value["kind"]),
        location=str(value["location"]),
        source_clock_domain=ClockDomain(value["source_clock_domain"]),
        source_clock=int(value["source_clock"]),
        body=dict(value.get("body") or {}),
        provenance=_provenance_from_dict(value["provenance"]),
        owner_receipt_hash=value.get("owner_receipt_hash"),
        source_owned=bool(value.get("source_owned", False)),
    )


def _access_from_dict(value: dict[str, Any]) -> ActorAccess:
    return ActorAccess(
        event_id=str(value["event_id"]),
        actor_id=str(value["actor_id"]),
        channel=str(value["channel"]),
        perceived=bool(value["perceived"]),
        source_clock_domain=ClockDomain(value["source_clock_domain"]),
        source_clock=int(value["source_clock"]),
        provenance=_provenance_from_dict(value["provenance"]),
    )


def _response_from_dict(value: dict[str, Any]) -> ActorResponse:
    return ActorResponse(
        event_id=str(value["event_id"]),
        actor_id=str(value["actor_id"]),
        kind=str(value["kind"]),
        performed=bool(value["performed"]),
        body=dict(value.get("body") or {}),
        source_clock_domain=ClockDomain(value["source_clock_domain"]),
        source_clock=int(value["source_clock"]),
        provenance=_provenance_from_dict(value["provenance"]),
    )


def _year_from_dict(value: dict[str, Any]) -> YearRecord:
    deltas = tuple(
        MaterialDelta(
            event_id=str(item["event_id"]),
            field=str(item["field"]),
            before=float(item["before"]),
            delta=float(item["delta"]),
            after=float(item["after"]),
            source_fact_hash=str(item["source_fact_hash"]),
            authority=str(item.get("authority", "TEST_ONLY_MATERIAL_ACCOUNTING_POLICY")),
        )
        for item in value.get("material_deltas", [])
    )
    steps = tuple(
        StepOutcome(
            step_id=str(item["step_id"]),
            status=Status(item["status"]),
            rule_id=str(item.get("rule_id", "")),
            details=dict(item.get("details") or {}),
        )
        for item in value.get("step_outcomes", [])
    )
    dispositions = tuple(
        EventDisposition(
            event_id=str(item["event_id"]),
            status=Status(item["status"]),
            reason=str(item["reason"]),
            rule_id=str(item.get("rule_id", "")),
            source_fact_hash=str(item.get("source_fact_hash", "")),
            durable_mutation=bool(item.get("durable_mutation", False)),
            details=dict(item.get("details") or {}),
        )
        for item in value.get("event_dispositions", [])
    )
    return YearRecord(
        schema=str(value["schema"]),
        annual_year=int(value["annual_year"]),
        age=None if value.get("age") is None else int(value["age"]),
        schedule_clock_domain=ClockDomain(value["schedule_clock_domain"]),
        source_event_ids=tuple(str(x) for x in value.get("source_event_ids", [])),
        state_before_hash=str(value["state_before_hash"]),
        state_after_hash=str(value["state_after_hash"]),
        derived_diagnostic_hash=str(value["derived_diagnostic_hash"]),
        published_material_index_before=float(value["published_material_index_before"]),
        published_material_index_after=float(value["published_material_index_after"]),
        material_deltas=deltas,
        step_outcomes=steps,
        event_dispositions=dispositions,
        generation_status=str(value["generation_status"]),
        readiness=str(value["readiness"]),
        authority=str(value.get("authority", "TEST_ONLY_SOURCEFREE_NO_SCIENCE_ISSUANCE")),
        canonical_c9_claimed=bool(value.get("canonical_c9_claimed", False)),
    )


@dataclass
class HistoricalProjection:
    """Durable source-free material projection over actual source events."""

    projection_id: str
    actor_id: str
    world_id: str
    state: BackboneState
    prior_snapshot: SourceActorSnapshot
    years: list[YearRecord] = field(default_factory=list)
    source_events: dict[str, ActorWorldEvent] = field(default_factory=dict)
    accesses: dict[tuple[str, str], ActorAccess] = field(default_factory=dict)
    responses: dict[tuple[str, str], ActorResponse] = field(default_factory=dict)
    material_facts: dict[str, Any] = field(default_factory=dict)
    source_metadata: dict[str, Any] = field(default_factory=dict)
    applied_event_ids: list[str] = field(default_factory=list)
    authority: str = "TEST_ONLY_SOURCEFREE_NO_SCIENCE_ISSUANCE"
    canonical_c9_claimed: bool = False
    rival_store_created: bool = False

    def state_hash(self) -> str:
        return canonical_state_hash(self.state)

    def is_applied(self, event_id: str) -> bool:
        return event_id in self.applied_event_ids

    def add_source(
        self,
        event: ActorWorldEvent,
        access: ActorAccess,
        response: ActorResponse,
    ) -> None:
        self.source_events[event.event_id] = event
        self.accesses[(event.event_id, access.actor_id)] = access
        self.responses[(event.event_id, response.actor_id)] = response

    def append_year(self, record: YearRecord) -> None:
        self.years.append(record)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema": LEDGER_SCHEMA,
            "projection_id": self.projection_id,
            "actor_id": self.actor_id,
            "world_id": self.world_id,
            "authority": self.authority,
            "native": False,
            "canonical_c9_claimed": self.canonical_c9_claimed,
            "rival_store_created": self.rival_store_created,
            "state": state_to_dict(self.state),
            "state_hash": self.state_hash(),
            "prior_snapshot": record_to_dict(self.prior_snapshot),
            "source_events": [record_to_dict(v) for v in self.source_events.values()],
            "accesses": [record_to_dict(v) for v in self.accesses.values()],
            "responses": [record_to_dict(v) for v in self.responses.values()],
            "material_facts": dict(self.material_facts),
            "source_metadata": dict(self.source_metadata),
            "applied_event_ids": list(self.applied_event_ids),
            "years": [record_to_dict(r) for r in self.years],
        }
        payload["ledger_hash"] = digest(payload)
        return payload

    def save(self, path: str | Path, *, replace=None) -> str:
        """Write the ledger atomically. A failed replace leaves the old file intact."""
        replace = replace or os.replace
        path = Path(path)
        payload = self.to_dict()
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(path.name + ".tmp")
        try:
            temp.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            replace(temp, path)
        except Exception:
            if temp.exists():
                temp.unlink()
            raise
        return payload["ledger_hash"]

    @classmethod
    def load(cls, path: str | Path) -> "HistoricalProjection":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload.get("schema") != LEDGER_SCHEMA:
            raise LedgerRefusal("LEDGER_SCHEMA_UNSUPPORTED", str(payload.get("schema")))
        recorded_hash = payload.pop("ledger_hash", "")
        if digest(payload) != recorded_hash:
            raise LedgerRefusal("LEDGER_HASH_MISMATCH")
        if payload.get("canonical_c9_claimed") is not False:
            raise LedgerRefusal("LEDGER_CLAIMS_CANONICAL_C9")
        if payload.get("rival_store_created") is not False:
            raise LedgerRefusal("LEDGER_CLAIMS_RIVAL_STORE")
        state = state_from_dict(payload["state"])
        restore_unset_after_codec(state)
        projection = cls(
            projection_id=str(payload["projection_id"]),
            actor_id=str(payload["actor_id"]),
            world_id=str(payload["world_id"]),
            state=state,
            prior_snapshot=_snapshot_from_dict(payload["prior_snapshot"]),
            years=[_year_from_dict(item) for item in payload.get("years", [])],
            source_events={item["event_id"]: _event_from_dict(item) for item in payload.get("source_events", [])},
            accesses={
                (item["event_id"], item["actor_id"]): _access_from_dict(item)
                for item in payload.get("accesses", [])
            },
            responses={
                (item["event_id"], item["actor_id"]): _response_from_dict(item)
                for item in payload.get("responses", [])
            },
            material_facts=dict(payload.get("material_facts") or {}),
            source_metadata=dict(payload.get("source_metadata") or {}),
            applied_event_ids=[str(x) for x in payload.get("applied_event_ids", [])],
            authority=str(payload.get("authority", "TEST_ONLY_SOURCEFREE_NO_SCIENCE_ISSUANCE")),
            canonical_c9_claimed=bool(payload.get("canonical_c9_claimed", False)),
            rival_store_created=bool(payload.get("rival_store_created", False)),
        )
        if projection.state_hash() != payload.get("state_hash"):
            raise LedgerRefusal("LEDGER_STATE_HASH_MISMATCH")
        return projection
