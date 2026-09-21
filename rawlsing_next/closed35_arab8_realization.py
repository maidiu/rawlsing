"""Governed source-specific realization law for CLOSED_35 Arab Barometer Wave 8.

This module never reads the SAV. It freezes one candidate-neutral semantic law
that later A/B/C physical realizations must share.

Physical source states, documentary routing, variable identity, and analytic
weight/design authority are separate jurisdictions. In particular:
- ID=0 is an ordinary source value and never a hard replay key;
- BLOCK_ID="" is an ordinary stored blank, not SYSTEM_MISSING;
- Q1 and STRATUM remain distinct variables even when their source vectors are equal;
- routing follows exact Wave 8 documentary rules, never empirical missingness;
- WT/PSU/STRATUM remain source carriers without invented estimand/default use.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence


CONTRACT_ID = "CLOSED35_R3_ARAB8_SOURCE_REALIZATION@1.0.0"
SEMANTIC_OWNER = "ARAB8_SEMANTIC_OWNER_V1"
CANONICAL_FILENAME = "Arab Barometer Wave 8.sav"
CANONICAL_SHA256 = "a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998"
SOURCE_FORMAT = "SAV"
SOURCE_PHYSICAL_MODE = "SAV_NATIVE_GOVERNED"
SOURCE_DECLARED_ENCODING = "UTF-8"
SOURCE_DECLARED_CHARACTER_CODE = 65001
REPLAY_IDENTITY = "SOURCE_SHA256+ROW_ORDINAL"
LAUNCH_CLASS = "L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED"
BOUNDED_UNKNOWN = "BOUNDED_UNKNOWN"

ORDINARY_STORED_VALUE = "ORDINARY_STORED_VALUE"
SYSTEM_MISSING = "SYSTEM_MISSING"

APPLICABLE_EDGE_CLASSES = ("EC01", "EC05", "EC07", "EC10", "EC12", "EC14")

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
    "form_module_skip_routing_carriers",
    "weight_design_variables",
)


class Arab8RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise Arab8RealizationError(
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
        raise Arab8RealizationError("canonical Arab8 source root mismatch")
    if physical_mode != SOURCE_PHYSICAL_MODE:
        raise Arab8RealizationError("Arab8 physical-mode drift")
    if replay_identity != REPLAY_IDENTITY:
        raise Arab8RealizationError("Arab8 replay-identity drift")
    return SourceAdmission(source_sha256, physical_mode, replay_identity, False)


@dataclass(frozen=True)
class NativeIdentifierProjection:
    variable_name: str
    raw_value: Any
    physical_state: str
    documentary_role: str
    hard_replay_authority: bool


def project_id(raw_value: Any) -> NativeIdentifierProjection:
    """Preserve ID exactly, including ordinary zero, without minting identity authority."""

    return NativeIdentifierProjection(
        variable_name="ID",
        raw_value=raw_value,
        physical_state=ORDINARY_STORED_VALUE,
        documentary_role="RESPONDENT_ID_NUMBER",
        hard_replay_authority=False,
    )


IDENTITY_AUTHORITY: Mapping[str, Any] = {
    "hard_replay_identity": REPLAY_IDENTITY,
    "ID_documentary_role": "RESPONDENT_ID_NUMBER",
    "ID_zero_physical_state": ORDINARY_STORED_VALUE,
    "ID_hard_replay_authority": False,
    "COUNTRY_PLUS_ID_hard_replay_authority": False,
    "accepted_snapshot_zero_id_count": 2400,
    "accepted_snapshot_zero_id_country_code": 8,
}


@dataclass(frozen=True)
class BlockIdProjection:
    raw_value: str
    physical_state: str
    semantic_state: str


def project_block_id(raw_value: str) -> BlockIdProjection:
    if not isinstance(raw_value, str):
        raise Arab8RealizationError("BLOCK_ID must remain a source string")
    return BlockIdProjection(
        raw_value=raw_value,
        physical_state=ORDINARY_STORED_VALUE,
        semantic_state=BOUNDED_UNKNOWN,
    )


BLOCK_ID_AUTHORITY: Mapping[str, Any] = {
    "carrier": "BLOCK_ID",
    "ordinary_blank_is_system_missing": False,
    "accepted_snapshot_blank_count": 2408,
    "accepted_snapshot_system_missing_count": 0,
    "blank_semantics": BOUNDED_UNKNOWN,
    "block_identifier_jurisdiction": BOUNDED_UNKNOWN,
}


@dataclass(frozen=True)
class VariableIdentityRule:
    variable_name: str
    documentary_role: str
    semantic_state: str


Q1_IDENTITY = VariableIdentityRule(
    variable_name="Q1",
    documentary_role="GOVERNORATE_FIRST_ADMINISTRATIVE_DIVISION",
    semantic_state="SOURCE_NATIVE_DOCUMENTARY_ROLE",
)
STRATUM_IDENTITY = VariableIdentityRule(
    variable_name="STRATUM",
    documentary_role=BOUNDED_UNKNOWN,
    semantic_state=BOUNDED_UNKNOWN,
)


def require_q1_stratum_nonalias(
    *,
    vectors_equal: bool,
    semantic_alias_requested: bool = False,
) -> tuple[VariableIdentityRule, VariableIdentityRule]:
    """Equal vectors never create alias authority."""

    del vectors_equal
    if semantic_alias_requested:
        raise Arab8RealizationError(
            "Q1/STRATUM semantic alias requires independent documentary authority"
        )
    return Q1_IDENTITY, STRATUM_IDENTITY


@dataclass(frozen=True)
class DocumentaryRoutingRule:
    route_id: str
    target: str
    country_code: int
    split_assignment: str | None
    applicability: str
    topology: str | None
    documentary_authority: str


ROUTING_RULES = (
    DocumentaryRoutingRule(
        route_id="AB8_RT_Q1A_PAL_COUNTRY15",
        target="Q1A_PAL",
        country_code=15,
        split_assignment=None,
        applicability="APPLIES_FOR_COUNTRY_15",
        topology=None,
        documentary_authority="ARAB_BAROMETER_W8_QUESTIONNAIRE_P5",
    ),
    DocumentaryRoutingRule(
        route_id="AB8_RT_Q622C_IRQ_COUNTRY7_SPLITA",
        target="Q622C_IRQ_*",
        country_code=7,
        split_assignment="A",
        applicability="APPLIES_FOR_COUNTRY_7_SPLIT_A",
        topology="SELECT_ALL_THAT_APPLY",
        documentary_authority="ARAB_BAROMETER_W8_QUESTIONNAIRE_P47",
    ),
)


@dataclass(frozen=True)
class RoutingResolution:
    target: str
    status: str
    applicability: str
    topology: str | None
    route_id: str | None
    documentary_authority: str | None


def resolve_documentary_routing(
    target: str,
    *,
    country_code: int | None,
    split_assignment: str | None = None,
    observed_missing_state: str | None = None,
    rules: Sequence[DocumentaryRoutingRule] = ROUTING_RULES,
) -> RoutingResolution:
    """Resolve only exact documentary routes; missingness has no routing authority."""

    del observed_missing_state
    exact = [
        rule
        for rule in rules
        if rule.target == target
        and rule.country_code == country_code
        and rule.split_assignment == split_assignment
    ]
    if not exact:
        return RoutingResolution(
            target=target,
            status=BOUNDED_UNKNOWN,
            applicability=BOUNDED_UNKNOWN,
            topology=None,
            route_id=None,
            documentary_authority=None,
        )
    if len(exact) != 1:
        raise Arab8RealizationError("ambiguous Wave 8 documentary routing authority")
    rule = exact[0]
    return RoutingResolution(
        target=target,
        status="DOCUMENTARY_ROUTING_RESOLVED",
        applicability=rule.applicability,
        topology=rule.topology,
        route_id=rule.route_id,
        documentary_authority=rule.documentary_authority,
    )


Q622C_TOPOLOGY: Mapping[str, Any] = {
    "group": "Q622C_IRQ_*",
    "documentary_topology": "SELECT_ALL_THAT_APPLY",
    "native_spss_mr_metadata": False,
    "member_variables_remain_distinct": True,
    "scalar_flattening_authorized": False,
}


def require_q622c_member_topology(member_names: Sequence[str]) -> tuple[str, ...]:
    members = tuple(member_names)
    if not members:
        raise Arab8RealizationError("Q622C_IRQ member topology cannot be empty")
    if len(set(members)) != len(members):
        raise Arab8RealizationError("Q622C_IRQ member topology cannot deduplicate")
    if any(not name.startswith("Q622C_IRQ_") for name in members):
        raise Arab8RealizationError("Q622C_IRQ member topology cannot be scalar-flattened")
    return members


@dataclass(frozen=True)
class DesignCarrierAuthority:
    carrier_name: str
    physical_preservation: str
    documentary_role: str
    analytic_role: str
    default_use_authorized: bool


DESIGN_CARRIERS = (
    DesignCarrierAuthority(
        "WT",
        "REQUIRED_SOURCE_CARRIER",
        BOUNDED_UNKNOWN,
        BOUNDED_UNKNOWN,
        False,
    ),
    DesignCarrierAuthority(
        "PSU",
        "REQUIRED_SOURCE_CARRIER",
        "SOURCE_NATIVE_SAMPLING_VARIABLE",
        BOUNDED_UNKNOWN,
        False,
    ),
    DesignCarrierAuthority(
        "STRATUM",
        "REQUIRED_SOURCE_CARRIER",
        BOUNDED_UNKNOWN,
        BOUNDED_UNKNOWN,
        False,
    ),
)


def require_current_design_or_weight_use_authority(carrier_name: str) -> None:
    known = {carrier.carrier_name for carrier in DESIGN_CARRIERS}
    if carrier_name not in known:
        raise Arab8RealizationError("unknown Arab8 design/weight carrier request")
    raise Arab8RealizationError(
        f"{carrier_name} analytic/design authority is bounded UNKNOWN in this realization"
    )


def require_wave8_documentary_scope(authority_wave: str) -> str:
    if authority_wave != "Wave 8":
        raise Arab8RealizationError(
            "cross-wave Arab Barometer semantics are not authority for Wave 8"
        )
    return authority_wave


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
        "identity": IDENTITY_AUTHORITY,
        "block_id": BLOCK_ID_AUTHORITY,
        "q1_stratum": {
            "q1": Q1_IDENTITY.__dict__,
            "stratum": STRATUM_IDENTITY.__dict__,
            "accepted_snapshot_vectors_equal": True,
            "accepted_snapshot_equal_row_count": 15627,
            "semantic_alias_authorized": False,
        },
        "routing": {
            "missingness_is_authority": False,
            "rules": [rule.__dict__ for rule in ROUTING_RULES],
            "unclosed_route_state": BOUNDED_UNKNOWN,
        },
        "q622c_topology": Q622C_TOPOLOGY,
        "design_carriers": [carrier.__dict__ for carrier in DESIGN_CARRIERS],
        "bounded_unknowns": (
            "BLOCK_ID_EXACT_SEMANTICS",
            "BLOCK_ID_BLANK_EXACT_SEMANTICS",
            "WT_ESTIMAND_AND_NORMALIZATION",
            "STRATUM_DESIGN_SEMANTICS",
            "PSU_ANALYTIC_DESIGN_USE_BEYOND_DOCUMENTED_CARRIER_ROLE",
            "Q1_STRATUM_EQUALITY_CAUSAL_OR_SEMANTIC_RELATION",
            "UNDOCUMENTED_COUNTRY_MODULE_ROUTING",
            "CROSS_WAVE_SEMANTIC_EQUIVALENCE",
        ),
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
            raise Arab8RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise Arab8RealizationError("candidate source root divergence")
        if (
            self.source_specific_realization_identity
            != SOURCE_SPECIFIC_REALIZATION_IDENTITY
        ):
            raise Arab8RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(
    bindings: Sequence[CandidateSemanticBinding],
) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise Arab8RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise Arab8RealizationError("A/B/C source root divergence")
    if len(
        {binding.source_specific_realization_identity for binding in bindings}
    ) != 1:
        raise Arab8RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "APPLICABLE_EDGE_CLASSES",
    "Arab8RealizationError",
    "BLOCK_ID_AUTHORITY",
    "BOUNDED_UNKNOWN",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "CONTRACT_ID",
    "CandidateSemanticBinding",
    "DESIGN_CARRIERS",
    "IDENTITY_AUTHORITY",
    "LAUNCH_CLASS",
    "ORDINARY_STORED_VALUE",
    "Q1_IDENTITY",
    "Q622C_TOPOLOGY",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "REPLAY_IDENTITY",
    "ROUTING_RULES",
    "SEMANTIC_OWNER",
    "SOURCE_PHYSICAL_MODE",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "STRATUM_IDENTITY",
    "SYSTEM_MISSING",
    "admit_source_binding",
    "canonical_digest",
    "project_block_id",
    "project_id",
    "require_common_abc_semantic_law",
    "require_current_design_or_weight_use_authority",
    "require_q1_stratum_nonalias",
    "require_q622c_member_topology",
    "require_wave8_documentary_scope",
    "resolve_documentary_routing",
    "source_specific_realization_payload",
]
