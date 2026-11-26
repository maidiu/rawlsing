"""Actual joined R31/R29 transport court. No simulated provider tokens.

R31's acquired technique is not itself a cache. Its epistemic distinction
is measured separately from reversible transport savings at fixed arm.
"""
from collections import defaultdict
import json
import unittest
from unittest.mock import patch

import test_neighbor_constitutive_compression_r31 as r31
import test_neighbor_correspondence_r29 as r29
from um_sorok_organism.live_psychological_llm import (
    ExplicitJSONLLMProvider, _expand_exact_aliases,
)
from um_sorok_organism.types import canonical, digest

MARKER="That afternoon I learned the precise way to mend the blue bowl."


class InferenceEconomyR5(unittest.TestCase):
    def _provider(self,callback,compact,witness,stage):
        def send(req):
            body=json.loads(req["messages"][1]["content"])
            task=body["task"]
            p=_expand_exact_aliases(task,body["actor_source_packet"],
                                     body.get("same_call_exact_aliases",{}))
            witness.append({"task":task,"stage":stage(),"digest":digest(p),
                "marker":MARKER in canonical(p),
                "rehearsal_bytes":len(canonical(p.get("private_rehearsal_options",[])).encode("utf-8"))})
            return {"choices":[{"message":{"content":canonical(callback(task,p))}}]}
        return ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
            model="sourcefree-fixture",api_key="not-a-key",allow_private_actor_data=True,
            transport=send,compact_exact_packet=compact,metrics_capacity=1000)

    def _r31(self,compact):
        witnesses=defaultdict(list);providers={}
        class Probe(r31.ConstitutiveCompressionR31):
            def build(self,name):
                self.arm=name
                self.ordinal=0
                return super().build(name)
            def repair(self,*args,**kwargs):
                self.ordinal+=1
                return super().repair(*args,**kwargs)
        probe=Probe("test_acquired_facility_persists_when_original_episode_is_inaccessible")
        def factory(callback):
            arm=probe.arm
            self.assertNotIn(arm,providers)
            p=self._provider(callback,compact,witnesses[arm],lambda:probe.ordinal)
            providers[arm]=p
            return p
        try:
            with patch.object(r31,"CallbackLLMProvider",side_effect=factory):
                probe.test_acquired_facility_persists_when_original_episode_is_inaccessible()
        finally:
            probe.doCleanups()
        stats={}
        for arm,p in providers.items():
            rows=p.usage_snapshot()["receipts"]
            w=witnesses[arm]
            self.assertEqual(len(rows),len(w))
            self.assertEqual(p.usage_snapshot()["evicted"],0)
            cold=[(m,x) for m,x in zip(rows,w) if x["stage"]==4 and x["task"]=="actor_attempt"]
            self.assertEqual(len(cold),2)
            by_task=defaultdict(lambda:dict(calls=0,request_bytes=0,source_packet_bytes=0))
            for m,x in zip(rows,w):
                self.assertEqual(m["task"],x["task"])
                self.assertEqual(m["transport"],"MOCK")
                self.assertIsNone(m["usage"]["input_tokens"])
                d=by_task[m["task"]]
                d["calls"]+=1
                d["request_bytes"]+=m["request_bytes"]
                d["source_packet_bytes"]+=m["packet_bytes"]
            stats[arm]={"by_task":dict(by_task),
                "cold_actor_selection_calls":len(cold),
                "cold_selections_with_origin_text":sum(x["marker"] for m,x in cold),
                "cold_selection_request_bytes":sum(m["request_bytes"] for m,x in cold),
                "cold_rehearsal_option_bytes":sum(x["rehearsal_bytes"] for m,x in cold)}
        self.assertEqual(stats["compressionTrue"]["cold_selections_with_origin_text"],0)
        self.assertGreater(stats["compressionFalse"]["cold_selections_with_origin_text"],0)
        return dict(witnesses),stats

    def test_r31_same_acquired_capacity_and_epistemic_boundary_under_compilation(self):
        w0,s0=self._r31(False)
        w1,s1=self._r31(True)
        self.assertEqual(w0,w1)
        for arm in s0:
            self.assertLess(sum(v["request_bytes"] for v in s1[arm]["by_task"].values()),
                            sum(v["request_bytes"] for v in s0[arm]["by_task"].values()))
            self.assertEqual({k:v["source_packet_bytes"] for k,v in s0[arm]["by_task"].items()},
                             {k:v["source_packet_bytes"] for k,v in s1[arm]["by_task"].items()})
        print("INFERENCE_ECONOMY_R5_MEASURED "+canonical({
            "full":s0,"compiled":s1,"within_arm_packets_equal":True,
            "fourth_repair_condition_both_arms":.9,"provider_tokens":None,
            "scope":"HERMITIC_R31_ACTUAL_OWNER_COURSE"}))

    def test_r29_and_r31_forgery_and_correspondence_access_remain(self):
        witness=[]
        def factory(cb):
            return self._provider(cb,True,witness,lambda:0)
        for module,cls,names in (
            (r29,r29.CorrespondenceR29,
             ("test_delivery_opening_and_optional_private_afterlife","test_revocation_and_no_unissued_open")),
            (r31,r31.ConstitutiveCompressionR31,("test_unissued_access_decrease_rolls_back",))):
            for name in names:
                case=cls(name)
                try:
                    with patch.object(module,"CallbackLLMProvider",side_effect=factory):
                        getattr(case,name)()
                finally:
                    case.doCleanups()
        self.assertTrue(witness)


if __name__=="__main__":
    unittest.main()
