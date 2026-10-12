// PYAT HQ281 D06 R2 -- TEST-ONLY, all fixture authorities synthetic.
// No source science, Field Forge, EE13 issuance, CURRENT selection, N9 runtime, or model-use established.
// Run: node repro/run_d06_source_free_contract_v2.mjs
const copy=x=>JSON.parse(JSON.stringify(x));
function validateR2(r,t){
 const hold=(reason)=>({state:"HELD",reason});
 if(!r||!Array.isArray(r.fields)||r.fields.length!==2)return hold("TWO_FIELDS_REQUIRED");
 if(r.mode!=="SOURCE_INDEXED_NONPOOLED"||r.respondentJoin||r.pooling)return hold("FALSE_CROSS_SOURCE_POOLING");
 if(r.requestedUse!=="WORLD_CONTEXT"||r.causalUse||r.actorUse||r.modelUse)return hold("UNAUTHORIZED_USE_OR_CAUSAL_INFERENCE");
 if(!r.ee13Ref||!r.n9QueryRef||!r.outputRef||!r.worldScopeRef||!r.selectionRef)return hold("WORLD_DEMAND_INCOMPLETE");
 const picks=[], seen=new Set();
 for(const field of r.fields){
   if(!field||!field.productRef||seen.has(field.productRef))return hold("DUPLICATE_FIELD_REF");
   seen.add(field.productRef);
   const source=t.products[field.productRef];
   if(!source||source.state!=="ISSUED_AUTHENTICATED"||!source.issuerRef)return hold("PRODUCT_OR_ISSUER_NOT_AUTHENTICATED");
   const issuer=t.authorities[source.issuerRef];
   if(!issuer||issuer.status!=="COMPETENT_ISSUED"||!issuer.roles.includes("EXTERNAL_FIELD_PRODUCER"))return hold("FIELD_PRODUCER_ISSUER_NOT_COMPETENT");
   const keys=["productRef","productHash","sourceFamily","sourceRootRef","originCustodyRef","sourceUniverseRef","targetPopulationRef","unit","estimandRef","timeScopeRef","placeScopeRef","uncertaintyState","semanticKind"];
   for(const k of keys){
     if(!source[k]||field[k]!==source[k])return hold("FORGED_OR_UNBOUND_FIELD_IDENTITY_"+k.toUpperCase());
   }
   if(!["EXTERNAL_INSTITUTIONAL_OBSERVATION","OWNER_AUTHENTICATED_STRUCTURAL_RULE_FIELD"].includes(source.semanticKind))return hold("SUBJECTIVE_OR_DOCUMENTARY_NOT_OBJECTIVE");
   if(!Array.isArray(source.allowedUses)||!source.allowedUses.includes("WORLD_CONTEXT"))return hold("NO_PRODUCER_WORLD_CONTEXT_PERMISSION");
   picks.push(source);
 }
 if(picks[0].sourceFamily===picks[1].sourceFamily)return hold("SAME_FAMILY_MASQUERADING_AS_TWO");
 if(picks[0].sourceRootRef===picks[1].sourceRootRef||picks[0].originCustodyRef===picks[1].originCustodyRef||picks[0].sourceUniverseRef===picks[1].sourceUniverseRef)return hold("NONINDEPENDENT_OR_DUPLICATE_SOURCE_ROOT");
 // The *target population* may legitimately be the same; source-specific universes remain distinct.
 // The *source time/place* may legitimately differ. Only a competent EE13 owner can issue compatibility.
 const compose=t.ee13[r.ee13Ref];
 if(!compose||compose.state!=="OWNER_ISSUED"||!compose.issuerRef)return hold("MISSING_COMPETENT_EE13");
 const eeIssuer=t.authorities[compose.issuerRef];
 if(!eeIssuer||eeIssuer.status!=="COMPETENT_ISSUED"||!eeIssuer.roles.includes("EE13_N7_COMPOSITION"))return hold("EE13_ISSUER_NOT_COMPETENT");
 if(compose.mode!=="SOURCE_INDEXED_NONPOOLED"||compose.permission!=="WORLD_CONTEXT"||compose.compatibility!=="EXPLICIT_BOUND_SCOPE"||compose.worldScopeRef!==r.worldScopeRef)return hold("EE13_SCOPE_OR_PERMISSION_MISMATCH");
 if(!Array.isArray(compose.boundFieldRefs)||compose.boundFieldRefs.length!==2||compose.boundFieldRefs.slice().sort().join("|")!==picks.map(x=>x.productRef).sort().join("|"))return hold("EE13_NOT_BOUND_TO_EXACT_PRODUCT_PAIR");
 if(!Array.isArray(compose.boundFieldScopes)||compose.boundFieldScopes.length!==2)return hold("EE13_ORIGINAL_SCOPE_BINDINGS_MISSING");
 for(const source of picks){
   const b=compose.boundFieldScopes.find(x=>x.productRef===source.productRef);
   if(!b||!["sourceUniverseRef","timeScopeRef","placeScopeRef","estimandRef","uncertaintyState","unit"].every(k=>b[k]===source[k]))return hold("EE13_ORIGINAL_SCOPE_BINDING_MISMATCH");
 }
 // No EQ/source-universe equality imposed, no invented joint respondents, no default "same epoch".
 const sel=t.selections[r.selectionRef];
 if(!sel||sel.issuerRef===undefined||!["CURRENT_ISSUED","AS_OF_ISSUED"].includes(sel.state)||sel.worldScopeRef!==r.worldScopeRef||sel.ee13Ref!==r.ee13Ref)return hold("MISSING_SELECTED_WORLD_CURRENTNESS");
 const selIssuer=t.authorities[sel.issuerRef];
 if(!selIssuer||selIssuer.status!=="COMPETENT_ISSUED"||!selIssuer.roles.includes("N9_WORLD_SELECTION"))return hold("WORLD_SELECTION_ISSUER_NOT_COMPETENT");
 const n9=t.n9[r.n9QueryRef];
 if(!n9||n9.state!=="ACTUALLY_CONSUMED"||!n9.issuerRef||!n9.outputRef)return hold("NO_ACTUAL_N9_TWO_FIELD_CONSUMER");
 const n9Issuer=t.authorities[n9.issuerRef];
 if(!n9Issuer||n9Issuer.status!=="COMPETENT_ISSUED"||!n9Issuer.roles.includes("N9_TERMINAL_CONSUMER"))return hold("N9_CONSUMER_ISSUER_NOT_COMPETENT");
 if(n9.queryRef!==r.n9QueryRef||n9.outputRef!==r.outputRef||n9.worldScopeRef!==r.worldScopeRef||n9.ee13Ref!==r.ee13Ref||n9.selectionRef!==r.selectionRef)return hold("N9_QUERY_OUTPUT_CLOSURE_MISMATCH");
 if(!Array.isArray(n9.consumedFieldRefs)||n9.consumedFieldRefs.length!==2||n9.consumedFieldRefs.slice().sort().join("|")!==picks.map(x=>x.productRef).sort().join("|"))return hold("N9_FAILED_TO_CONSUME_BOTH");
 if(n9.sourceIndexed!==true||n9.pooled!==false||n9.permission!=="WORLD_CONTEXT")return hold("N9_SCOPE_OR_POOLING_WIDENED");
 return {state:"SYNTHETIC_CONTRACT_SHAPE_PASS_ONLY",reason:"REAL_PRODUCER_ISSUANCE_AND_N9_RUNTIME_NOT_VERIFIED",refs:picks.map(x=>x.productRef)};
}
function fixtureR2(){
 const A={productRef:"fixture:objfield:alpha",productHash:"a".repeat(64),sourceFamily:"SYNTHETIC_FAMILY_A",sourceRootRef:"fixture:root:a",originCustodyRef:"fixture:origin:a",sourceUniverseRef:"fixture:sample:a",targetPopulationRef:"fixture:population:ghana",unit:"rule-presence",estimandRef:"fixture:estimand:legal-status",timeScopeRef:"fixture:period:2000",placeScopeRef:"fixture:ghana",uncertaintyState:"NOT_QUANTIFIED",semanticKind:"OWNER_AUTHENTICATED_STRUCTURAL_RULE_FIELD",allowedUses:["WORLD_CONTEXT"],issuerRef:"fixture:authority:prodA",state:"ISSUED_AUTHENTICATED"};
 const B={productRef:"fixture:objfield:beta",productHash:"b".repeat(64),sourceFamily:"SYNTHETIC_FAMILY_B",sourceRootRef:"fixture:root:b",originCustodyRef:"fixture:origin:b",sourceUniverseRef:"fixture:sample:b",targetPopulationRef:"fixture:population:ghana",unit:"facility-count",estimandRef:"fixture:estimand:facilities",timeScopeRef:"fixture:period:2001",placeScopeRef:"fixture:ghana-north",uncertaintyState:"DESCRIPTIVE_ONLY",semanticKind:"EXTERNAL_INSTITUTIONAL_OBSERVATION",allowedUses:["WORLD_CONTEXT"],issuerRef:"fixture:authority:prodB",state:"ISSUED_AUTHENTICATED"};
 const field=x=>({productRef:x.productRef,productHash:x.productHash,sourceFamily:x.sourceFamily,sourceRootRef:x.sourceRootRef,originCustodyRef:x.originCustodyRef,sourceUniverseRef:x.sourceUniverseRef,targetPopulationRef:x.targetPopulationRef,unit:x.unit,estimandRef:x.estimandRef,timeScopeRef:x.timeScopeRef,placeScopeRef:x.placeScopeRef,uncertaintyState:x.uncertaintyState,semanticKind:x.semanticKind});
 const scope=x=>({productRef:x.productRef,sourceUniverseRef:x.sourceUniverseRef,timeScopeRef:x.timeScopeRef,placeScopeRef:x.placeScopeRef,estimandRef:x.estimandRef,uncertaintyState:x.uncertaintyState,unit:x.unit});
 const r={fields:[field(A),field(B)],mode:"SOURCE_INDEXED_NONPOOLED",respondentJoin:false,pooling:false,requestedUse:"WORLD_CONTEXT",causalUse:false,actorUse:false,modelUse:false,worldScopeRef:"fixture:world:ghana:historical-scope",ee13Ref:"fixture:ee13:r1",selectionRef:"fixture:selection:asof",n9QueryRef:"fixture:n9:query",outputRef:"fixture:n9:output"};
 const t={authorities:{
   "fixture:authority:prodA":{status:"COMPETENT_ISSUED",roles:["EXTERNAL_FIELD_PRODUCER"]},
   "fixture:authority:prodB":{status:"COMPETENT_ISSUED",roles:["EXTERNAL_FIELD_PRODUCER"]},
   "fixture:authority:ee13":{status:"COMPETENT_ISSUED",roles:["EE13_N7_COMPOSITION"]},
   "fixture:authority:selection":{status:"COMPETENT_ISSUED",roles:["N9_WORLD_SELECTION"]},
   "fixture:authority:n9":{status:"COMPETENT_ISSUED",roles:["N9_TERMINAL_CONSUMER"]}
  },products:{[A.productRef]:A,[B.productRef]:B},
  ee13:{[r.ee13Ref]:{state:"OWNER_ISSUED",issuerRef:"fixture:authority:ee13",mode:r.mode,permission:r.requestedUse,compatibility:"EXPLICIT_BOUND_SCOPE",worldScopeRef:r.worldScopeRef,boundFieldRefs:[A.productRef,B.productRef],boundFieldScopes:[scope(A),scope(B)]}},
  selections:{[r.selectionRef]:{state:"AS_OF_ISSUED",issuerRef:"fixture:authority:selection",worldScopeRef:r.worldScopeRef,ee13Ref:r.ee13Ref}},
  n9:{[r.n9QueryRef]:{state:"ACTUALLY_CONSUMED",issuerRef:"fixture:authority:n9",queryRef:r.n9QueryRef,outputRef:r.outputRef,worldScopeRef:r.worldScopeRef,ee13Ref:r.ee13Ref,selectionRef:r.selectionRef,sourceIndexed:true,pooled:false,permission:"WORLD_CONTEXT",consumedFieldRefs:[A.productRef,B.productRef]}}
 };
 return [r,t];
}
function runR2(){
 const [base,trs]=fixtureR2(), cases=[];
 const scenario=(id,fn,expect)=>{
   const r=copy(base),t=copy(trs);fn(r,t);
   const a=validateR2(r,t);
   if(a.reason!==expect)throw new Error(`CASE ${id}: expected ${expect}, got ${JSON.stringify(a)}`);
   cases.push({id,result:a.state,reason:a.reason,pass:true});
 };
 const ok="REAL_PRODUCER_ISSUANCE_AND_N9_RUNTIME_NOT_VERIFIED";
 scenario("positive_synthetic_same_named_population_different_scopes",(r,t)=>{},ok);
 scenario("same_population_allowed_but_distinct_samples_required",(r,t)=>{r.fields[1].targetPopulationRef=r.fields[0].targetPopulationRef},ok);
 scenario("different_time_and_place_allowed_only_with_issuer",(r,t)=>{},ok);
 scenario("duplicate_product",(r,t)=>{r.fields[1]=copy(r.fields[0])},"DUPLICATE_FIELD_REF");
 scenario("duplicate_family",(r,t)=>{r.fields[1].sourceFamily=r.fields[0].sourceFamily;t.products["fixture:objfield:beta"].sourceFamily=r.fields[0].sourceFamily},"SAME_FAMILY_MASQUERADING_AS_TWO");
 scenario("two_labels_one_underlying_custody",(r,t)=>{r.fields[1].originCustodyRef=r.fields[0].originCustodyRef;t.products["fixture:objfield:beta"].originCustodyRef=r.fields[0].originCustodyRef},"NONINDEPENDENT_OR_DUPLICATE_SOURCE_ROOT");
 scenario("two_families_one_source_root",(r,t)=>{r.fields[1].sourceRootRef=r.fields[0].sourceRootRef;t.products["fixture:objfield:beta"].sourceRootRef=r.fields[0].sourceRootRef},"NONINDEPENDENT_OR_DUPLICATE_SOURCE_ROOT");
 scenario("one_sample_pseudojoin",(r,t)=>{r.respondentJoin=true},"FALSE_CROSS_SOURCE_POOLING");
 scenario("pooled_mode",(r,t)=>{r.mode="AUTHORIZED_COMPOSITE"},"FALSE_CROSS_SOURCE_POOLING");
 scenario("forged_source_root",(r,t)=>{r.fields[0].sourceRootRef="fixture:forge"},"FORGED_OR_UNBOUND_FIELD_IDENTITY_SOURCEROOTREF");
 scenario("forged_hash",(r,t)=>{r.fields[0].productHash="f".repeat(64)},"FORGED_OR_UNBOUND_FIELD_IDENTITY_PRODUCTHASH");
 scenario("missing_producer_issuer",(r,t)=>{delete t.products["fixture:objfield:beta"].issuerRef},"PRODUCT_OR_ISSUER_NOT_AUTHENTICATED");
 scenario("fake_producer_issuer",(r,t)=>{t.authorities["fixture:authority:prodB"].roles=[]},"FIELD_PRODUCER_ISSUER_NOT_COMPETENT");
 scenario("unissued_field",(r,t)=>{t.products["fixture:objfield:alpha"].state="CANDIDATE"},"PRODUCT_OR_ISSUER_NOT_AUTHENTICATED");
 scenario("subjective_context_to_institution",(r,t)=>{r.fields[0].semanticKind="SURVEY_CONTEXT";t.products["fixture:objfield:alpha"].semanticKind="SURVEY_CONTEXT"},"SUBJECTIVE_OR_DOCUMENTARY_NOT_OBJECTIVE");
 scenario("official_legal_text_without_field_producer",(r,t)=>{r.fields[0].semanticKind="LEGAL_DOCUMENT";t.products["fixture:objfield:alpha"].semanticKind="LEGAL_DOCUMENT"},"SUBJECTIVE_OR_DOCUMENTARY_NOT_OBJECTIVE");
 scenario("external_survey_judgment_to_structural",(r,t)=>{r.fields[1].semanticKind="REPORTED_ATTITUDE";t.products["fixture:objfield:beta"].semanticKind="REPORTED_ATTITUDE"},"SUBJECTIVE_OR_DOCUMENTARY_NOT_OBJECTIVE");
 scenario("causal_overclaim",(r,t)=>{r.causalUse=true},"UNAUTHORIZED_USE_OR_CAUSAL_INFERENCE");
 scenario("actor_overclaim",(r,t)=>{r.actorUse=true},"UNAUTHORIZED_USE_OR_CAUSAL_INFERENCE");
 scenario("model_use_overclaim",(r,t)=>{r.modelUse=true},"UNAUTHORIZED_USE_OR_CAUSAL_INFERENCE");
 scenario("producer_use_not_authorized",(r,t)=>{t.products["fixture:objfield:alpha"].allowedUses=[]},"NO_PRODUCER_WORLD_CONTEXT_PERMISSION");
 scenario("uncertainty_stripped",(r,t)=>{r.fields[0].uncertaintyState=""},"FORGED_OR_UNBOUND_FIELD_IDENTITY_UNCERTAINTYSTATE");
 scenario("estimand_identity_corrupted",(r,t)=>{r.fields[1].estimandRef="fixture:impostor"},"FORGED_OR_UNBOUND_FIELD_IDENTITY_ESTIMANDREF");
 scenario("source_time_forgery",(r,t)=>{r.fields[0].timeScopeRef="fixture:period:2026"},"FORGED_OR_UNBOUND_FIELD_IDENTITY_TIMESCOPEREF");
 scenario("source_place_forgery",(r,t)=>{r.fields[0].placeScopeRef="fixture:other-country"},"FORGED_OR_UNBOUND_FIELD_IDENTITY_PLACESCOPEREF");
 scenario("original_universe_reidentified",(r,t)=>{r.fields[1].sourceUniverseRef=r.fields[0].sourceUniverseRef;t.products["fixture:objfield:beta"].sourceUniverseRef=r.fields[0].sourceUniverseRef},"NONINDEPENDENT_OR_DUPLICATE_SOURCE_ROOT");
 scenario("missing_ee13_issuer",(r,t)=>{delete t.ee13[r.ee13Ref]},"MISSING_COMPETENT_EE13");
 scenario("ee13_issuer_not_competent",(r,t)=>{t.authorities["fixture:authority:ee13"].roles=[]},"EE13_ISSUER_NOT_COMPETENT");
 scenario("ee13_fake_pair",(r,t)=>{t.ee13[r.ee13Ref].boundFieldRefs[1]="fixture:other"},"EE13_NOT_BOUND_TO_EXACT_PRODUCT_PAIR");
 scenario("ee13_compatibility_held",(r,t)=>{t.ee13[r.ee13Ref].compatibility="UNKNOWN"},"EE13_SCOPE_OR_PERMISSION_MISMATCH");
 scenario("ee13_scope_binding_time_wrong",(r,t)=>{t.ee13[r.ee13Ref].boundFieldScopes[0].timeScopeRef="fixture:period:1998"},"EE13_ORIGINAL_SCOPE_BINDING_MISMATCH");
 scenario("ee13_world_scope_wrong",(r,t)=>{r.worldScopeRef="fixture:wrong-world"},"EE13_SCOPE_OR_PERMISSION_MISMATCH");
 scenario("world_selection_absent",(r,t)=>{delete t.selections[r.selectionRef]},"MISSING_SELECTED_WORLD_CURRENTNESS");
 scenario("selection_issuer_not_competent",(r,t)=>{t.authorities["fixture:authority:selection"].roles=[]},"WORLD_SELECTION_ISSUER_NOT_COMPETENT");
 scenario("missing_actual_consumer",(r,t)=>{delete t.n9[r.n9QueryRef]},"NO_ACTUAL_N9_TWO_FIELD_CONSUMER");
 scenario("consumer_not_actually_run",(r,t)=>{t.n9[r.n9QueryRef].state="CONTRACT_ONLY"},"NO_ACTUAL_N9_TWO_FIELD_CONSUMER");
 scenario("n9_issuer_not_competent",(r,t)=>{t.authorities["fixture:authority:n9"].roles=[]},"N9_CONSUMER_ISSUER_NOT_COMPETENT");
 scenario("n9_dropped_second_field",(r,t)=>{t.n9[r.n9QueryRef].consumedFieldRefs.pop()},"N9_FAILED_TO_CONSUME_BOTH");
 scenario("n9_output_forgery",(r,t)=>{r.outputRef="fixture:fake-output"},"N9_QUERY_OUTPUT_CLOSURE_MISMATCH");
 scenario("n9_pooled_consumption",(r,t)=>{t.n9[r.n9QueryRef].pooled=true},"N9_SCOPE_OR_POOLING_WIDENED");
 return cases;
}
const checks=runR2();
console.log(JSON.stringify({schema:"PYAT_HQ281_D06_SOURCE_FREE_R2",synthetic:true,kind:"TEST_ONLY",checked:checks.length,passed:checks.length,failed:0,actual_n9:false,real_issuer:false},null,2));
