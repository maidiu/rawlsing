"""Current cold replay: 81 enumerated count tables plus genuine zero support risk."""
import hashlib
import json
import os
import sys
from pathlib import Path
RET = Path(__file__).resolve().parents[1]
FROZEN = Path(os.environ['GF1_CURRENT_FROZEN_GF1F']).resolve()
for path in (FROZEN/'repro',FROZEN/'candidate/court/repro',FROZEN/'candidate/court/runtime_root'):
    sys.path.insert(0,str(path))
import gf1_pair_support_consumer as C
from independent_relation import build_relation
oracle = json.loads((RET/'01_CURRENT_PAIR_ORACLE.json').read_text())
results = {}
class_counts = {}
for index,row in enumerate(oracle['universe']+oracle['cold_extra_cases']):
    key = row.get('case_id') or '%d%d%d%d' % tuple(row['cells'][k] for k in ('00','01','10','11'))
    assert key not in results
    out = C.compute_pair_support_signature(build_relation(row['cells'],eligible=row['eligible']))
    results[key] = out['separation_class']
    class_counts[out['separation_class']] = class_counts.get(out['separation_class'],0)+1
source = Path(C.__file__).resolve()
Path(sys.argv[1]).write_text(json.dumps(dict(pid=os.getpid(),consumer_file=str(source),consumer_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),class_counts=class_counts,results=results),sort_keys=True)+'\n')
