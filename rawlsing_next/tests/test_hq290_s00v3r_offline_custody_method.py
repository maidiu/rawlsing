"""PYAT HQ290 S00V3R independent OFFLINE-CUSTODY method court @1.

Source-free, local unauthenticated, NOT a real survey issuer.
Frozen oracles: WORKER_RETURNS/PYAT-R3-HQ290-S00V3R-OFFLINE-CUSTODY-METHOD-R1/
               01_FROZEN_OFFLINE_ORACLES.json.
This test MUST run in a fresh isolated Python process, not in the Browser reviewer.
Never alter accepted I01R, S00C or S00CR tests to make this pass.

Required separately attested selector (DO NOT derive from candidate):
    PYAT_S00V3R_COMPOSITE_ROOT=<absolute assembled I01R + candidate seam tree>
    PYAT_S00V3R_SELECTOR=<absolute selector JSON>
    PYAT_S00V3R_SELECTOR_SHA256=<64hex digest supplied by independent executor>
Selector:
{
 "schema": "PYAT_HQ290_S00V3R_TEST_SELECTOR@1",
 "candidate_commit": "<external exact new candidate 40-hex>",
 "reviewed_root_kind": "ISOLATED_COMPOSITE_I01R_PLUS_SEAM",
 "source_sha256": {
    "rawlsing_next/r3_s02_seam_witness.py": "<attested candidate 64hex>",
    "rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py": "<attested accepted-I01R 64hex>",
    "rawlsing_next/pre553_selected_world_progressive_contract.py": "6608ffe1c19e7ec889541cfe4f6f50fda7ab21a1871d42b19b92e1742875a0e3",
    "rawlsing_next/pre553_n9_n10w_progressive_candidate.py": "78f85aea938e9a087167af2938ab11aabbf5a731e852194f021918cf21044c8d"
 }
}
Separate attestation of selector and exact Git source remains mandatory;
a locally recomputed selector digest is NOT an independent attestation.
Expected against baseline S00V2: producer-disabled serve FAILS.
"""
from __future__ import annotations

import copy
from dataclasses import replace
from fractions import Fraction
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ARTIFACT = "a5d1146a5bc0182a0232b1f59dda9ea78a35b4c42096c2fc938fc0cd8ebd7606"
RELEASE = "582317a6731c43d84959f7d0e74604f30bba4d49f3fe114f1afb07f63108d22a"
P04_PINS = {
    "rawlsing_next/pre553_selected_world_progressive_contract.py": "6608ffe1c19e7ec889541cfe4f6f50fda7ab21a1871d42b19b92e1742875a0e3",
    "rawlsing_next/pre553_n9_n10w_progressive_candidate.py": "78f85aea938e9a087167af2938ab11aabbf5a731e852194f021918cf21044c8d",
}
P04 = ("P_Y_given_A", "P_Y_given_A_B", "P_Y_given_A_B_C")


