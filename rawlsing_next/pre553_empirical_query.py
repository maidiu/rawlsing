"""Public PRE553 I03 exact empirical query executor.

Population empirical computation only: no discovery, structural admission, V553,
generated-position mapping, actor/V3/V2 state, rendering, legacy fallback or cutover.
"""
from __future__ import annotations

from typing import Iterable, Mapping

from rawlsing_next._pre553_query_common import (
    AuthorityRef,
    AuthorityRegistry,
    C11LogicalRelease,
    C11Repository,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQueryExecutionError,
    EmpiricalQueryResolutionError,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553AuthorityError,
    Pre553SemanticCollapseError,
    QueryExecutionResult,
    SOURCE_SCOPE_MODES,
    UnsupportedResponseTopology,
    _authority,
    _canonical_authorities,
    _canonical_refs,
    _exact,
    _parse_target_plan,
    _profile,
    _ReleaseIndex,
    _require_mapping,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_authority import require_positive_authority
from rawlsing_next._pre553_query_eval import (
    _build_fact,
    _build_negative_fact,
    _evaluate_index_group,
)
from rawlsing_next._pre553_query_predicate import (
    _build_release_index,
    _validate_public_object_authorities,
)


def _verify_public_identity(obj: EmpiricalQuerySpec | EmpiricalPredicate) -> None:
    if semantic_hash(obj.semantic_projection()) != obj.content_hash:
        raise EmpiricalQueryExecutionError(
            f"{obj.schema_id} semantic projection/content hash mismatch"
        )
    if obj.ref.object_id != obj.object_id or obj.ref.content_hash != obj.content_hash:
        raise EmpiricalQueryExecutionError(f"{obj.schema_id} ExactRef identity mismatch")


def _resolve_release_exact(repository: C11Repository, ref: ExactRef) -> C11LogicalRelease:
    try:
        return repository.resolve_release_exact(ref)
    except KeyError as exc:
        raise EmpiricalQueryResolutionError(
            "exact C11 release unavailable; no latest/default/fuzzy/nearest fallback permitted"
        ) from exc


def _release_index_for(
    repository: C11Repository, release: C11LogicalRelease, universe_ref: ExactRef,
) -> _ReleaseIndex:
    key = (release.release_ref, universe_ref)
    with repository._i03_index_lock:
        index = repository._i03_release_indices.get(key)
        if index is None or index.release is not release or index.universe.ref != universe_ref:
            index = _build_release_index(release, universe_ref)
            repository._i03_release_indices[key] = index
        return index


def _resolve_release_indices(
    repository: C11Repository,
    *,
    query: EmpiricalQuerySpec,
    release_refs: Iterable[ExactRef],
):
    universe_refs = _canonical_refs(
        _exact(value, "query.empirical_universe_refs") for value in query.empirical_universe_refs
    )
    supplied = _canonical_refs(_exact(ref, "release_refs") for ref in release_refs)
    if not supplied:
        raise EmpiricalQueryResolutionError("one or more exact C11 release refs are required")
    releases = tuple(_resolve_release_exact(repository, ref) for ref in supplied)
    resolved = []
    used_release_refs: set[ExactRef] = set()
    for universe_ref in universe_refs:
        matches = []
        for release in releases:
            if any(getattr(obj, "ref", None) == universe_ref for obj in release.public_objects):
                matches.append((release.release_ref, _release_index_for(repository, release, universe_ref)))
        if len(matches) != 1:
            raise EmpiricalQueryResolutionError(
                "each exact query universe must resolve in exactly one supplied sealed C11 release"
            )
        release_ref, index = matches[0]
        resolved.append((universe_ref, index))
        used_release_refs.add(release_ref)
    if set(supplied) != used_release_refs:
        raise EmpiricalQueryResolutionError(
            "supplied release_refs include a release outside the exact query source scope"
        )
    return tuple(resolved)


def _authorized_composite_refs(
    query: EmpiricalQuerySpec,
    registry: AuthorityRegistry,
) -> tuple[AuthorityRef, ...]:
    grain = _require_mapping(query.requested_output_grain, "requested_output_grain")
    raw = grain.get("authorized_composite_authority_refs")
    if not isinstance(raw, Mapping):
        raise Pre553AuthorityError(
            "AUTHORIZED_COMPOSITE requires an exact operation-specific authority bundle"
        )
    role_kinds = {
        "pooling": frozenset({"SOURCE_COMPOSITION_POOLING"}),
        "nonduplication": frozenset({"SOURCE_UNIVERSE_RELATION"}),
        "estimand_composition": frozenset({"SOURCE_COMPOSITION_POOLING", "WEIGHT_DESIGN_ESTIMAND"}),
    }
    if not set(role_kinds).issubset(raw):
        raise Pre553AuthorityError(
            "AUTHORIZED_COMPOSITE authority bundle must bind pooling, nonduplication and estimand composition"
        )
    universe_refs = _canonical_refs(
        _exact(value, "query.empirical_universe_refs") for value in query.empirical_universe_refs
    )
    refs: list[AuthorityRef] = []
    for role in sorted(role_kinds):
        entry = _require_mapping(raw[role], f"authorized_composite_authority_refs.{role}")
        if set(entry) != {"authority_ref", "operation"}:
            raise Pre553AuthorityError(
                f"composite {role} binding must contain exact authority_ref and operation only"
            )
        ref = _authority(entry["authority_ref"], f"authorized_composite_authority_refs.{role}.authority_ref")
        operation = entry["operation"]
        if not isinstance(operation, str) or not operation.strip():
            raise Pre553AuthorityError(f"composite {role} operation must be an exact non-empty string")
        snapshot = registry.resolve_exact(ref).snapshot
        if snapshot.authority_kind not in role_kinds[role]:
            raise Pre553AuthorityError(
                f"composite {role} authority kind {snapshot.authority_kind!r} is not sufficient"
            )
        for universe_ref in universe_refs:
            require_positive_authority(
                snapshot,
                authority_kind=snapshot.authority_kind,
                operation=operation.strip(),
                source_universe_ref=universe_ref.as_dict(),
            )
        refs.append(ref)
    return _canonical_authorities(refs)


def _failure_code(exc: Exception) -> tuple[str, str]:
    text = str(exc).lower()
    if isinstance(exc, UnsupportedResponseTopology):
        return "UNRESOLVED", "UNSUPPORTED_RESPONSE_TOPOLOGY"
    if isinstance(exc, Pre553AuthorityError):
        if "weight" in text or "measure" in text:
            return "UNAVAILABLE", "MEASURE_UNAVAILABLE"
        return "UNAVAILABLE", "MISSING_REQUIRED_AUTHORITY"
    if isinstance(exc, EmpiricalQueryResolutionError):
        if "routing" in text or "risk-set" in text or "risk set" in text:
            return "UNAVAILABLE", "RISK_SET_UNAVAILABLE"
        if "weight" in text or "measure" in text:
            return "UNAVAILABLE", "MEASURE_UNAVAILABLE"
        if "release" in text or "universe" in text or "source" in text:
            return "UNAVAILABLE", "SOURCE_SCOPE_UNAVAILABLE"
        return "UNRESOLVED", "UNRESOLVED"
    if isinstance(exc, EmpiricalQueryExecutionError):
        return "INTEGRITY_FAILURE", "INTEGRITY_FAILURE"
    return "INTEGRITY_FAILURE", "INTEGRITY_FAILURE"


def _negative_result(
    *,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    profile,
    p01_state: str,
    p02_state: str,
    detail: str,
    universe_refs: Iterable[ExactRef],
    release_refs: Iterable[ExactRef],
) -> QueryExecutionResult:
    universes = _canonical_refs(universe_refs)
    releases = _canonical_refs(release_refs)
    if profile.source_scope_mode == "SOURCE_INDEXED_MULTI_UNIVERSE" and len(universes) > 1:
        facts = tuple(
            sorted(
                (
                    _build_negative_fact(
                        query=query, predicate=predicate, profile=profile,
                        p01_state=p01_state, p02_failure_state=p02_state, detail=detail,
                        universe_refs=(universe_ref,), release_refs=releases,
                    )
                    for universe_ref in universes
                ),
                key=lambda fact: fact.ref.key,
            )
        )
    else:
        facts = (
            _build_negative_fact(
                query=query, predicate=predicate, profile=profile,
                p01_state=p01_state, p02_failure_state=p02_state, detail=detail,
                universe_refs=universes, release_refs=releases,
            ),
        )
    return QueryExecutionResult(
        query_ref=query.ref,
        facts=facts,
        source_scope_mode=profile.source_scope_mode,
        release_refs=releases,
    )


def _negative_for_index(
    *, query, predicate, profile, index, exc: Exception,
) -> EmpiricalFact:
    p01, p02 = _failure_code(exc)
    return _build_negative_fact(
        query=query,
        predicate=predicate,
        profile=profile,
        p01_state=p01,
        p02_failure_state=p02,
        detail=str(exc),
        universe_refs=(index.universe.ref,),
        release_refs=(index.release.release_ref,),
    )


def _require_exact_i03_authority_fitness(
    *,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    authority_registry: AuthorityRegistry,
    universe_refs: tuple[ExactRef, ...],
) -> None:
    """Require operation/family/source/use fitness at the shared I03 boundary.

    Object closure proves that referenced snapshots exist and are positive.  It
    does not prove that an ALLOW snapshot governs this exact operation, public
    object family, source universe, or declared target use.  Shared execution
    therefore performs that fit check itself instead of relying on a stronger
    caller/wrapper having done so earlier.
    """
    query_authority_refs = _canonical_authorities(
        _authority(ref, "query.query_authority_refs")
        for ref in query.query_authority_refs
    )
    if not query_authority_refs:
        raise Pre553AuthorityError("I03 query requires exact query_authority_refs")

    grammar_ref = _authority(predicate.grammar_authority_ref, "predicate.grammar_authority_ref")
    try:
        from rawlsing_next.pre553_runtime_context import current_runtime_binding
        runtime_binding = current_runtime_binding()
    except ImportError:
        runtime_binding = None
    runtime = None if runtime_binding is None else runtime_binding.authorities
    runtime_grammar = (
        runtime is not None
        and runtime.is_positive_runtime_predicate_authority(grammar_ref)
    )
    if grammar_ref not in query_authority_refs and not runtime_grammar:
        raise Pre553AuthorityError(
            "predicate grammar authority is not an exact query authority"
        )
    if runtime_grammar:
        runtime.validate_predicate(predicate)

    snapshots = tuple(
        authority_registry.resolve_exact(ref).snapshot for ref in query_authority_refs
    )
    grain = _require_mapping(query.requested_output_grain, "requested_output_grain")
    explicit_query_operation = grain.get("query_operation")
    if explicit_query_operation is not None:
        if not isinstance(explicit_query_operation, str) or not explicit_query_operation.strip():
            raise Pre553AuthorityError("query_operation must be an exact non-empty string")
        query_operation = explicit_query_operation.strip()
    else:
        operation_sets = tuple(tuple(snapshot.governed_operations) for snapshot in snapshots)
        if any(len(operations) != 1 for operations in operation_sets):
            raise Pre553AuthorityError(
                "I03 query operation is ambiguous; exact query_operation or singleton authority operation required"
            )
        inferred = {operations[0] for operations in operation_sets}
        if len(inferred) != 1:
            raise Pre553AuthorityError(
                "I03 query authorities do not agree on one exact operation"
            )
        query_operation = next(iter(inferred))

    for snapshot in snapshots:
        for family in (
            "EmpiricalPredicate@1.0.0",
            "EmpiricalQuerySpec@1.0.0",
            "EmpiricalFact@1.0.0",
        ):
            for universe_ref in universe_refs:
                try:
                    require_positive_authority(
                        snapshot,
                        authority_kind="PREDICATE_GRAMMAR",
                        operation=query_operation,
                        object_family=family,
                        source_universe_ref=universe_ref.as_dict(),
                    )
                except Pre553AuthorityError:
                    if runtime is None:
                        raise
                    runtime.authorize_i03_operation_successor(
                        snapshot=snapshot,
                        historical_parent_snapshot=runtime.resolve_exact_runtime_authority(
                            snapshot.authority_ref
                        ),
                        runtime_catalog_identity=runtime_binding.runtime_catalog_identity,
                        query=query,
                        requested_operation=query_operation,
                        universe_refs=universe_refs,
                        required_object_family=family,
                    )

    target_keys = (
        "target_use_ref",
        "target_use_authority_ref",
        "target_use_operation",
    )
    declared_target_keys = tuple(
        key for key in target_keys if grain.get(key) is not None
    )
    if declared_target_keys and len(declared_target_keys) != len(target_keys):
        raise Pre553AuthorityError(
            "I03 target-use permission must bind ref, authority, and operation together"
        )
    if not declared_target_keys:
        return

    target_use_ref = _exact(grain["target_use_ref"], "requested_output_grain.target_use_ref")
    target_use_authority_ref = _authority(
        grain["target_use_authority_ref"],
        "requested_output_grain.target_use_authority_ref",
    )
    target_use_operation = grain["target_use_operation"]
    if not isinstance(target_use_operation, str) or not target_use_operation.strip():
        raise Pre553AuthorityError("target_use_operation must be an exact non-empty string")
    target_use_operation = target_use_operation.strip()

    query_closure_authorities = _canonical_authorities(
        _authority(ref, "query.authority_snapshot_refs")
        for ref in query.authority_snapshot_refs
    )
    if target_use_authority_ref not in query_closure_authorities:
        raise Pre553AuthorityError(
            "target-use authority is not present in exact query authority closure"
        )
    query_dependencies = _canonical_refs(
        _exact(ref, "query.dependency_refs") for ref in query.dependency_refs
    )
    if target_use_ref not in query_dependencies:
        raise Pre553AuthorityError(
            "target-use ref is not present in exact query dependency closure"
        )

    snapshot = authority_registry.resolve_exact(target_use_authority_ref).snapshot
    for universe_ref in universe_refs:
        require_positive_authority(
            snapshot,
            authority_kind="TARGET_USE_PERMISSION",
            operation=target_use_operation,
            object_family="EmpiricalFact@1.0.0",
            source_universe_ref=universe_ref.as_dict(),
            target_use_ref=target_use_ref.as_dict(),
        )


def execute_empirical_query(
    *,
    repository: C11Repository,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef],
) -> QueryExecutionResult:
    """Execute one exact P02 query against one exact sealed C11 source scope.

    Identity/hash tampering raises and cannot be laundered into a semantic state.
    Lawful but nonpositive runtime outcomes are returned as typed EmpiricalFacts.
    """
    if not isinstance(repository, C11Repository):
        raise EmpiricalQueryExecutionError("repository must be accepted I02 C11Repository")
    if not isinstance(query, EmpiricalQuerySpec):
        raise EmpiricalQueryExecutionError("query must be EmpiricalQuerySpec@1.0.0")
    if not isinstance(predicate, EmpiricalPredicate):
        raise EmpiricalQueryExecutionError("predicate must be EmpiricalPredicate@1.0.0")
    if not isinstance(authority_registry, AuthorityRegistry):
        raise EmpiricalQueryExecutionError(
            "authority_registry must be exact immutable AuthorityRegistry"
        )
    _verify_public_identity(query)
    _verify_public_identity(predicate)
    if query.typed_state != "QUERY_AUTHORIZED_RESOLVABLE":
        raise Pre553AuthorityError(
            f"query state {query.typed_state!r} is not executable as positive empirical query"
        )
    if predicate.typed_state != "PREDICATE_RESOLVED_AUTHORIZED":
        raise Pre553AuthorityError(
            f"predicate state {predicate.typed_state!r} is not executable as positive empirical predicate"
        )
    condition_ref = _exact(query.condition_predicate_ref, "query.condition_predicate_ref")
    if condition_ref != predicate.ref:
        raise EmpiricalQueryResolutionError(
            "query condition_predicate_ref does not exactly match supplied predicate identity"
        )

    universe_refs = _canonical_refs(
        _exact(value, "query.empirical_universe_refs") for value in query.empirical_universe_refs
    )
    supplied_releases = _canonical_refs(_exact(ref, "release_refs") for ref in release_refs)
    profile = _profile(query)
    _exact(query.risk_set_ref, "query.risk_set_ref")
    _exact(query.measure_basis_ref, "query.measure_basis_ref")

    try:
        _validate_public_object_authorities(query, authority_registry)
        _validate_public_object_authorities(predicate, authority_registry)
        _require_exact_i03_authority_fitness(
            query=query,
            predicate=predicate,
            authority_registry=authority_registry,
            universe_refs=universe_refs,
        )
        plan = _parse_target_plan(query, authority_registry)
    except Pre553SemanticCollapseError:
        raise
    except (UnsupportedResponseTopology, Pre553AuthorityError, EmpiricalQueryExecutionError) as exc:
        p01, p02 = _failure_code(exc)
        return _negative_result(
            query=query, predicate=predicate, profile=profile,
            p01_state=p01, p02_state=p02, detail=str(exc),
            universe_refs=universe_refs, release_refs=supplied_releases,
        )

    try:
        resolved = _resolve_release_indices(repository, query=query, release_refs=supplied_releases)
    except EmpiricalQueryResolutionError as exc:
        p01, p02 = _failure_code(exc)
        return _negative_result(
            query=query, predicate=predicate, profile=profile,
            p01_state=p01, p02_state=p02, detail=str(exc),
            universe_refs=universe_refs, release_refs=supplied_releases,
        )
    indices = tuple(item[1] for item in resolved)

    if profile.source_scope_mode not in SOURCE_SCOPE_MODES:
        raise EmpiricalQueryExecutionError("unknown source scope mode")
    if profile.source_scope_mode == "SINGLE_UNIVERSE" and len(indices) != 1:
        return _negative_result(
            query=query, predicate=predicate, profile=profile,
            p01_state="INTEGRITY_FAILURE", p02_state="INTEGRITY_FAILURE",
            detail="SINGLE_UNIVERSE query must bind exactly one universe",
            universe_refs=universe_refs, release_refs=supplied_releases,
        )
    if profile.source_scope_mode in {"SOURCE_INDEXED_MULTI_UNIVERSE", "AUTHORIZED_COMPOSITE"} and len(indices) < 2:
        return _negative_result(
            query=query, predicate=predicate, profile=profile,
            p01_state="INTEGRITY_FAILURE", p02_state="INTEGRITY_FAILURE",
            detail=f"{profile.source_scope_mode} requires at least two exact universes",
            universe_refs=universe_refs, release_refs=supplied_releases,
        )

    facts: list[EmpiricalFact] = []
    if profile.source_scope_mode == "SOURCE_INDEXED_MULTI_UNIVERSE":
        for index in indices:
            try:
                evaluation = _evaluate_index_group(
                    (index,), query=query, predicate=predicate, plan=plan,
                    profile=profile, registry=authority_registry,
                )
                fact = _build_fact(
                    (index,), query=query, predicate=predicate, plan=plan,
                    profile=profile, evaluation=evaluation, registry=authority_registry,
                )
            except (UnsupportedResponseTopology, Pre553AuthorityError,
                    EmpiricalQueryResolutionError, EmpiricalQueryExecutionError) as exc:
                fact = _negative_for_index(
                    query=query, predicate=predicate, profile=profile, index=index, exc=exc
                )
            facts.append(fact)

    elif profile.source_scope_mode == "AUTHORIZED_COMPOSITE":
        try:
            composite_refs = _authorized_composite_refs(query, authority_registry)
        except Pre553AuthorityError as exc:
            return _negative_result(
                query=query, predicate=predicate, profile=profile,
                p01_state="NONCOMPARABLE", p02_state="UNRESOLVED_SOURCE_RELATION",
                detail=str(exc), universe_refs=universe_refs, release_refs=supplied_releases,
            )
        try:
            evaluation = _evaluate_index_group(
                indices, query=query, predicate=predicate, plan=plan,
                profile=profile, registry=authority_registry,
            )
            facts.append(_build_fact(
                indices, query=query, predicate=predicate, plan=plan,
                profile=profile, evaluation=evaluation, registry=authority_registry,
                extra_authority_refs=composite_refs,
            ))
        except (UnsupportedResponseTopology, Pre553AuthorityError,
                EmpiricalQueryResolutionError, EmpiricalQueryExecutionError) as exc:
            p01, p02 = _failure_code(exc)
            return _negative_result(
                query=query, predicate=predicate, profile=profile,
                p01_state=p01, p02_state=p02, detail=str(exc),
                universe_refs=universe_refs, release_refs=supplied_releases,
            )

    else:
        index = indices[0]
        try:
            evaluation = _evaluate_index_group(
                indices, query=query, predicate=predicate, plan=plan,
                profile=profile, registry=authority_registry,
            )
            facts.append(_build_fact(
                indices, query=query, predicate=predicate, plan=plan,
                profile=profile, evaluation=evaluation, registry=authority_registry,
            ))
        except (UnsupportedResponseTopology, Pre553AuthorityError,
                EmpiricalQueryResolutionError, EmpiricalQueryExecutionError) as exc:
            facts.append(_negative_for_index(
                query=query, predicate=predicate, profile=profile, index=index, exc=exc
            ))

    canonical_facts = tuple(sorted(facts, key=lambda fact: fact.ref.key))
    canonical_releases = _canonical_refs(index.release.release_ref for index in indices)
    return QueryExecutionResult(
        query_ref=query.ref,
        facts=canonical_facts,
        source_scope_mode=profile.source_scope_mode,
        release_refs=canonical_releases,
    )


def replay_empirical_query(
    *,
    repository: C11Repository,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef],
    expected_fact_refs: Iterable[ExactRef],
) -> QueryExecutionResult:
    """Replay and require exact fact identities; cache/materialization is nonauthoritative."""
    result = execute_empirical_query(
        repository=repository,
        query=query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=release_refs,
    )
    expected = _canonical_refs(_exact(ref, "expected_fact_refs") for ref in expected_fact_refs)
    actual = tuple(fact.ref for fact in result.facts)
    if actual != expected:
        raise EmpiricalQueryExecutionError(
            "deterministic replay mismatch: exact fact identities differ"
        )
    return result


__all__ = [
    "execute_empirical_query",
    "replay_empirical_query",
    "QueryExecutionResult",
    "EmpiricalQueryExecutionError",
    "EmpiricalQueryResolutionError",
]
