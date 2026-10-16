#!/usr/bin/env python3
"""C07P — one process role of the cross-process custody experiment.

Invoked as a REAL subprocess with an independent interpreter and an independent
import of the pinned custody module. Roles:

  phaseA        build escrow through the native public API, persist, emit fingerprint
  phaseB        cold-import the pinned module, restore from the journal, emit fingerprint
  crashA        same as phaseA but raises at a named crash point mid-write-protocol
  continueB     restore then safely continue the authorised lifecycle

Every role prints a single JSON object on stdout between BEGIN/END sentinels so
the parent can parse without trusting human-readable output.
"""
from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "source"))
sys.path.insert(0, str(HERE))

import c07_journal as J  # noqa: E402
import custody_protocol as CP  # noqa: E402


def make_capsule(cid: str, frame: str, stamp: float) -> CP.CustodyCapsule:
    return CP.CustodyCapsule(
        capsule_id=cid, schema_version="1.0", purpose="SOURCEFREE_TEST_ONLY",
        scenario_frame=frame, family_graph_digest="fgd-" + cid,
        content_digest="cd-" + cid, contribution_digest="contrib-" + cid,
        public_projection_digest="ppd-" + cid, hidden_projection_digest="hpd-" + cid,
        lawful_set_digest="lsd-" + cid, coder_rubric_digest="crd-" + cid,
        split_assignment_digest="sad-" + cid, generation_history_digest="ghd-" + cid,
        rejected_alternatives_digest="rad-" + cid, freeze_timestamp=stamp)


def module_provenance() -> dict:
    """Actual imported module identity, not the pinned constant."""
    real = os.path.realpath(CP.__file__)
    data = Path(real).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()
    return {
        "module_file": real,
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob_sha1": blob,
        "bytes": len(data),
        "python": sys.version.split()[0],
        "pid": os.getpid(),
        "cwd": os.getcwd(),
    }


def build_escrow(j: J.EscrowJournal) -> None:
    """The authorised lifecycle, native public API only."""
    j.authorize_holder("custodian-alice", CP.Role.CUSTODIAN)
    j.authorize_holder("runner1", CP.Role.CUSTODIAN)
    j.commit(make_capsule("cap-A", "frame-A", 1000.0))
    j.unblind("cap-A", "custodian-alice")
    j.release("cap-A")
    j.record_exposure("cap-A", "coder-7", "development")


def emit(obj: dict) -> None:
    print("@@BEGIN@@" + json.dumps(obj, sort_keys=True) + "@@END@@")


def main() -> int:
    role = sys.argv[1]
    journal = Path(sys.argv[2])
    out = {"role": role, "provenance": module_provenance()}

    if role == "phaseA":
        j = J.EscrowJournal(journal)
        build_escrow(j)
        out["fingerprint"] = J.escrow_fingerprint(j.state)
        out["journal_records"] = len(J.read_records(journal))
        emit(out)
        return 0

    if role == "crashA":
        point = sys.argv[3]
        j = J.EscrowJournal(journal)
        j.authorize_holder("custodian-alice", CP.Role.CUSTODIAN)
        j.commit(make_capsule("cap-A", "frame-A", 1000.0))
        # This commit delivers a REAL, uncatchable SIGKILL in place, inside the
        # write protocol: no unwinding, no flush, no atexit, no cleanup.
        def killer(where):
            sys.stderr.write(f"C07P SIGKILL at {where}\n")
            sys.stderr.flush()
            os.kill(os.getpid(), signal.SIGKILL)

        j.commit(make_capsule("cap-C", "frame-C", 2000.0), crash=point, kill_at=killer)
        emit({"role": role, "reached_end": True})  # unreachable
        return 0

    if role in ("phaseB", "continueB"):
        # Fresh interpreter, fresh import: nothing is carried in memory.
        j = J.EscrowJournal(journal)
        info = j.restore()
        out["restore"] = info
        out["fingerprint"] = J.escrow_fingerprint(j.state)
        if role == "continueB":
            j.authorize_holder("runner9", CP.Role.CUSTODIAN)
            j.commit(make_capsule("cap-B", "frame-B", 1500.0))
            j.unblind("cap-B", "runner9")
            j.release("cap-B")
            out["continued_fingerprint"] = J.escrow_fingerprint(j.state)
            out["journal_records_after"] = len(J.read_records(journal))
        emit(out)
        return 0

    print(f"unknown role {role!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
