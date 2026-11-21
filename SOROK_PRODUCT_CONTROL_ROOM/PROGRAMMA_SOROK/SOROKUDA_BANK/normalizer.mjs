// GENERATED SOURCE OF THE MATERIALIZED SOROKUDA BANK. Pure, deterministic, no external network.

// Run bank_cli.mjs build/check from the repository after inputs are checked out.

export function parse44(s){
 const lines=s.split("\n"),found=[];
 for(let i=0;i<lines.length;i++){const l=lines[i];if(!/^\| NM-\d{3} \|/.test(l))continue;let cells=l.split("|").slice(1,-1).map(x=>x.trim());if(cells.length!==5)throw Error("Malformed NM source table at "+(i+1));let [id,origin,claim,antecedent,status]=cells;found.push({id,origin,claim,antecedent,status,source_line:i+1})}
 if(found.length!==44||new Set(found.map(x=>x.id)).size!==44)throw Error("44 source ideas not exact");return found
}

export function refFromLink(u){const m=String(u??"").match(/\/blob\/([a-f0-9]{40})\//);return m?m[1]:null}

export function sourceDateHint(s){const m=String(s??"").match(/(?:^|[^0-9])(20(?:2[0-9]))[._/-]?(0[1-9]|1[012])[._/-]?([012][0-9]|3[01])(?:[^0-9]|$)/);if(!m)return null;return `${m[1]}-${m[2]}-${m[3]}`}

export function versionClock(ref,dateCache,contextHint,bankedOn){
 const verified=ref&&dateCache[ref]?dateCache[ref]:null;
 return {first_produced_on:null,first_produced_grade:"UNKNOWN__PATH_HISTORY_NOT_EXECUTED",
  selected_version_observed_at:verified,selected_version_grade:verified?"GIT_AUTHOR_DATE_AT_EXACT_COMMIT__NOT_FIRST_PRODUCTION":"UNKNOWN_NO_COMMIT_TIMESTAMP_READ",
  unverified_reference_date_hint:sourceDateHint(contextHint),banked_on:bankedOn||"2026-11-21",
  note:"Commit timestamp proves selected source cut existed by that time; does not prove the first day the concept or file was created."}
}

export function codeArtifactKind(k,path){
 if(k==="HISTORICAL_IMPLEMENTER_POINTER_NOT_VALIDATED_STRANDED"||k==="CROSS_HQ_SOURCE_POINTER_NOT_NEW_FUNCTION")return "historical_source_pointer";
 if(k==="B67_ORIGINAL_INDEPENDENT_REVIEW_PRIMARY_RETURN"||k==="REPAIR_OR_REVIEW_SUCCESSION_SOURCE")return "review_or_return_document";
 if(/TEST_SOURCE|TEST_SUPPORT|HOSTILE_TEST_BODY|OPERATIONAL_TEST|REGRESSION_SOURCE|EXECUTABLE_TEST_OR_PROOF/.test(k))return "executable_test_or_proof";
 if(/VALIDATOR/.test(k))return "validator_or_utility_code";
 if(/CODE_MODULE|MODULE|SOURCE_BODY|CODE_BODY|OPERATIONAL_CODE/.test(k))return "runtime_or_operational_code";
 if(/DISTINCT_SOURCE_VERSION_OR_TEST/.test(k))return "historical_code_or_test_variant";
 if(/\.md$/i.test(path??""))return "review_or_return_document";
 return "mixed_code_or_evidence_unresolved"
}

export function codeStatus(k,r){
 if(k==="CODE_MODULE"||k==="TEST_SOURCE")return "ACTIVE_CANDIDATE__PROTECTED_RECEIVING_HELD";
 if(k==="PROTECTED_POST_CENSUS_CODE_BODY")return "PROTECTED_ARCHIVAL_SOURCEFREE__CURRENT_READER_NOT_INFERRED";
 if(k==="HISTORICAL_IMPLEMENTER_POINTER_NOT_VALIDATED_STRANDED")return "HISTORICAL_POINTER__STRANDED_NOT_PROVEN";
 if(k==="CROSS_HQ_SOURCE_POINTER_NOT_NEW_FUNCTION")return "CROSS_HQ_REFERENCE_ONLY__NOT_ADDITIONAL_FUNCTION";
 if(k==="B67_ORIGINAL_INDEPENDENT_REVIEW_PRIMARY_RETURN"||k==="REPAIR_OR_REVIEW_SUCCESSION_SOURCE")return "HISTORICAL_REVIEW_EVIDENCE__NOT_LIVE_VERDICT";
 if(/UNMERGED/.test(k))return "UNMERGED_SOURCE_CANDIDATE";
 if(/LEGACY_|POST_REWORK|SOURCE_BODY/.test(k))return "HISTORICAL_SOURCE_OR_VERSION__REUSE_UNRESOLVED";
 if(r.successor_disposition)return "HISTORICAL_WITH_SOURCE_PINNED_SUCCESSOR_DISPOSITION";
 return "SOURCE_PRESENT__CURRENT_INTEGRATION_NOT_ESTABLISHED"
}

export function normalize(union,theme,code,nm,co,dateCache){
 const originals=new Map(code.map(r=>[r.id,r]));
 if(code.length<300||new Set(code.map(x=>x.id)).size!==code.length)throw Error("SOROKUDA 482 no-drop failed");
 for(const old of union.sorokuda_source_and_alternative_versions){
   const now=originals.get(old.id);if(!now)throw Error("Prior 300 missing: "+old.id);
   const a=old.blob??old.git_blob??old.source_blob,b=now.blob??now.git_blob??now.source_blob;
   const ap=old.path??old.source_path,bp=now.path??now.source_path;
   if((a&&b&&a!==b)||(ap&&bp&&ap!==bp))throw Error("Changed prior source: "+old.id);
 }
 const hh=new Map((theme.H_original_ideation_first_pass??[]).map(x=>[x.source_id,x]));
 const qq=new Map((theme.Q_original_questions_first_pass??[]).map(x=>[x.source_id,x]));
 const out=[], push=r=>out.push(r);
 const skeleton=(id,bank,artifactType,title,raw,source,sourceCut,origin,claimEvidence,ownerIds=[],ownerGrade="UNKNOWN")=>({
   id,bank,artifact_type:artifactType,title,
   source:{path:source.path??null,blob:source.blob??null,exact_ref:sourceCut??null,url:source.url??null,origin:origin},
   dates:versionClock(sourceCut,dateCache,`${source.path??""} ${sourceCut??""}`,"2026-11-21"),
   meaning:{description:raw.claim??raw.original_question??raw.title??raw.name??raw.summary??raw.finding??title,
      source_claim_grade:claimEvidence,source_exact_text_available:Boolean(raw.claim||raw.original_question)},
   function:{owner_ids:ownerIds,owner_link_grade:ownerGrade,first_consumer_text:null,actual_current_reader_verified:false,
     producer_text:null,required_consumer_text:null},
   integration:{state:"UNRESOLVED",protected_received_at_exact_source:null,current_selected_consumer_ref:null,
     upstream_implementation_version:null,do_not_infer_absence:true},
   evidence:{source_grade:claimEvidence,reported_execution:null,reviewer_verdict:null,native_science_authority:"NOT_GRANTED_BY_INDEX",actor_authority:"NOT_GRANTED_BY_INDEX"},
   relationships:{historical_version_of:null,same_source_id_in_other_bank:null,mentions_only:[],explicit_replacement:null},
   original_record:raw
 });
 for(const r of union.original_function_and_source_registry){
   let x=skeleton(r.id,"functions","functional_contract",r.title,r,{path:r.source_evidence_path,blob:r.source_blob,url:`https://github.com/${"maidiu/rawlsing"}/blob/${r.source_commit}/${r.source_evidence_path}`},r.source_commit,"EXISTING_O_INDEX_144_ORIGINAL_NOT_NEW_OWNER","PINNED_HISTORICAL_OWNER_FUNCTION",[r.id],"EXACT_ORIGINAL_FUNCTION_ID");
   x.function.required_consumer_text=r.first_consumer_required??null;x.function.first_consumer_text=r.actual_consumer_state??null;x.integration.state="HISTORICAL_FUNCTION_STATUS__NOT_NATIVE_ACCEPTANCE";x.evidence.source_grade=r.engineering_grade??"HISTORICAL";x.evidence.review_grade=r.original_status??"HISTORICAL";x.evidence.original_science_grade=r.science_grade??null;x.evidence.original_authority_grade=r.authority_grade??null;
   push(x);
 }
 for(const r of union.original_ideation_H001_H190){
   let t=hh.get(r.id),cut=refFromLink(r.source_link);
   let x=skeleton(r.id,"ideas","original_historical_idea",r.claim,r,{path:null,blob:null,url:r.source_link},cut,"ORIGINAL_SOROK_IDEATION_H001_H190","ORIGINAL_CLAIM_AT_HISTORICAL_SOURCE",t?.home_owners??[],"THEMATIC_FIRST_PASS__NOT_CURRENT_FUNCTION_PARITY");
   x.meaning.theme=t?.theme??null;x.meaning.historical_disposition=r.original_disposition;
   x.meaning.first_mulch_falsifier=t?.first_mulch_falsifier??null;x.integration.state="BANKED_HISTORICAL_IDEA__CURRENT_OPERATION_UNKNOWN";
   push(x);
 }
 for(const r of union.original_product_questions_Q){
   const t=qq.get(r.id),cut=refFromLink(r.source_link);
   let x=skeleton(r.id,"ideas","original_product_question",r.original_question,r,{path:null,blob:null,url:r.source_link},cut,"ORIGINAL_SOROK_QUESTION_123","ORIGINAL_HISTORICAL_QUESTION",[r.workstream].filter(Boolean),"EXPLICIT_WORKSTREAM__NOT_IMPLEMENTATION");
   x.meaning.historical_closure=r.original_closure;x.meaning.stage=r.original_blocking_stage;x.meaning.first_mulch_approach=t?.first_mulch_approach??null;x.integration.state="HISTORICAL_QUESTION__CLOSURE_NOT_CURRENT_PROOF";push(x);
 }
 for(const r of code){
   const path=r.path??r.source_path??null,blob=r.blob??r.git_blob??r.source_blob??null,cut=r.source_cut??r.head??r.pinned_sha??null,k=r.kind;
   let title=path?path.split("/").at(-1):r.id;
   let x=skeleton(r.id,"code",codeArtifactKind(k,path),title,r,{path,blob,url:r.url??(path&&cut?`https://github.com/maidiu/rawlsing/blob/${cut}/${path}`:null)},cut,"SOROKUDA_CODE_INDEX_R9_EXACT_ID","EXACT_SOURCE_IDENTITY__FUNCTION_UNVERIFIED",[],"FUNCTIONAL_CLUSTER_OR_SOURCE_TEXT_ONLY");
   if(k==="CODE_MODULE"||k==="TEST_SOURCE"){
    const pi=dateCache.__path_intro?.[path];
    if(pi&&cut==="6647f746f4f7d2ae3dd0d14af5cde38191044773"){
      x.dates.first_path_committed_on=pi.date;
      x.dates.first_path_commit=pi.commit;
      x.dates.first_path_grade=pi.evidence;
    }
   }
   x.meaning.original_kind=k;x.meaning.description=r.summary??r.finding??r.functional_delta??r.note??r.limits??title;
   x.function.first_consumer_text=r.first_reader??r.first_consumer??r.real_first_reader_family??r.first_consumer_reported??null;
   x.function.producer_text=r.function_name??null;x.function.functional_cluster=r.functional_cluster??r.family??null;
   x.integration.state=codeStatus(k,r);x.integration.upstream_implementation_version=cut;
   if(r.successor_disposition)x.integration.successor_disposition=r.successor_disposition;
   x.evidence.source_grade=r.source_read_grade??r.read_grade??r.source_grade??r.verified??"EXACT_CODE_INDEX_ENTRY_UNREVIEWED";
   x.evidence.reported_execution=r.historical_test_status??r.evidence??r.historical_verdict??null;
   x.evidence.reviewer_verdict=r.historical_verdict??null;
   x.evidence.original_protected_grade=r.protected_receiving??null;
   if(union.sorokuda_source_and_alternative_versions.find(y=>y.id===r.id))x.relationships.same_source_id_in_other_bank="NEIGHBORMULCH_TOTAL_757";
   push(x);
 }
 for(const r of parse44(nm)){
   let x=skeleton(r.id,"ideas","user_product_idea_or_falsifier",r.claim,r,{path:"SEAM/NEIGHBORMULCH/SOROK_TOTAL_MULCH/04_USER_CONVERSATION_NO_DROP_AND_NEW_IDEAS.md",blob:"399ce39e54204b4ef907f580ecf14d4174af7fa6",url:`https://github.com/maidiu/rawlsing/blob/be7b32911f3467c870f18887a3d5b0e7a88952dd/SEAM/NEIGHBORMULCH/SOROK_TOTAL_MULCH/04_USER_CONVERSATION_NO_DROP_AND_NEW_IDEAS.md#L${r.source_line}`},"be7b32911f3467c870f18887a3d5b0e7a88952dd","LATE_USER_IDEA_44_SOURCE_BANKEDED","USER_ORIGIN_DISTINCTION_IN_SOURCE",[],"ANTECEDENT_TEXT__NOT_OWNER_VERIFICATION");
   x.meaning.origin_fidelity=r.origin;x.meaning.antecedent_text=r.antecedent;x.meaning.recorded_status=r.status;x.meaning.source_line=r.source_line;
   x.integration.state="USER_IDEA_BANKED__IMPLEMENTATION_STATUS_AS_ORIGINALLY_REPORTED";push(x);
 }
 for(const r of co.rows){
   let x=skeleton(r.id,"ideas","soracle_co_integration_idea",r.name,r,{path:"SEAM/ORACLE/UM_SOROK_ORGANISM_R3/docs/R27_MULCHINEERING_ONE_PER_INTRODUCTION_20261121.json",blob:"b3425bf3399bfca716bc737c64d9d2eea6d7eb86",url:"https://github.com/maidiu/rawlsing/blob/d682db603f4c2916d68cfe30334e1ca539190bb5/SEAM/ORACLE/UM_SOROK_ORGANISM_R3/docs/R27_MULCHINEERING_ONE_PER_INTRODUCTION_20261121.json"},"d682db603f4c2916d68cfe30334e1ca539190bb5","SORACLE_CO_R27_SOURCEFREE_CANDIDATE","R27_REQUIREMENT_ORIGIN",[],"OWNER_PROSE__NOT_VERIFIED_ACTUAL_READER");
   x.meaning.classification=r.classification;x.meaning.user_delta=r.user_delta;x.meaning.existing_owner=r.existing_owner;x.meaning.acceptance=r.acceptance;x.meaning.status_gap=r.status_gap;
   x.integration.state=r.status??"R27_PARTIAL_OR_HELD";x.evidence.source_grade=r.grade??"R27_PROVISIONAL";push(x);
 }
 if(out.length!==517+code.length)throw Error("Expected "+(517+code.length)+" exact slots, got "+out.length);
 const ids=new Set(out.map(r=>r.id));if(ids.size!==out.length)throw Error("DUPLICATE SOURCE ID in unified bank");
 const counts={};for(const x of out)counts[x.bank]=(counts[x.bank]||0)+1;
 if(counts.ideas!==373||counts.functions!==144||counts.code!==code.length)throw Error("Wrong partitions "+JSON.stringify(counts));
 if(theme.H_original_ideation_first_pass.length!==190||theme.Q_original_questions_first_pass.length!==123||theme.O_index_owner_first_pass.length!==144)throw Error("Thematic source lost");
 return out;
}

export function documentIndex(locator){
 const out=[];for(const group of locator.directories??[]){for(const r of group.rows??[]){
  const kind=r.type==="file"?"reference_document_or_source_file":r.type==="dir"?"directory_entrance":"other";
  out.push({id:`DOC:${out.length+1}`,kind,path:r.path,blob:r.blob_sha??null,url:r.url??null,ref:group.ref??null,source_group:group.category??null,bytes:r.bytes??null,first_created_at:null,exact_source_revision_date:null,
     caution:"A directory or file locator is NOT a separately proved conceptual claim, source code implementation or native right."})}}
 const files=out.filter(r=>r.kind==="reference_document_or_source_file").length,dirs=out.filter(r=>r.kind==="directory_entrance").length;
 if(files!==locator.total_file_entries||dirs!==locator.total_directory_entries)throw Error("Curated file/dir no-drop "+files+"/"+dirs);
 return out;
}

export function validateBank(records,docs,code,union){
 if(records.length!==517+code.length||new Set(records.map(x=>x.id)).size!==records.length)throw Error("999 no-drop");
 const codeSet=new Set(code.map(x=>x.id));const gotCode=records.filter(x=>x.bank==="code");
 if(gotCode.length!==code.length||gotCode.some(r=>!codeSet.has(r.id)))throw Error("CODE 482 no-drop");
 if(docs.filter(x=>x.kind==="reference_document_or_source_file").length!==227)throw Error("Document locator no drop");
 for(const r of records){
  if(r.dates.first_produced_on!==null && r.dates.first_produced_grade==="UNKNOWN__PATH_HISTORY_NOT_EXECUTED")throw Error("Counterfeit production date");
  if(r.dates.selected_version_observed_at&&!r.source.exact_ref)throw Error("Unpinned date "+r.id);
  if(r.dates.first_path_committed_on && (!r.dates.first_path_commit||!r.source.path))throw Error("Invalid path introduction proof "+r.id);
  if(r.integration.do_not_infer_absence!==true)throw Error("Missing no-absence firewall");
 }
 return {total:records.length,concepts:records.filter(r=>r.bank==="ideas").length,functions:records.filter(r=>r.bank==="functions").length,code:gotCode.length,files:227,directories:25,
  dated_version:records.filter(r=>r.dates.selected_version_observed_at).length,first_production_verified:records.filter(r=>r.dates.first_produced_on).length,
  first_path_committed_verified:records.filter(r=>r.dates.first_path_committed_on).length,
  prior_300_preserved:union.sorokuda_source_and_alternative_versions.length}
}
