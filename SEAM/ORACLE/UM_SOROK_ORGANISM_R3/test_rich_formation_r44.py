"""R44: actual richer historical genesis through the shared semantic compiler.
Same conditional later policies, changed historical nominations, native owners.
Explicit research setup acts stay distinct from independently selected surfaces.
"""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from modern_generation_port_r28 import ModernDevelopmentOwner,ModernGeneration
from test_modern_generation_port_r28 import action,policy,event,retro
import test_modern_generation_port_r28 as inherited

def rich(offer,construct,**augment):
    return {"offer":"historically_possible_"+offer,"construct":construct,"augment":augment}
def offer(name,**match):
    return {"offer":"historically_possible_"+name,"match":match}
def batch(r,rows,n):
    ctx=r["context"];t=ctx["clock"]
    return {"retrospective":retro(r),"prospective":[event(ctx,f"{n}:{i}",t+i+1,aid,pol)
                for i,(aid,pol) in enumerate(rows)]}
def own(a,actions,formation=()):
    return a,{a:policy(actions,formation)}
def term(r):
    return {"retrospective":retro(r),"prospective":None}

class Course:
    def __init__(self,phases):self.phases=phases;self.requests=[]
    def call(self,r):
        self.requests.append(r)
        if r["mode"]=="TERMINAL":return term(r)
        n=len(self.requests)-1
        return batch(r,self.phases[n],n)

