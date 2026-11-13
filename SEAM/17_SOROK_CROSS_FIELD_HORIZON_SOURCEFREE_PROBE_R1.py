"""One finite-domain PYAT-field + N9-power -> K -> U -> later action reference.

Everything is SOURCEFREE/HYPOTHETICAL: no measured survey, N9 source grant,
scientific transmission, CAN/P3 issuance, or protected runtime integration.
Run: python3 SEAM/17_SOROK_CROSS_FIELD_HORIZON_SOURCEFREE_PROBE_R1.py
"""
from dataclasses import dataclass, replace
import json

GRADE = "EXPLICIT_SOURCEFREE_TOY"


@dataclass(frozen=True)
class Field:
    # Hypothetical joint adult *saliences*, never a measured respondent/psyche.
    values_care: bool = True
    deference_salient: bool = True
    egalitarian_avowal: bool = True


@dataclass(frozen=True)
class World:
    # Objectively enacted rights/relations, NOT inferred from the Field.
    sanction_right: bool = True
    livelihood_dependence: bool = True
    adult_independent_project: bool = False
    institutional_care: bool = True
    institutional_breach: bool = False
    child_sees: bool = True
    breach_accessible: bool = True
    counterfield_coactor: bool = False
    child_practices: bool = False
    opposition_cost_seen: bool = False
    actor_can_sanction: bool = True
    resources: int = 2


@dataclass(frozen=True)
class Event:
    key: str
    kind: str
    happened: bool
    child_received: bool
    personally_practiced: bool = False
    consequence_received: bool = True


@dataclass(frozen=True)
class U:
    norm: int = 1
    skill: int = 1
    contradiction: int = 3
    decenter: int = 12


def k_enact(f: Field, w: World):
    """Candidate K: role, public norms, competing project, actual power.
    Not a law converting survey responses into real parents' behavior."""
    coercive = w.sanction_right and w.livelihood_dependence
    volunteered = not coercive and f.deference_salient and not w.adult_independent_project
    actual_practice = w.counterfield_coactor and w.child_practices
    events = [
        Event("care-claim", "claim", f.values_care, w.child_sees),
        Event("deference-claim", "claim", f.deference_salient, w.child_sees),
        Event("egalitarian-avowal", "claim", f.egalitarian_avowal, w.child_sees),
        Event("work-comply", "coerced", coercive, w.child_sees),
        Event("work-voluntary", "voluntary", volunteered, w.child_sees),
        Event("work-negotiate", "negotiate", not coercive and not volunteered, w.child_sees),
    ]
    for i in range(2):
        events.append(Event("care-"+str(i), "care", w.institutional_care,
                            w.child_sees, personally_practiced=True))
    # Chronology matters: the child must have actually acquired the criterion
    # from prior acts before this contrary institutional action can violate it.
    events.append(Event("breach", "harm", w.institutional_breach,
                        w.child_sees and w.breach_accessible))
    for ability in ("care", "repair"):
        events.append(Event("outside-"+ability, "skill-"+ability, actual_practice,
                            actual_practice and w.child_sees, actual_practice and w.child_sees))
    return events


@dataclass(frozen=True)
class Person:
    claims_heard: tuple = ()
    normality: int = 0
    experienced_sanction: int = 0
    practiced_care: int = 0
    contradiction: int = 0
    skills: tuple = ()
    reactive_reference: int = 0
    active_carrier_reference: int = 0
    paid_refusal_cost: int = 0


