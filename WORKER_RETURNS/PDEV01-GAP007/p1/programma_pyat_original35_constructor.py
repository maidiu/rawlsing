"""PROGRAMMA PYAT P1 sourcefree original35 prospective workload constructor.

This module is a nonissuing constructor. It accepts only exact externally
declared wave, source-grant, item, route, weight, eligibility, semantic, role
and use material. It does not read survey bytes, invent source metadata, mint
source or scientific authority, or claim populated original35 results.

The constructor emits one deterministic prospective operation record for every
admitted item/operation class. Missing or conflicting material becomes an exact
typed HOLD or ABSTAIN record, never a silent omission. Compiled operations are
handed to the present current BatchManifest owner; I03/I05/C11 execution remains
outside this constructor and requires separately granted source and C11
material.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_batch_runner import (
    BatchIntegrityError,
    BatchManifest,
    BatchUnitSpec,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    Pre553IntegrityError,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_issued_workload import (
    OriginalWaveIdentity,
    WorkloadAdmissionError,
    original35_roster,
)

CONSTRUCTOR_ID = "PROGRAMMA_PYAT_P1_ORIGINAL35_EPRE_CONSTRUCTOR@1.0.0"
CONSTRUCTOR_STATUS = "NONISSUING_SOURCEFREE_PROSPECTIVE_CONSTRUCTION_ONLY"
SCOPE_TEST_ONLY = "TEST_ONLY_SOURCEFREE"
SCOPE_ORIGINAL = "ORIGINAL_SOURCE_ISSUED"
ALLOWED_SCOPES = frozenset({SCOPE_TEST_ONLY, SCOPE_ORIGINAL})
OPERATION_DISTRIBUTION = "DISTRIBUTION"
OPERATION_CONDITIONAL = "CONDITIONAL"
OPERATION_JOINT = "JOINT"
OPERATION_HETEROGENEITY = "HETEROGENEITY"
OPERATION_RECURSIVE = "RECURSIVE_BRANCH"
OPERATION_KINDS = frozenset({
    OPERATION_DISTRIBUTION,
    OPERATION_CONDITIONAL,
    OPERATION_JOINT,
    OPERATION_HETEROGENEITY,
    OPERATION_RECURSIVE,
})
MEASURE_DIRECT = "DIRECT_MEASURED"
MEASURE_PROXY = "PROXY_MODELLED"
MEASURE_HYPOTHETICAL = "HYPOTHETICAL"
MEASURE_KINDS = frozenset({MEASURE_DIRECT, MEASURE_PROXY, MEASURE_HYPOTHETICAL})
STATUS_COMPILED = "COMPILED"
STATUS_HOLD = "HOLD"
STATUS_ABSTAIN = "ABSTAIN"
ITEM_ELIGIBLE = "ELIGIBLE"
ITEM_HELD = "HELD"
ITEM_ABSTAIN = "ABSTAIN"


class Original35ConstructorError(ValueError):
    """The exact original35 construction cannot be produced as requested."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Original35ConstructorError(f"{name} must be a non-empty string")
    return value.strip()


def _sha(value: Any, name: str) -> str:
    text = _text(value, name)
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise Original35ConstructorError(f"{name} must be a lowercase sha256")
    return text


