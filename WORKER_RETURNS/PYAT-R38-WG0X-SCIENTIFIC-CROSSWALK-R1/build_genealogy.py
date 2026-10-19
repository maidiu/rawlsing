import ast,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
M=json.loads((R/'evidence/source_manifest.json').read_text())
nodes=[
 ('V550_MAPPED_WORKLIST','sources/v550_worklist.py','_build_question_list','EXISTING_GENERATOR_MISSING_WITNESS','Mapped scope/mapping inner join and explicit budget. Existing selected worklist, not complete administered inventory proof.'),
 ('V550J_COMMISSION','sources/v550j_patterns.py','_validate_bounded_authority_registry','SOURCE_OR_OPERATION_HELD','Requires governed source configurations, exact adjudication and P2 lineage; discovery evidence alone does not grant response portability.'),
 ('V550J_OPERATOR','sources/v550j_joint_operator.py','compile_v550j_family_tables','EXISTING_GENERATOR_MISSING_WITNESS','Produces governed joint response patterns, item/position/relation/boundary indices and association surfaces; no automatic all35 modern-source enrollment proved.'),
 ('MODERN_CATALOG','native/rawlsing_next/pre553_carrier_execution.py','RuntimeObjectCatalog','MISSING_AUTHORITY_BINDING','Materializes supplied exact preimages and validates authority closure. Does not issue original source/item/operation enrollment.'),
 ('ROUTE_B_REQUEST','native/rawlsing_next/pre553_route_b_production.py','I03ExecutionRequest','EXISTING_GENERATOR_MISSING_WITNESS','Exact query/predicate pair; caller supplies qualified list.'),
 ('ROUTE_B_OWNER','native/rawlsing_next/pre553_route_b_production.py','execute_route_b_production','EXISTING_GENERATOR_MISSING_WITNESS','Existing C11 -> supplied requests and discovery -> I03/I05 graph and exact replay.'),
 ('I03','native/rawlsing_next/pre553_empirical_query.py','execute_empirical_query','EXISTING_GENERATOR_MISSING_WITNESS','Executes already qualified exact query and predicate; does not choose original target/routing/design semantics.'),
 ('I05_GRAMMAR','native/rawlsing_next/pre553_discovery_exact.py','_compile_frontier','EXISTING_GENERATOR_MISSING_WITNESS','Genuine finite grammar builder from authorized atoms/templates/rules; declared-frontier completeness is separate from full source jurisdiction.'),
 ('I05_EXECUTION','native/rawlsing_next/pre553_discovery_exact.py','execute_exact_bounded_discovery','EXISTING_GENERATOR_MISSING_WITNESS','Enumerates first, then evaluates candidates with typed outcomes.'),
 ('BATCH_MANIFEST','native/rawlsing_next/pre553_batch_runner.py','BatchManifest','EXISTING_GENERATOR_MISSING_WITNESS','Immutable units and deduplication; upstream anti-join must detect duplicated or omitted declarations before deduplication.'),
 ('BATCH_RUNNER','native/rawlsing_next/pre553_batch_runner.py','BatchExecutionRunner','EXISTING_GENERATOR_MISSING_WITNESS','Existing exact immutable scheduling and resume; prepared-list completion is only that list.'),
 ('P10_SCIENTIFIC_FIXTURE_COMPILER','sources/WG0P10_repaired_workload.py','build_executable_plan','EXISTING_GENERATOR_MISSING_WITNESS','Existing item/op/role/risk-aware TEST_ONLY compiler with independently frozen fixture inventories and FixtureOwner. Not an original35 source-semantic issuer.'),
 ('R37_CATALOG_TRANSPORT','reused_wg0r_fixture.py','enumerate_requests','EXISTING_GENERATOR_MISSING_WITNESS','Existing native query catalog -> request transport reused byte-exactly; no replacement adapter authored.'),
 ('R37_BATCH_AND_CONSUMER','reused_wg0r_fixture.py','run','EXISTING_GENERATOR_MISSING_WITNESS','Existing test-only request/discovery -> Batch -> M1 positive and held consumer path freshly replayed here.'),
 ('M1_CONSUMER','native/rawlsing_next/pre553_learned_empirical_adjudication.py','adjudicate_learned_empirical','SOURCE_OR_OPERATION_HELD','Rule-qualified empirical disposition; UNKNOWN premise remains unresolved. No source-wide or actor adoption follows.')]
out=[]
for name,path,function,classification,finding in nodes:
 p=R/path;tree=ast.parse(p.read_text());matches=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==function]
 assert len(matches)==1,(path,function,len(matches))
 n=matches[0];meta=next(x for x in M if x.get('retained_path')==path)
 out.append(dict(id=name,local_path=path,function=function,start_line=n.lineno,end_line=n.end_lineno,classification=classification,finding=finding,source=meta))
r=dict(schema='WG0X_PRODUCER_GENEALOGY@1',nodes=out,overall='MISSING_AUTHORITY_BINDING__NOT_PROVED_MISSING_GRAMMAR_OR_GENERATOR',missing_adapter='NOT_ESTABLISHED_AT_INSPECTED_SOURCEFREE_NATIVE_CONTRACTS',missing_grammar_or_generator='NOT_ESTABLISHED',new_native_bridge='NOT_AUTHORED__EXISTING_TRANSPORT_REUSED',search_limit='Exact named V550/J, P10/P11, WG0R, Route B/I03/I05/Batch/M1 owners at pinned cuts; not an exhaustive proof of global absence or all35 original jurisdiction.')
(R/'02_PRODUCER_GENEALOGY.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(dict(nodes=len(out),overall=r['overall'])))
