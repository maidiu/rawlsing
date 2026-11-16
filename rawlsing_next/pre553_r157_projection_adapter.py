"""Recovered R157 source/administration seam for the current PRE553 owners.

This module is an isolated adapter, not a replacement engine.  It re-expresses
the exact historical R157 ``library`` / ``factory`` / ``reader`` / ``validator``
contract at commit ``1924499ef52403a0f331b8aff9b7c7eff99bf1e2`` on top of the
current protected ``GovernedC11Projection`` and
``project_c11_candidate_from_physical_cells`` first consumer.

The historical package ``rawlsing_next/source_configuration`` no longer exists
in the protected tree, and ``rawlsing_next/pre553_source_read_admission.py`` is
also absent.  Their stronger closed behaviours are ported here because the
current tree has no source-config authority and no source-read admission owner.
Nothing in this module grants a source right, original35 permission, a new
semantic authority, a new statistical engine, or a fallback selector.  A
nonrespondent fixture is explicit sourcefree test input, not a source read.
"""

from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, fields as dataclass_fields, is_dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence

from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_empirical_objects import (
    STATE_FAMILIES,
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    SourceUniverseRelation,
    authority_ref,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    COMPATIBILITY_ONLY,
    DECLARED_ENCODING_ALLOWLIST,
    SOURCE_DECLARED_ENCODING_ONLY,
    DecoderError,
    PhysicalCell,
    PhysicalMissingState,
    PhysicalSourceIncidence,
    decode_dta,
    decode_sav,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    COORDINATE_OWNER_FAMILY,
    RESPONSE_OWNER_FAMILY,
    WEIGHT_OWNER_FAMILY,
    CoordinateSlotRule,
    CoordinateValueRule,
    ExactPhysicalCellStream,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    PhysicalSlotOwnerAuthorization,
    PhysicalSlotOwnerSet,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    WeightSlotRule,
    WeightValueRule,
    build_source_backed_c11_repository,
    build_validated_source_backed_c11_release,
    build_validated_source_backed_c11_release_from_stream,
    physical_value_binding_key,
)

R157_HISTORICAL_COMMIT = "1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
SCHEMA_ID = "PYAT_R157_SOURCE_CONFIGURATION@1.0.0"
FIXTURE_SCHEMA_ID = "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0"
CONFIG_PURPOSE_SOURCE = "SOURCE_PREPARATION"
CONFIG_PURPOSE_FIXTURE = "NONRESPONDENT_FIXTURE"
CONFIG_PURPOSE_EXAMPLE = "P0_EXAMPLE_FIXTURE"
IDENTITY_CLASS_ORIGINAL = "ORIGINAL_SOURCE"
IDENTITY_CLASS_FIXTURE = "NONRESPONDENT_FIXTURE"
ADAPTER_IMPLEMENTATION_ID = "rawlsing_next/pre553_r157_projection_adapter.py"


class SourceConfigurationError(ValueError):
    """Base configuration error."""


class SourceConfigurationSchemaError(SourceConfigurationError):
    """The serialized configuration is not closed/valid."""


class SourceConfigurationBindingError(SourceConfigurationError):
    """The active source/fixture binding is inconsistent with the config."""


class SourceConfigurationFactoryError(SourceConfigurationError):
    """The validated config cannot be mapped to the native owner."""


class SourceConfigurationEvidenceError(SourceConfigurationError):
    """Pinned evidence is missing, malformed, or inconsistent."""


class SourceReadAdmissionRefusal(ValueError):
    """The independently injected source-read decision did not admit a read."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


SOURCE_RESPONSE_DECODE = "SOURCE_RESPONSE_DECODE"
EXACT_FILE = "EXACT_FILE"
CURRENT_GRANTED = "CURRENT_GRANTED"
TERMINAL_STATES = frozenset({"REVOKED", "EXPIRED", "SUPERSEDED", "SUSPENDED"})
SOURCE_FORMATS = frozenset({"SAV", "DTA"})


def _sha_value(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value.lower() != value
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise SourceReadAdmissionRefusal("SOURCE_READ_SHA_REQUIRED", name)
    return value


def _text_value(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceReadAdmissionRefusal("SOURCE_READ_FIELD_REQUIRED", name)
    return value


def _exact_ref_values(value: Any, name: str) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or not value:
        raise SourceReadAdmissionRefusal("SOURCE_READ_REFS_REQUIRED", name)
    try:
        return tuple(sorted((exact_ref(item, name) for item in value), key=lambda ref: ref.key))
    except Exception as exc:
        raise SourceReadAdmissionRefusal("SOURCE_READ_REFS_INVALID", name) from exc


# ---------------------------------------------------------------------------
# Historical validator.py (closed schema) -- ported verbatim in behaviour.
# ---------------------------------------------------------------------------

"""Closed schema validation for R157 source configurations.