@pytest.fixture(scope="session")
def court():
    root_txt = os.environ.get("PYAT_S00V3R_COMPOSITE_ROOT")
    selector_txt = os.environ.get("PYAT_S00V3R_SELECTOR")
    expected_digest = os.environ.get("PYAT_S00V3R_SELECTOR_SHA256")
    if not root_txt or not selector_txt or not expected_digest:
        pytest.fail("RESOURCE_GATE: explicit composite root, attested selector and independent selector SHA256 required")
    root = Path(root_txt).resolve(strict=True)
    selector_path = Path(selector_txt).resolve(strict=True)
    raw = selector_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected_digest, "SELECTOR_ATTESTATION_MISMATCH"
    selector = json.loads(raw)
    assert selector["schema"] == "PYAT_HQ290_S00V3R_TEST_SELECTOR@1"
    assert selector["reviewed_root_kind"] == "ISOLATED_COMPOSITE_I01R_PLUS_SEAM"
    commit = selector["candidate_commit"]
    assert len(commit) == 40 and all(c in "0123456789abcdef" for c in commit)
    identities = selector["source_sha256"]
    required = set(P04_PINS) | {
        "rawlsing_next/r3_s02_seam_witness.py",
        "rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py",
    }
    assert set(identities) == required
    for rel, digest in identities.items():
        assert len(digest) == 64 and all(c in "0123456789abcdef" for c in digest)
        assert hashlib.sha256((root / rel).read_bytes()).hexdigest() == digest, rel
    for rel, pinned in P04_PINS.items():
        assert identities[rel] == pinned, "P04 code pin must precede candidate"
    sys.path.insert(0, str(root))
    pkg = importlib.import_module("rawlsing_next")
    assert root == Path(pkg.__file__).resolve().parents[1] or (
        root / "rawlsing_next" in list(map(Path, pkg.__path__))
    ), "IMPORTED_WRONG_PACKAGE_ROOT"
    I = importlib.import_module("rawlsing_next.pre553_i01_sourcefree_world_lifecycle_candidate")
    S = importlib.import_module("rawlsing_next.r3_s02_seam_witness")
    assert Path(I.__file__).resolve() == root / "rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py"
    assert Path(S.__file__).resolve() == root / "rawlsing_next/r3_s02_seam_witness.py"
    return root, I, S, selector


def _deny_all_p04(monkeypatch, I):
    def forbidden(*args, **kwargs):
        raise AssertionError("PRODUCER_REEXECUTION_ON_DURABLE_SERVE")
    # All producer entrypoints must be idle after a saved admission.
    for module, names in (
        (I.selected, ("select_world", "run_selected_world_progressive_chain")),
        (I.progressive, ("build_synthetic_world", "run_progressive_chain")),
        (I.seam, ("build_sociological_bundle", "build_source_free_native_joint_bundle",
                  "build_synthetic_world", "run_progressive_chain", "select_world")),
    ):
        for name in names:
            monkeypatch.setattr(module, name, forbidden)
    return forbidden


def _result(I, b, scenario="S00V3R_SOURCEFREE"):
    consumer = I.seam.ContractOnlySeamConsumer(b)
    r = consumer.compute_scenario(scenario, list(P04) if b.world_scope.get("target") is None
                                  else ["P_Q86A_given_Q86B_1"])
    return r, consumer.get_receipt()


def _rehash(S, b, **kw):
    v = replace(b, content_hash="", **kw)
    return replace(v, content_hash=S._content_hash(v.as_dict()))


def test_O01_O03_exact_admission_complete_oracle_and_saved_bytes(court, tmp_path):
    _, I, S, _ = court
    product, report = I.build_product(tmp_path)
    saved = I.artifact_path(tmp_path, product.subject_ref)
    raw = saved.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ARTIFACT
    assert product.subject_ref.content_hash == ARTIFACT
    assert product.release.ref.content_hash == RELEASE
    assert report["batch_state"] == "COMPLETED"
    ref, payload, completed = I.admit_saved_world(product.session)
    assert ref == product.subject_ref
    assert completed.state == "COMPLETED"
    assert completed.result_refs == (ref,)
    assert payload["schema"] == "I01_SOURCEFREE_SAVED_WORLD@1"
    assert payload["security_mode"] == "LOCAL_UNAUTHENTICATED"
    assert payload["producer_contract_ref"] == I.PRODUCER.as_dict()
    assert payload["bundle"]["replay"]["source_permission"] == "SOURCE_FREE_ONLY"
    assert payload["selected_contract"]["real_current"] is False
    assert len(payload["bundle"]["channels"]) == 6
    result = I.serve(product)
    trace = result["numeric_result"]["progressive_trace"]
    assert [(t["raw_denominator_support"],t["raw_numerators"]["1"],
             t["raw_numerators"]["0"],t["exact_probabilities"]["1"]["$exact_fraction"])
            for t in trace] == [(32,18,14,[9,16]),(16,10,6,[5,8]),(8,6,2,[3,4])]
    assert len(result["consumer_receipt"]["values_read"]) == 6
    assert all(v["semantic_effect"]=="VALUE_USED_IN_EXACT_CONDITIONAL"
               for v in result["consumer_receipt"]["values_read"])


