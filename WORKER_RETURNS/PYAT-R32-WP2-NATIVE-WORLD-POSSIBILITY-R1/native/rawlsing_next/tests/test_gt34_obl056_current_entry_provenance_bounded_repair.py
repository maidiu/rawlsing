from __future__ import annotations

from dataclasses import replace
from hashlib import sha1
from pathlib import Path

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as a


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_AUTHORITY_HASH = "6c9ab99a7d89835e7fdf405511abd7d6d66ced54b6e2fd8ef1863be842f39123"
EXPECTED_EMPTY_REGISTRY_HASH = "ca633451bfe56f86e1b463243bf721772a9ff582227411ed5137a346491b957e"
EXPECTED_W2_BLOB = "54d9acba40f0eb1db8bb03aec3c1bb900f849588"


def _entry(*, provenance: tuple[a.EvidenceRef, ...] | None = None) -> a.AcceptanceEntry:
    source = a.EvidenceRef("urn:r3:selection:exact", "1" * 64)
    if provenance is None:
        provenance = (a.EvidenceRef("urn:r3:entry-provenance:exact", "2" * 64),)
    provisional = a.AcceptanceEntry(
        a.ENTRY_SCHEMA_ID,
        a.CAUSAL_USE_PERMISSION,
        a.ContentAddressedRef("R3_FUTURE_CURRENT_CAUSAL_AUTHORITY", "1.0.0", "3" * 64),
        a.EvidenceRef("urn:r3:owner-jurisdiction:exact", "4" * 64),
        source,
        a.ACCEPT,
        a.CONSUMER,
        a.AcceptanceScope(
            a._TRANSITION_USE_BY_ROLE[a.CAUSAL_USE_PERMISSION],
            ("R3_FAMILY",),
            ("R3_SUBJECT",),
            ("R3_OBJECT",),
        ),
        (),
        a.CURRENT_ACCEPTED,
        provenance,
        "PENDING",
        "0" * 64,
    )
    h = a._digest("ENTRY", a._entry_body(provisional))
    return replace(
        provisional,
        entry_id="urn:rawlsing:gt34:obl056:acceptance-entry:sha256:" + h,
        entry_hash=h,
    )


def _registry_provenance() -> tuple[a.EvidenceRef, ...]:
    return (a.EvidenceRef("urn:r3:registry-provenance:exact", "5" * 64),)


def _good_snapshot(entry: a.AcceptanceEntry) -> a.AcceptanceRegistrySnapshot:
    return a._make_registry_snapshot(
        (entry,),
        currentness_state=a.CURRENT_ACCEPTED,
        adoption_current_selection_evidence_refs=(entry.source_acceptance_evidence_ref,),
        immutable_provenance=_registry_provenance(),
    )


def _handcrafted_snapshot(entry: a.AcceptanceEntry) -> a.AcceptanceRegistrySnapshot:
    evidence = (entry.source_acceptance_evidence_ref,)
    provenance = _registry_provenance()
    material = a._registry_material(
        acceptance_authority_ref=a.ACCEPTANCE_AUTHORITY_REF,
        currentness_state=a.CURRENT_ACCEPTED,
        adoption_current_selection_evidence_refs=evidence,
        immutable_provenance=provenance,
        entries=(entry,),
    )
    h = a._digest("REGISTRY", material)
    return a.AcceptanceRegistrySnapshot(
        a.REGISTRY_SNAPSHOT_SCHEMA_ID,
        a.ACCEPTANCE_AUTHORITY_REF,
        a.ContentAddressedRef(a.REGISTRY_ID, a.REGISTRY_VERSION, h),
        a.CURRENT_ACCEPTED,
        evidence,
        provenance,
        (entry,),
    )


def _receipt(entry: a.AcceptanceEntry, snapshot: a.AcceptanceRegistrySnapshot) -> a.AcceptanceReceipt:
    return a._issue_for_refs(entry, a.ACCEPTANCE_AUTHORITY_REF, snapshot.registry_ref)


