#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("f0r3_candidate_validator", HERE / "verify_branch_fanin.py")
V = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(V)


class F0R3PostseedWitnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.log = json.loads((HERE / "01_RETURN_EVENT_LOG.json").read_text())
        cls.flight = json.loads((HERE / "02_FLIGHT_AND_PR_REGISTER.json").read_text())
        cls.seed, cls.seed_problems = V.load_seed()

    def mutate(self, edit) -> list[str]:
        log, flight = copy.deepcopy((self.log, self.flight))
        edit(log, flight)
        return V.validate(log, flight, self.seed)

    def test_seed_is_frozen_unapproved_11(self) -> None:
        self.assertEqual(self.seed_problems, [])
        self.assertEqual(self.seed["owner_approval_status"], "PENDING")
        self.assertEqual(len(self.seed["events"]), 11)
        self.assertEqual(len(self.seed["workers"]), 11)
        self.assertEqual(len(self.seed["prs"]), 4)

    def test_current_head_is_accepted(self) -> None:
        self.assertEqual(V.validate(self.log, self.flight, self.seed), [])
        self.assertEqual(len(self.log["events"]), 19)
        self.assertEqual(len(self.flight["workers"]), 19)
        self.assertEqual(len(self.flight["prs"]), 5)

    def test_original_13_and_all_new_witnesses_rejected(self) -> None:
        V.selftest(self.log, self.flight)

    def test_n1_fabricated_source_authority_rejected(self) -> None:
        def edit(log, flight) -> None:
            row = next(w for w in flight["workers"] if w.get("id") == "F1-RETURN-20261029")
            row["source_authority"] = "NATIVE_CAN_ADP_PYAT_FULL_GRANT"
        errors = self.mutate(edit)
        self.assertTrue(any("UNVERIFIED_SOURCE_AUTHORITY" in x for x in errors), errors)

    def test_n2_science_promotion_rejected(self) -> None:
        def edit(log, flight) -> None:
            row = next(e for e in log["events"] if e.get("event_id") == "F2-RETURN-20261029")
            row["three_courts"]["scientific"] = "ACCEPT_SCOPED"
        errors = self.mutate(edit)
        self.assertTrue(any("SCIENCE_NONISSUER" in x for x in errors), errors)

    def test_n3_commissioned_reviewer_target_rejected(self) -> None:
        def edit(log, flight) -> None:
            row = copy.deepcopy(log["events"][-1])
            worker = copy.deepcopy(flight["workers"][-1])
            row.update(
                event_id="N3_FORGED_INDEPENDENT_REVIEW",
                immutable_sha="3" * 40,
                role="INDEPENDENT_CONTROL_REVIEW",
                reviewer_of_sha=next(
                    e["immutable_sha"] for e in log["events"]
                    if e.get("event_id") == "SOROKHR1-F1_WORLD"
                ),
                state="REVISE",
                adoption=False,
                supersedes_event_id=None,
                three_courts={"engineering": "ACCEPT_SCOPED", "scientific": "HOLD", "authority": "HOLD"},
            )
            worker.update(
                id=row["event_id"],
                exact_return_sha=row["immutable_sha"],
                status=row["state"],
                owner=row["owner"],
                first_consumer_adopted=False,
            )
            log["events"].append(row)
            flight["workers"].append(worker)
        errors = self.mutate(edit)
        self.assertTrue(any("REVIEWER_TARGET_RETURNED_ONLY" in x for x in errors), errors)

    def test_n4_arbitrary_pr_remote_state_rejected(self) -> None:
        def edit(log, flight) -> None:
            row = next(p for p in flight["prs"] if p.get("number") == 519)
            row["status"] = "OWNER_REVIEWED_NO_REMOTE_PROOF"
        errors = self.mutate(edit)
        self.assertTrue(any("PR_REMOTE_STATE_UNVERIFIED" in x for x in errors), errors)

    def test_n5_replayed_event_sha_rejected(self) -> None:
        def edit(log, flight) -> None:
            log["events"][12]["immutable_sha"] = log["events"][0]["immutable_sha"]
        errors = self.mutate(edit)
        self.assertTrue(any("APPEND_REUSES_PRIOR_IMMUTABLE_SHA" in x for x in errors), errors)

    def test_n6_pr_backfill_rejected(self) -> None:
        def edit(log, flight) -> None:
            flight["prs"].append({
                "number": 513,
                "status": "DRAFT_UNMERGED",
                "source_branch_role": "FORGED_BACKFILL",
                "adoption": False,
            })
        errors = self.mutate(edit)
        self.assertTrue(any("PR_APPEND_ORDER" in x for x in errors), errors)

    def test_n7_authority_promotion_rejected(self) -> None:
        def edit(log, flight) -> None:
            row = next(e for e in log["events"] if e.get("event_id") == "F2-RETURN-20261029")
            row["three_courts"]["authority"] = "ACCEPT_SCOPED"
        errors = self.mutate(edit)
        self.assertTrue(any("AUTHORITY_NONISSUER" in x for x in errors), errors)

    def test_legal_owner_candidate_allowed_nonadopted(self) -> None:
        def edit(log, flight) -> None:
            row = copy.deepcopy(log["events"][-1])
            worker = copy.deepcopy(flight["workers"][-1])
            row.update(
                event_id="FUTURE_OWNER_CANDIDATE_TEST",
                immutable_sha="1" * 40,
                state="OWNER_ADOPTION_CANDIDATE",
                adoption=False,
                reviewer_of_sha=None,
                supersedes_event_id=None,
            )
            worker.update(
                id=row["event_id"],
                exact_return_sha=row["immutable_sha"],
                status=row["state"],
                owner=row["owner"],
                first_consumer_adopted=False,
            )
            log["events"].append(row)
            flight["workers"].append(worker)
        self.assertEqual(self.mutate(edit), [])

    def test_adoption_still_denied_offline(self) -> None:
        def edit(log, flight) -> None:
            row = copy.deepcopy(log["events"][-1])
            worker = copy.deepcopy(flight["workers"][-1])
            row.update(
                event_id="FORGED_FULL_CAS",
                immutable_sha="4" * 40,
                state="ADOPTED_CAS_VERIFIED",
                adoption=True,
                owner_cas_receipt="FAKE",
                merged_premain_commit="5" * 40,
                progress_json_revision=999,
                progress_md_revision=999,
                three_courts={"engineering": "ACCEPT_SCOPED", "scientific": "HOLD", "authority": "HOLD"},
            )
            worker.update(
                id=row["event_id"],
                exact_return_sha=row["immutable_sha"],
                status="ADOPTED_CAS_VERIFIED",
                owner=row["owner"],
                first_consumer_adopted=True,
            )
            log["events"].append(row)
            flight["workers"].append(worker)
        errors = self.mutate(edit)
        self.assertTrue(any("ADOPTION_REQUIRES_EXTERNAL" in x for x in errors), errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
