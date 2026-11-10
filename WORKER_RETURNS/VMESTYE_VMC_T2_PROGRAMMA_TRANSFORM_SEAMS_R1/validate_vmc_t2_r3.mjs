#!/usr/bin/env node
// VMC-T2 R3 documentary structural auditor. Not a native/scientific test.
// Usage: node validate_vmc_t2_r3.mjs [--dir WORKER_RETURNS/...]
//        [--protected-root /path/to/checkout/rawlsing_next]
// The optional protected checkout MUST be PRE-MAIN@256d46bf425c..., not HEAD.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const base = new URL('.', import.meta.url).pathname;
const opts = process.argv.slice(2);
const at = flag => { const i = opts.indexOf(flag); return i >= 0 ? opts[i + 1] : undefined; };
const dir = path.resolve(at('--dir') || base);
const protectedRoot = at('--protected-root');
const errors = [];
let assertions = 0;
function check(condition, why) { assertions++; if (!condition) errors.push(why); }
function parseTSV(name) {
  const body = fs.readFileSync(path.join(dir, name), 'utf8').trimEnd().split(/\r?\n/);
  const header = body.shift().split('\t');
  check(new Set(header).size === header.length, name + ' duplicate columns');
  const rows = body.filter(Boolean).map((line, n) => {
    const cells = line.split('\t');
    check(cells.length === header.length, name + ':' + (n + 2) + ' malformed cell count');
    return Object.fromEntries(header.map((key, i) => [key, cells[i] ?? '']));
  });
  return rows;
}
function unique(rows, key, name) { check(new Set(rows.map(x => x[key])).size === rows.length, name + ' duplicate ' + key); }
function setEq(a, b, name) {
  const aa = new Set(a), bb = new Set(b);
  check(aa.size === bb.size && [...aa].every(x => bb.has(x)), name + ' anti-join mismatch');
}
const t1 = 'effa0a9e2aa9b2c156c43bd8c093f45faaa291b6';
const p = '256d46bf425cc37e114465cddbe3c60e535766ab';
const map = parseTSV('INTENDED_ACTUAL_TRANSFORMATION_MAP.tsv');
const actions = parseTSV('DISCREPANCY_AND_OWNER_ACTIONS.tsv');
const reverse = parseTSV('REVERSE_CONSUMER_TRACES.tsv');
const fates = parseTSV('R1_235_TO_T1_R3_52_CROSSWALK.tsv');
check(map.length === 52, 'not 52 T1 R3 contracts');
check(actions.length === 63, 'not 52 contract + 11 current decisions');
check(reverse.length === 534, 'not 534 source/code/roadmap evidence records');
check(fates.length === 235, 'not 235 inherited R1 fates');
unique(map, 'transform_id', 'transform map');
unique(actions, 'contract_or_current_id', 'actions');
unique(reverse, 'reverse_id', 'reverse');
unique(fates, 'r1_id', 'R1 fate');
const historic = new Set(map.map(r => r.transform_id));
const current = actions.filter(r => r.contract_or_current_id.startsWith('CUR-'));
const currentIds = current.map(x => x.contract_or_current_id);
check(current.length === 11, 'not eleven independently bounded current-first capabilities');
setEq(map.map(x => x.transform_id), actions.filter(x => !x.contract_or_current_id.startsWith('CUR-')).map(x => x.contract_or_current_id), 'historic contract/action');
setEq(map.map(x => x.transform_id), reverse.filter(x => x.grain === 'T1_R3_DISTINCT_CONTRACT').map(x => x.downstream_terminal_or_consumer), 'historic contract/reverse');
setEq(currentIds, reverse.filter(x => x.grain === 'CURRENT_FIRST_CAPABILITY').map(x => x.reverse_id.replace(/^CURRENT:/, '')), 'current first/reverse');
for (const r of map) {
  check(r.h_t1_r3_head === t1, 'obsolete T1 source pinned for ' + r.transform_id);
  for (const k of ['h_selected_input','h_guard_predicate','h_before_to_after_semantic_change','h_output','h_negative_or_refusal','h_c6_static_grade_and_runtime_limit','p_selected_oct28_pipeline_stage_and_precise_requirement','p_authoritative_owner','p_contract_specific_adoption_grade','c_protected_code_symbol_or_absence','c_rule_and_input_actually_bound_at_protected_cut','c_static_emitted_output_or_negative_NOT_EXECUTED','c_meaningful_first_reader_and_grade','earliest_h_to_p_to_c_discrepancy','smallest_s0_s1_falsifier'])
    check(Boolean(r[k]), r.transform_id + ' missing ' + k);
  check(/NOT_OBSERVED|NOT_PROVED|NO_/.test(r.h_c6_static_grade_and_runtime_limit), 'C6 original invocation overstated '+r.transform_id);
  check(!/(^|[;\\s])(?:ACCEPTED_EQUIVALENT|JUSTIFIED_RETIRED|NATIVE_ZERO_LOSS)(?:[;\\s]|$)/.test(r.equivalence_or_retirement_decision), 'overclaim '+r.transform_id);
}
for(const k of ['p_selected_oct28_pipeline_stage_and_precise_requirement','c_protected_code_symbol_or_absence','c_static_emitted_output_or_negative_NOT_EXECUTED','c_meaningful_first_reader_and_grade','earliest_h_to_p_to_c_discrepancy'])
  check(new Set(map.map(x=>x[k])).size === 52, 'template/group collapse in ' + k);
