"""#1006/#1271 sourcefree: distinct parallel physical runner invocation identity.

Two exact-content fixture providers and separate root directories share ONE output
location. This does NOT compare CPU across machines or exercise private R2 grants.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from . import runner
from .stores import StoreFailure
from .test_runner_sourcefree import FixtureSource


def _config(root: Path, output: Path, *, explicit_id: str | None = None):
    root.mkdir(parents=True)
    value = {
        "schema": "PYAT_FOUR_PERMANENT_STORE_BUNDLE@1",
        "output_dir": str(output),
        "minimum_free_gib": 0,
        "physical_question_limit": 3,
        "evidence_sample_limit": 6,
        "cold_reopen_limit": 0,
        "batch_commit": 2,
    }
    if explicit_id:
        value["run_id"] = explicit_id
    path = root / "bundle.json"
    path.write_text(json.dumps(value))
    return path


class R1271RunIdIsolationTests(unittest.TestCase):
    def test_two_same_time_single_arm_runs_are_distinct_and_never_four_arm_green(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            output = root / "shared-output"
            first = _config(root / "worker-a", output)
            second = _config(root / "worker-b", output)

            def execute(path):
                return runner.run(path, only="S2")

            # Mock only the original input estate, never the actual physical
            # four-store body writer, audit, cold reopen or status publication.
            # The CPU sampler counts this shared Python process: no standalone
            # resource or throughput conclusion follows from the percentages.
            with patch.object(runner, "InputEstate", FixtureSource):
                with ThreadPoolExecutor(max_workers=2) as pool:
                    futures = [pool.submit(execute, p) for p in (first, second)]
                    reports = [future.result() for future in futures]

            dirs = [Path(report["report_directory"]) for report in reports]
            self.assertEqual(len(set(dirs)), 2)
            self.assertTrue(all(folder.parent == output for folder in dirs))
            for report, folder in zip(reports, dirs):
                self.assertEqual(
                    report["status"],
                    "SINGLE_ARM_PHYSICAL_COMPLETE__ORIGINAL_ISSUER_HOLD",
                )
                self.assertEqual(set(report["arms"]), {"S2"})
                self.assertFalse(report["comparison"]["four_arm_complete"])
                self.assertTrue((folder / "S2" / "permanent.sqlite").is_file())
                self.assertTrue((folder / "S2" / "report.json").is_file())
                self.assertTrue((folder / "S2" / "progress.jsonl").is_file())
                persisted = json.loads((folder / "comparison.json").read_text())
                self.assertEqual(persisted["report_directory"], str(folder))
                cpu = report["arms"]["S2"]["resources"]
                self.assertGreaterEqual(cpu["sampled_cpu_user_s"], 0)
                self.assertGreaterEqual(cpu["sampled_cpu_system_s"], 0)
                self.assertGreaterEqual(cpu["peak_cpu_percent_one_core"], 0)
                self.assertGreaterEqual(cpu["avg_cpu_percent_host_capacity"], 0)
                self.assertGreaterEqual(cpu["logical_cpus"], 1)
                self.assertEqual(
                    cpu["cpu_measurement_grade"],
                    "SAMPLED_PROCESS_TREE_CPU_SECONDS_MAY_MISS_SHORT_LIVED_CHILDREN",
                )
                progress = (folder / "S2" / "progress.jsonl").read_text()
                self.assertIn('"stage":"resources_final"', progress)
                self.assertIn('"cpu_percent_host_capacity":', progress)

    def test_explicit_operator_run_id_refuses_collision_without_touching_source(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            output = root / "output"
            output.mkdir()
            collision = output / "OPERATOR_PINNED"
            collision.mkdir()
            marker = collision / "report.json"
            marker.write_text("MUST_NOT_CHANGE")

            path = _config(root / "worker", output, explicit_id="OPERATOR_PINNED")
            with patch.object(
                runner, "InputEstate",
                side_effect=AssertionError("source must never open on collision"),
            ):
                with self.assertRaises(FileExistsError):
                    runner.run(path, only="H")
            self.assertEqual(marker.read_text(), "MUST_NOT_CHANGE")
            self.assertEqual(set(item.name for item in collision.iterdir()), {"report.json"})


if __name__ == "__main__":
    unittest.main()
