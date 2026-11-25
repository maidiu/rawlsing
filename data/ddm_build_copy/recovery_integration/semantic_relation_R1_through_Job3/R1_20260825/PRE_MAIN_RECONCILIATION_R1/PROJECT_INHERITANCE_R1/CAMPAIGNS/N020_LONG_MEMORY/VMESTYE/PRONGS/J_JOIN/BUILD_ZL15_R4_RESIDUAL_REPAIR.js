/*
 * VMESTYE ZL-15 R4: exact R3@ffd9940453 -> bounded ZL16-R2-D05/D06 repair.
 * Documentary S0-S1 only; not original35, project CI, actor, science or issuer.
 * Run only on the author R3 source tree at exact ffd994045319db496e642cd797b01b615cc85a24.
 *   node PRONGS/J_JOIN/BUILD_ZL15_R4_RESIDUAL_REPAIR.js
 * On the resulting R4 tree use VALIDATE_ZL15_R4.js (read-only).
 */
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert');
const args=process.argv.slice(2),arg=(n,d)=>args.includes(n)?args[args.indexOf(n)+1]:d;
const root=path.resolve(arg('--root',path.resolve(__dirname,'../..')));
const locations={
  implementations:'DATA/IMPLEMENTATIONS.tsv',
  relations:'DATA/RELATIONS.tsv',
  stages:'PRONGS/J_JOIN/GENERATION_STAGE_COURT.tsv',
  evidence:'DATA/EVIDENCE.tsv',
  nodes:'PRONGS/J_JOIN/SEAM_DEPENDENCY_NODES.tsv',
  transfers:'PRONGS/J_JOIN/CANDIDATE_TRANSFERS.tsv',
  sorok:'PRONGS/J_JOIN/FROZEN_INPUTS/SOROK_VERSIONED_SEAMS_37915.jsonl'
};
const r3Blobs={implementations:'6b64cadfde02ec66cdc97e9d432ab2b82a251555',relations:'2483f7b798352c118b4d208cbcf4c8c1772eb15a',stages:'78f9ed413cc6263e6a39b0fe884eea449c44ae49',evidence:'75d6e2d29425b5f6438cd7808b1487bfd4e2691c',nodes:'19168ab976059d03b04632e81f5061397df7efd1',transfers:'1b3f7483f2a05f13d54e82e9adee84e8a0406de9',sorok:'d31eef4f4bc3f4fc6a32ba3e6563c788713f6c47'};
const gitBlob=bytes=>crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
function parse(bytes,name){const lines=bytes.toString('utf8').trimEnd().split(/\r?\n/),h=lines.shift().split('\t');let ids=new Set();const rows=lines.filter(Boolean).map((l,i)=>{const p=l.split('\t');assert.strictEqual(p.length,h.length,name+' row width '+(i+2));const r=Object.fromEntries(h.map((k,j)=>[k,p[j]]));assert(r[h[0]]&&!ids.has(r[h[0]]),name+' duplicate PK');ids.add(r[h[0]]);return r});return {h,rows}}
const serialize=t=>t.h.join('\t')+'\n'+t.rows.map(r=>t.h.map(k=>String(r[k]??'').replace(/[\t\r\n]+/g,' ').trim()).join('\t')).join('\n')+'\n';
const source={};for(const [n,rel]of Object.entries(locations)){
 const bytes=fs.readFileSync(path.join(root,rel));assert.strictEqual(gitBlob(bytes),r3Blobs[n],'requires exact R3 input: '+rel);
 source[n]=n==='sorok'?bytes.toString('utf8').trimEnd().split('\n').map(JSON.parse):parse(bytes,n);
}
const I=source.implementations,R=source.relations,S=source.stages,E=source.evidence,N=source.nodes,T=source.transfers;
assert.strictEqual(I.rows.length,884);assert.strictEqual(R.rows.length,8502);assert.strictEqual(S.rows.length,4420);
const ev=new Map(E.rows.map(x=>[x.evidence_id,x]));
const e001='J-EV-R3-SOROK-E001',e=ev.get(e001);
assert(e&&e.source_sha==='37915a47ed3e33a71ad8334c0aa505f5d65796ca');
assert(e.line_range_or_row_id.includes('BLOB='+r3Blobs.sorok));
const sorokE=source.sorok.find(x=>x.record_type==='VERSIONED_SEAM'&&x.seam_id==='E001');
assert(sorokE&&sorokE.producer.callable_or_required.includes('N11/N12'));
assert(/NONE_PROVEN/.test(sorokE.actual_consumer_or_none.callable_or_none));
const nodeId='J-SEAM-NODE-'+crypto.createHash('sha256').update('SOROK:E001').digest('hex').slice(0,18);
assert.strictEqual(nodeId,'J-SEAM-NODE-5fb36fd14859ce80d2');
assert(N.rows.some(x=>x.node_id===nodeId&&x.literal_endpoint==='SOROK:E001'));
for(const n of ['N11','N12'])assert(T.rows.some(x=>x.transfer_id==='J-R3-E001-REQUIRES-'+n&&x.receiver_node_id===nodeId&&x.exact_evidence_id===e001&&x.actual_first_reader_status==='NONE_PROVEN_SOROK_C11_NATIVE'));

