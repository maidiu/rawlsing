"use strict";
/*
 * VMESTYE ZL-15 R7 — exact R6-to-R7 global canonical status court.
 * S0–S1 documentary comparison ONLY. No original35/S2/S3 or owner/science grant.
 * Cold execution requires immutable R6 and R5 Git objects locally accessible.
 */
const fs = require("fs"), cp = require("child_process"), crypto = require("crypto"), path = require("path");
const BASE = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N020_LONG_MEMORY/VMESTYE/";
const R6 = "702e91b8ed2d330178f6c2889db25abed8d6d53b";
const BLOBS = {
  r6Atlas: "9c0db6568c5b0c9850ea9d422aca8c88443a172c",
  r7Atlas: "0c89d8767e9ee958217b4e0d07d72c22b7a0e485",
  r7Ledger: "42aca79ee6b775b2a38d7b7abdf29c937f8ebd0c",
  r6Audit: "6a8686d8813a5a768bae9af682aa0849f63a4c84",
  relations: "c863a906382ee4bfa5d08b9d7c5f6ed7a055fa38",
  evidence: "75d6e2d29425b5f6438cd7808b1487bfd4e2691c",
  seeds: "6ebee656c48628451943697c9649b9af88f03365"
};
const ALLOWED = new Set("PROVED_CURRENT_SUCCESSOR PROVED_STRONGER_SUPERSESSION PARTIAL_SUCCESSION OPEN_FUNCTIONAL_GAP OPEN_PROOF_GAP HISTORICAL_HEURISTIC_ONLY ACCIDENTAL_OR_OBSOLETE_MECHANIC OUTSIDE_PREV3__EXACT_OWNER DUPLICATE_OR_ALIAS NOT_INSPECTED".split(" "));
const EXPECTED_PRONG_COUNTS = { ZL03:19, ZL04:13, ZL05:151, ZL06:105, ZL07:62, ZL08:143, ZL09:42, ZL11:87, ZL12:26, ZL13:7 };
function ok(x, why) { if (!x) throw Error(why); }
function blobHash(s) { return crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob " + Buffer.byteLength(s) + "\0"), Buffer.from(s)])).digest("hex"); }
function parse(s,name) {
  const lines=s.trimEnd().split(/\r?\n/), fields=lines.shift().split("\t");
  ok(fields.length>1, name+" empty header");
  ok(new Set(fields).size===fields.length, name+" duplicate header");
  const rows=lines.map((line,i)=>{
    const c=line.split("\t");
    ok(c.length===fields.length,name+" invalid width at line "+(i+2));
    return Object.fromEntries(fields.map((f,j)=>[f,c[j]]));
  });
  return {fields, rows};
}
function serialize(t) {return t.fields.join("\t")+"\n"+t.rows.map(r=>t.fields.map(k=>r[k]).join("\t")).join("\n")+"\n";}
function index(t,key,name) {
  ok(t.fields.includes(key),name+" no "+key);
  const m=new Map();
  for(const r of t.rows) {const v=r[key];ok(v&&!m.has(v),name+" duplicate/empty "+key+" "+v);m.set(v,r);}
  return m;
}
function historicalBasis(r) {
  if (r.disposition==="HISTORICAL_BRANCH_INDEX" &&
      /^J-F-ZL05-ZL05-BR-/.test(r.record_id) &&
      r.function_statement.includes("Branch-era genealogy index"))
    return "ARCHIVAL_BRANCH_GENEALOGY_POINTER_NOT_EXECUTABLE_FUNCTION";
  if (r.disposition==="HISTORICAL_SOURCE_LOCATOR" &&
      /^J-F-ZL05-ZL05-REF-/.test(r.record_id) &&
      r.function_statement.includes("It is a source locator, not independent execution."))
    return "ARCHIVAL_SOURCE_REFERENCE_NOT_INDEPENDENT_OPERATION";
  if (r.disposition==="INAPPLICABLE_NOT_FUNCTION" &&
      /^J-F-ZL13-F_C6_(DENOMINATOR|CROSSREF)_/.test(r.record_id) &&
      r.completeness_grade.includes("S0_INDEX"))
    return "HISTORICAL_DENOMINATOR_OR_CROSSREF_ACCOUNTING_GRAIN_NOT_FUNCTION";
  if (["DIAGNOSTIC_ONLY","MIGRATION_ONLY","OPTIONAL_CACHE_OR_ACCELERATOR"].includes(r.disposition) &&
      /^J-F-ZL06-ZL06-F\d+$/.test(r.record_id) &&
      r.function_statement.includes("Distinguish binding semantics from physical assumption"))
    return "HISTORICAL_NONBINDING_PHYSICAL_DIAGNOSTIC_OR_MIGRATION_ASSUMPTION";
  return "SOURCE_GRADED_DOCUMENTARY_FINDING_CURRENT_SAME_GRAIN_AND_FIRST_READER_UNPROVED";
}
function expectedStatus(r) {
  return historicalBasis(r).startsWith("SOURCE_GRADED") ? "OPEN_PROOF_GAP" : "HISTORICAL_HEURISTIC_ONLY";
}
function verify(x) {
  const original=parse(x.r6Atlas,"immutable R6 atlas"), current=parse(x.r7Atlas,"R7 atlas"),
        ledger=parse(x.ledger,"R7 reversible ledger"), audit=parse(x.audit,"unchanged R6 audit");
  ok(original.fields.join("\t")===current.fields.join("\t"),"atlas schema drift");
  ok(original.rows.length===1740 && current.rows.length===1740 && ledger.rows.length===655 && audit.rows.length===655,"atlas/ledger census wrong");
  const old=index(original,"record_id","R6 atlas"), now=index(current,"record_id","R7 atlas"),
        migrations=index(ledger,"record_id","R7 ledger"), oldDebt=index(audit,"record_id","R6 audit");
  ok(old.size===now.size,"atlas distinct keys mismatch");
  const expectedLedgerFields="record_id namespace r6_source_locator r6_literal_disposition r7_canonical_disposition row_specific_evidence_basis r6_evidence_grade actual_first_non_test_consumer original_owner_route original_code_claim original_purpose original_next_proof_or_falsifier r6_author_head r6_atlas_git_blob r6_audit_git_blob exact_reversal_rule acceptance_ceiling".split(" ");
  ok(ledger.fields.join("\t")===expectedLedgerFields.join("\t"),"ledger contract drift");
  let changed=0,open=0,historical=0, illegal=0;
  const byProng={};
  for(let i=0;i<original.rows.length;i++){
    const before=original.rows[i],after=current.rows[i],id=before.record_id;
    ok(after.record_id===id,"atlas order/identity changed "+id);
    for(const f of original.fields) if(f!=="disposition")
      ok(before[f]===after[f],"nonstatus field drift "+id+" "+f);
    ok(ALLOWED.has(after.disposition),"noncanonical R7 disposition "+id);
    const wasIllegal=!ALLOWED.has(before.disposition), m=migrations.get(id), d=oldDebt.get(id);
    if(!wasIllegal){
      ok(!m&&!d&&before.disposition===after.disposition,"unreviewed canonical field changed "+id);
      continue;
    }
    changed++;
    ok(before.actual_consumer_ids==="NOT_PROVED_NON_TEST","unexpected verified first consumer "+id);
    ok(before.completeness_grade.startsWith("R5_RECEIVED_S0_S1"),"unexpected higher-grade source "+id);
    ok(before.source && before.pyat_owner_ids && before.next_step,"source/owner/falsifier blank "+id);
    ok(m&&d,"missing exact R6 audit/migration "+id);
    ok(d.namespace===before.namespace && d.source_locator===before.source &&
       d.inherited_r5_disposition===before.disposition &&
       d.r6_disposition===before.disposition &&
       d.r5_author_head==="cc21762ac3c7b49e389835b669a578d48caa1fc4" &&
       d.status==="R5_INHERITED_OUT_OF_VOCAB__R6_NOT_MODIFIED__SEPARATE_REVIEW_REQUIRED","R6 audit row drift "+id);
    ok(after.disposition===expectedStatus(before) &&
       m.r7_canonical_disposition===after.disposition &&
       m.row_specific_evidence_basis===historicalBasis(before),"unsupported canonical classification "+id);
    const expected = {
      namespace:before.namespace, r6_source_locator:before.source,
      r6_literal_disposition:before.disposition,
      r6_evidence_grade:before.completeness_grade,
      actual_first_non_test_consumer:before.actual_consumer_ids,
      original_owner_route:before.pyat_owner_ids,
      original_code_claim:before.current_code_and_sha,
      original_purpose:before.original_purpose,
      original_next_proof_or_falsifier:before.next_step,
      r6_author_head:R6, r6_atlas_git_blob:BLOBS.r6Atlas, r6_audit_git_blob:BLOBS.r6Audit,
      exact_reversal_rule:"RESTORE_ONLY_DISPOSITION_FROM_R6_LITERAL",
      acceptance_ceiling:"SOURCE_GRADED_S0_S1_ONLY__NO_CURRENT_FUNCTIONAL_OR_NATIVE_ACCEPTANCE"
    };
    for(const [f,v] of Object.entries(expected)) ok(m[f]===v,"migration provenance/reversibility loss "+id+" "+f);
    const prong=(id.match(/^J-F-(ZL\d+)-/)||[])[1];
    ok(prong&&EXPECTED_PRONG_COUNTS[prong],"unknown historical source prong "+id);
    byProng[prong]=(byProng[prong]||0)+1;
    if(after.disposition==="OPEN_PROOF_GAP")open++;
    else if(after.disposition==="HISTORICAL_HEURISTIC_ONLY")historical++;
    else ok(false,"evidence unsupported other status "+id);
  }
  ok(changed===655 && open===582 && historical===73 && illegal===0,"R7 status distribution/changed count");
  for(const [p,n] of Object.entries(EXPECTED_PRONG_COUNTS))ok(byProng[p]===n,"prong count "+p);
  for(const id of migrations.keys())ok(old.has(id)&&!ALLOWED.has(old.get(id).disposition),"extra migration "+id);
  for(const id of oldDebt.keys())ok(migrations.has(id),"unmigrated debt "+id);
  // Full exact reversal reconstructs the R6 atlas, including order and all nonstatus fields.
  const reconstructed=parse(x.r7Atlas,"reconstruction source");
  for(const row of reconstructed.rows)if(migrations.has(row.record_id))
    row.disposition=migrations.get(row.record_id).r6_literal_disposition;
  ok(serialize(reconstructed)===x.r6Atlas,"full exact R7→R6 reversal failed");
  // Previous evidence and seed-sidecar are frozen independently of classification.
  ok(x.relations===x.r6Relations && x.evidence===x.r6Evidence && x.seed===x.r6Seed && x.audit===x.r6Audit,
     "R6 relation/evidence/seed/audit mutated by R7");
  return {atlasRows:1740,changedCanonicalStatusCells:changed,openProofGap:open,historicalHeuristicOnly:historical,
          remainingIllegalDispositions:0,originalHistoricalLiteralsReversible:655,sourceProngs:byProng,
          nativeExecution:"NOT_RUN",scienceIssuerActorGrant:"NOT_GRANTED"};
}
function changedCell(s,pk,id,field,value) {
  const t=parse(s,"mutation"),r=t.rows.find(r=>r[pk]===id);
  ok(r&&field in r&&r[field]!==value,"hostile mutation would be no-op "+id+" "+field);
  r[field]=value;return serialize(t);
}
function hostile(x) {
  const l=parse(x.ledger,"hostile basis").rows;
  const open=l.find(r=>r.r7_canonical_disposition==="OPEN_PROOF_GAP").record_id,
        hist=l.find(r=>r.r7_canonical_disposition==="HISTORICAL_HEURISTIC_ONLY").record_id,
        frozen=parse(x.r6Atlas,"frozen");
  const seed=frozen.rows.find(r=>r.namespace==="LMX_INHERITED_OBLIGATION").record_id;
  const cases=[
    ["invented enum",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",open,"disposition","INVENTED__OPEN")],
    ["false proved successor",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",open,"disposition","PROVED_CURRENT_SUCCESSOR")],
    ["false partial",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",open,"disposition","PARTIAL_SUCCESSION")],
    ["historical source promoted current",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",hist,"disposition","PROVED_STRONGER_SUPERSESSION")],
    ["documentary index reclassified as open",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",hist,"disposition","OPEN_PROOF_GAP")],
    ["operational row mislabeled historical",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",open,"disposition","HISTORICAL_HEURISTIC_ONLY")],
    ["legacy illegal restored",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",open,"disposition",l.find(z=>z.record_id===open).r6_literal_disposition)],
    ["seed overwritten",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",seed,"disposition","PROVED_CURRENT_SUCCESSOR")],
    ["source forged",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",open,"source","FORGED_SOURCE")],
    ["owner forged",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",open,"pyat_owner_ids","RECEIVED")],
    ["first consumer forged",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",open,"actual_consumer_ids","PROVED_NON_TEST")],
    ["function meaning altered",y=>y.r7Atlas=changedCell(y.r7Atlas,"record_id",open,"function_statement","STOLEN_MEANING")],
    ["ledger original value falsified",y=>y.ledger=changedCell(y.ledger,"record_id",open,"r6_literal_disposition","FAKE_OLD_LITERAL")],
    ["ledger status falsified",y=>y.ledger=changedCell(y.ledger,"record_id",open,"r7_canonical_disposition","PROVED_CURRENT_SUCCESSOR")],
    ["ledger source falsified",y=>y.ledger=changedCell(y.ledger,"record_id",open,"r6_source_locator","FORGED")],
    ["ledger reason forged",y=>y.ledger=changedCell(y.ledger,"record_id",open,"row_specific_evidence_basis","FALSE_STATED_PROOF")],
    ["ledger owner falsified",y=>y.ledger=changedCell(y.ledger,"record_id",open,"original_owner_route","RECEIVED")],
    ["ledger falsifier erased",y=>y.ledger=changedCell(y.ledger,"record_id",open,"original_next_proof_or_falsifier","NONE")],
    ["ledger row dropped",y=>{let t=parse(y.ledger,"cut");t.rows.shift();y.ledger=serialize(t)}],
    ["ledger row duplicated",y=>{let t=parse(y.ledger,"dup");t.rows.push({...t.rows[0]});y.ledger=serialize(t)}],
    ["R6 source audit tampered",y=>y.audit=changedCell(y.audit,"record_id",open,"source_locator","FORGED_AUDIT")],
    ["negative relation overwritten",y=>y.relations+="\nFORGED_CURRENT_PROOF"],
    ["evidence report altered",y=>y.evidence+="\nFORGED_EVIDENCE"],
    ["seed classification changed",y=>y.seed+="\nFORGED_SEED"]
  ];
  let passes=0;
  for(const [name,mutate] of cases) {
    const y={...x}; mutate(y);
    let caught=false;try{verify(y)}catch(e){caught=true}
    ok(caught,"negative mutation escaped: "+name);passes++;
  }
  return passes;
}
if(require.main===module) {
  const root=cp.execFileSync("git",["rev-parse","--show-toplevel"],{encoding:"utf8"}).trim();
  const read=p=>fs.readFileSync(path.join(root,BASE+p),"utf8");
  const old=p=>cp.execFileSync("git",["show",R6+":"+BASE+p],{encoding:"utf8",maxBuffer:25*1024*1024});
  const x={
    r6Atlas:old("DATA/FUNCTION_ATLAS.tsv"), r7Atlas:read("DATA/FUNCTION_ATLAS.tsv"),
    ledger:read("PRONGS/J_JOIN/INHERITED_STATUS_CANONICAL_MIGRATION_R7.tsv"),
    audit:read("PRONGS/J_JOIN/INHERITED_NONCANONICAL_DISPOSITIONS_R6.tsv"),
    r6Audit:old("PRONGS/J_JOIN/INHERITED_NONCANONICAL_DISPOSITIONS_R6.tsv"),
    relations:read("DATA/RELATIONS.tsv"), r6Relations:old("DATA/RELATIONS.tsv"),
    evidence:read("DATA/EVIDENCE.tsv"), r6Evidence:old("DATA/EVIDENCE.tsv"),
    seed:read("PRONGS/J_JOIN/SEED_CURRENT_DISPOSITIONS_R5.tsv"), r6Seed:old("PRONGS/J_JOIN/SEED_CURRENT_DISPOSITIONS_R5.tsv")
  };
  for(const [name,content] of Object.entries({r6Atlas:x.r6Atlas,r7Atlas:x.r7Atlas,r7Ledger:x.ledger,r6Audit:x.audit,relations:x.relations,evidence:x.evidence,seeds:x.seed}))
    ok(blobHash(content)===BLOBS[name],"exact Git blob mismatch "+name);
  const summary=verify(x),rejects=hostile(x);
  console.log(JSON.stringify({court:"ZL15_R7_S0_S1_DOCUMENTARY_ONLY",...summary,hostileMutationsRejected:rejects,
    nodeCli:"EXECUTED",projectS2_S3:"NOT_RUN",original35:"NOT_RUN"},null,2));
}
module.exports={verify,hostile,historicalBasis,expectedStatus};
