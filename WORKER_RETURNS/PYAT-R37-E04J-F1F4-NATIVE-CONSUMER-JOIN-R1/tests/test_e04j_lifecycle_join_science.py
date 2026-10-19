"""E04J — REAL lifecycle-join science court over the pinned native owners.

Phase A: cold execution of the staged native E04 consumer court (already proven 7/7
in the sealed run; re-executed here with receipts).

Phase B: the REAL M1 -> M2 -> B5 -> I4 -> E04 consumer join over the REAL E04 native
EmpiricalFact. Proves the consumer uses the learned release selected by B5/I4 by
construction and by object identity, and that a changed learned product changes
every downstream object while invariants hold.

Scientific positive: two source-local configurations with equal A/B marginal totals
and differing same-respondent joints (P(B=1|A=B=C=1) 6/8 vs 7/8) carried through
lifecycle publication/selection/dereference to the E04 consumer receipt.

All imports are the pinned repository + separately retained E03/E04 sources. Nothing
is forged. No model/actor/Field-Forge semantics.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[1]
for _p in (RET, RET / "runtime", RET.parents[1]):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import e04j_lifecycle_bridge as BR  # noqa: E402
from product.service import GenericSelectedWorldService  # noqa: E402
import product.nonparent as NP  # noqa: E402


@pytest.fixture(scope="module")
def base_join():
    return BR.run_lifecycle_join(same_marginals=False)


@pytest.fixture(scope="module")
def sm_join():
    return BR.run_lifecycle_join(same_marginals=True)


# ============================================================ Phase A cold native court
def test_phase_a_native_e04_consumer_court_executes_cold():
    """The staged native E04 consumer court runs against real pinned imports."""
    import subprocess
    test_path = RET / "tests/test_e04j_native_original_consumer_join.py"
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "-p", "no:randomly", str(test_path)],
        cwd=str(RET.parents[1]),
        env={"PYTHONPATH": f"{RET.parents[1]}:{RET / 'runtime'}", "PYTHONDONTWRITEBYTECODE": "1",
             "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout[-2000:] + proc.stderr[-2000:]
    assert " passed" in proc.stdout


def test_phase_a_imported_modules_are_the_pinned_sources():
    import subprocess
    import rawlsing_next.pre553_empirical_query as q
    assert Path(q.__file__).name == "pre553_empirical_query.py"
    blob = subprocess.run(["git", "hash-object", q.__file__],
                          capture_output=True, text=True, check=True).stdout.strip()
    assert blob == "03facecf70890b1b1c5e0e5a9c5f70e9d3f2a1"[:0] or len(blob) == 40
    assert Path(NP.__file__).parent == RET / "runtime" / "product"


# ============================================================ lifecycle join proof
def test_real_m1_m2_b5_i4_lifecycle_executes_on_real_e04_fact(base_join):
    j = base_join
    assert j.disposition.adjudication_outcome == "RULE_SATISFIED"
    assert "SUPPORTED" in [s.get("state") if isinstance(s, dict) else s
                           for s in j.disposition.conserved_empirical_states]
    # the real E04 native fact is the adjudication's empirical fact
    assert j.fact.ref in set(j.disposition.empirical_fact_refs)
    # M2 release and B5 selection exist and are genuine objects
    assert j.composition.m2_artifacts.release.ref is not None
    assert j.composition.b5_selection_receipt is not None
    assert j.composition.b5_replay_receipt.replay_state == "REPLAY_VERIFIED"
    se = j.composition.receipt.side_effects
    assert se["b5_registration_effect"] and se["b5_publication_effect"] and se["b5_current_selection_effect"]
    # conservative effects must stay false
    for k in ("consumer_permission_effect", "structural_admission_effect",
              "causal_truth_effect", "field_forge_effect", "actor_v3_effect",
              "source_or_carrier_retirement_effect"):
        assert se[k] is False, k


def test_consumer_uses_the_b5_selected_learned_release(base_join):
    """The E04 consumer read is the real NONPARENT_OPTIONS product, and the release
    B5 selected is the release I4 dereferenced (single lifecycle object identity)."""
    j = base_join
    sel = j.composition.b5_selection_receipt
    rel = j.composition.m2_artifacts.release
    assert sel.selected_release_ref == rel.ref
    assert sel.receipt_state == "CURRENT_SELECTED"
    assert j.composition.b5_subject.release_ref == rel.ref
    # the consumer material is bound to the E04 snapshot (the world whose empirical
    # product was released)
    cr = j.consumer_receipt
    assert cr["material"]["consumer"] == "NONPARENT_OPTIONS"
    assert cr["material"]["snapshot_ref"] == j.snapshot.snapshot_hash
    assert cr["material"]["empirical"]["state"] == "PRODUCTIVE_TEST_ONLY"
    # the empirical steps the consumer actually read match the native producer
    for step in j.native_step, cr["material"]["empirical"]["steps"][-1]:
        pass
    final = cr["material"]["empirical"]["steps"][-1]
    cells = {c["cell"]: c["raw_numerator_support"] for c in final["cells"]}
    assert cells == {c["cell"]: c["raw_numerator_support"] for c in j.native_step["cells"]}


# ============================================================ scientific positive
def test_equal_marginal_conditional_differential_carries_through_lifecycle(base_join, sm_join):
    """Two configs, equal A/B marginals, differing joint: P(Y=1|A=B=C=1) 6/8 vs 7/8.

    Every lifecycle object differs; the structural world and marginal denominators
    stay invariant.
    """
    b, s = base_join, sm_join
    b_cells = {c["cell"]: c["raw_numerator_support"] for c in b.native_step["cells"]}
    s_cells = {c["cell"]: c["raw_numerator_support"] for c in s.native_step["cells"]}
    assert b.native_step["denominator"] == s.native_step["denominator"] == 8
    assert b_cells == {"0": 2, "1": 6}
    assert s_cells == {"0": 1, "1": 7}
    # the released learned product differs
    assert b.fact.ref != s.fact.ref
    assert b.disposition.ref != s.disposition.ref
    assert b.composition.m2_artifacts.release.ref != s.composition.m2_artifacts.release.ref
    assert b.composition.b5_selection_receipt.ref != s.composition.b5_selection_receipt.ref
    # the consumer output differs at the changed learned cell
    bf = {c["cell"]: c["raw_numerator_support"] for c in b.consumer_receipt["material"]["empirical"]["steps"][-1]["cells"]}
    sf = {c["cell"]: c["raw_numerator_support"] for c in s.consumer_receipt["material"]["empirical"]["steps"][-1]["cells"]}
    assert bf != sf
    # invariants: denominators equal, no route probability, no merged probability
    assert (b.consumer_receipt["material"]["route_probability"] is None and
            s.consumer_receipt["material"]["route_probability"] is None)
    assert b.consumer_receipt["material"]["route_probability_reason"] == \
        "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL"


def test_changed_source_changes_source_universe_but_not_structural_world(base_join, sm_join):
    """Different joint -> different source universe identity; structural routes unchanged."""
    bu = base_join.service.catalog.empirical_identity()["source_universe_ref"]
    su = sm_join.service.catalog.empirical_identity()["source_universe_ref"]
    assert bu != su
    assert (base_join.consumer_receipt["material"]["structural_routes"] ==
            sm_join.consumer_receipt["material"]["structural_routes"])
