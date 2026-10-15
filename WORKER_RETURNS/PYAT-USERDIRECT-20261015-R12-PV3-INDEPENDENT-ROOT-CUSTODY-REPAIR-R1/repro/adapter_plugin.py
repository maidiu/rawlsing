"""Load unchanged PV2I cases with a declared new-interface adapter."""

from pathlib import Path
import pytest, copy, json, hashlib
import pv2i_adapter as A
import common as C
import deployment as D
from pv2i_adapter import adapt_common

R = Path(__file__).resolve().parents[1]
adapt_common(C, R)
BASE_OWNER, BASE_API = D.owner, D.api
INITIAL = copy.deepcopy(D.owner._state)


@pytest.fixture(autouse=True)
def isolated_owner_control(request):
    # Trusted harness isolation; never supplied by any request/register argument.
    A.ACTIVE_CASE = request.node.name
    D.owner, D.api = BASE_OWNER, BASE_API
    D.owner._state = copy.deepcopy(INITIAL)
    D.owner._save_policy()
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    p = R / "observations/pv2i_case_execution.json"
    rows = json.loads(p.read_text()) if p.exists() else []
    rows = [r for r in rows if r["name"] != item.name]
    event = {
        "name": item.name,
        "raw_outcome": report.outcome,
        "api_events": [e for e in A.EVENTS if e["case"] == item.name],
    }
    if not event["api_events"] and any(t in item.name for t in ("cold_process", "journal_result", "checkpoint_receipt", "fresh_process", "missing_source")):
        event["separate_process_evidence"] = {
            f: hashlib.sha256((R / "observations" / f).read_bytes()).hexdigest()
            for f in (
                "cold_court.json",
                "cold_actual_result_ref_tamper.json",
                "cold_checkpoint_payload_tamper.json",
                "cold_forged_current_grant.json",
            )
        }
    if not event["api_events"] and "separate_process_evidence" not in event:
        event["actual_baseline_evidence"] = hashlib.sha256((R/"observations/physical_baseline.json").read_bytes()).hexdigest()
    rows.append(event)
    p.write_text(json.dumps(rows, indent=2) + "\n")
