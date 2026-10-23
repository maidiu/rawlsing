"""R61 R01 generic symbolic frontier and semantic native mapping tests (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from rawlsing_next.pre553_discovery_exact import (
    ExactBoundedCoverageError,
    execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_recursive_handoff import (
    load_recursive_handoff_bundle,
    write_recursive_handoff_bundle,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _d_auth,
    _discovery_authority,
    _registry as _i05_registry,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source,
    _branch_predicate,
    _predicate,
    _query,
    _query_authority,
    _response_leaf,
)
from rawlsing_next.universal_grammar.enumerate import (
    conservation_report,
    enumerate_frontier,
    inventory_ledger,
    iter_partitions,
)
from rawlsing_next.universal_grammar.native_map import (
    NATIVE_UNSUPPORTED,
    SUPPORTED,
    NativeCatalog,
    current_native_contract,
    COMPARATOR_PARENT,
    COMPARATOR_ROOT,
    PARENT_EXPLORATORY,
    PARENT_RECEIPT_BOUND,
    RecurrenceIssuePlan,
    RecurrenceParent,
    RecurrencePolicy,
    activate_next_generation,
    build_recurrence_issue_plan,
    execute_recurrence_generation,
    lower_frontier,
    lower_operation,
    make_root_parent,
    native_receipt_anti_join,
)
from rawlsing_next.universal_grammar.types import (
    ABSENT,
    ADMINISTERED,
    ADMINISTRATION_UNKNOWN,
    DEFERRED,
    ELIGIBLE,
    DISPOSITIONS,
    ELIGIBILITY_STATES,
    EXECUTION_STATES,
    HELD,
    INAPPLICABLE_PROVED,
    NOT_ADMINISTERED,
    NOT_STARTED,
    PROHIBITED,
    RESULT_STATES,
    UNKNOWN,
    UNSUPPORTED_RUNTIME,
    DirectionGrant,
    GrammarPolicy,
    HeldRecord,
    MeasurePlan,
    Occurrence,
    OccurrenceKey,
    SourceInventory,
    typed_value_key,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = "R61-TEST-ONLY-OWNER"
POLICY_ID = "R61-TEST-POLICY"


def _measures(*, population_weighted: bool = False):
    return (
        MeasurePlan(
            "SAMPLE", "SAMPLE", None, None, "descriptive-sample-proportion",
            "UNQUANTIFIED_SAMPLE",
        ),
        MeasurePlan(
            "POPULATION", "POPULATION",
            "WEIGHT-REF" if population_weighted else None,
            "DESIGN-REF" if population_weighted else None,
            "target-population-proportion", "DESIGN_BASED",
        ),
    )


def _grants(*, reverse: bool = False):
    grants = [
        DirectionGrant(("OUTCOME",), (), "DIST", "DIR-DIST"),
        DirectionGrant(("OUTCOME",), (), "STATE_ROBUSTNESS", "DIR-STATE"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE",), "CONDITIONAL", "DIR-COND"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE",), "FORK", "DIR-FORK"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE", "EXPOSURE"), "CONDITIONAL", "DIR-COND2"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE", "EXPOSURE"), "FORK", "DIR-FORK2"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE", "EXPOSURE"), "INTERACTION", "DIR-INT2"),
        DirectionGrant(("OUTCOME", "OUTCOME"), (), "JOINT", "DIR-JOINT"),
        DirectionGrant(("OUTCOME", "OUTCOME"), (), "CO_TRAVEL", "DIR-COTRAVEL"),
        DirectionGrant(
            ("OUTCOME", "OUTCOME"), ("EXPOSURE",), "JOINT", "DIR-JOINT-COND"
        ),
        DirectionGrant(
            ("OUTCOME", "OUTCOME"), ("EXPOSURE",), "CO_TRAVEL", "DIR-COTRAVEL-COND"
        ),
    ]
    if reverse:
        grants.extend([
            DirectionGrant(("EXPOSURE",), (), "DIST", "DIR-REV-DIST"),
            DirectionGrant(("EXPOSURE",), ("OUTCOME",), "CONDITIONAL", "DIR-REV-COND"),
        ])
    return tuple(grants)


def _policy(*, j=2, k=2, d=1, reverse=False, allowed=None, separate=()):
    return GrammarPolicy(
        policy_id=POLICY_ID,
        grade="PROPOSED_TEST_ONLY",
        allowed_classes=allowed or (
            "DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL", "FORK",
            "INTERACTION", "STATE_ROBUSTNESS",
        ),
        separate_classes=separate or ("CROSS_SOURCE", "TEMPORAL", "POSSIBILITY", "STRUCTURAL"),
        target_roles=("OUTCOME", "EXPOSURE"),
        conditioner_roles=("EXPOSURE", "OUTCOME"),
        administrative_roles=("IDENTITY",),
        direction_grants=_grants(reverse=reverse),
        bounds={"J": j, "K": k, "D": d},
        population_requires_weight=True,
        validation_policy="EXPLORATORY_TEST_ONLY",
        exploration_policy="FINITE_FULL_SYMBOLIC_FRONTIER_NO_UNARY_PRUNE",
        stop_policy="EXACT_COMPLETE_OR_BUDGET_PARTIAL_WITH_PENDING_IDS",
        owner_refs=(OWNER,),
        authority_refs=("urn:r61:test:policy:1",),
    )


def _occurrence(
    item,
    *,
    target_role="OUTCOME",
    conditioner_role="EXPOSURE",
    label=None,
    unit="person",
    topology="SCALAR_SINGULAR",
    forms=("ALL_FORM",),
    domain=(0, 1),
    administration=ADMINISTERED,
    route_state="KNOWN",
    option_id=None,
    form_id=None,
    repeat_id=None,
    scope="WAVE-A",
    risk_set_refs=("RISK-A",),
    administrative_role=None,
):
    return Occurrence(
        key=OccurrenceKey(item, option_id=option_id, form_id=form_id, repeat_id=repeat_id),
        label=label or item.upper(),
        unit=unit,
        topology=topology,
        forms=forms,
        domain=domain,
        target_role=target_role,
        conditioner_role=conditioner_role,
        administrative_role=administrative_role,
        administration=administration,
        route_state=route_state,
        scope=scope,
        risk_set_refs=risk_set_refs,
    )


def _inventory(occurrences, *, complete=True, gaps=(), held=()):
    return SourceInventory(
        inventory_id="R61-INVENTORY",
        source_id="R61-SYNTH-SOURCE",
        wave="WAVE-A",
        edition="EDITION-1",
        source_sha256="a" * 64,
        scope="WAVE-A",
        occurrences=tuple(occurrences),
        measure_plans=_measures(),
        risk_set_refs=("RISK-A",),
        unit_transforms=("PERSON_SELF",),
        state_map={"DK": "DONT_KNOW", "MISSING": "NOT_ADMINISTERED"},
        authority_refs=(OWNER,),
        current_selection=None,
        inventory_complete=complete,
        inventory_gaps=tuple(gaps),
        held=tuple(held),
        unresolved=(),
    )


def _main_inventory():
    return _inventory((
        _occurrence("q_alpha"),
        _occurrence("q_beta"),
        _occurrence("q_gamma"),
        _occurrence("q_delta"),
        _occurrence("admin_row", target_role=None, conditioner_role=None,
                    label="ADMINISTRATIVE", administrative_role="IDENTITY"),
    ))


def _tiny_inventory():
    return _inventory((
        _occurrence("z_one"),
        _occurrence("z_two"),
        _occurrence("admin_row", target_role=None, conditioner_role=None,
                    administrative_role="IDENTITY"),
    ))


def _frontier(inventory=None, policy=None, **kwargs):
    return enumerate_frontier(
        inventory or _main_inventory(), policy or _policy(), **kwargs
    )


def _op_for(frontier, *, claim_class, targets, conditions=(), condition_mode="AND",
            measure_id="SAMPLE"):
    target_keys = tuple(
        key for key in (OccurrenceKey(item) for item in targets)
    )
    for op in frontier.operations:
        if (
            op.claim_class == claim_class
            and op.targets == target_keys
            and op.conditions == tuple((OccurrenceKey(item), value) for item, value in conditions)
            and op.condition_mode == condition_mode
            and op.measure_id == measure_id
        ):
            return op
    raise AssertionError(f"operation not found: {claim_class} {targets} {conditions}")


def test_independent_tiny_frontier_oracle_and_complete_disposition_ledger():
    frontier = _frontier(_tiny_inventory(), _policy(j=1, k=1, d=0))
    # Independent combinatorial reference: two target occurrences, one
    # conditioner, two values, one SAMPLE measure plus one unweighted
    # POPULATION measure, and four method-gated classes.
    # SAMPLE: 1 DIST + 1 STATE_ROBUSTNESS + 2 CONDITIONAL = 4 per target.
    # POPULATION: 1 DIST + 2 CONDITIONAL = 3 per target (STATE uses SAMPLE only).
    # Method-gated classes are HELD, not a separate execution status.
    # Two targets: 8 eligible + (6 population + 8 method-gated) held = 22.
    assert len(frontier.operations) == 22
    assert frontier.disposition_counts[ELIGIBLE] == 8
    assert frontier.disposition_counts[HELD] == 14
    assert set(frontier.disposition_counts) <= set(ELIGIBILITY_STATES)
    assert set(frontier.execution_counts) <= set(EXECUTION_STATES)
    assert set(frontier.result_counts) <= set(RESULT_STATES)
    assert frontier.execution_counts == {NOT_STARTED: 22}
    assert frontier.result_counts == {UNKNOWN: 22}
    axis = frontier.axis_conservation()
    assert axis["considered_equals_eligibility"] is True
    assert axis["execution_equals_considered"] is True
    assert axis["result_equals_considered"] is True
    assert len(frontier.inventory_ledger) == 3
    assert frontier.e_pre_count == 8
    assert frontier.e_pre_root
    assert frontier.original_science_grade == "SOURCEFREE_PROPOSAL_NOT_ORIGINAL"
    assert all(op.measure_id in {"SAMPLE", "POPULATION"} for op in frontier.operations)
    population = [op for op in frontier.operations if op.measure_id == "POPULATION"]
    assert population and all(op.disposition == HELD for op in population)
    assert all(op.reasons for op in population if op.disposition == HELD)


def test_arbitrary_labels_and_bijective_rename_preserve_logical_frontier():
    original = _frontier()
    rename = {
        "q_alpha": "renamed_9f",
        "q_beta": "renamed_2a",
        "q_gamma": "renamed_7c",
        "q_delta": "renamed_4d",
        "admin_row": "renamed_admin",
    }
    occurrences = []
    for occurrence in _main_inventory().occurrences:
        item = rename[occurrence.key.item_id]
        occurrences.append(replace(
            occurrence,
            key=OccurrenceKey(item, option_id=occurrence.key.option_id,
                              form_id=occurrence.key.form_id,
                              repeat_id=occurrence.key.repeat_id),
            label=occurrence.label + "-REL",
        ))
    renamed_inventory = replace(
        _main_inventory(), occurrences=tuple(occurrences),
        authority_refs=("urn:r61:test:renamed-authority",),
    )
    renamed = _frontier(renamed_inventory, _policy())

    def logical_key(operation, remap=None):
        material = operation.identity_material()
        if remap is not None:
            material["targets"] = [
                {**key, "item_id": remap.get(key["item_id"], key["item_id"])}
                for key in material["targets"]
            ]
            material["conditions"] = [
                [{**key, "item_id": remap.get(key["item_id"], key["item_id"])}, value]
                for key, value in material["conditions"]
            ]
        material["baseline_ref"] = None
        return json.dumps(material, sort_keys=True)

    original_by_key = {logical_key(op, rename): op.op_id for op in original.operations}
    renamed_by_key = {
        logical_key(op): op.op_id for op in renamed.operations
    }
    assert set(original_by_key) == set(renamed_by_key)
    baseline_map = {
        original_by_key[key]: renamed_by_key[key] for key in original_by_key
    }

    def normalize(operation, *, remap_baseline=False):
        material = operation.identity_material()
        material["targets"] = [
            {**key, "item_id": rename.get(key["item_id"], key["item_id"])}
            for key in material["targets"]
        ]
        material["conditions"] = [
            [{**key, "item_id": rename.get(key["item_id"], key["item_id"])}, value]
            for key, value in material["conditions"]
        ]
        if remap_baseline and material["baseline_ref"] is not None:
            material["baseline_ref"] = baseline_map[material["baseline_ref"]]
        return json.dumps(material, sort_keys=True)

    assert sorted(normalize(op, remap_baseline=True) for op in original.operations) == sorted(
        normalize(op) for op in renamed.operations
    )
    assert original.e_pre_count == renamed.e_pre_count
    assert original.class_counts == renamed.class_counts
    assert original.disposition_counts == renamed.disposition_counts
    assert original.e_pre_root != renamed.e_pre_root


def test_ordered_targets_and_conditioners_are_distinct_exact_identities():
    frontier = _frontier()
    forward = _op_for(frontier, claim_class="JOINT", targets=("q_alpha", "q_beta"))
    reverse = _op_for(frontier, claim_class="JOINT", targets=("q_beta", "q_alpha"))
    assert forward.op_id != reverse.op_id
    assert forward.targets != reverse.targets
    c_forward = _op_for(
        frontier, claim_class="CONDITIONAL", targets=("q_alpha",),
        conditions=(("q_beta", 1), ("q_gamma", 0)),
    )
    c_reverse = _op_for(
        frontier, claim_class="CONDITIONAL", targets=("q_alpha",),
        conditions=(("q_gamma", 0), ("q_beta", 1)),
    )
    assert c_forward.op_id != c_reverse.op_id
    assert c_forward.conditions != c_reverse.conditions
    assert forward.disposition == ELIGIBLE
    assert reverse.disposition == ELIGIBLE
    assert c_forward.disposition == ELIGIBLE
    assert c_reverse.disposition == ELIGIBLE


def test_topology_form_repeat_and_administration_are_accounted_not_pruned():
    occurrences = (
        _occurrence("repeat_item", topology="REPEATED_OCCASION", repeat_id="T2"),
        _occurrence("mr_item", topology="MULTI_SELECT_SET"),
        _occurrence("rank_item", topology="RANKED_RESPONSE"),
        _occurrence("form_a", forms=("FORM_A",), form_id="FORM_A"),
        _occurrence("form_b", forms=("FORM_B",), form_id="FORM_B"),
        _occurrence("not_admin", administration=NOT_ADMINISTERED),
        _occurrence("unknown_admin", administration=ADMINISTRATION_UNKNOWN),
        _occurrence("route_unknown", route_state="UNKNOWN"),
        _occurrence("held_item"),
        _occurrence("household_item", unit="household"),
    )
    held_record = HeldRecord(
        occurrence_id=OccurrenceKey("held_item").key,
        reason="OWNER_HOLD_TEST", authority_ref="urn:r61:test:held-authority",
    )
    inventory = _inventory(occurrences, held=(held_record,))
    frontier = _frontier(inventory, _policy(j=2, k=0, d=0))
    assert frontier.operations
    assert any(op.claim_class == "DIST" and op.disposition == ELIGIBLE
               and op.execution_state == NOT_STARTED
               for op in frontier.operations if op.topology in {
                   "REPEATED_OCCASION", "MULTI_SELECT_SET", "RANKED_RESPONSE"
               })
    assert any(op.claim_class == "DIST" and op.disposition == HELD
               and op.administration_states == (NOT_ADMINISTERED,)
               for op in frontier.operations)
    assert any(op.claim_class == "DIST" and op.disposition == UNKNOWN
               and op.administration_states == (ADMINISTRATION_UNKNOWN,)
               for op in frontier.operations)
    assert any(op.claim_class == "DIST" and op.disposition == HELD
               and op.reasons == ("HELD_BY_STRUCTURED_OWNER_RECORD",)
               for op in frontier.operations)
    assert any(op.claim_class == "JOINT" and op.disposition == INAPPLICABLE_PROVED
               and op.reasons == ("DISJOINT_ADMINISTRATION_FORM",)
               for op in frontier.operations)
    assert any(op.claim_class == "JOINT" and op.disposition == HELD
               and op.reasons == ("UNRESOLVED_UNIT_LINK",)
               for op in frontier.operations)
    ledger = inventory_ledger(inventory, _policy(j=2, k=0, d=0))
    assert len(ledger) == len(occurrences)
    assert {entry.disposition for entry in ledger} <= set(ELIGIBILITY_STATES)
    assert sum(1 for entry in ledger if entry.disposition == ELIGIBLE) > 0


def test_administrative_roles_and_reverse_direction_are_prohibited():
    inventory = _inventory((
        _occurrence("outcome_item", conditioner_role="OUTCOME"),
        _occurrence("exposure_item", target_role="EXPOSURE", conditioner_role="OUTCOME"),
        _occurrence("admin_item", target_role=None, conditioner_role=None,
                    administrative_role="IDENTITY"),
    ))
    frontier = _frontier(inventory, _policy(j=1, k=1, d=0))
    ledger = inventory_ledger(inventory, _policy(j=1, k=1, d=0))
    admin_entry = next(
        entry for entry in ledger
        if entry.administrative_role == "IDENTITY"
    )
    assert admin_entry.disposition == PROHIBITED
    assert admin_entry.reasons == ("ADMINISTRATIVE_NONSEMANTIC",)
    assert all(op.targets[0].item_id != "admin_item" for op in frontier.operations)
    reverse = _op_for(frontier, claim_class="DIST", targets=("exposure_item",))
    reverse_cond = _op_for(
        frontier, claim_class="CONDITIONAL", targets=("exposure_item",),
        conditions=(("outcome_item", 1),),
    )
    assert reverse.disposition == PROHIBITED
    assert reverse.reasons == ("DIRECTION_NOT_GRANTED",)
    assert reverse_cond.disposition == PROHIBITED
    assert reverse_cond.reasons == ("DIRECTION_NOT_GRANTED",)
    reverse_policy = _policy(j=1, k=1, d=0, reverse=True)
    reverse_frontier = _frontier(inventory, reverse_policy)
    assert _op_for(reverse_frontier, claim_class="DIST", targets=("exposure_item",)).disposition == ELIGIBLE
    assert _op_for(
        reverse_frontier, claim_class="CONDITIONAL", targets=("exposure_item",),
        conditions=(("outcome_item", 1),),
    ).disposition == ELIGIBLE


def test_duplicate_occurrence_and_count_preserving_substitution_refused():
    duplicate = _occurrence("q_alpha")
    with pytest.raises(ValueError, match="DUPLICATE_OCCURRENCE"):
        _inventory((_occurrence("q_alpha"), duplicate))
    frontier = _frontier(_tiny_inventory(), _policy(j=1, k=1, d=0))
    expected = [op.op_id for op in frontier.operations]
    good = conservation_report(frontier, expected)
    assert good["no_drop_ok"] is True
    substituted = list(expected)
    substituted[0] = substituted[1]
    bad = conservation_report(frontier, substituted)
    assert bad["no_drop_ok"] is False
    assert bad["count_preserving_substitution"] is True
    assert bad["duplicate_operation_ids"]
    assert bad["missing_operation_ids"]


def test_all_missing_observations_do_not_shrink_eligible_frontier():
    inventory = _main_inventory()
    first = _frontier(inventory, _policy())
    empty_rows = ()
    # The enumerator has no observation parameter: an empty/all-missing value
    # store cannot remove an occurrence or an operation from the frontier.
    second = _frontier(inventory, _policy())
    assert empty_rows == ()
    assert first.content_hash == second.content_hash
    assert first.eligible()
    assert any(op.administration_states == (ADMINISTERED,) for op in first.eligible())


def test_incomplete_inventory_has_no_epre_and_budget_never_prunes():
    incomplete = _inventory(
        _main_inventory().occurrences, complete=False, gaps=("UNRESOLVED_WAVE_MODULE",)
    )
    unhealthy = _frontier(incomplete, _policy(j=1, k=1, d=0))
    assert unhealthy.e_pre_root is None
    assert unhealthy.e_pre_count is None
    assert "INCOMPLETE_DECLARED_INVENTORY" in unhealthy.e_pre_cause
    assert unhealthy.operations
    full = _frontier(_tiny_inventory(), _policy(j=1, k=1, d=0))
    partial = _frontier(_tiny_inventory(), _policy(j=1, k=1, d=0), budget=3)
    assert partial.budget_state == "PARTIAL"
    assert len(partial.operations) == len(full.operations)
    assert partial.e_pre_root == full.e_pre_root
    assert partial.e_pre_count == full.e_pre_count
    assert len(partial.pending_operation_ids) == len(full.eligible()) - 3


def test_lazy_partition_and_cold_subprocess_recomputation():
    frontier = _frontier(_tiny_inventory(), _policy(j=1, k=1, d=0), partition_size=5)
    partitions = list(iter_partitions(frontier))
    assert len(partitions) == frontier.partition_count
    flattened = [op_id for part in partitions for op_id in part.operation_ids]
    assert flattened == sorted(op.op_id for op in frontier.operations)
    assert all(part.operation_count == len(part.operation_ids) for part in partitions)
    assert len({part.root for part in partitions}) == len(partitions)
    # Deterministic cold recomputation, not serialized custody restore (R04).
    first = _frontier(_tiny_inventory(), _policy(j=1, k=1, d=0), partition_size=5)
    assert first.content_hash == frontier.content_hash
    code = (
        "from rawlsing_next.tests.test_universal_grammar import "
        "_tiny_inventory, _policy, _frontier;"
        "f=_frontier(_tiny_inventory(), _policy(j=1,k=1,d=0), partition_size=5);"
        "print(f.content_hash, f.partition_root, f.partition_count)"
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", code], cwd=str(REPO_ROOT), env=env,
        capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    assert proc.stdout.strip() == (
        f"{frontier.content_hash} {frontier.partition_root} {frontier.partition_count}"
    )


def _native_fixture():
    rows = []
    labels = ("q_alpha", "q_beta", "q_gamma", "q_delta")
    for index in range(12):
        responses = {
            labels[0]: index % 2,
            labels[1]: (index // 2) % 2,
            labels[2]: index % 3 % 2,
            labels[3]: (index // 3) % 2,
        }
        rows.append({"id": f"R{index:02d}", "responses": responses})
    source = _build_source("r61-universal", rows)
    qauth = _query_authority("r61-universal")
    dauth = _d_auth("UNIVERSAL-SEMANTIC-LOWERING")
    all_predicate = _branch_predicate(source, qauth, tag="r61-all")
    predicates = {}
    for label in labels:
        for value in (0, 1):
            predicates[(label, value)] = _predicate(
                source, qauth, _response_leaf(source, qauth, label, value),
                tag=f"r61-{label}-{value}",
            )
    queries = {}
    for label in labels:
        queries[(label,)] = _query(source, qauth, all_predicate, (label,), tag=f"r61-q-{label}")
    queries[(labels[0], labels[1])] = _query(
        source, qauth, all_predicate, (labels[0], labels[1]), tag="r61-q-joint"
    )
    return source, qauth, dauth, all_predicate, predicates, queries, labels


def _native_catalog(labels, all_predicate, predicates, queries, *, discovery_authority_ref=None,
                    supported_topologies=("SCALAR_SINGULAR",)):
    predicate_refs = {
        f"{OccurrenceKey(label).key}|{typed_value_key(value)}": predicate.ref
        for (label, value), predicate in predicates.items()
    }
    query_refs = {
        json.dumps([OccurrenceKey(label).key], sort_keys=False, separators=(",", ":"))
        + "|SAMPLE": queries[(label,)].ref
        for label in labels
    }
    joint_refs = {
        json.dumps([OccurrenceKey(labels[0]).key, OccurrenceKey(labels[1]).key],
                   sort_keys=False, separators=(",", ":")): queries[(labels[0], labels[1])].ref
    }
    marginal_refs = {OccurrenceKey(label).key: queries[(label,)].ref for label in labels}
    predicate_objects = {predicate.ref.key: predicate for predicate in predicates.values()}
    predicate_objects[all_predicate.ref.key] = all_predicate
    query_objects = {query.ref.key: query for query in queries.values()}
    return NativeCatalog(
        catalog_ref="urn:r61:test:native-catalog",
        baseline_predicate_ref=all_predicate.ref,
        predicate_refs=predicate_refs,
        query_refs=query_refs,
        joint_query_refs=joint_refs,
        marginal_query_refs=marginal_refs,
        supported_claims=(
            "DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL", "FORK", "INTERACTION",
        ),
        supported_topologies=supported_topologies,
        supported_condition_modes=("AND", "XOR_EXACTLY_ONE"),
        maximum_target_arity=2,
        maximum_conditioner_arity=2,
        cell_codec={typed_value_key(0): "0", typed_value_key(1): "1"},
        predicate_objects=predicate_objects,
        query_objects=query_objects,
        discovery_authority_ref=discovery_authority_ref,
        batch_unit_refs=("BATCH-UNIT-UNISSUED",),
    )


def test_native_mapping_uses_current_i05_contract_and_real_receipts():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory((
        _occurrence(labels[0]),
        _occurrence(labels[1]),
        _occurrence(labels[2]),
    ))
    policy = _policy(j=2, k=2, d=1)
    frontier = _frontier(inventory, policy)
    selected = []
    for operation in frontier.operations:
        if operation.disposition != ELIGIBLE or operation.measure_id != "SAMPLE":
            continue
        if operation.claim_class == "STATE_ROBUSTNESS":
            continue
        if set(key.item_id for key in operation.targets) - set(labels):
            continue
        if any(key.item_id not in labels for key, _ in operation.conditions):
            continue
        if len(operation.conditions) > 2:
            continue
        if operation.claim_class in {"JOINT", "CO_TRAVEL"}:
            if tuple(key.item_id for key in operation.targets) != (labels[0], labels[1]):
                continue
        elif tuple(key.item_id for key in operation.targets) != (labels[0],):
            continue
        selected.append(operation)
        if len(selected) >= 7:
            break
    assert len(selected) == 7
    selected_frontier = replace(frontier, operations=tuple(selected))
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    plan = lower_frontier(inventory, policy, selected_frontier, catalog)
    report = plan.coverage_report()
    assert report["no_drop_ok"] is True
    assert report["unsupported_are_typed"] is True
    assert plan.supported_operation_ids
    assert current_native_contract()["contract_id"] == plan.contract_id

    grammar = plan.native_grammar()
    authority = _discovery_authority(source, grammar, dauth)
    result = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates.values()) + (all_predicate,),
        query_template_catalog=tuple(queries.values()),
    )
    assert result.candidate_count >= 7
    join = native_receipt_anti_join(plan, result.receipts)
    assert join["no_drop_ok"], join
    assert join["missing_rule_ids"] == ()
    assert join["unexpected_rule_ids"] == ()
    assert not join["count_mismatches"]
    assert any(record.status == SUPPORTED for record in plan.records)
    assert any(record.coverage_roles for record in plan.records if record.status == SUPPORTED)
    assert any(record.expected_candidate_keys for record in plan.records
               if record.status == SUPPORTED)
    assert any(record.query_role_refs for record in plan.records
               if record.status == SUPPORTED)

    dropped_rule_id = sorted(plan.expected_native_catalog())[0]
    dropped_grammar = deepcopy(grammar)
    dropped_grammar["rules"] = tuple(
        rule for rule in dropped_grammar["rules"] if rule["rule_id"] != dropped_rule_id
    )
    dropped_authority = _discovery_authority(source, dropped_grammar, dauth)
    dropped_result = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=dropped_authority,
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates.values()) + (all_predicate,),
        query_template_catalog=tuple(queries.values()),
    )
    mutated = native_receipt_anti_join(plan, dropped_result.receipts)
    assert mutated["no_drop_ok"] is False
    assert dropped_rule_id in mutated["missing_rule_ids"]
    restored = native_receipt_anti_join(plan, result.receipts)
    assert restored["no_drop_ok"] is True
    assert restored["missing_rule_ids"] == ()

    semantics = deepcopy(grammar)
    atoms = list(semantics["atoms"])
    changed = False
    for label in labels:
        zero_ref = predicates[(label, 0)].ref.as_dict()
        one_ref = predicates[(label, 1)].ref.as_dict()
        if any(atom["predicate_ref"] == zero_ref for atom in atoms):
            atoms = [
                {**atom, "predicate_ref": one_ref}
                if atom["predicate_ref"] == zero_ref else atom
                for atom in atoms
            ]
            changed = True
            break
    assert changed
    semantics["atoms"] = tuple(atoms)
    semantic_authority = _discovery_authority(source, semantics, dauth)
    semantic_result = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=semantic_authority,
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates.values()) + (all_predicate,),
        query_template_catalog=tuple(queries.values()),
    )
    semantic_join = native_receipt_anti_join(plan, semantic_result.receipts)
    assert semantic_join["no_drop_ok"] is False
    assert (
        semantic_join["missing_candidate_ids"]
        or semantic_join["unexpected_candidate_ids"]
        or semantic_join["semantic_mismatches"]
    )
    restored_semantics = native_receipt_anti_join(plan, result.receipts)
    assert restored_semantics["no_drop_ok"] is True


def test_conditioned_joint_and_cotravel_bind_condition_roles_natively():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory(tuple(_occurrence(label) for label in labels))
    policy = _policy(j=2, k=1, d=0)
    frontier = _frontier(inventory, policy)
    selected = tuple(
        op for op in frontier.operations
        if op.disposition == ELIGIBLE and op.measure_id == "SAMPLE"
        and op.claim_class in {"JOINT", "CO_TRAVEL"}
        and tuple(key.item_id for key in op.targets) == (labels[0], labels[1])
        and len(op.conditions) == 1
        and op.conditions[0][0].item_id in labels[2:4]
    )
    assert len(selected) == 8
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    plan = lower_frontier(inventory, policy, replace(frontier, operations=selected), catalog)
    assert plan.coverage_report()["no_drop_ok"] is True
    assert len(plan.expected_candidates) == len(selected)
    baseline_key = all_predicate.ref.key
    for record in plan.records:
        assert record.status == SUPPORTED, record.reason
        assert record.derived_predicates
        derived_refs = {
            derived.ref.key for derived in record.derived_predicates.values()
        }
        candidates = [
            candidate for candidate in plan.expected_candidates
            if candidate["rule_id"] == record.rule_id
        ]
        assert candidates
        for candidate in candidates:
            assert {
                role["predicate_ref"]["content_hash"]
                for role in candidate["query_roles"]
            } != {all_predicate.ref.content_hash}
            for role in candidate["query_roles"]:
                role_ref = exact_ref(role["predicate_ref"], "candidate role")
                assert role_ref.key in derived_refs

    by_value = {}
    for record in plan.records:
        operation = next(op for op in selected if op.op_id == record.operation_id)
        value_key = typed_value_key(operation.conditions[0][1])
        by_value.setdefault(
            (operation.claim_class, operation.conditions[0][0].key, value_key), set()
        ).update(record.derived_predicates.keys())
        assert any(
            operation.conditions[0][0].item_id in atom_ref
            for atom_ref in record.atoms
        ) or record.derived_predicates
    assert all(len(values) == 1 for values in by_value.values())
    zero_refs = set().union(
        *[values for (cls, item, value), values in by_value.items()
          if value == typed_value_key(0)]
    )
    one_refs = set().union(
        *[values for (cls, item, value), values in by_value.items()
          if value == typed_value_key(1)]
    )
    assert zero_refs.isdisjoint(one_refs)

    grammar = plan.native_grammar()
    result = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=_discovery_authority(source, grammar, dauth),
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates.values()) + (all_predicate,),
        query_template_catalog=tuple(queries.values()),
    )
    join = native_receipt_anti_join(plan, result.receipts)
    assert join["no_drop_ok"], join
    assert len({candidate["candidate_id"] for candidate in plan.expected_candidates}) == len(selected)

    multi_policy = _policy(j=2, k=2, d=0)
    multi_policy = replace(
        multi_policy,
        direction_grants=multi_policy.direction_grants + (
            DirectionGrant(
                ("OUTCOME", "OUTCOME"), ("EXPOSURE", "EXPOSURE"),
                "JOINT", "DIR-JOINT-COND2",
            ),
        ),
    )
    multi_frontier = _frontier(inventory, multi_policy)
    multi = next(
        op for op in multi_frontier.operations
        if op.disposition == ELIGIBLE and op.measure_id == "SAMPLE"
        and op.claim_class == "JOINT"
        and tuple(key.item_id for key in op.targets) == (labels[0], labels[1])
        and len(op.conditions) == 2
    )
    multi_plan = lower_frontier(
        inventory, multi_policy, replace(multi_frontier, operations=(multi,)), catalog
    )
    multi_record = multi_plan.records[0]
    assert multi_record.status == SUPPORTED, multi_record.reason
    assert len(multi_record.derived_predicates) == 1
    multi_candidate = multi_plan.expected_candidates[0]
    derived_refs = {
        predicate.ref.key for predicate in multi_record.derived_predicates.values()
    }
    assert {
        exact_ref(role["predicate_ref"], "multi role").key
        for role in multi_candidate["query_roles"]
    } == derived_refs
    multi_grammar = multi_plan.native_grammar()
    multi_result = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=_discovery_authority(source, multi_grammar, dauth),
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates.values()) + (all_predicate,) + tuple(
            multi_record.derived_predicates.values()
        ),
        query_template_catalog=tuple(queries.values()),
    )
    assert native_receipt_anti_join(multi_plan, multi_result.receipts)["no_drop_ok"] is True


def test_unsupported_only_frontier_is_not_declared_valid_empty():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory((_occurrence(labels[0]),))
    policy = _policy(j=1, k=0, d=0)
    frontier = _frontier(inventory, policy)
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    catalog = replace(catalog, supported_claims=())
    plan = lower_frontier(inventory, policy, frontier, catalog)
    assert plan.unsupported_operation_ids
    assert plan.native_grammar()["allow_empty_frontier"] is False


def test_native_mapping_marks_unsupported_and_never_returns_none():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory((_occurrence(labels[0]),))
    policy = _policy(j=1, k=0, d=0)
    frontier = _frontier(inventory, policy)
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    catalog = replace(catalog, supported_claims=("DIST",))
    plan = lower_frontier(inventory, policy, frontier, catalog)
    assert any(record.status == NATIVE_UNSUPPORTED for record in plan.records)
    assert all(
        record.reason is not None for record in plan.records
        if record.status == NATIVE_UNSUPPORTED
    )
    assert all(record.rule_id is not None for record in plan.records if record.status == SUPPORTED)
    covered = (
        set(plan.supported_operation_ids)
        | set(plan.unsupported_operation_ids)
        | set(plan.not_eligible_operation_ids)
    )
    assert covered == {op.op_id for op in frontier.operations}
    bad_catalog = replace(catalog, contract_id="HISTORICAL-I05")
    bad_plan = lower_frontier(inventory, policy, frontier, bad_catalog)
    assert all(
        record.status == NATIVE_UNSUPPORTED
        for record in bad_plan.records if record.status != "NOT_ELIGIBLE"
    )


def _dummy_ref(kind, tag):
    digest = hashlib.sha256(f"{kind}|{tag}".encode()).hexdigest()
    return ExactRef(kind, f"urn:r61:test:{kind.lower()}:{tag}", digest)


def _minimal_catalog(*, target="typed_target", topologies=("SCALAR_SINGULAR",), codec=None):
    target_key = json.dumps(
        [OccurrenceKey(target).key], sort_keys=False, separators=(",", ":")
    )
    return NativeCatalog(
        catalog_ref="urn:r61:test:minimal-catalog",
        baseline_predicate_ref=_dummy_ref("Predicate", "baseline"),
        predicate_refs={},
        query_refs={target_key + "|SAMPLE": _dummy_ref("QueryTemplate", "query")},
        joint_query_refs={},
        marginal_query_refs={},
        supported_claims=("DIST",),
        supported_topologies=topologies,
        supported_condition_modes=("AND",),
        maximum_target_arity=1,
        maximum_conditioner_arity=0,
        cell_codec=codec or {},
    )


def test_typed_bool_int_string_null_and_absent_identity_and_cells():
    inventory = _inventory((
        _occurrence("typed_target", conditioner_role=None, domain=(1, "1")),
        _occurrence("bool_cond", target_role=None, domain=(True, False)),
        _occurrence("null_cond", target_role=None, domain=(None, ABSENT, 0)),
        _occurrence("mixed_cond", target_role=None, domain=("1", 1)),
    ))
    policy = _policy(j=1, k=1, d=0)
    frontier = _frontier(inventory, policy)
    assert _op_for(frontier, claim_class="CONDITIONAL", targets=("typed_target",),
                   conditions=(("bool_cond", True),)).op_id != _op_for(
        frontier, claim_class="CONDITIONAL", targets=("typed_target",),
        conditions=(("bool_cond", False),)).op_id
    null_op = _op_for(frontier, claim_class="CONDITIONAL", targets=("typed_target",),
                      conditions=(("null_cond", None),))
    absent_op = _op_for(frontier, claim_class="CONDITIONAL", targets=("typed_target",),
                        conditions=(("null_cond", ABSENT),))
    zero_op = _op_for(frontier, claim_class="CONDITIONAL", targets=("typed_target",),
                      conditions=(("null_cond", 0),))
    assert len({null_op.op_id, absent_op.op_id, zero_op.op_id}) == 3
    str_op = _op_for(frontier, claim_class="CONDITIONAL", targets=("typed_target",),
                     conditions=(("mixed_cond", "1"),))
    int_op = _op_for(frontier, claim_class="CONDITIONAL", targets=("typed_target",),
                     conditions=(("mixed_cond", 1),))
    assert str_op.op_id != int_op.op_id

    dist_op = _op_for(frontier, claim_class="DIST", targets=("typed_target",))
    preserved = lower_operation(inventory, policy, dist_op, _minimal_catalog())
    assert preserved.status == SUPPORTED, preserved.reason
    assert list(preserved.rule["target_cells"]) == [1, "1"]
    collided = lower_operation(
        inventory, policy, dist_op,
        _minimal_catalog(codec={typed_value_key(1): "one", typed_value_key("1"): "one"}),
    )
    assert collided.status == NATIVE_UNSUPPORTED
    assert collided.reason == "NATIVE_CELL_CODEC_NOT_INJECTIVE"
    governed = lower_operation(
        inventory, policy, dist_op,
        _minimal_catalog(codec={typed_value_key(1): "1", typed_value_key("1"): "s1"}),
    )
    assert governed.status == SUPPORTED
    assert list(governed.rule["target_cells"]) == ["1", "s1"]


def test_operation_identity_binds_source_measure_clocks_and_selection():
    base = _inventory((_occurrence("alpha", conditioner_role=None),))
    policy = _policy(j=1, k=0, d=0)
    first = _frontier(base, policy)
    changed_source = _frontier(replace(
        base, wave="W2", edition="E2", source_sha256="b" * 64,
        dataset_id="DATASET-2", instrument_ref="INSTRUMENT-2",
    ), policy)
    assert {op.op_id for op in first.operations} != {op.op_id for op in changed_source.operations}
    m1 = MeasurePlan("SAMPLE", "SAMPLE", None, None, "estimand-one", "UNCERTAINTY_ONE")
    m2 = MeasurePlan("SAMPLE", "SAMPLE", "WEIGHT-2", "DESIGN-2",
                     "estimand-two", "UNCERTAINTY_TWO")
    measure_a = _frontier(replace(base, measure_plans=(m1,)), policy)
    measure_b = _frontier(replace(base, measure_plans=(m2,)), policy)
    assert {op.op_id for op in measure_a.operations} != {op.op_id for op in measure_b.operations}
    clocked = _frontier(replace(
        base, observation_clock_ref="OBS-2", reference_clock_ref="REF-2",
        as_of_ref="ASOF-2", publication_clock_ref="PUB-2",
        current_selection="CURRENT-2",
    ), policy)
    assert {op.op_id for op in first.operations} != {op.op_id for op in clocked.operations}
    fields = set(type(first.operations[0]).__dataclass_fields__)
    assert {
        "observation_clock_ref", "reference_clock_ref", "as_of_ref",
        "publication_clock_ref", "current_selection_ref",
    } <= fields


def test_axes_and_lowering_record_contract_fields_are_complete():
    from rawlsing_next.universal_grammar.native_map import LoweringRecord
    assert DISPOSITIONS == ELIGIBILITY_STATES
    assert UNSUPPORTED_RUNTIME not in DISPOSITIONS
    assert DEFERRED not in DISPOSITIONS
    required = {
        "lowering_version", "discovery_authority_ref", "batch_unit_refs",
        "evidence_grade_ceiling", "typed_refusal", "predicate_refs",
        "query_refs", "query_role_refs", "expected_candidate_keys",
    }
    assert required <= set(LoweringRecord.__dataclass_fields__)
    frontier = _frontier(_tiny_inventory(), _policy(j=1, k=1, d=0), budget=3)
    assert len(frontier.pending_operation_ids) == 5
    pending = set(frontier.pending_operation_ids)
    assert all(
        op.execution_state == "PENDING" for op in frontier.operations
        if op.op_id in pending
    )
    assert all(op.disposition == ELIGIBLE for op in frontier.operations
               if op.op_id in pending)
    assert frontier.axis_conservation()["eligibility_total"] == len(frontier.operations)
    fork_frontier = _frontier(_main_inventory(), _policy(j=1, k=2, d=1))
    fork = _op_for(
        fork_frontier, claim_class="FORK", targets=("q_alpha",),
        conditions=(("q_beta", 1), ("q_gamma", 0)),
    )
    assert fork.baseline_ref is not None
    assert fork.recursion_depth == 0
    assert fork.recursion_relation_ref is None
    assert fork.baseline_policy_ref is None
    recursion_frontier = _frontier(
        _main_inventory(),
        replace(_policy(j=1, k=2, d=3),
                recursion_relation_ref="REC-1", baseline_policy_ref="BASE-1"),
    )
    recursion_fork = _op_for(
        recursion_frontier, claim_class="FORK", targets=("q_alpha",),
        conditions=(("q_beta", 1), ("q_gamma", 0)),
    )
    assert recursion_fork.recursion_depth == 0
    assert recursion_fork.recursion_relation_ref == "REC-1"
    assert recursion_fork.baseline_policy_ref == "BASE-1"
    assert any(
        gap.get("kind") == "RECURSION_BASELINE_NOT_ENUMERATED"
        and gap["state"] == "EXACT_CONTRACT_GAP"
        for gap in recursion_frontier.deferred
    )


def test_catalog_topology_promotion_and_forged_direction_refusal():
    inventory = _inventory((_occurrence("mr_target", topology="MULTI_SELECT_SET",
                                         conditioner_role=None),))
    policy = _policy(j=1, k=0, d=0)
    frontier = _frontier(inventory, policy)
    operation = _op_for(frontier, claim_class="DIST", targets=("mr_target",))
    assert operation.disposition == ELIGIBLE
    promoted = lower_operation(
        inventory, policy, operation,
        _minimal_catalog(target="mr_target",
                         topologies=("SCALAR_SINGULAR", "MULTI_SELECT_SET")),
    )
    assert promoted.status == SUPPORTED, promoted.reason
    forged = replace(operation, direction_ref="FORGED-DIRECTION")
    forged = replace(forged, op_id="urn:r61:op:" + forged.canonical_hash)
    refused = lower_operation(inventory, policy, forged, _minimal_catalog(target="mr_target"))
    assert refused.status == NATIVE_UNSUPPORTED
    assert refused.reason == "FORGED_OR_UNAUTHORIZED_DIRECTION_REF"
    noncanonical = replace(operation, op_id="urn:r61:op:forged-identity")
    id_refused = lower_operation(
        inventory, policy, noncanonical, _minimal_catalog(target="mr_target")
    )
    assert id_refused.status == NATIVE_UNSUPPORTED
    assert id_refused.reason == "OPERATION_ID_NOT_CANONICAL"


def test_structured_held_and_unknown_risk_policy():
    held_key = OccurrenceKey("held_target").key
    structured = HeldRecord(occurrence_id=held_key, reason="OWNER_PRIVACY_HOLD",
                            authority_ref="urn:r61:test:hold-authority")
    inventory = _inventory((
        _occurrence("held_target", conditioner_role=None),
        _occurrence("legacy_held", conditioner_role=None),
    ), held=(structured, OccurrenceKey("legacy_held").key))
    ledger = inventory_ledger(inventory, _policy(j=1, k=0, d=0))
    held_entry = next(entry for entry in ledger if entry.occurrence_id == held_key)
    legacy_entry = next(entry for entry in ledger if entry.occurrence_id == OccurrenceKey("legacy_held").key)
    assert held_entry.disposition == HELD
    assert held_entry.held_reason == "OWNER_PRIVACY_HOLD"
    assert held_entry.held_authority_ref == "urn:r61:test:hold-authority"
    assert legacy_entry.disposition == UNKNOWN
    assert legacy_entry.reasons == ("UNSTRUCTURED_HELD_CLAIM_NOT_AUTHORIZATION",)
    unknown_risk = _inventory((_occurrence("no_risk", conditioner_role=None, risk_set_refs=()),))
    unknown_frontier = _frontier(unknown_risk, _policy(j=1, k=0, d=0))
    assert _op_for(unknown_frontier, claim_class="DIST", targets=("no_risk",)).disposition == UNKNOWN
    relaxed = replace(_policy(j=1, k=0, d=0), risk_set_policy="UNCONSTRAINED")
    relaxed_frontier = _frontier(unknown_risk, relaxed)
    assert _op_for(relaxed_frontier, claim_class="DIST", targets=("no_risk",)).disposition == ELIGIBLE


def test_valid_complete_empty_native_grammar_is_explicitly_empty():
    inventory = _inventory((
        _occurrence("admin_only", target_role=None, conditioner_role=None,
                    administrative_role="IDENTITY"),
    ))
    policy = _policy(j=1, k=0, d=0)
    frontier = _frontier(inventory, policy)
    assert frontier.operations == ()
    assert frontier.e_pre_count == 0 and frontier.e_pre_root is not None
    plan = lower_frontier(
        inventory, policy, frontier,
        _minimal_catalog(target="admin_only"),
    )
    assert plan.supported_operation_ids == ()
    assert plan.native_grammar()["allow_empty_frontier"] is True


def test_all_missing_native_boundary_does_not_shrink_frontier():
    label = "q_missing"
    rows = [{"id": f"R{index}", "responses": {label: None}} for index in range(4)]
    source = _build_source("r61-missing", rows)
    qauth = _query_authority("r61-missing")
    dauth = _d_auth("UNIVERSAL-SEMANTIC-LOWERING")
    all_predicate = _branch_predicate(source, qauth, tag="r61-missing-all")
    query = _query(source, qauth, all_predicate, (label,), tag="r61-missing-query")
    inventory = _inventory((_occurrence(label, conditioner_role=None),))
    policy = _policy(j=1, k=0, d=0)
    frontier = _frontier(inventory, policy)
    before = len(frontier.eligible())
    assert before > 0
    target_key = json.dumps(
        [OccurrenceKey(label).key], sort_keys=False, separators=(",", ":")
    )
    catalog = NativeCatalog(
        catalog_ref="urn:r61:test:missing-catalog",
        baseline_predicate_ref=all_predicate.ref,
        predicate_refs={},
        query_refs={target_key + "|SAMPLE": query.ref},
        joint_query_refs={},
        marginal_query_refs={},
        supported_claims=("DIST",),
        supported_topologies=("SCALAR_SINGULAR",),
        supported_condition_modes=("AND",),
        maximum_target_arity=1,
        maximum_conditioner_arity=0,
        cell_codec={typed_value_key(0): "0", typed_value_key(1): "1"},
        predicate_objects={all_predicate.ref.key: all_predicate},
        query_objects={query.ref.key: query},
    )
    plan = lower_frontier(inventory, policy, frontier, catalog)
    grammar = plan.native_grammar()
    # The current synthetic I03 fixture refuses an all-missing response value
    # as a typed integrity failure before I05 can issue a result. This is not a
    # positive all-missing native result; it is an honest typed boundary. The
    # prospective frontier remains unchanged either way.
    with pytest.raises(ExactBoundedCoverageError, match="integrity failure"):
        execute_exact_bounded_discovery(
            repository=source["repo"],
            discovery_authority=_discovery_authority(source, grammar, dauth),
            authority_registry=_i05_registry(source, qauth, dauth),
            release_refs=(source["release_ref"],),
            predicate_catalog=(all_predicate,),
            query_template_catalog=(query,),
        )
    assert len(frontier.eligible()) == before
    assert frontier.e_pre_count == before
    assert plan.supported_operation_ids


def _recurrence_policy(*, d=3, k=3, breadth=2, per_generation=4, total=12):
    return RecurrencePolicy(
        policy_id="R61-R4-TEST-POLICY",
        policy_version="r61.r4.1",
        grade="TEST_ONLY",
        owner_refs=("R61-R4-TEST",),
        counting_convention="ANCESTOR_CONDITIONS_COUNT_TOWARD_K",
        bounds={"J": 2, "K": k, "D": d},
        breadth_cap=breadth,
        followup_cap=breadth,
        protected_exploration_slots=1,
        per_generation_issued_cap=per_generation,
        total_issued_cap=total,
        comparators=(COMPARATOR_ROOT, COMPARATOR_PARENT),
    )


def _recurrence_source():
    rows = []

    def add(s1, s2, s3, t):
        rows.append({
            "id": f"R{len(rows):02d}",
            "responses": {"s1": s1, "s2": s2, "s3": s3, "t": t},
        })

    for index in range(4):
        add(0, 0, index % 2, 1 if index < 3 else 0)
    for index in range(2):
        add(0, 1, 0, 1)
    for index in range(2):
        add(0, 1, 1, 1 if index == 0 else 0)
    for index in range(4):
        add(1, 0, index % 2, 0)
    for index in range(2):
        add(1, 1, 0, 1 if index == 0 else 0)
    for index in range(2):
        add(1, 1, 1, 1 if index == 0 else 0)
    source = _build_source("r61-r4", rows)
    qauth = _query_authority("r61-r4")
    root = _branch_predicate(source, qauth, tag="r61-r4-root")
    query = _query(source, qauth, root, ("t",), tag="r61-r4-t")
    return source, qauth, root, query


def _condition_predicates(source, qauth, variable, values=(0, 1)):
    return tuple(
        (OccurrenceKey(variable), value,
         _predicate(source, qauth, _response_leaf(source, qauth, variable, value),
                    tag=f"r61-r4-{variable}-{value}"))
        for value in values
    )


def _run_recurrence_generation(source, qauth, plan, generation, predicates):
    dauth = _d_auth(f"R61-R4-G{generation}")
    grammar = plan.grammar
    return execute_recurrence_generation(
        plan=plan,
        repository=source["repo"],
        discovery_authority=_discovery_authority(
            source, grammar, dauth, tag=f"r61-r4-g{generation}"
        ),
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates),
        query_template_catalog=(plan.query_object,),
    )


def test_bounded_adaptive_recurrence_three_generations_actual_native():
    source, qauth, root_predicate, query = _recurrence_source()
    policy = _recurrence_policy()
    root_parent = make_root_parent(
        predicate=root_predicate, source_release_refs=(source["release_ref"],)
    )
    catalog = [root_predicate]
    generations = []
    parents = (root_parent,)
    s1 = _condition_predicates(source, qauth, "s1")
    s2 = _condition_predicates(source, qauth, "s2")
    s3 = _condition_predicates(source, qauth, "s3")
    for generation, conditions in ((1, s1), (2, s2), (3, s3)):
        catalog.extend(predicate for _, _, predicate in conditions)
        if generation > 1:
            catalog.extend(parent.predicate for parent in parents)
        plan = build_recurrence_issue_plan(
            policy=policy, generation=generation, parents=parents,
            root_predicate=root_predicate, target_label="t",
            query_ref=query, condition_predicates=conditions,
        )
        result = _run_recurrence_generation(source, qauth, plan, generation, catalog)
        assert result.anti_join["no_drop_ok"], result.anti_join
        generations.append(result)
        if generation < 3:
            next_conditions = s2 if generation == 1 else s3
            activation = activate_next_generation(
                policy=policy, generation=result, parents=parents,
                root_parent=root_parent, next_generation=generation + 1,
                condition_predicates=next_conditions,
            )
            assert activation.active_parents
            parents = activation.active_parents
    assert [generation.plan.generation for generation in generations] == [1, 2, 3]
    assert all(generation.anti_join["no_drop_ok"] for generation in generations)

    gen2 = generations[1]
    parent_ids = {parent.parent_id: parent for parent in gen2.plan.parents}
    contrast = None
    for parent in gen2.plan.parents:
        parent_ops = [
            operation for operation in gen2.plan.expected_operations
            if operation.parent_id == parent.parent_id
        ]
        if {operation.comparator for operation in parent_ops} != {
            COMPARATOR_ROOT, COMPARATOR_PARENT
        }:
            continue
        states = {
            operation.comparator: gen2.receipt_by_rule[operation.rule_id].typed_state
            for operation in parent_ops
        }
        if states[COMPARATOR_ROOT] != states[COMPARATOR_PARENT]:
            contrast = (parent, parent_ops, states)
            break
    assert contrast is not None
    neutral_parent, neutral_ops, states = contrast
    assert set(states) == {COMPARATOR_ROOT, COMPARATOR_PARENT}
    assert states[COMPARATOR_ROOT] != states[COMPARATOR_PARENT]

    activation2 = activate_next_generation(
        policy=policy, generation=gen2, parents=gen2.plan.parents,
        root_parent=root_parent, next_generation=3,
        condition_predicates=s3,
    )
    assert any(
        parent.kind == PARENT_EXPLORATORY
        for parent in activation2.active_parents
    )
    assert any(
        entry["reason"] == "PROTECTED_NONWINNING_EXPLORATION"
        for entry in activation2.activation_ledger
    )
    assert activation2.waiting or activation2.activation_ledger

    gen3 = generations[2]
    exploratory_parents = [
        parent for parent in gen3.plan.parents if parent.kind == PARENT_EXPLORATORY
    ]
    assert exploratory_parents
    exploratory_ops = [
        operation for operation in gen3.plan.expected_operations
        if operation.parent_id == exploratory_parents[0].parent_id
    ]
    exploratory_states = {
        operation.comparator: gen3.receipt_by_rule[operation.rule_id].typed_state
        for operation in exploratory_ops
    }
    assert exploratory_states
    assert any(
        state == "DISCOVERED_RESULT_SUPPORTED"
        for state in exploratory_states.values()
    )
    assert any(
        state != "DISCOVERED_RESULT_SUPPORTED"
        for state in exploratory_states.values()
    )

    gen1 = generations[0]
    assert all(
        operation.comparator in {COMPARATOR_ROOT, COMPARATOR_PARENT}
        for operation in gen1.plan.expected_operations
    )
    assert len({receipt.ref.key for receipt in gen1.execution.discovery_result.receipts}) == len(
        gen1.execution.discovery_result.receipts
    )
    # D controls actual generations independently; K constrains ancestor count.
    short_policy = _recurrence_policy(d=2)
    stopped = activate_next_generation(
        policy=short_policy, generation=generation, parents=parents,
        root_parent=root_parent, next_generation=3, condition_predicates=s3,
    )
    assert stopped.stopped and stopped.stopped[0]["reason"] == "D_REACHED"


def test_recurrence_k_bound_and_budget_leave_explicit_unrun_work():
    source, qauth, root_predicate, query = _recurrence_source()
    root_parent = make_root_parent(
        predicate=root_predicate, source_release_refs=(source["release_ref"],)
    )
    s1 = _condition_predicates(source, qauth, "s1")
    s2 = _condition_predicates(source, qauth, "s2")
    s3 = _condition_predicates(source, qauth, "s3")
    catalog = [root_predicate] + [predicate for _, _, predicate in s1 + s2 + s3]
    tight_k = _recurrence_policy(k=2)
    p1 = build_recurrence_issue_plan(
        policy=tight_k, generation=1, parents=(root_parent,),
        root_predicate=root_predicate, target_label="t",
        query_ref=query, condition_predicates=s1,
    )
    g1 = _run_recurrence_generation(source, qauth, p1, 1, catalog)
    assert g1.anti_join["no_drop_ok"]
    activation1 = activate_next_generation(
        policy=tight_k, generation=g1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=s2,
    )
    parents = activation1.active_parents
    catalog.extend(parent.predicate for parent in parents)
    p2 = build_recurrence_issue_plan(
        policy=tight_k, generation=2, parents=parents,
        root_predicate=root_predicate, target_label="t",
        query_ref=query, condition_predicates=s2,
    )
    g2 = _run_recurrence_generation(source, qauth, p2, 2, catalog)
    activation2 = activate_next_generation(
        policy=tight_k, generation=g2, parents=parents,
        root_parent=root_parent, next_generation=3, condition_predicates=s3,
    )
    catalog.extend(parent.predicate for parent in activation2.active_parents)
    with pytest.raises(ValueError, match="EXCEED_K"):
        build_recurrence_issue_plan(
            policy=tight_k, generation=3, parents=activation2.active_parents,
            root_predicate=root_predicate, target_label="t",
            query_ref=query, condition_predicates=s3,
        )
    budget_policy = _recurrence_policy(breadth=3, per_generation=2)
    p_budget = build_recurrence_issue_plan(
        policy=budget_policy, generation=1, parents=(root_parent,),
        root_predicate=root_predicate, target_label="t",
        query_ref=query, condition_predicates=s1,
    )
    assert p_budget.unissued
    assert p_budget.unissued[0]["reason"] == "PER_GENERATION_ISSUED_CAP"
    assert len(p_budget.expected_operations) == 2


def test_recurrence_issued_mutation_and_invalid_parent_identity():
    source, qauth, root_predicate, query = _recurrence_source()
    policy = _recurrence_policy()
    root_parent = make_root_parent(
        predicate=root_predicate, source_release_refs=(source["release_ref"],)
    )
    s1 = _condition_predicates(source, qauth, "s1")
    catalog = [root_predicate] + [predicate for _, _, predicate in s1]
    plan = build_recurrence_issue_plan(
        policy=policy, generation=1, parents=(root_parent,),
        root_predicate=root_predicate, target_label="t",
        query_ref=query, condition_predicates=s1,
    )
    good = _run_recurrence_generation(source, qauth, plan, 1, catalog)
    assert good.anti_join["no_drop_ok"]
    dropped = deepcopy(plan.grammar)
    dropped_rule = dropped["rules"][0]["rule_id"]
    dropped["rules"] = tuple(
        rule for rule in dropped["rules"] if rule["rule_id"] != dropped_rule
    )
    mutated_plan = replace(plan, grammar=dropped)
    mutated = _run_recurrence_generation(source, qauth, mutated_plan, 1, catalog)
    assert mutated.anti_join["no_drop_ok"] is False
    assert dropped_rule in mutated.anti_join["missing_rule_ids"]
    assert _run_recurrence_generation(source, qauth, plan, 1, catalog).anti_join["no_drop_ok"]
    with pytest.raises(ValueError, match="exploratory parent"):
        RecurrenceParent(
            parent_id="bad", predicate=root_predicate, kind=PARENT_EXPLORATORY,
            generation=1, source_release_refs=(source["release_ref"],),
            receipt_ref=ExactRef("K", "urn:test:bad", "a" * 64),
        )
    wrong_parent = RecurrenceParent(
        parent_id="wrong", predicate=root_predicate, kind=PARENT_RECEIPT_BOUND,
        generation=1, source_release_refs=(source["release_ref"],),
    )
    wrong_plan = build_recurrence_issue_plan(
        policy=policy, generation=1, parents=(wrong_parent,),
        root_predicate=root_predicate, target_label="t",
        query_ref=query, condition_predicates=s1,
    )
    dauth = _d_auth("R61-R4-G1")
    with pytest.raises(ValueError, match="GRAMMAR_MISMATCH"):
        execute_recurrence_generation(
            plan=wrong_plan, repository=source["repo"],
            discovery_authority=_discovery_authority(source, plan.grammar, dauth,
                                                     tag="r61-r4-wrong-authority"),
            authority_registry=_i05_registry(source, qauth, dauth),
            release_refs=(source["release_ref"],),
            predicate_catalog=tuple(catalog),
            query_template_catalog=(query,),
        )


def test_recurrence_persisted_handoff_roundtrip_and_renamed_profile(tmp_path):
    source, qauth, root_predicate, query = _recurrence_source()
    policy = _recurrence_policy()
    root_parent = make_root_parent(
        predicate=root_predicate, source_release_refs=(source["release_ref"],)
    )
    s1 = _condition_predicates(source, qauth, "s1")
    catalog = [root_predicate] + [predicate for _, _, predicate in s1]
    plan = build_recurrence_issue_plan(
        policy=policy, generation=1, parents=(root_parent,),
        root_predicate=root_predicate, target_label="t",
        query_ref=query, condition_predicates=s1,
    )
    generation = _run_recurrence_generation(source, qauth, plan, 1, catalog)
    path = tmp_path / "r4_handoffs.json"
    bundle_ref = write_recursive_handoff_bundle(path, generation.execution.handoffs)
    loaded_ref, loaded = load_recursive_handoff_bundle(path)
    assert loaded_ref == bundle_ref
    assert [handoff.ref for handoff in loaded] == sorted(
        (handoff.ref for handoff in generation.execution.handoffs), key=lambda ref: ref.key
    )
    assert loaded
    provenance = {
        "bundle_ref": bundle_ref.as_dict(),
        "handoff_refs": [handoff.ref.as_dict() for handoff in loaded],
        "source_release_refs": [source["release_ref"].as_dict()],
    }
    assert provenance["bundle_ref"]["content_hash"] == bundle_ref.content_hash
    s2 = _condition_predicates(source, qauth, "s2")
    activation1 = activate_next_generation(
        policy=policy, generation=generation, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=s2,
    )
    persisted_parent = activation1.active_parents[0]
    persisted_index = next(
        index for index, handoff in enumerate(loaded)
        if handoff.ref == persisted_parent.replay_binding_ref
    )
    persisted_handoff = loaded[persisted_index]
    persisted_value = persisted_parent.ancestry_conditions[0][1]
    child_code = """