def _validate(receipt: a.AcceptanceReceipt) -> a.AcceptanceReceipt:
    return a.validate_acceptance_receipt(
        receipt,
        expected_role=receipt.role,
        expected_accepted_authority_ref=receipt.accepted_authority_ref,
        expected_owner_jurisdiction_ref=receipt.accepted_authority_owner_jurisdiction_ref,
        expected_source_acceptance_evidence_ref=receipt.source_acceptance_evidence_ref,
        expected_scope=receipt.scope,
        required_currentness=a.CURRENT_ACCEPTED,
    )


def _git_blob(path: str) -> str:
    data = (ROOT / path).read_bytes()
    return sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def test_01_exact_future_current_entry_with_nonempty_provenance_remains_representable(monkeypatch):
    entry = _entry()
    snapshot = _good_snapshot(entry)
    receipt = _receipt(entry, snapshot)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snapshot)
    assert _validate(receipt) == receipt


def test_02_empty_current_entry_provenance_fails_snapshot_construction():
    entry = _entry(provenance=())
    with pytest.raises(a.AcceptanceMissingAuthority, match="entry requires immutable provenance"):
        _good_snapshot(entry)


def test_03_empty_current_entry_provenance_fails_again_at_validation(monkeypatch):
    entry = _entry(provenance=())
    snapshot = _handcrafted_snapshot(entry)
    receipt = _receipt(entry, snapshot)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snapshot)
    with pytest.raises(a.AcceptanceMissingAuthority, match="entry lacks immutable provenance"):
        _validate(receipt)


def test_04_installed_candidate_registry_stays_empty_and_current_fails_closed():
    assert a._CURRENT_REGISTRY.currentness_state == a.CANDIDATE_NOT_ADOPTED
    assert a._CURRENT_REGISTRY.entries == ()
    assert a.candidate_registry_artifact()["current_positive_entries"] == []
    entry = _entry()
    snapshot = _good_snapshot(entry)
    receipt = _receipt(entry, snapshot)
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(receipt)


def test_05_contract_artifacts_explicitly_require_entry_and_registry_provenance():
    registry = a.candidate_registry_artifact()
    receipt = a.receipt_schema_artifact()
    assert registry["future_current_contract"]["requires_immutable_entry_provenance"] is True
    assert registry["future_current_contract"]["requires_immutable_registry_provenance"] is True
    assert receipt["current_entry_requires_immutable_provenance"] is True
    assert receipt["current_registry_requires_adoption_current_selection_evidence"] is True


def test_06_authority_and_present_empty_registry_content_addresses_remain_exact():
    assert a.ACCEPTANCE_AUTHORITY_CONTENT_HASH == EXPECTED_AUTHORITY_HASH
    assert a.ACCEPTANCE_AUTHORITY_REF.content_hash == EXPECTED_AUTHORITY_HASH
    assert a.REGISTRY_CONTENT_HASH == EXPECTED_EMPTY_REGISTRY_HASH
    assert a.REGISTRY_REF.content_hash == EXPECTED_EMPTY_REGISTRY_HASH


def test_07_contact_pair_constituent_first_repair_remains_operable_and_forgery_fails():
    occurrence = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_OCCURRENCE_WITNESS)
    independence = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_WITNESS_INDEPENDENCE)
    assert a.validate_contact_acceptance_pair(occurrence, independence) == (occurrence, independence)
    forged_occurrence = replace(occurrence, receipt_id="urn:r3:forged-receipt")
    with pytest.raises(a.AcceptanceIntegrityError):
        a.validate_contact_acceptance_pair(forged_occurrence, independence)


def test_08_w2_executor_blob_is_untouched():
    assert _git_blob("rawlsing_next/v3_adp010_oee_executor_authenticated.py") == EXPECTED_W2_BLOB
