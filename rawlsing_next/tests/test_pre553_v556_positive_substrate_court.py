"""HQ206 repaired focused court — V556 substrate ontology/authoring repair.

Source-free. Synthetic material only. No attractor population. No source access.

These are MACHINERY-level hostile tests. The review's central finding was that the
previous court asserted properties of the two canary *instances* while the generic
authoring path would author, register and positively evaluate unadopted ontology.
Every test below therefore drives the generic authoring/registry path directly.

The adopted M3 seam is not modified and is exercised only for regression.
"""
from __future__ import annotations

import pytest

from rawlsing_next import pre553_v556_positive_substrate as S
from rawlsing_next.pre553_v556_positive_substrate import (
    AUTHORIZED_INTERACTION_RELATION_KINDS,
    BLOCKED_STRONG_NOUNS,
    MULTIPLICITY_POLICIES,
    TD_R03_NON_INFERABLE_F1_PREMISE_KINDS,
    TOPOLOGY_CANARY_F2_CLAIM,
    TOPOLOGY_CANARY_MAX_CARDINALITY,
    TOPOLOGY_CANARY_SHAPE_LABEL,
    TRANCHE_LOCAL_ACTOR_INDEXING_MODES,
    VALID_EMPTY_NO_GOVERNED_RULE,
    GovernedRule,
    ResultContractBinding,
    SubstrateAuthoringError,
    V556RuleMaterialRegistry,
    author_closed_result_schema,
    author_governed_rule,
    author_result_contract_binding,
    interaction_relation_canary_rule,
    source_free_canary_registry,
    topology_canary_rule,
    validate_payload_against_participants,
    validate_result_contract_binding,
)

V555_FAMILY = "STRUCTURAL_MEDIATION_ROUTE_CANDIDATE"


def _hash(value) -> str:
    from rawlsing_next.m2_v555_atomic_route import semantic_hash
    return semantic_hash(value)


def _ref(kind: str, object_id: str) -> dict[str, str]:
    return {"kind": kind, "object_id": object_id, "content_hash": _hash([kind, object_id])}


def _route_ref(object_id: str) -> dict[str, str]:
    return {"kind": V555_FAMILY, "object_id": object_id, "content_hash": _hash([object_id])}


def _closed_schema(**overrides):
    """A lawful closed OBJECTIVE_STRUCTURAL_RESULT schema."""
    schema_id = overrides.pop("schema_id", "HQ206_COURT_SCHEMA")
    semantic_class = overrides.pop("semantic_class", "OBJECTIVE_STRUCTURAL_RESULT")
    root = overrides.pop("root", S._node_object(
        {"incidence_kind": S._node_string("OBJECTIVE_STATUS",
                                          ("STRUCTURAL_INCIDENCE_PRESENT",))},
        ("incidence_kind",)))
    return author_closed_result_schema(schema_id=schema_id, semantic_class=semantic_class,
                                       root=root)


def _binding(schema_bundle=None, **overrides):
    bundle = schema_bundle if schema_bundle is not None else _closed_schema()
    kwargs = dict(binding_id="HQ206-COURT-BINDING", rule_id="HQ206-COURT-RULE",
                  rule_version="1.0.0", schema=bundle["schema"], schema_ref=bundle["schema_ref"])
    kwargs.update(overrides)
    return author_result_contract_binding(**kwargs)


def _rule(binding=None, **overrides):
    contract = binding if binding is not None else _binding()
    kwargs = dict(
        authority_id="HQ206_COURT_AUTHORITY", authority_version="1.0.0",
        authority_content_hash=_hash(["HQ206_COURT_AUTHORITY", "1.0.0"]),
        rule_id="HQ206-COURT-RULE", rule_version="1.0.0",
        semantic_family="V556_TOPOLOGY",
        participant_roles=("STRUCTURAL_ENDPOINT_A", "STRUCTURAL_ENDPOINT_B"),
        participant_order_policy="ORDERED", minimum_cardinality=2,
        maximum_cardinality_or_unbounded_marker=2,
        result_contract=contract)
    kwargs.update(overrides)
    return author_governed_rule(**kwargs)