def _exact(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise Original35ConstructorError(str(exc)) from exc


def _optional_exact(value: Any, name: str) -> ExactRef | None:
    return None if value is None else _exact(value, name)


def _derive(kind: str, tag: str, material: Any) -> ExactRef:
    digest = semantic_hash({"kind": kind, "tag": tag, "material": canonicalize(material)})
    return ExactRef(kind, f"urn:programma:pyat:{kind.lower()}:{digest}", digest)


def _unique_texts(values: Iterable[Any], name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise Original35ConstructorError(f"{name} must be an iterable of exact strings")
    out = tuple(sorted({_text(value, name) for value in values}))
    return out


@dataclass(frozen=True)
class SourceGrant:
    grant_ref: ExactRef | None
    source_sha256: str | None
    scope: str
    operations: tuple[str, ...] = ()
    host: str | None = None
    purpose: str | None = None
    currentness: str | None = None
    item_registry_ref: ExactRef | None = None
    eligible_population_ref: ExactRef | None = None
    target_use_permission_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "grant_ref", _optional_exact(self.grant_ref, "grant_ref"))
        if self.source_sha256 is not None:
            object.__setattr__(self, "source_sha256", _sha(self.source_sha256, "source_sha256"))
        scope = _text(self.scope, "scope")
        if scope not in ALLOWED_SCOPES:
            raise Original35ConstructorError(f"unknown source scope: {scope}")
        object.__setattr__(self, "scope", scope)
        object.__setattr__(self, "operations", _unique_texts(self.operations, "operation"))
        object.__setattr__(self, "host", None if self.host is None else _text(self.host, "host"))
        object.__setattr__(self, "purpose", None if self.purpose is None else _text(self.purpose, "purpose"))
        object.__setattr__(
            self, "currentness",
            None if self.currentness is None else _text(self.currentness, "currentness"))
        object.__setattr__(self, "item_registry_ref", _optional_exact(
            self.item_registry_ref, "item_registry_ref"))
        object.__setattr__(self, "eligible_population_ref", _optional_exact(
            self.eligible_population_ref, "eligible_population_ref"))
        object.__setattr__(self, "target_use_permission_ref", _optional_exact(
            self.target_use_permission_ref, "target_use_permission_ref"))

    def material(self) -> dict[str, Any]:
        return {
            "grant_ref": self.grant_ref.as_dict() if self.grant_ref else None,
            "source_sha256": self.source_sha256,
            "scope": self.scope,
            "operations": list(self.operations),
            "host": self.host,
            "purpose": self.purpose,
            "currentness": self.currentness,
            "item_registry_ref": self.item_registry_ref.as_dict() if self.item_registry_ref else None,
            "eligible_population_ref": (
                self.eligible_population_ref.as_dict() if self.eligible_population_ref else None),
            "target_use_permission_ref": (
                self.target_use_permission_ref.as_dict() if self.target_use_permission_ref else None),
        }


@dataclass(frozen=True)
class WaveIdentity:
    atlas_id: str
    dataset_id: str
    source_family: str
    wave: str
    source_sha256: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "atlas_id", _text(self.atlas_id, "atlas_id"))
        object.__setattr__(self, "dataset_id", _text(self.dataset_id, "dataset_id"))
        object.__setattr__(self, "source_family", _text(self.source_family, "source_family"))
        object.__setattr__(self, "wave", _text(self.wave, "wave"))
        object.__setattr__(self, "source_sha256", _sha(self.source_sha256, "source_sha256"))

    def as_roster(self) -> dict[str, Any]:
        return {
            "atlas_id": self.atlas_id,
            "original_manifest_identity": {"dataset_id": self.dataset_id},
            "family": self.source_family,
            "wave": self.wave,
        }

    def as_original_wave(self) -> OriginalWaveIdentity:
        return OriginalWaveIdentity(
            self.atlas_id, self.dataset_id, self.source_family, self.wave)

    def material(self) -> dict[str, Any]:
        return {
            "atlas_id": self.atlas_id,
            "dataset_id": self.dataset_id,
            "source_family": self.source_family,
            "wave": self.wave,
            "source_sha256": self.source_sha256,
        }


@dataclass(frozen=True)
class ConditionerBinding:
    conditioner_ref: ExactRef | None
    conditioner_code: str
    values: tuple[str, ...]
    eligibility_ref: ExactRef | None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "conditioner_ref", _optional_exact(self.conditioner_ref, "conditioner_ref"))
        object.__setattr__(
            self, "conditioner_code", _text(self.conditioner_code, "conditioner_code"))
        object.__setattr__(self, "values", _unique_texts(self.values, "conditioner_value"))
        object.__setattr__(
            self, "eligibility_ref", _optional_exact(self.eligibility_ref, "conditioner_eligibility_ref"))

    def material(self) -> dict[str, Any]:
        return {
            "conditioner_ref": self.conditioner_ref.as_dict() if self.conditioner_ref else None,
            "conditioner_code": self.conditioner_code,
            "values": list(self.values),
            "eligibility_ref": self.eligibility_ref.as_dict() if self.eligibility_ref else None,
        }


@dataclass(frozen=True)
class JointBinding:
    other_item_ref: ExactRef | None
    other_code: str
    values: tuple[str, ...]
    joint_authority_ref: ExactRef | None
    eligibility_ref: ExactRef | None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "other_item_ref", _optional_exact(self.other_item_ref, "other_item_ref"))
        object.__setattr__(self, "other_code", _text(self.other_code, "other_code"))
        object.__setattr__(self, "values", _unique_texts(self.values, "joint_value"))
        object.__setattr__(
            self, "joint_authority_ref", _optional_exact(
                self.joint_authority_ref, "joint_authority_ref"))
        object.__setattr__(
            self, "eligibility_ref", _optional_exact(self.eligibility_ref, "joint_eligibility_ref"))

    def material(self) -> dict[str, Any]:
        return {
            "other_item_ref": self.other_item_ref.as_dict() if self.other_item_ref else None,
            "other_code": self.other_code,
            "values": list(self.values),
            "joint_authority_ref": self.joint_authority_ref.as_dict()
            if self.joint_authority_ref else None,
            "eligibility_ref": self.eligibility_ref.as_dict() if self.eligibility_ref else None,
        }


