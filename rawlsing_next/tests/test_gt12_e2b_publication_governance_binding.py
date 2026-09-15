from __future__ import annotations

from copy import deepcopy
import inspect

import pytest

import rawlsing_next.gt12_e2b_publication_governance_binding as binding
from rawlsing_next.gt12_permission_translation_authority import ADOPTED_AUTHORITY_REF
from rawlsing_next.m1_temporal_v554_admission_dedup import semantic_hash
from rawlsing_next.m4_v557_v558_publication_repository import V557DecisionState
from rawlsing_next.pre553_repo_native_seal import load_current_gt2_query_fact
from rawlsing_next.tests import gt12_e2b_actual_object_consumer_harness as harness


def test_all_adopted_semantic_hashes_recompute_exactly():
    assert semantic_hash(binding._V554_RULE_MATERIAL) == binding.V554_RULE_HASH
    assert (
        semantic_hash(binding._PUBLICATION_AUTHORITY_MATERIAL)
        == binding.PUBLICATION_AUTHORITY_HASH
    )
    assert semantic_hash(binding._V557_BINDING_MATERIAL) == binding.V557_BINDING_HASH
    assert semantic_hash(binding._BUNDLE_MATERIAL) == binding.BUNDLE_CONTENT_HASH
    assert semantic_hash(binding._ADOPTION_MATERIAL) == binding.ADOPTION_CONTENT_HASH


def test_no_argument_current_provider_returns_exact_adopted_bundle():
    assert not inspect.signature(
        binding.load_current_gt12_e2b_publication_governance_binding
    ).parameters
    current = binding.load_current_gt12_e2b_publication_governance_binding()
    assert current.bundle_id == binding.BUNDLE_ID
    assert current.bundle_version == "1.0.0"
    assert current.bundle_content_hash == (
        "f7d4d2313bcc70faf104cff205b0eb7aaa7d88556c895c8ea123a3725105cf14"
    )
    assert current.adoption_content_hash == (
        "ff3c0db1ee346b176f240523f36048d88beb6216722988ea087040b4840cd492"
    )
    assert current.governed_use_id == binding.GOVERNED_USE_ID
    assert dict(current.v554_rule_ref) == binding._V554_RULE_REF
    assert tuple(current.publication_authority["allowed_object_families"]) == ("F1",)
    assert current.v557_authority_ref.authority_id == binding.V557_AUTHORITY_ID
    assert current.v557_authority_ref.authority_version == "1.0.0"
    assert current.v557_authority_ref.authority_hash == binding.V557_BINDING_HASH
    assert binding.V557_STATE is V557DecisionState.ALLOW_CONTEXT_ONLY
    assert binding.V557_ALLOWED_USES == ("CONTEXT",)


def test_current_provider_exposes_no_selection_override():
    forbidden = {
        "governed_use_id",
        "v554_rule_ref",
        "publication_authority",
        "v557_authority_ref",
        "path",
        "current_selector",
        "permission",
        "families",
        "conditions",
    }
    assert not (
        forbidden
        & set(
            inspect.signature(
                binding.load_current_gt12_e2b_publication_governance_binding
            ).parameters
        )
    )


@pytest.mark.parametrize(
    ("material_name", "mutate"),
    [
        ("publication", lambda m: m.__setitem__("governed_use_id", "DRIFT")),
        (
            "publication",
            lambda m: m["rule_ref"].__setitem__("id", "WRONG-RULE"),
        ),
        (
            "publication",
            lambda m: m["rule_ref"].__setitem__("version", "9.9.9"),
        ),
        (
            "publication",
            lambda m: m["rule_ref"].__setitem__("hash", "0" * 64),
        ),
        ("publication", lambda m: m.__setitem__("producer", "V555")),
        ("publication", lambda m: m.__setitem__("publisher", "V556")),
        ("publication", lambda m: m.__setitem__("decision", "DENIED")),
        ("publication", lambda m: m.__setitem__("allowed_object_families", [])),
        (
            "publication",
            lambda m: m.__setitem__("allowed_object_families", ["F1", "F2"]),
        ),
        (
            "publication",
            lambda m: m.__setitem__("allowed_object_families", ["F1", "B1"]),
        ),
        (
            "v557",
            lambda m: m["narrowed_jurisdiction"].__setitem__(
                "decision_state", "ALLOW_REVIEW_ONLY"
            ),
        ),
        (
            "v557",
            lambda m: m["narrowed_jurisdiction"].__setitem__(
                "v557_allowed_uses_exact", ["REVIEW"]
            ),
        ),
        (
            "v557",
            lambda m: m["narrowed_jurisdiction"].__setitem__(
                "v557_allowed_uses_exact", ["ACTIVE_CAUSAL"]
            ),
        ),
        (
            "v557",
            lambda m: m["narrowed_jurisdiction"].__setitem__(
                "producer_family", "V553"
            ),
        ),
        (
            "v557",
            lambda m: m["narrowed_jurisdiction"].__setitem__(
                "producer_family", "V555"
            ),
        ),
        (
            "v557",
            lambda m: m["narrowed_jurisdiction"].__setitem__(
                "producer_family", "V556"
            ),
        ),
    ],
)
def test_any_adopted_authority_drift_fails_closed(material_name, mutate):
    if material_name == "publication":
        material = deepcopy(binding._PUBLICATION_AUTHORITY_MATERIAL)
        mutate(material)
        with pytest.raises(binding.GT12E2BBindingError):
            binding._validate_materials(publication_authority_material=material)
    else:
        material = deepcopy(binding._V557_BINDING_MATERIAL)
        mutate(material)
        with pytest.raises(binding.GT12E2BBindingError):
            binding._validate_materials(v557_binding_material=material)


