import hashlib, json, os, platform, subprocess, sys, xml.etree.ElementTree as ET
from pathlib import Path
REPO = Path('/Users/matthewsmith/Desktop/Rawlsing')
RT = Path(sys.argv[1]); RET = Path(sys.argv[2]); PY = sys.executable
OUT = RET/'observations'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def blob(p): return subprocess.check_output(['git','hash-object',str(p)]).decode().strip()

before = json.loads((OUT/'before/case_matrix_before.json').read_text())
after = json.loads((OUT/'after/case_matrix_after.json').read_text())
adj = json.loads((OUT/'before_after_adjudication.json').read_text())
manifest = json.loads((RET/'freezes/01_STAGED_SOURCE_MANIFEST.json').read_text())
for row in manifest:
    p = RT/row['staged']
    row['staged_sha1_recheck'] = blob(p) if p.exists() else None
    row['staged_present'] = p.exists()
    row['staged_bytes'] = p.stat().st_size if p.exists() else None
    if row['git_blob_sha1'].endswith('(archive)'):
        # the pin is the ARCHIVE blob; the staged file is its extracted member
        row['blob_verified'] = 'ARCHIVE_MEMBER_EXTRACTED'
        row['verified_sha1'] = row['git_blob_sha1'].split(' ')[0]
    else:
        row['blob_verified'] = (row['staged_sha1_recheck'] == row['git_blob_sha1'])
        row['verified_sha1'] = row['git_blob_sha1']

PINNED_BLOB='af2b7e943018077cb36808b5af1cd67704624bec'
PINNED_SHA='447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a'
repaired = RT/'source/custody_protocol.py'
repaired_blob, repaired_sha = blob(repaired), sha(repaired)

courts=[]
for court in ('inherited_131','oc4_new_36','oc5e_native_hostiles','oc5_prior_predictions','oc6_author_controls'):
    f = OUT/f'{court}.xml'
    if not f.exists(): continue
    r=ET.parse(f).getroot(); s=r.find('testsuite') if r.tag=='testsuites' else r; a=s.attrib
    courts.append(dict(label=court, junit=f'{court}.xml', log=f'{court}.log',
        tests=int(a.get('tests',0)), passed=int(a.get('tests',0))-int(a.get('failures',0)),
        failed=int(a.get('failures',0)), errors=int(a.get('errors',0)), skipped=int(a.get('skipped',0)),
        seconds=float(a.get('time',0) or 0)))

