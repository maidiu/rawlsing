"""Independent G5 native positive witness and changed-input discovery/restore.

Uses the frozen native five-unit sourcefree Batch and existing test builders.
No substitutive calculator: F1/F2/F3/F4 come from execute_i03/execute_i05.
"""
from __future__ import annotations

import json
import resource
import sys

from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _build_source, _predicate, _query, _query_authority,
    _response_leaf, _coordinate_leaf,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom, _d_auth, _discovery_authority, _grammar, _qt, _rule,
)
from rawlsing_next.tests.test_pyat919_s2e_a_whole_native_batch import _batch
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog

SOURCE_SUFFIXES = (".sav", ".dta", ".parquet", ".csv", ".rdata", ".rds", ".xpt")
source_opens = []

def audit(event, args):
    if event == "open" and args and isinstance(args[0], str):
        if args[0].lower().endswith(SOURCE_SUFFIXES):
            source_opens.append(args[0])

sys.addaudithook(audit)

def make_case(*, all_y_one=False):
    rows = [
        {"id": f"A{i}", "responses": {"X": i % 2, "Y": 1 if all_y_one else 0, "Z": i % 2},
         "coords": {"G": "A"}}
        for i in range(10)
    ]
    rows.extend([
        {"id": "C1", "responses": {"X": 1, "Y": 1, "Z": 0}, "coords": {"G": "C"}},
        {"id": "C2", "responses": {"X": 0, "Y": 1, "Z": 1}, "coords": {"G": "C"}},
    ])
    tag = "pyat919-s2e-all-families" + ("-ally1" if all_y_one else "")
    source = _build_source(tag, rows)
    qa = _query_authority("pyat919-s2e-queries" + ("-ally1" if all_y_one else ""))
    da = _d_auth("pyat919-s2e-discovery")
    allp = _branch_predicate(source, qa, tag="all")
    px = _predicate(source, qa, _response_leaf(source, qa, "X", 1), tag="x1")
    py = _predicate(source, qa, _response_leaf(source, qa, "Y", 1), tag="y1")
    pc = _predicate(source, qa, _coordinate_leaf(source, "G", "C"), tag="minority-c")
    f1 = _query(source, qa, allp, ("Y",), tag="F1-MARGINAL")
    f2yx = _query(source, qa, px, ("Y",), tag="F2-Y-GIVEN-X")
    f2xy = _query(source, qa, py, ("X",), tag="F2-X-GIVEN-Y")
    f4 = _query(source, qa, allp, ("X", "Y", "Z"), tag="F4-JOINT")
    grammar = _grammar(
        operation="I03-OP-pyat919-s2e-discovery",
        atoms=(_atom("ALL", allp, "BRANCH"), _atom("MIN", pc, "COORDINATE")),
        templates=(_qt("F1", f1),),
        rules=(_rule(
            "minority", "MINORITY_OR_NONMODAL_DEPARTURE", "SINGLE_ATOM",
            atom_ids=("MIN",), baseline_atom_id="ALL", query_template_id="F1",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        ),),
    )
    discovery = _discovery_authority(source, grammar, da, tag="s2e-all")
    catalog = RuntimeObjectCatalog(
        authorities=(*source["authorities"], qa, da),
        predicates=(allp, px, py, pc),
        queries=(f1, f2yx, f2xy, f4),
        discovery_authorities=(discovery,),
    )
    return source, catalog, ((f1, allp), (f2yx, px), (f2xy, py), (f4, allp)), discovery

def run(case):
    with I03GroupedExecutionScope() as scope:
        manifest, receipts, outputs, census, elapsed, calls = _batch(case, scope=scope)
    return manifest, receipts, outputs, census, elapsed, calls

