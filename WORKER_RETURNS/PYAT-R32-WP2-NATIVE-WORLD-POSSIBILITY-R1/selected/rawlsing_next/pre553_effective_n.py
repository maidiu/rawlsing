"""Governed PRE553 F018 effective-N measurement successor.

This module is deliberately downstream of I03 empirical truth.  It consumes an
exact EmpiricalFact plus the exact WeightMeasureFact records already used by
that fact and emits a separate replayable measurement receipt.  It does not
mint EmpiricalFacts, select a weight, invent an estimand, or alter discovery or
structural authority.

Effective N is computed exactly as:

    (sum(w) ** 2) / sum(w ** 2)

but only when an exact governed weighted query, exact denominator membership,
exact weight basis, exact weight scope, and positive design + estimand
authorities all close.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    WeightMeasureFact,
    authority_ref,
    canonicalize,
    exact_ref,
    semantic_hash,
)

EFFECTIVE_N_CONTRACT_ID = "PRE553_F018_EFFECTIVE_N@1.0.0"
EFFECTIVE_N_FORMULA_ID = "SUM_W_SQUARED_OVER_SUM_W2_EXACT@1.0.0"

EFFECTIVE_N_STATES = frozenset({
    "SUPPORTED",
    "NOT_APPLICABLE",
    "NOT_AUTHORIZED",
    "INVALID_WEIGHT",
    "DEGENERATE_WEIGHT_SUM",
    "SCOPE_MISMATCH",
    "UPSTREAM_UNAVAILABLE",
})


class EffectiveNError(Pre553IntegrityError):
    """Effective-N input identity, authority, scope, or replay is invalid."""


@dataclass(frozen=True)
class EffectiveNProduct:
    """Content-addressed F018 measurement receipt; never empirical truth authority."""

    contract_id: str
    formula_id: str
    typed_state: str
    empirical_fact_ref: ExactRef
    query_ref: ExactRef
    release_refs: tuple[ExactRef, ...]
    source_universe_refs: tuple[ExactRef, ...]
    risk_set_ref: ExactRef
    condition_predicate_ref: ExactRef
    measure_basis_ref: ExactRef
    source_scope_mode: str
    target_topology_identity: str
    denominator_member_refs: tuple[ExactRef, ...]
    weight_basis_id: str | None
    authorized_weight_scope_ref: ExactRef | None
    weight_fact_refs: tuple[ExactRef, ...]
    weight_source_refs: tuple[ExactRef, ...]
    design_authority_refs: tuple[AuthorityRef, ...]
    estimand_authority_refs: tuple[AuthorityRef, ...]
    authority_refs: tuple[AuthorityRef, ...]
    sum_w: Fraction | None
    sum_w2: Fraction | None
    effective_n: Fraction | None
    provenance_refs: tuple[ExactRef, ...]
    replay_ref: ExactRef
    product_ref: ExactRef
    detail: str

    def __post_init__(self) -> None:
        if self.contract_id != EFFECTIVE_N_CONTRACT_ID:
            raise EffectiveNError("unexpected effective-N contract id")
        if self.formula_id != EFFECTIVE_N_FORMULA_ID:
            raise EffectiveNError("unexpected effective-N formula id")
        if self.typed_state not in EFFECTIVE_N_STATES:
            raise EffectiveNError("unknown effective-N typed state")
        if not isinstance(self.detail, str) or not self.detail.strip():
            raise EffectiveNError("effective-N product requires a non-empty detail")

        for name in (
            "release_refs",
            "source_universe_refs",
            "denominator_member_refs",
            "weight_fact_refs",
            "weight_source_refs",
            "provenance_refs",
        ):
            refs = getattr(self, name)
            if tuple(sorted(set(refs), key=lambda ref: ref.key)) != refs:
                raise EffectiveNError(f"{name} must be canonical exact-ref sorted")
        for name in (
            "design_authority_refs",
            "estimand_authority_refs",
            "authority_refs",
        ):
            refs = getattr(self, name)
            if tuple(sorted(set(refs), key=lambda ref: ref.key)) != refs:
                raise EffectiveNError(f"{name} must be canonical authority-ref sorted")

        if self.typed_state == "SUPPORTED":
            if self.weight_basis_id is None or self.authorized_weight_scope_ref is None:
                raise EffectiveNError("SUPPORTED effective-N requires exact weight basis and scope")
            if not self.weight_fact_refs:
                raise EffectiveNError("SUPPORTED effective-N requires exact weight facts")
            if not self.design_authority_refs or not self.estimand_authority_refs:
                raise EffectiveNError(
                    "SUPPORTED effective-N requires separate design and estimand authority bindings"
                )
            if self.sum_w is None or self.sum_w2 is None or self.effective_n is None:
                raise EffectiveNError("SUPPORTED effective-N requires exact numeric outputs")
            if self.sum_w <= 0 or self.sum_w2 <= 0:
                raise EffectiveNError("SUPPORTED effective-N requires positive nondegenerate sums")
            if self.effective_n != (self.sum_w * self.sum_w) / self.sum_w2:
                raise EffectiveNError("effective-N does not equal exact sum_w^2 / sum_w2")
        elif any(value is not None for value in (self.sum_w, self.sum_w2, self.effective_n)):
            raise EffectiveNError(
                "nonpositive effective-N states may not leak partial or fabricated numeric values"
            )

        expected_replay = _derived_ref(
            "PRE553_F018_EFFECTIVE_N_REPLAY",
            "effective-n-replay",
            self._replay_material(),
        )
        if self.replay_ref != expected_replay:
            raise EffectiveNError("effective-N replay identity mismatch")
        expected_product = _derived_ref(
            "PRE553_F018_EFFECTIVE_N_PRODUCT",
            "effective-n-product",
            self._product_material(),
        )
        if self.product_ref != expected_product:
            raise EffectiveNError("effective-N product identity mismatch")

    def _replay_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": self.contract_id,
            "formula_id": self.formula_id,
            "typed_state": self.typed_state,
            "empirical_fact_ref": self.empirical_fact_ref,
            "query_ref": self.query_ref,
            "release_refs": self.release_refs,
            "source_universe_refs": self.source_universe_refs,
            "risk_set_ref": self.risk_set_ref,
            "condition_predicate_ref": self.condition_predicate_ref,
            "measure_basis_ref": self.measure_basis_ref,
            "source_scope_mode": self.source_scope_mode,
            "target_topology_identity": self.target_topology_identity,
            "denominator_member_refs": self.denominator_member_refs,
            "weight_basis_id": self.weight_basis_id,
            "authorized_weight_scope_ref": self.authorized_weight_scope_ref,
            "weight_fact_refs": self.weight_fact_refs,
            "weight_source_refs": self.weight_source_refs,
            "design_authority_refs": self.design_authority_refs,
            "estimand_authority_refs": self.estimand_authority_refs,
            "authority_refs": self.authority_refs,
            "sum_w": self.sum_w,
            "sum_w2": self.sum_w2,
            "effective_n": self.effective_n,
            "provenance_refs": self.provenance_refs,
        }

    def _product_material(self) -> Mapping[str, Any]:
        return {
            **self._replay_material(),
            "replay_ref": self.replay_ref,
            "detail": self.detail,
        }

    def as_dict(self) -> dict[str, Any]:
        return canonicalize({
            **self._product_material(),
            "product_ref": self.product_ref,
        })


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(
        kind,
        f"urn:rawlsing:pre553:f018:{namespace}:sha256:{digest}",
        digest,
    )


def _canonical_refs(values: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return tuple(sorted(set(values), key=lambda ref: ref.key))


def _canonical_authorities(values: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    return tuple(sorted(set(values), key=lambda ref: ref.key))


def _as_exact_refs(values: Iterable[Any], name: str) -> tuple[ExactRef, ...]:
    return _canonical_refs(exact_ref(value, name) for value in values)


def _as_authority_refs(values: Iterable[Any], name: str) -> tuple[AuthorityRef, ...]:
    return _canonical_authorities(authority_ref(value, name) for value in values)


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise EffectiveNError(f"{name} must be an exact mapping")
    return value


def _fraction(value: Any, name: str) -> Fraction:
    if isinstance(value, bool):
        raise EffectiveNError(f"{name} cannot be boolean")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise EffectiveNError(f"{name} is empty")
        try:
            return Fraction(text)
        except (ValueError, ZeroDivisionError) as exc:
            raise EffectiveNError(f"{name} is not exact rational/decimal text") from exc
    if isinstance(value, Mapping):
        if set(value) == {"$exact_fraction"}:
            pair = value["$exact_fraction"]
            if (
                not isinstance(pair, Sequence)
                or isinstance(pair, (str, bytes, bytearray))
                or len(pair) != 2
                or not all(isinstance(item, int) and not isinstance(item, bool) for item in pair)
            ):
                raise EffectiveNError(f"{name} has invalid exact fraction")
            try:
                return Fraction(pair[0], pair[1])
            except ZeroDivisionError as exc:
                raise EffectiveNError(f"{name} has zero denominator") from exc
        if set(value) == {"$exact_decimal"} and isinstance(value["$exact_decimal"], str):
            try:
                return Fraction(value["$exact_decimal"])
            except (ValueError, ZeroDivisionError) as exc:
                raise EffectiveNError(f"{name} has invalid exact decimal") from exc
    raise EffectiveNError(f"{name} is not an accepted exact numeric representation")


def _verify_semantic_identity(obj: Any, expected_type: type, name: str) -> None:
    if not isinstance(obj, expected_type):
        raise EffectiveNError(f"{name} has wrong exact object type")
    if semantic_hash(obj.semantic_projection()) != obj.content_hash:
        raise EffectiveNError(f"{name} semantic projection/content hash mismatch")
    if obj.ref.object_id != obj.object_id or obj.ref.content_hash != obj.content_hash:
        raise EffectiveNError(f"{name} ExactRef identity mismatch")


def _positive_object_authorities(
    obj: EmpiricalFact | EmpiricalQuerySpec | WeightMeasureFact,
    registry: AuthorityRegistry,
) -> tuple[AuthorityRef, ...]:
    try:
        snapshots = validate_object_authority_closure(obj, registry)
    except Pre553AuthorityError:
        raise
    refs: list[AuthorityRef] = []
    for snapshot in snapshots:
        if snapshot.typed_state != "ALLOW":
            raise Pre553AuthorityError(
                f"{obj.schema_id} authority closure contains nonpositive exact snapshot"
            )
        refs.append(snapshot.authority_ref)
    return _canonical_authorities(refs)


def _base_context(
    *,
    fact: EmpiricalFact,
    query: EmpiricalQuerySpec,
    release_refs: Iterable[ExactRef],
    authority_registry: AuthorityRegistry,
) -> dict[str, Any]:
    _verify_semantic_identity(fact, EmpiricalFact, "fact")
    _verify_semantic_identity(query, EmpiricalQuerySpec, "query")

    fact_query_ref = exact_ref(fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref")
    if fact_query_ref != query.ref:
        raise EffectiveNError("fact/query exact identity mismatch")

    query_risk = exact_ref(query.risk_set_ref, "query.risk_set_ref")
    fact_risk = exact_ref(fact.risk_set_ref, "fact.risk_set_ref")
    if query_risk != fact_risk:
        raise EffectiveNError("fact/query risk-set exact identity mismatch")

    query_measure = exact_ref(query.measure_basis_ref, "query.measure_basis_ref")
    fact_measure = exact_ref(fact.measure_basis_ref, "fact.measure_basis_ref")
    if query_measure != fact_measure:
        raise EffectiveNError("fact/query measure-basis exact identity mismatch")

    query_universes = _as_exact_refs(query.empirical_universe_refs, "query.empirical_universe_refs")
    fact_universes = _as_exact_refs(fact.empirical_universe_refs, "fact.empirical_universe_refs")
    if query_universes != fact_universes:
        raise EffectiveNError("fact/query source-universe exact identity mismatch")

    releases = _canonical_refs(release_refs)
    if not releases:
        raise EffectiveNError("effective-N requires one or more exact source release refs")
    fact_provenance = _as_exact_refs(
        fact.source_empirical_provenance_refs,
        "fact.source_empirical_provenance_refs",
    )
    missing_releases = tuple(ref for ref in releases if ref not in fact_provenance)
    if missing_releases:
        raise EffectiveNError("supplied release ref is absent from exact EmpiricalFact provenance")

    fact_condition = exact_ref(fact.condition_predicate_ref, "fact.condition_predicate_ref")
    query_condition = exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref")
    if fact_condition != query_condition:
        raise EffectiveNError("fact/query condition predicate exact identity mismatch")

    denominator_members = _as_exact_refs(
        getattr(fact, "denominator_member_refs", ()),
        "fact.denominator_member_refs",
    )
    grain = _mapping(query.requested_output_grain, "query.requested_output_grain")
    measure_kind = grain.get("measure_kind")
    if measure_kind not in {"RAW", "GOVERNED_WEIGHTED"}:
        raise EffectiveNError("effective-N requires exact RAW or GOVERNED_WEIGHTED measure kind")

    fact_measure_kind = fact.semantic_fields.get("measure_kind")
    if fact_measure_kind is not None and fact_measure_kind != measure_kind:
        raise EffectiveNError("fact/query measure-kind mismatch")

    source_scope_mode = grain.get("source_scope_mode")
    if not isinstance(source_scope_mode, str) or not source_scope_mode.strip():
        raise EffectiveNError("query lacks exact source_scope_mode")

    fact_auth = _positive_object_authorities(fact, authority_registry)
    query_auth = _positive_object_authorities(query, authority_registry)

    return {
        "release_refs": releases,
        "fact_provenance": fact_provenance,
        "source_universe_refs": fact_universes,
        "risk_set_ref": fact_risk,
        "condition_predicate_ref": fact_condition,
        "measure_basis_ref": fact_measure,
        "source_scope_mode": source_scope_mode.strip(),
        "target_topology_identity": semantic_hash(fact.target_topology),
        "denominator_member_refs": denominator_members,
        "measure_kind": measure_kind,
        "grain": grain,
        "base_authority_refs": _canonical_authorities((*fact_auth, *query_auth)),
    }


def _make_product(
    *,
    state: str,
    fact: EmpiricalFact,
    query: EmpiricalQuerySpec,
    context: Mapping[str, Any],
    weight_basis_id: str | None,
    authorized_weight_scope_ref: ExactRef | None,
    weight_fact_refs: Iterable[ExactRef] = (),
    weight_source_refs: Iterable[ExactRef] = (),
    design_authority_refs: Iterable[AuthorityRef] = (),
    estimand_authority_refs: Iterable[AuthorityRef] = (),
    authority_refs: Iterable[AuthorityRef] = (),
    sum_w: Fraction | None = None,
    sum_w2: Fraction | None = None,
    effective_n: Fraction | None = None,
    extra_provenance_refs: Iterable[ExactRef] = (),
    detail: str,
) -> EffectiveNProduct:
    weight_refs = _canonical_refs(weight_fact_refs)
    source_refs = _canonical_refs(weight_source_refs)
    design_refs = _canonical_authorities(design_authority_refs)
    estimand_refs = _canonical_authorities(estimand_authority_refs)
    auth_refs = _canonical_authorities((*context["base_authority_refs"], *authority_refs))
    provenance = _canonical_refs((
        fact.ref,
        query.ref,
        *context["release_refs"],
        *context["fact_provenance"],
        *weight_refs,
        *source_refs,
        *extra_provenance_refs,
        *((authorized_weight_scope_ref,) if authorized_weight_scope_ref is not None else ()),
    ))

    prelim = {
        "contract_id": EFFECTIVE_N_CONTRACT_ID,
        "formula_id": EFFECTIVE_N_FORMULA_ID,
        "typed_state": state,
        "empirical_fact_ref": fact.ref,
        "query_ref": query.ref,
        "release_refs": context["release_refs"],
        "source_universe_refs": context["source_universe_refs"],
        "risk_set_ref": context["risk_set_ref"],
        "condition_predicate_ref": context["condition_predicate_ref"],
        "measure_basis_ref": context["measure_basis_ref"],
        "source_scope_mode": context["source_scope_mode"],
        "target_topology_identity": context["target_topology_identity"],
        "denominator_member_refs": context["denominator_member_refs"],
        "weight_basis_id": weight_basis_id,
        "authorized_weight_scope_ref": authorized_weight_scope_ref,
        "weight_fact_refs": weight_refs,
        "weight_source_refs": source_refs,
        "design_authority_refs": design_refs,
        "estimand_authority_refs": estimand_refs,
        "authority_refs": auth_refs,
        "sum_w": sum_w,
        "sum_w2": sum_w2,
        "effective_n": effective_n,
        "provenance_refs": provenance,
    }
    replay_ref = _derived_ref(
        "PRE553_F018_EFFECTIVE_N_REPLAY",
        "effective-n-replay",
        prelim,
    )
    product_material = {**prelim, "replay_ref": replay_ref, "detail": detail}
    product_ref = _derived_ref(
        "PRE553_F018_EFFECTIVE_N_PRODUCT",
        "effective-n-product",
        product_material,
    )
    return EffectiveNProduct(
        **prelim,
        replay_ref=replay_ref,
        product_ref=product_ref,
        detail=detail,
    )


def compute_effective_n(
    *,
    fact: EmpiricalFact,
    query: EmpiricalQuerySpec,
    weight_facts: Iterable[WeightMeasureFact],
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef],
    authorized_weight_scope_ref: ExactRef | Mapping[str, Any] | None,
) -> EffectiveNProduct:
    """Compute one governed F018 effective-N product from exact current inputs.

    The function never discovers a weight.  For governed weighted queries the
    query must already name the exact weight_basis_id and the caller must supply
    the exact authorized weight scope.  The denominator population is owned by
    I03 and is taken only from the supplied EmpiricalFact.
    """
    if not isinstance(authority_registry, AuthorityRegistry):
        raise EffectiveNError("authority_registry must be exact immutable AuthorityRegistry")
    context = _base_context(
        fact=fact,
        query=query,
        release_refs=release_refs,
        authority_registry=authority_registry,
    )
    weights = tuple(weight_facts)

    if context["measure_kind"] == "RAW":
        if weights or authorized_weight_scope_ref is not None:
            raise EffectiveNError(
                "RAW effective-N is not applicable and may not accept inferred or supplied weight inputs"
            )
        return _make_product(
            state="NOT_APPLICABLE",
            fact=fact,
            query=query,
            context=context,
            weight_basis_id=None,
            authorized_weight_scope_ref=None,
            detail=(
                "RAW/unweighted empirical grain has no authorized weighted estimand; "
                "respondent count is not effective-N"
            ),
        )

    # Caller presentation order is never an identity determinant.  Validate
    # exact objects first, then canonicalize the governed weight-fact set.
    for weight in weights:
        _verify_semantic_identity(weight, WeightMeasureFact, "weight_fact")
    weights = tuple(sorted(weights, key=lambda weight: weight.ref.key))

    weight_basis = context["grain"].get("weight_basis_id")
    if not isinstance(weight_basis, str) or not weight_basis.strip():
        raise EffectiveNError(
            "GOVERNED_WEIGHTED effective-N requires query-owned exact weight_basis_id; "
            "default weight inference is forbidden"
        )
    weight_basis = weight_basis.strip()

    if authorized_weight_scope_ref is None:
        return _make_product(
            state="NOT_AUTHORIZED",
            fact=fact,
            query=query,
            context=context,
            weight_basis_id=weight_basis,
            authorized_weight_scope_ref=None,
            detail="exact authorized weight scope is absent; no default scope or estimand is permitted",
        )
    scope_ref = exact_ref(authorized_weight_scope_ref, "authorized_weight_scope_ref")

    if fact.typed_state != "SUPPORTED":
        return _make_product(
            state="UPSTREAM_UNAVAILABLE",
            fact=fact,
            query=query,
            context=context,
            weight_basis_id=weight_basis,
            authorized_weight_scope_ref=scope_ref,
            detail=f"I03 fact state {fact.typed_state!r} does not expose a positive weighted denominator",
        )

    denominator_members = context["denominator_member_refs"]
    if not denominator_members:
        return _make_product(
            state="DEGENERATE_WEIGHT_SUM",
            fact=fact,
            query=query,
            context=context,
            weight_basis_id=weight_basis,
            authorized_weight_scope_ref=scope_ref,
            detail="exact I03 denominator membership is empty",
        )

    if not weights:
        return _make_product(
            state="NOT_AUTHORIZED",
            fact=fact,
            query=query,
            context=context,
            weight_basis_id=weight_basis,
            authorized_weight_scope_ref=scope_ref,
            detail="no exact governed weight facts were supplied for the I03 denominator",
        )

    fact_provenance = set(context["fact_provenance"])
    denominator_set = set(denominator_members)
    by_member: dict[ExactRef, list[WeightMeasureFact]] = {}
    weight_refs: list[ExactRef] = []
    weight_source_refs: list[ExactRef] = []
    design_refs: list[AuthorityRef] = []
    estimand_refs: list[AuthorityRef] = []
    all_auth_refs: list[AuthorityRef] = []
    exact_values: list[Fraction] = []

    for weight in weights:
        _verify_semantic_identity(weight, WeightMeasureFact, "weight_fact")
        weight_refs.append(weight.ref)

        member_ref = exact_ref(weight.scoped_respondent_ref, "weight.scoped_respondent_ref")
        universe_ref = exact_ref(weight.empirical_universe_ref, "weight.empirical_universe_ref")
        effective_scope = exact_ref(weight.effective_scope_ref, "weight.effective_scope_ref")
        source_ref = exact_ref(weight.weight_source_ref, "weight.weight_source_ref")
        weight_source_refs.append(source_ref)

        if member_ref not in denominator_set:
            return _make_product(
                state="SCOPE_MISMATCH",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                detail="weight fact respondent lies outside exact I03 denominator membership",
            )
        if universe_ref not in set(context["source_universe_refs"]):
            return _make_product(
                state="SCOPE_MISMATCH",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                detail="weight fact source universe lies outside exact I03 source scope",
            )
        if weight.weight_basis_id != weight_basis:
            return _make_product(
                state="SCOPE_MISMATCH",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                detail="weight fact basis does not equal query-owned exact weight_basis_id",
            )
        if effective_scope != scope_ref:
            return _make_product(
                state="SCOPE_MISMATCH",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                detail="weight fact effective_scope_ref does not equal authorized weight scope",
            )
        if weight.ref not in fact_provenance:
            return _make_product(
                state="SCOPE_MISMATCH",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                detail="weight fact was not consumed by the exact I03 fact provenance",
            )

        by_member.setdefault(member_ref, []).append(weight)

        if weight.typed_state in {"WEIGHT_NOT_AUTHORIZED", "WEIGHT_BASIS_UNRESOLVED"}:
            return _make_product(
                state="NOT_AUTHORIZED",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                detail=f"weight fact carries governed nonauthorization state {weight.typed_state}",
            )
        if weight.typed_state in {"WEIGHT_MISSING", "WEIGHT_INVALID"}:
            return _make_product(
                state="INVALID_WEIGHT",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                detail=f"weight fact carries unusable state {weight.typed_state}",
            )
        if weight.typed_state != "WEIGHT_VALID_AUTHORIZED":
            return _make_product(
                state="INVALID_WEIGHT",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                detail=f"unexpected weight state {weight.typed_state}",
            )

        try:
            object_auth_refs = _positive_object_authorities(weight, authority_registry)
        except Pre553AuthorityError:
            return _make_product(
                state="NOT_AUTHORIZED",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                detail="weight fact authority closure is absent or nonpositive",
            )
        all_auth_refs.extend(object_auth_refs)

        design_ref = authority_ref(weight.design_authority_ref, "weight.design_authority_ref")
        estimand_ref = authority_ref(weight.estimand_authority_ref, "weight.estimand_authority_ref")
        design_refs.append(design_ref)
        estimand_refs.append(estimand_ref)

        for label, ref in (("design", design_ref), ("estimand", estimand_ref)):
            try:
                snapshot = authority_registry.resolve_exact(ref).snapshot
            except Pre553AuthorityError:
                return _make_product(
                    state="NOT_AUTHORIZED",
                    fact=fact,
                    query=query,
                    context=context,
                    weight_basis_id=weight_basis,
                    authorized_weight_scope_ref=scope_ref,
                    weight_fact_refs=weight_refs,
                    weight_source_refs=weight_source_refs,
                    design_authority_refs=design_refs,
                    estimand_authority_refs=estimand_refs,
                    authority_refs=all_auth_refs,
                    detail=f"exact {label} authority is unavailable; no default is permitted",
                )
            if snapshot.typed_state != "ALLOW" or snapshot.authority_kind != "WEIGHT_DESIGN_ESTIMAND":
                return _make_product(
                    state="NOT_AUTHORIZED",
                    fact=fact,
                    query=query,
                    context=context,
                    weight_basis_id=weight_basis,
                    authorized_weight_scope_ref=scope_ref,
                    weight_fact_refs=weight_refs,
                    weight_source_refs=weight_source_refs,
                    design_authority_refs=design_refs,
                    estimand_authority_refs=estimand_refs,
                    authority_refs=(*all_auth_refs, snapshot.authority_ref),
                    detail=f"exact {label} authority is not positive WEIGHT_DESIGN_ESTIMAND authority",
                )
            all_auth_refs.append(snapshot.authority_ref)

        try:
            value = _fraction(
                weight.exact_weight_value_representation,
                "weight.exact_weight_value_representation",
            )
        except EffectiveNError:
            return _make_product(
                state="INVALID_WEIGHT",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                design_authority_refs=design_refs,
                estimand_authority_refs=estimand_refs,
                authority_refs=all_auth_refs,
                detail="weight value is not an exact lawful numeric representation",
            )
        if value < 0:
            return _make_product(
                state="INVALID_WEIGHT",
                fact=fact,
                query=query,
                context=context,
                weight_basis_id=weight_basis,
                authorized_weight_scope_ref=scope_ref,
                weight_fact_refs=weight_refs,
                weight_source_refs=weight_source_refs,
                design_authority_refs=design_refs,
                estimand_authority_refs=estimand_refs,
                authority_refs=all_auth_refs,
                detail="negative governed respondent weight is invalid for effective-N",
            )
        exact_values.append(value)

    if set(by_member) != denominator_set or any(len(items) != 1 for items in by_member.values()):
        return _make_product(
            state="NOT_AUTHORIZED" if set(by_member) < denominator_set else "SCOPE_MISMATCH",
            fact=fact,
            query=query,
            context=context,
            weight_basis_id=weight_basis,
            authorized_weight_scope_ref=scope_ref,
            weight_fact_refs=weight_refs,
            weight_source_refs=weight_source_refs,
            design_authority_refs=design_refs,
            estimand_authority_refs=estimand_refs,
            authority_refs=all_auth_refs,
            detail=(
                "exact one-to-one governed weight coverage of the I03 denominator is absent"
                if set(by_member) < denominator_set
                else "multiple weight facts compete for one exact I03 denominator member"
            ),
        )

    sum_w = sum(exact_values, Fraction(0, 1))
    sum_w2 = sum((value * value for value in exact_values), Fraction(0, 1))
    if sum_w <= 0 or sum_w2 <= 0:
        return _make_product(
            state="DEGENERATE_WEIGHT_SUM",
            fact=fact,
            query=query,
            context=context,
            weight_basis_id=weight_basis,
            authorized_weight_scope_ref=scope_ref,
            weight_fact_refs=weight_refs,
            weight_source_refs=weight_source_refs,
            design_authority_refs=design_refs,
            estimand_authority_refs=estimand_refs,
            authority_refs=all_auth_refs,
            detail="exact governed weight sums are zero or degenerate; numerical effective-N is unavailable",
        )

    fact_weighted_denominator = fact.weighted_denominator_support_if_authorized
    if fact_weighted_denominator is None:
        return _make_product(
            state="UPSTREAM_UNAVAILABLE",
            fact=fact,
            query=query,
            context=context,
            weight_basis_id=weight_basis,
            authorized_weight_scope_ref=scope_ref,
            weight_fact_refs=weight_refs,
            weight_source_refs=weight_source_refs,
            design_authority_refs=design_refs,
            estimand_authority_refs=estimand_refs,
            authority_refs=all_auth_refs,
            detail="I03 fact does not expose an authorized weighted denominator",
        )
    if _fraction(fact_weighted_denominator, "fact.weighted_denominator_support_if_authorized") != sum_w:
        return _make_product(
            state="SCOPE_MISMATCH",
            fact=fact,
            query=query,
            context=context,
            weight_basis_id=weight_basis,
            authorized_weight_scope_ref=scope_ref,
            weight_fact_refs=weight_refs,
            weight_source_refs=weight_source_refs,
            design_authority_refs=design_refs,
            estimand_authority_refs=estimand_refs,
            authority_refs=all_auth_refs,
            detail="effective-N weight sum does not reproduce the exact I03 weighted denominator",
        )

    effective_n = (sum_w * sum_w) / sum_w2
    return _make_product(
        state="SUPPORTED",
        fact=fact,
        query=query,
        context=context,
        weight_basis_id=weight_basis,
        authorized_weight_scope_ref=scope_ref,
        weight_fact_refs=weight_refs,
        weight_source_refs=weight_source_refs,
        design_authority_refs=design_refs,
        estimand_authority_refs=estimand_refs,
        authority_refs=all_auth_refs,
        sum_w=sum_w,
        sum_w2=sum_w2,
        effective_n=effective_n,
        detail="exact governed weighted effective-N resolved at the I03 denominator/risk-set/query grain",
    )


def replay_effective_n(
    *,
    expected_product_ref: ExactRef,
    expected_replay_ref: ExactRef,
    **kwargs: Any,
) -> EffectiveNProduct:
    """Recompute and require exact product plus replay identity."""
    product = compute_effective_n(**kwargs)
    if product.product_ref != expected_product_ref:
        raise EffectiveNError("effective-N deterministic replay product identity mismatch")
    if product.replay_ref != expected_replay_ref:
        raise EffectiveNError("effective-N deterministic replay ref mismatch")
    return product


__all__ = [
    "EFFECTIVE_N_CONTRACT_ID",
    "EFFECTIVE_N_FORMULA_ID",
    "EFFECTIVE_N_STATES",
    "EffectiveNError",
    "EffectiveNProduct",
    "compute_effective_n",
    "replay_effective_n",
]