def test_O02_exact_saved_producer_disabled_service(court, tmp_path, monkeypatch):
    _, I, _, _ = court
    product, _ = I.build_product(tmp_path)
    expected = I.serve(product)
    payload = I.load_artifact(tmp_path, product.subject_ref)
    _deny_all_p04(monkeypatch, I)
    consumer_type = I.seam.ContractOnlySeamConsumer
    seen = []
    def spy(bundle):
        seen.append(bundle.as_dict())
        return consumer_type(bundle)
    monkeypatch.setattr(I.seam, "ContractOnlySeamConsumer", spy)
    assert I.serve(product) == expected
    assert seen == [payload["bundle"]]
    assert len(product.calls) == 1


def test_O04_corrupted_saved_bytes_refuse_without_regeneration(court, tmp_path, monkeypatch):
    _, I, _, _ = court
    product, _ = I.build_product(tmp_path)
    path = I.artifact_path(tmp_path, product.subject_ref)
    original = path.read_bytes()
    path.write_bytes(original[:-1] + (b"x" if original[-1:] != b"x" else b"y"))
    _deny_all_p04(monkeypatch, I)
    with pytest.raises(I.I01Error, match="SAVED_WORLD_BYTES_MISMATCH"):
        I.serve(product)


def test_O05_coherently_rehashed_artifact_cannot_replace_committed_receipt(court, tmp_path, monkeypatch):
    _, I, _, _ = court
    product, _ = I.build_product(tmp_path)
    altered = copy.deepcopy(I.load_artifact(tmp_path, product.subject_ref))
    altered["bundle"]["world_scope"]["unrelated_test_note"] = "locally rewritten"
    ref = I.local_ref("I01SourceFreeSavedWorld", altered)
    I.save_json(tmp_path / "artifacts" / (ref.content_hash + ".json"), altered)
    product.subject_ref = ref
    _deny_all_p04(monkeypatch, I)
    with pytest.raises(I.I01Error):
        I.serve(product)


def test_O06_durable_result_receipt_is_not_caller_replaceable(court, tmp_path):
    _, I, _, _ = court
    product, _ = I.build_product(tmp_path)
    checkpoint = tmp_path / "b01e_checkpoint.json"
    data = json.loads(checkpoint.read_text())
    assert data["records"][0]["receipt_projection"]["state"] == "COMPLETED"
    data["records"][0]["receipt_projection"]["result_refs"][0]["content_hash"] = "0" * 64
    checkpoint.write_text(json.dumps(data))
    try:
        I.restore_product(tmp_path)
    except Exception as exc:
        assert type(exc).__name__ in {
            "CheckpointTornError", "I01Error", "BatchCheckpointError",
            "BatchIntegrationError", "CheckpointIntegrityError",
        }, f"untyped durable failure: {type(exc).__name__}: {exc}"
    else:
        pytest.fail("DURABLE_RECEIPT_SUBSTITUTION_WAS_ACCEPTED")


