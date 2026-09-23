from __future__ import annotations
import copy, hashlib, importlib.util, json, subprocess, sys, tempfile, types, warnings
from pathlib import Path

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, CarrierExecutionBindingError
from rawlsing_next.pre553_discovery_exact import (
    I05_CONTRACT_ID, ExactBoundedDiscoveryError, _catalog_atoms, _catalog_templates,
    _compile_frontier, _validate_catalog_scope, _verify_discovery_authority,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, AuthoritySnapshot, DiscoveryAuthority, ExactRef, authority_ref,
    exact_ref, semantic_hash,
)
from rawlsing_next.pre553_runtime_authority import Pre553RuntimeAuthoritySet
from rawlsing_next.pre553_runtime_context import bind_runtime
from rawlsing_next.fiabc_lits_i_i03_operation_authority import (
    AUTHORITY_CONTENT_HASH as I03_OPERATION_SUCCESSOR_HASH,
    PARENT_AUTHORITY_REF as I03_PARENT_AUTHORITY_REF,
    PART_A_PROJECTION_AUTHORITY_HASH,
    RUNTIME_CATALOG_IDENTITY as I03_RUNTIME_CATALOG_IDENTITY,
    historical_i03_parent_authority_snapshot,
    historical_projection_authority_snapshot,
    operation_successor_authority_record,
)
from rawlsing_next.fiabc_lits_i_d03_risk_set_authority import (
    AUTHORITY_CONTENT_HASH as D03_RISK_SET_SUCCESSOR_HASH,
    risk_set_successor_authority_record,
)
from rawlsing_next.fiabc_lits_i_f02_event_representation_authority import (
    AUTHORITY_CONTENT_HASH as F02_EVENT_REPRESENTATION_SUCCESSOR_HASH,
    event_representation_successor_authority_record,
)
from rawlsing_next.fiabc_lits_cross_schema_candidate_identity import (
    current_pre553_logical_candidate_bindings,
)

