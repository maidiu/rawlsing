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
EXPECTED_IMPLEMENTATION_BLOB = "49538b9c36e58e19a6dc293ecac5bc2dff58eebe"
EXPECTED_W2_BLOB = "54d9acba40f0eb1db8bb03aec3c1bb900f849588"
EXPECTED_R3_FOCUSED_BLOB = "fe4c67ab66d574b577be03b7f8848ca79c227310"
EXPECTED_R3_REGISTRY_ARTIFACT_BLOB = "d92d362d9ae4dae9b052b98213c87217f239a020"
EXPECTED_R3_RECEIPT_ARTIFACT_BLOB = "8c770b08a0a687f74b13580e064d4405cb1c6e5c"
EXPECTED_R3_COMPATIBILITY_ARTIFACT_BLOB = "8033fba2e95f31966c38393a9d91d7aabd048ee2"
EXPECTED_R3_EVIDENCE_BLOB = "84b89a96ceb33679d6525d91ab30fe58e2a90bc3"
R3_DIR = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT34_OBL056_ACCEPTANCE_AUTHORITY_WAVE_R1/"
    "R3_CURRENT_ACCEPTED_ENTRY_PROVENANCE_BOUNDED_REPAIR_R1"
)


def _norm(v):
    if isinstance(v, str):
        return unicodedata.normalize("NFC", v)
    if isinstance(v, dict):
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_norm(x) for x in v]
    return v


