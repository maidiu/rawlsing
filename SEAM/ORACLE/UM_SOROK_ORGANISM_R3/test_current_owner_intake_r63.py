"""Current exact owners, separate intake; no claims of their mutual merge."""
import os
import tempfile
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
import unittest

from modern_generation_port_r28 import ConditionalPolicy,policy_check
from test_modern_generation_port_r28 import action,policy
from um_sorok_organism.semantics import CallbackLLMProvider
from um_sorok_organism.runtime import ConstitutiveRuntime

class CurrentOwnerIntake(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("INFERENCE_OWNER_LANE")=="CO","separate CO checkout")
    def test_co_actual_local_transfer_and_actor_local_affect(self):
        from test_early_ordinary_practice_r66 import EarlyOrdinaryPractice
        from um_sorok_organism.types import canonical
        old=CallbackLLMProvider.propose
        routes=[]
        def bridged(provider,task,packet):
            original=old(provider,task,packet)
            if task!="development":return original
            rules=[];wanted=[]
            for c in original.get("candidates",[]):
                if c.get("ordinary_vocal_context_transfer"):
                    rules.append({"offer":"historically_possible_ordinary_context_transfers",
                        "match":{"project_id":c["project_id"]}})
                    wanted.append(c)
                elif c.get("kind")=="ACQUIRE_ACTIVITY_AFFECT":
                    if c["basis"].get("formation_source")!="OWN_ORDINARY_PROJECT_EXERCISE":continue
                    rules.append({"offer":"historically_possible_activity_affects","construct":"ACTIVITY_AFFECT",
                        "match":c["basis"],"augment":{k:c[k] for k in ("affect_name","personal_sense","course_orientation")}})
                    wanted.append(c)
            if not rules:return original
            pol=policy([],rules);policy_check(pol)
            p=ConditionalPolicy({packet["actor"]["id"]:pol})
            admitted=p.propose(task,packet)["candidates"]
            # policy() base may include local proposals; retain only the
            # specific owner fixture's nominations, from the actual compiler.
            actual=[c for c in admitted if any(canonical(c)==canonical(q) for q in wanted)]
            self.assertEqual({canonical(c) for c in wanted},{canonical(c) for c in actual})
            routes.extend(p.routes.items())
            result=deepcopy(original)
            for i,c in enumerate(result["candidates"]):
                match=next((q for q in actual if canonical(c)==canonical(q)),None)
                if match is not None:result["candidates"][i]=match
            return result
        owner=EarlyOrdinaryPractice()
        with tempfile.TemporaryDirectory() as d,patch.object(CallbackLLMProvider,"propose",bridged):
            owner.productive_ordinary_arm(Path(d)/"co.db",True,transfer=True,affect=True,local_period=True)
        self.assertTrue(any(k=="checkpoint_exact_offer_nomination" and n for k,n in routes))
        self.assertTrue(any(k=="typed_activity_affect" and n for k,n in routes))
        print("R63_CO_CURRENT_CARRIER",routes)

    @unittest.skipUnless(os.environ.get("INFERENCE_OWNER_LANE")=="NEIGHBOR","separate NEIGHBOR checkout")
    def test_neighbor_actual_reciprocal_acquisition_pause_resume(self):
        # Use the current owner's actual full ordinary-life court, replacing
        # its actor-local routine candidates at the genuine semantic boundary
        # with the combined historical/live conditional compiler's output.
        from test_neighbor_reciprocal_routine import ReciprocalOrdinaryLife
        from um_sorok_organism.types import canonical
        old=CallbackLLMProvider.propose;routes=[]
        def bridged(provider,task,packet):
            original=old(provider,task,packet)
            if task!="development":return original
            rules=[];wanted=[]
            for c in original.get("candidates",[]):
                if c.get("kind")=="ACQUIRE_RECURRENT_ROUTINE":
                    rules.append({"offer":"historically_possible_recurrent_routines","construct":"RECURRENT_ROUTINE",
                        "match":{"basis":c["basis"]},"augment":{k:v for k,v in c.items() if k not in ("kind","basis")}})
                    wanted.append(c)
                elif c.get("kind")=="REVISE_RECURRENT_ROUTINE":
                    rules.append({"offer":"historically_possible_routine_revisions","construct":"ROUTINE_REVISION",
                        "match":{"basis":c["basis"]},"augment":{k:v for k,v in c.items() if k not in ("kind","basis")}})
                    wanted.append(c)
            if not rules:return original
            pol=policy([],rules);policy_check(pol);p=ConditionalPolicy({packet["actor"]["id"]:pol})
            compiled=p.propose(task,packet)["candidates"]
            actual=[c for c in compiled if any(canonical(c)==canonical(q) for q in wanted)]
            self.assertEqual({canonical(c) for c in wanted},{canonical(c) for c in actual})
            routes.extend(p.routes.items())
            result=deepcopy(original)
            for i,c in enumerate(result["candidates"]):
                match=next((q for q in actual if canonical(c)==canonical(q)),None)
                if match is not None:result["candidates"][i]=match
            return result
        owner=ReciprocalOrdinaryLife()
        with tempfile.TemporaryDirectory() as d,patch.object(CallbackLLMProvider,"propose",bridged):
            owner.course(Path(d)/"neighbor.db",True)
            owner.course(Path(d)/"unilateral.db",False)
        self.assertTrue(any(k=="typed_recurrent_routine" and n for k,n in routes))
        self.assertTrue(any(k=="typed_routine_revision" and n for k,n in routes))
        print("R63_NEIGHBOR_CURRENT_CARRIER",routes)

if __name__=="__main__":unittest.main()