class RichFormationCourt(unittest.TestCase):
    def g(self,rt,folder,p,actor):
        return inherited.ModernGenerationCourt.generation(self,rt,folder,actor,p)
    def test_affect_of_own_expression_becomes_operative_without_public_private_collapse(self):
        for nominate in (True,False):
            with self.subTest(nominate=nominate),tempfile.TemporaryDirectory() as d:
                f=Path(d);db=f/"life.sqlite";rt=ConstitutiveRuntime(str(db))
                a=adult("worker","Mara")
                a["projects"]=[{"id":"duty","object":"sustain availability","means":["REST","SPEAK"],
                    "status":"active","priority":.5,"expected_difference":{"feature":"availability",
                    "direction":"PRESERVE","sign_tags":["wait"]}}]
                rt.ledger.initialize(blank_world(),[a,adult("hearer","Hearer"),adult("blocked","Blocked")])
                rt.register_sourcefree_recursive_encounter_paths({"grade":"SOURCEFREE_TEST_ONLY",
                    "source_ref":"R44_sound","paths":[{"observer":aid,"source_actor":"worker","location":"home",
                    "from_clock":0,"through_clock":30,"hearing":audible,"sound_path":"audible" if audible else "blocked",
                    "visual":True,"light":"lit","sightline":"unobstructed","facing":"away"}
                    for aid,audible in [("hearer",True),("blocked",False)]]})
                def q(actions,rules=()):return own("worker",actions,rules)
                wait=q([action("WAIT")])
                speak=action("SPEAK",{"project_id":"duty"})
                halting=rich("expressive_practices","EXPRESSIVE_PRACTICE",cadence="HALTING")
                affect=rich("activity_affects","ACTIVITY_AFFECT",affect_name="private unease",
                     personal_sense="quiet conflicts with duty",course_orientation="APPROACH")
                second=rich("self_expression_affects","ACTIVITY_AFFECT",affect_name="unease about my own speech",
                     personal_sense="my effort to speak can itself become uncomfortable",course_orientation="WITHHOLD")
                later=deepcopy(speak);later["exclude_affect"]={"course_orientation":"WITHHOLD",
                    "basis":{"formation_source":"OWN_PERFORMED_EXPRESSION"}}
                p=Course([[q([{"action":"REST","project_id":"duty"}]),
                    q([action("WAIT")],[rich("delayed_appraisals","DELAYED_APPRAISAL",appraisal="ACTOR_INTERPRETS_DISAPPOINTED")]),
                    q([action("WAIT")],[affect])],
                    [wait,q([speak],[halting]),wait,q([speak],[halting])],
                    [wait,q([speak],[second] if nominate else []),wait],
                    [q([later,action("WAIT")]),wait,wait]])
                g=self.g(rt,f,p,"worker")
                try:
                    g.bootstrap();g.advance();r=g.advance()
                    old=deepcopy(rt.snapshot("worker")["expectations"][0]["affective_organizations"])
                    self.assertEqual(len(old),1+int(nominate))
                    self.assertEqual(old[0]["expressive_practice"]["cadence"],"HALTING")
                    if nominate:self.assertEqual(old[1]["depth"],2)
                    self.assertNotIn("blocked",r["records"][1]["accessible"]["by_actor"])
                    self.assertNotIn("unease about my own speech",json.dumps(r["records"][1]["objective"]))
                finally:g.close();rt.close()
                rt=ConstitutiveRuntime(str(db));g=self.g(rt,f,p,"worker")
                try:
                    r=g.advance();self.assertEqual(r["records"][0]["objective"]["attempt"],"WAIT" if nominate else "SPEAK")
                    self.assertEqual(rt.snapshot("worker")["expectations"][0]["affective_organizations"],old)
                    g.finish();self.assertEqual(len(p.requests),5)
                    self.assertTrue(rt.verify()["valid"]);self.assertTrue(g.engine.verify())
                    print("R44_AFFECT",json.dumps({"nominate":nominate,"later":r["records"][0]["objective"]["attempt"],
                        "organizations":len(old),"checkpoint_calls":len(p.requests)},sort_keys=True))
                finally:g.close();rt.close()
    def test_care_practice_suspension_after_actual_counterpart_imposition(self):
        for nominate in (True,False):
            with self.subTest(nominate=nominate),tempfile.TemporaryDirectory() as d:
                f=Path(d);db=f/"life.sqlite";rt=ConstitutiveRuntime(str(db))
                a=adult("giver","Giver");a["projects"]=[{"id":"care","object":"care for other","means":["CARE"],
                    "addressed_party_ref":"other","status":"active","priority":.6}]
                others=[adult("other","Other"),adult("third","Third")]
                # A particular independent practical project is required:
                # never make the imposition an automatic reaction to care.
                for other in others:
                    other["projects"]=[{"id":"impose:"+other["id"],"object":"obtain compliance",
                        "means":["IMPOSE"],"addressed_party_ref":"giver","status":"active","priority":.6}]
                rt.ledger.initialize(blank_world(),[a,*others])
                care=action("CARE",{"world_request":{"addressed_party_ref":"other"}})
                specific=action("CARE",{"world_request":{"addressed_party_ref":"other"},
                                      "grounds_status":"HISTORICALLY_PRACTICED_PARTICULAR_CARE"})
                rev={"offer":"historically_possible_care_practice_revisions",
                      "augment":{"interpretive_hypothesis":"I need not keep doing this for this person."}}
                # Both actual counterpart and unrelated Other act with the same
                # conditional selection; only counterpart history qualifies.
                def impose(aid):
                    return aid,{aid:policy([action("IMPOSE",{"world_request":{"addressed_party_ref":"giver"}}),
                                           action("WAIT")]),"giver":policy([action("REFUSE")],[rev] if nominate else [])}
                p=Course([[own("giver",[care],[offer("care_practices")]),own("giver",[action("REST")]),
                           own("giver",[care],[offer("care_practices")]),own("giver",[action("REST")])],
                          [impose("third"),impose("other"),own("giver",[action("REST")])],
                          [own("giver",[specific,action("WAIT")]),own("giver",[action("REST")]),own("giver",[action("WAIT")])]])
                g=self.g(rt,f,p,"giver")
                try:
                    g.bootstrap();old=deepcopy(rt.snapshot("giver")["care_practical_commitments"][0])
                    r=g.advance()
                    self.assertEqual([x["objective"]["attempt"] for x in r["records"][:2]],["IMPOSE","IMPOSE"])
                    self.assertEqual(r["records"][0]["consequences"]["conditional_routes"].get("checkpoint_exact_offer_nomination",0),0)
                    new=rt.snapshot("giver")["care_practical_commitments"][0]
                    self.assertEqual({k:v for k,v in new.items() if k!="revisions"},old)
                    self.assertEqual(len(new.get("revisions",[])),int(nominate))
                finally:g.close();rt.close()
                rt=ConstitutiveRuntime(str(db));g=self.g(rt,f,p,"giver")
                try:
                    r=g.advance();self.assertEqual(r["records"][0]["objective"]["attempt"],"WAIT" if nominate else "CARE")
                    self.assertEqual(rt.snapshot("giver")["projects"][0]["id"],"care")
                    g.finish();self.assertTrue(rt.verify()["valid"]);self.assertTrue(g.engine.verify())
                    print("R44_CARE",json.dumps({"nominate":nominate,"later":r["records"][0]["objective"]["attempt"],
                         "checkpoint_calls":len(p.requests)},sort_keys=True))
                finally:g.close();rt.close()

if __name__=="__main__":unittest.main()
