"""PFF §11 / PRE-A0 §§16–18 transport court, not constitutive compression.

Same causal states and histories, exact same model-visible information in
a different wire representation. Hermetic expansion proves the contract,
not that a remote LLM will reliably interpret aliases.
"""
import json
import tempfile
import unittest
from pathlib import Path
from collections import defaultdict
from unittest.mock import patch
from um_sorok_organism.types import canonical, copy
from um_sorok_organism.live_psychological_llm import (
    ExplicitJSONLLMProvider, _compile_exact_aliases, _expand_exact_aliases,
)
from um_sorok_organism.runtime import ConstitutiveRuntime
import test_tco_r23_relational_transduction as r32
import test_productive_vocal_genesis_r51 as r51


def reply(value):
    return {"choices":[{"message":{"content":canonical(value)}}]}


class ExactPacketEconomyR3(unittest.TestCase):
    def test_only_exact_same_phase_aliases_and_nonmutation(self):
        rows=[{"id":"event:"+str(i),"witness":"é"*20} for i in range(24)]
        packet={"selected_constitution":{"currents":rows,"readset":["x"]},
                "historical_psychodynamic_context":{
                    "before_objective_transition":{"currents":copy(rows)},
                    "after_world_before_formation":{"currents":copy(rows),
                                                      "readset":["different"]}},
                "experience":{"retained_actor_content":"actor local"}}
        original=canonical(packet)
        reduced,aliases=_compile_exact_aliases("development",packet)
        self.assertEqual(aliases,{
            "historical_psychodynamic_context.after_world_before_formation.currents":
                "selected_constitution.currents"})
        self.assertEqual(reduced["historical_psychodynamic_context"]
                         ["before_objective_transition"]["currents"],rows)
        self.assertEqual(reduced["historical_psychodynamic_context"]
                         ["after_world_before_formation"]["readset"],["different"])
        self.assertEqual(canonical(_expand_exact_aliases("development",reduced,aliases)),original)
        self.assertEqual(canonical(packet),original)
        with self.assertRaises(ValueError):
            _expand_exact_aliases("expression",reduced,aliases)
        with self.assertRaises(ValueError):
            _expand_exact_aliases("development",packet,aliases)
        for task in ("expression","adult_constructor","blind_adult_interview",
                     "family_pathway_selection"):
            self.assertEqual(_compile_exact_aliases(task,packet),(packet,{}))
        # Distinct cooperative option rosters are not silently unified.
        actor={"options":rows[:-1],"situated":{"candidate_actions":rows},
               "accessible":{"cues":rows}}
        self.assertEqual(_compile_exact_aliases("actor_attempt",actor),(actor,{}))

    def _provider(self,callback,compact,providers):
        def send(req):
            body=json.loads(req["messages"][1]["content"])
            task=body["task"]
            packet=body["actor_source_packet"]
            aliases=body.get("same_call_exact_aliases",{})
            if aliases:
                self.assertIn("preserve its original scope and time",
                              req["messages"][0]["content"])
                self.assertNotEqual(task,"expression")
                packet=_expand_exact_aliases(task,packet,aliases)
            return reply(callback(task,packet))
        p=ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
            model="sourcefree-fixture",api_key="not-a-key",
            allow_private_actor_data=True,transport=send,
            compact_exact_packet=compact,metrics_capacity=100000)
        providers.append(p)
        return p

    def _stats(self,providers):
        totals=defaultdict(lambda:dict(calls=0,aliases=0,raw_packet=0,
                                      wire_packet=0,request=0))
        for p in providers:
            snap=p.usage_snapshot()
            self.assertEqual(snap["evicted"],0)
            for row in snap["receipts"]:
                self.assertEqual(row["transport"],"MOCK")
                self.assertIsNone(row["usage"]["input_tokens"])
                self.assertEqual(row["outcome"],"PROPOSAL_RETURNED")
                s=totals[row["task"]]
                s["calls"]+=1;s["aliases"]+=row["alias_count"]
                s["raw_packet"]+=row["packet_bytes"]
                s["wire_packet"]+=row["wire_packet_bytes"]
                s["request"]+=row["request_bytes"]
        return dict(totals)

    def _r32(self,compact):
        providers=[];results={}
        with tempfile.TemporaryDirectory() as d:
            with patch.object(r32,"CallbackLLMProvider",
                              side_effect=lambda cb:self._provider(cb,compact,providers)):
                for decision in ("revalue","abstain"):
                    db=str(Path(d)/(decision+".sqlite"))
                    service,source,old,state,situated,offers,chosen=(
                        r32.CrossContextMetabolismR32._run_history(db,decision))
                    rt=ConstitutiveRuntime(db,semantic=service)
                    try:
                        actual=rt.step("mother")
                        results[decision]={"actual":actual,"state":rt.snapshot("mother"),
                            "world":rt.ledger.world()[1],"history":rt.verify(),
                            "before":state,"situated":situated,"offers":offers,"chosen":chosen}
                    finally:rt.close()
        self.assertEqual({k:v["actual"]["attempt"] for k,v in results.items()},
                         {"revalue":"REST","abstain":"WAIT"})
        return results,self._stats(providers)

    def _r51(self,compact,forge=False):
        providers=[]
        with patch.object(r51,"CallbackLLMProvider",
                          side_effect=lambda cb:self._provider(cb,compact,providers)):
            r51.ProductiveVocalR51().run_course(forge=forge)
        return self._stats(providers)

    def test_actual_revaluation_and_positive_genesis_wire_economy(self):
        full,s0=self._r32(False)
        compact,s1=self._r32(True)
        # Compare entire actual state, world and verified ledger hash,
        # not merely matching selected operations or prose.
        self.assertEqual(full,compact)
        p0=self._r51(False);p1=self._r51(True)
        for a,b in ((s0,s1),(p0,p1)):
            self.assertEqual({k:(v["calls"],v["raw_packet"]) for k,v in a.items()},
                             {k:(v["calls"],v["raw_packet"]) for k,v in b.items()})
            self.assertGreater(sum(v["aliases"] for v in b.values()),0)
            self.assertLess(sum(v["request"] for v in b.values()),
                            sum(v["request"] for v in a.values()))
            self.assertEqual(a["expression"],b["expression"])
        print("INFERENCE_ECONOMY_R3_MEASURED "+canonical({
            "r32":{"full":s0,"compiled":s1,"actual":{"revalue":"REST","abstain":"WAIT"},
                   "matched_entire_state_and_chain":True},
            "r51":{"full":p0,"compiled":p1},
            "scope":"HERMETIC_SAME_INFORMATION_WIRE_PROJECTION",
            "provider_tokens":None}))

    def test_actual_forged_source_rejected_after_compilation(self):
        self._r51(True,forge=True)

    def test_short_packet_and_cap_preserved(self):
        seen=[]
        p=ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
            model="sourcefree-fixture",api_key="not-a-key",
            allow_private_actor_data=True,transport=lambda req:(
                seen.append(req) or reply({"task":"actor_attempt","action":"WAIT"})),
            compact_exact_packet=True,metrics_capacity=8)
        p.propose("actor_attempt",{"options":[],"situated":{"candidate_actions":[]}})
        self.assertNotIn("same_call_exact_aliases",json.loads(seen[0]["messages"][1]["content"]))
        self.assertEqual(p.usage_snapshot()["receipts"][0]["packet_variant"],"FULL")
        with self.assertRaisesRegex(ValueError,"REMOTE_MODEL_SOURCE_PACKET_TOO_LARGE"):
            p.propose("actor_attempt",{"options":["x"*65000],
                "situated":{"candidate_actions":["x"*65000]}})
        self.assertEqual(len(seen),1)


if __name__=="__main__":
    unittest.main()
