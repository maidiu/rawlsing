"""Real BatchExecutionRunner over S1 query and discovery units."""
from __future__ import annotations

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec, ExecutionOutcome,
    ExecutorBinding,
)
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from ur_b.s1_queries import queries
from ur_b.s1_route_b import build as route_build


def run(fx):
    qa, allp, a1, b1, specs, registry = queries(fx)
    route_setup = route_build(fx)
    repo, release = build_source_backed_c11_repository(fx["incidence"], fx["projection"])
    registry = route_setup["catalog"].authority_registry
    by_query = {spec.ref.key: spec for spec in specs.values()}
    by_pred = {allp.ref.key: allp, a1.ref.key: a1, b1.ref.key: b1}
    units = []
    units = []
    for name in ("DIST_A_RAW", "DIST_Y_RAW", "COND_Y_GIVEN_A1"):
        spec = specs[name]
        pred = next(p for p in (allp, a1, b1) if p.ref.as_dict() == spec.condition_predicate_ref)
        units.append(BatchUnitSpec("QUERY", spec.ref, (release.release_ref,), (pred.ref,)))
    discovery = route_setup["discovery"]
    units.append(BatchUnitSpec("DISCOVERY", discovery.ref, (release.release_ref,), ()))
    manifest = BatchManifest(tuple(units))
    runner = BatchExecutionRunner(manifest=manifest, repository=repo)

    def run_query(unit):
        spec = by_query[unit.job_ref.key]
        pred = by_pred[unit.semantic_input_refs[0].key]
        result = execute_empirical_query(
            repository=repo, query=spec, predicate=pred,
            authority_registry=registry, release_refs=(release.release_ref,))
        return ExecutionOutcome(result_refs=tuple(f.ref for f in result.facts))

    def run_discovery(unit):
        result = execute_exact_bounded_discovery(
            repository=repo, discovery_authority=discovery,
            authority_registry=registry, release_refs=(release.release_ref,),
            predicate_catalog=route_setup["catalog"].predicates,
            query_template_catalog=route_setup["catalog"].queries)
        return ExecutionOutcome(result_refs=tuple(r.ref for r in result.receipts))

    executors = {
        "QUERY": ExecutorBinding(ExactRef("EXECUTOR", "ur-b-s1-query", "a" * 64), run_query),
        "DISCOVERY": ExecutorBinding(ExactRef("EXECUTOR", "ur-b-s1-discovery", "b" * 64), run_discovery),
    }
    receipts = runner.run(executors=executors)
    return {"manifest": manifest, "runner": runner, "receipts": receipts,
            "release": release, "repo": repo}