# ============================================================ R1 authoring validation
def test_open_schema_is_refused_via_the_binding_path():
    """Review F1/P1: the binding author must validate the schema it is handed."""
    open_root = {"type": "object", "semantic_role": "OBJECTIVE_GROUPING",
                 "fields": {"incidence_kind": S._node_string("OBJECTIVE_STATUS",
                                                            ("STRUCTURAL_INCIDENCE_PRESENT",))},
                 "required": ["incidence_kind"], "additional_fields": True}
    with pytest.raises(SubstrateAuthoringError) as exc:
        _closed_schema(schema_id="HQ206_OPEN", root=open_root)
    assert "additional_fields" in str(exc.value)
    # and it cannot be smuggled past author_closed_result_schema by hand-building
    bundle = {"schema": {"schema_id": "HQ206_OPEN", "schema_version": "1.0.0",
                         "semantic_class": "OBJECTIVE_STRUCTURAL_RESULT", "root": open_root},
              "schema_ref": {"kind": "M3ResultSchema@2.0.0", "object_id": "HQ206_OPEN@1.0.0",
                             "content_hash": _hash(["wrong"])}}
    with pytest.raises(SubstrateAuthoringError):
        _binding(bundle)


def test_schema_ref_must_resolve_to_the_supplied_schema():
    """Review F1/P1: an unrelated schema_ref content_hash is refused."""
    bundle = _closed_schema(schema_id="HQ206_REFDRIFT")
    tampered = dict(bundle["schema_ref"])
    tampered["content_hash"] = _hash(["unrelated"])
    with pytest.raises(SubstrateAuthoringError) as exc:
        _binding(bundle, schema_ref=tampered)
    assert "does not resolve" in str(exc.value)


def test_person_state_role_is_refused_via_the_binding_path():
    """Review F1/P1: person-state role smuggled past author_closed_result_schema."""
    bad_root = {"type": "object", "semantic_role": "OBJECTIVE_GROUPING",
                "fields": {"inner": {"type": "string",
                                     "semantic_role": "SUBJECTIVE_BELIEF_IDEOLOGY",
                                     "allowed_values_or_unbounded_marker": "UNBOUNDED"}},
                "required": ["inner"], "additional_fields": False}
    bundle = {"schema": {"schema_id": "HQ206_PERSON", "schema_version": "1.0.0",
                         "semantic_class": "OBJECTIVE_STRUCTURAL_RESULT", "root": bad_root},
              "schema_ref": {"kind": "M3ResultSchema@2.0.0", "object_id": "HQ206_PERSON@1.0.0",
                             "content_hash": _hash(["x"])}}
    with pytest.raises(SubstrateAuthoringError) as exc:
        _binding(bundle)
    assert "person-state" in str(exc.value)


def test_author_governed_rule_revalidates_its_embedded_contract():
    """A forged binding must not survive the rule author (R1)."""
    contract = _binding()
    forged = dict(contract.binding)
    forged["result_schema"] = dict(forged["result_schema"])
    forged["result_schema"]["root"] = {"type": "object", "semantic_role": "OBJECTIVE_GROUPING",
                                       "fields": {}, "required": [],
                                       "additional_fields": True}
    with pytest.raises(SubstrateAuthoringError):
        author_governed_rule(
            authority_id="A", authority_version="1.0.0", authority_content_hash=_hash(["A", "1.0.0"]),
            rule_id="HQ206-COURT-RULE", rule_version="1.0.0", semantic_family="V556_TOPOLOGY",
            participant_roles=("R1", "R2"), result_contract=ResultContractBinding(
                binding=forged, binding_ref=contract.binding_ref))


