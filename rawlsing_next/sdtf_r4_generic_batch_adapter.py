"""Generic S03 batch-row adapter for the adopted SDTF R4 constructor.

This module implements only the frozen S03 generic batch envelope.  It does
not select current rules, resolve sources, mint authorities/refs/rule bodies,
or materialize actor/entity/topology state.  Fully resolved rows are projected
one-for-one into the already-adopted R4 constructor, which remains the final
validator of the projected mechanism-rule envelope.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.sdtf_r4_mechanism_rule_authority_binding import (
    CONTRACT_ID as R4_CONTRACT_ID,
    AuthorityCeilingBinding,
    AuthorityDisposition,
    AuthorityRole,
    MechanismRuleAuthorityBinding,
    MechanismRuleIdentity,
    R4MechanismRuleAuthorityBindingError,
    RuleCurrentness,
    RuleTraceBinding,
    RuleValueMode,
)

GENERIC_CONTRACT_ID = (
    "SDTF_R4_GENERIC_BATCH_RULE_ENVELOPE_INTAKE_AND_CONSTRUCTOR_CONTRACT_R1@1.0.0"
)
GENERIC_CONTRACT_REF = ExactRef(
    "SDTF_R4_GENERIC_BATCH_ENVELOPE_CONTRACT",
    GENERIC_CONTRACT_ID,
    "abc44b2b4ff04e164b5188e5929b0c10ca1b6e582b28207bb7e464ace698a83d",
)
ADOPTED_R4_IMPLEMENTATION_BLOB = "c94997f5c7f2bbee9cd99c570554fd48c0f47556"
CANDIDATE_ROW_KIND = "SDTF_R4_GENERIC_BATCH_CANDIDATE_ROW"
BATCH_KIND = "SDTF_R4_GENERIC_BATCH"
CANDIDATE_RECEIPT_KIND = "SDTF_R4_GENERIC_BATCH_CANDIDATE_RECEIPT"
BATCH_RECEIPT_KIND = "SDTF_R4_GENERIC_BATCH_ADAPTER_RECEIPT"

SATISFIED_CURRENT = "SATISFIED_CURRENT"
SATISFIED_CANDIDATE_ONLY = "SATISFIED_CANDIDATE_ONLY"
MISSING = "MISSING"
BLOCKED = "BLOCKED"
NOT_APPLICABLE = "NOT_APPLICABLE"
STATUS_STATES = frozenset(
    {SATISFIED_CURRENT, SATISFIED_CANDIDATE_ONLY, MISSING, BLOCKED, NOT_APPLICABLE}
)

NOT_PROJECTABLE = "NOT_PROJECTABLE"
READY_FOR_ADAPTER_PROJECTION = "READY_FOR_ADAPTER_PROJECTION"
ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT = "ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT"
ELIGIBLE_FOR_SEPARATE_CURRENT_SELECTION = "ELIGIBLE_FOR_SEPARATE_CURRENT_SELECTION"
HISTORICAL_NONCURRENT_VALIDATED = "HISTORICAL_NONCURRENT_VALIDATED"

NOT_REQUESTED = "NOT_REQUESTED"
SERIAL_GATE_BLOCKED = "SERIAL_GATE_BLOCKED"
ELIGIBLE_FOR_SEPARATE_SELECTION = "ELIGIBLE_FOR_SEPARATE_SELECTION"
SELECTION_EVIDENCE_PRESENT = "SELECTION_EVIDENCE_PRESENT"

MALFORMED_EXACT_REF = "MALFORMED_EXACT_REF"
MUTABLE_SELECTOR_FORBIDDEN = "MUTABLE_SELECTOR_FORBIDDEN"
SILENT_NA_FORBIDDEN = "SILENT_NA_FORBIDDEN"
ROLE_DISPOSITION_INVALID = "ROLE_DISPOSITION_INVALID"
VALUE_MODE_CALIBRATION_MISMATCH = "VALUE_MODE_CALIBRATION_MISMATCH"
CURRENTNESS_EVIDENCE_MISMATCH = "CURRENTNESS_EVIDENCE_MISMATCH"
ROW_IDENTITY_CONFLICT = "ROW_IDENTITY_CONFLICT"
PREDECESSOR_CHAIN_INVALID = "PREDECESSOR_CHAIN_INVALID"
CANDIDATE_BLOCKED = "CANDIDATE_BLOCKED"
FAIL_CLOSED_CODES = frozenset(
    {
        MALFORMED_EXACT_REF,
        MUTABLE_SELECTOR_FORBIDDEN,
        SILENT_NA_FORBIDDEN,
        ROLE_DISPOSITION_INVALID,
        VALUE_MODE_CALIBRATION_MISMATCH,
        CURRENTNESS_EVIDENCE_MISMATCH,
        ROW_IDENTITY_CONFLICT,
        PREDECESSOR_CHAIN_INVALID,
        CANDIDATE_BLOCKED,
    }
)

_FORBIDDEN_SELECTOR_TOKENS = frozenset(
    {"LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "SEMVER_FALLBACK", "*"}
)
_FORBIDDEN_SELECTOR_PREFIXES = ("LATEST:", "DEFAULT:", "FUZZY:", "NEAREST:", "SEMVER:")
_FORBIDDEN_VERSION_RANGE_CHARS = frozenset("*<>^~")

# Frozen one-to-one S03 determinant catalog.  No candidate-specific term or
# default is present here.
_DETERMINANTS = (
    (1, "GBE-R4-001", "rule_identity.rule_id", "PKG-A_RULE_IDENTITY_SHAPE_VALUE_CLASS", False),
    (2, "GBE-R4-002", "rule_identity.rule_version", "PKG-A_RULE_IDENTITY_SHAPE_VALUE_CLASS", False),
    (3, "GBE-R4-003", "rule_identity.rule_content_hash", "PKG-A_RULE_IDENTITY_SHAPE_VALUE_CLASS", False),
    (4, "GBE-R4-004", "mechanism_classes", "PKG-A_RULE_IDENTITY_SHAPE_VALUE_CLASS", False),
    (5, "GBE-R4-005", "constitution_current_selection_ref", "PKG-D_TRACE_EXACT_REF_LIFT", False),
    (6, "GBE-R4-006", "trace.source_refs", "PKG-D_TRACE_EXACT_REF_LIFT", False),
    (7, "GBE-R4-007", "trace.claim_refs", "PKG-D_TRACE_EXACT_REF_LIFT", False),
    (8, "GBE-R4-008", "trace.evidence_status_ref", "PKG-D_TRACE_EXACT_REF_LIFT", False),
    (9, "GBE-R4-009", "trace.normalized_mechanism_ref", "PKG-A_RULE_IDENTITY_SHAPE_VALUE_CLASS", False),
    (10, "GBE-R4-010", "trace.permitted_rule_shape_ref", "PKG-A_RULE_IDENTITY_SHAPE_VALUE_CLASS", False),
    (11, "GBE-R4-011", "trace.required_objective_inputs_bindings_ref", "PKG-D_TRACE_EXACT_REF_LIFT", False),
    (12, "GBE-R4-012", "trace.qualification_realization_proof_contract_ref", "PKG-E_QUALIFICATION_TEMPORAL_PORTABILITY", False),
    (13, "GBE-R4-013", "trace.temporal_currentness_contract_ref", "PKG-E_QUALIFICATION_TEMPORAL_PORTABILITY", False),
    (14, "GBE-R4-014", "trace.portability_ceiling_ref", "PKG-E_QUALIFICATION_TEMPORAL_PORTABILITY", False),
    (15, "GBE-R4-015", "trace.currentness_ceiling_ref", "PKG-D_TRACE_EXACT_REF_LIFT", False),
    (16, "GBE-R4-016", "trace.historical_institutional_validity_ref", "PKG-D_TRACE_EXACT_REF_LIFT", False),
    (17, "GBE-R4-017", "trace.negative_ceiling_ref", "PKG-D_TRACE_EXACT_REF_LIFT", False),
    (18, "GBE-R4-018", "trace.v3_stop_boundary_ref", "PKG-D_TRACE_EXACT_REF_LIFT", False),
    (19, "GBE-R4-019", "rule_owner", "PKG-B_MANDATORY_AUTHORITIES", False),
    (20, "GBE-R4-020", "measurement_authority", "PKG-C_AUXILIARY_AUTHORITY_DISPOSITIONS", True),
    (21, "GBE-R4-021", "estimand_authority", "PKG-C_AUXILIARY_AUTHORITY_DISPOSITIONS", True),
    (22, "GBE-R4-022", "identification_authority", "PKG-C_AUXILIARY_AUTHORITY_DISPOSITIONS", True),
    (23, "GBE-R4-023", "causal_use_authority", "PKG-B_MANDATORY_AUTHORITIES", False),
    (24, "GBE-R4-024", "calibration_authority", "PKG-C_AUXILIARY_AUTHORITY_DISPOSITIONS", True),
    (25, "GBE-R4-025", "value_mode", "PKG-A_RULE_IDENTITY_SHAPE_VALUE_CLASS", False),
    (26, "GBE-R4-026", "rule_currentness", "PKG-F_RULE_CURRENTNESS_SELECTION", False),
    (27, "GBE-R4-027", "rule_current_selection_evidence_refs", "PKG-F_RULE_CURRENTNESS_SELECTION", True),
    (28, "GBE-R4-028", "rule_noncurrent_disposition_refs", "PKG-F_RULE_CURRENTNESS_SELECTION", True),
)
DETERMINANT_IDS = tuple(item[1] for item in _DETERMINANTS)
FIELD_PATHS = tuple(item[2] for item in _DETERMINANTS)

PACKAGE_PARTITION = (
    ("PKG-A_RULE_IDENTITY_SHAPE_VALUE_CLASS", (1, 2, 3, 4, 9, 10, 25)),
    ("PKG-B_MANDATORY_AUTHORITIES", (19, 23)),
    ("PKG-C_AUXILIARY_AUTHORITY_DISPOSITIONS", (20, 21, 22, 24)),
    ("PKG-D_TRACE_EXACT_REF_LIFT", (5, 6, 7, 8, 11, 15, 16, 17, 18)),
    ("PKG-E_QUALIFICATION_TEMPORAL_PORTABILITY", (12, 13, 14)),
    ("PKG-F_RULE_CURRENTNESS_SELECTION", (26, 27, 28)),
)
_PACKAGE_BY_ORDINAL = {ordinal: package for ordinal, _, _, package, _ in _DETERMINANTS}
_NA_PERMITTED = {ordinal: allowed for ordinal, _, _, _, allowed in _DETERMINANTS}
_ROLE_BY_ORDINAL = {
    19: AuthorityRole.RULE_OWNER,
    20: AuthorityRole.MEASUREMENT,
    21: AuthorityRole.ESTIMAND,
    22: AuthorityRole.IDENTIFICATION,
    23: AuthorityRole.CAUSAL_USE,
    24: AuthorityRole.CALIBRATION,
}


class GenericR4BatchAdapterError(ValueError):
    """The S03 batch boundary itself is malformed or contract-mismatched."""


@dataclass(frozen=True, slots=True)
class _Cell:
    determinant_id: str
    state: str
    resolved_value: Any
    candidate_material_refs: tuple[ExactRef, ...]
    blocker_refs: tuple[ExactRef, ...]
    na_basis_ref: ExactRef | None
    basis_text: str | None

    def governed_material(self) -> Mapping[str, Any]:
        # basis_text is free-text diagnostics and is explicitly excluded from
        # candidate-row governed identity material by S03.
        return {
            "determinant_id": self.determinant_id,
            "state": self.state,
            "resolved_value": self.resolved_value,
            "candidate_material_refs": [r.as_dict() for r in self.candidate_material_refs],
            "blocker_refs": [r.as_dict() for r in self.blocker_refs],
            "na_basis_ref": None if self.na_basis_ref is None else self.na_basis_ref.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class CandidateAdapterReceipt:
    contract_ref: ExactRef
    batch_ref: ExactRef
    candidate_row_ref: ExactRef
    determinant_states: tuple[tuple[str, str], ...]
    package_states: tuple[tuple[str, str], ...]
    integrity_failures: tuple[str, ...]
    blocking_refs: tuple[ExactRef, ...]
    runtime_projection_state: str
    runtime_binding_ref: ExactRef | None
    current_selection_state: str
    receipt_predecessor_ref: ExactRef | None = None
    diagnostics: tuple[str, ...] = field(default=(), compare=False, repr=False)
    runtime_binding: MechanismRuleAuthorityBinding | None = field(
        default=None, compare=False, repr=False
    )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_ref": self.contract_ref.as_dict(),
            "batch_ref": self.batch_ref.as_dict(),
            "candidate_row_ref": self.candidate_row_ref.as_dict(),
            "determinant_states": [
                {"determinant_id": determinant_id, "state": state}
                for determinant_id, state in self.determinant_states
            ],
            "package_states": [
                {"package_id": package_id, "state": state}
                for package_id, state in self.package_states
            ],
            "integrity_failures": list(self.integrity_failures),
            "blocking_refs": [ref.as_dict() for ref in self.blocking_refs],
            "runtime_projection_state": self.runtime_projection_state,
            "runtime_binding_ref": (
                None if self.runtime_binding_ref is None else self.runtime_binding_ref.as_dict()
            ),
            "current_selection_state": self.current_selection_state,
            "receipt_predecessor_ref": (
                None
                if self.receipt_predecessor_ref is None
                else self.receipt_predecessor_ref.as_dict()
            ),
        }

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            CANDIDATE_RECEIPT_KIND,
            self.candidate_row_ref.object_id,
            semantic_hash(self.as_material()),
        )


@dataclass(frozen=True, slots=True)
class GenericR4BatchAdapterResult:
    contract_ref: ExactRef
    batch_ref: ExactRef
    candidate_receipts: tuple[CandidateAdapterReceipt, ...]

    @property
    def batch_receipt_material(self) -> Mapping[str, Any]:
        return {
            "contract_ref": self.contract_ref.as_dict(),
            "batch_ref": self.batch_ref.as_dict(),
            "candidate_receipt_refs": [
                receipt.ref.as_dict() for receipt in self.candidate_receipts
            ],
            "row_count": len(self.candidate_receipts),
            "projected_count": sum(
                receipt.runtime_binding_ref is not None
                for receipt in self.candidate_receipts
            ),
        }

    @property
    def batch_receipt_ref(self) -> ExactRef:
        return ExactRef(
            BATCH_RECEIPT_KIND,
            self.batch_ref.object_id,
            semantic_hash(self.batch_receipt_material),
        )

    def as_material(self) -> Mapping[str, Any]:
        return {
            **self.batch_receipt_material,
            "batch_receipt_ref": self.batch_receipt_ref.as_dict(),
            "candidate_receipts": [r.as_material() for r in self.candidate_receipts],
        }


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GenericR4BatchAdapterError(f"{name} must be non-empty exact text")
    return value.strip()


def _reject_selector(value: Any, name: str, *, version: bool = False) -> str:
    text = _text(value, name)
    upper = text.upper()
    if upper in _FORBIDDEN_SELECTOR_TOKENS or upper.startswith(_FORBIDDEN_SELECTOR_PREFIXES):
        raise GenericR4BatchAdapterError(
            f"{MUTABLE_SELECTOR_FORBIDDEN}: {name} may not use mutable selector syntax"
        )
    if version and any(ch in text for ch in _FORBIDDEN_VERSION_RANGE_CHARS):
        raise GenericR4BatchAdapterError(
            f"{MUTABLE_SELECTOR_FORBIDDEN}: {name} may not use range/wildcard syntax"
        )
    return text


def _ref(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except (Pre553IntegrityError, ValueError, TypeError) as exc:
        raise GenericR4BatchAdapterError(f"{MALFORMED_EXACT_REF}: {name}: {exc}") from exc


def _refs(
    value: Any,
    name: str,
    *,
    allow_empty: bool = True,
    deduplicate_exact: bool = False,
) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Iterable):
        raise GenericR4BatchAdapterError(f"{MALFORMED_EXACT_REF}: {name} must be a ref list")
    refs = tuple(_ref(item, f"{name}[]") for item in value)
    if not allow_empty and not refs:
        raise GenericR4BatchAdapterError(f"{MALFORMED_EXACT_REF}: {name} must not be empty")
    by_key: dict[str, ExactRef] = {}
    for item in refs:
        if item.key in by_key and not deduplicate_exact:
            raise GenericR4BatchAdapterError(
                f"{MALFORMED_EXACT_REF}: {name} contains duplicate exact refs"
            )
        by_key[item.key] = item
    return tuple(by_key[key] for key in sorted(by_key))


def _authority_ref(value: Any, name: str) -> AuthorityRef:
    try:
        return authority_ref(value, name)
    except (Pre553IntegrityError, ValueError, TypeError) as exc:
        raise GenericR4BatchAdapterError(f"{MALFORMED_EXACT_REF}: {name}: {exc}") from exc


def _exact_contract_ref(value: Any) -> ExactRef:
    ref = _ref(value, "contract_ref")
    if ref != GENERIC_CONTRACT_REF:
        raise GenericR4BatchAdapterError(
            "contract_ref must equal the exact frozen S03 generic contract; mutable, "
            "substitute, or mismatched contract selectors are forbidden"
        )
    return ref


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise GenericR4BatchAdapterError(f"{name} must be a mapping")
    return value


def _row_parts(row: Mapping[str, Any]) -> tuple[
    ExactRef,
    str,
    str,
    int,
    ExactRef | None,
    Sequence[Any],
    tuple[ExactRef, ...],
]:
    contract_ref = _exact_contract_ref(row.get("contract_ref"))
    key = row.get("key")
    if key is None:
        key = {
            "candidate_namespace": row.get("candidate_namespace"),
            "candidate_id": row.get("candidate_id"),
        }
    key = _mapping(key, "candidate row key")
    if set(key) != {"candidate_namespace", "candidate_id"}:
        raise GenericR4BatchAdapterError(
            "candidate row key must contain candidate_namespace/candidate_id only"
        )
    namespace = _reject_selector(key["candidate_namespace"], "candidate_namespace")
    candidate_id = _reject_selector(key["candidate_id"], "candidate_id")

    snapshot = row.get("snapshot")
    if snapshot is None:
        snapshot = {
            "row_generation": row.get("row_generation"),
            "predecessor_row_ref": row.get("predecessor_row_ref"),
            "requirement_cells": row.get("requirement_cells"),
            "provenance_refs": row.get("provenance_refs"),
        }
    snapshot = _mapping(snapshot, "candidate row snapshot")
    required_snapshot_keys = {
        "row_generation",
        "predecessor_row_ref",
        "requirement_cells",
        "provenance_refs",
    }
    if set(snapshot) != required_snapshot_keys:
        raise GenericR4BatchAdapterError(
            "candidate row snapshot must contain row_generation/predecessor_row_ref/"
            "requirement_cells/provenance_refs only"
        )
    generation = snapshot["row_generation"]
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 0:
        raise GenericR4BatchAdapterError("row_generation must be a nonnegative int")
    predecessor_raw = snapshot["predecessor_row_ref"]
    predecessor = None if predecessor_raw is None else _ref(predecessor_raw, "predecessor_row_ref")
    cells = snapshot["requirement_cells"]
    if not isinstance(cells, Sequence) or isinstance(cells, (str, bytes, bytearray)):
        raise GenericR4BatchAdapterError("requirement_cells must be an exact ordered sequence")
    provenance = _refs(snapshot["provenance_refs"], "provenance_refs")

    row_ref_raw = row.get("ref", row.get("candidate_row_ref"))
    row_ref = _ref(row_ref_raw, "candidate_row_ref")
    return contract_ref, namespace, candidate_id, generation, predecessor, cells, provenance, row_ref


def _parse_cell(raw: Any, ordinal: int) -> _Cell:
    raw = _mapping(raw, f"requirement_cells[{ordinal - 1}]")
    expected_keys = {
        "determinant_id",
        "state",
        "resolved_value",
        "candidate_material_refs",
        "blocker_refs",
        "na_basis_ref",
        "basis_text",
    }
    if set(raw) != expected_keys:
        raise GenericR4BatchAdapterError(
            f"requirement cell {ordinal} must carry the exact S03 status-cell shape"
        )
    determinant_id = raw["determinant_id"]
    expected_id = DETERMINANT_IDS[ordinal - 1]
    if determinant_id != expected_id:
        raise GenericR4BatchAdapterError(
            f"determinant ordinal {ordinal} must be {expected_id}, got {determinant_id!r}"
        )
    state = raw["state"]
    if state not in STATUS_STATES:
        raise GenericR4BatchAdapterError(f"unknown S03 cell state for {determinant_id}: {state!r}")
    candidate_refs = _refs(raw["candidate_material_refs"], f"{determinant_id}.candidate_material_refs")
    blocker_refs = _refs(raw["blocker_refs"], f"{determinant_id}.blocker_refs")
    na_basis = None if raw["na_basis_ref"] is None else _ref(raw["na_basis_ref"], f"{determinant_id}.na_basis_ref")
    basis_text = raw["basis_text"]
    if basis_text is not None and not isinstance(basis_text, str):
        raise GenericR4BatchAdapterError(f"{determinant_id}.basis_text must be text or null")
    resolved = raw["resolved_value"]

    if state == SATISFIED_CURRENT:
        if resolved is None:
            raise GenericR4BatchAdapterError(f"{determinant_id}: SATISFIED_CURRENT requires resolved_value")
        if blocker_refs or na_basis is not None:
            raise GenericR4BatchAdapterError(f"{determinant_id}: SATISFIED_CURRENT forbids blocker/N-A basis")
    elif state == SATISFIED_CANDIDATE_ONLY:
        if not candidate_refs or blocker_refs:
            raise GenericR4BatchAdapterError(
                f"{determinant_id}: SATISFIED_CANDIDATE_ONLY requires candidate refs and no blockers"
            )
        if na_basis is not None:
            raise GenericR4BatchAdapterError(f"{determinant_id}: candidate-only may not carry N/A basis")
    elif state == MISSING:
        if resolved is not None or blocker_refs or na_basis is not None:
            raise GenericR4BatchAdapterError(
                f"{determinant_id}: MISSING may not carry resolved value, blockers, or N/A basis"
            )
    elif state == BLOCKED:
        if resolved is not None or not blocker_refs or na_basis is not None:
            raise GenericR4BatchAdapterError(
                f"{determinant_id}: BLOCKED requires blocker refs and no resolved value/N-A basis"
            )
    else:
        if not _NA_PERMITTED[ordinal]:
            raise GenericR4BatchAdapterError(f"{SILENT_NA_FORBIDDEN}: {determinant_id} cannot be N/A")
        if resolved is not None or blocker_refs:
            raise GenericR4BatchAdapterError(
                f"{determinant_id}: NOT_APPLICABLE carries no resolved value or blockers"
            )
        if ordinal in _ROLE_BY_ORDINAL and na_basis is None:
            raise GenericR4BatchAdapterError(
                f"{SILENT_NA_FORBIDDEN}: authority N/A requires exact na_basis_ref"
            )
    return _Cell(
        determinant_id,
        state,
        resolved,
        candidate_refs,
        blocker_refs,
        na_basis,
        basis_text,
    )


def _compute_row_ref(
    contract_ref: ExactRef,
    namespace: str,
    candidate_id: str,
    generation: int,
    predecessor: ExactRef | None,
    cells: Sequence[_Cell],
    provenance: Sequence[ExactRef],
) -> ExactRef:
    identity_material = {
        "contract_ref": contract_ref.as_dict(),
        "key": {"candidate_namespace": namespace, "candidate_id": candidate_id},
        "row_generation": generation,
        "predecessor_row_ref": None if predecessor is None else predecessor.as_dict(),
        "requirement_cells": [cell.governed_material() for cell in cells],
        "provenance_refs": [ref.as_dict() for ref in provenance],
    }
    return ExactRef(
        CANDIDATE_ROW_KIND,
        f"{namespace}:{candidate_id}:g{generation}",
        semantic_hash(identity_material),
    )


def _parse_exact_ref_value(value: Any, name: str) -> ExactRef:
    return _ref(value, name)


def _parse_exact_ref_list_value(value: Any, name: str, *, nonempty: bool = False) -> tuple[ExactRef, ...]:
    return _refs(value, name, allow_empty=not nonempty)


def _parse_authority_binding(value: Any, role: AuthorityRole, name: str) -> AuthorityCeilingBinding:
    value = _mapping(value, name)
    keys = {
        "role",
        "disposition",
        "scope_or_na_ref",
        "authority_ref",
        "current_selection_evidence_refs",
    }
    if set(value) != keys:
        raise GenericR4BatchAdapterError(f"{name} must carry exact AuthorityCeilingBinding fields")
    if value["role"] != role.value:
        raise GenericR4BatchAdapterError(f"{ROLE_DISPOSITION_INVALID}: {name} role mismatch")
    if value["disposition"] != AuthorityDisposition.BOUND.value:
        raise GenericR4BatchAdapterError(
            f"{ROLE_DISPOSITION_INVALID}: SATISFIED_CURRENT authority must be BOUND"
        )
    try:
        return AuthorityCeilingBinding(
            role=role,
            disposition=AuthorityDisposition.BOUND,
            scope_or_na_ref=_ref(value["scope_or_na_ref"], f"{name}.scope_or_na_ref"),
            authority_ref=_authority_ref(value["authority_ref"], f"{name}.authority_ref"),
            current_selection_evidence_refs=_refs(
                value["current_selection_evidence_refs"],
                f"{name}.current_selection_evidence_refs",
                allow_empty=False,
            ),
        )
    except R4MechanismRuleAuthorityBindingError as exc:
        raise GenericR4BatchAdapterError(f"{ROLE_DISPOSITION_INVALID}: {name}: {exc}") from exc


def _parse_na_authority(cell: _Cell, role: AuthorityRole, name: str) -> AuthorityCeilingBinding:
    if cell.na_basis_ref is None:
        raise GenericR4BatchAdapterError(f"{SILENT_NA_FORBIDDEN}: {name} lacks N/A basis")
    try:
        return AuthorityCeilingBinding(
            role=role,
            disposition=AuthorityDisposition.NOT_APPLICABLE,
            scope_or_na_ref=cell.na_basis_ref,
            authority_ref=None,
            current_selection_evidence_refs=(),
        )
    except R4MechanismRuleAuthorityBindingError as exc:
        raise GenericR4BatchAdapterError(f"{ROLE_DISPOSITION_INVALID}: {name}: {exc}") from exc


def _map_r4_error(exc: Exception) -> str:
    text = str(exc).lower()
    if "selector" in text or "version range" in text or "wildcard" in text:
        return MUTABLE_SELECTOR_FORBIDDEN
    if "calibration" in text or "nonnumeric" in text or "numeric rule" in text:
        return VALUE_MODE_CALIBRATION_MISMATCH
    if "current-selection" in text or "currentness" in text or "historical" in text:
        return CURRENTNESS_EVIDENCE_MISMATCH
    if "authority" in text or "role" in text or "not_applicable" in text:
        return ROLE_DISPOSITION_INVALID
    if "exactref" in text or "sha256" in text or "exact ref" in text:
        return MALFORMED_EXACT_REF
    return CANDIDATE_BLOCKED


def _effective_ref_tuple(cell: _Cell, name: str) -> tuple[ExactRef, ...]:
    if cell.state == NOT_APPLICABLE:
        return ()
    return _parse_exact_ref_list_value(cell.resolved_value, name)


def _project(cells: Sequence[_Cell]) -> MechanismRuleAuthorityBinding:
    by_ordinal = {index: cell for index, cell in enumerate(cells, start=1)}
    # Only current/exact or explicit lawful N/A cells may cross the runtime boundary.
    for ordinal, cell in by_ordinal.items():
        if cell.state not in {SATISFIED_CURRENT, NOT_APPLICABLE}:
            raise GenericR4BatchAdapterError(
                f"{CANDIDATE_BLOCKED}: {cell.determinant_id} is not runtime-projectable"
            )
        if cell.state == NOT_APPLICABLE and not _NA_PERMITTED[ordinal]:
            raise GenericR4BatchAdapterError(
                f"{SILENT_NA_FORBIDDEN}: {cell.determinant_id} cannot be N/A"
            )

    rule_id = _reject_selector(by_ordinal[1].resolved_value, "rule_identity.rule_id")
    rule_version = _reject_selector(
        by_ordinal[2].resolved_value,
        "rule_identity.rule_version",
        version=True,
    )
    identity = MechanismRuleIdentity(rule_id, rule_version, by_ordinal[3].resolved_value)

    mechanism_classes_raw = by_ordinal[4].resolved_value
    if not isinstance(mechanism_classes_raw, Sequence) or isinstance(
        mechanism_classes_raw, (str, bytes, bytearray)
    ):
        raise GenericR4BatchAdapterError("mechanism_classes must be an exact class list")

    trace = RuleTraceBinding(
        source_refs=_parse_exact_ref_list_value(by_ordinal[6].resolved_value, "trace.source_refs", nonempty=True),
        claim_refs=_parse_exact_ref_list_value(by_ordinal[7].resolved_value, "trace.claim_refs", nonempty=True),
        evidence_status_ref=_parse_exact_ref_value(by_ordinal[8].resolved_value, "trace.evidence_status_ref"),
        normalized_mechanism_ref=_parse_exact_ref_value(by_ordinal[9].resolved_value, "trace.normalized_mechanism_ref"),
        permitted_rule_shape_ref=_parse_exact_ref_value(by_ordinal[10].resolved_value, "trace.permitted_rule_shape_ref"),
        required_objective_inputs_bindings_ref=_parse_exact_ref_value(by_ordinal[11].resolved_value, "trace.required_objective_inputs_bindings_ref"),
        qualification_realization_proof_contract_ref=_parse_exact_ref_value(by_ordinal[12].resolved_value, "trace.qualification_realization_proof_contract_ref"),
        temporal_currentness_contract_ref=_parse_exact_ref_value(by_ordinal[13].resolved_value, "trace.temporal_currentness_contract_ref"),
        portability_ceiling_ref=_parse_exact_ref_value(by_ordinal[14].resolved_value, "trace.portability_ceiling_ref"),
        currentness_ceiling_ref=_parse_exact_ref_value(by_ordinal[15].resolved_value, "trace.currentness_ceiling_ref"),
        historical_institutional_validity_ref=_parse_exact_ref_value(by_ordinal[16].resolved_value, "trace.historical_institutional_validity_ref"),
        negative_ceiling_ref=_parse_exact_ref_value(by_ordinal[17].resolved_value, "trace.negative_ceiling_ref"),
        v3_stop_boundary_ref=_parse_exact_ref_value(by_ordinal[18].resolved_value, "trace.v3_stop_boundary_ref"),
    )

    authorities: dict[int, AuthorityCeilingBinding] = {}
    for ordinal, role in _ROLE_BY_ORDINAL.items():
        cell = by_ordinal[ordinal]
        if cell.state == NOT_APPLICABLE:
            if role in {AuthorityRole.RULE_OWNER, AuthorityRole.CAUSAL_USE}:
                raise GenericR4BatchAdapterError(
                    f"{ROLE_DISPOSITION_INVALID}: {role.value} must be BOUND"
                )
            authorities[ordinal] = _parse_na_authority(cell, role, FIELD_PATHS[ordinal - 1])
        else:
            authorities[ordinal] = _parse_authority_binding(
                cell.resolved_value, role, FIELD_PATHS[ordinal - 1]
            )

    try:
        value_mode = RuleValueMode(by_ordinal[25].resolved_value)
        currentness = RuleCurrentness(by_ordinal[26].resolved_value)
    except (TypeError, ValueError) as exc:
        raise GenericR4BatchAdapterError(str(exc)) from exc

    if value_mode is RuleValueMode.NUMERIC and by_ordinal[24].state != SATISFIED_CURRENT:
        raise GenericR4BatchAdapterError(
            f"{VALUE_MODE_CALIBRATION_MISMATCH}: NUMERIC requires CALIBRATION BOUND"
        )
    if value_mode is RuleValueMode.NONNUMERIC and by_ordinal[24].state != NOT_APPLICABLE:
        raise GenericR4BatchAdapterError(
            f"{VALUE_MODE_CALIBRATION_MISMATCH}: NONNUMERIC requires explicit CALIBRATION N/A"
        )

    current_refs = _effective_ref_tuple(
        by_ordinal[27], "rule_current_selection_evidence_refs"
    )
    noncurrent_refs = _effective_ref_tuple(
        by_ordinal[28], "rule_noncurrent_disposition_refs"
    )
    if currentness is RuleCurrentness.CANDIDATE_NOT_CURRENT:
        if current_refs or noncurrent_refs:
            raise GenericR4BatchAdapterError(
                f"{CURRENTNESS_EVIDENCE_MISMATCH}: candidate-not-current rows 27/28 must be empty"
            )
    elif currentness is RuleCurrentness.CURRENT_ACCEPTED:
        if not current_refs or noncurrent_refs:
            raise GenericR4BatchAdapterError(
                f"{CURRENTNESS_EVIDENCE_MISMATCH}: current-accepted requires row 27 only"
            )
    elif not current_refs or not noncurrent_refs:
        raise GenericR4BatchAdapterError(
            f"{CURRENTNESS_EVIDENCE_MISMATCH}: historical noncurrent requires rows 27 and 28"
        )

    return MechanismRuleAuthorityBinding(
        rule_identity=identity,
        mechanism_classes=tuple(mechanism_classes_raw),
        constitution_current_selection_ref=_parse_exact_ref_value(
            by_ordinal[5].resolved_value, "constitution_current_selection_ref"
        ),
        trace=trace,
        rule_owner=authorities[19],
        measurement_authority=authorities[20],
        estimand_authority=authorities[21],
        identification_authority=authorities[22],
        causal_use_authority=authorities[23],
        calibration_authority=authorities[24],
        value_mode=value_mode,
        rule_currentness=currentness,
        rule_current_selection_evidence_refs=current_refs,
        rule_noncurrent_disposition_refs=noncurrent_refs,
    )


def _package_states(cells: Sequence[_Cell]) -> tuple[tuple[str, str], ...]:
    by_ordinal = {index: cell for index, cell in enumerate(cells, start=1)}
    states: list[tuple[str, str]] = []
    for package_id, ordinals in PACKAGE_PARTITION:
        package_cell_states = [by_ordinal[o].state for o in ordinals]
        if BLOCKED in package_cell_states:
            state = BLOCKED
        elif MISSING in package_cell_states:
            state = MISSING
        elif SATISFIED_CANDIDATE_ONLY in package_cell_states:
            state = SATISFIED_CANDIDATE_ONLY
        else:
            # Explicit N/A is a closed determinant, not missing.
            state = SATISFIED_CURRENT
        states.append((package_id, state))
    return tuple(states)


def _failure_order(codes: Iterable[str]) -> tuple[str, ...]:
    order = (
        MALFORMED_EXACT_REF,
        MUTABLE_SELECTOR_FORBIDDEN,
        SILENT_NA_FORBIDDEN,
        ROLE_DISPOSITION_INVALID,
        VALUE_MODE_CALIBRATION_MISMATCH,
        CURRENTNESS_EVIDENCE_MISMATCH,
        ROW_IDENTITY_CONFLICT,
        PREDECESSOR_CHAIN_INVALID,
        CANDIDATE_BLOCKED,
    )
    present = set(codes)
    return tuple(code for code in order if code in present)


def _code_from_adapter_error(exc: Exception) -> str:
    text = str(exc)
    for code in FAIL_CLOSED_CODES:
        if code in text:
            return code
    return _map_r4_error(exc)


def _current_selection_state(cells: Sequence[_Cell], failures: Sequence[str]) -> str:
    if failures or any(cell.state in {MISSING, BLOCKED, SATISFIED_CANDIDATE_ONLY} for cell in cells):
        return SERIAL_GATE_BLOCKED
    currentness = cells[25].resolved_value
    if currentness == RuleCurrentness.CANDIDATE_NOT_CURRENT.value:
        return ELIGIBLE_FOR_SEPARATE_SELECTION
    if currentness in {
        RuleCurrentness.CURRENT_ACCEPTED.value,
        RuleCurrentness.HISTORICAL_NONCURRENT.value,
    }:
        return SELECTION_EVIDENCE_PRESENT
    return NOT_REQUESTED


def _validate_lineage(
    namespace: str,
    candidate_id: str,
    generation: int,
    predecessor: ExactRef | None,
) -> tuple[str, ...]:
    if generation == 0:
        return () if predecessor is None else (PREDECESSOR_CHAIN_INVALID,)
    if predecessor is None:
        return (PREDECESSOR_CHAIN_INVALID,)
    expected_object_id = f"{namespace}:{candidate_id}:g{generation - 1}"
    if predecessor.kind != CANDIDATE_ROW_KIND or predecessor.object_id != expected_object_id:
        return (PREDECESSOR_CHAIN_INVALID,)
    return ()


def _make_candidate_receipt(
    *,
    batch_ref: ExactRef,
    row_ref: ExactRef,
    cells: Sequence[_Cell],
    failures: Iterable[str],
    diagnostics: Iterable[str],
) -> CandidateAdapterReceipt:
    failures_list = list(failures)
    blocking_refs = tuple(
        sorted(
            {ref for cell in cells for ref in cell.blocker_refs},
            key=lambda ref: ref.key,
        )
    )
    if any(cell.state == BLOCKED for cell in cells):
        failures_list.append(CANDIDATE_BLOCKED)
    failures_tuple = _failure_order(failures_list)
    runtime_binding: MechanismRuleAuthorityBinding | None = None
    runtime_binding_ref: ExactRef | None = None
    projection_state = NOT_PROJECTABLE

    if not failures_tuple and all(
        cell.state in {SATISFIED_CURRENT, NOT_APPLICABLE} for cell in cells
    ):
        projection_state = READY_FOR_ADAPTER_PROJECTION
        try:
            runtime_binding = _project(cells)
            runtime_binding_ref = runtime_binding.ref
            if runtime_binding.rule_currentness is RuleCurrentness.CANDIDATE_NOT_CURRENT:
                projection_state = ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT
            elif runtime_binding.rule_currentness is RuleCurrentness.HISTORICAL_NONCURRENT:
                projection_state = HISTORICAL_NONCURRENT_VALIDATED
            else:
                # The adapter validates already-supplied selection evidence but does
                # not itself issue or choose CURRENT_ACCEPTED.
                projection_state = ELIGIBLE_FOR_SEPARATE_CURRENT_SELECTION
        except (GenericR4BatchAdapterError, R4MechanismRuleAuthorityBindingError) as exc:
            failures_tuple = _failure_order((*failures_tuple, _code_from_adapter_error(exc)))
            diagnostics = (*tuple(diagnostics), str(exc))
            runtime_binding = None
            runtime_binding_ref = None
            projection_state = NOT_PROJECTABLE

    return CandidateAdapterReceipt(
        contract_ref=GENERIC_CONTRACT_REF,
        batch_ref=batch_ref,
        candidate_row_ref=row_ref,
        determinant_states=tuple((cell.determinant_id, cell.state) for cell in cells),
        package_states=_package_states(cells),
        integrity_failures=failures_tuple,
        blocking_refs=blocking_refs,
        runtime_projection_state=projection_state,
        runtime_binding_ref=runtime_binding_ref,
        current_selection_state=_current_selection_state(cells, failures_tuple),
        receipt_predecessor_ref=None,
        diagnostics=tuple(diagnostics),
        runtime_binding=runtime_binding,
    )


def _batch_ref(
    batch_namespace: str,
    batch_id: str,
    row_refs: Sequence[ExactRef],
    provenance_refs: Sequence[ExactRef],
) -> ExactRef:
    material = {
        "contract_ref": GENERIC_CONTRACT_REF.as_dict(),
        "batch_namespace": batch_namespace,
        "batch_id": batch_id,
        "candidate_row_refs": [ref.as_dict() for ref in sorted(set(row_refs), key=lambda r: r.key)],
        "batch_provenance_refs": [ref.as_dict() for ref in sorted(set(provenance_refs), key=lambda r: r.key)],
    }
    return ExactRef(BATCH_KIND, f"{batch_namespace}:{batch_id}", semantic_hash(material))


def adapt_generic_r4_batch(envelope: Mapping[str, Any]) -> GenericR4BatchAdapterResult:
    """Validate one S03 batch and project each independently-ready row into R4.

    The top-level envelope carries the frozen ``contract_ref``, exact batch
    namespace/id, row bodies in ``candidate_rows``, the corresponding
    ``candidate_row_refs`` (exact duplicates permitted), and exact batch
    provenance refs.  Row order and duplicate presentation are nonsemantic.

    Boundary-shape/contract errors raise :class:`GenericR4BatchAdapterError`.
    Governed row failures are quarantined into that row's deterministic receipt
    and never prevent an unrelated valid row from being processed.
    """
    envelope = _mapping(envelope, "batch envelope")
    required = {
        "contract_ref",
        "batch_namespace",
        "batch_id",
        "candidate_rows",
        "candidate_row_refs",
        "batch_provenance_refs",
    }
    optional = {"ref", "batch_ref"}
    if not required.issubset(envelope) or set(envelope) - required - optional:
        raise GenericR4BatchAdapterError(
            "batch envelope must carry exact S03 contract/header/rows/ref-list/provenance fields"
        )
    _exact_contract_ref(envelope["contract_ref"])
    batch_namespace = _reject_selector(envelope["batch_namespace"], "batch_namespace")
    batch_id = _reject_selector(envelope["batch_id"], "batch_id")
    batch_provenance = _refs(envelope["batch_provenance_refs"], "batch_provenance_refs")
    declared_row_refs = _refs(
        envelope["candidate_row_refs"],
        "candidate_row_refs",
        deduplicate_exact=True,
    )
    raw_rows = envelope["candidate_rows"]
    if not isinstance(raw_rows, Sequence) or isinstance(raw_rows, (str, bytes, bytearray)):
        raise GenericR4BatchAdapterError("candidate_rows must be a sequence")

    parsed: list[dict[str, Any]] = []
    for raw_row in raw_rows:
        row = _mapping(raw_row, "candidate row")
        (
            contract_ref,
            namespace,
            candidate_id,
            generation,
            predecessor,
            raw_cells,
            provenance,
            supplied_row_ref,
        ) = _row_parts(row)
        if contract_ref != GENERIC_CONTRACT_REF:
            raise GenericR4BatchAdapterError("candidate row contract mismatch")
        if len(raw_cells) != 28:
            raise GenericR4BatchAdapterError("candidate row must carry exactly 28 requirement cells")
        cells = tuple(_parse_cell(raw, ordinal) for ordinal, raw in enumerate(raw_cells, start=1))
        computed_row_ref = _compute_row_ref(
            contract_ref,
            namespace,
            candidate_id,
            generation,
            predecessor,
            cells,
            provenance,
        )
        failures: list[str] = list(
            _validate_lineage(namespace, candidate_id, generation, predecessor)
        )
        diagnostics: list[str] = []
        if supplied_row_ref.kind != CANDIDATE_ROW_KIND:
            failures.append(MALFORMED_EXACT_REF)
            diagnostics.append("candidate_row_ref kind mismatch")
        if supplied_row_ref.object_id != computed_row_ref.object_id:
            failures.append(ROW_IDENTITY_CONFLICT)
            diagnostics.append("candidate_row_ref object_id does not match candidate key/generation")
        if supplied_row_ref.content_hash != computed_row_ref.content_hash:
            failures.append(ROW_IDENTITY_CONFLICT)
            diagnostics.append("candidate_row_ref content hash does not match governed row material")
        parsed.append(
            {
                "namespace": namespace,
                "candidate_id": candidate_id,
                "generation": generation,
                "predecessor": predecessor,
                "cells": cells,
                "supplied_ref": supplied_row_ref,
                "computed_ref": computed_row_ref,
                "failures": failures,
                "diagnostics": diagnostics,
            }
        )

    # Exact duplicate row refs collapse idempotently, independent of input order.
    unique_by_ref: dict[str, dict[str, Any]] = {}
    for item in parsed:
        unique_by_ref.setdefault(item["supplied_ref"].key, item)
    rows = tuple(sorted(unique_by_ref.values(), key=lambda item: item["supplied_ref"].key))
    actual_refs = tuple(item["supplied_ref"] for item in rows)
    if tuple(ref.key for ref in actual_refs) != tuple(ref.key for ref in declared_row_refs):
        raise GenericR4BatchAdapterError(
            "candidate_row_refs must equal the exact deduplicated refs carried by candidate_rows"
        )

    # Quarantine every presented row participating in same-key/same-generation
    # hash conflict.  Never choose a winner.
    by_logical_snapshot: dict[tuple[str, str, int], list[dict[str, Any]]] = {}
    for item in rows:
        key = (item["namespace"], item["candidate_id"], item["generation"])
        by_logical_snapshot.setdefault(key, []).append(item)
    for group in by_logical_snapshot.values():
        hashes = {item["supplied_ref"].content_hash for item in group}
        if len(hashes) > 1:
            for item in group:
                item["failures"].append(ROW_IDENTITY_CONFLICT)
                item["diagnostics"].append(
                    "same candidate key/generation presented with conflicting content hashes"
                )

    # If both predecessor and successor snapshots are present, the successor's
    # exact predecessor hash must identify the presented prior generation.
    presented_by_object_id = {item["supplied_ref"].object_id: item["supplied_ref"] for item in rows}
    for item in rows:
        predecessor = item["predecessor"]
        if predecessor is None:
            continue
        presented = presented_by_object_id.get(predecessor.object_id)
        if presented is not None and presented != predecessor:
            item["failures"].append(PREDECESSOR_CHAIN_INVALID)
            item["diagnostics"].append("predecessor ref conflicts with presented prior snapshot")

    batch_ref = _batch_ref(batch_namespace, batch_id, actual_refs, batch_provenance)
    supplied_batch_ref_raw = envelope.get("ref", envelope.get("batch_ref"))
    if supplied_batch_ref_raw is not None:
        supplied_batch_ref = _ref(supplied_batch_ref_raw, "batch_ref")
        if supplied_batch_ref != batch_ref:
            raise GenericR4BatchAdapterError("batch_ref does not match exact governed batch material")

    receipts = tuple(
        _make_candidate_receipt(
            batch_ref=batch_ref,
            row_ref=item["supplied_ref"],
            cells=item["cells"],
            failures=item["failures"],
            diagnostics=item["diagnostics"],
        )
        for item in rows
    )
    return GenericR4BatchAdapterResult(
        contract_ref=GENERIC_CONTRACT_REF,
        batch_ref=batch_ref,
        candidate_receipts=receipts,
    )


__all__ = [
    "GENERIC_CONTRACT_ID",
    "GENERIC_CONTRACT_REF",
    "ADOPTED_R4_IMPLEMENTATION_BLOB",
    "R4_CONTRACT_ID",
    "CANDIDATE_ROW_KIND",
    "BATCH_KIND",
    "CANDIDATE_RECEIPT_KIND",
    "BATCH_RECEIPT_KIND",
    "DETERMINANT_IDS",
    "FIELD_PATHS",
    "PACKAGE_PARTITION",
    "STATUS_STATES",
    "FAIL_CLOSED_CODES",
    "SATISFIED_CURRENT",
    "SATISFIED_CANDIDATE_ONLY",
    "MISSING",
    "BLOCKED",
    "NOT_APPLICABLE",
    "NOT_PROJECTABLE",
    "READY_FOR_ADAPTER_PROJECTION",
    "ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT",
    "ELIGIBLE_FOR_SEPARATE_CURRENT_SELECTION",
    "HISTORICAL_NONCURRENT_VALIDATED",
    "NOT_REQUESTED",
    "SERIAL_GATE_BLOCKED",
    "ELIGIBLE_FOR_SEPARATE_SELECTION",
    "SELECTION_EVIDENCE_PRESENT",
    "MALFORMED_EXACT_REF",
    "MUTABLE_SELECTOR_FORBIDDEN",
    "SILENT_NA_FORBIDDEN",
    "ROLE_DISPOSITION_INVALID",
    "VALUE_MODE_CALIBRATION_MISMATCH",
    "CURRENTNESS_EVIDENCE_MISMATCH",
    "ROW_IDENTITY_CONFLICT",
    "PREDECESSOR_CHAIN_INVALID",
    "CANDIDATE_BLOCKED",
    "GenericR4BatchAdapterError",
    "CandidateAdapterReceipt",
    "GenericR4BatchAdapterResult",
    "adapt_generic_r4_batch",
]
