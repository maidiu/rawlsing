"""TEST_ONLY adapter for the S35 present-orientation / T-NO_CHANGE candidate."""
from __future__ import annotations

A_ACTIONS = ("ATTEND_OBJECT", "REQUEST_TOOL", "EXPLICIT_REFUSAL")
T_NO_CHANGE = {
    "state_kind": "V3MS_PRACTICE",
    "operation": "NO_CHANGE",
    "target_proposal": None,
    "grant": None,
    "beforestate_mutation": False,
    "native": False,
}


def evaluate(*, access: bool, actions: tuple[str, ...] = (),
             contradictory: bool = False, b_operation: str | None = None,
             prior_acts: tuple[str, ...] = (), labels: tuple[str, ...] = ()) -> dict:
    """Classify one sourcefree A witness without inventing psychology.

    Prior acts do not imply acquisition; labels do not change the predicate.
    """
    if contradictory:
        status = "AMBIGUOUS_CONTRADICTORY"
        response = None
    elif not access:
        status = "UNKNOWN_RECEIVABILITY"
        response = None
    elif actions:
        unknown = [action for action in actions if action not in A_ACTIONS]
        if unknown:
            status = "UNSUPPORTED_ACTION"
            response = None
        elif all(action == "EXPLICIT_REFUSAL" for action in actions):
            status = "OBSERVED_CURRENT_REFUSAL"
            response = "EXPLICIT_REFUSAL"
        else:
            status = "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
            response = actions[-1]
    else:
        status = "RECEIVABLE_NO_OBSERVED_UPTAKE"
        response = None
    return {
        "schema": "S35_CONDITIONAL_A_T_ADAPTER@1",
        "status": status,
        "a_access": "ADMITTED" if access else "NOT_ADMITTED",
        "a_actions": list(actions),
        "a_response": response,
        "b_operation": b_operation,
        "b_refusal_implies_a_help_accept": False,
        "prior_acts_ignored": list(prior_acts),
        "labels_ignored": list(labels),
        "t": dict(T_NO_CHANGE),
        "grade": "TEST_ONLY_SOURCEFREE_NOT_ISSUED",
        "native": False,
    }
