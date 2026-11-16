import sys, tempfile, json
from pathlib import Path
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1')
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests')
sys.path.insert(0,'WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1')
import test_p3_vertical_slice as T
case=T.build_case(Path(tempfile.mkdtemp(prefix='p3-compress-one-')))
try:
    r=case.owner.realize('compress-one-1', case.proposals[0], case.owner.snapshot())
    print('accessible', r.accessible.get('status'), r.accessible.get('actor_ref'), 'events', [(e.get('event_id'),e.get('perception')) for e in r.accessible.get('events',[])])
    print('compression', json.dumps(r.consequences.get('test_only_compression_evidence'), indent=2)[:3000])
finally:
    case.owner.close()
