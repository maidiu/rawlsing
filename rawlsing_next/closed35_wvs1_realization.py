"""Governed source-specific realization law for CLOSED_35 WVS Wave 1.

This module is source-independent: it never opens or decodes WVS Wave 1.sav.
It freezes the candidate-neutral authority surface that later A/B/C physical
realizations must consume.

The central law is non-conversion:
- display metadata never rewrites raw storage;
- native identifier-looking fields never replace source-SHA + row ordinal;
- physical missing states never mint routing/applicability semantics;
- all-system columns remain source information;
- weight-carrier presence never selects an estimand or default weight.

Remaining identity, weight/design, and routing semantics are intentionally
preserved as BOUNDED_UNKNOWN where accepted Authority71/72 evidence does not
close them.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence


CONTRACT_ID = "CLOSED35_R2_WVS1_SOURCE_REALIZATION@1.0.0"
CANONICAL_FILENAME = "WVS Wave 1.sav"
CANONICAL_SHA256 = "051bf450568f44181559a5b2bfbe58b4f05b58bc806643d0c63353c937ff0824"
SOURCE_FORMAT = "SAV"
SOURCE_FAMILY = "WVS"
SOURCE_RELEASE = "Wave 1"
DECODER_MODE = "SAV_NATIVE_GOVERNED"
COMPATIBILITY_STATUS = "NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE"
COMPATIBILITY_SEMANTIC_CLAIM = "NO_COMPATIBILITY_OVERRIDE__NO_SEMANTIC_CLAIM"
REPLAY_IDENTITY_LAW = "SOURCE_SHA256+ROW_ORDINAL"
BOUNDED_UNKNOWN = "BOUNDED_UNKNOWN"

S007_VARIABLE = "S007"
S007_DOCUMENTARY_NAME = "Unified respondent number"
S007_DISPLAY_FORMAT_SENTINEL = "F2.0"
S007_DOCUMENTARY_DOMAIN = "1..9999999999"
S007_ACCEPTED_RAW_MIN = 320120001
S007_ACCEPTED_RAW_MAX = 8400122325

V3_VARIABLE = "V3"
V3_DOCUMENTARY_NAME = "Original respondent number"

NAMED_ALL_SYSTEM_SENTINEL = "I_WOMPOL"
ACCEPTED_ALL_SYSTEM_COLUMN_COUNT = 8

WEIGHT_CARRIERS = (
    "V236",
    "SECVALWGT",
    "RESEMAWEIGHT",
    "WEIGHT1A",
    "WEIGHT2A",
    "WEIGHT3A",
    "WEIGHT4A",
    "WEIGHT1B",
    "WEIGHT2B",
    "WEIGHT3B",
    "WEIGHT4B",
    "S018",
    "S019",
)

DOCUMENTED_WEIGHT_LABELS: Mapping[str, str] = {
    "V236": "Weight",
    "S018": "Equilibrated weight-1000",
    "S019": "Equilibrated weight-1500",
}

APPLICABLE_EDGE_CLASSES = ("EC01", "EC04", "EC05", "EC06", "EC12", "EC14")
R35_REQUIRED_PHYSICAL_DIMENSIONS = (
    "physical_metadata",
    "variable_inventory_order",
    "raw_storage_values",
    "row_replay_identity",
    "raw_display_separation",
    "typed_missingness",
    "all_missing_column_retention",
    "weight_design_variables",
)

R35_PHYSICAL_METADATA_SCHEMA = "PRE553_PHYSICAL_METADATA@1.0.0"
R35_CANONICAL_SOURCE_RECEIPT_SCHEMA = "FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0"
R35_DERIVATIVE_PARENTAGE_BUNDLE_SCHEMA = "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0"
R35_PHYSICAL_SCOPE_SCHEMA = "FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0"
R35_PHYSICAL_EXPECTATION_SCHEMA = "FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0"
R35_PHYSICAL_REALIZATION_SCHEMA = "FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0"
R35_PHYSICAL_EQUIVALENCE_RECEIPT_SCHEMA = "FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0"

ALLOWED_PHYSICAL_STATES = frozenset({
    "OBSERVED_STORAGE_VALUE",
    "SYSTEM_MISSING",
    "FORMAT_USER_MISSING_VALUE",
    "FORMAT_USER_MISSING_RANGE",
    "FORMAT_EXTENDED_MISSING",
    "SOURCE_CELL_ABSENT_OR_UNREPRESENTED",
    "PHYSICAL_STATE_UNKNOWN",
})


class WVS1RealizationError(ValueError):
    """Fail-closed WVS1 source-realization violation."""


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise WVS1RealizationError(f"non-canonical realization material: {type(value).__name__}")


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        _canonical(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WVS1RealizationError(f"{name} must be a non-empty string")
    return value


def admit_source_identity(source_sha256: str) -> str:
    """Admit only the exact canonical WVS1 physical root."""
    if source_sha256 != CANONICAL_SHA256:
        raise WVS1RealizationError("canonical WVS1 source root mismatch")
    return source_sha256


@dataclass(frozen=True)
class ReplayIdentity:
    source_sha256: str
    row_ordinal: int

    def __post_init__(self) -> None:
        admit_source_identity(self.source_sha256)
        if isinstance(self.row_ordinal, bool) or not isinstance(self.row_ordinal, int) or self.row_ordinal < 0:
            raise WVS1RealizationError("row_ordinal must be a non-negative integer")

    @property
    def key(self) -> str:
        return f"{self.source_sha256}:{self.row_ordinal}"


def replay_identity(row_ordinal: int, *, source_sha256: str = CANONICAL_SHA256) -> ReplayIdentity:
    """The only hard replay identity: exact source SHA + physical row ordinal."""
    return ReplayIdentity(source_sha256=source_sha256, row_ordinal=row_ordinal)


@dataclass(frozen=True)
class NativeIdentityEvidence:
    variable_name: str
    documentary_name: str | None
    physical_value: Any
    source_local_injectivity_observed: bool | None
    semantic_role: str = BOUNDED_UNKNOWN
    replay_authority: bool = False

    def __post_init__(self) -> None:
        _nonempty(self.variable_name, "variable_name")
        if self.replay_authority:
            raise WVS1RealizationError(
                "native identifier-looking fields cannot replace source-SHA + row-ordinal replay identity"
            )


def preserve_native_identity_evidence(
    variable_name: str,
    *,
    physical_value: Any,
    source_local_injectivity_observed: bool | None = None,
    documentary_name: str | None = None,
) -> NativeIdentityEvidence:
    """Preserve source-local identifier evidence without promoting it to a key."""
    if variable_name == S007_VARIABLE and documentary_name is None:
        documentary_name = S007_DOCUMENTARY_NAME
    if variable_name == V3_VARIABLE and documentary_name is None:
        documentary_name = V3_DOCUMENTARY_NAME
    return NativeIdentityEvidence(
        variable_name=variable_name,
        documentary_name=documentary_name,
        physical_value=physical_value,
        source_local_injectivity_observed=source_local_injectivity_observed,
    )


@dataclass(frozen=True)
class RawDisplayProjection:
    variable_name: str
    raw_storage_value: Any
    display_metadata: Mapping[str, Any]
    display_rendering: str | None
    semantic_role: str
    display_is_raw_value_authority: bool = False

    def __post_init__(self) -> None:
        _nonempty(self.variable_name, "variable_name")
        if self.display_is_raw_value_authority:
            raise WVS1RealizationError("display metadata/rendering cannot become raw-value authority")


def preserve_raw_display_separation(
    variable_name: str,
    *,
    raw_storage_value: Any,
    display_metadata: Mapping[str, Any],
    display_rendering: str | None = None,
) -> RawDisplayProjection:
    """Preserve raw storage and display evidence as independent witnesses.

    No parsing, truncation, width coercion, rounding, or rescaling is performed.
    """
    _nonempty(variable_name, "variable_name")
    if not isinstance(display_metadata, Mapping):
        raise WVS1RealizationError("display_metadata must be a mapping")
    if variable_name == S007_VARIABLE:
        if isinstance(raw_storage_value, bool) or not isinstance(raw_storage_value, (int, float)):
            raise WVS1RealizationError("S007 raw storage must remain numeric physical evidence")
        semantic_role = "SOURCE_LOCAL_IDENTITY_EVIDENCE__SEMANTIC_ROLE_BOUNDED_UNKNOWN"
    else:
        semantic_role = BOUNDED_UNKNOWN
    return RawDisplayProjection(
        variable_name=variable_name,
        raw_storage_value=raw_storage_value,
        display_metadata=dict(display_metadata),
        display_rendering=display_rendering,
        semantic_role=semantic_role,
    )


@dataclass(frozen=True)
class TypedMissingProjection:
    variable_name: str
    physical_state: str
    raw_storage_value: Any
    missing_declaration: Mapping[str, Any] | None
    documentary_label: str | None
    semantic_response_state: str = BOUNDED_UNKNOWN
    routing_applicability_state: str = BOUNDED_UNKNOWN

    def __post_init__(self) -> None:
        _nonempty(self.variable_name, "variable_name")
        if self.physical_state not in ALLOWED_PHYSICAL_STATES:
            raise WVS1RealizationError("unrecognized physical missing-state token")
        if self.physical_state == "SYSTEM_MISSING" and self.raw_storage_value is not None:
            raise WVS1RealizationError("SYSTEM_MISSING must not be rewritten as an ordinary raw code")


def preserve_typed_missingness(
    variable_name: str,
    *,
    physical_state: str,
    raw_storage_value: Any = None,
    missing_declaration: Mapping[str, Any] | None = None,
    documentary_label: str | None = None,
) -> TypedMissingProjection:
    """Preserve physical missing class without inferring response/routing meaning."""
    if missing_declaration is not None and not isinstance(missing_declaration, Mapping):
        raise WVS1RealizationError("missing_declaration must be a mapping or None")
    return TypedMissingProjection(
        variable_name=variable_name,
        physical_state=physical_state,
        raw_storage_value=raw_storage_value,
        missing_declaration=None if missing_declaration is None else dict(missing_declaration),
        documentary_label=documentary_label,
    )


@dataclass(frozen=True)
class AllSystemColumnProjection:
    variable_name: str
    row_count: int
    system_missing_count: int
    declared_user_missing_metadata: Any
    retained: bool = True
    semantic_role: str = BOUNDED_UNKNOWN
    routing_applicability_state: str = BOUNDED_UNKNOWN

    def __post_init__(self) -> None:
        _nonempty(self.variable_name, "variable_name")
        if self.row_count < 0 or self.system_missing_count < 0:
            raise WVS1RealizationError("row/system-missing counts must be non-negative")
        if self.system_missing_count != self.row_count:
            raise WVS1RealizationError("all-system projection requires system_missing_count == row_count")
        if not self.retained:
            raise WVS1RealizationError("all-system columns may not be deleted")


def preserve_all_system_column(
    variable_name: str,
    *,
    row_count: int,
    system_missing_count: int,
    declared_user_missing_metadata: Any = None,
) -> AllSystemColumnProjection:
    """Retain an all-system column as source information, without semantic inference."""
    return AllSystemColumnProjection(
        variable_name=variable_name,
        row_count=row_count,
        system_missing_count=system_missing_count,
        declared_user_missing_metadata=declared_user_missing_metadata,
    )


@dataclass(frozen=True)
class WeightCarrierProjection:
    variable_name: str
    documentary_label: str | None
    role_state: str = BOUNDED_UNKNOWN
    design_state: str = BOUNDED_UNKNOWN
    estimand_state: str = BOUNDED_UNKNOWN
    selected_by_default: bool = False

    def __post_init__(self) -> None:
        if self.variable_name not in WEIGHT_CARRIERS:
            raise WVS1RealizationError("unknown WVS1 weight carrier")
        if self.selected_by_default:
            raise WVS1RealizationError("WVS1 has no authorized default weight in the accepted packet")


def weight_surface() -> tuple[WeightCarrierProjection, ...]:
    """Return the exact 13-carrier surface; preserve all, select none."""
    return tuple(
        WeightCarrierProjection(
            variable_name=name,
            documentary_label=DOCUMENTED_WEIGHT_LABELS.get(name),
        )
        for name in WEIGHT_CARRIERS
    )


def authorize_weight_selection(
    carrier: str | None,
    *,
    authority: Mapping[str, Any] | None,
) -> str:
    """Permit a later selection only under explicit source-native role authority.

    The currently accepted WVS1 packet supplies no such default/estimand
    authority; callers must not use carrier presence as a substitute.
    """
    if carrier is None:
        raise WVS1RealizationError("no default WVS1 weight authority")
    if carrier not in WEIGHT_CARRIERS:
        raise WVS1RealizationError("weight carrier is not on the exact WVS1 surface")
    if not isinstance(authority, Mapping):
        raise WVS1RealizationError("explicit source-native weight-role authority required")
    if authority.get("status") != "EXPLICIT_SOURCE_NATIVE_WEIGHT_ROLE_AUTHORITY":
        raise WVS1RealizationError("explicit source-native weight-role authority required")
    if authority.get("carrier") != carrier:
        raise WVS1RealizationError("weight authority/carrier mismatch")
    return carrier


R35_HOOK_BINDING: Mapping[str, Any] = {
    "i01_physical_metadata": {
        "worker_branch": "agent/rabochii-premain-fiabc-r35-i01-raw-layout-metadata-r1",
        "schema": R35_PHYSICAL_METADATA_SCHEMA,
        "required": True,
        "wvs1_requirement": "RAW_STORAGE_AND_DISPLAY_METADATA_REMAIN_INDEPENDENT_WITNESSES",
        "semantic_authority": False,
    },
    "i02_derivative_parentage": {
        "worker_branch": "agent/rabochii-premain-fiabc-r35-i02-derivative-parentage-r1",
        "source_receipt_schema": R35_CANONICAL_SOURCE_RECEIPT_SCHEMA,
        "bundle_schema": R35_DERIVATIVE_PARENTAGE_BUNDLE_SCHEMA,
        "required_for_non_direct_raw": True,
        "semantic_authority": False,
    },
    "i03_whole_source_physical_equivalence": {
        "worker_branch": "agent/rabochii-premain-fiabc-r35-i03-physical-equivalence-r1",
        "source_scope_schema": R35_PHYSICAL_SCOPE_SCHEMA,
        "expectation_schema": R35_PHYSICAL_EXPECTATION_SCHEMA,
        "candidate_realization_schema": R35_PHYSICAL_REALIZATION_SCHEMA,
        "receipt_schema": R35_PHYSICAL_EQUIVALENCE_RECEIPT_SCHEMA,
        "applicable_edge_classes": APPLICABLE_EDGE_CLASSES,
        "required_physical_dimensions": R35_REQUIRED_PHYSICAL_DIMENSIONS,
        "pass_status": "PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS",
        "semantic_authority": False,
    },
}


def source_specific_realization_payload() -> Mapping[str, Any]:
    """Canonical candidate-neutral WVS1 source law."""
    return {
        "contract": CONTRACT_ID,
        "source": {
            "family": SOURCE_FAMILY,
            "release": SOURCE_RELEASE,
            "canonical_filename": CANONICAL_FILENAME,
            "canonical_sha256": CANONICAL_SHA256,
            "format": SOURCE_FORMAT,
            "decoder_mode": DECODER_MODE,
            "compatibility_status": COMPATIBILITY_STATUS,
            "compatibility_semantic_claim": COMPATIBILITY_SEMANTIC_CLAIM,
            "replay_identity": REPLAY_IDENTITY_LAW,
        },
        "native_identity": {
            "V3": BOUNDED_UNKNOWN,
            "S007": BOUNDED_UNKNOWN,
            "hard_replay_key": REPLAY_IDENTITY_LAW,
            "injectivity_does_not_mint_replay_authority": True,
        },
        "raw_display": {
            "S007_display_sentinel": S007_DISPLAY_FORMAT_SENTINEL,
            "law": "RAW_STORAGE_VALUE_AND_DISPLAY_METADATA_PRESERVED_SEPARATELY",
            "display_semantic_or_physical_value_authority": False,
        },
        "missingness": {
            "typed_physical_states_preserved": True,
            "semantic_response_refinement": BOUNDED_UNKNOWN,
            "routing_from_missingness": False,
        },
        "all_system_columns": {
            "accepted_packet_count": ACCEPTED_ALL_SYSTEM_COLUMN_COUNT,
            "named_sentinel": NAMED_ALL_SYSTEM_SENTINEL,
            "retention_required": True,
            "semantic_or_routing_meaning": BOUNDED_UNKNOWN,
        },
        "weights": {
            "carriers": WEIGHT_CARRIERS,
            "documented_labels": DOCUMENTED_WEIGHT_LABELS,
            "role_state": BOUNDED_UNKNOWN,
            "design_state": BOUNDED_UNKNOWN,
            "estimand_state": BOUNDED_UNKNOWN,
            "default_weight": None,
        },
        "routing": {
            "state_where_not_documentarily_closed": BOUNDED_UNKNOWN,
            "missingness_is_routing_authority": False,
        },
        "s35_edge_classes": APPLICABLE_EDGE_CLASSES,
        "r35_hooks": R35_HOOK_BINDING,
        "semantic_owner_surface": "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0",
        "candidate_law": "A_B_C_SHARE_ONE_WVS1_SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    }


SOURCE_SPECIFIC_REALIZATION_IDENTITY = canonical_digest(source_specific_realization_payload())


@dataclass(frozen=True)
class CandidateSemanticBinding:
    candidate_id: str
    source_sha256: str = CANONICAL_SHA256
    source_specific_realization_identity: str = SOURCE_SPECIFIC_REALIZATION_IDENTITY

    def __post_init__(self) -> None:
        if self.candidate_id not in {"A", "B", "C"}:
            raise WVS1RealizationError("candidate must be A, B or C")
        admit_source_identity(self.source_sha256)
        if self.source_specific_realization_identity != SOURCE_SPECIFIC_REALIZATION_IDENTITY:
            raise WVS1RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(bindings: Sequence[CandidateSemanticBinding]) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise WVS1RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise WVS1RealizationError("A/B/C source root divergence")
    if len({binding.source_specific_realization_identity for binding in bindings}) != 1:
        raise WVS1RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "ACCEPTED_ALL_SYSTEM_COLUMN_COUNT",
    "ALLOWED_PHYSICAL_STATES",
    "APPLICABLE_EDGE_CLASSES",
    "BOUNDED_UNKNOWN",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "CONTRACT_ID",
    "CandidateSemanticBinding",
    "DOCUMENTED_WEIGHT_LABELS",
    "NativeIdentityEvidence",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "RawDisplayProjection",
    "ReplayIdentity",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "S007_ACCEPTED_RAW_MAX",
    "S007_ACCEPTED_RAW_MIN",
    "S007_DISPLAY_FORMAT_SENTINEL",
    "S007_VARIABLE",
    "TypedMissingProjection",
    "WEIGHT_CARRIERS",
    "WeightCarrierProjection",
    "WVS1RealizationError",
    "admit_source_identity",
    "authorize_weight_selection",
    "canonical_digest",
    "preserve_all_system_column",
    "preserve_native_identity_evidence",
    "preserve_raw_display_separation",
    "preserve_typed_missingness",
    "replay_identity",
    "require_common_abc_semantic_law",
    "source_specific_realization_payload",
    "weight_surface",
]
