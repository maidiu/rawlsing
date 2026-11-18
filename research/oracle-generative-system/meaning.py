"""A proposed early receiving rule, followed by the existing P3/P4 owner.

python3 meaning.py    # run from any working directory, with repository deps
The four dated work allocations and actor-access law are research semantics.
"""
from dataclasses import asdict, dataclass
from itertools import product
import json
from random import Random
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
P4 = HERE.parents[1] / "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py"


@dataclass(frozen=True)
class Allocation:
    shift: int
    posted: str
    proposed: str | None
    performed: str


def work_history(offered, supervisor):
    """Independent project schedules. One machine slot serves one order per shift."""
    rows = []
    for t, (posted, needed, meeting) in enumerate(zip(
            ("east", "west", "east", "west"), ("west", "east", "east", "west"), offered)):
        # Worker sees next pickup's destination. Dispatcher controls the machine.
        proposal = needed if meeting else None
        executed = proposal if proposal and supervisor == "accept_revision" else posted
        rows.append(Allocation(t, posted, proposal, executed))
    return rows


def read_history(rows, *, saw_result=True, law="contrast"):
    """Interpret only the worker's proposals and accessible resulting allocations."""
    known = [r for r in rows if r.proposed and saw_result]
    if law == "coincidence":
        # Competing learning law credits successful suggestion even if it changed nothing.
        if known and all(r.proposed == r.performed for r in known):
            return "recognized_plan"
    # Rule is identifiable within these four alternatives only. A constant choice
    # or the posted schedule can also fit a short history of apparent agreement.
    predictions = {"recognized_plan": lambda r: r.proposed, "imposed_plan": lambda r: r.posted,
                   "always_east": lambda r: "east", "always_west": lambda r: "west"}
    fits = [k for k, predict in predictions.items() if all(predict(r) == r.performed for r in known)]
    return fits[0] if len(fits) == 1 and fits[0] in ("recognized_plan", "imposed_plan") else ""


def interview_work(rows, meaning):
    """Two provisional readings of participation for a synthetic four-shift job.

    Counting four shifts as the relevant recall horizon is a scenario assumption.
    Only score the polar cases; the cutoff for sometimes/rarely is unidentified.
    """
    if meaning == "contributing":
        qualifying = [r for r in rows if r.proposed]
    elif meaning == "changing_the_allocation":
        qualifying = [r for r in rows if r.proposed and r.performed != r.posted]
    else:
        raise ValueError(meaning)
    if not qualifying:
        return "never"
    if len(qualifying) == len(rows):
        return "often"
    return "intermediate_threshold_unqualified"


def later_expression(root, antecedent):
    def command(*args):
        reply = subprocess.run([sys.executable, str(P4), "--state", str(root), *args],
                               cwd=HERE.parents[1], capture_output=True, text=True, timeout=120)
        if reply.returncode:
            raise RuntimeError(reply.stderr or reply.stdout)
        return json.loads(reply.stdout)
    command("new", "--history", antecedent)
    command("say", "Could we check the edge together?", "--request-edge", "--request-id", "check")
    turn = json.loads((root / "p4_receipts.json").read_text())["turns"][-1]["receipt"]
    assert turn["speech"]["performed"] and turn["expression"]["event_id"]
    return {"mode": turn["uptake"]["mode"], "expression": turn["expression"]["event_id"],
            "readset": turn["uptake"]["readset"]}


