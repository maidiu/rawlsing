"""A sourcefree two-parent rehearsal. The learner reads only heard speech.

python3 shared_practice.py OWNER_TREE 2010_stata.zip
"""
import argparse
from collections import Counter, defaultdict
from datetime import timedelta
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from child_evidence import PIN
from parent_week import START, REFERENCE, observe_hours, propose
from reference_target import run as draw_targets

ADULTS = {"Mara": "fictional-workshop-parent-M", "Sam": "fictional-workshop-parent-S"}
PLAYER = "learner determines who plays"
STEWARD = "leader keeps a common rotation"
YES = "Yes. You can choose the next player."
NO = "I will call the turns."
INVITES = ("Ready to start?", "Shall we begin?")
KIN = "be present for the dependent who waits at home"


def select_means(end, options):
    """The opening endorses only alternatives anticipated to preserve this good."""
    return [act for act, expected in options.items() if end in expected]


def use_free_time(opening, *, community_cover=None):
    # In this constructed biography the paid shift gives access to this group
    # of apprentices. A different group would not keep a promise to these ones.
    options = {"PAID_WORK": {PLAYER, STEWARD}, "CARE_DEPENDENT": {KIN}}
    if community_cover is None:
        community_cover = opening["expects_off_shift_access"]
    if community_cover:
        # The same apprentices are now reachable outside the paid position.
        options["CARE_DEPENDENT"].update((PLAYER, STEWARD))
    # Precedence is local to a conflict between the two commitments. Where
    # both preserve the first, the other commitment can become decisive.
    possible = list(options)
    for claim in (opening["first_claim"], opening["other_claim"]):
        preserving = select_means(claim, {key: options[key] for key in possible})
        if preserving:
            possible = preserving
    return possible


def financial_hypothetical(opening, *, community_cover=None):
    # Target-blind reader with a specific interpretation of 'work' as paid work.
    choices = use_free_time(opening, community_cover=community_cover)
    if len(choices) == 1:
        return {"PAID_WORK": 1, "CARE_DEPENDENT": 2}[choices[0]]
    return None


def compatible_openings(practice_good, report):
    # Compressed fictional antecedents. A room without the same pupils, or
    # pupils without a room, does not supply an alternative to the paid shift.
    proposals = [
        (practice_good, KIN, True, False),  # had the key, pupils could only attend on shift
        (practice_good, KIN, True, True),   # also arranged an off-shift return
        (KIN, practice_good, True, False),  # kin took precedence even without cover
    ]
    candidates = []
    for first, other, had_room, pupils_arranged_return in proposals:
        opening = {"practice_good": practice_good, "first_claim": first, "other_claim": other,
                   "expects_off_shift_access": had_room and pupils_arranged_return}
        if financial_hypothetical(opening) == report:
            candidates.append(opening)
    if not candidates:
        raise ValueError("No proposed opening can give the reference response")
    return candidates


class HeardReplies:
    """Research projection for one already speaking child, separate from P3."""
    def __init__(self, actor):
        self.actor = actor
        self.seen = set()
        self.counts = {model: defaultdict(Counter) for model in ("pooled", "speaker", "wording")}
        self.likelihood = {model: Fraction(1) for model in self.counts}

    def observe(self, invite, reply):
        if any(row["child_actor_id"] != self.actor for row in (invite, reply)):
            raise ValueError("Wrong recipient")
        if invite["speaker_alias"] != reply["speaker_alias"]:
            raise ValueError("Reply from a different speaker")
        outcome = reply["public_text"]
        if outcome not in (YES, NO) or reply["event_id"] in self.seen:
            return
        self.seen.add(reply["event_id"])
        for model, counts in self.counts.items():
            key = self.key(model, invite["speaker_alias"], invite["public_text"])
            n = counts[key]
            accepted = outcome == YES
            self.likelihood[model] *= Fraction(1 + n[accepted], 2 + n.total())
            n[accepted] += 1

    def forecasts(self, offers):
        # Equal model odds, a uniform beta prior per group, pooled first on ties.
        best = max(self.likelihood, key=self.likelihood.get)
        scores = []
        for offer in offers:
            if offer["child_actor_id"] != self.actor:
                raise ValueError("Wrong recipient")
            key = self.key(best, offer["speaker_alias"], offer["public_text"])
            n = self.counts[best].get(key, Counter())
            scores.append(Fraction(1 + n[True], 2 + n.total()))
        choice = max(range(len(offers)), key=scores.__getitem__)
        return offers[choice]["speaker_alias"], best, [str(s) for s in scores]

    @staticmethod
    def key(model, speaker, phrase):
        return {"pooled": None, "speaker": speaker, "wording": phrase}[model]


