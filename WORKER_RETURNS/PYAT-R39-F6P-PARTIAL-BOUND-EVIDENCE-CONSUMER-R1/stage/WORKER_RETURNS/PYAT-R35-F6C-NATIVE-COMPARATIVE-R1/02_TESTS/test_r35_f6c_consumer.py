"""Second experiment: an ACTUAL changed F6 result carried through WP2's real
named TEST_ONLY selected-world / E04 consumer.

Every artifact asserted here was produced by the UNMODIFIED wp2.py (Git blob
55e567e4...) from WP2 commit f7824794bc6674c662734c9a8b110dd3df224be7, in three
separate cold processes differing only in which pinned F6 producer blob was
staged. See 04_REAL_CONSUMER_DELTA_AND_ALTERNATIVE_RANKING.json and
consumer_runs/wp2_consumer_substitution_receipt.json.

These assertions separate five things the mission requires be distinguished:
a method-caused delta, a delta from unrelated fixture edits, genuine
invariance, a justified no-pool/unknown result, and a refusal.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

RETURN = Path(__file__).resolve().parents[1]
RUNS = RETURN / "consumer_runs"
WP2 = "WORKER_RETURNS/PYAT-R32-WP2-NATIVE-WORLD-POSSIBILITY-R1"
REPRO = RETURN / "repro"
STAGING = RETURN / "staging"

D = {k: json.loads((RUNS / f"wp2_sub_{k}.json").read_text())
     for k in ("A", "A0", "B")}
RECEIPT = json.loads((RUNS / "wp2_consumer_substitution_receipt.json").read_text())

# Each envelope is ~9 MB. Canonicalize once and cache; repeated canonicalization
# dominated the runtime otherwise.
_CANON: dict = {}
_FULL: dict = {}


def canon(o):
    key = id(o)
    if key not in _CANON:
        _CANON[key] = json.dumps(o, sort_keys=True, separators=(",", ":"))
    return _CANON[key]


def full_canon(o):
    key = id(o)
    if key not in _FULL:
        _FULL[key] = canon(o).lower()
    return _FULL[key]


def h(o):
    return hashlib.sha256(canon(o).encode()).hexdigest()


def sidecar(key, case):
    return D[key]["generic_read_only_input"]["f6_sidecars"][case]


def uncovered(key, case):
    c = D[key]["f6_sourcefree"][case]["native_bundle"]["candidate"]
    return None if c is None else c["uncovered_target_mass"]


# ------------------------------------------------------------- custody ----

def test_wp2_code_was_never_edited_and_each_run_got_a_fresh_tree():
    assert RECEIPT["wp2_code_edited"] is False
    assert RECEIPT["wp2_repro_wp2_py_blob"] == "55e567e4d0780c251bf949268d3d477abdc76a9b"
    for k in ("A", "A0", "B"):
        r = RECEIPT["runs"][k]
        assert r["wp2_py_edited"] is False
        assert r["returncode"] == 0
        assert r["f6_producer_blob_after"] == {
            "A": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
            "A0": "182cc7970d7624f6614015f5a51d0602e1630d52",
            "B": "2df811d76db258d98d89ffb43c830cb221ff9a7d"}[k]
    b = RECEIPT["baseline_unmodified_wp2_run"]
    assert b["sha256"] == "5e7fded47aef7c1c81518881bd7667287f22699fc12234766d83712ca6f2818b"
    assert "byte-redundant with runs.B" in b["note"]
    assert not (RUNS / "wp2_baseline_F6M_B.json").exists(), \
        "the baseline envelope was removed as byte-redundant; its identity must stay recorded in the receipt"


def test_substitution_receipt_discloses_manifest_amendment():
    """A substituted run's manifest certifies the SUBSTITUTED blob, not the
    original F6M blob. The receipt must say so rather than hide it."""
    for k in ("A", "A0"):
        r = RECEIPT["runs"][k]
        assert r["manifest_no_longer_certifies_original_F6M_blob"] is True
        assert r["manifest_row_updated_to_remain_truthful"] == 1
    assert RECEIPT["runs"]["B"]["manifest_no_longer_certifies_original_F6M_blob"] is False


# ------------------------------------------- 1. METHOD-CAUSED VALUE-READ DELTA ----

def test_F6_caused_value_read_delta_exists_on_wp2s_own_inherited_frozen_case():
    """Not a synthetic case invented by this court. This is WP2's inherited
    F6L frozen case P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED, executed
    inside the real wp2.py consumer path."""
    a = sidecar("A", "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED")["conditional"]
    b = sidecar("B", "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED")["conditional"]
    assert a["state"] == "SUPPORTED_MODEL"
    assert a["probabilities"] == {"NO": "1/2", "YES": "1/2"}
    assert b["state"] == "UNAVAILABLE"
    assert b["reason"] == "NO_COMPLETE_TARGET_JOINT"
    assert "probabilities" not in b


def test_the_delta_is_method_caused_not_coverage_caused():
    """A reports full coverage where B reports unknown mass on the SAME frozen
    inputs. That is exactly the renormalization defect, reproduced in the real
    consumer path on inherited data."""
    assert uncovered("A", "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED") == "0"
    assert uncovered("B", "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED") not in (None, "0")
    assert D["A"]["f6_sourcefree"][
        "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED"]["native_bundle"]["decision"] \
        == "SYNTHETIC_CANDIDATE"
    assert D["B"]["f6_sourcefree"][
        "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED"]["native_bundle"]["decision"] \
        == "PARTIAL_IDENTIFICATION_ONLY"


def test_the_obsolete_blob_reproduces_the_same_defective_point_as_A():
    a0 = sidecar("A0", "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED")["conditional"]
    a = sidecar("A", "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED")["conditional"]
    assert a0["probabilities"] == a["probabilities"] == {"NO": "1/2", "YES": "1/2"}


# --------------------------------------------- 2. NOT A FIXTURE/SOURCE EDIT ----

def test_only_F6_scoped_keys_differ_between_methods():
    """Rules out 'a difference arising from unrelated fixture or source
    edits'. Every empirical and structural value is bit-identical across the
    three methods."""
    same, differ = set(), set()
    for k in sorted(D["B"]):
        vals = {canon(D[m][k]) for m in ("A", "B", "A0")}
        (same if len(vals) == 1 else differ).add(k)
    assert same == {"actual_C1_returns", "actual_N10E_returns",
                    "at07_native_2x2", "cases", "edge_statuses",
                    "hold", "installation", "terminal"}
    assert differ == {"call_counts", "f6_sourcefree", "generic_read_only_input"}


@pytest.mark.parametrize("key", ["actual_C1_returns", "actual_N10E_returns", "at07_native_2x2"])
def test_empirical_and_structural_values_are_bit_identical(key):
    assert len({h(D[m][key]) for m in ("A", "B", "A0")}) == 1


def test_the_same_F6_inputs_were_used_by_all_three_methods():
    """Identical inputs plus different output is the definition of a
    method-caused difference."""
    for case in ("world_a", "world_b", "P1_ORIGINAL_UNCOVERED_WORLD",
                 "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED"):
        ins = {m: canon(D[m]["f6_sourcefree"][case]["input_sources"]) for m in ("A", "B", "A0")}
        tg = {m: canon(D[m]["f6_sourcefree"][case]["input_target"]) for m in ("A", "B", "A0")}
        po = {m: canon(D[m]["f6_sourcefree"][case]["input_policy"]) for m in ("A", "B", "A0")}
        assert len(set(ins.values())) == 1, case
        assert len(set(tg.values())) == 1, case
        assert len(set(po.values())) == 1, case


# ------------------------------------------------- 3. GENUINE INVARIANCE ----

def test_world_a_is_invariant_in_value_across_all_three_methods():
    vals = {m: sidecar(m, "world_a")["conditional"]["probabilities"] for m in ("A", "B", "A0")}
    assert len({canon(v) for v in vals.values()}) == 1
    assert vals["B"] == {"formal": "26/31", "informal": "5/31"}


def test_invariant_values_are_still_bound_to_distinct_provenance():
    """Equal values under different bundle hashes. Otherwise 'invariance' would
    be indistinguishable from 'the same object counted twice'."""
    hs = {m: sidecar(m, "world_a")["bundle_hash"] for m in ("A", "B", "A0")}
    assert len(set(hs.values())) == 3


def test_world_b_is_an_invariant_refusal_across_all_three_methods():
    for m in ("A", "B", "A0"):
        c = sidecar(m, "world_b")["conditional"]
        assert c["state"] == "UNAVAILABLE"
        assert c["reason"] == "NO_COMPLETE_TARGET_JOINT"


def test_the_named_world_consumer_did_not_move_at_all():
    """The scientifically important negative. The F6 sidecar moved; the named
    consumer NONPARENT_OPTIONS did not, because at the permitted grade the
    sidecar is an inert sibling key with no data-flow edge to the consumer."""
    hsh = {m: h(D[m]["generic_read_only_input"]["nonparent_consumer"])
           for m in ("A", "B", "A0")}
    assert len(set(hsh.values())) == 1
    npc = D["B"]["generic_read_only_input"]["nonparent_consumer"]
    assert npc["consumer"] == "NONPARENT_OPTIONS"
    assert npc["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"


def test_the_invariance_is_due_to_the_hold_not_to_a_broken_experiment():
    g = D["B"]["generic_read_only_input"]
    assert g["state"] == "UNINSTALLED_TEST_ONLY_PORT"
    assert g["join_state"] == "NO_AUTHORIZED_COMMON_WORLD_OR_RESPONDENT_JOIN"
    assert g["hold"]["code"] == "NAMED_N10W_RULE_HOLD"
    assert g["actor_executions"] == 0 and g["model_calls"] == 0


def _iter_slots(o, key, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                yield path + "/" + k, v
            else:
                yield from _iter_slots(v, key, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _iter_slots(v, key, path + f"[{i}]")


def test_no_route_probability_or_selection_weight_was_ever_produced():
    """The real run DOES contain route_probability and selection_weight slots.
    Every one of them is null. Asserting the keys are absent would hide the
    more useful fact: the consumer is structurally GIVEN these slots and
    refuses to fill them, which is exactly the behaviour the mission requires.
    Counts are asserted equal across methods, so a method that quietly began
    populating them could not pass unnoticed."""
    counts = {}
    for m in ("A", "B", "A0"):
        mat = D[m]["generic_read_only_input"]["nonparent_consumer"]["consumer_material"]
        assert mat["route_probability"] is None, m
        assert "NO_JOINT" in mat["route_probability_reason"], m
        rp = list(_iter_slots(D[m], "route_probability"))
        sw = list(_iter_slots(D[m], "selection_weight"))
        assert rp and sw, m
        assert all(v is None for _, v in rp), m
        assert all(v is None for _, v in sw), m
        counts[m] = (len(rp), len(sw))
    assert len(set(counts.values())) == 1, counts
    # Exact slot counts measured in this run from the unmodified wp2.py output,
    # pinned so a future change that populates or drops a slot is a test failure
    # rather than a silent change in what the consumer is offered.
    assert counts["B"] == (15, 28), counts


def test_no_numeric_route_or_selection_value_exists_anywhere_in_the_artifacts():
    """Scan raw text for a forbidden key carrying a NUMBER. The keys are
    allowed to exist and be null; what is forbidden is any produced quantity."""
    import re
    pats = (r'"route_probability"\s*:\s*(?!null\b)[0-9]',
            r'"selection_weight"\s*:\s*(?!null\b)[0-9]',
            r'"route_propensity"\s*:\s*(?!null\b)[0-9]')
    for m in ("A", "B", "A0"):
        text = (RUNS / f"wp2_sub_{m}.json").read_text()
        for p in pats:
            hit = re.search(p, text)
            assert hit is None, (m, p, hit.group(0)[:40])


# ------------------------------------------ 4/5. NO-POOL, UNKNOWN, REFUSAL ----

@pytest.mark.parametrize("case", ["world_b", "P1_ORIGINAL_UNCOVERED_WORLD"])
def test_justified_unknown_results_survive_into_the_envelope(case):
    for m in ("A", "B", "A0"):
        c = sidecar(m, case)["conditional"]
        assert c["state"] == "UNAVAILABLE"
        assert c["reason"] == "NO_COMPLETE_TARGET_JOINT"


def test_real_use_is_refused_by_B_inside_the_real_consumer_run():
    b = D["B"]["f6_sourcefree"]["world_a"]["native_bundle"]
    assert b["real_use_authorized"] is False
    assert b["use_scope"] == "SOURCEFREE_EXPERIMENT_ONLY"
    assert b["owner_admission_status"] == "UNVERIFIED_INTEGRATION_BOUNDARY"


def test_the_consumer_is_read_only_toward_the_world_graph():
    """No canonical write, no installation, no actor. Asserted from the real
    run rather than from documentation."""
    for m in ("A", "B", "A0"):
        assert D[m]["installation"] is False
        assert D[m]["generic_read_only_input"]["actor_executions"] == 0
        assert D[m]["generic_read_only_input"]["model_calls"] == 0
        assert D[m]["terminal"] == "OWNER_CHAIN_PARTIAL_WITH_EXACT_HOLD"


def test_all_three_runs_reached_the_same_empirical_scale():
    for m in ("A", "B", "A0"):
        assert len(D[m]["actual_C1_returns"]) == 79


# ------------------------------------------------------------ honesty ----

def test_this_court_did_not_modify_wp2_sources():
    """The staged WP2 tree must still match f7824794 outside the F6 candidate
    file and the one manifest row this court disclosed amending."""
    import subprocess
    w = "WORKER_RETURNS/PYAT-R32-WP2-NATIVE-WORLD-POSSIBILITY-R1/inherited/F6M"
    out = subprocess.run(["git", "ls-tree", "-r", "f7824794bc6674c662734c9a8b110dd3df224be7",
                          "--", w], capture_output=True, text=True).stdout
    import hashlib
    root = RETURN / "02_TESTS" / w
    for line in out.strip().splitlines():
        meta, path = line.split("\t")
        _, _, blob = meta.split()
        b = (root / path[len(w) + 1:]).read_bytes()
        got = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        assert got == blob, path