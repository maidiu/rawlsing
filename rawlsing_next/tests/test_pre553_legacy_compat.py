import hashlib
from dataclasses import replace

import pytest

from rawlsing_next.pre553_legacy_compat import (
    P04_ACCEPTED_RETURN_COMMIT,
    P04_COMPATIBILITY_CONTRACT_ID,
    P04_COMPATIBILITY_CONTRACT_VERSION,
    R1_AUTHORITY_ID,
    R1_AUTHORITY_MANIFEST_SHA256,
    R1_AUTHORITY_VERSION,
    R1_RESPONDENT_LINKAGE_MODE,
    R1_SOURCE_FILE_SHA256,
    R1_STUDY_KEY,
    V550_V551_AUTHORITY_ID,
    V550_V551_AUTHORITY_SHA256,
    V550_V551_AUTHORITY_VERSION,
    LegacyFamily,
    LegacyParityError,
    LegacyParityReceipt,
    ParityClass,
    adapt_semantic_projection,
    classify_legacy_parity,
    deferred_mappings,
    semantic_projection_hash,
    supported_mappings,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _receipt(family=LegacyFamily.V550, mapping="V550_RESPONSE_SEMANTICS_EXACT"):
    projection = {"meaning": "exact", "state": "ok", "value": 0}
    p = semantic_projection_hash(projection)
    common = dict(
        receipt_id="R14-TEST-1",
        p04_return_commit=P04_ACCEPTED_RETURN_COMMIT,
        p04_contract_id=P04_COMPATIBILITY_CONTRACT_ID,
        p04_contract_version=P04_COMPATIBILITY_CONTRACT_VERSION,
        legacy_family=family,
        mapping_id=mapping,
        source_carrier_id="carrier-1",
        source_carrier_content_hash=_h("carrier"),
        authority_id=V550_V551_AUTHORITY_ID,
        authority_version=V550_V551_AUTHORITY_VERSION,
        authority_content_hash=V550_V551_AUTHORITY_SHA256,
        source_semantic_projection_hash=p,
        target_semantic_projection_hash=p,
        source_scope_hash=_h("scope"),
        target_scope_hash=_h("scope"),
        source_state_model_hash=_h("states"),
        target_state_model_hash=_h("states"),
        source_provenance_hash=_h("prov"),
        target_provenance_hash=_h("prov"),
        source_universe_hash=_h("universe"),
        target_universe_hash=_h("universe"),
        generated_content_proved=True,
        negative_semantics_preserved=True,
    )
    return projection, LegacyParityReceipt(**common)


def test_supported_registry_is_narrow_and_named():
    assert {r.mapping_id for r in supported_mappings()} == {
        "V550_RESPONSE_SEMANTICS_EXACT",
        "V551_METRIC_SOURCE_STATE_EXACT",
        "R1_ATP_W135_SHARED_RESPONDENT_RELATION_EXACT",
    }
    assert {r.legacy_family for r in deferred_mappings()} == {
        LegacyFamily.V550J, LegacyFamily.V551J, LegacyFamily.V552, LegacyFamily.V552J,
    }


def test_v550_exact_parity_admits_valid_zero_without_falsey_collapse():
    projection, receipt = _receipt()
    decision = classify_legacy_parity(receipt)
    assert decision.parity_class is ParityClass.EXACT_PARITY
    assert decision.decision_code == "ADMIT_EXACT_PARITY"
    adapted = adapt_semantic_projection(projection, receipt)
    assert adapted.semantic_projection["value"] == 0


def test_v551_exact_parity_uses_same_pinned_bound_authority():
    _, receipt = _receipt(LegacyFamily.V551, "V551_METRIC_SOURCE_STATE_EXACT")
    decision = classify_legacy_parity(receipt)
    assert decision.parity_class is ParityClass.EXACT_PARITY


@pytest.mark.parametrize(
    "family,mapping",
    [
        (LegacyFamily.V550J, "V550J_OBJECT_PARITY"),
        (LegacyFamily.V551J, "V551J_OBJECT_PARITY"),
        (LegacyFamily.V552, "V552_OBJECT_PARITY"),
        (LegacyFamily.V552J, "V552J_OBJECT_PARITY"),
    ],
)
def test_unproved_j_and_v552_family_equivalence_is_deferred(family, mapping):
    _, base = _receipt()
    receipt = replace(base, legacy_family=family, mapping_id=mapping)
    decision = classify_legacy_parity(receipt)
    assert decision.parity_class is ParityClass.DEFERRED
    assert decision.decision_code == "DEFER_NO_ACCEPTED_NAMED_PARITY_AUTHORITY"


def test_same_shape_or_family_name_cannot_select_a_mapping():
    _, receipt = _receipt()
    decision = classify_legacy_parity(replace(receipt, mapping_id="V550_LOOKALIKE"))
    assert decision.parity_class is ParityClass.DENIED
    assert decision.decision_code == "REJECT_AMBIGUOUS_CARRIER_IDENTITY"


def test_wrong_named_authority_denied_even_when_every_hash_dimension_matches():
    _, receipt = _receipt()
    decision = classify_legacy_parity(replace(receipt, authority_content_hash=_h("lookalike")))
    assert decision.parity_class is ParityClass.DENIED
    assert decision.decision_code == "REJECT_PROVENANCE_MISMATCH"


def test_wrong_p04_binding_denied():
    _, receipt = _receipt()
    decision = classify_legacy_parity(replace(receipt, p04_return_commit="0" * 40))
    assert decision.parity_class is ParityClass.DENIED
    assert decision.decision_code == "REJECT_PROVENANCE_MISMATCH"


def test_negative_semantics_collapse_is_nonparity():
    _, receipt = _receipt()
    decision = classify_legacy_parity(replace(receipt, negative_semantics_preserved=False))
    assert decision.parity_class is ParityClass.NONPARITY
    assert decision.decision_code == "REJECT_NEGATIVE_SEMANTICS_COLLAPSE"


def test_scope_change_is_nonparity_not_coercion():
    _, receipt = _receipt()
    decision = classify_legacy_parity(replace(receipt, target_scope_hash=_h("all-not-filtered")))
    assert decision.parity_class is ParityClass.NONPARITY
    assert decision.decision_code == "REJECT_SCOPE_DOWNCAST"


def test_semantic_projection_mismatch_is_nonparity_despite_value_resemblance():
    _, receipt = _receipt()
    decision = classify_legacy_parity(replace(receipt, target_semantic_projection_hash=_h("same-looking-values")))
    assert decision.parity_class is ParityClass.NONPARITY
    assert decision.decision_code == "REJECT_UNPROVEN_PARITY"


def test_retired_runtime_and_v558_fallbacks_are_denied():
    _, receipt = _receipt()
    old = classify_legacy_parity(replace(receipt, uses_retired_runtime=True))
    assert (old.parity_class, old.decision_code) == (
        ParityClass.DENIED, "REJECT_RETIRED_RUNTIME_FALLBACK"
    )
    v558 = classify_legacy_parity(replace(receipt, uses_v558_current_runtime_context=True))
    assert (v558.parity_class, v558.decision_code) == (
        ParityClass.DENIED, "REJECT_V558_CURRENT_RUNTIME_FALLBACK"
    )


def test_profile_persona_shortcut_is_forbidden():
    _, receipt = _receipt()
    decision = classify_legacy_parity(replace(receipt, profile_or_persona_shortcut=True))
    assert decision.parity_class is ParityClass.DENIED
    assert decision.decision_code == "REJECT_FORBIDDEN_PROFILE_PERSONA_SHORTCUT"


def test_carrier_substitution_requires_exact_neutrality_proof():
    _, receipt = _receipt()
    denied = classify_legacy_parity(replace(receipt, carrier_substitution=True))
    assert denied.parity_class is ParityClass.DENIED
    admitted = classify_legacy_parity(
        replace(receipt, carrier_substitution=True, carrier_neutrality_proof_hash=_h("neutrality"))
    )
    assert admitted.parity_class is ParityClass.EXACT_PARITY


def test_generated_content_cannot_be_replaced_by_default_constant():
    _, receipt = _receipt()
    decision = classify_legacy_parity(replace(receipt, generated_content_proved=False))
    assert decision.parity_class is ParityClass.DENIED
    assert decision.decision_code == "REJECT_UNPROVEN_PARITY"


def _r1_receipt():
    projection, base = _receipt()
    return projection, replace(
        base,
        legacy_family=LegacyFamily.R1,
        mapping_id="R1_ATP_W135_SHARED_RESPONDENT_RELATION_EXACT",
        authority_id=R1_AUTHORITY_ID,
        authority_version=R1_AUTHORITY_VERSION,
        authority_content_hash=R1_AUTHORITY_MANIFEST_SHA256,
        study_key=R1_STUDY_KEY,
        source_file_sha256=R1_SOURCE_FILE_SHA256,
        authority_manifest_sha256=R1_AUTHORITY_MANIFEST_SHA256,
        respondent_linkage_mode=R1_RESPONDENT_LINKAGE_MODE,
        source_level_exclusions_preserved=True,
    )


def test_exact_r1_finite_universe_authority_admits():
    _, receipt = _r1_receipt()
    decision = classify_legacy_parity(receipt)
    assert decision.parity_class is ParityClass.EXACT_PARITY
    assert decision.decision_code == "ADMIT_R1_EXACT_AUTHORITY"


@pytest.mark.parametrize(
    "field,value",
    [
        ("study_key", "OTHER_STUDY"),
        ("source_file_sha256", hashlib.sha256(b"other").hexdigest()),
        ("authority_manifest_sha256", hashlib.sha256(b"other-manifest").hexdigest()),
        ("respondent_linkage_mode", "ROW_ORDER"),
        ("source_level_exclusions_preserved", False),
    ],
)
def test_r1_widening_or_identity_substitution_denied(field, value):
    _, receipt = _r1_receipt()
    decision = classify_legacy_parity(replace(receipt, **{field: value}))
    assert decision.parity_class is ParityClass.DENIED
    assert decision.decision_code == "REJECT_SOURCE_UNIVERSE_MISMATCH"


def test_payload_must_match_receipted_target_projection_exactly():
    projection, receipt = _receipt()
    with pytest.raises(LegacyParityError):
        adapt_semantic_projection({**projection, "value": 1}, receipt)


def test_binary_float_is_not_allowed_in_semantic_projection_identity():
    with pytest.raises(LegacyParityError):
        semantic_projection_hash({"value": 0.0})


def test_module_has_no_legacy_runtime_imports():
    import inspect
    import rawlsing_next.pre553_legacy_compat as module

    source = inspect.getsource(module)
    assert "data.ddm_build_copy" not in source
    assert "import ddm_v550" not in source
    assert "import ddm_v551" not in source
    assert "import ddm_v552" not in source
