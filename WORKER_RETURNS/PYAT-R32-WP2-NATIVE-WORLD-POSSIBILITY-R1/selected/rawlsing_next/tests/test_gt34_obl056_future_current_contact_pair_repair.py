from __future__ import annotations

from dataclasses import asdict, replace
from hashlib import sha1
from pathlib import Path

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as a


ROOT = Path(__file__).resolve().parents[2]
W2 = ROOT / "rawlsing_next/v3_adp010_oee_executor_authenticated.py"
W2_BLOB = "54d9acba40f0eb1db8bb03aec3c1bb900f849588"


def _readdress_receipt(r: a.AcceptanceReceipt) -> a.AcceptanceReceipt:
    p = replace(r, receipt_id="PENDING", receipt_hash="0" * 64)
    h = a._digest("RECEIPT", a._receipt_body(p))
    return replace(r, receipt_id=f"urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:{h}", receipt_hash=h)


def _readdress_entry(e: a.AcceptanceEntry) -> a.AcceptanceEntry:
    p = replace(e, entry_id="PENDING", entry_hash="0" * 64)
    h = a._digest("ENTRY", a._entry_body(p))
    return replace(e, entry_id=f"urn:rawlsing:gt34:obl056:acceptance-entry:sha256:{h}", entry_hash=h)


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


def _future_current_entry(role: str = a.CAUSAL_USE_PERMISSION, suffix: str = "A") -> a.AcceptanceEntry:
    base = a._make_entry(role)
    source = a.EvidenceRef(f"urn:future-current-contract-test-only:selection:{suffix}", (suffix.lower() * 64)[:64])
    owner = a.EvidenceRef(f"urn:future-current-contract-test-only:owner:{suffix}", (suffix.upper() * 64)[:64])
    provenance = (a.EvidenceRef(f"urn:future-current-contract-test-only:provenance:{suffix}", ("f" + suffix.lower()) * 32),)
    accepted = a.ContentAddressedRef(f"FUTURE_CURRENT_CONTRACT_TEST_ONLY_{role}_{suffix}", "1.0.0", ("a" + suffix.lower()) * 32)
    provisional = replace(
        base,
        accepted_authority_ref=accepted,
        accepted_authority_owner_jurisdiction_ref=owner,
        source_acceptance_evidence_ref=source,
        currentness_state=a.CURRENT_ACCEPTED,
        immutable_provenance=provenance,
    )
    return _readdress_entry(provisional)


def _future_registry(*entries: a.AcceptanceEntry) -> a.AcceptanceRegistrySnapshot:
    evidence = tuple(e.source_acceptance_evidence_ref for e in entries)
    provenance = (a.EvidenceRef("urn:future-current-contract-test-only:registry-provenance", "9" * 64),)
    return a._make_registry_snapshot(
        tuple(entries),
        currentness_state=a.CURRENT_ACCEPTED,
        adoption_current_selection_evidence_refs=evidence,
        immutable_provenance=provenance,
    )


def _future_receipt(e: a.AcceptanceEntry, registry: a.AcceptanceRegistrySnapshot) -> a.AcceptanceReceipt:
    return a._issue_for_refs(e, a.ACCEPTANCE_AUTHORITY_REF, registry.registry_ref)


def test_h1_d1_reproduction_closed_future_current_is_representable(monkeypatch):
    assert a._CURRENT_REGISTRY.currentness_state == a.CANDIDATE_NOT_ADOPTED
    assert a._CURRENT_REGISTRY.entries == ()
    entry = _future_current_entry()
    registry = _future_registry(entry)
    receipt = _future_receipt(entry, registry)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", registry)
    assert _validate(receipt, currentness=a.CURRENT_ACCEPTED) == receipt


def test_h1_d2_reproduction_closed_forged_contact_pair_fails_constituent_validation():
    o = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_OCCURRENCE_WITNESS)
    i = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_WITNESS_INDEPENDENCE)
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
        a.validate_contact_acceptance_pair(forged_o, forged_i)