@dataclass(frozen=True)
class EligibleItem:
    item_ref: ExactRef | None
    source_variable_code: str
    response_values: tuple[str, ...]
    route_ref: ExactRef | None
    weight_ref: ExactRef | None
    eligibility_ref: ExactRef | None
    semantic_ref: ExactRef | None
    role_ref: ExactRef | None
    use_permission_ref: ExactRef | None
    operation_kinds: tuple[str, ...]
    measure_kind: str = MEASURE_DIRECT
    measure_authority_ref: ExactRef | None = None
    conditioner_bindings: tuple[ConditionerBinding, ...] = ()
    joint_bindings: tuple[JointBinding, ...] = ()
    stratum_refs: tuple[ExactRef, ...] = ()
    recursive_authority_ref: ExactRef | None = None
    disposition: str = ITEM_ELIGIBLE
    reason: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "item_ref", _optional_exact(self.item_ref, "item_ref"))
        object.__setattr__(
            self, "source_variable_code", _text(self.source_variable_code, "source_variable_code"))
        object.__setattr__(
            self, "response_values", _unique_texts(self.response_values, "response_value"))
        for name in ("route_ref", "weight_ref", "eligibility_ref", "semantic_ref",
                     "role_ref", "use_permission_ref", "measure_authority_ref",
                     "recursive_authority_ref"):
            object.__setattr__(self, name, _optional_exact(getattr(self, name), name))
        kinds = _unique_texts(self.operation_kinds, "operation_kind")
        if any(kind not in OPERATION_KINDS for kind in kinds):
            raise Original35ConstructorError("unknown operation kind")
        object.__setattr__(self, "operation_kinds", kinds)
        measure_kind = _text(self.measure_kind, "measure_kind")
        if measure_kind not in MEASURE_KINDS:
            raise Original35ConstructorError(f"unknown measure kind: {measure_kind}")
        object.__setattr__(self, "measure_kind", measure_kind)
        bindings = tuple(self.conditioner_bindings)
        if not all(isinstance(binding, ConditionerBinding) for binding in bindings):
            raise Original35ConstructorError("conditioner_bindings must be ConditionerBinding")
        object.__setattr__(self, "conditioner_bindings", bindings)
        joints = tuple(self.joint_bindings)
        if not all(isinstance(binding, JointBinding) for binding in joints):
            raise Original35ConstructorError("joint_bindings must be JointBinding")
        object.__setattr__(self, "joint_bindings", joints)
        object.__setattr__(
            self, "stratum_refs", tuple(_exact(ref, "stratum_ref") for ref in self.stratum_refs))
        disposition = _text(self.disposition, "disposition").upper()
        if disposition not in {ITEM_ELIGIBLE, ITEM_HELD, ITEM_ABSTAIN}:
            raise Original35ConstructorError(f"unknown item disposition: {disposition}")
        object.__setattr__(self, "disposition", disposition)
        object.__setattr__(
            self, "reason", None if self.reason is None else _text(self.reason, "reason"))

    def material(self) -> dict[str, Any]:
        return {
            "item_ref": self.item_ref.as_dict() if self.item_ref else None,
            "source_variable_code": self.source_variable_code,
            "response_values": list(self.response_values),
            "route_ref": self.route_ref.as_dict() if self.route_ref else None,
            "weight_ref": self.weight_ref.as_dict() if self.weight_ref else None,
            "eligibility_ref": self.eligibility_ref.as_dict() if self.eligibility_ref else None,
            "semantic_ref": self.semantic_ref.as_dict() if self.semantic_ref else None,
            "role_ref": self.role_ref.as_dict() if self.role_ref else None,
            "use_permission_ref": (
                self.use_permission_ref.as_dict() if self.use_permission_ref else None),
            "operation_kinds": list(self.operation_kinds),
            "measure_kind": self.measure_kind,
            "measure_authority_ref": (
                self.measure_authority_ref.as_dict() if self.measure_authority_ref else None),
            "conditioner_bindings": [binding.material() for binding in self.conditioner_bindings],
            "joint_bindings": [binding.material() for binding in self.joint_bindings],
            "stratum_refs": [ref.as_dict() for ref in self.stratum_refs],
            "recursive_authority_ref": (
                self.recursive_authority_ref.as_dict() if self.recursive_authority_ref else None),
            "disposition": self.disposition,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class WaveAdmission:
    identity: WaveIdentity
    release_ref: ExactRef | None
    source_grant: SourceGrant | None
    items: tuple[EligibleItem, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.identity, WaveIdentity):
            raise Original35ConstructorError("identity must be WaveIdentity")
        release_ref = _optional_exact(self.release_ref, "release_ref")
        if release_ref is not None and release_ref.kind != "C11LogicalRelease":
            raise Original35ConstructorError("release_ref must be C11LogicalRelease")
        object.__setattr__(self, "release_ref", release_ref)
        if self.source_grant is not None and not isinstance(self.source_grant, SourceGrant):
            raise Original35ConstructorError("source_grant must be SourceGrant or None")
        items = tuple(self.items)
        if not items or not all(isinstance(item, EligibleItem) for item in items):
            raise Original35ConstructorError("each wave requires EligibleItem entries")
        object.__setattr__(self, "items", items)


@dataclass(frozen=True)
class ScientificMethodInput:
    method_ref: ExactRef | None
    method_kind: str
    owner_ref: ExactRef | None
    authority_ref: ExactRef | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "method_ref", _optional_exact(self.method_ref, "method_ref"))
        kind = _text(self.method_kind, "method_kind")
        if kind not in MEASURE_KINDS:
            raise Original35ConstructorError(f"unknown method kind: {kind}")
        object.__setattr__(self, "method_kind", kind)
        object.__setattr__(self, "owner_ref", _optional_exact(self.owner_ref, "owner_ref"))
        object.__setattr__(
            self, "authority_ref", _optional_exact(self.authority_ref, "authority_ref"))

    def material(self) -> dict[str, Any]:
        return {
            "method_ref": self.method_ref.as_dict() if self.method_ref else None,
            "method_kind": self.method_kind,
            "owner_ref": self.owner_ref.as_dict() if self.owner_ref else None,
            "authority_ref": self.authority_ref.as_dict() if self.authority_ref else None,
        }


