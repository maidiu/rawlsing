"use strict";
/* ZL-15 R8 P4-R4 73-row corrective court. S0-S1 source-documentary ONLY.
 * This court DOES NOT establish semantic conservation, first-reader operation, original35,
 * science/source/actor admission or independent acceptance. It rejects the R7 unsupported
 * HISTORICAL_HEURISTIC_ONLY mapping while preserving the original documentary record.
 */
const fs=require("fs"),cp=require("child_process"),path=require("path"),crypto=require("crypto");
const ROOT="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N020_LONG_MEMORY/VMESTYE/";
const JOIN=ROOT+"PRONGS/J_JOIN/";
const R6="702e91b8ed2d330178f6c2889db25abed8d6d53b", R7="8072f1e64c4c8e5fe4c82d64db2742a9f55e0f46";
const B={
  "r6Atlas": "9c0db6568c5b0c9850ea9d422aca8c88443a172c",
  "r7Atlas": "0c89d8767e9ee958217b4e0d07d72c22b7a0e485",
  "r8Atlas": "68f146b5bb06d96c2469369d5c70ab4bd39e2944",
  "r7Ledger": "42aca79ee6b775b2a38d7b7abdf29c937f8ebd0c",
  "r8Ledger": "012fef58ef2cf0e3d1befc51756ac653a4054778",
  "delta": "a905832f62dfb8f181b20311b0cb5d0a8422fdb4",
  "review": "77e0042fa62339d489dc98ed5c1ae3a67f4271b0"
};
const allowed=new Set("PROVED_CURRENT_SUCCESSOR PROVED_STRONGER_SUPERSESSION PARTIAL_SUCCESSION OPEN_FUNCTIONAL_GAP OPEN_PROOF_GAP HISTORICAL_HEURISTIC_ONLY ACCIDENTAL_OR_OBSOLETE_MECHANIC OUTSIDE_PREV3__EXACT_OWNER DUPLICATE_OR_ALIAS NOT_INSPECTED".split(" "));
function ok(cond,why){if(!cond)throw Error(why);}
function blobHash(s){return crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+Buffer.byteLength(s)+"\\0"),Buffer.from(s)])).digest("hex");}
function parse(s,name){const lines=s.trimEnd().split(/\\r?\\n/),cols=lines.shift().split("\\t");return{cols,rows:lines.map((line,i)=>{const vs=line.split("\\t");ok(vs.length===cols.length,name+" width "+(i+2));return Object.fromEntries(cols.map((c,j)=>[c,vs[j]]))})};}
function dump(t){return t.cols.join("\\t")+"\\n"+t.rows.map(r=>t.cols.map(c=>r[c]).join("\\t")).join("\\n")+"\\n";}
function idx(rs,key){const m=new Map;for(const r of rs){ok(r[key]&&!m.has(r[key]),"duplicate/empty "+key+" "+r[key]);m.set(r[key],r)}return m}
function run(x) {
 for(const [k,blob] of Object.entries(B))ok(blobHash(x[k])===blob,"pinned blob mismatch "+k);
 const b=parse(x.r6Atlas,"R6"),p=parse(x.r7Atlas,"R7"),a=parse(x.r8Atlas,"R8"),m7=parse(x.r7Ledger,"R7 migration"),m8=parse(x.r8Ledger,"R8 migration"),d=parse(x.delta,"R8 delta"),r=parse(x.review,"P4 R4 review");
 ok(b.rows.length===1740&&p.rows.length===1740&&a.rows.length===1740&&m7.rows.length===655&&m8.rows.length===655&&d.rows.length===73&&r.rows.length===73,"source counts");
 ok(b.cols.join("|")===p.cols.join("|")&&p.cols.join("|")===a.cols.join("|"),"atlas fields");
 const old=idx(b.rows,"record_id"),prev=idx(p.rows,"record_id"),cur=idx(a.rows,"record_id"),ml7=idx(m7.rows,"record_id"),ml8=idx(m8.rows,"record_id"),dd=idx(d.rows,"record_id"),rr=idx(r.rows,"r7_record_id");
 ok(ml8.size===655&&dd.size===73&&rr.size===73,"distinct count");
 let deltaCount=0,allMigrate=0;
 for(const o of b.rows) {
  const id=o.record_id,q=prev.get(id),v=cur.get(id),l=ml8.get(id),h=ml7.get(id),g=dd.get(id),rev=rr.get(id);
  ok(q&&v&&q.record_id===id&&v.record_id===id,"identity/order");
  for(const f of b.cols)if(f!=="disposition")ok(o[f]===v[f]&&q[f]===v[f],"nonstatus field changed "+id+" "+f);
  ok(allowed.has(v.disposition),"illegal canonical value "+id);
  if(h){allMigrate++;ok(l&&l.r6_literal_disposition===o.disposition&&l.r8_canonical_disposition==="OPEN_PROOF_GAP"&&v.disposition==="OPEN_PROOF_GAP","R6 migration not open "+id);
   ok(h.r6_literal_disposition===l.r6_literal_disposition&&h.r6_source_locator===l.r6_source_locator&&l.r6_source_locator===o.source,"source ledger rewritten "+id);
   ok(h.row_specific_evidence_basis===l.r7_original_status_basis_limited&&h.original_next_proof_or_falsifier===l.original_next_proof_or_falsifier&&h.original_owner_route===l.original_owner_route&&h.original_purpose===l.original_purpose,"historical source custody changed "+id);
   ok(h.r7_canonical_disposition===q.disposition,"R7 migration edited "+id);
  } else ok(!l&&v.disposition===o.disposition,"R6 status not mapped "+id);
  if(g){
   deltaCount++;ok(rev&&q.disposition==="HISTORICAL_HEURISTIC_ONLY"&&v.disposition==="OPEN_PROOF_GAP","73 change not exact "+id);
   ok(rev.lawful_interim_disposition==="OPEN_PROOF_GAP"&&rev.exact_separate_conservation_proved==="NONE_PROVED"&&rev.direct_same_grain_conservation_links==="0"&&rev.independent_decision==="REVISE_HEURISTIC_NOT_SUBSTANTIATED","review unsupported "+id);
   ok(g.r7_disposition===q.disposition&&g.r8_disposition===v.disposition&&g.original_source_locator===o.source&&g.r6_literal_disposition===o.disposition,"delta identity/source mismatch "+id);
   ok(g.independent_semantic_finding===rev.independent_law_test_and_reason&&g.original_negative===rev.original_negative&&g.individual_proof_action_and_falsifier===rev.proof_action_and_falsifier&&g.source_claim_or_valuable_duty===rev.source_claim_or_valuable_duty,"independent record content mutated "+id);
   ok(g.first_non_test_consumer===v.actual_consumer_ids&&g.current_owner===v.pyat_owner_ids&&g.exact_separate_conservation_proved==="NONE_PROVED","fabricated owner/first reader "+id);
   ok(l&&l.p4_r4_record_id===id&&l.p4_r4_reviewer_commit==="f8e0ed3d8b17777c1149230a109827be42a842a8"&&l.p4_r4_adjudication_scope.startsWith("73_RECORD_"),"migration review not attributed "+id);
  } else ok(!rev&&q.disposition===v.disposition,"R7 to R8 unauthorized change "+id);
 }
 ok(allMigrate===655&&deltaCount===73,"migration or delta coverage");
 for(const id of dd.keys())ok(rr.has(id)&&cur.has(id),"orphan delta "+id);
 for(const id of rr.keys())ok(dd.has(id),"unaddressed review "+id);
 for(const id of ml8.keys())ok(ml7.has(id),"orphan migration "+id);
 const reversed=parse(x.r8Atlas,"reverse");for(const row of reversed.rows)if(ml8.has(row.record_id))row.disposition=ml8.get(row.record_id).r6_literal_disposition;
 ok(dump(reversed)===x.r6Atlas,"R8-to-R6 byte exact reversal");
 const status={};for(const row of a.rows)status[row.disposition]=(status[row.disposition]||0)+1;
 ok(status.OPEN_PROOF_GAP===1691&&status.HISTORICAL_HEURISTIC_ONLY===2&&status.PARTIAL_SUCCESSION===33&&status.NOT_INSPECTED===13&&status.OPEN_FUNCTIONAL_GAP===1,"R8 status totals");
 return {canonicalAtlasRows:1740,r6MigratedRows:655,r7ToR8DispositionOnlyChanges:deltaCount,reviewedRows:73,openProofGapMigrated:655,atlasStatusCounts:status,fullR6AtlasByteReversal:true,sourceTier:"S0_S1_DOCUMENTARY_ONLY",s2:"NOT_RUN",s3Original35:"NOT_RUN",semanticConservation:"NOT_PROVED",firstConsumer:"NOT_PROVED"};
}
if(require.main===module){
 const repo=cp.execFileSync("git",["rev-parse","--show-toplevel"],{encoding:"utf8"}).trim();
 const read=p=>fs.readFileSync(path.join(repo,p),"utf8");
 const historical=(ref,p)=>cp.execFileSync("git",["show",ref+":"+p],{encoding:"utf8",maxBuffer:30*1024*1024});
 const x={
 r6Atlas:historical(R6,ROOT+"DATA/FUNCTION_ATLAS.tsv"),
 r7Atlas:historical(R7,ROOT+"DATA/FUNCTION_ATLAS.tsv"),
 r8Atlas:read(ROOT+"DATA/FUNCTION_ATLAS.tsv"),
 r7Ledger:historical(R7,JOIN+"INHERITED_STATUS_CANONICAL_MIGRATION_R7.tsv"),
 r8Ledger:read(JOIN+"INHERITED_STATUS_CANONICAL_MIGRATION_R8.tsv"),
 delta:read(JOIN+"R8_P4_R4_73_RECORD_SEMANTIC_CORRECTIONS.tsv"),
 review:read(JOIN+"R8_FROZEN_INDEPENDENT_P4_R4_73_ROW_REVIEW.tsv")
 };
 console.log(JSON.stringify({court:"ZL15_R8_P4_R4_AUTHOR_DOCUMENTARY",...run(x),nodeCli:"EXECUTED"},null,2));
}
module.exports={run};
