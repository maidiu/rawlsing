from __future__ import annotations

from dataclasses import asdict, replace
import json
from pathlib import Path

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as a


A1_ARTIFACT_DIR = Path(
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT34_OBL056_ACCEPTANCE_AUTHORITY_WAVE_R1/"
    "A1_ADP010_INPUT_AUTHORITY_ACCEPTANCE_BINDING_R1"
)


def _good(role: str) -> a.AcceptanceReceipt:
    return a.issue_noncurrent_synthetic_test_receipt(role)


def _readdress(r: a.AcceptanceReceipt) -> a.AcceptanceReceipt:
    provisional = replace(r, receipt_id="PENDING", receipt_hash="0" * 64)
    h = a._digest("RECEIPT", a._receipt_body(provisional))
    return replace(
        r,
        receipt_id=f"urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:{h}",
        receipt_hash=h,
    )


def _validate(r: a.AcceptanceReceipt, *, role: str | None = None, currentness: str | None = None):
    return a.validate_acceptance_receipt(
        r,
        expected_role=role or r.role,
        expected_accepted_authority_ref=r.accepted_authority_ref,
        expected_owner_jurisdiction_ref=r.accepted_authority_owner_jurisdiction_ref,
        expected_source_acceptance_evidence_ref=r.source_acceptance_evidence_ref,
        expected_scope=r.scope,
        required_currentness=currentness or r.currentness_state,
    )


def _mutated_ref(ref: a.ContentAddressedRef, *, id=None, version=None, content_hash=None):
    return a.ContentAddressedRef(id or ref.id, version or ref.version, content_hash or ref.content_hash)


def _future_current_entry(role: str) -> a.AcceptanceEntry:
    seed = next(e for e in a._SYNTH_ENTRIES if e.role == role)
    provisional = replace(
        seed,
        currentness_state=a.CURRENT_ACCEPTED,
        immutable_provenance=(a._ev("future-hq-adoption", {"role": role, "adopted": True}),),
        entry_id="PENDING",
        entry_hash="0" * 64,
    )
    h = a._digest("ENTRY", a._entry_body(provisional))
    return replace(
        provisional,
        entry_id=f"urn:rawlsing:gt34:obl056:acceptance-entry:sha256:{h}",
        entry_hash=h,
    )


def _future_current_receipt(entry: a.AcceptanceEntry, registry_ref: a.ContentAddressedRef) -> a.AcceptanceReceipt:
    provisional = a.AcceptanceReceipt(
        a.RECEIPT_SCHEMA_ID,
        a.ACCEPTANCE_AUTHORITY_REF,
        registry_ref,
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
    return replace(
        provisional,
        receipt_id=f"urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:{h}",
        receipt_hash=h,
    )


def test_h01_h02_caller_selected_authority_and_currentness_cannot_self_issue():
    r = _good(a.CAUSAL_USE_PERMISSION)
    fake = a.ContentAddressedRef("CALLER_FAKE", "9.9.9", "1" * 64)
    forged = _readdress(replace(r, accepted_authority_ref=fake, currentness_state=a.CURRENT_ACCEPTED))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_h03_forged_registry_entry_identity_rehash_fails():
    r = _good(a.CAUSAL_USE_PERMISSION)
    forged = _readdress(replace(r, registry_entry_ref=a.EvidenceRef("urn:fake:entry", "2" * 64)))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)


def test_h04_h05_forged_receipt_identity_or_body_rehash_does_not_confer_membership():
    r = _good(a.POSITIVE_APPLICABILITY)
    fake = a.ContentAddressedRef("NO_SUCH_AUTHORITY", "1.0.0", "3" * 64)
    forged = _readdress(replace(r, accepted_authority_ref=fake))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(replace(r, receipt_hash="4" * 64))


def test_h06_issuer_substitution_fails_even_after_rehash():
    r = _good(a.CAUSAL_USE_PERMISSION)
    fake = _mutated_ref(r.acceptance_authority_ref, id="ATTACKER_ISSUER")
    forged = _readdress(replace(r, acceptance_authority_ref=fake))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)


def test_h07_registry_substitution_fails_even_after_rehash():
    r = _good(a.CAUSAL_USE_PERMISSION)
    fake = _mutated_ref(r.registry_ref, id="ATTACKER_REGISTRY")
    forged = _readdress(replace(r, registry_ref=fake))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)