// R2-D05: normalize original typed code_symbol, retaining every report locator.
let unknown=0,verified=0;
for(const im of I.rows){
 assert.strictEqual(im.code_symbol,im.reported_code_locator,'R3 raw pointer changed unexpectedly');
 if(im.code_sha==='NOT_PROVED_CODE'){
  assert(im.underlying_code_sha==='NOT_PROVED_CODE'&&im.underlying_code_path_symbol==='NOT_PROVED_SYMBOL');
  im.code_symbol='NOT_PROVED_CODE_SYMBOL';unknown++;
 }else{
  assert.strictEqual(im.implementation_id,'J-IM-ZL12-F-N10E','unverified extra code claim');
  assert.strictEqual(im.code_sha,'256d46bf425cc37e114465cddbe3c60e535766ab');
  assert.strictEqual(im.underlying_code_blob_sha,'23167aa25291fb148b1e3cf210ac33fe7769b783');
  assert.strictEqual(im.underlying_code_path_symbol,'rawlsing_next/pre553_empirical_possibility_provider.py#provide_empirical_possibility_slice');
  im.code_symbol=im.underlying_code_path_symbol;verified++;
 }
}
assert.strictEqual(unknown,883);assert.strictEqual(verified,1);

// R2-D06: a source-qualified link to E001 identity/recipient, not proof of native receipt.
const F='J-F-ZL12-F-E001',stageNames=['DVA','TRII','CHETIRI','LONG_MEMORY','PYAT_CURRENT'];
const stageIds=[];for(const name of stageNames){
 const sid='J-STAGE-ZL12-F-E001-'+name;
 const s=S.rows.find(x=>x.stage_court_id===sid&&x.finding_id===F);assert(s,'missing E001 stage '+name);
 assert.strictEqual(s.corroborating_evidence_id,'UNRESOLVED_EVIDENCE');
 assert(s.join_disposition.includes('SEMANTIC_SUCCESSION_UNJOINED'));
 s.corroborating_evidence_id=e001;
 s.join_disposition+='__HISTORICAL_E001_IDENTITY_WITNESS_ONLY';
 s.next_falsifier+='; E001 receipt witnesses historical identity/recipient contract ONLY, not this generation-stage succession';
 const link=R.rows.find(x=>x.relation_id==='JR-R3-STAGE-ZL12-F-E001-'+name&&x.from_id===F&&x.to_id===sid);
 assert(link&&link.evidence_id==='UNRESOLVED_EVIDENCE');link.evidence_id=e001;
 link.grade+='__SOURCE_E001_IDENTITY_ONLY';
 link.comment+='; exact E001 witness supports identity/recipient ONLY; intermediate Dva/Trii/Chetiri/LM/Pyat stage effect remains unproved';
 stageIds.push(sid);
}
const linkId='JR-R4-E001-FINDING-TO-RECIPIENT';
assert(!R.rows.some(x=>x.relation_id===linkId));
R.rows.push({relation_id:linkId,from_id:F,
 relation_type:'HISTORICAL_E001_IDENTITY_TO_SOROK_RECIPIENT_CANDIDATE__OWNER_HELD',to_id:nodeId,
 generation_from:'ZL12_SOROK_W7_HISTORICAL_SOURCE',generation_to:'SOROK_PRE_V3_RECIPIENT_CANDIDATE',
 applicability_or_condition:'EXACT_E001_ORIGINAL_IDENTITY_AND_N11_N12_REQUIRED_CONTRACT__NATIVE_IMPORT_NONE_PROVEN__OWNER_CONSENT_AND_READSET_HELD',
 operation_or_authority_id:'SOROK:E001__NOT_PYAT_EMPIRICAL_C11',evidence_id:e001,
 at_cut:'37915a47ed3e33a71ad8334c0aa505f5d65796ca',
 grade:'S1_EXACT_HISTORICAL_E001_IDENTITY_RECIPIENT__NOT_SEMANTIC_SUCCESSION_OR_NATIVE_EXECUTION',
 comment:'Source cut 37915a47 and blob d31eef4f frozen; distinct Sorok actor C11 from Pyat empirical C11. Requires N11/N12 qualified release, Sorok receiver consent/readset/retention and actual native importer; NONE_PROVEN'});
