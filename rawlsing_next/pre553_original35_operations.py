"""Source-pack-neutral original35 operation adapter.

The source configuration document is the only source-selection input. This
module does not read respondent values, invent source semantics, issue native
rights, or choose a survey-specific code path. It accounts every original item
and physical slot, emits per-operation typed eligibility, and provides a
minimal typed join to the existing R03 compiler/Batch/I03/I05 owners.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping
import json

from rawlsing_next.pre553_batch_runner import BatchUnitSpec
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_universal_workload import (
    UniversalOperation, compile_universal_workload, execute_universal_workload,
    compile_governed_frontier,
)
from rawlsing_next.universal_grammar.enumerate import (
    inventory_ledger, role_disposition,
)
from rawlsing_next.universal_grammar.types import (
    ADMINISTERED, ADMINISTRATION_UNKNOWN, NOT_ADMINISTERED, ELIGIBLE,
    MeasurePlan, Occurrence,
    OccurrenceKey, SourceInventory, GrammarPolicy, DirectionGrant,
    ScientificFrontier, FRONTIER_SCHEMA, NOT_STARTED, UNKNOWN,
    make_operation, content_hash,
)

SCHEMA = "PRE553_ORIGINAL35_OPERATIONS@1.0.0"
OPERATION_F1 = "F1_DISTRIBUTION"
OPERATION_F2 = "F2_CONDITIONAL"
OPERATION_F3H = "F3_HETEROGENEITY"
OPERATION_F3R = "F3_RECURSIVE"
OPERATION_F4 = "F4_JOINT"
EXECUTABLE = "EXECUTABLE_RAW"
HELD = "HELD"
ABSTAIN = "ABSTAIN"
INAPPLICABLE = "INAPPLICABLE"
DEFERRED = "DEFERRED"
NOT_REQUESTED = "NOT_REQUESTED"
STATUSES = (EXECUTABLE, HELD, ABSTAIN, INAPPLICABLE, DEFERRED, NOT_REQUESTED)
SOURCE_NOT_PRESENT_HERE = "SOURCE_NOT_PRESENT_HERE"
SOURCE_PRESENT = "SOURCE_PRESENT_BY_CUSTODY"
SOURCE_UNVERIFIED = "SOURCE_PRESENCE_NOT_VERIFIED_HERE"
RAW = "RAW_OBSERVED_SAMPLE"
WEIGHTED = "GOVERNED_WEIGHTED"


class Original35OperationError(ValueError):
    pass


def _sha(value: Any, name: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(
            ch not in "0123456789abcdef" for ch in value):
        raise Original35OperationError(name + " must be lowercase sha256")
    return value


def _ref(kind: str, object_id: str, digest: str) -> ExactRef:
    return ExactRef(kind, object_id, _sha(digest, "ref hash"))


def _documents(document: Any) -> list[dict]:
    if isinstance(document, (list, tuple)):
        docs = list(document)
    elif isinstance(document, Mapping) and isinstance(document.get("sources"), list):
        docs = document["sources"]
    elif isinstance(document, Mapping) and document.get("schema") == "PYAT_R157_SOURCE_CONFIGURATION@1.0.0":
        docs = [document]
    else:
        raise Original35OperationError("LIBRARY_OR_SOURCE_CONFIG_DOCUMENT_REQUIRED")
    if not docs or not all(isinstance(doc, Mapping) for doc in docs):
        raise Original35OperationError("SOURCE_CONFIG_DOCUMENT_LIST_REQUIRED")
    return [dict(doc) for doc in docs]


def _substantive(values: Iterable[Mapping[str, Any]]) -> tuple[str, ...]:
    out = set()
    for row in values:
        if (row.get("response_state") == "SUBSTANTIVE_RESPONSE"
                and row.get("canonical_value") is not None):
            out.add(str(row["canonical_value"]))
    return tuple(sorted(out))


def _special_states(values: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in values:
        state = row.get("response_state") or row.get("missing_state") or "UNKNOWN"
        if state != "SUBSTANTIVE_RESPONSE":
            counts[str(state)] += 1
    return dict(sorted(counts.items()))


@dataclass(frozen=True)
class PlanOperation:
    operation_id: str
    source_id: str
    kind: str
    item_ids: tuple[str, ...]
    source_variable_codes: tuple[str, ...]
    response_values: tuple[str, ...]
    conditioner_item_id: str | None
    conditioner_values: tuple[str, ...]
    joint_arity: int
    stratum_ref: str | None
    measure_kind: str
    status: str
    reason: str | None
    route_status: str
    response_states: Mapping[str, int]
    source_sha256: str
    administration: str = ADMINISTRATION_UNKNOWN
    unit: str = "UNKNOWN_UNIT"
    topology: str = "TOPOLOGY_UNKNOWN"
    forms: tuple[str, ...] = ("FORM_SLICE_UNKNOWN",)
    native: bool = False

    def material(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id, "source_id": self.source_id,
            "kind": self.kind, "item_ids": list(self.item_ids),
            "source_variable_codes": list(self.source_variable_codes),
            "response_values": list(self.response_values),
            "conditioner_item_id": self.conditioner_item_id,
            "conditioner_values": list(self.conditioner_values),
            "joint_arity": self.joint_arity, "stratum_ref": self.stratum_ref,
            "measure_kind": self.measure_kind, "status": self.status,
            "reason": self.reason, "route_status": self.route_status,
            "response_states": dict(self.response_states),
            "source_sha256": self.source_sha256,
            "administration": self.administration, "unit": self.unit,
            "topology": self.topology, "forms": list(self.forms),
            "native": self.native,
        }


@dataclass(frozen=True)
class SourceRow:
    source_id: str
    family: str
    wave: str
    source_sha256: str
    source_presence: str
    item_ids: tuple[str, ...]
    physical_slots: tuple[int, ...]
    response_slot_count: int
    weight_slot_count: int
    counts: Mapping[str, int]
    operation_refs: tuple[str, ...]
    weight_status: str
    pair_candidates: int
    pair_selected: int
    joint_candidates: int
    joint_selected: int

    def material(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id, "family": self.family, "wave": self.wave,
            "source_sha256": self.source_sha256,
            "source_presence": self.source_presence,
            "item_ids": list(self.item_ids),
            "physical_slots": list(self.physical_slots),
            "response_slot_count": self.response_slot_count,
            "weight_slot_count": self.weight_slot_count,
            "counts": dict(self.counts),
            "operation_refs": list(self.operation_refs),
            "weight_status": self.weight_status,
            "pair_candidates": self.pair_candidates,
            "pair_selected": self.pair_selected,
            "joint_candidates": self.joint_candidates,
            "joint_selected": self.joint_selected,
            "native": False,
        }


@dataclass(frozen=True)
class Original35OperationPlan:
    schema: str
    rows: tuple[SourceRow, ...]
    operations: tuple[PlanOperation, ...]
    counts: Mapping[str, int]
    item_count: int
    physical_slot_count: int
    pair_candidates: int
    pair_selected: int
    joint_candidates: int
    joint_selected: int
    no_drop_ok: bool
    universal_operations: tuple[UniversalOperation, ...]
    batch_units: tuple[BatchUnitSpec, ...]
    plan_ref: str

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "rows": [row.material() for row in self.rows],
            "operations": [op.material() for op in self.operations],
            "counts": dict(self.counts), "item_count": self.item_count,
            "physical_slot_count": self.physical_slot_count,
            "pair_candidates": self.pair_candidates,
            "pair_selected": self.pair_selected,
            "joint_candidates": self.joint_candidates,
            "joint_selected": self.joint_selected,
            "no_drop_ok": self.no_drop_ok,
            "batch_unit_count": len(self.batch_units),
            "plan_ref": self.plan_ref, "native": False,
        }

    def operations_for(self, source_id: str) -> tuple[PlanOperation, ...]:
        return tuple(op for op in self.operations if op.source_id == source_id)


def _presence(source_id: str, source_presence: Mapping[str, Any] | None,
              source_root: str | Path | None, artifact_name: str | None) -> str:
    if source_presence is not None and source_id in source_presence:
        value = source_presence[source_id]
        if isinstance(value, Mapping):
            return str(value.get("presence_grade") or value.get("status") or
                       (SOURCE_PRESENT if value.get("present") else SOURCE_NOT_PRESENT_HERE))
        return SOURCE_PRESENT if value is True else (
            SOURCE_NOT_PRESENT_HERE if value is False else str(value))
    if source_root is not None and artifact_name:
        return (SOURCE_PRESENT if (Path(source_root) / artifact_name).is_file()
                else SOURCE_NOT_PRESENT_HERE)
    return SOURCE_UNVERIFIED


def _source_plan(config: Mapping[str, Any], *, source_presence: Mapping[str, Any] | None,
                 source_root: str | Path | None, pair_budget: int,
                 joint_budget: int) -> tuple[SourceRow, list[PlanOperation], list[UniversalOperation], list[BatchUnitSpec]]:
    identity = config.get("identity") or {}
    binding = config.get("binding") or {}
    source_id = str(identity.get("source_id") or "")
    if not source_id.startswith("SRC"):
        raise Original35OperationError("SOURCE_ID_REQUIRED")
    source_sha = _sha(binding.get("source_sha256") or identity.get("expected_source_sha256"),
                      "source_sha256")
    items = list(config.get("items") or [])
    physical = list(config.get("physical_slots") or [])
    response_slots = list(config.get("response_slots") or [])
    coordinate_slots = list(config.get("coordinate_slots") or [])
    weight_slots = list(config.get("weight_slots") or [])
    routing = {str(row.get("question_id")): row for row in config.get("routing") or []}
    response_by_q = {str(row.get("question_id")): row for row in response_slots}
    item_ids = tuple(str(item.get("item_id") or item.get("implementation_id"))
                     for item in items)
    if any(not value or value == "None" for value in item_ids):
        raise Original35OperationError("ORIGINAL_ITEM_ID_REQUIRED")
    if len(set(item_ids)) != len(item_ids):
        raise Original35OperationError("DUPLICATE_ORIGINAL_ITEM_ID")
    item_by_code = {str(item.get("source_variable_code")): item for item in items}
    item_id_by_code = {
        str(item.get("source_variable_code")): str(item.get("item_id") or item.get("implementation_id"))
        for item in items}
    presence = _presence(
        source_id, source_presence, source_root,
        identity.get("source_artifact_id"))
    operations: list[PlanOperation] = []
    universal: list[UniversalOperation] = []
    batch: list[BatchUnitSpec] = []
    release = _ref(
        "C11LogicalRelease",
        "urn:rawlsing:pre553:original35:release:" + source_id + ":" + source_sha[:16],
        semantic_hash({"source_id": source_id, "source_sha256": source_sha,
                       "release": identity.get("release_id")}))
    eligible: list[tuple[str, str, tuple[str, ...], str, Mapping[str, int]]] = []
    stat_counts = Counter({status: 0 for status in STATUSES})
    subject_unit = str((config.get("respondents") or {}).get("subject_unit") or "")
    unit = ("household" if "HOUSEHOLD" in subject_unit.upper() else
            "person" if subject_unit else "UNKNOWN_UNIT")
    form_slice = str((config.get("supported_scope") or {}).get("supported_form_slice")
                     or "FORM_SLICE_UNKNOWN")
    item_facts: dict[str, dict[str, Any]] = {}
    for item in items:
        code = str(item.get("source_variable_code"))
        relation = item.get("relation") or {}
        raw_topology = str(relation.get("manual_response_topology") or "TOPOLOGY_UNKNOWN")
        topology = {"scalar": "SCALAR_SINGULAR",
                    "scalar_coordinate": "SCALAR_SINGULAR"}.get(
                        raw_topology, raw_topology)
        route = routing.get(code) or {}
        route_state = str(route.get("typed_state") or "ROUTING_UNKNOWN")
        administration = (ADMINISTERED if route_state == "ELIGIBLE_APPLICABLE"
                          else NOT_ADMINISTERED
                          if route_state in {"NOT_ASKED", "INAPPLICABLE"}
                          else ADMINISTRATION_UNKNOWN)
        item_facts[code] = {
            "administration": administration, "unit": unit,
            "topology": topology, "forms": (form_slice,),
            "route_state": route_state,
        }

    def emit(kind: str, item_ids_: tuple[str, ...], codes: tuple[str, ...],
             values: tuple[str, ...], status: str, reason: str | None,
             route_status: str, states: Mapping[str, int] | None = None,
             conditioner_id: str | None = None,
             conditioner_values: tuple[str, ...] = (),
             joint_arity: int = 0, stratum: str | None = None,
             measure: str = RAW) -> PlanOperation:
        material = {
            "source_id": source_id, "source_sha256": source_sha, "kind": kind,
            "item_ids": item_ids_, "codes": codes, "values": values,
            "conditioner_id": conditioner_id, "conditioner_values": conditioner_values,
            "joint_arity": joint_arity, "stratum": stratum, "measure": measure,
            "status": status, "reason": reason, "route": route_status,
            "states": dict(states or {}),
        }
        digest = semantic_hash(material)
        op = PlanOperation(
            operation_id="urn:rawlsing:pre553:original35:op:" + digest,
            source_id=source_id, kind=kind, item_ids=item_ids_,
            source_variable_codes=codes, response_values=values,
            conditioner_item_id=conditioner_id,
            conditioner_values=conditioner_values, joint_arity=joint_arity,
            stratum_ref=stratum, measure_kind=measure, status=status,
            reason=reason, route_status=route_status,
            response_states=dict(states or {}), source_sha256=source_sha,
            administration=item_facts.get(codes[0], {}).get(
                "administration", ADMINISTRATION_UNKNOWN),
            unit=item_facts.get(codes[0], {}).get("unit", "UNKNOWN_UNIT"),
            topology=item_facts.get(codes[0], {}).get("topology", "TOPOLOGY_UNKNOWN"),
            forms=item_facts.get(codes[0], {}).get(
                "forms", ("FORM_SLICE_UNKNOWN",)))
        operations.append(op)
        stat_counts[status] += 1
        if status == EXECUTABLE and kind == OPERATION_F1 and values:
            for value in values:
                uop = UniversalOperation(
                    operation_id="urn:r03:op:" + semantic_hash({
                        "original_operation": op.operation_id, "value": value})[:40],
                    source_variable_code=codes[0], response_value=value,
                    occurrence_identity={"item_id": item_ids_[0],
                                         "source_id": source_id,
                                         "source_sha256": source_sha},
                    measure_kind="RAW", status="COMPILED")
                universal.append(uop)
                batch.append(BatchUnitSpec(
                    job_kind="QUERY",
                    job_ref=_ref("PRE553Original35Operation",
                                 op.operation_id,
                                 semantic_hash({"op": op.operation_id, "value": value})),
                    release_refs=(release,),
                    semantic_input_refs=(_ref("Original35Item", item_ids_[0],
                                              semantic_hash({"item": item_ids_[0]})),)))
        return op

    for item in items:
        code = str(item.get("source_variable_code"))
        item_id = item_id_by_code[code]
        disposition = str(item.get("disposition") or "")
        slot = response_by_q.get(code)
        route = routing.get(code) or {}
        route_state = str(route.get("typed_state") or "ROUTING_UNKNOWN")
        if slot is None:
            if item_id in {str((c.get("slot") or {}).get("name")) for c in coordinate_slots} or "COORDINATE" in disposition:
                emit(OPERATION_F1, (item_id,), (code,), (), INAPPLICABLE,
                     "COORDINATE_CONTEXT_NOT_A_RESPONSE_DISTRIBUTION", route_state)
            elif "HELD" in disposition or "UNKNOWN" in disposition:
                emit(OPERATION_F1, (item_id,), (code,), (), HELD,
                     "ITEM_DISPOSITION_" + disposition, route_state)
            elif "GENERATION_FORBIDDEN" in disposition or "ADMIN" in disposition:
                emit(OPERATION_F1, (item_id,), (code,), (), INAPPLICABLE,
                     "ITEM_DISPOSITION_" + disposition, route_state)
            elif "SUPPORTED" in disposition or "INCLUDED" in disposition:
                emit(OPERATION_F1, (item_id,), (code,), (), HELD,
                     "RESPONSE_MAPPING_ABSENT", route_state)
            else:
                emit(OPERATION_F1, (item_id,), (code,), (), INAPPLICABLE,
                     "NO_ADMINISTERED_RESPONSE_SLOT", route_state)
            continue
        values = _substantive(slot.get("values") or [])
        states = _special_states(slot.get("values") or [])
        if not values:
            emit(OPERATION_F1, (item_id,), (code,), (), HELD,
                 "NO_SUBSTANTIVE_DOMAIN_VALUE", route_state, states)
            continue
        if route_state in {"NOT_ASKED", "INAPPLICABLE"}:
            emit(OPERATION_F1, (item_id,), (code,), values, HELD,
                 "ROUTE_" + route_state, route_state, states)
            continue
        if "HELD" in disposition or disposition == "UNKNOWN":
            emit(OPERATION_F1, (item_id,), (code,), values, HELD,
                 "ITEM_DISPOSITION_" + disposition, route_state, states)
            continue
        emit(OPERATION_F1, (item_id,), (code,), values, EXECUTABLE, None,
             route_state, states)
        eligible.append((item_id, code, values, route_state, states))

    # Optional weights never gate RAW. A weighted request is typed separately.
    weight_status = ("WEIGHT_DESIGN_AUTHORITY_UNRESOLVED" if weight_slots
                     else "ABSENT_OPTIONAL_RAW_SUPPORTED")
    if weight_slots and eligible:
        item_id, code, values, route_state, states = eligible[0]
        emit(OPERATION_F1, (item_id,), (code,), values, DEFERRED,
             weight_status, route_state, states, measure=WEIGHTED)

    # F2 both directions, bounded deterministic frontier, not all pairs.
    pair_candidates = len(eligible) * (len(eligible) - 1)
    pair_selected = 0
    for index, (left_id, left_code, left_values, left_route, left_states) in enumerate(eligible):
        if pair_selected >= pair_budget:
            break
        for right in eligible[index + 1:]:
            if pair_selected >= pair_budget:
                break
            right_id, right_code, right_values, right_route, right_states = right
            for source_item, target_item, source_code, target_code, target_values in (
                (left_id, right_id, left_code, right_code, right_values),
                (right_id, left_id, right_code, left_code, left_values),
            ):
                emit(OPERATION_F2, (target_item, source_item),
                     (target_code, source_code), target_values, EXECUTABLE,
                     None, right_route if target_item == right_id else left_route,
                     {**left_states, **right_states},
                     conditioner_id=source_item,
                     conditioner_values=(left_values if target_item == right_id else right_values))
                pair_selected += 1

    # F3 heterogeneity/recursive alternatives are typed even when deferred.
    if eligible:
        item_id, code, values, route_state, states = eligible[0]
        stratum = (coordinate_slots[0].get("slot") or {}).get("name") if coordinate_slots else None
        emit(OPERATION_F3H, (item_id,), (code,), values,
             EXECUTABLE if stratum else DEFERRED,
             None if stratum else "STRATUM_VALUES_ABSENT", route_state, states,
             stratum=str(stratum) if stratum else None)
        emit(OPERATION_F3R, (item_id,), (code,), values, DEFERRED,
             "RECURSIVE_AUTHORITY_NOT_ISSUED", route_state, states)

    # F4 true 3+ same-person joint/minority request; source rows not decoded here.
    joint_candidates = (len(eligible) * (len(eligible) - 1) * (len(eligible) - 2)
                        if len(eligible) >= 3 else 0)
    joint_selected = 0
    for start in range(min(joint_budget, max(0, len(eligible) - 2))):
        triple = eligible[start:start + 3]
        if len(triple) < 3:
            break
        ids = tuple(row[0] for row in triple)
        codes = tuple(row[1] for row in triple)
        values = tuple(value for row in triple for value in row[2])
        emit(OPERATION_F4, ids, codes, values, DEFERRED,
             "SOURCE_ROWS_NOT_DECODED_THIS_RUN", "SAME_PERSON_ROW_REQUIRED",
             {key: value for row in triple for key, value in row[4].items()},
             joint_arity=3)
        joint_selected += 1

    for status in STATUSES:
        stat_counts.setdefault(status, 0)
    row = SourceRow(
        source_id=source_id, family=str(identity.get("family")),
        wave=str(identity.get("wave")), source_sha256=source_sha,
        source_presence=presence, item_ids=item_ids,
        physical_slots=tuple(int(row.get("ordinal")) for row in physical),
        response_slot_count=len(response_slots), weight_slot_count=len(weight_slots),
        counts=dict(sorted(stat_counts.items())),
        operation_refs=tuple(op.operation_id for op in operations),
        weight_status=weight_status, pair_candidates=pair_candidates,
        pair_selected=pair_selected, joint_candidates=joint_candidates,
        joint_selected=joint_selected)
    return row, operations, universal, batch


def build_original35_operation_plan(
    document: Any, *, source_presence: Mapping[str, Any] | None = None,
    source_root: str | Path | None = None, pair_budget: int = 6,
    joint_budget: int = 1, require_all35: bool = True,
    expected_item_count: int | None = None,
    expected_physical_slot_count: int | None = None,
) -> Original35OperationPlan:
    """Build the no-drop source-neutral plan from library/config documents."""
    docs = _documents(document)
    if require_all35 and len(docs) != 35:
        raise Original35OperationError("INDEPENDENT_ORIGINAL35_ROSTER_REQUIRED")
    rows: list[SourceRow] = []
    operations: list[PlanOperation] = []
    universal: list[UniversalOperation] = []
    batch: list[BatchUnitSpec] = []
    seen_sources: set[str] = set()
    for config in docs:
        row, ops, uops, units = _source_plan(
            config, source_presence=source_presence, source_root=source_root,
            pair_budget=pair_budget, joint_budget=joint_budget)
        if row.source_id in seen_sources:
            raise Original35OperationError("DUPLICATE_SOURCE_ID")
        seen_sources.add(row.source_id)
        rows.append(row)
        operations.extend(ops)
        universal.extend(uops)
        batch.extend(units)
    total_items = sum(len(row.item_ids) for row in rows)
    total_slots = sum(len(row.physical_slots) for row in rows)
    if expected_item_count is not None and total_items != expected_item_count:
        raise Original35OperationError("ORIGINAL_ITEM_COUNT_MISMATCH")
    if expected_physical_slot_count is not None and total_slots != expected_physical_slot_count:
        raise Original35OperationError("PHYSICAL_SLOT_COUNT_MISMATCH")
    counts = Counter({status: 0 for status in STATUSES})
    for operation in operations:
        counts[operation.status] += 1
    item_keys = [(row.source_id, item_id) for row in rows for item_id in row.item_ids]
    no_drop_ok = (
        (not require_all35 or len(rows) == 35)
        and len(set(item_keys)) == len(item_keys) == total_items
        and sum(counts.values()) == len(operations)
        and all(sum(row.counts.values()) == len(row.operation_refs) for row in rows)
    )
    # Whole-plan duplicate check uses counters, never quadratic scans.
    duplicates = [key for key, count in Counter(
        op.operation_id for op in operations).items() if count > 1]
    no_drop_ok = no_drop_ok and not duplicates
    plan_material = {
        "schema": SCHEMA,
        "rows": [row.material() for row in rows],
        "operations": [op.material() for op in operations],
        "counts": dict(sorted(counts.items())),
        "item_count": total_items, "physical_slot_count": total_slots,
    }
    plan_ref = semantic_hash(plan_material)
    return Original35OperationPlan(
        schema=SCHEMA, rows=tuple(rows), operations=tuple(operations),
        counts=dict(sorted(counts.items())), item_count=total_items,
        physical_slot_count=total_slots,
        pair_candidates=sum(row.pair_candidates for row in rows),
        pair_selected=sum(row.pair_selected for row in rows),
        joint_candidates=sum(row.joint_candidates for row in rows),
        joint_selected=sum(row.joint_selected for row in rows),
        no_drop_ok=no_drop_ok, universal_operations=tuple(universal),
        batch_units=tuple(sorted(batch, key=lambda unit: unit.unit_ref.key)),
        plan_ref=plan_ref)


@dataclass(frozen=True)
class UniversalLowering:
    plan_ref: str
    compilation: Any
    matched_operation_ids: tuple[str, ...]
    missing: tuple[tuple[str, str], ...]
    unexpected: tuple[tuple[str, str], ...]
    no_drop_ok: bool


def lower_to_universal_workload(plan: Original35OperationPlan, *, bundle: Any,
                                as_of: str, host: str, purpose: str) -> UniversalLowering:
    """Join plan distribution requests to the CURRENT R03 compiler; no second compiler."""
    if not isinstance(plan, Original35OperationPlan):
        raise Original35OperationError("ORIGINAL35_OPERATION_PLAN_REQUIRED")
    compilation = compile_universal_workload(
        bundle=bundle, as_of=as_of, host=host, purpose=purpose)
    required = {
        (op.source_variable_codes[0], value)
        for op in plan.operations
        if op.kind == OPERATION_F1 and op.status == EXECUTABLE
        and op.measure_kind == RAW
        for value in op.response_values
    }
    compiled = {
        (op.source_variable_code, op.response_value)
        for op in compilation.operations if op.status == "COMPILED"
    }
    missing = tuple(sorted(required - compiled))
    unexpected = tuple(sorted(compiled - required))
    return UniversalLowering(
        plan_ref=plan.plan_ref, compilation=compilation,
        matched_operation_ids=tuple(sorted(
            op.operation_id for op in compilation.operations
            if (op.source_variable_code, op.response_value) in required)),
        missing=missing, unexpected=unexpected,
        no_drop_ok=not missing and not unexpected)


def execute_plan_universal(plan: Original35OperationPlan, *, bundle: Any,
                           source_factory: Any, as_of: str, host: str,
                           purpose: str) -> tuple[UniversalLowering, Any]:
    lowering = lower_to_universal_workload(
        plan, bundle=bundle, as_of=as_of, host=host, purpose=purpose)
    if not lowering.no_drop_ok:
        raise Original35OperationError(
            "CURRENT_COMPILER_PLAN_MISMATCH:" + json.dumps(
                {"missing": lowering.missing, "unexpected": lowering.unexpected}))
    result = execute_universal_workload(
        compilation=lowering.compilation, source_factory=source_factory)
    if not result.anti_join()["no_drop_ok"]:
        raise Original35OperationError("CURRENT_CONSUMER_NO_DROP_FAILED")
    return lowering, result




def build_frontier_inputs_from_plan(plan: Original35OperationPlan, *,
                                    source_id: str | None = None):
    """Build CURRENT grammar types from ONLY explicit planned F2/F3/F4 requests."""
    if not isinstance(plan, Original35OperationPlan):
        raise Original35OperationError("ORIGINAL35_OPERATION_PLAN_REQUIRED")
    sid = source_id or (plan.rows[0].source_id if plan.rows else None)
    if sid is None:
        raise Original35OperationError("SOURCE_ID_REQUIRED")
    row = next((r for r in plan.rows if r.source_id == sid), None)
    if row is None:
        raise Original35OperationError("SOURCE_NOT_IN_PLAN")
    selected = [op for op in plan.operations
                if op.source_id == sid
                and op.kind in {OPERATION_F2, OPERATION_F3H, OPERATION_F3R, OPERATION_F4}
                and op.status not in {HELD, INAPPLICABLE}
                and not (op.kind == OPERATION_F3R and op.status == DEFERRED)]
    if not selected:
        raise Original35OperationError("NO_EXPLICIT_PLANNED_FRONTIER")
    id_by_code: dict[str, str] = {}
    facts_by_code: dict[str, PlanOperation] = {}
    domain_by_code: dict[str, set[str]] = {}
    for op in plan.operations:
        if op.source_id != sid:
            continue
        if op.kind == OPERATION_F1:
            code = op.source_variable_codes[0]
            facts_by_code[code] = op
            domain_by_code.setdefault(code, set()).update(op.response_values)
        for original_id, code in zip(op.item_ids, op.source_variable_codes):
            prior = id_by_code.get(code)
            if prior is not None and prior != original_id:
                raise Original35OperationError(
                    "ORIGINAL_ID_TO_PHYSICAL_CODE_CONFLICT:" + code)
            id_by_code[code] = original_id
    codes = sorted({code for op in selected for code in op.source_variable_codes})
    missing_ids = [code for code in codes if not id_by_code.get(code)]
    if missing_ids:
        raise Original35OperationError(
            "ORIGINAL_ITEM_ID_ABSENT:" + ",".join(missing_ids))
    occurrences = []
    for code in codes:
        original_id = id_by_code[code]
        fact = facts_by_code.get(code)
        if fact is None:
            raise Original35OperationError("ITEM_FACT_ABSENT:" + code)
        domain = tuple(sorted(domain_by_code.get(code) or {"0"}))
        occurrences.append(Occurrence(
            key=OccurrenceKey(item_id=original_id), label=code,
            unit=fact.unit, topology=fact.topology, forms=fact.forms,
            domain=domain, target_role="TARGET", conditioner_role="CONDITIONER",
            administration=fact.administration,
            route_state=("KNOWN" if fact.route_status == "ELIGIBLE_APPLICABLE"
                         else "UNKNOWN" if fact.route_status == "ROUTING_UNKNOWN"
                         else fact.route_status),
            semantic_state="OBSERVED_SOURCE_NATIVE", scope=sid,
            risk_set_refs=()))
    classes = ("DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL",
               "INTERACTION", "FORK", "STATE_ROBUSTNESS")
    grants = []
    for cls in classes:
        for arity in (1, 2, 3):
            grants.append(DirectionGrant(
                tuple("TARGET" for _ in range(arity)), (), cls,
                "urn:plan:direction:" + cls + ":unary:" + str(arity)))
            grants.append(DirectionGrant(
                tuple("TARGET" for _ in range(arity)), ("CONDITIONER",), cls,
                "urn:plan:direction:" + cls + ":conditional:" + str(arity)))
    policy = GrammarPolicy(
        policy_id="PLAN-POLICY-" + sid, grade="PROPOSED_TEST_ONLY",
        allowed_classes=classes, separate_classes=(),
        target_roles=("TARGET",), conditioner_roles=("CONDITIONER",),
        administrative_roles=(), direction_grants=tuple(grants),
        bounds={"J": 3, "K": 1, "D": 0}, population_requires_weight=False,
        validation_policy="EXPLICIT_PLANNED_REQUESTS", exploration_policy="BOUNDED",
        stop_policy="EXPLICIT_PLANNED_FRONTIER", owner_refs=("D_PLAN_ADAPTER",),
        authority_refs=(), risk_set_policy="UNCONSTRAINED")
    measure = MeasurePlan(
        measure_id="PLAN-RAW", kind="SAMPLE", weight_ref=None, design_ref=None,
        estimand="RAW_OBSERVED_SAMPLE", variance_policy="NONE")
    inventory = SourceInventory(
        inventory_id="PLAN-INV-" + sid, source_id=sid, wave=row.wave,
        edition=row.wave, source_sha256=row.source_sha256, scope=sid,
        occurrences=tuple(occurrences), measure_plans=(measure,),
        risk_set_refs=(), unit_transforms=(), state_map={}, authority_refs=(),
        current_selection=None, inventory_complete=True, dataset_id=sid,
        instrument_ref=None, observation_clock_ref=None, reference_clock_ref=None,
        as_of_ref=None, publication_clock_ref=None)
    by_key = inventory.by_key()
    operations = []
    for planned in selected:
        if planned.kind == OPERATION_F4:
            target_keys = tuple(OccurrenceKey(item_id=value) for value in planned.item_ids)
            claim_class = "JOINT"
            conditions = ()
            conditioner_roles = ()
            condition_values = (None,)
        else:
            target_key = OccurrenceKey(item_id=planned.item_ids[0])
            target_keys = (target_key,)
            claim_class = ("STATE_ROBUSTNESS" if planned.kind == OPERATION_F3H
                           else "CONDITIONAL")
            condition_key = None
            if planned.kind == OPERATION_F2 and planned.conditioner_item_id:
                condition_key = OccurrenceKey(item_id=planned.conditioner_item_id)
                condition_values = planned.conditioner_values or (None,)
                conditioner_roles = ("CONDITIONER",)
            else:
                condition_values = (None,)
                conditioner_roles = ()
        for condition_value in condition_values:
            active_conditions = (() if condition_value is None or condition_key is None
                                 else ((condition_key, condition_value),))
            target_roles = tuple(by_key[key].target_role for key in target_keys)
            disposition, reasons, risk_refs = role_disposition(
                inventory, policy, targets=target_keys, target_roles=target_roles,
                conditions=active_conditions, conditioner_roles=conditioner_roles,
                claim_class=claim_class, condition_mode="AND", measure=measure)
            direction = policy.direction_for(target_roles, conditioner_roles, claim_class)
            used = [by_key[key] for key in target_keys] + [
                by_key[key] for key, _ in active_conditions]
            form_scope = sorted(set.intersection(*(set(item.forms) for item in used)))
            operation = make_operation(
                inventory=inventory, policy=policy, claim_class=claim_class,
                targets=target_keys, target_roles=target_roles,
                conditions=active_conditions, conditioner_roles=conditioner_roles,
                condition_mode="AND", unit=used[0].unit,
                topology=used[0].topology, measure=measure,
                risk_set_ref=(risk_refs[0] if risk_refs else None),
                risk_set_refs=risk_refs,
                direction_ref=(direction.direction_ref if direction else None),
                form_scope=form_scope, scope=sid,
                disposition=disposition, reasons=reasons,
                native_support=("PENDING" if disposition == ELIGIBLE else "NOT_APPLICABLE"),
                administration_states=sorted({item.administration for item in used}),
                aliases=(planned.operation_id,))
            operations.append(operation)
    operations = tuple(sorted(operations, key=lambda op: op.op_id))
    if not operations:
        raise Original35OperationError("NO_EXPLICIT_FRONTIER_OPERATIONS")
    class_counts = Counter(op.claim_class for op in operations)
    disposition_counts = Counter(op.disposition for op in operations)
    ids = tuple(op.op_id for op in operations)
    frontier = ScientificFrontier(
        schema=FRONTIER_SCHEMA, inventory_id=inventory.inventory_id,
        inventory_hash=inventory.content_hash, policy_id=policy.policy_id,
        policy_hash=policy.content_hash, policy_grade=policy.grade,
        source_identity={"source_id": sid, "source_sha256": row.source_sha256,
                         "wave": row.wave, "edition": row.wave},
        operations=operations,
        inventory_ledger=inventory_ledger(inventory, policy),
        class_counts=dict(sorted(class_counts.items())),
        disposition_counts=dict(sorted(disposition_counts.items())),
        execution_counts={NOT_STARTED: len(operations)},
        result_counts={UNKNOWN: len(operations)},
        deferred=tuple({"operation_id": op.op_id, "reason": list(op.reasons)}
                       for op in operations if op.disposition in {HELD, UNKNOWN}),
        unknown=(), excluded=(), budget_state="EXPLICIT_PLANNED",
        pending_operation_ids=(), partition_size=64,
        partition_root=content_hash({"operation_ids": list(ids),
                                     "partition_size": 64}),
        partition_count=(len(ids) + 63) // 64,
        maximum_bounds=dict(policy.bounds), u_item_root=None,
        u_unit_root=None, u_app_root=None, e_pre_count=len(operations),
        e_pre_root=content_hash([op.identity_material() for op in operations]),
        e_pre_cause=None)
    return inventory, policy, frontier


def _bundle_with_plan_aliases(plan: Original35OperationPlan, source_id: str,
                              bundle: Any) -> Any:
    """Verified OriginalItemID -> physical code -> native question-ref aliases."""
    from dataclasses import replace
    aliases: dict[str, Any] = {}
    for op in plan.operations:
        if op.source_id != source_id:
            continue
        for original_id, code in zip(op.item_ids, op.source_variable_codes):
            qref = bundle.question_refs.get(code)
            if qref is None:
                raise Original35OperationError(
                    "PHYSICAL_CODE_NOT_IN_BUNDLE:" + code)
            prior = aliases.get(original_id)
            if prior is not None and prior != qref:
                raise Original35OperationError(
                    "CROSS_SOURCE_OR_CONFLICTING_ORIGINAL_ID:" + original_id)
            existing = bundle.question_refs.get(original_id)
            if existing is not None and existing != qref:
                raise Original35OperationError(
                    "ORIGINAL_ID_CONTRADICTS_BUNDLE_IDENTITY:" + original_id)
            aliases[original_id] = qref
    if not aliases:
        raise Original35OperationError("NO_ORIGINAL_ITEM_ALIASES")
    merged = dict(bundle.question_refs)
    merged.update(aliases)
    return replace(bundle, question_refs=merged)


def _plan_frontier_missing(plan: Original35OperationPlan, source_id: str,
                           frontier: Any) -> tuple[str, ...]:
    operations = list(frontier.operations)
    missing: list[str] = []
    for op in plan.operations:
        if op.source_id != source_id or op.kind not in {
                OPERATION_F2, OPERATION_F3H, OPERATION_F3R, OPERATION_F4}:
            continue
        if op.status in {HELD, INAPPLICABLE}:
            continue
        if op.kind == OPERATION_F3R and op.status == DEFERRED:
            continue
        targets = list(op.item_ids)
        if op.kind == OPERATION_F4:
            if not any(len(candidate.targets) >= 3
                       and [key.item_id for key in candidate.targets] == targets
                       for candidate in operations):
                missing.append("F4:" + ",".join(targets))
            continue
        target = op.item_ids[0]
        if op.kind == OPERATION_F3H:
            if not any(len(candidate.targets) == 1
                       and candidate.targets[0].item_id == target
                       for candidate in operations):
                missing.append("F3H:" + target)
            continue
        if op.kind == OPERATION_F3R:
            if not any(candidate.claim_class == "FORK"
                       and candidate.targets[0].item_id == target
                       for candidate in operations):
                missing.append("F3R:" + target)
            continue
        conditioner = op.conditioner_item_id
        if not any(
            len(candidate.targets) == 1
            and candidate.targets[0].item_id == target
            and any(key.item_id == conditioner and str(value) in op.conditioner_values
                    for key, value in candidate.conditions)
            for candidate in operations
        ):
            missing.append("F2:" + target + "<-" + conditioner)
    return tuple(sorted(set(missing)))

def bind_governed_frontier(plan: Original35OperationPlan, *, bundle: Any,
                           inventory: Any | None = None, policy: Any | None = None,
                           frontier: Any | None = None,
                           source_id: str | None = None,
                           as_of: str, host: str, purpose: str) -> Any:
    """Wire actual planned F2/F3/F4 payload into CURRENT compiler inputs."""
    sid = source_id or (plan.rows[0].source_id if plan.rows else None)
    if inventory is None or policy is None or frontier is None:
        inventory, policy, frontier = build_frontier_inputs_from_plan(
            plan, source_id=sid)
    else:
        if inventory.source_sha256 != next(
                row.source_sha256 for row in plan.rows if row.source_id == sid):
            raise Original35OperationError("PROVIDED_INVENTORY_SOURCE_MISMATCH")
    missing = _plan_frontier_missing(plan, sid, frontier)
    if missing:
        raise Original35OperationError(
            "GOVERNED_FRONTIER_PLAN_PAYLOAD_MISSING:" + ",".join(missing))
    alias_bundle = _bundle_with_plan_aliases(plan, sid, bundle)
    compilation = compile_governed_frontier(
        bundle=alias_bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=as_of, host=host, purpose=purpose)
    return compilation


__all__ = [
    "ABSTAIN", "DEFERRED", "EXECUTABLE", "HELD", "INAPPLICABLE",
    "NOT_REQUESTED", "OPERATION_F1", "OPERATION_F2", "OPERATION_F3H",
    "OPERATION_F3R", "OPERATION_F4", "Original35OperationError",
    "Original35OperationPlan", "PlanOperation", "RAW", "SCHEMA",
    "SOURCE_NOT_PRESENT_HERE", "SOURCE_PRESENT", "SOURCE_UNVERIFIED",
    "SourceRow", "UniversalLowering", "WEIGHTED", "bind_governed_frontier",
    "build_frontier_inputs_from_plan", "build_original35_operation_plan",
    "execute_plan_universal", "lower_to_universal_workload",
]
