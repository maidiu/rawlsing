"""RA-D S48 source-owner/SCI05 probe. Fake product runner; no provider call."""
from __future__ import annotations
import json, sys, tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
ARCHIVE = RETURN / "isolated_archive_s52c821"
S48 = ARCHIVE / "WORKER_RETURNS" / "SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1"
if str(S48) not in sys.path:
    sys.path.insert(0, str(S48))
from s48.bootstrap import install  # noqa: E402
install()
from s45.fixtures import root_bundle  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s48.session import S48Session  # noqa: E402
from s48.sources import candidate_specs  # noqa: E402

def start(state):
    case = case_for(True)
    return S48Session.start(state, bundle=root_bundle("01" * 32), case=case,
                            source=source_for(case),
                            language_context={"milieu_id": "workshop"})

def envelope(candidate="OTHER_REFUSES_TOOL", self_account=None):
    return {"schema": "S48_PRODUCT_ENVELOPE@1",
            "narrative": "The prior turn is retained.",
            "self_account": self_account,
            "self_account_present": bool(self_account),
            "prospective": ([{"candidate_id": candidate, "rationale": "fixture"}]
                            if candidate else [])}

def runner(env, calls):
    def run(prompt, *, workdir, log_dir, timeout):
        calls.append(1)
        return {"status": "OK", "envelope": dict(env),
                "call_receipt": {"actual_provider_call": False,
                                 "provider_call_count": 1, "step_count": 1},
                "prompt_hash": "fixture"}
    return run

out = {}
state = Path(tempfile.mkdtemp(prefix="ra-d-s48-"))
s = start(state)
try:
    calls = []
    r = s.run_turn(product_runner=runner(envelope(), calls))
    out["unsupported_component"] = {
        "status": r.get("status"), "reason": r.get("reason"),
        "missing_function": r.get("missing_function"),
        "event_ref": r.get("event_ref"),
        "provider_call_count": r.get("provider_call_count"),
        "candidate_specs": candidate_specs(s), "calls": len(calls)}
finally:
    s.close()
state2 = Path(tempfile.mkdtemp(prefix="ra-d-s48-"))
s = start(state2)
try:
    calls = []
    r = s.run_turn(product_runner=runner(
        envelope(self_account="a proposed self-account"), calls))
    out["nonempty_self_account"] = {
        "status": r.get("status"), "reason": r.get("reason"),
        "event_ref": r.get("event_ref"),
        "provider_call_count": r.get("provider_call_count"),
        "calls": len(calls)}
finally:
    s.close()
print(json.dumps(out, indent=2, sort_keys=True))
