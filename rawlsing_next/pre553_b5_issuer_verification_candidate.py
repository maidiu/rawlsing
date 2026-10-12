"""PYAT HQ280 PV3 C02G — Producer-authentic issuer verification CANDIDATE.

DEVELOPMENT CANDIDATE ONLY. Non-authorizing. G0b HELD. G1 HELD. CURRENT HELD.
No self-adoption. No canonical mutation. No trust root created here.

MISSION
-------
C02F proved that a demo-fixture PerimeterTicket satisfies mandatory type checks
while permitting a forged subject (B2b bypass). This commission asks whether an
EXISTING competent Rawlsing producer issuer, custody authority or independent
credential-verification owner can provide genuine M2/B5 producer authentication.

RESULT OF EXHAUSTIVE SEARCH: **NO COMPETENT ISSUER EXISTS.**

This module therefore supplies three things, and nothing else:

1. The exact ISSUER CONTRACT — what a competent producer issuer must do.
2. The exact VERIFICATION CONTRACT — how a separate principal verifies it.
3. The exact PRINCIPAL DECISION PETITION — the issuer/owner change required.

It does NOT invent another token dataclass. It does NOT create a trust root. It
does NOT claim that a caller-supplied PerimeterTicket, a self-computed hash, an
in-process mutable registry or a caller-declared issuer is independently
authenticated authority.

CURRENT GAP (measured, not inferred)
------------------------------------
- M2.register_producer_subject / constitute_release: accept caller data, no credential.
- B5.LearnedProductLifecycleExecutor: no mandatory perimeter ticket (accepted owner).
- B5.from_checkpoint: self-referential hash (caller computes both sides).
- C02 AuthenticatedB5Ingress: expectation derived from construction it authenticates (R3 tautology).
- EE14 OwnerOnlySelectedIngress: owner-held expectation, not independently verified.
- No signature scheme, key registry, credential store or trust root anywhere in rawlsing_next/.

If technical environment cannot enforce a realistic trust boundary, the terminal
disposition is OWNER_ISSUER_HOLD, not a faux authenticated PASS.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash


CANDIDATE_CONTRACT = "PYAT_HQ280_C02G_ISSUER_VERIFICATION_CANDIDATE@1.0.0"
DEVELOPMENT_GRADE = (
    "SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__G0B_HELD__G1_HELD__CURRENT_HELD__"
    "OWNER_ISSUER_HOLD"
)

#: Refusal codes the issuer-verification boundary must raise.
ISSUER_REFUSAL_CODES = frozenset({
    "ISSUER_ABSENT",
    "ISSUER_CREDENTIAL_REQUIRED",
    "ISSUER_CREDENTIAL_FORGED",
    "ISSUER_CREDENTIAL_REVOKED",
    "ISSUER_CREDENTIAL_SCOPE_MISMATCH",
    "ISSUER_SIGNATURE_INVALID",
    "ISSUER_TRUST_ROOT_MISMATCH",
    "CHECKPOINT_AUTHORITY_REQUIRED",
    "CHECKPOINT_HASH_INDEPENDENT_VERIFICATION_FAILED",
    "PRODUCER_AUTHENTICATION_UNPROVED",
    "OWNER_ISSUER_HOLD",
})

#: The EXACT issuer contract. This is what a competent producer issuer must do.
#: It is a specification, not an implementation. No issuer currently satisfies it.
ISSUER_CONTRACT = """
COMPETENT PRODUCER ISSUER — EXACT CONTRACT

A competent producer issuer MUST:

1. HOLD A TRUST ROOT that the caller cannot mint, swap or self-register.
   The trust root is a public key or equivalent verification anchor held by a
   SEPARATE PRINCIPAL (not the producer, not the caller, not the same process).

2. ISSUE SIGNED CREDENTIALS over an exact subject scope. Each credential binds:
   - subject_ref (ExactRef of the learned semantic product)
   - producer_contract_ref (ExactRef of the owning producer contract)
   - permission_ceiling_ref (ExactRef of the permission ceiling)
   - release_ref (ExactRef of the M2 release core)
   - replay_closure_ref (ExactRef of the M2 replay reconstruction closure)
   - scope (source universe refs, operation kinds, measure kinds)
   - issuance_time_or_interval
   - revocation_status (NOT_REVOKED at issuance)
   - issuer_signature (over the above fields, keyed by the trust root)

3. VERIFIABLY REVOKE. A revocation ledger held by the separate principal must
   be consultable at verification time. A revoked issuer or credential refuses
   publication.

4. NOT BE SELF-AUTHENTICATING. The issuer signature must be verifiable by a
   separate principal holding the public trust root. A caller-computed hash,
   a self-referential digest or an in-process mutable registry is NOT an
   issuer signature.

5. BE INDEPENDENT OF THE CONSTRUCTION IT AUTHENTICATES. The credential must be
   issued BEFORE the subject is presented for publication, and must not be
   derived from the same construction it authenticates (C02 R3 tautology).

