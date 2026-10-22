"""R29P generated actor history -> cold C12 -> real A0/A2 product tests."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT,
    ROOT / "candidate",
    ROOT / "candidate" / "vendor" / "bp2",
    ROOT / "candidate" / "vendor" / "bp4",
    ROOT / "r26e",
    ROOT / "n1",
]
PYTHONPATH = os.pathsep.join(str(path) for path in PATHS)


def _cold(root: Path, branch: str = "root") -> dict:
    code = (
        "import json,sys;"
        "from r29p.product import R29PProduct;"
        "p=R29PProduct.reopen(sys.argv[1], branch_id=sys.argv[2]);"
        "obs=p.observe_verified();"
        "eps=p.store.episodes(p.branch_id);"
        "out={'status':obs.get('status'),'code':obs.get('code',''),"
        "'claims':[c['kind'] for c in obs.get('claims',[])],"
        "'others':[o['actor'] for o in obs.get('others_present',[])],"
        "'tools':obs.get('self',{}).get('state',{}).get('tools_remaining'),"
        "'history':obs.get('self',{}).get('history_hash'),"
        "'episodes':[e['kind'] for e in eps],"
        "'b_episodes':[e['kind'] for e in eps if e['actor_id']=='B'],"
        "'verify':p.c12_verify(),"
        "'other_units':p.other()['public']['completed_units']};"
        "p.close();print(json.dumps(out,sort_keys=True))"
    )
    env = dict(os.environ, PYTHONPATH=PYTHONPATH, PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, "-B", "-c", code, str(root), branch],
        cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=240)
    assert completed.returncode == 0, completed.stderr[-2000:]
    return json.loads(completed.stdout.strip().splitlines()[-1])


def test_baseline_reaches_persisted_cold_c12_and_a0_a2(tmp_path):
    from bp4.store import C12Store
    from r29p.runner import build_bundle, observable

    product, artifacts, producer = build_bundle(tmp_path / "baseline")
    try:
        observed = observable(product)
        assert observed["status"] == "OK"
        assert observed["claims"] == ["ARRIVAL"]
        assert observed["others"] == ["B"]
        assert observed["tools"] == 1
        assert observed["a2_clock"] == 40
        assert observed["a2_other_units"] == 5
        assert "OFFSCREEN_REPAIR" in observed["a2_offscreen"]
        verify = product.c12_verify()
        assert verify["ok"] is True, verify
        assert verify["counts"]["episode"] >= 1
        assert verify["counts"]["world_event"] >= 2
        assert verify["counts"]["checkpoint"] >= 2
        path = product.store.path
        assert C12Store(path).verify("root")["ok"] is False
    finally:
        product.close()
        producer.close()
    cold = _cold(tmp_path / "baseline" / "product")
    assert cold["status"] == "OK"
    assert "ARRIVAL" in cold["claims"]
    assert cold["tools"] == 1
    assert cold["other_units"] == 5
    assert cold["verify"]["ok"] is True
    assert cold["verify"]["counts"]["episode"] >= 1


def test_m6_actor_only_knowledge_after_independent_b_offscreen(tmp_path):
    from r29p.runner import run_m6

    result = run_m6(tmp_path / "m6")
    before = [row[0] for row in result["before_claims"]]
    after = [row[0] for row in result["after_claims"]]
    assert "OFFSCREEN_REPAIR" not in before
    assert "OFFSCREEN_REPAIR" in after
    permissions = {row[0]: row[2] for row in result["after_claims"]}
    assert permissions["OFFSCREEN_REPAIR"] == "PERMIT_FIRST_PERSON_KNOWLEDGE"
    assert "OFFSCREEN" in result["b_episodes"]
    assert result["verify"]["ok"] is True
    cold = _cold(tmp_path / "m6" / "product")
    assert "OFFSCREEN_REPAIR" in cold["claims"]
    assert "OFFSCREEN" in cold["b_episodes"]
    assert cold["verify"]["ok"] is True


def test_fork_retains_shared_past_and_independent_post_fork_history(tmp_path):
    from r29p.runner import run_fork

    result = run_fork(tmp_path / "fork")
    assert result["shared_before"]["equal"] is True
    assert result["shared_after"]["equal"] is True
    assert result["alt_say"]["status"] == "OK"
    assert result["root_verify"]["ok"] is True
    assert result["alt_verify"]["ok"] is True
    assert result["alt_verify"]["counts"]["episode"] > result["root_verify"]["counts"]["episode"]
    root_cold = _cold(tmp_path / "fork" / "product", "root")
    alt_cold = _cold(tmp_path / "fork" / "product", "alt")
    assert root_cold["verify"]["ok"] is True
    assert alt_cold["verify"]["ok"] is True
    assert len(alt_cold["episodes"]) > len(root_cold["episodes"])
    assert root_cold["episodes"] != alt_cold["episodes"]


def test_seven_same_observable_faults_prove_and_restore(tmp_path):
    from r29p.faults import seven_trials

    result = seven_trials(tmp_path / "faults")
    assert result["all_proved"] is True, json.dumps(result, indent=2, default=str)
    assert len(result["trials"]) == 7
    assert {row["edge"] for row in result["trials"]} == {
        "A_GENESIS_HISTORY",
        "A_PERFORMED_OMISSION",
        "B_INDEPENDENT_ACTION",
        "ADP010_ENCOUNTER_CONTACT",
        "C8_E1_PROOF",
        "CAN008_CAN011_TARGET",
        "LATER_E2",
    }
    for row in result["trials"]:
        assert row["baseline_pass"] is True
        assert row["fault_changed_or_refused"] is True
        assert row["restored_pass"] is True
        assert row["stable_restore"] is True


def test_no_global_builder_mutation_and_two_isolates(tmp_path):
    import bp2_joined.producer as P
    from r29p.runner import build_bundle

    original = P.build_two_actor_life
    a, a_artifacts, a_producer = build_bundle(tmp_path / "a")
    try:
        b, b_artifacts, b_producer = build_bundle(
            tmp_path / "b", variant="B_RESOURCE_RICH")
        try:
            assert P.build_two_actor_life is original
            assert a_artifacts.life.a_source.source_hash != b_artifacts.life.a_source.source_hash
            assert a_producer.env.key_path != b_producer.env.key_path
            assert a_artifacts.target_id != b_artifacts.target_id
            assert a.store.path != b.store.path
        finally:
            b.close()
            b_producer.close()
    finally:
        a.close()
        a_producer.close()


def test_n1_screen_and_empty_native_registries(tmp_path):
    import bp2_joined.ports as ports
    from n1_eligibility import GRADE, compile_test_only_bp2_resources, screen, seal_record
    from r29p.runner import build_bundle

    A, B = "TEST_ONLY_A", "TEST_ONLY_B"

    def entry(kind, name, time, who=A, owner=None, occurred=True):
        return seal_record(dict(
            kind=kind, ref="TEST_ONLY_" + name, time=time, subject=who,
            owner=owner or "TEST_ONLY_OWNER_" + name, grade=GRADE,
            operation="coordinated_material_inspection", occurred=occurred))

    case = dict(case_id="TEST_ONLY_R29P", actor_id=A, other_actor_id=B,
                operation="coordinated_material_inspection", as_of=50,
                records=[
                    entry("ADP010_OPPORTUNITY", "opp", 1),
                    entry("ACTOR_ENACTED", "first", 2),
                    entry("ACTOR_ENACTED", "second", 4),
                    entry("ADP010_ENCOUNTER", "enc", 6),
                    entry("OTHER_OFFER", "offer", 7, B),
                    entry("ADP019_E1", "e1", 9),
                ])
    assert screen(case)["status"] == "OWNER_REVIEW_CANDIDATE"
    assert screen({**case, "records": [
        r for r in case["records"] if r["kind"] != "ADP019_E1"]})["status"] == "REQUEST_EVIDENCE"
    assert screen({**case, "records": [
        r for r in case["records"] if r["kind"] != "ACTOR_ENACTED"]})["status"] == "NO_CHANGE"
    assert screen({**case, "records": case["records"] + [
        entry("CONTRARY_ACTION", "contrary", 8)]})["status"] == "COMPETING"
    assert screen({**case, "other_actor_id": A})["status"] == "DENY"
    compiled = compile_test_only_bp2_resources(case, ports, now=50)
    assert compiled["grant"] is None
    assert compiled["rule_a"].test_only is True
    assert compiled["rule_t"].test_only is True
    assert compiled["native_registry_mutation"] is False
    assert ports.production_registries()["response_rule_count"] == 0
    assert ports.production_registries()["target_rule_count"] == 0

    product, artifacts, producer = build_bundle(tmp_path / "n1")
    try:
        before = product.store.latest_state("root")
        screen(case)
        compile_test_only_bp2_resources(case, ports, now=50)
        assert product.store.latest_state("root") == before
        assert product.observe_verified()["status"] == "OK"
    finally:
        product.close()
        producer.close()


def test_lawful_no_change_deny_and_h0(tmp_path):
    import historical_actor_producer as H
    from r29p.runner import build_bundle

    h0 = H.build_no_development_record()
    assert h0["performed_actions"] == []
    assert h0["practice_established"] is False
    product, artifacts, producer = build_bundle(tmp_path / "deny")
    try:
        assert product.inspect()["status"] == "NO_CHANGE"
        assert product.travel("market")["status"] == "OK"
        denied_repair = product.repair()
        assert denied_repair["status"] == "DENY"
        assert denied_repair["code"] == "WRONG_LOCATION"
        denied = product.address_other("B, can you hear me?")
        assert denied["status"] == "DENY"
        assert denied["code"] == "OTHER_ACTOR_NOT_PRESENT"
    finally:
        product.close()
        producer.close()


def test_source_manifest_closure():
    import hashlib

    manifest = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    for relative, expected in manifest["vendor_files"].items():
        path = ROOT / "candidate" / "vendor" / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, relative
    for relative, row in manifest["extras"].items():
        path = ROOT / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], relative
    assert manifest["vendor_file_count"] == 150
    assert len(manifest["vendor_files"]) == 150


def test_native_ports_remain_unissued():
    from native_ports import NativeHistoricalActorPorts

    ports = NativeHistoricalActorPorts()
    results = ports.probe_all()
    assert len(results) == len(ports.PORTS)
    assert set(results.values()) == {"NATIVE_AUTHORITY_UNISSUED"}
