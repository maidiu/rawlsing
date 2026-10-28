"""Smallest native-C11 receipt adapter for the actual Lane A durable product.

Lane A stores native public/internal objects as streaming pickle streams plus
JSON receipt/manifest files.  This adapter validates the external receipt,
stream hashes/counts, replay manifest and release identity before rehydrating a
trusted locally-produced ``C11LogicalRelease`` through the existing native C11
factory.  It does not convert storage, read the original SAV, or trust a bare
path descriptor.
"""
from __future__ import annotations

import copyreg
from dataclasses import fields
import hashlib
import json
import pickle
from pathlib import Path
import types
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_c11_integrity import (
    C11InternalRecord,
    ReplayManifest,
    TypedAbsence,
    assert_internal_carrier_record,
    make_m01_m18_coverage,
    verify_public_object_integrity,
)
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, _make_validated_release
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    CanonicalSemanticObject,
    ExactRef,
    exact_ref,
    semantic_hash,
)

# Match Lane A's local writer so mappingproxy descendants remain loadable.
copyreg.pickle(types.MappingProxyType, lambda mapping: (dict, (dict(mapping),)))

LOCAL_SCHEMA = "PYAT_SRC04_FULL_LOCAL_RELEASE@1.0.0"
RELEASE_SCHEMA = "PYAT_SRC04_FULL_RELEASE_RECEIPT@1.0.0"
PRIMARY_SCHEMA = "PYAT_SRC04_FULL_PRIMARY_RUN@1.0.0"
SOURCE_ID = "SRC04"
SOURCE_SHA256 = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
DEFAULT_SOURCE_ARTIFACT_ID = "Arab Barometer Wave 1.sav"


class ActualCarrierRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def _sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ActualCarrierRefusal("ACTUAL_RECEIPT_UNREADABLE", str(exc)) from exc


def _decode_external(value: Any) -> Any:
    if isinstance(value, Mapping):
        keys = set(value)
        if keys == {"kind", "object_id", "content_hash"}:
            return exact_ref(value)
        if keys == {"authority_id", "authority_version", "authority_content_hash"}:
            return AuthorityRef(value["authority_id"], value["authority_version"], value["authority_content_hash"])
        if keys == {"typed_absence_state", "detail"}:
            return TypedAbsence(value["typed_absence_state"], value.get("detail"))
        return {key: _decode_external(item) for key, item in value.items()}
    if isinstance(value, list):
        return tuple(_decode_external(item) for item in value)
    return value


def _replay_manifest(path: Path) -> ReplayManifest:
    raw = _load_json(path)
    if not isinstance(raw, Mapping) or raw.get("record_family") != "ReplayManifest":
        raise ActualCarrierRefusal("REPLAY_MANIFEST_FAMILY_MISMATCH")
    semantic = raw.get("semantic_fields")
    if not isinstance(semantic, Mapping):
        raise ActualCarrierRefusal("REPLAY_MANIFEST_FIELDS_MISSING")
    kwargs = {key: _decode_external(value) for key, value in semantic.items()}
    manifest = ReplayManifest(**kwargs)
    if raw.get("object_id") != manifest.object_id or raw.get("content_hash") != manifest.content_hash:
        raise ActualCarrierRefusal("REPLAY_MANIFEST_IDENTITY_MISMATCH")
    return manifest


def _iter_pickle(path: Path):
    with path.open("rb") as handle:
        while True:
            try:
                yield pickle.load(handle)
            except EOFError:
                return


