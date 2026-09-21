"""Governed source-specific realization law for CLOSED_35 Asian Barometer Wave 4.

This module does not read or execute the SAV. It freezes the candidate-neutral
semantic owner surface that later A/B/C realizations must share after lawful
physical extraction.

The accepted Wave-4 packet requires preservation of ordinary stored -1 values,
merged-data versus instrument geography separation, ranked-slot topology,
documented ASEAN-only q172 scope, distinct w/w_cross carriers, and bounded
documentary unknowns. Physical evidence never manufactures survey semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence


CONTRACT_ID = "CLOSED35_R3_ASIAN4_SOURCE_REALIZATION@1.0.0"
CANONICAL_FILENAME = "Asian Barometer Wave 4.sav"
CANONICAL_SHA256 = "4d914817509d0e5f3adde49707df148f696992055937f085080a016002a39200"
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

APPLICABLE_EDGE_CLASSES = ("EC01", "EC05", "EC09", "EC10", "EC12", "EC13")
R35_REQUIRED_PHYSICAL_DIMENSIONS = (
    "physical_metadata",
    "variable_inventory_order",
    "raw_storage_values",
    "row_replay_identity",
    "physical_missingness",
    "ordered_repeated_slot_topology",
    "form_module_skip_routing_carriers",
    "weight_design_variables",
    "source_local_coordinate_carriers",
)


class Asian4RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise Asian4RealizationError(
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
class ReplayBinding:
    source_sha256: str
    zero_based_row_ordinal: int
    native_country: Any = None
    native_idnumber: Any = None

    def __post_init__(self) -> None:
        if self.source_sha256 != CANONICAL_SHA256:
            raise Asian4RealizationError("source root mismatch")
        if not isinstance(self.zero_based_row_ordinal, int) or self.zero_based_row_ordinal < 0:
            raise Asian4RealizationError("row ordinal must be a non-negative integer")

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


def reject_native_id_as_replay_authority(*, key_fields: Sequence[str]) -> None:
    normalized = tuple(str(x).lower() for x in key_fields)
    if normalized in (
        ("idnumber",),
        ("country", "idnumber"),
        ("country", "id"),
    ):
        raise Asian4RealizationError(
            "native ID fields are source attributes only; replay authority is source SHA + row ordinal"
        )


@dataclass(frozen=True)
class MinusOneProjection:
    variable_name: str
    raw_value: int
    physical_state: str
    semantic_state: str


def project_ordinary_minus_one(
    variable_name: str,
    *,
    raw_value: int | float = -1,
    physical_state: str = "OBSERVED_STORAGE_VALUE",
) -> MinusOneProjection:
    if not variable_name:
        raise Asian4RealizationError("variable name is required")
    if raw_value != -1:
        raise Asian4RealizationError("Wave-4 ordinary sentinel projection is defined for raw -1")
    if physical_state != "OBSERVED_STORAGE_VALUE":
        raise Asian4RealizationError(
            "ordinary stored -1 cannot be coerced into system/user physical missing"
        )
    return MinusOneProjection(
        variable_name=variable_name,
        raw_value=-1,
        physical_state="OBSERVED_STORAGE_VALUE",
        semantic_state=f"BOUNDED_UNKNOWN__VARIABLE_LOCAL_MINUS1_SEMANTICS__{variable_name}",
    )


def reject_global_minus_one_semantics(*, asserted_semantic_state: str) -> None:
    if asserted_semantic_state and asserted_semantic_state != BOUNDED_UNKNOWN:
        raise Asian4RealizationError(
            "Wave-4 -1 semantics are variable-local and may not be globally assigned"
        )


@dataclass(frozen=True)
class RankedSlotFamily:
    family_id: str
    slots: tuple[str, ...]
    role_authority: tuple[str, ...]
    semantic_state: str


EXPECTED_RANKED_FAMILIES: tuple[RankedSlotFamily, ...] = (
    RankedSlotFamily(
        family_id="Q20_Q21_Q22",
        slots=("q20", "q21", "q22"),
        role_authority=("ORDER_1", "ORDER_2", "ORDER_3"),
        semantic_state="PHYSICAL_ORDERED_TOPOLOGY__ITEM_ROLE_REFINEMENT_BOUNDED_UNKNOWN",
    ),
    RankedSlotFamily(
        family_id="Q99_Q99A_Q99B",
        slots=("q99", "q99a", "q99b"),
        role_authority=("FIRST_RESPONSE", "SECOND_RESPONSE_OPTIONAL", "THIRD_RESPONSE_OPTIONAL"),
        semantic_state="SOURCE_NATIVE_COREQ_ROLE_AUTHORITY_AT_RANKED_GRAIN",
    ),
)
_EXPECTED_RANKED_BY_ID = {family.family_id: family for family in EXPECTED_RANKED_FAMILIES}


def validate_ranked_slot_topology(
    actual: Sequence[RankedSlotFamily],
) -> tuple[RankedSlotFamily, ...]:
    by_id = {family.family_id: family for family in actual}
    if len(by_id) != len(actual):
        raise Asian4RealizationError("duplicate ranked family identity")
    if set(by_id) != set(_EXPECTED_RANKED_BY_ID):
        raise Asian4RealizationError("ranked family flattening or deletion")
    for family_id, expected in _EXPECTED_RANKED_BY_ID.items():
        if by_id[family_id] != expected:
            raise Asian4RealizationError(f"ranked-slot topology drift for {family_id}")
    return tuple(by_id[x.family_id] for x in EXPECTED_RANKED_FAMILIES)


@dataclass(frozen=True)
class RoutingProjection:
    route_id: str
    variables: tuple[str, ...]
    documented_scope: str
    exact_source_risk_set_state: str
    merged_minus1_semantics_state: str


Q172_ROUTING = RoutingProjection(
    route_id="ASEAN_Q172",
    variables=("q172",),
    documented_scope="ASEAN_COUNTRIES_ONLY",
    exact_source_risk_set_state="BOUNDED_UNKNOWN__EXACT_SOURCE_RISK_SET_NOT_CLOSED",
    merged_minus1_semantics_state="BOUNDED_UNKNOWN__VARIABLE_LOCAL_MINUS1_ROUTING_MEANING",
)


def require_q172_documentary_scope(scope: str) -> str:
    if scope != Q172_ROUTING.documented_scope:
        raise Asian4RealizationError(
            "q172 may not be applied beyond the documented ASEAN-countries-only instrument scope"
        )
    return scope


def resolve_q172_row_applicability(
    *,
    native_country_value: Any = None,
    observed_missing_or_sentinel_state: Any = None,
) -> str:
    # Country storage and -1 incidence are physical evidence only.
    del native_country_value, observed_missing_or_sentinel_state
    return Q172_ROUTING.exact_source_risk_set_state


GEOGRAPHY_BINDING: Mapping[str, Any] = {
    "merged_source_carrier": "country",
    "instrument_country_carrier": "SE1",
    "merged_physical_coordinate_authority": "RAW_SOURCE_LOCAL_CARRIER",
    "instrument_documentary_authority": "SOURCE_NATIVE_CORE_QUESTIONNAIRE",
    "merged_to_instrument_reconciliation": BOUNDED_UNKNOWN,
    "cross_wave_harmonization_authorized": False,
    "drift_witness": {
        "merged_codes_3_to_8": (
            "3=Korea",
            "4=China",
            "5=Mongolia",
            "6=Philippines",
            "7=Taiwan",
            "8=Thailand",
        ),
        "instrument_codes_3_to_8": (
            "3=Taiwan",
            "4=Korea",
            "5=Thailand",
            "6=Philippines",
            "7=Mainland China",
            "8=Mongolia",
        ),
    },
}


def reconcile_merged_and_instrument_geography() -> None:
    raise Asian4RealizationError(
        "merged-data and instrument country coding may not be harmonized without explicit release authority"
    )


@dataclass(frozen=True)
class WeightCarrier:
    variable_name: str
    role_or_estimand: str = BOUNDED_UNKNOWN
    normalization: str = BOUNDED_UNKNOWN
    default_use_authorized: bool = False


WEIGHT_CARRIERS: tuple[WeightCarrier, ...] = (
    WeightCarrier("w"),
    WeightCarrier("w_cross"),
)


def select_default_weight() -> str:
    raise Asian4RealizationError(
        "no default Asian W4 weight is authorized by the accepted authority packet"
    )


def require_distinct_weight_carriers(*, asserted_alias: bool) -> None:
    if asserted_alias:
        raise Asian4RealizationError(
            "w and w_cross are distinct source carriers and may not be semantically aliased"
        )


def reject_cross_wave_semantic_import(source_wave: str) -> None:
    if str(source_wave).strip().lower() not in {"4", "wave 4", "w4"}:
        raise Asian4RealizationError(
            "Wave-4 realization cannot import semantic authority from another Asian Barometer wave"
        )


def admit_source_identity(*, source_sha256: str, reader_mode: str) -> None:
    if source_sha256 != CANONICAL_SHA256:
        raise Asian4RealizationError("source root mismatch")
    if reader_mode != READER_MODE:
        raise Asian4RealizationError("reader mode drift")


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
        "minus_one": {
            "physical_state": "OBSERVED_STORAGE_VALUE",
            "semantic_rule": "VARIABLE_LOCAL_ONLY",
            "semantic_default": BOUNDED_UNKNOWN,
            "typed_missing_equivalence_authorized": False,
        },
        "ranked_families": [
            {
                "family_id": family.family_id,
                "slots": family.slots,
                "role_authority": family.role_authority,
                "semantic_state": family.semantic_state,
            }
            for family in EXPECTED_RANKED_FAMILIES
        ],
        "q172_routing": {
            "variables": Q172_ROUTING.variables,
            "documented_scope": Q172_ROUTING.documented_scope,
            "exact_source_risk_set_state": Q172_ROUTING.exact_source_risk_set_state,
            "merged_minus1_semantics_state": Q172_ROUTING.merged_minus1_semantics_state,
        },
        "geography": GEOGRAPHY_BINDING,
        "weights": [
            {
                "variable_name": carrier.variable_name,
                "role_or_estimand": carrier.role_or_estimand,
                "normalization": carrier.normalization,
                "default_use_authorized": carrier.default_use_authorized,
            }
            for carrier in WEIGHT_CARRIERS
        ],
        "semantic_owner_surface": SEMANTIC_OWNER_SURFACE,
        "r35_hooks": R35_HOOK_BINDING,
        "candidate_law": "A_B_C_SHARE_ONE_SOURCE_SPECIFIC_SEMANTIC_REALIZATION_IDENTITY",
        "cross_wave_semantic_import_authorized": False,
    }


SOURCE_SPECIFIC_REALIZATION_IDENTITY = canonical_digest(source_specific_realization_payload())


@dataclass(frozen=True)
class CandidateSemanticBinding:
    candidate_id: str
    source_sha256: str = CANONICAL_SHA256
    source_specific_realization_identity: str = SOURCE_SPECIFIC_REALIZATION_IDENTITY

    def __post_init__(self) -> None:
        if self.candidate_id not in {"A", "B", "C"}:
            raise Asian4RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise Asian4RealizationError("candidate source root divergence")
        if self.source_specific_realization_identity != SOURCE_SPECIFIC_REALIZATION_IDENTITY:
            raise Asian4RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(
    bindings: Sequence[CandidateSemanticBinding],
) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise Asian4RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise Asian4RealizationError("A/B/C source root divergence")
    if len({binding.source_specific_realization_identity for binding in bindings}) != 1:
        raise Asian4RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "APPLICABLE_EDGE_CLASSES",
    "AUTHORITY_CLASS",
    "Asian4RealizationError",
    "BOUNDED_UNKNOWN",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "CONTRACT_ID",
    "CandidateSemanticBinding",
    "EXPECTED_RANKED_FAMILIES",
    "GEOGRAPHY_BINDING",
    "MinusOneProjection",
    "Q172_ROUTING",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "READER_MODE",
    "REPLAY_IDENTITY_RULE",
    "RankedSlotFamily",
    "ReplayBinding",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "WEIGHT_CARRIERS",
    "admit_source_identity",
    "canonical_digest",
    "make_replay_binding",
    "project_ordinary_minus_one",
    "reconcile_merged_and_instrument_geography",
    "reject_cross_wave_semantic_import",
    "reject_global_minus_one_semantics",
    "reject_native_id_as_replay_authority",
    "require_common_abc_semantic_law",
    "require_distinct_weight_carriers",
    "require_q172_documentary_scope",
    "resolve_q172_row_applicability",
    "select_default_weight",
    "source_specific_realization_payload",
    "validate_ranked_slot_topology",
]
