#!/usr/bin/env python3
"""FFX002-R2 integrated A/B/C execution stack.

Mechanical orchestration only. It consumes frozen authority/CITC bindings,
never mints semantic authority, never chooses a preferred representation, and
never performs V3 interpretation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    from data.ddm_build_copy import field_forge_ffx002_harness as harness
    from data.ddm_build_copy import ddm_ffx_exact_configuration as core_a
    from data.ddm_build_copy import ffx002_r2_local_geometry as core_b
    from data.ddm_build_copy import ddm_ffx002_r2_direct_conditional as core_c
except ModuleNotFoundError:  # direct script execution
    import field_forge_ffx002_harness as harness
    import ddm_ffx_exact_configuration as core_a
    import ffx002_r2_local_geometry as core_b
    import ddm_ffx002_r2_direct_conditional as core_c

INPUT_SCHEMA_VERSION = "FFX002_R2_INTEGRATED_EXECUTION_STACK_INPUT@1"
OUTPUT_SCHEMA_VERSION = "FFX002_R2_INTEGRATED_EXECUTION_STACK_OUTPUT@1"
RECEIPT_SCHEMA_VERSION = "FFX002_R2_INTEGRATED_RECEIPT_COLLECTION@1"
SCORING_SCHEMA_VERSION = "FFX002_R2_CITC_SCORING_INTERFACE@1"
PREV3_SCHEMA_VERSION = "FFX002_R2_PREV3_DOWNSTREAM_ABLATION@1"
DESIGN_REF = "5343862783959a1455735c0a5eb7b330c76f42d5"
TERMINAL_READY = "PASS__FFX002_R2_INTEGRATED_SOFTWARE_STACK_READY_PENDING_FROZEN_EMPIRICAL_AUTHORITY_BINDINGS"

_FORBIDDEN_CROSS_ARM_KEYS = {
    "learned_output", "learned_outputs", "upstream_arm_output", "upstream_arm_outputs",
    "other_arm_output", "other_arm_outputs", "cross_arm_features",
}
_FORBIDDEN_SEMANTIC_OVERRIDE_FRAGMENTS = (
    "merge", "collapse", "rebin", "recode", "reorder", "role_override", "rerole",
    "re_role", "risk_set_override", "estimand_override", "special_state_pool",
    "semantic_transform", "state_mapping", "state_map",
)


class IntegratedStackError(ValueError):
    def __init__(self, state: str, detail: str = "") -> None:
        self.state, self.detail = state, detail
        super().__init__(f"{state}: {detail}" if detail else state)


def _clone(value: Any) -> Any:
    try:
        return json.loads(json.dumps(value, ensure_ascii=False, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise IntegratedStackError("INTEGRATED_NONCANONICAL_JSON_VALUE", str(exc)) from exc


def _hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()


def _verified_hash(artifact: Mapping[str, Any], field: str, state: str) -> str:
    obj = _clone(dict(artifact))
    supplied = obj.pop(field, None)
    if not isinstance(supplied, str) or len(supplied) != 64:
        raise IntegratedStackError(state, f"{field} missing/invalid")
    expected = harness.hash_payload(obj)
    if supplied.lower() != expected:
        raise IntegratedStackError(state, f"{field} mismatch")
    return supplied.lower()


def _walk_keys(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            p = path + (str(key),)
            yield p, child
            yield from _walk_keys(child, p)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from _walk_keys(child, path + (str(idx),))


def _reject_cross_arm_or_semantic_overrides(value: Mapping[str, Any], arm_id: str) -> None:
    for path, _ in _walk_keys(value):
        leaf = path[-1].lower()
        if leaf in _FORBIDDEN_CROSS_ARM_KEYS:
            raise IntegratedStackError(
                "EXPERIMENT_INVALID__CROSS_ARM_LEARNED_OUTPUT_CONSUMPTION",
                f"arm={arm_id} field={'.'.join(path)}",
            )
        if any(fragment in leaf for fragment in _FORBIDDEN_SEMANTIC_OVERRIDE_FRAGMENTS):
            raise IntegratedStackError(
                "EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE",
                f"arm={arm_id} forbidden field={'.'.join(path)}",
            )


def _common_echo(arm_id: str, arm_input: Mapping[str, Any]) -> Mapping[str, Any] | None:
    if arm_id == "A":
        return arm_input.get("common_semantic_input_manifest")
    return arm_input.get("common_manifest")


def _assert_common_echo(arm_id: str, arm_input: Mapping[str, Any], common: Mapping[str, Any]) -> None:
    echo = _common_echo(arm_id, arm_input)
    if echo is None:
        return
    att = harness.attest_arm(arm_id, echo)
    if (
        att["attestation_status"] != "ATTESTED_EQUAL"
        or att["recomputed_manifest_hash"] != common["manifest_hash"]
    ):
        raise IntegratedStackError(
            "FORK_SEMANTIC_TAMPER__COMMON_MANIFEST_HASH_DIVERGENCE",
            f"arm={arm_id}",
        )


def _assert_semantic_echo_fields(arm_id: str, arm_input: Mapping[str, Any], common: Mapping[str, Any]) -> None:
    expected_by_leaf = {
        "risk_set_ref": ("COMMON_INPUT_RISK_SET_DIVERGENCE", common["exposure_risk_set_ref"]),
        "estimand_ref": ("COMMON_INPUT_ESTIMAND_DIVERGENCE", common["estimand_ref"]),
        "weight_design_refs": ("COMMON_INPUT_ESTIMAND_DIVERGENCE", common["weight_design_refs"]),
        "analytic_role_binding_ref": ("EXPERIMENT_INVALID__ANALYTIC_ROLE_DIVERGENCE", common["analytic_role_authority_refs"]),
        "special_state_semantics_ref": ("EXPERIMENT_INVALID__POSTFORK_SPECIAL_STATE_DIVERGENCE", common["special_state_semantics_ref"]),
        "response_state_semantics_ref": ("EXPERIMENT_INVALID__POSTFORK_STATE_IDENTITY_DIVERGENCE", common["response_state_semantics_ref"]),
        "post_transform_state_manifest_ref": ("EXPERIMENT_INVALID__POSTFORK_STATE_IDENTITY_DIVERGENCE", common["post_transform_state_manifest"]),
    }
    for key_path, value in _walk_keys(arm_input):
        if "common_manifest" in key_path or "common_semantic_input_manifest" in key_path:
            continue
        leaf = key_path[-1]
        if leaf not in expected_by_leaf:
            continue
        state, expected = expected_by_leaf[leaf]
        if _clone(value) != _clone(expected):
            raise IntegratedStackError(state, f"arm={arm_id} field={'.'.join(key_path)}")


def _respondent_ids_from_a(a: Mapping[str, Any]) -> tuple[str, ...]:
    units = a.get("frozen_units")
    if not isinstance(units, list) or not units:
        raise IntegratedStackError("INTEGRATED_ARM_A_INPUT_INVALID", "frozen_units")
    ids = [str(row.get("unit_id", "")) for row in units if isinstance(row, Mapping)]
    if len(ids) != len(units) or any(not x for x in ids) or len(ids) != len(set(ids)):
        raise IntegratedStackError("INTEGRATED_ARM_A_INPUT_INVALID", "unit identity")
    return tuple(sorted(ids))


def _respondent_ids_from_b_surface(surface: Mapping[str, Any], side: str) -> tuple[str, ...]:
    rows = surface.get("rows") if isinstance(surface, Mapping) else None
    if not isinstance(rows, list) or not rows:
        raise IntegratedStackError("INTEGRATED_ARM_B_INPUT_INVALID", side)
    ids = [str(row.get("respondent_id", "")) for row in rows if isinstance(row, Mapping)]
    if len(ids) != len(rows) or any(not x for x in ids) or len(ids) != len(set(ids)):
        raise IntegratedStackError("INTEGRATED_ARM_B_INPUT_INVALID", f"{side} respondent identity")
    return tuple(sorted(ids))


def _respondent_ids_from_c(c: Mapping[str, Any]) -> tuple[str, ...]:
    risk = c.get("risk_set")
    ids = risk.get("respondent_ids") if isinstance(risk, Mapping) else None
    if not isinstance(ids, list) or not ids or any(not isinstance(x, str) or not x for x in ids):
        raise IntegratedStackError("INTEGRATED_ARM_C_INPUT_INVALID", "risk_set.respondent_ids")
    if len(ids) != len(set(ids)):
        raise IntegratedStackError("INTEGRATED_ARM_C_INPUT_INVALID", "duplicate risk-set respondent")
    return tuple(sorted(ids))


def _measurement_sets(a: Mapping[str, Any], b: Mapping[str, Any]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    method = a.get("method_contract")
    if not isinstance(method, Mapping):
        raise IntegratedStackError("INTEGRATED_ARM_A_INPUT_INVALID", "method_contract")
    apos = tuple(method.get("position_measurement_ids", ()))
    adisp = tuple(method.get("disposition_measurement_ids", ()))
    if not apos or not adisp:
        raise IntegratedStackError("INTEGRATED_ARM_A_INPUT_INVALID", "measurement ids")
    pmeas = b.get("position_surface", {}).get("measurements", [])
    dmeas = b.get("disposition_surface", {}).get("measurements", [])
    bpos = tuple(row.get("measurement_id") for row in pmeas if isinstance(row, Mapping))
    bdisp = tuple(row.get("measurement_id") for row in dmeas if isinstance(row, Mapping))
    if set(apos) != set(bpos) or set(adisp) != set(bdisp):
        raise IntegratedStackError(
            "EXPERIMENT_INVALID__ANALYTIC_ROLE_DIVERGENCE",
            f"A/B position={apos}/{bpos} disposition={adisp}/{bdisp}",
        )
    return apos, adisp


def _state_catalog(c: Mapping[str, Any]) -> Mapping[str, Any]:
    registry = c.get("frozen_state_registry")
    states = registry.get("states_by_measurement") if isinstance(registry, Mapping) else None
    if not isinstance(states, Mapping) or not states:
        raise IntegratedStackError("INTEGRATED_ARM_C_INPUT_INVALID", "frozen_state_registry")
    return states


def _assert_state_coherence(
    a: Mapping[str, Any], b: Mapping[str, Any], c: Mapping[str, Any],
    position_ids: Sequence[str], disposition_ids: Sequence[str],
) -> None:
    catalog = _state_catalog(c)
    declared = set(position_ids) | set(disposition_ids)
    if not declared <= set(catalog):
        raise IntegratedStackError("EXPERIMENT_INVALID__POSTFORK_STATE_IDENTITY_DIVERGENCE", "catalog missing active measurements")

    for unit in a["frozen_units"]:
        for field in ("position_states", "disposition_states"):
            states = unit.get(field, {})
            if not isinstance(states, Mapping):
                raise IntegratedStackError("EXPERIMENT_INVALID__POSTFORK_STATE_IDENTITY_DIVERGENCE", field)
            for mid, sid in states.items():
                if mid not in catalog or sid not in catalog[mid]:
                    raise IntegratedStackError(
                        "EXPERIMENT_INVALID__POSTFORK_STATE_IDENTITY_DIVERGENCE",
                        f"A {unit.get('unit_id')}/{mid}={sid}",
                    )

    for side in ("position_surface", "disposition_surface"):
        surface = b.get(side)
        if not isinstance(surface, Mapping):
            raise IntegratedStackError("INTEGRATED_ARM_B_INPUT_INVALID", side)
        for measurement in surface.get("measurements", []):
            mid = measurement.get("measurement_id")
            states = measurement.get("state_ids")
            if mid not in catalog or set(states or ()) != set(catalog[mid]):
                raise IntegratedStackError(
                    "EXPERIMENT_INVALID__POSTFORK_STATE_IDENTITY_DIVERGENCE",
                    f"B {mid} state catalog differs",
                )
        for row in surface.get("rows", []):
            for mid, sid in row.get("state_by_measurement", {}).items():
                if mid not in catalog or sid not in catalog[mid]:
                    raise IntegratedStackError(
                        "EXPERIMENT_INVALID__POSTFORK_STATE_IDENTITY_DIVERGENCE",
                        f"B {row.get('respondent_id')}/{mid}={sid}",
                    )


def _assert_c_query_roles(c: Mapping[str, Any], position_ids: Sequence[str], disposition_ids: Sequence[str]) -> None:
    requests = c.get("requests")
    if not isinstance(requests, list) or not requests:
        raise IntegratedStackError("INTEGRATED_ARM_C_INPUT_INVALID", "requests")
    pos, disp = set(position_ids), set(disposition_ids)
    for request in requests:
        if not isinstance(request, Mapping) or not request.get("query_id"):
            raise IntegratedStackError("INTEGRATED_ARM_C_INPUT_INVALID", "request identity")
        condition = request.get("condition", {})
        mids = {
            row.get("measurement_id") for row in condition.get("states", [])
            if isinstance(row, Mapping)
        }
        outcome_mid = request.get("outcome", {}).get("measurement_id")
        if not mids or not mids <= pos or outcome_mid not in disp:
            raise IntegratedStackError(
                "EXPERIMENT_INVALID__ANALYTIC_ROLE_DIVERGENCE",
                f"C query={request.get('query_id')}",
            )


def preflight_integrated_bundle(bundle: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(bundle, Mapping) or bundle.get("schema_version") != INPUT_SCHEMA_VERSION:
        raise IntegratedStackError("INTEGRATED_INPUT_SCHEMA_INVALID")
    execution_mode = bundle.get("execution_mode")
    if execution_mode not in {"SYNTHETIC_FIXTURE", "FROZEN_EMPIRICAL_CANARY"}:
        raise IntegratedStackError("INTEGRATED_EXECUTION_MODE_INVALID")
    common = harness.validate_common_manifest(bundle.get("common_manifest"))
    holdout = bundle.get("holdout_manifest")
    query_manifest = bundle.get("query_manifest")
    holdout_hash = _verified_hash(holdout, "holdout_manifest_hash", "EXPERIMENT_INVALID__HOLDOUT")
    query_hash = _verified_hash(query_manifest, "query_manifest_hash", "HARNESS_QUERY_MANIFEST_HASH_DIVERGENCE")
    if holdout.get("common_manifest_hash") != common["manifest_hash"]:
        raise IntegratedStackError("COMMON_INPUT_RISK_SET_DIVERGENCE", "holdout/common binding")
    if query_manifest.get("common_manifest_hash") != common["manifest_hash"] or query_manifest.get("holdout_manifest_hash") != holdout_hash:
        raise IntegratedStackError("COMMON_INPUT_ARM_HASH_DIVERGENCE", "query/common/holdout binding")

    arm_inputs = bundle.get("arm_inputs")
    if not isinstance(arm_inputs, Mapping) or set(arm_inputs) != set(harness.CORE):
        raise IntegratedStackError("INTEGRATED_CORE_ARM_SET_INVALID")
    for arm_id in harness.CORE:
        if not isinstance(arm_inputs[arm_id], Mapping):
            raise IntegratedStackError("INTEGRATED_ARM_INPUT_INVALID", arm_id)
        _reject_cross_arm_or_semantic_overrides(arm_inputs[arm_id], arm_id)
        _assert_common_echo(arm_id, arm_inputs[arm_id], common)
        _assert_semantic_echo_fields(arm_id, arm_inputs[arm_id], common)

    a, b, c = arm_inputs["A"], arm_inputs["B"], arm_inputs["C"]
    ids_a = _respondent_ids_from_a(a)
    ids_bp = _respondent_ids_from_b_surface(b.get("position_surface"), "position")
    ids_bd = _respondent_ids_from_b_surface(b.get("disposition_surface"), "disposition")
    ids_c = _respondent_ids_from_c(c)
    design_ids = tuple(sorted(holdout.get("design_unit_ids", ())))
    if not design_ids or not (ids_a == ids_bp == ids_bd == ids_c == design_ids):
        raise IntegratedStackError(
            "COMMON_INPUT_RISK_SET_DIVERGENCE",
            f"A={ids_a} Bp={ids_bp} Bd={ids_bd} C={ids_c} design={design_ids}",
        )
    risk_set = c.get("risk_set", {})
    if risk_set.get("risk_set_ref") != common["exposure_risk_set_ref"]:
        raise IntegratedStackError("COMMON_INPUT_RISK_SET_DIVERGENCE", "C risk_set_ref")
    estimand = c.get("estimand_design")
    if not isinstance(estimand, Mapping) or estimand.get("estimand_ref") != common["estimand_ref"] or estimand.get("weight_design_refs") != common["weight_design_refs"]:
        raise IntegratedStackError("COMMON_INPUT_ESTIMAND_DIVERGENCE")
    if c.get("analytic_role_binding_ref") != common["analytic_role_authority_refs"]:
        raise IntegratedStackError("EXPERIMENT_INVALID__ANALYTIC_ROLE_DIVERGENCE", "C analytic role binding")

    position_ids, disposition_ids = _measurement_sets(a, b)
    _assert_state_coherence(a, b, c, position_ids, disposition_ids)
    _assert_c_query_roles(c, position_ids, disposition_ids)

    registry = c["frozen_state_registry"]
    if registry.get("post_transform_state_manifest_ref") != common["post_transform_state_manifest"]:
        raise IntegratedStackError("EXPERIMENT_INVALID__POSTFORK_STATE_IDENTITY_DIVERGENCE", "registry binding")

    code_refs = bundle.get("execution_code_refs")
    if not isinstance(code_refs, Mapping) or set(code_refs) != {"stack", "A", "B", "C"} or any(not isinstance(v, str) or not v for v in code_refs.values()):
        raise IntegratedStackError("INTEGRATED_CODE_IDENTITY_BINDING_INVALID")

    citc = bundle.get("citc")
    validate_citc(citc)

    return {
        "common_manifest": common,
        "holdout_hash": holdout_hash,
        "query_hash": query_hash,
        "design_unit_ids": list(design_ids),
        "position_measurement_ids": list(position_ids),
        "disposition_measurement_ids": list(disposition_ids),
        "code_refs": dict(code_refs),
        "citc_ref": citc["citc_ref"],
        "execution_mode": execution_mode,
    }


def _bound_a_input(a: Mapping[str, Any], common: Mapping[str, Any]) -> dict[str, Any]:
    out = _clone(dict(a))
    out["common_semantic_input_manifest"] = _clone(common)
    return out


def _bound_b_input(b: Mapping[str, Any], common: Mapping[str, Any]) -> dict[str, Any]:
    out = _clone(dict(b))
    out["common_manifest"] = _clone(common)
    return out


def _run_c(c: Mapping[str, Any], common: Mapping[str, Any]) -> list[dict[str, Any]]:
    results = []
    shared = {
        "common_manifest": common,
        "frozen_state_registry": c["frozen_state_registry"],
        "risk_set": c["risk_set"],
        "respondent_measurements": c["respondent_measurements"],
        "estimand_design": c["estimand_design"],
        "analytic_role_binding_ref": c["analytic_role_binding_ref"],
    }
    for request in c["requests"]:
        kwargs = dict(shared)
        kwargs.update({
            "condition": request["condition"],
            "outcome": request["outcome"],
            "support_policy": request["support_policy"],
        })
        produced = core_c.produce_direct_conditional_redistribution(**kwargs)
        results.append({"query_id": request["query_id"], "result": produced})
    return results


def _attestation_from_output(arm_id: str, output: Mapping[str, Any]) -> Mapping[str, Any]:
    if arm_id == "A":
        return output["common_input_attestation"]
    return output["common_manifest_attestation"]


def _assert_output_attestations(common: Mapping[str, Any], outputs: Mapping[str, Any]) -> dict[str, Any]:
    hashes = {}
    for arm_id in harness.CORE:
        if arm_id == "C":
            rows = outputs["C"]
            if not rows:
                raise IntegratedStackError("INTEGRATED_ARM_C_NO_RESULTS")
            atts = [_attestation_from_output("C", row["result"]) for row in rows]
            arm_hashes = {att["recomputed_manifest_hash"] for att in atts}
            if len(arm_hashes) != 1:
                raise IntegratedStackError("COMMON_INPUT_ARM_HASH_DIVERGENCE", "C requests disagree")
            att = atts[0]
        else:
            att = _attestation_from_output(arm_id, outputs[arm_id])
        if att.get("attestation_status") != "ATTESTED_EQUAL":
            raise IntegratedStackError("COMMON_INPUT_ARM_HASH_DIVERGENCE", arm_id)
        hashes[arm_id] = att.get("recomputed_manifest_hash")
    if set(hashes.values()) != {common["manifest_hash"]}:
        raise IntegratedStackError("COMMON_INPUT_ARM_HASH_DIVERGENCE", repr(hashes))
    return {
        "schema_version": "FFX002_R2_INTEGRATED_COMMON_HASH_ATTESTATION@1",
        "expected_common_manifest_hash": common["manifest_hash"],
        "arm_recomputed_hashes": hashes,
        "status": "A_B_C_ATTEST_IDENTICAL",
    }


def _a_query_map(output: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {row["query_id"]: row for row in output.get("query_results", [])}


def _c_query_map(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {row["query_id"]: row["result"] for row in rows}


def orchestrate_common_queries(
    query_manifest: Mapping[str, Any],
    arm_outputs: Mapping[str, Any],
) -> dict[str, Any]:
    plan = harness.query_plan(query_manifest, harness.CORE)
    a_map, c_map = _a_query_map(arm_outputs["A"]), _c_query_map(arm_outputs["C"])
    qrows = {row["query_id"]: row for row in query_manifest["queries"]}
    results = []
    for route in plan["dispatch_rows"]:
        qid, arm = route["query_id"], route["arm_id"]
        if route["framework_disposition"] == "DOES_NOT_REPRESENT":
            results.append({
                "query_id": qid, "arm_id": arm, "query_status": "DOES_NOT_REPRESENT",
                "answer": None, "reason": route.get("abstention_rule"),
            })
            continue
        query = qrows[qid]
        refs = query.get("arm_query_refs", {})
        ref = refs.get(arm) if isinstance(refs, Mapping) else None
        if arm == "A" and ref in a_map:
            results.append({"query_id": qid, "arm_id": arm, "query_status": a_map[ref]["query_status"], "answer": a_map[ref]})
        elif arm == "C" and ref in c_map:
            result = c_map[ref]
            results.append({"query_id": qid, "arm_id": arm, "query_status": result["status"], "answer": result})
        elif arm == "B" and ref in {"POSITION_LOCAL_NEIGHBORHOOD", "DISPOSITION_LOCAL_NEIGHBORHOOD"}:
            side = "position_geometry" if ref.startswith("POSITION") else "disposition_geometry"
            results.append({
                "query_id": qid, "arm_id": arm, "query_status": "REPRESENTED_BY_LOCAL_GEOMETRY_OUTPUT",
                "answer": {"geometry_side": side, "output_hash": _hash(arm_outputs["B"][side])},
            })
        else:
            results.append({
                "query_id": qid, "arm_id": arm, "query_status": "ABSTAIN__NO_DECLARED_ARM_QUERY_ADAPTER",
                "answer": None, "reason": route.get("abstention_rule"),
            })
    out = {"schema_version": "FFX002_R2_INTEGRATED_QUERY_RESULTS@1", "query_plan": plan, "results": results}
    out["query_results_hash"] = _hash(out)
    return out


def _distribution_map(rows: Sequence[Mapping[str, Any]], *, state_key: str = "state_id", prob_key: str = "probability") -> dict[str, float]:
    out: dict[str, float] = {}
    for row in rows:
        sid = row.get(state_key)
        p = row.get(prob_key)
        if not isinstance(sid, str) or not isinstance(p, (int, float)) or isinstance(p, bool) or not math.isfinite(float(p)) or float(p) < 0:
            raise IntegratedStackError("SCORING_DISTRIBUTION_INVALID")
        if sid in out:
            raise IntegratedStackError("SCORING_DISTRIBUTION_DUPLICATE_STATE", sid)
        out[sid] = float(p)
    if not out:
        raise IntegratedStackError("SCORING_DISTRIBUTION_EMPTY")
    return out


def distribution_metrics(truth_rows: Sequence[Mapping[str, Any]], estimate_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    truth = _distribution_map(truth_rows)
    estimate = _distribution_map(estimate_rows)
    if set(truth) != set(estimate):
        raise IntegratedStackError("SCORING_STATE_UNIVERSE_DIVERGENCE", f"truth={sorted(truth)} estimate={sorted(estimate)}")
    tv = 0.5 * math.fsum(abs(truth[s] - estimate[s]) for s in truth)
    terms = []
    zero_mass = False
    for sid, p in truth.items():
        if p <= 0:
            continue
        q = estimate[sid]
        if q <= 0:
            zero_mass = True
            break
        terms.append(-p * math.log(q))
    return {
        "TV_DISTANCE": tv,
        "LOG_LOSS": None if zero_mass else math.fsum(terms),
        "LOG_LOSS_STATUS": "INFINITE__ZERO_PREDICTED_MASS" if zero_mass else "FINITE",
    }


def _extract_a_distribution(answer: Mapping[str, Any], output_a: Mapping[str, Any]) -> list[dict[str, Any]] | None:
    selected = answer.get("selected_attempt")
    if not isinstance(selected, Mapping):
        return None
    rows = selected.get("disposition_distribution")
    if not isinstance(rows, list):
        return None
    basis = output_a.get("method_manifest", {}).get("distribution_basis")
    prob_key = "probability_analysis_weight" if basis == "ANALYSIS_WEIGHT" else "probability_unweighted"
    out = []
    for row in rows:
        pairs = row.get("state_pairs", [])
        if len(pairs) != 1:
            return None
        out.append({"state_id": pairs[0]["state_id"], "probability": row[prob_key]})
    return out


def _extract_c_distribution(answer: Mapping[str, Any]) -> list[dict[str, Any]] | None:
    rows = answer.get("destination_distribution")
    if not isinstance(rows, list):
        return None
    return [{"state_id": row["destination_state_id"], "probability": row["probability"]} for row in rows]


def score_query_cases(
    scoring_cases: Sequence[Mapping[str, Any]],
    query_results: Mapping[str, Any],
    arm_outputs: Mapping[str, Any],
) -> list[dict[str, Any]]:
    routed = {(r["query_id"], r["arm_id"]): r for r in query_results["results"]}
    observations = []
    for case in scoring_cases:
        qid = case.get("query_id")
        truth = case.get("truth_distribution")
        if not isinstance(qid, str) or not isinstance(truth, list):
            raise IntegratedStackError("SCORING_CASE_INVALID")
        for arm in harness.CORE:
            route = routed.get((qid, arm))
            if route is None or route["query_status"] in {"DOES_NOT_REPRESENT", "ABSTAIN__NO_DECLARED_ARM_QUERY_ADAPTER"}:
                observations.append({"query_id": qid, "arm_id": arm, "metric_id": "QUERY_COVERAGE", "value": 0.0, "status": route["query_status"] if route else "NO_ROUTE"})
                continue
            answer = route.get("answer")
            estimate = _extract_a_distribution(answer, arm_outputs["A"]) if arm == "A" else _extract_c_distribution(answer) if arm == "C" else None
            observations.append({"query_id": qid, "arm_id": arm, "metric_id": "QUERY_COVERAGE", "value": 1.0, "status": route["query_status"]})
            if estimate is None:
                continue
            metrics = distribution_metrics(truth, estimate)
            observations.append({"query_id": qid, "arm_id": arm, "metric_id": "TV_DISTANCE", "value": metrics["TV_DISTANCE"], "status": "MEASURED"})
            observations.append({"query_id": qid, "arm_id": arm, "metric_id": "LOG_LOSS", "value": metrics["LOG_LOSS"], "status": metrics["LOG_LOSS_STATUS"]})
    return observations


def validate_citc(citc: Any) -> dict[str, Any]:
    if not isinstance(citc, Mapping):
        raise IntegratedStackError("CITC_BINDING_MISSING")
    ref = citc.get("citc_ref")
    rules = citc.get("rules")
    if not isinstance(ref, str) or not ref or ref.startswith("<") or not isinstance(rules, list):
        raise IntegratedStackError("CITC_BINDING_INVALID")
    for rule in rules:
        if not isinstance(rule, Mapping) or not isinstance(rule.get("metric_id"), str):
            raise IntegratedStackError("CITC_RULE_INVALID")
        if rule.get("operator") not in {"GE", "GT", "LE", "LT", "ABS_GE", "ABS_GT"}:
            raise IntegratedStackError("CITC_RULE_INVALID", f"operator={rule.get('operator')}")
        threshold = rule.get("threshold")
        if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or not math.isfinite(float(threshold)):
            raise IntegratedStackError("CITC_RULE_INVALID", "threshold must be externally supplied finite number")
        if "preferred_view" in rule or "winner" in rule:
            raise IntegratedStackError("CITC_RULE_INVALID", "preferred-view/winner rules are outside this interface")
    return _clone(dict(citc))


def _apply_operator(value: float, operator: str, threshold: float) -> bool:
    if operator == "GE": return value >= threshold
    if operator == "GT": return value > threshold
    if operator == "LE": return value <= threshold
    if operator == "LT": return value < threshold
    if operator == "ABS_GE": return abs(value) >= threshold
    if operator == "ABS_GT": return abs(value) > threshold
    raise IntegratedStackError("CITC_RULE_INVALID", operator)


def apply_citc(observations: Sequence[Mapping[str, Any]], citc: Mapping[str, Any]) -> dict[str, Any]:
    contract = validate_citc(citc)
    rules = {rule["metric_id"]: rule for rule in contract["rules"]}
    rulings = []
    for obs0 in observations:
        obs = _clone(dict(obs0))
        rule = rules.get(obs.get("metric_id"))
        value = obs.get("value")
        if rule is None or value is None:
            disposition = "NO_CITC_RULE__UNADJUDICATED" if rule is None else "NONFINITE_OR_UNAVAILABLE__UNADJUDICATED"
            material = None
        elif not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
            disposition, material = "NONFINITE_OR_UNAVAILABLE__UNADJUDICATED", None
        else:
            material = _apply_operator(float(value), rule["operator"], float(rule["threshold"]))
            disposition = "CITC_RULE_TRUE" if material else "CITC_RULE_FALSE"
        rulings.append({**obs, "citc_disposition": disposition, "materiality_rule_result": material})
    out = {
        "schema_version": SCORING_SCHEMA_VERSION,
        "citc_ref": contract["citc_ref"],
        "citc_rules_hash": _hash(contract["rules"]),
        "rulings": rulings,
        "master_score": None,
        "preferred_view": None,
        "adjudication_ceiling": "MATERIALITY_ONLY__NO_MASTER_REPRESENTATION_SELECTION",
    }
    out["scoring_hash"] = _hash(out)
    return out


def build_full_ablation_orchestration(common_hash: str, query_hash: str) -> dict[str, Any]:
    base = harness.ablation_plan(common_hash, query_hash, harness.CORE)
    packages = {row["package_id"]: row for row in base["packages"]}
    packages["SUBSTRATE"] = {"package_id": "SUBSTRATE", "views": []}
    packages["A+B"] = {"package_id": "A+B", "views": ["A", "B"]}
    targets = [
        {
            "target_view": "A",
            "weaker_baseline_package": "B+C",
            "target_added_package": "A+B+C",
            "full_admitted_package": "A+B+C",
            "target_removed_package": "B+C",
        },
        {
            "target_view": "B",
            "weaker_baseline_package": "A+C",
            "target_added_package": "A+B+C",
            "full_admitted_package": "A+B+C",
            "target_removed_package": "A+C",
        },
        {
            "target_view": "C",
            "weaker_baseline_package": "SUBSTRATE",
            "target_added_package": "C",
            "full_admitted_package": "A+B+C",
            "target_removed_package": "A+B",
        },
    ]
    out = {
        "schema_version": "FFX002_R2_FULL_ABLATION_ORCHESTRATION_PLAN@1",
        "design_ref": DESIGN_REF,
        "common_manifest_hash": common_hash,
        "query_manifest_hash": query_hash,
        "packages": [packages[k] for k in ("SUBSTRATE", "C", "A+C", "B+C", "A+B", "A+B+C")],
        "target_add_remove_rows": targets,
        "legacy_ffp009_plan_hash": base["ablation_plan_hash"],
        "query_specific_weaker_baseline_resolution": "REQUIRED_AT_SCORING_TIME",
        "materiality_source": "CITC_ONLY",
        "preferred_view": None,
        "master_score": None,
        "execution_status": "FRAMEWORK_READY__NO_GENUINE_EMPIRICAL_EXECUTION",
    }
    out["ablation_plan_hash"] = _hash(out)
    return out


def build_prev3_ablation(
    common: Mapping[str, Any],
    query_results: Mapping[str, Any],
    scoring: Mapping[str, Any],
) -> dict[str, Any]:
    by_query: dict[str, dict[str, Any]] = {}
    for row in query_results["results"]:
        by_query.setdefault(row["query_id"], {})[row["arm_id"]] = row
    packets = []
    packages = {
        "P0": ["C"],
        "P1": ["C", "A"],
        "P2": ["C", "B"],
        "P3": ["C", "A", "B"],
    }
    for qid, arm_rows in sorted(by_query.items()):
        for packet_id, arms in packages.items():
            represented = []
            abstentions = []
            for arm in arms:
                row = arm_rows.get(arm)
                if row and row["query_status"] not in {"DOES_NOT_REPRESENT", "ABSTAIN__NO_DECLARED_ARM_QUERY_ADAPTER"}:
                    represented.append({"arm_id": arm, "query_status": row["query_status"], "answer": row["answer"]})
                else:
                    abstentions.append({"arm_id": arm, "reason": row["query_status"] if row else "NO_ROUTE"})
            packets.append({
                "packet_id": packet_id,
                "query_id": qid,
                "claim_scope_ref": common["claim_scope_ref"],
                "common_semantic_input_manifest_hash": common["manifest_hash"],
                "risk_set_ref": common["exposure_risk_set_ref"],
                "estimand_ref": common["estimand_ref"],
                "represented_view_results": represented,
                "typed_absences": abstentions,
                "representation_dependence": "CITC_SCORING_ATTACHED_SEPARATELY",
                "actor_interpretation": "PROHIBITED",
            })
    out = {
        "schema_version": PREV3_SCHEMA_VERSION,
        "packets": packets,
        "scoring_hash": scoring["scoring_hash"],
        "forbidden_outputs": ["PERSONALITY", "BELIEF_ASSIGNMENT", "MOTIVE", "BIOGRAPHY", "REALIZED_V3_PERSON"],
    }
    out["prev3_ablation_hash"] = _hash(out)
    return out


def collect_receipts(
    common: Mapping[str, Any],
    holdout: Mapping[str, Any],
    query_manifest: Mapping[str, Any],
    code_refs: Mapping[str, str],
    arm_inputs: Mapping[str, Any],
    arm_outputs: Mapping[str, Any],
) -> dict[str, Any]:
    arm_receipts = {}
    for arm in harness.CORE:
        output = arm_outputs[arm]
        if arm == "A":
            replay = output["replay_receipt"]
            producer_output_hash = _hash(output)
        elif arm == "B":
            replay = output["replay_receipt"]
            producer_output_hash = _hash(output)
        else:
            replay = [row["result"]["replay_receipt"] for row in output]
            producer_output_hash = _hash(output)
        arm_receipts[arm] = {
            "code_identity_ref": code_refs[arm],
            "arm_input_hash": _hash(arm_inputs[arm]),
            "arm_output_hash": producer_output_hash,
            "producer_replay_receipt_hash": _hash(replay),
            "common_manifest_hash": common["manifest_hash"],
        }
    out = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "stack_code_identity_ref": code_refs["stack"],
        "common_manifest_hash": common["manifest_hash"],
        "holdout_manifest_hash": holdout["holdout_manifest_hash"],
        "query_manifest_hash": query_manifest["query_manifest_hash"],
        "arm_receipts": arm_receipts,
        "cross_arm_learned_output_consumption": "PROHIBITED_AND_PREFLIGHT_REJECTED",
    }
    out["receipt_collection_hash"] = _hash(out)
    return out


def build_fork_tamper_hostile_receipt(common: Mapping[str, Any]) -> dict[str, Any]:
    cases = []
    for arm in harness.CORE:
        tampered = _clone(common)
        tampered["estimand_ref"] = {"synthetic_hostile_estimand": arm}
        tampered["manifest_hash"] = harness.compute_common_hash(tampered)
        try:
            harness.reject_fork_semantic_tamper(common, tampered, arm)
        except harness.HarnessViolation as exc:
            cases.append({"arm_id": arm, "status": "PASS__REJECTED_BEFORE_EXECUTION", "failure_state": exc.state})
        else:
            raise IntegratedStackError("HOSTILE_FAIL__FORK_SEMANTIC_TAMPER_ACCEPTED", arm)
    out = {
        "hostile_id": "FORK_SEMANTIC_TAMPER__COMMON_MANIFEST_HASH_DIVERGENCE",
        "cases": cases,
        "expected_failure": "EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE",
    }
    out["hostile_receipt_hash"] = _hash(out)
    return out


def run_integrated_stack(bundle: Mapping[str, Any]) -> dict[str, Any]:
    preflight = preflight_integrated_bundle(bundle)
    common = preflight["common_manifest"]
    arm_inputs = _clone(bundle["arm_inputs"])

    # All producer calls receive the same already-frozen common manifest.
    output_a = core_a.produce_exact_configuration_set(_bound_a_input(arm_inputs["A"], common))
    output_b = core_b.compile_local_geometric_view(_bound_b_input(arm_inputs["B"], common))
    output_c = _run_c(arm_inputs["C"], common)
    outputs = {"A": output_a, "B": output_b, "C": output_c}

    common_attestation = _assert_output_attestations(common, outputs)
    query_results = orchestrate_common_queries(bundle["query_manifest"], outputs)
    hostile = harness.hostile_plan(
        common,
        bundle.get("hostile_rows", []),
        harness.CORE,
        bundle.get("hostile_variant_bindings"),
    )
    fork_tamper = build_fork_tamper_hostile_receipt(common)
    ablation = build_full_ablation_orchestration(
        common["manifest_hash"],
        bundle["query_manifest"]["query_manifest_hash"],
    )
    observations = score_query_cases(bundle.get("scoring_cases", []), query_results, outputs)
    scoring = apply_citc(observations, bundle["citc"])
    prev3 = build_prev3_ablation(common, query_results, scoring)
    receipts = collect_receipts(
        common, bundle["holdout_manifest"], bundle["query_manifest"], preflight["code_refs"], arm_inputs, outputs
    )

    result = {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "software_stack_state": TERMINAL_READY,
        "execution_mode": preflight["execution_mode"],
        "execution_state": (
            "SYNTHETIC_FIXTURE_EXECUTION_COMPLETE"
            if preflight["execution_mode"] == "SYNTHETIC_FIXTURE"
            else "FROZEN_EMPIRICAL_CANARY_EXECUTION_COMPLETE"
        ),
        "design_ref": DESIGN_REF,
        "common_hash_attestation": common_attestation,
        "arm_outputs": outputs,
        "query_results": query_results,
        "hostile_plan": hostile,
        "fork_semantic_tamper_receipt": fork_tamper,
        "ablation_plan": ablation,
        "citc_scoring": scoring,
        "prev3_ablation": prev3,
        "receipt_collection": receipts,
        "authority_minted": False,
        "genuine_empirical_execution_performed": preflight["execution_mode"] == "FROZEN_EMPIRICAL_CANARY",
        "preferred_view": None,
        "master_score": None,
    }
    result["integrated_output_hash"] = _hash(result)
    return result


OUTPUT_FILES = {
    "arm_outputs": "03_CORE_ARM_OUTPUTS.json",
    "query_results": "04_COMMON_QUERY_RESULTS.json",
    "hostile_plan": "05_HOSTILE_PLAN.json",
    "fork_semantic_tamper_receipt": "06_FORK_SEMANTIC_TAMPER_RECEIPT.json",
    "ablation_plan": "07_ABLATION_PLAN.json",
    "citc_scoring": "08_CITC_SCORING.json",
    "prev3_ablation": "09_PREV3_ABLATION.json",
    "receipt_collection": "10_REPLAY_OUTPUT_RECEIPTS.json",
}


def write_integrated_outputs(result: Mapping[str, Any], output_dir: str | Path) -> dict[str, str]:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for key, filename in OUTPUT_FILES.items():
        data = json.dumps(result[key], ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n"
        (root / filename).write_bytes(data)
        hashes[filename] = hashlib.sha256(data).hexdigest()
    summary = {k: v for k, v in result.items() if k not in OUTPUT_FILES}
    summary["artifact_hashes"] = hashes
    data = json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    (root / "00_INTEGRATED_EXECUTION_RETURN.json").write_bytes(data)
    hashes["00_INTEGRATED_EXECUTION_RETURN.json"] = hashlib.sha256(data).hexdigest()
    return hashes


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one frozen FFX002-R2 A/B/C execution stack.")
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)
    bundle = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    result = run_integrated_stack(bundle)
    write_integrated_outputs(result, args.output_dir)
    print(json.dumps({
        "software_stack_state": result["software_stack_state"],
        "execution_state": result["execution_state"],
        "common_manifest_hash": result["common_hash_attestation"]["expected_common_manifest_hash"],
        "integrated_output_hash": result["integrated_output_hash"],
        "output_dir": str(Path(args.output_dir)),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
