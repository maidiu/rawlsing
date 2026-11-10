#!/usr/bin/env node
// VMC-T1 R4 S0-S1 documentary validator. No original-source Python or respondent data execution.
// Usage: node validate_vmc_t1_r3.mjs --self-test --require-source
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
const HERE=path.dirname(fileURLToPath(import.meta.url));
const REL="WORKER_RETURNS/VMESTYE_VMC_T1_TRANSFORM_CONTRACTS_R1/";
const R2="627660cfca3e638b793c9e6369ab3ea314c9018b";
const R1="0a0172960596f53125ee93e2698d15c7aa3db8eb";
const C6="aed1a0ae13c58f11f4dabd07c818b62f72adf989";
const C6PATH="WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv";
function parseTsv(raw){
 const lines=raw.replace(/\r/g,"").trimEnd().split("\n"),cols=lines.shift().split("\t");
 return lines.map(line=>{const fields=line.split("\t"),r={};cols.forEach((col,i)=>r[col]=fields[i]||"");return r});
}
function fromFile(file){return parseTsv(fs.readFileSync(path.join(HERE,file),"utf8"));}
const base={
 contracts:fromFile("HISTORICAL_TRANSFORM_CONTRACTS.tsv"),
 ledger:fromFile("SOURCE_RECORD_TO_TRANSFORM.tsv"),
 r1fates:fromFile("R1_CANDIDATE_FATES.tsv"),
 c6:fromFile("C6_SELECTED_AUTHORITY_EVIDENCE.tsv"),
 obligations:fromFile("INHERITED_OBLIGATION_FATES.tsv"),
 finite:fromFile("FINITE_ESTATE_DELTA.tsv")
};

