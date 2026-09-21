"""Governed source-specific realization law for CLOSED_35 Asian Barometer Wave 1.

This module does not read or execute the SAV. It freezes the candidate-neutral
semantic owner surface that later A/B/C realizations must share after lawful
physical extraction.

The accepted packet authorizes exact physical facts for the frozen source:
source-declared BIG-5 reader metadata, typed SPSS missingness, source-local
identity/geography carriers, nine distinct weight carriers, and ranked q097
slots. It does not recover exact Wave-1 questionnaire/routing/weight semantics.
Those gaps remain governed bounded unknowns rather than guessed meanings.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence


CONTRACT_ID = "CLOSED35_R3_ASIAN1_SOURCE_REALIZATION@1.0.0"
CANONICAL_FILENAME = "Asian Barometer Wave 1.sav"
CANONICAL_SHA256 = "ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2"
SOURCE_FORMAT = "SAV"
AUTHORITY_CLASS = "L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED"
READER_MODE = "SAV_SOURCE_DECLARED_BIG5"
SOURCE_DECLARED_ENCODING = "BIG-5"
COMPATIBILITY_MODE = "NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE"
REPLAY_IDENTITY_RULE = "SOURCE_SHA256+ROW_ORDINAL"
BOUNDED_UNKNOWN = "BOUNDED_UNKNOWN"
SEMANTIC_OWNER_SURFACE = "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0"

ACCEPTED_SOURCE_ROWS = 12217
ACCEPTED_SOURCE_VARIABLES = 217
ACCEPTED_USER_MISSING_CELLS = 284794
ACCEPTED_SYSTEM_MISSING_CELLS = 720729
ACCEPTED_VARIABLES_WITH_MISSING_DECLARATIONS = 199

R35_PHYSICAL_METADATA_SCHEMA = "PRE553_PHYSICAL_METADATA@1.0.0"
R35_DERIVATIVE_PARENTAGE_BUNDLE_SCHEMA = "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0"
R35_PHYSICAL_SCOPE_SCHEMA = "FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0"
R35_PHYSICAL_EXPECTATION_SCHEMA = "FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0"
R35_PHYSICAL_REALIZATION_SCHEMA = "FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0"
R35_PHYSICAL_EQUIVALENCE_RECEIPT_SCHEMA = (
    "FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0"
)

APPLICABLE_EDGE_CLASSES = (
    "EC01",
    "EC02",
    "EC05",
    "EC07",
    "EC09",
    "EC12",
    "EC13",
    "EC14",
)

R35_REQUIRED_PHYSICAL_DIMENSIONS = (
    "physical_metadata",
    "reader_configuration",
    "decoded_text_evidence",
    "variable_inventory_order",
    "raw_storage_values",
    "physical_missing_states",
    "row_replay_identity",
    "native_id_replay_evidence",
    "ordered_repeated_slot_topology",
    "weight_design_variables",
    "source_local_coordinate_carriers",
)


class Asian1RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise Asian1RealizationError(
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


def admit_source_identity(
    *,
    source_sha256: str,
    reader_mode: str,
    compatibility_mode: str = COMPATIBILITY_MODE,
) -> None:
    if source_sha256 != CANONICAL_SHA256:
        raise Asian1RealizationError("source root mismatch")
    if reader_mode != READER_MODE:
        raise Asian1RealizationError("BIG-5 reader mode drift")
    if compatibility_mode != COMPATIBILITY_MODE:
        raise Asian1RealizationError("unauthorized compatibility reader override")


def preserve_decoded_text(
    decoded_text: str,
    *,
    normalization_requested: bool = False,
    asserted_documentary_semantic_authority: bool = False,
) -> str:
    if not isinstance(decoded_text, str):
        raise Asian1RealizationError("decoded text must be a string")
    if normalization_requested:
        raise Asian1RealizationError(
            "decoded Wave-1 text may not be normalized or harmonized without authority"
        )
    if asserted_documentary_semantic_authority:
        raise Asian1RealizationError(
            "readable BIG-5 decoding is physical reader evidence, not documentary semantic authority"
        )
    return decoded_text


@dataclass(frozen=True)
class ReplayBinding:
    source_sha256: str
    zero_based_row_ordinal: int
    native_country: Any = None
    native_idnumber: Any = None

    def __post_init__(self) -> None:
        if self.source_sha256 != CANONICAL_SHA256:
            raise Asian1RealizationError("source root mismatch")
        if not isinstance(self.zero_based_row_ordinal, int) or self.zero_based_row_ordinal < 0:
            raise Asian1RealizationError("row ordinal must be a non-negative integer")

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
    if normalized in {
        ("idnumber",),
        ("country", "idnumber"),
        ("country", "id"),
    }:
        raise Asian1RealizationError(
            "Wave-1 native identity carriers are source-local attributes and cannot replace source SHA + row ordinal"
        )


@dataclass(frozen=True)
class MissingWitness:
    variable_name: str
    packet_variable_ordinal: int
    physical_state: str
    stored_value: Any
    declaration: str | None
    semantic_state: str = BOUNDED_UNKNOWN

    def __post_init__(self) -> None:
        allowed = {
            "FORMAT_USER_MISSING_VALUE",
            "SYSTEM_MISSING",
            "OBSERVED_STORAGE_VALUE",
        }
        if self.physical_state not in allowed:
            raise Asian1RealizationError("unsupported physical missing-state witness")
        if self.physical_state == "FORMAT_USER_MISSING_VALUE":
            if self.stored_value is None or not self.declaration:
                raise Asian1RealizationError(
                    "user-missing witness must preserve stored value and declaration"
                )
        if self.physical_state == "SYSTEM_MISSING" and self.stored_value is not None:
            raise Asian1RealizationError(
                "system-missing witness must not invent a stored response value"
            )


Q001_USER_MISSING_98 = MissingWitness(
    variable_name="q001",
    packet_variable_ordinal=32,
    physical_state="FORMAT_USER_MISSING_VALUE",
    stored_value=98.0,
    declaration="USER_MISSING_VALUES_98_99",
)

Q018_1_SYSTEM_MISSING = MissingWitness(
    variable_name="q018_1",
    packet_variable_ordinal=50,
    physical_state="SYSTEM_MISSING",
    stored_value=None,
    declaration=None,
)


def require_typed_missing_noncollapse(
    left: MissingWitness,
    right: MissingWitness,
    *,
    asserted_same_physical_state: bool,
) -> None:
    if left.physical_state != right.physical_state and asserted_same_physical_state:
        raise Asian1RealizationError(
            "typed physical missing states cannot be collapsed"
        )


@dataclass(frozen=True)
class WeightCarrier:
    variable_name: str
    packet_variable_ordinal: int
    role_or_estimand: str = BOUNDED_UNKNOWN
    normalization: str = BOUNDED_UNKNOWN
    default_use_authorized: bool = False


_WEIGHT_NAMES = (
    "w_jp",
    "w_hk",
    "w_kr",
    "w_cn",
    "w_mo",
    "w_ph",
    "w_tw",
    "w_th",
    "w_all",
)
EXPECTED_WEIGHT_CARRIERS = tuple(
    WeightCarrier(name, 208 + index) for index, name in enumerate(_WEIGHT_NAMES)
)


def validate_weight_carriers(
    actual: Sequence[WeightCarrier],
) -> tuple[WeightCarrier, ...]:
    actual_tuple = tuple(actual)
    if actual_tuple != EXPECTED_WEIGHT_CARRIERS:
        raise Asian1RealizationError(
            "nine-weight topology drift, collapse, alias, or invented role"
        )
    return actual_tuple


def select_default_weight() -> str:
    raise Asian1RealizationError(
        "no default Asian W1 weight is authorized by the accepted authority packet"
    )


@dataclass(frozen=True)
class RankedSlot:
    variable_name: str
    packet_variable_ordinal: int
    rank: int


EXPECTED_Q097_RANKED_SLOTS = (
    RankedSlot("q097_1", 135, 1),
    RankedSlot("q097_2", 136, 2),
    RankedSlot("q097_3", 137, 3),
)


def validate_q097_ranked_topology(
    actual: Sequence[RankedSlot],
) -> tuple[RankedSlot, ...]:
    actual_tuple = tuple(actual)
    if actual_tuple != EXPECTED_Q097_RANKED_SLOTS:
        raise Asian1RealizationError(
            "q097 ranked-slot topology may not be flattened, reordered, or aliased"
        )
    return actual_tuple


@dataclass(frozen=True)
class RoutingProjection:
    variable_name: str
    exact_applicability_state: str
    semantic_detail_state: str


def resolve_routing_projection(
    variable_name: str,
    *,
    observed_physical_state: Any = None,
    decoded_label_text: Any = None,
) -> RoutingProjection:
    # Physical missingness and decoded labels are not routing authority.
    del observed_physical_state, decoded_label_text
    return RoutingProjection(
        variable_name=str(variable_name),
        exact_applicability_state="BOUNDED_UNKNOWN__W1_ROUTING_AUTHORITY_NOT_RECOVERED",
        semantic_detail_state="BOUNDED_UNKNOWN__W1_QUESTIONNAIRE_CODEBOOK_NOT_RECOVERED",
    )


GEOGRAPHY_BINDING: Mapping[str, Any] = {
    "country_carrier": "country",
    "level3_carrier": "level3",
    "country_dictionary_physical_evidence": {
        1: "Japan",
        2: "Hong Kong",
        3: "Korea",
        4: "Mainland China",
        5: "Mongolia",
        6: "Philippines",
        7: "Taiwan",
        8: "Thailand",
    },
    "level3_observed_counts": {1: 7870, 2: 4342, 3: 5},
    "cross_wave_recoding_authorized": False,
    "instrument_reconciliation_state": BOUNDED_UNKNOWN,
}


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
            "compatibility_mode": COMPATIBILITY_MODE,
            "replay_identity": REPLAY_IDENTITY_RULE,
            "accepted_rows": ACCEPTED_SOURCE_ROWS,
            "accepted_variables": ACCEPTED_SOURCE_VARIABLES,
        },
        "missing_regime": {
            "user_missing_cells": ACCEPTED_USER_MISSING_CELLS,
            "system_missing_cells": ACCEPTED_SYSTEM_MISSING_CELLS,
            "variables_with_missing_declarations": ACCEPTED_VARIABLES_WITH_MISSING_DECLARATIONS,
            "semantic_mapping_state": BOUNDED_UNKNOWN,
        },
        "weights": [
            {
                "variable_name": carrier.variable_name,
                "packet_variable_ordinal": carrier.packet_variable_ordinal,
                "role_or_estimand": carrier.role_or_estimand,
                "normalization": carrier.normalization,
                "default_use_authorized": carrier.default_use_authorized,
            }
            for carrier in EXPECTED_WEIGHT_CARRIERS
        ],
        "ranked_q097": [
            {
                "variable_name": slot.variable_name,
                "packet_variable_ordinal": slot.packet_variable_ordinal,
                "rank": slot.rank,
            }
            for slot in EXPECTED_Q097_RANKED_SLOTS
        ],
        "geography": GEOGRAPHY_BINDING,
        "routing_authority_state": "BOUNDED_UNKNOWN__W1_ROUTING_AUTHORITY_NOT_RECOVERED",
        "decoded_text_semantic_authority": False,
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
            raise Asian1RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise Asian1RealizationError("candidate source root divergence")
        if self.source_specific_realization_identity != SOURCE_SPECIFIC_REALIZATION_IDENTITY:
            raise Asian1RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(
    bindings: Sequence[CandidateSemanticBinding],
) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise Asian1RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise Asian1RealizationError("A/B/C source root divergence")
    if len({binding.source_specific_realization_identity for binding in bindings}) != 1:
        raise Asian1RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "ACCEPTED_SOURCE_ROWS",
    "ACCEPTED_SOURCE_VARIABLES",
    "ACCEPTED_SYSTEM_MISSING_CELLS",
    "ACCEPTED_USER_MISSING_CELLS",
    "APPLICABLE_EDGE_CLASSES",
    "AUTHORITY_CLASS",
    "Asian1RealizationError",
    "BOUNDED_UNKNOWN",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "CandidateSemanticBinding",
    "COMPATIBILITY_MODE",
    "CONTRACT_ID",
    "EXPECTED_Q097_RANKED_SLOTS",
    "EXPECTED_WEIGHT_CARRIERS",
    "GEOGRAPHY_BINDING",
    "MissingWitness",
    "Q001_USER_MISSING_98",
    "Q018_1_SYSTEM_MISSING",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "READER_MODE",
    "REPLAY_IDENTITY_RULE",
    "RankedSlot",
    "ReplayBinding",
    "RoutingProjection",
    "SOURCE_DECLARED_ENCODING",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "WeightCarrier",
    "admit_source_identity",
    "canonical_digest",
    "make_replay_binding",
    "preserve_decoded_text",
    "reject_native_id_as_replay_authority",
    "require_common_abc_semantic_law",
    "require_typed_missing_noncollapse",
    "resolve_routing_projection",
    "select_default_weight",
    "source_specific_realization_payload",
    "validate_q097_ranked_topology",
    "validate_weight_carriers",
]
