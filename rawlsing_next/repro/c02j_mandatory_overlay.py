"""PYAT HQ281 C02J — Test-only mandatory enforcement overlay (UNADOPTED).

This module applies mandatory verifier routing at RUNTIME for hostile testing.
It does NOT modify source files. It is isolated to the test process.

Enforcement: every operative B5/M2 entrypoint consults a registry of
OwnerHeldB5Verifier instances. A release unknown to every registered verifier
is refused BEFORE the accepted owner is invoked. Known releases are checked
against the verifier's frozen expectation (re-resolved from the held
repository, so post-authoring mutation is detected).

Wrapped (all mutating B5 methods, not just the constructor):
  LearnedProductLifecycleExecutor.stage_release / stage_protocol /
  register_product / publish_product / record_recertification /
  select_current / declare_no_current / from_checkpoint
Wrapped (M2 registration):
  register_producer_subject / constitute_release (repository identity check)
Read-only resolution (resolve_selection_exact, selection_key, lifecycle_state,
export_checkpoint) is intentionally unwrapped: it publishes nothing.

No credential, ticket, token, signature or hash is presented by any caller at
any wrapped method. There is no credential surface to forge.
"""
from __future__ import annotations

import contextlib
import functools
from dataclasses import dataclass
from typing import Any, Callable

from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next.pre553_b5_owner_held_verifier_candidate import (
    OwnerHeldB5Verifier,
    VerifierUnknownReleaseError,
    VerifierUnregisteredRepositoryError,
    VerifierCheckpointError,
    OwnerHeldVerifierError,
)


@dataclass
class _Originals:
    B5_stage_release: Any = None
    B5_stage_protocol: Any = None
    B5_register_product: Any = None
    B5_publish_product: Any = None
    B5_record_recertification: Any = None
    B5_select_current: Any = None
    B5_declare_no_current: Any = None
    B5_from_checkpoint: Any = None
    M2_register_producer_subject: Any = None
    M2_constitute_release: Any = None


_ORIGINALS = _Originals()
_PATCH_ACTIVE = False

# release_ref.key -> OwnerHeldB5Verifier
_RELEASE_REGISTRY: dict[str, OwnerHeldB5Verifier] = {}
# id(M2Repository) -> OwnerHeldB5Verifier
_REPO_REGISTRY: dict[int, OwnerHeldB5Verifier] = {}


def register_verifier(verifier: OwnerHeldB5Verifier) -> None:
    """Register a verifier's releases and repository with the overlay."""
    if not isinstance(verifier, OwnerHeldB5Verifier):
        raise TypeError("register_verifier requires an OwnerHeldB5Verifier")
    _REPO_REGISTRY[id(verifier.held_repository())] = verifier
    for slot in verifier.slots():
        material = verifier._custody[slot]
        _RELEASE_REGISTRY[material.release_ref.key] = verifier


def clear_registry() -> None:
    _RELEASE_REGISTRY.clear()
    _REPO_REGISTRY.clear()


def _verifier_for_release(release_ref: Any) -> OwnerHeldB5Verifier:
    ref = exact_ref(release_ref, "release_ref")
    verifier = _RELEASE_REGISTRY.get(ref.key)
    if verifier is None:
        raise VerifierUnknownReleaseError(
            "release %s is not registered with any verifier; "
            "direct unmediated publication is refused" % ref.key
        )
    return verifier


def _verifier_for_repository(repository: Any) -> OwnerHeldB5Verifier:
    verifier = _REPO_REGISTRY.get(id(repository))
    if verifier is None:
        raise VerifierUnregisteredRepositoryError(
            "M2 repository is not held by any registered verifier; "
            "caller-minted registration is refused"
        )
    return verifier


def _subject_field_map(subject: Any) -> dict[str, Any]:
    """Observed identity built from the PRESENTED subject's own fields."""
    from rawlsing_next.pre553_empirical_objects import semantic_hash as _sh

    def _k(r: Any) -> str:
        if r is None:
            return ""
        if isinstance(r, str):
            return r
        for attr in ("object_id", "authority_id"):
            v = getattr(r, attr, None)
            if isinstance(v, str) and v:
                return v
        return ""

    def _sk(refs: Any) -> tuple[str, ...]:
        return tuple(sorted({_k(r) for r in refs if _k(r)}))

    return {
        "release_key": _k(subject.release_ref),
        "producer_contract_key": _k(subject.producer_contract_ref),
        "semantic_projection_hash": subject.semantic_projection_hash,
        "product_key": _k(subject.product_ref),
        "product_family_key": _k(subject.product_family_ref),
        "producer_owner_key": _k(subject.producer_owner_ref),
        "selection_scope_key": _k(subject.selection_scope_ref),
        "authority_snapshot_keys": _sk(subject.authority_snapshot_refs),
        "determinant_keys": _sk(subject.determinant_refs),
        "determinant_set_hash": subject.determinant_set_hash,
        "replay_root_key": _k(subject.replay_root_ref),
        "receipt_keys": _sk(subject.build_or_release_receipt_refs),
        "permission_ceiling_key": _k(subject.producer_permission_ceiling_ref),
    }


