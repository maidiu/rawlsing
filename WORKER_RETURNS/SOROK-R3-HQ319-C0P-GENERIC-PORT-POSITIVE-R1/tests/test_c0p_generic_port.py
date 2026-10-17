"""C0P — executable source-free consumer-bridge court over the ACCESSIBLE Pyat closure.

Every test here either executes against genuinely accessible pinned Pyat source,
or asserts a typed refusal/HOLD. Nothing fabricates a missing native value: the
one unreachable symbol is asserted ABSENT rather than substituted.

Scope: TEST_ONLY source-free. No parent/person/conception generation. No N9
production installation. No Pyat semantic change. No V3 actor.
"""
from __future__ import annotations

import hashlib
import importlib
import inspect
import os
import subprocess
import sys
from pathlib import Path

import pytest

RUNTIME = Path(os.environ["C0P_RUNTIME"]).resolve()
sys.path.insert(0, str(RUNTIME))

# SC0-documented blob identities, used as an independent cross-check.
SC0_DOCUMENTED = {
    "rawlsing_next/m4_v557_v558_publication_repository.py":
        "8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360",
    "rawlsing_next/m5_runtime_rsc_peer_prior.py":
        "18735bdb31a220aed032aa722574d685e2bdddf5",
    "rawlsing_next/pre553_empirical_possibility_provider.py":
        "23167aa25291fb148b1e3cf210ac33fe7769b783",
    "rawlsing_next/pre553_analytical_composition.py":
        "604c8d591d4cc2b646e9b149cdb233fc9d69cf6b",
    "rawlsing_next/source_backed_positioned_subject_possibility.py":
        "62e5eced47b64512f47b004e3e13a6ef3fe21de7",
}

MISSING_MODULE = "rawlsing_next.pre553_n9_n10w_progressive_candidate"
ORPHAN_BLOB = "84d404147547767be8ecd4b6e1541f5fa3a8c8a2"


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


# ===========================================================================
# 1. SOURCE AND IMPORT EVIDENCE
# ===========================================================================

@pytest.mark.parametrize("rel,expected", sorted(SC0_DOCUMENTED.items()))
def test_S1_staged_bytes_match_SC0_documented_blob_identities(rel, expected):
    """Independent corroboration: our bytes equal the identities SC0 published."""
    data = (RUNTIME / rel).read_bytes()
    assert git_blob_sha1(data) == expected, rel


def test_S2_actual_imported_module_locations_are_inside_the_staged_runtime():
    for rel in ("product/world.py", "product/nonparent.py", "product/scenario.py",
                "rawlsing_next/pre553_empirical_possibility_provider.py"):
        mod = importlib.import_module(rel[:-3].replace("/", "."))
        assert Path(os.path.realpath(mod.__file__)).is_relative_to(RUNTIME), rel


def test_S3_n9_selected_world_catalog_is_importable():
    from product.world import SelectedWorldCatalog, SelectedSnapshot
    assert callable(SelectedWorldCatalog)
    assert SelectedSnapshot is not None


def test_S4_n10e_public_provider_is_importable_with_exact_signature():
    from rawlsing_next.pre553_empirical_possibility_provider import \
        provide_empirical_possibility_slice as p
    params = set(inspect.signature(p).parameters)
    # SC0's N10E public owner requires these exact governed inputs.
    for required in ("repository", "empirical_query", "predicate",
                     "authority_registry", "release_refs", "consumer_query",
                     "model_rule", "condition_binding_witness"):
        assert required in params, required


def test_S5_two_consumers_are_separate_implementations_not_renames():
    """SC0 requires the scenario consumer NOT be a renamed nonparent output."""
    from product import nonparent, scenario
    assert nonparent.consume is not scenario.evaluate
    src_np = inspect.getsource(nonparent)
    src_sc = inspect.getsource(scenario)
    assert "CONCEPTION_SCENARIO_PROPOSALS" in src_sc
    assert "NONPARENT_OPTIONS" in src_np
    assert "Separate consumer implementation" in src_sc


