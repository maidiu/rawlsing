// P05 SOURCE-FREE ROSTER->INDEPENDENT-E->DECLARED->BATCH/RESULT HOSTILE
// This is Node-compatible JS. Only simulated instrument, issuer and custody.
// Run: node WORKER_RETURNS/PYAT-HQ282-P05-ORIGINAL-ROSTER-INDEPENDENT-E-R1/repro/p05_original_to_e_hostiles.mjs
const ALL35=["Afrobarometer::R1","Afrobarometer::R5","Afrobarometer::R9","Arab Barometer::I","Arab Barometer::II","Arab Barometer::V","Arab Barometer::VIII","Asian Barometer::W1","Asian Barometer::W4","Asian Barometer::W5","EVS::1981","EVS::1990","EVS::1999","EVS::2008","EVS::2017","GSS::1972","GSS::1973","GSS::1984","GSS::1993","GSS::2002","GSS::2010","GSS::2016","GSS::2024","Latinobarómetro::1995","Latinobarómetro::2011","Latinobarómetro::2024","LiTS::2006","LiTS::II","LiTS::III","LiTS::IV","South Asia::W1","South Asia::W2","WVS::W1","WVS::W4","WVS::W7"];
const clone=x=>JSON.parse(JSON.stringify(x));
const key=(q,itemMap)=>JSON.stringify(["E@P05_F1",q.opid,q.family,q.wave,q.form,q.risk,q.route,q.target,q.condition_order,q.response_topology,q.measure_kind,q.design_ref,q.estimand_ref,q.respondent_relation,q.items.map(id=>{const x=itemMap[id];return x?[x.id,x.instrument_edition,x.language,x.form,x.slot,x.occurrence,x.person_unit,x.source_release,x.asked_route]:["ITEM_NOT_IN_NATIVE_ROSTER",id]})]);
function fixture(){
 const mk=(id,slot,form="F1",person="ADULT_1",asked="ASKED_IN_FORM")=>({id,instrument_edition:"SYNTHETIC_FIELD_INSTRUMENT_V1",language:"xx-fixture",form,slot,occurrence:"O1",person_unit:person,source_release:"FIXTURE_BYTE_ROOT_A",asked_route:asked});
 const items=[mk("A","Q-A"),mk("B","Q-B"),mk("J1","Q-J1","F2"),mk("J2","Q-J2","F2"),mk("H","Q-HELD","F3","ADULT_UNKNOWN","ROUTING_UNKNOWN"),mk("N","Q-NA","F4","NO_EXPOSURE","PROVED_NOT_FIELDED")];
 const ops=[
  {opid:"A_U_RAW",items:["A"],family:"FIXTURE",wave:"S1",form:"F1",risk:"RISK_A",route:"ASKED_A",target:"A",condition_order:[],response_topology:"SCALAR",measure_kind:"RAW",design_ref:"RAW_SAMPLE_ONLY",estimand_ref:"SAMPLE_DISTRIBUTION",respondent_relation:"SINGLE",state:"PERMITTED_EXACT_GRAIN",owner:"I03"},
  {opid:"B_U_RAW",items:["B"],family:"FIXTURE",wave:"S1",form:"F1",risk:"RISK_B",route:"ASKED_B",target:"B",condition_order:[],response_topology:"SCALAR",measure_kind:"RAW",design_ref:"RAW_SAMPLE_ONLY",estimand_ref:"SAMPLE_DISTRIBUTION",respondent_relation:"SINGLE",state:"PERMITTED_EXACT_GRAIN",owner:"I03"},
  {opid:"A_TO_B_CONDITION",items:["A","B"],family:"FIXTURE",wave:"S1",form:"F1",risk:"RISK_B_GIVEN_A",route:"ASKED_B_AND_A",target:"B",condition_order:["A"],response_topology:"CONDITIONAL",measure_kind:"RAW",design_ref:"RAW_SAMPLE_ONLY",estimand_ref:"CONDITIONAL_SAMPLE",respondent_relation:"SAME_PERSON_ISSUED_FIXTURE",state:"PERMITTED_EXACT_GRAIN",owner:"I03"},
  {opid:"JONLY_PAIR",items:["J1","J2"],family:"FIXTURE",wave:"S1",form:"F2",risk:"RISK_J12",route:"ASKED_J_FORM",target:"J2",condition_order:["J1"],response_topology:"J_ONLY_SAME_PERSON",measure_kind:"RAW",design_ref:"RAW_SAMPLE_ONLY",estimand_ref:"JOINT_SAMPLE",respondent_relation:"SAME_PERSON_ISSUED_FIXTURE",state:"PERMITTED_EXACT_GRAIN",owner:"I05"},
  {opid:"H_ROUTE_HOLD",items:["H"],family:"FIXTURE",wave:"S1",form:"F3",risk:"RISK_UNKNOWN",route:"UNKNOWN",target:"H",condition_order:[],response_topology:"SCALAR",measure_kind:"RAW",design_ref:"RAW_SAMPLE_ONLY",estimand_ref:"SAMPLE_DISTRIBUTION",respondent_relation:"UNKNOWN",state:"HELD",owner:"I03"},
  {opid:"N_PROVED_INTRINSIC",items:["N"],family:"FIXTURE",wave:"S1",form:"F4",risk:"NO_EXPOSURE",route:"PROVED_NOT_FIELDED",target:"N",condition_order:[],response_topology:"SCALAR",measure_kind:"RAW",design_ref:"RAW_SAMPLE_ONLY",estimand_ref:"SAMPLE_DISTRIBUTION",respondent_relation:"NOT_EXPOSED",state:"SOURCE_INTRINSIC_NA_PROVED",warrant:"FIXTURE_NOT_FIELDED_EVIDENCE_ONLY",owner:"I03"}
 ];
 const map=Object.fromEntries(items.map(x=>[x.id,x]));
 const e=ops.map(x=>({opid:x.opid,key:key(x,map),state:x.state,consumer:"FIXTURE_NOT_ACTUAL_CONSUMER",original_authority:"FIXTURE_ISSUER_UNAUTHENTICATED",owner:x.owner,warrant:x.warrant||null}));
 const d=e.filter(x=>x.state==="PERMITTED_EXACT_GRAIN").map(x=>({opid:x.opid,key:x.key,owner:x.owner}));
 const batch=d.map(x=>({opid:x.opid,key:x.key,batch_status:"COMPLETE"}));
 const results=d.map(x=>({opid:x.opid,key:x.key,result_state:"SUPPORTED_FIXTURE"}));
 return {u:{schema:"P05_SOURCE_NATIVE_ORIGINAL_ROSTER_FIXTURE",source_kind:"SYNTHETIC_NOT_REAL",original_inventory_complete:true,items,operations:ops}, frozen:{schema:"P05_INDEPENDENT_E_FIXTURE",issuer:"SIMULATED_EXTERNAL_ORIGINAL_AND_OPERATION_ISSUER",custody:"SIMULATED_PREEXECUTION_EXPLICIT_EXPECTED_SET",frozen_before_results:true,entries:e},declared:d,batch,results,waves:ALL35.map(w=>({wave:w,state:"HOLD_ORIGINAL_ITEM_ISSUER_NOT_ESTABLISHED"}))};
}
function localCourt(p){
 const d=p.declared.map(x=>x.key),b=p.batch.map(x=>x.key),r=p.results.map(x=>x.key);
 const unique=xs=>new Set(xs).size===xs.length;
 const sort=xs=>xs.slice().sort().join("\n");
 return !!d.length&&unique(d)&&unique(b)&&unique(r)&&sort(d)===sort(b)&&sort(b)===sort(r);
}
function globalCourt(p){
 const bad=[],put=(code)=>{if(!bad.includes(code))bad.push(code)};
 if(!Array.isArray(p.waves)||p.waves.length!==35||new Set(p.waves.map(x=>x.wave)).size!==35||ALL35.some(w=>!p.waves.some(x=>x.wave===w)))put("ALL35_WAVE_REGISTRY_NOT_CONSERVED");
 if(!p.u||p.u.source_kind!=="SYNTHETIC_NOT_REAL")put("NO_REAL_SOURCE_ISSUER_PROOF");
 if(!p.u||p.u.original_inventory_complete!==true)put("ORIGINAL_ROSTER_COMPLETENESS_UNASSERTED");
 if(!p.frozen||p.frozen.frozen_before_results!==true)put("INDEPENDENT_PRE_RESULT_E_CUSTODY_UNESTABLISHED");
 if(!Array.isArray(p.u?.items)||!Array.isArray(p.u?.operations)||!Array.isArray(p.frozen?.entries))return {local_declared_pass:localCourt(p),reconciled:false,errors:[...bad,"MALFORMED_ORIGINAL_OR_E"],grade:"NO_EXTERNAL_ISSUER_OR_CUSTODY"};
 const itemIds=p.u.items.map(x=>x.id),ops=p.u.operations, opIds=ops.map(x=>x.opid);
 if(new Set(itemIds).size!==itemIds.length||new Set(opIds).size!==opIds.length)put("DUPLICATE_ORIGINAL_ID_OR_OPERATION");
 const map=Object.fromEntries(p.u.items.map(x=>[x.id,x]));
 if(ops.some(x=>x.items.some(i=>!map[i])))put("ORIGINAL_ITEM_REFERENT_MISSING");
 if(ops.some(x=>x.response_topology==="J_ONLY_SAME_PERSON"&&x.items.length<2))put("J_ONLY_NATIVE_TOPOLOGY_LOST");
 const calc=new Map(ops.map(x=>[x.opid,{key:key(x,map),state:x.state,warrant:x.warrant||null,owner:x.owner}]));
 const E=new Map(p.frozen.entries.map(x=>[x.opid,x]));
 if(E.size!==p.frozen.entries.length)put("DUPLICATE_EXPECTED_OPERATION");
 for(const [id,x] of calc){const y=E.get(id);if(!y)put("ORIGINAL_TO_E_OMISSION");else if(y.key!==x.key||y.state!==x.state||y.owner!==x.owner)put("ORIGINAL_TO_E_SCOPE_OR_STATE_MUTATION");}
 for(const id of E.keys())if(!calc.has(id))put("E_NOT_IN_ORIGINAL_OPERATION_ROSTER");
 const D=new Map(p.declared.map(x=>[x.opid,x]));
 if(D.size!==p.declared.length||new Set(p.declared.map(x=>x.key)).size!==p.declared.length)put("DECLARED_DUPLICATE");
 for(const [id,y] of E){if(y.state==="PERMITTED_EXACT_GRAIN"){const z=D.get(id);if(!z||z.key!==y.key||z.owner!==y.owner)put("E_TO_DECLARED_OMISSION_OR_REKEY");}else if(D.has(id))put("HELD_DENIED_OR_NA_LAUNDERED_TO_JOB");}
 for(const [id,z] of D)if(!E.has(id))put("UNEXPECTED_UNFROZEN_DECLARED_JOB");
 for(const x of p.frozen.entries)if(x.state==="SOURCE_INTRINSIC_NA_PROVED"&&(!x.warrant||x.warrant!==calc.get(x.opid)?.warrant))put("INTRINSIC_NA_WITHOUT_ORIGINAL_WARRANT");
 for(const x of ops)if(x.state==="HELD"&&x.route==="UNKNOWN"&&p.declared.some(y=>y.opid===x.opid))put("UNKNOWN_ROUTE_ISSUED_AS_OPERATION");
 const B=new Map(p.batch.map(x=>[x.key,x])),R=new Map(p.results.map(x=>[x.key,x]));
 for(const x of p.declared){if(!B.has(x.key)||!R.has(x.key))put("DECLARED_TO_BATCH_OR_RESULT_OMISSION");}
 for(const x of p.batch)if(!p.declared.some(y=>y.key===x.key))put("EXTRA_BATCH_JOB");
 for(const x of p.results)if(!p.declared.some(y=>y.key===x.key))put("EXTRA_RESULT");
 if(!localCourt(p))put("LOCAL_DECLARED_BATCH_RESULT_INCONSISTENT");
 return {local_declared_pass:localCourt(p),reconciled:bad.length===0,errors:bad,grade:"SYNTHETIC_STRUCTURE_ONLY__SOURCE_ISSUER_CUSTODIAN_AND_REAL_CONSUMER_HELD",expected:p.frozen.entries.length,runnable:p.frozen.entries.filter(x=>x.state==="PERMITTED_EXACT_GRAIN").length,declared:p.declared.length,held:p.frozen.entries.filter(x=>x.state==="HELD").length,intrinsic_na:p.frozen.entries.filter(x=>x.state==="SOURCE_INTRINSIC_NA_PROVED").length};
}
function runHostiles(){
 const checks=[];
 const check=(id,mutate,code,local)=>{const p=fixture();mutate(p);const r=globalCourt(p);if(code&&!r.errors.includes(code))throw Error(`${id}: missing ${code}: ${r.errors}`);if(r.local_declared_pass!==local)throw Error(`${id}: local=${r.local_declared_pass} want ${local}`);if(!code&&!r.reconciled)throw Error(`${id}: unexpected ${r.errors}`);checks.push({id,expected:code||"STRUCTURAL_RECONCILED_WITH_STANDING_ISSUER_HOLD",local_declared_pass:r.local_declared_pass,global_reconciled:r.reconciled,passed:true});};
 const deleteOperation=(p,id)=>{p.declared=p.declared.filter(x=>x.opid!==id);p.batch=p.batch.filter(x=>x.opid!==id);p.results=p.results.filter(x=>x.opid!==id)};
 const rekeyOperation=(p,id,newKey)=>{for(const arr of [p.declared,p.batch,p.results]){const rec=arr.find(x=>x.opid===id);if(rec)rec.key=newKey}};
 check("F00_positive_synthetic_four_jobs_two_items_conditional_and_Jonly",()=>{},null,true);
 check("F01_original_eligible_B_omitted_before_job_construction_all_local_pass",p=>deleteOperation(p,"B_U_RAW"),"E_TO_DECLARED_OMISSION_OR_REKEY",true);
 check("F02_J_only_survives_unary_base_absence_and_omission_caught",p=>deleteOperation(p,"JONLY_PAIR"),"E_TO_DECLARED_OMISSION_OR_REKEY",true);
 check("F03_omitted_conditional_direction_all_declared_jobs_pass",p=>deleteOperation(p,"A_TO_B_CONDITION"),"E_TO_DECLARED_OMISSION_OR_REKEY",true);
 check("F04_both_B_and_joint_dropped_no_downstream_alarm",p=>{deleteOperation(p,"B_U_RAW");deleteOperation(p,"JONLY_PAIR")},"E_TO_DECLARED_OMISSION_OR_REKEY",true);
 check("F05_E_truncated_after_original_issuer_frontier",p=>p.frozen.entries=p.frozen.entries.filter(x=>x.opid!=="B_U_RAW"),"ORIGINAL_TO_E_OMISSION",true);
 check("F06_source_operation_B_dropped_only_original_universe",p=>p.u.operations=p.u.operations.filter(x=>x.opid!=="B_U_RAW"),"E_NOT_IN_ORIGINAL_OPERATION_ROSTER",true);
 check("F07_historic_question_var_alias_rekey_on_B",p=>rekeyOperation(p,"B_U_RAW","FAKE_CANONICALIZED_B"),"E_TO_DECLARED_OMISSION_OR_REKEY",true);
 check("F08_forged_form_only_declared_job",p=>rekeyOperation(p,"JONLY_PAIR","FORM_SWAPPED_BUT_LOCALLY_CONSISTENT"),"E_TO_DECLARED_OMISSION_OR_REKEY",true);
 check("F09_false_unknown_route_as_measured_permitted",p=>{const x=p.frozen.entries.find(x=>x.opid==="H_ROUTE_HOLD");p.declared.push({opid:x.opid,key:x.key,owner:x.owner});p.batch.push({opid:x.opid,key:x.key,batch_status:"COMPLETE"});p.results.push({opid:x.opid,key:x.key,result_state:"SUPPORTED_FIXTURE"})},"HELD_DENIED_OR_NA_LAUNDERED_TO_JOB",true);
 check("F10_intrinsic_NA_executed_as_regular_query",p=>{const x=p.frozen.entries.find(x=>x.opid==="N_PROVED_INTRINSIC");p.declared.push({opid:x.opid,key:x.key,owner:x.owner});p.batch.push({opid:x.opid,key:x.key,batch_status:"COMPLETE"});p.results.push({opid:x.opid,key:x.key,result_state:"SUPPORTED_FIXTURE"})},"HELD_DENIED_OR_NA_LAUNDERED_TO_JOB",true);
 check("F11_na_warrant_deleted_but_downstream_unchanged",p=>p.frozen.entries.find(x=>x.opid==="N_PROVED_INTRINSIC").warrant=null,"INTRINSIC_NA_WITHOUT_ORIGINAL_WARRANT",true);
 check("F12_pre_result_freeze_assertion_revoked",p=>p.frozen.frozen_before_results=false,"INDEPENDENT_PRE_RESULT_E_CUSTODY_UNESTABLISHED",true);
 check("F13_source_completeness_assertion_revoked",p=>p.u.original_inventory_complete=false,"ORIGINAL_ROSTER_COMPLETENESS_UNASSERTED",true);
 check("F14_all35_registry_one_wave_dropped",p=>p.waves.pop(),"ALL35_WAVE_REGISTRY_NOT_CONSERVED",true);
 check("F15_original_form_switch_different_from_E",p=>p.u.items.find(x=>x.id==="J1").form="F3","ORIGINAL_TO_E_SCOPE_OR_STATE_MUTATION",true);
 check("F16_original_same_person_relation_rewritten",p=>p.u.operations.find(x=>x.opid==="A_TO_B_CONDITION").respondent_relation="UNKNOWN","ORIGINAL_TO_E_SCOPE_OR_STATE_MUTATION",true);
 check("F17_original_design_estimand_rewritten",p=>p.u.operations.find(x=>x.opid==="B_U_RAW").estimand_ref="NATIONAL_WEIGHTED_FAKE","ORIGINAL_TO_E_SCOPE_OR_STATE_MUTATION",true);
 check("F18_original_condition_order_reversed",p=>p.u.operations.find(x=>x.opid==="A_TO_B_CONDITION").condition_order=["B","A"],"ORIGINAL_TO_E_SCOPE_OR_STATE_MUTATION",true);
 check("F19_original_weighted_measure_forged",p=>p.u.operations.find(x=>x.opid==="B_U_RAW").measure_kind="WEIGHTED","ORIGINAL_TO_E_SCOPE_OR_STATE_MUTATION",true);
 check("F20_unfrozen_extra_job_all_downstream_still_self_consistent",p=>{const z={opid:"EXTRA",key:"UNEXPECTED_FAKE_JOB",owner:"I03"};p.declared.push(z);p.batch.push({...z,batch_status:"COMPLETE"});p.results.push({...z,result_state:"SUPPORTED_FIXTURE"})},"UNEXPECTED_UNFROZEN_DECLARED_JOB",true);
 check("F21_existing_declared_job_absent_batch",p=>p.batch.pop(),"DECLARED_TO_BATCH_OR_RESULT_OMISSION",false);
 check("F22_existing_declared_job_absent_result",p=>p.results.pop(),"DECLARED_TO_BATCH_OR_RESULT_OMISSION",false);
 check("F23_post_result_forged_E_rewrite_that_self_certifies_declared_subset",p=>{deleteOperation(p,"B_U_RAW");p.frozen.entries=p.frozen.entries.filter(x=>x.opid!=="B_U_RAW")},"ORIGINAL_TO_E_OMISSION",true);
 check("F24_original_identity_disappears_but_op_stays",p=>p.u.items=p.u.items.filter(x=>x.id!=="B"),"ORIGINAL_ITEM_REFERENT_MISSING",true);
 check("F25_semantic_to_dispatch_provenance_not_recoverable_by_count_only",p=>rekeyOperation(p,"A_TO_B_CONDITION","SAME_JOB_COUNT_DIFFERENT_SEMANTIC_ID"),"E_TO_DECLARED_OMISSION_OR_REKEY",true);
 check("F26_wrong_source_wave_operator_scope",p=>p.u.operations.find(x=>x.opid==="A_U_RAW").wave="S2","ORIGINAL_TO_E_SCOPE_OR_STATE_MUTATION",true);
 check("F27_issuer_status_in_E_changed_to_denied",p=>p.frozen.entries.find(x=>x.opid==="B_U_RAW").state="DENIED_EXACT_GRAIN","ORIGINAL_TO_E_SCOPE_OR_STATE_MUTATION",true);
 check("F28_no_new_original_survey_claim_from_all35_labels",()=>{},null,true);
 return checks;
}
const cases=runHostiles();
console.log(JSON.stringify({schema:"PYAT_HQ282_P05_SOURCEFREE_HOSTILES_R1",execution_grade:"SYNTHETIC_ONLY",cases:cases.length,pass:cases.length,fail:0,local_python:false,real_survey:false,external_issuer:false,external_custodian:false,actual_consumer:false},null,2));
