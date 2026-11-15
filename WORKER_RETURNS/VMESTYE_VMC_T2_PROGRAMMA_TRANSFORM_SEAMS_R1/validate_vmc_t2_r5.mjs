#!/usr/bin/env node
// VMC-T2 R5 documentary validator (no native Python, tests/CI, original respondents or scientific issuance).
// Usage: node validate_vmc_t2_r5.mjs [--dir PATH] [--no-negative-controls]
// R3 legacy validator retained separately as historical evidence; it is intentionally NOT R5-compatible.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const args=process.argv.slice(2);
const option=(name)=>{const i=args.indexOf(name);return i>=0?args[i+1]:null};
const dir=path.resolve(option('--dir') || path.dirname(fileURLToPath(import.meta.url)));
const raw={};
let shapeFailures=[];
function parse(name){
  const bytes=fs.readFileSync(path.join(dir,name));
  raw[name]=bytes;
  const lines=bytes.toString('utf8').replace(/\r?\n$/,'').split(/\r?\n/);
  const keys=lines.shift().split('\t');
  if(keys.length!==new Set(keys).size)shapeFailures.push(name+':DUPLICATE_COLUMNS');
  const rows=lines.filter(x=>x.length).map((l,i)=>{
    const a=l.split('\t'); if(a.length!==keys.length)shapeFailures.push(name+':BAD_WIDTH:'+(i+2));
    return Object.fromEntries(keys.map((k,j)=>[k,a[j]??'']));
  });
  return rows;
}
const names=['INTENDED_ACTUAL_TRANSFORMATION_MAP.tsv','DISCREPANCY_AND_OWNER_ACTIONS.tsv',
  'REVERSE_CONSUMER_TRACES.tsv','R1_235_TO_T1_R3_52_CROSSWALK.tsv',
  'R4_ROW_LEVEL_DELTA.tsv','R5_HOSTILE_ROW_DELTA.tsv','R4_T1_T2_CROSS_REFERENCES.tsv'];
