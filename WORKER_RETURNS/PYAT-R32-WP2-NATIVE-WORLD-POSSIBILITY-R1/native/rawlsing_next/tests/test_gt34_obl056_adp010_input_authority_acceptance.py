from dataclasses import asdict, replace

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as a


def _good(role):
    return a.issue_noncurrent_synthetic_test_receipt(role)


def _validate(receipt, role=None):
    role = role or receipt.role
    return a.validate_acceptance_receipt(
        receipt,
        expected_role=role,
        expected_accepted_authority_ref=receipt.accepted_authority_ref,
        expected_owner_jurisdiction_ref=receipt.accepted_authority_owner_jurisdiction_ref,
        expected_source_acceptance_evidence_ref=receipt.source_acceptance_evidence_ref,
        expected_scope=receipt.scope,
        required_currentness=receipt.currentness_state,
    )


def _readdress(receipt):
    provisional = replace(receipt, receipt_id="PENDING", receipt_hash="0" * 64)
    h = a._digest("RECEIPT", a._receipt_body(provisional))
    return replace(receipt, receipt_id=f"urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:{h}", receipt_hash=h)


def _mutated_ref(ref, *, id=None, version=None, content_hash=None):
    return a.ContentAddressedRef(id or ref.id, version or ref.version, content_hash or ref.content_hash)


def test_exact_separately_issued_positive_receipt_validates_for_each_role():
    for role in a.SUPPORTED_ROLES:
        receipt = _good(role)
        assert _validate(receipt) == receipt
        assert receipt.currentness_state == a.NONCURRENT_SYNTHETIC_TEST_ONLY


def test_arbitrary_caller_cannot_self_issue_acceptance_even_with_perfect_rehash():
    good = _good(a.CAUSAL_USE_PERMISSION)
    arbitrary = a.ContentAddressedRef("CALLER_SELECTED_FAKE_AUTHORITY", "9.9.9", "1" * 64)
    forged = _readdress(replace(good, accepted_authority_ref=arbitrary))
    with pytest.raises(a.AcceptanceMissingAuthority):
        a.validate_acceptance_receipt(
            forged,
            expected_role=a.CAUSAL_USE_PERMISSION,
            expected_accepted_authority_ref=arbitrary,
            expected_owner_jurisdiction_ref=forged.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=forged.source_acceptance_evidence_ref,
            expected_scope=forged.scope,
            required_currentness=a.NONCURRENT_SYNTHETIC_TEST_ONLY,
        )


@pytest.mark.parametrize("mutation", [
    lambda r: replace(r, accepted_authority_ref=_mutated_ref(r.accepted_authority_ref, id=r.accepted_authority_ref.id + "_MUT")),
    lambda r: replace(r, accepted_authority_ref=_mutated_ref(r.accepted_authority_ref, version="2.0.0")),
    lambda r: replace(r, accepted_authority_ref=_mutated_ref(r.accepted_authority_ref, content_hash="2" * 64)),
], ids=["authority-id", "authority-version", "authority-content-hash"])
def test_accepted_authority_identity_mutation_fails_closed(mutation):
    forged = _readdress(mutation(_good(a.POSITIVE_APPLICABILITY)))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged)


def test_role_mutation_fails_closed_even_with_rehash():
    forged = _readdress(replace(_good(a.CAUSAL_USE_PERMISSION), role=a.POSITIVE_APPLICABILITY))
    with pytest.raises(a.AcceptanceMissingAuthority):
        _validate(forged, role=a.POSITIVE_APPLICABILITY)


def test_consumer_mutation_fails_closed():
    forged = _readdress(replace(_good(a.POSITIVE_APPLICABILITY), consumer="OTHER_CONSUMER@1.0.0"))
    with pytest.raises(a.AcceptanceOutOfScope):
        _validate(forged)


def test_transition_use_scope_mutation_fails_closed():
    good = _good(a.CAUSAL_USE_PERMISSION)
    scope = replace(good.scope, transition_use_scope="AVAILABLE_TO_OPPORTUNITY:WIDENED")
    forged = _readdress(replace(good, scope=scope))
    with pytest.raises(a.AcceptanceMissingAuthority):
        a.validate_acceptance_receipt(forged, expected_role=forged.role,
            expected_accepted_authority_ref=forged.accepted_authority_ref,
            expected_owner_jurisdiction_ref=forged.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=forged.source_acceptance_evidence_ref,
            expected_scope=scope, required_currentness=forged.currentness_state)


def test_source_adoption_current_selection_evidence_mutation_fails_closed():
    good = _good(a.CAUSAL_USE_PERMISSION)
    evidence = a.EvidenceRef(good.source_acceptance_evidence_ref.ref + ":mut", "3" * 64)
    forged = _readdress(replace(good, source_acceptance_evidence_ref=evidence))
    with pytest.raises(a.AcceptanceMissingAuthority):
        a.validate_acceptance_receipt(forged, expected_role=forged.role,
            expected_accepted_authority_ref=forged.accepted_authority_ref,
            expected_owner_jurisdiction_ref=forged.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=evidence,
            expected_scope=forged.scope, required_currentness=forged.currentness_state)


