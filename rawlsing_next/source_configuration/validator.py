"""Closed schema validation for R157 source configurations.

The validator is intentionally explicit.  It parses the serialized form into the
*actual* native dataclasses where a native owner exists, so a config cannot pass
validation while claiming fields the receiving owner does not have.
"""
from __future__ import annotations

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

from .errors import SourceConfigurationSchemaError
from .schema import (
    CONFIG_PURPOSE_EXAMPLE,
    CONFIG_PURPOSE_FIXTURE,
    CONFIG_PURPOSE_SOURCE,
    IDENTITY_CLASS_FIXTURE,
    IDENTITY_CLASS_ORIGINAL,
    SCHEMA_ID,
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

_RUNTIME_CALLABLES = {
    "projection_builder": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
    "release_builder": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
    "repository_builder": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
    "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
    "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
    "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
    "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
}


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
        if _text(runtime[name], f"$.runtime.{name}") != expected:
            _fail(f"$.runtime.{name}", f"must be {expected!r}; no replacement engine is permitted")
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
