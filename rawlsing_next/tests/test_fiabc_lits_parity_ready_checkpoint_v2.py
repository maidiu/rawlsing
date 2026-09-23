from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

import rawlsing_next.fiabc_final_oracle_freeze_producers as producer
from rawlsing_next.pre553_empirical_objects import semantic_hash


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _fixture():
    facts = [
        {
            "ref": {
                "kind": "EmpiricalFact@1.0.0",
                "object_id": f"urn:test:parity-ready:fact:{i:02d}",
                "content_hash": _h(f"fact-{i:02d}"),
            },
            "typed_state": "SUPPORTED",
        }
        for i in range(60)
    ]
    facts.sort(key=lambda row: producer._ref_key(row["ref"]))

    execution_body = {
        "schema": "PRE553_LEARNED_EMPIRICAL_EXECUTION_RECEIPT@1.0.0",
        "claim_kind": "LEARNED_EMPIRICAL_EXECUTION_ONLY",
        "candidate_count": 50,
    }
    execution = {**execution_body, "execution_identity": semantic_hash(execution_body)}
    replay = _h("semantic-replay")

    rows = []
    cursor = 0
    for i in range(50):
        fact_count = 2 if i < 10 else 1
        constituent = facts[cursor:cursor + fact_count]
        cursor += fact_count
        roles = [
            {"role": f"role-{i:02d}-{j}"}
            for j in range(2 if i < 27 else 1)
        ]
        coverage = "EVALUATED_VALID_EMPTY" if i == 49 else "EVALUATED_SUPPORTED"
        typed = "VALID_EMPTY" if i == 49 else "DISCOVERED_RESULT_SUPPORTED"
        candidate_hash = _h(f"candidate-{i:02d}")
        rows.append({
            "candidate_hash": candidate_hash,
            "typed_state": typed,
            "semantic_fields": {
                "candidate_identity": {
                    "candidate_hash": candidate_hash,
                    "rule_id": f"TEST_RULE_{i:02d}",
                    "validation": {"kind": "TEST", "ordinal": i},
                    "query_roles": roles,
                },
                "constituent_fact_manifest": constituent,
                "coverage_state": coverage,
                "support_uncertainty_state": {},
                "replay_ref": {
                    "kind": "ReplayManifest@1.0.0",
                    "object_id": f"urn:test:replay:{i:02d}",
                    "content_hash": _h(f"candidate-replay-{i:02d}"),
                },
            },
        })

    closure = semantic_hash({
        "candidate_fact_rows": rows,
        "constituent_fact_manifest": facts,
    })
    frontier = {
        "candidate_count": 50,
        "query_role_count": 77,
        "frontier_seal": producer.LITS_FRONTIER_SEAL,
        "ordered_candidate_hashes": [row["candidate_hash"] for row in rows],
    }
    learned = producer._bind_current_lits_execution_to_astra(
        execution_receipt=execution,
        semantic_replay_identity=replay,
        terminal_counts=producer.LITS_ACCEPTED_TERMINAL_COUNTS,
        candidate_count=50,
        query_role_count=77,
    )
    logical = [
        {
            "logical_candidate_key": _h(f"logical-{i:02d}"),
            "logical_candidate_material": {
                "contract": "FIABC_LITS_CROSS_SCHEMA_LOGICAL_CANDIDATE@1.0.0",
                "candidate_semantics": {"ordinal": i},
            },
        }
        for i in range(50)
    ]
    summary = {
        "schema": "FIABC_LITS_ASTRA_SHAPED_EMPIRICAL_SUMMARY@1.0.0",
        "frontier": {
            "candidate_count": 50,
            "query_role_count": 77,
            "frontier_seal": producer.LITS_FRONTIER_SEAL,
        },
        "logical_candidate_identity": logical,
        "P2": [{"logical_candidate_key": logical[i]["logical_candidate_key"]} for i in range(18)],
        "final_envelope": dict(producer.LITS_ACCEPTED_TERMINAL_COUNTS),
    }
    exact_refs = [{
        "kind": "EmpiricalQuerySpec@1.0.0",
        "object_id": "urn:test:checkpoint-query",
        "content_hash": _h("checkpoint-query"),
    }]
    material = {
        "source_identity": {
            "source": "LITS_I",
            "sha256": producer.LITS_SOURCE_SHA256,
            "rows": producer.LITS_ROWS,
            "variables": producer.LITS_VARIABLES,
        },
        "court_constitution_refs": {
            "frozen_authority_identity": producer._neutral_lits_authority_identity(),
            "frozen_workload_identity": frontier,
        },
        "semantic_authority_closure": [{
            "kind": "AuthoritySnapshot@1.0.0",
            "object_id": "urn:test:authority",
            "content_hash": _h("authority"),
        }],
        "projection_and_release_refs": {
            "projection_identity": producer.LITS_PROJECTION_IDENTITY,
            "c11_release_identity": producer.LITS_RUNTIME_RELEASE,
            "c11_replay_identity": producer.LITS_RUNTIME_REPLAY,
        },
        "frontier_manifest": frontier,
        "comparison_fact_manifest": rows,
        "expected_learned_product": learned,
        "replay_manifest": {
            "i05_replay_ref": {
                "kind": "PRE553_I05_FRONTIER_REPLAY",
                "object_id": "urn:test:i05-replay",
                "content_hash": replay,
            },
            "constituent_i03_closure_identity": closure,
            "dependency_root": _h("dependency"),
        },
        "exact_ref_manifest": exact_refs,
        "constituent_i03_fact_manifest": facts,
        "constituent_i03_closure_identity": closure,
        "astra_shaped_empirical_summary": summary,
    }
    audit = {
        "runtime_catalog_identity": producer.LITS_RUNTIME_CATALOG,
        "common_execution_binding": {},
        "current_i05_execution_identity": execution["execution_identity"],
        "astra_shaped_empirical_summary_identity": semantic_hash(summary),
        "constituent_i03_fact_count": 60,
        "constituent_i03_closure_identity": closure,
        "exact_ref_count": len(exact_refs),
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
        "representation_authority": producer.LITS_REPRESENTATION_AUTHORITY_REF.as_dict(),
        "accepted_legacy_facade_blob": producer.LITS_LEGACY_FACADE_BLOB,
    }
    precheck = {
        "schema": "FIABC_LITS_CURRENT_NEUTRAL_I05_PRECHECK@1.0.0",
        "candidate_count": 50,
        "query_role_count": 77,
        "coverage_state_counts": dict(producer.LITS_ACCEPTED_TERMINAL_COUNTS),
        "typed_state_counts": dict(producer.LITS_ACCEPTED_TYPED_TERMINAL_COUNTS),
        "empirical_fact_state_counts": {"SUPPORTED": 60},
        "empirical_facts": [
            {"fact_ref": fact["ref"], "typed_state": fact["typed_state"]}
            for fact in facts
        ],
        "by_rule": [
            {
                "candidate_hash": row["candidate_hash"],
                "rule_id": row["semantic_fields"]["candidate_identity"]["rule_id"],
                "validation": row["semantic_fields"]["candidate_identity"]["validation"],
                "coverage_state": row["semantic_fields"]["coverage_state"],
                "typed_state": row["typed_state"],
            }
            for row in rows
        ],
        "current_semantic_replay_identity": replay,
        "current_execution_identity": execution["execution_identity"],
        "candidate_processes_started": 0,
    }
    return material, audit, execution, precheck


