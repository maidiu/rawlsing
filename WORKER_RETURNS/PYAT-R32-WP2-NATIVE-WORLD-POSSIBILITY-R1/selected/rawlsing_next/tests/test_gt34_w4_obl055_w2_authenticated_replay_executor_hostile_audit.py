"""Independent W4 hostile audit probes for the frozen W2 OBL055 successor.

These probes never admit an OEE record.  They attack the authentication
validators directly, so no current first-canary subject or OEE fact is created.
A green court means the adoption-blocking reproductions are stable.
"""
from hashlib import sha256
import json
import unicodedata

import rawlsing_next.v3_adp010_oee_executor_authenticated as oee


AUTH_DOMAIN = "RAWLSING\0GT34-W2\0AUTHENTICATION_BINDING_V1\0"


def h(tag: str) -> str:
    return sha256(tag.encode("utf-8")).hexdigest()


def ref(kind: str, tag: str) -> oee.ExactRef:
    return oee.ExactRef(kind, f"urn:w4:{tag}", h(tag))


def norm(value):
    if isinstance(value, oee.ExactRef):
        return {
            "kind": value.kind,
            "ref": value.ref,
            "content_hash": value.content_hash,
        }
    if isinstance(value, dict):
        return {str(k): norm(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [norm(v) for v in value]
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    return value


def self_content_ref(kind: str, prefix: str, material) -> oee.ExactRef:
    payload = json.dumps(
        norm(material),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    digest = sha256((AUTH_DOMAIN + payload).encode("utf-8")).hexdigest()
    return oee.ExactRef(kind, prefix + digest, digest)


def self_acceptance_ref(
    kind: str,
    authority_id: str,
    authority_version: str,
    authority_hash: str,
    currentness: str,
) -> oee.ExactRef:
    prefix = f"urn:rawlsing:{kind.lower().replace('_', '-')}:sha256:"
    return self_content_ref(
        kind,
        prefix,
        {
            "authority_id": authority_id,
            "authority_version": authority_version,
            "authority_content_hash": authority_hash,
            "currentness_state": currentness,
        },
    )


def test_current_applicability_validator_accepts_arbitrary_self_issued_authority():
    authority_id = "W4_UNACCEPTED_APPLICABILITY_AUTHORITY"
    authority_version = "999.0"
    authority_hash = h("unaccepted-applicability-authority")
    receipt = ref("POSITIVE_APPLICABILITY_RECEIPT", "app-receipt")
    provenance = (ref("PROVENANCE", "app-provenance"),)
    acceptance = self_acceptance_ref(
        "ACCEPTED_APPLICABILITY_AUTHORITY_RECEIPT",
        authority_id,
        authority_version,
        authority_hash,
        oee.CURRENT_ACCEPTED,
    )
    material = {
        "receipt": receipt,
        "authority": [authority_id, authority_version, authority_hash],
        "authority_acceptance_ref": acceptance,
        "result": "POSITIVE",
        "provenance_refs": provenance,
        "currentness_state": oee.CURRENT_ACCEPTED,
    }
    authentication = self_content_ref(
        "POSITIVE_APPLICABILITY_AUTHENTICATION",
        "urn:rawlsing:positive-applicability-authentication:sha256:",
        material,
    )
    attack = oee.PositiveApplicabilityReceipt(
        receipt=receipt,
        authority_id=authority_id,
        authority_version=authority_version,
        authority_content_hash=authority_hash,
        authority_acceptance_ref=acceptance,
        result="POSITIVE",
        provenance_refs=provenance,
        authentication_ref=authentication,
        currentness_state=oee.CURRENT_ACCEPTED,
    )

    accepted_receipt, accepted_auth = oee._validate_app(
        attack, oee.CURRENT_ACCEPTED
    )
    assert accepted_receipt == receipt
    assert accepted_auth == authentication


def test_current_causal_use_validator_accepts_arbitrary_self_issued_authority():
    authority_id = "W4_UNACCEPTED_CAUSAL_USE_AUTHORITY"
    authority_version = "31337"
    authority_hash = h("unaccepted-causal-use-authority")
    subject_ref = "urn:w4:not-current-first-canary:subject"
    semantic_object = ref("W4_SYNTHETIC_OBJECT", "object")
    materialization = ref("SUBJECT_MATERIALIZATION_RECEIPT", "materialization")
    permission_ref = ref("CAUSAL_USE_PERMISSION", "causal-use")
    provenance = (ref("PROVENANCE", "causal-provenance"),)
    acceptance = self_acceptance_ref(
        "ACCEPTED_CAUSAL_USE_AUTHORITY_RECEIPT",
        authority_id,
        authority_version,
        authority_hash,
        oee.CURRENT_ACCEPTED,
    )
    material = {
        "permission_ref": permission_ref,
        "authority": [authority_id, authority_version, authority_hash],
        "authority_acceptance_ref": acceptance,
        "subject_ref": subject_ref,
        "semantic_object_ref": semantic_object,
        "materialization_receipt_ref": materialization,
        "scope": "ADP010_CAUSAL_USE",
        "provenance_refs": provenance,
        "currentness_state": oee.CURRENT_ACCEPTED,
    }
    authentication = self_content_ref(
        "CAUSAL_USE_PERMISSION_AUTHENTICATION",
        "urn:rawlsing:causal-use-authentication:sha256:",
        material,
    )
    attack = oee.CausalUsePermission(
        permission_ref=permission_ref,
        authority_id=authority_id,
        authority_version=authority_version,
        authority_content_hash=authority_hash,
        authority_acceptance_ref=acceptance,
        subject_ref=subject_ref,
        semantic_object_ref=semantic_object,
        materialization_receipt_ref=materialization,
        scope="ADP010_CAUSAL_USE",
        provenance_refs=provenance,
        authentication_ref=authentication,
        currentness_state=oee.CURRENT_ACCEPTED,
    )

    assert (
        oee._validate_permission(
            attack,
            subject_ref,
            semantic_object,
            materialization,
            oee.CURRENT_ACCEPTED,
        )
        == attack
    )


def test_current_contact_independence_accepts_one_arbitrary_self_issued_authority_for_both_roles():
    authority_id = "W4_UNACCEPTED_CONTACT_AND_INDEPENDENCE_AUTHORITY"
    authority_version = "0.0-unaccepted"
    authority_hash = h("same-unaccepted-contact-independence-authority")
    actor_id = "urn:w4:actor:synthetic"
    subject_ref = "urn:w4:not-current-first-canary:subject"
    occurrence_time = "2031-01-01T12:00:00.000000Z"
    witness_ref = ref(oee.CONTACT_WITNESS_KIND, "contact-witness")
    independence_ref = ref(oee.CONTACT_INDEPENDENCE_KIND, "independence")
    independence_receipt = ref(
        "CONTACT_WITNESS_INDEPENDENCE_RECEIPT", "independence-receipt"
    )
    contact_basis = (ref("DIRECT_CONTACT_OBSERVATION", "contact-basis"),)
    independence_basis = (ref("INDEPENDENT_OBSERVER_CHAIN", "independence-basis"),)
    provenance = (ref("PROVENANCE", "contact-provenance"),)

    witness_acceptance = self_acceptance_ref(
        "ACCEPTED_CONTACT_OCCURRENCE_AUTHORITY_RECEIPT",
        authority_id,
        authority_version,
        authority_hash,
        oee.CURRENT_ACCEPTED,
    )
    independence_acceptance = self_acceptance_ref(
        "ACCEPTED_CONTACT_INDEPENDENCE_AUTHORITY_RECEIPT",
        authority_id,
        authority_version,
        authority_hash,
        oee.CURRENT_ACCEPTED,
    )

    contact_material = {
        "witness_ref": witness_ref,
        "witness_authority": [authority_id, authority_version, authority_hash],
        "witness_authority_acceptance_ref": witness_acceptance,
        "actor_id": actor_id,
        "subject_ref": subject_ref,
        "occurrence_time": occurrence_time,
        "semantic": oee.CONTACT_OCCURRENCE_SEMANTIC,
        "contact_basis_refs": contact_basis,
        "provenance_refs": provenance,
        "currentness_state": oee.CURRENT_ACCEPTED,
    }
    contact_auth = self_content_ref(
        "CONTACT_OCCURRENCE_AUTHENTICATION",
        "urn:rawlsing:contact-occurrence-authentication:sha256:",
        contact_material,
    )
    independence_material = {
        "contact_authentication_ref": contact_auth,
        "independence_ref": independence_ref,
        "independence_authority": [authority_id, authority_version, authority_hash],
        "independence_authority_acceptance_ref": independence_acceptance,
        "independence_receipt_ref": independence_receipt,
        "independence_basis_refs": independence_basis,
        "currentness_state": oee.CURRENT_ACCEPTED,
    }
    independence_auth = self_content_ref(
        "CONTACT_INDEPENDENCE_AUTHENTICATION",
        "urn:rawlsing:contact-independence-authentication:sha256:",
        independence_material,
    )
    attack = oee.ContactOccurrenceWitness(
        witness_ref=witness_ref,
        witness_authority_id=authority_id,
        witness_authority_version=authority_version,
        witness_authority_content_hash=authority_hash,
        witness_authority_acceptance_ref=witness_acceptance,
        actor_id=actor_id,
        subject_ref=subject_ref,
        occurrence_time=occurrence_time,
        semantic=oee.CONTACT_OCCURRENCE_SEMANTIC,
        contact_basis_refs=contact_basis,
        contact_authentication_ref=contact_auth,
        independence_ref=independence_ref,
        independence_authority_id=authority_id,
        independence_authority_version=authority_version,
        independence_authority_content_hash=authority_hash,
        independence_authority_acceptance_ref=independence_acceptance,
        independence_receipt_ref=independence_receipt,
        independence_basis_refs=independence_basis,
        independence_authentication_ref=independence_auth,
        provenance_refs=provenance,
        currentness_state=oee.CURRENT_ACCEPTED,
    )

    validated, got_contact_auth, got_independence_auth = oee._validate_contact(
        attack,
        actor_id,
        subject_ref,
        occurrence_time,
        oee.CURRENT_ACCEPTED,
    )
    assert validated == attack
    assert got_contact_auth == contact_auth
    assert got_independence_auth == independence_auth
