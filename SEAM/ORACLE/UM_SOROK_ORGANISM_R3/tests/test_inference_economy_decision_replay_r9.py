"""A stronger SC-07 replay control: no captured actor snapshots.

Use actual recorded input commands and exact prior semantic decisions, verified
against the original committed chain. Reconstruct the whole history in scratch
storage only when needed. This is an upper-information replay comparator, not
an independent LLM's raw-history inference, and not a production persistence
format or new authority.
"""
from pathlib import Path
from time import perf_counter_ns
from unittest.mock import patch
import tempfile
import unittest

from um_sorok_organism import runtime
from um_sorok_organism.types import canonical, copy, digest
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
import test_tco_r23_relational_transduction as inherited
import test_inference_economy_history_reconstruction_r8 as r8


class DecisionReplayR9(unittest.TestCase):
    def _record(self,path,decision):
        commands=[];tape=[]
        original_init=runtime.ConstitutiveRuntime.initialize
        original_step=runtime.ConstitutiveRuntime.step
        def initialize(rt,*a,**kw):
            result=original_init(rt,*a,**kw)
            commands.append({"method":"initialize","args":copy(a),
                             "kwargs":copy(kw),"result":copy(result)})
            return result
        def step(rt,*a,**kw):
            result=original_step(rt,*a,**kw)
            commands.append({"method":"step","args":copy(a),
                             "kwargs":copy(kw),"result":copy(result)})
            return result
        def provider(cb):
            def record(task,packet):
                result=cb(task,packet)
                tape.append({"task":task,"packet_digest":digest(packet),
                             "decision":copy(result)})
                return result
            return CallbackLLMProvider(record)
        with patch.object(runtime.ConstitutiveRuntime,"initialize",initialize), \
             patch.object(runtime.ConstitutiveRuntime,"step",step), \
             patch.object(inherited,"CallbackLLMProvider",side_effect=provider):
            inherited.CrossContextMetabolismR32._run_history(str(path),decision)
        return commands,tape

    def _replay(self,path,commands,tape):
        offset=0
        def decide(task,packet):
            nonlocal offset
            if offset>=len(tape):raise ValueError("DECISION_REPLAY_MISSING")
            rec=tape[offset];offset+=1
            if rec["task"]!=task or rec["packet_digest"]!=digest(packet):
                raise ValueError("DECISION_REPLAY_SOURCE_MISMATCH")
            return copy(rec["decision"])
        svc=ValidatingSemanticService(CallbackLLMProvider(decide))
        rt=runtime.ConstitutiveRuntime(path,semantic=svc)
        try:
            for cmd in commands:
                if cmd["method"] not in ("initialize","step"):
                    raise ValueError("DECISION_REPLAY_UNSUPPORTED_COMMAND")
                result=getattr(rt,cmd["method"])(*cmd["args"],**cmd["kwargs"])
                if result!=cmd["result"]:
                    raise ValueError("DECISION_REPLAY_EVENT_RESULT_MISMATCH")
            if offset!=len(tape):raise ValueError("DECISION_REPLAY_UNUSED")
            self.assertTrue(rt.verify()["valid"])
            return self._state(rt)
        finally:rt.close()

    @staticmethod
    def _state(rt):
        return {"actors":rt.ledger.actors(),"world":rt.ledger.world()[1],
                "history":rt.verify(),"events":rt.ledger.events()}

    def test_compact_exact_decisions_can_reconstruct_without_stored_topology(self):
        rows={};sources={}
        with tempfile.TemporaryDirectory() as tmp:
            for decision in ("revalue","abstain"):
                src=Path(tmp)/("source-"+decision+".sqlite")
                commands,tape=self._record(src,decision)
                start=perf_counter_ns()
                cold=runtime.ConstitutiveRuntime(src)
                try:original=self._state(cold)
                finally:cold.close()
                reopen_ns=perf_counter_ns()-start
                self.assertTrue(original["history"]["valid"])
                replay=Path(tmp)/("replay-"+decision+".sqlite")
                start=perf_counter_ns()
                recovered=self._replay(replay,commands,tape)
                replay_ns=perf_counter_ns()-start
                self.assertEqual(original,recovered)
                # No relation state was supplied to replay from any snapshot.
                self.assertEqual([c["method"] for c in commands],
                                 ["initialize"]+["step"]*5)
                # On both paths a fresh independent action follows real history.
                reader=r8.HistoricalReconstructionR8()
                stored_future,stored_cost=reader._continue(src,[],False)
                replay_future,replay_cost=reader._continue(replay,[],False)
                self.assertEqual(stored_future,replay_future)
                self.assertEqual(stored_future["actual"]["attempt"],
                                 "REST" if decision=="revalue" else "WAIT")
                self.assertEqual(stored_cost["request_bytes"],replay_cost["request_bytes"])
                self.assertEqual(stored_cost["semantic_calls"],replay_cost["semantic_calls"])
                # Raw material facts and personally lived receipts; deliberately
                # NOT the historical semantic choices, computed psychic audits,
                # or digests of the already transformed actor.
                sources[decision]={"world":original["world"],
                    "events":[{"actual":e["envelope"]["payload"]["actual"],
                       "lived":e["envelope"]["payload"]["private_actor_experience_receipts"]}
                        for e in original["events"] if e["kind"]=="ACTOR_LIFE_TRANSITION"]}
                topology={k:original["actors"]["mother"][k] for k in r8.TOPOLOGY}
                rows[decision]={"historical_commands":len(commands),
                    "historical_decisions_replayed":len(tape),
                    "command_bytes":len(canonical(commands).encode("utf-8")),
                    "decision_tape_bytes":len(canonical(tape).encode("utf-8")),
                    "stored_mother_topology_bytes":len(canonical(topology).encode("utf-8")),
                    "stored_cold_read_ns":reopen_ns,"full_scratch_replay_ns":replay_ns,
                    "stored_future":stored_cost,"replay_future":replay_cost,
                    "actual":stored_future["actual"]["attempt"]}
            # The distinction is a new semantic formation, not a difference
            # in the externally given trajectory. This is an ambiguity witness,
            # not proof that an independently reasoning history-only model loses.
            self.assertEqual(sources["revalue"],sources["abstain"])
        print("INFERENCE_ECONOMY_R9_EXACT_DECISIONS "+canonical({
            "arms":rows,"equal_committed_state_and_history":True,
            "equal_raw_actual_and_lived_facts_across_interpretive_arms":True,
            "no_snapshot_input":True,"not_full_stage_r":True,
            "paid_provider_calls":0,"provider_tokens":None}))

    def test_changed_or_missing_decision_tape_refuses_exact_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"source.sqlite"
            commands,tape=self._record(path,"revalue")
            bad=copy(tape);bad[0]["packet_digest"]="forged"
            with self.assertRaisesRegex(ValueError,"DECISION_REPLAY_SOURCE_MISMATCH"):
                self._replay(Path(tmp)/"wrong.sqlite",commands,bad)
            with self.assertRaisesRegex(ValueError,"DECISION_REPLAY_MISSING"):
                self._replay(Path(tmp)/"short.sqlite",commands,tape[:-1])
            with self.assertRaisesRegex(ValueError,"DECISION_REPLAY_UNUSED"):
                self._replay(Path(tmp)/"long.sqlite",commands,tape+[tape[-1]])


if __name__=="__main__":
    unittest.main()
