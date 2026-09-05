from __future__ import annotations
import builtins, hashlib, inspect, json
import pytest
import rawlsing_next.pre553_repo_native_seal as seal
from rawlsing_next.pre553_empirical_objects import AuthorityRef, EmpiricalFact, EmpiricalQuerySpec, ExactRef, canonical_json


def _h(x): return hashlib.sha256(f"SYNTHETIC_TEST_ONLY::{x}".encode()).hexdigest()
def _r(kind, tag): return ExactRef(kind, f"urn:synthetic-test-only:{tag}", _h(f"r:{kind}:{tag}"))
def _a(tag): return AuthorityRef(f"SYNTHETIC_TEST_ONLY_AUTH_{tag}", "1.0.0", _h(f"a:{tag}"))


def _fixture(query_universes=None, fact_universes=None):
    auth, pred, risk, measure = _a("query"), _r("EmpiricalPredicate@1.0.0", "pred"), _r("RISK_SET", "risk"), _r("MEASURE_BASIS", "raw")
    state, ua, ub = _r("RESPONSE_STATE_SEMANTICS", "state"), _r("EmpiricalUniverse@1.0.0", "ua"), _r("EmpiricalUniverse@1.0.0", "ub")
    qu, fu, target = query_universes or (ua,), fact_universes or (ua,), _r("QUESTION_NATIVE", "target")
    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE", authority_snapshot_refs=(auth,), dependency_refs=(pred,),
        producer_replay_locator_or_reference_root=_r("REPLAY_ROOT", "query"), target_refs=(target,),
        target_arity_and_topology={"arity": 1, "joint_order_semantics": "SEMANTIC_ORDERED", "components": [{"target_ref": target}]},
        condition_predicate_ref=pred, risk_set_ref=risk, empirical_universe_refs=qu, scope_refs=qu, measure_basis_ref=measure,
        requested_output_grain={"source_scope_mode": "SINGLE_UNIVERSE" if len(qu) == 1 else "SOURCE_INDEXED_MULTI_UNIVERSE", "measure_kind": "RAW", "risk_set_type": "WHOLE_QUESTION_RISK_SET", "response_state_semantics_ref": state},
        query_authority_refs=(auth,),
    )
    replay = _r("PRE553_I03_QUERY_REPLAY", "replay")
    provenance = tuple(sorted((_r("C11LogicalRelease", "release"), _r("ReplayManifest", "manifest"), *fu), key=lambda x: x.key))
    risk_members = tuple(sorted((_r("RespondentIdentity", "r1"), _r("RespondentIdentity", "r2"), _r("RespondentIdentity", "r3")), key=lambda x: x.key))
    denom = risk_members[:2]
    fact = EmpiricalFact(
        typed_state="SUPPORTED", authority_snapshot_refs=(auth,),
        dependency_refs=tuple(sorted((query.ref, pred, replay, *provenance), key=lambda x: x.key)),
        producer_replay_locator_or_reference_root=replay, empirical_query_spec_ref=query.ref, empirical_universe_refs=fu,
        target_topology={"arity": 1}, condition_predicate_ref=pred, risk_set_ref=risk,
        raw_numerator_support=1, raw_denominator_support=2, weighted_numerator_support_if_authorized=None,
        weighted_denominator_support_if_authorized=None, measure_basis_ref=measure, response_state_semantics_ref=state,
        uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED", source_empirical_provenance_refs=provenance,
        replay_ref=replay, query_execution_contract_id="SYNTHETIC_TEST_ONLY", risk_set_member_refs=risk_members,
        denominator_member_refs=denom,
    )
    return query, fact


def _doc(q, f): return {"document_schema": seal.DOCUMENT_SCHEMA, "query": q.as_dict(), "fact": f.as_dict()}
def _copy(x): return json.loads(canonical_json(x))
def _reseal(x): return seal._seal_document(x, shard_char_limit=211)


def test_round_trip_returns_ordinary_objects_with_exact_query_fact_replay_identity():
    q, f = _fixture(); payload = seal.seal_query_fact(q, f, shard_char_limit=211); rq, rf = seal.rehydrate_repo_native_query_fact(payload)
    assert isinstance(rq, EmpiricalQuerySpec) and isinstance(rf, EmpiricalFact)
    assert rq.ref == q.ref and rf.ref == f.ref and rq.as_dict() == q.as_dict() and rf.as_dict() == f.as_dict()
    assert rf.producer_replay_locator_or_reference_root == ExactRef(**rf.replay_ref)