const [map,actions,reverse,fates,r4Delta,r5Delta,xrefs]=names.map(parse);
const protectedCut='6a5c12f04323d74001f9632063ec907f4fc4468e';
const t1R3='effa0a9e2aa9b2c156c43bd8c093f45faaa291b6';
const t1R6='bb83248e6e7140122d0f01171409954fc9d0cf70';
const gitBlob=(bytes)=>crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
function validate(d){
  const e=[];
  const claim=(q,msg)=>{if(!q)e.push(msg)};
  const count=(a,n,label)=>claim(a.length===n,label+':COUNT '+a.length+' != '+n);
  const unique=(arr,k)=>claim(new Set(arr.map(x=>x[k])).size===arr.length,k+':NONUNIQUE');
  const eq=(a,b,label)=>{const aa=new Set(a),bb=new Set(b);claim(aa.size===bb.size&&[...aa].every(x=>bb.has(x)),label+':INVERSE_ANTIJOIN');};
  const get=(arr,k,v)=>arr.find(x=>x[k]===v);
  count(d.map,52,'HISTORICAL_CONTRACTS');count(d.actions,68,'OWNER_ACTIONS');
  count(d.reverse,542,'REVERSE_CONSUMERS');count(d.fates,235,'R1_FATES');
  count(d.r4Delta,17,'R4_REPAIR_IDS');count(d.r5Delta,23,'R5_REPAIR_IDS');
  count(d.xrefs,7,'T1_T2_CROSSREFS');
  for(const [a,k] of [[d.map,'transform_id'],[d.actions,'action_id'],[d.reverse,'reverse_id'],[d.fates,'r1_id'],[d.xrefs,'cross_ref_id']])unique(a,k);
  const hist=d.actions.filter(x=>x.action_id.startsWith('R3-')&&!x.contract_or_current_id.startsWith('CUR-'));
  const current=d.actions.filter(x=>x.action_id.startsWith('R3-')&&x.contract_or_current_id.startsWith('CUR-'));
  const r4=d.actions.filter(x=>x.action_id.startsWith('R4-'));
  count(hist,52,'HISTORICAL_ORIGINAL_ACTIONS');count(current,11,'CURRENT_ORIGINAL_ACTIONS');
  count(r4,5,'R4_SUPPLEMENTARY_ACTIONS');
  eq(d.map.map(x=>x.transform_id),hist.map(x=>x.contract_or_current_id),'HISTORICAL_ACTIONS');
  eq(d.map.map(x=>x.transform_id),d.reverse.filter(x=>x.grain==='T1_R3_DISTINCT_CONTRACT').map(x=>x.downstream_terminal_or_consumer),'HISTORICAL_REVERSE');
  eq(current.map(x=>x.contract_or_current_id),d.reverse.filter(x=>x.grain==='CURRENT_FIRST_CAPABILITY').map(x=>x.reverse_id.replace(/^CURRENT:/,'')),'CURRENT_FIRST_ORIGINAL');
  claim(d.map.every(x=>x.h_t1_r3_head===t1R3),'R3_BASE_PIN_DRIFT');
  claim(d.fates.every(x=>x.t2_original_t1_r3_head===t1R3),'235_FATE_SOURCE_DRIFT');
  const grains={CURRENT_FIRST_CAPABILITY:11,ROADMAP_SECTION_NOT_RUNTIME:11,ROADMAP_NAMED_CHILD:51,J_TYPED_SEAM_EDGE:82,G4_ORIGINAL_GAP:49,T1_R3_DISTINCT_CONTRACT:52,PROTECTED_PY_MODULE_CENSUS:160,DIRECT_PROTECTED_CALLSITE:44,INHERITED_LONG_MEMORY_OBLIGATION_NOT_RUNTIME:74};
  for(const [g,n] of Object.entries(grains))count(d.reverse.filter(x=>x.grain===g),n,g);
  claim(d.reverse.filter(x=>x.grain==='INHERITED_LONG_MEMORY_OBLIGATION_NOT_RUNTIME'&&x.reverse_id.startsWith('LM:LMX-')).length===44,'LMX_44');
  claim(d.reverse.filter(x=>x.grain==='INHERITED_LONG_MEMORY_OBLIGATION_NOT_RUNTIME'&&x.reverse_id.startsWith('LM:LMQ-')).length===30,'LMQ_30');
  for(const id of ['CURRENT:I07:ESTIMAND_COMPOSITION_GUARD','CURRENT:R08:SIGNED_PREFIX_VERIFY','CURRENT:R08:SIGNED_STEP_EFFECT','CURRENT:BATCH:SEMANTIC_INPUT_REFS_CARRIER','CANDIDATE:F6M:EXPERIMENTAL_NUMERIC_PARTIAL_ID','HISTORICAL:V553:KEYED_WAVE_HARMONIZATION','HISTORICAL:V554:COUNTRY_YEAR_NUMERIC_SEED','CURRENT:M1:V554_CONDITIONAL_TEMPORAL_GATE'])claim(Boolean(get(d.reverse,'reverse_id',id)),'MISSING_R4_REVERSE:'+id);
  const i07=get(d.reverse,'reverse_id','CURRENT:I07:ESTIMAND_COMPOSITION_GUARD');
  claim(Boolean(i07&&/OperationGuardReceipt/.test(i07.data_transformation_or_output)&&/NONTEST_CONSUMER_OPEN_PROOF_GAP/.test(i07.code_source_grade)&&/NOT_HISTORICAL_F6M_NUMERIC_EQUIVALENT/.test(i07.historical_reciprocity_grade)),'I07_GUARD_MISGRADED');
  const signed=get(d.reverse,'reverse_id','CURRENT:R08:SIGNED_STEP_EFFECT');
  const check=get(d.reverse,'reverse_id','CURRENT:R08:SIGNED_PREFIX_VERIFY');
  claim(Boolean(check&&signed&&/TEST_ONLY/.test(check.code_source_grade)&&/TEST_ONLY/.test(signed.code_source_grade)&&/denominator/.test(signed.data_transformation_or_output)&&/cells/.test(signed.data_transformation_or_output)),'R08_TWO_STAGE_FALSE_NATIVE_OR_NO_EFFECT');
  const batch=get(d.reverse,'reverse_id','CURRENT:BATCH:SEMANTIC_INPUT_REFS_CARRIER');
  claim(Boolean(batch&&/CALLER-SUPPLIED/.test(batch.source_or_upstream)&&/NOT_F03_F08/.test(batch.historical_reciprocity_grade)),'BATCH_CARRIER_PROMOTED_TO_SELECTED_RULE');
  const f6m=get(d.reverse,'reverse_id','CANDIDATE:F6M:EXPERIMENTAL_NUMERIC_PARTIAL_ID');
  claim(Boolean(f6m&&/PRIOR_R29_SOURCEFREE/.test(f6m.grain)&&/NOT_ORIGINAL_HISTORICAL/.test(f6m.grain)&&/NOT_ADOPTED_CURRENT_NATIVE/.test(f6m.code_source_grade)),'F6M_EXPERIMENT_BECAME_ORIGINAL_OR_ADOPTED');
  const presence=get(d.map,'transform_id','T1R2-V549B-PRESENCE');
  claim(Boolean(presence&&/literal '1' and '0'/.test(presence.h_selected_input)&&/mask-False/.test(presence.h_guard_predicate)&&/source-only respondent/.test(presence.smallest_s0_s1_falsifier)&&/NOT governed DENY/.test(presence.h_negative_or_refusal)),'V549B_MASK_WAVE_OR_PROGRESS_LOST');
  const topn=get(d.map,'transform_id','T1R2-V549B-TOPN');
  claim(Boolean(topn&&/conditional/.test(topn.h_guard_predicate)&&/NOT original observed failure/.test(topn.h_negative_or_refusal)),'V549B_TOPN_RUNTIME_INVENTED');
  const j=get(d.map,'transform_id','T1R2-V552J-EXACT-JOIN');
  claim(Boolean(j&&/selected-only/.test(j.h_output)&&/HISTORICAL STATIC V553 consumer found/.test(j.c_meaningful_first_reader_and_grade)&&/OPEN_PROOF_GAP/.test(j.c_meaningful_first_reader_and_grade)),'V552J_ALTERNATES_STATIC_READER_COLLAPSE');
  const v553=get(d.reverse,'reverse_id','HISTORICAL:V553:KEYED_WAVE_HARMONIZATION');
  claim(Boolean(v553&&/STATIC V553 canonical/.test(v553.actual_reader_callsite_or_reported_reader)&&/Static original reader LOCATED/.test(v553.smallest_missing_proof)),'V553_STATIC_READER_NOT_RESTORED');
  for(const id of ['T2R4-X01','T2R4-X02','T2R4-X03','T2R4-X04','T2R4-X05','T2R5-X06','T2R5-X07'])claim(Boolean(get(d.xrefs,'cross_ref_id',id)),'CROSSREF_MISSING:'+id);
  claim(d.xrefs.some(x=>x.reviewer_source.includes(t1R6)),'T1_R6_HANDOFF_MISSING');
  claim(d.r5Delta.filter(x=>x.change_kind==='CELL_REPLACE').length===21,'R5_CELL_DELTA_21');
  claim(d.r5Delta.filter(x=>x.change_kind==='APPEND_ROW').length===2,'R5_APPENDS_2');
  for(const x of d.r5Delta.filter(x=>x.change_kind==='CELL_REPLACE')){
    const target=x.file===names[0]?d.map:x.file===names[1]?d.actions:x.file===names[2]?d.reverse:d.xrefs;
    const key=x.file===names[0]?'transform_id':x.file===names[1]?'action_id':x.file===names[2]?'reverse_id':'cross_ref_id';
    const row=get(target,key,x.row_id);claim(Boolean(row&&row[x.field]===x.after_R5),'R5_DELTA_NOT_APPLIED:'+x.row_id+':'+x.field);
  }
  for(const x of d.r5Delta.filter(x=>x.change_kind==='APPEND_ROW'))claim(Boolean(get(d.xrefs,'cross_ref_id',x.row_id)),'R5_APPENDED_LINK_ABSENT:'+x.row_id);
  for(const x of d.r4Delta){if(x.change_kind==='MODIFY_FIELD'){
    const row=get(d.map,'transform_id',x.record_id);claim(Boolean(row&&row[x.column]===x.after_R4),'R4_BASE_DELTA_NOT_CONSERVED:'+x.record_id);
  }else{const target=x.file===names[1]?d.actions:d.reverse;const key=x.file===names[1]?'action_id':'reverse_id';claim(Boolean(get(target,key,x.record_id)),'R4_ADDED_ID_MISSING:'+x.record_id)}}
  claim(d.reverse.every(x=>x.grain!=='J_TYPED_SEAM_EDGE'||/SOURCE_GRAPH_EDGE|ROADMAP|NOT_CODE_CALL/.test(x.code_source_grade)),'GRAPH_INCORRECTLY_EFFECT_BEARING');
  claim(d.reverse.every(x=>x.grain!=='G4_ORIGINAL_GAP'||/ROADMAP|NOT_EXECUTED|NOT_CODE/.test(x.code_source_grade)),'ROADMAP_INCORRECTLY_EFFECT_BEARING');
  claim(d.map.every(x=>!/(^|[;\s])(?:ACCEPTED_EQUIVALENT|JUSTIFIED_RETIRED|NATIVE_ZERO_LOSS)(?:[;\s]|$)/.test(x.equivalence_or_retirement_decision)),'FALSE_ACCEPTANCE');
  claim(d.reverse.find(x=>x.reverse_id==='CURRENT:R08:SIGNED_STEP_EFFECT')?.cut_and_exact_anchor.includes(protectedCut),'R08_SOURCE_CUT_DRIFT');
  return e;
}
const d={map,actions,reverse,fates,r4Delta,r5Delta,xrefs};
const errors=[...shapeFailures,...validate(d)];
const negatives=[];
if(!args.includes('--no-negative-controls')&&errors.length===0){
  const cases=[
    ['drop I07',a=>a.reverse=a.reverse.filter(x=>x.reverse_id!=='CURRENT:I07:ESTIMAND_COMPOSITION_GUARD')],
    ['promote R08 native',a=>a.reverse.find(x=>x.reverse_id==='CURRENT:R08:SIGNED_STEP_EFFECT').code_source_grade='NATIVE_ACCEPTED'],
    ['fake F6M original',a=>a.reverse.find(x=>x.reverse_id==='CANDIDATE:F6M:EXPERIMENTAL_NUMERIC_PARTIAL_ID').grain='HISTORICAL_ORIGINAL_PROVED'],
    ['promote Batch carrier',a=>a.reverse.find(x=>x.reverse_id==='CURRENT:BATCH:SEMANTIC_INPUT_REFS_CARRIER').source_or_upstream='SOURCE_ISSUER_SELECTED_F03_F08'],
    ['collapse V552J selected to all',a=>a.map.find(x=>x.transform_id==='T1R2-V552J-EXACT-JOIN').h_output='all alternatives delivered'],
    ['impute V549b missing as zero',a=>a.map.find(x=>x.transform_id==='T1R2-V549B-PRESENCE').h_guard_predicate='binary arbitrary values'],
    ['erase T1 R6 crossref',a=>a.xrefs=a.xrefs.filter(x=>x.cross_ref_id!=='T2R5-X06')],
    ['duplicate historic ID',a=>a.map[1].transform_id=a.map[0].transform_id],
    ['drop a prior R4 action',a=>a.actions=a.actions.filter(x=>x.action_id!=='R4-003')]
  ];
  for(const [label,mut] of cases){
    const altered=structuredClone(d);mut(altered);
    const result=validate(altered);negatives.push({label,rejected:result.length>0,example:result[0]});
    if(!result.length)errors.push('SYNTHETIC_NEGATIVE_NOT_REJECTED:'+label);
  }
}
const sourceBlob=gitBlob(raw['R1_235_TO_T1_R3_52_CROSSWALK.tsv']);
if(sourceBlob!=='2b4e4e81cb2d242e9f4eb648cb66a79fc41b43a8')errors.push('R1_235_BLOB_DRIFT:'+sourceBlob);
const result={status:errors.length?'FAIL':'PASS',contracts:map.length,actions:actions.length,reverse:reverse.length,inherited_fates:fates.length,cross_refs:xrefs.length,r4_delta:r4Delta.length,r5_delta:r5Delta.length,r1_fates_git_blob:sourceBlob,negative_controls:negatives,source_grade:'GITHUB_DOCUMENTARY_ONLY__NO_NATIVE_OR_SOURCE_SCIENCE_ACTOR_ISSUER_ACCEPTANCE',errors};
console.log(JSON.stringify(result,null,2));if(errors.length)process.exitCode=1;