def test_O07_complete_local_rehash_with_stale_p04_root(court, monkeypatch):
    _, I, S, _ = court
    b = S.build_sociological_bundle()
    channels = []
    for ch in b.channels:
        if ch.value["step_id"] == "P_Y_given_A":
            cell = ch.value["cell"]
            numerator = 15 if cell == "0" else 17
            v = dict(ch.value)
            f = Fraction(numerator, 32)
            v["raw_numerator_support"] = numerator
            v["raw_probability_exact_fraction"] = {"$exact_fraction": [f.numerator,f.denominator]}
            channels.append(replace(ch, value=v))
        else:
            channels.append(ch)
    steps = copy.deepcopy(list(b.steps))
    for st in steps:
        if st["step_id"] == "P_Y_given_A":
            for cell, count in (("0",15),("1",17)):
                f = Fraction(count,32)
                st["cells"][cell] = {"numerator":count,
                                     "fraction":{"$exact_fraction":[f.numerator,f.denominator]}}
    forged = _rehash(S,b,channels=tuple(channels),steps=tuple(steps))
    c = S.ContractOnlySeamConsumer(forged)
    assert c._validate_complete_domain() is None
    assert c._validate_fraction_closure() is None
    assert c._validate_step_geometry() is None
    _deny_all_p04(monkeypatch,I)
    r, receipt = _result(I,forged)
    assert r["status"] == "REFUSED"
    assert r["reason"] in {
        "PRODUCER_VALUE_IDENTITY_MISMATCH", "SAVED_PRODUCER_CUSTODY_MISMATCH",
        "PINNED_PRODUCER_ORACLE_MISMATCH", "OFFLINE_PRODUCER_IDENTITY_MISMATCH",
    }
    assert not [v for v in receipt.values_read if v.semantic_effect=="VALUE_USED_IN_EXACT_CONDITIONAL"]


def test_O08_fresh_native_sourcefree_law_has_genuinely_new_roots(court):
    _, I, S, _ = court
    a = S.build_source_free_native_joint_bundle({
        (0,0):3,(0,1):1,(1,0):1,(1,1):3
    })
    b = S.build_source_free_native_joint_bundle({
        (0,0):3,(0,1):1,(1,0):2,(1,1):2
    })
    for key in ("source_universe_ref", "release_ref", "risk_set_ref"):
        assert getattr(a.selected_world_contract,key) != getattr(b.selected_world_contract,key)
    x, xr = _result(I,a)
    y, yr = _result(I,b)
    assert x["status"] == y["status"] == "COMPUTED"
    assert x["exact_probabilities"]["1"] == {"$exact_fraction":[3,4]}
    assert y["exact_probabilities"]["1"] == {"$exact_fraction":[1,2]}
    assert y["scientific_claim_grade"] == "SOURCE_FREE_SYNTHETIC"
    assert len([v for v in yr.values_read if v.semantic_effect=="VALUE_USED_IN_EXACT_CONDITIONAL"]) == 2


@pytest.mark.parametrize("attack", ["missing_channel","duplicate_channel","missing_step","missing_fraction",
                                     "stale_fraction","extra_cell","false_scope"])
def test_O09_malformed_or_incomplete_never_compute(court, attack):
    _, I, S, _ = court
    b = S.build_source_free_native_joint_bundle({(0,0):3,(0,1):1,(1,0):1,(1,1):3})
    if attack=="missing_channel": b=_rehash(S,b,channels=b.channels[:-1])
    if attack=="duplicate_channel": b=_rehash(S,b,channels=b.channels+(b.channels[0],))
    if attack=="missing_step": b=_rehash(S,b,steps=b.steps[:-1])
    if attack in ("missing_fraction","stale_fraction"):
        ch=b.channels[-1]; v=dict(ch.value)
        if attack=="missing_fraction":v.pop("raw_probability_exact_fraction")
        else:v["raw_probability_exact_fraction"]={"$exact_fraction":[100,101]}
        b=_rehash(S,b,channels=b.channels[:-1]+(replace(ch,value=v),))
    if attack=="extra_cell":
        st=copy.deepcopy(list(b.steps));st[-1]["cells"]["9"]={"numerator":0}
        b=_rehash(S,b,steps=tuple(st))
    if attack=="false_scope":
        b=_rehash(S,b,world_scope={**b.world_scope,"qualified_real_source_value_read":True})
    r,receipt=_result(I,b)
    assert r["status"] != "COMPUTED"
    assert not [v for v in receipt.values_read if v.semantic_effect=="VALUE_USED_IN_EXACT_CONDITIONAL"]


