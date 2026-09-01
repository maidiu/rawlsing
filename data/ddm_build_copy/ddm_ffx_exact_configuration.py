#!/usr/bin/env python3
"""FFX002-R2 Core A EXACT_CONFIGURATION_SET producer.

Consumes frozen governed state facts only. No distance/similarity, latent model,
ontology induction, semantic recoding/inference, or missingness-based exposure.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from data.ddm_build_copy.field_forge_ffx002_harness import HarnessViolation as _HarnessViolation, compute_common_hash as _shared_common_hash
except ModuleNotFoundError:  # direct script execution
    from field_forge_ffx002_harness import HarnessViolation as _HarnessViolation, compute_common_hash as _shared_common_hash

ARM_ID = "A"
VIEW_FAMILY = "EXACT_CONFIGURATION_SET"
INPUT_SCHEMA_VERSION = "FFX_EXACT_CONFIGURATION_INPUT_R1"

COMMON_MANIFEST_REQUIRED_FIELDS = (
    "manifest_schema_version", "current_execution_sha", "observation_substrate_ref",
    "respondent_entity_binding_ref", "exposure_risk_set_ref", "source_scope_ref",
    "source_native_measurement_refs", "qimpl_measurement_binding_refs",
    "response_state_semantics_ref", "special_state_semantics_ref",
    "ttar_execution_sequence", "post_transform_state_manifest", "claim_scope_ref",
    "estimand_ref", "weight_design_refs", "analytic_role_authority_refs",
    "ancestry_disjointness_receipt", "unresolved_noncomparable_manifest",
    "source_native_ancestry_ref", "loss_profile", "holdout_generation_inputs_hash",
    "canonicalization_spec", "manifest_hash",
)

TOP_KEYS = {
    "schema_version", "arm_id", "common_semantic_input_manifest", "method_contract",
    "frozen_units", "query_manifest", "replay_context",
}
METHOD_KEYS = {
    "position_measurement_ids", "disposition_measurement_ids",
    "minimum_exact_support", "minimum_backoff_support", "support_basis",
    "distribution_basis", "weighting_mode", "backoff_mode", "pruning_mode",
}
UNIT_KEYS = {
    "unit_id", "exposed_measurement_ids", "position_states", "disposition_states",
    "analysis_weight",
}
QUERY_KEYS = {
    "query_id", "position_condition", "disposition_measurement_ids", "backoff_sequence",
}
REPLAY_KEYS = {
    "code_version_ref", "partition_manifest_ref", "partition_manifest_hash",
    "query_manifest_ref", "hostile_fixture_refs", "execution_contract_ref",
}


class CoreAContractError(ValueError):
    def __init__(self, status: str, detail: str):
        self.status, self.detail = status, detail
        super().__init__(f"{status}: {detail}")


def fail(status: str, detail: str) -> None:
    raise CoreAContractError(status, detail)


def _json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def stable_hash(value: Any) -> str:
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _ptr(path: str, key: str) -> str:
    key = str(key).replace("~", "~0").replace("/", "~1")
    return f"{path}/{key}" if path else f"/{key}"


def _manifest_normalize(value: Any, path: str, set_paths: set[str]) -> Any:
    if isinstance(value, dict):
        return {str(k): _manifest_normalize(v, _ptr(path, str(k)), set_paths) for k, v in value.items()}
    if isinstance(value, list):
        items = [_manifest_normalize(v, f"{path}/{i}", set_paths) for i, v in enumerate(value)]
        if path in set_paths:
            items.sort(key=_json_bytes)
        return items
    return value


def recompute_common_manifest_hash(manifest: dict[str, Any]) -> str:
    """Recompute only through the FFP009 frozen canonicalization contract."""
    try:
        return _shared_common_hash(manifest)
    except _HarnessViolation as exc:
        fail(exc.state, exc.detail)


def attest_common_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    received = str(manifest.get("manifest_hash", "")).strip()
    if not received:
        fail("COMMON_INPUT_MISSING_HARD_FIELD", "manifest_hash")
    recomputed = recompute_common_manifest_hash(manifest)
    if received != recomputed:
        fail("COMMON_INPUT_ARM_HASH_DIVERGENCE", f"received={received} recomputed={recomputed}")
    return {
        "schema_version": "FFX_COMMON_INPUT_ATTESTATION_R1", "arm_id": ARM_ID,
        "view_family": VIEW_FAMILY, "received_manifest_hash": received,
        "recomputed_manifest_hash": recomputed, "attestation_status": "ATTESTED_EQUAL",
    }


def _exact_keys(obj: dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(obj) - allowed)
    if unknown:
        fail("CORE_A_INPUT_SCHEMA_REJECTED", f"{label} unknown fields: {unknown}")


def _ids(value: Any, label: str, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        fail("CORE_A_INPUT_SCHEMA_REJECTED", f"{label} must be array")
    out = []
    for x in value:
        if not isinstance(x, str) or not x.strip():
            fail("CORE_A_INPUT_SCHEMA_REJECTED", f"{label} contains invalid id")
        out.append(x.strip())
    if len(out) != len(set(out)):
        fail("CORE_A_INPUT_SCHEMA_REJECTED", f"{label} contains duplicate ids")
    if not allow_empty and not out:
        fail("CORE_A_INPUT_SCHEMA_REJECTED", f"{label} must not be empty")
    return out


def _states(value: Any, label: str) -> dict[str, str]:
    if not isinstance(value, dict):
        fail("CORE_A_INPUT_SCHEMA_REJECTED", f"{label} must be object")
    out = {}
    for k, v in value.items():
        if not isinstance(k, str) or not k.strip() or not isinstance(v, str) or not v.strip():
            fail("CORE_A_INPUT_SCHEMA_REJECTED", f"{label} has invalid measurement/state id")
        out[k.strip()] = v.strip()
    return out


def _method(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail("CORE_A_INPUT_SCHEMA_REJECTED", "method_contract must be object")
    _exact_keys(value, METHOD_KEYS, "method_contract")
    pos = _ids(value.get("position_measurement_ids"), "position_measurement_ids")
    disp = _ids(value.get("disposition_measurement_ids"), "disposition_measurement_ids")
    if set(pos) & set(disp):
        fail("CORE_A_ACTIVE_SPACE_OVERLAP", f"overlap={sorted(set(pos) & set(disp))}")
    try:
        ef, bf = int(value.get("minimum_exact_support")), int(value.get("minimum_backoff_support"))
    except (TypeError, ValueError):
        fail("CORE_A_INPUT_SCHEMA_REJECTED", "support floors must be integers")
    if ef < 1 or bf < 1:
        fail("CORE_A_INPUT_SCHEMA_REJECTED", "support floors must be >=1")
    if value.get("support_basis") != "UNWEIGHTED_COUNT":
        fail("CORE_A_FORBIDDEN_METHOD", "support_basis must be UNWEIGHTED_COUNT")
    if value.get("distribution_basis") not in {"UNWEIGHTED_COUNT", "ANALYSIS_WEIGHT"}:
        fail("CORE_A_FORBIDDEN_METHOD", "unsupported distribution_basis")
    if value.get("weighting_mode") not in {"NONE", "FROZEN_ANALYSIS_WEIGHT"}:
        fail("CORE_A_FORBIDDEN_METHOD", "unsupported weighting_mode")
    expected_weighting = "FROZEN_ANALYSIS_WEIGHT" if value["distribution_basis"] == "ANALYSIS_WEIGHT" else "NONE"
    if value["weighting_mode"] != expected_weighting:
        fail("CORE_A_ESTIMAND_WEIGHT_BINDING_INVALID", "distribution/weighting modes disagree")
    if value.get("backoff_mode") != "DECLARED_NESTED_SUBSET_ONLY":
        fail("CORE_A_FORBIDDEN_METHOD", "backoff must be DECLARED_NESTED_SUBSET_ONLY")
    if value.get("pruning_mode") != "NONE":
        fail("CORE_A_FORBIDDEN_METHOD", "pruning_mode must be NONE")
    return {**value, "position_measurement_ids": pos, "disposition_measurement_ids": disp,
            "minimum_exact_support": ef, "minimum_backoff_support": bf}


def _units(value: Any, method: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        fail("CORE_A_INPUT_SCHEMA_REJECTED", "frozen_units must be nonempty array")
    declared = set(method["position_measurement_ids"]) | set(method["disposition_measurement_ids"])
    seen, out = set(), []
    for i, unit in enumerate(value):
        if not isinstance(unit, dict):
            fail("CORE_A_INPUT_SCHEMA_REJECTED", f"frozen_units[{i}] must be object")
        _exact_keys(unit, UNIT_KEYS, f"frozen_units[{i}]")
        uid = str(unit.get("unit_id", "")).strip()
        if not uid or uid in seen:
            fail("CORE_A_EMPIRICAL_UNIT_IDENTITY_INVALID", f"invalid/duplicate unit_id {uid!r}")
        seen.add(uid)
        exposed = set(_ids(unit.get("exposed_measurement_ids"), f"{uid}.exposed_measurement_ids", True))
        if not exposed <= declared:
            fail("CORE_A_EXPOSURE_SCOPE_INVALID", f"{uid} undeclared exposure {sorted(exposed-declared)}")
        ps, ds = _states(unit.get("position_states"), f"{uid}.position_states"), _states(unit.get("disposition_states"), f"{uid}.disposition_states")
        if not set(ps) <= set(method["position_measurement_ids"]) or not set(ds) <= set(method["disposition_measurement_ids"]):
            fail("CORE_A_FROZEN_STATE_SCOPE_INVALID", f"{uid} state outside declared space")
        state_keys = set(ps) | set(ds)
        if not state_keys <= exposed:
            fail("CORE_A_EXPOSURE_STATE_DIVERGENCE", f"{uid} state without explicit exposure")
        if exposed - state_keys:
            fail("CORE_A_EXPOSURE_STATE_DIVERGENCE", f"{uid} exposure without frozen state: {sorted(exposed-state_keys)}")
        if method["weighting_mode"] == "FROZEN_ANALYSIS_WEIGHT":
            raw = unit.get("analysis_weight")
            try:
                weight = float(raw)
            except (TypeError, ValueError):
                fail("CORE_A_ESTIMAND_WEIGHT_BINDING_INVALID", f"{uid} invalid analysis_weight")
            if isinstance(raw, bool) or not math.isfinite(weight) or weight < 0:
                fail("CORE_A_ESTIMAND_WEIGHT_BINDING_INVALID", f"{uid} analysis_weight must be finite >=0")
        else:
            if "analysis_weight" in unit:
                fail("CORE_A_ESTIMAND_WEIGHT_BINDING_INVALID", f"{uid} unexpected analysis_weight")
            weight = 1.0
        out.append({"unit_id": uid, "exposed_measurement_ids": sorted(exposed),
                    "position_states": ps, "disposition_states": ds, "analysis_weight": weight})
    return sorted(out, key=lambda x: x["unit_id"])


def _queries(value: Any, method: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        fail("CORE_A_INPUT_SCHEMA_REJECTED", "query_manifest must be array")
    pos, disp, seen, out = set(method["position_measurement_ids"]), set(method["disposition_measurement_ids"]), set(), []
    for i, q in enumerate(value):
        if not isinstance(q, dict):
            fail("CORE_A_INPUT_SCHEMA_REJECTED", f"query_manifest[{i}] must be object")
        _exact_keys(q, QUERY_KEYS, f"query_manifest[{i}]")
        qid = str(q.get("query_id", "")).strip()
        if not qid or qid in seen:
            fail("CORE_A_QUERY_MANIFEST_INVALID", f"invalid/duplicate query_id {qid!r}")
        seen.add(qid)
        raw = _states(q.get("position_condition"), f"{qid}.position_condition")
        if not raw or not set(raw) <= pos:
            fail("CORE_A_QUERY_MANIFEST_INVALID", f"{qid} invalid position_condition")
        cond = {mid: raw[mid] for mid in method["position_measurement_ids"] if mid in raw}
        targets = _ids(q.get("disposition_measurement_ids"), f"{qid}.disposition_measurement_ids")
        if not set(targets) <= disp:
            fail("CORE_A_QUERY_MANIFEST_INVALID", f"{qid} invalid disposition target")
        seq = q.get("backoff_sequence")
        if not isinstance(seq, list):
            fail("CORE_A_QUERY_MANIFEST_INVALID", f"{qid}.backoff_sequence must be array")
        prev, norm = list(cond), []
        for level, raw_retained in enumerate(seq, 1):
            retained = _ids(raw_retained, f"{qid}.backoff_sequence[{level-1}]", True)
            if not set(retained) <= set(prev) or len(retained) >= len(prev):
                fail("CORE_A_QUERY_MANIFEST_INVALID", f"{qid} backoff level {level} is not strict nested subset")
            if retained != [mid for mid in prev if mid in set(retained)]:
                fail("CORE_A_QUERY_MANIFEST_INVALID", f"{qid} backoff level {level} reorders measurements")
            norm.append(retained)
            prev = retained
        out.append({"query_id": qid, "position_condition": cond,
                    "disposition_measurement_ids": targets, "backoff_sequence": norm})
    return out


def _replay(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail("CORE_A_INPUT_SCHEMA_REJECTED", "replay_context must be object")
    _exact_keys(value, REPLAY_KEYS, "replay_context")
    out = {}
    for f in ("code_version_ref", "partition_manifest_ref", "partition_manifest_hash",
              "query_manifest_ref", "execution_contract_ref"):
        v = value.get(f)
        if not isinstance(v, str) or not v.strip():
            fail("CORE_A_REPLAY_BINDING_INVALID", f"{f} must be exact nonempty ref/hash")
        out[f] = v.strip()
    out["hostile_fixture_refs"] = _ids(value.get("hostile_fixture_refs"), "hostile_fixture_refs", True)
    return out


def _validate(payload: Any):
    if not isinstance(payload, dict):
        fail("CORE_A_INPUT_SCHEMA_REJECTED", "top-level input must be object")
    _exact_keys(payload, TOP_KEYS, "top-level input")
    if payload.get("schema_version") != INPUT_SCHEMA_VERSION or payload.get("arm_id") != ARM_ID:
        fail("CORE_A_INPUT_SCHEMA_REJECTED", "wrong schema_version or arm_id")
    manifest = payload.get("common_semantic_input_manifest")
    if not isinstance(manifest, dict):
        fail("CORE_A_INPUT_SCHEMA_REJECTED", "common manifest must be object")
    att = attest_common_manifest(manifest)
    method = _method(payload.get("method_contract"))
    return manifest, method, _units(payload.get("frozen_units"), method), _queries(payload.get("query_manifest"), method), _replay(payload.get("replay_context")), att


def _complete(unit: dict[str, Any], mids: list[str], field: str) -> bool:
    exp, states = set(unit["exposed_measurement_ids"]), unit[field]
    return all(mid in exp and mid in states for mid in mids)


def _pairs(states: dict[str, str], mids: list[str]) -> list[dict[str, str]]:
    return [{"measurement_id": mid, "state_id": states[mid]} for mid in mids]


def _cfg_id(space: str, mids: list[str], states: dict[str, str]) -> str:
    return f"{space[:1]}CFG_{stable_hash({'space': space, 'state_pairs': _pairs(states, mids)})[:24]}"


def _distribution(matched: list[dict[str, Any]], targets: list[str], method: dict[str, Any]) -> list[dict[str, Any]]:
    groups = defaultdict(list)
    for u in matched:
        if _complete(u, targets, "disposition_states"):
            groups[tuple(u["disposition_states"][m] for m in targets)].append(u)
    total_n = sum(map(len, groups.values()))
    total_w = math.fsum(u["analysis_weight"] for rows in groups.values() for u in rows)
    if not total_n:
        return []
    scored = []
    for key, rows in groups.items():
        w = math.fsum(u["analysis_weight"] for u in rows)
        score = len(rows) if method["distribution_basis"] == "UNWEIGHTED_COUNT" else w
        scored.append((key, rows, w, score))
    mx = max(x[3] for x in scored)
    ties = sum(1 for x in scored if x[3] == mx)
    out = []
    for key, rows, w, score in scored:
        states = dict(zip(targets, key))
        status = ("MODAL" if ties == 1 else "MODAL_TIE") if score == mx else "MINORITY_ALTERNATIVE"
        out.append({
            "disposition_configuration_id": _cfg_id("DISPOSITION", targets, states),
            "configuration_order": len(targets), "state_pairs": _pairs(states, targets),
            "support_n_unweighted": len(rows), "support_mass_analysis_weight": w,
            "probability_unweighted": len(rows) / total_n,
            "probability_analysis_weight": w / total_w if total_w > 0 else 0.0,
            "branch_status": status,
        })
    basis = "probability_unweighted" if method["distribution_basis"] == "UNWEIGHTED_COUNT" else "probability_analysis_weight"
    return sorted(out, key=lambda r: (0 if r["branch_status"].startswith("MODAL") else 1, -r[basis], r["disposition_configuration_id"]))


def _surfaces(units: list[dict[str, Any]], method: dict[str, Any]):
    pids, dids = method["position_measurement_ids"], method["disposition_measurement_ids"]
    pg, dg, both, members = defaultdict(list), defaultdict(list), defaultdict(list), []
    for u in units:
        pok, dok = _complete(u, pids, "position_states"), _complete(u, dids, "disposition_states")
        pid = did = None
        if pok:
            pk = tuple(u["position_states"][m] for m in pids); pg[pk].append(u); pid = _cfg_id("POSITION", pids, u["position_states"])
        if dok:
            dk = tuple(u["disposition_states"][m] for m in dids); dg[dk].append(u); did = _cfg_id("DISPOSITION", dids, u["disposition_states"])
        if pok and dok:
            both[tuple(u["position_states"][m] for m in pids)].append(u)
        members.append({"unit_id": u["unit_id"], "position_configuration_id": pid,
                        "disposition_configuration_id": did, "coexposed_for_full_cross_surface": pok and dok})

    def index(space, mids, groups):
        rows = []
        for key, us in groups.items():
            st = dict(zip(mids, key))
            rows.append({"configuration_id": _cfg_id(space, mids, st), "configuration_order": len(mids),
                         "state_pairs": _pairs(st, mids), "support_n_unweighted": len(us),
                         "support_mass_analysis_weight": math.fsum(u["analysis_weight"] for u in us)})
        return sorted(rows, key=lambda r: r["configuration_id"])

    cross = []
    for key, us in both.items():
        st = dict(zip(pids, key)); branches = _distribution(us, dids, method)
        cross.append({
            "position_configuration_id": _cfg_id("POSITION", pids, st),
            "position_state_pairs": _pairs(st, pids),
            "eligible_joint_support_n_unweighted": sum(b["support_n_unweighted"] for b in branches),
            "eligible_joint_support_mass_analysis_weight": math.fsum(b["support_mass_analysis_weight"] for b in branches),
            "destination_branch_count": len(branches),
            "counterpattern_status": "MULTIPLE_EXACT_DESTINATIONS_PRESENT" if len(branches) > 1 else "SINGLE_EXACT_DESTINATION_OBSERVED",
            "disposition_distribution": branches,
        })
    config = {
        "schema_version": "FFX_EXACT_CONFIGURATION_SET_R1", "arm_id": ARM_ID, "view_family": VIEW_FAMILY,
        "position_measurement_ids": pids, "disposition_measurement_ids": dids,
        "position_configuration_index": index("POSITION", pids, pg),
        "disposition_configuration_index": index("DISPOSITION", dids, dg),
        "same_unit_membership": sorted(members, key=lambda r: r["unit_id"]),
        "input_unit_count": len(units),
        "full_position_coexposed_unit_count": sum(_complete(u, pids, "position_states") for u in units),
        "full_disposition_coexposed_unit_count": sum(_complete(u, dids, "disposition_states") for u in units),
        "full_cross_surface_coexposed_unit_count": sum(_complete(u, pids, "position_states") and _complete(u, dids, "disposition_states") for u in units),
    }
    return config, sorted(cross, key=lambda r: r["position_configuration_id"])


def _match(u, cond, retained, targets):
    return _complete(u, retained, "position_states") and _complete(u, targets, "disposition_states") and all(u["position_states"][m] == cond[m] for m in retained)


def _run_queries(units, queries, method):
    out = []
    for q in queries:
        exact = list(q["position_condition"]); levels = [exact] + q["backoff_sequence"]; attempts = []; selected = None
        for i, retained in enumerate(levels):
            matched = [u for u in units if _match(u, q["position_condition"], retained, q["disposition_measurement_ids"])]
            floor = method["minimum_exact_support"] if i == 0 else method["minimum_backoff_support"]
            n, w = len(matched), math.fsum(u["analysis_weight"] for u in matched)
            mass_ok = method["distribution_basis"] != "ANALYSIS_WEIGHT" or w > 0
            attempt = {
                "level": "EXACT" if i == 0 else f"BACKOFF_{i}",
                "retained_position_measurement_ids": retained,
                "relaxed_position_measurement_ids": [m for m in exact if m not in retained],
                "support_threshold_unweighted": floor, "support_n_unweighted": n,
                "support_mass_analysis_weight": w,
                "support_status": "SUFFICIENT" if n >= floor else "LOW_SUPPORT",
                "estimand_mass_status": "POSITIVE_OR_NOT_REQUIRED" if mass_ok else "ZERO_ANALYSIS_WEIGHT_MASS",
                "uncertainty_status": "NOT_MODELED__EXACT_EMPIRICAL_MASS_AND_SUPPORT_ONLY",
                "disposition_distribution": _distribution(matched, q["disposition_measurement_ids"], method),
            }
            attempts.append(attempt)
            if n >= floor and mass_ok:
                selected = i; break
        if selected is None:
            zero = method["distribution_basis"] == "ANALYSIS_WEIGHT" and any(a["support_n_unweighted"] >= a["support_threshold_unweighted"] and a["estimand_mass_status"] == "ZERO_ANALYSIS_WEIGHT_MASS" for a in attempts)
            status, chosen = ("ABSTAIN_ZERO_ANALYSIS_WEIGHT_MASS" if zero else "ABSTAIN_NO_LAWFUL_SUPPORTED_LEVEL"), None
        else:
            status, chosen = ("ANSWER_EXACT" if selected == 0 else "ANSWER_DECLARED_BACKOFF"), attempts[selected]
        out.append({
            "query_id": q["query_id"], "query_status": status,
            "exact_position_condition": [{"measurement_id": m, "state_id": q["position_condition"][m]} for m in exact],
            "target_disposition_measurement_ids": q["disposition_measurement_ids"], "attempts": attempts,
            "selected_attempt": chosen, "information_relaxation": [] if chosen is None else chosen["relaxed_position_measurement_ids"],
            "distance_metric_used": False, "semantic_state_changed": False,
        })
    return out


def _method_manifest(method):
    return {
        "schema_version": "FFX_CORE_A_METHOD_MANIFEST_R1", "arm_id": ARM_ID, "view_family": VIEW_FAMILY,
        "same_unit_conjunction": "EXACT_ONLY",
        "configuration_identity": "DECLARED_MEASUREMENT_ORDER_PLUS_OPAQUE_FROZEN_STATE_ID",
        **method,
        "minority_policy": "RETAIN_ALL_OBSERVED_EXACT_DESTINATION_BRANCHES",
        "counterpattern_policy": "MULTIPLE_EXACT_DESTINATIONS_ONLY__NO_SEMANTIC_POLARITY_INFERENCE",
        "higher_order_policy": "NO_ORDER_CAP__EXACT_DECLARED_CONJUNCTION",
        "postfork_state_transformations": [], "distance_metric": None, "similarity_function": None,
        "latent_model": None, "semantic_inference": None, "randomness": "NONE",
    }


def _loss(query_results):
    inv = {
        "I01_empirical_unit_identity": "PRESERVES_BY_CONSTRUCTION",
        "I02_risk_set_integrity": "PRESERVES_BY_CONSTRUCTION",
        "I03_source_native_measurement_identity": "PRESERVES_BY_CONSTRUCTION",
        "I04_exact_same_unit_cooccurrence": "PRESERVES_BY_CONSTRUCTION",
        "I05_minority_branch_preservation": "PRESERVES_BY_CONSTRUCTION",
        "I06_higher_order_configuration": "PRESERVES_BY_CONSTRUCTION",
        "I07_conditional_redistribution": "PRESERVES_BY_CONSTRUCTION",
        "I08_rank_order": "DOES_NOT_REPRESENT", "I09_neighborhood": "DOES_NOT_REPRESENT",
        "I10_opposition": "DOES_NOT_REPRESENT", "I11_topology_connectivity": "DOES_NOT_REPRESENT",
        "I12_multimodality": "PRESERVES_AS_EXACT_BRANCHES",
        "I13_contradiction_nonmodal_alternatives": "PRESERVES_BY_CONSTRUCTION",
        "I14_source_instrument_topology": "PRESERVES_AS_PROVENANCE_ONLY",
        "I15_uncertainty_support": "PRESERVES_EXACT_SUPPORT_AND_ABSTENTION__NO_MODEL_UNCERTAINTY_ASSERTED",
        "I16_estimand_fidelity": "PRESERVES_BOUND_DISTRIBUTION_BASIS",
        "I17_cross_context_transportable_signature_components": "DOES_NOT_ASSERT",
        "I18_semantic_manifest_identity": "PRESERVES_BY_ATTESTATION",
    }
    relax = [{
        "query_id": r["query_id"], "loss_type": "DECLARED_QUERY_CONDITION_RELAXATION",
        "relaxed_position_measurement_ids": r["information_relaxation"],
        "raw_exact_attempt_retained": True, "semantic_state_changed": False,
    } for r in query_results if r["query_status"] == "ANSWER_DECLARED_BACKOFF"]
    return {
        "schema_version": "FFX_VIEW_LOSS_MANIFEST_R1", "arm_id": ARM_ID, "view_family": VIEW_FAMILY,
        "invariant_dispositions": inv, "raw_configuration_fact_loss": "NONE",
        "minority_branch_pruning": "NONE", "runtime_query_relaxations": relax,
        "forbidden_claims": ["DISTANCE_OR_NEIGHBORHOOD", "LATENT_PROFILE_OR_CLASS",
                             "SEMANTIC_ONTOLOGY", "CAUSAL_MECHANISM", "CROSS_CONTEXT_TRANSPORT"],
    }


def produce_exact_configuration_set(payload: dict[str, Any]) -> dict[str, Any]:
    manifest, method, units, queries, replay, att = _validate(payload)
    mm = _method_manifest(method)
    config, cross = _surfaces(units, method)
    counter = [{
        "position_configuration_id": row["position_configuration_id"],
        "destination_branch_count": row["destination_branch_count"],
        "destination_configuration_ids": [b["disposition_configuration_id"] for b in row["disposition_distribution"]],
        "modal_destination_configuration_ids": [b["disposition_configuration_id"] for b in row["disposition_distribution"] if b["branch_status"].startswith("MODAL")],
        "minority_destination_configuration_ids": [b["disposition_configuration_id"] for b in row["disposition_distribution"] if b["branch_status"] == "MINORITY_ALTERNATIVE"],
        "counterpattern_semantics": "EXACT_MULTIPLE_DESTINATION_ONLY__NO_POLARITY_OR_MEANING_INFERENCE",
    } for row in cross if row["destination_branch_count"] > 1]
    qr = _run_queries(units, queries, method)
    loss = _loss(qr)
    facts = [{"unit_id": u["unit_id"], "exposed_measurement_ids": u["exposed_measurement_ids"],
              "position_states": u["position_states"], "disposition_states": u["disposition_states"],
              "analysis_weight": u["analysis_weight"]} for u in units]
    build = {
        "schema_version": "FFX_CORE_A_CONFIGURATION_BUILD_MANIFEST_R1", "arm_id": ARM_ID, "view_family": VIEW_FAMILY,
        "common_manifest_hash": att["recomputed_manifest_hash"], "method_manifest_hash": stable_hash(mm),
        "frozen_fact_surface_hash": stable_hash(facts), "query_manifest_hash": stable_hash(queries),
        "loss_manifest_hash": stable_hash(loss),
        "position_configuration_count": len(config["position_configuration_index"]),
        "disposition_configuration_count": len(config["disposition_configuration_index"]),
        "configuration_to_disposition_row_count": len(cross), "counterpattern_row_count": len(counter),
        "query_result_count": len(qr), "exact_same_unit_conjunction": True,
        "minority_alternatives_retained": True, "higher_order_configuration_supported": True,
        "counterpattern_detection": "EXACT_MULTIPLE_DESTINATION_ONLY", "distance_metric_used": False,
        "latent_model_used": False, "semantic_inference_used": False,
    }
    hashes = {
        "common_input_attestation": stable_hash(att), "method_manifest": stable_hash(mm),
        "configuration_set": stable_hash(config), "configuration_to_disposition": stable_hash(cross),
        "counterpattern_index": stable_hash(counter), "query_results": stable_hash(qr),
        "loss_manifest": stable_hash(loss), "build_manifest": stable_hash(build),
    }
    receipt = {
        "schema_version": "FFX_VIEW_REPLAY_RECEIPT_R1", "arm_id": ARM_ID, "view_family": VIEW_FAMILY,
        "common_manifest_hash": att["recomputed_manifest_hash"], "code_version_ref": replay["code_version_ref"],
        "partition_manifest_ref": replay["partition_manifest_ref"], "partition_manifest_hash": replay["partition_manifest_hash"],
        "query_manifest_ref": replay["query_manifest_ref"], "query_manifest_hash": stable_hash(queries),
        "hostile_fixture_refs": replay["hostile_fixture_refs"], "execution_contract_ref": replay["execution_contract_ref"],
        "frozen_fact_surface_hash": stable_hash(facts), "output_hashes": hashes,
        "deterministic_operation_inventory": [
            "COMMON_MANIFEST_SHA256_ATTESTATION", "EXACT_SAME_UNIT_CONFIGURATION_GROUPING",
            "EXACT_DESTINATION_BRANCH_ENUMERATION", "UNWEIGHTED_SUPPORT_COUNTING",
            "FROZEN_ANALYSIS_WEIGHT_SUMMATION_IF_BOUND", "DECLARED_NESTED_SUBSET_BACKOFF",
            "CANONICAL_JSON_SHA256_OUTPUT_HASHING",
        ],
        "nondeterministic_operation_inventory": [], "seed_usage": "NONE",
        "byte_replay_contract": "CANONICAL_JSON_SORTED_KEYS_COMPACT_UTF8_PLUS_NEWLINE",
        "replay_status": "DETERMINISTIC_REPLAY_READY",
    }
    return {
        "common_input_attestation": att, "method_manifest": mm, "configuration_set": config,
        "configuration_to_disposition": cross, "counterpattern_index": counter, "query_results": qr,
        "loss_manifest": loss, "build_manifest": build, "replay_receipt": receipt,
    }


OUTPUT_FILENAMES = {
    "common_input_attestation": "03_CORE_A_COMMON_INPUT_ATTESTATION.json",
    "method_manifest": "06_CORE_A_METHOD_MANIFEST.json",
    "configuration_set": "07_CORE_A_EXACT_CONFIGURATION_SET.json",
    "configuration_to_disposition": "08_CORE_A_CONFIGURATION_TO_DISPOSITION.json",
    "counterpattern_index": "09_CORE_A_COUNTERPATTERN_INDEX.json",
    "query_results": "10_CORE_A_QUERY_RESULTS.json",
    "loss_manifest": "11_CORE_A_LOSS_MANIFEST.json",
    "build_manifest": "12_CORE_A_CONFIGURATION_BUILD_MANIFEST.json",
    "replay_receipt": "13_CORE_A_REPLAY_RECEIPT.json",
}


def write_outputs(result: dict[str, Any], output_dir: str | Path) -> dict[str, str]:
    root = Path(output_dir); root.mkdir(parents=True, exist_ok=True)
    out = {}
    for key, filename in OUTPUT_FILENAMES.items():
        data = _json_bytes(result[key]) + b"\n"
        (root / filename).write_bytes(data)
        out[filename] = hashlib.sha256(data).hexdigest()
    return out