def _canonical(v) -> str:
    return json.dumps(_norm(v), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(label: str, v) -> str:
    return sha256((DOMAIN + label + "\0" + _canonical(v)).encode()).hexdigest()


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
    p = replace(e, entry_id="PENDING", entry_hash="0" * 64)
    h = _digest("ENTRY", _entry_body(p))
    return replace(e, entry_id="urn:rawlsing:gt34:obl056:acceptance-entry:sha256:" + h, entry_hash=h)


def _readdress_receipt(r: a.AcceptanceReceipt) -> a.AcceptanceReceipt:
    p = replace(r, receipt_id="PENDING", receipt_hash="0" * 64)
    h = _digest("RECEIPT", _receipt_body(p))
    return replace(r, receipt_id="urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:" + h, receipt_hash=h)


def _entry(
    role: str = a.CAUSAL_USE_PERMISSION,
    *,
    suffix: str = "A",
    provenance: tuple[a.EvidenceRef, ...] | None = None,
    schema_id: str | None = None,
    scope: a.AcceptanceScope | None = None,
    owner: a.EvidenceRef | None = None,
    source: a.EvidenceRef | None = None,
    authority: a.ContentAddressedRef | None = None,
    limits: tuple[a.EvidenceRef, ...] = (),
    decision: str = a.ACCEPT,
    currentness: str = a.CURRENT_ACCEPTED,
    consumer: str = a.CONSUMER,
) -> a.AcceptanceEntry:
    source = source or a.EvidenceRef(f"urn:h3:selection:{suffix}", sha256(("selection:" + suffix).encode()).hexdigest())
    owner = owner or a.EvidenceRef(f"urn:h3:owner:{suffix}", sha256(("owner:" + suffix).encode()).hexdigest())
    authority = authority or a.ContentAddressedRef(
        f"H3_FUTURE_CURRENT_{role}_{suffix}", "1.0.0", sha256(("authority:" + role + ":" + suffix).encode()).hexdigest()
    )
    if provenance is None:
        provenance = (
            a.EvidenceRef(f"urn:h3:entry-provenance:{suffix}", sha256(("entry-prov:" + suffix).encode()).hexdigest()),
        )
    scope = scope or a.AcceptanceScope(
        a._TRANSITION_USE_BY_ROLE[role],
        (f"H3_FAMILY_{suffix}",),
        (f"H3_SUBJECT_{suffix}",),
        (f"H3_OBJECT_{suffix}",),
    )
    e = a.AcceptanceEntry(
        schema_id or a.ENTRY_SCHEMA_ID,
        role,
        authority,
        owner,
        source,
        decision,
        consumer,
        scope,
        limits,
        currentness,
        provenance,
        "PENDING",
        "0" * 64,
    )
    return _readdress_entry(e)


def _registry_provenance(*, empty_fields: bool = False):
    if empty_fields:
        return (a.EvidenceRef("", ""),)
    return (a.EvidenceRef("urn:h3:registry-provenance", sha256(b"h3-registry-provenance").hexdigest()),)


def _snapshot(
    entries: tuple[a.AcceptanceEntry, ...],
    *,
    evidence: tuple[a.EvidenceRef, ...] | None = None,
    provenance: tuple[a.EvidenceRef, ...] | None = None,
    currentness: str = a.CURRENT_ACCEPTED,
    authority_ref: a.ContentAddressedRef = a.ACCEPTANCE_AUTHORITY_REF,
) -> a.AcceptanceRegistrySnapshot:
    if evidence is None:
        evidence = tuple(dict.fromkeys(e.source_acceptance_evidence_ref for e in entries))
    if provenance is None:
        provenance = _registry_provenance()
    material = a._registry_material(
        acceptance_authority_ref=authority_ref,
        currentness_state=currentness,
        adoption_current_selection_evidence_refs=evidence,
        immutable_provenance=provenance,
        entries=entries,
    )
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


def _constructed_snapshot(entries: tuple[a.AcceptanceEntry, ...], *, provenance=None):
    evidence = tuple(dict.fromkeys(e.source_acceptance_evidence_ref for e in entries))
    return a._make_registry_snapshot(
        entries,
        currentness_state=a.CURRENT_ACCEPTED,
        adoption_current_selection_evidence_refs=evidence,
        immutable_provenance=_registry_provenance() if provenance is None else provenance,
    )


def _receipt(entry: a.AcceptanceEntry, snapshot: a.AcceptanceRegistrySnapshot):
    return a._issue_for_refs(entry, snapshot.acceptance_authority_ref, snapshot.registry_ref)


def _validate(r: a.AcceptanceReceipt, *, role=None, authority=None, owner=None, source=None, scope=None, currentness=None):
    return a.validate_acceptance_receipt(
        r,
        expected_role=role or r.role,
        expected_accepted_authority_ref=authority or r.accepted_authority_ref,
        expected_owner_jurisdiction_ref=owner or r.accepted_authority_owner_jurisdiction_ref,
        expected_source_acceptance_evidence_ref=source or r.source_acceptance_evidence_ref,
        expected_scope=scope or r.scope,
        required_currentness=currentness or r.currentness_state,
    )


def _git_blob(path: str) -> str:
    data = (ROOT / path).read_bytes()
    return sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def test_01_installed_candidate_current_positive_set_is_empty_and_fails_closed():
    assert a._CURRENT_REGISTRY.currentness_state == a.CANDIDATE_NOT_ADOPTED
    assert a._CURRENT_REGISTRY.entries == ()
    assert a.candidate_registry_artifact()["current_positive_entries"] == []
    e = _entry()
    s = _constructed_snapshot((e,))
    r = _receipt(e, s)
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_02_lawful_future_current_entry_with_nonempty_provenance_remains_representable(monkeypatch):
    e = _entry()
    s = _constructed_snapshot((e,))
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    assert _validate(r, currentness=a.CURRENT_ACCEPTED) == r


def test_03_empty_entry_provenance_rejected_at_constructor():
    e = _entry(provenance=())
    with pytest.raises(a.AcceptanceMissingAuthority, match="entry requires immutable provenance"):
        _constructed_snapshot((e,))


def test_04_empty_entry_provenance_rejected_again_at_validation(monkeypatch):
    e = _entry(provenance=())
    s = _snapshot((e,))
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceMissingAuthority, match="entry lacks immutable provenance"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


@pytest.mark.parametrize(
    "prov",
    [
        (a.EvidenceRef("", ""),),
        (a.EvidenceRef("", "7" * 64),),
        (a.EvidenceRef("urn:h3:placeholder-provenance", ""),),
    ],
)
def test_05_OBSERVATION_nonempty_tuple_with_structurally_empty_provenance_fields_is_accepted(monkeypatch, prov):
    e = _entry(provenance=prov)
    s = _constructed_snapshot((e,))
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    assert r.immutable_provenance == prov
    assert _validate(r, currentness=a.CURRENT_ACCEPTED) == r


def test_06_OBSERVATION_structurally_empty_registry_provenance_element_is_accepted(monkeypatch):
    e = _entry()
    s = _constructed_snapshot((e,), provenance=_registry_provenance(empty_fields=True))
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    assert s.immutable_provenance == (a.EvidenceRef("", ""),)
    assert _validate(r, currentness=a.CURRENT_ACCEPTED) == r


def test_07_entry_provenance_mutation_without_rehash_fails_constructor():
    e = _entry()
    bad = replace(e, immutable_provenance=(a.EvidenceRef("urn:h3:other", "1" * 64),))
    with pytest.raises(a.AcceptanceIntegrityError):
        _constructed_snapshot((bad,))


def test_08_entry_provenance_mutation_with_entry_rehash_but_without_registry_membership_update_fails(monkeypatch):
    original = _entry()
    s = _snapshot((original,))
    mutated = _readdress_entry(replace(original, immutable_provenance=(a.EvidenceRef("urn:h3:other", "1" * 64),)))
    r = _receipt(mutated, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_09_entry_provenance_substitution_in_receipt_rehash_fails_exact_membership(monkeypatch):
    e = _entry()
    s = _snapshot((e,))
    r = _receipt(e, s)
    bad = _readdress_receipt(replace(r, immutable_provenance=(a.EvidenceRef("urn:h3:receipt-substitute", "2" * 64),)))
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(bad, currentness=a.CURRENT_ACCEPTED)


def test_10_missing_registry_provenance_rejected(monkeypatch):
    e = _entry()
    s = _snapshot((e,), provenance=())
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceMissingAuthority, match="registry lacks immutable provenance"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_11_missing_adoption_current_selection_evidence_rejected(monkeypatch):
    e = _entry()
    s = _snapshot((e,), evidence=())
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceMissingAuthority, match="adoption/current-selection"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_12_entry_source_not_selected_by_registry_rejected(monkeypatch):
    e = _entry()
    s = _snapshot((e,), evidence=(a.EvidenceRef("urn:h3:other-selection", "3" * 64),))
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceMissingAuthority, match="not selected"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_13_duplicate_identical_membership_is_ambiguous_and_rejected(monkeypatch):
    e = _entry()
    s = _snapshot((e, e), evidence=(e.source_acceptance_evidence_ref,))
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceMissingAuthority, match="no exact positive registry entry"):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_14_nonmember_current_receipt_rejected(monkeypatch):
    member = _entry(suffix="M")
    attacker = _entry(suffix="X")
    s = _snapshot((member,))
    r = _receipt(attacker, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_15_OBSERVATION_snapshot_with_integrity_invalid_nonmatched_member_can_validate_good_receipt(monkeypatch):
    good = _entry(suffix="GOOD")
    bad0 = _entry(suffix="BAD")
    bad = replace(bad0, consumer="CORRUPTED_NONMATCHED_MEMBER")
    s = _snapshot((good, bad), evidence=(good.source_acceptance_evidence_ref, bad.source_acceptance_evidence_ref))
    r = _receipt(good, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    assert _validate(r, currentness=a.CURRENT_ACCEPTED) == r
    with pytest.raises(a.AcceptanceIntegrityError):
        a._check_entry_integrity(bad)


def test_16_matched_integrity_invalid_member_rejected(monkeypatch):
    e0 = _entry()
    e = replace(e0, consumer="CORRUPTED_MATCHED_MEMBER")
    s = _snapshot((e,))
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_17_OBSERVATION_wrong_entry_schema_id_can_be_admitted_and_validated(monkeypatch):
    e = _entry(schema_id="FOREIGN_ACCEPTANCE_ENTRY_SCHEMA@9.9.9")
    s = _constructed_snapshot((e,))
    r = _receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    assert e.schema_id != a.ENTRY_SCHEMA_ID
    assert _validate(r, currentness=a.CURRENT_ACCEPTED) == r


@pytest.mark.parametrize("axis", ["authority-id", "authority-version", "authority-hash", "role", "consumer", "transition", "family", "subject", "object", "owner", "source", "limits", "currentness", "decision"])
def test_18_exact_receipt_binding_mutations_fail(monkeypatch, axis):
    e = _entry()
    s = _snapshot((e,))
    r = _receipt(e, s)
    if axis == "authority-id":
        bad = replace(r, accepted_authority_ref=replace(r.accepted_authority_ref, id="OTHER"))
    elif axis == "authority-version":
        bad = replace(r, accepted_authority_ref=replace(r.accepted_authority_ref, version="2.0.0"))
    elif axis == "authority-hash":
        bad = replace(r, accepted_authority_ref=replace(r.accepted_authority_ref, content_hash="4" * 64))
    elif axis == "role":
        bad = replace(r, role=a.POSITIVE_APPLICABILITY)
    elif axis == "consumer":
        bad = replace(r, consumer="OTHER_CONSUMER@1.0.0")
    elif axis in {"transition", "family", "subject", "object"}:
        field = {"transition": "transition_use_scope", "family": "family_scope", "subject": "subject_scope", "object": "object_scope"}[axis]
        value = "OTHER:USE" if axis == "transition" else ("OTHER",)
        bad = replace(r, scope=replace(r.scope, **{field: value}))
    elif axis == "owner":
        bad = replace(r, accepted_authority_owner_jurisdiction_ref=a.EvidenceRef("urn:h3:other-owner", "5" * 64))
    elif axis == "source":
        bad = replace(r, source_acceptance_evidence_ref=a.EvidenceRef("urn:h3:other-source", "6" * 64))
    elif axis == "limits":
        bad = replace(r, negative_limit_refs=(a.EvidenceRef("urn:h3:limit", "7" * 64),))
    elif axis == "currentness":
        bad = replace(r, currentness_state=a.NONCURRENT_SYNTHETIC_TEST_ONLY)
    else:
        bad = replace(r, decision_state="REJECT")
    bad = _readdress_receipt(bad)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceAuthorityError):
        _validate(
            bad,
            role=bad.role if axis == "role" else r.role,
            authority=bad.accepted_authority_ref if axis.startswith("authority-") else r.accepted_authority_ref,
            owner=bad.accepted_authority_owner_jurisdiction_ref if axis == "owner" else r.accepted_authority_owner_jurisdiction_ref,
            source=bad.source_acceptance_evidence_ref if axis == "source" else r.source_acceptance_evidence_ref,
            scope=bad.scope if axis in {"transition", "family", "subject", "object"} else r.scope,
            currentness=bad.currentness_state if axis == "currentness" else a.CURRENT_ACCEPTED,
        )


@pytest.mark.parametrize("axis", ["authority-id", "authority-version", "authority-hash", "registry-id", "registry-version", "registry-hash"])
def test_19_registry_or_issuer_substitution_rejected(monkeypatch, axis):
    e = _entry()
    s = _snapshot((e,))
    r = _receipt(e, s)
    if axis.startswith("authority-"):
        field = axis.split("-", 1)[1]
        kwargs = {"id": "OTHER"} if field == "id" else {"version": "2.0.0"} if field == "version" else {"content_hash": "8" * 64}
        bad = replace(s, acceptance_authority_ref=replace(s.acceptance_authority_ref, **kwargs))
    else:
        field = axis.split("-", 1)[1]
        kwargs = {"id": "OTHER"} if field == "id" else {"version": "2.0.0"} if field == "version" else {"content_hash": "9" * 64}
        bad = replace(s, registry_ref=replace(s.registry_ref, **kwargs))
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", bad)
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(r, currentness=a.CURRENT_ACCEPTED)


def test_20_synthetic_to_current_masquerade_rejected():
    r = a.issue_noncurrent_synthetic_test_receipt(a.CAUSAL_USE_PERMISSION)
    bad = _readdress_receipt(replace(r, currentness_state=a.CURRENT_ACCEPTED))
    with pytest.raises(a.AcceptanceAuthorityError):
        _validate(bad, currentness=a.CURRENT_ACCEPTED)


def test_21_current_to_synthetic_substitution_rejected(monkeypatch):
    e = _entry()
    s = _snapshot((e,))
    r = _receipt(e, s)
    bad = _readdress_receipt(replace(r, currentness_state=a.NONCURRENT_SYNTHETIC_TEST_ONLY))
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceAuthorityError):
        _validate(bad, currentness=a.NONCURRENT_SYNTHETIC_TEST_ONLY)


@pytest.mark.parametrize("case", ["forged-occurrence", "forged-independence", "both-forged"])
def test_22_contact_pair_forged_constituents_rejected(case):
    o = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_OCCURRENCE_WITNESS)
    i = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_WITNESS_INDEPENDENCE)
    if case in {"forged-occurrence", "both-forged"}:
        o = _readdress_receipt(replace(o, accepted_authority_ref=a.ContentAddressedRef("NONMEMBER_O", "1", "a" * 64)))
    if case in {"forged-independence", "both-forged"}:
        i = _readdress_receipt(replace(i, accepted_authority_ref=a.ContentAddressedRef("NONMEMBER_I", "1", "b" * 64)))
    with pytest.raises(a.AcceptanceAuthorityError):
        a.validate_contact_acceptance_pair(o, i)


