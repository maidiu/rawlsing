"""I03 queries for the frozen S2 person/household contrast."""
from __future__ import annotations

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec, ExactRef
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _coordinate_leaf, _predicate, _query_authority, _ref,
)


def _query_domain(source, qauth, predicate, targets, *, domain, measure="RAW", tag="q"):
    components = [{
        "target_ref": source["qrefs"][target],
        "topology": "SCALAR_SINGULAR",
        "domain": [str(value) for value in domain],
        "target_domain_replay_ref": _ref("TARGET_DOMAIN", f"{target}-{'|'.join(map(str, domain))}"),
        "topology_authority_refs": [source["source_auth"].authority_ref],
        "response_semantic_authority_refs": [source["source_auth"].authority_ref],
        "included_states": ["SUBSTANTIVE_RESPONSE"],
    } for target in targets]
    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": measure,
        "risk_set_type": "WHOLE_QUESTION_RISK_SET",
        "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
    }
    if measure == "GOVERNED_WEIGHTED":
        grain["weight_basis_id"] = "W"
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(qauth.authority_ref,),
        dependency_refs=(predicate.ref,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"query-{tag}"),
        target_refs=tuple(source["qrefs"][target] for target in targets),
        target_arity_and_topology={
            "arity": len(targets), "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": components},
        condition_predicate_ref=predicate.ref,
        risk_set_ref=source["risk_refs"]["R"],
        empirical_universe_refs=(source["universe"].ref,),
        scope_refs=(source["universe"].ref,),
        measure_basis_ref=_ref("MEASURE_BASIS", measure),
        requested_output_grain=grain,
        query_authority_refs=(qauth.authority_ref,),
    )


def run_person(fx):
    source = fx["source"]
    qa = _query_authority("ur-b-s2-person-query")
    allp = _branch_predicate(source, qa, tag="s2-all")
    half = _predicate(source, qa, {
        "op": "OR", "children": [
            _coordinate_leaf(source, "HID", 0),
            _coordinate_leaf(source, "HID", 1),
            _coordinate_leaf(source, "HID", 2),
            _coordinate_leaf(source, "HID", 3),
        ]}, tag="s2-half")
    specs = {
        "OUTCOME_WEIGHTED": _query_domain(source, qa, allp, ("OUTCOME",),
                                          domain=(0, 1, 2), measure="GOVERNED_WEIGHTED", tag="s2-out"),
        "PITEM_P1_WEIGHTED": _query_domain(source, qa, allp, ("PITEM",),
                                           domain=(0, 1, 2), measure="GOVERNED_WEIGHTED", tag="s2-pitem"),
        "PITEM_B_P1_WEIGHTED": _query_domain(source, qa, allp, ("PITEM_B",),
                                             domain=(0, 1, 2), measure="GOVERNED_WEIGHTED", tag="s2-pitemb"),
        "OUTCOME_HOUSEHOLD_HALF": _query_domain(source, qa, half, ("OUTCOME",),
                                                domain=(0, 1, 2), measure="GOVERNED_WEIGHTED", tag="s2-half"),
    }
    registry = AuthorityRegistry(tuple((*fx["authorities"], qa)))
    repo, release = build_source_backed_c11_repository(fx["incidence"], fx["projection"])
    results = {}
    for name, spec in specs.items():
        pred = next(p for p in (allp, half) if p.ref.as_dict() == spec.condition_predicate_ref)
        results[name] = execute_empirical_query(
            repository=repo, query=spec, predicate=pred,
            authority_registry=registry, release_refs=(release.release_ref,))
    return {"release": release, "repo": repo, "specs": specs,
            "predicates": {"all": allp, "half": half}, "results": results, "qa": qa}


def cross_unit_attempt(person_fx, household_fx):
    """A person outcome conditioned on a household universe ref, if accepted."""
    source = person_fx["source"]
    qa = _query_authority("ur-b-s2-cross")
    allp = _branch_predicate(source, qa, tag="s2-cross-all")
    from rawlsing_next.tests.test_pre553_empirical_query import _query
    spec = _query(source, qa, allp, ("OUTCOME",), measure="RAW",
                  source_mode="SOURCE_INDEXED_MULTI_UNIVERSE",
                  universe_refs=(source["universe"].ref,
                                 household_fx["source"]["universe"].ref),
                  tag="s2-cross")
    registry = AuthorityRegistry(tuple((*person_fx["authorities"], qa)))
    repo, release = build_source_backed_c11_repository(
        person_fx["incidence"], person_fx["projection"])
    try:
        result = execute_empirical_query(
            repository=repo, query=spec, predicate=allp,
            authority_registry=registry, release_refs=(release.release_ref,))
        return {"accepted": True, "typed_state": result.facts[0].typed_state,
                "release": release.release_ref}
    except Exception as exc:
        return {"accepted": False, "error_type": type(exc).__name__, "error": str(exc)}


def run_household(fx):
    source = fx["source"]
    qa = _query_authority("ur-b-s2-house-query")
    allp = _branch_predicate(source, qa, tag="s2-house-all")
    from rawlsing_next.tests.test_pre553_empirical_query import _query
    spec = _query(source, qa, allp, ("HMEAS",), measure="RAW", tag="s2-house")
    registry = AuthorityRegistry(tuple((*fx["authorities"], qa)))
    repo, release = build_source_backed_c11_repository(fx["incidence"], fx["projection"])
    result = execute_empirical_query(
        repository=repo, query=spec, predicate=allp,
        authority_registry=registry, release_refs=(release.release_ref,))
    return {"release": release, "result": result, "spec": spec}