def test_h08_absent_registry_membership_fails_closed():
    r = _good(a.POSITIVE_APPLICABILITY)
    forged = _readdress(replace(r, accepted_authority_ref=_mutated_ref(r.accepted_authority_ref, id="ABSENT")))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_h09_duplicate_ambiguous_membership_fails_closed(monkeypatch):
    r = _good(a.CAUSAL_USE_PERMISSION)
    entry = next(e for e in a._SYNTH_ENTRIES if e.role == r.role)
    monkeypatch.setattr(a, "_SYNTH_ENTRIES", a._SYNTH_ENTRIES + (entry,))
    with pytest.raises(a.AcceptanceMissingAuthority, match="no exact positive registry entry"):
        _validate(r)


@pytest.mark.parametrize(
    "field,value",
    [
        ("id", "MUTATED_ID"),
        ("version", "2.0.0"),
        ("content_hash", "5" * 64),
    ],
)
def test_h10_h11_h12_accepted_authority_identity_mutations_fail(field, value):
    r = _good(a.CAUSAL_USE_PERMISSION)
    kwargs = {field: value}
    forged = _readdress(replace(r, accepted_authority_ref=_mutated_ref(r.accepted_authority_ref, **kwargs)))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_h13_role_mutation_fails():
    r = _good(a.CAUSAL_USE_PERMISSION)
    forged = _readdress(replace(r, role=a.POSITIVE_APPLICABILITY))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_h14_consumer_mutation_fails():
    forged = _readdress(replace(_good(a.POSITIVE_APPLICABILITY), consumer="OTHER_CONSUMER@1.0.0"))
    with pytest.raises(a.AcceptanceOutOfScope):
        _validate(forged)


@pytest.mark.parametrize("scope_field", ["transition_use_scope", "family_scope", "subject_scope", "object_scope"])
def test_h15_h16_h17_h18_scope_mutations_fail(scope_field):
    r = _good(a.CAUSAL_USE_PERMISSION)
    if scope_field == "transition_use_scope":
        scope = replace(r.scope, transition_use_scope=r.scope.transition_use_scope + ":WIDEN")
    else:
        scope = replace(r.scope, **{scope_field: getattr(r.scope, scope_field) + ("ATTACKER",)})
    forged = _readdress(replace(r, scope=scope))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_h19_owner_jurisdiction_evidence_mutation_fails():
    r = _good(a.CAUSAL_USE_PERMISSION)
    ev = a.EvidenceRef(r.accepted_authority_owner_jurisdiction_ref.ref + ":mut", "6" * 64)
    forged = _readdress(replace(r, accepted_authority_owner_jurisdiction_ref=ev))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_h20_source_acceptance_evidence_mutation_fails():
    r = _good(a.CAUSAL_USE_PERMISSION)
    ev = a.EvidenceRef(r.source_acceptance_evidence_ref.ref + ":mut", "7" * 64)
    forged = _readdress(replace(r, source_acceptance_evidence_ref=ev))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_h21_negative_limit_reference_mutation_fails():
    r = _good(a.CAUSAL_USE_PERMISSION)
    lim = a.EvidenceRef("urn:attacker:limit", "8" * 64)
    forged = _readdress(replace(r, negative_limit_refs=(lim,)))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)


def test_h22_provenance_mutation_fails():
    r = _good(a.CAUSAL_USE_PERMISSION)
    prov = a.EvidenceRef("urn:attacker:prov", "9" * 64)
    forged = _readdress(replace(r, immutable_provenance=(prov,)))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)


def test_h23_currentness_mutation_fails_closed():
    r = _good(a.POSITIVE_APPLICABILITY)
    forged = _readdress(replace(r, currentness_state=a.CURRENT_ACCEPTED))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_h24_decision_state_mutation_fails_closed():
    r = _good(a.POSITIVE_APPLICABILITY)
    forged = _readdress(replace(r, decision_state="DENY"))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_h25_receipt_id_or_hash_mutation_fails_integrity():
    r = _good(a.CAUSAL_USE_PERMISSION)
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(replace(r, receipt_id="urn:attacker:receipt"))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(replace(r, receipt_hash="a" * 64))


def test_h26_cross_role_receipt_reuse_fails_individual_validation():
    r = _good(a.CAUSAL_USE_PERMISSION)
    with pytest.raises(a.AcceptanceOutOfScope):
        _validate(r, role=a.POSITIVE_APPLICABILITY)