const strict = fates.filter(x => x.t2_strict_semantic_successor_if_any !== 'NO_PROVED_SAME_STATIC_BRANCH');
check(strict.length === 7, 'not seven narrowly supported strict F03/F08 branches');
for(const f of fates){
  check(f.t2_original_t1_r3_head === t1, 'R1 fate stale historical head '+f.r1_id);
  if (f.t2_strict_semantic_successor_if_any === 'NO_PROVED_SAME_STATIC_BRANCH')
    check(f.t2_successor_relation_grade.includes('NO_SEMANTIC_EQUIVALENCE'), 'fabricated R1 equivalence '+f.r1_id);
  else {
    check(historic.has(f.t2_strict_semantic_successor_if_any), 'R1 unknown strict target '+f.r1_id);
    check(f.t2_successor_relation_grade.includes('SAME_CODE_BRANCH_ON_STATIC_EVIDENCE'), 'R1 strict not evidence-qualified '+f.r1_id);
  }
}
const counts={};
for(const r of reverse)counts[r.grain]=(counts[r.grain]||0)+1;
for(const [grain,n] of Object.entries({CURRENT_FIRST_CAPABILITY:11,ROADMAP_SECTION_NOT_RUNTIME:11,ROADMAP_NAMED_CHILD:51,J_TYPED_SEAM_EDGE:82,G4_ORIGINAL_GAP:49,T1_R3_DISTINCT_CONTRACT:52,PROTECTED_PY_MODULE_CENSUS:160,DIRECT_PROTECTED_CALLSITE:44,INHERITED_LONG_MEMORY_OBLIGATION_NOT_RUNTIME:74}))
  check(counts[grain] === n, grain+' source/call/roadmap grain mismatch');
const lm = reverse.filter(x=>x.grain==='INHERITED_LONG_MEMORY_OBLIGATION_NOT_RUNTIME');
check(lm.filter(x=>x.reverse_id.startsWith('LM:LMX-')).length===44, 'LMX inherited count');
check(lm.filter(x=>x.reverse_id.startsWith('LM:LMQ-')).length===30, 'LMQ inherited count');
check(lm.some(x=>x.reverse_id==='LM:LMX-043' && /ATOMIC/.test(x.selected_authority_predicate)), 'LMX-043 lost atomicity');
const moduleRows=reverse.filter(x=>x.grain==='PROTECTED_PY_MODULE_CENSUS');
const callRows=reverse.filter(x=>x.grain==='DIRECT_PROTECTED_CALLSITE');
unique(moduleRows,'protected_file_symbol','module ledger');
check(callRows.every(x=>(x.code_source_grade.includes('LEXICAL_') || x.code_source_grade.includes('DIRECT_BODY_CALL_CONFIRMED_S1')) && x.actual_callsite_line!=='NOT_PROVED'), 'calls misgraded or without line');
check(reverse.filter(x=>x.grain==='J_TYPED_SEAM_EDGE').every(x=>/SOURCE_GRAPH_EDGE|ROADMAP|NOT_CODE_CALL/.test(x.code_source_grade)), 'J graph promoted to code');
check(reverse.filter(x=>x.grain==='G4_ORIGINAL_GAP').every(x=>/ROADMAP|NOT_EXECUTED|NOT_CODE/.test(x.code_source_grade)), 'G4 gap promoted to executable code');
check(map.every(x=>x.h_t1_r3_head===t1), 'T1 R3 source frozen');

