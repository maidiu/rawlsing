"""Requirement-by-requirement completion of the court, not candidate acceptance."""
import collections, hashlib, json, pathlib, subprocess
RET=pathlib.Path(__file__).resolve().parents[1];RT=RET/'runtime_root'
START='cdd1f1c9eb74b02abe2ed23ccc5278bcfaad684c'
PARENT='75341803ace63da30dfcd66273b6e3d75ad87132'
BRANCH='agent/reviewer-sorok-r3-hq302-rsc0-connected-port-independent-r1'
def git(*a):return subprocess.check_output(['git',*a],cwd=RET,text=True).strip()
assert git('branch','--show-current')==BRANCH
assert git('rev-parse',START+'^')==PARENT
assert hashlib.sha256((RET/'01_FROZEN_INDEPENDENT_EXPECTATIONS.json').read_bytes()).hexdigest()=='539b67e90cf46ab1dc4639f1f73c87db839d8ccf755678f2f2830950b0bad5e3'
obj=json.loads((RET/'02_EXECUTION_PER_CASE.json').read_text())
expected={'smoke':(2,0),'baseline_rc0':(13,12),'rc0':(25,0),'k9_k10':(36,0),'original_k9_k10':(34,2),'connection':(6,0),'n10e_c1':(56,0),'pe':(21,0),'hostile':(16,31)}
for result in obj['results']:
 counts=result['counts']; assert (counts['PASS'],counts['RED'])==expected[result['suite']]
 assert counts['ERROR']==counts['SKIP']==0
 assert result['execution']['exit_code']==int(counts['RED']>0)
 assert (RET/result['execution']['junit']).exists() and (RET/result['execution']['log']).exists()