def test_h27_same_contact_authority_rejected_by_pair_helper():
    occurrence = _good(a.CONTACT_OCCURRENCE_WITNESS)
    independence = _good(a.CONTACT_WITNESS_INDEPENDENCE)
    forged = _readdress(replace(independence, accepted_authority_ref=occurrence.accepted_authority_ref))
    with pytest.raises(a.AcceptanceOutOfScope, match="distinct accepted authorities"):
        a.validate_contact_acceptance_pair(occurrence, forged)


def test_h28_same_contact_receipt_rejected_by_pair_helper():
    occurrence = _good(a.CONTACT_OCCURRENCE_WITNESS)
    with pytest.raises(a.AcceptanceOutOfScope, match="distinct acceptance receipts"):
        a.validate_contact_acceptance_pair(occurrence, occurrence)


def test_h29_role_relabel_and_rehash_still_lacks_registry_membership():
    r = _good(a.CAUSAL_USE_PERMISSION)
    forged = _readdress(replace(r, role=a.CONTACT_OCCURRENCE_WITNESS))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_h30_h31_synthetic_issuer_registry_cannot_be_reused_as_current():
    r = _good(a.CAUSAL_USE_PERMISSION)
    forged = _readdress(replace(r, currentness_state=a.CURRENT_ACCEPTED))
    assert forged.acceptance_authority_ref == a._SYNTH_AUTHORITY_REF
    assert forged.registry_ref == a._SYNTH_REGISTRY_REF
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_h32_synthetic_currentness_flip_and_rehash_fails():
    r = _good(a.POSITIVE_APPLICABILITY)
    forged = _readdress(replace(r, currentness_state=a.CURRENT_ACCEPTED))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_h33_synthetic_authority_copied_into_current_shaped_receipt_fails():
    r = _good(a.CAUSAL_USE_PERMISSION)
    forged = _readdress(
        replace(
            r,
            acceptance_authority_ref=a.ACCEPTANCE_AUTHORITY_REF,
            registry_ref=a.REGISTRY_REF,
            currentness_state=a.CURRENT_ACCEPTED,
        )
    )
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_h34_no_current_entry_and_no_receipt_fail_closed_without_fallback():
    artifact = a.candidate_registry_artifact()
    assert artifact["current_positive_entries"] == []
    assert artifact["positive_fallback"] is False
    r = _good(a.CAUSAL_USE_PERMISSION)
    with pytest.raises(a.AcceptanceMissingAuthority):
        a.validate_acceptance_receipt(
            None,
            expected_role=r.role,
            expected_accepted_authority_ref=r.accepted_authority_ref,
            expected_owner_jurisdiction_ref=r.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=r.source_acceptance_evidence_ref,
            expected_scope=r.scope,
            required_currentness=a.CURRENT_ACCEPTED,
        )


def test_h35_h42_future_current_registry_entry_is_permanently_rejected_even_if_installed(monkeypatch):
    entry = _future_current_entry(a.CAUSAL_USE_PERMISSION)
    future_registry_material = {
        "registry_id": a.REGISTRY_ID,
        "registry_version": a.REGISTRY_VERSION,
        "acceptance_authority_ref": asdict(a.ACCEPTANCE_AUTHORITY_REF),
        "receipt_schema_id": a.RECEIPT_SCHEMA_ID,
        "consumer": a.CONSUMER,
        "supported_roles": a.SUPPORTED_ROLES,
        "currentness_state": a.CURRENT_ACCEPTED,
        "current_positive_entries": [entry.entry_hash],
    }
    future_registry_ref = a.ContentAddressedRef(
        a.REGISTRY_ID,
        a.REGISTRY_VERSION,
        a._digest("REGISTRY", future_registry_material),
    )
    monkeypatch.setattr(a, "_CURRENT_ENTRIES", (entry,))
    monkeypatch.setattr(a, "REGISTRY_REF", future_registry_ref)
    receipt = _future_current_receipt(entry, future_registry_ref)
    assert a._CURRENT_ENTRIES == (entry,)
    assert receipt.registry_ref == future_registry_ref
    with pytest.raises(
        a.AcceptanceMissingAuthority,
        match="candidate registry not adopted/current; current positive set empty",
    ):
        _validate(receipt, currentness=a.CURRENT_ACCEPTED)


