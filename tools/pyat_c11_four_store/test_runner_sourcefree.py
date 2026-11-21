"""Sourcefree end-to-end runner integration: deliberately no issued science.

The actual InputEstate constructor is mocked, never represented as authorized
source or native I03. Tests all FOUR complete physical stores and fresh
new-Python-process reopen against a local 13-family miniature Parquet corpus.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from . import runner
from .test_stores import fixture, family_expected
from .stores import FAMILIES,StoreFailure,canonical

class MockVerified:
    def _live(self):
        return True

class FixtureSource:
    def __init__(self, conf, root, emit):
        self.data,self.qs,self.people=fixture()
        self.manifest={
            "schema":"ANVIL_STREAM_C11_ESTATE@1",
            "family_counts":{k:len(v) for k,v in self.data.items()},
            "members":{},
        }
        self.identity={
            "schema":"ANVIL_STREAM_C11_ESTATE@1",
            "source_id":"SOURCEFREE_INTEGRATION_TEST_ONLY",
            "manifest_sha256":"f"*64,
            "roots":{"logical":"b"*64},
        }
        self.estate_root=root
        self.estate_path=root/"fixture_estate"
        self.estate_path.mkdir()
        self.verified=MockVerified()
        import pyarrow as pa
        import pyarrow.parquet as pq
        for family,rows in self.data.items():
            p=self.estate_path/(family+".parquet")
            pq.write_table(pa.Table.from_pylist(rows),p)
            self.manifest["members"][family+".parquet"]="TEST_ONLY"
        p=self.estate_path/"event_locator.parquet"
        pq.write_table(pa.table({"ref":[]}),p)
        self.manifest["members"][p.name]="TEST_ONLY"
        self.source_bytes=sum(x.stat().st_size for x in self.estate_path.iterdir())
        emit(stage="fixture_sourcefree_only",completed="synthetic_rows")
    def feed(self,store,progress,resources,batch_commit=2048):
        results=family_expected(self.data)
        for fam,rows in self.data.items():
            for position,row in enumerate(rows):
                routing=(self.qs[0],"RISK|set|"+"d"*64) if fam=="RoutingEligibilityFact" else None
                store.add_row(fam,position,row,0,position,routing=routing)
            store.commit_batch()
            progress(stage="fixture_build",family=fam,completed=len(rows))
            resources.check()
        return results

class RunnerIntegrationTests(unittest.TestCase):
    def test_four_arms_single_launch_and_unqualified_native_hold(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            config={
                "schema":"PYAT_FOUR_PERMANENT_STORE_BUNDLE@1",
                "output_dir":"output",
                "run_id":"SOURCEFREE_4ARM_CI",
                "minimum_free_gib":0,
                "physical_question_limit":3,
                "evidence_sample_limit":6,
                "cold_reopen_limit":2,
                "batch_commit":2,
                "continue_after_arm_failure":False,
            }
            path=root/"bundle.json"
            path.write_text(json.dumps(config))
            with patch.object(runner,"InputEstate",FixtureSource):
                out=runner.run(path)
            self.assertEqual(out["status"],"PHYSICAL_COMPLETE__ORIGINAL_ISSUER_HOLD")
            self.assertEqual(set(out["arms"]),{"H","S1","S2","S3"})
            self.assertTrue(out["comparison"]["source_family_body_parity"])
            self.assertTrue(out["comparison"]["physical_query_parity"])
            economics=out["measured_economics"]
            self.assertTrue(economics["all_four_measured"])
            self.assertEqual(set(economics["individual_arm_costs"]),{"H","S1","S2","S3"})
            self.assertIn("versus_H",economics["individual_arm_costs"]["S2"])
            self.assertEqual(economics["storage_selection"],
                "HELD_UNTIL_NATIVE_ISSUER_ALL13_FAMILIES_SOURCE_SCIENCE_AND_DOWNSTREAM_PARITY")
            self.assertEqual(out["comparison"]["native_i03_fact_parity"],"HELD_NO_ORIGINAL_ISSUER")
            for arm,report in out["arms"].items():
                self.assertEqual(report["status"],"COMPLETED_PHYSICAL_AND_NATIVE_WHERE_ISSUED")
                self.assertEqual(report["metrics"]["events"],6)
                self.assertEqual(report["metrics"]["distinct_questions"],3)
                cpu=report["resources"]
                self.assertGreaterEqual(cpu["sampled_cpu_user_s"],0)
                self.assertGreaterEqual(cpu["sampled_cpu_system_s"],0)
                self.assertGreaterEqual(cpu["peak_cpu_percent_one_core"],0)
                self.assertGreaterEqual(cpu["avg_cpu_percent_one_core"],0)
                self.assertGreaterEqual(cpu["logical_cpus"],1)
                self.assertGreaterEqual(cpu["samples"],1)
                self.assertEqual(cpu["cpu_measurement_grade"],
                    "SAMPLED_PROCESS_TREE_CPU_SECONDS_MAY_MISS_SHORT_LIVED_CHILDREN")
                progress=(root/"output"/config["run_id"]/arm/"progress.jsonl").read_text()
                self.assertIn('"stage":"resources_final"',progress)
                self.assertIn('"cpu_percent_one_core":',progress)
                self.assertEqual(len(report["query_report"]["fresh_process_probes"]),2)
                for cp in report["query_report"]["fresh_process_probes"]:
                    self.assertIsNotNone(cp["one_body_sha256"])
                self.assertTrue((root/"output"/config["run_id"]/arm/"permanent.sqlite").exists())
                self.assertTrue((root/"output"/config["run_id"]/arm/"report.json").exists())
                self.assertTrue((root/"output"/config["run_id"]/arm/"progress.jsonl").exists())
            compare=json.loads((root/"output"/config["run_id"]/"comparison.json").read_text())
            self.assertEqual(compare["status"],"PHYSICAL_COMPLETE__ORIGINAL_ISSUER_HOLD")
            self.assertTrue((root/"output"/config["run_id"]/"summary.csv").exists())

    def test_single_arm_succeeds_without_false_four_arm_comparison(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            cfg={
                "schema":"PYAT_FOUR_PERMANENT_STORE_BUNDLE@1",
                "output_dir":"output",
                "run_id":"SOURCEFREE_SINGLE_ARM",
                "minimum_free_gib":0,
                "physical_question_limit":3,
                "evidence_sample_limit":6,
                "cold_reopen_limit":1,
                "batch_commit":2,
            }
            path=root/"bundle.json"
            path.write_text(json.dumps(cfg))
            with patch.object(runner,"InputEstate",FixtureSource):
                result=runner.run(path,only="S2")
            self.assertEqual(result["status"],
                "SINGLE_ARM_PHYSICAL_COMPLETE__ORIGINAL_ISSUER_HOLD")
            self.assertEqual(set(result["arms"]),{"S2"})
            self.assertFalse(result["comparison"]["four_arm_complete"])
            self.assertEqual(result["comparison"]["selected_arm"],"S2")
            self.assertEqual(result["arms"]["S2"]["status"],
                             "COMPLETED_PHYSICAL_AND_NATIVE_WHERE_ISSUED")
            self.assertTrue(Path(result["report_directory"]).is_dir())

    def test_invalid_parameters_fail_before_source_admission(self):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/"bundle.json"
            for value in (0,-1,True,1.5):
                with self.subTest(value=value):
                    path.write_text(json.dumps({
                        "schema":"PYAT_FOUR_PERMANENT_STORE_BUNDLE@1",
                        "output_dir":"output",
                        "batch_commit":value,
                    }))
                    with patch.object(runner,"InputEstate",
                                      side_effect=AssertionError("source admission must not start")):
                        with self.assertRaisesRegex(StoreFailure,"batch_commit"):
                            runner.run(path)

if __name__=="__main__":
    unittest.main()
