#!/usr/bin/env python3
"""C07I — reviewer's own process roles. Independent of C07P's c07_worker.py.

Uses only the public `EscrowState` API and the pinned OC6 module. Emits one JSON
object between sentinels so the parent parses structure, not prose.

Roles:
  build    process A — construct an authorised lifecycle and persist it
  recover  process B — cold import, restore, report identity + measured time drift
  continue process B — restore then continue the lifecycle
  crash    die by real SIGKILL at a named write-protocol point
"""
from __future__ import annotations

import hashlib
import json
import os
import signal
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "source"))
sys.path.insert(0, str(HERE))

import c07_journal as J          # the adapter under review
import custody_protocol as CP    # the pinned native module


def cap(cid: str, frame: str, stamp: float) -> CP.CustodyCapsule:
    return CP.CustodyCapsule(
        capsule_id=cid, schema_version="1.0", purpose="SOURCEFREE_TEST_ONLY",
        scenario_frame=frame, family_graph_digest="fgd-" + cid,
        content_digest="cd-" + cid, contribution_digest="contrib-" + cid,
        public_projection_digest="ppd-" + cid, hidden_projection_digest="hpd-" + cid,
        lawful_set_digest="lsd-" + cid, coder_rubric_digest="crd-" + cid,
        split_assignment_digest="sad-" + cid, generation_history_digest="ghd-" + cid,
        rejected_alternatives_digest="rad-" + cid, freeze_timestamp=stamp)


def provenance() -> dict:
    real = os.path.realpath(CP.__file__)
    data = Path(real).read_bytes()
    return {
        "module_file": real,
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob_sha1": hashlib.sha1(
            b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest(),
        "bytes": len(data),
        "python": sys.version.split()[0],
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "argv_role": sys.argv[1] if len(sys.argv) > 1 else None,
    }


def identity(state: CP.EscrowState) -> dict:
    """Reviewer's own identity probe — not C07P's fingerprint function."""
    return {
        "committed_ids": sorted(state.committed),
        "seals": {cid: CP.capsule_envelope_commitment(c)
                  for cid, c in sorted(state.committed.items())},
        "capsule_18_fields": {cid: {k: getattr(c, k) for k in J.CAPSULE_FIELDS}
                              for cid, c in sorted(state.committed.items())},
        "unblinded": {cid: st["holder"] for cid, st in sorted(state.unblinded.items())},
        "released": sorted(state.released),
        "exposures": sorted([r["capsule_id"], r["exposed_to"], r["purpose"]]
                            for r in state.exposure_log),
        "holders": {k: (v.value if isinstance(v, CP.Role) else repr(v))
                    for k, v in sorted(state.holder_roles.items())},
        "ledger": [(r["seq"], r["op"], r.get("capsule_id")) for r in state.ledger],
        "integrity": state.verify_ledger_integrity(),
        # escrow event timestamps, measured rather than assumed
        "escrow_unblinded_at": {cid: st["unblinded_at"]
                                for cid, st in sorted(state.unblinded.items())},
        "escrow_ledger_ts": [r["ts"] for r in state.ledger],
    }


def emit(obj: dict) -> None:
    print("@@C07I@@" + json.dumps(obj, sort_keys=True) + "@@END@@")


def lifecycle(j: J.EscrowJournal, cid: str, frame: str, stamp: float, holder: str) -> None:
    j.authorize_holder("custodian-zoe", CP.Role.CUSTODIAN)
    j.commit(cap(cid, frame, stamp))
    j.unblind(cid, holder)
    j.release(cid)
    j.record_exposure(cid, "coder-reviewer", "development")


def main() -> int:
    role = sys.argv[1]
    journal = Path(sys.argv[2])
    out = {"role": role, "provenance": provenance()}

    if role == "build":
        j = J.EscrowJournal(journal)
        lifecycle(j, "cap-A", "frame-A", 1111.0, "custodian-zoe")
        out["identity"] = identity(j.state)
        out["journal_head"] = J.verify_chain(J.read_records(journal))["head"]
        out["journal_records"] = len(J.read_records(journal))
        out["journal_bytes"] = journal.stat().st_size
        emit(out)
        return 0

    if role == "recover":
        j = J.EscrowJournal(journal)
        out["restore"] = j.restore()
        out["identity"] = identity(j.state)
        recs = J.read_records(journal)
        out["journal_head"] = J.verify_chain(recs)["head"]
        # journal-side timestamps, for direct comparison against the escrow's own
        out["journal_unblinded_at"] = [r["payload"]["unblinded_at"]
                                        for r in recs if r["kind"] == "UNBLIND"]
        out["journal_exposure_ts"] = [r["payload"]["exposure_ts"]
                                      for r in recs if r["kind"] == "EXPOSURE"]
        emit(out)
        return 0

    if role == "continue":
        j = J.EscrowJournal(journal)
        out["restore"] = j.restore()
        out["identity_after_restore"] = identity(j.state)
        lifecycle(j, "cap-B", "frame-B", 2222.0, "custodian-zoe")
        out["identity_after_continue"] = identity(j.state)
        out["journal_records_after"] = len(J.read_records(journal))
        emit(out)
        return 0

    if role == "crash":
        point = sys.argv[3]
        j = J.EscrowJournal(journal)
        j.authorize_holder("custodian-zoe", CP.Role.CUSTODIAN)
        j.commit(cap("cap-A", "frame-A", 1111.0))

        def killer(where: str) -> None:
            sys.stderr.write(f"C07I SIGKILL at {where}\n")
            sys.stderr.flush()
            os.kill(os.getpid(), signal.SIGKILL)

        if point == "0_before_tmp_fsync":
            # The adapter exposes NO crash hook before the temp file is fsynced,
            # so this point is reached WITHOUT editing it: os.fsync is shadowed in
            # this worker only, and the process dies the instant the adapter first
            # asks for a flush. The temp file exists but is not fsynced.
            real_fsync = os.fsync

            def killing_fsync(fd):
                killer("0_before_tmp_fsync")
                return real_fsync(fd)

            os.fsync = killing_fsync
            J.append_records(journal, [{"kind": "AUTHORIZE",
                                        "payload": {"person_id": "x", "role": "CUSTODIAN"}}],
                             crash=None)
            emit({"role": role, "unreachable": True})
            return 0

        j.commit(cap("cap-C", "frame-C", 3333.0), crash=point, kill_at=killer)
        emit({"role": role, "unreachable": True})
        return 0

    print(f"unknown role {role!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
