"""Authority-gated exact physical/native representation bindings.

This module owns only the A->B representation seam:
exact source-native integer code/state + explicitly enumerated decoder token ->
exact physical binding key.  It never coerces observed values, never changes R5
typed equality, and never grants native->canonical or cross-source semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    Pre553AuthorityError,
    require_positive_authority,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key

CONTRACT = "PRE553_SOURCE_PHYSICAL_NATIVE_REPRESENTATION_BINDING@1.0.0"
AUTHORITY_KIND = "SOURCE_PHYSICAL_NATIVE_REPRESENTATION_BINDING"
GOVERNED_OPERATION = "BIND_EXACT_SOURCE_NATIVE_CODE_TO_DECODER_REPRESENTATION"
GOVERNED_OBJECT_FAMILY = "RespondentEvent@1.0.0"

UPSTREAM_DECODER_LAW_EVIDENCE_KIND = (
    "FIABC_R1J_UPSTREAM_DECODER_REPRESENTATION_LAW_EVIDENCE@1.0.0"
)
VARIABLE_TYPE_EVIDENCE_KIND = (
    "FIABC_R1J_SOURCE_VARIABLE_TYPE_EVIDENCE@1.0.0"
)
REQUIRED_EVIDENCE_KINDS = frozenset(
    (UPSTREAM_DECODER_LAW_EVIDENCE_KIND, VARIABLE_TYPE_EVIDENCE_KIND)
)

BINDING_KEYS = frozenset({
    "source_sha256",
    "variable",
    "native_code_token",
    "native_response_state",
    "decoder_value_token",
    "physical_missing_state",
    "source_missing_declaration",
})


class PhysicalNativeRepresentationError(Pre553AuthorityError):
    """Exact physical/native representation authority is absent or malformed."""


def _sha256(value: str, name: str = "source_sha256") -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value.lower() != value
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise PhysicalNativeRepresentationError(f"{name} must be lowercase sha256")
    return value


def _same(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def _normalize_binding_row(row: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(row, Mapping) or set(row) != BINDING_KEYS:
        raise PhysicalNativeRepresentationError("representation binding row has wrong exact shape")

    source_sha256 = _sha256(str(row["source_sha256"]))
    variable = row["variable"]
    if not isinstance(variable, Mapping) or set(variable) != {"ordinal", "name"}:
        raise PhysicalNativeRepresentationError("variable coordinate must contain exact ordinal/name")
    ordinal = variable["ordinal"]
    name = variable["name"]
    if (
        not isinstance(ordinal, int)
        or isinstance(ordinal, bool)
        or ordinal < 1
        or not isinstance(name, str)
        or not name
    ):
        raise PhysicalNativeRepresentationError("invalid exact variable coordinate")

    native_token = row["native_code_token"]
    if not isinstance(native_token, Mapping):
        raise PhysicalNativeRepresentationError("native code token must be an R5 token mapping")
    native_value = R5TypedValueCodec().decode(native_token)
    if not isinstance(native_value, int) or isinstance(native_value, bool):
        raise PhysicalNativeRepresentationError("this representation seam accepts exact integer source-native codes only")
    if not _same(R5TypedValueCodec().encode(native_value), native_token):
        raise PhysicalNativeRepresentationError("native code token is not canonical/reversible")

    native_state = row["native_response_state"]
    if not isinstance(native_state, str) or not native_state:
        raise PhysicalNativeRepresentationError("native response state must be a non-empty string")

    decoder_token = row["decoder_value_token"]
    if not isinstance(decoder_token, Mapping):
        raise PhysicalNativeRepresentationError("decoder value token must be an R5 token mapping")
    decoder_value = R5TypedValueCodec().decode(decoder_token)
    if not _same(R5TypedValueCodec().encode(decoder_value), decoder_token):
        raise PhysicalNativeRepresentationError("decoder value token is not canonical/reversible")

    state_text = row["physical_missing_state"]
    try:
        physical_state = PhysicalMissingState(state_text)
    except Exception as exc:
        raise PhysicalNativeRepresentationError("unknown physical missing state") from exc
    if physical_state is PhysicalMissingState.SYSTEM_MISSING:
        raise PhysicalNativeRepresentationError("system missing is outside source-native representation authority")

    declaration = row["source_missing_declaration"]
    if declaration is not None and not isinstance(declaration, Mapping):
        raise PhysicalNativeRepresentationError("source missing declaration must be mapping or null")

    return {
        "source_sha256": source_sha256,
        "variable": {"ordinal": ordinal, "name": name},
        "native_code_token": canonicalize(native_token),
        "native_response_state": native_state,
        "decoder_value_token": canonicalize(decoder_token),
        "physical_missing_state": physical_state.value,
        "source_missing_declaration": canonicalize(declaration),
    }


def representation_authority_fingerprint(
    *,
    scope_envelope: Mapping[str, Any],
    parent_authority_refs: Sequence[AuthorityRef | Mapping[str, Any]],
    dependency_refs: Sequence[ExactRef | Mapping[str, Any]],
    negative_limit_refs: Sequence[ExactRef | Mapping[str, Any]],
) -> str:
    # AuthoritySnapshot canonicalizes these fields as set-like collections.
    # Fingerprinting must therefore be invariant to caller insertion order and
    # must replay from the immutable snapshot's canonical ordering.
    parents = tuple(sorted(
        (authority_ref(x, "representation parent authority") for x in parent_authority_refs),
        key=lambda x: x.key,
    ))
    dependencies = tuple(sorted(
        (exact_ref(x, "representation evidence dependency") for x in dependency_refs),
        key=lambda x: x.key,
    ))
    negatives = tuple(sorted(
        (exact_ref(x, "representation negative limit") for x in negative_limit_refs),
        key=lambda x: x.key,
    ))
    return semantic_hash({
        "contract": CONTRACT,
        "authority_kind": AUTHORITY_KIND,
        "governed_operation": GOVERNED_OPERATION,
        "scope_envelope": canonicalize(scope_envelope),
        "parent_authority_refs": [x.as_dict() for x in parents],
        "dependency_refs": [x.as_dict() for x in dependencies],
        "negative_limit_refs": [x.as_dict() for x in negatives],
    })


def validate_representation_authority(snapshot: AuthoritySnapshot) -> AuthoritySnapshot:
    require_positive_authority(
        snapshot,
        authority_kind=AUTHORITY_KIND,
        operation=GOVERNED_OPERATION,
        object_family=GOVERNED_OBJECT_FAMILY,
    )

    scope = snapshot.scope_envelope
    if not isinstance(scope, Mapping):
        raise PhysicalNativeRepresentationError("representation authority scope must be a mapping")
    required_scope_keys = {
        "source_artifact_sha256",
        "source_universe_refs",
        "target_use_refs",
        "predicate_or_risk_set_refs",
        "exact_representation_bindings",
        "source_semantics_authority_ref",
        "upstream_evidence_refs",
        "canonical_question_mapping",
        "native_to_canonical_mapping",
        "cross_source_relation",
        "candidate_output_parentage",
        "system_missing",
    }
    if set(scope) != required_scope_keys:
        raise PhysicalNativeRepresentationError("representation authority scope has wrong exact keys")

    _sha256(str(scope["source_artifact_sha256"]))
    rows = scope["exact_representation_bindings"]
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes, bytearray)) or not rows:
        raise PhysicalNativeRepresentationError("representation authority requires explicit binding rows")
    normalized_rows = tuple(_normalize_binding_row(row) for row in rows)
    if len({canonical_json(row) for row in normalized_rows}) != len(normalized_rows):
        raise PhysicalNativeRepresentationError("duplicate exact representation binding row")

    for row in normalized_rows:
        if row["source_sha256"] != scope["source_artifact_sha256"]:
            raise PhysicalNativeRepresentationError("binding row source differs from authority source")

    if scope["canonical_question_mapping"] != "ABSENT_NOT_AUTHORIZED":
        raise PhysicalNativeRepresentationError("representation authority cannot grant canonical question mapping")
    if scope["native_to_canonical_mapping"] != "OUT_OF_SCOPE":
        raise PhysicalNativeRepresentationError("representation authority cannot grant native-to-canonical mapping")
    if scope["cross_source_relation"] != "NONE_AUTHORIZED":
        raise PhysicalNativeRepresentationError("representation authority cannot grant cross-source relation")
    if scope["candidate_output_parentage"] != "FORBIDDEN":
        raise PhysicalNativeRepresentationError("candidate output cannot parent representation authority")
    if scope["system_missing"] != "OUT_OF_SCOPE":
        raise PhysicalNativeRepresentationError("system missing must remain outside source-native representation authority")

    source_semantics = authority_ref(scope["source_semantics_authority_ref"], "source semantics authority")
    parents = tuple(authority_ref(x, "representation parent authority") for x in snapshot.parent_authority_refs)
    if parents != (source_semantics,):
        raise PhysicalNativeRepresentationError("exact source semantics must be the sole authority parent")

    evidence = tuple(exact_ref(x, "upstream representation evidence") for x in snapshot.dependency_refs)
    if len(evidence) != 2 or {x.kind for x in evidence} != REQUIRED_EVIDENCE_KINDS:
        raise PhysicalNativeRepresentationError("exact decoder-law and variable-type evidence are both required")
    scoped_evidence = tuple(exact_ref(x, "scoped upstream evidence") for x in scope["upstream_evidence_refs"])
    if {x.key for x in evidence} != {x.key for x in scoped_evidence}:
        raise PhysicalNativeRepresentationError("scope upstream evidence differs from dependency closure")

    expected_fingerprint = representation_authority_fingerprint(
        scope_envelope=scope,
        parent_authority_refs=snapshot.parent_authority_refs,
        dependency_refs=snapshot.dependency_refs,
        negative_limit_refs=snapshot.negative_limit_refs,
    )
    if snapshot.interpretation_semantics_fingerprint != expected_fingerprint:
        raise PhysicalNativeRepresentationError("representation authority interpretation fingerprint mismatch")
    return snapshot


@dataclass(frozen=True)
class AuthorizedPhysicalBinding:
    source_sha256: str
    variable_ordinal: int
    variable_name: str
    native_code: int
    native_response_state: str
    decoder_value: Any
    decoder_value_token: Mapping[str, Any]
    physical_missing_state: PhysicalMissingState
    source_missing_declaration: Mapping[str, Any] | None
    physical_key: str
    representation_authority_ref: AuthorityRef


def resolve_authorized_physical_binding(
    snapshot: AuthoritySnapshot,
    *,
    source_sha256: str,
    variable_ordinal: int,
    variable_name: str,
    native_code: int,
    native_response_state: str,
) -> AuthorizedPhysicalBinding:
    validate_representation_authority(snapshot)
    source_sha256 = _sha256(source_sha256)
    if source_sha256 != snapshot.scope_envelope["source_artifact_sha256"]:
        raise PhysicalNativeRepresentationError("source outside exact representation authority")
    if not isinstance(variable_ordinal, int) or isinstance(variable_ordinal, bool) or variable_ordinal < 1:
        raise PhysicalNativeRepresentationError("invalid variable ordinal")
    if not isinstance(variable_name, str) or not variable_name:
        raise PhysicalNativeRepresentationError("invalid variable name")
    if not isinstance(native_code, int) or isinstance(native_code, bool):
        raise PhysicalNativeRepresentationError("native code must be an exact integer")
    if not isinstance(native_response_state, str) or not native_response_state:
        raise PhysicalNativeRepresentationError("native response state required")

    native_token = R5TypedValueCodec().encode(native_code)
    matches = []
    for raw_row in snapshot.scope_envelope["exact_representation_bindings"]:
        row = _normalize_binding_row(raw_row)
        if (
            row["source_sha256"] == source_sha256
            and row["variable"] == {"ordinal": variable_ordinal, "name": variable_name}
            and _same(row["native_code_token"], native_token)
            and row["native_response_state"] == native_response_state
        ):
            matches.append(row)
    if len(matches) != 1:
        raise PhysicalNativeRepresentationError("no unique exact authorized representation binding")

    row = matches[0]
    decoder_value = R5TypedValueCodec().decode(row["decoder_value_token"])
    physical_state = PhysicalMissingState(row["physical_missing_state"])
    declaration = row["source_missing_declaration"]
    physical_key = physical_value_binding_key(
        decoder_value,
        physical_state,
        declaration,
    )
    return AuthorizedPhysicalBinding(
        source_sha256=source_sha256,
        variable_ordinal=variable_ordinal,
        variable_name=variable_name,
        native_code=native_code,
        native_response_state=native_response_state,
        decoder_value=decoder_value,
        decoder_value_token=row["decoder_value_token"],
        physical_missing_state=physical_state,
        source_missing_declaration=declaration,
        physical_key=physical_key,
        representation_authority_ref=snapshot.authority_ref,
    )


def build_representation_authority_snapshot(
    *,
    authority_id: str,
    authority_version: str,
    source_sha256: str,
    source_universe_ref: ExactRef,
    target_use_ref: Any,
    predicate_or_risk_set_ref: ExactRef,
    source_semantics_authority_ref: AuthorityRef,
    upstream_decoder_law_evidence_ref: ExactRef,
    variable_type_evidence_ref: ExactRef,
    exact_representation_bindings: Sequence[Mapping[str, Any]],
    negative_limit_refs: Sequence[ExactRef],
    effective_time_or_interval: Mapping[str, Any],
) -> AuthoritySnapshot:
    source_sha256 = _sha256(source_sha256)
    if upstream_decoder_law_evidence_ref.kind != UPSTREAM_DECODER_LAW_EVIDENCE_KIND:
        raise PhysicalNativeRepresentationError("wrong upstream decoder-law evidence class")
    if variable_type_evidence_ref.kind != VARIABLE_TYPE_EVIDENCE_KIND:
        raise PhysicalNativeRepresentationError("wrong variable-type evidence class")
    rows = tuple(_normalize_binding_row(row) for row in exact_representation_bindings)
    if any(row["source_sha256"] != source_sha256 for row in rows):
        raise PhysicalNativeRepresentationError("binding row source differs from authority source")

    evidence_refs = (upstream_decoder_law_evidence_ref, variable_type_evidence_ref)
    scope = {
        "source_artifact_sha256": source_sha256,
        "source_universe_refs": [source_universe_ref.as_dict()],
        "target_use_refs": [canonicalize(target_use_ref)],
        "predicate_or_risk_set_refs": [predicate_or_risk_set_ref.as_dict()],
        "exact_representation_bindings": list(rows),
        "source_semantics_authority_ref": source_semantics_authority_ref.as_dict(),
        "upstream_evidence_refs": [x.as_dict() for x in evidence_refs],
        "canonical_question_mapping": "ABSENT_NOT_AUTHORIZED",
        "native_to_canonical_mapping": "OUT_OF_SCOPE",
        "cross_source_relation": "NONE_AUTHORIZED",
        "candidate_output_parentage": "FORBIDDEN",
        "system_missing": "OUT_OF_SCOPE",
    }
    authority_material = {
        "contract": CONTRACT,
        "authority_kind": AUTHORITY_KIND,
        "governed_operation": GOVERNED_OPERATION,
        "governed_object_family": GOVERNED_OBJECT_FAMILY,
        "scope_envelope": scope,
        "source_semantics_authority_ref": source_semantics_authority_ref.as_dict(),
        "upstream_evidence_refs": [x.as_dict() for x in evidence_refs],
        "negative_limit_refs": [x.as_dict() for x in negative_limit_refs],
    }
    authority_content_hash = semantic_hash(authority_material)
    authority_ref_obj = AuthorityRef(authority_id, authority_version, authority_content_hash)
    fingerprint = representation_authority_fingerprint(
        scope_envelope=scope,
        parent_authority_refs=(source_semantics_authority_ref,),
        dependency_refs=evidence_refs,
        negative_limit_refs=negative_limit_refs,
    )
    replay_material = {
        "contract": CONTRACT,
        "authority_ref": authority_ref_obj.as_dict(),
        "authority_material_hash": authority_content_hash,
        "interpretation_semantics_fingerprint": fingerprint,
    }
    replay_hash = semantic_hash(replay_material)
    replay_ref = ExactRef(
        "PRE553_PHYSICAL_NATIVE_REPRESENTATION_REPLAY_ROOT@1.0.0",
        f"urn:rawlsing:pre553:physical-native-representation:sha256:{replay_hash}",
        replay_hash,
    )
    snapshot = AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=evidence_refs,
        producer_replay_locator_or_reference_root=replay_ref,
        authority_id=authority_ref_obj.authority_id,
        authority_version=authority_ref_obj.authority_version,
        authority_content_hash=authority_ref_obj.authority_content_hash,
        authority_kind=AUTHORITY_KIND,
        decision_state="ALLOW",
        governed_operations=(GOVERNED_OPERATION,),
        governed_object_families=(GOVERNED_OBJECT_FAMILY,),
        scope_envelope=scope,
        effective_time_or_interval=effective_time_or_interval,
        parent_authority_refs=(source_semantics_authority_ref,),
        negative_limit_refs=tuple(negative_limit_refs),
        supersession_refs=(),
        interpretation_semantics_fingerprint=fingerprint,
        replay_protocol_ref=replay_ref,
    )
    return validate_representation_authority(snapshot)


__all__ = [
    "AUTHORITY_KIND",
    "BINDING_KEYS",
    "CONTRACT",
    "GOVERNED_OBJECT_FAMILY",
    "GOVERNED_OPERATION",
    "PhysicalNativeRepresentationError",
    "REQUIRED_EVIDENCE_KINDS",
    "UPSTREAM_DECODER_LAW_EVIDENCE_KIND",
    "VARIABLE_TYPE_EVIDENCE_KIND",
    "AuthorizedPhysicalBinding",
    "build_representation_authority_snapshot",
    "representation_authority_fingerprint",
    "resolve_authorized_physical_binding",
    "validate_representation_authority",
]
