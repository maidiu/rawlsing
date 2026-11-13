"""#997: one actual SAV/DTA Q2 -> S2-C -> S2-D I03/I05/Batch and S1-C fate join.

All fixtures are TEST_ONLY_SOURCEFREE; neither saved current guard nor the
existing test-only issuer grants original35 or production source rights.
"""
from __future__ import annotations

from pathlib import Path
from dataclasses import replace
from collections.abc import Mapping

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_batch_runner import (
    BatchManifest, BatchUnitSpec, BatchExecutionRunner,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission, SavedReleaseIdentity
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_i03, execute_saved_i05, execute_saved_batch,
)
from rawlsing_next.pre553_issued_workload import execute_issued_workload
from rawlsing_next.pre553_source_postconsumer_receipts import (
    join_saved_source_operation_fates, SourceReceiptJoinError,
    _verify_realized_q2_body_witness,
)
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.tests.test_pyat960_s1e_native_fact import (
    _native_fixture, _native_bundle, _compile_native, _NATIVE_HOST, _NATIVE_PURPOSE,
)
from rawlsing_next.tests.test_pyat960_s1e_support import build
from rawlsing_next.tests.test_universal_grammar import _frontier
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet


def _full(tmp_path: Path, values=(0., 1., 0., 1., 0.), source_format="SAV"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    # R03 owner fixture has exact TEST_ONLY risk/authority and canonical cells.
    fixture = _native_fixture(tmp_path, values=values)
    # Cross-root restoration must preserve the *same* scientific inventory
    # identity, not source_fixture's test-root-specific id(root) debug label.
    fixed_inventory = replace(
        fixture["inventory"], inventory_id="PYAT997-S1E-EXACT-RESTORE")
    fixed_frontier = _frontier(fixed_inventory, fixture["policy"])
    fixture.update(
        inventory=fixed_inventory, frontier=fixed_frontier,
        census=_freeze_packet(fixed_frontier),
    )
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    certificate = tmp_path / "source-i02.sqlite"
    sink = SourceSavedBodySink(
        certificate_path=certificate, authorized_private_root=private, chunk_rows=2,
    )
    handoff = build(
        tmp_path, fixture, name="source-i02.sqlite",
        body_sink=sink, chunk_size=2,
    )
    estate = sink.receipt
    assert estate.i02 == handoff.roots
    assert handoff.stats.source_reads == 1
    assert handoff.stats.full_c11_builds == 0
    # The native compiler only needs a *release identity* in this bundle;
    # saved reader uses the genuine qualified physical body and exact v1 ref.
    release_identity = SavedReleaseIdentity(estate.reconstructed_v1_release_ref)
    bundle = _native_bundle(handoff, fixture, fixture["projection"], release_identity)
    compilation = _compile_native(fixture, handoff, fixture["projection"], release_identity)
    issued = compilation.issued
    assert issued.workload.projection == fixture["projection"]
    admission = SavedC11Admission.open(
        root=private, exact_path=estate.path,
        independently_held_manifest_sha256=estate.manifest_sha256,
        independently_held_i02=estate.i02,
        release_ref=estate.reconstructed_v1_release_ref,
        runtime_catalog=issued.workload.catalog,
        current_authorizer=lambda _roots: True,
    )
    resolver = TestOnlyDecisionResolver(issued.record)
    return handoff, estate, admission, compilation, resolver, sink


def _native_i03(admission, compilation):
    for entry in compilation.plan.records:
        if entry.status != "SUPPORTED" or not entry.query_refs:
            continue
        raw = entry.query_refs[0]
        if isinstance(raw, Mapping):
            raw = {key: raw[key] for key in ("kind", "object_id", "content_hash")}
        query_ref = exact_ref(raw, "lowering query")
        query = compilation.issued.workload.catalog.resolve_query_exact(query_ref)
        predicate_ref = exact_ref(query.condition_predicate_ref, "lowering predicate")
        result = execute_saved_i03(
            admission, query_ref=query_ref, predicate_ref=predicate_ref)
        if result.facts:
            return entry.operation_id, result
    pytest.fail("no S1-C supported saved-native I03 first reader")


def _issued_manifest(workload, admission):
    """Every originally issued unit, not merely a convenient discovery."""
    units = tuple(
        BatchUnitSpec(
            "QUERY", request.query_ref,
            (admission.release_ref,), (workload.decision_ref,),
        )
        for request in workload.requests
    ) + tuple(
        BatchUnitSpec(
            "DISCOVERY", authority,
            (admission.release_ref,), (workload.decision_ref,),
        )
        for authority in workload.discoveries
    )
    return BatchManifest(units), {
        request.query_ref.key: request.predicate_ref
        for request in workload.requests
    }


def _run(tmp_path, values):
    handoff, estate, admission, compilation, resolver, sink = _full(tmp_path, values)
    record = compilation.issued.record
    workload = compilation.issued.workload
    operation, fact_result = _native_i03(admission, compilation)
    authority_ref = workload.discoveries[0]
    discovery = execute_saved_i05(admission, discovery_authority_ref=authority_ref)
    assert discovery.receipts
    batch_manifest, predicates = _issued_manifest(workload, admission)
    batch = execute_saved_batch(
        admission, manifest=batch_manifest, predicate_ref_by_query=predicates,
    )
    assert len(batch.receipts) == len(batch_manifest.units)
    assert all(receipt.state == "COMPLETED" for receipt in batch.receipts)
    # Also exercise the previously accepted S2-D normal issued-workload reader
    # with source_factory absent: it must NOT re-decode the SAV source.
    normal = execute_issued_workload(
        workload, resolver, source_factory=None,
        saved_admission_factory=lambda: admission,
        host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, allow_test_only=True,
    )
    assert all(r.state == "COMPLETED" for r in normal.receipts)
    joined = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=compilation, workload=workload, resolver=resolver,
        host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=batch,
    )
    assert len(joined.rows) == len(handoff.operation_fates)
    assert joined.audit["positive_native_linked_operations"] > 0
    assert joined.audit["native_discovery_candidates_exactly_joined"] > 0
    assert all(x["issued_receipt_refs"] == () for x in handoff.operation_fates)
    assert any(x["disposition"] != "ELIGIBLE" for x in joined.rows)
    assert all(
        not row["postconsumer_receipt_refs"]
        for row in joined.rows if row["disposition"] != "ELIGIBLE"
    )
    assert all(
        row["postconsumer_batch_receipt_refs"]
        for row in joined.rows
        if row["postconsumer_state"] == "TEST_ONLY_SAVED_NATIVE_DISCOVERY_RECEIPTED"
    )
    return (handoff, estate, admission, compilation, resolver, batch, joined,
            tuple(f.ref.key for f in fact_result.facts),
            tuple(r.ref.key for r in discovery.receipts))


