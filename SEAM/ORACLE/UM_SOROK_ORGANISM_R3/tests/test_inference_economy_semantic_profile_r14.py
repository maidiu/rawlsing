"""Account for epistemic packet functions without inferring psychic demand.

The counts describe the actual interface, not an actor's labor, conscious
intent, causal need for a call or accepted formations. No new scheduling.
"""
from collections import Counter
from unittest.mock import patch
import unittest

from um_sorok_organism.types import canonical
from um_sorok_organism.live_psychological_llm import ExplicitJSONLLMProvider
import test_inference_economy_counterhistory_r7 as r7


class SemanticPacketProfileR14(unittest.TestCase):
    def test_redacted_exact_accounting_and_no_offer_does_not_bar_new_proposal(self):
        private="secret actor memory and identity é"
        packet={"actor_forms":{"private_key":{"id":private}},
                "historically_possible_counterhistory_release":[],
                "historically_proposed_functional":[],
                private:{"value":private}}
        out={"task":"development","candidates":[{"kind":"ACQUIRE_FORM","meaning":private}]}
        requests=[]
        p=ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
            model="fixture",api_key="not-a-key",allow_private_actor_data=True,
            transport=lambda req:requests.append(req) or
                {"choices":[{"message":{"content":canonical(out)}}]},
            metrics_capacity=2,profile_semantic_demand=True)
        self.assertEqual(p.propose("development",packet),out)
        self.assertEqual(len(requests),1)
        row=p.usage_snapshot()["receipts"][0]
        profile=row["semantic_packet_profile"]
        self.assertEqual(profile["development_offer_shape"],
            {"family_fields":2,"nonempty_family_fields":0,"list_entries":0})
        self.assertEqual(row["proposed_candidate_count"],1)
        self.assertEqual(sum(x["canonical_field_bytes"] for x in profile["groups"].values())+
                         profile["json_framing_bytes"],row["packet_bytes"])
        self.assertNotIn(private,canonical(row))
        self.assertNotIn("private_key",canonical(row))
        self.assertEqual(profile["groups"]["unclassified"]["fields"],1)
        # This is a valid transport proposal, NOT developmental admission.

    def test_actual_counterhistory_profile_never_changes_call_or_state(self):
        original=r7.ExplicitJSONLLMProvider
        rows={}
        for release in (False,True):
            arms=[]
            for enabled in (False,True):
                providers=[]
                def factory(**kw):
                    p=original(**kw,profile_semantic_demand=enabled)
                    providers.append(p)
                    return p
                with patch.object(r7,"ExplicitJSONLLMProvider",factory):
                    result=r7.CounterhistoryEconomyR7()._course(release,True)
                self.assertEqual(len(providers),1)
                rec=providers[0].usage_snapshot()["receipts"]
                arms.append((result,rec))
            self.assertEqual(arms[0][0],arms[1][0])
            self.assertEqual(len(arms[0][1]),len(arms[1][1]))
            totals=Counter(); shapes=Counter()
            for a,b in zip(arms[0][1],arms[1][1]):
                self.assertNotIn("semantic_packet_profile",a)
                self.assertEqual(a["request_bytes"],b["request_bytes"])
                self.assertEqual(a["packet_bytes"],b["packet_bytes"])
                p=b["semantic_packet_profile"]
                self.assertEqual(sum(x["canonical_field_bytes"] for x in p["groups"].values())+
                                 p["json_framing_bytes"],b["packet_bytes"])
                if b["task"]=="development":
                    totals.update({k:v["canonical_field_bytes"] for k,v in p["groups"].items()})
                    shapes["calls"]+=1
                    shapes["proposed_candidates"]+=b["proposed_candidate_count"]
                    shapes["zero_candidate_calls"]+=b["proposed_candidate_count"]==0
                    shapes["nonempty_family_fields"]+=p["development_offer_shape"]["nonempty_family_fields"]
                    shapes["list_entries"]+=p["development_offer_shape"]["list_entries"]
                    shapes["calls_without_populated_offer_fields"]+=p["development_offer_shape"]["nonempty_family_fields"]==0
            self.assertGreater(shapes["zero_candidate_calls"],0)
            self.assertGreater(shapes["proposed_candidates"],0)
            rows[str(release)]={"development_field_bytes":dict(totals),
                 "proposal_observations":dict(shapes),"same_requests_and_state":True}
        print("INFERENCE_ECONOMY_R14_PROFILE "+canonical(rows))


if __name__=="__main__":unittest.main()