The validator is intentionally explicit.  It parses the serialized form into the
*actual* native dataclasses where a native owner exists, so a config cannot pass
validation while claiming fields the receiving owner does not have.
"""

from dataclasses import fields as dataclass_fields, is_dataclass
import re
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    STATE_FAMILIES,
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    SourceUniverseRelation,
    authority_ref,
    exact_ref,
)
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    COMPATIBILITY_ONLY,
    PhysicalMissingState,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    COORDINATE_OWNER_FAMILY,
    RESPONSE_OWNER_FAMILY,
    WEIGHT_OWNER_FAMILY,
    CoordinateSlotRule,
    CoordinateValueRule,
    OccurrenceRule,
    PhysicalSlot,
    PhysicalSlotOwnerAuthorization,
    PhysicalSlotOwnerSet,
    ResponseSlotRule,
    ResponseValueRule,
    WeightSlotRule,
    WeightValueRule,
    physical_value_binding_key,
)


_SOURCE_ID = re.compile(r"^SRC(0[1-9]|[12][0-9]|3[0-5])$")
_SHA = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_FORMATS = frozenset({"SAV", "DTA"})
_FORBIDDEN_SELECTOR_TOKENS = ("latest", "default", "fuzzy", "nearest")
_FORBIDDEN_PRIVATE_PATH_FRAGMENTS = (
    "/Users/", "/private/", "\\Users\\", "Rawlsing_Worktrees",
    "Rawlsing_Authority_Document_Archive", "/.r61/", "\\.r61\\",
)
_SYNTHETIC_TOKENS = (
    "SYNTHETIC_SOURCEFREE", "TEST_ONLY", "DEFAULT_FORM", "DEFAULT_SAMPLE",
    "ADMINISTERED_TRUE", "ZZ-SYNTHETIC",
)
_MISSING_STATES = frozenset(x.value for x in PhysicalMissingState)
_RESPONSE_STATES = STATE_FAMILIES["RESPONSE_EVENT_STATE"]
_COORDINATE_STATES = STATE_FAMILIES["EMPIRICAL_COORDINATE_STATE"]
_WEIGHT_STATES = STATE_FAMILIES["WEIGHT_MEASURE_STATE"]
_ROUTING_STATES = STATE_FAMILIES["ROUTING_ELIGIBILITY_STATE"]
_OWNER_FAMILIES = frozenset({RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY, WEIGHT_OWNER_FAMILY})

_HISTORICAL_RUNTIME_CALLABLES = {
    "projection_builder": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
    "release_builder": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
    "repository_builder": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
    "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
    "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
    "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
    "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
}
_ADAPTER_RUNTIME_CALLABLES = {
    "projection_builder": "rawlsing_next.pre553_r157_projection_adapter.build_governed_c11_projection",
    "release_builder": "rawlsing_next.pre553_r157_projection_adapter.build_validated_c11_release_from_config",
    "repository_builder": "rawlsing_next.pre553_r157_projection_adapter.build_source_backed_c11_repository_from_config",
    "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
    "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
    "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
    "source_read_owner": "rawlsing_next.pre553_r157_projection_adapter.decode_with_source_read_permission",
}
_RUNTIME_CALLABLES = _ADAPTER_RUNTIME_CALLABLES


def _fail(path: str, message: str) -> None:
    raise SourceConfigurationSchemaError(f"{path}: {message}")


def _mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail(path, "must be an object")
    return value


def _sequence(value: Any, path: str, *, nonempty: bool = False) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        _fail(path, "must be an array")
    if nonempty and not value:
        _fail(path, "must not be empty")
    return value


def _text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(path, "must be a non-empty string")
    return value.strip()


def _optional_text(value: Any, path: str) -> str | None:
    if value is None:
        return None
    return _text(value, path)


def _integer(value: Any, path: str, *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        _fail(path, f"must be an integer >= {minimum}")
    return value


def _boolean(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        _fail(path, "must be a boolean")
    return value


def _sha(value: Any, path: str) -> str:
    if not isinstance(value, str) or not _SHA.match(value):
        _fail(path, "must be a lowercase sha256")
    return value


def _exact_keys(mapping: Mapping[str, Any], path: str, required: Iterable[str],
                optional: Iterable[str] = ()) -> None:
    required = set(required)
    optional = set(optional)
    missing = sorted(required - set(mapping))
    if missing:
        _fail(path, f"missing keys {missing!r}")
    extra = sorted(set(mapping) - required - optional)
    if extra:
        _fail(path, f"unknown keys {extra!r}")


def _native_allowed_keys(cls: type) -> set[str]:
    if is_dataclass(cls):
        return {field.name for field in dataclass_fields(cls)}
    # CanonicalSemanticObject subclasses are not dataclasses: they take the
    # common carrier arguments plus their declared semantic fields.
    return {
        "typed_state", "authority_snapshot_refs", "dependency_refs",
        "producer_replay_locator_or_reference_root", *getattr(cls, "REQUIRED_FIELDS", ()),
    }


def _native_keys(payload: Mapping[str, Any], cls: type, path: str) -> dict[str, Any]:
    allowed = _native_allowed_keys(cls)
    extra = sorted(set(payload) - allowed)
    if extra:
        _fail(path, f"keys are not fields of {cls.__name__}: {extra!r}")
    return dict(payload)


def _exact_ref_value(value: Any, path: str) -> ExactRef:
    mapping = _mapping(value, path)
    _exact_keys(mapping, path, ("kind", "object_id", "content_hash"))
    try:
        return exact_ref(mapping, path)
    except Exception as exc:  # native error type is intentionally not leaked as schema
        raise SourceConfigurationSchemaError(f"{path}: invalid ExactRef: {exc}") from exc


def _authority_ref_value(value: Any, path: str) -> AuthorityRef:
    mapping = _mapping(value, path)
    _exact_keys(mapping, path, ("authority_id", "authority_version", "authority_content_hash"))
    try:
        return authority_ref(mapping, path)
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid AuthorityRef: {exc}") from exc


def _ref_list(value: Any, path: str, *, nonempty: bool = False) -> tuple[ExactRef, ...]:
    items = _sequence(value, path, nonempty=nonempty)
    return tuple(_exact_ref_value(item, f"{path}[{index}]") for index, item in enumerate(items))


def _authority_ref_list(value: Any, path: str, *, nonempty: bool = False) -> tuple[AuthorityRef, ...]:
    items = _sequence(value, path, nonempty=nonempty)
    return tuple(_authority_ref_value(item, f"{path}[{index}]") for index, item in enumerate(items))


def _typed_absence_value(value: Any, path: str) -> TypedAbsence:
    mapping = _mapping(value, path)
    _exact_keys(mapping, path, ("typed_absence_state",), ("detail",))
    try:
        return TypedAbsence(mapping["typed_absence_state"], mapping.get("detail"))
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid typed absence: {exc}") from exc


def _typed_absence_or_ref(value: Any, path: str) -> ExactRef | TypedAbsence:
    if isinstance(value, Mapping) and "typed_absence_state" in value:
        return _typed_absence_value(value, path)
    return _exact_ref_value(value, path)


def _check_no_private_paths(value: Any, path: str = "$") -> None:
    if isinstance(value, str):
        for fragment in _FORBIDDEN_PRIVATE_PATH_FRAGMENTS:
            if fragment in value:
                _fail(path, f"private/absolute runtime path is not portable: {value!r}")
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            _check_no_private_paths(item, f"{path}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, item in enumerate(value):
            _check_no_private_paths(item, f"{path}[{index}]")


def _assert_no_forbidden_selector(text: str, path: str) -> None:
    lowered = text.strip().lower()
    if any(token == lowered or lowered.startswith(token + ":") for token in _FORBIDDEN_SELECTOR_TOKENS):
        _fail(path, "latest/default/fuzzy/nearest selection is forbidden")


def _validate_locator(value: Any, path: str) -> None:
    locator = _mapping(value, path)
    _exact_keys(locator, path, ("root",), ("relative_path", "locator_id"))
    root = _text(locator["root"], f"{path}.root")
    if root == "SOURCE_ROOT":
        relative = _text(locator.get("relative_path"), f"{path}.relative_path")
        if relative.startswith("/") or relative.startswith("\\") or ".." in relative.split("/"):
            _fail(f"{path}.relative_path", "must be a source-root-relative path without '..'")
        if "locator_id" in locator:
            _fail(path, "SOURCE_ROOT locator cannot also carry locator_id")
    elif root == "EXTERNAL_LOCATOR_ID":
        locator_id = _text(locator.get("locator_id"), f"{path}.locator_id")
        if locator_id.startswith(("/", "\\")) or ".." in locator_id.split("/"):
            _fail(f"{path}.locator_id", "must be a stable external locator id, not a filesystem path")
        if "relative_path" in locator:
            _fail(path, "EXTERNAL_LOCATOR_ID locator cannot also carry relative_path")
    else:
        _fail(f"{path}.root", "must be SOURCE_ROOT or EXTERNAL_LOCATOR_ID")


def _validate_reader(value: Any, path: str, source_format: str, source_sha256: str) -> None:
    reader = _mapping(value, path)
    _exact_keys(reader, path, ("decoder_owner", "configuration_ref"), ("encoding",))
    owner = _text(reader["decoder_owner"], f"{path}.decoder_owner")
    expected_owner = (
        "rawlsing_next.pre553_physical_decoder.decode_sav"
        if source_format == "SAV" else
        "rawlsing_next.pre553_physical_decoder.decode_dta"
    )
    if owner != expected_owner:
        _fail(f"{path}.decoder_owner", f"must be {expected_owner!r}")
    _exact_ref_value(reader["configuration_ref"], f"{path}.configuration_ref")
    encoding = reader.get("encoding")
    if encoding is None:
        return
    encoding_map = _mapping(encoding, f"{path}.encoding")
    _exact_keys(encoding_map, f"{path}.encoding", ("value", "sha256", "authority_status"))
    value = _text(encoding_map["value"], f"{path}.encoding.value")
    claimed_sha = _sha(encoding_map["sha256"], f"{path}.encoding.sha256")
    status = _text(encoding_map["authority_status"], f"{path}.encoding.authority_status")
    if claimed_sha != source_sha256:
        _fail(f"{path}.encoding.sha256", "must equal the original source SHA it configures")
    qualified = COMPATIBILITY_ALLOWLIST.get(source_sha256)
    if qualified is None:
        _fail(f"{path}.encoding", "source SHA is not in the exact decoder compatibility allowlist")
    if value != qualified:
        _fail(f"{path}.encoding.value", f"must be the allowlisted encoding {qualified!r}")
    if status != COMPATIBILITY_ONLY:
        _fail(f"{path}.encoding.authority_status", f"must be {COMPATIBILITY_ONLY!r}")


def _native_authority(value: Any, path: str) -> AuthoritySnapshot:
    payload = _native_keys(_mapping(value, path), AuthoritySnapshot, path)
    try:
        return AuthoritySnapshot(**payload)
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid AuthoritySnapshot: {exc}") from exc


def _native_universe(value: Any, path: str) -> EmpiricalUniverse:
    payload = _native_keys(_mapping(value, path), EmpiricalUniverse, path)
    try:
        return EmpiricalUniverse(**payload)
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid EmpiricalUniverse: {exc}") from exc


def _native_question(value: Any, path: str) -> QuestionVariableBinding:
    source = _mapping(value, path)
    allowed = {field.name for field in dataclass_fields(QuestionVariableBinding)}
    payload = {key: item for key, item in source.items() if key in allowed}
    extra = sorted(set(source) - allowed - {"question_id", "item_evidence"})
    if extra:
        _fail(path, f"keys are not fields of QuestionVariableBinding: {extra!r}")
    for name in ("empirical_universe_ref", "native_question_ref"):
        payload[name] = _exact_ref_value(payload[name], f"{path}.{name}")
    for name in ("canonical_question_ref_or_typed_absence", "component_subitem_ref_or_typed_absence"):
        if name in payload and isinstance(payload[name], Mapping) and "typed_absence_state" in payload[name]:
            payload[name] = _typed_absence_value(payload[name], f"{path}.{name}")
        elif name in payload and isinstance(payload[name], Mapping):
            payload[name] = _exact_ref_value(payload[name], f"{path}.{name}")
    for name in ("semantic_authority_ref", "topology_authority_ref"):
        if name in payload and isinstance(payload[name], Mapping):
            payload[name] = _authority_ref_value(payload[name], f"{path}.{name}")
    try:
        return QuestionVariableBinding(**payload)
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid QuestionVariableBinding: {exc}") from exc


def _native_source_relation(value: Any, path: str) -> SourceUniverseRelation:
    payload = _native_keys(_mapping(value, path), SourceUniverseRelation, path)
    try:
        return SourceUniverseRelation(**payload)
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid SourceUniverseRelation: {exc}") from exc


def _slot(value: Any, path: str) -> PhysicalSlot:
    payload = _mapping(value, path)
    _exact_keys(payload, path, ("ordinal", "name"))
    try:
        return PhysicalSlot(_integer(payload["ordinal"], f"{path}.ordinal", minimum=1), _text(payload["name"], f"{path}.name"))
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid PhysicalSlot: {exc}") from exc


def _occurrence(value: Any, path: str) -> OccurrenceRule:
    payload = _mapping(value, path)
    _exact_keys(payload, path, ("key", "topology_ref", "multiplicity_order_rank_fields"), ("component_ref",))
    component = payload.get("component_ref")
    if component is not None:
        component = _exact_ref_value(component, f"{path}.component_ref")
    try:
        return OccurrenceRule(
            _text(payload["key"], f"{path}.key"),
            _exact_ref_value(payload["topology_ref"], f"{path}.topology_ref"),
            _mapping(payload["multiplicity_order_rank_fields"], f"{path}.multiplicity_order_rank_fields"),
            component,
        )
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid OccurrenceRule: {exc}") from exc


def _validate_value_common(value: Any, path: str) -> Mapping[str, Any]:
    payload = _mapping(value, path)
    _exact_keys(
        payload, path,
        ("raw_value", "missing_state"),
        ("source_missing_declaration", "canonical_value", "transform_authority_ref",
         "extra_authority_refs", "occurrences", "coordinate_state", "response_state"),
    )
    missing_state = _text(payload["missing_state"], f"{path}.missing_state")
    if missing_state not in _MISSING_STATES:
        _fail(f"{path}.missing_state", f"unknown PhysicalMissingState {missing_state!r}")
    declaration = payload.get("source_missing_declaration")
    if declaration is not None:
        _mapping(declaration, f"{path}.source_missing_declaration")
    for name in ("extra_authority_refs",):
        if name in payload:
            _authority_ref_list(payload[name], f"{path}.{name}")
    transform = payload.get("transform_authority_ref")
    if transform is not None:
        _authority_ref_value(transform, f"{path}.transform_authority_ref")
    return payload


def _response_value_rule(value: Any, path: str) -> ResponseValueRule:
    payload = _validate_value_common(value, path)
    _exact_keys(
        payload, path,
        ("raw_value", "missing_state", "response_state", "occurrences"),
        ("source_missing_declaration", "canonical_value", "transform_authority_ref", "extra_authority_refs",
         "coordinate_state"),
    )
    state = _text(payload["response_state"], f"{path}.response_state")
    if state not in _RESPONSE_STATES:
        _fail(f"{path}.response_state", f"unknown RESPONSE_EVENT_STATE {state!r}")
    occurrences = tuple(_occurrence(item, f"{path}.occurrences[{index}]")
                        for index, item in enumerate(_sequence(payload["occurrences"], f"{path}.occurrences", nonempty=True)))
    transform = payload.get("transform_authority_ref")
    transform_ref = _authority_ref_value(transform, f"{path}.transform_authority_ref") if transform is not None else None
    extras = tuple(_authority_ref_value(x, f"{path}.extra_authority_refs[{i}]")
                   for i, x in enumerate(payload.get("extra_authority_refs") or ()))
    try:
        return ResponseValueRule(
            physical_key=physical_value_binding_key(
                payload["raw_value"],
                PhysicalMissingState(_text(payload["missing_state"], f"{path}.missing_state")),
                payload.get("source_missing_declaration"),
            ),
            response_state=state,
            occurrences=occurrences,
            canonical_value=payload.get("canonical_value"),
            transform_authority_ref=transform_ref,
            extra_authority_refs=extras,
        )
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid ResponseValueRule: {exc}") from exc


def _coordinate_value_rule(value: Any, path: str) -> CoordinateValueRule:
    payload = _validate_value_common(value, path)
    _exact_keys(
        payload, path,
        ("raw_value", "missing_state", "coordinate_state"),
        ("source_missing_declaration", "canonical_value", "extra_authority_refs", "response_state"),
    )
    state = _text(payload["coordinate_state"], f"{path}.coordinate_state")
    if state not in _COORDINATE_STATES:
        _fail(f"{path}.coordinate_state", f"unknown EMPIRICAL_COORDINATE_STATE {state!r}")
    extras = tuple(_authority_ref_value(x, f"{path}.extra_authority_refs[{i}]")
                   for i, x in enumerate(payload.get("extra_authority_refs") or ()))
    try:
        return CoordinateValueRule(
            physical_key=physical_value_binding_key(
                payload["raw_value"],
                PhysicalMissingState(_text(payload["missing_state"], f"{path}.missing_state")),
                payload.get("source_missing_declaration"),
            ),
            coordinate_state=state,
            canonical_value=payload.get("canonical_value"),
            extra_authority_refs=extras,
        )
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"{path}: invalid CoordinateValueRule: {exc}") from exc


def _weight_value_rule(value: Any, path: str) -> WeightValueRule:
    payload = _mapping(value, path)
    _exact_keys(payload, path, ("raw_value", "exact_value"), ("state", "source_missing_declaration", "missing_state"))
    state = _text(payload.get("state", "WEIGHT_VALID_AUTHORIZED"), f"{path}.state")
    if state not in _WEIGHT_STATES:
        _fail(f"{path}.state", f"unknown WEIGHT_MEASURE_STATE {state!r}")
    missing_state = _text(payload.get("missing_state", "OBSERVED_STORAGE_VALUE"), f"{path}.missing_state")
    if missing_state not in _MISSING_STATES:
        _fail(f"{path}.missing_state", f"unknown PhysicalMissingState {missing_state!r}")
    declaration = payload.get("source_missing_declaration")
    if declaration is not None:
        _mapping(declaration, f"{path}.source_missing_declaration")
    return WeightValueRule(
        physical_key=physical_value_binding_key(
            payload["raw_value"], PhysicalMissingState(missing_state), declaration),
        exact_value=payload["exact_value"],
        state=state,
    )


def _validate_slot_owner_sets(value: Any, path: str, slots: Mapping[tuple[int, str], PhysicalSlot],
                              authorities: Mapping[str, AuthorityRef]) -> None:
    owner_sets = _sequence(value, path)
    seen: set[tuple[int, str]] = set()
    for index, item in enumerate(owner_sets):
        item_path = f"{path}[{index}]"
        payload = _mapping(item, item_path)
        _exact_keys(payload, item_path, ("slot", "owners"), ("contract_id",))
        slot = _slot(payload["slot"], f"{item_path}.slot")
        if slot.key not in slots:
            _fail(f"{item_path}.slot", "owner set references a slot absent from physical_slots")
        if slot.key in seen:
            _fail(f"{item_path}.slot", "duplicate physical-slot owner set")
        seen.add(slot.key)
        owners = _sequence(payload["owners"], f"{item_path}.owners", nonempty=True)
        families: set[str] = set()
        for owner_index, owner in enumerate(owners):
            owner_path = f"{item_path}.owners[{owner_index}]"
            owner_payload = _mapping(owner, owner_path)
            _exact_keys(owner_payload, owner_path, ("owner_family", "authority_refs"))
            family = _text(owner_payload["owner_family"], f"{owner_path}.owner_family")
            if family not in _OWNER_FAMILIES:
                _fail(f"{owner_path}.owner_family", f"unsupported owner family {family!r}")
            if family in families:
                _fail(f"{owner_path}.owner_family", "duplicate owner family")
            families.add(family)
            refs = _authority_ref_list(owner_payload["authority_refs"], f"{owner_path}.authority_refs", nonempty=True)
            if not set(refs).issubset(authorities):
                _fail(f"{owner_path}.authority_refs", "owner authority is absent from authority.snapshots")


def _validate_coverage(value: Any, path: str, *, purpose: str, physical_total: int,
                       item_total: int, physical_slots: Sequence[Any], items: Sequence[Any]) -> None:
    coverage = _mapping(value, path)
    _exact_keys(
        coverage, path,
        ("physical_slots_total", "items_total"),
        ("physical_slots_included", "physical_slots_excluded", "items_included", "items_excluded",
         "partial_scope_reason", "not_a_lane_config"),
    )
    if _integer(coverage["physical_slots_total"], f"{path}.physical_slots_total") != physical_total:
        _fail(f"{path}.physical_slots_total", "must equal identity.source_column_count")
    if _integer(coverage["items_total"], f"{path}.items_total") != item_total:
        _fail(f"{path}.items_total", "must equal identity.original_item_count")
    if purpose == CONFIG_PURPOSE_SOURCE:
        included_slots = {_integer(x, f"{path}.physical_slots_included[{i}]", minimum=1)
                          for i, x in enumerate(_sequence(coverage.get("physical_slots_included", []),
                                                          f"{path}.physical_slots_included"))}
        excluded_slots = _sequence(coverage.get("physical_slots_excluded", []), f"{path}.physical_slots_excluded")
        excluded_ordinals: set[int] = set()
        for i, entry in enumerate(excluded_slots):
            entry_path = f"{path}.physical_slots_excluded[{i}]"
            payload = _mapping(entry, entry_path)
            _exact_keys(payload, entry_path, ("ordinal", "name", "reason"))
            excluded_ordinals.add(_integer(payload["ordinal"], f"{entry_path}.ordinal", minimum=1))
            _text(payload["name"], f"{entry_path}.name")
            _text(payload["reason"], f"{entry_path}.reason")
        if len(physical_slots) != physical_total:
            _fail("$.physical_slots", "SOURCE_PREPARATION must serialize every physical slot")
        serialized_ordinals = {_integer(x["ordinal"], "$.physical_slots[].ordinal", minimum=1) for x in physical_slots}
        if included_slots | excluded_ordinals != set(range(1, physical_total + 1)):
            _fail(f"{path}", "physical slots must be partitioned exactly into included/excluded")
        if included_slots & excluded_ordinals:
            _fail(f"{path}", "a physical slot cannot be both included and excluded")
        if serialized_ordinals != set(range(1, physical_total + 1)):
            _fail("$.physical_slots", "physical slot ordinals are not a complete 1..N set")

        included_items = {_text(x, f"{path}.items_included[{i}]")
                          for i, x in enumerate(_sequence(coverage.get("items_included", []), f"{path}.items_included"))}
        excluded_items = _sequence(coverage.get("items_excluded", []), f"{path}.items_excluded")
        excluded_ids: set[str] = set()
        for i, entry in enumerate(excluded_items):
            entry_path = f"{path}.items_excluded[{i}]"
            payload = _mapping(entry, entry_path)
            _exact_keys(payload, entry_path, ("implementation_id", "reason"))
            excluded_ids.add(_text(payload["implementation_id"], f"{entry_path}.implementation_id"))
            _text(payload["reason"], f"{entry_path}.reason")
        if len(items) != item_total:
            _fail("$.items", "SOURCE_PREPARATION must serialize every original item")
        serialized_ids = {_text(x["implementation_id"], "$.items[].implementation_id") for x in items}
        if included_items | excluded_ids != serialized_ids:
            _fail(f"{path}", "items_included/items_excluded must partition serialized original items")
        if included_items & excluded_ids:
            _fail(f"{path}", "an item cannot be both included and excluded")
    else:
        _text(coverage.get("partial_scope_reason"), f"{path}.partial_scope_reason")
        if "not_a_lane_config" in coverage:
            _boolean(coverage["not_a_lane_config"], f"{path}.not_a_lane_config")


def validate_source_config(document: Any) -> None:
    """Validate one serialized R157 source configuration.

    Raises ``SourceConfigurationSchemaError`` on the first closed-schema breach.
    """
    _check_no_private_paths(document)
    doc = _mapping(document, "$")
    _exact_keys(
        doc, "$",
        ("schema", "config_id", "config_revision", "config_purpose", "identity", "binding",
         "authority", "universe", "respondents", "questions", "physical_slots", "items",
         "response_slots", "coordinate_slots", "weight_slots", "routing",
         "source_relations", "replay", "supported_scope", "coverage", "residuals",
         "evidence", "runtime"),
        ("slot_owner_sets", "notes"),
    )
    if doc["schema"] != SCHEMA_ID:
        _fail("$.schema", f"must be {SCHEMA_ID!r}")
    _text(doc["config_id"], "$.config_id")
    _integer(doc["config_revision"], "$.config_revision", minimum=1)
    purpose = _text(doc["config_purpose"], "$.config_purpose")
    if purpose not in {CONFIG_PURPOSE_SOURCE, CONFIG_PURPOSE_FIXTURE, CONFIG_PURPOSE_EXAMPLE}:
        _fail("$.config_purpose", "unknown config purpose")

    identity = _mapping(doc["identity"], "$.identity")
    _exact_keys(
        identity, "$.identity",
        ("source_id", "family", "wave", "source_family_id", "study_product_id", "release_id",
         "instrument_release_id", "source_artifact_id", "expected_source_sha256", "source_format",
         "source_row_count", "source_column_count", "source_bytes", "codebook_rows",
         "original_item_count", "source_snapshot_retention_ref", "metadata_witness_ref",
         "locator", "reader"),
    )
    source_id = _text(identity["source_id"], "$.identity.source_id")
    if not _SOURCE_ID.match(source_id):
        _fail("$.identity.source_id", "must be SRC01..SRC35")
    for name in ("family", "wave", "source_family_id", "study_product_id", "release_id",
                 "instrument_release_id", "source_artifact_id"):
        text = _text(identity[name], f"$.identity.{name}")
        _assert_no_forbidden_selector(text, f"$.identity.{name}")
    source_sha = _sha(identity["expected_source_sha256"], "$.identity.expected_source_sha256")
    source_format = _text(identity["source_format"], "$.identity.source_format").upper()
    if source_format not in _ALLOWED_FORMATS:
        _fail("$.identity.source_format", "must be SAV or DTA")
    if identity["source_format"] != source_format:
        _fail("$.identity.source_format", "must be uppercase")
    for name in ("source_row_count", "source_column_count", "source_bytes", "codebook_rows", "original_item_count"):
        _integer(identity[name], f"$.identity.{name}", minimum=1)
    snapshot = _exact_ref_value(identity["source_snapshot_retention_ref"], "$.identity.source_snapshot_retention_ref")
    if snapshot.content_hash != source_sha:
        _fail("$.identity.source_snapshot_retention_ref.content_hash", "must equal expected_source_sha256")
    _exact_ref_value(identity["metadata_witness_ref"], "$.identity.metadata_witness_ref")
    _validate_locator(identity["locator"], "$.identity.locator")
    _validate_reader(identity["reader"], "$.identity.reader", source_format, source_sha)

    binding = _mapping(doc["binding"], "$.binding")
    _exact_keys(
        binding, "$.binding",
        ("identity_class", "source_sha256", "row_count", "source_snapshot_ref"),
        ("fixture_provenance",),
    )
    identity_class = _text(binding["identity_class"], "$.binding.identity_class")
    if identity_class not in {IDENTITY_CLASS_ORIGINAL, IDENTITY_CLASS_FIXTURE}:
        _fail("$.binding.identity_class", "unknown identity class")
    active_sha = _sha(binding["source_sha256"], "$.binding.source_sha256")
    active_rows = _integer(binding["row_count"], "$.binding.row_count", minimum=1)
    binding_snapshot = _exact_ref_value(binding["source_snapshot_ref"], "$.binding.source_snapshot_ref")
    if binding_snapshot.content_hash != active_sha:
        _fail("$.binding.source_snapshot_ref.content_hash", "must equal binding.source_sha256")
    fixture = binding.get("fixture_provenance")
    if identity_class == IDENTITY_CLASS_ORIGINAL:
        if purpose != CONFIG_PURPOSE_SOURCE:
            _fail("$.config_purpose", "ORIGINAL_SOURCE binding requires SOURCE_PREPARATION")
        if fixture is not None:
            _fail("$.binding.fixture_provenance", "original source binding cannot carry fixture provenance")
        if active_sha != source_sha:
            _fail("$.binding.source_sha256", "original binding must equal identity.expected_source_sha256")
        if active_rows != identity["source_row_count"]:
            _fail("$.binding.row_count", "original binding must equal identity.source_row_count")
    else:
        if purpose not in {CONFIG_PURPOSE_FIXTURE, CONFIG_PURPOSE_EXAMPLE}:
            _fail("$.config_purpose", "fixture binding requires NONRESPONDENT_FIXTURE or P0_EXAMPLE_FIXTURE")
        if active_sha == source_sha:
            _fail("$.binding.source_sha256", "fixture byte identity must be distinct from original source identity")
        fixture = _mapping(fixture, "$.binding.fixture_provenance")
        _exact_keys(
            fixture, "$.binding.fixture_provenance",
            ("fixture_id", "provenance", "authority_grade", "original_source_id",
             "original_source_sha256", "no_original_respondents", "fixture_study_product_id",
             "fixture_release_id", "fixture_instrument_release_id"),
        )
        _text(fixture["fixture_id"], "$.binding.fixture_provenance.fixture_id")
        _text(fixture["provenance"], "$.binding.fixture_provenance.provenance")
        if _text(fixture["authority_grade"], "$.binding.fixture_provenance.authority_grade") != "NONRESPONDENT_FIXTURE_ONLY":
            _fail("$.binding.fixture_provenance.authority_grade", "must be NONRESPONDENT_FIXTURE_ONLY")
        if _text(fixture["original_source_id"], "$.binding.fixture_provenance.original_source_id") != source_id:
            _fail("$.binding.fixture_provenance.original_source_id", "must equal identity.source_id")
        if _sha(fixture["original_source_sha256"], "$.binding.fixture_provenance.original_source_sha256") != source_sha:
            _fail("$.binding.fixture_provenance.original_source_sha256", "must equal identity.expected_source_sha256")
        if not _boolean(fixture["no_original_respondents"], "$.binding.fixture_provenance.no_original_respondents"):
            _fail("$.binding.fixture_provenance.no_original_respondents", "must be true")
        for name in ("fixture_study_product_id", "fixture_release_id", "fixture_instrument_release_id"):
            _text(fixture[name], f"$.binding.fixture_provenance.{name}")

    authority = _mapping(doc["authority"], "$.authority")
    _exact_keys(
        authority, "$.authority",
        ("snapshots", "required_refs", "projection_authority_ref", "replay_authority_ref",
         "projection_identity_ref", "tie_order_ref", "replay_protocol_version"),
    )
    snapshot_values = _sequence(authority["snapshots"], "$.authority.snapshots", nonempty=True)
    snapshots = tuple(_native_authority(value, f"$.authority.snapshots[{i}]")
                      for i, value in enumerate(snapshot_values))
    by_ref = {snap.authority_ref: snap for snap in snapshots}
    if len(by_ref) != len(snapshots):
        _fail("$.authority.snapshots", "duplicate authority snapshot ref")
    required = _authority_ref_list(authority["required_refs"], "$.authority.required_refs", nonempty=True)
    if not set(required).issubset(by_ref):
        _fail("$.authority.required_refs", "required authority is absent from snapshots")
    projection_auth = _authority_ref_value(authority["projection_authority_ref"], "$.authority.projection_authority_ref")
    replay_auth = _authority_ref_value(authority["replay_authority_ref"], "$.authority.replay_authority_ref")
    if projection_auth not in required or replay_auth not in required:
        _fail("$.authority.required_refs", "projection and replay authorities must be explicitly required")
    _exact_ref_value(authority["projection_identity_ref"], "$.authority.projection_identity_ref")
    _exact_ref_value(authority["tie_order_ref"], "$.authority.tie_order_ref")
    _text(authority["replay_protocol_version"], "$.authority.replay_protocol_version")
    for index, snap in enumerate(snapshots):
        scope = snap.scope_envelope
        fixture_only = isinstance(scope, Mapping) and scope.get("fixture_only") is True
        grade = str(scope.get("grade", "")) if isinstance(scope, Mapping) else ""
        if identity_class == IDENTITY_CLASS_FIXTURE:
            if not fixture_only or grade != "NONRESPONDENT_FIXTURE_ONLY":
                _fail(f"$.authority.snapshots[{index}]", "fixture configs require fixture-only authority snapshots")
        else:
            if fixture_only or "FIXTURE" in grade.upper() or "TEST_ONLY" in grade.upper():
                _fail(f"$.authority.snapshots[{index}]", "original config cannot use fixture/test-only authority")

    universe = _mapping(doc["universe"], "$.universe")
    _exact_keys(universe, "$.universe", ("universes",))
    universe_values = _sequence(universe["universes"], "$.universe.universes", nonempty=True)
    universes = tuple(_native_universe(value, f"$.universe.universes[{i}]")
                      for i, value in enumerate(universe_values))
    universe_by_key = {x.ref.key: x for x in universes}
    if len(universe_by_key) != len(universes):
        _fail("$.universe.universes", "duplicate EmpiricalUniverse ref")
    for index, item in enumerate(universes):
        for name in ("country_geography", "sampling_geography", "target_population_and_sample_frame",
                     "sampling_design_regime"):
            rendered = str(getattr(item, name)).upper()
            if identity_class == IDENTITY_CLASS_ORIGINAL:
                if rendered in {"ZZ", "ZZ-SYNTHETIC"} or any(token in rendered for token in _SYNTHETIC_TOKENS):
                    _fail(f"$.universe.universes[{index}].{name}", "synthetic/default universe metadata is forbidden")
            else:
                if "FIXTURE" not in rendered and "NONRESPONDENT" not in rendered:
                    _fail(f"$.universe.universes[{index}].{name}", "fixture universe must identify its fixture provenance")

    respondents = _mapping(doc["respondents"], "$.respondents")
    _exact_keys(
        respondents, "$.respondents",
        ("subject_unit", "respondent_namespace", "respondent_key_pattern"),
        ("source_native_key_slot", "identity_map_authority_ref", "row_identity_grade"),
    )
    _text(respondents["subject_unit"], "$.respondents.subject_unit")
    _text(respondents["respondent_namespace"], "$.respondents.respondent_namespace")
    pattern = _text(respondents["respondent_key_pattern"], "$.respondents.respondent_key_pattern")
    if "{row_ordinal" not in pattern:
        _fail("$.respondents.respondent_key_pattern", "must contain a {row_ordinal...} placeholder")
    try:
        pattern.format(row_ordinal=1)
    except Exception as exc:
        raise SourceConfigurationSchemaError(f"$.respondents.respondent_key_pattern: {exc}") from exc
    native_key_slot = respondents.get("source_native_key_slot")
    if native_key_slot is not None:
        _slot(native_key_slot, "$.respondents.source_native_key_slot")
    identity_map = respondents.get("identity_map_authority_ref")
    if identity_map is not None:
        ref = _authority_ref_value(identity_map, "$.respondents.identity_map_authority_ref")
        if ref not in by_ref:
            _fail("$.respondents.identity_map_authority_ref", "absent from authority.snapshots")

    question_values = _sequence(doc["questions"], "$.questions", nonempty=True)
    questions = []
    for index, value in enumerate(question_values):
        path = f"$.questions[{index}]"
        payload = _mapping(value, path)
        _exact_keys(
            payload, path,
            ("question_id", "empirical_universe_ref", "native_question_ref",
             "instrument_question_version", "canonical_question_ref_or_typed_absence",
             "component_subitem_ref_or_typed_absence", "semantic_authority_ref",
             "topology_authority_ref"),
            ("item_evidence",),
        )
        _text(payload["question_id"], f"{path}.question_id")
        question = _native_question(payload, path)
        if question.empirical_universe_ref.key not in universe_by_key:
            _fail(f"{path}.empirical_universe_ref", "unknown universe")
        for name in ("semantic_authority_ref", "topology_authority_ref"):
            if getattr(question, name) not in by_ref:
                _fail(f"{path}.{name}", "absent from authority.snapshots")
        questions.append((payload["question_id"], question))
    if len({key for key, _ in questions}) != len(questions):
        _fail("$.questions", "duplicate question_id")
    question_by_id = dict(questions)
    native_question_keys = {(q.empirical_universe_ref.key, q.native_question_ref.key) for _, q in questions}
    if len(native_question_keys) != len(questions):
        _fail("$.questions", "duplicate empirical-universe/native-question binding")

    physical_values = _sequence(doc["physical_slots"], "$.physical_slots", nonempty=True)
    physical_slots: list[Mapping[str, Any]] = []
    slot_by_key: dict[tuple[int, str], PhysicalSlot] = {}
    for index, value in enumerate(physical_values):
        path = f"$.physical_slots[{index}]"
        payload = _mapping(value, path)
        _exact_keys(
            payload, path,
            ("ordinal", "name", "label", "storage_type", "original_type", "storage_width",
             "measure", "value_labels", "missing_declarations", "mr_declarations",
             "codebook_mapping", "disposition"),
            ("disposition_reason",),
        )
        slot = _slot({"ordinal": payload["ordinal"], "name": payload["name"]}, path)
        if slot.key in slot_by_key:
            _fail(path, "duplicate physical slot ordinal/name")
        slot_by_key[slot.key] = slot
        _optional_text(payload["label"], f"{path}.label")
        _optional_text(payload["storage_type"], f"{path}.storage_type")
        _optional_text(payload["original_type"], f"{path}.original_type")
        _optional_text(payload["storage_width"], f"{path}.storage_width")
        _optional_text(payload["measure"], f"{path}.measure")
        for name in ("value_labels", "missing_declarations", "mr_declarations"):
            if payload[name] is not None and not isinstance(payload[name], (Mapping, list)):
                _fail(f"{path}.{name}", "must be an object, array, or null")
        mapping = _mapping(payload["codebook_mapping"], f"{path}.codebook_mapping")
        _exact_keys(mapping, f"{path}.codebook_mapping", ("var_name", "row_hash", "status"))
        _text(mapping["var_name"], f"{path}.codebook_mapping.var_name")
        _optional_text(mapping["row_hash"], f"{path}.codebook_mapping.row_hash")
        _text(mapping["status"], f"{path}.codebook_mapping.status")
        _text(payload["disposition"], f"{path}.disposition")
        physical_slots.append(payload)

    item_values = _sequence(doc["items"], "$.items", nonempty=True)
    items: list[Mapping[str, Any]] = []
    item_ids: set[str] = set()
    for index, value in enumerate(item_values):
        path = f"$.items[{index}]"
        payload = _mapping(value, path)
        _exact_keys(
            payload, path,
            ("implementation_id", "source_variable_code", "exact_identity_sha256",
             "question_text", "disposition", "response_classes", "mapping_status",
             "authority_status", "evidence_refs", "limits"),
            ("relation", "item_id"),
        )
        implementation_id = _text(payload["implementation_id"], f"{path}.implementation_id")
        if implementation_id in item_ids:
            _fail(path, "duplicate implementation_id")
        item_ids.add(implementation_id)
        _text(payload["source_variable_code"], f"{path}.source_variable_code")
        _sha(payload["exact_identity_sha256"], f"{path}.exact_identity_sha256")
        _text(payload["question_text"], f"{path}.question_text")
        _text(payload["disposition"], f"{path}.disposition")
        _text(payload["response_classes"], f"{path}.response_classes")
        _text(payload["mapping_status"], f"{path}.mapping_status")
        _text(payload["authority_status"], f"{path}.authority_status")
        _ref_list(payload["evidence_refs"], f"{path}.evidence_refs")
        _sequence(payload["limits"], f"{path}.limits")
        relation = payload.get("relation")
        if relation is not None:
            relation = _mapping(relation, f"{path}.relation")
            _exact_keys(
                relation, f"{path}.relation",
                ("status", "question_id", "mapping_status", "manual_response_topology",
                 "manual_response_normalization_rule", "manual_position_conditioning",
                 "manual_semantic_role", "manual_signed_polarity_status",
                 "forbidden_inference", "does_not_measure", "governed_row_payload_hash"),
                ("p2_exact_identity_sha256", "unmatched_witness"),
            )
            for name in ("status", "mapping_status", "manual_response_topology",
                         "manual_response_normalization_rule", "manual_position_conditioning",
                         "manual_semantic_role", "manual_signed_polarity_status",
                         "forbidden_inference", "does_not_measure"):
                _text(relation[name], f"{path}.relation.{name}")
            _text(relation["question_id"], f"{path}.relation.question_id")
            _optional_text(relation["governed_row_payload_hash"], f"{path}.relation.governed_row_payload_hash")
        items.append(payload)

    response_slots = []
    for index, value in enumerate(_sequence(doc["response_slots"], "$.response_slots")):
        path = f"$.response_slots[{index}]"
        payload = _mapping(value, path)
        _exact_keys(
            payload, path,
            ("slot", "question_id", "values"),
            ("slot_owner_authorities",),
        )
        slot = _slot(payload["slot"], f"{path}.slot")
        if slot.key not in slot_by_key:
            _fail(f"{path}.slot", "unknown physical slot")
        question_id = _text(payload["question_id"], f"{path}.question_id")
        if question_id not in question_by_id:
            _fail(f"{path}.question_id", "unknown question")
        values = tuple(_response_value_rule(item, f"{path}.values[{i}]")
                       for i, item in enumerate(_sequence(payload["values"], f"{path}.values", nonempty=True)))
        if len({x.physical_key for x in values}) != len(values):
            _fail(f"{path}.values", "duplicate physical value binding")
        owner_auths = ()
        if "slot_owner_authorities" in payload:
            owner_auths = tuple(
                PhysicalSlotOwnerAuthorization(
                    _text(_mapping(item, f"{path}.slot_owner_authorities[{i}]").get("owner_family"),
                          f"{path}.slot_owner_authorities[{i}].owner_family"),
                    _authority_ref_list(
                        _mapping(item, f"{path}.slot_owner_authorities[{i}]")["authority_refs"],
                        f"{path}.slot_owner_authorities[{i}].authority_refs", nonempty=True),
                )
                for i, item in enumerate(_sequence(payload["slot_owner_authorities"],
                                                   f"{path}.slot_owner_authorities"))
            )
        response_slots.append(ResponseSlotRule(slot, question_by_id[question_id], values))

    coordinate_slots = []
    for index, value in enumerate(_sequence(doc["coordinate_slots"], "$.coordinate_slots")):
        path = f"$.coordinate_slots[{index}]"
        payload = _mapping(value, path)
        _exact_keys(
            payload, path,
            ("slot", "native_coordinate_ref", "unit_taxonomy_ref", "effective_time",
             "source_semantic_authority_ref"),
            ("canonical_coordinate_ref", "normalization_ref", "values", "copy_observed_raw",
             "slot_owner_authorities"),
        )
        slot = _slot(payload["slot"], f"{path}.slot")
        if slot.key not in slot_by_key:
            _fail(f"{path}.slot", "unknown physical slot")
        source_auth = _authority_ref_value(payload["source_semantic_authority_ref"],
                                           f"{path}.source_semantic_authority_ref")
        if source_auth not in by_ref:
            _fail(f"{path}.source_semantic_authority_ref", "absent from authority.snapshots")
        canonical = payload.get("canonical_coordinate_ref")
        if canonical is not None:
            _exact_ref_value(canonical, f"{path}.canonical_coordinate_ref")
        normalization = payload.get("normalization_ref")
        if normalization is not None:
            if isinstance(normalization, Mapping) and "typed_absence_state" in normalization:
                _typed_absence_value(normalization, f"{path}.normalization_ref")
            elif isinstance(normalization, Mapping) and "authority_id" in normalization:
                _authority_ref_value(normalization, f"{path}.normalization_ref")
            else:
                _exact_ref_value(normalization, f"{path}.normalization_ref")
        values = tuple(_coordinate_value_rule(item, f"{path}.values[{i}]")
                       for i, item in enumerate(_sequence(payload.get("values", []), f"{path}.values")))
        coordinate_slots.append(CoordinateSlotRule(
            slot=slot,
            native_coordinate_ref=_exact_ref_value(payload["native_coordinate_ref"], f"{path}.native_coordinate_ref"),
            unit_taxonomy_ref=_exact_ref_value(payload["unit_taxonomy_ref"], f"{path}.unit_taxonomy_ref"),
            effective_time=payload["effective_time"],
            source_semantic_authority_ref=source_auth,
            canonical_coordinate_ref=canonical,
            normalization_ref=normalization,
            values=values,
            copy_observed_raw=_boolean(payload.get("copy_observed_raw", False), f"{path}.copy_observed_raw"),
        ))

    weight_slots = []
    for index, value in enumerate(_sequence(doc["weight_slots"], "$.weight_slots")):
        path = f"$.weight_slots[{index}]"
        payload = _mapping(value, path)
        _exact_keys(
            payload, path,
            ("slot", "weight_basis_id", "weight_source_ref", "design_authority_ref",
             "estimand_authority_ref", "effective_scope_ref"),
            ("normalization_ref", "values", "copy_observed_numeric", "extra_authority_refs",
             "slot_owner_authorities"),
        )
        slot = _slot(payload["slot"], f"{path}.slot")
        if slot.key not in slot_by_key:
            _fail(f"{path}.slot", "unknown physical slot")
        design = _authority_ref_value(payload["design_authority_ref"], f"{path}.design_authority_ref")
        estimand = _authority_ref_value(payload["estimand_authority_ref"], f"{path}.estimand_authority_ref")
        if design not in by_ref or estimand not in by_ref:
            _fail(f"{path}", "weight design/estimand authority absent from authority.snapshots")
        extras = tuple(_authority_ref_value(x, f"{path}.extra_authority_refs[{i}]")
                       for i, x in enumerate(payload.get("extra_authority_refs") or ()))
        values = tuple(_weight_value_rule(item, f"{path}.values[{i}]")
                       for i, item in enumerate(_sequence(payload.get("values", []), f"{path}.values")))
        normalization = payload.get("normalization_ref")
        if normalization is not None:
            if isinstance(normalization, Mapping) and "typed_absence_state" in normalization:
                normalization = _typed_absence_value(normalization, f"{path}.normalization_ref")
            elif isinstance(normalization, Mapping) and "authority_id" in normalization:
                normalization = _authority_ref_value(normalization, f"{path}.normalization_ref")
            else:
                normalization = _exact_ref_value(normalization, f"{path}.normalization_ref")
        weight_slots.append(WeightSlotRule(
            slot=slot,
            weight_basis_id=_text(payload["weight_basis_id"], f"{path}.weight_basis_id"),
            weight_source_ref=_exact_ref_value(payload["weight_source_ref"], f"{path}.weight_source_ref"),
            design_authority_ref=design,
            estimand_authority_ref=estimand,
            effective_scope_ref=_exact_ref_value(payload["effective_scope_ref"], f"{path}.effective_scope_ref"),
            normalization_ref=normalization,
            values=values,
            copy_observed_numeric=_boolean(payload.get("copy_observed_numeric", False),
                                          f"{path}.copy_observed_numeric"),
            extra_authority_refs=extras,
        ))

    routing = []
    for index, value in enumerate(_sequence(doc["routing"], "$.routing", nonempty=True)):
        path = f"$.routing[{index}]"
        payload = _mapping(value, path)
        _exact_keys(
            payload, path,
            ("question_id", "row_selector", "typed_state", "risk_set_ref", "routing_rule_ref",
             "member_set_replay_ref", "authority_ref"),
            ("parent_predicate_refs", "dependency_refs", "replay_root"),
        )
        question_id = _text(payload["question_id"], f"{path}.question_id")
        if question_id not in question_by_id:
            _fail(f"{path}.question_id", "unknown question")
        selector = payload["row_selector"]
        if selector != "ALL":
            for i, row in enumerate(_sequence(selector, f"{path}.row_selector", nonempty=True)):
                _integer(row, f"{path}.row_selector[{i}]", minimum=1)
        state = _text(payload["typed_state"], f"{path}.typed_state")
        if state not in _ROUTING_STATES:
            _fail(f"{path}.typed_state", f"unknown ROUTING_ELIGIBILITY_STATE {state!r}")
        authority_ref_value = _authority_ref_value(payload["authority_ref"], f"{path}.authority_ref")
        if authority_ref_value not in by_ref:
            _fail(f"{path}.authority_ref", "absent from authority.snapshots")
        _exact_ref_value(payload["risk_set_ref"], f"{path}.risk_set_ref")
        _exact_ref_value(payload["routing_rule_ref"], f"{path}.routing_rule_ref")
        _exact_ref_value(payload["member_set_replay_ref"], f"{path}.member_set_replay_ref")
        for name in ("parent_predicate_refs", "dependency_refs"):
            if name in payload:
                _ref_list(payload[name], f"{path}.{name}")
        if "replay_root" in payload:
            _exact_ref_value(payload["replay_root"], f"{path}.replay_root")
        routing.append(payload)

    _validate_slot_owner_sets(doc.get("slot_owner_sets", []), "$.slot_owner_sets",
                              slot_by_key, by_ref)
    source_relations = _mapping(doc["source_relations"], "$.source_relations")
    _exact_keys(source_relations, "$.source_relations", (), ("typed_absence_state", "relations"))
    if ("typed_absence_state" in source_relations) == ("relations" in source_relations):
        _fail("$.source_relations", "must carry exactly one of typed_absence_state or relations")
    if "typed_absence_state" in source_relations and \
            source_relations["typed_absence_state"] != "DISTINCT_BY_DEFAULT":
        _fail("$.source_relations.typed_absence_state", "must be DISTINCT_BY_DEFAULT")
    for index, value in enumerate(_sequence(source_relations.get("relations", []), "$.source_relations.relations")):
        relation = _native_source_relation(value, f"$.source_relations.relations[{index}]")
        for ref in relation.source_universe_refs:
            if ref.key not in universe_by_key:
                _fail(f"$.source_relations.relations[{index}].source_universe_refs", "unknown universe")

    replay = _mapping(doc["replay"], "$.replay")
    _exact_keys(replay, "$.replay", ("predicate", "comparator", "discovery", "structural"))
    for name in ("predicate", "comparator", "discovery", "structural"):
        absence = _typed_absence_value(replay[name], f"$.replay.{name}")
        allowed = {
            "predicate": {"NOT_APPLICABLE", "DEFERRED"},
            "comparator": {"DEFERRED"},
            "discovery": {"DEFERRED"},
            "structural": {"NOT_APPLICABLE"},
        }[name]
        if absence.state not in allowed:
            _fail(f"$.replay.{name}", f"state must be one of {sorted(allowed)!r}; P0 does not freeze replay payloads")

    supported = _mapping(doc["supported_scope"], "$.supported_scope")
    _exact_keys(
        supported, "$.supported_scope",
        ("scope_id", "purpose", "declared_supported", "supported_question_ids",
         "native_validation_expectation", "original_source_execution"),
        ("supported_unit_slice", "supported_form_slice", "notes"),
    )
    _text(supported["scope_id"], "$.supported_scope.scope_id")
    purpose_value = _text(supported["purpose"], "$.supported_scope.purpose")
    _boolean(supported["declared_supported"], "$.supported_scope.declared_supported")
    question_ids = {_text(x, f"$.supported_scope.supported_question_ids[{i}]")
                    for i, x in enumerate(_sequence(supported["supported_question_ids"],
                                                    "$.supported_scope.supported_question_ids"))}
    if not question_ids.issubset(question_by_id):
        _fail("$.supported_scope.supported_question_ids", "contains unknown question_id")
    expectation = _text(supported["native_validation_expectation"],
                        "$.supported_scope.native_validation_expectation")
    if expectation not in {"POSITIVE_RELEASE", "REFUSAL", "NOT_RUN"}:
        _fail("$.supported_scope.native_validation_expectation", "unknown expectation")
    if _text(supported["original_source_execution"], "$.supported_scope.original_source_execution") != \
            "NOT_PERFORMED_UNDER_R157_PREPARATION":
        _fail("$.supported_scope.original_source_execution", "must remain NOT_PERFORMED_UNDER_R157_PREPARATION")
    if purpose == CONFIG_PURPOSE_SOURCE and purpose_value != "SOURCE_PREPARATION":
        _fail("$.supported_scope.purpose", "SOURCE_PREPARATION config must declare purpose SOURCE_PREPARATION")
    if purpose == CONFIG_PURPOSE_EXAMPLE and purpose_value != "P0_EXAMPLE_ONLY":
        _fail("$.supported_scope.purpose", "P0 example must declare purpose P0_EXAMPLE_ONLY")
    if purpose == CONFIG_PURPOSE_FIXTURE and purpose_value != "NONRESPONDENT_FIXTURE_VALIDATION":
        _fail("$.supported_scope.purpose", "fixture config must declare NONRESPONDENT_FIXTURE_VALIDATION")
    for name in ("supported_unit_slice", "supported_form_slice"):
        if name in supported:
            _text(supported[name], f"$.supported_scope.{name}")
    if "notes" in supported:
        for i, note in enumerate(_sequence(supported["notes"], "$.supported_scope.notes")):
            _text(note, f"$.supported_scope.notes[{i}]")

    _validate_coverage(
        doc["coverage"], "$.coverage", purpose=purpose,
        physical_total=identity["source_column_count"],
        item_total=identity["original_item_count"],
        physical_slots=physical_slots, items=items,
    )

    residuals = _sequence(doc["residuals"], "$.residuals")
    for index, value in enumerate(residuals):
        path = f"$.residuals[{index}]"
        payload = _mapping(value, path)
        _exact_keys(
            payload, path,
            ("residual_id", "scope", "field", "status", "reason", "dependent_operation",
             "unaffected_scope", "owner", "next_step"),
        )
        for name in ("residual_id", "scope", "field", "status", "reason", "dependent_operation",
                     "unaffected_scope", "owner", "next_step"):
            _text(payload[name], f"{path}.{name}")

    evidence = _mapping(doc["evidence"], "$.evidence")
    _exact_keys(
        evidence, "$.evidence",
        ("source_roster_path", "item_index_path", "evidence_manifest_path",
         "pinned_inputs", "field_evidence", "limits"),
    )
    for name in ("source_roster_path", "item_index_path", "evidence_manifest_path"):
        path_value = _text(evidence[name], f"$.evidence.{name}")
        if path_value.startswith("/") or ".." in path_value.split("/"):
            _fail(f"$.evidence.{name}", "must be a repository-relative path")
    for index, value in enumerate(_sequence(evidence["pinned_inputs"], "$.evidence.pinned_inputs")):
        path = f"$.evidence.pinned_inputs[{index}]"
        payload = _mapping(value, path)
        _exact_keys(payload, path, ("kind",), ("sha256", "commit", "path", "bytes", "locator"))
        _text(payload["kind"], f"{path}.kind")
        if "sha256" not in payload and "commit" not in payload:
            _fail(path, "a pinned input requires sha256 or commit identity")
        if "sha256" in payload:
            _sha(payload["sha256"], f"{path}.sha256")
        for name in ("commit", "path", "locator"):
            if name in payload:
                _text(payload[name], f"{path}.{name}")
        if "bytes" in payload:
            _integer(payload["bytes"], f"{path}.bytes", minimum=1)
    for index, value in enumerate(_sequence(evidence["field_evidence"], "$.evidence.field_evidence")):
        path = f"$.evidence.field_evidence[{index}]"
        payload = _mapping(value, path)
        _exact_keys(payload, path, ("field", "refs"))
        _text(payload["field"], f"{path}.field")
        _ref_list(payload["refs"], f"{path}.refs")
    for index, value in enumerate(_sequence(evidence["limits"], "$.evidence.limits")):
        _text(value, f"$.evidence.limits[{index}]")

    runtime = _mapping(doc["runtime"], "$.runtime")
    _exact_keys(
        runtime, "$.runtime",
        ("projection_builder", "release_builder", "repository_builder", "native_owner",
         "native_validator_stream", "native_validator_incidence", "source_read_owner",
         "transport", "reader_encoding_transport"),
    )
    for name, expected in _RUNTIME_CALLABLES.items():
        actual = _text(runtime[name], f"$.runtime.{name}")
        historical = _HISTORICAL_RUNTIME_CALLABLES[name]
        if actual not in {expected, historical}:
            _fail(
                f"$.runtime.{name}",
                f"must be {expected!r} or the exact historical owner {historical!r}; "
                "no replacement engine is permitted",
            )
    transports = {_text(x, f"$.runtime.transport[{i}]")
                  for i, x in enumerate(_sequence(runtime["transport"], "$.runtime.transport", nonempty=True))}
    if not transports.issubset({"ExactPhysicalCellStream", "PhysicalSourceIncidence"}):
        _fail("$.runtime.transport", "unsupported transport; use the existing C11 owners")
    _text(runtime["reader_encoding_transport"], "$.runtime.reader_encoding_transport")

    if "notes" in doc:
        for index, note in enumerate(_sequence(doc["notes"], "$.notes")):
            _text(note, f"$.notes[{index}]")

    # Bind the serialized question ids to the actual native questions.
    if set(question_by_id) != {qid for qid, _ in questions}:
        _fail("$.questions", "internal question binding mismatch")


# ---------------------------------------------------------------------------
# Historical schema.py -- public schema surface.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceConfig:
    """Validated, serialized source configuration.

    ``document`` is the exact JSON-shaped config.  Native objects are
    reconstructed by the factory, never cached as pre-invented witnesses.
    """

    document: Mapping[str, Any]
    path: Path | None = None

    def __post_init__(self) -> None:
        validate_source_config(self.document)

    @property
    def config_id(self) -> str:
        return self.document["config_id"]

    @property
    def source_id(self) -> str:
        return self.document["identity"]["source_id"]

    @property
    def config_purpose(self) -> str:
        return self.document["config_purpose"]

    @property
    def identity_class(self) -> str:
        return self.document["binding"]["identity_class"]

    @property
    def active_source_sha256(self) -> str:
        return self.document["binding"]["source_sha256"]

    @property
    def active_row_count(self) -> int:
        return self.document["binding"]["row_count"]

    @property
    def original_source_sha256(self) -> str:
        return self.document["identity"]["expected_source_sha256"]

    @property
    def fixture_provenance(self) -> Mapping[str, Any] | None:
        return self.document["binding"].get("fixture_provenance")

    def to_dict(self) -> dict[str, Any]:
        return deepcopy(dict(self.document))


def load_source_config(path: str | Path) -> SourceConfig:
    """Load and validate a JSON source configuration from *path*."""
    path = Path(path)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"cannot read source configuration {path}: {exc}") from exc
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"source configuration {path} is not valid UTF-8 JSON: {exc}") from exc
    return SourceConfig(document, path=path)


def canonical_config_hash(config: SourceConfig | Mapping[str, Any]) -> str:
    """Deterministic SHA-256 of the JSON-shaped config (not a native object hash)."""
    document = config.document if isinstance(config, SourceConfig) else config
    material = json.dumps(
        document, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def config_file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

"""Externally authenticated source-read admission before R04 response decode.

