"""RA-D S52 verifier control: same tamper with and without a later episode."""
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

def one(with_note):
    state = Path(tempfile.mkdtemp(prefix="ra-d-s52-ctl-"))
    case = case_for(True)
    s = S52Session.start(state, bundle=root_bundle("01" * 32), case=case,
                         source=source_for(case),
                         language_context={"milieu_id": "workshop"})
    try:
        r = s.run_experiment()
        s.perform_paid_participation(r["candidate"], generation=r["generation"],
                                     counterpart_performed=True)
        if with_note:
            s._append("S52_UNRELATED_TEST_NOTE", {"schema": "RA_D_UNRELATED_NOTE@1"})
        world = s.world()
        world.actor_state["B"]["cash"] = 999
        s.product._checkpoint(s.branch_id, s.clock(), world)
        v = s.verify()
        return {"with_note": with_note, "warm_ok": v.get("ok"),
                "errors": v.get("s52", {}).get("errors", [])}
    finally:
        s.close()

print(json.dumps([one(False), one(True)], indent=2, sort_keys=True))
