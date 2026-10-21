"""R30G GM01 material mechanism to real R29P C12/A0/A2 product."""
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
        "from r30g.gm01_product import GM01Product;"
        "p=GM01Product.reopen(sys.argv[1]);"
        "o=p.observe_verified();e=p.store.episodes('root');"
        "print(json.dumps({'status':o.get('status'),"
        "'tools':o['self']['state'].get('tools_remaining'),"
        "'completed':o['self']['state'].get('completed_units'),"
        "'material':o['self']['state'].get('material_remaining'),"
        "'episodes':[x['kind'] for x in e],"
        "'episode_bodies':[x['body'] for x in e],"
        "'other':p.other()['public']['completed_units'],"
        "'verify':p.c12_verify()},sort_keys=True,default=str));p.close()")
    env = dict(os.environ, PYTHONPATH=PYTHONPATH, PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run([sys.executable, "-B", "-c", code, str(root)],
                               cwd=str(ROOT), env=env, capture_output=True,
                               text=True, timeout=240)
    assert completed.returncode == 0, completed.stderr[-2000:]
    return json.loads(completed.stdout.strip().splitlines()[-1])


def test_share_e2_enables_actual_material_outcome(tmp_path):
    from r30g.scenarios import share_e2
    from r30g.runner import build, observable
    from r30g.assertion import p01

    scenario = share_e2()
    product, artifacts, producer = build(tmp_path / "share_e2", scenario["gm01"])
    try:
        observed = observable(product, perform="e2")
        assert p01(observed, scenario["gm01"]) is True, json.dumps(observed, indent=2, default=str)
        assert observed["material_start"]["tools_for_a"] == 1
        assert observed["completed_after"] == 5
        assert observed["a2_other_units"] == 4
        assert "OFFSCREEN_NO_CHANGE" in observed["a2_offscreen"]
        assert observed["c12_verify"]["ok"] is True
    finally:
        product.close()
        producer.close()


def test_refusal_omission_no_effect_and_deny_differ_materially(tmp_path):
    from r30g.scenarios import refuse_e2, share_omit, refuse_omit, share_contrary_omit
    from r30g.runner import build, observable
    from r30g.assertion import p01, share_omit as share_omit_assert, deny_no_material

    cases = [
        (refuse_e2(), "e2", "refuse_e2"),
        (share_omit(), "omit", "share_omit"),
        (refuse_omit(), "omit", "refuse_omit"),
        (share_contrary_omit(), "omit", "contrary_omit"),
    ]
    observed = {}
    for scenario, perform, name in cases:
        product, artifacts, producer = build(tmp_path / name, scenario["gm01"])
        try:
            observed[name] = (observable(product, perform=perform), scenario["gm01"])
        finally:
            product.close()
            producer.close()
    assert p01(*observed["refuse_e2"]) is False
    assert deny_no_material(observed["refuse_e2"][0]) is True
    assert p01(*observed["share_omit"]) is False
    assert share_omit_assert(observed["share_omit"][0]) is True
    assert p01(*observed["refuse_omit"]) is False
    assert observed["refuse_omit"][0]["a2_other_units"] == 4
    assert p01(*observed["contrary_omit"]) is False
    assert observed["contrary_omit"][1]["status"] == "UNCERTAIN_CONTRADICTORY_PROJECTS"
    assert observed["contrary_omit"][0]["action"]["status"] == "NO_CHANGE"


def test_b_source_cut_and_restore_at_real_product(tmp_path):
    from r30g.scenarios import share_e2, refuse_e2
    from r30g.runner import build, observable
    from r30g.assertion import p01

    good = share_e2()
    product, artifacts, producer = build(tmp_path / "good", good["gm01"])
    try:
        assert p01(observable(product, perform="e2"), good["gm01"]) is True
    finally:
        product.close()
        producer.close()

    bad = refuse_e2()
    product, artifacts, producer = build(tmp_path / "bad", bad["gm01"])
    try:
        assert p01(observable(product, perform="e2"), bad["gm01"]) is False
    finally:
        product.close()
        producer.close()

    restored = share_e2()
    product, artifacts, producer = build(tmp_path / "restored", restored["gm01"])
    try:
        assert p01(observable(product, perform="e2"), restored["gm01"]) is True
    finally:
        product.close()
        producer.close()


def test_gm01_c12_cold_reopen_preserves_material_state(tmp_path):
    from r30g.scenarios import share_e2
    from r30g.runner import build, observable

    scenario = share_e2()
    product, artifacts, producer = build(tmp_path / "cold", scenario["gm01"])
    try:
        warm = observable(product, perform="e2")
        assert warm["tools_after"] == 0 and warm["completed_after"] == 5
    finally:
        product.close()
        producer.close()
    cold = _cold(tmp_path / "cold" / "product")
    assert cold["status"] == "OK"
    assert cold["tools"] == 0
    assert cold["completed"] == 5
    assert cold["material"] == 3
    assert "DO" in cold["episodes"]
    assert cold["verify"]["ok"] is True
    assert any(body.get("action") == "material_inspect"
               and body.get("gm01_receipt_hash") == scenario["gm01"]["result_hash"]
               for body in cold["episode_bodies"])


def test_gm01_real_bp2_ports_are_separate_test_only_and_no_grant():
    import bp2_joined.bootstrap as bootstrap
    from bp2_joined import ports
    from generative_resource import bp2_test_only_resources, candidate_resource
    from r30g.scenarios import A

    bootstrap.install()
    before = ports.production_registries()
    obj = bp2_test_only_resources(ports, candidate_resource(), A, 10)
    assert obj["rule_a"].test_only is True
    assert obj["rule_t"].test_only is True
    assert obj["grant"] is None
    assert obj["native_issuer"] is None
    assert obj["actual_target_mutations"] == 0
    assert obj["production_registry_writes"] == 0
    assert obj["rule_a"].issuer_ref != obj["rule_t"].issuer_ref
    assert obj["rule_t"].body["rule_semantics"]["allowed_operations"] == ["NO_CHANGE"]
    after = ports.production_registries()
    assert before["response_rule_count"] == after["response_rule_count"] == 0
    assert before["target_rule_count"] == after["target_rule_count"] == 0


def test_no_psyche_or_role_label_effect():
    import copy
    from generative_resource import candidate_resource, evaluate
    from r30g.scenarios import case

    baseline = evaluate(case(share=True, e2=True), candidate_resource())
    for role, label in (("other_job", "CLASS_B"), ("unemployed", "ENNEAGRAM_4")):
        changed = copy.deepcopy(case(share=True, e2=True))
        changed["social_role"] = role
        changed["demographic_label"] = label
        assert evaluate(changed, candidate_resource()) == baseline
    assert baseline["psyche_delta"] == {}
    assert baseline["v3ms_created"] == 0
    assert baseline["rule_t_result"] == "NO_CHANGE"
    assert baseline["rule_t_grant"] is None


def test_forged_and_revoked_gm01_inputs_deny_without_product_action(tmp_path):
    from r30g.scenarios import forged_e2, evaluated
    from r30g.runner import build, observable
    from r30g.assertion import p01

    forged = forged_e2()
    assert forged["gm01"]["status"] == "DENY_E2_NOT_LATER"
    product, artifacts, producer = build(tmp_path / "forged", forged["gm01"])
    try:
        observed = observable(product, perform="e2")
        assert p01(observed, forged["gm01"]) is False
        assert observed["action"]["status"] == "DENY"
    finally:
        product.close()
        producer.close()

    revoked = evaluated(share=True, e2=True)
    revoked["gm01"] = dict(revoked["gm01"])
    revoked["gm01"]["status"] = "DENY_REVOKED"
    revoked["gm01"]["material_feasible_after"] = None
    product, artifacts, producer = build(tmp_path / "revoked", revoked["gm01"])
    try:
        observed = observable(product, perform="e2")
        assert observed["tools_before"] == 0
        assert p01(observed, revoked["gm01"]) is False
    finally:
        product.close()
        producer.close()


def test_actor_private_source_and_typed_holds_not_exposed(tmp_path):
    from generative_resource import candidate_resource
    from r30g.scenarios import share_e2
    from r30g.runner import build, observable

    scenario = share_e2()
    b_event = next(r for r in scenario["case"]["records"]
                   if r["kind"] == "OTHER_PERFORMED")
    assert b_event["subject"] == scenario["case"]["other"]
    assert b_event["payload"]["operation"] == "SHARE_TOOL"
    resource = candidate_resource()
    assert resource["actual_source_permission"] == "NOT_GRANTED"
    assert resource["native_grant"] is None and resource["source_grant"] is None

    product, artifacts, producer = build(tmp_path / "privacy", scenario["gm01"])
    try:
        observed = observable(product, perform="e2")
        other = product.other()
        assert other["private_fields_hidden"] == [
            "cash", "material_remaining", "free_hours", "debt_units"]
        assert observed["others"] == ["B"]
        assert "cash" not in json.dumps(observed["claims"])
    finally:
        product.close()
        producer.close()
