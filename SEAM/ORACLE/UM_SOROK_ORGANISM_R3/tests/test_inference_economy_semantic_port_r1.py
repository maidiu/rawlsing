"""Owner-local economic experiment; hermetic transport, not live LLM fidelity."""
import json
import unittest
from unittest.mock import patch
from collections import Counter, defaultdict
from um_sorok_organism.live_psychological_llm import ExplicitJSONLLMProvider
from um_sorok_organism.types import canonical
import test_productive_vocal_genesis_r51 as r51


def provider(transport, *, compact=False, capacity=128):
    return ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
        model="sourcefree-fixture", api_key="fake-key-not-a-credential",
        allow_private_actor_data=True, transport=transport,
        compact_task_prompt=compact, metrics_capacity=capacity)


def reply(data, usage=None):
    return {"choices":[{"message":{"content":canonical(data)}}], "usage":usage}


class InferenceEconomyPort(unittest.TestCase):
    def test_id_only_grammar_and_failure_receipts(self):
        for choice in ({"practical_option_id":"issued"}, {"possible_end_trial_id":"trial"},
                       {"action":"WAIT"}, {"action":"WAIT","practical_option_id":"issued"}):
            p=provider(lambda req:reply({"task":"actor_attempt",**choice}))
            self.assertEqual(p.propose("actor_attempt",{}),{"task":"actor_attempt",**choice})
            self.assertEqual(p.usage_snapshot()["receipts"][0]["outcome"],"PROPOSAL_RETURNED")
        for choice in ({}, {"practical_option_id":123}, {"action":None,"possible_end_trial_id":"trial"}):
            p=provider(lambda req:reply({"task":"actor_attempt",**choice}))
            with self.assertRaisesRegex(ValueError,"REMOTE_MODEL_BAD_ACTION"):
                p.propose("actor_attempt",{})
            self.assertEqual(p.usage_snapshot()["receipts"][0]["outcome"],"REJECTED_OR_FAILED")
        p=provider(lambda req: self.fail("oversized packet must not send"))
        with self.assertRaisesRegex(ValueError,"REMOTE_MODEL_SOURCE_PACKET_TOO_LARGE"):
            p.propose("expression",{"secret":"x"*128001})
        self.assertEqual(p.usage_snapshot()["receipts"][0]["attempts"],0)

    def test_usage_report_and_bounded_redacted_receipt(self):
        data={"task":"expression","surface":"private output marker"}
        usage={"prompt_tokens":100,"completion_tokens":20,"total_tokens":120,
            "prompt_tokens_details":{"cached_tokens":50},
            "completion_tokens_details":{"reasoning_tokens":7}}
        seen=[]
        def transport(req):
            seen.append(len(canonical(req).encode("utf-8")))
            return reply(data,usage)
        p=provider(transport,capacity=1)
        for _ in range(2):
            self.assertEqual(p.propose("expression",{"private":"secret history marker"}),data)
        snap=p.usage_snapshot()
        self.assertEqual((snap["total"],snap["evicted"],len(snap["receipts"])),(2,1,1))
        row=snap["receipts"][0]
        self.assertEqual(row["request_bytes"],seen[-1])
        self.assertEqual(row["usage"],{"input_tokens":100,"output_tokens":20,
            "total_tokens":120,"cached_input_tokens":50,"cache_write_tokens":None,"reasoning_tokens":7})
        for secret in ("secret history marker","private output marker","fake-key-not-a-credential"):
            self.assertNotIn(secret,canonical(snap))
        snap["receipts"].clear()
        self.assertEqual(len(p.usage_snapshot()["receipts"]),1)

    def test_task_projection_conserves_common_and_own_rules(self):
        starts={"expression":"For expression disclose only actor-accessible",
                "adult_constructor":"For adult_constructor all history",
                "family_pathway_selection":"For family_pathway_selection choose",
                "blind_adult_interview":"For blind_adult_interview no cached"}
        for task in starts:
            prompts=[]
            def send(req):
                prompts.append(req["messages"][0]["content"])
                return reply({"task":task})
            for compact in (False,True):
                p=provider(send,compact=compact)
                p.propose(task,{"one":"same"})
            full,short=prompts
            self.assertLess(len(short),len(full))
            self.assertIn(starts[task],short)
            self.assertIn("Never invent world events",short)
            self.assertIn("Return valid JSON and no Markdown.",short)
            self.assertNotIn("For development emit candidates",short)
        for task in ("actor_attempt","development"):
            prompts=[]
            def send(req):
                prompts.append(req["messages"][0]["content"])
                return reply({"task":task,"action":"WAIT","candidates":[]})
            for compact in (False,True):
                provider(send,compact=compact).propose(task,{})
            self.assertEqual(prompts[0],prompts[1])

    def _actual_course(self, *, compact, forge=False):
        providers=[]
        selections=Counter()
        def factory(callback):
            def send(req):
                body=json.loads(req["messages"][1]["content"])
                task=body["task"]
                ans=callback(task,body["actor_source_packet"])
                if task=="actor_attempt":
                    for k in ("possible_end_trial_id","practical_option_id"):
                        if k in ans and "action" not in ans:selections[k]+=1
                return reply(ans)
            p=provider(send,compact=compact,capacity=100000)
            providers.append(p)
            return p
        # Exercise existing R51 actual runtime, including its cold SQLite
        # reopen, causal assertions and independently selected trial/project.
        with patch.object(r51,"CallbackLLMProvider",side_effect=factory):
            r51.ProductiveVocalR51().run_course(forge=forge)
        self.assertEqual(len(providers),1)
        snap=providers[0].usage_snapshot()
        self.assertEqual(snap["evicted"],0)
        stats=defaultdict(lambda:dict(calls=0,instruction_bytes=0,packet_bytes=0,
                                       request_bytes=0,response_content_bytes=0))
        for row in snap["receipts"]:
            self.assertEqual(row["transport"],"MOCK")
            self.assertIsNone(row["usage"]["input_tokens"])
            self.assertEqual(row["outcome"],"PROPOSAL_RETURNED")
            self.assertEqual(row["attempts"],1)
            s=stats[row["task"]]
            s["calls"]+=1
            for key in ("instruction_bytes","packet_bytes","request_bytes","response_content_bytes"):
                s[key]+=row[key]
        if not forge:
            self.assertGreater(selections["possible_end_trial_id"],0)
            self.assertGreater(selections["practical_option_id"],0)
        return dict(stats),dict(selections)

    def test_actual_r51_full_vs_task_prompt(self):
        full,s1=self._actual_course(compact=False)
        short,s2=self._actual_course(compact=True)
        self.assertEqual(s1,s2)
        self.assertEqual({k:v["calls"] for k,v in full.items()},
                         {k:v["calls"] for k,v in short.items()})
        self.assertLess(sum(x["instruction_bytes"] for x in short.values()),
                        sum(x["instruction_bytes"] for x in full.values()))
        print("INFERENCE_ECONOMY_R1_MEASURED "+canonical({"full":full,"task_only":short,
                 "id_only_selections":s1,"provider_tokens":None,"scope":"R51_HERMETIC_CALLBACK"}))

    def test_actual_r51_forged_source_still_rejected(self):
        self._actual_course(compact=True,forge=True)


if __name__=="__main__":
    unittest.main()
