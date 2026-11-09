"use strict";
const R4="d10602355c77564b2b6d50601ebba4fed4ac7d58",RB="c081eb73e7bd9523f0699769fedc68de2dafe7c0",AB="98df0d9642a3c3f5fa1ecbf7a9cf7251e32b9fa0";
const ALLOWED=new Set("ORIGINATED_AS PRESERVED_BY SHARPENED_BY CORRECTED_BY SPLIT_INTO COMPOSED_FROM SUPERSEDED_BY REJECTED_WITH_REASON ASSIGNED_TO REQUIRES_AUTHORITY SELECTS_RULE APPLIES_RULE PRODUCES CONSUMED_BY IF_CONDITION MUST_DEPENDENCY ALTERNATIVE_TO TESTED_BY HELD_BY STRANDED_ON BLOCKED_BY FALSIFIED_BY ALIAS_OF".split(" "));
const MAP={CANDIDATE_PRODUCER_EDGE__NOT_EXECUTION:"ASSIGNED_TO",DOCUMENTED_DEPENDENCY__FUNCTIONAL:"IF_CONDITION",DOCUMENTED_DEPENDENCY__OBSERVED:"ASSIGNED_TO",CROSS_GENERATION_TYPED_UNJOIN:"HELD_BY",SELF_STAGE_SOURCE_RETURN__NOT_SUCCESSION:"ASSIGNED_TO",CROSS_PRONG_CANDIDATE_UNJOIN__NOT_SUCCESSION:"HELD_BY",CANDIDATE_REQUIRED_FOR_SOROK_E001__OWNER_HELD:"HELD_BY",CANDIDATE_IMPLEMENTATION_LABEL__SOURCE_STATIC:"ASSIGNED_TO",STATIC_CALL_AT_SHA__NO_EXECUTION:"ASSIGNED_TO",HISTORICAL_E001_IDENTITY_TO_SOROK_RECIPIENT_CANDIDATE__OWNER_HELD:"ASSIGNED_TO"};
function ok(v,m){if(!v)throw Error(m)}
function parse(s,name){const l=s.trimEnd().split(/\r?\n/),h=l.shift().split("\t"),i=Object.fromEntries(h.map((k,j)=>[k,j]));const r=l.map((x,n)=>{const a=x.split("\t");ok(a.length===h.length,name+" invalid width "+(n+2));return a});return {h,i,r}}
function val(t,r,k){return r[t.i[k]]}
function index(t,k){ok(k in t.i,"missing field "+k);let m=new Map;for(const r of t.r){let v=val(t,r,k);ok(v&&!m.has(v),"duplicate/empty "+k+" "+v);m.set(v,r)}return m}
function normalize(t,condition){if(ALLOWED.has(t))return t;if(t==="DOCUMENTED_DEPENDENCY__ASTRA"){if(condition.startsWith("MUST :: "))return "MUST_DEPENDENCY";if(condition.startsWith("IF :: "))return "IF_CONDITION";throw Error("ASTRA conditional law altered")}ok(t in MAP,"R4 unexpected type "+t);return MAP[t]}
function verify(x){
 const a=parse(x.r4Relations,"R4 relations"),b=parse(x.r5Relations,"R5 relations"),m=parse(x.relationMigration,"D01 migration");
 ok(a.h.join("\t")===b.h.join("\t")&&a.r.length===8503&&b.r.length===8503&&m.r.length===4841,"D01 schema/count");
 const mi=index(m,"relation_id");let migrated=0,astIf=0,astMust=0;const ids=new Set,types=new Set;
 for(let n=0;n<a.r.length;n++){const q=a.r[n],r=b.r[n],id=val(a,q,"relation_id"),old=val(a,q,"relation_type"),newType=val(b,r,"relation_type"),condition=val(a,q,"applicability_or_condition");
  ok(!ids.has(id),"duplicate relation "+id);ids.add(id);types.add(old);ok(val(b,r,"relation_id")===id&&ALLOWED.has(newType)&&normalize(old,condition)===newType,"D01 type "+id);
  for(const k of a.h)if(k!=="relation_type")ok(val(a,q,k)===val(b,r,k),"D01 semantic field changed "+id+" "+k);
  if(old==="DOCUMENTED_DEPENDENCY__ASTRA"){if(newType==="IF_CONDITION")astIf++;else if(newType==="MUST_DEPENDENCY")astMust++}
  const record=mi.get(id);
  if(old!==newType){migrated++;ok(record&&val(m,record,"r4_relation_type")===old&&val(m,record,"canonical_relation_type")===newType,"D01 bad inverse "+id);ok(val(m,record,"immutable_r4_relation_blob")===RB&&val(m,record,"immutable_r4_author_head")===R4&&val(m,record,"reversal_rule")==="REPLACE_CANONICAL_TYPE_WITH_R4_TYPE_ONLY","D01 provenance "+id)}
  else ok(!record,"D01 spurious inverse "+id);
 }
 ok(migrated===4841&&mi.size===migrated&&[...types].filter(z=>!ALLOWED.has(z)).length===11&&astIf===26&&astMust===7,"D01 4841/11/MUST/IF proof");
 const oa=parse(x.r4Atlas,"R4 atlas"),na=parse(x.r5Atlas,"R5 atlas"),s=parse(x.seedDispositions,"D02 seed fates"),ev=index(parse(x.evidence,"EVIDENCE"),"evidence_id");
 ok(oa.h.join("\t")===na.h.join("\t")&&oa.r.length===1740&&na.r.length===1740&&s.r.length===73,"D02 seed/atlas widths");
 const om=index(oa,"record_id"),nm=index(na,"record_id"),sm=index(s,"seed_id"),rm=index(b,"relation_id");ok(om.size===nm.size,"D02 atlas ID conservation");
 let lmx=0,f29=0;for(const [id,q] of om){let r=nm.get(id),f=sm.get(id);ok(r,"D02 lost atlas node "+id);if(!f){ok(q.join("\t")===r.join("\t"),"D02 nonseed altered "+id);continue}
  const ns=val(oa,q,"namespace"),isL=ns==="LMX_INHERITED_OBLIGATION";ok(isL||ns==="C6_LEGACY_FUNCTION_CLASS","D02 not inherited seed "+id);
  const fam=isL?"LMX44":"C6_F29";ok(val(s,f,"seed_family")===fam,"D02 seed family "+id);if(isL)lmx++;else f29++;
  const changes=new Set(["pyat_owner_ids","completeness_grade","disposition","next_step"]);
  for(const k of oa.h)if(!changes.has(k))ok(val(oa,q,k)===val(na,r,k),"D02 inherited immutable field changed "+id+" "+k);
  const d=val(na,r,"disposition");ok(val(oa,q,"disposition")==="NOT_ASSESSED_CURRENT"&&d===val(s,f,"current_disposition")&&d.includes("CURRENT_")&&d.includes("OPEN"),"D02 current fate not honest "+id);
  ok(val(na,r,"completeness_grade")==="SOURCE_IDENTITY_AND_DOCUMENTARY_ALIAS_ONLY__CURRENT_SAME_GRAIN_OPEN","D02 false grade "+id);
  ok(val(na,r,"pyat_owner_ids")==="PYAT_HQ_OWNER_ROUTE_PROPOSED__NOT_RECEIVED"&&val(s,f,"current_owner_receipt")==="NOT_RECEIVED","D02 forged owner "+id);
  ok(val(na,r,"next_step")==="R5_SEED_FATE_LEDGER:"+id+"__OWNER_NOT_RECEIVED__PROOF_REQUIRED","D02 finite next step "+id);
  ok(val(s,f,"same_grain_current_successor")==="NO_PROOF"&&val(s,f,"actual_non_test_first_reader")==="UNRESOLVED"&&val(s,f,"applied_rule_effect")==="NO_PROOF"&&val(s,f,"enforced_refusal")==="NO_PROOF","D02 false ready "+id);
  ok(val(s,f,"inherited_source_locator")===val(oa,q,"source")&&val(s,f,"source_author_head")===R4,"D02 source cut "+id);
  let cand=rm.get(val(s,f,"documentary_candidate_relation"));ok(cand&&val(b,cand,"from_id")===val(s,f,"documentary_candidate_finding")&&val(b,cand,"to_id")===id,"D02 exact candidate "+id);
  ok(val(b,cand,"relation_type")==="ASSIGNED_TO"&&val(b,cand,"grade")==="EXACT_LABEL_MATCH__NO_EQUIVALENCE","D02 alias promoted "+id);
  const evId=val(s,f,"documentary_evidence_id");ok(ev.has(evId)&&val(b,cand,"evidence_id")===evId,"D02 fake evidence "+id);
  ok(val(s,f,"finite_next_action").includes(id)&&val(s,f,"case_specific_falsifier").includes(id),"D02 not finite "+id);
 }
 ok(lmx===44&&f29===29&&sm.size===73,"D02 44/29 conservation");
 return {relations:8503,migrated:4841,originalExceptionalTypes:11,ASTRA_MUST:astMust,ASTRA_IF:astIf,seedLMX:lmx,seedC6F:f29,seedFates:73,newLostFunctions:0};
}
function hostile(x){
 const tests=[
 ["illegal type",y=>y.r5Relations=y.r5Relations.replace("\tASSIGNED_TO\t","\tUNAUTHORIZED\t")],
 ["IF to MUST",y=>y.r5Relations=y.r5Relations.replace("\tIF_CONDITION\t","\tMUST_DEPENDENCY\t")],
 ["MUST to IF",y=>y.r5Relations=y.r5Relations.replace("\tMUST_DEPENDENCY\t","\tIF_CONDITION\t")],
 ["unlogged edge",y=>{let l=y.relationMigration.trimEnd().split("\n");l.splice(1,1);y.relationMigration=l.join("\n")+"\n"}],
 ["forged original type",y=>y.relationMigration=y.relationMigration.replace("CANDIDATE_PRODUCER_EDGE__NOT_EXECUTION","EXECUTED_OPERATION")],
 ["negative turned positive",y=>y.r5Relations=y.r5Relations.replace("NO_NON_TEST_FIRST_READER_PROVED","NON_TEST_FIRST_READER_PROVED")],
 ["condition erased",y=>y.r5Relations=y.r5Relations.replace("IF :: Current authority for this scope is not already competently bound.","MUST :: always within selected node scope")],
 ["seed false current",y=>y.r5Atlas=y.r5Atlas.replace("HISTORICAL_PRESERVATION_DOCUMENTED__CURRENT_SUCCESSOR_PROOF_OPEN","PROVED_CURRENT_SUCCESSOR")],
 ["owner forged",y=>y.r5Atlas=y.r5Atlas.replace("PYAT_HQ_OWNER_ROUTE_PROPOSED__NOT_RECEIVED","PYAT_OWNER_ADOPTED")],
 ["seed dropped",y=>{let l=y.seedDispositions.trimEnd().split("\n");l.splice(1,1);y.seedDispositions=l.join("\n")+"\n"}],
 ["candidate evidence forged",y=>y.seedDispositions=y.seedDispositions.replace("J-EV-ZL08-ZL08-E-ZL01-000001","J-EV-FAKE_SOURCE")],
 ["original source tampered",y=>y.r5Atlas=y.r5Atlas.replace("bb0814fa39de335558a11fec2b9d085e68216c9a","NOT_REAL_SOURCE")]
 ];let pass=0;for(const [label,fn] of tests){const y={...x};fn(y);let caught=false;try{verify(y)}catch(e){caught=true}ok(caught,"unrejected negative mutation "+label);pass++}return pass;
}

