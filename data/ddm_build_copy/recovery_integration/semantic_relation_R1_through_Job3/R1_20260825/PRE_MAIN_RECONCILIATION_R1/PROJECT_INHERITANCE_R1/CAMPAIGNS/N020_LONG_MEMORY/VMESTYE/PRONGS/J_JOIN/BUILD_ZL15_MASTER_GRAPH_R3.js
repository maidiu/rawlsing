/*
 * VMESTYE ZL-15 R3: deterministic S0-S1 documentary repair of R2 master atlas.
 * The 13 P1 input bundles and original R2 return remain frozen. This is a
 * reproducible materialization of review corrections, not source/native execution.
 *
 * In the repository this file lives in VMESTYE/PRONGS/J_JOIN/. Run from any cwd:
 *   node PRONGS/J_JOIN/BUILD_ZL15_MASTER_GRAPH_R3.js
 * Scratch source review: --root zl15 --p0 zl15/P0_ORIGINAL.tsv
 *   --seams zl15/CURRENT_SEAM_STATES.jsonl --sorok zl15/SOROK_VERSIONED_SEAMS.jsonl
 * Run ONLY against the immutable PR #864 R2 HEAD 6be7a625... baseline.
 * On an R3 checkout use VALIDATE_ZL15_R3.js; do not apply repairs twice.
 */
