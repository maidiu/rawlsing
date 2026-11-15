import sys, tempfile
from pathlib import Path
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1')
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests')
sys.path.insert(0,'WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1')
import test_p3_vertical_slice as T
from p3 import compression
case=T.build_case(Path(tempfile.mkdtemp(prefix='p3-compress-crash-')))
try:
    original=compression.bind
    def fail(*a,**k): raise RuntimeError('INJECTED_COMPRESSION_BIND_FAILURE')
    compression.bind=fail
    try:
        case.owner.realize('compress-crash-op', case.proposals[0], case.owner.snapshot())
    except Exception as e:
        print('first exception', type(e).__name__, str(e)[:200])
    compression.bind=original
    print('phase after failure', case.owner.store.get_operation('compress-crash-op')['phase'])
    result=case.owner.realize('compress-crash-op', case.proposals[0], case.owner.snapshot())
    print('recovered status', result.status, 'compression evidence?', 'test_only_compression_evidence' in result.consequences)
    print('operation phase', case.owner.store.get_operation('compress-crash-op')['phase'])
finally:
    case.owner.close()