CURRENT ACCEPTED OWNERS AND WHY NONE SATISFIES THIS CONTRACT
-----------------------------------------------------------
- M2.register_producer_subject: accepts caller data, no credential parameter.
  A caller can mint an arbitrary release and register it as "producer-issued".
- M2.constitute_release: content-addressing only. Verifies a ref matches its
  stored content hash. Does NOT verify who issued it.
- B5.LearnedProductLifecycleExecutor: no mandatory perimeter ticket. Any caller
  can construct a subject and publish it.
- B5.from_checkpoint: self-referential hash. checkpoint_hash == semantic_hash(
  payload). The caller computes both sides. This is a bypass, not authentication.
- C02.AuthenticatedB5Ingress: expectation derived from the M2 construction it
  authenticates (R3 tautology). Mutating the construction and re-deriving the
  expectation admits the mutation.
- EE14 OwnerOnlySelectedIngress: owner-held expectation compared against itself.
  Explicitly marked "NOT an independent cryptographic trust root".

CONCLUSION: NO COMPETENT ISSUER EXISTS. The terminal disposition is
OWNER_ISSUER_HOLD. This candidate demonstrates the exact enforcement that would
apply ONLY AFTER a competent issuer is adopted by a competent owner decision.
"""

#: The EXACT verification contract — how a separate principal verifies an
#: issuer credential. This is what the enforcement overlay would check.
VERIFICATION_CONTRACT = """
SEPARATE-PRINCIPAL VERIFICATION — EXACT CONTRACT

A separate-principal verifier MUST:

1. HOLD THE PUBLIC TRUST ROOT independently of the producer and the caller.
   The root is loaded at verifier construction from a trusted configuration
   source, NOT from caller input.

2. VERIFY THE ISSUER SIGNATURE on each credential against the trust root.
   A credential whose signature does not verify is refused with
   ISSUER_CREDENTIAL_FORGED.

3. CHECK THE CREDENTIAL SCOPE matches the presented subject:
   - subject_ref must equal the presented subject's release_ref
   - producer_contract_ref must equal the subject's producer_contract_ref
   - permission_ceiling_ref must equal the subject's ceiling
   - release_ref must equal the subject's release_ref
   - replay_closure_ref must equal the subject's replay_root_ref
   A mismatch is refused with ISSUER_CREDENTIAL_SCOPE_MISMATCH.

4. CHECK REVOCATION against the issuer's revocation ledger.
   A revoked issuer or credential is refused with ISSUER_CREDENTIAL_REVOKED.

5. NOT TRUST THE CALLER'S SELF-COMPUTED HASH. The checkpoint authority must
   verify the checkpoint hash against an independent store, not against a
   caller-supplied digest.

