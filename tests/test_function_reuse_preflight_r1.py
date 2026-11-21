"""REMONT sourcefree first-fault court for October-19 existing-function stop-off.

Tests cover refusal mechanisms, not whether a human design is truly novel.
Author issues tests to REMONT; no independent green is claimed here.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_function_reuse_preflight.py"
spec = importlib.util.spec_from_file_location("function_reuse_gate", MODULE_PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args],
                       check=True, capture_output=True, text=True)
    return p.stdout.strip()


def write(root: Path, path: str, content: str) -> None:
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


class ExistingFunctionStopOffCourt(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "remont@example.invalid")
        git(self.root, "config", "user.name", "REMONT_TEST")
        write(self.root, gate.LAW, "Search live product edge backward before invention.\n")
        write(self.root, gate.G4, json.dumps({
            "obligation_id": "G3A:FUNCTION:G1A-FUNC-026",
            "capability": "F6M_PARTIAL_IDENTIFICATION",
        }) + "\n")
        write(self.root, "tools/existing.py", "def owner_function():\n    return 1\n")
        write(self.root, ".github/workflows/programma-canonical-pre-main.yml",
              "name: existing receiver\nsteps: [existing-consumer]\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "existing function and law")
        self.base = git(self.root, "rev-parse", "HEAD")
        self.cardpath = (gate.RECEIPTS + "/FRS-TEST-001.json")
        self.target = "tools/new_capability.py"
        self.card = self.make_card()

    def blob(self, path: str) -> str:
        return git(self.root, "hash-object", path)

    def make_card(self):
        return {
            "schema": gate.SCHEMA,
            "decision_id": "FRS-TEST-001",
            "stage": "BEFORE_IMPLEMENTATION",
            "disposition": "EXTEND_EXISTING",
            "protected_cut": "a" * 40,
            "governing_law": {
                "path": gate.LAW, "blob": self.blob(gate.LAW),
            },
            "g4_parity": {
                "path": gate.G4, "blob": self.blob(gate.G4),
                "examined_ids": ["G3A:FUNCTION:G1A-FUNC-026"],
                "function_relationship": "F6M had an earlier partial-identification method, which must be reused.",
            },
            "function": {
                "inputs": "Actual repository code, governance and previous consumers.",
                "operation": "Compare existing symbol behavior before adding a narrowly necessary adapter.",
                "outputs": "A source-pinned evidence artifact consumed by the existing receiver.",
                "first_consumer": "Current existing-consumer workflow and source owner.",
                "real_gap": "Existing workflow checks no functional collision before new implementation.",
            },
            "search_scope": {
                "current_code": "Current code compared with owner_function and existing receiver",
                "historical_and_g4": "Inspected G4 F6M partial identification and prior source law",
                "active_development": "Checked known current branch and functional counterparts",
                "uninspected": "External private machines cannot be inspected here",
            },
            "existing_candidates": [{
                "path": "tools/existing.py", "kind": "python_symbol",
                "symbol": "owner_function", "blob": self.blob("tools/existing.py"),
                "role": "REUSE_EXISTING",
                "difference": "Present owner lacks the proposed source-pinned receiver."
            }],
            "implementation_targets": [self.target],
            "first_consumer": {
                "path": ".github/workflows/programma-canonical-pre-main.yml",
                "needle": "existing-consumer",
                "expected_effect": "The receiving workflow would reject unexamined new modules.",
            },
            "active_pr_heads": [],
            "positive_proof": "First card commit precedes first changed production module commit.",
            "negative_proof": "A fake law, owner, G4 ID or same-commit card must fail.",
            "user_answer": "USER_ORDERED_PREBUILD_REUSE_STOP_OFF_FOR_THIS_FUNCTION",
            "owner": "Existing competent owner plus an independent source reviewer",
            "authority_limits": "SOURCEFREE_TEST__NO_ORIGINAL_PERMISSIONS_GRANTED",
        }

    def commit(self, message: str) -> str:
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", message)
        return git(self.root, "rev-parse", "HEAD")

    def save_card(self):
        write(self.root, self.cardpath, json.dumps(self.card, indent=2) + "\n")

    def test_prebuild_receipt_precedes_implementation_and_checks_owner_and_g4(self):
        self.save_card()
        self.commit("capability predecision evidence")
        write(self.root, self.target, "def new_capability():\n    return 2\n")
        head = self.commit("implement only after decision")
        out = gate.check_changed(self.root, self.base, head, online=False)
        self.assertEqual(out["checked_implementation_files"], 1)
        self.assertEqual(out["decisions"][0]["checked_owners"], 1)
        self.assertIn("OFFLINE", out["state"])

    def test_same_commit_card_plus_code_is_not_a_prebuild_decision(self):
        self.save_card()
        write(self.root, self.target, "def new_capability():\n    return 2\n")
        head = self.commit("bad all at once")
        with self.assertRaisesRegex(gate.ReusePreflightError, "RECEIPT_COMMITTED_TOO_LATE"):
            gate.check_changed(self.root, self.base, head, online=False)

    def test_missing_card_is_hard_refusal(self):
        write(self.root, self.target, "def new_capability():\n    return 2\n")
        head = self.commit("bad no card")
        with self.assertRaisesRegex(gate.ReusePreflightError, "MISSING_PREBUILD"):
            gate.check_changed(self.root, self.base, head, online=False)

    def test_fake_historical_parity_id_is_refused(self):
        self.card["g4_parity"]["examined_ids"] = ["MADE_UP_PARITY"]
        with self.assertRaisesRegex(gate.ReusePreflightError, "G4_FALSE"):
            gate.validate_card(self.root, self.card, online=False)

    def test_stale_owner_blob_is_refused(self):
        self.card["existing_candidates"][0]["blob"] = "0" * 40
        with self.assertRaisesRegex(gate.ReusePreflightError, "OWNER_SOURCE_NOT_CURRENT"):
            gate.validate_card(self.root, self.card, online=False)

    def test_fabricated_owner_symbol_is_refused(self):
        self.card["existing_candidates"][0]["symbol"] = "nonexistent"
        with self.assertRaisesRegex(gate.ReusePreflightError, "INHERITED_SYMBOL_NOT_FOUND"):
            gate.validate_card(self.root, self.card, online=False)

    def test_unmatched_first_consumer_is_refused(self):
        self.card["first_consumer"]["needle"] = "never-present-in-repo"
        with self.assertRaisesRegex(gate.ReusePreflightError, "FIRST_CONSUMER_CARRIER_NOT_FOUND"):
            gate.validate_card(self.root, self.card, online=False)

    def test_unknown_design_cannot_be_promoted_to_build(self):
        self.card["disposition"] = "UNRESOLVED"
        with self.assertRaisesRegex(gate.ReusePreflightError, "NO_UNRECONCILED"):
            gate.validate_card(self.root, self.card, online=False)

    def test_preflight_checks_source_even_when_not_changed(self):
        self.card["governing_law"]["blob"] = "0" * 40
        with self.assertRaisesRegex(gate.ReusePreflightError, "GOVERNING_LAW_STALE"):
            gate.validate_card(self.root, self.card, online=False)

    def test_online_currentness_never_silently_becomes_offline_green(self):
        out = gate.validate_card(self.root, self.card, online=False)
        self.assertIn("CURRENTNESS_NOT_CERTIFIED", out["state"])
        self.assertNotIn("SOURCE_CHECKS_CURRENT__", out["state"])

    def test_target_selection_covers_production_and_commissions_not_tests(self):
        gate.self_test()
        self.assertTrue(gate.production_target("WORKER_COMMISSIONS/new_commission.md"))
        self.assertFalse(gate.production_target("rawlsing_next/tests/test_foo.py"))


if __name__ == "__main__":
    unittest.main()
