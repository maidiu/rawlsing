/* G4 no-drop/inherited-function/head-drift guard. No semantic accreditation. */
import {readFile} from "node:fs/promises";
const ROOT=new URL("./",import.meta.url);
function drift(expected,observed){
 const filtered=x=>x.filter(p=>p.title_based_scope==="POSSIBLY_PYAT");
 const E=new Map(filtered(expected).map(p=>[p.pr,p])), O=new Map(filtered(observed).map(p=>[p.pr,p]));
 let issues=[];for(const [id,e] of E){const o=O.get(id);if(!o){issues.push({pr:id,status:"CLOSED_OR_UNOBSERVED_REQUIRES_FATE_RECEIVING",old_head:e.head});continue}if(e.head!==o.head)issues.push({pr:id,status:"STALE_SOURCE_HEAD_REQUIRES_TARGETED_G4_RECEIVING",old_head:e.head,new_head:o.head});}
 for(const [id,o] of O)if(!E.has(id))issues.push({pr:id,status:"NEW_RELEVANT_BRANCH_UNRECONCILED",new_head:o.head});
 return issues.sort((a,b)=>a.pr-b.pr);
}
function antiAbsence(claims){
 const known=[
 ["I05_ADAPTIVE","adaptive scheduler|adaptive exploration|i05 adaptive","rawlsing_next/pre553_discovery_adaptive.py::execute_adaptive_exploration@5d387a9a"],
 ["F012_ENTROPY_MI","entropy|mutual information|information gain|f012","rawlsing_next/pre553_diagnostics.py::_association_metrics@5d387a9a"],
 ["S04_KWAY_REVERSE","reverse inference|reverse conditional|k.way|s04 reverse","rawlsing_next/pre553_s04_general_joint_algebra.py::S04GeneralJointWorkspace.query@434f88c9 (CANDIDATE)"],
 ["F6M_BOUNDS","fr[eé]chet|partial identification bounds|intersection bounds","WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py::complementary_binary_bounds@1f1c72f8"],
 ["POSITION_WALKBACK","positioned.subject walkback|specificity walkback|positioned subject specificity","rawlsing_next/source_backed_positioned_subject_possibility.py@5d387a9a"]
 ];
 const held=[];for(const c of claims){if(c.proposed_status!=="MISSING")continue;let txt=(c.function||"").toLowerCase();for(const [id,pattern,owner] of known){if(new RegExp(pattern,"i").test(txt))held.push({id,status:"FALSE_ABSENCE_REUSE_OWNER_CHECK_REQUIRED",proposed:c.function,existing_owner:owner,consumer_specific_delta:c.consumer_specific_delta||null});}}
 return held;
}
function validateRows(index,parity,components,seams,manifest){
 const specs=[[index,"id",782],[parity,"obligation_id",150],[components,"id",62],[seams,"edge_id",82]];
 const failures=[];for(const [rows,key,count] of specs){if(rows.length!==count)failures.push("G4_EXPECTED_"+count+"_FOUND_"+rows.length);if(new Set(rows.map(x=>x[key])).size!==rows.length)failures.push("DUPLICATE_"+key)}
 if(index.filter(x=>x.kind==="GUIDE_SECTION").length!==11)failures.push("SECTION_COUNT");
 if(index.filter(x=>x.kind==="GUIDE_SECTION"&&!x.g4_once_20261120).length)failures.push("CHAPTER_CROSSWALK_LOST");
 if(parity.some(x=>!x.g4_once_20261120))failures.push("FUNCTION_EVIDENCE_LANE_LOST");
 if(components.some(x=>!x.g4_once_20261120))failures.push("COMPONENT_EVIDENCE_LANE_LOST");
 if(seams.some(x=>!x.g4_once_20261120))failures.push("SEAM_EVIDENCE_LANE_LOST");
 if(seams.some(x=>x.g4_once_20261120.original_requiredness_preserved!==x.original_requiredness))failures.push("CONDITIONAL_SEAM_PROMOTED");
 if(manifest?.protected_pre_main!=="5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e")failures.push("PROTECTED_SOURCE_CUT_CONFLICT");
 if(manifest?.open_PR_snapshot?.count!==manifest?.open_PR_snapshot?.all_open_prs_compact?.length)failures.push("OPEN_PR_PATH_LOSS");
 const chapters=new Set(index.filter(x=>x.kind==="GUIDE_SECTION").flatMap(x=>x.g4_once_20261120.chapters_mapped));
 for(const n of ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX"])if(!chapters.has(n))failures.push("MISSING_CHAPTER_"+n);
 const sourceGrains={zak02:28,vosk_a:18,vosk_b:26,k1:29,k3_proposals:26,k3_edges:8,vmestye_p4r:14};
 const recovered=Object.fromEntries(Object.keys(sourceGrains).map(k=>[k,[]]));
 for(const section of index.filter(x=>x.kind==="GUIDE_SECTION")){
   const crosswalk=section.g4_once_r2_inherited_source_crosswalk;
   if(!crosswalk){failures.push("G4_R2_SECTION_WITHOUT_INHERITED_SOURCE_"+section.id);continue;}
   for(const key of Object.keys(sourceGrains)){
     const rows=crosswalk.source_adjudications?.[key];
     if(!Array.isArray(rows)){failures.push("G4_R2_SOURCE_GROUP_MISSING_"+section.id+"_"+key);continue;}
     recovered[key].push(...rows.map(v=>v.id));
     if(rows.some(v=>!v.id))failures.push("G4_R2_UNIDENTIFIED_SOURCE_"+section.id+"_"+key);
   }
 }
 for(const [key,n] of Object.entries(sourceGrains)){
   if(recovered[key].length!==n||new Set(recovered[key]).size!==n)failures.push("G4_R2_SOURCE_LOSS_OR_DUPLICATE_"+key+"_EXPECTED_"+n+"_ACTUAL_"+recovered[key].length);
 }
 const joins=index.find(x=>x.id==="ROADMAP:S11")?.g4_once_r2_inherited_source_crosswalk?.unresolved_w1h_custody?.ids||[];
 if(joins.length!==164||new Set(joins).size!==164)failures.push("G4_R2_W1H_164_UNJOINED_CUSTODY_LOST");
 const k1ar=index.find(x=>x.id==="ROADMAP:S01")?.g4_once_r3_k1_source_authority_unjoined?.unjoined_AR_records||[];
 const k1history=index.find(x=>x.id==="ROADMAP:S11")?.g4_once_r3_k1_historical_custody;
 if(k1ar.length!==47||new Set(k1ar.map(x=>x.id)).size!==47)failures.push("G4_K1_47_SOURCE_AUTHORITY_UNJOINED_LOST");
 if(k1history?.typed_unjoined_67?.AR_unverified!==47||k1history?.typed_unjoined_67?.held_owner_actions?.length!==14||k1history?.typed_unjoined_67?.nonadditive_families?.length!==6)failures.push("G4_K1_67_TYPED_SENTINEL_DECOMPOSITION_LOST");
 if(k1history?.inherited_history?.LMX44?.length!==44||k1history?.inherited_history?.LMQ30?.length!==30)failures.push("G4_K1_LMX44_LMQ30_HISTORICAL_CUSTODY_LOST");
 const historicLinks=parity.filter(x=>x.g4_once_r2_historical_function_relationship);
 if(historicLinks.length!==18||historicLinks.some(x=>x.g4_once_r2_historical_function_relationship.preserve_frozen_parity!==x.parity))failures.push("G4_R2_18_HISTORICAL_FUNCTION_LINKS_LOST_OR_PARITY_PROMOTED");
  return {pass:failures.length===0,failures,counts:Object.fromEntries(specs.map(([x,k,n])=>[k+"_"+n,x.length])),chapters:chapters.size,inherited:Object.fromEntries(Object.keys(sourceGrains).map(k=>[k,recovered[k].length])),w1h_unjoined:joins.length,historical_function_relations:historicLinks.length};
}
function selfTest(){
 const E=[{pr:1,head:"aaa",title_based_scope:"POSSIBLY_PYAT"}],same=JSON.parse(JSON.stringify(E));
 let cases=[
 {name:"UNCHANGED_CANDIDATE_ALLOWED",pass:drift(E,same).length===0},
 {name:"ALTERED_CANDIDATE_HEAD_HELD",pass:drift(E,[{...E[0],head:"bbb"}])[0]?.status==="STALE_SOURCE_HEAD_REQUIRES_TARGETED_G4_RECEIVING"},
 {name:"CLOSED_BRANCH_FATE_HELD",pass:drift(E,[])[0]?.status==="CLOSED_OR_UNOBSERVED_REQUIRES_FATE_RECEIVING"},
 {name:"NEW_BRANCH_REQUIRES_RECONCILIATION",pass:drift(E,[...E,{pr:2,head:"ccc",title_based_scope:"POSSIBLY_PYAT"}]).some(x=>x.pr===2)},
 {name:"RECEIVED_NEW_HEAD_ALLOWED",pass:drift([{...E[0],head:"bbb"}],[{...E[0],head:"bbb"}]).length===0},
 {name:"FALSE_ABSENCE_FIVE_KNOWN_OWNERS_RED",pass:antiAbsence(["Build adaptive scheduler","Build entropy MI","Build reverse inference","Invent Fréchet bounds","Build positioned subject specificity walkback"].map(function(s){return{proposed_status:"MISSING",function:s}})).length===5}
 ];return {pass:cases.every(x=>x.pass),cases};
}
const FILES=["INDEX.jsonl","FUNCTION_PARITY.jsonl","COMPONENT_STATUS.jsonl","CURRENT_SEAM_STATES.jsonl","G4_ONE_TIME_SOURCE_AND_BRANCH_COVERAGE_20261120_R1.json"];
async function load(){const r=await Promise.all(FILES.map(async f=>{const txt=await readFile(new URL(f,ROOT),"utf8");return f.endsWith(".jsonl")?txt.trim().split("\n").map(JSON.parse):JSON.parse(txt)}));return r;}
async function livePRs(){const all=[];for(let page=1;page<=30;page++){let url="https://api.github.com/repos/maidiu/rawlsing/pulls?state=open&per_page=100&page="+page;let headers={"Accept":"application/vnd.github+json"};if(process.env.GITHUB_TOKEN)headers.Authorization="Bearer "+process.env.GITHUB_TOKEN;let res=await fetch(url,{headers});if(!res.ok)throw Error("G4_LIVE_PR_FETCH_FAILED_STATUS_"+res.status);let data=await res.json();all.push(...data);if(data.length<100)break;}const re=/pyat|dhikr|anvil|field.?forge|source|C11|F6|I03|N10|G4|Q014|Q019|programme|programma|s04|c6|n9/i;return all.map(p=>({pr:p.number,head:p.head.sha,branch:p.head.ref,base:p.base.ref,title_based_scope:re.test(p.title+" "+p.head.ref+" "+p.base.ref)?"POSSIBLY_PYAT":"NOT_CLASSIFIED_PYAT_BY_TITLE"}));}
async function main(){if(process.argv.includes("--self-test")){const result=selfTest();console.log(JSON.stringify(result));process.exitCode=result.pass?0:1;return;}let files=await load();const result=validateRows(...files);const issues=[...result.failures];let observed=undefined;
if(process.argv.includes("--github-current"))observed=await livePRs();
if(process.argv.includes("--observed")){const i=process.argv.indexOf("--observed");observed=JSON.parse(await readFile(process.argv[i+1],"utf8"));}
if(observed){const driftResult=drift(files[4].open_PR_snapshot.all_open_prs_compact,observed);issues.push(...driftResult.map(x=>x.status+"_PR_"+x.pr));console.log(JSON.stringify({drift:driftResult}));}
if(process.argv.includes("--claims")){const i=process.argv.indexOf("--claims");let claims=JSON.parse(await readFile(process.argv[i+1],"utf8"));const falseAbsence=antiAbsence(claims);issues.push(...falseAbsence.map(x=>x.status+"_"+x.id));console.log(JSON.stringify({false_absence:falseAbsence}));}
console.log(JSON.stringify({integrity:result,unresolved:issues,grade:"IDENTITY_AND_HEAD_CURRENTNESS_ONLY_NOT_FUNCTIONAL_SCIENCE"}));process.exitCode=issues.length?1:0;
}
await main();
