"""Retained GT2 -> N10E analytical preparation, not a counterfeit provider.

This module is deliberately a *preparation* owner-adapter, not a second
empirical engine and not an N10E provider.  It takes the exact retained GT2
query/fact from the fixed committed transport, reconstructs the exact retained
predicate identity, reuses the accepted Field Forge conditional-support owner
for the exact 6x6 count profile, and exposes the exact N10E determinants that
are present and the exact determinants that are absent.

It never opens source material, never reconstructs respondent values, never
invents a probability model, never creates ``PossibilitySliceEvidence`` and
never calls ``provide_empirical_possibility_slice`` or
``evaluate_positioned_subject_possibility``.  A caller that needs the accepted
N10E route is refused with a typed contract-gap error naming every absent
determinant.

The retained joint product is source-free and object-exact, but it is not a
sealed C11 repository with respondent preimages.  The accepted N10E direct route
re-executes I03 against such a repository, so the missing material is a real
contract boundary, not a formatting problem.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next.field_forge_conditional_support import (
    produce_exact_conditional_support_profile,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_repo_native_current_payload import (
    CURRENT_FACT_HASH,
    CURRENT_PREDICATE_HASH,
    CURRENT_QUERY_HASH,
    CURRENT_REPLAY_HASH,
    load_current_gt2_query_fact_from_committed_transport,
)
from rawlsing_next.wave1_gt12_i03_positive_facts import (
    FROZEN_Q86A_QIMPL,
    FROZEN_Q86B_QIMPL,
    FROZEN_RISK_SET_MEMBER_COUNT,
    FROZEN_R5_SOURCE_SHA256,
    reconstruct_gt2_risk_cohort_predicate,
)

PREPARATION_CONTRACT_ID = "RETAINED_GT2_N10E_ANALYTICAL_PREPARATION@1.0.0"
PREPARATION_STATE = "PREPARED_ONLY__N10E_PROVIDER_CONTRACT_BLOCKED"
N10E_PROVIDER_CALLABLE = (
    "rawlsing_next.pre553_empirical_possibility_provider."
    "provide_empirical_possibility_slice"
)
N10E_CONSUMER_CALLABLE = (
    "rawlsing_next.source_backed_positioned_subject_possibility."
    "evaluate_positioned_subject_possibility"
)
N10E_COMPOSER_CALLABLE = (
    "rawlsing_next.pre553_analytical_composition."
    "compose_positioned_subject_possibility"
)
FIELD_FORGE_CALLABLE = (
    "rawlsing_next.field_forge_conditional_support."
    "produce_exact_conditional_support_profile"
)

DETERMINANT_EXACT_RETAINED = "EXACT_RETAINED"
DETERMINANT_EXACT_RECONSTRUCTED = "EXACT_RECONSTRUCTED_FROM_RETAINED_REFS"
DETERMINANT_ABSENT_TRANSPORT = "ABSENT_FROM_RETAINED_TRANSPORT"
DETERMINANT_UNAVAILABLE_AUTHORITY = "UNAVAILABLE_OPERATION_SPECIFIC_AUTHORITY"

STRUCTURAL_PERMISSION_CEILING = "STRUCTURAL_MEDIATION_INPUT"


class RetainedGT2AnalyticalPreparationError(Pre553IntegrityError):
    """The exact retained preparation failed closed."""


class RetainedGT2N10EContractGapError(RetainedGT2AnalyticalPreparationError):
    """The accepted N10E direct contract cannot be satisfied by retained material."""

    def __init__(self, missing: tuple[tuple[str, str], ...]) -> None:
        self.missing = missing
        detail = "; ".join(f"{name}={state}" for name, state in missing)
        super().__init__(f"N10E_RETAINED_CONTRACT_GAP: {detail}")


@dataclass(frozen=True)
class N10EDeterminant:
    """One exact N10E request determinant and its custody state."""

    name: str
    state: str
    ref_or_null: Mapping[str, Any] | None
    reason: str

    def __post_init__(self) -> None:
        if not self.name or not self.state or not self.reason:
            raise RetainedGT2AnalyticalPreparationError(
                "determinant name/state/reason must be non-empty"
            )
        if self.state not in {
            DETERMINANT_EXACT_RETAINED,
            DETERMINANT_EXACT_RECONSTRUCTED,
            DETERMINANT_ABSENT_TRANSPORT,
            DETERMINANT_UNAVAILABLE_AUTHORITY,
        }:
            raise RetainedGT2AnalyticalPreparationError(
                f"unexpected determinant state {self.state!r}"
            )

    def material(self) -> Mapping[str, Any]:
        return {
            "name": self.name,
            "state": self.state,
            "ref_or_null": None if self.ref_or_null is None else dict(self.ref_or_null),
            "reason": self.reason,
        }


@dataclass(frozen=True)
class RetainedConditionedTargetRow:
    """Exact Field Forge conditioner row: counts and denominator only.

    No ratio/probability is calculated here.  Ratio construction belongs to the
    accepted analytical owner, not to this preparation adapter.
    """

    conditioner_state: Any
    conditioner_denominator_support: int
    target_counts: tuple[Mapping[str, Any], ...]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.conditioner_denominator_support, int)
            or isinstance(self.conditioner_denominator_support, bool)
            or self.conditioner_denominator_support < 0
        ):
            raise RetainedGT2AnalyticalPreparationError(
                "conditioner denominator must be a nonnegative integer"
            )
        if len(self.target_counts) != 6:
            raise RetainedGT2AnalyticalPreparationError(
                "each conditioner row must retain all six native target states"
            )
        total = sum(
            int(count["joint_support_count"]) for count in self.target_counts
        )
        if total != self.conditioner_denominator_support:
            raise RetainedGT2AnalyticalPreparationError(
                "conditioner target counts do not sum to the exact denominator"
            )

    def material(self) -> Mapping[str, Any]:
        return {
            "conditioner_state": canonicalize(self.conditioner_state),
            "conditioner_denominator_support": self.conditioner_denominator_support,
            "target_counts": [
                canonicalize(count) for count in self.target_counts
            ],
        }


@dataclass(frozen=True)
class RetainedGT2AnalyticalPreparation:
    """Exact retained GT2 preparation with typed N10E determinant gaps."""

    schema: str
    preparation_state: str
    source_family: str
    source_wave: str
    source_sha256: str
    query_ref: ExactRef
    fact_ref: ExactRef
    predicate_ref: ExactRef
    predicate_hash: str
    predicate_leaf_type: str
    predicate_value_bearing_leaf_count: int
    replay_ref: ExactRef
    risk_set_ref: ExactRef
    release_ref: ExactRef
    universe_ref: ExactRef
    relation_ref: ExactRef
    joint_cells: tuple[Mapping[str, Any], ...]
    conditioned_rows: tuple[RetainedConditionedTargetRow, ...]
    producer_authority_refs: tuple[AuthorityRef, ...]
    determinants: tuple[N10EDeterminant, ...]
    provider_receipt_or_null: Mapping[str, Any] | None
    consumer_result_or_null: Mapping[str, Any] | None
    replay_or_null: Mapping[str, Any] | None

    def __post_init__(self) -> None:
        if self.schema != PREPARATION_CONTRACT_ID:
            raise RetainedGT2AnalyticalPreparationError("preparation schema drift")
        if self.preparation_state != PREPARATION_STATE:
            raise RetainedGT2AnalyticalPreparationError("preparation state drift")
        if self.predicate_hash != self.predicate_ref.content_hash:
            raise RetainedGT2AnalyticalPreparationError("predicate hash/ref mismatch")
        if len(self.joint_cells) != 36:
            raise RetainedGT2AnalyticalPreparationError(
                "joint cells must remain the complete 6x6 native product"
            )
        if len(self.conditioned_rows) != 6:
            raise RetainedGT2AnalyticalPreparationError(
                "conditioned rows must retain all six native conditioner states"
            )
        if self.provider_receipt_or_null is not None:
            raise RetainedGT2AnalyticalPreparationError(
                "preparation may not claim an N10E provider receipt"
            )
        if self.consumer_result_or_null is not None:
            raise RetainedGT2AnalyticalPreparationError(
                "preparation may not claim an N10E consumer result"
            )
        if self.replay_or_null is not None:
            raise RetainedGT2AnalyticalPreparationError(
                "preparation may not claim an N10E replay"
            )

    def identity_material(self) -> Mapping[str, Any]:
        return {
            "schema": self.schema,
            "preparation_state": self.preparation_state,
            "source_family": self.source_family,
            "source_wave": self.source_wave,
            "source_sha256": self.source_sha256,
            "query_ref": self.query_ref.as_dict(),
            "fact_ref": self.fact_ref.as_dict(),
            "predicate_ref": self.predicate_ref.as_dict(),
            "predicate_hash": self.predicate_hash,
            "predicate_leaf_type": self.predicate_leaf_type,
            "predicate_value_bearing_leaf_count": (
                self.predicate_value_bearing_leaf_count
            ),
            "replay_ref": self.replay_ref.as_dict(),
            "risk_set_ref": self.risk_set_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "universe_ref": self.universe_ref.as_dict(),
            "relation_ref": self.relation_ref.as_dict(),
            "joint_cells": [canonicalize(cell) for cell in self.joint_cells],
            "conditioned_rows": [row.material() for row in self.conditioned_rows],
            "producer_authority_refs": [
                ref.as_dict() for ref in self.producer_authority_refs
            ],
            "determinants": [item.material() for item in self.determinants],
            "provider_receipt_or_null": None,
            "consumer_result_or_null": None,
            "replay_or_null": None,
        }

    @property
    def preparation_hash(self) -> str:
        return semantic_hash(self.identity_material())

    @property
    def preparation_ref(self) -> ExactRef:
        digest = self.preparation_hash
        return ExactRef(
            PREPARATION_CONTRACT_ID,
            f"urn:rawlsing:retained-gt2:n10e-preparation:sha256:{digest}",
            digest,
        )

    def material(self) -> Mapping[str, Any]:
        return {
            **self.identity_material(),
            "preparation_ref": self.preparation_ref.as_dict(),
        }

    def provider_request_shape(self) -> Mapping[str, Any]:
        """Return the exact provider shape with typed-null missing determinants.

        This is a preparation report, not a callable request and not a provider
        receipt.  Exact retained fields are shown exactly; absent fields are
        null with the reason recorded in ``determinants``.
        """
        by_name = {item.name: item for item in self.determinants}
        return {
            "provider_callable": N10E_PROVIDER_CALLABLE,
            "provider_input_mode": (
                "EXACT_DETERMINANTS_ONLY__NO_PRECOMPUTED_SLICE_GEOMETRY"
            ),
            "repository": None,
            "repository_state": by_name["repository"].state,
            "empirical_query": self.query_ref.as_dict(),
            "predicate": {
                "ref": self.predicate_ref.as_dict(),
                "predicate_hash": self.predicate_hash,
                "leaf_type": self.predicate_leaf_type,
                "value_bearing_leaf_count": (
                    self.predicate_value_bearing_leaf_count
                ),
            },
            "authority_registry": None,
            "authority_registry_state": by_name["authority_registry"].state,
            "release_refs": [self.release_ref.as_dict()],
            "release_refs_state": by_name["release_refs"].state,
            "consumer_query": None,
            "consumer_query_state": by_name["consumer_query"].state,
            "model_rule": None,
            "model_rule_state": by_name["model_rule"].state,
            "condition_binding_witness": None,
            "condition_binding_witness_state": by_name[
                "condition_binding_witness"
            ].state,
            "missing_determinants": [
                item.name
                for item in self.determinants
                if item.state
                in {
                    DETERMINANT_ABSENT_TRANSPORT,
                    DETERMINANT_UNAVAILABLE_AUTHORITY,
                }
            ],
        }

    def require_n10e_provider_route(self) -> None:
        """Refuse the accepted N10E route while exact determinants are absent."""
        missing = tuple(
            (item.name, item.state)
            for item in self.determinants
            if item.state
            in {
                DETERMINANT_ABSENT_TRANSPORT,
                DETERMINANT_UNAVAILABLE_AUTHORITY,
            }
        )
        if missing:
            raise RetainedGT2N10EContractGapError(missing)


def _one_ref_of_kind(
    refs: tuple[ExactRef, ...], kind: str, name: str
) -> ExactRef:
    matches = tuple(ref for ref in refs if ref.kind == kind)
    if len(matches) != 1:
        raise RetainedGT2AnalyticalPreparationError(
            f"{name} must resolve exactly once in the retained fact closure"
        )
    return matches[0]


def _value_bearing_leaf_count(predicate: EmpiricalPredicate) -> int:
    """Count the C1 value-bearing leaves under the exact retained predicate.

    Mirrors the accepted composition owner's leaf law without importing a
    private helper: only EQ leaves of ``SURVEY_RESPONSE_EVENT`` or
    ``EMPIRICAL_POSITION_COORDINATE`` are value-bearing.
    """

    count = 0

    def walk(node: Mapping[str, Any]) -> None:
        nonlocal count
        if (
            node.get("op") == "LEAF"
            and node.get("leaf_type")
            in {"SURVEY_RESPONSE_EVENT", "EMPIRICAL_POSITION_COORDINATE"}
            and node.get("operator") == "EQ"
            and "exact_value" in node
        ):
            count += 1
        elif node.get("op") in {"AND", "OR", "NOT"}:
            for child in node.get("children", ()):
                if isinstance(child, Mapping):
                    walk(child)

    walk(canonicalize(predicate.predicate_ast))
    return count


def _determinant(
    name: str,
    state: str,
    ref: ExactRef | Mapping[str, Any] | None,
    reason: str,
) -> N10EDeterminant:
    if isinstance(ref, ExactRef):
        material: Mapping[str, Any] | None = ref.as_dict()
    else:
        material = ref
    return N10EDeterminant(
        name=name, state=state, ref_or_null=material, reason=reason
    )


def _build_determinants(
    *,
    query: EmpiricalQuerySpec,
    fact: EmpiricalFact,
    predicate: EmpiricalPredicate,
    release_ref: ExactRef,
    universe_ref: ExactRef,
    risk_set_ref: ExactRef,
) -> tuple[N10EDeterminant, ...]:
    value_bearing = _value_bearing_leaf_count(predicate)
    return (
        _determinant(
            "repository",
            DETERMINANT_ABSENT_TRANSPORT,
            None,
            "the fixed transport contains the executed query/fact and hash-only "
            "respondent/routing/event refs, not a sealed C11LogicalRelease with "
            "respondent-level event preimages; a fresh I03 execution cannot be "
            "mounted without fabricating respondents or reopening source",
        ),
        _determinant(
            "empirical_query",
            DETERMINANT_EXACT_RETAINED,
            query.ref,
            "exact retained EmpiricalQuerySpec identity",
        ),
        _determinant(
            "predicate",
            DETERMINANT_EXACT_RECONSTRUCTED,
            predicate.ref,
            "exact retained predicate identity reconstructed from the query/fact "
            "refs and frozen risk-member closure; the predicate is a "
            "DERIVED_BRANCH_COHORT and contains "
            f"{value_bearing} value-bearing conditioner leaf(s)",
        ),
        _determinant(
            "authority_registry",
            DETERMINANT_ABSENT_TRANSPORT,
            None,
            "the retained fact/query carry exact AuthorityRefs but not the "
            "authority snapshot bodies needed by the accepted AuthorityRegistry",
        ),
        _determinant(
            "release_refs",
            DETERMINANT_ABSENT_TRANSPORT,
            release_ref,
            "the exact C11LogicalRelease ref is retained, but the sealed release "
            "object/public_objects/internal_records are absent from the transport",
        ),
        _determinant(
            "consumer_query",
            DETERMINANT_UNAVAILABLE_AUTHORITY,
            None,
            "no accepted GT2 positioned-subject consumer query binds Q86B as a "
            "value-bearing conditioner and Q86A as target; the retained joint "
            "query is SEMANTIC_ORDERED [Q86B, Q86A] with a cohort predicate",
        ),
        _determinant(
            "model_rule",
            DETERMINANT_UNAVAILABLE_AUTHORITY,
            None,
            "no adopted operation-specific N10E model/walkback authority exists "
            "for GT2; the only nearby candidate (HQ230 C1-AT07) is "
            "CANDIDATE_NOT_ADOPTED and explicitly AT07-fixture-scoped",
        ),
        _determinant(
            "condition_binding_witness",
            DETERMINANT_UNAVAILABLE_AUTHORITY,
            None,
            "the current C1 witness contract requires a value-bearing producer "
            "predicate leaf and an operation-specific pairing authority; the "
            "retained GT2 predicate has no value-bearing leaves and the retained "
            "authority closure contains no condition-value pairing authority",
        ),
    )


def load_retained_gt2_analytical_preparation() -> RetainedGT2AnalyticalPreparation:
    """Build the exact source-free preparation from the fixed committed transport."""

    query, fact = load_current_gt2_query_fact_from_committed_transport()
    if type(query) is not EmpiricalQuerySpec or type(fact) is not EmpiricalFact:
        raise RetainedGT2AnalyticalPreparationError(
            "retained loader did not return ordinary exact query/fact objects"
        )
    if query.content_hash != CURRENT_QUERY_HASH:
        raise RetainedGT2AnalyticalPreparationError("retained query identity drift")
    if fact.content_hash != CURRENT_FACT_HASH:
        raise RetainedGT2AnalyticalPreparationError("retained fact identity drift")
    if exact_ref(fact.replay_ref, "fact.replay_ref").content_hash != CURRENT_REPLAY_HASH:
        raise RetainedGT2AnalyticalPreparationError("retained replay identity drift")

    predicate = reconstruct_gt2_risk_cohort_predicate(query=query, fact=fact)
    if predicate.content_hash != CURRENT_PREDICATE_HASH:
        raise RetainedGT2AnalyticalPreparationError(
            "retained predicate identity drift after reconstruction"
        )

    relation = produce_exact_conditional_support_profile(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=query.target_refs[0],
        target_ref=query.target_refs[1],
        producer_permission_ceiling=(STRUCTURAL_PERMISSION_CEILING,),
        relation_permission_ceiling=(STRUCTURAL_PERMISSION_CEILING,),
    )
    if relation.typed_state != "SUPPORTED":
        raise RetainedGT2AnalyticalPreparationError(
            f"retained Field Forge relation is not positive: {relation.typed_state!r}"
        )

    provenance = tuple(
        exact_ref(ref, "fact.source_empirical_provenance_refs")
        for ref in fact.source_empirical_provenance_refs
    )
    release_ref = _one_ref_of_kind(
        provenance, "C11LogicalRelease", "retained release"
    )
    universe_refs = tuple(
        exact_ref(ref, "query.empirical_universe_refs")
        for ref in query.empirical_universe_refs
    )
    if len(universe_refs) != 1:
        raise RetainedGT2AnalyticalPreparationError(
            "retained GT2 query must bind exactly one empirical universe"
        )
    risk_set_ref = exact_ref(fact.risk_set_ref, "fact.risk_set_ref")

    joint_cells = tuple(
        canonicalize(cell)
        for cell in canonicalize(fact.target_topology)[
            "complete_cell_semantic_projection"
        ]
    )
    if len(joint_cells) != 36:
        raise RetainedGT2AnalyticalPreparationError(
            "retained joint cell geometry is not the complete 6x6 product"
        )
    if sum(int(cell["raw_numerator_support"]) for cell in joint_cells) != (
        FROZEN_RISK_SET_MEMBER_COUNT
    ):
        raise RetainedGT2AnalyticalPreparationError(
            "retained joint cell support does not conserve the exact risk set"
        )

    rows: list[RetainedConditionedTargetRow] = []
    for raw_row in relation.conditional_count_profile:
        row = canonicalize(raw_row)
        target_counts = tuple(
            canonicalize(count) for count in row["target_counts"]
        )
        if len(target_counts) != 6:
            raise RetainedGT2AnalyticalPreparationError(
                "Field Forge row lost a native target state"
            )
        rows.append(
            RetainedConditionedTargetRow(
                conditioner_state=canonicalize(row["condition_state"]),
                conditioner_denominator_support=int(
                    row["condition_denominator_support"]
                ),
                target_counts=target_counts,
            )
        )
    if len(rows) != 6:
        raise RetainedGT2AnalyticalPreparationError(
            "Field Forge relation lost a native conditioner state"
        )
    if sum(row.conditioner_denominator_support for row in rows) != (
        FROZEN_RISK_SET_MEMBER_COUNT
    ):
        raise RetainedGT2AnalyticalPreparationError(
            "conditioned rows do not conserve the exact risk-set denominator"
        )

    determinants = _build_determinants(
        query=query,
        fact=fact,
        predicate=predicate,
        release_ref=release_ref,
        universe_ref=universe_refs[0],
        risk_set_ref=risk_set_ref,
    )

    predicate_ast = canonicalize(predicate.predicate_ast)
    value_bearing = _value_bearing_leaf_count(predicate)
    return RetainedGT2AnalyticalPreparation(
        schema=PREPARATION_CONTRACT_ID,
        preparation_state=PREPARATION_STATE,
        source_family="Afrobarometer",
        source_wave="R5",
        source_sha256=FROZEN_R5_SOURCE_SHA256,
        query_ref=query.ref,
        fact_ref=fact.ref,
        predicate_ref=predicate.ref,
        predicate_hash=predicate.content_hash,
        predicate_leaf_type=str(predicate_ast.get("leaf_type")),
        predicate_value_bearing_leaf_count=value_bearing,
        replay_ref=exact_ref(fact.replay_ref, "fact.replay_ref"),
        risk_set_ref=risk_set_ref,
        release_ref=release_ref,
        universe_ref=universe_refs[0],
        relation_ref=relation.ref,
        joint_cells=joint_cells,
        conditioned_rows=tuple(rows),
        producer_authority_refs=tuple(
            authority_ref(ref, "fact.authority_snapshot_refs")
            for ref in fact.authority_snapshot_refs
        ),
        determinants=determinants,
        provider_receipt_or_null=None,
        consumer_result_or_null=None,
        replay_or_null=None,
    )


__all__ = [
    "PREPARATION_CONTRACT_ID",
    "PREPARATION_STATE",
    "N10E_PROVIDER_CALLABLE",
    "N10E_CONSUMER_CALLABLE",
    "N10E_COMPOSER_CALLABLE",
    "FIELD_FORGE_CALLABLE",
    "DETERMINANT_EXACT_RETAINED",
    "DETERMINANT_EXACT_RECONSTRUCTED",
    "DETERMINANT_ABSENT_TRANSPORT",
    "DETERMINANT_UNAVAILABLE_AUTHORITY",
    "RetainedGT2AnalyticalPreparationError",
    "RetainedGT2N10EContractGapError",
    "N10EDeterminant",
    "RetainedConditionedTargetRow",
    "RetainedGT2AnalyticalPreparation",
    "load_retained_gt2_analytical_preparation",
]
