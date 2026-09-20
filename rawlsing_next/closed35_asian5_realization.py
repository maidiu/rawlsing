"""Governed source-specific realization law for CLOSED_35 Asian Barometer Wave 5.

This module does not read or execute the SAV. It freezes the candidate-neutral
semantic owner surface that later A/B/C realizations must share after lawful
physical extraction.

Bounded documentary unknowns remain explicit. In particular, native MR-set
identity is physical/topological authority, not authority to invent semantic
aliases; source-local respondent IDs are not replay identity; routing is never
inferred from missingness; and the source weight carrier is not a default
analytical weight without explicit authority.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence


CONTRACT_ID = "CLOSED35_R2_ASIAN5_SOURCE_REALIZATION@1.0.0"
CANONICAL_FILENAME = "Asian Barometer Wave 5.sav"
CANONICAL_SHA256 = "2576e428ff8de3c8d93a418c9120a1c2955ab7b1f35961d8c18fa562bc4b5e63"
SOURCE_FORMAT = "SAV"
AUTHORITY_CLASS = "L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED"
READER_MODE = "SAV_NATIVE_GOVERNED"
SOURCE_DECLARED_ENCODING = "UTF-8"
REPLAY_IDENTITY_RULE = "SOURCE_SHA256+ROW_ORDINAL"
BOUNDED_UNKNOWN = "BOUNDED_UNKNOWN"
SEMANTIC_OWNER_SURFACE = "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0"

R35_PHYSICAL_METADATA_SCHEMA = "PRE553_PHYSICAL_METADATA@1.0.0"
R35_DERIVATIVE_PARENTAGE_BUNDLE_SCHEMA = "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0"
R35_PHYSICAL_SCOPE_SCHEMA = "FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0"
R35_PHYSICAL_EXPECTATION_SCHEMA = "FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0"
R35_PHYSICAL_REALIZATION_SCHEMA = "FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0"
R35_PHYSICAL_EQUIVALENCE_RECEIPT_SCHEMA = (
    "FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0"
)

APPLICABLE_EDGE_CLASSES = ("EC01", "EC07", "EC08", "EC10", "EC12", "EC13", "EC14")
R35_REQUIRED_PHYSICAL_DIMENSIONS = (
    "physical_metadata",
    "variable_inventory_order",
    "raw_storage_values",
    "row_replay_identity",
    "native_id_replay_evidence",
    "native_mr_sets",
    "form_module_skip_routing_carriers",
    "weight_design_variables",
    "source_local_coordinate_carriers",
)


class Asian5RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise Asian5RealizationError(
        f"non-canonical realization material: {type(value).__name__}"
    )


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        _canonical(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class NativeMRSet:
    set_name: str
    set_kind: str
    counted_value: int
    members: tuple[str, ...]
    semantic_alias_state: str

    def __post_init__(self) -> None:
        if not self.set_name:
            raise Asian5RealizationError("MR set name is required")
        if self.set_kind != "DICHOTOMY":
            raise Asian5RealizationError("Asian W5 native MR sets must remain dichotomy sets")
        if self.counted_value != 1:
            raise Asian5RealizationError("Asian W5 native MR counted value must remain 1")
        if not self.members:
            raise Asian5RealizationError("MR set members are required")


EXPECTED_MR_SETS: tuple[NativeMRSet, ...] = (
    NativeMRSet(
        "IR3a",
        "DICHOTOMY",
        1,
        tuple(f"IR3a_{i}" for i in range(1, 6)),
        "COREQ_SUPPORTS_MULTIPLE_ANSWER_TOPOLOGY",
    ),
    NativeMRSet(
        "Q112",
        "DICHOTOMY",
        1,
        tuple(f"SE15{letter}" for letter in "ABCDEFGHIJKLM"),
        "BOUNDED_UNKNOWN__NATIVE_SET_NAME_IS_NOT_QUESTIONNAIRE_Q112_AUTHORITY",
    ),
    NativeMRSet(
        "SE15",
        "DICHOTOMY",
        1,
        tuple(f"SE15{letter}" for letter in "ABCDEFGHIJKLMNO"),
        "COREQ_SUPPORTS_SE15_A_TO_O_ASSET_BATTERY",
    ),
)
_EXPECTED_MR_BY_NAME = {spec.set_name: spec for spec in EXPECTED_MR_SETS}
EXPECTED_Q112_SE15_OVERLAP = tuple(f"SE15{letter}" for letter in "ABCDEFGHIJKLM")


def validate_native_mr_topology(actual: Sequence[NativeMRSet]) -> tuple[NativeMRSet, ...]:
    by_name = {spec.set_name: spec for spec in actual}
    if len(by_name) != len(actual):
        raise Asian5RealizationError("duplicate native MR set identity")
    if set(by_name) != set(_EXPECTED_MR_BY_NAME):
        raise Asian5RealizationError("MR flattening, deletion, or invented set identity")
    for name, expected in _EXPECTED_MR_BY_NAME.items():
        if by_name[name] != expected:
            raise Asian5RealizationError(f"native MR topology drift for {name}")
    overlap = tuple(
        member for member in by_name["Q112"].members if member in set(by_name["SE15"].members)
    )
    if overlap != EXPECTED_Q112_SE15_OVERLAP:
        raise Asian5RealizationError("Q112/SE15 overlap topology drift")
    if by_name["Q112"].set_name == by_name["SE15"].set_name:
        raise Asian5RealizationError("Q112/SE15 identity collapse")
    return tuple(by_name[name] for name in ("IR3a", "Q112", "SE15"))


def require_no_mr_semantic_alias(
    left_set_name: str,
    right_set_name: str,
    *,
    asserted_alias: bool,
) -> None:
    if {left_set_name, right_set_name} == {"Q112", "SE15"} and asserted_alias:
        raise Asian5RealizationError(
            "member overlap does not authorize Q112/SE15 semantic aliasing"
        )


def require_questionnaire_q112_nonidentity(*, asserted_same_semantics: bool) -> None:
    if asserted_same_semantics:
        raise Asian5RealizationError(
            "native MR set Q112 cannot be identified with questionnaire item 112 by name"
        )


@dataclass(frozen=True)
class ReplayBinding:
    source_sha256: str
    zero_based_row_ordinal: int
    native_country: Any = None
    native_idnumber: Any = None

    def __post_init__(self) -> None:
        if self.source_sha256 != CANONICAL_SHA256:
            raise Asian5RealizationError("source root mismatch")
        if not isinstance(self.zero_based_row_ordinal, int) or self.zero_based_row_ordinal < 0:
            raise Asian5RealizationError("row ordinal must be a non-negative integer")

    @property
    def replay_key(self) -> tuple[str, int]:
        return (self.source_sha256, self.zero_based_row_ordinal)


def make_replay_binding(
    zero_based_row_ordinal: int,
    *,
    native_country: Any = None,
    native_idnumber: Any = None,
) -> ReplayBinding:
    return ReplayBinding(
        CANONICAL_SHA256,
        zero_based_row_ordinal,
        native_country=native_country,
        native_idnumber=native_idnumber,
    )


def reject_native_id_as_replay_authority(
    *,
    key_fields: Sequence[str],
) -> None:
    normalized = tuple(str(x) for x in key_fields)
    if normalized in (("COUNTRY", "IDnumber"), ("country", "ID"), ("COUNTRY", "ID")):
        raise Asian5RealizationError(
            "country+ID is noninjective in Asian W5 and cannot replace source SHA + row ordinal"
        )


@dataclass(frozen=True)
class RoutingProjection:
    route_id: str
    variables: tuple[str, ...]
    topology_authority: str
    exact_applicability_state: str
    semantic_detail_state: str


ROUTING_PROJECTIONS: Mapping[str, RoutingProjection] = {
    "INDIA_Q106CDE": RoutingProjection(
        "INDIA_Q106CDE",
        ("Q106c", "Q106d", "Q106e"),
        "SOURCE_PACKET_PRESERVES_INDIA_COUNTRY_SPECIFIC_MODULE_TOPOLOGY",
        BOUNDED_UNKNOWN,
        "BOUNDED_UNKNOWN__COUNTRY_TEAM_AUTHORITY_REQUIRED",
    ),
    "ASEAN_Q186": RoutingProjection(
        "ASEAN_Q186",
        ("q186",),
        "COREQ_MARKS_Q186_ASEAN_ONLY",
        "BOUNDED_UNKNOWN__EXACT_SOURCE_RISK_SET_NOT_DOCUMENTARILY_CLOSED",
        "BOUNDED_UNKNOWN__MERGED_MINUS1_MEANING_NOT_CLOSED",
    ),
}


def resolve_routing_projection(
    route_id: str,
    *,
    observed_missing_or_sentinel_state: Any = None,
    native_country_value: Any = None,
) -> RoutingProjection:
    # These observations are physical evidence only; they do not decide routing.
    del observed_missing_or_sentinel_state, native_country_value
    try:
        return ROUTING_PROJECTIONS[route_id]
    except KeyError as exc:
        raise Asian5RealizationError("unknown governed routing projection") from exc


@dataclass(frozen=True)
class WeightCarrier:
    variable_name: str = "w"
    role_or_estimand: str = BOUNDED_UNKNOWN
    normalization: str = BOUNDED_UNKNOWN
    default_use_authorized: bool = False


WEIGHT_CARRIER = WeightCarrier()


def select_default_weight() -> str:
    raise Asian5RealizationError(
        "no default Asian W5 weight is authorized by the accepted authority packet"
    )


GEOGRAPHY_BINDING: Mapping[str, Any] = {
    "carrier": "COUNTRY",
    "physical_coordinate_authority": "RAW_SOURCE_LOCAL_CARRIER",
    "merged_to_instrument_mapping": BOUNDED_UNKNOWN,
    "india_addition_semantics": BOUNDED_UNKNOWN,
    "cross_wave_recoding_authorized": False,
}


def admit_source_identity(*, source_sha256: str, reader_mode: str) -> None:
    if source_sha256 != CANONICAL_SHA256:
        raise Asian5RealizationError("source root mismatch")
    if reader_mode != READER_MODE:
        raise Asian5RealizationError("reader mode drift")


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
        "authority_class": AUTHORITY_CLASS,
        "source": {
            "canonical_filename": CANONICAL_FILENAME,
            "canonical_sha256": CANONICAL_SHA256,
            "format": SOURCE_FORMAT,
            "reader_mode": READER_MODE,
            "source_declared_encoding": SOURCE_DECLARED_ENCODING,
            "replay_identity": REPLAY_IDENTITY_RULE,
        },
        "mr_sets": [
            {
                "set_name": spec.set_name,
                "set_kind": spec.set_kind,
                "counted_value": spec.counted_value,
                "members": spec.members,
                "semantic_alias_state": spec.semantic_alias_state,
            }
            for spec in EXPECTED_MR_SETS
        ],
        "q112_se15_overlap": EXPECTED_Q112_SE15_OVERLAP,
        "routing": {
            route_id: {
                "variables": projection.variables,
                "topology_authority": projection.topology_authority,
                "exact_applicability_state": projection.exact_applicability_state,
                "semantic_detail_state": projection.semantic_detail_state,
            }
            for route_id, projection in sorted(ROUTING_PROJECTIONS.items())
        },
        "weight": {
            "variable_name": WEIGHT_CARRIER.variable_name,
            "role_or_estimand": WEIGHT_CARRIER.role_or_estimand,
            "normalization": WEIGHT_CARRIER.normalization,
            "default_use_authorized": WEIGHT_CARRIER.default_use_authorized,
        },
        "geography": GEOGRAPHY_BINDING,
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
            raise Asian5RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise Asian5RealizationError("candidate source root divergence")
        if self.source_specific_realization_identity != SOURCE_SPECIFIC_REALIZATION_IDENTITY:
            raise Asian5RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(
    bindings: Sequence[CandidateSemanticBinding],
) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise Asian5RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise Asian5RealizationError("A/B/C source root divergence")
    if len({binding.source_specific_realization_identity for binding in bindings}) != 1:
        raise Asian5RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "APPLICABLE_EDGE_CLASSES",
    "AUTHORITY_CLASS",
    "Asian5RealizationError",
    "BOUNDED_UNKNOWN",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "CONTRACT_ID",
    "CandidateSemanticBinding",
    "EXPECTED_MR_SETS",
    "EXPECTED_Q112_SE15_OVERLAP",
    "GEOGRAPHY_BINDING",
    "NativeMRSet",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "READER_MODE",
    "REPLAY_IDENTITY_RULE",
    "ROUTING_PROJECTIONS",
    "ReplayBinding",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "WEIGHT_CARRIER",
    "admit_source_identity",
    "canonical_digest",
    "make_replay_binding",
    "reject_native_id_as_replay_authority",
    "require_common_abc_semantic_law",
    "require_no_mr_semantic_alias",
    "require_questionnaire_q112_nonidentity",
    "resolve_routing_projection",
    "select_default_weight",
    "source_specific_realization_payload",
    "validate_native_mr_topology",
]
