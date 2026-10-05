"""C1-03R analytical replay-grade and dependency-closure adapter (AT18/AT19).

Owner-closure corrected (HQ149). This module is a *bounded adapter* over
already-accepted owners. It is explicitly **not** a lifecycle owner:

* the analytical dependency transition (affected/unaffected computation, recompiler
  invocation, and receipt construction) is performed by the accepted
  ``AuthorityMaintenanceExecutor.promote_current`` / ``rollback_current``;
* this adapter never computes affected/unaffected sets, never calls a recompiler on its
  own initiative, and never constructs an ``AuthorityInvalidationReceipt``;
* replay claims are emitted as the existing public ``ReplayReceipt@1.0.0`` family.

What it owns is narrow: naming the replay *grade* of an analytical replay claim, and
registering exact analytical products with the determinants they **actually consumed**
so the owner's graph can lawfully reach them.

Registration binds only consumed determinants. A revised/new authority is never
pre-registered as a determinant of a product produced before it; the revision enters
only through the owner's governed promotion transition (whose changed-authority set
already contains both the prior and the successor revision).

Known owner gap (see the correction return for the executable counterexample):
``AuthorityInvalidationReceipt`` requires ``recompilation_pairs`` to cover exactly the
affected dependent set, and the owner's recompilation law requires every affected
dependent to move to a *new* exact ref. A genuinely affected product with no lawful
replacement therefore has no lawful representation in the current owner contract. This
adapter refuses to fabricate one and raises
``NoLawfulReplacementRepresentable`` instead.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next.pre553_authority_maintenance import (
    AuthorityInvalidationReceipt,
    AuthorityMaintenanceError,
    DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT,
    DEPENDENT_LIFECYCLE_NOT_GOVERNED,
    Recompiler,
    SemanticDeterminantGraph,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    ReplayReceipt,
    semantic_hash,
)

REPLAY_GRADE_CONTRACT_ID = "C1_03R_ANALYTICAL_REPLAY_GRADE@1"
DEPENDENCY_CONTRACT_ID = "C1_03R_ANALYTICAL_DEPENDENCY_CLOSURE@1"

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

MECHANISM_MAX_GRADE = {
    MECHANISM_HISTORICAL_NARRATION: REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
    MECHANISM_STORED_RECEIPT_DESERIALIZATION: REPLAY_GRADE_SERIALIZATION_REPLAY,
    MECHANISM_STORED_PRODUCT_DESERIALIZATION: REPLAY_GRADE_SERIALIZATION_REPLAY,
    MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER: REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
}

FRESH_PROCESS_MECHANISMS = frozenset({MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER})

FRESH_GRADES = frozenset(
    {REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY, REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION}
)

#: Fields that must never appear in a fresh-runner *input* artifact: they are answers.
FORBIDDEN_RUNNER_INPUT_FIELDS = frozenset(
    {
        "expected_output_identity",
        "expected_composed_result_identity_hash",
        "composed_result_identity_hash",
        "producer_fact_ref",
        "evidence_ref",
        "evidence_ref_or_null",
        "consumer_result_hash",
        "consumer_result_hash_or_null",
        "raw_denominator_support",
        "complete_cell_geometry",
        "geometry",
        "exact_fraction",
        "cell_numerators",
        "oracle",
    }
)


class AnalyticalReplayDependencyError(Pre553IntegrityError):
    """Typed C1-03R adapter failure; owner-law errors are never laundered."""


class ReplayGradeOverclaim(AnalyticalReplayDependencyError):
    code = "REPLAY_GRADE_OVERCLAIM"


class MissingExactDeterminant(AnalyticalReplayDependencyError):
    code = "MISSING_EXACT_DETERMINANT"


class RunnerInputCarriesAnswer(AnalyticalReplayDependencyError):
    code = "RUNNER_INPUT_CARRIES_ANSWER"


class MissingCrossOwnerEdge(AnalyticalReplayDependencyError):
    code = "MISSING_CROSS_OWNER_EDGE"


class NoLawfulReplacementRepresentable(AnalyticalReplayDependencyError):
    """No recomposition path is registered and no explicit absence was declared."""


class ExplicitNoncurrentDependent(AnalyticalReplayDependencyError):
    """The lifecycle owner recorded this dependent as noncurrent.

    The historical exact artifact remains addressable; it simply may not be served
    as current under the governing release. Cache or object presence does not
    restore currentness.
    """
    """Owner gap: the current lifecycle owner cannot lawfully represent this case."""

    code = "NO_LAWFUL_REPLACEMENT_REPRESENTABLE"


class OwnerUnknownDependent(AnalyticalReplayDependencyError):
    """The lifecycle owner does not know this dependent at all.

    This is the narrowest fail-closed answer to an unknown ref: it is not a
    noncurrent outcome, because the owner never recorded one, and it is certainly
    not CURRENT. The owner simply has no currentness to report for a ref absent
    from its own known dependent set. Cache or object presence cannot supply one.
    """

    code = "OWNER_UNKNOWN_DEPENDENT"


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


# --------------------------------------------------------------------------
# AT18 - replay grade
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class AnalyticalReplayClaim:
    """One exact analytical replay claim at an explicitly declared grade."""

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
            self, "retained_determinant_refs", _refs(self.retained_determinant_refs)
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
            raise AnalyticalReplayDependencyError(f"unknown replay grade {self.replay_grade!r}")
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
    claim: AnalyticalReplayClaim, *, observed_output_identity_hash: str
) -> ReplayGradeAssertion:
    """Fail closed if a claim is dishonest or its identity does not reproduce.

    The *expected* identity lives on the oracle side (here), never in the fresh
    runner's input artifact.
    """

    claim.assert_grade_is_honest()
    if len(observed_output_identity_hash) != 64:
        raise AnalyticalReplayDependencyError("observed output identity must be sha256")
    if observed_output_identity_hash != claim.expected_output_identity_hash:
        raise AnalyticalReplayDependencyError(
            "replay identity did not reproduce at the declared grade: "
            f"expected {claim.expected_output_identity_hash}, "
            f"observed {observed_output_identity_hash}"
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


def assert_runner_input_carries_no_answer(determinants: Mapping[str, Any]) -> None:
    """Fail closed if a fresh-runner input artifact carries any expected answer."""

    def walk(node: Any, path: str) -> None:
        if isinstance(node, Mapping):
            for key, value in node.items():
                if str(key) in FORBIDDEN_RUNNER_INPUT_FIELDS:
                    raise RunnerInputCarriesAnswer(
                        "RUNNER_INPUT_CARRIES_ANSWER: runner input must contain only "
                        f"retained determinants, but carries {path}{key!r}"
                    )
                walk(value, f"{path}{key}.")
        elif isinstance(node, (list, tuple)):
            for index, value in enumerate(node):
                walk(value, f"{path}{index}.")

    walk(determinants, "")


# --------------------------------------------------------------------------
# AT19 - analytical dependency registration (consumed determinants only)
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class AnalyticalProductRegistration:
    """One exact analytical product registered with the determinants it consumed.

    ``determinant_authority_refs`` must be authorities the product genuinely consumed at
    production time. A future/revised authority must never appear here; it enters only
    through the owner's governed promotion transition.
    """

    product_ref: ExactRef
    product_identity_hash: str
    determinant_authority_refs: tuple[AuthorityRef, ...]
    determinant_exact_refs: tuple[ExactRef, ...] = ()
    dependency_edges_from: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.product_ref, ExactRef):
            raise AnalyticalReplayDependencyError("product_ref must be ExactRef")
        if len(self.product_identity_hash) != 64:
            raise AnalyticalReplayDependencyError("product_identity_hash must be sha256")
        object.__setattr__(
            self, "determinant_authority_refs", _auths(self.determinant_authority_refs)
        )
        object.__setattr__(self, "determinant_exact_refs", _refs(self.determinant_exact_refs))
        object.__setattr__(self, "dependency_edges_from", _refs(self.dependency_edges_from))
        if not self.determinant_authority_refs:
            raise MissingExactDeterminant(
                "MISSING_EXACT_DETERMINANT: a registration requires at least one exact "
                "consumed determinant authority ref"
            )


class AnalyticalDependencyRegistry:
    """Registers exact analytical products into the existing determinant-graph owner."""

    def __init__(self) -> None:
        self._registrations: dict[str, AnalyticalProductRegistration] = {}

    @property
    def registrations(self) -> tuple[AnalyticalProductRegistration, ...]:
        return tuple(self._registrations[key] for key in sorted(self._registrations))

    def register(self, registration: AnalyticalProductRegistration) -> None:
        key = registration.product_ref.key
        if key in self._registrations:
            raise AnalyticalReplayDependencyError(
                "product already registered with exact determinants"
            )
        self._registrations[key] = registration

    def build_graph(
        self, *, omit_authority_edges: Iterable[tuple[Any, Any]] = ()
    ) -> SemanticDeterminantGraph:
        """Build the owner's graph from consumed determinants only.

        ``omit_authority_edges`` exists solely to construct the deliberately incomplete
        cross-owner graph for the mandatory missing-edge hostile.
        """

        from rawlsing_next.pre553_empirical_objects import authority_ref, exact_ref

        omitted = {
            (authority_ref(a, "authority_ref").key, exact_ref(d, "ref").key)
            for a, d in omit_authority_edges
        }
        authority_edges: list[tuple[AuthorityRef, ExactRef]] = []
        dependency_edges: list[tuple[ExactRef, ExactRef]] = []
        known: list[ExactRef] = []
        for registration in self.registrations:
            known.append(registration.product_ref)
            for authority in registration.determinant_authority_refs:
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


@dataclass(frozen=True)
class OwnerDependencyInvalidationOutcome:
    """Outcome of an owner-driven analytical dependency transition."""

    release_ref: ExactRef
    invalidation_receipt: AuthorityInvalidationReceipt
    changed_authority_refs: tuple[AuthorityRef, ...]
    recomposed_products: tuple[tuple[ExactRef, ExactRef], ...]

    def material(self) -> Mapping[str, Any]:
        return {
            "contract_id": DEPENDENCY_CONTRACT_ID,
            "release_ref": self.release_ref.as_dict(),
            "invalidation_receipt": self.invalidation_receipt.as_dict(),
            "changed_authority_refs": [x.as_dict() for x in self.changed_authority_refs],
            "recomposed_products": [
                {"old_ref": old.as_dict(), "new_ref": new.as_dict()}
                for old, new in self.recomposed_products
            ],
            "noncurrent_dependents": [
                row.as_dict() for row in self.invalidation_receipt.noncurrent_dependents
            ],
            "lifecycle_performed_by": "AuthorityMaintenanceExecutor.promote_current",
        }


def resolve_current_analytical_product(
    *,
    executor: Any,
    dependent_ref: ExactRef,
) -> Mapping[str, Any]:
    """Resolve one registered dependent through the OWNER's lifecycle state.

    This is the analytical current-product path. It never infers currentness from
    object or cache presence: it asks the accepted lifecycle owner, which is the only
    party that computes lifecycle outcomes.

    Returns a mapping with ``lifecycle_state`` and, for a replaced dependent, the
    exact ``current_replacement_ref``. Raises :class:`ExplicitNoncurrentDependent`
    when the owner recorded an explicit noncurrent outcome, so a stale historical
    product can never be served as current. Raises :class:`OwnerUnknownDependent`
    when the owner does not know the ref at all, so absence of a recorded transition
    can never be laundered into currentness.
    """
    status = dict(executor.dependent_lifecycle_status(dependent_ref))
    if status["lifecycle_state"] == DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT:
        raise ExplicitNoncurrentDependent(
            "the lifecycle owner recorded an explicit noncurrent outcome for "
            f"{dependent_ref.key} (disposition={status['disposition']!r}, "
            f"reason_code={status['reason_code']!r}, "
            f"governing_release={status['governing_release_ref']}); the historical exact "
            "artifact remains addressable but may not be served as current, and cached "
            "bytes do not restore currentness"
        )
    if status["lifecycle_state"] == DEPENDENT_LIFECYCLE_NOT_GOVERNED:
        raise OwnerUnknownDependent(
            "the lifecycle owner does not know this dependent: "
            f"{dependent_ref.key} is absent from the owner's known dependent set, so no "
            "governed transition has ever spoken about it. The owner has no currentness "
            "to report and will not infer one from the absence of a recorded outcome; "
            "cached or resident bytes do not make it current either"
        )
    return status


def build_owner_recompiler(
    *,
    executor: Any,
    registry: AnalyticalDependencyRegistry,
    recompose: Mapping[str, Callable[[ExactRef, AuthorityRef], ExactRef]],
) -> Recompiler:
    """Build the ``Recompiler`` the accepted lifecycle owner invokes.

    The owner calls ``recompiler(affected_product_ref, changed_authority_refs)``. For
    each affected *product*, the adapter resolves the lawful successor of exactly the
    determinants that product consumed and that the owner reports as changed. It never
    guesses a successor from tuple position, and it never treats an unaffected authority
    as if it had been replaced.
    """

    registrations = {r.product_ref.key: r for r in registry.registrations}

    def recompiler(
        affected_ref: ExactRef, changed: tuple[AuthorityRef, ...]
    ) -> ExactRef:
        registration = registrations.get(affected_ref.key)
        if registration is None:
            raise AuthorityMaintenanceError(
                "the owner reports an affected dependent that is not a registered "
                f"analytical product: {affected_ref.key}"
            )
        recomposer = recompose.get(affected_ref.key)
        if recomposer is None:
            raise NoLawfulReplacementRepresentable(
                "NO_LAWFUL_REPLACEMENT_REPRESENTABLE: the accepted lifecycle owner's "
                "receipt requires a replacement for every affected dependent, but no "
                "analytical recomposition path is registered for affected product "
                f"{affected_ref.key}. The current owner contract has no representation "
                "for an affected product with no lawful replacement, and this adapter "
                "will not fabricate one."
            )
        # Which EXACT consumed prior authority ref did the owner actually change?
        #
        # Astra's defect was selecting by the consumed ``(authority_id,
        # authority_version)`` tuple. In a v1 -> v2 promotion the owner reports
        # ``changed = (prior_v1, selected_v2)``, so that filter matched the PRIOR
        # ref and handed it to recomposition as though it were the successor.
        #
        # The correct resolution is by exact identity, in two steps:
        #   1. find the consumed ref that is itself present in the owner's changed
        #      set -- that is the exact prior determinant that moved;
        #   2. resolve the one OTHER changed ref sharing that authority identity --
        #      that is the governed successor the same transition selected.
        # Never by tuple position, never by version label alone.
        changed_keys = {ref.key for ref in changed}
        consumed_prior = [
            ref
            for ref in registration.determinant_authority_refs
            if ref.key in changed_keys
        ]
        if len(consumed_prior) != 1:
            raise AuthorityMaintenanceError(
                "an affected analytical product must have exactly one of its consumed "
                "determinant refs present in the owner's changed set, found "
                f"{len(consumed_prior)} for {affected_ref.key}"
            )
        prior = consumed_prior[0]
        successors = [
            ref
            for ref in changed
            if ref.authority_id == prior.authority_id and ref.key != prior.key
        ]
        if len(successors) != 1:
            raise AuthorityMaintenanceError(
                "the governed transition must resolve exactly one successor authority "
                f"ref for identity {prior.authority_id!r} besides the consumed prior ref, "
                f"found {len(successors)} for {affected_ref.key}"
            )
        successor = successors[0]
        if successor == prior:
            raise AuthorityMaintenanceError(
                "the recomposition successor must differ from the consumed prior ref")
        # The successor must be an authority the owner actually knows, i.e. sealed and
        # registered. This is what forbids handing a recomposition a merely
        # well-formed or future authority ref.
        if not getattr(executor, "_known_authority_ref", None) or not executor._known_authority_ref(
            successor
        ):
            raise AuthorityMaintenanceError(
                "the resolved successor authority ref is not a registered owner "
                f"authority; future or unknown authority pre-binding is forbidden "
                f"({successor.key})"
            )
        # The recomposition path owns the new exact identity; it is handed the
        # affected product ref and the exact sealed/released successor authority ref.
        new_ref = recomposer(affected_ref, successor)
        if new_ref == affected_ref:
            raise AuthorityMaintenanceError(
                "affected dependent recompilation must produce a new exact ref"
            )
        return new_ref

    return recompiler


def transition_analytical_dependencies(
    *,
    executor: Any,
    registry: AnalyticalDependencyRegistry,
    seal_ref: ExactRef,
    selection_rule_ref: ExactRef,
    selection_attestation_ref: ExactRef,
    recompose: Mapping[str, Callable[[ExactRef, AuthorityRef], ExactRef]],
    noncurrent_dependents: Mapping[str, Any] | None = None,
) -> OwnerDependencyInvalidationOutcome:
    """Let the accepted lifecycle owner perform the analytical dependency transition.

    The owner computes affected/unaffected, invokes the recompiler, validates the
    outcome set, and constructs the ``AuthorityInvalidationReceipt``. This adapter
    supplies only the analytical recomposition functions plus any *explicitly
    grounded* absence declaration; it does not reproduce
    ``AuthorityMaintenanceExecutor._recompile`` semantics, does not compute the
    affected or unaffected set, and never builds the receipt.

    ``noncurrent_dependents`` maps a registered product ref key to a grounded
    ``NoncurrentDependentOutcome`` for a product the domain genuinely cannot rebuild.
    It is a declaration, not an inference: a product with neither a recomposition path
    nor an explicit grounded row still raises
    :class:`NoLawfulReplacementRepresentable`. A missing callback, a callback
    exception, and an unchanged-ref return all remain errors.
    """

    from rawlsing_next.pre553_empirical_objects import exact_ref

    executor_recompiler = build_owner_recompiler(
        executor=executor,
        registry=registry,
        recompose=recompose,
    )
    declared = {
        (value if isinstance(value, str) else exact_ref(value).key): row
        for value, row in dict(noncurrent_dependents or {}).items()
    }
    release = executor.promote_current(
        seal_ref,
        selection_rule_ref=selection_rule_ref,
        selection_attestation_ref=selection_attestation_ref,
        recompiler=executor_recompiler,
        noncurrent_outcomes=declared,
    )
    receipt = executor.invalidation_receipt_for_release(release.ref)
    return OwnerDependencyInvalidationOutcome(
        release_ref=exact_ref(release.ref, "release_ref"),
        invalidation_receipt=receipt,
        changed_authority_refs=_auths(receipt.changed_authority_refs),
        recomposed_products=tuple(receipt.recompilation_pairs),
    )


def assert_closure_covers_registered_products(
    *,
    outcome: OwnerDependencyInvalidationOutcome,
    registry: AnalyticalDependencyRegistry,
    recompose: Mapping[str, Callable[[ExactRef, AuthorityRef], ExactRef]],
    successor_authority: AuthorityRef,
) -> None:
    """Hostile closure check over the owner's own affected set.

    For every registered product the owner did *not* claim affected, recompose it under
    the successor authority. If its identity genuinely moves, the owner's affected set
    did not reach a real dependency: the closure witness is incomplete and object/cache
    presence cannot restore it.

    Callers must pass the lawful successor authority obtained from the owner.
    """

    affected = {ref.key for ref in outcome.invalidation_receipt.affected_dependent_refs}
    missing: list[str] = []
    for registration in registry.registrations:
        key = registration.product_ref.key
        if key in affected:
            continue
        recomposer = recompose.get(key)
        if recomposer is None:
            continue
        if recomposer(registration.product_ref, successor_authority) != (
            registration.product_ref
        ):
            missing.append(key)
    if missing:
        raise MissingCrossOwnerEdge(
            "MISSING_CROSS_OWNER_EDGE: closure claim failed; these registered products "
            "genuinely reidentify under the successor authority but the owner's affected "
            f"set does not reach them: {sorted(missing)!r}"
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
    "FORBIDDEN_RUNNER_INPUT_FIELDS",
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
    "RunnerInputCarriesAnswer",
    "MissingCrossOwnerEdge",
    "NoLawfulReplacementRepresentable",
    "AnalyticalReplayClaim",
    "ReplayGradeAssertion",
    "assert_replay_claim",
    "assert_runner_input_carries_no_answer",
    "AnalyticalProductRegistration",
    "AnalyticalDependencyRegistry",
    "OwnerDependencyInvalidationOutcome",
    "build_owner_recompiler",
    "transition_analytical_dependencies",
    "assert_closure_covers_registered_products",
]
