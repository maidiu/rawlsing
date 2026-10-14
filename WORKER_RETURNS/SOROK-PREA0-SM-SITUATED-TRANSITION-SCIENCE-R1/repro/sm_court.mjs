#!/usr/bin/env node
// Source-free schema gate for S-M. This is not an actor or psychology simulator.
// Usage: node repro/sm_court.mjs path/to/02_K1_K6_SPEC.json [path/to/authorized_receipts.json]
import fs from 'node:fs';
const [manifestPath, receiptsPath] = process.argv.slice(2);
if (!manifestPath) { console.error('Usage: node sm_court.mjs specification.json [authorized_receipts.json]'); process.exit(2); }
function manifestCourt(d){
const errors=[];
if(d.cases?.length!==6)errors.push("K1_K6_NOT_COMPLETE");
if(d.rules?.length!==9)errors.push("RULE_SET_MISSING");
if(Object.keys(d.baselines||{}).join(",")!=="A,B,C")errors.push("BASELINE_ORDER_WRONG");
if(d.epistemic_status?.generated_actor_transition_runtime_executed!==false)errors.push("FALSE_EXECUTION_CLAIM");
for(const [i,c] of d.cases.entries()){
if(c.id!==`K${i+1}`)errors.push("CASE_ID_OR_ORDER_"+i);
for(const k of ["world","baseline","interventions","primary_predicate","negative_controls","kill"])if(!c[k])errors.push("CASE_MISSING_"+c.id+"_"+k);
for(const k of ["world_receipt","actor_position","relationship","opportunity","event","ancestry"])if(!c.world?.[k])errors.push("MISSING_SITUATED_WORLD_"+c.id+"_"+k);
for(const k of ["world_receipt","actor_position","relationship","opportunity","present_event","ancestry"])if(!c.baseline?.[k])errors.push("MISSING_EVENT_BINDING_"+c.id+"_"+k);
if(c.interventions?.length<2)errors.push("NO_COMPARISON_"+c.id);
}
if(d.fixed_budgets?.model_calls_per_arm!==1)errors.push("MODEL_CALL_BUDGET_DIFFERENT");
if(!d.audit_schema?.hard_invariants?.includes("NO_ACTOR_INACCESSIBLE_LINEAGE_LEAK"))errors.push("OPAQUE_AUDIT_MISSING");
return errors;
}
function receiptCourt(d,receipts){
const errors=[]; const req=d.audit_schema.output_required;
for(const row of receipts){
for(const f of req)if(!(f in row))errors.push(`RECEIPT_MISSING:${row.case_id}:${f}`);
if(!d.cases.some(c=>c.id===row.case_id))errors.push("UNKNOWN_CASE");
if(!["A","B","C"].includes(row.baseline))errors.push("UNKNOWN_BASELINE");
if(row.model_call_count>d.fixed_budgets.model_calls_per_arm)errors.push("BUDGET_MODEL_CALLS");
if(row.retrieval_token_count>d.fixed_budgets.max_evidence_input_tokens)errors.push("BUDGET_TOKENS");
if(!row.world_receipt_hash||!row.admitted_event_hashes?.length)errors.push("CONTEXT_OR_EVENT_ABSENT");
if(row.actor_safe_projection?.hidden_origin_refs?.length)errors.push("HIDDEN_ORIGIN_LEAK");
if(row.committed_effect_receipts?.length&&row.invalid_and_hold_codes?.includes("NO_WORLD_CONTEXT"))errors.push("WORLDLESS_COMMIT");
}
return errors;
}
const d=JSON.parse(fs.readFileSync(manifestPath,'utf8'));
const errors=manifestCourt(d);
if(receiptsPath){
  const receipts=JSON.parse(fs.readFileSync(receiptsPath,'utf8'));
  if(!Array.isArray(receipts)) throw Error('RECEIPTS_MUST_BE_ARRAY');
  errors.push(...receiptCourt(d,receipts));
}
console.log(JSON.stringify({mode:receiptsPath?'SCHEMA_AND_RECEIPT_INTEGRITY':'SPECIFICATION_PREFLIGHT_ONLY',cases:d.cases?.length,received_receipts:!!receiptsPath,passed:errors.length===0,errors,empirical_causal_result:'NOT_ESTABLISHED_BY_THIS_SCRIPT'},null,2));
if(errors.length)process.exit(1);
