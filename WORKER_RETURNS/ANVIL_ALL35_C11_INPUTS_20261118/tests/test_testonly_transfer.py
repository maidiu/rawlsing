from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
RUN=HERE/'testonly_bundle'/'run.py'
def test_existing_small_sourcefree_typed_bundle_builds_reopens_and_refuses(tmp_path):
    root=tmp_path/'fresh_replay'
    p=subprocess.run([sys.executable,'-B',str(RUN),str(root)],cwd=str(HERE),text=True,capture_output=True,env={**__import__('os').environ,'PYTHONPATH':str(HERE.parents[2]),'PYTHONDONTWRITEBYTECODE':'1'})
    assert p.returncode==0,p.stdout+p.stderr
    assert 'TESTONLY_BUNDLE_PASS' in p.stdout
    build=json.loads((root/'proof'/'build.json').read_text())
    reopen=json.loads((root/'proof'/'reopen.json').read_text())
    refusal=json.loads((root/'proof'/'refusal.json').read_text())
    revoked=json.loads((root/'proof'/'reopen_refusal_revoked.json').read_text())
    wrong=json.loads((root/'proof'/'reopen_refusal_wrong_root.json').read_text())
    digest=json.loads((root/'proof'/'digest_refusal.json').read_text())
    assert revoked['refused'] and 'authority' in revoked['error']
    assert wrong['refused'] and 'roots mismatch' in wrong['error']
    assert digest['before_deserialization'] is True
    assert build['source_rows']==5
    assert len(build['family_counts'])==13
    assert reopen['family_counts']==build['family_counts']
    assert refusal['refused'] is True and refusal['before_source'] is True
    assert refusal['error_type']=='SourceI02Refusal'