This module is transport only. It creates no source right, issuer, current grant,
or scientific permission. A trusted deployment resolver authenticates the
supplied exact decision; fixture resolvers only exercise call order.
"""

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    COMPATIBILITY_ONLY,
    PhysicalSourceIncidence,
    decode_dta,
    decode_sav,
)


def _admission_sha(value: Any, name: str) -> str:
    if (not isinstance(value, str) or len(value) != 64 or value.lower() != value
            or any(ch not in "0123456789abcdef" for ch in value)):
        raise SourceReadAdmissionRefusal("SOURCE_READ_SHA_REQUIRED", name)
    return value


def _admission_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceReadAdmissionRefusal("SOURCE_READ_FIELD_REQUIRED", name)
    return value


def _admission_refs(value: Any, name: str) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or not value:
        raise SourceReadAdmissionRefusal("SOURCE_READ_REFS_REQUIRED", name)
    try:
        return tuple(sorted((exact_ref(item, name) for item in value), key=lambda ref: ref.key))
    except Exception as exc:
        raise SourceReadAdmissionRefusal("SOURCE_READ_REFS_INVALID", name) from exc


@dataclass(frozen=True)
class SourceReadRequest:
    """Metadata-only request; it contains no decoded response capability."""

    source_id: str
    source_sha256: str
    source_format: str
    custody_locator_binding: str
    host: str
    purpose: str
    consumer_use: str
    read_operation: str = SOURCE_RESPONSE_DECODE
    physical_read_extent: str = EXACT_FILE
    metadata_freeze_refs: tuple[ExactRef, ...] = ()
    semantic_use_scope: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _admission_text(self.source_id, "source_id")
        _admission_sha(self.source_sha256, "source_sha256")
        if not isinstance(self.source_format, str) or self.source_format.upper() not in SOURCE_FORMATS:
            raise SourceReadAdmissionRefusal("SOURCE_READ_FORMAT_REQUIRED", self.source_format)
        object.__setattr__(self, "source_format", self.source_format.upper())
        for name in ("custody_locator_binding", "host", "purpose", "consumer_use"):
            _admission_text(getattr(self, name), name)
        if self.read_operation != SOURCE_RESPONSE_DECODE:
            raise SourceReadAdmissionRefusal("SOURCE_READ_OPERATION_UNSUPPORTED", self.read_operation)
        if self.physical_read_extent != EXACT_FILE:
            raise SourceReadAdmissionRefusal("SOURCE_READ_EXTENT_UNSUPPORTED", self.physical_read_extent)
        object.__setattr__(self, "metadata_freeze_refs", _admission_refs(
            self.metadata_freeze_refs, "metadata_freeze_refs"))
        if (isinstance(self.semantic_use_scope, (str, bytes))
                or not isinstance(self.semantic_use_scope, Sequence)
                or not self.semantic_use_scope
                or any(not isinstance(item, str) or not item.strip()
                       for item in self.semantic_use_scope)):
            raise SourceReadAdmissionRefusal("SOURCE_READ_SEMANTIC_SCOPE_REQUIRED")
        object.__setattr__(self, "semantic_use_scope", tuple(sorted(set(self.semantic_use_scope))))


@dataclass(frozen=True)
class IssuedSourceReadDecision:
    """External issuer read result; construction here does not authenticate it."""

    decision_ref: ExactRef
    source_permission_refs: tuple[ExactRef, ...]
    source_id: str
    source_sha256: str
    source_format: str
    custody_locator_binding: str
    host: str
    purpose: str
    consumer_use: str
    read_operation: str
    physical_read_extent: str
    metadata_freeze_refs: tuple[ExactRef, ...]
    semantic_use_scope: tuple[str, ...]
    effective_interval: str
    currentness: str
    revocation_ref: ExactRef | None
    retention_export_limits: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_ref", exact_ref(self.decision_ref, "decision_ref"))
        object.__setattr__(self, "source_permission_refs", _admission_refs(
            self.source_permission_refs, "source_permission_refs"))
        _admission_text(self.source_id, "source_id")
        _admission_sha(self.source_sha256, "source_sha256")
        if not isinstance(self.source_format, str) or self.source_format.upper() not in SOURCE_FORMATS:
            raise SourceReadAdmissionRefusal("SOURCE_READ_FORMAT_REQUIRED", self.source_format)
        object.__setattr__(self, "source_format", self.source_format.upper())
        for name in ("custody_locator_binding", "host", "purpose", "consumer_use",
                     "read_operation", "physical_read_extent", "effective_interval",
                     "currentness"):
            _admission_text(getattr(self, name), name)
        if self.read_operation != SOURCE_RESPONSE_DECODE:
            raise SourceReadAdmissionRefusal("SOURCE_READ_OPERATION_UNSUPPORTED", self.read_operation)
        if self.physical_read_extent != EXACT_FILE:
            raise SourceReadAdmissionRefusal("SOURCE_READ_EXTENT_UNSUPPORTED", self.physical_read_extent)
        object.__setattr__(self, "metadata_freeze_refs", _admission_refs(
            self.metadata_freeze_refs, "metadata_freeze_refs"))
        if (isinstance(self.semantic_use_scope, (str, bytes))
                or not isinstance(self.semantic_use_scope, Sequence)
                or not self.semantic_use_scope
                or any(not isinstance(item, str) or not item.strip()
                       for item in self.semantic_use_scope)):
            raise SourceReadAdmissionRefusal("SOURCE_READ_SEMANTIC_SCOPE_REQUIRED")
        object.__setattr__(self, "semantic_use_scope", tuple(sorted(set(self.semantic_use_scope))))
        if self.revocation_ref is not None:
            object.__setattr__(self, "revocation_ref", exact_ref(self.revocation_ref, "revocation_ref"))
        if not isinstance(self.retention_export_limits, Mapping):
            raise SourceReadAdmissionRefusal("SOURCE_READ_LIMITS_REQUIRED")


@dataclass(frozen=True)
class SourceReaderConfiguration:
    """Qualified exact-SHA reader configuration supplied before source I/O.

    The object carries no source right.  It only proves that an encoding choice
    is the exact allowlisted choice for the request's source SHA, or that no
    override is requested.
    """

    source_sha256: str
    encoding: str | None = None
    authority_status: str | None = None
    configuration_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        _admission_sha(self.source_sha256, "source_sha256")
        if self.configuration_ref is not None:
            object.__setattr__(
                self, "configuration_ref",
                exact_ref(self.configuration_ref, "configuration_ref"))
        if self.encoding in ("auto", "guess", "fallback"):
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_ENCODING_GUESS_FORBIDDEN", str(self.encoding))
        if self.encoding is None:
            if self.authority_status is not None:
                raise SourceReadAdmissionRefusal(
                    "SOURCE_READ_ENCODING_STATUS_WITHOUT_ENCODING")
            return
        if not isinstance(self.encoding, str) or not self.encoding.strip():
            raise SourceReadAdmissionRefusal("SOURCE_READ_ENCODING_REQUIRED")
        qualified = COMPATIBILITY_ALLOWLIST.get(self.source_sha256)
        if qualified != self.encoding:
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_ENCODING_NOT_QUALIFIED", self.encoding)
        if self.authority_status != COMPATIBILITY_ONLY:
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_ENCODING_STATUS_REQUIRED", str(self.authority_status))


class SourceReadDecisionResolver(Protocol):
    def resolve_current(self, request: SourceReadRequest) -> IssuedSourceReadDecision:
        """Authenticate issuer/currentness/revocation/host/purpose externally."""
        ...


def _assert_current(decision: IssuedSourceReadDecision, request: SourceReadRequest) -> None:
    if not isinstance(decision, IssuedSourceReadDecision):
        raise SourceReadAdmissionRefusal("SOURCE_READ_DECISION_REQUIRED")
    if decision.currentness != CURRENT_GRANTED:
        raise SourceReadAdmissionRefusal("SOURCE_READ_NOT_CURRENT", decision.currentness)
    if decision.revocation_ref is not None:
        raise SourceReadAdmissionRefusal("SOURCE_READ_REVOKED")
    pairs = (
        ("source_id", decision.source_id, request.source_id),
        ("source_sha256", decision.source_sha256, request.source_sha256),
        ("source_format", decision.source_format, request.source_format),
        ("custody_locator_binding", decision.custody_locator_binding, request.custody_locator_binding),
        ("host", decision.host, request.host),
        ("purpose", decision.purpose, request.purpose),
        ("consumer_use", decision.consumer_use, request.consumer_use),
        ("read_operation", decision.read_operation, request.read_operation),
        ("physical_read_extent", decision.physical_read_extent, request.physical_read_extent),
        ("metadata_freeze_refs", decision.metadata_freeze_refs, request.metadata_freeze_refs),
        ("semantic_use_scope", decision.semantic_use_scope, request.semantic_use_scope),
    )
    for name, actual, expected in pairs:
        if actual != expected:
            raise SourceReadAdmissionRefusal(f"SOURCE_READ_{name.upper()}_MISMATCH")


def decode_with_source_read_permission(
    *,
    source_path: Any,
    request: SourceReadRequest,
    resolver: SourceReadDecisionResolver,
    reader: SourceReaderConfiguration | None = None,
) -> PhysicalSourceIncidence:
    """Resolve exact current predecode permission, then invoke the R04 decoder.

    ``source_path`` is not opened, stat'ed, hashed or inspected by this function
    before ``resolver.resolve_current(request)`` returns a valid current decision.
    A supplied ``reader`` is qualified against the request's exact source SHA
    before any source I/O; it cannot select an unallowlisted encoding.
    """
    if not isinstance(request, SourceReadRequest):
        raise SourceReadAdmissionRefusal("SOURCE_READ_REQUEST_REQUIRED")
    if reader is not None:
        if not isinstance(reader, SourceReaderConfiguration):
            raise SourceReadAdmissionRefusal("SOURCE_READ_READER_CONFIGURATION_REQUIRED")
        if reader.source_sha256 != request.source_sha256:
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_READER_SOURCE_SHA_MISMATCH", reader.source_sha256)
    decision = resolver.resolve_current(request)
    _assert_current(decision, request)
    decoder = decode_sav if request.source_format == "SAV" else decode_dta
    encoding = None if reader is None else reader.encoding
    incidence = decoder(
        source_path, expected_source_sha256=decision.source_sha256, encoding=encoding)
    try:
        current = resolver.resolve_current(request)
        _assert_current(current, request)
        if current != decision:
            raise SourceReadAdmissionRefusal("SOURCE_READ_DECISION_CHANGED_AFTER_DECODE")
        if incidence.source_sha256 != decision.source_sha256:
            raise SourceReadAdmissionRefusal("SOURCE_READ_DECODED_EDITION_MISMATCH")
        if str(incidence.source_format).upper() != decision.source_format:
            raise SourceReadAdmissionRefusal("SOURCE_READ_DECODED_FORMAT_MISMATCH")
        if reader is not None:
            actual = incidence.reader_configuration
            if actual.get("encoding") != reader.encoding:
                raise SourceReadAdmissionRefusal(
                    "SOURCE_READ_READER_ENCODING_MISMATCH", str(actual.get("encoding")))
            if reader.encoding is not None and actual.get("authority_status") != COMPATIBILITY_ONLY:
                raise SourceReadAdmissionRefusal(
                    "SOURCE_READ_READER_ENCODING_AUTHORITY_MISMATCH",
                    str(actual.get("authority_status")))
        return incidence
    except BaseException:
        incidence.close()
        raise


__all__ = [
    "CURRENT_GRANTED", "EXACT_FILE", "SOURCE_RESPONSE_DECODE",
    "IssuedSourceReadDecision", "SourceReadAdmissionRefusal",
    "SourceReadDecisionResolver", "SourceReadRequest", "SourceReaderConfiguration",
    "decode_with_source_read_permission",
]

"""Executable config-to-existing-owner factory.

