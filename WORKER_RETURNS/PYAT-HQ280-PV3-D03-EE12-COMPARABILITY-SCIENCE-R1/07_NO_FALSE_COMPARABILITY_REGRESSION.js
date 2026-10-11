"use strict";
// SOURCE-FREE decision-policy test ONLY; not a Rawlsing owner test and no raw surveys.
// node 07_NO_FALSE_COMPARABILITY_REGRESSION.js
const assert=require("node:assert/strict");
const base={original:true,release:true,meaning:true,form:true,population:true,
nationalSelector:true,risk:true,design:true,estimand:true,products:true,
pairIssuer:true,useIssuer:true,preSelected:true,consumer:true};
function decide(s) {
 if (s.provenMismatch && s.competentNegative) return "SCIENTIFIC_NONCOMPARABLE_SPECIFIC_USE";
 if (s.provenMismatch) return "HELD_SCIENTIFIC_ADJUDICATION";
 if (["original","release","meaning","form","population","nationalSelector","risk","design","estimand"].some(k=>!s[k]))
   return "HELD_ORIGINAL_SCIENCE";
 if (!s.products) return "HELD_MEASURED_WAVE_PRODUCTS";
 if (!s.pairIssuer||!s.useIssuer) return "HELD_EE12_ISSUANCE";
 if (!s.preSelected) return "HELD_POST_RESULT_SELECTION";
 if (!s.consumer) return "HELD_CONSUMER";
 return "PREEXECUTION_READY_NOT_A_MEASURED_RESULT";
}
const cases=[
 ["positive-contract-only",{},"PREEXECUTION_READY_NOT_A_MEASURED_RESULT"],
 ["fielded-q-absent",{original:false},"HELD_ORIGINAL_SCIENCE"],
 ["version-unproved",{release:false},"HELD_ORIGINAL_SCIENCE"],
 ["different-numeric-target",{meaning:false},"HELD_ORIGINAL_SCIENCE"],
 ["changed-card-read",{form:false},"HELD_ORIGINAL_SCIENCE"],
 ["wrong-country",{population:false},"HELD_ORIGINAL_SCIENCE"],
 ["national-boost-leak",{nationalSelector:false},"HELD_ORIGINAL_SCIENCE"],
 ["proxy-or-notasked",{risk:false},"HELD_ORIGINAL_SCIENCE"],
 ["missing-psu-weight",{design:false},"HELD_ORIGINAL_SCIENCE"],
 ["wrong-estimand",{estimand:false},"HELD_ORIGINAL_SCIENCE"],
 ["zero-products",{products:false},"HELD_MEASURED_WAVE_PRODUCTS"],
 ["no-EE12",{pairIssuer:false},"HELD_EE12_ISSUANCE"],
 ["no-temporal-use",{useIssuer:false},"HELD_EE12_ISSUANCE"],
 ["post-result",{preSelected:false},"HELD_POST_RESULT_SELECTION"],
 ["no-world-consumer",{consumer:false},"HELD_CONSUMER"],
 ["proven-break-without-issuer",{provenMismatch:true},"HELD_SCIENTIFIC_ADJUDICATION"],
 ["proven-break-with-issuer",{provenMismatch:true,competentNegative:true},"SCIENTIFIC_NONCOMPARABLE_SPECIFIC_USE"]
];
for(const [name,mod,expected] of cases){
 const actual=decide({...base,...mod});
 assert.equal(actual,expected,name);
 console.log("PASS",name,actual);
}
console.log("SOURCEFREE_DOCUMENTARY_POLICY_FIXTURE",cases.length,"PASS");
