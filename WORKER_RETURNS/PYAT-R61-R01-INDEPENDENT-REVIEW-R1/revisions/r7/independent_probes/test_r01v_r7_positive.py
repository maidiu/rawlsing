"""R61-R01V R6 independent changed-data D3 positive through the campaign owner."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys

from rawlsing_next.tests.test_pre553_discovery_exact import (
    _d_auth, _discovery_authority, _registry as _i05_registry,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source, _branch_predicate, _predicate, _query, _query_authority,
    _response_leaf,
)
from rawlsing_next.universal_grammar.native_map import (
    COMPARATOR_PARENT, COMPARATOR_ROOT, PARENT_EXPLORATORY,
    RecurrencePolicy, RetainedRecurrenceCampaign, create_campaign,
)
from rawlsing_next.universal_grammar.types import OccurrenceKey

REPO_ROOT = Path(__file__).resolve().parents[5]


def _source():
    rows = []

    def add(group, t, q3):
        rows.append({
            "id": f"N{len(rows):02d}",
            "responses": {"q1": int(group[0]), "q2": int(group[1]),
                          "q3": q3, "out": t},
        })

    for t, q3 in ((1, 0), (1, 1), (1, 0), (0, 1)):
        add("00", t, q3)
    for t, q3 in ((1, 0), (0, 1), (0, 0), (0, 1)):
        add("01", t, q3)
    for t, q3 in ((1, 0), (1, 1), (1, 0), (0, 1)):
        add("10", t, q3)
    for t, q3 in ((1, 0), (0, 1), (0, 0), (0, 1)):
        add("11", t, q3)
    source = _build_source("r61-r6-independent", rows)
    source["_rows"] = rows
    qauth = _query_authority("r61-r6-independent")
    root = _branch_predicate(source, qauth, tag="r61-r6-independent-root")
    query = _query(source, qauth, root, ("out",), tag="r61-r6-independent-out")
    return source, qauth, root, query, rows


def _conditions(source, qauth, variable):
    return tuple(
        (OccurrenceKey(variable), value,
         _predicate(source, qauth, _response_leaf(source, qauth, variable, value),
                    tag=f"r61-r6-independent-{variable}-{value}"))
        for value in (0, 1)
    )


def _policy():
    return RecurrencePolicy(
        policy_id="R61-R6-INDEPENDENT-POLICY", policy_version="r61.r4.1",
        grade="TEST_ONLY", owner_refs=("R61-R6-INDEPENDENT",),
        counting_convention="ANCESTOR_CONDITIONS_COUNT_TOWARD_K",
        bounds={"J": 2, "K": 3, "D": 3}, breadth_cap=2, followup_cap=2,
        protected_exploration_slots=1, per_generation_issued_cap=8,
        total_issued_cap=24, comparators=(COMPARATOR_ROOT, COMPARATOR_PARENT),
    )


def _fixture():
    source, qauth, root, query, rows = _source()
    policy = _policy()
    q1 = _conditions(source, qauth, "q1")
    q2 = _conditions(source, qauth, "q2")
    q3 = _conditions(source, qauth, "q3")
    dauths = {tag: _d_auth(tag) for tag in ("R61-R4-G1", "R61-R4-G2", "R61-R4-G3")}
    registry = _i05_registry(source, qauth, *dauths.values())

    def authority_factory(grammar):
        tag = grammar["discovery_operation"].removeprefix("I03-OP-")
        return _discovery_authority(source, grammar, dauths[tag], tag=f"r61-r6-{tag}")

    campaign = create_campaign(
        policy=policy, root_predicate=root,
        source_release_refs=(source["release_ref"],), target_label="out",
        query_object=query, condition_catalog=q1 + q2 + q3,
        repository=source["repo"], authority_registry=registry,
        authority_factory=authority_factory, owner_refs=("R61-R6-INDEPENDENT",),
    )
    return source, qauth, root, query, rows, policy, q1, q2, q3, campaign


def _records(campaign):
    inspected = campaign.inspect()
    lineage = {record["lineage_ref"]: record for record in inspected["lineage"]}
    return inspected, lineage


def _expected_shape(campaign, issuance_ref, parent_refs, condition_refs, root_hash):
    inspected, lineage = _records(campaign)
    shape = []
    for parent_ref in parent_refs:
        parent = lineage[parent_ref]
        for key, value in condition_refs:
            shape.append((
                parent["parent_id"], COMPARATOR_PARENT,
                (key.item_id,), (value,), parent["predicate"]["content_hash"],
            ))
            root_keys = tuple(
                cond["key"]["item_id"] for cond in parent["ancestry_conditions"]
            ) + (key.item_id,)
            root_values = tuple(
                cond["value"] for cond in parent["ancestry_conditions"]
            ) + (value,)
            shape.append((
                parent["parent_id"], COMPARATOR_ROOT,
                root_keys, root_values, root_hash,
            ))
    return Counter(shape)


def _actual_shape(plan):
    return Counter(
        (
            operation["parent_id"], operation["comparator"],
            tuple(key["item_id"] for key in operation["condition_keys"]),
            tuple(operation["condition_values"]),
            operation["baseline_predicate_ref"]["content_hash"],
        )
        for operation in plan["expected_operations"]
    )


def _rate(rows, conditions):
    selected = [
        row for row in rows
        if all(row["responses"][key.item_id] == value for key, value in conditions)
    ]
    assert selected, conditions
    return sum(row["responses"]["out"] for row in selected), len(selected)


def _state(rows, parent, operation):
    child_conditions = tuple(
        (OccurrenceKey(cond["key"]["item_id"]), cond["value"])
        for cond in parent["ancestry_conditions"]
    ) + tuple(
        zip(
            (OccurrenceKey(key["item_id"]) for key in operation["condition_keys"][-1:]),
            operation["condition_values"][-1:],
        )
    )
    child_num, child_den = _rate(rows, child_conditions)
    base_conditions = (
        tuple((OccurrenceKey(cond["key"]["item_id"]), cond["value"])
              for cond in parent["ancestry_conditions"])
        if operation["comparator"] == COMPARATOR_PARENT else ()
    )
    base_num, base_den = _rate(rows, base_conditions)
    return (
        "DISCOVERED_RESULT_SUPPORTED"
        if child_num * base_den != base_num * child_den
        else "VALID_EMPTY"
    )


def _run_generation(campaign, parent_refs, conditions):
    issue_ref = campaign.issue(
        parent_lineage_refs=tuple(parent_refs),
        condition_refs=tuple((key, value) for key, value, _ in conditions),
    )
    execution_ref = campaign.execute(issue_ref)
    return issue_ref, execution_ref


def test_P1_changed_data_d3_owner_arithmetic_and_hidden_minority():
    source, qauth, root, query, rows, policy, q1, q2, q3, campaign = _fixture()
    root_ref = campaign.root_lineage_ref
    i1, e1 = _run_generation(campaign, (root_ref,), q1)
    a1 = campaign.activate(e1)
    inspect = campaign.inspect()
    plan1 = next(r["plan"] for r in inspect["issuances"] if r["issuance_ref"] == i1)
    assert _actual_shape(plan1) == _expected_shape(
        campaign, i1, (root_ref,), ((key, value) for key, value, _ in q1),
        root.ref.content_hash,
    )
    active1 = next(
        r["active_lineage_refs"] for r in inspect["activations"]
        if r["activation_ref"] == a1
    )
    assert active1
    assert any(
        inspect_lineage["kind"] == PARENT_EXPLORATORY
        for inspect_lineage in inspect["lineage"]
        if inspect_lineage["lineage_ref"] in active1
    )

    i2, e2 = _run_generation(campaign, active1, q2)
    a2 = campaign.activate(e2)
    inspect = campaign.inspect()
    plan2 = next(r["plan"] for r in inspect["issuances"] if r["issuance_ref"] == i2)
    assert _actual_shape(plan2) == _expected_shape(
        campaign, i2, active1, ((key, value) for key, value, _ in q2),
        root.ref.content_hash,
    )
    active2 = next(
        r["active_lineage_refs"] for r in inspect["activations"]
        if r["activation_ref"] == a2
    )
    assert active2

    i3, e3 = _run_generation(campaign, active2, q3)
    inspect = campaign.inspect()
    plan3 = next(r["plan"] for r in inspect["issuances"] if r["issuance_ref"] == i3)
    assert _actual_shape(plan3) == _expected_shape(
        campaign, i3, active2, ((key, value) for key, value, _ in q3),
        root.ref.content_hash,
    )

    lineage = {record["lineage_ref"]: record for record in inspect["lineage"]}
    for execution_ref, parent_refs in ((e2, active1), (e3, active2)):
        execution = campaign._executions[execution_ref]
        native = campaign._projection(execution)
        plan = native.plan
        for operation in plan.expected_operations:
            parent = next(
                lineage[ref] for ref in parent_refs
                if lineage[ref]["parent_id"] == operation.parent_id
            )
            expected = _state(rows, parent, operation.material())
            actual = native.receipt_by_rule[operation.rule_id].typed_state
            assert actual == expected, (operation.parent_id, operation.comparator, expected, actual)

    exploratory = next(
        lineage[record["lineage_ref"]] for record in inspect["lineage"]
        if record["lineage_ref"] in active1
        and record["kind"] == PARENT_EXPLORATORY
    )
    parent_rate = _rate(rows, tuple(
        (OccurrenceKey(cond["key"]["item_id"]), cond["value"])
        for cond in exploratory["ancestry_conditions"]
    ))
    root_rate = _rate(rows, ())
    assert parent_rate[0] * root_rate[1] == root_rate[0] * parent_rate[1]
    execution2 = campaign._projection(campaign._executions[e2])
    ops = [
        operation for operation in execution2.plan.expected_operations
        if operation.parent_id == exploratory["parent_id"]
        and operation.comparator == COMPARATOR_PARENT
    ]
    states = {
        operation.condition_values[-1]:
            execution2.receipt_by_rule[operation.rule_id].typed_state
        for operation in ops
    }
    assert states == {0: "DISCOVERED_RESULT_SUPPORTED", 1: "DISCOVERED_RESULT_SUPPORTED"}
    child_rates = {
        operation.condition_values[-1]: _rate(
            rows, tuple(
                (OccurrenceKey(cond["key"]["item_id"]), cond["value"])
                for cond in exploratory["ancestry_conditions"]
            ) + ((OccurrenceKey("q2"), operation.condition_values[-1]),)
        )
        for operation in ops
    }
    assert child_rates[0][0] * child_rates[1][1] > child_rates[1][0] * child_rates[0][1]
    assert child_rates[0][0] * parent_rate[1] > parent_rate[0] * child_rates[0][1]
    assert child_rates[1][0] * parent_rate[1] < parent_rate[0] * child_rates[1][1]

    for operation in ops:
        root_op = next(
            candidate for candidate in execution2.plan.expected_operations
            if candidate.parent_id == exploratory["parent_id"]
            and candidate.comparator == COMPARATOR_ROOT
            and candidate.condition_values[-1] == operation.condition_values[-1]
        )
        assert root_op.operation_id != operation.operation_id
        assert root_op.baseline_predicate_ref["content_hash"] != (
            operation.baseline_predicate_ref["content_hash"]
        )

    # Snapshot/restore after activation, then real N+1 from retained lineage.
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )
    restored_active = [
        record["lineage_ref"] for record in restored.inspect()["lineage"]
        if record["producer_generation"] == 2
    ]
    assert restored_active
    i4, e4 = _run_generation(restored, restored_active, q3)
    assert restored.execute(i4) == e4
    restored_inspect = restored.inspect()
    assert len(restored_inspect["executions"]) == 4
    assert all(
        record["cumulative_issued_count"] <= policy.total_issued_cap
        for record in restored_inspect["issuances"]
    )


def test_P2_fresh_process_owner_restore_runs_next_generation(tmp_path):
    import json
    import os

    from rawlsing_next.pre553_empirical_objects import canonicalize

    source, qauth, root, query, rows, policy, q1, q2, q3, campaign = _fixture()
    i1, e1 = _run_generation(campaign, (campaign.root_lineage_ref,), q1)
    a1 = campaign.activate(e1)
    active1 = next(
        record["active_lineage_refs"] for record in campaign.inspect()["activations"]
        if record["activation_ref"] == a1
    )
    i2, e2 = _run_generation(campaign, active1, q2)
    campaign.activate(e2)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    snapshot_path = tmp_path / "r61_r6_owner_snapshot.json"
    snapshot_path.write_text(json.dumps(canonicalize(snapshot), sort_keys=True))

    code = """