The only production target is the existing ``GovernedC11Projection`` and its
source-backed C11 facade.  This module deliberately contains no alternate
engine, no synthetic original universe, and no default authority.
"""

from dataclasses import fields as dataclass_fields
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    SourceUniverseRelation,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule,
    CoordinateValueRule,
    ExactPhysicalCellStream,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    PhysicalSlotOwnerAuthorization,
    PhysicalSlotOwnerSet,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    WeightSlotRule,
    WeightValueRule,
    build_source_backed_c11_repository,
    build_validated_source_backed_c11_release,
    build_validated_source_backed_c11_release_from_stream,
    physical_value_binding_key,
)
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState



def _doc(config: SourceConfig | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(config, SourceConfig):
        return config.document
    validate_source_config(config)
    return config


def _typed_absence(value: Mapping[str, Any]) -> TypedAbsence:
    return TypedAbsence(value["typed_absence_state"], value.get("detail"))


def _ref(value: Mapping[str, Any]) -> ExactRef:
    return exact_ref(value, "exact ref")


def _active_identity(doc: Mapping[str, Any], *, source_sha256: str | None,
                     row_count: int | None) -> tuple[str, int, str, str, str]:
    identity = doc["identity"]
    binding = doc["binding"]
    active_sha = binding["source_sha256"] if source_sha256 is None else source_sha256
    active_rows = binding["row_count"] if row_count is None else row_count
    if active_sha != binding["source_sha256"]:
        raise SourceConfigurationBindingError(
            "active source SHA differs from the frozen config binding")
    if active_rows != binding["row_count"]:
        raise SourceConfigurationBindingError(
            "active row count differs from the frozen config binding")
    if binding["identity_class"] == "ORIGINAL_SOURCE":
        if active_sha != identity["expected_source_sha256"]:
            raise SourceConfigurationBindingError(
                "original binding SHA differs from the original source identity")
        if active_rows != identity["source_row_count"]:
            raise SourceConfigurationBindingError(
                "original binding row count differs from the original source identity")
        return (active_sha, active_rows, identity["source_artifact_id"],
                identity["study_product_id"], identity["release_id"])
    fixture = binding["fixture_provenance"]
    if active_sha == identity["expected_source_sha256"]:
        raise SourceConfigurationBindingError(
            "fixture binding may not reuse the original source SHA")
    return (
        active_sha,
        active_rows,
        f"R157_FIXTURE:{fixture['fixture_id']}",
        fixture["fixture_study_product_id"],
        fixture["fixture_release_id"],
    )


def _respondents(
    doc: Mapping[str, Any],
    *,
    active_rows: int,
    universes: Sequence[EmpiricalUniverse],
    row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None,
) -> tuple[Any, ...]:
    universe = universes[0]
    section = doc["respondents"]
    pattern = section["respondent_key_pattern"]
    identity_map = section.get("identity_map_authority_ref")
    identity_map_ref = None if identity_map is None else _authority_ref(identity_map)
    fixture = doc["binding"].get("fixture_provenance")
    configured_key_slot = section.get("source_native_key_slot")
    respondents = []
    for row in range(1, active_rows + 1):
        if fixture is not None and configured_key_slot is None:
            native_key = ExactRef(
                "R157_NONRESPONDENT_FIXTURE_ROW",
                f"urn:rawlsing:r157:fixture:{fixture['fixture_id']}:row:{row}",
                semantic_hash({
                    "fixture_id": fixture["fixture_id"],
                    "row_ordinal": row,
                    "fixture_source_sha256": doc["binding"]["source_sha256"],
                }),
            )
        elif configured_key_slot is not None:
            if row_native_keys is None or row not in row_native_keys:
                raise SourceConfigurationBindingError(
                    "configured source_native_key_slot requires row_native_keys after a permitted decode")
            native_key = row_native_keys[row]
            if not isinstance(native_key, (ExactRef, TypedAbsence)):
                raise SourceConfigurationBindingError(
                    "row_native_keys values must be exact ExactRef/TypedAbsence witnesses")
        else:
            native_key = TypedAbsence(
                "UNKNOWN",
                "source-native respondent key is not established in this P0/P3 config slice",
            )
        from rawlsing_next.pre553_c11_integrity import RespondentIdentity
        respondents.append(RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=pattern.format(row_ordinal=row),
            source_native_respondent_key_ref_or_typed_absence=native_key,
            identity_map_authority_ref_or_typed_absence=(
                identity_map_ref if identity_map_ref is not None else TypedAbsence("NOT_AUTHORIZED")
            ),
        ))
    return tuple(respondents)


def row_native_keys_from_transport(
    config: SourceConfig | Mapping[str, Any],
    *,
    stream: ExactPhysicalCellStream | None = None,
    incidence: PhysicalSourceIncidence | None = None,
    batch_size: int = 10_000,
) -> Mapping[int, ExactRef | TypedAbsence] | None:
    """Extract exact per-row key witnesses from the configured key slot.

    The raw physical key value remains a witness, not a new semantic category.
    Repeated values keep distinct row-bound refs; missing key cells stay typed
    unknowns.  This function performs no source I/O itself: the caller must
    supply an already permitted physical transport.
    """
    doc = _doc(config)
    slot = doc["respondents"].get("source_native_key_slot")
    if slot is None:
        return None
    if (stream is None) == (incidence is None):
        raise SourceConfigurationFactoryError("exactly one physical transport is required for key extraction")
    physical_slots = {
        (item["ordinal"], item["name"]) for item in doc["physical_slots"]
    }
    key = (slot["ordinal"], slot["name"])
    if key not in physical_slots:
        raise SourceConfigurationBindingError(
            "configured source_native_key_slot is absent from physical_slots")
    source_sha = stream.source_sha256 if stream is not None else incidence.source_sha256
    row_count = stream.row_count if stream is not None else incidence.row_count
    fixture = doc["binding"].get("fixture_provenance")
    kind = ("R157_NONRESPONDENT_FIXTURE_KEY" if fixture is not None
            else "SOURCE_NATIVE_RESPONDENT_KEY")
    scope = (fixture["fixture_id"] if fixture is not None else source_sha[:16])
    cells = stream.iter_cells() if stream is not None else incidence.iter_cells(batch_size)
    keys: dict[int, ExactRef | TypedAbsence] = {}
    for cell in cells:
        if (cell.variable_ordinal, cell.variable_name) != key:
            continue
        if cell.row_ordinal in keys:
            raise SourceConfigurationFactoryError("duplicate configured key cell for one row")
        if cell.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            keys[cell.row_ordinal] = ExactRef(
                kind,
                (f"urn:rawlsing:r157:{kind.lower()}:{doc['identity']['source_id']}:"
                 f"{scope}:{slot['ordinal']}:{cell.row_ordinal}"),
                physical_value_binding_key(
                    cell.raw_value, cell.missing_state, cell.source_missing_declaration),
            )
        else:
            keys[cell.row_ordinal] = TypedAbsence(
                "UNKNOWN",
                "configured source-native key cell is missing or unrepresented",
            )
    if set(keys) != set(range(1, row_count + 1)):
        raise SourceConfigurationFactoryError(
            "configured key slot did not yield exactly one witness per active row")
    return keys


def _effective_row_native_keys(
    config: SourceConfig | Mapping[str, Any],
    *,
    stream: ExactPhysicalCellStream | None,
    incidence: PhysicalSourceIncidence | None,
    explicit: Mapping[int, ExactRef | TypedAbsence] | None,
    batch_size: int,
) -> Mapping[int, ExactRef | TypedAbsence] | None:
    doc = _doc(config)
    slot = doc["respondents"].get("source_native_key_slot")
    if slot is None:
        if explicit is not None:
            raise SourceConfigurationBindingError(
                "row_native_keys supplied without a configured source_native_key_slot")
        return None
    if stream is None and incidence is None:
        raise SourceConfigurationFactoryError(
            "a physical stream/incidence is required to verify row-native key witnesses")
    derived = row_native_keys_from_transport(
        config, stream=stream, incidence=incidence, batch_size=batch_size)
    if explicit is None:
        return derived
    try:
        provided = {int(row): value for row, value in explicit.items()}
    except (TypeError, ValueError) as exc:
        raise SourceConfigurationBindingError(
            "supplied row-native keys are not an exact row mapping") from exc
    if dict(provided) != dict(derived):
        raise SourceConfigurationBindingError(
            "supplied row-native keys differ from the physical cell key witnesses")
    # Return the transport-derived witnesses, not the caller's copy, so the
    # projection is built from the same physical facts that were just checked.
    return derived


def _authority_ref(value: Mapping[str, Any]) -> AuthorityRef:
    return AuthorityRef(
        value["authority_id"], value["authority_version"], value["authority_content_hash"])


def _question(payload: Mapping[str, Any]) -> QuestionVariableBinding:
    native = {key: value for key, value in payload.items()
              if key in {field.name for field in dataclass_fields(QuestionVariableBinding)}}
    for name in ("empirical_universe_ref", "native_question_ref"):
        native[name] = _ref(native[name])
    for name in ("canonical_question_ref_or_typed_absence", "component_subitem_ref_or_typed_absence"):
        value = native.get(name)
        if isinstance(value, Mapping):
            native[name] = _typed_absence(value) if "typed_absence_state" in value else _ref(value)
    for name in ("semantic_authority_ref", "topology_authority_ref"):
        native[name] = _authority_ref(native[name])
    return QuestionVariableBinding(**native)


def _occurrence_rule(payload: Mapping[str, Any]) -> OccurrenceRule:
    component = payload.get("component_ref")
    return OccurrenceRule(
        payload["key"],
        _ref(payload["topology_ref"]),
        payload["multiplicity_order_rank_fields"],
        None if component is None else _ref(component),
    )


def _response_slots(doc: Mapping[str, Any], questions: Mapping[str, QuestionVariableBinding]) -> tuple[ResponseSlotRule, ...]:
    result = []
    for section in doc["response_slots"]:
        values = tuple(ResponseValueRule(
            physical_key=physical_value_binding_key(
                value["raw_value"],
                PhysicalMissingState(value["missing_state"]),
                value.get("source_missing_declaration"),
            ),
            response_state=value["response_state"],
            occurrences=tuple(_occurrence_rule(item) for item in value["occurrences"]),
            canonical_value=value.get("canonical_value"),
            transform_authority_ref=(None if value.get("transform_authority_ref") is None
                                     else _authority_ref(value["transform_authority_ref"])),
            extra_authority_refs=tuple(_authority_ref(x) for x in value.get("extra_authority_refs") or ()),
        ) for value in section["values"])
        result.append(ResponseSlotRule(
            PhysicalSlot(section["slot"]["ordinal"], section["slot"]["name"]),
            questions[section["question_id"]],
            values,
        ))
    return tuple(result)


def _coordinate_slots(doc: Mapping[str, Any]) -> tuple[CoordinateSlotRule, ...]:
    result = []
    for section in doc["coordinate_slots"]:
        values = tuple(CoordinateValueRule(
            physical_key=physical_value_binding_key(
                value["raw_value"],
                PhysicalMissingState(value["missing_state"]),
                value.get("source_missing_declaration"),
            ),
            coordinate_state=value["coordinate_state"],
            canonical_value=value.get("canonical_value"),
            extra_authority_refs=tuple(_authority_ref(x) for x in value.get("extra_authority_refs") or ()),
        ) for value in section.get("values", ()))
        normalization = section.get("normalization_ref")
        if isinstance(normalization, Mapping):
            if "typed_absence_state" in normalization:
                normalization = _typed_absence(normalization)
            elif "authority_id" in normalization:
                normalization = _authority_ref(normalization)
            else:
                normalization = _ref(normalization)
        result.append(CoordinateSlotRule(
            slot=PhysicalSlot(section["slot"]["ordinal"], section["slot"]["name"]),
            native_coordinate_ref=_ref(section["native_coordinate_ref"]),
            unit_taxonomy_ref=_ref(section["unit_taxonomy_ref"]),
            effective_time=section["effective_time"],
            source_semantic_authority_ref=_authority_ref(section["source_semantic_authority_ref"]),
            canonical_coordinate_ref=(None if section.get("canonical_coordinate_ref") is None
                                       else _ref(section["canonical_coordinate_ref"])),
            normalization_ref=normalization,
            values=values,
            copy_observed_raw=section.get("copy_observed_raw", False),
        ))
    return tuple(result)


def _weight_slots(doc: Mapping[str, Any]) -> tuple[WeightSlotRule, ...]:
    result = []
    for section in doc["weight_slots"]:
        values = tuple(WeightValueRule(
            physical_key=physical_value_binding_key(
                value["raw_value"],
                PhysicalMissingState(value.get("missing_state", "OBSERVED_STORAGE_VALUE")),
                value.get("source_missing_declaration"),
            ),
            exact_value=value["exact_value"],
            state=value.get("state", "WEIGHT_VALID_AUTHORIZED"),
        ) for value in section.get("values", ()))
        normalization = section.get("normalization_ref")
        if isinstance(normalization, Mapping):
            if "typed_absence_state" in normalization:
                normalization = _typed_absence(normalization)
            elif "authority_id" in normalization:
                normalization = _authority_ref(normalization)
            else:
                normalization = _ref(normalization)
        result.append(WeightSlotRule(
            slot=PhysicalSlot(section["slot"]["ordinal"], section["slot"]["name"]),
            weight_basis_id=section["weight_basis_id"],
            weight_source_ref=_ref(section["weight_source_ref"]),
            design_authority_ref=_authority_ref(section["design_authority_ref"]),
            estimand_authority_ref=_authority_ref(section["estimand_authority_ref"]),
            effective_scope_ref=_ref(section["effective_scope_ref"]),
            normalization_ref=normalization,
            values=values,
            copy_observed_numeric=section.get("copy_observed_numeric", False),
            extra_authority_refs=tuple(_authority_ref(x) for x in section.get("extra_authority_refs") or ()),
        ))
    return tuple(result)


def _routing(doc: Mapping[str, Any], questions: Mapping[str, QuestionVariableBinding],
             respondents: Sequence[Any], *, active_rows: int) -> tuple[Any, ...]:
    from rawlsing_next.pre553_empirical_objects import RoutingEligibilityFact
    result = []
    for rule in doc["routing"]:
        question = questions[rule["question_id"]]
        selector = rule["row_selector"]
        rows = tuple(range(1, active_rows + 1)) if selector == "ALL" else tuple(selector)
        if any(row < 1 or row > active_rows for row in rows):
            raise SourceConfigurationFactoryError(
                "routing row selector is outside the active source row range")
        authority = _authority_ref(rule["authority_ref"])
        replay_root = rule.get("replay_root")
        for row in rows:
            respondent = respondents[row - 1]
            root = (_ref(replay_root) if replay_root is not None else ExactRef(
                "ROUTING_REPLAY_ROOT",
                f"urn:rawlsing:r157:routing:{doc['config_id']}:{rule['question_id']}:{row}",
                semantic_hash({
                    "config_id": doc["config_id"],
                    "question_id": rule["question_id"],
                    "row_ordinal": row,
                    "respondent_ref": respondent.ref.as_dict(),
                }),
            ))
            result.append(RoutingEligibilityFact(
                typed_state=rule["typed_state"],
                authority_snapshot_refs=(authority,),
                dependency_refs=(respondent.ref, *(_ref(x) for x in rule.get("dependency_refs", ()))),
                producer_replay_locator_or_reference_root=root,
                empirical_universe_ref=respondent.empirical_universe_ref,
                scoped_respondent_ref=respondent.ref,
                question_or_target_ref=question.native_question_ref,
                risk_set_ref=_ref(rule["risk_set_ref"]),
                routing_rule_ref=_ref(rule["routing_rule_ref"]),
                applicability_state=rule["typed_state"],
                routing_state=rule["typed_state"],
                parent_predicate_refs=tuple(_ref(x) for x in rule.get("parent_predicate_refs", ())),
                member_set_replay_ref=_ref(rule["member_set_replay_ref"]),
            ))
    return tuple(result)


def _slot_owner_sets(doc: Mapping[str, Any]) -> tuple[PhysicalSlotOwnerSet, ...]:
    result = []
    for item in doc.get("slot_owner_sets", ()):
        owners = tuple(
            PhysicalSlotOwnerAuthorization(
                owner["owner_family"],
                tuple(_authority_ref(x) for x in owner["authority_refs"]),
            )
            for owner in item["owners"]
        )
        result.append(PhysicalSlotOwnerSet(
            PhysicalSlot(item["slot"]["ordinal"], item["slot"]["name"]), owners))
    return tuple(result)


def _source_relations(doc: Mapping[str, Any]) -> tuple[SourceUniverseRelation, ...] | TypedAbsence:
    section = doc["source_relations"]
    if "relations" not in section:
        return TypedAbsence(section["typed_absence_state"])
    return tuple(SourceUniverseRelation(**payload) for payload in section["relations"])


def _replay_absence(doc: Mapping[str, Any], name: str) -> TypedAbsence:
    return _typed_absence(doc["replay"][name])


def build_governed_c11_projection(
    config: SourceConfig | Mapping[str, Any],
    *,
    source_sha256: str | None = None,
    row_count: int | None = None,
    row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None,
) -> GovernedC11Projection:
    """Construct the actual ``GovernedC11Projection`` from a validated config.

    The caller may repeat the active SHA/row count after a permitted decode;
    they must match the frozen binding.  No respondent/value witness is invented
    here: response events and coordinates are created by the existing facade
    only when the physical cell stream is projected.
    """
    doc = _doc(config)
    active_sha, active_rows, artifact_id, study_id, release_id = _active_identity(
        doc, source_sha256=source_sha256, row_count=row_count)
    authority_snapshots = tuple(
        AuthoritySnapshot(**payload) for payload in doc["authority"]["snapshots"])
    universes = tuple(EmpiricalUniverse(**payload) for payload in doc["universe"]["universes"])
    questions_by_id = {
        section["question_id"]: _question(section) for section in doc["questions"]
    }
    respondents = _respondents(
        doc, active_rows=active_rows, universes=universes, row_native_keys=row_native_keys)
    row_bindings = tuple(
        RowRespondentBinding(row, respondent.ref)
        for row, respondent in enumerate(respondents, 1)
    )
    binding = doc["binding"]
    if binding["identity_class"] == IDENTITY_CLASS_FIXTURE:
        fixture = binding["fixture_provenance"]
        study_id = fixture["fixture_study_product_id"]
        release_id = fixture["fixture_release_id"]
        instrument_id = fixture["fixture_instrument_release_id"]
        snapshot_ref = _ref(binding["source_snapshot_ref"])
    else:
        instrument_id = doc["identity"]["instrument_release_id"]
        snapshot_ref = _ref(doc["identity"]["source_snapshot_retention_ref"])
    required = tuple(_authority_ref(x) for x in doc["authority"]["required_refs"])
    projection = GovernedC11Projection(
        projection_identity_ref=_ref(doc["authority"]["projection_identity_ref"]),
        source_artifact_id=artifact_id,
        expected_source_sha256=active_sha,
        source_family_id=doc["identity"]["source_family_id"],
        study_product_id=study_id,
        release_id=release_id,
        instrument_release_id=instrument_id,
        source_snapshot_retention_ref=snapshot_ref,
        universes=universes,
        respondents=respondents,
        row_bindings=row_bindings,
        questions=tuple(questions_by_id.values()),
        response_slots=_response_slots(doc, questions_by_id),
        coordinate_slots=_coordinate_slots(doc),
        routing=_routing(doc, questions_by_id, respondents, active_rows=active_rows),
        weight_slots=_weight_slots(doc),
        authority_snapshots=authority_snapshots,
        source_relations=_source_relations(doc),
        predicate_replay=_replay_absence(doc, "predicate"),
        comparator_replay=_replay_absence(doc, "comparator"),
        discovery_replay=_replay_absence(doc, "discovery"),
        structural_replay=_replay_absence(doc, "structural"),
        required_authority_refs=required,
        projection_authority_ref=_authority_ref(doc["authority"]["projection_authority_ref"]),
        replay_authority_ref=_authority_ref(doc["authority"]["replay_authority_ref"]),
        tie_order_ref=_ref(doc["authority"]["tie_order_ref"]),
        replay_protocol_version=doc["authority"]["replay_protocol_version"],
        slot_owner_sets=_slot_owner_sets(doc),
    )
    return projection


# Explicit frozen name used by P0_RETURN.json and source lanes.
construct_governed_c11_projection = build_governed_c11_projection


def _verify_transport(projection: GovernedC11Projection, *,
                      stream: ExactPhysicalCellStream | None,
                      incidence: PhysicalSourceIncidence | None) -> None:
    if (stream is None) == (incidence is None):
        raise SourceConfigurationFactoryError(
            "exactly one of stream or incidence is required")
    source_sha = stream.source_sha256 if stream is not None else incidence.source_sha256
    source_rows = stream.row_count if stream is not None else incidence.row_count
    if source_sha != projection.expected_source_sha256:
        raise SourceConfigurationBindingError("physical transport SHA differs from active config binding")
    if source_rows != len(projection.row_bindings):
        raise SourceConfigurationBindingError("physical transport row count differs from active config binding")


def build_validated_c11_release_from_config(
    config: SourceConfig | Mapping[str, Any],
    *,
    stream: ExactPhysicalCellStream | None = None,
    incidence: PhysicalSourceIncidence | None = None,
    source_sha256: str | None = None,
    row_count: int | None = None,
    row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None,
    batch_size: int = 10_000,
):
    """Build and validate a native C11 release through the existing owner."""
    if stream is not None and incidence is not None:
        raise SourceConfigurationFactoryError("pass exactly one physical transport")
    if stream is None and incidence is None:
        raise SourceConfigurationFactoryError("a permitted physical stream/incidence is required")
    active_sha = source_sha256
    active_rows = row_count
    if stream is not None:
        active_sha = active_sha or stream.source_sha256
        active_rows = active_rows or stream.row_count
    if incidence is not None:
        active_sha = active_sha or incidence.source_sha256
        active_rows = active_rows or incidence.row_count
    row_native_keys = _effective_row_native_keys(
        config, stream=stream, incidence=incidence,
        explicit=row_native_keys, batch_size=batch_size)
    projection = build_governed_c11_projection(
        config, source_sha256=active_sha, row_count=active_rows,
        row_native_keys=row_native_keys)
    _verify_transport(projection, stream=stream, incidence=incidence)
    if stream is not None:
        return build_validated_source_backed_c11_release_from_stream(stream, projection)
    return build_validated_source_backed_c11_release(incidence, projection, batch_size=batch_size)


def build_source_backed_c11_repository_from_config(
    config: SourceConfig | Mapping[str, Any],
    source: ExactPhysicalCellStream | PhysicalSourceIncidence,
    *,
    row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None,
    cache: Any = None,
    batch_size: int = 10_000,
):
    """Build the existing source-backed C11 repository from a validated config."""
    if not isinstance(source, (ExactPhysicalCellStream, PhysicalSourceIncidence)):
        raise SourceConfigurationFactoryError("existing physical transport is required")
    row_native_keys = _effective_row_native_keys(
        config,
        stream=source if isinstance(source, ExactPhysicalCellStream) else None,
        incidence=source if isinstance(source, PhysicalSourceIncidence) else None,
        explicit=row_native_keys, batch_size=batch_size)
    projection = build_governed_c11_projection(
        config, source_sha256=source.source_sha256, row_count=source.row_count,
        row_native_keys=row_native_keys)
    return build_source_backed_c11_repository(
        source, projection, cache=cache, batch_size=batch_size)

"""Config-to-source-read transport glue for the existing admission owner.

