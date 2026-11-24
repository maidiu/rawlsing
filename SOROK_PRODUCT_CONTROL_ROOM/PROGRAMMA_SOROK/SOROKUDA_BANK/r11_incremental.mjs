/** One SOURCE-LOCKED incremental intake inside the existing bank, not a second owner. */
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const root=path.dirname(fileURLToPath(import.meta.url));
const read=x=>JSON.parse(fs.readFileSync(path.join(root,x),"utf8"));
export function incrementalRows(){
  const source=read("inputs/NEIGHBOR_R9_CROSS_LINEAGE_104.json");
  const code=read("inputs/SORACLE_R30_TWO_SOURCE_IDENTITIES.json");
  const rows=source.rows;
  if(!Array.isArray(rows)||rows.length!==104||!Array.isArray(code.entries)||
    code.entries.length!==2)throw Error("R11_SOURCE_INTAKE_NOT_104_PLUS_2");
  const C=rows.filter(x=>/^C\d\d$/.test(x.id));
  const NM=rows.filter(x=>/^NM-\d{3}$/.test(x.id));
  const R=rows.filter(x=>/^R9-\d\d$/.test(x.id));
  if(C.length!==44||NM.length!==44||R.length!==16||
    new Set(rows.map(x=>x.id)).size!==104)throw Error("R11_SOURCE_LINEAGE_MISMATCH");
  const old=fs.readFileSync(path.join(root,"ALL_NORMALIZED.jsonl"),"utf8")
    .trimEnd().split("\n").map(JSON.parse);
  if(old.length!==1003)throw Error("R11_BASE_NOT_1003");
  const ids=new Set(old.map(x=>x.id));
  if(NM.some(x=>!ids.has(x.id)))throw Error("R11_PREVIOUS_NM_ID_MISSING");
  const item=(id,bank,artifact_type,description,url,cut,origin,consumer=null)=>({
    id,bank,artifact_type,title:description,
    source:{url,exact_ref:cut,origin},
    dates:{first_produced_on:null,selected_version_observed_at:null},
    meaning:{description},
    function:{owner_ids:[],first_consumer_text:consumer},
    integration:{state:"R11_SOURCE_LOCKED_INCREMENTAL_NOT_YET_FULLY_MATERIALIZED",do_not_infer_absence:true},
    evidence:{source_grade:"EXACT_PINNED_SOURCE_NOT_INDEPENDENT_G5",
      native_science_authority:"NOT_GRANTED_BY_INDEX",actor_authority:"NOT_GRANTED_BY_INDEX"}});
  const ideas=[...C,...R].map(x=>{
    const id=x.id.startsWith("C")?"NEIGHBOR-R8-"+x.id:"NEIGHBOR-"+x.id;
    const r=item(id,"ideas",x.id.startsWith("C")?"prior_neighbor_r8_conversation_proposition":
      "neighbor_r9_conversation_proposition",x.proposition,
      "https://github.com/maidiu/rawlsing/blob/3ac178f0b3b24ca4d4fe0f5d08b9f2100a8623a2/SEAM/NEIGHBORMULCH/SOROK_TOTAL_MULCH/11_CROSS_LINEAGE_CONVERSATION_NO_DROP_UNION.json",
      "3ac178f0b3b24ca4d4fe0f5d08b9f2100a8623a2",x.source);
    r.meaning.origin_fidelity=x.source;r.meaning.r9_disposition=x.r9_disposition??null;
    r.original_record=x;return r;});
  const codes=code.entries.map(x=>{
    const r=item(x.id,"code",x.kind,x.description,
      "https://github.com/maidiu/rawlsing/blob/"+code.code_head+"/"+x.path,
      code.code_head,"SORACLE_R30_SOURCE_BLOB",x.first_consumer);
    r.source.blob=x.blob;r.source.path=x.path;r.original_record=x;
    r.evidence.source_grade=code.grade;return r;});
  const delta=[...ideas,...codes];
  if(delta.length!==62||delta.some(x=>ids.has(x.id))||
    new Set(delta.map(x=>x.id)).size!==62)throw Error("R11_DOUBLE_COUNT_HOLD");
  return delta;
}