def _run_cold(root, working, *, invalidate=False):
    script = """
import json,sys
from pathlib import Path
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
p, report=I.build_product(Path(sys.argv[1]))
assert p.calls == [], 'DUPLICATE_DURABLE_CALLBACK'
assert report['executed'] == [], 'REEXECUTED_COMMITTED_JOB'
def forbid(*args,**kwargs): raise AssertionError('PRODUCER_CALLED_ON_COLD_SERVE')
for mod,names in ((I.selected,('select_world','run_selected_world_progressive_chain')),
                  (I.progressive,('build_synthetic_world','run_progressive_chain')),
                  (I.seam,('build_sociological_bundle','build_source_free_native_joint_bundle',
                           'build_synthetic_world','run_progressive_chain','select_world'))):
    for name in names:setattr(mod,name,forbid)
if sys.argv[2]=='invalidate':
    try:I.serve(p)
    except I.I01Error as exc:assert 'NO_CURRENT' in str(exc)
    else:raise AssertionError('CURRENT_RESURRECTED')
    result=I.serve(p,historical=True)
else:
    result=I.serve(p)
print(json.dumps(result,sort_keys=True))
"""
    env=os.environ.copy()
    env["PYTHONPATH"]=str(root)+os.pathsep+env.get("PYTHONPATH","")
    proc=subprocess.run([sys.executable,"-c",script,str(working),"invalidate" if invalidate else "current"],
                        cwd=str(root),env=env,capture_output=True,text=True)
    assert proc.returncode==0, proc.stderr
    return json.loads(proc.stdout)


def test_O10_cold_restart_has_zero_durable_producer_execution(court,tmp_path):
    root,I,_,_=court
    p,_=I.build_product(tmp_path)
    expected=I.serve(p)
    observed=_run_cold(root,tmp_path)
    assert observed["numeric_result"]==expected["numeric_result"]
    assert observed["consumer_receipt"]==expected["consumer_receipt"]
    assert observed["producer_subject_ref"]==expected["producer_subject_ref"]
    assert observed["durable_receipt_ref"]==expected["durable_receipt_ref"]


def test_O11_O12_invalidation_no_current_and_exact_historical_asof(court,tmp_path):
    root,I,_,_=court
    p,_=I.build_product(tmp_path)
    before=I.serve(p)
    I.invalidate(p)
    with pytest.raises(I.I01Error,match="NO_CURRENT"):
        I.serve(p)
    after=_run_cold(root,tmp_path,invalidate=True)
    assert after["historical"] is True
    assert after["numeric_result"]==before["numeric_result"]
    assert after["consumer_receipt"]==before["consumer_receipt"]
    assert after["producer_subject_ref"]==before["producer_subject_ref"]


def test_O13_external_original_source_and_issuer_remain_refused(court,tmp_path):
    _,I,S,_=court
    with pytest.raises(S.SeamContractError,match="SOURCE_VALUE_UNAVAILABLE"):
        S.build_retained_gt2_bundle(
            issued_source_owned_values={"Q86A":1,"Q86B":1,"coexposure":19210},
            issued_use_authority="CALLER_SUPPLIED_FAKE_ISSUER")
    p,_=I.build_product(tmp_path)
    from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleError
    from rawlsing_next.pre553_learned_product_release import M2ReleaseError
    with pytest.raises(LearnedProductLifecycleError,match="EXTERNAL_ISSUER_HOLD"):
        p.lifecycle.require_external_issuer("PROTECTED_CURRENT")
    with pytest.raises(M2ReleaseError,match="EXTERNAL_ISSUER_HOLD"):
        p.repository.require_external_issuer("PROTECTED_CURRENT")


def test_O14_code_pins_and_candidate_selector_are_held_outside_saved_bundle(court):
    root,I,S,selector=court
    assert selector["source_sha256"]["rawlsing_next/r3_s02_seam_witness.py"] == hashlib.sha256(
        (root/"rawlsing_next/r3_s02_seam_witness.py").read_bytes()).hexdigest()
    assert all(hashlib.sha256((root/rel).read_bytes()).hexdigest()==sha
               for rel,sha in P04_PINS.items())
    assert I.PRODUCER.kind=="ProducerContract"
    assert I.CEILING.kind=="SourceFreeCeiling"