This module does not grant source rights.  It only turns a validated source
configuration's exact identity/reader fields into the existing request/decision
transport and passes the qualified reader configuration to the unchanged
physical decoder.
"""

from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import exact_ref


def _reader_doc(config: SourceConfig | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(config, SourceConfig):
        return config.document
    if not isinstance(config, Mapping):
        raise SourceConfigurationBindingError("source configuration must be SourceConfig or mapping")
    return config


def _identity(doc: Mapping[str, Any]) -> Mapping[str, Any]:
    identity = doc.get("identity")
    if not isinstance(identity, Mapping):
        raise SourceConfigurationBindingError("source configuration lacks identity")
    return identity


def _require_original_binding(doc: Mapping[str, Any]) -> None:
    binding = doc.get("binding")
    if not isinstance(binding, Mapping):
        raise SourceConfigurationBindingError("source configuration lacks binding")
    if binding.get("identity_class") != IDENTITY_CLASS_ORIGINAL:
        raise SourceConfigurationBindingError(
            "source-read transport applies only to an ORIGINAL_SOURCE config; fixtures are not original reads")


def reader_configuration_from_config(
    config: SourceConfig | Mapping[str, Any],
) -> SourceReaderConfiguration:
    """Extract the exact qualified reader configuration from identity.reader."""
    doc = _reader_doc(config)
    _require_original_binding(doc)
    identity = _identity(doc)
    reader = identity.get("reader")
    if not isinstance(reader, Mapping):
        raise SourceConfigurationBindingError("identity.reader is required")
    config_ref = exact_ref(reader["configuration_ref"], "identity.reader.configuration_ref")
    encoding = reader.get("encoding")
    if encoding is None:
        return SourceReaderConfiguration(
            source_sha256=identity["expected_source_sha256"],
            configuration_ref=config_ref,
        )
    if not isinstance(encoding, Mapping):
        raise SourceConfigurationBindingError("identity.reader.encoding must be object or null")
    return SourceReaderConfiguration(
        source_sha256=identity["expected_source_sha256"],
        encoding=encoding["value"],
        authority_status=encoding["authority_status"],
        configuration_ref=config_ref,
    )


def source_read_request_from_config(
    config: SourceConfig | Mapping[str, Any],
    *,
    host: str,
    purpose: str,
    consumer_use: str,
    semantic_use_scope: Sequence[str],
    metadata_freeze_refs: Sequence[Any] | None = None,
    custody_locator_binding: str | None = None,
) -> SourceReadRequest:
    """Build the existing metadata-only request without opening source bytes."""
    doc = _reader_doc(config)
    _require_original_binding(doc)
    identity = _identity(doc)
    locator = identity.get("locator")
    if not isinstance(locator, Mapping):
        raise SourceConfigurationBindingError("identity.locator is required")
    if custody_locator_binding is None:
        if locator.get("root") == "SOURCE_ROOT":
            custody_locator_binding = locator.get("relative_path")
        elif locator.get("root") == "EXTERNAL_LOCATOR_ID":
            custody_locator_binding = locator.get("locator_id")
    if not isinstance(custody_locator_binding, str) or not custody_locator_binding.strip():
        raise SourceConfigurationBindingError("an exact custody locator binding is required")
    if metadata_freeze_refs is None:
        metadata_freeze_refs = (identity["metadata_witness_ref"],)
    if isinstance(semantic_use_scope, (str, bytes)) or not semantic_use_scope:
        raise SourceConfigurationEvidenceError("semantic_use_scope must be an explicit non-empty scope")
    return SourceReadRequest(
        source_id=identity["source_id"],
        source_sha256=identity["expected_source_sha256"],
        source_format=identity["source_format"],
        custody_locator_binding=custody_locator_binding,
        host=host,
        purpose=purpose,
        consumer_use=consumer_use,
        metadata_freeze_refs=tuple(exact_ref(x, "metadata_freeze_ref") for x in metadata_freeze_refs),
        semantic_use_scope=tuple(semantic_use_scope),
    )


def decode_config_with_source_read_permission(
    config: SourceConfig | Mapping[str, Any],
    *,
    source_path: Any,
    resolver: Any,
    host: str,
    purpose: str,
    consumer_use: str,
    semantic_use_scope: Sequence[str],
    metadata_freeze_refs: Sequence[Any] | None = None,
    custody_locator_binding: str | None = None,
):
    """Decode through the existing source-read owner with config reader facts."""
    request = source_read_request_from_config(
        config,
        host=host,
        purpose=purpose,
        consumer_use=consumer_use,
        semantic_use_scope=semantic_use_scope,
        metadata_freeze_refs=metadata_freeze_refs,
        custody_locator_binding=custody_locator_binding,
    )
    reader = reader_configuration_from_config(config)
    return decode_with_source_read_permission(
        source_path=source_path, request=request, resolver=resolver, reader=reader)


__all__ = [
    "reader_configuration_from_config",
    "source_read_request_from_config",
    "decode_config_with_source_read_permission",
]

"""Clearly nonrespondent fixture transport for R157 validation.

