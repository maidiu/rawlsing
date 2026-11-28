"""Same-call exact ordered representations; no new psychic ownership.

Retain every field of the original developmental and selection packets.
Full grammar, hard raw cap and default transport remain unchanged.
Hermetic expansion is not a live-model fidelity claim.
"""
from collections import defaultdict
import json
import unittest
from unittest.mock import patch

from um_sorok_organism.types import canonical, copy, digest
from um_sorok_organism.live_psychological_llm import (
    ExplicitJSONLLMProvider, _compile_structured_fields,
    _expand_structured_fields, _expand_exact_aliases,
)
import test_inference_economy_exact_packet_r3 as r3
import test_inference_economy_counterhistory_r7 as r7


class StructuredPacketEconomyR13(unittest.TestCase):
    def test_exact_order_identity_and_no_unqualified_reconstruction(self):
        rows=[{"id":"f"+str(i),"meaning":"é"*100} for i in range(4)]
        packet={"actor_forms":{x["id"]:x for x in rows},
                "selected_constitution":{"recruited":[rows[3],rows[1],rows[3]],
                                         "inhibited":["f0"]}}
        before=canonical(packet)
        reduced,desc=_compile_structured_fields("development",packet)
        self.assertEqual(desc,{"selected_constitution.recruited":{
            "recruited_form_ids":["f3","f1","f3"]}})
        self.assertEqual(canonical(_expand_structured_fields("development",reduced,desc)),before)
        self.assertEqual(canonical(packet),before)
        changed=copy(packet);changed["selected_constitution"]["recruited"][0]["meaning"]="different"
        self.assertEqual(_compile_structured_fields("development",changed),(changed,{}))
        with self.assertRaises(ValueError):
            _expand_structured_fields("development",reduced,
                {"selected_constitution.recruited":{"recruited_form_ids":["foreign"]}})
        with self.assertRaises(ValueError):
            _expand_structured_fields("expression",reduced,desc)
        with self.assertRaises(ValueError):
            _expand_structured_fields("development",packet,desc)
        opts=[{"action":"REST","practical_alternatives":rows[:2],
               "possible_end_trials":rows[2:]},{"action":"WAIT","practical_alternatives":rows[2:]}]
        packet={"options":opts,"practical_options":rows,"possible_end_trials":rows[2:],
                "situated":{"candidate_actions":list(reversed(opts))}}
        reduced,desc=_compile_structured_fields("actor_attempt",packet)
        self.assertEqual(set(desc),{"practical_options","possible_end_trials"})
        self.assertEqual(_expand_structured_fields("actor_attempt",reduced,desc),packet)
        changed=copy(packet);changed["practical_options"].reverse()
        _,desc=_compile_structured_fields("actor_attempt",changed)
        self.assertNotIn("practical_options",desc)

    def _run(self,structured):
        stats=defaultdict(lambda:dict(calls=0,request_bytes=0,packet_bytes=0,structured=0))
        witnesses=[]
        original=r3.ExplicitJSONLLMProvider
        providers=[]
        def factory(**kw):
            callback=kw["transport"]
            def wire(req):
                body=json.loads(req["messages"][1]["content"])
                task=body["task"]
                fields=body.get("reconstructed_fields",{})
                p=_expand_exact_aliases(task,body["actor_source_packet"],
                                       body.get("same_call_exact_aliases",{}))
                p=_expand_structured_fields(task,p,fields)
                witnesses.append((task,digest(p)))
                if fields:
                    self.assertIn("Do not add other forms",req["messages"][0]["content"])
                    self.assertNotEqual(task,"expression")
                # The original hermetic callback accepts exact alias bodies.
                # Expand both transforms before giving it the original packet.
                clean=copy(req)
                clean["messages"][1]["content"]=canonical(
                    {"task":task,"actor_source_packet":p})
                return callback(clean)
            kw["transport"]=wire
            kw["compact_structured_packet"]=structured
            provider=original(**kw);providers.append(provider)
            return provider
        with patch.object(r3,"ExplicitJSONLLMProvider",factory), \
             patch.object(r7,"ExplicitJSONLLMProvider",factory):
            court=r3.ExactPacketEconomyR3()
            historical,_=court._r32(True)
            court._r51(True)
            court._r51(True,forge=True)
            c=r7.CounterhistoryEconomyR7()
            counter=[c._course(release,True)[:3] for release in (False,True)]
        for provider in providers:
            snap=provider.usage_snapshot()
            self.assertEqual(snap["evicted"],0)
            for m in snap["receipts"]:
                self.assertEqual(m["transport"],"MOCK")
                self.assertIsNone(m["usage"]["input_tokens"])
                d=stats[m["task"]]
                d["calls"]+=1;d["request_bytes"]+=m["request_bytes"]
                d["packet_bytes"]+=m["packet_bytes"]
                d["structured"]+=m["structured_field_count"]
        return historical,counter,witnesses,dict(stats)

    def test_actual_revaluation_vocal_genesis_and_counterhistory(self):
        old=self._run(False);new=self._run(True)
        self.assertEqual(old[:3],new[:3])
        for task in old[3]:
            self.assertEqual(old[3][task]["calls"],new[3][task]["calls"])
            self.assertEqual(old[3][task]["packet_bytes"],new[3][task]["packet_bytes"])
            self.assertLessEqual(new[3][task]["request_bytes"],old[3][task]["request_bytes"])
        self.assertGreater(new[3]["actor_attempt"]["structured"],0)
        self.assertGreater(new[3]["development"]["structured"],0)
        print("INFERENCE_ECONOMY_R13_STRUCTURED "+canonical({
            "prior_exact_aliases":old[3],"with_structured":new[3],
            "same_actual_and_packet_digests":True,"provider_tokens":None}))

    def test_raw_limit_and_default_retained(self):
        seen=[]
        p=ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
            model="fixture",api_key="not-a-key",allow_private_actor_data=True,
            transport=lambda req:seen.append(req) or r3.reply({"task":"actor_attempt","action":"WAIT"}),
            compact_structured_packet=True,metrics_capacity=4)
        with self.assertRaisesRegex(ValueError,"REMOTE_MODEL_SOURCE_PACKET_TOO_LARGE"):
            p.propose("actor_attempt",{"options":[{"practical_alternatives":["x"*65000]}],
                                      "practical_options":["x"*65000]})
        self.assertEqual(seen,[])
        p.propose("actor_attempt",{"options":[],"practical_options":[]})
        self.assertNotIn("reconstructed_fields",json.loads(seen[0]["messages"][1]["content"]))


if __name__=="__main__":unittest.main()
