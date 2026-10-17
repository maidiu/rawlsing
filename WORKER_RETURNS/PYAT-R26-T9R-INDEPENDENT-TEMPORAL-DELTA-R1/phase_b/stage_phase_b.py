"""Byte-preserving Phase B transport; never executes the candidate."""
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
RET = ROOT.parent
REPO = RET.parents[1]
CAND = '9a33c2dcaa7ac0d50606416ab965488c9782934b'
PREFIX = 'WORKER_RETURNS/PYAT-R26-T9C-TEMPORAL-ADAPTER-SEVEN-RED-CONTINUATION-R1/'
FREEZE = '68c5c2a15d234fe2589083af17e6f0dbc2f60d5a'

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])

def main():
    for item in json.loads((RET/'01C_PHASE_A_FREEZE_MANIFEST.json').read_text())['files']:
        b = (RET/item['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == item['sha256'], item
        assert b == git('show', FREEZE+':'+str((RET/item['path']).relative_to(REPO)))
    for folder in ['evidence', 'junit', 'logs', 'tests', 'pinned_candidate']:
        (ROOT/folder).mkdir(exist_ok=True)
    manifest = []
    def copy(b, rel, rev, source):
        dest = ROOT/rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b)
        oid = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        manifest[:] = [m for m in manifest if m['relative'] != (str(dest.relative_to(ROOT/'pinned_candidate')) if dest.is_relative_to(ROOT/'pinned_candidate') else '../'+rel)]
        manifest.append(dict(relative=str(dest.relative_to(ROOT/'pinned_candidate')) if dest.is_relative_to(ROOT/'pinned_candidate') else '../'+rel,
                             source_commit=rev, candidate_git_path=source,
                             git_blob_sha1=oid, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b)))
    paths = git('ls-tree', '-r', '--name-only', CAND, '--', PREFIX).decode().splitlines()
    for path in paths:
        rel = path.removeprefix(PREFIX)
        if rel.startswith('native/') or rel in ['t9b_temporal.py', 'test_t9c_repair.py', '01_SEVEN_DEFECT_CONTRACTS.json']:
            copy(git('show', CAND+':'+path), 'pinned_candidate/'+rel, CAND, path)
    # Original author and V553 tests, original artifact and BOTH independent courts
    # come from the already-pushed Phase A, not author's retransport.
    for rel in ['pinned_candidate/test_t9b_temporal.py',
                'pinned_candidate/01_PREDECLARED_SERIES_CLOCK_ORACLE.json',
                'pinned_candidate/evidence/native_source_ledger.json',
                'pinned_candidate/native/data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py',
                'pinned_candidate/evidence/02_real_temporal_to_selected_world_two_times.json',
                'tests/test_independent_clock_custody.py','tests/test_t9r_delta.py',
                '01B_FROZEN_COUPLED_BINDING_VECTORS.json', 'pytest.ini']:
        src = str((RET/rel).relative_to(REPO))
        copy(git('show', FREEZE+':'+src), rel, FREEZE, src)
    for rel in ['phase_b_direct_bindings.py', 'tests/test_postinspection_hostiles.py']:
        b = (ROOT/rel).read_bytes()
        manifest.append(dict(relative='../'+rel, source_commit=None, reviewer_created=True,
                             git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),
                             sha256=hashlib.sha256(b).hexdigest(), bytes=len(b)))
    (ROOT/'evidence/staged_source_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    native = [m for m in manifest if m['relative'].startswith('native/')]
    inherited = {r['relative']:r for r in json.loads((RET/'evidence/staged_source_manifest.json').read_text())}
    assert all(m['git_blob_sha1'] == inherited[m['relative']]['git_blob_sha1'] for m in native)
    changed = git('diff', '--name-only', '79cf24ee615ec24bee2dc8584b31fb6b240fd3cf', CAND).decode().splitlines()
    assert all(p.startswith(PREFIX) for p in changed)
    receipt = dict(candidate=CAND, at_utc=datetime.now(timezone.utc).isoformat(),
                   phase_a_payload=FREEZE, phase_a_freeze_verified=True,
                   final_publication_receipt=PREFIX+'05_REMOTE_VERIFICATION.json',
                   native_files=len(native), native_original_blob_matches=len(native),
                   archival_audit_inherited='../evidence/source_audit_summary.json',
                   archival_files=1259, unchanged_author_and_independent_assertions=True,
                   changed_candidate_paths=changed, source_author_modifications=False)
    (ROOT/'evidence/gate_and_transport.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