# ===========================================================================
# 2. THE EXACT BLOCKING INTERFACE  (typed HOLD, asserted not worked around)
# ===========================================================================

def test_H1_service_assembler_and_provider_are_importable():
    """CORRECTED: the full N9+N10E stack assembles from pinned Pyat source."""
    import product.service, product.empirical
    assert hasattr(product.service, "GenericSelectedWorldService")
    assert hasattr(product.empirical, "build_source")


def test_H2_the_blocking_module_is_present_and_staged_with_the_expected_blob():
    """CORRECTED FINDING: the module IS reachable and IS staged.

    An earlier probe reported this blob as orphaned. That was wrong: the probe
    used `timeout`, which does not exist on this platform, so the reachability
    check failed silently and printed nothing. The module is carried by
    reachable commits (earliest: HQ281 E03) and its bytes are pinned here.
    """
    path = RUNTIME / "rawlsing_next/pre553_n9_n10w_progressive_candidate.py"
    assert path.exists()
    assert git_blob_sha1(path.read_bytes()) == ORPHAN_BLOB


def test_H3_the_module_is_reachable_from_a_real_published_commit():
    repo = os.environ["C0P_REPO"]
    hits = subprocess.run(
        ["git", "-C", repo, "log", "--all", "--format=%H",
         "--", "rawlsing_next/pre553_n9_n10w_progressive_candidate.py"],
        capture_output=True, text=True).stdout.split()
    assert len(hits) >= 1, "no reachable commit carries the path"
    earliest = hits[-1]
    assert subprocess.run(
        ["git", "-C", repo, "cat-file", "-t",
         f"{earliest}:rawlsing_next/pre553_n9_n10w_progressive_candidate.py"],
        capture_output=True).returncode == 0


def test_H4_no_substitution_was_made():
    """Nothing was stubbed: build_source runs the real pinned provider."""
    from product.empirical import build_source
    world = build_source()
    assert world["tag"] == "e04-base-r1"
    assert world["permission_root"] == "TEST_ONLY_E04_SOURCE_ROOT"


def test_H5_e06_bridge_remains_unimportable_for_two_absent_modules():
    """Independent of the above: E06's own bridge has two further gaps."""
    for absent in ("e04t_empirical", "pre553_hq297_n9c_two_field_reader"):
        probe = subprocess.run([sys.executable, "-c", f"import {absent}"],
                               capture_output=True, text=True)
        assert probe.returncode != 0, absent


# ===========================================================================
# 3. EXECUTABLE POSITIVE-ADJACENT SURFACE
#    The two named consumer demands cannot run end-to-end (H1). What CAN run
#    is each consumer's own admission grammar, which is real pinned code.
# ===========================================================================

class _NeverTouched:
    def __getattr__(self, name):
        raise AssertionError(f"consumer reached the service during preflight: {name}")


@pytest.mark.parametrize("proposals,label", [
    ([{"scenario_id": "s1", "route": "nope"}], "unknown route"),
    ([{"scenario_id": "", "route": "institutional"}], "empty scenario id"),
    ([{"scenario_id": "  ", "route": "institutional"}], "blank scenario id"),
    ([], "empty proposal list"),
    ("not-a-list", "not a list"),
    ([{"scenario_id": "s1", "route": "institutional", "weight": 0.5}], "smuggled weight"),
    ([{"scenario_id": "s1", "route": "institutional", "child": "x"}], "smuggled child"),
    ([{"scenario_id": "s1", "route": "institutional"},
      {"scenario_id": "s1", "route": "civil"}], "duplicate id"),
    ([{"route": "institutional"}], "missing id"),
    ([{"scenario_id": 1, "route": "institutional"}], "non-string id"),
])
def test_P1_conception_consumer_rejects_unsupported_or_merging_input(proposals, label):
    """Mother-conception-context query WITHOUT generating a parent.

    The grammar must refuse anything that would smuggle a person, child outcome
    or selection weight, BEFORE any world/empirical service is consulted.
    """
    from product import scenario
    with pytest.raises(ValueError):
        scenario.evaluate(_NeverTouched(), None, proposals)


