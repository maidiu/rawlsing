"""Author repair map, preserving the predecessor's independent findings."""
from pathlib import Path
import json,hashlib
RET=Path(__file__).resolve().parents[1]
prior=json.loads((RET/'04_INHERITED_LAW_BINDINGS.json').read_text())
rows=[]
for r in prior['rows']:
 n=r['ordinal'];rows.append(dict(ordinal=n,adopted_requirement=r['adopted_requirement'],predecessor_status=r['status'],current_author_assessment='CONDITIONAL_NOT_USED' if n in (7,8,14,20,21) else 'ENFORCED_FIXED_SYNTHETIC_RULE; external owner authority HOLD',enforcement='candidate/can008_candidate_rule.py registered binding_digest includes full source-body hashes; CandidateRegistryFixture lookup validates exact actor/time/effect scope',test='test_binding_mutation_enters_valid_event_path_and_refuses',scope='One exact synthetic cell; no general owner, stochastic, modality or public-state authority'))
law=json.loads((RET/'runtime_root/law/ADP016.txt').read_text())
paths=['registry.verify_event(full sealed event)','same immutable full event ID/hash in candidate admission ledger','exact actor relation and CAUSAL_TRACE_MEMORY; no first-person inference','finite exact source public-feature bindings; no invented remembered feature','exact candidate rule/version/body hash and fixture issuer, registered in context','context checksum, exact prestate, validated proposal token, complete source-bound IDs','stochastic request -> MISSING_RNG_AUTHORITY; no RNG authority inferred']
gates=[dict(law_requirement=g,enforcement=p,scope='TEST_ONLY_CANDIDATE_STATE; accepted destination owner HOLD') for g,p in zip(law['formation_rule']['all_gates_required'],paths)]
route={
'INELIGIBLE_NONCAUSAL_SOURCE':'Formation rejects structural/V2/render/nonoccurred content classes',
'DEFERRED_MISSING_MEMORY_BASIS':'No-context proposal remains deferred/uncommitted; unknown cue/owner never auto-applies',
'MISSING_PARENT_EVENT':'Missing event or id/hash refuses',
'PARENT_EVENT_HASH_MISMATCH':'Context verifies exact admitted event; transition checks declared parent hash',
'UNKNOWN_MEMORY_ID':'A transition cannot use memory absent from verified context',
'MEMORY_ID_COLLISION':'Conflicting formation under same identity refuses; exact replay is idempotent',
'PRE_STATE_HASH_MISMATCH':'Exact live pre-state required for formation/commit and transition request',
'UNAUTHORIZED_TRANSITION':'Only finite candidate formation rule is registered; other operations/cues do not gain authority',
'UNAUTHORIZED_RECALL_CUE':'Trace is not recallable; no registered recall cue rule',
'UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION':'Direct analyst-ledger rehydration refuses',
'UNAUTHORIZED_V2_SESSION_PROMOTION':'No promotion API; V2 formation is INELIGIBLE_NONCAUSAL_SOURCE, unsupported transition is UNAUTHORIZED_TRANSITION (no exact-code emission claimed)',
'UNSUPPORTED_CONFABULATION':'No substitute-detail API; invented formation trigger/features refuse UNAUTHORIZED_TRANSITION; generic confabulation operation refuses (no exact-code emission claimed)',
'MISSING_RULE_VERSION':'Empty version explicitly refuses; no default version',
'MISSING_RNG_AUTHORITY':'Stochastic formation/transition refuses; no RNG authority',
'RETENTION_UNKNOWN':'Remains unknown; permission DEFER, no content/stance default',
'ACCESS_UNKNOWN':'Remains unknown; permission DEFER, no automatic known denial',
'INTEGRITY_FAILURE':'Modified memory/proposal/state/journal prevents mutation or downstream causal use'}
neg=[dict(**r,repair_route=route[r['state']],authority='Exact adopted blob c6619a286e115d060ab4830889e7fc23762167a5') for r in law['fail_closed_states']]
actions=[dict(id=i,required=a) for i,a in [
('DISTINCT_I2','Separate HQ-commissioned independent reviewer reproduces exact CAN2 source, final counts and narrowed causal inference; current author cannot accept own repair'),
('RETAINED_ORACLES','Adjudicate8 candidate fixture-conflict REDs and1 precommit-flag RCP3 RED without erasing original tests/freeze. Any future authorized valid-fixture adaptation must preserve semantic assertions and custody'),
('PRODUCTION_ISSUER','Competent owner/HQ separately issues any operative rule registry, external-event issuer/version/admission, conditioning or destination owner authority; current production registry stays empty'),
('MEMORY_LIFECYCLE','Exact owner rules/cues and grants before any degradation/recall/access/RNG operations; current implementation supports only finite candidate formation'),
('KNOWLEDGE_AND_PUBLIC','No verified knowledge acquisition/objective-truth/public-standing owner in this cell: typed HOLD, never infer them from private belief or test labels'),
('CAUSAL_SCOPE','Memory/epistemic ref ablation leaves typed DEFLECT unchanged. Preserve prior CAN008 history mechanism; do not claim stronger ADP mediation or accepted owner persistence'),
('MODEL_SOURCE_ACTOR','No original respondent source, external model/provider trial, real actor/V3 operation or adoption rights issued')]]
out=dict(schema='CAN2_AUTHOR_LAW_REPAIR_MAP@1',independent_acceptance=False,can008_23=rows,adp016_7=gates,adp016_17=neg,adp017=dict(canonical_claim='All11 fields/content identity verify against finite registry',effect='All12 fields and provenance-bound ID',state='All9 required fields, set-valued records, exact transition/permission snapshots',operations='ADD/WITHDRAW/SUPERSEDE_EXACT_RECORD/NO_CHANGE; exact target required',knowledge='HOLD_NO_ACCEPTED_KNOWLEDGE_ACQUISITION_RULE',belief='One finite private BELIEF emission with admitted basis and exact state',K3='Trace/inaccessible cannot permit; UNKNOWN defers; exact snapshot required; hidden-origin explanation blocked',K5='Objective relation never auto-edits belief or public standing; public owner HOLD'),owner_actions=actions,I3='NOT_TRIGGERED; no adopted-law collision')
(RET/'06_REPAIR_LAW_AND_OWNER_ACTIONS.json').write_text(json.dumps(out,indent=2)+'\n')
prior_matrix=json.loads((RET/'runtime_root/rcp3/04_EXECUTED_CASE_MATRIX.json').read_text())
old=next(s for s in prior_matrix['suites'] if s['suite']=='reviewer__final')
current=json.loads((RET/'02_EXECUTED_CASE_MATRIX.json').read_text());new=next(s for s in current['runs'] if s['run']=='repaired_reviewer_sealed2')
lookup={c['name']:c for c in new['cases']};transitions=[dict(name=c['name'],RCP3=c['status'],CAN2=lookup[c['name']]['status'],CAN2_message=lookup[c['name']]['message']) for c in old['cases']]
assert len(transitions)==82
(RET/'07_RCP3_REPAIR_TRANSITIONS.json').write_text(json.dumps(dict(schema='CAN2_ORACLE_TRANSITIONS@1',predecessor_prereview_source='a11982e6cf135a8ecc72b6152ec796b4a4707093',note='Not all passes are positive-path proofs: old opaque hash fixtures may refuse earlier. New89 author controls carry valid baseline checks; stronger mediation remains unproved',transitions=transitions),indent=2)+'\n')
print('law23/gates7/negative17 and exact82 transitions mapped; old matrix fully parsed')
