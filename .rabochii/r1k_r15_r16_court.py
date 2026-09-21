from __future__ import annotations

import base64
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace
import time

from rawlsing_next.fiabc_lm2_r1e_common_c11 import build_common_c11_release
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
    learned_empirical_execution_receipt,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.pre553_independent_parity_oracle import (
    FreezeContext,
    NEGATIVE_STATE_LAW,
    WVS7_DISCOVERY_AUTHORITY,
    WVS7_EMPIRICAL_UNIVERSE,
    WVS7_FAMILY_COUNTS,
    WVS7_LOCK2_IDENTITY,
    WVS7_LOCK2_REPLAY_IDENTITY,
    WVS7_MEASURE_BASIS,
    WVS7_ORDERED_CANDIDATE_HASHES,
    WVS7_RISK_SET,
    WVS7_SOURCE_SHA256,
    WVS_MATERIALIZER_CONTRACT,
    freeze_wvs7_oracle_from_common_material,
    verify_frozen_oracle,
)
import rawlsing_next.fiabc_live_terminal_control as t5

ROOT = Path(__file__).resolve().parents[1]
CARRIER = ROOT / "WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/LOCAL_OUTPUT/FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json"
PKG = ROOT / "WORKER_RETURNS/EE-P2R6S/SUPPORT/02_WVS7_P2F2_RUNTIME_PACKAGE.json"
R1J_DELTA = ROOT / "WORKER_RETURNS/FIABC-LM2-R1J-SAV-REPRESENTATION-AUTHORITY/05_R6S_IDENTITY_DELTA.json"
R1J_AUTH = ROOT / "WORKER_RETURNS/FIABC-LM2-R1J-SAV-REPRESENTATION-AUTHORITY/04_AUTHORITY_OBJECT_AND_SCOPE.json"
R1J_PARITY = ROOT / "WORKER_RETURNS/FIABC-LM2-R1J-SAV-REPRESENTATION-AUTHORITY/06_VERSION_PARITY_HOLDING.md"
R1J_HOSTILE = ROOT / "WORKER_RETURNS/FIABC-LM2-R1J-SAV-REPRESENTATION-AUTHORITY/07_HOSTILE_REGRESSION_RECEIPT.json"
R1H_CONSERVATION = ROOT / "WORKER_RETURNS/FIABC-LM2-R1H-C11-ORACLE/05_FROZEN_OBJECT_CONSERVATION.json"
R1E_SOURCE_FREE = ROOT / "WORKER_RETURNS/FIABC-LM2-R1E/11_SOURCE_FREE_COURT_RECEIPT.json"
PHYSICAL_EXPECTATION = ROOT / "WORKER_RETURNS/FIABC-LM2/04_WVS7_CANONICAL_PHYSICAL_EXPECTATION.json"

EXPECTED = {
    "source_sha256": "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d",
    "carrier_sha256": "1aea888d8d576fc8606d56dd7a3b1a552411b8f8126ea27a54c36ff6d551dd7e",
    "carrier_bytes": 83340882,
    "rows": 97220,
    "physical_cells": 194440,
    "structural_preimage": "151907b3163959d0eb5ebb020fa5253d33447362420e465600035744112fe5bc",
    "parentage_bundle": "5037c55bf1a017112c0fe5f18ca5905696d66dfefcc4d8f47dcb0e7fcb13f37c",
    "physical_expectation": "9845c24da0c03adb4dfd65118b7c8c39a60a30337f33cc4177ffc6c848d02390",
    "mapping_authority": "76e63b2af0bf0b9a53319a74d2ded099c9ac175de99935d0741ac52f68086670",
    "representation_authority": "63543411892d8d30fb5670a39714a3dc115145e3f054a7017a325dab1c6cf053",
    "representation_snapshot": "e23ec7451d150597799bbd9049cdab45339e647694a9ccfacb2e53aaf09b609b",
    "response_binding": "f225e6289b553ab221902c95c1b416bbd01fb722efcc77c909e239d4ee02e87b",
    "projection_authority": "5e793e2fe255d0a0ef6dd405f4bd4c7df125c2d6fb23bd464a0f77d65cb1fcdf",
    "projection_snapshot": "540914a3ddf3b0349720fd81de49b1a88f194929adf1ea5506718af94e65c0d2",
    "projection_identity": "f400c804fea9b526f25eac823138ecb30e10efaad3207c4578661f684adee665",
    "lock2": "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188",
    "candidate_grammar": "a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6",
}

