"""Independent exact-object materialization and executable review. No candidate edits."""
from pathlib import Path
import hashlib, importlib.util, io, json, os, shutil, subprocess, sys, tarfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
STAGE = ROOT / '.runtime'
EVIDENCE = ROOT / 'evidence'
BASE = '950ecf0b3816ea7d0dd3ab48b62c92cedfe0e883'
R1 = '358fd1086eac0a4aa7791ca14abc25c45b935ddd'
X2 = '931aec3497c60114444806c375d1bb51ec7c0e7d'
B2_PATH = 'WORKER_RETURNS/SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1'
R1_PATH = 'WORKER_RETURNS/SOROK-V2-HQ327-R1-EVENT-IDENTITY-REPAIR-R1'
X2_PATH = 'WORKER_RETURNS/SOROK-V2-HQ326-X2-B2-INDEPENDENT-EXECUTABLE-R1'
PINS = {
    'B1': ('c0f4588c158b40c8903b4aae2f292eae5238b8a0', 'SOROK-V2-HQ324-B1-COUPLED-DEVELOPMENT-R1'),
    'P1': ('fb4fa049b6e3dd9df8d25a4f42a2b41e9d737c60', 'SOROK-V2-HQ324-P1-PROPOSAL-ADMISSION-R1'),
    'D1': ('2e3f3e48293bdcd5774b9465909f16d537e48e35', 'SOROK-V2-HQ324-D1-DEVELOPMENTAL-SCIENCE-R1'),
    'F1': ('ed367d96af66d816a01dd651b91f0af285762c82', 'SOROK-V2-HQ324-F1-INDEPENDENT-DEVELOPMENTAL-FALSIFIERS-R1'),
}

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

def tree(commit, prefix):
    for line in git('ls-tree', '-r', commit, prefix).decode().splitlines():
        meta, path = line.split('\t')
        blob = meta.split()[2]
        data = git('cat-file', 'blob', blob)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == blob
        yield path, data, dict(commit=commit, source_path=path, git_blob_sha1=blob, sha256=sha(data), bytes=len(data))

def materialize(phase):
    dest = STAGE / phase
    dest.mkdir(parents=True, exist_ok=True)
    manifest = []
    for path, data, row in tree(BASE, B2_PATH):
        target = dest / Path(path).relative_to(B2_PATH)
        if phase == 'repaired' and target.name == 'bridge.py':
            data = git('show', R1+':'+path)
            row = dict(commit=R1, source_path=path, git_blob_sha1=git('rev-parse', R1+':'+path).decode().strip(), sha256=sha(data), bytes=len(data))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        manifest.append(dict(row, staged_path=str(target.relative_to(ROOT))))
    # Independent transport and archive validation, without using author's manifest as oracle.
    inherited = []
    for component, (commit, folder) in PINS.items():
        prefix = 'WORKER_RETURNS/'+folder
        for path, data, row in tree(commit, prefix):
            target = dest / 'imports' / component / Path(path).relative_to(prefix)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            inherited.append(dict(row, component=component, materialized_path=str(target.relative_to(dest))))
    archive = dest / 'imports/F1/F1_frozen_court.tar.gz'
    with tarfile.open(fileobj=io.BytesIO(archive.read_bytes())) as tar:
        for member in tar.getmembers():
            assert not member.issym() and not member.islnk()
            target = dest / 'imports/F1/court' / member.name
            assert target.resolve().is_relative_to(dest.resolve())
            if member.isfile():
                data = tar.extractfile(member).read()
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                inherited.append(dict(component='F1_ARCHIVE_MEMBER', archive_sha256=sha(archive.read_bytes()), archive_member=member.name, materialized_path=str(target.relative_to(dest)), sha256=sha(data)))
    assert len(inherited) == 69
    dump(dest/'imported_sources.json', inherited)
    manifest.extend(dict(row, staged_path=str((dest/row['materialized_path']).relative_to(ROOT))) for row in inherited)
    dump(EVIDENCE/phase/'source_manifest.json', manifest)
    return dest, manifest

def sanitize(path):
    if path.suffix == '.xml':
        t = ET.parse(path)
        for node in t.iter():
            node.attrib.pop('hostname', None)
            for key, value in node.attrib.items(): node.set(key, portable(value))
            if node.text: node.text = portable(node.text)
            if node.tail: node.tail = portable(node.tail)
        t.write(path, encoding='utf-8', xml_declaration=True)
    elif path.suffix in ('.json', '.log'):
        path.write_text(portable(path.read_text()))

def portable(s):
    return s.replace(str(ROOT), '<E2>').replace(str(REPO), '<WORKTREE>').replace(str(Path.home()), '<HOME>')

