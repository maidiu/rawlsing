"""RA-C hostile S52 verifier diagnostic; UNEXECUTED here. SOURCEFREE TEST_ONLY.

Must run against pinned S52 archive with verified G18 and selected import closure.
A red assertion after true warm/cold verify establishes the unresolved defect.
Do not interpret controlled counterpart performance as an endogenous actor decision.
"""
from __future__ import annotations
import json
import tempfile
from pathlib import Path
from s52.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s52.session import S52Session

def run() -> dict:
    c = case_for(True)
    with tempfile.TemporaryDirectory(prefix="ra_c_s52_") as root:
        s = S52Session.start(
            Path(root), bundle=root_bundle("01" * 32),
            case=c, source=source_for(c),
            language_context={"milieu_id": "workshop"},
        )
        try:
            actual = s.run_experiment()
            candidate = actual["candidate"]
            generation = actual["generation"]
            out = s.perform_paid_participation(
                candidate, generation=generation, counterpart_performed=True
            )
            assert out["performed"] is True, "fixture setup controlled payment did not occur"
            expected_cash = (out["after"] or {})["cash"]
            s._append("S52_UNRELATED_TEST_NOTE", {
                "scope": "RA_C_TEST_ONLY",
                "cause": "none",
                "actor_transition": False,
            })
            world = s.world()
            world.actor_state["B"]["cash"] = expected_cash + 943
            s.product._checkpoint(s.branch_id, s.clock(), world)
            warm = s.verify()
            result = {
                "schema": "RA_C_S52_LATER_UNRELATED_NOTE_ABLATION@1",
                "source_grade": "TEST_ONLY_NON_NATIVE",
                "controlled_performance": True,
                "unrelated_note": True,
                "lawful_actor_transition_after_paid": False,
                "cash_lawful_after": expected_cash,
                "cash_tampered": expected_cash + 943,
                "warm_ok": bool(warm.get("ok")),
                "warm_errors": warm.get("s52", {}).get("errors", []),
            }
        finally:
            s.close()
        cold = S52Session.open(Path(root))
        try:
            cv = cold.verify()
            result["cold_ok"] = bool(cv.get("ok"))
            result["cold_errors"] = cv.get("s52", {}).get("errors", [])
        finally:
            cold.close()
        print(json.dumps(result, indent=2, sort_keys=True))
        if result["warm_ok"] or result["cold_ok"]:
            raise AssertionError("S52_VERIFIER_RED: unauthorized B cash mutation was not rejected")
        return result

if __name__ == "__main__":
    run()