def run():
    data = json.loads((HERE / "conditioning.json").read_text())
    all_shifts = (True,) * 4
    same_plan_only = (False, False, True, True)
    examples = {}
    with TemporaryDirectory() as tmp:
        by_label = {}
        for name, offers, boss, visible, law in [
                ("revisions_used", all_shifts, "accept_revision", True, "contrast"),
                ("roster_controls", all_shifts, "follow_roster", True, "contrast"),
                ("results_inaccessible", all_shifts, "follow_roster", False, "contrast"),
                ("observational_alias", same_plan_only, "follow_roster", True, "contrast"),
                ("coincidence_rival", same_plan_only, "follow_roster", True, "coincidence")]:
            history = work_history(offers, boss)
            label = read_history(history, saw_result=visible, law=law)
            if label not in by_label:
                by_label[label] = later_expression(Path(tmp) / name, label)
            examples[name] = {"world_allocations": [asdict(r) for r in history],
                              "saw_result": visible, "rule": law, "derived_input": label or None,
                              "incumbent": by_label[label],
                              "work_question_if_contributing": interview_work(history, "contributing"),
                              "work_question_if_changing_allocation": (
                                  interview_work(history, "changing_the_allocation") if visible else None)}
    assert [e["incumbent"]["mode"] for e in examples.values()] == [
        "joint_check", "private_check", "inspect_alone", "inspect_alone", "joint_check"]

    assert examples["revisions_used"]["work_question_if_contributing"] == "often"
    assert examples["roster_controls"]["work_question_if_contributing"] == "often"
    assert examples["roster_controls"]["work_question_if_changing_allocation"] == "never"

    def yield_at(rate, boss):
        success = 0.
        for offers in product([False, True], repeat=4):
            probability = rate**sum(offers) * (1-rate)**(4-sum(offers))
            if read_history(work_history(offers, boss)):
                success += probability
        return success

    # Scenario assumptions about chances to compare plans. In the alternative
    # law equalizing these rates removes the entire source effect through this path.
    contributions = {}
    for domain in ("employed_female", "employed_male"):
        for target, condition in data[domain]["conditionals"].items():
            p = condition["team_often"]
            for boss in ("accept_revision", "follow_roster"):
                high, low = yield_at(.8, boss), yield_at(.2, boss)
                contributions[f"{domain}/{target}/{boss}"] = {
                    "probability_of_informative_history": p * high + (1-p) * low,
                    "equal_opportunity_control": yield_at(.5, boss)}

    # Bounds for a misclassified formative regime. P(report != regime) <= eps
    # separately inside the tip and its complement. The profile includes the tip.
    sensitivity = {}
    for domain in ("employed_female", "employed_male"):
        facts = data[domain]
        mass = facts["weighted_observed_support"]["1111"]["mass"]
        p_tip = facts["conditionals"]["1111"]["team_often"]
        p_all = facts["conditionals"]["profile_only"]["team_often"]
        p_rest = (p_all - mass * p_tip) / (1 - mass)
        gap = yield_at(.8, "accept_revision") - yield_at(.2, "accept_revision")
        for eps in (0., .05, .10, .20):
            low = (1-mass) * (max(0., p_tip-eps) - min(1., p_rest+eps))
            high = (1-mass) * (min(1., p_tip+eps) - max(0., p_rest-eps))
            sensitivity[f"{domain}/{eps}"] = {
                "formative_probability_difference_bounds": [gap * low, gap * high],
                "design_se_at_zero_disagreement": gap * facts["tip_profile_difference_se"]}

    def propose(domain, rng):
        support = data[domain]["weighted_observed_support"]
        tip = rng.choices(list(support), weights=[row["mass"] for row in support.values()])[0]
        return tip, support[tip]["team_often"]

    def proposal_to_act(root, team_probability, draw, shifts, boss):
        rate = .8 if draw < team_probability else .2
        offered = [u < rate for u in shifts]
        history = work_history(offered, boss)
        label = read_history(history)
        receipt = later_expression(root, label)
        return {"offers": offered, "derived": label or None, "response": receipt["mode"],
                "performed_expression": receipt["expression"], "readset": receipt["readset"]}

    # An inverse research ticket and opportunity draws are never supplied to P3.
    # Show both unselected draws and a common-quantile causal contrast. The
    # integrated results above also cover the quantiles where nothing changes.
    with TemporaryDirectory() as tmp:
        rng = Random(20261118)
        sampled = []
        for domain in ("employed_female", "employed_male"):
            tip, p = propose(domain, rng)
            sampled.append({"domain": domain, "external_tip": tip,
                            **proposal_to_act(Path(tmp) / domain, p, rng.random(), [rng.random() for _ in range(4)],
                                              "accept_revision")})
        women = data["employed_female"]["conditionals"]
        paired = {key: proposal_to_act(Path(tmp) / key, women[key]["team_often"], .4, [.5] * 4, "accept_revision")
                  for key in ("1111", "profile_only")}
    assert paired["1111"]["response"] == "joint_check"
    assert paired["profile_only"]["response"] == "inspect_alone"
    return {"test_only_antecedent_translation": examples, "scenario_law": contributions,
            "misclassification_sensitivity": sensitivity, "sampled_uncommitted_proposals": sampled, "same_draw_source_ablation": paired}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