def test_source_to_saved_cold_s1c_i03_i05_batch_normal_and_exact_fate_join(tmp_path):
    first = _run(tmp_path / "first", (0., 1., 0., 1., 0.))
    changed = _run(tmp_path / "changed", (0., 1., 1., 1., 0.))
    restored = _run(tmp_path / "restored", (0., 1., 0., 1., 0.))
    assert first[0].source_sha256 != changed[0].source_sha256
    assert first[1].i02.logical != changed[1].i02.logical
    assert first[1].i02.logical == restored[1].i02.logical
    assert first[7] != changed[7] or first[8] != changed[8]
    assert first[7] == restored[7]
    assert first[8] == restored[8]
    assert first[6].result_hash == restored[6].result_hash


def test_missing_issued_batch_receipt_stays_pending_not_invented(tmp_path):
    handoff, estate, admission, compilation, resolver, _ = _full(tmp_path / "missing")
    workload = compilation.issued.workload
    batch_manifest, _predicates = _issued_manifest(workload, admission)
    never_executed = BatchExecutionRunner(
        manifest=batch_manifest, repository=admission, saved_mode=True)
    joined = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=compilation, workload=workload, resolver=resolver,
        host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=never_executed,
    )
    assert joined.audit["positive_native_linked_operations"] == 0
    assert joined.audit["pending_eligible_operations"] > 0
    assert not any(row["postconsumer_receipt_refs"] for row in joined.rows)


def test_mixed_source_issued_receipt_join_refused_before_claim(tmp_path):
    original = _full(tmp_path / "original")
    other = _full(tmp_path / "other", values=(1., 1., 1., 1., 1.))
    handoff, estate, admission, compilation, resolver, _ = original
    alien_admission = other[2]
    workload = compilation.issued.workload
    manifest = BatchManifest((
        BatchUnitSpec("DISCOVERY", workload.discoveries[0],
                      (alien_admission.release_ref,), (workload.decision_ref,)),
    ))
    runner = BatchExecutionRunner(manifest=manifest,
                                  repository=alien_admission, saved_mode=True)
    with pytest.raises(SourceReceiptJoinError, match="Q2_SAVED_REPLAY_AND_RELEASE_IDENTITY_DRIFT"):
        join_saved_source_operation_fates(
            handoff=handoff, estate_receipt=estate, admission=alien_admission,
            compilation=compilation, workload=workload, resolver=resolver,
            host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=runner,
        )