import json, sys
from test_r01v_r7_positive import _fixture
from rawlsing_next.universal_grammar.native_map import RetainedRecurrenceCampaign
snapshot_path, pin = sys.argv[1], sys.argv[2]
snapshot = json.loads(open(snapshot_path, encoding="utf-8").read())
source, qauth, root, query, rows, policy, q1, q2, q3, campaign = _fixture()
restored = RetainedRecurrenceCampaign.restore(
    snapshot=snapshot, expected_checkpoint_ref=pin,
    repository=source["repo"], authority_registry=campaign._registry,
    authority_factory=campaign._authority_factory,
    condition_catalog=campaign._condition_catalog, query_object=query,
)
active = [
    record["lineage_ref"] for record in restored.inspect()["lineage"]
    if record["producer_generation"] == 2
]
issue = restored.issue(
    parent_lineage_refs=tuple(active),
    condition_refs=tuple((key, value) for key, value, _ in q3),
)
execution = restored.execute(issue)
record = next(
    record for record in restored.inspect()["issuances"]
    if record["issuance_ref"] == issue
)
print(json.dumps({
    "execution": execution,
    "plan_ref": record["plan_ref"],
    "expected_operations": len(record["plan"]["expected_operations"]),
    "cumulative": record["cumulative_issued_count"],
}, sort_keys=True))
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = (
        str(REPO_ROOT) + os.pathsep + str(Path(__file__).resolve().parent)
        + os.pathsep + env.get("PYTHONPATH", "")
    )
    proc = subprocess.run(
        [sys.executable, "-c", code, str(snapshot_path), pin],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-3000:]
    child = json.loads(proc.stdout)
    assert child["execution"]
    assert child["expected_operations"] > 0
    assert child["cumulative"] <= policy.total_issued_cap