def _check_subject(verifier: OwnerHeldB5Verifier, subject: Any, release_ref: Any) -> None:
    verifier.verify_subject_for_release(subject, exact_ref(release_ref, "release_ref"))
    # Additionally: the PRESENTED subject's own fields must equal the frozen
    # expectation. Held-derived maps alone would let a forged subject through
    # and then execute it. The forgery must fail here, before the B5 call.
    slot = verifier.verify_release_registered(exact_ref(release_ref, "release_ref"))
    expected = verifier._expected.get(slot)
    observed = _subject_field_map(subject)
    mismatches = tuple(sorted(
        k for k in observed if observed[k] != expected.get(k)
    ))
    if mismatches:
        from rawlsing_next.pre553_b5_owner_held_verifier_candidate import (
            VerifierAuthenticationError,
        )
        raise VerifierAuthenticationError(
            "presented subject fields do not match the frozen owner-held "
            "expectation for slot %r; mismatched fields: %s"
            % (slot, ", ".join(mismatches)),
            mismatched_fields=mismatches,
            missing_keys=(),
        )


def _patch_b5() -> None:
    _ORIGINALS.B5_stage_release = B5.LearnedProductLifecycleExecutor.stage_release
    _ORIGINALS.B5_stage_protocol = B5.LearnedProductLifecycleExecutor.stage_protocol
    _ORIGINALS.B5_register_product = B5.LearnedProductLifecycleExecutor.register_product
    _ORIGINALS.B5_publish_product = B5.LearnedProductLifecycleExecutor.publish_product
    _ORIGINALS.B5_record_recertification = B5.LearnedProductLifecycleExecutor.record_recertification
    _ORIGINALS.B5_select_current = B5.LearnedProductLifecycleExecutor.select_current
    _ORIGINALS.B5_declare_no_current = B5.LearnedProductLifecycleExecutor.declare_no_current
    _ORIGINALS.B5_from_checkpoint = B5.LearnedProductLifecycleExecutor.from_checkpoint.__func__

    def patched_stage_release(self, subject):
        verifier = _verifier_for_release(subject.release_ref)
        _check_subject(verifier, subject, subject.release_ref)
        return _ORIGINALS.B5_stage_release(self, subject)

    def patched_stage_protocol(self, value, **overrides):
        subject = B5.LearnedProductLifecycleSubject.from_protocol(value, **overrides)
        verifier = _verifier_for_release(subject.release_ref)
        _check_subject(verifier, subject, subject.release_ref)
        return _ORIGINALS.B5_stage_release(self, subject)

    def patched_register_product(self, release_ref, **kwargs):
        verifier = _verifier_for_release(release_ref)
        subject = self._repository_subjects.get(exact_ref(release_ref, "release_ref").key)
        if subject is not None:
            _check_subject(verifier, subject, release_ref)
        return _ORIGINALS.B5_register_product(self, release_ref, **kwargs)

    def patched_publish_product(self, release_ref, **kwargs):
        verifier = _verifier_for_release(release_ref)
        subject = self._repository_subjects.get(exact_ref(release_ref, "release_ref").key)
        if subject is not None:
            _check_subject(verifier, subject, release_ref)
        return _ORIGINALS.B5_publish_product(self, release_ref, **kwargs)

    def patched_record_recertification(self, release_ref, **kwargs):
        _verifier_for_release(release_ref)
        return _ORIGINALS.B5_record_recertification(self, release_ref, **kwargs)

    def patched_select_current(self, selection_key_ref, release_ref, **kwargs):
        verifier = _verifier_for_release(release_ref)
        subject = self._repository_subjects.get(exact_ref(release_ref, "release_ref").key)
        if subject is not None:
            _check_subject(verifier, subject, release_ref)
        return _ORIGINALS.B5_select_current(
            self, selection_key_ref, release_ref, **kwargs
        )

    def patched_declare_no_current(self, selection_key_ref, **kwargs):
        subject_release_ref = kwargs.get("subject_release_ref")
        if subject_release_ref is not None:
            _verifier_for_release(subject_release_ref)
        return _ORIGINALS.B5_declare_no_current(self, selection_key_ref, **kwargs)

    @classmethod
    def patched_from_checkpoint(cls, checkpoint, **kwargs):
        rehydrated = _ORIGINALS.B5_from_checkpoint(cls, checkpoint)
        # Every rehydrated subject must resolve through a registered verifier.
        for key, subject in rehydrated._repository_subjects.items():
            verifier = _RELEASE_REGISTRY.get(key)
            if verifier is None:
                raise VerifierCheckpointError(
                    "rehydrated subject release %s is not registered with any "
                    "verifier; checkpoint rehydration is refused" % key
                )
            verifier.verify_checkpoint_subject(subject)
        return rehydrated

    B5.LearnedProductLifecycleExecutor.stage_release = patched_stage_release
    B5.LearnedProductLifecycleExecutor.stage_protocol = patched_stage_protocol
    B5.LearnedProductLifecycleExecutor.register_product = patched_register_product
    B5.LearnedProductLifecycleExecutor.publish_product = patched_publish_product
    B5.LearnedProductLifecycleExecutor.record_recertification = patched_record_recertification
    B5.LearnedProductLifecycleExecutor.select_current = patched_select_current
    B5.LearnedProductLifecycleExecutor.declare_no_current = patched_declare_no_current
    B5.LearnedProductLifecycleExecutor.from_checkpoint = patched_from_checkpoint


