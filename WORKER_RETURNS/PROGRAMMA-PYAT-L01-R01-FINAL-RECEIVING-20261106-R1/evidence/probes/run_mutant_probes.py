import hashlib, json, os, subprocess, sys
from pathlib import Path

ROOT = Path('/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/r01-cold-702')
EVID = Path('/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/r01-receive-evidence')
PDEPS = str(EVID / 'pydeps')
contracts = [
    ROOT/'rawlsing_next/tests/test_l01_evidence_world_consumer.py.proof.json',
    ROOT/'rawlsing_next/tests/test_universal_evidence_binding.py.proof.json',
    ROOT/'rawlsing_next/tests/test_universal_world_binding.py.proof.json',
    ROOT/'rawlsing_next/tests/test_world_conditioned_progressive_service.py.proof.json',
]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
env['PYTHONPATH'] = PDEPS + os.pathsep + env.get('PYTHONPATH','')
results = []
for cfile in contracts:
    doc = json.loads(cfile.read_text())
    for claim in doc['claims']:
        target = ROOT / claim['fault']['path']
        before = target.read_text()
        old, new = claim['fault']['old'], claim['fault']['new']
        assert before.count(old) == 1, (cfile, before.count(old))
        sha_before = hashlib.sha256(before.encode()).hexdigest()
        rec = {'claim_id': claim['claim_id'], 'contract': str(cfile.relative_to(ROOT)),
               'positive_node': claim['positive_node'], 'fault_path': claim['fault']['path']}
        try:
            target.write_text(before.replace(old, new, 1))
            proc = subprocess.run(
                [sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                 '--tb=long', claim['positive_node']],
                cwd=ROOT, env=env, text=True, capture_output=True, timeout=1200)
            rec['returncode'] = proc.returncode
            out = proc.stdout + proc.stderr
            rec['failure_lines'] = [line for line in out.splitlines()
                                    if line.startswith('E   ') or line.startswith('>') or 'AssertionError' in line][-12:]
            rec['tail'] = out.splitlines()[-25:]
        finally:
            target.write_text(before)
            sha_after = hashlib.sha256(target.read_text().encode()).hexdigest()
            rec['source_restored'] = sha_before == sha_after
        results.append(rec)
        print(json.dumps(rec, indent=2))
        print('-----')
(EVID/'mutant-probes.json').write_text(json.dumps(results, indent=2) + '\n')
