/* Source-free synthetic E01 contract check. Does not load respondent data, source files, or owner runtime.
   Executed in connected orchestration V8 isolate; Node/pytest NOT_EXECUTED. */
const fixture = {
  "class": "SYNTHETIC_SOURCE_FREE_ONLY",
  "pre_result": true,
  "independent_issuer": "SIMULATED_NOT_AUTHENTIC",
  "original": [
    {
      "id": "A@P1",
      "native_item": "A",
      "form": "FORM_ALPHA",
      "respondent": "P1",
      "route": "ASKED"
    },
    {
      "id": "B@P1",
      "native_item": "B",
      "form": "FORM_BETA",
      "respondent": "P1",
      "route": "ASKED"
    },
    {
      "id": "B@P2",
      "native_item": "B",
      "form": "FORM_BETA",
      "respondent": "P2",
      "route": "NOT_ASKED_PROVED"
    }
  ],
  "issued_operations": [
    {
      "id": "A_UNARY",
      "item_ids": [
        "A@P1"
      ],
      "semantic_class": "UNARY_DISTRIBUTION",
      "state": "HELD_P01_CONSUMER_UNSUPPORTED"
    },
    {
      "id": "B_TO_A_J",
      "item_ids": [
        "B@P1",
        "A@P1"
      ],
      "semantic_class": "PAIR_RESPONSE_COTRAVEL",
      "direction": "B->A",
      "state": "RUNNABLE_P01_FF"
    },
    {
      "id": "A_IF_B_C",
      "item_ids": [
        "B@P1",
        "A@P1"
      ],
      "semantic_class": "CONDITIONAL",
      "direction": "B.C->A",
      "state": "HELD_OPERATION_MAPPING"
    }
  ],
  "expected": [
    {
      "id": "A_UNARY",
      "form": "FORM_ALPHA",
      "respondent": "P1",
      "mapping_ref": null,
      "measure": "RAW",
      "design_authority_ref": null
    },
    {
      "id": "B_TO_A_J",
      "form": "FORM_BETA",
      "respondent": "P1",
      "mapping_ref": "SYNTHETIC_MAP_REF",
      "measure": "RAW",
      "design_authority_ref": null
    },
    {
      "id": "A_IF_B_C",
      "form": "FORM_BETA",
      "respondent": "P1",
      "mapping_ref": null,
      "measure": "RAW",
      "design_authority_ref": null
    }
  ],
  "declared": [
    "B_TO_A_J"
  ],
  "outcomes": {
    "B_TO_A_J": "MEASURED_ZERO_OR_POSITIVE"
  }
};
function court(x){
 const bad=[];
 if(x.class!=="SYNTHETIC_SOURCE_FREE_ONLY"||x.independent_issuer!=="SIMULATED_NOT_AUTHENTIC"||!x.pre_result)bad.push("TEST_E_NOT_FROZEN_BEFORE_RESULTS");
 const ops=new Map(x.issued_operations.map(o=>[o.id,o])),ev=new Map(x.expected.map(o=>[o.id,o]));
 const original=new Map(x.original.map(o=>[o.id,o]));
 if(ev.size!==x.expected.length)bad.push("DUPLICATE_E_KEY");
 for(const k of ops.keys())if(!ev.has(k))bad.push("ORIGINAL_TO_E_OMISSION:"+k);
 for(const k of ev.keys())if(!ops.has(k))bad.push("UNISSUED_E_OPERATION:"+k);
 const runnable=x.issued_operations.filter(o=>o.state==="RUNNABLE_P01_FF").map(o=>o.id);
 for(const k of runnable)if(!x.declared.includes(k))bad.push("E_TO_D_OMISSION:"+k);
 for(const k of x.declared)if(!runnable.includes(k))bad.push("D_FOREIGN_OR_HELD:"+k);
 for(const o of x.issued_operations){
  for(const id of o.item_ids)if(!original.has(id))bad.push("ORIGINAL_ITEM_NOT_PRESENT:"+id);
  if(o.state==="RUNNABLE_P01_FF"){
   if(o.semantic_class!=="PAIR_RESPONSE_COTRAVEL"||o.direction!=="B->A")bad.push("P01_SCOPE_UNSUPPORTED:"+o.id);
   if(o.item_ids.some(id=>original.get(id)?.route!=="ASKED"))bad.push("ROUTING_NOT_ESTABLISHED:"+o.id);
  }
  const e=ev.get(o.id);
  if(e){
   const primary=original.get(o.item_ids[0]);
   if(primary&&(e.form!==primary.form||e.respondent!==primary.respondent))bad.push("ORIGINAL_IDENTITY_SCOPE_MISMATCH:"+o.id);
   if(o.state==="RUNNABLE_P01_FF"&&!e.mapping_ref)bad.push("MAPPING_UNRESOLVED:"+o.id);
   if(e.measure==="WEIGHTED"&&!e.design_authority_ref)bad.push("WEIGHT_DESIGN_AUTHORITY_REQUIRED:"+o.id);
  }
 }
 return bad;
};
const tests = [
  ["POSITIVE_J_ONLY_P01_MAPPED_AND_HELD_ACCOUNTED", x=>x, []],
  ["J_ONLY_MISSING_D", x=>{x.declared=[];return x}, ["E_TO_D_OMISSION"]],
  ["ORIGINAL_ITEM_OPERATION_NOT_IN_E", x=>{x.expected.shift();return x}, ["ORIGINAL_TO_E_OMISSION"]],
  ["E_NOT_PROSPECTIVE", x=>{x.pre_result=false;return x}, ["TEST_E_NOT_FROZEN_BEFORE_RESULTS"]],
  ["REVERSE_ASSOCIATION_UNISSUED", x=>{x.declared.push("A_TO_B");return x}, ["D_FOREIGN_OR_HELD"]],
  ["J_ONLY_UNISSUED_E_EXTRA", x=>{x.expected.push({id:"B_UNARY"});return x}, ["UNISSUED_E_OPERATION"]],
  ["HELD_UNARY_DISPATCHED", x=>{x.declared.push("A_UNARY");return x}, ["D_FOREIGN_OR_HELD"]],
  ["HELD_CONDITION_DISPATCHED", x=>{x.declared.push("A_IF_B_C");return x}, ["D_FOREIGN_OR_HELD"]],
  ["ORIGINAL_FORM_REKEY", x=>{x.expected[1].form="FORM_OTHER";return x}, ["ORIGINAL_IDENTITY_SCOPE_MISMATCH"]],
  ["HOUSEHOLD_REKEY_AS_PERSON", x=>{x.expected[1].respondent="H1";return x}, ["ORIGINAL_IDENTITY_SCOPE_MISMATCH"]],
  ["NOT_ASKED_ROUTE_LAUNDERED", x=>{x.original[1].route="NOT_ASKED_PROVED";return x}, ["ROUTING_NOT_ESTABLISHED"]],
  ["MISSING_MAPPING_FALSE_RUNNABLE", x=>{x.expected[1].mapping_ref=null;return x}, ["MAPPING_UNRESOLVED"]],
  ["WEIGHTED_WITHOUT_DESIGN", x=>{x.expected[1].measure="WEIGHTED";return x}, ["WEIGHT_DESIGN_AUTHORITY_REQUIRED"]],
  ["SOURCE_ITEM_MISSING_IN_U", x=>{x.original=x.original.filter(o=>o.id!=="B@P1");return x}, ["ORIGINAL_ITEM_NOT_PRESENT"]],
  ["REKEY_E_BY_OUTPUT_STATUS", x=>{x.expected=x.expected.filter(o=>o.id!=="B_TO_A_J");return x}, ["ORIGINAL_TO_E_OMISSION"]],
  ["DUPLICATED_E_ID", x=>{x.expected.push({...x.expected[1]});return x}, ["DUPLICATE_E_KEY"]]
];
const results = tests.map(([id, mutate, prefixes]) => { const observed = court(mutate(JSON.parse(JSON.stringify(fixture)))); const pass = prefixes.length === 0 ? observed.length === 0 : prefixes.every(p => observed.some(x => x.startsWith(p))); return { id, pass, observed }; });
if (results.some(x => !x.pass)) throw Error('source-free contract discrepancy: ' + JSON.stringify(results.filter(x=>!x.pass)));
console.log(JSON.stringify({ source: 'SYNTHETIC_ONLY', cases: results.length, passed: results.filter(x=>x.pass).length, results }, null, 2));