def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def ref_key(ref):
    return (ref["kind"], ref["object_id"], ref["content_hash"])

def unique_refs(refs):
    by = {ref_key(ref): canonicalize(ref) for ref in refs}
    return [by[k] for k in sorted(by)]

def emit(name: str, text: str):
    encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
    width = 20000
    pieces = [encoded[i:i+width] for i in range(0, len(encoded), width)] or [""]
    for idx, piece in enumerate(pieces, 1):
        print(f"R1K_ARTIFACT::{name}::{idx}/{len(pieces)}::{piece}")

def emit_json(name: str, value):
    emit(name, json.dumps(value, sort_keys=True, indent=2) + "\n")

def authority_hash(ref):
    return ref["authority_content_hash"]

started = time.perf_counter()
telemetry = {
    "schema": "FIABC_LM2_R1K_COMMAND_TELEMETRY@1.0.0",
    "github_actions_run_id": os.environ.get("GITHUB_RUN_ID"),
    "github_actions_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
    "github_sha": os.environ.get("GITHUB_SHA"),
    "github_ref": os.environ.get("GITHUB_REF"),
    "browser_github_only": True,
    "wvs_sav_opened": False,
    "wvs_zip_opened": False,
    "candidate_a_b_c_processes_started": 0,
    "measured_p2x_executed": False,
    "stages": [],
}

# Gate 1: exact conservation.
g1_start = time.perf_counter()
delta = load(R1J_DELTA)
r1h = load(R1H_CONSERVATION)
auth = load(R1J_AUTH)
hostile = load(R1J_HOSTILE)
physical = load(PHYSICAL_EXPECTATION)
source_free = load(R1E_SOURCE_FREE)
pkg = load(PKG)

assert CARRIER.is_file()
assert CARRIER.stat().st_size == EXPECTED["carrier_bytes"]
assert sha256(CARRIER) == EXPECTED["carrier_sha256"]
assert r1h["source_sha256"] == EXPECTED["source_sha256"]
assert r1h["structural_preimage"] == EXPECTED["structural_preimage"]
assert r1h["parentage_bundle"] == EXPECTED["parentage_bundle"]
assert r1h["physical_expectation"] == EXPECTED["physical_expectation"]
assert r1h["mapping_authority"] == EXPECTED["mapping_authority"]
assert r1h["candidate_grammar"] == EXPECTED["candidate_grammar"]
assert r1h["candidate_count"] == 46
assert r1h["lock2"] == EXPECTED["lock2"]
assert physical["expectation_identity"] == EXPECTED["physical_expectation"]
assert pkg["source_sha256"] == EXPECTED["source_sha256"]
assert pkg["lock2"] == EXPECTED["lock2"]
assert pkg["counts"]["candidates"] == 46
assert auth["authority_ref"]["authority_content_hash"] == EXPECTED["representation_authority"]
assert auth["snapshot_ref"]["content_hash"] == EXPECTED["representation_snapshot"]
assert delta["reissued"]["response_binding"]["new"] == EXPECTED["response_binding"]
assert delta["reissued"]["projection_authority"]["new"] == EXPECTED["projection_authority"]
assert delta["reissued"]["projection_snapshot"]["new"] == EXPECTED["projection_snapshot"]
assert delta["reissued"]["projection_identity"]["new"] == EXPECTED["projection_identity"]
assert hostile["status"] == "PASS"
assert hostile["forbidden_execution"]["candidate_abc"] is False
assert source_free["status"] == "PASS"

