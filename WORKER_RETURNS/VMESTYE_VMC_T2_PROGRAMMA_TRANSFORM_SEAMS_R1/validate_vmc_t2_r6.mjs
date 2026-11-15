#!/usr/bin/env node
// VMC-T2 R6 documentary conservation verifier. NOT a native/scientific/actor test.
// node validate_vmc_t2_r6.mjs --repo-root /exact/pinned/repository/checkout
// node validate_vmc_t2_r6.mjs --structural-only
// FULL PASS requires local Git objects at R3, R4, R5, the protected source cut and current R6 TSVs.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const args=process.argv.slice(2);
const arg=(name)=>{let i=args.indexOf(name);return i<0?null:args[i+1];};
const strictRoot=arg('--repo-root');
const structural=args.includes('--structural-only');
const dir=path.resolve(arg('--dir')||path.dirname(fileURLToPath(import.meta.url)));
const area='WORKER_RETURNS/VMESTYE_VMC_T2_PROGRAMMA_TRANSFORM_SEAMS_R1/';
const old={R3:'5a73ee31e7dd5af26474f35bbe280dd3bb3b0bac',
 R4:'edfe7bb9fab1fd295621e9447745ddab4bb67bfb',
 R5:'355b49217087159a0ed93ae2c076f4a4c23b287b'};
const cuts={PREMAIN:'6a5c12f04323d74001f9632063ec907f4fc4468e',
 ORIGINAL:'9253064bc9423a0f0ccda4fbdea43c2f54f800c6',
 T1R6:'bb83248e6e7140122d0f01171409954fc9d0cf70'};
const tableFiles=['INTENDED_ACTUAL_TRANSFORMATION_MAP.tsv','DISCREPANCY_AND_OWNER_ACTIONS.tsv',
 'REVERSE_CONSUMER_TRACES.tsv','R4_T1_T2_CROSS_REFERENCES.tsv'];
const otherFiles=['R1_235_TO_T1_R3_52_CROSSWALK.tsv','R4_ROW_LEVEL_DELTA.tsv',
 'R5_HOSTILE_ROW_DELTA.tsv','R6_HOSTILE_ROW_DELTA.tsv','R6_T1_R6_ROW_SOURCE_OVERLAYS.tsv'];
const EXPECTED_BLOBS={
 'INTENDED_ACTUAL_TRANSFORMATION_MAP.tsv':'af30592573206ec90d0fd2a67767b56a658bde74',
 'DISCREPANCY_AND_OWNER_ACTIONS.tsv':'c01bc4d649319f338f89674903438c641bf7cdb8',
 'REVERSE_CONSUMER_TRACES.tsv':'b881e4eddc9b0b95be1da665fd7e0f5b9cbfb372',
 'R4_T1_T2_CROSS_REFERENCES.tsv':'cf792d11f5da3308756428176cbdec3d1745e385',
 'R1_235_TO_T1_R3_52_CROSSWALK.tsv':'2b4e4e81cb2d242e9f4eb648cb66a79fc41b43a8',
 'R4_ROW_LEVEL_DELTA.tsv':'3ee9fcd27664a579919955c805e6975768553904',
 'R5_HOSTILE_ROW_DELTA.tsv':'86bbef7e75663bf7131d12da439990a52954eabb',
 'R6_HOSTILE_ROW_DELTA.tsv':'6a2b9532b37a09ad1338d5b3d97910b2e03d96b3',
 'R6_T1_R6_ROW_SOURCE_OVERLAYS.tsv':'072d6433cc9f28c4585f0e41fd54b9513df8ee45'};
