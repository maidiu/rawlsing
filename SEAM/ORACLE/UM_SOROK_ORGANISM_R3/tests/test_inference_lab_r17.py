"""Executable sourcefree lab: actual owner history, exact replay and bounded transport.

No paid calls. Fake HTTP tests explicitly patch the existing HTTPS boundary.
"""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from inference_lab_cli import capture_course, replay_course, fixture_arms
from um_sorok_organism.inference_lab import (
    WorkloadCapture, CaptureProvider, ExactTapeProvider, verify_workload,
    load_workload, compare_frozen, save_report, LiveBudget, BudgetedLiveProvider,
    BudgetStop, selected_rows)
from um_sorok_organism.live_psychological_llm import ExplicitJSONLLMProvider
from um_sorok_organism.semantics import CallbackLLMProvider
from um_sorok_organism.types import canonical, copy, digest
from um_sorok_organism.inference_lab_admission import evaluate_admissions, verify_admissions

HEAD="a"*40

def response(task="expression",a=100,b=20):
    return {"choices":[{"message":{"content":canonical({"task":task,"surface":"fixture"})}}],
            "usage":{"prompt_tokens":a,"completion_tokens":b,"total_tokens":a+b}}

def budget(path,**kw):
    params=dict(max_calls=2,max_wire_bytes=100000,input_token_ceiling=10000,
                completion_token_limit=200,input_nanos_per_token=1000,
                output_nanos_per_token=4000,max_budget_nanos=21600000,
                sourcefree_live_authorized=True)
    params.update(kw)
    return LiveBudget(journal=path,**params)

def provider(b):
    return BudgetedLiveProvider(budget=b,endpoint="https://example.invalid/chat/completions",
         model="fixture",api_key="not-a-key",allow_private_actor_data=True,metrics_capacity=1)


