"""Public PRE553 I03 exact empirical query executor.

Population empirical computation only: no discovery, structural admission, V553,
generated-position mapping, actor/V3/V2 state, rendering, legacy fallback or cutover.
"""
from __future__ import annotations

from dataclasses import replace
from typing import Any, Iterable, Mapping

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
    _ConditionMemo,
    _CountryConstituentMemo,
    _build_negative_fact,
    _evaluate_index_group,
    _evaluate_index_group_core,
    _group_core_fingerprint,
    _materialize_grouped_evaluation,
    _predicate_identity,
    _registry_fingerprint,
    _respondent_root,
    _target_plan_identity,
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


# The E1 builder freezes the respondent dictionaries into mapping proxies and
# values into tuples. Hold their original object identities separately from the
# mutable cache slot: checking these references is constant-time per cache hit,
# unlike rehashing or traversing the full respondent graph per query.
_I03_INDEX_ATTESTED_FIELDS = (
    "release", "universe", "respondents", "events_by_respondent",
    "coordinates_by_respondent", "routing_by_respondent",
    "weights_by_respondent", "source_relations", "runtime_authorities",
    "runtime_repository", "runtime_predicate_grammar_authority_ref",
    "routing_lookup", "native_verified_physical_respondent_order",
)
_I03_INDEX_MISSING = object()


def _i03_index_attestation(index: _ReleaseIndex) -> tuple[object, ...]:
    return (index,) + tuple(
        getattr(index, name) for name in _I03_INDEX_ATTESTED_FIELDS
    )


def _i03_index_attestation_matches(
    index: object, attestation: object,
) -> bool:
    return (
        isinstance(index, _ReleaseIndex)
        and isinstance(attestation, tuple)
        and len(attestation) == len(_I03_INDEX_ATTESTED_FIELDS) + 1
        and attestation[0] is index
        and all(
            getattr(index, name, _I03_INDEX_MISSING) is original
            for name, original in zip(
                _I03_INDEX_ATTESTED_FIELDS, attestation[1:]
            )
        )
    )


def _release_index_for(
    repository: C11Repository, release: C11LogicalRelease, universe_ref: ExactRef,
) -> _ReleaseIndex:
    key = (release.release_ref, universe_ref)
    # An entry merely claiming the same release/universe is insufficient. E2
    # demonstrated that a substituted respondent map otherwise changes a
    # SUPPORTED native fact. Never evaluate an un-attested cache payload.
    with repository._i03_index_lock:
        index = repository._i03_release_indices.get(key)
        attestation = repository._i03_index_attestations.get(key)
        if (
            not _i03_index_attestation_matches(index, attestation)
            or index.release is not release
            or index.universe.ref != universe_ref
        ):
            # Recompute ONLY from the sealed I02 release, under the original
            # per-repository lock. No cache/attestation grants source authority.
            rebuilt = _build_release_index(release, universe_ref)
            repository._i03_release_indices[key] = rebuilt
            repository._i03_index_attestations[key] = _i03_index_attestation(rebuilt)
            index = rebuilt
        return index


def install_sourcefree_i02_certified_i03_range(
    repository: C11Repository,
    *,
    release_ref: ExactRef,
    universe_ref: ExactRef,
    witness: Any,
    independently_held_root: str,
) -> None:
    """Opt in ONE exact I02-sealed sourcefree release to verified I03 selection.

    This owner method does not accept caller-created postings, issue a source
    permission, mint an I02 seal, certify source-native science, or install a
    durable saved view. It uses the complete *existing* I02 release as its
    separate provenance oracle. Publication into the ordinary I03 derived
    cache occurs only after all original-source and exact-keyspace checks
    succeed. The normal execute_empirical_query path then reads the same
    attested index; callers cannot substitute a Protocol or index object.
    """
    if type(repository) is not C11Repository:
        raise EmpiricalQueryResolutionError(
            "S2-A sourcefree installation requires the native exact C11Repository"
        )
    release = _resolve_release_exact(repository, release_ref)
    from rawlsing_next._pre553_verified_semantic_range import certified_i03_events

    selected = certified_i03_events(
        release, universe_ref, witness=witness,
        independently_held_root=independently_held_root,
    )
    native = _build_release_index(release, universe_ref)
    if set(selected) != set(native.respondents):
        raise EmpiricalQueryResolutionError(
            "sourcefree certified selector respondent domain differs from I02"
        )
    index = replace(native, events_by_respondent=selected)
    attestation = _i03_index_attestation(index)
    key = (release.release_ref, universe_ref)
    # No code path can observe a half-installed cache pair. A failed
    # certification leaves the previously accepted native index untouched.
    with repository._i03_index_lock:
        if repository.resolve_release_exact(release_ref) is not release:
            raise EmpiricalQueryResolutionError(
                "exact sourcefree release changed during index installation"
            )
        repository._i03_release_indices[key] = index
        repository._i03_index_attestations[key] = attestation


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
            if any(getattr(obj, "ref", None) == universe_ref for obj in release._public_non_events):
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


