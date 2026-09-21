"""Governed source-specific realization law for CLOSED_35 Arab Barometer Wave 5.

This module never opens or processes the canonical SAV. It freezes the one
candidate-neutral semantic realization that later A/B/C physical candidates
must share.

Authority is deliberately separated into jurisdictions:
- physical source state and replay identity;
- source dictionary membership and observed-incidence facts;
- source-native documentary semantics;
- routing applicability;
- analytical weight/design authority.

Bounded documentary uncertainty is a lawful semantic state. Physical carrier
names, dictionary membership, missingness, Unicode readability, or cross-wave
similarity never manufacture semantic authority.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence


CONTRACT_ID = "CLOSED35_R3_ARAB5_SOURCE_REALIZATION@1.0.0"
SEMANTIC_OWNER = "ARAB5_SEMANTIC_OWNER_V1"
CANONICAL_FILENAME = "Arab Barometer Wave 5.sav"
CANONICAL_SHA256 = "6a5cbad637ce1546833a1d4812ba6d1e8d75f85b5b199b0cf3ec5cf456068dbc"
SOURCE_FORMAT = "SAV"
SOURCE_PHYSICAL_MODE = "SAV_NATIVE_GOVERNED"
SOURCE_DECLARED_ENCODING = "UTF-8"
SOURCE_DECLARED_CHARACTER_CODE = 65001
REPLAY_IDENTITY = "SOURCE_SHA256+ROW_ORDINAL"
LAUNCH_CLASS = "L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED"
BOUNDED_UNKNOWN = "BOUNDED_UNKNOWN"

SYSTEM_MISSING = "SYSTEM_MISSING"
ORDINARY_STORED_VALUE = "ORDINARY_STORED_VALUE"

ACCEPTED_ROW_COUNT = 27850
ACCEPTED_LOGICAL_VARIABLE_COUNT = 359
ACCEPTED_STORAGE_SLOT_COUNT = 361
ACCEPTED_NATIVE_SPSS_MR_SET_COUNT = 0

APPLICABLE_EDGE_CLASSES = (
    "EC01",
    "EC05",
    "EC07",
    "EC09",
    "EC10",
    "EC11",
    "EC12",
)

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
    "physical_missing_states",
    "missing_declarations",
    "row_replay_identity",
    "ordered_repeated_slot_topology",
    "form_module_skip_routing_carriers",
    "variable_dictionary_identity",
    "weight_design_variables",
)

Q101_DICTIONARY_KEYS = (-9, -8, 1, 2, 3, 4, 97, 98, 99)
Q101_OBSERVED_CODES = (1, 2, 3, 4, 98, 99)
Q101_EXTRA_DICTIONARY_CODES = (-9, -8, 97)

Q101_DOCUMENTARY_LABELS: Mapping[int, str] = {
    98: "DON'T_KNOW",
    99: "REFUSED_TO_ANSWER",
}

Q101_DOCUMENTARY_MEMBERSHIP = (1, 2, 3, 4, 98, 99)

DESIGN_CARRIERS = ("WT", "PSU", "STRATUM", "SAMPLE", "MODE")
SPLIT_CARRIERS: Mapping[str, tuple[int, ...]] = {
    "SPLITA": (1, 2),
    "SPLITB": (1, 2, 3),
}

UNICODE_WITNESS_VARIABLE = "E2001B"
UNICODE_WITNESS_ROW_ORDINAL = 19250
UNICODE_WITNESS_TEXT = "ظريف"
UNICODE_WITNESS_WIDTH = 21
UNICODE_WITNESS_STORAGE_SLOTS = 3


class Arab5RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise Arab5RealizationError(
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
class SourceAdmission:
    source_sha256: str
    physical_mode: str
    replay_identity: str
    physical_equivalence_claimed: bool = False


def admit_source_binding(
    *,
    source_sha256: str,
    physical_mode: str = SOURCE_PHYSICAL_MODE,
    replay_identity: str = REPLAY_IDENTITY,
) -> SourceAdmission:
    if source_sha256 != CANONICAL_SHA256:
        raise Arab5RealizationError("canonical Arab5 source root mismatch")
    if physical_mode != SOURCE_PHYSICAL_MODE:
        raise Arab5RealizationError("Arab5 physical-mode drift")
    if replay_identity != REPLAY_IDENTITY:
        raise Arab5RealizationError("Arab5 replay-identity drift")
    return SourceAdmission(source_sha256, physical_mode, replay_identity, False)


IDENTITY_AUTHORITY: Mapping[str, Any] = {
    "hard_replay_identity": REPLAY_IDENTITY,
    "native_id_carrier": "ID",
    "native_id_noninjective": True,
    "country_plus_id_still_noninjective": True,
    "accepted_country_plus_id_duplicate_pairs": 3,
    "native_id_hard_replay_authority": False,
    "country_plus_id_hard_replay_authority": False,
}


@dataclass(frozen=True)
class Q101DictionaryState:
    code: int
    source_dictionary_member: bool
    observed_in_accepted_snapshot: bool | None
    documentary_membership: bool
    semantic_status: str
    documentary_label: str | None


def resolve_q101_dictionary_state(code: int) -> Q101DictionaryState:
    source_member = code in Q101_DICTIONARY_KEYS
    observed: bool | None
    if code in Q101_OBSERVED_CODES:
        observed = True
    elif code in Q101_EXTRA_DICTIONARY_CODES:
        observed = False
    else:
        observed = None

    documentary_member = code in Q101_DOCUMENTARY_MEMBERSHIP
    if code in Q101_DOCUMENTARY_LABELS:
        semantic_status = "DOCUMENTARY_CODE_SEMANTICS_RESOLVED"
        label = Q101_DOCUMENTARY_LABELS[code]
    elif documentary_member:
        semantic_status = "DOCUMENTARY_CODE_MEMBERSHIP_RESOLVED__LABEL_NOT_ASSERTED_HERE"
        label = None
    else:
        semantic_status = BOUNDED_UNKNOWN
        label = None

    return Q101DictionaryState(
        code=code,
        source_dictionary_member=source_member,
        observed_in_accepted_snapshot=observed,
        documentary_membership=documentary_member,
        semantic_status=semantic_status,
        documentary_label=label,
    )


def require_full_q101_dictionary(codes: Sequence[int]) -> tuple[int, ...]:
    normalized = tuple(sorted(set(codes)))
    if normalized != tuple(sorted(Q101_DICTIONARY_KEYS)):
        raise Arab5RealizationError(
            "Q101 source dictionary membership changed or pruned"
        )
    return normalized


@dataclass(frozen=True)
class RankedSlot:
    variable_name: str
    rank: int
    documentary_role: str


RANKED_CHALLENGE_SLOTS = (
    RankedSlot("Q2061A", 1, "MOST_IMPORTANT_CHALLENGE"),
    RankedSlot("Q2061B", 2, "SECOND_MOST_IMPORTANT_CHALLENGE"),
)

Q2061B_DOCUMENTARY_CODES: Mapping[int, str] = {
    97: "THERE_IS_NO_SECOND_PROBLEM",
}


def require_ranked_challenge_topology(slots: Sequence[RankedSlot]) -> tuple[RankedSlot, ...]:
    normalized = tuple(slots)
    if normalized != RANKED_CHALLENGE_SLOTS:
        raise Arab5RealizationError(
            "Q2061A/Q2061B ranked-slot topology changed or flattened"
        )
    return normalized


@dataclass(frozen=True)
class SplitCarrierState:
    carrier_name: str
    allowed_documentary_assignments: tuple[int, ...]
    assignment_semantics: str
    item_routing_semantics: str


def split_carrier_state(carrier_name: str) -> SplitCarrierState:
    if carrier_name not in SPLIT_CARRIERS:
        raise Arab5RealizationError("unknown Arab5 split carrier")
    return SplitCarrierState(
        carrier_name=carrier_name,
        allowed_documentary_assignments=SPLIT_CARRIERS[carrier_name],
        assignment_semantics="RANDOM_ASSIGNMENT_DOCUMENTED",
        item_routing_semantics=BOUNDED_UNKNOWN,
    )


@dataclass(frozen=True)
class RoutingResolution:
    target_variable: str
    status: str
    applicability: str
    authority_id: str | None


def resolve_item_routing(
    target_variable: str,
    *,
    authority_id: str | None = None,
    documented_applicability: str | None = None,
    observed_missing_state: str | None = None,
) -> RoutingResolution:
    """Require an explicit documentary join; missingness never supplies routing."""

    del observed_missing_state
    if authority_id is None or documented_applicability is None:
        return RoutingResolution(
            target_variable=target_variable,
            status=BOUNDED_UNKNOWN,
            applicability=BOUNDED_UNKNOWN,
            authority_id=None,
        )
    return RoutingResolution(
        target_variable=target_variable,
        status="DOCUMENTARY_ROUTING_RESOLVED",
        applicability=documented_applicability,
        authority_id=authority_id,
    )


@dataclass(frozen=True)
class DesignCarrierProjection:
    carrier_name: str
    physical_state: str
    raw_storage_value: Any
    semantic_role: str
    row_retention_required: bool
    default_analysis_use_authorized: bool


def project_design_carrier(
    carrier_name: str,
    *,
    physical_state: str,
    raw_value: Any = None,
) -> DesignCarrierProjection:
    if carrier_name not in DESIGN_CARRIERS:
        raise Arab5RealizationError("unknown Arab5 weight/design carrier")

    if physical_state == SYSTEM_MISSING:
        if raw_value is not None:
            raise Arab5RealizationError(
                "SYSTEM_MISSING design carrier may not carry ordinary raw value"
            )
        return DesignCarrierProjection(
            carrier_name=carrier_name,
            physical_state=SYSTEM_MISSING,
            raw_storage_value=None,
            semantic_role=BOUNDED_UNKNOWN,
            row_retention_required=True,
            default_analysis_use_authorized=False,
        )

    if physical_state == ORDINARY_STORED_VALUE:
        return DesignCarrierProjection(
            carrier_name=carrier_name,
            physical_state=ORDINARY_STORED_VALUE,
            raw_storage_value=raw_value,
            semantic_role=BOUNDED_UNKNOWN,
            row_retention_required=True,
            default_analysis_use_authorized=False,
        )

    raise Arab5RealizationError("unsupported physical state for design carrier")


def require_current_design_use_authority(carrier_name: str) -> None:
    if carrier_name not in DESIGN_CARRIERS:
        raise Arab5RealizationError("unknown Arab5 weight/design carrier request")
    raise Arab5RealizationError(
        f"{carrier_name} analytical design/weight role is bounded UNKNOWN"
    )


def preserve_literal_source_text(text: str) -> str:
    if not isinstance(text, str):
        raise Arab5RealizationError("source text must remain a Unicode string")
    return text


@dataclass(frozen=True)
class UnicodeStorageWitness:
    variable_name: str
    row_ordinal: int
    literal_text: str
    width: int
    storage_slots: int


UNICODE_STORAGE_WITNESS = UnicodeStorageWitness(
    variable_name=UNICODE_WITNESS_VARIABLE,
    row_ordinal=UNICODE_WITNESS_ROW_ORDINAL,
    literal_text=UNICODE_WITNESS_TEXT,
    width=UNICODE_WITNESS_WIDTH,
    storage_slots=UNICODE_WITNESS_STORAGE_SLOTS,
)


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
        "semantic_owner": SEMANTIC_OWNER,
        "source": {
            "filename": CANONICAL_FILENAME,
            "sha256": CANONICAL_SHA256,
            "format": SOURCE_FORMAT,
            "physical_mode": SOURCE_PHYSICAL_MODE,
            "declared_encoding": SOURCE_DECLARED_ENCODING,
            "declared_character_code": SOURCE_DECLARED_CHARACTER_CODE,
            "replay_identity": REPLAY_IDENTITY,
            "launch_class": LAUNCH_CLASS,
            "accepted_rows": ACCEPTED_ROW_COUNT,
            "accepted_logical_variables": ACCEPTED_LOGICAL_VARIABLE_COUNT,
            "accepted_storage_slots": ACCEPTED_STORAGE_SLOT_COUNT,
            "native_spss_mr_sets": ACCEPTED_NATIVE_SPSS_MR_SET_COUNT,
        },
        "identity": IDENTITY_AUTHORITY,
        "q101": {
            "dictionary_keys": Q101_DICTIONARY_KEYS,
            "observed_codes": Q101_OBSERVED_CODES,
            "extra_dictionary_codes": Q101_EXTRA_DICTIONARY_CODES,
            "dictionary_membership_is_observation_authority": False,
            "dictionary_membership_is_semantic_authority": False,
            "extra_code_semantics": BOUNDED_UNKNOWN,
        },
        "ranked_topology": [
            {
                "variable_name": slot.variable_name,
                "rank": slot.rank,
                "documentary_role": slot.documentary_role,
            }
            for slot in RANKED_CHALLENGE_SLOTS
        ],
        "q2061b_documentary_codes": {
            str(code): label for code, label in Q2061B_DOCUMENTARY_CODES.items()
        },
        "split_carriers": {
            name: {
                "assignments": assignments,
                "assignment_semantics": "RANDOM_ASSIGNMENT_DOCUMENTED",
                "item_routing_semantics": BOUNDED_UNKNOWN,
            }
            for name, assignments in SPLIT_CARRIERS.items()
        },
        "routing": {
            "missingness_is_authority": False,
            "unjoined_item_route_state": BOUNDED_UNKNOWN,
        },
        "design": {
            "carriers": DESIGN_CARRIERS,
            "semantic_roles": BOUNDED_UNKNOWN,
            "default_weight": None,
            "missing_psu_authorizes_row_drop": False,
            "missing_wt_authorizes_row_drop": False,
        },
        "text": {
            "unicode_preservation": "EXACT_NO_LOSSY_NORMALIZATION",
            "witness_variable": UNICODE_STORAGE_WITNESS.variable_name,
            "witness_row_ordinal": UNICODE_STORAGE_WITNESS.row_ordinal,
            "witness_text": UNICODE_STORAGE_WITNESS.literal_text,
            "witness_width": UNICODE_STORAGE_WITNESS.width,
            "witness_storage_slots": UNICODE_STORAGE_WITNESS.storage_slots,
        },
        "cross_wave": {
            "semantic_imports_allowed": False,
            "wave2_semantics_inherited": False,
            "wave8_semantics_inherited": False,
        },
        "s35_edge_classes": APPLICABLE_EDGE_CLASSES,
        "r35_hooks": R35_HOOK_BINDING,
        "semantic_owner_surface": "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0",
        "candidate_law": "A_B_C_SHARE_ONE_SOURCE_SPECIFIC_SEMANTIC_REALIZATION_IDENTITY",
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
            raise Arab5RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise Arab5RealizationError("candidate source root divergence")
        if (
            self.source_specific_realization_identity
            != SOURCE_SPECIFIC_REALIZATION_IDENTITY
        ):
            raise Arab5RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(
    bindings: Sequence[CandidateSemanticBinding],
) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise Arab5RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise Arab5RealizationError("A/B/C source root divergence")
    if len(
        {binding.source_specific_realization_identity for binding in bindings}
    ) != 1:
        raise Arab5RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "ACCEPTED_LOGICAL_VARIABLE_COUNT",
    "ACCEPTED_ROW_COUNT",
    "ACCEPTED_STORAGE_SLOT_COUNT",
    "APPLICABLE_EDGE_CLASSES",
    "Arab5RealizationError",
    "BOUNDED_UNKNOWN",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "CONTRACT_ID",
    "CandidateSemanticBinding",
    "DESIGN_CARRIERS",
    "IDENTITY_AUTHORITY",
    "LAUNCH_CLASS",
    "ORDINARY_STORED_VALUE",
    "Q101_DICTIONARY_KEYS",
    "Q101_EXTRA_DICTIONARY_CODES",
    "Q101_OBSERVED_CODES",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "RANKED_CHALLENGE_SLOTS",
    "REPLAY_IDENTITY",
    "SEMANTIC_OWNER",
    "SOURCE_PHYSICAL_MODE",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "SPLIT_CARRIERS",
    "SYSTEM_MISSING",
    "UNICODE_STORAGE_WITNESS",
    "admit_source_binding",
    "canonical_digest",
    "preserve_literal_source_text",
    "project_design_carrier",
    "require_common_abc_semantic_law",
    "require_current_design_use_authority",
    "require_full_q101_dictionary",
    "require_ranked_challenge_topology",
    "resolve_item_routing",
    "resolve_q101_dictionary_state",
    "source_specific_realization_payload",
    "split_carrier_state",
]
