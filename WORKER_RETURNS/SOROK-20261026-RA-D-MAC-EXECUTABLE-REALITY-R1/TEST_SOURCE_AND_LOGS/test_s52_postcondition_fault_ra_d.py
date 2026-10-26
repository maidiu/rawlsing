"""RA-D independent reproduction of the S52 later-episode postcondition skip.

This is a forensic diagnostic, not an accepted product test. It asserts the
correct invariant: unauthorized B-state divergence after a performed paid
episode must be rejected even when an unrelated later episode exists.
"""
from __future__ import annotations
import json, sys, tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
ARCHIVE = RETURN / "isolated_archive_s52c821"
S52 = ARCHIVE / "WORKER_RETURNS" / "SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1"
if str(S52) not in sys.path:
    sys.path.insert(0, str(S52))
from s52.bootstrap import install  # noqa: E402
install()
from s45.fixtures import root_bundle  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s52.session import S52Session  # noqa: E402

state = Path(tempfile.mkdtemp(prefix="ra-d-s52-hostile-"))
c = case_for(True)
s = S52Session.start(state, bundle=root_bundle("01"*32), case=c,
                     source=source_for(c), language_context={"milieu_id":"workshop"})
try:
    actual = s.run_experiment()
    candidate = actual["candidate"]; generation = actual["generation"]
    performed = s.perform_paid_participation(
        candidate, generation=generation, counterpart_performed=True)
    after = dict(s.world().actor_state["B"])
    s._append("S52_UNRELATED_TEST_NOTE", {
        "schema": "RA_D_UNRELATED_NOTE@1",
        "reason": "A later canonical episode without a lawful B transition.",
        "caught": "S52_CURRENT_STATE_DIVERGES:cash",
    })
    world = s.world()
    world.actor_state["B"]["cash"] = 999
    s.product._checkpoint(s.branch_id, s.clock(), world)
    warm = s.verify()
finally:
    s.close()

cold = S52Session.open(state)
try:
    cold_verify = cold.verify()
    cold_b = dict(cold.world().actor_state["B"])
finally:
    cold.close()

result = {
    "schema": "RA_D_S52_POSTCONDITION_FAULT_PROBE@1",
    "state_root": str(state),
    "performed": performed.get("performed"),
    "after_action_cash": after.get("cash"),
    "tampered_cash": cold_b.get("cash"),
    "warm_ok": warm.get("ok"),
    "warm_s52_errors": warm.get("s52", {}).get("errors", []),
    "cold_ok": cold_verify.get("ok"),
    "cold_s52_errors": cold_verify.get("s52", {}).get("errors", []),
    "correct_invariant": "tampered cash after performed paid episode must be rejected",
    "defect_reproduced": bool(warm.get("ok") is True and cold_verify.get("ok") is True),
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["defect_reproduced"] else 2)