def test_currentness_mutation_and_synthetic_masquerade_fail():
    good = _good(a.POSITIVE_APPLICABILITY)
    forged = _readdress(replace(good, currentness_state=a.CURRENT_ACCEPTED))
    with pytest.raises(a.AcceptanceMissingAuthority):
        a.validate_acceptance_receipt(forged, expected_role=forged.role,
            expected_accepted_authority_ref=forged.accepted_authority_ref,
            expected_owner_jurisdiction_ref=forged.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=forged.source_acceptance_evidence_ref,
            expected_scope=forged.scope, required_currentness=a.CURRENT_ACCEPTED)


def test_receipt_content_hash_mismatch_fails():
    with pytest.raises(a.AcceptanceIntegrityError):
        _validate(replace(_good(a.CAUSAL_USE_PERMISSION), receipt_hash="4" * 64))


def test_absent_receipt_fails_closed():
    good = _good(a.CAUSAL_USE_PERMISSION)
    with pytest.raises(a.AcceptanceMissingAuthority):
        a.validate_acceptance_receipt(None, expected_role=good.role,
            expected_accepted_authority_ref=good.accepted_authority_ref,
            expected_owner_jurisdiction_ref=good.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=good.source_acceptance_evidence_ref,
            expected_scope=good.scope, required_currentness=good.currentness_state)


def test_one_roles_receipt_cannot_satisfy_another_role():
    with pytest.raises(a.AcceptanceOutOfScope):
        _validate(_good(a.CAUSAL_USE_PERMISSION), role=a.POSITIVE_APPLICABILITY)


def test_contact_occurrence_and_independence_require_distinct_authority_identities():
    occurrence = _good(a.CONTACT_OCCURRENCE_WITNESS)
    independence = _good(a.CONTACT_WITNESS_INDEPENDENCE)
    forged = _readdress(replace(independence, accepted_authority_ref=occurrence.accepted_authority_ref))
    with pytest.raises((a.AcceptanceMissingAuthority, a.AcceptanceOutOfScope)):
        a.validate_contact_acceptance_pair(occurrence, forged)


def test_contact_occurrence_and_independence_require_distinct_acceptance_receipts():
    occurrence = _good(a.CONTACT_OCCURRENCE_WITNESS)
    with pytest.raises(a.AcceptanceOutOfScope):
        a.validate_contact_acceptance_pair(occurrence, occurrence)


def test_lawful_contact_pair_is_mechanically_distinct():
    occurrence = _good(a.CONTACT_OCCURRENCE_WITNESS)
    independence = _good(a.CONTACT_WITNESS_INDEPENDENCE)
    assert a.validate_contact_acceptance_pair(occurrence, independence) == (occurrence, independence)
    assert occurrence.accepted_authority_ref != independence.accepted_authority_ref
    assert occurrence.receipt_hash != independence.receipt_hash


def test_exact_replay_is_idempotent():
    for role in a.SUPPORTED_ROLES:
        one = _good(role); two = _good(role)
        assert one == two
        assert one.receipt_id == two.receipt_id
        assert one.receipt_hash == two.receipt_hash


def test_acceptance_receipt_emits_no_underlying_semantic_proposition():
    fields = set(asdict(_good(a.CONTACT_OCCURRENCE_WITNESS)))
    assert fields.isdisjoint({"contact_occurred","contact_independent","causal_use_true","applicable","encounter","exposure","event","actor_mutation"})


def test_candidate_current_registry_is_empty_and_cannot_validate_current_positive():
    artifact = a.candidate_registry_artifact()
    assert artifact["status"] == a.CANDIDATE_NOT_ADOPTED
    assert artifact["current_positive_entries"] == []
    assert artifact["positive_fallback"] is False
    synthetic = _good(a.CAUSAL_USE_PERMISSION)
    with pytest.raises(a.AcceptanceOutOfScope):
        a.validate_acceptance_receipt(synthetic, expected_role=synthetic.role,
            expected_accepted_authority_ref=synthetic.accepted_authority_ref,
            expected_owner_jurisdiction_ref=synthetic.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=synthetic.source_acceptance_evidence_ref,
            expected_scope=synthetic.scope, required_currentness=a.CURRENT_ACCEPTED)


def test_no_implicit_role_widening_or_downstream_authority_widening():
    assert a.SUPPORTED_ROLES == (a.CAUSAL_USE_PERMISSION,a.POSITIVE_APPLICABILITY,a.CONTACT_OCCURRENCE_WITNESS,a.CONTACT_WITNESS_INDEPENDENCE)
    artifact = a.candidate_registry_artifact()
    assert artifact["consumer"] == a.CONSUMER
    assert artifact["generic_project_wide_authority"] is False
    assert {"NO_COMPARATOR","NO_PSEPF","NO_METABOLISM","NO_CAN_008","NO_V2","NO_POSITIVE_V3_ACTOR_MUTATION","NO_GENERIC_PROJECT_WIDE_AUTHORITY_ADMISSION"} <= set(artifact["authority_ceiling"])


def test_receipt_schema_binds_required_authority_registry_role_scope_and_provenance_fields():
    required = set(a.receipt_schema_artifact()["required_fields"])
    assert {"acceptance_authority_ref","registry_ref","registry_entry_ref","role","accepted_authority_ref","accepted_authority_owner_jurisdiction_ref","source_acceptance_evidence_ref","consumer","scope.transition_use_scope","scope.family_scope","scope.subject_scope","scope.object_scope","negative_limit_refs","currentness_state","immutable_provenance","receipt_id","receipt_hash"} <= required