gate1 = {
    "schema": "FIABC_LM2_R1K_R1J_CONSERVATION_RECEIPT@1.0.0",
    "status": "PASS",
    "source_sha256": EXPECTED["source_sha256"],
    "carrier": {
        "path": str(CARRIER.relative_to(ROOT)),
        "sha256": EXPECTED["carrier_sha256"],
        "bytes": EXPECTED["carrier_bytes"],
        "rows": EXPECTED["rows"],
        "physical_cells": EXPECTED["physical_cells"],
    },
    "structural_preimage_identity": EXPECTED["structural_preimage"],
    "parentage_bundle_identity": EXPECTED["parentage_bundle"],
    "physical_expectation_identity": EXPECTED["physical_expectation"],
    "r1e_mapping_authority": EXPECTED["mapping_authority"],
    "representation_authority": EXPECTED["representation_authority"],
    "representation_snapshot": EXPECTED["representation_snapshot"],
    "r6s_response_binding": EXPECTED["response_binding"],
    "projection_authority": EXPECTED["projection_authority"],
    "projection_snapshot": EXPECTED["projection_snapshot"],
    "projection_identity": EXPECTED["projection_identity"],
    "candidate_grammar": EXPECTED["candidate_grammar"],
    "candidate_count": 46,
    "lock2": EXPECTED["lock2"],
    "candidate_outputs_consulted": 0,
    "candidate_processes_started": 0,
    "r1j_version_parity_holding_present": R1J_PARITY.is_file(),
    "r1j_hostile_regression_pass": hostile["status"] == "PASS",
}
telemetry["stages"].append({"stage": "GATE_1_R1J_CONSERVATION", "seconds": time.perf_counter() - g1_start, "status": "PASS"})

# Gate 2/R15: real persisted carrier -> strict common C11 using current R1J R6S.
r15_start = time.perf_counter()
release, projection = build_common_c11_release(CARRIER)
assert projection.projection_identity_ref.content_hash == EXPECTED["projection_identity"]
assert projection.projection_authority_ref.authority_content_hash == EXPECTED["projection_authority"]
assert len(projection.response_slots) == 2
assert tuple(slot.slot.name for slot in projection.response_slots) == ("Q291G5", "Q291P5")
for slot in projection.response_slots:
    assert len(slot.values) == 10
    substantive = [x for x in slot.values if x.canonical_value is not None]
    special = [x for x in slot.values if x.canonical_value is None]
    assert sorted(x.canonical_value for x in substantive) == ["1", "2", "3", "4", "5"]
    assert len(special) == 5  # four source-special rules + system missing.
    for rule in slot.values:
        if rule.canonical_value is not None:
            assert rule.transform_authority_ref.authority_content_hash == EXPECTED["mapping_authority"]

serialized_public = json.dumps([x.ref.as_dict() for x in release.public_objects], sort_keys=True)
assert "CANDIDATE_A" not in serialized_public
assert "CANDIDATE_B" not in serialized_public
assert "CANDIDATE_C" not in serialized_public

r15 = {
    "schema": "FIABC_LM2_R1K_R15_COMMON_C11_RECEIPT@1.0.0",
    "status": "PASS__STRICT_REAL_COMMON_C11_ADMITTED",
    "source_sha256": EXPECTED["source_sha256"],
    "carrier_sha256": EXPECTED["carrier_sha256"],
    "structural_preimage_identity": EXPECTED["structural_preimage"],
    "representation_authority": EXPECTED["representation_authority"],
    "r6s_response_binding": EXPECTED["response_binding"],
    "projection_identity_ref": projection.projection_identity_ref.as_dict(),
    "projection_authority_ref": projection.projection_authority_ref.as_dict(),
    "release_ref": release.release_ref.as_dict(),
    "source_release_manifest_hash": release.source_release_manifest_hash,
    "semantic_release_hash": release.semantic_release_hash,
    "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
    "public_object_count": len(release.public_objects),
    "internal_record_count": len(release.internal_records),
    "response_slots": [
        {
            "name": slot.slot.name,
            "ordinal": slot.slot.ordinal,
            "governed_rule_count": len(slot.values),
            "complete_real_row_coverage_required_by_strict_c11": True,
        }
        for slot in projection.response_slots
    ],
    "strict_exact_physical_binding": True,
    "generic_int_float_coercion": False,
    "raw_value_semantic_inference": False,
    "candidate_neutral": True,
    "candidate_outputs_consulted": 0,
    "candidate_processes_started": 0,
}
telemetry["stages"].append({"stage": "R15_STRICT_COMMON_C11", "seconds": time.perf_counter() - r15_start, "status": "PASS"})