@dataclass(frozen=True)
class Original35Input:
    waves: tuple[WaveAdmission, ...]
    scientific_method: ScientificMethodInput

    def __post_init__(self) -> None:
        waves = tuple(self.waves)
        if not all(isinstance(wave, WaveAdmission) for wave in waves):
            raise Original35ConstructorError("waves must be WaveAdmission entries")
        if not isinstance(self.scientific_method, ScientificMethodInput):
            raise Original35ConstructorError("scientific_method must be ScientificMethodInput")
        object.__setattr__(self, "waves", waves)


@dataclass(frozen=True)
class EpreOperation:
    operation_ref: ExactRef
    wave_atlas_id: str
    item_ref: ExactRef | None
    operation_kind: str
    target_value: str | None
    conditioner_ref: ExactRef | None
    conditioner_value: str | None
    joint_item_ref: ExactRef | None
    joint_value: str | None
    stratum_ref: ExactRef | None
    measure_kind: str
    status: str
    reason: str | None
    batch_job_ref: ExactRef | None
    semantic_input_refs: tuple[ExactRef, ...]

    def material(self) -> dict[str, Any]:
        return {
            "operation_ref": self.operation_ref.as_dict(),
            "wave_atlas_id": self.wave_atlas_id,
            "item_ref": self.item_ref.as_dict() if self.item_ref else None,
            "operation_kind": self.operation_kind,
            "target_value": self.target_value,
            "conditioner_ref": self.conditioner_ref.as_dict() if self.conditioner_ref else None,
            "conditioner_value": self.conditioner_value,
            "joint_item_ref": self.joint_item_ref.as_dict() if self.joint_item_ref else None,
            "joint_value": self.joint_value,
            "stratum_ref": self.stratum_ref.as_dict() if self.stratum_ref else None,
            "measure_kind": self.measure_kind,
            "status": self.status,
            "reason": self.reason,
            "batch_job_ref": self.batch_job_ref.as_dict() if self.batch_job_ref else None,
            "semantic_input_refs": [ref.as_dict() for ref in self.semantic_input_refs],
        }


@dataclass(frozen=True)
class WaveConstruction:
    identity: WaveIdentity
    u_item_refs: tuple[ExactRef, ...]
    u_unit_ref: ExactRef | None
    u_app_ref: ExactRef | None
    e_pre_ref: str | None
    operations: tuple[EpreOperation, ...]
    completed: bool
    reasons: tuple[str, ...]

    def material(self) -> dict[str, Any]:
        return {
            "identity": self.identity.material(),
            "u_item_refs": [ref.as_dict() for ref in self.u_item_refs],
            "u_unit_ref": self.u_unit_ref.as_dict() if self.u_unit_ref else None,
            "u_app_ref": self.u_app_ref.as_dict() if self.u_app_ref else None,
            "e_pre_ref": self.e_pre_ref,
            "operations": [operation.material() for operation in self.operations],
            "completed": self.completed,
            "reasons": list(self.reasons),
        }


@dataclass(frozen=True)
class Original35EprePlan:
    schema: str
    constructor_status: str
    roster: tuple[OriginalWaveIdentity, ...]
    roster_ref: str
    waves: tuple[WaveConstruction, ...]
    operations: tuple[EpreOperation, ...]
    holds: tuple[EpreOperation, ...]
    abstentions: tuple[EpreOperation, ...]
    batch_manifest: BatchManifest | None
    batch_units: tuple[BatchUnitSpec, ...]
    no_drop_manifest: Mapping[str, Any]
    no_drop_ok: bool
    source_qualification: str
    scientific_method: ScientificMethodInput
    all35_populated_claim: bool
    sourced_results_claim: bool
    plan_ref: str

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "constructor_status": self.constructor_status,
            "roster": [wave.material() for wave in self.roster],
            "roster_ref": self.roster_ref,
            "waves": [wave.material() for wave in self.waves],
            "operations": [operation.material() for operation in self.operations],
            "holds": [operation.material() for operation in self.holds],
            "abstentions": [operation.material() for operation in self.abstentions],
            "batch_manifest_ref": (
                self.batch_manifest.manifest_ref.as_dict() if self.batch_manifest else None),
            "batch_unit_refs": [unit.unit_ref.as_dict() for unit in self.batch_units],
            "no_drop_manifest": canonicalize(self.no_drop_manifest),
            "no_drop_ok": self.no_drop_ok,
            "source_qualification": self.source_qualification,
            "scientific_method": self.scientific_method.material(),
            "all35_populated_claim": self.all35_populated_claim,
            "sourced_results_claim": self.sourced_results_claim,
        }


