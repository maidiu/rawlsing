"""FFP023 Core-B exact-profile quotient classical MDS implementation.

This is a versioned representation-local method variant.  It does not replace
FFP011's historical CLASSICAL_MDS_JACOBI_R1 implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any, Mapping, Sequence

import numpy as np
from scipy import linalg

METHOD_FAMILY = "CLASSICAL_MDS_EXACT_PROFILE_QUOTIENT_SYMMETRIC_EIGEN_R1"
ABS_TOL = 1e-10
REL_TOL = 1e-10
POSITIVE_EIGEN_EPS = 1e-12
EIGH_DRIVER = "evr"

class ExactQuotientGeometryError(ValueError):
    pass


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def _require_finite(name: str, a: np.ndarray) -> None:
    if not np.all(np.isfinite(a)):
        raise ExactQuotientGeometryError(f"{name}: nonfinite")


def _canonical_sign(vectors: np.ndarray) -> np.ndarray:
    out = np.array(vectors, dtype=np.float64, copy=True)
    for j in range(out.shape[1]):
        col = out[:, j]
        abs_col = np.abs(col)
        pivot = int(np.flatnonzero(abs_col == abs_col.max())[0])
        if col[pivot] < 0.0:
            out[:, j] *= -1.0
    return out


@dataclass(frozen=True)
class ProfileQuotient:
    measurement_ids: tuple[str, ...]
    respondent_ids: tuple[str, ...]
    profile_state_vectors: tuple[tuple[str, ...], ...]
    profile_members: tuple[tuple[str, ...], ...]
    respondent_profile_index: tuple[int, ...]
    multiplicities: np.ndarray


def build_exact_profile_quotient(
    rows: Sequence[Mapping[str, Any]], measurement_ids: Sequence[str]
) -> ProfileQuotient:
    mids = tuple(measurement_ids)
    if not mids or len(mids) != len(set(mids)):
        raise ExactQuotientGeometryError("measurement_ids missing/duplicate")
    normalized = sorted(rows, key=lambda r: str(r["respondent_id"]))
    respondent_ids = tuple(str(r["respondent_id"]) for r in normalized)
    if not respondent_ids or len(respondent_ids) != len(set(respondent_ids)):
        raise ExactQuotientGeometryError("respondent identity missing/duplicate")
    profile_to_members: dict[tuple[str, ...], list[str]] = {}
    for row in normalized:
        states = row.get("state_by_measurement")
        if not isinstance(states, Mapping) or set(states) != set(mids):
            raise ExactQuotientGeometryError("missing/extra measurement state")
        profile = tuple(str(states[m]) for m in mids)
        profile_to_members.setdefault(profile, []).append(str(row["respondent_id"]))
    profiles = tuple(sorted(profile_to_members))
    members = tuple(tuple(sorted(profile_to_members[p])) for p in profiles)
    rid_to_profile = {rid: i for i, group in enumerate(members) for rid in group}
    respondent_profile_index = tuple(rid_to_profile[rid] for rid in respondent_ids)
    multiplicities = np.asarray([len(g) for g in members], dtype=np.float64)
    if int(multiplicities.sum()) != len(respondent_ids):
        raise ExactQuotientGeometryError("profile reconstruction mismatch")
    return ProfileQuotient(mids, respondent_ids, profiles, members,
                           respondent_profile_index, multiplicities)


def exact_profile_distance_matrix(
    quotient: ProfileQuotient, measurement_weights: Mapping[str, float] | None = None
) -> np.ndarray:
    k = len(quotient.profile_state_vectors)
    delta = np.zeros((k, k), dtype=np.float64)
    if measurement_weights is None:
        weights = np.ones(len(quotient.measurement_ids), dtype=np.float64)
    else:
        if set(measurement_weights) != set(quotient.measurement_ids):
            raise ExactQuotientGeometryError("weights must bind exactly active measurements")
        weights = np.asarray([float(measurement_weights[m]) for m in quotient.measurement_ids])
        if np.any(~np.isfinite(weights)) or np.any(weights <= 0):
            raise ExactQuotientGeometryError("weights must be finite positive")
    denom = float(weights.sum())
    profiles = quotient.profile_state_vectors
    for j, w in enumerate(weights):
        codes: dict[str, int] = {}
        col = np.empty(k, dtype=np.int64)
        for i, p in enumerate(profiles):
            col[i] = codes.setdefault(p[j], len(codes))
        delta += float(w) * (col[:, None] != col[None, :])
    delta /= denom
    np.fill_diagonal(delta, 0.0)
    _require_finite("profile distance", delta)
    return delta


def quotient_classical_mds_gram(delta: np.ndarray, multiplicities: np.ndarray) -> np.ndarray:
    delta = np.asarray(delta, dtype=np.float64)
    m = np.asarray(multiplicities, dtype=np.float64)
    if delta.ndim != 2 or delta.shape[0] != delta.shape[1] or delta.shape[0] != m.size:
        raise ExactQuotientGeometryError("distance/multiplicity shape mismatch")
    if np.any(m <= 0) or not np.allclose(delta, delta.T, atol=0.0, rtol=0.0):
        raise ExactQuotientGeometryError("invalid quotient distance/multiplicity")
    n = float(m.sum())
    s = np.sqrt(m)
    h = np.eye(m.size, dtype=np.float64) - np.outer(s, s) / n
    weighted_d2 = s[:, None] * (delta * delta) * s[None, :]
    gram = -0.5 * (h @ weighted_d2 @ h)
    gram = (gram + gram.T) * 0.5
    _require_finite("quotient gram", gram)
    return gram


def symmetric_eigensystem(gram: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    gram = np.asarray(gram, dtype=np.float64)
    if gram.ndim != 2 or gram.shape[0] != gram.shape[1]:
        raise ExactQuotientGeometryError("gram not square")
    if not np.allclose(gram, gram.T, atol=1e-12, rtol=1e-12):
        raise ExactQuotientGeometryError("gram not symmetric")
    try:
        values, vectors = linalg.eigh(gram, lower=True, overwrite_a=False,
                                      check_finite=True, driver=EIGH_DRIVER)
    except Exception as exc:
        raise ExactQuotientGeometryError(f"symmetric eigensolver failed: {exc}") from exc
    order = np.argsort(values, kind="stable")[::-1]
    values = np.asarray(values[order], dtype=np.float64)
    vectors = _canonical_sign(np.asarray(vectors[:, order], dtype=np.float64))
    _require_finite("eigenvalues", values); _require_finite("eigenvectors", vectors)
    residual = np.linalg.norm(gram @ vectors - vectors * values[None, :], ord="fro")
    scale = max(1.0, float(np.linalg.norm(gram, ord="fro")))
    orth = np.linalg.norm(vectors.T @ vectors - np.eye(vectors.shape[1]), ord="fro")
    if residual > ABS_TOL + REL_TOL * scale or orth > ABS_TOL + REL_TOL * vectors.shape[0]:
        raise ExactQuotientGeometryError(f"eigen replay failed residual={residual} orth={orth}")
    return values, vectors


def retained_profile_coordinates(values: np.ndarray, vectors: np.ndarray,
                                 multiplicities: np.ndarray, retained_d: int) -> np.ndarray:
    positive = np.flatnonzero(values > POSITIVE_EIGEN_EPS)
    if retained_d < 1 or retained_d > len(positive):
        raise ExactQuotientGeometryError("retained_d exceeds positive algebraic rank")
    idx = positive[:retained_d]
    coords = vectors[:, idx] * np.sqrt(values[idx])[None, :] / np.sqrt(multiplicities)[:, None]
    _require_finite("profile coordinates", coords)
    return coords


def embedded_profile_distances(coords: np.ndarray) -> np.ndarray:
    sq = np.sum(coords * coords, axis=1)
    d2 = np.maximum(0.0, sq[:, None] + sq[None, :] - 2.0 * coords @ coords.T)
    out = np.sqrt(d2)
    np.fill_diagonal(out, 0.0)
    return out


def expanded_gram_from_quotient(gram: np.ndarray, quotient: ProfileQuotient) -> np.ndarray:
    idx = np.asarray(quotient.respondent_profile_index, dtype=np.int64)
    m = quotient.multiplicities
    return gram[idx[:, None], idx[None, :]] / np.sqrt(m[idx])[:, None] / np.sqrt(m[idx])[None, :]


def normalized_stress_exact(delta: np.ndarray, embedded: np.ndarray, multiplicities: np.ndarray) -> float:
    m = np.asarray(multiplicities, dtype=np.int64)
    num = den = 0.0
    k = len(m)
    for a in range(k):
        for b in range(a + 1, k):
            w = int(m[a]) * int(m[b])
            num += w * float((delta[a,b] - embedded[a,b]) ** 2)
            den += w * float(delta[a,b] ** 2)
    return math.sqrt(num / den) if den > 0 else 0.0


def exact_distance_groups_for_profile(quotient: ProfileQuotient, delta: np.ndarray, profile_index: int) -> list[dict[str, Any]]:
    buckets: dict[float, list[str]] = {}
    for j, members in enumerate(quotient.profile_members):
        buckets.setdefault(float(delta[profile_index, j]), []).extend(members)
    return [{"distance": d, "respondent_ids": sorted(ids)} for d, ids in sorted(buckets.items())]


def exact_neighbors_for_respondent(quotient: ProfileQuotient, delta: np.ndarray,
                                   respondent_id: str, k: int) -> list[tuple[str, float]]:
    rid_pos = quotient.respondent_ids.index(respondent_id)
    p = quotient.respondent_profile_index[rid_pos]
    peers: list[tuple[float, str]] = []
    for group in exact_distance_groups_for_profile(quotient, delta, p):
        d = float(group["distance"])
        peers.extend((d, rid) for rid in group["respondent_ids"] if rid != respondent_id)
    peers.sort(key=lambda x: (x[0], x[1]))
    return [(rid, d) for d, rid in peers[:min(k, len(peers))]]


def jackknife_neighborhood_stability_exact(n: int, k: int) -> dict[str, Any]:
    if n <= 2:
        return {"replicate_count":0,"median_jaccard":1.0,"p10_jaccard":1.0,
                "status":"INSUFFICIENT_N_FOR_NONTRIVIAL_JACKKNIFE"}
    k0 = min(k, n - 1)
    if k0 == n - 1 or k0 == 0:
        bad_score = 1.0; bad_count = 0
    else:
        bad_score = (k0 - 1) / k0
        bad_count = n * k0
    total = n * (n - 1)
    def q(index: int) -> float:
        return bad_score if index < bad_count else 1.0
    return {"method":"DETERMINISTIC_LEAVE_ONE_RESPONDENT_OUT_R1",
            "replicate_count":n,"comparison_count":total,
            "median_jaccard":q(total//2),
            "p10_jaccard":q(max(0, math.ceil(0.10*total)-1)),
            "status":"DIAGNOSTIC_ONLY__THRESHOLDS_PREDECLARED_BY_EXECUTION_COURT"}


def solve_component(rows: Sequence[Mapping[str, Any]], measurement_ids: Sequence[str], *,
                    retained_d: int, neighborhood_k: int,
                    measurement_weights: Mapping[str, float] | None = None) -> dict[str, Any]:
    q = build_exact_profile_quotient(rows, measurement_ids)
    delta = exact_profile_distance_matrix(q, measurement_weights)
    gram = quotient_classical_mds_gram(delta, q.multiplicities)
    values, vectors = symmetric_eigensystem(gram)
    positive_rank = int(np.sum(values > POSITIVE_EIGEN_EPS))
    coords = retained_profile_coordinates(values, vectors, q.multiplicities, retained_d)
    embedded = embedded_profile_distances(coords)
    profile_receipt = {
        "respondent_count":len(q.respondent_ids),"profile_count":len(q.profile_members),
        "multiplicity_sum":int(q.multiplicities.sum()),
        "max_multiplicity":int(q.multiplicities.max()),
        "respondent_reconstruction_count":sum(len(x) for x in q.profile_members),
        "respondent_deletion_count":0,"semantic_state_merge_count":0,
        "profile_state_vectors_sha256":canonical_sha256(q.profile_state_vectors),
        "profile_membership_sha256":canonical_sha256(q.profile_members),
    }
    return {
        "method_family":METHOD_FAMILY,
        "measurement_ids":list(q.measurement_ids),
        "profile_receipt":profile_receipt,
        "positive_algebraic_rank":positive_rank,
        "retained_d":retained_d,
        "positive_eigenvalues":[float(x) for x in values[values > POSITIVE_EIGEN_EPS]],
        "quotient_gram_sha256":hashlib.sha256(np.asarray(gram,dtype='<f8',order='C').tobytes()).hexdigest(),
        "profile_distance_sha256":hashlib.sha256(np.asarray(delta,dtype='<f8',order='C').tobytes()).hexdigest(),
        "profile_coordinates_sha256":hashlib.sha256(np.asarray(coords,dtype='<f8',order='C').tobytes()).hexdigest(),
        "normalized_stress":normalized_stress_exact(delta, embedded, q.multiplicities),
        "neighborhood_k":neighborhood_k,
        "neighborhood_jackknife":jackknife_neighborhood_stability_exact(len(q.respondent_ids), neighborhood_k),
        "relation_reconstruction":"EXACT_FROM_PROFILE_DISTANCE_PLUS_PROFILE_MEMBERSHIP__SORT_DISTANCE_THEN_RESPONDENT_ID",
        "axis_interpretation":"PROHIBITED__NUMERIC_DIMENSION_IDS_ONLY",
    }
