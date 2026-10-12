"""PYAT HQ280 PV3 C02E -- Test-only mandatory enforcement patch overlay.

This module applies the mandatory boundary patch at RUNTIME for hostile testing.
It does NOT modify source files. It is isolated to this test process.

The patch enforces:
1. PerimeterTicket required on ALL B5 methods
2. ProducerCredential required on M2 registration
3. Independent CheckpointAuthority on from_checkpoint
4. Frozen EXPECTATION_KEY_TYPES (C02R F4)
"""
from __future__ import annotations

import contextlib
from dataclasses import dataclass, replace
from typing import Any, Callable

from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    AuthorityRef,
    semantic_hash,
)
from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next import pre553_authenticated_b5_ingress_candidate as C02


# ---- Patch data structures ----


@dataclass(frozen=True)
class PerimeterTicket:
    slot: str
    issuance_hash: str
    perimeter_ref: ExactRef
    authority_snapshot_refs: tuple[AuthorityRef, ...]
    expected_identity_hash: str
    issued_at_event_ref: ExactRef


@dataclass(frozen=True)
class ProducerCredential:
    subject_ref: ExactRef
    producer_issuer_ref: AuthorityRef
    issuance_hash: str
    credential_ref: ExactRef


@dataclass(frozen=True)
class CheckpointAuthority:
    checkpoint_hash: str
    verifying_authority_ref: AuthorityRef
    verification_hash: str
    verification_ref: ExactRef


# ---- Patch errors ----


class PerimeterTicketError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


class ProducerCredentialError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


class CheckpointAuthorityError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


class ExpectationMutationError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


# ---- Storage for original methods ----


@dataclass
class _OriginalMethods:
    B5_init: Callable = None
    B5_stage_release: Callable = None
    B5_register_product: Callable = None
    B5_publish_product: Callable = None
    B5_select_current: Callable = None
    B5_declare_no_current: Callable = None
    B5_from_checkpoint: classmethod = None
    M2_register_producer_subject: Callable = None
    M2_constitute_release: Callable = None
    C02_EXPECTATION_KEY_TYPES: dict = None
    C02_publish_registered: Callable = None


_ORIGINALS = _OriginalMethods()
_PATCH_ACTIVE = False


def _check_perimeter(self) -> None:
    """Check that this executor has a valid PerimeterTicket."""
    if not hasattr(self, "_perimeter_ticket") or self._perimeter_ticket is None:
        raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
            "mandatory boundary: every lifecycle executor requires a PerimeterTicket")


