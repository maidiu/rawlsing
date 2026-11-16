"""New R2 correctness probe; separate from the reviewer's unchanged gap oracle."""
from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PROGRAMMA = REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK"
sys.path.insert(0, str(PROGRAMMA))
import operational_currentness_runtime_r1 as rt
import test_operational_currentness_runtime_r1 as t

RESULTS = []


def check(name, fn):
    try:
        fn()
    except Exception as exc:  # noqa: BLE001
        RESULTS.append({"check": name, "pass": False,
                        "detail": type(exc).__name__ + ": " + str(exc)})
        print("FAIL " + name + " :: " + type(exc).__name__ + ": " + str(exc))
    else:
        RESULTS.append({"check": name, "pass": True})
        print("PASS " + name)


def expect_error(code, fn):
    try:
        fn()
    except rt.CurrentnessError as exc:
        if code not in str(exc):
            raise AssertionError("expected " + code + ", got " + str(exc))
        return
    raise AssertionError("expected refusal " + code)


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        config = t.make_sandbox(root)
        live = t.fake_live(config, status_coverage="REF_SHA_ONLY")
        original_fetch = rt.fetch_live_github
        rt.fetch_live_github = lambda cfg: live

        def fresh_observation():
            result = rt.startup(config, reconcile=True)
            _whole, _md, state = rt.read_pair(config)
            stored = state["authenticated_checkpoint"]["live_github"]
            assert stored["source_trust"] == "AUTHENTICATED_LIVE_GITHUB"
            assert stored["fetched_at_utc"] == live["fetched_at_utc"]
            assert stored["expires_at_utc"] == live["expires_at_utc"]
            assert stored["evidence_digest"] == live["evidence_digest"]
            assert result["readout"]["authenticated_github_live"]["fresh"] is True

        def status_gap_visible():
            _whole, _md, state = rt.read_pair(config)
            items, _live = rt.reconciliation_items(config, state)
            assert any("GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE" in
                       i["what_changed"] for i in items)

        def tampered_baseline():
            data = json.loads(config["_baseline"].read_text())
            pr = next(row for row in data if row.get("number") == 1062)
            pr["value"]["head"] = "SIMULATED_LOCAL_BASELINE_ADVANCE"
            config["_baseline"].write_text(json.dumps(data) + "\n")
            items, _live = rt.reconciliation_items(config, rt.read_pair(config)[2])
            assert any("LOCAL_GITHUB_BASELINE_BRANCH_UNAVAILABLE" in
                       i["what_changed"] for i in items)

        def mechanism_not_task_unknown():
            receipt = t.replay_receipt if hasattr(t, "replay_receipt") else None
            receipt = json.loads((REPO / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/"
                                  "fixtures/historical_reviews/B05_1089/REPLAY_RECEIPT.json").read_text())
            receipt.update({"task_id": rt.MECHANISM_ID,
                            "implementation_commit": "a" * 40,
                            "review_commit": "5c83a8321dce70fcc40c8f210af06a9edb1f8999",
                            "author_session": "ses_author_fixture",
                            "reviewer_session": "ses_reviewer_fixture",
                            "source_trust": "REAL_LOCAL_NONAUTHOR_REVIEW",
                            "source_documents": []})
            expect_error("REVIEW_SUPERVISED_RUN_REQUIRED",
                         lambda: rt._validate_review_receipt(
                             config, receipt, replay=False, source=None))

        def fake_task_review_refused():
            receipt = json.loads((REPO / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/"
                                  "fixtures/historical_reviews/B05_1089/REPLAY_RECEIPT.json").read_text())
            receipt.update({"task_id": "C05",
                            "implementation_commit": "4b33b8be1127c2186931a66f23e3a2b05feaf0a6",
                            "review_commit": "24f532de43ab6d1ee8a6480a856ba6c6b56e7f53",
                            "author_session": "ses_author_fixture",
                            "reviewer_session": "ses_reviewer_fixture",
                            "source_trust": "REAL_LOCAL_NONAUTHOR_REVIEW",
                            "source_documents": []})
            expect_error("REVIEW_SUPERVISED_RUN_REQUIRED",
                         lambda: rt._validate_review_receipt(
                             config, receipt, replay=False, source=None))

        def arbitrary_control_refused():
            expect_error("OPERATOR_AUTHORIZATION_UNAVAILABLE",
                         lambda: rt.intake_event(config, t.event(
                             "USER_STOP", payload={"scope": "B02",
                                                   "owner": "fake"})))
            _whole, _md, state = rt.read_pair(config)
            assert state["controls"]["stops"] == []

        def arbitrary_resolution_refused():
            _whole, _md, state = rt.read_pair(config)
            items, _live = rt.reconciliation_items(config, state)
            item = next(i for i in items if i["source_kind"] == "LIVE_GITHUB")
            expect_error("RESOLUTION_AUTHENTICATION_REQUIRED",
                         lambda: rt.intake_event(config, t.event(
                             "RECONCILIATION_RESOLVED",
                             payload={"what_changed": item["what_changed"],
                                      "evidence": "arbitrary text"})))
            expect_error("RESOLUTION_FRESH_OBSERVATION_INVALID",
                         lambda: rt.intake_event(config, t.event(
                             "RECONCILIATION_RESOLVED",
                             payload={"what_changed": item["what_changed"],
                                      "fresh_observation_digest": "0" * 64})))
            rt.intake_event(config, t.event(
                "RECONCILIATION_RESOLVED",
                payload={"what_changed": item["what_changed"],
                         "fresh_observation_digest": live["evidence_digest"]}))
            _whole, _md, state = rt.read_pair(config)
            assert not any(row["what_changed"] == item["what_changed"]
                           for row in state["reconciliation_required"])

        def live_unavailable_typed():
            with tempfile.TemporaryDirectory() as td2:
                config2 = t.make_sandbox(Path(td2))
                def unavailable(cfg):
                    raise rt.CurrentnessError(
                        "LIVE_GITHUB_REF_FETCH_UNAVAILABLE", {"exit": 1})
                rt.fetch_live_github = unavailable
                result = rt.startup(config2, reconcile=True)
                assert any("LIVE_GITHUB_REF_FETCH_UNAVAILABLE" in i["what_changed"]
                           for i in result["reconciliation_required"])
                rt.fetch_live_github = lambda cfg: live

        check("fresh live observation persisted with time/expiry/digest", fresh_observation)
        check("live status/updated source gap remains explicit", status_gap_visible)
        check("tampered local baseline head is not accepted", tampered_baseline)
        check("mechanism review is not TASK_UNKNOWN", mechanism_not_task_unknown)
        check("fake task review without supervised run refused", fake_task_review_refused)
        check("arbitrary STOP/control refused", arbitrary_control_refused)
        check("arbitrary reconciliation text refused; fresh digest resolves", arbitrary_resolution_refused)
        check("live source unavailable is typed HOLD", live_unavailable_typed)
        rt.fetch_live_github = original_fetch
    failed = [row for row in RESULTS if not row["pass"]]
    print(json.dumps({"schema": "SOROK_CURRENTNESS_R2_CORRECTNESS_PROBE@1",
                      "checks": RESULTS, "failed": failed,
                      "verdict": "PASS" if not failed else "FAIL"}, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
