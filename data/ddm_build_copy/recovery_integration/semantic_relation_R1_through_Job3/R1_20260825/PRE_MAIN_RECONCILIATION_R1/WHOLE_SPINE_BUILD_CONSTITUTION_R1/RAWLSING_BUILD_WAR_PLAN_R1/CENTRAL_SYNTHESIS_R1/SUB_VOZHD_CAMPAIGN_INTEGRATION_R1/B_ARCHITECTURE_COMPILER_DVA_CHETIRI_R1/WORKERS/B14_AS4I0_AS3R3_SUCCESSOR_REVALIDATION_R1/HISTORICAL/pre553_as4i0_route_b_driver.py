"""AS4I0 exact AS3R2 loader and fail-closed Route-B production driver."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib, importlib.util, json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

DA="98d52062a0acc04a1949053a8f83397621e810950ff70ceff0260b68d17fd28c"
GRAMMAR="85d314d8222d96328b3e0449495ea3946d02cecaf3f2ccd3b249270a3fca2b66"
FRONTIER="84349595622ed6eec5bd6af60de5b74df26ae6752ae64e40d7595fd7560b7d67"
REPLAY="a1dcecc79c9174ffbb0e6607676689706ccf1a8f8753bbb417a1d7aaabef45d6"
BINDING="88cf52def32ad8942628e90d3f954d8fc59c785c668a891290ddf74a91d19afd"
SOURCE="7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
C11="e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
AS2BREPLAY="6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"
SUPPORT="6df2664f4a9cd8fe5d334b954aed4db1b97de4937b4d03e5ce63bcc322baab4c"
FILES={"snapshot":"02_DISCOVERY_FRONTIER_AUTHORITY_SNAPSHOT.json","binding":"04_RUNTIME_CATALOG_BINDING_MANIFEST.json","da":"05_FINAL_DISCOVERY_AUTHORITY.json","grammar":"06_OFFICIAL_CANDIDATE_GRAMMAR.json","frontier":"07_OFFICIAL_82_CANDIDATE_FRONTIER_MANIFEST.json","replay":"10_OFFICIAL_PREEXECUTION_REPLAY_CLOSURE_RECEIPT.json","final":"13_FINAL_AS3R2_RETURN.json"}

class AS4I0Error(RuntimeError): pass
class SealValidationError(AS4I0Error): pass
class RuntimeCatalogPreimageMissing(AS4I0Error): pass

def _load(p):
    try: x=json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as e: raise SealValidationError(f"cannot load exact seal artifact {p}: {e}") from e
    if not isinstance(x,dict): raise SealValidationError(f"seal artifact must be one JSON object: {p}")
    return x

def _hash(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def _rh(x,label):
    h=x.get("content_hash") if isinstance(x,Mapping) else None
    if not isinstance(h,str) or len(h)!=64: raise SealValidationError(f"{label} lacks exact content_hash")
    return h
def _eq(a,b,label):
    if a!=b: raise SealValidationError(f"{label} mismatch: expected {b!r}, got {a!r}")

@dataclass(frozen=True)
class AS3R2Seal:
    root: Path
    documents: Mapping[str,Mapping[str,Any]]
    predicate_refs: tuple[Mapping[str,Any],...]
    query_refs: tuple[Mapping[str,Any],...]

def load_and_validate_as3r2(root):
    root=Path(root); d={k:_load(root/v) for k,v in FILES.items()}
    da=d["da"]; sf=da.get("semantic_fields",{}); definition=sf.get("candidate_universe_definition",{})
    _eq(da.get("content_hash"),DA,"DiscoveryAuthority hash"); _eq(_rh(da.get("exact_ref",{}),"DA exact_ref"),DA,"DA exact ref")
    _eq(_rh(sf.get("candidate_grammar_ref",{}),"grammar ref"),GRAMMAR,"grammar ref"); _eq(_hash(definition),GRAMMAR,"grammar material hash")
    _eq(sf.get("support_rules",{}).get("minimum_raw_denominator"),0,"minimum_raw_denominator")
    _eq(sf.get("pruning_contract",{}).get("kind"),"NONE_EXACT_EVALUATE_ALL","pruning")
    _eq(sf.get("tie_order_rules"),"CANONICAL_CANDIDATE_HASH_ORDER","tie order"); _eq(sf.get("rng_policy_if_any"),"NONE","rng")
    atoms=definition.get("atoms",()); queries=definition.get("query_templates",()); rules=definition.get("rules",())
    if any(isinstance(x,(str,bytes)) or not isinstance(x,Sequence) for x in (atoms,queries,rules)): raise SealValidationError("grammar collections missing")
    _eq((len(atoms),len(queries),len(rules)),(19,3,82),"grammar counts")
    b=d["binding"]; pb=b.get("predicate_bindings",()); qb=b.get("query_bindings",())
    _eq((b.get("runtime_predicate_count"),b.get("runtime_query_template_count"),len(pb),len(qb)),(19,3,19,3),"runtime binding counts")
    _eq(_rh(b.get("identity",{}),"binding identity"),BINDING,"binding identity")
    _eq({x["predicate_ref"]["content_hash"] for x in atoms},{x["runtime_empirical_predicate_ref"]["content_hash"] for x in pb},"predicate refs")
    _eq({x["query_ref"]["content_hash"] for x in queries},{x["runtime_empirical_query_spec_ref"]["content_hash"] for x in qb},"query refs")
    f=d["frontier"]; _eq(_rh(f.get("discovery_authority_ref",{}),"frontier DA"),DA,"frontier DA"); _eq(_rh(f.get("candidate_grammar_ref",{}),"frontier grammar"),GRAMMAR,"frontier grammar"); _eq(_rh(f.get("official_frontier_ref",{}),"frontier"),FRONTIER,"frontier")
    _eq((f.get("candidate_count"),len(f.get("candidates",[])),f.get("candidate_execution_count")),(82,82,0),"frontier counts")
    _eq((f.get("semantic_membership_change_count"),f.get("addition_count"),f.get("deletion_count")),(0,0,0),"frontier membership")
    _eq(f.get("canonical_order_law"),"CANONICAL_CANDIDATE_HASH_ORDER","frontier order")
    r=d["replay"]; _eq(_rh(r.get("discovery_authority_ref",{}),"replay DA"),DA,"replay DA"); _eq(_rh(r.get("candidate_grammar_ref",{}),"replay grammar"),GRAMMAR,"replay grammar"); _eq(_rh(r.get("official_frontier_ref",{}),"replay frontier"),FRONTIER,"replay frontier"); _eq(_rh(r.get("identity",{}),"replay closure"),REPLAY,"replay closure")
    _eq((r.get("source_sha256"),_rh(r.get("c11_release_ref",{}),"C11"),_rh(r.get("as2b_replay_manifest_ref",{}),"AS2B replay"),_rh(r.get("support_rule_ref",{}),"support"),r.get("candidate_execution_count")),(SOURCE,C11,AS2BREPLAY,SUPPORT,0),"replay inputs")
    z=d["final"]; _eq((z.get("unresolved_fairness_blocker_count"),z.get("pre_candidate_execution_fairness_blocker_count"),z.get("candidate_execution_count")),(0,0,0),"fairness/execution blockers")
    _eq(z.get("official_frontier",{}).get("hash"),FRONTIER,"final frontier"); _eq(z.get("discovery_authority",{}).get("content_hash"),DA,"final DA")
    return AS3R2Seal(root,d,tuple(x["runtime_empirical_predicate_ref"] for x in pb),tuple(x["runtime_empirical_query_spec_ref"] for x in qb))

def _materialize(doc,cls):
    fields=doc.get("semantic_fields")
    if not isinstance(fields,Mapping): raise RuntimeCatalogPreimageMissing(f"{cls.__name__} semantic_fields missing")
    return cls(schema_id=doc.get("schema_id"),schema_version=doc.get("schema_version"),typed_state=doc.get("typed_state"),authority_snapshot_refs=doc.get("authority_snapshot_refs",()),dependency_refs=doc.get("dependency_refs",()),producer_replay_locator_or_reference_root=doc.get("producer_replay_locator_or_reference_root"),object_id=doc.get("object_id"),content_hash=doc.get("content_hash"),**fields)

def validate_runtime_catalog_preimages(seal,predicate_documents,query_documents):
    from rawlsing_next.pre553_empirical_objects import EmpiricalPredicate,EmpiricalQuerySpec
    p=tuple(_materialize(x,EmpiricalPredicate) for x in predicate_documents); q=tuple(_materialize(x,EmpiricalQuerySpec) for x in query_documents)
    _eq((len(p),len(q)),(19,3),"runtime object counts"); _eq({x.content_hash for x in p},{_rh(x,"predicate ref") for x in seal.predicate_refs},"predicate identities"); _eq({x.content_hash for x in q},{_rh(x,"query ref") for x in seal.query_refs},"query identities")
    return p,q

def require_runtime_catalog_payload(path,seal):
    path=Path(path)
    if not path.exists(): raise RuntimeCatalogPreimageMissing("AS4I0-B01__AS3R2_RUNTIME_CATALOG_CANONICAL_OBJECT_PREIMAGES_NOT_SERIALIZED: accepted AS3R2 seals 19 predicate refs and 3 query refs but no full canonical object projections/replay roots; exact SHA-256 refs cannot be inverted or guessed")
    x=_load(path); return validate_runtime_catalog_preimages(seal,x.get("predicates",()),x.get("queries",()))

def materialize_discovery_authority(seal):
    from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority
    x=_materialize(seal.documents["da"],DiscoveryAuthority); _eq(x.content_hash,DA,"materialized DA"); return x

def materialize_frontier_snapshot(seal):
    from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
    x=_materialize(seal.documents["snapshot"],AuthoritySnapshot); _eq(x.content_hash,"c553cb8a05923f4d344366a47460050888cd4b602e09d61d05a2f79100200980","frontier authority snapshot"); return x

@dataclass
class RouteBSourceSession:
    repository: Any; release: Any; context: Mapping[str,Any]
    source_sha256: str; projection_hash: str; repository_snapshot_hash: str; replay_manifest_hash: str
    persistent_transformed_empirical_payload_files: tuple[str,...]=()
    def close(self): self.repository=None; self.release=None; self.context={}

def load_banked_as2b_builder(script,as2a_dir):
    spec=importlib.util.spec_from_file_location("_as4i0_banked_as2b",Path(script))
    if spec is None or spec.loader is None: raise AS4I0Error("cannot load banked AS2B builder")
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.PART_A_DIR=Path(as2a_dir); m.LEDGER=m.PART_A_DIR/"01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv"; m.PACKAGE=m.PART_A_DIR/"04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json"
    return m

def build_route_b_source_session(source_path,banked_as2b_builder,banked_as2a_dir):
    m=load_banked_as2b_builder(banked_as2b_builder,banked_as2a_dir); source_path=Path(source_path)
    _eq(m.sha256_file(source_path),SOURCE,"LiTS-I source SHA"); package,ledger,slots=m.read_banked_authority()
    incidence=m.decode_dta(source_path,encoding="latin1"); _eq((incidence.source_sha256,incidence.row_count,len(incidence.variables)),(SOURCE,m.ROWS,m.VARIABLES),"decoded source identity")
    projection,context=m.build_projection(incidence,package,ledger,slots); _eq(projection.cache_identity,"84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872","projection hash")
    names={"country","city","region","tablec","tabled","q301_2","q301_7"}; vars=tuple(v for v in incidence.variables if v.name in names); _eq({v.name for v in vars},names,"projection slots")
    selected=m.PhysicalSourceIncidence(source_sha256=incidence.source_sha256,source_format=incidence.source_format,row_count=incidence.row_count,variables=vars,reader_configuration={**incidence.reader_configuration,"transport":"AS4I0_ROUTE_B_EXACT_SELECTED_SLOT_STREAM"},file_metadata=incidence.file_metadata,_frame=incidence._frame[[v.name for v in vars]])
    candidate=m.project_c11_candidate_from_physical_cells(source_sha256=SOURCE,row_count=m.ROWS,cells=(m.exact_cell(c) for c in selected.iter_cells(batch_size=20000)),projection=projection)
    _eq(candidate.candidate_replay_manifest.semantic_projection_hash,"7f81a222ea2611638d7ce7ac55c695120b57323832e6dc17ff65c1992201659c","C11 candidate")
    release=m.validate_c11_source_release(candidate); _eq(release.semantic_release_hash,C11,"C11 release"); _eq(release.replay_manifest.content_hash,AS2BREPLAY,"AS2B replay")
    repo=m.C11Repository((release,)); rh=m.semantic_hash(repo.snapshot_identity()); _eq(rh,"ff8a49d2560fe3cf229f4d5a0f87a14c52d08086a74649968d8c9c9d0225aa77","repository snapshot")
    return RouteBSourceSession(repo,release,context,SOURCE,projection.cache_identity,rh,release.replay_manifest.content_hash)

def execute_route_b_production(seal,session,predicate_documents,query_documents):
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
    from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
    p,q=validate_runtime_catalog_preimages(seal,predicate_documents,query_documents); da=materialize_discovery_authority(seal); snap=materialize_frontier_snapshot(seal)
    try:
        result=execute_exact_bounded_discovery(repository=session.repository,discovery_authority=da,authority_registry=AuthorityRegistry((*session.context["authorities"],snap)),release_refs=(session.release.release_ref,),predicate_catalog=p,query_template_catalog=q)
        _eq((result.evaluated_frontier_ref.content_hash,result.candidate_count,result.covered_candidate_count),(FRONTIER,82,82),"executed frontier")
        return result
    finally: session.close()

def preflight_receipt():
    return {"schema":"AS4I0_AS3R2_PREFLIGHT_RECEIPT@1.0.0","status":"PASS__SEALED_INPUTS_VALID__RUNTIME_OBJECT_PREIMAGES_REQUIRED","discovery_authority_hash":DA,"candidate_grammar_hash":GRAMMAR,"official_frontier_hash":FRONTIER,"candidate_count":82,"predicate_count":19,"query_template_count":3,"fairness_blocker_count":0,"source_sha256":SOURCE,"candidate_execution_count":0,"persistent_transformed_empirical_payload_files":[]}
