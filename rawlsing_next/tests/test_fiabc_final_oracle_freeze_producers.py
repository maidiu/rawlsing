from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

import rawlsing_next.pre553_independent_parity_oracle as oracle_mod
import rawlsing_next.fiabc_final_oracle_freeze_producers as producer_mod
from rawlsing_next.fiabc_final_oracle_freeze_producers import (
    FinalOracleProducerError,
    LITS_CANDIDATE_COUNT,
    LITS_QUERY_ROLE_COUNT,
    R1M_ORACLE_IDENTITY,
    R1M_TRUTH_IDENTITY,
    SUCCESSOR_DISCOVERY_AUTHORITY,
    SUCCESSOR_LOCK2,
    SUCCESSOR_LOCK2_REPLAY,
    _bind_current_lits_execution_to_astra,
    _reject_candidate_owned_path,
    produce_lits_local_oracle,
    produce_t3_two_source_freeze,
    standardize_wvs_r1m_oracle,
)
from rawlsing_next.pre553_independent_parity_oracle import (
    FreezeContext,
    LITS_C11_RELEASE_IDENTITY,
    LITS_C11_REPLAY_IDENTITY,
    LITS_FRONTIER_SEAL,
    LITS_LEARNED_PRODUCT_IDENTITY,
    LITS_PROJECTION_IDENTITY,
    LITS_SEMANTIC_REPLAY_IDENTITY,
    LITS_SOURCE_SHA256,
    ORACLE_SCHEMA,
    WVS7_SOURCE_SHA256,
    build_lits_i_oracle,
    verify_frozen_oracle,
)

