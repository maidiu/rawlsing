"""I05 and Route-B/Batch-adjacent execution for S1."""
from __future__ import annotations

import rawlsing_next.pre553_route_b_production as route_b
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom, _d_auth, _discovery_authority, _grammar, _qt, _rule,
)
from ur_b.s1_queries import queries


def build(fx):
    qa, all_p, a1, b1, specs, registry = queries(fx)
    source = fx["source"]
    dauth = _d_auth("ur-b-s1-discovery")
    grammar = _grammar(
        operation="I03-OP-ur-b-s1-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("A1", a1, "RESPONSE")],
        templates=[_qt("Y", specs["DIST_Y_RAW"])],
        rules=[_rule("s1-rule", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
                     atom_ids=("A1",), baseline_atom_id="ALL",
                     query_template_id="Y",
                     validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"})],
    )
    discovery = _discovery_authority(source, grammar, dauth, tag="ur-b-s1")
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*fx["authorities"], qa, dauth)),
        predicates=(all_p, a1, b1),
        queries=tuple(specs.values()),
        discovery_authorities=(discovery,),
    )
    requests = tuple(
        route_b.I03ExecutionRequest(spec.ref, spec.condition_predicate_ref)
        for spec in specs.values())
    return {"qa": qa, "dauth": dauth, "grammar": grammar,
            "discovery": discovery, "catalog": catalog, "requests": requests,
            "predicates": {"all": all_p, "a1": a1, "b1": b1}}


def execute(fx):
    setup = build(fx)
    result = route_b.execute_route_b_production(
        source=fx["incidence"], projection=fx["projection"],
        runtime_catalog=setup["catalog"], i03_requests=setup["requests"],
        discovery_authority_ref=setup["discovery"].ref)
    return setup, result
