"""KUDA-017/018: existing F6M stratum synthesis -> original F6P real value consumer.

This is NOT the S04 same-finite-frame Fréchet operation, original-wave
source authority, a new standardization method, a person sampler, or N9.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from rawlsing_next import pre553_heterogeneous_synthesis as f6m
from rawlsing_next._f6_candidate import f6p_partial_bound_evidence_consumer as f6p
from rawlsing_next.pre553_empirical_objects import semantic_hash


class F6PairIntegrationError(ValueError):
    """Sourcefree original-product custody or downstream evidence integrity lost."""


@dataclass(frozen=True)
class F6PairEvidence:
    product: Mapping[str, Any]
    evidence: Mapping[str, Any]
    grade: str = "SOURCEFREE_EXPERIMENT_ONLY__OWNER_ADMISSION_UNVERIFIED"


def evaluate_f6m_f6p_sourcefree(
    *,
    target: Mapping[str, Any],
    sources: Sequence[Mapping[str, Any]],
    policy: Mapping[str, Any],
    request: Mapping[str, Any] | None = None,
) -> F6PairEvidence:
    """One original F6M computation and first actual F6P reader.

    F6M's own source, denominator, overlap and transport gates remain intact.
    F6P must issue typed negative rather than an uncovered-as-observed point.
    Do not call this wrapper with genuine originals without separate owner
    authorization; it is deliberately an experimental transport only.
    """
    # No admission callback is accepted here: no caller is allowed to
    # impersonate the missing owner or scientific-transport issuer.
    bundle = f6m.synthesize(dict(target), [dict(s) for s in sources], dict(policy))
    evidence = f6p.consume_f6m_evidence(bundle, dict(request or {}))
    if evidence["input_bundle"]["content_hash"] != bundle["content_hash"]:
        raise F6PairIntegrationError("F6P is not bound to the original F6M product")
    if evidence["source_product"]["module_git_blob"] != (
            "2df811d76db258d98d89ffb43c830cb221ff9a7d"):
        raise F6PairIntegrationError("original repaired F6M producer body not retained")
    if semantic_hash({k: v for k, v in evidence.items() if k != "output_hash"}) != evidence["output_hash"]:
        raise F6PairIntegrationError("F6P computed evidence output hash mismatch")
    if (evidence["real_use_authorized"] is not False
            or not evidence["no_common_respondent_inference"]
            or not evidence["no_route_probability"]
            or not evidence["no_selection_weight"]):
        raise F6PairIntegrationError("F6P silently promoted sourcefree evidence")
    if evidence["evidence_state"] != f6p.SUPPORTED and evidence["supported_point"] is not None:
        raise F6PairIntegrationError("partial/unidentified/held state cannot return a point")
    return F6PairEvidence(bundle, evidence)


__all__ = ["F6PairIntegrationError", "F6PairEvidence", "evaluate_f6m_f6p_sourcefree"]
