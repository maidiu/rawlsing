#!/usr/bin/env python3
import datetime, hashlib, json, sys
from pathlib import Path
if len(sys.argv) != 3 or sys.argv[1] != "--return":
    raise SystemExit("usage: fixture_child.py --return PATH")
out = Path(sys.argv[2])
payload = {
    "schema": "SOROK_CURRENTNESS_WORKER_RETURN@1",
    "scope": "INFRASTRUCTURE_QUALIFICATION_NOT_ORIGINAL_SCIENCE",
    "produced_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "author_session": "ses_local_fixture_child_r1",
    "author_identity": "LOCAL_FIXTURE_CHILD_PROCESS_NOT_NATIVE",
    "artifact": {
        "kind": "local_sourcefree_fixture",
        "message": "finite controller supervised child produced this hashed return",
    },
}
body = json.dumps(payload, sort_keys=True, indent=2) + "\n"
out.write_text(body, encoding="utf-8")
print(json.dumps({"status": "OK", "return_path": str(out),
                  "sha256": hashlib.sha256(body.encode()).hexdigest()}, sort_keys=True))