def _operation_ref(atlas_id: str, item: EligibleItem, kind: str, target: str | None,
                   conditioner: ConditionerBinding | None, conditioner_value: str | None,
                   joint: JointBinding | None, joint_value: str | None,
                   stratum: ExactRef | None) -> ExactRef:
    material = {
        "atlas_id": atlas_id,
        "item": item.item_ref.as_dict() if item.item_ref else None,
        "source_variable_code": item.source_variable_code,
        "kind": kind,
        "target": target,
        "conditioner": conditioner.material() if conditioner else None,
        "conditioner_value": conditioner_value,
        "joint": joint.material() if joint else None,
        "joint_value": joint_value,
        "stratum": stratum.as_dict() if stratum else None,
        "measure_kind": item.measure_kind,
    }
    return _derive("PROGRAMMA_PYAT_EPRE_OPERATION", atlas_id, material)


def _operation(
    *, wave: WaveAdmission, item: EligibleItem, kind: str, target: str | None = None,
    conditioner: ConditionerBinding | None = None, conditioner_value: str | None = None,
    joint: JointBinding | None = None, joint_value: str | None = None,
    stratum: ExactRef | None = None, status: str, reason: str | None,
    semantic_input_refs: Iterable[ExactRef] = (),
) -> EpreOperation:
    ref = _operation_ref(wave.identity.atlas_id, item, kind, target, conditioner,
                         conditioner_value, joint, joint_value, stratum)
    inputs = {
        ref for ref in (
            item.item_ref, item.route_ref, item.weight_ref, item.eligibility_ref,
            item.semantic_ref, item.role_ref, item.use_permission_ref,
            item.measure_authority_ref, conditioner.conditioner_ref if conditioner else None,
            joint.other_item_ref if joint else None,
            joint.joint_authority_ref if joint else None,
            stratum, item.recursive_authority_ref,
        ) if ref is not None
    }
    inputs.update(semantic_input_refs)
    job_ref = ref if status == STATUS_COMPILED else None
    return EpreOperation(
        operation_ref=ref,
        wave_atlas_id=wave.identity.atlas_id,
        item_ref=item.item_ref,
        operation_kind=kind,
        target_value=target,
        conditioner_ref=conditioner.conditioner_ref if conditioner else None,
        conditioner_value=conditioner_value,
        joint_item_ref=joint.other_item_ref if joint else None,
        joint_value=joint_value,
        stratum_ref=stratum,
        measure_kind=item.measure_kind,
        status=status,
        reason=reason,
        batch_job_ref=job_ref,
        semantic_input_refs=tuple(sorted(inputs, key=lambda value: value.key)),
    )


def _item_refusal(item: EligibleItem, grant: SourceGrant, method: ScientificMethodInput) -> str | None:
    if item.disposition == ITEM_HELD:
        return f"ITEM_HELD:{item.reason or 'EXTERNAL_HOLD'}"
    if item.disposition == ITEM_ABSTAIN:
        return f"ITEM_ABSTAIN:{item.reason or 'EXTERNAL_ABSTAIN'}"
    if item.item_ref is None:
        return "ITEM_REF_ABSENT"
    if not item.response_values:
        return "RESPONSE_VALUES_ABSENT"
    if item.route_ref is None:
        return "ROUTE_REF_ABSENT"
    if item.weight_ref is None:
        return "WEIGHT_REF_ABSENT"
    if item.eligibility_ref is None:
        return "ELIGIBILITY_REF_ABSENT"
    if item.semantic_ref is None:
        return "SEMANTIC_REF_ABSENT"
    if item.role_ref is None:
        return "ROLE_REF_ABSENT"
    if item.use_permission_ref is None:
        return "USE_PERMISSION_REF_ABSENT"
    if grant.eligible_population_ref is not None and item.eligibility_ref != grant.eligible_population_ref:
        return "RESPONDENT_ELIGIBILITY_MISMATCH"
    if item.measure_kind not in grant.operations:
        return "MEASURE_NOT_IN_SOURCE_GRANT"
    if item.measure_kind == MEASURE_DIRECT and item.measure_authority_ref is None:
        return "DIRECT_MEASURE_AUTHORITY_ABSENT"
    if item.measure_kind != MEASURE_DIRECT and (
            method.owner_ref is None or method.authority_ref is None):
        return "METHOD_OWNER_OR_AUTHORITY_ABSENT"
    if method.method_kind != item.measure_kind:
        return "MEASURE_METHOD_KIND_MISMATCH"
    return None


