from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
RUN=HERE/'testonly_bundle'/'run.py'
def test_existing_small_sourcefree_typed_bundle_builds_reopens_and_refuses():
    p=subprocess.run([sys.executable,'-B',str(RUN)],cwd=str(HERE),text=True,capture_output=True,env={**__import__('os').environ,'PYTHONPATH':str(HERE.parents[2]),'PYTHONDONTWRITEBYTECODE':'1'})
    assert p.returncode==0,p.stdout+p.stderr
    assert 'TESTONLY_BUNDLE_PASS' in p.stdout
    build=json.loads((HERE/'testonly_bundle'/'proof'/'build.json').read_text())
    reopen=json.loads((HERE/'testonly_bundle'/'proof'/'reopen.json').read_text())
    refusal=json.loads((HERE/'testonly_bundle'/'proof'/'refusal.json').read_text())
    assert build['source_rows']==5
    assert len(build['family_counts'])==13
    assert reopen['family_counts']==build['family_counts']
    assert refusal['refused'] is True and refusal['before_source'] is True
    assert refusal['error_type']=='SourceI02Refusal'
