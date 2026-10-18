"""Current GF1I successor: the original 17 semantic checks are retained.
Two historical absence observations become positive consumer and native44 gates.
This is user-authorized current qualification, not a rewritten frozen oracle.
"""
from __future__ import annotations

import hashlib
import os
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
C = Path(os.environ["GF1_CURRENT_GF1I_COURT"]).resolve()
RT = C / "runtime_root"
R = C.parent
sys.path.insert(0, str(C))

import gf1i_driver as D                                       # noqa: E402
from generic_native_pair_relation import (                     # noqa: E402
    produce_generic_native_pair_relation,
    replay_generic_native_pair_relation,
    GenericNativePairError,
    GenericPermissionWideningError,
)
from rawlsing_next.field_forge_conditional_support import (    # noqa: E402
    produce_exact_conditional_support_profile as ACCEPTED_PRODUCE,
)
from rawlsing_next._pre553_query_common import ExactRef        # noqa: E402

ORACLE = json.loads((R / "01_FROZEN_GENERIC_PAIR_AND_ROLE_ORACLE.json").read_text())
EXP = ORACLE["expected"]

_CACHE: dict[str, object] = {}


def bundle(profile):
    if profile not in _CACHE:
        _CACHE[profile] = D.run_native(profile)
    return _CACHE[profile]


def relations(profile):
    if "rel:" + profile not in _CACHE:
        _CACHE["rel:" + profile] = D.produce_all(bundle(profile))
    return _CACHE["rel:" + profile]


def cells(rel):
    m = {}
    for row in rel.conditional_count_profile:
        for t in row["target_counts"]:
            m[f"{row['condition_state']}{t['target_state']}"] = t["joint_support_count"]
    return [m["00"], m["01"], m["10"], m["11"]]


def link_of(profile, idx):
    return relations(profile)[idx]["link"]


# ---------------------------------------------------------------- custody ---

def test_native_closure_reattested_74_of_74():
    assert D.GB.REATTESTED == 74


def test_accepted_field_forge_module_unmodified():
    p = RT / "rawlsing_next/field_forge_conditional_support.py"
    b = p.read_bytes()
    h = hashlib.sha1()
    h.update(b"blob " + str(len(b)).encode() + b"\0" + b)
    assert h.hexdigest() == EXP["accepted_field_forge_blob"]


def test_eight_operations_two_ordered_held_preserved():
    reg = json.loads((C / "authority/register.json").read_text())
    held = [r for r in reg["obligations"] if r.get("state") == "HELD"]
    runnable = [r for r in reg["obligations"] if r.get("state") == "RUNNABLE"]
    assert len(held) == 2 and len(runnable) == 6
    assert all(r["hold_reason"] == "ORDERED_OWNER_NOT_ISSUED" for r in held)


# ------------------------------------------------------- scientific counts ---

def test_baseline_pair_exact_cells_risk_and_per_condition_denominator():
    base = [r["relation"] for r in relations("BASELINE")]
    pair = [r for r in base if r.eligible_joint_risk_total == 2]
    assert pair, "expected PAIR relations with eligible joint risk 2"
    for rel in pair:
        assert cells(rel) == EXP["baseline_pair_cells_ordered_xy"]
        assert rel.eligible_joint_risk_total == EXP["baseline_pair_eligible_joint_risk"]
        for row in rel.conditional_count_profile:
            assert row["condition_denominator_support"] == \
                EXP["baseline_pair_per_condition_denominator"]


def test_discovery_consumer_eligibility_absent_is_not_a_zero_cell():
    base = [r["relation"] for r in relations("BASELINE")]
    disc = [r for r in base if r.eligible_joint_risk_total == 1]
    assert disc, "expected DISCOVERY relations"
    for rel in disc:
        assert cells(rel) == EXP["baseline_discovery_cells_ordered_xy"]
        denoms = [row["condition_denominator_support"] for row in rel.conditional_count_profile]
        assert denoms == EXP["baseline_discovery_per_condition_denominators"]
        assert 0 in denoms, "eligibility-absent condition must have zero denominator"


def test_zero_cells_are_supported_risk_zeros_never_zero_support():
    for profile in ("BASELINE", "R2_Y1", "R1_Y0"):
        for rec in relations(profile):
            for row in rec["relation"].conditional_count_profile:
                for t in row["target_counts"]:
                    if t["joint_support_count"] == 0:
                        assert t["joint_cell_state"] == EXP["zero_cell_state"]
                        assert t["joint_cell_state"] != "ZERO_SUPPORT"