def _wave_refusal(wave: WaveAdmission, method: ScientificMethodInput) -> str | None:
    if wave.release_ref is None:
        return "C11_RELEASE_REF_ABSENT"
    if wave.source_grant is None:
        return "SOURCE_GRANT_ABSENT"
    grant = wave.source_grant
    if grant.grant_ref is None:
        return "SOURCE_GRANT_REF_ABSENT"
    if grant.scope not in ALLOWED_SCOPES:
        return "SOURCE_SCOPE_INVALID"
    if grant.currentness != "CURRENT":
        return "SOURCE_GRANT_NOT_CURRENT"
    if grant.source_sha256 is None:
        return "SOURCE_SHA_ABSENT"
    if grant.source_sha256 != wave.identity.source_sha256:
        return "SOURCE_SHA_MISMATCH"
    if grant.item_registry_ref is None:
        return "ITEM_REGISTRY_REF_ABSENT"
    if grant.eligible_population_ref is None:
        return "ELIGIBLE_POPULATION_REF_ABSENT"
    if grant.target_use_permission_ref is None:
        return "TARGET_USE_PERMISSION_REF_ABSENT"
    if not grant.operations:
        return "SOURCE_OPERATION_SET_ABSENT"
    if method.method_kind != MEASURE_DIRECT and (
            method.owner_ref is None or method.authority_ref is None):
        return "SCIENTIFIC_METHOD_OWNER_ABSENT"
    return None


def _slot_operations(wave: WaveAdmission, item: EligibleItem, *, status: str,
                     reason: str) -> list[EpreOperation]:
    out: list[EpreOperation] = []
    for kind in item.operation_kinds:
        if not item.response_values:
            out.append(_operation(wave=wave, item=item, kind=kind, status=status, reason=reason))
            continue
        if kind == OPERATION_DISTRIBUTION:
            for value in item.response_values:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, target=value,
                    status=status, reason=reason))
        elif kind == OPERATION_CONDITIONAL:
            if not item.conditioner_bindings:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, status=status, reason=reason))
                continue
            for binding in item.conditioner_bindings:
                for target in item.response_values:
                    for value in binding.values:
                        out.append(_operation(
                            wave=wave, item=item, kind=kind, target=target,
                            conditioner=binding, conditioner_value=value,
                            status=status, reason=reason))
        elif kind == OPERATION_JOINT:
            if not item.joint_bindings:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, status=status, reason=reason))
                continue
            for binding in item.joint_bindings:
                for target in item.response_values:
                    for value in binding.values:
                        out.append(_operation(
                            wave=wave, item=item, kind=kind, target=target,
                            joint=binding, joint_value=value,
                            status=status, reason=reason))
        elif kind == OPERATION_HETEROGENEITY:
            if not item.stratum_refs:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, status=status, reason=reason))
                continue
            for stratum in item.stratum_refs:
                for target in item.response_values:
                    out.append(_operation(
                        wave=wave, item=item, kind=kind, target=target,
                        stratum=stratum, status=status, reason=reason))
        elif kind == OPERATION_RECURSIVE:
            for target in item.response_values:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, target=target,
                    status=status, reason=reason))
    return out