def u_learn(events, rule=U()):
    """Distinct actor-local uptake: unseen effects never mint subjective learning."""
    claims, skills = [], []
    norm = risk = care = harm = 0
    for e in events:
        if not e.happened or not e.child_received or not e.consequence_received:
            continue
        if e.kind == "claim":
            claims.append(e.key)
        elif e.kind == "care":
            norm += rule.norm
            if e.personally_practiced:
                care += rule.skill
        elif e.kind in ("coerced", "voluntary"):
            norm += rule.norm
            if e.kind == "coerced":
                risk += rule.norm
        elif e.kind == "harm" and care:
            harm += rule.contradiction
        elif e.kind.startswith("skill-") and e.personally_practiced:
            skills.append(e.kind.removeprefix("skill-"))
            care += rule.skill
    reactive = 2 * harm
    return Person(tuple(claims), norm, risk, care, harm, tuple(skills),
                  reactive, norm + reactive)


def defend_normality(p: Person, w: World, perceived_threat: bool = True):
    """A habituated *world grammar* can be activated despite universalist speech."""
    if not perceived_threat or p.normality <= p.contradiction or not p.active_carrier_reference:
        return "NO_RECRUITMENT"
    return "PERFORM_DEFENSE" if w.actor_can_sanction else "DEFENSE_WITHOUT_POWER"


def perform_refusal(p: Person, w: World):
    # A real act/cost is necessary; experienced cost is distinct from objective cost.
    if not p.contradiction or not p.reactive_reference:
        return p, "NO_REFUSAL"
    actual_cost = 2 if w.livelihood_dependence else 1
    return replace(p, paid_refusal_cost=actual_cost if w.opposition_cost_seen else 0), "REFUSAL_OCCURRED"


def possible_decenter(p: Person, rule=U()):
    # Rival U may have decenter=0. Alternatives alone are not a conversion switch.
    if not p.paid_refusal_cost or len(set(p.skills)) < 2:
        return p
    return replace(p, active_carrier_reference=max(0, p.active_carrier_reference-rule.decenter))


def later_response(p: Person, w: World, institution_sponsored: bool):
    if not w.resources:
        return "MATERIAL_HOLD"
    # The sponsor affects action only while it has active positive/negative gravity.
    symbolic_cost = p.reactive_reference if institution_sponsored and p.active_carrier_reference else 0
    return "ACCEPT_HELP" if p.practiced_care-symbolic_cost >= 1 else "DECLINE"


def later_shift_strategy(p: Person, current: World):
    """Actual prospective reader of learned risk, subject to CURRENT world gate.

    This returns a candidate actor decision, not an admitted P2 performed act.
    """
    if current.resources < 1:
        return "MATERIAL_HOLD"
    if not current.sanction_right:
        return "REQUEST_ALONE"
    if p.experienced_sanction:
        if current.counterfield_coactor and {"care", "repair"} <= set(p.skills):
            return "COORDINATE_WITH_PEERS"
        return "AVOID_UNSUPPORTED_REQUEST"
    return "REQUEST_ALONE"


def new_activity(p: Person, w: World):
    # Bounded composition of practiced capacity + independent person + time/stock.
    return ("COOPERATIVE_CARE_REPAIR" if {"care", "repair"} <= set(p.skills)
            and w.counterfield_coactor and w.resources >= 2 else None)


