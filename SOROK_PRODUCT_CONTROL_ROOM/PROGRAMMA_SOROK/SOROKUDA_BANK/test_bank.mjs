import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {spawnSync} from "node:child_process";
import {normalize,documentIndex,parse44,validateBank,versionClock} from "./normalizer.mjs";

const root=path.dirname(fileURLToPath(import.meta.url));
const base=path.resolve(root,"../../..");
const read=(name)=>fs.readFileSync(path.join(root,name),"utf8");
const j=(name)=>JSON.parse(read(name));
const jl=(name)=>read(name).split("\n").filter(Boolean).map(JSON.parse);
const code=fs.readFileSync(path.join(base,"SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/SOROKUDA_CODE_INDEX.jsonl"),"utf8").split("\n").filter(Boolean).map(JSON.parse);
const union=j("inputs/NEIGHBOR_SOURCE_UNION_757.json"), thematic=j("inputs/NEIGHBOR_THEMATIC_757.json"),
 ideas=read("inputs/NEIGHBOR_USER_IDEAS_44.md"), co=j("inputs/SORACLE_CO_R27_16.json"),
 locator=j("inputs/NEIGHBOR_CURATED_SOURCE_LOCATOR.json"),dates=j("VERIFIED_COMMIT_AUTHOR_DATES.json").dates;
const records=jl("ALL_NORMALIZED.jsonl");
const docs=jl("DOCUMENT_LOCATOR_252.jsonl");
const of=(id)=>records.find(x=>x.id===id);

test("all source identities and 300 previous SOROKUDA code identities conserved",()=>{
 assert.deepEqual(validateBank(records,docs,code,union),{
  total:1003,concepts:373,functions:144,code:486,files:227,directories:25,
  dated_version:689,first_production_verified:0,first_path_committed_verified:117,prior_300_preserved:300
 });
 assert.equal(code.length,486);
 assert.equal(new Set(records.map(x=>x.id)).size,1003);
 for(const old of union.sorokuda_source_and_alternative_versions){
  const current=code.find(x=>x.id===old.id);
  assert.ok(current,old.id);
  if((old.path??old.source_path)&&(current.path??current.source_path))assert.equal(old.path??old.source_path,current.path??current.source_path);
  if((old.blob??old.git_blob??old.source_blob)&&(current.blob??current.git_blob??current.source_blob))assert.equal(old.blob??old.git_blob??old.source_blob,current.blob??current.git_blob??current.source_blob);
 }
});
test("regeneration from exact inputs is byte for byte deterministic",()=>{
 const fresh=normalize(union,thematic,code,ideas,co,dates);
 assert.equal(fresh.map(JSON.stringify).join("\n")+"\n",read("ALL_NORMALIZED.jsonl"));
 assert.equal(documentIndex(locator).map(JSON.stringify).join("\n")+"\n",read("DOCUMENT_LOCATOR_252.jsonl"));
 for(const [bank,file,n] of [["ideas","IDEAS.jsonl",373],["functions","FUNCTIONS.jsonl",144],["code","CODE_AND_EVIDENCE.jsonl",486]]){
  assert.equal(records.filter(r=>r.bank===bank).length,n);
  assert.equal(read(file),records.filter(x=>x.bank===bank).map(JSON.stringify).join("\n")+"\n");
 }
});
test("44 new ideas retain direct user versus reconstructed history",()=>{
 const rows=parse44(ideas);
 assert.equal(rows.length,44);
 for(let i=1;i<=44;i++){
  const id="NM-"+String(i).padStart(3,"0"),r=of(id);
  assert.ok(r,id);
  assert.equal(r.meaning.origin_fidelity,i<=16?"User, latest exact":"Earlier, banked");
  assert.equal(r.source.blob,"399ce39e54204b4ef907f580ecf14d4174af7fa6");
 }
 assert.match(of("NM-030").meaning.description,/Shared root/);
 assert.match(of("NM-004").meaning.description,/Family patterns/);
});
test("original workstreams embedded within 144, not 17 new functions",()=>{
 assert.equal(union.original_workstreams_S0_S16.length,17);
 assert.equal(records.filter(x=>x.bank==="functions").length,144);
 for(const w of union.original_workstreams_S0_S16)assert.ok(of(w.id),w.id);
});
test("original code and reviewer proof do not become native science",()=>{
 const active=of("SOROKUDA-ORG-001"),review=of("SOROKUDA-R8-B15"),pointer=of("SOROKUDA-294-A001");
 assert.equal(active.integration.state,"ACTIVE_CANDIDATE__PROTECTED_RECEIVING_HELD");
 assert.equal(review.artifact_type,"review_or_return_document");
 assert.equal(pointer.artifact_type,"historical_source_pointer");
 assert.equal(pointer.integration.state,"HISTORICAL_POINTER__STRANDED_NOT_PROVEN");
 for(const x of [active,review,pointer]){
  assert.equal(x.integration.do_not_infer_absence,true);
  assert.equal(x.evidence.native_science_authority,"NOT_GRANTED_BY_INDEX");
 }
});
test("time stamps are not fake first-production dates",()=>{
 const entry=of("SOROKUDA-ORG-001");
 assert.equal(entry.dates.selected_version_observed_at,"2026-11-21T08:10:14Z");
 assert.equal(entry.dates.first_produced_on,null);
 assert.equal(entry.dates.first_path_committed_on,"2026-11-21T06:51:50Z");
 assert.equal(records.filter(r=>r.dates.first_path_committed_on).length,117);
 assert.equal(versionClock("unverified",dates,"some_20261121_name",null).first_produced_on,null);
});
test("source mutation fail closed; no new false artifact can disappear silently",()=>{
 const cut=structuredClone(code);
 cut[0].blob="0".repeat(40);
 assert.throws(()=>normalize(union,thematic,cut,ideas,co,dates),/Changed prior source/);
 assert.throws(()=>normalize(union,thematic,code.slice(1),ideas,co,dates),/(SOROKUDA .*no-drop|Prior 300 missing)/);
});