def test_nonempty_conditions_fail_adopted_contract():
    rule = deepcopy(binding._V554_RULE_MATERIAL)
    rule["jurisdiction"]["conditions_exact"] = [{"kind": "NOT_ADOPTED"}]
    with pytest.raises(binding.GT12E2BBindingError):
        binding._validate_materials(v554_rule_material=rule)


def test_publication_authority_hash_drift_fails_bundle():
    bundle = deepcopy(binding._BUNDLE_MATERIAL)
    bundle["publication_authority"]["authority_hash"] = "0" * 64
    with pytest.raises(binding.GT12E2BBindingError):
        binding._validate_materials(bundle_material=bundle)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("authority_id", "WRONG"),
        ("authority_version", "9.9.9"),
        ("authority_hash", "0" * 64),
    ],
)
def test_v557_authority_ref_identity_drift_fails_bundle(field, value):
    bundle = deepcopy(binding._BUNDLE_MATERIAL)
    bundle["v557_authority_ref"][field] = value
    with pytest.raises(binding.GT12E2BBindingError):
        binding._validate_materials(bundle_material=bundle)


def test_permission_translator_cannot_impersonate_v557_current_binding():
    current = binding.load_current_gt12_e2b_publication_governance_binding()
    assert current.v557_authority_ref != ADOPTED_AUTHORITY_REF
    assert current.v557_authority_ref.authority_hash == binding.V557_BINDING_HASH
    assert ADOPTED_AUTHORITY_REF.authority_hash != binding.V557_BINDING_HASH


def test_real_entry_exposes_only_current_query_and_fact():
    params = inspect.signature(harness.run_current_r1c_e2b_actual_objects).parameters
    assert tuple(params) == ("query", "fact")
    for forbidden in (
        "governed_use_id",
        "v554_rule_ref",
        "publication_authority",
        "v557_authority_ref",
        "producer_permission_ceiling",
        "relation_permission_ceiling",
        "permission_translation_authority_ref",
        "v557_allowed_uses",
        "requested_resolution_uses",
        "v557_decision_state",
        "review",
        "active_causal",
    ):
        assert forbidden not in params


def test_real_entry_projects_all_four_values_from_current_provider_without_running_chain(
    monkeypatch,
):
    current = binding.load_current_gt12_e2b_publication_governance_binding()
    captured = {}

    monkeypatch.setattr(harness, "require_current_r1c_actual_objects", lambda q, f: None)

    def capture(query, fact, **kwargs):
        captured.update(kwargs)
        return "CAPTURED_WITHOUT_E2B_EXECUTION"

    monkeypatch.setattr(harness, "_run_bounded_chain", capture)
    result = harness.run_current_r1c_e2b_actual_objects(object(), object())
    assert result == "CAPTURED_WITHOUT_E2B_EXECUTION"
    assert captured["governed_use_id"] == current.governed_use_id
    assert dict(captured["v554_rule_ref"]) == dict(current.v554_rule_ref)
    assert captured["publication_authority"] == current.publication_authority
    assert captured["v557_authority_ref"] == current.v557_authority_ref


def test_actual_repo_native_current_objects_pass_astra_exact_ref_boundary():
    query, fact = load_current_gt2_query_fact()
    harness.require_current_r1c_actual_objects(query, fact)
    assert query.content_hash == harness.CURRENT_R1C_QUERY_HASH
    assert fact.content_hash == harness.CURRENT_R1C_FACT_HASH


def test_actual_current_target_refs_and_topology_are_exact_same_ordered_refs():
    query, fact = load_current_gt2_query_fact()
    harness.require_current_r1c_actual_objects(query, fact)
    targets = tuple(
        harness.exact_ref(ref, "query.target_refs") for ref in query.target_refs
    )
    components = query.target_arity_and_topology["components"]
    component_refs = tuple(
        harness.exact_ref(item["target_ref"], "component.target_ref")
        for item in components
    )
    assert component_refs == targets
    assert tuple(ref.object_id for ref in targets) == (
        "question_impl.phase0.2fb3a62609dad4c1306d",
        "question_impl.phase0.67f036c0efb7fb98ff4a",
    )
    assert tuple(ref.kind for ref in component_refs) == tuple(ref.kind for ref in targets)
    assert tuple(ref.content_hash for ref in component_refs) == tuple(
        ref.content_hash for ref in targets
    )
