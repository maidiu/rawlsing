"""R61 semantic lowerer for the current PRE553 I05 exact grammar contract.

The lowerer asks a supplied native catalog for exact typed predicate/query refs
and objects, validates the operation against the frozen policy, and compiles the
expected native candidate identities before execution. Missing capability is a
typed refusal; the scientific operation is never pruned.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
import copy
import json
import re
import threading
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_discovery_exact import (
    CANDIDATE_FAMILIES,
    CANDIDATE_GRAMMAR_SCHEMA,
    I05_CONTRACT_ID,
    PREDICATE_FORMS,
    VALIDATION_KINDS,
    _Atom,
    _Template,
    _combine_predicates,
    _compile_frontier,
    _xor_exactly_one,
    _catalog_atoms, _catalog_templates, _validate_catalog_scope,
    _verify_discovery_authority, _allowed_validation_kinds,
    _derived_ref as _discovery_ref, COVERAGE_CLAIM,
    QUERY_EXECUTION_CONTRACT_ID, TERMINAL_COVERAGE_STATES,
)
from rawlsing_next.pre553_empirical_objects import (
    canonicalize,
    exact_ref,
    semantic_hash,
    DiscoveryResultReceipt, DiscoveryAuthority, EmpiricalQuerySpec,
)
from rawlsing_next.pre553_empirical_authority import validate_object_authority_closure
from rawlsing_next.pre553_recursive_handoff import (
    RecursiveBranchHandoff,
    _restore_binding,
    _restore_predicate,
    execute_exact_bounded_discovery_with_handoffs,
    load_recursive_handoff_bundle,
    replay_recursive_branch_membership,
    _make_handoff, _resolve_receipt_winner,
)

from rawlsing_next.pre553_empirical_query import (
    _resolve_release_indices, _require_exact_i03_authority_fitness,
    _parse_target_plan, _verify_public_identity,
)
from rawlsing_next._pre553_query_predicate import (
    _validate_public_object_authorities, _eval_predicate,
)
from types import SimpleNamespace

from .enumerate import role_disposition
from .types import (
    ELIGIBLE, UNSUPPORTED_RUNTIME, GrammarPolicy, OccurrenceKey,
    ScientificFrontier, ScientificOperation, SourceInventory, typed_value_key,
    value_material, ABSENT, _validate_typed_value,
)

SUPPORTED = "SUPPORTED"
NOT_ELIGIBLE = "NOT_ELIGIBLE"
NATIVE_UNSUPPORTED = UNSUPPORTED_RUNTIME
SUPPORTED_DISPOSITIONS = (SUPPORTED, NOT_ELIGIBLE, NATIVE_UNSUPPORTED)
LOWERING_VERSION = "R61_R01_LOWERING@2.0.0"

_DIFF_VALIDATION = {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}
_JOINT_VALIDATION = {"kind": "JOINT_NOT_PRODUCT_OF_MARGINALS"}
_TARGET_VALIDATION = {"kind": "TARGET_CELL_SUPPORTED"}


def current_native_contract() -> dict[str, Any]:
    """Read the actual imported current I05 contract, not a historical memory."""

    return {
        "contract_id": I05_CONTRACT_ID,
        "grammar_schema": CANDIDATE_GRAMMAR_SCHEMA,
        "families": tuple(sorted(CANDIDATE_FAMILIES)),
        "forms": tuple(sorted(PREDICATE_FORMS)),
        "validations": tuple(sorted(VALIDATION_KINDS)),
        "lowering_version": LOWERING_VERSION,
    }


def _catalog_key(occurrence_key: OccurrenceKey, value: Any) -> str:
    return occurrence_key.key + "|" + typed_value_key(value)


def _target_key(targets: Sequence[OccurrenceKey]) -> str:
    return json.dumps([target.key for target in targets], sort_keys=False, separators=(",", ":"))


def _ref_material(value: Any) -> dict[str, str]:
    return exact_ref(value, "native catalog ref").as_dict()


def _normalize_material(value: Any) -> Any:
    if isinstance(value, Mapping):
        if {"kind", "object_id", "content_hash"} <= set(value):
            return exact_ref(value, "receipt ref").as_dict()
        return {str(key): _normalize_material(item) for key, item in value.items()}
    if hasattr(value, "as_dict"):
        return _normalize_material(value.as_dict())
    if isinstance(value, (tuple, list)):
        return [_normalize_material(item) for item in value]
    return value


@dataclass(frozen=True)
class NativeCatalog:
    """Capabilities, exact refs and exact owner objects supplied by native owner."""

    catalog_ref: str
    baseline_predicate_ref: Any
    predicate_refs: Mapping[str, Any]
    query_refs: Mapping[str, Any]
    joint_query_refs: Mapping[str, Any]
    marginal_query_refs: Mapping[str, Any]
    supported_claims: tuple[str, ...]
    supported_topologies: tuple[str, ...]
    supported_condition_modes: tuple[str, ...]
    maximum_target_arity: int
    maximum_conditioner_arity: int
    contract_id: str = I05_CONTRACT_ID
    grammar_schema: str = CANDIDATE_GRAMMAR_SCHEMA
    supported_measures: tuple[str, ...] = ("SAMPLE", "POPULATION")
    cell_codec_ref: str = "IDENTITY_TYPED_CELLS"
    cell_codec: Mapping[str, Any] = field(default_factory=dict)
    predicate_objects: Mapping[str, Any] = field(default_factory=dict)
    query_objects: Mapping[str, Any] = field(default_factory=dict)
    discovery_authority_ref: Any | None = None
    batch_unit_refs: tuple[str, ...] = ()
    evidence_grade_ceiling: str = "SOURCEFREE_TEST_ONLY"

    def predicate_ref(self, key: OccurrenceKey, value: Any) -> Any | None:
        return self.predicate_refs.get(_catalog_key(key, value))

    def query_ref(self, targets: Sequence[OccurrenceKey], measure_kind: str) -> Any | None:
        return self.query_refs.get(_target_key(targets) + "|" + measure_kind)

    def joint_query_ref(self, targets: Sequence[OccurrenceKey]) -> Any | None:
        return self.joint_query_refs.get(_target_key(targets))

    def marginal_query_ref(self, target: OccurrenceKey) -> Any | None:
        return self.marginal_query_refs.get(target.key)

    def native_cell(self, value: Any) -> Any:
        key = typed_value_key(value)
        if key in self.cell_codec:
            return self.cell_codec[key]
        return value_material(value)


@dataclass(frozen=True)
class LoweringRecord:
    operation_id: str
    status: str
    reason: str | None
    contract_id: str
    catalog_ref: str
    family: str | None
    form: str | None
    rule_id: str | None
    rule: Mapping[str, Any] | None
    atoms: Mapping[str, Any]
    query_templates: Mapping[str, Any]
    expected_candidate_count: int
    coverage_roles: tuple[str, ...]
    lowering_version: str = LOWERING_VERSION
    discovery_authority_ref: Any | None = None
    batch_unit_refs: tuple[str, ...] = ()
    evidence_grade_ceiling: str = "SOURCEFREE_TEST_ONLY"
    typed_refusal: Mapping[str, Any] | None = None
    predicate_refs: tuple[Mapping[str, str], ...] = ()
    query_refs: tuple[Mapping[str, str], ...] = ()
    query_role_refs: tuple[Mapping[str, Any], ...] = ()
    expected_candidate_keys: tuple[str, ...] = ()
    derived_predicates: Mapping[str, Any] = field(default_factory=dict)

    def material(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id, "status": self.status,
            "reason": self.reason, "contract_id": self.contract_id,
            "catalog_ref": self.catalog_ref, "family": self.family,
            "form": self.form, "rule_id": self.rule_id,
            "rule": canonicalize(self.rule) if self.rule is not None else None,
            "atoms": {key: canonicalize(value) for key, value in sorted(self.atoms.items())},
            "query_templates": {
                key: canonicalize(value) for key, value in sorted(self.query_templates.items())
            },
            "expected_candidate_count": self.expected_candidate_count,
            "coverage_roles": list(self.coverage_roles),
            "lowering_version": self.lowering_version,
            "discovery_authority_ref": _normalize_material(self.discovery_authority_ref),
            "batch_unit_refs": list(self.batch_unit_refs),
            "evidence_grade_ceiling": self.evidence_grade_ceiling,
            "typed_refusal": _normalize_material(self.typed_refusal),
            "predicate_refs": [dict(ref) for ref in self.predicate_refs],
            "query_refs": [dict(ref) for ref in self.query_refs],
            "query_role_refs": [_normalize_material(role) for role in self.query_role_refs],
            "expected_candidate_keys": list(self.expected_candidate_keys),
            "derived_predicate_refs": {
                atom_id: exact_ref(predicate.ref, "derived predicate").as_dict()
                for atom_id, predicate in sorted(self.derived_predicates.items())
            },
        }


def _unsupported(
    operation: ScientificOperation,
    catalog: NativeCatalog,
    reason: str,
    *,
    detail: str | None = None,
) -> LoweringRecord:
    refusal = {
        "code": reason, "operation_id": operation.op_id,
        "contract_id": catalog.contract_id,
        "lowering_version": LOWERING_VERSION,
        "detail": detail,
    }
    return LoweringRecord(
        operation_id=operation.op_id, status=NATIVE_UNSUPPORTED,
        reason=reason, contract_id=catalog.contract_id,
        catalog_ref=catalog.catalog_ref, family=None, form=None,
        rule_id=None, rule=None, atoms={}, query_templates={},
        expected_candidate_count=0, coverage_roles=(),
        discovery_authority_ref=catalog.discovery_authority_ref,
        batch_unit_refs=catalog.batch_unit_refs,
        evidence_grade_ceiling=catalog.evidence_grade_ceiling,
        typed_refusal=refusal,
    )


def _not_eligible(
    operation: ScientificOperation,
    catalog: NativeCatalog,
) -> LoweringRecord:
    refusal = {
        "code": "FRONTIER_NOT_ELIGIBLE",
        "eligibility_state": operation.disposition,
        "execution_state": operation.execution_state,
        "result_state": operation.result_state,
        "operation_id": operation.op_id,
        "lowering_version": LOWERING_VERSION,
    }
    return LoweringRecord(
        operation_id=operation.op_id, status=NOT_ELIGIBLE,
        reason="FRONTIER_ELIGIBILITY_" + operation.disposition,
        contract_id=catalog.contract_id, catalog_ref=catalog.catalog_ref,
        family=None, form=None, rule_id=None, rule=None,
        atoms={}, query_templates={}, expected_candidate_count=0,
        coverage_roles=(), discovery_authority_ref=catalog.discovery_authority_ref,
        batch_unit_refs=catalog.batch_unit_refs,
        evidence_grade_ceiling=catalog.evidence_grade_ceiling,
        typed_refusal=refusal,
    )


def _atom_id(ref: Any) -> str:
    return "ATOM-" + exact_ref(ref, "atom ref").content_hash


def _template_id(ref: Any) -> str:
    return "QT-" + exact_ref(ref, "template ref").content_hash


def _rule_id(operation: ScientificOperation) -> str:
    return "R61-" + operation.canonical_hash


def _base_rule(
    operation: ScientificOperation,
    *,
    family: str,
    form: str,
    baseline_atom_id: str,
    query_template_id: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    rule = {
        "rule_id": _rule_id(operation),
        "family": family,
        "form": form,
        "baseline_atom_id": baseline_atom_id,
        **fields,
    }
    if query_template_id is not None:
        rule["query_template_id"] = query_template_id
    return rule


def _policy_revalidated(
    inventory: SourceInventory,
    policy: GrammarPolicy,
    operation: ScientificOperation,
) -> tuple[bool, str | None]:
    if operation.source_inventory != inventory.inventory_id:
        return False, "OPERATION_INVENTORY_ID_MISMATCH"
    for name in ("source_id", "wave", "edition", "source_sha256", "dataset_id",
                 "instrument_ref", "observation_clock_ref", "reference_clock_ref",
                 "as_of_ref", "publication_clock_ref"):
        if getattr(operation, name) != getattr(inventory, name):
            return False, "OPERATION_SOURCE_IDENTITY_MISMATCH:" + name
    if operation.current_selection_ref != inventory.current_selection:
        return False, "OPERATION_CURRENT_SELECTION_MISMATCH"
    if operation.policy_id != policy.policy_id or operation.policy_hash != policy.content_hash:
        return False, "OPERATION_POLICY_IDENTITY_MISMATCH"
    if operation.policy_grade != policy.grade:
        return False, "OPERATION_POLICY_GRADE_MISMATCH"
    measure = next(
        (plan for plan in inventory.measure_plans if plan.measure_id == operation.measure_id),
        None,
    )
    if measure is None:
        return False, "OPERATION_MEASURE_UNAVAILABLE"
    if (operation.estimand, operation.weight_ref, operation.design_ref,
            operation.variance_policy) != (
                measure.estimand, measure.weight_ref, measure.design_ref,
                measure.variance_policy):
        return False, "OPERATION_MEASURE_IDENTITY_MISMATCH"
    disposition, reasons, risk_refs = role_disposition(
        inventory, policy, targets=operation.targets,
        target_roles=operation.target_roles, conditions=operation.conditions,
        conditioner_roles=operation.conditioner_roles,
        claim_class=operation.claim_class, condition_mode=operation.condition_mode,
        measure=measure, branch_depth=operation.branch_depth,
    )
    if disposition != ELIGIBLE:
        return False, "OPERATION_POLICY_REVALIDATION_" + (
            reasons[0] if reasons else disposition
        )
    by_key = inventory.by_key()
    used = [by_key[key] for key in operation.targets] + [
        by_key[key] for key, _ in operation.conditions
    ]
    expected_target_roles = tuple(item.target_role for item in used[:len(operation.targets)])
    expected_conditioner_roles = tuple(item.conditioner_role for item in used[len(operation.targets):])
    if operation.target_roles != expected_target_roles:
        return False, "FORGED_TARGET_ROLES"
    if operation.conditioner_roles != expected_conditioner_roles:
        return False, "FORGED_CONDITIONER_ROLES"
    if operation.risk_set_refs != risk_refs:
        return False, "FORGED_RISK_SET_IDENTITY"
    if operation.risk_set_ref != (risk_refs[0] if risk_refs else None):
        return False, "FORGED_RISK_SET_REF"
    expected_form_scope = tuple(sorted(set.intersection(
        *(set(item.forms) for item in used)
    )))
    if operation.form_scope != expected_form_scope:
        return False, "FORGED_FORM_SCOPE"
    if operation.unit != used[0].unit:
        return False, "FORGED_UNIT_IDENTITY"
    if operation.topology != used[0].topology:
        return False, "FORGED_TOPOLOGY_IDENTITY"
    if operation.scope != used[0].scope:
        return False, "FORGED_SCOPE_IDENTITY"
    expected_administration = tuple(sorted({item.administration for item in used}))
    if operation.administration_states != expected_administration:
        return False, "FORGED_ADMINISTRATION_STATE"
    grant = policy.direction_for(
        operation.target_roles, operation.conditioner_roles, operation.claim_class
    )
    if grant is None or operation.direction_ref != grant.direction_ref:
        return False, "FORGED_OR_UNAUTHORIZED_DIRECTION_REF"
    return True, None


def _typed_native_cells(
    operation: ScientificOperation,
    inventory: SourceInventory,
    catalog: NativeCatalog,
) -> tuple[tuple[Any, ...] | None, str | None]:
    target = inventory.by_key()[operation.targets[0]]
    mapped: list[Any] = []
    seen: dict[str, str] = {}
    for value in target.domain:
        native = catalog.native_cell(value)
        typed_key = typed_value_key(value)
        native_key = typed_value_key(native)
        if native_key in seen and seen[native_key] != typed_key:
            return None, "NATIVE_CELL_CODEC_NOT_INJECTIVE"
        seen[native_key] = typed_key
        mapped.append(native)
    return tuple(mapped), None


def lower_operation(
    inventory: SourceInventory,
    policy: GrammarPolicy,
    operation: ScientificOperation,
    catalog: NativeCatalog,
) -> LoweringRecord:
    if operation.disposition != ELIGIBLE:
        return _not_eligible(operation, catalog)
    if operation.op_id != "urn:r61:op:" + operation.canonical_hash:
        return _unsupported(operation, catalog, "OPERATION_ID_NOT_CANONICAL")
    if catalog.contract_id != I05_CONTRACT_ID:
        return _unsupported(operation, catalog, "CURRENT_I05_CONTRACT_MISMATCH")
    if catalog.grammar_schema != CANDIDATE_GRAMMAR_SCHEMA:
        return _unsupported(operation, catalog, "CURRENT_I05_GRAMMAR_SCHEMA_MISMATCH")
    valid, refusal = _policy_revalidated(inventory, policy, operation)
    if not valid:
        return _unsupported(operation, catalog, refusal or "OPERATION_POLICY_REVALIDATION_FAILED")
    if operation.claim_class not in catalog.supported_claims:
        return _unsupported(operation, catalog, "CLAIM_CLASS_NOT_IN_CURRENT_CATALOG")
    if operation.topology not in catalog.supported_topologies:
        return _unsupported(operation, catalog, "TOPOLOGY_NOT_IN_CURRENT_CATALOG")
    if operation.condition_mode not in catalog.supported_condition_modes:
        return _unsupported(operation, catalog, "CONDITION_MODE_NOT_IN_CURRENT_CATALOG")
    if operation.measure_kind not in catalog.supported_measures:
        return _unsupported(operation, catalog, "MEASURE_NOT_IN_CURRENT_CATALOG")
    if len(operation.targets) > catalog.maximum_target_arity:
        return _unsupported(operation, catalog, "TARGET_ARITY_EXCEEDS_CURRENT_CATALOG")
    if len(operation.conditions) > catalog.maximum_conditioner_arity:
        return _unsupported(operation, catalog, "CONDITIONER_ARITY_EXCEEDS_CURRENT_CATALOG")
    if operation.claim_class in {"DIST", "CONDITIONAL", "FORK", "INTERACTION"}:
        if operation.state_variant != "COMPLETE_RESPONSE":
            return _unsupported(operation, catalog, "STATE_VARIANT_NOT_IN_CURRENT_CATALOG")

    baseline_ref = catalog.baseline_predicate_ref
    if baseline_ref is None:
        return _unsupported(operation, catalog, "CURRENT_CATALOG_BASELINE_UNAVAILABLE")
    baseline_atom_id = _atom_id(baseline_ref)
    atoms: dict[str, Any] = {baseline_atom_id: _ref_material(baseline_ref)}
    templates: dict[str, Any] = {}

    def condition_atom(key: OccurrenceKey, value: Any) -> str | None:
        ref = catalog.predicate_ref(key, value)
        if ref is None:
            return None
        atom_id = _atom_id(ref)
        atoms[atom_id] = _ref_material(ref)
        return atom_id

    condition_atoms: list[str] = []
    for key, value in operation.conditions:
        atom_id = condition_atom(key, value)
        if atom_id is None:
            return _unsupported(operation, catalog, "CURRENT_CATALOG_PREDICATE_UNAVAILABLE")
        condition_atoms.append(atom_id)

    if operation.claim_class == "DIST":
        query_ref = catalog.query_ref(operation.targets, operation.measure_kind)
        if query_ref is None:
            return _unsupported(operation, catalog, "CURRENT_CATALOG_QUERY_UNAVAILABLE")
        template_id = _template_id(query_ref)
        templates[template_id] = _ref_material(query_ref)
        target_cells, cell_error = _typed_native_cells(operation, inventory, catalog)
        if cell_error is not None:
            return _unsupported(operation, catalog, cell_error)
        rule = _base_rule(
            operation, family="BRANCH_CONDITIONED_DISTRIBUTION", form="BASE_QUERY",
            baseline_atom_id=baseline_atom_id, query_template_id=template_id,
            target_cells=list(target_cells or ()), validation=_TARGET_VALIDATION,
        )
        return _supported_lowering(
            operation, catalog, rule, atoms, templates, len(target_cells or ()), ("BASE",)
        )

    if operation.claim_class in {"CONDITIONAL", "FORK", "INTERACTION"}:
        query_ref = catalog.query_ref(operation.targets, operation.measure_kind)
        if query_ref is None:
            return _unsupported(operation, catalog, "CURRENT_CATALOG_QUERY_UNAVAILABLE")
        template_id = _template_id(query_ref)
        templates[template_id] = _ref_material(query_ref)
        if operation.claim_class == "FORK":
            family = "RECURSIVE_SUBGROUP_FORK"
        elif operation.claim_class == "INTERACTION":
            family = "BOUNDED_K_WAY_RESPONSE_CONFIGURATION"
        else:
            family = "BRANCH_CONDITIONED_DISTRIBUTION"
        if operation.condition_mode == "XOR_EXACTLY_ONE":
            rule = _base_rule(
                operation, family=family, form="XOR_EXACTLY_ONE_COMBINATIONS",
                baseline_atom_id=baseline_atom_id, query_template_id=template_id,
                atom_ids=list(condition_atoms), arity=len(condition_atoms),
                validation=_DIFF_VALIDATION,
            )
        elif len(condition_atoms) == 1:
            rule = _base_rule(
                operation, family=family, form="SINGLE_ATOM",
                baseline_atom_id=baseline_atom_id, query_template_id=template_id,
                atom_ids=list(condition_atoms), validation=_DIFF_VALIDATION,
            )
        else:
            rule = _base_rule(
                operation, family=family, form="AND_CARTESIAN_GROUPS",
                baseline_atom_id=baseline_atom_id, query_template_id=template_id,
                atom_groups=[[atom_id] for atom_id in condition_atoms],
                validation=_DIFF_VALIDATION,
            )
        return _supported_lowering(
            operation, catalog, rule, atoms, templates, 1,
            tuple(["CONDITION"] * len(condition_atoms) + ["BASELINE"]),
        )

    if operation.claim_class in {"JOINT", "CO_TRAVEL"}:
        joint_ref = catalog.joint_query_ref(operation.targets)
        if joint_ref is None:
            return _unsupported(operation, catalog, "CURRENT_CATALOG_JOINT_QUERY_UNAVAILABLE")
        joint_id = _template_id(joint_ref)
        templates[joint_id] = _ref_material(joint_ref)
        marginal_ids: list[str] = []
        for target in operation.targets:
            marginal_ref = catalog.marginal_query_ref(target)
            if marginal_ref is None:
                return _unsupported(operation, catalog, "CURRENT_CATALOG_MARGINAL_QUERY_UNAVAILABLE")
            marginal_id = _template_id(marginal_ref)
            templates[marginal_id] = _ref_material(marginal_ref)
            marginal_ids.append(marginal_id)
        joint_baseline_atom_id = baseline_atom_id
        derived_predicates: dict[str, Any] = {}
        condition_atom_ids: list[str] = []
        if operation.conditions:
            condition_objects = []
            for key, value in operation.conditions:
                ref = catalog.predicate_ref(key, value)
                if ref is None:
                    return _unsupported(operation, catalog, "CURRENT_CATALOG_PREDICATE_UNAVAILABLE")
                obj = catalog.predicate_objects.get(exact_ref(ref, "condition predicate").key)
                if obj is None:
                    return _unsupported(
                        operation, catalog, "CURRENT_CATALOG_PREDICATE_OBJECT_UNAVAILABLE"
                    )
                condition_objects.append(obj)
                atom_id = _atom_id(ref)
                atoms[atom_id] = _ref_material(ref)
                condition_atom_ids.append(atom_id)
            tag_material = {
                "rule": _rule_id(operation), "operation": operation.op_id,
                "conditions": [
                    {"key": key.key, "value": typed_value_key(value)}
                    for key, value in operation.conditions
                ],
            }
            if operation.condition_mode == "XOR_EXACTLY_ONE":
                derived = _xor_exactly_one(condition_objects, tag_material=tag_material)
            elif len(condition_objects) == 1:
                derived = condition_objects[0]
            else:
                derived = _combine_predicates(
                    condition_objects, op="AND", tag_material=tag_material
                )
            derived_id = _atom_id(derived.ref)
            atoms[derived_id] = _ref_material(derived.ref)
            derived_predicates[derived_id] = derived
            joint_baseline_atom_id = derived_id
        rule = _base_rule(
            operation, family="PAIR_RESPONSE_COTRAVEL", form="JOINT_DEPENDENCE",
            baseline_atom_id=joint_baseline_atom_id, joint_template_id=joint_id,
            marginal_template_ids=marginal_ids, validation=_JOINT_VALIDATION,
            condition_atom_ids=condition_atom_ids,
        )
        return _supported_lowering(
            operation, catalog, rule, atoms, templates, 1,
            tuple(["JOINT"] + [f"MARGINAL_{index}" for index in range(len(marginal_ids))]),
            derived_predicates=derived_predicates,
        )

    return _unsupported(operation, catalog, "CLAIM_CLASS_NOT_LOWERABLE_TO_CURRENT_I05")


def _supported_lowering(
    operation: ScientificOperation,
    catalog: NativeCatalog,
    rule: Mapping[str, Any],
    atoms: Mapping[str, Any],
    templates: Mapping[str, Any],
    expected_candidate_count: int,
    coverage_roles: tuple[str, ...],
    derived_predicates: Mapping[str, Any] | None = None,
) -> LoweringRecord:
    family = str(rule["family"])
    form = str(rule["form"])
    if family not in CANDIDATE_FAMILIES:
        return _unsupported(operation, catalog, "FAMILY_NOT_IN_IMPORTED_CURRENT_CONTRACT")
    if form not in PREDICATE_FORMS:
        return _unsupported(operation, catalog, "FORM_NOT_IN_IMPORTED_CURRENT_CONTRACT")
    validation = rule.get("validation")
    if not isinstance(validation, Mapping) or validation.get("kind") not in VALIDATION_KINDS:
        return _unsupported(operation, catalog, "VALIDATION_NOT_IN_IMPORTED_CURRENT_CONTRACT")
    return LoweringRecord(
        operation_id=operation.op_id, status=SUPPORTED, reason=None,
        contract_id=catalog.contract_id, catalog_ref=catalog.catalog_ref,
        family=family, form=form, rule_id=str(rule["rule_id"]), rule=rule,
        atoms=dict(atoms), query_templates=dict(templates),
        expected_candidate_count=expected_candidate_count,
        coverage_roles=coverage_roles,
        discovery_authority_ref=catalog.discovery_authority_ref,
        batch_unit_refs=catalog.batch_unit_refs,
        evidence_grade_ceiling=catalog.evidence_grade_ceiling,
        predicate_refs=tuple(
            {"role": atom_id, **exact_ref(ref, "atom ref").as_dict()}
            for atom_id, ref in sorted(atoms.items())
        ),
        query_refs=tuple(
            {"role": template_id, **exact_ref(ref, "template ref").as_dict()}
            for template_id, ref in sorted(templates.items())
        ),
        derived_predicates=dict(derived_predicates or {}),
    )


@dataclass(frozen=True)
class LoweringPlan:
    records: tuple[LoweringRecord, ...]
    supported_operation_ids: tuple[str, ...]
    unsupported_operation_ids: tuple[str, ...]
    not_eligible_operation_ids: tuple[str, ...]
    contract_id: str
    grammar_schema: str
    maximum_bounds: Mapping[str, int]
    expected_candidates: tuple[Mapping[str, Any], ...] = ()
    expected_candidate_error: str | None = None
    allow_empty_frontier: bool = False

    def material(self) -> dict[str, Any]:
        return {
            "records": [record.material() for record in self.records],
            "supported_operation_ids": list(self.supported_operation_ids),
            "unsupported_operation_ids": list(self.unsupported_operation_ids),
            "not_eligible_operation_ids": list(self.not_eligible_operation_ids),
            "contract_id": self.contract_id,
            "grammar_schema": self.grammar_schema,
            "maximum_bounds": dict(self.maximum_bounds),
            "expected_candidates": [canonicalize(candidate) for candidate in self.expected_candidates],
            "expected_candidate_error": self.expected_candidate_error,
            "allow_empty_frontier": self.allow_empty_frontier,
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.material())

    def coverage_report(self) -> dict[str, Any]:
        supported = set(self.supported_operation_ids)
        unsupported = set(self.unsupported_operation_ids)
        not_eligible = set(self.not_eligible_operation_ids)
        all_ids = supported | unsupported | not_eligible
        total = len(self.records)
        return {
            "record_count": total,
            "supported_count": len(supported),
            "unsupported_count": len(unsupported),
            "not_eligible_count": len(not_eligible),
            "disjoint_partition": (
                len(all_ids) == total
                and not (supported & unsupported)
                and not (supported & not_eligible)
                and not (unsupported & not_eligible)
            ),
            "unsupported_are_typed": all(
                record.typed_refusal is not None
                for record in self.records if record.status == NATIVE_UNSUPPORTED
            ),
            "expected_candidate_error": self.expected_candidate_error,
            "expected_candidate_count": len(self.expected_candidates),
            "no_drop_ok": len(all_ids) == total,
        }

    def native_grammar(self) -> dict[str, Any]:
        atoms: dict[str, Any] = {}
        templates: dict[str, Any] = {}
        rules: list[dict[str, Any]] = []
        for record in self.records:
            if record.status != SUPPORTED:
                continue
            atoms.update(record.atoms)
            templates.update(record.query_templates)
            rules.append(dict(record.rule or {}))
        return {
            "schema": CANDIDATE_GRAMMAR_SCHEMA,
            "discovery_operation": "I03-OP-UNIVERSAL-SEMANTIC-LOWERING",
            "atoms": tuple(
                {"atom_id": atom_id, "predicate_ref": ref, "kind": "RESPONSE"}
                for atom_id, ref in sorted(atoms.items())
            ),
            "query_templates": tuple(
                {"template_id": template_id, "query_ref": ref}
                for template_id, ref in sorted(templates.items())
            ),
            "rules": tuple(sorted(rules, key=lambda rule: rule["rule_id"])),
            "limits": {
                "maximum_conditioner_arity_K": int(self.maximum_bounds["K"]),
                "maximum_target_arity_J": int(self.maximum_bounds["J"]),
            },
            "allow_empty_frontier": self.allow_empty_frontier,
        }

    def expected_native_catalog(self) -> dict[str, int]:
        return {
            record.rule_id: record.expected_candidate_count
            for record in self.records
            if record.status == SUPPORTED and record.rule_id is not None
        }


def _compute_expected_candidates(
    plan: LoweringPlan,
    catalog: NativeCatalog,
) -> tuple[tuple[Mapping[str, Any], ...], str | None]:
    grammar = plan.native_grammar()
    missing_objects: list[str] = []
    derived_by_atom: dict[str, Any] = {}
    for record in plan.records:
        derived_by_atom.update(record.derived_predicates)
    atoms: dict[str, _Atom] = {}
    for item in grammar["atoms"]:
        ref = exact_ref(item["predicate_ref"], "expected atom ref")
        obj = derived_by_atom.get(item["atom_id"]) or catalog.predicate_objects.get(ref.key)
        if obj is None:
            missing_objects.append(f"PREDICATE:{ref.key}")
            continue
        atoms[item["atom_id"]] = _Atom(
            item["atom_id"], str(item.get("kind", "RESPONSE")), obj, ()
        )
    templates: dict[str, _Template] = {}
    for item in grammar["query_templates"]:
        ref = exact_ref(item["query_ref"], "expected template ref")
        obj = catalog.query_objects.get(ref.key)
        if obj is None:
            missing_objects.append(f"QUERY:{ref.key}")
            continue
        templates[item["template_id"]] = _Template(item["template_id"], obj)
    if missing_objects:
        return (), "CURRENT_CATALOG_OBJECTS_UNAVAILABLE:" + ",".join(sorted(missing_objects))
    candidates = _compile_frontier(grammar, atoms, templates)
    return tuple({
        "candidate_id": candidate.candidate_id,
        "candidate_hash": candidate.candidate_hash,
        "family": candidate.family,
        "rule_id": candidate.rule_id,
        "winning_predicate_ref": candidate.winning_predicate.ref.as_dict(),
        "query_roles": [
            {
                "role": role.role,
                "predicate_ref": role.predicate.ref.as_dict(),
                "query_ref": role.query.ref.as_dict(),
            }
            for role in candidate.query_roles
        ],
        "validation": canonicalize(candidate.validation),
        "ancestry_refs": [ref.as_dict() for ref in candidate.ancestry_refs],
    } for candidate in candidates), None


def lower_frontier(
    inventory: SourceInventory,
    policy: GrammarPolicy,
    frontier: ScientificFrontier,
    catalog: NativeCatalog,
) -> LoweringPlan:
    records = tuple(
        lower_operation(inventory, policy, operation, catalog)
        for operation in frontier.operations
    )
    plan = LoweringPlan(
        records=records,
        supported_operation_ids=tuple(
            sorted(record.operation_id for record in records if record.status == SUPPORTED)
        ),
        unsupported_operation_ids=tuple(
            sorted(record.operation_id for record in records if record.status == NATIVE_UNSUPPORTED)
        ),
        not_eligible_operation_ids=tuple(
            sorted(record.operation_id for record in records if record.status == NOT_ELIGIBLE)
        ),
        contract_id=catalog.contract_id,
        grammar_schema=catalog.grammar_schema,
        maximum_bounds=dict(policy.bounds),
    )
    expected, error = _compute_expected_candidates(plan, catalog)
    expected_by_rule: dict[str, list[Mapping[str, Any]]] = {}
    for candidate in expected:
        expected_by_rule.setdefault(str(candidate["rule_id"]), []).append(candidate)
    enriched_records = []
    for record in records:
        candidates = expected_by_rule.get(record.rule_id or "", [])
        role_refs: list[Mapping[str, Any]] = []
        seen_roles: set[str] = set()
        for candidate in candidates:
            for role in candidate["query_roles"]:
                role_key = json.dumps(role, sort_keys=True)
                if role_key not in seen_roles:
                    seen_roles.add(role_key)
                    role_refs.append(role)
        enriched_records.append(replace(
            record,
            expected_candidate_keys=tuple(
                sorted(str(candidate["candidate_id"]) for candidate in candidates)
            ),
            query_role_refs=tuple(role_refs),
        ))
    plan = replace(plan, records=tuple(enriched_records))
    return LoweringPlan(
        **{
            **{name: getattr(plan, name) for name in plan.__dataclass_fields__},
            "expected_candidates": expected,
            "expected_candidate_error": error,
            "allow_empty_frontier": (
                not frontier.operations and not plan.unsupported_operation_ids
            ),
        }
    )


def _actual_candidate_material(receipt: Any) -> dict[str, Any]:
    identity = receipt.candidate_identity
    if not isinstance(identity, Mapping):
        raise ValueError("receipt candidate_identity must be a mapping")
    required = (
        "candidate_id", "candidate_hash", "family", "rule_id",
        "query_roles", "validation",
    )
    missing = [name for name in required if name not in identity]
    if missing:
        raise ValueError("receipt candidate identity lacks " + ",".join(missing))
    winning = identity.get("winning_predicate_ref")
    if winning is None:
        winning = getattr(receipt, "winning_predicate_ref", None)
    if winning is None:
        raise ValueError("receipt lacks exact winning predicate ref")
    ancestry = identity.get("ancestry_refs")
    if ancestry is None:
        ancestry = getattr(receipt, "branch_or_parent_ancestry_refs", ())
    return _normalize_material({
        **{name: identity[name] for name in required},
        "winning_predicate_ref": winning,
        "ancestry_refs": ancestry,
    })


def native_receipt_anti_join(plan: LoweringPlan, receipts: Sequence[Any]) -> dict[str, Any]:
    """Anti-join actual I05 receipts by exact candidate/query-role semantics."""

    if plan.expected_candidate_error is not None:
        raise ValueError(plan.expected_candidate_error)
    if not plan.expected_candidates and plan.supported_operation_ids:
        raise ValueError("EXPECTED_CANDIDATES_NOT_COMPUTED")
    expected_by_id = {candidate["candidate_id"]: candidate for candidate in plan.expected_candidates}
    if len(expected_by_id) != len(plan.expected_candidates):
        raise ValueError("EXPECTED_CANDIDATE_ID_DUPLICATE")
    actual_by_id: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    semantic_mismatches: list[dict[str, Any]] = []
    actual_rule_counts: dict[str, int] = {}
    for receipt in receipts:
        material = _actual_candidate_material(receipt)
        candidate_id = material["candidate_id"]
        actual_rule_counts[material["rule_id"]] = actual_rule_counts.get(material["rule_id"], 0) + 1
        if candidate_id in actual_by_id:
            duplicates.append(candidate_id)
            continue
        actual_by_id[candidate_id] = material
        expected = expected_by_id.get(candidate_id)
        if expected is not None and canonicalize(expected) != canonicalize(material):
            semantic_mismatches.append({
                "candidate_id": candidate_id,
                "expected": canonicalize(expected),
                "actual": canonicalize(material),
            })
    expected_ids = set(expected_by_id)
    actual_ids = set(actual_by_id)
    missing = tuple(sorted(expected_ids - actual_ids))
    unexpected = tuple(sorted(actual_ids - expected_ids))
    expected_rule_counts = plan.expected_native_catalog()
    missing_rules = tuple(sorted(set(expected_rule_counts) - set(actual_rule_counts)))
    unexpected_rules = tuple(sorted(set(actual_rule_counts) - set(expected_rule_counts)))
    count_mismatches = {
        rule_id: {"expected": expected_rule_counts[rule_id], "actual": actual_rule_counts[rule_id]}
        for rule_id in sorted(set(expected_rule_counts) & set(actual_rule_counts))
        if expected_rule_counts[rule_id] != actual_rule_counts[rule_id]
    }
    no_drop = (
        not missing and not unexpected and not duplicates and not semantic_mismatches
        and not missing_rules and not unexpected_rules and not count_mismatches
        and len(actual_by_id) == len(expected_by_id)
    )
    return {
        "expected_rule_count": len(expected_rule_counts),
        "actual_rule_count": len(actual_rule_counts),
        "expected_candidate_count": len(expected_by_id),
        "actual_candidate_count": len(actual_by_id),
        "missing_rule_ids": missing_rules,
        "unexpected_rule_ids": unexpected_rules,
        "count_mismatches": count_mismatches,
        "missing_candidate_ids": missing,
        "unexpected_candidate_ids": unexpected,
        "duplicate_candidate_ids": tuple(sorted(duplicates)),
        "semantic_mismatches": semantic_mismatches,
        "no_drop_ok": no_drop,
    }


RECURRENCE_POLICY_SCHEMA = "RecurrencePolicy@r61.r4.1"
RECURRENCE_PLAN_SCHEMA = "RecurrenceIssuePlan@r61.r4.1"
RECURRENCE_GENERATION_SCHEMA = "RecurrenceGeneration@r61.r4.1"
COMPARATOR_ROOT = "ROOT_RELATIVE"
COMPARATOR_PARENT = "IMMEDIATE_PARENT_RELATIVE"
PARENT_ROOT = "ROOT"
PARENT_RECEIPT_BOUND = "RECEIPT_BOUND"
PARENT_EXPLORATORY = "EXPLORATORY_PREDICATE"
RECURRENCE_COUNTING_CONVENTION = "ANCESTOR_CONDITIONS_COUNT_TOWARD_K"
RECURRENCE_ISSUED = "ISSUED"
RECURRENCE_STOPPED_BUDGET = "STOPPED_BUDGET"


class RecurrenceRefusal(ValueError):
    """Typed recurrence identity/lineage/accounting refusal."""


@dataclass(frozen=True)
class RecurrencePolicy:
    policy_id: str
    policy_version: str
    grade: str
    owner_refs: tuple[str, ...]
    counting_convention: str
    bounds: Mapping[str, int]
    breadth_cap: int
    followup_cap: int
    protected_exploration_slots: int
    per_generation_issued_cap: int
    total_issued_cap: int
    comparators: tuple[str, ...]
    complement_policy: str = "OPTIONAL_NOT_MANDATORY"
    sourcefree_test_only: bool = True
    schema: str = RECURRENCE_POLICY_SCHEMA

    def __post_init__(self) -> None:
        if self.schema != RECURRENCE_POLICY_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_RECURRENCE_POLICY:{self.schema}")
        if self.grade != "TEST_ONLY":
            raise ValueError("RECURRENCE_POLICY_GRADE_MUST_BE_TEST_ONLY")
        if self.counting_convention != RECURRENCE_COUNTING_CONVENTION:
            raise ValueError("UNSUPPORTED_RECURRENCE_COUNTING_CONVENTION")
        for name in ("breadth_cap", "followup_cap", "protected_exploration_slots",
                     "per_generation_issued_cap", "total_issued_cap"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"{name} must be nonnegative integer")
        if not isinstance(self.bounds, Mapping):
            raise TypeError("bounds must be mapping")
        normalized = {}
        for name in ("J", "K", "D"):
            value = self.bounds.get(name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError(f"BOUND_{name}_MUST_BE_POSITIVE_INTEGER")
            normalized[name] = value
        object.__setattr__(self, "bounds", normalized)
        if self.comparators != (COMPARATOR_ROOT, COMPARATOR_PARENT):
            raise ValueError("RECURRENCE_REQUIRES_ROOT_AND_PARENT_COMPARATORS")

    @property
    def content_hash(self) -> str:
        return semantic_hash(canonicalize({
            name: getattr(self, name) for name in self.__dataclass_fields__
        }))

    def material(self) -> dict[str, Any]:
        return canonicalize({
            name: getattr(self, name) for name in self.__dataclass_fields__
        })


@dataclass(frozen=True)
class RecurrenceParent:
    parent_id: str
    predicate: Any
    kind: str
    generation: int
    source_release_refs: tuple[Any, ...]
    ancestry_conditions: tuple[tuple[OccurrenceKey, Any], ...] = ()
    ancestry_predicates: tuple[Any, ...] = ()
    receipt_ref: Any | None = None
    replay_binding_ref: Any | None = None
    handoff: RecursiveBranchHandoff | None = None
    activation_reason: str = "ROOT"
    construction_ref: str | None = None

    def __post_init__(self) -> None:
        if self.kind not in {PARENT_ROOT, PARENT_RECEIPT_BOUND, PARENT_EXPLORATORY}:
            raise ValueError(f"UNKNOWN_RECURRENCE_PARENT_KIND:{self.kind}")
        if self.kind == PARENT_ROOT and self.generation != 0:
            raise ValueError("root parent must be generation 0")
        if self.kind == PARENT_EXPLORATORY and self.receipt_ref is not None:
            raise ValueError("exploratory parent may not claim a winner receipt")
        if len(self.ancestry_conditions) != len(self.ancestry_predicates):
            raise ValueError("ancestry condition/predicate length mismatch")

    @property
    def predicate_ref(self):
        return self.predicate.ref

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "parent_id": self.parent_id, "predicate_ref": self.predicate.ref,
            "kind": self.kind, "generation": self.generation,
            "source_release_refs": self.source_release_refs,
            "ancestry_conditions": [
                {"key": key.material(), "value": value_material(value)}
                for key, value in self.ancestry_conditions
            ],
            "ancestry_predicate_refs": [p.ref for p in self.ancestry_predicates],
            "receipt_ref": self.receipt_ref,
            "replay_binding_ref": self.replay_binding_ref,
            "activation_reason": self.activation_reason,
            "construction_ref": self.construction_ref,
        })


@dataclass(frozen=True)
class RecurrenceParentResolver:
    """Trusted coordinator catalog of canonical recursive handoffs."""

    handoffs: tuple[RecursiveBranchHandoff, ...]
    bundle_ref: Any | None = None

    def __post_init__(self) -> None:
        ordered = tuple(sorted(self.handoffs, key=lambda handoff: handoff.ref.key))
        if len({handoff.ref.key for handoff in ordered}) != len(ordered):
            raise RecurrenceRefusal("DUPLICATE_RESOLVER_HANDOFF")
        object.__setattr__(self, "handoffs", ordered)

    def resolve(self, ref: Any) -> RecursiveBranchHandoff:
        target = exact_ref(ref, "parent replay binding ref")
        matches = [handoff for handoff in self.handoffs if handoff.ref == target]
        if len(matches) != 1:
            raise RecurrenceRefusal("PARENT_REPLAY_BINDING_NOT_RESOLVED")
        return matches[0]


def make_recurrence_parent_resolver(
    handoffs: Sequence[RecursiveBranchHandoff], *, bundle_ref: Any | None = None
) -> RecurrenceParentResolver:
    return RecurrenceParentResolver(tuple(handoffs), bundle_ref=bundle_ref)


def load_recurrence_parent_resolver(path: str | Path) -> RecurrenceParentResolver:
    bundle_ref, handoffs = load_recursive_handoff_bundle(path)
    return RecurrenceParentResolver(handoffs, bundle_ref=bundle_ref)


def _validate_parent_resolution(
    parent: RecurrenceParent,
    resolver: RecurrenceParentResolver | None,
    release_refs: Sequence[Any],
) -> RecurrenceParent:
    if parent.kind == PARENT_ROOT:
        if parent.generation != 0 or parent.receipt_ref is not None or parent.handoff is not None:
            raise RecurrenceRefusal("ROOT_PARENT_IDENTITY_INVALID")
        return parent
    if parent.kind == PARENT_EXPLORATORY:
        if parent.receipt_ref is not None or parent.replay_binding_ref is not None or parent.handoff is not None:
            raise RecurrenceRefusal("EXPLORATORY_PARENT_MAY_NOT_CLAIM_WINNER_RECEIPT")
        if not parent.construction_ref:
            raise RecurrenceRefusal("EXPLORATORY_PARENT_CONSTRUCTION_REF_MISSING")
        return parent
    if resolver is None:
        raise RecurrenceRefusal("PARENT_RESOLVER_REQUIRED")
    if parent.receipt_ref is None or parent.replay_binding_ref is None or parent.handoff is None:
        raise RecurrenceRefusal("RECEIPT_BOUND_PARENT_BINDING_MISSING")
    handoff = resolver.resolve(parent.replay_binding_ref)
    if parent.handoff.ref != handoff.ref:
        raise RecurrenceRefusal("PARENT_HANDOFF_RESOLUTION_MISMATCH")
    if handoff.receipt_ref != exact_ref(parent.receipt_ref, "parent receipt ref"):
        raise RecurrenceRefusal("PARENT_RECEIPT_REF_MISMATCH")
    if handoff.winning_predicate.ref != parent.predicate.ref:
        raise RecurrenceRefusal("PARENT_PREDICATE_HANDOFF_MISMATCH")
    if handoff.winning_predicate.content_hash != parent.predicate.content_hash:
        raise RecurrenceRefusal("PARENT_PREDICATE_HASH_MISMATCH")
    if tuple(sorted(handoff.source_release_refs, key=lambda ref: ref.key)) != tuple(sorted(
        (exact_ref(ref, "parent source release ref") for ref in parent.source_release_refs),
        key=lambda ref: ref.key,
    )):
        raise RecurrenceRefusal("PARENT_SOURCE_RELEASE_HANDOFF_MISMATCH")
    execution_releases = tuple(sorted(
        (exact_ref(ref, "execution release ref") for ref in release_refs),
        key=lambda ref: ref.key,
    ))
    if tuple(sorted(handoff.source_release_refs, key=lambda ref: ref.key)) != execution_releases:
        raise RecurrenceRefusal("PARENT_SOURCE_RELEASE_EXECUTION_MISMATCH")
    expected_id = _parent_id(
        PARENT_RECEIPT_BOUND, handoff.winning_predicate, parent.generation,
        {
            "receipt": exact_ref(parent.receipt_ref, "parent receipt ref"),
            "handoff": handoff.ref,
            "conditions": [
                {"key": key.material(), "value": value_material(value)}
                for key, value in parent.ancestry_conditions
            ],
            "predicates": [p.ref for p in parent.ancestry_predicates],
        },
    )
    if parent.parent_id != expected_id:
        raise RecurrenceRefusal("PARENT_CANONICAL_ID_MISMATCH")
    return RecurrenceParent(
        **{
            **{name: getattr(parent, name) for name in parent.__dataclass_fields__},
            "predicate": handoff.winning_predicate,
            "handoff": handoff,
            "receipt_ref": handoff.receipt_ref,
            "replay_binding_ref": handoff.ref,
            "source_release_refs": tuple(handoff.source_release_refs),
        }
    )


def _parent_id(kind: str, predicate: Any, generation: int, ancestry_refs: Any) -> str:
    return "urn:r61:recurrence:parent:" + semantic_hash(canonicalize({
        "kind": kind, "predicate_ref": predicate.ref,
        "generation": generation, "ancestry": ancestry_refs,
    }))


def make_root_parent(*, predicate: Any, source_release_refs: Sequence[Any]) -> RecurrenceParent:
    return RecurrenceParent(
        parent_id=_parent_id(PARENT_ROOT, predicate, 0, ()),
        predicate=predicate, kind=PARENT_ROOT, generation=0,
        source_release_refs=tuple(source_release_refs),
        activation_reason="SOURCE_ROOT",
    )


@dataclass(frozen=True)
class RecurrenceExpectedOperation:
    operation_id: str
    generation: int
    parent_id: str
    comparator: str
    rule_id: str
    condition_keys: tuple[OccurrenceKey, ...]
    condition_values: tuple[Any, ...]
    baseline_predicate_ref: Mapping[str, str]
    expected_candidate_count: int = 1

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "operation_id": self.operation_id, "generation": self.generation,
            "parent_id": self.parent_id, "comparator": self.comparator,
            "rule_id": self.rule_id,
            "condition_keys": [key.material() for key in self.condition_keys],
            "condition_values": [value_material(value) for value in self.condition_values],
            "baseline_predicate_ref": self.baseline_predicate_ref,
            "expected_candidate_count": self.expected_candidate_count,
        })


@dataclass(frozen=True)
class RecurrenceIssuePlan:
    generation: int
    policy: RecurrencePolicy
    grammar: Mapping[str, Any]
    expected_operations: tuple[RecurrenceExpectedOperation, ...]
    parents: tuple[RecurrenceParent, ...]
    condition_predicates: tuple[Any, ...]
    target_label: str
    query_ref: Mapping[str, str]
    unissued: tuple[Mapping[str, Any], ...] = ()
    query_object: Any = None
    predecessor_plan_ref: str | None = None
    predecessor_issued_count: int = 0
    cumulative_issued_count: int = 0
    root_predicate_ref: Mapping[str, str] | None = None
    state: str = RECURRENCE_ISSUED
    schema: str = RECURRENCE_PLAN_SCHEMA

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "schema": self.schema, "generation": self.generation,
            "policy_id": self.policy.policy_id, "policy_hash": self.policy.content_hash,
            "grammar": self.grammar,
            "expected_operations": [op.material() for op in self.expected_operations],
            "parents": [parent.material() for parent in self.parents],
            "condition_predicate_refs": [item[2].ref for item in self.condition_predicates],
            "condition_entries": [
                {"key": item[0].material(), "value": value_material(item[1]),
                 "predicate_ref": item[2].ref}
                for item in self.condition_predicates
            ],
            "target_label": self.target_label,
            "query_ref": self.query_ref,
            "unissued": list(self.unissued),
            "predecessor_plan_ref": self.predecessor_plan_ref,
            "predecessor_issued_count": self.predecessor_issued_count,
            "cumulative_issued_count": self.cumulative_issued_count,
            "root_predicate_ref": self.root_predicate_ref,
            "state": self.state,
        })

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.material())


def _recurrence_rule_id(material: Any) -> str:
    return "R64-" + semantic_hash(canonicalize(material))


def build_recurrence_issue_plan(
    *,
    policy: RecurrencePolicy,
    generation: int,
    parents: Sequence[RecurrenceParent],
    root_predicate: Any,
    target_label: str,
    query_ref: Any,
    condition_predicates: Sequence[tuple[OccurrenceKey, Any, Any]],
    previous_plan: RecurrenceIssuePlan | None = None,
    parent_resolver: RecurrenceParentResolver | None = None,
    release_refs: Sequence[Any] | None = None,
    total_issued_before: int | None = None,
) -> RecurrenceIssuePlan:
    """Freeze one finite generation's exact grammar and expected operation IDs."""

    if generation < 1 or generation > int(policy.bounds["D"]):
        raise RecurrenceRefusal("RECURRENCE_GENERATION_OUTSIDE_ISSUED_D")
    if total_issued_before is not None:
        raise RecurrenceRefusal("UNBOUND_TOTAL_ISSUED_BEFORE_REFUSED")
    if not parents:
        raise RecurrenceRefusal("RECURRENCE_REQUIRES_ACTIVE_PARENT")
    if not condition_predicates:
        raise RecurrenceRefusal("RECURRENCE_REQUIRES_NEXT_CONDITION")
    parent_ids = [parent.parent_id for parent in parents]
    if len(set(parent_ids)) != len(parent_ids):
        raise RecurrenceRefusal("DUPLICATE_PARENT_IDENTITY")
    if generation == 1:
        if len(parents) != 1 or parents[0].kind != PARENT_ROOT or parents[0].generation != 0:
            raise RecurrenceRefusal("GENERATION_ONE_REQUIRES_SINGLE_ROOT_PARENT")
        if parents[0].predicate.ref != root_predicate.ref:
            raise RecurrenceRefusal("ROOT_PARENT_PREDICATE_MISMATCH")
        if release_refs is not None and tuple(sorted(
            (exact_ref(ref, "root release") for ref in parents[0].source_release_refs),
            key=lambda ref: ref.key,
        )) != tuple(sorted(
            (exact_ref(ref, "root release") for ref in release_refs),
            key=lambda ref: ref.key,
        )):
            raise RecurrenceRefusal("ROOT_PARENT_SOURCE_RELEASE_MISMATCH")
    else:
        if any(parent.kind == PARENT_ROOT for parent in parents):
            raise RecurrenceRefusal("ROOT_PARENT_NOT_ALLOWED_AFTER_GENERATION_ONE")
        if any(parent.generation != generation - 1 for parent in parents):
            raise RecurrenceRefusal("PARENT_GENERATION_CONTINUITY_VIOLATION")
        if previous_plan is None:
            raise RecurrenceRefusal("PREDECESSOR_PLAN_REQUIRED")
    # Chronological predecessor and discovery ancestry are independent.
    issued_before = 0
    predecessor_ref = None
    if previous_plan is not None:
        if previous_plan.policy.content_hash != policy.content_hash:
            raise RecurrenceRefusal("PREDECESSOR_PLAN_POLICY_MISMATCH")
        root_ref = exact_ref(root_predicate.ref, "root predicate").as_dict()
        if previous_plan.root_predicate_ref != root_ref:
            raise RecurrenceRefusal("PREDECESSOR_PLAN_ROOT_MISMATCH")
        if previous_plan.state not in {RECURRENCE_ISSUED, RECURRENCE_STOPPED_BUDGET}:
            raise RecurrenceRefusal("PREDECESSOR_PLAN_NOT_ISSUED")
        if previous_plan.cumulative_issued_count != (
            previous_plan.predecessor_issued_count + len(previous_plan.expected_operations)
        ):
            raise RecurrenceRefusal("PREDECESSOR_PLAN_ISSUED_COUNT_INCONSISTENT")
        issued_before = previous_plan.cumulative_issued_count
        predecessor_ref = previous_plan.content_hash
    canonical_parents = tuple(
        _validate_parent_resolution(
            parent, parent_resolver, release_refs or ()
        )
        for parent in parents
    )
    remaining_total = max(0, policy.total_issued_cap - issued_before)
    if remaining_total == 0 or policy.per_generation_issued_cap == 0:
        return RecurrenceIssuePlan(
            generation=generation, policy=policy,
            grammar={"schema": CANDIDATE_GRAMMAR_SCHEMA, "atoms": (),
                     "query_templates": (), "rules": (),
                     "limits": {"maximum_conditioner_arity_K": int(policy.bounds["K"]),
                                "maximum_target_arity_J": int(policy.bounds["J"])},
                     "allow_empty_frontier": False},
            expected_operations=(), parents=canonical_parents,
            condition_predicates=tuple(condition_predicates),
            target_label=target_label,
            query_ref=_ref_material(getattr(query_ref, "ref", query_ref)),
            unissued=tuple({
                "parent_id": parent.parent_id,
                "reason": ("TOTAL_ISSUED_CAP" if remaining_total == 0 else "PER_GENERATION_ISSUED_CAP"),
                "state": RECURRENCE_STOPPED_BUDGET,
            } for parent in canonical_parents),
            query_object=query_ref if hasattr(query_ref, "ref") else None,
            predecessor_plan_ref=predecessor_ref,
            predecessor_issued_count=issued_before,
            cumulative_issued_count=issued_before,
            root_predicate_ref=exact_ref(root_predicate.ref, "root predicate").as_dict(),
            state=RECURRENCE_STOPPED_BUDGET,
        )
    issued_cap = min(policy.per_generation_issued_cap, remaining_total)
    query_ref_object = getattr(query_ref, "ref", query_ref)
    query_material = _ref_material(query_ref_object)
    atoms: dict[str, Any] = {}
    templates: dict[str, Any] = {}
    rules: list[dict[str, Any]] = []
    expected: list[RecurrenceExpectedOperation] = []
    unissued: list[Mapping[str, Any]] = []

    def atom_for(predicate: Any, kind: str, ancestry: Sequence[Any] = ()) -> str:
        atom_id = _atom_id(predicate.ref)
        atoms[atom_id] = {
            "atom_id": atom_id, "predicate_ref": predicate.ref,
            "kind": kind, "ancestry_refs": tuple(ancestry),
        }
        return atom_id

    root_atom = atom_for(root_predicate, "BRANCH", ())
    template_id = _template_id(query_ref_object)
    templates[template_id] = {"template_id": template_id, "query_ref": query_ref_object}
    seen_condition_refs: set[str] = set()
    for key, value, predicate in condition_predicates:
        if predicate.ref.key in seen_condition_refs:
            raise RecurrenceRefusal("RECURRENCE_DUPLICATE_CONDITION_PREDICATE")
        seen_condition_refs.add(predicate.ref.key)
        atom_for(predicate, "RESPONSE")
    issued_so_far = 0
    for parent in canonical_parents:
        for condition_key, condition_value, condition_predicate in condition_predicates:
            all_conditions = parent.ancestry_conditions + ((condition_key, condition_value),)
            if len({key.item_id for key, _ in all_conditions}) != len(all_conditions):
                raise ValueError("RECURRENCE_ANCESTOR_CONDITIONS_EXCEED_OR_REPEAT_K")
            if len(all_conditions) > int(policy.bounds["K"]):
                raise ValueError("RECURRENCE_ANCESTOR_CONDITIONS_EXCEED_K")
            parent_atom = atom_for(parent.predicate, "BRANCH", (parent.predicate_ref,))
            for comparator in policy.comparators:
                if issued_so_far >= issued_cap:
                    unissued.append({
                        "parent_id": parent.parent_id, "comparator": comparator,
                        "reason": ("TOTAL_ISSUED_CAP"
                                   if issued_cap < policy.per_generation_issued_cap
                                   else "PER_GENERATION_ISSUED_CAP"),
                        "condition_key": condition_key.material(),
                        "condition_value": value_material(condition_value),
                    })
                    continue
                if comparator == COMPARATOR_PARENT:
                    baseline_atom = parent_atom
                    selected = ((condition_key, condition_value, condition_predicate),)
                else:
                    baseline_atom = root_atom
                    selected = tuple(
                        (key, value, parent.ancestry_predicates[index])
                        for index, (key, value) in enumerate(parent.ancestry_conditions)
                    ) + ((condition_key, condition_value, condition_predicate),)
                atom_ids = [atom_for(predicate, "RESPONSE") for _, _, predicate in selected]
                rule_material = {
                    "generation": generation, "policy": policy.content_hash,
                    "parent": parent.parent_id, "parent_predicate": parent.predicate_ref,
                    "comparator": comparator, "baseline": baseline_atom,
                    "condition_refs": [predicate.ref for _, _, predicate in selected],
                    "condition_values": [value_material(value) for _, value, _ in selected],
                    "target": target_label, "query_ref": query_material,
                }
                operation_id = "urn:r61:recurrence:op:" + semantic_hash(canonicalize(rule_material))
                rule_id = _recurrence_rule_id(rule_material)
                form = "SINGLE_ATOM" if len(atom_ids) == 1 else "AND_CARTESIAN_GROUPS"
                rule = {
                    "rule_id": rule_id,
                    "family": "RECURSIVE_SUBGROUP_FORK",
                    "form": form,
                    "baseline_atom_id": baseline_atom,
                    "query_template_id": template_id,
                    "validation": _DIFF_VALIDATION,
                }
                if form == "SINGLE_ATOM":
                    rule["atom_ids"] = atom_ids
                else:
                    rule["atom_groups"] = [[atom_id] for atom_id in atom_ids]
                rules.append(rule)
                expected.append(RecurrenceExpectedOperation(
                    operation_id=operation_id, generation=generation,
                    parent_id=parent.parent_id, comparator=comparator, rule_id=rule_id,
                    condition_keys=tuple(key for key, _, _ in selected),
                    condition_values=tuple(value for _, value, _ in selected),
                    baseline_predicate_ref=exact_ref(
                        atoms[baseline_atom]["predicate_ref"], "baseline"
                    ).as_dict(),
                ))
                issued_so_far += 1
    if not rules:
        raise RecurrenceRefusal("RECURRENCE_GENERATION_ISSUED_NO_OPERATIONS")
    grammar = {
        "schema": CANDIDATE_GRAMMAR_SCHEMA,
        "discovery_operation": f"I03-OP-R61-R4-G{generation}",
        "atoms": tuple(atoms[key] for key in sorted(atoms)),
        "query_templates": tuple(templates[key] for key in sorted(templates)),
        "rules": tuple(sorted(rules, key=lambda rule: rule["rule_id"])),
        "limits": {
            "maximum_conditioner_arity_K": int(policy.bounds["K"]),
            "maximum_target_arity_J": int(policy.bounds["J"]),
        },
        "allow_empty_frontier": False,
    }
    return RecurrenceIssuePlan(
        generation=generation, policy=policy, grammar=grammar,
        expected_operations=tuple(sorted(expected, key=lambda op: op.operation_id)),
        parents=canonical_parents, condition_predicates=tuple(condition_predicates),
        target_label=target_label, query_ref=query_material,
        unissued=tuple(sorted(unissued, key=lambda item: (item["parent_id"], item["comparator"]))),
        query_object=query_ref if hasattr(query_ref, "ref") else None,
        predecessor_plan_ref=predecessor_ref,
        predecessor_issued_count=issued_before,
        cumulative_issued_count=issued_before + len(expected),
        root_predicate_ref=exact_ref(root_predicate.ref, "root predicate").as_dict(),
        state=RECURRENCE_ISSUED,
    )


