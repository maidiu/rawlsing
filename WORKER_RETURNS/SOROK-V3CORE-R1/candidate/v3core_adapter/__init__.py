"""SOROK V3CORE-R1 source-free historical-development adapter."""

import sys
from pathlib import Path

_VENDOR = Path(__file__).resolve().parent.parent / "vendor"
if str(_VENDOR) not in sys.path:
    sys.path.insert(0, str(_VENDOR))

from .contracts import (
    ActorAccess,
    ActorResponse,
    ActorWorldEvent,
    AnnualBinding,
    ClockDomain,
    EventDisposition,
    MaterialDelta,
    Provenance,
    SourceActorSnapshot,
    Status,
    StepOutcome,
    YearInput,
    YearRecord,
    YearResult,
)
from .derived_scope import derive_scoped, material_capacity_index
from .flow_quarantine import run_conserved_charge_flow_probe
from .i1_consumer import project_actual_market_event
from .ledger import HistoricalProjection
from .quarantine import assert_no_forbidden_defaults, quarantine_manifest
from .scheduler import SchedulerRefusal, load_plan, run_year, validate_step_order

__all__ = [
    "ActorAccess",
    "ActorResponse",
    "ActorWorldEvent",
    "AnnualBinding",
    "ClockDomain",
    "EventDisposition",
    "HistoricalProjection",
    "MaterialDelta",
    "Provenance",
    "SchedulerRefusal",
    "SourceActorSnapshot",
    "Status",
    "StepOutcome",
    "YearInput",
    "YearRecord",
    "YearResult",
    "assert_no_forbidden_defaults",
    "derive_scoped",
    "load_plan",
    "material_capacity_index",
    "project_actual_market_event",
    "quarantine_manifest",
    "run_conserved_charge_flow_probe",
    "run_year",
    "validate_step_order",
]
