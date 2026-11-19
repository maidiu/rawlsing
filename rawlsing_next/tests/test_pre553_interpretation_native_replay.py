"""Actual cold C11 sourcefree I03/S04 interpretation-version replay and Batch.

No original GSS/SRC16 access. These fixtures run the preexisting native C11,
I03 and PYAT S04/FF01 first consumers with a separately supplied
response-semantics CURRENT resolver. This resolver must later come from the
competent interpretation/source authority; it is NOT issued by the test.
"""
import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref, semantic_hash
from rawlsing_next.pre553_interpretation_qualification import (
    InterpretationQualificationError,
)
from rawlsing_next.pre553_s04_dynamic_research import (
    S04DynamicQuestion, S04DynamicResearchSession,
)
from rawlsing_next.pre553_s04_general_joint_algebra import S04Projection
from rawlsing_next.pre553_distinct_cold_s04_batch import (
    S04DistinctOperation, SOURCEFREE_ONLY_ASSERTION,
    execute_distinct_native_s04_research,
)
from rawlsing_next.tests.test_pre553_s04_dynamic_research import _source
from rawlsing_next.tests.test_pre553_distinct_cold_s04_batch import _mixed


def _semantics_ref(query):
    return exact_ref(
        query.requested_output_grain["response_state_semantics_ref"],
        "native response semantic mapping version",
    )


def _revision(ref):
    return ExactRef(
        ref.kind,
        "urn:test:updated-interpretation-not-physical-c11-rebuild",
        semantic_hash({"version": "B", "original": ref.key}),
    )


def test_live_native_s04_cached_answer_refuses_mapping_change_without_rebuilding_c11(
    tmp_path, monkeypatch,
):
    _, _, predicate, queries, executor, _, _ = _source(
        tmp_path, monkeypatch, size=2, tag="ANVIL-MAPPING-CURRENT-CHANGES",
    )
    original_ref = _semantics_ref(queries[0])
    epoch = {"mapping": original_ref}

    def current_semantics(expected):
        # Valid only when source-interpretation owner says this exact
        # source meaning remains CURRENT. Source C11 physical bits unchanged.
        return epoch["mapping"]

    with S04DynamicResearchSession(
        executor=executor, sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
        resolve_current_response_semantics_ref=current_semantics,
    ) as session:
        first = session.ask(S04DynamicQuestion(queries[0].ref, predicate.ref))
        result = first.joint_workspace.query(S04Projection((0,), {})).material()
        assert result["raw_selected_full_case_n"] == 4
        assert result["interpretation_version_ref"] == original_ref.as_dict()
        assert result["interpretation_current_check"].startswith("BOUND_EXACT")
        assert session.stats()["original_native_i03_queries_executed"] == 1

        epoch["mapping"] = _revision(original_ref)
        with pytest.raises(InterpretationQualificationError, match="VERSION_STALE"):
            first.joint_workspace.query(S04Projection((0,), {}))
        # Before executing the second I03, changed interpretation must deny
        # its old exact mapping binding, even though C11 remains physically
        # readable and the source release has not changed.
        with pytest.raises(InterpretationQualificationError, match="VERSION_STALE"):
            session.ask(S04DynamicQuestion(queries[1].ref, predicate.ref))
        assert session.stats()["original_native_i03_queries_executed"] == 1


def test_distinct_saved_batch_rechecks_each_mapping_before_native_index(
    tmp_path, monkeypatch,
):
    _, _, predicate, query_pair, query_unary, executor, operations, _ = _mixed(
        tmp_path, monkeypatch, tag="ANVIL-MAP-RECEIPT-CURRENT",
    )
    ref = _semantics_ref(query_pair)
    epoch = {"mapping": ref}
    result = execute_distinct_native_s04_research(
        executor=executor, operations=operations,
        sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
        resolve_current_response_semantics_ref=lambda expected: epoch["mapping"],
    )
    material = result.receipt.material()
    assert material["interpretation_current_check"].startswith("ALL_EXACT")
    assert all(
        row["interpretation_current_check"].startswith("OPERATION_SCOPED")
        for row in material["ordered_research_products"]
    )
    assert all(row["response_interpretation_semantics_ref"] == ref.as_dict()
               for row in material["ordered_research_products"])

    epoch["mapping"] = _revision(ref)
    with pytest.raises(InterpretationQualificationError, match="VERSION_STALE"):
        execute_distinct_native_s04_research(
            executor=executor, operations=operations,
            sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
            resolve_current_response_semantics_ref=lambda expected: epoch["mapping"],
        )


def test_batch_semantics_change_during_second_consumer_refuses_final_completion(
    tmp_path, monkeypatch,
):
    import rawlsing_next.pre553_distinct_cold_s04_batch as subject
    _, _, predicate, pair, unary, executor, operations, _ = _mixed(
        tmp_path, monkeypatch, tag="ANVIL-MAP-CHANGED-MID-BATCH",
    )
    ref = _semantics_ref(pair)
    epoch = {"mapping": ref}
    real = subject.receive_s04_first_consumer
    received = {"count": 0}

    def change_interpretation_during_processing(**kwargs):
        publication = real(**kwargs)
        received["count"] += 1
        if received["count"] == 1:
            epoch["mapping"] = _revision(ref)
        return publication

    with monkeypatch.context() as patch:
        patch.setattr(subject, "receive_s04_first_consumer", change_interpretation_during_processing)
        with pytest.raises(InterpretationQualificationError, match="VERSION_STALE"):
            subject.execute_distinct_native_s04_research(
                executor=executor, operations=operations,
                sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
                resolve_current_response_semantics_ref=lambda expected: epoch["mapping"],
            )
    assert received["count"] == 1


def test_unqualified_saved_batch_marks_interpretation_current_as_unverified(
    tmp_path, monkeypatch,
):
    _, _, _, pair, unary, executor, operations, _ = _mixed(
        tmp_path, monkeypatch, tag="ANVIL-UNBOUND-MAP-GRADE",
    )
    raw = execute_distinct_native_s04_research(
        executor=executor, operations=operations,
        sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
    )
    assert raw.receipt.material()["interpretation_current_check"].startswith("UNVERIFIED")
    assert all(
        row["interpretation_current_check"] == "INTERPRETATION_CURRENT_NOT_VERIFIED"
        for row in raw.receipt.material()["ordered_research_products"]
    )
