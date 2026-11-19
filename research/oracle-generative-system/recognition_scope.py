"""Locate the recall/transfer boundary on one existing P2/P3/P4 fixture."""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

RETURNS = Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
sys.path.insert(0, str(RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests"))
sys.path.insert(0, str(RETURNS / "SOROK-P4-FIRST-FULL-MPC-R1"))

from p3_fixture_support import build_case
from developmental_recursion.contracts import RecursionRefusal
from response import express, read_response
from speech import admit_speech


def run(directory):
    case = build_case(directory, history_outcomes=("recognized_plan",),
                      include_compression=False, standpoints=False)
    try:
        owner = case.owner
        owner.realize("prior", case.proposals[0], owner.snapshot())
        session = case.base_owner.fanin.session
        session.produce_interval(case.base_owner.fanin.deps["make_domain"](
            mode="ACTUAL", start=session.clock(), end=session.clock() + 2))
        admission = admit_speech(session, text="Could you look at this edge?",
                                 actor_ref=case.initial.actor, request_edge=True)
        plan = case.plans[0]
        scope = dict(plan, relation_ref=plan["relation_refs"][0])
        head = owner.store.head()
        modes = {}
        for label, change in (("original", {}), ("other counterpart", {"counterpart": "other"}),
                              ("other project", {"project": "other"}), ("null counterpart", {"counterpart": None}),
                              ("inhibited role", {"interlocutor_role": "other"})):
            read_scope = {**scope, **change}
            records = owner.store.query(project=read_scope["project"], counterpart=read_scope["counterpart"],
                                        as_of=session.clock() - 1)
            try:
                uptake = read_response(owner, admission, read_scope)
            except RecursionRefusal as exc:
                if label != "null counterpart" or str(exc).split(":")[0] != "CONTEXT_COUNTERPART":
                    raise
                modes[label] = (len(records), "CONTEXT_COUNTERPART", None)
                continue
            assert admission["performed"]["hash"] in uptake["readset"]
            modes[label] = (len(records), uptake["status"], uptake["mode"])
        assert owner.store.head() == head
        assert modes == {"original": (1, "UPTAKE", "joint_check"),
                         "other counterpart": (0, "UPTAKE", "inspect_alone"),
                         "other project": (0, "UPTAKE", "inspect_alone"),
                         "null counterpart": (0, "CONTEXT_COUNTERPART", None),
                         "inhibited role": (1, "NO_EXPRESSION", None)}
        # Only the original, actually situated read is expressed in the world.
        event, observable = express(session, read_response(owner, admission, scope))
        assert event["event_id"] == observable["event_id"]
        return modes
    finally:
        case.cycle.engine.close()
        case.owner.close()


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        for label, values in run(Path(directory)).items():
            print(label, *values, sep=" | ")