const audit = function audit(d){
 const err=[],check=(name,pred,note)=>{if(!pred&&err.length<100)err.push(name+": "+note)};
 const unique=a=>new Set(a).size===a.length;
 const [cs,ls,fs,ars,os,ds]=[d.contracts,d.ledger,d.r1fates,d.c6,d.obligations,d.finite];
 const C=new Map(cs.map(x=>[x.transform_id,x])), L=new Map(ls.map(x=>[x.source_record_key,x])), A=new Map(ars.map(x=>[x.ID,x])), O=new Map(os.map(x=>[x.identity,x]));
 check("CONTRACTS_52",cs.length===52&&unique(cs.map(x=>x.transform_id)),String(cs.length));
 check("FROZEN_10348",ls.length===10348&&unique(ls.map(x=>x.source_record_key)),String(ls.length));
 check("R1_FATES_235",fs.length===235&&unique(fs.map(x=>x.r1_id)),String(fs.length));
 check("C6_29_58_94",ars.length===94&&ars.filter(x=>x.ROW_TYPE==="FUNCTION").length===29&&ars.filter(x=>x.ROW_TYPE==="RELEASE").length===58,"denominators");
 check("LONG_MEMORY_44_30",os.length===74&&unique(os.map(x=>x.identity))&&os.filter(x=>x.identity.startsWith("LMX-")).length===44&&os.filter(x=>x.identity.startsWith("LMQ-")).length===30,"denominators");
 check("FINITE_27_WITH_SIX_R4",ds.length===27&&unique(ds.map(x=>x.delta_id))&&ds.filter(x=>/^D2[2-7]_/.test(x.delta_id)).length===6,"R3 21 plus six decision-changing R4 questions");
 for(const delta of ds)check("FINITE_OWNED_FALSIFIABLE_STOPPED",!!delta.source_identity&&!!delta.method&&!!delta.grade&&!!delta.owner&&!!delta.earliest_falsifier&&!!delta.consequence&&!!delta.stop_rule,delta.delta_id);
 for(const delta of ds.filter(x=>/^D2[2-7]_/.test(x.delta_id)))check("R4_FINITE_EXACT_CODE_ANCHOR",delta.source_identity.startsWith("9253064bc9423a0f0ccda4fbdea43c2f54f800c6::data/ddm_build_copy/")&&/^[0-9a-f]{40}$/.test(delta.source_blob_sha),delta.delta_id);
 const byT=new Map(cs.map(x=>[x.transform_id,[]]));
 for(const l of ls){
  check("LEDGER_GRADE_CUT",!!l.source_cut&&!!l.exact_source_identity&&!!l.owner&&!!l.falsifier&&!!l.source_grade,l.source_record_key);
  for(const id of (l.transform_ids||"").split(";").filter(Boolean)){check("DANGLING_LINK",C.has(id),l.source_record_key+":"+id);if(byT.has(id))byT.get(id).push(l.source_record_key)}
 }
 for(const c of cs){
  const keys=byT.get(c.transform_id)||[];
  check("INVERSE_EXISTS",keys.length>0,c.transform_id);
  check("INVERSE_COUNT",Number(c.frozen_witness_total)===keys.length,c.transform_id);
  const explicit=(c.frozen_witness_source_record_keys||"").split(";").filter(Boolean);
  check("WITNESSES_INCLUDED",explicit.length>0,c.transform_id);
  for(const k of explicit)check("WITNESS_BIDIRECTIONAL",L.has(k)&&(L.get(k).transform_ids||"").split(";").includes(c.transform_id),c.transform_id+":"+k);
  check("FALSE_ALIAS",(!/(ZL06[-:]T0(03|04|29|30)|F15_V551_COND)/.test(c.source_ids_and_aliases||"") || c.transform_id==="T1R2-F15-CONDITIONAL-STATE"),c.transform_id);
  const blob=c.immutable_evidence.match(/blob=([0-9a-f]{40})/);
  if(blob)check("CODE_PIN",c.source_ids_and_aliases.startsWith("CODE_BODY:"+blob[1]+"::")&&c.source_relation_grade.includes("STATIC_CODE_BODY"),c.transform_id);
  else check("REPORT_NOT_CODE_ALIAS",c.source_ids_and_aliases.startsWith("C6_REPORTED_FUNCTION:")||c.source_ids_and_aliases==="NO_C6_FUNCTION_IDENTITY_CLAIMED",c.transform_id);
  check("CONTEXT_GRADED",!!c.r2_prior_mixed_refs_not_semantic_aliases&&!!c.corrected_alias_disposition,c.transform_id);
  const id=c.c6_direct_function_id,ar=A.get(id);
  check("VALID_DIRECT_C6",id==="NO_DIRECT_C6_F"||!!ar&&ar.ROW_TYPE==="FUNCTION",c.transform_id+":"+id);
  if(ar&&ar.ROW_TYPE==="FUNCTION"){
    for(const [field,col,fallback] of [
    ["c6_selected_release_ids","SELECTED_RELEASE_IDS","NONE_SELECTED_OR_UNPROVED"],
    ["c6_unresolved_release_ids","UNRESOLVED_RELEASE_IDS","NONE_REPORTED"],
    ["c6_exact_selected_sha256_or_set","SELECTED_SHA256_OR_SET","NO_SELECTED_SHA_REPORTED"],
    ["c6_selected_version_or_document","SELECTED_VERSION_OR_DOCUMENT","NO_SELECTED_VERSION_REPORTED"],
    ["c6_selection_rule_and_scope","ROW_RULE_OR_SELECTION_LAW","NO_C6_RULE_ESTABLISHED_FOR_CONTRACT"],
    ["c6_selected_release_status","RELEASE_SELECTION_STATUS","NO_C6_FUNCTION_RELEASE_ROW"],
    ["c6_selected_release_grade","GRADE","NO_C6_PROOF_GRADE"]])
      check("C6_FIELD",c[field]===(ar[col]||fallback),c.transform_id+":"+field);
  }
  check("C6_CUT",c.c6_exact_ledger_blob==="ba39d8f9c9f06440df5d068bdd9f0b857c06ce58",c.transform_id);
  check("NOT_INVOKED",c.c6_original_observed_invocation==="NOT_OBSERVED__C6_REPORT_SELECTED_RELEASE_IS_NOT_ORIGINAL_CALL",c.transform_id);
 }
 const f03=cs.filter(x=>x.transform_id.startsWith("T1R2-F03-")),f08=cs.filter(x=>x.transform_id.startsWith("T1R2-F08-"));
 check("F03_FOUR_GUARDS",f03.length===4&&f03.every(x=>x.c6_direct_function_id==="F03_QREL"&&x.c6_selected_release_ids==="AR-0005;AR-0006"),"F03");
 check("F08_FOUR_RELEASES",f08.length===3&&f08.every(x=>x.c6_direct_function_id==="F08_Q_USE"&&x.c6_selected_release_ids==="AR-0047;AR-0048;AR-0049;AR-0050"),"F08");
 const adj=C.get("T1R2-V551-ADJUDICATE"),cov=C.get("T1R2-V551-COVERAGE");
 check("F15_SEPARATION",adj&&adj.c6_direct_function_id==="F14_V551_ATOMS"&&adj.corrected_alias_disposition.includes("REMOVED_FALSE_F15")&&C.has("T1R2-F15-CONDITIONAL-STATE"),"F15");
 check("V551_COVERAGE_PIN",cov&&cov.source_ids_and_aliases.includes("ddm_v551_atoms.py#L160-L166")&&(byT.get(cov.transform_id)||[]).length>=1,"coverage");
 check("C11_DISTINCT",L.get("ZL06:OPERATION_TRACES:ZL06-T029")?.transform_ids===""&&L.get("ZL06:OPERATION_TRACES:ZL06-T030")?.transform_ids==="","C11");
 const sel=ars.filter(x=>x.ROW_TYPE==="FUNCTION").flatMap(x=>[...(x.SELECTED_SHA256_OR_SET||"").matchAll(/AR-\d{4}:([0-9a-f]{64})/g)].map(m=>m[1]));
 check("SELECTED_34_UNIQUE_52_USES",sel.length===52&&new Set(sel).size===34,String(sel.length));
 check("C6_PIN_94",ars.every(x=>x.C6_CUT==="aed1a0ae13c58f11f4dabd07c818b62f72adf989"&&x.C6_BLOB==="ba39d8f9c9f06440df5d068bdd9f0b857c06ce58"),"C6");
 check("C6_NOT_INVOKED_94",ars.every(x=>x.ORIGINAL_INVOKED_RULE_EFFECT==="NOT_OBSERVED__STATIC_SELECTED_RELEASE_REPORT_ONLY"&&x.CURRENT_INVOCATION==="NOT_PROVED_NO_NATIVE_EXECUTION"),"C6");
 const no=fs.filter(x=>x.r3_candidate_contract_refs==="NONE__NOT_PROMOTED");
 check("R1_148_UNLINKED_EXPLICIT",no.length===148,String(no.length));
 for(const f of fs){
  check("R1_ROW_REASON",f.r3_reason.length>=75&&!!f.r1_source_cut_or_locator&&!!f.r1_source_grade&&!!f.r3_row_specific_subject&&!!f.r1_falsifier&&!!f.r3_owner_referral,f.r1_id);
  check("NO_UNJUSTIFIED_RETIREMENT",f.r3_disposition==="PRESERVE__NOT_RETIRE__NO_ZERO_LOSS_CLAIM"&&!/LAWFULLY_RETIRED|PROVEN_ABSENT/.test(f.r3_fate_class),f.r1_id);
  for(const id of f.r3_candidate_contract_refs.split(";").filter(x=>x!=="NONE__NOT_PROMOTED"&&x))check("R1_TARGET_VALID",C.has(id),f.r1_id+":"+id);
 }
 for(const o of os){check("OBLIGATION_SOURCE",L.has(o.source_record_key)&&!!o.original_label&&!!o.first_falsifier&&!!o.first_consumer_or_referral&&!!o.required_rule_or_refusal,o.identity);check("OBLIGATION_NOT_EXECUTED",o.execution_status==="NOT_RUN_NO_SAME_GRAIN_NATIVE_PROOF",o.identity)}
 const a43=O.get("LMX-043");
 check("LMX043_ATOMIC_ROLLBACK_REPLAY",!!a43&&/ATOMIC/.test(a43.required_rule_or_refusal)&&/ROLLBACK/.test(a43.required_rule_or_refusal)&&/REPLAY/.test(a43.required_rule_or_refusal)&&a43.before_state.includes("STAGED"),"LMX-043");

 // Source-challenge semantic sentinels: pin the seven corrected distinctions.
 // These check the returned representation; the accepted original code body must still be read separately.
 const claim=id=>C.get(id)||{};
 check("F08_CONFLICT_IS_EXCEPTION",claim("T1R2-F08-DUPLICATE-REFUSE").semantic_delta?.includes("Raise RuntimeError")&&claim("T1R2-F08-DUPLICATE-REFUSE").output_guarantee?.includes("no emitted conflict/review artifact"),"selector raises, not durable review");
 check("V549B_LITERAL_BINARY_ONLY",claim("T1R2-V549B-PRESENCE").semantic_delta?.includes("Textual 'present'/'absent' do not")&&claim("T1R2-V549B-PRESENCE").negative_refusal?.includes("remains unanchored"),"only numeric-string 1 and 0 anchor");
 check("V551_NEUTRAL_SHORT_CIRCUIT",claim("T1R2-V551-SIGNED-PROJECTION").guard_rule_predicate?.includes("neutral direction short-circuits")&&claim("T1R2-V551-SIGNED-PROJECTION").negative_refusal?.includes("neutral bypasses"),"no geometry claim for neutral");
 check("V551_PREFILTER_NOT_REPAIR_DEBT",claim("T1R2-V551-ADJUDICATE").negative_refusal?.includes("omitted, not automatically logged")&&claim("T1R2-V551-ADJUDICATE").guard_rule_predicate?.includes("10 explicit row predicates"),"candidate prefilter separate");
 check("V552_PARTIAL_CAN_SCORE",claim("T1R2-V552-PRESSURE").guard_rule_predicate?.includes("still permits a score")&&claim("T1R2-V552-PRESSURE").output_guarantee?.includes("pressure_measure_class stays conditional"),"partial selected coverage not automatically DENY");
 check("V551J_TARGET_GATE_FALLBACK",claim("T1R2-V551J-CERTIFY").guard_rule_predicate?.includes("registry_resolved_share>0")&&claim("T1R2-V551J-CERTIFY").semantic_invariants?.includes("do not infer every component"),"target resolution not necessarily per component");
 check("V552J_PARTIAL_AND_TIE",claim("T1R2-V552J-EXACT-JOIN").guard_rule_predicate?.includes("score >=5")&&claim("T1R2-V552J-EXACT-JOIN").negative_refusal?.includes("ties at accepted score are not rejected"),"exact scope not full semantic equivalence");

 const staticMatches={
 "T1-F03-DIRECTIONAL":"T1R2-F03-DIRECTIONAL",
 "T1-F03-PRESENT-NONDIRECTIONAL":"T1R2-F03-NONDIRECTIONAL",
 "T1-F03-NOMATCH-QUC-PRESERVE":"T1R2-F03-NOMATCH-KEEP",
 "T1-F03-NOMATCH-REFUSE":"T1R2-F03-NOMATCH-DENY",
 "T1-F08-SPECIFICITY":"T1R2-F08-SELECT",
 "T1-F08-ROLE-NOT-PERMISSION":"T1R2-F08-ROLE-PERMISSION",
 "T1-F08-CONFLICT-REFUSE":"T1R2-F08-DUPLICATE-REFUSE"};
 for(const f of fs){
  check("R1_STRICT_BRANCH_GRADE",f.r3_strict_same_static_branch===(staticMatches[f.r1_id]||"NONE__SAME_GRAIN_NOT_PROVED"),f.r1_id);
  check("R1_ROW_SPECIFIC_REASON",f.r3_reason.includes(f.r3_row_specific_subject.slice(0,Math.min(100,f.r3_row_specific_subject.length)))&&f.r3_reason.includes("Earliest source/consumer falsifier:"),f.r1_id);
 }
 return err;
};

