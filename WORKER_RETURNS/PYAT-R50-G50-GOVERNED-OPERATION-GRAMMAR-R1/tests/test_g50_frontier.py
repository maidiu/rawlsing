"""R50 G50 native courts: symbolic frontier, independent oracle, real I05, canaries."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

RETURN_DIR = Path(__file__).resolve().parents[1]
if str(RETURN_DIR) not in sys.path:
    sys.path.insert(0, str(RETURN_DIR))
import bootstrap  # noqa: F401,E402

from g50.canaries import canary_matrix, decision_demands, original35_census  # noqa: E402
from g50.enumerate import enumerate_frontier, role_disposition  # noqa: E402
from g50.fixture import bundle, incomplete_bundle, policy, synthetic_rows  # noqa: E402
from g50.native_i05 import (  # noqa: E402
    native_no_drop, run_empty_probe, run_native,
)
from g50.native_map import native_rule_key  # noqa: E402
from g50.oracle import expected_eligible_ids, expected_epre_root  # noqa: E402
from g50.plan import native_construction_plan  # noqa: E402
from g50.types import ScientificGrammarPolicy  # noqa: E402
from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryError  # noqa: E402


def _frontier(budget=None):
    return enumerate_frontier(bundle(), policy(), budget=budget)


# ---------------------------------------------------------------------------
# symbolic frontier + independent oracle
# ---------------------------------------------------------------------------


def test_frontier_matches_independent_oracle_and_expected_root():
    frontier = _frontier()
    expected = expected_eligible_ids(bundle(), policy())
    actual = sorted(op.op_id for op in frontier.eligible())
    assert actual == expected
    assert frontier.e_pre_root == expected_epre_root(bundle(), policy())
    assert frontier.e_pre_count == len(expected) == 432
    assert frontier.policy_grade == "PROPOSED_TEST_ONLY"
    assert frontier.original_science_grade == "SOURCEFREE_PROPOSAL_NOT_ORIGINAL"
    assert set(frontier.class_counts) >= {
        "DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL", "FORK", "INTERACTION", "STATE_ROBUSTNESS"
    }
    native = [op for op in frontier.eligible() if op.native_support.startswith("I05_EXACT:")]
    assert len(native) == 15


def test_source_value_mutation_does_not_change_epre_root():
    frontier = _frontier()
    changed = []
    for row in synthetic_rows():
        row = deepcopy(row)
        row["responses"]["Y"] = 1 - row["responses"]["Y"]
        changed.append(row)
    run_a = run_native()
    run_b = run_native(rows=changed)
    assert _frontier().e_pre_root == frontier.e_pre_root
    assert run_a.result_identity_hash != run_b.result_identity_hash
    assert run_a.fact_summaries != run_b.fact_summaries


def test_nonsemantic_impossible_roles_and_authority_denied():
    frontier = _frontier()

    def op_for(claim_class, targets, conditions=()):
        return next(
            op for op in frontier.operations
            if op.claim_class == claim_class and op.targets == tuple(targets)
            and op.conditions == tuple(conditions)
        )

    assert op_for("DIST", ("ID",)).reasons == ("ADMINISTRATIVE_TARGET_DENIED",)
    assert op_for("JOINT", ("Y", "H")).reasons == ("UNRESOLVED_UNIT_LINK",)
    assert op_for("CONDITIONAL", ("Y",), (("RT", 1),)).reasons == ("UNKNOWN_ROUTING_NONPROMOTION",)
    assert op_for("JOINT", ("X1", "X2")).reasons == ("DISJOINT_ADMINISTRATION",)
    assert op_for("JOINT", ("Y", "SET")).reasons == ("UNSANCTIONED_TOPOLOGY_OBLIGATION",)
    assert op_for("CONDITIONAL", ("A",), (("Y", 1),)).reasons == ("REVERSE_ROLE_RISK_NOT_AUTHORIZED",)
    forged = role_disposition(
        bundle(), policy(), targets=("FORGED",), conditions=(), class_name="DIST"
    )
    assert forged[0] == "PROHIBITED"
    assert forged[1] == ["TARGET_ROLE_DENIED"]


def test_invented_authority_and_missing_catalog_are_refused():
    from g50.native_i05 import build_native_grammar
    from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
    from rawlsing_next.tests.test_pre553_discovery_exact import _d_auth, _discovery_authority
    from rawlsing_next.tests.test_pre553_empirical_query import _registry

    grammar, materialized, _leaf, _all = build_native_grammar()
    source = materialized["source"]
    qauth = materialized["qauth"]
    dauth = _d_auth("g50-discovery")
    authority = _discovery_authority(source, grammar, dauth, tag="g50-native")
    with pytest.raises(Exception):
        execute_exact_bounded_discovery(
            repository=source["repo"], discovery_authority=authority,
            authority_registry=_registry(source, qauth, dauth),
            release_refs=(source["release_ref"],),
            predicate_catalog=(), query_template_catalog=(),
        )


# ---------------------------------------------------------------------------
# native I05 execution
# ---------------------------------------------------------------------------


def test_native_i05_executes_generated_grammar_and_no_drop():
    frontier = _frontier()
    run = run_native()
    check = native_no_drop(frontier, run)
    assert check["no_drop_ok"], check
    assert check["candidate_count_ok"]
    assert run.candidate_count == 15
    assert run.candidate_rule_counts == {
        "COND-A0": 1, "COND-A1": 1, "COND-B0": 1, "COND-B1": 1,
        "COND-M0": 1, "COND-M1": 1, "DIST-Y": 2, "FORK-A1-M1": 1,
        "GRID-AB": 4, "JOINT-YM": 1, "XOR-AB": 1,
    }
    assert run.predicate_count > 0 and run.query_count > 0 and run.fact_count > 0
    assert "DISCOVERED_RESULT_SUPPORTED" in run.receipt_states


def test_native_xor_minority_and_observed_zero():
    run = run_native()
    by_rule = {}
    for summary in run.fact_summaries:
        by_rule.setdefault(summary["rule_id"], []).append(summary)
    # Minority condition M=1 is actually executed over the 10-person cohort.
    m1 = by_rule["COND-M1"][0]
    assert any(fact["denominator"] == 10 for fact in m1["facts"])
    # Zero-unary XOR: the unconditional/unary cells are balanced while the
    # A=1,B=0 joint cell is decisive for Y=1.
    grid = [s for s in by_rule["GRID-AB"]]
    decisive = None
    for summary in grid:
        for fact in summary["facts"]:
            cells = {str(c["cell"]): c["numerator"] for c in fact["cells"]}
            if "1" in cells:
                decisive = (cells, fact["denominator"])
    assert decisive is not None
    assert run.observed_zero_cell_count > 0
    empty = run_empty_probe()
    assert empty["receipt_states"] == ("VALID_EMPTY",)
    assert empty["zero_denominator_fact_count"] >= 1


def test_grammar_mutation_red_and_restore():
    frontier = _frontier()
    good = run_native()
    assert native_no_drop(frontier, good)["no_drop_ok"] is True
    mutated = run_native(drop_rule="COND-M1")
    bad = native_no_drop(frontier, mutated)
    assert bad["no_drop_ok"] is False
    assert "COND-M1" in bad["missing_rules"]
    restored = run_native()
    assert native_no_drop(frontier, restored)["no_drop_ok"] is True
    assert restored.result_identity_hash == good.result_identity_hash


def test_budget_partial_and_incomplete_inventory():
    full = _frontier()
    partial = _frontier(budget=10)
    assert partial.budget_state == "PARTIAL"
    assert len(partial.pending_operation_ids) == len(partial.eligible()) - 10
    assert partial.e_pre_root == full.e_pre_root
    assert partial.e_pre_count == full.e_pre_count
    incomplete = enumerate_frontier(incomplete_bundle(), policy())
    assert incomplete.e_pre_count is None
    assert incomplete.e_pre_root is None
    assert incomplete.u_item_root is None
    assert "INCOMPLETE_DECLARED_ADMINISTERED_INVENTORY" in incomplete.e_pre_cause
    assert incomplete.operations


# ---------------------------------------------------------------------------
# canaries, census, orthogonal grades, replay, B49 interface
# ---------------------------------------------------------------------------


def test_canary_matrix_all_28():
    frontier = _frontier()
    budget_frontier = _frontier(budget=10)
    rows = canary_matrix(frontier, run_native(), budget_frontier=budget_frontier,
                         empty_probe=run_empty_probe())
    assert len(rows) == 28
    assert [r["id"] for r in rows] == [f"C{i:02d}" for i in range(1, 29)]
    dispositions = {r["id"]: r["disposition"] for r in rows}
    for cid in ("C01", "C02", "C03", "C04", "C06", "C07", "C15", "C19", "C21", "C25", "C26", "C27"):
        assert dispositions[cid] == "TYPED_REFUSAL"
    for cid in ("C10", "C11", "C12", "C13", "C22", "C28"):
        assert dispositions[cid] == "NATIVE_EXECUTED"
    for cid in ("C16", "C17", "C18", "C20", "C23", "C24"):
        assert dispositions[cid] == "POLICY_HOLD"
    assert dispositions["C05"] == "SPEC_ONLY_NATIVE_UNSUPPORTED"
    assert all("PASS" not in r["disposition"] for r in rows)


def test_original35_census_and_original_zero_unchanged():
    census = original35_census()
    assert len(census) == 35 and len({r["source_id"] for r in census}) == 35
    assert all(r["original_U_count"] is None for r in census)
    assert all(r["original_E_pre_count"] is None for r in census)
    assert all(r["E_exec_count"] == 0 for r in census)
    assert all(r["original_measured_occupied"] is False for r in census)
    assert len(decision_demands()) == 9


def test_orthogonal_columns_and_no_actor_route():
    frontier = _frontier()
    for op in frontier.eligible():
        assert op.native_support in {"I05_EXACT:" + key for key in (
            "DIST-Y", "COND-A0", "COND-A1", "COND-B0", "COND-B1",
            "COND-M0", "COND-M1", "GRID-AB", "XOR-AB", "JOINT-YM", "FORK-A1-M1",
        )} or op.native_support == "POLICY_ONLY"
        assert op.current_permission == "NOT_ASSERTED"
        assert op.validation_status == "EXPLORATORY_NOT_VALIDATED"
        assert op.release_status == "NOT_RELEASED"
    material = json.dumps(frontier.material())
    assert "route_probability" not in material
    assert "actor_belief" not in material


def test_cold_replay_identical_in_process_and_subprocess():
    first = run_native()
    second = run_native()
    assert first.content_hash == second.content_hash
    env = dict(os.environ)
    env["PYTHONPATH"] = str(RETURN_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c",
         "import bootstrap; from g50.native_i05 import run_native; "
         "print(run_native().content_hash)"],
        cwd=str(RETURN_DIR), env=env, capture_output=True, text=True, timeout=900,
    )
    assert proc.returncode == 0, proc.stderr[-1500:]
    assert proc.stdout.strip() == first.content_hash


def test_b49_interface_plan_and_version_refusal():
    frontier = _frontier()
    plan = native_construction_plan(frontier, run_native())
    assert plan["schema"] == "NativeConstructionPlan@candidate1"
    assert plan["no_new_batch_writer"] is True
    assert plan["no_new_c11_engine"] is True
    assert plan["no_original_source_grant"] is True
    assert plan["candidate_count"] == 15
    bad = ScientificGrammarPolicy(
        **{**{name: getattr(policy(), name) for name in policy().__dataclass_fields__},
           "schema": "ScientificGrammarPolicy@incompatible"}
    )
    with pytest.raises(ValueError, match="INCOMPATIBLE_POLICY_SCHEMA"):
        bad.require_version()
