#!/usr/bin/env node
// VMC-T2 R7 hostile receiving preflight. S0/S1 code/data conservation only.
// Usage: node validate_vmc_t2_r7.mjs --repo-root /pinned/rawlsing --candidate-ref <exact_40_hex_R7_SHA>
// Strict only. No green structural-only fallback; no native, source/actor/science issuer, S2/S3 or merge.
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const argv=process.argv.slice(2);
const arg=k=>{const i=argv.indexOf(k);return i>=0?argv[i+1]:null;};
const root=arg('--repo-root'),candidate=arg('--candidate-ref');
const here=path.dirname(fileURLToPath(import.meta.url));
const authorFile=fileURLToPath(import.meta.url);
const prefix='WORKER_RETURNS/VMESTYE_VMC_T2_PROGRAMMA_TRANSFORM_SEAMS_R1/';
const HEAD_PREMAIN='6a5c12f04323d74001f9632063ec907f4fc4468e';
const HIST='9253064bc9423a0f0ccda4fbdea43c2f54f800c6';
const R29='1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa';
const R3='5a73ee31e7dd5af26474f35bbe280dd3bb3b0bac';
const R4='edfe7bb9fab1fd295621e9447745ddab4bb67bfb';
const R5='355b49217087159a0ed93ae2c076f4a4c23b287b';
const R6='3d7ed2c23354decee6f75b0a3ddfdb805de58795';
const T1R6='bb83248e6e7140122d0f01171409954fc9d0cf70';
const ownerRef=arg('--owner-ref')||'refs/heads/research/vmestye-vmc-t2-programma-transform-seams-r1';
const protectedRef=arg('--protected-ref')||'refs/heads/integration/pre-main-reconciliation-r1';
const reasons=[],negatives=[];
const fail=s=>reasons.push(s);
const requireTest=(test,msg)=>{if(!test)fail(msg);};
const hex=s=>typeof s==='string'&&/^[0-9a-f]{40}$/.test(s);
const git=(...args)=>execFileSync('git',['-C',root,...args],{maxBuffer:12*1024*1024});
const rev=ref=>git('rev-parse','--verify',ref).toString('utf8').trim();
const src=(ref,pathText)=>git('show',ref+':'+pathText);
const data=(buffer,label)=>{
 const ls=buffer.toString('utf8').split(/\r?\n/);
 if(ls.at(-1)==='')ls.pop();
 const h=ls.shift().split('\t');
 if(h.length!==new Set(h).size)fail('DUPLICATE_COLUMNS:'+label);
 const rows=ls.map((line,i)=>{
  if(!line.length)fail('EMPTY_DATA_ROW:'+label+':'+(i+2));
  const cells=line.split('\t');
  if(cells.length!==h.length)fail('BAD_WIDTH:'+label+':'+(i+2));
  return Object.fromEntries(h.map((key,j)=>[key,cells[j]??'']));
 });
 const keys=rows.map(row=>row[h[0]]);
 if(keys.length!==new Set(keys).size)fail('DUPLICATE_ID:'+label);
 if(keys.some(k=>!k))fail('EMPTY_ID:'+label);
 return {h,rows,keys};
};
const noDup=x=>new Set(x.map(y=>y.id)).size===x.length;
if(!root||!hex(candidate)||argv.includes('--structural-only')){
 console.log(JSON.stringify({status:'HOLD_EXACT_INPUT',reason:'Specify --repo-root and --candidate-ref <40 hex> (strict only). No structural-only PASS.'},null,2));process.exit(2);
}
try{
 for(const ref of [R3,R4,R5,R6,T1R6,HEAD_PREMAIN,HIST,R29,candidate]){
  const actual=rev(ref+'^{commit}');
  requireTest(actual===ref,'MISSING_OR_WRONG_COMMIT:'+ref);
 }
 requireTest(rev(ownerRef)===candidate,'OWNER_BRANCH_SHA_DRIFT');
 requireTest(rev(protectedRef)===HEAD_PREMAIN,'PROTECTED_BRANCH_SHA_DRIFT');
 // Verify that we are running exactly the version committed at the candidate SHA.
 requireTest(fs.readFileSync(authorFile).equals(src(candidate,prefix+'validate_vmc_t2_r7.mjs')),
  'EXECUTED_R7_SCRIPT_NOT_CANDIDATE_BLOB');
 // R6's source validator is a conserved predecessor; do not substitute another script.
 requireTest(fs.readFileSync(path.join(here,'validate_vmc_t2_r6.mjs')).equals(
   src(R6,prefix+'validate_vmc_t2_r6.mjs')),'INHERITED_R6_VALIDATOR_CHANGED');
 const tables=['INTENDED_ACTUAL_TRANSFORMATION_MAP.tsv','DISCREPANCY_AND_OWNER_ACTIONS.tsv',
  'REVERSE_CONSUMER_TRACES.tsv','R4_T1_T2_CROSS_REFERENCES.tsv'];
 const stages={};
 for(const [name,ref,selection] of [
  ['R3',R3,tables.slice(0,3)],['R4',R4,tables],['R5',R5,tables],
  ['R6',R6,tables],['R7',candidate,tables]]){
  stages[name]={};
  for(const n of selection){
   const bytes=src(ref,prefix+n);
   const local=name==='R7'?fs.readFileSync(path.join(here,n)):null;
   if(local)requireTest(local.equals(bytes),'CURRENT_FILE_NOT_AT_CANDIDATE_SHA:'+n);
   stages[name][n]=data(bytes,name+':'+n);
  }
 }
 const counts={R3:[52,63,534],R4:[52,68,542,5],R5:[52,68,542,7],R6:[52,68,542,7],R7:[52,68,542,7]};
 for(const [name,values] of Object.entries(counts)){
  const got=Object.values(stages[name]).map(x=>x.rows.length);
  requireTest(JSON.stringify(values)===JSON.stringify(got),'ROW_DENOMINATORS_CHANGED:'+name+':'+got);
 }
 const original=stages.R3,now=stages.R7;
 for(const n of tables.slice(0,3)){
  for(const id of original[n].keys)requireTest(now[n].keys.includes(id),'LOST_R3_ID:'+n+':'+id);
  requireTest(JSON.stringify(now[n].keys.slice(0,original[n].keys.length))===JSON.stringify(original[n].keys),
   'R3_ORIGINAL_ID_ORDER_CHANGED:'+n);
 }
 for(const n of tables){
  requireTest(src(R6,prefix+n).equals(src(candidate,prefix+n)),'R7_UNAUTHORIZED_TSV_CHANGE:'+n);
 }
 // R6 added four row-specific T1 overlays. Verify they correspond to frozen T1 R6 and known original T2 IDs.
 const overlayName='R6_T1_R6_ROW_SOURCE_OVERLAYS.tsv';
 const overlayBytes=src(candidate,prefix+overlayName);
 requireTest(overlayBytes.equals(src(R6,prefix+overlayName)),'R6_T1_OVERLAY_CHANGED');
 const overlay=data(overlayBytes,'R7:overlays');
 requireTest(overlay.rows.length===4,'T1_OVERLAY_COUNT_CHANGED');
 const oldIds=new Set(original[tables[0]].keys);
 for(const row of overlay.rows){
  requireTest(oldIds.has(row.original_t2_contract_id),'T1_OVERLAY_UNKNOWN_ORIGINAL_ID:'+row.original_t2_contract_id);
  requireTest(row.later_t1_r6_author_head===T1R6,'T1_OVERLAY_WRONG_AUTHOR_SHA');
 }
 const t1contracts=src(T1R6,'WORKER_RETURNS/VMESTYE_VMC_T1_TRANSFORM_CONTRACTS_R1/HISTORICAL_TRANSFORM_CONTRACTS.tsv');
 const t1=data(t1contracts,'T1R6:historical');
 for(const row of overlay.rows){
  requireTest(t1.keys.includes(row.original_t2_contract_id),'T1_R6_CONTRACT_ID_NOT_FOUND:'+row.original_t2_contract_id);
 }
 // Check the precise code blobs; a commit existing does not prove that the named file or symbol is at the stated source cut.
 const sourcePins=[
  [HEAD_PREMAIN,'rawlsing_next/pre553_source_relations.py','5b67e3f98a5faf95a6c82700af2346fef6e306a5'],
  [HEAD_PREMAIN,'rawlsing_next/pre553_evidence_world_consumer.py','75ff3b9a73b1533c5fa6619e36577b69a4c65aed'],
  [HEAD_PREMAIN,'rawlsing_next/pre553_universal_world_binding.py','fdda8b2f887bd1fb7703bc5fb8ce1fefc52ca09d'],
  [HEAD_PREMAIN,'rawlsing_next/pre553_batch_runner.py','2d291600b9a10c56d9c6f6de7f7d619f6c52e829'],
  [HEAD_PREMAIN,'rawlsing_next/m1_temporal_v554_admission_dedup.py','e8bd6376720a2de132b384e7771d71d8d39cf261'],
  [HEAD_PREMAIN,'data/ddm_build_copy/ddm_v554_seed_contract.py','b11b73fc171f6b37976fa579d54700505a69f84c'],
  [HIST,'data/ddm_build_copy/ddm_v552j_handoff.py','476e617370e8947ee1f38b0718243ecfc5ba9e5c'],
  [HIST,'data/ddm_build_copy/compile_v552j_structural_handoff.py','a3e6bf17386b58beb0c14b2d79d9e4a9e405c300'],
  [HIST,'data/ddm_build_copy/ddm_v553_canonical_harmonization.py','1951ada5cb7453108939eae9af91fcbfc90ad517'],
  [HIST,'data/ddm_build_copy/ddm_v553_temporal_pressure.py','5304b70f9f6522c5ae3893eff215c1d445681983'],
  [R29,'WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py','2df811d76db258d98d89ffb43c830cb221ff9a7d']
 ];
 for(const [ref,p,blob] of sourcePins){
  const actual=rev(ref+':'+p);
  requireTest(actual===blob,'SOURCE_BLOB_NOT_PINNED:'+p);
 }
 // Source lines are separately checked instead of trusting the authored description.
 const world=src(HEAD_PREMAIN,'rawlsing_next/pre553_universal_world_binding.py').toString('utf8').split(/\r?\n/);
 requireTest(world[1223]?.includes('step["denominator"]')&&world[1224]?.includes('step["cells"]'),
  'R08_SIGNED_STEP_EFFECT_MISSING');
 const temporal=src(HIST,'data/ddm_build_copy/ddm_v553_temporal_pressure.py').toString('utf8').split(/\r?\n/);
 requireTest(temporal[2047]?.includes('_packet_structural_dimension_resolution('),
  'V553_TEMPORAL_CALL_NOT_AT_2048');
 // Execute predecessor strict validator as a process; require its specific strict result and all hostile controls.
 const inherited=JSON.parse(execFileSync(process.execPath,[
  path.join(here,'validate_vmc_t2_r6.mjs'),'--repo-root',root,'--dir',here
 ],{encoding:'utf8',maxBuffer:5*1024*1024}));
 requireTest(inherited.status==='PASS_STRICT_DOCUMENTARY'&&inherited.errors.length===0,
  'INHERITED_R6_STRICT_FAILED');
 requireTest(inherited.hostile_controls.length===5&&inherited.hostile_controls.every(x=>x.rejected),
  'R6_HOSTILE_CONTROLS_NOT_ALL_REJECTED');
 // Hostilely exercise the new uniqueness/ledger gate on a pure duplicate of a previous ID.
 const copied=now[tables[2]].keys.map(id=>({id}));
 const injected=[...copied,{...copied[0]}];
 requireTest(noDup(copied),'GOOD_IDS_REJECTED');
 const caughtDuplicate=!noDup(injected);
 negatives.push({attack:'same-content existing-ID append',rejected:caughtDuplicate});
 requireTest(caughtDuplicate,'DUPLICATE_EXISTING_ID_ESCAPED');
 // Verify that formerly invisible extra delta rows or duplicate receipt identities fail exact ledger eligibility.
 for(const name of ['R4_ROW_LEVEL_DELTA.tsv','R5_HOSTILE_ROW_DELTA.tsv','R6_HOSTILE_ROW_DELTA.tsv']){
  const present=src(candidate,prefix+name);
  const frozen=src(R6,prefix+name);
  requireTest(present.equals(frozen),'CUMULATIVE_DELTA_BLOB_DRIFT:'+name);
  const ledger=data(present,'CUMULATIVE:'+name);
  const key=x=>[x.file,x.record_id||x.row_id,x.column||x.field].join('|');
  const values=ledger.rows.map(key);
  requireTest(values.length===new Set(values).size,'DUPLICATE_LEDGER_EDIT:'+name);
  requireTest(ledger.rows.every(row=>tables.includes(row.file)),'UNKNOWN_LEDGER_TABLE:'+name);
 }
}catch(e){fail('STRICT_EXECUTION_EXCEPTION:'+String(e.message||e).slice(0,1400));}
const result={status:reasons.length?'HOLD_EXACT_MATERIAL_DEFECT':'PASS_R7_STRICT_DOCUMENTARY_ONLY',
 candidate,owner_ref:ownerRef,protected_ref:protectedRef,previous:R6,original_r3:R3,
 checks:'Pinned branch & exact executable blob, R3-R7 identity/row order, frozen R6 TSV, T1 R6 IDs, eleven source file blobs, inherited R6 strict validator, delta receipts and hostile duplicate mutation',
 negatives,source_ceiling:'NO_NATIVE_ORIGINAL35_S2_S3_SCIENCE_SOURCE_ACTOR_ISSUER_OR_INDEPENDENT_ACCEPTANCE',
 errors:reasons};
console.log(JSON.stringify(result,null,2));
if(reasons.length)process.exitCode=1;