# Build the exact candidate-neutral runtime above the admitted common release.
oracle_start = time.perf_counter()
catalog = RuntimeObjectCatalog.from_documents(
    authority_documents=pkg["authority_documents"],
    predicate_documents=pkg["predicate_documents"],
    query_documents=pkg["query_documents"],
    discovery_authority_documents=pkg["discovery_authority_documents"],
)
repository = C11Repository((release,))
executor = CarrierNeutralResearchExecutor(
    repository=repository,
    release_refs=(release.release_ref,),
    runtime_catalog=catalog,
)
neutral_binding = SimpleNamespace(executor=executor)
assert len(catalog.discovery_authority_refs) == 1

def current_authority_freeze():
    return canonicalize({
        "schema": "FIABC_LM2_R1K_WVS7_AUTHORITY_FREEZE@1.0.0",
        "source_sha256": EXPECTED["source_sha256"],
        "p2f2_authority_refs": [a.ref.as_dict() for a in catalog.authorities],
        "r1e_native_to_program_mapping_authority": EXPECTED["mapping_authority"],
        "r1j_physical_native_representation_authority": EXPECTED["representation_authority"],
        "r1j_representation_snapshot": EXPECTED["representation_snapshot"],
        "r6s_response_binding": EXPECTED["response_binding"],
        "r6s_projection_authority": EXPECTED["projection_authority"],
        "r6s_projection_snapshot": EXPECTED["projection_snapshot"],
        "r6s_projection_identity": EXPECTED["projection_identity"],
        "physical_expectation_identity": EXPECTED["physical_expectation"],
        "source_special_states": {
            "-5": "MISSING",
            "-4": "NOT_ASKED",
            "-2": "SOURCE_SPECIFIC_SPECIAL",
            "-1": "DK",
        },
        "source_special_states_canonical_values": None,
        "system_missing": "SEPARATE_NOT_SOURCE_NATIVE",
        "canonical_question_mapping": "ABSENT_NOT_AUTHORIZED",
        "cross_source_relation": "NONE_AUTHORIZED",
    })

def current_workload_freeze():
    return canonicalize({
        "schema": "FIABC_LM2_R1K_WVS7_WORKLOAD_FREEZE@1.0.0",
        "lock2": WVS7_LOCK2_IDENTITY,
        "lock2_replay": WVS7_LOCK2_REPLAY_IDENTITY,
        "discovery_authority": WVS7_DISCOVERY_AUTHORITY,
        "empirical_universe": WVS7_EMPIRICAL_UNIVERSE,
        "risk_set": WVS7_RISK_SET,
        "measure_basis": WVS7_MEASURE_BASIS,
        "predicate_refs": [p.ref.as_dict() for p in catalog.predicates],
        "query_refs": [q.ref.as_dict() for q in catalog.queries],
        "discovery_authority_refs": [d.ref.as_dict() for d in catalog.discovery_authorities],
        "ordered_candidate_hashes": list(WVS7_ORDERED_CANDIDATE_HASHES),
        "family_counts": dict(WVS7_FAMILY_COUNTS),
        "candidate_count": 46,
        "complete_frontier_no_pruning": True,
    })

authority_freeze = current_authority_freeze()
workload_freeze = current_workload_freeze()

