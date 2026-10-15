"""Build the independent law matrices and case receipts from actual observations."""
from pathlib import Path
import json,re,xml.etree.ElementTree as ET,hashlib,subprocess,datetime
RET=Path(__file__).resolve().parents[1]
LAW=RET/'runtime_root/law'
can=(LAW/'CAN008_R2.txt').read_text();section=can.split('# 16. Concrete R2 rule obligations')[1].split('# 17.')[0]
requirements=re.findall(r'^\d+\. (.*?)[;.]?$',section,re.M)
assert len(requirements)==23
fields=['rule_id/version/content_hash','eligible_event_authority_signatures + eligible_event_roles','actor_scope + temporal_scope','receivability_semantics','eligible_conditioning_owner_signatures','conditioning_causal_use_roles','counterpart_scoping','modality_evidence_authorities','uptake_appraisal_semantics','recruitment_semantics','multiplicity_handling','co_determination_closure','prior_response_history_predicates','current_condition_effort_role','effect_kinds','target_authority_kind + target_validation','pff_current_consequence_projection','valid_empty_behavior','missing_deferred_ambiguous_behavior','quantitative_contract','adp020_binding','atomic_commit_behavior','provenance_replay_requirements']
notes={
1:'Presence-only helper is not called on active evaluation. Empty or foreign rule identity and an empty fixture registry still permit positive evaluation; no registration lookup.',
2:'Issuer-ID membership rejects missing/foreign ID. Issuer version and event-role signature are not bound; changing issuer version leaves the receipt hash unchanged.',
3:'Event actor label is checked against binding, but registered actor scope, prestate actor and temporal_scope are not enforced. A future2099 event is accepted without the helper flag.',
4:'Empty public features label receivability UNRESOLVED but still allow response effects; omission of semantics is accepted on active path.',
5:'Striving/practice/memory strings are recruited without dereferencing exact owner/authority/version/state hashes. Removing eligible owner signatures does not block.',
6:'Declared roles are copied into receipt but not checked against consumed state. Removing them leaves a positive response.',
7:'No counterpart/relationship input participates in this narrow cell. Conditional obligation is N/A, not a proved general scoping mechanism.',
8:'No modality evidence is consumed. NONE_USED declaration is not implementation of future modality authority or roles.',
9:'A constant appraisal template is emitted. No exact registered event-to-appraisal semantic binding is verified; omission still produces effects.',
10:'String references are appended to recruitment without owner-state validation; missing recruitment semantics still produces effects.',
11:'Selected lists preserve some order; tensions/expectations and contradictory owner states are not exercised. No active multiplicity binding check.',
12:'One straight deterministic pass has finite execution and exact fixture replay. Its declared closure binding can be omitted; no iterative semantics are established.',
13:'Default binding declares prior history NONE, but chain directly branches on prior BUFFER row. No exact history predicate/hash/actor scope is validated.',
14:'No current condition/effort input is used. N/A for this cell; no capacity scalar or general effort claim inferred.',
15:'Requested effect outside six inherited kinds refuses. This establishes enum guarding only; caller still chooses allowed effect and target request remains unvalidated.',
16:'Target requests explicitly have validated=False and committed=False; chain nonetheless reports target owner effect committed. Target validation binding is not executed.',
17:'Binding says current projection NOT_EMITTED but response emits NON_DURABLE_CURRENT_CONSEQUENCE. No governed PFF consumer envelope; current row is later history, not proof of durable owner state.',
18:'No public features still produces positive response. Declared valid-empty behavior is text; omit it and active path continues.',
19:'Some simple refusal codes work, but after a rejected coupling the chain can continue to commits or leave partial effects. Failure behavior string not enforced.',
20:'No numeric semantic operation is used; conditional numeric contract N/A. No quantitative validity is certified.',
21:'No stochastic operation is used; conditional ADP020 binding N/A. No stochastic grant or RNG success inferred.',
22:'Whole-chain forged issuer completes; unadmitted/missing hash returns ADP016_REFUSED after a CAN008 row has committed. No rollback; mutable payload and broken predecessor hash binding.',
23:'Fixture replay matches exactly. Version/owner state provenance omitted or unchecked; corrupt stored effect is read, and formation/epistemic IDs alias changed provenance.'}
rows=[]
for i,(requirement,field) in enumerate(zip(requirements,fields),1):
 obs=json.loads((RET/'repro/observations'/('binding_%02d.json'%i)).read_text())
 conditional=i in (7,8,14,20,21)
 state='NOT_APPLICABLE_IN_THIS_CELL' if conditional else 'PARTIAL_GRAMMAR_ONLY' if i==15 else 'REVISE_SEMANTIC_BINDING_NOT_ESTABLISHED'
 rows.append(dict(ordinal=i,adopted_requirement=requirement,candidate_fields=field,law='CAN008_R2 b80dd692 §16 item'+str(i),status=state,independent_assessment=notes[i],active_omission_output=obs['response'].get('decision_state'),observation='repro/observations/binding_%02d.json'%i))