def test_registry_build_revalidates_before_governed_rules_present():
    """Review F1: unlawful material must not reach GOVERNED_RULES_PRESENT (R1/R5)."""
    rule = _rule()
    assert V556RuleMaterialRegistry.build([rule]).state == "GOVERNED_RULES_PRESENT"
    # a hand-built rule whose embedded contract is invalid must be refused at build
    broken = GovernedRule(rule=dict(rule.rule), rule_key=rule.rule_key,
                          result_contract={"binding_id": "X", "binding_version": "1.0.0"},
                          result_contract_ref=dict(rule.result_contract_ref),
                          semantic_family="V556_TOPOLOGY")
    with pytest.raises(SubstrateAuthoringError):
        V556RuleMaterialRegistry.build([broken])


def test_registry_build_refuses_invented_semantic_family():
    """Review F5/P4: the registry is an unguarded publication surface; now guarded."""
    rule = _rule()
    invented = GovernedRule(rule=dict(rule.rule), rule_key=rule.rule_key,
                            result_contract=rule.result_contract,
                            result_contract_ref=dict(rule.result_contract_ref),
                            semantic_family="V556_INVENTED_FAMILY")
    with pytest.raises(SubstrateAuthoringError) as exc:
        V556RuleMaterialRegistry.build([invented])
    assert "non-frozen semantic_family" in str(exc.value)


def test_registry_build_detects_a_stale_rule_hash():
    rule = _rule()
    body = {k: v for k, v in dict(rule.rule).items()
            if k not in ("rule_content_hash", "authority_id", "authority_version",
                         "authority_content_hash")}
    body["multiplicity_policy"] = "ROUTE_INDEXED_OCCURRENCE_SET"
    tampered = dict(rule.rule)
    tampered.update(body)
    stale = GovernedRule(rule=tampered, rule_key=rule.rule_key,
                         result_contract=rule.result_contract,
                         result_contract_ref=dict(rule.result_contract_ref),
                         semantic_family="V556_TOPOLOGY")
    with pytest.raises(SubstrateAuthoringError) as exc:
        V556RuleMaterialRegistry.build([stale])
    assert "stale or forged" in str(exc.value)


# ================================================================ R2 ontology gating
def test_actor_semantic_participant_labels_are_refused():
    """Review F2/P2: ACTOR_DESIRE / ACTOR_BELIEF must not become registrable."""
    for roles in (("ACTOR_DESIRE", "ACTOR_BELIEF"), ("STRUCTURAL_ENDPOINT", "PERSON_TRAIT"),
                  ("ACTOR_PSYCHE", "R2"), ("SUBJECTIVE_DESIRE", "R2")):
        with pytest.raises(SubstrateAuthoringError) as exc:
            _rule(participant_roles=roles)
        assert "actor-semantic participant label" in str(exc.value)


def test_strong_noun_enum_is_refused():
    """Review F2/P19: DOMINATION/HEGEMONY/CAPITAL/PRESSURE_COUPLING must not author."""
    for nouns in (("DOMINATION", "STRUCTURAL_INCIDENCE_PRESENT"),
                  ("HEGEMONY", "STRUCTURAL_INCIDENCE_PRESENT"),
                  ("CAPITAL", "STRUCTURAL_INCIDENCE_PRESENT"),
                  ("PRESSURE_COUPLING", "STRUCTURAL_INCIDENCE_PRESENT"),
                  ("HOMOLOGY", "STRUCTURAL_INCIDENCE_PRESENT")):
        with pytest.raises(SubstrateAuthoringError) as exc:
            _closed_schema(schema_id="HQ206_NOUN", root=S._node_object(
                {"k": S._node_string("OBJECTIVE_STRUCTURAL_RELATION", nouns)}, ("k",)))
        assert "blocked strong noun" in str(exc.value)


def test_forbidden_premise_relation_kind_is_refused():
    """Review F3: TD_R03 §5 non-inferable premises may not constitute an F1."""
    for premise in TD_R03_NON_INFERABLE_F1_PREMISE_KINDS:
        with pytest.raises(SubstrateAuthoringError) as exc:
            _closed_schema(schema_id="HQ206_PREMISE", root=S._node_object(
                {"relation_kind": S._node_string("OBJECTIVE_STRUCTURAL_RELATION", (premise,))},
                ("relation_kind",)))
        assert "never the rule itself" in str(exc.value)