def _validate_receipts(
    *,
    local_receipt: Mapping[str, Any],
    release_receipt: Mapping[str, Any],
    primary: Mapping[str, Any],
    bundle: Path,
    expected_source_sha256: str,
) -> None:
    if local_receipt.get("schema") != LOCAL_SCHEMA:
        raise ActualCarrierRefusal("LOCAL_RECEIPT_SCHEMA_MISMATCH")
    if release_receipt.get("schema") != RELEASE_SCHEMA:
        raise ActualCarrierRefusal("RELEASE_RECEIPT_SCHEMA_MISMATCH")
    if primary.get("schema") != PRIMARY_SCHEMA or primary.get("status") != "FULL_PRIMARY_COMPLETE":
        raise ActualCarrierRefusal("PRIMARY_NOT_COMPLETE")
    for receipt, label in ((local_receipt, "local"), (release_receipt, "release")):
        if receipt.get("source_id") != SOURCE_ID or receipt.get("source_sha256") != expected_source_sha256:
            raise ActualCarrierRefusal(f"{label.upper()}_SOURCE_MISMATCH")
        if receipt.get("release_ref") != local_receipt.get("release_ref"):
            raise ActualCarrierRefusal(f"{label.upper()}_RELEASE_MISMATCH")
        if receipt.get("source_release_manifest_hash") != local_receipt.get("source_release_manifest_hash"):
            raise ActualCarrierRefusal(f"{label.upper()}_MANIFEST_MISMATCH")
    if release_receipt.get("source_read_performed") is not True:
        raise ActualCarrierRefusal("RELEASE_RECEIPT_NOT_ORIGINAL_READ")
    if local_receipt.get("local_only") is not True or local_receipt.get("raw_respondent_cells_committed") is not False:
        raise ActualCarrierRefusal("LOCAL_RECEIPT_PRIVACY_STATE_INVALID")
    if release_receipt.get("release_audit", {}).get("source_artifact_sha") is not True:
        raise ActualCarrierRefusal("RELEASE_AUDIT_SOURCE_IDENTITY_FAILED")
    if release_receipt.get("release_audit", {}).get("semantic_hash_matches_ref") is not True:
        raise ActualCarrierRefusal("RELEASE_AUDIT_SEMANTIC_IDENTITY_FAILED")
    if release_receipt.get("release_audit", {}).get("no_canonical") is not True:
        raise ActualCarrierRefusal("RELEASE_AUDIT_CANONICAL_VALUE_PRESENT")
    for key in ("public_objects", "internal_records", "replay_manifest"):
        info = local_receipt.get(key)
        if not isinstance(info, Mapping):
            raise ActualCarrierRefusal(f"LOCAL_RECEIPT_{key.upper()}_MISSING")
        file_path = bundle / str(info.get("file"))
        if not file_path.is_file():
            raise ActualCarrierRefusal(f"LOCAL_RECEIPT_{key.upper()}_FILE_MISSING")
        if _sha_file(file_path) != info.get("sha256"):
            raise ActualCarrierRefusal(f"LOCAL_RECEIPT_{key.upper()}_SHA_MISMATCH")
        if key != "replay_manifest" and file_path.stat().st_size != info.get("bytes"):
            raise ActualCarrierRefusal(f"LOCAL_RECEIPT_{key.upper()}_BYTE_COUNT_MISMATCH")