ROOT=Path(__file__).resolve().parents[3]
OWNER_COMMIT="0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
A_PATH="rawlsing_next/pre553_r5_source_backed_adapter.py"; A_BLOB="d4915e7e6755ba1850756aebff72f982f73a332b"
B_PATH="rawlsing_next/pre553_source_backed_c11_facade.py"; B_BLOB="7c509c2098d0030f253344eb3f682471378812a8"
P2R1="9511f44728a8469d685463ec0fc880864c9187de"
P2R1_SEAM="rawlsing_next/pre553_carrier_execution.py"; P2R1_SEAM_BLOB="e7cda773e6a2426bfa12b22790fd8e005fe75153"
P2R1_MATRIX="WORKER_RETURNS/EE-P2R1/10_ABC_ADAPTER_QUALIFICATION_MATRIX.json"
P2X="29e434a385719f9835e0bcd252fb24bc37675a99"
A_STAGE="WORKER_RETURNS/EE-P2X/01_LITS_I_A_FIRST_BUILD_STAGE.json"
B_STAGE="WORKER_RETURNS/EE-P2X/03_LITS_I_B_CACHELESS_C11_STAGE.json"
D02="40cb8585f076a66d9884b99022a59bb909606c03"
D02_PATH="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/HQ_FIRST_WAVE_FANIN_AND_SECOND_WAVE_DISPATCH_R1/SECOND_WAVE_WORKER_RETURNS/W2-D02/01_FROZEN_DISCOVERY_FRONTIER_AUTHORITY.json"
D02_BLOB="5399a3f64642c8d9f8a0644db0adc15d38642971"
F02="482bb884a99e31ba77e904d0df39fffc872cbed3"
F02_PATH="rawlsing_next/prev3_lits1_selector_closure.py"; F02_BLOB="7b45b277164fa90c3da739aab26b516f7a8cb8dc"
B12="e5f9a14a77c2b84a86ce6eefaddb4b5c12b17e39"
NODE4A_SUPPORT="WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py"
NODE4A_BLOB="504944f9533b7385d201076e2e834b8a9446dee8"
QUERY_INPUT_PATH="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B6_AS3R3_NODE4B_QUERY_INPUT_FREEZE_R1/01_QUERY_INPUTS.json"
QUERY_INPUT_BLOB="3f56e3b3c5e3c3be61adef392ee9ca59875827a3"
PRODUCER="cfc240aa3a64c59509eab97450a7d3603af813cc"
PRODUCER_PATH="rawlsing_next/pre553_as3r3_runtime_producer.py"; PRODUCER_BLOB="d63370dbcadc043dd2f27f5383cf36f0e84d1235"
CONTRACT_PATH="rawlsing_next/pre553_as3r3_runtime_producer_contract.py"; CONTRACT_BLOB="26a7d123881513524e26f2342ab93dd1141fb5f6"
R6N="ab7e7f6e764eba43e85fe5c8629fee6cc0ba2a5c"
R6N_PROOF="WORKER_RETURNS/EE-P2R6N/03_R6A_PRODUCTION_RUNTIME_PROOF.json"; R6N_PROOF_BLOB="b18811757596058fe97a7f6088c39e00ef6ca05f"
HQ_HANDOFF="73eae181e4c831cddc4db8780fde08bdcd47d270"
REGISTRY="HQ_HANDOFF/BINDING_REGISTRY_SNAPSHOTS/20260918T2000-0400.json"
REGISTRY_HASH="6f2eb0f93576b6ea2b9360fdb7c437f9f1810056494149c64b03d2c7834d03c4"
ACTIVE_BINDING="a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308"
QUARANTINED="fd4177eaddff07dc1e51a6f900c07f163965f996742b301932bbeb79a8690bb0"
BASE_RELEASE="e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
RUNTIME_RELEASE="192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f"
R4_HASHES=("3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74","0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55","225e4b80390500451834ea784d955465eb9f145a4cd1f798dace51f3a6d3baa4","b87c387f9d222c83106c8d47d369af44f5c5368b274fd85e7a08b12c20d49cae")
R5A="6586da01edac5e87fb81b6beb8d7b16fc0ea18ef"
R5A_RELATION="WORKER_RETURNS/EE-P2R5A/02_RELEASE_REALIZATION_RELATION_AUTHORITY.json"; R5A_RELATION_BLOB="a0af45cc3db6e81def84357f50c310daac32b1e5"
R5A_SCHEMA="WORKER_RETURNS/EE-P2R5A/03_CONCRETE_REALIZATION_BINDING_SCHEMA.json"; R5A_SCHEMA_BLOB="00159aae4117c00d9dfcc7e9b558e1c1d1637302"
R5A_CLAUSE="WORKER_RETURNS/EE-P2R5A/04_R4A_RELEASE_PRECONDITION_SUCCESSOR_CLAUSE.json"; R5A_CLAUSE_BLOB="3a2802954412e075373920d1351cc3b37a2ebbd3"
R6J="ab7e7f6e764eba43e85fe5c8629fee6cc0ba2a5c"
R6J_BINDING="WORKER_RETURNS/EE-P2R6J/04_PROPOSED_ACTIVE_RUNTIME_BINDING_RECORD.json"; R6J_BINDING_BLOB="4ac8cd48aac62600e648ff9692488796c51c826f"
R5_HASHES=("9da19997168612891f59012e69674bac59fbee417d9b30b003171f3074168bf5","d9aa476c493810651baefa8bad23990d9dd80812a48670ad2052353f0e7d52a2","a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0","d8e3d9a19fa36599e8cd6b1bc8e82092c425fd9119be478f7ba79335d05a1b3e")
BASE_REFS={"A000":"ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0","A1V1":"082157ea8f31fe0d209c6241552116108e3e3917f7ddb7a49fa365ad5362aeeb","A1V5":"9ba962d35fc630686b7538ae22dbabe2f5b51fe8c7b3473beab901214b1db43c"}
F02_REFS={"Q310V1":"c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a","Q310V2":"78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df","Q310V3":"c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca","Q311V1":"69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8","Q311V2":"f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849","Q311V3":"a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d"}
QUERY_REFS={"T_Q301_2_RAW":"8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44","T_Q301_7_RAW":"deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7","T_Q301_2_Q301_7_RAW":"ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053"}
F02_GRAMMAR="bc6d433ff58e67e343f1bd1d8e3e92d691b81931dca6447716b08dbf0c8eff8b"
BASE_GRAMMAR="6c6d2f5fb5f4165e5de19989bd456ee8c09f42ab175fa4d10572dc2b9403ca0d"

