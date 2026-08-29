"""Authority-45 dependency-addressed fracture-map invalidation identities.

This module separates two identities which must not be collapsed:

* immutable content/provenance identity (source releases, replay refs, exact facts), and
* selective invalidation identity (only the local semantic projection and the exact
  determinant/artifact dependencies declared by the frozen dependency graph).

The latter is the identity required by I08 AC11/AC12.  A whole-source release ref is
therefore preserved in provenance receipts but cannot silently invalidate topology that
does not depend on the changed determinant.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

SELECTIVE_INVALIDATION_CONTRACT_ID = (
    "PRE553_AUTH45_FRACTUREMAP_SELECTIVE_INVALIDATION@1.0.0"
)

# These are immutable provenance/address fields, not local semantic effects.  They may
# be carried by the receipt, but admitting them into the dependency-addressed semantic
# projection recreates the AC11 over-invalidation defect.
_FORBIDDEN_PROVENANCE_KEYS = frozenset({
    "source_release_ref",
    "source_release_refs",
    "source_empirical_provenance_refs",
    "producer_replay_locator_or_reference_root",
    "replay_ref",
    "dependency_refs",
    "content_hash",
    "object_id",
})


class SelectiveInvalidationError(ValueError):
    """Dependency-addressed identity material is incomplete or unlawful."""


class SelectiveInvalidationMismatch(SelectiveInvalidationError):
    """Observed invalidation does not equal exact dependency reachability."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SelectiveInvalidationError(f"{name} must be a non-empty string")
    return value.strip()