def recurrence_anti_join(plan: RecurrenceIssuePlan, receipts: Sequence[Any]) -> dict[str, Any]:
    expected = {op.rule_id: op for op in plan.expected_operations}
    counts: dict[str, int] = {}
    for receipt in receipts:
        identity = receipt.candidate_identity
        rule_id = identity.get("rule_id") if isinstance(identity, Mapping) else None
        if not isinstance(rule_id, str):
            raise ValueError("receipt lacks recurrence rule id")
        counts[rule_id] = counts.get(rule_id, 0) + 1
    missing = tuple(sorted(set(expected) - set(counts)))
    unexpected = tuple(sorted(set(counts) - set(expected)))
    count_mismatches = {
        rule_id: {"expected": expected[rule_id].expected_candidate_count,
                  "actual": counts[rule_id]}
        for rule_id in sorted(set(expected) & set(counts))
        if expected[rule_id].expected_candidate_count != counts[rule_id]
    }
    return {
        "expected_operation_count": len(expected),
        "received_rule_count": len(counts),
        "missing_rule_ids": missing,
        "unexpected_rule_ids": unexpected,
        "count_mismatches": count_mismatches,
        "no_drop_ok": not missing and not unexpected and not count_mismatches,
    }


@dataclass(frozen=True)
class RecurrenceGeneration:
    plan: RecurrenceIssuePlan
    execution: Any
    anti_join: Mapping[str, Any]
    receipt_by_rule: Mapping[str, Any]
    handoff_by_receipt: Mapping[str, Any]
    schema: str = RECURRENCE_GENERATION_SCHEMA

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "schema": self.schema, "plan": self.plan.material(),
            "anti_join": self.anti_join,
            "receipt_refs": [receipt.ref for receipt in self.execution.discovery_result.receipts],
            "handoff_refs": [handoff.ref for handoff in self.execution.handoffs],
            "evaluated_frontier_ref": self.execution.discovery_result.evaluated_frontier_ref,
            "replay_ref": self.execution.discovery_result.replay_ref,
        })

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.material())


