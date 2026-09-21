from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import types
from typing import Any, Mapping, Sequence

import rawlsing_next.pre553_independent_parity_oracle as oracle_mod
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.pre553_independent_parity_oracle import (
    FreezeContext,
    LITS_ASTRA_D04_R2_COMMIT,
    LITS_FRONTIER_SEAL,
    LITS_LEARNED_PRODUCT_IDENTITY,
    LITS_SEMANTIC_REPLAY_IDENTITY,
    LITS_SOURCE_SHA256,
    ORACLE_SCHEMA,
    WVS7_SOURCE_SHA256,
    WVS_MATERIALIZER_CONTRACT,
    build_lits_i_oracle,
    freeze_wvs7_oracle_from_common_material,
    verify_frozen_oracle,
)
from rawlsing_next.ee_p2x_candidate_process_envelope import (
    FREEZE_RECEIPT_SCHEMA,
    load_frozen_upstream_receipt,
)

PRODUCER_SCHEMA = "RAWLSING_FIABC_FINAL_ORACLE_FREEZE_PRODUCERS@1.0.0"
R1M_SCHEMA = "FIABC_LM2_R1M_FRESH_WVS_ORACLE@1.0.0"
R1M_TRUTH_SCHEMA = "FIABC_LM2_R1M_WVS_TRUTH_PAYLOAD@1.0.0"
R1M_ORACLE_IDENTITY = "3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800"
R1M_TRUTH_IDENTITY = "eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405"
SUCCESSOR_DISCOVERY_AUTHORITY = "3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873"
SUCCESSOR_LOCK2 = "5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139"
SUCCESSOR_LOCK2_REPLAY = "9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a"

LITS_RUNTIME_CATALOG = "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02"
LITS_ACTIVE_BINDING = "a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308"
LITS_RUNTIME_RELEASE = "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f"
LITS_ROWS = 29002
LITS_VARIABLES = 1198
WVS_ROWS = 97220
WVS_VARIABLES = 613

ASTRA_PRODUCT_PATH = "WORKER_RETURNS/ASTRA-D04-R2/01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json"
ASTRA_REPLAY_PATH = "WORKER_RETURNS/ASTRA-D04-R2/03_SOURCE_AND_REPLAY_RECEIPT.json"
CURRENT_SOURCE_MANIFEST_REF = "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json#source_root_law.canonical_source_sha256"


class FinalOracleProducerError(RuntimeError):
    pass


def _canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def _write_json(path: Path, value: Any) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _canonical_bytes(value)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(payload)
    os.replace(tmp, path)
    return hashlib.sha256(payload).hexdigest()


def _load_json(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise FinalOracleProducerError(f"invalid JSON: {path}") from exc
    if not isinstance(value, Mapping):
        raise FinalOracleProducerError(f"JSON object required: {path}")
    return value


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_json(repo_root: Path, commit: str, path: str) -> Mapping[str, Any]:
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(Path(repo_root).resolve()), "show", f"{commit}:{path}"],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        raise FinalOracleProducerError(
            f"required immutable historical input unavailable at {commit}:{path}"
        ) from exc
    value = json.loads(raw)
    if not isinstance(value, Mapping):
        raise FinalOracleProducerError("historical JSON input is not an object")
    return value


def _candidate_cells_root(work_root: Path) -> Path:
    return (Path(work_root).resolve() / "cells").resolve()


def _reject_candidate_owned_path(path: Path, work_root: Path, label: str) -> None:
    p = Path(path).resolve()
    cells = _candidate_cells_root(work_root)
    if p == cells or cells in p.parents:
        raise FinalOracleProducerError(f"{label} may not reside in candidate-owned cells root")


def _check_zero_candidate_provenance(value: Mapping[str, Any], label: str) -> None:
    if value.get("candidate_outputs_seen") != 0:
        raise FinalOracleProducerError(f"{label} observed candidate output")
    if value.get("candidate_owned_roots_consulted") not in ([], ()):
        raise FinalOracleProducerError(f"{label} consulted candidate-owned roots")
    if value.get("candidate_owned_state_reused") is not False:
        raise FinalOracleProducerError(f"{label} reused candidate-owned state")
    processes = value.get("candidate_processes_started")
    if processes not in (None, 0):
        raise FinalOracleProducerError(f"{label} started candidate processes")


