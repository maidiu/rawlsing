"""Preregistered lab campaign: actual sourcefree workload and hermetic wire court."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from inference_lab_cli import capture_course
from um_sorok_organism.inference_lab_campaign import (
    build_plan, verify_plan, execute_plan, select_cases)
from um_sorok_organism.inference_lab import WorkloadCapture
from um_sorok_organism.live_psychological_llm import (
    ExplicitJSONLLMProvider, _expand_exact_aliases, _expand_structured_fields)
from um_sorok_organism.semantics import CallbackLLMProvider
from um_sorok_organism.types import canonical, copy, digest

HEAD="a"*40
def config():
    return {"arms":[
        {"name":"F","endpoint":"https://example.invalid/chat/completions",
         "model":"fixture-a","key_env":"LAB_FIXTURE_KEY","compiled":False,
         "input_nanos_per_token":1000,"output_nanos_per_token":2000},
        {"name":"E","endpoint":"https://example.invalid/chat/completions",
         "model":"fixture-b","key_env":"LAB_FIXTURE_KEY","compiled":True,
         "input_nanos_per_token":500,"output_nanos_per_token":1000}],
        "budget":{"max_calls":40,"max_wire_bytes":10000000,
          "input_token_ceiling":100000,"completion_token_limit":500,
          "input_nanos_per_token":1000,"output_nanos_per_token":2000,
          "max_budget_nanos":4040000000}}


class InferenceCampaignR19(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc,cls.actual=capture_course(True,HEAD)

    def test_actual_stratified_preflight_and_matched_wire(self):
        cfg=config();plan=build_plan(self.doc,cfg,per_stratum=2)
        p=verify_plan(self.doc,cfg,plan)
        self.assertEqual(p["status"],"FITS_DECLARED_LIMITS")
        self.assertEqual(p["network_calls"],0)
        self.assertEqual(p["planned_calls"],20)
        self.assertEqual(len(p["cases"]),10)
        self.assertIn("development/named_offer_present",p["coverage"])
        self.assertIn("development/no_named_offer",p["coverage"])
        for name,c in p["coverage"].items():
            seq=[x["seq"] for x in p["cases"] if x["stratum"]==name]
            self.assertEqual(seq,[c["first_seq"],c["last_seq"]])
        self.assertEqual(p["planned_wire_bytes"],sum(x["request_bytes"] for x in p["schedule"]))
        self.assertEqual(p["declared_reserve_nanos"],2020000000)
        self.assertEqual([x["arm"] for x in p["schedule"][:4]],["F","E","E","F"])
        self.assertLess(p["arms"]["E"]["request_bytes"],p["arms"]["F"]["request_bytes"])
        self.assertNotIn("not-a-key",canonical(plan))
        rows=self.doc["payload"]["rows"];seen=[]
        def fake(provider,req):
            i=len(seen);expected=p["schedule"][i]
            self.assertEqual(digest(req),expected["request_sha256"])
            self.assertEqual(req["max_completion_tokens"],500)
            self.assertEqual(req["model"],"fixture-a" if expected["arm"]=="F" else "fixture-b")
            body=json.loads(req["messages"][1]["content"])
            packet=_expand_exact_aliases(body["task"],body["actor_source_packet"],
                                         body.get("same_call_exact_aliases",{}))
            packet=_expand_structured_fields(body["task"],packet,body.get("reconstructed_fields",{}))
            row=rows[expected["seq"]]
            self.assertEqual(digest(packet),row["packet_digest"])
            answer=copy(row["proposal"]);answer.setdefault("task",row["task"])
            seen.append(expected)
            return {"choices":[{"message":{"content":canonical(answer)}}],
                    "usage":{"prompt_tokens":100,"completion_tokens":20,"total_tokens":120}}
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            with patch.dict(os.environ,{"LAB_FIXTURE_KEY":"SECRET_TEST_SENTINEL"}), \
                 patch.object(ExplicitJSONLLMProvider,"_request",fake):
                result=execute_plan(self.doc,cfg,plan,journal=path/"budget.json",
                  observation_log=path/"observations.jsonl",sourcefree_live_authorized=True)
            self.assertEqual(result["status"],"COMPLETED")
            self.assertEqual(len(seen),20)
            self.assertEqual(result["budget"]["attempts"],20)
            self.assertEqual(result["budget"]["reserved_nanos"],p["declared_reserve_nanos"])
            self.assertEqual(result["budget"]["wire_bytes"],p["planned_wire_bytes"])
            self.assertEqual(result["declared_model_rate_estimates"]["F"]["known_usage_nanos"],1400000)
            self.assertEqual(result["declared_model_rate_estimates"]["E"]["known_usage_nanos"],700000)
            saved=[json.loads(x) for x in (path/"observations.jsonl").read_text().splitlines()]
            self.assertEqual(saved,result["observations"])
            self.assertEqual((path/"observations.jsonl").stat().st_mode&0o777,0o600)
            self.assertNotIn("SECRET_TEST_SENTINEL",canonical(result))
            self.assertNotIn("SECRET_TEST_SENTINEL",(path/"budget.json.jsonl").read_text())
        print("INFERENCE_LAB_R19 "+canonical({"cases":len(p["cases"]),
            "calls":p["planned_calls"],"coverage":p["coverage"],"wire":p["arms"],
            "exact_wire_plan":True,"mock_usage_only":True,"actual_network_calls":0}))

    def test_refuse_changed_plan_config_or_limit_before_network(self):
        cfg=config();plan=build_plan(self.doc,cfg,per_stratum=1,tasks=["development"])
        bad=copy(plan);bad["payload"]["schedule"][0]["request_bytes"]+=1
        bad["sha256"]=digest(bad["payload"])
        with self.assertRaisesRegex(ValueError,"RECONSTRUCTION_MISMATCH"):
            verify_plan(self.doc,cfg,bad)
        changed=copy(cfg);changed["arms"][0]["model"]="different"
        with self.assertRaisesRegex(ValueError,"RECONSTRUCTION_MISMATCH"):
            verify_plan(self.doc,changed,plan)
        too_small=copy(cfg);too_small["budget"]["max_wire_bytes"]=1
        refused=build_plan(self.doc,too_small,per_stratum=1,tasks=["development"])
        self.assertIn("WIRE_BYTE_LIMIT",refused["payload"]["violations"])
        with self.assertRaisesRegex(ValueError,"EXCEEDS_DECLARED_LIMITS"):
            verify_plan(self.doc,too_small,refused)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            with self.assertRaisesRegex(ValueError,"AUTHORIZATION"):
                execute_plan(self.doc,cfg,plan,journal=path/"budget",
                    observation_log=path/"observations")
            self.assertFalse((path/"budget").exists())

    def test_unknown_usage_stops_and_preserves_partial_observations(self):
        cfg=config();plan=build_plan(self.doc,cfg,per_stratum=1,tasks=["development"])
        calls=[]
        def fake(provider,request):
            calls.append(digest(request))
            return {"choices":[{"message":{"content":canonical({"task":"development","candidates":[]})}}]}
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            with patch.dict(os.environ,{"LAB_FIXTURE_KEY":"SECRET_TEST_SENTINEL"}), \
                 patch.object(ExplicitJSONLLMProvider,"_request",fake):
                result=execute_plan(self.doc,cfg,plan,journal=path/"budget",
                    observation_log=path/"observations",sourcefree_live_authorized=True)
            self.assertEqual(len(calls),1)
            self.assertEqual(result["status"],"STOPPED_BUDGET_OR_UNKNOWN_SPEND")
            self.assertEqual(result["observations"][0]["outcome"],"BUDGET_STOP")
            self.assertEqual(result["budget"]["reserved_nanos"],101000000)
            self.assertEqual(result["declared_model_rate_estimates"]["F"]["unknown_usage_calls"],1)
            self.assertEqual(len((path/"observations").read_text().splitlines()),1)
            self.assertIn("UNCERTAIN_SPEND_STOP",(path/"budget.jsonl").read_text())


if __name__=="__main__":unittest.main()
