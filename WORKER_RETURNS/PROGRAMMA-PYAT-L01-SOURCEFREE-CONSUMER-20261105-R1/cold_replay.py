"""Build and replay a one-commit checkout with no historical Git objects.

Run from the candidate checkout: python3 WORKER_RETURNS/.../cold_replay.py
Only the declared current source/test closure and four sourcefree JSON freezes
are copied. The host's Git object database is never cloned or shared.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FIXTURES = (
    'WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/02_VALUE_RELATION_ORACLE.json',
    'WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json',
    'WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json',
    'WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/04_CURRENT_AT07_IDENTITY_SPINE.json',
)
HISTORICAL = ('f27d1101048638bba395143a48efb7ef00bfcda4',
              'f53cb0d2bce52640268c844c398bbd8007d28edc',
              '849a76de18ef627c3c403b426ebe70f0951a7e7b')


def run(argv, cwd, log, env=None):
    with (OUT/'logs'/log).open('w') as handle:
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=handle,
                                stderr=subprocess.STDOUT)
    if result.returncode: raise RuntimeError(f'{log}: exit {result.returncode}')


def main():
    base = Path(tempfile.mkdtemp(prefix='l01-hermetic-'))
    checkout = base/'checkout'; checkout.mkdir()
    paths = subprocess.check_output(['git','ls-files','rawlsing_next'], cwd=ROOT, text=True).splitlines()
    paths = [path for path in paths if path.endswith('.py')] + list(FIXTURES)
    manifest = []
    for name in sorted(paths):
        source = ROOT/name; target = checkout/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        manifest.append({'path': name, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    (OUT/'cold-source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    run(['git','init','-q'],checkout,'cold-git-init.log')
    run(['git','add','.'],checkout,'cold-git-add.log')
    run(['git','-c','user.name=L01 cold replay','-c','user.email=l01@example.invalid',
         'commit','-qm','Current sourcefree closure only'],checkout,'cold-git-commit.log')
    absent = {sha: subprocess.run(['git','cat-file','-e',sha+'^{commit}'],cwd=checkout,
              capture_output=True).returncode != 0 for sha in HISTORICAL}
    assert all(absent.values())
    assert subprocess.check_output(['git','rev-list','--count','HEAD'],cwd=checkout,text=True).strip() == '1'
    assert not subprocess.check_output(['git','remote'],cwd=checkout,text=True).strip()
    run([sys.executable,'-m','venv',str(base/'venv')],checkout,'cold-venv.log')
    python = str(base/'venv/bin/python')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0',
               PYTHONPATH=str(checkout), PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    run([python,'-m','pip','--isolated','install','--index-url','https://pypi.org/simple',
         '-r',str(OUT/'requirements-cold.txt')],checkout,'cold-install.log',env)
    run([python,'-m','pip','freeze'],checkout,'cold-dependency-lock.txt',env)
    tests = ['test_l01_evidence_world_consumer.py','test_universal_evidence_binding.py',
             'test_l01_reviewed_progressive_world.py','test_world_conditioned_progressive_service.py',
             'test_universal_world_binding.py']
    run([python,'-m','pytest','-q','--tb=short','--junitxml='+str(OUT/'logs/cold-junit.xml'),
         *['rawlsing_next/tests/'+name for name in tests],
         '-k','not j42 and not context_authority'],checkout,'cold-tests.log',env)
    run([python,'-m','rawlsing_next.tests.l01_sourcefree_replay'],checkout,'cold-trace.json',env)
    child = json.loads((OUT/'logs/cold-trace.json').read_text())
    run([sys.executable,'-m','rawlsing_next.tests.l01_sourcefree_replay'],ROOT,'warm-final-trace.json',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    parent = json.loads((OUT/'logs/warm-final-trace.json').read_text())
    assert child == parent, 'cold consumer output/source closure differs'
    result = {'state':'PASS','historical_objects_absent':absent,'remote_count':0,
              'checkout_commit_count':1,'clean_checkout':not subprocess.check_output(['git','status','--porcelain'],cwd=checkout,text=True).strip(),
              'trace_byte_identical':(OUT/'logs/cold-trace.json').read_bytes()==(OUT/'logs/warm-final-trace.json').read_bytes(),
              'output_hash':child['output_hash'],'fresh_venv':True,'source_files':len(manifest),
              'external_test_dependencies':'requirements-cold.txt; resolved versions in logs/cold-dependency-lock.txt','checkout_path':str(checkout)}
    assert result['clean_checkout'] and result['trace_byte_identical']
    (OUT/'cold-replay-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