def _load_accepted_r1m(path: Path) -> Mapping[str, Any]:
    doc = _load_json(path)
    if doc.get("schema") != R1M_SCHEMA or doc.get("source") != "WVS7":
        raise FinalOracleProducerError("accepted R1M WVS wrapper schema/source drift")
    if doc.get("status") != "PASS__FROZEN_BEFORE_CANDIDATE_EXECUTION":
        raise FinalOracleProducerError("accepted R1M WVS wrapper is not frozen PASS")
    if doc.get("successor_discovery_authority") != SUCCESSOR_DISCOVERY_AUTHORITY:
        raise FinalOracleProducerError("R1M successor DiscoveryAuthority drift")
    if doc.get("successor_lock2") != SUCCESSOR_LOCK2:
        raise FinalOracleProducerError("R1M successor Lock2 drift")
    if doc.get("oracle_identity_sha256") != R1M_ORACLE_IDENTITY:
        raise FinalOracleProducerError("R1M accepted wrapper identity drift")
    if doc.get("truth_payload_identity") != R1M_TRUTH_IDENTITY:
        raise FinalOracleProducerError("R1M accepted truth identity drift")
    _check_zero_candidate_provenance(doc, "R1M wrapper")
    freeze = doc.get("freeze_receipt")
    if not isinstance(freeze, Mapping):
        raise FinalOracleProducerError("R1M freeze receipt missing")
    _check_zero_candidate_provenance(freeze, "R1M freeze receipt")

    body = {
        key: value
        for key, value in doc.items()
        if key not in {"oracle_identity_sha256", "freeze_receipt"}
    }
    if semantic_hash(canonicalize(body)) != R1M_ORACLE_IDENTITY:
        raise FinalOracleProducerError("R1M wrapper semantic identity mismatch")
    truth = doc.get("truth_payload")
    if not isinstance(truth, Mapping) or truth.get("schema") != R1M_TRUTH_SCHEMA:
        raise FinalOracleProducerError("R1M truth payload schema drift")
    if semantic_hash(canonicalize(truth)) != R1M_TRUTH_IDENTITY:
        raise FinalOracleProducerError("R1M truth payload semantic identity mismatch")
    source = truth.get("source_identity")
    if source != {
        "source": "WVS7",
        "sha256": WVS7_SOURCE_SHA256,
        "rows": WVS_ROWS,
        "variables": WVS_VARIABLES,
    }:
        raise FinalOracleProducerError("R1M WVS source identity drift")
    return doc


def _assert_live_successor_oracle_law() -> None:
    expected = {
        "WVS7_DISCOVERY_AUTHORITY": SUCCESSOR_DISCOVERY_AUTHORITY,
        "WVS7_LOCK2_IDENTITY": SUCCESSOR_LOCK2,
        "WVS7_LOCK2_REPLAY_IDENTITY": SUCCESSOR_LOCK2_REPLAY,
    }
    for name, value in expected.items():
        if getattr(oracle_mod, name) != value:
            raise FinalOracleProducerError(
                f"live standard oracle law has not been rebound to accepted successor: {name}"
            )