def hear_request(session, addressed):
    from developmental_recursion.supporting_actor import record_supporting_participation, read_actor_access

    # Same speech writer as the actor-side "speak" branch of P6 reconsider().
    utterance = session.product.say(f"{addressed}, may I choose the next player?", actor="A")
    assert utterance["admitted"]
    event = session.event(utterance["event_id"])
    assert event["clock"] == session.clock() and event["actor_id"] == "A"
    witnesses = list(ADULTS.values())
    record_supporting_participation(session, event=event, participants=witnesses)
    result = {}
    for alias, actor in ADULTS.items():
        access = read_actor_access(session, actor, event["event_id"])
        assert access["status"] == "PERCEIVED"
        result[alias] = access["event"]["body_public"]["text"]
    return result


def say(session, alias, words, turn):
    from developmental_recursion.parent_speech import perform_parent_utterance, read_child_experience

    actor = ADULTS[alias]
    receipt = perform_parent_utterance(session, actor, decision_id="rehearsal",
                                       text=words, operation_id=turn, hidden_reason={})
    result = read_child_experience(session, session.read_root()["actor_ids"][0],
                                   event_id=receipt["event_id"])
    assert result["status"] == "PERCEIVED"
    return result["response_input"]


def private_opening(session, actor):
    from developmental_recursion.supporting_actor import read_supporting_actor

    return read_supporting_actor(session, actor, as_actor=actor)["private_state"]


def proposed_holder(session, alias, heard):
    # Only an addressed request recruits the learner-directed offer. The
    # steward can act on an existing independent project without being asked.
    actor = ADULTS[alias]
    options = {"self": {STEWARD}}
    if heard == f"{alias}, may I choose the next player?":
        options["child"] = {PLAYER}
    choices = select_means(private_opening(session, actor)["practice_good"], options)
    return choices[0] if choices else None