class InferenceLab(unittest.TestCase):
    def test_actual_owner_course_capture_cold_exact_replay_and_frozen_comparison(self):
        doc,actual,witness=capture_course(True,HEAD,with_admissions=True)
        self.assertEqual(len(witness["payload"]["rows"]),182)
        self.assertEqual(len(doc["payload"]["rows"]),225)
        self.assertTrue(actual["audit"]["valid"])
        self.assertEqual(doc["payload"]["owner_state_sha256"],digest(actual))
        self.assertEqual(actual["first"]["received"]["counterpart_ref"],"x5")
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"tape.json"
            save_report(path,doc)
            self.assertEqual(path.stat().st_mode&0o777,0o600)
            self.assertEqual(load_workload(path,source_head=HEAD),doc)
            with self.assertRaises(FileExistsError):save_report(path,doc)
            cold=load_workload(path,source_head=HEAD)
            self.assertEqual(replay_course(cold,HEAD),actual)
            result=compare_frozen(cold,fixture_arms(cold),per_task=2)
            self.assertEqual(len(result["observations"]),16)
            self.assertEqual(result["scope"],"PROPOSAL_ONLY_NOT_ADMITTED_DEVELOPMENT")
            for row in result["observations"]:
                self.assertEqual(row["outcome"],"PROPOSAL_RETURNED")
                self.assertTrue(row["equals_recorded_proposal"])
                self.assertIsNone(row["metric"]["usage"]["input_tokens"])
            for k,t in result["totals"].items():
                self.assertIsNone(t["input_tokens"])
                self.assertEqual(t["calls"],2)
            full=sum(x["request_bytes"] for k,x in result["totals"].items() if k.startswith("F/"))
            comp=sum(x["request_bytes"] for k,x in result["totals"].items() if k.startswith("E/"))
            self.assertLess(comp,full)
            # The local scratch court uses the actual original admission owner.
            before=digest(witness)
            evaluated=evaluate_admissions(cold,witness,result)
            self.assertEqual(len(evaluated["observations"]),4)
            self.assertTrue(all(x["matches_recorded_admission"] for x in evaluated["observations"]))
            dev=next(x for x in result["observations"] if x["task"]=="development")
            forged=copy(result);forged["observations"]=[copy(dev)]
            item=forged["observations"][0]
            item["proposal"]={"task":"development","candidates":[{"kind":"NOT_AN_OWNER_OPERATION"}]}
            item["proposal_digest"]=digest(item["proposal"])
            refused=evaluate_admissions(cold,witness,forged)["observations"][0]
            self.assertEqual(refused["outcome"],"OWNER_REFUSED_SCRATCH")
            self.assertFalse(refused["actor_changed"])
            self.assertEqual(digest(witness),before)
            self.assertEqual(digest(actual),doc["payload"]["owner_state_sha256"])
            print("INFERENCE_LAB_R17 "+canonical({
                "workload_rows":len(doc["payload"]["rows"]),
                "tape_bytes":path.stat().st_size,"actual_complete_history_equal":True,
                "frozen_calls":len(result["observations"]),
                "admission_witnesses":len(witness["payload"]["rows"]),
                "admission_witness_bytes":len(canonical(witness).encode("utf-8")),
                "matched_scratch_admissions":len(evaluated["observations"]),
                "forged_scratch_refused":True,
                "F_request_bytes":full,"E_request_bytes":comp,
                "provider_tokens":None,"network_calls":0}))

    def test_source_scope_integrity_caps_and_exact_sequence(self):
        with self.assertRaisesRegex(ValueError,"ATTESTATION"):
            WorkloadCapture(source_head=HEAD,fixture="fixture")
        p=CallbackLLMProvider(lambda t,x:{"task":t,"surface":"fixture"})
        c=WorkloadCapture(source_head=HEAD,fixture="fixture",
                           sourcefree_fixture_attested=True,max_rows=1)
        packet={"actor":"sourcefree","text":"é"}
        CaptureProvider(p,c).propose("expression",packet)
        doc=c.document()
        with self.assertRaisesRegex(ValueError,"HEAD_MISMATCH"):
            verify_workload(doc,source_head="b"*40)
        bad=copy(doc);bad["payload"]["rows"][0]["packet"]["text"]="changed"
        with self.assertRaisesRegex(ValueError,"INTEGRITY"):verify_workload(bad)
        bad["sha256"]=digest(bad["payload"])
        with self.assertRaisesRegex(ValueError,"ROW_INTEGRITY"):verify_workload(bad)
        r=ExactTapeProvider(doc,source_head=HEAD,original_grade="fixture")
        with self.assertRaisesRegex(ValueError,"UNUSED"):r.finish()
        with self.assertRaisesRegex(ValueError,"CONTEXT_MISMATCH"):
            r.propose("expression",{"actor":"other"})
        self.assertEqual(r.propose("expression",packet),{"task":"expression","surface":"fixture"})
        r.finish()
        with self.assertRaisesRegex(ValueError,"EXHAUSTED"):r.propose("expression",packet)
        with self.assertRaisesRegex(ValueError,"CAP"):
            c.invoke(p,"expression",packet)
        with self.assertRaisesRegex(ValueError,"INCOMPLETE"):c.document()

    def test_shared_budget_reserves_before_send_and_refuses_third_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            b=budget(Path(tmp)/"budget")
            one=provider(b);two=provider(b)
            seen=[]
            def fake(p,payload):
                seen.append(payload)
                self.assertTrue(b.pending)
                self.assertEqual(payload["max_completion_tokens"],200)
                self.assertIn("RESERVED_BEFORE_SEND",b.log.read_text())
                return response()
            with patch.object(ExplicitJSONLLMProvider,"_request",fake):
                one.propose("expression",{"actor":"fiction"})
                two.propose("expression",{"actor":"fiction"})
                with self.assertRaises(BudgetStop):one.propose("expression",{})
            self.assertEqual(len(seen),2)
            self.assertEqual(b.snapshot()["reserved_nanos"],21600000)
            self.assertEqual(b.snapshot()["reported_usage_rate_estimate_nanos"],360000)
            self.assertTrue(b.stopped)
            self.assertEqual(len(b.log.read_text().splitlines()),4)
            self.assertEqual(one.usage_snapshot()["receipts"][-1]["outcome"],"REJECTED_OR_FAILED")

    def test_live_unknown_usage_stops_and_keeps_reservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            b=budget(Path(tmp)/"unknown")
            p=provider(b);seen=[]
            def unknown(_self,payload):
                seen.append(payload)
                x=response();x.pop("usage");return x
            with patch.object(ExplicitJSONLLMProvider,"_request",unknown):
                with self.assertRaises(BudgetStop):p.propose("expression",{})
                with self.assertRaises(BudgetStop):p.propose("expression",{})
            self.assertEqual(len(seen),1)
            self.assertTrue(b.stopped)
            self.assertEqual(b.reserved,10800000)
            self.assertIn("UNCERTAIN_SPEND_STOP",b.log.read_text())
            with self.assertRaisesRegex(ValueError,"AUTHORIZATION"):
                budget(Path(tmp)/"denied",sourcefree_live_authorized=False)
            self.assertFalse((Path(tmp)/"denied").exists())

    def test_partial_matched_report_conserves_completed_observations(self):
        c=WorkloadCapture(source_head=HEAD,fixture="fixture",sourcefree_fixture_attested=True)
        cp=CallbackLLMProvider(lambda t,p:{"task":t,"surface":"fixture"})
        for i in range(2):c.invoke(cp,"expression",{"i":i})
        with tempfile.TemporaryDirectory() as tmp:
            b=budget(Path(tmp)/"budget",max_calls=1)
            p=provider(b);seen=[]
            def fake(_self,payload):
                seen.append(payload);return response()
            with patch.object(ExplicitJSONLLMProvider,"_request",fake):
                r=compare_frozen(c.document(),{"one":p,"two":provider(b)},per_task=2)
            self.assertEqual(r["planned_observations"],4)
            self.assertEqual(r["status"],"STOPPED_BUDGET_OR_UNKNOWN_SPEND")
            self.assertEqual(len(seen),1)
            self.assertEqual([x["outcome"] for x in r["observations"]],
                             ["PROPOSAL_RETURNED","BUDGET_STOP"])

    def test_completion_cap_is_opt_in_and_no_transport_override(self):
        seen=[]
        def wire(req):
            seen.append(req);return response()
        p=ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
          model="fixture",api_key="not-a-key",allow_private_actor_data=True,transport=wire)
        p.propose("expression",{})
        self.assertNotIn("max_completion_tokens",seen[-1])
        with tempfile.TemporaryDirectory() as tmp:
            b=budget(Path(tmp)/"budget")
            with self.assertRaisesRegex(ValueError,"NO_TRANSPORT_OVERRIDE"):
                BudgetedLiveProvider(budget=b,endpoint="https://example.invalid/chat/completions",
                   model="fixture",api_key="not-a-key",allow_private_actor_data=True,transport=wire)


if __name__=="__main__":unittest.main()
