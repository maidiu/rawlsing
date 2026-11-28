"""Measure actual R54 life continuation through the existing semantic adapter.

Scope: an owner-qualified sourcefree fictional course, not human attention
calibration, a live-model ablation, or a machine-cost-to-person-cost identity.
The released focal opportunity is an actual change in available activity, not
a reason to suppress a call. Preserve the admitted development and private
rehearsal, trial and project continuation.
"""
from collections import Counter, defaultdict
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.live_psychological_llm import (
    ExplicitJSONLLMProvider, _expand_exact_aliases, _expand_structured_fields)
from um_sorok_organism.types import canonical, digest
import test_released_attention_r54 as owner


def byte_size(value):
    return len(canonical(value).encode("utf-8"))


class ReleasedAttentionEconomyR15(unittest.TestCase):
    def _run(self,release,compiled,forge=False):
        providers=[]; witnesses=[]; fields=Counter(); phases=Counter()
        def factory(cb):
            def transport(req):
                body=json.loads(req["messages"][1]["content"]); task=body["task"]
                packet=_expand_exact_aliases(task,body["actor_source_packet"],
                                             body.get("same_call_exact_aliases",{}))
                packet=_expand_structured_fields(task,packet,
                                                body.get("reconstructed_fields",{}))
                if task=="development":
                    selected=packet["selected_constitution"]
                    history=packet["historical_psychodynamic_context"]
                    for k,v in selected.items():
                        # Fixed runtime keys; only totals, not names from data.
                        fields["selected."+k]+=byte_size(v)
                    for phase in ("before_objective_transition",
                                  "after_world_before_formation"):
                        for k,v in history[phase].items():
                            phases[phase+"."+k]+=byte_size(v)
                    if packet.get("historically_possible_monitoring_changes"):
                        self.assertIn("entire monitoring_basis or monitoring_revision_basis",
                                      req["messages"][0]["content"])
                if task=="actor_attempt" and packet.get("focal_encounter_options"):
                    self.assertIn("exact focal_encounter_id",req["messages"][0]["content"])
                if task=="expression":
                    self.assertNotIn("focal_encounter_receipt",packet["actor_accessible"])
                    self.assertNotIn("historically_possible_monitoring_changes",packet)
                ans=cb(task,packet)
                witnesses.append((task,digest(packet),digest(ans)))
                return {"choices":[{"message":{"content":canonical(ans)}}]}
            p=ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
                model="sourcefree-fixture",api_key="not-a-key",allow_private_actor_data=True,
                transport=transport,compact_exact_packet=compiled,
                compact_structured_packet=compiled,metrics_capacity=10000,
                profile_semantic_demand=True)
            providers.append(p)
            return p
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"world.sqlite"
            with patch.object(owner,"CallbackLLMProvider",side_effect=factory):
                first=owner.ReleasedAttentionR54().run_arm(path,release,forge=forge)
            rt=ConstitutiveRuntime(path)
            try:
                self.assertTrue(rt.verify()["valid"])
                final={"world":rt.ledger.world()[1],"actors":rt.ledger.actors(),
                       "chain":rt.verify(),"events":rt.ledger.events()}
            finally:rt.close()
        totals=defaultdict(lambda:dict(calls=0,raw_bytes=0,request_bytes=0,
                                       max_raw_bytes=0,aliases=0,structured=0))
        for p in providers:
            snap=p.usage_snapshot();self.assertEqual(snap["evicted"],0)
            for m in snap["receipts"]:
                self.assertEqual(m["transport"],"MOCK")
                self.assertEqual(m["outcome"],"PROPOSAL_RETURNED")
                self.assertIsNone(m["usage"]["input_tokens"])
                row=totals[m["task"]]
                row["calls"]+=1;row["raw_bytes"]+=m["packet_bytes"]
                row["request_bytes"]+=m["request_bytes"]
                row["max_raw_bytes"]=max(row["max_raw_bytes"],m["packet_bytes"])
                row["aliases"]+=m["alias_count"];row["structured"]+=m["structured_field_count"]
        return (first,final,witnesses,dict(totals),dict(fields),dict(phases))

    def test_actual_released_focal_opportunity_and_new_project(self):
        rows={}
        for release in (False,True):
            full=self._run(release,False);compact=self._run(release,True)
            self.assertEqual(full[:3],compact[:3])
            self.assertEqual(full[4:],compact[4:])
            for task in full[3]:
                self.assertEqual(full[3][task]["calls"],compact[3][task]["calls"])
                self.assertEqual(full[3][task]["raw_bytes"],compact[3][task]["raw_bytes"])
                self.assertLessEqual(compact[3][task]["request_bytes"],full[3][task]["request_bytes"])
            self.assertEqual(bool(full[0]["received"]),release)
            if release:self.assertEqual(full[0]["received"]["counterpart_ref"],"x5")
            rows[str(release)]={"full":full[3],"compiled":compact[3],
                 "selected_projection_field_value_bytes":full[4],
                 "historical_phase_field_value_bytes":full[5],
                 "received_new_other":bool(full[0]["received"])}
        print("INFERENCE_ECONOMY_R15_RELEASED_ATTENTION "+canonical({
            "arms":rows,"exact_outcomes_and_packets_within_arm":True,
            "model_tokens":None,"value_bytes_exclude_field_names_and_framing":True,
            "no_automatic_call_suppression":True}))

    def test_forged_release_still_rolls_back_with_compilation(self):
        self._run(True,True,forge=True)


if __name__=="__main__":unittest.main()