def sh(cmd): return subprocess.check_output(cmd,cwd=ROOT)
def ensure(commit):
    if subprocess.run(["git","cat-file","-e",commit+"^{commit}"],cwd=ROOT).returncode:
        subprocess.run(["git","fetch","--no-tags","origin",commit],cwd=ROOT,check=True)
def git_bytes(commit,path):
    ensure(commit); return sh(["git","show",f"{commit}:{path}"])
def git_json(commit,path): return json.loads(git_bytes(commit,path))
def git_blob_sha(commit,path):
    ensure(commit)
    return sh(["git","rev-parse",f"{commit}:{path}"]).decode().strip()
def mod_from_bytes(name,data):
    m=types.ModuleType(name); m.__file__=f"<{name}>"; sys.modules[name]=m
    exec(compile(data.decode(),m.__file__,"exec"),m.__dict__); return m

def load_producer():
    contract=git_bytes(PRODUCER,CONTRACT_PATH); assert git_blob_sha(PRODUCER,CONTRACT_PATH)==CONTRACT_BLOB
    mod_from_bytes("rawlsing_next.pre553_as3r3_runtime_producer_contract",contract)
    producer=git_bytes(PRODUCER,PRODUCER_PATH); assert git_blob_sha(PRODUCER,PRODUCER_PATH)==PRODUCER_BLOB
    return mod_from_bytes("ee_p2r6o_exact_b12_producer",producer)

def load_base_objects():
    producer=load_producer()
    node4_path=ROOT/NODE4A_SUPPORT
    assert sh(["git","hash-object",str(node4_path)]).decode().strip()==NODE4A_BLOB
    node4=mod_from_bytes("ee_p2r6o_node4a",node4_path.read_bytes())
    records=node4.load_predicate_inputs()
    preds={r["as3_semantic_source_identity"]["as3_id"]:producer.construct_successor_predicate(r) for r in records}
    assert git_blob_sha(B12,QUERY_INPUT_PATH)==QUERY_INPUT_BLOB
    qdoc=json.loads(git_bytes(B12,QUERY_INPUT_PATH))
    allrefs=tuple(p.ref for p in preds.values())
    queries={r["as3_semantic_source_identity"]["as3_id"]:producer.construct_successor_query(r,successor_predicate_refs=allrefs) for r in qdoc["query_inputs"]}
    assert {k:v.content_hash for k,v in preds.items() if k in BASE_REFS}==BASE_REFS
    assert {k:v.content_hash for k,v in queries.items()}==QUERY_REFS
    return preds,queries

def load_f02():
    assert git_blob_sha(F02,F02_PATH)==F02_BLOB
    m=mod_from_bytes("ee_p2r6o_exact_f02",git_bytes(F02,F02_PATH))
    closure=m.build_selector_closure(); out={}
    for sid,item in closure["selectors"].items():
        doc=dict(item["predicate_projection"]); doc["object_id"]=item["predicate_ref"]["object_id"]; doc["content_hash"]=item["predicate_ref"]["content_hash"]
        from rawlsing_next.pre553_carrier_execution import materialize_public_object
        obj=materialize_public_object(doc); out[item["atom_id"]]=obj
    assert {k:v.content_hash for k,v in out.items()}==F02_REFS
    return closure,out