const errors=[],mutations=[];
const verify=(yes,why)=>{if(!yes)errors.push(why);};
const sha=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const reader=b=>{
 const lines=b.toString('utf8').replace(/\r?\n$/,'').split(/\r?\n/);
 const head=lines.shift().split('\t');
 if(new Set(head).size!==head.length)throw Error('duplicate TSV columns');
 const data=lines.filter(x=>x.length).map((line,i)=>{
  const cols=line.split('\t');
  if(cols.length!==head.length)throw Error('bad TSV width line '+(i+2));
  return Object.fromEntries(head.map((k,j)=>[k,cols[j]]));
 });
 return {head,data};
};
const current={};
for(const n of [...tableFiles,...otherFiles]){
 const b=fs.readFileSync(path.join(dir,n));
 verify(sha(b)===EXPECTED_BLOBS[n],'R6_BLOB_MISMATCH:'+n);
 current[n]=reader(b);
}
const keys=['transform_id','action_id','reverse_id','cross_ref_id'];
function ids(tsv){return tsv.data.map(r=>r[tsv.head[0]]);}
function get(tsv,id){return tsv.data.find(r=>r[tsv.head[0]]===id);}
function assertUnique(tsv,n){const a=ids(tsv);verify(a.length===new Set(a).size,'DUPLICATE_ID:'+n);}
for(const n of tableFiles)assertUnique(current[n],n);
const counts=[52,68,542,7,235,17,23,25,4];
const allNames=[...tableFiles,...otherFiles];
for(let i=0;i<allNames.length;i++)verify(current[allNames[i]].data.length===counts[i],'ROW_COUNT:'+allNames[i]);
const r=current[tableFiles[2]],map=current[tableFiles[0]],actions=current[tableFiles[1]];
const i07=get(r,'CURRENT:I07:ESTIMAND_COMPOSITION_GUARD');
const r08=get(r,'CURRENT:R08:SIGNED_STEP_EFFECT');
const early=get(r,'CURRENT:R08:SIGNED_PREFIX_VERIFY');
const v553=get(r,'HISTORICAL:V553:KEYED_WAVE_HARMONIZATION');
const batch=get(r,'CURRENT:BATCH:SEMANTIC_INPUT_REFS_CARRIER');
verify(Boolean(i07&&i07.actual_callsite_line.includes('NO_NONTEST_DOWNSTREAM_CALLSITE_PROVED')),'I07_DEF_FALSE_CALLSITE');
verify(Boolean(early&&early.actual_callsite_line.includes('L79')&&early.code_source_grade.includes('TEST_ONLY')),'R08_EARLY_CALL_UNVERIFIED');
verify(Boolean(r08&&r08.actual_callsite_line.includes('L1224-1225')&&r08.cut_and_exact_anchor.includes('1174-1226')&&r08.code_source_grade.includes('TEST_ONLY')),'R08_EFFECT_LINE_OR_PROOF_GRADE');
verify(Boolean(v553&&v553.cut_and_exact_anchor.includes('5304b70f9f6522c5ae3893eff215c1d445681983')&&v553.actual_callsite_line.includes('L2048')),'V553_TEMPORAL_CALLER_NOT_PINNED');
verify(Boolean(batch&&batch.actual_callsite_line.includes('NO_HISTORICAL_F03_F08_RULE_CALLER_PROVED')),'BATCH_DEFINITION_PROMOTED_TO_RULE');
verify(Boolean(get(r,'CANDIDATE:F6M:EXPERIMENTAL_NUMERIC_PARTIAL_ID')?.actual_callsite_line.includes('NO_SOURCE_SELECTED_N9_CALLSITE')),'F6M_DEFINITION_PROMOTED_TO_READER');
const original=actions.data.filter(x=>x.action_id.startsWith('R3-'));
verify(original.length===63,'R3_ACTION_GRANULARITY_LOST');
verify(actions.data.filter(x=>x.action_id.startsWith('R4-')).length===5,'R4_OWNER_ROWS_LOST');
verify(r.data.filter(x=>x.grain==='T1_R3_DISTINCT_CONTRACT').length===52,'HISTORICAL_REVERSE_LOST');
verify(map.data.every(x=>x.h_t1_r3_head==='effa0a9e2aa9b2c156c43bd8c093f45faaa291b6'),'R3_BASE_SOURCE_PIN_CORRUPT');
const overlays=current['R6_T1_R6_ROW_SOURCE_OVERLAYS.tsv'];
verify(overlays.data.every(x=>x.later_t1_r6_author_head===cuts.T1R6),'SOURCE_OVERLAY_R6_PIN');
verify(overlays.data.every(x=>map.data.some(y=>y.transform_id===x.original_t2_contract_id)),'OVERLAY_UNKNOWN_HISTORICAL_ID');
const R6ledger=current['R6_HOSTILE_ROW_DELTA.tsv'];
function diff(a,b,file){
 const violations=[];
 if(a.head.join('\t')!==b.head.join('\t'))violations.push('HEADER:'+file);
 const prior=new Set(ids(a)),later=new Set(ids(b));
 for(const id of prior)if(!later.has(id))violations.push('DROP:'+file+':'+id);
 const modifications=[];
 for(const item of a.data){
  const next=get(b,item[a.head[0]]);
  if(!next)continue;
  for(const col of a.head)if(item[col]!==next[col])
   modifications.push({file,row_id:item[a.head[0]],field:col,old:item[col],now:next[col]});
 }
 const appended=b.data.filter(x=>!prior.has(x[b.head[0]])).map(x=>x[b.head[0]]);
 return {violations,modifications,appended};
}
function checkTransition(a,b,delta,mode){
 const problems=[];
 const attr=mode==='R4'?{file:'file',id:'record_id',col:'column',bef:'before_R3',aft:'after_R4',typ:'change_kind'}:
 mode==='R5'?{file:'file',id:'row_id',col:'field',bef:'before_R4',aft:'after_R5',typ:'change_kind'}:
 {file:'file',id:'row_id',col:'field',bef:'before_R5',aft:'after_R6',typ:'change_kind'};
 const categories=mode==='R4'?['MODIFY_FIELD','ADD_CURRENT_FIRST_OR_TYPED_LEGACY_REVERSE','ADD_FINITE_OWNER_ACTION']:
 mode==='R5'?['CELL_REPLACE','APPEND_ROW']:['CELL_REPLACE'];
 for(const file of tableFiles){
  if(!a[file]||!b[file]){
   if(mode==='R4'&&file==='R4_T1_T2_CROSS_REFERENCES.tsv')continue;
   problems.push('NO_TABLE:'+file);continue;
  }
  const d=diff(a[file],b[file],file);problems.push(...d.violations);
  const relevant=delta.data.filter(x=>x[attr.file]===file);
  const fieldEdits=relevant.filter(x=>x[attr.typ]==='MODIFY_FIELD'||x[attr.typ]==='CELL_REPLACE');
  const added=relevant.filter(x=>!['MODIFY_FIELD','CELL_REPLACE'].includes(x[attr.typ]));
  for(const e of d.modifications){
   const x=fieldEdits.find(x=>x[attr.id]===e.row_id&&x[attr.col]===e.field);
   if(!x||x[attr.bef]!==e.old||x[attr.aft]!==e.now)
    problems.push('UNRECORDED_OR_MISMATCHED_FIELD:'+file+':'+e.row_id+':'+e.field);
  }
  for(const x of fieldEdits){
   if(!d.modifications.some(y=>y.row_id===x[attr.id]&&y.field===x[attr.col]))
    problems.push('LEDGER_EDIT_NOT_APPLIED:'+file+':'+x[attr.id]+':'+x[attr.col]);
  }
  if(added.length!==d.appended.length)problems.push('APPEND_COUNT_MISMATCH:'+file);
  for(const id of d.appended)if(!added.some(x=>x[attr.id]===id))problems.push('UNRECORDED_ADD:'+file+':'+id);
  const aIds=ids(a[file]),bIds=ids(b[file]);
  if(aIds.some((id,i)=>id!==bIds[i]))problems.push('ORIGINAL_ID_ORDER_CHANGED:'+file);
 }
 return problems;
}
let strictResults=null;
if(strictRoot){
 const show=(shaRef,filename)=>execFileSync('git',['-C',strictRoot,'show',shaRef+':'+area+filename],{maxBuffer:8*1024*1024});
 const tree=(ref,names)=>{
  const result={};for(const n of names)result[n]=reader(show(ref,n));return result;
 };
 const cutsToVerify=[old.R3,old.R4,old.R5,cuts.PREMAIN,cuts.ORIGINAL,cuts.T1R6];
 for(const s of cutsToVerify){
  const actual=execFileSync('git',['-C',strictRoot,'rev-parse','--verify',s+'^{commit}'],{encoding:'utf8'}).trim();
  verify(actual===s,'UNAVAILABLE_PINNED_GIT_COMMIT:'+s);
 }
 const core=tableFiles.slice(0,3);
 const R3=tree(old.R3,core);
 const R4=tree(old.R4,tableFiles);
 const R5=tree(old.R5,tableFiles);
 const R6=Object.fromEntries(tableFiles.map(n=>[n,current[n]]));
 strictResults={
  r3_to_r4:checkTransition(R3,R4,current['R4_ROW_LEVEL_DELTA.tsv'],'R4'),
  r4_to_r5:checkTransition(R4,R5,current['R5_HOSTILE_ROW_DELTA.tsv'],'R5'),
  r5_to_r6:checkTransition(R5,R6,R6ledger,'R6')
 };
 for(const [kind,probs]of Object.entries(strictResults))for(const e of probs)errors.push(kind+':'+e);
 // These are real source line reads, not production execution.
 const src=(ref,n)=>show(ref,n).toString('utf8').split(/\r?\n/);
 const world=src(cuts.PREMAIN,'rawlsing_next/pre553_universal_world_binding.py');
 verify(world[1223]?.includes('step["denominator"]')&&world[1224]?.includes('step["cells"]'),'R08_SOURCE_EFFECT_NOT_AT_1224_1225');
 const oldTemporal=src(cuts.ORIGINAL,'data/ddm_build_copy/ddm_v553_temporal_pressure.py');
 verify(oldTemporal[2047]?.includes('_packet_structural_dimension_resolution('),'V553_L2048_NOT_A_STATIC_CALL');
 const v552j=src(cuts.ORIGINAL,'data/ddm_build_copy/ddm_v552j_handoff.py');
 verify(v552j[94]?.includes('source_v552_structural_fact_ids_json'),'V552J_SELECTED_FACT_SOURCE_CHANGED');
 // Negative controls target byte-identical, same-count, same-ID mutation, not merely a count check.
 if(strictResults.r5_to_r6.length===0){
  const mutate=(label,fn)=>{
   const dirty=structuredClone(R6);fn(dirty);
   const detect=checkTransition(R5,dirty,R6ledger,'R6');
   const pass=detect.length>0;mutations.push({label,rejected:pass,defect:detect[0]||null});
   if(!pass)errors.push('NEGATIVE_CONTROL_ESCAPED:'+label);
  };
  mutate('tamper unedited historic row',d=>d[tableFiles[0]].data[0].h_output+=' FALSE_EXTRA_PROOF');
  mutate('fake R08 native effect source',d=>get(d[tableFiles[2]],'CURRENT:R08:SIGNED_STEP_EFFECT').actual_callsite_line='L1174-1223_ONLY');
  mutate('erase static V553 temporal call',d=>get(d[tableFiles[2]],'HISTORICAL:V553:KEYED_WAVE_HARMONIZATION').cut_and_exact_anchor='canonical only');
  mutate('fake selected Batch F03 policy',d=>get(d[tableFiles[2]],'CURRENT:BATCH:SEMANTIC_INPUT_REFS_CARRIER').source_or_upstream='source-issued applied policy');
  mutate('change negative J tie semantics',d=>get(d[tableFiles[0]],'T1R2-V552J-EXACT-JOIN').h_negative_or_refusal='tie raises source denial');
 }
} else if(!structural){
 errors.push('STRICT_BASELINE_REQUIRED: use --repo-root for full Git R3-R6 conservation or explicitly --structural-only');
}
const outcome={status:errors.length?'FAIL':strictRoot?'PASS_STRICT_DOCUMENTARY':'PASS_STRUCTURAL_ONLY_NOT_RECEIVING',
 cut:'VMC-T2-R6',exact_prior_R5:old.R5,source_pre_main:cuts.PREMAIN,
 records:{historical_contracts:map.data.length,owner_actions:actions.data.length,reverse:r.data.length,
  fate_identities:current[otherFiles[0]].data.length,r4_delta:current[otherFiles[1]].data.length,
  r5_delta:current[otherFiles[2]].data.length,r6_delta:R6ledger.data.length,
  crossrefs:current[tableFiles[3]].data.length,t1_r6_overlays:overlays.data.length},
 strictGitReview:strictResults?Object.fromEntries(Object.entries(strictResults).map(([k,v])=>[k,{errors:v.length}])):null,
 hostile_controls:mutations,source_ceiling:'S0-S1_DOCUMENTARY_ONLY;NO_S2_S3_NATIVE_ISSUER_SCIENCE_ACTOR_OR_MERGE',
 errors};
console.log(JSON.stringify(outcome,null,2));if(errors.length)process.exitCode=1;