def _canonical(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, Mapping):
        return {
            str(key): _canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    if isinstance(value, (set, frozenset)):
        normalized = [_canonical(item) for item in value]
        return sorted(
            normalized,
            key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")),
        )
    if hasattr(value, "as_dict") and callable(value.as_dict):
        return _canonical(value.as_dict())
    raise SelectiveInvalidationError(
        f"unsupported identity material type: {type(value).__name__}"
    )


def _hash(value: Any) -> str:
    encoded = json.dumps(
        _canonical(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _reject_provenance_leak(value: Any, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            name = str(key)
            here = f"{path}.{name}"
            if name in _FORBIDDEN_PROVENANCE_KEYS:
                raise SelectiveInvalidationError(
                    f"provenance/address field {name!r} is not selective-invalidation "
                    f"semantic material at {here}"
                )
            _reject_provenance_leak(item, here)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for index, item in enumerate(value):
            _reject_provenance_leak(item, f"{path}[{index}]")


def _canonical_graph(
    graph: Mapping[str, Iterable[str]],
) -> Mapping[str, tuple[str, ...]]:
    if not isinstance(graph, Mapping) or not graph:
        raise SelectiveInvalidationError("dependency_graph must be a non-empty mapping")
    result: dict[str, tuple[str, ...]] = {}
    for raw_artifact, raw_deps in graph.items():
        artifact = _text(raw_artifact, "artifact id")
        if isinstance(raw_deps, (str, bytes, bytearray)):
            raise SelectiveInvalidationError(
                f"dependency list for {artifact} must be an iterable of exact names"
            )
        deps = tuple(sorted({_text(dep, f"dependency of {artifact}") for dep in raw_deps}))
        if artifact in deps:
            raise SelectiveInvalidationError(f"self dependency is forbidden: {artifact}")
        result[artifact] = deps
    return MappingProxyType(dict(sorted(result.items())))


def _canonical_mapping(value: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise SelectiveInvalidationError(f"{name} must be a mapping")
    return MappingProxyType(dict(sorted((str(k), _canonical(v)) for k, v in value.items())))


def _canonical_provenance(
    value: Mapping[str, Iterable[Any]] | None,
) -> Mapping[str, tuple[Any, ...]]:
    rows: dict[str, tuple[Any, ...]] = {}
    for raw_artifact, raw_refs in (value or {}).items():
        artifact = _text(raw_artifact, "provenance artifact id")
        if isinstance(raw_refs, (str, bytes, bytearray)):
            raw_refs = (raw_refs,)
        canonical = [_canonical(ref) for ref in raw_refs]
        canonical.sort(
            key=lambda ref: json.dumps(ref, sort_keys=True, separators=(",", ":"))
        )
        rows[artifact] = tuple(canonical)
    return MappingProxyType(dict(sorted(rows.items())))


@dataclass(frozen=True)
class SelectiveInvalidationComparison:
    changed_determinants: tuple[str, ...]
    expected_invalidated_artifacts: tuple[str, ...]
    observed_invalidated_artifacts: tuple[str, ...]
    stable_artifacts: tuple[str, ...]
    status: str = "PASS"

    def as_dict(self) -> dict[str, Any]:
        return {
            "contract_id": SELECTIVE_INVALIDATION_CONTRACT_ID,
            "changed_determinants": list(self.changed_determinants),
            "expected_invalidated_artifacts": list(self.expected_invalidated_artifacts),
            "observed_invalidated_artifacts": list(self.observed_invalidated_artifacts),
            "stable_artifacts": list(self.stable_artifacts),
            "status": self.status,
        }


class DependencyAddressedIdentityLedger:
    """Deterministic, dependency-local invalidation identity map.

    `provenance_refs` are intentionally excluded from the identity hash. They remain
    exact audit material in `receipt()` and may not be smuggled into `artifact_semantics`.
    """

    def __init__(
        self,
        *,
        determinant_values: Mapping[str, Any],
        dependency_graph: Mapping[str, Iterable[str]],
        artifact_semantics: Mapping[str, Any],
        provenance_refs: Mapping[str, Iterable[Any]] | None = None,
    ) -> None:
        self._determinants = _canonical_mapping(determinant_values, "determinant_values")
        self._graph = _canonical_graph(dependency_graph)
        self._semantics = _canonical_mapping(artifact_semantics, "artifact_semantics")
        self._provenance = _canonical_provenance(provenance_refs)

        graph_keys = set(self._graph)
        semantic_keys = set(self._semantics)
        if graph_keys != semantic_keys:
            missing_semantics = sorted(graph_keys - semantic_keys)
            missing_graph = sorted(semantic_keys - graph_keys)
            raise SelectiveInvalidationError(
                "dependency_graph and artifact_semantics must name the same artifacts; "
                f"missing_semantics={missing_semantics}; missing_graph={missing_graph}"
            )
        unknown_provenance = sorted(set(self._provenance) - graph_keys)
        if unknown_provenance:
            raise SelectiveInvalidationError(
                f"provenance references name unknown artifacts: {unknown_provenance}"
            )
        for artifact, semantic in self._semantics.items():
            _reject_provenance_leak(semantic, f"$.artifact_semantics.{artifact}")
        for artifact, deps in self._graph.items():
            for dep in deps:
                if dep not in self._determinants and dep not in self._graph:
                    raise SelectiveInvalidationError(
                        f"{artifact} depends on unknown determinant/artifact {dep!r}"
                    )
        # Force full graph traversal now so cycles fail during construction.
        for artifact in self._graph:
            self.dependency_closure(artifact)

    @property
    def determinant_values(self) -> Mapping[str, Any]:
        return self._determinants

    @property
    def dependency_graph(self) -> Mapping[str, tuple[str, ...]]:
        return self._graph

    def dependency_closure(self, artifact: str) -> tuple[str, ...]:
        artifact = _text(artifact, "artifact")
        if artifact not in self._graph:
            raise SelectiveInvalidationError(f"unknown artifact {artifact!r}")
        closure: set[str] = set()
        visited_artifacts: set[str] = set()
        active: set[str] = set()

        def visit(node: str) -> None:
            if node in active:
                raise SelectiveInvalidationError(
                    f"dependency graph cycle detected through {node!r}"
                )
            if node in visited_artifacts:
                return
            active.add(node)
            for dep in self._graph[node]:
                closure.add(dep)
                if dep in self._graph:
                    visit(dep)
            active.remove(node)
            visited_artifacts.add(node)

        visit(artifact)
        return tuple(sorted(closure))

    def determinant_dependencies(self, artifact: str) -> tuple[str, ...]:
        return tuple(
            item for item in self.dependency_closure(artifact) if item in self._determinants
        )

    def _identity(self, artifact: str, cache: dict[str, str], active: set[str]) -> str:
        if artifact in cache:
            return cache[artifact]
        if artifact in active:
            raise SelectiveInvalidationError(
                f"dependency graph cycle detected through {artifact!r}"
            )
        active.add(artifact)
        dependencies: list[dict[str, Any]] = []
        for dep in self._graph[artifact]:
            if dep in self._determinants:
                dependencies.append({
                    "kind": "DETERMINANT",
                    "name": dep,
                    "value": self._determinants[dep],
                })
            else:
                dependencies.append({
                    "kind": "ARTIFACT",
                    "name": dep,
                    "identity": self._identity(dep, cache, active),
                })
        material = {
            "contract_id": SELECTIVE_INVALIDATION_CONTRACT_ID,
            "artifact_id": artifact,
            "local_semantic_projection": self._semantics[artifact],
            "direct_dependencies": dependencies,
        }
        digest = _hash(material)
        active.remove(artifact)
        cache[artifact] = digest
        return digest

    def identity(self, artifact: str) -> str:
        artifact = _text(artifact, "artifact")
        if artifact not in self._graph:
            raise SelectiveInvalidationError(f"unknown artifact {artifact!r}")
        return self._identity(artifact, {}, set())

    def identities(self) -> Mapping[str, str]:
        cache: dict[str, str] = {}
        for artifact in self._graph:
            self._identity(artifact, cache, set())
        return MappingProxyType(dict(sorted(cache.items())))

    def receipt(self, artifact: str) -> Mapping[str, Any]:
        artifact = _text(artifact, "artifact")
        return MappingProxyType({
            "contract_id": SELECTIVE_INVALIDATION_CONTRACT_ID,
            "artifact_id": artifact,
            "selective_invalidation_identity": self.identity(artifact),
            "direct_dependencies": list(self._graph[artifact]),
            "determinant_dependencies": list(self.determinant_dependencies(artifact)),
            "provenance_refs": list(self._provenance.get(artifact, ())),
            "provenance_refs_are_identity_bearing": False,
        })

    def compare(
        self,
        other: "DependencyAddressedIdentityLedger",
        *,
        changed_determinants: Iterable[str],
    ) -> SelectiveInvalidationComparison:
        if not isinstance(other, DependencyAddressedIdentityLedger):
            raise SelectiveInvalidationError("other must be DependencyAddressedIdentityLedger")
        if dict(self._graph) != dict(other._graph):
            raise SelectiveInvalidationMismatch(
                "dependency graph mutated during selective-invalidation comparison"
            )
        if set(self._semantics) != set(other._semantics):
            raise SelectiveInvalidationMismatch("artifact set changed during comparison")
        changed = tuple(sorted({_text(x, "changed determinant") for x in changed_determinants}))
        for determinant in changed:
            if determinant not in self._determinants or determinant not in other._determinants:
                raise SelectiveInvalidationError(
                    f"changed determinant {determinant!r} is not present in both ledgers"
                )
            if self._determinants[determinant] == other._determinants[determinant]:
                raise SelectiveInvalidationMismatch(
                    f"declared changed determinant {determinant!r} did not change"
                )
        undeclared_changes = sorted(
            key for key in set(self._determinants) | set(other._determinants)
            if self._determinants.get(key) != other._determinants.get(key) and key not in changed
        )
        if undeclared_changes:
            raise SelectiveInvalidationMismatch(
                f"undeclared determinant changes present: {undeclared_changes}"
            )

        expected = tuple(sorted(
            artifact for artifact in self._graph
            if set(self.determinant_dependencies(artifact)) & set(changed)
        ))
        before = self.identities()
        after = other.identities()
        observed = tuple(sorted(
            artifact for artifact in self._graph if before[artifact] != after[artifact]
        ))
        if expected != observed:
            expected_set, observed_set = set(expected), set(observed)
            over = sorted(observed_set - expected_set)
            under = sorted(expected_set - observed_set)
            raise SelectiveInvalidationMismatch(
                "selective invalidation mismatch; "
                f"over_invalidated={over}; under_invalidated={under}"
            )
        stable = tuple(sorted(set(self._graph) - set(expected)))
        return SelectiveInvalidationComparison(
            changed_determinants=changed,
            expected_invalidated_artifacts=expected,
            observed_invalidated_artifacts=observed,
            stable_artifacts=stable,
        )


__all__ = [
    "SELECTIVE_INVALIDATION_CONTRACT_ID",
    "SelectiveInvalidationError",
    "SelectiveInvalidationMismatch",
    "SelectiveInvalidationComparison",
    "DependencyAddressedIdentityLedger",
]
