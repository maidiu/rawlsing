import {readFileSync} from "node:fs";
const root="WORKER_RETURNS/PYAT-HQ282-P03-TWO-FAMILY-EXTERNAL-FIELD-PRODUCTS-R1/";
const candidate=JSON.parse(readFileSync(root+"06_ORIGINAL_PRIMARY_FIELD_CANDIDATES.json","utf8"));
const owner=readFileSync("rawlsing_next/objective_consumer_bounded_evidence.py","utf8");
// Pure assertion function used in executed HQ282 P03 JS court.

function validate(d,owner){
const checks=[];const assert=(id,ok)=>{if(!ok)throw Error("REJECT_"+id);checks.push(id)};
const [a,b]=d.fields;
assert("PAIR_EXACTLY_TWO",d.fields.length===2);
assert("SOURCE_FAMILIES_INDEPENDENT",a.original_source_family!==b.original_source_family);
assert("SEPARATE_REGISTRAR_CUSTODIANS",a.custodian!==b.custodian);
assert("ORIGINAL_ROOTS_DISTINCT",a.original_source_root!==b.original_source_root);
assert("DIFFERENT_RECORDED_INSTRUMENT",a.source_native_record!==b.source_native_record);
assert("SOURCE_NATIVE_DATES_RETAINED",a.native_action_date==="1964-01-13"&&b.native_action_date==="1972-05-01");
assert("SOURCE_NATIVE_ACTIONS",a.native_action==="RATIFICATION"&&b.native_action==="ACCESSION");
assert("KENYA_ORIGINAL_TARGET",a.jurisdiction==="Kenya"&&b.jurisdiction==="Kenya"&&d.pair_boundary.same_named_target_country===true);
assert("OFFICIAL_ORIGIN_URLS",a.original_urls.every(u=>u.includes("ilo.org"))&&b.original_urls.every(u=>u.includes("treaties.un.org")));
assert("DOCUMENTARY_NOT_EMPIRICAL",a.original_pop_estimate===null&&b.original_pop_estimate===null&&d.pair_boundary.common_respondents.startsWith("NOT_APPLICABLE"));
assert("NO_FAKE_BYTES_HASH",d.fields.every(x=>x.byte_snapshot_sha256===null));
assert("RAWLSING_ISSUER_UNISSUED",d.fields.every(x=>x.rawlsing_field_issuer_ref===null&&x.n5_n6_field_product_ref===null));
assert("N9_USE_NOT_GRANTED",d.fields.every(x=>x.permitted_n9_use_ref===null));
assert("NO_FALSE_POSITIVE_PAIR",d.pair_boundary.n5_n6_product_count===0&&d.pair_boundary.ee13_issuer_count===0&&d.pair_boundary.n9_actual_consumer_count===0);
assert("EE13_INDEPENDENT_DECISION_REQUIRED",d.pair_boundary.first_allowable_relation_only_if_issued.startsWith("EE13_"));
assert("TIME_SOURCE_INDEXED_NOT_FORCED_IDENTICAL",d.pair_boundary.native_times_may_differ===true);
assert("CURRENT_OC05_IS_NOT_APPLICABLE",owner.includes('OC05:ConsumerBinding(OC05,"NOT_YET_APPLICABLE",None,')&&owner.includes('if not b.applicable or b.seam is None: raise NotYetApplicableConsumer'));
assert("NO_ANONYMOUS_AUTHORITY",d.source_caveats.some(x=>x.includes("do not appoint the Rawlsing")));
assert("SCIENTIFIC_GRADE_NOT_MINTED",d.scientific_status==="DUAL_DOCUMENTARY_EXTERNAL_SOURCE_WITNESSES__NO_ISSUED_TWO_FIELD_N5_N6_PRODUCT_PAIR");
assert("NO_GHANA_CONFOUNDING",d.world_target.includes("Kenya"));
return checks;
}
const baseline=validate(candidate,owner);
// Mutator SAME_FAMILY
// Mutator SAME_ROOT
// Mutator SAME_CUSTODIAN
// Mutator DATE_COLLAPSE
// Mutator RATIFICATION_ACCESSION_CONFUSION
// Mutator FALSE_POP_ESTIMATE
// Mutator FAKE_PRIMARY_BYTE_SHA
// Mutator SELF_ISSUED_FIELD
// Mutator FAKE_PRODUCER_PRODUCT
// Mutator FAKE_MODEL_USE
// Mutator FAKE_EE13_COUNT
// Mutator FAKE_N9_COUNT
// Mutator FORCED_TIME_EQUALITY
// Mutator DOCUMENTARY_TO_ISSUED
// Mutator CHANGE_TARGET_TO_GHANA
const mutants=[
["SAME_FAMILY",d=>d.fields[1].original_source_family=d.fields[0].original_source_family],
["SAME_ROOT",d=>d.fields[1].original_source_root=d.fields[0].original_source_root],
["SAME_CUSTODIAN",d=>d.fields[1].custodian=d.fields[0].custodian],
["DATE_COLLAPSE",d=>d.fields[1].native_action_date="1964-01-13"],
["RATIFICATION_ACCESSION_CONFUSION",d=>d.fields[1].native_action="RATIFICATION"],
["FALSE_POP_ESTIMATE",d=>d.fields[1].original_pop_estimate=1000000],
["FAKE_PRIMARY_BYTE_SHA",d=>d.fields[0].byte_snapshot_sha256="0".repeat(64)],
["SELF_ISSUED_FIELD",d=>d.fields[0].rawlsing_field_issuer_ref="P03_SELF"],
["FAKE_PRODUCER_PRODUCT",d=>d.fields[0].n5_n6_field_product_ref="fake"],
["FAKE_MODEL_USE",d=>d.fields[1].permitted_n9_use_ref="fake"],
["FAKE_EE13_COUNT",d=>d.pair_boundary.ee13_issuer_count=1],
["FAKE_N9_COUNT",d=>d.pair_boundary.n9_actual_consumer_count=1],
["FORCED_TIME_EQUALITY",d=>d.pair_boundary.native_times_may_differ=false],
["OMIT_OC05_NOT_APPLICABLE",d=>d.owner=d.owner.replace('OC05:ConsumerBinding(OC05,"NOT_YET_APPLICABLE",None,','OC05:ConsumerBinding(OC05,"APPLICABLE_CURRENT","made-up",')],
["DOCUMENTARY_TO_ISSUED",d=>d.scientific_status="REAL_ISSUED_PAIR"],
["CHANGE_TARGET_TO_GHANA",d=>d.world_target="Ghana"]
];
const results=[];
for(const [id,mutate] of mutants){const x=JSON.parse(JSON.stringify(candidate));x.owner=owner;mutate(x);let detected=false;try{validate(x,x.owner)}catch{detected=true}results.push({id,detected})}
if(results.some(x=>!x.detected))throw new Error("Hostile escaped");
console.log(JSON.stringify({contract_checks:baseline.length,hostile_refusals:results.length,grade:"DOCUMENTARY_SOURCE_FREE_NO_N5_N6_EE13_N9_AUTHORITY"},null,2));
