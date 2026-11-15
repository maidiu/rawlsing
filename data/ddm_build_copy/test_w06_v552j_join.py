from __future__ import annotations

import ast
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pandas as pd

from data.ddm_build_copy import ddm_v552j_handoff as handoff
from data.ddm_build_copy import compile_v552j_structural_handoff as compiler


def packet(packet_id: str = "p1", **overrides):
    row = {
        "run_id": "run",
        "packet_id": packet_id,
        "source": "TEST",
        "source_family": "TEST",
        "wave": "W1",
        "canonical_wave": "W1",
        "country_code": "XX",
        "relation_axis_ids_json": '["axis"]',
        "target_entity_ids_json": '["target"]',
        "driver_facet_ids_json": '["facet"]',
        "question_ids_json": '["q1"]',
        "certification_status": "CERTIFIED_JOINT_RELATION_EVIDENCE",
        "joint_support_status": "sufficient_support",
        "joint_directionality_authority_status": "CERTIFIED",
        "joint_evidence_authority_status": "CERTIFIED",
        "review_required": False,
    }
    row.update(overrides)
    return row


def fact(fact_id: str = "f1", **overrides):
    row = {
        "run_id": "run",
        "source": "TEST",
        "source_family": "TEST",
        "wave": "W1",
        "canonical_wave": "W1",
        "country_code": "XX",
        "v552_structural_fact_id": fact_id,
        "source_artifact": "v552_pressure_observation_index",
        "source_row_index": 0,
        "source_row_id": "obs-1",
        "relation_axis_id": "axis",
        "target_entity_id": "target",
        "driver_facet_id": "facet",
        "question_id": "q1",
        "structural_channel_id": "channel",
        "horizon_constraint_id": "horizon",
        "semantic_signature": "semantic",
        "structural_fact_lane": "primary_pressure",
        "structural_fact_grain": "empirical_distribution_pressure_observation",
        "structural_fact_status": "PRESENT",
        "pressure_score": 0.25,
        "pressure_score_status": "OBSERVED_NONZERO",
        "measurement_evidence_status": "PRESENT",
        "downstream_permission_status": "ALLOW",
        "schema_version": "v3.0",
        "compiler_version": "v3.0",
    }
    row.update(overrides)
    return row


def state(evidence="PRESENT", permission="ALLOW"):
    return {
        "run_integrity_status": "PASS",
        "evidence_status": evidence,
        "downstream_permission_status": permission,
    }


