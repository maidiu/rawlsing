"""PYAT HQ282 N04 — B5 checkpoint interface correction CANDIDATE.

Development-only, source-free.  This module fixes a demonstrable false
refusal in the C02J owner-held verifier's checkpoint restoration path and
inventories B5/M2 state-changing methods for coverage analysis.

The concrete defect
-------------------
The C02J ``verify_checkpoint_subject`` calls
``self._m2.subject_exact(subject.release_ref)``.  The M2 ``subject_exact``
method expects a ``release_subject_ref`` (the producer subject), not a
``release_ref`` (the release identity).  This mismatch causes valid
checkpoint restores to be falsely rejected with
``RELEASE_SUBJECT_NOT_FOUND: exact producer subject is not registered``.

The correction
--------------
Use ``resolve_subject_exact(repository, release_ref)`` which:
1. Resolves the release via ``release_exact``
2. Extracts ``release.release_subject_ref``
3. Calls ``subject_exact`` with the correct ref
4. Verifies producer-contract and subject-kind consistency

This is the smallest correction that restores valid checkpoint behavior
while preserving legitimate rejection of changed/shortened history/state.

What this module does NOT do
----------------------------
* No accepted lifecycle/M2 owner is edited
* No new credential infrastructure is introduced
* No external authority, permission, or publication is issued
* No G0b, B5 CURRENT, or production publication
"""

from __future__ import annotations

import inspect
from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleExecutor,
    LearnedProductLifecycleSubject,
)

N04_CONTRACT_ID = "PYAT_HQ282_N04_B5_CHECKPOINT_INTERFACE_CORRECTION@1.0.0"


class N04CheckpointCorrectionError(ValueError):
    """The checkpoint correction cannot lawfully complete the requested operation."""


def corrected_verify_checkpoint_subject(
    repository: M2.M2Repository,
    subject: LearnedProductLifecycleSubject,
) -> Any:
    """Correctly resolve a checkpoint subject through the M2 repository.

    Uses ``resolve_subject_exact`` (which resolves the release first, then
    looks up the subject via ``release.release_subject_ref``) instead of
    the defective ``subject_exact(subject.release_ref)`` call.

    Returns the resolved ProducerSubject.
    """
    return M2.resolve_subject_exact(repository, subject.release_ref)


def demonstrate_checkpoint_defect() -> dict[str, Any]:
    """Reproduce the C02J checkpoint defect and show the correction.

    Returns a dict with:
    - ``defect_reproduced``: True if the original call pattern fails
    - ``correction_works``: True if the corrected call pattern succeeds
    - ``original_error``: the error from the defective call
    - ``corrected_result``: the result from the corrected call
    """
    from rawlsing_next.repro.c02j_owner_court import (
        build_m2,
        b5_subject_from_m2,
    )
    from rawlsing_next.pre553_learned_product_release import M2Repository

    repo = M2Repository()
    release, m2_subject = build_m2(repo, tag="n04-defect")
    subject = b5_subject_from_m2(repo, release, m2_subject)

    result = {
        "defect_reproduced": False,
        "correction_works": False,
        "original_error": None,
        "corrected_result": None,
    }

    try:
        repo.subject_exact(subject.release_ref)
    except Exception as exc:
        result["defect_reproduced"] = True
        result["original_error"] = f"{type(exc).__name__}: {exc}"

    try:
        resolved = corrected_verify_checkpoint_subject(repo, subject)
        result["correction_works"] = True
        result["corrected_result"] = {
            "producer_contract_ref": resolved.producer_contract_ref.as_dict(),
            "subject_kind": resolved.subject_kind,
        }
    except Exception as exc:
        result["corrected_error"] = f"{type(exc).__name__}: {exc}"

    return result


def inventory_b5_state_changing_methods() -> Mapping[str, Any]:
    """Inventory B5 public state-changing methods and their overlay coverage.

    Returns a frozen mapping grouping methods by whether they are:
    - ``WRAPPED``: covered by the C02J mandatory overlay
    - ``UNWRAPPED``: not covered by the overlay
    - ``PARTIAL``: partially covered
    """
    b5_methods = {
        "WRAPPED": (
            "stage_release",
            "stage_protocol",
            "register_product",
            "publish_product",
            "record_recertification",
            "select_current",
            "declare_no_current",
            "from_checkpoint",
        ),
        "UNWRAPPED": (
            "supersede_current",
            "withdraw_product",
            "declare_invalidation",
            "record_rebuild_eligibility",
            "link_rebuild",
            "record_cache_materialized",
            "record_cache_dropped",
            "attest_gc_eligibility",
            "record_payload_gc",
        ),
        "PARTIAL": (
            "declare_no_current",  # only checked if subject_release_ref supplied
            "record_recertification",  # registry lookup only, no event/authority check
        ),
    }
    m2_methods = {
        "WRAPPED": (
            "register_producer_subject",
            "constitute_release",
        ),
        "UNWRAPPED": (
            "M2Repository.register_subject",
            "M2Repository.register_closure",
            "M2Repository.register_release",
            "M2Repository.register_representation",
            "M2Repository.register_binding",
            "constitute_closure",
            "register_representation",
            "publish_binding",
        ),
    }
    return MappingProxyType({
        "b5_methods": MappingProxyType(b5_methods),
        "m2_methods": MappingProxyType(m2_methods),
        "checkpoint_defect": "verify_checkpoint_subject uses subject_exact(subject.release_ref) instead of resolve_subject_exact(repository, subject.release_ref)",
        "identity_mismatch": "release_ref != release.release_subject_ref",
    })


def effects() -> Mapping[str, bool]:
    """Declare every right this module does NOT hold."""
    return MappingProxyType({
        "source_meaning_inference": False,
        "model_use_grant": False,
        "g0b_issuance": False,
        "b5_current_selection": False,
        "field_forge_effect": False,
        "temporal_current_effect": False,
        "actor_v3_effect": False,
        "real_current_claim": False,
        "production_publication": False,
        "external_authority_issuance": False,
    })


__all__ = [
    "N04_CONTRACT_ID",
    "N04CheckpointCorrectionError",
    "corrected_verify_checkpoint_subject",
    "demonstrate_checkpoint_defect",
    "inventory_b5_state_changing_methods",
    "effects",
]
