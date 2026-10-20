"""PA0 scope-honest smoke consumer over ACTUAL runnable producer code.

Two independent invocations at this checkout:

A. CURRENT_ACCEPTED nonactor subject materialization
   rawlsing_next.gt34_u2_v3p1_authenticated_subject_materializer
   Reconstructs the exact adopted OBL053 semantic-object bytes from the in-repo
   adoption artifact preimage (content-addressing law: SHA256(canonical JSON)),
   then materializes the one-object subject receipt under the adopted OBL054
   root/permit. This is a REAL current nonactor subject producer, NOT a person.

B. NONCURRENT SYNTHETIC TEST ONLY ADP-010 OEE chain
   rawlsing_next.v3_adp010_oee_executor_authenticated
   AVAILABLE -> OPPORTUNITY -> ENCOUNTER through the module's own synthetic
   noncurrent helpers. This is real executor code with test-only evidence; it is
   not a native actor event and not a person.

Each invocation carries a source-edge severance control: the same positive
result must be absent and a typed refusal raised when the exact source edge is
changed. No file outside this return is modified.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

import rawlsing_next.gt34_u2_v3p1_authenticated_subject_materializer as u2
import rawlsing_next.v3_adp010_oee_executor_authenticated as oee

OBL053_ARTIFACT_BLOB = "14ff405cfb77ccfe30adbce16e9c0ff14fa540f9"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def ref(kind, tag):
    h = hashlib.sha256(tag.encode()).hexdigest()
    return oee.ExactRef(kind, f"urn:pa0:test:{tag}", h)


def git_blob_hex(path):
    return subprocess.run(
        ["git", "hash-object", str(path)], cwd=str(REPO), capture_output=True, text=True, check=True
    ).stdout.strip()


def module_receipt(module):
    path = Path(module.__file__)
    raw = path.read_bytes()
    return {
        "module": module.__name__,
        "file": str(path.relative_to(REPO)),
        "git_blob": git_blob_hex(path),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def adopted_semantic_bytes():
    raw = subprocess.run(
        ["git", "cat-file", "-p", OBL053_ARTIFACT_BLOB],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    artifact = json.loads(raw)
    projection = artifact["prospective_semantic_object"]["semantic_projection"]
    data = canonical(projection)
    digest = hashlib.sha256(data).hexdigest()
    return artifact, data, digest, raw


def subject_materialization():
    root = u2.CURRENT_ACCEPTED_OWNER_ROOT
    artifact, object_bytes, object_digest, artifact_raw = adopted_semantic_bytes()
    assert object_digest == root.semantic_object_ref.sha256, "adopted preimage hash mismatch"
    binding = u2.compute_owner_binding_content_hash(
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=root.semantic_object_ref,
        semantic_object_bytes=object_bytes,
        evidence_refs=root.evidence_refs,
        provenance_refs=root.provenance_refs,
    )
    material = u2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=root.semantic_object_ref,
        semantic_object_bytes=object_bytes,
        evidence_refs=root.evidence_refs,
        provenance_refs=root.provenance_refs,
        owner_binding_content_hash=binding,
    )
    receipt = u2.materialize_owner_bound_subject(
        material, u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT
    )
    positives = {
        "integrity_state": receipt.integrity_state,
        "subject_ref": receipt.subject_ref,
        "subject_ref_hash": receipt.subject_ref_hash,
        "receipt_id": receipt.receipt_id,
        "receipt_hash": receipt.receipt_hash,
        "adoption_artifact_blob": receipt.adoption_artifact_blob,
        "accepted_owner_root_hash": receipt.accepted_owner_root_hash,
        "materialization_permit_hash": receipt.materialization_permit_hash,
        "semantic_object_ref": receipt.semantic_object_ref.as_dict(),
        "semantic_object_bytes_sha256": object_digest,
        "semantic_object_bytes_len": len(object_bytes),
        "semantic_owner_transfer": receipt.semantic_owner_transfer,
        "semantic_fields_interpreted": receipt.semantic_fields_interpreted,
        "adoption_artifact_blob_content_sha256": hashlib.sha256(artifact_raw.encode()).hexdigest(),
        "semantic_object_facts": artifact["prospective_semantic_object"]["semantic_projection"][
            "objective_entity_facts"
        ],
        "scope": "CURRENT_ACCEPTED_NONACTOR_SUBJECT__NOT_A_PERSON",
    }
    severances = []

    defect_bytes = object_bytes + b" "
    try:
        u2.compute_owner_binding_content_hash(
            semantic_owner_authority_id=root.semantic_owner_authority_id,
            semantic_owner_authority_version=root.semantic_owner_authority_version,
            semantic_owner_authority_hash=root.semantic_owner_authority_hash,
            semantic_object_ref=root.semantic_object_ref,
            semantic_object_bytes=defect_bytes,
            evidence_refs=root.evidence_refs,
            provenance_refs=root.provenance_refs,
        )
        defect_result = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001 - typed refusal evidence
        defect_result = type(exc).__name__ + ": " + str(exc)
    severances.append(
        {
            "edge": "semantic_object_bytes",
            "mutation": "append one byte while keeping the adopted object ref",
            "expected": "typed refusal, no receipt",
            "observed": defect_result,
            "positive_absent": defect_result != "NO_REFUSAL",
        }
    )

    wrong_owner = replace(material, semantic_owner_authority_id="PA0_FORGED_OWNER")
    try:
        u2.materialize_owner_bound_subject(
            wrong_owner, u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT
        )
        owner_result = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        owner_result = type(exc).__name__ + ": " + str(exc)
    severances.append(
        {
            "edge": "semantic_owner_authority_id",
            "mutation": "replace owner id with PA0_FORGED_OWNER",
            "expected": "AcceptedOwnerAuthenticationError",
            "observed": owner_result,
            "positive_absent": owner_result != "NO_REFUSAL",
        }
    )

    historical = u2._build_permit(
        replace(
            root,
            adoption_artifact_blob=u2.HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB,
        )
    )
    try:
        u2.materialize_owner_bound_subject(material, historical)
        historical_result = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        historical_result = type(exc).__name__ + ": " + str(exc)
    severances.append(
        {
            "edge": "adopted_root_currentness",
            "mutation": "use the historical invalid OBL053 adoption blob",
            "expected": "MaterializationPermitError",
            "observed": historical_result,
            "positive_absent": historical_result != "NO_REFUSAL",
        }
    )

    return {
        "invocation": "A",
        "producer": "rawlsing_next.gt34_u2_v3p1_authenticated_subject_materializer.materialize_owner_bound_subject",
        "module": module_receipt(u2),
        "positive": positives,
        "severances": severances,
        "all_severed": all(s["positive_absent"] for s in severances),
    }


def adp010_chain():
    from hashlib import sha256

    def r(kind, tag):
        h = sha256(tag.encode()).hexdigest()
        return oee.ExactRef(kind, f"urn:w2:test:{tag}", h)

    subject = oee._synthetic_subject()
    actor = oee._synthetic_actor()
    av = oee._admit_available_noncurrent_for_test(
        subject=subject,
        actor=actor,
        effective_from="2031-01-01T00:00:00Z",
        effective_until="2031-01-02T00:00:00Z",
        time_granularity="INTERVAL",
        context_or_world_receipt_refs=(r("WORLD_RECEIPT", "world"), r("CONTEXT_RECEIPT", "ctx")),
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l0"),
        provenance_refs=(r("PROVENANCE", "av"),),
    )
    op = oee._admit_opportunity_noncurrent_for_test(
        parent_available=av.record,
        subject=subject,
        actor=actor,
        opportunity_basis=oee._synthetic_basis(subject, actor),
        effective_from="2031-01-01T08:00:00Z",
        effective_until="2031-01-01T18:00:00Z",
        time_granularity="INTERVAL",
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l1"),
        provenance_refs=(r("PROVENANCE", "op"),),
    )
    en = oee._admit_encounter_noncurrent_for_test(
        parent_opportunity=op.record,
        subject=subject,
        actor=actor,
        contact_witness=oee._synthetic_contact(subject, actor),
        effective_time="2031-01-01T12:00:00Z",
        time_granularity="INSTANT",
        prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2"),
        declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre"),),
        provenance_refs=(r("PROVENANCE", "en"),),
    )
    chain = oee.validate_basis_available_opportunity_encounter_chain(
        (av.record, op.record, en.record)
    )
    positives = {
        "states": [x.realization_state for x in chain],
        "effect_kinds": [x.event_effect_kind for x in chain],
        "subject_refs": sorted({x.subject_ref for x in chain}),
        "actor_ids": sorted({x.actor_id for x in chain}),
        "authority": {
            "id": av.record.authority_id,
            "version": av.record.authority_version,
            "registry": av.record.registry_id,
        },
        "record_hashes": [x.record_hash for x in chain],
        "source_candidate_replay_hashes": [x.source_candidate_replay_hash for x in chain],
        "encounter_event_id": en.record.event_id,
        "scope": "NONCURRENT_SYNTHETIC_TEST_ONLY__NOT_NATIVE_ADP010__NOT_A_PERSON",
    }
    severances = []

    try:
        oee._admit_encounter_noncurrent_for_test(
            parent_opportunity=op.record,
            subject=subject,
            actor=actor,
            contact_witness=oee._synthetic_contact(subject, actor, semantic="COLOCATION"),
            effective_time="2031-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2"),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre"),),
            provenance_refs=(r("PROVENANCE", "en"),),
        )
        colocation = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        colocation = type(exc).__name__ + ": " + str(exc)
    severances.append(
        {
            "edge": "contact_occurrence_semantic",
            "mutation": "replace CONTACT_OCCURRENCE with COLOCATION",
            "expected": "typed refusal, no ENCOUNTER",
            "observed": colocation,
            "positive_absent": colocation != "NO_REFUSAL",
        }
    )

    try:
        oee._admit_encounter_noncurrent_for_test(
            parent_opportunity=av.record,
            subject=subject,
            actor=actor,
            contact_witness=oee._synthetic_contact(subject, actor),
            effective_time="2031-01-01T12:00:00Z",
            time_granularity="INSTANT",
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l2"),
            declared_precondition_refs=(r("DECLARED_PRECONDITION", "pre"),),
            provenance_refs=(r("PROVENANCE", "en"),),
        )
        wrong_parent = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        wrong_parent = type(exc).__name__ + ": " + str(exc)
    severances.append(
        {
            "edge": "parent_opportunity_record",
            "mutation": "pass the AVAILABLE record as the OPPORTUNITY parent",
            "expected": "typed refusal",
            "observed": wrong_parent,
            "positive_absent": wrong_parent != "NO_REFUSAL",
        }
    )

    try:
        oee.admit_available(
            subject=subject,
            actor=actor,
            effective_from="2031-01-01T00:00:00Z",
            effective_until="2031-01-02T00:00:00Z",
            time_granularity="INTERVAL",
            context_or_world_receipt_refs=(r("WORLD_RECEIPT", "world"),),
            prior_ledger_anchor_ref=r("LEDGER_ANCHOR", "l0"),
            provenance_refs=(r("PROVENANCE", "av"),),
        )
        production_current = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        production_current = type(exc).__name__ + ": " + str(exc)
    severances.append(
        {
            "edge": "production CURRENT_ACCEPTED executor",
            "mutation": "present NONCURRENT synthetic subject/actor to the installed production executor",
            "expected": "typed currentness refusal",
            "observed": production_current,
            "positive_absent": production_current != "NO_REFUSAL",
        }
    )

    return {
        "invocation": "B",
        "producer": "rawlsing_next.v3_adp010_oee_executor_authenticated._admit_*_noncurrent_for_test",
        "module": module_receipt(oee),
        "positive": positives,
        "severances": severances,
        "all_severed": all(s["positive_absent"] for s in severances),
    }


def main():
    out = {
        "schema": "SOROK_PA0_SMOKE@1",
        "checkout": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=str(REPO), capture_output=True, text=True, check=True
        ).stdout.strip(),
        "python": sys.version.split()[0],
        "invocations": [subject_materialization(), adp010_chain()],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