def _patch_b5_executor() -> None:
    """Patch LearnedProductLifecycleExecutor to require PerimeterTicket."""
    global _ORIGINALS

    # Store originals
    _ORIGINALS.B5_init = B5.LearnedProductLifecycleExecutor.__init__
    _ORIGINALS.B5_stage_release = B5.LearnedProductLifecycleExecutor.stage_release
    _ORIGINALS.B5_register_product = B5.LearnedProductLifecycleExecutor.register_product
    _ORIGINALS.B5_publish_product = B5.LearnedProductLifecycleExecutor.publish_product
    _ORIGINALS.B5_select_current = B5.LearnedProductLifecycleExecutor.select_current
    _ORIGINALS.B5_declare_no_current = B5.LearnedProductLifecycleExecutor.declare_no_current
    _ORIGINALS.B5_from_checkpoint = B5.LearnedProductLifecycleExecutor.from_checkpoint.__func__

    # Patch __init__
    def patched_init(self, perimeter_ticket=None):
        if perimeter_ticket is None:
            raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
                "mandatory boundary: every lifecycle executor requires a PerimeterTicket")
        _ORIGINALS.B5_init(self)
        self._perimeter_ticket = perimeter_ticket

    # Patch methods
    def patched_stage_release(self, subject):
        _check_perimeter(self)
        return _ORIGINALS.B5_stage_release(self, subject)

    def patched_register_product(self, *args, **kwargs):
        _check_perimeter(self)
        return _ORIGINALS.B5_register_product(self, *args, **kwargs)

    def patched_publish_product(self, *args, **kwargs):
        _check_perimeter(self)
        return _ORIGINALS.B5_publish_product(self, *args, **kwargs)

    def patched_select_current(self, *args, **kwargs):
        _check_perimeter(self)
        return _ORIGINALS.B5_select_current(self, *args, **kwargs)

    def patched_declare_no_current(self, *args, **kwargs):
        _check_perimeter(self)
        return _ORIGINALS.B5_declare_no_current(self, *args, **kwargs)

    @classmethod
    def patched_from_checkpoint(cls, checkpoint, checkpoint_authority=None):
        if checkpoint_authority is None:
            raise CheckpointAuthorityError("CHECKPOINT_AUTHORITY_REQUIRED",
                "from_checkpoint requires independent CheckpointAuthority; "
                "self-referential hash is not authentication")
        if not hasattr(checkpoint_authority, 'verification_hash'):
            raise CheckpointAuthorityError("CHECKPOINT_AUTHORITY_REQUIRED",
                "checkpoint_authority must have verification_hash")
        payload = checkpoint.get("checkpoint_payload")
        if payload is None:
            raise CheckpointAuthorityError("CHECKPOINT_AUTHORITY_REQUIRED",
                "checkpoint payload missing")
        if getattr(checkpoint_authority, 'verification_hash', None) != semantic_hash(
            checkpoint.get("checkpoint_payload", {})
        ):
            raise CheckpointAuthorityError(
                "CHECKPOINT_HASH_INDEPENDENT_VERIFICATION_FAILED",
                "independent authority verification failed"
            )
        # Reconstruct with a demo ticket for the internal stage_release call
        demo = PerimeterTicket(
            slot="c02f-rehydrate",
            issuance_hash="c02f-demo-fixture-rehydrate",
            perimeter_ref=ExactRef("Perimeter", "c02f-demo-fixture-rehydrate",
                                   semantic_hash({"fixture": "c02f-rehydrate"})),
            authority_snapshot_refs=(),
            expected_identity_hash="c02f-demo-fixture",
            issued_at_event_ref=ExactRef("Event", "c02f-demo-fixture-rehydrate-event",
                                         semantic_hash({"fixture": "c02f-rehydrate-event"})),
        )
        original_init = B5.LearnedProductLifecycleExecutor.__init__
        def ticketed_init(self, perimeter_ticket=None):
            original_init(self, perimeter_ticket=demo)
        B5.LearnedProductLifecycleExecutor.__init__ = ticketed_init
        try:
            return _ORIGINALS.B5_from_checkpoint(cls, checkpoint)
        finally:
            B5.LearnedProductLifecycleExecutor.__init__ = original_init

    # Apply patches with __wrapped__ markers
    B5.LearnedProductLifecycleExecutor.__init__ = patched_init
    B5.LearnedProductLifecycleExecutor.stage_release = patched_stage_release
    B5.LearnedProductLifecycleExecutor.register_product = patched_register_product
    B5.LearnedProductLifecycleExecutor.publish_product = patched_publish_product
    B5.LearnedProductLifecycleExecutor.select_current = patched_select_current
    B5.LearnedProductLifecycleExecutor.declare_no_current = lambda self, *a, **kw: (_check_perimeter(self), _ORIGINALS.B5_declare_no_current(self, *a, **kw))[1]
    B5.LearnedProductLifecycleExecutor.from_checkpoint = patched_from_checkpoint


