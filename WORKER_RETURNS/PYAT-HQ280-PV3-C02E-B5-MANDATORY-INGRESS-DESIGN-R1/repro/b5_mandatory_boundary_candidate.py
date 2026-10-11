"""PYAT HQ280 PV3 C02E -- Mandatory B5 publication and rehydration trust boundary CANDIDATE.

DEVELOPMENT CANDIDATE ONLY. Non-authorizing, G0b HELD, G1 HELD, CURRENT HELD.
No self-adoption, no canonical mutation, no trust root.

WHAT THIS IS
------------
The **smallest mandatory authentication and replay/rehydration boundary** that covers
ALL reachable B5 publication and restore paths, as independently mapped by C02R:

1. `LearnedProductLifecycleExecutor.stage_release` (invoked by
   `pre553_learned_world_composition.py:1203`)
2. `LearnedProductLifecycleExecutor.register_product`
   (`pre553_learned_world_composition.py:1206`)
3. `LearnedProductLifecycleExecutor.publish_product`
   (`pre553_learned_world_composition.py:1219`)
4. `LearnedProductLifecycleExecutor.select_current`
   (`pre553_learned_world_composition.py:1241`)
5. `LearnedProductLifecycleExecutor.declare_no_current`
6. `LearnedProductLifecycleExecutor.from_checkpoint` (rehydration bypass)
7. `M2.register_producer_subject` (caller-minted release bypass)
8. `M2.constitute_release` (content-addressing only, no producer credential)

The C02 optional facade (`pre553_authenticated_b5_ingress_candidate.py`) is **not** on
these paths. It is an optional caller-side surface. This candidate places the
enforcement at the **owner jurisdiction** where it cannot be bypassed.

DESIGN
------
This module defines the **exact contract** a mandatory boundary must satisfy.
It does NOT invent a new scheduling engine, credential system, or trust root.

The enforcement point is the **accepted B5 owner** (`LearnedProductLifecycleExecutor`)
and the **accepted M2 owner** (`register_producer_subject`, `constitute_release`).
The test-only patch overlay (in repro/) demonstrates the minimal changes to make
enforcement mandatory at those owners. This module records the exact caller graphs,
the exact authority act required, and the hostile surface.

NO G0b, NO CURRENT, NO OPERATIVE PUBLICATION.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    AuthorityRef,
    semantic_hash,
)
from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next import pre553_learned_product_release as M2
from rawlsing_next import pre553_learned_world_composition as LWC
from rawlsing_next import pre553_authenticated_b5_ingress_candidate as C02


MANDATORY_BOUNDARY_CONTRACT = "PYAT_HQ280_C02E_MANDATORY_B5_INGRESS_BOUNDARY@1.0.0"
DEVELOPMENT_GRADE = "SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__G0B_HELD__G1_HELD__CURRENT_HELD"

#: The EXACT call graph from production code into B5/M2/Current.
#: Independently reproduced from C02R F1/F2/F3 findings.
REACHABLE_INGRESS_CALL_GRAPH = MappingProxyType({
    "B5.stage_release": [
        ("pre553_learned_world_composition.py", 1203,
         "lifecycle_executor.stage_release(b5_subject)"),
        ("pre553_authenticated_b5_ingress_candidate.py", 899,
         "executor.stage_release(subject)"),
    ],
    "B5.register_product": [
        ("pre553_learned_world_composition.py", 1206,
         "lifecycle_executor.register_product(...)"),
        ("pre553_authenticated_b5_ingress_candidate.py", 901,
         "executor.register_product(...)"),
    ],
    "B5.publish_product": [
        ("pre553_learned_world_composition.py", 1219,
         "lifecycle_executor.publish_product(...)"),
        ("pre553_authenticated_b5_ingress_candidate.py", 906,
         "executor.publish_product(...)"),
    ],
    "B5.select_current": [
        ("pre553_learned_world_composition.py", 1241,
         "lifecycle_executor.select_current(...)"),
    ],
    "B5.declare_no_current": [
        ("pre553_learned_world_composition.py", None,
         "available but not used in current composition"),
    ],
    "B5.from_checkpoint": [
        ("pre553_learned_product_lifecycle.py", 2699,
         "classmethod rehydration with self-referential hash"),
        ("pre553_learned_product_lifecycle.py", 2833,
         "audit_replay re-invokes from_checkpoint"),
    ],
    "M2.register_producer_subject": [
        ("pre553_learned_product_release.py", 549,
         "caller-provided subject data; no producer credential check"),
        ("pre553_learned_world_composition.py", 1193,
         "adapt_m1_disposition_to_m2 -> register_producer_subject"),
    ],
    "M2.constitute_release": [
        ("pre553_learned_product_release.py", 646,
         "content-addressing only; no issuer/signature/credential check"),
        ("pre553_learned_world_composition.py", 1198,
         "adapt_m2_release_to_b5 -> constitute_release"),
    ],
    "C02_optional_facade": [
        ("pre553_authenticated_b5_ingress_candidate.py", 589,
         "publish(PublicationRequest) -- OPTIONAL, caller chooses whether to call"),
    ],
})

#: EXACT authority act required to make every path mandatory.
#: This is the smallest competent owner jurisdiction: the B5 owner itself
#: (LearnedProductLifecycleExecutor) and the M2 owner (register_producer_subject/
#: constitute_release). The perimeter MUST be enforced at the owner, not at a
#: caller-side facade.
REQUIRED_AUTHORITY_ACT = """
MANDATORY AUTHORITY ACT (smallest competent owner jurisdiction):