(RET/'01_CAN008_23_LAW_BINDINGS.json').write_text(json.dumps(dict(schema='RCP3_INDEPENDENT_CAN008_LAW_MAP@1',derivation='Exact adopted §16 text, not author obligation tuple',rows=rows,disposition='REVIEW_REVISE',conditional_NA_items=[7,8,14,20,21],note='Tests are source-aware new reviewer controls, not a new or retroactive pre-observation freeze'),indent=2)+'\n')
a16=json.loads((LAW/'ADP016.txt').read_text());a17=json.loads((LAW/'ADP017.txt').read_text())
gate_status=[('PARTIAL','Admission string and future-derived flag are checked. Source owner/event-kind issuance is not verified by formation.'),('REVISE','ID/hash nonempty only; no source-ledger hash verification in formation. Explicit mismatch helper separately rejects when supplied.'),('SCOPED_CAUSAL_TRACE_EXCEPTION','CAUSAL_TRACE_MEMORY may be formed without declarative experience; this does not grant actor knowledge or arbitrary actor/rule authority.'),('UNPROVED_FEATURE_CUSTODY','A content-state enum is stored as source_feature_bindings; exact source feature identities/hashes are not verified.'),('REVISE','Nonempty rule strings suffice; forged rule/authority forms memory.'),('REVISE','Empty prestate accepted; formation ID does not bind prestate; corrupt memory marker accepted by transition helper.'),('NOT_APPLICABLE_DETERMINISTIC','No stochastic operation in this cell; no ADP020/RNG grant inferred.')]
fail_notes={
'INELIGIBLE_NONCAUSAL_SOURCE':'Admitted flag false and five noncausal content kinds refuse; behavior positively observed.',
'DEFERRED_MISSING_MEMORY_BASIS':'Missing basis None raises untyped AttributeError; expected typed owner refusal not implemented.',
'MISSING_PARENT_EVENT':'Empty event ID/hash formation guard raises; transition helper permits parent=None.',
'PARENT_EVENT_HASH_MISMATCH':'Explicit declared hash mismatch in transition helper raises correct typed error; formation has no authoritative lookup.',
'UNKNOWN_MEMORY_ID':'No owner memory registry to verify existence; dataclass/enum shape validation only. Not established.',
'MEMORY_ID_COLLISION':'Explicit override aliases different source events to same memory ID/current state hash; no collision check.',
'PRE_STATE_HASH_MISMATCH':'Explicit supplied mismatch rejects; omitted transition prestate or blank formation prestate accepts.',
'UNAUTHORIZED_TRANSITION':'DELETE_MEMORY and unrecognized kind refuse. Forged formation rule/authority still accepts.',
'UNAUTHORIZED_RECALL_CUE':'CAUSAL_TRACE RECALL refuses; broader cue registry/slow-process authority not implemented.',
'UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION':'Dedicated helper always raises this typed refusal; no actual rehydration allowed.',
'UNAUTHORIZED_V2_SESSION_PROMOTION':'V2 transcript content-state refuses through generic INELIGIBLE_NONCAUSAL_SOURCE, not this distinct handler.',
'UNSUPPORTED_CONFABULATION':'Unknown content-state enum refuses. Exact source-feature graph not verified; no broad confabulation safety claim.',
'MISSING_RULE_VERSION':'Empty formation version refuses using UNAUTHORIZED_TRANSITION; exact version authority dereference missing.',
'MISSING_RNG_AUTHORITY':'No stochastic input or transition executed. N/A, not a separately exercised missing-RNG gate.',
'RETENTION_UNKNOWN':'Law says remain UNKNOWN, not universally raise. Dataclass admits unknown enum; no governed mutation/persistence engine demonstrated.',
'ACCESS_UNKNOWN':'Law says remain UNKNOWN. Sole-basis helper collapses permission to known DENY instead of DEFER_MISSING_AUTHORITY.',
'INTEGRITY_FAILURE':'Explicit corrupt memory integrity marker is accepted for commit; state-content hash validation absent.'}
d=dict(schema='RCP3_ADP016_ADP017_INDEPENDENT_LAW_MAP@1',inherited_prereg_count_correction=dict(inherited_text='16 ADP016 fail-closed states',adopted_JSON_actual_entries=len(a16['fail_closed_states']),inherited_freeze_changed=False,interpretation='17 entries are authoritative. RETENTION_UNKNOWN/ACCESS_UNKNOWN remain unknown; the prior blanket must-raise wording is stronger than law. This is a disclosed law-vs-prior discrepancy, not a rewritten freeze.'),adp016_formation_gates=[dict(ordinal=i+1,adopted_gate=g,status=gate_status[i][0],assessment=gate_status[i][1]) for i,g in enumerate(a16['formation_rule']['all_gates_required'])],adp016_failclosed=[dict(adopted=x,assessment=fail_notes[x['state']]) for x in a16['fail_closed_states']],memory_transition_fields=dict(required=a16['transition_record']['required_fields'],observed='All20 named fields present in actual return',identity='REVISE: changed prestate produces same memory_transition_id'),adp017=dict(effect_fields=a17['epistemic_effect']['required_fields'],field_presence='All12 fields and four operation labels execute; no exact canonical claim registry or actor/state/parent authority validation',canonical_claim_required=a17['claim_model']['required_fields'],knowledge_gates=[dict(ordinal=i+1,adopted=g,assessment=('Objective relation gate rejects contradicted knowledge.' if i==1 else 'Nonempty actor-facing string check only; forged string accepted.' if i==2 else 'Not independently verified against canonical claim/rule/actor/prestate/authority registry; forged positive knowledge observed.')) for i,g in enumerate(a17['knowledge_gate']['all_required'])],belief_gates=a17['belief_gate']['all_required'],belief_assessment='Empty claim, parents and rule identity still emit APPLIED. No state-set/transition store exists; stance_persisted is a boolean assertion.',K3='Explicit trace representation denies first-person and recall; sole-trace helper nevertheless permits BELIEF; known inaccessible event memory is also permitted by direct first-person helper.',K5='BELIEF effect identical when objective relation flips SUPPORTED/CONTRADICTED; bounded invariance verified. No public-standing ratification owner or real actor state is executed; do not claim a full standing-to-belief causal system.',first_person='Ordinary accessible stance mapping and no-stance denial work. Unknown sole-memory basis is collapsed to DENY instead of DEFER; no complete actor-safe envelope producer in this candidate.',production_boundary='M6 owner tests separately pass; candidate chain does not thereby become an integrated M6/V2/V3 actor path.'),disposition='REVIEW_REVISE')
(RET/'02_ADP016_ADP017_LAW_GATES.json').write_text(json.dumps(d,indent=2)+'\n')
suites=[]
for f in sorted((RET/'repro/runs').glob('*/junit.xml')):
 r=ET.parse(f).getroot();ss=list(r.iter('testsuite'));c={k:sum(int(x.attrib.get(k,0)) for x in ss) for k in ('tests','failures','errors','skipped')};c['passed']=c['tests']-c['failures']-c['errors']-c['skipped']
 ex=json.loads((f.parent/'execution.json').read_text());cases=[]
 for t in r.iter('testcase'):
  issue=t.find('failure');issue=issue if issue is not None else t.find('error')
  status='ERROR' if t.find('error') is not None else 'RED' if t.find('failure') is not None else 'SKIP' if t.find('skipped') is not None else 'PASS'
  cases.append(dict(name=t.attrib['name'],status=status,message=issue.attrib.get('message') if issue is not None else None))
 suites.append(dict(suite=f.parent.name,counts=c,exit_code=ex['exit_code'],junit=str(f.relative_to(RET)),command=ex['command'],cases=cases))
(RET/'04_EXECUTED_CASE_MATRIX.json').write_text(json.dumps(dict(suites=suites,primary_pinned_reproduction=['owners__closed','rsm__closed','candidate__closed'],primary_independent_science='reviewer__final',initial_import_failures='Missing root from-import render_bounded_expression fixed by exact Git staging; all original outputs retained. These were reviewer closure failures, not candidate science.',no_xfail_relabelled=True,own_source_history='repro/history contains exact80-test reviewer source before two additional controls',reviewer_test_polarity='Assertions express law/claimed mechanism;45 REDs retained, not inverted to PASS because a defect was observed. Repeated and related predicates are not45 independent production defects.'),indent=2)+'\n')
print('23-item law map,7+17 memory map, epistemic map and complete per-case receipts generated')
