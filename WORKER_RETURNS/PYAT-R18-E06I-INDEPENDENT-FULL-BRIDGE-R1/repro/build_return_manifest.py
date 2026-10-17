"""Build the reviewer return manifests: artifact digests and passport delta."""
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
CAND = os.path.realpath(os.environ.get('E06_CANDIDATE_ROOT', ''))
SHA = 'f9c52113de38caececc450f0e54c980f64ed3981'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


summary = json.loads((RET / 'observations' / 'junit_summary.json').read_text())
closure = json.loads((RET / 'observations' / 'source_closure_proof.json').read_text())

passport = dict(
    schema='E06I_SANITIZED_ENVIRONMENT_PASSPORT_DELTA@1',
    environment_id='E06I_LOCAL_REVIEWER_COURT',
    epoch_id='E06I_R18_INDEPENDENT_FULL_BRIDGE',
    session_alias='E06I_R18',
    surface='S2_LOCAL_HOST',
    machine_alias='LOCAL_SHARED_STORE_HOST',
    status='LIVE_VERIFIED',
    observed_at_utc=datetime.now(timezone.utc).isoformat(),
    interpreter=platform.python_version(),
    pytest=subprocess.check_output([sys.executable, '-m', 'pytest', '--version'], text=True).strip(),
    git=subprocess.check_output(['git', '--version'], text=True).strip(),
    platform=platform.system() + ' ' + platform.machine(),
    branch='agent/reviewer-pyat-20261016-r18-e06i-full-bridge-independent-r1',
    sealed_startup='6aea052f09ef01205aff1c38cd8c68197b762447',
    candidate=dict(branch='agent/userdirect-pyat-20261016-r17-e06-e04e05-native-bridge-r1', sha=SHA,
                   bridge_sha256=closure['candidate_bridge_sha256']),
    source_closure=dict(manifest_entries=closure['manifest_entries'],
                        verified_preimages=closure['verified_preimages'],
                        e05s_objects=closure['e05s_objects'], e04t_owner_commit=closure['e04t_owner_commit']),
    tests=dict(author_regression=summary['author_regression']['counts'],
               independent_court=summary['independent_court']['counts'],
               author_exit=summary['author_regression']['exit'],
               independent_exit=summary['independent_court']['exit']),
    cold_processes=4,
    model=dict(requested='Codex GPT-6.1 Sol Medium or cheaper qualified Python/pytest executor',
               observed_provider='DeepSeek Harness', actual_model='deepseek-flash',
               actual_reasoning_effort='NOT_EXPOSED'),
    quota=dict(plan='UNKNOWN', incremental_cash='UNKNOWN'),
    independence='reviewer did not author or modify the candidate; author 40 is regression only',
    installation_status='NOT_INSTALLED; OC05 NOT_YET_APPLICABLE; no source/model/actor rights exercised',
    privacy='synthetic fixtures only; no original SAV/DTA/PDF, credentials or source issuance',
    retire_or_reprobe='runtime reset, candidate/source branch change, new rights, or unrelated task',
)
(RET / 'environment_passport_delta.json').write_text(json.dumps(passport, indent=1, sort_keys=True) + '\n')

# artifact digests last, so every hashed file (including the passport) is final
artifacts = {}
for p in sorted(RET.rglob('*')):
    if not p.is_file():
        continue
    rel = str(p.relative_to(RET))
    if rel == 'artifact_sha256.json' or rel.startswith('runtime/') or '__pycache__' in rel:
        continue
    artifacts[rel] = sha(p)
(RET / 'artifact_sha256.json').write_text(json.dumps(artifacts, indent=1, sort_keys=True) + '\n')
print('artifacts', len(artifacts), 'passport written')