def test_numeric_scalar_leaf_is_refused():
    """Review F2/P9: no numeric pressure magnitude through a positive path."""
    for node in ({"type": "number", "semantic_role": "OBJECTIVE_MEASUREMENT"},
                 {"type": "integer", "semantic_role": "OBJECTIVE_MEASUREMENT"}):
        root = {"type": "object", "semantic_role": "OBJECTIVE_GROUPING",
                "fields": {"pressure_magnitude": node},
                "required": ["pressure_magnitude"], "additional_fields": False}
        with pytest.raises(SubstrateAuthoringError) as exc:
            _closed_schema(schema_id="HQ206_NUM", root=root)
        assert "numeric-formula ref" in str(exc.value)


def test_blocked_nouns_are_quoted_from_adopted_law_not_invented():
    for noun in ("DOMINATION", "HEGEMONY", "CAPITAL", "HOMOLOGY", "FIELD",
                 "PRESSURE_FOOTPRINT", "PRESSURE_PATHWAY", "CONVERSION"):
        assert noun in BLOCKED_STRONG_NOUNS


# ================================================================= R3 interaction
def test_interaction_family_is_lawfully_valid_empty():
    """Critical ceiling: no governed interaction-rule authority exists."""
    assert AUTHORIZED_INTERACTION_RELATION_KINDS == ()
    with pytest.raises(SubstrateAuthoringError) as exc:
        interaction_relation_canary_rule()
    message = str(exc.value)
    assert "VALID_EMPTY" in message and "TD_R03" in message
    registry = source_free_canary_registry()
    assert "V556_INTERACTION_RELATION" in registry.unfilled_families
    assert "V556_INTERACTION_RELATION" not in registry.populated_families


def test_no_positive_interaction_relation_is_fabricated():
    registry = source_free_canary_registry()
    assert registry.rule_for("V556_INTERACTION_RELATION") is None
    assert registry.registered_rule_count == 1


def test_attractor_family_remains_unfilled():
    """No attractor population, and the family name is spelled correctly."""
    registry = source_free_canary_registry()
    assert registry.rule_for("V556_ATTRACTOR_PREREQUISITE") is None
    assert "V556_ATTRACTOR_PREREQUISITE" in registry.unfilled_families


# ==================================================================== R4 topology
def test_topology_canary_declares_a_truthful_dyadic_maximum():
    """Review F4/P6b: a false UNBOUNDED maximum is corrected."""
    rule = topology_canary_rule()
    assert rule.rule["minimum_cardinality"] == 2
    assert rule.rule["maximum_cardinality_or_unbounded_marker"] == TOPOLOGY_CANARY_MAX_CARDINALITY
    assert rule.rule["maximum_cardinality_or_unbounded_marker"] != "UNBOUNDED"


def test_topology_canary_is_labelled_one_illustrative_shape_without_an_f2_claim():
    """Review F4/P6c: not generic topology, and no F2 grain claim."""
    assert TOPOLOGY_CANARY_SHAPE_LABEL.startswith("HQ206_ONE_ILLUSTRATIVE_AUTHORIZED")
    assert TOPOLOGY_CANARY_F2_CLAIM.startswith("NOT_AN_F2_ATTRACTOR_PREREQUISITE_TOPOLOGY")
    snapshot = source_free_canary_registry().snapshot()
    assert snapshot["tranche_local_admitted_role_narrowing"]


def test_topology_canary_no_longer_requires_a_shared_channel():
    """Review F4/P6c: the mandatory shared-channel dyad is removed."""
    schema = S._topology_schema()["schema"]["root"]
    fields = set(schema["fields"])
    assert "shared_structural_channel_ref" not in fields
    assert {"endpoint_a_ref", "endpoint_b_ref", "incidence_kind"} <= fields