class I03GroupedExecutionScope:
    """Finite, execution-local reuse of exact measure-independent I03 cores.

    The scope is a context-managed, nonauthoritative memo owned by one workload
    execution. It stores only routing/risk membership, condition truth, exact
    target cell resolution, and the used object/authority material for a
    demonstrably compatible core. Every operation still validates its own
    identity, source binding, index attestation, authority/issuance/revocation
    state, and builds its own native EmpiricalFact, provenance, and replay.

    The core key excludes measure/weight/design deliberately: those determinants
    do not govern the measure-independent core, and RAW/GOVERNED_WEIGHTED
    aggregation plus all weight validation is recomputed per operation. No
    weighted result is cached or reused across measure regimes.
    """

    _SCHEMA = "PRE553_I03_GROUPED_EXECUTION_SCOPE@1"

    def __init__(
        self,
        *,
        max_groups: int = 64,
        max_cached_members: int = 500_000,
        max_condition_bytes: int = 16*1024*1024,
        rolling_groups: bool = False,
        max_constituent_bytes: int = 0,
    ) -> None:
        if type(max_constituent_bytes) is not int or max_constituent_bytes<0:
            raise ValueError("max_constituent_bytes must be a nonnegative integer")
        self._max_constituent_bytes=max_constituent_bytes
        self._constituent_bytes=0
        self._constituent_memos={}
        if type(rolling_groups) is not bool:
            raise ValueError("explicit boolean rolling group selection required")
        self._rolling_groups=rolling_groups
        if not isinstance(max_groups, int) or isinstance(max_groups, bool) or max_groups < 1:
            raise ValueError("max_groups must be a positive integer")
        if (
            not isinstance(max_cached_members, int)
            or isinstance(max_cached_members, bool)
            or max_cached_members < 1
        ):
            raise ValueError("max_cached_members must be a positive integer")
        if type(max_condition_bytes) is not int or max_condition_bytes<0:
            raise ValueError("max_condition_bytes must be a nonnegative integer")
        self._max_condition_bytes=max_condition_bytes
        self._condition_bytes=0
        self._condition_memos={}
        self._max_groups = max_groups
        self._max_cached_members = max_cached_members
        self._cache: dict[tuple, Any] = {}
        self._index_identities: dict[int, tuple[Any, tuple]] = {}
        self._registry_identities: dict[int, tuple[Any, str]] = {}
        self._closed = False
        self._stats = {
            "core_build_attempts": 0,
            "core_builds": 0,
            "core_hits": 0,
            "core_evictions": 0,
            "fingerprint_failures": 0,
            "capacity_fallbacks": 0,
            "early_capacity_fallbacks": 0,
            "fallbacks": 0,
            "raw_materializations": 0,
            "weighted_materializations": 0,
        }

    def __enter__(self) -> "I03GroupedExecutionScope":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def close(self) -> None:
        self._cache.clear()
        self._condition_memos.clear()
        self._condition_bytes=0
        self._constituent_memos.clear()
        self._constituent_bytes=0
        self._index_identities.clear()
        self._registry_identities.clear()
        self._closed = True

    def receipt(self) -> Mapping[str, Any]:
        return {
            "schema": self._SCHEMA,
            "closed": self._closed,
            "open_groups": len(self._cache),
            "max_groups": self._max_groups,
            "max_cached_members": self._max_cached_members,
            "rolling_groups":self._rolling_groups,
            "retained_core_units":sum(self._retention_units(x) for x in self._cache.values()),
            "constituent_cache_bytes_estimate":self._constituent_bytes,
            "constituent_legacy_bytes_same_retained_rows":sum(m.legacy_bytes for m in self._constituent_memos.values()),
            "constituent_retained_rows":sum(m.retained_rows for m in self._constituent_memos.values()),
            "constituent_planes":sum(len(m.planes) for m in self._constituent_memos.values()),
            "constituent_shared_respondents":sum(len(m.respondent_keys) for m in self._constituent_memos.values()),
            "constituent_shared_authority_sets":sum(len(m.authority_sets) for m in self._constituent_memos.values()),
            "constituent_compact_identities":sum(m.compact_identities for m in self._constituent_memos.values()),
            "constituent_explicit_identities":sum(m.explicit_identities for m in self._constituent_memos.values()),
            "constituent_cache_hits":{k:sum(m.hits[k] for m in self._constituent_memos.values())
                                      for k in ("routing","target")},
            "constituent_cache_misses":{k:sum(m.misses[k] for m in self._constituent_memos.values())
                                        for k in ("routing","target")},
            "constituent_cache_refusals":sum(m.refusals for m in self._constituent_memos.values()),
            "condition_cache_bytes_estimate":self._condition_bytes,
            "condition_cache_hits":sum(m.hits for m in self._condition_memos.values()),
            "condition_cache_misses":sum(m.misses for m in self._condition_memos.values()),
            "condition_capacity_fallbacks":sum(m.capacity_fallbacks for m in self._condition_memos.values()),
            **self._stats,
        }

    def _index_identity(self, index) -> tuple:
        entry = self._index_identities.get(id(index))
        if entry is not None and entry[0] is index:
            return entry[1]
        release = index.release
        identity = (
            release.release_ref.key,
            release.semantic_release_hash,
            release.source_release_manifest_hash,
            release.replay_manifest.ref.key,
            index.universe.ref.key,
            id(index),
            _respondent_root(index),
            len(index.respondents),
            len(index.events_by_respondent),
            len(index.coordinates_by_respondent),
            len(index.routing_by_respondent),
            len(index.weights_by_respondent),
        )
        self._index_identities[id(index)] = (index, identity)
        return identity

    def _registry_identity(self, registry) -> str:
        entry = self._registry_identities.get(id(registry))
        if entry is not None and entry[0] is registry:
            return entry[1]
        identity = _registry_fingerprint(registry)
        # Catalog may create one validated registry per operation. Do not
        # retain every registry for a long distinct-query workload.
        if len(self._registry_identities)>=8:
            self._registry_identities.pop(next(iter(self._registry_identities)))
        self._registry_identities[id(registry)] = (registry, identity)
        return identity

    def _core_key(self, *, index, query, predicate, plan, profile, registry):
        try:
            from rawlsing_next.pre553_runtime_context import current_runtime_binding

            runtime_binding = current_runtime_binding()
        except ImportError:
            runtime_binding = None
        if runtime_binding is not None:
            return None
        if (
            index.runtime_authorities is not None
            or index.runtime_repository is not None
            or index.runtime_predicate_grammar_authority_ref is not None
        ):
            return None
        return (
            self._SCHEMA,
            self._index_identity(index),
            (
                _exact(query.risk_set_ref, "query.risk_set_ref").key,
                profile.risk_set_type,
                profile.source_scope_mode,
                _exact(
                    profile.response_state_semantics_ref,
                    "response_state_semantics_ref",
                ).key,
            ),
            _predicate_identity(predicate),
            _target_plan_identity(plan),
            tuple(sorted(
                _authority(ref, "query.query_authority_refs").key
                for ref in query.query_authority_refs
            )),
            self._registry_identity(registry),
            "MEASURE_INDEPENDENT_CORE",
        )

    def _condition_memo_for(self,index,registry,predicate):
        if self._closed or not self._max_condition_bytes:
            return None
        if (index.runtime_authorities is not None or index.runtime_repository is not None
                or index.runtime_predicate_grammar_authority_ref is not None):
            return None
        from rawlsing_next.pre553_runtime_context import current_runtime_binding
        if current_runtime_binding() is not None:
            return None
        key=(self._index_identity(index),self._registry_identity(registry),_predicate_identity(predicate))
        memo=self._condition_memos.get(key)
        if memo is not None:
            return memo if memo.compatible(index,registry,predicate) else None
        # Cap the number of condition plans as well as retained row evidence.
        if len(self._condition_memos)>=self._max_groups:
            return None
        def budget(cost):
            if self._condition_bytes+cost>self._max_condition_bytes:
                return False
            self._condition_bytes+=cost
            return True
        memo=_ConditionMemo(index,registry,predicate,budget)
        self._condition_memos[key]=memo
        return memo

    def _constituent_memo_for(self,index,registry):
        from rawlsing_next._pre553_query_predicate import _CountryRoutingLookup
        from rawlsing_next.pre553_runtime_context import current_runtime_binding
        if (self._closed or not self._max_constituent_bytes
                or current_runtime_binding() is not None
                or type(index.routing_lookup) is not _CountryRoutingLookup
                or index.runtime_authorities is not None
                or index.runtime_repository is not None
                or index.runtime_predicate_grammar_authority_ref is not None):
            return None
        key=(self._index_identity(index),self._registry_identity(registry))
        memo=self._constituent_memos.get(key)
        if memo is not None:
            return memo if memo.compatible(index,registry) else None
        if len(self._constituent_memos)>=self._max_groups:return None
        def budget(cost):
            if self._constituent_bytes+cost>self._max_constituent_bytes:return False
            self._constituent_bytes+=cost
            return True
        memo=_CountryConstituentMemo(index,registry,budget)
        self._constituent_memos[key]=memo
        return memo

    def _retention_units(self,core):
        # A zero-denominator core can still retain a full risk set and
        # provenance. Continuing use is bounded by total retained entries,
        # not just successful denominator members. Not a byte/RSS guarantee.
        if not self._rolling_groups:
            return len(core.denominator_members)
        return (len(core.denominator_members)+len(core.risk_members)
                +len(core.used_objects)+len(core.used_authority_refs)
                +len(core.cell_by_respondent)+len(core.raw_cells)+len(core.cell_material)
                +len(core.unresolved_condition_member_refs))

    def _miss_capacity_exhausted(self, cached_members: int) -> bool:
        """Return True only when no new core can fit the current bounds.

        This is the early cache-MISS guard. An existing cache HIT is always
        evaluated before this check, so full-capacity cores remain reusable.
        The member condition is exact only when the already-cached member count
        has reached the cap; a prospective unknown denominator is still checked
        after core construction, preserving the honest fallback bound.
        """
        return (
            len(self._cache) >= self._max_groups
            or cached_members >= self._max_cached_members
        )

    def evaluate(
        self,
        *,
        index,
        query,
        predicate,
        plan,
        profile,
        registry,
    ):
        if self._closed:
            self._stats["fallbacks"] += 1
            return None
        try:
            key = self._core_key(
                index=index, query=query, predicate=predicate, plan=plan,
                profile=profile, registry=registry,
            )
        except Exception:
            self._stats["fallbacks"] += 1
            return None
        if key is None:
            self._stats["fallbacks"] += 1
            return None
        entry = self._cache.get(key)
        if entry is not None:
            if entry.index is not index:
                self._cache.pop(key, None)
                self._stats["fingerprint_failures"] += 1
                return None
            if _group_core_fingerprint(entry) != entry.fingerprint:
                self._cache.pop(key, None)
                self._stats["fingerprint_failures"] += 1
                return None
            self._stats["core_hits"] += 1
            if self._rolling_groups:
                # Dict insertion order is the bounded recency queue. No
                # change to cache identity or per-hit proof.
                self._cache.pop(key)
                self._cache[key]=entry
            try:
                evaluation = _materialize_grouped_evaluation(
                    entry, plan=plan, profile=profile, registry=registry,
                )
            except Exception:
                self._stats["fallbacks"] += 1
                return None
            self._stats[
                "weighted_materializations"
                if profile.measure_kind == "GOVERNED_WEIGHTED"
                else "raw_materializations"
            ] += 1
            return evaluation
        cached_members = sum(
            self._retention_units(existing) for existing in self._cache.values()
        )
        if not self._rolling_groups and self._miss_capacity_exhausted(cached_members):
            self._stats["capacity_fallbacks"] += 1
            self._stats["early_capacity_fallbacks"] += 1
            return None
        self._stats["core_build_attempts"] += 1
        try:
            core = _evaluate_index_group_core(
                index,
                query=query,
                predicate=predicate,
                plan=plan,
                profile=profile,
                registry=registry,
                condition_memo=self._condition_memo_for(index,registry,predicate),
                constituent_memo=self._constituent_memo_for(index,registry),
            )
        except Exception:
            self._stats["fallbacks"] += 1
            return None
        size=self._retention_units(core)
        if self._rolling_groups and size<=self._max_cached_members:
            while self._cache and (len(self._cache)>=self._max_groups
                   or cached_members+size>self._max_cached_members):
                evicted=self._cache.pop(next(iter(self._cache)))
                cached_members-=self._retention_units(evicted)
                self._stats["core_evictions"]+=1
        if (
            len(self._cache) >= self._max_groups
            or cached_members + size > self._max_cached_members
        ):
            self._stats["capacity_fallbacks"] += 1
            # Capacity limits govern retention, not truth. The complete
            # exact measure-independent core has already been evaluated.
            # Materialize it once rather than re-running the respondent
            # scan solely because we cannot retain its derivative graph.
        else:
            self._cache[key] = core
            self._stats["core_builds"] += 1
        try:
            evaluation = _materialize_grouped_evaluation(
                core, plan=plan, profile=profile, registry=registry,
            )
        except Exception:
            self._stats["fallbacks"] += 1
            return None
        self._stats[
            "weighted_materializations"
            if profile.measure_kind == "GOVERNED_WEIGHTED"
            else "raw_materializations"
        ] += 1
        return evaluation