A fixture is not an original source package.  Its byte identity is the canonical
hash of the fixture document, and the document must declare the separate original
source identity it is exercising.  No original respondent rows are represented.
"""

from pathlib import Path
import hashlib
import json
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell,
    PhysicalMissingState,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream


FIXTURE_SCHEMA_ID = "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0"


def _fixture_mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise SourceConfigurationEvidenceError(f"{path} must be an object")
    return value


def _fixture_sequence(value: Any, path: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise SourceConfigurationEvidenceError(f"{path} must be an array")
    return value


def _fixture_text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceConfigurationEvidenceError(f"{path} must be a non-empty string")
    return value


def _fixture_integer(value: Any, path: str, *, minimum: int = 1) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise SourceConfigurationEvidenceError(f"{path} must be an integer >= {minimum}")
    return value


def _fixture_material(document: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in document.items() if key != "fixture_source_sha256"}


def fixture_document_sha256(document: Mapping[str, Any]) -> str:
    """Deterministic SHA-256 of the fixture document excluding its own hash field.

    Fixture cells may carry exact numeric source values (including decimals).
    This is a byte-binding identity for the fixture input, not a semantic object
    identity; the native physical-value codec remains authoritative for values.
    """
    material = json.dumps(
        _fixture_material(document), sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def _validate_cell(cell: Any, path: str) -> PhysicalCell:
    payload = _fixture_mapping(cell, path)
    expected = {
        "row_ordinal", "variable_ordinal", "variable_name", "raw_value",
        "missing_state", "source_missing_declaration",
    }
    missing = sorted(expected - set(payload))
    extra = sorted(set(payload) - expected - {"raw_value_label"})
    if missing:
        raise SourceConfigurationEvidenceError(f"{path} missing keys {missing!r}")
    if extra:
        raise SourceConfigurationEvidenceError(f"{path} unknown keys {extra!r}")
    state = _fixture_text(payload["missing_state"], f"{path}.missing_state")
    if state not in {x.value for x in PhysicalMissingState}:
        raise SourceConfigurationEvidenceError(f"{path}.missing_state is not a PhysicalMissingState")
    declaration = payload["source_missing_declaration"]
    if declaration is not None:
        _fixture_mapping(declaration, f"{path}.source_missing_declaration")
    return PhysicalCell(
        row_ordinal=_fixture_integer(payload["row_ordinal"], f"{path}.row_ordinal"),
        variable_ordinal=_fixture_integer(payload["variable_ordinal"], f"{path}.variable_ordinal"),
        variable_name=_fixture_text(payload["variable_name"], f"{path}.variable_name"),
        raw_value=payload["raw_value"],
        missing_state=PhysicalMissingState(state),
        source_missing_declaration=declaration,
        raw_value_label=payload.get("raw_value_label"),
    )


def fixture_stream_from_document(document: Mapping[str, Any]) -> ExactPhysicalCellStream:
    """Validate a nonrespondent fixture and return the exact physical stream."""
    document = _fixture_mapping(document, "fixture")
    if document.get("schema") != FIXTURE_SCHEMA_ID:
        raise SourceConfigurationEvidenceError(
            f"fixture.schema must be {FIXTURE_SCHEMA_ID!r}")
    if document.get("identity_class") != "NONRESPONDENT_FIXTURE":
        raise SourceConfigurationEvidenceError(
            "fixture.identity_class must be NONRESPONDENT_FIXTURE")
    if document.get("nonrespondent") is not True:
        raise SourceConfigurationEvidenceError("fixture.nonrespondent must be true")
    _fixture_text(document.get("fixture_id"), "fixture.fixture_id")
    row_count = _fixture_integer(document.get("row_count"), "fixture.row_count")
    cells = tuple(_validate_cell(cell, f"fixture.cells[{index}]")
                  for index, cell in enumerate(_fixture_sequence(document.get("cells"), "fixture.cells")))
    if not cells:
        raise SourceConfigurationEvidenceError("fixture.cells must not be empty")
    rows = {cell.row_ordinal for cell in cells}
    if rows != set(range(1, row_count + 1)):
        raise SourceConfigurationEvidenceError(
            "fixture row ordinals must be exactly 1..row_count")
    seen: set[tuple[int, int, str]] = set()
    slot_names: dict[int, str] = {}
    for cell in cells:
        key = (cell.row_ordinal, cell.variable_ordinal, cell.variable_name)
        if key in seen:
            raise SourceConfigurationEvidenceError("duplicate fixture physical cell")
        seen.add(key)
        previous = slot_names.get(cell.variable_ordinal)
        if previous is not None and previous != cell.variable_name:
            raise SourceConfigurationEvidenceError(
                "fixture variable ordinal is reused with a different name")
        slot_names[cell.variable_ordinal] = cell.variable_name
    expected_sha = _fixture_text(document.get("fixture_source_sha256"), "fixture.fixture_source_sha256")
    actual_sha = fixture_document_sha256(document)
    if expected_sha != actual_sha:
        raise SourceConfigurationEvidenceError(
            "fixture_source_sha256 does not bind the canonical fixture document")
    return ExactPhysicalCellStream(
        source_sha256=expected_sha,
        row_count=row_count,
        cell_iter_factory=lambda: cells,
        transport_identity="R157_NONRESPONDENT_FIXTURE_EXACT_CELLS@1.0.0",
    )


def load_fixture_stream(path: str | Path) -> ExactPhysicalCellStream:
    path = Path(path)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SourceConfigurationEvidenceError(f"cannot read fixture {path}: {exc}") from exc
    return fixture_stream_from_document(document)


__all__ = [
    "FIXTURE_SCHEMA_ID", "fixture_document_sha256", "fixture_stream_from_document",
    "load_fixture_stream",
]

"""Portable registry, index and delivery helpers for R157 source configurations.

