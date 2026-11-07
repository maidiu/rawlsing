import sys, tempfile, json
from pathlib import Path
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1')
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests')
sys.path.insert(0,'WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1')
import test_p3_vertical_slice as T
case=T.build_case(Path(tempfile.mkdtemp(prefix='p3-compress-four-')))
try:
    for i,p in enumerate(case.proposals[:4]):
        r=case.owner.realize(f'compress-four-{i}', p, case.owner.snapshot())
        ev=r.consequences.get('test_only_compression_evidence')
        print(i+1, 'status', r.status, 'exceptional', r.consequences.get('test_only_psychological',{}).get('status'), 'form', (ev or {}).get('representation_form'), 'compression_status', (ev or {}).get('status'), 'held_reason', (ev or {}).get('held_reason'), 'actual_action', (ev or {}).get('actual_action_ref'), 'perceptions', len((ev or {}).get('perception_refs') or []), 'interval', (ev or {}).get('actual_interval_status'))
finally:
    case.owner.close()
