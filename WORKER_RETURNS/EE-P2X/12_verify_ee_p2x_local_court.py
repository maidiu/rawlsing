#!/usr/bin/env python3
"""Deterministic final verifier for the proposed EE-P2X local Darwin court.

PROPOSED ONLY until HQ adoption.  This verifier never opens source carriers and
never manufactures evidence.  It consumes only frozen authority files and
executor-written receipts.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
EXPECT_PATH = HERE / "09_LOCAL_COURT_FROZEN_EXPECTATIONS.json"
CONTRACT_PATH = HERE / "10_LOCAL_COURT_RECEIPT_CONTRACT.json"
COURT = HERE / "LOCAL_COURT"
FINAL = COURT / "90_FINAL_VERIFICATION_RECEIPT.json"

CANONICAL = ["LITS_I/A","LITS_I/B","LITS_I/C","WVS7/A","WVS7/B","WVS7/C"]
EXECUTABLE = CANONICAL[:-1]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
PASS = "PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE"

class CourtBlocker(Exception):
    pass

def load(path: Path):
    if not path.exists():
        raise CourtBlocker("BLOCKER__MISSING_EVIDENCE_FILE__" + path.name.upper().replace(".","_"))
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        raise CourtBlocker("BLOCKER__INVALID_JSON__" + path.name.upper().replace(".","_"))

def require(ok: bool, terminal: str):
    if not ok:
        raise CourtBlocker(terminal)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def is_hex64(value) -> bool:
    return isinstance(value, str) and HEX64.fullmatch(value) is not None

def token(value: str) -> str:
    out = re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")
    return out[:120] or "UNSPECIFIED"

def scan_forbidden_keys(obj, forbidden, where="root"):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in forbidden:
                raise CourtBlocker(f"FAILURE__FORBIDDEN_OUTPUT_SURFACE__{token(where)}__{token(key)}")
            scan_forbidden_keys(value, forbidden, where + "." + key)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            scan_forbidden_keys(value, forbidden, f"{where}[{i}]")

def exact_runtime(actual, expected, label):
    for key in ("platform","python","pyreadstat","pyarrow","darwin_ru_maxrss_unit"):
        require(actual.get(key) == expected.get(key), f"BLOCKER__RUNTIME_DRIFT__{token(label)}__{token(key)}")

def validate_metric_slot(name, slot, preserved_allowed, stopped_allowed=False):
    require(isinstance(slot, dict), f"FAILURE__METRIC_SLOT_NOT_OBJECT__{token(name)}")
    state = slot.get("state")
    value = slot.get("value")
    unit = slot.get("unit")
    reason = slot.get("reason")
    allowed = {
        "MEASURED","PRESERVED_MEASURED","NOT_CAPTURED_PRESERVED_STAGE",
        "NOT_APPLICABLE_BY_FROZEN_COURT","UNAVAILABLE_ON_HOST_WITH_REASON",
        "NOT_REACHED_AUTHORIZED_STOP"
    }
    require(state in allowed, f"BLOCKER__METRIC_SLOT_PENDING_OR_UNKNOWN__{token(name)}")
    require(isinstance(unit, str) and unit and unit != "UNSET", f"BLOCKER__METRIC_UNIT_MISSING__{token(name)}")
    if state in {"MEASURED","PRESERVED_MEASURED"}:
        require(isinstance(value, (int,float)) and not isinstance(value, bool), f"BLOCKER__METRIC_VALUE_MISSING__{token(name)}")
        require(value >= 0, f"FAILURE__NEGATIVE_METRIC__{token(name)}")
    else:
        require(value is None, f"FAILURE__NONMEASURED_METRIC_HAS_VALUE__{token(name)}")
        require(isinstance(reason, str) and reason.strip(), f"BLOCKER__NONMEASURED_METRIC_REASON_MISSING__{token(name)}")
    if state == "NOT_CAPTURED_PRESERVED_STAGE":
        require(preserved_allowed, f"FAILURE__PRESERVED_STAGE_EXCEPTION_OUTSIDE_PRESERVED_CELL__{token(name)}")
    if state == "UNAVAILABLE_ON_HOST_WITH_REASON":
        require(name in {"cpu_user_ns","cpu_system_ns"}, f"FAILURE__HOST_UNAVAILABLE_STATE_NOT_ALLOWED__{token(name)}")
    if state == "NOT_REACHED_AUTHORIZED_STOP":
        require(stopped_allowed, f"FAILURE__STOP_EXCEPTION_OUTSIDE_STOPPED_CELL__{token(name)}")

def validate_behavior(name, value, stopped_allowed=False):
    require(isinstance(value, dict), f"BLOCKER__BEHAVIOR_RECEIPT_MISSING__{token(name)}")
    state = value.get("state")
    evidence = value.get("evidence_identity")
    require(isinstance(state, str) and state and "PENDING" not in state, f"BLOCKER__BEHAVIOR_PENDING__{token(name)}")
    if state == "NOT_REACHED_AUTHORIZED_STOP":
        require(stopped_allowed, f"FAILURE__STOP_BEHAVIOR_EXCEPTION_OUTSIDE_STOPPED_CELL__{token(name)}")
        require(evidence is None, f"FAILURE__UNREACHED_BEHAVIOR_HAS_EVIDENCE__{token(name)}")
    else:
        require(is_hex64(evidence), f"BLOCKER__BEHAVIOR_EVIDENCE_IDENTITY_MISSING__{token(name)}")

def validate_cell(path: Path, cell_key: str, e, contract, host_ids, source_oracles, source_catalogs, wvs_projections,
                  expected_disposition="QUALIFYING_CELL_COMPLETE"):
    obj = load(path)
    forbidden = set(e["forbidden_output_keys"])
    scan_forbidden_keys(obj, forbidden, cell_key)
    source, candidate = cell_key.split("/")
    stopped = expected_disposition == "AUTHORIZED_STOP"
    require(expected_disposition in {"QUALIFYING_CELL_COMPLETE","AUTHORIZED_STOP"},
            f"FAILURE__INTERNAL_EXPECTED_DISPOSITION__{token(cell_key)}")
    require(obj.get("schema") == "RAWLSING_EE_P2X_SOURCE_CANDIDATE_RECEIPT@1.0.0",
            f"FAILURE__CELL_SCHEMA__{token(cell_key)}")
    require(obj.get("source") == source and obj.get("candidate") == candidate,
            f"FAILURE__CELL_IDENTITY__{token(cell_key)}")
    require(obj.get("sequence_index") == EXECUTABLE.index(cell_key),
            f"FAILURE__CELL_SEQUENCE_INDEX__{token(cell_key)}")
    auth = obj.get("authority", {})
    require(auth.get("hq_handoff_commit") == e["hq"]["handoff_commit"], f"FAILURE__HQ_AUTHORITY_DRIFT__{token(cell_key)}")
    require(auth.get("lock1_manifest_blob") == e["lock1"]["manifest_json_git_blob_sha1"], f"FAILURE__LOCK1_DRIFT__{token(cell_key)}")
    require(auth.get("lock2_hash") == e["lock2"]["hash"], f"FAILURE__LOCK2_DRIFT__{token(cell_key)}")
    exact_runtime(obj.get("runtime", {}), e["runtime"], cell_key)

    host = obj.get("host", {})
    require(is_hex64(host.get("identity_sha256")), f"BLOCKER__HOST_IDENTITY_MISSING__{token(cell_key)}")
    require(isinstance(host.get("same_physical_host_token"), str) and host.get("same_physical_host_token"),
            f"BLOCKER__HOST_TOKEN_MISSING__{token(cell_key)}")
    host_ids.add((host["identity_sha256"], host["same_physical_host_token"]))

    bindings = obj.get("bindings", {})
    require(bindings.get("source_sha256") == e["sources"][source]["sha256"], f"FAILURE__SOURCE_IDENTITY_DRIFT__{token(cell_key)}")
    require(bindings.get("candidate_owner_blob") == e["candidates"][candidate]["owner_blob"], f"FAILURE__CANDIDATE_OWNER_DRIFT__{token(cell_key)}")
    require(bindings.get("execution_seam_blob") == e["execution_seam"]["git_blob_sha1"], f"FAILURE__EXECUTION_SEAM_DRIFT__{token(cell_key)}")
    require(is_hex64(bindings.get("runtime_catalog_identity")), f"BLOCKER__RUNTIME_CATALOG_IDENTITY_MISSING__{token(cell_key)}")
    require(is_hex64(bindings.get("candidate_provider_identity")), f"BLOCKER__CANDIDATE_PROVIDER_IDENTITY_MISSING__{token(cell_key)}")
    source_catalogs.setdefault(source, set()).add(bindings["runtime_catalog_identity"])
    projection = bindings.get("projection_identity")
    require(is_hex64(projection), f"BLOCKER__PROJECTION_IDENTITY_MISSING__{token(cell_key)}")
    if source == "LITS_I":
        require(projection == e["sources"]["LITS_I"]["projection_cache_identity"], f"FAILURE__LITS_PROJECTION_DRIFT__{token(cell_key)}")
    else:
        wvs_projections.add(projection)

    oracle = obj.get("oracle", {})
    require(oracle.get("candidate_neutral") is True and oracle.get("candidate_defined") is False,
            f"FAILURE__CANDIDATE_DEFINED_ORACLE__{token(cell_key)}")
    require(is_hex64(oracle.get("oracle_identity_sha256")), f"BLOCKER__ORACLE_IDENTITY_MISSING__{token(cell_key)}")
    source_oracles.setdefault(source, set()).add(oracle["oracle_identity_sha256"])

    ev = obj.get("event_ordinals", {})
    of,co,pc,pa = (ev.get("oracle_frozen"),ev.get("candidate_output_first"),
                   ev.get("parity_complete"),ev.get("performance_first_admitted"))
    require(isinstance(of, int) and not isinstance(of, bool) and of >= 0,
            f"BLOCKER__ORACLE_FREEZE_ORDINAL_MISSING__{token(cell_key)}")
    if co is not None:
        require(isinstance(co, int) and not isinstance(co, bool) and co >= 0 and of < co,
                f"FAILURE__ORACLE_NOT_FROZEN_BEFORE_CANDIDATE_OUTPUT__{token(cell_key)}")

    parity = obj.get("parity", {})
    dims = contract["source_candidate_receipt"]["parity_required"]
    allowed_parity={"PASS","FAIL","NOT_RUN_AUTHORIZED_STOP"}
    require(all(parity.get(k) in allowed_parity for k in dims),
            f"BLOCKER__PARITY_PENDING_OR_UNKNOWN__{token(cell_key)}")
    if not stopped:
        require(co is not None and isinstance(pc, int) and isinstance(pa, int),
                f"BLOCKER__QUALIFYING_EVENT_ORDINALS_INCOMPLETE__{token(cell_key)}")
        require(all(parity.get(k) == "PASS" for k in dims), f"FAILURE__PARITY_NOT_PASS__{token(cell_key)}")
        require(pc < pa, f"FAILURE__PERFORMANCE_BEFORE_PARITY__{token(cell_key)}")
        require(obj.get("performance_admission") == "ADMITTED_AFTER_PARITY",
                f"BLOCKER__QUALIFYING_CELL_PERFORMANCE_NOT_ADMITTED__{token(cell_key)}")
    else:
        require(pa is None, f"FAILURE__STOPPED_CELL_HAS_PERFORMANCE_ADMISSION_ORDINAL__{token(cell_key)}")
        require(obj.get("performance_admission") == "NOT_ADMITTED",
                f"FAILURE__STOPPED_CELL_PERFORMANCE_ADMITTED__{token(cell_key)}")
        if pc is not None:
            require(isinstance(pc, int) and not isinstance(pc, bool) and pc >= 0,
                    f"FAILURE__STOPPED_CELL_PARITY_ORDINAL_INVALID__{token(cell_key)}")

    expected_preserved = []
    if cell_key == "LITS_I/A": expected_preserved = ["LITS_I_A_FIRST_BUILD"]
    elif cell_key == "LITS_I/B": expected_preserved = ["LITS_I_B_CACHELESS_C11"]
    require(obj.get("preserved_stage_consumption") == expected_preserved,
            f"FAILURE__PRESERVED_STAGE_CONSUMPTION_DRIFT__{token(cell_key)}")
    preserved_allowed = bool(expected_preserved)

    metrics = obj.get("metrics", {})
    required_metrics = contract["source_candidate_receipt"]["metric_names"]
    require(set(metrics) == set(required_metrics), f"BLOCKER__METRIC_VECTOR_SHAPE__{token(cell_key)}")
    for name in required_metrics:
        validate_metric_slot(name, metrics[name], preserved_allowed, stopped)

    behaviors = obj.get("behaviors", {})
    for name in contract["source_candidate_receipt"]["behavior_required"]:
        validate_behavior(name, behaviors.get(name), stopped)

    outputs = obj.get("outputs", {})
    for name in contract["source_candidate_receipt"]["output_required"]:
        value=outputs.get(name)
        if stopped:
            require(value is None or (isinstance(value,str) and value),
                    f"FAILURE__STOPPED_OUTPUT_IDENTITY_SHAPE__{token(cell_key)}__{token(name)}")
        else:
            require(isinstance(value, str) and value,
                    f"BLOCKER__OUTPUT_IDENTITY_MISSING__{token(cell_key)}__{token(name)}")
    require(obj.get("disposition") == expected_disposition, f"FAILURE__CELL_DISPOSITION__{token(cell_key)}")
    require(obj.get("ranking_or_selection") is False, f"FAILURE__RANKING_OR_SELECTION_EMITTED__{token(cell_key)}")
    return obj

def validate_lits_learned(path: Path, cell, e):
    x = load(path)
    scan_forbidden_keys(x, set(e["forbidden_output_keys"]), "lits_learned")
    source, candidate = cell.split("/")
    exp = e["sources"]["LITS_I"]["learned"]
    require(x.get("schema") == "RAWLSING_EE_P2X_LITS_LEARNED_PRODUCT_RECEIPT@1.0.0", f"FAILURE__LITS_LEARNED_SCHEMA__{candidate}")
    require(x.get("source") == "LITS_I" and x.get("candidate") == candidate, f"FAILURE__LITS_LEARNED_CELL__{candidate}")
    require(x.get("fresh_execution") is True and x.get("product_origin") == "CURRENT_CELL_EXECUTION",
            f"FAILURE__LITS_HISTORIC_PRODUCT_NOT_FRESH__{candidate}")
    require(x.get("historic_product_substitution") is False, f"FAILURE__LITS_HISTORIC_PRODUCT_SUBSTITUTION__{candidate}")
    require(x.get("candidate_count") == exp["candidate_count"], f"FAILURE__LITS_CANDIDATE_COUNT__{candidate}")
    require(x.get("independently_executed_roles") == exp["independently_executed_roles"], f"FAILURE__LITS_ROLE_COUNT__{candidate}")
    require(x.get("terminal_counts") == exp["terminal_counts"], f"FAILURE__LITS_TERMINAL_SHAPE__{candidate}")
    require(x.get("product_sha256") == exp["expected_fresh_product_sha256"], f"FAILURE__LITS_PRODUCT_SHA__{candidate}")
    require(x.get("semantic_replay_hash") == exp["expected_semantic_replay_hash"], f"FAILURE__LITS_SEMANTIC_REPLAY__{candidate}")
    require(is_hex64(x.get("execution_receipt_identity")), f"BLOCKER__LITS_EXECUTION_RECEIPT_IDENTITY__{candidate}")
    return x

def validate_wvs_learned(path: Path, cell, e, outputs):
    x = load(path)
    scan_forbidden_keys(x, set(e["forbidden_output_keys"]), "wvs_learned")
    _, candidate = cell.split("/")
    require(x.get("schema") == "RAWLSING_EE_P2X_WVS_LEARNED_PRODUCT_RECEIPT@1.0.0", f"FAILURE__WVS_LEARNED_SCHEMA__{candidate}")
    require(x.get("source") == "WVS7" and x.get("candidate") == candidate and candidate in {"A","B"},
            f"FAILURE__WVS_LEARNED_CELL__{candidate}")
    l2 = e["lock2"]
    require(x.get("lock2_hash") == l2["hash"], f"FAILURE__WVS_LOCK2_DRIFT__{candidate}")
    require(x.get("discovery_authority_hash") == l2["discovery_authority_hash"], f"FAILURE__WVS_DISCOVERY_AUTHORITY_DRIFT__{candidate}")
    require(x.get("candidate_hashes") == l2["candidate_hashes"], f"FAILURE__WVS_FRONTIER_MUTATED__{candidate}")
    require(x.get("family_shape") == l2["family_shape"], f"FAILURE__WVS_FAMILY_SHAPE__{candidate}")
    require(x.get("predicate_hashes") == l2["predicate_hashes"], f"FAILURE__WVS_PREDICATE_CATALOG_DRIFT__{candidate}")
    require(x.get("query_hashes") == l2["query_hashes"], f"FAILURE__WVS_QUERY_CATALOG_DRIFT__{candidate}")
    require(x.get("frozen_before_outcome_access") is True and x.get("altered_after_outcome_access") is False,
            f"FAILURE__WVS_FRONTIER_POST_OUTCOME_MUTATION__{candidate}")
    require(x.get("synthetic_fallback") is False, f"FAILURE__WVS_SYNTHETIC_FALLBACK__{candidate}")
    for key, outkey in (("product_identity","product_identity"),("semantic_identity","semantic_identity"),("replay_identity","replay_identity")):
        require(isinstance(x.get(key), str) and x.get(key) == outputs[outkey],
                f"FAILURE__WVS_LEARNED_OUTPUT_MISMATCH__{candidate}__{token(key)}")
    return x

def validate_deletion(path: Path, cell, outputs):
    x = load(path)
    source, candidate = cell.split("/")
    require(x.get("schema") == "RAWLSING_EE_P2X_DELETION_REGEN_RECEIPT@1.0.0", f"FAILURE__DELETION_SCHEMA__{token(cell)}")
    require(x.get("source") == source and x.get("candidate") == candidate, f"FAILURE__DELETION_CELL__{token(cell)}")
    require(x.get("deleted_classes") == ["P4_OPTIONAL_CACHE","P5_TRANSIENT_COMPILER_STATE"], f"FAILURE__P4_P5_DELETION_SHAPE__{token(cell)}")
    require(x.get("retained_classes") == ["P1_SOURCE","P2_GOVERNED_SEMANTIC_AND_LEARNED_PRODUCTS","P3_REPLAY_PROVENANCE_DETERMINANTS"],
            f"FAILURE__P1_P2_P3_RETENTION_SHAPE__{token(cell)}")
    require(all(x.get(k) is True for k in ("c11_reachable","i03_reachable","i05_reachable","fresh_process_regeneration","identity_equivalent")),
            f"FAILURE__DELETION_REGEN_REACHABILITY__{token(cell)}")
    before, after = x.get("before",{}), x.get("after",{})
    require(before == after, f"FAILURE__DELETION_REGEN_IDENTITY_DRIFT__{token(cell)}")
    require(before == {"product":outputs["product_identity"],"semantic":outputs["semantic_identity"],"replay":outputs["replay_identity"]},
            f"FAILURE__DELETION_REGEN_WRONG_GOVERNED_IDENTITIES__{token(cell)}")
    return x

def validate_a_persistence(path: Path, cell):
    x = load(path)
    source, candidate = cell.split("/")
    require(x.get("schema") == "RAWLSING_EE_P2X_A_PERSISTENCE_INFORMATION_RECEIPT@1.0.0", f"FAILURE__A_PERSISTENCE_SCHEMA__{source}")
    require(x.get("source") == source and x.get("candidate") == "A", f"FAILURE__A_PERSISTENCE_CELL__{source}")
    require(x.get("expensive_to_rebuild_used_as_authority_basis") is False, f"FAILURE__EXPENSIVE_TO_REBUILD_USED_AS_AUTHORITY__{source}")
    contains = x.get("contains_irrecoverable_information")
    require(isinstance(contains, bool), f"BLOCKER__A_INFORMATION_CLASSIFICATION_MISSING__{source}")
    state = x.get("information_authority")
    require(state in {"AUTHORITATIVE_INFORMATION","REGENERABLE_REPRESENTATION","MIXED__EXPLICITLY_ITEMIZED"},
            f"BLOCKER__A_INFORMATION_AUTHORITY_STATE__{source}")
    if contains is False:
        require(state == "REGENERABLE_REPRESENTATION", f"FAILURE__A_REGENERABLE_REPRESENTATION_MISCLASSIFIED_AUTHORITATIVE__{source}")
    require(isinstance(x.get("operational_persistence_value"), dict) and x["operational_persistence_value"],
            f"BLOCKER__A_OPERATIONAL_PERSISTENCE_VALUE_MISSING__{source}")
    require(isinstance(x.get("rebuild_cost"), dict) and x["rebuild_cost"],
            f"BLOCKER__A_REBUILD_COST_MISSING__{source}")
    return x

def validate_failure(path: Path, cell, e):
    x = load(path)
    scan_forbidden_keys(x, set(e["forbidden_output_keys"]), "failure")
    source, candidate = cell.split("/")
    require(x.get("schema") == "RAWLSING_EE_P2X_FAILURE_STOP_RECEIPT@1.0.0", f"FAILURE__STOP_SCHEMA__{token(cell)}")
    require(x.get("source") == source, f"FAILURE__STOP_SOURCE__{token(cell)}")
    require(x.get("candidate") in {candidate, None}, f"FAILURE__STOP_CANDIDATE__{token(cell)}")
    kinds={"CANDIDATE_LOCAL_CORRECTNESS_FAILURE","SOURCE_SPECIFIC_CANDIDATE_FAILURE","COMMON_SOURCE_AUTHORITY_FAILURE",
           "WVS7_C_CURRENT_PORTABILITY_FAILURE","INTERRUPTED_PARTIAL_EXECUTION","PARITY_ORACLE_FAILURE"}
    require(x.get("kind") in kinds, f"FAILURE__UNKNOWN_STOP_KIND__{token(cell)}")
    require(x.get("later_lawful_cells_suppressed") is False, f"FAILURE__LATER_LAWFUL_CELLS_SUPPRESSED__{token(cell)}")
    require(x.get("synthetic_fallback_used") is False, f"FAILURE__SYNTHETIC_FALLBACK_USED__{token(cell)}")
    require(isinstance(x.get("disposition"), str) and x["disposition"], f"BLOCKER__STOP_DISPOSITION_MISSING__{token(cell)}")
    require(isinstance(x.get("evidence_paths"), list) and x["evidence_paths"], f"BLOCKER__STOP_EVIDENCE_PATHS_MISSING__{token(cell)}")
    if cell == "WVS7/C":
        require(x.get("kind") == "WVS7_C_CURRENT_PORTABILITY_FAILURE", "FAILURE__WVS_C_WRONG_STOP_KIND")
        require(x.get("disposition") == e["wvs_c"]["required_disposition"], "FAILURE__WVS_C_DISPOSITION_DRIFT")
        require(x.get("blocking_scope") == "NONBLOCKING_PRESERVED_CANDIDATE_EVIDENCE", "FAILURE__WVS_C_WRONG_BLOCKING_SCOPE")
    return x

def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()

def main():
    final = {"schema":"RAWLSING_EE_P2X_FINAL_VERIFICATION_RECEIPT@1.0.0","terminal":None,
             "verified_receipts":[],"blocking_failures":[],"source_metric_pooling":False,"ranking_or_selection":False}
    terminal = None
    try:
        e = load(EXPECT_PATH)
        c = load(CONTRACT_PATH)
        require(e.get("authority_class") == "PROPOSED_FOR_HQ_ADOPTION__NON_OPERATIVE_UNTIL_ADOPTED",
                "BLOCKER__RECEIPT_PREP_AUTHORITY_CLASS_DRIFT")

        # Frozen file identities: verify local tree still contains the exact adopted law.
        lock1_path = REPO / e["lock1"]["manifest_json_path"]
        require(lock1_path.exists(), "BLOCKER__LOCK1_MANIFEST_MISSING")
        require(git_blob_sha1(lock1_path) == e["lock1"]["manifest_json_git_blob_sha1"], "FAILURE__LOCK1_MANIFEST_DRIFT")
        seam_path = REPO / e["execution_seam"]["path"]
        require(seam_path.exists(), "BLOCKER__P2R1_EXECUTION_SEAM_MISSING")
        require(git_blob_sha1(seam_path) == e["execution_seam"]["git_blob_sha1"], "FAILURE__P2R1_EXECUTION_SEAM_DRIFT")

        for stage in e["preserved_completed_stages"].values():
            p = REPO / stage["receipt_path"]
            require(p.exists(), "BLOCKER__PRESERVED_STAGE_RECEIPT_MISSING__" + token(stage["receipt_path"]))
            require(sha256_file(p) == stage["receipt_sha256"], "FAILURE__PRESERVED_STAGE_RECEIPT_DRIFT__" + token(stage["receipt_path"]))

        manifest = load(COURT / "00_COURT_RUN_MANIFEST.json")
        scan_forbidden_keys(manifest, set(e["forbidden_output_keys"]), "court_manifest")
        require(manifest.get("hq_handoff_commit") == e["hq"]["handoff_commit"], "FAILURE__COURT_HQ_AUTHORITY_DRIFT")
        require(manifest.get("lock1_manifest_blob") == e["lock1"]["manifest_json_git_blob_sha1"], "FAILURE__COURT_LOCK1_DRIFT")
        require(manifest.get("lock2_hash") == e["lock2"]["hash"], "FAILURE__COURT_LOCK2_DRIFT")
        exact_runtime(manifest.get("runtime", {}), e["runtime"], "court")
        require(is_hex64(manifest.get("physical_host_identity_sha256")), "BLOCKER__COURT_HOST_IDENTITY_MISSING")
        require(manifest.get("source_metric_pooling") is False, "FAILURE__CROSS_UNIVERSE_METRIC_POOLING")
        require(manifest.get("ranking_or_selection") is False, "FAILURE__RANKING_OR_SELECTION_EMITTED")
        executed_stages = manifest.get("executed_stage_ids")
        require(isinstance(executed_stages, list), "BLOCKER__EXECUTED_STAGE_LOG_MISSING")
        for forbidden_stage in e["preserved_completed_stages"]:
            require(forbidden_stage not in executed_stages, "FAILURE__PRESERVED_COMPLETED_STAGE_RERUN__" + forbidden_stage)

        attempted = manifest.get("attempted_cells")
        require(isinstance(attempted, list), "BLOCKER__ATTEMPT_ORDER_MISSING")
        require(len(attempted) == len(set(attempted)), "FAILURE__CELL_RERUN_OR_DUPLICATE_ATTEMPT")
        require(all(x in EXECUTABLE for x in attempted), "FAILURE__UNKNOWN_OR_WVS_C_ATTEMPT")
        require(attempted == [x for x in EXECUTABLE if x in attempted], "FAILURE__SOURCE_OR_CANDIDATE_ORDER_DRIFT")

        coverage = manifest.get("coverage")
        require(isinstance(coverage, list) and [x.get("cell") for x in coverage] == CANONICAL,
                "BLOCKER__REQUIRED_CELL_COVERAGE_SHAPE")
        host_ids=set()
        source_oracles={}
        source_catalogs={}
        wvs_projections=set()
        qualifying={}
        wvs_learned=[]
        blocking=[]

        for idx, entry in enumerate(coverage):
            cell = CANONICAL[idx]
            state = entry.get("state")
            cell_receipt = entry.get("cell_receipt")
            failure_receipt = entry.get("failure_receipt")
            require(state in {"QUALIFYING_CELL_COMPLETE","AUTHORIZED_STOP","PRESERVED_FAILURE"},
                    "BLOCKER__CELL_PENDING__" + token(cell))

            if state == "QUALIFYING_CELL_COMPLETE":
                require(cell in attempted, "FAILURE__QUALIFYING_CELL_NOT_ATTEMPTED__" + token(cell))
                require(cell != "WVS7/C", "FAILURE__WVS_C_EXECUTED")
                require(isinstance(cell_receipt,str) and cell_receipt,
                        "BLOCKER__CELL_RECEIPT_POINTER_MISSING__" + token(cell))
                require(failure_receipt is None, "FAILURE__QUALIFYING_CELL_HAS_FAILURE_RECEIPT__" + token(cell))
                cell_path=REPO/cell_receipt
                require(cell_path.exists(), "BLOCKER__POINTED_CELL_RECEIPT_MISSING__" + token(cell))
                cell_obj=validate_cell(cell_path, cell, e, c, host_ids, source_oracles, source_catalogs, wvs_projections)
                qualifying[cell]=cell_obj
                final["verified_receipts"].append(cell_receipt)
                source,candidate=cell.split("/")
                learned_path=COURT/"learned"/f"{source}__{candidate}.json"
                if source=="LITS_I":
                    validate_lits_learned(learned_path, cell, e)
                else:
                    wvs_learned.append(validate_wvs_learned(learned_path, cell, e, cell_obj["outputs"]))
                final["verified_receipts"].append(relative(learned_path))
                if candidate in {"B","C"}:
                    d=COURT/"deletion"/f"{source}__{candidate}.json"
                    validate_deletion(d, cell, cell_obj["outputs"])
                    final["verified_receipts"].append(relative(d))
                if candidate=="A":
                    p=COURT/"persistence"/f"{source}__A.json"
                    validate_a_persistence(p, cell)
                    final["verified_receipts"].append(relative(p))
            else:
                require(isinstance(failure_receipt,str) and failure_receipt,
                        "BLOCKER__FAILURE_RECEIPT_POINTER_MISSING__" + token(cell))
                failure_path=REPO/failure_receipt
                require(failure_path.exists(), "BLOCKER__POINTED_FAILURE_RECEIPT_MISSING__" + token(cell))
                fail=validate_failure(failure_path, cell, e)
                final["verified_receipts"].append(failure_receipt)

                if cell in attempted:
                    require(isinstance(cell_receipt,str) and cell_receipt,
                            "BLOCKER__ATTEMPTED_STOPPED_CELL_RECEIPT_MISSING__" + token(cell))
                    cell_path=REPO/cell_receipt
                    require(cell_path.exists(), "BLOCKER__POINTED_STOPPED_CELL_RECEIPT_MISSING__" + token(cell))
                    validate_cell(cell_path, cell, e, c, host_ids, source_oracles, source_catalogs,
                                  wvs_projections, expected_disposition="AUTHORIZED_STOP")
                    final["verified_receipts"].append(cell_receipt)
                else:
                    require(cell_receipt is None, "FAILURE__UNATTEMPTED_CELL_HAS_EXECUTION_RECEIPT__" + token(cell))
                    require(cell=="WVS7/C" or fail.get("kind") in {"COMMON_SOURCE_AUTHORITY_FAILURE","INTERRUPTED_PARTIAL_EXECUTION"},
                            "FAILURE__SKIPPED_CELL_WITHOUT_AUTHORIZED_BLOCKING_STOP__" + token(cell))

                if cell=="WVS7/C":
                    require(state=="PRESERVED_FAILURE", "FAILURE__WVS_C_COVERAGE_STATE")
                else:
                    require(state=="AUTHORIZED_STOP", "FAILURE__NON_WVS_C_PRESERVED_FAILURE_STATE__" + token(cell))

                if fail.get("kind") in {"COMMON_SOURCE_AUTHORITY_FAILURE","INTERRUPTED_PARTIAL_EXECUTION"} or fail.get("blocking_scope") in {"SOURCE_ONLY","COURT_UNTIL_RESUME"}:
                    blocking.append((idx, fail["disposition"]))
                if fail.get("kind")=="PARITY_ORACLE_FAILURE" and fail.get("blocking_scope")=="SOURCE_ONLY":
                    blocking.append((idx, fail["disposition"]))

        if host_ids:
            require(len(host_ids)==1, "FAILURE__SAME_PHYSICAL_HOST_VIOLATION")
            require(next(iter(host_ids))[0] == manifest["physical_host_identity_sha256"], "FAILURE__COURT_CELL_HOST_IDENTITY_MISMATCH")
        require(all(len(v)==1 for v in source_oracles.values()), "FAILURE__ORACLE_DIFFERS_BY_CANDIDATE")
        require(all(len(v)==1 for v in source_catalogs.values()), "FAILURE__RUNTIME_CATALOG_DIFFERS_BY_CANDIDATE")
        require(len(wvs_projections) <= 1, "FAILURE__WVS_GOVERNED_PROJECTION_DIFFERS_BY_CANDIDATE")

        # No WVS-C receipt may exist as an execution/learned product.
        require(not (COURT/"cells"/"WVS7__C.json").exists(), "FAILURE__WVS_C_EXECUTION_RECEIPT_EXISTS")
        require(not (COURT/"learned"/"WVS7__C.json").exists(), "FAILURE__WVS_C_LEARNED_RECEIPT_EXISTS")

        # Successful WVS A/B must produce the same governed identities.
        if len(wvs_learned)==2:
            a,b=wvs_learned
            require((a["product_identity"],a["semantic_identity"],a["replay_identity"]) ==
                    (b["product_identity"],b["semantic_identity"],b["replay_identity"]),
                    "FAILURE__WVS_A_B_GOVERNED_IDENTITY_MISMATCH")

        if blocking:
            blocking.sort()
            terminal=blocking[0][1]
            final["blocking_failures"]=[{"cell":CANONICAL[i],"disposition":d} for i,d in blocking]
        else:
            terminal=PASS
    except CourtBlocker as exc:
        terminal=str(exc)

    final["terminal"]=terminal
    COURT.mkdir(parents=True, exist_ok=True)
    FINAL.write_text(json.dumps(final, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(terminal)
    return 0 if terminal==PASS else 1

if __name__=="__main__":
    sys.exit(main())
