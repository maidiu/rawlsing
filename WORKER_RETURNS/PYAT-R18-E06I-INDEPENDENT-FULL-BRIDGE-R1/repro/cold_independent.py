"""Independent cold-process replay for the E06I court.

Loads a persisted fixture-grant ledger, attaches it to a brand-new process's
bridge before any empirical query, then:
  * performs the real prepare/read;
  * injects a prior-process public cache projection into a second bridge and
    proves it is not accepted as an owner entry.

argv: <ledger.json> <dest.json>
env : E06_CANDIDATE_ROOT (staged candidate return directory)
"""
import hashlib
import json
import os
import sys
from pathlib import Path

CAND = os.environ.get('E06_CANDIDATE_ROOT')
if not CAND or not os.path.exists(os.path.join(CAND, 'bridge.py')):
    raise SystemExit('E06_CANDIDATE_ROOT must point at the staged candidate return directory')
CAND = os.path.abspath(CAND)
RT = os.path.join(CAND, 'runtime')
sys.path[:0] = [os.path.join(CAND, 'repro'), CAND, os.path.join(RT, 'owners'), RT,
                os.path.join(RT, 'rawlsing_next', 'tests'), os.path.join(RT, 'rawlsing_next')]

from support import bridge, request, hydrate, AuthorityRegistry  # noqa: E402
from observe import Observer  # noqa: E402

ledger_path, dest = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
ledger = json.loads(Path(ledger_path).read_text())

obs = Observer()
obs.start()
b = bridge()
b.provider.world['registry'] = AuthorityRegistry(hydrate(x) for x in ledger['grants'])
out = b.read(b.prepare(request()))
obs.stop()
trace = obs.result()

# A prior-process public projection is never a trusted owner entry.
f = bridge()
f.provider.world['registry'] = AuthorityRegistry(hydrate(x) for x in ledger['grants'])
f.provider.cache[('Y', (('A', 1),))] = ledger['projection']
try:
    f.prepare(request())
except ValueError as exc:
    foreign_reason = str(exc)
else:
    raise AssertionError('FOREIGN_PROCESS_PROJECTION_ACCEPTED')

Path(dest).write_text(json.dumps(dict(
    pid=os.getpid(),
    ledger_state=ledger['state'],
    ledger_sha256=hashlib.sha256(Path(ledger_path).read_bytes()).hexdigest(),
    grant_ledger_attached_before_first_query=True,
    result=out,
    foreign_projection_reason=foreign_reason,
    frames=trace['actual_frames'],
    imports=len(trace['imports']),
), separators=(',', ':')) + '\n')
print('E06I COLD', ledger['state'], out['state'], 'imports', len(trace['imports']))
