from __future__ import annotations

from dataclasses import asdict, fields, replace
from hashlib import sha256
import inspect
import json
from pathlib import Path
import subprocess
import unicodedata

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as a


def _good(role: str = a.CAUSAL_USE_PERMISSION):
    return a.issue_noncurrent_synthetic_test_receipt(role)


def _readdress(receipt):
    provisional = replace(receipt, receipt_id="PENDING", receipt_hash="0" * 64)
    h = a._digest("RECEIPT", a._receipt_body(provisional))
    return replace(receipt, receipt_id=f"urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:{h}", receipt_hash=h)


def _validate(receipt, *, role=None, currentness=None, scope=None):
    return a.validate_acceptance_receipt(
        receipt,
        expected_role=role or receipt.role,
        expected_accepted_authority_ref=receipt.accepted_authority_ref,
        expected_owner_jurisdiction_ref=receipt.accepted_authority_owner_jurisdiction_ref,
        expected_source_acceptance_evidence_ref=receipt.source_acceptance_evidence_ref,
        expected_scope=scope or receipt.scope,
        required_currentness=currentness or receipt.currentness_state,
    )


def _ind_norm(v):
    if isinstance(v, str):
        return unicodedata.normalize("NFC", v)
    if isinstance(v, dict):
        return {unicodedata.normalize("NFC", str(k)): _ind_norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_ind_norm(x) for x in v]
    return v


def _ind_digest(label, value):
    domain = "RAWLSING\0GT34\0OBL056\0ADP010_INPUT_AUTHORITY_ACCEPTANCE_V1\0"
    body = json.dumps(_ind_norm(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256((domain + label + "\0" + body).encode()).hexdigest()


def _future_current_entry(role=a.CAUSAL_USE_PERMISSION):
    base = a._make_entry(role)
    accepted = a.ContentAddressedRef("FUTURE_HQ_ADOPTED_AUTHORITY", "1.0.0", "a" * 64)
    owner = a.EvidenceRef("urn:future:owner", "b" * 64)
    source = a.EvidenceRef("urn:future:adoption", "c" * 64)
    prov = (a.EvidenceRef("urn:future:provenance", "d" * 64),)
    provisional = replace(
        base,
        accepted_authority_ref=accepted,
        accepted_authority_owner_jurisdiction_ref=owner,
        source_acceptance_evidence_ref=source,
        currentness_state=a.CURRENT_ACCEPTED,
        immutable_provenance=prov,
        entry_id="PENDING",
        entry_hash="0" * 64,
    )
    h = a._digest("ENTRY", a._entry_body(provisional))
    return replace(provisional, entry_id=f"urn:rawlsing:gt34:obl056:acceptance-entry:sha256:{h}", entry_hash=h)


def _receipt_for_entry(entry):
    provisional = a.AcceptanceReceipt(
        a.RECEIPT_SCHEMA_ID,
        a.ACCEPTANCE_AUTHORITY_REF,
        a.REGISTRY_REF,
        a.EvidenceRef(entry.entry_id, entry.entry_hash),
        entry.role,
        entry.accepted_authority_ref,
        entry.accepted_authority_owner_jurisdiction_ref,
        entry.source_acceptance_evidence_ref,
        entry.decision_state,
        entry.consumer,
        entry.scope,
        entry.negative_limit_refs,
        entry.currentness_state,
        entry.immutable_provenance,
        "PENDING",
        "0" * 64,
    )
    h = a._digest("RECEIPT", a._receipt_body(provisional))
    return replace(provisional, receipt_id=f"urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:{h}", receipt_hash=h)


@pytest.mark.parametrize("role", a.SUPPORTED_ROLES)
def test_01_lawful_noncurrent_synthetic_fixture_validates_exactly(role):
    r = _good(role)
    assert _validate(r) == r
    assert r.currentness_state == a.NONCURRENT_SYNTHETIC_TEST_ONLY


def test_02_caller_selected_authority_cannot_self_issue_by_rehash():
    r = _good()
    forged_ref = a.ContentAddressedRef("CALLER_SELECTED", "9.9.9", "1" * 64)
    forged = _readdress(replace(r, accepted_authority_ref=forged_ref))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


@pytest.mark.parametrize("field,value", [("id", "MUTATED"), ("version", "2.0.0"), ("content_hash", "2" * 64)])
def test_03_accepted_authority_identity_mutations_fail(field, value):
    r = _good(a.POSITIVE_APPLICABILITY)
    d = asdict(r.accepted_authority_ref)
    d[field] = value
    forged = _readdress(replace(r, accepted_authority_ref=a.ContentAddressedRef(**d)))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_04_forged_registry_entry_ref_rehash_still_fails():
    r = _good()
    forged = _readdress(replace(r, registry_entry_ref=a.EvidenceRef("urn:forged:entry", "3" * 64)))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)


@pytest.mark.parametrize("which", ["authority", "registry"])
def test_05_issuer_or_registry_substitution_fails(which):
    r = _good()
    bad = a.ContentAddressedRef("CALLER_ISSUER", "1.0.0", "4" * 64)
    forged = _readdress(replace(r, **({"acceptance_authority_ref": bad} if which == "authority" else {"registry_ref": bad})))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)