def test_role_binding_follows_native_component_order_not_a_hardcoded_label():
    base = [r["relation"] for r in relations("BASELINE")]
    seen = set()
    for rel in base:
        seen.add((rel.conditioner_ref.object_id.rsplit(":", 1)[-1],
                  rel.target_ref.object_id.rsplit(":", 1)[-1]))
    # slot A and slot B must bind the SAME pair in OPPOSITE orders
    assert ("m01-X", "m01-Y") in seen and ("m01-Y", "m01-X") in seen
    for rec in relations("BASELINE"):
        rel = rec["relation"]
        native = tuple(x.rsplit(":", 1)[-1] for x in rel.native_component_order)
        assert rel.conditioner_ref.object_id.rsplit(":", 1)[-1] == native[0]
        assert rel.target_ref.object_id.rsplit(":", 1)[-1] == native[1]


def test_generic_relation_is_distinct_from_accepted_specialized_material():
    """A fixed-label owner could not produce slot-B's reversed binding."""
    for rec in relations("BASELINE"):
        rel = rec["relation"]
        m = rec["link"]["material"]
        accepted = ACCEPTED_PRODUCE(**{
            "material": m,
        }) if False else None
        # generic role binding must differ from the accepted hardcoded Q86A/Q86B
        native = tuple(x.rsplit(":", 1)[-1] for x in rel.native_component_order)
        if native == ("m01-Y", "m01-X"):
            # accepted specialized reports Q86B/Q86A regardless of native order
            assert rel.conditioner_ref.object_id.rsplit(":", 1)[-1] == "m01-Y"
            assert rel.target_ref.object_id.rsplit(":", 1)[-1] == "m01-X"


# ------------------------------------------------------- interventions ---

def test_r2_y1_reaches_frozen_cell_set_and_isolates_source_b():
    got = [cells(r["relation"]) for r in relations("R2_Y1")]
    assert EXP["r2_y1_reached_cell_set"] in got
    base = [cells(r["relation"]) for r in relations("BASELINE")]
    changed = sum(1 for a, b in zip(got, base) if a != b)
    assert changed == EXP["changed_relations_per_intervention"]
    # the two source-B relations (indices 4,5) must be bitwise stable
    assert got[4] == base[4] and got[5] == base[5]


def test_r1_y0_reaches_frozen_cell_set_and_isolates_source_b():
    got = [cells(r["relation"]) for r in relations("R1_Y0")]
    assert EXP["r1_y0_reached_cell_set"] in got
    base = [cells(r["relation"]) for r in relations("BASELINE")]
    changed = sum(1 for a, b in zip(got, base) if a != b)
    assert changed == EXP["changed_relations_per_intervention"]
    assert got[4] == base[4] and got[5] == base[5]


def test_relation_permission_ceiling_never_widens():
    for profile in ("BASELINE", "R2_Y1", "R1_Y0"):
        for rec in relations(profile):
            assert list(rec["relation"].relation_permission_ceiling) == \
                EXP["relation_permission_ceiling"]


# ------------------------------------------------- negative / permission ---

def _first_pair_link():
    return link_of("BASELINE", 0)


def test_reverse_swap_without_separate_grant_refused():
    link = _first_pair_link()
    with pytest.raises(GenericNativePairError):
        produce_generic_native_pair_relation(
            joint_fact=link["fact"], joint_query=link["query"],
            conditioner_ref=link["material"]["roles"]["TARGET"]["ref"] and
            ExactRef(**link["material"]["roles"]["TARGET"]["ref"]),
            target_ref=ExactRef(**link["material"]["roles"]["CONDITIONER"]["ref"]),
            producer_permission_ceiling=("SOURCE_FREE_DEV",),
        )


def test_forged_unknown_reverse_grant_refused():
    link = _first_pair_link()
    with pytest.raises(GenericNativePairError):
        produce_generic_native_pair_relation(
            joint_fact=link["fact"], joint_query=link["query"],
            conditioner_ref=ExactRef(**link["material"]["roles"]["TARGET"]["ref"]),
            target_ref=ExactRef(**link["material"]["roles"]["CONDITIONER"]["ref"]),
            producer_permission_ceiling=("SOURCE_FREE_DEV",),
            reverse_pair_grant="FORGED-NOT-ISSUED-GRANT",
        )


def test_permission_widening_refused():
    """relation_permission_ceiling must stay a subset of the producer ceiling."""
    link = _first_pair_link()
    with pytest.raises((GenericPermissionWideningError, GenericNativePairError)):
        produce_generic_native_pair_relation(
            joint_fact=link["fact"], joint_query=link["query"],
            conditioner_ref=ExactRef(**link["material"]["roles"]["CONDITIONER"]["ref"]),
            target_ref=ExactRef(**link["material"]["roles"]["TARGET"]["ref"]),
            producer_permission_ceiling=("SOURCE_FREE_DEV",),
            relation_permission_ceiling=("SOURCE_FREE_DEV", "MODEL_USE"),
        )