// Falsify a validator that merely checks counts but not identities/source provenance.
function synthetic(name, mutate, detect){
  const altered=mutate(); check(detect(altered), 'synthetic negative control FAILED: '+name);
}
synthetic('duplicate historic id',()=>[...map.slice(0,51),{...map[51],transform_id:map[0].transform_id}], x=>new Set(x.map(r=>r.transform_id)).size!==52);
synthetic('stale T1 evidence',()=>({...map[0],h_t1_r3_head:'627660cfca3e638b793c9e6369ab3ea314c9018b'}), x=>x.h_t1_r3_head!==t1);
synthetic('invented strict successor',()=>({...fates[17],t2_strict_semantic_successor_if_any:'T1R2-FAKE'}), x=>!historic.has(x.t2_strict_semantic_successor_if_any));
synthetic('demote selected branch',()=>[...fates.slice(0,1),{...fates[1],t2_strict_semantic_successor_if_any:'NO_PROVED_SAME_STATIC_BRANCH'},...fates.slice(2)], x=>x.filter(r=>r.t2_strict_semantic_successor_if_any!=='NO_PROVED_SAME_STATIC_BRANCH').length!==7);
synthetic('roadmap as code',()=>({...reverse.find(x=>x.grain==='J_TYPED_SEAM_EDGE'),code_source_grade:'DIRECT_PROTECTED_S1'}),x=>!/SOURCE_GRAPH_EDGE|ROADMAP|NOT_CODE_CALL/.test(x.code_source_grade));
synthetic('drop LMX rollback',()=>({...lm.find(x=>x.reverse_id==='LM:LMX-043'),selected_authority_predicate:'serialize'}),x=>!/ATOMIC/.test(x.selected_authority_predicate));
synthetic('miss a current capability',()=>actions.filter(x=>x.contract_or_current_id!=='CUR-M5-RSC'),x=>x.length!==63);
synthetic('module SHA replaced',()=>({...moduleRows[0],code_module_sha:'f'.repeat(40)}),x=>x.code_module_sha!==moduleRows[0].code_module_sha);
synthetic('callsite row replaced',()=>({...callRows[0],actual_callsite_line:'NOT_PROVED'}),x=>x.actual_callsite_line==='NOT_PROVED');

// Optional independently repeatable bounded code search against exact source cut.
// Lexical search is *not* Python callgraph resolution or proof of executed reader.
if(protectedRoot){
  const root=path.resolve(protectedRoot);
  const code=new Map();
  for(const r of moduleRows){
    const file=path.join(root,r.protected_file_symbol);
    check(fs.existsSync(file),'missing protected file '+r.protected_file_symbol);
    if(!fs.existsSync(file))continue;
    const bytes=fs.readFileSync(file);
    const gitHeader=Buffer.from('blob '+bytes.length+'\0');
    const hash=crypto.createHash('sha1').update(gitHeader).update(bytes).digest('hex');
    check(hash===r.code_module_sha,'changed protected module '+r.protected_file_symbol);
    code.set(r.protected_file_symbol,bytes.toString('utf8').split(/\r?\n/));
  }
  check(code.size===160,'bounded module census incomplete');
  for(const r of callRows){
    const m=/^CALL:([^:]+):(.+):(\d+)$/.exec(r.reverse_id);
    check(Boolean(m),'malformed call identifier '+r.reverse_id);
    if(!m)continue;
    const [,symbol,file,n]=m; const line=code.get(file)?.[Number(n)-1]||'';
    const regex=new RegExp('(^|[^\\w])'+symbol+'\\s*\\(');
    check(regex.test(line) && !/^\s*(def |#)/.test(line),'callsite not repeatable '+r.reverse_id);
  }
  const noExternal=['evaluate_m1_temporal_v554_admission_dedup','evaluate_m2_v555_atomic_route','evaluate_m3_v556_higher_order_structural','bind_structural_peer_use','select_r05_world_view','progressive_world_view','evaluate_structural_empirical_admission','compose_learned_world','evaluate_learned_world_consumer'];
  for(const symbol of noExternal){
    const rx=new RegExp('(^|[^\\w])'+symbol+'\\s*\\(');
    const hits=[];
    for(const [file,lines] of code) for(let i=0;i<lines.length;i++){
      const s=lines[i];if(rx.test(s)&&!/^\s*(def |#)/.test(s))hits.push(file+':'+(i+1));
    }
    check(hits.length===0,'unexpected bounded lexical caller '+symbol+':'+hits.join(','));
  }
}
const result={contracts:map.length,actions:actions.length,reverse:reverse.length,r1_fates:fates.length,strict_static_successors:strict.length,independent_lm:lm.length,protected_file_census:moduleRows.length,lexical_calls:callRows.length,source_t1_r3:t1,protected_pre_main:p,protected_checkout_verified:Boolean(protectedRoot),assertions,errors};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
if(errors.length)process.exitCode=1;
