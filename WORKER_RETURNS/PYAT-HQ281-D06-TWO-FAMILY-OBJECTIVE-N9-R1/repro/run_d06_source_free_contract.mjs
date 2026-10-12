// HQ281 D06 TEST-ONLY. All data synthetic; no source, issuer, EE13 or N9 rights.
// Identical functions were executed in the browser/connector JavaScript orchestration.
// Run: node repro/run_d06_source_free_contract.mjs
const deep=x=>JSON.parse(JSON.stringify(x));
function validateTwoFamily(request, trusted) {
  const hold=reason=>({state:"HELD_SOURCE_FREE_CONTRACT",reason});
  if(!request || !Array.isArray(request.fields) || request.fields.length!==2) return hold("EXACT_TWO_FIELDS_REQUIRED");
  if(request.mode!=="SOURCE_INDEXED_NONPOOLED") return hold("CROSS_SAMPLE_PSEUDO_POOLING");
  if(request.claim!=="COMPOSED_CONTEXT_ONLY") return hold("CLAIM_WIDENING_NOT_ISSUED");
  if(request.actorUse || request.modelUse) return hold("ACTOR_OR_MODEL_USE_NOT_GRANTED");
  const seen=new Set();const receipts=[];
  for(const f of request.fields){
    if(!f || !f.ref || seen.has(f.ref))return hold("DUPLICATE_FIELD_PRODUCT");
    seen.add(f.ref);
    const receipt=trusted.producers[f.ref];
    if(!receipt || receipt.state!=="OWNER_ISSUED" || !receipt.issuerRef) return hold("MISSING_AUTHENTIC_PRODUCER_ISSUER");
    if(f.hash!==receipt.hash || f.sourceRoot!==receipt.sourceRoot || f.sourceFamily!==receipt.sourceFamily)return hold("FORGED_OR_UNBOUND_SOURCE_ROOT");
    if(f.unit!==receipt.unit || f.estimand!==receipt.estimand || f.population!==receipt.population)return hold("UNIT_ESTIMAND_POPULATION_MISMATCH");
    if(f.time!==receipt.time || f.place!==receipt.place)return hold("FIELD_TIME_PLACE_BINDING_MISMATCH");
    if(f.uncertainty!==receipt.uncertainty || !f.uncertainty)return hold("UNCERTAINTY_NOT_CONSERVED");
    if(!receipt.permissions.includes("N9_WORLD_CONTEXT"))return hold("MISSING_CONSUMER_USE_PERMISSION");
    if(!["EXTERNAL_OBSERVATION","STRUCTURAL_RULE_OBSERVATION"].includes(receipt.semanticKind))return hold("SUBJECTIVE_CONTEXT_NOT_OBJECTIVE_FIELD");
    receipts.push(receipt);
  }
  if(receipts[0].sourceFamily===receipts[1].sourceFamily || receipts[0].sourceRoot===receipts[1].sourceRoot)return hold("DUPLICATE_SOURCE_FAMILY");
  if(receipts[0].population===receipts[1].population)return hold("CROSS_FAMILY_UNIVERSE_REIDENTIFICATION");
  if(request.fields.some(f=>f.time!==request.time || f.place!==request.place))return hold("WORLD_TIME_PLACE_INCOMPATIBLE");
  const ee13=trusted.ee13[request.ee13Ref];
  if(!ee13 || !ee13.issuerRef || ee13.state!=="OWNER_ISSUED")return hold("MISSING_EE13_COMPETENT_ISSUANCE");
  if(ee13.time!==request.time || ee13.place!==request.place || ee13.mode!=="SOURCE_INDEXED_NONPOOLED" || ee13.claim!=="COMPOSED_CONTEXT_ONLY")return hold("EE13_SCOPE_MISMATCH");
  if(ee13.productRefs.slice().sort().join("|")!==request.fields.map(f=>f.ref).sort().join("|"))return hold("EE13_PRODUCT_PAIR_NOT_BOUND");
  const n9=trusted.consumers[request.queryRef];
  if(!n9 || n9.state!=="CONSUMED" || !n9.ownerRef)return hold("NO_ACTUAL_N9_CONSUMER");
  if(n9.outputRef!==request.outputRef || n9.ee13Ref!==request.ee13Ref || n9.time!==request.time || n9.place!==request.place || n9.productRefs.slice().sort().join("|")!==request.fields.map(f=>f.ref).sort().join("|"))return hold("N9_CONSUMPTION_IDENTITY_MISMATCH");
  return {state:"SYNTHETIC_CONTRACT_SHAPE_PASS_ONLY",reason:"NO_REAL_FIELD_OR_N9_ISSUANCE_IMPLIED",consumedRefs:request.fields.map(f=>f.ref)};
}
function runHostileContract() {
  const A={ref:"synthetic:alpha:product-a",hash:"synthetic-hash-a",sourceRoot:"synthetic:alpha:root",sourceFamily:"synthetic-family-alpha",unit:"rule-status",estimand:"rule-existence",population:"synthetic-universe-alpha",time:"synthetic-period-1",place:"synthetic-zone-1",uncertainty:"not-quantified"};
  const B={ref:"synthetic:beta:product-b",hash:"synthetic-hash-b",sourceRoot:"synthetic:beta:root",sourceFamily:"synthetic-family-beta",unit:"institution-count",estimand:"count-at-place",population:"synthetic-universe-beta",time:"synthetic-period-1",place:"synthetic-zone-1",uncertainty:"descriptive-enumeration"};
  const r={mode:"SOURCE_INDEXED_NONPOOLED",claim:"COMPOSED_CONTEXT_ONLY",fields:[deep(A),deep(B)],time:"synthetic-period-1",place:"synthetic-zone-1",ee13Ref:"synthetic:ee13:1",queryRef:"synthetic:n9:query-1",outputRef:"synthetic:n9:output-1",actorUse:false,modelUse:false};
  const auth={producers:{
    [A.ref]:{...A,state:"OWNER_ISSUED",issuerRef:"synthetic:owner:alpha",permissions:["N9_WORLD_CONTEXT"],semanticKind:"EXTERNAL_OBSERVATION"},
    [B.ref]:{...B,state:"OWNER_ISSUED",issuerRef:"synthetic:owner:beta",permissions:["N9_WORLD_CONTEXT"],semanticKind:"STRUCTURAL_RULE_OBSERVATION"}
  },ee13:{["synthetic:ee13:1"]:{state:"OWNER_ISSUED",issuerRef:"synthetic:ee13:issuer",mode:"SOURCE_INDEXED_NONPOOLED",claim:"COMPOSED_CONTEXT_ONLY",productRefs:[A.ref,B.ref],time:r.time,place:r.place}},consumers:{["synthetic:n9:query-1"]:{state:"CONSUMED",ownerRef:"synthetic:n9:owner",productRefs:[A.ref,B.ref],ee13Ref:r.ee13Ref,outputRef:r.outputRef,time:r.time,place:r.place}}};
  const cases=[];
  function check(id,mutate,expected){
    const req=deep(r),trusted=deep(auth);mutate(req,trusted);
    const v=validateTwoFamily(req,trusted);
    if(v.reason!==expected)throw Error("HOSTILE_FAILED "+id+" expected "+expected+" got "+JSON.stringify(v));
    cases.push({id,expected_state:v.state,reason:v.reason,pass:true});
  }
  check("fixture_positive_shape_only",()=>{},"NO_REAL_FIELD_OR_N9_ISSUANCE_IMPLIED");
  check("duplicate_product_as_second_family",(x)=>{x.fields[1]=deep(x.fields[0])},"DUPLICATE_FIELD_PRODUCT");
  check("duplicate_family_under_distinct_product",(x,a)=>{a.producers[B.ref].sourceFamily=A.sourceFamily;x.fields[1].sourceFamily=A.sourceFamily},"DUPLICATE_SOURCE_FAMILY");
  check("cross_sample_pseudo_pooling",(x)=>{x.mode="POOLED_JOINT"},"CROSS_SAMPLE_PSEUDO_POOLING");
  check("forged_source_root",(x)=>{x.fields[0].sourceRoot="synthetic:forged"},"FORGED_OR_UNBOUND_SOURCE_ROOT");
  check("missing_issuer",(x,a)=>{delete a.producers[A.ref].issuerRef},"MISSING_AUTHENTIC_PRODUCER_ISSUER");
  check("missing_ee13_issuer",(x,a)=>{delete a.ee13[x.ee13Ref]},"MISSING_EE13_COMPETENT_ISSUANCE");
  check("fake_ee13_pair",(x,a)=>{a.ee13[x.ee13Ref].productRefs=["synthetic:other",B.ref]},"EE13_PRODUCT_PAIR_NOT_BOUND");
  check("context_into_institution",(x,a)=>{a.producers[A.ref].semanticKind="SURVEY_REPORTED_CONTEXT"},"SUBJECTIVE_CONTEXT_NOT_OBJECTIVE_FIELD");
  check("reported_attitude_as_external_fact",(x,a)=>{a.producers[B.ref].semanticKind="REPORTED_ATTITUDE"},"SUBJECTIVE_CONTEXT_NOT_OBJECTIVE_FIELD");
  check("context_into_cause",(x)=>{x.claim="ACTIVE_CAUSAL"},"CLAIM_WIDENING_NOT_ISSUED");
  check("time_mismatch",(x)=>{x.time="synthetic-period-2"},"WORLD_TIME_PLACE_INCOMPATIBLE");
  check("place_mismatch",(x)=>{x.place="synthetic-zone-2"},"WORLD_TIME_PLACE_INCOMPATIBLE");
  check("missing_uncertainty",(x)=>{x.fields[0].uncertainty=null},"UNCERTAINTY_NOT_CONSERVED");
  check("missing_n9_consumer",(x,a)=>{delete a.consumers[x.queryRef]},"NO_ACTUAL_N9_CONSUMER");
  check("fake_consumer_selected_ref",(x,a)=>{a.consumers[x.queryRef].productRefs=[A.ref,"synthetic:impostor"]},"N9_CONSUMPTION_IDENTITY_MISMATCH");
  check("wrong_estimand",(x)=>{x.fields[1].estimand="population-share"},"UNIT_ESTIMAND_POPULATION_MISMATCH");
  check("same_cross_source_population",(x,a)=>{x.fields[1].population=A.population;a.producers[B.ref].population=A.population},"CROSS_FAMILY_UNIVERSE_REIDENTIFICATION");
  check("permission_removed",(x,a)=>{a.producers[B.ref].permissions=[]},"MISSING_CONSUMER_USE_PERMISSION");
  check("ee13_time_not_qualified",(x,a)=>{a.ee13[x.ee13Ref].time="synthetic-other-period"},"EE13_SCOPE_MISMATCH");
  check("missing_world_output",(x)=>{x.outputRef="synthetic:unconsumed"},"N9_CONSUMPTION_IDENTITY_MISMATCH");
  check("actor_wake",(x)=>{x.actorUse=true},"ACTOR_OR_MODEL_USE_NOT_GRANTED");
  check("model_use_wake",(x)=>{x.modelUse=true},"ACTOR_OR_MODEL_USE_NOT_GRANTED");
  return cases;
}
const results=runHostileContract();
if(results.some(x=>!x.pass))throw Error("D06 synthetic court failed");
console.log(JSON.stringify({contract:"HQ281_D06_SYNTHETIC_SOURCE_FREE_ONLY",checks:results.length,passed:results.length,failed:0,no_real_authority_or_n9:true},null,2));
