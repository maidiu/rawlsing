"""Measured bounded historical workloads, not a calibrated human-life model."""
import json
import tempfile
import time
import tracemalloc
import unittest
from pathlib import Path
from unittest.mock import patch
from collections import defaultdict
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import ValidatingSemanticService, HeuristicSemanticProvider
from um_sorok_organism.live_psychological_llm import ExplicitJSONLLMProvider
from um_sorok_organism import storage
from um_sorok_organism.types import canonical, digest
import test_productive_vocal_genesis_r51 as r51


def legacy_hashes(envelope, raw, prior, eid):
    # Exact original hashing preimages, not a parallel ledger implementation.
    return ('evt_'+digest({'prev':prior,'envelope':envelope})[:20],
            digest({'previous':prior,'eid':eid,'envelope':envelope}))


def measured(fn):
    tracemalloc.start()
    try:
        start=time.perf_counter_ns()
        result=fn()
        elapsed=time.perf_counter_ns()-start
        _,peak=tracemalloc.get_traced_memory()
        return result,elapsed,peak
    finally:
        tracemalloc.stop()


class HistoryEconomyR2(unittest.TestCase):
    def test_canonical_preimages_exact(self):
        for env in ({}, {'z':'é 👋 " \\ \\n','a':[True,None,1,1.2,-0.0]},
                    {'actor':None,'world':'w','clock':7,'nested':{'b':2,'a':1}},
                    {'payload':'x'*100000,'ref':'a'}):
            for prior,eid in [('GENESIS','evt_example'),('a"é','b\\c')]:
                raw=canonical(env)
                self.assertEqual(storage._canonical_event_hashes(env,raw,prior,eid),
                                 legacy_hashes(env,raw,prior,eid))

    def _course(self, age, history_steps):
        with tempfile.TemporaryDirectory() as tmp:
            db=str(Path(tmp)/'history.sqlite')
            observed=[]
            def transport(req):
                p=json.loads(req['messages'][1]['content'])
                task=p['task'];packet=p['actor_source_packet']
                if task=='adult_constructor':
                    ans=HeuristicSemanticProvider().propose(task,packet)
                elif task=='actor_attempt':
                    # This is an installed controlled policy choosing an offered
                    # operation, not a caller injecting the actor's action.
                    self.assertTrue(any(x['action']=='WAIT' for x in packet['options']))
                    ans={'task':task,'action':'WAIT'}
                elif task=='development':
                    ans={'task':task,'candidates':[]}
                    e=packet['experience']
                    if packet['actor']['id']=='nadia' and e.get('own_action')=='WAIT':
                        ans['candidates']=[{'kind':'MEMORY','cue_terms':['waiting'],
                                           'content':'I waited.','manifestation':'ordinary waiting'}]
                elif task=='expression':
                    ans={'task':task,'surface':'Life continues.'}
                else:raise AssertionError(task)
                observed.append((task,len(canonical(req).encode('utf-8')),
                     {k:len(canonical(v).encode('utf-8')) for k,v in packet.items()}))
                return {'choices':[{'message':{'content':canonical(ans)}}]}
            provider=ExplicitJSONLLMProvider(endpoint='https://example.invalid/chat/completions',
                     model='sourcefree-fixture',api_key='not-a-key',
                     allow_private_actor_data=True,transport=transport)
            service=ValidatingSemanticService(provider)
            rt=ConstitutiveRuntime(db,semantic=service)
            try:
                rt.initialize([('mother','Mother',r51.PARENT)])
                left=age
                while left:
                    days=min(3650,left);rt.background(days);left-=days
                for _ in range(history_steps):
                    result=rt.step('nadia')
                    self.assertEqual(result['attempt'],'WAIT')
                before=rt.snapshot('nadia')
                event_count=rt.verify()['events']
                self.assertGreaterEqual(len(before['memories']),history_steps)
                # Audit precisely the same persisted history in each arm.
                # Repeat to reduce single-timing noise; preserve the complete
                # original list + hash path in the comparator.
                original=storage.ResearchLedger._iter_events
                def list_reader(ledger,limit=None):
                    return iter(list(original(ledger,limit)))
                old=[];new=[]
                for arm in ('old','new','new','old'):
                    if arm=='old':
                        with patch.object(storage.ResearchLedger,'_iter_events',list_reader), patch.object(storage,'_canonical_event_hashes',legacy_hashes):
                            value,t,peak=measured(rt.verify)
                        old.append((t,peak))
                    else:
                        value,t,peak=measured(rt.verify)
                        new.append((t,peak))
                    self.assertEqual(value['events'],event_count)
                    self.assertTrue(value['valid'])
                    self.assertEqual(value,rt.verify())
                rt.close()
                rt=ConstitutiveRuntime(db,semantic=service)
                self.assertEqual(before,rt.snapshot('nadia'))
                self.assertEqual(rt.verify()['events'],event_count)
                observed.clear()
                result=rt.step('nadia')
                self.assertEqual(result['attempt'],'WAIT')
                self.assertTrue(rt.verify()['valid'])
                sizes=defaultdict(int);calls=defaultdict(int);fields=defaultdict(lambda:defaultdict(int))
                for task,n,kv in observed:
                    sizes[task]+=n;calls[task]+=1
                    for k,v in kv.items():fields[task][k]+=v
                return {'age_days':before['age_days'],'prior_beats':history_steps,
                    'prior_events':event_count,'memories':len(before['memories']),
                    'request_bytes':dict(sizes),'calls':dict(calls),
                    'largest_packet_fields':{t:sorted(v.items(),key=lambda x:-x[1])[:8] for t,v in fields.items()},
                    'legacy_verify_ns':[v[0] for v in old],'stream_verify_ns':[v[0] for v in new],
                    'legacy_peak_python_bytes':[v[1] for v in old],'stream_peak_python_bytes':[v[1] for v in new]}
            finally:rt.close()

    def test_matched_age_and_history_growth(self):
        rows=[self._course(age,steps) for age,steps in ((280,4),(280,24),(3650,4),(3650,24),(14600,4))]
        self.assertEqual(len({r['age_days'] for r in rows}),3)
        self.assertGreater(rows[1]['memories'],rows[0]['memories'])
        self.assertGreater(rows[3]['memories'],rows[2]['memories'])
        print('INFERENCE_ECONOMY_R2_MEASURED '+canonical({'rows':rows,
            'scope':'HERMETIC_ACTUAL_RUNTIME_CONTROLLED_WAIT_AND_MEMORY',
            'tokens':None,'timings_include_tracemalloc':True}))

    def test_historical_mutations_not_cached_or_laundered(self):
        with tempfile.TemporaryDirectory() as tmp:
            rt=ConstitutiveRuntime(str(Path(tmp)/'test.sqlite'))
            try:
                rt.initialize()
                rt.background(30)
                rt.background(30)
                clean=rt.verify()
                c=rt.ledger.conn
                rows=rt.ledger.events()
                original=rows[1]['envelope_bytes']
                eid=rows[1]['id']
                c.execute('UPDATE events SET payload=? WHERE eid=?',(original+' ',eid))
                with self.assertRaisesRegex(AssertionError,'EVENT_ENVELOPE_NONCANONICAL_BYTES'):
                    rt.verify()
                with self.assertRaises(storage.Conflict):
                    rt.background(1)
                c.execute('UPDATE events SET payload=? WHERE eid=?',(original,eid))
                self.assertEqual(rt.verify(),clean)
                c.execute('UPDATE events SET clock=clock+1 WHERE eid=?',(eid,))
                with self.assertRaisesRegex(AssertionError,'EVENT_HEADER_ENVELOPE_MISMATCH'):
                    rt.verify()
                c.execute('UPDATE events SET clock=clock-1 WHERE eid=?',(eid,))
                self.assertEqual(rt.verify(),clean)
                self.assertEqual(rt.ledger.events(1),rows[:1])
                self.assertEqual(rt.ledger.events(0),[])
            finally:rt.close()


if __name__=='__main__':
    unittest.main()
