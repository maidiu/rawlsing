#!/usr/bin/env node
// Read-only HQ281 A06 documentary/contract court. Node >=18.
// Use from repository root: node WORKER_RETURNS/PYAT-HQ281-A06-FIRST-QUALIFIED-SOURCE-TO-CONSUMER-R1/repro/validate_source_free_contract.mjs
// This does NOT execute source-read / Python owner functions or confer permission.
import {readFileSync} from "node:fs";
const root="WORKER_RETURNS/PYAT-HQ281-A06-FIRST-QUALIFIED-SOURCE-TO-CONSUMER-R1/";
const js=p=>JSON.parse(readFileSync(p,"utf8"));
const txt=p=>readFileSync(p,"utf8");
const baseline={
 p:js(root+"01_THREE_NEAREST_ISSUED_PATHS.json"),
 h:js(root+"04_HOSTILES.json"),
 s:js(root+"06_ALL35_NINE_FAMILY_SCREEN.json"),
 w:js("WORKER_RETURNS/PYAT-HQ221-C5-GT2-STRUCTURAL-POSITIVE-REALIZATION-R1/01_RETAINED_EMPIRICAL_INPUT_BINDING.json"),
 ff:txt("rawlsing_next/field_forge_conditional_support.py"),
 gov:txt("rawlsing_next/gt12_e2b_publication_governance_binding.py"),
 c11:txt("rawlsing_next/pre553_source_backed_c11_facade.py")
};
function verify(d){
 const checks=[];const must=(name,b)=>{if(!b)throw Error("A06 SOURCEFREE FAIL "+name);checks.push(name)};
 const {p,h,s,w,ff,gov,c11}=d,[a,b,c]=p.paths;
 must("01_35_WAVES",s.sources.length===35&&s.count.waves===35);
 must("02_NINE_FAMILIES",new Set(s.sources.map(x=>x.family)).size===9&&s.count.families===9);
 must("03_UNIQUE_IDENTITIES",new Set(s.sources.map(x=>x.source_id)).size===35);
 must("04_HISTORICAL_IMPLEMENTATIONS",s.sources.reduce((n,x)=>n+x.historical_implementations,0)===18276);
 must("05_MEASUREMENT_CANDIDATES",s.sources.reduce((n,x)=>n+x.measurement_candidate_implementations,0)===13270);
 must("06_INCIDENT_VS_DISTINCT",s.sources.reduce((n,x)=>n+x.alternative_conflict_incidences_a01,0)===10479&&s.count.a01_global_distinct_implementations_with_alternative_conflicts===10457);
 must("07_UNIQUE_EXISTING_CONSUMED_SOURCE",s.sources.filter(x=>x.item_to_current_consumer_issuance_proved).map(x=>x.source_id).join()==="SRC02");
 must("08_NEW_B02_UNISSUED",s.sources.every(x=>x.new_B02_issuance_proved===false));
 must("09_HOLD_NOT_INTRINSIC_NA",s.sources.every(x=>x.other_unevidenced_scopes==="UNKNOWN_NOT_INTRINSIC_NA"));
 must("10_FAMILY_TOTAL",Object.values(s.family_counts).reduce((n,x)=>n+x,0)===35);
 must("11_THREE_PROSPECTS_NOT_POSITIVES",p.full_three_positive_found===false&&p.grading==="THREE_PROSPECTS_NOT_THREE_ISSUED_FULL_PATHS");
 must("12_RANKED_PATHS",p.paths.length===3&&p.paths.map(x=>x.rank).join()==="1,2,3"&&s.ranked_nearest.join()==="SRC02,SRC27,SRC35");
 must("13_TEMPORAL_SYNTAX",p.screen.temporal_candidate_pairs===63&&s.count.temporal_syntactic_pairs===63);
 must("14_Q86_ROLES",a.items.conditioner==="Q86B"&&a.items.target==="Q86A"&&w.target_roles.conditioner.source_native_variable==="Q86B"&&w.target_roles.target.source_native_variable==="Q86A");
 must("15_SOURCE_SHA",a.source_sha256===w.source_sha256_frozen&&a.source_sha256.length===64);
 must("16_QUERY_FACT_REFS",a.query_sha256===w.empirical_query_spec_ref.content_hash&&a.fact_sha256===w.empirical_fact_ref.content_hash);
 must("17_RISK_SET_19210",w.raw_denominator_support===19210&&w.raw_numerator_support===19210&&w.risk_set.retained_rows===19210&&a.native.risk.includes("19,210"));
 must("18_GHANA_EXCLUDED",a.native.risk.includes("EXCLUDING Ghana")&&s.sources.find(x=>x.source_id==="SRC02").narrow_claims[0].not_proven.includes("GHANA"));
 must("19_RAW_UNWEIGHTED",w.measure_kind==="RAW"&&w.weighted_support_authorized===false&&a.native.weight==="RAW unweighted");
 must("20_TYPED_SCOPE",w.source_scope_mode==="SINGLE_UNIVERSE"&&w.fact_typed_state==="SUPPORTED"&&w.joint_order_semantics==="SEMANTIC_ORDERED");
 must("21_5_AUTHORITY_SNAPSHOTS",a.accepted_authorities.length===5&&w.fact_authority_snapshot_refs.length===5);
 must("22_EXACT_AUTHORITY_HASHES",a.accepted_authorities.every(([id,hash])=>w.fact_authority_snapshot_refs.some(x=>x.authority_id===id&&x.authority_content_hash===hash)));
 must("23_QUERY_AUTHORITY_SUBSET",w.query_authority_snapshot_refs.every(x=>w.fact_authority_snapshot_refs.some(y=>x.authority_id===y.authority_id&&x.authority_content_hash===y.authority_content_hash)));
 must("24_NO_NEW_ROW_READ",w.raw_source_access==="FORBIDDEN__NOT_PERFORMED"&&a.new_B02==="HOLD"&&a.expected_E.includes("NOT_ISSUED"));
 must("25_LITS_JOINT_NOT_MARGINAL",b.native.joint_risk===24630&&b.native.marginal_risks.join()==="24897,28325"&&b.native.joint_risk!==b.native.marginal_risks[0]);
 must("26_LITS_NOT_FF02",b.status.includes("CONSUMER_HELD")&&b.permission.includes("not FF02"));
 must("27_WVS_UNISSUED",c.native.risk==="HELD"&&c.status.includes("NOT_AN_ISSUED_PATH")&&c.expected_E==="NOT_ISSUED");
 must("28_DOCUMENTARY_HOSTILES_UNEXECUTED",h.tests.length===15&&h.tests.every(x=>x.observed_runtime==="NOT_EXECUTED_BY_A06")&&h.source_raw_reads===0);
 must("29_HOSTILE_IDS_UNIQUE",new Set(h.tests.map(x=>x.id)).size===15);
 must("30_FIELD_FORGE_RISK_GUARD_PRESENT",ff.includes("producer fact/query risk-set mismatch")&&ff.includes("SINGLE_UNIVERSE"));
 must("31_FIELD_FORGE_WEIGHT_GUARD_PRESENT",ff.includes("GT2 relation may not consume weighted numerator")&&ff.includes("GT2 relation may not consume weighted denominator"));
 must("32_FIELD_FORGE_CELL_GUARD_PRESENT",ff.includes("does not preserve the complete native Q86B x Q86A domain")&&ff.includes("zero joint count has inconsistent cell state"));
 must("33_CONTEXT_ONLY_GOVERNANCE_TEXT",gov.includes("V557_STATE = V557DecisionState.ALLOW_CONTEXT_ONLY")&&gov.includes('"producer_permission_created_here": False'));
 must("34_DENIAL_TOKENS_TEXT",gov.includes('"ACTIVE_CAUSAL"')&&gov.includes('"V555"')&&gov.includes("forbidden permission/lane entered V557 current uses"));
 must("35_C11_SOURCE_SHA_GUARD_TEXT",c11.includes("snapshot ref does not bind expected source SHA")&&c11.includes("source_sha256 != projection.expected_source_sha256"));
 must("36_C11_RESPONDENT_BINDING_TEXT",c11.includes("class RowRespondentBinding"));
 return checks;
}
const positive=verify(baseline);
const mutators=[
 ["DROP_WAVE",x=>x.s.sources.pop()],
 ["DUPLICATE_SOURCE",x=>x.s.sources[2].source_id="SRC02"],
 ["DROP_IMPLEMENTATION",x=>x.s.sources[4].historical_implementations--],
 ["MEASUREMENT_INFLATION",x=>x.s.sources[4].measurement_candidate_implementations++],
 ["ISSUE_B02",x=>x.s.sources[1].new_B02_issuance_proved=true],
 ["UNKNOWN_TO_INTRINSIC_NA",x=>x.s.sources[1].other_unevidenced_scopes="SOURCE_NONAPPLICABLE"],
 ["THREE_FALSE_POSITIVES",x=>x.p.full_three_positive_found=true],
 ["GHANA_SCOPE_WIDEN",x=>x.p.paths[0].native.risk="19,210 including Ghana"],
 ["ROLE_SWAP",x=>x.p.paths[0].items.conditioner="Q86A"],
 ["FACT_HASH_DRIFT",x=>x.p.paths[0].fact_sha256="0".repeat(64)],
 ["DENOMINATOR_REASSIGN",x=>x.p.paths[0].native.risk="24,630"],
 ["WEIGHT_PROMOTION",x=>x.p.paths[0].native.weight="national weighted"],
 ["AUTHORITY_DROP",x=>x.p.paths[0].accepted_authorities.pop()],
 ["LITS_MARGINAL_AS_JOINT",x=>x.p.paths[1].native.joint_risk=24897],
 ["WVS_FALSE_RISK",x=>x.p.paths[2].native.risk=100],
 ["HOSTILE_RUNTIME_FORGERY",x=>x.h.tests[0].observed_runtime="PASS"],
 ["GOVERNANCE_WIDENING_TEXT",x=>x.gov=x.gov.replace("V557_STATE = V557DecisionState.ALLOW_CONTEXT_ONLY","V557_STATE = V557DecisionState.ALLOW_ACTIVE_CAUSAL")],
 ["C11_GUARD_ERASURE_TEXT",x=>x.c11=x.c11.replace("snapshot ref does not bind expected source SHA","unchecked")]
];
const results=[];
for(const [id,mutate] of mutators){
 const x=JSON.parse(JSON.stringify(baseline));mutate(x);
 let refused=false,reason="";
 try{verify(x)}catch(e){refused=true;reason=e.message}
 results.push({id,refused,reason});
}
if(results.some(x=>!x.refused))throw Error("A06 mutation escaped: "+results.filter(x=>!x.refused).map(x=>x.id));
console.log(JSON.stringify({schema:"HQ281_A06_SOURCEFREE_REPRO@1",checks_passed:positive.length,mutation_refusals:results.length,source_read:false,python_runtime_executed:false,consumer_executed:false,results},null,2));