if(require.main===module){
 const fs=require("fs"),cp=require("child_process"),crypto=require("crypto"),path=require("path");
 const B="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N020_LONG_MEMORY/VMESTYE/";
 const gitTop=cp.execFileSync("git",["rev-parse","--show-toplevel"],{encoding:"utf8"}).trim();
 const read=p=>fs.readFileSync(path.join(gitTop,B+p),"utf8");
 const show=p=>cp.execFileSync("git",["show",R4+":"+B+p],{encoding:"utf8",maxBuffer:25*1024*1024});
 const hash=s=>crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+Buffer.byteLength(s)+"\0"),Buffer.from(s)])).digest("hex");
 const oldRel=show("DATA/RELATIONS.tsv"),oldAtlas=show("DATA/FUNCTION_ATLAS.tsv");
 ok(hash(oldRel)===RB&&hash(oldAtlas)===AB,"R4 immutable provenance mismatch");
 const input={r4Relations:oldRel,r4Atlas:oldAtlas,r5Relations:read("DATA/RELATIONS.tsv"),r5Atlas:read("DATA/FUNCTION_ATLAS.tsv"),relationMigration:read("PRONGS/J_JOIN/RELATION_TYPE_MIGRATION_R5.tsv"),seedDispositions:read("PRONGS/J_JOIN/SEED_CURRENT_DISPOSITIONS_R5.tsv"),evidence:read("DATA/EVIDENCE.tsv")};
 const result=verify(input),rejected=hostile(input);
 console.log(JSON.stringify({court:"S0_S1_DOCUMENTARY_ONLY",...result,negativeMutationsRejected:rejected,native_S2_S3:"NOT_RUN",science_source_actor_rights:"NOT_GRANTED"},null,2));
}
module.exports={verify,hostile};
