from __future__ import annotations

import hashlib
import json

import pytest

from rawlsing_next.pre553_fracture_map_invalidation import (
    DependencyAddressedIdentityLedger,
    SelectiveInvalidationError,
    SelectiveInvalidationMismatch,
)


def _graph():
    return {
        "ROOT": ("TARGET",),
        "P_CONFORMER": ("ROOT", "P"),
        "P_DEVIANT": ("ROOT", "P"),
        "ALT_CONVERGER": ("ROOT", "P"),
        "ALT_MINORITY": ("ROOT", "P"),
        "Q_CHILD": ("P_DEVIANT", "Q"),
        "S_CHILD": ("Q_CHILD", "S"),
        "R_TOPO": ("ROOT", "R"),
        "COSIG": ("Q_CHILD",),
        "J3": ("ROOT",),
    }


def _semantics(r_support=(14, 6)):
    return {
        "ROOT": {"morphology": "ROOT_STABLE"},
        "P_CONFORMER": {"branch": "P_CONFORMER"},
        "P_DEVIANT": {"branch": "P_DEVIANT"},
        "ALT_CONVERGER": {"branch": "ALT_CONVERGER"},
        "ALT_MINORITY": {"branch": "ALT_MINORITY"},
        "Q_CHILD": {"branch": "Q_CHILD"},
        "S_CHILD": {"branch": "S_CHILD"},
        "R_TOPO": {"r0_support": r_support[0], "r1_support": r_support[1]},
        "COSIG": {"closure": "C1_C2_BRANCH_COSIGNATURE"},
        "J3": {"source_kind": "EXACT_SAME_RESPONDENT_JOINT", "arity": 3},
    }


def _determinants(r="0", target="v1"):
    return {"TARGET": target, "P": "v1", "Q": "v1", "R": r, "S": "v1"}


def _ledger(*, r="0", target="v1", semantics=None, release="release-A"):
    return DependencyAddressedIdentityLedger(
        determinant_values=_determinants(r=r, target=target),
        dependency_graph=_graph(),
        artifact_semantics=_semantics() if semantics is None else semantics,
        provenance_refs={name: ({"kind": "C11LogicalRelease", "ref": release},) for name in _graph()},
    )


def _legacy_release_coupled_identities(release: str, semantics):
    result = {}
    for artifact, semantic in semantics.items():
        payload = json.dumps(
            {"artifact": artifact, "source_release_ref": release, "semantic": semantic},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        result[artifact] = hashlib.sha256(payload).hexdigest()
    return result


def test_ac11_reproduces_old_global_release_overinvalidation_then_repairs_selectively():
    before_semantics = _semantics((14, 6))
    after_semantics = _semantics((13, 7))

    # Exact old failure mechanism: a one-row R mutation changes whole-source release
    # identity, so every release-coupled artifact identity churns even though only R
    # semantics changed.
    legacy_before = _legacy_release_coupled_identities("release-before", before_semantics)
    legacy_after = _legacy_release_coupled_identities("release-after", after_semantics)
    assert set(legacy_before) == {
        name for name in legacy_before if legacy_before[name] != legacy_after[name]
    }

    before = _ledger(r="0", semantics=before_semantics, release="release-before")
    after = _ledger(r="1", semantics=after_semantics, release="release-after")
    receipt = before.compare(after, changed_determinants=("R",))

    assert receipt.expected_invalidated_artifacts == ("R_TOPO",)
    assert receipt.observed_invalidated_artifacts == ("R_TOPO",)
    assert set(receipt.stable_artifacts) == {
        "ROOT",
        "P_CONFORMER",
        "P_DEVIANT",
        "ALT_CONVERGER",
        "ALT_MINORITY",
        "Q_CHILD",
        "S_CHILD",
        "COSIG",
        "J3",
    }
    assert before.receipt("ROOT")["provenance_refs"] != after.receipt("ROOT")["provenance_refs"]
    assert before.identity("ROOT") == after.identity("ROOT")


def test_truly_upstream_target_determinant_invalidates_all_and_only_lawful_descendants():
    before = _ledger(target="target-v1")
    after = _ledger(target="target-v2")
    receipt = before.compare(after, changed_determinants=("TARGET",))
    assert set(receipt.expected_invalidated_artifacts) == set(_graph())
    assert receipt.observed_invalidated_artifacts == receipt.expected_invalidated_artifacts
    assert receipt.stable_artifacts == ()


def test_dependency_local_change_propagates_through_artifact_edges_only():
    before = _ledger()
    changed = _semantics()
    changed["Q_CHILD"] = {"branch": "Q_CHILD_CHANGED"}
    after = _ledger(semantics=changed)

    # No determinant changed; this is an artifact-semantic mutation.  The identities
    # of Q_CHILD and its artifact descendants must move, while independent branches do not.
    b = before.identities()
    a = after.identities()
    moved = {name for name in b if b[name] != a[name]}
    assert moved == {"Q_CHILD", "S_CHILD", "COSIG"}


def test_replay_identity_is_deterministic_under_mapping_and_dependency_order_permutation():
    graph = {k: tuple(reversed(v)) for k, v in reversed(list(_graph().items()))}
    semantics = dict(reversed(list(_semantics().items())))
    determinants = dict(reversed(list(_determinants().items())))
    a = _ledger()
    b = DependencyAddressedIdentityLedger(
        determinant_values=determinants,
        dependency_graph=graph,
        artifact_semantics=semantics,
        provenance_refs={name: ({"ref": "different-storage-order-only"},) for name in graph},
    )
    # provenance can differ without becoming invalidation identity; semantic/dependency
    # inputs are the same.
    assert dict(a.identities()) == dict(b.identities())


def test_source_release_or_replay_ref_cannot_leak_into_selective_semantic_projection():
    bad = _semantics()
    bad["ROOT"] = {"morphology": "ROOT_STABLE", "source_release_ref": "global-release"}
    with pytest.raises(SelectiveInvalidationError, match="not selective-invalidation semantic material"):
        DependencyAddressedIdentityLedger(
            determinant_values=_determinants(),
            dependency_graph=_graph(),
            artifact_semantics=bad,
        )


def test_cycle_unknown_dependency_and_mutated_graph_fail_closed():
    cyclic = _graph()
    cyclic["ROOT"] = ("J3", "TARGET")
    with pytest.raises(SelectiveInvalidationError, match="cycle"):
        DependencyAddressedIdentityLedger(
            determinant_values=_determinants(), dependency_graph=cyclic, artifact_semantics=_semantics()
        )

    unknown = _graph()
    unknown["ROOT"] = ("TARGET", "UNKNOWN_DETERMINANT")
    with pytest.raises(SelectiveInvalidationError, match="unknown determinant/artifact"):
        DependencyAddressedIdentityLedger(
            determinant_values=_determinants(), dependency_graph=unknown, artifact_semantics=_semantics()
        )

    before = _ledger()
    changed_graph = _graph()
    changed_graph["Q_CHILD"] = ("P_DEVIANT", "Q", "R")
    after = DependencyAddressedIdentityLedger(
        determinant_values=_determinants(r="1"),
        dependency_graph=changed_graph,
        artifact_semantics=_semantics((13, 7)),
    )
    with pytest.raises(SelectiveInvalidationMismatch, match="dependency graph mutated"):
        before.compare(after, changed_determinants=("R",))