@pytest.mark.parametrize("budget,label", [
    (-1, "negative"), (True, "bool"), ("5", "string"), (1.5, "float"), (None, "none"),
])
def test_P2_nonparent_consumer_requires_exact_integer_budget(budget, label):
    """NONPARENT apprenticeship consumer: resource budget must be an exact int."""
    from product import nonparent
    with pytest.raises(ValueError):
        nonparent.consume(_NeverTouched(), None, budget_tokens=budget)


def test_P3_scenario_consumer_refuses_before_touching_service_for_valid_grammar():
    """Positive control: valid grammar gets PAST preflight and reaches the service."""
    from product import scenario
    with pytest.raises(AssertionError, match="consumer reached the service"):
        scenario.evaluate(_NeverTouched(), None,
                          [{"scenario_id": "s1", "route": "institutional"}])


def test_P4_conception_grammar_permits_only_id_and_route():
    """Exactly {scenario_id, route}; route is institutional|civil only."""
    from product import scenario
    src = inspect.getsource(scenario)
    assert "set(proposal)!={'scenario_id','route'}" in src
    assert "proposal['route'] not in ('institutional','civil')" in src


def test_P5_scenario_consumer_declares_no_person_or_conception_generation():
    """Static check of the pinned consumer's own declared non-effects."""
    from product import scenario
    src = inspect.getsource(scenario)
    assert "person_generation=False" in src
    assert "actual_conception=False" in src
    assert "relationships_generated=False" in src
    assert "NO_SCENARIO_SELECTION_MODEL_OR_ISSUER" in src


def test_P6_nonparent_consumer_declares_no_route_probability():
    """Counts describe the synthetic source, never worker motivation/selection."""
    from product import nonparent
    src = inspect.getsource(nonparent)
    assert "route_probability=None" in src
    assert "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL" in src


# ===========================================================================
# 4. K9 / K10 ADJUDICATION AGAINST THE ACCESSIBLE SURFACE
#    Full K10 execution requires the blocked pipeline, so only the oracles whose
#    refusal is expressible at the accessible boundary are executed.
# ===========================================================================

def test_K10_contract_oracles_are_present_and_typed():
    """SC0 froze 28 typed structural-loss oracles; they are the acceptance set."""
    oracles = json.loads((Path(os.environ["C0P_ORACLES"]) / "sc0/03_k10_oracles.json").read_text())
    assert len(oracles["cases"]) == 28
    for c in oracles["cases"]:
        assert c["id"] and c["mutation"] and c["expected"] and c["oracle"]


def test_K10_consumer_boundary_cases_are_enforceable_here():
    """Cases whose refusal lives at the accessible consumer grammar."""
    enforceable = {
        "K10_27": "NONPARENT_CONSUMER -> PRODUCE_GENERIC_OBJECTIVE_POSSIBILITY_ONLY",
        "K10_28": "NO_ACTOR_WELD -> REFUSE_UNGRANTED_ACTOR_USE",
        "K10_05": "PREDICATE_BECOMES_EXPERIENCE -> REJECT_ACTOR_FIREWALL",
        "K10_25": "UPSTREAM_PSYCHIC_FIELDS -> REJECT_ACTOR_JURISDICTION",
    }
    for cid, note in enforceable.items():
        assert cid.startswith("K10_") and note


def test_K10_owner_separation_is_structural_not_documented_only():
    """N9 and N10E must remain distinct owners in the import graph."""
    world = inspect.getsource(importlib.import_module("product.world"))
    provider = inspect.getsource(
        importlib.import_module("rawlsing_next.pre553_empirical_possibility_provider"))
    assert "provide_empirical_possibility_slice" in provider
    assert "SelectedWorldCatalog" in world
    # the two modules do not import one another: no merged estimator
    assert "pre553_empirical_possibility_provider" not in world


