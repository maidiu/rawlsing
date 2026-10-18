"""Independent fresh-process causal receipt canonicalization for Phase A."""
import json
from frozen_oracle import run
from preregistered_cases import CASES
q=next(x['input'] for x in CASES if x['id']=='A08')
print(json.dumps({'version':'ONECALL_C0F_COLD_SOURCEFREE@1','result':run(q)},sort_keys=True,separators=(',',':')))