def execute_recurrence_generation(
    *,
    plan: RecurrenceIssuePlan,
    repository: Any,
    discovery_authority: Any,
    authority_registry: Any,
    release_refs: Sequence[Any],
    predicate_catalog: Sequence[Any],
    query_template_catalog: Sequence[Any],
) -> RecurrenceGeneration:
    if plan.state != RECURRENCE_ISSUED or not plan.expected_operations:
        raise RecurrenceRefusal("RECURRENCE_PLAN_HAS_NO_ISSUED_WORK")
    if exact_ref(discovery_authority.candidate_grammar_ref).content_hash != semantic_hash(plan.grammar):
        raise RecurrenceRefusal("RECURRENCE_AUTHORITY_GRAMMAR_MISMATCH")
    releases = tuple(sorted(
        (exact_ref(ref, "execution release ref") for ref in release_refs),
        key=lambda ref: ref.key,
    ))
    if not releases:
        raise RecurrenceRefusal("RECURRENCE_EXECUTION_RELEASE_REQUIRED")
    for parent in plan.parents:
        if parent.kind == PARENT_RECEIPT_BOUND:
            if parent.handoff is None:
                raise RecurrenceRefusal("RECEIPT_BOUND_PARENT_HANDOFF_MISSING")
            if parent.handoff.ref != exact_ref(parent.replay_binding_ref, "parent replay ref"):
                raise RecurrenceRefusal("EXECUTION_PARENT_HANDOFF_REF_MISMATCH")
            if parent.handoff.receipt_ref != exact_ref(parent.receipt_ref, "parent receipt ref"):
                raise RecurrenceRefusal("EXECUTION_PARENT_RECEIPT_REF_MISMATCH")
            if parent.handoff.winning_predicate.ref != parent.predicate.ref:
                raise RecurrenceRefusal("EXECUTION_PARENT_PREDICATE_MISMATCH")
            if tuple(sorted(parent.source_release_refs, key=lambda ref: ref.key)) != releases:
                raise RecurrenceRefusal("PARENT_SOURCE_RELEASE_EXECUTION_MISMATCH")
            try:
                replay_recursive_branch_membership(
                    repository=repository,
                    handoff=parent.handoff,
                    authority_registry=authority_registry,
                    release_refs=releases,
                )
            except Exception as exc:
                raise RecurrenceRefusal(
                    "PARENT_RECEIPT_REPLAY_REFUSED:" + type(exc).__name__
                ) from exc
        else:
            try:
                validate_object_authority_closure(parent.predicate, authority_registry)
            except Exception as exc:
                raise RecurrenceRefusal(
                    "PARENT_PREDICATE_AUTHORITY_REFUSED:" + type(exc).__name__
                ) from exc
    execution = execute_exact_bounded_discovery_with_handoffs(
        repository=repository,
        discovery_authority=discovery_authority,
        authority_registry=authority_registry,
        release_refs=release_refs,
        predicate_catalog=predicate_catalog,
        query_template_catalog=query_template_catalog,
    )
    anti = recurrence_anti_join(plan, execution.discovery_result.receipts)
    receipt_by_rule = {
        receipt.candidate_identity["rule_id"]: receipt
        for receipt in execution.discovery_result.receipts
    }
    handoff_by_receipt = {
        handoff.receipt_ref.key: handoff for handoff in execution.handoffs
    }
    return RecurrenceGeneration(
        plan=plan, execution=execution, anti_join=anti,
        receipt_by_rule=receipt_by_rule, handoff_by_receipt=handoff_by_receipt,
    )


