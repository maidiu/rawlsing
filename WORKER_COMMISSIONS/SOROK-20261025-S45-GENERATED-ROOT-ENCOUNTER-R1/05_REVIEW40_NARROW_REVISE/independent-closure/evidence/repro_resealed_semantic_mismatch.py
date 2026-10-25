import json
import os
import sys
import tempfile
from pathlib import Path

RETURN = Path(os.environ["S45_RETURN"]).resolve()
sys.path.insert(0, str(RETURN))

from s45.bootstrap import install

install()

from bp1.canon import digest
from s37.harness import case_for, source_for
from s45.fixtures import root_bundle
from s45.session import S45Session


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="s45-resealed-semantic-"))
    session = S45Session.start(
        root / "state",
        bundle=root_bundle("01" * 32),
        case=case_for(True),
        source=source_for(case_for(True)),
        language_context={"milieu_id": "workshop"},
    )
    try:
        said = session.say("Can I help?")
        real = session.read_encounters()[-1]
        forged_status = dict(real)
        forged_status.pop("encounter_id", None)
        forged_status.pop("encounter_hash", None)
        forged_status["status"] = "BOGUS"
        forged_status["strategy"] = "HELP_REFUSE"
        forged_status["encounter_hash"] = digest(forged_status)
        status_episode = session.product._append_episode(
            session.branch_id, "A", "S45_USER_ENCOUNTER",
            session.clock(), forged_status,
        )
        forged_admission = dict(real)
        forged_admission.pop("encounter_id", None)
        forged_admission.pop("encounter_hash", None)
        forged_admission["admission_id"] = ""
        forged_admission["encounter_hash"] = digest(forged_admission)
        admission_episode = session.product._append_episode(
            session.branch_id, "A", "S45_USER_ENCOUNTER",
            session.clock(), forged_admission,
        )
        session.product._checkpoint(session.branch_id, session.clock(), session.world())
        status_read = session.read_event(status_episode["episode_id"])
        admission_read = session.read_event(admission_episode["episode_id"])
        status_s45 = status_read.get("s45") or {}
        admission_s45 = admission_read.get("s45") or {}
        report = {
            "schema": "SOROK_S45_RESEALED_SEMANTIC_REPRO@1",
            "real_user_event_id": said["user_event"]["event_id"],
            "resealed_status_read": status_read.get("status"),
            "resealed_status_s45": status_s45.get("status"),
            "resealed_status_strategy": status_s45.get("strategy"),
            "resealed_admission_read": admission_read.get("status"),
            "resealed_admission_s45": admission_s45.get("status"),
            "resealed_admission_id": admission_s45.get("admission_id"),
            "resealed_status_has_c9": "c9" in status_read,
            "warm_verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()

    cold = S45Session.open(root / "state")
    try:
        cold_status = cold.read_event(status_episode["episode_id"])
        report.update({
            "cold_status_read": cold_status.get("status"),
            "cold_status_s45": (cold_status.get("s45") or {}).get("status"),
            "cold_verify_ok": cold.verify()["ok"],
        })
    finally:
        cold.close()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