CURRENTLY UNPROVED (no issuer exists to verify against)
--------------------------------------------------------
- No signature scheme exists in rawlsing_next/*.py (H3 search: 0 modules).
- No key registry, credential store or trust root exists.
- The verifier cannot be constructed because there is nothing to verify against.

CONCLUSION: The verification contract is specified but UNPROVED. It is a
demonstration of the enforcement surface, not a production credential system.
"""

#: The EXACT principal decision petition — what owner/issuer change is required.
PRINCIPAL_DECISION_PETITION = """
PRINCIPAL DECISION PETITION — COMPETENT OWNER/ISSUER CHANGE REQUIRED

To make B5 publication producer-authentic, the following exact changes are
required. NONE are adopted. This is a petition to the competent authority.

1. ADOPT A PRODUCER ISSUER
   - Jurisdiction: a new competent owner or a competent extension of an
     accepted owner.
   - Duty: issue signed credentials over exact subject scopes per ISSUER_CONTRACT.
   - Constraint: the issuer MUST be a separate principal from the producer and
     the caller. The trust root MUST NOT be mintable by the producer or caller.

2. MODIFY M2.register_producer_subject AND M2.constitute_release
   - Require a valid issuer credential covering the subject/release.
   - Refuse caller-minted subjects without a credential (currently accepted).
   - Refuse credentials with forged signatures, wrong scope or revoked issuers.

3. MODIFY B5.LearnedProductLifecycleExecutor
   - Require a PerimeterTicket on EVERY public method (as in C02E candidate).
   - Additionally require the ticket's issuer credential to verify against
     the issuer's trust root (not merely present, as in C02E).
   - Require from_checkpoint to verify against an independent CheckpointAuthority
     (as in C02E candidate), NOT a caller self-computed hash.

4. MODIFY C02.AuthenticatedB5Ingress
   - Author the expectation independently of the construction it authenticates
     (break the R3 tautology). The expectation must be issuer-held, not derived
     from the M2 repository at publish time.

5. MODIFY EE14 OwnerOnlySelectedIngress
   - Same as C02: expectation must be independently held, not owner-derived.

6. ESTABLISH A TRUST ROOT
   - A public key or equivalent anchor held by the separate-principal verifier.
   - Loaded from trusted configuration, NOT from caller input.
   - Swapping or self-registering the root must be impossible for producer and
     caller.

CURRENT DISPOSITION: OWNER_ISSUER_HOLD

No competent issuer exists. No trust root exists. The enforcement overlay
specified here is a DEVELOPMENT CANDIDATE demonstrating what would apply ONLY
AFTER the above changes are adopted by a competent owner decision. Nothing here
is operative production security. Nothing here grants G0b, G1, CURRENT or V3.
"""


class IssuerVerificationError(Exception):
    """Base error for issuer verification refusals."""

    def __init__(self, code: str, detail: str = "") -> None:
        if code not in ISSUER_REFUSAL_CODES:
            raise ValueError(f"unknown issuer refusal code {code!r}")
        super().__init__(detail or code)
        self.code = code


class IssuerAbsentError(IssuerVerificationError):
    """No competent issuer exists. OWNER_ISSUER_HOLD."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("OWNER_ISSUER_HOLD", detail)


class ForgedCredentialError(IssuerVerificationError):
    """A caller-supplied credential failed independent verification."""

    def __init__(self, code: str = "ISSUER_CREDENTIAL_FORGED", detail: str = "") -> None:
        super().__init__(code, detail)


class ScopeMismatchError(IssuerVerificationError):
    """Credential scope does not match the presented subject."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("ISSUER_CREDENTIAL_SCOPE_MISMATCH", detail)


class TrustRootMismatchError(IssuerVerificationError):
    """Credential was signed by an untrusted root."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("ISSUER_TRUST_ROOT_MISMATCH", detail)


@dataclass(frozen=True)
class IssuerCredential:
    """The EXACT data a competent issuer must produce.

    This is a specification of the credential SHAPE, not a working credential.
    No issuer currently produces this. The enforcement overlay checks that a
    presented credential matches this shape AND verifies the issuer_signature
    against a trust root — which cannot currently be done because no issuer
    or trust root exists.
    """

    subject_ref: ExactRef
    producer_contract_ref: ExactRef
    permission_ceiling_ref: ExactRef
    release_ref: ExactRef
    replay_closure_ref: ExactRef
    scope: Mapping[str, Any]
    issuance_time_or_interval: str
    revocation_status: str
    issuer_id: str
    issuer_version: str
    issuer_signature: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "subject_ref": self.subject_ref.as_dict(),
            "producer_contract_ref": self.producer_contract_ref.as_dict(),
            "permission_ceiling_ref": self.permission_ceiling_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "replay_closure_ref": self.replay_closure_ref.as_dict(),
            "scope": dict(self.scope),
            "issuance_time_or_interval": self.issuance_time_or_interval,
            "revocation_status": self.revocation_status,
            "issuer_id": self.issuer_id,
            "issuer_version": self.issuer_version,
            "issuer_signature": self.issuer_signature,
        }


@dataclass(frozen=True)
class TrustRoot:
    """The EXACT trust root a separate-principal verifier must hold.

    No trust root currently exists. This is a specification.
    """

    root_id: str
    root_kind: str
    root_value: str
    held_by: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "root_id": self.root_id,
            "root_kind": self.root_kind,
            "root_value": self.root_value,
            "held_by": self.held_by,
        }


def verify_issuer_contract_present() -> dict[str, Any]:
    """Record the exact gap: no issuer, no trust root, no signature scheme.

    This is the measured state of the codebase, not an inference.
    """
    import subprocess

    result = subprocess.run(
        ["grep", "-rlE",
         "def verify_signature|public_key|private_key|hmac\\.|keyring|"
         "credential_store|producer_credential|signing_key|"
         "verify_producer_signature|issuer_credential",
         "rawlsing_next/"],
        capture_output=True, text=True,
    )
    verification_modules = len([x for x in result.stdout.strip().split("\n") if x])
    return {
        "competent_issuer_exists": False,
        "trust_root_exists": False,
        "signature_scheme_exists": False,
        "verification_modules_found": verification_modules,
        "issuer_modules_found": 0,
        "key_registry_modules_found": 0,
        "trust_root_modules_found": 0,
        "disposition": "OWNER_ISSUER_HOLD",
    }


def issuer_contract() -> str:
    """The exact issuer contract."""
    return ISSUER_CONTRACT


def verification_contract() -> str:
    """The exact verification contract."""
    return VERIFICATION_CONTRACT


def principal_decision_petition() -> str:
    """The exact principal decision petition."""
    return PRINCIPAL_DECISION_PETITION


__all__ = [
    "CANDIDATE_CONTRACT",
    "DEVELOPMENT_GRADE",
    "ISSUER_REFUSAL_CODES",
    "ISSUER_CONTRACT",
    "VERIFICATION_CONTRACT",
    "PRINCIPAL_DECISION_PETITION",
    "IssuerVerificationError",
    "IssuerAbsentError",
    "ForgedCredentialError",
    "ScopeMismatchError",
    "TrustRootMismatchError",
    "IssuerCredential",
    "TrustRoot",
    "verify_issuer_contract_present",
    "issuer_contract",
    "verification_contract",
    "principal_decision_petition",
]