def _operations_for_item(wave: WaveAdmission, item: EligibleItem,
                         method: ScientificMethodInput) -> list[EpreOperation]:
    grant = wave.source_grant
    assert grant is not None
    refusal = _item_refusal(item, grant, method)
    if refusal is not None:
        status = STATUS_ABSTAIN if "MISMATCH" in refusal or "ABSTAIN" in refusal else STATUS_HOLD
        return _slot_operations(wave, item, status=status, reason=refusal)
    out: list[EpreOperation] = []
    for kind in item.operation_kinds:
        if kind not in grant.operations:
            out.append(_operation(
                wave=wave, item=item, kind=kind, status=STATUS_HOLD,
                reason="OPERATION_NOT_IN_SOURCE_GRANT"))
            continue
        if kind == OPERATION_DISTRIBUTION:
            for value in item.response_values:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, target=value,
                    status=STATUS_COMPILED, reason=None))
        elif kind == OPERATION_CONDITIONAL:
            if not item.conditioner_bindings:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, status=STATUS_HOLD,
                    reason="CONDITIONER_BINDING_ABSENT"))
                continue
            for binding in item.conditioner_bindings:
                if binding.conditioner_ref is None or binding.eligibility_ref is None:
                    out.append(_operation(
                        wave=wave, item=item, kind=kind, status=STATUS_HOLD,
                        reason="CONDITIONER_REF_OR_ELIGIBILITY_ABSENT"))
                    continue
                if binding.eligibility_ref != item.eligibility_ref:
                    out.append(_operation(
                        wave=wave, item=item, kind=kind, status=STATUS_ABSTAIN,
                        reason="CONDITIONER_ELIGIBILITY_MISMATCH"))
                    continue
                for target in item.response_values:
                    for value in binding.values:
                        out.append(_operation(
                            wave=wave, item=item, kind=kind, target=target,
                            conditioner=binding, conditioner_value=value,
                            status=STATUS_COMPILED, reason=None))
        elif kind == OPERATION_JOINT:
            if not item.joint_bindings:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, status=STATUS_HOLD,
                    reason="JOINT_BINDING_ABSENT"))
                continue
            for binding in item.joint_bindings:
                if (binding.other_item_ref is None or binding.joint_authority_ref is None
                        or binding.eligibility_ref is None):
                    out.append(_operation(
                        wave=wave, item=item, kind=kind, status=STATUS_HOLD,
                        reason="JOINT_REF_OR_AUTHORITY_ABSENT"))
                    continue
                if binding.eligibility_ref != item.eligibility_ref:
                    out.append(_operation(
                        wave=wave, item=item, kind=kind, status=STATUS_ABSTAIN,
                        reason="JOINT_ELIGIBILITY_MISMATCH"))
                    continue
                for target in item.response_values:
                    for value in binding.values:
                        out.append(_operation(
                            wave=wave, item=item, kind=kind, target=target,
                            joint=binding, joint_value=value,
                            status=STATUS_COMPILED, reason=None))
        elif kind == OPERATION_HETEROGENEITY:
            if not item.stratum_refs:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, status=STATUS_HOLD,
                    reason="STRATUM_REF_ABSENT"))
                continue
            for stratum in item.stratum_refs:
                for target in item.response_values:
                    out.append(_operation(
                        wave=wave, item=item, kind=kind, target=target, stratum=stratum,
                        status=STATUS_COMPILED, reason=None))
        elif kind == OPERATION_RECURSIVE:
            if item.recursive_authority_ref is None:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, status=STATUS_HOLD,
                    reason="RECURSIVE_AUTHORITY_ABSENT"))
                continue
            for target in item.response_values:
                out.append(_operation(
                    wave=wave, item=item, kind=kind, target=target,
                    status=STATUS_COMPILED, reason=None))
    return out


def _batch_unit(wave: WaveAdmission, operation: EpreOperation) -> BatchUnitSpec:
    assert wave.release_ref is not None
    assert operation.batch_job_ref is not None
    kind = "DISCOVERY" if operation.operation_kind == OPERATION_RECURSIVE else "QUERY"
    try:
        return BatchUnitSpec(
            job_kind=kind,
            job_ref=operation.batch_job_ref,
            release_refs=(wave.release_ref,),
            semantic_input_refs=operation.semantic_input_refs,
        )
    except BatchIntegrityError as exc:
        raise Original35ConstructorError(str(exc)) from exc


