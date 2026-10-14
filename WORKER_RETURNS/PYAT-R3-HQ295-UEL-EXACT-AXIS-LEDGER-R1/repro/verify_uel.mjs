// Standalone source-free verifier; NOT_EXECUTED as Node in this worker.
import fs from "node:fs";
const copy=x=>JSON.parse(JSON.stringify(x));
c=>[...c.axes_source_native.map(x=>({kind:"SOURCE_NATIVE",id:x.id,key:"S:"+x.id})),...c.axes_EE01_EE16.map(id=>({kind:"EE",id,key:"EE:"+id})),...c.axes_F1_F8.map(x=>({kind:"F",id:x.id,key:"F:"+x.id}))]
function count(xs){const m=new Map();for(const x of xs)m.set(x,(m.get(x)||0)+1);return m}
function antijoin(a,b){
 const x=count(a),y=count(b),missing=[],extra=[];
 for(const [k,v] of x)if(v>(y.get(k)||0))missing.push({key:k,n:v-(y.get(k)||0)});
 for(const [k,v] of y)if(v>(x.get(k)||0))extra.push({key:k,n:v-(x.get(k)||0)});
 return {missing,extra};
}
function verify(c,o,h,n,l){
 const errors=[],fail=x=>{if(!errors.includes(x))errors.push(x)};
 const axes=getAxes(c),axisKeys=axes.map(x=>x.key),waveIds=c.sources.map(s=>s.id);
 const required=waveIds.flatMap(w=>axisKeys.map(a=>w+"|"+a));
 if(axisKeys.length!==54||new Set(axisKeys).size!==54)fail("CANONICAL_AXES_NOT_UNIQUE_54");
 if(c.sources.length!==35||new Set(waveIds).size!==35)fail("CANONICAL_SOURCES_NOT_UNIQUE_35");
 if(l.schema!=="PYAT_R3_HQ295_UEL_CANONICAL_AXIS_LEDGER@2.0.0")fail("SCHEMA_WRONG");
 if(!Array.isArray(l.waves))return {ok:false,errors:["NO_WAVES"]};
 const srcIds=l.waves.map(x=>x.source_id),sourceJoin=antijoin(waveIds,srcIds);
 if(srcIds.length!==35||sourceJoin.missing.length||sourceJoin.extra.length)fail("SOURCE_ID_MISSING_DUPLICATE_OR_INVENTED");
 const cBy=new Map(c.sources.map(x=>[x.id,x])),oBy=new Map(o.coverage_conservation.wave_rows.map(x=>[x.source_id,x])),actual=[];
 for(const row of l.waves){
  const s=cBy.get(row.source_id),p=oBy.get(row.source_id);
  if(!s||!p){fail("UNKNOWN_WAVE");continue}
  if(row.source_name!==s.name||row.source_name!==p.source_name)fail("WAVE_NAME_SWAP");
  const meta=Object.fromEntries(Object.entries(s).filter(([k])=>!["source_native_axes","empirical_engine_axes","f1_f8_axes"].includes(k)));
  if(JSON.stringify(meta)!==JSON.stringify(row.canonical_source_metadata))fail("SOURCE_METADATA_CHANGED");
  const nonaxis=Object.fromEntries(Object.entries(p).filter(([k])=>k!=="axis_identities"));
  if(JSON.stringify(nonaxis)!==JSON.stringify(row.E01_nonaxis_status))fail("E01_UNRESOLVED_STATUS_OR_CUSTODY_LOST");
  if(row.E01_repeated_EE_undefined_slots!==16)fail("HISTORICAL_DEFECT_DISGUISED");
  if(!Array.isArray(row.cells)){fail("MISSING_CELLS");continue}
  if(row.cells.length!==54)fail("PER_WAVE_AXIS_COUNT_NOT_54");
  const byKind={SOURCE_NATIVE:new Map(s.source_native_axes.map(x=>[x.id,x])),EE:new Map(s.empirical_engine_axes.map(x=>[x.id,x])),F:new Map(s.f1_f8_axes.map(x=>[x.id,x]))};
  for(const cell of row.cells){
   actual.push(cell.key);
   if(cell.key!==cell.source_id+"|"+cell.axis_key||cell.source_id!==row.source_id)fail("KEY_SOURCE_MISMATCH");
   if(!axes.some(a=>a.kind===cell.axis_kind&&a.id===cell.axis_id&&a.key===cell.axis_key))fail("MISSING_INVENTED_OR_SUBSTITUTED_AXIS");
   if(JSON.stringify(byKind[cell.axis_kind]?.get(cell.axis_id))!==JSON.stringify(cell.canonical_record))fail("CANONICAL_PER_AXIS_STATUS_OR_RECORD_MUTATED");
   if(cell.axis_key.includes("undefined"))fail("UNDEFINED_AXIS_SURVIVED");
  }
 }
 const j=antijoin(required,actual);
 if(j.missing.length)fail("CANONICAL_TO_LEDGER_MISSING");
 if(j.extra.length)fail("LEDGER_TO_CANONICAL_EXTRA_OR_DUPLICATE");
 if(actual.length!==1890||new Set(actual).size!==1890)fail("NOT_1890_UNIQUE_KEYS");
 if(JSON.stringify(l.definitions)!==JSON.stringify({source_native:c.axes_source_native,EE:c.axes_EE01_EE16,F:c.axes_F1_F8}))fail("AXIS_DEFINITIONS_CHANGED");
 if(JSON.stringify(l.global_relations)!==JSON.stringify(c.global_relation_obligations)||JSON.stringify(l.canonical_manifest_ontology)!==JSON.stringify(c.manifest_ontology))fail("GLOBAL_F6_F7_F8_SCOPE_CHANGED");
 const m=l.mapping_151_to_101;
 if(!m||antijoin(h.tasks.map(x=>x.id),m.historical_ids||[]).missing.length||antijoin(h.tasks.map(x=>x.id),m.historical_ids||[]).extra.length||antijoin(n.task_rows.map(x=>x.id),m.normalized_ids||[]).missing.length||antijoin(n.task_rows.map(x=>x.id),m.normalized_ids||[]).extra.length||m.historical_unresolved?.length!==151||m.normalized_unresolved?.length!==101)fail("151_TO_101_CLASSES_LOST");
 if(m?.new_accepted_edges!==0||m?.historical_unresolved?.some(x=>x.normalized_ids!==null)||m?.normalized_unresolved?.some(x=>x.historical_ids!==null))fail("151_TO_101_MAPPING_FABRICATED");
 if(l.authorization?.E_pre_issued!==false||l.authorization?.science_issued!==false||l.authorization?.new_source_read!==false)fail("SCIENTIFIC_SELF_ISSUANCE");
 return {ok:errors.length===0,errors,anti_join:{missing:j.missing.slice(0,6),extra:j.extra.slice(0,6),missing_count:j.missing.reduce((v,x)=>v+x.n,0),extra_count:j.extra.reduce((v,x)=>v+x.n,0),source_missing_count:sourceJoin.missing.length,source_extra_count:sourceJoin.extra.length},counts:{waves:srcIds.length,cells:actual.length,unique:new Set(actual).size,S:actual.filter(x=>x.includes("|S:")).length,EE:actual.filter(x=>x.includes("|EE:")).length,F:actual.filter(x=>x.includes("|F:")).length}};
}
if(process.argv.length!==7){console.error("node verify_uel.mjs canonical.json E01.json historical151.json normalized101.json successor.json");process.exit(2);}
const [c,o,h,n,l]=process.argv.slice(2).map(x=>JSON.parse(fs.readFileSync(x,"utf8")));
const r=verify(c,o,h,n,l);console.log(JSON.stringify(r,null,2));process.exit(r.ok?0:1);
