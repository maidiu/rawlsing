"""Actual source-custody attacks, supplementary to the immutable Phase A tests.

Run only after positive replay. Mutate one preimage at a time; always restore
its exact bytes. These are deliberate hostile stimuli, never candidate repairs.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

R = Path(os.environ['WG0P11_ROOT']).resolve()
C = R / 'candidate'
COURT = C / 'court'
OUT = Path(os.environ['WG0P11_EVIDENCE']).resolve()
OUT.mkdir(parents=True, exist_ok=True)
REPAIRED = C / 'court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py'
DIRECT = C / 'court/runtime_phase_b/candidate/repro/wg0p4_workload.py'
MISSING = C / 'court/runtime_phase_b/candidate/pinned/predecessors/j/observations/cold_checkpoint.json'
PAYLOAD = "print('PAYLOAD_STARTED',flush=True); from phase_b_support_v1 import plan,execute; execute(plan()); print('EXECUTED_NATIVE_I03',flush=True)"


def run(label, args, bootstrap=False):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    env.pop('PYTHONPATH', None)
    if bootstrap:
        env['PYTHONPATH'] = os.pathsep.join([str(COURT/'bootstrap_p6'), str(COURT/'repro')])
    cmd = [sys.executable, '-B', *args]
    p = subprocess.run(cmd, cwd=COURT if bootstrap else R, env=env,
                       capture_output=True, text=True, timeout=120)
    receipt = dict(command=cmd, cwd=str(COURT if bootstrap else R),
                   exit=p.returncode, stdout=p.stdout, stderr=p.stderr)
    (OUT/(label+'.json')).write_text(json.dumps(receipt, indent=2)+'\n')
    return receipt


def verify(label):
    return run(label, [str(R/'repro/wg0p8_publication.py'), 'verify'])


def main():
    assert verify('hostile_initial_baseline')['exit'] == 0
    results = []
    for label, path, replacement in [
        ('omitted_restored_source', MISSING, None),
        ('changed_source_hash', MISSING, MISSING.read_bytes()+b'\nWG0P11_INTENTIONAL_HOSTILE\n'),
        ('pristine_wrong_P5', REPAIRED, DIRECT.read_bytes()),
    ]:
        original = path.read_bytes()
        try:
            if replacement is None:
                path.unlink()
            else:
                path.write_bytes(replacement)
            v = verify(label+'_verifier')
            b = run(label+'_bootstrap', ['-c', PAYLOAD], bootstrap=True)
            assert v['exit'] == 86 and 'WG0P8_PRE_I03_REFUSE:' in v['stderr'], v
            assert b['exit'] == 86 and 'WG0P6_BOOTSTRAP_REFUSE:' in b['stderr'], b
            assert 'PAYLOAD_STARTED' not in b['stdout'], b
            assert 'EXECUTED_NATIVE_I03' not in b['stdout'], b
            results.append(dict(case=label, verifier_exit=v['exit'], bootstrap_exit=b['exit'],
                                payload_started=False, new_I03_calls=0,
                                zero_I03_basis='bootstrap terminates before any payload statement'))
        finally:
            path.write_bytes(original)
        assert verify(label+'_restored_baseline')['exit'] == 0
    (OUT/'actual_source_hostiles_summary.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