R4A_MIXED_AUTHORITY_ID="urn:rawlsing:prev3:p2r4a:pre553:mixed-predicate-grammar"
R4A_MIXED_AUTHORITY_VERSION="1.0.0-candidate"
R4A_MIXED_AUTHORITY_HASH="0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55"
R4A_SUCCESSOR_AUTHORITY_HASH="b87c387f9d222c83106c8d47d369af44f5c5368b274fd85e7a08b12c20d49cae"
R4A_ADOPTION_DECISION_ID="HQD-2026-09-18-044"
R4A_ADOPTION_DECISION_HASH="38ccf7e51fde4366f86c9d181b18da6efd59751be8f4b84f16685953cd79d891"


def _r4a_mixed_grammar_adoption_snapshot(mixed, successor, decision_records=None):
    """Materialize the exact HQ-adopted mixed-grammar ref as a history snapshot.

    The R4A fixture remains an immutable candidate artifact. Its status field
    records the worker's pre-adoption state; current activation is controlled
    by the exact HQ decision and immutable authority identity below.
    """
    if decision_records is None:
        ledger_path=ROOT/"HQ_HANDOFF/DECISION_LEDGER.jsonl"
        decision_records=[json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line]
    matches=[(i,record) for i,record in enumerate(decision_records) if record.get("decision_id")==R4A_ADOPTION_DECISION_ID]
    if len(matches)!=1:
        raise Pre553AuthorityError("exact HQ R4A mixed-authority adoption decision must resolve once")
    decision_index, decision=matches[0]
    if (
        decision.get("status")!="ADOPTED_BOUNDED_PRE553_PUBLIC_PREDICATE_AND_MIXED_COMPOSITION_SUCCESSOR_AUTHORITY"
        or decision.get("subject")!="EE-P2R4A D02/F02 identity-preserving predicate dialect and mixed-composition authority"
        or semantic_hash(decision)!=R4A_ADOPTION_DECISION_HASH
    ):
        raise Pre553AuthorityError("exact HQ R4A adoption decision identity/status drift")
    for later in decision_records[decision_index+1:]:
        supersedes=later.get("supersedes",())
        if isinstance(supersedes,(list,tuple)) and ({R4A_ADOPTION_DECISION_ID,R4A_MIXED_AUTHORITY_HASH}&set(supersedes)):
            raise Pre553AuthorityError("HQ R4A mixed-authority adoption was explicitly superseded")

    ref=authority_ref(mixed.get("candidate_authority_ref"),"R4A mixed authority candidate ref")
    if mixed.get("authority_content_hash")!=R4A_MIXED_AUTHORITY_HASH or semantic_hash(mixed.get("identity_material"))!=R4A_MIXED_AUTHORITY_HASH:
        raise Pre553AuthorityError("R4A mixed composition authority preimage/hash mismatch")
    if (ref.authority_id,ref.authority_version,ref.authority_content_hash)!=(
        R4A_MIXED_AUTHORITY_ID,R4A_MIXED_AUTHORITY_VERSION,R4A_MIXED_AUTHORITY_HASH
    ):
        raise Pre553AuthorityError("R4A mixed authority exact ref drift")
    material=mixed.get("identity_material")
    if not isinstance(material,dict):
        raise Pre553AuthorityError("R4A mixed authority identity material is absent")
    successor_hash=successor.get("authority_candidate_content_hash")
    if not isinstance(successor_hash,str):
        raise Pre553AuthorityError("R4A successor authority hash is absent")
    if semantic_hash(successor.get("identity_material"))!=successor_hash:
        raise Pre553AuthorityError("R4A public predicate successor preimage/hash mismatch")
    if successor_hash!=R4A_SUCCESSOR_AUTHORITY_HASH:
        raise Pre553AuthorityError("R4A adopted successor authority identity drift")
    successor_material=successor.get("identity_material")
    if not isinstance(successor_material,dict):
        raise Pre553AuthorityError("R4A successor authority identity material is absent")
    if authority_ref(successor_material.get("mixed_grammar_authority_ref"))!=ref:
        raise Pre553AuthorityError("R4A successor does not bind the exact mixed grammar authority")
    approved={
        R4A_MIXED_AUTHORITY_HASH,
        R4A_SUCCESSOR_AUTHORITY_HASH,
        "3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74",
        "225e4b80390500451834ea784d955465eb9f145a4cd1f798dace51f3a6d3baa4",
    }
    if not approved<=set(decision.get("authority_refs",())):
        raise Pre553AuthorityError("HQ R4A decision omits one or more linked adopted authority refs")
    if R4A_MIXED_AUTHORITY_HASH not in R4_HASHES:
        raise Pre553AuthorityError("R4A mixed authority is absent from exact runtime adoption pins")

    permitted=material.get("permitted_mixed_composition")
    if not isinstance(permitted,dict):
        raise Pre553AuthorityError("R4A permitted mixed composition is absent")
    if permitted.get("ast_operation")!="AND" or permitted.get("maximum_arity")!=3:
        raise Pre553AuthorityError("R4A exact mixed operation/arity scope drift")
    decision_digest=semantic_hash(decision)
    decision_ref=ExactRef(
        "HQ_ADOPTION_DECISION",
        f"urn:rawlsing:hq:decision:{R4A_ADOPTION_DECISION_ID}",
        decision_digest,
    )
    scope={
        "exact_workload_scope":material["exact_workload_scope"],
        "allowed_input_grammar_refs":material["allowed_input_grammar_refs"],
        "permitted_mixed_composition":permitted,
        "leaf_operation_families":material["leaf_operation_families"],
        "respondent_binding_compatibility_ref":material["respondent_binding_compatibility_ref"],
        "identity_preservation":material["identity_preservation"],
        "negative_cases":material["negative_cases"],
        "no_adjacent_family_inference":material["no_adjacent_family_inference"],
        "fail_closed":material["fail_closed"],
        "adopted_successor_authority_ref":successor.get("candidate_ref"),
    }
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(decision_ref,),
        producer_replay_locator_or_reference_root=decision_ref,
        authority_id=ref.authority_id,
        authority_version=ref.authority_version,
        authority_content_hash=ref.authority_content_hash,
        authority_kind="PREDICATE_GRAMMAR",
        decision_state="ALLOW",
        governed_operations=(permitted["ast_operation"],),
        governed_object_families=("EmpiricalPredicate@1.0.0",),
        scope_envelope=scope,
        effective_time_or_interval=decision["date"],
        parent_authority_refs=tuple(material["parent_authority_refs"]),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(material),
        replay_protocol_ref=decision_ref,
    )