def test_23_contact_same_authority_rejected_after_constituent_validation(monkeypatch):
    o0 = next(e for e in a._SYNTH_ENTRIES if e.role == a.CONTACT_OCCURRENCE_WITNESS)
    i0 = next(e for e in a._SYNTH_ENTRIES if e.role == a.CONTACT_WITNESS_INDEPENDENCE)
    i = _readdress_entry(replace(i0, accepted_authority_ref=o0.accepted_authority_ref))
    entries = tuple(i if e.role == a.CONTACT_WITNESS_INDEPENDENCE else e for e in a._SYNTH_ENTRIES)
    reg = a.ContentAddressedRef(a.REGISTRY_ID + "_SYNTHETIC_TEST", "1.0.0", _digest("SYNTH_REGISTRY", [e.entry_hash for e in entries]))
    monkeypatch.setattr(a, "_SYNTH_ENTRIES", entries)
    monkeypatch.setattr(a, "_SYNTH_REGISTRY_REF", reg)
    o = a._issue_for_refs(o0, a._SYNTH_AUTHORITY_REF, reg)
    ir = a._issue_for_refs(i, a._SYNTH_AUTHORITY_REF, reg)
    assert _validate(o) == o
    assert _validate(ir) == ir
    with pytest.raises(a.AcceptanceOutOfScope, match="distinct accepted authorities"):
        a.validate_contact_acceptance_pair(o, ir)


