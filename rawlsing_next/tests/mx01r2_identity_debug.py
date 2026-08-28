#!/usr/bin/env python3
from rawlsing_next.pre553_discovery_exact import (
    _catalog_atoms, _catalog_templates, _compile_frontier, _verify_discovery_authority,
    execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_recursive_handoff import _compose_predicates
from rawlsing_next.tests.test_pre553_recursive_handoff import _fixture, _respondents
from rawlsing_next.tests.test_pre553_discovery_exact import _atom, _d_auth, _discovery_authority, _grammar, _qt, _rule
from rawlsing_next.tests.test_pre553_empirical_query import _branch_predicate, _predicate, _query, _registry, _response_leaf

source, qauth = _fixture()
parent = _branch_predicate(source, qauth, members=_respondents(source, ("R1","R2","R3","R4","R5","R6")), tag="mx01r2-parent")
x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="mx01r2-x1")
xq = _query(source, qauth, parent, ("X",), tag="mx01r2-g1-x")
dauth = _d_auth("mx01r2-g1-discovery")
grammar = _grammar(operation="I03-OP-mx01r2-g1-discovery", atoms=[_atom("PARENT", parent, "BRANCH"), _atom("X1", x1, "RESPONSE")], templates=[_qt("X", xq)], rules=[_rule("child", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM", atom_ids=("X1",), baseline_atom_id="PARENT", query_template_id="X", validation={"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"})], k=2)
authority = _discovery_authority(source, grammar, dauth, tag="mx01r2-g1")
registry = _registry(source, qauth, dauth)
result = execute_exact_bounded_discovery(repository=source["repo"], discovery_authority=authority, authority_registry=registry, release_refs=(source["release_ref"],), predicate_catalog=(parent,x1), query_template_catalog=(xq,))
definition = _verify_discovery_authority(authority, registry)
private = _compile_frontier(definition, _catalog_atoms(definition,(parent,x1)), _catalog_templates(definition,(xq,)))[0].winning_predicate
public = _compose_predicates((parent,x1), op="AND", tag_material={"rule":"child","baseline":"PARENT","condition":x1.ref.as_dict()})
print("receipt", result.receipts[0].winning_predicate_ref.as_dict())
print("private", private.ref.as_dict())
print("public ", public.ref.as_dict())
pp = private.semantic_projection(); qp = public.semantic_projection()
for key in sorted(set(pp)|set(qp)):
    if pp.get(key) != qp.get(key):
        print("DIFF", key)
        print("  private=", pp.get(key))
        print("  public =", qp.get(key))
