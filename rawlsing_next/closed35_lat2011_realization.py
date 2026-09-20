"""Candidate-neutral governed realization for CLOSED_35 Latinobarometro 2011.

This module does not read the SAV and does not execute source processing.
It freezes the minimal source-specific authority surface that later A/B/C
candidates must share after generic S35/R35 physical extraction.

Latinobarometro 2011 is intentionally the clean L0 baseline.  The realization
therefore adds only source-local identity, coordinate, missing-state and weight
authority required by the accepted Authority71/72 packet.  It does not import
1995 or 2024 exceptions and it does not manufacture an aggregate weight
estimand from the existence of WT.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState


CONTRACT_ID = "CLOSED35_R2_LAT2011_SOURCE_REALIZATION@1.0.0"
CANONICAL_FILENAME = "Latinobarometro 2011.sav"
CANONICAL_SHA256 = "a44e89e08e564e4e175199eeeabfa6163f32f4ba0a19a6c3f5b4752de6cca22e"
SOURCE_FORMAT = "SAV"
SOURCE_FAMILY = "Latinobarometro"
SOURCE_WAVE = "2011"
PRODUCER_RELEASE_ID = "v2011.1"
AUTHORITY72_CLASS = "L0_EXECUTION_PACKET_READY__NO_NAMED_DOCUMENTARY_BLOCKER"

REPLAY_IDENTITY_LAW = "SOURCE_SHA256+ROW_ORDINAL"
VARIABLE_IDENTITY_LAW = "SOURCE_LOCAL_EXACT_VARIABLE_IDENTITY"
NO_AGGREGATE_ESTIMAND = "NO_AGGREGATE_ESTIMAND_AUTHORIZED"
NO_DEFAULT_WEIGHT = "NO_DEFAULT_WEIGHT_SELECTION_AUTHORIZED"
CROSS_WAVE_INHERITANCE = "NONE_AUTHORIZED"

# Accepted Authority71 packet expectations.  These are inherited documentary /
# previously measured source facts; this browser worker does not remeasure them.
ACCEPTED_PACKET_ROW_COUNT = 20_204
ACCEPTED_PACKET_VARIABLE_COUNT = 414
COUNTRY_COORDINATE_VARIABLE = "IDENPA"
NATIVE_INTERVIEW_NUMBER_VARIABLE = "NUMENTRE"
WEIGHT_VARIABLE = "WT"
WEIGHT_PACKET_ZERO_BASED_ORDINAL = 413
WEIGHT_GENERIC_DECODER_ORDINAL = 414

COUNTRY_SAMPLE_COUNTS: Mapping[str, int] = {
    "32": 1200,
    "68": 1200,
    "76": 1204,
    "152": 1200,
    "170": 1200,
    "188": 1000,
    "214": 1000,
    "218": 1200,
    "222": 1000,
    "320": 1000,
    "340": 1000,
    "484": 1200,
    "558": 1000,
    "591": 1000,
    "600": 1200,
    "604": 1200,
    "858": 1200,
    "862": 1200,
}

DOCUMENTARY_AUTHORITY: Mapping[str, Mapping[str, Any]] = {
    "LAT2011_QUESTIONNAIRE_ENG": {
        "scope": "administered wording, batteries, routing/instrument-layer response codes",
        "authority_strength": "SOURCE_NATIVE_EXPLICIT",
    },
    "LAT2011_CODEBOOK_V20190707": {
        "scope": "released-data variable identities, IDENPA/NUMENTRE labels, P-variable storage semantics, WT label",
        "authority_strength": "SOURCE_NATIVE_EXPLICIT",
    },
    "LAT2011_METHODOLOGY": {
        "scope": "country sample counts, coverage, selection stages/strata, country-specific weighting descriptions",
        "authority_strength": "SOURCE_NATIVE_EXPLICIT",
    },
}

# I01/I02/I03 schemas are frozen integration hooks, not claims that this worker
# executed their whole-source physical-equivalence court.
R35_PHYSICAL_METADATA_SCHEMA = "PRE553_PHYSICAL_METADATA@1.0.0"
R35_DERIVATIVE_PARENTAGE_BUNDLE_SCHEMA = "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0"
R35_PHYSICAL_SCOPE_SCHEMA = "FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0"
R35_PHYSICAL_EXPECTATION_SCHEMA = "FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0"
R35_PHYSICAL_REALIZATION_SCHEMA = "FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0"
R35_PHYSICAL_EQUIVALENCE_RECEIPT_SCHEMA = "FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0"

APPLICABLE_EDGE_CLASSES = ("EC01", "EC05", "EC12", "EC13")
R35_REQUIRED_PHYSICAL_DIMENSIONS = (
    "physical_metadata",
    "variable_inventory_order",
    "raw_storage_values",
    "physical_missing_declarations",
    "physical_missing_states",
    "row_replay_identity",
    "reader_configuration_digest",
    "source_coordinate_carriers",
    "weight_design_carriers",
)

EXACT_READER_CONFIGURATION: Mapping[str, Any] = {
    "decoder_implementation": "rawlsing_next/pre553_physical_decoder.py",
    "decoder_version": "pyreadstat/1.3.6",
    "decoder_mode": "SAV_NATIVE_GOVERNED",
    "config": {
        "reader": "pyreadstat.read_sav",
        "encoding": None,
        "user_missing": True,
        "apply_value_formats": False,
        "automatic_encoding_guessing": False,
    },
    "compatibility_mode": "NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE",
    "compatibility_semantic_scope": "NO_COMPATIBILITY_OVERRIDE__NO_SEMANTIC_CLAIM",
    "semantic_authority": False,
}

# These special laws belong to other exact snapshots.  Naming them here is a
# negative admission so they cannot leak into the 2011 baseline by family
# analogy.
FORBIDDEN_CROSS_WAVE_SPECIAL_LAWS = frozenset(
    {
        "LAT1995_BRAZIL_120_ROW_RELEASE_DISCREPANCY",
        "LAT1995_NONINJECTIVE_INTERVIEW_ID_SPECIAL_CASE",
        "LAT2024_NOMINAL_CASE_SIZE_174_VS_332",
        "LAT2024_WT_PUBLISHED_DOMAIN_CONFLICT",
        "LAT2024_P2ST_REPURPOSING",
        "LAT2024_P13ST_REPURPOSING",
        "LAT2024_P19ST_REPURPOSING",
    }
)


class LAT2011RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_canonical(v) for v in value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise LAT2011RealizationError(
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


def _require_nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LAT2011RealizationError(f"{name} must be a non-empty string")
    return value


def _normalize_reader_configuration(reader_configuration: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "decoder_implementation": reader_configuration.get(
            "decoder_implementation", "rawlsing_next/pre553_physical_decoder.py"
        ),
        "decoder_version": (
            f"pyreadstat/{reader_configuration.get('reader_version')}"
            if reader_configuration.get("reader_version")
            else reader_configuration.get("decoder_version")
        ),
        "decoder_mode": reader_configuration.get("decoder_mode", "SAV_NATIVE_GOVERNED"),
        "config": {
            "reader": (
                "pyreadstat.read_sav"
                if reader_configuration.get("reader") == "pyreadstat"
                else reader_configuration.get("reader")
            ),
            "encoding": reader_configuration.get("encoding"),
            "user_missing": reader_configuration.get("user_missing"),
            "apply_value_formats": reader_configuration.get("apply_value_formats"),
            "automatic_encoding_guessing": reader_configuration.get(
                "automatic_encoding_guessing", False
            ),
        },
        "compatibility_mode": reader_configuration.get(
            "compatibility_mode", "NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE"
        ),
        "compatibility_semantic_scope": reader_configuration.get(
            "compatibility_semantic_scope",
            "NO_COMPATIBILITY_OVERRIDE__NO_SEMANTIC_CLAIM",
        ),
        "semantic_authority": reader_configuration.get("semantic_authority", False),
    }


@dataclass(frozen=True)
class PhysicalAdmission:
    source_sha256: str
    reader_configuration_digest: str
    whole_source_physical_equivalence_qualified: bool = False


def admit_physical_incidence(incidence: Any) -> PhysicalAdmission:
    """Admit only the exact source/config boundary; do not certify the source."""

    if getattr(incidence, "source_sha256", None) != CANONICAL_SHA256:
        raise LAT2011RealizationError("canonical Latinobarometro 2011 source root mismatch")

    source_format = getattr(incidence, "source_format", SOURCE_FORMAT)
    if str(source_format).upper() != SOURCE_FORMAT:
        raise LAT2011RealizationError("Latinobarometro 2011 source format drift")

    reader_configuration = getattr(incidence, "reader_configuration", None)
    if not isinstance(reader_configuration, Mapping):
        raise LAT2011RealizationError("reader configuration missing")

    normalized = _normalize_reader_configuration(reader_configuration)
    if _canonical(normalized) != _canonical(EXACT_READER_CONFIGURATION):
        raise LAT2011RealizationError("Latinobarometro 2011 reader/config drift")

    return PhysicalAdmission(
        source_sha256=CANONICAL_SHA256,
        reader_configuration_digest=canonical_digest(EXACT_READER_CONFIGURATION),
        whole_source_physical_equivalence_qualified=False,
    )


@dataclass(frozen=True)
class ReplayIdentity:
    source_sha256: str
    row_ordinal: int

    def __post_init__(self) -> None:
        if self.source_sha256 != CANONICAL_SHA256:
            raise LAT2011RealizationError("replay identity source root drift")
        if not isinstance(self.row_ordinal, int) or isinstance(self.row_ordinal, bool):
            raise LAT2011RealizationError("row ordinal must be an integer")
        if self.row_ordinal < 0:
            raise LAT2011RealizationError("row ordinal must be nonnegative")


def replay_identity(row_ordinal: int) -> ReplayIdentity:
    """Preserve the physical row ordinal exactly; do not reindex through native IDs."""

    return ReplayIdentity(CANONICAL_SHA256, row_ordinal)


@dataclass(frozen=True)
class SourceLocalVariableIdentity:
    source_sha256: str
    variable_name: str
    variable_ordinal: int

    def __post_init__(self) -> None:
        if self.source_sha256 != CANONICAL_SHA256:
            raise LAT2011RealizationError("variable identity source root drift")
        _require_nonempty(self.variable_name, "variable_name")
        if not isinstance(self.variable_ordinal, int) or isinstance(
            self.variable_ordinal, bool
        ):
            raise LAT2011RealizationError("variable ordinal must be an integer")
        if self.variable_ordinal < 1:
            raise LAT2011RealizationError("generic decoder variable ordinal must be positive")


def source_local_variable_identity(
    variable_name: str, variable_ordinal: int
) -> SourceLocalVariableIdentity:
    return SourceLocalVariableIdentity(
        CANONICAL_SHA256, variable_name, variable_ordinal
    )


@dataclass(frozen=True)
class PhysicalStateWitness:
    source_sha256: str
    row_ordinal: int
    variable_ordinal: int
    variable_name: str
    raw_value: Any
    missing_state: str
    source_missing_declaration: Mapping[str, Any] | None


def preserve_physical_cell(cell: PhysicalCell, *, source_sha256: str = CANONICAL_SHA256) -> PhysicalStateWitness:
    """Carry raw storage + typed missing state without semantic promotion."""

    if source_sha256 != CANONICAL_SHA256:
        raise LAT2011RealizationError("physical cell source root drift")
    if not isinstance(cell, PhysicalCell):
        raise LAT2011RealizationError("physical witness must be a PhysicalCell")
    state = (
        cell.missing_state.value
        if isinstance(cell.missing_state, PhysicalMissingState)
        else str(cell.missing_state)
    )
    allowed_states = {item.value for item in PhysicalMissingState}
    if state not in allowed_states:
        raise LAT2011RealizationError("unknown physical missing state")

    declaration = (
        None
        if cell.source_missing_declaration is None
        else _canonical(cell.source_missing_declaration)
    )
    return PhysicalStateWitness(
        source_sha256=CANONICAL_SHA256,
        row_ordinal=cell.row_ordinal,
        variable_ordinal=cell.variable_ordinal,
        variable_name=cell.variable_name,
        raw_value=_canonical(cell.raw_value),
        missing_state=state,
        source_missing_declaration=declaration,
    )


@dataclass(frozen=True)
class CountryCoordinateAuthority:
    variable_name: str = COUNTRY_COORDINATE_VARIABLE
    documentary_role: str = "Country of interview"
    source_scope: str = "LATINOBAROMETRO_2011_ONLY"
    cross_wave_equivalence_authorized: bool = False


COUNTRY_COORDINATE_AUTHORITY = CountryCoordinateAuthority()


def validate_country_structure(country_counts: Mapping[str, int]) -> Mapping[str, int]:
    """Validate a supplied/synthetic count map against the accepted 2011 packet."""

    normalized = {str(code): int(count) for code, count in country_counts.items()}
    if normalized != dict(COUNTRY_SAMPLE_COUNTS):
        raise LAT2011RealizationError("2011 country-coordinate/sample structure drift")
    if sum(normalized.values()) != ACCEPTED_PACKET_ROW_COUNT:
        raise LAT2011RealizationError("2011 country-coordinate row total drift")
    return dict(COUNTRY_SAMPLE_COUNTS)


@dataclass(frozen=True)
class NativeIdentityAttributeLaw:
    variables: tuple[str, ...] = (
        COUNTRY_COORDINATE_VARIABLE,
        NATIVE_INTERVIEW_NUMBER_VARIABLE,
    )
    role: str = "SOURCE_LOCAL_ATTRIBUTES_ONLY"
    replay_identity_authorized: bool = False
    durable_cross_release_identity_authorized: bool = False


NATIVE_IDENTITY_ATTRIBUTE_LAW = NativeIdentityAttributeLaw()


@dataclass(frozen=True)
class WeightCarrierWitness:
    variable_name: str
    variable_ordinal: int
    raw_value: Any
    missing_state: str
    source_missing_declaration: Mapping[str, Any] | None
    documentary_role: str = "Weighting"
    aggregate_estimand_authority: str = NO_AGGREGATE_ESTIMAND
    default_selection_authority: str = NO_DEFAULT_WEIGHT


def bind_weight_carrier(
    cell: PhysicalCell,
    *,
    requested_aggregate_estimand: str | None = None,
    select_as_default: bool = False,
) -> WeightCarrierWitness:
    """Bind WT as a preserved source carrier, never as an inferred estimand."""

    if cell.variable_name != WEIGHT_VARIABLE:
        raise LAT2011RealizationError("weight binding requires exact WT source variable")
    if requested_aggregate_estimand is not None:
        raise LAT2011RealizationError("aggregate WT estimand is not authorized")
    if select_as_default:
        raise LAT2011RealizationError("default WT use is not authorized by carrier presence")

    physical = preserve_physical_cell(cell)
    return WeightCarrierWitness(
        variable_name=physical.variable_name,
        variable_ordinal=physical.variable_ordinal,
        raw_value=physical.raw_value,
        missing_state=physical.missing_state,
        source_missing_declaration=physical.source_missing_declaration,
    )


def reject_cross_wave_special_law(law_id: str) -> None:
    _require_nonempty(law_id, "law_id")
    if law_id in FORBIDDEN_CROSS_WAVE_SPECIAL_LAWS:
        raise LAT2011RealizationError("foreign Latinobarometro wave law is not authorized for 2011")


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
        "authority72_class": AUTHORITY72_CLASS,
        "source": {
            "family": SOURCE_FAMILY,
            "wave": SOURCE_WAVE,
            "canonical_filename": CANONICAL_FILENAME,
            "canonical_sha256": CANONICAL_SHA256,
            "format": SOURCE_FORMAT,
            "producer_release_id": PRODUCER_RELEASE_ID,
            "replay_identity": REPLAY_IDENTITY_LAW,
            "variable_identity": VARIABLE_IDENTITY_LAW,
        },
        "reader_configuration": EXACT_READER_CONFIGURATION,
        "accepted_packet_structure": {
            "row_count": ACCEPTED_PACKET_ROW_COUNT,
            "variable_count": ACCEPTED_PACKET_VARIABLE_COUNT,
            "country_coordinate_variable": COUNTRY_COORDINATE_VARIABLE,
            "country_sample_counts": COUNTRY_SAMPLE_COUNTS,
            "native_interview_number_variable": NATIVE_INTERVIEW_NUMBER_VARIABLE,
            "native_identity_is_replay_authority": False,
        },
        "missingness": {
            "physical_state_and_declaration_preserved": True,
            "system_missing_distinct_from_user_missing": True,
            "missingness_is_semantic_authority": False,
        },
        "weight": {
            "variable": WEIGHT_VARIABLE,
            "documentary_role": "Weighting",
            "carrier_preserved": True,
            "aggregate_estimand": NO_AGGREGATE_ESTIMAND,
            "default_selection": NO_DEFAULT_WEIGHT,
            "country_specific_methodology_does_not_authorize_universal_pooling": True,
        },
        "documentary_authority": DOCUMENTARY_AUTHORITY,
        "cross_wave_inheritance": CROSS_WAVE_INHERITANCE,
        "forbidden_cross_wave_imports": sorted(FORBIDDEN_CROSS_WAVE_SPECIAL_LAWS),
        "semantic_owner_surface": "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0",
        "r35_hooks": R35_HOOK_BINDING,
        "candidate_law": "A_B_C_SHARE_ONE_LAT2011_SOURCE_SPECIFIC_REALIZATION_IDENTITY",
        "claim_boundary": "SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__NOT_PHYSICAL_EQUIVALENCE_QUALIFIED",
    }


SOURCE_SPECIFIC_REALIZATION_IDENTITY = canonical_digest(
    source_specific_realization_payload()
)


@dataclass(frozen=True)
class CandidateSemanticBinding:
    candidate_id: str
    source_sha256: str = CANONICAL_SHA256
    source_specific_realization_identity: str = SOURCE_SPECIFIC_REALIZATION_IDENTITY

    def __post_init__(self) -> None:
        if self.candidate_id not in {"A", "B", "C"}:
            raise LAT2011RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise LAT2011RealizationError("candidate source root divergence")
        if (
            self.source_specific_realization_identity
            != SOURCE_SPECIFIC_REALIZATION_IDENTITY
        ):
            raise LAT2011RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(
    bindings: Sequence[CandidateSemanticBinding],
) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise LAT2011RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise LAT2011RealizationError("A/B/C source root divergence")
    if (
        len(
            {
                binding.source_specific_realization_identity
                for binding in bindings
            }
        )
        != 1
    ):
        raise LAT2011RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "ACCEPTED_PACKET_ROW_COUNT",
    "ACCEPTED_PACKET_VARIABLE_COUNT",
    "APPLICABLE_EDGE_CLASSES",
    "AUTHORITY72_CLASS",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "COUNTRY_COORDINATE_AUTHORITY",
    "COUNTRY_SAMPLE_COUNTS",
    "CandidateSemanticBinding",
    "CROSS_WAVE_INHERITANCE",
    "DOCUMENTARY_AUTHORITY",
    "EXACT_READER_CONFIGURATION",
    "FORBIDDEN_CROSS_WAVE_SPECIAL_LAWS",
    "LAT2011RealizationError",
    "NATIVE_IDENTITY_ATTRIBUTE_LAW",
    "NO_AGGREGATE_ESTIMAND",
    "NO_DEFAULT_WEIGHT",
    "PhysicalAdmission",
    "PhysicalStateWitness",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "REPLAY_IDENTITY_LAW",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "SourceLocalVariableIdentity",
    "WeightCarrierWitness",
    "admit_physical_incidence",
    "bind_weight_carrier",
    "canonical_digest",
    "preserve_physical_cell",
    "reject_cross_wave_special_law",
    "replay_identity",
    "require_common_abc_semantic_law",
    "source_local_variable_identity",
    "source_specific_realization_payload",
    "validate_country_structure",
]
