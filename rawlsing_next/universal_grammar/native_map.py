"""R61 semantic lowerer for the current PRE553 I05 exact grammar contract.

The lowerer asks a supplied native catalog for exact typed predicate/query refs
and objects, validates the operation against the frozen policy, and compiles the
expected native candidate identities before execution. Missing capability is a
typed refusal; the scientific operation is never pruned.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
import json
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
)
from rawlsing_next.pre553_empirical_objects import (
    canonicalize,
    exact_ref,
    semantic_hash,
)

from .enumerate import role_disposition
from .types import (
    ELIGIBLE, UNSUPPORTED_RUNTIME, GrammarPolicy, OccurrenceKey,
    ScientificFrontier, ScientificOperation, SourceInventory, typed_value_key,
    value_material,
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


__all__ = [
    "SUPPORTED", "NOT_ELIGIBLE", "NATIVE_UNSUPPORTED", "SUPPORTED_DISPOSITIONS",
    "LOWERING_VERSION", "current_native_contract", "NativeCatalog",
    "LoweringRecord", "LoweringPlan", "lower_operation", "lower_frontier",
    "native_receipt_anti_join",
]