def test_q2_held_fate_cannot_be_promoted_into_native_issued_positive(tmp_path):
    handoff, estate, admission, compilation, resolver, _ = _full(
        tmp_path / "held-promotion"
    )
    manifest, _ = _issued_manifest(compilation.issued.workload, admission)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True,
    )
    assert any(row["disposition"] == "HELD" for row in handoff.operation_fates)
    target = next(
        row["operation_id"] for row in handoff.operation_fates
        if row["disposition"] == "HELD"
    )
    altered = tuple(
        {**row, "disposition": "ELIGIBLE"}
        if row["operation_id"] == target else row
        for row in handoff.operation_fates
    )
    forged = replace(handoff, operation_fates=altered)
    with pytest.raises(
        SourceReceiptJoinError, match="Q2_OPERATION_FATE_OR_CLAIM_PROMOTED",
    ):
        join_saved_source_operation_fates(
            handoff=forged, estate_receipt=estate, admission=admission,
            compilation=compilation, workload=compilation.issued.workload,
            resolver=resolver, host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
            runner=runner,
        )


def test_postconsumer_receipt_rows_cannot_change_after_source_mutation(tmp_path):
    handoff, estate, admission, compilation, resolver, _ = _full(
        tmp_path / "immutable-fate"
    )
    manifest, _ = _issued_manifest(compilation.issued.workload, admission)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True,
    )
    joined = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=compilation, workload=compilation.issued.workload,
        resolver=resolver, host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
        runner=runner,
    )
    old = joined.rows[0]["source_preimage"]["source_id"]
    # The producer's shallow-frozen dataclass contains nested dictionaries.
    # Editing one after join must NOT silently rewrite a hashed P1 receipt.
    handoff.operation_fates[0]["source_preimage"]["source_id"] = "MUTATED"
    assert joined.rows[0]["source_preimage"]["source_id"] == old
    with pytest.raises(TypeError):
        joined.rows[0]["source_preimage"]["source_id"] = "TAMPERED"


@pytest.mark.parametrize("forgery", ["realized", "state", "census"])
def test_source_realization_witness_must_agree_before_native_join(
    tmp_path, forgery,
):
    """A mutable Q2 row or its separate census must not confer a receipt."""
    handoff, estate, admission, compilation, resolver, _ = _full(
        tmp_path / ("source-witness-" + forgery)
    )
    manifest, _ = _issued_manifest(compilation.issued.workload, admission)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True,
    )
    if forgery == "census":
        altered_audit = dict(handoff.census_audit)
        source_audit = dict(altered_audit["operation_source_antijoin"])
        source_audit["operation_count"] += 1
        altered_audit["operation_source_antijoin"] = source_audit
        forged = replace(handoff, census_audit=altered_audit)
        refusal = "Q2_SOURCE_REALIZATION_AUDIT_DRIFT"
    else:
        target = next(
            row for row in handoff.operation_fates
            if row["disposition"] == "ELIGIBLE"
            and row["source_realized"] is True
        )
        forged_row = dict(target)
        if forgery == "realized":
            # The original Q2 source-state witness still says REALIZED.
            forged_row["source_realized"] = False
        else:
            # Keep the favorable boolean and conceal the original source state.
            forged_row["operation_source_state"] = "ELIGIBLE_TYPED_HOLD"
        forged = replace(
            handoff, operation_fates=tuple(
                forged_row if row["operation_id"] == target["operation_id"]
                else row for row in handoff.operation_fates
            ),
        )
        refusal = "Q2_SOURCE_REALIZATION_CONTRADICTION"
    with pytest.raises(SourceReceiptJoinError, match=refusal):
        join_saved_source_operation_fates(
            handoff=forged, estate_receipt=estate, admission=admission,
            compilation=compilation, workload=compilation.issued.workload,
            resolver=resolver, host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
            runner=runner,
        )


