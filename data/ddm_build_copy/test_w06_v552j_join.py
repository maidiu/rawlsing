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
        "family_id": "family",
        "pattern_id": "pattern",
        "packet_contract_hash": "packet-contract",
        "pattern_item_count": 2,
        "component_contract_hashes_ordered_json": '["component-contract-1","component-contract-2"]',
        "joint_response_identity_signature": "joint-response",
        "joint_semantic_signature": "joint-semantic",
        "joint_orientation_signature": "joint-orientation",
        "joint_topology_signature": "joint-topology",
        "joint_target_signature": "joint-target",
        "joint_structural_signature": "joint-structural",
        "joint_measurement_contract_hash": "joint-measurement",
        "component_response_vector_json": '["r1","r2"]',
        "component_semantic_vector_json": '["s1","s2"]',
        "component_orientation_vector_json": '["o1","o2"]',
        "component_topology_vector_json": '["t1","t2"]',
        "component_target_vector_json": '["target1","target2"]',
        "component_structural_vector_json": '["struct1","struct2"]',
        "component_denominator_vector_json": json.dumps([
            {"item_order": 1, "empirical_distribution_id": "dist-1", "n_respondents": 100},
            {"item_order": 2, "empirical_distribution_id": "dist-2", "n_respondents": 100},
        ]),
        "denominator_separation_status": "PASS",
        "joint_n_unweighted": 100,
        "joint_pattern_count_unweighted": 10,
        "joint_support_status": "sufficient_support",
        "joint_semantic_authority_status": "CERTIFIED",
        "joint_directionality_authority_status": "CERTIFIED",
        "joint_family_target_authority_status": "CERTIFIED",
        "joint_structural_authority_status": "CERTIFIED",
        "joint_measurement_authority_status": "CERTIFIED",
        "joint_evidence_authority_status": "CERTIFIED",
        "v550j_pattern_index_artifact_hash": "a" * 64,
        "v550j_pattern_item_index_artifact_hash": "b" * 64,
        "v550j_manifest_hash": "c" * 64,
        "review_required": False,
    }
    row.update(overrides)
    return row


def component(packet_row: dict, item_order: int):
    return {
        "run_id": packet_row.get("run_id", "run"),
        "packet_id": packet_row.get("packet_id", "p1"),
        "pattern_id": packet_row.get("pattern_id", "pattern"),
        "family_id": packet_row.get("family_id", "family"),
        "item_order": item_order,
        "component_id": f"component-{item_order}",
        "component_contract_hash": f"component-contract-{item_order}",
        "source": packet_row.get("source", "TEST"),
        "source_family": packet_row.get("source_family", "TEST"),
        "canonical_wave": packet_row.get("canonical_wave", "W1"),
        "country_code": packet_row.get("country_code", "XX"),
        "v550j_item_role": f"role-{item_order}",
        "v551_evidence_role": "RELATION_EVIDENCE",
        "v551_evidence_role_status": "VALID_RELATION_EVIDENCE_ROLE",
        "component_evidence_role": "relation_component",
        "component_certification_contribution": "relation_component",
        "v551_empirical_distribution_id": f"dist-{item_order}",
        "v551_n_respondents": 100,
        "v551_semantic_role_authority_status": "CERTIFIED",
        "v551_response_semantics_authority_status": "CERTIFIED",
        "v551_directionality_authority_status": "CERTIFIED",
        "v551_provenance_basis": "fixture",
        "schema_version": "v2.2.3",
        "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
    }


def components_for_frames(*frames):
    rows = []
    seen = set()
    for frame in frames:
        if frame is None or frame.empty:
            continue
        for packet_row in frame.to_dict("records"):
            packet_id = str(packet_row.get("packet_id") or "")
            if not packet_id or packet_id in seen:
                continue
            seen.add(packet_id)
            rows.extend([component(packet_row, 1), component(packet_row, 2)])
    return pd.DataFrame(rows)


def build_v552j_join(**kwargs):
    if "v551j_components" not in kwargs:
        kwargs["v551j_components"] = components_for_frames(
            kwargs.get("v551j_certified"), kwargs.get("v551j_review")
        )
    return handoff.build_v552j_join(**kwargs)


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
        result = build_v552j_join(
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
        result = build_v552j_join(
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
        result = build_v552j_join(
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
        result = build_v552j_join(
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
        result = build_v552j_join(
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
        component_index = components_for_frames(candidate)
        review = pd.DataFrame([{"run_id": "run", "packet_id": "p1", "certification_status": "REVIEW_REQUIRED_AUTHORITY_GAP", "review_required": True}])
        def declared(_path, declaration, *, label, expected_schema):
            if label == "V551J_CANDIDATE": return candidate.copy()
            if label == "V551J_COMPONENT": return component_index.copy()
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
        result = build_v552j_join(
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
        joined = build_v552j_join(
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