@dataclass(frozen=True)
class RecurrenceActivation:
    generation: int
    active_parents: tuple[RecurrenceParent, ...]
    waiting: tuple[Mapping[str, Any], ...]
    stopped: tuple[Mapping[str, Any], ...]
    activation_ledger: tuple[Mapping[str, Any], ...]

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "generation": self.generation,
            "active_parents": [parent.material() for parent in self.active_parents],
            "waiting": self.waiting, "stopped": self.stopped,
            "activation_ledger": self.activation_ledger,
        })


def activate_next_generation(
    *,
    policy: RecurrencePolicy,
    generation: RecurrenceGeneration,
    parents: Sequence[RecurrenceParent],
    root_parent: RecurrenceParent,
    next_generation: int,
    condition_predicates: Sequence[tuple[OccurrenceKey, Any, Any]],
) -> RecurrenceActivation:
    expected_next = generation.plan.generation + 1
    if next_generation != expected_next:
        raise RecurrenceRefusal("ACTIVATION_NEXT_GENERATION_MISMATCH")
    if next_generation > int(policy.bounds["D"]):
        return RecurrenceActivation(
            generation=next_generation, active_parents=(),
            waiting=(), stopped=({"reason": "D_REACHED"},),
            activation_ledger=(),
        )
    parent_by_id = {parent.parent_id: parent for parent in parents}
    candidates: list[tuple[RecurrenceExpectedOperation, Any, Any]] = []
    for operation in generation.plan.expected_operations:
        receipt = generation.receipt_by_rule.get(operation.rule_id)
        if receipt is None:
            continue
        parent = parent_by_id[operation.parent_id]
        candidates.append((operation, parent, receipt))
    selected: list[RecurrenceParent] = []
    ledger: list[Mapping[str, Any]] = []
    waiting: list[Mapping[str, Any]] = []
    supported_candidates = [
        (operation, parent, receipt) for operation, parent, receipt in candidates
        if operation.comparator == COMPARATOR_PARENT
        and receipt.typed_state == "DISCOVERED_RESULT_SUPPORTED"
    ]
    for index, (operation, parent, receipt) in enumerate(
        sorted(supported_candidates, key=lambda item: item[0].operation_id)
    ):
        supported_limit = max(
            0, min(policy.breadth_cap,
                   policy.followup_cap - policy.protected_exploration_slots)
        )
        if index >= supported_limit:
            waiting.append({"operation_id": operation.operation_id,
                            "reason": "BREADTH_OR_FOLLOWUP_CAP"})
            continue
        handoff = generation.handoff_by_receipt.get(receipt.ref.key)
        if handoff is None:
            waiting.append({"operation_id": operation.operation_id,
                            "reason": "RECEIPT_BOUND_HANDOFF_UNAVAILABLE"})
            continue
        predicate_lookup = {
            (key.key, typed_value_key(value)): predicate
            for key, value, predicate in generation.plan.condition_predicates
        }
        condition_pairs = tuple(zip(operation.condition_keys, operation.condition_values))
        selected_predicates = tuple(
            predicate_lookup[(key.key, typed_value_key(value))]
            for key, value in condition_pairs
        )
        ancestry_keys = parent.ancestry_conditions + condition_pairs
        ancestry_predicates = parent.ancestry_predicates + selected_predicates
        child = RecurrenceParent(
            parent_id=_parent_id(PARENT_RECEIPT_BOUND, handoff.winning_predicate,
                                 generation.plan.generation, {
                                     "receipt": receipt.ref, "handoff": handoff.ref,
                                     "conditions": [
                                         {"key": key.material(), "value": value_material(value)}
                                         for key, value in (parent.ancestry_conditions + tuple(zip(operation.condition_keys, operation.condition_values)))
                                     ],
                                     "predicates": [
                                         p.ref for p in (parent.ancestry_predicates + selected_predicates)
                                     ],
                                 }),
            predicate=handoff.winning_predicate,
            kind=PARENT_RECEIPT_BOUND, generation=generation.plan.generation,
            source_release_refs=tuple(parent.source_release_refs),
            ancestry_conditions=ancestry_keys,
            ancestry_predicates=ancestry_predicates,
            receipt_ref=receipt.ref, replay_binding_ref=handoff.ref,
            handoff=handoff, activation_reason="SUPPORTED_CHILD_BREADTH",
        )
        selected.append(child)
        ledger.append({"parent_id": child.parent_id, "operation_id": operation.operation_id,
                       "reason": child.activation_reason, "receipt_ref": receipt.ref,
                       "handoff_ref": handoff.ref})
    exploratory_candidates = [
        (operation, parent, receipt) for operation, parent, receipt in candidates
        if operation.comparator == COMPARATOR_PARENT
        and receipt.typed_state != "DISCOVERED_RESULT_SUPPORTED"
    ]
    remaining_slots = max(
        0, min(policy.protected_exploration_slots,
               policy.followup_cap - len(selected))
    )
    for operation, parent, receipt in sorted(
        exploratory_candidates, key=lambda item: item[0].operation_id
    )[:remaining_slots]:
        predicate_lookup = {
            (key.key, typed_value_key(value)): predicate
            for key, value, predicate in generation.plan.condition_predicates
        }
        new_predicates = tuple(
            predicate_lookup[(key.key, typed_value_key(value))]
            for key, value in zip(operation.condition_keys, operation.condition_values)
        )
        composed = _combine_predicates(
            (parent.predicate,) + new_predicates, op="AND",
            tag_material={"generation": next_generation,
                          "parent": parent.parent_id,
                          "operation": operation.operation_id},
        )
        child = RecurrenceParent(
            parent_id=_parent_id(PARENT_EXPLORATORY, composed,
                                 generation.plan.generation, {
                                     "observed_receipt": receipt.ref,
                                     "conditions": [
                                         {"key": key.material(), "value": value_material(value)}
                                         for key, value in (parent.ancestry_conditions + tuple(zip(operation.condition_keys, operation.condition_values)))
                                     ],
                                     "predicates": [
                                         p.ref for p in (parent.ancestry_predicates + new_predicates)
                                     ],
                                     "construction": semantic_hash(canonicalize({
                                         "parent": parent.predicate_ref,
                                         "operation": operation.operation_id,
                                         "observed_receipt": receipt.ref,
                                     })),
                                 }),
            predicate=composed, kind=PARENT_EXPLORATORY,
            generation=generation.plan.generation,
            source_release_refs=tuple(parent.source_release_refs),
            ancestry_conditions=parent.ancestry_conditions + tuple(
                zip(operation.condition_keys, operation.condition_values)
            ),
            ancestry_predicates=parent.ancestry_predicates + new_predicates,
            receipt_ref=None, replay_binding_ref=None, handoff=None,
            activation_reason="PROTECTED_NONWINNING_EXPLORATION",
            construction_ref=semantic_hash(canonicalize({
                "parent": parent.predicate_ref, "operation": operation.operation_id,
                "observed_receipt": receipt.ref,
            })),
        )
        selected.append(child)
        ledger.append({"parent_id": child.parent_id, "operation_id": operation.operation_id,
                       "reason": child.activation_reason,
                       "observed_receipt_ref": receipt.ref})
    for operation, parent, receipt in candidates:
        if any(entry.get("operation_id") == operation.operation_id for entry in ledger):
            continue
        if any(entry.get("operation_id") == operation.operation_id for entry in waiting):
            continue
        waiting.append({"operation_id": operation.operation_id,
                        "reason": "NOT_ACTIVATED_BY_POLICY",
                        "receipt_state": receipt.typed_state})
    return RecurrenceActivation(
        generation=next_generation,
        active_parents=tuple(sorted(selected, key=lambda parent: parent.parent_id)),
        waiting=tuple(sorted(waiting, key=lambda entry: entry["operation_id"])),
        stopped=(),
        activation_ledger=tuple(sorted(ledger, key=lambda entry: entry["operation_id"])),
    )