def test_empty_current_registry_still_fails_closed():
    entry = _future_current_entry()
    registry = _future_registry(entry)
    receipt = _future_receipt(entry, registry)
    with pytest.raises(a.AcceptanceMissingAuthority, match="registry is not current"):
        _validate(receipt, currentness=a.CURRENT_ACCEPTED)
    artifact = a.candidate_registry_artifact()
    assert artifact["current_positive_entries"] == []
    assert artifact["positive_fallback"] is False


def test_future_current_requires_exact_governed_membership_and_evidence(monkeypatch):
    entry = _future_current_entry()
    registry = _future_registry(entry)
    receipt = _future_receipt(entry, registry)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", registry)
    assert _validate(receipt, currentness=a.CURRENT_ACCEPTED) == receipt
    other = _future_current_entry(suffix="B")
    forged = _future_receipt(other, registry)
    with pytest.raises(a.AcceptanceMissingAuthority, match="no exact positive registry entry"):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_current_entry_or_receipt_mutation_fails(monkeypatch):
    entry = _future_current_entry()
    registry = _future_registry(entry)
    receipt = _future_receipt(entry, registry)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", registry)
    mutated_source = a.EvidenceRef("urn:future-current-contract-test-only:selection:MUTATED", "7" * 64)
    forged = _readdress_receipt(replace(receipt, source_acceptance_evidence_ref=mutated_source))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)
    bad_entry = replace(entry, entry_hash="8" * 64)
    with pytest.raises(a.AcceptanceIntegrityError):
        a._make_registry_snapshot(
            (bad_entry,),
            currentness_state=a.CURRENT_ACCEPTED,
            adoption_current_selection_evidence_refs=(bad_entry.source_acceptance_evidence_ref,),
            immutable_provenance=(a.EvidenceRef("urn:prov", "8" * 64),),
        )


def test_current_registry_or_issuer_substitution_fails(monkeypatch):
    entry = _future_current_entry()
    registry = _future_registry(entry)
    receipt = _future_receipt(entry, registry)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", registry)
    bad_registry = _readdress_receipt(replace(receipt, registry_ref=a.ContentAddressedRef("OTHER", "1.0.0", "1" * 64)))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(bad_registry, currentness=a.CURRENT_ACCEPTED)
    bad_issuer = _readdress_receipt(replace(receipt, acceptance_authority_ref=a.ContentAddressedRef("OTHER", "1.0.0", "2" * 64)))
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(bad_issuer, currentness=a.CURRENT_ACCEPTED)


def test_source_adoption_current_selection_evidence_mutation_fails(monkeypatch):
    entry = _future_current_entry()
    registry = _future_registry(entry)
    receipt = _future_receipt(entry, registry)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", registry)
    mutated = a.EvidenceRef("urn:future-current-contract-test-only:selection:forged", "3" * 64)
    forged = _readdress_receipt(replace(receipt, source_acceptance_evidence_ref=mutated))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_synthetic_receipt_cannot_masquerade_as_current():
    r = a.issue_noncurrent_synthetic_test_receipt(a.CAUSAL_USE_PERMISSION)
    forged = _readdress_receipt(replace(r, currentness_state=a.CURRENT_ACCEPTED))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_arbitrary_caller_cannot_self_issue_current_receipt():
    entry = _future_current_entry()
    registry = _future_registry(entry)
    receipt = _future_receipt(entry, registry)
    assert receipt.currentness_state == a.CURRENT_ACCEPTED
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(receipt, currentness=a.CURRENT_ACCEPTED)


def test_contact_pair_validates_both_constituents_before_success(monkeypatch):
    o = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_OCCURRENCE_WITNESS)
    i = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_WITNESS_INDEPENDENCE)
    original = a.validate_acceptance_receipt
    calls = []

    def wrapped(r, **kwargs):
        result = original(r, **kwargs)
        calls.append(kwargs["expected_role"])
        return result

    monkeypatch.setattr(a, "validate_acceptance_receipt", wrapped)
    assert a.validate_contact_acceptance_pair(o, i) == (o, i)
    assert calls == [a.CONTACT_OCCURRENCE_WITNESS, a.CONTACT_WITNESS_INDEPENDENCE]


def test_one_individually_forged_contact_constituent_fails_pair():
    o = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_OCCURRENCE_WITNESS)
    i = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_WITNESS_INDEPENDENCE)
    forged_i = replace(i, receipt_hash="0" * 64)
    with pytest.raises(a.AcceptanceIntegrityError):
        a.validate_contact_acceptance_pair(o, forged_i)


