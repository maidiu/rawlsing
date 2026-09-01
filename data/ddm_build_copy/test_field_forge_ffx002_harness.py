from __future__ import annotations
import copy,json
from pathlib import Path
import pytest
import field_forge_ffx002_harness as h

def inputs(ids=("u3","u1","u2","u4")):
    return h.holdout_inputs(ids,"seed-v1",2500,"synthetic-code@1",{"float":"exact"})

def source():
    hi=h.hash_payload(inputs())
    return {
      "manifest_schema_version":h.SCHEMA_VERSION,"current_execution_sha":"a"*40,
      "observation_substrate_ref":"obs@1#abc","respondent_entity_binding_ref":"respondent@1#abc",
      "exposure_risk_set_ref":"risk@1#abc","source_scope_ref":"scope@1#abc",
      "source_native_measurement_refs":[{"id":"m2"},{"id":"m1"}],
      "qimpl_measurement_binding_refs":[{"id":"q2"},{"id":"q1"}],
      "response_state_semantics_ref":"response@1#abc","special_state_semantics_ref":"special@1#abc",
      "ttar_execution_sequence":[{"id":"t1"},{"id":"t2"}],
      "post_transform_state_manifest":{"ref":"state@1#abc"},"claim_scope_ref":"claim@1#abc",
      "estimand_ref":"estimand@1#abc","weight_design_refs":"NONE",
      "analytic_role_authority_refs":[{"id":"role2"},{"id":"role1"}],
      "ancestry_disjointness_receipt":{"ref":"ancestry@1#abc"},
      "unresolved_noncomparable_manifest":{"ref":"noncomp@1#abc"},
      "source_native_ancestry_ref":"source-ancestry@1#abc","loss_profile":{"ref":"loss@1#abc"},
      "holdout_generation_inputs_hash":hi
    }

def frozen():
    m=h.compile_common_manifest(source())
    ho=h.freeze_holdout(m,inputs())
    qs=h.freeze_queries(m,ho,[
      {"query_id":"Q05","views_permitted":"B;F","abstention_rule":"ABSTAIN_IF_NOT_REPRESENTED"},
      {"query_id":"Q01","views_permitted":"A;B;C","abstention_rule":"ABSTAIN_IF_OUTSIDE_SUPPORT"}])
    return m,ho,qs

def test_canonicalization_set_arrays_but_not_semantic_arrays():
    a=source();b=copy.deepcopy(a)
    b["source_native_measurement_refs"].reverse();b["analytic_role_authority_refs"].reverse()
    assert h.compile_common_manifest(a)["manifest_hash"]==h.compile_common_manifest(b)["manifest_hash"]
    c=copy.deepcopy(a);c["ttar_execution_sequence"].reverse()
    assert h.compile_common_manifest(a)["manifest_hash"]!=h.compile_common_manifest(c)["manifest_hash"]

def test_authority_must_be_consumed_never_minted():
    a=source();a["claim_scope_ref"]="<REF>"
    with pytest.raises(h.HarnessViolation) as e:h.compile_common_manifest(a)
    assert e.value.state=="COMMON_INPUT_UNRESOLVED_AUTHORITY"

def test_independent_attestation_and_self_rehashed_tamper_rejected():
    m=h.compile_common_manifest(source())
    assert all(h.attest_arm(a,m)["attestation_status"]=="ATTESTED_EQUAL" for a in h.CORE)
    t=copy.deepcopy(m);t["estimand_ref"]="different@1";t["manifest_hash"]=h.compute_common_hash(t)
    with pytest.raises(h.HarnessViolation) as e:h.reject_fork_semantic_tamper(m,t,"B")
    assert e.value.state=="EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE"

def test_holdout_and_query_freezes_are_deterministic():
    m=h.compile_common_manifest(source())
    ho1=h.freeze_holdout(m,inputs(("u1","u2","u3","u4")))
    ho2=h.freeze_holdout(m,inputs(("u4","u3","u2","u1")))
    assert ho1==ho2
    q1=h.freeze_queries(m,ho1,[{"query_id":"Q02","views_permitted":"A"},{"query_id":"Q01","views_permitted":"C"}])
    q2=h.freeze_queries(m,ho1,[{"query_id":"Q01","views_permitted":"C"},{"query_id":"Q02","views_permitted":"A"}])
    assert q1==q2

def test_dispatch_rejects_forbidden_postfork_transform():
    m,ho,qs=frozen()
    bad={"preprocessing_functions":[{"function_id":"semantic-recode","classification":"FORBIDDEN_UNDECLARED_SEMANTIC_TRANSFORM"}]}
    with pytest.raises(h.HarnessViolation) as e:h.dispatch("A",m,ho,qs,bad)
    assert e.value.state=="EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE"

def test_dispatch_loss_replay_result_envelopes_bind_exact_hashes():
    m,ho,qs=frozen();method={"preprocessing_functions":[{"function_id":"view-index","classification":"IDENTITY_PRESERVING_METHOD"}]}
    d=h.dispatch("C",m,ho,qs,method)
    loss=h.loss_receipt("C",[{"invariant_id":"INV001","loss_status":"PRESERVED","materiality":"CRITICAL"}])
    outputs={"query_results":"b"*64}
    replay=h.replay_receipt("C",d["common_manifest_hash"],d["method_manifest_hash"],"synthetic-arm@1",
      d["holdout_manifest_hash"],d["query_manifest_hash"],[],loss["loss_receipt_hash"],outputs,[{"op":"sort"}])
    r=h.result(d,"SYNTHETIC_PASS",outputs,loss,replay)
    assert r["arm_id"]=="C" and len(r["result_hash"])==64

def test_hostile_plan_requires_external_common_variant_binding():
    m,_,_=frozen()
    p=h.hostile_plan(m,[{"perturbation_id":"R2F004","views_attacked":"ALL",
      "semantic_input_handling":"NEW_COMMON_INPUT_VARIANT","failure_state":"typed"}],h.CORE)
    assert p["cases"][0]["framework_status"]=="BLOCKED__EXTERNAL_COMMON_VARIANT_BINDING_REQUIRED"
    assert p["cases"][0]["bound_common_manifest_hash"] is None

def test_query_abstention_and_core_ablation_packages():
    m,_,qs=frozen();p=h.query_plan(qs,h.CORE)
    q05={x["arm_id"]:x["framework_disposition"] for x in p["dispatch_rows"] if x["query_id"]=="Q05"}
    assert q05=={"A":"DOES_NOT_REPRESENT","B":"DISPATCH_QUERY","C":"DOES_NOT_REPRESENT"}
    a=h.ablation_plan(m["manifest_hash"],qs["query_manifest_hash"],h.CORE)
    assert [x["package_id"] for x in a["packages"]]==["C","A+C","B+C","A+B+C"]
    assert a["execution_status"]=="FRAMEWORK_ONLY__NO_EMPIRICAL_RESULTS"

def test_schema_is_machine_readable_and_exact():
    s=json.loads(Path(__file__).with_name("COMMON_SEMANTIC_INPUT_MANIFEST.schema.json").read_text())
    assert s["$schema"]=="https://json-schema.org/draft/2020-12/schema"
    assert s["additionalProperties"] is False
    assert set(s["required"])==set(h.REQUIRED)
    canon=s["properties"]["canonicalization_spec"]["properties"]
    assert canon["set_array_paths"]["const"]==h.CANON["set_array_paths"]