def construct_original35_epre(input: Original35Input) -> Original35EprePlan:
    if not isinstance(input, Original35Input):
        raise Original35ConstructorError("Original35Input required")
    try:
        roster = original35_roster([wave.identity.as_roster() for wave in input.waves])
    except WorkloadAdmissionError as exc:
        raise Original35ConstructorError(str(exc)) from exc
    seen_item_refs: set[str] = set()
    seen_operation_refs: set[str] = set()
    waves: list[WaveConstruction] = []
    operations: list[EpreOperation] = []
    holds: list[EpreOperation] = []
    abstentions: list[EpreOperation] = []
    batch_units: list[BatchUnitSpec] = []
    for wave in input.waves:
        reasons: list[str] = []
        wave_refusal = _wave_refusal(wave, input.scientific_method)
        if wave_refusal is not None:
            reasons.append(wave_refusal)
        wave_operations: list[EpreOperation] = []
        for item in wave.items:
            if item.item_ref is not None:
                if item.item_ref.key in seen_item_refs:
                    raise Original35ConstructorError("DUPLICATE_ITEM_REF")
                seen_item_refs.add(item.item_ref.key)
            if wave_refusal is not None:
                status = STATUS_ABSTAIN if "MISMATCH" in wave_refusal else STATUS_HOLD
                wave_operations.extend(_slot_operations(
                    wave, item, status=status, reason=wave_refusal))
            else:
                wave_operations.extend(_operations_for_item(wave, item, input.scientific_method))
        for operation in wave_operations:
            if operation.operation_ref.key in seen_operation_refs:
                raise Original35ConstructorError("DUPLICATE_OPERATION_REF")
            seen_operation_refs.add(operation.operation_ref.key)
            operations.append(operation)
            if operation.status == STATUS_HOLD:
                holds.append(operation)
            elif operation.status == STATUS_ABSTAIN:
                abstentions.append(operation)
            else:
                batch_units.append(_batch_unit(wave, operation))
        compiled = sum(1 for operation in wave_operations if operation.status == STATUS_COMPILED)
        wave_holds = sum(1 for operation in wave_operations if operation.status == STATUS_HOLD)
        wave_abstains = sum(1 for operation in wave_operations if operation.status == STATUS_ABSTAIN)
        if not wave_operations:
            reasons.append("NO_OPERATIONS_EMITTED")
        e_pre_ref = semantic_hash([operation.material() for operation in wave_operations]) if wave_operations else None
        u_item_refs = tuple(sorted({
            item.item_ref for item in wave.items if item.item_ref is not None
        }, key=lambda ref: ref.key))
        u_unit_ref = _derive("PROGRAMMA_PYAT_U_UNIT", wave.identity.atlas_id, wave.identity.material())
        u_app_ref = wave.source_grant.eligible_population_ref if wave.source_grant else None
        completed = bool(wave_operations) and not (wave_refusal is not None and not wave_operations)
        waves.append(WaveConstruction(
            identity=wave.identity,
            u_item_refs=u_item_refs,
            u_unit_ref=u_unit_ref,
            u_app_ref=u_app_ref,
            e_pre_ref=e_pre_ref,
            operations=tuple(wave_operations),
            completed=completed,
            reasons=tuple(sorted(set(reasons))),
        ))
        if compiled or wave_holds or wave_abstains:
            continue
    batch_manifest = None
    if batch_units:
        try:
            batch_manifest = BatchManifest(tuple(batch_units))
        except BatchIntegrityError as exc:
            raise Original35ConstructorError(str(exc)) from exc
    roster_material = [wave.identity.material() for wave in input.waves]
    roster_ref = semantic_hash(roster_material)
    operation_ids = [operation.operation_ref.key for operation in operations]
    expected_item_count = sum(len(wave.items) for wave in input.waves)
    processed_item_count = sum(
        1 for wave in input.waves for item in wave.items
        if any(op.item_ref == item.item_ref for op in operations))
    no_drop_manifest = {
        "roster_count": len(roster),
        "wave_count": len(input.waves),
        "expected_item_count": expected_item_count,
        "processed_item_count": processed_item_count,
        "compiled_operations": len(batch_units),
        "held_operations": len(holds),
        "abstained_operations": len(abstentions),
        "operation_record_count": len(operations),
        "duplicate_operation_refs": sorted({
            key for key in operation_ids if operation_ids.count(key) > 1
        }),
        "waves_completed": sum(1 for wave in waves if wave.completed),
        "wave_reasons": {wave.identity.atlas_id: list(wave.reasons) for wave in waves if wave.reasons},
    }
    no_drop_ok = (
        len(roster) == 35
        and len({wave.identity.atlas_id for wave in input.waves}) == 35
        and processed_item_count == expected_item_count
        and all(wave.completed for wave in waves)
        and not no_drop_manifest["duplicate_operation_refs"]
        and len(operations) == len(batch_units) + len(holds) + len(abstentions)
    )
    if any(wave.source_grant is None for wave in input.waves):
        source_qualification = "NONISSUING_MIXED_OR_ABSENT"
    else:
        scopes = {wave.source_grant.scope for wave in input.waves}
        source_qualification = (
            SCOPE_ORIGINAL if scopes == {SCOPE_ORIGINAL}
            else SCOPE_TEST_ONLY if scopes == {SCOPE_TEST_ONLY}
            else "NONISSUING_MIXED_OR_ABSENT")
    plan = Original35EprePlan(
        schema=CONSTRUCTOR_ID,
        constructor_status=CONSTRUCTOR_STATUS,
        roster=roster,
        roster_ref=roster_ref,
        waves=tuple(waves),
        operations=tuple(operations),
        holds=tuple(holds),
        abstentions=tuple(abstentions),
        batch_manifest=batch_manifest,
        batch_units=tuple(sorted(batch_units, key=lambda unit: unit.unit_ref.key)),
        no_drop_manifest=no_drop_manifest,
        no_drop_ok=no_drop_ok,
        source_qualification=source_qualification,
        scientific_method=input.scientific_method,
        all35_populated_claim=False,
        sourced_results_claim=False,
        plan_ref=semantic_hash({
            "schema": CONSTRUCTOR_ID,
            "roster_ref": roster_ref,
            "waves": [wave.material() for wave in waves],
            "no_drop_manifest": no_drop_manifest,
            "source_qualification": source_qualification,
            "scientific_method": input.scientific_method.material(),
        }),
    )
    return plan


__all__ = [
    "CONSTRUCTOR_ID",
    "CONSTRUCTOR_STATUS",
    "SCOPE_TEST_ONLY",
    "SCOPE_ORIGINAL",
    "OPERATION_KINDS",
    "MEASURE_KINDS",
    "Original35ConstructorError",
    "SourceGrant",
    "WaveIdentity",
    "ConditionerBinding",
    "JointBinding",
    "EligibleItem",
    "WaveAdmission",
    "ScientificMethodInput",
    "Original35Input",
    "EpreOperation",
    "WaveConstruction",
    "Original35EprePlan",
    "construct_original35_epre",
]