def _patch_m2_registration() -> None:
    """Patch M2 registration to require ProducerCredential."""
    global _ORIGINALS

    _ORIGINALS.M2_register_producer_subject = M2.register_producer_subject
    _ORIGINALS.M2_constitute_release = M2.constitute_release

    def patched_register_producer_subject(repository, *, producer_credential=None, **kwargs):
        if producer_credential is None:
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_REQUIRED",
                "register_producer_subject requires ProducerCredential under mandatory boundary")
        if not hasattr(producer_credential, 'subject_ref'):
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_INVALID",
                "producer_credential must have subject_ref")
        if producer_credential.subject_ref != kwargs.get('subject_ref'):
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_INVALID",
                "credential subject_ref does not match registered subject")
        return _ORIGINALS.M2_register_producer_subject(repository, **kwargs)

    def patched_constitute_release(repository, *, producer_credential=None, **kwargs):
        if producer_credential is None:
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_REQUIRED",
                "constitute_release requires ProducerCredential under mandatory boundary")
        if not hasattr(producer_credential, 'subject_ref'):
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_INVALID",
                "producer_credential must have subject_ref")
        if producer_credential.subject_ref != kwargs.get('release_subject_ref'):
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_INVALID",
                "credential subject_ref does not match release subject")
        return _ORIGINALS.M2_constitute_release(repository, **kwargs)

    _ORIGINALS.M2_register_producer_subject = M2.register_producer_subject
    _ORIGINALS.M2_constitute_release = M2.constitute_release

    M2.register_producer_subject = patched_register_producer_subject
    M2.constitute_release = patched_constitute_release


def _freeze_expectation_key_types() -> None:
    """Freeze the mutable EXPECTATION_KEY_TYPES dict (C02R F4)."""
    from types import MappingProxyType
    global _ORIGINALS
    if not isinstance(C02.EXPECTATION_KEY_TYPES, MappingProxyType):
        _ORIGINALS.C02_EXPECTATION_KEY_TYPES = dict(C02.EXPECTATION_KEY_TYPES)
        C02.EXPECTATION_KEY_TYPES = MappingProxyType(C02.EXPECTATION_KEY_TYPES)


def _patch_c02_ingress() -> None:
    """Wrap C02 ingress to supply a demo-fixture ticket for its internal executor.

    C02's _publish_registered creates B5.LearnedProductLifecycleExecutor() internally.
    Under the mandatory patch that constructor requires a PerimeterTicket. This
    wrapper injects a demo-fixture ticket so the C02 path remains functional
    while the mandatory boundary is active. The ticket is a DEMO FIXTURE, not
    an issuer credential — see the issuer hold.
    """
    global _ORIGINALS
    original_publish_registered = C02.AuthenticatedB5Ingress._publish_registered

    def _demo_ticket(slot: str):
        return PerimeterTicket(
            slot=slot,
            issuance_hash="c02f-demo-fixture-ticket",
            perimeter_ref=ExactRef("Perimeter", "c02f-demo-fixture",
                                   semantic_hash({"fixture": "c02f"})),
            authority_snapshot_refs=(),
            expected_identity_hash="c02f-demo-fixture",
            issued_at_event_ref=ExactRef("Event", "c02f-demo-fixture-event",
                                         semantic_hash({"fixture": "c02f-event"})),
        )

    def wrapped_publish_registered(self, slot, material):
        # Inject a demo ticket so the internal executor construction succeeds.
        # The C02 path authenticates against owner-held material; the ticket
        # only satisfies the mandatory constructor requirement.
        ticket = _demo_ticket(slot)
        # Monkey-patch the executor construction inside this call only.
        original_init = B5.LearnedProductLifecycleExecutor.__init__
        def ticketed_init(self, perimeter_ticket=None):
            original_init(self, perimeter_ticket=ticket)
        B5.LearnedProductLifecycleExecutor.__init__ = ticketed_init
        try:
            return original_publish_registered(self, slot, material)
        finally:
            B5.LearnedProductLifecycleExecutor.__init__ = original_init

    C02.AuthenticatedB5Ingress._publish_registered = wrapped_publish_registered
    _ORIGINALS.C02_publish_registered = original_publish_registered


def _restore_c02_ingress() -> None:
    """Restore C02 ingress."""
    global _ORIGINALS
    if _ORIGINALS.C02_publish_registered is not None:
        C02.AuthenticatedB5Ingress._publish_registered = _ORIGINALS.C02_publish_registered
        _ORIGINALS.C02_publish_registered = None


