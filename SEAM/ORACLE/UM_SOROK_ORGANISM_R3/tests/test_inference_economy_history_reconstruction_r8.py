"""SC-07 exact historical-reconstruction CONTROL (not full Stage R).

The history arm receives the same actual events and original semantic decisions
as the stored-organization arm. Test-only captured pre-admission witnesses omit
links/motifs; every reconstruction uses the existing admission owner and is
checked against committed actor digests. No new persistent journal, no
production replay claim, no raw-history-only semantic prediction claim.
"""
import json
import sqlite3
import tempfile
from collections import Counter
from pathlib import Path
from time import perf_counter_ns
from unittest.mock import patch
import unittest

from um_sorok_organism import runtime
from um_sorok_organism.types import canonical, copy, digest
from um_sorok_organism.development import admit
from um_sorok_organism.live_psychological_llm import ExplicitJSONLLMProvider
from um_sorok_organism.semantics import ValidatingSemanticService
import test_tco_r23_relational_transduction as inherited


TOPOLOGY=("links","relational_motifs")


def without_topology(actor):
    return copy({k:v for k,v in actor.items() if k not in TOPOLOGY})


def reconstruct(actor_id,history,events):
    """Ephemeral research comparator; no read of the actor's final topology."""
    topology={k:[] for k in TOPOLOGY}
    events_for_actor=[]
    for row in events:
        env=row["envelope"]
        if env["kind"]!="ACTOR_LIFE_TRANSITION":continue
        p=env["payload"]
        if actor_id in p["developmental_effects"]:
            events_for_actor.append(env)
    if len(history)!=len(events_for_actor):
        raise ValueError("HISTORY_REPLAY_INCOMPLETE")
    for rec,env in zip(history,events_for_actor):
        p=env["payload"]
        if (rec["event"]!=p["objective_ref"]
                or rec["actor"]["id"]!=actor_id
                or rec["experience"]!=p["private_actor_experience_receipts"][actor_id]):
            raise ValueError("HISTORY_REPLAY_SOURCE_MISMATCH")
        actor=copy(rec["actor"])
        if any(k in actor for k in TOPOLOGY):
            raise ValueError("HISTORY_REPLAY_PRECOMPUTED_TOPOLOGY")
        actor.update(copy(topology))
        effects=admit(actor,rec["experience"],rec["event"],copy(rec["candidates"]),
                      issued_trial=rec["issued_trial"])
        if (effects!=p["developmental_effects"][actor_id]
                or digest(actor)!=env["actor_digests"][actor_id]):
            raise ValueError("HISTORY_REPLAY_COMMITTED_STATE_MISMATCH")
        topology={k:copy(actor[k]) for k in TOPOLOGY}
    return topology