def fact_summary(fact):
    cells = []
    for row in fact.target_topology.get("complete_cell_semantic_projection", ()):
        d = dict(row)
        cell = d["cell"]
        if isinstance(cell, (list, tuple)):
            cell = list(cell)
        cells.append({"cell": cell, "count": d["raw_numerator_support"], "state": d["cell_state"]})
    return {
        "typed_state": fact.typed_state,
        "denominator": fact.raw_denominator_support,
        "numerator": fact.raw_numerator_support,
        "resolved": fact.raw_resolved_target_support,
        "denominator_member_refs": len(fact.denominator_member_refs),
        "risk_member_refs": len(fact.risk_set_member_refs),
        "arity": fact.target_topology.get("arity"),
        "cells": cells,
        "target_domain_identity": fact.target_domain_identity,
        "query_contract": fact.query_execution_contract_id,
        "provenance_refs": len(fact.source_empirical_provenance_refs),
        "universe_refs": len(fact.empirical_universe_refs),
    }

baseline_case = make_case()
manifest, receipts, outputs, baseline, elapsed, calls = run(baseline_case)
by_query = {}
for unit in manifest.units:
    if unit.job_kind == "QUERY":
        out = outputs[unit.unit_hash]
        by_query[unit.job_ref.object_id] = {
            "fact_ref": out.facts[0].ref.object_id,
            "summary": fact_summary(out.facts[0]),
        }
    else:
        disc = outputs[unit.unit_hash]
        by_query["DISCOVERY"] = {
            "contract_id": disc.contract_id,
            "valid_empty": disc.valid_empty,
            "candidate_count": disc.candidate_count,
            "empirical_fact_count": len(disc.empirical_facts),
            "executed_predicates": len(disc.executed_predicates),
            "executed_queries": len(disc.executed_queries),
            "receipts": [
                {
                    "typed_state": r.typed_state,
                    "coverage_state": r.coverage_state,
                    "query_contract": r.exact_query_contract_id,
                    "diagnostic_promoted": r.diagnostic_score_is_empirical_fact,
                    "structural_effect": r.structural_truth_effect,
                    "actor_effect": r.actor_v3_effect,
                    "candidate_hash": r.candidate_identity["candidate_hash"],
                    "dependency_refs": len(r.dependency_refs),
                    "authority_snapshot_refs": len(r.authority_snapshot_refs),
                    "empirical_fact_refs": len(r.empirical_fact_refs),
                    "support_uncertainty": dict(r.support_uncertainty_state),
                }
                for r in disc.receipts
            ],
        }

changed_case = make_case(all_y_one=True)
c_manifest, c_receipts, c_outputs, c_census, c_elapsed, c_calls = run(changed_case)
c_disc_unit = next(u for u in c_manifest.units if u.job_kind == "DISCOVERY")
changed_disc = c_outputs[c_disc_unit.unit_hash]

restored_manifest, restored_receipts, restored_outputs, restored, r_elapsed, r_calls = run(make_case())
from rawlsing_next.pre553_s2e_exact_conservation import require_same_native_output_graph
require_same_native_output_graph(baseline, restored)

print("S2E_POSITIVE_WITNESS_JSON=" + json.dumps({
    "schema": "PYAT_S2E_INDEPENDENT_NATIVE_WITNESS@1",
    "sourcefree_universe_respondents": 12,
    "batch_units": len(manifest.units),
    "calls": calls,
    "grouped_core_builds": None,
    "elapsed_seconds": round(elapsed, 6),
    "full_output_sha256": baseline.full_output_sha256,
    "i03_fact_count": baseline.i03_fact_count,
    "i05_fact_count": baseline.i05_fact_count,
    "i05_receipt_count": baseline.i05_receipt_count,
    "typed_state_counts": dict(baseline.typed_state_counts),
    "units": by_query,
    "changed_input_discovery": {
        "valid_empty": changed_disc.valid_empty,
        "receipt_states": [r.typed_state for r in changed_disc.receipts],
        "coverage_states": [r.coverage_state for r in changed_disc.receipts],
        "frontier_ref": changed_disc.evaluated_frontier_ref.object_id,
        "replay_ref": changed_disc.replay_ref.object_id,
    },
    "restored_full_output_sha256": restored.full_output_sha256,
    "restore_identical": restored.as_dict() == baseline.as_dict(),
    "actual_source_file_opens_during_all_runs": source_opens,
    "process_maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}, sort_keys=True, default=str))
