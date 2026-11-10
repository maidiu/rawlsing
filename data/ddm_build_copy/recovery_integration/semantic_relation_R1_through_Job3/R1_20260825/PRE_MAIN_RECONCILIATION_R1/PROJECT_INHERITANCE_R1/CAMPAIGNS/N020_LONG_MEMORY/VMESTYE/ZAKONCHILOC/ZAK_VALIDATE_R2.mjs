#!/usr/bin/env node
/* ZAK-00 R2 S0-S1 author-side structural/semantic-receiving preflight.
 * No original respondent/native invocation, GitHub reviewer credential, or scientific issuance.
 * Run: node ZAK_VALIDATE_R2.mjs
 *       node ZAK_VALIDATE_R2.mjs --negative-controls
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const FILES = {
  obligations:'ZAK_INHERITED_OBLIGATIONS.tsv',
  sources:'ZAK_SOURCE_BASELINE.tsv',
  dispatch:'ZAK_DISPATCH_LEDGER.tsv'
};
const R1_SHA = {
  obligations: 'a00305aaccdf422c86f7311a7e39b55eca2a6bbd',
  sources: 'acdf012408e8546283b298a8185e242f2ae81930'
};
const FAMILY_COUNTS = {
  LEGACY_F_CLASS:29, AUTHORITY_RELEASE:58, LONG_MEMORY_REQUIREMENT:44,
  LONG_MEMORY_PROOF_DEBT:30, PRONG_RETURN_REFERENCE:13, MATERIAL_RESIDUAL_REFERENCE:8
};
const requiredSourceKeys = [
  'C6_SELECTED_01','C6_CASES_03','F29_SEED','AR58_SEED','LMX44_SEED','LMQ30_SEED',
  'LEGACY_V549B_DIRECT','LEGACY_J_REGISTRY_DIRECT','LEGACY_J_PATTERN_DIRECT',
  'LEGACY_V551J_DIRECT','LEGACY_V552J_DIRECT','CURRENT_C11_INGEST_DIRECT',
  'CURRENT_C11_PROJECTION_DIRECT','CURRENT_C11_AUTHORITY_DIRECT','CURRENT_I03_QUERY_DIRECT',
  'C10_F03_RETURN_DIRECT','C10_F03_TRACE_DIRECT','C10_F03_REVIEW_DIRECT',
  'C11_F08_RETURN_DIRECT','C11_F08_TRACE_DIRECT','C11_F08_REVIEW_DIRECT',
  'D04_LMQ_DISPOSITIONS_DIRECT','D04_OPEN_GAPS_DIRECT','R5_SEED_CURRENT_JOIN',
  'VMC_CANDIDATE_FATES'
];
const fail = message => { throw new Error('ZAK_R2_REJECT: ' + message); };
const must = (test,message) => { if(!test) fail(message); };
function gitBlobOid(raw) {
  const bytes=Buffer.from(raw,'utf8');
  return crypto.createHash('sha1')
    .update(Buffer.from('blob '+bytes.length+'\0'))
    .update(bytes).digest('hex');
}
function loadTSV(filename) {
  const raw=fs.readFileSync(path.join(DIR,filename),'utf8');
  must(raw.endsWith('\n'),filename+' missing terminal newline');
  const lines=raw.trimEnd().split(/\r?\n/);
  const headers=lines.shift().split('\t');
  const rows=lines.map((line,i)=>{
    const cells=line.split('\t');
    must(cells.length===headers.length,filename+' ragged at row '+(i+2)+': '+cells.length+' vs '+headers.length);
    return Object.fromEntries(headers.map((header,j)=>[header,cells[j]]));
  });
  return {headers,rows};
}
function copyRows(rows){return rows.map(x=>({...x}));}
function originalBlob(columns,rows) {
  return gitBlobOid(columns.join('\t')+'\n'+rows.map(r=>columns.map(c=>r[c]).join('\t')).join('\n')+'\n');
}
function validate(registers) {
  const {obligations:O,sources:S,dispatch:D}=registers;
  must(O.rows.length===182,'inherited count != 182');
  must(S.rows.length===47,'direct-source references != 47');
  must(D.rows.length===13,'dispatch row count != 13 including 00R and 07E');
  const uniq=(arr,key,name)=>{
    const seen=new Set();for(const r of arr) {
      must(r[key]&&!seen.has(r[key]),name+' duplicate/missing key '+r[key]);
      seen.add(r[key]);
    }return seen;
  };
  const ok=uniq(O.rows,'zak_evidence_key','obligation');
  const sk=uniq(S.rows,'source_key','source');
  const dk=uniq(D.rows,'commission','dispatch');
  const oc={};for(const r of O.rows)oc[r.obligation_family]=(oc[r.obligation_family]||0)+1;
  must(JSON.stringify(Object.keys(FAMILY_COUNTS).sort().map(x=>[x,oc[x]]))===
    JSON.stringify(Object.keys(FAMILY_COUNTS).sort().map(x=>[x,FAMILY_COUNTS[x]])),
    '29/58/44/30/13/8 denominator mismatch');
  const origColumns=O.headers.slice(0,14),sourceColumns=S.headers.slice(0,14);
  must(originalBlob(origColumns,O.rows)===R1_SHA.obligations,'R1 inherited source columns changed');
  must(originalBlob(sourceColumns,S.rows.slice(0,26))===R1_SHA.sources,'original 26 source pins changed');
  const byID=new Map(O.rows.map(r=>[r.original_id,r]));
  for(const [stem,n] of [['F',29],['AR-',58],['LMX-',44],['LMQ-',30]]) {
    for(let i=1;i<=n;i++){
      const id=stem==='F'?'F'+String(i).padStart(2,'0'):stem+String(i).padStart(3,'0');
      if(stem==='F')must(O.rows.some(r=>r.original_id.startsWith(id+'_')),'missing F '+id);
      else must(byID.has(id),'missing '+id);
    }
  }
  for(const key of requiredSourceKeys)must(sk.has('ZAK:SRC:'+key),'missing direct source/receipt '+key);
  for(const s of S.rows){
    must(/^[a-f0-9]{40}$/.test(s.frozen_commit_sha),'bad immutable source commit '+s.source_key);
    must(/^[a-f0-9]{40}$/.test(s.git_blob_sha),'bad source blob '+s.source_key);
    for(const k of ['selected_authority_grade','executable_reader_grade','output_effect_grade',
      'first_consumer_grade','review_or_receiving_grade'])must(Boolean(s[k]),'ungraded direct source '+s.source_key+'/'+k);
  }
  let histSelected=0,histUnresolved=0, currentAccepted=0;
  for(const r of O.rows){
    for(const k of ['current_disposition_at_reviewed_source','current_disposition_source_key',
      'current_candidate_or_canonical_join','candidate_join_grade','current_successor_or_receipt',
      'specific_current_owner_route','investigative_commission','earliest_case_falsifier',
      'positive_execution_application_grade','current_receiving_status','source_to_reader_effect_edge']) {
      const v=r[k]||'';
      must(v.length>0 && !/^(TBD|UNKNOWN|UNASSIGNED|PLACEHOLDER)$/i.test(v),
        r.original_id+' missing '+k);
    }
    must(r.earliest_case_falsifier.includes(r.original_id),r.original_id+' falsifier not identity-specific');
    for(const cid of r.investigative_commission.split(';')){
      must(dk.has(cid),r.original_id+' references missing commission '+cid);
    }
    must(r.current_receiving_status==='NOT_INDEPENDENTLY_RECEIVED_AS_CURRENT_EXECUTION',
      r.original_id+' self-promotion of modern execution');
    must(r.source_to_reader_effect_edge==='NO_PROVED_ZAK_EDGE__SOURCE_JOIN_NOT_EFFECT',
      r.original_id+' invented effective edge without source-rule-consumer witness');
    if(r.obligation_family==='AUTHORITY_RELEASE') {
      must(r.current_disposition_source_key.includes('01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv#'+r.original_id),
        r.original_id+' missing exact C6 release-grain key');
      if(r.selected_or_inherited_state.includes('HISTORICAL_VERSION_UNRESOLVED')) histUnresolved++;
      else if(r.selected_or_inherited_state.includes('HISTORICAL_VERSION_SELECTED')) histSelected++;
      else fail(r.original_id+' unclassified selected-state');
    }
    if(r.obligation_family==='LEGACY_F_CLASS'||r.obligation_family==='LONG_MEMORY_REQUIREMENT') {
      must(r.current_disposition_source_key.includes('SEED_CURRENT_DISPOSITIONS_R5.tsv#'+r.original_id),
        r.original_id+' lacks exact R5 candidate row');
      must(r.candidate_join_grade.includes('NO_EQUIVALENCE') ||
        r.candidate_join_grade.includes('NOT_CURRENT_ACCEPTANCE'),
        r.original_id+' falsely accepts R5 identity-label match as successor equivalence');
    }
    if(r.current_receiving_status.includes('ACCEPT'))currentAccepted++;
  }
  must(histSelected===42&&histUnresolved===16,'historical 42 selected-state/16 unresolved broken: '+histSelected+'/'+histUnresolved);
  must(currentAccepted===0,'unexpected current acceptances');
  must(byID.get('LMQ-001').current_disposition_at_reviewed_source===
     'DISCHARGED_AS_COURT_EXISTENCE_TASK__CURRENT_MACHINE_ZERO_LOSS_NOT_PROVED',
     'LMQ-001 court completion confused with zero-loss acceptance');
  must(byID.get('LMQ-001').current_disposition_source_key.includes('D04_INFORMATION_REPLAY/LMQ001_LMQ009_DISPOSITION.md#LMQ-001'),
     'LMQ-001 missing actual D04 court source');
  must(byID.get('LMQ-009').current_disposition_at_reviewed_source.includes('NINE_C4_GRAINS'),
    'LMQ-009 actual nine open C4 gains not represented');
  for(const k of ['ZAK-00R',...'ZAK-01 ZAK-02 ZAK-03 ZAK-04 ZAK-05 ZAK-06 ZAK-07 ZAK-07E ZAK-08 ZAK-09 ZAK-10 ZAK-11'.split(' ')])
    must(dk.has(k),'missing control/commission '+k);
  const review=D.rows.find(r=>r.commission==='ZAK-00R');
  must(review.initial_review_issue.includes('/issues/884'),'missing initial independent receiving work item');
  must(review.independent_reviewer_identity==='REQUIRED__NOT_APPOINTED','unverified reviewer falsely appointed');
  must(review.investigation_status==='REVIEW_ISSUE_CREATED_NOT_LAUNCHED','false reviewer launch');
  for(const r of D.rows){
    must(r.actual_worker_launch_receipt==='NO_WORKER_LAUNCHED','invented launched worker '+r.commission);
    must(r.independently_accepted_result==='NONE__COMMISSION_NOT_EXECUTED_OR_RECEIVED' ||
      r.independently_accepted_result==='NONE__REVIEW_NOT_PERFORMED','commission self-accepted '+r.commission);
    must(r.initial_review_issue.includes('/issues/884'),'missing initial receiving gate '+r.commission);
  }
  for(const k of ['ZAK-01','ZAK-04','ZAK-05','ZAK-07','ZAK-08','ZAK-09','ZAK-10']){
    const r=D.rows.find(x=>x.commission===k);
    must(r.investigation_status.startsWith('READY_'),'artificial serial investigation hold '+k);
    must(!/ZAK-0[1-9]_ACCEPT|NATIVE_ISSUER_REQUIRED_BEFORE_STATIC/.test(r.investigation_permission_gate),
      'investigation improperly blocked by acceptance '+k);
    must(/SELECTED_ISSUER_RULE|NEVER_AUTO/.test(r.positive_acceptance_gate),
      'positive acceptance gate missing '+k);
  }
  must(D.rows.find(x=>x.commission==='ZAK-07E').investigation_status==='BLOCKED_OPTIONAL_NATIVE__NO_DISPATCH',
    'S3 native incorrectly launched');
  must(D.rows.find(x=>x.commission==='ZAK-01').next_bounded_artifact.includes('235-fate'),
     'ZAK-01 collapsed back to C6 denominator');
  return {ok:true,sourceReferences:S.rows.length,inheritedRows:O.rows.length,
    dispatchRows:D.rows.length,historicalSelected:histSelected,historicalUnresolved:histUnresolved,
    reviewIssue:884,independentReview:'PENDING',workerLaunches:0,authorityPromotion:'NONE'};
}
const regs=Object.fromEntries(Object.entries(FILES).map(([k,f])=>[k,loadTSV(f)]));
const status=validate(regs);
if(process.argv.includes('--negative-controls')){
  const cases=[
    ['drop inherited obligation',x=>{x.obligations.rows=x.obligations.rows.filter(r=>r.original_id!=='LMX-043');}],
    ['mutate original preserved cell',x=>{x.obligations.rows[0].inherited_label+=' CORRUPTED';}],
    ['collapse 42/16 release distinction',x=>{const r=x.obligations.rows.find(y=>y.original_id==='AR-0005');r.selected_or_inherited_state='HISTORICAL_VERSION_UNRESOLVED / POINTER';}],
    ['erase individual falsifier',x=>{x.obligations.rows.find(r=>r.original_id==='LMQ-002').earliest_case_falsifier='TBD';}],
    ['forge modern accepted receipt',x=>{x.obligations.rows.find(r=>r.original_id==='LMX-002').current_receiving_status='ACCEPTED_CURRENT';}],
    ['serialize static investigation',x=>{x.dispatch.rows.find(r=>r.commission==='ZAK-04').investigation_status='HELD_UNTIL_ZAK01_ACCEPTED';}],
    ['remove initial independent gate',x=>{x.dispatch.rows=x.dispatch.rows.filter(r=>r.commission!=='ZAK-00R');}],
    ['falsify the D04 zero-loss verdict',x=>{x.obligations.rows.find(r=>r.original_id==='LMQ-001').current_disposition_at_reviewed_source='CURRENT_MACHINE_ZERO_LOSS_PROVED';}],
    ['omit high-impact direct historical code',x=>{x.sources.rows=x.sources.rows.filter(r=>r.source_key!=='ZAK:SRC:LEGACY_V549B_DIRECT');}],
    ['invent source/consumer edge',x=>{x.obligations.rows.find(r=>r.original_id==='F08_Q_USE').source_to_reader_effect_edge='PROVED_NATIVE_ALLOW';}]
  ];
  const negatives=[];
  for(const [name,mutation] of cases){
    const clone=Object.fromEntries(Object.entries(regs).map(([k,v])=>[k,{headers:[...v.headers],rows:copyRows(v.rows)}]));
    mutation(clone);
    let rejected=false;
    try { validate(clone); } catch(e) { rejected=true;negatives.push({test:name,result:'REJECT',reason:e.message}); }
    if(!rejected) fail('NEGATIVE_TEST_FALSE_PASS: '+name);
  }
  console.log(JSON.stringify({status,negatives},{},2));
}else console.log(JSON.stringify(status,null,2));