test("R11 incremental source is queryable without duplicating 44 NM rows",()=>{
 const source=j("inputs/NEIGHBOR_R9_CROSS_LINEAGE_104.json");
 assert.equal(source.rows.length,104);
 assert.equal(source.rows.filter(x=>/^NM-\d{3}$/.test(x.id)).length,44);
 for(const r of source.rows.filter(x=>/^NM-\d{3}$/.test(x.id)))assert.ok(of(r.id),r.id);
 const p=spawnSync(process.execPath,[path.join(root,"bank_cli.mjs"),"coverage"],{encoding:"utf8"});
 assert.equal(p.status,0,p.stderr);
 const counts=JSON.parse(p.stdout).counts;
 assert.deepEqual([counts.all,counts.materialized_base,counts.incremental_source_overlay],[1065,1003,62]);
 const g=spawnSync(process.execPath,[path.join(root,"bank_cli.mjs"),"gate-new","mistaken Other"],{encoding:"utf8"});
 assert.equal(g.status,0,g.stderr);
 assert.match(g.stdout,/NO_BUILD_RIGHT_ISSUED/);
 assert.match(g.stdout,/SOROKUDA-R11-R30-OWNER/);
 const s=spawnSync(process.execPath,[path.join(root,"bank_cli.mjs"),"show","NEIGHBOR-R9-01"],{encoding:"utf8"});
 assert.equal(s.status,0,s.stderr);
 assert.equal(JSON.parse(s.stdout).meaning.origin_fidelity,"DIRECT_USER");
});

test("CLI check and no-new-owner gate execute",()=>{
 const check=spawnSync(process.execPath,[path.join(root,"bank_cli.mjs"),"check"],{encoding:"utf8"});
 assert.equal(check.status,0,check.stderr);
 const ask=spawnSync(process.execPath,[path.join(root,"bank_cli.mjs"),"gate-new","Birkenstocks"],{encoding:"utf8"});
 assert.equal(ask.status,0,ask.stderr);
 assert.match(ask.stdout,/NO_BUILD_RIGHT_ISSUED/);
 assert.match(ask.stdout,/SOROKUDA_BANK_HOLD|SOROKUDA|NM-030/);
 const missing=spawnSync(process.execPath,[path.join(root,"bank_cli.mjs"),"gate-new","neverbuiltxyzq"],{encoding:"utf8"});
 assert.equal(missing.status,0,missing.stderr);
 assert.match(missing.stdout,/UNKNOWN_NOT_MISSING/);
});