def test_payload_refs_must_be_bound_to_governed_participant_routes():
    """Review R4: payload refs bind to governed participant route identities."""
    rule = topology_canary_rule()
    a, b = _route_ref("urn:rawlsing:v555:route:sha256:" + "a" * 64), \
           _route_ref("urn:rawlsing:v555:route:sha256:" + "b" * 64)
    bindings = [{"v555_route_identity_ref": a, "role": "STRUCTURAL_ENDPOINT_A",
                 "ordinal_or_null": 1, "multiplicity_index": 0},
                {"v555_route_identity_ref": b, "role": "STRUCTURAL_ENDPOINT_B",
                 "ordinal_or_null": 2, "multiplicity_index": 1}]
    payload = {"endpoint_a_ref": a, "endpoint_b_ref": b,
               "incidence_kind": "STRUCTURAL_INCIDENCE_PRESENT"}
    validate_payload_against_participants(rule, payload, bindings,
                                          ("endpoint_a_ref", "endpoint_b_ref"))
    unbound = dict(payload, endpoint_a_ref=_route_ref("urn:rawlsing:v555:route:sha256:" + "f" * 64))
    with pytest.raises(SubstrateAuthoringError) as exc:
        validate_payload_against_participants(rule, unbound, bindings,
                                              ("endpoint_a_ref", "endpoint_b_ref"))
    assert "not bound to any governed participant" in str(exc.value)


def test_payload_binding_enforces_the_rule_cardinality_floor():
    rule = topology_canary_rule()
    a = _route_ref("urn:rawlsing:v555:route:sha256:" + "a" * 64)
    with pytest.raises(SubstrateAuthoringError) as exc:
        validate_payload_against_participants(rule, {"endpoint_a_ref": a}, [], ("endpoint_a_ref",))
    assert "below the rule minimum" in str(exc.value)


# ================================================================= R5 registry/tranche
def test_duplicate_semantic_family_branch_uses_distinct_rule_keys():
    """Review F7: the previous court registered two IDENTICAL rules, tripping the
    duplicate-KEY branch instead of the per-family branch. These keys are distinct."""
    first = _rule()
    second_binding = _binding(
        schema_bundle=_closed_schema(schema_id="HQ206_SECOND_SCHEMA"),
        binding_id="HQ206-COURT-BINDING-DISTINCT",
        rule_id="HQ206-COURT-RULE-DISTINCT", rule_version="2.0.0")
    second = author_governed_rule(
        authority_id="HQ206_COURT_AUTHORITY", authority_version="1.0.0",
        authority_content_hash=_hash(["HQ206_COURT_AUTHORITY", "1.0.0"]),
        rule_id="HQ206-COURT-RULE-DISTINCT", rule_version="2.0.0",
        semantic_family="V556_TOPOLOGY",
        participant_roles=("STRUCTURAL_ENDPOINT_A", "STRUCTURAL_ENDPOINT_B"),
        minimum_cardinality=2, maximum_cardinality_or_unbounded_marker=2,
        result_contract=second_binding)
    assert first.rule_key != second.rule_key, "keys must be distinct to reach the family branch"
    V556RuleMaterialRegistry.build([first])          # one rule alone is fine
    with pytest.raises(SubstrateAuthoringError) as exc:
        V556RuleMaterialRegistry.build([first, second])
    assert "per semantic family" in str(exc.value)


def test_one_rule_per_family_is_recorded_as_tranche_local_data():
    """Review F7/D: the restriction is named data, not only an exception string."""
    snapshot = source_free_canary_registry().snapshot()
    assert snapshot["tranche_local_one_rule_per_family"] is True
    assert "IN THIS TRANCHE" in snapshot["tranche_local_one_rule_per_family_note"]
    assert "not a timeless ceiling" in snapshot["tranche_local_one_rule_per_family_note"]


def test_admitted_role_narrowing_is_documented_as_tranche_local():
    """Review F6: the narrowing is recorded, not silent."""
    narrowing = S.TRANCHE_LOCAL_ADMITTED_ROLE_NARROWING
    assert "OBJECTIVE_ACTOR_INDEX" in narrowing["m3_also_admits_but_this_tranche_excludes"]
    assert "no architectural ceiling is claimed" in narrowing["why"]
    assert "OBJECTIVE_ACTOR_INDEX" not in S.ADMITTED_OBJECTIVE_ROLES