def oracle_material_from_result(result, execution_receipt):
    candidate_rows, constituent_facts, i03_closure = t5._constituent_i03(neutral_binding, result)
    ordered = sorted(result.receipts, key=lambda x: x.candidate_identity["candidate_hash"])
    hashes = [x.candidate_identity["candidate_hash"] for x in ordered]
    families = dict(sorted(Counter(x.candidate_identity["family"] for x in ordered).items()))
    assert tuple(hashes) == tuple(WVS7_ORDERED_CANDIDATE_HASHES)
    assert families == dict(sorted(WVS7_FAMILY_COUNTS.items()))
    assert result.candidate_count == 46
    assert result.covered_candidate_count == 46
    assert result.coverage_claim == "COMPLETE_FOR_EXACT_DECLARED_FRONTIER"
    query_role_count = sum(len(x.candidate_identity["query_roles"]) for x in ordered)
    terminal_counts = dict(sorted(Counter(x.typed_state for x in ordered).items()))
    authorities = [a.ref.as_dict() for a in catalog.authorities]
    exact_refs = unique_refs([
        *authorities,
        *[p.ref.as_dict() for p in catalog.predicates],
        *[q.ref.as_dict() for q in catalog.queries],
        *[d.ref.as_dict() for d in catalog.discovery_authorities],
        release.release_ref.as_dict(),
        result.discovery_authority_ref.as_dict(),
        result.candidate_grammar_ref.as_dict(),
        result.evaluated_frontier_ref.as_dict(),
        result.replay_ref.as_dict(),
        *[x.as_dict() for x in result.empirical_fact_refs],
        *[x.ref.as_dict() for x in result.receipts],
    ])
    projection_refs = {
        "projection_identity": projection.projection_identity_ref.content_hash,
        "release_refs": [release.release_ref.as_dict()],
        "release_replay_refs": [release.replay_manifest.ref.as_dict()],
    }
    frontier = {
        "candidate_count": 46,
        "ordered_candidate_hashes": hashes,
        "family_counts": families,
    }
    learned = {
        "product_identity": semantic_hash(execution_receipt),
        "semantic_identity": result.replay_ref.content_hash,
        "replay_identity": execution_receipt["execution_identity"],
        "exact_output_identity": execution_receipt["execution_identity"],
        "coverage": {
            "candidate_count": 46,
            "query_role_count": query_role_count,
            "typed_terminal_counts": terminal_counts,
        },
    }
    replay_manifest = {
        "i05_replay_ref": result.replay_ref.as_dict(),
        "constituent_i03_closure_identity": i03_closure,
        "dependency_root": semantic_hash(exact_refs),
    }
    material = {
        "contract": WVS_MATERIALIZER_CONTRACT,
        "source_identity": {
            "source": "WVS7",
            "sha256": EXPECTED["source_sha256"],
            "rows": EXPECTED["rows"],
            "variables": 613,
        },
        "court_constitution_refs": {
            "frozen_authority_identity": authority_freeze,
            "frozen_workload_identity": workload_freeze,
            "lock2_hash": WVS7_LOCK2_IDENTITY,
            "lock2_replay_hash": WVS7_LOCK2_REPLAY_IDENTITY,
            "discovery_authority": WVS7_DISCOVERY_AUTHORITY,
            "empirical_universe": WVS7_EMPIRICAL_UNIVERSE,
            "risk_set": WVS7_RISK_SET,
            "measure_basis": WVS7_MEASURE_BASIS,
        },
        "semantic_authority_closure": canonicalize(authorities),
        "projection_and_release_refs": canonicalize(projection_refs),
        "frontier_manifest": canonicalize(frontier),
        "expected_fact_manifest": canonicalize(candidate_rows),
        "expected_learned_product": canonicalize(learned),
        "replay_manifest": canonicalize(replay_manifest),
        "exact_ref_manifest": canonicalize(exact_refs),
        "oracle_build_provenance": {
            "builder": "FIABC_LM2_R1K_CANDIDATE_NEUTRAL_COMMON_C11_I03_I05",
            "dependencies": [
                {"owner_class": "EXACT_SOURCE", "identity": EXPECTED["source_sha256"]},
                {"owner_class": "ACCEPTED_AUTHORITY", "identity": semantic_hash(authority_freeze)},
                {"owner_class": "COURT_NEUTRAL", "identity": semantic_hash(workload_freeze)},
                {"owner_class": "COMMON_SEMANTIC_PRODUCER", "identity": release.release_ref.content_hash},
            ],
            "candidate_outputs_used": [],
            "pairwise_candidate_vote": False,
            "first_successful_candidate_as_golden": False,
            "candidate_a_b_c_processes_started": 0,
            "raw_source_reread": False,
        },
    }
    return material, constituent_facts, i03_closure

