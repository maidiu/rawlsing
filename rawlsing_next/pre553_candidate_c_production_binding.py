"""Governed current production binding for PRE553 Candidate C.

Candidate C owns a physical realization policy, not empirical semantics.  The
frozen Candidate-C owner identity is preserved here while exact-source fallback
delegates C11 construction to the already-authoritative source-backed facade.
No accelerator can create source meaning, alter C11/I03/I05 truth, or define
candidate reachability.

The current admitted LiTS-I F02 projection requires material outside the frozen
CACC1/CACC2 scope (including q310/q311), so its lawful Candidate-C realization
is exact-source-backed.  WVS7 has zero permitted Candidate-C accelerators and is
also exact-source-backed.  In both cases Candidate C remains Candidate C.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.pre553_source_backed_c11_facade import (
    CONTRACT_ID as SOURCE_BACKED_C11_CONTRACT_ID,
    GovernedC11Projection,
    build_source_backed_c11_repository,
)


CONTRACT_ID = "PRE553_CANDIDATE_C_PRODUCTION_BINDING@1.0.0"
CANDIDATE_ID = "C"
CANDIDATE_POLICY = "SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS"

# Frozen accepted Candidate-C policy/implementation owner.  This module does not
# replace that owner; it binds the owner's already-accepted zero-accelerator
# state to the common semantic C11 owner.
CANDIDATE_C_OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
CANDIDATE_C_OWNER_PATH = "rawlsing_next/pre553_route_c_accelerators.py"
CANDIDATE_C_OWNER_BLOB = "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889"
CANDIDATE_C_HASH = "a476e6e44c21b8029ae5d3e6d387428a5fa19549a2126d61aae7c71c50c64a3c"

CACC1_ID = "CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE"
CACC2_ID = "CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK"
KNOWN_ACCELERATORS = frozenset((CACC1_ID, CACC2_ID))

LITS_I_SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
LITS_I_CURRENT_PROJECTION_CACHE_IDENTITY = "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
WVS7_SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
WVS7_CURRENT_PROJECTION_CACHE_IDENTITY = "f400c804fea9b526f25eac823138ecb30e10efaad3207c4578661f684adee665"


class CandidateCProductionBindingError(ValueError):
    """Fail-closed Candidate-C production-binding error."""


def _sha256(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value.lower() != value
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise CandidateCProductionBindingError(f"{label} must be lowercase SHA-256")
    return value


def _accelerators(values: Iterable[str]) -> tuple[str, ...]:
    result = tuple(sorted(values))
    if len(result) != len(set(result)):
        raise CandidateCProductionBindingError("duplicate accelerator identity")
    unknown = set(result) - KNOWN_ACCELERATORS
    if unknown:
        raise CandidateCProductionBindingError(
            f"unaccepted Candidate-C accelerator identity: {sorted(unknown)!r}"
        )
    return result


@dataclass(frozen=True)
class CandidateCSourceBindingSpec:
    """Exact source/projection admission for one current Candidate-C cell.

    permitted_accelerators describes policy-level physical artifacts that may
    exist for this source. applicable_accelerators is narrower: artifacts whose
    frozen determinant scope completely covers this exact projection/workload.
    This source-backed fallback binder intentionally refuses to pretend that a
    partially covering accelerator is applicable.
    """

    source_name: str
    source_sha256: str
    projection_cache_identity: str
    permitted_accelerators: tuple[str, ...]
    applicable_accelerators: tuple[str, ...]
    realization_strategy: str
    scope_reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.source_name, str) or not self.source_name:
            raise CandidateCProductionBindingError("source_name must be nonempty")
        _sha256(self.source_sha256, "source_sha256")
        _sha256(self.projection_cache_identity, "projection_cache_identity")
        permitted = _accelerators(self.permitted_accelerators)
        applicable = _accelerators(self.applicable_accelerators)
        if not set(applicable) <= set(permitted):
            raise CandidateCProductionBindingError(
                "applicable accelerators must be a subset of explicitly permitted accelerators"
            )
        if not isinstance(self.realization_strategy, str) or not self.realization_strategy:
            raise CandidateCProductionBindingError("realization_strategy must be explicit")
        if not isinstance(self.scope_reason, str) or not self.scope_reason:
            raise CandidateCProductionBindingError("scope_reason must be explicit")
        object.__setattr__(self, "permitted_accelerators", permitted)
        object.__setattr__(self, "applicable_accelerators", applicable)


LITS_I_CURRENT_SPEC = CandidateCSourceBindingSpec(
    source_name="LITS_I",
    source_sha256=LITS_I_SOURCE_SHA256,
    projection_cache_identity=LITS_I_CURRENT_PROJECTION_CACHE_IDENTITY,
    permitted_accelerators=(CACC1_ID, CACC2_ID),
    applicable_accelerators=(),
    realization_strategy="EXACT_SOURCE_BACKED_FALLBACK_FOR_CURRENT_F02",
    scope_reason=(
        "Frozen CACC1/CACC2 do not close the exact current F02 projection; "
        "q310/q311 and any other uncovered exact source material remain mandatory."
    ),
)

WVS7_CURRENT_SPEC = CandidateCSourceBindingSpec(
    source_name="WVS7",
    source_sha256=WVS7_SOURCE_SHA256,
    projection_cache_identity=WVS7_CURRENT_PROJECTION_CACHE_IDENTITY,
    permitted_accelerators=(),
    applicable_accelerators=(),
    realization_strategy="EXACT_SOURCE_BACKED_ZERO_ACCELERATOR",
    scope_reason=(
        "The accepted Candidate-C accelerator implementation is LiTS-specific; "
        "no WVS-specific accelerator is authorized or required."
    ),
)

CURRENT_SOURCE_SPECS: Mapping[str, CandidateCSourceBindingSpec] = {
    "LITS_I": LITS_I_CURRENT_SPEC,
    "WVS7": WVS7_CURRENT_SPEC,
}


@dataclass(frozen=True)
class CandidateCProductionBinding:
    """Identity-bearing Candidate-C physical binding over the common C11 core."""

    repository: C11Repository
    release: Any
    projection: GovernedC11Projection
    spec: CandidateCSourceBindingSpec
    observed_accelerators: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.repository, C11Repository):
            raise CandidateCProductionBindingError("Candidate C must produce a C11Repository")
        if not isinstance(self.projection, GovernedC11Projection):
            raise CandidateCProductionBindingError("Candidate C requires exact governed projection")
        release_ref = getattr(self.release, "release_ref", None)
        if release_ref is None:
            raise CandidateCProductionBindingError("Candidate C release lacks exact release_ref")
        try:
            self.repository.resolve_release_exact(release_ref)
        except KeyError as exc:
            raise CandidateCProductionBindingError(
                "Candidate C release absent from returned repository"
            ) from exc
        object.__setattr__(self, "observed_accelerators", _accelerators(self.observed_accelerators))

    @property
    def candidate_identity(self) -> str:
        return CANDIDATE_ID

    @property
    def c11_semantic_result_identity(self) -> str:
        replay_manifest = getattr(self.release, "replay_manifest", None)
        replay_ref = getattr(replay_manifest, "ref", None)
        if replay_ref is None:
            raise CandidateCProductionBindingError("validated C11 replay identity missing")
        material = {
            "release_ref": self.release.release_ref.as_dict(),
            "replay_ref": replay_ref.as_dict(),
            "public_object_refs": [
                obj.ref.as_dict() for obj in getattr(self.release, "public_objects", ())
            ],
            "internal_record_refs": [
                obj.ref.as_dict() for obj in getattr(self.release, "internal_records", ())
            ],
        }
        return semantic_hash(material)

    def receipt(self) -> Mapping[str, Any]:
        replay_manifest = getattr(self.release, "replay_manifest", None)
        replay_ref = getattr(replay_manifest, "ref", None)
        if replay_ref is None:
            raise CandidateCProductionBindingError("validated C11 replay identity missing")
        observed = self.observed_accelerators
        material = {
            "schema": CONTRACT_ID,
            "candidate_identity": CANDIDATE_ID,
            "candidate_policy": CANDIDATE_POLICY,
            "candidate_owner": {
                "commit": CANDIDATE_C_OWNER_COMMIT,
                "path": CANDIDATE_C_OWNER_PATH,
                "blob": CANDIDATE_C_OWNER_BLOB,
                "candidate_hash": CANDIDATE_C_HASH,
            },
            "source_name": self.spec.source_name,
            "source_sha256": self.spec.source_sha256,
            "projection_cache_identity": self.spec.projection_cache_identity,
            "projection_identity_ref": self.projection.projection_identity_ref.as_dict(),
            "semantic_owner_contract": SOURCE_BACKED_C11_CONTRACT_ID,
            "semantic_release_ref": self.release.release_ref.as_dict(),
            "semantic_replay_ref": replay_ref.as_dict(),
            "c11_semantic_result_identity": self.c11_semantic_result_identity,
            "permitted_accelerators": list(self.spec.permitted_accelerators),
            "applicable_accelerators": list(self.spec.applicable_accelerators),
            "observed_accelerators": list(observed),
            "applied_accelerators": [],
            "accelerator_authoritative": False,
            "realization_strategy": self.spec.realization_strategy,
            "scope_reason": self.spec.scope_reason,
            "semantic_owner_moved": False,
            "candidate_b_identity_substituted": False,
            "source_semantics_inferred_from_physical_data": False,
        }
        return {**material, "binding_identity": semantic_hash(canonicalize(material))}


def _validate_exact_cell(
    *,
    spec: CandidateCSourceBindingSpec,
    source: Any,
    projection: GovernedC11Projection,
    observed_accelerators: tuple[str, ...],
) -> None:
    source_sha = getattr(source, "source_sha256", None)
    if source_sha != spec.source_sha256:
        raise CandidateCProductionBindingError(
            f"{spec.source_name} exact source identity mismatch"
        )
    if not isinstance(projection, GovernedC11Projection):
        raise CandidateCProductionBindingError("GovernedC11Projection required")
    if projection.expected_source_sha256 != spec.source_sha256:
        raise CandidateCProductionBindingError(
            f"{spec.source_name} projection/source authority mismatch"
        )
    if projection.cache_identity != spec.projection_cache_identity:
        raise CandidateCProductionBindingError(
            f"{spec.source_name} exact projection identity mismatch"
        )
    if not set(observed_accelerators) <= set(spec.permitted_accelerators):
        raise CandidateCProductionBindingError(
            f"{spec.source_name} accelerator inventory exceeds accepted source scope"
        )
    if spec.applicable_accelerators:
        raise CandidateCProductionBindingError(
            "source-backed fallback may not claim an accelerator whose exact "
            "determinant scope fully covers the workload; use the frozen "
            "Candidate-C accelerator owner for that separately qualified scope"
        )


def bind_candidate_c_repository(
    *,
    spec: CandidateCSourceBindingSpec,
    source: Any,
    projection: GovernedC11Projection,
    accelerator_inventory: Iterable[str] = (),
    common_semantic_result: tuple[C11Repository, Any] | None = None,
) -> CandidateCProductionBinding:
    """Bind Candidate C through exact source-backed reconstruction.

    This is deliberately not Candidate B substitution.  Candidate C's frozen
    policy identity is bound in the returned receipt, while empirical semantics
    stay with the common source-backed C11 facade.  Physical accelerator
    presence is nonauthoritative; for the current LiTS-I and WVS7 workloads no
    accelerator has complete exact projection coverage, so none is applied.
    """

    if not isinstance(spec, CandidateCSourceBindingSpec):
        raise CandidateCProductionBindingError("exact CandidateCSourceBindingSpec required")
    observed = _accelerators(accelerator_inventory)
    _validate_exact_cell(
        spec=spec,
        source=source,
        projection=projection,
        observed_accelerators=observed,
    )
    if common_semantic_result is None:
        repository, release = build_source_backed_c11_repository(
            source,
            projection,
            cache=None,
        )
    else:
        if (
            not isinstance(common_semantic_result, tuple)
            or len(common_semantic_result) != 2
            or not isinstance(common_semantic_result[0], C11Repository)
        ):
            raise CandidateCProductionBindingError("common semantic result must be an exact C11 repository/release pair")
        repository, release = common_semantic_result
        release_ref = getattr(release, "release_ref", None)
        source_ref = getattr(release, "source_artifact_ref", None)
        if (
            release_ref is None
            or source_ref is None
            or getattr(source_ref, "content_hash", None) != spec.source_sha256
        ):
            raise CandidateCProductionBindingError("common semantic result source identity mismatch")
        try:
            exact_release = repository.resolve_release_exact(release_ref)
        except KeyError as exc:
            raise CandidateCProductionBindingError("common semantic release absent from exact repository") from exc
        if exact_release is not release:
            raise CandidateCProductionBindingError("common semantic result release object is not exact repository member")
    return CandidateCProductionBinding(
        repository=repository,
        release=release,
        projection=projection,
        spec=spec,
        observed_accelerators=observed,
    )


def bind_current_candidate_c_repository(
    *,
    source_name: str,
    source: Any,
    projection: GovernedC11Projection,
    accelerator_inventory: Iterable[str] = (),
    common_semantic_result: tuple[C11Repository, Any] | None = None,
) -> CandidateCProductionBinding:
    try:
        spec = CURRENT_SOURCE_SPECS[source_name]
    except KeyError as exc:
        raise CandidateCProductionBindingError(
            f"unadmitted Candidate-C source: {source_name!r}"
        ) from exc
    return bind_candidate_c_repository(
        spec=spec,
        source=source,
        projection=projection,
        accelerator_inventory=accelerator_inventory,
        common_semantic_result=common_semantic_result,
    )


def build_lits_candidate_c_repository(
    *,
    source: Any,
    projection: GovernedC11Projection,
    accelerator_inventory: Iterable[str] = (),
    common_semantic_result: tuple[C11Repository, Any] | None = None,
):
    """Repository-builder-compatible LiTS-I Candidate-C production entrypoint."""
    binding = bind_current_candidate_c_repository(
        source_name="LITS_I",
        source=source,
        projection=projection,
        accelerator_inventory=accelerator_inventory,
        common_semantic_result=common_semantic_result,
    )
    return binding.repository, binding.release, binding.receipt()


def build_wvs7_candidate_c_repository(
    *,
    source: Any,
    projection: GovernedC11Projection,
):
    """Repository-builder-compatible WVS7 zero-accelerator Candidate-C entrypoint."""
    binding = bind_current_candidate_c_repository(
        source_name="WVS7",
        source=source,
        projection=projection,
        accelerator_inventory=(),
    )
    return binding.repository, binding.release, binding.receipt()


def candidate_c_builder_identity(source_name: str) -> Mapping[str, Any]:
    """Exact candidate-owner identity for the common repository-binding seam."""
    try:
        spec = CURRENT_SOURCE_SPECS[source_name]
    except KeyError as exc:
        raise CandidateCProductionBindingError(
            f"unadmitted Candidate-C source: {source_name!r}"
        ) from exc
    return {
        "candidate": CANDIDATE_ID,
        "candidate_policy": CANDIDATE_POLICY,
        "candidate_hash": CANDIDATE_C_HASH,
        "owner_commit": CANDIDATE_C_OWNER_COMMIT,
        "owner_path": CANDIDATE_C_OWNER_PATH,
        "owner_blob": CANDIDATE_C_OWNER_BLOB,
        "source": source_name,
        "projection_cache_identity": spec.projection_cache_identity,
        "semantic_owner_contract": SOURCE_BACKED_C11_CONTRACT_ID,
        "candidate_b_identity_substituted": False,
    }


def candidate_c_repository_builder_for_source(source_name: str):
    """Return the exact current source-specific Candidate-C production entrypoint."""
    if source_name == "LITS_I":
        return build_lits_candidate_c_repository
    if source_name == "WVS7":
        return build_wvs7_candidate_c_repository
    raise CandidateCProductionBindingError(
        f"unadmitted Candidate-C source: {source_name!r}"
    )


__all__ = [
    "CONTRACT_ID",
    "CANDIDATE_ID",
    "CANDIDATE_POLICY",
    "CANDIDATE_C_OWNER_COMMIT",
    "CANDIDATE_C_OWNER_PATH",
    "CANDIDATE_C_OWNER_BLOB",
    "CANDIDATE_C_HASH",
    "CACC1_ID",
    "CACC2_ID",
    "LITS_I_CURRENT_SPEC",
    "WVS7_CURRENT_SPEC",
    "CURRENT_SOURCE_SPECS",
    "CandidateCProductionBindingError",
    "CandidateCSourceBindingSpec",
    "CandidateCProductionBinding",
    "bind_candidate_c_repository",
    "bind_current_candidate_c_repository",
    "build_lits_candidate_c_repository",
    "build_wvs7_candidate_c_repository",
    "candidate_c_builder_identity",
    "candidate_c_repository_builder_for_source",
]