def test_objective_actor_indexed_is_removed_rather_than_dead():
    """Review F6/P3: no dead accepted mode."""
    assert TRANCHE_LOCAL_ACTOR_INDEXING_MODES == ("NO_ACTOR_INDEX",)
    with pytest.raises(SubstrateAuthoringError) as exc:
        _binding(actor_indexing_mode="OBJECTIVE_ACTOR_INDEXED")
    assert "withdrawn" in str(exc.value)
    assert "OBJECTIVE_ACTOR_INDEXED" in S.ACTOR_INDEXED_MODE_WITHDRAWN_REASON


# ========================================================================= R7 robustness
def test_multiplicity_policy_is_frozen_to_a_named_vocabulary():
    """Review F10/P11."""
    _rule(multiplicity_policy="EXACT_OCCURRENCE_INDEX")
    _rule(multiplicity_policy="ROUTE_INDEXED_OCCURRENCE_SET")
    with pytest.raises(SubstrateAuthoringError) as exc:
        _rule(multiplicity_policy="WHATEVER_I_LIKE")
    assert "frozen named vocabulary" in str(exc.value)
    assert set(MULTIPLICITY_POLICIES) == {"EXACT_OCCURRENCE_INDEX", "ROUTE_INDEXED_OCCURRENCE_SET"}


def test_authored_material_is_deep_frozen():
    """Review F9/P16c: a post-authoring mutation must be impossible, not just detected."""
    rule = topology_canary_rule()
    with pytest.raises(TypeError):
        rule.rule["multiplicity_policy"] = "TAMPERED"
    with pytest.raises(TypeError):
        rule.result_contract["result_schema"]["root"] = {}


def test_valid_empty_registry_emits_no_positive_object_and_infers_nothing():
    """Review F8: VALID_EMPTY is lawful at the substrate."""
    registry = V556RuleMaterialRegistry.build([])
    assert registry.state == VALID_EMPTY_NO_GOVERNED_RULE
    assert registry.registered_rule_count == 0
    assert registry.active_rule_keys() == []
    snapshot = registry.snapshot()
    assert sorted(snapshot["unfilled_families"]) == sorted(S.SUPPORTED_FAMILIES)
    assert snapshot["populated_families"] == []


def test_registry_distinguishes_valid_empty_from_integrity_failure():
    """TD_R03 §12: empty-because-no-rule is distinct from build/schema/hash failure."""
    empty = V556RuleMaterialRegistry.build([])
    assert empty.state == VALID_EMPTY_NO_GOVERNED_RULE
    with pytest.raises(SubstrateAuthoringError):
        V556RuleMaterialRegistry.build([object()])


def test_tampered_binding_fails_validation_rather_than_being_registered():
    contract = _binding()
    validate_result_contract_binding(contract.binding)
    tampered = dict(contract.binding)
    tampered["binding_content_hash"] = _hash(["forged"])
    with pytest.raises(SubstrateAuthoringError):
        validate_result_contract_binding(tampered)


def test_unbound_rule_identity_and_foreign_contract_are_refused():
    with pytest.raises(SubstrateAuthoringError) as exc:
        _rule(rule_id="HQ206-DIFFERENT-RULE")
    assert "bound to a different rule" in str(exc.value)


def test_invented_family_is_refused_by_the_rule_author_too():
    with pytest.raises(SubstrateAuthoringError) as exc:
        _rule(semantic_family="V556_INVENTED_FAMILY")
    assert "not an adopted V556 family" in str(exc.value)


def test_registry_snapshot_carries_the_repair_identity_and_tranche_ceilings():
    snapshot = source_free_canary_registry().snapshot()
    assert snapshot["repair_id"] == S.REPAIR_ID
    assert snapshot["authorized_interaction_relation_kinds"] == []
    assert snapshot["td_r03_non_inferable_f1_premise_kinds"] == list(
        TD_R03_NON_INFERABLE_F1_PREMISE_KINDS)
    assert snapshot["actor_indexing_modes"] == ["NO_ACTOR_INDEX"]

