"""Independent GF1J *post-preregistration* scientific identity hostiles.

Do NOT count as Phase A prior frozen oracle. Run against pinned GF1H court:
GF1J_GF1G_TEST=/abs/.../phase_a/test_gf1g_precommitted.py
GF1G_COURT=/abs/.../R17 COURT
GF1G_ORACLE=/abs/.../GF1G/01_FROZEN_ORACLE.json
"""
from copy import deepcopy
import importlib.util
import os
from pathlib import Path
import pytest

spec=importlib.util.spec_from_file_location("gf1j_helper",Path(os.environ["GF1J_GF1G_TEST"]))
h=importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

def _make(change):
    rel=h._rebuild(counts={"00":1,"11":1},eligible=2)
    f=dict(rel.__dict__)
    f.pop("content_hash")
    f.pop("object_id")
    f["conditional_count_profile"]=deepcopy(f["conditional_count_profile"])
    change(f)
    digest=h.G.semantic_hash(h.G._projection(f))
    return h.G.GenericNativePairRelation(
        **f,content_hash=digest,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}")

@pytest.mark.parametrize("which",["condition","target"])
def test_exact_native_state_identity_no_string_alias(which):
    def change(f):
        if which=="condition":
            # Real native conditioner domain contains string "0", not integer 0.
            f["conditional_count_profile"][0]["condition_state"]=0
        else:
            # Real native target domain contains string "0", not integer 0.
            f["conditional_count_profile"][0]["target_counts"][0]["target_state"]=0
    rel=_make(change)
    res=h.CONS(rel)
    assert res["decision_state"]=="CONSUMER_RELATION_INTEGRITY_REJECTED",res
    assert res["separation_class"] is None and res["downstream_value_produced"] is False

def test_normal_exact_native_state_remains_positive():
    rel=h._rebuild(counts={"00":1,"11":1},eligible=2)
    res=h.CONS(rel)
    assert res["decision_state"]=="PAIR_SUPPORT_SIGNATURE_COMPUTED"
    assert res["separation_class"]=="EXACT_PAIR_SEPARATION"
