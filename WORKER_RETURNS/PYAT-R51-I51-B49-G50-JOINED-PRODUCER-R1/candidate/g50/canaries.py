"""M48 28-canary disposition matrix for the G50 composer + native I05 bridge."""
from __future__ import annotations

import json
from pathlib import Path

from .enumerate import enumerate_frontier, role_disposition
from .fixture import bundle, incomplete_bundle, policy
from .native_i05 import NativeRun, run_empty_probe
from .types import ScientificFrontier, SourceDecisionBundle

ROOT = Path(__file__).resolve().parents[3]
MATRIX_PATH = ROOT / "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/ESTATE_35X_REQUIREMENTS_MATRIX.json"


def _find(frontier: ScientificFrontier, *, claim_class=None, targets=None,
          conditions=None, disposition=None, state_variant=None):
    for op in frontier.operations:
        if claim_class is not None and op.claim_class != claim_class:
            continue
        if targets is not None and op.targets != tuple(targets):
            continue
        if conditions is not None and op.conditions != tuple(conditions):
            continue
        if disposition is not None and op.disposition != disposition:
            continue
        if state_variant is not None and op.state_variant != state_variant:
            continue
        return op
    return None


def _entry(cid, klass, disposition, evidence, detail):
    return {"id": cid, "class": klass, "disposition": disposition,
            "evidence": evidence, "detail": detail}