CAMPAIGN_SCHEMA = "RetainedRecurrenceCampaign@r61.r7.1"
CAMPAIGN_ROOT_SCHEMA = "RecurrenceCampaignRoot@r61.r7.1"
CAMPAIGN_ISSUANCE_SCHEMA = "RecurrenceCampaignIssuance@r61.r7.1"
CAMPAIGN_EXECUTION_SCHEMA = "RecurrenceCampaignExecution@r61.r7.1"
CAMPAIGN_LINEAGE_SCHEMA = "RecurrenceCampaignLineage@r61.r7.1"
CAMPAIGN_ACTIVATION_SCHEMA = "RecurrenceCampaignActivation@r61.r7.1"


def _campaign_hash(value: Any) -> str:
    return semantic_hash(canonicalize(value))


def _restore_handoff_material(item: Mapping[str, Any]) -> RecursiveBranchHandoff:
    return RecursiveBranchHandoff(
        receipt_ref=exact_ref(item.get("receipt_ref")),
        branch_replay_binding=_restore_binding(_mapping(item.get("branch_replay_binding"), "branch replay binding")),
        winning_predicate=_restore_predicate(_mapping(item.get("winning_predicate"), "winning predicate")),
        source_release_refs=tuple(sorted(
            (exact_ref(ref) for ref in item.get("source_release_refs", ())),
            key=lambda ref: ref.key,
        )),
        discovery_authority_ref=exact_ref(item.get("discovery_authority_ref")),
        evaluated_frontier_ref=exact_ref(item.get("evaluated_frontier_ref")),
        candidate_universe_definition=_mapping(item.get("candidate_universe_definition"), "candidate universe"),
        scope_context=_mapping(item.get("scope_context"), "scope context"),
        coverage_pruning_material=_mapping(item.get("coverage_pruning_material"), "coverage pruning"),
        deterministic_parameters=_mapping(item.get("deterministic_parameters"), "deterministic parameters"),
    )


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RecurrenceRefusal(f"{name} must be a mapping")
    return value


def _restore_native_object(cls: Any, payload: Mapping[str, Any]) -> Any:
    obj = cls(
        typed_state=payload.get("typed_state"),
        authority_snapshot_refs=payload.get("authority_snapshot_refs", ()),
        dependency_refs=payload.get("dependency_refs", ()),
        producer_replay_locator_or_reference_root=payload.get("producer_replay_locator_or_reference_root"),
        object_id=payload.get("object_id"), content_hash=payload.get("content_hash"),
        schema_id=payload.get("schema_id"), schema_version=payload.get("schema_version"),
        **dict(_mapping(payload.get("semantic_fields"), "native semantic fields")),
    )
    if canonicalize(obj.as_dict()) != canonicalize(payload):
        raise RecurrenceRefusal("NATIVE_OBJECT_PROJECTION_MISMATCH")
    return obj


def _authority_profile(authority: Any, registry: Any) -> dict[str, Any]:
    _verify_discovery_authority(authority, registry)
    # Grammar and replay locator vary by issuance. All semantic execution policy
    # and exact governing authority snapshots remain portable host configuration.
    fields = dict(authority.semantic_fields)
    fields.pop("candidate_grammar_ref", None)
    fields.pop("candidate_universe_definition", None)
    return canonicalize({
        "family": authority.FAMILY, "typed_state": authority.typed_state,
        "authority_snapshot_refs": authority.authority_snapshot_refs,
        "dependency_refs": authority.dependency_refs, "semantic_fields": fields,
        "authority_material": [registry.resolve_exact(ref).snapshot.as_dict()
                               for ref in authority.authority_snapshot_refs],
    })


def _label_matches_ref(label: str, ref: Any) -> bool:
    ref = exact_ref(ref, "inventory ref")
    if label == ref.object_id:
        return True
    parts = [part for part in re.split(r"[:/|]", ref.object_id) if part]
    tail = parts[-1] if parts else ref.object_id
    return label == tail or label == tail.rsplit("-", 1)[-1]


def _response_leaf_identity(predicate: Any) -> tuple[Any, str]:
    ast = getattr(predicate, "predicate_ast", None)
    if not isinstance(ast, Mapping) or ast.get("op") != "LEAF":
        raise RecurrenceRefusal("CAMPAIGN_CONDITION_PREDICATE_NOT_RESPONSE_LEAF")
    if ast.get("leaf_type") != "SURVEY_RESPONSE_EVENT":
        raise RecurrenceRefusal("CAMPAIGN_CONDITION_PREDICATE_NOT_RESPONSE_EVENT")
    question_ref = exact_ref(ast.get("question_semantic_ref"), "response question ref")
    exact_value = ast.get("exact_value")
    if not isinstance(exact_value, str):
        raise RecurrenceRefusal("CAMPAIGN_CONDITION_PREDICATE_VALUE_UNRESOLVED")
    return question_ref, exact_value


def _validate_target_label(target_label: str, query: Any, question_refs: set[str]) -> None:
    matches = [ref for ref in (exact_ref(r) for r in query.target_refs)
               if _label_matches_ref(target_label, ref)]
    if len(matches) != 1:
        raise RecurrenceRefusal("CAMPAIGN_TARGET_LABEL_QUERY_MISMATCH")
    if matches[0].key not in question_refs:
        raise RecurrenceRefusal("CAMPAIGN_TARGET_LABEL_NOT_IN_SOURCE_INVENTORY")


def _validate_condition_catalog(
    catalog: Mapping[tuple[str, str], Any], question_refs: set[str]
) -> None:
    for (key_text, value_text), predicate in sorted(catalog.items()):
        try:
            key = OccurrenceKey(**json.loads(key_text))
            value = json.loads(value_text)
        except Exception as exc:
            raise RecurrenceRefusal("CAMPAIGN_CONDITION_KEY_OR_VALUE_MALFORMED") from exc
        question_ref, exact_value = _response_leaf_identity(predicate)
        if question_ref.key not in question_refs:
            raise RecurrenceRefusal("CAMPAIGN_CONDITION_QUESTION_NOT_IN_SOURCE_INVENTORY")
        if not _label_matches_ref(key.item_id, question_ref):
            raise RecurrenceRefusal("CAMPAIGN_CONDITION_KEY_QUESTION_MISMATCH")
        expected = str(value)
        if exact_value != expected:
            raise RecurrenceRefusal("CAMPAIGN_CONDITION_VALUE_PREDICATE_MISMATCH")