def test_06_absent_receipt_fails_closed():
    r = _good()
    with pytest.raises(a.AcceptanceMissingAuthority):
        a.validate_acceptance_receipt(
            None,
            expected_role=r.role,
            expected_accepted_authority_ref=r.accepted_authority_ref,
            expected_owner_jurisdiction_ref=r.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=r.source_acceptance_evidence_ref,
            expected_scope=r.scope,
            required_currentness=r.currentness_state,
        )


def test_07_duplicate_ambiguous_registry_membership_fails_closed(monkeypatch):
    r = _good()
    e = next(x for x in a._SYNTH_ENTRIES if x.role == r.role)
    monkeypatch.setattr(a, "_SYNTH_ENTRIES", a._SYNTH_ENTRIES + (e,))
    with pytest.raises(a.AcceptanceMissingAuthority, match="no exact positive registry entry"):
        _validate(r)


def test_08_role_mutation_plus_rehash_fails():
    forged = _readdress(replace(_good(a.CAUSAL_USE_PERMISSION), role=a.POSITIVE_APPLICABILITY))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_09_consumer_mutation_fails():
    forged = _readdress(replace(_good(), consumer="OTHER_CONSUMER@1.0.0"))
    with pytest.raises(a.AcceptanceOutOfScope):
        _validate(forged)


@pytest.mark.parametrize("axis,value", [
    ("transition_use_scope", "WIDENED:USE"),
    ("family_scope", ("OTHER_FAMILY",)),
    ("subject_scope", ("OTHER_SUBJECT",)),
    ("object_scope", ("OTHER_OBJECT",)),
])
def test_10_scope_axis_mutation_fails(axis, value):
    r = _good()
    scope = replace(r.scope, **{axis: value})
    forged = _readdress(replace(r, scope=scope))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, scope=scope)


def test_11_owner_jurisdiction_mutation_fails():
    r = _good()
    ev = a.EvidenceRef("urn:mutated:owner", "5" * 64)
    forged = _readdress(replace(r, accepted_authority_owner_jurisdiction_ref=ev))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_12_source_acceptance_evidence_mutation_fails():
    r = _good()
    ev = a.EvidenceRef("urn:mutated:source", "6" * 64)
    forged = _readdress(replace(r, source_acceptance_evidence_ref=ev))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


@pytest.mark.parametrize("axis", ["negative", "provenance"])
def test_13_limits_and_provenance_mutation_fail(axis):
    r = _good()
    ev = a.EvidenceRef("urn:mutated:bound", "7" * 64)
    forged = _readdress(replace(r, **({"negative_limit_refs": (ev,)} if axis == "negative" else {"immutable_provenance": (ev,)})))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)


