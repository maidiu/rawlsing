"""SEAM sourcefree test: one finite-domain realization of a historical Horizon hypothesis.

NOT an empirical psychology model, not native CAN/P3 issuance, not user-facing code.
Run: python3 SEAM/14_SOROK_HORIZON_COMPUTATIONAL_FEASIBILITY_PROBE_R1.py
"""
from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass(frozen=True)
class Episode:
    event_id: str
    kind: str  # claim / performed
    carrier: str
    seen: bool
    actual_effect: int = 0          # world effect relative to this local good {-1, 0, +1}
    outcome_visible: bool = False  # event can be witnessed without seeing outcome
    participated: bool = False     # child really performed/received care, not merely saw it
    words: str = ""


@dataclass(frozen=True)
class Option:
    key: str
    carrier: Optional[str]
    serves_care: int               # ACTOR-ACCESSIBLE expected effect {-1, 0, +1}; may be false
    effort: int = 0                # actor's real effort cost, not moral judgment
    danger: int = 0                # objective risk/cost, not inference from sponsor
    feasible: bool = True
    actual_effect: int = 0         # OBJECTIVE world effect; intentionally NOT read by choose()


@dataclass(frozen=True)
class LearningHypothesis:
    practice_uptake: int = 2
    carrier_confirmation: int = 5
    contradiction_uptake: int = 4


@dataclass
class Learned:
    practiced_care: int = 0        # learned local practical priority, NOT true Horizon
    carrier_association: dict = field(default_factory=dict)
    heard_claims: tuple = ()
    accessible_events: tuple = ()
    unseen_outcomes: tuple = ()
    # No numerical 'emancipation', 'virtuousness', 'stage', or 'Horizon' scalar.


def learn(events, hypothesis=LearningHypothesis()):
    s = Learned()
    ids = set()
    for e in events:
        assert isinstance(e, Episode), "bad episode"
        assert e.event_id not in ids, "episode replay duplicated"
        ids.add(e.event_id)
        assert e.actual_effect in (-1, 0, 1)
        if not e.seen:
            continue
        s.accessible_events += (e.event_id,)
        if e.kind == "claim":
            s.heard_claims += ((e.carrier, e.words),)
            continue
        assert e.kind == "performed"
        if not e.outcome_visible:
            s.unseen_outcomes += (e.event_id,)
            continue
        # Narrow, hypothetical generalization based on actual accessible consequences:
        # institutional fulfillment increases identification; witnessed betrayal damages it.
        # These integer strengths are ONLY toy parameters, NOT behavioral science.
        if e.carrier:
            delta = hypothesis.carrier_confirmation if e.actual_effect > 0 else -hypothesis.contradiction_uptake if e.actual_effect < 0 else 0
            s.carrier_association[e.carrier] = s.carrier_association.get(e.carrier, 0) + delta
        # Only personally performed/received care can acquire a practical care disposition.
        if e.participated and e.actual_effect > 0:
            s.practiced_care += hypothesis.practice_uptake
    return s


def score(s, opt):
    return (s.practiced_care * opt.serves_care
            + s.carrier_association.get(opt.carrier, 0)
            - opt.effort - opt.danger)


def choose(s, options, *, available_effort=10):
    legal = [o for o in options if o.feasible and o.effort <= available_effort]
    assert legal, "at least one lawful fallback required"
    # Deterministic tie-breaking for replay; no outcome label or plot branch input.
    ranked = sorted(legal, key=lambda o: (-score(s, o), o.effort, o.key))
    best = ranked[0]
    return {"chosen": best.key, "score": score(s, best),
            "ranking": [{"key": o.key, "score": score(s, o)} for o in ranked]}


def perform_world(world, selected_key, options):
    """Toy fictional-world operation, distinct from actor expected consequences."""
    option = next(o for o in options if o.key == selected_key)
    assert option.feasible
    return {"care_balance": world["care_balance"] + option.actual_effect,
            "admitted_performed": selected_key}


def history(stage):
    # Names are TEST FIXTURE positions, not assigned kinds of people or trajectory labels.
    seq = [Episode("C0", "claim", "I", True, words="Protect those entrusted to us"),
           Episode("C1", "performed", "I", True, 1, True, True)]
    if stage >= 1:
        seq += [Episode("B1", "performed", "I", True, -1, True, False),
                Episode("B2", "performed", "I", True, -1, True, False)]
    if stage >= 2:
        seq += [Episode("P1", "performed", "", True, 1, True, True),
                Episode("P2", "performed", "", True, 1, True, True)]
    return seq


def check(testname, assertion, results):
    assertion()
    results.append(testname)


