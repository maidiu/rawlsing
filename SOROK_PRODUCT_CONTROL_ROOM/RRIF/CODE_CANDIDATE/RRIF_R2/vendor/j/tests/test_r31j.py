"""R31J pre-C9 GM01 material source to cold C12/A0/A2."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHONPATH = os.pathsep.join(str(p) for p in (
    ROOT, ROOT / "r29m" / "source", ROOT / "candidate",
    ROOT / "candidate" / "vendor" / "bp2",
    ROOT / "candidate" / "vendor" / "bp4",
    ROOT / "r29p", ROOT / "r26e", ROOT / "n1"))


def _cold(root: Path) -> dict:
    code = (
        "import json,sys;"
        "from r31j.product import R31JProduct;"
        "p=R31JProduct.reopen(sys.argv[1]);o=p.observe_verified();e=p.store.episodes('root');"
        "print(json.dumps({'status':o.get('status'),"
        "'tools':o['self']['state'].get('tools_remaining'),"
        "'completed':o['self']['state'].get('completed_units'),"
        "'material':o['self']['state'].get('material_remaining'),"
        "'episodes':[x['kind'] for x in e],"
        "'source':[x['body']['gm01_source'] for x in e if x['kind']=='GM01_SOURCE'],"
        "'c8':o.get('c8'),'target':o.get('c9'),"
        "'other':p.other()['public']['completed_units'],"
        "'verify':p.c12_verify()},sort_keys=True,default=str));p.close()")
    env = dict(os.environ, PYTHONPATH=PYTHONPATH, PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run([sys.executable, "-B", "-c", code, str(root)],
                               cwd=str(ROOT), env=env, capture_output=True,
                               text=True, timeout=240)
    assert completed.returncode == 0, completed.stderr[-2000:]
    return json.loads(completed.stdout.strip().splitlines()[-1])


def test_share_e2_pre_c9_source_reaches_product(tmp_path):
    from r31j.assertion import p01
    from r31j.runner import observable
    from r31j.scenarios import evaluated

    scenario = evaluated(share=True, e2=True)
    observed = observable(tmp_path / "share", gm01=scenario["gm01"],
                          case=scenario["case"], perform="e2", need_e2=True)
    assert p01(observed, scenario["gm01"]) is True, json.dumps(observed, indent=2, default=str)
    source = observed["source_episode"]["body"]["gm01_source"]
    assert source["b_actor"] == scenario["case"]["other"]
    assert source["b_operation"] == "SHARE_TOOL"
    assert source["b_performed"] is True
    assert source["gm01_result_hash"] == scenario["gm01"]["result_hash"]
    assert observed["c8_state_digest"] != "cd5a12fc5e1965cbba2a2ef65a6a7af62452226f0c276a061c1616366570ac38"
    assert observed["c9_target_id"]
    assert observed["c12_verify"]["ok"] is True


def test_b_refusal_changes_c9_source_decision(tmp_path):
    from r31j.build import c9_only
    from r31j.runner import observable
    from r31j.scenarios import evaluated

    good = evaluated(share=True, e2=True)
    good_obs = observable(tmp_path / "good", gm01=good["gm01"],
                          case=good["case"], perform="e2", need_e2=True)
    bad = evaluated(share=False, e2=True)
    partial, producer = c9_only(tmp_path / "bad", gm01=bad["gm01"],
                                case=bad["case"])
    try:
        assert partial["c9"]["target_branch"] == "NO_CHANGE"
        assert partial["c9"]["target_reason"] == "NO_PROPOSAL"
        assert partial["c9"]["target_id"] == ""
        assert partial["c9"]["response_status"] == "RESPONSE_EFFECTS_VALID_EMPTY"
        assert partial["c9"]["response_reason"] == "NO_ELIGIBLE_MATERIAL_SOURCE"
        assert partial["c8_state_digest"] != good_obs["c8_state_digest"]
        assert partial["e1_event_hash"] != good_obs["e1_pre_c9_hash"]
    finally:
        producer.close()


def test_share_omit_leaves_option_without_enacted_action(tmp_path):
    from r31j.assertion import share_omit
    from r31j.runner import observable
    from r31j.scenarios import evaluated

    scenario = evaluated(share=True, e2=False)
    observed = observable(tmp_path / "omit", gm01=scenario["gm01"],
                          case=scenario["case"], perform="omit", need_e2=True)
    assert share_omit(observed) is True, json.dumps(observed, indent=2, default=str)
    assert observed["source_episode"]["body"]["gm01_source"]["a_e2_performed"] is False
    assert observed["c12_verify"]["ok"] is True


def test_source_fault_and_restore_same_product(tmp_path):
    from r31j.assertion import p01
    from r31j.build import c9_only
    from r31j.runner import observable
    from r31j.scenarios import evaluated

    good = evaluated(share=True, e2=True)
    first = observable(tmp_path / "one", gm01=good["gm01"], case=good["case"],
                       perform="e2", need_e2=True)
    assert p01(first, good["gm01"]) is True

    bad = evaluated(share=False, e2=True)
    partial, producer = c9_only(tmp_path / "two", gm01=bad["gm01"],
                                case=bad["case"])
    try:
        assert partial["c9"]["target_branch"] == "NO_CHANGE"
        assert partial["c9"]["target_id"] == ""
    finally:
        producer.close()

    restored = evaluated(share=True, e2=True)
    again = observable(tmp_path / "three", gm01=restored["gm01"],
                       case=restored["case"], perform="e2", need_e2=True)
    assert p01(again, restored["gm01"]) is True


def test_cold_reopen_preserves_pre_c9_source_and_material(tmp_path):
    from r31j.runner import observable
    from r31j.scenarios import evaluated

    scenario = evaluated(share=True, e2=True)
    observed = observable(tmp_path / "cold", gm01=scenario["gm01"],
                          case=scenario["case"], perform="e2", need_e2=True)
    assert observed["tools_after"] == 0 and observed["completed_after"] == 5
    cold = _cold(tmp_path / "cold" / "product")
    assert cold["status"] == "OK"
    assert cold["tools"] == 0 and cold["completed"] == 5 and cold["material"] == 3
    assert "GM01_SOURCE" in cold["episodes"]
    assert cold["source"][0]["b_event_hash"]
    assert cold["verify"]["ok"] is True


def test_real_bp2_ports_are_test_only_and_no_grant():
    import bp2_joined.bootstrap as bootstrap
    from bp2_joined import ports
    from generative_resource import bp2_test_only_resources, candidate_resource
    from r31j.scenarios import A

    bootstrap.install()
    before = ports.production_registries()
    obj = bp2_test_only_resources(ports, candidate_resource(), A, 10)
    assert obj["rule_a"].test_only is True
    assert obj["rule_t"].test_only is True
    assert obj["grant"] is None and obj["native_issuer"] is None
    assert obj["actual_target_mutations"] == 0
    assert obj["production_registry_writes"] == 0
    after = ports.production_registries()
    assert before["response_rule_count"] == after["response_rule_count"] == 0
    assert before["target_rule_count"] == after["target_rule_count"] == 0


def test_label_only_and_e1_missing_fail_closed():
    import copy
    from generative_resource import candidate_resource, evaluate
    from r31j.scenarios import case, evaluated

    baseline = evaluate(case(share=True, e2=True), candidate_resource())
    for label in ("CLASS_B", "ENNEAGRAM_4"):
        changed = copy.deepcopy(case(share=True, e2=True))
        changed["demographic_label"] = label
        assert evaluate(changed, candidate_resource()) == baseline
    missing = case(share=True, e2=True)
    missing["records"] = [r for r in missing["records"] if r["kind"] != "E1_EVENT"]
    assert evaluate(missing, candidate_resource())["status"] == "HOLD_E1_NOT_ADMITTED_TEST_ONLY"
    assert baseline["psyche_delta"] == {}
    assert baseline["v3ms_created"] == 0
    assert baseline["rule_t_grant"] is None


def test_fork_preserves_pre_c9_source_and_diverges(tmp_path):
    from r31j.scenarios import evaluated
    from r31j.build import product

    scenario = evaluated(share=True, e2=True)
    p, built, producer = product(tmp_path / "fork", gm01=scenario["gm01"],
                                 case=scenario["case"], need_e2=True,
                                 perform="e2")
    try:
        p.material_inspect()
        p.wait(30)
        fork = p.fork("alt")
        assert fork["shared_root"]["equal"] is True
        p.use("alt")
        say = p.say("The alternate branch keeps the inspected fitting.")
        assert say["status"] == "OK"
        shared = p.store.shared_root_equal("root", "alt")
        assert shared["equal"] is True
        assert p.store.verify("root")["ok"] is True
        assert p.store.verify("alt")["ok"] is True
        assert len(p.store.episodes("alt")) > len(p.store.episodes("root"))
    finally:
        p.close()
        producer.close()
