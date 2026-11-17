"""Bounded FIELD FORGE conditional-support count relation for GT2.

This module owns only the exact actor-independent relation commitment frozen as
EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0.

It consumes an already-produced PRE553 I03 two-target joint EmpiricalFact.  It
does not execute empirical queries, reinterpret source-native states, calculate
ratios, infer order/metric/causal semantics, admit PRE-V3 structure, or create
actor facts.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)


RELATION_FAMILY = "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0"
SEMANTIC_OWNER = "FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER"
CONDITIONER_ROLE = "CONDITIONER"
TARGET_ROLE = "TARGET"
CONDITIONER_SOURCE_NATIVE_VARIABLE = "Q86B"
TARGET_SOURCE_NATIVE_VARIABLE = "Q86A"
INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"
STATE_ORDER_SEMANTICS = "IDENTITY_ONLY__NO_ORDINAL_OR_METRIC_MEANING"
RELATION_SEMANTICS = "EXACT_CONDITIONAL_SUPPORT_COUNT_PROFILE_WITHIN_SCOPE"
FROZEN_TARGET_ORDER = "SEMANTIC_ORDERED"

NONPOSITIVE_PRODUCER_STATES = frozenset({
    "OBSERVED_ZERO",
    "ZERO_SUPPORT",
    "ZERO_OVERLAP",
    "LOW_SUPPORT",
    "NONCOMPARABLE",
    "NOT_APPLICABLE",
    "UNAVAILABLE",
    "UNCERTAINTY_UNQUANTIFIED",
    "UNRESOLVED",
    "VALID_EMPTY",
    "INTEGRITY_FAILURE",
})
ALLOWED_PRODUCER_STATES = frozenset({"SUPPORTED", *NONPOSITIVE_PRODUCER_STATES})


class FieldForgeConditionalSupportError(ValueError):
    """The frozen GT2 FIELD FORGE relation cannot be produced lawfully."""


class FieldForgePermissionWideningError(FieldForgeConditionalSupportError):
    """The relation attempted to exceed the producer permission ceiling."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FieldForgeConditionalSupportError(f"{name} must be non-empty")
    return value.strip()


