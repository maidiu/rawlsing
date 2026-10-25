import json
import os
import sys
import tempfile
from pathlib import Path

RETURN = Path(os.environ["S45_RETURN"]).resolve()
sys.path.insert(0, str(RETURN))

from s45.bootstrap import install

install()

from s37.harness import case_for, source_for
from s45.fixtures import root_bundle
from s45.session import S45Session


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="s45-encounter-tamper-"))
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
        forged = dict(real)
        forged.pop("encounter_id", None)
        forged.pop("encounter_hash", None)
        forged.update({
            "kind": "SAY",
            "status": "OK",
            "strategy": "HELP_INVITE",
            "native_text": "FORGED ENCOUNTER TEXT",
            "translation_text": "FORGED ENCOUNTER VIEW",
            "user_event_id": "TEST_ONLY_FORGED_USER_EVENT",
            "speech_event_id": "TEST_ONLY_FORGED_SPEECH_EVENT",
            "action_event_id": "",
            "source_event_refs": [{
                "event_id": "TEST_ONLY_FORGED_SOURCE",
                "event_hash": "0" * 64,
                "branch_id": "forged-branch",
            }],
            "access_receipt_ids": ["TEST_ONLY_FORGED_ACCESS"],
        })
        session.product._append_episode(
            session.branch_id, "A", "S45_USER_ENCOUNTER",
            session.clock(), forged,
        )
        session.product._checkpoint(session.branch_id, session.clock(), session.world())
        forged_read = session.read_event("TEST_ONLY_FORGED_USER_EVENT")
        forged_encounter = session.read_encounters()[-1]
        real_receipts = list(real.get("access_receipt_ids") or [])
        for receipt in real_receipts:
            session.revoke_language_access(receipt, reason="TEST_ONLY_S45_TAMPER")
        warm_verify = session.verify()["ok"]
        report = {
            "schema": "SOROK_S45_ENCOUNTER_TAMPER_REPRO@1",
            "real_say_status": said.get("status"),
            "real_speech_event_id": said.get("language", {}).get("speech_event_id"),
            "forged_user_event_id": forged["user_event_id"],
            "forged_speech_event_id": forged["speech_event_id"],
            "forged_encounter_status": forged_encounter.get("status"),
            "forged_encounter_native_text": forged_encounter.get("native_text"),
            "forged_encounter_source_event_refs": forged_encounter.get(
                "source_event_refs"
            ),
            "read_event_forged_status": forged_read.get("status"),
            "read_event_forged_s45_status": (forged_read.get("s45") or {}).get(
                "status"
            ),
            "read_event_forged_has_c9": "c9" in forged_read,
            "real_source_access_revoked": bool(real_receipts),
            "warm_verify_after_tamper_and_revoke": warm_verify,
        }
    finally:
        session.close()

    cold = S45Session.open(root / "state")
    try:
        cold_forged = cold.read_event("TEST_ONLY_FORGED_USER_EVENT")
        report.update({
            "cold_forged_status": cold_forged.get("status"),
            "cold_forged_s45_status": (cold_forged.get("s45") or {}).get(
                "status"
            ),
            "cold_verify_ok": cold.verify()["ok"],
        })
    finally:
        cold.close()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