def standardize_wvs_r1m_oracle(
    *, r1m_path: Path, output_path: Path, freeze_sequence: int = 30
) -> Mapping[str, Any]:
    """Source-free R1M successor oracle -> standard live T3/T5 oracle."""
    doc = _load_accepted_r1m(Path(r1m_path))
    truth = doc["truth_payload"]
    court = truth["court_constitution_refs"]
    if court.get("successor_discovery_authority") != SUCCESSOR_DISCOVERY_AUTHORITY:
        raise FinalOracleProducerError("R1M truth successor DiscoveryAuthority drift")
    if court.get("successor_lock2_hash") != SUCCESSOR_LOCK2:
        raise FinalOracleProducerError("R1M truth successor Lock2 drift")
    if court.get("successor_lock2_replay_hash") != SUCCESSOR_LOCK2_REPLAY:
        raise FinalOracleProducerError("R1M truth successor Lock2 replay drift")

    authority_identity = canonicalize(court)
    workload_identity = canonicalize(truth["frontier_manifest"])
    standard_court = {
        "frozen_authority_identity": authority_identity,
        "frozen_workload_identity": workload_identity,
        "lock2_hash": court["successor_lock2_hash"],
        "lock2_replay_hash": court["successor_lock2_replay_hash"],
        "discovery_authority": court["successor_discovery_authority"],
        "empirical_universe": court["empirical_universe"],
        "risk_set": court["risk_set"],
        "measure_basis": court["measure_basis"],
    }
    material = {
        "contract": WVS_MATERIALIZER_CONTRACT,
        "source_identity": canonicalize(truth["source_identity"]),
        "court_constitution_refs": canonicalize(standard_court),
        "semantic_authority_closure": canonicalize(truth["semantic_authority_closure"]),
        "projection_and_release_refs": canonicalize(truth["projection_and_release_refs"]),
        "frontier_manifest": canonicalize(truth["frontier_manifest"]),
        "expected_fact_manifest": canonicalize(truth["expected_fact_manifest"]),
        "expected_learned_product": canonicalize(truth["expected_learned_product"]),
        "replay_manifest": canonicalize(truth["replay_manifest"]),
        "exact_ref_manifest": canonicalize(truth["exact_ref_manifest"]),
        "oracle_build_provenance": canonicalize(truth["oracle_build_provenance"]),
    }
    _assert_live_successor_oracle_law()
    frozen = freeze_wvs7_oracle_from_common_material(
        material=material,
        freeze=FreezeContext(freeze_sequence=freeze_sequence),
    )
    identity = verify_frozen_oracle(frozen)
    if frozen.get("schema") != ORACLE_SCHEMA or frozen.get("source") != "WVS7":
        raise FinalOracleProducerError("standardized WVS oracle schema/source drift")
    output_sha = _write_json(Path(output_path), frozen)
    return {
        "schema": PRODUCER_SCHEMA,
        "operation": "STANDARDIZE_WVS_R1M_SUCCESSOR_ORACLE",
        "status": "PASS",
        "source": "WVS7",
        "source_free": True,
        "r1m_oracle_identity": R1M_ORACLE_IDENTITY,
        "r1m_truth_payload_identity": R1M_TRUTH_IDENTITY,
        "standard_oracle_identity_sha256": identity,
        "standard_oracle_document_sha256": output_sha,
        "output_path": str(Path(output_path)),
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
    }


def _neutral_lits_authority_identity() -> Mapping[str, Any]:
    return {
        "runtime_catalog_identity": LITS_RUNTIME_CATALOG,
        "active_binding": LITS_ACTIVE_BINDING,
        "runtime_release": LITS_RUNTIME_RELEASE,
    }