def test_same_occurrence_independence_accepted_authority_still_fails(monkeypatch):
    o_entry = next(e for e in a._SYNTH_ENTRIES if e.role == a.CONTACT_OCCURRENCE_WITNESS)
    i_entry = next(e for e in a._SYNTH_ENTRIES if e.role == a.CONTACT_WITNESS_INDEPENDENCE)
    i_entry = _readdress_entry(replace(i_entry, accepted_authority_ref=o_entry.accepted_authority_ref))
    entries = (o_entry, i_entry)
    synth_registry_ref = a.ContentAddressedRef(
        a.REGISTRY_ID + "_SYNTHETIC_TEST",
        "1.0.0",
        a._digest("SYNTH_REGISTRY", [e.entry_hash for e in entries]),
    )
    monkeypatch.setattr(a, "_SYNTH_ENTRIES", entries)
    monkeypatch.setattr(a, "_SYNTH_REGISTRY_REF", synth_registry_ref)
    o = a._issue_for_refs(o_entry, a._SYNTH_AUTHORITY_REF, synth_registry_ref)
    i = a._issue_for_refs(i_entry, a._SYNTH_AUTHORITY_REF, synth_registry_ref)
    with pytest.raises(a.AcceptanceOutOfScope, match="distinct accepted authorities"):
        a.validate_contact_acceptance_pair(o, i)


def test_same_receipt_for_occurrence_and_independence_still_fails():
    o = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_OCCURRENCE_WITNESS)
    with pytest.raises(a.AcceptanceOutOfScope):
        a.validate_contact_acceptance_pair(o, o)


@pytest.mark.parametrize("role", a.SUPPORTED_ROLES)
def test_all_four_roles_preserve_exact_scope_and_membership(role):
    r = a.issue_noncurrent_synthetic_test_receipt(role)
    assert _validate(r) == r
    widened_scope = replace(r.scope, object_scope=r.scope.object_scope + ("WIDENED",))
    forged = _readdress_receipt(replace(r, scope=widened_scope))
    with pytest.raises(a.AcceptanceMissingAuthority):
        a.validate_acceptance_receipt(
            forged,
            expected_role=role,
            expected_accepted_authority_ref=forged.accepted_authority_ref,
            expected_owner_jurisdiction_ref=forged.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=forged.source_acceptance_evidence_ref,
            expected_scope=widened_scope,
            required_currentness=a.NONCURRENT_SYNTHETIC_TEST_ONLY,
        )


def test_exact_replay_idempotence_remains_stable():
    for role in a.SUPPORTED_ROLES:
        assert a.issue_noncurrent_synthetic_test_receipt(role) == a.issue_noncurrent_synthetic_test_receipt(role)
    e = _future_current_entry()
    assert _future_registry(e) == _future_registry(e)


def test_authority_ceiling_and_no_semantic_truth_emission_remain_intact():
    artifact = a.candidate_registry_artifact()
    assert artifact["generic_project_wide_authority"] is False
    assert artifact["future_current_contract"]["no_latest_default_fuzzy_fallback"] is True
    assert set(artifact["authority_ceiling"]) == set(a.AUTHORITY_CEILING)
    receipt_fields = set(asdict(a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_OCCURRENCE_WITNESS)))
    assert receipt_fields.isdisjoint({
        "contact_occurred", "contact_independent", "causal_use_true", "applicable",
        "encounter", "exposure", "comparator", "psepf", "metabolism", "can_008",
        "v2", "positive_v3", "actor_mutation",
    })


def test_repaired_contract_hashes_are_not_stale_a1_hashes():
    assert a.ACCEPTANCE_AUTHORITY_CONTENT_HASH != "41b79e7f622f3c9eb0d6df649254c812fcb769db45cf6e47a808a95eebe2a50f"
    assert a.REGISTRY_CONTENT_HASH != "9ef38509ad5798c038bbcfa1b3a6e343df5a7c4f2a1ed4fd2af33f31f19e3a9e"


def test_w2_executor_blob_is_unchanged():
    data = W2.read_bytes()
    blob = sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    assert blob == W2_BLOB
