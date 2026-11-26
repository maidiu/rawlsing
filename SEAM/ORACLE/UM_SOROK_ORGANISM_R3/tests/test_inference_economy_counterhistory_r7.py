"""R53 owner source: actual counterhistory needs new semantic work, not a cache.

Measure stage-local semantic expenditure and exact packet compilation. Both
nomination and abstention receive the same qualified offer; neither follows
from a byte budget. All outcomes are sourcefree controlled choices.
"""
from collections import defaultdict
from pathlib import Path
import json
import tempfile
import unittest

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import ValidatingSemanticService, HeuristicSemanticProvider
from um_sorok_organism.live_psychological_llm import (
    ExplicitJSONLLMProvider, _expand_exact_aliases)
from um_sorok_organism.types import canonical, copy, digest


PARENT={'source_ref':'R53_FICTIONAL_PARENT',
        'source_grade':'SOURCEFREE_TEST_FIXTURE_NOT_EMPIRICAL',
        'answers':{'r53':'not_a_survey_observation'},'fictional_seed':{'projects':[]}}


class CounterhistoryEconomyR7(unittest.TestCase):
    def _course(self, release, compiled):
        stage="initialize"; acquire=True; witnesses=[]; offers=[]
        def callback(task,p):
            nonlocal acquire
            if task=="adult_constructor":
                return HeuristicSemanticProvider().propose(task,p)
            if task=="expression":
                self.assertNotIn("historically_possible_counterhistory_release",p)
                return {"task":task,"surface":"The household continues."}
            if task=="actor_attempt":
                self.assertNotIn("historically_possible_counterhistory_release",p)
                return {"task":task,"action":"EAT" if p["actor"]["id"]=="mother"
                    and any(o["action"]=="EAT" for o in p["options"]) else "WAIT"}
            if task!="development":raise AssertionError(task)
            candidates=[]
            if p["actor"]["id"]=="mother" and p["experience"].get("own_action")=="EAT":
                if acquire:
                    candidates=[{"kind":"ACQUIRE_HISTORICAL_ORIENTATION",
                                 "operation":"EAT","orientation_mode":"WITHHOLD"}]
                    acquire=False
                else:
                    qualified=p["historically_possible_counterhistory_release"]
                    offers.append((stage,copy(qualified)))
                    if stage=="second_relief" and release:candidates=qualified
            return {"task":task,"candidates":candidates}
        def send(req):
            body=json.loads(req["messages"][1]["content"])
            task=body["task"]
            p=_expand_exact_aliases(task,body["actor_source_packet"],
                                      body.get("same_call_exact_aliases",{}))
            if task=="development" and p.get("historically_possible_counterhistory_release"):
                self.assertIn("entire counterhistory_release_basis",req["messages"][0]["content"])
            result=callback(task,p)
            witnesses.append({"stage":stage,"task":task,"digest":digest(p),
                "qualified_releases":len(p.get("historically_possible_counterhistory_release",[])),
                "proposed_changes":len(result.get("candidates",[]))})
            return {"choices":[{"message":{"content":canonical(result)}}]}
        provider=ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
            model="sourcefree-fixture",api_key="not-a-key",allow_private_actor_data=True,
            transport=send,metrics_capacity=1000,compact_exact_packet=compiled)
        svc=ValidatingSemanticService(provider)
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/"counterhistory.sqlite"
            rt=ConstitutiveRuntime(db,semantic=svc)
            try:
                rt.initialize([("mother","Mother",PARENT),("father","Father",PARENT)])
                stage="acquire"
                rt.step("mother",requested_action="EAT")
                initial=rt.snapshot("mother")["historical_orientations"][0]
                self.assertTrue(any(o["action"]=="EAT" for o in
                                    rt.situated("mother")["suspended_actions"]))
                stage="first_relief"
                rt.step("mother",requested_action="EAT")
                self.assertEqual(offers,[("first_relief",[])])
                stage="second_relief"
                rt.step("mother",requested_action="EAT")
                self.assertEqual(len(offers[1][1]),1)
                saved=rt.snapshot("mother")
                row=saved["historical_orientations"][0]
                self.assertEqual(row["id"],initial["id"])
                self.assertEqual({k:v for k,v in row.items() if k!="revisions"},
                                 {k:v for k,v in initial.items() if k!="revisions"})
                self.assertEqual(saved["memories"],[])
                self.assertTrue(rt.verify()["valid"])
                self.assertEqual(any(o["action"]=="EAT" for o in
                    rt.situated("mother")["suspended_actions"]),not release)
            finally:rt.close()
            cold=ConstitutiveRuntime(db,semantic=svc)
            try:
                stage="cold_independent"
                self.assertEqual(cold.snapshot("mother"),saved)
                actual=cold.step("mother")
                self.assertEqual(actual["attempt"],"EAT" if release else "WAIT")
                self.assertEqual(actual["status"],"PERFORMED")
                final={"world":cold.ledger.world()[1],"actor":cold.snapshot("mother"),
                       "history":cold.verify(),"actual":actual}
                self.assertTrue(final["history"]["valid"])
            finally:cold.close()
        metrics=provider.usage_snapshot()
        self.assertEqual(metrics["evicted"],0)
        self.assertEqual(len(metrics["receipts"]),len(witnesses))
        by_stage=defaultdict(lambda:defaultdict(lambda:{
            "calls":0,"request_bytes":0,"qualified_releases":0,"proposed_changes":0}))
        for m,w in zip(metrics["receipts"],witnesses):
            self.assertEqual(m["task"],w["task"])
            self.assertEqual(m["transport"],"MOCK")
            self.assertIsNone(m["usage"]["input_tokens"])
            row=by_stage[w["stage"]][w["task"]]
            row["calls"]+=1
            row["request_bytes"]+=m["request_bytes"]
            row["qualified_releases"]+=w["qualified_releases"]
            row["proposed_changes"]+=w["proposed_changes"]
        return final,witnesses,offers,{s:dict(v) for s,v in by_stage.items()}

    def test_same_evidence_distinct_reconstitution_and_exact_transport(self):
        rows={}
        for release in (False,True):
            original=self._course(release,False)
            compact=self._course(release,True)
            self.assertEqual(original[:3],compact[:3])
            rows[str(release)]={
                "full":original[3],"compiled":compact[3],
                "actual":original[0]["actual"]["attempt"],
                "first_and_second_relief_offer_counts":[len(x[1]) for x in original[2][:2]]}
        # Same source evidence offered in both arms; compare only up to the
        # nomination, not post-reconstitution packets, which must differ.
        abstain=self._course(False,False)
        nominate=self._course(True,False)
        self.assertEqual(abstain[2][:2],nominate[2][:2])
        self.assertEqual([x for x in abstain[1] if x["stage"] in ("initialize","acquire","first_relief")],
                         [x for x in nominate[1] if x["stage"] in ("initialize","acquire","first_relief")])
        print("INFERENCE_ECONOMY_R7_COUNTERHISTORY "+canonical({
            "arms":rows,"exact_packet_and_causal_equality_within_arm":True,
            "same_offers_before_choice":True,"provider_tokens":None,
            "not_a_semantic_suppression_policy":True}))


if __name__=="__main__":
    unittest.main()
