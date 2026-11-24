"""#997/#998: actual SAV -> thirteen-family persisted C11 -> native I03 -> S04.

Real sourcefree saved body (not an unrelated mock/native fact injection);
existing R03 compiler/query, S2-C, S2-D, Batch/fates, S04 and observation
owners remain unchanged. No original respondent data or scientific rights.
"""
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission, SavedC11AdmissionError
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_i03_to_s04, execute_saved_batch,
)
from rawlsing_next.pre553_source_postconsumer_receipts import (
    join_saved_source_operation_fates,
)
from rawlsing_next.tests.test_pyat997_s1e_saved_native_first_consumer import (
    _full, _issued_manifest, _NATIVE_HOST, _NATIVE_PURPOSE,
)


def _issued_q101(compilation):
    """Select the real compiler's q101, NEVER author a matching mock query."""
    catalog = compilation.issued.workload.catalog
    candidates = []
    for entry in compilation.plan.records:
        if entry.status != "SUPPORTED":
            continue
        for raw in entry.query_refs:
            # R03's compiler carries the *role* alongside the exact ref.
            # The original #997 first reader intentionally strips role
            # metadata before converting the native ref, without reissuing it.
            if isinstance(raw, dict):
                raw = {key: raw[key] for key in ("kind", "object_id", "content_hash")}
            query = catalog.resolve_query_exact(exact_ref(raw, "original R03 query"))
            if any(
                exact_ref(target).kind == "QUESTION_NATIVE"
                and exact_ref(target).object_id.endswith(":q101")
                for target in query.target_refs
            ):
                candidates.append(query)
    assert candidates, "original R03 issued q101 must exist for this fixture"
    return candidates[0]


def test_real_sav_to_saved_native_s04_and_exact_operation_fate_join(tmp_path):
    handoff, estate, admission, compilation, resolver, sink = _full(tmp_path / "s1e")
    assert handoff.stats.source_reads == 1
    assert handoff.stats.full_c11_builds == 0
    assert sink.stats["second_i02_certification_in_frozen_writer"]
    assert sink.stats["source_decodes_by_sink"] == 0

    query = _issued_q101(compilation)
    predicate = exact_ref(query.condition_predicate_ref, "original query predicate")
    first = execute_saved_i03_to_s04(
        admission, query=query, predicate_ref=predicate,
    )
    assert first.execution.facts[0].typed_state == "SUPPORTED"
    assert first.execution.facts[0].raw_denominator_support == 5
    assert first.first_consumer.execution is first.execution
    assert first.first_consumer.ff01 is None  # R03 q101 is unary; do not invent F4
    assert first.first_consumer.receipt.material()["consumer_status"] == "UPSTREAM_S04_ONLY"
    assert first.first_consumer.knowledge.material()["fact_ref"] == (
        first.execution.facts[0].ref.as_dict()
    )
    scope = first.observation_scope.material()
    assert scope["fact_ref"] == first.execution.facts[0].ref.as_dict()
    assert scope["i03_resolved_joint_n"] == 5
    assert scope["i03_known_true_condition_n"] == 5
    assert scope["source_frame_population_n"] is None
    assert scope["observed_route_and_nonresponse_cause"] is None
    assert scope["source_asked_eligible_raw_summary"] is None

    # The existing source-native operation ledger must also reconcile with the
    # real saved Batch, independently of this new S04 first-consumer receipt.
    workload = compilation.issued.workload
    batch_manifest, preds = _issued_manifest(workload, admission)
    batch = execute_saved_batch(
        admission, manifest=batch_manifest, predicate_ref_by_query=preds,
    )
    joined = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=compilation, workload=workload, resolver=resolver,
        host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=batch,
    )
    assert len(joined.rows) == len(handoff.operation_fates)
    assert joined.audit["positive_native_linked_operations"] > 0
    assert any(x["disposition"] != "ELIGIBLE" for x in joined.rows)
    assert all(
        not x["postconsumer_receipt_refs"]
        for x in joined.rows if x["disposition"] != "ELIGIBLE"
    )


def test_prepared_and_unprepared_saved_s04_share_exact_i03_and_scoped_observation(tmp_path):
    _, _, admission, compilation, _, _ = _full(tmp_path / "prepared")
    query = _issued_q101(compilation)
    predicate = exact_ref(query.condition_predicate_ref)
    direct = execute_saved_i03_to_s04(
        admission, query=query, predicate_ref=predicate,
    )
    prepared = PreparedSavedC11Admission.from_verified_admission(admission)
    retained = execute_saved_i03_to_s04(
        prepared, query=query, predicate_ref=predicate,
    )
    assert direct.execution.facts[0].ref == retained.execution.facts[0].ref
    assert direct.first_consumer.knowledge.ref == retained.first_consumer.knowledge.ref
    assert direct.observation_scope.ref == retained.observation_scope.ref


def test_saved_s04_rejects_foreign_query_predicate_and_revoked_source(tmp_path):
    _, estate, admission, compilation, _, _ = _full(tmp_path / "revoked")
    query = _issued_q101(compilation)
    predicate = exact_ref(query.condition_predicate_ref)
    with pytest.raises(SavedC11AdmissionError, match="query/predicate"):
        execute_saved_i03_to_s04(
            admission, query=query, predicate_ref=query.ref,
        )
    with pytest.raises(SavedC11AdmissionError, match="exact saved"):
        execute_saved_i03_to_s04(
            object(), query=query, predicate_ref=predicate,
        )
    live = {"yes": True}
    private = (tmp_path / "revoked" / "private")
    guarded = SavedC11Admission.open(
        root=private,
        exact_path=estate.path,
        independently_held_manifest_sha256=estate.manifest_sha256,
        independently_held_i02=estate.i02,
        release_ref=estate.reconstructed_v1_release_ref,
        runtime_catalog=compilation.issued.workload.catalog,
        current_authorizer=lambda _: live["yes"],
    )
    assert execute_saved_i03_to_s04(
        guarded, query=query, predicate_ref=predicate,
    ).first_consumer.knowledge is not None
    live["yes"] = False
    with pytest.raises(DirectEstateError):
        execute_saved_i03_to_s04(
            guarded, query=query, predicate_ref=predicate,
        )