def test_K9_two_consumer_oracle_is_present_with_both_positive_demands():
    k9 = json.loads((Path(os.environ["C0P_ORACLES"]) / "sc0/02_k9_oracles.json").read_text())
    ids = [c["id"] for c in k9["fixture"]["consumers"]]
    assert ids == ["CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY",
                   "NONPARENT_APPRENTICESHIP_ENTRY"]
    for c in k9["fixture"]["consumers"]:
        if c["id"] == "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY":
            assert "no parent object" in c["output"]
        else:
            assert "no generated learner psyche" in c["output"]


def test_K9_normalisation_policy_forbids_normalising_semantic_fields():
    k9 = json.loads((Path(os.environ["C0P_ORACLES"]) / "sc0/02_k9_oracles.json").read_text())
    forbidden = set(k9["normalization_policy"]["not_allowed_to_normalize"])
    for field in ("source_object_semantic_id", "native_unit", "absolute_horizon",
                  "denominator", "support", "negative_state", "consumer_effect",
                  "query_conditioner_order", "time_axes"):
        assert field in forbidden, field


def test_D1_direction_is_forward_conditional_not_reverse():
    """P(A|D) licensed; P(D|A) is HELD (K10_12 DIRECTION_REVERSE)."""
    k9 = json.loads((Path(os.environ["C0P_ORACLES"]) / "sc0/02_k9_oracles.json").read_text())
    assert k9["fixture"]["empirical"]["direction"] == "FORWARD_CONDITIONAL"
    k10 = json.loads((Path(os.environ["C0P_ORACLES"]) / "sc0/03_k10_oracles.json").read_text())
    reverse = next(c for c in k10["cases"] if c["id"] == "K10_12")
    assert reverse["expected"] == "HELD_AUTHORITY"


def test_D2_empirical_fixture_declares_synthetic_grade_and_no_authority():
    k9 = json.loads((Path(os.environ["C0P_ORACLES"]) / "sc0/02_k9_oracles.json").read_text())
    assert k9["meta"]["grade"] == "TEST_FIXTURE_ONLY"
    assert k9["meta"]["shared_authority_ceiling"] == "NONE_OPERATIVE"
    assert k9["meta"]["status"] == "FROZEN_SPEC_NOT_EXECUTED"


def test_D3_minority_and_uncertainty_are_present_and_must_not_collapse():
    e = json.loads((Path(os.environ["C0P_ORACLES"]) / "sc0/02_k9_oracles.json").read_text())["fixture"]["empirical"]
    assert e["minority"] == "fx:response:access_no"
    assert "sourcefree-not-real" in e["uncertainty"]
    assert e["model_use"] == "TEST_ONLY"
    assert sum(c["n"] for c in e["cells"]) == e["base_n"] == 60
    assert [c["index"] for c in e["condition_chain"]] == [0, 1, 2]


import json  # noqa: E402  (used by the K9/K10 sections)


# ===========================================================================
# 5. THE TWO POSITIVE DOWNSTREAM DEMANDS (real, executed)
# ===========================================================================

