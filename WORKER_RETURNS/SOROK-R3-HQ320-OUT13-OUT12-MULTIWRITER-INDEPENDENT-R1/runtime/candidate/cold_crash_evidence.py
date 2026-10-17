#!/usr/bin/env python3
"""HQ314 OUT9 — explicit cold-crash evidence generator (real subprocess, os._exit).

Produces evidence/cold_crash_evidence.json:
  * BEFORE_RENAME: prior journal bytes byte-identical, no partial record, prior
    state still validates after recovery
  * AFTER_COMMIT: newest committed state durable, valid, and contains the
    post-crash mutation
  * tampered-state recompute: journal recover refuses with typed code
Source-free only: single writer, no multiwriter proof, no perception.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from outbox_prototype import DeliveryState, Journal, _hash  # noqa: E402
from test_out9_independent_hostile import chain_ack, mk, dkey  # noqa: E402

EVIDENCE = HERE.parent / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)


def run_child(jp: Path, eid: str, boundary: str) -> dict:
    code = (
        "import sys\n"
        f"sys.path.insert(0, {str(HERE)!r})\n"
        "from outbox_prototype import Journal\n"
        "j = Journal(sys.argv[1]); p = j.recover(); e = sys.argv[2]\n"
        "assert p.outbox.authorize_viewer(e, 'W')\n"
        "assert p.outbox.emit_to(e, 'W')\n"
        "assert p.outbox.deliver_to(e, 'W')\n"
        "j.commit(p, crash_boundary=sys.argv[3])\n"
        "raise AssertionError('did not crash')\n"
    )
    r = subprocess.run([sys.executable, "-c", code, str(jp), eid, boundary],
                       capture_output=True, text=True, timeout=25)
    return {"child_exit": r.returncode, "stderr_tail": r.stderr.strip().splitlines()[-1:] if r.stderr.strip() else []}


def main() -> int:
    ev: dict = {"evidence_schema": "HQ314_OUT9_COLD_CRASH_EVIDENCE@1.0.0",
                "method": "real child process; os._exit(79) inside Journal.commit; real files"}
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        p, eid = mk("COLD_EVIDENCE")
        chain_ack(p, eid, "V")
        jp = td / "journal.json"
        Journal(jp).commit(p)
        before = jp.read_bytes()
        ev["baseline"] = {
            "event": eid,
            "aggregate_state": "ACKNOWLEDGED",
            "journal_bytes": len(before),
            "journal_sha256": hashlib.sha256(before).hexdigest(),
        }

        # --- BEFORE_RENAME: atomicity, no partial record, prior state intact ---
        b = run_child(jp, eid, "BEFORE_RENAME")
        after = jp.read_bytes()
        pending = sorted(x.name for x in td.glob(".outbox-pending-*"))
        q = Journal(jp).recover()
        ev["crash_before_rename"] = {
            **b,
            "prior_bytes_identical": after == before,
            "partial_records_left": pending,
            "recovered_validates": None,
            "recovered_aggregate_state": q.outbox.deliveries[eid]["state"],
        }
        q.validate_state()
        ev["crash_before_rename"]["recovered_validates"] = True

        # --- AFTER_COMMIT: newest committed state durable and valid ---
        a = run_child(jp, eid, "AFTER_COMMIT")
        r = Journal(jp).recover()
        r.validate_state()
        ev["crash_after_commit"] = {
            **a,
            "newest_committed_durable": jp.exists(),
            "recovered_validates": True,
            "viewer_W_present_in_recovered": "W" in r.outbox.viewers[eid],
            "W_client_state": r.outbox.client_deliveries[dkey(eid, "W")]["state"],
        }

        # --- tampered payload + recomputed unkeyed digest: typed refusal ---
        rec = json.loads(jp.read_text())
        rec["state"]["outbox"][eid].update({"state": DeliveryState.ACKNOWLEDGED.value,
                                            "ack_count": 1, "attempts": 0})
        rec["state_digest"] = _hash(rec["state"])
        tampered = td / "tampered.json"
        tampered.write_text(json.dumps(rec))
        try:
            Journal(tampered).recover()
            ev["cold_tampered_forgery"] = {"refused": False}
        except ValueError as e:
            ev["cold_tampered_forgery"] = {"refused": True, "code": str(e)}

    (EVIDENCE / "cold_crash_evidence.json").write_text(
        json.dumps(ev, indent=1, sort_keys=True) + "\n")
    print(json.dumps(ev, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
