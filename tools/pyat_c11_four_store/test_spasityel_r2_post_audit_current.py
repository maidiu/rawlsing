"""#1006/#1271: no SOURCE_CURRENT positive report after external revocation.

Sourcefree test-only authority; does not impersonate the private MainMac R2 file.
The real runner's source.verify._live is installed with a synthetic revocable
callback and the actual S2 writer, audit, cold reopen, queries and receipt run.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from . import runner
from .stores import StoreFailure
from .test_runner_sourcefree import FixtureSource


class RevocableFixtureSource(FixtureSource):
    allow = None

    def __init__(self, config, root, emit):
        super().__init__(config, root, emit)
        flag = type(self).allow

        class Verified:
            def _live(self):
                if not flag["current"]:
                    raise StoreFailure("external source CURRENT revoked during physical runner")

        self.verified = Verified()


def _config(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "schema": "PYAT_FOUR_PERMANENT_STORE_BUNDLE@1",
        "output_dir": "output",
        "minimum_free_gib": 0,
        "physical_question_limit": 3,
        "evidence_sample_limit": 6,
        "cold_reopen_limit": 0,
        "batch_commit": 2,
    }))
    return path


class RevocationAfterAuditTests(unittest.TestCase):
    def _run(self, root: Path, flag: dict, *, revoke_at: str | None = None):
        path = _config(root / "bundle.json")
        RevocableFixtureSource.allow = flag
        real_audit = runner.Store.audit_families
        real_engine = runner._engine_report

        def audit_and_revoke(store, *args, **kwargs):
            result = real_audit(store, *args, **kwargs)
            if revoke_at == "post_audit":
                flag["current"] = False
            return result

        def queries_and_revoke(*args, **kwargs):
            result = real_engine(*args, **kwargs)
            if revoke_at == "post_queries":
                flag["current"] = False
            return result

        with (
            patch.object(runner, "InputEstate", RevocableFixtureSource),
            patch.object(runner.Store, "audit_families", audit_and_revoke),
            patch.object(runner, "_engine_report", queries_and_revoke),
        ):
            try:
                return runner.run(path, only="S2")
            finally:
                RevocableFixtureSource.allow = None

    def test_revocation_after_full_audit_refuses_positive_benchmark_publication(self):
        with tempfile.TemporaryDirectory() as home:
            flag = {"current": True}
            with self.assertRaisesRegex(StoreFailure, "source CURRENT revoked"):
                self._run(Path(home), flag, revoke_at="post_audit")
            reports = list((Path(home) / "output").glob("*/comparison.json"))
            self.assertEqual(len(reports), 1)
            result = json.loads(reports[0].read_text())
            self.assertEqual(result["status"], "SOURCE_AUTHORITY_RESOURCE_OR_RUNNER_HOLD")
            self.assertNotEqual(
                result.get("comparison", {}).get("four_arm_complete"), True,
            )

    def test_revocation_after_physical_query_refuses_positive_report(self):
        with tempfile.TemporaryDirectory() as home:
            flag = {"current": True}
            with self.assertRaisesRegex(StoreFailure, "source CURRENT revoked"):
                self._run(Path(home), flag, revoke_at="post_queries")
            reports = list((Path(home) / "output").glob("*/comparison.json"))
            self.assertEqual(len(reports), 1)
            result = json.loads(reports[0].read_text())
            self.assertEqual(result["status"], "SOURCE_AUTHORITY_RESOURCE_OR_RUNNER_HOLD")

    def test_unchanged_current_allows_same_s2_physical_suite_but_no_science(self):
        with tempfile.TemporaryDirectory() as home:
            flag = {"current": True}
            result = self._run(Path(home), flag)
            self.assertTrue(flag["current"])
            self.assertEqual(
                result["status"],
                "SINGLE_ARM_PHYSICAL_COMPLETE__ORIGINAL_ISSUER_HOLD",
            )
            self.assertFalse(result["comparison"]["four_arm_complete"])
            self.assertEqual(set(result["arms"]), {"S2"})


if __name__ == "__main__":
    unittest.main()