def run_case(support, root, draws, *, retrieve=True, hours_delta=0, reverse=False, maternal_contrast=False):
    from developmental_recursion import parent_activity as activity, parent_decision as decision
    from developmental_recursion.p2_owner import load_p2

    instance = load_p2().start(root)
    try:
        session = instance.session
        focal = session.read_root()["actor_ids"][0]
        assert session.world().actor_state["A"]["actor_id"] == focal
        support.house.establish(session)
        support.house.establish_dwelling(session)
        period = activity.historical_period_module()
        period.establish_period_plan(session)
        market = decision._b04_module()
        stock = market.default_market_items()
        next(x for x in stock if x["kind"] == "junior_drum_kit")["quantity"] = 1
        market.establish_market_inventory(session, items=stock)

        schedules, references, withdrawal = {}, {}, {}
        for alias, actor in ADULTS.items():
            maternal = alias == "Mara"
            references[alias] = draws["female_profile" if maternal else "male_profile"]
            end = PLAYER if maternal != reverse else STEWARD
            if maternal and maternal_contrast:
                references[alias] = draws["female_profile_work_contrast"]
            target_report = references[alias].read_constraint("richwork")
            candidates = compatible_openings(end, target_report)
            opening = candidates[0]  # declared scenario order, not a probability estimate
            withdrawal[alias] = [use_free_time(candidate, community_cover=False)[0]
                                 for candidate in candidates]
            support.register_supporting_actor(session, alias=alias, actor_id=actor, role="parent",
                                              private_state=opening)
            hours = references[alias].read_constraint("hrs1") + (hours_delta if maternal else 0)
            schedules[alias] = propose(hours, 11 if maternal else 12)
            fixture = {**support.BASE, "cash_units": 3 if maternal else 100,
                       "free_hours": 80, "wage_units_per_hour": 1}
            activity.establish_parent_material(session, actor,
                fixture=activity.parent_material_fixture(actor_id=actor, **fixture))
        for offset in range(7):
            day = START + timedelta(days=offset)
            period.materialize_to(session, day.isoformat())
            for alias, actor in ADULTS.items():
                hours = schedules[alias][offset]
                if hours:
                    activity.record_parent_activity(session, actor, operation_id=str(day),
                                                    activity="PAID_WORK", hours=hours)
        period.materialize_to(session, REFERENCE.isoformat())
        interviews = {}
        for alias, actor in ADULTS.items():
            opening = private_opening(session, actor)
            reports = {"hrs1": observe_hours(activity, session, actor),
                       "richwork": financial_hypothetical(opening)}
            interviews[alias] = {"reports": reports, "matched_items":
                references[alias].compare_emissions(reports)["matched"],
                "alternative_workshop_reading": financial_hypothetical(opening, community_cover=True)}
            decision.admit_parent_decision(session, actor, operation_id="rehearsal",
                request=decision.parent_request_fixture(kind="junior", owner_actor_id=actor), as_actor=actor)

        # Following the reference interview there is a discretionary hour.
        # These adults anticipate who can be reached by each feasible use.
        extra_hour = {}
        for alias, actor in ADULTS.items():
            choices = use_free_time(private_opening(session, actor))
            choice, = choices
            activity.record_parent_activity(session, actor, operation_id="free-hour",
                                            activity=choice, hours=1)
            extra_hour[alias] = choice

        learned = HeardReplies(focal)
        for round_no, phrase in enumerate(INVITES):
            period.materialize_to(session, (REFERENCE + timedelta(days=round_no + 1)).isoformat())
            # Cross speaker with wording. Order reverses across rehearsal bouts.
            for alias in (list(ADULTS) if round_no == 0 else list(reversed(ADULTS))):
                invite = say(session, alias, phrase, f"offer-{round_no}")
                request = hear_request(session, invite["speaker_alias"])
                holder = proposed_holder(session, alias, request[alias])
                reply = say(session, alias, YES if holder == "child" else NO, f"reply-{round_no}")
                learned.observe(invite, reply)

        period.materialize_to(session, (REFERENCE + timedelta(days=3)).isoformat())
        offers = [say(session, who, "Anyone ready?", "today") for who in reversed(ADULTS)]
        state = learned if retrieve else HeardReplies(focal)
        chosen, distinction, scores = state.forecasts(offers)
        request = hear_request(session, chosen)
        attempts = {}
        # The addressee can answer first. The other parent still has a turn.
        for alias in [chosen] + [who for who in ADULTS if who != chosen]:
            actor = ADULTS[alias]
            holder = proposed_holder(session, alias, request[alias])
            if holder is None:
                attempts[alias] = {"action": "no proposal"}
                continue
            admitted = decision.admit_parent_decision(session, actor, operation_id="today",
                request=decision.parent_request_fixture(
                    kind="junior", owner_actor_id=focal if holder == "child" else actor), as_actor=actor)
            acted = decision.perform_parent_decision(session, actor, decision_id="today", as_actor=actor)
            attempts[alias] = {"action": acted["decision_action"], "performed": acted["performed"],
                               "reasons": admitted["decision"]["reasons"]}
        holdings = market.read_owned_objects(session)["totals"]
        assert len(holdings) == 1 and holdings[0]["quantity"] == 1
        owner_id = holdings[0]["owner_actor_id"]
        return {"interviews": interviews, "post_interview_activity": extra_hour,
                "compatible_openings_if_off_shift_access_lost": withdrawal, "heard_rehearsal_exchanges": len(learned.seen),
                "recruited": retrieve, "forecast_grouping": distinction, "forecasts_Sam_Mara": scores,
                "addressed": chosen, "attempts": attempts,
                "holder": "child" if owner_id == focal else next(name for name, identity in ADULTS.items() if identity == owner_id)}
    finally:
        instance.close()


def run(tree, archive):
    subprocess.run(["git", "diff", "--quiet", PIN, "--", ":(glob)WORKER_RETURNS/SOROK-*/**", "rawlsing_next"],
                   cwd=tree, check=True)
    sys.path.insert(0, str(tree / "WORKER_RETURNS/SOROK-DUEL-D03-R1/tests"))
    import d03_support
    source, draws = draw_targets(archive, include_work_contrasts=True)
    scenarios = {"ordinary": {}, "without_recruitment": {"retrieve": False},
                 "shorter_maternal_week": {"hours_delta": -8}, "exchanged_commitments": {"reverse": True},
                 "different_maternal_reference": {"maternal_contrast": True}}
    with TemporaryDirectory() as folder:
        cases = {key: run_case(d03_support, Path(folder) / key, draws, **options)
                 for key, options in scenarios.items()}
    assert [(case["addressed"], case["holder"]) for case in cases.values()] == [
        ("Mara", "child"), ("Sam", "Sam"), ("Mara", "Sam"), ("Sam", "child"), ("Mara", "Sam")]
    return {"owner_pin": PIN, "grade": "sourcefree owner execution with research-only readers",
            "work_context": {key: source[key]["work_context"] for key in ("female_profile", "male_profile")},
            "shorter_week": "single-constraint intervention, eight hours below the original draw",
            "different_maternal_reference": "entire empirical A/C reference drawn within the same three work codes, conditional on the other RICHWORK answer", "cases": cases}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owner_tree", type=Path)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.owner_tree.resolve(), args.archive), indent=2))