def test_14_decision_state_mutation_fails():
    forged = _readdress(replace(_good(), decision_state="REJECT"))
    with pytest.raises(a.AcceptanceMissingAuthority, match="nonpositive"):
        _validate(forged)


@pytest.mark.parametrize("axis", ["id", "hash"])
def test_15_receipt_identity_mutation_fails_integrity(axis):
    r = _good()
    forged = replace(r, **({"receipt_id": "urn:forged"} if axis == "id" else {"receipt_hash": "8" * 64}))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)


def test_16_cross_role_receipt_reuse_fails():
    r = _good(a.CAUSAL_USE_PERMISSION)
    with pytest.raises(a.AcceptanceOutOfScope):
        _validate(r, role=a.POSITIVE_APPLICABILITY)


def test_17_contact_same_accepted_authority_fails():
    o = _good(a.CONTACT_OCCURRENCE_WITNESS)
    i = _good(a.CONTACT_WITNESS_INDEPENDENCE)
    i2 = _readdress(replace(i, accepted_authority_ref=o.accepted_authority_ref))
    with pytest.raises(a.AcceptanceOutOfScope, match="distinct accepted authorities"):
        a.validate_contact_acceptance_pair(o, i2)


def test_18_contact_same_receipt_fails():
    o = _good(a.CONTACT_OCCURRENCE_WITNESS)
    with pytest.raises(a.AcceptanceOutOfScope, match="distinct acceptance receipts"):
        a.validate_contact_acceptance_pair(o, o)


def test_19_currentness_flip_and_rehash_cannot_upgrade_synthetic_receipt():
    forged = _readdress(replace(_good(), currentness_state=a.CURRENT_ACCEPTED))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


@pytest.mark.parametrize("axis", ["issuer", "registry", "accepted_authority"])
def test_20_synthetic_material_relabelled_current_fails(axis):
    r = replace(_good(), currentness_state=a.CURRENT_ACCEPTED)
    if axis == "issuer":
        r = replace(r, acceptance_authority_ref=a.ACCEPTANCE_AUTHORITY_REF)
    elif axis == "registry":
        r = replace(r, registry_ref=a.REGISTRY_REF)
    else:
        r = replace(r, accepted_authority_ref=a.ContentAddressedRef("CURRENT_SHAPED_COPY", "1.0.0", r.accepted_authority_ref.content_hash))
    forged = _readdress(r)
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_21_no_current_entry_no_receipt_path_fails_closed_without_fallback():
    artifact = a.candidate_registry_artifact()
    assert artifact["current_positive_entries"] == []
    assert artifact["positive_fallback"] is False
    r = _good()
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(_readdress(replace(r, currentness_state=a.CURRENT_ACCEPTED)), currentness=a.CURRENT_ACCEPTED)


def test_22_DEFECT_future_current_entry_is_unrepresentable_by_current_validator(monkeypatch):
    entry = _future_current_entry()
    receipt = _receipt_for_entry(entry)
    monkeypatch.setattr(a, "_CURRENT_ENTRIES", (entry,))
    assert a._CURRENT_ENTRIES == (entry,)
    assert a._check_integrity(receipt) is None
    src = inspect.getsource(a.validate_acceptance_receipt)
    assert "_CURRENT_ENTRIES" not in src
    with pytest.raises(a.AcceptanceMissingAuthority, match="candidate registry not adopted/current"):
        _validate(receipt, currentness=a.CURRENT_ACCEPTED)
    # A future exact current entry cannot be consumed without changing code/contract.
    assert a.candidate_registry_artifact()["current_positive_entries"] == []


