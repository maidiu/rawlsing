"""Sourcefree regressions for session-locator append-only and G1-G6 custody."""
from __future__ import annotations

import copy
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_session_locators as locator  # noqa: E402

REGISTRY = json.loads((HERE / "SESSION_LOCATORS.json").read_text())


def _hard(issues):
    return [item for item in issues if "WARN_" not in item]


QF2_ROW = {
    "registry_id": "RETURN-QF2-R2",
    "revision": 2,
    "supersedes": "DISPATCH-QF2-R1",
    "commission_id": "QF2",
    "branch": "integration/sorok-r3-qf2-conditional-qualified-fanin-20261030",
    "sealed_commission_sha": "cba6b56ec76445a768c25e643d44f89040685f01",
    "actual_commission_head": "187fdd11963163dab03c7b061e20067ea1f99134",
    "status": "RETURNED",
    "device": "oldMac",
    "device_evidence": (
        "local-machine-name-verified: scutil --get ComputerName returned oldMac; "
        "hostname Matthews-MBP.lan"),
    "harness": "Codex",
    "agent_name": "Codex",
    "agent_id": None,
    "agent_id_evidence": (
        "Separate provider agent ID not exposed; /root is task path, session ID separate"),
    "agent_role": (
        "QF2 conditional gate verifier and STOP-return author; "
        "original-owner-delegate authority not established"),
    "agent_mode": "Default",
    "model_provider": "OpenAI",
    "model_id": "UNKNOWN",
    "model_family_evidence": (
        "System identifies GPT-6 family; exact model selector not exposed"),
    "reasoning_effort_requested": "HIGH (commission recommendation)",
    "reasoning_effort_verified": "UNVERIFIED",
    "evidence_source": (
        "Local tool host name, Codex list_threads title/id/cwd; "
        "no model or quota UI telemetry"),
    "session_name": "Review QF2 Sorok fan-in",
    "session_name_evidence": "INSPECTED_IN_APP",
    "suggested_session_name": (
        "RAWLSING QF2 | QF2 conditional review-qualified | oldMac | Codex"),
    "session_id": "01a18e10-6391-7a52-8950-dec3073e1800",
    "session_url": None,
    "session_locator_type": "APP_SESSION_ID",
    "worktree_path": "/Users/matthewsmith/.codex/worktrees/ba29/Rawlsing",
    "editor_workspace": "Rawlsing",
    "original_implementing_session": {
        "registry_id": "HISTORICAL-SOROK-QF1-R1",
        "revision": 1,
        "commission_id": "SOROK-QF1",
        "branch": "integration/sorok-qualified-inheritance-fanin-owner-court-r1",
        "status": "RETURNED",
        "device": "UNKNOWN",
        "device_evidence": "LOCAL_MAC_REPORTED_WHICH_MACHINE_UNVERIFIED",
        "harness": "OpenCode",
        "model_id": "opencode-go/deepseek-v4.1-flash",
        "session_name": None,
        "session_id": None,
        "session_url": None,
        "session_locator_type": "UNKNOWN",
        "return_sha": "68e49f92d5b9f0859d08847ee108684ddfd193ca",
        "return_directory": "WORKER_RETURNS/SOROK-QF1-ORIGINAL-OWNER-QUALIFIED-CODE-FANIN-R1",
        "confirmed_by": "WORKER",
        "machine_claim": "SELF_REPORTED",
        "locator_status": "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
    },
    "is_resumption": False,
    "parent_session": None,
    "reviewer_session": None,
    "post_return_independent_review_owner": (
        "Incumbent HQ + separate reviewer; NOT_ASSIGNED"),
    "return_sha": None,
    "return_sha_resolution": (
        "Final exact SHA externally read back after push; PRE-MAIN owner "
        "appends central revision through own authorized CAS"),
    "return_directory": "WORKER_RETURNS/QF2-R3",
    "collected_at": "2026-10-30T18:31:33.157110+00:00",
    "confirmed_by": "WORKER",
    "confirmation_evidence": "OPERATOR_SELF_REPORT",
    "machine_claim": "SELF_REPORTED",
    "locator_status": "APP_TITLE_AND_SESSION_ID_VERIFIED",
    "no_autonomous_harness_or_model_switch": True,
    "source_execution_permission": (
        "Read-only private Git and own return publication only exercised; "
        "original-source/native/production NOT_RUN"),
    "source_authority": False,
    "adoption": False,
}


def _with_qf2():
    obj = copy.deepcopy(REGISTRY)
    obj["records"].append(copy.deepcopy(QF2_ROW))
    return obj