def main():
    EVIDENCE.mkdir(exist_ok=True)
    frozen = STAGE/'frozen'
    frozen.mkdir(parents=True, exist_ok=True)
    (frozen/'test_hostile_x2.py').write_bytes(git('show', X2+':'+X2_PATH+'/test_hostile_x2.py'))
    author = STAGE/'R1'
    author.mkdir(exist_ok=True)
    for path, data, row in tree(R1, R1_PATH):
        if path.endswith('.py'):
            target = author/Path(path).relative_to(R1_PATH)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    assert (author/'frozen/test_hostile_x2.py').read_bytes() == (frozen/'test_hostile_x2.py').read_bytes()
    changed = git('diff', '--name-only', BASE, R1).decode().splitlines()
    assert all(p == B2_PATH+'/bridge.py' or p.startswith(R1_PATH+'/') or p.startswith('WORKER_COMMISSIONS/') for p in changed)
    candidate_changes = git('diff', '--name-only', 'a52fc56c72b2a0496356a68c9a9e8563edf1c107', R1).decode().splitlines()
    assert all(p == B2_PATH+'/bridge.py' or p.startswith(R1_PATH+'/') for p in candidate_changes)
    dump(EVIDENCE/'candidate_delta.json', dict(changed_from_original=changed, changed_since_seal=candidate_changes))
    env = dict(os.environ, GIT_DIR=git('rev-parse', '--path-format=absolute', '--git-common-dir').decode().strip(), PYTHONDONTWRITEBYTECODE='1')
    commands = []
    def run(args, cwd, label, expected, extra=None):
        out = EVIDENCE/label
        out.parent.mkdir(parents=True, exist_ok=True)
        p = subprocess.run(args, cwd=cwd, env=dict(env, **(extra or {})), capture_output=True, text=True)
        out.with_suffix('.log').write_text(portable(p.stdout+p.stderr))
        commands.append(dict(command=[portable(str(x)) for x in args], cwd=portable(str(cwd)), label=label, exit=p.returncode, expected_exit=expected,
            environment=dict(GIT_DIR='<EXISTING_SHARED_GIT_OBJECT_STORE>',PYTHONDONTWRITEBYTECODE='1',**{k:portable(v) for k,v in (extra or {}).items()})))
        dump(EVIDENCE/'commands.json', commands)
        assert p.returncode == expected, (label, p.returncode, p.stdout[-1000:], p.stderr[-1000:])
    manifests = {}
    for phase in ('original', 'repaired'):
        dest, manifests[phase] = materialize(phase)
        run([sys.executable, 'run_courts.py'], dest, phase+'/inherited', 0)
        shutil.copytree(dest/'evidence', EVIDENCE/phase/'inherited', dirs_exist_ok=True, ignore=shutil.ignore_patterns('*.sqlite', '*.sqlite-*'))
        shutil.copyfile(dest/'execution_receipt.json', EVIDENCE/phase/'execution_receipt.json')
        extra = dict(B2_REVIEW_ROOT=str(dest), E2_EVIDENCE=str(EVIDENCE/phase/'sql'))
        run([sys.executable, '-m', 'pytest', '-q', str(frozen/'test_hostile_x2.py'), '--junitxml='+str(EVIDENCE/phase/'x2.xml')], dest, phase+'/x2', 0 if phase == 'original' else 1, extra)
        x2 = ET.parse(EVIDENCE/phase/'x2.xml').find('testsuite')
        failed = [c.get('name') for c in x2.findall('testcase') if c.find('failure') is not None]
        assert failed == ([] if phase == 'original' else ['test_same_event_id_accepts_distinct_objective_payload_hashes'])
        run([sys.executable, str(ROOT/'probe_e2.py'), str(EVIDENCE/phase/'collision.json')], dest, phase+'/collision', 0, extra)
        run([sys.executable, str(ROOT/'runtime_probe.py'), str(EVIDENCE/phase/'runtime.json')], dest, phase+'/runtime', 0, extra)
        if phase == 'repaired':
            concurrency = EVIDENCE/phase/'r1_concurrency'; concurrency.mkdir(exist_ok=True)
            run([sys.executable, '-m', 'pytest', '-q', str(author/'test_identity.py'), '--junitxml='+str(EVIDENCE/phase/'r1.xml')], dest, phase+'/r1', 0, dict(extra, R1_EVIDENCE=str(concurrency)))
            run([sys.executable, '-m', 'pytest', '-q', str(ROOT/'test_e2.py'), '--junitxml='+str(EVIDENCE/phase/'e2.xml')], dest, phase+'/e2', 1, extra)
            suite=ET.parse(EVIDENCE/phase/'e2.xml').find('testsuite')
            failures=[c.get('name') for c in suite.findall('testcase') if c.find('failure') is not None]
            assert failures == ['test_legacy_after_mapping_must_fail_closed_at_b2_reentry[False]', 'test_legacy_after_mapping_must_fail_closed_at_b2_reentry[True]']
        # Hash actual files after execution against independently retrieved original preimages.
        for row in manifests[phase]:
            path = ROOT/row['staged_path']
            if '/evidence/' in str(path) or path.name in ('execution_receipt.json',): continue
            assert sha(path.read_bytes()) == row['sha256'], str(path)
        print(phase+' independently executed and source-verified', flush=True)
    for phase in ('original', 'repaired'):
        for mode in ('positive', 'journal_only'):
            rel='inherited/vertical/'+mode+'/trace.json'
            assert (EVIDENCE/'original'/rel).read_bytes() == (EVIDENCE/'repaired'/rel).read_bytes()
    for p in EVIDENCE.rglob('*'):
        if p.is_file(): sanitize(p)
    print('E2 execution complete', flush=True)

if __name__ == '__main__': main()