# ====================================================== positive core preserved
def _m2(seed: str):
    """One real governed V555 route candidate, built through the accepted M2 contract."""
    import hashlib
    from rawlsing_next.m2_v555_atomic_route import (
        M2_CONTRACT_ID, M2DecisionState, M2Evaluation, SEMANTIC_FAMILY, semantic_hash)
    h = lambda x: hashlib.sha256(x.encode()).hexdigest()
    ref = lambda k, o: {"kind": k, "object_id": o, "content_hash": h(o)}
    f1 = {"kind": "F1", "object_id": f"urn:rawlsing:v554:f1:sha256:{h('f1:' + seed)}",
          "content_hash": h("f1c:" + seed)}
    b1 = {"kind": "B1", "object_id": f"urn:rawlsing:v554:b1:sha256:{h('b1:' + seed)}",
          "content_hash": h("b1c:" + seed)}
    ident = (f1["object_id"],
             "V555-RR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL@1.0.0",
             "V555-RS-001-SOURCE-EXACT-CHANNEL-EXACT-RECEIVER@1.0.0",
             "V555-LCR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL",
             ref("StructuralChannel", "channel:" + seed),
             "V555-RC-001-EXACT-STRUCTURAL-POSITION-REF",
             ref("StructuralPosition", "receiver:" + seed))
    ih = semantic_hash(list(ident))
    route = {"semantic_family": SEMANTIC_FAMILY,
             "route_id": f"urn:rawlsing:v555:route:sha256:{ih}",
             "canonical_route_identity": ident, "canonical_route_identity_hash": ih,
             "exact_v554_f1_ref": f1, "exact_v554_b1_ref": b1,
             "inherited_v554_f2_refs": (), "producer_allowed_uses": ("M3_USE",),
             "actor_independent": True}
    return M2Evaluation(M2_CONTRACT_ID, M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED, "ok",
                        "ELIGIBLE", f1, b1, (), ident, ih, route, {}, None,
                        h("replay:" + seed))


def _m3_route_ref(m2):
    from rawlsing_next.m2_v555_atomic_route import SEMANTIC_FAMILY, semantic_hash
    return {"kind": SEMANTIC_FAMILY, "object_id": m2.route["route_id"],
            "content_hash": semantic_hash(m2.route)}


def _evaluate(registry, upstream, request):
    from rawlsing_next.m3_v556_higher_order_structural import evaluate_m3_v556_higher_order_structural
    return evaluate_m3_v556_higher_order_structural(
        upstream, request,
        active_rule_keys=registry.active_rule_keys(),
        active_source_composition_keys=[],
        active_result_contract_refs=registry.active_result_contract_refs())


def _positive_request(rule, bindings, payload):
    return {
        "higher_order_semantics_required": True,
        "rule_authority": dict(rule.rule),
        "participant_bindings": bindings,
        "source_composition_authority": None,
        "result_contract_binding": dict(rule.result_contract),
        "governed_result": {"state": "SUPPORTED", "semantic_payload": payload},
        "intended_use": "M3_USE",
    }