def canary_matrix(
    frontier: ScientificFrontier,
    native_run: NativeRun,
    *,
    budget_frontier: ScientificFrontier,
    empty_probe: dict | None = None,
) -> list[dict]:
    empty_probe = empty_probe or run_empty_probe()
    b = bundle()
    p = policy()
    ops = []

    id_op = _find(frontier, targets=("ID",))
    ops.append(_entry("C01", "Administrative ID as attitude", "TYPED_REFUSAL",
                      id_op.op_id if id_op else "role_disposition",
                      "administrative ID is excluded from target/condition roles; explicit prohibition retained"))
    h_op = _find(frontier, claim_class="JOINT", targets=("Y", "H"))
    ops.append(_entry("C02", "Household selected adult", "TYPED_REFUSAL",
                      h_op.op_id if h_op else "role_disposition",
                      "adult/household joint stays UNRESOLVED_UNIT_LINK without a sanctioned transform"))
    rt_op = _find(frontier, claim_class="CONDITIONAL", targets=("Y",), conditions=(("RT", 1),))
    ops.append(_entry("C03", "Unknown routing", "TYPED_REFUSAL",
                      rt_op.op_id if rt_op else "role_disposition",
                      "UNKNOWN route is not promoted to true/false; no eligible operation"))
    split_op = _find(frontier, claim_class="JOINT", targets=("X1", "X2"))
    ops.append(_entry("C04", "Split ballot", "TYPED_REFUSAL",
                      split_op.op_id if split_op else "role_disposition",
                      "disjoint forms proved INAPPLICABLE for a shared-administration joint"))
    state_op = _find(frontier, claim_class="STATE_ROBUSTNESS",
                     state_variant="SPECIAL_STATES_PRESERVED")
    ops.append(_entry("C05", "DK and refusal", "SPEC_ONLY_NATIVE_UNSUPPORTED",
                      state_op.op_id if state_op else "state_map",
                      "special states preserved in state map; no native recode is performed"))
    set_op = _find(frontier, claim_class="JOINT", targets=("Y", "SET"))
    ops.append(_entry("C06", "MR respondent inflation", "TYPED_REFUSAL",
                      set_op.op_id if set_op else "role_disposition",
                      "MULTI_SELECT_SET topology is not silently scalarized; UNSUPPORTED_RUNTIME"))
    rank_op = _find(frontier, claim_class="JOINT", targets=("Y", "RANK"))
    rep_op = _find(frontier, claim_class="JOINT", targets=("Y", "REP"))
    ops.append(_entry("C07", "Rank and repeated occasions", "TYPED_REFUSAL",
                      (rank_op.op_id if rank_op else "") + "," + (rep_op.op_id if rep_op else ""),
                      "RANKED/REPEATED topologies remain exact unsupported obligations"))
    pop_op = _find(frontier, claim_class="DIST", targets=("Y",), disposition="UNRESOLVED_SCIENCE")
    pop_op = pop_op if pop_op and pop_op.measure == "POPULATION" else next(
        (op for op in frontier.operations if op.measure == "POPULATION"), None)
    ops.append(_entry("C08", "Missing population weights", "TYPED_REFUSAL",
                      pop_op.op_id if pop_op else "measure_plan",
                      "population variant held; no weight/design invented, sample variant remains separate"))
    ops.append(_entry("C09", "Kish as full design", "TYPED_REFUSAL",
                      "measure_plan:M-POP", "design variance/replicates absent; population inference held"))
    ops.append(_entry("C10", "Sample zero versus impossible", "NATIVE_EXECUTED",
                      f"native observed_zero_cells={native_run.observed_zero_cell_count}; "
                      f"empty_probe_zero_denominator={empty_probe['zero_denominator_fact_count']}",
                      "observed-zero cells stay zero with positive denominator; impossible joint has zero denominator"))
    ops.append(_entry("C11", "Unary-screen XOR", "NATIVE_EXECUTED",
                      "GRID-AB,XOR-AB",
                      f"{native_run.candidate_rule_counts.get('GRID-AB', 0)} grid + "
                      f"{native_run.candidate_rule_counts.get('XOR-AB', 0)} exactly-one candidates executed"))
    ops.append(_entry("C12", "Unlisted minority branch", "NATIVE_EXECUTED",
                      "COND-M1", "M=1 minority condition executed independently of outcome-based whitelists"))
    ops.append(_entry("C13", "Semantic relation absence", "NATIVE_EXECUTED",
                      "JOINT-YM + CO_TRAVEL", "descriptive co-travel eligible; STRUCTURAL stays separately DEFERRED"))
    ops.append(_entry("C14", "Same marginals different joint", "SPEC_ONLY_NATIVE_UNSUPPORTED",
                      "M48 toy oracle",
                      "native joint validator executed for Y-M dependence; distinct-joint contrast remains model-only"))
    rev_op = _find(frontier, claim_class="CONDITIONAL", targets=("A",), conditions=(("Y", 1),))
    ops.append(_entry("C15", "Reverse denominator", "TYPED_REFUSAL",
                      rev_op.op_id if rev_op else "role_disposition",
                      "reverse role requires its own risk/role issue; explicit prohibition"))
    ops.append(_entry("C16", "False cross-survey person", "POLICY_HOLD",
                      "CROSS_SOURCE", "cross-source class is method-gated; no respondent join"))
    ops.append(_entry("C17", "F6 missing target mass", "POLICY_HOLD",
                      "CROSS_SOURCE/STRUCTURAL", "transport/F6 method remains separately deferred"))
    ops.append(_entry("C18", "Country/time comparability", "POLICY_HOLD",
                      "TEMPORAL", "comparability method not issued; no observed comparable pair"))
    held = list(b.held)
    ops.append(_entry("C19", "Future publication leakage", "TYPED_REFUSAL",
                      "currentness:" + ",".join(held),
                      "no current selection; current host/purpose held"))
    ops.append(_entry("C20", "Unknown crosswave covariance", "POLICY_HOLD",
                      "TEMPORAL", "covariance not silently zero; temporal interval method deferred"))
    exploratory = all(op.validation_status == "EXPLORATORY_NOT_VALIDATED" for op in frontier.eligible())
    ops.append(_entry("C21", "Exact discovery as validation", "TYPED_REFUSAL",
                      f"validation_status_exploratory={exploratory}",
                      "I05 exact support never self-issues statistical validation"))
    ops.append(_entry("C22", "Budget stop as absence", "NATIVE_EXECUTED",
                      f"budget_state={budget_frontier.budget_state}; "
                      f"pending={len(budget_frontier.pending_operation_ids)}",
                      "budget exhaustion is PARTIAL with explicit pending identities; E_pre root unchanged"))
    ops.append(_entry("C23", "Historical LiTS rights", "POLICY_HOLD",
                      "current_permission=NOT_ASSERTED",
                      "historical positive does not authorize a current source read; no source factory call"))
    ops.append(_entry("C24", "All35 unissued counts", "POLICY_HOLD",
                      "original35_census", "35 identities preserved; original U/E_pre NULL with cause"))
    ops.append(_entry("C25", "Actor and route inference", "TYPED_REFUSAL",
                      "no actor/route_probability fields",
                      "no actor belief, route probability or person claim is emitted"))
    leakage = role_disposition(
        b, p, targets=("Y",), conditions=(("Y", 1),), class_name="CONDITIONAL"
    )
    ops.append(_entry("C26", "Target leakage alias", "TYPED_REFUSAL",
                      "role_disposition:" + ",".join(leakage[1]),
                      "target as conditioner is denied; deterministic alias is not predictor evidence"))
    inc = enumerate_frontier(incomplete_bundle(), p)
    ops.append(_entry("C27", "Source extra and manual ceiling", "TYPED_REFUSAL",
                      f"incomplete_e_pre={inc.e_pre_count}",
                      "incomplete declared inventory refuses a complete U root; no silent polarity/omission"))
    ops.append(_entry("C28", "Empty jointly applicable risk", "NATIVE_EXECUTED",
                      f"empty_probe={empty_probe['receipt_states'][0]}",
                      "eligible operation persists with VALID_EMPTY and a zero denominator; no fake probability"))
    assert [row["id"] for row in ops] == [f"C{i:02d}" for i in range(1, 29)]
    return ops


