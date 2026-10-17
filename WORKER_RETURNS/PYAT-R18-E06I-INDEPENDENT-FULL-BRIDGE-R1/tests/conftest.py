import os
import sys

CAND = os.environ.get('E06_CANDIDATE_ROOT')
if not CAND:
    for cand in (
        '/tmp/e06i/court/WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-E06-E04E05-NATIVE-BRIDGE-R1',
        os.path.join(os.getcwd(), 'WORKER_RETURNS',
                     'PYAT-USERDIRECT-20261016-R17-E06-E04E05-NATIVE-BRIDGE-R1'),
    ):
        if os.path.exists(os.path.join(cand, 'bridge.py')):
            CAND = cand
            break
if not CAND or not os.path.exists(os.path.join(CAND, 'bridge.py')):
    raise RuntimeError(
        'set E06_CANDIDATE_ROOT to the staged candidate return directory '
        '(agent/userdirect-pyat-20261016-r17-e06-e04e05-native-bridge-r1 @ '
        'f9c52113de38caececc450f0e54c980f64ed3981, repro/stage_sources.py already run)')
CAND = os.path.abspath(CAND)
os.environ['E06_CANDIDATE_ROOT'] = CAND
RT = os.path.join(CAND, 'runtime')
if not os.path.exists(os.path.join(RT, 'owners', 'e04t_empirical.py')):
    raise RuntimeError('candidate runtime/ is not staged; run repro/stage_sources.py in ' + CAND)

sys.path[:0] = [os.path.join(CAND, 'repro'), CAND, os.path.join(RT, 'owners'), RT,
                os.path.join(RT, 'rawlsing_next', 'tests'), os.path.join(RT, 'rawlsing_next')]