def test_repaired_topology_canary_still_evaluates_supported_through_the_unmodified_seam():
    """The positive core the review credited must survive the repair."""
    from rawlsing_next.m3_v556_higher_order_structural import M3DecisionState
    registry = source_free_canary_registry()
    rule = registry.rule_for("V556_TOPOLOGY")
    a, b = _m2("a"), _m2("b")
    source = {"kind": "SourceUniverse", "object_id": "s1", "content_hash": _hash(["s1"])}
    bindings = [
        {"v555_route_identity_ref": _m3_route_ref(a), "role": "STRUCTURAL_ENDPOINT_A",
         "ordinal_or_null": 1, "multiplicity_index": 0, "source_universe_ref": source},
        {"v555_route_identity_ref": _m3_route_ref(b), "role": "STRUCTURAL_ENDPOINT_B",
         "ordinal_or_null": 2, "multiplicity_index": 0, "source_universe_ref": source},
    ]
    payload = {"endpoint_a_ref": _m3_route_ref(a), "endpoint_b_ref": _m3_route_ref(b),
               "incidence_kind": S.PERMITTED_INCIDENCE_KINDS[0]}
    validate_payload_against_participants(rule, payload, bindings,
                                          ("endpoint_a_ref", "endpoint_b_ref"))
    result = _evaluate(registry, [a, b], _positive_request(rule, bindings, payload))
    assert result.decision_state is M3DecisionState.SUPPORTED, result.reason
    assert result.v556_object is not None


def test_repaired_topology_evaluation_replay_is_stable():
    from rawlsing_next.m3_v556_higher_order_structural import M3DecisionState
    registry = source_free_canary_registry()
    rule = registry.rule_for("V556_TOPOLOGY")
    a, b = _m2("a"), _m2("b")
    source = {"kind": "SourceUniverse", "object_id": "s1", "content_hash": _hash(["s1"])}
    bindings = [
        {"v555_route_identity_ref": _m3_route_ref(a), "role": "STRUCTURAL_ENDPOINT_A",
         "ordinal_or_null": 1, "multiplicity_index": 0, "source_universe_ref": source},
        {"v555_route_identity_ref": _m3_route_ref(b), "role": "STRUCTURAL_ENDPOINT_B",
         "ordinal_or_null": 2, "multiplicity_index": 0, "source_universe_ref": source},
    ]
    payload = {"endpoint_a_ref": _m3_route_ref(a), "endpoint_b_ref": _m3_route_ref(b),
               "incidence_kind": S.PERMITTED_INCIDENCE_KINDS[0]}
    first = _evaluate(registry, [a, b], _positive_request(rule, bindings, payload))
    second = _evaluate(registry, [b, a], _positive_request(
        rule, list(reversed(bindings)), payload))
    assert first.decision_state is M3DecisionState.SUPPORTED
    assert first.replay_key_hash == second.replay_key_hash


def test_truthful_cardinality_is_enforced_by_the_seam_not_only_by_us():
    """A third participant must be refused, matching the declared dyadic maximum."""
    from rawlsing_next.m3_v556_higher_order_structural import M3DecisionState
    registry = source_free_canary_registry()
    rule = registry.rule_for("V556_TOPOLOGY")
    a, b, c = _m2("a"), _m2("b"), _m2("c")
    source = {"kind": "SourceUniverse", "object_id": "s1", "content_hash": _hash(["s1"])}
    bindings = [
        {"v555_route_identity_ref": _m3_route_ref(a), "role": "STRUCTURAL_ENDPOINT_A",
         "ordinal_or_null": 1, "multiplicity_index": 0, "source_universe_ref": source},
        {"v555_route_identity_ref": _m3_route_ref(b), "role": "STRUCTURAL_ENDPOINT_B",
         "ordinal_or_null": 2, "multiplicity_index": 0, "source_universe_ref": source},
        {"v555_route_identity_ref": _m3_route_ref(c), "role": "STRUCTURAL_ENDPOINT_B",
         "ordinal_or_null": 3, "multiplicity_index": 0, "source_universe_ref": source},
    ]
    payload = {"endpoint_a_ref": _m3_route_ref(a), "endpoint_b_ref": _m3_route_ref(b),
               "incidence_kind": S.PERMITTED_INCIDENCE_KINDS[0]}
    result = _evaluate(registry, [a, b, c], _positive_request(rule, bindings, payload))
    assert result.decision_state is not M3DecisionState.SUPPORTED
    with pytest.raises(SubstrateAuthoringError) as exc:
        validate_payload_against_participants(rule, payload, bindings,
                                              ("endpoint_a_ref", "endpoint_b_ref"))
    assert "exceeds the rule maximum" in str(exc.value)
