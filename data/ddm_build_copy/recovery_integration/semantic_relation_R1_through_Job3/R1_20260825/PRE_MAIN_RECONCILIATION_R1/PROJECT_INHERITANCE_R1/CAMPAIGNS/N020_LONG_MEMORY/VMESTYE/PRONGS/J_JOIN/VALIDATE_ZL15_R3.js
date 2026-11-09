/* Independent read-only R3 documentary table court. No source execution or merge. */
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert');
const args=process.argv.slice(2),arg=(n,d)=>args.includes(n)?args[args.indexOf(n)+1]:d;
const root=path.resolve(arg('--root',path.resolve(__dirname,'../..')));
const p0Path=path.resolve(arg('--p0',path.join(root,'CONTROL/P0_RETURN_AND_BRANCH_CENSUS.tsv')));
const seamPath=path.resolve(arg('--seams',path.join((()=>{let p=root;while(!fs.existsSync(path.join(p,'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl'))){let n=path.dirname(p);if(n===p)return root;p=n}return p})(),'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl')));
const sorokPath=path.resolve(arg('--sorok',path.join(root,'PRONGS/J_JOIN/FROZEN_INPUTS/SOROK_VERSIONED_SEAMS_37915.jsonl')));
function parse(s,n){let l=s.trimEnd().split(/\r?\n/),h=l.shift().split('\t');const rows=l.filter(Boolean).map((x,i)=>{let a=x.split('\t');assert.strictEqual(a.length,h.length,n+' width '+i);return Object.fromEntries(h.map((v,j)=>[v,a[j]]))});let ids=new Set();for(let r of rows){assert(r[h[0]]&&(!ids.has(r[h[0]])),n+' duplicate');ids.add(r[h[0]])}return rows}
const read=r=>parse(fs.readFileSync(path.join(root,r),'utf8'),r);
const blob=(buf)=>crypto.createHash('sha1').update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex');
const origBytes=fs.readFileSync(p0Path),seamBytes=fs.readFileSync(seamPath);
const sorokBytes=fs.readFileSync(sorokPath);
assert.strictEqual(blob(origBytes),'65c1bbe4a602341c5caacca2d58dced31a23f382');
assert.strictEqual(blob(seamBytes),'5a951626c0dde91b682eb23216c88dbfc054808d');
assert.strictEqual(blob(sorokBytes),'d31eef4f4bc3f4fc6a32ba3e6563c788713f6c47');
const p0=parse(origBytes.toString('utf8'),'P0'),seams=seamBytes.toString('utf8').trimEnd().split('\n').map(JSON.parse);
const sorok=sorokBytes.toString('utf8').trimEnd().split('\n').map(JSON.parse),e001=sorok.find(x=>x.record_type==='VERSIONED_SEAM'&&x.seam_id==='E001');
assert(e001&&/NONE_PROVEN/.test(e001.actual_consumer_or_none.callable_or_none),'Sorok exact historical E001 owner/native negative missing');
const names=['FUNCTION_ATLAS','RELATIONS','OPERATION_TRACES','AUTHORITY_APPLICATIONS','EVIDENCE','IMPLEMENTATIONS','CONSUMER_EDGES','DECISION_EVENTS'];
const d=Object.fromEntries(names.map(x=>[x,read('DATA/'+x+'.tsv')]));
const left=read('PRONGS/J_JOIN/P0_LEFT_DISPOSITIONS.tsv'),stage=read('PRONGS/J_JOIN/GENERATION_STAGE_COURT.tsv'),bridge=read('PRONGS/J_JOIN/CROSS_PRONG_BRIDGES.tsv'),seam=read('PRONGS/J_JOIN/SEAM_DEPENDENCIES.tsv'),nodes=read('PRONGS/J_JOIN/SEAM_DEPENDENCY_NODES.tsv'),transfer=read('PRONGS/J_JOIN/CANDIDATE_TRANSFERS.tsv'),conflict=read('PRONGS/J_JOIN/CONFLICTS_AND_REPAIR_ORDER.tsv'),anti=read('PRONGS/J_JOIN/FULL_ID_ANTI_JOINS.tsv');
const map=(rows,k)=>new Map(rows.map(x=>[x[k],x]));
const P=map(p0,'census_id'), L=map(left,'census_id'), E=map(d.EVIDENCE,'evidence_id'), O=map(d.OPERATION_TRACES,'operation_id'), CE=map(d.CONSUMER_EDGES,'edge_id'), C=map(conflict,'conflict_id'), SE=map(seam,'seam_edge_id'), N=map(nodes,'node_id'), S=map(stage,'stage_court_id');
const all=new Set([...d.FUNCTION_ATLAS.map(x=>x.record_id),...O.keys(),...CE.keys(),...d.AUTHORITY_APPLICATIONS.map(x=>x.application_id),...C.keys(),...left.map(x=>x.source_node_id),...N.keys(),...S.keys()]);
const tup=x=>JSON.stringify([x.estate_id,x.source_commit_sha,x.source_path,x.source_composite_id,x.record_grain??x.source_grain]);
function check(rel=d.RELATIONS,ops=d.OPERATION_TRACES,edges=d.CONSUMER_EDGES,auth=d.AUTHORITY_APPLICATIONS,impl=d.IMPLEMENTATIONS,sea=seam,lef=left){
 assert.strictEqual(lef.length,6125,'left census loss');assert.strictEqual(lef.filter(x=>x.prong_observations==='NONE_EXACT').length,4256,'left disposition count drift');
 for(const r of lef){assert(P.has(r.census_id)&&tup(P.get(r.census_id))===tup(r),'P0 identity substituted');assert(r.new_function_count_increment==='0','false function inflation')}
 const rowsByType={};for(const r of rel){rowsByType[r.relation_type]=(rowsByType[r.relation_type]||0)+1;
  if(r.relation_type==='HELD_BY'||r.relation_id.startsWith('JR-R3-')){assert(all.has(r.from_id),'relation from endpoint unresolved '+r.relation_id);assert(all.has(r.to_id),'relation to endpoint unresolved '+r.relation_id)}
  if(r.relation_id.startsWith('JR-R3-'))assert(['UNRESOLVED','UNRESOLVED_EVIDENCE'].includes(r.evidence_id)||E.has(r.evidence_id),'invalid new evidence ID')
 }
 assert.strictEqual(rowsByType.HELD_BY,1868,'holds lost');
 assert.strictEqual(rel.filter(x=>x.relation_type==='HELD_BY'&&x.to_id.startsWith('C-')).length,1536,'unrepaired conflict FK');
 assert.strictEqual(rel.filter(x=>x.relation_type==='HELD_BY'&&x.from_id.startsWith('J-P0-')).length,241,'source anchor count drift');
 for(const c of C.values())assert(rel.some(x=>x.relation_type==='HELD_BY'&&x.to_id===c.conflict_id),'unlinked original unjoin');
 for(const o of ops)assert(CE.has(o.producer_edge_id),'operation producer edge dangling');
 for(const e of edges){assert(O.has(e.producer_operation_id),'producer operation dangling');assert(e.consumer_operation_id==='UNRESOLVED'||O.has(e.consumer_operation_id),'consumer string in normalized ID');
  assert(E.has(e.negative_evidence_id)||e.negative_evidence_id==='UNRESOLVED_NEGATIVE','negative provenance placeholder');
  assert(e.current_actual_status==='OPEN_PROOF_GAP'&&e.actual_call_site_sha==='NOT_PROVED','unearned actual reader')}
 for(const a of auth){assert(a.evidence_ids==='UNRESOLVED_EVIDENCE'||a.evidence_ids.split(';').every(id=>E.has(id)),'authority evidence bogus');
  assert(a.rule_applied_to_output!=='YES'&&a.negative_or_refusal_enforced!=='YES','unearned applied/negative enforcement')}
 for(const im of impl){assert(im.code_sha==='NOT_PROVED_CODE'||/^[a-f0-9]{40}$/.test(im.code_sha),'not a code SHA');
  if(im.code_sha!=='NOT_PROVED_CODE')assert(im.code_sha===im.underlying_code_sha&&/\.py#/.test(im.underlying_code_path_symbol),'code SHA/path unsound')}
 assert.strictEqual(sea.length,82,'seam drop');for(let i=0;i<82;i++){const o=seams[i],s=sea[i];assert.strictEqual(s.seam_edge_id,o.edge_id,'wrong source seam');
  assert.strictEqual(s.original_requiredness,o.original_requiredness,'IF/MUST/OR changed');assert.strictEqual(s.literal_predicate,o.original_predicate||o.original_G2.edge_condition,'condition changed');
  assert(E.has(s.canonical_evidence_id),'no evidence for seam');assert(N.has(s.from_node_id)&&N.has(s.to_node_id),'seam endpoint unresolved');
  const r=rel.find(r=>r.relation_id===s.relation_id);assert(r&&r.from_id===s.from_node_id&&r.to_id===s.to_node_id&&r.applicability_or_condition.includes(s.literal_predicate),'nontraversable seam')}
 assert.strictEqual(stage.length,4420,'stage court missing');for(const s of stage)assert(all.has(s.finding_id)&&(['UNRESOLVED','UNRESOLVED_EVIDENCE'].includes(s.corroborating_evidence_id)||E.has(s.corroborating_evidence_id)),'stage evidence/finding');
 for(const b of bridge)assert(d.FUNCTION_ATLAS.some(f=>f.record_id===b.from_finding_id)&&d.FUNCTION_ATLAS.some(f=>f.record_id===b.to_finding_id),'historical crossbridge missing');
 const e001=N.get(transfer.find(x=>x.transfer_id==='J-R3-E001-REQUIRES-N11')?.receiver_node_id);assert(e001?.literal_endpoint==='SOROK:E001','Sorok cold reverse broken');
 assert(transfer.some(x=>x.transfer_id==='J-R3-E001-REQUIRES-N12'),'Sorok N12 dependency absent');
 assert(sea.some(x=>x.seam_edge_id==='ASTRA:REQ:N10W:N11'&&x.original_requiredness==='MUST'),'N10W->N11 lost');
}
check();
const mutate=x=>JSON.parse(JSON.stringify(x)),hostile=[];
function reject(label,fn){let denied=false;try{fn()}catch(_){denied=true}assert(denied,'false-green negative '+label);hostile.push(label)}
reject('wrong-hold-target',()=>{const r=mutate(d.RELATIONS);r.find(x=>x.to_id.startsWith('C-')).to_id='J-UJ-BROKEN';check(r)});
reject('unanchored-source',()=>{const r=mutate(d.RELATIONS);r.find(x=>x.from_id.startsWith('J-P0-')).from_id='UNRESOLVED';check(r)});
reject('fake-consumer-id',()=>{const v=mutate(d.CONSUMER_EDGES);v[0].consumer_operation_id='first-reader-name';check(d.RELATIONS,d.OPERATION_TRACES,v)});
reject('generic-negative',()=>{const v=mutate(d.CONSUMER_EDGES);v[0].negative_evidence_id='SOURCE_NEGATIVE_CARRIED';check(d.RELATIONS,d.OPERATION_TRACES,v)});
reject('report-as-authority-evidence',()=>{const v=mutate(d.AUTHORITY_APPLICATIONS);v[0].evidence_ids='SOURCE_RETURN_AT_sha';check(d.RELATIONS,d.OPERATION_TRACES,d.CONSUMER_EDGES,v)});
reject('false-applied-rule',()=>{const v=mutate(d.AUTHORITY_APPLICATIONS);v[0].rule_applied_to_output='YES';check(d.RELATIONS,d.OPERATION_TRACES,d.CONSUMER_EDGES,v)});
reject('report-as-code-sha',()=>{const v=mutate(d.IMPLEMENTATIONS);v[0].code_sha='PRONG_REPORT_AT_sha';check(d.RELATIONS,d.OPERATION_TRACES,d.CONSUMER_EDGES,d.AUTHORITY_APPLICATIONS,v)});
reject('conditional-promoted-to-must',()=>{const v=mutate(seam);v.find(x=>x.original_requiredness==='IF').original_requiredness='MUST';check(d.RELATIONS,d.OPERATION_TRACES,d.CONSUMER_EDGES,d.AUTHORITY_APPLICATIONS,d.IMPLEMENTATIONS,v)});
reject('conditional-erased',()=>{const v=mutate(seam);v.find(x=>x.original_requiredness==='IF').literal_predicate='always';check(d.RELATIONS,d.OPERATION_TRACES,d.CONSUMER_EDGES,d.AUTHORITY_APPLICATIONS,d.IMPLEMENTATIONS,v)});
reject('p0-left-deletion',()=>{const v=mutate(left).slice(1);check(d.RELATIONS,d.OPERATION_TRACES,d.CONSUMER_EDGES,d.AUTHORITY_APPLICATIONS,d.IMPLEMENTATIONS,seam,v)});
reject('p0-function-inflation',()=>{const v=mutate(left);v[0].new_function_count_increment='1';check(d.RELATIONS,d.OPERATION_TRACES,d.CONSUMER_EDGES,d.AUTHORITY_APPLICATIONS,d.IMPLEMENTATIONS,seam,v)});
assert.strictEqual(anti.length,2607);assert.strictEqual(conflict.length,1536);
console.log(JSON.stringify({verdict:'S0_S1_R3_GRAPH_INTEGRITY_PASS__NOT_SEMANTIC_OR_NATIVE_ACCEPTANCE',baseline_p0:p0.length,p0_left_unmatched:4256,rel:d.RELATIONS.length,stage:stage.length,seams:seam.length,consumer:d.CONSUMER_EDGES.length,authority:d.AUTHORITY_APPLICATIONS.length,remaining_actual_consumer_positive:0,remaining_rule_application_positive:0,negative_controls:hostile.length,controls:hostile},null,2));
