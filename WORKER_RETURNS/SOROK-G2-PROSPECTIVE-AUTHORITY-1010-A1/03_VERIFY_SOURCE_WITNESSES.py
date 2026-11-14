#!/usr/bin/env python3
"""Read-only source witness check. PASS does not prove G2 implementation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CUT = "44e664eff316e0f644b1326bf5d7b1d23594c179"
LOG = "WORKER_RETURNS/SOROK-D03-E01-1010-NATIVE-EXEC-R1/evidence/integration-run-2-with-real-pending.log"
LOG_BLOB = "1d2d27dd3a4ad3982ce7e283feed0bc616a9352c"


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + bytes((0,)) + data
    ).hexdigest()


def local(path: str) -> Path:
    if not isinstance(path, str) or not path or path.startswith("/"):
        raise AssertionError("INVALID_PATH")
    file = (REPO / path).resolve()
    if not file.is_relative_to(REPO.resolve()) or not file.is_file():
        raise AssertionError("SOURCE_PATH_INVALID:" + path)
    return file


def check() -> None:
    manifest = json.loads((HERE / "02_EXECUTED_SOURCE_WITNESSES.json").read_text())
    contract = json.loads((HERE / "01_ISSUANCE_REQUEST.json").read_text())
    if manifest["source_cut"] != CUT or contract["source_cut"] != CUT:
        raise AssertionError("SOURCE_CUT_CHANGED")
    if (contract["disposition"] != "NOT_ISSUED__G2_HELD"
            or contract["not_native_science"] is not True):
        raise AssertionError("UNAUTHORIZED_AUTHORITY_PROMOTION")
    if contract["schema"] != "SOROK_G2_MINIMUM_SOURCE_OWNER_ISSUANCE_REQUEST@1":
        raise AssertionError("CONTRACT_SCHEMA_CHANGED")
    if set(contract["required_receipts"]) != {
        "candidate_set", "candidate_entry", "evaluation_decision",
        "p3_plan_binding", "p2_selected_event_binding", "evaluated_inaction",
        "adp_optional",
    }:
        raise AssertionError("ISSUANCE_RECEIPTS_CHANGED")
    if set(contract["allowed_decisions"]) != {
        "SELECTED_ACTOR_ACTIVITY", "EVALUATED_INACTION",
        "DEFERRED_UNRESOLVED", "REFUSED_UNLAWFUL",
    }:
        raise AssertionError("DECISION_VOCABULARY_CHANGED")
    rows = manifest["checks"]
    if len(rows) != 10 or len({r["path"] for r in rows}) != len(rows):
        raise AssertionError("SOURCE_WITNESS_SET_CHANGED")
    assertions = 0
    for row in rows:
        data = local(row["path"]).read_bytes()
        if blob_sha(data) != row["git_blob_sha"]:
            raise AssertionError("SOURCE_BLOB_MISMATCH:" + row["path"])
        text = data.decode("utf-8")
        for assertion in row["assertions"]:
            if assertion["found"] is not True or assertion["fragment"] not in text:
                raise AssertionError("SOURCE_ASSERTION_FAILED:" + row["id"])
            assertions += 1
    if assertions != 22:
        raise AssertionError("SOURCE_ASSERTION_COUNT_CHANGED")
    log = local(LOG).read_bytes()
    if blob_sha(log) != LOG_BLOB or b"37 passed in 570.69s" not in log:
        raise AssertionError("INHERITED_37_PASS_LOG_CHANGED")
    print("S0_S1_SOURCE_WITNESSES_PASS: 10 exact blobs / 22 checks / inherited 37-pass log")
    print("G2_HELD: rule issuance, plan mapping, P2 selection and later actor consumer unproved")


if __name__ == "__main__":
    try:
        check()
    except (AssertionError, OSError, ValueError, KeyError, UnicodeError) as exc:
        print("S0_S1_SOURCE_WITNESSES_FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
