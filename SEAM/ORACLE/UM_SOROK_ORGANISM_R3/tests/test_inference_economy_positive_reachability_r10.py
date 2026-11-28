"""Exact positive-link reachability; no change of relational psychology."""
from dataclasses import asdict
from collections import Counter
from random import Random
from time import perf_counter_ns
from unittest.mock import patch
import unittest

from um_sorok_organism import constitution as owner
from um_sorok_organism.types import canonical, digest
from um_sorok_organism.semantics import ValidatingSemanticService
import test_relational_metabolism_r4_integrated as prior
import test_inference_economy_exact_packet_r3 as courses


def scan_reference(positive,qualified):
    # The actual pre-R10 owner algorithm, retained only as a comparator.
    def closure(start,blocked=frozenset()):
        reached=(set(start)&qualified)-set(blocked)
        while True:
            added={link['target'] for link in positive
                   if link['source'] in reached
                   and link['target'] in qualified
                   and link['target'] not in blocked}
            newer=reached|added
            if newer==reached:return reached
            reached=newer
    return closure


class PositiveReachabilityR10(unittest.TestCase):
    def test_exact_sets_for_sparse_dense_cyclic_and_blocked_graphs(self):
        rng=Random(1778)
        for n in (0,1,4,16,48):
            nodes=[str(i) for i in range(n)]
            for probability in (.05,.25,.75):
                for _ in range(10):
                    edges=[{'source':s,'target':t} for s in nodes for t in nodes
                           if rng.random()<probability]
                    # Duplicate edges and unknown/unqualified endpoints.
                    edges+=edges[:2]+[{'source':'foreign','target':'0'},
                                      {'source':'0','target':'foreign'}]
                    qualified={x for x in nodes if rng.random()<.85}
                    start={x for x in nodes+['foreign'] if rng.random()<.25}
                    blocked={x for x in nodes if rng.random()<.2}
                    self.assertEqual(owner._positive_reachability(edges,qualified)(start,blocked),
                                     scan_reference(edges,qualified)(start,blocked))

    def _compare(self,fn):
        original=owner._positive_reachability
        results=[]
        for factory in (scan_reference,original):
            counts=Counter()
            class Counted:
                def __init__(self,items):self.items=items
                def __iter__(self):
                    for x in self.items:
                        counts['input_edge_reads']+=1
                        yield x
            def instrument(positive,qualified):
                counts['indexes_or_readers']+=1
                reader=factory(Counted(positive),qualified)
                def read(*a,**kw):
                    counts['closure_queries']+=1
                    return reader(*a,**kw)
                return read
            start=perf_counter_ns()
            with patch.object(owner,'_positive_reachability',instrument):
                out=fn()
            results.append((out,dict(counts),perf_counter_ns()-start))
        self.assertEqual(results[0][0],results[1][0])
        return {'scan':results[0][1],'indexed':results[1][1],
                'scan_ns':results[0][2],'indexed_ns':results[1][2],
                'exact_results_equal':True}

    def test_long_acquired_link_chains_keep_all_recruited_forms(self):
        rows=[]
        for n in (4,16,48,128):
            c=prior.constitution(motif_present=False)
            previous='authority'
            for i in range(n):
                fid='acquired_%d'%i
                c.forms[fid]=prior.form(fid,'WAIT',['unreceived_%d'%i])
                c.links.append({'source':previous,'target':fid,'relation':'RECRUITS',
                                'origin':['sourcefree:prior:%d'%i],'contexts':['home']})
                previous=fid
            # Reversed edge order and one cycle; no assumed linear psyche.
            c.links.reverse()
            c.links.append({'source':previous,'target':'authority','relation':'SUPPORTS',
                            'origin':['sourcefree:cycle'],'contexts':['home']})
            e=prior.access()
            def read():
                x=owner.compose(c,e)
                self.assertEqual(len(x.recruited),n+2)
                return canonical(asdict(x))
            result=self._compare(read)
            self.assertLess(result['indexed']['input_edge_reads'],
                            result['scan']['input_edge_reads'])
            rows.append({'links':n+1,**result})
        print('INFERENCE_ECONOMY_R10_CHAINS '+canonical(rows))

    def test_actual_history_and_distinct_vetoes(self):
        def actual():
            observed=[]
            original=ValidatingSemanticService.proposal
            def see(obj,task,packet):
                observed.append((task,digest(packet)))
                return original(obj,task,packet)
            with patch.object(ValidatingSemanticService,'proposal',see):
                c=courses.ExactPacketEconomyR3()
                result=(c._r32(True),c._r51(True),c._r51(True,forge=True))
            # Include independent veto and indirect inhibited relation cases.
            variants=[canonical(asdict(owner.compose(prior.constitution(
                    suppress=s,withhold=w),prior.access())))
                      for s in (False,True) for w in (False,True)]
            return result,observed,variants
        result=self._compare(actual)
        self.assertLessEqual(result['indexed'].get('input_edge_reads',0),
                             result['scan'].get('input_edge_reads',0))
        print('INFERENCE_ECONOMY_R10_ACTUAL '+canonical(result))


if __name__=='__main__':
    unittest.main()