def test_24_contact_same_receipt_identity_or_cross_role_reuse_rejected():
    o = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_OCCURRENCE_WITNESS)
    i = a.issue_noncurrent_synthetic_test_receipt(a.CONTACT_WITNESS_INDEPENDENCE)
    same_identity = replace(i, receipt_id=o.receipt_id, receipt_hash=o.receipt_hash)
    with pytest.raises(a.AcceptanceIntegrityError):
        a.validate_contact_acceptance_pair(o, same_identity)
    with pytest.raises(a.AcceptanceAuthorityError):
        a.validate_contact_acceptance_pair(o, o)


def test_25_OBSERVATION_current_contact_pair_accepts_role_transition_incoherent_registry_member(monkeypatch):
    wrong_scope = a.AcceptanceScope(
        a._TRANSITION_USE_BY_ROLE[a.CAUSAL_USE_PERMISSION],
        ("H3_CONTACT_FAMILY",),
        ("H3_CONTACT_SUBJECT",),
        ("H3_CONTACT_OBJECT",),
    )
    o = _entry(a.CONTACT_OCCURRENCE_WITNESS, suffix="CO", scope=wrong_scope)
    i = _entry(a.CONTACT_WITNESS_INDEPENDENCE, suffix="CI")
    s = _constructed_snapshot((o, i))
    ro = _receipt(o, s)
    ri = _receipt(i, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    assert ro.scope.transition_use_scope != a._TRANSITION_USE_BY_ROLE[a.CONTACT_OCCURRENCE_WITNESS]
    assert a.validate_contact_acceptance_pair(ro, ri) == (ro, ri)


def test_26_body_mutation_plus_attacker_rehash_does_not_create_membership(monkeypatch):
    e = _entry()
    s = _snapshot((e,))
    r = _receipt(e, s)
    changed_ref = a.ContentAddressedRef("ATTACKER_REHASHED_NONMEMBER", "1.0.0", "c" * 64)
    bad = _readdress_receipt(replace(r, accepted_authority_ref=changed_ref))
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    assert _digest("RECEIPT", _receipt_body(replace(bad, receipt_id="PENDING", receipt_hash="0" * 64))) == bad.receipt_hash
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(bad, authority=changed_ref, currentness=a.CURRENT_ACCEPTED)


def test_27_canonicalization_nfc_key_order_and_replay_are_deterministic():
    left = {"z": "e\u0301", "a": ["x", {"b": 2, "a": 1}]}
    right = {"a": ["x", {"a": 1, "b": 2}], "z": "é"}
    assert _canonical(left) == _canonical(right)
    assert _digest("H3", left) == _digest("H3", right)
    e1 = _entry(suffix="REPLAY")
    e2 = _entry(suffix="REPLAY")
    assert e1 == e2
    s1 = _constructed_snapshot((e1,))
    s2 = _constructed_snapshot((e2,))
    assert s1 == s2
    assert _receipt(e1, s1) == _receipt(e2, s2)


def test_28_authority_and_present_empty_registry_hashes_recompute_exactly():
    authority_material = {
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
    assert _digest("AUTHORITY", authority_material) == EXPECTED_AUTHORITY_HASH == a.ACCEPTANCE_AUTHORITY_CONTENT_HASH
    empty_material = a._registry_material(
        acceptance_authority_ref=a.ACCEPTANCE_AUTHORITY_REF,
        currentness_state=a.CANDIDATE_NOT_ADOPTED,
        adoption_current_selection_evidence_refs=(),
        immutable_provenance=(),
        entries=(),
    )
    assert _digest("REGISTRY", empty_material) == EXPECTED_EMPTY_REGISTRY_HASH == a.REGISTRY_CONTENT_HASH


def test_29_exact_relevant_blobs_are_frozen_and_w2_untouched():
    expected = {
        "rawlsing_next/gt34_adp010_input_authority_acceptance.py": EXPECTED_IMPLEMENTATION_BLOB,
        "rawlsing_next/tests/test_gt34_obl056_current_entry_provenance_bounded_repair.py": EXPECTED_R3_FOCUSED_BLOB,
        R3_DIR + "/01_REPAIRED_AUTHORITY_REGISTRY.json": EXPECTED_R3_REGISTRY_ARTIFACT_BLOB,
        R3_DIR + "/02_REPAIRED_RECEIPT_SCHEMA_AND_CONTRACT_EXAMPLE.json": EXPECTED_R3_RECEIPT_ARTIFACT_BLOB,
        R3_DIR + "/03_PREDECESSOR_TO_REPAIR_COMPATIBILITY.json": EXPECTED_R3_COMPATIBILITY_ARTIFACT_BLOB,
        R3_DIR + "/04_GOVERNED_EVIDENCE.json": EXPECTED_R3_EVIDENCE_BLOB,
        "rawlsing_next/v3_adp010_oee_executor_authenticated.py": EXPECTED_W2_BLOB,
    }
    for path, blob in expected.items():
        assert _git_blob(path) == blob, path


def test_30_contract_and_authority_ceiling_remain_narrow():
    artifact = a.candidate_registry_artifact()
    assert artifact["supported_roles"] == list(a.SUPPORTED_ROLES)
    assert artifact["consumer"] == a.CONSUMER
    assert artifact["positive_fallback"] is False
    assert artifact["generic_project_wide_authority"] is False
    assert artifact["future_current_contract"]["no_latest_default_fuzzy_fallback"] is True
    assert artifact["future_current_contract"]["requires_immutable_entry_provenance"] is True
    required_ceiling = {
        "NO_CAUSAL_USE_SEMANTIC_TRUTH",
        "NO_APPLICABILITY_SEMANTIC_TRUTH",
        "NO_CONTACT_OCCURRENCE",
        "NO_CONTACT_INDEPENDENCE_FACT",
        "NO_ENCOUNTER",
        "NO_EXPOSURE",
        "NO_COMPARATOR",
        "NO_PSEPF",
        "NO_METABOLISM",
        "NO_CAN_008",
        "NO_V2",
        "NO_POSITIVE_V3_ACTOR_MUTATION",
        "NO_GENERIC_PROJECT_WIDE_AUTHORITY_ADMISSION",
    }
    assert required_ceiling <= set(a.AUTHORITY_CEILING)
    sig = inspect.signature(a.validate_acceptance_receipt)
    assert set(sig.parameters) == {
        "r", "expected_role", "expected_accepted_authority_ref", "expected_owner_jurisdiction_ref",
        "expected_source_acceptance_evidence_ref", "expected_scope", "required_currentness",
    }