# R16 primary materialization.
result1 = executor.execute_i05(discovery_authority_ref=catalog.discovery_authority_refs[0])
receipt1 = learned_empirical_execution_receipt(result1)
material1, constituent1, closure1 = oracle_material_from_result(result1, receipt1)
freeze_ctx = FreezeContext(
    freeze_sequence=3,
    candidate_outputs_seen=0,
    candidate_owned_roots_consulted=(),
    candidate_owned_state_reused=False,
    candidate_output_first_sequence=None,
)
oracle1 = freeze_wvs7_oracle_from_common_material(material=material1, freeze=freeze_ctx)
identity1 = verify_frozen_oracle(oracle1)

# Independent deterministic replay from the same admitted common C11 and frozen workload.
replay_start = time.perf_counter()
result2 = executor.execute_i05(discovery_authority_ref=catalog.discovery_authority_refs[0])
receipt2 = learned_empirical_execution_receipt(result2)
material2, constituent2, closure2 = oracle_material_from_result(result2, receipt2)
oracle2 = freeze_wvs7_oracle_from_common_material(material=material2, freeze=freeze_ctx)
identity2 = verify_frozen_oracle(oracle2)
assert canonicalize(material1) == canonicalize(material2)
assert canonicalize(receipt1) == canonicalize(receipt2)
assert canonicalize(constituent1) == canonicalize(constituent2)
assert closure1 == closure2
assert identity1 == identity2
assert canonicalize(oracle1) == canonicalize(oracle2)

assert oracle1["frontier_manifest"]["candidate_count"] == 46
assert tuple(oracle1["frontier_manifest"]["ordered_candidate_hashes"]) == tuple(WVS7_ORDERED_CANDIDATE_HASHES)
assert oracle1["freeze_receipt"]["candidate_outputs_seen"] == 0
assert oracle1["freeze_receipt"]["candidate_owned_roots_consulted"] == []
assert oracle1["freeze_receipt"]["candidate_owned_state_reused"] is False

telemetry["stages"].append({"stage": "R16_PRIMARY_ORACLE_MATERIALIZE_FREEZE", "seconds": time.perf_counter() - oracle_start, "status": "PASS"})
telemetry["stages"].append({"stage": "R16_DETERMINISTIC_REPLAY", "seconds": time.perf_counter() - replay_start, "status": "PASS"})

independence = {
    "schema": "FIABC_LM2_R1K_ORACLE_INDEPENDENCE_PROOF@1.0.0",
    "status": "PASS",
    "oracle_identity_sha256": identity1,
    "source_identity_freeze_sequence": 1,
    "authority_workload_freeze_sequence": 2,
    "oracle_materialize_freeze_sequence": 3,
    "candidate_process_start_sequence": None,
    "oracle_constructed_before_candidate_start": True,
    "candidate_outputs_consulted": 0,
    "candidate_processes_started": 0,
    "candidate_owned_roots_consulted": [],
    "candidate_owned_state_reused": False,
    "pairwise_candidate_vote_used": False,
    "first_successful_candidate_used_as_golden": False,
    "frontier_candidate_count": 46,
    "frontier_exact_order_match": True,
    "family_counts": dict(WVS7_FAMILY_COUNTS),
    "pruning_performed": False,
    "deterministic_second_i05_material_equal": True,
    "deterministic_second_constituent_i03_equal": True,
    "deterministic_second_oracle_byte_semantics_equal": True,
    "truth_payload_identity": semantic_hash(material1),
    "constituent_i03_closure_identity": closure1,
    "expected_learned_product_identity": oracle1["expected_learned_product"]["product_identity"],
    "expected_replay_identity": oracle1["expected_learned_product"]["replay_identity"],
    "typed_negative_state_law": canonicalize(NEGATIVE_STATE_LAW),
    "wvs_special_states_bound_in_authority_freeze": authority_freeze["source_special_states"],
}