def load_actual_carrier_release(
    *,
    local_receipt_path: str | Path,
    release_receipt_path: str | Path,
    primary_run_path: str | Path,
    bundle_dir: str | Path | None = None,
    expected_source_sha256: str = SOURCE_SHA256,
    local_receipt_sha256: str | None = None,
    release_receipt_sha256: str | None = None,
    primary_run_sha256: str | None = None,
) -> C11LogicalRelease:
    local_path = Path(local_receipt_path)
    release_path = Path(release_receipt_path)
    primary_path = Path(primary_run_path)
    for path, expected, label in (
        (local_path, local_receipt_sha256, "local receipt"),
        (release_path, release_receipt_sha256, "release receipt"),
        (primary_path, primary_run_sha256, "primary run"),
    ):
        if expected is not None and _sha_file(path) != expected:
            raise ActualCarrierRefusal(
                f"{label.upper().replace(' ', '_')}_SHA256_MISMATCH")
    local = _load_json(local_path)
    release = _load_json(release_path)
    primary = _load_json(primary_path)
    if not isinstance(local, Mapping) or not isinstance(release, Mapping) or not isinstance(primary, Mapping):
        raise ActualCarrierRefusal("ACTUAL_RECEIPT_NOT_MAPPING")
    bundle = Path(bundle_dir) if bundle_dir is not None else local_path.parent
    _validate_receipts(
        local_receipt=local, release_receipt=release, primary=primary,
        bundle=bundle, expected_source_sha256=expected_source_sha256,
    )
    public_path = bundle / local["public_objects"]["file"]
    internal_path = bundle / local["internal_records"]["file"]
    replay_path = bundle / local["replay_manifest"]["file"]
    public_objects = tuple(_iter_pickle(public_path))
    internal_records = tuple(_iter_pickle(internal_path))
    if len(public_objects) != local["public_objects"]["lines"]:
        raise ActualCarrierRefusal("PUBLIC_STREAM_COUNT_MISMATCH")
    if len(internal_records) != local["internal_records"]["lines"]:
        raise ActualCarrierRefusal("INTERNAL_STREAM_COUNT_MISMATCH")
    if any(not isinstance(obj, CanonicalSemanticObject) for obj in public_objects):
        raise ActualCarrierRefusal("PUBLIC_STREAM_TYPE_MISMATCH")
    if any(not isinstance(obj, C11InternalRecord) for obj in internal_records):
        raise ActualCarrierRefusal("INTERNAL_STREAM_TYPE_MISMATCH")
    for obj in public_objects:
        verify_public_object_integrity(obj)
    for obj in internal_records:
        assert_internal_carrier_record(obj)
    replay_manifest = _replay_manifest(replay_path)
    if replay_manifest.ref.as_dict() != local.get("replay_manifest_ref"):
        raise ActualCarrierRefusal("REPLAY_MANIFEST_REF_MISMATCH")
    release_ref = exact_ref(local["release_ref"], "release_ref")
    if release_ref.kind != "C11LogicalRelease":
        raise ActualCarrierRefusal("RELEASE_REF_KIND_MISMATCH")
    source_sha = local["source_sha256"]
    if source_sha != expected_source_sha256:
        raise ActualCarrierRefusal("ACTUAL_SOURCE_SHA_MISMATCH")
    source_artifact_ref = exact_ref(
        local.get("source_artifact_ref")
        or {"kind": "SOURCE_ARTIFACT", "object_id": DEFAULT_SOURCE_ARTIFACT_ID, "content_hash": source_sha},
        "source_artifact_ref",
    )
    if source_artifact_ref.content_hash != source_sha:
        raise ActualCarrierRefusal("SOURCE_ARTIFACT_REF_MISMATCH")
    universes = tuple(obj for obj in public_objects if obj.schema_id == "EmpiricalUniverse")
    respondents = tuple(obj for obj in internal_records if obj.__class__.__name__ == "RespondentIdentity")
    questions = tuple(obj for obj in internal_records if obj.__class__.__name__ == "QuestionVariableBinding")
    events = tuple(obj for obj in public_objects if obj.schema_id == "RespondentEvent")
    routing = tuple(obj for obj in public_objects if obj.schema_id == "RoutingEligibilityFact")
    coordinates = tuple(obj for obj in public_objects if obj.schema_id == "EmpiricalCoordinateFact")
    authorities = tuple(obj for obj in public_objects if obj.schema_id == "AuthoritySnapshot")
    coverage = make_m01_m18_coverage(
        universes=universes,
        respondents=respondents,
        questions=questions,
        events=events,
        routing=routing,
        coordinates=coordinates,
        weight_section_explicit=True,
        authority_snapshots=authorities,
        source_relation_section_explicit=True,
        predicate_replay_section_explicit=True,
        comparator_section_explicit=True,
        discovery_section_explicit=True,
        structural_admission_section_explicit=True,
        replay_manifest=replay_manifest,
    )
    derived_hash = semantic_hash({
        "candidate_projection_hash": replay_manifest.semantic_projection_hash,
        "replay_manifest_ref": replay_manifest.ref.as_dict(),
        "m01_m18": {key: list(value) for key, value in coverage.items()},
    })
    if derived_hash != local.get("semantic_release_hash") or derived_hash != release_ref.content_hash:
        raise ActualCarrierRefusal("RELEASE_SEMANTIC_HASH_MISMATCH")
    if release_ref.object_id != release.get("release_ref", {}).get("object_id"):
        raise ActualCarrierRefusal("RELEASE_RECEIPT_OBJECT_ID_MISMATCH")
    try:
        native_release = _make_validated_release(
            release_id=release_ref.object_id,
            source_artifact_ref=source_artifact_ref,
            source_release_manifest_hash=local["source_release_manifest_hash"],
            semantic_release_hash=derived_hash,
            replay_manifest=replay_manifest,
            public_objects=tuple(sorted(public_objects, key=lambda obj: obj.ref.key)),
            internal_records=tuple(sorted(internal_records, key=lambda obj: obj.ref.key)),
            m01_m18_coverage=coverage,
        )
    except Exception as exc:
        raise ActualCarrierRefusal("NATIVE_RELEASE_REHYDRATION_FAILED", str(exc)) from exc
    if native_release.release_ref != release_ref:
        raise ActualCarrierRefusal("NATIVE_RELEASE_REF_MISMATCH")
    if native_release.source_artifact_ref.content_hash != expected_source_sha256:
        raise ActualCarrierRefusal("NATIVE_RELEASE_SOURCE_IDENTITY_MISMATCH")
    return native_release


__all__ = [
    "LOCAL_SCHEMA", "RELEASE_SCHEMA", "PRIMARY_SCHEMA",
    "ActualCarrierRefusal", "load_actual_carrier_release",
]
