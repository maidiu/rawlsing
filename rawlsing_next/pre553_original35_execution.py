"""D: bounded original35 manifest and original-source C11 execution bridge.

A source_configuration library is the selector; the B operation plan is the
accounting layer. This module decodes caller-authorized original bytes through
the existing physical decoder, builds the existing governed C11 release and
repository, and records RAW observed-sample products. It never invents source
semantics, native rights or a second compiler.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import json
import os
from pathlib import Path
import time
from typing import Any, Mapping

from dataclasses import replace
from rawlsing_next.pre553_original35_operations import (
    EXECUTABLE, OPERATION_F1, OPERATION_F2, OPERATION_F3H,
    _bundle_with_plan_aliases, bind_governed_frontier,
    build_frontier_inputs_from_plan, build_original35_operation_plan,
)
from rawlsing_next.universal_grammar.enumerate import (
    inventory_ledger, role_disposition,
)
from rawlsing_next.universal_grammar.types import (
    ELIGIBLE, FRONTIER_SCHEMA, NOT_STARTED, UNKNOWN, OccurrenceKey,
    ScientificFrontier, content_hash, make_operation,
)
from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav
from rawlsing_next.pre553_empirical_objects import (
    RespondentEvent, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_field_forge_empirical_ingress import envelope_material
from rawlsing_next.source_configuration.factory import (
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.reader import (
    decode_config_with_source_read_permission,
    reader_configuration_from_config, source_read_request_from_config,
)
from rawlsing_next.pre553_source_read_admission import (
    decode_with_source_read_permission,
)
from rawlsing_next.pre553_original35_physical_stream import bounded_physical_cell_stream
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_source_native_preimage_adapter import (
    NativeSourceIdentity, NativeSourcePackage, NativeSourceRule,
    materialize_native_preimages,
)
from rawlsing_next.pre553_universal_workload import (
    compile_governed_frontier, compile_universal_workload,
    execute_governed_frontier, execute_universal_workload,
)

SCHEMA = "PRE553_ORIGINAL35_EXECUTION@1.0.0"
DEFAULT_BINDING = Path(".local-logs/pyat-universal35/source-runtime-binding.local.json")


class Original35ExecutionError(ValueError):
    pass


@dataclass(frozen=True)
class SourceExecutionResult:
    source_id: str
    status: str
    source_sha256: str | None
    config_path: str | None
    source_format: str | None
    row_count: int
    physical_slots: int
    response_slots: int
    operation_counts: Mapping[str, int]
    c11_release_ref: Mapping[str, Any] | None
    c11_object_count: int
    raw_state_counts: Mapping[str, int]
    question_state_counts: Mapping[str, Mapping[str, int]]
    respondent_count: int
    max_events_per_respondent: int
    respondents_with_3plus_items: int
    repository_ref: str | None
    elapsed_seconds: float
    maxrss_bytes: int
    reasons: tuple[str, ...]

    def material(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA, "source_id": self.source_id, "status": self.status,
            "source_sha256": self.source_sha256, "config_path": self.config_path,
            "source_format": self.source_format, "row_count": self.row_count,
            "physical_slots": self.physical_slots,
            "response_slots": self.response_slots,
            "operation_counts": dict(self.operation_counts),
            "c11_release_ref": dict(self.c11_release_ref) if self.c11_release_ref else None,
            "c11_object_count": self.c11_object_count,
            "raw_state_counts": dict(self.raw_state_counts),
            "question_state_counts": {
                key: dict(value) for key, value in self.question_state_counts.items()
            },
            "respondent_count": self.respondent_count,
            "max_events_per_respondent": self.max_events_per_respondent,
            "respondents_with_3plus_items": self.respondents_with_3plus_items,
            "repository_ref": self.repository_ref,
            "elapsed_seconds": round(self.elapsed_seconds, 3),
            "maxrss_bytes": self.maxrss_bytes,
            "reasons": list(self.reasons), "native": False,
        }


def load_runtime_binding(path: str | Path | None = None) -> dict[str, Any]:
    target = Path(path or os.environ.get("PYAT_SOURCE_RUNTIME_BINDING", DEFAULT_BINDING))
    if not target.is_file():
        raise Original35ExecutionError("SOURCE_RUNTIME_BINDING_REQUIRED:" + str(target))
    document = json.loads(target.read_text(encoding="utf8"))
    root = document.get("USER_ORIGINAL35_DATA_ROOT")
    if not isinstance(root, str) or not Path(root).is_dir():
        raise Original35ExecutionError("SOURCE_ROOT_UNAVAILABLE")
    return document


def _encoding(config) -> str | None:
    reader = config.document["identity"].get("reader") or {}
    value = reader.get("encoding")
    return value.get("value") if isinstance(value, Mapping) else None


def _maxrss() -> int:
    try:
        import resource
        return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    except Exception:
        return 0


def _raw_products(release) -> tuple[dict[str, int], dict[str, dict[str, int]], int, int, int]:
    states: Counter[str] = Counter()
    by_question: dict[str, Counter[str]] = defaultdict(Counter)
    by_respondent: dict[str, set[str]] = defaultdict(set)
    objects = list(release.public_objects)
    for obj in objects:
        if not isinstance(obj, RespondentEvent):
            continue
        state = str(obj.typed_state)
        states[state] += 1
        question = str(dict(obj.native_question_ref).get("object_id", "UNKNOWN"))
        by_question[question][state] += 1
        respondent = str(dict(obj.scoped_respondent_ref).get("object_id", "UNKNOWN"))
        by_respondent[respondent].add(question)
    max_items = max((len(value) for value in by_respondent.values()), default=0)
    three_plus = sum(1 for value in by_respondent.values() if len(value) >= 3)
    return (dict(sorted(states.items())),
            {key: dict(sorted(value.items())) for key, value in sorted(by_question.items())},
            len(by_respondent), max_items, three_plus)


def execute_source(source_id: str, *, library: SourceConfigLibrary,
                   source_root: str | Path, state_root: str | Path | None = None,
                   allow_decode: bool = True) -> SourceExecutionResult:
    started = time.time()
    reasons: list[str] = []
    config = library.load_original(source_id)
    selection = library.select(source_id, source_root=source_root)
    resolution = selection.get("source_resolution") or {}
    if resolution.get("status") != "RESOLVED_UNDER_EFFECTIVE_ROOT":
        raise Original35ExecutionError(
            "SOURCE_PATH_UNRESOLVED:" + str(resolution.get("status")))
    path = Path(resolution["resolved_source_path"])
    if not path.is_file():
        raise Original35ExecutionError("SOURCE_NOT_PRESENT_HERE:" + source_id)
    plan = build_original35_operation_plan(
        [config.document], source_presence={source_id: True},
        require_all35=False)
    row = plan.rows[0]
    if not allow_decode:
        return SourceExecutionResult(
            source_id=source_id, status="MANIFEST_ONLY", source_sha256=row.source_sha256,
            config_path=selection.get("original_config_path"),
            source_format=selection.get("source_format"), row_count=0,
            physical_slots=len(row.physical_slots),
            response_slots=row.response_slot_count,
            operation_counts=row.counts, c11_release_ref=None,
            c11_object_count=0, raw_state_counts={}, question_state_counts={},
            respondent_count=0, max_events_per_respondent=0,
            respondents_with_3plus_items=0, repository_ref=None,
            elapsed_seconds=time.time() - started, maxrss_bytes=_maxrss(),
            reasons=("MANIFEST_ONLY_NOT_DECODED",))
    fmt = str(selection.get("source_format") or "").upper()
    encoding = _encoding(config)
    try:
        if fmt == "SAV":
            incidence = decode_sav(path, encoding=encoding)
        elif fmt == "DTA":
            incidence = decode_dta(path, encoding=encoding)
        else:
            raise Original35ExecutionError("SOURCE_FORMAT_UNSUPPORTED:" + fmt)
        if incidence.source_sha256 != row.source_sha256:
            raise Original35ExecutionError("SOURCE_SHA_MISMATCH_AFTER_DECODE:" + source_id)
        release = build_validated_c11_release_from_config(config, incidence=incidence)
        repository, _repo_release = build_source_backed_c11_repository_from_config(
            config, incidence)
        raw_states, question_states, respondents, max_items, three_plus = _raw_products(release)
        release_ref = release.release_ref.as_dict()
    except Exception as exc:
        reason = type(exc).__name__ + ":" + str(exc)
        return SourceExecutionResult(
            source_id=source_id, status="C11_RELEASE_REFUSED",
            source_sha256=row.source_sha256,
            config_path=selection.get("original_config_path"),
            source_format=fmt, row_count=0,
            physical_slots=len(row.physical_slots),
            response_slots=row.response_slot_count,
            operation_counts=row.counts, c11_release_ref=None,
            c11_object_count=0, raw_state_counts={}, question_state_counts={},
            respondent_count=0, max_events_per_respondent=0,
            respondents_with_3plus_items=0, repository_ref=None,
            elapsed_seconds=time.time() - started, maxrss_bytes=_maxrss(),
            reasons=(reason,))
    result = SourceExecutionResult(
        source_id=source_id, status="ORIGINAL_C11_RELEASE_EXECUTED",
        source_sha256=incidence.source_sha256,
        config_path=selection.get("original_config_path"),
        source_format=fmt, row_count=incidence.row_count,
        physical_slots=len(row.physical_slots), response_slots=row.response_slot_count,
        operation_counts=row.counts, c11_release_ref=release_ref,
        c11_object_count=len(list(release.public_objects)),
        raw_state_counts=raw_states, question_state_counts=question_states,
        respondent_count=respondents, max_events_per_respondent=max_items,
        respondents_with_3plus_items=three_plus,
        repository_ref=getattr(repository, "repository_id", None),
        elapsed_seconds=time.time() - started, maxrss_bytes=_maxrss(),
        reasons=tuple(reasons))
    if state_root is not None:
        target = Path(state_root) / (source_id + ".json")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result.material(), indent=2, sort_keys=True) + "\n",
                          encoding="utf8")
    return result




class _RecordingResolver:
    """Delegate unchanged admission calls while capturing exact decision material."""

    def __init__(self, inner: Any) -> None:
        self.inner = inner
        self.captured: list[dict[str, Any]] = []

    def resolve_current(self, request: Any) -> Any:
        from dataclasses import asdict
        decision = self.inner.resolve_current(request)
        self.captured.append(asdict(decision))
        return decision


def _joint_frontier_for_pair(plan: Any, source_id: str, pair: Any,
                             inventory: Any, policy: Any,
                             base_frontier: Any) -> tuple[Any, tuple[Any, ...]]:
    target_id = pair.item_ids[0]
    conditioner_id = pair.conditioner_item_id
    targets = (OccurrenceKey(item_id=conditioner_id),
               OccurrenceKey(item_id=target_id))
    by_key = inventory.by_key()
    if any(key not in by_key for key in targets):
        raise Original35ExecutionError("JOINT_TARGET_NOT_IN_INVENTORY")
    if pair.measure_kind != "RAW_OBSERVED_SAMPLE":
        raise Original35ExecutionError("WEIGHTED_REQUEST_NOT_AUTHORIZED")
    expected_measure = {
        "kind": "SAMPLE", "weight_ref": None, "design_ref": None,
        "estimand": "RAW_OBSERVED_SAMPLE", "variance_policy": "NONE",
    }
    measure_matches = [
        m for m in inventory.measure_plans
        if m.kind == expected_measure["kind"]
        and m.weight_ref == expected_measure["weight_ref"]
        and m.design_ref == expected_measure["design_ref"]
        and m.estimand == expected_measure["estimand"]
        and m.variance_policy == expected_measure["variance_policy"]]
    if not measure_matches:
        raise Original35ExecutionError("RAW_SAMPLE_MEASURE_MISSING")
    if len(measure_matches) != 1:
        raise Original35ExecutionError("RAW_SAMPLE_MEASURE_AMBIGUOUS")
    measure = measure_matches[0]
    target_roles = tuple(by_key[key].target_role for key in targets)
    disposition, reasons, risk_refs = role_disposition(
        inventory, policy, targets=targets, target_roles=target_roles,
        conditions=(), conditioner_roles=(), claim_class="JOINT",
        condition_mode="AND", measure=measure)
    if disposition != ELIGIBLE:
        raise Original35ExecutionError(
            "JOINT_REQUEST_NOT_ELIGIBLE:" + ",".join(reasons))
    direction = policy.direction_for(target_roles, (), "JOINT")
    used = [by_key[key] for key in targets]
    form_scope = sorted(set.intersection(*(set(item.forms) for item in used)))
    operation = make_operation(
        inventory=inventory, policy=policy, claim_class="JOINT",
        targets=targets, target_roles=target_roles, conditions=(),
        conditioner_roles=(), condition_mode="AND", unit=used[0].unit,
        topology=used[0].topology, measure=measure,
        risk_set_ref=(risk_refs[0] if risk_refs else None),
        risk_set_refs=risk_refs,
        direction_ref=(direction.direction_ref if direction else None),
        form_scope=form_scope, scope=source_id,
        disposition=disposition, reasons=reasons,
        native_support="PENDING",
        administration_states=sorted({item.administration for item in used}),
        aliases=(pair.operation_id,))
    operations = (operation,)
    class_counts = Counter(op.claim_class for op in operations)
    disposition_counts = Counter(op.disposition for op in operations)
    ids = tuple(op.op_id for op in operations)
    frontier = ScientificFrontier(
        schema=FRONTIER_SCHEMA, inventory_id=inventory.inventory_id,
        inventory_hash=inventory.content_hash, policy_id=policy.policy_id,
        policy_hash=policy.content_hash, policy_grade=policy.grade,
        source_identity=base_frontier.source_identity,
        operations=operations,
        inventory_ledger=inventory_ledger(inventory, policy),
        class_counts=dict(sorted(class_counts.items())),
        disposition_counts=dict(sorted(disposition_counts.items())),
        execution_counts={NOT_STARTED: 1},
        result_counts={UNKNOWN: 1}, deferred=(), unknown=(), excluded=(),
        budget_state="EXPLICIT_PLANNED", pending_operation_ids=(),
        partition_size=64,
        partition_root=content_hash({"operation_ids": list(ids),
                                     "partition_size": 64}),
        partition_count=1, maximum_bounds=dict(policy.bounds),
        u_item_root=None, u_unit_root=None, u_app_root=None,
        e_pre_count=1,
        e_pre_root=content_hash([operation.identity_material()]),
        e_pre_cause=None)
    return frontier, targets


def execute_requested_two_target_joints(plan: Any, *, bundle: Any,
                                        source_id: str,
                                        requested_operation_ids: Any,
                                        requested_conditioner_values: Any | None = None,
                                        as_of: str, host: str,
                                        purpose: str) -> list[dict[str, Any]]:
    """Execute an explicit caller-selected batch of F2 pair/value requests."""
    if (isinstance(requested_operation_ids, (str, bytes))
            or not isinstance(requested_operation_ids, (tuple, list))
            or not requested_operation_ids
            or any(not isinstance(x, str) or not x for x in requested_operation_ids)):
        raise Original35ExecutionError(
            "EXPLICIT_REQUESTED_F2_OPERATION_IDS_REQUIRED")
    if requested_conditioner_values is None:
        value_specs = [None] * len(requested_operation_ids)
    else:
        if (isinstance(requested_conditioner_values, (str, bytes))
                or not isinstance(requested_conditioner_values, (tuple, list))
                or len(requested_conditioner_values) != len(requested_operation_ids)):
            raise Original35ExecutionError(
                "REQUESTED_CONDITIONER_VALUES_ALIGNMENT_REQUIRED")
        value_specs = []
        for values in requested_conditioner_values:
            if (isinstance(values, (str, bytes))
                    or not isinstance(values, (tuple, list))
                    or not values
                    or any(not isinstance(x, str) or not x for x in values)):
                raise Original35ExecutionError(
                    "REQUESTED_CONDITIONER_VALUES_REQUIRED")
            value_specs.append(tuple(values))
    request_keys = []
    for requested_id, values in zip(requested_operation_ids, value_specs):
        key = (requested_id, values)
        if key in request_keys:
            raise Original35ExecutionError("DUPLICATE_REQUESTED_OPERATION_VALUE")
        request_keys.append(key)
    inventory, policy, base_frontier = build_frontier_inputs_from_plan(
        plan, source_id=source_id)
    by_id = {op.operation_id: op for op in plan.operations
             if op.source_id == source_id}
    results: list[dict[str, Any]] = []
    for requested_id, requested_values in zip(requested_operation_ids, value_specs):
        pair = by_id.get(requested_id)
        if pair is None:
            results.append({"requested_operation_id": requested_id,
                            "conditioner_values": list(requested_values or ()),
                            "status": "REFUSED",
                            "code": "REQUESTED_OPERATION_NOT_IN_PLAN"})
            continue
        if (pair.kind != OPERATION_F2 or pair.status != EXECUTABLE
                or pair.route_status != "ELIGIBLE_APPLICABLE"
                or not pair.conditioner_item_id):
            results.append({"requested_operation_id": requested_id,
                            "conditioner_values": list(requested_values or ()),
                            "status": "REFUSED",
                            "code": "REQUESTED_OPERATION_NOT_ELIGIBLE_F2"})
            continue
        conditioner_values = (tuple(requested_values)
                              if requested_values is not None
                              else tuple(pair.conditioner_values))
        if (not conditioner_values
                or any(value not in pair.conditioner_values
                       for value in conditioner_values)):
            results.append({"requested_operation_id": requested_id,
                            "conditioner_values": list(conditioner_values),
                            "status": "REFUSED",
                            "code": "REQUESTED_CONDITIONER_VALUE_NOT_IN_PLAN"})
            continue
        try:
            joint_frontier, targets = _joint_frontier_for_pair(
                plan, source_id, pair, inventory, policy, base_frontier)
            alias_bundle = _bundle_with_plan_aliases(
                plan, source_id, bundle, joint_frontier)
            compilation = compile_governed_frontier(
                bundle=alias_bundle, inventory=inventory, policy=policy,
                frontier=joint_frontier, as_of=as_of, host=host,
                purpose=purpose)
            result = execute_governed_frontier(
                compilation=compilation,
                source_factory=lambda _ref: bundle.physical_stream)
        except Exception as exc:
            results.append({"requested_operation_id": requested_id,
                            "status": "REFUSED",
                            "code": type(exc).__name__ + ":" + str(exc)})
            continue
        native = result.native_execution.native_result
        query_by_key = {q.ref.key: q for q in native.executed_queries}
        fact_rows = []
        for fact in native.empirical_facts:
            qref = exact_ref(fact.empirical_query_spec_ref,
                             "fact.empirical_query_spec_ref")
            query = query_by_key.get(qref.key)
            if query is None:
                continue
            topology = query.target_arity_and_topology or {}
            if topology.get("arity") != 2:
                continue
            fact_rows.append({
                "fact": fact,
                "query": query,
                "fact_ref": fact.ref.as_dict(),
                "query_ref": query.ref.as_dict(),
            })
        results.append({
            "requested_operation_id": requested_id,
            "conditioner_values": list(conditioner_values),
            "status": "OK" if fact_rows else "REFUSED",
            "code": None if fact_rows else "TWO_TARGET_FACT_NOT_PRODUCED",
            "conditioner_item_id": pair.conditioner_item_id,
            "target_item_id": pair.item_ids[0],
            "joint_operation_id": joint_frontier.operations[0].op_id,
            "joint_target_order": [key.item_id for key in targets],
            "compilation_hash": compilation.content_hash,
            "fact_refs": [row["fact_ref"] for row in fact_rows],
            "query_refs": [row["query_ref"] for row in fact_rows],
            "result": result,
            "fact_rows": fact_rows,
        })
    return results


def execute_two_target_joint_from_plan(plan: Any, *, bundle: Any,
                                        source_id: str,
                                        requested_operation_ids: Any,
                                        requested_conditioner_values: Any | None = None,
                                        as_of: str, host: str,
                                        purpose: str) -> list[dict[str, Any]]:
    return execute_requested_two_target_joints(
        plan, bundle=bundle, source_id=source_id,
        requested_operation_ids=requested_operation_ids,
        requested_conditioner_values=requested_conditioner_values,
        as_of=as_of, host=host, purpose=purpose)


def write_requested_joint_transport(results: Any, *, source_id: str,
                                    state_root: str | Path,
                                    producer_permission_ceiling: Any) -> dict[str, Any]:
    """Write per-request envelopes and supporting request identities."""
    if (isinstance(producer_permission_ceiling, (str, bytes))
            or not isinstance(producer_permission_ceiling, (tuple, list))
            or not producer_permission_ceiling
            or any(not isinstance(x, str) or not x.strip()
                   for x in producer_permission_ceiling)):
        raise Original35ExecutionError(
            "EXPLICIT_PRODUCER_PERMISSION_CEILING_REQUIRED")
    ceiling = tuple(producer_permission_ceiling)
    requests = []
    for entry in results:
        row = {k: v for k, v in entry.items()
               if k not in {"result", "fact_rows"}}
        if entry.get("status") == "OK":
            envelopes = [envelope_material(
                fact=fact_row["fact"], query=fact_row["query"],
                producer_permission_ceiling=ceiling)
                for fact_row in entry["fact_rows"]]
            row["envelopes"] = envelopes
            row["envelope_count"] = len(envelopes)
        else:
            row["envelopes"] = []
            row["envelope_count"] = 0
        requests.append(row)
    target = Path(state_root) / (source_id + ".requested_joint_transport.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    staged = target.with_name(target.name + ".staged-tmp")
    try:
        staged.write_text(json.dumps({
            "schema": "PRE553_ORIGINAL35_REQUESTED_JOINT_TRANSPORT@1.0.0",
            "source_id": source_id,
            "producer_permission_ceiling": list(ceiling),
            "requests": requests,
            "raw_respondent_rows_included": False,
            "native_science_authority": False,
        }, indent=2, sort_keys=True) + "\n", encoding="utf8")
        os.replace(staged, target)
    finally:
        if staged.exists():
            staged.unlink()
    return {"path": str(target), "request_count": len(requests),
            "ok_count": sum(1 for r in requests if r["status"] == "OK"),
            "refused_count": sum(1 for r in requests if r["status"] != "OK")}


def consume_requested_joint_transport(path: str | Path, *,
                                       producer_permission_ceiling: Any) -> dict[str, Any]:
    """Cold D consumer: apply exact requested conditioner-value selection."""
    from rawlsing_next.pre553_field_forge_empirical_ingress import ingest_envelope
    if (isinstance(producer_permission_ceiling, (str, bytes))
            or not isinstance(producer_permission_ceiling, (tuple, list))
            or not producer_permission_ceiling
            or any(not isinstance(x, str) or not x.strip()
                   for x in producer_permission_ceiling)):
        raise Original35ExecutionError(
            "EXPLICIT_PRODUCER_PERMISSION_CEILING_REQUIRED")
    ceiling = tuple(producer_permission_ceiling)
    document = json.loads(Path(path).read_text(encoding="utf8"))
    if document.get("schema") != "PRE553_ORIGINAL35_REQUESTED_JOINT_TRANSPORT@1.0.0":
        raise Original35ExecutionError("REQUESTED_JOINT_TRANSPORT_SCHEMA_REQUIRED")
    if tuple(document.get("producer_permission_ceiling") or ()) != ceiling:
        raise Original35ExecutionError("REQUESTED_JOINT_PERMISSION_MISMATCH")
    consumed = []
    for request in document.get("requests", ()):
        entry = {
            "requested_operation_id": request.get("requested_operation_id"),
            "conditioner_item_id": request.get("conditioner_item_id"),
            "target_item_id": request.get("target_item_id"),
            "conditioner_values": list(request.get("conditioner_values") or ()),
            "status": request.get("status"),
            "code": request.get("code"),
            "backing_fact_refs": list(request.get("fact_refs") or ()),
            "backing_query_refs": list(request.get("query_refs") or ()),
            "joint_operation_id": request.get("joint_operation_id"),
            "selections": [],
        }
        if request.get("status") != "OK":
            consumed.append(entry)
            continue
        envelopes = list(request.get("envelopes") or ())
        if not envelopes:
            entry["status"] = "REFUSED"
            entry["code"] = "REQUESTED_JOINT_ENVELOPE_MISSING"
            consumed.append(entry)
            continue
        responses = [ingest_envelope(envelope) for envelope in envelopes]
        profile_rows = []
        for response in responses:
            if response.get("state") != "CONDITIONAL_SUPPORT_PROFILE":
                entry["status"] = "REFUSED"
                entry["code"] = response.get("refusal_code") or "E_PROFILE_REFUSED"
                break
            profile = response.get("profile") or {}
            profile_rows.extend(profile.get("conditional_count_profile") or [])
        if entry["status"] != "OK":
            consumed.append(entry)
            continue
        by_condition = {str(row.get("condition_state")): row for row in profile_rows}
        requested_values = tuple(str(v) for v in entry["conditioner_values"])
        unmatched = [value for value in requested_values
                     if value not in by_condition]
        if unmatched:
            entry["status"] = "REFUSED"
            entry["code"] = "REQUESTED_CONDITIONER_VALUE_NOT_IN_PROFILE"
            entry["unmatched_values"] = unmatched
            consumed.append(entry)
            continue
        for value in requested_values:
            row = by_condition[value]
            selection_material = {
                "requested_operation_id": entry["requested_operation_id"],
                "conditioner_item_id": entry["conditioner_item_id"],
                "target_item_id": entry["target_item_id"],
                "conditioner_value": value,
                "backing_query_refs": entry["backing_query_refs"],
                "backing_fact_refs": entry["backing_fact_refs"],
                "selected_row": row,
                "producer_permission_ceiling": list(ceiling),
            }
            entry["selections"].append({
                "conditioner_value": value,
                "selected_result_id": "urn:rawlsing:pre553:original35:requested-joint-selection:" +
                semantic_hash(selection_material),
                "condition_denominator_support": row.get("condition_denominator_support"),
                "target_counts": list(row.get("target_counts") or ()),
                "selection_material": selection_material,
            })
        consumed.append(entry)
    return {
        "schema": "PRE553_ORIGINAL35_REQUESTED_JOINT_CONSUMPTION@1.0.0",
        "source_id": document.get("source_id"),
        "producer_permission_ceiling": list(ceiling),
        "requests": consumed,
        "raw_respondent_rows_included": False,
        "native_science_authority": False,
    }


def write_field_forge_envelopes(result: Any, *, source_id: str,
                                state_root: str | Path,
                                producer_permission_ceiling: Any) -> dict[str, Any]:
    """Persist exact existing fact/query envelopes; never mint permission."""
    if (isinstance(producer_permission_ceiling, (str, bytes))
            or not isinstance(producer_permission_ceiling, (tuple, list))
            or not producer_permission_ceiling
            or any(not isinstance(value, str) or not value.strip()
                   for value in producer_permission_ceiling)):
        raise Original35ExecutionError(
            "EXPLICIT_PRODUCER_PERMISSION_CEILING_REQUIRED")
    producer_permission_ceiling = tuple(producer_permission_ceiling)
    native = getattr(getattr(result, "native_execution", None), "native_result", None)
    if native is None:
        raise Original35ExecutionError("GOVERNED_NATIVE_RESULT_REQUIRED")
    facts = tuple(getattr(native, "empirical_facts", ()))
    catalog = getattr(getattr(result, "compilation", None), "runtime_catalog", None)
    queries = {query.ref.key: query for query in getattr(catalog, "queries", ())}
    queries.update({query.ref.key: query
                    for query in getattr(native, "executed_queries", ())})
    envelopes = []
    missing = []
    for fact in facts:
        qref = exact_ref(fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref")
        query = queries.get(qref.key)
        if query is None:
            missing.append(qref.as_dict())
            continue
        envelopes.append(envelope_material(
            fact=fact, query=query,
            producer_permission_ceiling=producer_permission_ceiling))
    if missing:
        raise Original35ExecutionError(
            "FIELD_FORGE_QUERY_REF_MISSING:" + json.dumps(missing, sort_keys=True))
    target = Path(state_root) / (source_id + ".field_forge_envelopes.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    staged = target.with_name(target.name + ".staged-tmp")
    try:
        staged.write_text(json.dumps({
            "schema": "PRE553_ORIGINAL35_E_TRANSPORT@1.0.0",
            "source_id": source_id,
            "fact_count": len(facts),
            "envelope_count": len(envelopes),
            "missing_query_refs": missing,
            "envelopes": envelopes,
            "raw_respondent_rows_included": False,
            "producer_permission_ceiling": list(producer_permission_ceiling),
            "native_science_authority": False,
        }, indent=2, sort_keys=True) + "\n", encoding="utf8")
        os.replace(staged, target)
    finally:
        if staged.exists():
            staged.unlink()
    return {"path": str(target), "fact_count": len(facts),
            "envelope_count": len(envelopes), "missing_query_refs": missing}


def execute_native_compiler_source(source_id: str, *, library: SourceConfigLibrary,
                                   source_root: str | Path, host: str,
                                   purpose: str, as_of: str,
                                   max_items: int | None = None,
                                   resolver: Any | None = None,
                                   state_root: str | Path | None = None,
                                   producer_permission_ceiling: Any | None = None) -> dict[str, Any]:
    """Run full supported explicit plan through CURRENT governed compiler/facts.

    Source bytes are opened only through the existing current source-read
    decision/resolver path. No raw incidence or fabricated resolver can bypass it.
    """
    started = time.time()
    config = library.load_original(source_id)
    doc = config.document
    selection = library.select(source_id, source_root=source_root)
    resolution = selection["source_resolution"]
    if resolution.get("status") != "RESOLVED_UNDER_EFFECTIVE_ROOT":
        raise Original35ExecutionError("SOURCE_PATH_UNRESOLVED")
    path = Path(resolution["resolved_source_path"])
    if resolver is None:
        raise Original35ExecutionError(
            "CURRENT_SOURCE_READ_DECISION_REQUIRED_BEFORE_IO")
    plan = build_original35_operation_plan(
        [doc], source_presence={source_id: True}, require_all35=False)
    selected_ops = []
    for op in plan.operations:
        if (op.source_id == source_id
                and op.kind in {OPERATION_F1, OPERATION_F2, OPERATION_F3H}
                and op.status == EXECUTABLE
                and op.route_status == "ELIGIBLE_APPLICABLE"
                and op.response_values):
            selected_ops.append(op)
    if max_items is not None:
        if type(max_items) is not int or max_items < 1:
            raise Original35ExecutionError("DIAGNOSTIC_MAX_ITEMS_INVALID")
        selected_ops = selected_ops[:max_items]
    if not selected_ops:
        raise Original35ExecutionError("NO_ROUTE_QUALIFIED_SUBSTANTIVE_ITEMS")
    bindings: dict[str, tuple[str, str, str]] = {}
    for op in selected_ops:
        for original_id, physical in zip(op.item_ids, op.source_variable_codes):
            prior = bindings.get(physical)
            if prior is not None and prior[0] != original_id:
                raise Original35ExecutionError(
                    "ORIGINAL_ID_PHYSICAL_CODE_CONFLICT:" + physical)
            bindings[physical] = (original_id, op.unit, op.topology)
    selected_names = set(bindings)
    coordinate = None
    for slot in doc.get("coordinate_slots", []):
        name = slot["slot"]["name"]
        if name not in selected_names:
            coordinate = name
            break
    if coordinate is None:
        key_slot = (doc.get("respondents") or {}).get("source_native_key_slot")
        if isinstance(key_slot, Mapping) and key_slot.get("name") not in selected_names:
            coordinate = key_slot.get("name")
    if coordinate is None:
        raise Original35ExecutionError("COORDINATE_FACT_ABSENT_NOT_GUESSED")
    fmt = str(selection.get("source_format") or "").upper()
    consumer_use = "D_ORIGINAL35_NATIVE_EXECUTION"
    semantic_scope = ("RAW_OBSERVED_SAMPLE",)
    request = source_read_request_from_config(
        config, host=host, purpose=purpose, consumer_use=consumer_use,
        semantic_use_scope=semantic_scope)
    reader = reader_configuration_from_config(config)
    recording = _RecordingResolver(resolver)
    incidence = decode_with_source_read_permission(
        source_path=path, request=request, resolver=recording, reader=reader)
    if not recording.captured:
        incidence.close()
        raise Original35ExecutionError("SOURCE_READ_DECODE_DECISION_NOT_OBSERVED")
    decode_decision = recording.captured[0]
    if incidence.source_sha256 != doc["binding"]["source_sha256"]:
        incidence.close()
        raise Original35ExecutionError("SOURCE_SHA_MISMATCH_AFTER_DECODE")
    selected_variables = tuple(sorted(selected_names | {coordinate}))
    stream = bounded_physical_cell_stream(
        incidence, include_variables=selected_variables)
    package = NativeSourcePackage(
        source=NativeSourceIdentity(
            source_id=source_id, family=str(doc["identity"]["family"]),
            wave=str(doc["identity"]["wave"]),
            canonical_filename=str(doc["identity"]["source_artifact_id"]),
            declared_sha256=incidence.source_sha256, source_format=fmt,
            expected_rows=incidence.row_count),
        selected=tuple(NativeSourceRule(
            implementation_id=bindings[name][0], source_variable_code=name,
            unit=bindings[name][1]) for name in sorted(bindings)),
        coordinate_variable=coordinate,
        study_product_id=str(doc["identity"]["study_product_id"]),
        release_id=str(doc["identity"]["release_id"]),
        instrument_release_id=str(doc["identity"]["instrument_release_id"]),
        as_of=as_of)
    bundle = materialize_native_preimages(package=package, incidence=stream)
    non_f1 = any(op.kind != OPERATION_F1 for op in selected_ops)
    if non_f1:
        compilation = bind_governed_frontier(
            plan, bundle=bundle, source_id=source_id, as_of=as_of,
            host=host, purpose=purpose)
        result = execute_governed_frontier(
            compilation=compilation,
            source_factory=lambda _ref: bundle.physical_stream)
        expected_operation_ids = list(compilation.expected_operation_ids)
        expected_candidate_ids = list(compilation.expected_candidate_ids)
        fact_refs = [ref.as_dict() for ref in result.fact_refs]
        receipt_refs = [ref.as_dict() for ref in result.receipt_refs]
        anti_join = dict(result.anti_join)
        operation_anti_join = dict(result.operation_anti_join)
        ledger_hash = result.content_hash
        compilation_material = compilation.material()
        transport = None
    else:
        compilation = compile_universal_workload(
            bundle=bundle, as_of=as_of, host=host, purpose=purpose)
        result = execute_universal_workload(
            compilation=compilation,
            source_factory=lambda _ref: bundle.physical_stream)
        expected_operation_ids = [
            op.operation_id for op in compilation.operations
            if op.status == "COMPILED"]
        expected_candidate_ids = []
        fact_refs = [ref.as_dict() for ref in result.fact_refs]
        receipt_refs = [ref.as_dict() for ref in result.receipt_refs]
        anti_join = dict(result.anti_join())
        operation_anti_join = {"no_drop_ok": result.anti_join()["no_drop_ok"]}
        ledger_hash = compilation.content_hash
        compilation_material = compilation.material()
        transport = None
    after_decision = recording.resolve_current(request)
    from dataclasses import asdict
    if asdict(after_decision) != decode_decision:
        incidence.close()
        raise Original35ExecutionError(
            "SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER")
    if (non_f1 and state_root is not None
            and producer_permission_ceiling is not None):
        transport = write_field_forge_envelopes(
            result, source_id=source_id, state_root=state_root,
            producer_permission_ceiling=producer_permission_ceiling)
    material = {
        "schema": "PRE553_ORIGINAL35_NATIVE_COMPILER_RESULT@1.0.0",
        "source_id": source_id, "source_sha256": incidence.source_sha256,
        "selected_items": sorted(bindings),
        "selected_original_ids": {name: bindings[name][0] for name in bindings},
        "selected_units": {name: bindings[name][1] for name in bindings},
        "selected_topologies": {name: bindings[name][2] for name in bindings},
        "coordinate_variable": coordinate,
        "source_custody": dict(incidence.source_custody or {}),
        "diagnostic_max_items": max_items,
        "row_count": incidence.row_count,
        "compilation_hash": compilation.content_hash,
        "compilation": compilation_material,
        "expected_operation_ids": expected_operation_ids,
        "expected_candidate_ids": expected_candidate_ids,
        "fact_refs": fact_refs,
        "receipt_refs": receipt_refs,
        "anti_join": anti_join,
        "operation_anti_join": operation_anti_join,
        "ledger_hash": ledger_hash,
        "field_forge_transport": transport,
        "elapsed_seconds": round(time.time() - started, 3),
        "maxrss_bytes": _maxrss(), "native": False,
    }
    incidence.close()
    if state_root is not None:
        target = Path(state_root) / (source_id + ".native.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(material, indent=2, sort_keys=True) + "\n",
                          encoding="utf8")
    return material


def execute_all(*, library: SourceConfigLibrary, source_root: str | Path,
                state_root: str | Path | None = None,
                allow_decode: bool = True) -> list[SourceExecutionResult]:
    results = []
    for source_id in library.source_ids():
        results.append(execute_source(
            source_id, library=library, source_root=source_root,
            state_root=state_root, allow_decode=allow_decode))
    return results


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--binding", default=str(DEFAULT_BINDING))
    parser.add_argument("--state", default=".local-logs/pyat-universal35/d-state")
    args = parser.parse_args(argv)
    binding = load_runtime_binding(args.binding)
    root = binding["USER_ORIGINAL35_DATA_ROOT"]
    library = SourceConfigLibrary(index_path="source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json",
                                  source_root=root)
    ids = library.source_ids() if args.all else tuple(args.source)
    if not ids:
        parser.error("--source or --all required")
    for source_id in ids:
        result = execute_source(source_id, library=library, source_root=root,
                                state_root=args.state,
                                allow_decode=not args.manifest_only)
        print(json.dumps(result.material(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DEFAULT_BINDING", "Original35ExecutionError", "SCHEMA",
    "SourceExecutionResult", "execute_all",
    "execute_native_compiler_source", "execute_requested_two_target_joints",
    "consume_requested_joint_transport", "execute_source",
    "execute_two_target_joint_from_plan", "write_field_forge_envelopes",
    "write_requested_joint_transport",
    "load_runtime_binding", "main",
]
