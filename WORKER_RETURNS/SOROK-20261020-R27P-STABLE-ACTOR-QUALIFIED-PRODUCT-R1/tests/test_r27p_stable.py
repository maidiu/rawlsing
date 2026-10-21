"""R27P stable historical-actor injection, seven faults, cold and C12/A0/A2."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CAND = ROOT / "candidate"
sys.path.insert(0, str(CAND))
sys.path.insert(0, str(ROOT.parents[1]))
import stable_actor_binding as S
import historical_actor_producer as H
import native_ports as N
import bp2_joined.producer as P


def test_stable_injection_does_not_mutate_global_builder(tmp_path):
    original = P.build_two_actor_life
    r = S.run_stable("A_REPAIR_LONG", tmp_path / "one")
    assert P.build_two_actor_life is original
    assert r["actor_id"] == "TEST_ONLY_BP1_R26V_ACTOR_A"
    assert r["a0_claims"] == ["ARRIVAL"]
    assert r["a0_tools_remaining"] == 1
    assert r["a2_clock"] == 40
    assert "OFFSCREEN_REPAIR" in r["a2_offscreen_kinds"]
    assert r["a2_other_completed_units"] == 5
    assert r["c12_world_hash"] and r["c12_clock"] == 40
    assert S.assert_stable(r, expected_target=r["target_id"],
                           expected_source_hash=r["actor_source_hash"])["status"] == "PASS"


def test_branch_isolation_a_b_a_no_global_carry(tmp_path):
    original = P.build_two_actor_life
    a1 = S.run_stable("A_REPAIR_LONG", tmp_path / "a1")
    b = S.run_stable("B_RESOURCE_RICH", tmp_path / "b")
    a2 = S.run_stable("A_REPAIR_LONG", tmp_path / "a2")
    assert P.build_two_actor_life is original
    assert a1["actor_source_hash"] == a2["actor_source_hash"]
    assert a1["actor_source_hash"] != b["actor_source_hash"]
    assert a1["life"]["actor_ids"][0] == a2["life"]["actor_ids"][0]
    assert a1["target_id"] != b["target_id"]


def test_seven_actor_source_faults_prove_and_restore(tmp_path):
    receipt = S.seven_actor_source_faults(tmp_path / "cuts")
    assert len(receipt["trials"]) == 7
    assert receipt["all_proved"] is True
    edges = {t["edge"] for t in receipt["trials"]}
    assert edges == {"ACTOR_SOURCE_GENESIS", "A_OWN_OMISSION", "B_INDEPENDENT_ACT",
                     "ADP010_ENCOUNTER", "E1_C8_PROOF", "A_T_TARGET_GRANT",
                     "INDEPENDENT_E2"}
    for trial in receipt["trials"]:
        assert trial["red"]["status"] == "RED"
        assert trial["restored"]["status"] == "PASS"
        assert trial["proves"] is True


def test_alternatives_h0_and_no_material_are_lawful():
    h0 = H.build_no_development_record()
    assert h0["performed_actions"] == []
    assert h0["practice_established"] is False
    with pytest.raises(Exception):
        H.build_life("A_NO_MATERIAL")
    good = H.build_life("A_REPAIR_LONG")
    assert good.a_snapshot["state"]["completed_units"] >= 1


def test_actor_privacy_and_event_kinds_are_source_owned(tmp_path):
    r = S.run_stable("A_REPAIR_LONG", tmp_path / "privacy")
    kinds = r["life"]["event_kinds"]
    assert kinds["TEST_ONLY_BP1_R26V_ACTOR_B"][-1] == "NO_CHANGE"
    assert kinds["TEST_ONLY_BP1_R26V_ACTOR_A"][-1] == "NO_CHANGE"
    assert r["native_claims"] == {"actor": False, "rule": False, "c8_trust": False,
                                  "world": False, "c12": False, "c11": False}
    a0 = r["a0_projects"]
    assert len(a0) == 1
    assert "cash" not in r["life"]


def test_native_ports_remain_unissued():
    assert set(N.NativeHistoricalActorPorts().probe_all().values()) == {
        "NATIVE_AUTHORITY_UNISSUED"}


def test_cold_process_stable_replay(tmp_path):
    code = (
        "import json,sys;"
        f"sys.path.insert(0,{str(CAND)!r});"
        f"sys.path.insert(0,{str(ROOT.parents[1])!r});"
        "import stable_actor_binding as S;"
        "r=S.run_stable('A_REPAIR_LONG',sys.argv[1]);"
        "print(json.dumps({'c8':r['c8_state_digest'],'source':r['actor_source_hash'],"
        "'a0':r['a0_claims'],'tools':r['a0_tools_remaining'],'a2':r['a2_clock'],"
        "'kinds':r['a2_offscreen_kinds'],'other':r['a2_other_completed_units'],"
        "'c12':r['c12_world_hash']},sort_keys=True))"
    )
    env = dict(os.environ, PYTHONPATH=str(CAND) + os.pathsep + str(ROOT.parents[1]))
    outs = []
    for i in range(2):
        proc = subprocess.run([sys.executable, "-B", "-c", code, str(tmp_path / f"cold{i}")],
                              capture_output=True, text=True, env=env,
                              cwd=str(ROOT.parents[1]), timeout=240)
        assert proc.returncode == 0, proc.stderr[-1000:]
        outs.append(json.loads(proc.stdout.strip().splitlines()[-1]))
    assert outs[0]["c8"] == outs[1]["c8"]
    assert outs[0]["source"] == outs[1]["source"]
    assert outs[0]["a0"] == outs[1]["a0"]
    assert outs[0]["tools"] == outs[1]["tools"]
    assert outs[0]["a2"] == outs[1]["a2"]
    assert outs[0]["kinds"] == outs[1]["kinds"]
    assert outs[0]["other"] == outs[1]["other"]
    assert outs[0]["c12"] and outs[1]["c12"]
    warm = S.run_stable("A_REPAIR_LONG", tmp_path / "warm")
    assert outs[0]["c8"] == warm["c8_state_digest"]
    assert outs[0]["source"] == warm["actor_source_hash"]
    assert outs[0]["a0"] == warm["a0_claims"]
    assert outs[0]["a2"] == warm["a2_clock"]
