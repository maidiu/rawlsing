"""Native I03/F2/F4/I05 query bundle over the #1006 sourcefree fixture."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_discovery_exact import (
    COVERAGE_CLAIM,
    DiscoveryAuthority,
    execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
)
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.tests.pre553_query_frontier_fixtures import _custom_query
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _d_auth,
    _discovery_authority,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _coordinate_leaf,
    _predicate,
    _query,
    _query_authority,
    _response_leaf,
)

from fixture_1006 import (
    REPEATED_QUESTION,
    RISK_NAME,
    FixtureContext,
    source_descriptor,
)


@dataclass(frozen=True)
class QueryBundle:
    catalog: RuntimeObjectCatalog
    selected: EmpiricalQuerySpec
    selected_predicate: EmpiricalPredicate
    f2_forward: EmpiricalQuerySpec
    f2_forward_predicate: EmpiricalPredicate
    f2_reverse: EmpiricalQuerySpec
    f2_reverse_predicate: EmpiricalPredicate
    f4_three: EmpiricalQuerySpec
    f4_three_predicate: EmpiricalPredicate
    f4_four: EmpiricalQuerySpec
    f4_four_predicate: EmpiricalPredicate
    weighted: EmpiricalQuerySpec | None
    weighted_predicate: EmpiricalPredicate | None
    repeated: EmpiricalQuerySpec | None
    repeated_predicate: EmpiricalPredicate | None
    discovery_authority: DiscoveryAuthority
    requests: tuple[I03ExecutionRequest, ...]

    def by_name(self, name: str) -> tuple[EmpiricalQuerySpec, EmpiricalPredicate]:
        mapping = {
            "selected": (self.selected, self.selected_predicate),
            "f2_forward": (self.f2_forward, self.f2_forward_predicate),
            "f2_reverse": (self.f2_reverse, self.f2_reverse_predicate),
            "f4_three": (self.f4_three, self.f4_three_predicate),
            "f4_four": (self.f4_four, self.f4_four_predicate),
        }
        if self.weighted is not None:
            mapping["weighted"] = (self.weighted, self.weighted_predicate)
        if self.repeated is not None:
            mapping["repeated"] = (self.repeated, self.repeated_predicate)
        return mapping[name]


def _or_all(ctx: FixtureContext, qa: Any) -> EmpiricalPredicate:
    ast = {
        "op": "OR",
        "children": [
            _coordinate_leaf(source_descriptor(ctx), "G", "A"),
            _coordinate_leaf(source_descriptor(ctx), "G", "B"),
        ],
    }
    return _predicate(source_descriptor(ctx), qa, ast, tag=f"{ctx.tag}-all")


def build_query_bundle(ctx: FixtureContext) -> QueryBundle:
    source = source_descriptor(ctx)
    qa = _query_authority(ctx.tag)
    a1 = _predicate(
        source, qa, _response_leaf(source, qa, "A", 1), tag=f"{ctx.tag}-a1"
    )
    b1 = _predicate(
        source, qa, _response_leaf(source, qa, "B", 1), tag=f"{ctx.tag}-b1"
    )
    a1_and_b1 = _predicate(
        source, qa,
        {"op": "AND", "children": [
            _response_leaf(source, qa, "A", 1),
            _response_leaf(source, qa, "B", 1),
        ]},
        tag=f"{ctx.tag}-a1b1",
    )
    c1 = _predicate(
        source, qa, _response_leaf(source, qa, "C", 1), tag=f"{ctx.tag}-c1"
    )
    selected = _query(
        source, qa, a1, ("C",), tag=f"{ctx.tag}-selected"
    )
    f2_forward = _query(
        source, qa, a1, ("C",), tag=f"{ctx.tag}-f2-forward"
    )
    f2_reverse = _query(
        source, qa, c1, ("A",), tag=f"{ctx.tag}-f2-reverse"
    )
    f4_three = _query(
        source, qa, a1_and_b1, ("C",), tag=f"{ctx.tag}-f4-three"
    )
    f4_four = _query(
        source, qa, a1_and_b1, ("C", "D"), tag=f"{ctx.tag}-f4-four"
    )
    weighted = None
    weighted_predicate = None
    if ctx.shape.include_weights:
        weighted_predicate = a1
        weighted = _query(
            source, qa, a1, ("C",), measure="GOVERNED_WEIGHTED",
            tag=f"{ctx.tag}-weighted",
        )
    repeated_domain = []
    for index in range(ctx.shape.respondents):
        if index % ctx.shape.repeated_mod != 0:
            continue
        repeated_domain.append([
            {
                "event_id": f"{index:08d}-{REPEATED_QUESTION}-{occurrence}",
                "multiplicity_order_rank_fields": {
                    "kind": "REPEATED_EVENT",
                    "multiplicity_index": occurrence,
                    "rank": occurrence + 1,
                },
                "value": str((index + occurrence) % 3),
            }
            for occurrence in range(2)
        ])
    repeated = _custom_query(
        source, qa, a1, REPEATED_QUESTION, topology="REPEATED_EVENT",
        domain=repeated_domain, included_states=("SUBSTANTIVE_RESPONSE",),
        tag=f"{ctx.tag}-repeated",
    )
    all_predicate = _or_all(ctx, qa)
    dauth = _d_auth(f"{ctx.tag}-discovery")
    discovery_query = _query(
        source, qa, all_predicate, ("C",), tag=f"{ctx.tag}-i05-target"
    )
    grammar = _grammar(
        operation=f"I03-OP-{ctx.tag}-discovery",
        atoms=[
            _atom("ALL", all_predicate, "BRANCH"),
            _atom("A1", a1, "RESPONSE"),
        ],
        templates=[_qt("B", discovery_query)],
        rules=[
            _rule(
                "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
                atom_ids=("A1",), baseline_atom_id="ALL", query_template_id="B",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            ),
        ],
    )
    base = _discovery_authority(source, grammar, dauth)
    discovery_authority = DiscoveryAuthority(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        **{
            **dict(base.semantic_fields),
            "validation_rules": {
                "rules": ({"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},)
            },
        },
    )
    predicates = (all_predicate, a1, b1, c1, a1_and_b1)
    queries = (selected, f2_forward, f2_reverse, f4_three, f4_four, discovery_query)
    authorities = (*ctx.authorities, qa, dauth)
    if weighted is not None:
        queries = (*queries, weighted)
    if repeated is not None:
        queries = (*queries, repeated)
    catalog = RuntimeObjectCatalog(
        authorities=authorities,
        predicates=predicates,
        queries=queries,
        discovery_authorities=(discovery_authority,),
    )
    requests = (
        I03ExecutionRequest(selected.ref, a1.ref),
        I03ExecutionRequest(f2_forward.ref, a1.ref),
        I03ExecutionRequest(f2_reverse.ref, c1.ref),
        I03ExecutionRequest(f4_three.ref, a1_and_b1.ref),
        I03ExecutionRequest(f4_four.ref, a1_and_b1.ref),
    )
    return QueryBundle(
        catalog=catalog,
        selected=selected,
        selected_predicate=a1,
        f2_forward=f2_forward,
        f2_forward_predicate=a1,
        f2_reverse=f2_reverse,
        f2_reverse_predicate=c1,
        f4_three=f4_three,
        f4_three_predicate=a1_and_b1,
        f4_four=f4_four,
        f4_four_predicate=a1_and_b1,
        weighted=weighted,
        weighted_predicate=weighted_predicate,
        repeated=repeated,
        repeated_predicate=a1,
        discovery_authority=discovery_authority,
        requests=requests,
    )


def execute_bundle_oracle(
    repository: Any,
    release_ref: ExactRef,
    bundle: QueryBundle,
    *,
    qa: Any,
    dauth: Any,
) -> dict[str, Any]:
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
    from rawlsing_next.pre553_empirical_query import execute_empirical_query

    registry = AuthorityRegistry((*bundle.catalog.authorities,))
    result: dict[str, Any] = {}
    for name in ("selected", "f2_forward", "f2_reverse", "f4_three", "f4_four"):
        query, predicate = bundle.by_name(name)
        result[name] = execute_empirical_query(
            repository=repository,
            query=query,
            predicate=predicate,
            authority_registry=registry,
            release_refs=(release_ref,),
        )
    if bundle.weighted is not None:
        result["weighted"] = execute_empirical_query(
            repository=repository,
            query=bundle.weighted,
            predicate=bundle.weighted_predicate,
            authority_registry=registry,
            release_refs=(release_ref,),
        )
    if bundle.repeated is not None:
        result["repeated"] = execute_empirical_query(
            repository=repository,
            query=bundle.repeated,
            predicate=bundle.repeated_predicate,
            authority_registry=registry,
            release_refs=(release_ref,),
        )
    result["i05"] = execute_exact_bounded_discovery(
        repository=repository,
        discovery_authority=bundle.discovery_authority,
        authority_registry=registry,
        release_refs=(release_ref,),
        predicate_catalog=bundle.catalog.predicates,
        query_template_catalog=bundle.catalog.queries,
    )
    return result


__all__ = ["QueryBundle", "build_query_bundle", "execute_bundle_oracle"]
