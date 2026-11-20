"""Country issuance proof across a genuinely MULTI-country source universe.

Tests the real EmpiricalUniverse/Predicate/Query/AuthorityRegistry identity
chain before I03's multi-country source native first-reader is claimed.
Unlike the US-only I03+S04 vertical fixture, these tests exercise
the *multinational source-semantic authority* contract in isolation.
"""
import pytest

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot, EmpiricalUniverse, EmpiricalQuerySpec,
    make_empirical_predicate,
)
from rawlsing_next.pre553_s04_country_refinement import (
    CountryRefinementError, CountryRequest, _country_scope,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth, _build_source, _coordinate_leaf, _query, _query_authority,
    _ref,
)


def _fixture(*, predicate_style="EQ", grant_mapping=True, candidate_only=False):
    source = _build_source("country-multinational-source", [
        {"id": "U1", "responses": {"Y": "1", "X1": "1"},
         "coords": {"COUNTRY": "840"}},
        {"id": "U2", "responses": {"Y": "0", "X1": "1"},
         "coords": {"COUNTRY": "840"}},
        {"id": "D1", "responses": {"Y": "0", "X1": "0"},
         "coords": {"COUNTRY": "276"}},
    ])
    old = source["universe"]
    fields = dict(old.semantic_fields)
    fields["country_geography"] = "MULTI_COUNTRY"
    universe = EmpiricalUniverse(
        typed_state=old.typed_state,
        authority_snapshot_refs=old.authority_snapshot_refs,
        dependency_refs=old.dependency_refs,
        producer_replay_locator_or_reference_root=old.producer_replay_locator_or_reference_root,
        **fields,
    )
    authority = source["coord_auth"]
    auth_fields = dict(authority.semantic_fields)
    scope = {
        "source_universe_refs": [universe.ref.as_dict()],
        "country_scope_kind": "MULTICOUNTRY_SOURCE_COORDINATE",
        "country_coordinate_semantic_ref": source["crefs"]["COUNTRY"].as_dict(),
        "source_universe_country_geography": "MULTI_COUNTRY",
    }
    if grant_mapping:
        scope["country_values_by_canonical_code"] = {"US": "840", "DE": "276"}
    if candidate_only:
        scope["candidate_only_not_positive_authority"] = True
    auth_fields["scope_envelope"] = scope
    country_auth = AuthoritySnapshot(
        typed_state=authority.typed_state,
        authority_snapshot_refs=authority.authority_snapshot_refs,
        dependency_refs=authority.dependency_refs,
        producer_replay_locator_or_reference_root=authority.producer_replay_locator_or_reference_root,
        **auth_fields,
    )
    issued_source = {**source, "universe": universe, "coord_auth": country_auth}
    qauth = _query_authority("country-multinational-query")
    leaf = _coordinate_leaf(issued_source, "COUNTRY", "840")
    if predicate_style == "OR":
        ast = {"op": "OR", "children": (
            leaf, {"op": "LEAF", "leaf_type": "DERIVED_BRANCH_COHORT"},
        )}
        # Predicate syntax is valid, but no stronger country implication.
    elif predicate_style == "IN":
        ast = {**leaf, "operator": "IN", "exact_values": ["840", "276"]}
    elif predicate_style == "NONE":
        ast = {"op": "LEAF", "leaf_type": "DERIVED_BRANCH_COHORT",
               "branch_definition_id": "EVERYONE"}
    else:
        ast = leaf
    predicate = make_empirical_predicate(
        predicate_ast=ast, typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(qauth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "multi-country-predicate"),
        grammar_authority_ref=qauth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=tuple(source["risk_refs"].values()),
        scope_refs=(universe.ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )
    query = _query(issued_source, qauth, predicate, ("Y", "X1"),
                   tag="multinational-with-exact-country-predicate")
    registry = AuthorityRegistry((
        source["source_auth"], source["routing_auth"], country_auth, qauth,
        *tuple(a for a in source["authorities"]
               if a.authority_kind not in {
                   "SOURCE_SEMANTICS_TOPOLOGY", "ROUTING_RISK_SET",
                   "COORDINATE_SEMANTICS",
               }),
    ))
    return universe, predicate, query, registry, issued_source


def test_source_issued_country_predicate_positive_with_native_value_mapping():
    u, p, q, registry, issued_source = _fixture()
    req = CountryRequest(country="US", source_family="SURVEY", wave="W1",
                         country_coordinate_ref=issued_source["crefs"]["COUNTRY"],
                         country_coordinate_authority_ref=issued_source["coord_auth"].authority_ref,
                         source_country_value="840")
    mode, axis, val = _country_scope(
        universe=u, predicate=p, query=q, registry=registry, request=req)
    assert (mode, axis, val) == ("ISSUED_EXACT_COUNTRY_PREDICATE", None, "840")


def test_wrong_source_country_mapping_must_refuse():
    u, p, q, registry, source = _fixture()
    with pytest.raises(CountryRefinementError, match="SOURCE_COUNTRY_VALUE_MISMATCH"):
        _country_scope(
            universe=u, predicate=p, query=q, registry=registry,
            request=CountryRequest(
                country="US", source_family="SURVEY", wave="W1",
                country_coordinate_ref=source["crefs"]["COUNTRY"],
                country_coordinate_authority_ref=source["coord_auth"].authority_ref,
                source_country_value="276",
            ),
        )


def test_multinational_without_country_code_meaning_is_held():
    u, p, q, registry, source = _fixture(grant_mapping=False)
    with pytest.raises(CountryRefinementError, match="COUNTRY_CODE_TO_SOURCE_VALUE_NOT_ISSUED"):
        _country_scope(
            universe=u, predicate=p, query=q, registry=registry,
            request=CountryRequest(
                country="US", source_family="SURVEY", wave="W1",
                country_coordinate_ref=source["crefs"]["COUNTRY"],
                country_coordinate_authority_ref=source["coord_auth"].authority_ref,
            ),
        )


def test_or_or_in_country_predicate_cannot_prove_one_country():
    for kind in ("OR", "IN", "NONE"):
        u, p, q, registry, source = _fixture(predicate_style=kind)
        with pytest.raises(CountryRefinementError, match="PREDICATE_DOES_NOT_ENTAIL_COUNTRY"):
            _country_scope(
                universe=u, predicate=p, query=q, registry=registry,
                request=CountryRequest(
                    country="US", source_family="SURVEY", wave="W1",
                    country_coordinate_ref=source["crefs"]["COUNTRY"],
                    country_coordinate_authority_ref=source["coord_auth"].authority_ref,
                ),
            )


def test_multinational_country_target_axis_has_to_be_issued_target():
    u, p, q, registry, source = _fixture(predicate_style="NONE")
    coord = source["crefs"]["COUNTRY"]
    fields = dict(q.semantic_fields)
    components = [dict(c) for c in q.target_arity_and_topology["components"]]
    components[1]["target_ref"] = coord
    components[1]["domain"] = ["276", "840"]
    fields["target_refs"] = (fields["target_refs"][0], coord)
    fields["target_arity_and_topology"] = {
        **dict(q.target_arity_and_topology), "components": components,
    }
    axis_query = EmpiricalQuerySpec(
        typed_state=q.typed_state, authority_snapshot_refs=q.authority_snapshot_refs,
        dependency_refs=q.dependency_refs,
        producer_replay_locator_or_reference_root=q.producer_replay_locator_or_reference_root,
        **fields,
    )
    req = CountryRequest(
        country="US", source_family="SURVEY", wave="W1", country_axis=1,
        country_coordinate_ref=coord,
        country_coordinate_authority_ref=source["coord_auth"].authority_ref,
    )
    mode, axis, value = _country_scope(
        universe=u, predicate=p, query=axis_query, registry=registry,
        request=req,
    )
    assert (mode, axis, value) == ("ISSUED_COUNTRY_AXIS", 1, "840")
    with pytest.raises(CountryRefinementError, match="COUNTRY_AXIS_NOT_SOURCE_COORDINATE"):
        _country_scope(
            universe=u, predicate=p, query=q, registry=registry,
            request=req,
        )



def test_historical_country_mapping_candidate_cannot_self_promote_even_in_allow_snapshot():
    u, p, q, registry, source = _fixture(candidate_only=True)
    with pytest.raises(CountryRefinementError, match="CANDIDATE_NOT_POSITIVE"):
        _country_scope(
            universe=u, predicate=p, query=q, registry=registry,
            request=CountryRequest(
                country="US", source_family="SURVEY", wave="W1",
                country_coordinate_ref=source["crefs"]["COUNTRY"],
                country_coordinate_authority_ref=source["coord_auth"].authority_ref,
            ),
        )
