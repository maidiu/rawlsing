"""I03 query for the S3 repeated SCORE contrast."""
from __future__ import annotations

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _query_authority, _ref,
)


def run(fx, release=None):
    source = fx["source"]
    qa = _query_authority("ur-b-s3-query")
    allp = _branch_predicate(source, qa, tag="s3-all")
    components = [{
        "target_ref": source["qrefs"]["SCORE"],
        "topology": "SCALAR_SINGULAR",
        "domain": ["0", "1", "2"],
        "target_domain_replay_ref": _ref("TARGET_DOMAIN", "score-012"),
        "topology_authority_refs": [source["source_auth"].authority_ref],
        "response_semantic_authority_refs": [source["source_auth"].authority_ref],
        "included_states": ["SUBSTANTIVE_RESPONSE"],
    }]
    spec = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(qa.authority_ref,),
        dependency_refs=(allp.ref,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "s3-query"),
        target_refs=(source["qrefs"]["SCORE"],),
        target_arity_and_topology={
            "arity": 1, "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": components},
        condition_predicate_ref=allp.ref,
        risk_set_ref=source["risk_refs"]["R"],
        empirical_universe_refs=(source["universe"].ref,),
        scope_refs=(source["universe"].ref,),
        measure_basis_ref=_ref("MEASURE_BASIS", "RAW"),
        requested_output_grain={
            "source_scope_mode": "SINGLE_UNIVERSE", "measure_kind": "RAW",
            "risk_set_type": "WHOLE_QUESTION_RISK_SET",
            "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"),
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
        },
        query_authority_refs=(qa.authority_ref,),
    )
    registry = AuthorityRegistry(tuple((*fx["authorities"], qa)))
    repo, rel = (build_source_backed_c11_repository(fx["incidence"], fx["projection"])
                 if release is None else (release[0], release[1]))
    result = execute_empirical_query(
        repository=repo, query=spec, predicate=allp,
        authority_registry=registry, release_refs=(rel.release_ref,))
    return {"spec": spec, "result": result, "release": rel, "qa": qa}