def test_v2_checkpoint_round_trip_binds_parity_ready_summary(tmp_path):
    material, audit, execution, precheck = _fixture()
    path = tmp_path / "checkpoint-v2.json"
    identity, document_sha = producer._write_lits_materialization_checkpoint(
        path=path,
        material=material,
        audit=audit,
        execution_receipt=execution,
        precheck=precheck,
    )
    loaded = producer._load_lits_materialization_checkpoint(path)
    assert loaded[0]["astra_shaped_empirical_summary"] == material["astra_shaped_empirical_summary"]
    assert loaded[1]["astra_shaped_empirical_summary_identity"] == semantic_hash(
        material["astra_shaped_empirical_summary"]
    )
    assert loaded[4] == identity
    assert loaded[5] == document_sha
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["schema"] == producer.LITS_MATERIALIZATION_CHECKPOINT_SCHEMA
    assert doc["schema"].endswith("@2.0.0")


def test_legacy_v1_checkpoint_fails_closed_for_repaired_parity():
    material, audit, execution, precheck = _fixture()
    body = {
        "schema": producer.LITS_LEGACY_MATERIALIZATION_CHECKPOINT_SCHEMA,
        "source_identity": material["source_identity"],
        "material": material,
        "audit": audit,
        "execution_receipt": execution,
        "precheck": precheck,
    }
    with pytest.raises(
        producer.FinalOracleProducerError,
        match="legacy LiTS checkpoint lacks parity-ready empirical summary",
    ):
        producer._validate_lits_materialization_checkpoint_body(body)


