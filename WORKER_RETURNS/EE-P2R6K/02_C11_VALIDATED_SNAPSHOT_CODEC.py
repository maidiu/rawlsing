#!/usr/bin/env python3
"""Deterministic full-body C11 validated-candidate snapshot codec for EE-P2R6K."""
from __future__ import annotations

from dataclasses import fields
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    CanonicalSemanticObject,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
    SourceUniverseRelation,
    WeightMeasureFact,
    authority_ref,
    canonical_json,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_c11_integrity import (
    C11InternalRecord,
    ComparatorReplayBinding,
    DiscoveryBranchReplayBinding,
    EmpiricalPredicateReplayBinding,
    QuestionVariableBinding,
    ReplayManifest,
    RespondentIdentity,
    StructuralAdmissionReplayBinding,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_ingest import (
    C11SourceReleaseCandidate,
    SourceReleaseManifest,
    record_counts_for_candidate,
)
from rawlsing_next.pre553_c11_repository import C11Repository

SNAPSHOT_SCHEMA = "EE_P2R6K_C11_VALIDATED_CANDIDATE_SNAPSHOT@1.0.0"
SNAPSHOT_ENCODING = "UTF8_CANONICAL_JSON_SORT_KEYS_COMPACT_TRAILING_LF"
SOURCE_MANIFEST_FAMILY = "SourceReleaseManifest@PRE553_C11_INGEST@1.0.0"
TYPED_ABSENCE_FAMILY = "TypedAbsence@1.0.0"

PUBLIC_CLASSES = {
    "EmpiricalUniverse@1.0.0": EmpiricalUniverse,
    "RespondentEvent@1.0.0": RespondentEvent,
    "RoutingEligibilityFact@1.0.0": RoutingEligibilityFact,
    "EmpiricalCoordinateFact@1.0.0": EmpiricalCoordinateFact,
    "WeightMeasureFact@1.0.0": WeightMeasureFact,
    "AuthoritySnapshot@1.0.0": AuthoritySnapshot,
    "SourceUniverseRelation@1.0.0": SourceUniverseRelation,
}
INTERNAL_CLASSES = {
    "RespondentIdentity": RespondentIdentity,
    "QuestionVariableBinding": QuestionVariableBinding,
    "EmpiricalPredicateReplayBinding": EmpiricalPredicateReplayBinding,
    "ComparatorReplayBinding": ComparatorReplayBinding,
    "DiscoveryBranchReplayBinding": DiscoveryBranchReplayBinding,
    "StructuralAdmissionReplayBinding": StructuralAdmissionReplayBinding,
    "ReplayManifest": ReplayManifest,
}

SECTION_SPECS = {
    "empirical_universes": ("EmpiricalUniverse@1.0.0", False),
    "respondent_identities": ("RespondentIdentity", False),
    "question_variable_bindings": ("QuestionVariableBinding", False),
    "respondent_events": ("RespondentEvent@1.0.0", False),
    "routing_eligibility_facts_or_exact_rules": ("RoutingEligibilityFact@1.0.0", False),
    "empirical_coordinate_facts": ("EmpiricalCoordinateFact@1.0.0", False),
    "weight_measure_facts_or_typed_absence": ("WeightMeasureFact@1.0.0", True),
    "authority_snapshots": ("AuthoritySnapshot@1.0.0", False),
    "source_universe_relations_or_explicit_distinct_default": ("SourceUniverseRelation@1.0.0", True),
    "predicate_replay_bindings_when_retained_objects_require_them": ("EmpiricalPredicateReplayBinding", True),
    "comparator_replay_bindings_or_typed_deferred_state": ("ComparatorReplayBinding", True),
    "discovery_branch_replay_bindings_or_typed_deferred_state": ("DiscoveryBranchReplayBinding", True),
    "structural_admission_replay_bindings_or_typed_not_applicable_state": ("StructuralAdmissionReplayBinding", True),
}


class SnapshotCodecError(ValueError):
    pass


def _require_exact_keys(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    got = set(value)
    if got != expected:
        raise SnapshotCodecError(f"{label} keys differ: missing={sorted(expected-got)!r} extra={sorted(got-expected)!r}")


def _canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def canonical_snapshot_bytes(snapshot: Mapping[str, Any]) -> bytes:
    return _canonical_bytes(snapshot)


def _record_ref_dict(record: Any) -> dict[str, str]:
    if not hasattr(record, "ref"):
        raise SnapshotCodecError("identity-bearing record lacks exact ref")
    return record.ref.as_dict()


def _serialize_record(record: Any) -> dict[str, Any]:
    if isinstance(record, CanonicalSemanticObject):
        family = record.family
        body = record.as_dict()
    elif isinstance(record, C11InternalRecord):
        family = record.RECORD_FAMILY
        body = record.as_dict()
    else:
        raise SnapshotCodecError(f"unsupported record type {type(record).__name__}")
    return {
        "record_family": family,
        "exact_ref": _record_ref_dict(record),
        "canonical_body": body,
        "canonical_body_sha256": hashlib.sha256(_canonical_bytes(body)).hexdigest(),
    }


def _serialize_absence(value: TypedAbsence) -> dict[str, Any]:
    body = value.as_dict()
    return {
        "record_family": TYPED_ABSENCE_FAMILY,
        "canonical_body": body,
        "semantic_body_hash": semantic_hash(body),
    }


def _serialize_manifest(manifest: SourceReleaseManifest) -> dict[str, Any]:
    body = manifest.semantic_projection()
    return {
        "record_family": SOURCE_MANIFEST_FAMILY,
        "canonical_body": body,
        "content_hash": manifest.content_hash,
        "canonical_body_sha256": hashlib.sha256(_canonical_bytes(body)).hexdigest(),
    }


def _serialize_section(value: Any, family: str, absence_allowed: bool) -> dict[str, Any]:
    if isinstance(value, TypedAbsence):
        if not absence_allowed:
            raise SnapshotCodecError(f"{family} section cannot be typed absence")
        return {
            "representation": "TYPED_ABSENCE",
            "record_family": family,
            "value": _serialize_absence(value),
        }
    if not isinstance(value, tuple):
        raise SnapshotCodecError(f"{family} section must be immutable tuple")
    records = sorted(value, key=lambda item: item.ref.key)
    return {
        "representation": "SEQUENCE",
        "record_family": family,
        "records": [_serialize_record(item) for item in records],
    }


def serialize_candidate(candidate: C11SourceReleaseCandidate, validated_release: Any) -> dict[str, Any]:
    if not isinstance(candidate, C11SourceReleaseCandidate):
        raise SnapshotCodecError("expected C11SourceReleaseCandidate")
    if candidate.candidate_replay_manifest is None:
        raise SnapshotCodecError("candidate replay manifest is required")
    if validated_release.replay_manifest.ref != candidate.candidate_replay_manifest.ref:
        raise SnapshotCodecError("validated release replay manifest differs from candidate")
    if validated_release.source_release_manifest_hash != candidate.source_release_manifest.content_hash:
        raise SnapshotCodecError("validated release source manifest hash differs from candidate")

    sections = {
        name: _serialize_section(getattr(candidate, name), family, absence_allowed)
        for name, (family, absence_allowed) in SECTION_SPECS.items()
    }
    counts = dict(record_counts_for_candidate(candidate))
    repository = C11Repository((validated_release,))
    release_identity = {
        "release_ref": validated_release.release_ref.as_dict(),
        "source_artifact_ref": validated_release.source_artifact_ref.as_dict(),
        "source_release_manifest_hash": validated_release.source_release_manifest_hash,
        "semantic_release_hash": validated_release.semantic_release_hash,
        "replay_manifest_ref": validated_release.replay_manifest.ref.as_dict(),
        "m01_m18_coverage": {key: list(value) for key, value in validated_release.m01_m18_coverage.items()},
        "repository_snapshot_identity": repository.snapshot_identity(),
    }
    return {
        "schema": SNAPSHOT_SCHEMA,
        "encoding": SNAPSHOT_ENCODING,
        "semantic_boundary": "EVIDENCE_TRANSPORT_OF_ALREADY_GOVERNED_CANONICAL_C11_CANDIDATE_BODIES__NO_NEW_SEMANTIC_IDENTITY",
        "source_release_manifest": _serialize_manifest(candidate.source_release_manifest),
        "sections": sections,
        "candidate_replay_manifest": _serialize_record(candidate.candidate_replay_manifest),
        "identity_summary": {
            "source_release_manifest_hash": candidate.source_release_manifest.content_hash,
            "candidate_projection_hash": candidate.candidate_replay_manifest.semantic_projection_hash,
            "replay_manifest_ref": candidate.candidate_replay_manifest.ref.as_dict(),
            "record_counts": counts,
        },
        "validated_release_identity": release_identity,
    }


def serialize_snapshot_bytes(candidate: C11SourceReleaseCandidate, validated_release: Any) -> bytes:
    return canonical_snapshot_bytes(serialize_candidate(candidate, validated_release))


def write_snapshot(candidate: C11SourceReleaseCandidate, validated_release: Any, path: Path) -> dict[str, Any]:
    payload = serialize_candidate(candidate, validated_release)
    data = canonical_snapshot_bytes(payload)
    Path(path).write_bytes(data)
    return {
        "path": str(path),
        "byte_length": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def parse_snapshot_bytes(data: bytes) -> dict[str, Any]:
    if not isinstance(data, (bytes, bytearray)):
        raise SnapshotCodecError("snapshot input must be bytes")
    try:
        decoded = json.loads(bytes(data).decode("utf-8"))
    except Exception as exc:
        raise SnapshotCodecError("snapshot is not valid UTF-8 JSON") from exc
    if not isinstance(decoded, dict):
        raise SnapshotCodecError("snapshot root must be an object")
    if canonical_snapshot_bytes(decoded) != bytes(data):
        raise SnapshotCodecError("snapshot bytes are not exact canonical encoding")
    return decoded


def _decode_value(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(_decode_value(item) for item in value)
    if isinstance(value, dict):
        keys = set(value)
        if keys == {"kind", "object_id", "content_hash"}:
            return exact_ref(value)
        if keys == {"authority_id", "authority_version", "authority_content_hash"}:
            return authority_ref(value)
        if keys == {"typed_absence_state", "detail"}:
            return TypedAbsence(value["typed_absence_state"], value["detail"])
        return {key: _decode_value(item) for key, item in value.items()}
    return value


def _verify_body_sha(wrapper: Mapping[str, Any]) -> None:
    body = wrapper["canonical_body"]
    observed = hashlib.sha256(_canonical_bytes(body)).hexdigest()
    if wrapper.get("canonical_body_sha256") != observed:
        raise SnapshotCodecError("canonical body byte hash mismatch")


def _decode_public(wrapper: Mapping[str, Any], expected_family: str) -> CanonicalSemanticObject:
    _require_exact_keys(wrapper, {"record_family", "exact_ref", "canonical_body", "canonical_body_sha256"}, "public record")
    if wrapper["record_family"] != expected_family:
        raise SnapshotCodecError("public record family mismatch")
    cls = PUBLIC_CLASSES.get(expected_family)
    if cls is None:
        raise SnapshotCodecError(f"unsupported public family {expected_family}")
    _verify_body_sha(wrapper)
    body = wrapper["canonical_body"]
    if not isinstance(body, dict):
        raise SnapshotCodecError("public canonical body must be object")
    required = {
        "schema_id", "schema_version", "typed_state", "authority_snapshot_refs",
        "dependency_refs", "producer_replay_locator_or_reference_root", "semantic_fields",
        "object_id", "content_hash",
    }
    _require_exact_keys(body, required, "public canonical body")
    semantic_fields = _decode_value(body["semantic_fields"])
    if not isinstance(semantic_fields, dict):
        raise SnapshotCodecError("public semantic_fields must be object")
    obj = cls(
        typed_state=body["typed_state"],
        authority_snapshot_refs=tuple(authority_ref(x) for x in body["authority_snapshot_refs"]),
        dependency_refs=tuple(exact_ref(x) for x in body["dependency_refs"]),
        producer_replay_locator_or_reference_root=_decode_value(body["producer_replay_locator_or_reference_root"]),
        object_id=body["object_id"],
        content_hash=body["content_hash"],
        schema_id=body["schema_id"],
        schema_version=body["schema_version"],
        **semantic_fields,
    )
    expected_ref = exact_ref(wrapper["exact_ref"])
    if obj.ref != expected_ref:
        raise SnapshotCodecError("public object exact ref did not recompute")
    if canonical_json(obj.as_dict()) != canonical_json(body):
        raise SnapshotCodecError("public object canonical body did not reconstruct exactly")
    return obj


def _decode_internal(wrapper: Mapping[str, Any], expected_family: str) -> C11InternalRecord:
    _require_exact_keys(wrapper, {"record_family", "exact_ref", "canonical_body", "canonical_body_sha256"}, "internal record")
    if wrapper["record_family"] != expected_family:
        raise SnapshotCodecError("internal record family mismatch")
    cls = INTERNAL_CLASSES.get(expected_family)
    if cls is None:
        raise SnapshotCodecError(f"unsupported internal family {expected_family}")
    _verify_body_sha(wrapper)
    body = wrapper["canonical_body"]
    if not isinstance(body, dict):
        raise SnapshotCodecError("internal canonical body must be object")
    _require_exact_keys(body, {"record_family", "record_version", "semantic_fields", "object_id", "content_hash"}, "internal canonical body")
    if body["record_family"] != expected_family or body["record_version"] != "1.0.0":
        raise SnapshotCodecError("internal record family/version mismatch")
    raw_fields = body["semantic_fields"]
    if not isinstance(raw_fields, dict):
        raise SnapshotCodecError("internal semantic_fields must be object")
    expected_field_names = {item.name for item in fields(cls)}
    if set(raw_fields) != expected_field_names:
        raise SnapshotCodecError("internal semantic field set differs from constructor")
    obj = cls(**{name: _decode_value(raw_fields[name]) for name in raw_fields})
    expected_ref = exact_ref(wrapper["exact_ref"])
    if obj.ref != expected_ref:
        raise SnapshotCodecError("internal record exact ref did not recompute")
    if canonical_json(obj.as_dict()) != canonical_json(body):
        raise SnapshotCodecError("internal record canonical body did not reconstruct exactly")
    return obj


def _decode_record(wrapper: Mapping[str, Any], family: str) -> Any:
    if family in PUBLIC_CLASSES:
        return _decode_public(wrapper, family)
    return _decode_internal(wrapper, family)


def _decode_absence(wrapper: Mapping[str, Any]) -> TypedAbsence:
    _require_exact_keys(wrapper, {"record_family", "canonical_body", "semantic_body_hash"}, "typed absence")
    if wrapper["record_family"] != TYPED_ABSENCE_FAMILY:
        raise SnapshotCodecError("typed absence family mismatch")
    body = wrapper["canonical_body"]
    if not isinstance(body, dict):
        raise SnapshotCodecError("typed absence body must be object")
    _require_exact_keys(body, {"typed_absence_state", "detail"}, "typed absence body")
    if semantic_hash(body) != wrapper["semantic_body_hash"]:
        raise SnapshotCodecError("typed absence body identity mismatch")
    absence = TypedAbsence(body["typed_absence_state"], body["detail"])
    if canonical_json(absence.as_dict()) != canonical_json(body):
        raise SnapshotCodecError("typed absence body did not reconstruct exactly")
    return absence


def _decode_manifest(wrapper: Mapping[str, Any]) -> SourceReleaseManifest:
    _require_exact_keys(wrapper, {"record_family", "canonical_body", "content_hash", "canonical_body_sha256"}, "source manifest")
    if wrapper["record_family"] != SOURCE_MANIFEST_FAMILY:
        raise SnapshotCodecError("source manifest family mismatch")
    _verify_body_sha(wrapper)
    body = wrapper["canonical_body"]
    if not isinstance(body, dict):
        raise SnapshotCodecError("source manifest body must be object")
    expected = {
        "source_artifact_ref", "source_family_id", "study_product_id", "release_id",
        "instrument_release_id", "ingest_contract_version", "declared_universe_refs",
        "declared_authority_snapshot_refs", "declared_record_counts_by_logical_family",
        "source_snapshot_retention_ref",
    }
    _require_exact_keys(body, expected, "source manifest body")
    source_ref = exact_ref(body["source_artifact_ref"])
    manifest = SourceReleaseManifest(
        source_artifact_id=source_ref.object_id,
        source_artifact_content_hash=source_ref.content_hash,
        source_family_id=body["source_family_id"],
        study_product_id=body["study_product_id"],
        release_id=body["release_id"],
        instrument_release_id=body["instrument_release_id"],
        ingest_contract_version=body["ingest_contract_version"],
        declared_universe_refs=tuple(exact_ref(x) for x in body["declared_universe_refs"]),
        declared_authority_snapshot_refs=tuple(authority_ref(x) for x in body["declared_authority_snapshot_refs"]),
        declared_record_counts_by_logical_family=dict(body["declared_record_counts_by_logical_family"]),
        source_snapshot_retention_ref=exact_ref(body["source_snapshot_retention_ref"]),
    )
    if manifest.content_hash != wrapper["content_hash"]:
        raise SnapshotCodecError("source manifest content hash did not recompute")
    if canonical_json(manifest.semantic_projection()) != canonical_json(body):
        raise SnapshotCodecError("source manifest canonical body did not reconstruct exactly")
    return manifest


def candidate_from_snapshot(snapshot: Mapping[str, Any]) -> C11SourceReleaseCandidate:
    if not isinstance(snapshot, Mapping):
        raise SnapshotCodecError("snapshot root must be mapping")
    root_keys = {
        "schema", "encoding", "semantic_boundary", "source_release_manifest", "sections",
        "candidate_replay_manifest", "identity_summary", "validated_release_identity",
    }
    _require_exact_keys(snapshot, root_keys, "snapshot root")
    if snapshot["schema"] != SNAPSHOT_SCHEMA or snapshot["encoding"] != SNAPSHOT_ENCODING:
        raise SnapshotCodecError("snapshot schema/encoding mismatch")
    sections = snapshot["sections"]
    if not isinstance(sections, Mapping):
        raise SnapshotCodecError("sections must be object")
    if set(sections) != set(SECTION_SPECS):
        raise SnapshotCodecError("snapshot section set mismatch")

    manifest = _decode_manifest(snapshot["source_release_manifest"])
    decoded: dict[str, Any] = {}
    for name, (family, absence_allowed) in SECTION_SPECS.items():
        section = sections[name]
        if not isinstance(section, Mapping):
            raise SnapshotCodecError(f"{name} section must be object")
        representation = section.get("representation")
        if representation == "TYPED_ABSENCE":
            if not absence_allowed:
                raise SnapshotCodecError(f"{name} may not be absent")
            _require_exact_keys(section, {"representation", "record_family", "value"}, name)
            if section["record_family"] != family:
                raise SnapshotCodecError(f"{name} record family mismatch")
            decoded[name] = _decode_absence(section["value"])
        elif representation == "SEQUENCE":
            _require_exact_keys(section, {"representation", "record_family", "records"}, name)
            if section["record_family"] != family:
                raise SnapshotCodecError(f"{name} record family mismatch")
            records = section["records"]
            if not isinstance(records, list):
                raise SnapshotCodecError(f"{name} records must be array")
            objects = tuple(_decode_record(item, family) for item in records)
            if tuple(item.ref.key for item in objects) != tuple(sorted(item.ref.key for item in objects)):
                raise SnapshotCodecError(f"{name} records are not canonical exact-ref sorted")
            if len({item.ref.key for item in objects}) != len(objects):
                raise SnapshotCodecError(f"{name} contains duplicate exact refs")
            decoded[name] = objects
        else:
            raise SnapshotCodecError(f"{name} has unknown representation")

    replay = _decode_internal(snapshot["candidate_replay_manifest"], "ReplayManifest")
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=manifest,
        **decoded,
        candidate_replay_manifest=replay,
    )
    summary = snapshot["identity_summary"]
    expected_summary_keys = {
        "source_release_manifest_hash", "candidate_projection_hash",
        "replay_manifest_ref", "record_counts",
    }
    _require_exact_keys(summary, expected_summary_keys, "identity summary")
    if manifest.content_hash != summary["source_release_manifest_hash"]:
        raise SnapshotCodecError("identity summary source manifest hash mismatch")
    if replay.semantic_projection_hash != summary["candidate_projection_hash"]:
        raise SnapshotCodecError("identity summary candidate projection hash mismatch")
    if replay.ref != exact_ref(summary["replay_manifest_ref"]):
        raise SnapshotCodecError("identity summary replay manifest ref mismatch")
    if dict(record_counts_for_candidate(candidate)) != dict(summary["record_counts"]):
        raise SnapshotCodecError("identity summary record counts mismatch")
    return candidate


def snapshot_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


__all__ = [
    "SNAPSHOT_SCHEMA", "SNAPSHOT_ENCODING", "SnapshotCodecError", "SECTION_SPECS",
    "canonical_snapshot_bytes", "serialize_candidate", "serialize_snapshot_bytes",
    "write_snapshot", "parse_snapshot_bytes", "candidate_from_snapshot", "snapshot_sha256",
]
