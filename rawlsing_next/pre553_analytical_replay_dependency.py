"""C1-03R analytical replay-grade and dependency-closure adapter (AT18/AT19).

This module is a *bounded adapter* over already-accepted owners. It is explicitly
**not** a second authority-maintenance owner:

* invalidation/dependency closure is delegated to
  ``rawlsing_next.pre553_authority_maintenance.SemanticDeterminantGraph`` and
  ``AuthorityInvalidationReceipt``;
* replay-grade claims are emitted as the existing public ``ReplayReceipt@1.0.0``
  family and audited against ``pre553_replay_audit`` closure law;
* the analytical product identity itself always comes from the accepted
  ``compose_positioned_subject_possibility`` owner, never from this module.

What this module owns is narrow: naming the replay *grade* of an analytical replay
claim, and registering exact analytical product dependencies so that a single exact
determinant mutation invalidates exactly the registered affected products.

It never chooses latest/default authority, never infers semantic lifecycle meaning,
never invents dependencies from object similarity, and never mutates current selection
outside the existing owner.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next.pre553_authority_maintenance import (
    AuthorityInvalidationReceipt,
    SemanticDeterminantGraph,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    ReplayReceipt,
    canonicalize,
    semantic_hash,
)

REPLAY_GRADE_CONTRACT_ID = "C1_03R_ANALYTICAL_REPLAY_GRADE@1"
DEPENDENCY_CONTRACT_ID = "C1_03R_ANALYTICAL_DEPENDENCY_CLOSURE@1"

#: Replay grades, weakest first. A claim may only ever assert the grade its actual
#: mechanism genuinely demonstrates; upgrading requires a stronger mechanism.
REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY = "HISTORICAL_EXPLANATION_ONLY"
REPLAY_GRADE_SERIALIZATION_REPLAY = "SERIALIZATION_REPLAY"
REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY = "FRESH_PROCESS_PRODUCT_REPLAY"
REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION = "FRESH_EMPIRICAL_RECOMPUTATION"

REPLAY_GRADES = (
    REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
    REPLAY_GRADE_SERIALIZATION_REPLAY,
    REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY,
    REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
)

GRADE_STRENGTH = {grade: index for index, grade in enumerate(REPLAY_GRADES)}

#: Actual replay mechanisms. Only a fresh-process mechanism may support a
#: fresh-process grade.
MECHANISM_HISTORICAL_NARRATION = "HISTORICAL_NARRATION"
MECHANISM_STORED_RECEIPT_DESERIALIZATION = "STORED_RECEIPT_DESERIALIZATION"
MECHANISM_STORED_PRODUCT_DESERIALIZATION = "STORED_PRODUCT_DESERIALIZATION"
MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER = "FRESH_PROCESS_ACCEPTED_PRODUCER"

REPLAY_MECHANISMS = (
    MECHANISM_HISTORICAL_NARRATION,
    MECHANISM_STORED_RECEIPT_DESERIALIZATION,
    MECHANISM_STORED_PRODUCT_DESERIALIZATION,
    MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER,
)

#: The strongest grade each mechanism can honestly support.
MECHANISM_MAX_GRADE = {
    MECHANISM_HISTORICAL_NARRATION: REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
    MECHANISM_STORED_RECEIPT_DESERIALIZATION: REPLAY_GRADE_SERIALIZATION_REPLAY,
    MECHANISM_STORED_PRODUCT_DESERIALIZATION: REPLAY_GRADE_SERIALIZATION_REPLAY,
    MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER: REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
}

FRESH_PROCESS_MECHANISMS = frozenset({MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER})

#: Grades that assert fresh empirical recomputation happened.
FRESH_GRADES = frozenset(
    {REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY, REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION}
)


class AnalyticalReplayDependencyError(Pre553IntegrityError):
    """Typed C1-03R adapter failure; owner-law errors are never laundered."""


class ReplayGradeOverclaim(AnalyticalReplayDependencyError):
    code = "REPLAY_GRADE_OVERCLAIM"


class MissingExactDeterminant(AnalyticalReplayDependencyError):
    code = "MISSING_EXACT_DETERMINANT"


class DependencyClosureFailure(AnalyticalReplayDependencyError):
    code = "DEPENDENCY_CLOSURE_FAILURE"


class MissingCrossOwnerEdge(DependencyClosureFailure):
    code = "MISSING_CROSS_OWNER_EDGE"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AnalyticalReplayDependencyError(f"{name} must be non-empty string")
    return value.strip()


def _refs(values: Iterable[ExactRef | Mapping[str, Any]]) -> tuple[ExactRef, ...]:
    from rawlsing_next.pre553_empirical_objects import exact_ref

    return tuple(sorted({exact_ref(v, "ref") for v in values}, key=lambda r: r.key))


def _auths(values: Iterable[AuthorityRef | Mapping[str, Any]]) -> tuple[AuthorityRef, ...]:
    from rawlsing_next.pre553_empirical_objects import authority_ref

    return tuple(
        sorted({authority_ref(v, "authority_ref") for v in values}, key=lambda r: r.key)
    )


@dataclass(frozen=True)
class AnalyticalReplayClaim:
    """One exact analytical replay claim at an explicitly declared grade.

    The claim binds exact retained determinants, the exact producer path, exact
    authority refs, the expected output identity, the actual replay mechanism and the
    limitations of the grade being asserted.
    """

    claim_id: str
    replayed_product_ref: ExactRef
    retained_determinant_refs: tuple[ExactRef, ...]
    producer_route: str
    producer_path: str
    authority_refs: tuple[AuthorityRef, ...]
    expected_output_identity_hash: str
    actual_replay_mechanism: str
    replay_grade: str
    limitations: tuple[str, ...]
    replay_protocol_ref: ExactRef
    deterministic_order_or_tie_rule_refs: tuple[ExactRef, ...]
    replay_state: str = "REPLAY_VERIFIED"

    def __post_init__(self) -> None:
        object.__setattr__(self, "claim_id", _text(self.claim_id, "claim_id"))
        object.__setattr__(self, "producer_route", _text(self.producer_route, "producer_route"))
        object.__setattr__(self, "producer_path", _text(self.producer_path, "producer_path"))
        if not isinstance(self.replayed_product_ref, ExactRef):
            raise AnalyticalReplayDependencyError("replayed_product_ref must be ExactRef")
        object.__setattr__(
            self,
            "retained_determinant_refs",
            _refs(self.retained_determinant_refs),
        )
        if not self.retained_determinant_refs:
            raise MissingExactDeterminant(
                "MISSING_EXACT_DETERMINANT: a replay claim requires exact retained determinants"
            )
        object.__setattr__(self, "authority_refs", _auths(self.authority_refs))
        if not self.authority_refs:
            raise MissingExactDeterminant(
                "MISSING_EXACT_DETERMINANT: a replay claim requires exact authority refs"
            )
        if len(self.expected_output_identity_hash) != 64:
            raise AnalyticalReplayDependencyError(
                "expected_output_identity_hash must be sha256"
            )
        if self.actual_replay_mechanism not in REPLAY_MECHANISMS:
            raise AnalyticalReplayDependencyError(
                f"unknown replay mechanism {self.actual_replay_mechanism!r}"
            )
        if self.replay_grade not in REPLAY_GRADES:
            raise AnalyticalReplayDependencyError(
                f"unknown replay grade {self.replay_grade!r}"
            )
        if not isinstance(self.replay_protocol_ref, ExactRef):
            raise AnalyticalReplayDependencyError("replay_protocol_ref must be ExactRef")
        object.__setattr__(
            self,
            "deterministic_order_or_tie_rule_refs",
            _refs(self.deterministic_order_or_tie_rule_refs),
        )
        object.__setattr__(self, "limitations", tuple(str(x) for x in self.limitations))
        self.assert_grade_is_honest()

    def assert_grade_is_honest(self) -> None:
        """Fail closed if the claimed grade exceeds what the mechanism demonstrates."""

        max_grade = MECHANISM_MAX_GRADE[self.actual_replay_mechanism]
        if GRADE_STRENGTH[self.replay_grade] > GRADE_STRENGTH[max_grade]:
            raise ReplayGradeOverclaim(
                "REPLAY_GRADE_OVERCLAIM: mechanism "
                f"{self.actual_replay_mechanism!r} can support at most {max_grade!r}, "
                f"not {self.replay_grade!r}"
            )
        if (
            self.replay_grade in FRESH_GRADES
            and self.actual_replay_mechanism not in FRESH_PROCESS_MECHANISMS
        ):
            raise ReplayGradeOverclaim(
                "REPLAY_GRADE_OVERCLAIM: a fresh-process grade requires a fresh-process "
                "accepted-producer mechanism"
            )

    def material(self) -> Mapping[str, Any]:
        return {
            "contract_id": REPLAY_GRADE_CONTRACT_ID,
            "claim_id": self.claim_id,
            "replayed_product_ref": self.replayed_product_ref.as_dict(),
            "retained_determinant_refs": [x.as_dict() for x in self.retained_determinant_refs],
            "producer_route": self.producer_route,
            "producer_path": self.producer_path,
            "authority_refs": [x.as_dict() for x in self.authority_refs],
            "expected_output_identity_hash": self.expected_output_identity_hash,
            "actual_replay_mechanism": self.actual_replay_mechanism,
            "replay_grade": self.replay_grade,
            "limitations": list(self.limitations),
            "replay_protocol_ref": self.replay_protocol_ref.as_dict(),
            "deterministic_order_or_tie_rule_refs": [
                x.as_dict() for x in self.deterministic_order_or_tie_rule_refs
            ],
            "replay_state": self.replay_state,
        }

    @property
    def claim_hash(self) -> str:
        return semantic_hash(self.material())

    def to_replay_receipt(self) -> ReplayReceipt:
        """Emit the claim as the existing public ReplayReceipt family.

        No new object family is invented: the grade and mechanism travel as explicit
        extra semantic material inside the accepted receipt family.
        """

        return ReplayReceipt(
            typed_state=self.replay_state,
            authority_snapshot_refs=self.authority_refs,
            dependency_refs=(self.replayed_product_ref,),
            producer_replay_locator_or_reference_root=self.replay_protocol_ref,
            replayed_object_ref=self.replayed_product_ref,
            input_content_identity_refs=self.retained_determinant_refs,
            authority_snapshot_refs_replayed=self.authority_refs,
            producer_or_algorithm_identity=self.producer_path,
            canonical_semantic_projection_hash=self.expected_output_identity_hash,
            deterministic_order_or_tie_rule_refs=self.deterministic_order_or_tie_rule_refs,
            replay_protocol_ref=self.replay_protocol_ref,
            replay_state=self.replay_state,
            replay_grade=self.replay_grade,
            actual_replay_mechanism=self.actual_replay_mechanism,
            replay_grade_contract_id=REPLAY_GRADE_CONTRACT_ID,
            producer_route=self.producer_route,
            claim_hash=self.claim_hash,
            limitations=list(self.limitations),
        )


@dataclass(frozen=True)
class ReplayGradeAssertion:
    """Result of checking an observed replay identity against a declared claim."""

    claim_hash: str
    replay_grade: str
    actual_replay_mechanism: str
    expected_output_identity_hash: str
    observed_output_identity_hash: str
    identity_reproduced: bool
    asserted_grade_is_honest: bool
    limitations: tuple[str, ...]

    def material(self) -> Mapping[str, Any]:
        return {
            "contract_id": REPLAY_GRADE_CONTRACT_ID,
            "claim_hash": self.claim_hash,
            "replay_grade": self.replay_grade,
            "actual_replay_mechanism": self.actual_replay_mechanism,
            "expected_output_identity_hash": self.expected_output_identity_hash,
            "observed_output_identity_hash": self.observed_output_identity_hash,
            "identity_reproduced": self.identity_reproduced,
            "asserted_grade_is_honest": self.asserted_grade_is_honest,
            "limitations": list(self.limitations),
        }


def assert_replay_claim(
    claim: AnalyticalReplayClaim,
    *,
    observed_output_identity_hash: str,
) -> ReplayGradeAssertion:
    """Fail closed if a claim is dishonest or its identity does not reproduce."""

    claim.assert_grade_is_honest()
    if len(observed_output_identity_hash) != 64:
        raise AnalyticalReplayDependencyError("observed output identity must be sha256")
    reproduced = observed_output_identity_hash == claim.expected_output_identity_hash
    if not reproduced:
        raise AnalyticalReplayDependencyError(
            "replay identity did not reproduce at the declared grade: "
            f"expected {claim.expected_output_identity_hash}, observed {observed_output_identity_hash}"
        )
    return ReplayGradeAssertion(
        claim_hash=claim.claim_hash,
        replay_grade=claim.replay_grade,
        actual_replay_mechanism=claim.actual_replay_mechanism,
        expected_output_identity_hash=claim.expected_output_identity_hash,
        observed_output_identity_hash=observed_output_identity_hash,
        identity_reproduced=True,
        asserted_grade_is_honest=True,
        limitations=claim.limitations,
    )


@dataclass(frozen=True)
class AnalyticalProductRegistration:
    """One exact analytical product registered with its real determinants.

    ``determinant_authority_refs`` are authority refs the product genuinely consumes:
    they must actually appear in the product's own composition authority refs, or be
    demonstrated to change the product's identity. Registration never infers a
    dependency from object similarity.
    """

    product_ref: ExactRef
    product_identity_hash: str
    determinant_authority_refs: tuple[AuthorityRef, ...]
    determinant_exact_refs: tuple[ExactRef, ...]
    consumer_lane_authority_refs: tuple[AuthorityRef, ...] = ()
    dependency_edges_from: tuple[ExactRef, ...] = ()
    recompose: Callable[[tuple[AuthorityRef, ...]], ExactRef] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.product_ref, ExactRef):
            raise AnalyticalReplayDependencyError("product_ref must be ExactRef")
        if len(self.product_identity_hash) != 64:
            raise AnalyticalReplayDependencyError("product_identity_hash must be sha256")
        object.__setattr__(
            self,
            "determinant_authority_refs",
            _auths(self.determinant_authority_refs),
        )
        object.__setattr__(
            self,
            "consumer_lane_authority_refs",
            _auths(self.consumer_lane_authority_refs),
        )
        object.__setattr__(
            self, "determinant_exact_refs", _refs(self.determinant_exact_refs)
        )
        object.__setattr__(
            self, "dependency_edges_from", _refs(self.dependency_edges_from)
        )
        if not self.determinant_authority_refs and not self.consumer_lane_authority_refs:
            raise MissingExactDeterminant(
                "MISSING_EXACT_DETERMINANT: a registration requires at least one exact "
                "determinant authority ref"
            )

    @property
    def all_determinant_authority_refs(self) -> tuple[AuthorityRef, ...]:
        return _auths(
            (*self.determinant_authority_refs, *self.consumer_lane_authority_refs)
        )


class AnalyticalDependencyRegistry:
    """Registers exact analytical products into the existing determinant-graph owner."""

    def __init__(self) -> None:
        self._registrations: dict[str, AnalyticalProductRegistration] = {}

    @property
    def registrations(self) -> tuple[AnalyticalProductRegistration, ...]:
        return tuple(
            self._registrations[key] for key in sorted(self._registrations)
        )

    def register(self, registration: AnalyticalProductRegistration) -> None:
        key = registration.product_ref.key
        if key in self._registrations:
            raise AnalyticalReplayDependencyError(
                "product already registered with exact determinants"
            )
        self._registrations[key] = registration

    def build_graph(
        self, *, omit_authority_edges: Iterable[tuple[AuthorityRef, ExactRef]] = ()
    ) -> SemanticDeterminantGraph:
        """Build the existing owner's graph from real registrations.

        ``omit_authority_edges`` exists only to construct a deliberately incomplete
        cross-owner graph for the mandatory AT19 missing-edge hostile. It is never used
        on a lawful closure path.
        """

        omitted = {
            (_auth_key(a), _ref_key(d)) for a, d in omit_authority_edges
        }
        authority_edges: list[tuple[AuthorityRef, ExactRef]] = []
        dependency_edges: list[tuple[ExactRef, ExactRef]] = []
        known: list[ExactRef] = []
        for registration in self.registrations:
            known.append(registration.product_ref)
            for authority in registration.all_determinant_authority_refs:
                if (authority.key, registration.product_ref.key) in omitted:
                    continue
                authority_edges.append((authority, registration.product_ref))
            for parent in registration.dependency_edges_from:
                dependency_edges.append((parent, registration.product_ref))
        return SemanticDeterminantGraph(
            authority_edges=tuple(authority_edges),
            dependency_edges=tuple(dependency_edges),
            known_dependent_refs=tuple(known),
        )


def _auth_key(value: Any) -> str:
    from rawlsing_next.pre553_empirical_objects import authority_ref

    return authority_ref(value, "authority_ref").key


def _ref_key(value: Any) -> str:
    from rawlsing_next.pre553_empirical_objects import exact_ref

    return exact_ref(value, "ref").key


@dataclass(frozen=True)
class AnalyticalInvalidationOutcome:
    """Selective invalidation outcome over real analytical products."""

    changed_determinant_refs: tuple[AuthorityRef, ...]
    invalidation_receipt: AuthorityInvalidationReceipt
    recompiled_identity_hashes: Mapping[str, str]
    noncurrent_product_refs: tuple[ExactRef, ...]
    closure_verified: bool

    def material(self) -> Mapping[str, Any]:
        return {
            "contract_id": DEPENDENCY_CONTRACT_ID,
            "changed_determinant_refs": [x.as_dict() for x in self.changed_determinant_refs],
            "invalidation_receipt": self.invalidation_receipt.as_dict(),
            "recompiled_identity_hashes": dict(sorted(self.recompiled_identity_hashes.items())),
            "noncurrent_product_refs": [x.as_dict() for x in self.noncurrent_product_refs],
            "closure_verified": self.closure_verified,
        }


def invalidate_for_changed_determinants(
    *,
    registry: AnalyticalDependencyRegistry,
    changed_determinant_refs: Iterable[AuthorityRef | Mapping[str, Any]],
    graph: SemanticDeterminantGraph | None = None,
) -> AnalyticalInvalidationOutcome:
    """Mutate one exact determinant and invalidate exactly the registered affected set.

    Closure law (delegated to ``SemanticDeterminantGraph``):

    * affected  = products reached from the changed determinant over registered edges;
    * unaffected = registered products not reached;
    * every affected product must recompile through its own accepted composition
      entry point and produce a *new* exact identity;
    * an affected product with no lawful replacement is recorded noncurrent instead of
      being silently treated as current.
    """

    changed = _auths(changed_determinant_refs)
    if not changed:
        raise AnalyticalReplayDependencyError("at least one changed determinant is required")
    active_graph = graph if graph is not None else registry.build_graph()
    affected = active_graph.affected(changed)
    unaffected = active_graph.unaffected(affected)
    affected_keys = {ref.key for ref in affected}

    registrations = {r.product_ref.key: r for r in registry.registrations}
    pairs: list[tuple[ExactRef, ExactRef]] = []
    recomposed: dict[str, str] = {}
    noncurrent: list[ExactRef] = []
    for ref in affected:
        registration = registrations.get(ref.key)
        if registration is None or registration.recompose is None:
            # No lawful replacement is available: record the explicit noncurrent state
            # rather than claiming a fabricated replacement identity.
            noncurrent.append(ref)
            continue
        new_ref = registration.recompose(changed)
        if not isinstance(new_ref, ExactRef):
            raise AnalyticalReplayDependencyError(
                "recompiler must return an exact ref for the recompiled product"
            )
        if new_ref == ref:
            raise DependencyClosureFailure(
                "DEPENDENCY_CLOSURE_FAILURE: an affected product recompiled to the same "
                "identity; the determinant mutation did not reach the product"
            )
        pairs.append((ref, new_ref))
        recomposed[new_ref.key] = semantic_hash(
            {
                "product_ref": new_ref.as_dict(),
                "changed_determinant_refs": [x.as_dict() for x in changed],
            }
        )

    if noncurrent:
        # An explicit noncurrent state is lawful; a *fabricated* pair is not. Build the
        # receipt over the pairs we genuinely have by covering remaining affected
        # products with their explicit noncurrent sentinel identity.
        for ref in noncurrent:
            sentinel = ExactRef(
                "C1_03R_NONCURRENT_PRODUCT",
                f"urn:rawlsing:c1_03r:noncurrent:sha256:{semantic_hash({'product_ref': ref.as_dict(), 'state': 'NO_CURRENT'})}",
                semantic_hash({"product_ref": ref.as_dict(), "state": "NO_CURRENT"}),
            )
            pairs.append((ref, sentinel))

    receipt = AuthorityInvalidationReceipt(
        changed_authority_refs=changed,
        affected_dependent_refs=affected,
        unaffected_dependent_refs=unaffected,
        recompilation_pairs=tuple(pairs),
    )
    return AnalyticalInvalidationOutcome(
        changed_determinant_refs=changed,
        invalidation_receipt=receipt,
        recompiled_identity_hashes=recomposed,
        noncurrent_product_refs=tuple(noncurrent),
        closure_verified=True,
    )


def assert_closure_against_actual_identity_change(
    *,
    registry: AnalyticalDependencyRegistry,
    changed_determinant_refs: Iterable[AuthorityRef | Mapping[str, Any]],
    graph: SemanticDeterminantGraph | None = None,
) -> None:
    """Hostile closure check: every product whose identity actually changes must be
    registered as affected.

    This is the missing-cross-owner-edge detector. A product whose bytes remain present
    but whose *identity genuinely depends* on the changed determinant, while no
    registered edge connects them, is a failed closure witness: cache/object presence
    cannot restore its authority.
    """

    changed = _auths(changed_determinant_refs)
    active_graph = graph if graph is not None else registry.build_graph()
    affected_keys = {ref.key for ref in active_graph.affected(changed)}
    missing: list[str] = []
    for registration in registry.registrations:
        if registration.product_ref.key in affected_keys:
            continue
        if registration.recompose is None:
            continue
        try:
            new_ref = registration.recompose(changed)
        except Exception as exc:  # an unavailable recomputation is not an edge proof
            raise MissingCrossOwnerEdge(
                "MISSING_CROSS_OWNER_EDGE: a registered product could not be recomputed "
                f"to test closure: {exc}"
            ) from exc
        if new_ref != registration.product_ref:
            missing.append(registration.product_ref.key)
    if missing:
        raise MissingCrossOwnerEdge(
            "MISSING_CROSS_OWNER_EDGE: closure claim failed; these registered products "
            "genuinely reidentify under the changed determinant but no registered "
            f"cross-owner edge reaches them: {sorted(missing)!r}"
        )


__all__ = [
    "REPLAY_GRADE_CONTRACT_ID",
    "DEPENDENCY_CONTRACT_ID",
    "REPLAY_GRADES",
    "GRADE_STRENGTH",
    "REPLAY_MECHANISMS",
    "MECHANISM_MAX_GRADE",
    "FRESH_PROCESS_MECHANISMS",
    "FRESH_GRADES",
    "REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY",
    "REPLAY_GRADE_SERIALIZATION_REPLAY",
    "REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY",
    "REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION",
    "MECHANISM_HISTORICAL_NARRATION",
    "MECHANISM_STORED_RECEIPT_DESERIALIZATION",
    "MECHANISM_STORED_PRODUCT_DESERIALIZATION",
    "MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER",
    "AnalyticalReplayDependencyError",
    "ReplayGradeOverclaim",
    "MissingExactDeterminant",
    "DependencyClosureFailure",
    "MissingCrossOwnerEdge",
    "AnalyticalReplayClaim",
    "ReplayGradeAssertion",
    "assert_replay_claim",
    "AnalyticalProductRegistration",
    "AnalyticalDependencyRegistry",
    "AnalyticalInvalidationOutcome",
    "invalidate_for_changed_determinants",
    "assert_closure_against_actual_identity_change",
]