def _patch_m2() -> None:
    _ORIGINALS.M2_register_producer_subject = M2.register_producer_subject
    _ORIGINALS.M2_constitute_release = M2.constitute_release

    def patched_register_producer_subject(repository, **kwargs):
        _verifier_for_repository(repository)
        return _ORIGINALS.M2_register_producer_subject(repository, **kwargs)

    def patched_constitute_release(repository, **kwargs):
        _verifier_for_repository(repository)
        return _ORIGINALS.M2_constitute_release(repository, **kwargs)

    M2.register_producer_subject = patched_register_producer_subject
    M2.constitute_release = patched_constitute_release


def apply_mandatory_overlay() -> None:
    """Apply all mandatory routing patches at runtime."""
    global _PATCH_ACTIVE, _ORIGINALS
    if _PATCH_ACTIVE:
        return
    _ORIGINALS = _Originals()
    _patch_b5()
    _patch_m2()
    _PATCH_ACTIVE = True


def remove_mandatory_overlay() -> None:
    """Remove all mandatory routing patches."""
    global _PATCH_ACTIVE, _ORIGINALS
    if not _PATCH_ACTIVE:
        return
    if _ORIGINALS.B5_stage_release:
        B5.LearnedProductLifecycleExecutor.stage_release = _ORIGINALS.B5_stage_release
    if _ORIGINALS.B5_stage_protocol:
        B5.LearnedProductLifecycleExecutor.stage_protocol = _ORIGINALS.B5_stage_protocol
    if _ORIGINALS.B5_register_product:
        B5.LearnedProductLifecycleExecutor.register_product = _ORIGINALS.B5_register_product
    if _ORIGINALS.B5_publish_product:
        B5.LearnedProductLifecycleExecutor.publish_product = _ORIGINALS.B5_publish_product
    if _ORIGINALS.B5_record_recertification:
        B5.LearnedProductLifecycleExecutor.record_recertification = (
            _ORIGINALS.B5_record_recertification
        )
    if _ORIGINALS.B5_select_current:
        B5.LearnedProductLifecycleExecutor.select_current = _ORIGINALS.B5_select_current
    if _ORIGINALS.B5_declare_no_current:
        B5.LearnedProductLifecycleExecutor.declare_no_current = _ORIGINALS.B5_declare_no_current
    if _ORIGINALS.B5_from_checkpoint:
        B5.LearnedProductLifecycleExecutor.from_checkpoint = classmethod(
            _ORIGINALS.B5_from_checkpoint
        )
    if _ORIGINALS.M2_register_producer_subject:
        M2.register_producer_subject = _ORIGINALS.M2_register_producer_subject
    if _ORIGINALS.M2_constitute_release:
        M2.constitute_release = _ORIGINALS.M2_constitute_release
    clear_registry()
    _ORIGINALS = _Originals()
    _PATCH_ACTIVE = False


@contextlib.contextmanager
def mandatory_overlay_active():
    """Context manager for running tests under mandatory enforcement."""
    apply_mandatory_overlay()
    try:
        yield
    finally:
        remove_mandatory_overlay()


__all__ = [
    "register_verifier",
    "clear_registry",
    "apply_mandatory_overlay",
    "remove_mandatory_overlay",
    "mandatory_overlay_active",
]
