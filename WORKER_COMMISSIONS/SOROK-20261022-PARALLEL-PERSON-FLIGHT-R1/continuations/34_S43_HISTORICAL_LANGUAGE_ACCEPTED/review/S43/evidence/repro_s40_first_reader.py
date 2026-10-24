import json
import os
import sys
import tempfile
from pathlib import Path

RETURN = Path(os.environ["S43_RETURN"]).resolve()
sys.path.insert(0, str(RETURN))

from s43.bootstrap import install

install()

from s43.session import S43Session
from s37.harness import case_for, source_for


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="s43-first-reader-"))
    session = S43Session.start(
        root / "state", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        first = session.read_events()[0]
        base = session.read_event(first["e1_event_id"])
        try:
            session.read_s43_event(first["e1_event_id"])
            single = {"status": "OK"}
        except Exception as exc:
            single = {
                "status": "REFUSED",
                "type": type(exc).__name__,
                "code": getattr(exc, "code", None),
                "error": str(exc),
            }
        try:
            events = session.read_s43_events()
            all_read = {
                "status": "OK",
                "count": len(events),
            }
        except Exception as exc:
            all_read = {
                "status": "REFUSED",
                "type": type(exc).__name__,
                "code": getattr(exc, "code", None),
                "error": str(exc),
            }
        report = {
            "schema": "SOROK_S43_S40_FIRST_READER_REPRO@1",
            "first_event_ordinal": first["event_ordinal"],
            "first_event_id": first["e1_event_id"],
            "base_s42_read_status": base["status"],
            "s43_single_read": single,
            "s43_all_read": all_read,
            "verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
