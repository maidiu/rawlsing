import pathlib,json,xml.etree.ElementTree as E,collections,hashlib
RET=pathlib.Path(__file__).resolve().parents[1]
def cases(suite):
 out=[]
 for t in E.parse(RET/'repro'/f'{suite}.xml').getroot().iter('testcase'):
  f=t.find('failure');err=t.find('error');skip=t.find('skipped')
  out.append(dict(name=t.attrib['name'],classname=t.attrib.get('classname'),status='RED' if f is not None or err is not None else 'NOT_REACHED' if skip is not None else 'PASS',seconds=t.attrib.get('time'),failure_message=(f.attrib.get('message') if f is not None else err.attrib.get('message') if err is not None else None),full_failure=(f.text if f is not None else err.text if err is not None else None)))
 return out
all_results={n:cases(n) for n in ['smoke','k9','k10','n10e_c1','pe','hq297','independent']}
assert collections.Counter(x['status'] for x in all_results['hq297'])=={'PASS':4,'RED':9}
assert collections.Counter(x['status'] for x in all_results['independent'])=={'PASS':13,'RED':12}
for n,num in [('k9',8),('k10',28),('n10e_c1',56),('pe',21)]:assert len(all_results[n])==num and all(x['status']=='PASS' for x in all_results[n])
(RET/'02_EXECUTION_PER_CASE.json').write_text(json.dumps(dict(schema='RC0_INDEPENDENT_ACTUAL_EXECUTION_PER_CASE@1',results=all_results,initial19_independent=cases('initial19_independent'),no_xfail_or_skip=True,counts_overlap=True),indent=2)+'\n')
classifications={
 'test_strict_reverse_scoped_issuer_forgery_must_refuse':('VERIFIED_CANDIDATE_CODE_DEFECT','PE explicitly promises positively scoped reversal authority but checks non-null shape only. Forged issuer/version/hash still returns EXACT_SUPPORTED; it is neither dereferenced nor passed as scientific authority to C1. Correct computed reverse fractions do not qualify this supplied grant.','Pyat PE/source-operation owner plus independent reviewer; bind competent exact reversed target/risk/denominator/use, preserve native C1 computation.'),
 'test_strict_selected_world_nary_F2_AH_strata_roundtrip':('UNPROVED_DEPENDENCY','N9WorldDependency is explicitly an opaque reference carrier, not a value-bearing N9 resolver. Missing absolute_horizon is a real full-SC0 contract gap, not evidence of incorrect empirical C1 arithmetic.','N9 selected-world owner and SC0 adapter owner must supply and version a qualified value-bearing receipt.'),
 'test_strict_generated_runtime_fact_echo_not_source_promotion':('UNPROVED_DEPENDENCY','No N9 binding_echo object is supplied. This assertion does not demonstrate that PE promoted a generated fact into an original observation; the intended H3 integration is unproved.','N9/caller-binding and adapter owners; conserve opaque filter echo and ownership through the versioned boundary.'),
 'test_strict_two_distinct_world_refresh_receipts':('UNPROVED_DEPENDENCY','The PE receipt binds selected/as-of IDs and rejects INVALIDATED, but contains no two producer H2 refresh receipts. Issuance and binding of these separate successors is a cross-owner dependency.','Publication/currentness and generated-binding owners plus adapter; preserve separate receipts and targeted invalidation.'),
 'test_strict_four_clocks_historical_knowledge':('UNPROVED_DEPENDENCY','The demanded nested clocks object is absent. KeyError proves missing SC0 clock representation, not failure of PE future-time guards already covered by its native suite.','N9 temporal/currentness owner and adapter; declare exact four-clock mapping without actor-state or source authority inference.'),
 'test_strict_negative_status_algebra_and_source_risk':('UNPROVED_DEPENDENCY','No world.scoped_status_rows supplied. PE has its own typed refusal states and native empirical risk, but does not supply the full scoped N9 negative roster.','N9 status/selection owner and adapter; retain original twelve scoped states and independent native risk/routing, not a generic result-null substitute.'),
 'test_strict_values_read_not_only_hash_or_inferred_label':('REVIEWER_EXPECTATION_PROBLEM','First failing key is n9_values_read_receipt. The subsequent N10E numerator/denominator assertions were not reached. PE actually computes and consumes C1 geometry in executed positive controls; calling all PE evidence opaque hashes is false. N9 values-read remains an unproved integration dependency.','Correct the unit-level diagnosis; separately require N9 values-read and an actual producer-to-port witness.'),
 'test_strict_nonparent_apprenticeship_world_effect':('REVIEWER_EXPECTATION_PROBLEM','generic_consumers and the SC0-specific apprenticeship output map are not PE public receipt fields. PE native generic nonparent reverse computations execute correctly. Absence of this named downstream consumer is a legitimate whole-port gap, not proof that PE has no generic nonparent use.','SC0/nonparent application adapter owner with PE owner contract; avoid forcing downstream application results into an empirical producer.'),
 'test_strict_parent_scenario_remains_input_only':('REVIEWER_EXPECTATION_PROBLEM','The strict assertion fails on absent generic_consumers, before checking no_parent_actor_created. It neither shows an actor was created nor tests the existing PE actor firewall. The SC0 scenario adapter remains a separate input-only application dependency.','SC0 scenario-input adapter owner; preserve PE no-parent semantics and separate any eventual V3 authority.')}
