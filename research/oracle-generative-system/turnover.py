"""Finite ORACLE experiment. Run from the repository root with PYTHONPATH=.

C11 queries and the P6 encounter use incumbent code. Workshop rules, the learner,
the census instrument and its truthful reporting assumption are research fixtures.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _build_source, _cell_map, _query, _query_authority, _run,
)

ITEMS = ("made_a_repair", "gave_a_lesson", "signed_an_admission")
PROFILES = tuple(product((0, 1), repeat=3))
P6 = Path(__file__).resolve().parents[2] / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py"


@dataclass(frozen=True)
class Incumbent:
    name: str
    past_acts: tuple[str, ...]

    def report(self):
        return tuple(int(item in self.past_acts) for item in ITEMS)


def select_rosters(parity):
    """Match the intact observation, before any encounter or future choices."""
    tag = f"workshop-{parity}"
    rows = [{"id": f"r{x}{y}", "responses": dict(zip(ITEMS, (x, y, x ^ y ^ parity)))}
            for x, y in product((0, 1), repeat=2)]
    source = _build_source(tag, rows, question_namespace="workshop", risk_namespace="workshop")
    authority = _query_authority(tag)
    population = _branch_predicate(source, authority)

    def counts(items):
        query = _query(source, authority, population, items)
        fact, = _run(source, authority, population, query).facts
        assert fact.raw_denominator_support == len(rows)
        cells = {cell: entry["raw_numerator_support"] for cell, entry in _cell_map(fact).items()}
        return fact.ref.key, cells

    fact_ref, observed = counts(ITEMS)
    lower = {"+".join(items): {str(k): n for k, n in counts(items)[1].items()}
             for size in (1, 2) for items in combinations(ITEMS, size)}
    target = Counter({tuple(map(int, cell)): n for cell, n in observed.items() if n})
    matches = []
    # Enumerate the same library for both releases. No respondent is a named worker.
    # Four distinct profiles is a finite support choice specific to this witness.
    for candidate in combinations(PROFILES, 4):
        workers = tuple(Incumbent(f"worker-{i}", tuple(item for item, bit in zip(ITEMS, bits) if bit))
                        for i, bits in enumerate(candidate))
        if Counter(w.report() for w in workers) == target:
            matches.append(workers)
    roster, = matches  # unique multiset in this small library, not unique human lives
    return roster, {"release": source["release_ref"].key, "fact": fact_ref,
                    "joint": {"".join(cell): n for cell, n in observed.items()}, "lower": lower}


def teaching_team(roster, *, divided, mandates, refuse=()):
    """External office mandates and actors' availability independently gate participation.

    The three jobs are sequential. One available person may take several turns.
    The continuing competence of former performers is a fixture assumption.
    """
    available = [w for w in roster if w.name not in refuse]
    possible = [[w.name for w in available if item in w.past_acts
                 and (item != ITEMS[2] or w.name in mandates)] for item in ITEMS]
    return next((team for team in product(*possible) if divided or len(set(team)) == 1), ())


def command(state, *args):
    completed = subprocess.run([sys.executable, str(P6), "--state", str(state), *args],
                               capture_output=True, text=True, check=True, timeout=120)
    return json.loads(completed.stdout)


def encounter(state, team):
    """A fictional delegation can request a joint inspection. Nadia can withhold it."""
    command(state, "new")
    if not team:
        return {"offered": False, "inspection": False, "uptake": None}
    reply = command(state, "say", "Could we look at the edge together?", "--request-edge",
                    "--request-id", "workshop-visit")
    restored = command(state, "view")
    assert restored["invitation"] == reply["invitation"]
    turns = json.loads((state / "p4_receipts.json").read_text())["turns"]
    receipt = turns[-1]["receipt"]
    inspected = False
    if restored["invitation"]:
        command(state, "inspect-edge", restored["invitation"], "--request-id", "accepted-visit")
        turn = json.loads((state / "p4_receipts.json").read_text())["turns"][-1]
        inspected = bool(turn["public"]["performed"] and turn["receipt"]["performed"]["kind"] == "INSPECT")
    return {"offered": True, "inspection": inspected, "uptake": receipt["uptake"]["status"],
            "actor_mode": receipt["uptake"]["mode"], "actor_sources": receipt["uptake"]["readset"],
            "speech_event": receipt["speech"]["performed"]["event_id"],
            "expression_event": (receipt["expression"] or {}).get("event_id")}


@dataclass(frozen=True)
class Demonstration:
    mark: str
    touched: str


def choose_edge(memory, mark, rule):
    if rule is None or not memory:
        return None
    last = memory[-1]
    if rule == "repeat":
        return last.touched
    if rule == "follow_mark" and last.mark == last.touched:
        return mark
    return None


@dataclass(frozen=True)
class PublicDecision:
    """One earlier conflict the apprentice personally witnessed and acted in."""
    listed: bool
    repaired: bool
    endorsed: bool


def practical_reading(history, encounter):
    """Two TEST_ONLY representations of how this actor has used a standard of worth.

    Retain every interpretation compatible with witnessed prior endorsements.
    A refusal to infer a unique act differs from an inferred refusal to act.
    """
    standards = ("listed", "repaired")
    remembered = tuple(key for key in standards
                       if all(getattr(row, key) == row.endorsed for row in history))
    # Event-memory rival reconstructs its predictions when a fresh case arrives.
    episodic = {getattr(encounter, key) for key in standards if all(
        getattr(row, key) == row.endorsed for row in history)}
    # The sparse representation retained those same undefeated distinctions.
    compiled = {getattr(encounter, key) for key in remembered}
    assert compiled == episodic
    return next(iter(compiled)) if len(compiled) == 1 else None


def succession(inspection, *, sight=True, rule="follow_mark", exam="register",
               can_appeal=False, examiner_assents=False, proprietor_honors=False,
               pass_on=True, materials=2, past_choice="endorse_work"):
    """Explicit reference semantics after the native visit. All times are ordered."""
    # The physical cue is provided by this experiment AFTER native inspection.
    # P6 did not teach a skill or produce a guild certificate.
    memory = [Demonstration("left", "left")] if inspection and sight else []
    attempted = choose_edge(memory, "right", rule)
    worked = attempted == "right" and materials > 0
    remaining = materials - int(attempted is not None and materials > 0)
    # The inherited register admits only a founder's family; the newcomer is unrelated.
    # The exercise examiner judges a completed test independently of self-description.
    admitted = worked if exam == "work_sample" else False
    # Prior voluntary endorsements are historical inputs. An evaluator cannot
    # infer the origin of the actor's commitment simply by fitting these acts.
    history = [PublicDecision(True, True, True), PublicDecision(False, False, False)]
    if past_choice != "unseparated":
        history.append(PublicDecision(False, True, past_choice == "endorse_work"))
    recognizes_claim = practical_reading(history, PublicDecision(False, worked, False))
    petition = worked and not admitted and can_appeal and recognizes_claim is True
    ratified = petition and examiner_assents and proprietor_honors
    next_exam = "work_sample" if ratified else exam
    # Prospective amended rule recognizes the retained sample on resubmission.
    admitted = admitted or (ratified and worked)
    # Original roster has exited. A new learner can be served only by this successor.
    teaches_next = admitted and pass_on and remaining > 0
    if teaches_next:
        remaining -= 1
    return {"observations": len(memory), "assessment": "NOT_EVALUATED" if rule is None else "TEST_ONLY",
            "attempt": attempted, "successful_work": worked, "own_reading": recognizes_claim,
            "petition": petition,
            "amendment": ratified, "next_exam": next_exam, "new_standing": admitted,
            "next_learner_saw_lesson": teaches_next, "remaining_stock": remaining}


def main(directory):
    results = []
    for parity in (0, 1):
        roster, evidence = select_rosters(parity)
        # Fictional separate charter and mandate, never derived as authority from survey.
        mandates = {w.name for w in roster}
        for divided in (False, True):
            team = teaching_team(roster, divided=divided, mandates=mandates)
            assert not teaching_team(roster, divided=divided, mandates=set())
            assert not teaching_team(roster, divided=divided, mandates=mandates, refuse=mandates)
            visit = encounter(directory / f"{parity}-{int(divided)}", team)
            inspected = visit["inspection"]
            amended = dict(can_appeal=True, examiner_assents=True, proprietor_honors=True)
            branches = {name: succession(inspected, **options) for name, options in {
                "inherited_register": {}, "collective_amendment": amended,
                "defends_register": dict(amended, past_choice="endorse_register"),
                "meaning_underdetermined": dict(amended, past_choice="unseparated"),
                "examiner_dissents": dict(amended, examiner_assents=False),
                "owner_declines": dict(amended, proprietor_honors=False),
                "unseen": dict(amended, sight=False), "law_withheld": dict(amended, rule=None),
                "replay_gesture": dict(amended, rule="repeat"),
                "declines_to_teach": dict(amended, pass_on=False),
                "materials_exhausted": dict(amended, materials=1),
                "work_sample_charter": {"exam": "work_sample"},
            }.items()}
            results.append({"parity": parity, "divided": divided, "team": team,
                            "evidence": evidence, "visit": visit, "branches": branches})
    assert results[0]["evidence"]["lower"] == results[2]["evidence"]["lower"]
    assert [r["visit"]["inspection"] for r in results] == [False, True, True, True]
    for r in results:
        cases = r["branches"]
        seen = r["visit"]["inspection"]
        assert cases["collective_amendment"]["next_learner_saw_lesson"] == seen
        assert cases["work_sample_charter"]["next_learner_saw_lesson"] == seen
        if seen:
            assert cases["meaning_underdetermined"]["own_reading"] is None
            assert cases["defends_register"]["own_reading"] is False
        assert cases["inherited_register"]["successful_work"] == seen
        assert cases["declines_to_teach"]["new_standing"] == seen
        assert cases["materials_exhausted"]["remaining_stock"] == (0 if seen else 1)
        assert cases["law_withheld"]["assessment"] == "NOT_EVALUATED"
        for name in set(cases) - {"collective_amendment", "work_sample_charter"}:
            assert not cases[name]["next_learner_saw_lesson"]
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, help="keep the four fresh, playable P6 roots here")
    args = parser.parse_args()
    if args.state:
        args.state.mkdir(parents=True, exist_ok=False)
        print(json.dumps(main(args.state), indent=2))
    else:
        with TemporaryDirectory() as tmp:
            print(json.dumps(main(Path(tmp)), indent=2))
