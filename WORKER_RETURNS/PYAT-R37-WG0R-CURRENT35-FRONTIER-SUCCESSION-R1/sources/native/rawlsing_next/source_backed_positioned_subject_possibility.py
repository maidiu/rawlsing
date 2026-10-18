"""Governed source-backed positioned-subject possibility + specificity walkback.

Separate learned-world service: PRE553 exact queries are never broadened.
A broader slice can appear only in an explicit PROXY lane with authority,
specificity loss, provenance, and deterministic replay.

PROXY != EXACT FACT != ACTOR BELIEF.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, ExactRef, Pre553IntegrityError, canonicalize, semantic_hash,
)

CONTRACT_ID = "SOURCE_BACKED_POSITIONED_SUBJECT_POSSIBILITY@1.0.0"
QUERY_CONTRACT_ID = "POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_QUERY@1"
FIELD_CONTRACT_ID = "POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_FIELD@1"
MODEL_RULE_ID = "POSITIONED_SUBJECT_EXACT_CONDITIONAL_WITH_GOVERNED_WALKBACK@1.0.0"
MODEL_ALGORITHM_ID = "EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION"
EVIDENCE_STATES = frozenset({"SUPPORTED", "UNDERPOWERED", "VALID_EMPTY", "UNRESOLVED", "NONCOMPARABLE", "UNAVAILABLE"})
RESULT_STATES = frozenset({"EXACT_SUPPORTED", "EXACT_UNRESOLVED_PROXY_AVAILABLE", "UNRESOLVED", "VALID_EMPTY", "NONCOMPARABLE", "FAIL_CLOSED"})
EPISTEMIC_CEILING = (
    "PROXY != EXACT FACT != ACTOR BELIEF",
    "EMPIRICAL_POSSIBILITY != INDIVIDUAL_PREDICTION",
    "EMPIRICAL_POSSIBILITY != NORMATIVE_RECOMMENDATION",
    "GENERATED_SUBJECT_FACT_IS_QUERY_CRITERION_NOT_UPSTREAM_OWNED_FACT",
)


class PositionedSubjectPossibilityError(Pre553IntegrityError):
    pass


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PositionedSubjectPossibilityError(f"{name} must be non-empty string")
    out = value.strip()
    if out.lower() in {"latest", "default", "nearest", "fuzzy", "*"}:
        raise PositionedSubjectPossibilityError(f"{name} may not be mutable/fuzzy")
    return out


def _ids(values: Iterable[str], name: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    out = tuple(sorted({_text(v, name) for v in values}))
    if not out and not allow_empty:
        raise PositionedSubjectPossibilityError(f"{name} may not be empty")
    return out


def _refs(values: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    values = tuple(values)
    if any(not isinstance(v, ExactRef) for v in values):
        raise PositionedSubjectPossibilityError("expected ExactRef")
    return tuple(sorted(set(values), key=lambda v: v.key))


def _auths(values: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    values = tuple(values)
    if any(not isinstance(v, AuthorityRef) for v in values):
        raise PositionedSubjectPossibilityError("expected AuthorityRef")
    return tuple(sorted(set(values), key=lambda v: v.key))


def _mat(value: Any) -> Any:
    return canonicalize(value)


@dataclass(frozen=True)
class ConditionerBinding:
    binding_id: str
    subject_fact_ref: ExactRef
    empirical_coordinate_ref: ExactRef
    comparability_authority_ref: AuthorityRef
    source_universe_ref: ExactRef
    release_ref: ExactRef
    effective_time_or_interval: Any

    def __post_init__(self) -> None:
        object.__setattr__(self, "binding_id", _text(self.binding_id, "binding_id"))
        if not all(isinstance(v, ExactRef) for v in (self.subject_fact_ref, self.empirical_coordinate_ref, self.source_universe_ref, self.release_ref)):
            raise PositionedSubjectPossibilityError("conditioner exact refs required")
        if not isinstance(self.comparability_authority_ref, AuthorityRef):
            raise PositionedSubjectPossibilityError("positive comparability authority ref required")
        _mat(self.effective_time_or_interval)

    def material(self) -> Mapping[str, Any]:
        return {
            "binding_id": self.binding_id,
            "subject_fact_ref": self.subject_fact_ref.as_dict(),
            "empirical_coordinate_ref": self.empirical_coordinate_ref.as_dict(),
            "comparability_authority_ref": self.comparability_authority_ref.as_dict(),
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "effective_time_or_interval": _mat(self.effective_time_or_interval),
        }


@dataclass(frozen=True)
class PositionedSubjectPossibilityQuery:
    query_id: str
    subject_ref: ExactRef
    target_ref: ExactRef
    source_universe_ref: ExactRef
    release_ref: ExactRef
    conditioner_bindings: tuple[ConditionerBinding, ...]
    requested_projection: Mapping[str, Any]
    purpose: str = "EMPIRICAL_POSSIBILITY_ONLY"

    def __post_init__(self) -> None:
        object.__setattr__(self, "query_id", _text(self.query_id, "query_id"))
        object.__setattr__(self, "purpose", _text(self.purpose, "purpose"))
        if self.purpose != "EMPIRICAL_POSSIBILITY_ONLY":
            raise PositionedSubjectPossibilityError("actor/prediction jurisdiction forbidden")
        if not all(isinstance(v, ExactRef) for v in (self.subject_ref, self.target_ref, self.source_universe_ref, self.release_ref)):
            raise PositionedSubjectPossibilityError("query exact refs required")
        if not self.conditioner_bindings:
            raise PositionedSubjectPossibilityError("at least one exact conditioner required")
        ids = [x.binding_id for x in self.conditioner_bindings]
        if len(ids) != len(set(ids)):
            raise PositionedSubjectPossibilityError("duplicate conditioner binding")
        if any(x.source_universe_ref != self.source_universe_ref or x.release_ref != self.release_ref for x in self.conditioner_bindings):
            raise PositionedSubjectPossibilityError("conditioner source/release mismatch; no implicit bridge")
        _mat(self.requested_projection)

    @property
    def conditioner_ids(self) -> tuple[str, ...]:
        return tuple(sorted(x.binding_id for x in self.conditioner_bindings))

    def material(self) -> Mapping[str, Any]:
        return {
            "contract": QUERY_CONTRACT_ID,
            "query_id": self.query_id,
            "purpose": self.purpose,
            "subject_ref": self.subject_ref.as_dict(),
            "target_ref": self.target_ref.as_dict(),
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "conditioner_bindings": [x.material() for x in sorted(self.conditioner_bindings, key=lambda x: x.binding_id)],
            "requested_projection": _mat(self.requested_projection),
        }

    @property
    def ref(self) -> ExactRef:
        h = semantic_hash(self.material())
        return ExactRef(QUERY_CONTRACT_ID, f"urn:rawlsing:learned-world:positioned-subject-query:sha256:{h}", h)


@dataclass(frozen=True)
class PossibilitySliceEvidence:
    evidence_ref: ExactRef
    source_universe_ref: ExactRef
    release_ref: ExactRef
    target_ref: ExactRef
    retained_conditioner_ids: tuple[str, ...]
    evidence_state: str
    geometry: Mapping[str, Any] | None
    raw_support: int | None
    uncertainty_state: str
    provenance_refs: tuple[ExactRef, ...] = ()
    authority_refs: tuple[AuthorityRef, ...] = ()

    def __post_init__(self) -> None:
        if not all(isinstance(v, ExactRef) for v in (self.evidence_ref, self.source_universe_ref, self.release_ref, self.target_ref)):
            raise PositionedSubjectPossibilityError("slice exact refs required")
        object.__setattr__(self, "retained_conditioner_ids", _ids(self.retained_conditioner_ids, "retained_conditioner_ids", allow_empty=True))
        state = _text(self.evidence_state, "evidence_state")
        if state not in EVIDENCE_STATES:
            raise PositionedSubjectPossibilityError("unsupported evidence state")
        object.__setattr__(self, "evidence_state", state)
        if self.raw_support is not None and (not isinstance(self.raw_support, int) or isinstance(self.raw_support, bool) or self.raw_support < 0):
            raise PositionedSubjectPossibilityError("raw_support must be nonnegative integer or None")
        object.__setattr__(self, "uncertainty_state", _text(self.uncertainty_state, "uncertainty_state"))
        if state == "SUPPORTED" and self.geometry is None:
            raise PositionedSubjectPossibilityError("SUPPORTED evidence requires geometry")
        if self.geometry is not None:
            _mat(self.geometry)
        object.__setattr__(self, "provenance_refs", _refs(self.provenance_refs))
        object.__setattr__(self, "authority_refs", _auths(self.authority_refs))


@dataclass(frozen=True)
class SpecificityWalkbackStep:
    step_id: str
    retained_conditioner_ids: tuple[str, ...]
    proxy_authority_ref: AuthorityRef
    source_universe_ref: ExactRef
    release_ref: ExactRef
    rationale: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "step_id", _text(self.step_id, "step_id"))
        object.__setattr__(self, "retained_conditioner_ids", _ids(self.retained_conditioner_ids, "retained_conditioner_ids", allow_empty=True))
        if not isinstance(self.proxy_authority_ref, AuthorityRef):
            raise PositionedSubjectPossibilityError("proxy authority ref required")
        if not isinstance(self.source_universe_ref, ExactRef) or not isinstance(self.release_ref, ExactRef):
            raise PositionedSubjectPossibilityError("walkback source/release exact refs required")
        object.__setattr__(self, "rationale", _text(self.rationale, "rationale"))

    def material(self) -> Mapping[str, Any]:
        return {
            "step_id": self.step_id,
            "retained_conditioner_ids": list(self.retained_conditioner_ids),
            "proxy_authority_ref": self.proxy_authority_ref.as_dict(),
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class PositionedSubjectPossibilityModelRule:
    model_authority_ref: AuthorityRef
    walkback_authority_ref: AuthorityRef
    source_universe_refs: tuple[ExactRef, ...]
    walkback_steps: tuple[SpecificityWalkbackStep, ...]
    positive_proxy_authority_refs: tuple[AuthorityRef, ...]
    model_rule_id: str = MODEL_RULE_ID
    algorithm_id: str = MODEL_ALGORITHM_ID

    def __post_init__(self) -> None:
        if not isinstance(self.model_authority_ref, AuthorityRef) or not isinstance(self.walkback_authority_ref, AuthorityRef):
            raise PositionedSubjectPossibilityError("model/walkback authority refs required")
        refs = _refs(self.source_universe_refs)
        if not refs:
            raise PositionedSubjectPossibilityError("governed source universe required")
        object.__setattr__(self, "source_universe_refs", refs)
        if _text(self.model_rule_id, "model_rule_id") != MODEL_RULE_ID or _text(self.algorithm_id, "algorithm_id") != MODEL_ALGORITHM_ID:
            raise PositionedSubjectPossibilityError("unrecognized or smoothing/interpolation model rule")
        step_ids = [x.step_id for x in self.walkback_steps]
        if len(step_ids) != len(set(step_ids)):
            raise PositionedSubjectPossibilityError("duplicate walkback step")
        positive = _auths(self.positive_proxy_authority_refs)
        object.__setattr__(self, "positive_proxy_authority_refs", positive)
        if {x.proxy_authority_ref for x in self.walkback_steps} - set(positive):
            raise PositionedSubjectPossibilityError("every walkback step needs positively listed proxy authority")

    def material(self) -> Mapping[str, Any]:
        return {
            "contract": CONTRACT_ID,
            "model_rule_id": self.model_rule_id,
            "algorithm_id": self.algorithm_id,
            "model_authority_ref": self.model_authority_ref.as_dict(),
            "walkback_authority_ref": self.walkback_authority_ref.as_dict(),
            "source_universe_refs": [x.as_dict() for x in self.source_universe_refs],
            "walkback_steps": [x.material() for x in self.walkback_steps],
            "positive_proxy_authority_refs": [x.as_dict() for x in self.positive_proxy_authority_refs],
            "cross_source_proxy": "FORBIDDEN_IN_V1",
            "proxy_can_satisfy_exact_request": False,
            "actor_inference_allowed": False,
        }

    @property
    def rule_hash(self) -> str:
        return semantic_hash(self.material())


@dataclass(frozen=True)
class SpecificityLoss:
    requested_conditioner_ids: tuple[str, ...]
    retained_conditioner_ids: tuple[str, ...]
    dropped_conditioner_ids: tuple[str, ...]
    loss_count: int
    loss_fraction: Fraction

    @classmethod
    def build(cls, requested: Iterable[str], retained: Iterable[str]) -> "SpecificityLoss":
        req = _ids(requested, "requested_conditioner_ids")
        keep = _ids(retained, "retained_conditioner_ids", allow_empty=True)
        if not set(keep) < set(req):
            raise PositionedSubjectPossibilityError("proxy must strictly lose specificity")
        dropped = tuple(sorted(set(req) - set(keep)))
        return cls(req, keep, dropped, len(dropped), Fraction(len(dropped), len(req)))

    def material(self) -> Mapping[str, Any]:
        return {
            "requested_conditioner_ids": list(self.requested_conditioner_ids),
            "retained_conditioner_ids": list(self.retained_conditioner_ids),
            "dropped_conditioner_ids": list(self.dropped_conditioner_ids),
            "loss_count": self.loss_count,
            "loss_fraction": self.loss_fraction,
        }


@dataclass(frozen=True)
class WalkbackAttempt:
    step_id: str
    state: str
    specificity_loss: SpecificityLoss
    proxy_authority_ref: AuthorityRef
    evidence_ref: ExactRef | None
    detail: str

    def material(self) -> Mapping[str, Any]:
        return {
            "step_id": self.step_id,
            "state": self.state,
            "specificity_loss": self.specificity_loss.material(),
            "proxy_authority_ref": self.proxy_authority_ref.as_dict(),
            "evidence_ref": None if self.evidence_ref is None else self.evidence_ref.as_dict(),
            "detail": self.detail,
        }


@dataclass(frozen=True)
class ProxyPossibilityProjection:
    evidence_ref: ExactRef
    geometry: Mapping[str, Any]
    uncertainty_state: str
    raw_support: int | None
    specificity_loss: SpecificityLoss
    proxy_authority_ref: AuthorityRef
    source_universe_ref: ExactRef
    release_ref: ExactRef

    def material(self) -> Mapping[str, Any]:
        return {
            "projection_kind": "EXPLICIT_LOWER_SPECIFICITY_PROXY",
            "evidence_ref": self.evidence_ref.as_dict(),
            "geometry": _mat(self.geometry),
            "uncertainty_state": self.uncertainty_state,
            "raw_support": self.raw_support,
            "specificity_loss": self.specificity_loss.material(),
            "proxy_authority_ref": self.proxy_authority_ref.as_dict(),
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "is_exact_fact": False,
            "is_actor_belief": False,
        }


@dataclass(frozen=True)
class PositionedSubjectPossibilityResult:
    query_ref: ExactRef
    result_state: str
    exact_disposition: str
    exact_reason: str
    exact_evidence_ref: ExactRef | None
    exact_geometry: Mapping[str, Any] | None
    proxy: ProxyPossibilityProjection | None
    fallback_path: tuple[WalkbackAttempt, ...]
    model_authority_ref: AuthorityRef
    walkback_authority_ref: AuthorityRef
    source_universe_ref: ExactRef
    release_ref: ExactRef
    target_ref: ExactRef
    replay_determinants: tuple[ExactRef, ...]
    model_rule_hash: str

    def __post_init__(self) -> None:
        if self.result_state not in RESULT_STATES:
            raise PositionedSubjectPossibilityError("invalid result state")
        _text(self.exact_disposition, "exact_disposition"); _text(self.exact_reason, "exact_reason")
        if self.exact_geometry is not None: _mat(self.exact_geometry)
        object.__setattr__(self, "replay_determinants", _refs(self.replay_determinants))
        if not isinstance(self.model_rule_hash, str) or len(self.model_rule_hash) != 64:
            raise PositionedSubjectPossibilityError("model_rule_hash must be sha256")

    def material(self) -> Mapping[str, Any]:
        return {
            "contract": FIELD_CONTRACT_ID,
            "query_ref": self.query_ref.as_dict(),
            "result_state": self.result_state,
            "exact_lane": {
                "disposition": self.exact_disposition,
                "reason": self.exact_reason,
                "evidence_ref": None if self.exact_evidence_ref is None else self.exact_evidence_ref.as_dict(),
                "geometry": _mat(self.exact_geometry),
            },
            "proxy_lane": None if self.proxy is None else self.proxy.material(),
            "fallback_path": [x.material() for x in self.fallback_path],
            "model_authority_ref": self.model_authority_ref.as_dict(),
            "walkback_authority_ref": self.walkback_authority_ref.as_dict(),
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "target_ref": self.target_ref.as_dict(),
            "replay_determinants": [x.as_dict() for x in self.replay_determinants],
            "model_rule_hash": self.model_rule_hash,
            "epistemic_ceiling": list(EPISTEMIC_CEILING),
        }

    @property
    def result_hash(self) -> str:
        return semantic_hash(self.material())

    @property
    def ref(self) -> ExactRef:
        h = self.result_hash
        return ExactRef(FIELD_CONTRACT_ID, f"urn:rawlsing:learned-world:positioned-subject-field:sha256:{h}", h)

    @property
    def replay_identity(self) -> str:
        return f"urn:rawlsing:learned-world:positioned-subject-replay:sha256:{self.result_hash}"


def _find(evidence: tuple[PossibilitySliceEvidence, ...], query: PositionedSubjectPossibilityQuery, ids: tuple[str, ...]) -> PossibilitySliceEvidence | None:
    matches = [x for x in evidence if x.source_universe_ref == query.source_universe_ref and x.release_ref == query.release_ref and x.target_ref == query.target_ref and x.retained_conditioner_ids == ids]
    if len(matches) > 1:
        raise PositionedSubjectPossibilityError("duplicate evidence at exact source/release/target/specificity grain")
    return matches[0] if matches else None


def _result(query, rule, state, disposition, reason, exact, proxy, path, used_refs=()) -> PositionedSubjectPossibilityResult:
    return PositionedSubjectPossibilityResult(
        query.ref, state, disposition, reason,
        None if exact is None else exact.evidence_ref,
        exact.geometry if exact is not None and exact.evidence_state == "SUPPORTED" else None,
        proxy, tuple(path), rule.model_authority_ref, rule.walkback_authority_ref,
        query.source_universe_ref, query.release_ref, query.target_ref,
        (query.ref, *tuple(used_refs)), rule.rule_hash,
    )


def evaluate_positioned_subject_possibility(*, query: PositionedSubjectPossibilityQuery, rule: PositionedSubjectPossibilityModelRule, evidence: Iterable[PossibilitySliceEvidence]) -> PositionedSubjectPossibilityResult:
    evidence = tuple(sorted(evidence, key=lambda x: x.evidence_ref.key))
    if query.source_universe_ref not in set(rule.source_universe_refs):
        return _result(query, rule, "FAIL_CLOSED", "UNRESOLVED", "MODEL_SOURCE_UNIVERSE_OUT_OF_SCOPE", None, None, ())

    exact = _find(evidence, query, query.conditioner_ids)
    if exact is not None:
        if exact.evidence_state == "SUPPORTED":
            return _result(query, rule, "EXACT_SUPPORTED", "SUPPORTED", "EXACT_POSITIONED_STRATUM_SUPPORTED", exact, None, (), (exact.evidence_ref,))
        if exact.evidence_state == "VALID_EMPTY":
            return _result(query, rule, "VALID_EMPTY", "VALID_EMPTY", "EXACT_POSITIONED_STRATUM_VALID_EMPTY", exact, None, (), (exact.evidence_ref,))
        if exact.evidence_state == "NONCOMPARABLE":
            return _result(query, rule, "NONCOMPARABLE", "NONCOMPARABLE", "EXACT_POSITIONED_STRATUM_NONCOMPARABLE", exact, None, (), (exact.evidence_ref,))
        exact_reason = f"EXACT_{exact.evidence_state}"
    else:
        exact_reason = "EXACT_POSITIONED_STRATUM_ABSENT"

    requested = set(query.conditioner_ids); previous = requested
    path: list[WalkbackAttempt] = []; used: list[ExactRef] = []
    if exact is not None: used.append(exact.evidence_ref)
    for step in rule.walkback_steps:
        retained = set(step.retained_conditioner_ids)
        if not retained < requested or not retained < previous:
            raise PositionedSubjectPossibilityError("walkback ladder must strictly decrease specificity")
        previous = retained
        loss = SpecificityLoss.build(query.conditioner_ids, step.retained_conditioner_ids)
        if step.source_universe_ref != query.source_universe_ref or step.release_ref != query.release_ref:
            path.append(WalkbackAttempt(step.step_id, "FAIL_CLOSED_UNAUTHORIZED_PROXY_SOURCE", loss, step.proxy_authority_ref, None, "V1 proxies may not cross source universe or release"))
            return _result(query, rule, "FAIL_CLOSED", "UNRESOLVED", exact_reason, exact, None, path, used)
        candidate = _find(evidence, query, step.retained_conditioner_ids)
        if candidate is None:
            path.append(WalkbackAttempt(step.step_id, "NO_EVIDENCE_AT_AUTHORIZED_PROXY_GRAIN", loss, step.proxy_authority_ref, None, "authorized proxy grain has no source-backed slice")); continue
        used.append(candidate.evidence_ref)
        if candidate.evidence_state != "SUPPORTED":
            path.append(WalkbackAttempt(step.step_id, f"PROXY_EVIDENCE_{candidate.evidence_state}", loss, step.proxy_authority_ref, candidate.evidence_ref, "typed proxy evidence cannot satisfy proxy support")); continue
        proxy = ProxyPossibilityProjection(candidate.evidence_ref, candidate.geometry or {}, candidate.uncertainty_state, candidate.raw_support, loss, step.proxy_authority_ref, candidate.source_universe_ref, candidate.release_ref)
        path.append(WalkbackAttempt(step.step_id, "AUTHORIZED_PROXY_SELECTED", loss, step.proxy_authority_ref, candidate.evidence_ref, "broader support selected only as explicit proxy; exact lane remains unresolved"))
        return _result(query, rule, "EXACT_UNRESOLVED_PROXY_AVAILABLE", "UNRESOLVED", exact_reason, exact, proxy, path, used)
    return _result(query, rule, "UNRESOLVED", "UNRESOLVED", exact_reason, exact, None, path, used)


def verify_positioned_subject_possibility_replay(expected: PositionedSubjectPossibilityResult, *, query: PositionedSubjectPossibilityQuery, rule: PositionedSubjectPossibilityModelRule, evidence: Iterable[PossibilitySliceEvidence]) -> PositionedSubjectPossibilityResult:
    replayed = evaluate_positioned_subject_possibility(query=query, rule=rule, evidence=evidence)
    if replayed.result_hash != expected.result_hash or replayed.material() != expected.material():
        raise PositionedSubjectPossibilityError("positioned-subject possibility replay mismatch")
    return replayed
