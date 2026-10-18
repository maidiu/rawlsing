"""Create additive repair receipts without touching the frozen review."""
import difflib,hashlib,json,subprocess,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from run_repair import ROOT,REVIEW,check_frozen,sanitize

check_frozen()
before=(REVIEW/'reconstructed/clr3/recursive_court.py').read_text().splitlines(keepends=True)
candidate=ROOT/'candidate/recursive_court.py'
after=candidate.read_text().splitlines(keepends=True)
(ROOT/'candidate.patch').write_text(''.join(difflib.unified_diff(before,after,fromfile='frozen_clr3/recursive_court.py',tofile='repair_r1/candidate/recursive_court.py')))
for path in (ROOT/'evidence').iterdir():
    if path.suffix in {'.log','.xml'}:path.write_text(sanitize(path.read_text()))
for path in (ROOT/'evidence').glob('*.xml'):ET.parse(path)
execution=json.loads((ROOT/'evidence/execution_receipts.json').read_text())
previous=json.loads((REVIEW/'environment_passport_delta.json').read_text())
assert hashlib.sha256((REVIEW/'.environment_marker').read_bytes()).hexdigest()==previous['runtime_marker_digest']
passport=dict(passport_schema='SOROK_ENVIRONMENT_PASSPORT_R1',environment_id=previous['environment_id'],epoch_id=previous['epoch_id'],owner_session_alias='clr3-reviewer-now-repair-author',surface='LOCAL_SHARED_STORE',status='LIVE_VERIFIED',last_live_probe_at=datetime.now(timezone.utc).isoformat(),runtime_marker_digest=previous['runtime_marker_digest'],continuity='same verified worktree, marker, original source hashes and .runtime requirements; no reinstall or environment switch',git_object_store_alias=previous['git_object_store_alias'],worktree_alias=previous['worktree_alias'],branch=previous['branch'],base_review_commit='0a5da3542f9bb5dd442a2cc1bd605d8958388f13',git_state='clean at repair launch; only additive repair_r1 changes',source_family='frozen CLR3 legacy closure plus repaired research wrapper',materialized_source_refs='../evidence/reconstruction_manifest.json',candidate_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest(),import_receipts='evidence/replay_and_imports.json',dependency_closure_status='same frozen 65-file closure, 54 legacy modules observed; no dependency change',python='3.11.3',pytest='9.1.1',PyYAML='6.0.2',git='2.43.0',probe_command_and_result={'command':'python3 run_repair.py','exit_code':1,'meaning':'55 PASS plus six preserved historical REDs'},covered_test_suites=execution['suites'],science_grade='SOURCEFREE_AUTHOR_REPAIR_REGRESSION; NOT_INDEPENDENT_ACCEPTANCE_OR_ADOPTION',editor='Codex',model=previous['model'],effort=previous['effort'],model_provider=previous['model_provider'],cash_known=False,cash=None,quota_known=True,repair_launch_quota={'primary_used_percent':31,'secondary_used_percent':30,'scope':'account-wide live observation, not job cost'},privacy_source_grant='explicit user follow-up for two research validation fixes; no original source/actor/native rights',independent_review_separation='Frozen review retained; agent is now repair author. HQ owns later distinct acceptance.',assignments_completed=['bounded repair of I2-F01 and I2-F02'],next_good_affinity_tags=['CANON_VALIDATION','SOURCE_CONSISTENCY_REVIEW'],staged_state_preservation='retained; re-probe before reuse',retire_or_rebuild_reason=None,external_model_calls=0,semantic_issuance=False,native_adoption=False)
(ROOT/'environment_passport_delta.json').write_text(json.dumps(passport,indent=2,sort_keys=True)+'\n')
completion=dict(authorization='direct user follow-up: okay, can you fix them please',role='author repair, not independent review of own candidate',base_review='0a5da3542f9bb5dd442a2cc1bd605d8958388f13',fixed_counterexamples=['I2-F01','I2-F02'],unchanged_test_probes=True,tests=execution['suites'],valid_trajectory_records_equal=4,cold_processes=4,legacy_source_files_unchanged=65,all_previous_review_bytes_unchanged=True,original_six_RED_preserved=True,native_owner_holds_unchanged=True,whole_archive_lineage_hold_unchanged=True,additional_49_dependencies_not_historically_admitted=True,numerical_law_changed=False,semantic_issuance=False,independent_acceptance=False,post_return_owner='HQ',write_terrain='new repair_r1 subtree only')
(ROOT/'evidence/completion_audit.json').write_text(json.dumps(completion,indent=2,sort_keys=True)+'\n')
rows=[]
for p in sorted(ROOT.rglob('*')):
    rel=str(p.relative_to(ROOT))
    if not p.is_file() or rel in {'return_manifest.json','SHA256SUMS'} or '__pycache__' in p.parts or p.suffix=='.pyc':continue
    data=p.read_bytes()
    assert all(prefix not in data for prefix in (b'/' + b'Users/',b'/' + b'home/')),rel
    rows.append(dict(path=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
(ROOT/'return_manifest.json').write_text(json.dumps(dict(base_review='0a5da3542f9bb5dd442a2cc1bd605d8958388f13',file_count=len(rows),files=rows,excluded=['manifest and checksum self hashes','local bytecode caches'],role='authored repair candidate; no self-adoption'),indent=2)+'\n')
(ROOT/'SHA256SUMS').write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in rows))
print('Repair seal:',len(rows),'files;',sum(r['bytes'] for r in rows),'bytes; previous review unchanged; all JUnit parses')