def _append_new_commission():
    obj = copy.deepcopy(REGISTRY)
    row = copy.deepcopy(obj["records"][-1])
    row.update({
        "registry_id": "LOC2-R4-NEW-R1",
        "revision": 1,
        "supersedes": None,
        "commission_id": "LOC2-R4-NEW",
        "status": "SEALED_NOT_LAUNCHED",
        "confirmed_by": "UNVERIFIED",
        "confirmation_evidence": "UNVERIFIED",
        "machine_claim": "UNVERIFIED",
        "locator_status": "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
        "return_sha": None,
    })
    obj["records"].append(row)
    return obj


class LocatorIntegrityR2(unittest.TestCase):
    def test_current_registry_and_prefix(self):
        self.assertEqual(_hard(locator.check(REGISTRY)), [])
        self.assertEqual(_hard(locator.check(REGISTRY, previous=REGISTRY)), [])

    def test_qf2_revision_is_representable_without_source_authority(self):
        obj = _with_qf2()
        self.assertEqual(_hard(locator.check(obj, previous=REGISTRY)), [])
        self.assertFalse(QF2_ROW["source_authority"])
        self.assertFalse(QF2_ROW["adoption"])
        self.assertEqual(QF2_ROW["device"], "oldMac")
        self.assertEqual(QF2_ROW["harness"], "Codex")
        self.assertEqual(QF2_ROW["agent_name"], "Codex")
        self.assertEqual(QF2_ROW["agent_mode"], "Default")
        self.assertEqual(QF2_ROW["session_name"], "Review QF2 Sorok fan-in")
        self.assertEqual(QF2_ROW["session_id"],
                         "01a18e10-6391-7a52-8950-dec3073e1800")
        self.assertFalse(any("QF2" in item for item in locator.check(obj)))

    def test_qf2_cannot_grant_source_authority(self):
        obj = copy.deepcopy(REGISTRY)
        row = copy.deepcopy(QF2_ROW)
        row["source_authority"] = True
        obj["records"].append(row)
        self.assertTrue(any("LOCATOR_CANNOT_GRANT_AUTHORITY" in item
                            for item in locator.check(obj, previous=REGISTRY)))

    def test_g1_historical_rewrite_is_rejected(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"][0]["device_evidence"] = "rewritten after return"
        self.assertTrue(any("HISTORICAL_ROW_REWRITTEN" in item
                            for item in locator.check(obj, previous=REGISTRY)))

    def test_g1_historical_delete_is_rejected(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"].pop(0)
        self.assertTrue(any("HISTORICAL_ROW_MISSING" in item
                            or "HISTORICAL_ROWS_TRUNCATED" in item
                            for item in locator.check(obj, previous=REGISTRY)))

    def test_g1_reorder_is_rejected(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"].insert(0, obj["records"].pop(1))
        self.assertTrue(any("HISTORICAL_ROW_REWRITTEN" in item
                            for item in locator.check(obj, previous=REGISTRY)))

    def test_g1_legitimate_append_revision(self):
        self.assertEqual(_hard(locator.check(_with_qf2(), previous=REGISTRY)), [])

    def test_g1_legitimate_new_commission(self):
        self.assertEqual(_hard(locator.check(_append_new_commission(),
                                             previous=REGISTRY)), [])

    def test_g1_revision_gap_and_missing_supersedes(self):
        obj = _with_qf2()
        obj["records"][-1]["revision"] = 3
        self.assertTrue(any("NON_APPEND_REVISION" in item
                            for item in locator.check(obj, previous=REGISTRY)))
        obj = _with_qf2()
        obj["records"][-1].pop("supersedes")
        self.assertTrue(any("SUPERSEDES" in item
                            for item in locator.check(obj, previous=REGISTRY)))

    def test_g2_fabricated_observed_title(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"][0].update({
            "session_name": "Fabricated observed title",
            "suggested_session_name": "a different proposed title",
            "session_locator_type": "APP_TITLE",
            "confirmed_by": "WORKER",
        })
        found = locator.check(obj)
        self.assertTrue(any("SESSION_NAME_EVIDENCE_MISSING" in item
                            for item in found))

    def test_g2_unknown_type_with_title_is_rejected(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"][0].update({
            "session_name": "Fabricated title",
            "session_locator_type": "UNKNOWN",
            "confirmed_by": "WORKER",
            "session_name_evidence": "INSPECTED_IN_APP",
        })
        self.assertTrue(any("LOCATOR_TYPE_UNKNOWN_WITH_FIELDS" in item
                            for item in locator.check(obj)))

    def test_g2_suggested_title_is_not_observed(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"][0].update({
            "session_name": "same",
            "suggested_session_name": "same",
            "confirmed_by": "UNVERIFIED",
        })
        self.assertTrue(any("UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED" in item
                            for item in locator.check(obj)))

    def test_g3_invalid_locator_type(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"][0]["session_locator_type"] = "SCREENSHOT"
        self.assertTrue(any("LOCATOR_TYPE" in item
                            for item in locator.check(obj)))

    def test_g3_type_field_consistency(self):
        for kind, mutation, expected in (
            ("APP_TITLE", {"session_name": None}, "LOCATOR_TYPE_TITLE_MISSING"),
            ("APP_SESSION_ID", {"session_id": None},
             "LOCATOR_TYPE_SESSION_ID_MISSING"),
            ("APP_URL", {"session_url": None}, "LOCATOR_TYPE_URL_MISSING"),
            ("WORKTREE_AND_OPERATOR_NOTE",
             {"worktree_path": None, "notes": None},
             "LOCATOR_TYPE_WORKTREE_MISSING"),
        ):
            obj = copy.deepcopy(REGISTRY)
            row = obj["records"][0]
            row.update({"session_locator_type": kind, **mutation})
            self.assertTrue(any(expected in item for item in locator.check(obj)),
                            (kind, expected, locator.check(obj)))

    def test_g4_duplicate_registry_id(self):
        obj = copy.deepcopy(REGISTRY)
        duplicate = copy.deepcopy(obj["records"][0])
        duplicate["commission_id"] = "OTHER-COMMISSION"
        duplicate["revision"] = 1
        obj["records"].append(duplicate)
        self.assertTrue(any("DUPLICATE_REGISTRY_ID" in item
                            for item in locator.check(obj)))

    def test_g4_duplicate_revision(self):
        obj = copy.deepcopy(REGISTRY)
        duplicate = copy.deepcopy(obj["records"][0])
        duplicate["registry_id"] = "OTHER-REGISTRY-ID"
        obj["records"].append(duplicate)
        self.assertTrue(any("DUPLICATE_REVISION" in item
                            for item in locator.check(obj)))

    def test_g5_bogus_confirmer_enum(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"][0]["confirmed_by"] = "ADMIN"
        self.assertTrue(any("CONFIRMED_BY" in item
                            for item in locator.check(obj)))

    def test_g5_user_confirmation_without_evidence(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"][0].update({"confirmed_by": "USER"})
        self.assertTrue(any("USER_CONFIRMATION_EVIDENCE" in item
                            for item in locator.check(obj)))

    def test_g5_verified_machine_without_device(self):
        obj = copy.deepcopy(REGISTRY)
        obj["records"][0].update({"machine_claim": "VERIFIED",
                                  "device": "UNKNOWN"})
        self.assertTrue(any("VERIFIED_CLAIM_WITHOUT_DEVICE" in item
                            for item in locator.check(obj)))

    def test_g6_forged_valid_format_sha(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
            subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                            "locator@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
                            "Locator Test"], check=True)
            (tmp_path / "seed.txt").write_text("seed\n")
            subprocess.run(["git", "-C", str(tmp_path), "add", "seed.txt"],
                           check=True)
            subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "seed"],
                           check=True)
            real = subprocess.run(
                ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
                capture_output=True, text=True, check=True).stdout.strip()
            single = {"schema": REGISTRY["schema"],
                      "records": [copy.deepcopy(REGISTRY["records"][0])]}
            branch = single["records"][0]["branch"]
            subprocess.run(["git", "-C", str(tmp_path), "branch", branch],
                           check=True)
            single["records"][0]["return_sha"] = "0" * 40
            self.assertTrue(any("SHA_NOT_LOCAL" in item for item in
                                locator.check(single, repo=tmp_path,
                                              require_sha=True)))
            single["records"][0]["return_sha"] = real
            self.assertFalse(any("SHA_NOT_LOCAL" in item or "SHA_READBACK" in item
                                 for item in locator.check(
                                     single, repo=tmp_path, require_sha=True)))

    def test_historical_unknown_is_preserved(self):
        row = copy.deepcopy(REGISTRY["records"][0])
        row.update({
            "device": "UNKNOWN",
            "device_evidence": "LOCAL_MAC_REPORTED_WHICH_MACHINE_UNVERIFIED",
            "agent_name": "UNKNOWN",
            "agent_id": None,
            "agent_role": "UNKNOWN",
            "session_name": None,
            "session_id": None,
            "session_url": None,
            "session_locator_type": "UNKNOWN",
            "locator_status": "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
            "confirmed_by": "WORKER",
            "machine_claim": "SELF_REPORTED",
        })
        obj = {"schema": REGISTRY["schema"], "records": [row]}
        self.assertEqual(_hard(locator.check(obj)), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