def original35_census() -> list[dict]:
    data = json.loads(MATRIX_PATH.read_text())
    sources = data["sources"]
    rows = [{
        "source_id": s["id"],
        "original_U_count": None,
        "original_E_pre_count": None,
        "cause": "SOURCE_SPECIFIC_COMPETENT_U_E_PRE_UNISSUED",
        "E_exec_count": 0,
        "original_measured_occupied": False,
        "grade": "SOURCEFREE_PROPOSAL_NOT_ORIGINAL",
        "grammar_classes": "POLICY_DECLARED_ONLY",
    } for s in sources]
    if len(rows) != 35 or len({r["source_id"] for r in rows}) != 35:
        raise ValueError("EXACT35_REQUIRED")
    return rows


def decision_demands() -> list[dict]:
    return [
        {"decision": "D1", "id": "SOURCE_HOST_PURPOSE_LICENCE",
         "owner_role": "source custodian + deployment/use owner",
         "current_state": "NOT_ISSUED", "affected": "all original execution",
         "software_done": "grant interface and early guard", "finite": True},
        {"decision": "D2", "id": "COMPLETE_ADMINISTERED_OCCURRENCES",
         "owner_role": "source-semantic specialist",
         "current_state": "UNRESOLVED", "affected": "U_item/U_app completeness",
         "software_done": "inventory reconciliation and typed gaps", "finite": True},
        {"decision": "D3", "id": "ROUTE_UNIT_STATE",
         "owner_role": "source specialist + survey-method owner",
         "current_state": "UNRESOLVED", "affected": "UNKNOWN routes, household/adult link",
         "software_done": "three-valued route and unit checker", "finite": True},
        {"decision": "D4", "id": "POPULATION_MEASURE",
         "owner_role": "survey-method statistician",
         "current_state": "NOT_ISSUED", "affected": "population variants",
         "software_done": "parameterized sample/population split; no invented weights", "finite": True},
        {"decision": "D5", "id": "GRAMMAR_AND_VALIDATION_POLICY",
         "owner_role": "competent empirical-method owner",
         "current_state": "PROPOSED_TEST_ONLY", "affected": "J/K/D, validation semantics",
         "software_done": "finite enumerator, independent oracle, native bridge", "finite": True},
        {"decision": "D6", "id": "STRUCTURAL_USE",
         "owner_role": "Field Forge semantic/use owner",
         "current_state": "HELD", "affected": "STRUCTURAL class",
         "software_done": "capability declaration only", "finite": True},
        {"decision": "D7", "id": "F6_TRANSPORT",
         "owner_role": "comparative-method and target-use owner",
         "current_state": "HELD", "affected": "CROSS_SOURCE/F6",
         "software_done": "typed hold only", "finite": True},
        {"decision": "D8", "id": "F7_TEMPORAL",
         "owner_role": "temporal-method/source/use owner",
         "current_state": "HELD", "affected": "TEMPORAL/F7",
         "software_done": "typed hold only", "finite": True},
        {"decision": "D9", "id": "REVERSE_POSSIBILITY_USE",
         "owner_role": "empirical possibility/model and consumer-use owner",
         "current_state": "HELD", "affected": "reverse roles/POSSIBILITY",
         "software_done": "role-asymmetry refusal", "finite": True},
    ]


__all__ = ["canary_matrix", "original35_census", "decision_demands"]
