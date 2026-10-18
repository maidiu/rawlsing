"""Independent original/candidate collision probe, with complete SQL snapshots."""
from pathlib import Path
from copy import deepcopy
import json, os, sys
sys.path.insert(0, os.environ['B2_REVIEW_ROOT'])
import bridge as m

def tables(db):
    names=[r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    return {name:db.execute('SELECT * FROM '+name+' ORDER BY 1').fetchall() for name in names}

def main(output):
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        initial=m.b1.initialize(m.b1.prehistory())
        b=m.Bridge(Path(temp)/'state.sqlite', initial)
        packet, context, policy=m.input_pair(b.store.state())
        witness=m.occurrence_witness(b.store.state(),packet,context)
        cap, registry=m.capability_fixture()
        b.witnesses={witness['hash']:witness};b.capability_witnesses=registry
        sql=[];b.store.db.set_trace_callback(sql.append)
        before=tables(b.store.db)
        first=b.advance(packet,context,policy,witness,cap,grant=False)
        middle=tables(b.store.db)
        altered=deepcopy(witness);altered.pop('hash');altered['objective_occurrence']='E2_DIFFERENT_MATERIAL_OCCURRENCE'
        altered=m.b1.sealed(altered);b.witnesses[altered['hash']]=altered
        second=b.advance(packet,context,policy,altered,cap,grant=False)
        after=tables(b.store.db)
        result=dict(inputs=dict(initial=initial,packet=packet,context=context,policy=policy,witness=witness,altered=altered,capability=cap,registry=registry),first=first,second=second,before=before,middle=middle,after=after,sql_trace=sql)
        assert b.store.state()==json.loads(before['checkpoint'][0][1])
        if 'b2_event_identity' in after:
            assert len(after['occurrence'])==1 and after==middle
            assert second['reason']=='EVENT_IDENTITY_CONFLICT' and second['event_admission']=='NOT_PERFORMED'
            assert not second['b1_invoked']
        else:
            assert len(after['occurrence'])==2
            assert len({json.loads(r[1])['event_id'] for r in after['occurrence']})==1
        Path(output).write_text(json.dumps(result,indent=2)+'\n')
        b.close()

if __name__=='__main__':main(sys.argv[1])
