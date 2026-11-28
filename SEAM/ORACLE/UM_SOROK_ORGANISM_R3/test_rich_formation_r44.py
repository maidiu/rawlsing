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


    def test_actual_family_then_wage_dependence_and_reconstitution(self):
        # Existing family owner and same actual ledger, not prepared parents or
        # a second newborn. Explicit route/contract and suspension research
        # premises are actual native acts, separately graded as injections.
        import test_joined_generation_r33 as joined
        from modern_generation_port_r28 import link_actual_live_interval
        for nominate in (True,False):
            with self.subTest(nominate=nominate),tempfile.TemporaryDirectory() as d:
                root=Path(d);db=root/"life.sqlite";rt,sid,catalog,constructors=joined.JoinedGenerationCourt.setup(self,db)
                args={"family_sources":(sid,),"period_catalog":catalog,"qualified_interval_cuts":True}
                first=root/"first";first.mkdir()
                p=joined.LifeCheckpoint(sid)
                g=inherited.ModernGenerationCourt.generation(self,rt,first,"mother",p,**args)
                try:
                    g.bootstrap();g.advance();g.finish();handoff=g.terminal_handoff()
                    prefix=rt.ledger.events();self.assertEqual(constructors,["mother","father"])
                    self.assertTrue(rt.snapshot("nadia")["co_regulation_orientations"])
                finally:g.close()
                # No movement or institutional terms automatically inferred
                # from the parents' psyche. These exact external research
                # premises are not evidence of autonomous route selection.
                try:
                    spec=rt.register_sourcefree_work_regime({"grade":"EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO",
                        "source_ref":"R46_fictional_work_regime","site":"workshop","controller":"workshop_steward",
                        "eligible_workers":["mother","father"],"delegates":["father"]})
                    for aid in ("mother","father"):
                        self.assertEqual(rt.step(aid,requested_action="MOVE",object_ref="workshop")["status"],"PERFORMED")
                        rt.step(aid,requested_action="INSPECT",object_ref=spec["terms_notice_ref"])
                        self.assertEqual(rt.step(aid,requested_action="ACCEPT_WORK_TERMS")["status"],"PERFORMED")
                    link=link_actual_live_interval(rt,handoff,first/"cycle.json")
                finally:rt.close()
                second=root/"work";second.mkdir()
                def m(op,rules=()):return own("mother",[action(op)],rules)
                work=m("WORK",[rich("recurrent_livelihood_orientation","RECURRENT_WORK_ORIENTATION",
                                   orientation_mode="APPROACH")])
                rest=m("REST")
                p2=Course([[rest,rest,work,rest,rest],[work,rest,rest,work,rest]])
                rt=ConstitutiveRuntime(str(db));g=inherited.ModernGenerationCourt.generation(self,rt,second,"mother",p2,
                                continuity_link=link,**args)
                try:
                    a=g.bootstrap();b=g.advance()
                    self.assertEqual([x["objective"]["attempt"] for x in a["records"]+b["records"]].count("WORK"),3)
                    self.assertTrue(all(x["objective"]["status"]=="PERFORMED" for x in a["records"]+b["records"]))
                    old=deepcopy(rt.snapshot("mother")["historical_orientations"][0])
                    self.assertEqual(old["orientation_mode"],"APPROACH")
                    g.finish();handoff=g.terminal_handoff()
                finally:g.close();rt.close()
                # Stipulate the historically actual institutional conflict;
                # never attribute the research's imposed actions to a model.
                rt=ConstitutiveRuntime(str(db))
                try:
                    for aid,op,target in [("mother","REST",None),("mother","REST",None),
                            ("father","REST",None),("father","WORK",None),
                            ("father","CONTRIBUTE_WAGE_RELIEF",None),("father","SUSPEND_WAGE_WORK","mother")]:
                        self.assertEqual(rt.step(aid,requested_action=op,target=target)["status"],"PERFORMED")
                    self.assertEqual(rt.step("mother",requested_action="WORK")["status"],"BLOCKED")
                    link2=link_actual_live_interval(rt,handoff,second/"cycle.json")
                    before=rt.ledger.world()[1]["accounts"]["mother"]
                finally:rt.close()
                third=root/"relief";third.mkdir()
                later={"action":"WORK","current_match":{"action":"WORK","kind":"HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE"}}
                p3=Course([[m("DRAW_WAGE_RELIEF",[offer("relief_reconstitution")] if nominate else []),rest,rest,rest,rest],
                            [rest,own("mother",[later,action("WAIT")]),rest]])
                rt=ConstitutiveRuntime(str(db));g=inherited.ModernGenerationCourt.generation(self,rt,third,"mother",p3,
                                continuity_link=link2,**args)
                try:
                    r=g.bootstrap();self.assertEqual(r["records"][0]["objective"]["attempt"],"DRAW_WAGE_RELIEF")
                    self.assertEqual(r["records"][0]["objective"]["status"],"PERFORMED")
                    self.assertEqual(rt.ledger.world()[1]["accounts"]["mother"],before+.25)
                    new=rt.snapshot("mother")["historical_orientations"][0]
                    self.assertEqual({k:v for k,v in old.items() if k!="revisions"},{k:v for k,v in new.items() if k!="revisions"})
                    self.assertEqual(len(new["revisions"]),int(nominate))
                finally:g.close();rt.close()
                rt=ConstitutiveRuntime(str(db));g=inherited.ModernGenerationCourt.generation(self,rt,third,"mother",p3,
                                continuity_link=link2,**args)
                try:
                    r=g.advance();self.assertEqual(r["records"][1]["objective"]["attempt"],"WAIT" if nominate else "WORK")
                    g.finish();handoff=g.terminal_handoff()
                    self.assertEqual(rt.ledger.events()[:len(prefix)],prefix)
                    self.assertEqual(rt.ledger.world()[1]["work_regimes"]["workshop"]["contracts"]["mother"]["status"],"ACTIVE")
                    self.assertEqual(constructors,["mother","father"])
                finally:g.close()
                try:
                    # Return is a distinct sourcefree research route, not
                    # generated initiative. Resume actual family life again.
                    for aid in ("mother","father"):rt.step(aid,requested_action="MOVE",object_ref="home")
                    link3=link_actual_live_interval(rt,handoff,third/"cycle.json")
                    tail=root/"later";tail.mkdir()
                    p4=joined.LifeCheckpoint(sid,resumed=True)
                    g=inherited.ModernGenerationCourt.generation(self,rt,tail,"mother",p4,continuity_link=link3,**args)
                    try:
                        g.bootstrap();g.finish()
                        self.assertEqual(rt.snapshot("nadia")["age_days"],70)
                        self.assertEqual(rt.ledger.events()[:len(prefix)],prefix)
                        self.assertTrue(rt.verify()["valid"]);self.assertTrue(g.engine.verify())
                        print("R46_FAMILY_LIVELIHOOD",json.dumps({"nominate":nominate,"later":r["records"][1]["objective"]["attempt"],
                            "child_age_days":70,"native_events":len(rt.ledger.events()),"checkpoint_calls":
                            sum(len(x.requests) for x in (p,p2,p3,p4)),"constructors":len(constructors)},sort_keys=True))
                    finally:g.close()
                finally:rt.close()


    def test_exact_granular_retrieval_and_bounded_working_set_over_continuing_history(self):
        from modern_generation_port_r28 import RecursionRefusal
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);db=f/"life.sqlite";rt=ConstitutiveRuntime(str(db))
            rt.ledger.initialize(blank_world(),[adult("worker","Mara")])
            class MemoryCourse:
                def __init__(self):self.requests=[]
                def call(self,r):
                    self.requests.append(r);ctx=r["context"];n=len(self.requests)
                    if r["mode"]=="TERMINAL":return term(r)
                    rows=[]
                    for i in range(5):
                        rule={"candidate":{"kind":"MEMORY","content":f"Actual ordinary rest {n}:{i}: "+("the afternoon passed. "*12),
                                           "cue_terms":["rest"]},"when":{"own_action":"REST","status":"PERFORMED"}}
                        rows.append(own("worker",[action("REST")],[rule]))
                    result=batch(r,rows,n)
                    if n==4:
                        result["prospective"][-1]["circumstances"]["next_analytic_reads"]=[
                            {"kind":"ACTOR_DOMAIN_PAGE","actor":"worker","domain":"memories","offset":0,"limit":3}]
                    if n==5:
                        page=ctx["selected_exact_analytic_reads"][0]["value"]
                        result["prospective"][-1]["circumstances"]["next_analytic_reads"]=[
                            {"kind":"ACTOR_ROW","actor":"worker","domain":"memories","row_ref":page["rows"][0]["row_ref"]}]
                    return result
            p=MemoryCourse()
            g=inherited.ModernGenerationCourt.generation(self,rt,f,"worker",p,selective_memory_context=True)
            try:
                g.bootstrap()
                for _ in range(4):g.advance()
                old=deepcopy(rt.snapshot("worker")["memories"])
                self.assertEqual(len(old),25)
            finally:g.close();rt.close()
            rt=ConstitutiveRuntime(str(db));g=inherited.ModernGenerationCourt.generation(self,rt,f,"worker",p,selective_memory_context=True)
            try:
                page=p.requests[4]["context"]["selected_exact_analytic_reads"][0]["value"]
                self.assertEqual(page["count"],20);self.assertEqual(len(page["rows"]),3)
                g.advance()
                c=p.requests[5]["context"]
                got=c["selected_exact_analytic_reads"][0]
                self.assertEqual(got["value"],old[0])
                self.assertEqual(got["value_digest"],page["rows"][0]["row_digest"])
                projection=c["actor_contexts"]["worker"]["accessible_memory_projection"]
                self.assertEqual(projection["full_accessible_count"],25)
                self.assertLess(projection["included_count"],25)
                current=rt.snapshot("worker")["memories"]
                self.assertEqual(current[:25],old)
                full=g.owner.resolve_analytic_reads([{"kind":"ACTOR_DOMAIN","actor":"worker","domain":"memories"}])
                row=g.owner.resolve_analytic_reads([{"kind":"ACTOR_ROW","actor":"worker","domain":"memories",
                    "row_ref":page["rows"][0]["row_ref"]}])
                nfull=len(json.dumps(full,separators=(",",":"),sort_keys=True).encode())
                nrow=len(json.dumps(row,separators=(",",":"),sort_keys=True).encode())
                self.assertLess(nrow,nfull/3)
                with self.assertRaises(RecursionRefusal):
                    g.owner.resolve_analytic_reads([{"kind":"ACTOR_ROW","actor":"worker","domain":"memories",
                        "row_ref":"id:unissued"}])
                g.advance();g.finish();self.assertTrue(rt.verify()["valid"]);self.assertTrue(g.engine.verify())
                print("R47_GRANULAR",json.dumps({"memories":len(current),"checkpoint_calls":len(p.requests),
                    "full_accessible_count":projection["full_accessible_count"],"working_count":projection["included_count"],
                    "full_domain_bytes":nfull,"single_row_bytes":nrow},sort_keys=True))
            finally:g.close();rt.close()

if __name__=="__main__":unittest.main()