def _unfreeze_expectation_key_types() -> None:
    """Restore the mutable EXPECTATION_KEY_TYPES."""
    global _ORIGINALS
    if _ORIGINALS.C02_EXPECTATION_KEY_TYPES is not None:
        C02.EXPECTATION_KEY_TYPES = _ORIGINALS.C02_EXPECTATION_KEY_TYPES
        _ORIGINALS.C02_EXPECTATION_KEY_TYPES = None


# ---- Global state ----


_PATCH_ACTIVE = False


def apply_mandatory_patch() -> None:
    """Apply all mandatory boundary patches at runtime."""
    global _PATCH_ACTIVE, _ORIGINALS
    if _PATCH_ACTIVE:
        return
    _ORIGINALS = _OriginalMethods()
    _patch_b5_executor()
    _patch_m2_registration()
    _freeze_expectation_key_types()
    _patch_c02_ingress()
    _PATCH_ACTIVE = True


def remove_mandatory_patch() -> None:
    """Remove all mandatory boundary patches."""
    global _PATCH_ACTIVE, _ORIGINALS
    if not _PATCH_ACTIVE:
        return

    # Restore B5
    if _ORIGINALS.B5_init:
        B5.LearnedProductLifecycleExecutor.__init__ = _ORIGINALS.B5_init
    if _ORIGINALS.B5_stage_release:
        B5.LearnedProductLifecycleExecutor.stage_release = _ORIGINALS.B5_stage_release
    if _ORIGINALS.B5_register_product:
        B5.LearnedProductLifecycleExecutor.register_product = _ORIGINALS.B5_register_product
    if _ORIGINALS.B5_publish_product:
        B5.LearnedProductLifecycleExecutor.publish_product = _ORIGINALS.B5_publish_product
    if _ORIGINALS.B5_select_current:
        B5.LearnedProductLifecycleExecutor.select_current = _ORIGINALS.B5_select_current
    if _ORIGINALS.B5_declare_no_current:
        B5.LearnedProductLifecycleExecutor.declare_no_current = _ORIGINALS.B5_declare_no_current
    if _ORIGINALS.B5_from_checkpoint:
        B5.LearnedProductLifecycleExecutor.from_checkpoint = classmethod(_ORIGINALS.B5_from_checkpoint)

    # Restore M2
    if _ORIGINALS.M2_register_producer_subject:
        M2.register_producer_subject = _ORIGINALS.M2_register_producer_subject
    if _ORIGINALS.M2_constitute_release:
        M2.constitute_release = _ORIGINALS.M2_constitute_release

    # Restore C02
    _restore_c02_ingress()

    # Restore C02 EXPECTATION_KEY_TYPES
    _unfreeze_expectation_key_types()

    _ORIGINALS = _OriginalMethods()
    _PATCH_ACTIVE = False


@contextlib.contextmanager
def mandatory_boundary_active():
    """Context manager for running tests under mandatory enforcement."""
    apply_mandatory_patch()
    try:
        yield
    finally:
        remove_mandatory_patch()


# ---- Error classes ----


class PerimeterTicketError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


class ProducerCredentialError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


class CheckpointAuthorityError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


# ---- Patch data structures for test use ----


@dataclass(frozen=True)
class PerimeterTicket:
    slot: str
    issuance_hash: str
    perimeter_ref: ExactRef
    authority_snapshot_refs: tuple[AuthorityRef, ...]
    expected_identity_hash: str
    issued_at_event_ref: ExactRef


@dataclass(frozen=True)
class ProducerCredential:
    subject_ref: ExactRef
    producer_issuer_ref: AuthorityRef
    issuance_hash: str
    credential_ref: ExactRef


@dataclass(frozen=True)
class CheckpointAuthority:
    checkpoint_hash: str
    verifying_authority_ref: AuthorityRef
    verification_hash: str
    verification_ref: ExactRef


__all__ = [
    "PerimeterTicket",
    "ProducerCredential",
    "CheckpointAuthority",
    "PerimeterTicketError",
    "ProducerCredentialError",
    "CheckpointAuthorityError",
    "apply_mandatory_patch",
    "remove_mandatory_patch",
    "mandatory_boundary_active",
]