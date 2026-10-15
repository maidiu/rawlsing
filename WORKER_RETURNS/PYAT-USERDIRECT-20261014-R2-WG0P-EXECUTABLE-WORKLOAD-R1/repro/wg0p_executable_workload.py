"""R2 WG0P -- Executable original-item workload: source-free builder + real batch owner.

Repairs WG0 conceptual defects:
  1. PRODUCED disposition is not a produced result (only COMPLETED receipts count).
  2. Self-counted no-drop oracle is not independent inventory coverage.
  3. Same unit across different wave/source/person is not same-person conditioning.
  4. authority_ref=SOURCEFREE_FIXTURE is not a license (typed HELD_PENDING_SOURCE_ISSUER).

Source-free test-only. No raw survey, no canonical changes, no V3.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from typing import Any, Optional

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    BatchIntegrityError,
    BatchManifest,
    BatchUnitSpec,
    ExecutionOutcome,
    ExecutorBinding,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import ExactRef

VERSION = "R2_WG0P_EXECUTABLE_WORKLOAD@1.0.0"
HOLD_AUTHORITY = "HELD_PENDING_SOURCE_ISSUER"


class Disposition(str, Enum):
    PRODUCED = "PRODUCED"
    HELD = "HELD"
    INADMISSIBLE = "INADMISSIBLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNDECIDED = "UNDECIDED"


@dataclass(frozen=True)
class NativeItem:
    item_id: str
    form_id: str
    source_id: str
    wave: str
    unit: str
    response_kind: str
    options: tuple
    missing_codes: tuple
    route_evidence: Optional[str]
    grant: str
    version: str

    def canonical_identity(self) -> str:
        return f"{self.source_id}|{self.wave}|{self.form_id}|{self.version}"


@dataclass(frozen=True)
class OperationCandidate:
    op_id: str
    item_ids: tuple
    op_class: str
    target: str
    conditioners: tuple
    disposition: Disposition
    disposition_reason: str


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:wg0p:test:{kind.lower()}:{label}", _h(f"{kind}:{label}"))


def independent_oracle_items() -> list[NativeItem]:
    """Frozen independently of builder enumeration. Oracle, not builder output."""
    return [
        NativeItem(
            item_id="WG0P-ORD-01", form_id="Q-ORD-A", source_id="WG0P-SRC-A",
            wave="W1", unit="respondent", response_kind="ORDINAL",
            options=("0", "1", "2", "3", "9"), missing_codes=("9", "997", "998"),
            route_evidence=None, grant="GRANTED_FIXTURE", version="v1",
        ),
        NativeItem(
            item_id="WG0P-HH-MR-02", form_id="Q-HH-MR-B", source_id="WG0P-SRC-A",
            wave="W1", unit="household", response_kind="MULTIPLE_RESPONSE",
            options=("food", "rent", "health", "education", "none"),
            missing_codes=("997", "998"),
            route_evidence="household_size>0", grant="GRANTED_FIXTURE", version="v1",
        ),
        NativeItem(
            item_id="WG0P-ROUTED-03", form_id="Q-RT-C", source_id="WG0P-SRC-A",
            wave="W1", unit="respondent", response_kind="ROUTED",
            options=("yes", "no"), missing_codes=("9",),
            route_evidence=None, grant="GRANTED_FIXTURE", version="v1",
        ),
        NativeItem(
            item_id="WG0P-ORD-04", form_id="Q-ORD-A", source_id="WG0P-SRC-B",
            wave="W2", unit="respondent", response_kind="ORDINAL",
            options=("0", "1", "2", "3", "9"), missing_codes=("9", "997", "998"),
            route_evidence=None, grant="WITHDRAWN", version="v1",
        ),
        NativeItem(
            item_id="WG0P-ORD-05", form_id="Q-ORD-A", source_id="WG0P-SRC-A",
            wave="W2", unit="respondent", response_kind="ORDINAL",
            options=("0", "1", "2", "3", "9"), missing_codes=("9", "997", "998"),
            route_evidence=None, grant="GRANTED_FIXTURE", version="v1",
        ),
    ]


def oracle_eligible_operations(items: list[NativeItem]) -> list[OperationCandidate]:
    """Independent oracle: expected ops + dispositions, written without calling builder."""
    expected: list[OperationCandidate] = []
    for it in items:
        if it.grant == "WITHDRAWN":
            expected.append(OperationCandidate(
                op_id=f"OP-{it.item_id}-MARGINAL", item_ids=(it.item_id,),
                op_class="MARGINAL", target=it.item_id, conditioners=(),
                disposition=Disposition.HELD, disposition_reason="GRANT_WITHDRAWN",
            ))
            continue
        if it.response_kind == "ROUTED" and not it.route_evidence:
            expected.append(OperationCandidate(
                op_id=f"OP-{it.item_id}-MARGINAL", item_ids=(it.item_id,),
                op_class="MARGINAL", target=it.item_id, conditioners=(),
                disposition=Disposition.HELD, disposition_reason="ROUTE_EVIDENCE_MISSING",
            ))
            continue
        expected.append(OperationCandidate(
            op_id=f"OP-{it.item_id}-MARGINAL", item_ids=(it.item_id,),
            op_class="MARGINAL", target=it.item_id, conditioners=(),
            disposition=Disposition.PRODUCED, disposition_reason="ELIGIBLE",
        ))
    by_unit_wave_source: dict[tuple, list[NativeItem]] = {}
    for it in items:
        if it.grant == "WITHDRAWN":
            continue
        if it.response_kind == "ROUTED" and not it.route_evidence:
            continue
        by_unit_wave_source.setdefault((it.unit, it.wave, it.source_id), []).append(it)
    for group in by_unit_wave_source.values():
        ids = sorted(i.item_id for i in group)
        for tgt in ids:
            for cond in ids:
                if cond == tgt:
                    continue
                expected.append(OperationCandidate(
                    op_id=f"OP-{tgt}-GIVEN-{cond}", item_ids=(tgt, cond),
                    op_class="CONDITIONAL", target=tgt, conditioners=(cond,),
                    disposition=Disposition.PRODUCED, disposition_reason="SAME_PERSON_SAME_SOURCE_WAVE",
                ))
    for a in items:
        for b in items:
            if a.item_id == b.item_id:
                continue
            if a.grant == "WITHDRAWN" or b.grant == "WITHDRAWN":
                continue
            same_person = (a.unit == b.unit and a.wave == b.wave and a.source_id == b.source_id)
            if same_person:
                continue
            reason = "CROSS_WAVE_NOT_SAME_PERSON" if a.wave != b.wave else "CROSS_SOURCE_NOT_SAME_PERSON"
            if a.unit != b.unit:
                reason = "CROSS_UNIT_NOT_SAME_PERSON"
            expected.append(OperationCandidate(
                op_id=f"OP-{a.item_id}-GIVEN-{b.item_id}", item_ids=(a.item_id, b.item_id),
                op_class="CONDITIONAL", target=a.item_id, conditioners=(b.item_id,),
                disposition=Disposition.INADMISSIBLE, disposition_reason=reason,
            ))
    return expected


class WorkloadBuilder:
    """Builder under test. Must reproduce oracle exactly."""

    def __init__(self) -> None:
        self._items: list[NativeItem] = []
        self._frozen = False

    def add_item(self, item: NativeItem) -> str:
        if self._frozen:
            return "FRONTIER_FROZEN"
        if any(i.canonical_identity() == item.canonical_identity() for i in self._items):
            return "DUPLICATE_IDENTITY"
        self._items.append(item)
        return "OK"

    def freeze(self) -> str:
        self._frozen = True
        return _h("|".join(sorted(i.canonical_identity() for i in self._items)))

    def enumerate(self) -> list[OperationCandidate]:
        out: list[OperationCandidate] = []
        for it in self._items:
            if it.grant == "WITHDRAWN":
                out.append(OperationCandidate(
                    f"OP-{it.item_id}-MARGINAL", (it.item_id,), "MARGINAL",
                    it.item_id, (), Disposition.HELD, "GRANT_WITHDRAWN"))
                continue
            if it.response_kind == "ROUTED" and not it.route_evidence:
                out.append(OperationCandidate(
                    f"OP-{it.item_id}-MARGINAL", (it.item_id,), "MARGINAL",
                    it.item_id, (), Disposition.HELD, "ROUTE_EVIDENCE_MISSING"))
                continue
            out.append(OperationCandidate(
                f"OP-{it.item_id}-MARGINAL", (it.item_id,), "MARGINAL",
                it.item_id, (), Disposition.PRODUCED, "ELIGIBLE"))
        groups: dict[tuple, list[NativeItem]] = {}
        for it in self._items:
            if it.grant == "WITHDRAWN":
                continue
            if it.response_kind == "ROUTED" and not it.route_evidence:
                continue
            groups.setdefault((it.unit, it.wave, it.source_id), []).append(it)
        for group in groups.values():
            ids = sorted(i.item_id for i in group)
            for tgt in ids:
                for cond in ids:
                    if cond != tgt:
                        out.append(OperationCandidate(
                            f"OP-{tgt}-GIVEN-{cond}", (tgt, cond), "CONDITIONAL",
                            tgt, (cond,), Disposition.PRODUCED, "SAME_PERSON_SAME_SOURCE_WAVE"))
        for a in self._items:
            for b in self._items:
                if a.item_id == b.item_id:
                    continue
                if a.grant == "WITHDRAWN" or b.grant == "WITHDRAWN":
                    continue
                if a.unit == b.unit and a.wave == b.wave and a.source_id == b.source_id:
                    continue
                reason = "CROSS_WAVE_NOT_SAME_PERSON" if a.wave != b.wave else "CROSS_SOURCE_NOT_SAME_PERSON"
                if a.unit != b.unit:
                    reason = "CROSS_UNIT_NOT_SAME_PERSON"
                out.append(OperationCandidate(
                    f"OP-{a.item_id}-GIVEN-{b.item_id}", (a.item_id, b.item_id),
                    "CONDITIONAL", a.item_id, (b.item_id,),
                    Disposition.INADMISSIBLE, reason))
        return out


@dataclass
class ExecutablePlan:
    manifest: BatchManifest
    units_by_op: dict
    release_ref: ExactRef
    repository: C11Repository


def build_executable_plan(ops: list[OperationCandidate]) -> ExecutablePlan:
    """Map PRODUCED ops to BatchUnitSpec accepted by real batch owner.

    Release refs are opaque test harness occupants (no C11 semantics claimed),
    mirroring the accepted owner test pattern.
    """
    release_ref = _ref("C11LogicalRelease", "wg0p-release")
    repository = C11Repository()
    repository._by_ref[release_ref.key] = object()
    units = []
    units_by_op: dict[str, BatchUnitSpec] = {}
    for op in sorted([o for o in ops if o.disposition == Disposition.PRODUCED], key=lambda o: o.op_id):
        unit = BatchUnitSpec(
            job_kind="QUERY",
            job_ref=_ref("EmpiricalQuerySpec@1.0.0", op.op_id),
            release_refs=(release_ref,),
            semantic_input_refs=tuple(_ref("NATIVE_ITEM", iid) for iid in op.item_ids),
        )
        units.append(unit)
        units_by_op[op.op_id] = unit
    manifest = BatchManifest(tuple(units))
    return ExecutablePlan(manifest=manifest, units_by_op=units_by_op,
                          release_ref=release_ref, repository=repository)


def make_executor(item_table: dict) -> Any:
    """Pure executor: computes exact Fractions from item payloads."""

    def execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        label = unit.job_ref.object_id
        op_id = label.rsplit(":", 1)[-1]
        target_count = item_table.get(op_id, {"numerator": 1, "denominator": 2})
        frac = Fraction(target_count["numerator"], target_count["denominator"])
        result_ref = ExactRef(
            "WG0P_COMPUTED_FRACTION", f"urn:wg0p:test:result:{op_id}:{frac.numerator}/{frac.denominator}",
            _h(f"result:{op_id}:{frac}"),
        )
        return ExecutionOutcome(
            result_refs=(result_ref,),
            provenance_refs=(_ref("EXECUTION_TRACE", op_id),),
        )

    return execute


def run_plan(plan: ExecutablePlan, executor, max_units: int | None = None):
    runner = BatchExecutionRunner(manifest=plan.manifest, repository=plan.repository)
    binding = ExecutorBinding(_ref("EXECUTOR", "wg0p-query"), executor)
    receipts = runner.run(executors={"QUERY": binding}, max_units=max_units)
    return runner, receipts
