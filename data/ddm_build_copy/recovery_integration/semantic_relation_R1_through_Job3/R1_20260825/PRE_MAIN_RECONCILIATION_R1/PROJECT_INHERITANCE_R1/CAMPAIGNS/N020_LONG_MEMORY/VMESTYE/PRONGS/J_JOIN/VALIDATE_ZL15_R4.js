/* Independent read-only structural court of ZL-15 R4 residual author repairs. */
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert'),cp=require('child_process');
const args=process.argv.slice(2),arg=(n,d)=>args.includes(n)?args[args.indexOf(n)+1]:d;
const root=path.resolve(arg('--root',path.resolve(__dirname,'../..')));
const validator=path.join(__dirname,'VALIDATE_ZL15_R3.js');
const priorArgs=['--root',root];for(const n of ['--p0','--seams','--sorok'])if(args.includes(n))priorArgs.push(n,arg(n,''));
const earlier=JSON.parse(cp.execFileSync(process.execPath,[validator,...priorArgs],{encoding:'utf8',maxBuffer:2*1024*1024}));
assert.strictEqual(earlier.negative_controls,11,'R3 source/graph controls were not honored');
function parse(r){const lines=fs.readFileSync(path.join(root,r),'utf8').trimEnd().split(/\r?\n/),h=lines.shift().split('\t');let seen=new Set();const rows=lines.filter(Boolean).map((line,i)=>{const cells=line.split('\t');assert.strictEqual(cells.length,h.length,r+' width '+(i+2));const x=Object.fromEntries(h.map((k,j)=>[k,cells[j]]));assert(x[h[0]]&&!seen.has(x[h[0]]),'duplicate primary '+r);seen.add(x[h[0]]);return x});return rows}
const impl=parse('DATA/IMPLEMENTATIONS.tsv'),rel=parse('DATA/RELATIONS.tsv'),stage=parse('PRONGS/J_JOIN/GENERATION_STAGE_COURT.tsv'),ev=parse('DATA/EVIDENCE.tsv'),nodes=parse('PRONGS/J_JOIN/SEAM_DEPENDENCY_NODES.tsv'),transfers=parse('PRONGS/J_JOIN/CANDIDATE_TRANSFERS.tsv'),seams=parse('PRONGS/J_JOIN/SEAM_DEPENDENCIES.tsv'),bridge=parse('PRONGS/J_JOIN/E001_SOURCE_RECIPIENT_BRIDGE_R4.tsv'),edges=parse('DATA/CONSUMER_EDGES.tsv'),auth=parse('DATA/AUTHORITY_APPLICATIONS.tsv');
const E=new Map(ev.map(r=>[r.evidence_id,r])),N=new Map(nodes.map(r=>[r.node_id,r])),seamBy=new Map(seams.map(x=>[x.seam_edge_id,x]));
const sourceBytes=fs.readFileSync(path.join(root,'PRONGS/J_JOIN/FROZEN_INPUTS/SOROK_VERSIONED_SEAMS_37915.jsonl'));
const blob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
assert.strictEqual(blob(sourceBytes),'d31eef4f4bc3f4fc6a32ba3e6563c788713f6c47');
const sourceE=sourceBytes.toString('utf8').trimEnd().split('\n').map(JSON.parse).find(x=>x.record_type==='VERSIONED_SEAM'&&x.seam_id==='E001');
assert(sourceE&&/NONE_PROVEN/.test(sourceE.actual_consumer_or_none.callable_or_none),'Sorok source native negative altered');
const EID='J-EV-R3-SOROK-E001',F='J-F-ZL12-F-E001',to='J-SEAM-NODE-5fb36fd14859ce80d2',LINK='JR-R4-E001-FINDING-TO-RECIPIENT';
const e001=E.get(EID);assert(e001&&e001.source_sha==='37915a47ed3e33a71ad8334c0aa505f5d65796ca');
assert(e001.line_range_or_row_id.includes('BLOB='+blob(sourceBytes))&&e001.original_native_or_sourcefree==='NO_NATIVE_SOROK_IMPORT');
const codeVerified='J-IM-ZL12-F-N10E';
const clone=x=>JSON.parse(JSON.stringify(x));
function check(i=impl,r=rel,s=stage,t=transfers,fromEvidence=e001,b=bridge){
 assert.strictEqual(i.length,884);assert.strictEqual(r.length,8503);assert.strictEqual(s.length,4420);
 let nUnknown=0,nVerified=0;
 for(const im of i){
  assert(im.reported_code_locator&&im.reported_code_locator!=='UNRESOLVED','source report locator lost');
  assert.notStrictEqual(im.code_symbol,im.reported_code_locator,'report locator leaked into code_symbol');
  if(im.code_sha==='NOT_PROVED_CODE'){
   assert.strictEqual(im.code_symbol,'NOT_PROVED_CODE_SYMBOL','unverified executable symbol claimed');
   assert(im.underlying_code_sha==='NOT_PROVED_CODE'&&im.underlying_code_path_symbol==='NOT_PROVED_SYMBOL');nUnknown++;
  }else{
   assert.strictEqual(im.implementation_id,codeVerified,'unreviewed code verification');
   assert.strictEqual(im.code_sha,'256d46bf425cc37e114465cddbe3c60e535766ab');
   assert.strictEqual(im.code_symbol,im.underlying_code_path_symbol);
   assert.strictEqual(im.code_symbol,'rawlsing_next/pre553_empirical_possibility_provider.py#provide_empirical_possibility_slice');
   assert.strictEqual(im.underlying_code_blob_sha,'23167aa25291fb148b1e3cf210ac33fe7769b783');nVerified++;
  }
 }
 assert.strictEqual(nUnknown,883);assert.strictEqual(nVerified,1);
 assert(N.get(to)?.literal_endpoint==='SOROK:E001','wrong recipient namespace');
 assert(fromEvidence.evidence_id===EID&&fromEvidence.original_native_or_sourcefree==='NO_NATIVE_SOROK_IMPORT','E001 receipt mutated');
 assert.strictEqual(r.filter(x=>x.relation_id===LINK).length,1,'E001 source-to-recipient link missing');
 const l=r.find(x=>x.relation_id===LINK);assert(l.from_id===F&&l.to_id===to&&l.evidence_id===EID,'E001 source recipient wrong endpoint/evidence');
 assert(l.relation_type.includes('CANDIDATE')&&l.relation_type.includes('OWNER_HELD')&&l.grade.includes('NOT_SEMANTIC_SUCCESSION_OR_NATIVE_EXECUTION'),'false native E001 bridge');
 for(const name of ['DVA','TRII','CHETIRI','LONG_MEMORY','PYAT_CURRENT']){
  const id='J-STAGE-ZL12-F-E001-'+name,q=s.find(x=>x.stage_court_id===id);
  assert(q&&q.finding_id===F&&q.corroborating_evidence_id===EID&&q.join_disposition.includes('SEMANTIC_SUCCESSION_UNJOINED'),'stage E001 identity misgraded');
  assert(q.join_disposition.includes('HISTORICAL_E001_IDENTITY_WITNESS_ONLY')&&q.next_falsifier.includes('not this generation-stage succession'),'E001 stage evidence inflated');
  const edge=r.find(x=>x.relation_id==='JR-R3-STAGE-ZL12-F-E001-'+name);
  assert(edge&&edge.from_id===F&&edge.to_id===id&&edge.evidence_id===EID&&edge.grade.includes('SOURCE_E001_IDENTITY_ONLY'),'E001 stage relation not evidenced');
 }
 const other=s.filter(x=>x.corroborating_evidence_id==='UNRESOLVED_EVIDENCE');assert.strictEqual(other.length,90,'unrelated source stage holes overwritten');
 for(const name of ['N11','N12'])assert(t.some(x=>x.transfer_id==='J-R3-E001-REQUIRES-'+name&&x.receiver_node_id===to&&x.exact_evidence_id===EID&&x.actual_first_reader_status==='NONE_PROVEN_SOROK_C11_NATIVE'),'N11/N12 owner/native hold changed');
 assert(seamBy.get('ASTRA:REQ:N10W:N11')?.original_requiredness==='MUST');
 const must=seamBy.get('ASTRA:REQ:N10W:N11');assert(r.some(x=>x.relation_id===must.relation_id&&x.from_id===must.from_node_id&&x.to_id===must.to_node_id),'N10W->N11 candidate path severed');
 // Explicit cold walk, ignoring edge direction only for reverse producer lookup.
 const adjacency=new Map();for(const x of r){if(!adjacency.has(x.from_id))adjacency.set(x.from_id,new Set());if(!adjacency.has(x.to_id))adjacency.set(x.to_id,new Set());adjacency.get(x.from_id).add(x.to_id);adjacency.get(x.to_id).add(x.from_id)}
 const reached=new Set([F]),queue=[F];while(queue.length){const x=queue.shift();for(const n of adjacency.get(x)||[])if(!reached.has(n)){reached.add(n);queue.push(n)}}
 assert(reached.has(to),'E001 cold finding->recipient disconnected');
 for(const n of ['N11','N12']){const record=[...N.values()].find(x=>x.literal_endpoint==='PYAT:ASTRA:'+n);assert(record&&reached.has(record.node_id),'E001 cannot reverse to '+n)}
 assert(reached.has(must.from_node_id),'E001 cannot reverse through N10W prerequisite');
 assert.strictEqual(b.length,1);const side=b[0];assert(side.finding_id===F&&side.recipient_node_id===to&&side.relation_id===LINK&&side.historical_evidence_id===EID);
 assert(side.stage_evidence_scope.includes('NOT_STAGE_FATE_PROOF')&&side.sorok_consumer==='NONE_PROVEN_NATIVE_SOROK_C11_IMPORTER');
 assert(edges.every(x=>x.current_actual_status==='OPEN_PROOF_GAP'&&x.actual_call_site_sha==='NOT_PROVED'));
 assert(auth.every(x=>x.rule_applied_to_output!=='YES'&&x.negative_or_refusal_enforced!=='YES'));
}
check();
let negatives=0;function refuse(name,fn){let failed=false;try{fn()}catch(_){failed=true}assert(failed,'R4 mutation not rejected '+name);negatives++}
refuse('unverified-report-into-code_symbol',()=>{const x=clone(impl),r=x.find(y=>y.code_sha==='NOT_PROVED_CODE');r.code_symbol=r.reported_code_locator;check(x)});
refuse('verified-report-into-code_symbol',()=>{const x=clone(impl),r=x.find(y=>y.implementation_id===codeVerified);r.code_symbol=r.reported_code_locator;check(x)});
refuse('raw-report-locator-erased',()=>{const x=clone(impl);x[0].reported_code_locator='UNRESOLVED';check(x)});
refuse('E001-link-deleted',()=>{const x=clone(rel).filter(y=>y.relation_id!==LINK);check(impl,x)});
refuse('E001-recipient-mistargeted',()=>{const x=clone(rel);x.find(y=>y.relation_id===LINK).to_id='J-IDENT-SOROK:E001';check(impl,x)});
refuse('E001-link-unevidenced',()=>{const x=clone(rel);x.find(y=>y.relation_id===LINK).evidence_id='UNRESOLVED';check(impl,x)});
refuse('E001-stage-unevidenced',()=>{const x=clone(stage);x.find(y=>y.stage_court_id==='J-STAGE-ZL12-F-E001-DVA').corroborating_evidence_id='UNRESOLVED_EVIDENCE';check(impl,rel,x)});
refuse('E001-stage-false-green',()=>{const x=clone(stage);x.find(y=>y.stage_court_id==='J-STAGE-ZL12-F-E001-DVA').join_disposition='PROVED_SUCCESSION';check(impl,rel,x)});
refuse('E001-native-consumer-false-green',()=>{const x=clone(transfers);x.find(y=>y.transfer_id==='J-R3-E001-REQUIRES-N11').actual_first_reader_status='PROVED_NATIVE';check(impl,rel,stage,x)});
refuse('E001-negative-witness-mutated',()=>{const x=clone(e001);x.original_native_or_sourcefree='NATIVE_PASS';check(impl,rel,stage,transfers,x)});
refuse('N10W-source-reverse-severance',()=>{const x=clone(rel).filter(y=>y.relation_id!==seamBy.get('ASTRA:REQ:N10W:N11').relation_id);check(impl,x)});
console.log(JSON.stringify({terminal:'ZL15_R4_S0_S1_READ_ONLY_GRAPH_TEST_PASS__INDEPENDENT_ZL16_PENDING',r3_controls:earlier.negative_controls,r4_mutation_controls:negatives,implementations:impl.length,code_symbol_unknown:883,code_symbol_verified_static:1,relation_count:rel.length,e001_evidence_linked_stages:5,remaining_other_stage_evidence_holes:90,actual_native_importer:'NONE_PROVEN',s2_s3:'NOT_RUN'},null,2));
