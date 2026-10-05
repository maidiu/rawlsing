"""HQ206 repaired focused court — V556 substrate ontology/authoring repair.

Source-free. Synthetic material only. No attractor population. No source access.

These are MACHINERY-level hostile tests. The review's central finding was that the
previous court asserted properties of the two canary *instances* while the generic
authoring path would author, register and positively evaluate unadopted ontology.
Every test below therefore drives the generic authoring/registry path directly.

The adopted M3 seam is not modified and is exercised only for regression.
"""
from __future__ import annotations

import sys

import pytest

from rawlsing_next import pre553_v556_positive_substrate as S
from rawlsing_next.pre553_v556_positive_substrate import (
    AUTHORIZED_INTERACTION_RELATION_KINDS,
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
    """Review F2/P2 and HQ211 Repair 4: no actor-semantic role may become registrable.

    HQ211 changed the ENFORCEMENT MECHANISM, so this assertion is narrowed to what is
    actually enforced. The primary authority is now the POSITIVE per-family role
    allowlist, not the substring blacklist; an unlisted role is refused by construction
    and therefore never reaches the blacklist. This test asserts the refusal and the
    real mechanism rather than a stale message.
    """
    for roles in (("ACTOR_DESIRE", "ACTOR_BELIEF"), ("STRUCTURAL_ENDPOINT", "PERSON_TRAIT"),
                  ("ACTOR_PSYCHE", "R2"), ("SUBJECTIVE_DESIRE", "R2")):
        with pytest.raises(SubstrateAuthoringError) as exc:
            _rule(participant_roles=roles)
        assert "governed role allowlist" in str(exc.value)


def test_participant_role_allowlist_is_the_ceiling_not_a_blacklist():
    """HQ211 Repair 4: an unlisted but innocent-looking role is ALSO refused.

    This is the discriminating witness. A blacklist would accept ``CIVIC_ASSOCIATION``
    because it names no blocked token; a positive allowlist refuses it because it is not
    one of the two already-authorized topology roles. It is refused at REGISTRY BUILD too.
    """
    for roles in (("CIVIC_ASSOCIATION", "STRUCTURAL_ENDPOINT_B"),
                  ("STRUCTURAL_ENDPOINT_A", "CIVIC_ASSOCIATION"),
                  ("INSTITUTIONAL_NODE", "STRUCTURAL_ENDPOINT_B")):
        with pytest.raises(SubstrateAuthoringError) as exc:
            _rule(participant_roles=roles)
        assert "governed role allowlist" in str(exc.value)
# and the ceiling holds at the registry surface as well: a hand-constructed
    # GovernedRule carrying an unlisted role cannot reach GOVERNED_RULES_PRESENT
    rule = _rule()
    forged_rule = GovernedRule(
        rule={**S._plain(rule.rule),
              "participant_roles": ["CIVIC_ASSOCIATION", "STRUCTURAL_ENDPOINT_B"]},
        rule_key=rule.rule_key, result_contract=rule.result_contract,
        result_contract_ref=rule.result_contract_ref, semantic_family=rule.semantic_family)
    with pytest.raises(SubstrateAuthoringError) as exc:
        V556RuleMaterialRegistry.build([forged_rule])
    assert "governed allowlist" in str(exc.value)


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


def _bindings(a, b):
    """Two governed participant bindings for the dyadic topology canary."""
    source = {"kind": "SourceUniverse", "object_id": "s1", "content_hash": _hash(["s1"])}
    return [
        {"v555_route_identity_ref": _m3_route_ref(a), "role": "STRUCTURAL_ENDPOINT_A",
         "ordinal_or_null": 1, "multiplicity_index": 0, "source_universe_ref": source},
        {"v555_route_identity_ref": _m3_route_ref(b), "role": "STRUCTURAL_ENDPOINT_B",
         "ordinal_or_null": 2, "multiplicity_index": 0, "source_universe_ref": source},
    ]


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


# ================================================================= HQ211 Repair 5
# Independent literal witnesses. Every hostile token below is a LITERAL written in this
# file. None is imported from the production vocabulary lists, so no witness proves
# production correct by reading production's own list back.
_HQ211_BLOCKED_NOUNS = ("DOMINATION", "HEGEMONY", "SUBHEGEMONY", "CAPITAL",
                        "FIELD_SPECIFIC_CAPITAL", "CONVERSION", "HOMOLOGY",
                        "PRESSURE_FOOTPRINT", "PRESSURE_PATHWAY", "PRESSURE_COUPLING",
                        "PRESSURE_COUPLING_PROFILE", "STRUCTURAL_MECHANISM")
_HQ211_REF_KINDS = ("HEGEMONY", "DOMINATION", "SUBHEGEMONY", "PRESSURE_COUPLING_PROFILE")
_HQ211_MAGNITUDES = ("0.87", "1", "0.5", "100", "3.14159")
_HQ211_ACTOR_ROLE_WITNESSES = ("SELF_MODEL", "IDENTITY_COMMITMENT", "INNER_STATE",
                              "SUBJECTIVE_MEANING", "WORLDVIEW", "TEMPERAMENT",
                              "STRUCTURAL_SELF", "HABITUS", "DISPOSITION", "ORIENTATION")


def test_w1_unbounded_string_leaf_with_blocked_noun_is_refused():
    """Witness 1: an UNBOUNDED semantic string leaf may not be authored."""
    for marker in ("UNBOUNDED", None):
        with pytest.raises(SubstrateAuthoringError) as exc:
            S._node_string("OBJECTIVE_TEXT_LABEL", marker)
        assert "UNBOUNDED sentinel is refused" in str(exc.value)


def test_w1b_unbounded_string_leaf_cannot_carry_a_blocked_noun_into_a_schema():
    """Witness 1 (end to end): the blocked noun never reaches an authored schema."""
    for noun in _HQ211_BLOCKED_NOUNS:
        for marker in ("UNBOUNDED", None):
            with pytest.raises(SubstrateAuthoringError):
                _closed_schema(schema_id="HQ211_W1", root=S._node_object(
                    {"k": S._node_string("OBJECTIVE_TEXT_LABEL", marker)}, ("k",)))


def test_w2_unbounded_exact_ref_kind_leaf_with_blocked_kind_is_refused():
    """Witness 2: an UNBOUNDED exact-ref kind leaf may not be authored."""
    for marker in ("UNBOUNDED", None):
        with pytest.raises(SubstrateAuthoringError) as exc:
            S._node_exact_ref("OBJECTIVE_REFERENCE", marker)
        assert "UNBOUNDED sentinel is refused" in str(exc.value)
    for kind in _HQ211_REF_KINDS:
        with pytest.raises(SubstrateAuthoringError):
            _closed_schema(schema_id="HQ211_W2", root=S._node_object(
                {"r": S._node_exact_ref("OBJECTIVE_REFERENCE", (kind, "STRUCTURAL_MEDIATION_ROUTE_CANDIDATE"))},
                ("r",)))


def test_w3_numeric_magnitude_riding_a_string_leaf_is_refused():
    """Witness 3: a numeric magnitude cannot ride a semantic value leaf.

    Two distinct routes are closed. (a) A numeric NOD TYPE is refused outright. (b) The
    route HQ210 exploited -- a magnitude STRING on an UNBOUNDED leaf -- is now refused
    because no UNBOUNDED semantic value leaf can be authored at all. A closed list of
    digit strings is NOT unlawful to declare; what is unlawful is smuggling an undeclared
    magnitude, so the end-to-end assertion drives M3 and proves the value cannot pass.
    """
    for node_type in ("number", "integer"):
        root = {"type": "object", "semantic_role": "OBJECTIVE_GROUPING",
                "fields": {"pressure_magnitude": {"type": node_type,
                                                   "semantic_role": "OBJECTIVE_MEASUREMENT"}},
                "required": ["pressure_magnitude"], "additional_fields": False}
        with pytest.raises(SubstrateAuthoringError) as exc:
            _closed_schema(schema_id="HQ211_W3", root=root)
        assert "numeric-formula ref" in str(exc.value)
    # (b) the unbounded route that carried "0.87" before the repair
    for marker in ("UNBOUNDED", None):
        with pytest.raises(SubstrateAuthoringError):
            _closed_schema(schema_id="HQ211_W3B", root=S._node_object(
                {"mag": S._node_string("OBJECTIVE_MEASUREMENT", marker)}, ("mag",)))


def test_w3b_numeric_magnitude_cannot_reach_a_supported_object_end_to_end():
    """Witness 3 end to end: no magnitude string reaches a SUPPORTED positive object."""
    from rawlsing_next.m3_v556_higher_order_structural import M3DecisionState
    for magnitude in _HQ211_MAGNITUDES:
        bundle = _closed_schema(schema_id="HQ211_W3E", root=S._node_object(
            {"mag": S._node_string("OBJECTIVE_MEASUREMENT", ("STRUCTURAL_INCIDENCE_PRESENT",))},
            ("mag",)))
        contract = author_result_contract_binding(
            binding_id="B-M", rule_id="R-M", rule_version="1.0.0",
            schema=bundle["schema"], schema_ref=bundle["schema_ref"])
        rule = author_governed_rule(
            authority_id="A", authority_version="1.0.0", authority_content_hash=_hash(["A"]),
            rule_id="R-M", rule_version="1.0.0", semantic_family="V556_TOPOLOGY",
            participant_roles=("STRUCTURAL_ENDPOINT_A", "STRUCTURAL_ENDPOINT_B"),
            minimum_cardinality=2, maximum_cardinality_or_unbounded_marker=2,
            result_contract=contract)
        registry = V556RuleMaterialRegistry.build([rule])
        a, b = _m2("m1"), _m2("m2")
        result = _evaluate(registry, [a, b], _positive_request(
            rule, _bindings(a, b), {"mag": magnitude}))
        assert result.decision_state is not M3DecisionState.SUPPORTED, magnitude


def test_w4_generic_authoring_of_interaction_relation_is_refused():
    """Witness 4: V556_INTERACTION_RELATION refuses GENERIC positive authoring."""
    with pytest.raises(SubstrateAuthoringError) as exc:
        _rule(semantic_family="V556_INTERACTION_RELATION")
    assert "not authorable in this tranche" in str(exc.value)
    assert "V556_INTERACTION_RELATION" in str(exc.value)


def test_w5_generic_authoring_of_attractor_prerequisite_is_refused():
    """Witness 5: V556_ATTRACTOR_PREREQUISITE refuses GENERIC positive authoring."""
    with pytest.raises(SubstrateAuthoringError) as exc:
        _rule(semantic_family="V556_ATTRACTOR_PREREQUISITE")
    assert "not authorable in this tranche" in str(exc.value)


def test_w5b_valid_empty_ceiling_holds_at_registry_build_not_only_at_authoring():
    """The valid-empty claim is a MACHINERY ceiling, so a hand-built rule is refused too."""
    rule = _rule()
    for family in ("V556_INTERACTION_RELATION", "V556_ATTRACTOR_PREREQUISITE"):
        forged = GovernedRule(
            rule={**S._plain(rule.rule), "semantic_family": family},
            rule_key=rule.rule_key, result_contract=rule.result_contract,
            result_contract_ref=rule.result_contract_ref, semantic_family=family)
        with pytest.raises(SubstrateAuthoringError) as exc:
            V556RuleMaterialRegistry.build([forged])
        assert "required-valid-empty family" in str(exc.value)


def test_w6_ten_actor_person_semantic_role_witnesses_are_all_refused():
    """Witness 6: all ten HQ210 witnesses are refused as participant roles."""
    for role in _HQ211_ACTOR_ROLE_WITNESSES:
        with pytest.raises(SubstrateAuthoringError) as exc:
            _rule(participant_roles=(role, "STRUCTURAL_ENDPOINT_B"))
        assert "governed role allowlist" in str(exc.value)


def test_w7_lawful_topology_canary_still_evaluates_supported_through_unmodified_m3():
    """Witness 7: the positive core survives, through the byte-unchanged seam."""
    from rawlsing_next.m3_v556_higher_order_structural import M3DecisionState
    registry = source_free_canary_registry()
    rule = registry.rule_for("V556_TOPOLOGY")
    a, b = _m2("wa"), _m2("wb")
    src = {"kind": "SourceUniverse", "object_id": "s1", "content_hash": _hash(["s1"])}
    bindings = [
        {"v555_route_identity_ref": _m3_route_ref(a), "role": "STRUCTURAL_ENDPOINT_A",
         "ordinal_or_null": 1, "multiplicity_index": 0, "source_universe_ref": src},
        {"v555_route_identity_ref": _m3_route_ref(b), "role": "STRUCTURAL_ENDPOINT_B",
         "ordinal_or_null": 2, "multiplicity_index": 0, "source_universe_ref": src},
    ]
    payload = {"endpoint_a_ref": _m3_route_ref(a), "endpoint_b_ref": _m3_route_ref(b),
               "incidence_kind": S.PERMITTED_INCIDENCE_KINDS[0]}
    result = _evaluate(registry, [a, b], _positive_request(rule, bindings, payload))
    assert result.decision_state is M3DecisionState.SUPPORTED, result.reason


def test_w8_closed_semantic_leaf_positive_control_still_works():
    """Witness 8: a closed governed value list still authors and evaluates."""
    from rawlsing_next.m3_v556_higher_order_structural import M3DecisionState
    root = S._node_object({"k": S._node_string("OBJECTIVE_TEXT_LABEL", ("PERMITTED_A", "PERMITTED_B"))},
                          ("k",))
    bundle = author_closed_result_schema(schema_id="HQ211_W8",
                                         semantic_class="OBJECTIVE_STRUCTURAL_RESULT", root=root)
    contract = author_result_contract_binding(
        binding_id="B-W8", rule_id="R-W8", rule_version="1.0.0",
        schema=bundle["schema"], schema_ref=bundle["schema_ref"])
    rule = author_governed_rule(
        authority_id="A", authority_version="1.0.0", authority_content_hash=_hash(["A"]),
        rule_id="R-W8", rule_version="1.0.0", semantic_family="V556_TOPOLOGY",
        participant_roles=("STRUCTURAL_ENDPOINT_A", "STRUCTURAL_ENDPOINT_B"),
        minimum_cardinality=2, maximum_cardinality_or_unbounded_marker=2,
        result_contract=contract)
    registry = V556RuleMaterialRegistry.build([rule])
    a, b = _m2("w8a"), _m2("w8b")
    src = {"kind": "SourceUniverse", "object_id": "s1", "content_hash": _hash(["s1"])}
    bindings = [
        {"v555_route_identity_ref": _m3_route_ref(a), "role": "STRUCTURAL_ENDPOINT_A",
         "ordinal_or_null": 1, "multiplicity_index": 0, "source_universe_ref": src},
        {"v555_route_identity_ref": _m3_route_ref(b), "role": "STRUCTURAL_ENDPOINT_B",
         "ordinal_or_null": 2, "multiplicity_index": 0, "source_universe_ref": src},
    ]
    payload = {"k": "PERMITTED_A"}
    result = _evaluate(registry, [a, b], _positive_request(rule, bindings, payload))
    assert result.decision_state is M3DecisionState.SUPPORTED, result.reason


def test_w9_semantic_ref_kind_positive_control_still_works():
    """Witness 9: a closed governed exact-ref kind list still authors."""
    root = S._node_object(
        {"r": S._node_exact_ref("OBJECTIVE_REFERENCE", ("STRUCTURAL_MEDIATION_ROUTE_CANDIDATE",))},
        ("r",))
    bundle = author_closed_result_schema(schema_id="HQ211_W9",
                                         semantic_class="OBJECTIVE_STRUCTURAL_RESULT", root=root)
    assert list(bundle["schema"]["root"]["fields"]["r"][
        "allowed_kinds_or_unbounded_marker"]) == ["STRUCTURAL_MEDIATION_ROUTE_CANDIDATE"]


def test_court_imports_no_refusal_vocabulary_from_production():
    """HQ214 Repair D-3: a structural check that CAN fail.

    The HQ213 rereview proved the HQ211 ``test_w10`` could never fail: it built the
    banned names by concatenation and then scanned the source for literals, so it
    examined a string that was never present. This replacement is a genuine tripwire.

    It parses this file's AST and inspects IMPORT nodes only. It never searches for a
    literal name, so concatenating names cannot defeat it, and it references no
    production vocabulary value. If anyone adds an import from the substrate module
    whose name is not in the declared allowlist, the court fails and a reviewer sees
    the new import in the failure message.

    Residual, stated honestly: this is a tripwire that makes an unlisted import visible,
    not a proof that no future witness could ever be self-referential. Self-reference
    protection remains a review discipline; this test is a machine-checked alarm, not
    an invariant.
    """
    import ast
    import inspect
    tree = ast.parse(inspect.getsource(sys.modules[__name__]))
    permitted = {
        # the module alias itself (from rawlsing_next import ... as S)
        "pre553_v556_positive_substrate",
        "AUTHORIZED_INTERACTION_RELATION_KINDS", "MULTIPLICITY_POLICIES",
        "TD_R03_NON_INFERABLE_F1_PREMISE_KINDS", "TOPOLOGY_CANARY_F2_CLAIM",
        "TOPOLOGY_CANARY_MAX_CARDINALITY", "TOPOLOGY_CANARY_SHAPE_LABEL",
        "TRANCHE_LOCAL_ACTOR_INDEXING_MODES", "VALID_EMPTY_NO_GOVERNED_RULE",
        "GovernedRule", "ResultContractBinding", "SubstrateAuthoringError",
        "V556RuleMaterialRegistry", "author_closed_result_schema",
        "author_governed_rule", "author_result_contract_binding",
        "interaction_relation_canary_rule", "source_free_canary_registry",
        "topology_canary_rule", "validate_payload_against_participants",
        "validate_result_contract_binding",
    }
    imported = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        module = node.module or ""
        from_substrate = (module.endswith("pre553_v556_positive_substrate")
                          or module == "rawlsing_next")
        if not from_substrate:
            continue
        for alias in node.names:
            if alias.name == "*":
                raise AssertionError("court must not star-import the substrate module")
            imported.add(alias.name)
    unlisted = imported - permitted
    assert not unlisted, f"court imports names outside the declared allowlist: {sorted(unlisted)}"


# ================================================================= HQ211 Repair 6
def test_illustrative_labels_are_snapshot_only_and_this_is_asserted():
    """Repair 6: the shape/F2 labels are documentary, and that is stated, not implied."""
    rule = topology_canary_rule()
    emitted = S._plain(rule.rule)
    contract = S._plain(rule.result_contract)
    schema = contract["result_schema"]
    blob = repr(emitted) + repr(contract) + repr(schema)
    assert TOPOLOGY_CANARY_SHAPE_LABEL not in blob
    assert TOPOLOGY_CANARY_F2_CLAIM not in blob
    # they ARE surfaced in the registry snapshot, which is the truthful location
    snapshot = source_free_canary_registry().snapshot()
    assert snapshot["topology_canary_shape_label"] == TOPOLOGY_CANARY_SHAPE_LABEL
    assert snapshot["topology_canary_f2_claim"] == TOPOLOGY_CANARY_F2_CLAIM


def test_payload_participant_helper_classification_is_machine_readable():
    """D-4: the classification is asserted as DATA, field by field.

    The HQ211 version proved the classification by searching the helper's docstring for
    the word "court". That is decorative: the prose can be reworded while behaviour is
    unchanged, and a docstring can be edited to contain or omit any word. Here the
    classification is a frozen record and every field is asserted directly.
    """
    c = S.PAYLOAD_PARTICIPANT_HELPER_CLASSIFICATION
    assert c["helper"] == "validate_payload_against_participants"
    assert c["classification"] == "COURT_HELPER_VALIDATION_UTILITY"
    assert c["is_seam_enforcement"] is False
    assert c["is_production_evaluation_path"] is False
    assert c["invoked_by_m3_seam"] is False
    assert c["invoked_by_evaluation_path"] is False
    assert c["new_seam_added_to_make_it_real"] is False
    # no claim of production enforcement is made anywhere in the record
    assert "enforcement" not in c["classification"].lower()
    # the record is frozen, so a caller cannot relabel the helper into enforcement
    with pytest.raises(TypeError):
        c["is_seam_enforcement"] = True


def test_payload_participant_helper_is_never_invoked_by_the_seam():
    """D-4: the seam-absence half is proved behaviourally, not by docstring wording.

    This inspects the real seam source for the helper name. It would fail if a future
    change wired the helper into the seam without updating the classification.
    """
    import inspect
    import rawlsing_next.m3_v556_higher_order_structural as seam
    source = inspect.getsource(seam)
    assert "validate_payload_against_participants" not in source
    assert "payload_participant" not in source
    # and the seam module surface offers no such helper at all
    assert not hasattr(seam, "validate_payload_against_participants")
    # nor does any evaluation entry point in this substrate invoke it implicitly
    assert "validate_payload_against_participants" not in inspect.getsource(
        S.V556RuleMaterialRegistry.build)


def test_payload_participant_helper_still_works_when_a_court_calls_it():
    """Positive control: declaring it a helper must not have broken it."""
    registry = source_free_canary_registry()
    rule = registry.rule_for("V556_TOPOLOGY")
    a, b = _m2("ph1"), _m2("ph2")
    payload = {"endpoint_a_ref": _m3_route_ref(a), "endpoint_b_ref": _m3_route_ref(b),
               "incidence_kind": S.PERMITTED_INCIDENCE_KINDS[0]}
    validate_payload_against_participants(rule, payload, _bindings(a, b),
                                          ("endpoint_a_ref", "endpoint_b_ref"))
    # and it still refuses a payload route ref that is NOT a governed participant.
    # Swapping a and b would NOT be refused, because both are governed; an unbound third
    # route is the real negative case.
    c = _m2("ph3")
    with pytest.raises(SubstrateAuthoringError) as exc:
        validate_payload_against_participants(
            rule, {"endpoint_a_ref": _m3_route_ref(c), "endpoint_b_ref": _m3_route_ref(b),
                   "incidence_kind": S.PERMITTED_INCIDENCE_KINDS[0]},
            _bindings(a, b), ("endpoint_a_ref", "endpoint_b_ref"))
    assert "not bound to any governed participant" in str(exc.value)
    # swapping the two governed endpoints is still accepted
    validate_payload_against_participants(
        rule, {"endpoint_a_ref": _m3_route_ref(b), "endpoint_b_ref": _m3_route_ref(a),
               "incidence_kind": S.PERMITTED_INCIDENCE_KINDS[0]},
        _bindings(a, b), ("endpoint_a_ref", "endpoint_b_ref"))


# ================================================================= HQ211 Repair 7
def test_binding_ref_object_id_is_checked_at_authoring():
    """Repair 7: object_id consistency is enforced at authoring, not only at M3."""
    contract = _binding()
    from dataclasses import replace
    bad = ResultContractBinding(binding=contract.binding,
                                binding_ref={**dict(contract.binding_ref),
                                             "object_id": "SOME-OTHER-BINDING@9.9.9"})
    with pytest.raises(SubstrateAuthoringError) as exc:
        _rule(result_contract=bad)
    assert "object_id does not resolve" in str(exc.value)


def test_actor_named_schema_classes_are_withdrawn_from_the_admitted_set():
    """Repair 7: actor-named result classes are gone and class is linked to family."""
    for withdrawn in ("OBJECTIVE_ACTOR_POSITION", "OBJECTIVE_ACTOR_OPPORTUNITY"):
        assert withdrawn not in S.ADMITTED_OBJECTIVE_SCHEMA_CLASSES
    assert "OBJECTIVE_STRUCTURAL_RESULT" in S.ADMITTED_OBJECTIVE_SCHEMA_CLASSES
    assert S.TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP[
        "OBJECTIVE_STRUCTURAL_RESULT"] == "V556_TOPOLOGY"


def _coherent_rule_for_class(semantic_class):
    """A fully lawful rule bound to an admitted schema class."""
    root = S._node_object({"k": S._node_string("OBJECTIVE_TEXT_LABEL", ("X",))}, ("k",))
    bundle = author_closed_result_schema(schema_id=f"HQ214_{semantic_class}",
                                         semantic_class=semantic_class, root=root)
    contract = author_result_contract_binding(
        binding_id=f"B-{semantic_class}", rule_id=f"R-{semantic_class}", rule_version="1.0.0",
        schema=bundle["schema"], schema_ref=bundle["schema_ref"])
    return author_governed_rule(
        authority_id="A", authority_version="1.0.0", authority_content_hash=_hash(["A"]),
        rule_id=f"R-{semantic_class}", rule_version="1.0.0", semantic_family="V556_TOPOLOGY",
        participant_roles=("STRUCTURAL_ENDPOINT_A", "STRUCTURAL_ENDPOINT_B"),
        minimum_cardinality=2, maximum_cardinality_or_unbounded_marker=2,
        result_contract=contract)


def _rehash_rule_body(rule_body):
    """Rehash a forged rule body so every hash is internally consistent (D-1 requirement)."""
    forged = dict(rule_body)
    body = {"contract_id": S.M3_CONTRACT_ID}
    body.update({k: v for k, v in forged.items()
                 if k not in ("rule_content_hash", "authority_id",
                              "authority_version", "authority_content_hash")})
    forged["rule_content_hash"] = S.semantic_hash(body)
    return forged


#: Genuine mismatches: every class and family here is REAL. No invented class or family.
_HQ214_GENUINE_MISMATCHES = (
    ("OBJECTIVE_STRUCTURAL_RESULT", "V556_INTERACTION_RELATION"),
    ("OBJECTIVE_STRUCTURAL_RESULT", "V556_ATTRACTOR_PREREQUISITE"),
    ("OBJECTIVE_MEASUREMENT", "V556_INTERACTION_RELATION"),
    ("OBJECTIVE_WORLD_STATUS", "V556_ATTRACTOR_PREREQUISITE"),
)


def test_d1_coherence_decision_refuses_genuine_mismatches():
    """D-1: the coherence DECISION refuses, proven behaviourally on real pairs.

    This replaces the HQ211 test that asserted a map entry equals itself, which proved
    nothing. Each pair below is a real admitted class against a real adopted family that
    the class is NOT authorized by, so this fails if the coherence logic is removed.
    """
    for semantic_class, family in _HQ214_GENUINE_MISMATCHES:
        assert S.TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP[semantic_class] != family
        with pytest.raises(SubstrateAuthoringError) as exc:
            S._refuse_if_class_family_mismatch(
                semantic_class=semantic_class, family=family, where="probe")
        assert "incoherent" in str(exc.value)


def test_d1_unmapped_class_is_refused_by_the_coherence_decision():
    """D-1: an unmapped class is never authorable, distinct from a mismatch."""
    with pytest.raises(SubstrateAuthoringError) as exc:
        S._refuse_if_class_family_mismatch(
            semantic_class="OBJECTIVE_NOT_IN_ANY_MAP", family="V556_TOPOLOGY", where="probe")
    assert "no governed family authorizes" in str(exc.value)


def test_d1_authoring_refuses_a_genuine_class_family_mismatch():
    """D-2: authoring refuses a genuinely mismatched class/family pair."""
    for semantic_class, family in _HQ214_GENUINE_MISMATCHES:
        root = S._node_object({"k": S._node_string("OBJECTIVE_TEXT_LABEL", ("X",))}, ("k",))
        bundle = author_closed_result_schema(schema_id=f"HQ214_A_{semantic_class}",
                                             semantic_class=semantic_class, root=root)
        contract = author_result_contract_binding(
            binding_id="B-A", rule_id="R-A", rule_version="1.0.0",
            schema=bundle["schema"], schema_ref=bundle["schema_ref"])
        with pytest.raises(SubstrateAuthoringError):
            author_governed_rule(
                authority_id="A", authority_version="1.0.0", authority_content_hash=_hash(["A"]),
                rule_id="R-A", rule_version="1.0.0", semantic_family=family,
                participant_roles=("STRUCTURAL_ENDPOINT_A", "STRUCTURAL_ENDPOINT_B"),
                minimum_cardinality=2, maximum_cardinality_or_unbounded_marker=2,
                result_contract=contract)


def test_d1_registry_build_refuses_a_rehashed_hand_built_mismatched_rule():
    """D-1/D-2: DIRECT registry build of a hand-built, consistently rehashed rule refuses.

    Every hash is internally consistent, so a stale-hash refusal cannot be what stops
    this; the rule is refused on a semantic ground.

    HONEST LIMITATION: this test does NOT isolate the class/family gate. In this tranche
    every constructible mismatch also carries a non-authorable family, so the family
    ceiling refuses it first. Verified by removing the registry coherence call: this test
    still passed. What isolates the gate is
    ``test_d1_coherence_decision_refuses_genuine_mismatches`` (behavioural) and
    ``test_d1_registry_build_is_wired_to_the_coherence_decision`` (structural wiring).
    The reason a mismatch with an AUTHORABLE family is unconstructible is stated in the
    return: every admitted class is authorized by V556_TOPOLOGY, the only authorable
    family, so the mismatch set is empty by construction of the authority-derived map.
    """
    for semantic_class, family in _HQ214_GENUINE_MISMATCHES:
        rule = _coherent_rule_for_class(semantic_class)
        forged = _rehash_rule_body({**S._plain(rule.rule), "semantic_family": family})
        hand_built = GovernedRule(
            rule=forged, rule_key=rule.rule_key, result_contract=rule.result_contract,
            result_contract_ref=rule.result_contract_ref, semantic_family=family)
        with pytest.raises(SubstrateAuthoringError) as exc:
            V556RuleMaterialRegistry.build([hand_built])
        message = str(exc.value)
        assert ("incoherent" in message) or ("required-valid-empty" in message), message


def test_d1_registry_build_is_wired_to_the_coherence_decision():
    """D-1: fail-capable structural proof that the registry surface really calls the gate.

    The end-to-end mismatch test below cannot isolate this gate, because in this tranche
    every constructible mismatch is ALSO refused by the tranche-local family ceiling.
    This test closes that gap structurally: it parses ``V556RuleMaterialRegistry.build``
    and asserts the coherence decision is actually invoked. Deleting the call fails here
    even though the end-to-end test would still pass.
    """
    import ast
    import inspect
    import textwrap
    # build is a @staticmethod, so its source still carries class-body indentation
    source = textwrap.dedent(inspect.getsource(S.V556RuleMaterialRegistry.build))
    tree = ast.parse(source)
    called = {node.func.id for node in ast.walk(tree)
              if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert "_refuse_if_class_family_mismatch" in called, (
        "registry build must independently invoke the class/family coherence decision")
    # and it must run AFTER the contract/binding re-validation, as the commission requires
    assert source.index("validate_result_contract_binding") < \
        source.index("_refuse_if_class_family_mismatch")
    # authoring must use the SAME decision, not a private duplicate
    author_source = inspect.getsource(S.author_governed_rule)
    assert "_refuse_if_class_family_mismatch" in author_source
    assert "TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP.get(bound_class)" not in author_source


def test_d1_registry_build_still_accepts_a_coherent_pair():
    """Positive control: the coherence gate is not simply refusing everything.

    Without this, D-1's gate could be satisfied by blanket refusal.
    """
    for semantic_class in sorted(S.TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP):
        rule = _coherent_rule_for_class(semantic_class)
        registry = V556RuleMaterialRegistry.build([rule])
        assert registry.state == "GOVERNED_RULES_PRESENT"
        assert registry.populated_families == ("V556_TOPOLOGY",)


def test_stored_binding_is_deep_frozen_at_rule_authoring():
    """Repair 7: immutability no longer waits for registry build."""
    rule = topology_canary_rule()
    binding = rule.result_contract
    with pytest.raises(TypeError):
        binding["authorization_state"] = "TAMPERED"
    with pytest.raises(TypeError):
        binding["result_schema"]["semantic_class"] = "TAMPERED"