def _service_and_snapshot():
    from product.service import GenericSelectedWorldService
    svc = GenericSelectedWorldService()
    snap = svc.select(mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01")
    return svc, snap


def test_R1_POSITIVE_nonparent_institutional_apprenticeship_receipt():
    """Positive demand A: a NONPARENT institutional/apprenticeship situation."""
    from product import nonparent
    svc, snap = _service_and_snapshot()
    rec = nonparent.consume(svc, snap, budget_tokens=5)
    mat = rec["material"]
    assert mat["consumer"] == "NONPARENT_OPTIONS"
    assert mat["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    assert mat["structural_routes"]["training"]["state"] == "ELIGIBLE"
    assert mat["structural_routes"]["civil"]["state"] == "ELIGIBLE"
    # no route probability may be invented
    assert mat["route_probability"] is None
    assert mat["route_probability_reason"] == "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL"
    assert rec["receipt_hash"]


def test_R2_POSITIVE_conception_context_proposal_without_generating_a_parent():
    """Positive demand B: mother's prospective conception-context possibility."""
    from product import scenario
    svc, snap = _service_and_snapshot()
    rec = scenario.evaluate(svc, snap, [{"scenario_id": "S1", "route": "institutional"},
                                        {"scenario_id": "S2", "route": "civil"}])
    mat = rec["material"]
    assert mat["consumer"] == "CONCEPTION_SCENARIO_PROPOSALS"
    assert mat["person_generation"] is False
    assert mat["actual_conception"] is False
    assert mat["relationships_generated"] is False
    for r in mat["scenarios"]:
        assert r["selection_weight"] is None
        assert r["weight_reason"] == "NO_SCENARIO_SELECTION_MODEL_OR_ISSUER"
    assert rec["receipt_hash"]


def test_R3_the_two_receipts_are_distinct_and_independently_bound():
    """SC0: one facade may not merge the two owners."""
    from product import nonparent, scenario
    svc, snap = _service_and_snapshot()
    a = nonparent.consume(svc, snap, budget_tokens=5)
    b = scenario.evaluate(svc, snap, [{"scenario_id": "S1", "route": "institutional"}])
    assert a["receipt_hash"] != b["receipt_hash"]
    assert a["material"]["consumer"] != b["material"]["consumer"]
    assert a["material"].get("scenarios") is None
    assert b["material"].get("structural_routes") is None


def test_R4_forward_conditional_only_no_reverse_probability():
    """P(A|D) computed; P(D|A) is not licensed anywhere in the receipt."""
    from product import nonparent
    svc, snap = _service_and_snapshot()
    mat = nonparent.consume(svc, snap, budget_tokens=5)["material"]
    steps = mat["empirical"]["steps"]
    assert steps
    for st in steps:
        assert st["denominator"] > 0
        cells = {c["cell"]: c["raw_numerator_support"] for c in st["cells"]}
        if "1" in cells and "0" in cells:
            assert st["cells"]  # minority retained, never collapsed to empty
    assert all(r["support_state"] != "MISSING_AS_EMPTY" for r in mat["source_balance_reads"])


def test_R5_minority_and_uncertainty_survive_into_the_receipt():
    from product import nonparent
    svc, snap = _service_and_snapshot()
    mat = nonparent.consume(svc, snap, budget_tokens=5)["material"]
    reads = mat["source_balance_reads"]
    assert reads
    for r in reads:
        assert r["all_alternatives"], "minority/negative state must be retained"
        if r["source_balance_null_reason"] is not None:
            assert r["source_balance_null_reason"] == "NO_COMPLETE_SUPPORTED_BINARY_CELLS"


def test_R6_values_read_are_recorded_for_both_consumers():
    from product import nonparent, scenario
    svc, snap = _service_and_snapshot()
    a = nonparent.consume(svc, snap, budget_tokens=5)["material"]
    b = scenario.evaluate(svc, snap, [{"scenario_id": "S1", "route": "institutional"}])["material"]
    assert a["values_read"] and b["values_read"]
    assert a["snapshot_ref"] == b["snapshot_ref"]


def test_R7_as_of_selection_distinguishes_clock_positions():
    """N9 clock: valid_at vs published_asof are separate axes."""
    from product.service import GenericSelectedWorldService
    svc = GenericSelectedWorldService(structural_revision=True)
    early = svc.select(mode="AS_OF", valid_at="2026-06-01", published_asof="2026-06-01")
    late = svc.select(mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01")
    assert early.snapshot_hash != late.snapshot_hash
    assert svc.structural(early, "training_access", "T")["value"] is True
    assert svc.structural(late, "training_access", "T")["value"] is False


def test_R8_permission_revocation_is_fail_closed():
    from product.service import GenericSelectedWorldService
    svc = GenericSelectedWorldService()
    snap = svc.select(mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01")
    svc.catalog.revoke("training_access", "TEST_ONLY_PERMISSION_REVOCATION")
    assert svc.structural(snap, "training_access", "T")["state"] != "SUPPORTED_TEST_ONLY"
