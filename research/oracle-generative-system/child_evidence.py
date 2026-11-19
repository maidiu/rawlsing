"""What can this child distinguish about a parent's performed purchase?

Run against the pinned SOROK candidate. Uses the actual speech, child-access,
P3 immediate-response and purchase owners on one session per counterfactual.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

PIN = "ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9"


def measure(support, root, prior, debt):
    from developmental_recursion import parent_decision
    from developmental_recursion.parent_speech import read_child_experience
    from p3.immediate_uptake import build_immediate_uptake

    case = support.open_speech_case(root, outcome=prior, debt_units=debt, child_present=True,
                                    text="We can talk about it.", operation_id="one-utterance")
    owner = case["case"].owner
    try:
        session = case["session"]
        event = case["receipt"]["event_id"]
        speech = read_child_experience(session, case["focal"], event_id=event)
        uptake = build_immediate_uptake(owner, speech_event_id=event, child_id=case["focal"],
                                         utterance_receipt=case["receipt"], plan=case["plan"])
        # The parent performs the decision after speaking. Read both sides of
        # the actual transaction and the child's own receipt stream.
        market = parent_decision._b04_module()
        child_alias = speech["response_input"]["child_alias"]

        def stock():
            items = market.read_market_inventory(session)["items"]
            return next(item["quantity"] for item in items if item["kind"] == "junior_drum_kit")

        def child_receipts():
            return session.product.store.perceptions(session.branch_id, actor_id=child_alias)

        before_stock = stock()
        before_access = child_receipts()
        acted = parent_decision.perform_parent_decision(
            session, support.PARENT_ID, decision_id="d03-decision", as_actor=support.PARENT_ID)
        after_access = child_receipts()
        assert before_access == after_access
        assert uptake["store_head"]["before"] == uptake["store_head"]["after"]
        return {"prior_fixture": prior, "opening_debt": debt, "present": True,
                "child_speech_status": speech["status"],
                "eligible_modes": uptake["immediate_response"]["eligible_modes"],
                "action": acted["decision_action"], "action_status": acted["status"],
                "stock_change": stock() - before_stock, "new_child_receipts_at_purchase": len(after_access) - len(before_access),
                "durable_status": uptake["durable_formation"]["status"]}, speech.get("response_input")
    finally:
        owner.close()


def run(owner_root):
    subprocess.run(["git", "diff", "--quiet", PIN, "--", ":(glob)WORKER_RETURNS/SOROK-*/**",
                    "rawlsing_next"], cwd=owner_root, check=True)
    sys.path.insert(0, str(owner_root / "WORKER_RETURNS/SOROK-DUEL-D03-R1/tests"))
    import d03_support
    cases, projections = [], []
    with TemporaryDirectory() as tmp:
        # Reuse the same fixture pathname for deterministic event identities.
        for prior in ("recognized_plan", "imposed_plan"):
            for debt in (4, 210):
                case, projection = measure(d03_support, Path(tmp) / "world", prior, debt)
                cases.append(case)
                projections.append(projection)
    assert projections[0] and all(p == projections[0] for p in projections)
    assert [r["stock_change"] for r in cases] == [-1, 0, -1, 0]
    assert [r["eligible_modes"] for r in cases] == [["joint_check"]] * 2 + [["private_check"]] * 2
    return {"owner_pin": PIN, "identical_complete_child_speech_inputs": True, "cases": cases}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owner_root", type=Path)
    print(json.dumps(run(parser.parse_args().owner_root.resolve()), indent=2))