def _native_campaign_context(*, policy: RecurrencePolicy, root_predicate: Any,
                             releases: Sequence[Any], target_label: str,
                             query: Any, catalog: Mapping[tuple[str, str], Any],
                             repository: Any, registry: Any, factory: Any) -> dict[str, Any]:
    """Shared create/live/restore resolver; performs no discovery invocation."""
    try:
        if not callable(factory) or not isinstance(target_label, str) or not target_label:
            raise RecurrenceRefusal("CAMPAIGN_NATIVE_SETUP_INVALID")
        _verify_public_identity(query)
        _verify_public_identity(root_predicate)
        if exact_ref(query.condition_predicate_ref) != root_predicate.ref:
            raise RecurrenceRefusal("CAMPAIGN_QUERY_ROOT_MISMATCH")
        if int(query.target_arity_and_topology["arity"]) > int(policy.bounds["J"]):
            raise RecurrenceRefusal("CAMPAIGN_QUERY_EXCEEDS_J")
        _parse_target_plan(query, registry)
        resolved = _resolve_release_indices(repository, query=query, release_refs=releases)
        universe_refs = tuple(ref for ref, _ in resolved)
        _require_exact_i03_authority_fitness(
            query=query, predicate=root_predicate, authority_registry=registry,
            universe_refs=universe_refs,
        )
        source_material = []
        authorities = {}
        question_refs: set[str] = set()
        def add_object(obj):
            if semantic_hash(obj.semantic_projection()) != obj.content_hash:
                raise RecurrenceRefusal("CAMPAIGN_SOURCE_OBJECT_IDENTITY_MISMATCH")
            for ref in _validate_public_object_authorities(obj, registry):
                snap = registry.resolve_exact(ref).snapshot
                authorities[ref.key] = snap.as_dict()
        for release_ref in releases:
            release = repository.resolve_release_exact(release_ref)
            for obj in release.public_objects:
                add_object(obj)
                native_question_ref = getattr(obj, "native_question_ref", None)
                if native_question_ref is not None:
                    question_refs.add(exact_ref(native_question_ref).key)
            source_material.append({
                "release_ref": release.release_ref,
                "source_artifact_ref": release.source_artifact_ref,
                "source_release_manifest_hash": release.source_release_manifest_hash,
                "public_refs": [obj.ref for obj in release.public_objects],
                "internal_refs": [obj.ref for obj in release.internal_records],
                "replay_ref": release.replay_manifest.ref,
            })
        add_object(query)
        _validate_target_label(target_label, query, question_refs)
        _validate_condition_catalog(catalog, question_refs)
        predicates = (root_predicate,) + tuple(catalog.values())
        for predicate in predicates:
            _verify_public_identity(predicate)
            add_object(predicate)
            _require_exact_i03_authority_fitness(
                query=query, predicate=predicate, authority_registry=registry,
                universe_refs=universe_refs,
            )
            if set(exact_ref(ref).key for ref in predicate.scope_refs) != set(ref.key for ref in universe_refs):
                raise RecurrenceRefusal("CAMPAIGN_PREDICATE_SOURCE_SCOPE_MISMATCH")
            for ref, index in resolved:
                risk_refs = {exact_ref(obj.risk_set_ref).key
                             for rows in index.routing_by_respondent.values() for obj in rows}
                if exact_ref(query.risk_set_ref).key not in risk_refs:
                    raise RecurrenceRefusal("CAMPAIGN_QUERY_RISK_UNRESOLVED")
                if not {exact_ref(r).key for r in predicate.risk_set_refs} <= risk_refs:
                    raise RecurrenceRefusal("CAMPAIGN_PREDICATE_RISK_UNRESOLVED")
                events = [obj for rows in index.events_by_respondent.values() for obj in rows]
                known_targets = {exact_ref(obj.native_question_ref).key for obj in events}
                known_targets.update(exact_ref(obj.canonical_question_ref_if_authorized).key
                                     for obj in events if obj.canonical_question_ref_if_authorized is not None)
                if not {exact_ref(r).key for r in query.target_refs} <= known_targets:
                    raise RecurrenceRefusal("CAMPAIGN_QUERY_TARGET_UNRESOLVED")
                # Resolve native leaf semantics, including exact branch membership
                # and source authority, without manufacturing empirical receipts.
                for respondent in index.respondents.values():
                    used, used_auth = [], []
                    _eval_predicate(predicate.predicate_ast, respondent=respondent,
                                    index=index, registry=registry, used=used, used_auth=used_auth)
                    for auth in used_auth:
                        snap = registry.resolve_exact(auth).snapshot
                        authorities[auth.key] = snap.as_dict()
        profiles = []
        for generation in range(1, int(policy.bounds["D"]) + 1):
            probe = {
                "schema": CANDIDATE_GRAMMAR_SCHEMA,
                "discovery_operation": f"I03-OP-R61-R4-G{generation}",
                "atoms": (), "query_templates": (), "rules": (),
                "limits": {"maximum_conditioner_arity_K": int(policy.bounds["K"]),
                           "maximum_target_arity_J": int(policy.bounds["J"])},
                "allow_empty_frontier": True,
            }
            authority = factory(probe)
            profiles.append(_authority_profile(authority, registry))
            allowed = {exact_ref(ref).key for ref in authority.source_universe_scope["allowed_universe_refs"]}
            if not set(ref.key for ref in universe_refs) <= allowed:
                raise RecurrenceRefusal("CAMPAIGN_DISCOVERY_SOURCE_SCOPE_MISMATCH")
            if exact_ref(query.risk_set_ref).key not in {
                exact_ref(r).key for r in authority.risk_set_scope["allowed_risk_set_refs"]
            }:
                raise RecurrenceRefusal("CAMPAIGN_DISCOVERY_RISK_SCOPE_MISMATCH")
        return canonicalize({
            "native_contract": current_native_contract(),
            "repository_owner": type(repository).__module__ + "." + type(repository).__qualname__,
            "registry_owner": type(registry).__module__ + "." + type(registry).__qualname__,
            "source_inventory": source_material,
            "query": query.as_dict(), "root_predicate": root_predicate.as_dict(),
            "condition_catalog": [
                {"key": key, "value": value, "predicate": predicate.as_dict()}
                for (key, value), predicate in sorted(catalog.items())
            ],
            "authorities": [authorities[key] for key in sorted(authorities)],
            "discovery_profiles": profiles,
        })
    except RecurrenceRefusal:
        raise
    except Exception as exc:
        raise RecurrenceRefusal("CAMPAIGN_NATIVE_CONTEXT_REFUSED:" + type(exc).__name__) from exc


@dataclass(frozen=True)
class CampaignRootRecord:
    campaign_ref: str
    policy: RecurrencePolicy
    root_predicate: Any
    source_release_refs: tuple[Any, ...]
    target_label: str
    query_ref: Mapping[str, str]
    native_config_ref: str
    owner_refs: tuple[str, ...]
    native_context: Mapping[str, Any]
    schema: str = CAMPAIGN_ROOT_SCHEMA

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "schema": self.schema, "campaign_ref": self.campaign_ref,
            "policy": self.policy.material(),
            "root_predicate": self.root_predicate.as_dict(),
            "source_release_refs": self.source_release_refs,
            "target_label": self.target_label, "query_ref": self.query_ref,
            "native_config_ref": self.native_config_ref,
            "native_context": self.native_context,
            "owner_refs": self.owner_refs,
        })


@dataclass(frozen=True)
class CampaignLineageRecord:
    lineage_ref: str
    campaign_ref: str
    parent_id: str
    predicate: Any
    kind: str
    producer_generation: int
    producing_issuance_ref: str | None
    producing_execution_ref: str | None
    producing_operation_id: str | None
    prior_lineage_ref: str | None
    ancestry_conditions: tuple[tuple[OccurrenceKey, Any], ...]
    ancestry_predicates: tuple[Any, ...]
    source_release_refs: tuple[Any, ...]
    receipt_ref: Any | None = None
    replay_binding_ref: Any | None = None
    handoff: RecursiveBranchHandoff | None = None
    activation_reason: str = "ROOT"
    construction_ref: str | None = None
    schema: str = CAMPAIGN_LINEAGE_SCHEMA

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "schema": self.schema, "lineage_ref": self.lineage_ref,
            "campaign_ref": self.campaign_ref, "parent_id": self.parent_id,
            "predicate": self.predicate.as_dict(), "kind": self.kind,
            "producer_generation": self.producer_generation,
            "producing_issuance_ref": self.producing_issuance_ref,
            "producing_execution_ref": self.producing_execution_ref,
            "producing_operation_id": self.producing_operation_id,
            "prior_lineage_ref": self.prior_lineage_ref,
            "ancestry_conditions": [
                {"key": key.material(), "value": value_material(value)}
                for key, value in self.ancestry_conditions
            ],
            "ancestry_predicate_refs": [p.ref for p in self.ancestry_predicates],
            "source_release_refs": self.source_release_refs,
            "receipt_ref": self.receipt_ref,
            "replay_binding_ref": self.replay_binding_ref,
            "handoff": None if self.handoff is None else self.handoff.as_dict(),
            "activation_reason": self.activation_reason,
            "construction_ref": self.construction_ref,
        })

    def legacy_parent(self) -> RecurrenceParent:
        return RecurrenceParent(
            parent_id=self.parent_id, predicate=self.predicate, kind=self.kind,
            generation=self.producer_generation,
            source_release_refs=self.source_release_refs,
            ancestry_conditions=self.ancestry_conditions,
            ancestry_predicates=self.ancestry_predicates,
            receipt_ref=self.receipt_ref, replay_binding_ref=self.replay_binding_ref,
            handoff=self.handoff, activation_reason=self.activation_reason,
            construction_ref=self.construction_ref,
        )


@dataclass(frozen=True)
class CampaignIssuanceRecord:
    issuance_ref: str
    sequence: int
    generation: int
    parent_lineage_refs: tuple[str, ...]
    predecessor_issuance_ref: str | None
    predecessor_issued_count: int
    cumulative_issued_count: int
    plan: RecurrenceIssuePlan
    plan_ref: str
    state: str
    schema: str = CAMPAIGN_ISSUANCE_SCHEMA

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "schema": self.schema, "issuance_ref": self.issuance_ref,
            "sequence": self.sequence, "generation": self.generation,
            "parent_lineage_refs": self.parent_lineage_refs,
            "predecessor_issuance_ref": self.predecessor_issuance_ref,
            "predecessor_issued_count": self.predecessor_issued_count,
            "cumulative_issued_count": self.cumulative_issued_count,
            "plan": self.plan.material(), "plan_ref": self.plan_ref,
            "state": self.state,
        })


@dataclass(frozen=True)
class CampaignExecutionRecord:
    execution_ref: str
    issuance_ref: str
    plan_ref: str
    grammar_ref: Mapping[str, str]
    receipt_refs: tuple[Any, ...]
    handoff_refs: tuple[Any, ...]
    handoffs: tuple[RecursiveBranchHandoff, ...]
    anti_join: Mapping[str, Any]
    activation_preimage: Mapping[str, Any] = field(default_factory=dict)
    native_result: Any | None = None
    schema: str = CAMPAIGN_EXECUTION_SCHEMA

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "schema": self.schema, "execution_ref": self.execution_ref,
            "issuance_ref": self.issuance_ref, "plan_ref": self.plan_ref,
            "grammar_ref": self.grammar_ref, "receipt_refs": self.receipt_refs,
            "handoff_refs": self.handoff_refs,
            "anti_join": self.anti_join,
            "activation_preimage": self.activation_preimage,
        })


@dataclass(frozen=True)
class CampaignActivationRecord:
    activation_ref: str
    execution_ref: str
    next_generation: int
    active_lineage_refs: tuple[str, ...]
    waiting: tuple[Mapping[str, Any], ...]
    stopped: tuple[Mapping[str, Any], ...]
    ledger: tuple[Mapping[str, Any], ...]
    schema: str = CAMPAIGN_ACTIVATION_SCHEMA

    def material(self) -> dict[str, Any]:
        return canonicalize({
            "schema": self.schema, "activation_ref": self.activation_ref,
            "execution_ref": self.execution_ref,
            "next_generation": self.next_generation,
            "active_lineage_refs": self.active_lineage_refs,
            "waiting": self.waiting, "stopped": self.stopped, "ledger": self.ledger,
        })


