"""Governed source-specific realization law for CLOSED_35 Arab Barometer Wave 1.

This module does not read or decode the SAV. It freezes the candidate-neutral
source law that later A/B/C physical realizations must share.

The exact Authority71/72 packet is deliberately asymmetric: physical source
facts are preserved strongly while unresolved source-text display transforms,
design details, and undocumented routing remain BOUNDED_UNKNOWN rather than
being guessed or turned into blockers.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence


CONTRACT_ID = "CLOSED35_R3_ARAB1_SOURCE_REALIZATION@1.0.0"
CANONICAL_FILENAME = "Arab Barometer Wave 1.sav"
CANONICAL_SHA256 = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
SOURCE_FORMAT = "SAV"
AUTHORITY_CLASS = "L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED"
SEMANTIC_OWNER_SURFACE = "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0"

REPLAY_IDENTITY_RULE = "SOURCE_SHA256+ROW_ORDINAL"
NATIVE_ID_FIELD = "SER"
COUNTRY_FIELD = "COUNTRY"
MOROCCO_COUNTRY_CODE = 4

NATIVE_READER_MODE = "SAV_NATIVE_GOVERNED"
SOURCE_REPORTED_ENCODING = "UTF-8"
SOURCE_REPORTED_CHARACTER_CODE = 65001
COMPATIBILITY_OVERRIDE = "NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE"

BOUNDED_UNKNOWN = "BOUNDED_UNKNOWN"
ROUTING_BOUNDED_UNKNOWN = "ROUTING_BOUNDED_UNKNOWN"
DESIGN_BOUNDED_UNKNOWN = "DESIGN_BOUNDED_UNKNOWN"
DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN = "DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN"

APPLICABLE_EDGE_CLASSES = ("EC01", "EC07", "EC10", "EC14")

# Accepted R35 integration seams. They are physical/governance contracts only;
# none grants source semantics.
R35_PHYSICAL_METADATA_SCHEMA = "PRE553_PHYSICAL_METADATA@1.0.0"
R35_DERIVATIVE_PARENTAGE_BUNDLE_SCHEMA = "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0"
R35_PHYSICAL_SCOPE_SCHEMA = "FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0"
R35_PHYSICAL_EXPECTATION_SCHEMA = "FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0"
R35_PHYSICAL_REALIZATION_SCHEMA = "FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0"
R35_PHYSICAL_EQUIVALENCE_RECEIPT_SCHEMA = "FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0"

R35_REQUIRED_PHYSICAL_DIMENSIONS = (
    "physical_metadata",
    "variable_inventory_order",
    "raw_storage_values",
    "row_replay_identity",
    "native_id_replay_evidence",
    "form_module_skip_routing_carriers",
)

EXACT_READER_CONFIGURATION: Mapping[str, Any] = {
    "decoder_mode": NATIVE_READER_MODE,
    "source_reported_encoding": SOURCE_REPORTED_ENCODING,
    "source_reported_character_code": SOURCE_REPORTED_CHARACTER_CODE,
    "compatibility_override": COMPATIBILITY_OVERRIDE,
    "automatic_encoding_guessing": False,
    "semantic_authority": False,
}

BOUNDED_UNKNOWN_SET = (
    "DISPLAY_TEXT_NORMALIZATION_BEYOND_ACCEPTED_SOURCE_EVIDENCE",
    "EXACT_WEIGHT_DESIGN_ESTIMAND_AND_IMPLEMENTATION",
    "UNDOCUMENTED_ROUTING_DETAILS",
    "EXACT_DATASET_ALIAS_BINDING_FOR_V715ONLYMOROCCO_TO_PRINTED_Q715MOROCCOONLY",
    "CROSS_WAVE_SEMANTIC_EQUIVALENCE",
)


class Arab1RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise Arab1RealizationError(f"non-canonical realization material: {type(value).__name__}")


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        _canonical(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise Arab1RealizationError(f"{name} must be a non-empty string")
    return value


@dataclass(frozen=True)
class ReplayIdentity:
    source_sha256: str
    row_ordinal: int

    def __post_init__(self) -> None:
        if self.source_sha256 != CANONICAL_SHA256:
            raise Arab1RealizationError("canonical Arab Barometer Wave 1 source root mismatch")
        if not isinstance(self.row_ordinal, int) or self.row_ordinal < 0:
            raise Arab1RealizationError("row ordinal must be a non-negative integer")

    @property
    def key(self) -> tuple[str, int]:
        return (self.source_sha256, self.row_ordinal)


@dataclass(frozen=True)
class NativeRespondentAttribute:
    replay_identity: ReplayIdentity
    ser: Any
    country: Any = None

    @property
    def hard_replay_key(self) -> tuple[str, int]:
        return self.replay_identity.key


def require_distinct_rows(rows: Sequence[NativeRespondentAttribute]) -> tuple[tuple[str, int], ...]:
    """Preserve duplicate/noninjective SER rows as distinct physical respondents."""
    keys = tuple(row.hard_replay_key for row in rows)
    if len(set(keys)) != len(keys):
        raise Arab1RealizationError("duplicate hard replay identity")
    # SER uniqueness is intentionally not checked.
    return keys


def preserve_literal_source_text(source_text: str) -> str:
    """Return source text byte-decoding result exactly; do not typography-normalize."""
    if not isinstance(source_text, str):
        raise Arab1RealizationError("source text must be a string")
    return source_text


def authorize_display_text_transform(
    source_text: str,
    transformed_text: str,
    *,
    authority_id: str | None = None,
) -> str:
    """A changed display rendering requires an explicit separately governed authority."""
    preserve_literal_source_text(source_text)
    preserve_literal_source_text(transformed_text)
    if transformed_text == source_text:
        return source_text
    if not authority_id:
        raise Arab1RealizationError(DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN)
    _require_nonempty(authority_id, "authority_id")
    return transformed_text


@dataclass(frozen=True)
class RoutingResolution:
    variable_name: str
    country_code: Any
    status: str
    documented_scope: str | None
    alias_status: str
    missingness_used_as_authority: bool = False


def resolve_routing(
    variable_name: str,
    *,
    country_code: Any = None,
    observed_missing_state: Any = None,
) -> RoutingResolution:
    """Resolve only the source-documented Morocco/non-Morocco split.

    Missingness is never routing authority. Any other route remains bounded
    UNKNOWN unless later source-specific documentary authority closes it.
    """
    _require_nonempty(variable_name, "variable_name")
    del observed_missing_state

    if variable_name == "q715withoutmorocco":
        if country_code is None:
            return RoutingResolution(
                variable_name,
                country_code,
                ROUTING_BOUNDED_UNKNOWN,
                "DOCUMENTED_NON_MOROCCO_SCOPE__COUNTRY_REQUIRED",
                "SOURCE_VARIABLE_NAME_EXACT",
            )
        if country_code == MOROCCO_COUNTRY_CODE:
            return RoutingResolution(
                variable_name,
                country_code,
                "DOCUMENTED_NOT_APPLICABLE_TO_MOROCCO",
                "WITHOUT_MOROCCO",
                "SOURCE_VARIABLE_NAME_EXACT",
            )
        return RoutingResolution(
            variable_name,
            country_code,
            "DOCUMENTED_APPLICABLE_NON_MOROCCO",
            "WITHOUT_MOROCCO",
            "SOURCE_VARIABLE_NAME_EXACT",
        )

    if variable_name == "V715onlymorocco":
        alias_status = "PRINTED_Q715MOROCCOONLY_ALIAS_BINDING_BOUNDED_UNKNOWN"
        if country_code is None:
            return RoutingResolution(
                variable_name,
                country_code,
                ROUTING_BOUNDED_UNKNOWN,
                "DOCUMENTED_MOROCCO_ONLY_SCOPE__COUNTRY_REQUIRED",
                alias_status,
            )
        if country_code == MOROCCO_COUNTRY_CODE:
            return RoutingResolution(
                variable_name,
                country_code,
                "DOCUMENTED_MOROCCO_ONLY_SCOPE__ALIAS_BINDING_BOUNDED_UNKNOWN",
                "MOROCCO_ONLY",
                alias_status,
            )
        return RoutingResolution(
            variable_name,
            country_code,
            "DOCUMENTED_NOT_APPLICABLE_OUTSIDE_MOROCCO__ALIAS_BINDING_BOUNDED_UNKNOWN",
            "MOROCCO_ONLY",
            alias_status,
        )

    return RoutingResolution(
        variable_name,
        country_code,
        ROUTING_BOUNDED_UNKNOWN,
        None,
        "NO_DOCUMENTED_SOURCE_LOCAL_ROUTE_BOUND",
    )


@dataclass(frozen=True)
class PhysicalDesignLikeCarrier:
    variable_name: str
    physical_value: Any = None
    physical_metadata: Mapping[str, Any] | None = None
    semantic_state: str = DESIGN_BOUNDED_UNKNOWN
    analytical_weight_authorized: bool = False
    survey_design_role_authorized: bool = False

    def __post_init__(self) -> None:
        _require_nonempty(self.variable_name, "variable_name")
        if self.semantic_state != DESIGN_BOUNDED_UNKNOWN:
            raise Arab1RealizationError("Arab1 design semantics must remain bounded UNKNOWN")
        if self.analytical_weight_authorized or self.survey_design_role_authorized:
            raise Arab1RealizationError("no Arab1 weight/design authority is admitted here")


def preserve_design_like_carrier(
    variable_name: str,
    *,
    physical_value: Any = None,
    physical_metadata: Mapping[str, Any] | None = None,
) -> PhysicalDesignLikeCarrier:
    """Preserve a carrier physically without inferring design from its name or values."""
    return PhysicalDesignLikeCarrier(
        variable_name=variable_name,
        physical_value=physical_value,
        physical_metadata=physical_metadata,
    )


def require_wave1_authority_scope(
    *,
    source_filename: str,
    source_sha256: str,
    authority_wave: str,
) -> None:
    if source_filename != CANONICAL_FILENAME or source_sha256 != CANONICAL_SHA256:
        raise Arab1RealizationError("cross-source semantic leakage")
    if authority_wave not in {"W1", "Wave 1", "I"}:
        raise Arab1RealizationError("cross-wave semantic leakage")


R35_HOOK_BINDING: Mapping[str, Any] = {
    "i01_physical_metadata": {
        "schema": R35_PHYSICAL_METADATA_SCHEMA,
        "required": True,
        "semantic_authority": False,
    },
    "i02_derivative_parentage": {
        "schema": R35_DERIVATIVE_PARENTAGE_BUNDLE_SCHEMA,
        "required_for_non_direct_raw": True,
        "semantic_authority": False,
    },
    "i03_source_scope": {
        "scope_schema": R35_PHYSICAL_SCOPE_SCHEMA,
        "expectation_schema": R35_PHYSICAL_EXPECTATION_SCHEMA,
        "candidate_realization_schema": R35_PHYSICAL_REALIZATION_SCHEMA,
        "receipt_schema": R35_PHYSICAL_EQUIVALENCE_RECEIPT_SCHEMA,
        "applicable_edge_classes": APPLICABLE_EDGE_CLASSES,
        "required_physical_dimensions": R35_REQUIRED_PHYSICAL_DIMENSIONS,
        "semantic_authority": False,
    },
}


def source_specific_realization_payload() -> Mapping[str, Any]:
    return {
        "contract": CONTRACT_ID,
        "source": {
            "canonical_filename": CANONICAL_FILENAME,
            "canonical_sha256": CANONICAL_SHA256,
            "format": SOURCE_FORMAT,
            "reader_mode": NATIVE_READER_MODE,
            "replay_identity": REPLAY_IDENTITY_RULE,
            "native_id_field": NATIVE_ID_FIELD,
        },
        "authority_class": AUTHORITY_CLASS,
        "reader_configuration": EXACT_READER_CONFIGURATION,
        "literal_text_law": {
            "source_text_preserved_exactly": True,
            "typography_normalization_without_authority": False,
            "unresolved_transform_state": DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN,
        },
        "routing_law": {
            "documented_scope": ["q715withoutmorocco", "V715onlymorocco"],
            "morocco_country_code": MOROCCO_COUNTRY_CODE,
            "missingness_is_authority": False,
            "unresolved_state": ROUTING_BOUNDED_UNKNOWN,
        },
        "design_law": {
            "physical_carriers_preserved": True,
            "carrier_name_mints_design_semantics": False,
            "unresolved_state": DESIGN_BOUNDED_UNKNOWN,
        },
        "bounded_unknowns": BOUNDED_UNKNOWN_SET,
        "semantic_owner_surface": SEMANTIC_OWNER_SURFACE,
        "r35_hooks": R35_HOOK_BINDING,
        "candidate_law": "A_B_C_SHARE_ONE_SOURCE_SPECIFIC_SEMANTIC_REALIZATION_IDENTITY",
    }


SOURCE_SPECIFIC_REALIZATION_IDENTITY = canonical_digest(source_specific_realization_payload())


@dataclass(frozen=True)
class CandidateSemanticBinding:
    candidate_id: str
    source_sha256: str = CANONICAL_SHA256
    source_specific_realization_identity: str = SOURCE_SPECIFIC_REALIZATION_IDENTITY

    def __post_init__(self) -> None:
        if self.candidate_id not in {"A", "B", "C"}:
            raise Arab1RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise Arab1RealizationError("candidate source root divergence")
        if self.source_specific_realization_identity != SOURCE_SPECIFIC_REALIZATION_IDENTITY:
            raise Arab1RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(bindings: Sequence[CandidateSemanticBinding]) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise Arab1RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise Arab1RealizationError("A/B/C source root divergence")
    if len({binding.source_specific_realization_identity for binding in bindings}) != 1:
        raise Arab1RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "APPLICABLE_EDGE_CLASSES",
    "AUTHORITY_CLASS",
    "BOUNDED_UNKNOWN",
    "BOUNDED_UNKNOWN_SET",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "CONTRACT_ID",
    "CandidateSemanticBinding",
    "DESIGN_BOUNDED_UNKNOWN",
    "DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN",
    "EXACT_READER_CONFIGURATION",
    "MOROCCO_COUNTRY_CODE",
    "NativeRespondentAttribute",
    "PhysicalDesignLikeCarrier",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "REPLAY_IDENTITY_RULE",
    "ROUTING_BOUNDED_UNKNOWN",
    "ReplayIdentity",
    "RoutingResolution",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "Arab1RealizationError",
    "authorize_display_text_transform",
    "preserve_design_like_carrier",
    "preserve_literal_source_text",
    "require_common_abc_semantic_law",
    "require_distinct_rows",
    "require_wave1_authority_scope",
    "resolve_routing",
    "source_specific_realization_payload",
]