def _neutral_lits_material(
    *,
    source_path: Path,
    repo_root: Path,
    work_root: Path,
) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    """Execute the common LiTS semantic path without composing A/B/C."""
    from rawlsing_next.pre553_physical_decoder import decode_dta
    from rawlsing_next.pre553_source_backed_c11_facade import (
        build_source_backed_c11_repository,
    )
    from rawlsing_next.pre553_carrier_execution import (
        CarrierNeutralResearchExecutor,
        RuntimeObjectCatalog,
        learned_empirical_execution_receipt,
    )
    from rawlsing_next.pre553_runtime_context import bind_runtime
    import rawlsing_next.ee_p2x_darwin_stage_backend as backend
    import rawlsing_next.fiabc_live_terminal_control as terminal

    source_path = Path(source_path).resolve()
    repo_root = Path(repo_root).resolve()
    work_root = Path(work_root).resolve()
    if not source_path.is_file():
        raise FinalOracleProducerError("LiTS exact source file is required")
    _reject_candidate_owned_path(source_path, work_root, "LiTS source")
    if _sha256_file(source_path) != LITS_SOURCE_SHA256:
        raise FinalOracleProducerError("LiTS canonical source sha256 drift")

    neutral_root = work_root / "court" / "oracle_producers" / "LITS_I"
    _reject_candidate_owned_path(neutral_root, work_root, "LiTS neutral producer root")
    neutral_root.mkdir(parents=True, exist_ok=True)

    incidence = decode_dta(source_path, encoding="latin1")
    if incidence.source_sha256 != LITS_SOURCE_SHA256:
        raise FinalOracleProducerError("LiTS decoder source identity drift")
    if incidence.row_count != LITS_ROWS or len(incidence.variables) != LITS_VARIABLES:
        raise FinalOracleProducerError("LiTS decoder source shape drift")

    ctx = types.SimpleNamespace(work_root=neutral_root)
    services = types.SimpleNamespace(repo_root=repo_root)
    projection, _pctx, _banked = backend._lits_projection(ctx, services, {}, incidence)
    runtime = backend._lits_runtime(ctx, services, projection)

    repository, release = build_source_backed_c11_repository(incidence, projection)
    catalog = RuntimeObjectCatalog.from_documents(
        authority_documents=runtime["authorities"],
        predicate_documents=runtime["predicates"],
        query_documents=runtime["queries"],
        discovery_authority_documents=runtime["discoveries"],
    )
    if catalog.receipt()["catalog_identity"] != LITS_RUNTIME_CATALOG:
        raise FinalOracleProducerError("LiTS current runtime catalog identity drift")
    executor = CarrierNeutralResearchExecutor(
        repository=repository,
        release_refs=(release.release_ref,),
        runtime_catalog=catalog,
    )
    discovery_refs = catalog.discovery_authority_refs
    if len(discovery_refs) != 1:
        raise FinalOracleProducerError("LiTS runtime must expose exactly one DiscoveryAuthority")
    with bind_runtime(runtime["runtime_authority_set"]):
        result = executor.execute_i05(discovery_authority_ref=discovery_refs[0])
    execution_receipt = learned_empirical_execution_receipt(result)

    binding = types.SimpleNamespace(executor=executor)
    state = {"bindings": {"projection_identity": projection.cache_identity}}
    projection_refs = terminal._projection_refs("LITS_I", binding, state)
    candidate_rows, constituent_facts, i03_closure = terminal._constituent_i03(binding, result)

    ordered = sorted(
        result.receipts, key=lambda receipt: receipt.candidate_identity["candidate_hash"]
    )
    hashes = [receipt.candidate_identity["candidate_hash"] for receipt in ordered]
    query_role_count = sum(
        len(receipt.candidate_identity["query_roles"]) for receipt in ordered
    )
    frontier = {
        "candidate_count": result.candidate_count,
        "query_role_count": query_role_count,
        "frontier_seal": LITS_FRONTIER_SEAL,
        "ordered_candidate_hashes": hashes,
    }
    if result.candidate_count != 50 or query_role_count != 77:
        raise FinalOracleProducerError("LiTS current neutral runtime is not exact 50/77")

    terminal_counts = dict(
        sorted(Counter(receipt.typed_state for receipt in ordered).items())
    )
    learned = {
        "product_identity": semantic_hash(execution_receipt),
        "semantic_identity": result.replay_ref.content_hash,
        "replay_identity": execution_receipt["execution_identity"],
        "exact_output_identity": execution_receipt["execution_identity"],
        "coverage": {
            "candidate_count": result.candidate_count,
            "query_role_count": query_role_count,
            "typed_terminal_counts": terminal_counts,
        },
    }
    if learned["product_identity"] != LITS_LEARNED_PRODUCT_IDENTITY:
        raise FinalOracleProducerError(
            "current neutral LiTS learned product does not equal accepted ASTRA identity"
        )
    if learned["semantic_identity"] != LITS_SEMANTIC_REPLAY_IDENTITY:
        raise FinalOracleProducerError(
            "current neutral LiTS semantic replay does not equal accepted ASTRA identity"
        )

    authorities = [authority.ref.as_dict() for authority in catalog.authorities]
    exact_refs = terminal._unique_refs([
        *authorities,
        *[predicate.ref.as_dict() for predicate in catalog.predicates],
        *[query.ref.as_dict() for query in catalog.queries],
        *[authority.ref.as_dict() for authority in catalog.discovery_authorities],
        *[ref.as_dict() for ref in executor.release_refs],
        result.discovery_authority_ref.as_dict(),
        result.candidate_grammar_ref.as_dict(),
        result.evaluated_frontier_ref.as_dict(),
        result.replay_ref.as_dict(),
        *[ref.as_dict() for ref in result.empirical_fact_refs],
        *[receipt.ref.as_dict() for receipt in result.receipts],
    ])
    replay_manifest = {
        "i05_replay_ref": result.replay_ref.as_dict(),
        "constituent_i03_closure_identity": i03_closure,
        "dependency_root": semantic_hash(exact_refs),
    }
    authority_identity = _neutral_lits_authority_identity()
    workload_identity = canonicalize(frontier)
    material = {
        "source_identity": {
            "source": "LITS_I",
            "sha256": LITS_SOURCE_SHA256,
            "rows": LITS_ROWS,
            "variables": LITS_VARIABLES,
        },
        "court_constitution_refs": {
            "frozen_authority_identity": canonicalize(authority_identity),
            "frozen_workload_identity": workload_identity,
        },
        "semantic_authority_closure": canonicalize(authorities),
        "projection_and_release_refs": canonicalize(projection_refs),
        "frontier_manifest": workload_identity,
        "comparison_fact_manifest": canonicalize(candidate_rows),
        "expected_learned_product": canonicalize(learned),
        "replay_manifest": canonicalize(replay_manifest),
        "exact_ref_manifest": canonicalize(exact_refs),
        "constituent_i03_fact_manifest": canonicalize(constituent_facts),
        "constituent_i03_closure_identity": i03_closure,
    }
    audit = {
        "runtime_catalog_identity": catalog.receipt()["catalog_identity"],
        "common_execution_binding": executor.binding_receipt(),
        "current_i05_execution_identity": execution_receipt["execution_identity"],
        "constituent_i03_fact_count": len(constituent_facts),
        "constituent_i03_closure_identity": i03_closure,
        "exact_ref_count": len(exact_refs),
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
    }
    return material, audit, execution_receipt