The registry is a discovery/selection layer over the frozen SourceConfig schema and
the existing source-backed C11 factory.  It never invents source meaning or opens
original source bytes.
"""

from collections import Counter
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import sqlite3
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "rawlsing_next/source_configuration/data"
VALIDATION_DIR = ROOT / "source_pre553_validation"
INTEGRATION_DIR = VALIDATION_DIR / "integration"
INDEX_PATH = INTEGRATION_DIR / "SOURCE_LIBRARY_INDEX.json"
SQLITE_PATH = INTEGRATION_DIR / "SOURCE_LIBRARY_INDEX.sqlite"
PLAN_SEAL = "4c0c619eac747afee1d8e65e1418bf2d472da4c3"
FROZEN_P0 = "d8d7087a8e56c24042bf5945fea1c97eb0d6c710"
FROZEN_P3 = "519355ec2215409b40d566ef13c3b21f611e0726"
SOURCE_IDS = tuple(f"SRC{i:02d}" for i in range(1, 36))
PENDING_SOURCE_IDS = ("SRC27", "SRC28", "SRC29", "SRC30", "SRC33", "SRC34", "SRC35")


class SourceLibraryError(ValueError):
    pass


class SourceNotPrepared(SourceLibraryError):
    def __init__(self, source_id: str, status: str, detail: str = ""):
        self.source_id = source_id
        self.status = status
        self.detail = detail
        super().__init__(f"{source_id}: {status}" + (f": {detail}" if detail else ""))


class SourceArtifactError(SourceLibraryError):
    pass


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    family: str
    wave: str
    lane: str | None
    status: str
    original_config_path: str | None
    original_config_file_sha256: str | None
    original_config_canonical_sha256: str | None
    fixture_config_path: str | None
    fixture_config_file_sha256: str | None
    fixture_path: str | None
    fixture_file_sha256: str | None
    fixture_source_sha256: str | None
    native_results_path: str | None
    native_results_file_sha256: str | None
    release_ref: Mapping[str, Any] | None
    counts: Mapping[str, Any] = field(default_factory=dict)
    held: Mapping[str, Any] = field(default_factory=dict)
    details: tuple[str, ...] = ()

    @property
    def available(self) -> bool:
        return self.status == "AVAILABLE_NATIVE_RECEIPT"

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "family": self.family,
            "wave": self.wave,
            "lane": self.lane,
            "status": self.status,
            "original_config_path": self.original_config_path,
            "original_config_file_sha256": self.original_config_file_sha256,
            "original_config_canonical_sha256": self.original_config_canonical_sha256,
            "fixture_config_path": self.fixture_config_path,
            "fixture_config_file_sha256": self.fixture_config_file_sha256,
            "fixture_path": self.fixture_path,
            "fixture_file_sha256": self.fixture_file_sha256,
            "fixture_source_sha256": self.fixture_source_sha256,
            "native_results_path": self.native_results_path,
            "native_results_file_sha256": self.native_results_file_sha256,
            "release_ref": dict(self.release_ref) if self.release_ref else None,
            "counts": dict(self.counts),
            "held": dict(self.held),
            "details": list(self.details),
        }


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _exact_case_path(directory: Path, name: str) -> Path | None:
    """Return the actual directory entry whose spelling is exactly ``name``.

    ``Path.is_file()`` is case-insensitive on macOS, so it can silently accept a
    candidate spelling that does not exist on a case-sensitive checkout.  Indexed
    artifact paths must be the real committed spelling.
    """
    try:
        entries = list(directory.iterdir())
    except FileNotFoundError:
        return None
    for entry in entries:
        if entry.name == name and entry.is_file():
            return entry
    return None


def _exact_case_join(root: Path, relative: str | Path) -> Path:
    """Resolve a repository-relative path component-by-component, exact-case."""
    current = root
    for part in Path(relative).parts:
        if part in ("", "."):
            continue
        try:
            entries = list(current.iterdir())
        except FileNotFoundError:
            raise SourceArtifactError(f"missing path component {part!r} under {current}")
        child = next((entry for entry in entries if entry.name == part), None)
        if child is None:
            raise SourceArtifactError(f"non-exact path component {part!r} under {current}")
        current = child
    return current


def assert_exact_index_paths(index: Mapping[str, Any], root: Path = ROOT) -> None:
    """Assert every serialized source artifact path is the real directory spelling."""
    for row in index.get("sources", ()):  # type: ignore[union-attr]
        for field in ("original_config_path", "fixture_config_path", "fixture_path", "native_results_path"):
            relative = row.get(field)
            if not relative:
                continue
            path = _exact_case_join(root, relative)
            if not path.is_file():
                raise SourceArtifactError(f"{row.get('source_id')}: indexed {field} is not a file: {relative}")


def _lane_map() -> dict[str, str]:
    path = ROOT / "SOURCE_PRE553_PLAN/LANES.json"
    try:
        lanes = _json(path)["lanes"]
    except Exception:
        return {}
    return {sid: lane["lane_id"] for lane in lanes for sid in lane["source_ids"]}


def _candidate_original(source_id: str) -> Path | None:
    data = DATA_DIR / source_id
    numeric = source_id[3:]
    for name in (f"{source_id}.config.json", f"{source_id}.source.config.json",
                 f"src{numeric}.config.json", f"src{numeric}.source.config.json", "source.config.json"):
        path = _exact_case_path(data, name)
        if path is not None:
            try:
                config = load_source_config(path)
            except Exception:
                continue
            if config.config_purpose == "SOURCE_PREPARATION" and config.source_id == source_id:
                return path
    return None


def _candidate_fixture(source_id: str) -> tuple[Path, Path] | None:
    data = DATA_DIR / source_id
    validation = VALIDATION_DIR / source_id
    candidates = (
        (data, f"{source_id}.full.fixture.config.json", validation, f"{source_id}.full.fixture.json"),
        (data, f"{source_id}.fixture.config.json", validation, f"{source_id}.fixture.json"),
        (validation, f"{source_id}.full.fixture.config.json", validation, f"{source_id}.full.fixture.json"),
        (validation, f"{source_id}.fixture.config.json", validation, f"{source_id}.fixture.json"),
        (validation, "fixture.config.json", validation, "fixture.json"),
    )
    for config_dir, config_name, fixture_dir, fixture_name in candidates:
        config_path = _exact_case_path(config_dir, config_name)
        fixture_path = _exact_case_path(fixture_dir, fixture_name)
        if config_path is None or fixture_path is None:
            continue
        try:
            config = load_source_config(config_path)
            fixture = load_fixture_stream(fixture_path)
        except Exception:
            continue
        if config.config_purpose != "NONRESPONDENT_FIXTURE" or config.identity_class != "NONRESPONDENT_FIXTURE":
            continue
        if config.source_id != source_id:
            continue
        if config.active_source_sha256 != fixture.source_sha256:
            continue
        if config.active_row_count != fixture.row_count:
            continue
        return config_path, fixture_path
    return None


def _candidate_native(source_id: str) -> tuple[Path, Mapping[str, Any], Mapping[str, Any]] | None:
    validation = VALIDATION_DIR / source_id
    for name in ("FULL_NATIVE_RESULTS.json", "NATIVE_RESULTS.json",
                 "VALIDATION_RESULTS.json", f"{source_id}.validation-results.json",
                 "validation_results.json"):
        path = _exact_case_path(validation, name)
        if path is None:
            continue
        try:
            document = _json(path)
        except Exception:
            continue
        release = _find_release_ref(document)
        if release is not None:
            return path, document, release
    return None


def _find_release_ref(value: Any) -> Mapping[str, Any] | None:
    if isinstance(value, Mapping):
        ref = value.get("release_ref")
        if isinstance(ref, Mapping) and ref.get("kind") == "C11LogicalRelease":
            return ref
        if (value.get("kind") == "C11LogicalRelease"
                and isinstance(value.get("object_id"), str)
                and isinstance(value.get("content_hash"), str)):
            return value
        for item in value.values():
            found = _find_release_ref(item)
            if found is not None:
                return found
    elif isinstance(value, list):
        for item in value:
            found = _find_release_ref(item)
            if found is not None:
                return found
    return None


def _candidate_exception(source_id: str) -> Path | None:
    validation = VALIDATION_DIR / source_id
    for name in ("EXCEPTION_LEDGER.json", "EXCEPTIONS.json", f"{source_id}.exceptions.json",
                 "exception_ledger.json"):
        path = _exact_case_path(validation, name)
        if path is not None:
            return path
    return None


def _exception_summary(source_id: str) -> dict[str, Any]:
    path = _candidate_exception(source_id)
    if path is None:
        return {}
    try:
        document = _json(path)
    except Exception:
        return {"exception_path": str(path.relative_to(ROOT)), "exception_file_sha256": _file_sha(path)}
    summary: dict[str, Any] = {
        "exception_path": str(path.relative_to(ROOT)),
        "exception_file_sha256": _file_sha(path),
    }
    for key in ("residual_count", "bound_item_count", "held_item_count", "held_by_role_counts"):
        if key in document:
            summary[key] = document[key]
    held_items = document.get("held_items")
    if isinstance(held_items, list):
        summary["held_item_refs"] = [
            {
                "implementation_id": item.get("implementation_id"),
                "physical_slot": item.get("physical_slot"),
                "configuration_role": item.get("configuration_role"),
                "source_disposition": item.get("source_disposition"),
                "native_field": item.get("native_field"),
            }
            for item in held_items
            if isinstance(item, Mapping)
        ]
    return summary


def _held_counts(config: SourceConfig) -> dict[str, Any]:
    categories = Counter()
    for slot in config.document.get("physical_slots", ()):
        disposition = str(slot.get("disposition", ""))
        if disposition.startswith("HELD"):
            categories[disposition] += 1
    return {"held_slots": sum(categories.values()), "held_by_disposition": dict(sorted(categories.items()))}


def build_index(*, index_path: str | Path = INDEX_PATH, sqlite_path: str | Path | None = SQLITE_PATH) -> dict[str, Any]:
    """Refuse absent historical discovery rather than inventing a source root.

    The historical ``SOURCE_PRE553_PLAN`` / ``source_pre553_validation`` /
    ``source_configuration/data`` discovery tree is not present in the current
    protected checkout.  A caller may still load an independently supplied
    portable index through ``SourceConfigLibrary``.
    """
    raise SourceLibraryError(
        "build_index is an ABSENT_CURRENT_PORT: the historical all35 discovery "
        "tree is not in the protected checkout; supply an external portable index "
        "to SourceConfigLibrary"
    )

class SourceConfigLibrary:
    """Actual callable registry over the portable index."""

    def __init__(self, *, index_path: str | Path = INDEX_PATH, root: str | Path = ROOT):
        self.root = Path(root).resolve()
        self.index_path = Path(index_path)
        if not self.index_path.is_file():
            raise SourceLibraryError(
                f"index missing: {self.index_path}; run `python -m rawlsing_next.source_configuration.cli build-index`")
        document = _json(self.index_path)
        self.document = document
        self.records = {row["source_id"]: row for row in document["sources"]}

    def record(self, source_id: str) -> Mapping[str, Any]:
        if source_id not in self.records:
            raise SourceNotPrepared(source_id, "UNKNOWN_SOURCE")
        row = self.records[source_id]
        if not row.get("status", "").startswith("AVAILABLE"):
            raise SourceNotPrepared(source_id, row.get("status", "PENDING"), "; ".join(row.get("details", [])))
        return row

    def source_ids(self) -> tuple[str, ...]:
        return tuple(self.records)

    def available_source_ids(self) -> tuple[str, ...]:
        return tuple(x for x in self.records if self.records[x].get("status") == "AVAILABLE_NATIVE_RECEIPT")

    def pending_source_ids(self) -> tuple[str, ...]:
        return tuple(self.document.get("pending_source_ids", []))

    def _artifact(self, source_id: str, kind: str) -> tuple[Path, Mapping[str, Any]]:
        row = self.record(source_id)
        if kind == "original":
            path = _exact_case_join(self.root, row["original_config_path"])
            expected = row["original_config_file_sha256"]
        elif kind == "fixture-config":
            path = _exact_case_join(self.root, row["fixture_config_path"])
            expected = row["fixture_config_file_sha256"]
        elif kind == "fixture":
            path = _exact_case_join(self.root, row["fixture_path"])
            expected = row["fixture_file_sha256"]
        else:
            raise SourceArtifactError(f"unknown artifact kind {kind!r}")
        if not path.is_file():
            raise SourceArtifactError(f"{source_id}: missing {kind} artifact {path}")
        actual = _file_sha(path)
        if actual != expected:
            raise SourceArtifactError(f"{source_id}: {kind} SHA mismatch")
        return path, row

    def load_original(self, source_id: str) -> SourceConfig:
        path, _ = self._artifact(source_id, "original")
        config = load_source_config(path)
        if config.source_id != source_id or config.config_purpose != "SOURCE_PREPARATION":
            raise SourceArtifactError(f"{source_id}: original config identity/purpose mismatch")
        return config

    def load_fixture_config(self, source_id: str) -> SourceConfig:
        path, _ = self._artifact(source_id, "fixture-config")
        config = load_source_config(path)
        if config.source_id != source_id or config.config_purpose != "NONRESPONDENT_FIXTURE":
            raise SourceArtifactError(f"{source_id}: fixture config identity/purpose mismatch")
        return config

    def load_fixture_stream(self, source_id: str):
        path, row = self._artifact(source_id, "fixture")
        stream = load_fixture_stream(path)
        if stream.source_sha256 != row["fixture_source_sha256"]:
            raise SourceArtifactError(f"{source_id}: fixture stream source SHA mismatch")
        return stream

    def build_fixture_release(self, source_id: str):
        config = self.load_fixture_config(source_id)
        stream = self.load_fixture_stream(source_id)
        release = build_validated_c11_release_from_config(config, stream=stream)
        row = self.record(source_id)
        expected = (row.get("release_ref") or {}).get("content_hash")
        if expected and release.release_ref.content_hash != expected:
            raise SourceArtifactError(
                f"{source_id}: native release receipt mismatch {release.release_ref.content_hash} != {expected}")
        return release

    def validate_source(
        self,
        source_id: str,
        *,
        historical_roster_entry: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Validate the portable index/config/fixture binding and roster counts.

        The historical ``SOURCE_ROSTER.json``/exception tree is absent from the
        current protected checkout, so the roster denominators are not silently
        assumed.  A caller that has the independently supplied historical roster
        entry can pass it here; the exact historical physical-slot and
        original-item comparisons then execute.  Without that entry the local
        checks still run, but ``passed`` is false and the roster comparison is a
        typed external HOLD rather than a false pass.
        """
        row = self.record(source_id)
        original = self.load_original(source_id)
        fixture = self.load_fixture_config(source_id)
        stream = self.load_fixture_stream(source_id)
        counts = row.get("counts") or {}
        checks = {
            "original_schema": True,
            "fixture_schema": True,
            "original_source_id": original.source_id == source_id,
            "fixture_identity_class": fixture.identity_class == "NONRESPONDENT_FIXTURE",
            "fixture_sha_binding": fixture.active_source_sha256 == stream.source_sha256,
            "fixture_row_count": fixture.active_row_count == stream.row_count,
        }
        if counts.get("physical_slots") is not None:
            checks["index_physical_slots"] = (
                len(original.document.get("physical_slots", ()))
                == int(counts["physical_slots"])
            )
        if counts.get("original_items") is not None:
            checks["index_original_items"] = (
                len(original.document.get("items", ()))
                == int(counts["original_items"])
            )
        roster_state = "HOLD_EXTERNAL__SOURCE_ROSTER_ABSENT_CURRENT_PORT"
        if historical_roster_entry is not None:
            entry_source_id = historical_roster_entry.get("source_id")
            if entry_source_id is not None and entry_source_id != source_id:
                raise SourceConfigurationEvidenceError(
                    f"historical roster entry source_id {entry_source_id!r} "
                    f"does not match {source_id!r}")
            for key in ("physical_columns", "original_items"):
                if key not in historical_roster_entry:
                    raise SourceConfigurationEvidenceError(
                        f"historical roster entry for {source_id} lacks {key!r}")
            checks["historical_physical_slots"] = (
                len(original.document.get("physical_slots", ()))
                == int(historical_roster_entry["physical_columns"])
            )
            checks["historical_original_items"] = (
                len(original.document.get("items", ()))
                == int(historical_roster_entry["original_items"])
            )
            roster_state = "PASS" if (
                checks["historical_physical_slots"]
                and checks["historical_original_items"]
            ) else "FAIL"
        return {
            "source_id": source_id,
            "status": row["status"],
            "config_path": row["original_config_path"],
            "fixture_config_path": row["fixture_config_path"],
            "fixture_path": row["fixture_path"],
            "native_results_path": row["native_results_path"],
            "checks": checks,
            "passed": all(checks.values()) and historical_roster_entry is not None,
            "historical_roster_comparison": roster_state,
            "historical_roster_denominators_checked": historical_roster_entry is not None,
        }

    def original_plan(self, source_id: str, *, source_path: str, host: str, purpose: str,
                      consumer_use: str, semantic_use_scope: Iterable[str],
                      custody_locator_binding: str | None = None,
                      metadata_freeze_refs: Iterable[Any] | None = None) -> dict[str, Any]:
        config = self.load_original(source_id)
        request = source_read_request_from_config(
            config, host=host, purpose=purpose, consumer_use=consumer_use,
            semantic_use_scope=tuple(semantic_use_scope),
            custody_locator_binding=custody_locator_binding,
            metadata_freeze_refs=tuple(metadata_freeze_refs) if metadata_freeze_refs is not None else None,
        )
        reader = reader_configuration_from_config(config)
        return {
            "source_id": source_id,
            "source_path": source_path,
            "source_read_request": {
                "source_id": request.source_id,
                "source_sha256": request.source_sha256,
                "source_format": request.source_format,
                "custody_locator_binding": request.custody_locator_binding,
                "host": request.host,
                "purpose": request.purpose,
                "consumer_use": request.consumer_use,
                "read_operation": request.read_operation,
                "physical_read_extent": request.physical_read_extent,
                "metadata_freeze_refs": [x.as_dict() for x in request.metadata_freeze_refs],
                "semantic_use_scope": list(request.semantic_use_scope),
            },
            "reader_configuration": {
                "source_sha256": reader.source_sha256,
                "encoding": reader.encoding,
                "authority_status": reader.authority_status,
                "configuration_ref": reader.configuration_ref.as_dict() if reader.configuration_ref else None,
            },
            "required_external_arguments": [
                "source_path under the separately authorized source root",
                "a current SourceReadDecisionResolver decision for this exact request",
                "host/purpose/consumer_use/semantic_use_scope accepted by the issuer",
            ],
            "source_read_performed": False,
            "original_workload_issued": False,
            "note": "Plan only; no source bytes are opened. The existing source-read admission owner must authorize and decode separately.",
        }


__all__ = [
    "ROOT", "DATA_DIR", "VALIDATION_DIR", "INTEGRATION_DIR", "INDEX_PATH", "SQLITE_PATH",
    "PLAN_SEAL", "FROZEN_P0", "FROZEN_P3", "SOURCE_IDS", "PENDING_SOURCE_IDS",
    "SourceLibraryError", "SourceNotPrepared", "SourceArtifactError", "SourceRecord",
    "build_index", "SourceConfigLibrary", "assert_exact_index_paths",
]


# ---------------------------------------------------------------------------
# Explicit G1 census: historical functions, current ports, and absent ports.
# ---------------------------------------------------------------------------

# The historical roster recorded 26 original item implementation IDs with no
# exact question-relation match.  They remain preparation evidence.  No entry
# is a response slot, an administered item, an empirical positive, or an
# invented join.
UNJOINED_R157_ORIGINAL_ITEMS: Mapping[str, tuple[str, ...]] = {
    "SRC01": (
        "question_impl.phase0.238565c640e3d79b72d0",
        "question_impl.phase0.c1b201b575e7490270a8",
        "question_impl.phase0.e8a81e3fdbb1f7e81e74",
    ),
    "SRC24": (
        "question_impl.phase0.0fa0a9f546132c54f98c",
        "question_impl.phase0.1f60935613eb8655add9",
        "question_impl.phase0.23f75ff1ae9fa5f9e832",
        "question_impl.phase0.30e308d2f5b1add44a69",
        "question_impl.phase0.339be33bf48093941579",
        "question_impl.phase0.62f74db198472da0b525",
        "question_impl.phase0.715c3c525b8d7aea42cc",
        "question_impl.phase0.7207b6d4db8252fc0c90",
        "question_impl.phase0.7d541ce591ee2c5b7920",
        "question_impl.phase0.7dbb9eae2776776e6ea9",
        "question_impl.phase0.9147f6bcfc5d312f0ffd",
        "question_impl.phase0.a4d13df93b0b5f774305",
        "question_impl.phase0.b347c6c99a427d8b7c48",
        "question_impl.phase0.b5595cebe965f664cb27",
        "question_impl.phase0.e02d1acbdbe0dd0d28ca",
        "question_impl.phase0.e8dc88eb458ddb593acd",
        "question_impl.phase0.ec543f8a2afb10e7974a",
        "question_impl.phase0.f86530d3805d17e8e918",
    ),
    "SRC26": (
        "question_impl.phase0.50b49a78bd42f4ccc762",
        "question_impl.phase0.79ced092c7ce65377c1c",
        "question_impl.phase0.8399e795f61d5c853609",
        "question_impl.phase0.9e4cec8d21b7bd803dd5",
        "question_impl.phase0.f90eff21049e70ac36bf",
    ),
}

R157_IRREDUCIBLE_DETERMINANTS: Mapping[str, tuple[str, ...]] = {
    "source_identity": (
        "source_id", "family", "wave", "source_family_id", "study_product_id",
        "release_id", "instrument_release_id", "source_artifact_id",
        "expected_source_sha256", "source_format", "source_row_count",
        "source_column_count", "source_bytes", "codebook_rows",
    ),
    "custody_and_reader": (
        "source_snapshot_retention_ref", "metadata_witness_ref", "locator",
        "reader.decoder_owner", "reader.configuration_ref",
        "reader.encoding.value", "reader.encoding.sha256",
        "reader.encoding.authority_status",
    ),
    "binding_and_edition": (
        "binding.identity_class", "binding.source_sha256", "binding.row_count",
        "binding.source_snapshot_ref", "binding.fixture_provenance",
    ),
    "row_and_respondent": (
        "respondents.subject_unit", "respondents.respondent_namespace",
        "respondents.respondent_key_pattern", "respondents.source_native_key_slot",
        "respondents.identity_map_authority_ref", "respondents.row_identity_grade",
    ),
    "instrument_question_and_topology": (
        "questions[].question_id", "questions[].empirical_universe_ref",
        "questions[].native_question_ref", "questions[].instrument_question_version",
        "questions[].canonical_question_ref_or_typed_absence",
        "questions[].component_subitem_ref_or_typed_absence",
        "questions[].semantic_authority_ref", "questions[].topology_authority_ref",
    ),
    "physical_slot": (
        "physical_slots[].ordinal", "physical_slots[].name",
        "physical_slots[].label", "physical_slots[].storage_type",
        "physical_slots[].original_type", "physical_slots[].storage_width",
        "physical_slots[].measure", "physical_slots[].value_labels",
        "physical_slots[].missing_declarations", "physical_slots[].mr_declarations",
        "physical_slots[].codebook_mapping", "physical_slots[].disposition",
    ),
    "response_and_occurrence": (
        "response_slots[].slot", "response_slots[].question_id",
        "response_slots[].values[].raw_value",
        "response_slots[].values[].missing_state",
        "response_slots[].values[].source_missing_declaration",
        "response_slots[].values[].response_state",
        "response_slots[].values[].occurrences", "response_slots[].values[].canonical_value",
    ),
    "coordinate": (
        "coordinate_slots[].slot", "coordinate_slots[].native_coordinate_ref",
        "coordinate_slots[].unit_taxonomy_ref", "coordinate_slots[].effective_time",
        "coordinate_slots[].source_semantic_authority_ref",
        "coordinate_slots[].values", "coordinate_slots[].copy_observed_raw",
    ),
    "weight": (
        "weight_slots[].slot", "weight_slots[].weight_basis_id",
        "weight_slots[].weight_source_ref", "weight_slots[].design_authority_ref",
        "weight_slots[].estimand_authority_ref", "weight_slots[].effective_scope_ref",
        "weight_slots[].values", "weight_slots[].copy_observed_numeric",
    ),
    "routing_eligibility": (
        "routing[].question_id", "routing[].row_selector", "routing[].typed_state",
        "routing[].risk_set_ref", "routing[].routing_rule_ref",
        "routing[].member_set_replay_ref", "routing[].authority_ref",
        "routing[].parent_predicate_refs", "routing[].dependency_refs",
    ),
    "authority_and_replay": (
        "authority.snapshots", "authority.required_refs",
        "authority.projection_authority_ref", "authority.replay_authority_ref",
        "authority.projection_identity_ref", "authority.tie_order_ref",
        "authority.replay_protocol_version", "replay.predicate", "replay.comparator",
        "replay.discovery", "replay.structural",
    ),
    "ownership": ("slot_owner_sets",),
    "scope_and_conservation": (
        "supported_scope", "coverage", "residuals", "items", "evidence", "runtime",
    ),
}

