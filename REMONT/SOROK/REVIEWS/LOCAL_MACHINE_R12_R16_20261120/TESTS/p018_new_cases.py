import tempfile, unittest
from pathlib import Path
from um_sorok_organism.storage import ResearchLedger, Conflict
from um_sorok_organism.types import adult, blank_world

def ledger(path):
    l=ResearchLedger(str(path))
    l.initialize(blank_world(),[adult('amy','Amy')],source_seals=[('seed','CONDITIONING_NOT_REAL_PERSON',{'truth':'A'})])
    v,w=l.world(); l.commit('w1',v,w,{}, {},'OBJECTIVE_CUE',None,{'event':'ordinary'})
    assert l.verify_chain()['valid']
    return l

class NewP018(unittest.TestCase):
    def test_noncanonical_initialization_payload_must_refuse_source_read(self):
        with tempfile.TemporaryDirectory() as d:
            l=ledger(Path(d)/'x.sqlite')
            try:
                raw=l.conn.execute('SELECT payload FROM events WHERE seq=1').fetchone()[0]
                l.conn.execute('UPDATE events SET payload=? WHERE seq=1',(raw+' ',))
                with self.assertRaises(AssertionError):
                    l.verify_chain()
                with self.assertRaises(Conflict):
                    l.source('seed')
            finally:l.close()
    def test_noncanonical_ordinary_payload_must_refuse_source_read(self):
        with tempfile.TemporaryDirectory() as d:
            l=ledger(Path(d)/'x.sqlite')
            try:
                raw=l.conn.execute("SELECT payload FROM events WHERE kind='OBJECTIVE_CUE'").fetchone()[0]
                l.conn.execute("UPDATE events SET payload=? WHERE kind='OBJECTIVE_CUE'",(raw+' ',))
                with self.assertRaises(AssertionError):
                    l.verify_chain()
                with self.assertRaises(Conflict):
                    l.source('seed')
            finally:l.close()
if __name__=='__main__': unittest.main()
