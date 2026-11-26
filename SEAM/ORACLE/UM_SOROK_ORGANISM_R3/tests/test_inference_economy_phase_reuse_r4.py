"""Same-phase principal composition reuse: exact behavior, no new cache owner.

Compare old recomputation to one local projection, through existing R32 and
R51 runtime courses, including cold continuations and hostile formation.
Times are aggregate runtime helper wall time in the hermetic court only.
"""
from collections import Counter
from time import perf_counter_ns
from unittest.mock import patch
import unittest

from um_sorok_organism import runtime
from um_sorok_organism.types import canonical, digest
from um_sorok_organism.semantics import ValidatingSemanticService
import test_inference_economy_exact_packet_r3 as r3


class PhaseReuseR4(unittest.TestCase):
    def _course(self, reuse, *, forge=False):
        counts=Counter()
        times=Counter()
        packets=[]
        plans=Counter()
        original_plan=runtime.ConstitutiveRuntime._actor_plan
        original_proposal=ValidatingSemanticService.proposal
        original_step=runtime.ConstitutiveRuntime.step
        def counted(name,fn):
            def call(*args,**kw):
                start=perf_counter_ns()
                counts[name]+=1
                try:
                    return fn(*args,**kw)
                finally:
                    times[name]+=perf_counter_ns()-start
            return call
        def step(obj,*args,**kw):
            counts["step"]+=1
            return original_step(obj,*args,**kw)
        def plan(obj,*args,**kw):
            projection=kw.get("_principal_projection")
            if projection is not None:
                plans["same_phase_principal"]+=1
                # This internal path is only used for the focal actor,
                # never the independent coactor (positional args 5/6).
                self.assertLessEqual(len(args),4)
                if not reuse:
                    kw.pop("_principal_projection")
            else:
                plans["fresh"]+=1
            return original_plan(obj,*args,**kw)
        def proposal(obj,task,packet):
            # Ephemeral equality witness only; no private payload in output.
            packets.append((task,digest(packet)))
            return original_proposal(obj,task,packet)
        with patch.object(runtime,"compose",counted("compose",runtime.compose)), \
             patch.object(runtime,"materialize",counted("materialize",runtime.materialize)), \
             patch.object(runtime,"actor_access",counted("actor_access",runtime.actor_access)), \
             patch.object(runtime.ConstitutiveRuntime,"_actor_plan",plan), \
             patch.object(runtime.ConstitutiveRuntime,"step",step), \
             patch.object(ValidatingSemanticService,"proposal",proposal):
            court=r3.ExactPacketEconomyR3()
            if forge:
                result=court._r51(True,forge=True)
            else:
                result=(court._r32(True),court._r51(True))
        self.assertEqual(counts["step"],plans["same_phase_principal"])
        self.assertGreater(plans["fresh"],0)
        return result,packets,dict(counts),dict(times),dict(plans)

    def _compare(self,forge=False):
        old=self._course(False,forge=forge)
        new=self._course(True,forge=forge)
        self.assertEqual(old[0],new[0])
        self.assertEqual(old[1],new[1])
        self.assertEqual(old[4],new[4])
        self.assertEqual(old[2]["step"],new[2]["step"])
        for name in ("compose","materialize","actor_access"):
            self.assertEqual(old[2][name]-new[2][name],old[2]["step"])
        return {"old_calls":old[2],"new_calls":new[2],
                "old_helper_ns":old[3],"new_helper_ns":new[3],
                "plan_paths":new[4],"semantic_calls":len(new[1]),
                "semantic_packet_digests_equal":True,"causal_results_equal":True}

    def test_phase_local_reuse_actual_history_and_positive_genesis(self):
        print("INFERENCE_ECONOMY_R4_MEASURED "+canonical(self._compare()))

    def test_phase_local_reuse_keeps_forgery_rejection(self):
        self._compare(forge=True)


if __name__=="__main__":
    unittest.main()
