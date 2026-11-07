import sys, tempfile
from pathlib import Path
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1')
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests')
sys.path.insert(0,'WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1')
from p3 import p3_owner
from developmental_recursion.contracts import EventProposal, digest
import test_p3_owner as T

def scenario(root, first_phase):
    fanin, owner, initial, source_hash, config, first = T._build(root, history=True, phase=first_phase)
    second = EventProposal('same-control-second', initial.clock+12, 'ADMIT_EVENT', (owner.source_ref,), owner.participants, {})
    second_plan = T._plan(initial, second, source_hash, phase='RECRUIT', counterpart='owner-counterpart')
    config['plans']=[config['plans'][0], second_plan]
    p3=p3_owner.P3Owner(owner, **config)
    try:
        r1=p3.realize('first-'+first_phase, first, p3.snapshot())
        r2=p3.realize('second-'+first_phase, second, p3.snapshot())
        return p3.store.head(), r1.consequences['test_only_psychological'], r2.consequences['test_only_psychological']
    finally:
        p3.close()

for phase in ('FORMATION','STABILITY'):
    root=Path(tempfile.mkdtemp(prefix='p3-same-hist-'+phase+'-'))
    head,r1,r2=scenario(root, phase)
    print('phase',phase,'head',head)
    print(' first streams',[(s['mode'],s.get('record_hash')) for s in r1['streams']])
    print(' second streams',[(s['mode'],s.get('record_hash')) for s in r2['streams']])
