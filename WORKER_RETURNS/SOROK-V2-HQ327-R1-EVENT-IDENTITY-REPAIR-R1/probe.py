"""Reproduce X2 collision, retaining complete inputs and raw SQLite rows."""
import json, os, sys, tempfile
from pathlib import Path
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m
from copy import deepcopy
with tempfile.TemporaryDirectory() as tmp:
    initial=m.b1.initialize(m.b1.prehistory());b=m.Bridge(Path(tmp)/'state.sqlite',initial)
    packet,context,policy=m.input_pair(initial)
    witness=m.occurrence_witness(initial,packet,context)
    cap,registry=m.capability_fixture();b.capability_witnesses=registry
    b.witnesses={witness['hash']:witness}
    first=b.advance(packet,context,policy,witness,cap,grant=False)
    changed=deepcopy(witness);changed.pop('hash');changed['objective_occurrence']='DIFFERENT_OBJECTIVE_EVENT'
    changed=m.b1.sealed(changed);b.witnesses[changed['hash']]=changed
    second=b.advance(packet,context,policy,changed,cap,grant=False)
    rows=[dict(hash=h,body=body) for h,body in b.store.db.execute('SELECT hash,body FROM occurrence ORDER BY hash')]
    result=dict(initial=initial,packet=packet,context=context,policy=policy,witnesses=[witness,changed],capability=cap,registry=registry,first=first,second=second,raw_occurrence_rows=rows,checkpoint=b.store.state())
    Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(occurrences=len(rows),second_status=second['status'],reason=second.get('reason'))))
    b.close()
