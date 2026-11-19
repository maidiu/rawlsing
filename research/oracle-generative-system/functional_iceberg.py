"""Research semantics for directly populated adult expectations and child acquisition.

The two authored proposals are fictional alternatives for one adult. The four
reference questions are a selected capacity probe, not a production target draw.
No model service, source respondent reconstruction or native P3 writer is invoked.
"""
from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass(frozen=True)
class Occasion:
    audience_can_reply: bool
    sponsor_vouches: bool
    message_disputed: bool = True


@dataclass(frozen=True)
class Expectation:
    cue: str
    anticipated_effect: str
    provenance: str
    threatens: str | None = None


@dataclass
class Actor:
    commitments: frozenset
    expectations: dict = field(default_factory=dict)

    def retain_or_admit(self, event):
        # One actor's situated interpretation of giving space to a disputed message.
        # Independent constraints (a venue closing, another participant declining)
        # can still defeat an attempted act.
        if not event.message_disputed:
            return True
        cues = []
        if event.sponsor_vouches:
            cues.append("public_sponsor_vouches")
        if not event.audience_can_reply:
            cues.append("audience_cannot_reply")
        for cue in cues:
            anticipated = self.expectations.get(cue)
            if anticipated and anticipated.threatens in self.commitments:
                return False
        return True

    def attempt(self, cue):
        expected = self.expectations.get(cue)
        if expected and expected.anticipated_effect in {
                "my_choice_considered", "selected_object_obtained_after_indicating"}:
            return "indicate_choice"
        return "observe"


def install_opening(proposal):
    """Interpret a small fixed capability vocabulary without executing generated code."""
    cues = {"public_sponsor_vouches", "audience_cannot_reply", "open_hand"}
    if proposal["provenance"] != "constructed_adult_antecedent":
        raise ValueError("Wrong inlet for an acquired or witnessed record")
    actor = Actor(frozenset(proposal["protected_goods"]))
    for cue, effect, threatened_good in proposal["expectations"]:
        if cue not in cues or cue in actor.expectations:
            raise ValueError("Unknown or duplicate recruitment cue")
        if threatened_good is not None and threatened_good not in actor.commitments:
            raise ValueError("Unbound commitment")
        actor.expectations[cue] = Expectation(cue, effect, proposal["provenance"], threatened_good)
    return actor


def reference(actor):
    # Source polarity: permit speech = 1; remove book = 1. The four original
    # prompts and interpretations are distinct; this scoped world posits that
    # both described views are disputed and each library is understood to vouch.
    answers = {}
    for subject in ("ath", "com"):
        talk = Occasion(True, False)
        shelf = Occasion(False, True)
        answers["spk" + subject] = 1 if actor.retain_or_admit(talk) else 2
        answers["lib" + subject] = 2 if actor.retain_or_admit(shelf) else 1
    return answers


@dataclass(frozen=True)
class Encounter:
    cue: str
    child_signaled: bool
    other_was_free: bool
    outcome_visible: bool
    own_choice_realized: bool


def acquire(child, experienced):
    # Test-only within-cue contrast. Equal exposures alone have no learning effect.
    # An event that was not accessible never enters this first-person trace list.
    for cue in {event.cue for event in experienced}:
        eligible = [e for e in experienced if e.cue == cue and e.other_was_free and e.outcome_visible]
        attempted = [e.own_choice_realized for e in eligible if e.child_signaled]
        baseline = [e.own_choice_realized for e in eligible if not e.child_signaled]
        if len(attempted) < 2 or len(baseline) < 2:
            continue
        difference = sum(attempted) / len(attempted) - sum(baseline) / len(baseline)
        if difference >= 0.5:
            child.expectations[cue] = Expectation(cue, "selected_object_obtained_after_indicating",
                                                  "contrast_in_accessible_encounters")


def run():
    proposals = json.loads(Path(__file__).with_name("constructed_openings.json").read_text())
    reference_target = {"spkath": 1, "libath": 1, "spkcom": 1, "libcom": 1}
    independent_shelf = Occasion(False, False)
    # At a neighborhood lending table the sponsor explicitly disclaims endorsement.
    # Both adults have the physical ability to leave a disputed story available.
    results = []
    for proposal in proposals:
        person = install_opening(proposal)
        emitted = reference(person)
        assert emitted == reference_target
        keep = person.retain_or_admit(independent_shelf)
        child = Actor(frozenset())
        before = child.attempt("open_hand")
        traces = []
        for signaled in (False, True, True, False):
            # An ordinary prelinguistic choice between objects; practice scenarios
            # share an adult's open hand. The disputed story is available only
            # if the adult left it on the table. Child sees what was picked.
            own_choice_realized = signaled and keep
            traces.append(Encounter("open_hand", signaled, True, True, own_choice_realized))
        acquire(child, traces)
        learned = child.expectations.get("open_hand")
        act = child.attempt("open_hand")
        # The adult and child read the same expectation type. A later shortage
        # can defeat the child's newly attempted action without erasing its cause.
        def fulfill(available):
            return available and act == "indicate_choice" and keep

        later = {name: fulfill(available) for name, available in (("stocked", True), ("empty", False))}
        results.append({"constructed_opening": proposal["name"], "reference": emitted, "disclaimed_collection_retained": keep,
                        "adult_at_same_invitation": person.attempt("open_hand"),
                        "acquired_anticipation": learned.anticipated_effect if learned else None,
                        "before": before, "after": act, "other_cue": child.attempt("closed_book"),
                        "later_choice_fulfilled": later})
    assert [r["acquired_anticipation"] for r in results] == [
        "selected_object_obtained_after_indicating", None]
    assert results[0]["after"] == "indicate_choice" and results[1]["after"] == "observe"
    return results


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