def produce_lits_local_oracle(
    *,
    source_path: Path,
    repo_root: Path,
    work_root: Path,
    output_path: Path,
    freeze_sequence: int = 30,
) -> Mapping[str, Any]:
    material, audit, execution_receipt = _neutral_lits_material(
        source_path=source_path,
        repo_root=repo_root,
        work_root=work_root,
    )
    prior_product = _git_json(Path(repo_root), LITS_ASTRA_D04_R2_COMMIT, ASTRA_PRODUCT_PATH)
    prior_replay = _git_json(Path(repo_root), LITS_ASTRA_D04_R2_COMMIT, ASTRA_REPLAY_PATH)
    provenance = {
        "builder": "FIABC_FINAL_LITS_CANDIDATE_NEUTRAL_LOCAL_ORACLE_PRODUCER_R1",
        "dependencies": [
            {"owner_class": "EXACT_SOURCE", "identity": LITS_SOURCE_SHA256},
            {
                "owner_class": "ACCEPTED_AUTHORITY",
                "identity": LITS_RUNTIME_CATALOG,
            },
            {
                "owner_class": "COMMON_SEMANTIC_PRODUCER",
                "identity": execution_receipt["execution_identity"],
            },
            {
                "owner_class": "ACCEPTED_IMMUTABLE_PRIOR_EMPIRICAL_PRODUCT",
                "identity": LITS_LEARNED_PRODUCT_IDENTITY,
            },
        ],
        "candidate_outputs_used": [],
        "pairwise_candidate_vote": False,
        "first_successful_candidate_as_golden": False,
        "candidate_a_b_c_processes_started": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
    }
    frozen = build_lits_i_oracle(
        prior_product=prior_product,
        prior_replay_receipt=prior_replay,
        source_identity=material["source_identity"],
        court_constitution_refs=material["court_constitution_refs"],
        semantic_authority_closure=material["semantic_authority_closure"],
        projection_and_release_refs=material["projection_and_release_refs"],
        frontier_manifest=material["frontier_manifest"],
        comparison_fact_manifest=material["comparison_fact_manifest"],
        expected_learned_product=material["expected_learned_product"],
        replay_manifest=material["replay_manifest"],
        exact_ref_manifest=material["exact_ref_manifest"],
        oracle_build_provenance=provenance,
        freeze=FreezeContext(freeze_sequence=freeze_sequence),
    )
    identity = verify_frozen_oracle(frozen)
    output_sha = _write_json(Path(output_path), frozen)
    return {
        "schema": PRODUCER_SCHEMA,
        "operation": "PRODUCE_LITS_LOCAL_CANDIDATE_NEUTRAL_ORACLE",
        "status": "PASS",
        "source": "LITS_I",
        "oracle_identity_sha256": identity,
        "oracle_document_sha256": output_sha,
        "output_path": str(Path(output_path)),
        "current_standardized_constituent_i03_fact_refs": [
            row["ref"] for row in material["constituent_i03_fact_manifest"]
        ],
        "current_constituent_i03_closure_identity": material[
            "constituent_i03_closure_identity"
        ],
        "current_observation_shaped_exact_ref_manifest": material["exact_ref_manifest"],
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
        "audit": audit,
    }


