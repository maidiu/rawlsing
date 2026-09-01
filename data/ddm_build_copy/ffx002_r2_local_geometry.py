#!/usr/bin/env python3
"""Bounded FFX002-R2 Core-B LOCAL_GEOMETRIC producer.

Geometry is a representation-local view over already-frozen semantic state IDs.
This module never merges, rebins, reorders, relabels, re-roles, or changes the
eligible respondent/risk-set universe.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from typing import Any, Iterable, Mapping, Sequence

try:
    from data.ddm_build_copy.field_forge_ffx002_harness import HarnessViolation as _HarnessViolation, compute_common_hash as _shared_common_hash
except ModuleNotFoundError:  # direct script execution
    from field_forge_ffx002_harness import HarnessViolation as _HarnessViolation, compute_common_hash as _shared_common_hash

PRODUCER_SCHEMA_VERSION = "FFX002_R2_LOCAL_GEOMETRIC_OUTPUT_R1"
METHOD_SCHEMA_VERSION = "FFX002_R2_LOCAL_GEOMETRIC_METHOD_R1"
NUMERIC_REPLAY_VERSION = "FFX002_R2_LOCAL_GEOMETRIC_NUMERIC_REPLAY_R1"
CANONICALIZATION_VERSION = "FFX002_R2_COMMON_CANONICAL_JSON_SHA256_R1"

POSITION_ROLE = "ACTIVE_POSITION"
DISPOSITION_ROLE = "ACTIVE_DISPOSITION"
ARM_ID = "B"
VIEW_FAMILY = "LOCAL_GEOMETRIC"

_FORBIDDEN_METHOD_KEY_FRAGMENTS = (
    "merge",
    "collapse",
    "rebin",
    "recode",
    "reorder",
    "state_map",
    "state_mapping",
    "role_override",
    "rerole",
    "re_role",
    "eligibility_filter",
    "risk_set_filter",
    "estimand_override",
    "semantic_transform",
    "category_pool",
    "special_state_pool",
)

_REQUIRED_COMMON_FIELDS = {
    "manifest_schema_version",
    "current_execution_sha",
    "observation_substrate_ref",
    "respondent_entity_binding_ref",
    "exposure_risk_set_ref",
    "source_scope_ref",
    "source_native_measurement_refs",
    "qimpl_measurement_binding_refs",
    "response_state_semantics_ref",
    "special_state_semantics_ref",
    "ttar_execution_sequence",
    "post_transform_state_manifest",
    "claim_scope_ref",
    "estimand_ref",
    "weight_design_refs",
    "analytic_role_authority_refs",
    "ancestry_disjointness_receipt",
    "unresolved_noncomparable_manifest",
    "source_native_ancestry_ref",
    "loss_profile",
    "holdout_generation_inputs_hash",
    "canonicalization_spec",
    "manifest_hash",
}


class LocalGeometryContractError(RuntimeError):
    """Fail-closed Core-B contract violation."""


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _parse_set_paths(spec: Any) -> set[tuple[str, ...]]:
    if not isinstance(spec, Mapping):
        return set()
    raw = spec.get("set_array_paths", [])
    if raw in (None, []):
        return set()
    if not isinstance(raw, list) or not all(isinstance(x, str) and x for x in raw):
        raise LocalGeometryContractError("canonicalization_spec.set_array_paths must be a list of dotted paths")
    return {tuple(x.split(".")) for x in raw}


def _normalize_manifest_value(value: Any, path: tuple[str, ...], set_paths: set[tuple[str, ...]]) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _normalize_manifest_value(v, path + (str(k),), set_paths) for k, v in value.items()}
    if isinstance(value, list):
        items = [_normalize_manifest_value(v, path + ("[]",), set_paths) for v in value]
        if path in set_paths:
            return sorted(items, key=lambda x: _canonical_json_bytes(x))
        return items
    return value


def compute_common_manifest_hash(common_manifest: Mapping[str, Any]) -> str:
    """Recompute only through the FFP009 frozen canonicalization contract."""
    try:
        return _shared_common_hash(common_manifest)
    except _HarnessViolation as exc:
        raise LocalGeometryContractError(f"{exc.state}: {exc.detail}") from exc


def attest_common_manifest(common_manifest: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(common_manifest, Mapping):
        raise LocalGeometryContractError("common_manifest must be an object")
    missing = sorted(_REQUIRED_COMMON_FIELDS - set(common_manifest))
    if missing:
        raise LocalGeometryContractError(f"COMMON_INPUT_MISSING_HARD_FIELD: {missing}")
    received = common_manifest.get("manifest_hash")
    if not isinstance(received, str) or len(received) != 64:
        raise LocalGeometryContractError("common_manifest.manifest_hash must be a 64-character SHA-256 hex digest")
    recomputed = compute_common_manifest_hash(common_manifest)
    if received.lower() != recomputed:
        raise LocalGeometryContractError(
            "COMMON_INPUT_ARM_HASH_DIVERGENCE: received common manifest hash does not match independent recomputation"
        )
    return {
        "arm_id": ARM_ID,
        "received_manifest_hash": received.lower(),
        "recomputed_manifest_hash": recomputed,
        "attestation_status": "ATTESTED_EQUAL",
    }


def _walk_method_keys(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            p = path + (str(key),)
            yield p, child
            yield from _walk_method_keys(child, p)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from _walk_method_keys(child, path + (str(idx),))


def validate_method_manifest(method: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(method, Mapping):
        raise LocalGeometryContractError("method_manifest must be an object")
    if method.get("schema_version") != METHOD_SCHEMA_VERSION:
        raise LocalGeometryContractError(f"method_manifest.schema_version must equal {METHOD_SCHEMA_VERSION}")

    for path, _ in _walk_method_keys(method):
        leaf = path[-1].lower()
        if any(fragment in leaf for fragment in _FORBIDDEN_METHOD_KEY_FRAGMENTS):
            raise LocalGeometryContractError(
                f"FORBIDDEN_UNDECLARED_SEMANTIC_TRANSFORM: method key {'.'.join(path)} is not representation-local"
            )

    preprocessing = method.get("preprocessing", [])
    if not isinstance(preprocessing, list):
        raise LocalGeometryContractError("method_manifest.preprocessing must be a list")
    for item in preprocessing:
        if not isinstance(item, Mapping):
            raise LocalGeometryContractError("each preprocessing inventory row must be an object")
        classification = item.get("classification")
        executed_postfork = bool(item.get("executed_postfork", True))
        if classification == "IDENTITY_PRESERVING_METHOD":
            continue
        if classification == "AUTHORIZED_PREFORK_TRANSFORM_ALREADY_IN_MANIFEST" and not executed_postfork:
            continue
        raise LocalGeometryContractError(
            "FORBIDDEN_UNDECLARED_SEMANTIC_TRANSFORM: post-fork preprocessing may not change frozen semantics"
        )

    metric = method.get("metric")
    if not isinstance(metric, Mapping):
        raise LocalGeometryContractError("method_manifest.metric must be an object")
    metric_family = metric.get("family")
    if metric_family not in {"EXACT_STATE_HAMMING_R1", "EXACT_STATE_WEIGHTED_HAMMING_R1"}:
        raise LocalGeometryContractError("unsupported metric family")
    if metric.get("state_comparison") != "EXACT_FROZEN_STATE_IDENTITY_ONLY":
        raise LocalGeometryContractError("metric must compare exact frozen state identity only")
    weights = metric.get("measurement_weights")
    if metric_family == "EXACT_STATE_WEIGHTED_HAMMING_R1":
        if not isinstance(weights, Mapping) or not weights:
            raise LocalGeometryContractError("weighted Hamming requires measurement_weights")
        for key, val in weights.items():
            if not isinstance(key, str) or not isinstance(val, (int, float)) or isinstance(val, bool) or val <= 0:
                raise LocalGeometryContractError("measurement_weights must map measurement IDs to positive numbers")
    elif weights not in (None, {}):
        raise LocalGeometryContractError("unweighted Hamming may not declare measurement_weights")

    decomposition = method.get("decomposition")
    if not isinstance(decomposition, Mapping) or decomposition.get("family") != "CLASSICAL_MDS_JACOBI_R1":
        raise LocalGeometryContractError("decomposition.family must be CLASSICAL_MDS_JACOBI_R1")
    if decomposition.get("axis_labels", "NUMERIC_IDS_ONLY") != "NUMERIC_IDS_ONLY":
        raise LocalGeometryContractError("axis interpretation is forbidden; only numeric dimension IDs are allowed")

    dimensionality = method.get("dimensionality")
    if not isinstance(dimensionality, Mapping):
        raise LocalGeometryContractError("method_manifest.dimensionality must be an object")
    rule = dimensionality.get("rule")
    if rule == "FIXED_R1":
        d = dimensionality.get("retained_d")
        if not isinstance(d, int) or isinstance(d, bool) or not (1 <= d <= 10):
            raise LocalGeometryContractError("FIXED_R1 retained_d must be an integer in [1,10]")
    elif rule != "FULL_POSITIVE_RANK_R1":
        raise LocalGeometryContractError("unsupported dimensionality rule")

    neighborhood = method.get("neighborhood")
    if not isinstance(neighborhood, Mapping):
        raise LocalGeometryContractError("method_manifest.neighborhood must be an object")
    k = neighborhood.get("k")
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise LocalGeometryContractError("neighborhood.k must be a positive integer")

    compression = method.get("compression", {})
    if not isinstance(compression, Mapping):
        raise LocalGeometryContractError("method_manifest.compression must be an object")
    digits = compression.get("float_digits", 12)
    if not isinstance(digits, int) or not (6 <= digits <= 15):
        raise LocalGeometryContractError("compression.float_digits must be an integer in [6,15]")

    return copy.deepcopy(dict(method))


def _surface_semantic_projection(surface: Mapping[str, Any]) -> dict[str, Any]:
    projected = []
    for m in surface["measurements"]:
        projected.append(
            {
                "measurement_id": m["measurement_id"],
                "analytic_role": m["analytic_role"],
                "state_ids": list(m["state_ids"]),
                "ancestry_ids": list(m["ancestry_ids"]),
                "component_id": m.get("component_id", "C0"),
            }
        )
    return {
        "side": surface["side"],
        "measurements": sorted(projected, key=lambda x: x["measurement_id"]),
        "respondent_ids": sorted(row["respondent_id"] for row in surface["rows"]),
        "states": sorted(
            (
                row["respondent_id"],
                measurement_id,
                state_id,
            )
            for row in surface["rows"]
            for measurement_id, state_id in row["state_by_measurement"].items()
        ),
    }


def _validate_surface(surface: Mapping[str, Any], *, side: str, required_role: str) -> dict[str, Any]:
    if not isinstance(surface, Mapping):
        raise LocalGeometryContractError(f"{side}_surface must be an object")
    if surface.get("side") != side:
        raise LocalGeometryContractError(f"{side}_surface.side must equal {side}")
    measurements = surface.get("measurements")
    rows = surface.get("rows")
    if not isinstance(measurements, list) or not measurements:
        raise LocalGeometryContractError(f"{side}_surface.measurements must be a non-empty list")
    if not isinstance(rows, list) or len(rows) < 2:
        raise LocalGeometryContractError(f"{side}_surface.rows must contain at least two respondents")

    measurement_ids: list[str] = []
    allowed_states: dict[str, set[str]] = {}
    components: dict[str, list[str]] = {}
    ancestry_by_measurement: dict[str, set[str]] = {}
    for m in measurements:
        if not isinstance(m, Mapping):
            raise LocalGeometryContractError("measurement rows must be objects")
        mid = m.get("measurement_id")
        if not isinstance(mid, str) or not mid:
            raise LocalGeometryContractError("measurement_id must be a non-empty opaque string")
        if mid in allowed_states:
            raise LocalGeometryContractError(f"duplicate measurement_id {mid}")
        if m.get("analytic_role") != required_role:
            raise LocalGeometryContractError(
                f"ROLE_RECLASSIFICATION forbidden: {mid} must retain frozen role {required_role}"
            )
        states = m.get("state_ids")
        if not isinstance(states, list) or not states or not all(isinstance(x, str) and x for x in states):
            raise LocalGeometryContractError(f"{mid}.state_ids must be a non-empty list of opaque state IDs")
        if len(states) != len(set(states)):
            raise LocalGeometryContractError(f"{mid}.state_ids contains duplicate semantic states")
        ancestry = m.get("ancestry_ids")
        if not isinstance(ancestry, list) or not ancestry or not all(isinstance(x, str) and x for x in ancestry):
            raise LocalGeometryContractError(f"{mid}.ancestry_ids must be a non-empty list")
        component_id = m.get("component_id", "C0")
        if not isinstance(component_id, str) or not component_id:
            raise LocalGeometryContractError(f"{mid}.component_id must be a non-empty string")
        measurement_ids.append(mid)
        allowed_states[mid] = set(states)
        ancestry_by_measurement[mid] = set(ancestry)
        components.setdefault(component_id, []).append(mid)

    expected_measurements = set(measurement_ids)
    respondent_ids: list[str] = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise LocalGeometryContractError("surface rows must be objects")
        rid = row.get("respondent_id")
        states = row.get("state_by_measurement")
        if not isinstance(rid, str) or not rid:
            raise LocalGeometryContractError("respondent_id must be a non-empty opaque string")
        if not isinstance(states, Mapping):
            raise LocalGeometryContractError(f"{rid}.state_by_measurement must be an object")
        if set(states) != expected_measurements:
            raise LocalGeometryContractError(
                f"risk-set/coexposure mutation forbidden: respondent {rid} must carry exactly the frozen measurement set"
            )
        for mid, sid in states.items():
            if not isinstance(sid, str) or sid not in allowed_states[mid]:
                raise LocalGeometryContractError(
                    f"semantic state mutation forbidden: {rid}/{mid} state {sid!r} is not in the frozen state manifest"
                )
        respondent_ids.append(rid)
    if len(respondent_ids) != len(set(respondent_ids)):
        raise LocalGeometryContractError("empirical unit collision: duplicate respondent_id")

    clean = copy.deepcopy(dict(surface))
    clean["_components"] = {k: sorted(v) for k, v in sorted(components.items())}
    clean["_ancestry"] = ancestry_by_measurement
    clean["_semantic_hash"] = _sha256(_surface_semantic_projection(surface))
    return clean


def _measurement_weights(method: Mapping[str, Any], mids: Sequence[str]) -> list[float]:
    metric = method["metric"]
    if metric["family"] == "EXACT_STATE_HAMMING_R1":
        return [1.0] * len(mids)
    source = metric["measurement_weights"]
    missing = [mid for mid in mids if mid not in source]
    if missing:
        raise LocalGeometryContractError(f"measurement_weights missing IDs: {missing}")
    return [float(source[mid]) for mid in mids]


def _pair_distance(row_a: Mapping[str, str], row_b: Mapping[str, str], mids: Sequence[str], weights: Sequence[float]) -> float:
    denom = sum(weights)
    if denom <= 0:
        raise LocalGeometryContractError("metric has zero total weight")
    return sum(w for mid, w in zip(mids, weights) if row_a[mid] != row_b[mid]) / denom


def _distance_matrix(rows: Sequence[Mapping[str, Any]], mids: Sequence[str], weights: Sequence[float]) -> list[list[float]]:
    n = len(rows)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        a = rows[i]["state_by_measurement"]
        for j in range(i + 1, n):
            d = _pair_distance(a, rows[j]["state_by_measurement"], mids, weights)
            out[i][j] = d
            out[j][i] = d
    return out


def _identity(n: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def _jacobi_eigh(matrix: Sequence[Sequence[float]], *, tol: float = 1e-14, max_sweeps: int = 100) -> tuple[list[float], list[list[float]]]:
    """Deterministic Jacobi eigen-decomposition for small symmetric matrices."""
    n = len(matrix)
    a = [list(map(float, row)) for row in matrix]
    v = _identity(n)
    if n == 0:
        return [], []
    for _ in range(max_sweeps * max(1, n * n)):
        p = q = 0
        largest = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                x = abs(a[i][j])
                if x > largest + 0.0:
                    largest = x
                    p, q = i, j
        if largest <= tol:
            break
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        phi = 0.5 * math.atan2(2.0 * apq, aqq - app)
        c, s = math.cos(phi), math.sin(phi)

        for k in range(n):
            if k in (p, q):
                continue
            aik, akq = a[k][p], a[k][q]
            a[k][p] = a[p][k] = c * aik - s * akq
            a[k][q] = a[q][k] = s * aik + c * akq

        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = a[q][p] = 0.0

        for k in range(n):
            vip, viq = v[k][p], v[k][q]
            v[k][p] = c * vip - s * viq
            v[k][q] = s * vip + c * viq
    else:
        raise LocalGeometryContractError("numeric decomposition did not converge under deterministic Jacobi contract")

    eigenvalues = [a[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: (-eigenvalues[i], i))
    vals = [eigenvalues[i] for i in order]
    vecs = [[v[r][i] for i in order] for r in range(n)]

    for col in range(n):
        pivot = max(range(n), key=lambda r: (abs(vecs[r][col]), -r))
        if vecs[pivot][col] < 0:
            for r in range(n):
                vecs[r][col] *= -1.0
    return vals, vecs


def _classical_mds(distance: Sequence[Sequence[float]], retained_d: int | None) -> tuple[list[list[float]], list[float], int]:
    n = len(distance)
    d2 = [[distance[i][j] ** 2 for j in range(n)] for i in range(n)]
    row_mean = [sum(row) / n for row in d2]
    grand = sum(row_mean) / n
    gram = [[-0.5 * (d2[i][j] - row_mean[i] - row_mean[j] + grand) for j in range(n)] for i in range(n)]
    vals, vecs = _jacobi_eigh(gram)
    eps = 1e-12
    positive = [i for i, value in enumerate(vals) if value > eps]
    if retained_d is None:
        d = min(10, len(positive))
    else:
        d = retained_d
    coords = [[0.0] * d for _ in range(n)]
    for out_col in range(d):
        if out_col >= len(positive):
            continue
        col = positive[out_col]
        scale = math.sqrt(max(vals[col], 0.0))
        for r in range(n):
            coords[r][out_col] = vecs[r][col] * scale
    return coords, vals, len(positive)


def _euclidean(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _embedded_distances(coords: Sequence[Sequence[float]]) -> list[list[float]]:
    n = len(coords)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = _euclidean(coords[i], coords[j])
            out[i][j] = out[j][i] = d
    return out


def _stress(original: Sequence[Sequence[float]], embedded: Sequence[Sequence[float]]) -> float:
    num = den = 0.0
    n = len(original)
    for i in range(n):
        for j in range(i + 1, n):
            num += (original[i][j] - embedded[i][j]) ** 2
            den += original[i][j] ** 2
    return math.sqrt(num / den) if den > 0 else 0.0


def _ranks(values: Sequence[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: (values[i], i))
    out = [0.0] * len(values)
    pos = 0
    while pos < len(order):
        end = pos + 1
        while end < len(order) and values[order[end]] == values[order[pos]]:
            end += 1
        avg = (pos + 1 + end) / 2.0
        for k in range(pos, end):
            out[order[k]] = avg
        pos = end
    return out


def _spearman(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys) or not xs:
        return 1.0
    rx, ry = _ranks(xs), _ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    if dx == 0 or dy == 0:
        return 1.0 if all(abs(a - b) <= 1e-15 for a, b in zip(xs, ys)) else 0.0
    return num / (dx * dy)


def _upper_triangle(matrix: Sequence[Sequence[float]]) -> list[float]:
    return [matrix[i][j] for i in range(len(matrix)) for j in range(i + 1, len(matrix))]


def _round_number(value: float, digits: int) -> float:
    if abs(value) < 10 ** (-(digits + 1)):
        value = 0.0
    return round(float(value), digits)


def _round_matrix(matrix: Sequence[Sequence[float]], digits: int) -> list[list[float]]:
    return [[_round_number(v, digits) for v in row] for row in matrix]


def _neighborhood_output(respondent_ids: Sequence[str], distance: Sequence[Sequence[float]], k: int, digits: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    neighborhoods: list[dict[str, Any]] = []
    orders: list[dict[str, Any]] = []
    oppositions: list[dict[str, Any]] = []
    n = len(respondent_ids)
    k_eff = min(k, n - 1)
    for i, rid in enumerate(respondent_ids):
        ranked = sorted(
            ((distance[i][j], respondent_ids[j]) for j in range(n) if j != i),
            key=lambda x: (x[0], x[1]),
        )
        neighborhoods.append(
            {
                "respondent_id": rid,
                "k_effective": k_eff,
                "neighbors": [
                    {"respondent_id": peer, "distance": _round_number(dist, digits)}
                    for dist, peer in ranked[:k_eff]
                ],
            }
        )
        orders.append(
            {
                "respondent_id": rid,
                "distance_order": [
                    {"rank": rank, "respondent_id": peer, "distance": _round_number(dist, digits)}
                    for rank, (dist, peer) in enumerate(ranked, start=1)
                ],
            }
        )
        max_d = max((dist for dist, _ in ranked), default=0.0)
        farthest = sorted(peer for dist, peer in ranked if abs(dist - max_d) <= 1e-15)
        oppositions.append(
            {
                "respondent_id": rid,
                "max_distance": _round_number(max_d, digits),
                "opposite_peer_ids": farthest,
                "interpretation": "METRIC_OPPOSITION_ONLY__NO_SOCIAL_ONTOLOGY",
            }
        )
    return neighborhoods, orders, oppositions


def _jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def _jackknife_neighborhood_stability(respondent_ids: Sequence[str], distance: Sequence[Sequence[float]], k: int, digits: int) -> dict[str, Any]:
    n = len(respondent_ids)
    if n <= 2:
        return {
            "method": "DETERMINISTIC_LEAVE_ONE_RESPONDENT_OUT_R1",
            "replicate_count": 0,
            "median_jaccard": 1.0,
            "p10_jaccard": 1.0,
            "status": "INSUFFICIENT_N_FOR_NONTRIVIAL_JACKKNIFE",
        }
    baseline: dict[str, list[str]] = {}
    k0 = min(k, n - 1)
    for i, rid in enumerate(respondent_ids):
        ranked = sorted(
            ((distance[i][j], respondent_ids[j]) for j in range(n) if i != j),
            key=lambda x: (x[0], x[1]),
        )
        baseline[rid] = [peer for _, peer in ranked[:k0]]

    scores: list[float] = []
    for held in respondent_ids:
        keep = [rid for rid in respondent_ids if rid != held]
        index = {rid: i for i, rid in enumerate(respondent_ids)}
        k1 = min(k, len(keep) - 1)
        for rid in keep:
            i = index[rid]
            ranked = sorted(
                ((distance[i][index[peer]], peer) for peer in keep if peer != rid),
                key=lambda x: (x[0], x[1]),
            )
            new = {peer for _, peer in ranked[:k1]}
            old = [peer for peer in baseline[rid] if peer != held][:k1]
            scores.append(_jaccard(set(old), new))
    scores.sort()
    if not scores:
        median = p10 = 1.0
    else:
        median = scores[len(scores) // 2]
        p10 = scores[max(0, math.ceil(0.10 * len(scores)) - 1)]
    return {
        "method": "DETERMINISTIC_LEAVE_ONE_RESPONDENT_OUT_R1",
        "replicate_count": n,
        "comparison_count": len(scores),
        "median_jaccard": _round_number(median, digits),
        "p10_jaccard": _round_number(p10, digits),
        "status": "DIAGNOSTIC_ONLY__THRESHOLDS_PREDECLARED_BY_EXECUTION_COURT",
    }


def _build_component(surface: Mapping[str, Any], component_id: str, mids: Sequence[str], method: Mapping[str, Any]) -> dict[str, Any]:
    rows = sorted(surface["rows"], key=lambda r: r["respondent_id"])
    respondent_ids = [r["respondent_id"] for r in rows]
    weights = _measurement_weights(method, mids)
    distance = _distance_matrix(rows, mids, weights)
    dimensionality = method["dimensionality"]
    requested_d = dimensionality.get("retained_d") if dimensionality["rule"] == "FIXED_R1" else None
    coords, eigenvalues, positive_rank = _classical_mds(distance, requested_d)
    retained_d = len(coords[0]) if coords else 0
    embedded = _embedded_distances(coords)
    digits = int(method.get("compression", {}).get("float_digits", 12))
    neighborhoods, orders, oppositions = _neighborhood_output(
        respondent_ids, distance, int(method["neighborhood"]["k"]), digits
    )

    dimension_sensitivity = []
    for d in sorted({max(1, retained_d - 1), max(1, retained_d), min(10, max(1, retained_d + 1))}):
        alt_coords, _, _ = _classical_mds(distance, d)
        alt_embedded = _embedded_distances(alt_coords)
        dimension_sensitivity.append(
            {
                "retained_d": d,
                "metric_to_embedding_spearman": _round_number(
                    _spearman(_upper_triangle(distance), _upper_triangle(alt_embedded)), digits
                ),
                "normalized_stress": _round_number(_stress(distance, alt_embedded), digits),
            }
        )

    return {
        "component_id": component_id,
        "measurement_ids": list(mids),
        "respondent_ids": respondent_ids,
        "metric": {
            "family": method["metric"]["family"],
            "distance_matrix": _round_matrix(distance, digits),
        },
        "decomposition": {
            "family": method["decomposition"]["family"],
            "dimension_ids": [f"D{i}" for i in range(1, retained_d + 1)],
            "retained_d": retained_d,
            "positive_algebraic_rank": positive_rank,
            "eigenvalues": [_round_number(v, digits) for v in eigenvalues[: max(retained_d, 1)]],
            "respondent_coordinates": [
                {
                    "respondent_id": rid,
                    "coordinates": [_round_number(v, digits) for v in coord],
                }
                for rid, coord in zip(respondent_ids, coords)
            ],
            "axis_interpretation": "PROHIBITED__NUMERIC_DIMENSION_IDS_ONLY",
        },
        "local_neighborhoods": neighborhoods,
        "local_orders": orders,
        "local_oppositions": oppositions,
        "compression": {
            "normalized_stress": _round_number(_stress(distance, embedded), digits),
            "source_measurement_count": len(mids),
            "retained_dimension_count": retained_d,
            "semantic_state_deletion_count": 0,
            "semantic_state_merge_count": 0,
        },
        "stability": {
            "neighborhood_jackknife": _jackknife_neighborhood_stability(
                respondent_ids, distance, int(method["neighborhood"]["k"]), digits
            ),
            "dimensionality_sensitivity": dimension_sensitivity,
            "direct_metric_replay": "DETERMINISTIC_EXACT_FROM_FROZEN_STATE_IDS",
        },
    }


def _build_surface(surface: Mapping[str, Any], method: Mapping[str, Any]) -> dict[str, Any]:
    components = [
        _build_component(surface, component_id, mids, method)
        for component_id, mids in surface["_components"].items()
    ]
    role = POSITION_ROLE if surface["side"] == "position" else DISPOSITION_ROLE
    return {
        "side": surface["side"],
        "authorized_active_role": role,
        "surface_semantic_hash": surface["_semantic_hash"],
        "component_count": len(components),
        "components": components,
        "cross_component_metric": "DOES_NOT_REPRESENT" if len(components) > 1 else "NOT_APPLICABLE_SINGLE_COMPONENT",
    }


def _loss_receipt(position: Mapping[str, Any], disposition: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "receipt_schema_version": "FFX002_R2_LOCAL_GEOMETRIC_INVARIANT_LOSS_R1",
        "semantic_mutation_count": 0,
        "state_universe_preservation": "EXACT_HASH_BOUND",
        "analytic_role_preservation": "EXACT_VALIDATED",
        "risk_set_preservation": "EXACT_RESPONDENT_SET_VALIDATED",
        "ancestry_disjointness": "EXACT_VALIDATED",
        "invariants": {
            "I01_empirical_unit_identity": "PRESERVED_BY_EXACT_RESPONDENT_SET_VALIDATION",
            "I02_risk_set_integrity": "PRESERVED_BY_NO_POSTFORK_FILTERING",
            "I03_source_native_measurement_identity": "PRESERVED_BY_OPAQUE_MEASUREMENT_AND_ANCESTRY_IDS",
            "I04_exact_same_unit_cooccurrence": "PRESERVED_APPROXIMATELY_IN_DISTANCE_VIEW__SOURCE_FACTS_NOT_DELETED",
            "I05_minority_branch_preservation": "NOT_GUARANTEED_BY_GEOMETRY__LOSS_EXPLICIT__SOURCE_STATES_RETAINED",
            "I06_higher_order_configuration": "NOT_GUARANTEED_BY_GEOMETRY__LOSS_EXPLICIT",
            "I08_rank_order": "PRESERVED_ONLY_AS_METRIC_DISTANCE_ORDER__NO_SOURCE_ORDINAL_REINTERPRETATION",
            "I09_neighborhood": "PRESERVED_BY_CONSTRUCTION_WITH_STABILITY_DIAGNOSTIC",
            "I10_opposition": "PRESERVED_AS_METRIC_OPPOSITION_ONLY",
            "I11_topology_connectivity": "NO_FORCED_BRIDGE_ACROSS_DECLARED_COMPONENTS",
            "I12_multimodality": "MAY_DESTROY__LOSS_EXPLICIT",
            "I13_contradiction_nonmodal_alternatives": "MAY_DESTROY__LOSS_EXPLICIT",
            "I14_source_instrument_topology": "NOT_PROMOTED_TO_SOCIAL_FACT",
            "I15_uncertainty_support": "DIAGNOSTIC_SUPPORT_ONLY__NO_UNCERTAINTY_INFERENCE_MINTED",
            "I16_estimand_fidelity": "COMMON_MANIFEST_BOUND__NO_ESTIMAND_SWITCH",
            "I17_cross_context_transportable_signature_components": "DOES_NOT_ASSERT",
            "I18_semantic_manifest_identity": "PRESERVED_BY_INDEPENDENT_HASH_ATTESTATION",
        },
        "known_losses": [
            "LOW_DIMENSIONAL_COORDINATES_MAY_DISTORT_EXACT_PAIRWISE_METRIC",
            "K_NEIGHBORHOOD_OUTPUT_TRUNCATES_FULL_DISTANCE_ORDER_FOR_LOCAL_RETRIEVAL",
            "GEOMETRY_DOES_NOT_PRESERVE_EXACT_HIGHER_ORDER_CONFIGURATION_AS_A_QUERY_PRIMITIVE",
            "GEOMETRY_DOES_NOT_CREATE_OR_ASSERT_SOCIAL_ONTOLOGY",
        ],
        "source_state_hashes": {
            "position": position["_semantic_hash"],
            "disposition": disposition["_semantic_hash"],
        },
    }


def compile_local_geometric_view(payload: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise LocalGeometryContractError("input payload must be an object")
    common_manifest = payload.get("common_manifest")
    method = validate_method_manifest(payload.get("method_manifest"))
    attestation = attest_common_manifest(common_manifest)
    position = _validate_surface(payload.get("position_surface"), side="position", required_role=POSITION_ROLE)
    disposition = _validate_surface(payload.get("disposition_surface"), side="disposition", required_role=DISPOSITION_ROLE)

    position_ids = {row["respondent_id"] for row in position["rows"]}
    disposition_ids = {row["respondent_id"] for row in disposition["rows"]}
    if position_ids != disposition_ids:
        raise LocalGeometryContractError(
            "COMMON_INPUT_RISK_SET_DIVERGENCE: position and disposition respondent sets must be identical"
        )

    position_ancestry = set().union(*position["_ancestry"].values())
    disposition_ancestry = set().union(*disposition["_ancestry"].values())
    overlap = sorted(position_ancestry & disposition_ancestry)
    if overlap:
        raise LocalGeometryContractError(
            f"ANCESTRY_CONTAMINATED__BLOCK_CROSS_SPACE_CLAIM: active position/disposition ancestry overlaps: {overlap}"
        )

    if method["metric"]["family"] == "EXACT_STATE_WEIGHTED_HAMMING_R1":
        declared = set(method["metric"]["measurement_weights"])
        all_mids = {m["measurement_id"] for m in position["measurements"]} | {
            m["measurement_id"] for m in disposition["measurements"]
        }
        if declared != all_mids:
            raise LocalGeometryContractError(
                "weighted metric must declare exactly one positive weight for every active measurement across both surfaces"
            )

    state_universe_hash = _sha256(
        {
            "position": _surface_semantic_projection(position),
            "disposition": _surface_semantic_projection(disposition),
        }
    )
    method_hash = _sha256(method)
    core = {
        "producer_schema_version": PRODUCER_SCHEMA_VERSION,
        "arm_id": ARM_ID,
        "view_family": VIEW_FAMILY,
        "claim_ceiling": "LOCAL_GEOMETRIC_RELATIONS_ONLY__NO_EMPIRICAL_WORLD_OR_SOCIAL_ONTOLOGY",
        "common_manifest_attestation": attestation,
        "frozen_input_attestation": {
            "state_universe_hash": state_universe_hash,
            "position_surface_hash": position["_semantic_hash"],
            "disposition_surface_hash": disposition["_semantic_hash"],
            "respondent_set_hash": _sha256(sorted(position_ids)),
            "position_disposition_ancestry_disjoint": True,
            "semantic_mutation_allowed": False,
        },
        "method_manifest": method,
        "method_manifest_hash": method_hash,
        "position_geometry": _build_surface(position, method),
        "disposition_geometry": _build_surface(disposition, method),
        "position_disposition_dependence_profile": "NOT_PRODUCED_BY_CORE_B_R1__SPACES_NOT_REOPTIMIZED_FOR_CORRESPONDENCE",
        "invariant_loss_receipt": _loss_receipt(position, disposition),
        "allowed_claims": [
            "LOCAL_NEIGHBORHOOD",
            "METRIC_DISTANCE_ORDER",
            "METRIC_OPPOSITION",
            "LOW_DIMENSIONAL_COMPRESSION",
            "METHOD_AND_RESAMPLE_STABILITY_DIAGNOSTIC",
        ],
        "forbidden_claims": [
            "GLOBAL_WORLD_SPACE",
            "SOCIAL_ONTOLOGY",
            "CLASS_FIELD_CAPITAL_HEGEMONY",
            "HOMOLOGY",
            "CAUSAL_MECHANISM",
            "ACTOR_PSYCHOLOGY",
            "REALIZED_V3_PERSONALITY",
            "CROSS_CONTEXT_RECURRENCE",
        ],
    }
    output_payload_hash = _sha256(core)
    core["replay_receipt"] = {
        "receipt_schema_version": NUMERIC_REPLAY_VERSION,
        "common_manifest_hash": attestation["recomputed_manifest_hash"],
        "state_universe_hash": state_universe_hash,
        "method_manifest_hash": method_hash,
        "output_payload_hash": output_payload_hash,
        "deterministic_operation_inventory": [
            "UTF8_SORTED_KEY_JSON_SHA256_MANIFEST_ATTESTATION",
            "EXACT_OPAQUE_STATE_ID_EQUALITY",
            "NORMALIZED_HAMMING_PAIR_DISTANCE",
            "DETERMINISTIC_JACOBI_CLASSICAL_MDS",
            "CANONICAL_EIGENVECTOR_SIGN",
            "RESPONDENT_ID_TIE_BREAK",
            "DETERMINISTIC_LEAVE_ONE_OUT_NEIGHBORHOOD_STABILITY",
        ],
        "numeric_comparison_contract": {
            "version": NUMERIC_REPLAY_VERSION,
            "serialized_float_digits": int(method.get("compression", {}).get("float_digits", 12)),
            "absolute_tolerance": 1e-10,
            "relative_tolerance": 1e-10,
            "coordinate_rule": "COMPARE_CANONICALIZED_COORDINATES_WHEN_EIGENVALUES_NONDEGENERATE",
            "degenerate_eigenspace_rule": "COMPARE_PAIRWISE_EMBEDDED_DISTANCE_OR_GRAM_INVARIANTS_WITH_DECLARED_TOLERANCE",
            "non_numeric_artifacts": "BYTE_IDENTICAL_CANONICAL_JSON_REQUIRED",
        },
    }
    return core