R157_HISTORICAL_FUNCTION_MAP: Mapping[str, Mapping[str, str]] = {
    "library.record_registry": {
        "historical": "SourceLibraryError, SourceNotPrepared, SourceArtifactError, SourceRecord",
        "current_port": "this module: same names",
        "status": "PORTED",
    },
    "library.SourceConfigLibrary": {
        "historical": "SourceConfigLibrary.{record,source_ids,available_source_ids,pending_source_ids,load_original,load_fixture_config,load_fixture_stream,build_fixture_release,validate_source,original_plan}",
        "current_port": "this module: SourceConfigLibrary; validate_source executes the historical roster comparison when the caller supplies the independently held roster entry, otherwise returns a typed HOLD instead of a false pass",
        "status": "PORTED_WITH_EXTERNAL_HOLD",
    },
    "library.exact_case_paths": {
        "historical": "assert_exact_index_paths, _exact_case_path, _exact_case_join",
        "current_port": "this module: same names",
        "status": "PORTED",
    },
    "library.build_index": {
        "historical": "build_index and _candidate_* discovery over rawlsing_next/source_configuration/data plus source_pre553_validation",
        "current_port": "explicit refusal; no historical data/discovery tree exists in the current protected checkout",
        "status": "ABSENT_CURRENT_PORT",
    },
    "library.cli": {
        "historical": "rawlsing_next/source_configuration/cli.py",
        "current_port": "none; no current consumer or authorized data root",
        "status": "ABSENT_CURRENT_PORT",
    },
    "factory.projection": {
        "historical": "build_governed_c11_projection, construct_governed_c11_projection",
        "current_port": "this module: same names",
        "status": "PORTED",
    },
    "factory.row_native_keys": {
        "historical": "row_native_keys_from_transport, _effective_row_native_keys",
        "current_port": "this module: same names",
        "status": "PORTED",
    },
    "factory.release": {
        "historical": "build_validated_c11_release_from_config, build_source_backed_c11_repository_from_config, _verify_transport",
        "current_port": "this module: same names plus verify_config_projection_binding",
        "status": "PORTED_REPAIRED_BINDING",
    },
    "reader.configuration": {
        "historical": "reader_configuration_from_config, source_read_request_from_config",
        "current_port": "this module: same names",
        "status": "PORTED",
    },
    "reader.decode": {
        "historical": "decode_config_with_source_read_permission",
        "current_port": "this module: same name; admission classes ported from absent pre553_source_read_admission.py",
        "status": "PORTED_MISSING_OWNER",
    },
    "validator.closed_schema": {
        "historical": "validate_source_config and all closed-schema helpers",
        "current_port": "this module: validate_source_config",
        "status": "PORTED",
    },
    "fixture.validator": {
        "historical": "fixture_document_sha256, fixture_stream_from_document, load_fixture_stream",
        "current_port": "this module: same names",
        "status": "PORTED",
    },
    "decoder.bounded_transport": {
        "historical": "pre553_physical_decoder iter_batches / _decode",
        "current_port": "rawlsing_next/pre553_physical_decoder.py: chunked SAV and DTA; no full-frame fallback",
        "status": "REPAIRED_CURRENT_OWNER",
    },
}

R157_ABSENT_CURRENT_PORTS: Mapping[str, str] = {
    "rawlsing_next.source_configuration package": (
        "Absent from the protected checkout. The seam is recovered in this adapter; "
        "historical config/data files remain preparation evidence and are not re-created."
    ),
    "source_configuration.data all35 configs": (
        "Historical 18276-item / 18413-slot preparation ledger is not present in the "
        "current tree. It is not copied, and no unverified config is promoted to current authority."
    ),
    "source_pre553_validation discovery tree": (
        "The historical index/fixture/native-results discovery layout is absent; "
        "build_index therefore refuses. A caller-supplied portable index is still loadable."
    ),
    "SourceConfigLibrary.validate_source historical roster comparison": (
        "SOURCE_ROSTER.json and the per-source exception ledgers are absent from the "
        "current protected checkout. Portable index/config/fixture checks remain. The "
        "exact historical physical-slot and original-item comparison executes when a "
        "caller supplies the independently held roster entry; without it the result is "
        "a typed HOLD and never a false pass."
    ),
    "rawlsing_next/pre553_source_read_admission.py": (
        "Absent from the protected checkout. Its transport-only classes and exact-current "
        "checks are ported here; no production issuer, credential, or grant is created."
    ),
    "original35 source/science/U/Epre issuance": (
        "External HOLD. This adapter consumes explicit sourcefree fixtures and never claims "
        "original35 entitlement, respondent access, or native scientific acceptance."
    ),
}


def unjoined_r157_original_item_census() -> Mapping[str, Any]:
    """Return the exact 26-item preparation census without inventing a join."""
    items = tuple(
        (source_id, implementation_id)
        for source_id in sorted(UNJOINED_R157_ORIGINAL_ITEMS)
        for implementation_id in UNJOINED_R157_ORIGINAL_ITEMS[source_id]
    )
    if len(items) != 26 or len(set(items)) != 26:
        raise SourceConfigurationError("unjoined R157 original-item census is not exactly 26 distinct items")
    return {
        "contract": "R157_UNJOINED_ORIGINAL_ITEMS@1.0.0",
        "historical_commit": R157_HISTORICAL_COMMIT,
        "count": len(items),
        "by_source": {key: len(value) for key, value in sorted(UNJOINED_R157_ORIGINAL_ITEMS.items())},
        "items": items,
        "status": "PREPARATION_HELD__NOT_SCIENCE",
        "claim_boundary": (
            "These implementation IDs had no exact question-relation match. They are not "
            "administered items, response slots, eligible operations, or empirical positives."
        ),
    }


def _resolved_identity(doc: Mapping[str, Any]) -> tuple[str, int, str, str, str, str]:
    """Resolve active SHA/rows, artifact, study, release, instrument from config."""
    identity = doc["identity"]
    binding = doc["binding"]
    active_sha = binding["source_sha256"]
    active_rows = binding["row_count"]
    if binding["identity_class"] == IDENTITY_CLASS_ORIGINAL:
        if active_sha != identity["expected_source_sha256"]:
            raise SourceConfigurationBindingError(
                "original binding SHA differs from the original source identity")
        if active_rows != identity["source_row_count"]:
            raise SourceConfigurationBindingError(
                "original binding row count differs from the original source identity")
        return (
            active_sha,
            active_rows,
            identity["source_artifact_id"],
            identity["study_product_id"],
            identity["release_id"],
            identity["instrument_release_id"],
        )
    fixture = binding["fixture_provenance"]
    if active_sha == identity["expected_source_sha256"]:
        raise SourceConfigurationBindingError(
            "fixture binding may not reuse the original source SHA")
    return (
        active_sha,
        active_rows,
        f"R157_FIXTURE:{fixture['fixture_id']}",
        fixture["fixture_study_product_id"],
        fixture["fixture_release_id"],
        fixture["fixture_instrument_release_id"],
    )


def verify_config_projection_binding(
    config: SourceConfig | Mapping[str, Any],
    projection: GovernedC11Projection,
    *,
    source_sha256: str | None = None,
    row_count: int | None = None,
    row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None,
) -> None:
    """Refuse a projection built for another exact edition/source/binding.

    The historical factory verified only source SHA and row count.  That is not
    sufficient once a caller can supply a projection: the instrument edition,
    study product, release, artifact id and row-native keys are also irreducible
    determinants.  This guard does not infer any new semantic fact; it only
    requires the projection to equal the validated config.
    """
    if not isinstance(projection, GovernedC11Projection):
        raise SourceConfigurationFactoryError("explicit GovernedC11Projection is required")
    doc = _doc(config)
    active_sha = doc["binding"]["source_sha256"] if source_sha256 is None else source_sha256
    active_rows = doc["binding"]["row_count"] if row_count is None else row_count
    expected = _resolved_identity(doc)
    if (active_sha, active_rows) != expected[:2]:
        raise SourceConfigurationBindingError(
            "physical transport SHA/row count differs from the validated config binding")
    if projection.expected_source_sha256 != active_sha:
        raise SourceConfigurationBindingError(
            "projection expected source SHA differs from the validated config binding")
    if len(projection.row_bindings) != active_rows:
        raise SourceConfigurationBindingError(
            "projection row/respondent map cardinality differs from the validated config binding")
    actual = (
        projection.source_artifact_id,
        projection.study_product_id,
        projection.release_id,
        projection.instrument_release_id,
    )
    if actual != expected[2:]:
        raise SourceConfigurationBindingError(
            "projection study/release/artifact/instrument edition differs from the validated config")

    # A projection is caller-owned.  The identity checks above do not prove that
    # its semantic rules are the config's rules, so compare the closed
    # config-derived rule surface before any cell is projected.
    if projection.projection_identity_ref != _ref(doc["authority"]["projection_identity_ref"]):
        raise SourceConfigurationBindingError(
            "projection identity reference differs from the validated config")
    if projection.source_family_id != doc["identity"]["source_family_id"]:
        raise SourceConfigurationBindingError(
            "projection source family differs from the validated config")
    required = tuple(_authority_ref(item) for item in doc["authority"]["required_refs"])
    if sorted(projection.required_authority_refs, key=lambda item: item.key) != sorted(
        required, key=lambda item: item.key
    ):
        raise SourceConfigurationBindingError(
            "projection required authority closure differs from the validated config")
    if projection.projection_authority_ref != _authority_ref(doc["authority"]["projection_authority_ref"]):
        raise SourceConfigurationBindingError(
            "projection authority differs from the validated config")
    if projection.replay_authority_ref != _authority_ref(doc["authority"]["replay_authority_ref"]):
        raise SourceConfigurationBindingError(
            "projection replay authority differs from the validated config")
    if projection.tie_order_ref != _ref(doc["authority"]["tie_order_ref"]):
        raise SourceConfigurationBindingError(
            "projection tie-order rule differs from the validated config")
    if projection.replay_protocol_version != doc["authority"]["replay_protocol_version"]:
        raise SourceConfigurationBindingError(
            "projection replay protocol differs from the validated config")

    fixture = doc["binding"].get("fixture_provenance")
    expected_snapshot_ref = (
        _ref(doc["binding"]["source_snapshot_ref"])
        if fixture is not None
        else _ref(doc["identity"]["source_snapshot_retention_ref"])
    )
    if projection.source_snapshot_retention_ref != expected_snapshot_ref:
        raise SourceConfigurationBindingError(
            "projection source snapshot retention reference differs from the validated config")

    expected_universes = tuple(
        EmpiricalUniverse(**payload) for payload in doc["universe"]["universes"]
    )
    if sorted(projection.universes, key=lambda item: item.ref.key) != sorted(
        expected_universes, key=lambda item: item.ref.key
    ):
        raise SourceConfigurationBindingError(
            "projection universes differ from the validated config")
    expected_authorities = tuple(
        AuthoritySnapshot(**payload) for payload in doc["authority"]["snapshots"]
    )

    def _authority_snapshot_key(item: Any) -> tuple[str, str]:
        return (item.authority_ref.key, item.object_id)

    def _canonical_object_key(item: Any) -> tuple[str, str]:
        return (item.object_id, item.content_hash)

    if sorted(projection.authority_snapshots, key=_authority_snapshot_key) != sorted(
        expected_authorities, key=_authority_snapshot_key
    ):
        raise SourceConfigurationBindingError(
            "projection authority snapshots differ from the validated config")
    questions_by_id = {
        section["question_id"]: _question(section) for section in doc["questions"]
    }
    if sorted(projection.questions, key=lambda item: item.ref.key) != sorted(
        questions_by_id.values(), key=lambda item: item.ref.key
    ):
        raise SourceConfigurationBindingError(
            "projection question bindings differ from the validated config")

    # Respondents, row bindings and routing are config-derived.  The
    # source-native key witnesses are physical facts.  A caller that supplies
    # them is checked against the config-derived respondent construction; a
    # direct verify caller without them falls back to the projection's own
    # witnesses, while the first-consumer wrapper below requires/derives them.
    if len(projection.respondents) != active_rows:
        raise SourceConfigurationBindingError(
            "projection respondent cardinality differs from the validated config")
    if row_native_keys is None:
        row_native_keys = {
            row: respondent.source_native_respondent_key_ref_or_typed_absence
            for row, respondent in enumerate(projection.respondents, 1)
        }
    else:
        if set(row_native_keys) != set(range(1, active_rows + 1)):
            raise SourceConfigurationBindingError(
                "supplied row-native keys do not cover exactly the active rows")
        row_native_keys = {
            int(row): value for row, value in row_native_keys.items()
        }
    expected_respondents = _respondents(
        doc,
        active_rows=active_rows,
        universes=expected_universes,
        row_native_keys=row_native_keys,
    )
    if projection.respondents != expected_respondents:
        raise SourceConfigurationBindingError(
            "projection respondents differ from the validated config")
    expected_bindings = tuple(
        RowRespondentBinding(row, respondent.ref)
        for row, respondent in enumerate(expected_respondents, 1)
    )
    if projection.row_bindings != expected_bindings:
        raise SourceConfigurationBindingError(
            "projection row/respondent bindings differ from the validated config")
    expected_routing = _routing(
        doc, questions_by_id, expected_respondents, active_rows=active_rows)
    if sorted(projection.routing, key=_canonical_object_key) != sorted(
        expected_routing, key=_canonical_object_key
    ):
        raise SourceConfigurationBindingError(
            "projection routing rules differ from the validated config")

    expected_surfaces = (
        ("response", {item.slot.key: item for item in _response_slots(doc, questions_by_id)},
         {item.slot.key: item for item in projection.response_slots}),
        ("coordinate", {item.slot.key: item for item in _coordinate_slots(doc)},
         {item.slot.key: item for item in projection.coordinate_slots}),
        ("weight", {item.slot.key: item for item in _weight_slots(doc)},
         {item.slot.key: item for item in projection.weight_slots}),
        ("slot-owner", {item.slot.key: item for item in _slot_owner_sets(doc)},
         {item.slot.key: item for item in projection.slot_owner_sets}),
    )
    for name, expected_surface, actual_surface in expected_surfaces:
        if actual_surface != expected_surface:
            raise SourceConfigurationBindingError(
                f"projection {name} rules differ from the validated config")
    if projection.source_relations != _source_relations(doc):
        raise SourceConfigurationBindingError(
            "projection source relations differ from the validated config")
    for name in ("predicate", "comparator", "discovery", "structural"):
        if getattr(projection, f"{name}_replay") != _replay_absence(doc, name):
            raise SourceConfigurationBindingError(
                f"projection {name} replay state differs from the validated config")


def _keys_from_reiterable_cells(
    config: SourceConfig | Mapping[str, Any],
    *,
    source_sha256: str,
    row_count: int,
    cell_iter_factory: Callable[[], Iterable[PhysicalCell]],
) -> Mapping[int, ExactRef | TypedAbsence] | None:
    doc = _doc(config)
    if doc["respondents"].get("source_native_key_slot") is None:
        return None
    stream = ExactPhysicalCellStream(
        source_sha256=source_sha256,
        row_count=row_count,
        cell_iter_factory=cell_iter_factory,
    )
    return row_native_keys_from_transport(config, stream=stream)


def project_c11_candidate_from_config(
    config: SourceConfig | Mapping[str, Any],
    projection: GovernedC11Projection,
    *,
    cells: Iterable[PhysicalCell] | None = None,
    cells_factory: Callable[[], Iterable[PhysicalCell]] | None = None,
    row_native_keys: Mapping[int, ExactRef | TypedAbsence] | None = None,
    source_sha256: str,
    row_count: int,
):
    """Project through the actual current first consumer after exact binding.

    For a config with a source-native key slot, the key witnesses are not
    trusted from the caller-owned projection.  They are derived from a fresh
    physical cell pass when the cells are re-iterable / a factory is supplied,
    and compared with any caller-supplied mapping.  A one-shot cell iterator
    without a factory is refused unless the caller supplies the independently
    derived key mapping; that mapping is then still checked against the config
    and projection.
    """
    if cells is None and cells_factory is None:
        raise SourceConfigurationFactoryError("cells or cells_factory is required")
    doc = _doc(config)
    keyed = doc["respondents"].get("source_native_key_slot") is not None
    derived_keys = None
    if keyed:
        if cells_factory is not None:
            derived_keys = _keys_from_reiterable_cells(
                config,
                source_sha256=source_sha256,
                row_count=row_count,
                cell_iter_factory=cells_factory,
            )
        elif isinstance(cells, Sequence) and not isinstance(cells, (str, bytes, bytearray)):
            derived_keys = _keys_from_reiterable_cells(
                config,
                source_sha256=source_sha256,
                row_count=row_count,
                cell_iter_factory=lambda: tuple(cells),
            )
        if row_native_keys is None:
            if derived_keys is None:
                raise SourceConfigurationBindingError(
                    "configured source_native_key_slot requires row_native_keys "
                    "or re-iterable cells/cells_factory for exact key verification")
            row_native_keys = derived_keys
        elif derived_keys is not None and dict(derived_keys) != dict(row_native_keys):
            raise SourceConfigurationBindingError(
                "supplied row-native keys differ from the physical cell key witnesses")
    verify_config_projection_binding(
        config,
        projection,
        source_sha256=source_sha256,
        row_count=row_count,
        row_native_keys=row_native_keys,
    )
    projected_cells = cells_factory() if cells_factory is not None else cells
    from rawlsing_next.pre553_source_backed_c11_facade import (
        project_c11_candidate_from_physical_cells,
    )
    return project_c11_candidate_from_physical_cells(
        source_sha256=source_sha256,
        row_count=row_count,
        cells=projected_cells,
        projection=projection,
    )


def decode_fixture_config(
    config: SourceConfig | Mapping[str, Any],
    source_path: str | Path,
    *,
    batch_size: int = 10_000,
) -> PhysicalSourceIncidence:
    """Decode a NONRESPONDENT_FIXTURE file; never an original source read.

    This stand-in performs no source-read admission because a fixture is
    repository-generated sourcefree evidence, not an original35 source.  It
    refuses an ORIGINAL_SOURCE config: that path must use
    ``decode_config_with_source_read_permission`` with an independently injected
    current decision.
    """
    doc = _doc(config)
    if doc["binding"]["identity_class"] != IDENTITY_CLASS_FIXTURE:
        raise SourceConfigurationBindingError(
            "decode_fixture_config refuses ORIGINAL_SOURCE; use the injected source-read decision path")
    source_format = doc["identity"]["source_format"]
    decoder = decode_sav if source_format == "SAV" else decode_dta
    incidence = decoder(
        source_path,
        expected_source_sha256=doc["binding"]["source_sha256"],
        encoding=None,
    )
    if incidence.source_sha256 != doc["binding"]["source_sha256"]:
        incidence.close()
        raise SourceConfigurationBindingError("decoded fixture SHA differs from binding")
    if incidence.row_count != doc["binding"]["row_count"]:
        incidence.close()
        raise SourceConfigurationBindingError("decoded fixture row count differs from binding")
    return incidence


__all__ = [
    "R157_HISTORICAL_COMMIT", "SCHEMA_ID", "FIXTURE_SCHEMA_ID",
    "CONFIG_PURPOSE_SOURCE", "CONFIG_PURPOSE_FIXTURE", "CONFIG_PURPOSE_EXAMPLE",
    "IDENTITY_CLASS_ORIGINAL", "IDENTITY_CLASS_FIXTURE", "ADAPTER_IMPLEMENTATION_ID",
    "SourceConfigurationError", "SourceConfigurationSchemaError",
    "SourceConfigurationBindingError", "SourceConfigurationFactoryError",
    "SourceConfigurationEvidenceError", "SourceReadAdmissionRefusal",
    "SOURCE_RESPONSE_DECODE", "EXACT_FILE", "CURRENT_GRANTED", "TERMINAL_STATES",
    "SourceConfig", "validate_source_config", "load_source_config",
    "canonical_config_hash", "config_file_sha256",
    "SourceReadRequest", "IssuedSourceReadDecision", "SourceReaderConfiguration",
    "SourceReadDecisionResolver", "decode_with_source_read_permission",
    "build_governed_c11_projection", "construct_governed_c11_projection",
    "row_native_keys_from_transport", "build_validated_c11_release_from_config",
    "build_source_backed_c11_repository_from_config", "reader_configuration_from_config",
    "source_read_request_from_config", "decode_config_with_source_read_permission",
    "fixture_document_sha256", "fixture_stream_from_document", "load_fixture_stream",
    "SourceLibraryError", "SourceNotPrepared", "SourceArtifactError", "SourceRecord",
    "assert_exact_index_paths", "SourceConfigLibrary", "build_index",
    "UNJOINED_R157_ORIGINAL_ITEMS", "R157_IRREDUCIBLE_DETERMINANTS",
    "R157_HISTORICAL_FUNCTION_MAP", "R157_ABSENT_CURRENT_PORTS",
    "unjoined_r157_original_item_census", "verify_config_projection_binding",
    "project_c11_candidate_from_config", "decode_fixture_config",
]