reds=[]
for case in all_results['hq297']:
 if case['status']!='RED':continue
 grade,reason,action=classifications[case['name']]
 reds.append(dict(**case,classification=grade,scientific_adjudication=reason,accountable_owner_action=action,expanded_SC0_demand='UNSATISFIED_OR_UNPROVED; NOT_WAIVED',independent_adoption=False))
(RET/'03_NINE_PE_REDS_ADJUDICATED.json').write_text(json.dumps(dict(schema='RC0_NINE_EXECUTED_PE_REDS_ADJUDICATION@1',counts=dict(collections.Counter(r['classification'] for r in reds)),cases=reds,all_nine_remain_executed_red=True,scope_correction='Eight missing-key failures are not nine distinct demonstrated PE computational bugs; do not waive full-port requirements.'),indent=2)+'\n')
# Exact frozen case classes + implementation coverage limitations.
frozen=json.loads((RET/'01_FROZEN_INDEPENDENT_EXPECTATIONS.json').read_text());rows=[]
for family in ['K9','K10']:
 suite=all_results[family.lower()]
 for spec,run in zip(frozen[family],suite):
  suffix=int(spec['id'].split('_')[1]);notes=[]
  fidelity='EXECUTED_AUTHOR_ASSERTION; NOT_FULL_FROZEN_CONTRACT_ACCEPTANCE'
  if family=='K9' and suffix==1:notes+=['Original schema_valid assertions not executed by author test; independent JSON Schema validation RED. A/B equality is independently reproduced.']
  if family=='K9' and suffix==6:notes+=['None/obvious forged issuer are held; matching issuer with foreign scope/target is accepted by both port providers in new independent cases.']
  if family=='K9' and suffix==7:notes+=['Test explicitly invokes revoked_use only after adapter has returned consumer values; adapter-level denied-use RED.']
  if family=='K10' and suffix==15:notes+=['Author mutates as_of to equal published. Frozen procedure is future publication as known at earlier as_of; baseline published2010/asof2009 is accepted in independent RED.']
  if family=='K10' and suffix==20:notes+=['Explicit provider.revoked_use guard passes; full adapter does not apply it before values-read.']
  if family=='K10' and suffix==21:notes+=['Error is manually raised in test body, not candidate implementation. Foreign demand is independently labelled COMPLETE.']
  if family=='K10' and suffix==28:notes+=['Provider has no actor-weld method; test fallback manually raises. Actor calls truly absent, but no implemented weld-refusal API is proved.']
  if family=='K10' and suffix in [8,9,10]:notes+=['Author baseline has eight states, not original twelve, and changes DENIED_USE to DENIED. Full-roster independent RED.']
  if family=='K10' and suffix in [18,19]:notes+=['Direct freshness helper is tested; adapter does not invoke it. New resolution changes selection digest, so no stale-digest reuse was demonstrated by the additional binding probe.']
  rows.append(dict(id=spec['id'],frozen_expected=spec['expected'],author_test=run['name'],executed_status=run['status'],test_coverage_grade=fidelity,limitations=notes or ['Targeted assertion/class reproduction; original required affected-descendant/unrelated-consumer receipts are not all individually proved by this test.']))
(RET/'04_FROZEN_CASE_COVERAGE.json').write_text(json.dumps(dict(schema='RC0_8_PLUS_28_REPRODUCTION_AND_FIDELITY@1',cases=rows,port_fields_not_source_or_model_issuance=True,full_strict_freeze='CHANGES_REQUIRED'),indent=2)+'\n')
print('Required suite results and all nine RED classifications written; 36 original case coverage rows retained.')
