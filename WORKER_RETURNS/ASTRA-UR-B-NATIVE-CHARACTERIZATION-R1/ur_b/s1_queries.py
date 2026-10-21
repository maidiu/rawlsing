"""I03 queries for the frozen S1 instrument."""
from __future__ import annotations

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_source_backed_c11_repository, execute_source_backed_empirical_query,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _predicate, _query, _query_authority, _response_leaf,
)


def queries(fx):
    source = fx["source"]
    qa = _query_authority("ur-b-s1-query")
    all_p = _branch_predicate(source, qa, tag="s1-all")
    a1 = _predicate(source, qa, _response_leaf(source, qa, "A", 1), tag="s1-a1")
    b1 = _predicate(source, qa, _response_leaf(source, qa, "B", 1), tag="s1-b1")
    specs = {
        "DIST_A_RAW": _query(source, qa, all_p, ("A",), tag="s1-a-raw"),
        "DIST_B_RAW": _query(source, qa, all_p, ("B",), tag="s1-b-raw"),
        "DIST_Y_RAW": _query(source, qa, all_p, ("Y",), tag="s1-y-raw"),
        "DIST_A_WEIGHTED": _query(source, qa, all_p, ("A",), measure="GOVERNED_WEIGHTED", tag="s1-a-w"),
        "DIST_B_WEIGHTED": _query(source, qa, all_p, ("B",), measure="GOVERNED_WEIGHTED", tag="s1-b-w"),
        "DIST_Y_WEIGHTED": _query(source, qa, all_p, ("Y",), measure="GOVERNED_WEIGHTED", tag="s1-y-w"),
        "COND_Y_GIVEN_A1": _query(source, qa, a1, ("Y",), tag="s1-y-a1"),
        "COND_Y_GIVEN_B1": _query(source, qa, b1, ("Y",), tag="s1-y-b1"),
        "JOINT_A_B_Y": _query(source, qa, all_p, ("A", "B", "Y"), tag="s1-aby"),
        "ZERO_SUPPORT_Z": _query(source, qa, all_p, ("Z",), tag="s1-z"),
    }
    registry = AuthorityRegistry(tuple((*fx["authorities"], qa)))
    return qa, all_p, a1, b1, specs, registry


def run(fx):
    qa, all_p, a1, b1, specs, registry = queries(fx)
    repo, release = build_source_backed_c11_repository(fx["incidence"], fx["projection"])
    results = {}
    for name, spec in specs.items():
        pred = spec.condition_predicate_ref
        # Resolve the exact predicate object by ref from the small local map.
        pred_obj = next(p for p in (all_p, a1, b1) if p.ref.as_dict() == pred)
        results[name] = execute_empirical_query(
            repository=repo, query=spec, predicate=pred_obj,
            authority_registry=registry, release_refs=(release.release_ref,))
    return {"release": release, "repo": repo, "queries": specs,
            "predicates": {"all": all_p, "a1": a1, "b1": b1},
            "results": results, "qa": qa}