'use strict';
const fs=require('fs'), path=require('path'), crypto=require('crypto'), assert=require('assert');
const args=process.argv.slice(2);
const arg=(k,d)=>args.includes(k)?args[args.indexOf(k)+1]:d;
const root=path.resolve(arg('--root',path.resolve(__dirname,'../..')));
function findRepo(start){let p=start;while(true){if(fs.existsSync(path.join(p,'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl')))return p;const n=path.dirname(p);if(n===p)throw Error('Repository root unavailable; supply --seams and --sorok');p=n;}}
const needsSource=!(args.includes('--p0')&&args.includes('--seams')&&args.includes('--sorok'));
const repo=needsSource?findRepo(root):root;
const p0File=path.resolve(arg('--p0',path.join(root,'CONTROL/P0_RETURN_AND_BRANCH_CENSUS.tsv')));
const seamFile=path.resolve(arg('--seams',path.join(repo,'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl')));
// The E001 review witness was at an earlier immutable source cut than the
// branch's current Sorok file. Use the *byte-exact frozen witness*, never a
// later same-path worktree file as if its blob SHA were unchanged.
const sorokFile=path.resolve(arg('--sorok',path.join(root,'PRONGS/J_JOIN/FROZEN_INPUTS/SOROK_VERSIONED_SEAMS_37915.jsonl')));
if(args.includes('--validate-only'))throw Error('Use VALIDATE_ZL15_R3.js on the materialized R3 branch. This builder requires exact R2 baseline.');
const expectedBlobs={p0:'65c1bbe4a602341c5caacca2d58dced31a23f382',seams:'5a951626c0dde91b682eb23216c88dbfc054808d',sorok:'d31eef4f4bc3f4fc6a32ba3e6563c788713f6c47'};
function gitBlob(buf){return crypto.createHash('sha1').update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex')}
function sourced(file,sha){const bytes=fs.readFileSync(file);assert.strictEqual(gitBlob(bytes),sha,'immutable source blob mismatch: '+file);return bytes.toString('utf8')}
function norm(v){return String(v??'').replace(/[\t\r\n]+/g,' ').trim()}
function parse(s,name){const lines=s.trimEnd().split(/\r?\n/);const h=lines.shift().split('\t');assert(h.length>1,name+' bad header');const rows=lines.filter(Boolean).map((line,i)=>{const cols=line.split('\t');assert.strictEqual(cols.length,h.length,name+' row '+(i+2)+' wrong width');return Object.fromEntries(h.map((k,j)=>[k,cols[j]]))});return {h,rows}}
function read(rel){return parse(fs.readFileSync(path.join(root,rel),'utf8'),rel)}
function format(t){return t.h.join('\t')+'\n'+t.rows.map(r=>t.h.map(k=>norm(r[k])).join('\t')).join('\n')+(t.rows.length?'\n':'')}
function table(header,rows=[]){return {h:header.split('\t'),rows}}
function rowPut(t,r){for(const k of t.h)if(r[k]===undefined)r[k]='';t.rows.push(r);return r}
function addCol(t,k,value=''){if(!t.h.includes(k)){t.h.push(k);for(const r of t.rows)r[k]=value}}
function unique(t,name){let ids=new Set();for(const r of t.rows){let k=r[t.h[0]];assert(k,name+' empty PK');assert(!ids.has(k),name+' duplicate '+k);ids.add(k)}return ids}
const DATA=['FUNCTION_ATLAS','RELATIONS','OPERATION_TRACES','AUTHORITY_APPLICATIONS','EVIDENCE','IMPLEMENTATIONS','CONSUMER_EDGES','DECISION_EVENTS'];
const D=Object.fromEntries(DATA.map(n=>[n,read('DATA/'+n+'.tsv')]));
const side={anti:read('PRONGS/J_JOIN/FULL_ID_ANTI_JOINS.tsv'),conflict:read('PRONGS/J_JOIN/CONFLICTS_AND_REPAIR_ORDER.tsv')};
const p0=parse(sourced(p0File,expectedBlobs.p0),'original P0');
const seams=sourced(seamFile,expectedBlobs.seams).trimEnd().split('\n').map(JSON.parse);
const sorok=sourced(sorokFile,expectedBlobs.sorok).trimEnd().split('\n').map(JSON.parse);
const bundle={};for(let i=2;i<=14;i++){const pid='ZL'+String(i).padStart(2,'0');bundle[pid]=JSON.parse(fs.readFileSync(path.join(root,'PRONGS/J_JOIN/FROZEN_INPUTS/'+pid+'.json'),'utf8'))}
const baseline={FUNCTION_ATLAS:1740,RELATIONS:3662,OPERATION_TRACES:332,AUTHORITY_APPLICATIONS:370,EVIDENCE:2718,IMPLEMENTATIONS:884,CONSUMER_EDGES:332,DECISION_EVENTS:884};
for(const n of DATA){unique(D[n],n);assert.strictEqual(D[n].rows.length,baseline[n],n+' requires exact R2 pre-repair row count')}
const fiveFields=['estate_id','source_commit_sha','source_path','source_composite_id','record_grain'];
const tuple=r=>JSON.stringify([r.estate_id,r.source_commit_sha,r.source_path,r.source_composite_id,r.record_grain??r.source_grain]);
const p0ByTuple=new Map(),p0ById=new Map();
for(const r of p0.rows){assert(!p0ByTuple.has(tuple(r)),'P0 duplicate tuple');assert(!p0ById.has(r.census_id),'P0 duplicate ID');p0ByTuple.set(tuple(r),r);p0ById.set(r.census_id,r)}
assert.strictEqual(p0.rows.length,6125);
const matched=new Map(),audit=[];
for(const c of side.anti.rows){const p=p0ByTuple.get(tuple(c));if(p){assert.strictEqual(p.census_id,c.census_id,'P0 census-ID mismatch');const a=matched.get(p.census_id)||[];a.push(c.anti_join_id);matched.set(p.census_id,a)}audit.push([c.anti_join_id,p?.census_id||'OUTSIDE_P0'])}
assert.strictEqual(side.anti.rows.length,2607);assert.strictEqual(matched.size,1869);
assert.strictEqual(audit.filter(x=>x[1]!=='OUTSIDE_P0').length,1962);
const C=Object.fromEntries(side.conflict.rows.map(r=>[r.conflict_id,r]));
assert.strictEqual(Object.keys(C).length,1536);
const E=Object.fromEntries(D.EVIDENCE.rows.map(r=>[r.evidence_id,r]));
const OP=Object.fromEntries(D.OPERATION_TRACES.rows.map(r=>[r.operation_id,r]));
const EDGE=Object.fromEntries(D.CONSUMER_EDGES.rows.map(r=>[r.edge_id,r]));
const F=Object.fromEntries(D.FUNCTION_ATLAS.rows.map(r=>[r.record_id,r]));
const getB=(p,n)=>parse(bundle[p].tables[n],p+'/'+n).rows;
const origE={},origOp={},origAu={};
for(const pid of Object.keys(bundle)){
  origE[pid]=getB(pid,'EVIDENCE');
  origOp[pid]=Object.fromEntries(getB(pid,'OPERATION_TRACES').map(r=>[r.trace_id,r]));
  origAu[pid]=Object.fromEntries(getB(pid,'AUTHORITY_USE').map(r=>[r.authority_use_id,r]));
}
const srcEvidence=(pid,id)=>id&&id!=='UNRESOLVED'&&E['J-EV-'+pid+'-'+id]?'J-EV-'+pid+'-'+id:null;
const findEvidence=(pid,fid,requiresNegative)=>{
  const candidates=origE[pid].filter(x=>x.finding_id===fid&&E['J-EV-'+pid+'-'+x.evidence_id]);
  if(requiresNegative){const meaningful=x=>!/^(UNKNOWN|UNRESOLVED|NOT_ASSESSED|NONE|NOT_RUN|)$/i.test((x.negative_or_refusal||'').trim());return candidates.find(meaningful)||null}
  return candidates[0]||null;
};
const p0H='source_node_id\tcensus_id\testate_id\tsource_commit_sha\tsource_path\tsource_blob_sha\tsource_row_locator\tsource_exact_id\tsource_composite_id\trecord_grain\tp0_left_disposition\tprong_observations\tsource_join_state\tsource_missing_link_type\toriginal_source_grade\toriginal_negative_status\tcandidate_current_owner\tnext_owner\tsame_grain_function_proved\tnew_function_count_increment\toriginal_evidence_id';
const p0Left=table(p0H);
const classify=r=>{
 const e=r.estate_id;
 if(e==='PYAT_SR01_2416'||e==='SOROK_SR01_1314')return 'CLASSIFICATION_ONLY_SR01_OVERLAY__NO_FUNCTION_CLAIM';
 if(e==='SOROK_SOURCE_INDEX_ONLY48')return 'EXTERNAL_INDEX_ONLY__SOURCE_BODY_NOT_PROVED';
 if(e.includes('UNRESOLVED')||e==='PROG_GAP49')return 'EXPLICIT_GAP_OR_UNRESOLVED_SAME_GRAIN';
 if(/^(VMESTYE_|SECTIONS11|RECENT_CAMPAIGN30)/.test(e))return 'ADMINISTRATIVE_GATE_OR_SECTION__OUTSIDE_FUNCTION_DENOMINATOR';
 if(e==='SOROK_ASSETS304'||e==='SOROK_W1_INPUT100'||e==='SOROK_PHASE_GATES83')return 'EXTERNAL_SOURCE_INDEX_OR_GATE__NOT_EXECUTABLE_FUNCTION';
 return 'SOURCE_IDENTITY_SAME_GRAIN_SEMANTIC_JOIN_OPEN';
};
for(const r of p0.rows){const refs=matched.get(r.census_id)||[];rowPut(p0Left,{
 source_node_id:'J-P0-'+r.census_id,census_id:r.census_id,estate_id:r.estate_id,
 source_commit_sha:r.source_commit_sha,source_path:r.source_path,source_blob_sha:r.source_blob_sha,
 source_row_locator:r.source_row_locator,source_exact_id:r.source_exact_id,source_composite_id:r.source_composite_id,
 record_grain:r.record_grain,p0_left_disposition:refs.length?'EXACT_PRONG_OBSERVATION__SEMANTIC_STATUS_UNCHANGED':classify(r),
 prong_observations:refs.join(';')||'NONE_EXACT',source_join_state:r.join_state,source_missing_link_type:r.missing_link_type,
 original_source_grade:r.source_grade,original_negative_status:r.negative_status,
 candidate_current_owner:r.candidate_current_owner,next_owner:r.next_owner,
 same_grain_function_proved:'NO_NEW_PROOF',new_function_count_increment:'0',original_evidence_id:r.evidence_id
})}
assert.strictEqual(p0Left.rows.filter(x=>x.prong_observations==='NONE_EXACT').length,4256);
// R16-D01: map every held conflict to its actual PK, and exact ZL08 P0 source node.
let repairedHolds=0,repairedOrigins=0;
for(const r of D.RELATIONS.rows){if(r.relation_type!=='HELD_BY'||!r.to_id.startsWith('J-UJ-'))continue;
 const target='C-'+r.to_id.slice('J-UJ-'.length);assert(C[target],'dangling held court '+target);
 r.to_id=target;repairedHolds++;
 if(r.from_id==='UNRESOLVED'){
   const c=C[target],p=p0ById.get(c.census_id);assert(p,'missing source identity for '+target);
   assert.strictEqual(tuple(p),tuple(c),'generic source endpoint tuple mismatch');
   r.from_id='J-P0-'+c.census_id;r.applicability_or_condition='EXACT_P0_SOURCE_TUPLE__FUNCTION_JOIN_OPEN';repairedOrigins++;
 }
}
assert.strictEqual(repairedHolds,1536);assert.strictEqual(repairedOrigins,241);
// R17-D02/D03: preserve report labels separately from exact normalized _id FKs.
for(const col of ['reported_consumer_label','consumer_id_resolution','negative_evidence_grade','negative_evidence_scope'])addCol(D.CONSUMER_EDGES,col);
for(const col of ['prong_trace_locator','reported_producer_edge_label','underlying_code_sha','underlying_code_path_symbol','code_provenance_grade','prong_return_sha'])addCol(D.OPERATION_TRACES,col);
let negDirect=0,negFinding=0,negUnresolved=0;
for(const c of D.CONSUMER_EDGES.rows){const op=OP[c.producer_operation_id];assert(op,'missing producer op '+c.edge_id);
 const pid=op.generation,local=op.operation_id.slice(('J-OP-'+pid+'-').length),src=origOp[pid][local];assert(src,'missing frozen source op '+op.operation_id);
 const oldLabel=c.consumer_operation_id;
 c.reported_consumer_label=oldLabel;c.consumer_operation_id='UNRESOLVED';c.consumer_id_resolution='NOT_PROVED_AS_NORMALIZED_ACTUAL_FIRST_CONSUMER';
 let ev=null,grade='UNRESOLVED_NEGATIVE__REQUIRES_SOURCE_RECEIPT';
 const direct=srcEvidence(pid,src.first_consumer_evidence_id);
 if(direct){const d=origE[pid].find(e=>e.evidence_id===src.first_consumer_evidence_id);if(d&&d.negative_or_refusal){ev=direct;grade='DIRECT_SOURCE_EVIDENCE_ID__NOT_CURRENT_ENFORCEMENT';negDirect++}}
 if(!ev){const x=findEvidence(pid,src.finding_id,true);if(x){ev=srcEvidence(pid,x.evidence_id);grade='SAME_FINDING_SOURCE_NEGATIVE__NOT_CURRENT_ENFORCEMENT';negFinding++}}
 if(!ev)negUnresolved++;
 c.negative_evidence_id=ev||'UNRESOLVED_NEGATIVE';c.negative_evidence_grade=grade;c.negative_evidence_scope=src.negative_or_refusal||'UNRESOLVED';
 op.prong_trace_locator=op.code_symbol_at_sha;op.reported_producer_edge_label=op.producer_edge_id;
 op.producer_edge_id=c.edge_id;op.prong_return_sha=bundle[pid].source_head;
 op.underlying_code_sha='NOT_PROVED_CODE';op.underlying_code_path_symbol='NOT_PROVED_SYMBOL';
 op.code_provenance_grade='PRONG_REPORT_TRACE_ONLY__NO_INDEPENDENT_CODE_SHA';op.code_symbol_at_sha='NOT_PROVED_CODE_SYMBOL__SEE_PRONG_TRACE_LOCATOR';
 rowPut(D.RELATIONS,{
   relation_id:'JR-R3-'+pid+'-'+local+'-PRODUCER',from_id:op.operation_id,relation_type:'CANDIDATE_PRODUCER_EDGE__NOT_EXECUTION',to_id:c.edge_id,
   generation_from:pid,generation_to:'VMESTYE_CANDIDATE',applicability_or_condition:'NO_NON_TEST_FIRST_READER_PROVED',
   operation_or_authority_id:op.operation_id,evidence_id:c.positive_evidence_id,
   at_cut:bundle[pid].source_head,grade:'S1_PRONG_REPORT_OPERATION_LINK_ONLY',
   comment:'ID-addressable report producer; consumer endpoint deliberately UNRESOLVED, not a real call'
 });
}
assert.strictEqual(negDirect+negFinding+negUnresolved,332);
// R16-D04: report SHA and source locator cannot be stored as executable code SHA.
for(const col of ['prong_return_sha','reported_code_locator','underlying_code_sha','underlying_code_path_symbol','underlying_code_blob_sha','code_sha_grade'])addCol(D.IMPLEMENTATIONS,col);
for(const im of D.IMPLEMENTATIONS.rows){const pid=im.implementation_id.split('-')[2];assert(bundle[pid],'bad implementation prong '+im.implementation_id);
 im.prong_return_sha=bundle[pid].source_head;im.reported_code_locator=im.code_symbol;
 im.underlying_code_sha='NOT_PROVED_CODE';im.underlying_code_path_symbol='NOT_PROVED_SYMBOL';im.underlying_code_blob_sha='UNVERIFIED';
 im.code_sha='NOT_PROVED_CODE';im.code_sha_grade='SOURCE_CLAIM_NOT_CODE_READBACK';
}
// Explicit independently read code provenance is intentionally tiny and enumerated.
const knownCode=[
 ['J-IM-ZL12-F-N10E','256d46bf425cc37e114465cddbe3c60e535766ab','rawlsing_next/pre553_empirical_possibility_provider.py#provide_empirical_possibility_slice','23167aa25291fb148b1e3cf210ac33fe7769b783'],
];
for(const [id,sha,symbol,blob] of knownCode){const r=D.IMPLEMENTATIONS.rows.find(x=>x.implementation_id===id);assert(r,'known code ID missing '+id);r.code_sha=sha;r.underlying_code_sha=sha;r.underlying_code_path_symbol=symbol;r.underlying_code_blob_sha=blob;r.code_sha_grade='INDEPENDENT_S1_BLOB_READ__NO_RUNTIME_OR_CURRENT_SELECTION'}
for(const op of D.OPERATION_TRACES.rows){if(op.operation_id==='J-OP-ZL12-T-I03N10E'){
 op.underlying_code_sha='256d46bf425cc37e114465cddbe3c60e535766ab';
 op.underlying_code_path_symbol='rawlsing_next/pre553_empirical_possibility_provider.py#provide_empirical_possibility_slice';
 op.code_symbol_at_sha=op.underlying_code_sha+'::'+op.underlying_code_path_symbol;
 op.code_provenance_grade='INDEPENDENT_S1_BLOB_READ__NO_ACTUAL_FIRST_READER';
}}
// R17-D04: replace 370 report-head values with explicit exact evidence refs or typed misses.
for(const col of ['prong_return_sha','authority_evidence_join_grade','reported_first_consumer_evidence_label'])addCol(D.AUTHORITY_APPLICATIONS,col);
let authDirect=0,authFinding=0,authMissing=0;
for(const a of D.AUTHORITY_APPLICATIONS.rows){const pid=a.application_id.split('-')[2],local=a.application_id.slice(('J-AU-'+pid+'-').length),src=origAu[pid][local];assert(src,'frozen authority ID missing '+a.application_id);
 a.prong_return_sha=bundle[pid].source_head;a.reported_first_consumer_evidence_label=src.first_consumer_evidence_id;
 const direct=srcEvidence(pid,src.first_consumer_evidence_id),same=findEvidence(pid,src.finding_id,false);
 if(direct){a.evidence_ids=direct;a.authority_evidence_join_grade='DIRECT_PRONG_EVIDENCE_REF__NOT_APPLIED';authDirect++}
 else if(same){a.evidence_ids=srcEvidence(pid,same.evidence_id);a.authority_evidence_join_grade='SAME_FINDING_SOURCE_RECORD__RULE_SELECTION_UNPROVED';authFinding++}
 else{a.evidence_ids='UNRESOLVED_EVIDENCE';a.authority_evidence_join_grade='NO_MATCHING_SOURCE_EVIDENCE__HELD';authMissing++}
}
assert.strictEqual(authDirect+authFinding+authMissing,370);
// R17-D01: 82 distinct source seam edges, literal predicates, and evidence IDs.
const seamNodes=table('node_id\tliteral_endpoint\tseam_class\tclaim_grade\tactual_runtime_status');
const seamMap=new Map(),seamRows=table('seam_edge_id\trelation_id\tfrom_node_id\tto_node_id\tfrom_literal\tto_literal\toriginal_requiredness\tliteral_predicate\tapplicability\tproof_ceiling\tnegative_preserved\tsource_sha\tsource_blob_sha\tsource_path\tsource_jsonl_line\tcanonical_evidence_id\tactual_execution\tsource_class');
const node=(literal,kind='PYAT_DECLARED')=>{if(!seamMap.has(literal)){
 const id='J-SEAM-NODE-'+crypto.createHash('sha256').update(literal).digest('hex').slice(0,18);
 seamMap.set(literal,id);rowPut(seamNodes,{node_id:id,literal_endpoint:literal,seam_class:kind,claim_grade:'S1_DECLARED_OR_REPORTED_ENDPOINT',actual_runtime_status:'NOT_PROVED_BY_EDGE_IDENTITY'});
 }return seamMap.get(literal)};
const eSeam=Object.values(E).filter(x=>x.path==='PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl');
assert.strictEqual(seams.length,82);assert.strictEqual(eSeam.length,82);
const countKinds={};
for(let i=0;i<seams.length;i++){
 const s=seams[i],v=s.original_G2,litFrom=v.from,litTo=v.to,kind=s.original_requiredness;
 assert(v&&v.edge_id===s.edge_id);assert(litFrom&&litTo,'seam endpoint missing');
 const candidates=eSeam.filter(e=>e.line_range_or_row_id.startsWith('jsonl:'+(i+1)+';')&&e.line_range_or_row_id.includes('COMPOSITE='+JSON.stringify([s.edge_id])+';'));
 assert.strictEqual(candidates.length,1,'seam evidence mismatch '+s.edge_id);
 const evidence=candidates[0].evidence_id,relation='JR-R3-SEAM-'+String(i+1).padStart(3,'0');
 const from=node(litFrom,s.edge_class),to=node(litTo,s.edge_class);
 const pred=s.original_predicate||v.edge_condition||'PREDICATE_NOT_SUPPLIED';
 countKinds[kind]=(countKinds[kind]||0)+1;
 rowPut(seamRows,{seam_edge_id:s.edge_id,relation_id:relation,from_node_id:from,to_node_id:to,from_literal:litFrom,to_literal:litTo,
   original_requiredness:kind,literal_predicate:pred,applicability:s.applicability,proof_ceiling:s.g4_proof_ceiling||s.current?.proof_grade||'SOURCE_ONLY',
   negative_preserved:s.retained_negative||v.negative||'NOT_ASSESSED',source_sha:'7a5429ffbc48efd25e28c912da80c822e66bc182',
   source_blob_sha:expectedBlobs.seams,source_path:'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl',
   source_jsonl_line:String(i+1),canonical_evidence_id:evidence,actual_execution:'NOT_RUN_BY_ZL15__SOURCE_STATUS='+String(s.current?.status||'UNKNOWN'),source_class:s.edge_class
 });
 rowPut(D.RELATIONS,{relation_id:relation,from_id:from,relation_type:'DOCUMENTED_DEPENDENCY__'+s.edge_class,to_id:to,
   generation_from:s.edge_class,generation_to:'PYAT_DECLARED_OR_REPORTED',applicability_or_condition:kind+' :: '+pred,
   operation_or_authority_id:s.edge_id,evidence_id:evidence,at_cut:'7a5429ffbc48efd25e28c912da80c822e66bc182',
   grade:'SOURCE_S1__'+kind+'__NO_CURRENT_NATIVE_INFERENCE',comment:'Preserves source conditional applicability='+s.applicability+'; negative='+s.retained_negative
 });
}
assert.deepStrictEqual(countKinds,{MUST:7,IF:26,FUNCTIONAL_OR_CONSUMES__NOT_NODE_DAG:12,FUNCTIONAL_IF__NOT_ASTRA_NODE_DAG:2,OBSERVED_OR_REPORTED_PRODUCER_RECEIVER__DOES_NOT_ADD_ASTRA_REQUIRED_EDGE:35});
// R16-D02: explicit per-finding/side-of-generation open disposition; no label equivalence.
const stages=['DVA','TRII','CHETIRI','LONG_MEMORY','PYAT_CURRENT'];
const stagesT=table('stage_court_id\tfinding_id\torigin_prong\tstage\tstage_source_generation\tpossible_owner_label\tqualified_target_id\tstage_fate\tjoin_disposition\tcorroborating_evidence_id\tnegative_preserved\tsource_ref\tnext_falsifier');
for(const f of D.FUNCTION_ATLAS.rows.filter(r=>/^ZL\d\d_DOCUMENTARY_FINDING$/.test(r.namespace))){const pid=f.namespace.slice(0,4),id=f.record_id,evidence=Object.values(E).find(x=>x.evidence_id.startsWith('J-EV-'+pid+'-')&&f.source.endsWith('#'+(x.evidence_id.replace('J-EV-'+pid+'-','').replace(/^.*?E-/,'F-'))));
 const src=getB(pid,'FINDINGS').find(r=>'J-F-'+pid+'-'+r.finding_id===id);assert(src,'finding source missing '+id);
 const sameEvidence=findEvidence(pid,src.finding_id,false),eid=sameEvidence?srcEvidence(pid,sameEvidence.evidence_id):'UNRESOLVED_EVIDENCE';
 for(const stage of stages){let fate=stage==='DVA'?f.dva_fate:stage==='TRII'?f.trii_fate:stage==='CHETIRI'?f.chetiri_fate:stage==='LONG_MEMORY'?f.long_memory_id:f.pyat_owner_ids;
  const same=(stage==='DVA'&&pid==='ZL05')||(stage==='TRII'&&pid==='ZL06')||(stage==='CHETIRI'&&pid==='ZL07');
  const stageRow=rowPut(stagesT,{stage_court_id:'J-STAGE-'+pid+'-'+src.finding_id+'-'+stage,finding_id:id,origin_prong:pid,stage,
    stage_source_generation:src.source_generation||pid,possible_owner_label:fate||'UNRESOLVED',qualified_target_id:same?id:'UNRESOLVED',
    stage_fate:fate||'UNRECONCILED',join_disposition:same?'SELF_STAGE_SOURCE_RETURN__NOT_CROSS_STAGE_PROOF':'EXACT_SOURCE_FINDING_TO_STAGE__SEMANTIC_SUCCESSION_UNJOINED',
    corroborating_evidence_id:eid,negative_preserved:src.negative_case||'UNKNOWN',source_ref:f.source,next_falsifier:src.unresolved_and_falsifier||'SAME_GRAIN_OPERATION_AUTHORITY_AND_FIRST_READER_REQUIRED'});
  rowPut(D.RELATIONS,{relation_id:'JR-R3-STAGE-'+pid+'-'+src.finding_id+'-'+stage,
    from_id:id,relation_type:same?'SELF_STAGE_SOURCE_RETURN__NOT_SUCCESSION':'CROSS_GENERATION_TYPED_UNJOIN',
    to_id:stageRow.stage_court_id,generation_from:pid,generation_to:stage,
    applicability_or_condition:'STAGE_FATE='+stageRow.stage_fate+';NEGATIVE='+stageRow.negative_preserved,
    operation_or_authority_id:stageRow.stage_court_id,evidence_id:eid,
    at_cut:bundle[pid].source_head,grade:'S1_STAGE_NAVIGATION__NO_SEMANTIC_EQUIVALENCE',
    comment:'Exact original finding to stage question; qualified target '+stageRow.qualified_target_id+'; '+stageRow.next_falsifier});
 }
}
assert.strictEqual(stagesT.rows.length,884*5);
const bridges=table('bridge_id\tfrom_finding_id\tto_finding_id\tbridge_kind\told_source_semantic_scope\tcurrent_candidate_scope\tnegative_falsifier\tfrom_evidence_id\tto_evidence_id\tintermediate_stage_status\tcurrent_first_reader_status\tproof_grade');
for(const [legacy,negative,evidence] of [
 ['F03_QREL','Five QUC guards permit row-none preservation on missing/ambiguous/excluded W6; one false clears; explicit BLOCKED row differs','J-EV-ZL02-ZL02-E-SRC-F03_QREL-rel_apply'],
 ['F08_Q_USE','allowed_as_v551_relation_evidence=false may forbid apparently matched question-use; no collapse to F03 six-coordinate rule','J-EV-ZL02-ZL02-E-C6-F08_Q_USE']
]){
 const from='J-F-ZL02-ZL02-F-'+legacy,to='J-F-ZL09-ZL09-F-F03F08',toE='J-EV-ZL09-ZL09-E-F03F08';
 assert(F[from]&&F[to]&&E[evidence]);
 const e2=E[toE]?toE:'UNRESOLVED_EVIDENCE';
 rowPut(bridges,{bridge_id:'J-BRIDGE-'+legacy+'-TO-F03F08',from_finding_id:from,to_finding_id:to,
   bridge_kind:'EXPLICIT_CROSS_PRONG_CANDIDATE__NOT_SEMANTIC_EQUIVALENCE',old_source_semantic_scope:legacy,
   current_candidate_scope:'ZL09-F03F08 C11 generic capability; source selection and use unproved',negative_falsifier:negative,
   from_evidence_id:evidence,to_evidence_id:e2,intermediate_stage_status:'DVA_TRII_CHETIRI_LONG_MEMORY__EACH_UNJOINED_UNTIL_PROVEN',
   current_first_reader_status:'NOT_PROVED_NON_TEST',proof_grade:'SOURCE_S1_CANDIDATE_LINK_ONLY'});
 rowPut(D.RELATIONS,{relation_id:'JR-R3-BRIDGE-'+legacy,from_id:from,relation_type:'CROSS_PRONG_CANDIDATE_UNJOIN__NOT_SUCCESSION',to_id:to,
   generation_from:'C6_HISTORICAL_ZL02',generation_to:'PYAT_C11_ZL09',applicability_or_condition:negative,
   operation_or_authority_id:'F03F08_CANDIDATE_UNPROVED',evidence_id:evidence,at_cut:bundle.ZL09.source_head,
   grade:'S1_SOURCE_SEMANTIC_DIFFERENCE__NO_EQUIVALENCE_OR_NATIVE',comment:'Dva/Trii/Chetiri/LM intermediate fates held; wrong-use negative must be replayed'});
}
// R17-D02: a source-bound Sorok E001 receiving dependency (not a native import).
const e001=sorok.find(x=>x.record_type==='VERSIONED_SEAM'&&x.seam_id==='E001');assert(e001,'Sorok E001 source row unavailable');
assert(/NONE_PROVEN/.test(e001.actual_consumer_or_none.callable_or_none),'Sorok E001 native hold changed');
const e001Ev='J-EV-R3-SOROK-E001';
if(!E[e001Ev]){rowPut(D.EVIDENCE,{evidence_id:e001Ev,source_sha:'37915a47ed3e33a71ad8334c0aa505f5d65796ca',
 path:'SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/15_W7_VERSIONED_SEAMS_AND_GATE_JOIN_CANDIDATES_R1.jsonl',
 line_range_or_row_id:'VERSIONED_SEAM:E001;BLOB='+expectedBlobs.sorok,claim_supported:'E001 requires N11/N12 qualified world release and Sorok C11 recipient owner/readset; native first reader NONE_PROVEN',
 evidence_type:'EXACT_SOURCE_JSON_ROW',observed_at_cut:'37915a47ed3e33a71ad8334c0aa505f5d65796ca',
 original_native_or_sourcefree:'NO_NATIVE_SOROK_IMPORT',independent_review_ref:'ZL17_R1_SOURCE_COLD_READ__AUTHOR_RECHECK_S1',
 ceiling_and_negative:e001.join_status+'; '+e001.actual_consumer_or_none.callable_or_none});E[e001Ev]=D.EVIDENCE.rows.at(-1)}
const e001Node=node('SOROK:E001','SOROK_OWNER_HELD');
const transfers=table('transfer_id\tproducer_node_id\treceiver_node_id\ttransfer_type\tinput_output_contract\tpredicate_and_negative\texact_evidence_id\tcode_or_source_sha\tsource_path_symbol\tverification_grade\tactual_first_reader_status');
for(const n of ['N11','N12']){
 const from=node('PYAT:ASTRA:'+n);const transferId='J-R3-E001-REQUIRES-'+n;
 rowPut(transfers,{transfer_id:transferId,producer_node_id:from,receiver_node_id:e001Node,transfer_type:'OWNER_CONTRACT_CANDIDATE__NOT_NATIVE',
 input_output_contract:e001.producer.callable_or_required,predicate_and_negative:e001.join_status+'; Pyat owner release and Sorok C11 actor readset/consent required',
 exact_evidence_id:e001Ev,code_or_source_sha:'37915a47ed3e33a71ad8334c0aa505f5d65796ca',source_path_symbol:'SOROK_VERSIONED_SEAM:E001',
 verification_grade:'S1_DECLARED_GATE_ONLY',actual_first_reader_status:'NONE_PROVEN_SOROK_C11_NATIVE'});
 rowPut(D.RELATIONS,{relation_id:'JR-R3-E001-'+n,from_id:from,relation_type:'CANDIDATE_REQUIRED_FOR_SOROK_E001__OWNER_HELD',to_id:e001Node,
 generation_from:'PYAT',generation_to:'SOROK_PRE_V3',applicability_or_condition:'E001 owner grant/readset/consent/retention not satisfied',
 operation_or_authority_id:transferId,evidence_id:e001Ev,at_cut:'37915a47ed3e33a71ad8334c0aa505f5d65796ca',
 grade:'SOURCE_S1_OWNER_HELD__NO_NATIVE_IMPORT',comment:'Different empirical Pyat C11 facade and Sorok actor C11; no same-namespace substitution'});
}
const codeEv='J-EV-R3-N10E-PROVIDER-STATIC';
rowPut(D.EVIDENCE,{evidence_id:codeEv,source_sha:'256d46bf425cc37e114465cddbe3c60e535766ab',
 path:'rawlsing_next/pre553_empirical_possibility_provider.py',line_range_or_row_id:'lines:531-585;BLOB=23167aa25291fb148b1e3cf210ac33fe7769b783',
 claim_supported:'provide_empirical_possibility_slice calls compose_positioned_subject_possibility at source line 574; static call, not native/selected execution',
 evidence_type:'INDEPENDENT_S1_CODE_BODY',observed_at_cut:'256d46bf425cc37e114465cddbe3c60e535766ab',original_native_or_sourcefree:'NOT_RUN_BY_ZL15',
 independent_review_ref:'ZL17_R1_AND_ZL15_AUTHOR_S1_STATIC_READ',ceiling_and_negative:'No selected original35 native invocation, actor grant or first-reader receipt'});
E[codeEv]=D.EVIDENCE.rows.at(-1);
const provider=node('RAWLSING:provide_empirical_possibility_slice','VERIFIED_STATIC_CODE'),composition=node('RAWLSING:compose_positioned_subject_possibility','VERIFIED_STATIC_CODE');
const n10e=node('PYAT:ASTRA:N10E');
for(const [id,from,to,kind,grade] of [
 ['J-R3-CODE-N10E-IMPLEMENTATION',n10e,provider,'CANDIDATE_IMPLEMENTATION_LABEL__SOURCE_STATIC','SOURCE_S1_NO_SELECTED_NATIVE'],
 ['J-R3-CODE-PROVIDER-COMPOSITION',provider,composition,'STATIC_CALL_AT_SHA__NO_EXECUTION','INDEPENDENT_S1_VERIFIED_CODE_CALL']
]){
 rowPut(transfers,{transfer_id:id,producer_node_id:from,receiver_node_id:to,transfer_type:kind,
   input_output_contract:'N10E provider/composition scoped empirical possibility contract',predicate_and_negative:'Exact source, rule, universe, witness, selected owner/actual reader unproved',
   exact_evidence_id:codeEv,code_or_source_sha:'256d46bf425cc37e114465cddbe3c60e535766ab',
   source_path_symbol:'rawlsing_next/pre553_empirical_possibility_provider.py#provide_empirical_possibility_slice:574',
   verification_grade:grade,actual_first_reader_status:'NOT_PROVED_NON_TEST'});
 rowPut(D.RELATIONS,{relation_id:'JR-R3-'+id,from_id:from,relation_type:kind,to_id:to,
   generation_from:'PYAT_CODE_S1',generation_to:'PYAT_CODE_CANDIDATE',applicability_or_condition:'STATIC_CODE_ONLY__SELECTED_SOURCE_EFFECT_UNVERIFIED',
   operation_or_authority_id:id,evidence_id:codeEv,at_cut:'256d46bf425cc37e114465cddbe3c60e535766ab',grade,comment:'No current native first consumer or actor rights'});
}
const proofTables={
 'PRONGS/J_JOIN/P0_LEFT_DISPOSITIONS.tsv':p0Left,
 'PRONGS/J_JOIN/GENERATION_STAGE_COURT.tsv':stagesT,
 'PRONGS/J_JOIN/CROSS_PRONG_BRIDGES.tsv':bridges,
 'PRONGS/J_JOIN/SEAM_DEPENDENCY_NODES.tsv':seamNodes,
 'PRONGS/J_JOIN/SEAM_DEPENDENCIES.tsv':seamRows,
 'PRONGS/J_JOIN/CANDIDATE_TRANSFERS.tsv':transfers
};
// Reject precise hostile mutations using only the frozen source as truth.
function validate(){
 const dk=Object.fromEntries(DATA.map(n=>[n,unique(D[n],n)]));
 const source=unique(p0Left,'P0_LEFT');const conflict=unique(side.conflict,'CONFLICTS');const nodes=unique(seamNodes,'SEAM_NODES');
 const consumers=dk.CONSUMER_EDGES,opids=dk.OPERATION_TRACES,ev=dk.EVIDENCE;
 const stageIds=unique(stagesT,'GENERATION_STAGE_COURT');
 const endpoints=new Set([...dk.FUNCTION_ATLAS,...dk.OPERATION_TRACES,...dk.AUTHORITY_APPLICATIONS,...consumers,...conflict,...source,...nodes,...stageIds]);
 const check=(rel,edges,auth,impl,op,dependency,ledger)=>{
 for(const r of rel){if(r.relation_type==='HELD_BY')assert(endpoints.has(r.to_id),'dangling hold '+r.relation_id);
  if(r.relation_type==='HELD_BY')assert(endpoints.has(r.from_id),'unanchored hold '+r.relation_id);
  if(r.relation_id.startsWith('JR-R3-')){assert(endpoints.has(r.from_id)&&endpoints.has(r.to_id),'R3 relation orphan '+r.relation_id);assert(['UNRESOLVED','UNRESOLVED_EVIDENCE'].includes(r.evidence_id)||ev.has(r.evidence_id),'R3 evidence dangling '+r.relation_id)}
 }
 for(const c of edges){assert(opids.has(c.producer_operation_id),'producer missing');assert(c.consumer_operation_id==='UNRESOLVED'||opids.has(c.consumer_operation_id),'consumer ID is not normalized');
  assert(c.negative_evidence_id==='UNRESOLVED_NEGATIVE'||ev.has(c.negative_evidence_id),'generic/invalid negative');
  assert(c.current_actual_status==='OPEN_PROOF_GAP'&&c.actual_call_site_sha==='NOT_PROVED','false actual consumer positive')}
 for(const a of auth){assert(a.evidence_ids==='UNRESOLVED_EVIDENCE'||a.evidence_ids.split(';').every(id=>ev.has(id)),'authority evidence not joined');
  assert(a.rule_applied_to_output!=='YES'&&a.negative_or_refusal_enforced!=='YES','false applied authority positive')}
 for(const im of impl){assert(im.code_sha==='NOT_PROVED_CODE'||/^[0-9a-f]{40}$/.test(im.code_sha),'report pointer in code_sha');
  if(im.code_sha!=='NOT_PROVED_CODE')assert(im.code_sha===im.underlying_code_sha&&/\.py#/.test(im.underlying_code_path_symbol),'unqualified code attribution')}
 for(const o of op){assert(consumers.has(o.producer_edge_id),'producer edge unresolved');assert(o.code_symbol_at_sha.startsWith('NOT_PROVED_CODE_SYMBOL')||/^[a-f0-9]{40}::/.test(o.code_symbol_at_sha),'report pointer in code symbol')}
 assert.strictEqual(ledger.length,6125,'P0 row loss');assert.strictEqual(ledger.filter(x=>x.prong_observations==='NONE_EXACT').length,4256,'P0-left miscount');
 assert.strictEqual(dependency.length,82,'seam edge loss');for(let i=0;i<82;i++){
  const d=dependency[i],s=seams[i];assert.strictEqual(d.seam_edge_id,s.edge_id,'seam identity substituted');
  assert.strictEqual(d.original_requiredness,s.original_requiredness,'MUST/IF/OR promoted or altered');
  assert.strictEqual(d.literal_predicate,s.original_predicate||s.original_G2.edge_condition,'seam predicate altered');
  assert(ev.has(d.canonical_evidence_id),'seam negative provenance missing')}
 };
 check(D.RELATIONS.rows,D.CONSUMER_EDGES.rows,D.AUTHORITY_APPLICATIONS.rows,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,seamRows.rows,p0Left.rows);
 let mutated=0;const refuse=(action)=>{let failed=false;try{action()}catch(e){failed=true}assert(failed,'hostile mutation accepted');mutated++};
 const clone=x=>JSON.parse(JSON.stringify(x));
 refuse(()=>{let t=clone(D.RELATIONS.rows);t.find(x=>x.relation_type==='HELD_BY').to_id='J-UJ-BOGUS';check(t,D.CONSUMER_EDGES.rows,D.AUTHORITY_APPLICATIONS.rows,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,seamRows.rows,p0Left.rows)});
 refuse(()=>{let t=clone(D.RELATIONS.rows);t.find(x=>x.from_id.startsWith('J-P0-')).from_id='UNRESOLVED';check(t,D.CONSUMER_EDGES.rows,D.AUTHORITY_APPLICATIONS.rows,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,seamRows.rows,p0Left.rows)});
 refuse(()=>{let t=clone(D.CONSUMER_EDGES.rows);t[0].consumer_operation_id='free-text-first-reader';check(D.RELATIONS.rows,t,D.AUTHORITY_APPLICATIONS.rows,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,seamRows.rows,p0Left.rows)});
 refuse(()=>{let t=clone(D.CONSUMER_EDGES.rows);t[0].negative_evidence_id='SOURCE_NEGATIVE_CARRIED';check(D.RELATIONS.rows,t,D.AUTHORITY_APPLICATIONS.rows,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,seamRows.rows,p0Left.rows)});
 refuse(()=>{let t=clone(D.AUTHORITY_APPLICATIONS.rows);t[0].evidence_ids='SOURCE_RETURN_AT_unknown';check(D.RELATIONS.rows,D.CONSUMER_EDGES.rows,t,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,seamRows.rows,p0Left.rows)});
 refuse(()=>{let t=clone(D.IMPLEMENTATIONS.rows);t[0].code_sha='PRONG_REPORT_AT_unknown';check(D.RELATIONS.rows,D.CONSUMER_EDGES.rows,D.AUTHORITY_APPLICATIONS.rows,t,D.OPERATION_TRACES.rows,seamRows.rows,p0Left.rows)});
 refuse(()=>{let t=clone(seamRows.rows);t.find(x=>x.original_requiredness==='IF').original_requiredness='MUST';check(D.RELATIONS.rows,D.CONSUMER_EDGES.rows,D.AUTHORITY_APPLICATIONS.rows,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,t,p0Left.rows)});
 refuse(()=>{let t=clone(seamRows.rows);t.find(x=>x.original_requiredness==='IF').literal_predicate='always';check(D.RELATIONS.rows,D.CONSUMER_EDGES.rows,D.AUTHORITY_APPLICATIONS.rows,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,t,p0Left.rows)});
 refuse(()=>{let t=clone(p0Left.rows).slice(1);check(D.RELATIONS.rows,D.CONSUMER_EDGES.rows,D.AUTHORITY_APPLICATIONS.rows,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,seamRows.rows,t)});
 refuse(()=>{let t=clone(D.AUTHORITY_APPLICATIONS.rows);t[0].rule_applied_to_output='YES';check(D.RELATIONS.rows,D.CONSUMER_EDGES.rows,t,D.IMPLEMENTATIONS.rows,D.OPERATION_TRACES.rows,seamRows.rows,p0Left.rows)});
 return {negative_mutations_rejected:mutated};
}
const receipt=validate();
for(const n of DATA)fs.writeFileSync(path.join(root,'DATA/'+n+'.tsv'),format(D[n]));
for(const [name,t] of Object.entries(proofTables))fs.writeFileSync(path.join(root,name),format(t));
console.log(JSON.stringify({status:'R3_GENERATED_AND_VALIDATED',r16:{held_targets_repaired:repairedHolds,source_origins_repaired:repairedOrigins,p0_total:p0.rows.length,p0_left:4256,stages:stagesT.rows.length,explicit_bridges:bridges.rows.length},r17:{seams:seamRows.rows.length,seam_nodes:seamNodes.rows.length,consumer_edges:D.CONSUMER_EDGES.rows.length,negative_direct:negDirect,negative_same_finding:negFinding,negative_unresolved:negUnresolved,authority_direct:authDirect,authority_same_finding:authFinding,authority_unresolved:authMissing,transfers:transfers.rows.length},tables:Object.fromEntries(DATA.map(n=>[n,D[n].rows.length])),...receipt},null,2));
