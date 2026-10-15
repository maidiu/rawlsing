"""Trusted test bootstrap in another process, independent of request arguments."""

from pathlib import Path
import json, os, sys
from fixture_owner import FixtureOwnerControl
from pv3_candidate import RequestAPI
import pv2_original_scope_register as OLD

owner = FixtureOwnerControl(policy_path=Path(sys.argv[1]))
api = RequestAPI(owner.client(), owner._attest)
current = {
    ns: owner.client().resolve(ns).__dict__ for ns in ("PV2-ADULT-A", "PV2-ADULT-B")
}
try:
    reading = api.read_current_consumer_material(
        OLD.author_sourcefree_original_scope_register(),
        json.loads(Path(sys.argv[2]).read_text()),
    )
except ValueError as e:
    reading = {"servable": False, "claim": str(e)}
print(
    json.dumps({"pid": os.getpid(), "decisions": current, "old_request_read": reading})
)
