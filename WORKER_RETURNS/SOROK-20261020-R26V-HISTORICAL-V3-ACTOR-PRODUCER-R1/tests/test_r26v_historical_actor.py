"""R26V sourcefree historical actor/other producer and BP2→BP4 downstream court."""
from __future__ import annotations

import dataclasses
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
import historical_actor_producer as H
import native_ports as N


def test_two_genesis_histories_are_distinct_and_not_role_psychology():
    a = H.build_life("A_REPAIR_LONG")
    b = H.build_life("B_RESOURCE_RICH")
    assert a.a_source.actor_id == b.a_source.actor_id
    assert a.a_source.actor_id != a.b_source.actor_id
    assert a.a_source.source_hash != b.a_source.source_hash
    assert a.a_snapshot["state_hash"] != b.a_snapshot["state_hash"]
    assert a.a_snapshot["state"]["cash"] != b.a_snapshot["state"]["cash"]
    assert a.historical_receipt["event_kinds"][a.a_source.actor_id][-1] == "NO_CHANGE"
    assert a.historical_receipt["event_kinds"][a.b_source.actor_id][-1] == "NO_CHANGE"
    assert a.historical_receipt["psychology_claim"] is False
    assert a.historical_receipt["native_actor"] is False
    assert "CHILDHOOD_HISTORY_SPARSE" in a.a_source.known_unknowns


def test_new_histories_feed_real_bp2_bp4_a0_a2(tmp_path):
    r = H.run_joined("A_REPAIR_LONG", root=tmp_path / "one")
    assert r["schema"] == "R26V_JOINED_PRODUCT@1"
    assert r["life"]["variant"] == "A_REPAIR_LONG"
    assert r["target_id"]
    assert r["c8_state_digest"]
    assert r["e2_receipt_hash"]
    assert r["a0_claims"] == ["ARRIVAL"]
    assert r["a0_tools_remaining"] == 1
    assert r["a2_clock"] == 40
    assert "OFFSCREEN_REPAIR" in r["a2_offscreen_kinds"]
    assert r["native_claims"] == {"actor": False, "rule": False, "c8_trust": False,
                                  "world": False, "c12": False, "c11": False}
    receipt = H.r26v_joined_assertion(r)
    assert receipt["status"] == "PASS"
    assert receipt["native"] is False


def test_other_refusal_removal_red_same_assertion_then_restore(tmp_path):
    good = H.run_joined("A_REPAIR_LONG", root=tmp_path / "good")
    base_target = good["target_id"]
    assert H.r26v_joined_assertion(good, expected_target=base_target)["status"] == "PASS"
    bad = H.run_joined("B_NO_REFUSAL", root=tmp_path / "bad")
    assert bad["target_id"] != base_target
    with pytest.raises(AssertionError, match="R26V_TARGET_NOT_BOUND_TO_ACTOR_HISTORY"):
        H.r26v_joined_assertion(bad, expected_target=base_target)
    restored = H.run_joined("A_REPAIR_LONG", root=tmp_path / "restored")
    assert H.r26v_joined_assertion(restored, expected_target=restored["target_id"])["status"] == "PASS"


def test_focal_omission_removal_red_same_assertion_then_restore(tmp_path):
    good = H.run_joined("A_REPAIR_LONG", root=tmp_path / "good")
    bad = H.run_joined("A_NO_OMISSION", root=tmp_path / "bad")
    assert bad["target_id"] != good["target_id"]
    with pytest.raises(AssertionError, match="R26V_TARGET_NOT_BOUND_TO_ACTOR_HISTORY"):
        H.r26v_joined_assertion(bad, expected_target=good["target_id"])
    restored = H.run_joined("A_REPAIR_LONG", root=tmp_path / "restored")
    assert H.r26v_joined_assertion(restored)["status"] == "PASS"


