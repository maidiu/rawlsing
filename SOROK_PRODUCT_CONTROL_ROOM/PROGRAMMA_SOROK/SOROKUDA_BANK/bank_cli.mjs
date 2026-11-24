#!/usr/bin/env node
/**
 * SOROKUDA BANK — derived navigation, never a sovereign PROGRAMMA.
 * All records come from pinned originals; zero results never prove novelty.
 * Requires Node 20+; stdlib only; no network on build/check/search.
 */
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {spawnSync} from "node:child_process";
import {createHash} from "node:crypto";
import {normalize,documentIndex,validateBank} from "./normalizer.mjs";

const here=path.dirname(fileURLToPath(import.meta.url));
const repo=path.resolve(here,"../../..");
const folder=(p)=>path.join(here,p);
const read=(p)=>fs.readFileSync(folder(p),"utf8");
const json=(p)=>JSON.parse(read(p));
const jsonl=(p)=>read(p).split("\n").filter(Boolean).map(JSON.parse);
const serialize=(x)=>x.map(r=>JSON.stringify(r)).join("\n")+"\n";
const inputs={
  union:"inputs/NEIGHBOR_SOURCE_UNION_757.json",
  theme:"inputs/NEIGHBOR_THEMATIC_757.json",
  ideas:"inputs/NEIGHBOR_USER_IDEAS_44.md",
  co:"inputs/SORACLE_CO_R27_16.json",
  locator:"inputs/NEIGHBOR_CURATED_SOURCE_LOCATOR.json",
  r9:"inputs/NEIGHBOR_R9_CROSS_LINEAGE_104.json"
};
const recordsPath="ALL_NORMALIZED.jsonl";
const views=[["ideas","IDEAS.jsonl"],["functions","FUNCTIONS.jsonl"],["code","CODE_AND_EVIDENCE.jsonl"]];
const codeIndex=path.join(repo,"SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/SOROKUDA_CODE_INDEX.jsonl");
function gitBlob(bytes){const b=Buffer.isBuffer(bytes)?bytes:Buffer.from(bytes,"utf8");return createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex");}
function checkLocks(){
 const lock=json("SOURCE_LOCK.json");
 for(const [relative,sha] of Object.entries(lock.pinned_files)){
  const file=path.resolve(repo,relative);
  if(!file.startsWith(repo+path.sep) || !fs.existsSync(file))throw Error("PINNED_SOURCE_MISSING: "+relative);
  if(gitBlob(fs.readFileSync(file))!==sha)throw Error("PINNED_SOURCE_DRIFT_HOLD: "+relative+" original "+sha);
 }
 for(const [name,sha] of Object.entries(lock.materialized_outputs)){
  const file=folder(name);
  if(!fs.existsSync(file)||gitBlob(fs.readFileSync(file))!==sha)throw Error("MATERIALIZED_BANK_DRIFT_HOLD: "+name);
 }
 return lock;
}
function sourceInputs(){
 checkLocks();
 if(!fs.existsSync(codeIndex))throw Error("Original SOROKUDA_CODE_INDEX.jsonl missing; refuse stand-in");
 return {
   union:json(inputs.union),theme:json(inputs.theme),ideas:read(inputs.ideas),
   co:json(inputs.co),locator:json(inputs.locator),r9:json(inputs.r9),
   code:fs.readFileSync(codeIndex,"utf8").split("\n").filter(Boolean).map(JSON.parse),
   dates:json("VERIFIED_COMMIT_AUTHOR_DATES.json").dates
 };
}
function build(write){
 const i=sourceInputs();
 const r=normalize(i.union,i.theme,i.code,i.ideas,i.co,i.dates,i.r9);
 const documents=documentIndex(i.locator);
 const result=validateBank(r,documents,i.code,i.union);
 const artifacts=[[recordsPath,serialize(r)],["DOCUMENT_LOCATOR_252.jsonl",serialize(documents)],
    ...views.map(([bank,name])=>[name,serialize(r.filter(row=>row.bank===bank))])];
 for(const [name,body] of artifacts){
   if(write)fs.writeFileSync(folder(name),body,"utf8");
   else if(!fs.existsSync(folder(name)) || read(name)!==body)throw Error("STALE_BANK: "+name+" does not equal its pinned sources; do not silently use");
 }
 const all=jsonl(recordsPath);
 if(all.length!==577+i.code.length || new Set(all.map(r=>r.id)).size!==all.length)throw Error("MATERIALIZED_MISMATCH");
 return result;
}
function clockSummary(){
 const r=jsonl(recordsPath),o={verified_version_observation:0,source_history_first_production:0,unverified:0};
 for(const row of r){
  if(row.dates.selected_version_observed_at)o.verified_version_observation++;
  else o.unverified++;
  if(row.dates.first_produced_on)o.source_history_first_production++;
 }
 return o;
}
function tokenize(s){
 return [...new Set(String(s??"").toLowerCase().replace(/<[^>]*>/g," ").match(/[a-z0-9_-]{3,}/g)??[])];
}
function search(q,limit=20,bank=null){
 const words=tokenize(q);
 if(words.length===0)throw Error("Nonempty search query required");
 const records=jsonl(recordsPath);
 const ranked=[];
 for(const r of records){
  if(bank&&r.bank!==bank)continue;
  const main=(r.title+" "+(r.meaning.description??"")+" "+(r.meaning.user_delta??"")+" "+(r.meaning.original_question??"")).toLowerCase();
  const sec=(JSON.stringify([r.function.owner_ids,r.function.first_consumer_text,r.function.functional_cluster,r.meaning.theme,r.meaning.antecedent_text,r.meaning.first_mulch_falsifier,r.meaning.existing_owner])??"").toLowerCase();
  let score=0;if(main.includes(q.toLowerCase()))score+=15;
  for(const w of words){if(main.includes(w))score+=4;if(sec.includes(w))score+=1;}
  if(score>0)ranked.push({record:r,score});
 }
 ranked.sort((a,b)=>b.score-a.score||a.record.id.localeCompare(b.record.id));
 return ranked.slice(0,limit);
}
function printSearch(q,limit=20,bank=null){
 const hits=search(q,limit,bank);
 console.log(JSON.stringify({query:q,bank,found:hits.length,absence_inference:"PROHIBITED",meaning:"Search finds evidence leads, not owner parity or complete proof. If none: UNKNOWN, never MISSING.",hits:hits.map(x=>({
 id:x.record.id,bank:x.record.bank,kind:x.record.artifact_type,score:x.score,
 title:x.record.title,implementation:x.record.integration.state,
 source:x.record.source.url,source_cut:x.record.source.exact_ref,
 selected_version_observed_at:x.record.dates.selected_version_observed_at,
 first_production:x.record.dates.first_produced_on,
 first_consumer:x.record.function.first_consumer_text,
 evidence:x.record.evidence.source_grade
 }))},null,2));
}
function git(args){
 const p=spawnSync("git",args,{cwd:repo,encoding:"utf8",timeout:15000});
 if(p.error||p.status!==0)return null;
 return p.stdout.trim();
}
function enrichDates(max){
 const r=jsonl(recordsPath).filter(x=>x.bank==="code"&&x.source.path&&x.source.exact_ref);
 const newDates=[];let considered=0;
 for(const item of r){
  if(considered>=max)break;considered++;
  const sha=item.source.exact_ref,p=item.source.path;
  const have=git(["cat-file","-t",sha]);
  if(have!=="commit"){
    newDates.push({id:item.id,path:p,source_commit:sha,first_path_production:null,last_path_change:null,status:"SOURCE_COMMIT_NOT_AVAILABLE_IN_LOCAL_GIT"});continue;
  }
  const introduced=git(["log","--follow","--diff-filter=A","--reverse","--format=%aI|%H",sha,"--",p]);
  const last=git(["log","-1","--format=%aI|%H",sha,"--",p]);
  const firstLine=introduced?.split("\n").filter(Boolean)[0]??null;
  newDates.push({id:item.id,path:p,source_commit:sha,
    first_path_production:firstLine?.split("|")[0]??null,
    introduced_commit:firstLine?.split("|")[1]??null,
    last_path_change:last?.split("|")[0]??null,
    last_changed_commit:last?.split("|")[1]??null,
    status:firstLine?"VERIFIED_LOCAL_GIT_PATH_INTRODUCTION_WITHIN_SOURCE_ANCESTRY":"FIRST_PATH_INTRODUCTION_UNRESOLVED",
    caution:"First history-visible path addition at exact source ancestry; renames, sibling branches and conceptual prehistory may predate it."});
 }
 const output="DATE_ENRICHMENT_LOCAL.jsonl";
 fs.writeFileSync(folder(output),serialize(newDates));
 console.log(JSON.stringify({output,rows:newDates.length,first_path_proven:newDates.filter(x=>x.first_path_production).length,
   unresolved:newDates.filter(x=>!x.first_path_production).length,scope:"LOCAL_CHECKOUT_HISTORY_ONLY_NOT_ORIGINAL_CONCEPT_DATE"},null,2));
}
function main(argv){
 const [command,...rest]=argv;
 checkLocks();
 if(command==="build"||command==="check"){
   const result=build(command==="build");
   console.log(JSON.stringify({command,validated:result,clock:clockSummary(),status:command==="check"?"EXACT_INPUT_DERIVATION_VERIFIED":"BUILT_FROM_PINNED_INPUTS__NOT_PROTECTED_RECEIVED"},null,2));return;
 }
 if(command==="search"||command==="gate-new"){
   const b=rest.find(s=>s.startsWith("--bank="));const bank=b?b.slice(7):null;
   const query=rest.filter(s=>!s.startsWith("--")).join(" ");
   const hits=search(query,20,bank);
   if(command==="gate-new")console.log(JSON.stringify({decision:"NO_BUILD_RIGHT_ISSUED",match_count:hits.length,
     next: hits.length?"Read exact positive and negative source/first consumer before proposing a new owner":"UNKNOWN_NOT_MISSING__check_PROGRAMMA_O_Index_and_unindexed_live_returns_before_proposing_a_new_owner"}));
   printSearch(query,20,bank);return;
 }
 if(command==="show"){
   const all=jsonl(recordsPath),r=all.find(x=>x.id===rest[0]);if(!r)throw Error("UNKNOWN_ID_NOT_PROOF_OF_ABSENCE");
   console.log(JSON.stringify(r,null,2));return;
 }
 if(command==="coverage"){const r=jsonl(recordsPath),counts={all:r.length,ideas:r.filter(x=>x.bank==="ideas").length,functions:r.filter(x=>x.bank==="functions").length,code:r.filter(x=>x.bank==="code").length,materialized_base:r.length,incremental_source_overlay:0,document_locators:227,directory_entrances:25}; console.log(JSON.stringify({counts,dates:clockSummary(),
   gap:"Not exhaustive every idea in every Git branch/chat; only exact 757+182+44+16 source collection; individual current owner/first-reader adjudication incomplete."},null,2));return}
 if(command==="enrich-dates"){
    const v=rest.find(x=>x.startsWith("--limit=")),max=v?Number(v.slice(8)):30;
    const maximum=jsonl(recordsPath).filter(x=>x.bank==="code").length;
    if(!Number.isInteger(max)||max<1||max>maximum)throw Error("--limit must be integer 1.."+maximum);
    enrichDates(max);return;
 }
 throw Error("Usage: node bank_cli.mjs check|build|search TERMS [--bank=ideas|code|functions]|show ID|gate-new TERMS|coverage|enrich-dates [--limit=N]");
}
try{main(process.argv.slice(2))}catch(e){console.error("SOROKUDA_BANK_HOLD:",e.message);process.exitCode=1}