function clone(x){return JSON.parse(JSON.stringify(x));}
const muts=[
 ["FALSE_ALIAS_T029",d=>d.contracts.find(x=>x.transform_id==="T1R2-V551-ATOM").source_ids_and_aliases="ZL06-T029"],
 ["FALSE_ALIAS_T030",d=>d.contracts.find(x=>x.transform_id==="T1R2-V552-PRESSURE").source_ids_and_aliases="ZL06-T030"],
 ["F15_FALSE_EQUIVALENCE",d=>d.contracts.find(x=>x.transform_id==="T1R2-V551-ADJUDICATE").c6_direct_function_id="F15_V551_COND"],
 ["MISSING_COVERAGE_INVERSE",d=>d.ledger.forEach(x=>x.transform_ids=x.transform_ids.split(";").filter(y=>y!=="T1R2-V551-COVERAGE").join(";"))],
 ["C6_SELECTED_SHA_TAMPER",d=>d.contracts.find(x=>x.transform_id==="T1R2-F03-DIRECTIONAL").c6_exact_selected_sha256_or_set="AR-0005:0000"],
 ["C6_SOURCE_GRADE_TAMPER",d=>d.contracts.find(x=>x.transform_id==="T1R2-F08-SELECT").c6_selected_release_grade="PROVEN_RUNTIME"],
 ["ORIGINAL_INVOCATION_PROMOTION",d=>d.contracts[0].c6_original_observed_invocation="OBSERVED_NATIVE_PRODUCTION"],
 ["R1_UNLINKED_DROP",d=>d.r1fates.splice(d.r1fates.findIndex(x=>x.r3_candidate_contract_refs==="NONE__NOT_PROMOTED"),1)],
 ["R1_FALSE_RETIREMENT",d=>d.r1fates[12].r3_disposition="RETIRED"],
 ["LMX043_ROLLBACK_ERASURE",d=>d.obligations.find(x=>x.identity==="LMX-043").required_rule_or_refusal="ATOMIC_ONLY"],
 ["LMQ_RESOURCE_DROP",d=>d.obligations.splice(d.obligations.findIndex(x=>x.identity==="LMQ-030"),1)],
 ["LEDGER_KEY_DUPLICATE",d=>d.ledger[10].source_record_key=d.ledger[11].source_record_key],
 ["LEDGER_KEY_DELETE",d=>d.ledger.splice(10,1)],
 ["CODE_PIN_TAMPER",d=>d.contracts.find(x=>x.transform_id==="T1R2-V551-COVERAGE").source_ids_and_aliases="CODE_BODY:0000000000000000000000000000000000000000::data/ddm_build_copy/ddm_v551_atoms.py#L160-L166"],
 ["C6_SELECTED_ROW_TAMPER",d=>d.c6.find(x=>x.ID==="F03_QREL").SELECTED_SHA256_OR_SET="AR-0005:"+("0".repeat(64))+";AR-0006:"+("f".repeat(64))],
 ["MISSING_EXPLICIT_WITNESS",d=>d.contracts[0].frozen_witness_source_record_keys="BOGUS:KEY"],
 ["F08_CONFLICT_AS_REVIEW_ARTIFACT",d=>d.contracts.find(x=>x.transform_id==="T1R2-F08-DUPLICATE-REFUSE").output_guarantee="typed manual review row emitted"],
 ["V549B_FALSE_TEXTUAL_NORMALIZATION",d=>d.contracts.find(x=>x.transform_id==="T1R2-V549B-PRESENCE").semantic_delta="Textual present and absent both become anchors"],
 ["V551_NEUTRAL_FALSE_GEOMETRY",d=>d.contracts.find(x=>x.transform_id==="T1R2-V551-SIGNED-PROJECTION").guard_rule_predicate="Every neutral and nonneutral response requires valid geometry"],
 ["V551_PREFILTER_FALSE_DEBT",d=>d.contracts.find(x=>x.transform_id==="T1R2-V551-ADJUDICATE").negative_refusal="Every excluded raw input is registered as repair debt"],
 ["V552_PARTIAL_FALSE_DENY",d=>d.contracts.find(x=>x.transform_id==="T1R2-V552-PRESSURE").guard_rule_predicate="All partially covered selected response surfaces DENY scoring"],
 ["V551J_TARGET_FALSE_ALL_COMPONENT",d=>d.contracts.find(x=>x.transform_id==="T1R2-V551J-CERTIFY").semantic_invariants="Every component independently target certified"],
 ["V552J_TIE_FALSE_REFUSAL",d=>d.contracts.find(x=>x.transform_id==="T1R2-V552J-EXACT-JOIN").negative_refusal="Any tie is always a hard refusal"],
 ["FINITE_R4_DECISION_DROP",d=>d.finite.splice(d.finite.findIndex(x=>x.delta_id.startsWith("D25_")),1)],
 ["FINITE_R4_STOP_ERASURE",d=>d.finite.find(x=>x.delta_id.startsWith("D27_")).stop_rule=""]
];
function sourceCutCheck(requireSource){
 let repoRoot;
 try{repoRoot=execFileSync("git",["rev-parse","--show-toplevel"],{cwd:HERE,encoding:"utf8"}).trim()}
 catch(e){if(requireSource)throw Error("Git clone unavailable: required original-cut comparison NOT_RUN");return ["SOURCE_CUT_REPLAY_NOT_RUN__NO_LOCAL_GIT"]}
 const show=(sha,filename)=>parseTsv(execFileSync("git",["show",sha+":"+filename],{cwd:repoRoot,encoding:"utf8",maxBuffer:25000000}));
 let oldR2,oldR1,oldC6;
 try{
   oldR2=show(R2,REL+"SOURCE_RECORD_TO_TRANSFORM.tsv");
   oldR1=show(R1,REL+"HISTORICAL_TRANSFORM_CONTRACTS.tsv");
   oldC6=show(C6,C6PATH);
 }catch(e){if(requireSource)throw Error("Pinned Git sources not accessible; fetch exact historical commits before source-cut PASS: "+e.message);return ["SOURCE_CUT_REPLAY_NOT_RUN__PINNED_GIT_COMMIT_UNFETCHED"]}
 const errors=[];
 const prev=new Map(oldR2.map(x=>[x.source_record_key,x]));
 if(prev.size!==10348)errors.push("R2 source identity denominator incorrect");
 for(const x of base.ledger){
  const y=prev.get(x.source_record_key);
  if(!y || ["source_class","source_cut","exact_source_identity","reported_function_authority_labels","owner","falsifier"].some(k=>x[k]!==y[k]))
    errors.push("SOURCE_IDENTITY_DRIFT:"+x.source_record_key);
 }
 const r1=new Map(oldR1.map(x=>[x.transform_id,x]));
 if(r1.size!==235)errors.push("R1 235 identity denominator incorrect");
 const fields=[["r1_owner","owner_prong"],["r1_contract_kind","contract_kind"],["r1_generation","historical_generation"],["r1_source_ids","source_ids_and_aliases"],["r1_source_cut_or_locator","immutable_evidence"],["r1_source_grade","source_grade"],["r1_input_state","input_data_state"],["r1_claimed_change","semantic_delta"],["r1_output","output_guarantee"],["r1_negative","negative_refusal"],["r1_claimed_first_consumer","next_consumer"],["r1_falsifier","earliest_falsifier"]];
 for(const x of base.r1fates){const y=r1.get(x.r1_id);if(!y||fields.some(([a,b])=>x[a]!==y[b]))errors.push("R1_FATE_SOURCE_DRIFT:"+x.r1_id)}
 if(oldC6.length!==94)errors.push("C6 original source denominator incorrect");
 const c6map=new Map(oldC6.map(x=>[x.ID,x]));
 for(const x of base.c6){const y=c6map.get(x.ID);if(!y||Object.keys(y).some(k=>x[k]!==y[k]))errors.push("C6_SELECTED_SOURCE_DRIFT:"+x.ID)}
 return errors;
}
const baseline=audit(base);
const requestedSelfTest=process.argv.includes("--self-test");
const requireSource=process.argv.includes("--require-source");
let sourceIssues=[];try{sourceIssues=sourceCutCheck(requireSource)}catch(e){sourceIssues=[e.message]}
const mutationOut=requestedSelfTest?muts.map(([name,f])=>{const d=clone(base);f(d);const errors=audit(d);return {name,rejected:errors.length>0,first_error:errors[0]||"NO_REJECTION"}}):[];
const fullIssues=baseline.concat(sourceIssues.filter(x=>!x.startsWith("SOURCE_CUT_REPLAY_NOT_RUN")));
if(mutationOut.some(x=>!x.rejected))fullIssues.push("NEGATIVE_CONTROL_ACCEPTED");
const out={status:fullIssues.length?"FAIL_OR_HOLD":"PASS_S0_S1_DOCUMENTARY_ONLY",scope:"NO_PYTHON_NO_SOURCE_NATIVE_NO_S2_S3_NO_ACCEPTANCE",counts:{contracts:base.contracts.length,ledger:base.ledger.length,r1fates:base.r1fates.length,c6:base.c6.length,obligations:base.obligations.length,finite:base.finite.length},baseline_issues:baseline,source_cut_evidence:sourceIssues.length?sourceIssues:["EXACT_R2_R1_C6_GIT_SOURCE_CUTS_MATCHED"],negative_controls:mutationOut};
console.log(JSON.stringify(out,null,2));
if(fullIssues.length)process.exitCode=1;
