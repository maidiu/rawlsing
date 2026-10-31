"""POST-ASTRA R3 PE — generic multi-condition / role-reversal world-situated possibility seam.

Candidate versioned public interface over the ALREADY-ACCEPTED C1 analytical
composition (``pre553_analytical_composition.compose_positioned_subject_possibility``,
which consumes the lower generic ``_all_bindings`` multi-conditioner law) and the
accepted public consumer (``source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility``).

OWNERSHIP LAW — this module is a thin versioned boundary, NOT a new estimator:

* it owns NO survey semantics, NO comparability meaning, NO probability model,
  NO smoothing/interpolation/extrapolation, NO structural admission and NO
  actor/person state;
* it never accepts a caller-supplied ``PossibilitySliceEvidence`` and never
  accepts precomputed probability geometry as authoritative input;
* slice geometry is produced only by the accepted C1 producer path from exact
  empirical products;
* the legacy public N10E facade (``provide_empirical_possibility_slice`` /
  ``_single_binding``) is UNCHANGED and still enforces its accepted C1-01
  single-conditioner grain; this seam is the separate versioned path that
  exposes the richer EXISTING C1 multi-binding/joint capability plus lawful
  role/target reversal, where the caller supplies the exact reversal, unit and
  operation authority.

GENERICITY LAW — no parent-specific PRE-V3 semantics:

* the request schema carries only generic opaque subject/coordinate refs;
* there is no ``is_father_query`` / parent / household flag anywhere in the
  contract; parent-flavored usage is a downstream TEST-ONLY consumer fixture
  label, never an upstream noun;
* a request whose subject/projection material smuggles parent-assignment,
  household-sampling or type/psyche claims is rejected at this boundary
  (artificial parent sampling and type-from-marginals are refused here, not
  laundered into a generic class name);
* a request demanding a NEW unit of analysis (e.g. household/dyad joint) that
  the source operation does not authorize is refused: same-respondent joint is
  not household dependence and neither is a causal effect.

ROLE / TARGET REVERSAL LAW:

* ``FORWARD_SUBJECT_TO_TARGET``: subject fixed at a conditioner value; target is
  a distinct coordinate;
* ``REVERSE_TARGET_VALUE_TO_SUBJECT``: subject fixed at a target-coordinate
  value; target is a distinct coordinate; REQUIRES an explicit positively scoped
  role-reversal authority (P(A|D) is not P(D|A); reversal needs its own valid
  target topology, risk set, denominator and operation/design authority);
* ``MULTI_CONDITION_INTERSECTION``: two or more conditioners intersected in one
  exact C1 condition predicate at the declared empirical grain;
* a REVERSE request without positively scoped reversal authority is refused
  (``REVERSED_UNAUTHORIZED_ROLE``). Conditioning on the target coordinate
  itself is refused (``SELF_TARGET_CONDITIONING``).

N9 WORLD DEPENDENCY LAW:

* every request binds an immutable selected N9 world snapshot ref and an
  immutable as-of coordinate, plus declared selected/asof dependency IDs;
* this seam never invents N9 current and never resolves a world itself; it only
  carries exact caller-declared world dependency identity into the receipt;
* an INVALIDATED current snapshot yields a typed refusal, never a stale positive;
* an as-of / effective claim at or after the request time yields a typed refusal
  (``FUTURE_TIME_AVAILABILITY_REFUSED``): later publication is not knowledge
  available to an earlier request.

INFERENCE-LANE LAW (W10's joint carriage is not joint conditioning):

* ``N10E_CONDITIONED_EMPIRICAL_INFERENCE`` — an exact empirical slice was
  actually computed by C1 at its declared grain for the requested conditioner
  set; the numeric fractions are exact arithmetic on the source law at that
  grain only;
* ``WORLD_ONLY_ROUTE_ELIGIBILITY`` — only world premises / route eligibility
  were bound; NO empirical probability is produced and the receipt forbids any
  numeric merge across grains;
* a receipt that carries both a world premise and an N10E slice declares the
  N10E lane for the numeric content and explicitly labels the world content as
  non-probabilistic carriage (never multiplied, never a route probability).

EPISTEMIC_CEILING: a GENERIC WORLD-SITUATED RECEIPT is not an adoption, not an
operative N9 world, not a structural-world claim, not an actor/person state, not
a scientific probability about real people, and not an AT33 progressive-world
proof. Fractions are exact synthetic-source arithmetic at the declared empirical
grain. This is a CANDIDATE TEST-ONLY interface court.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionResult,
    ConditionValueBindingWitness,
    compose_positioned_subject_possibility,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    PositionedSubjectPossibilityResult,
    evaluate_positioned_subject_possibility,
)

CONTRACT_ID = "POSTASTRA_PE_GENERIC_WORLD_SITATED_POSSIBILITY@1.0.0"
REQUEST_SCHEMA = "POSTASTRA_PE_GENERIC_WORLD_SITATED_REQUEST@1"
RECEIPT_SCHEMA = "POSTASTRA_PE_GENERIC_WORLD_SITATED_RECEIPT@1"
SERVICE_GRADE = (
    "CANDIDATE_TEST_ONLY__NOT_OPERATIVE_N9__NOT_SCIENCE__NOT_V3__"
    "NOT_SOURCE_OR_E_PRE_ISSUER__NOT_MODEL_USE_ISSUER__NOT_ADOPTION"
)

PURPOSE = "EMPIRICAL_POSSIBILITY_ONLY"

ROLE_FORWARD = "FORWARD_SUBJECT_TO_TARGET"
ROLE_REVERSE = "REVERSE_TARGET_VALUE_TO_SUBJECT"
ROLE_MULTI = "MULTI_CONDITION_INTERSECTION"
ROLE_DIRECTIONS = frozenset({ROLE_FORWARD, ROLE_REVERSE, ROLE_MULTI})

N9_SELECTED_IMMUTABLE = "SELECTED_IMMUTABLE"
N9_INVALIDATED = "INVALIDATED"
N9_SNAPSHOT_STATES = frozenset({N9_SELECTED_IMMUTABLE, N9_INVALIDATED})

LANE_N10E = "N10E_CONDITIONED_EMPIRICAL_INFERENCE"
LANE_WORLD_ONLY = "WORLD_ONLY_ROUTE_ELIGIBILITY"
INFERENCE_LANES = frozenset({LANE_N10E, LANE_WORLD_ONLY})

REFUSAL_REVERSED_UNAUTHORIZED_ROLE = "REVERSED_UNAUTHORIZED_ROLE"
REFUSAL_SELF_TARGET_CONDITIONING = "SELF_TARGET_CONDITIONING"
REFUSAL_NEW_UNIT = "NEW_UNIT_NOT_AUTHORIZED"
REFUSAL_ARTIFICIAL_PARENT_SAMPLING = "ARTIFICIAL_PARENT_SAMPLING_REFUSED"
REFUSAL_FAKE_MODEL_USE = "FAKE_MODEL_USE_REFUSED"
REFUSAL_SOURCE_HASH_FORGERY = "SOURCE_HASH_FORGERY_REFUSED"
REFUSAL_MISSING_DENOMINATOR = "MISSING_CONDITIONAL_DENOMINATOR"
REFUSAL_INVALIDATED_CURRENT = "INVALIDATED_CURRENT_REFUSED"
REFUSAL_FUTURE_TIME = "FUTURE_TIME_AVAILABILITY_REFUSED"

#: Assignment-shaped parent / household / type / psyche tokens.  A generic
#: request may carry opaque subject refs and exact empirical coordinates only;
#: any claim-bearing parent-assignment, household-sampling or type token is
#: refused at this boundary (no parent nouns upstream, no type-from-marginals).
FORBIDDEN_REQUEST_TOKENS = (
    "IS_FATHER",
    "IS FATHER",
    "IS_MOTHER",
    "IS MOTHER",
    "IS_PARENT",
    "IS PARENT",
    "ARTIFICIAL_PARENT",
    "PARENT_SAMPLING",
    "HOUSEHOLD_SAMPLING",
    "DYAD_SAMPLE",
    "IS_TYPE",
    "IS TYPE",
    "TYPE_5",
    "TYPE 6",
    "ENNEAGRAM",
    "PERSONALITY_ASSIGNED",
    "BIOGRAPHY_ASSIGNED",
    "VOICE_ASSIGNED",
    "PSYCHE_STATE",
)

EPISTEMIC_CEILING = (
    "PROXY != EXACT FACT != ACTOR BELIEF",
    "EMPIRICAL_POSSIBILITY != INDIVIDUAL_PREDICTION",
    "EMPIRICAL_POSSIBILITY != CAUSAL_EFFECT",
    "EMPIRICAL_POSSIBILITY != NORMATIVE_RECOMMENDATION",
    "SAME_RESPONDENT_JOINT != HOUSEHOLD_DYAD_DEPENDENCE",
    "WORLD_ROUTE_ELIGIBILITY != N10E_CONDITIONED_NUMERICAL_INFERENCE",
    "GENERATED_SUBJECT_FACT_IS_QUERY_CRITERION_NOT_UPSTREAM_OWNED_FACT",
    "FRACTIONS_ARE_EXACT_ARITHMETIC_AT_DECLARED_EMPIRICAL_GRAIN_ONLY",
)


class GenericWorldPossibilityError(Pre553IntegrityError):
    """Typed generic-seam failure; upstream owner errors are not laundered."""


class GenericWorldRequestShapeError(GenericWorldPossibilityError):
    code = "GENERIC_WORLD_REQUEST_SHAPE_ERROR"


class GenericWorldRequestLawError(GenericWorldPossibilityError):
    code = "GENERIC_WORLD_REQUEST_LAW_ERROR"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GenericWorldRequestShapeError(f"{name} must be non-empty string")
    out = value.strip()
    if out.lower() in {"latest", "default", "nearest", "fuzzy", "*"}:
        raise GenericWorldRequestShapeError(f"{name} may not be mutable/fuzzy")
    return out


def _exact(value: ExactRef | Mapping[str, Any], name: str) -> ExactRef:
    if isinstance(value, ExactRef):
        return value
    if isinstance(value, Mapping):
        return ExactRef(**value)
    raise GenericWorldRequestShapeError(f"{name} must be ExactRef or mapping")


def _auth(value: AuthorityRef | Mapping[str, Any], name: str) -> AuthorityRef:
    if isinstance(value, AuthorityRef):
        return value
    if isinstance(value, Mapping):
        return AuthorityRef(**value)
    raise GenericWorldRequestShapeError(f"{name} must be AuthorityRef or mapping")


def _reversal_authority_competent(
    authority_registry: Any,
    ref: AuthorityRef,
    *,
    target_ref: ExactRef,
    denominator_basis_ref: ExactRef,
) -> bool:
    """Dereference caller-supplied reversal authority against the issuer registry.

    A non-null AuthorityRef is only a caller shape.  Competence requires the
    exact authority snapshot to be present and positively scoped to the
    reverse-direction operation, target use and denominator/risk set.
    """
    try:
        snapshot = authority_registry.require(
            ref,
            authority_kind="TARGET_USE_PERMISSION",
            operation=ROLE_REVERSE,
            target_use_ref=target_ref,
            predicate_or_risk_set_ref=denominator_basis_ref,
        )
    except Exception:
        return False
    return (
        snapshot.typed_state == "ALLOW"
        and snapshot.decision_state == "ALLOW"
        and ROLE_REVERSE in snapshot.governed_operations
        and "POSTASTRA_PE_GENERIC_WORLD_SITATED_POSSIBILITY@1.0.0"
        in snapshot.governed_object_families
    )


def _refs(values: Iterable[ExactRef], name: str) -> tuple[ExactRef, ...]:
    out = tuple(_exact(v, name) for v in values)
    return tuple(sorted(set(out), key=lambda v: v.key))


def _scan_forbidden_tokens(material: Any) -> str | None:
    """Return the first forbidden parent/type token found in claim-bearing text."""
    blob = canonicalize(material)
    text = str(blob).upper()
    for token in FORBIDDEN_REQUEST_TOKENS:
        if token.upper() in text:
            return token
    return None


def _future_time(asof: Any, request_time: Any) -> bool:
    """True when the as-of/effective claim is at-or-after the request time.

    Both sides are canonicalized frozen fixture time coordinates.  A simple
    lexical ISO-8601 comparison is used because the seam only ever receives
    frozen fixture time coordinates; non-comparable shapes fail closed.
    """
    try:
        a_text = str(canonicalize(asof))
        r_text = str(canonicalize(request_time))
    except Exception:
        return True
    if not re.fullmatch(r"[0-9T:\-\.Z+]+", a_text) or not re.fullmatch(
        r"[0-9T:\-\.Z+]+", r_text
    ):
        return True
    return a_text >= r_text


@dataclass(frozen=True)
class N9WorldDependency:
    """Immutable selected N9 world identity carried into the receipt.

    This seam never resolves or invents N9 current; it binds exact caller-declared
    selected snapshot + as-of + dependency IDs so a consumer can prove which
    world cut its possibility claim is situated against.
    """

    n9_snapshot_ref: ExactRef
    n9_asof_ref: ExactRef
    n9_asof_time: Any
    n9_snapshot_state: str
    selected_dependency_refs: tuple[ExactRef, ...]
    asof_dependency_refs: tuple[ExactRef, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "n9_snapshot_ref", _exact(self.n9_snapshot_ref, "n9_snapshot_ref"))
        object.__setattr__(self, "n9_asof_ref", _exact(self.n9_asof_ref, "n9_asof_ref"))
        canonicalize(self.n9_asof_time)
        state = _text(self.n9_snapshot_state, "n9_snapshot_state")
        if state not in N9_SNAPSHOT_STATES:
            raise GenericWorldRequestShapeError("unsupported n9_snapshot_state")
        object.__setattr__(self, "n9_snapshot_state", state)
        object.__setattr__(
            self, "selected_dependency_refs", _refs(self.selected_dependency_refs, "selected_dependency_refs")
        )
        object.__setattr__(
            self, "asof_dependency_refs", _refs(self.asof_dependency_refs, "asof_dependency_refs")
        )

    def material(self) -> Mapping[str, Any]:
        return {
            "n9_snapshot_ref": self.n9_snapshot_ref.as_dict(),
            "n9_asof_ref": self.n9_asof_ref.as_dict(),
            "n9_asof_time": canonicalize(self.n9_asof_time),
            "n9_snapshot_state": self.n9_snapshot_state,
            "selected_dependency_refs": [x.as_dict() for x in self.selected_dependency_refs],
            "asof_dependency_refs": [x.as_dict() for x in self.asof_dependency_refs],
        }


@dataclass(frozen=True)
class GenericWorldSituatedRequest:
    """Generic, parent-noun-free world-situated empirical possibility request."""

    request_id: str
    subject_ref: ExactRef
    target_ref: ExactRef
    conditioner_bindings: tuple[ConditionerBinding, ...]
    role_direction: str
    native_unit_ref: ExactRef
    analysis_unit_ref: ExactRef
    denominator_basis_ref: ExactRef
    operation_authority_ref: AuthorityRef
    model_use_ref: AuthorityRef
    n9_world: N9WorldDependency
    request_time: Any
    role_reversal_authority_ref: AuthorityRef | None = None
    requested_projection: Mapping[str, Any] = None
    purpose: str = PURPOSE

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _text(self.request_id, "request_id"))
        purpose = _text(self.purpose, "purpose")
        if purpose != PURPOSE:
            raise GenericWorldRequestLawError("actor/prediction jurisdiction forbidden")
        object.__setattr__(self, "purpose", purpose)
        object.__setattr__(self, "subject_ref", _exact(self.subject_ref, "subject_ref"))
        object.__setattr__(self, "target_ref", _exact(self.target_ref, "target_ref"))
        object.__setattr__(
            self,
            "conditioner_bindings",
            tuple(self.conditioner_bindings),
        )
        if not self.conditioner_bindings:
            raise GenericWorldRequestShapeError("at least one exact conditioner required")
        if not all(isinstance(b, ConditionerBinding) for b in self.conditioner_bindings):
            raise GenericWorldRequestShapeError("conditioner bindings must be ConditionerBinding")
        ids = [b.binding_id for b in self.conditioner_bindings]
        if len(ids) != len(set(ids)):
            raise GenericWorldRequestShapeError("duplicate conditioner binding id")
        direction = _text(self.role_direction, "role_direction")
        if direction not in ROLE_DIRECTIONS:
            raise GenericWorldRequestShapeError("unsupported role_direction")
        if direction == ROLE_MULTI and len(self.conditioner_bindings) < 2:
            raise GenericWorldRequestLawError(
                "MULTI_CONDITION_INTERSECTION requires at least two conditioners"
            )
        object.__setattr__(self, "role_direction", direction)
        object.__setattr__(self, "native_unit_ref", _exact(self.native_unit_ref, "native_unit_ref"))
        object.__setattr__(self, "analysis_unit_ref", _exact(self.analysis_unit_ref, "analysis_unit_ref"))
        object.__setattr__(
            self, "denominator_basis_ref", _exact(self.denominator_basis_ref, "denominator_basis_ref")
        )
        object.__setattr__(
            self,
            "operation_authority_ref",
            _auth(self.operation_authority_ref, "operation_authority_ref"),
        )
        object.__setattr__(self, "model_use_ref", _auth(self.model_use_ref, "model_use_ref"))
        if not isinstance(self.n9_world, N9WorldDependency):
            raise GenericWorldRequestShapeError("n9_world must be N9WorldDependency")
        _mat = canonicalize(self.request_time)
        if self.role_reversal_authority_ref is not None:
            object.__setattr__(
                self,
                "role_reversal_authority_ref",
                _auth(self.role_reversal_authority_ref, "role_reversal_authority_ref"),
            )
        projection = dict(self.requested_projection or {})
        projection.setdefault("kind", "GENERIC_WORLD_SITATED_POSSIBILITY")
        object.__setattr__(self, "requested_projection", canonicalize(projection))
        _scan = _scan_forbidden_tokens(
            {
                "subject_ref": self.subject_ref.as_dict(),
                "requested_projection": self.requested_projection,
            }
        )
        if _scan is not None:
            raise GenericWorldRequestLawError(
                f"{REFUSAL_ARTIFICIAL_PARENT_SAMPLING}: forbidden token {_scan!r} in request"
            )

    @property
    def conditioner_ids(self) -> tuple[str, ...]:
        return tuple(sorted(b.binding_id for b in self.conditioner_bindings))

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": REQUEST_SCHEMA,
            "contract": CONTRACT_ID,
            "request_id": self.request_id,
            "purpose": self.purpose,
            "subject_ref": self.subject_ref.as_dict(),
            "target_ref": self.target_ref.as_dict(),
            "conditioner_bindings": [
                b.material() for b in sorted(self.conditioner_bindings, key=lambda x: x.binding_id)
            ],
            "role_direction": self.role_direction,
            "native_unit_ref": self.native_unit_ref.as_dict(),
            "analysis_unit_ref": self.analysis_unit_ref.as_dict(),
            "denominator_basis_ref": self.denominator_basis_ref.as_dict(),
            "operation_authority_ref": self.operation_authority_ref.as_dict(),
            "model_use_ref": self.model_use_ref.as_dict(),
            "role_reversal_authority_ref": (
                None
                if self.role_reversal_authority_ref is None
                else self.role_reversal_authority_ref.as_dict()
            ),
            "n9_world": self.n9_world.material(),
            "request_time": canonicalize(self.request_time),
            "requested_projection": self.requested_projection,
        }

    @property
    def request_hash(self) -> str:
        return semantic_hash(self.material())

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            REQUEST_SCHEMA,
            f"urn:rawlsing:postastra-pe:generic-world-request:sha256:{self.request_hash}",
            self.request_hash,
        )

    def derived_positioned_query(self) -> PositionedSubjectPossibilityQuery:
        """Exact accepted public consumer query shape, derived generically.

        The target/condition role mapping is preserved: the query target is the
        request target coordinate and the conditioners are exactly the request's
        bindings, so P(target | conditions) keeps its declared direction.
        """
        return PositionedSubjectPossibilityQuery(
            query_id=f"postastra-pe:{self.request_id}",
            subject_ref=self.subject_ref,
            target_ref=self.target_ref,
            source_universe_ref=self.conditioner_bindings[0].source_universe_ref,
            release_ref=self.conditioner_bindings[0].release_ref,
            conditioner_bindings=self.conditioner_bindings,
            requested_projection=self.requested_projection,
        )


@dataclass(frozen=True)
class GenericWorldSituatedReceipt:
    receipt_id: str
    request_ref: ExactRef
    role_direction: str
    inference_lane: str
    world_carriage_is_not_route_probability: bool
    n9_world: N9WorldDependency
    conditioner_count: int
    conditioner_ids: tuple[str, ...]
    target_ref: ExactRef
    native_unit_ref: ExactRef
    analysis_unit_ref: ExactRef
    denominator_basis_ref: ExactRef
    operation_authority_ref: AuthorityRef
    model_use_ref: AuthorityRef
    model_rule_hash: str
    producer_query_ref: ExactRef | None
    producer_predicate_ref: ExactRef | None
    producer_fact_ref: ExactRef | None
    producer_fact_state: str | None
    composed_result_identity_hash: str | None
    consumer_result_state: str | None
    consumer_result_identity_hash: str | None
    consumer_exact_geometry: Mapping[str, Any] | None
    consumer_exact_disposition: str | None
    consumer_exact_reason: str | None
    proxy_lane_present: bool
    refusal_state: str | None
    refusal_reason: str | None
    epistemic_ceiling: tuple[str, ...]

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": RECEIPT_SCHEMA,
            "contract": CONTRACT_ID,
            "service_grade": SERVICE_GRADE,
            "receipt_id": self.receipt_id,
            "request_ref": self.request_ref.as_dict(),
            "role_direction": self.role_direction,
            "inference_lane": self.inference_lane,
            "world_carriage_is_not_route_probability": self.world_carriage_is_not_route_probability,
            "n9_world": self.n9_world.material(),
            "conditioner_count": self.conditioner_count,
            "conditioner_ids": list(self.conditioner_ids),
            "target_ref": self.target_ref.as_dict(),
            "native_unit_ref": self.native_unit_ref.as_dict(),
            "analysis_unit_ref": self.analysis_unit_ref.as_dict(),
            "denominator_basis_ref": self.denominator_basis_ref.as_dict(),
            "operation_authority_ref": self.operation_authority_ref.as_dict(),
            "model_use_ref": self.model_use_ref.as_dict(),
            "model_rule_hash": self.model_rule_hash,
            "producer_query_ref": (
                None if self.producer_query_ref is None else self.producer_query_ref.as_dict()
            ),
            "producer_predicate_ref": (
                None if self.producer_predicate_ref is None else self.producer_predicate_ref.as_dict()
            ),
            "producer_fact_ref": (
                None if self.producer_fact_ref is None else self.producer_fact_ref.as_dict()
            ),
            "producer_fact_state": self.producer_fact_state,
            "composed_result_identity_hash": self.composed_result_identity_hash,
            "consumer_result_state": self.consumer_result_state,
            "consumer_result_identity_hash": self.consumer_result_identity_hash,
            "consumer_exact_geometry": canonicalize(self.consumer_exact_geometry),
            "consumer_exact_disposition": self.consumer_exact_disposition,
            "consumer_exact_reason": self.consumer_exact_reason,
            "proxy_lane_present": self.proxy_lane_present,
            "refusal_state": self.refusal_state,
            "refusal_reason": self.refusal_reason,
            "epistemic_ceiling": list(self.epistemic_ceiling),
        }

    @property
    def receipt_hash(self) -> str:
        return semantic_hash(self.material())

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            RECEIPT_SCHEMA,
            f"urn:rawlsing:postastra-pe:generic-world-receipt:sha256:{self.receipt_hash}",
            self.receipt_hash,
        )


@dataclass(frozen=True)
class GenericWorldSituatedResult:
    request_ref: ExactRef
    receipt: GenericWorldSituatedReceipt
    composition: AnalyticalCompositionResult | None
    consumer_result: PositionedSubjectPossibilityResult | None
    result_state: str

    @property
    def result_hash(self) -> str:
        return semantic_hash(
            {
                "request_ref": self.request_ref.as_dict(),
                "receipt_ref": self.receipt.ref.as_dict(),
                "result_state": self.result_state,
            }
        )


def _refusal(
    *,
    request: GenericWorldSituatedRequest,
    model_rule: PositionedSubjectPossibilityModelRule,
    inference_lane: str,
    refusal_state: str,
    refusal_reason: str,
    producer_fact_state: str | None = None,
) -> GenericWorldSituatedResult:
    receipt = GenericWorldSituatedReceipt(
        receipt_id=f"postastra-pe:refusal:{request.request_id}:{refusal_state}",
        request_ref=request.ref,
        role_direction=request.role_direction,
        inference_lane=inference_lane,
        world_carriage_is_not_route_probability=True,
        n9_world=request.n9_world,
        conditioner_count=len(request.conditioner_bindings),
        conditioner_ids=request.conditioner_ids,
        target_ref=request.target_ref,
        native_unit_ref=request.native_unit_ref,
        analysis_unit_ref=request.analysis_unit_ref,
        denominator_basis_ref=request.denominator_basis_ref,
        operation_authority_ref=request.operation_authority_ref,
        model_use_ref=request.model_use_ref,
        model_rule_hash=model_rule.rule_hash,
        producer_query_ref=None,
        producer_predicate_ref=None,
        producer_fact_ref=None,
        producer_fact_state=producer_fact_state,
        composed_result_identity_hash=None,
        consumer_result_state=None,
        consumer_result_identity_hash=None,
        consumer_exact_geometry=None,
        consumer_exact_disposition=None,
        consumer_exact_reason=None,
        proxy_lane_present=False,
        refusal_state=refusal_state,
        refusal_reason=refusal_reason,
        epistemic_ceiling=EPISTEMIC_CEILING,
    )
    return GenericWorldSituatedResult(
        request_ref=request.ref,
        receipt=receipt,
        composition=None,
        consumer_result=None,
        result_state="TYPED_REFUSAL",
    )


def serve_generic_world_situated_possibility(
    *,
    repository: Any,
    empirical_query: Any,
    predicate: Any,
    authority_registry: Any,
    release_refs: Iterable[ExactRef],
    request: GenericWorldSituatedRequest,
    model_rule: PositionedSubjectPossibilityModelRule,
    condition_binding_witness: ConditionValueBindingWitness,
    discovery_result: Any = None,
    discovery_receipt_ref: ExactRef | None = None,
    recursive_handoff: Any = None,
) -> GenericWorldSituatedResult:
    """Serve one generic world-situated empirical possibility claim.

    Fail-closed law: every boundary check below returns a typed refusal receipt
    with no geometry.  Upstream owner typed errors from the accepted C1
    composition propagate as those owners' own errors and are never laundered
    into invented geometry.
    """
    release_refs = _refs(release_refs, "release_refs")

    # --- future-time availability law -------------------------------------
    # The as-of coordinate must strictly precede the request time; a future or
    # as-of-at-request claim is not knowledge available to this request.  The
    # seam receives frozen fixture time coordinates only.
    if _future_time(request.n9_world.n9_asof_time, request.request_time):
        return _refusal(
            request=request,
            model_rule=model_rule,
            inference_lane=LANE_WORLD_ONLY,
            refusal_state=REFUSAL_FUTURE_TIME,
            refusal_reason="AS_OF_NOT_BEFORE_REQUEST_TIME__LATER_PUBLICATION_IS_NOT_EARLIER_KNOWLEDGE",
        )

    # --- invalidated current law ------------------------------------------
    if request.n9_world.n9_snapshot_state != N9_SELECTED_IMMUTABLE:
        return _refusal(
            request=request,
            model_rule=model_rule,
            inference_lane=LANE_WORLD_ONLY,
            refusal_state=REFUSAL_INVALIDATED_CURRENT,
            refusal_reason="N9_SNAPSHOT_INVALIDATED__NO_STALE_POSITIVE_SERVICE",
        )

    # --- new unit law ------------------------------------------------------
    if request.analysis_unit_ref != request.native_unit_ref:
        return _refusal(
            request=request,
            model_rule=model_rule,
            inference_lane=LANE_WORLD_ONLY,
            refusal_state=REFUSAL_NEW_UNIT,
            refusal_reason=(
                "ANALYSIS_UNIT_DIFFERS_FROM_SOURCE_NATIVE_UNIT__"
                "SAME_RESPONDENT_JOINT_IS_NOT_HOUSEHOLD_DYAD_DEPENDENCE"
            ),
        )

    # --- self-target conditioning law -------------------------------------
    for binding in request.conditioner_bindings:
        if binding.empirical_coordinate_ref == request.target_ref:
            return _refusal(
                request=request,
                model_rule=model_rule,
                inference_lane=LANE_WORLD_ONLY,
                refusal_state=REFUSAL_SELF_TARGET_CONDITIONING,
                refusal_reason="CONDITIONER_BINDS_THE_TARGET_COORDINATE_ITSELF",
            )

    # --- role reversal authority law --------------------------------------
    if request.role_direction == ROLE_REVERSE:
        reversal = request.role_reversal_authority_ref
        if reversal is None or not _reversal_authority_competent(
            authority_registry,
            reversal,
            target_ref=request.target_ref,
            denominator_basis_ref=request.denominator_basis_ref,
        ):
            return _refusal(
                request=request,
                model_rule=model_rule,
                inference_lane=LANE_WORLD_ONLY,
                refusal_state=REFUSAL_REVERSED_UNAUTHORIZED_ROLE,
                refusal_reason=(
                    "REVERSE_DIRECTION_REQUIRES_POSITIVELY_SCOPED_ROLE_REVERSAL_AUTHORITY__"
                    "P_A_GIVEN_D_IS_NOT_P_D_GIVEN_A__EXACT_ISSUER_DEREFERENCE_REQUIRED"
                ),
            )

    # --- model-use law ----------------------------------------------------
    if request.model_use_ref != model_rule.model_authority_ref:
        return _refusal(
            request=request,
            model_rule=model_rule,
            inference_lane=LANE_WORLD_ONLY,
            refusal_state=REFUSAL_FAKE_MODEL_USE,
            refusal_reason="REQUEST_MODEL_USE_REF_DOES_NOT_MATCH_GOVERNED_MODEL_RULE_AUTHORITY",
        )

    # --- denominator law --------------------------------------------------
    derived_query = request.derived_positioned_query()
    producer_risk_ref = getattr(empirical_query, "risk_set_ref", None)
    if producer_risk_ref is None or _exact(producer_risk_ref, "producer.risk_set_ref") != request.denominator_basis_ref:
        return _refusal(
            request=request,
            model_rule=model_rule,
            inference_lane=LANE_WORLD_ONLY,
            refusal_state=REFUSAL_MISSING_DENOMINATOR,
            refusal_reason="REQUEST_DENOMINATOR_BASIS_DOES_NOT_MATCH_PRODUCER_RISK_SET",
        )

    # --- accepted C1 computation (NO new estimator here) ------------------
    composition = compose_positioned_subject_possibility(
        repository=repository,
        empirical_query=empirical_query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=release_refs,
        consumer_query=derived_query,
        model_rule=model_rule,
        condition_binding_witness=condition_binding_witness,
        discovery_result=discovery_result,
        discovery_receipt_ref=discovery_receipt_ref,
        recursive_handoff=recursive_handoff,
    )

    evidence = () if composition.possibility_slice_evidence_or_null is None else (composition.possibility_slice_evidence_or_null,)
    consumer_result = evaluate_positioned_subject_possibility(
        query=derived_query, rule=model_rule, evidence=evidence
    )

    fact_state = composition.producer_fact_state
    if fact_state != "SUPPORTED":
        return _refusal(
            request=request,
            model_rule=model_rule,
            inference_lane=LANE_N10E,
            refusal_state="PRODUCER_FACT_NOT_SUPPORTED",
            refusal_reason=f"PRODUCER_FACT_STATE={fact_state}__NO_INVENTED_GEOMETRY",
            producer_fact_state=fact_state,
        )

    receipt = GenericWorldSituatedReceipt(
        receipt_id=f"postastra-pe:receipt:{request.request_id}",
        request_ref=request.ref,
        role_direction=request.role_direction,
        inference_lane=LANE_N10E,
        world_carriage_is_not_route_probability=True,
        n9_world=request.n9_world,
        conditioner_count=len(request.conditioner_bindings),
        conditioner_ids=request.conditioner_ids,
        target_ref=request.target_ref,
        native_unit_ref=request.native_unit_ref,
        analysis_unit_ref=request.analysis_unit_ref,
        denominator_basis_ref=request.denominator_basis_ref,
        operation_authority_ref=request.operation_authority_ref,
        model_use_ref=request.model_use_ref,
        model_rule_hash=model_rule.rule_hash,
        producer_query_ref=composition.producer_query_ref,
        producer_predicate_ref=composition.producer_predicate_ref,
        producer_fact_ref=composition.producer_fact_ref,
        producer_fact_state=composition.producer_fact_state,
        composed_result_identity_hash=composition.composed_result_identity_hash,
        consumer_result_state=consumer_result.result_state,
        consumer_result_identity_hash=consumer_result.result_hash,
        consumer_exact_geometry=consumer_result.exact_geometry,
        consumer_exact_disposition=consumer_result.exact_disposition,
        consumer_exact_reason=consumer_result.exact_reason,
        proxy_lane_present=consumer_result.proxy is not None,
        refusal_state=None,
        refusal_reason=None,
        epistemic_ceiling=EPISTEMIC_CEILING,
    )
    return GenericWorldSituatedResult(
        request_ref=request.ref,
        receipt=receipt,
        composition=composition,
        consumer_result=consumer_result,
        result_state="EXACT_SUPPORTED" if consumer_result.result_state == "EXACT_SUPPORTED" else consumer_result.result_state,
    )


def verify_generic_world_situated_replay(
    expected: GenericWorldSituatedResult,
    *,
    repository: Any,
    empirical_query: Any,
    predicate: Any,
    authority_registry: Any,
    release_refs: Iterable[ExactRef],
    request: GenericWorldSituatedRequest,
    model_rule: PositionedSubjectPossibilityModelRule,
    condition_binding_witness: ConditionValueBindingWitness,
) -> GenericWorldSituatedResult:
    replayed = serve_generic_world_situated_possibility(
        repository=repository,
        empirical_query=empirical_query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=release_refs,
        request=request,
        model_rule=model_rule,
        condition_binding_witness=condition_binding_witness,
    )
    if replayed.result_hash != expected.result_hash:
        raise GenericWorldPossibilityError("generic world-situated replay mismatch")
    return replayed


__all__ = [
    "CONTRACT_ID",
    "REQUEST_SCHEMA",
    "RECEIPT_SCHEMA",
    "SERVICE_GRADE",
    "PURPOSE",
    "ROLE_FORWARD",
    "ROLE_REVERSE",
    "ROLE_MULTI",
    "ROLE_DIRECTIONS",
    "N9_SELECTED_IMMUTABLE",
    "N9_INVALIDATED",
    "LANE_N10E",
    "LANE_WORLD_ONLY",
    "REFUSAL_REVERSED_UNAUTHORIZED_ROLE",
    "REFUSAL_SELF_TARGET_CONDITIONING",
    "REFUSAL_NEW_UNIT",
    "REFUSAL_ARTIFICIAL_PARENT_SAMPLING",
    "REFUSAL_FAKE_MODEL_USE",
    "REFUSAL_SOURCE_HASH_FORGERY",
    "REFUSAL_MISSING_DENOMINATOR",
    "REFUSAL_INVALIDATED_CURRENT",
    "REFUSAL_FUTURE_TIME",
    "EPISTEMIC_CEILING",
    "GenericWorldPossibilityError",
    "GenericWorldRequestShapeError",
    "GenericWorldRequestLawError",
    "N9WorldDependency",
    "GenericWorldSituatedRequest",
    "GenericWorldSituatedReceipt",
    "GenericWorldSituatedResult",
    "serve_generic_world_situated_possibility",
    "verify_generic_world_situated_replay",
]