def test_h36_h41_contact_pair_helper_accepts_forged_unvalidated_constituents():
    occurrence = _good(a.CONTACT_OCCURRENCE_WITNESS)
    independence = _good(a.CONTACT_WITNESS_INDEPENDENCE)
    forged_occurrence = replace(
        occurrence,
        acceptance_authority_ref=a.ContentAddressedRef("ATTACKER_ISSUER_O", "9.9.9", "b" * 64),
        registry_ref=a.ContentAddressedRef("ATTACKER_REGISTRY_O", "9.9.9", "c" * 64),
        registry_entry_ref=a.EvidenceRef("urn:attacker:o", "d" * 64),
        receipt_id="urn:attacker:receipt:o",
        receipt_hash="e" * 64,
    )
    forged_independence = replace(
        independence,
        acceptance_authority_ref=a.ContentAddressedRef("ATTACKER_ISSUER_I", "9.9.9", "f" * 64),
        registry_ref=a.ContentAddressedRef("ATTACKER_REGISTRY_I", "9.9.9", "0" * 64),
        registry_entry_ref=a.EvidenceRef("urn:attacker:i", "1" * 64),
        receipt_id="urn:attacker:receipt:i",
        receipt_hash="2" * 64,
    )
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged_occurrence)
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged_independence)
    assert a.validate_contact_acceptance_pair(forged_occurrence, forged_independence) == (
        forged_occurrence,
        forged_independence,
    )


def test_h37_authority_and_registry_content_addresses_recompute_exactly():
    assert a._digest("AUTHORITY", a._AUTHORITY_MATERIAL) == "41b79e7f622f3c9eb0d6df649254c812fcb769db45cf6e47a808a95eebe2a50f"
    assert a._digest("REGISTRY", a._REGISTRY_MATERIAL) == "9ef38509ad5798c038bbcfa1b3a6e343df5a7c4f2a1ed4fd2af33f31f19e3a9e"
    r = _good(a.CAUSAL_USE_PERMISSION)
    assert a._digest("RECEIPT", a._receipt_body(r)) == r.receipt_hash
    entry = next(e for e in a._SYNTH_ENTRIES if e.role == r.role)
    assert a._digest("ENTRY", a._entry_body(entry)) == entry.entry_hash


def test_h38_canonical_ordering_nfc_and_replay_are_deterministic():
    assert a._digest("X", {"b": 2, "a": 1}) == a._digest("X", {"a": 1, "b": 2})
    assert a._digest("X", {"s": "e\u0301"}) == a._digest("X", {"s": "é"})
    for role in a.SUPPORTED_ROLES:
        assert _good(role) == _good(role)


def test_h39_candidate_artifacts_match_frozen_module_constants():
    registry = json.loads((A1_ARTIFACT_DIR / "01_CANDIDATE_AUTHORITY_REGISTRY.json").read_text(encoding="utf-8"))
    schema = json.loads((A1_ARTIFACT_DIR / "02_RECEIPT_SCHEMA_AND_SYNTHETIC_EXAMPLE.json").read_text(encoding="utf-8"))
    assert registry["acceptance_authority_ref"] == asdict(a.ACCEPTANCE_AUTHORITY_REF)
    assert registry["registry_ref"] == asdict(a.REGISTRY_REF)
    assert registry["consumer"] == a.CONSUMER
    assert registry["supported_roles"] == list(a.SUPPORTED_ROLES)
    assert schema["schema"]["schema_id"] == a.RECEIPT_SCHEMA_ID


def test_h40_authority_ceiling_has_no_underlying_semantic_or_downstream_grants():
    artifact = a.candidate_registry_artifact()
    assert artifact["generic_project_wide_authority"] is False
    assert artifact["positive_fallback"] is False
    assert {
        "NO_CAUSAL_USE_SEMANTIC_TRUTH",
        "NO_APPLICABILITY_SEMANTIC_TRUTH",
        "NO_CONTACT_OCCURRENCE",
        "NO_CONTACT_INDEPENDENCE_FACT",
        "NO_ENCOUNTER",
        "NO_EXPOSURE",
        "NO_EXTERNAL_EVENT_ADMISSION",
        "NO_COMPARATOR",
        "NO_PSEPF",
        "NO_METABOLISM",
        "NO_CAN_008",
        "NO_V2",
        "NO_POSITIVE_V3_ACTOR_MUTATION",
        "NO_GENERIC_PROJECT_WIDE_AUTHORITY_ADMISSION",
    } <= set(artifact["authority_ceiling"])