class HistoricalReconstructionR8(unittest.TestCase):
    def _history(self,path,decision):
        records=[]
        def capture(actor,experience,event_ref,candidates,**kw):
            if actor["id"]=="mother":
                if not records:
                    self.assertEqual({k:actor[k] for k in TOPOLOGY},
                                     {k:[] for k in TOPOLOGY})
                records.append({"actor":without_topology(actor),
                    "experience":copy(experience),"event":event_ref,
                    "candidates":copy(candidates),
                    "issued_trial":copy(kw.get("issued_trial"))})
            return admit(actor,experience,event_ref,candidates,**kw)
        with patch.object(runtime,"admit",capture):
            inherited.CrossContextMetabolismR32._run_history(str(path),decision)
        return records

    def _clone(self,src,dst):
        with sqlite3.connect(src) as a,sqlite3.connect(dst) as b:
            a.backup(b)

    def _continue(self,path,history,replay):
        seen=[];reads=Counter();replay_ns=0
        def send(req):
            body=json.loads(req["messages"][1]["content"])
            task=body["task"];p=body["actor_source_packet"]
            seen.append((task,digest(p)))
            if task=="actor_attempt":
                out={"task":task,"action":"REST" if any(
                    x["action"]=="REST" for x in p["options"]) else "WAIT"}
            elif task=="development":out={"task":task,"candidates":[]}
            elif task=="expression":out={"task":task,"surface":"The household continues."}
            else:raise AssertionError(task)
            return {"choices":[{"message":{"content":canonical(out)}}]}
        provider=ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
            model="sourcefree-fixture",api_key="not-a-key",
            allow_private_actor_data=True,transport=send,metrics_capacity=100)
        rt=runtime.ConstitutiveRuntime(path,semantic=ValidatingSemanticService(provider))
        try:
            self.assertTrue(rt.verify()["valid"])
            events=rt.ledger.events()
            original=runtime.materialize
            def materialize(actor,world):
                nonlocal replay_ns
                if actor["id"]!="mother":return original(actor,world)
                reads["mother"]+=1
                if replay:
                    t=perf_counter_ns()
                    restored=reconstruct("mother",history,events)
                    replay_ns+=perf_counter_ns()-t
                    actor=without_topology(actor)
                    actor.update(restored)
                return original(actor,world)
            start=perf_counter_ns()
            with patch.object(runtime,"materialize",materialize):
                # Actual native selection; not requested by the court.
                result=rt.step("mother")
            step_ns=perf_counter_ns()-start
            metrics=provider.usage_snapshot()
            self.assertEqual(metrics["evicted"],0)
            self.assertTrue(all(x["transport"]=="MOCK" for x in metrics["receipts"]))
            self.assertTrue(all(x["usage"]["input_tokens"] is None
                                for x in metrics["receipts"]))
            self.assertTrue(rt.verify()["valid"])
            return ({"actual":result,"actors":rt.ledger.actors(),
                "world":rt.ledger.world()[1],"chain":rt.verify(),"semantic":seen},
                {"materialize_reads":reads["mother"],"step_ns":step_ns,
                 "reconstruction_ns":replay_ns,"semantic_calls":len(seen),
                 "request_bytes":sum(x["request_bytes"] for x in metrics["receipts"])})
        finally:rt.close()

    def test_exact_reconstruction_control_actual_cold_continuation(self):
        rows={}
        with tempfile.TemporaryDirectory() as tmp:
            for decision in ("revalue","abstain"):
                path=Path(tmp)/("original-"+decision+".sqlite")
                history=self._history(path,decision)
                cold=runtime.ConstitutiveRuntime(path)
                try:
                    self.assertTrue(cold.verify()["valid"])
                    events=cold.ledger.events()
                    t=perf_counter_ns()
                    restored=reconstruct("mother",history,events)
                    initial_replay_ns=perf_counter_ns()-t
                    actor=cold.snapshot("mother")
                    stored={k:actor[k] for k in TOPOLOGY}
                    self.assertEqual(restored,stored)
                    self.assertTrue(stored["relational_motifs"])
                    historical_bytes=len(canonical(history).encode("utf-8"))
                    topology_bytes=len(canonical(stored).encode("utf-8"))
                finally:cold.close()
                results=[]
                for replay in (False,True):
                    dest=Path(tmp)/("future-"+decision+str(replay)+".sqlite")
                    self._clone(path,dest)
                    results.append(self._continue(dest,history,replay))
                self.assertEqual(results[0][0],results[1][0])
                self.assertEqual(results[0][1]["semantic_calls"],results[1][1]["semantic_calls"])
                self.assertEqual(results[0][1]["request_bytes"],results[1][1]["request_bytes"])
                self.assertGreater(results[1][1]["reconstruction_ns"],0)
                self.assertEqual(results[0][0]["actual"]["attempt"],
                                 "REST" if decision=="revalue" else "WAIT")
                rows[decision]={"actual":results[0][0]["actual"]["attempt"],
                    "historical_admissions":len(history),
                    "captured_history_bytes":historical_bytes,
                    "stored_topology_bytes":topology_bytes,
                    "initial_reconstruction_ns":initial_replay_ns,
                    "stored":results[0][1],"replayed":results[1][1]}
        print("INFERENCE_ECONOMY_R8_REPLAY "+canonical({
            "arms":rows,"equal_actual_and_semantic_packets":True,
            "original_decisions_supplied_to_both":True,
            "test_only_pre_admission_witnesses":True,
            "not_full_stage_r":True,"provider_tokens":None}))

    def test_severed_or_changed_history_cannot_be_reconstructed_as_fact(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"adverse.sqlite"
            history=self._history(path,"revalue")
            cold=runtime.ConstitutiveRuntime(path)
            try:
                self.assertTrue(cold.verify()["valid"])
                events=cold.ledger.events()
                with self.assertRaisesRegex(ValueError,"HISTORY_REPLAY_INCOMPLETE"):
                    reconstruct("mother",history[:-1],events)
                bad=copy(history);bad[0]["event"]="forged"
                with self.assertRaisesRegex(ValueError,"HISTORY_REPLAY_SOURCE_MISMATCH"):
                    reconstruct("mother",bad,events)
                bad=copy(history)
                # Same event grounds, different valid semantic relation choice.
                # A committed historical result must not be silently rewritten.
                changed=False
                for rec in bad:
                    for c in rec["candidates"]:
                        if c.get("kind")=="REORGANIZE_RELATIONAL_MOTIF":
                            c["new_relation"]="CONTRADICTS"
                            changed=True
                self.assertTrue(changed)
                with self.assertRaisesRegex(ValueError,"HISTORY_REPLAY_COMMITTED_STATE_MISMATCH"):
                    reconstruct("mother",bad,events)
                bad=copy(history);bad[0]["actor"]["links"]=[]
                with self.assertRaisesRegex(ValueError,"HISTORY_REPLAY_PRECOMPUTED_TOPOLOGY"):
                    reconstruct("mother",bad,events)
                self.assertTrue(cold.verify()["valid"])
            finally:cold.close()


if __name__=="__main__":
    unittest.main()