def execute_empirical_query(
    *,
    repository: C11Repository,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef],
    group_scope: "I03GroupedExecutionScope | None" = None,
) -> QueryExecutionResult:
    """Execute one exact P02 query against one exact sealed C11 source scope.

    Identity/hash tampering raises and cannot be laundered into a semantic state.
    Lawful but nonpositive runtime outcomes are returned as typed EmpiricalFacts.
    """
    # This is the ORIGINAL I03 semantics owner. A strictly verified S2-C
    # sourcefree saved-read session may supply the same _ReleaseIndex inputs;
    # it is not passed off as a validated v1 C11Repository or a science issuer.
    from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
    if not isinstance(repository, C11Repository) and type(repository) is not DirectEstateI03Session:
        raise EmpiricalQueryExecutionError(
            "repository must be accepted I02 C11Repository or exact verified S2-C I03 session"
        )
    if type(repository) is DirectEstateI03Session and group_scope is not None:
        raise EmpiricalQueryExecutionError("grouped native I03 cache not yet qualified for cold sourcefree estate")
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
        resolved = (
            _resolve_release_indices(repository, query=query, release_refs=supplied_releases)
            if isinstance(repository, C11Repository)
            else repository.indices_for(query=query, release_refs=supplied_releases)
        )
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
                    group_scope=group_scope,
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
                group_scope=group_scope,
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
                group_scope=group_scope,
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
    "I03GroupedExecutionScope",
    "install_sourcefree_i02_certified_i03_range",
    "execute_empirical_query",
    "replay_empirical_query",
    "QueryExecutionResult",
    "EmpiricalQueryExecutionError",
    "EmpiricalQueryResolutionError",
]