class TestW06BV552JSemantics(unittest.TestCase):
    def test_one_first_nonempty_helper_only(self):
        source = Path(handoff.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
        self.assertEqual(names.count("_first_nonempty"), 1)

    def test_wrong_source_never_enters_semantic_match(self):
        p = pd.Series(packet())
        wrong = pd.Series(fact(source="OTHER", source_family="OTHER"))
        self.assertEqual(handoff._structural_fact_match_score(p, wrong), -1)
        resolved = handoff._packet_structural_dimension_resolution(p, pd.DataFrame([wrong]), pd.DataFrame())
        self.assertEqual(resolved["v552_structural_match_status"], "no_match")
        self.assertEqual(resolved["matched_fact_count"], 0)
        self.assertEqual(resolved["source_v552_structural_fact_id"], "")

    def test_wrong_country_and_wave_cannot_cross_scope(self):
        p = pd.Series(packet())
        for changed in (fact(country_code="YY"), fact(wave="W2", canonical_wave="W2")):
            self.assertEqual(handoff._structural_fact_match_score(p, pd.Series(changed)), -1)


    def test_stronger_wrong_scope_candidate_never_beats_in_scope_candidate(self):
        p = pd.Series(packet())
        wrong = fact(fact_id="wrong", source="OTHER", source_family="OTHER")
        inside = fact(fact_id="inside", question_id="other-question")
        self.assertEqual(handoff._structural_fact_match_score(p, pd.Series(wrong)), -1)
        self.assertGreaterEqual(handoff._structural_fact_match_score(p, pd.Series(inside)), 5)
        resolved = handoff._packet_structural_dimension_resolution(p, pd.DataFrame([wrong, inside]), pd.DataFrame())
        self.assertEqual(resolved["source_v552_structural_fact_id"], "inside")
        self.assertNotIn("wrong", resolved["source_v552_structural_fact_ids_diagnostic_json"])

    def test_present_packet_with_no_exact_scope_candidate_is_typed_unresolved_without_primary(self):
        result = handoff.build_v552j_join(
            run_id="run", v551j_certified=pd.DataFrame([packet()]), v551j_review=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame([fact(source="OTHER", source_family="OTHER")]),
            v551j_state=state(), v552_state=state(),
        )
        self.assertEqual(len(result["join_index"]), 0)
        self.assertEqual(len(result["join_audit"]), 1)
        self.assertEqual(result["join_audit"].iloc[0]["join_status"], "UNRESOLVED_NO_STRUCTURAL_MATCH")
        self.assertEqual(result["state"]["run_integrity_status"], "PASS")
        self.assertEqual(result["state"]["evidence_status"], "APPLICABLE_UNRESOLVED")
        self.assertEqual(result["state"]["downstream_permission_status"], "DENY")

    def test_shard_scope_mismatch_is_rejected_when_country_is_absent(self):
        p = pd.Series(packet(country_code="", shard_id="shard-a"))
        f = pd.Series(fact(country_code="", shard_id="shard-b"))
        self.assertEqual(handoff._structural_fact_match_score(p, f), -1)

    def test_no_evidence_has_zero_primary_rows_and_null_constraint_metrics(self):
        result = handoff.build_v552j_join(
            run_id="run",
            v551j_certified=pd.DataFrame(),
            v551j_review=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame([fact()]),
            v551j_state=state("VALID_EMPTY", "NOT_APPLICABLE"),
            v552_state=state("PRESENT", "ALLOW"),
        )
        self.assertEqual(len(result["join_index"]), 0)
        self.assertEqual(result["state"]["run_integrity_status"], "PASS")
        self.assertEqual(result["state"]["evidence_status"], "VALID_EMPTY")
        self.assertEqual(result["state"]["downstream_permission_status"], "NOT_APPLICABLE")
        self.assertEqual(result["metrics"]["constraint_count"], 0)
        for key, value in result["metrics"].items():
            if key.startswith("mean_"):
                self.assertIsNone(value)

    def test_review_only_packet_is_preserved_but_not_zero_constraint(self):
        review = pd.DataFrame([packet(certification_status="REVIEW_REQUIRED_AUTHORITY_GAP", review_required=True, joint_support_status="underpowered")])
        result = handoff.build_v552j_join(
            run_id="run", v551j_certified=pd.DataFrame(), v551j_review=review,
            v552_structural_facts=pd.DataFrame([fact()]),
            v551j_state=state("PRESENT", "DENY"), v552_state=state(),
        )
        row = result["join_index"].iloc[0]
        self.assertEqual(row["join_permission"], "REVIEW_ONLY")
        self.assertEqual(row["repair_debt_status"], "REVIEW_REQUIRED")
        self.assertEqual(result["metrics"]["constraint_count"], 0)
        self.assertIsNone(result["metrics"]["mean_readiness_score"])

    def test_observed_zero_is_measurement_not_absence(self):
        zero_fact = fact(pressure_score=0.0, pressure_score_status="OBSERVED_ZERO", measurement_evidence_status="PRESENT")
        result = handoff.build_v552j_join(
            run_id="run", v551j_certified=pd.DataFrame([packet()]), v551j_review=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame([zero_fact]), v551j_state=state(), v552_state=state(),
        )
        row = result["join_index"].iloc[0]
        self.assertEqual(row["join_permission"], "ALLOW")
        self.assertTrue(bool(row["observed_zero"]))
        self.assertEqual(row["pressure_score"], 0.0)
        self.assertEqual(result["state"]["evidence_status"], "PRESENT")
        self.assertEqual(result["metrics"]["observed_zero_count"], 1)

    def test_applicable_unresolved_never_becomes_observed_zero(self):
        unresolved_fact = fact(
            pressure_score=None,
            pressure_score_status="APPLICABLE_BUT_UNRESOLVED",
            measurement_evidence_status="APPLICABLE_BUT_UNRESOLVED",
            downstream_permission_status="DENY",
        )
        result = handoff.build_v552j_join(
            run_id="run", v551j_certified=pd.DataFrame([packet()]), v551j_review=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame([unresolved_fact]), v551j_state=state(), v552_state=state(),
        )
        row = result["join_index"].iloc[0]
        self.assertEqual(row["join_permission"], "DENY")
        self.assertFalse(bool(row["observed_zero"]))
        self.assertEqual(row["repair_debt_status"], "APPLICABLE_BUT_UNRESOLVED")
        self.assertTrue(pd.isna(row["pressure_score"]))

    def test_missing_packet_identity_is_never_synthesized(self):
        rows = handoff._packet_rows(pd.DataFrame([packet(packet_id="")]), pd.DataFrame())
        self.assertEqual(rows, [])
        source = Path(handoff.__file__).read_text(encoding="utf-8")
        self.assertNotIn('f"v552j__', source)
        self.assertNotIn('source="unknown"', source)


class TestW06BV552JProducerBoundary(unittest.TestCase):
    def setUp(self):
        self.scope = {"run_id": "run", "source": "TEST", "wave": "W1", "country_code": "XX", "shard_id": ""}

    def test_cross_run_and_cross_country_are_rejected(self):
        with self.assertRaisesRegex(Exception, "CROSS_RUN_MISMATCH"):
            compiler._coherent_scope("run", {**self.scope, "run_id": "other"}, self.scope)
        with self.assertRaisesRegex(Exception, "CROSS_SCOPE_MISMATCH:country"):
            compiler._coherent_scope("run", self.scope, {**self.scope, "country_code": "YY", "shard_id": "same"})

    def test_failed_producer_manifest_is_rejected(self):
        doc = SimpleNamespace(exists=True, readable=True, error="", payload={
            "contract_version": compiler.PIPELINE_BOUNDARY_CONTRACT_VERSION,
            "run_integrity_status": "FAIL",
            "evidence_status": "APPLICABLE_UNRESOLVED",
            "downstream_permission_status": "DENY",
        })
        boundary = SimpleNamespace(run_integrity_status="FAIL", evidence_status="APPLICABLE_UNRESOLVED", downstream_permission_status="DENY")
        with mock.patch.object(compiler, "read_status_document", return_value=doc), mock.patch.object(compiler, "boundary_state_from_payload", return_value=boundary):
            with self.assertRaisesRegex(Exception, "RUN_INTEGRITY_NOT_PASS"):
                compiler._read_manifest(Path("manifest.json"), "V552")

    def test_hash_mismatch_fails_before_semantic_parquet_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            manifest.write_text("{}", encoding="utf-8")
            artifact = root / "artifact.parquet"
            artifact.write_bytes(b"serialized")
            declaration = {"path": "artifact.parquet", "artifact_kind": "canonical", "schema_version": "v3.0", "row_count": 1, "artifact_file_sha256": "0" * 64}
            inspection = SimpleNamespace(exists=True, readable=True, error="", row_count=1, artifact_file_sha256="1" * 64)
            with mock.patch.object(compiler, "inspect_artifact", return_value=inspection), mock.patch.object(compiler.pd, "read_parquet") as read:
                with self.assertRaisesRegex(Exception, "ARTIFACT_FILE_SHA256_MISMATCH"):
                    compiler._verify_and_read_declared(manifest, declaration, label="FIXTURE", expected_schema="v3.0")
                read.assert_not_called()


    def test_valid_declared_artifact_hash_is_accepted_before_semantic_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            manifest.write_text("{}", encoding="utf-8")
            artifact = root / "artifact.parquet"
            artifact.write_bytes(b"serialized-good")
            digest = __import__("hashlib").sha256(artifact.read_bytes()).hexdigest()
            declaration = {"path": "artifact.parquet", "artifact_kind": "canonical", "schema_version": "v3.0", "row_count": 1, "artifact_file_sha256": digest}
            inspection = SimpleNamespace(exists=True, readable=True, error="", row_count=1, artifact_file_sha256=digest)
            expected = pd.DataFrame([{"run_id": "run"}])
            with mock.patch.object(compiler, "inspect_artifact", return_value=inspection), mock.patch.object(compiler.pd, "read_parquet", return_value=expected) as read:
                actual = compiler._verify_and_read_declared(manifest, declaration, label="FIXTURE", expected_schema="v3.0")
            self.assertEqual(actual.to_dict("records"), expected.to_dict("records"))
            read.assert_called_once_with(artifact.resolve())

    def test_v552_valid_supported_producer_bundle_passes(self):
        payload = {
            "schema_version": compiler.V552_SCHEMA_VERSION,
            "compiler_version": compiler.V552_COMPILER_VERSION,
            "producer_scope_identity": self.scope,
        }
        producer_state = SimpleNamespace(run_integrity_status="PASS", evidence_status="PRESENT", downstream_permission_status="ALLOW")
        facts = pd.DataFrame([fact()])
        temporal = pd.DataFrame([{
            "run_id": "run", "source": "TEST", "source_family": "TEST", "canonical_wave": "W1", "country_code": "XX",
            "v552_structural_fact_id": "f1", "v552_temporal_key_source_id": "t1", "schema_version": "v3.0", "compiler_version": "v3.0",
        }])
        with mock.patch.object(compiler, "_read_manifest", return_value=(payload, producer_state)), \
             mock.patch.object(compiler, "_find_declaration", side_effect=lambda *a, **k: {"path": "facts.parquet" if "STRUCTURAL_FACT" in k["label"] else "keys.parquet"}), \
             mock.patch.object(compiler, "_verify_and_read_declared", side_effect=lambda _p, _d, *, label, expected_schema: facts.copy() if "STRUCTURAL_FACT" in label else temporal.copy()), \
             mock.patch.object(compiler, "_resolve_declared_path", side_effect=lambda _p, d, _l: Path(d["path"]).resolve()), \
             mock.patch.object(compiler, "sha256_file", return_value="d" * 64):
            bundle = compiler.verify_v552_producer_bundle("manifest.json", run_id="run")
        self.assertEqual(bundle["state"]["run_integrity_status"], "PASS")
        self.assertEqual(bundle["state"]["evidence_status"], "PRESENT")
        self.assertEqual(bundle["structural_facts"].iloc[0]["v552_structural_fact_id"], "f1")

    def test_review_surface_is_enriched_from_authoritative_candidate_identity(self):
        payload = {
            "schema_version": compiler.V551J_SCHEMA_VERSION,
            "compiler_version": compiler.V551J_COMPILER_VERSION,
            "producer_scope_identity": self.scope,
        }
        producer_state = SimpleNamespace(run_integrity_status="PASS", evidence_status="PRESENT", downstream_permission_status="DENY")
        candidate = pd.DataFrame([packet(certification_status="REVIEW_REQUIRED_AUTHORITY_GAP", review_required=True)])
        certified = pd.DataFrame(columns=candidate.columns)
        review = pd.DataFrame([{"run_id": "run", "packet_id": "p1", "certification_status": "REVIEW_REQUIRED_AUTHORITY_GAP", "review_required": True}])
        def declared(_path, declaration, *, label, expected_schema):
            if label == "V551J_CANDIDATE": return candidate.copy()
            if label == "V551J_CERTIFIED": return certified.copy()
            if label == "V551J_REVIEW": return review.copy()
            raise AssertionError(label)
        with mock.patch.object(compiler, "_read_manifest", return_value=(payload, producer_state)), \
             mock.patch.object(compiler, "_find_declaration", side_effect=lambda *a, **k: {"label": k["label"]}), \
             mock.patch.object(compiler, "_verify_and_read_declared", side_effect=declared), \
             mock.patch.object(compiler, "sha256_file", return_value="a" * 64):
            bundle = compiler.verify_v551j_producer_bundle("manifest.json", run_id="run")
        row = bundle["review"].iloc[0]
        self.assertEqual(row["source"], "TEST")
        self.assertEqual(row["canonical_wave"], "W1")
        self.assertEqual(row["country_code"], "XX")
        self.assertEqual(row["relation_axis_ids_json"], '["axis"]')


    def test_producer_version_mismatch_is_rejected(self):
        payload = {
            "schema_version": "stale-v551j",
            "compiler_version": compiler.V551J_COMPILER_VERSION,
            "producer_scope_identity": self.scope,
        }
        producer_state = SimpleNamespace(run_integrity_status="PASS", evidence_status="VALID_EMPTY", downstream_permission_status="NOT_APPLICABLE")
        with mock.patch.object(compiler, "_read_manifest", return_value=(payload, producer_state)):
            with self.assertRaisesRegex(Exception, "V551J_SCHEMA_VERSION_MISMATCH"):
                compiler.verify_v551j_producer_bundle("manifest.json", run_id="run")

    def test_no_parquet_mode_is_rejected_before_producer_reads(self):
        with mock.patch.object(compiler, "verify_v551j_producer_bundle") as v551j:
            with self.assertRaises(Exception):
                compiler.compile_v552j_run(run_id="run", v551j_manifest_path="a", v552_manifest_path="b", write_parquet=False)
            v551j.assert_not_called()

    def test_v553_compatibility_view_preserves_packet_and_probe_aliases(self):
        result = handoff.build_v552j_join(
            run_id="run", v551j_certified=pd.DataFrame([packet()]), v551j_review=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame([fact()]), v551j_state=state(), v552_state=state(),
        )
        compat = compiler._v553_compatibility_frame(result["join_index"])
        row = compat.iloc[0]
        self.assertEqual(row["v552j_packet_id"], "p1")
        self.assertEqual(row["source_v552_structural_fact_id"], "f1")
        self.assertTrue(bool(row["single_wave_probe_allowed"]))
        self.assertTrue(bool(row["ready_for_v553"]))
        self.assertFalse(bool(row["temporal_field_allowed"]))
        self.assertFalse(bool(row["ready_for_runtime_consumption"]))

    def test_stale_output_is_replaced_transactionally(self):
        joined = handoff.build_v552j_join(
            run_id="run", v551j_certified=pd.DataFrame(), v551j_review=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame(),
            v551j_state=state("NOT_APPLICABLE", "NOT_APPLICABLE"),
            v552_state=state("NOT_APPLICABLE", "NOT_APPLICABLE"),
        )
        producer = {
            "manifest_path": "producer/manifest.json", "manifest_sha256": "a" * 64,
            "scope": self.scope, "state": state("NOT_APPLICABLE", "NOT_APPLICABLE"),
            "certified": pd.DataFrame(), "review": pd.DataFrame(), "candidate": pd.DataFrame(),
            "artifact_paths": {"v552_structural_fact_index": "producer/facts.parquet", "v552_temporal_key_source_index": "producer/keys.parquet"},
        }
        def fake_write(frame, path, *, artifact, kind="canonical"):
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text("frame", encoding="utf-8")
            return {"artifact": artifact, "path": str(path.relative_to(path.parents[1])), "artifact_kind": kind, "row_count": len(frame), "artifact_file_sha256": "b" * 64, "logical_content_sha256": "c" * 64, "schema_version": handoff.V552J_JOIN_SCHEMA_VERSION, "compiler_version": handoff.V552J_JOIN_COMPILER_VERSION}
        def fake_atomic(path, payload):
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(payload), encoding="utf-8")
        def fake_publish(stage, final):
            if final.exists(): shutil.rmtree(final)
            shutil.move(str(stage), str(final))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); stale = root / "run"; stale.mkdir(); (stale / "retired.parquet").write_text("stale")
            with mock.patch.object(compiler, "verify_v551j_producer_bundle", return_value=producer), \
                 mock.patch.object(compiler, "verify_v552_producer_bundle", return_value={**producer, "structural_facts": pd.DataFrame(), "temporal_keys": pd.DataFrame()}), \
                 mock.patch.object(compiler, "build_v552j_join", return_value=joined), \
                 mock.patch.object(compiler, "_write_frame", side_effect=fake_write), \
                 mock.patch.object(compiler, "atomic_write_json", side_effect=fake_atomic), \
                 mock.patch.object(compiler, "publish_staged_directory", side_effect=fake_publish):
                compiler.compile_v552j_run(run_id="run", v551j_manifest_path="a", v552_manifest_path="b", output_root=root)
            self.assertFalse((root / "run" / "retired.parquet").exists())
            self.assertTrue((root / "run" / "manifest.json").exists())

    def test_mandatory_parquet_and_stage_local_boundary_hooks_are_present(self):
        source = Path(compiler.__file__).read_text(encoding="utf-8")
        for token in ("validate_machine_output_policy", "publish_staged_directory", "artifact_file_sha256", "producer_scope_identity", "v552j_structural_join_index.parquet"):
            self.assertIn(token, source)
        self.assertNotIn("resolve_pipeline_lineage", source)
        self.assertNotIn("section85", source.lower())


if __name__ == "__main__":
    unittest.main()