@pytest.mark.parametrize("attack", ["missing_emission", "unresolved_routing", "measure_preimage"])
def test_agent_b_q2_detail_witness_cannot_be_overruled_by_summary(
    tmp_path, attack,
):
    """A's summary/census are kept favorable while physical Q2 detail is forged.

    This is a negative-first preservation test: the unexecuted Batch runner is
    intentional because Q2 contradictions must be refused before promotion.
    """
    handoff, estate, admission, compilation, resolver, _ = _full(
        tmp_path / ("agent-b-" + attack)
    )
    manifest, _ = _issued_manifest(compilation.issued.workload, admission)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True,
    )
    candidates = [
        row for row in handoff.operation_fates
        if row["disposition"] == "ELIGIBLE" and row["source_realized"] is True
    ]
    if attack == "unresolved_routing":
        candidates = [
            row for row in candidates
            if any(w["family"] == "RespondentEvent" and w["emitted"] > 0
                   for w in row["source_realization"])
        ]
    target = next(iter(candidates))
    forged_row = dict(target)
    if attack == "missing_emission":
        key = target["source_realization"][0]["key"]
        forged_row["source_realization"] = tuple(
            {**w, "emitted": 0} if w["key"] == key else w
            for w in target["source_realization"]
        )
        refusal = "Q2_REALIZATION_BODY_OR_ROUTING_CONTRADICTION"
    elif attack == "unresolved_routing":
        witness = next(
            w for w in target["source_realization"]
            if w["family"] == "RespondentEvent" and w["emitted"] > 0
        )
        forged_row["source_realization"] = tuple(
            {**w, "routing_unresolved": True} if w is witness else w
            for w in target["source_realization"]
        )
        refusal = "Q2_REALIZATION_BODY_OR_ROUTING_CONTRADICTION"
    else:
        source_preimage = dict(target["source_preimage"])
        source_preimage["measure"] = {
            **source_preimage["measure"],
            "weight_ref": "FORGED_WEIGHT_MEASURE",
        }
        forged_row["source_preimage"] = source_preimage
        refusal = "Q2_MEASURE_PREIMAGE_CONTRADICTION"
    forged = replace(
        handoff, operation_fates=tuple(
            forged_row if row["operation_id"] == target["operation_id"] else row
            for row in handoff.operation_fates
        ),
    )
    with pytest.raises(SourceReceiptJoinError, match=refusal):
        join_saved_source_operation_fates(
            handoff=forged, estate_receipt=estate, admission=admission,
            compilation=compilation, workload=compilation.issued.workload,
            resolver=resolver, host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
            runner=runner,
        )


@pytest.mark.parametrize(
    "attack,refusal",
    [
        ("zero_routable", "Q2_REALIZATION_ZERO_ROUTABLE_DENOMINATOR"),
        ("concealed_unknown", "Q2_REALIZATION_ROUTING_CENSUS_DRIFT"),
        ("eligible_count_drift", "Q2_REALIZATION_ROUTING_CENSUS_DRIFT"),
    ],
)
def test_agent_a_counter_b_q2_routing_denominator_and_state_anti_forgery(
    tmp_path, attack, refusal,
):
    """B's per-key emitted/occurrence check alone admits false routed support.

    Keep ELIGIBLE, the favorable per-key summary, aggregate census, and
    physical I02 roots intact; mutate only one Q2 detail witness family.
    """
    handoff, estate, admission, compilation, resolver, _ = _full(
        tmp_path / ("agent-a-routing-" + attack)
    )
    manifest, _ = _issued_manifest(compilation.issued.workload, admission)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True,
    )
    target = next(
        row for row in handoff.operation_fates
        if row["disposition"] == "ELIGIBLE" and row["source_realized"] is True
        and any(
            w["family"] == "RespondentEvent" and w["emitted"] > 0
            for w in row["source_realization"]
        )
    )
    original = next(
        w for w in target["source_realization"]
        if w["family"] == "RespondentEvent" and w["emitted"] > 0
    )
    key = original["key"]
    modified = []
    for witness in target["source_realization"]:
        new = dict(witness)
        if attack == "zero_routable" and (
            witness["key"] == key and witness["family"] == "RespondentEvent"
            and witness["emitted"] > 0
        ):
            states = dict(witness["routing_states"])
            states["ELIGIBLE_APPLICABLE"] = 0
            new["routing_states"] = states
            new["routable_rows"] = 0
        elif witness is original and attack == "concealed_unknown":
            new["routing_states"] = {
                **witness["routing_states"], "ROUTING_UNKNOWN": 1,
            }
            # The favorable but now false 'routing_unresolved' remains False.
        elif witness is original and attack == "eligible_count_drift":
            new["routable_rows"] = witness["routable_rows"] + 1
        modified.append(new)
    forged = replace(handoff, operation_fates=tuple(
        {**row, "source_realization": tuple(modified)}
        if row["operation_id"] == target["operation_id"]
        else row for row in handoff.operation_fates
    ))
    with pytest.raises(SourceReceiptJoinError, match=refusal):
        join_saved_source_operation_fates(
            handoff=forged, estate_receipt=estate, admission=admission,
            compilation=compilation, workload=compilation.issued.workload,
            resolver=resolver, host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
            runner=runner,
        )