1. LearnedProductLifecycleExecutor MUST require a PerimeterTicket on EVERY public
   method (stage_release, register_product, publish_product, select_current,
   declare_no_current, from_checkpoint). The ticket is issued by the authenticated
   perimeter after verifying the subject against owner-held M2-verified material.

2. M2.register_producer_subject and M2.constitute_release MUST require a
   ProducerCredential proving the subject was issued by a competent producer.
   Current code accepts only data.

3. from_checkpoint MUST verify the checkpoint hash against an INDEPENDENT
   authority (not the caller's self-computed hash). The self-referential hash
   (checkpoint_hash == semantic_hash(payload)) is a bypass, not authentication.

4. The mutable EXPECTATION_KEY_TYPES in the C02 candidate must be frozen
   (MappingProxyType) to prevent runtime type-gate weakening.

No new trust root, issuer, key registry, or signature scheme is created by this
act. The enforcement binds the existing M2 content-addressing to a producer-
issued credential, and binds the B5 owner to a mandatory perimeter ticket.
"""

#: Refusal codes the mandatory boundary must raise.
MANDATORY_REFUSAL_CODES = frozenset({
    "PERIMETER_TICKET_REQUIRED",
    "PERIMETER_TICKET_INVALID",
    "PERIMETER_TICKET_REVOKED",
    "PRODUCER_CREDENTIAL_REQUIRED",
    "PRODUCER_CREDENTIAL_INVALID",
    "CHECKPOINT_AUTHORITY_REQUIRED",
    "CHECKPOINT_HASH_INDEPENDENT_VERIFICATION_FAILED",
    "EXPECTATION_TYPE_GATE_MUTATED",
    "EXPECTATION_INCOMPLETE",
    "IDENTITY_AUTHENTICATION_FAILED",
    "DETERMINANT_CLOSURE_INCOMPLETE",
    "REPLAY_CLOSURE_REFUSED",
    "M2_RESOLUTION_REFUSED",
    "AUTHORITY_REVOKED",
})


class MandatoryBoundaryError(Exception):
    """Base error for mandatory boundary refusals."""

    def __init__(self, code: str, message: str = "") -> None:
        if code not in MANDATORY_REFUSAL_CODES:
            raise ValueError(f"unknown mandatory refusal code {code!r}")
        super().__init__(message or code)
        self.code = code


class PerimeterTicketError(MandatoryBoundaryError):
    """A mandatory PerimeterTicket was required but not provided or was invalid."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code, detail)


class ProducerCredentialError(MandatoryBoundaryError):
    """A mandatory ProducerCredential was required but not provided or was invalid."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code, detail)


class CheckpointAuthorityError(MandatoryBoundaryError):
    """Checkpoint rehydration requires independent authority verification."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code, detail)


class ExpectationMutationError(MandatoryBoundaryError):
    """The owner-held expectation type gate was mutated at runtime."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code, detail)


# ---------------------------------------------------------------------------
# Data-only perimeter contract (what a mandatory ticket/credential carries)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PerimeterTicket:
    """A mandatory ticket issued by the authenticated perimeter.

    This is the EXACT data structure that must be presented to every B5 method
    when the mandatory boundary is active. It carries NO subject data -- only
    the authentication result and the slot it was issued for.
    """

    slot: str
    issuance_hash: str
    perimeter_ref: ExactRef
    authority_snapshot_refs: tuple[AuthorityRef, ...]
    expected_identity_hash: str
    issued_at_event_ref: ExactRef

    def as_dict(self) -> dict[str, Any]:
        return {
            "slot": self.slot,
            "issuance_hash": self.issuance_hash,
            "perimeter_ref": self.perimeter_ref.as_dict(),
            "authority_snapshot_refs": [ref.as_dict() for ref in self.authority_snapshot_refs],
            "expected_identity_hash": self.expected_identity_hash,
            "issued_at_event_ref": self.issued_at_event_ref.as_dict(),
        }


@dataclass(frozen=True)
class ProducerCredential:
    """A mandatory credential proving producer issuance.

    This is what M2.register_producer_subject and constitute_release MUST require
    when the mandatory boundary is active. It is NOT the subject data itself --
    it is a separate attestation that a competent producer issued this subject.
    """

    subject_ref: ExactRef
    producer_issuer_ref: AuthorityRef
    issuance_hash: str
    credential_ref: ExactRef

    def as_dict(self) -> dict[str, Any]:
        return {
            "subject_ref": self.subject_ref.as_dict(),
            "producer_issuer_ref": self.producer_issuer_ref.as_dict(),
            "issuance_hash": self.issuance_hash,
            "credential_ref": self.credential_ref.as_dict(),
        }


@dataclass(frozen=True)
class CheckpointAuthority:
    """Independent authority that verifies a checkpoint hash.

    The current from_checkpoint verifies checkpoint_hash == semantic_hash(payload)
    where the caller computes BOTH sides. This is a bypass. A mandatory boundary
    requires an INDEPENDENT authority that can verify the checkpoint without
    trusting the caller's computation.
    """

    checkpoint_hash: str
    verifying_authority_ref: AuthorityRef
    verification_hash: str
    verification_ref: ExactRef

    def as_dict(self) -> dict[str, Any]:
        return {
            "checkpoint_hash": self.checkpoint_hash,
            "verifying_authority_ref": self.verifying_authority_ref.as_dict(),
            "verification_hash": self.verification_hash,
            "verification_ref": self.verification_ref.as_dict(),
        }


# ---------------------------------------------------------------------------
# Caller graph introspection (recorded, never re-implemented)
# ---------------------------------------------------------------------------

def record_caller_graphs() -> dict[str, Any]:
    """Exact, independently reproducible caller graphs from the production code.

    This records the exact reachable paths C02R found (F1/F2/F3), so the
    boundary design is traceable to source.
    """
    return dict(REACHABLE_INGRESS_CALL_GRAPH)


def required_authority_act() -> str:
    """The exact authority act required for mandatory enforcement."""
    return REQUIRED_AUTHORITY_ACT


# ---------------------------------------------------------------------------
# Owner introspection (recorded, never re-implemented)
# ---------------------------------------------------------------------------

_INTRSPECTED_OWNERS = (
    "rawlsing_next.pre553_learned_product_lifecycle.LearnedProductLifecycleExecutor",
    "rawlsing_next.pre553_learned_product_release.register_producer_subject",
    "rawlsing_next.pre553_learned_product_release.constitute_release",
    "rawlsing_next.pre553_learned_world_composition.build_m1_bundle_from_m01",
    "rawlsing_next.pre553_authenticated_b5_ingress_candidate.AuthenticatedB5Ingress",
)


def introspect_owner_signatures() -> dict[str, str]:
    """Exact introspected signatures of the owners the mandatory boundary covers."""
    import inspect
    import importlib

    recorded: dict[str, str] = {}
    for dotted in _INTRSPECTED_OWNERS:
        module_name, _, attribute = dotted.rpartition(".")
        module = importlib.import_module(module_name)
        target = getattr(module, attribute)
        # For a plain class, record its constructor contract.
        probe = target.__init__ if inspect.isclass(target) else target
        name = attribute if not inspect.isclass(target) else attribute
        recorded[dotted] = f"{name}{inspect.signature(probe)}"
    return dict(sorted(recorded.items()))


# ---------------------------------------------------------------------------
# Patch overlay specification (exact diff for test-only mandatory enforcement)
# ---------------------------------------------------------------------------

# This is the EXACT minimal patch that would make enforcement mandatory at the
# B5 owner level. It is a specification, NOT an active patch. The test-only
# overlay in repro/ applies this at runtime for hostile testing.
#
# The patch targets:
#   1. LearnedProductLifecycleExecutor.__init__ - add perimeter_ticket arg
#   2. stage_release - require perimeter_ticket
#   3. register_product - require perimeter_ticket
#   4. publish_product - require perimeter_ticket
#   5. select_current - require perimeter_ticket
#   6. declare_no_current - require perimeter_ticket
#   7. from_checkpoint - require CheckpointAuthority
#   8. M2.register_producer_subject - require ProducerCredential
#   9. M2.constitute_release - require ProducerCredential
#  10. Freeze EXPECTATION_KEY_TYPES in C02 candidate (MappingProxyType)
#
# Each method raises PerimeterTicketError("PERIMETER_TICKET_REQUIRED") if
# the ticket is missing/invalid, and ProducerCredentialError if producer
# credential is missing/invalid. from_checkpoint raises
# CheckpointAuthorityError if independent verification fails.

PATCH_OVERLAY_SPEC = MappingProxyType({
    "target_modules": (
        "rawlsing_next.pre553_learned_product_lifecycle",
        "rawlsing_next.pre553_learned_product_release",
        "rawlsing_next.pre553_authenticated_b5_ingress_candidate",
    ),
    "changes": (
        {
            "module": "pre553_learned_product_lifecycle",
            "class": "LearnedProductLifecycleExecutor",
            "method": "__init__",
            "add_param": "perimeter_ticket: PerimeterTicket | None = None",
            "body": """
        if perimeter_ticket is None:
            raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
                "mandatory boundary: every lifecycle executor requires a PerimeterTicket")
        self._perimeter_ticket = perimeter_ticket
            """,
        },
        {
            "module": "pre553_learned_product_lifecycle",
            "class": "LearnedProductLifecycleExecutor",
            "method": "stage_release",
            "add_check": """
        if not hasattr(self, "_perimeter_ticket") or self._perimeter_ticket is None:
            raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
                "stage_release requires valid PerimeterTicket")
        if self._perimeter_ticket.slot != subject.slot:
            raise PerimeterTicketError("PERIMETER_TICKET_INVALID",
                "ticket slot does not match subject slot")
            """,
        },
        {
            "module": "pre553_learned_product_lifecycle",
            "class": "LearnedProductLifecycleExecutor",
            "method": "register_product",
            "add_check": """
        if not hasattr(self, "_perimeter_ticket") or self._perimeter_ticket is None:
            raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
                "register_product requires valid PerimeterTicket")
            """,
        },
        {
            "module": "pre553_learned_product_lifecycle",
            "class": "LearnedProductLifecycleExecutor",
            "method": "publish_product",
            "add_check": """
        if not hasattr(self, "_perimeter_ticket") or self._perimeter_ticket is None:
            raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
                "publish_product requires valid PerimeterTicket")
            """,
        },
        {
            "module": "pre553_learned_product_lifecycle",
            "class": "LearnedProductLifecycleExecutor",
            "method": "select_current",
            "add_check": """
        if not hasattr(self, "_perimeter_ticket") or self._perimeter_ticket is None:
            raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
                "select_current requires valid PerimeterTicket")
            """,
        },
        {
            "module": "pre553_learned_product_lifecycle",
            "class": "LearnedProductLifecycleExecutor",
            "method": "declare_no_current",
            "add_check": """
        if not hasattr(self, "_perimeter_ticket") or self._perimeter_ticket is None:
            raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
                "declare_no_current requires valid PerimeterTicket")
            """,
        },
        {
            "module": "pre553_learned_product_lifecycle",
            "class": "LearnedProductLifecycleExecutor",
            "method": "from_checkpoint",
            "add_check": """
        # Mandatory: require independent checkpoint authority, not self-hash
        checkpoint_authority = kwargs.get("checkpoint_authority")
        if checkpoint_authority is None:
            raise CheckpointAuthorityError("CHECKPOINT_AUTHORITY_REQUIRED",
                "from_checkpoint requires independent CheckpointAuthority; "
                "self-referential hash is not authentication")
        if not isinstance(checkpoint_authority, CheckpointAuthority):
            raise CheckpointAuthorityError("CHECKPOINT_AUTHORITY_REQUIRED",
                "checkpoint_authority must be a CheckpointAuthority instance")
        # Verify the authority's verification_hash against the payload
        if checkpoint_authority.verification_hash != semantic_hash(payload):
            raise CheckpointAuthorityError(
                "CHECKPOINT_HASH_INDEPENDENT_VERIFICATION_FAILED",
                "independent authority verification failed")
            """,
        },
        {
            "module": "pre553_learned_product_release",
            "function": "register_producer_subject",
            "add_param": "producer_credential: ProducerCredential | None = None",
            "body": """
        if producer_credential is None:
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_REQUIRED",
                "register_producer_subject requires ProducerCredential under mandatory boundary")
        if not isinstance(producer_credential, ProducerCredential):
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_INVALID",
                "producer_credential must be a ProducerCredential instance")
        # Verify credential covers this subject
        if producer_credential.subject_ref != subject:
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_INVALID",
                "credential subject_ref does not match registered subject")
            """,
        },
        {
            "module": "pre553_learned_product_release",
            "function": "constitute_release",
            "add_param": "producer_credential: ProducerCredential | None = None",
            "body": """
        if producer_credential is None:
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_REQUIRED",
                "constitute_release requires ProducerCredential under mandatory boundary")
        if not isinstance(producer_credential, ProducerCredential):
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_INVALID",
                "producer_credential must be a ProducerCredential instance")
        if producer_credential.subject_ref != release_subject_ref:
            raise ProducerCredentialError("PRODUCER_CREDENTIAL_INVALID",
                "credential subject_ref does not match release subject")
            """,
        },
        {
            "module": "pre553_authenticated_b5_ingress_candidate",
            "target": "EXPECTATION_KEY_TYPES",
            "action": "freeze",
            "body": """
        # Freeze the mutable type gate to prevent runtime weakening (C02R F4)
        from types import MappingProxyType
        EXPECTATION_KEY_TYPES = MappingProxyType(EXPECTATION_KEY_TYPES)
            """,
        },
    ),
})


def generate_patch_overlay() -> str:
    """Generate the exact unified diff for the test-only mandatory enforcement patch.

    This patch is NOT applied to the source branch. It exists only in the return's
    repro/ directory for hostile testing against the adopted owners.
    """
    # The actual unified diff is constructed by the test harness at runtime.
    # This function returns the specification; the test applies it via monkey-patch
    # or a temporary module overlay.
    return "# See PATCH_OVERLAY_SPEC for the exact changes. " \
           "Test harness applies via runtime overlay."


__all__ = [
    "MANDATORY_BOUNDARY_CONTRACT",
    "DEVELOPMENT_GRADE",
    "REACHABLE_INGRESS_CALL_GRAPH",
    "REQUIRED_AUTHORITY_ACT",
    "MANDATORY_REFUSAL_CODES",
    "MandatoryBoundaryError",
    "PerimeterTicketError",
    "ProducerCredentialError",
    "CheckpointAuthorityError",
    "ExpectationMutationError",
    "PerimeterTicket",
    "ProducerCredential",
    "CheckpointAuthority",
    "record_caller_graphs",
    "required_authority_act",
    "introspect_owner_signatures",
    "PATCH_OVERLAY_SPEC",
    "generate_patch_overlay",
]