#!/usr/bin/env python3
"""Cold two-process BP1 historical actor → C9 positive receipt.

Usage:
  python3 tools/bp1_cold_probe.py build <db> <receipt.json>
  python3 tools/bp1_cold_probe.py verify <db> <receipt.json>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
for _path in (
    RETURN / "candidate",
    RETURN / "vendor/g18/candidate",
    RETURN / "vendor/c9r",
    RETURN / "vendor/c9r/runtime/native",
):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from bp1 import build_two_actor_life, run_bp1_c9  # noqa: E402
from bp1.c9_bridge import ACTUATOR, EXPECTED_ACT, OCCURRENCE  # noqa: E402
from candidate import (  # noqa: E402
    CandidateStore,
    LaterActionConsumer,
    LaterActionStatus,
    admit_performed_action,
    make_performed_action_receipt,
    read_target_for_later_action,
)


def build(db: Path, receipt_path: Path):
    life = build_two_actor_life()
    with CandidateStore(db) as store:
        result = run_bp1_c9(life, store)
        record = store.read_target_state(result.target_id)
    payload = {
        "schema": "BP1_COLD_POSITIVE@1",
        "life": life.receipt(),
        "c9": result.receipt(),
        "target_id": result.target_id,
        "committed_record": record,
    }
    receipt_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(dict(committed=result.committed,
                          target_id=result.target_id,
                          state_hash=result.state_hash), sort_keys=True))
    return 0


def verify(db: Path, receipt_path: Path):
    saved = json.loads(receipt_path.read_text())
    life = build_two_actor_life()
    fresh = life.receipt()
    assert fresh["state_hashes"] == saved["life"]["state_hashes"]
    assert fresh["history_hashes"] == saved["life"]["history_hashes"]
    assert fresh["shared_objective_hash"] == saved["life"]["shared_objective_hash"]
    assert fresh["material_event_ref"] == saved["life"]["material_event_ref"]
    c9 = saved["c9"]
    assert c9["committed"] is True and c9["e2_admitted"] is True
    with CandidateStore(db) as store:
        record = store.read_target_state(saved["target_id"])
        assert record == saved["committed_record"]
        read = read_target_for_later_action(
            store,
            consumer=LaterActionConsumer("TEST_ONLY_BP1_E2_READER",
                                         "committed_target_state"),
            middle_state_id=saved["target_id"],
            as_of=int(c9["later_as_of"]),
            commit_time=int(c9["target_commit_time"]),
            expected_actor_id=c9["actor_id"],
        )
        assert read.status is LaterActionStatus.ACTION_ADMISSION_HELD
        assert read.state_hash == c9["consumed_state_hash"]
        receipt = make_performed_action_receipt(
            actor_id=c9["actor_id"],
            act=EXPECTED_ACT,
            actuator_ref=ACTUATOR,
            occurrence_ref=OCCURRENCE,
            action_time=int(c9["later_as_of"]) + 1,
            consumed_state_hash=read.state_hash,
            target_commit_time=int(c9["target_commit_time"]),
        )
        admitted = admit_performed_action(
            owner_receipt=receipt,
            expected_actor_id=c9["actor_id"],
            expected_act=EXPECTED_ACT,
            consumed_state_hash=read.state_hash,
            as_of=int(c9["later_as_of"]) + 2,
            target_commit_time=int(c9["target_commit_time"]),
        )
        assert admitted.admitted is True
    print(json.dumps(dict(cold_record_equal=True,
                          cold_read_state_hash=read.state_hash,
                          cold_e2_admitted=True), sort_keys=True))
    return 0


def main():
    mode, db, receipt = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    if mode == "build":
        return build(db, receipt)
    if mode == "verify":
        return verify(db, receipt)
    raise SystemExit("mode must be build or verify")


if __name__ == "__main__":
    raise SystemExit(main())
