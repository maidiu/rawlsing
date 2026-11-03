#!/usr/bin/env python3
"""Fail-closed regression probes for custody structural integrity, no network."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("validate_custody", ROOT / "validate_custody.py")
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


def seed():
    return json.loads((ROOT / "01_PRIORITY_RECOVERY_QUEUE.json").read_text(encoding="utf-8"))


class CustodyTest(unittest.TestCase):
    def test_seed_is_structurally_admissible_not_accepted(self):
        q = seed()
        self.assertEqual(V.audit(q), [])
        self.assertTrue(all(e["state"] != "CLOSED" for e in q["entries"]))

    def test_duplicate_identity_rejected(self):
        q = seed()
        q["entries"].append(copy.deepcopy(q["entries"][0]))
        self.assertIn("DUPLICATE_CUSTODY_ID", " ".join(V.audit(q)))

    def test_reviewed_without_review_sha_rejected(self):
        q = seed()
        e = q["entries"][0]
        e["state"] = "REVIEWED_SCOPED"
        e["review"]["commit_sha"] = None
        self.assertIn("REVIEWED_WITHOUT_REVIEW_SHA", " ".join(V.audit(q)))

    def test_durable_sourcefree_positive_cannot_be_promoted_without_consumer(self):
        q = seed()
        e = q["entries"][0]
        e["state"] = "CLOSED"
        e["disposition"] = "ADOPTED_WITH_CONSUMER"
        e["owner_intake_receipt"] = "unreviewed-scoped-status"
        s = " ".join(V.audit(q))
        self.assertIn("ADOPTED_WITHOUT_REAL_CONSUMER_AND_EXACT_TARGET", s)
        self.assertIn("ADOPTED_WITHOUT_INDEPENDENT_SCOPE_ACCEPTANCE", s)
        self.assertIn("ADOPTED_WITH_UNKNOWN_AUTHORITY", s)

    def test_held_is_not_closed(self):
        q = seed()
        e = q["entries"][1]
        e["state"] = "CLOSED"
        e["disposition"] = "HELD_WITH_OWNER"
        self.assertIn("CLOSED_WITHOUT_DISPOSITION", " ".join(V.audit(q)))

    def test_reviewed_sha_bad_ref_rejected(self):
        q = seed()
        e = q["entries"][0]
        e["review"]["commit_sha"] = "PASS"
        self.assertIn("INVALID_REVIEW_SHA", " ".join(V.audit(q)))


if __name__ == "__main__":
    unittest.main()
