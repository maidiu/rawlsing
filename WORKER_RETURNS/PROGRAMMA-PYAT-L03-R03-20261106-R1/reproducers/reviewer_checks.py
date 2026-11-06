"""Independent R03 discriminating checks (reviewer-authored, not implementation).

Runs the actual CarrierNeutralResearchExecutor first consumer against an
independent numeric oracle derived from the fixture rows, then exercises
same-world index cut/restore, poisoned-core refusal, and weight-basis refusal.
No source edits; outputs only reviewer evidence.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections.abc import Mapping
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from types import MappingProxyType

ROOT = Path(__file__).resolve()
while not (ROOT / 'rawlsing_next').is_dir():
    if ROOT.parent == ROOT:
        raise RuntimeError('repository root not found')
    ROOT = ROOT.parent
TOOLS = ROOT / "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(TOOLS))

import bench_common as bc  # noqa: E402
from rawlsing_next.pre553_c11_integrity import TYPED_ABSENCE_STATES  # noqa: E402
from rawlsing_next.pre553_carrier_execution import (  # noqa: E402
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
)
from rawlsing_next.pre553_empirical_objects import (  # noqa: E402
    EmpiricalQuerySpec,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import (  # noqa: E402
    I03GroupedExecutionScope,
)
from rawlsing_next.tests.pre553_query_frontier_fixtures import (  # noqa: E402
    _custom_query,
    special_state_fixture,
)
from rawlsing_next.tests.test_pre553_empirical_query import (  # noqa: E402
    _branch_predicate,
    _build_source,
    _query,
    _query_authority,
)


def frac(value):
    if value is None:
        return None
    if isinstance(value, Mapping) and "$exact_fraction" in value:
        n, d = value["$exact_fraction"]
        return Fraction(int(n), int(d))
    return Fraction(value)


def cell_key(cell):
    return tuple(cell) if isinstance(cell, list) else cell


def fact_cells(fact):
    rows = {}
    for row in fact.target_topology["complete_cell_semantic_projection"]:
        rows[cell_key(row["cell"])] = row
    return rows


def leaf_members(ast, found):
    if not isinstance(ast, Mapping):
        return
    if ast.get("op") == "LEAF":
        if ast.get("leaf_type") == "DERIVED_BRANCH_COHORT":
            found.extend(ast.get("exact_member_respondent_refs") or ())
        return
    for child in ast.get("children", ()):
        leaf_members(child, found)


def expected_for(op, rows, weights, rid_by_key):
    targets = tuple(op["targets"])
    ids = [row["id"] for row in rows]
    risk_ids = set(ids) if op["risk"] == "R" else {
        rid for index, rid in enumerate(ids) if index % 2 == 0
    }
    if op["group"] in {
        "G1_compatible", "G2_target_sibling", "G3_arity", "G7_incompatible_risk",
    }:
        condition = set(ids)
    elif op["op_id"] == "cond_X1_target_Y":
        condition = {row["id"] for row in rows if int(row["responses"]["X"]) == 1}
    elif op["op_id"] == "cond_Y1_target_X":
        condition = {row["id"] for row in rows if int(row["responses"]["Y"]) == 1}
    elif op["op_id"] == "xor_condition_target_Z":
        condition = {
            row["id"] for row in rows
            if int(row["responses"]["X"]) != int(row["responses"]["Y"])
        }
    elif op["op_id"] == "minority_branch_target_K":
        refs = []
        leaf_members(op["predicate"].predicate_ast, refs)
        condition = {
            rid_by_key[exact_ref(ref, "branch_member").key] for ref in refs
        }
    else:
        raise AssertionError(op["op_id"])
    denominator = [rid for rid in ids if rid in risk_ids and rid in condition]
    domain = list(itertools.product(("0", "1"), repeat=len(targets)))
    domain = [cell[0] if len(targets) == 1 else tuple(cell) for cell in domain]
    raw_cells = {cell: 0 for cell in domain}
    weighted_cells = {cell: Fraction(0, 1) for cell in domain}
    by_id = {row["id"]: row for row in rows}
    for rid in denominator:
        row = by_id[rid]
        cell = (
            str(row["responses"][targets[0]]) if len(targets) == 1
            else tuple(str(row["responses"][target]) for target in targets)
        )
        assert cell in raw_cells, (op["op_id"], cell, sorted(raw_cells))
        raw_cells[cell] += 1
        weighted_cells[cell] += Fraction(int(weights[rid][1]))
    denominator_set = set(denominator)
    return {
        "typed_state": "SUPPORTED" if denominator else "ZERO_SUPPORT",
        "risk_ids": risk_ids,
        "denominator": denominator,
        "domain": set(domain),
        "raw_cells": raw_cells,
        "weighted_cells": (
            weighted_cells if op["measure"] == "GOVERNED_WEIGHTED" else None
        ),
        "weighted_denominator": (
            sum((Fraction(int(weights[rid][1])) for rid in denominator), Fraction(0, 1))
            if op["measure"] == "GOVERNED_WEIGHTED" else None
        ),
    }


def assert_fact_matches(fact, expected, op, rid_by_key):
    assert fact.typed_state == expected["typed_state"], (
        op["op_id"], fact.typed_state, expected["typed_state"]
    )
    assert fact.measure_kind == op["measure"]
    assert fact.raw_denominator_support == len(expected["denominator"]), op["op_id"]
    assert fact.raw_numerator_support == len(expected["denominator"]), op["op_id"]
    assert fact.raw_resolved_target_support == len(expected["denominator"]), op["op_id"]
    risk_ids = {
        rid_by_key[exact_ref(ref, "risk_set_member_refs").key]
        for ref in fact.risk_set_member_refs
    }
    denominator_ids = {
        rid_by_key[exact_ref(ref, "denominator_member_refs").key]
        for ref in fact.denominator_member_refs
    }
    assert risk_ids == expected["risk_ids"], op["op_id"]
    assert denominator_ids == set(expected["denominator"]), op["op_id"]
    cells = fact_cells(fact)
    assert set(cells) == expected["domain"], (op["op_id"], sorted(cells))
    for key in expected["domain"]:
        row = cells[key]
        raw = expected["raw_cells"][key]
        assert row["raw_numerator_support"] == raw, (op["op_id"], key)
        if raw > 0:
            assert row["cell_state"] == "OBSERVED_POSITIVE"
        elif expected["denominator"]:
            assert row["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
        else:
            assert row["cell_state"] == "ZERO_SUPPORT"
        weighted = frac(row["weighted_numerator_support_if_authorized"])
        if op["measure"] == "GOVERNED_WEIGHTED":
            assert weighted == expected["weighted_cells"][key], (op["op_id"], key)
        else:
            assert weighted is None, (op["op_id"], key)
    assert frac(fact.weighted_denominator_support_if_authorized) == (
        expected["weighted_denominator"]
    ), op["op_id"]
    weighted_sum = sum(expected["weighted_cells"].values()) if expected["weighted_cells"] else None
    assert frac(fact.weighted_numerator_support_if_authorized) == weighted_sum, op["op_id"]


def run_all(executor, ops, scope=None):
    results = {}
    for op in ops:
        result = executor.execute_i03(
            query_ref=op["query"].ref,
            predicate_ref=op["predicate"].ref,
            group_scope=scope,
        )
        assert len(result.facts) == 1, op["op_id"]
        results[op["op_id"]] = result.facts[0]
    return results


def main():
    data = bc.build_main_source(200)
    source, catalog, ops = data["source"], data["catalog"], data["ops"]
    release = source["repo"].resolve_release_exact(source["release_ref"])
    rid_by_key = {
        respondent.ref.key: rid for rid, respondent in source["respondents"].items()
    }
    expected = {
        op["op_id"]: expected_for(op, data["rows"], data["weights"], rid_by_key)
        for op in ops
    }

    baseline_executor = CarrierNeutralResearchExecutor(
        bc.fresh_repository(release), (release.release_ref,), catalog,
    )
    candidate_executor = CarrierNeutralResearchExecutor(
        bc.fresh_repository(release), (release.release_ref,), catalog,
    )
    baseline = run_all(baseline_executor, ops)
    scope = I03GroupedExecutionScope()
    candidate = run_all(candidate_executor, ops, scope)
    receipt_after_cold = dict(scope.receipt())

    for op in ops:
        assert_fact_matches(baseline[op["op_id"]], expected[op["op_id"]], op, rid_by_key)
        assert_fact_matches(candidate[op["op_id"]], expected[op["op_id"]], op, rid_by_key)
        assert baseline[op["op_id"]].as_dict() == candidate[op["op_id"]].as_dict(), op["op_id"]
        assert baseline[op["op_id"]].ref == candidate[op["op_id"]].ref, op["op_id"]
        assert baseline[op["op_id"]].replay_ref == candidate[op["op_id"]].replay_ref, op["op_id"]
    assert receipt_after_cold["core_builds"] == 11
    assert receipt_after_cold["core_hits"] == 2
    assert receipt_after_cold["fallbacks"] == 0

    # Same-world index cut: remove the attested repository index, re-evaluate,
    # then restore the exact prior index object and re-evaluate.
    repository = candidate_executor.repository
    index_key = next(iter(repository._i03_release_indices))
    original_index = repository._i03_release_indices[index_key]
    original_attestation = repository._i03_index_attestations[index_key]
    repository._i03_release_indices.pop(index_key)
    repository._i03_index_attestations.pop(index_key)
    cut = run_all(candidate_executor, ops, scope)
    rebuilt_index = repository._i03_release_indices[index_key]
    assert rebuilt_index is not original_index
    receipt_after_cut = dict(scope.receipt())
    assert receipt_after_cut["core_builds"] == receipt_after_cold["core_builds"] + 11
    for op in ops:
        assert cut[op["op_id"]].as_dict() == baseline[op["op_id"]].as_dict(), op["op_id"]
        assert cut[op["op_id"]].replay_ref == baseline[op["op_id"]].replay_ref, op["op_id"]
    repository._i03_release_indices[index_key] = original_index
    repository._i03_index_attestations[index_key] = original_attestation
    restored = run_all(candidate_executor, ops, scope)
    receipt_after_restore = dict(scope.receipt())
    assert receipt_after_restore["core_builds"] == receipt_after_cut["core_builds"]
    assert receipt_after_restore["core_hits"] == receipt_after_cut["core_hits"] + 13
    for op in ops:
        assert restored[op["op_id"]].as_dict() == baseline[op["op_id"]].as_dict(), op["op_id"]

    # Poisoned core must be detected and must not publish a forged SUPPORTED fact.
    poison_key = next(iter(scope._cache))
    true_core = scope._cache[poison_key]
    poison_variants = {}
    forged_raw = dict(true_core.raw_cells)
    first_cell = next(iter(forged_raw))
    forged_raw[first_cell] = forged_raw[first_cell] + 999
    poison_variants["raw_cells"] = replace(
        true_core, raw_cells=MappingProxyType(forged_raw),
    )
    poison_variants["fact_state"] = replace(true_core, fact_state="ZERO_SUPPORT")
    forged_by_respondent = dict(true_core.cell_by_respondent)
    if forged_by_respondent:
        first_member = next(iter(forged_by_respondent))
        forged_by_respondent[first_member] = "__R03_FORGED_CELL__"
        poison_variants["cell_by_respondent"] = replace(
            true_core, cell_by_respondent=MappingProxyType(forged_by_respondent),
        )
    if true_core.used_objects:
        poison_variants["used_objects"] = replace(
            true_core, used_objects=true_core.used_objects[:-1],
        )
    if true_core.used_authority_refs:
        poison_variants["used_authority_refs"] = replace(
            true_core, used_authority_refs=true_core.used_authority_refs[:-1],
        )
    fingerprint_failure_counts = {}
    for label, forged_core in poison_variants.items():
        before = scope.receipt()["fingerprint_failures"]
        scope._cache[poison_key] = forged_core
        poisoned = run_all(candidate_executor, ops, scope)
        after = scope.receipt()["fingerprint_failures"]
        assert after > before, label
        for op in ops:
            assert poisoned[op["op_id"]].as_dict() == baseline[op["op_id"]].as_dict(), op["op_id"]
            assert poisoned[op["op_id"]].ref == baseline[op["op_id"]].ref, op["op_id"]
        scope._cache[poison_key] = true_core
        fingerprint_failure_counts[label] = after - before
    receipt_after_poison = dict(scope.receipt())
    repaired = run_all(candidate_executor, ops, scope)
    for op in ops:
        assert repaired[op["op_id"]].as_dict() == baseline[op["op_id"]].as_dict(), op["op_id"]

    # Weight-basis refusal: no W2 weights exist, so both paths must publish the
    # same typed negative, never a shared SUPPORTED core.
    weighted_op = next(op for op in ops if op["op_id"] == "all_K_weighted")
    base_query = weighted_op["query"]
    fields = dict(base_query.semantic_fields)
    grain = dict(fields["requested_output_grain"])
    grain["weight_basis_id"] = "W2"
    fields["requested_output_grain"] = grain
    w2_query = EmpiricalQuerySpec(
        typed_state=base_query.typed_state,
        authority_snapshot_refs=base_query.authority_snapshot_refs,
        dependency_refs=base_query.dependency_refs,
        producer_replay_locator_or_reference_root=(
            base_query.producer_replay_locator_or_reference_root
        ),
        **fields,
    )
    w2_catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], data["qa"])),
        predicates=(weighted_op["predicate"],),
        queries=(w2_query,),
        discovery_authorities=(),
    )
    w2_base_executor = CarrierNeutralResearchExecutor(
        bc.fresh_repository(release), (release.release_ref,), w2_catalog,
    )
    w2_cand_executor = CarrierNeutralResearchExecutor(
        bc.fresh_repository(release), (release.release_ref,), w2_catalog,
    )
    w2_scope = I03GroupedExecutionScope()
    w2_base = w2_base_executor.execute_i03(
        query_ref=w2_query.ref, predicate_ref=weighted_op["predicate"].ref,
    )
    w2_cand = w2_cand_executor.execute_i03(
        query_ref=w2_query.ref, predicate_ref=weighted_op["predicate"].ref,
        group_scope=w2_scope,
    )
    assert w2_base.facts[0].as_dict() == w2_cand.facts[0].as_dict()
    assert w2_base.facts[0].ref == w2_cand.facts[0].ref
    assert w2_base.facts[0].typed_state == "UNAVAILABLE"
    assert w2_base.facts[0].p02_failure_state == "MEASURE_UNAVAILABLE"
    assert w2_scope.receipt()["fallbacks"] >= 1

    # Zero support through the real consumer.
    qa = _query_authority("r03-review-zero")
    empty_predicate = _branch_predicate(source, qa, members=(), tag="r03-review-empty")
    empty_query = _query(source, qa, empty_predicate, ("K",), tag="r03-review-empty-q")
    empty_catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qa)),
        predicates=(empty_predicate,),
        queries=(empty_query,),
        discovery_authorities=(),
    )
    empty_base_executor = CarrierNeutralResearchExecutor(
        bc.fresh_repository(release), (release.release_ref,), empty_catalog,
    )
    empty_cand_executor = CarrierNeutralResearchExecutor(
        bc.fresh_repository(release), (release.release_ref,), empty_catalog,
    )
    empty_scope = I03GroupedExecutionScope()
    empty_base = empty_base_executor.execute_i03(
        query_ref=empty_query.ref, predicate_ref=empty_predicate.ref,
    )
    empty_cand = empty_cand_executor.execute_i03(
        query_ref=empty_query.ref, predicate_ref=empty_predicate.ref,
        group_scope=empty_scope,
    )
    assert empty_base.facts[0].as_dict() == empty_cand.facts[0].as_dict()
    assert empty_base.facts[0].typed_state == "ZERO_SUPPORT"

    # Typed MISSING/DK/REFUSAL/IAP/NOT_ASKED fixture through the consumer.
    special_source, baseline_fact, event_states, routing_states = special_state_fixture()
    special_qa = _query_authority("r03-review-special")
    special_predicate = _branch_predicate(special_source, special_qa, tag="r03-all")
    domain = [
        "1",
        {"typed_response_state": "MISSING"},
        {"typed_response_state": "DK"},
        {"typed_response_state": "REFUSAL"},
        {"typed_response_state": "IAP"},
        {"typed_response_state": "NOT_ASKED"},
    ]
    special_query = _custom_query(
        special_source, special_qa, special_predicate, "Q",
        topology="SCALAR_SINGULAR", domain=domain,
        included_states=(
            "SUBSTANTIVE_RESPONSE", "MISSING", "DK", "REFUSAL", "IAP", "NOT_ASKED",
        ),
        tag="r03-review-special",
    )
    special_catalog = RuntimeObjectCatalog(
        authorities=tuple((*special_source["authorities"], special_qa)),
        predicates=(special_predicate,),
        queries=(special_query,),
        discovery_authorities=(),
    )
    special_release = special_source["repo"].resolve_release_exact(
        special_source["release_ref"]
    )
    special_base_executor = CarrierNeutralResearchExecutor(
        bc.fresh_repository(special_release), (special_release.release_ref,),
        special_catalog,
    )
    special_cand_executor = CarrierNeutralResearchExecutor(
        bc.fresh_repository(special_release), (special_release.release_ref,),
        special_catalog,
    )
    special_scope = I03GroupedExecutionScope()
    special_base = special_base_executor.execute_i03(
        query_ref=special_query.ref, predicate_ref=special_predicate.ref,
    )
    special_cand = special_cand_executor.execute_i03(
        query_ref=special_query.ref, predicate_ref=special_predicate.ref,
        group_scope=special_scope,
    )
    assert special_base.facts[0].as_dict() == special_cand.facts[0].as_dict()
    assert (
        special_cand.facts[0].target_topology["complete_cell_semantic_projection"]
        == baseline_fact.target_topology["complete_cell_semantic_projection"]
    )
    assert special_cand.facts[0].raw_denominator_support == baseline_fact.raw_denominator_support
    assert special_cand.facts[0].typed_state == baseline_fact.typed_state == "SUPPORTED"
    assert "NOT_ADMINISTERED" not in TYPED_ABSENCE_STATES
    assert event_states == (
        "DK", "IAP", "MISSING", "NOT_ASKED", "REFUSAL", "SUBSTANTIVE_RESPONSE",
    )
    assert routing_states == ("ELIGIBLE_APPLICABLE", "INAPPLICABLE", "NOT_ASKED")

    receipt = {
        "schema": "R03_INDEPENDENT_DISCRIMINATING_CHECKS@1",
        "n": 200,
        "ops": len(ops),
        "independent_oracle": "PASS",
        "baseline_equals_candidate_full_as_dict_for_all_ops": True,
        "cold_scope_receipt": receipt_after_cold,
        "same_world_cut_rebuild_parity": True,
        "same_world_cut_scope_receipt": receipt_after_cut,
        "same_world_restore_hit_parity": True,
        "same_world_restore_scope_receipt": receipt_after_restore,
        "poisoned_core_refused": True,
        "poison_variants_detected": fingerprint_failure_counts,
        "poisoned_scope_receipt": receipt_after_poison,
        "weight_basis_refusal_parity": True,
        "zero_support_parity": True,
        "typed_special_state_parity": True,
        "not_administered_limitation": (
            "C11/I03 has no NOT_ADMINISTERED typed state; no state invented."
        ),
        "sample_fact_digests": {
            op_id: {
                "fact": fact.ref.as_dict(),
                "replay": exact_ref(fact.replay_ref, "replay_ref").as_dict(),
                "material_sha256": semantic_hash(fact.as_dict()),
            }
            for op_id, fact in baseline.items()
        },
    }
    out = ROOT / ".local-logs/pyat-l03-r03/evidence/reviewer-discriminating.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=1, sort_keys=True))
    print(json.dumps({
        "status": "PASS",
        "cold": receipt_after_cold,
        "cut_builds": receipt_after_cut["core_builds"],
        "restore_hits": receipt_after_restore["core_hits"],
        "poison_fingerprint_failures": receipt_after_poison["fingerprint_failures"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
