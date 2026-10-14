/** U04 sourcefree no-data mock court. No signature or real E_pre is made; all accepted=false.\n * Run: node WORKER_RETURNS/PYAT-R3-HQ295-U04-PRE-RESULT-EXPECTED-CUSTODY-R1/repro/sourcefree_multiset_court.mjs\n * This is NOT an independent signature/timestamp validator. */
function audit(c,w){
  const refuse=(reason)=>({grade:"MOCK_SOURCEFREE_ONLY",accepted:false,reason});
  if(!w||w.testWitness!==true)return refuse("INDEPENDENT_WITNESS_MISSING");
  if(!w.issuerDelegationEffective||w.issuerDelegationEffective>w.sealOrder)return refuse("DELEGATION_NOT_EFFECTIVE_AT_SEAL");
  if(w.custodian===w.author||w.custodian===w.operationIssuer||w.custodian===w.executor)return refuse("SELF_CUSTODY_REFUSED");
  if(!w.custodianDistinctAuthenticated)return refuse("EXTERNAL_ISSUER_OR_AUTHENTICATION_UNPROVED");
  if(!Number.isSafeInteger(w.sealOrder)||!Number.isSafeInteger(w.firstDOrder)||!Number.isSafeInteger(w.firstResultOrder)||w.sealOrder>=w.firstDOrder||w.sealOrder>=w.firstResultOrder)return refuse("INDEPENDENT_PRE_RESULT_ORDER_FAILED");
  if(c.derivedFromD||c.derivedFromResult)return refuse("RESULT_OR_D_DERIVED_E_REFUSED");
  if(c.replacedSameSealIdentity)return refuse("POST_SEAL_REWRITE_REFUSED");
  if(c.claimedOriginal.join("|")!==w.originalRoster.join("|"))return refuse("ORIGINAL_U_MISSING_OR_CHANGED");
  const normalize=(a)=>a.map(x=>[x.key,x.disposition,x.multiplicity].join("::")).sort().join("|");
  if(normalize(c.claimedOperations)!==normalize(w.operationRoster))return refuse("ISSUED_OPERATION_CLOSURE_MISMATCH");
  for(const op of w.operationRoster){
    if(!op.needs.every(id=>w.originalRoster.includes(id)))return refuse("O_HAS_NO_ORIGINAL_ITEM_WARRANT");
    if(op.disposition==="SOURCE_INTRINSIC_NA"&&!op.sourceNativeNAProof)return refuse("NA_WITHOUT_SOURCE_PROOF");
    if(!["PERMITTED","HELD","DENIED","SOURCE_INTRINSIC_NA"].includes(op.disposition))return refuse("ILLEGAL_DECISION_STATE");
  }
  if(normalize(c.expected)!==normalize(w.operationRoster))return refuse("E_PRE_MULTISET_OMISSION_OR_ADDITION");
  const runnable=w.operationRoster.filter(x=>x.disposition==="PERMITTED").map(x=>x.key).sort().join("|");
  if(c.D.slice().sort().join("|")!==runnable)return refuse("D_PERMITTED_ONLY_JOIN_MISMATCH");
  return {grade:"MOCK_SOURCEFREE_ONLY",accepted:false,reason:"DOCUMENTARY_NO_DATA_MOCK_RECONCILIATION_OK__NEVER_E_PRE"};
}
function run(){
  const U=["COUNTRY_FORM:Q86A","COUNTRY_FORM:Q86B"];
  const O=[
  {key:"GT1:Q86A",disposition:"HELD",multiplicity:1,needs:[U[0]]},
  {key:"GT2:Q86B>Q86A",disposition:"PERMITTED",multiplicity:1,needs:U},
  {key:"J_ONLY:Q86B>Q86A",disposition:"HELD",multiplicity:1,needs:U},
  {key:"OTHER:DENIED",disposition:"DENIED",multiplicity:1,needs:U},
  {key:"NA:PROVED",disposition:"SOURCE_INTRINSIC_NA",multiplicity:1,needs:U,sourceNativeNAProof:"FAKE_TEST_WARRANT"}
  ];
  const w={testWitness:true,custodian:"mock_distinct_custodian",author:"mock_U_author",operationIssuer:"mock_O3",executor:"mock_P01",
    custodianDistinctAuthenticated:true,issuerDelegationEffective:1,sealOrder:2,firstDOrder:3,firstResultOrder:4,
    originalRoster:U,operationRoster:O};
  const c={claimedOriginal:U,claimedOperations:O,expected:O,D:["GT2:Q86B>Q86A"],derivedFromD:false,derivedFromResult:false,replacedSameSealIdentity:false};
  const cp=x=>JSON.parse(JSON.stringify(x));
  const tests=[
    ["synthetic_positive_mock_only",cp(c),cp(w),"DOCUMENTARY_NO_DATA_MOCK_RECONCILIATION_OK__NEVER_E_PRE"],
    ["self_sign",cp(c),{...cp(w),custodian:"mock_U_author"},"SELF_CUSTODY_REFUSED"],
    ["result_derived", {...cp(c),derivedFromResult:true},cp(w),"RESULT_OR_D_DERIVED_E_REFUSED"],
    ["D_derived", {...cp(c),derivedFromD:true},cp(w),"RESULT_OR_D_DERIVED_E_REFUSED"],
    ["missing_original_B", {...cp(c),claimedOriginal:[U[0]]},cp(w),"ORIGINAL_U_MISSING_OR_CHANGED"],
    ["missing_J_only", {...cp(c),expected:O.filter(x=>!x.key.startsWith("J_ONLY"))},cp(w),"E_PRE_MULTISET_OMISSION_OR_ADDITION"],
    ["missing_GT1", {...cp(c),expected:O.filter(x=>!x.key.startsWith("GT1"))},cp(w),"E_PRE_MULTISET_OMISSION_OR_ADDITION"],
    ["missing_DENIED", {...cp(c),expected:O.filter(x=>x.disposition!=="DENIED")},cp(w),"E_PRE_MULTISET_OMISSION_OR_ADDITION"],
    ["missing_NA", {...cp(c),expected:O.filter(x=>x.disposition!=="SOURCE_INTRINSIC_NA")},cp(w),"E_PRE_MULTISET_OMISSION_OR_ADDITION"],
    ["backdated_but_real_inclusion_late",cp(c),{...cp(w),sealOrder:5},"INDEPENDENT_PRE_RESULT_ORDER_FAILED"],
    ["later_delegation",cp(c),{...cp(w),issuerDelegationEffective:3},"DELEGATION_NOT_EFFECTIVE_AT_SEAL"],
    ["wrong_untrusted_signer",cp(c),{...cp(w),custodianDistinctAuthenticated:false},"EXTERNAL_ISSUER_OR_AUTHENTICATION_UNPROVED"],
    ["post_seal_rewrite", {...cp(c),replacedSameSealIdentity:true},cp(w),"POST_SEAL_REWRITE_REFUSED"],
    ["unissued_D_job", {...cp(c),D:["GT2:Q86B>Q86A","OTHER:EXTRA"]},cp(w),"D_PERMITTED_ONLY_JOIN_MISMATCH"],
    ["invalid_NA_warrant",cp(c),{...cp(w),operationRoster:O.map(x=>x.key==="NA:PROVED"?{...x,sourceNativeNAProof:null}:x)},"NA_WITHOUT_SOURCE_PROOF"],
    ["no_external_witness",cp(c),null,"INDEPENDENT_WITNESS_MISSING"]
  ];
  const records=tests.map(([name,cc,ww,expect])=>{const got=audit(cc,ww);if(got.reason!==expect||got.accepted!==false)throw Error(name+" expected "+expect+" got "+JSON.stringify(got));return {name,outcome:"MOCK_SOURCEFREE_EXPECTATION_MATCHED",reason:got.reason};});
  return {schema:"U04_SOURCEFREE_MOCK_COURT@1",executed_in:"functions.exec V8 sourcefree, NOT Node subprocess",count:records.length,passed:records.length,records};
}
const report=run();
if(typeof process!=='undefined'&&process.stdout)process.stdout.write(JSON.stringify(report,null,2)+'\n');