def test_v2_summary_tampering_fails_checkpoint_validation():
    material, audit, execution, precheck = _fixture()
    material = copy.deepcopy(material)
    material["astra_shaped_empirical_summary"]["final_envelope"]["EVALUATED_SUPPORTED"] = 48
    body = {
        "schema": producer.LITS_MATERIALIZATION_CHECKPOINT_SCHEMA,
        "source_identity": material["source_identity"],
        "material": material,
        "audit": audit,
        "execution_receipt": execution,
        "precheck": precheck,
    }
    with pytest.raises(producer.FinalOracleProducerError, match="terminal envelope drift"):
        producer._validate_lits_materialization_checkpoint_body(body)


def test_v2_summary_identity_tampering_fails_closed():
    material, audit, execution, precheck = _fixture()
    audit = copy.deepcopy(audit)
    audit["astra_shaped_empirical_summary_identity"] = _h("wrong-summary")
    body = {
        "schema": producer.LITS_MATERIALIZATION_CHECKPOINT_SCHEMA,
        "source_identity": material["source_identity"],
        "material": material,
        "audit": audit,
        "execution_receipt": execution,
        "precheck": precheck,
    }
    with pytest.raises(producer.FinalOracleProducerError, match="summary identity drift"):
        producer._validate_lits_materialization_checkpoint_body(body)


def test_resume_v2_is_zero_source_and_reruns_parity_before_oracle(tmp_path, monkeypatch):
    material, audit, execution, precheck = _fixture()
    checkpoint = tmp_path / "checkpoint-v2.json"
    producer._write_lits_materialization_checkpoint(
        path=checkpoint,
        material=material,
        audit=audit,
        execution_receipt=execution,
        precheck=precheck,
    )

    def forbidden_source(**_kwargs):
        raise AssertionError("resume must not execute source-backed materialization")

    monkeypatch.setattr(producer, "_neutral_lits_material", forbidden_source)
    monkeypatch.setattr(producer, "_git_json", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(producer, "_verified_astra_input_manifest", lambda *_args, **_kwargs: [{"immutable": True}])
    monkeypatch.setattr(
        producer,
        "normalize_accepted_astra_summary",
        lambda **_kwargs: copy.deepcopy(material["astra_shaped_empirical_summary"]),
    )
    parity_called = {"value": False}

    def fake_parity(**kwargs):
        parity_called["value"] = True
        assert kwargs["observed_summary"] == material["astra_shaped_empirical_summary"]
        return {
            "parity_receipt_identity": _h("parity"),
            "expected_empirical_summary_identity": _h("summary"),
            "observed_empirical_summary_identity": _h("summary"),
        }

    monkeypatch.setattr(producer, "assert_lits_astra_substantive_parity", fake_parity)
    monkeypatch.setattr(producer, "build_lits_i_oracle", lambda **_kwargs: {"fake": True})
    monkeypatch.setattr(producer, "verify_frozen_oracle", lambda _doc: _h("oracle"))

    receipt = producer.produce_lits_local_oracle(
        repo_root=tmp_path,
        work_root=tmp_path / "work",
        output_path=tmp_path / "oracle.json",
        resume_checkpoint=checkpoint,
    )
    assert parity_called["value"] is True
    assert receipt["source_access"] == {
        "mode": "RESUME_VERIFIED_PARITY_READY_I05_CHECKPOINT",
        "source_hash_passes": 0,
        "decoder_calls": 0,
    }
    assert receipt["candidate_processes_started"] == 0
    assert receipt["candidate_outputs_seen"] == 0


def test_resume_rejects_source_or_checkpoint_output_mixing(tmp_path):
    material, audit, execution, precheck = _fixture()
    checkpoint = tmp_path / "checkpoint-v2.json"
    producer._write_lits_materialization_checkpoint(
        path=checkpoint,
        material=material,
        audit=audit,
        execution_receipt=execution,
        precheck=precheck,
    )
    with pytest.raises(producer.FinalOracleProducerError, match="may not also specify source"):
        producer.produce_lits_local_oracle(
            source_path=tmp_path / "source.dta",
            repo_root=tmp_path,
            work_root=tmp_path / "work",
            output_path=tmp_path / "oracle.json",
            resume_checkpoint=checkpoint,
        )