trans=obj['RC0_unchanged25_transitions'];assert len(trans)==25
assert collections.Counter(x['before'] for x in trans)=={'PASS':13,'RED':12}
assert all(x['after']=='PASS' for x in trans)
sel=json.loads((RET/'source_selector.json').read_text());assert len(sel['files'])==85
assert sum(x['family']=='original_29' for x in sel['files'])==29
for row in sel['files']:
 b=(RT/row['staging_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==row['git_blob_sha1']
 assert hashlib.sha256(b).hexdigest()==row['sha256']
for provider in ['ProviderA','ProviderB']:
 obs=RET/'repro/hostile_observations'
 calls=json.loads((obs/('calls_'+provider+'.json')).read_text())
 assert calls['actual_calls']=={'N10E':1,'C1':2,'PE':1}
 assert calls['lane']['support']['target_yes']==54 and calls['lane']['support']['target_no']==6
 fake=json.loads((obs/('fake_profile_'+provider+'.json')).read_text())
 assert fake['connected'] and not any(fake['actual_calls'].values())
 removed=json.loads((obs/('pe_removed_'+provider+'.json')).read_text())
 assert removed['actual_calls']['PE']==0 and removed['lane']['connected']
 for mode in ['absent','revoked']:
  denied=json.loads((obs/('world_deny_'+provider+'_'+mode+'.json')).read_text())
  assert denied['error']=='DENIED_USE' and denied['value_reads']==0 and not any(denied['calls'].values())
 refs=json.loads((obs/('h2_refs_'+provider+'.json')).read_text())
 assert len({x['hash'] for x in refs['world_refs']})==3
 assert len({x['hash'] for x in refs['possibility_refs']})==1
schema=json.loads((RET/'repro/observations_by_suite/rc0/schema.json').read_text())
assert not any(schema['errors'].values())
negative=json.loads((RET/'repro/observations_by_suite/rc0/negative_states.json').read_text())
assert negative['expected']==negative['actual'] and len(negative['actual'])==12
reverse=json.loads((RET/'repro/reverse_connection_probe.json').read_text())
assert all(not any(x['actual_reverse_calls'].values()) for x in reverse['candidate_reverse_paths'])
assert reverse['positive_control']['actual_calls']=={'N10E':1,'C1':1,'PE':0}
passport_text=(RET/'environment_passport_delta.json').read_text()
assert not any(s in passport_text for s in ['/Users/','/home/',pathlib.Path.home().name])
passport=json.loads(passport_text);assert passport['status']=='LIVE_VERIFIED'
assert passport['runtime_marker_digest']==hashlib.sha256((RT/'runtime_marker.json').read_bytes()).hexdigest()
assert passport['independent_review_separation']['distinct_from_prior_RC0_reviewer'] is False
assert len(passport['materialized_source_refs'])==85 and passport['selected_model']=='gpt-6.1-sol' and passport['effort']=='high'
assert len(json.loads((RET/'04_AUTHORITY_AND_CLAIM_GRADE_MATRIX.json').read_text())['matrix'])==12
assert len(json.loads((RET/'05_OWNER_ACTION_REGISTER.json').read_text())['actions'])==12
rows=[
 ('Exact seal/parent/branch, full commission00C00D and routing','repro/read_and_identity_receipt.json; live probes','VERIFIED'),
 ('Frozen expectations before candidate test observation','01_FROZEN_INDEPENDENT_EXPECTATIONS.json exact539b67e9 hash','VERIFIED'),
 ('Genuine blob/NUL hashes and actual module files, marker/epoch','source_selector.json; import_audits; passport; live_environment_probe.json','VERIFIED'),
 ('Unchanged RC025 and actual12RED baseline,13 preserved','02_EXECUTION_PER_CASE.json; baseline_rc0.xml; rc0.xml; isolated observations','VERIFIED'),
 ('Both original and revised K98+K1028; no hidden normalization','34PASS2RED original;36PASS revised; exact source diffs','VERIFIED_WITH_COMPATIBILITY_REDS'),
 ('Pinned56N10E/C1 and21PE and6connection full results','All suite logs/JUnit and actual exit receipts','VERIFIED'),
 ('Actual pinned producers and54/60,6/60 consumed baseline','Independent code-object trace both providers; source hashes','VERIFIED_BOUNDED'),
 ('Historical fixture revision, lookahead and prior exception','Explicit original2009/2010 refusal plus forged/dropped declaration counterexamples','VERIFIED_REVIEW_REVISE'),
 ('WORLD_READ absence/revocation before production/value effects','4 independent PASS probes, exact zero calls/reads; query permission4RED retained','VERIFIED_REVIEW_REVISE'),
 ('Scoped reversal real calculation versus flags','Real reverse positive control and zero-call candidate probe;6invalid grantRED','VERIFIED_REVIEW_REVISE'),
 ('F1/F2 H1-H3 refresh/release, negative schema, receipt freshness','RC0 positives plus final mismatch/refidentity/read-ref counterexamples','VERIFIED_REVIEW_REVISE'),
 ('New mandated hostiles including fake profile, static hint, source alteration, operative refs','47executed16PASS31RED; classifications and actual values','VERIFIED'),
 ('Inherited onePEdefect/fivedependencies/threeexpectationproblems','03_INHERITED_PE_RED_ADJUDICATION.json; unchanged PE21 rerun','VERIFIED_NO_WAIVER'),
 ('Independent verdict, precise claim grades and competent actions','00_RETURN.md;04matrix;05register','VERIFIED'),
 ('Reviewer distinct from C0 authors and priorRC0 reviewer','Distinct fromC0; same priorRC0chat explicitly disclosed','FORMAL_FRESH_REVIEWER_ACCEPTANCE_HOLD'),
 ('No candidate owner edits, source/model/actor/adoption/canonical action','Only assigned return path audit; source85unchanged; authority ceiling','VERIFIED_PENDING_FINAL_PATH_AUDIT'),
 ('Executable reproduction, sanitized passport, all failures and changed paths','reproduce.sh; scripts; full logs/JUnit; manifest/changed_paths','VERIFIED_PENDING_FINAL_MANIFEST'),
 ('Commit assigned return, push and direct full remote SHA/ancestry','Final publication external readback; futureSHA cannot self-reference','FINAL_PUBLICATION_EXTERNAL_READBACK_REQUIRED'),
]
audit=dict(schema='RSC0_COURT_COMPLETION_AUDIT@1',court_scientific_verdict='REVIEW_REVISE',candidate_acceptance='NOT_GRANTED',formal_fresh_reviewer_acceptance='HOLD_DISCLOSED_PRIOR_RC0_CONTINUITY',adoption=False,requirements=[dict(requirement=r,evidence=e,status=s) for r,e,s in rows],scope='Completion of an executed hostile court with exact negative verdict; not completion of candidate repairs or operative authority')
(RET/'06_REQUIREMENT_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
print('RSC0_COURT_EVIDENCE_VERIFIED; SCIENTIFIC_REVIEW_REVISE; FORMAL_FRESH_REVIEWER_HOLD_DISCLOSED; FINAL_PUBLICATION_PENDING')