def test_actor_performed_history_without_material_refuses_and_restores():
    with pytest.raises(Exception):
        H.build_life("A_NO_MATERIAL")
    good = H.build_life("A_REPAIR_LONG")
    assert good.a_snapshot["state"]["completed_units"] >= 1
    assert good.a_snapshot["state"]["material_remaining"] >= 0


def test_h0_no_development_remains_possible():
    h0 = H.build_no_development_record()
    assert h0["performed_actions"] == []
    assert h0["practice_established"] is False
    assert h0["native_actor"] is False
    assert "H0_NO_DEMONSTRATED_DEVELOPMENT" in h0["scientific_status"]


def test_named_downstream_assertion_reds_on_source_target_mismatch_and_restores(tmp_path):
    r = H.run_joined("A_REPAIR_LONG", root=tmp_path / "good")
    bad = dict(r)
    bad["target_id"] = "TAMPERED_TARGET"
    with pytest.raises(AssertionError, match="R26V_TARGET_NOT_BOUND_TO_ACTOR_HISTORY"):
        H.r26v_joined_assertion(bad, expected_target=r["target_id"])
    good = H.run_joined("A_REPAIR_LONG", root=tmp_path / "restored")
    assert H.r26v_joined_assertion(good)["status"] == "PASS"


def test_native_ports_all_fail_closed():
    ports = N.NativeHistoricalActorPorts()
    results = ports.probe_all()
    assert len(results) == len(ports.PORTS)
    assert set(results.values()) == {"NATIVE_AUTHORITY_UNISSUED"}


def test_cold_process_joined_history_is_stable(tmp_path):
    code = (
        "import json,sys;"
        f"sys.path.insert(0,{str(CAND)!r});"
        f"sys.path.insert(0,{str(ROOT.parents[1])!r});"
        "import historical_actor_producer as H;"
        "r=H.run_joined('A_REPAIR_LONG',root=sys.argv[1]);"
        "print(json.dumps({'c8':r['c8_state_digest'],'a0':r['a0_claims'],"
        "'tools':r['a0_tools_remaining'],'a2':r['a2_clock'],'other':r['a2_other_completed_units'],"
        "'kinds':r['a2_offscreen_kinds']},sort_keys=True))"
    )
    env = dict(os.environ, PYTHONPATH=str(CAND) + os.pathsep + str(ROOT.parents[1]))
    outs = []
    for i in range(2):
        proc = subprocess.run([sys.executable, "-B", "-c", code, str(tmp_path / f"cold{i}")],
                              capture_output=True, text=True, env=env,
                              cwd=str(ROOT.parents[1]), timeout=240)
        assert proc.returncode == 0, proc.stderr[-1000:]
        outs.append(json.loads(proc.stdout.strip().splitlines()[-1]))
    assert outs[0] == outs[1]
    inproc = H.run_joined("A_REPAIR_LONG", root=tmp_path / "warm")
    assert outs[0]["c8"] == inproc["c8_state_digest"]
    assert outs[0]["a0"] == inproc["a0_claims"]
    assert outs[0]["a2"] == inproc["a2_clock"]
    assert outs[0]["other"] == inproc["a2_other_completed_units"]


def test_b_refusal_and_a_omission_are_real_independent_ledger_events():
    base = H.build_life("A_REPAIR_LONG")
    assert base.b_ledger.events[-1].kind == "NO_CHANGE"
    assert base.a_ledger.events[-1].kind == "NO_CHANGE"
    assert base.b_ledger.events[-1].payload["reason"] == "OTHER_REFUSES_VOLUNTARY_EXTRA_TASK"
    assert base.a_ledger.events[-1].payload["reason"] == "FOCAL_DECLINES_OPTIONAL_TASK"
    no_b = H.build_life("B_NO_REFUSAL")
    assert all(e.kind != "NO_CHANGE" for e in no_b.b_ledger.events)
    no_a = H.build_life("A_NO_OMISSION")
    assert all(e.kind != "NO_CHANGE" for e in no_a.a_ledger.events)