frontier_conservation = {
    "schema": "FIABC_LM2_R1K_LOCK2_FRONTIER_CONSERVATION@1.0.0",
    "status": "PASS",
    "lock2": WVS7_LOCK2_IDENTITY,
    "lock2_replay": WVS7_LOCK2_REPLAY_IDENTITY,
    "candidate_grammar": result1.candidate_grammar_ref.content_hash,
    "evaluated_frontier_ref": result1.evaluated_frontier_ref.as_dict(),
    "discovery_authority": result1.discovery_authority_ref.as_dict(),
    "candidate_count": result1.candidate_count,
    "covered_candidate_count": result1.covered_candidate_count,
    "coverage_claim": result1.coverage_claim,
    "ordered_candidate_hashes": list(WVS7_ORDERED_CANDIDATE_HASHES),
    "family_counts": dict(WVS7_FAMILY_COUNTS),
    "predicate_refs": [p.ref.as_dict() for p in catalog.predicates],
    "query_refs": [q.ref.as_dict() for q in catalog.queries],
    "workload_freeze_identity": semantic_hash(workload_freeze),
    "frontier_mutated": False,
    "pruning_performed": False,
    "lock2_mutated": False,
}

# Original R1C R01-R18 final ledger. R01-R14/R17-R18 were accepted source-free
# at R1E and R1J's current hostile regression proves its bounded successor did not
# weaken those laws. R15/R16 are proved by this current real-material court.
rows = []
for n in range(1, 19):
    case = f"R{n:02d}"
    if n == 15:
        disposition = "PASS__CURRENT_R1K_REAL_MATERIAL_STRICT_COMMON_C11"
        evidence = "02_R15_COMMON_C11_RECEIPT.json"
    elif n == 16:
        disposition = "PASS__CURRENT_R1K_FRESH_INDEPENDENT_ORACLE"
        evidence = "04_R16_FRESH_WVS_ORACLE.json"
    else:
        disposition = "PASS__R1E_SOURCE_FREE_ACCEPTED_AND_R1J_SUCCESSOR_REGRESSION_CONSERVED"
        evidence = "R1E run 35566968890 + R1J hostile run 35578937508"
    rows.append((case, disposition, evidence))

ledger = '"case","final_disposition","evidence"\n' + "".join(
    f'"{case}","{disposition}","{evidence}"\n' for case, disposition, evidence in rows
)

telemetry["total_seconds"] = time.perf_counter() - started
telemetry["neutral_i05_executions"] = 2
telemetry["neutral_constituent_i03_replay_passes"] = 2
telemetry["candidate_a_b_c_processes_started"] = 0
telemetry["candidate_outputs_consulted"] = 0
telemetry["raw_wvs_source_reads"] = 0
telemetry["persisted_carrier_reads"] = 1
telemetry["terminal"] = "R1K_EXECUTION_COMPLETE__NO_CANDIDATE_START"

emit_json("01_R1J_CONSERVATION_RECEIPT.json", gate1)
emit_json("02_R15_COMMON_C11_RECEIPT.json", r15)
emit("03_R01_R18_FINAL_LEDGER.csv", ledger)
emit_json("04_R16_FRESH_WVS_ORACLE.json", oracle1)
emit_json("05_ORACLE_INDEPENDENCE_PROOF.json", independence)
emit_json("06_LOCK2_FRONTIER_CONSERVATION.json", frontier_conservation)
emit_json("07_COMMAND_TELEMETRY.json", telemetry)

summary = {
    "status": "PASS",
    "r15_release": release.release_ref.content_hash,
    "r15_replay": release.replay_manifest.ref.content_hash,
    "projection_identity": projection.projection_identity_ref.content_hash,
    "oracle_identity": identity1,
    "truth_payload_identity": independence["truth_payload_identity"],
    "i03_closure_identity": closure1,
    "i05_execution_identity": receipt1["execution_identity"],
    "i05_replay_identity": result1.replay_ref.content_hash,
    "candidate_count": result1.candidate_count,
    "family_counts": dict(WVS7_FAMILY_COUNTS),
    "candidate_processes_started": 0,
    "candidate_outputs_consulted": 0,
}
print("R1K_SUMMARY=" + json.dumps(summary, sort_keys=True, separators=(",", ":")))
print("FIABC_LM2_R1K_EXECUTION_PASS__R15_STRICT_COMMON_C11__R16_FRESH_INDEPENDENT_ORACLE")
