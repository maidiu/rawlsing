"""Governed source-specific realization law for CLOSED_35 Arab Barometer Wave 2.

This module never reads the SAV. It freezes the candidate-neutral semantic law
that later A/B/C realizations must share after independent physical extraction.

The central invariant is that physical state, source dictionary metadata,
documentary semantics, routing applicability, and analytical weight authority
remain separate jurisdictions. In particular, an ordinary stored zero is not
SYSTEM_MISSING merely because its source dictionary label contains "missing".
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence


CONTRACT_ID = "CLOSED35_R2_ARAB2_SOURCE_REALIZATION@1.0.0"
SEMANTIC_OWNER = "ARAB2_SEMANTIC_OWNER_V1"
CANONICAL_FILENAME = "Arab Barometer Wave 2.sav"
CANONICAL_SHA256 = "6529841b97bd56463490d810ad24ceaa4866066d12e4651a7081682d413606a1"
SOURCE_FORMAT = "SAV"
SOURCE_PHYSICAL_MODE = "SAV_NATIVE_GOVERNED"
SOURCE_DECLARED_ENCODING = "UTF-8"
SOURCE_DECLARED_CHARACTER_CODE = 65001
REPLAY_IDENTITY = "SOURCE_SHA256+ROW_ORDINAL"
LAUNCH_CLASS = "L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED"
BOUNDED_UNKNOWN = "BOUNDED_UNKNOWN"

SYSTEM_MISSING = "SYSTEM_MISSING"
ORDINARY_STORED_VALUE = "ORDINARY_STORED_VALUE"
Q2062_ZERO_SOURCE_DICTIONARY_LABEL = "0. missing"

APPLICABLE_EDGE_CLASSES = ("EC01", "EC05", "EC09", "EC10", "EC12", "EC14")

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
    "weight_design_variables",
)

DOCUMENTARY_CODE_AUTHORITY: Mapping[tuple[str, int], str] = {
    ("Q101", 8): "I don't know",
    ("Q101", 9): "Declined to answer",
    ("Q2062", 99998): "I don't know",
    ("Q2062", 99999): "Declined to answer",
}


class Arab2RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise Arab2RealizationError(
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
        raise Arab2RealizationError("canonical Arab2 source root mismatch")
    if physical_mode != SOURCE_PHYSICAL_MODE:
        raise Arab2RealizationError("Arab2 physical-mode drift")
    if replay_identity != REPLAY_IDENTITY:
        raise Arab2RealizationError("Arab2 replay-identity drift")
    return SourceAdmission(source_sha256, physical_mode, replay_identity, False)


@dataclass(frozen=True)
class SemanticCodeResolution:
    variable_name: str
    raw_value: Any
    status: str
    documentary_label: str | None
    source_dictionary_label: str | None = None


def resolve_semantic_code(
    variable_name: str,
    raw_value: Any,
    *,
    source_dictionary_label: str | None = None,
) -> SemanticCodeResolution:
    """Resolve only exact documentary code authority; never infer from raw value/label."""

    key = (variable_name, raw_value)
    if key in DOCUMENTARY_CODE_AUTHORITY:
        return SemanticCodeResolution(
            variable_name=variable_name,
            raw_value=raw_value,
            status="DOCUMENTARY_CODE_SEMANTICS_RESOLVED",
            documentary_label=DOCUMENTARY_CODE_AUTHORITY[key],
            source_dictionary_label=source_dictionary_label,
        )
    return SemanticCodeResolution(
        variable_name=variable_name,
        raw_value=raw_value,
        status=BOUNDED_UNKNOWN,
        documentary_label=None,
        source_dictionary_label=source_dictionary_label,
    )


@dataclass(frozen=True)
class MissingStateProjection:
    variable_name: str
    physical_state: str
    raw_storage_value: Any
    source_dictionary_label: str | None
    documentary_semantic_state: str
    semantic_refinement: str


def project_q2062_state(
    *,
    physical_state: str,
    raw_value: Any = None,
) -> MissingStateProjection:
    """Freeze the two hostile Q2062 state classes without semantic coercion."""

    if physical_state == SYSTEM_MISSING:
        if raw_value is not None:
            raise Arab2RealizationError(
                "SYSTEM_MISSING fixture may not carry an ordinary raw value"
            )
        return MissingStateProjection(
            variable_name="Q2062",
            physical_state=SYSTEM_MISSING,
            raw_storage_value=None,
            source_dictionary_label=None,
            documentary_semantic_state=BOUNDED_UNKNOWN,
            semantic_refinement=BOUNDED_UNKNOWN,
        )

    if physical_state == ORDINARY_STORED_VALUE:
        if raw_value == 0:
            return MissingStateProjection(
                variable_name="Q2062",
                physical_state=ORDINARY_STORED_VALUE,
                raw_storage_value=0,
                source_dictionary_label=Q2062_ZERO_SOURCE_DICTIONARY_LABEL,
                documentary_semantic_state=BOUNDED_UNKNOWN,
                semantic_refinement=BOUNDED_UNKNOWN,
            )
        semantic = resolve_semantic_code("Q2062", raw_value)
        return MissingStateProjection(
            variable_name="Q2062",
            physical_state=ORDINARY_STORED_VALUE,
            raw_storage_value=raw_value,
            source_dictionary_label=None,
            documentary_semantic_state=semantic.status,
            semantic_refinement=semantic.documentary_label or BOUNDED_UNKNOWN,
        )

    raise Arab2RealizationError("unsupported Q2062 physical state")


@dataclass(frozen=True)
class RankedSlot:
    variable_name: str
    rank: int
    documentary_role: str


RANKED_CHALLENGE_SLOTS = (
    RankedSlot("Q2061", 1, "MOST_IMPORTANT_CHALLENGE"),
    RankedSlot("Q2062", 2, "SECOND_MOST_IMPORTANT_CHALLENGE"),
)


def require_ranked_challenge_topology(slots: Sequence[RankedSlot]) -> tuple[RankedSlot, ...]:
    normalized = tuple(slots)
    if normalized != RANKED_CHALLENGE_SLOTS:
        raise Arab2RealizationError(
            "Q2061/Q2062 ranked-slot topology changed or flattened"
        )
    return normalized


@dataclass(frozen=True)
class DocumentaryRoutingRule:
    route_id: str
    target_variable: str
    country_name: str
    applicability: str
    documentary_authority: str


ROUTING_RULES = (
    DocumentaryRoutingRule(
        route_id="AB2_RT_Q2062_LBN",
        target_variable="Q2062",
        country_name="Lebanon",
        applicability="SECOND_RANK_NOT_RECORDED_BY_INSTRUMENT",
        documentary_authority="ARAB_BAR_W2_QUESTIONNAIRE_ENGLISH_PP11_13",
    ),
)


@dataclass(frozen=True)
class RoutingResolution:
    target_variable: str
    country_name: str | None
    status: str
    applicability: str
    route_id: str | None
    documentary_authority: str | None


def resolve_documentary_routing(
    target_variable: str,
    *,
    country_name: str | None,
    rules: Sequence[DocumentaryRoutingRule] = ROUTING_RULES,
    observed_missing_state: str | None = None,
) -> RoutingResolution:
    """Resolve applicability from exact documentary rules, never from missingness."""

    del observed_missing_state
    exact = [
        rule
        for rule in rules
        if rule.target_variable == target_variable
        and rule.country_name == country_name
    ]
    if not exact:
        return RoutingResolution(
            target_variable=target_variable,
            country_name=country_name,
            status=BOUNDED_UNKNOWN,
            applicability=BOUNDED_UNKNOWN,
            route_id=None,
            documentary_authority=None,
        )
    if len(exact) != 1:
        raise Arab2RealizationError("ambiguous documentary routing authority")
    rule = exact[0]
    return RoutingResolution(
        target_variable=target_variable,
        country_name=country_name,
        status="DOCUMENTARY_ROUTING_RESOLVED",
        applicability=rule.applicability,
        route_id=rule.route_id,
        documentary_authority=rule.documentary_authority,
    )


@dataclass(frozen=True)
class WeightCarrierAuthority:
    carrier_name: str
    carrier_preservation: str
    estimand: str
    normalization: str
    relation_to_sample_carrier: str
    default_use_authorized: bool


WT_AUTHORITY = WeightCarrierAuthority(
    carrier_name="WT",
    carrier_preservation="REQUIRED_SOURCE_CARRIER",
    estimand=BOUNDED_UNKNOWN,
    normalization=BOUNDED_UNKNOWN,
    relation_to_sample_carrier=BOUNDED_UNKNOWN,
    default_use_authorized=False,
)


def require_current_weight_use_authority(carrier_name: str = "WT") -> None:
    if carrier_name != "WT":
        raise Arab2RealizationError("unknown Arab2 weight carrier request")
    raise Arab2RealizationError(
        "WT estimand/default-use authority is bounded UNKNOWN in this realization"
    )


IDENTITY_AUTHORITY: Mapping[str, Any] = {
    "hard_replay_identity": REPLAY_IDENTITY,
    "QID_documentary_role": "QUESTIONNAIRE_ID_NUMBER",
    "QID_hard_replay_authority": False,
    "COUNTRY_PLUS_QID_hard_replay_authority": False,
    "COUNTRY_PLUS_QID_empirical_injectivity_is_semantic_authority": False,
}

SAMPLE_AUTHORITY: Mapping[str, Any] = {
    "carrier": "SAMP",
    "documentary_codes": {"1": "MAIN_SAMPLE", "2": "ADDITIONAL_SAMPLE"},
    "weight_estimand_relation": BOUNDED_UNKNOWN,
    "identity_relation": BOUNDED_UNKNOWN,
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
        },
        "missing_state_law": {
            "system_missing_distinct_from_ordinary_zero": True,
            "q2062_zero_source_dictionary_label": Q2062_ZERO_SOURCE_DICTIONARY_LABEL,
            "q2062_zero_semantic_refinement": BOUNDED_UNKNOWN,
            "source_dictionary_label_is_semantic_authority": False,
        },
        "documentary_codes": {
            f"{variable}:{value}": label
            for (variable, value), label in DOCUMENTARY_CODE_AUTHORITY.items()
        },
        "ranked_topology": [
            {
                "variable_name": slot.variable_name,
                "rank": slot.rank,
                "documentary_role": slot.documentary_role,
            }
            for slot in RANKED_CHALLENGE_SLOTS
        ],
        "routing": {
            "missingness_is_authority": False,
            "rules": [
                {
                    "route_id": rule.route_id,
                    "target_variable": rule.target_variable,
                    "country_name": rule.country_name,
                    "applicability": rule.applicability,
                    "documentary_authority": rule.documentary_authority,
                }
                for rule in ROUTING_RULES
            ],
            "unclosed_route_state": BOUNDED_UNKNOWN,
        },
        "identity": IDENTITY_AUTHORITY,
        "sample": SAMPLE_AUTHORITY,
        "weight": {
            "carrier_name": WT_AUTHORITY.carrier_name,
            "carrier_preservation": WT_AUTHORITY.carrier_preservation,
            "estimand": WT_AUTHORITY.estimand,
            "normalization": WT_AUTHORITY.normalization,
            "relation_to_sample_carrier": WT_AUTHORITY.relation_to_sample_carrier,
            "default_use_authorized": WT_AUTHORITY.default_use_authorized,
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
            raise Arab2RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise Arab2RealizationError("candidate source root divergence")
        if (
            self.source_specific_realization_identity
            != SOURCE_SPECIFIC_REALIZATION_IDENTITY
        ):
            raise Arab2RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(
    bindings: Sequence[CandidateSemanticBinding],
) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise Arab2RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise Arab2RealizationError("A/B/C source root divergence")
    if len(
        {binding.source_specific_realization_identity for binding in bindings}
    ) != 1:
        raise Arab2RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "APPLICABLE_EDGE_CLASSES",
    "Arab2RealizationError",
    "BOUNDED_UNKNOWN",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "CONTRACT_ID",
    "CandidateSemanticBinding",
    "DOCUMENTARY_CODE_AUTHORITY",
    "IDENTITY_AUTHORITY",
    "LAUNCH_CLASS",
    "ORDINARY_STORED_VALUE",
    "Q2062_ZERO_SOURCE_DICTIONARY_LABEL",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "RANKED_CHALLENGE_SLOTS",
    "REPLAY_IDENTITY",
    "ROUTING_RULES",
    "SAMPLE_AUTHORITY",
    "SEMANTIC_OWNER",
    "SOURCE_PHYSICAL_MODE",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "SYSTEM_MISSING",
    "WT_AUTHORITY",
    "admit_source_binding",
    "canonical_digest",
    "project_q2062_state",
    "require_common_abc_semantic_law",
    "require_current_weight_use_authority",
    "require_ranked_challenge_topology",
    "resolve_documentary_routing",
    "resolve_semantic_code",
    "source_specific_realization_payload",
]