def test_23_DEFECT_contact_pair_helper_accepts_unvalidated_caller_shaped_receipts():
    o = _good(a.CONTACT_OCCURRENCE_WITNESS)
    i = _good(a.CONTACT_WITNESS_INDEPENDENCE)
    forged_o = replace(
        o,
        acceptance_authority_ref=a.ContentAddressedRef("FORGED_ISSUER_O", "9", "1" * 64),
        registry_ref=a.ContentAddressedRef("FORGED_REGISTRY_O", "9", "2" * 64),
        receipt_id="FORGED_O",
        receipt_hash="3" * 64,
    )
    forged_i = replace(
        i,
        acceptance_authority_ref=a.ContentAddressedRef("FORGED_ISSUER_I", "9", "4" * 64),
        registry_ref=a.ContentAddressedRef("FORGED_REGISTRY_I", "9", "5" * 64),
        receipt_id="FORGED_I",
        receipt_hash="6" * 64,
    )
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged_o)
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged_i)
    assert a.validate_contact_acceptance_pair(forged_o, forged_i) == (forged_o, forged_i)


def test_24_authority_content_address_independently_recomputes_exactly():
    material = {
        "authority_id": a.ACCEPTANCE_AUTHORITY_ID,
        "authority_version": a.ACCEPTANCE_AUTHORITY_VERSION,
        "grain": "EXACT_ALREADY_EXISTING_AUTHORITY_ACCEPTANCE_FOR_ONE_ADP010_INPUT_ROLE_AND_SCOPE_ONLY",
        "consumer": a.CONSUMER,
        "supported_roles": a.SUPPORTED_ROLES,
        "status": a.CANDIDATE_NOT_ADOPTED,
        "authority_ceiling": a.AUTHORITY_CEILING,
    }
    assert _ind_digest("AUTHORITY", material) == a.ACCEPTANCE_AUTHORITY_CONTENT_HASH == "41b79e7f622f3c9eb0d6df649254c812fcb769db45cf6e47a808a95eebe2a50f"


def test_25_registry_content_address_independently_recomputes_exactly():
    material = {
        "registry_id": a.REGISTRY_ID,
        "registry_version": a.REGISTRY_VERSION,
        "acceptance_authority_ref": asdict(a.ACCEPTANCE_AUTHORITY_REF),
        "receipt_schema_id": a.RECEIPT_SCHEMA_ID,
        "consumer": a.CONSUMER,
        "supported_roles": a.SUPPORTED_ROLES,
        "currentness_state": a.CANDIDATE_NOT_ADOPTED,
        "current_positive_entries": [],
    }
    assert _ind_digest("REGISTRY", material) == a.REGISTRY_CONTENT_HASH == "9ef38509ad5798c038bbcfa1b3a6e343df5a7c4f2a1ed4fd2af33f31f19e3a9e"


def test_26_entry_and_receipt_content_addresses_independently_recompute():
    r = _good()
    e = next(x for x in a._SYNTH_ENTRIES if x.role == r.role)
    assert _ind_digest("ENTRY", a._entry_body(e)) == e.entry_hash
    assert _ind_digest("RECEIPT", a._receipt_body(r)) == r.receipt_hash


def test_27_canonical_key_order_and_nfc_value_normalization_are_deterministic():
    assert a._digest("CANON", {"b": "e\u0301", "a": [2, 1]}) == a._digest("CANON", {"a": [2, 1], "b": "é"})


def test_28_replay_is_idempotent_and_does_not_mutate_registry():
    before = a.candidate_registry_artifact()
    one = _good(a.POSITIVE_APPLICABILITY)
    two = _good(a.POSITIVE_APPLICABILITY)
    assert one == two
    assert _validate(one) == _validate(two)
    assert a.candidate_registry_artifact() == before


def test_29_candidate_registry_and_schema_artifacts_bind_exact_consumer_and_roles():
    artifact = a.candidate_registry_artifact()
    schema = a.receipt_schema_artifact()
    assert artifact["consumer"] == a.CONSUMER
    assert tuple(artifact["supported_roles"]) == a.SUPPORTED_ROLES
    assert schema["schema_id"] == a.RECEIPT_SCHEMA_ID
    assert schema["current_positive_requires_separate_adoption"] is True