def r4_runtime():
    fix=ROOT/"rawlsing_next/tests/fixtures"
    def load(p): return json.loads(p.read_text())
    d=load(fix/"ee_p2r6a_r4a_01_dialect.json"); r=load(fix/"ee_p2r6a_r4a_02_respondent.json")
    m=load(fix/"ee_p2r6a_r4a_03_mixed.json"); der=load(fix/"ee_p2r6a_r4a_04_derived.json"); s=load(fix/"ee_p2r6a_r4a_05_successor.json")
    mixed_snapshot=_r4a_mixed_grammar_adoption_snapshot(m,s)
    for commit,path,blob in ((R5A,R5A_RELATION,R5A_RELATION_BLOB),(R5A,R5A_SCHEMA,R5A_SCHEMA_BLOB),(R5A,R5A_CLAUSE,R5A_CLAUSE_BLOB),(R6J,R6J_BINDING,R6J_BINDING_BLOB)):
        if git_blob_sha(commit,path)!=blob: raise Pre553AuthorityError("exact adopted R5A/R6J runtime authority blob drift")
    relation=git_json(R5A,R5A_RELATION); schema=git_json(R5A,R5A_SCHEMA); clause=git_json(R5A,R5A_CLAUSE); binding=git_json(R6J,R6J_BINDING)
    if binding["binding_ref"]["content_hash"]!=ACTIVE_BINDING: raise Pre553AuthorityError("exact adopted active realization binding drift")
    return Pre553RuntimeAuthoritySet(adopted_authority_hashes=(*R4_HASHES,*R5_HASHES,I03_OPERATION_SUCCESSOR_HASH,I03_PARENT_AUTHORITY_REF.authority_content_hash,PART_A_PROJECTION_AUTHORITY_HASH,D03_RISK_SET_SUCCESSOR_HASH,F02_EVENT_REPRESENTATION_SUCCESSOR_HASH),predicate_dialect_matrices=(d,),respondent_compatibility_authorities=(r,),mixed_composition_authorities=(m,),derived_predicate_contracts=(der,),public_predicate_successor_authorities=(s,),i03_operation_successor_authorities=(operation_successor_authority_record(),),exact_risk_set_successor_authorities=(risk_set_successor_authority_record(),),event_representation_successor_authorities=(event_representation_successor_authority_record(),),historical_authority_snapshots=(historical_projection_authority_snapshot(),historical_i03_parent_authority_snapshot(),mixed_snapshot),release_realization_authorities=(relation,),realization_binding_schemas=(schema,),release_precondition_clauses=(clause,),realization_bindings=(binding,))

