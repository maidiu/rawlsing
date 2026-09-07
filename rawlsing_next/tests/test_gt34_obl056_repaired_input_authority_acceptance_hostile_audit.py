from __future__ import annotations

from dataclasses import asdict, replace
from hashlib import sha1, sha256
import inspect
import json
from pathlib import Path
import unicodedata

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as a


ROOT = Path(__file__).resolve().parents[2]
DOMAIN = "RAWLSING\0GT34\0OBL056\0ADP010_INPUT_AUTHORITY_ACCEPTANCE_V1\0"
EXPECTED_AUTHORITY_HASH = "6c9ab99a7d89835e7fdf405511abd7d6d66ced54b6e2fd8ef1863be842f39123"
EXPECTED_EMPTY_REGISTRY_HASH = "ca633451bfe56f86e1b463243bf721772a9ff582227411ed5137a346491b957e"
EXPECTED_BLOBS = {
    "rawlsing_next/gt34_adp010_input_authority_acceptance.py": "1bbc83f66f85ab46f4e1732fb43a158c0737dd6d",
    "rawlsing_next/tests/test_gt34_obl056_adp010_input_authority_acceptance.py": "454407f251c4146a2c0db8780afd7ea2e0b0a10c",
    "rawlsing_next/tests/test_gt34_obl056_future_current_contact_pair_repair.py": "c86896aa20224695f92ec9b89c27f9d2bb3d7a78",
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT34_OBL056_ACCEPTANCE_AUTHORITY_WAVE_R1/R2_FUTURE_CURRENT_CONTACT_PAIR_BOUNDED_REPAIR_R1/01_REPAIRED_AUTHORITY_REGISTRY.json": "7d9b2f4c4972c8bdcc7d9f958d136bb60532a1d6",
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT34_OBL056_ACCEPTANCE_AUTHORITY_WAVE_R1/R2_FUTURE_CURRENT_CONTACT_PAIR_BOUNDED_REPAIR_R1/02_REPAIRED_RECEIPT_SCHEMA_AND_CONTRACT_EXAMPLE.json": "7200514716f568356f6075b3decae29c247b169a",
    "rawlsing_next/v3_adp010_oee_executor_authenticated.py": "54d9acba40f0eb1db8bb03aec3c1bb900f849588",
}


def _norm(v):
    if isinstance(v, str):
        return unicodedata.normalize("NFC", v)
    if isinstance(v, dict):
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_norm(x) for x in v]
    return v


