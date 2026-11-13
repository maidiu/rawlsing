"""Q2 S1-E — issued native Batch fact from the Q2 body tee.

The fixture is engineering/sourcefree only: R157-shaped nonrespondent SAV bytes,
a TEST_ONLY query/predicate authority, and an engineering correction of two
fixture omissions (routing authority kind and canonical value spelling).  It is
not original35 science or a production CURRENT permission.

Unlike the earlier legacy comparator, this native path consumes the exact
``C11SourceReleaseCandidate`` reconstructed from the Q2 body tee during the same
source read.  There is no second fixture decode and no legacy
``build_validated_c11_release_from_config`` full build.  The S1-C frontier is
compiled by the existing ``compile_governed_frontier`` owner, the existing
test-only issuance path admits the workload, and the existing
``CarrierNeutralResearchExecutor`` executes I05/Batch against the same Q2 body
repository.  A deliberate body change changes the Batch facts; restoring the
exact body restores them.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import sqlite3

import pytest

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    BatchManifest,
    BatchUnitSpec,
    ExecutionOutcome,
    ExecutorBinding,
)
from rawlsing_next.pre553_c11_ingest import (
    C11SourceReleaseCandidate,
    build_candidate_replay_manifest,
    validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import (
    C11IntegrityError,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    RespondentEvent,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_issued_workload import admit
from rawlsing_next.pre553_native_workload_binding import (
    TestOnlyDecisionResolver,
)
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig,
    build_governed_c11_projection,
    # Kept as module attributes for the unchanged independent G5 lineage probe.
    build_validated_c11_release_from_config,
    decode_fixture_config,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
)
from rawlsing_next.pre553_source_native_preimage_adapter import (
    AdministeredItem,
    NativePreimageBundle,
)
from rawlsing_next.pre553_universal_workload import compile_governed_frontier
from rawlsing_next.tests.test_pyat960_s1e_support import (
    RecordingBodySink,
    build,
    source_fixture,
)
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import (
    _freeze_packet,
)
from rawlsing_next.tests.test_universal_grammar import _frontier

_NATIVE_AS_OF = "2026-11-12"
_NATIVE_HOST = "q2-s1e-b"
_NATIVE_PURPOSE = "Q2_G2_NATIVE_ISSUED_BATCH"

def _native_document(document):
    """Correct only sourcefree fixture omissions; no scientific widening."""
    doc = deepcopy(document)
    for snapshot in doc["authority"]["snapshots"]:
        if snapshot["authority_id"] == "S1B-ROUTING-AUTH":
            snapshot["authority_kind"] = "ROUTING_RISK_SET"
    for slot in doc["response_slots"]:
        for value in slot["values"]:
            if value.get("raw_value") in (0.0, 1.0):
                value["canonical_value"] = str(int(value["raw_value"]))
    return doc


def _native_fixture(tmp_path: Path, *, values=(0.0, 1.0, 0.0, 1.0, 0.0), policy_kwargs=None):
    """Build the sourcefree Q2 fixture with the TEST_ONLY native preimages.

    Two engineering-only fixture corrections are explicit: the routing
    authority kind is ROUTING_RISK_SET, and the test inventory risk-set tag is
    aligned to the exact C11 routing risk-set ref.  Neither changes source
    meaning or original science; both make the existing S1-C compiler and I05
    owner able to consume the Q2 projection without a second source read.
    """
    fixture = source_fixture(
        tmp_path / "native", values=values,
        policy_kwargs=policy_kwargs or {"j": 1, "k": 1, "d": 0})
    document = _native_document(fixture["document"])
    config = SourceConfig(document)
    projection = build_governed_c11_projection(config)
    risk_set_ref = exact_ref(
        projection.routing[0].risk_set_ref, "risk_set_ref")
    occurrences = tuple(
        replace(occurrence, risk_set_refs=(risk_set_ref.key,))
        for occurrence in fixture["inventory"].occurrences
    )
    inventory = replace(
        fixture["inventory"],
        occurrences=occurrences,
        risk_set_refs=(risk_set_ref.key,),
    )
    frontier = _frontier(inventory, fixture["policy"])
    census = _freeze_packet(frontier)
    fixture = dict(fixture)
    fixture.update(
        document=document,
        config=config,
        projection=projection,
        inventory=inventory,
        frontier=frontier,
        census=census,
    )
    return fixture


def _bodies_by_family(sink: RecordingBodySink):
    by_family: dict[str, list[object]] = {}
    for family, obj in sink.bodies:
        by_family.setdefault(family, []).append(obj)
    return by_family


def _section_or_absence(
    by_family, sink: RecordingBodySink, family: str, *, events=None
):
    if family == "RespondentEvent" and events is not None:
        return tuple(events)
    if by_family.get(family):
        return tuple(by_family[family])
    return TypedAbsence(sink.absences.get(family, "NOT_APPLICABLE"))


def _sealed_body_release(
    handoff,
    sink: RecordingBodySink,
    projection,
    *,
    event_mutator=None,
):
    """Build the existing sealed C11 release from the Q2 body tee only."""
    by_family = _bodies_by_family(sink)
    events = None
    if event_mutator is not None:
        events = event_mutator(tuple(by_family.get("RespondentEvent", ())))
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=handoff.manifest,
        empirical_universes=_section_or_absence(
            by_family, sink, "EmpiricalUniverse"),
        respondent_identities=_section_or_absence(
            by_family, sink, "RespondentIdentity"),
        question_variable_bindings=_section_or_absence(
            by_family, sink, "QuestionVariableBinding"),
        respondent_events=_section_or_absence(
            by_family, sink, "RespondentEvent", events=events),
        routing_eligibility_facts_or_exact_rules=_section_or_absence(
            by_family, sink, "RoutingEligibilityFact"),
        empirical_coordinate_facts=_section_or_absence(
            by_family, sink, "EmpiricalCoordinateFact"),
        weight_measure_facts_or_typed_absence=_section_or_absence(
            by_family, sink, "WeightMeasureFact"),
        authority_snapshots=_section_or_absence(
            by_family, sink, "AuthoritySnapshot"),
        source_universe_relations_or_explicit_distinct_default=(
            _section_or_absence(
                by_family, sink, "SourceUniverseRelation")),
        predicate_replay_bindings_when_retained_objects_require_them=(
            _section_or_absence(
                by_family, sink, "EmpiricalPredicateReplayBinding")),
        comparator_replay_bindings_or_typed_deferred_state=(
            _section_or_absence(
                by_family, sink, "ComparatorReplayBinding")),
        discovery_branch_replay_bindings_or_typed_deferred_state=(
            _section_or_absence(
                by_family, sink, "DiscoveryBranchReplayBinding")),
        structural_admission_replay_bindings_or_typed_not_applicable_state=(
            _section_or_absence(
                by_family, sink, "StructuralAdmissionReplayBinding")),
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=projection.replay_authority_ref,
        deterministic_tie_order_rules_ref=projection.tie_order_ref,
        replay_protocol_version=projection.replay_protocol_version,
    )
    return validate_c11_source_release(
        replace(candidate, candidate_replay_manifest=replay))


def _native_source(fixture, config, sink, release):
    projection = build_governed_c11_projection(config)
    return {
        "universe": projection.universes[0],
        "respondents": {row.ref.key: row for row in projection.respondents},
        "qrefs": {"q101": projection.questions[0].native_question_ref},
        "risk_refs": {"R": projection.routing[0].risk_set_ref},
        "authorities": projection.authority_snapshots,
        "source_auth": projection.authority_snapshots[0],
        "repo": C11Repository((release,)),
        "release_ref": release.release_ref,
        "projection": projection,
        "sink": sink,
        "body_release_built_from_q2_tee": True,
    }


def _build_native(tmp_path: Path, fixture, document, name: str):
    """Build Q2 handoff plus the native body repository from its body tee.

    Return shape is kept compatible with the independent G5 probe.  The second
    return value is the sealed ``C11LogicalRelease`` reconstructed from the Q2
    body tee, not a separately decoded legacy release.
    """
    config = SourceConfig(document)
    sink = RecordingBodySink()
    handoff = build(
        tmp_path, fixture, name=name, config=config, body_sink=sink)
    projection = build_governed_c11_projection(config)
    release = _sealed_body_release(handoff, sink, projection)
    source = _native_source(fixture, config, sink, release)
    return handoff, release, source


def _native_bundle(handoff, fixture, projection, release):
    risk_set_ref = exact_ref(
        projection.routing[0].risk_set_ref, "risk_set_ref")
    administered = (
        AdministeredItem(
            "Q2-BODY-q101", "q101", "ADMINISTERED",
            "TEST_ONLY_Q2_BODY_TEE", "person", "OUTCOME"),
        AdministeredItem(
            "Q2-BODY-country", "country", "ADMINISTERED",
            "TEST_ONLY_Q2_BODY_TEE", "person", "OUTCOME"),
    )
    return NativePreimageBundle(
        schema="PYAT_R56_NATIVE_PREIMAGE_BUNDLE@1.0.0",
        source_sha256=handoff.source_sha256,
        package_hash=semantic_hash({"q2_body": handoff.source_sha256}),
        projection=projection,
        # The S1-C compiler does not consume this field on the issued path;
        # the actual body is the sealed Q2 release above.  It is deliberately
        # empty rather than a second source read or a raw-cell corpus.
        physical_stream=ExactPhysicalCellStream(
            handoff.source_sha256, handoff.row_count, lambda: ()),
        release=release,
        administered=administered,
        held=(),
        excluded=(),
        unknown=(),
        bundle_hash=semantic_hash({
            "q2_body_source": handoff.source_sha256,
            "q2_body_release": release.release_ref.as_dict(),
        }),
        question_refs={
            "q101": projection.questions[0].native_question_ref,
            "country": projection.coordinate_slots[0].native_coordinate_ref,
        },
        risk_set_ref=risk_set_ref,
        respondent_rows=tuple(
            {"respondent_key": row.respondent_key, "ref": row.ref.key}
            for row in projection.respondents
        ),
        occurrence_bindings=(),
    )


def _compile_native(fixture, handoff, projection, release):
    return compile_governed_frontier(
        bundle=_native_bundle(handoff, fixture, projection, release),
        inventory=fixture["inventory"],
        policy=fixture["policy"],
        frontier=fixture["frontier"],
        as_of=_NATIVE_AS_OF,
        host=_NATIVE_HOST,
        purpose=_NATIVE_PURPOSE,
    )


def _execute_plan_i03(compilation, release, *, operation_id=None):
    """Execute one actual S1-C lowering-plan operation through I03.

    This is not a branch or ad-hoc query.  The query and predicate refs come
    from the existing ``compile_governed_frontier`` lowering records; the body
    repository is the sealed Q2 body-tee release.
    """
    repository = C11Repository((release,))
    executor = CarrierNeutralResearchExecutor(
        repository,
        (release.release_ref,),
        compilation.issued.workload.catalog,
    )
    for record in compilation.plan.records:
        if record.status != "SUPPORTED" or not record.query_refs:
            continue
        if operation_id is not None and record.operation_id != operation_id:
            continue
        for raw_query in record.query_refs:
            query_ref = exact_ref(
                {
                    key: raw_query[key]
                    for key in ("kind", "object_id", "content_hash")
                    if key in raw_query
                },
                "query_ref",
            )
            query = compilation.issued.workload.catalog.resolve_query_exact(
                query_ref)
            predicate_ref = exact_ref(
                query.condition_predicate_ref, "condition_predicate_ref")
            result = executor.execute_i03(
                query_ref=query_ref, predicate_ref=predicate_ref)
            assert len(result.facts) == 1
            fact = result.facts[0]
            if operation_id is None and fact.typed_state != "SUPPORTED":
                continue
            return record.operation_id, fact, query_ref
    return operation_id, None, None


def _execute_native_batch(compilation, release):
    repository = C11Repository((release,))
    admit(
        compilation.issued.workload,
        TestOnlyDecisionResolver(compilation.issued.record),
        host=_NATIVE_HOST,
        purpose=_NATIVE_PURPOSE,
        allow_test_only=True,
    )
    executor = CarrierNeutralResearchExecutor(
        repository,
        (release.release_ref,),
        compilation.issued.workload.catalog,
    )
    discovery_ref = compilation.issued.workload.discoveries[0]
    manifest = BatchManifest((
        BatchUnitSpec(
            "DISCOVERY",
            discovery_ref,
            (release.release_ref,),
            (compilation.issued.workload.decision_ref,),
        ),
    ))
    outputs: dict[str, object] = {}

    def execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        result = executor.execute_i05(
            discovery_authority_ref=unit.job_ref)
        outputs[unit.unit_hash] = result
        return ExecutionOutcome(
            tuple(receipt.ref for receipt in result.receipts),
            (release.replay_manifest.ref,
             compilation.issued.workload.decision_ref),
        )

    executor_ref = ExactRef(
        "S1E_Q2_BODY_DISCOVERY",
        "urn:pyat960:s1e:q2-body:"
        + compilation.issued.envelope_sha256,
        compilation.issued.envelope_sha256,
    )
    runner = BatchExecutionRunner(
        manifest=manifest, repository=repository)
    runner.run(executors={
        "DISCOVERY": ExecutorBinding(executor_ref, execute),
    })
    assert len(runner.receipts) == 1
    assert runner.receipts[0].state == "COMPLETED"
    assert runner.receipts[0].execution_performed is True
    native_result = outputs[manifest.units[0].unit_hash]
    return native_result, runner.receipts, manifest


def _fact_view(fact):
    fields = fact.semantic_fields
    return {
        "ref": fact.ref.key,
        "typed_state": fact.typed_state,
        "measure_kind": fields.get("measure_kind"),
        "raw": (
            fields.get("raw_numerator_support"),
            fields.get("raw_denominator_support"),
        ),
        "risk_set_ref": (
            exact_ref(fields["risk_set_ref"], "risk_set_ref").key
            if fields.get("risk_set_ref") is not None else None
        ),
    }


def _raw_supported_facts(facts):
    return tuple(
        fact for fact in facts
        if fact.typed_state == "SUPPORTED"
        and fact.semantic_fields.get("measure_kind") == "RAW"
        and (
            fact.semantic_fields.get("raw_numerator_support"),
            fact.semantic_fields.get("raw_denominator_support"),
        ) == (5, 5)
    )


def _record_ref_key(ref) -> str:
    if isinstance(ref, dict) or hasattr(ref, "keys"):
        ref = {
            key: ref[key]
            for key in ("kind", "object_id", "content_hash")
            if key in ref
        }
    return exact_ref(ref, "record_ref").key


def _fact_operation_candidates(compilation, fact) -> set[str]:
    """Map a discovery fact back to actual S1-C frontier lowering records.

    The discovery evaluator derives marginal/joint query objects from the
    lowering plan, so the fact's exact query ref need not equal the record's
    template ref.  Its condition atom does retain the record's predicate
    lineage; use that exact predicate and any exact query intersection.
    """
    fields = fact.semantic_fields
    predicate_key = None
    query_key = None
    if fields.get("condition_predicate_ref") is not None:
        predicate_key = exact_ref(
            fields["condition_predicate_ref"], "condition_predicate_ref").key
    if fields.get("empirical_query_spec_ref") is not None:
        query_key = exact_ref(
            fields["empirical_query_spec_ref"],
            "empirical_query_spec_ref").key
    found: set[str] = set()
    for record in compilation.plan.records:
        predicates = {
            _record_ref_key(ref)
            for ref in record.predicate_refs
        }
        queries = {
            _record_ref_key(ref)
            for ref in record.query_refs
        }
        if predicate_key in predicates or query_key in queries:
            found.add(record.operation_id)
    return found


def _mutate_first_event_to_dk(events):
    events = list(events)
    assert events
    event = events[0]
    fields = dict(event.semantic_fields)
    fields["response_state"] = "DK"
    fields["canonical_response_value_if_authorized"] = None
    events[0] = RespondentEvent(
        typed_state="DK",
        authority_snapshot_refs=event.authority_snapshot_refs,
        dependency_refs=event.dependency_refs,
        producer_replay_locator_or_reference_root=(
            event.producer_replay_locator_or_reference_root),
        **fields,
    )
    return tuple(events)


def test_s1e_issued_native_batch_consumes_q2_body_tee(tmp_path):
    fixture = _native_fixture(tmp_path)
    handoff, release, source = _build_native(
        tmp_path / "native", fixture, fixture["document"], "base.sqlite")
    projection = fixture["projection"]

    assert handoff.body_transport is not None
    assert source["sink"].counts["RespondentEvent"] == 5
    assert source["body_release_built_from_q2_tee"] is True
    assert handoff.stats.source_reads == 1
    assert handoff.stats.snapshot_acquisitions == 1
    assert handoff.stats.decode_calls == 1
    assert handoff.stats.full_c11_builds == 0
    assert handoff.stats.cell_passes == 1

    # The sealed body release is exactly the release reconstructed by the
    # direct Q2 certificate from the same one-read body; it is not a second
    # source decode or a legacy comparator.
    with sqlite3.connect(handoff.destination) as db:
        header = dict(db.execute("SELECT name, value FROM main.header"))
    assert release.release_ref.key == header["reconstructed_v1_release_ref"]
    assert release.replay_manifest.ref.key == header["reconstructed_v1_replay_ref"]
    assert release.release_ref != handoff.roots.release

    compilation = _compile_native(fixture, handoff, projection, release)
    frontier_ids = {op.op_id for op in fixture["frontier"].operations}
    assert compilation.expected_operation_ids
    assert set(compilation.expected_operation_ids) <= frontier_ids
    assert compilation.issued.record.scope == "TEST_ONLY_SOURCEFREE"
    assert compilation.issued.record.expected_jobs
    covered = (
        set(compilation.expected_operation_ids)
        | set(compilation.unsupported_operation_ids)
        | set(compilation.not_eligible_operation_ids)
        | set(compilation.pending_operation_ids)
    )
    assert covered == frontier_ids
    frontier_by_id = {op.op_id: op for op in fixture["frontier"].operations}
    assert any(
        frontier_by_id[op_id].measure_kind == "SAMPLE"
        for op_id in compilation.expected_operation_ids
    )
    assert compilation.operation_dispositions

    base_result, base_receipts, base_manifest = _execute_native_batch(
        compilation, release)
    base_facts = tuple(base_result.empirical_facts)
    assert base_facts
    supported = _raw_supported_facts(base_facts)
    assert supported
    assert any(
        view["risk_set_ref"].startswith("RISK_SET|urn:rawlsing:s1b:risk:q101|")
        for view in map(_fact_view, supported)
    )
    assert base_receipts[0].state == "COMPLETED"
    assert base_manifest.units[0].job_kind == "DISCOVERY"
    assert base_result.empirical_fact_refs
    base_fact_refs = tuple(fact.ref.key for fact in base_facts)

    # At least one supported fact maps back to an actual expected S1-C
    # frontier operation (not the old ad-hoc BRANCH-q2-native query).
    supported_operation_ids: set[str] = set()
    for fact in supported:
        supported_operation_ids |= _fact_operation_candidates(
            compilation, fact)
    expected_ids = set(compilation.expected_operation_ids)
    assert supported_operation_ids & expected_ids
    supported_operations = [
        frontier_by_id[op_id]
        for op_id in sorted(supported_operation_ids & expected_ids)
    ]
    assert any(
        operation.measure_kind == "SAMPLE"
        for operation in supported_operations
    )

    # Causal body severance: changing one Q2-emitted body event to DK changes
    # the native Batch fact refs.  No source re-read occurs.
    tampered = _sealed_body_release(
        handoff, source["sink"], projection,
        event_mutator=_mutate_first_event_to_dk,
    )
    assert tampered.release_ref != release.release_ref
    tampered_compilation = _compile_native(
        fixture, handoff, projection, tampered)
    tampered_result, tampered_receipts, _ = _execute_native_batch(
        tampered_compilation, tampered)
    tampered_fact_refs = tuple(
        fact.ref.key for fact in tampered_result.empirical_facts)
    assert tampered_fact_refs != base_fact_refs
    assert tampered_receipts[0].state == "COMPLETED"
    assert handoff.stats.source_reads == 1
    assert handoff.stats.decode_calls == 1
    assert handoff.stats.full_c11_builds == 0

    # Exact body restore reproduces the original sealed release and facts.
    restored = _sealed_body_release(
        handoff, source["sink"], projection)
    assert restored.release_ref == release.release_ref
    restored_compilation = _compile_native(
        fixture, handoff, projection, restored)
    restored_result, restored_receipts, _ = _execute_native_batch(
        restored_compilation, restored)
    assert tuple(
        fact.ref.key for fact in restored_result.empirical_facts
    ) == base_fact_refs
    assert restored_receipts[0].state == "COMPLETED"

    # The same plan operation also executes through the native I03 reader
    # (not only the Batch/I05 discovery path).  Its query/predicate refs are
    # actual S1-C lowering records, and the body is the same Q2 release.
    plan_operation_id, plan_fact, plan_query_ref = _execute_plan_i03(
        compilation, release)
    assert plan_operation_id in expected_ids
    assert plan_query_ref is not None
    assert plan_fact is not None
    assert plan_fact.typed_state == "SUPPORTED"
    assert (
        plan_fact.semantic_fields.get("raw_numerator_support"),
        plan_fact.semantic_fields.get("raw_denominator_support"),
    ) == (5, 5)
    assert frontier_by_id[plan_operation_id].measure_kind == "SAMPLE"

    # The native operation joins back to the exact returned handoff fate row;
    # this is a real operation/fate receipt, not only a frontier label.
    handoff_row = next(
        row for row in handoff.operation_fates
        if row["operation_id"] == plan_operation_id
    )
    assert handoff_row["measure_kind"] == (
        frontier_by_id[plan_operation_id].measure_kind)
    assert handoff_row["operation_hash"] == (
        frontier_by_id[plan_operation_id].canonical_hash)
    assert handoff_row["source_preimage"]["measure"]["measure_kind"] == (
        handoff_row["measure_kind"])
    assert base_receipts[0].receipt_ref.kind
    assert plan_fact.semantic_fields["empirical_query_spec_ref"]

    changed_plan_operation_id, changed_plan_fact, _ = _execute_plan_i03(
        tampered_compilation, tampered, operation_id=plan_operation_id)
    assert changed_plan_operation_id == plan_operation_id
    assert changed_plan_fact is not None
    assert (
        changed_plan_fact.ref != plan_fact.ref
        or changed_plan_fact.typed_state != plan_fact.typed_state
    )
    restored_plan_operation_id, restored_plan_fact, _ = _execute_plan_i03(
        restored_compilation, restored, operation_id=plan_operation_id)
    assert restored_plan_operation_id == plan_operation_id
    assert restored_plan_fact is not None
    assert restored_plan_fact.ref == plan_fact.ref
    assert (
        restored_plan_fact.semantic_fields.get("raw_numerator_support"),
        restored_plan_fact.semantic_fields.get("raw_denominator_support"),
    ) == (5, 5)


def test_s1e_native_body_severance_refuses_before_fact(tmp_path):
    fixture = _native_fixture(tmp_path)
    handoff, release, source = _build_native(
        tmp_path / "native", fixture, fixture["document"], "sever.sqlite")
    projection = fixture["projection"]
    by_family = _bodies_by_family(source["sink"])
    events = tuple(by_family["RespondentEvent"])[:-1]
    with pytest.raises(C11IntegrityError, match="count|record"):
        _sealed_body_release(
            handoff, source["sink"], projection,
            event_mutator=lambda _events: events,
        )
    assert handoff.stats.source_reads == 1
    assert handoff.stats.decode_calls == 1
    assert handoff.stats.full_c11_builds == 0


def test_s1e_native_body_build_does_not_second_decode(tmp_path, monkeypatch):
    import rawlsing_next.tests.test_pyat960_s1e_native_fact as module

    called = []

    def forbidden(*args, **kwargs):
        called.append((args, kwargs))
        raise AssertionError("second source decode/legacy build attempted")

    monkeypatch.setattr(module, "decode_fixture_config", forbidden)
    monkeypatch.setattr(
        module, "build_validated_c11_release_from_config", forbidden)
    fixture = _native_fixture(tmp_path)
    handoff, release, source = _build_native(
        tmp_path / "native", fixture, fixture["document"], "nodup.sqlite")
    assert called == []
    assert handoff.stats.source_reads == 1
    assert source["sink"].counts["RespondentEvent"] == 5
    assert release.release_ref