def _permissions(values: Iterable[str], name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise FieldForgeConditionalSupportError(f"{name} must be an iterable of permission atoms")
    out = tuple(sorted({_text(v, name) for v in values}))
    if not out:
        raise FieldForgeConditionalSupportError(f"{name} may not be empty")
    return out


def _exact(value: ExactRef | Mapping[str, Any], name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Exception as exc:
        raise FieldForgeConditionalSupportError(str(exc)) from exc


def _exact_seq(values: Iterable[ExactRef | Mapping[str, Any]], name: str) -> tuple[ExactRef, ...]:
    refs = tuple(_exact(v, name) for v in values)
    return tuple(sorted(set(refs), key=lambda r: r.key))


def _authority_seq(values: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    refs = tuple(values)
    if not all(isinstance(ref, AuthorityRef) for ref in refs):
        raise FieldForgeConditionalSupportError("producer authority closure must use exact AuthorityRef")
    return tuple(sorted(set(refs), key=lambda r: r.key))


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise FieldForgeConditionalSupportError(f"{name} must be a mapping")
    return value


def _sequence(value: Any, name: str, *, allow_empty: bool = False) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise FieldForgeConditionalSupportError(f"{name} must be a sequence")
    if not allow_empty and not value:
        raise FieldForgeConditionalSupportError(f"{name} may not be empty")
    return value


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(k): _freeze(v) for k, v in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_freeze(v) for v in value)
    return value


def _auth_dict(ref: AuthorityRef) -> dict[str, str]:
    return ref.as_dict()


def _query_component_material(
    query: EmpiricalQuerySpec,
    *,
    conditioner_ref: ExactRef,
    target_ref: ExactRef,
) -> tuple[tuple[Any, ...], tuple[Any, ...], str]:
    spec = _mapping(query.target_arity_and_topology, "query.target_arity_and_topology")
    if spec.get("arity") != 2:
        raise FieldForgeConditionalSupportError("GT2 relation requires exact two-target query arity")
    if spec.get("joint_order_semantics") != FROZEN_TARGET_ORDER:
        raise FieldForgeConditionalSupportError(
            "GT2 Q86B->Q86A target order must be SEMANTIC_ORDERED")

    query_targets = tuple(_exact(v, "query.target_refs") for v in query.target_refs)
    if query_targets != (conditioner_ref, target_ref):
        raise FieldForgeConditionalSupportError(
            "query target role/order must be exactly [Q86B CONDITIONER, Q86A TARGET]")

    components = _sequence(spec.get("components"), "query target components")
    if len(components) != 2:
        raise FieldForgeConditionalSupportError("GT2 query requires exactly two target components")

    normalized = []
    domains = []
    for idx, (raw, expected_ref) in enumerate(zip(components, query_targets)):
        comp = _mapping(raw, f"target component {idx}")
        comp_ref = _exact(comp.get("target_ref"), f"target component {idx}.target_ref")
        if comp_ref != expected_ref:
            raise FieldForgeConditionalSupportError("target component ref/order mismatch")
        if comp.get("topology") != "SCALAR_SINGULAR":
            raise FieldForgeConditionalSupportError(
                "frozen Q86A/Q86B GT2 relation requires source-native SCALAR_SINGULAR targets")
        domain = tuple(canonicalize(v) for v in _sequence(
            comp.get("domain"), f"target component {idx}.domain"))
        if len({canonical_json(v) for v in domain}) != len(domain):
            raise FieldForgeConditionalSupportError("target domain contains duplicate exact states")
        replay_ref = _exact(
            comp.get("target_domain_replay_ref"), f"target component {idx}.target_domain_replay_ref")
        domains.append(domain)
        normalized.append({
            "target_ref": comp_ref.as_dict(),
            "topology": comp["topology"],
            "domain": list(domain),
            "target_domain_replay_ref": replay_ref.as_dict(),
        })

    cartesian_domain = tuple(canonicalize(list(v)) for v in product(*domains))
    explicit_joint = spec.get("joint_domain")
    if explicit_joint is None:
        full_domain = cartesian_domain
    else:
        full_domain = tuple(canonicalize(v) for v in _sequence(
            explicit_joint, "query target joint_domain", allow_empty=True))
        if len({canonical_json(v) for v in full_domain}) != len(full_domain):
            raise FieldForgeConditionalSupportError(
                "explicit joint domain contains duplicate exact cells")
        if {canonical_json(v) for v in full_domain} != {
            canonical_json(v) for v in cartesian_domain
        }:
            raise FieldForgeConditionalSupportError(
                "GT2 explicit joint domain must preserve the complete native Q86B x Q86A product")
    identity = semantic_hash({
        "components": normalized,
        "joint_order_semantics": FROZEN_TARGET_ORDER,
        "full_domain": list(full_domain),
    })
    return domains[0], domains[1], identity


def _validate_common_closure(
    *,
    joint_fact: EmpiricalFact,
    joint_query: EmpiricalQuerySpec,
) -> tuple[ExactRef, tuple[ExactRef, ...], tuple[AuthorityRef, ...], ExactRef, tuple[ExactRef, ...]]:
    if not isinstance(joint_fact, EmpiricalFact):
        raise FieldForgeConditionalSupportError(
            "input must be producer-owned EmpiricalFact@1.0.0")
    if not isinstance(joint_query, EmpiricalQuerySpec):
        raise FieldForgeConditionalSupportError(
            "joint_query must be exact EmpiricalQuerySpec@1.0.0")
    if semantic_hash(joint_fact.semantic_projection()) != joint_fact.content_hash:
        raise FieldForgeConditionalSupportError("producer EmpiricalFact semantic identity mismatch")
    if semantic_hash(joint_query.semantic_projection()) != joint_query.content_hash:
        raise FieldForgeConditionalSupportError("producer EmpiricalQuerySpec semantic identity mismatch")
    if joint_fact.typed_state not in ALLOWED_PRODUCER_STATES:
        raise FieldForgeConditionalSupportError(
            f"unsupported producer typed_state {joint_fact.typed_state!r}")

    fact_query_ref = _exact(joint_fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref")
    if fact_query_ref != joint_query.ref:
        raise FieldForgeConditionalSupportError(
            "producer fact does not bind the supplied exact query identity")

    fact_risk = _exact(joint_fact.risk_set_ref, "fact.risk_set_ref")
    query_risk = _exact(joint_query.risk_set_ref, "query.risk_set_ref")
    if fact_risk != query_risk:
        raise FieldForgeConditionalSupportError("producer fact/query risk-set mismatch")

    fact_universes = _exact_seq(joint_fact.empirical_universe_refs, "fact.empirical_universe_refs")
    query_universes = _exact_seq(joint_query.empirical_universe_refs, "query.empirical_universe_refs")
    if fact_universes != query_universes or len(fact_universes) != 1:
        raise FieldForgeConditionalSupportError(
            "GT2 relation requires one exact identical SINGLE_UNIVERSE scope")

    grain = _mapping(joint_query.requested_output_grain, "query.requested_output_grain")
    if grain.get("source_scope_mode") != "SINGLE_UNIVERSE":
        raise FieldForgeConditionalSupportError("GT2 relation requires SINGLE_UNIVERSE")
    if grain.get("measure_kind") != "RAW":
        raise FieldForgeConditionalSupportError("GT2 relation is RAW/unweighted only")
    if getattr(joint_fact, "source_scope_mode", None) not in (None, "SINGLE_UNIVERSE"):
        raise FieldForgeConditionalSupportError("producer fact source scope is not SINGLE_UNIVERSE")
    if getattr(joint_fact, "measure_kind", None) not in (None, "RAW"):
        raise FieldForgeConditionalSupportError("producer fact is not RAW")
    if joint_fact.weighted_numerator_support_if_authorized is not None:
        raise FieldForgeConditionalSupportError("GT2 relation may not consume weighted numerator")
    if joint_fact.weighted_denominator_support_if_authorized is not None:
        raise FieldForgeConditionalSupportError("GT2 relation may not consume weighted denominator")

    authorities = _authority_seq(joint_fact.authority_snapshot_refs)
    query_authorities = _authority_seq(joint_query.authority_snapshot_refs)
    if not set(query_authorities).issubset(set(authorities)):
        raise FieldForgeConditionalSupportError(
            "producer fact authority closure does not preserve query authorities")

    replay_ref = _exact(joint_fact.replay_ref, "fact.replay_ref")
    if isinstance(joint_fact.producer_replay_locator_or_reference_root, ExactRef):
        if joint_fact.producer_replay_locator_or_reference_root != replay_ref:
            raise FieldForgeConditionalSupportError(
                "producer replay root differs from exact fact replay_ref")
    else:
        if _exact(joint_fact.producer_replay_locator_or_reference_root, "fact replay root") != replay_ref:
            raise FieldForgeConditionalSupportError(
                "producer replay root differs from exact fact replay_ref")

    dependencies = _exact_seq(joint_fact.dependency_refs, "fact.dependency_refs")
    if joint_query.ref not in dependencies or replay_ref not in dependencies:
        raise FieldForgeConditionalSupportError(
            "producer fact dependency closure omits query or replay identity")

    provenance = _exact_seq(
        joint_fact.source_empirical_provenance_refs, "fact.source_empirical_provenance_refs")
    if not provenance:
        raise FieldForgeConditionalSupportError("producer fact provenance closure is empty")
    if not set(provenance).issubset(set(dependencies)):
        raise FieldForgeConditionalSupportError(
            "producer provenance refs are not retained in fact dependency closure")

    return fact_risk, fact_universes, authorities, replay_ref, provenance


def _cell_profile(
    *,
    joint_fact: EmpiricalFact,
    conditioner_domain: tuple[Any, ...],
    target_domain: tuple[Any, ...],
    expected_domain_identity: str,
) -> tuple[Mapping[str, Any], ...]:
    topology = _mapping(joint_fact.target_topology, "fact.target_topology")
    if topology.get("arity") != 2:
        raise FieldForgeConditionalSupportError("positive GT2 fact target topology arity mismatch")
    if topology.get("joint_order_semantics") != FROZEN_TARGET_ORDER:
        raise FieldForgeConditionalSupportError("positive GT2 fact target role/order mismatch")
    if topology.get("target_domain_identity") != expected_domain_identity:
        raise FieldForgeConditionalSupportError("producer target-domain identity mismatch")
    if getattr(joint_fact, "target_domain_identity", expected_domain_identity) != expected_domain_identity:
        raise FieldForgeConditionalSupportError("producer target-domain identity closure mismatch")

    rows = _sequence(
        topology.get("complete_cell_semantic_projection"),
        "fact.target_topology.complete_cell_semantic_projection",
        allow_empty=True,
    )
    expected_cells = tuple((c, t) for c in conditioner_domain for t in target_domain)
    expected_keys = {canonical_json([c, t]) for c, t in expected_cells}
    seen: dict[str, Mapping[str, Any]] = {}

    for raw in rows:
        row = _mapping(raw, "joint cell")
        cell = _sequence(row.get("cell"), "joint cell identity")
        if len(cell) != 2:
            raise FieldForgeConditionalSupportError("joint cell must contain Q86B,Q86A states")
        key = canonical_json([canonicalize(cell[0]), canonicalize(cell[1])])
        if key not in expected_keys or key in seen:
            raise FieldForgeConditionalSupportError("joint cell domain is incomplete, duplicated, or tampered")
        count = row.get("raw_numerator_support")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise FieldForgeConditionalSupportError("joint support count must be nonnegative exact integer")
        cell_state = row.get("cell_state")
        if count == 0 and cell_state not in {
            "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET", "ZERO_SUPPORT"
        }:
            raise FieldForgeConditionalSupportError("zero joint count has inconsistent cell state")
        if count > 0 and cell_state != "OBSERVED_POSITIVE":
            raise FieldForgeConditionalSupportError("positive joint count has inconsistent cell state")
        seen[key] = row

    if set(seen) != expected_keys:
        raise FieldForgeConditionalSupportError(
            "producer joint fact does not preserve the complete native Q86B x Q86A domain")

    total = sum(int(seen[canonical_json([c, t])]["raw_numerator_support"])
                for c, t in expected_cells)
    if total != joint_fact.raw_numerator_support:
        raise FieldForgeConditionalSupportError(
            "joint cell counts do not equal producer raw numerator support")
    if getattr(joint_fact, "raw_resolved_target_support", total) != total:
        raise FieldForgeConditionalSupportError(
            "joint cell counts do not equal producer resolved target support")
    if total > joint_fact.raw_denominator_support:
        raise FieldForgeConditionalSupportError(
            "joint cell counts exceed producer risk-set denominator")

    profile = []
    for condition_state in conditioner_domain:
        target_counts = []
        denominator = 0
        for target_state in target_domain:
            row = seen[canonical_json([condition_state, target_state])]
            count = int(row["raw_numerator_support"])
            denominator += count
            target_counts.append({
                "target_state": canonicalize(target_state),
                "joint_support_count": count,
                "cell_state": row["cell_state"],
            })
        profile.append({
            "condition_state": canonicalize(condition_state),
            "condition_denominator_support": denominator,
            "target_counts": tuple(target_counts),
        })
    return tuple(_freeze(row) for row in profile)


@dataclass(frozen=True)
class ExactConditionalSupportProfile:
    """Immutable FIELD FORGE relation/result at the frozen GT2 relation grain."""

    typed_state: str
    producer_state_blocking: bool
    conditioner_ref: ExactRef
    target_ref: ExactRef
    conditioner_domain: tuple[Any, ...]
    target_domain: tuple[Any, ...]
    target_domain_identity: str
    risk_set_ref: ExactRef
    empirical_universe_refs: tuple[ExactRef, ...]
    producer_fact_ref: ExactRef
    producer_query_ref: ExactRef
    producer_authority_refs: tuple[AuthorityRef, ...]
    producer_provenance_refs: tuple[ExactRef, ...]
    producer_replay_ref: ExactRef
    producer_permission_ceiling: tuple[str, ...]
    relation_permission_ceiling: tuple[str, ...]
    conditional_count_profile: tuple[Mapping[str, Any], ...]
    content_hash: str
    object_id: str

    def __post_init__(self) -> None:
        if self.typed_state not in ALLOWED_PRODUCER_STATES:
            raise FieldForgeConditionalSupportError(
                f"invalid relation typed_state {self.typed_state!r}")
        if self.producer_state_blocking != (self.typed_state != "SUPPORTED"):
            raise FieldForgeConditionalSupportError(
                "producer_state_blocking must exactly reflect producer typed state")
        if not set(self.relation_permission_ceiling).issubset(
            set(self.producer_permission_ceiling)
        ):
            raise FieldForgePermissionWideningError(
                "stored relation permission exceeds producer permission ceiling")
        if self.producer_state_blocking and self.conditional_count_profile:
            raise FieldForgeConditionalSupportError(
                "blocked relation/result may not carry a positive count profile")
        digest = semantic_hash(self.semantic_projection())
        expected_id = f"urn:rawlsing:field-forge:conditional-support:sha256:{digest}"
        if self.content_hash != digest or self.object_id != expected_id:
            raise FieldForgeConditionalSupportError(
                "relation object_id/content_hash do not match deterministic semantic projection")

    @property
    def family(self) -> str:
        return RELATION_FAMILY

    @property
    def semantic_owner(self) -> str:
        return SEMANTIC_OWNER

    @property
    def ref(self) -> ExactRef:
        return ExactRef(RELATION_FAMILY, self.object_id, self.content_hash)

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "relation_family": RELATION_FAMILY,
            "semantic_owner": SEMANTIC_OWNER,
            "relation_semantics": RELATION_SEMANTICS,
            "typed_state": self.typed_state,
            "producer_state_blocking": self.producer_state_blocking,
            "roles": {
                CONDITIONER_ROLE: {
                    "source_native_variable": CONDITIONER_SOURCE_NATIVE_VARIABLE,
                    "ref": self.conditioner_ref.as_dict(),
                },
                TARGET_ROLE: {
                    "source_native_variable": TARGET_SOURCE_NATIVE_VARIABLE,
                    "ref": self.target_ref.as_dict(),
                },
            },
            "participant_cardinality": 2,
            "participant_role_order": [CONDITIONER_ROLE, TARGET_ROLE],
            "state_order_semantics": STATE_ORDER_SEMANTICS,
            "conditioner_domain": canonicalize(self.conditioner_domain),
            "target_domain": canonicalize(self.target_domain),
            "target_domain_identity": self.target_domain_identity,
            "risk_set_ref": self.risk_set_ref.as_dict(),
            "empirical_universe_refs": [r.as_dict() for r in self.empirical_universe_refs],
            "producer_fact_ref": self.producer_fact_ref.as_dict(),
            "producer_query_ref": self.producer_query_ref.as_dict(),
            "producer_authority_refs": [_auth_dict(r) for r in self.producer_authority_refs],
            "producer_provenance_refs": [r.as_dict() for r in self.producer_provenance_refs],
            "producer_replay_ref": self.producer_replay_ref.as_dict(),
            "producer_permission_ceiling": list(self.producer_permission_ceiling),
            "relation_permission_ceiling": list(self.relation_permission_ceiling),
            "information_loss": INFORMATION_LOSS,
            "conditional_count_profile": canonicalize(self.conditional_count_profile),
            "anti_inferences": [
                "CONDITIONER != CAUSE",
                "TARGET != EFFECT",
                "CONDITIONAL_SUPPORT_PROFILE != CONDITIONAL_REDISTRIBUTION_MECHANISM",
                "CONDITIONAL_SUPPORT_PROFILE != PRESSURE_PATHWAY",
                "CONDITIONAL_SUPPORT_PROFILE != STRUCTURAL_MECHANISM",
                "POPULATION_FACT != ACTOR_FACT",
            ],
        }

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.semantic_projection(),
            "object_id": self.object_id,
            "content_hash": self.content_hash,
        }


def produce_exact_conditional_support_profile(
    *,
    joint_fact: EmpiricalFact,
    joint_query: EmpiricalQuerySpec,
    conditioner_ref: ExactRef | Mapping[str, Any],
    target_ref: ExactRef | Mapping[str, Any],
    producer_permission_ceiling: Iterable[str],
    relation_permission_ceiling: Iterable[str] | None = None,
) -> ExactConditionalSupportProfile:
    """Produce the frozen Q86B-conditioned Q86A count profile.

    The function never computes a ratio.  A nonpositive producer fact yields an
    immutable typed blocking relation/result with an empty count profile rather
    than being promoted to a positive relation.
    """
    conditioner = _exact(conditioner_ref, "conditioner_ref")
    target = _exact(target_ref, "target_ref")
    producer_permissions = _permissions(
        producer_permission_ceiling, "producer_permission_ceiling")
    relation_permissions = (
        producer_permissions
        if relation_permission_ceiling is None
        else _permissions(relation_permission_ceiling, "relation_permission_ceiling")
    )
    if not set(relation_permissions).issubset(set(producer_permissions)):
        raise FieldForgePermissionWideningError(
            "FIELD FORGE relation permission may narrow but never widen producer permission")

    risk_ref, universes, authorities, replay_ref, provenance = _validate_common_closure(
        joint_fact=joint_fact, joint_query=joint_query)
    conditioner_domain, target_domain, domain_identity = _query_component_material(
        joint_query, conditioner_ref=conditioner, target_ref=target)

    producer_blocking = joint_fact.typed_state != "SUPPORTED"
    if producer_blocking:
        profile: tuple[Mapping[str, Any], ...] = ()
    else:
        if joint_fact.raw_denominator_support <= 0:
            raise FieldForgeConditionalSupportError(
                "SUPPORTED producer fact requires positive exact denominator")
        profile = _cell_profile(
            joint_fact=joint_fact,
            conditioner_domain=conditioner_domain,
            target_domain=target_domain,
            expected_domain_identity=domain_identity,
        )

    projection = {
        "relation_family": RELATION_FAMILY,
        "semantic_owner": SEMANTIC_OWNER,
        "relation_semantics": RELATION_SEMANTICS,
        "typed_state": joint_fact.typed_state,
        "producer_state_blocking": producer_blocking,
        "roles": {
            CONDITIONER_ROLE: {
                "source_native_variable": CONDITIONER_SOURCE_NATIVE_VARIABLE,
                "ref": conditioner.as_dict(),
            },
            TARGET_ROLE: {
                "source_native_variable": TARGET_SOURCE_NATIVE_VARIABLE,
                "ref": target.as_dict(),
            },
        },
        "participant_cardinality": 2,
        "participant_role_order": [CONDITIONER_ROLE, TARGET_ROLE],
        "state_order_semantics": STATE_ORDER_SEMANTICS,
        "conditioner_domain": canonicalize(conditioner_domain),
        "target_domain": canonicalize(target_domain),
        "target_domain_identity": domain_identity,
        "risk_set_ref": risk_ref.as_dict(),
        "empirical_universe_refs": [r.as_dict() for r in universes],
        "producer_fact_ref": joint_fact.ref.as_dict(),
        "producer_query_ref": joint_query.ref.as_dict(),
        "producer_authority_refs": [_auth_dict(r) for r in authorities],
        "producer_provenance_refs": [r.as_dict() for r in provenance],
        "producer_replay_ref": replay_ref.as_dict(),
        "producer_permission_ceiling": list(producer_permissions),
        "relation_permission_ceiling": list(relation_permissions),
        "information_loss": INFORMATION_LOSS,
        "conditional_count_profile": canonicalize(profile),
        "anti_inferences": [
            "CONDITIONER != CAUSE",
            "TARGET != EFFECT",
            "CONDITIONAL_SUPPORT_PROFILE != CONDITIONAL_REDISTRIBUTION_MECHANISM",
            "CONDITIONAL_SUPPORT_PROFILE != PRESSURE_PATHWAY",
            "CONDITIONAL_SUPPORT_PROFILE != STRUCTURAL_MECHANISM",
            "POPULATION_FACT != ACTOR_FACT",
        ],
    }
    digest = semantic_hash(projection)
    object_id = f"urn:rawlsing:field-forge:conditional-support:sha256:{digest}"
    return ExactConditionalSupportProfile(
        typed_state=joint_fact.typed_state,
        producer_state_blocking=producer_blocking,
        conditioner_ref=conditioner,
        target_ref=target,
        conditioner_domain=tuple(_freeze(v) for v in conditioner_domain),
        target_domain=tuple(_freeze(v) for v in target_domain),
        target_domain_identity=domain_identity,
        risk_set_ref=risk_ref,
        empirical_universe_refs=universes,
        producer_fact_ref=joint_fact.ref,
        producer_query_ref=joint_query.ref,
        producer_authority_refs=authorities,
        producer_provenance_refs=provenance,
        producer_replay_ref=replay_ref,
        producer_permission_ceiling=producer_permissions,
        relation_permission_ceiling=relation_permissions,
        conditional_count_profile=profile,
        content_hash=digest,
        object_id=object_id,
    )


def replay_exact_conditional_support_profile(
    *,
    expected_ref: ExactRef | Mapping[str, Any],
    **kwargs: Any,
) -> ExactConditionalSupportProfile:
    """Reconstruct and require exact deterministic relation identity."""
    expected = _exact(expected_ref, "expected_ref")
    result = produce_exact_conditional_support_profile(**kwargs)
    if result.ref != expected:
        raise FieldForgeConditionalSupportError(
            "deterministic relation replay mismatch: exact identity differs")
    return result


__all__ = [
    "RELATION_FAMILY",
    "SEMANTIC_OWNER",
    "CONDITIONER_ROLE",
    "TARGET_ROLE",
    "CONDITIONER_SOURCE_NATIVE_VARIABLE",
    "TARGET_SOURCE_NATIVE_VARIABLE",
    "INFORMATION_LOSS",
    "STATE_ORDER_SEMANTICS",
    "ExactConditionalSupportProfile",
    "FieldForgeConditionalSupportError",
    "FieldForgePermissionWideningError",
    "produce_exact_conditional_support_profile",
    "replay_exact_conditional_support_profile",
]