REPO = Path(__file__).resolve().parents[2]
R1M = (
    REPO
    / "WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json"
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _bind_successor_wvs_law(monkeypatch) -> None:
    monkeypatch.setattr(oracle_mod, "WVS7_DISCOVERY_AUTHORITY", SUCCESSOR_DISCOVERY_AUTHORITY)
    monkeypatch.setattr(oracle_mod, "WVS7_LOCK2_IDENTITY", SUCCESSOR_LOCK2)
    monkeypatch.setattr(oracle_mod, "WVS7_LOCK2_REPLAY_IDENTITY", SUCCESSOR_LOCK2_REPLAY)


def _lits_standard_oracle() -> dict:
    hashes = [_h(f"lits-current-{i:02d}") for i in range(LITS_CANDIDATE_COUNT)]
    facts = [
        {
            "candidate_hash": candidate_hash,
            "typed_state": (
                "EVALUATED_VALID_EMPTY"
                if i == LITS_CANDIDATE_COUNT - 1
                else "EVALUATED_SUPPORTED"
            ),
            "semantic_fields": {
                "candidate_identity": {
                    "candidate_hash": candidate_hash,
                    "query_roles": [],
                },
                "constituent_fact_manifest": [],
                "coverage_state": "COMPLETE",
                "support_uncertainty_state": {},
                "replay_ref": {
                    "kind": "ReplayManifest@1.0.0",
                    "object_id": f"urn:test:replay:{i}",
                    "content_hash": _h(f"replay-{i}"),
                },
            },
        }
        for i, candidate_hash in enumerate(hashes)
    ]
    authority_identity = {
        "runtime_catalog_identity": _h("lits-runtime-catalog"),
        "active_binding": _h("lits-active-binding"),
        "runtime_release": _h("lits-runtime-release"),
    }
    workload_identity = {
        "candidate_count": LITS_CANDIDATE_COUNT,
        "query_role_count": LITS_QUERY_ROLE_COUNT,
        "frontier_seal": LITS_FRONTIER_SEAL,
        "ordered_candidate_hashes": hashes,
    }
    prior_product = {
        "schema": "ASTRA_D04_R2_TYPED_LEARNED_EMPIRICAL_PRODUCT@1.0.0",
        "full_execution_product_sha256": LITS_LEARNED_PRODUCT_IDENTITY,
        "semantic_replay_hash": LITS_SEMANTIC_REPLAY_IDENTITY,
        "terminal_counts": {
            "EVALUATED_SUPPORTED": 49,
            "EVALUATED_VALID_EMPTY": 1,
        },
        "frontier": {
            "candidate_count": LITS_CANDIDATE_COUNT,
            "query_role_count": LITS_QUERY_ROLE_COUNT,
            "preexecution_seal": LITS_FRONTIER_SEAL,
        },
    }
    prior_replay = {
        "source": {"sha256": LITS_SOURCE_SHA256},
        "execution": {
            "byte_identical": True,
            "run_1_output_sha256": LITS_LEARNED_PRODUCT_IDENTITY,
            "run_2_output_sha256": LITS_LEARNED_PRODUCT_IDENTITY,
        },
        "preoutcome": {
            "candidate_count": LITS_CANDIDATE_COUNT,
            "query_role_count": LITS_QUERY_ROLE_COUNT,
            "frontier_seal": LITS_FRONTIER_SEAL,
        },
    }
    return build_lits_i_oracle(
        prior_product=prior_product,
        prior_replay_receipt=prior_replay,
        source_identity={
            "source": "LITS_I",
            "sha256": LITS_SOURCE_SHA256,
            "rows": 29002,
            "variables": 1198,
        },
        court_constitution_refs={
            "frozen_authority_identity": authority_identity,
            "frozen_workload_identity": workload_identity,
        },
        semantic_authority_closure=[
            {
                "kind": "AuthoritySnapshot@1.0.0",
                "object_id": "urn:test:lits:authority",
                "content_hash": _h("lits-authority"),
            }
        ],
        projection_and_release_refs={
            "projection_identity": LITS_PROJECTION_IDENTITY,
            "c11_release_identity": LITS_C11_RELEASE_IDENTITY,
            "c11_replay_identity": LITS_C11_REPLAY_IDENTITY,
        },
        frontier_manifest=workload_identity,
        comparison_fact_manifest=facts,
        expected_learned_product={
            "product_identity": LITS_LEARNED_PRODUCT_IDENTITY,
            "semantic_identity": LITS_SEMANTIC_REPLAY_IDENTITY,
            "replay_identity": _h("lits-current-replay"),
            "exact_output_identity": _h("lits-current-output"),
            "coverage": {
                "candidate_count": LITS_CANDIDATE_COUNT,
                "query_role_count": LITS_QUERY_ROLE_COUNT,
                "typed_terminal_counts": {
                    "EVALUATED_SUPPORTED": 49,
                    "EVALUATED_VALID_EMPTY": 1,
                },
            },
        },
        replay_manifest={
            "i05_replay_ref": {
                "kind": "ReplayManifest@1.0.0",
                "object_id": "urn:test:lits:i05",
                "content_hash": LITS_SEMANTIC_REPLAY_IDENTITY,
            },
            "constituent_i03_closure_identity": _h("lits-i03-closure"),
            "dependency_root": _h("lits-dependency-root"),
        },
        exact_ref_manifest=[
            {
                "kind": "EmpiricalQuerySpec@1.0.0",
                "object_id": "urn:test:lits:query",
                "content_hash": _h("lits-query"),
            }
        ],
        oracle_build_provenance={
            "builder": "SOURCE_FREE_TEST_FIXTURE",
            "dependencies": [
                {"owner_class": "EXACT_SOURCE", "identity": LITS_SOURCE_SHA256},
                {"owner_class": "ACCEPTED_AUTHORITY", "identity": _h("lits-authority-root")},
            ],
            "candidate_outputs_used": [],
            "pairwise_candidate_vote": False,
            "first_successful_candidate_as_golden": False,
        },
        freeze=FreezeContext(freeze_sequence=30),
    )


def _write(path: Path, doc: dict) -> None:
    path.write_text(
        json.dumps(doc, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _lits_materialization_checkpoint_fixture() -> tuple[dict, dict, dict, dict]:
    fact_rows = [
        {
            "ref": {
                "kind": "EmpiricalFact@1.0.0",
                "object_id": f"urn:test:lits:checkpoint-fact:{i:02d}",
                "content_hash": _h(f"checkpoint-fact-{i:02d}"),
            },
            "typed_state": "SUPPORTED",
        }
        for i in range(60)
    ]
    fact_rows.sort(key=lambda fact: producer_mod._ref_key(fact["ref"]))
    execution_body = {
        "schema": "PRE553_LEARNED_EMPIRICAL_EXECUTION_RECEIPT@1.0.0",
        "claim_kind": "LEARNED_EMPIRICAL_EXECUTION_ONLY",
        "candidate_count": 50,
    }
    execution = {
        **execution_body,
        "execution_identity": oracle_mod.semantic_hash(execution_body),
    }
    semantic_replay = _h("checkpoint-semantic-replay")

    candidate_rows = []
    assigned_facts = []
    fact_cursor = 0
    for index in range(50):
        candidate_hash = _h(f"checkpoint-candidate-{index:02d}")
        fact_count = 2 if index < 10 else 1
        constituent = fact_rows[fact_cursor:fact_cursor + fact_count]
        fact_cursor += fact_count
        assigned_facts.extend(constituent)
        query_roles = [
            {"role": f"query-role-{index:02d}-{role}"}
            for role in range(2 if index < 27 else 1)
        ]
        coverage = "EVALUATED_VALID_EMPTY" if index == 49 else "EVALUATED_SUPPORTED"
        typed = "VALID_EMPTY" if index == 49 else "DISCOVERED_RESULT_SUPPORTED"
        identity = {
            "candidate_hash": candidate_hash,
            "rule_id": f"TEST_RULE_{index:02d}",
            "validation": {"kind": "TEST_VALIDATION", "ordinal": index},
            "query_roles": query_roles,
        }
        candidate_rows.append({
            "candidate_hash": candidate_hash,
            "typed_state": typed,
            "semantic_fields": {
                "candidate_identity": identity,
                "constituent_fact_manifest": constituent,
                "coverage_state": coverage,
                "support_uncertainty_state": {},
                "replay_ref": {
                    "kind": "ReplayManifest@1.0.0",
                    "object_id": f"urn:test:lits:checkpoint-replay:{index:02d}",
                    "content_hash": _h(f"checkpoint-replay-{index:02d}"),
                },
            },
        })

    closure_identity = oracle_mod.semantic_hash({
        "candidate_fact_rows": candidate_rows,
        "constituent_fact_manifest": fact_rows,
    })
    frontier = {
        "candidate_count": 50,
        "query_role_count": 77,
        "frontier_seal": LITS_FRONTIER_SEAL,
        "ordered_candidate_hashes": [row["candidate_hash"] for row in candidate_rows],
    }
    learned = _bind_current_lits_execution_to_astra(
        execution_receipt=execution,
        semantic_replay_identity=semantic_replay,
        terminal_counts={
            "EVALUATED_SUPPORTED": 49,
            "EVALUATED_VALID_EMPTY": 1,
        },
        candidate_count=50,
        query_role_count=77,
    )
    exact_refs = [{
        "kind": "EmpiricalQuerySpec@1.0.0",
        "object_id": "urn:test:lits:checkpoint-query",
        "content_hash": _h("checkpoint-query"),
    }]
    material = {
        "source_identity": {
            "source": "LITS_I",
            "sha256": LITS_SOURCE_SHA256,
            "rows": 29002,
            "variables": 1198,
        },
        "court_constitution_refs": {
            "frozen_authority_identity": producer_mod._neutral_lits_authority_identity(),
            "frozen_workload_identity": frontier,
        },
        "semantic_authority_closure": [{
            "kind": "AuthoritySnapshot@1.0.0",
            "object_id": "urn:test:lits:checkpoint-authority",
            "content_hash": _h("checkpoint-authority"),
        }],
        "projection_and_release_refs": {
            "projection_identity": LITS_PROJECTION_IDENTITY,
            "c11_release_identity": producer_mod.LITS_RUNTIME_RELEASE,
            "c11_replay_identity": producer_mod.LITS_RUNTIME_REPLAY,
        },
        "frontier_manifest": frontier,
        "comparison_fact_manifest": candidate_rows,
        "expected_learned_product": learned,
        "replay_manifest": {
            "i05_replay_ref": {
                "kind": "ReplayManifest@1.0.0",
                "object_id": "urn:test:lits:checkpoint-i05",
                "content_hash": semantic_replay,
            },
            "constituent_i03_closure_identity": closure_identity,
            "dependency_root": _h("checkpoint-dependency-root"),
        },
        "exact_ref_manifest": exact_refs,
        "constituent_i03_fact_manifest": fact_rows,
        "constituent_i03_closure_identity": closure_identity,
    }
    audit = {
        "runtime_catalog_identity": producer_mod.LITS_RUNTIME_CATALOG,
        "common_execution_binding": {},
        "current_i05_execution_identity": execution["execution_identity"],
        "constituent_i03_fact_count": 60,
        "constituent_i03_closure_identity": closure_identity,
        "exact_ref_count": len(exact_refs),
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
        "representation_authority": producer_mod.LITS_REPRESENTATION_AUTHORITY_REF.as_dict(),
        "accepted_legacy_facade_blob": producer_mod.LITS_LEGACY_FACADE_BLOB,
    }
    precheck = {
        "schema": "FIABC_LITS_CURRENT_NEUTRAL_I05_PRECHECK@1.0.0",
        "candidate_count": 50,
        "query_role_count": 77,
        "coverage_state_counts": {
            "EVALUATED_SUPPORTED": 49,
            "EVALUATED_VALID_EMPTY": 1,
        },
        "typed_state_counts": {
            "DISCOVERED_RESULT_SUPPORTED": 49,
            "VALID_EMPTY": 1,
        },
        "empirical_fact_state_counts": {"SUPPORTED": 60},
        "empirical_facts": [
            {"fact_ref": fact["ref"], "typed_state": fact["typed_state"]}
            for fact in fact_rows
        ],
        "by_rule": [
            {
                "candidate_hash": row["candidate_hash"],
                "rule_id": row["semantic_fields"]["candidate_identity"]["rule_id"],
                "validation": row["semantic_fields"]["candidate_identity"]["validation"],
                "coverage_state": row["semantic_fields"]["coverage_state"],
                "typed_state": row["typed_state"],
            }
            for row in candidate_rows
        ],
        "current_semantic_replay_identity": semantic_replay,
        "current_execution_identity": execution["execution_identity"],
        "candidate_processes_started": 0,
    }
    return material, audit, execution, precheck


def test_wvs_r1m_standardization_is_source_free_deterministic_and_live_schema(
    tmp_path, monkeypatch
):
    _bind_successor_wvs_law(monkeypatch)
    first = tmp_path / "wvs-1.json"
    second = tmp_path / "wvs-2.json"

    r1 = standardize_wvs_r1m_oracle(r1m_path=R1M, output_path=first)
    r2 = standardize_wvs_r1m_oracle(r1m_path=R1M, output_path=second)

    assert first.read_bytes() == second.read_bytes()
    assert r1["source_free"] is True
    assert r1["candidate_processes_started"] == 0
    assert r1["candidate_outputs_seen"] == 0
    assert r1["candidate_owned_roots_consulted"] == []
    assert r1["standard_oracle_identity_sha256"] == r2["standard_oracle_identity_sha256"]
    doc = json.loads(first.read_text(encoding="utf-8"))
    assert doc["schema"] == ORACLE_SCHEMA
    assert doc["source"] == "WVS7"
    assert doc["source_identity"]["sha256"] == WVS7_SOURCE_SHA256
    assert verify_frozen_oracle(doc) == doc["oracle_identity_sha256"]


def test_wvs_adapter_rejects_predecessor_or_wrong_wrapper(tmp_path, monkeypatch):
    _bind_successor_wvs_law(monkeypatch)
    doc = json.loads(R1M.read_text(encoding="utf-8"))
    bad = copy.deepcopy(doc)
    bad["schema"] = "FIABC_LM2_R1L_PREDECESSOR_ORACLE@1.0.0"
    path = tmp_path / "bad.json"
    _write(path, bad)
    with pytest.raises(FinalOracleProducerError):
        standardize_wvs_r1m_oracle(r1m_path=path, output_path=tmp_path / "out.json")


def test_wvs_adapter_rejects_predecessor_authority_label(tmp_path, monkeypatch):
    _bind_successor_wvs_law(monkeypatch)
    doc = json.loads(R1M.read_text(encoding="utf-8"))
    doc["successor_lock2"] = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
    path = tmp_path / "predecessor.json"
    _write(path, doc)
    with pytest.raises(FinalOracleProducerError):
        standardize_wvs_r1m_oracle(r1m_path=path, output_path=tmp_path / "out.json")


def test_wvs_adapter_binds_exact_accepted_r1m_identities():
    doc = json.loads(R1M.read_text(encoding="utf-8"))
    assert doc["oracle_identity_sha256"] == R1M_ORACLE_IDENTITY
    assert doc["truth_payload_identity"] == R1M_TRUTH_IDENTITY
    assert doc["successor_discovery_authority"] == SUCCESSOR_DISCOVERY_AUTHORITY
    assert doc["successor_lock2"] == SUCCESSOR_LOCK2


def test_lits_producer_hard_codes_exact_50_77_and_rejects_candidate_roots(tmp_path):
    assert LITS_CANDIDATE_COUNT == 50
    assert LITS_QUERY_ROLE_COUNT == 77
    work = tmp_path / "court"
    candidate_owned = work / "cells" / "LITS_I" / "A" / "durable" / "oracle.json"
    candidate_owned.parent.mkdir(parents=True)
    candidate_owned.write_text("{}")
    with pytest.raises(FinalOracleProducerError):
        _reject_candidate_owned_path(candidate_owned, work, "test")

    producer_text = (
        REPO / "rawlsing_next/fiabc_final_oracle_freeze_producers.py"
    ).read_text(encoding="utf-8")
    assert "compose_p2r1_binding" not in producer_text
    assert "candidate_processes_started" in producer_text
    assert "candidate_outputs_used" in producer_text


def test_lits_materialization_checkpoint_resumes_without_source_or_decode(tmp_path, monkeypatch):
    material, audit, execution, precheck = _lits_materialization_checkpoint_fixture()
    checkpoint = tmp_path / "current_i05_materialization_checkpoint.json"
    checkpoint_identity, checkpoint_sha = producer_mod._write_lits_materialization_checkpoint(
        path=checkpoint,
        material=material,
        audit=audit,
        execution_receipt=execution,
        precheck=precheck,
    )
    loaded = producer_mod._load_lits_materialization_checkpoint(checkpoint)
    assert loaded[4] == checkpoint_identity
    assert loaded[5] == checkpoint_sha
    assert loaded[0] == material

    monkeypatch.setattr(
        producer_mod,
        "_neutral_lits_material",
        lambda **_kwargs: pytest.fail("resume must not reopen or decode the source"),
    )
    monkeypatch.setattr(producer_mod, "_git_json", lambda *_args: {})
    monkeypatch.setattr(
        producer_mod,
        "build_lits_i_oracle",
        lambda **_kwargs: {"oracle_identity_sha256": _h("resumed-oracle")},
    )
    monkeypatch.setattr(
        producer_mod,
        "verify_frozen_oracle",
        lambda frozen: frozen["oracle_identity_sha256"],
    )

    receipt = produce_lits_local_oracle(
        repo_root=REPO,
        work_root=tmp_path / "resume-work",
        output_path=tmp_path / "resumed-oracle.json",
        resume_checkpoint=checkpoint,
    )
    assert receipt["status"] == "PASS"
    assert receipt["materialization_checkpoint_sha256"] == checkpoint_identity
    assert receipt["source_access"] == {
        "mode": "RESUME_VERIFIED_I05_CHECKPOINT",
        "source_hash_passes": 0,
        "decoder_calls": 0,
    }


def test_lits_materialization_checkpoint_tampering_fails_closed(tmp_path):
    material, audit, execution, precheck = _lits_materialization_checkpoint_fixture()
    checkpoint = tmp_path / "checkpoint.json"
    producer_mod._write_lits_materialization_checkpoint(
        path=checkpoint,
        material=material,
        audit=audit,
        execution_receipt=execution,
        precheck=precheck,
    )
    doc = json.loads(checkpoint.read_text(encoding="utf-8"))
    doc["precheck"]["candidate_count"] = 49
    _write(checkpoint, doc)

    with pytest.raises(FinalOracleProducerError, match="checkpoint digest mismatch"):
        producer_mod._load_lits_materialization_checkpoint(checkpoint)


def test_lits_current_execution_preserves_current_identity_domains():
    current_execution = _h("current-neutral-execution")
    current_semantic = _h("current-neutral-semantic-replay")
    execution_receipt = {"execution_identity": current_execution}
    learned = _bind_current_lits_execution_to_astra(
        execution_receipt=execution_receipt,
        semantic_replay_identity=current_semantic,
        terminal_counts={
            "EVALUATED_SUPPORTED": 49,
            "EVALUATED_VALID_EMPTY": 1,
        },
        candidate_count=LITS_CANDIDATE_COUNT,
        query_role_count=LITS_QUERY_ROLE_COUNT,
    )
    assert learned["product_identity"] == oracle_mod.semantic_hash(execution_receipt)
    assert learned["semantic_identity"] == current_semantic
    assert learned["replay_identity"] == current_execution
    assert learned["exact_output_identity"] == current_execution


@pytest.mark.parametrize(
    ("semantic_identity", "terminal_counts"),
    [
        (
            "malformed",
            {"EVALUATED_SUPPORTED": 49, "EVALUATED_VALID_EMPTY": 1},
        ),
        (
            LITS_SEMANTIC_REPLAY_IDENTITY,
            {"EVALUATED_SUPPORTED": 50},
        ),
    ],
)
def test_lits_current_execution_rejects_current_identity_or_coverage_drift(
    semantic_identity, terminal_counts
):
    with pytest.raises(FinalOracleProducerError):
        _bind_current_lits_execution_to_astra(
            execution_receipt={"execution_identity": _h("current-neutral-execution")},
            semantic_replay_identity=semantic_identity,
            terminal_counts=terminal_counts,
            candidate_count=LITS_CANDIDATE_COUNT,
            query_role_count=LITS_QUERY_ROLE_COUNT,
        )

def test_t3_two_source_freeze_self_validates_zero_candidate_output(
    tmp_path, monkeypatch
):
    _bind_successor_wvs_law(monkeypatch)
    work = tmp_path / "court"
    oracle_root = work / "oracle"
    oracle_root.mkdir(parents=True)

    wvs_path = oracle_root / "wvs.json"
    standardize_wvs_r1m_oracle(r1m_path=R1M, output_path=wvs_path)
    lits_path = oracle_root / "lits.json"
    _write(lits_path, _lits_standard_oracle())

    freeze_path = work / "t3" / "frozen-upstream.json"
    receipt = produce_t3_two_source_freeze(
        lits_oracle_path=lits_path,
        wvs_oracle_path=wvs_path,
        work_root=work,
        output_path=freeze_path,
    )
    doc = json.loads(freeze_path.read_text(encoding="utf-8"))
    assert doc["candidate_neutral"] is True
    assert doc["frozen_before_candidate_execution"] is True
    assert doc["candidate_outputs_seen"] == 0
    assert doc["candidate_owned_roots_consulted"] == []
    assert doc["candidate_owned_state_reused"] is False
    assert doc["state"] == "FROZEN_READ_ONLY"
    assert doc["freeze_order"] == {
        "source_identity_freeze_sequence": 10,
        "authority_workload_freeze_sequence": 20,
        "oracle_materialize_freeze_sequence": 30,
    }
    assert receipt["freeze_document_sha256"] == hashlib.sha256(
        freeze_path.read_bytes()
    ).hexdigest()


def test_t3_rejects_nonstandard_oracle_document(tmp_path):
    work = tmp_path / "court"
    work.mkdir()
    bad = work / "bad.json"
    _write(
        bad,
        {
            "schema": "FIABC_LM2_R1M_FRESH_WVS_ORACLE@1.0.0",
            "source": "WVS7",
        },
    )
    lits = work / "lits.json"
    _write(lits, _lits_standard_oracle())
    with pytest.raises(FinalOracleProducerError):
        produce_t3_two_source_freeze(
            lits_oracle_path=lits,
            wvs_oracle_path=bad,
            work_root=work,
            output_path=work / "freeze.json",
        )


def test_t3_rejects_oracle_inside_candidate_owned_root(tmp_path):
    work = tmp_path / "court"
    candidate_root = work / "cells" / "LITS_I" / "A"
    candidate_root.mkdir(parents=True)
    lits = candidate_root / "oracle.json"
    _write(lits, _lits_standard_oracle())
    wvs = work / "wvs.json"
    _write(wvs, {"schema": ORACLE_SCHEMA, "source": "WVS7"})
    with pytest.raises(FinalOracleProducerError):
        produce_t3_two_source_freeze(
            lits_oracle_path=lits,
            wvs_oracle_path=wvs,
            work_root=work,
            output_path=work / "freeze.json",
        )


def test_t3_rejects_missing_oracle_document(tmp_path):
    work = tmp_path / "court"
    work.mkdir()
    lits = work / "lits.json"
    _write(lits, _lits_standard_oracle())
    with pytest.raises(FinalOracleProducerError):
        produce_t3_two_source_freeze(
            lits_oracle_path=lits,
            wvs_oracle_path=work / "missing-wvs.json",
            work_root=work,
            output_path=work / "freeze.json",
        )


def test_t3_rejects_mutated_unverified_oracle(tmp_path):
    work = tmp_path / "court"
    work.mkdir()
    lits = work / "lits.json"
    doc = _lits_standard_oracle()
    doc["expected_fact_manifest"][0]["typed_state"] = "MUTATED_AFTER_FREEZE"
    _write(lits, doc)
    with pytest.raises(Exception, match="frozen oracle|mutated"):
        produce_t3_two_source_freeze(
            lits_oracle_path=lits,
            wvs_oracle_path=work / "unused-wvs.json",
            work_root=work,
            output_path=work / "freeze.json",
        )
