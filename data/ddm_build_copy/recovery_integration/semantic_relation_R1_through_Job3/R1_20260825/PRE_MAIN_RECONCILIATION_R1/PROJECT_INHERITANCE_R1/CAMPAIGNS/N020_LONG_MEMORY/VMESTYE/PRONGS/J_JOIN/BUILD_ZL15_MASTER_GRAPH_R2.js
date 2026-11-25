/*
VMESTYE ZL-15 R1. Deterministic documentary-source atlas builder.
This source is NOT a science issuer, a native execution harness, a claims-of-success
validator or a substitute for ZL16/ZL17 independent review.
Inputs: eight DATA TSVs; three J_JOIN sidecars (empty initially); 1-2 exact
PR859 R5 received prong bundles, each preserving the six frozen original TSVs.
Output: eight populated DATA TSVs plus three append-only join sidecars.
*/
function normalize(input) {
  // R2 key conservation: all P1 local IDs are namespaced; rebuild from frozen P0 seeds, never append to R1.
  const DATA_NAMES = ["FUNCTION_ATLAS","RELATIONS","OPERATION_TRACES","AUTHORITY_APPLICATIONS","EVIDENCE","IMPLEMENTATIONS","CONSUMER_EDGES","DECISION_EVENTS"];
  const norm=x=>String(x===null||x===undefined?"":x).replace(/[\t\r\n]+/g," ").trim();
  function parse(s) {
    if(!s) throw Error("Missing TSV source");
    const lines=s.trimEnd().split(/\r?\n/), h=lines.shift().split("\t");
    const seen=new Set();
    const rows=lines.filter(Boolean).map((line,i)=>{
      const parts=line.split("\t");
      if(parts.length!==h.length) throw Error("Wrong TSV width at "+i+": "+parts.length+"/"+h.length);
      const o={};h.forEach((name,j)=>o[name]=parts[j]);
      return o;
    });
    return {h,rows};
  }
  function serialize(t) {
    return t.h.join("\t")+"\n"+t.rows.map(r=>t.h.map(k=>norm(r[k])).join("\t")).join("\n")+(t.rows.length?"\n":"");
  }
  const D={};
  for(const n of DATA_NAMES) {
    D[n]=parse(input.current[n]);
    D[n].keys=new Set(D[n].rows.map(r=>r[D[n].h[0]]));
    if(D[n].keys.size!==D[n].rows.length) throw Error("Existing key collision in "+n);
  }
  function put(n,row) {
    const t=D[n],key=norm(row[t.h[0]]);
    if(!key) throw Error("Missing primary ID in "+n);
    if(t.keys.has(key)) return false;
    t.keys.add(key);t.rows.push(row);return true;
  }
  const ANTI_H="anti_join_id\tprong_id\tcoverage_id\tcensus_id\testate_id\tsource_commit_sha\tsource_path\tsource_composite_id\tsource_grain\tfinding_id\tprong_coverage_status\tp0_tuple_check\tprong_review_grade\tgap_or_alias\towner\tfalsifier";
  const CONFLICT_H="conflict_id\tprong_id\tunjoin_id\tfinding_id\tcensus_id\testate_id\tsource_commit_sha\tsource_path\tsource_composite_id\tsource_grain\tjoin_target_type\tattempted_target_id\tfailure_code\tcandidate_aliases\tevidence_id\tnegative_preserved\tunresolved_question\tnext_owner\tfalsifier\tstatus\trepair_priority";
  const RECEIPT_H="prong_id\texact_author_head\treview_ref\tfindings\toperation_traces\tauthority_use\tevidence\tcoverage\tunjoins\trow_widths_verified\tcurrent_machine_scope";
  const side={
    anti:input.side.anti?parse(input.side.anti):parse(ANTI_H+"\n"),
    conflicts:input.side.conflicts?parse(input.side.conflicts):parse(CONFLICT_H+"\n"),
    receipts:input.side.receipts?parse(input.side.receipts):parse(RECEIPT_H+"\n")
  };
  for(const [k,h] of [["anti",ANTI_H],["conflicts",CONFLICT_H],["receipts",RECEIPT_H]]) if(side[k].h.join("\t")!==h) throw Error("Unexpected sidecar schema: "+k);
  for(const k of Object.keys(side)) {side[k].keys=new Set(side[k].rows.map(r=>r[side[k].h[0]]));}
  function sidePut(name,row) {
    const t=side[name],key=norm(row[t.h[0]]);
    if(!key||t.keys.has(key))return false;
    t.keys.add(key);t.rows.push(row);return true;
  }
  function fromValues(header,values){const h=header.split("\t"),o={};h.forEach((k,i)=>o[k]=values[i]??"");return o;}
  function relation(id,from,type,to,prong,grade,ref,cut,comment,evidenceId="UNRESOLVED"){
    put("RELATIONS",{relation_id:id,from_id:from,relation_type:type,to_id:to,generation_from:prong,generation_to:"VMESTYE_CANDIDATE",applicability_or_condition:"SOURCE_GRAIN_REVIEW_REQUIRED",operation_or_authority_id:ref||"UNRESOLVED",evidence_id:evidenceId||"UNRESOLVED",at_cut:cut,grade,comment});
  }
  const counts={};
  for(const b of input.bundles) {
    const pid=b.prong_id,cut=b.source_head,ts={};
    // P1 primary identity is (prong_id, local_id), never local_id alone.
    const key=(kind,id)=> !id || id==='UNRESOLVED' || id==='UNKNOWN' ? 'UNRESOLVED' : `J-${kind}-${pid}-${id}`;
    const fid=id=>key('F',id),tid=id=>key('OP',id),aid=id=>key('AU',id),eid=id=>key('EV',id),uid=id=>key('UJ',id);

    for(const [n,s] of Object.entries(b.tables))ts[n]=parse(s);
    const required=["FINDINGS","OPERATION_TRACES","AUTHORITY_USE","EVIDENCE","COVERAGE","UNJOINS"];
    for(const n of required){
      if(!ts[n]||ts[n].rows.length!==b.counts[n]) throw Error(pid+" count differs from frozen input: "+n);
      if(n!=="FINDINGS" && ts[n].h[0]!=="prong_id") throw Error(pid+" wrong first field: "+n);
      const expected={"FINDINGS":"finding_id","OPERATION_TRACES":"trace_id","AUTHORITY_USE":"authority_use_id","EVIDENCE":"evidence_id","COVERAGE":"coverage_id","UNJOINS":"unjoin_id"}[n];
      if((n==="FINDINGS"?ts[n].h[0]:ts[n].h[1])!==expected)throw Error(pid+" changed P1 contract: "+n);
      for(const r of ts[n].rows)if(n!=="FINDINGS"&&r.prong_id!==pid)throw Error(pid+" cross-prong row in "+n);
    }
    const findings=new Map(ts.FINDINGS.rows.map(f=>[f.finding_id,f]));
    if(findings.size!==ts.FINDINGS.rows.length)throw Error(pid+' duplicate local finding_id');
    for(const n of required.slice(1)){
      const k={OPERATION_TRACES:'trace_id',AUTHORITY_USE:'authority_use_id',EVIDENCE:'evidence_id',COVERAGE:'coverage_id',UNJOINS:'unjoin_id'}[n];
      const keys=ts[n].rows.map(r=>r[k]);
      if(new Set(keys).size!==keys.length)throw Error(pid+' duplicate local '+n+' '+k);
    }
    const mapOf=(n,k)=>{const m=new Map();for(const r of ts[n].rows){const a=m.get(r[k])||[];a.push(r);m.set(r[k],a);}return m};
    const ops=mapOf("OPERATION_TRACES","finding_id"),auth=mapOf("AUTHORITY_USE","finding_id"),ev=mapOf("EVIDENCE","finding_id");
    for(const n of required.slice(1))for(const r of ts[n].rows)if(r.finding_id && r.finding_id!=="UNRESOLVED" && !findings.has(r.finding_id))throw Error(pid+" dangling finding FK in "+n+": "+r.finding_id);
    for(const f of ts.FINDINGS.rows){
      const id=fid(f.finding_id),oo=ops.get(f.finding_id)||[],aa=auth.get(f.finding_id)||[],ee=ev.get(f.finding_id)||[];
      let disp=f.candidate_disposition||"OPEN_PROOF_GAP";
      if(/PROVED_CURRENT|PROVED_STRONGER|ZERO_LOSS/i.test(disp))disp="OPEN_PROOF_GAP__CURRENT_PROOF_REQUIRED";
      put("FUNCTION_ATLAS",{
        record_id:id,namespace:pid+"_DOCUMENTARY_FINDING",function_statement:(f.function_ids||"UNKNOWN")+" :: "+(f.transformation_human||"Source-derived functional finding"),
        source:cut+"::"+b.source_location+"/FINDINGS.tsv#"+f.finding_id,original_purpose:f.original_input||"UNKNOWN",
        legacy_operation_ids:oo.map(o=>tid(o.trace_id)).join(";")||"NO_TRACE",dva_fate:pid==="ZL05"?(f.candidate_disposition||"DOC_ONLY"):"UNRECONCILED",
        trii_fate:pid==="ZL06"?(f.candidate_disposition||"DOC_ONLY"):"UNRECONCILED",
        chetiri_fate:pid==="ZL07"?(f.candidate_disposition||"DOC_ONLY"):"UNRECONCILED",
        long_memory_id:(f.function_ids||"").match(/LMX-\d+|LMQ-\d+/g)?.join(";")||"UNRESOLVED",
        pyat_owner_ids:f.current_owner_or_unknown||"UNKNOWN",
        programma_s01_s11_ids:(f.function_ids||"").match(/(?:S0[1-9]|S1[01]|GAP-\d+)/g)?.join(";")||"UNRESOLVED",
        current_code_and_sha:"SOURCE_CLAIM_ONLY: "+(f.exact_source_sha_path_symbol||"UNKNOWN"),
        authority_application_ids:aa.map(a=>aid(a.authority_use_id)).join(";")||"NONE_RECORDED",
        actual_consumer_ids:"NOT_PROVED_NON_TEST",
        completeness_grade:"R5_RECEIVED_S0_S1__"+(f.current_evidence_grade||"UNKNOWN"),
        disposition:disp,next_step:f.unresolved_and_falsifier||"OWNER_REVIEW_REQUIRED"
      });
      const tokens=(f.function_ids||"").split(";").map(x=>x.trim()).filter(Boolean);
      for(let i=0;i<tokens.length;i++){
        const token=tokens[i],hub=D.FUNCTION_ATLAS.keys.has(token)?token:"J-IDENT-"+token;
        if(!D.FUNCTION_ATLAS.keys.has(hub))put("FUNCTION_ATLAS",{
          record_id:hub,namespace:"EXACT_LITERAL_FUNCTION_LABEL__NOT_SEMANTIC_EQUIVALENCE",
          function_statement:token,source:cut+"::"+b.source_location+"/FINDINGS.tsv#"+f.finding_id,
          original_purpose:"IDENTIFIER_HUB_ONLY",legacy_operation_ids:"NOT_ASSESSED",
          completeness_grade:"LABEL_ONLY",disposition:"OPEN_PROOF_GAP",
          next_step:"Independently determine same-grain functional equivalence"
        });
        relation("JR-"+pid+"-"+f.finding_id+"-ID"+i,id,"ASSIGNED_TO",hub,pid,"EXACT_LABEL_MATCH__NO_EQUIVALENCE",token,cut,"Many-to-many label crosswalk only; not a proven succession",eid(ee[0]?.evidence_id));
      }
      for(const a of aa)relation("JR-"+pid+"-"+f.finding_id+"-AU-"+a.authority_use_id,id,"REQUIRES_AUTHORITY",aid(a.authority_use_id),pid,"DOCUMENTARY_AUTHORITY_ONLY",a.authority_id,cut,"Issuer selection, applied effect and refusal require real independent proof",eid(ee[0]?.evidence_id));
      put("IMPLEMENTATIONS",{
        implementation_id:"J-IM-"+pid+"-"+f.finding_id,function_ids:id,generation:f.source_generation||pid,
        code_symbol:f.exact_source_sha_path_symbol||"UNKNOWN",
        code_sha:"PRONG_REPORT_AT_"+cut,branch_or_protected:"PRONG_BRANCH_AT_"+cut+"__NOT_PROTECTED_ADOPTION",
        interface_and_output:f.produced_output||"UNKNOWN",
        actual_caller:"NOT_VERIFIED",first_actual_consumer:"NOT_VERIFIED",test_and_review_receipts:"PR859_R5_S0_S1_DOCUMENTARY",
        source_native_scope:"NOT_PROVED",current_selection_status:"OPEN_PROOF_GAP",evidence_id:eid(ee[0]?.evidence_id)
      });
      put("DECISION_EVENTS",{
        event_id:"JEV-"+pid+"-"+f.finding_id,record_id:id,previous_state:"NOT_JOINED_IN_MASTER",
        new_state:"S0_S1_DOCUMENTARY_RETURN_ADMITTED_CANDIDATE",
        finding:pid+" "+(f.function_ids||"UNKNOWN"),interpretation:"R5 accepts prong documentary evidence only, not current/native success",
        action:"INDEPENDENT_ZL16_ZL17_REVIEW_REQUIRED",accountable_owner:"ZL15_THEN_#815_#816",
        source_evidence_id:eid(ee[0]?.evidence_id),
        writer_return_sha:cut,independent_reviewer_and_receipt:"PR859_R5_449a97480dfa5c9f7f2042d688fe1ed1869ffe91_S0_S1",
        decided_at_cut:input.protectedCut,falsifier:f.unresolved_and_falsifier||"NATIVE_AND_ACTUAL_READER_REQUIRED",
        pyat_reciprocal_status:"NOT_REQUESTED_NOT_RECEIVED"
      });
    }
    for(const o of ts.OPERATION_TRACES.rows){
      put("OPERATION_TRACES",{
        operation_id:tid(o.trace_id),function_ids:fid(o.finding_id),generation:pid,
        input_data_source:[o.estate_id,o.source_commit_sha,o.source_path,o.source_composite_id,o.source_grain].join("::"),
        input_meaning:o.input_semantics||o.input_source_ref,
        code_symbol_at_sha:cut+"::"+b.source_location+"/OPERATION_TRACES.tsv#"+o.trace_id+" ["+(o.execution_status||"UNKNOWN")+"]",
        selected_authority_ids:o.selected_rule_ref||"UNRESOLVED",
        transformation_human_language:o.transformation_human_language,
        output_object:o.output_object,producer_edge_id:o.producer_edge_id||"UNRESOLVED",
        actual_consumer_id:"NOT_PROVED_NON_TEST",consumer_evidence_id:eid(o.first_consumer_evidence_id),
        negative_behavior:o.negative_or_refusal||"UNKNOWN",test_receipt_ids:"NOT_RUN_BY_ZL15",
        semantic_scope:"SOURCE_GRAIN="+o.source_grain+";REPORTED_FIRST_READER="+(o.first_consumer_id||"UNRESOLVED"),
        current_proof_grade:"R5_DOCUMENTARY_ONLY__"+(o.proof_grade||"S1"),
        missing_next_edge:o.missing_next_edge||"READER_AUTHORITY_REQUIRED"
      });
      const edge="J-EDGE-"+pid+"-"+o.trace_id;
      put("CONSUMER_EDGES",{
        edge_id:edge,producer_operation_id:tid(o.trace_id),consumer_operation_id:o.first_consumer_id||"UNRESOLVED",
        from_object:o.output_object,to_required_contract:o.missing_next_edge||"FIRST_READER_RECEIPT_REQUIRED",
        edge_kind:"CANDIDATE_TRACE__NOT_PROVED_ACTUAL",predicate_when_if:"UNKNOWN_UNLESS_SOURCE_RECEIPT",
        actual_call_site_sha:"NOT_PROVED",current_actual_status:"OPEN_PROOF_GAP",
        positive_evidence_id:eid(o.first_consumer_evidence_id),
        negative_evidence_id:"SOURCE_NEGATIVE_CARRIED",terminal_consequence:"READER_AND_SEMANTIC_EFFECT_HELD"
      });
      relation("JR-"+pid+"-"+o.trace_id+"-EDGE",tid(o.trace_id),"HELD_BY",edge,pid,"FIRST_CONSUMER_NOT_NATIVE_PROVED",edge,cut,"Reported consumer retained as candidate; actual non-test first reader not issued",eid(o.first_consumer_evidence_id));
    }
    for(const a of ts.AUTHORITY_USE.rows)put("AUTHORITY_APPLICATIONS",{
      application_id:aid(a.authority_use_id),authority_id:a.authority_id||"UNRESOLVED",
      authority_source_sha_path_rule:a.authority_rule_source_ref,function_ids:fid(a.finding_id),operation_ids:tid(a.trace_id),
      rule_available:a.rule_available||"UNKNOWN",rule_selected_for_scope:a.rule_selected_for_scope||"UNKNOWN",
      rule_applied_to_output:a.rule_applied_to_output||"UNKNOWN",
      negative_or_refusal_enforced:a.refusal_enforced||"UNKNOWN",
      selected_authority_issuer:"NOT_VERIFIED_BY_ZL15",actual_consumer_edge_id:"NOT_PROVED_NON_TEST",
      evidence_ids:"SOURCE_RETURN_AT_"+cut,version_cut:cut,
      grade:"R5_DOCUMENTARY_ONLY__"+(a.authority_status||"UNKNOWN")+"__"+(a.proof_grade||"S1"),
      falsifier:a.falsifier||"CURRENT_ISSUER_AND_RULE_EFFECT_REQUIRED"
    });
    for(const e of ts.EVIDENCE.rows)put("EVIDENCE",{
      evidence_id:eid(e.evidence_id),source_sha:e.source_commit_sha||cut,
      path:e.source_path||b.source_location+"/EVIDENCE.tsv",
      line_range_or_row_id:[e.source_row_locator,"ESTATE="+e.estate_id,"BLOB="+e.source_blob_sha,"CENSUS="+e.census_id,"COMPOSITE="+e.source_composite_id,"GRAIN="+e.source_grain].join(";"),
      claim_supported:e.claim_supported||"UNKNOWN",evidence_type:e.evidence_kind||e.claim_kind||"SOURCE_RECORD",
      observed_at_cut:e.observed_cut||cut,original_native_or_sourcefree:e.original_native_status||"NOT_RUN",
      independent_review_ref:"PR859_R5_449a97480dfa5c9f7f2042d688fe1ed1869ffe91__S0_S1_ONLY",
      ceiling_and_negative:(e.proof_grade||"S1")+"; "+(e.negative_or_refusal||"UNKNOWN")
    });
    for(const c of ts.COVERAGE.rows)sidePut("anti",fromValues(ANTI_H,[
      "AJ-"+c.prong_id+"-"+c.coverage_id,c.prong_id,c.coverage_id,c.census_id,c.estate_id,c.source_commit_sha,
      c.source_path,c.source_composite_id,c.source_grain,c.finding_id,c.coverage_status,
      "P0_R5_REVIEWED__AUTHOR_RECHECK_PENDING","R5_S0_S1",c.missing_joins,c.next_owner,
      findings.get(c.finding_id)?.unresolved_and_falsifier||"SOURCE_TUPLE_AND_SEMANTIC_READER_COURT"
    ]));
    for(const u of ts.UNJOINS.rows){
      sidePut("conflicts",fromValues(CONFLICT_H,[
        "C-"+u.prong_id+"-"+u.unjoin_id,u.prong_id,u.unjoin_id,u.finding_id,u.census_id,u.estate_id,
        u.source_commit_sha,u.source_path,u.source_composite_id,u.source_grain,u.join_target_type,
        u.attempted_target_id,u.failure_code,u.candidate_aliases,u.evidence_id,u.negative_preserved,
        u.unresolved_question,u.next_owner,u.falsifier,u.status,
        (u.failure_code||"").includes("FIRST_READER")?"P1_FIRST_READER":"P2_OWNER_COURT"
      ]));
      relation("JR-"+pid+"-"+u.unjoin_id+"-HOLD",fid(u.finding_id),"HELD_BY",uid(u.unjoin_id),pid,
        "UNRESOLVED_TYPED_OPEN",u.unjoin_id,cut,u.failure_code||"UNKNOWN",eid(u.evidence_id));
    }
    sidePut("receipts",fromValues(RECEIPT_H,[
      pid,cut,"PR859_R5_S0_S1",...required.map(n=>ts[n].rows.length),"YES","NO_NATIVE_CLAIM"
    ]));
    counts[pid]=Object.fromEntries(required.map(n=>[n,ts[n].rows.length]));
  }
  const out={};
  for(const n of DATA_NAMES)out["DATA/"+n+".tsv"]=serialize(D[n]);
  out["PRONGS/J_JOIN/FULL_ID_ANTI_JOINS.tsv"]=serialize(side.anti);
  out["PRONGS/J_JOIN/CONFLICTS_AND_REPAIR_ORDER.tsv"]=serialize(side.conflicts);
  out["PRONGS/J_JOIN/SOURCE_PROOF_RECEIPTS.tsv"]=serialize(side.receipts);
  return {files:out,processed:counts,canonicalCounts:Object.fromEntries(DATA_NAMES.map(n=>[n,D[n].rows.length])),
    coverage:side.anti.rows.length,unjoins:side.conflicts.rows.length};
}
