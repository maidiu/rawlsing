"""PFF/PRE-A0/SC07: reuse one *identical* relational question, not a new psychology.

No constitutive ablation, source change, model call suppression, or persistent
cache. The comparator bypasses only the local closure memo, keeping the
same owner, algorithm, state and independently qualified offers.
"""
from dataclasses import asdict
from copy import deepcopy
from collections import Counter
from time import perf_counter_ns
from unittest.mock import patch
import unittest

from um_sorok_organism import constitution as owner
from um_sorok_organism import relational_metabolism as relations
from um_sorok_organism.semantics import ValidatingSemanticService
from um_sorok_organism.types import canonical, digest
import test_relational_metabolism_r4_integrated as prior
import test_inference_economy_exact_packet_r3 as courses


class RelationalClosureEconomyR6(unittest.TestCase):
    def _compare(self,fn):
        counts=Counter()
        elapsed=Counter()
        def timed(name,original):
            def call(*args,**kw):
                start=perf_counter_ns()
                counts[name]+=1
                try:return original(*args,**kw)
                finally:elapsed[name]+=perf_counter_ns()-start
            return call
        original=owner._same_composition_recruitment
        original_derive=owner.derive_relational_metabolism
        original_validate=relations.validate_motif
        out=[]
        for reuse in (False,True):
            counts.clear();elapsed.clear()
            with patch.object(owner,"_same_composition_recruitment",
                              original if reuse else lambda f:f), \
                 patch.object(owner,"derive_relational_metabolism",
                              timed("relation_projection",original_derive)), \
                 patch.object(relations,"validate_motif",
                              timed("motif_validation",original_validate)):
                result=fn()
            out.append((result,dict(counts),dict(elapsed)))
        self.assertEqual(out[0][0],out[1][0])
        self.assertLessEqual(out[1][1].get("relation_projection",0),
                             out[0][1].get("relation_projection",0))
        return {"before_calls":out[0][1],"after_calls":out[1][1],
                "before_ns":out[0][2],"after_ns":out[1][2],
                "exact_result_equal":True}

    @staticmethod
    def _chain(n):
        c=prior.constitution(motif_present=False)
        # Each link has a distinct historical form; recursive motif
        # recruitment genuinely propagates. No initial direct cue for the
        # additional forms and no developer personality score.
        previous="authority"
        for i in range(n):
            fid="acquired_%d"%i
            c.forms[fid]=prior.form(fid,"WAIT",["distinct_unreceived_%d"%i])
            c.relational_motifs.append({
                "id":"motif_%d"%i,"source_forms":["care",previous],
                "cue_terms":["rebuke"],"locations":["home"],
                "origin":["sourcefree_distinct_prior_%d"%i],"status":"ACTIVE",
                "effects":[{"kind":"RECRUIT_FORM","target_form":fid}]})
            previous=fid
        return c

    def test_recursive_recruitment_scaling_at_same_information(self):
        rows=[]
        for n in (4,16,48):
            c=self._chain(n);e=prior.access()
            baseline=canonical(asdict(c))
            def read():
                situated=owner.compose(c,e)
                self.assertEqual(canonical(asdict(c)),baseline)
                self.assertEqual(len(situated.recruited),n+2)
                self.assertEqual(sum(x["kind"]=="HISTORICALLY_RECRUITED_VIA_MOTIF"
                                     for x in situated.currents),n)
                return canonical(asdict(situated))
            result=self._compare(read)
            self.assertLess(result["after_calls"]["motif_validation"],
                            result["before_calls"]["motif_validation"])
            rows.append({"motifs":n,**result})
        print("INFERENCE_ECONOMY_R6_CHAIN "+canonical(rows))

    def test_distinct_vetoes_conflicts_and_new_context_remain_distinct(self):
        c=self._chain(5)
        # Different blocked sets must not share a result; even an inhibited
        # source can remain indirectly operative.
        for variant in ("acyclic","cyclic","bodily","foreign","revalued"):
            with self.subTest(variant=variant):
                x=deepcopy(c);e=prior.access()
                if variant in ("acyclic","cyclic"):
                    x.links.append({"source":"authority","target":"care",
                        "relation":"INHIBITS","origin":["past"],"contexts":["home"]})
                if variant=="cyclic":
                    x.links.append({"source":"care","target":"authority",
                        "relation":"INHIBITS","origin":["other_past"],"contexts":["home"]})
                if variant=="bodily":x.forms["care"]["body_min"]=2
                if variant=="foreign":e=prior.access(("unrelated",))
                if variant=="revalued":x.relational_motifs[0]["status"]="DORMANT"
                self._compare(lambda:canonical(asdict(owner.compose(x,e))))
        # No persistent caching of an earlier composition, even at equal clock.
        before=owner.compose(c,prior.access())
        c.relational_motifs[0]["status"]="DORMANT"
        after=owner.compose(c,prior.access())
        self.assertGreater(len(before.recruited),len(after.recruited))
        c.relational_motifs[0]["source_forms"]=["care","not_acquired"]
        for reuse in (False,True):
            original=owner._same_composition_recruitment
            with patch.object(owner,"_same_composition_recruitment",
                              original if reuse else lambda f:f):
                with self.assertRaises(relations.InvalidRelationalMotif):
                    owner.compose(c,prior.access())

    def test_actual_revaluation_positive_genesis_and_forgery(self):
        def actual():
            packet_digests=[]
            original=ValidatingSemanticService.proposal
            def observe(obj,task,packet):
                packet_digests.append((task,digest(packet)))
                return original(obj,task,packet)
            with patch.object(ValidatingSemanticService,"proposal",observe):
                court=courses.ExactPacketEconomyR3()
                result=(court._r32(True),court._r51(True),court._r51(True,forge=True))
            return result,packet_digests
        result=self._compare(actual)
        self.assertLess(result["after_calls"]["relation_projection"],
                        result["before_calls"]["relation_projection"])
        print("INFERENCE_ECONOMY_R6_ACTUAL "+canonical(result))


if __name__=="__main__":
    unittest.main()
