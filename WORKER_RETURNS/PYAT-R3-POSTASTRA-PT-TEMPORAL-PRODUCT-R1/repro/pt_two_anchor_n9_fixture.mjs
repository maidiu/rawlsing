// Post-Astra PT: source-free synthetic two-anchor -> N9 values-read contract.
// This is not original source data, not actual weighted survey inference, not an issued EE12 or N9.
function fixtureCompare(a,b,permission){
 const hold=(reason)=>({state:"TEST_ONLY_HELD",reason,n8e_delta:null});
 if(!permission||permission.grade!=="SYNTHETIC_TEST_ONLY"||permission.issued!==true)return hold("NO_EXPLICIT_SYNTHETIC_FIXTURE_GRANT");
 if(!a||!b||a.year>=b.year||a.root===b.root)return hold("TWO_ORDERED_DISTINCT_ANCHORS_REQUIRED");
 if(a.year!==2012||b.year!==2022||a.root!=="SRC02_TEST"||b.root!=="SRC03_TEST")return hold("WRONG_ANCHOR_SCOPE");
 if(!permission.test_ee12||!permission.test_measure_design)return hold("SYNTHETIC_EE12_OR_METHOD_MISSING");
 if(!Array.isArray(a.native_0to4)||!Array.isArray(b.native_0to4)||a.native_0to4.length!==5||b.native_0to4.length!==5)return hold("FULL_FIVE_CATEGORY_NATIVE_TOPOLOGY_REQUIRED");
 if([a,b].some(x=>x.native_0to4.some(v=>!Number.isSafeInteger(v)||v<0)))return hold("INVALID_SYNTHETIC_CELL");
 const ta=a.native_0to4.reduce((s,v)=>s+v,0),tb=b.native_0to4.reduce((s,v)=>s+v,0);
 if(!ta||!tb)return hold("VALID_DENOMINATOR_ZERO__NOT_DELTA_ZERO");
 if([a,b].some(x=>!x.typed_nonresponse||!["dk","refused","missing","not_asked"].every(k=>Object.hasOwn(x.typed_nonresponse,k))))return hold("NATIVE_NONRESPONSE_CHANNELS_MISSING");
 const pa=(a.native_0to4[3]+a.native_0to4[4])/ta,pb=(b.native_0to4[3]+b.native_0to4[4])/tb;
 return {state:"SYNTHETIC_DELTA_ONLY__NOT_GHANA_OBSERVATION",source_ids:[a.root,b.root],native_categories:[a.native_0to4,b.native_0to4],special:[a.typed_nonresponse,b.typed_nonresponse],synthetic_p2012:pa,synthetic_p2022:pb,n8e_delta:pb-pa,design_uncertainty:null,actual_ee12_authority:null};
}

function fixtureN9Read(a,b,c,permission,asof){
 const hold=(reason)=>({state:"TEST_ONLY_N9_HOLD",reason,values_read:null});
 if(!permission||permission.grade!=="SYNTHETIC_TEST_ONLY"||permission.issued!==true||!permission.test_n9)return hold("N9_READ_TARGET_USE_UNISSUED");
 if(!c||c.state!=="SYNTHETIC_DELTA_ONLY__NOT_GHANA_OBSERVATION")return hold("NO_QUALIFIED_SYNTHETIC_INPUT");
 if(asof!=="2024-11-01")return hold("ASOF_NOT_QUALIFIED_FOR_TEST");
 if(c.source_ids[0]!==a.root||c.source_ids[1]!==b.root)return hold("VALUES_READ_DEPENDENCY_SCOPE_MISMATCH");
 return {state:"TEST_ONLY_N9_VALUES_READ__NO_REAL_WORLD",values_read:{source_refs:c.source_ids,native_0to4:[a.native_0to4,b.native_0to4],synthetic_delta:c.n8e_delta},values_read_serialized:JSON.stringify([a.native_0to4,b.native_0to4,c.n8e_delta]),real_n9_receipt:null};
}