def closure_snapshot(ref,kind="REPLAY_PROTOCOL",ops=("EXACT_REPOSITORY_BOUND_CLOSURE",),families=("EmpiricalPredicate@1.0.0","EmpiricalQuerySpec@1.0.0")):
    ar=authority_ref(ref)
    rootmat={"authority_ref":ar.as_dict(),"purpose":"EE_P2R6O_EXACT_REF_CLOSURE_FROM_REPOSITORY_PREIMAGE"}
    root=ExactRef("EE_P2R6O_AUTHORITY_CLOSURE_INPUT",f"urn:rawlsing:prev3:p2r6o:authority-closure:sha256:{semantic_hash(rootmat)}",semantic_hash(rootmat))
    return AuthoritySnapshot(typed_state="ALLOW",authority_snapshot_refs=(),dependency_refs=(),producer_replay_locator_or_reference_root=root,
        authority_id=ar.authority_id,authority_version=ar.authority_version,authority_content_hash=ar.authority_content_hash,
        authority_kind=kind,decision_state="ALLOW",governed_operations=ops,governed_object_families=families,
        scope_envelope={"source_universe_refs":"EXPLICIT_UNRESTRICTED","target_use_refs":"EXPLICIT_UNRESTRICTED","predicate_or_risk_set_refs":"EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="REPOSITORY_BOUND_EXACT_REF",parent_authority_refs=(),negative_limit_refs=(),supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(rootmat),replay_protocol_ref=root)

def catalog_and_frontier():
    d02=git_json(D02,D02_PATH); assert git_blob_sha(D02,D02_PATH)==D02_BLOB
    base,queries=load_base_objects(); closure,f02=load_f02()
    primitives={**{k:base[k] for k in BASE_REFS},**f02}
    definition=copy.deepcopy(d02["candidate_grammar"])
    definition["atoms"]=[{"atom_id":k,"kind":"FROZEN_PRIMITIVE","predicate_ref":v.ref.as_dict(),"ancestry_refs":[]} for k,v in primitives.items()]
    definition["query_templates"]=[{"template_id":k,"query_ref":queries[k].ref.as_dict()} for k in ("T_Q301_2_RAW","T_Q301_7_RAW","T_Q301_2_Q301_7_RAW")]
    grammar_hash=semantic_hash(definition)
    grammar_ref=ExactRef("PRE553_I05_CANDIDATE_GRAMMAR",f"urn:rawlsing:prev3:p2r6o:d02-f02-grammar:sha256:{grammar_hash}",grammar_hash)
    op=definition["discovery_operation"]
    fm={"d02_commit":D02,"d02_blob":D02_BLOB,"f02_commit":F02,"f02_blob":F02_BLOB,"r4a":list(R4_HASHES),"binding":ACTIVE_BINDING,"r6n":R6N}
    fh=semantic_hash(fm); far=AuthorityRef("urn:rawlsing:prev3:p2r6o:d02-f02-frontier-qualification","1.0.0",fh)
    fs=closure_snapshot(far,"DISCOVERY_FRONTIER",(op,),("DiscoveryAuthority@1.0.0","DiscoveryResultReceipt@1.0.0"))
    universe=d02["source_scope"]["empirical_universe_ref"]; risk=d02["source_scope"]["risk_set_ref"]; measure=d02["source_scope"]["measure_basis_ref"]
    root=ExactRef("EE_P2R6O_D02_AUTHORITY_INPUT",f"urn:rawlsing:prev3:p2r6o:d02-authority:sha256:{D02_BLOB.rjust(64,'0')[-64:]}",hashlib.sha256((D02+D02_BLOB).encode()).hexdigest())
    disc=DiscoveryAuthority(typed_state="EXACT_BOUNDED_AUTHORIZED",authority_snapshot_refs=(far,),dependency_refs=tuple(x.ref for x in primitives.values())+tuple(x.ref for x in queries.values()),producer_replay_locator_or_reference_root=root,
        candidate_grammar_ref=grammar_ref,candidate_universe_definition=definition,
        source_universe_scope={"allowed_universe_refs":[universe]},risk_set_scope={"allowed_risk_set_refs":[risk]},
        topology_scope={"maximum_conditioner_arity_K":3,"maximum_target_arity_J":2},
        measure_scope={"allowed_measure_kinds":["RAW"],"allowed_measure_basis_refs":[measure]},
        support_rules=d02["support_rules"],validation_rules={"rules":[x["validation"] for x in definition["rules"]]},
        coverage_claim="COMPLETE_FOR_EXACT_DECLARED_FRONTIER",pruning_contract={"kind":"NONE_EXACT_EVALUATE_ALL"},
        algorithm_identity_if_semantically_required=I05_CONTRACT_ID,tie_order_rules="CANONICAL_CANDIDATE_HASH_ORDER",rng_policy_if_any="NONE")
    refs={r.key:r for obj in (*primitives.values(),*queries.values()) for r in obj.authority_snapshot_refs}
    kinds={BASE_GRAMMAR:"PREDICATE_GRAMMAR",F02_GRAMMAR:"PREDICATE_GRAMMAR","5f671f2cf9342820026af287009d1d9220e3f9f29d92134582d77eeebbdcd638":"SOURCE_SEMANTICS_TOPOLOGY","703f629c5d2b66e1ea5fccfddec80130bbb9b2ea5f8f93c4f69ad5797158d89a":"ROUTING_RISK_SET","47142de560f66e725283aaf96024bfad06fb0b33eeb56e3c8cfdc8afcc745bc0":"SOURCE_SEMANTICS_TOPOLOGY","52e741a07b75c475254628dfdf191a77f969e0a7cd7bbdf9b7a90addf324d540":"ROUTING_RISK_SET","08a00dae22e08905b42b650125920653897c6a88b66682699932a31ccb230115":"DISCOVERY_FRONTIER"}
    snaps=[fs]+[closure_snapshot(r,kinds.get(r.authority_content_hash,"REPLAY_PROTOCOL")) for r in refs.values()]
    catalog=RuntimeObjectCatalog(authorities=tuple(snaps),predicates=tuple(primitives.values()),queries=tuple(queries.values()),discovery_authorities=(disc,))
    verified=_verify_discovery_authority(disc,catalog.authority_registry); atoms=_catalog_atoms(verified,catalog.predicates); templates=_catalog_templates(verified,catalog.queries); _validate_catalog_scope(disc,atoms,templates)
    runtime=r4_runtime()
    with bind_runtime(runtime):
        candidates=_compile_frontier(verified,atoms,templates)
    roles=sum(len(c.query_roles) for c in candidates)
    assert len(candidates)==50 and roles==77
    mixed=[c for c in candidates if c.rule_id in {"D02_P2_HIGHER_ORDER_K3","D02_P3_CONDITIONAL_REVERSAL"}]
    assert mixed
    mixed_auth="0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55"
    assert any(c.winning_predicate.grammar_authority_ref["authority_content_hash"]==mixed_auth for c in mixed)
    assert {k:v.content_hash for k,v in primitives.items() if k in F02_REFS}==F02_REFS
    assert {k:v.content_hash for k,v in primitives.items() if k in BASE_REFS}==BASE_REFS
    return catalog,candidates,primitives,queries,definition

def active_registry():
    reg=git_json(HQ_HANDOFF,REGISTRY)
    assert reg["snapshot_ref"]["content_hash"]==REGISTRY_HASH
    active=reg["identity_material"]["active_positive_bindings"]; assert len(active)==1 and active[0]["content_hash"]==ACTIVE_BINDING
    return reg

def require_one_active(reg):
    active=reg["identity_material"]["active_positive_bindings"]
    if len(active)!=1 or active[0]["content_hash"]!=ACTIVE_BINDING: raise Pre553AuthorityError("exact sole active a5f36 binding required")
    return active[0]


PUBLIC_KEYS=frozenset({
    "schema_id","schema_version","typed_state","authority_snapshot_refs",
    "dependency_refs","producer_replay_locator_or_reference_root",
    "semantic_fields","object_id","content_hash",
})

def _public(obj):
    raw=obj.as_dict()
    doc={k:raw[k] for k in PUBLIC_KEYS if k in raw}
    if frozenset(doc)!=PUBLIC_KEYS:
        raise RuntimeError("R6O canonical public preimage incomplete")
    return doc

def materialize_runtime_package():
    catalog,candidates,primitives,queries,definition=catalog_and_frontier()
    receipt=catalog.receipt()
    if receipt["catalog_identity"]!=I03_RUNTIME_CATALOG_IDENTITY:
        raise RuntimeError("adopted R6O runtime catalog identity drift")
    if len(candidates)!=50 or sum(len(c.query_roles) for c in candidates)!=77:
        raise RuntimeError("adopted LiTS 50/77 workload drift")
    logical_bindings=current_pre553_logical_candidate_bindings(
        candidates=candidates,
        primitives=primitives,
        queries=queries,
    )
    return {
        "schema":"EE_P2R6S_LITS_CURRENT_RUNTIME_PACKAGE@1.0.0",
        "runtime_catalog_identity":receipt["catalog_identity"],
        "active_binding":ACTIVE_BINDING,
        "runtime_release":RUNTIME_RELEASE,
        "authority_documents":[_public(x) for x in catalog.authorities],
        "predicate_documents":[_public(x) for x in catalog.predicates],
        "query_documents":[_public(x) for x in catalog.queries],
        "discovery_authority_documents":[_public(x) for x in catalog.discovery_authorities],
        "candidate_count":len(candidates),
        "query_role_executions":sum(len(c.query_roles) for c in candidates),
        "cross_schema_logical_candidate_bindings":[dict(x) for x in logical_bindings],
    }

def materialize_runtime_authority_set():
    return r4_runtime()

__all__=["materialize_runtime_package","materialize_runtime_authority_set"]
