import datetime
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(root / "runtime_code"))
from rawlsing_next.as4.loader import HB04FreezeError
from rawlsing_next.as4.run_candidate import run_candidate

try:
    run_candidate(candidate="A", workdir=root / "production_gate_probe_workdir")
except HB04FreezeError as exc:
    message = str(exc)
else:
    raise AssertionError("the fixture-gated production entry unexpectedly executed")

assert message == (
    "production source preparation is separately gated; B21 may execute only "
    "the explicit governed bounded fixture"
)
receipt = {
    "schema": "RAWLSING_EE_R8B_PRODUCTION_ENTRYPOINT_GATE_PROBE@1.0.0",
    "status": "PROVED_BLOCKED_BY_EXACT_OWNER_ENTRYPOINT_GATE",
    "executed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "probe_driver_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    "candidate": "A",
    "bounded_fixture": False,
    "exception_type": "HB04FreezeError",
    "message": message,
    "source_opened": False,
    "candidate_semantic_execution": False,
}
(root / "production_gate_probe_receipt.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
print(receipt["status"])
