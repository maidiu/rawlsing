"""R03V R4 independent fixed-original-pin probes (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_universal_workload import (
    compile_governed_frontier, execute_governed_frontier,
    restore_governed_frontier_ledger,
)
from rawlsing_next.tests.test_universal_workload import (
    AS_OF, HOST, PURPOSE, _frontier_bundle, _frontier_fixture,
)


def _governed(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "r03v_r4.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    result = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    return bundle, compilation, result


def _forge(ledger):
    ledger = deepcopy(ledger)
    ledger.pop("ledger_hash", None)
    ledger["ledger_hash"] = semantic_hash(ledger)
    return ledger


def _fact_identity(ref):
    return (ref.get("object_id"), ref.get("content_hash"))


def _delete_fact(ledger):
    target = _fact_identity(ledger["native_facts"][0])
    ledger["native_facts"] = [f for f in ledger["native_facts"]
                              if _fact_identity(f) != target]
    ledger["fact_refs"] = [r for r in ledger["fact_refs"]
                           if _fact_identity(r) != target]
    for receipt in ledger["native_receipts"]:
        semantic = receipt.setdefault("semantic_fields", {})
        semantic["empirical_fact_refs"] = [
            r for r in semantic.get("empirical_fact_refs", ())
            if _fact_identity(r) != target
        ]
    for row in ledger["operation_ledger"]:
        row["fact_refs"] = [r for r in row.get("fact_refs", ())
                            if _fact_identity(r) != target]


def _duplicate_fact(ledger):
    target = _fact_identity(ledger["native_facts"][0])
    fact = next(f for f in ledger["native_facts"] if _fact_identity(f) == target)
    ref = next(r for r in ledger["fact_refs"] if _fact_identity(r) == target)
    ledger["native_facts"].append(deepcopy(fact))
    ledger["fact_refs"].append(deepcopy(ref))
    for receipt in ledger["native_receipts"]:
        semantic = receipt.setdefault("semantic_fields", {})
        refs = semantic.get("empirical_fact_refs", ())
        if any(_fact_identity(r) == target for r in refs):
            semantic["empirical_fact_refs"] = tuple(refs) + (deepcopy(ref),)
            break
    for row in ledger["operation_ledger"]:
        refs = row.get("fact_refs", ())
        if any(_fact_identity(r) == target for r in refs):
            row["fact_refs"] = tuple(refs) + (deepcopy(ref),)
            break


def test_H1_genuine_original_pin_restore_and_missing_wrong_pin_refuse(tmp_path):
    bundle, compilation, result = _governed(tmp_path)
    pin = result.freeze_restore_checkpoint()
    assert isinstance(pin, str) and pin
    restored = restore_governed_frontier_ledger(
        result.ledger(), expected_checkpoint_ref=pin)
    assert restored["schema"] == result.ledger()["schema"]
    with pytest.raises(Exception):
        restore_governed_frontier_ledger(result.ledger())
    with pytest.raises(Exception):
        restore_governed_frontier_ledger(
            result.ledger(), expected_checkpoint_ref="wrong-pin")


def test_H2_prior_fact_job_probes_refuse_against_original_pin(tmp_path):
    bundle, compilation, result = _governed(tmp_path)
    pin = result.freeze_restore_checkpoint()
    ledger = result.ledger()
    cases = []
    deleted = deepcopy(ledger); _delete_fact(deleted); cases.append(("fact_delete", _forge(deleted)))
    duplicated = deepcopy(ledger); _duplicate_fact(duplicated); cases.append(("fact_duplicate", _forge(duplicated)))
    substituted = deepcopy(ledger)
    job = list(substituted["expected_jobs"][0])
    job[1] = "urn:forged:query-ref"
    job[2] = "urn:forged:predicate-ref"
    substituted["expected_jobs"][0] = job
    substituted["compilation"]["issued"]["expected_jobs"][0] = job
    substituted["compilation_hash"] = semantic_hash(substituted["compilation"])
    cases.append(("job_substitution", _forge(substituted)))
    for name, forged in cases:
        with pytest.raises(Exception):
            restore_governed_frontier_ledger(forged, expected_checkpoint_ref=pin)
        # genuine original must remain restorable between faults
        restore_governed_frontier_ledger(ledger, expected_checkpoint_ref=pin)


def test_H3_content_mutation_retaining_refs_refuses_with_original_pin(tmp_path):
    bundle, compilation, result = _governed(tmp_path)
    pin = result.freeze_restore_checkpoint()
    ledger = result.ledger()
    mutated = deepcopy(ledger)
    fact = mutated["native_facts"][0]
    semantic = fact.setdefault("semantic_fields", {})
    # Change content while leaving the advertised object_id/content_hash refs stable.
    semantic["r04v_content_mutation"] = "changed"
    forged = _forge(mutated)
    with pytest.raises(Exception):
        restore_governed_frontier_ledger(forged, expected_checkpoint_ref=pin)


def test_H4_incomplete_live_result_cannot_freeze_checkpoint(tmp_path):
    bundle, compilation, result = _governed(tmp_path)
    assert result.freeze_restore_checkpoint()
    incomplete = replace(result, operation_ledger=())
    with pytest.raises(Exception):
        incomplete.freeze_restore_checkpoint()
    duplicated_refs = replace(
        result, fact_refs=result.fact_refs + (result.fact_refs[0],)
    )
    with pytest.raises(Exception):
        duplicated_refs.freeze_restore_checkpoint()


def test_H4b_duplicate_fact_refs_cannot_freeze_checkpoint(tmp_path):
    bundle, compilation, result = _governed(tmp_path)
    assert result.freeze_restore_checkpoint()
    duplicated_refs = replace(
        result, fact_refs=result.fact_refs + (result.fact_refs[0],)
    )
    with pytest.raises(Exception):
        duplicated_refs.freeze_restore_checkpoint()
