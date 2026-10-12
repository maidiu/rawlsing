"""PYAT HQ282 N04 — Corrected B5 mandatory overlay.

Development-only, source-free.  This module provides a corrected version
of the C02J mandatory overlay that fixes the checkpoint restoration defect.

The concrete correction
-----------------------
The C02J ``verify_checkpoint_subject`` calls
``self._m2.subject_exact(subject.release_ref)``.  The M2 ``subject_exact``
expects a ``release_subject_ref``, not a ``release_ref``.  This module
provides ``corrected_verify_checkpoint_subject`` which uses
``resolve_subject_exact`` to correctly resolve the release first, then
looks up the subject via ``release.release_subject_ref``.

The ``apply_corrected_overlay`` function patches the verifier's
``verify_checkpoint_subject`` method to use the corrected implementation.
"""

from __future__ import annotations

import contextlib
from typing import Any

from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next.pre553_b5_owner_held_verifier_candidate import (
    OwnerHeldB5Verifier,
    VerifierCheckpointError,
)
from rawlsing_next.repro.c02j_mandatory_overlay import (
    apply_mandatory_overlay,
    remove_mandatory_overlay,
    register_verifier,
    clear_registry,
)

N04_OVERLAY_CONTRACT = "PYAT_HQ282_N04_CORRECTED_B5_OVERLAY@1.0.0"

_ORIGINAL_VERIFY_CHECKPOINT_SUBJECT = None
_CORRECTED_ACTIVE = False


def corrected_verify_checkpoint_subject(
    self: OwnerHeldB5Verifier,
    subject: B5.LearnedProductLifecycleSubject,
) -> str:
    """Correctly resolve a checkpoint subject through the M2 repository.

    Uses ``resolve_subject_exact`` (which resolves the release first, then
    looks up the subject via ``release.release_subject_ref``) instead of
    the defective ``subject_exact(subject.release_ref)`` call.
    """
    try:
        stored = M2.resolve_subject_exact(self._m2, subject.release_ref)
    except Exception as exc:
        raise VerifierCheckpointError(
            "checkpoint subject release is absent from the held M2 repository: %s"
            % exc
        ) from exc
    void = stored
    del void
    slot = self.verify_release_registered(subject.release_ref)
    material = self._custody[slot]
    observed = self._observed_identity(material)
    self._revocation_check(material, observed)
    self._replay_gate(material)
    self._authenticate(subject, observed, slot)
    return slot


def apply_corrected_overlay() -> None:
    """Apply the C02J overlay plus the checkpoint correction."""
    global _ORIGINAL_VERIFY_CHECKPOINT_SUBJECT, _CORRECTED_ACTIVE
    if _CORRECTED_ACTIVE:
        return
    apply_mandatory_overlay()
    _ORIGINAL_VERIFY_CHECKPOINT_SUBJECT = (
        OwnerHeldB5Verifier.verify_checkpoint_subject
    )
    OwnerHeldB5Verifier.verify_checkpoint_subject = (
        corrected_verify_checkpoint_subject
    )
    _CORRECTED_ACTIVE = True


def remove_corrected_overlay() -> None:
    """Remove the checkpoint correction and the C02J overlay."""
    global _ORIGINAL_VERIFY_CHECKPOINT_SUBJECT, _CORRECTED_ACTIVE
    if not _CORRECTED_ACTIVE:
        return
    if _ORIGINAL_VERIFY_CHECKPOINT_SUBJECT:
        OwnerHeldB5Verifier.verify_checkpoint_subject = (
            _ORIGINAL_VERIFY_CHECKPOINT_SUBJECT
        )
    remove_mandatory_overlay()
    _ORIGINAL_VERIFY_CHECKPOINT_SUBJECT = None
    _CORRECTED_ACTIVE = False


@contextlib.contextmanager
def corrected_overlay_active():
    """Context manager for running tests under corrected overlay enforcement."""
    apply_corrected_overlay()
    try:
        yield
    finally:
        remove_corrected_overlay()


__all__ = [
    "N04_OVERLAY_CONTRACT",
    "corrected_verify_checkpoint_subject",
    "apply_corrected_overlay",
    "remove_corrected_overlay",
    "corrected_overlay_active",
    "register_verifier",
    "clear_registry",
]