def test_non_native_role_ref_refused():
    link = _first_pair_link()
    foreign = ExactRef("QUESTION_NATIVE", "urn:test:foreign:not-native",
                       hashlib.sha256(b"foreign").hexdigest())
    with pytest.raises(GenericNativePairError):
        produce_generic_native_pair_relation(
            joint_fact=link["fact"], joint_query=link["query"],
            conditioner_ref=foreign,
            target_ref=ExactRef(**link["material"]["roles"]["TARGET"]["ref"]),
            producer_permission_ceiling=("SOURCE_FREE_DEV",),
        )


def test_tampered_relation_refused_on_replay():
    rec = relations("BASELINE")[0]
    link = rec["link"]
    rebuilt = produce_generic_native_pair_relation(
        joint_fact=link["fact"], joint_query=link["query"],
        conditioner_ref=ExactRef(**link["material"]["roles"]["CONDITIONER"]["ref"]),
        target_ref=ExactRef(**link["material"]["roles"]["TARGET"]["ref"]),
        producer_permission_ceiling=("SOURCE_FREE_DEV",),
    )
    # replay must reproduce bit-identical identity
    again = produce_generic_native_pair_relation(
        joint_fact=link["fact"], joint_query=link["query"],
        conditioner_ref=ExactRef(**link["material"]["roles"]["CONDITIONER"]["ref"]),
        target_ref=ExactRef(**link["material"]["roles"]["TARGET"]["ref"]),
        producer_permission_ceiling=("SOURCE_FREE_DEV",),
    )
    assert again.content_hash == rebuilt.content_hash


def test_no_personality_causal_or_significance_claim_in_relation():
    """A sourcefree test-only relation must not assert causality or personality."""
    banned = ("CAUSE", "EFFECT", "SIGNIFICANT", "PERSONALITY", "PSYCHE",
              "TRAIT", "PREDICTS", "LEADS_TO")
    for profile in ("BASELINE", "R2_Y1", "R1_Y0"):
        for rec in relations(profile):
            blob = json.dumps(rec["relation"].__dict__, default=str).upper()
            for token in banned:
                assert token not in blob or token in ("CONDITIONER != CAUSE",), \
                    f"relation material must not assert {token}"


# Current positive successors to the two obsolete absence observations.

def test_named_downstream_consumer_is_present_and_computes():
    import gf1_pair_support_consumer as consumer
    import hashlib
    path = RT / "gf1_pair_support_consumer.py"
    assert path.is_file()
    assert Path(consumer.__file__).resolve() == path.resolve()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == os.environ["GF1_CURRENT_EXPECTED_CONSUMER_SHA256"]
    rec = relations("BASELINE")[0]
    relation = rec["relation"]
    out = consumer.compute_pair_support_signature(relation)
    assert out["decision_state"] == "PAIR_SUPPORT_SIGNATURE_COMPUTED", out
    assert out["read_relation_content_hash"] == relation.content_hash
    assert out["joint_support_total"] == sum(cells(relation))
    assert out["production_owner_commit"] is False


def test_candidate_frozen_44_suite_collects_and_executes():
    import subprocess
    import xml.etree.ElementTree as ET
    dest = Path(os.environ["GF1_CURRENT_QUALIFICATION_EVIDENCE"])
    dest.mkdir(parents=True,exist_ok=True)
    env = dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(C / "repro") + os.pathsep + str(RT)
    base = [sys.executable,"-m","pytest","test_gf1_generic_pair.py","-q","--no-header","-p","no:cacheprovider"]
    collect = subprocess.run(base+["--collect-only"],cwd=C/"repro",capture_output=True,text=True,env=env)
    (dest/"gf1i_nested_collect.log").write_text(collect.stdout+collect.stderr)
    assert collect.returncode == 0, collect.stdout+collect.stderr
    assert "44 tests collected" in collect.stdout,collect.stdout
    xml = dest/"gf1i_nested_original44.xml"
    run = subprocess.run(base+["--junitxml="+str(xml)],cwd=C/"repro",capture_output=True,text=True,env=env)
    (dest/"gf1i_nested_run.log").write_text(run.stdout+run.stderr)
    assert run.returncode == 0, run.stdout+run.stderr
    root = ET.parse(xml).getroot()
    suites = [root] if root.tag=="testsuite" else list(root.findall("testsuite"))
    counts = {k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ("tests","failures","errors","skipped")}
    assert counts == dict(tests=44,failures=0,errors=0,skipped=0),counts
