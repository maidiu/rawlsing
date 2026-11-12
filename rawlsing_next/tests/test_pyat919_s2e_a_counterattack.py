"""Agent A return: adversarial I05 candidate and whole-frontier falsifiers.

These execute the real inherited five-unit sourcefree Batch, and forge complete
canonical public receipt objects PLUS a newly valid outer frontier replay and
matching Batch completion receipt. A self-hash failure is deliberately avoided.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import (
    DiscoveryResultReceipt, ExactRef, semantic_hash,
)
from rawlsing_next.pre553_discovery_exact import I05_CONTRACT_ID
from rawlsing_next.pre553_s2e_exact_conservation import (
    S2EOutputConservationError, census_native_batch, require_same_native_output_graph,
)
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope
from rawlsing_next.tests.test_pyat919_s2e_a_whole_native_batch import (
    _batch, _native_case,
)


def _replay_ref(namespace, material):
    digest = semantic_hash(material)
    return ExactRef(
        "PRE553_I05_FRONTIER_REPLAY" if namespace == "frontier-replay"
        else "PRE553_I05_DISCOVERY_REPLAY",
        f"urn:rawlsing:pre553:i05:{namespace}:sha256:{digest}", digest,
    )


def _forge_receipt(receipt, *, overrides, root=None):
    data = dict(receipt.semantic_fields)
    data.update(overrides)
    return DiscoveryResultReceipt(
        typed_state=receipt.typed_state,
        authority_snapshot_refs=receipt.authority_snapshot_refs,
        dependency_refs=receipt.dependency_refs,
        producer_replay_locator_or_reference_root=(
            receipt.producer_replay_locator_or_reference_root if root is None else root
        ),
        **data,
    )


def _outer_consistent(manifest, history, outputs, unit, forged_receipt):
    """Rebuild outer frontier replay and Batch result refs; not a hash-only negative."""
    original = outputs[unit.unit_hash]
    substituted = tuple(sorted(
        (forged_receipt if r.ref == original.receipts[0].ref else r
         for r in original.receipts),
        key=lambda r: r.ref.key,
    ))
    outer = _replay_ref("frontier-replay", {
        "contract": I05_CONTRACT_ID,
        "frontier_ref": original.evaluated_frontier_ref.as_dict(),
        "receipt_refs": [r.ref.as_dict() for r in substituted],
        "fact_refs": [r.as_dict() for r in original.empirical_fact_refs],
        "valid_empty": original.valid_empty,
    })
    bogus = replace(original, receipts=substituted, replay_ref=outer)
    replaced_receipts = tuple(
        replace(r, result_refs=tuple(x.ref for x in substituted))
        if r.unit_ref == unit.unit_ref else r
        for r in history
    )
    return replaced_receipts, {**outputs, unit.unit_hash: bogus}


def _run():
    case = _native_case()
    with I03GroupedExecutionScope() as scope:
        manifest, receipts, outputs, baseline, _, _ = _batch(case, scope=scope)
    unit = next(u for u in manifest.units if u.job_kind == "DISCOVERY")
    return case, manifest, receipts, outputs, baseline, unit


def test_a2_rehashed_candidate_replay_and_rehashed_outer_frontier_refused():
    case, manifest, receipts, outputs, baseline, unit = _run()
    candidate = outputs[unit.unit_hash].receipts[0]
    fictitious = "f" * 64
    forged_inner = ExactRef(
        "PRE553_I05_DISCOVERY_REPLAY",
        f"urn:rawlsing:pre553:i05:candidate-replay:sha256:{fictitious}",
        fictitious,
    )
    assert candidate.replay_ref != forged_inner
    altered = _forge_receipt(
        candidate, overrides={"replay_ref": forged_inner}, root=forged_inner,
    )
    broken_history, broken_outputs = _outer_consistent(
        manifest, receipts, outputs, unit, altered,
    )
    # Candidate and outer replay refs are all self-consistent as objects;
    # only the native candidate-specific formula disproves the forgery.
    with pytest.raises(S2EOutputConservationError,
                       match="S2E_I05_CANDIDATE_REPLAY_MISMATCH"):
        census_native_batch(
            manifest, broken_history, broken_outputs,
            runtime_catalog=case[1], require_complete=True,
        )
    restored = census_native_batch(
        manifest, receipts, outputs,
        runtime_catalog=case[1], require_complete=True,
    )
    require_same_native_output_graph(baseline, restored)


def test_a2_rehashed_wrong_winning_predicate_and_outer_refused():
    case, manifest, receipts, outputs, baseline, unit = _run()
    native = outputs[unit.unit_hash]
    candidate = native.receipts[0]
    wrong = next(
        p.ref for p in native.executed_predicates
        if p.ref.key != candidate.winning_predicate_ref["kind"] + "|impossible"
        and p.ref != candidate.winning_predicate_ref
    )
    assert wrong != candidate.winning_predicate_ref
    altered = _forge_receipt(
        candidate, overrides={"winning_predicate_ref": wrong},
    )
    broken_history, broken_outputs = _outer_consistent(
        manifest, receipts, outputs, unit, altered,
    )
    with pytest.raises(S2EOutputConservationError,
                       match="S2E_I05_CANDIDATE_IDENTITY_MISMATCH"):
        census_native_batch(
            manifest, broken_history, broken_outputs,
            runtime_catalog=case[1], require_complete=True,
        )
    require_same_native_output_graph(
        baseline, census_native_batch(
            manifest, receipts, outputs,
            runtime_catalog=case[1], require_complete=True,
        ),
    )


def test_a2_declared_grammar_refuses_coordinated_missing_candidate_and_outer():
    case, manifest, receipts, outputs, baseline, unit = _run()
    original = outputs[unit.unit_hash]
    # A native executed frontier is not proven complete by identical CLAIMED
    # counters. A fabricated zero-candidate result must contradict the issued
    # exact discovery authority's nonempty grammar.
    emptied = replace(
        original, candidate_count=0, covered_candidate_count=0,
        receipts=(), empirical_fact_refs=(), empirical_facts=(),
        executed_queries=(), executed_predicates=(), valid_empty=True,
        replay_ref=_replay_ref("frontier-replay", {
            "contract": I05_CONTRACT_ID,
            "frontier_ref": original.evaluated_frontier_ref.as_dict(),
            "receipt_refs": [], "fact_refs": [], "valid_empty": True,
        }),
    )
    replaced = tuple(
        replace(r, result_refs=()) if r.unit_ref == unit.unit_ref else r
        for r in receipts
    )
    with pytest.raises(S2EOutputConservationError,
                       match="S2E_I05_DECLARED_FRONTIER_MISMATCH"):
        census_native_batch(
            manifest, replaced, {**outputs, unit.unit_hash: emptied},
            runtime_catalog=case[1], require_complete=True,
        )
    require_same_native_output_graph(
        baseline, census_native_batch(
            manifest, receipts, outputs,
            runtime_catalog=case[1], require_complete=True,
        ),
    )