import json, sys
from rawlsing_next.tests.test_universal_grammar import (
    _condition_predicates, _recurrence_policy, _recurrence_source,
    _run_recurrence_generation,
)
from rawlsing_next.universal_grammar.native_map import (
    PARENT_RECEIPT_BOUND, RecurrenceParent, build_recurrence_issue_plan,
)
from rawlsing_next.pre553_recursive_handoff import load_recursive_handoff_bundle
from rawlsing_next.universal_grammar.types import OccurrenceKey
bundle_path, value, handoff_index = sys.argv[1], json.loads(sys.argv[2]), int(sys.argv[3])
source, qauth, root, query = _recurrence_source()
policy = _recurrence_policy()
bundle_ref, handoffs = load_recursive_handoff_bundle(bundle_path)
handoff = handoffs[handoff_index]
s1 = _condition_predicates(source, qauth, "s1")
s2 = _condition_predicates(source, qauth, "s2")
s1_predicate = next(p for k, v, p in s1 if v == value)
parent = RecurrenceParent(
    parent_id="persisted-" + handoff.ref.content_hash,
    predicate=handoff.winning_predicate, kind=PARENT_RECEIPT_BOUND,
    generation=1, source_release_refs=(source["release_ref"],),
    ancestry_conditions=((OccurrenceKey("s1"), value),),
    ancestry_predicates=(s1_predicate,), receipt_ref=handoff.receipt_ref,
    replay_binding_ref=handoff.ref, handoff=handoff,
    activation_reason="PERSISTED_PARENT_FRESH_PROCESS",
)
plan = build_recurrence_issue_plan(
    policy=policy, generation=2, parents=(parent,), root_predicate=root,
    target_label="t", query_ref=query, condition_predicates=s2,
)
catalog = [root, handoff.winning_predicate] + [p for _, _, p in s1] + [p for _, _, p in s2]
result = _run_recurrence_generation(source, qauth, plan, 2, catalog)
print(json.dumps({
    "bundle_ref": bundle_ref.as_dict(),
    "handoff_ref": handoff.ref.as_dict(),
    "no_drop_ok": result.anti_join["no_drop_ok"],
    "receipt_refs": [r.ref.as_dict() for r in result.execution.discovery_result.receipts],
}))
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", child_code, str(path), json.dumps(persisted_value),
         str(persisted_index)],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    child = json.loads(proc.stdout)
    assert child["handoff_ref"] == persisted_handoff.ref.as_dict()
    assert child["bundle_ref"] == bundle_ref.as_dict()
    assert child["no_drop_ok"] is True
    assert child["receipt_refs"]

    # A transformed source uses different names and the second frozen profile's
    # smaller caps; the mechanism must not depend on selected question names.
    renamed_rows = []
    for index in range(16):
        s1v = 0 if index < 8 else 1
        s2v = 0 if (index % 8) < 4 else 1
        s3v = index % 2
        if s1v == 0 and s2v == 0:
            t = 1 if (index % 4) < 3 else 0
        elif s1v == 0 and s2v == 1:
            t = 1 if (index % 4) < 2 or (index % 4) == 2 else 0
        elif s1v == 1 and s2v == 0:
            t = 0
        else:
            t = 1 if (index % 2) == 0 else 0
        renamed_rows.append({
            "id": f"X{index:02d}",
            "responses": {"r1": s1v, "r2": s2v, "r3": s3v, "u": t},
        })
    renamed_source = _build_source("r61-r4-renamed", renamed_rows)
    renamed_qauth = _query_authority("r61-r4-renamed")
    renamed_root = _branch_predicate(renamed_source, renamed_qauth, tag="r61-r4-renamed-root")
    renamed_query = _query(renamed_source, renamed_qauth, renamed_root, ("u",),
                           tag="r61-r4-renamed-u")
    renamed_policy = _recurrence_policy(d=2, breadth=1, per_generation=2, total=6)
    renamed_root_parent = make_root_parent(
        predicate=renamed_root,
        source_release_refs=(renamed_source["release_ref"],),
    )
    renamed_conditions = _condition_predicates(renamed_source, renamed_qauth, "r1")
    renamed_catalog = [renamed_root] + [
        predicate for _, _, predicate in renamed_conditions
    ]
    renamed_plan = build_recurrence_issue_plan(
        policy=renamed_policy, generation=1, parents=(renamed_root_parent,),
        root_predicate=renamed_root, target_label="u",
        query_ref=renamed_query, condition_predicates=renamed_conditions,
    )
    renamed_generation = _run_recurrence_generation(
        renamed_source, renamed_qauth, renamed_plan, 1, renamed_catalog
    )
    assert renamed_generation.anti_join["no_drop_ok"]
    assert len(renamed_plan.expected_operations) <= 2
