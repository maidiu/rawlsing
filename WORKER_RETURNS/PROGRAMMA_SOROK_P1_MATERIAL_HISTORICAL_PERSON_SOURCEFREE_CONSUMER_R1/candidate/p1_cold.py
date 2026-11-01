"""Cold-process reader for P1 histories; used by the actual trajectory runner."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEPS = ROOT / "deps"
os.environ.setdefault("M35_JOIN_E_RETURN", str(DEPS / "join_e"))
if str(DEPS / "m35") not in sys.path:
    sys.path.insert(0, str(DEPS / "m35"))
import install  # noqa: E402
install.install()

from joined.session import JoinedSession  # noqa: E402
from joined.refusal import RefusalSession  # noqa: E402
from p1_no_access import open_no_access  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=("joined", "refusal", "no_access"), required=True)
    ap.add_argument("--state", required=True)
    args = ap.parse_args()
    process = {"executable": sys.executable, "pid": os.getpid()}
    if args.kind == "joined":
        s = JoinedSession.open(args.state)
        try:
            out = {"ok": True, "process": process, "verify": s.verify(),
                   "status": s.status(), "source": s.product.source,
                   "branch": s.branch_id, "state_root": str(s.state_root)}
        finally:
            s.close()
    elif args.kind == "refusal":
        s = RefusalSession.open(args.state)
        try:
            out = {"ok": True, "process": process, "verify": s.verify(),
                   "status": s.status(), "source": s.product.source,
                   "branch": s.branch_id, "state_root": str(s.state_root)}
        finally:
            s.close()
    else:
        p, sidecar = open_no_access(args.state)
        try:
            out = {"ok": True, "process": process, "view": p.no_access_view(),
                   "c12": p.c12_verify("root"), "sidecar": sidecar,
                   "state_root": str(p.root)}
        finally:
            p.close()
    print(json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