def test_source_indexed_query_allows_one_in_scope_fact_universe():
    ua, ub = _r("EmpiricalUniverse@1.0.0", "ma"), _r("EmpiricalUniverse@1.0.0", "mb")
    q, f = _fixture((ua, ub), (ub,)); rq, rf = seal.rehydrate_repo_native_query_fact(seal.seal_query_fact(q, f))
    assert {ExactRef(**x) for x in rf.empirical_universe_refs}.issubset({ExactRef(**x) for x in rq.empirical_universe_refs})


def test_missing_shard_and_reordered_shards_fail():
    p = seal.seal_query_fact(*_fixture(), shard_char_limit=100)
    with pytest.raises(seal.RepoNativeSealError, match="missing or extra shard"):
        seal.rehydrate_repo_native_query_fact(seal.RepoNativeSealPayload(p.manifest_json, p.shards[:-1], p.manifest_sha256))
    s = list(p.shards); s[0], s[1] = s[1], s[0]
    with pytest.raises(seal.RepoNativeSealError, match="shard"):
        seal.rehydrate_repo_native_query_fact(seal.RepoNativeSealPayload(p.manifest_json, tuple(s), p.manifest_sha256))


def test_shard_hash_tamper_fails():
    p = seal.seal_query_fact(*_fixture(), shard_char_limit=100); s = list(p.shards); s[0] += " "
    with pytest.raises(seal.RepoNativeSealError, match="shard"):
        seal.rehydrate_repo_native_query_fact(seal.RepoNativeSealPayload(p.manifest_json, tuple(s), p.manifest_sha256))


@pytest.mark.parametrize("kind", ["duplicate", "reorder"])
def test_provenance_duplicate_or_order_tamper_fails(kind):
    q, f = _fixture(); d = _copy(_doc(q, f)); refs = d["fact"]["semantic_fields"]["source_empirical_provenance_refs"]
    if kind == "duplicate": refs.append(refs[0])
    else: refs.reverse()
    with pytest.raises(seal.RepoNativeSealError): seal.rehydrate_repo_native_query_fact(_reseal(d))


@pytest.mark.parametrize("kind", ["authority", "provenance"])
def test_authority_or_provenance_drift_fails_existing_identity(kind):
    q, f = _fixture(); d = _copy(_doc(q, f))
    if kind == "authority": d["fact"]["authority_snapshot_refs"][0] = _a("tampered").as_dict()
    else:
        refs = d["fact"]["semantic_fields"]["source_empirical_provenance_refs"]; refs[0] = _r("C11LogicalRelease", "tampered").as_dict(); refs.sort(key=canonical_json)
    with pytest.raises(seal.RepoNativeSealError, match="constructor rejected"):
        seal.rehydrate_repo_native_query_fact(_reseal(d))


def test_denominator_risk_mismatch_and_count_mismatch_fail():
    q, f = _fixture(); fields = dict(f.semantic_fields); risk = tuple(ExactRef(**x) for x in fields["risk_set_member_refs"])
    for denom, pattern in [((risk[0], _r("RespondentIdentity", "outside")), "subset"), ((risk[0],), "denominator count")]:
        fields2 = dict(fields); fields2["denominator_member_refs"] = tuple(sorted(denom, key=lambda x: x.key))
        bad = EmpiricalFact(typed_state=f.typed_state, authority_snapshot_refs=f.authority_snapshot_refs, dependency_refs=f.dependency_refs,
            producer_replay_locator_or_reference_root=f.producer_replay_locator_or_reference_root, **fields2)
        with pytest.raises(seal.RepoNativeSealError, match=pattern): seal.rehydrate_repo_native_query_fact(_reseal(_doc(q, bad)))


def test_role_commitment_alias_fails():
    p = seal.seal_query_fact(*_fixture()); m = json.loads(p.manifest_json)
    m["sequence_commitments"]["fact.denominator_member_refs"] = dict(m["sequence_commitments"]["fact.risk_set_member_refs"])
    text = canonical_json(m); bad = seal.RepoNativeSealPayload(text, p.shards, hashlib.sha256(text.encode()).hexdigest())
    with pytest.raises(seal.RepoNativeSealError, match="commitment drift"): seal.rehydrate_repo_native_query_fact(bad)


def test_current_entrypoint_is_frozen_and_not_caller_selectable():
    assert not inspect.signature(seal.load_current_gt2_query_fact).parameters
    with pytest.raises(TypeError):
        seal.load_current_gt2_query_fact("override")


def test_transport_is_not_fact_and_rehydration_needs_no_runtime_file(monkeypatch):
    p = seal.seal_query_fact(*_fixture()); assert not isinstance(p, EmpiricalFact)
    monkeypatch.setattr(builtins, "open", lambda *a, **k: (_ for _ in ()).throw(AssertionError("filesystem forbidden")))
    q, f = seal.rehydrate_repo_native_query_fact(p); assert isinstance(q, EmpiricalQuerySpec) and isinstance(f, EmpiricalFact)