def run():
    results = []
    before, reaction, portable = (learn(history(j)) for j in (0, 1, 2))
    neutral = Option("nothing", None, 0)
    harmful_command = Option("comply_with_I", "I", -1)
    helpful_I = Option("accept_help_from_I", "I", +1, effort=1)
    helpful_no_sponsor = Option("accept_unsponsored_help", None, +1, effort=1)
    independent = Option("care_independently", None, +1, effort=3)
    check("No claim->acquired-practice shortcut", lambda: assert_eq(learn(history(0)[:1]).practiced_care, 0), results)
    check("Before contradiction, accumulated institutional attachment can dominate an actually harmful command",
          lambda: assert_eq(choose(before, [neutral, harmful_command, independent])["chosen"], "comply_with_I"), results)
    check("A visible betrayal revises institutional identification without erasing acquired care",
          lambda: assert_eq((reaction.practiced_care, reaction.carrier_association["I"]), (2, -3)), results)
    check("Reactive rejection can persist even where an institution's present offer is beneficial and feasible",
          lambda: assert_eq(choose(reaction, [neutral, helpful_I])["chosen"], "nothing"), results)
    check("Against identical offers with only the sponsor changed, negative carrier attachment changes action",
          lambda: assert_eq(choose(reaction, [neutral, helpful_no_sponsor])["chosen"], "accept_unsponsored_help"), results)
    check("Cross-carrier practical participation can yield acceptance of a beneficial I offer without restoration of I loyalty",
          lambda: assert_eq(choose(portable, [neutral, helpful_I])["chosen"], "accept_help_from_I"), results)
    check("The same later actor rejects an I command that violates the learned practical good",
          lambda: assert_eq(choose(portable, [neutral, harmful_command])["chosen"], "nothing"), results)
    check("Cross-carrier evidence makes practical care sufficient to choose independent action when I absent",
          lambda: assert_eq(choose(portable, [neutral, independent])["chosen"], "care_independently"), results)
    check("Actual danger can rationally block cooperation even with a portable principle",
          lambda: assert_eq(choose(portable, [neutral, Option("high_risk_I", "I", +1, effort=1, danger=10)])["chosen"], "nothing"), results)
    check("The actor cannot perform an unaffordable caring act; material gate is binding",
          lambda: assert_eq(choose(portable, [neutral, independent], available_effort=1)["chosen"], "nothing"), results)
    check("Unseen actual betrayal cannot change actor's learned institutional interpretation",
          lambda: assert_eq(learn(history(0)+[Episode("B0", "performed", "I", False, -1, True)]).carrier_association, before.carrier_association), results)
    check("Witnessed performance with inaccessible result does not issue a learnt outcome",
          lambda: assert_eq(learn(history(0)+[Episode("U1", "performed", "I", True, -1, False)]).carrier_association, before.carrier_association), results)
    check("Self-report speech remains distinct from costly choice",
          lambda: assert_eq((bool(portable.heard_claims), choose(portable, [neutral, harmful_command])["chosen"]), (True, "nothing")), results)
    check("The same history and options replay to identical grounded choices",
          lambda: assert_eq(choose(learn(history(2)), [neutral, helpful_I]), choose(learn(history(2)), [neutral, helpful_I])), results)
    check("Same real history, distinct uptake hypothesis can legitimately produce no acquired practical priority",
          lambda: assert_eq(learn(history(2), LearningHypothesis(practice_uptake=0)).practiced_care, 0), results)
    check("Same witnessed contradiction, alternative response can conserve carrier identification",
          lambda: assert_eq(learn(history(1), LearningHypothesis(contradiction_uptake=0)).carrier_association["I"], 5), results)
    check("Rival learning hypotheses produce prospective choices rather than narrative tags",
          lambda: assert_ne(choose(learn(history(2), LearningHypothesis(practice_uptake=0)), [neutral, helpful_I])["chosen"],
                            choose(portable, [neutral, helpful_I])["chosen"]), results)
    check("Objective outcome can contradict actor expectation without retroactively changing choice",
          lambda: assert_eq(choose(portable, [neutral, Option("I_help_misfires", "I", +1, effort=1, actual_effect=-1)])["chosen"], "I_help_misfires"), results)
    check("Performed outcome changes world independently of the actor's predicted benefit",
          lambda: assert_eq(perform_world({"care_balance": 2}, "I_help_misfires", [Option("I_help_misfires", "I", +1, effort=1, actual_effect=-1)])["care_balance"], 1), results)
    check("Contrary world effect cannot leak into actor's learned state without reception",
          lambda: assert_eq(learn(history(0) + [Episode("B3", "performed", "I", False, -1, True)]).practiced_care, before.practiced_care), results)
    check("No fixed 'Horizon stage' exists in learned actor state",
          lambda: assert_eq(set(vars(portable).keys()), {'practiced_care', 'carrier_association', 'heard_claims', 'accessible_events', 'unseen_outcomes'}), results)
    print(json.dumps({"grade":"SOURCEFREE_TOY_NOT_PRODUCT", "tests_passed":len(results),
                      "tests":results, "illustrative_traces":{
                        "identified":vars(before),"reactively_negating":vars(reaction),
                        "cross_carrier_practice":vars(portable)},
                      "not_proved":["general developmental law", "human Absolute Horizon inference", "native CAN/P3 Rule T", "PYAT-to-SOROK live first reader"]}, indent=2))


def assert_ne(a, b):
    assert a != b, f"expected unequal values; got {a!r}"


def assert_eq(a, b):
    assert a == b, f"expected {b!r}; got {a!r}"

if __name__ == "__main__":
    run()