def _relative_oracle_path(oracle_path: Path, freeze_path: Path) -> str:
    return os.path.relpath(
        str(Path(oracle_path).resolve()), str(Path(freeze_path).resolve().parent)
    )


def _verified_standard_oracle(
    *, path: Path, source: str, work_root: Path
) -> tuple[Mapping[str, Any], str, str]:
    _reject_candidate_owned_path(path, work_root, f"{source} oracle")
    doc = _load_json(path)
    if doc.get("schema") != ORACLE_SCHEMA or doc.get("source") != source:
        raise FinalOracleProducerError(f"{source} oracle is not the standard live schema")
    identity = verify_frozen_oracle(doc)
    receipt = doc.get("freeze_receipt")
    if not isinstance(receipt, Mapping):
        raise FinalOracleProducerError(f"{source} oracle freeze receipt missing")
    _check_zero_candidate_provenance(receipt, f"{source} standard oracle")
    court = doc.get("court_constitution_refs")
    if not isinstance(court, Mapping):
        raise FinalOracleProducerError(f"{source} oracle court constitution missing")
    if not isinstance(court.get("frozen_authority_identity"), Mapping):
        raise FinalOracleProducerError(f"{source} oracle frozen authority identity missing")
    if not isinstance(court.get("frozen_workload_identity"), Mapping):
        raise FinalOracleProducerError(f"{source} oracle frozen workload identity missing")
    return doc, identity, _sha256_file(path)


