import hashlib, inspect
from types import SimpleNamespace
import pytest
import rawlsing_next.c09_hb05_op014_autonomous_program as op

def h(x): return hashlib.sha256(x.encode()).hexdigest()
class R:
 def __init__(self,k,t): self.kind=k; self.object_id=f"urn:t:{k}:{t}"; self.content_hash=h(k+t)
 def as_dict(self): return {"kind":self.kind,"object_id":self.object_id,"content_hash":self.content_hash}
class O:
 def __init__(self,k,t): self.ref=R(k,t)
class A(O):
 def __init__(self):
  super().__init__("DiscoveryAuthority@1.0.0","a"); self.typed_state="EXACT_BOUNDED_AUTHORIZED"; self.coverage_claim=op.COVERAGE_CLAIM; self.algorithm_identity_if_semantically_required=op.ENGINE_CONTRACT_ID; self.tie_order_rules="CANONICAL_CANDIDATE_HASH_ORDER"; self.pruning_contract={"kind":"NONE_EXACT_EVALUATE_ALL"}; self.rng_policy_if_any="NONE"; self.semantic_fields={"mode":"EXACT_BOUNDED","candidate_scoring_or_ranking_rule_if_any":{"controls_frontier":False}}
class D(O):
 def __init__(self,t,s="EVALUATED_SUPPORTED"): super().__init__("DiscoveryResultReceipt@1.0.0",t); self.coverage_state=s
def result(t="x",n=2,c=None,s="EVALUATED_SUPPORTED"):
 return SimpleNamespace(contract_id=op.ENGINE_CONTRACT_ID,coverage_claim=op.COVERAGE_CLAIM,candidate_count=n,covered_candidate_count=n if c is None else c,receipts=tuple(D(f"{t}{i}",s) for i in range(n)),empirical_fact_refs=tuple(R("EmpiricalFact@1.0.0",f"{t}{i}") for i in range(n)),replay_ref=R("PRE553_I05_FRONTIER_REPLAY",t))
def args(): return dict(repository=object(),discovery_authority=A(),authority_registry=object(),release_refs=(R("C11Release","b"),R("C11Release","a")),predicate_catalog=(O("EmpiricalPredicate@1.0.0","b"),O("EmpiricalPredicate@1.0.0","a")),query_template_catalog=(O("EmpiricalQuerySpec@1.0.0","b"),O("EmpiricalQuerySpec@1.0.0","a")))
def eng(r): return lambda **kw:r

def test_program_hash(): assert op.semantic_hash(op.FROZEN_PROGRAM_PAYLOAD)==op.FROZEN_PROGRAM_PAYLOAD_SHA256
def test_public_contract_candidate_neutral(): assert op.public_input_names()==("repository","discovery_authority","authority_registry","release_refs","predicate_catalog","query_template_catalog")
def test_no_primitive_output_input(): assert all("primitive" not in x for x in op.public_input_names())
def test_engine_exact_blob_frozen(): assert op.ENGINE_GIT_BLOB_SHA=="b2b99460cc5991bc26aa2ffe5bda129b408fc197"
def test_complete_frontier():
 _,r=op._execute_with_engine(eng(result()),**args()); assert r.candidate_count==r.covered_candidate_count==2 and r.terminal_reason==op.TERMINATION_REASON
def test_input_order_invariant():
 a=args(); x,_=op.build_search_input_identity(discovery_authority=a["discovery_authority"],release_refs=a["release_refs"],predicate_catalog=a["predicate_catalog"],query_template_catalog=a["query_template_catalog"]); y,_=op.build_search_input_identity(discovery_authority=a["discovery_authority"],release_refs=a["release_refs"][::-1],predicate_catalog=a["predicate_catalog"][::-1],query_template_catalog=a["query_template_catalog"][::-1]); assert x==y
def test_outcomes_do_not_change_presearch_identity():
 a=args(); _,x=op._execute_with_engine(eng(result("x")),**a); _,y=op._execute_with_engine(eng(result("y")),**a); assert x.search_input_sha256==y.search_input_sha256 and x.program_replay_sha256!=y.program_replay_sha256
def test_incomplete_fails_closed():
 with pytest.raises(op.Op014ProgramBlocked) as e: op._execute_with_engine(eng(result(c=1)),**args())
 assert e.value.blocker_state==op.B_FRONTIER
def test_nonterminal_fails_closed():
 with pytest.raises(op.Op014ProgramBlocked): op._execute_with_engine(eng(result(s="UNEVALUATED")),**args())
def test_adaptive_authority_rejected():
 a=args(); a["discovery_authority"].typed_state="ADAPTIVE_EXPLORATORY_AUTHORIZED"
 with pytest.raises(op.Op014ProgramBlocked) as e: op._execute_with_engine(eng(result()),**a)
 assert e.value.blocker_state==op.B_AUTH
def test_pruning_or_rng_rejected():
 a=args(); a["discovery_authority"].pruning_contract={"kind":"TOP_K"}
 with pytest.raises(op.Op014ProgramBlocked): op._execute_with_engine(eng(result()),**a)
 b=args(); b["discovery_authority"].rng_policy_if_any={"kind":"SEEDED","seed":1}
 with pytest.raises(op.Op014ProgramBlocked): op._execute_with_engine(eng(result()),**b)
def test_result_controlled_frontier_rejected():
 a=args(); a["discovery_authority"].semantic_fields["candidate_scoring_or_ranking_rule_if_any"]={"controls_frontier":True}
 with pytest.raises(op.Op014ProgramBlocked): op._execute_with_engine(eng(result()),**a)
def test_nonexact_ref_and_duplicate_catalog_rejected():
 a=args(); a["release_refs"]=({"kind":"C11","object_id":"x","content_hash":"latest"},)
 with pytest.raises(op.Op014ProgramBlocked): op._execute_with_engine(eng(result()),**a)
 b=args(); p=O("EmpiricalPredicate@1.0.0","same"); b["predicate_catalog"]=(p,p)
 with pytest.raises(op.Op014ProgramBlocked): op._execute_with_engine(eng(result()),**b)
def test_engine_error_typed_and_no_verdict_output():
 def bad(**kw): raise ValueError("boom")
 with pytest.raises(op.Op014ProgramBlocked) as e: op._execute_with_engine(bad,**args())
 assert e.value.blocker_state==op.B_EXEC
 _,r=op._execute_with_engine(eng(result()),**args()); assert not ({"winner","rank","architecture","verdict"}&set(r.as_dict()))
def test_public_executor_rejects_hidden_architecture_kw():
 assert all(p.kind is not inspect.Parameter.VAR_KEYWORD for p in inspect.signature(op.execute_op014_autonomous_discovery).parameters.values())
 with pytest.raises(TypeError): op.execute_op014_autonomous_discovery(**args(),architecture="A")
