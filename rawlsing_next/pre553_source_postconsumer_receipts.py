"""S1-E #997 P1: exact postconsumer operation/fate receipt conservation.

READ-ONLY postconsumer sidecar. Does not alter Q2's preconsumer handoff,
mint an issuer or backdate receipts. The caller supplies a REAL accepted S2-D
saved admission and REAL BatchExecutionRunner (actual execution or legally
restored receipts). Every positive Batch output is checked by re-executing its
native cold reader and comparing exact result references under live CURRENT.
An operation is marked evidenced only if its S1-C expected candidate IDs
match re-executed I05 native receipts through R03's original candidate
anti-join, or its exact issued query units are complete. A shared Batch
COMPLETED state alone never marks every scientific operation COMPLETE. All negative/pending states survive verbatim.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, UnitExecutionReceipt,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_issued_workload import (
    NativeWorkload, IssuedWorkloadRecord, admit,
)
from rawlsing_next.pre553_native_workload_binding import (
    TestOnlyIssuedWorkload, _ref as _historical_test_only_ref,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import EstateReceipt
from rawlsing_next.pre553_source_i02_handoff import SourceI02Handoff
from rawlsing_next.pre553_universal_workload import (
    GovernedFrontierCompilation, GOVERNED_FRONTIER_SCHEMA,
)
from rawlsing_next.universal_grammar.native_map import native_receipt_anti_join

SCHEMA = "PYAT997_S1E_SOURCEFREE_SAVED_POSTCONSUMER_FATES@1"


class SourceReceiptJoinError(ValueError):
    """Missing, forged, stale or semantically unjoined evidence is a refusal."""


@dataclass(frozen=True)
class PostconsumerFateJoin:
    schema: str
    source_sha256: str
    issued_decision_ref: ExactRef
    issued_envelope_sha256: str
    release_ref: ExactRef
    estate_manifest_sha256: str
    rows: tuple[Mapping[str, Any], ...]
    audit: Mapping[str, Any]
    result_hash: str


def _key(value: Any) -> str:
    if isinstance(value, Mapping):
        if set(("kind", "object_id", "content_hash")) - set(value):
            raise SourceReceiptJoinError("INCOMPLETE_EXACT_QUERY_REFERENCE")
        value = {k: value[k] for k in ("kind", "object_id", "content_hash")}
    return exact_ref(value).key


def _deep_freeze(value: Any) -> Any:
    """Return an immutable independent view of all nested receipt material.

    A Q2 SourceI02Handoff is a frozen dataclass but its row dictionaries are
    not deeply immutable. Reusing nested preimage dictionaries here would
    allow a caller to change an already-hashed postconsumer result after G5.
    """
    if isinstance(value, Mapping):
        return MappingProxyType({k: _deep_freeze(v) for k, v in value.items()})
    if isinstance(value, (tuple, list)):
        return tuple(_deep_freeze(v) for v in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_deep_freeze(v) for v in value)
    return value


def _results(result: Any, kind: str) -> tuple[str, ...]:
    values = result.facts if kind == "QUERY" else result.receipts
    return tuple(sorted(ref.ref.key for ref in values))



def _verify_realized_q2_body_witness(source_fate: Mapping[str, Any]) -> None:
    """Check per-key Q2 emission before using its favorable summary flag.

    This validates Q2 internal consistency, not independent source authority.
    The original source-pass recorded all emission, occurrence and routing
    details; a mutable aggregate or Boolean cannot override that evidence.
    """
    if (source_fate.get("disposition") != "ELIGIBLE"
            or source_fate.get("source_realized") is not True):
        return
    witnesses = source_fate.get("source_realization")
    if not isinstance(witnesses, (list, tuple)) or not witnesses:
        raise SourceReceiptJoinError("Q2_REALIZED_OPERATION_WITHOUT_BODIES")
    present_keys: set[str] = set()
    supported_keys: set[str] = set()
    unresolved_response_keys: set[str] = set()
    # Original Q2 refuses a realized response key whose emitted response
    # slots all have zero eligible routed rows. Preserve that denominator
    # rule in the postconsumer boundary; B checked only the routing flag.
    emitted_response_routes: dict[str, list[int]] = {}
    for witness in witnesses:
        if not isinstance(witness, Mapping):
            raise SourceReceiptJoinError("Q2_REALIZATION_WITNESS_INVALID")
        key = witness.get("key")
        emitted = witness.get("emitted")
        occurrence = witness.get("occurrence_realized")
        routing_unresolved = witness.get("routing_unresolved", False)
        if (not isinstance(key, str) or not key
                or type(emitted) is not int or emitted < 0
                or type(occurrence) is not bool
                or type(routing_unresolved) is not bool):
            raise SourceReceiptJoinError("Q2_REALIZATION_WITNESS_INVALID")
        family = witness.get("family")
        if family not in {
            "RespondentEvent", "EmpiricalCoordinateFact", "WeightMeasureFact"
        }:
            raise SourceReceiptJoinError("Q2_REALIZATION_WITNESS_INVALID")
        routing_states = witness.get("routing_states")
        if (not isinstance(routing_states, Mapping)
                or any(not isinstance(name, str) or type(value) is not int
                       or value < 0 for name, value in routing_states.items())):
            raise SourceReceiptJoinError("Q2_REALIZATION_ROUTING_CENSUS_INVALID")
        routable_rows = witness.get("routable_rows")
        if family == "RespondentEvent":
            if (type(routable_rows) is not int or routable_rows < 0
                    or routable_rows != routing_states.get("ELIGIBLE_APPLICABLE", 0)
                    or routing_unresolved != any(
                        state in routing_states for state in (
                            "ROUTING_UNKNOWN", "RULE_UNAVAILABLE"
                        )
                    )):
                raise SourceReceiptJoinError("Q2_REALIZATION_ROUTING_CENSUS_DRIFT")
            if emitted > 0:
                emitted_response_routes.setdefault(key, []).append(routable_rows)
        elif (routing_states or routable_rows is not None or routing_unresolved):
            raise SourceReceiptJoinError("Q2_REALIZATION_NONRESPONSE_ROUTING_DRIFT")
        present_keys.add(key)
        if emitted > 0 and occurrence and not routing_unresolved:
            supported_keys.add(key)
        if (witness.get("family") == "RespondentEvent"
                and emitted > 0 and routing_unresolved):
            unresolved_response_keys.add(key)
    if any(not any(rows > 0 for rows in routes)
           for routes in emitted_response_routes.values()):
        raise SourceReceiptJoinError("Q2_REALIZATION_ZERO_ROUTABLE_DENOMINATOR")
    if (present_keys != supported_keys or unresolved_response_keys
            or source_fate.get("unrealized_keys")
            or source_fate.get("routing_unresolved_keys")):
        raise SourceReceiptJoinError("Q2_REALIZATION_BODY_OR_ROUTING_CONTRADICTION")



def _verify_original_governed_issuer(
    compilation: GovernedFrontierCompilation,
    workload: NativeWorkload,
    record: IssuedWorkloadRecord,
    *, host: str, purpose: str,
) -> None:
    """Conserve the EXISTING R03 compiler's one-DISCOVERY issuance contract.

    ``compile_governed_frontier`` calls ``build_test_only_discovery_workload``:
    one DISCOVERY, no QUERY, and exact deterministic issuer refs derived from
    its own plan hash + as_of. A caller may replace the dataclass's ``issued``
    member and even provide a matching test-only resolver; comparing those
    two forged objects is not an original-compiler proof. Reconstruct the
    historical producer contract using its existing _ref, not a new issuer.

    This check is specific to the existing governed-frontier compiler schema.
    The separate ``compile_universal_workload`` single-target QUERY path is
    not silently imported into S1-E governed-frontier acceptance. A future
    governed QUERY compiler needs its own explicit versioned contract.
    """
    issued = compilation.issued
    if (compilation.schema != GOVERNED_FRONTIER_SCHEMA
            or type(issued) is not TestOnlyIssuedWorkload
            or issued.workload != workload or issued.record != record
            or (host, purpose) != (compilation.host, compilation.purpose)):
        raise SourceReceiptJoinError("ORIGINAL_GOVERNED_COMPILATION_REQUIRED")
    plan_hash = compilation.plan.content_hash
    authorities = compilation.runtime_catalog.discovery_authorities
    if len(authorities) != 1:
        raise SourceReceiptJoinError("R03_COMPILER_DISCOVERY_CENSUS_DRIFT")
    discovery = authorities[0].ref
    prefix = "r03-discovery-" + plan_hash[:16]
    expected_decision = _historical_test_only_ref(
        "TEST_ONLY_DECISION", f"{prefix}-{compilation.as_of}",
    )
    expected_source_permission = _historical_test_only_ref(
        "TEST_ONLY_SOURCE_PERMISSION", prefix,
    )
    expected_science_permission = _historical_test_only_ref(
        "TEST_ONLY_SCIENTIFIC_PERMISSION", prefix,
    )
    # Do not allow an admitted catalog QUERY to become a compiler-issued
    # governed operation. The current compiler emits precisely ONE discovery.
    if (workload.requests != ()
            or workload.discoveries != (discovery,)
            or record.expected_jobs != (("DISCOVERY", discovery.key, ""),)
            or workload.catalog != compilation.runtime_catalog
            or workload.expected_frontier_root != plan_hash
            or record.expected_frontier_root != plan_hash):
        raise SourceReceiptJoinError("R03_COMPILER_ISSUED_JOB_OR_PLAN_DRIFT")
    if (workload.decision_ref != expected_decision
            or record.decision_ref != expected_decision
            or record.source_permission_ref != expected_source_permission
            or record.scientific_permission_refs != (expected_science_permission,)
            or record.host != compilation.host
            or record.purpose != compilation.purpose):
        raise SourceReceiptJoinError("R03_COMPILER_ORIGINAL_ISSUER_IDENTITY_DRIFT")
    # Original builder derives the prospective U root from the original
    # inventory and administered native-item census, NOT a caller's record.
    # It is still sourcefree; no original-source right is conferred here.
    try:
        import json
        desc = json.loads(workload.descriptor)
        native_item_ids = desc["native_item_ids"]
        if (not isinstance(native_item_ids, list)
                or any(not isinstance(item, str) for item in native_item_ids)):
            raise ValueError("invalid original native item ids")
        expected_u_root = semantic_hash({
            "inventory": compilation.inventory_hash,
            "source_sha256": compilation.source_sha256,
            "native_item_ids": native_item_ids,
        })
    except (KeyError, TypeError, ValueError, UnicodeError) as exc:
        raise SourceReceiptJoinError("R03_COMPILER_DESCRIPTOR_DRIFT") from exc
    if (dict(issued.descriptor) != desc
            or issued.envelope_sha256 != record.envelope_sha256
            or workload.original_u_root != expected_u_root
            or record.original_u_root != expected_u_root
            or workload.source_factory_ref != _historical_test_only_ref(
                "SOURCE_FACTORY", compilation.source_sha256,
            )
            or record.native_universe_refs != (
                workload.projection.universes[0].ref,
            )
            or record.original_wave_identity is not None
            or workload.original_wave_identity is not None):
        raise SourceReceiptJoinError("R03_COMPILER_SOURCE_U_ENVELOPE_DRIFT")


def join_saved_source_operation_fates(
    *, handoff: SourceI02Handoff, estate_receipt: EstateReceipt,
    admission: SavedC11Admission, compilation: GovernedFrontierCompilation,
    workload: NativeWorkload, resolver: Any,
    host: str, purpose: str, runner: BatchExecutionRunner,
    allow_test_only: bool = True,
) -> PostconsumerFateJoin:
    """Verify actual saved-native receipts and join to every original operation.

    No original35/native-scientific promotion is possible; only sourcefree
    TEST_ONLY is emitted. A positive marks an individual verified QUERY,
    not an unproved scientific interpretation or universal source eligibility.
    """
    if (type(handoff) is not SourceI02Handoff
            or type(estate_receipt) is not EstateReceipt
            or type(admission) is not SavedC11Admission
            or type(compilation) is not GovernedFrontierCompilation
            or type(workload) is not NativeWorkload
            or type(runner) is not BatchExecutionRunner):
        raise SourceReceiptJoinError("EXACT_ACCEPTED_PRODUCER_AND_NATIVE_TYPES_REQUIRED")
    if runner.repository is not admission:
        raise SourceReceiptJoinError("BATCH_RUNNER_NOT_BOUND_TO_SAVED_ADMISSION")
    if (handoff.roots != estate_receipt.i02
            or admission.i02 != handoff.roots
            or admission.manifest_sha256 != estate_receipt.manifest_sha256
            or admission.release_ref != estate_receipt.reconstructed_v1_release_ref
            or admission.estate_path != estate_receipt.path
            or admission.source_ref.key != handoff.roots.source
            or admission.replay_ref.key != handoff.roots.replay):
        raise SourceReceiptJoinError("Q2_SAVED_REPLAY_AND_RELEASE_IDENTITY_DRIFT")
    if (compilation.source_sha256 != handoff.source_sha256
            or workload.projection.expected_source_sha256 != handoff.source_sha256
            or compilation.issued.workload != workload
            or admission.binding_receipt().runtime_catalog != workload.catalog.receipt()):
        raise SourceReceiptJoinError("ISSUED_WORKLOAD_AND_SOURCE_IDENTITY_DRIFT")
    # Q2 independently certified the complete S1-C inventory/frontier
    # before opening the physical source; native R03 compiles that same
    # original frontier. A shared source SHA and matching operation labels
    # do NOT establish that the two products came from the same frontier.
    # Bind their original, non-pruned content hash before any issued receipt
    # can be associated with the source-side fates.
    census = handoff.census_audit
    if (not isinstance(census, Mapping)
            or not isinstance(compilation.frontier_hash, str)
            or census.get("frontier_hash") != compilation.frontier_hash):
        raise SourceReceiptJoinError("Q2_R03_ORIGINAL_FRONTIER_HASH_DRIFT")
    original_operation_count = len(handoff.operation_fates)
    original_fate_counts = dict(Counter(
        row["disposition"] for row in handoff.operation_fates
    ))
    if (census.get("source_candidate_count") != original_operation_count
            or census.get("scientific_fate_count") != original_operation_count
            or census.get("eligible_count") != original_fate_counts.get("ELIGIBLE", 0)
            or census.get("fate_counts") != original_fate_counts):
        raise SourceReceiptJoinError("Q2_ORIGINAL_FROZEN_FATE_CENSUS_DRIFT")
    admission.check_current()
    record = admit(
        workload, resolver, host=host, purpose=purpose,
        allow_test_only=allow_test_only,
    )
    if (type(record) is not IssuedWorkloadRecord
            or record.scope != "TEST_ONLY_SOURCEFREE"
            or record != compilation.issued.record):
        raise SourceReceiptJoinError("TEST_ONLY_CURRENT_ISSUER_NOT_EXACT")
    # The CURRENT resolver authenticates the record it was asked for, not
    # whether a caller replaced a compiler output with its own record.
    _verify_original_governed_issuer(
        compilation, workload, record, host=host, purpose=purpose,
    )
    # Q2's frozen handoff contains mutable nested preimages. Its source-
    # realization claim must agree with the source-side witness and the
    # independently recorded Q2 operation-source census before any native
    # result can be promoted. A compiler ELIGIBLE disposition alone is not
    # proof that this source physically realized the operation.
    source_audit = handoff.census_audit.get("operation_source_antijoin")
    if not isinstance(source_audit, Mapping):
        raise SourceReceiptJoinError("Q2_SOURCE_REALIZATION_AUDIT_MISSING")
    source_states = Counter()
    for source_fate in handoff.operation_fates:
        _verify_realized_q2_body_witness(source_fate)
        eligible = source_fate["disposition"] == "ELIGIBLE"
        realized = source_fate.get("source_realized")
        if type(realized) is not bool:
            raise SourceReceiptJoinError("Q2_SOURCE_REALIZATION_CONTRADICTION")
        state = (
            "ELIGIBLE_REALIZED" if eligible and realized
            else "ELIGIBLE_TYPED_HOLD" if eligible
            else "HELD_OR_UNKNOWN_SOURCE_STATE"
        )
        reader_state = (
            "HOLD_ROUTING_OR_BODY_UNRESOLVED" if eligible and not realized
            else "HOLD_DEPENDENCY_LINUX_PROC_SELF_FD_AND_SEALED_BODY_RELEASE"
        )
        if (source_fate.get("operation_source_state") != state
                or source_fate.get("native_first_reader_state") != reader_state
                or (realized and (
                    source_fate.get("routing_unresolved_keys")
                    or source_fate.get("unrealized_keys")
                ))):
            raise SourceReceiptJoinError("Q2_SOURCE_REALIZATION_CONTRADICTION")
        source_states["operation_count"] += 1
        source_states["source_realized_operation_count"] += int(realized)
        if eligible:
            source_states["eligible_operation_count"] += 1
            source_states["eligible_realized_count"] += int(realized)
            source_states["unrealized_eligible_count"] += int(not realized)
        else:
            source_states["held_operation_count"] += 1
    for key in (
        "operation_count", "eligible_operation_count", "eligible_realized_count",
        "held_operation_count", "source_realized_operation_count",
        "unrealized_eligible_count",
    ):
        if source_audit.get(key) != source_states[key]:
            raise SourceReceiptJoinError("Q2_SOURCE_REALIZATION_AUDIT_DRIFT")
    manifest = runner.manifest
    expected_jobs = set(record.expected_jobs)
    units_by_ref = {unit.unit_ref.key: unit for unit in manifest.units}
    if len(units_by_ref) != len(manifest.units):
        raise SourceReceiptJoinError("DUPLICATE_BATCH_UNIT")
    request_predicates = {r.query_ref.key: r.predicate_ref for r in workload.requests}
    jobs = set()
    for unit in manifest.units:
        if tuple(unit.release_refs) != (admission.release_ref,):
            raise SourceReceiptJoinError("BATCH_UNIT_OTHER_RELEASE")
        if record.decision_ref not in unit.semantic_input_refs:
            raise SourceReceiptJoinError("BATCH_UNIT_NOT_ISSUED_TO_DECISION")
        if unit.job_kind == "QUERY":
            pred = request_predicates.get(unit.job_ref.key)
            if pred is None:
                raise SourceReceiptJoinError("UNISSUED_SAVED_QUERY")
            jobs.add(("QUERY", unit.job_ref.key, pred.key))
        elif unit.job_kind == "DISCOVERY":
            if unit.job_ref not in workload.discoveries:
                raise SourceReceiptJoinError("UNISSUED_SAVED_DISCOVERY")
            jobs.add(("DISCOVERY", unit.job_ref.key, ""))
        else:
            raise SourceReceiptJoinError("BATCH_JOB_KIND_INVALID")
    if jobs != expected_jobs or len(jobs) != len(manifest.units):
        raise SourceReceiptJoinError("ISSUED_JOB_VS_SAVED_MANIFEST_ANTI_JOIN")

    by_unit: dict[str, list[UnitExecutionReceipt]] = {}
    for receipt in runner.receipts:
        if type(receipt) is not UnitExecutionReceipt:
            raise SourceReceiptJoinError("NONNATIVE_RECEIPT_TYPE")
        if (receipt.manifest_hash != manifest.manifest_hash
                or receipt.unit_ref.key not in units_by_ref):
            raise SourceReceiptJoinError("RECEIPT_MANIFEST_UNIT_DRIFT")
        by_unit.setdefault(receipt.unit_ref.key, []).append(receipt)
    completed: dict[str, UnitExecutionReceipt] = {}
    output_refs: dict[str, tuple[str, ...]] = {}
    # Actual native I05 receipt rows are collected across *all* issued
    # discovery jobs. R03's candidate universe is the whole frontier, not an
    # arbitrary single discovery's partial result. Pending units must remain
    # pending rather than triggering a false no-drop failure.
    discovery_candidates: dict[str, Any] = {}
    discovery_batch_receipts: dict[str, str] = {}
    all_discovery_receipts: list[Any] = []
    expected_candidate_ids = {
        candidate["candidate_id"] for candidate in compilation.plan.expected_candidates
    }
    if len(expected_candidate_ids) != len(compilation.plan.expected_candidates):
        raise SourceReceiptJoinError("DUPLICATE_EXPECTED_NATIVE_CANDIDATE")
    for unit in manifest.units:
        history = sorted(by_unit.get(unit.unit_ref.key, ()),
                         key=lambda r: r.attempt_index)
        if len({r.attempt_index for r in history}) != len(history):
            raise SourceReceiptJoinError("DUPLICATE_RECEIPT_ATTEMPT")
        if not history or history[-1].state != "COMPLETED":
            continue
        receipt = history[-1]
        if (not receipt.execution_performed or receipt.executor_ref is None
                or admission.replay_ref not in receipt.provenance_refs):
            raise SourceReceiptJoinError("NATIVE_COMPLETION_LACKS_REPLAY_EVIDENCE")
        admission.check_current()
        if unit.job_kind == "QUERY":
            observed = admission.execute_i03(
                query_ref=unit.job_ref,
                predicate_ref=request_predicates[unit.job_ref.key],
            )
        else:
            observed = admission.execute_i05(
                discovery_authority_ref=unit.job_ref,
            )
        obtained = _results(observed, unit.job_kind)
        if unit.job_kind == "DISCOVERY":
            for native in observed.receipts:
                identity = native.candidate_identity
                candidate_id = identity.get("candidate_id") if isinstance(identity, Mapping) else None
                if not isinstance(candidate_id, str) or not candidate_id:
                    raise SourceReceiptJoinError("NATIVE_CANDIDATE_ID_MISSING")
                if candidate_id not in expected_candidate_ids:
                    raise SourceReceiptJoinError("UNISSUED_NATIVE_DISCOVERY_CANDIDATE")
                if candidate_id in discovery_candidates:
                    raise SourceReceiptJoinError("DUPLICATE_NATIVE_DISCOVERY_CANDIDATE")
                discovery_candidates[candidate_id] = native
                discovery_batch_receipts[candidate_id] = receipt.receipt_ref.key
                all_discovery_receipts.append(native)
        retained = tuple(sorted(ref.key for ref in receipt.result_refs))
        if obtained != retained:
            raise SourceReceiptJoinError("RECEIPT_NATIVE_FIRST_CONSUMER_OUTPUT_DRIFT")
        completed[unit.unit_ref.key] = receipt
        output_refs[unit.unit_ref.key] = obtained
        admission.check_current()

    discovery_units = tuple(
        unit for unit in manifest.units if unit.job_kind == "DISCOVERY"
    )
    if discovery_units and all(
        unit.unit_ref.key in completed for unit in discovery_units
    ):
        # Only the fully issued discovery set can satisfy the global R03
        # native-candidate/rule no-drop court.
        audit = native_receipt_anti_join(
            compilation.plan, tuple(all_discovery_receipts),
        )
        if audit.get("no_drop_ok") is not True:
            raise SourceReceiptJoinError(
                "NATIVE_DISCOVERY_CANDIDATE_ANTI_JOIN_FAILED"
            )
    else:
        # An interrupted/missing discovery cannot be evidence that an S1-C
        # operation completed. Keep eligible operations explicitly pending.
        discovery_candidates.clear()
        discovery_batch_receipts.clear()

    # S1-C lowering's per-operation query lineage; no invented operation
    # labels derived from arbitrary output statistics or from discovery rank.
    query_unit = {
        u.job_ref.key: u for u in manifest.units if u.job_kind == "QUERY"
    }
    plan_by_op: dict[str, Any] = {}
    for entry in compilation.plan.records:
        if entry.operation_id in plan_by_op:
            raise SourceReceiptJoinError("DUPLICATE_LOWERED_OPERATION")
        plan_by_op[entry.operation_id] = entry
    # The compiled frontier independently retains the complete S1-C fate
    # and claim-class census. The preconsumer handoff may not be edited after
    # publication to turn HELD/UNKNOWN into an apparently issued ELIGIBLE row.
    dispositions = compilation.operation_dispositions
    claim_classes = compilation.operation_claim_classes
    if (not isinstance(dispositions, Mapping)
            or not isinstance(claim_classes, Mapping)
            or set(dispositions) != {
                r["operation_id"] for r in handoff.operation_fates
            }
            or set(claim_classes) != set(dispositions)):
        raise SourceReceiptJoinError("COMPLETE_ISSUED_FATE_CENSUS_REQUIRED")
    output_rows = []
    all_ops = set()
    positively_linked = 0
    pending_eligible = 0
    fate_counts: Counter[str] = Counter()
    for old in handoff.operation_fates:
        operation_id = old["operation_id"]
        if operation_id in all_ops:
            raise SourceReceiptJoinError("DUPLICATE_Q2_SOURCE_OPERATION")
        all_ops.add(operation_id)
        source = old["source_preimage"]
        # S1-C source_id names the original source roster; for TEST_ONLY
        # R157 the sealed Q2 artifact_id is R157_FIXTURE:<fixture_id>.
        # These are distinct identity axes and MUST NOT be equated.
        if (not isinstance(source["source_id"], str)
                or not source["source_id"].strip()
                or source["source_sha256"] != handoff.source_sha256
                or source["operation_hash"] != old["operation_hash"]
                or source["operation_hash_matches"] is not True
                or old.get("issued_receipt_refs") != ()):
            raise SourceReceiptJoinError("SOURCE_OPERATION_PROVENANCE_OR_PREISSUE_DRIFT")
        original_measure = source.get("measure")
        measure_keys = (
            "measure_kind", "measure_id", "weight_ref",
            "estimand", "design_ref", "variance_policy",
        )
        if (not isinstance(original_measure, Mapping)
                or set(original_measure) != set(measure_keys)
                or any(original_measure[k] != old[k] for k in measure_keys)):
            raise SourceReceiptJoinError("Q2_MEASURE_PREIMAGE_CONTRADICTION")
        state = old["disposition"]
        if (state != dispositions[operation_id]
                or old["claim_class"] != claim_classes[operation_id]):
            raise SourceReceiptJoinError("Q2_OPERATION_FATE_OR_CLAIM_PROMOTED")
        fate_counts[state] += 1
        entry = plan_by_op.get(operation_id)
        refs: tuple[str, ...] = ()
        result_refs: tuple[str, ...] = ()
        batch_refs: tuple[str, ...] = ()
        joined_state = "NONELIGIBLE_FATE_PRESERVED"
        if state == "ELIGIBLE":
            joined_state = "ELIGIBLE_PENDING_VERIFIED_NATIVE_RECEIPT"
            if (old.get("source_realized") is True and entry is not None
                    and entry.status == "SUPPORTED" and entry.expected_candidate_keys
                    and set(entry.expected_candidate_keys) <= set(discovery_candidates)):
                selected_candidates = [
                    discovery_candidates[c] for c in sorted(set(entry.expected_candidate_keys))
                ]
                refs = tuple(sorted(r.ref.key for r in selected_candidates))
                result_refs = tuple(sorted({
                    _key(fact) for r in selected_candidates
                    for fact in r.empirical_fact_refs
                }))
                batch_refs = tuple(sorted({
                    discovery_batch_receipts[c] for c in entry.expected_candidate_keys
                }))
                joined_state = "TEST_ONLY_SAVED_NATIVE_DISCOVERY_RECEIPTED"
                positively_linked += 1
            elif (old.get("source_realized") is True and entry is not None
                    and entry.status == "SUPPORTED" and entry.query_refs):
                qids = {_key(ref) for ref in entry.query_refs}
                if all(q in query_unit for q in qids):
                    selected = [query_unit[q] for q in sorted(qids)]
                    if all(u.unit_ref.key in completed for u in selected):
                        refs = tuple(sorted(
                            completed[u.unit_ref.key].receipt_ref.key for u in selected
                        ))
                        result_refs = tuple(sorted(
                            ref for u in selected
                            for ref in output_refs[u.unit_ref.key]
                        ))
                        batch_refs = refs
                        if not refs:
                            raise SourceReceiptJoinError("EMPTY_POSITIVE_RECEIPT_SET")
                        joined_state = "TEST_ONLY_SAVED_NATIVE_QUERY_RECEIPTED"
                        positively_linked += 1
            if not refs:
                pending_eligible += 1
        # Preserve Q2 rows without mutation, including HELD/UNKNOWN,
        # E_pre absence, routing, denominator, weight/design and source fates.
        row = dict(old)
        row["postconsumer_state"] = joined_state
        row["postconsumer_receipt_refs"] = refs
        row["postconsumer_native_output_refs"] = result_refs
        row["postconsumer_batch_receipt_refs"] = batch_refs
        row["postconsumer_decision_ref"] = record.decision_ref.key
        row["postconsumer_release_ref"] = admission.release_ref.key
        row["postconsumer_saved_manifest_sha256"] = admission.manifest_sha256
        output_rows.append(_deep_freeze(row))
    if len(all_ops) != len(handoff.operation_fates):
        raise SourceReceiptJoinError("OPERATION_ANTI_JOIN")
    if not set(plan_by_op).issubset(all_ops):
        raise SourceReceiptJoinError("LOWERING_OPERATION_OUTSIDE_SOURCE_CENSUS")
    admission.check_current()
    second = admit(workload, resolver, host=host, purpose=purpose,
                   allow_test_only=allow_test_only)
    if second != record:
        raise SourceReceiptJoinError("CURRENT_ISSUER_CHANGED_DURING_JOIN")
    summary = {
        "scope": "TEST_ONLY_SOURCEFREE_NOT_NATIVE_SCIENCE",
        "operation_count": len(output_rows),
        "preconsumer_fate_counts": dict(sorted(fate_counts.items())),
        "positive_native_linked_operations": positively_linked,
        "native_discovery_candidates_exactly_joined": len(discovery_candidates),
        "pending_eligible_operations": pending_eligible,
        "batch_units": len(manifest.units),
        "native_completed_units_rechecked": len(completed),
        "issue_grants_created": 0,
        "preconsumer_handoff_unchanged": True,
        "independent_g5": "NOT_RUN",
    }
    rows_material = [dict(row) for row in output_rows]
    digest = semantic_hash({
        "schema": SCHEMA, "source_sha256": handoff.source_sha256,
        "issuer_decision_ref": record.decision_ref.as_dict(),
        "issuer_envelope_sha256": record.envelope_sha256,
        "saved_manifest_sha256": admission.manifest_sha256,
        "release_ref": admission.release_ref.as_dict(),
        "rows": rows_material, "audit": summary,
    })
    return PostconsumerFateJoin(
        SCHEMA, handoff.source_sha256,
        record.decision_ref, record.envelope_sha256,
        admission.release_ref, admission.manifest_sha256,
        tuple(output_rows), MappingProxyType(summary), digest,
    )


__all__ = [
    "SCHEMA", "SourceReceiptJoinError", "PostconsumerFateJoin",
    "join_saved_source_operation_fates",
]