def produce_t3_two_source_freeze(
    *,
    lits_oracle_path: Path,
    wvs_oracle_path: Path,
    work_root: Path,
    output_path: Path,
) -> Mapping[str, Any]:
    work_root = Path(work_root).resolve()
    output_path = Path(output_path).resolve()
    _reject_candidate_owned_path(output_path, work_root, "T3 freeze receipt")
    lits, lits_id, lits_sha = _verified_standard_oracle(
        path=Path(lits_oracle_path), source="LITS_I", work_root=work_root
    )
    wvs, wvs_id, wvs_sha = _verified_standard_oracle(
        path=Path(wvs_oracle_path), source="WVS7", work_root=work_root
    )
    if lits["source_identity"] != {
        "source": "LITS_I",
        "sha256": LITS_SOURCE_SHA256,
        "rows": LITS_ROWS,
        "variables": LITS_VARIABLES,
    }:
        raise FinalOracleProducerError("LiTS standard oracle source identity drift")
    if wvs["source_identity"] != {
        "source": "WVS7",
        "sha256": WVS7_SOURCE_SHA256,
        "rows": WVS_ROWS,
        "variables": WVS_VARIABLES,
    }:
        raise FinalOracleProducerError("WVS standard oracle source identity drift")

    authority_identities = {
        "LITS_I": canonicalize(lits["court_constitution_refs"]["frozen_authority_identity"]),
        "WVS7": canonicalize(wvs["court_constitution_refs"]["frozen_authority_identity"]),
    }
    workload_identities = {
        "LITS_I": canonicalize(lits["court_constitution_refs"]["frozen_workload_identity"]),
        "WVS7": canonicalize(wvs["court_constitution_refs"]["frozen_workload_identity"]),
    }
    oracle_paths = {
        "LITS_I": Path(lits_oracle_path).resolve(),
        "WVS7": Path(wvs_oracle_path).resolve(),
    }
    identities = {"LITS_I": lits_id, "WVS7": wvs_id}
    shas = {"LITS_I": lits_sha, "WVS7": wvs_sha}
    source_shas = {"LITS_I": LITS_SOURCE_SHA256, "WVS7": WVS7_SOURCE_SHA256}

    source_freezes = {
        source: {
            "source_id": source,
            "canonical_source_sha256": source_shas[source],
            "source_identity_authority_ref": f"{CURRENT_SOURCE_MANIFEST_REF}.{source}",
            "derivative_identity": None,
            "derivative_to_source_provenance_ref": None,
        }
        for source in ("LITS_I", "WVS7")
    }
    oracle_identities = {}
    for source in ("LITS_I", "WVS7"):
        rel = _relative_oracle_path(oracle_paths[source], output_path)
        oracle_identities[source] = {
            "oracle_identity_sha256": identities[source],
            "oracle_freeze_authority_ref": rel + "#freeze_receipt",
            "oracle_document_path": rel,
            "oracle_document_sha256": shas[source],
        }

    doc = {
        "schema": FREEZE_RECEIPT_SCHEMA,
        "candidate_neutral": True,
        "frozen_before_candidate_execution": True,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
        "state": "FROZEN_READ_ONLY",
        "source_freezes": source_freezes,
        "authority_identities": authority_identities,
        "workload_identities": workload_identities,
        "oracle_identities": oracle_identities,
        "freeze_order": {
            "source_identity_freeze_sequence": 10,
            "authority_workload_freeze_sequence": 20,
            "oracle_materialize_freeze_sequence": 30,
        },
    }
    output_sha = _write_json(output_path, doc)
    loaded, loaded_sha = load_frozen_upstream_receipt(output_path)
    if loaded_sha != output_sha or canonicalize(loaded) != canonicalize(doc):
        raise FinalOracleProducerError("T3 self-validation identity mismatch")

    # Exercise the live T5 path resolver and standard oracle verifier, not only
    # the generic envelope validator.
    from rawlsing_next.fiabc_live_terminal_control import load_frozen_source_oracle

    for source in ("LITS_I", "WVS7"):
        live_oracle, _freeze, live_freeze_sha = load_frozen_source_oracle(
            freeze_path=output_path, source=source, work_root=work_root
        )
        if live_oracle.get("oracle_identity_sha256") != identities[source]:
            raise FinalOracleProducerError(f"{source} live T5 oracle binding mismatch")
        if live_freeze_sha != output_sha:
            raise FinalOracleProducerError(f"{source} live T5 freeze identity mismatch")

    return {
        "schema": PRODUCER_SCHEMA,
        "operation": "PRODUCE_FINAL_TWO_SOURCE_T3_FREEZE",
        "status": "PASS",
        "freeze_schema": FREEZE_RECEIPT_SCHEMA,
        "freeze_document_sha256": output_sha,
        "output_path": str(output_path),
        "oracle_identities": identities,
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m rawlsing_next.fiabc_final_oracle_freeze_producers"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    wvs = sub.add_parser(
        "standardize-wvs",
        help="Source-free accepted R1M WVS successor oracle -> standard live oracle",
    )
    wvs.add_argument("--r1m", required=True, type=Path)
    wvs.add_argument("--output", required=True, type=Path)
    wvs.add_argument("--freeze-sequence", type=int, default=30)

    lits = sub.add_parser(
        "produce-lits",
        help="Candidate-neutral local LiTS common-path oracle producer",
    )
    lits.add_argument("--repo-root", required=True, type=Path)
    lits.add_argument("--source", required=True, type=Path)
    lits.add_argument("--work-root", required=True, type=Path)
    lits.add_argument("--output", required=True, type=Path)
    lits.add_argument("--freeze-sequence", type=int, default=30)

    t3 = sub.add_parser(
        "freeze-t3",
        help="Verify two standard source oracles and emit final T3 upstream freeze",
    )
    t3.add_argument("--lits-oracle", required=True, type=Path)
    t3.add_argument("--wvs-oracle", required=True, type=Path)
    t3.add_argument("--work-root", required=True, type=Path)
    t3.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "standardize-wvs":
        receipt = standardize_wvs_r1m_oracle(
            r1m_path=args.r1m,
            output_path=args.output,
            freeze_sequence=args.freeze_sequence,
        )
    elif args.command == "produce-lits":
        receipt = produce_lits_local_oracle(
            source_path=args.source,
            repo_root=args.repo_root,
            work_root=args.work_root,
            output_path=args.output,
            freeze_sequence=args.freeze_sequence,
        )
    elif args.command == "freeze-t3":
        receipt = produce_t3_two_source_freeze(
            lits_oracle_path=args.lits_oracle,
            wvs_oracle_path=args.wvs_oracle,
            work_root=args.work_root,
            output_path=args.output,
        )
    else:  # pragma: no cover
        raise FinalOracleProducerError("unknown command")
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "FinalOracleProducerError",
    "PRODUCER_SCHEMA",
    "R1M_ORACLE_IDENTITY",
    "R1M_TRUTH_IDENTITY",
    "SUCCESSOR_DISCOVERY_AUTHORITY",
    "SUCCESSOR_LOCK2",
    "SUCCESSOR_LOCK2_REPLAY",
    "produce_lits_local_oracle",
    "produce_t3_two_source_freeze",
    "standardize_wvs_r1m_oracle",
]