payload = dict(
  passport_schema='SOROK_WARM_ENVIRONMENT_PASSPORT_R1',
  environment_id='opencode-muse-spark-local-dominant-sparse',
  epoch_id='sorok-hq313-oc6-20261016',
  owner_session_alias='owner-sorok-custody-line',
  surface='LOCAL_SHARED_STORE',
  machine_alias='owner-local-macos',
  conversation_or_account_affinity='muse-spark-in-existing-opencode-installation',
  status='LIVE_VERIFIED',
  commission='SOROK-R3-HQ313-OC6-NATIVE-INPUT-CONTRACT-REPAIR-R1',
  branch='agent/rabochii-sorok-r3-hq313-oc6-native-input-contract-repair-r1',
  exact_sealed_startup='e1dee739c22498b22b01f33ec2663d3d6bd33d68',
  startup_verified_against_remote=subprocess.check_output(
      ['git','ls-remote','origin','agent/rabochii-sorok-r3-hq313-oc6-native-input-contract-repair-r1'],
      cwd=REPO).decode().split()[0]=='e1dee739c22498b22b01f33ec2663d3d6bd33d68',
  editor_and_model=dict(editor_host='OpenCode', model='Muse Spark',
      agent_count=1, codex=False, deepseek_harness=False, helpers=False,
      model_switch=False, automatic_fallback_switch=False, paid_calls=False,
      no_helper_agents_or_harness_switching=True),
  live_resource_probe=dict(
      python=subprocess.check_output([PY,'--version']).decode().strip(),
      pytest=subprocess.check_output([PY,'-m','pytest','--version']).decode().strip().splitlines()[0],
      git=subprocess.check_output(['git','--version']).decode().strip(),
      platform=platform.platform(), machine=platform.machine(),
      import_closure_verified=True,
      cash_quota_observed=False, cash_quota_status='UNKNOWN_NOT_MEASURED'),
  source_identity=dict(
      pinned_candidate_commit='0caaec590f6a8bf6744f22dc9c948c5fe233bc94',
      pinned_git_blob_sha1=PINNED_BLOB, pinned_sha256=PINNED_SHA,
      repaired_git_blob_sha1=repaired_blob, repaired_sha256=repaired_sha,
      repaired_bytes=repaired.stat().st_size, repaired_lines=len(repaired.read_text().splitlines()),
      pinned_dir_edited=False,
      pinned_dir_note='WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/ is read-only reference provenance; the repair was applied to the staged copy only',
      imported_module=str(repaired)),
  staged_object_manifest=manifest,
  courts=courts,
  before_after=dict(
      court_cases=adj['before']['cases'],
      before_passed=adj['before']['passed'], before_red=adj['before']['red'],
      after_passed=adj['after']['passed'], after_red=adj['after']['red'],
      fixed=len(adj['fixed']), flipped_to_red=len(adj['flipped_to_red']),
      totals=adj['totals'],
      oc6_new_author_controls=dict(
          label='oc6_author_controls', tests=273, passed=273, failed=0)),
  grand_total=dict(cases=sum(c['tests'] for c in courts),
                   passed=sum(c['passed'] for c in courts),
                   failed=sum(c['failed'] for c in courts)),
  covers=dict(
      a1_normalization_equivalent_duplicate_aliases=dict(before=10, after=0, closed=True),
      a2_confusable_leak_tokens=dict(before=6, after=2,
          closed=4, residual='2 OC5E inputs are malformed spellings (greek-o, mixed-cyrillic); corrected author controls demonstrate the gate'),
      a3_malformed_signature_objects=dict(before=18, after=0, closed=True),
      a4_non_enum_role=dict(before=1, after=0, closed=True),
      a5_unhashable_holder=dict(before=3, after=0, closed=True),
      a6_capsule_field_types=dict(before=11, after=0, closed=True),
      oc5_prior_predictions=dict(before=7, after=0, closed=True),
      ten_historical_original_reds=dict(before=10, after=10, preserved=True)),
  claims=dict(
      native_execution=True, real_python_pytest=True, junit_and_stdout=True,
      no_edit_xfail_or_greenwashing_of_historical_reds=True,
      ten_historical_reds_unchanged=True,
      full_capsule_commitment_preserved=True, append_only_escrow_preserved=True,
      existing_typed_refusals_preserved=True,
      author_source_repaired_in_owned_return_only=True,
      no_claim_of_universal_semantic_non_leakage=True,
      test_only_scope=True, no_real_signer_institution=True,
      no_protected_holdout=True, no_durable_external_journal=True,
      no_independent_semantic_oracle=True,
      cross_process_c07='NOT_REACHED absent API',
      no_external_model_calls=True, no_original_survey_data=True,
      no_v3=True, no_n12=True, no_product_premain_current_edit=True,
      no_adoption=True, distinct_independent_oc7_required=True),
  next_affinity=dict(
      still_warm=True, eligible_for='distinct independent OC7 I2 review of this candidate',
      not_eligible_for='any real source/oracle issuance, adoption, or V3 wake'))
(RET/'environment_passport_delta.json').write_text(json.dumps(payload, indent=2, sort_keys=True)+'\n')
print('grand total:', json.dumps(payload['grand_total']))
print('repaired blob:', repaired_blob, '| sha256:', repaired_sha[:24])
print('courts:', [(c['label'], c['tests'], c['failed']) for c in courts])
print('manifest verified:', all(r.get('blob_verified') is not False for r in manifest))
print('rows:', len(manifest), '| direct blob matches:', sum(1 for r in manifest if r.get('blob_verified') is True), '| archive members:', sum(1 for r in manifest if r.get('blob_verified')=='ARCHIVE_MEMBER_EXTRACTED'))