def test_agent_a_counter_preserves_q2_multislot_one_routable_semantics():
    """Q2 requires at least one eligible routed response slot, not all slots.

    Synthetic per-key predicate test: no claim this invented tuple is a
    separately authorized source or a complete physical release.
    """
    first = {
        "key": "KEY-1", "item_id": "item-1", "family": "RespondentEvent",
        "slot": (0, "q1"), "question_id": "q1", "emitted": 5,
        "routing_states": {"ELIGIBLE_APPLICABLE": 5}, "routable_rows": 5,
        "routing_unresolved": False, "occurrence_realized": True,
        "occurrence_dimension": None,
    }
    zero = {
        **first, "slot": (1, "q2"), "question_id": "q2",
        "routing_states": {"NOT_ASKED": 5}, "routable_rows": 0,
    }
    source_fate = {
        "disposition": "ELIGIBLE", "source_realized": True,
        "source_realization": (first, zero),
        "routing_unresolved_keys": (), "unrealized_keys": (),
    }
    _verify_realized_q2_body_witness(source_fate)
    no_eligible_route = {
        **source_fate, "source_realization": (
            {**first, "routing_states": {"NOT_ASKED": 5},
             "routable_rows": 0}, zero,
        ),
    }
    with pytest.raises(
        SourceReceiptJoinError,
        match="Q2_REALIZATION_ZERO_ROUTABLE_DENOMINATOR",
    ):
        _verify_realized_q2_body_witness(no_eligible_route)


@pytest.mark.parametrize(
    "attack,refusal",
    [
        ("q2_frontier", "Q2_R03_ORIGINAL_FRONTIER_HASH_DRIFT"),
        ("r03_frontier", "Q2_R03_ORIGINAL_FRONTIER_HASH_DRIFT"),
        ("source_census", "Q2_ORIGINAL_FROZEN_FATE_CENSUS_DRIFT"),
        ("science_census", "Q2_ORIGINAL_FROZEN_FATE_CENSUS_DRIFT"),
        ("eligible_fate_partition", "Q2_ORIGINAL_FROZEN_FATE_CENSUS_DRIFT"),
    ],
)
def test_agent_b_r5_original_frontier_and_frozen_census_cut(
    tmp_path, attack, refusal,
):
    """Reject same-source but different original S1-C/R03 frontier preimage.

    Every attack keeps the source body, its SHA, Q2 emitted-key details,
    acceptable routing witness, legal P1 operation labels, and all physical
    saved roots unchanged. These contradictions were invisible to A R4.
    """
    handoff, estate, admission, compilation, resolver, _ = _full(
        tmp_path / ("agent-b-r5-" + attack)
    )
    assert handoff.census_audit["frontier_hash"] == compilation.frontier_hash
    assert (handoff.census_audit["source_candidate_count"]
            == len(handoff.operation_fates))
    assert (handoff.census_audit["scientific_fate_count"]
            == len(handoff.operation_fates))
    manifest, _ = _issued_manifest(compilation.issued.workload, admission)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True,
    )
    altered = dict(handoff.census_audit)
    if attack == "q2_frontier":
        altered["frontier_hash"] = "0" * 64
    elif attack == "r03_frontier":
        compilation = replace(compilation, frontier_hash="0" * 64)
    elif attack == "source_census":
        altered["source_candidate_count"] += 1
    elif attack == "science_census":
        altered["scientific_fate_count"] -= 1
    else:
        fate_counts = dict(altered["fate_counts"])
        fate_counts["ELIGIBLE"] += 1
        altered["fate_counts"] = fate_counts
    if attack != "r03_frontier":
        handoff = replace(handoff, census_audit=altered)
    with pytest.raises(SourceReceiptJoinError, match=refusal):
        join_saved_source_operation_fates(
            handoff=handoff, estate_receipt=estate, admission=admission,
            compilation=compilation, workload=compilation.issued.workload,
            resolver=resolver, host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
            runner=runner,
        )
