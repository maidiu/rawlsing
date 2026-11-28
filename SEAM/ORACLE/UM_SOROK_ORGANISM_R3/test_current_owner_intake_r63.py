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


    @unittest.skipUnless(os.environ.get("INFERENCE_OWNER_LANE")=="NEIGHBOR","separate NEIGHBOR checkout")
    def test_current_neighbor_one_response_actual_reciprocal_life(self):
        import sys,json
        from importlib.util import spec_from_file_location,module_from_spec
        from um_sorok_organism.types import adult,blank_world
        from neighbor_runtime import NeighborEncounter
        from live_turn_port_r38 import LiveTurnSession
        import mii
        folder=Path(__file__).parent/"um_sorok_organism"
        def module(name,path):
            spec=spec_from_file_location(name,path)
            mod=module_from_spec(spec);spec.loader.exec_module(mod);return mod
        wire=module("um_sorok_organism.r65_wire",folder/"live_psychological_llm.py")
        with patch.dict(sys.modules,{"um_sorok_organism.live_psychological_llm":wire}):
            lab=module("um_sorok_organism.r65_lab",folder/"inference_lab.py")
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);rt=ConstitutiveRuntime(str(root/"life.db"))
                aa=adult("a","A");bb=adult("b","B")
                aa["projects"]=[{"id":"a-song","object":"a particular shared practice","means":["SING"],
                                  "addressed_party_ref":"b","status":"active","priority":.7}]
                bb["projects"]=[{"id":"b-song","object":"a particular shared practice","means":["SING"],
                                  "addressed_party_ref":"a","status":"active","priority":.7}]
                rt.ledger.initialize(blank_world(),[aa,bb])
                endpoint="https://example.invalid/chat/completions"
                b=lab.LiveBudget(journal=root/"budget",max_calls=20,max_wire_bytes=20000000,
                    input_token_ceiling=100000,completion_token_limit=1000,input_nanos_per_token=1,
                    output_nanos_per_token=1,max_budget_nanos=3000000,sourcefree_live_authorized=True,
                    profiles={"reference":{"model":"fixture","endpoint":endpoint,
                        "input_token_ceiling":100000,"completion_token_limit":1000,
                        "input_nanos_per_token":1,"output_nanos_per_token":1}})
                provider=lab.CombinedAllocationProvider("LIVE",owner_head="3bafa19fda1ee7597583a649e8c3d1d0ee20ca21",
                    budget=b,reference_profile="reference",provider_options={"reference":{
                        "endpoint":endpoint,"model":"fixture","api_key":"not-a-key",
                        "allow_private_actor_data":True,"sourcefree_live_attested":True,
                        "compact_exact_packet":True}},sourcefree_allocation_authorized=True)
                phase={"op":"REST","refuse":False,"revision":None};sent=[]
                def answer(self,payload):
                    req=wire.expand_live_wire_request(json.loads(payload["messages"][1]["content"]))
                    principal=req["principal"];policies={}
                    for aid in [principal,*req["peer_tips"]]:
                        other="b" if aid=="a" else "a"
                        op=phase["op"] if aid==principal else "REFUSE" if phase["refuse"] else "SING"
                        acts=([action("SING",{"project_id":aid+"-song"}),action("SING"),action("WAIT")]
                              if op=="SING" else [action(op),action("WAIT")])
                        rules=[{"offer":"historically_possible_recurrent_routines","construct":"RECURRENT_ROUTINE",
                                "match":{"basis":{"operation":"SING","coactivity_partner":other}},
                                "augment":{"window_days":80,"hours_per_active_day":3. if aid=="a" else 2.,
                                           "provisional_exposure_fraction":1. if aid=="a" else .5}}]
                        if phase["revision"] and aid=="b":
                            rules.append({"offer":"historically_possible_routine_revisions","construct":"ROUTINE_REVISION",
                                "match":{"basis":{"operation":"SING"}},"augment":{"mode":phase["revision"],
                                    "interpretive_hypothesis":"Change my own involvement."}})
                        p=policy(acts,rules);p["expression"]={"surface":"Ordinary life."}
                        policies[aid]=p
                    sent.append(principal)
                    return {"choices":[{"message":{"content":json.dumps({"policies":policies})}}],
                            "usage":{"prompt_tokens":200,"completion_tokens":50}}
                session=LiveTurnSession(rt,provider,root/"turns.sqlite",sourcefree_attested=True)
                n=NeighborEncounter(rt,"visitor",mii_module=mii)
                def world():return rt.ledger.world()[1]
                def beat(a,op,status="PERFORMED"):
                    phase["op"]=op;out=session.owner_actor_beat(n,a)
                    self.assertEqual((out["attempt"],out["status"]),(op,status))
                    self.assertNotEqual(out["selection_grade"],"INJECTED_NOT_NATIVE_ACTOR_CHOICE")
                def interval(days):
                    start=world()["clock"];result=rt.continue_mixed_history(start+days,
                        cadence_origin=start,ordinary_span=days)
                    self.assertEqual(result["status"],"MODELED_HISTORY_CUT_REACHED")
                    return [x for x in world()["historical_periods"] if x["start"]>=start]
                try:
                    with patch.object(wire.ExplicitJSONLLMProvider,"_request",answer):
                        phase["refuse"]=True;beat("a","SING","PARTIAL");phase["refuse"]=False
                        for _ in range(3):
                            beat("a","REST");beat("b","REST");beat("a","SING")
                        sources=world()["routine_source_registry"]
                        self.assertEqual(len(sources),2)
                        x,y=sorted(sources.values(),key=lambda q:q["actor"])
                        self.assertEqual(x["basis_event_refs"],y["basis_event_refs"])
                        realized=interval(20);self.assertTrue(realized)
                        self.assertTrue(all(len(p["processes"])==2 and p["actor_time_claims"]=={"a":1.,"b":1.}
                                            for p in realized))
                        original=deepcopy(world()["historical_periods"])
                        phase["revision"]="PAUSE";beat("b","REST");phase["revision"]=None
                        held=interval(5);self.assertTrue(held)
                        self.assertTrue(all(not p["processes"] for p in held))
                        self.assertEqual(world()["historical_periods"][:len(original)],original)
                        phase["revision"]="RESUME";beat("b","REST");phase["revision"]=None
                        resumed=interval(5);self.assertTrue(resumed)
                        self.assertTrue(all(len(p["processes"])==2 for p in resumed))
                    receipts=session.custody.receipts()
                    self.assertEqual(len(receipts),12)
                    self.assertEqual(len(sent),12)
                    self.assertEqual(b.calls,12)
                    report=lab.reconcile_budget_owner_receipts(b,live_receipts=receipts)
                    self.assertEqual(report["profiles"]["reference"]["owner_operations_returned"],12)
                    self.assertEqual(report["profiles"]["reference"]["known_rate_estimate_nanos"],3000)
                    routes={}
                    for receipt in receipts:
                        for k,v in receipt.get("conditional_routes",{}).items():routes[k]=routes.get(k,0)+v
                    self.assertEqual(routes.get("typed_recurrent_routine"),2)
                    self.assertEqual(routes.get("typed_routine_revision"),2)
                    self.assertTrue(rt.verify()["valid"])
                    print("R65_ONE_RESPONSE_CURRENT_NEIGHBOR",json.dumps({"calls":len(sent),
                        "local_tasks":sum(sum(q["local_semantic_tasks"].values()) for q in receipts),
                        "routes":routes,"profile":report["profiles"]["reference"],
                        "realized":len(realized),"withdrawn":len(held),"resumed":len(resumed)},sort_keys=True))
                finally:session.close();rt.close()


if __name__=="__main__":unittest.main()
