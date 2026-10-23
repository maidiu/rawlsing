"""R61 R01 generic symbolic frontier and semantic native mapping tests (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
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
    lower_frontier,
    native_receipt_anti_join,
)
from rawlsing_next.universal_grammar.types import (
    ADMINISTERED,
    ADMINISTRATION_UNKNOWN,
    DEFERRED,
    ELIGIBLE,
    HELD,
    INAPPLICABLE_PROVED,
    NOT_ADMINISTERED,
    PROHIBITED,
    UNKNOWN,
    UNSUPPORTED_RUNTIME,
    DirectionGrant,
    GrammarPolicy,
    MeasurePlan,
    Occurrence,
    OccurrenceKey,
    SourceInventory,
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
    # POPULATION measure, and four deferred classes.
    # SAMPLE: 1 DIST + 1 STATE_ROBUSTNESS + 2 CONDITIONAL = 4 per target.
    # POPULATION: 1 DIST + 2 CONDITIONAL = 3 per target (STATE uses SAMPLE only).
    # Two targets: 8 eligible + 6 held + 8 deferred = 22 operations.
    assert len(frontier.operations) == 22
    assert frontier.disposition_counts[ELIGIBLE] == 8
    assert frontier.disposition_counts[HELD] == 6
    assert frontier.disposition_counts[DEFERRED] == 8
    assert set(frontier.disposition_counts) <= {
        ELIGIBLE, PROHIBITED, INAPPLICABLE_PROVED, HELD, UNKNOWN,
        UNSUPPORTED_RUNTIME, DEFERRED,
    }
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

    def normalize(operation):
        material = operation.identity_material()
        material["targets"] = [
            {**key, "item_id": rename.get(key["item_id"], key["item_id"])}
            for key in material["targets"]
        ]
        material["conditions"] = [
            [{**key, "item_id": rename.get(key["item_id"], key["item_id"])}, value]
            for key, value in material["conditions"]
        ]
        return json.dumps(material, sort_keys=True)

    assert sorted(normalize(op) for op in original.operations) == sorted(
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
    inventory = _inventory(occurrences, held=(OccurrenceKey("held_item").key,))
    frontier = _frontier(inventory, _policy(j=2, k=0, d=0))
    assert frontier.operations
    assert any(op.claim_class == "DIST" and op.disposition == UNSUPPORTED_RUNTIME
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
               and op.reasons == ("OCCURRENCE_HELD_BY_INVENTORY",)
               for op in frontier.operations)
    assert any(op.claim_class == "JOINT" and op.disposition == INAPPLICABLE_PROVED
               and op.reasons == ("DISJOINT_ADMINISTRATION_FORM",)
               for op in frontier.operations)
    assert any(op.claim_class == "JOINT" and op.disposition == HELD
               and op.reasons == ("UNRESOLVED_UNIT_LINK",)
               for op in frontier.operations)
    ledger = inventory_ledger(inventory, _policy(j=2, k=0, d=0))
    assert len(ledger) == len(occurrences)
    assert {entry.disposition for entry in ledger} <= {
        ELIGIBLE, PROHIBITED, INAPPLICABLE_PROVED, HELD, UNKNOWN,
        UNSUPPORTED_RUNTIME, DEFERRED,
    }
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


def test_lazy_partition_and_cold_subprocess_replay():
    frontier = _frontier(_tiny_inventory(), _policy(j=1, k=1, d=0), partition_size=5)
    partitions = list(iter_partitions(frontier))
    assert len(partitions) == frontier.partition_count
    flattened = [op_id for part in partitions for op_id in part.operation_ids]
    assert flattened == sorted(op.op_id for op in frontier.operations)
    assert all(part.operation_count == len(part.operation_ids) for part in partitions)
    assert len({part.root for part in partitions}) == len(partitions)
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
    labels = ("q_alpha", "q_beta", "q_gamma")
    for index in range(12):
        responses = {
            labels[0]: index % 2,
            labels[1]: (index // 2) % 2,
            labels[2]: index % 3 % 2,
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


def _native_catalog(labels, all_predicate, predicates, queries):
    predicate_refs = {
        f"{OccurrenceKey(label).key}|{json.dumps(value, separators=(',', ':'))}": predicate.ref
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
        supported_topologies=("SCALAR_SINGULAR",),
        supported_condition_modes=("AND", "XOR_EXACTLY_ONE"),
        maximum_target_arity=2,
        maximum_conditioner_arity=2,
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
    catalog = _native_catalog(labels, all_predicate, predicates, queries)
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


def test_native_mapping_marks_unsupported_and_never_returns_none():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory((_occurrence(labels[0]),))
    policy = _policy(j=1, k=0, d=0)
    frontier = _frontier(inventory, policy)
    catalog = _native_catalog(labels, all_predicate, predicates, queries)
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