class RetainedRecurrenceCampaign:
    """One trusted-host owner of recurrence issuance, execution and lineage."""

    def __init__(self, *, root: CampaignRootRecord, repository: Any,
                 authority_registry: Any, authority_factory: Any,
                 condition_catalog: Mapping[tuple[str, str], Any],
                 query_object: Any) -> None:
        self._root = root
        self._repository = repository
        self._registry = authority_registry
        self._authority_factory = authority_factory
        self._condition_catalog = dict(condition_catalog)
        self._query_object = query_object
        self._lineage: dict[str, CampaignLineageRecord] = {}
        self._issuances: dict[str, CampaignIssuanceRecord] = {}
        self._executions: dict[str, CampaignExecutionRecord] = {}
        self._activations: dict[str, CampaignActivationRecord] = {}
        self._issue_order: list[str] = []
        self._last_issuance_ref: str | None = None
        self._last_plan: RecurrenceIssuePlan | None = None
        self._completed_execution: dict[str, str] = {}
        self._activation_by_execution: dict[str, str] = {}
        self._lock = threading.RLock()
        self._inflight: set[str] = set()
        self._rebuilding = False
        root_lineage_ref = _campaign_hash({
            "campaign_ref": root.campaign_ref, "kind": PARENT_ROOT,
            "predicate": root.root_predicate.ref, "generation": 0,
            "source_release_refs": root.source_release_refs,
        })
        self._root_lineage_ref = root_lineage_ref
        self._lineage[root_lineage_ref] = CampaignLineageRecord(
            lineage_ref=root_lineage_ref, campaign_ref=root.campaign_ref,
            parent_id=root_lineage_ref, predicate=root.root_predicate,
            kind=PARENT_ROOT, producer_generation=0,
            producing_issuance_ref=None, producing_execution_ref=None,
            producing_operation_id=None, prior_lineage_ref=None,
            ancestry_conditions=(), ancestry_predicates=(),
            source_release_refs=root.source_release_refs,
            activation_reason="SOURCE_ROOT",
        )

    @property
    def campaign_ref(self) -> str:
        return self._root.campaign_ref

    @property
    def root_lineage_ref(self) -> str:
        return self._root_lineage_ref

    def _all_handoffs(self) -> tuple[RecursiveBranchHandoff, ...]:
        return tuple({
            record.handoff.ref.key: record.handoff for record in self._lineage.values()
            if record.handoff is not None
        }.values())

    def _resolver(self) -> RecurrenceParentResolver:
        return make_recurrence_parent_resolver(self._all_handoffs())

    def _condition_predicate(self, key: OccurrenceKey, value: Any) -> Any:
        predicate = self._condition_catalog.get(
            (key.key, typed_value_key(value))
        )
        if predicate is None:
            raise RecurrenceRefusal("CONDITION_NOT_IN_CAMPAIGN_CATALOG")
        return predicate

    def _lineage_record(self, ref: str) -> CampaignLineageRecord:
        record = self._lineage.get(ref)
        if record is None:
            raise RecurrenceRefusal("LINEAGE_REFERENCE_NOT_RETAINED")
        return record

    def issue(self, *, parent_lineage_refs: Sequence[str],
              condition_refs: Sequence[tuple[OccurrenceKey, Any]],
              requested_generation: int | None = None,
              predecessor_issuance_ref: str | None = None) -> str:
        with self._lock:
            self._check_history()
            parent_records = tuple(self._lineage_record(ref) for ref in parent_lineage_refs)
            if not parent_records:
                raise RecurrenceRefusal("CAMPAIGN_REQUIRES_PARENT_LINEAGE")
            if len({record.lineage_ref for record in parent_records}) != len(parent_records):
                raise RecurrenceRefusal("DUPLICATE_PARENT_LINEAGE")
            if predecessor_issuance_ref is not None and predecessor_issuance_ref != self._last_issuance_ref:
                raise RecurrenceRefusal("PREDECESSOR_ISSUANCE_NOT_RETAINED_HEAD")
            roots = [record for record in parent_records if record.kind == PARENT_ROOT]
            if roots:
                if len(parent_records) != 1:
                    raise RecurrenceRefusal("ROOT_PARENT_MUST_BE_SOLE_PARENT")
                generation = 1
            else:
                if any(record.producing_execution_ref is None for record in parent_records):
                    raise RecurrenceRefusal("PARENT_LINEAGE_MISSING_PRODUCING_EXECUTION")
                generations = {record.producer_generation for record in parent_records}
                if len(generations) != 1:
                    raise RecurrenceRefusal("PARENT_GENERATION_CONTINUITY_VIOLATION")
                generation = next(iter(generations)) + 1
            if requested_generation is not None and requested_generation != generation:
                raise RecurrenceRefusal("REQUESTED_GENERATION_MISMATCH")
            parents = tuple(record.legacy_parent() for record in parent_records)
            proposed = []
            seen_condition_keys: set[tuple[str, str]] = set()
            for key, value in condition_refs:
                if not isinstance(key, OccurrenceKey):
                    raise RecurrenceRefusal("CAMPAIGN_TYPED_OCCURRENCE_KEY_REQUIRED")
                try:
                    _validate_typed_value(value)
                except ValueError as exc:
                    raise RecurrenceRefusal("CAMPAIGN_TYPED_VALUE_REQUIRED") from exc
                typed_key = (key.key, typed_value_key(value))
                if typed_key in seen_condition_keys:
                    raise RecurrenceRefusal("DUPLICATE_CONDITION_REF")
                seen_condition_keys.add(typed_key)
                proposed.append((key, value, self._condition_predicate(key, value)))
            conditions = tuple(proposed)
            previous_plan = self._last_plan
            predecessor_issuance = self._last_issuance_ref
            plan = build_recurrence_issue_plan(
                policy=self._root.policy, generation=generation,
                parents=parents, root_predicate=self._root.root_predicate,
                target_label=self._root.target_label,
                query_ref=self._query_object, condition_predicates=conditions,
                previous_plan=previous_plan,
                parent_resolver=self._resolver(),
                release_refs=self._root.source_release_refs,
            )
            sequence = len(self._issue_order) + 1
            predecessor_ref = getattr(plan, "predecessor_plan_ref", None)
            issuance_material = {
                "campaign_ref": self._root.campaign_ref, "sequence": sequence,
                "generation": generation, "parent_lineage_refs": parent_lineage_refs,
                "predecessor_issuance_ref": predecessor_issuance,
                "predecessor_issued_count": plan.predecessor_issued_count,
                "cumulative_issued_count": plan.cumulative_issued_count,
                "plan_ref": plan.content_hash, "state": plan.state,
            }
            issuance_ref = _campaign_hash(issuance_material)
            record = CampaignIssuanceRecord(
                issuance_ref=issuance_ref, sequence=sequence, generation=generation,
                parent_lineage_refs=tuple(parent_lineage_refs),
                predecessor_issuance_ref=predecessor_issuance,
                predecessor_issued_count=plan.predecessor_issued_count,
                cumulative_issued_count=plan.cumulative_issued_count,
                plan=plan, plan_ref=plan.content_hash,
                state=plan.state,
            )
            self._issuances[issuance_ref] = record
            self._issue_order.append(issuance_ref)
            self._last_issuance_ref = issuance_ref
            self._last_plan = plan
            return issuance_ref

    def _issuance(self, ref: str) -> CampaignIssuanceRecord:
        record = self._issuances.get(ref)
        if record is None:
            raise RecurrenceRefusal("ISSUANCE_REFERENCE_NOT_RETAINED")
        if record.plan.content_hash != record.plan_ref:
            raise RecurrenceRefusal("ISSUANCE_PLAN_UNSTABLE")
        plan = record.plan
        retained = tuple(self._lineage_record(r).legacy_parent() for r in record.parent_lineage_refs)
        def full_parent(parent):
            return canonicalize({"parent": parent.material(),
                "predicate": parent.predicate.as_dict(),
                "ancestry_predicates": [p.as_dict() for p in parent.ancestry_predicates],
                "handoff": None if parent.handoff is None else parent.handoff.as_dict()})
        if (tuple(full_parent(p) for p in plan.parents) != tuple(full_parent(p) for p in retained)
            or plan.policy.material() != self._root.policy.material()
            or plan.query_object.as_dict() != self._query_object.as_dict()):
            raise RecurrenceRefusal("PLAN_FULL_RETAINED_PARENT_OR_CONTEXT_MISMATCH")
        for key, value, predicate in plan.condition_predicates:
            if predicate.as_dict() != self._condition_predicate(key, value).as_dict():
                raise RecurrenceRefusal("PLAN_FULL_CONDITION_PREDICATE_MISMATCH")
        return record

    def _validate_context(self) -> None:
        actual = _native_campaign_context(
            policy=self._root.policy, root_predicate=self._root.root_predicate,
            releases=self._root.source_release_refs, target_label=self._root.target_label,
            query=self._query_object, catalog=self._condition_catalog,
            repository=self._repository, registry=self._registry, factory=self._authority_factory,
        )
        if actual != self._root.native_context:
            raise RecurrenceRefusal("CAMPAIGN_FROZEN_NATIVE_CONTEXT_MISMATCH")

    def _check_history(self) -> None:
        if not self._rebuilding:
            self._validate_context()
            self._rebuild(self.snapshot()["payload"])

    def _predicate_catalog(self, plan: RecurrenceIssuePlan) -> tuple[Any, ...]:
        by_ref = {self._root.root_predicate.ref.key: self._root.root_predicate}
        by_ref.update((p.ref.key, p) for p in self._condition_catalog.values())
        by_ref.update((r.predicate.ref.key, r.predicate) for r in self._lineage.values())
        selected = {}
        for atom in plan.grammar.get("atoms", ()):
            ref = exact_ref(atom["predicate_ref"])
            if ref.key not in by_ref:
                raise RecurrenceRefusal("PLAN_PREDICATE_NOT_RETAINED")
            selected[ref.key] = by_ref[ref.key]
        return tuple(selected.values())

    def _projection(self, record: CampaignExecutionRecord) -> RecurrenceGeneration:
        """Checked activation view, identical for live and cold completed records."""
        try:
            issuance = self._issuance(record.issuance_ref)
            plan = issuance.plan
            if plan.state != RECURRENCE_ISSUED or record.plan_ref != plan.content_hash:
                raise RecurrenceRefusal("EXECUTION_ISSUANCE_MISMATCH")
            preimage = record.activation_preimage
            authority = _restore_native_object(DiscoveryAuthority, preimage["authority"])
            if _authority_profile(authority, self._registry) != self._root.native_context["discovery_profiles"][plan.generation - 1]:
                raise RecurrenceRefusal("EXECUTION_NATIVE_PROFILE_MISMATCH")
            if canonicalize(authority.candidate_universe_definition) != canonicalize(plan.grammar):
                raise RecurrenceRefusal("EXECUTION_NATIVE_GRAMMAR_MISMATCH")
            grammar_ref = exact_ref(authority.candidate_grammar_ref)
            if canonicalize(grammar_ref) != canonicalize(record.grammar_ref):
                raise RecurrenceRefusal("EXECUTION_GRAMMAR_REF_MISMATCH")
            predicates = self._predicate_catalog(plan)
            atoms = _catalog_atoms(plan.grammar, predicates)
            templates = _catalog_templates(plan.grammar, (self._query_object,))
            _validate_catalog_scope(authority, atoms, templates)
            candidates = _compile_frontier(plan.grammar, atoms, templates)
            if not {c.validation["kind"] for c in candidates} <= _allowed_validation_kinds(authority.validation_rules):
                raise RecurrenceRefusal("EXECUTION_VALIDATION_AUTHORITY_MISMATCH")
            frontier_ref = _discovery_ref("PRE553_I05_EVALUATED_FRONTIER", "frontier", {
                "contract": I05_CONTRACT_ID, "discovery_authority_ref": authority.ref.as_dict(),
                "candidate_grammar_ref": grammar_ref.as_dict(),
                "query_execution_contract": QUERY_EXECUTION_CONTRACT_ID,
                "candidate_identities": [{"candidate_id": c.candidate_id, "candidate_hash": c.candidate_hash} for c in candidates],
                "coverage_claim": COVERAGE_CLAIM,
            })
            if exact_ref(preimage["evaluated_frontier_ref"]) != frontier_ref:
                raise RecurrenceRefusal("EXECUTION_FRONTIER_MISMATCH")
            receipts = tuple(_restore_native_object(DiscoveryResultReceipt, raw) for raw in preimage["receipts"])
            if tuple(r.ref for r in receipts) != record.receipt_refs or len({r.ref.key for r in receipts}) != len(receipts):
                raise RecurrenceRefusal("EXECUTION_RECEIPT_SET_MISMATCH")
            by_rule = {c.rule_id: c for c in candidates}
            anti = recurrence_anti_join(plan, receipts)
            if not anti["no_drop_ok"] or canonicalize(anti) != canonicalize(record.anti_join):
                raise RecurrenceRefusal("EXECUTION_RECEIPT_RECONCILIATION_MISMATCH")
            state_by_coverage = {
                "EVALUATED_SUPPORTED": "DISCOVERED_RESULT_SUPPORTED",
                "EVALUATED_VALID_EMPTY": "VALID_EMPTY",
                "EVALUATED_UNDERPOWERED": "INSUFFICIENT_SUPPORT",
                "EVALUATED_NONCOMPARABLE": "NONCOMPARABLE",
                "EVALUATED_DENIED_BY_EXACT_AUTHORITY": "COVERAGE_LIMITED",
                "EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY": "COVERAGE_LIMITED",
            }
            for receipt in receipts:
                _validate_public_object_authorities(receipt, self._registry)
                candidate = by_rule.get(receipt.candidate_identity.get("rule_id"))
                if candidate is None:
                    raise RecurrenceRefusal("EXECUTION_RECEIPT_OPERATION_MISSING")
                identity = {
                    "candidate_id": candidate.candidate_id, "candidate_hash": candidate.candidate_hash,
                    "family": candidate.family, "rule_id": candidate.rule_id,
                    "validation": candidate.validation,
                    "query_roles": [{"role": r.role, "predicate_ref": r.predicate.ref, "query_ref": r.query.ref} for r in candidate.query_roles],
                }
                if canonicalize(receipt.candidate_identity) != canonicalize(identity):
                    raise RecurrenceRefusal("EXECUTION_RECEIPT_CANDIDATE_MISMATCH")
                if (exact_ref(receipt.discovery_authority_ref) != authority.ref
                    or exact_ref(receipt.winning_predicate_ref) != candidate.winning_predicate.ref
                    or exact_ref(receipt.evaluated_frontier_ref) != frontier_ref
                    or canonicalize(receipt.branch_or_parent_ancestry_refs) != canonicalize(candidate.ancestry_refs)
                    or canonicalize(receipt.source_release_refs) != canonicalize(self._root.source_release_refs)
                    or receipt.exact_query_contract_id != QUERY_EXECUTION_CONTRACT_ID
                    or state_by_coverage.get(receipt.coverage_state) != receipt.typed_state):
                    raise RecurrenceRefusal("EXECUTION_RECEIPT_NATIVE_CLOSURE_MISMATCH")
                fact_refs = tuple(sorted((exact_ref(r) for r in receipt.empirical_fact_refs), key=lambda r: r.key))
                if canonicalize(receipt.validation_fact_refs) != canonicalize(fact_refs):
                    raise RecurrenceRefusal("EXECUTION_RECEIPT_FACT_SET_MISMATCH")
                replay_ref = _discovery_ref("PRE553_I05_DISCOVERY_REPLAY", "candidate-replay", {
                    "contract": I05_CONTRACT_ID, "authority_ref": authority.ref.as_dict(),
                    "frontier_ref": frontier_ref.as_dict(), "candidate_id": candidate.candidate_id,
                    "candidate_hash": candidate.candidate_hash, "coverage_state": receipt.coverage_state,
                    "fact_refs": [r.as_dict() for r in fact_refs],
                    "release_refs": [r.as_dict() for r in self._root.source_release_refs],
                    "query_execution_contract": QUERY_EXECUTION_CONTRACT_ID,
                })
                deps = tuple(sorted((authority.ref, grammar_ref, frontier_ref, candidate.winning_predicate.ref, *fact_refs), key=lambda r: r.key))
                if (exact_ref(receipt.replay_ref) != replay_ref
                    or exact_ref(receipt.producer_replay_locator_or_reference_root) != replay_ref
                    or canonicalize(receipt.dependency_refs) != canonicalize(deps)):
                    raise RecurrenceRefusal("EXECUTION_RECEIPT_REPLAY_MISMATCH")
            handoffs = tuple(_restore_handoff_material(raw) for raw in preimage["handoffs"])
            if (tuple(h.ref for h in handoffs) != record.handoff_refs
                or canonicalize([h.as_dict() for h in handoffs]) != canonicalize([h.as_dict() for h in record.handoffs])):
                raise RecurrenceRefusal("EXECUTION_HANDOFF_SET_MISMATCH")
            native_view = SimpleNamespace(candidate_grammar_ref=grammar_ref, evaluated_frontier_ref=frontier_ref)
            expected_handoffs = []
            for receipt in receipts:
                if receipt.typed_state == "DISCOVERED_RESULT_SUPPORTED":
                    winner, parent = _resolve_receipt_winner(receipt, plan.grammar, predicates)
                    expected_handoffs.append(_make_handoff(
                        winning_predicate=winner, immediate_parent=parent, receipt=receipt,
                        discovery_authority=authority, discovery_result=native_view,
                        release_refs=self._root.source_release_refs, definition=plan.grammar,
                    ))
            expected_handoffs.sort(key=lambda h: h.ref.key)
            if canonicalize([h.as_dict() for h in handoffs]) != canonicalize([h.as_dict() for h in expected_handoffs]):
                raise RecurrenceRefusal("EXECUTION_HANDOFF_RECEIPT_CLOSURE_MISMATCH")
            for handoff in handoffs:
                replay_recursive_branch_membership(repository=self._repository, handoff=handoff,
                    authority_registry=self._registry, release_refs=self._root.source_release_refs)
            fact_refs = sorted({exact_ref(ref) for r in receipts for ref in r.empirical_fact_refs}, key=lambda r: r.key)
            final_replay = _discovery_ref("PRE553_I05_FRONTIER_REPLAY", "frontier-replay", {
                "contract": I05_CONTRACT_ID, "frontier_ref": frontier_ref.as_dict(),
                "receipt_refs": [r.ref.as_dict() for r in receipts],
                "fact_refs": [r.as_dict() for r in fact_refs],
                "valid_empty": all(r.typed_state == "VALID_EMPTY" for r in receipts),
            })
            if exact_ref(preimage["replay_ref"]) != final_replay:
                raise RecurrenceRefusal("EXECUTION_FINAL_REPLAY_MISMATCH")
            material = record.material()
            material.pop("schema"); material.pop("execution_ref")
            material["campaign_ref"] = self._root.campaign_ref
            if _campaign_hash(material) != record.execution_ref:
                raise RecurrenceRefusal("EXECUTION_RECORD_HASH_MISMATCH")
            return RecurrenceGeneration(
                plan=plan,
                execution=SimpleNamespace(discovery_result=SimpleNamespace(receipts=receipts,
                    evaluated_frontier_ref=frontier_ref, replay_ref=final_replay), handoffs=handoffs),
                anti_join=anti, receipt_by_rule={r.candidate_identity["rule_id"]: r for r in receipts},
                handoff_by_receipt={h.receipt_ref.key: h for h in handoffs},
            )
        except RecurrenceRefusal:
            raise
        except Exception as exc:
            raise RecurrenceRefusal("EXECUTION_PREIMAGE_REFUSED:" + type(exc).__name__) from exc

    def execute(self, issuance_ref: str) -> str:
        with self._lock:
            self._check_history()
            existing = self._completed_execution.get(issuance_ref)
            if existing is not None:
                return existing
            if issuance_ref in self._inflight:
                raise RecurrenceRefusal("HOLD_AMBIGUOUS_NATIVE_EXECUTION")
            record = self._issuance(issuance_ref)
            plan = record.plan
            if plan.state != RECURRENCE_ISSUED or not plan.expected_operations:
                raise RecurrenceRefusal("RECURRENCE_PLAN_HAS_NO_ISSUED_WORK")
            authority = self._authority_factory(plan.grammar)
            if _authority_profile(authority, self._registry) != self._root.native_context["discovery_profiles"][plan.generation - 1]:
                raise RecurrenceRefusal("EXECUTION_NATIVE_PROFILE_MISMATCH")
            self._inflight.add(issuance_ref)
            generation = execute_recurrence_generation(
                plan=plan, repository=self._repository, discovery_authority=authority,
                authority_registry=self._registry, release_refs=self._root.source_release_refs,
                predicate_catalog=self._predicate_catalog(plan), query_template_catalog=(self._query_object,),
            )
            preimage = canonicalize({
                "authority": authority.as_dict(),
                "evaluated_frontier_ref": generation.execution.discovery_result.evaluated_frontier_ref,
                "replay_ref": generation.execution.discovery_result.replay_ref,
                "receipts": [r.as_dict() for r in generation.execution.discovery_result.receipts],
                "handoffs": [h.as_dict() for h in generation.execution.handoffs],
            })
            material = canonicalize({
                "campaign_ref": self._root.campaign_ref, "issuance_ref": issuance_ref,
                "plan_ref": plan.content_hash, "grammar_ref": authority.candidate_grammar_ref,
                "receipt_refs": [r.ref for r in generation.execution.discovery_result.receipts],
                "handoff_refs": [h.ref for h in generation.execution.handoffs],
                "anti_join": generation.anti_join, "activation_preimage": preimage,
            })
            execution_ref = _campaign_hash(material)
            execution = CampaignExecutionRecord(
                execution_ref=execution_ref, issuance_ref=issuance_ref, plan_ref=plan.content_hash,
                grammar_ref=canonicalize(authority.candidate_grammar_ref),
                receipt_refs=tuple(r.ref for r in generation.execution.discovery_result.receipts),
                handoff_refs=tuple(h.ref for h in generation.execution.handoffs),
                handoffs=tuple(generation.execution.handoffs), anti_join=copy.deepcopy(generation.anti_join),
                activation_preimage=preimage,
            )
            self._projection(execution)
            self._executions[execution_ref] = execution
            self._completed_execution[issuance_ref] = execution_ref
            self._inflight.remove(issuance_ref)
            return execution_ref

    def activate(self, execution_ref: str, *,
                 requested_next_generation: int | None = None) -> str:
        with self._lock:
            self._check_history()
            execution = self._executions.get(execution_ref)
            if execution is None:
                raise RecurrenceRefusal("EXECUTION_REFERENCE_NOT_RETAINED")
            issuance = self._issuance(execution.issuance_ref)
            plan = issuance.plan
            next_generation = plan.generation + 1
            if requested_next_generation is not None and requested_next_generation != next_generation:
                raise RecurrenceRefusal("ACTIVATION_NEXT_GENERATION_MISMATCH")
            existing = self._activation_by_execution.get(execution_ref)
            if existing is not None:
                return existing
            root_lineage = self._lineage[self._root_lineage_ref]
            parent_by_id = {
                self._lineage[ref].legacy_parent().parent_id: self._lineage[ref]
                for ref in issuance.parent_lineage_refs
            }
            activation = activate_next_generation(
                policy=self._root.policy, generation=self._projection(execution),
                parents=tuple(self._lineage[ref].legacy_parent() for ref in issuance.parent_lineage_refs),
                root_parent=root_lineage.legacy_parent(),
                next_generation=next_generation,
                condition_predicates=plan.condition_predicates,
            )
            ledger_by_child = {
                entry["parent_id"]: entry for entry in activation.activation_ledger
            }
            operations_by_id = {
                operation.operation_id: operation for operation in plan.expected_operations
            }
            active_refs: list[str] = []
            for child in activation.active_parents:
                ledger = ledger_by_child.get(child.parent_id)
                if ledger is None:
                    raise RecurrenceRefusal("ACTIVATION_LEDGER_MISSING_CHILD")
                operation = operations_by_id.get(ledger["operation_id"])
                if operation is None:
                    raise RecurrenceRefusal("ACTIVATION_OPERATION_NOT_RETAINED")
                prior = None
                for lineage in parent_by_id.values():
                    if lineage.lineage_ref in issuance.parent_lineage_refs and lineage.parent_id == operation.parent_id:
                        prior = lineage
                        break
                if prior is None:
                    raise RecurrenceRefusal("ACTIVATION_PRIOR_LINEAGE_MISSING")
                lineage_material = {
                    "campaign_ref": self._root.campaign_ref, "parent_id": child.parent_id,
                    "predicate": child.predicate.ref, "kind": child.kind,
                    "producer_generation": plan.generation,
                    "producing_issuance_ref": issuance.issuance_ref,
                    "producing_execution_ref": execution_ref,
                    "producing_operation_id": operation.operation_id,
                    "prior_lineage_ref": prior.lineage_ref,
                    "ancestry_conditions": [
                        {"key": key.material(), "value": value_material(value)}
                        for key, value in child.ancestry_conditions
                    ],
                    "ancestry_predicate_refs": [p.ref for p in child.ancestry_predicates],
                    "source_release_refs": child.source_release_refs,
                    "receipt_ref": child.receipt_ref,
                    "replay_binding_ref": child.replay_binding_ref,
                    "activation_reason": child.activation_reason,
                    "construction_ref": child.construction_ref,
                }
                lineage_ref = _campaign_hash(lineage_material)
                if lineage_ref not in self._lineage:
                    self._lineage[lineage_ref] = CampaignLineageRecord(
                        lineage_ref=lineage_ref, campaign_ref=self._root.campaign_ref,
                        parent_id=child.parent_id, predicate=child.predicate,
                        kind=child.kind, producer_generation=plan.generation,
                        producing_issuance_ref=issuance.issuance_ref,
                        producing_execution_ref=execution_ref,
                        producing_operation_id=operation.operation_id,
                        prior_lineage_ref=prior.lineage_ref,
                        ancestry_conditions=child.ancestry_conditions,
                        ancestry_predicates=child.ancestry_predicates,
                        source_release_refs=child.source_release_refs,
                        receipt_ref=child.receipt_ref,
                        replay_binding_ref=child.replay_binding_ref,
                        handoff=child.handoff,
                        activation_reason=child.activation_reason,
                        construction_ref=child.construction_ref,
                    )
                active_refs.append(lineage_ref)
            activation_material = {
                "campaign_ref": self._root.campaign_ref, "execution_ref": execution_ref,
                "next_generation": next_generation,
                "active_lineage_refs": active_refs,
                "waiting": activation.waiting, "stopped": activation.stopped,
                "ledger": activation.activation_ledger,
            }
            activation_ref = _campaign_hash(activation_material)
            self._activations[activation_ref] = CampaignActivationRecord(
                activation_ref=activation_ref, execution_ref=execution_ref,
                next_generation=next_generation,
                active_lineage_refs=tuple(active_refs),
                waiting=copy.deepcopy(activation.waiting),
                stopped=copy.deepcopy(activation.stopped),
                ledger=copy.deepcopy(activation.activation_ledger),
            )
            self._activation_by_execution[execution_ref] = activation_ref
            return activation_ref

    def inspect(self) -> dict[str, Any]:
        with self._lock:
            return copy.deepcopy({
                "schema": CAMPAIGN_SCHEMA,
                "campaign_ref": self._root.campaign_ref,
                "root": self._root.material(),
                "lineage": [record.material() for record in self._lineage.values()],
                "issuances": [record.material() for record in self._issuances.values()],
                "executions": [record.material() for record in self._executions.values()],
                "activations": [record.material() for record in self._activations.values()],
                "inflight_issuance_refs": sorted(self._inflight),
            })

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            payload = self.inspect()
            payload["handoffs"] = [
                handoff.as_dict() for handoff in sorted({
                    h.ref.key: h for record in self._executions.values() for h in record.handoffs
                }.values(), key=lambda h: h.ref.key)
            ]
            payload["condition_catalog"] = [
                {"key": key, "value": value, "predicate": predicate.as_dict()}
                for (key, value), predicate in sorted(self._condition_catalog.items())
            ]
            checkpoint_ref = _campaign_hash(payload)
            return {"payload": payload, "checkpoint_ref": checkpoint_ref}

    def _rebuild(self, payload: Mapping[str, Any]) -> "RetainedRecurrenceCampaign":
        """Replay administrative transitions only; never re-execute discovery."""
        rebuilt = type(self)(root=self._root, repository=self._repository,
            authority_registry=self._registry, authority_factory=self._authority_factory,
            condition_catalog=self._condition_catalog, query_object=self._query_object)
        rebuilt._rebuilding = True
        try:
            if payload.get("schema") != CAMPAIGN_SCHEMA:
                raise RecurrenceRefusal("CAMPAIGN_SNAPSHOT_SCHEMA_MISMATCH")
            def unique(items, field):
                result = {}
                for item in items:
                    if item[field] in result:
                        raise RecurrenceRefusal("RESTORE_DUPLICATE_RECORD")
                    result[item[field]] = item
                return result
            execution_items = unique(payload.get("executions", ()), "issuance_ref")
            activation_items = unique(payload.get("activations", ()), "execution_ref")
            for item in payload.get("issuances", ()):
                conditions = tuple((OccurrenceKey(**entry["key"]),
                    ABSENT if entry["value"] == {"$typed_value": "ABSENT"} else entry["value"])
                    for entry in item["plan"]["condition_entries"])
                issue_ref = rebuilt.issue(parent_lineage_refs=tuple(item["parent_lineage_refs"]),
                    condition_refs=conditions, requested_generation=item["generation"],
                    predecessor_issuance_ref=item["predecessor_issuance_ref"])
                if rebuilt._issuance(issue_ref).material() != canonicalize(item):
                    raise RecurrenceRefusal("RESTORE_ISSUANCE_HISTORY_MISMATCH")
                raw = execution_items.pop(issue_ref, None)
                if raw is None:
                    continue
                preimage = raw["activation_preimage"]
                handoffs = tuple(_restore_handoff_material(h) for h in preimage["handoffs"])
                execution = CampaignExecutionRecord(
                    execution_ref=raw["execution_ref"], issuance_ref=raw["issuance_ref"],
                    plan_ref=raw["plan_ref"], grammar_ref=raw["grammar_ref"],
                    receipt_refs=tuple(exact_ref(r) for r in raw["receipt_refs"]),
                    handoff_refs=tuple(exact_ref(r) for r in raw["handoff_refs"]),
                    handoffs=handoffs, anti_join=raw["anti_join"],
                    activation_preimage=copy.deepcopy(preimage))
                if execution.material() != canonicalize(raw):
                    raise RecurrenceRefusal("RESTORE_EXECUTION_RECORD_MISMATCH")
                rebuilt._projection(execution)
                rebuilt._executions[execution.execution_ref] = execution
                rebuilt._completed_execution[issue_ref] = execution.execution_ref
                activation = activation_items.pop(execution.execution_ref, None)
                if activation is not None:
                    ref = rebuilt.activate(execution.execution_ref,
                        requested_next_generation=activation["next_generation"])
                    if rebuilt._activations[ref].material() != canonicalize(activation):
                        raise RecurrenceRefusal("RESTORE_ACTIVATION_RECORD_MISMATCH")
            if execution_items or activation_items:
                raise RecurrenceRefusal("RESTORE_ORPHAN_EXECUTION_OR_ACTIVATION")
            inflight = tuple(payload.get("inflight_issuance_refs", ()))
            if len(set(inflight)) != len(inflight):
                raise RecurrenceRefusal("RESTORE_DUPLICATE_INFLIGHT")
            for ref in inflight:
                issuance = rebuilt._issuance(ref)
                if ref in rebuilt._completed_execution or issuance.state != RECURRENCE_ISSUED:
                    raise RecurrenceRefusal("RESTORE_INVALID_INFLIGHT")
            rebuilt._inflight = set(inflight)
            # Full equality catches extra/dropped/reordered lineage, ancestry,
            # operations, catalog entries, counters and native side material.
            expected = canonicalize(rebuilt.snapshot()["payload"])
            # Execution/activation arrays preserve their actual commit order;
            # administrative replay uses issuance order. Compare by exact refs.
            for field, key in (("executions", "execution_ref"), ("activations", "activation_ref")):
                expected[field] = sorted(expected[field], key=lambda x: x[key])
            supplied = copy.deepcopy(canonicalize(payload))
            for field, key in (("executions", "execution_ref"), ("activations", "activation_ref")):
                supplied[field] = sorted(supplied[field], key=lambda x: x[key])
            if expected != supplied:
                raise RecurrenceRefusal("RESTORE_FULL_RECORD_CLOSURE_MISMATCH")
            # Retain observed execution/activation commit order after validation.
            rebuilt._executions = {raw["execution_ref"]: rebuilt._executions[raw["execution_ref"]]
                                   for raw in payload["executions"]}
            rebuilt._activations = {raw["activation_ref"]: rebuilt._activations[raw["activation_ref"]]
                                    for raw in payload["activations"]}
            return rebuilt
        except RecurrenceRefusal:
            raise
        except Exception as exc:
            raise RecurrenceRefusal("RESTORE_RECORD_CLOSURE_REFUSED:" + type(exc).__name__) from exc
        finally:
            rebuilt._rebuilding = False

    @classmethod
    def restore(cls, *, snapshot: Mapping[str, Any], expected_checkpoint_ref: str,
                repository: Any, authority_registry: Any, authority_factory: Any,
                condition_catalog: Mapping[tuple[str, str], Any],
                query_object: Any) -> "RetainedRecurrenceCampaign":
        try:
            payload = _mapping(snapshot.get("payload"), "snapshot payload")
            actual = _campaign_hash(payload)
            if (not expected_checkpoint_ref or snapshot.get("checkpoint_ref") != actual
                or expected_checkpoint_ref != actual):
                raise RecurrenceRefusal("SNAPSHOT_CHECKPOINT_PIN_MISMATCH")
            if payload.get("schema") != CAMPAIGN_SCHEMA:
                raise RecurrenceRefusal("CAMPAIGN_SNAPSHOT_SCHEMA_MISMATCH")
            root = _mapping(payload["root"], "campaign root")
            policy_material = dict(root["policy"])
            policy_material["comparators"] = tuple(policy_material.get("comparators", ()))
            policy_material["owner_refs"] = tuple(policy_material.get("owner_refs", ()))
            campaign = _create_campaign_from_catalog(
                policy=RecurrencePolicy(**policy_material),
                root_predicate=_restore_predicate(root["root_predicate"]),
                source_release_refs=tuple(exact_ref(r) for r in root["source_release_refs"]),
                target_label=root["target_label"], query_object=query_object,
                catalog=condition_catalog, repository=repository,
                authority_registry=authority_registry, authority_factory=authority_factory,
                owner_refs=tuple(root["owner_refs"]))
            if campaign._root.material() != canonicalize(root):
                raise RecurrenceRefusal("RESTORE_FROZEN_NATIVE_CONTEXT_MISMATCH")
            return campaign._rebuild(payload)
        except RecurrenceRefusal:
            raise
        except Exception as exc:
            raise RecurrenceRefusal("RESTORE_CONTEXT_REFUSED:" + type(exc).__name__) from exc