function executeFixtureCourt(){
 const make=(p)=>JSON.parse(JSON.stringify(p));
 const x={year:2012,root:"SRC02_TEST",native_0to4:[1,1,2,4,2],typed_nonresponse:{dk:1,refused:0,missing:0,not_asked:0}};
 const y={year:2022,root:"SRC03_TEST",native_0to4:[2,1,1,3,3],typed_nonresponse:{dk:0,refused:1,missing:0,not_asked:0}};
 const grant={grade:"SYNTHETIC_TEST_ONLY",issued:true,test_ee12:true,test_measure_design:true,test_n9:true};
 const outcomes=[];
 const add=(name,pass)=>{outcomes.push({name,pass});if(!pass)throw Error("sourcefree court fails: "+name)};
 const positive=fixtureCompare(x,y,grant);
 add("explicitly synthetic two anchors produce ONLY synthetic result",positive.state==="SYNTHETIC_DELTA_ONLY__NOT_GHANA_OBSERVATION"&&positive.actual_ee12_authority===null);
 add("unissued source permission refuses",fixtureCompare(x,y,null).state==="TEST_ONLY_HELD");
 add("unissued EE12 refuses",fixtureCompare(x,y,{...grant,test_ee12:false}).reason==="SYNTHETIC_EE12_OR_METHOD_MISSING");
 add("unissued measurement method refuses",fixtureCompare(x,y,{...grant,test_measure_design:false}).reason==="SYNTHETIC_EE12_OR_METHOD_MISSING");
 add("cross-section order rejects reversal",fixtureCompare(y,x,grant).reason==="TWO_ORDERED_DISTINCT_ANCHORS_REQUIRED");
 add("same exact source root rejects pseudojoin",fixtureCompare(x,{...y,root:x.root},grant).reason==="TWO_ORDERED_DISTINCT_ANCHORS_REQUIRED");
 add("2017 invented middle anchor rejected",fixtureCompare(x,{...y,year:2017},grant).reason==="WRONG_ANCHOR_SCOPE");
 add("native category 0 required",fixtureCompare({...x,native_0to4:[1,2,3,4]},y,grant).reason==="FULL_FIVE_CATEGORY_NATIVE_TOPOLOGY_REQUIRED");
 add("typed DK missing refused",fixtureCompare({...x,typed_nonresponse:{refused:0,missing:0,not_asked:0}},y,grant).reason==="NATIVE_NONRESPONSE_CHANNELS_MISSING");
 add("negative synthetic numerator fails",fixtureCompare(x,{...y,native_0to4:[2,-1,1,3,3]},grant).reason==="INVALID_SYNTHETIC_CELL");
 add("zero support typed not observed no change",fixtureCompare({...x,native_0to4:[0,0,0,0,0]},y,grant).reason==="VALID_DENOMINATOR_ZERO__NOT_DELTA_ZERO");
 const n9=fixtureN9Read(x,y,positive,grant,"2024-11-01");
 add("N9 sourcefree reads both native values not just hashes",n9.state==="TEST_ONLY_N9_VALUES_READ__NO_REAL_WORLD"&&n9.values_read.native_0to4.length===2&&n9.real_n9_receipt===null);
 add("N9 without permission refuses",fixtureN9Read(x,y,positive,{...grant,test_n9:false},"2024-11-01").reason==="N9_READ_TARGET_USE_UNISSUED");
 add("N9 asof before announced release refuses",fixtureN9Read(x,y,positive,grant,"2022-01-01").reason==="ASOF_NOT_QUALIFIED_FOR_TEST");
 add("N9 without comparison refuses",fixtureN9Read(x,y,{state:"TEST_ONLY_HELD"},grant,"2024-11-01").reason==="NO_QUALIFIED_SYNTHETIC_INPUT");
 const altered=make(y);altered.native_0to4[3]+=1;
 const comparison2=fixtureCompare(x,altered,grant),changed=fixtureN9Read(x,altered,comparison2,grant,"2024-11-01");
 add("one-wave perturbation changes mock comparator and values-read",comparison2.n8e_delta!==positive.n8e_delta&&changed.values_read_serialized!==n9.values_read_serialized);
 add("unchanged wave anchor retained under other-wave perturbation",comparison2.native_categories[0].join(",")===positive.native_categories[0].join(","));
 add("fake actual world still null",positive.design_uncertainty===null&&n9.real_n9_receipt===null);
 return {test_grade:"V8_EXECUTED_SOURCEFREE_FIXTURE_ONLY",executed:outcomes.length,passed:outcomes.filter(o=>o.pass).length,failed:outcomes.filter(o=>!o.pass).length,tests:outcomes,real_source_reads:0,real_ee12_grants:0,real_n8e_products:0,real_n9_receipts:0};
}

const verdict=executeFixtureCourt();
process.stdout.write(JSON.stringify(verdict,null,2)+'\n');
if(verdict.failed)process.exitCode=1;