def test_30_authority_ceiling_and_receipt_shape_emit_no_underlying_truth_or_downstream_power():
    receipt_fields = {f.name for f in fields(a.AcceptanceReceipt)}
    forbidden_fields = {"causal_use_true", "applicable", "contact_occurred", "contact_independent", "encounter", "exposure", "external_event", "comparator", "psepf", "metabolism", "can_008", "v2", "actor_mutation"}
    assert receipt_fields.isdisjoint(forbidden_fields)
    required_ceiling = {"NO_CAUSAL_USE_SEMANTIC_TRUTH", "NO_APPLICABILITY_SEMANTIC_TRUTH", "NO_CONTACT_OCCURRENCE", "NO_CONTACT_INDEPENDENCE_FACT", "NO_ENCOUNTER", "NO_EXPOSURE", "NO_EXTERNAL_EVENT_ADMISSION", "NO_COMPARATOR", "NO_PSEPF", "NO_METABOLISM", "NO_CAN_008", "NO_V2", "NO_POSITIVE_V3_ACTOR_MUTATION", "NO_GENERIC_PROJECT_WIDE_AUTHORITY_ADMISSION"}
    assert required_ceiling <= set(a.AUTHORITY_CEILING)


def test_31_frozen_candidate_module_git_blob_is_exact():
    path = "rawlsing_next/gt34_adp010_input_authority_acceptance.py"
    blob = subprocess.check_output(["git", "hash-object", path], text=True).strip()
    assert blob == "62b9cc43b0acf7cecc4647215929ef12ada955f2"


def test_32_persisted_candidate_artifacts_match_module_constants():
    base = Path("data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT34_OBL056_ACCEPTANCE_AUTHORITY_WAVE_R1/A1_ADP010_INPUT_AUTHORITY_ACCEPTANCE_BINDING_R1")
    reg = json.loads((base / "01_CANDIDATE_AUTHORITY_REGISTRY.json").read_text())
    rec = json.loads((base / "02_RECEIPT_SCHEMA_AND_SYNTHETIC_EXAMPLE.json").read_text())
    assert reg["acceptance_authority_ref"]["content_hash"] == a.ACCEPTANCE_AUTHORITY_CONTENT_HASH
    assert reg["registry_ref"]["content_hash"] == a.REGISTRY_CONTENT_HASH
    assert reg["consumer"] == a.CONSUMER
    assert reg["current_positive_entries"] == []
    assert rec["schema"]["schema_id"] == a.RECEIPT_SCHEMA_ID
    assert rec["synthetic_example_policy"]["may_masquerade_as_current"] is False


def test_33_unknown_currentness_fails_closed():
    r = _good()
    forged = _readdress(replace(r, currentness_state="CALLER_CURRENT"))
    with pytest.raises(a.AcceptanceOutOfScope):
        _validate(forged, currentness="CALLER_CURRENT")


def test_34_current_registry_contract_is_static_not_data_driven():
    assert a._CURRENT_ENTRIES == ()
    assert inspect.signature(a.candidate_registry_artifact).parameters == {}
    src = inspect.getsource(a.candidate_registry_artifact)
    assert '"current_positive_entries":[]' in src.replace(" ", "")


def test_35_composition_helper_has_no_constituent_validator_call():
    src = inspect.getsource(a.validate_contact_acceptance_pair)
    assert "validate_acceptance_receipt" not in src


def test_36_exact_supported_role_set_has_no_implicit_role_widening():
    assert a.SUPPORTED_ROLES == (
        a.CAUSAL_USE_PERMISSION,
        a.POSITIVE_APPLICABILITY,
        a.CONTACT_OCCURRENCE_WITNESS,
        a.CONTACT_WITNESS_INDEPENDENCE,
    )
