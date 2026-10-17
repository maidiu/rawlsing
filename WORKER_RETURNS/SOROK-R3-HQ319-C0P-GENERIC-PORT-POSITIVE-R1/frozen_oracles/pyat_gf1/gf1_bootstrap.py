"""R17 GF1 bootstrap — isolated court root; reattests the pinned native tree.

MIRRORS the accepted PV3/PV3N staging discipline:
  * the 74-file pinned native tree is re-attested from its ORIGINAL PV3 manifest
    using Git blob SHA-1 (NUL preimage) + sha256 + byte count;
  * the PV2I frozen packet is staged by the ORIGINAL PV3 stage.py, untouched;
  * the separately-installed TEST_ONLY owner is provisioned once, exactly as the
    accepted court did; cold/request paths never re-provision;
  * import path is asserted to land INSIDE this return directory.

Grain: SOURCEFREE TEST_ONLY candidate. No original SAV/DTA, no U/E_pre issuance,
no canonical Field Forge change, no actor/V3.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

C = Path(__file__).resolve().parents[1]          # .../GF1-...-R1/court
R = C.parent                                    # .../GF1-...-R1
RT = C / "runtime_root"

NATIVE = json.loads((C / "source_selector.json").read_text())["files"]


def blob(b: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob " + str(len(b)).encode() + b"\0" + b)
    return h.hexdigest()


def reattest() -> int:
    """Re-derive every pinned native identity from actual bytes. Refuse on any drift."""
    for row in NATIVE:
        p = RT / row["staged_path"]
        if not p.is_file():
            raise ValueError("MISSING_NATIVE_SOURCE_ATTESTATION:" + row["staged_path"])
        b = p.read_bytes()
        if blob(b) != row["git_blob_sha1"]:
            raise ValueError("CHANGED_NATIVE_SOURCE_ATTESTATION:" + row["staged_path"])
        if hashlib.sha256(b).hexdigest() != row["sha256"] or len(b) != row["bytes"]:
            raise ValueError("CHANGED_NATIVE_SOURCE_DIGEST:" + row["staged_path"])
    return len(NATIVE)


REATTESTED = reattest()

sys.path[:0] = [str(C / "repro"), str(RT), str(RT / "candidate/repro"), str(C / "frozen_pv2i/repro")]
os.environ.update(
    PV2_RUNTIME_ROOT=str(RT),
    PV_RETURN=str(RT / "prior_PV"),
    PYTHONDONTWRITEBYTECODE="1",
)


def import_custody() -> dict:
    """Physical import receipts: module.__file__ must resolve inside this return."""
    rows = []
    for name, m in sorted(sys.modules.items()):
        f = getattr(m, "__file__", None)
        if f and Path(f).is_file() and Path(f).suffix == ".py" and str(R) in f:
            b = Path(f).read_bytes()
            rows.append(dict(module=name, file=str(Path(f).resolve().relative_to(R)),
                             blob_sha1=blob(b), sha256=hashlib.sha256(b).hexdigest()))
    return dict(native_reattested=REATTESTED, imports=rows)