def _digest(label: str, value) -> str:
    body = json.dumps(_norm(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256((DOMAIN + label + "\0" + body).encode()).hexdigest()


def _entry_body(e: a.AcceptanceEntry):
    return {
        "schema_id": e.schema_id,
        "role": e.role,
        "accepted_authority_ref": asdict(e.accepted_authority_ref),
        "accepted_authority_owner_jurisdiction_ref": asdict(e.accepted_authority_owner_jurisdiction_ref),
        "source_acceptance_evidence_ref": asdict(e.source_acceptance_evidence_ref),
        "decision_state": e.decision_state,
        "consumer": e.consumer,
        "scope": asdict(e.scope),
        "negative_limit_refs": [asdict(x) for x in e.negative_limit_refs],
        "currentness_state": e.currentness_state,
        "immutable_provenance": [asdict(x) for x in e.immutable_provenance],
    }


def _receipt_body(r: a.AcceptanceReceipt):
    return {
        "schema_id": r.schema_id,
        "acceptance_authority_ref": asdict(r.acceptance_authority_ref),
        "registry_ref": asdict(r.registry_ref),
        "registry_entry_ref": asdict(r.registry_entry_ref),
        "role": r.role,
        "accepted_authority_ref": asdict(r.accepted_authority_ref),
        "accepted_authority_owner_jurisdiction_ref": asdict(r.accepted_authority_owner_jurisdiction_ref),
        "source_acceptance_evidence_ref": asdict(r.source_acceptance_evidence_ref),
        "decision_state": r.decision_state,
        "consumer": r.consumer,
        "scope": asdict(r.scope),
        "negative_limit_refs": [asdict(x) for x in r.negative_limit_refs],
        "currentness_state": r.currentness_state,
        "immutable_provenance": [asdict(x) for x in r.immutable_provenance],
    }


def _readdress_entry(e: a.AcceptanceEntry) -> a.AcceptanceEntry:
    provisional = replace(e, entry_id="PENDING", entry_hash="0" * 64)
    h = _digest("ENTRY", _entry_body(provisional))
    return replace(e, entry_id=f"urn:rawlsing:gt34:obl056:acceptance-entry:sha256:{h}", entry_hash=h)


def _readdress_receipt(r: a.AcceptanceReceipt) -> a.AcceptanceReceipt:
    provisional = replace(r, receipt_id="PENDING", receipt_hash="0" * 64)
    h = _digest("RECEIPT", _receipt_body(provisional))
    return replace(r, receipt_id=f"urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:{h}", receipt_hash=h)


def _current_entry(
    role: str = a.CAUSAL_USE_PERMISSION,
    *,
    suffix: str = "A",
    provenance: tuple[a.EvidenceRef, ...] | None = None,
    decision: str = a.ACCEPT,
    currentness: str = a.CURRENT_ACCEPTED,
    source: a.EvidenceRef | None = None,
    authority: a.ContentAddressedRef | None = None,
    owner: a.EvidenceRef | None = None,
    scope: a.AcceptanceScope | None = None,
    limits: tuple[a.EvidenceRef, ...] = (),
) -> a.AcceptanceEntry:
    source = source or a.EvidenceRef(f"urn:h2:selection:{suffix}", (suffix.lower() * 64)[:64])
    authority = authority or a.ContentAddressedRef(f"H2_FUTURE_CURRENT_{role}_{suffix}", "1.0.0", ("a" + suffix.lower()) * 32)
    owner = owner or a.EvidenceRef(f"urn:h2:owner:{suffix}", ("b" + suffix.lower()) * 32)
    scope = scope or a.AcceptanceScope(
        a._TRANSITION_USE_BY_ROLE[role],
        (f"H2_FAMILY_{suffix}",),
        (f"H2_SUBJECT_{suffix}",),
        (f"H2_OBJECT_{suffix}",),
    )
    if provenance is None:
        provenance = (a.EvidenceRef(f"urn:h2:entry-provenance:{suffix}", ("c" + suffix.lower()) * 32),)
    entry = a.AcceptanceEntry(
        a.ENTRY_SCHEMA_ID,
        role,
        authority,
        owner,
        source,
        decision,
        a.CONSUMER,
        scope,
        limits,
        currentness,
        provenance,
        "PENDING",
        "0" * 64,
    )
    return _readdress_entry(entry)


def _registry_material(
    entries: tuple[a.AcceptanceEntry, ...],
    *,
    currentness: str = a.CURRENT_ACCEPTED,
    evidence: tuple[a.EvidenceRef, ...] = (),
    provenance: tuple[a.EvidenceRef, ...] = (),
    authority_ref: a.ContentAddressedRef = a.ACCEPTANCE_AUTHORITY_REF,
):
    return {
        "registry_schema_id": a.REGISTRY_SNAPSHOT_SCHEMA_ID,
        "registry_id": a.REGISTRY_ID,
        "registry_version": a.REGISTRY_VERSION,
        "acceptance_authority_ref": asdict(authority_ref),
        "receipt_schema_id": a.RECEIPT_SCHEMA_ID,
        "consumer": a.CONSUMER,
        "supported_roles": a.SUPPORTED_ROLES,
        "currentness_state": currentness,
        "adoption_current_selection_evidence_refs": [asdict(x) for x in evidence],
        "immutable_provenance": [asdict(x) for x in provenance],
        "current_positive_entries": [{"entry_id": e.entry_id, "entry_hash": e.entry_hash} for e in entries],
    }


def _snapshot(
    entries: tuple[a.AcceptanceEntry, ...],
    *,
    currentness: str = a.CURRENT_ACCEPTED,
    evidence: tuple[a.EvidenceRef, ...] | None = None,
    provenance: tuple[a.EvidenceRef, ...] | None = None,
    authority_ref: a.ContentAddressedRef = a.ACCEPTANCE_AUTHORITY_REF,
) -> a.AcceptanceRegistrySnapshot:
    if evidence is None:
        evidence = tuple(e.source_acceptance_evidence_ref for e in entries)
    if provenance is None:
        provenance = (a.EvidenceRef("urn:h2:registry-provenance", "9" * 64),)
    material = _registry_material(entries, currentness=currentness, evidence=evidence, provenance=provenance, authority_ref=authority_ref)
    h = _digest("REGISTRY", material)
    return a.AcceptanceRegistrySnapshot(
        a.REGISTRY_SNAPSHOT_SCHEMA_ID,
        authority_ref,
        a.ContentAddressedRef(a.REGISTRY_ID, a.REGISTRY_VERSION, h),
        currentness,
        evidence,
        provenance,
        entries,
    )


def _receipt(entry: a.AcceptanceEntry, snapshot: a.AcceptanceRegistrySnapshot) -> a.AcceptanceReceipt:
    r = a.AcceptanceReceipt(
        a.RECEIPT_SCHEMA_ID,
        snapshot.acceptance_authority_ref,
        snapshot.registry_ref,
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
    return _readdress_receipt(r)


def _validate(r: a.AcceptanceReceipt, *, role=None, currentness=None, scope=None):
    return a.validate_acceptance_receipt(
        r,
        expected_role=role or r.role,
        expected_accepted_authority_ref=r.accepted_authority_ref,
        expected_owner_jurisdiction_ref=r.accepted_authority_owner_jurisdiction_ref,
        expected_source_acceptance_evidence_ref=r.source_acceptance_evidence_ref,
        expected_scope=scope or r.scope,
        required_currentness=currentness or r.currentness_state,
    )


def _good(role: str):
    return a.issue_noncurrent_synthetic_test_receipt(role)


def _git_blob(path: str) -> str:
    data = (ROOT / path).read_bytes()
    return sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def test_01_installed_candidate_current_registry_is_empty_and_current_fails_closed():
    assert a._CURRENT_REGISTRY.currentness_state == a.CANDIDATE_NOT_ADOPTED
    assert a._CURRENT_REGISTRY.entries == ()
    assert a.candidate_registry_artifact()["current_positive_entries"] == []
    entry = _current_entry()
    snap = _snapshot((entry,))
    r = _receipt(entry, snap)
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_02_future_current_exact_positive_is_representable_under_exact_snapshot(monkeypatch):
    entry = _current_entry()
    snap = _snapshot((entry,))
    r = _receipt(entry, snap)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    assert _validate(r, currentness=a.CURRENT_ACCEPTED) == r


def test_03_ADOPTION_BLOCKER_current_entry_empty_immutable_provenance_is_accepted(monkeypatch):
    entry = _current_entry(provenance=())
    # The candidate's own future-current registry constructor accepts the entry even
    # though the governing contract requires immutable entry provenance.
    snap = a._make_registry_snapshot(
        (entry,),
        currentness_state=a.CURRENT_ACCEPTED,
        adoption_current_selection_evidence_refs=(entry.source_acceptance_evidence_ref,),
        immutable_provenance=(a.EvidenceRef("urn:h2:registry-provenance", "9" * 64),),
    )
    r = a._issue_for_refs(entry, a.ACCEPTANCE_AUTHORITY_REF, snap.registry_ref)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    assert r.immutable_provenance == ()
    assert _validate(r, currentness=a.CURRENT_ACCEPTED) == r


@pytest.mark.parametrize("axis", ["authority-id", "authority-hash", "registry-id", "registry-hash"])
def test_04_current_registry_identity_or_hash_substitution_fails(monkeypatch, axis):
    entry = _current_entry()
    snap = _snapshot((entry,))
    r = _receipt(entry, snap)
    if axis == "authority-id":
        bad = replace(snap, acceptance_authority_ref=replace(snap.acceptance_authority_ref, id="OTHER"))
    elif axis == "authority-hash":
        bad = replace(snap, acceptance_authority_ref=replace(snap.acceptance_authority_ref, content_hash="0" * 64))
    elif axis == "registry-id":
        bad = replace(snap, registry_ref=replace(snap.registry_ref, id="OTHER"))
    else:
        bad = replace(snap, registry_ref=replace(snap.registry_ref, content_hash="0" * 64))
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", bad)
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_05_current_registry_empty_adoption_selection_evidence_fails(monkeypatch):
    entry = _current_entry()
    snap = _snapshot((entry,), evidence=())
    r = _receipt(entry, snap)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    with pytest.raises(a.AcceptanceMissingAuthority, match="adoption/current-selection"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_06_current_registry_missing_registry_provenance_fails(monkeypatch):
    entry = _current_entry()
    snap = _snapshot((entry,), provenance=())
    r = _receipt(entry, snap)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    with pytest.raises(a.AcceptanceMissingAuthority, match="immutable provenance"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_07_entry_source_not_selected_by_current_registry_fails(monkeypatch):
    entry = _current_entry()
    other = a.EvidenceRef("urn:h2:other-selection", "7" * 64)
    snap = _snapshot((entry,), evidence=(other,))
    r = _receipt(entry, snap)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    with pytest.raises(a.AcceptanceMissingAuthority, match="not selected"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_08_duplicate_ambiguous_current_membership_fails(monkeypatch):
    entry = _current_entry()
    snap = _snapshot((entry, entry), evidence=(entry.source_acceptance_evidence_ref,))
    r = _receipt(entry, snap)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    with pytest.raises(a.AcceptanceMissingAuthority, match="no exact positive registry entry"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_09_current_receipt_without_membership_fails(monkeypatch):
    member = _current_entry(suffix="M")
    attacker = _current_entry(suffix="A")
    snap = _snapshot((member,))
    r = _receipt(attacker, snap)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    with pytest.raises(a.AcceptanceMissingAuthority, match="no exact positive registry entry"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


@pytest.mark.parametrize("axis", ["role", "consumer", "transition", "family", "subject", "object", "authority-id", "authority-version", "authority-hash", "owner", "source", "limits", "entry-currentness"])
def test_10_current_entry_binding_mutations_fail(monkeypatch, axis):
    entry = _current_entry()
    snap = _snapshot((entry,))
    r = _receipt(entry, snap)
    if axis == "role":
        forged = replace(r, role=a.POSITIVE_APPLICABILITY)
    elif axis == "consumer":
        forged = replace(r, consumer="OTHER_CONSUMER@1.0.0")
    elif axis in {"transition", "family", "subject", "object"}:
        field = {"transition": "transition_use_scope", "family": "family_scope", "subject": "subject_scope", "object": "object_scope"}[axis]
        value = "OTHER:USE" if field == "transition_use_scope" else ("OTHER",)
        forged = replace(r, scope=replace(r.scope, **{field: value}))
    elif axis == "authority-id":
        forged = replace(r, accepted_authority_ref=replace(r.accepted_authority_ref, id="OTHER"))
    elif axis == "authority-version":
        forged = replace(r, accepted_authority_ref=replace(r.accepted_authority_ref, version="2.0.0"))
    elif axis == "authority-hash":
        forged = replace(r, accepted_authority_ref=replace(r.accepted_authority_ref, content_hash="4" * 64))
    elif axis == "owner":
        forged = replace(r, accepted_authority_owner_jurisdiction_ref=a.EvidenceRef("urn:h2:other-owner", "4" * 64))
    elif axis == "source":
        forged = replace(r, source_acceptance_evidence_ref=a.EvidenceRef("urn:h2:other-source", "5" * 64))
    elif axis == "limits":
        forged = replace(r, negative_limit_refs=(a.EvidenceRef("urn:h2:limit", "6" * 64),))
    else:
        forged = replace(r, currentness_state=a.NONCURRENT_SYNTHETIC_TEST_ONLY)
    forged = _readdress_receipt(forged)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    with pytest.raises(a.AcceptanceAuthorityError):
        _validate(forged, currentness=forged.currentness_state if axis == "entry-currentness" else a.CURRENT_ACCEPTED, scope=forged.scope)


def test_11_current_entry_identity_hash_corruption_fails_registry_construction():
    entry = replace(_current_entry(), entry_hash="1" * 64)
    with pytest.raises(a.AcceptanceIntegrityError):
        a._make_registry_snapshot(
            (entry,),
            currentness_state=a.CURRENT_ACCEPTED,
            adoption_current_selection_evidence_refs=(entry.source_acceptance_evidence_ref,),
            immutable_provenance=(a.EvidenceRef("urn:h2:registry-provenance", "9" * 64),),
        )


@pytest.mark.parametrize("axis", ["id", "hash"])
def test_12_current_receipt_identity_hash_corruption_fails(monkeypatch, axis):
    entry = _current_entry()
    snap = _snapshot((entry,))
    r = _receipt(entry, snap)
    forged = replace(r, **({"receipt_id": "urn:h2:forged"} if axis == "id" else {"receipt_hash": "2" * 64}))
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_13_synthetic_current_shape_masquerade_fails():
    r = _good(a.CAUSAL_USE_PERMISSION)
    forged = _readdress_receipt(replace(r, currentness_state=a.CURRENT_ACCEPTED))
    with pytest.raises(a.AcceptanceAuthorityError):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)


def test_14_no_latest_default_fuzzy_or_positive_fallback_surface():
    artifact = a.candidate_registry_artifact()
    assert artifact["positive_fallback"] is False
    assert artifact["future_current_contract"]["no_latest_default_fuzzy_fallback"] is True
    sig = inspect.signature(a.validate_acceptance_receipt)
    assert set(sig.parameters) == {
        "r", "expected_role", "expected_accepted_authority_ref", "expected_owner_jurisdiction_ref",
        "expected_source_acceptance_evidence_ref", "expected_scope", "required_currentness",
    }


def _forged_nonmember(r: a.AcceptanceReceipt) -> a.AcceptanceReceipt:
    ref = a.ContentAddressedRef("H2_NONMEMBER", "1.0.0", "3" * 64)
    return _readdress_receipt(replace(r, accepted_authority_ref=ref))


@pytest.mark.parametrize("case", ["forged-occurrence", "forged-independence", "both-forged"])
def test_15_contact_pair_rejects_forged_constituents_before_success(case):
    o = _good(a.CONTACT_OCCURRENCE_WITNESS)
    i = _good(a.CONTACT_WITNESS_INDEPENDENCE)
    if case in {"forged-occurrence", "both-forged"}:
        o = _forged_nonmember(o)
    if case in {"forged-independence", "both-forged"}:
        i = _forged_nonmember(i)
    with pytest.raises(a.AcceptanceAuthorityError):
        a.validate_contact_acceptance_pair(o, i)


@pytest.mark.parametrize("axis", ["integrity", "issuer", "registry", "role", "consumer", "scope", "owner", "source", "currentness", "decision"])
def test_16_contact_constituent_invalidity_cannot_reach_pair_success(axis):
    o = _good(a.CONTACT_OCCURRENCE_WITNESS)
    i = _good(a.CONTACT_WITNESS_INDEPENDENCE)
    if axis == "integrity":
        bad = replace(o, receipt_hash="0" * 64)
    elif axis == "issuer":
        bad = _readdress_receipt(replace(o, acceptance_authority_ref=a.ContentAddressedRef("OTHER", "1", "1" * 64)))
    elif axis == "registry":
        bad = _readdress_receipt(replace(o, registry_ref=a.ContentAddressedRef("OTHER", "1", "2" * 64)))
    elif axis == "role":
        bad = _readdress_receipt(replace(o, role=a.POSITIVE_APPLICABILITY))
    elif axis == "consumer":
        bad = _readdress_receipt(replace(o, consumer="OTHER_CONSUMER@1.0.0"))
    elif axis == "scope":
        bad = _readdress_receipt(replace(o, scope=replace(o.scope, object_scope=("OTHER",))))
    elif axis == "owner":
        bad = _readdress_receipt(replace(o, accepted_authority_owner_jurisdiction_ref=a.EvidenceRef("urn:h2:owner", "3" * 64)))
    elif axis == "source":
        bad = _readdress_receipt(replace(o, source_acceptance_evidence_ref=a.EvidenceRef("urn:h2:source", "4" * 64)))
    elif axis == "currentness":
        bad = _readdress_receipt(replace(o, currentness_state=a.CURRENT_ACCEPTED))
    else:
        bad = _readdress_receipt(replace(o, decision_state="REJECT"))
    with pytest.raises(a.AcceptanceAuthorityError):
        a.validate_contact_acceptance_pair(bad, i)


def test_17_contact_same_authority_fails_after_both_individually_validate(monkeypatch):
    o_entry = next(e for e in a._SYNTH_ENTRIES if e.role == a.CONTACT_OCCURRENCE_WITNESS)
    i_entry = next(e for e in a._SYNTH_ENTRIES if e.role == a.CONTACT_WITNESS_INDEPENDENCE)
    i_entry = _readdress_entry(replace(i_entry, accepted_authority_ref=o_entry.accepted_authority_ref))
    entries = (o_entry, i_entry)
    registry_ref = a.ContentAddressedRef(
        a.REGISTRY_ID + "_SYNTHETIC_TEST", "1.0.0", _digest("SYNTH_REGISTRY", [e.entry_hash for e in entries])
    )
    monkeypatch.setattr(a, "_SYNTH_ENTRIES", entries)
    monkeypatch.setattr(a, "_SYNTH_REGISTRY_REF", registry_ref)
    o = a._issue_for_refs(o_entry, a._SYNTH_AUTHORITY_REF, registry_ref)
    i = a._issue_for_refs(i_entry, a._SYNTH_AUTHORITY_REF, registry_ref)
    assert _validate(o) == o
    assert _validate(i) == i
    with pytest.raises(a.AcceptanceOutOfScope, match="distinct accepted authorities"):
        a.validate_contact_acceptance_pair(o, i)


def test_18_contact_same_receipt_identity_hash_cannot_individually_validate_for_both_roles():
    o = _good(a.CONTACT_OCCURRENCE_WITNESS)
    i = _good(a.CONTACT_WITNESS_INDEPENDENCE)
    forged = replace(i, receipt_id=o.receipt_id, receipt_hash=o.receipt_hash)
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(forged)
    with pytest.raises(a.AcceptanceAuthorityError):
        a.validate_contact_acceptance_pair(o, forged)


@pytest.mark.parametrize("role", a.SUPPORTED_ROLES)
def test_19_all_four_roles_remain_exact_and_replayable(role):
    r1 = _good(role)
    r2 = _good(role)
    assert r1 == r2
    assert _validate(r1) == r1
    other_roles = [x for x in a.SUPPORTED_ROLES if x != role]
    with pytest.raises(a.AcceptanceOutOfScope):
        _validate(r1, role=other_roles[0])


def test_20_body_mutation_plus_attacker_rehash_does_not_confer_nonmember_competence():
    r = _good(a.CAUSAL_USE_PERMISSION)
    forged = _forged_nonmember(r)
    assert _digest("RECEIPT", _receipt_body(replace(forged, receipt_id="PENDING", receipt_hash="0" * 64))) == forged.receipt_hash
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_21_authority_hash_independently_recomputes_exactly():
    material = {
        "authority_id": a.ACCEPTANCE_AUTHORITY_ID,
        "authority_version": a.ACCEPTANCE_AUTHORITY_VERSION,
        "grain": "EXACT_ALREADY_EXISTING_AUTHORITY_ACCEPTANCE_FOR_ONE_ADP010_INPUT_ROLE_AND_SCOPE_ONLY",
        "consumer": a.CONSUMER,
        "supported_roles": a.SUPPORTED_ROLES,
        "status": a.CANDIDATE_NOT_ADOPTED,
        "authority_ceiling": a.AUTHORITY_CEILING,
        "contract_revision": "R2_FUTURE_CURRENT_EXACT_MEMBERSHIP_AND_CONTACT_CONSTITUENT_VALIDATION",
        "future_current_law": "CURRENT_ACCEPTED_REQUIRES_EXACT_GOVERNED_REGISTRY_MEMBERSHIP_AND_ADOPTION_CURRENT_SELECTION_EVIDENCE",
        "contact_pair_law": "VALIDATE_BOTH_CONSTITUENT_ACCEPTANCE_RECEIPTS_BEFORE_PAIR_DISTINCTNESS",
    }
    assert _digest("AUTHORITY", material) == a.ACCEPTANCE_AUTHORITY_CONTENT_HASH == EXPECTED_AUTHORITY_HASH


def test_22_empty_registry_hash_independently_recomputes_exactly():
    material = _registry_material((), currentness=a.CANDIDATE_NOT_ADOPTED, evidence=(), provenance=())
    assert _digest("REGISTRY", material) == a.REGISTRY_CONTENT_HASH == EXPECTED_EMPTY_REGISTRY_HASH


def test_23_nfc_and_key_order_canonicalization_is_deterministic():
    left = {"z": "e\u0301", "a": {"y": 2, "x": 1}}
    right = {"a": {"x": 1, "y": 2}, "z": "é"}
    assert _digest("H2_CANONICAL", left) == _digest("H2_CANONICAL", right)


def test_24_repaired_candidate_relevant_git_blobs_are_exact():
    for path, expected in EXPECTED_BLOBS.items():
        assert _git_blob(path) == expected, path


def test_25_authority_ceiling_has_no_semantic_or_downstream_escape():
    artifact = a.candidate_registry_artifact()
    assert tuple(artifact["supported_roles"]) == a.SUPPORTED_ROLES
    assert artifact["consumer"] == a.CONSUMER
    assert artifact["generic_project_wide_authority"] is False
    assert set(artifact["authority_ceiling"]) == set(a.AUTHORITY_CEILING)
    fields = set(asdict(_good(a.CONTACT_OCCURRENCE_WITNESS)))
    assert fields.isdisjoint({
        "subject_identity", "subject_classification", "causal_use_true", "applicable",
        "contact_occurred", "contact_independent", "encounter", "exposure", "event_admission",
        "comparator", "psepf", "metabolism", "can_008", "v2", "positive_v3", "actor_mutation",
    })


def test_26_unmatched_corrupt_registry_entry_cannot_change_target_authority_result(monkeypatch):
    target = _current_entry(suffix="T")
    other = _current_entry(suffix="O")
    corrupt_other = replace(other, consumer="CORRUPTED_BUT_UNMATCHED")
    # Registry identity binds the other member by its content-addressed entry ref; the
    # target result must remain solely dependent on one exact target membership.
    snap = _snapshot((target, corrupt_other), evidence=(target.source_acceptance_evidence_ref, corrupt_other.source_acceptance_evidence_ref))
    r = _receipt(target, snap)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    assert _validate(r, currentness=a.CURRENT_ACCEPTED) == r


def test_27_registry_entry_ref_mismatch_fails_even_with_readdressed_receipt(monkeypatch):
    entry = _current_entry()
    snap = _snapshot((entry,))
    r = _receipt(entry, snap)
    forged = _readdress_receipt(replace(r, registry_entry_ref=a.EvidenceRef("urn:h2:wrong-entry", "8" * 64)))
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", snap)
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, currentness=a.CURRENT_ACCEPTED)