def run():
    checks = []
    def check(label, passed):
        assert passed, label
        checks.append(label)

    f, w = Field(), World()
    base = u_learn(k_enact(f,w))
    no_power = replace(w,sanction_right=False)
    powerless = u_learn(k_enact(f,no_power))
    check("same field, structural sanction changes performed K",
          [e.kind for e in k_enact(f,w) if e.happened] !=
          [e.kind for e in k_enact(f,no_power) if e.happened])
    check("same field, changed sanction changes experienced practical risk",
          base.experienced_sanction == 1 and powerless.experienced_sanction == 0)
    check("same field, changed sanction does not rewrite avowals",
          base.claims_heard == powerless.claims_heard)
    check("same structure, changed field changes enacted voluntary practice under K",
          any(e.kind=="negotiate" and e.happened for e in
              k_enact(replace(f,deference_salient=False),no_power)))
    check("same field, adult own project overrides K's voluntary deference",
          any(e.kind=="negotiate" and e.happened for e in
              k_enact(f,replace(no_power,adult_independent_project=True))))
    check("speech report never directly issues an act's coercive power",
          defend_normality(base,replace(w,actor_can_sanction=False)) == "DEFENSE_WITHOUT_POWER")
    check("egalitarian speech and hegemonic defense can coexist",
          "egalitarian-avowal" in base.claims_heard and defend_normality(base,w)=="PERFORM_DEFENSE")
    check("remove child access without changing world => no cognitive formation",
          u_learn(k_enact(f,replace(w,child_sees=False))).normality==0)
    check("no personal threat => no defensive recruitment",
          defend_normality(base,w,False)=="NO_RECRUITMENT")
    check("same present world, different sourcefree childhood sanctions => different later action",
          later_shift_strategy(base,w)!=later_shift_strategy(powerless,w))
    check("current world power may independently alter a feasible action",
          later_shift_strategy(base,replace(w,sanction_right=False))=="REQUEST_ALONE")
    breach = replace(w,institutional_breach=True)
    exposed = u_learn(k_enact(f,breach))
    check("accessible contradiction can expose institutional practice",
          exposed.contradiction>0)
    check("inaccessible contradiction does not update child",
          u_learn(k_enact(f,replace(breach,breach_accessible=False))).contradiction==0)
    check("visible contradiction does not automatically release institutional gravity",
          exposed.active_carrier_reference>0)
    costed, event = perform_refusal(exposed,replace(breach,opposition_cost_seen=True))
    check("actual refusal and witnessed cost are separate events",
          event=="REFUSAL_OCCURRED" and costed.paid_refusal_cost==2)
    check("cost alone without independent practices cannot produce release",
          possible_decenter(costed)==costed)
    with_coactor = replace(breach,counterfield_coactor=True,child_practices=True,opposition_cost_seen=True)
    skilled = u_learn(k_enact(f,with_coactor))
    check("counterfield-acquired skill changes later strategy without removing employer sanction",
          later_shift_strategy(skilled,with_coactor)=="COORDINATE_WITH_PEERS")
    costed_skilled, _ = perform_refusal(skilled,with_coactor)
    freed = possible_decenter(costed_skilled)
    check("actual coactor/practice + refusal cost permits a changed reference",
          freed.active_carrier_reference==0 and freed.normality>0)
    check("same history, rival U can retain reactive attachment",
          possible_decenter(costed_skilled,U(decenter=0)).active_carrier_reference>0)
    check("without child's actual participation no skill from mere counterfield",
          not u_learn(k_enact(f,replace(with_coactor,child_practices=False))).skills)
    check("sponsor ceases to determine beneficial choice when reference decentered",
          later_response(freed,with_coactor,True)==later_response(freed,with_coactor,False))
    check("sponsor still alters reactive actor's decision",
          later_response(costed_skilled,with_coactor,True)!=later_response(costed_skilled,with_coactor,False))
    check("new project needs skills, coactor and budget",
          new_activity(freed,with_coactor)=="COOPERATIVE_CARE_REPAIR")
    check("no resources => no project",new_activity(freed,replace(with_coactor,resources=0)) is None)
    check("no coactor => no project",new_activity(freed,replace(with_coactor,counterfield_coactor=False)) is None)
    check("world availability can block response without psyche mutation",
          later_response(freed,replace(with_coactor,resources=0),False)=="MATERIAL_HOLD")
    check("same events can yield legitimate zero learning under an alternative U",
          u_learn(k_enact(f,with_coactor),U(norm=0,skill=0,contradiction=0)).normality==0)
    check("cold deterministic recomputation",u_learn(k_enact(f,with_coactor))==u_learn(k_enact(f,with_coactor)))
    print(json.dumps({"grade":GRADE, "pass":len(checks), "checks":checks,
                      "native_science":False, "observed_pyat_joint_rows":0,
                      "integrated_p3_can_first_reader":False},indent=2))


if __name__ == "__main__":
    run()