assert.strictEqual(R.rows.length,8503);
const bridge={
 bridge_id:'J-R4-E001-SOURCE_TO_RECIPIENT',finding_id:F,recipient_node_id:nodeId,relation_id:linkId,
 historical_evidence_id:e001,source_cut:'37915a47ed3e33a71ad8334c0aa505f5d65796ca',source_blob:r3Blobs.sorok,
 stage_ids:stageIds.join(';'),stage_evidence_scope:'EXACT_E001_IDENTITY_AND_RECIPIENT_CONTRACT_ONLY__NOT_STAGE_FATE_PROOF',
 n11_n12_gate:'OWNER_HELD__NO_SELECTED_NATIVE_RELEASE',sorok_consumer:'NONE_PROVEN_NATIVE_SOROK_C11_IMPORTER',
 namespace_refusal:'PRE553_EMPIRICAL_C11_IS_NOT_SOROK_ACTOR_C11',proof_grade:'S1_TYPED_CANDIDATE_UNJOIN__NOT_NATIVE'
};
const bridgeHeader='bridge_id\tfinding_id\trecipient_node_id\trelation_id\thistorical_evidence_id\tsource_cut\tsource_blob\tstage_ids\tstage_evidence_scope\tn11_n12_gate\tsorok_consumer\tnamespace_refusal\tproof_grade';
const B={h:bridgeHeader.split('\t'),rows:[bridge]};
// A local self-check is not independent acceptance; R4 verifier adds hostile mutations.
assert(I.rows.every(x=>x.code_sha==='NOT_PROVED_CODE'?x.code_symbol==='NOT_PROVED_CODE_SYMBOL':x.code_symbol===x.underlying_code_path_symbol));
assert(R.rows.some(x=>x.relation_id===linkId&&x.to_id===nodeId&&x.evidence_id===e001));
for(const name of stageNames)assert(S.rows.find(x=>x.stage_court_id==='J-STAGE-ZL12-F-E001-'+name).corroborating_evidence_id===e001);
for(const [n,t]of [['implementations',I],['relations',R],['stages',S]])fs.writeFileSync(path.join(root,locations[n]),serialize(t));
fs.writeFileSync(path.join(root,'PRONGS/J_JOIN/E001_SOURCE_RECIPIENT_BRIDGE_R4.tsv'),serialize(B));
console.log(JSON.stringify({terminal:'ZL15_R4_R2_D05_D06_MATERIALIZED__NOT_INDEPENDENTLY_ACCEPTED',code_symbols_unknown:unknown,code_symbols_s1_verified:verified,relations:R.rows.length,e001_stage_receipts:5,e001_new_candidate_links:1,other_stage_unresolved_unchanged:90,original_native:'NOT_RUN',actual_actor_reader:'NONE_PROVEN'},null,2));
