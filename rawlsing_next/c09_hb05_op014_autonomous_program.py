"""C09 HB05-OP-014 frozen autonomous discovery program.

Adopts accepted PRE553 I05 exact-bounded discovery.  A/B/C identity,
performance results, primitive-I05 outputs, and post-outcome tuning are not
inputs, so they cannot steer the logical frontier or termination.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib, inspect, json, re
from typing import Any, Callable, Iterable, Mapping

PROGRAM_ID="C09_HB05_OP014_EXACT_BOUNDED_AUTONOMOUS_DISCOVERY_PROGRAM_R1"
PROGRAM_GRAIN="C09_HB05_OP014_AUTONOMOUS_DISCOVERY_SEARCH_TERMINATION_PROGRAM_AUTHORITY_AND_EXECUTABLE_CANDIDATE_R1_ONLY"
ENGINE_CONTRACT_ID="PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0"
ENGINE_GIT_BLOB_SHA="b2b99460cc5991bc26aa2ffe5bda129b408fc197"
L05_COMMISSION_TIP="600abba7d3c805e1f1e3e85de395a431021ee6e9"
L05_COMMISSION_BLOB_SHA="36cb39b70b9562d6f9ca0269bd4e0b4cc718883a"
K05_BLOCKER_COMMIT="66e3c90718bc11d080003e71571bfbdb7cfd4a22"
C09_MEASUREMENT_LAW_BLOB_SHA="2729ab4dca887f22fb3c90265f10c70020afdd3e"
HB05_MANIFEST_BLOB_SHA="e2bd3415c02bf7c8879773d09133f25d2c4d6a0c"
COVERAGE_CLAIM="COMPLETE_FOR_EXACT_DECLARED_FRONTIER"
TERMINATION_REASON="COMPLETE_EXACT_DECLARED_FRONTIER_EXHAUSTED"
TERMINAL_STATES=frozenset({"EVALUATED_SUPPORTED","EVALUATED_VALID_EMPTY","EVALUATED_UNDERPOWERED","EVALUATED_NONCOMPARABLE","EVALUATED_DENIED_BY_EXACT_AUTHORITY","EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY"})
B_PROGRAM="OP014_BLOCK__FROZEN_PROGRAM_IDENTITY_MISMATCH"
B_AUTH="OP014_BLOCK__DISCOVERY_AUTHORITY_NOT_EXACT_BOUNDED"
B_INPUT="OP014_BLOCK__NONEXACT_LOGICAL_INPUT_IDENTITY"
B_ENGINE="OP014_BLOCK__ACCEPTED_I05_ENGINE_CONTRACT_MISMATCH"
B_FRONTIER="OP014_BLOCK__INCOMPLETE_OR_NONTERMINAL_DISCOVERY_FRONTIER"
B_EXEC="OP014_BLOCK__DISCOVERY_ENGINE_EXECUTION_FAILURE"
_HEX64=re.compile(r"^[0-9a-f]{64}$")

def _c(v:Any)->Any:
    if v is None or isinstance(v,(str,int,bool)): return v
    if isinstance(v,float): raise TypeError("binary float forbidden")
    if isinstance(v,Mapping): return {str(k):_c(x) for k,x in sorted(v.items(),key=lambda p:str(p[0]))}
    if isinstance(v,(list,tuple)): return [_c(x) for x in v]
    if isinstance(v,(set,frozenset)): return sorted((_c(x) for x in v),key=lambda x:json.dumps(x,sort_keys=True,separators=(",",":")))
    if hasattr(v,"as_dict") and callable(v.as_dict): return _c(v.as_dict())
    raise TypeError(type(v).__name__)

def canonical_json(v:Any)->str: return json.dumps(_c(v),sort_keys=True,separators=(",",":"),ensure_ascii=False)
def semantic_hash(v:Any)->str: return hashlib.sha256(canonical_json(v).encode()).hexdigest()

FROZEN_PROGRAM_PAYLOAD={
 "program_id":PROGRAM_ID,"grain":PROGRAM_GRAIN,
 "authority":{"commission_tip":L05_COMMISSION_TIP,"commission_blob":L05_COMMISSION_BLOB_SHA,"parent_blocker":K05_BLOCKER_COMMIT},
 "law":{"c09_measurement_blob":C09_MEASUREMENT_LAW_BLOB_SHA,"hb05_manifest_blob":HB05_MANIFEST_BLOB_SHA,"operation":"HB05-OP-014"},
 "engine":{"module":"rawlsing_next.pre553_discovery_exact","contract":ENGINE_CONTRACT_ID,"git_blob":ENGINE_GIT_BLOB_SHA,"accepted_completion_commit":"6a75433b9a12b66e75f1def97f69163587970fd1"},
 "inputs":["repository","discovery_authority","authority_registry","release_refs","predicate_catalog","query_template_catalog"],
 "search":{"mode":"EXACT_BOUNDED","frontier":"EXACT_PRESEARCH_DISCOVERY_AUTHORITY_CANDIDATE_UNIVERSE","pruning":"NONE_EXACT_EVALUATE_ALL","rng":"NONE","order":"CANONICAL_CANDIDATE_HASH_ORDER","result_controls_frontier":False},
 "termination":{"reason":TERMINATION_REASON,"rule":"EVERY_PRECOMPILED_CANDIDATE_HAS_ONE_TERMINAL_COVERAGE_RECEIPT","terminal_states":sorted(TERMINAL_STATES)},
 "replay":{"preexecution_input_hash":True,"canonical_catalog_order":True,"covers":["program","inputs","result_replay","receipts","facts","termination"],"architecture_identity":False},
 "forbidden":["ARCHITECTURE_RANKING_OR_SELECTION","A_B_C_SEARCH_STEERING","PRIMITIVE_I05_OUTPUT_SUBSTITUTION","POST_OUTCOME_FRONTIER_CHANGE","SOURCE_SPECIFIC_POST_OUTCOME_TUNING","C09_COMPARISON_VERDICT","V553_V3_V2_PROMOTION"]}
FROZEN_PROGRAM_PAYLOAD_SHA256="5ccdde46139acbc94b07afd23db62450b997deffbc094617e5a61010b3e853c8"

class Op014ProgramBlocked(RuntimeError):
    def __init__(self,state:str,detail:str): self.blocker_state,self.detail=state,detail; super().__init__(f"{state}: {detail}")

@dataclass(frozen=True)
class Op014Receipt:
    typed_state:str; search_input_sha256:str; candidate_count:int; covered_candidate_count:int
    terminal_reason:str; result_replay_ref:Mapping[str,Any]; program_replay_sha256:str; receipt_sha256:str
    def as_dict(self): return _c(self.__dict__)

def _ref(v:Any,label:str)->Mapping[str,Any]:
    if hasattr(v,"as_dict") and callable(v.as_dict): v=v.as_dict()
    if not isinstance(v,Mapping) or set(v)!={"kind","object_id","content_hash"}: raise Op014ProgramBlocked(B_INPUT,f"{label} not exact ref")
    if not all(isinstance(v[k],str) and v[k] for k in ("kind","object_id")) or not isinstance(v["content_hash"],str) or not _HEX64.fullmatch(v["content_hash"]): raise Op014ProgramBlocked(B_INPUT,f"{label} invalid")
    return {k:v[k] for k in ("kind","object_id","content_hash")}

def _refs(xs:Iterable[Any],label:str,objects=False):
    vals=[_ref(x.ref if objects else x,label) for x in xs]; pairs=[(canonical_json(v),v) for v in vals]
    if len({k for k,_ in pairs})!=len(pairs): raise Op014ProgramBlocked(B_INPUT,f"duplicate {label}")
    return tuple(v for _,v in sorted(pairs))

def _auth(a:Any):
    ok=(getattr(a,"typed_state",None)=="EXACT_BOUNDED_AUTHORIZED" and getattr(a,"coverage_claim",None)==COVERAGE_CLAIM and getattr(a,"algorithm_identity_if_semantically_required",None)==ENGINE_CONTRACT_ID and getattr(a,"tie_order_rules",None)=="CANONICAL_CANDIDATE_HASH_ORDER" and isinstance(getattr(a,"pruning_contract",None),Mapping) and a.pruning_contract.get("kind")=="NONE_EXACT_EVALUATE_ALL")
    if not ok: raise Op014ProgramBlocked(B_AUTH,"authority not exact-bounded/evaluate-all/canonical-order")
    rng=getattr(a,"rng_policy_if_any",None)
    if rng not in (None,"NONE") and not (isinstance(rng,Mapping) and dict(rng)=={"kind":"NONE"}): raise Op014ProgramBlocked(B_AUTH,"rng must be NONE")
    fields=getattr(a,"semantic_fields",{})
    if isinstance(fields,Mapping) and (fields.get("mode","EXACT_BOUNDED")!="EXACT_BOUNDED" or (isinstance(fields.get("candidate_scoring_or_ranking_rule_if_any"),Mapping) and fields["candidate_scoring_or_ranking_rule_if_any"].get("controls_frontier") is True)): raise Op014ProgramBlocked(B_AUTH,"adaptive/ranking-controlled frontier forbidden")
    return _ref(a.ref,"discovery_authority")

def build_search_input_identity(*,discovery_authority:Any,release_refs:Iterable[Any],predicate_catalog:Iterable[Any],query_template_catalog:Iterable[Any]):
    if semantic_hash(FROZEN_PROGRAM_PAYLOAD)!=FROZEN_PROGRAM_PAYLOAD_SHA256: raise Op014ProgramBlocked(B_PROGRAM,"program payload hash mismatch")
    rel,pred,qry=_refs(tuple(release_refs),"release_refs"),_refs(tuple(predicate_catalog),"predicate_catalog",True),_refs(tuple(query_template_catalog),"query_template_catalog",True)
    if not rel or not qry: raise Op014ProgramBlocked(B_INPUT,"release/query sets must be nonempty")
    m={"program":FROZEN_PROGRAM_PAYLOAD_SHA256,"authority":_auth(discovery_authority),"releases":rel,"predicates":pred,"queries":qry,"result_independent_frontier":True,"termination":TERMINATION_REASON}
    return semantic_hash(m),m

def _git_blob(data:bytes)->str: return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()
def _load_engine()->Callable[...,Any]:
    from rawlsing_next import pre553_discovery_exact as e
    if getattr(e,"I05_CONTRACT_ID",None)!=ENGINE_CONTRACT_ID: raise Op014ProgramBlocked(B_ENGINE,"contract id mismatch")
    try:
        with open(e.__file__,"rb") as f: actual=_git_blob(f.read())
    except (OSError,TypeError) as x: raise Op014ProgramBlocked(B_ENGINE,f"engine bytes unavailable: {x}") from x
    if actual!=ENGINE_GIT_BLOB_SHA: raise Op014ProgramBlocked(B_ENGINE,f"engine blob {actual} != frozen {ENGINE_GIT_BLOB_SHA}")
    return e.execute_exact_bounded_discovery

def _execute_with_engine(engine:Callable[...,Any],*,repository:Any,discovery_authority:Any,authority_registry:Any,release_refs:Iterable[Any],predicate_catalog:Iterable[Any],query_template_catalog:Iterable[Any]):
    rel,pred,qry=tuple(release_refs),tuple(predicate_catalog),tuple(query_template_catalog)
    inp,_=build_search_input_identity(discovery_authority=discovery_authority,release_refs=rel,predicate_catalog=pred,query_template_catalog=qry)
    try: result=engine(repository=repository,discovery_authority=discovery_authority,authority_registry=authority_registry,release_refs=rel,predicate_catalog=pred,query_template_catalog=qry)
    except Op014ProgramBlocked: raise
    except Exception as x: raise Op014ProgramBlocked(B_EXEC,f"{type(x).__name__}: {x}") from x
    n,c=getattr(result,"candidate_count",None),getattr(result,"covered_candidate_count",None); receipts=tuple(getattr(result,"receipts",()))
    if getattr(result,"contract_id",None)!=ENGINE_CONTRACT_ID: raise Op014ProgramBlocked(B_ENGINE,"result contract mismatch")
    if getattr(result,"coverage_claim",None)!=COVERAGE_CLAIM or not isinstance(n,int) or isinstance(n,bool) or n<0 or c!=n or len(receipts)!=n or any(getattr(r,"coverage_state",None) not in TERMINAL_STATES for r in receipts): raise Op014ProgramBlocked(B_FRONTIER,"frontier incomplete/nonterminal")
    rr=_ref(getattr(result,"replay_ref",None),"result.replay_ref"); rrefs=_refs(receipts,"receipts",True) if receipts else (); frefs=_refs(tuple(getattr(result,"empirical_fact_refs",())),"facts")
    replay=semantic_hash({"program":FROZEN_PROGRAM_PAYLOAD_SHA256,"input":inp,"result_replay":rr,"n":n,"receipts":rrefs,"facts":frefs,"termination":TERMINATION_REASON})
    core={"typed_state":"OP014_EXECUTED_COMPLETE_EXACT_FRONTIER","search_input_sha256":inp,"candidate_count":n,"covered_candidate_count":c,"terminal_reason":TERMINATION_REASON,"result_replay_ref":rr,"program_replay_sha256":replay}
    return result,Op014Receipt(**core,receipt_sha256=semantic_hash(core))

def execute_op014_autonomous_discovery(*,repository:Any,discovery_authority:Any,authority_registry:Any,release_refs:Iterable[Any],predicate_catalog:Iterable[Any],query_template_catalog:Iterable[Any]):
    return _execute_with_engine(_load_engine(),repository=repository,discovery_authority=discovery_authority,authority_registry=authority_registry,release_refs=release_refs,predicate_catalog=predicate_catalog,query_template_catalog=query_template_catalog)

def public_input_names(): return tuple(inspect.signature(execute_op014_autonomous_discovery).parameters)