def _create_campaign_from_catalog(*, policy, root_predicate, source_release_refs,
                                  target_label, query_object, catalog, repository,
                                  authority_registry, authority_factory, owner_refs):
    if not isinstance(policy, RecurrencePolicy):
        raise RecurrenceRefusal("CAMPAIGN_POLICY_REQUIRED")
    releases = tuple(sorted((exact_ref(ref) for ref in source_release_refs), key=lambda r: r.key))
    if not releases or len(set(releases)) != len(releases):
        raise RecurrenceRefusal("CAMPAIGN_EXACT_RELEASE_SET_REQUIRED")
    # Reconstruct canonical immutable native objects; no public mutable semantic
    # dictionaries remain attached to campaign identity material.
    root_predicate = _restore_predicate(root_predicate.as_dict())
    query_object = _restore_native_object(EmpiricalQuerySpec, query_object.as_dict())
    catalog = {key: _restore_predicate(p.as_dict()) for key, p in catalog.items()}
    context = _native_campaign_context(policy=policy, root_predicate=root_predicate,
        releases=releases, target_label=target_label, query=query_object, catalog=catalog,
        repository=repository, registry=authority_registry, factory=authority_factory)
    config_ref = _campaign_hash({"policy": policy.material(), "root": root_predicate.as_dict(),
        "releases": releases, "target": target_label, "native_context": context,
        "owner_refs": tuple(owner_refs)})
    root = CampaignRootRecord(campaign_ref="urn:r61:campaign:" + config_ref,
        policy=copy.deepcopy(policy), root_predicate=root_predicate, source_release_refs=releases,
        target_label=target_label, query_ref=query_object.ref.as_dict(),
        native_config_ref=config_ref, native_context=context, owner_refs=tuple(owner_refs))
    return RetainedRecurrenceCampaign(root=root, repository=repository,
        authority_registry=authority_registry, authority_factory=authority_factory,
        condition_catalog=catalog, query_object=query_object)


def create_campaign(*, policy: RecurrencePolicy, root_predicate: Any,
                    source_release_refs: Sequence[Any], target_label: str,
                    query_object: Any,
                    condition_catalog: Sequence[tuple[OccurrenceKey, Any, Any]],
                    repository: Any, authority_registry: Any,
                    authority_factory: Any,
                    owner_refs: Sequence[str] = ()) -> RetainedRecurrenceCampaign:
    catalog = {}
    for key, value, predicate in condition_catalog:
        if not isinstance(key, OccurrenceKey):
            raise RecurrenceRefusal("CAMPAIGN_TYPED_OCCURRENCE_KEY_REQUIRED")
        try:
            _validate_typed_value(value)
        except ValueError as exc:
            raise RecurrenceRefusal("CAMPAIGN_TYPED_VALUE_REQUIRED") from exc
        typed_key = (key.key, typed_value_key(value))
        if typed_key in catalog:
            raise RecurrenceRefusal("DUPLICATE_CAMPAIGN_CATALOG_KEY")
        catalog[typed_key] = predicate
    return _create_campaign_from_catalog(policy=policy, root_predicate=root_predicate,
        source_release_refs=source_release_refs, target_label=target_label,
        query_object=query_object, catalog=catalog, repository=repository,
        authority_registry=authority_registry, authority_factory=authority_factory,
        owner_refs=owner_refs)


__all__ = [
    "SUPPORTED", "NOT_ELIGIBLE", "NATIVE_UNSUPPORTED", "SUPPORTED_DISPOSITIONS",
    "LOWERING_VERSION", "current_native_contract", "NativeCatalog",
    "LoweringRecord", "LoweringPlan", "lower_operation", "lower_frontier",
    "native_receipt_anti_join", "RecurrencePolicy", "RecurrenceParent",
    "RecurrenceExpectedOperation", "RecurrenceIssuePlan", "RecurrenceGeneration",
    "RecurrenceActivation", "make_root_parent", "build_recurrence_issue_plan",
    "execute_recurrence_generation", "recurrence_anti_join",
    "activate_next_generation", "RECURRENCE_POLICY_SCHEMA",
    "RECURRENCE_PLAN_SCHEMA", "RECURRENCE_GENERATION_SCHEMA",
    "COMPARATOR_ROOT", "COMPARATOR_PARENT", "PARENT_ROOT",
    "PARENT_RECEIPT_BOUND", "PARENT_EXPLORATORY",
]
