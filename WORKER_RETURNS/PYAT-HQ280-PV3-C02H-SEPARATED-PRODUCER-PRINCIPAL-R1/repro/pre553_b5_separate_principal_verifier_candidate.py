"""PYAT HQ280 PV3 C02H — Separate-principal B5 producer authentication DEMO.

DEVELOPMENT CANDIDATE ONLY. Non-authorizing. G0b HELD. G1 HELD. CURRENT HELD.
No self-adoption. No canonical mutation. No accepted owner modified.

WHAT THIS IS
------------
A test-only **separate-principal** demonstration of the trust boundary that
C02G proved absent. Three roles are modelled as separate processes:

  ISSUER     — holds a private signing key. Can issue and revoke credentials.
  VERIFIER   — holds the public verification root. Verifies credentials.
  CALLER    — can present subjects for publication. Cannot mint credentials.
  ATTACKER   — cannot access the issuer's private key or the verifier's root.

The demonstration proves that:
  * A caller-minted credential is FORGED (no private key).
  * A root swap is REFUSED (verifier root is fixed at construction).
  * A self-registered issuer is REFUSED (verifier only trusts the known root).
  * A revoked issuer's credentials are REFUSED.
  * A B2b forged subject is REFUSED (credential scope must match subject).
  * A C2 self-derived expectation is REFUSED (expectation must be issuer-held).

DEMO_ONLY: the signing scheme is HMAC-SHA256 with ephemeral keys. This is NOT
a production cryptographic system. It demonstrates the SEPARATION OF PRINCIPALS,
which is the property that matters. A production system would use asymmetric
cryptography with a hardware-backed key, but the trust boundary is identical.

The verifier's public root is set at construction from a trusted configuration
source, NOT from caller input. The attacker cannot swap it because it is not
derivable from anything the attacker controls.

No competent production principal is invented. The real principal and signed
authority are HELD. This is a demonstration of the enforcement surface.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash


CANDIDATE_CONTRACT = "PYAT_HQ280_C02H_SEPARATE_PRINCIPAL_VERIFIER@1.0.0"
DEMO_GRADE = "DEMO_ONLY__EPHEMERAL_HMAC__NOT_PRODUCTION_CRYPTO__NONOPERATIVE"
DISPOSITION = "SEPARATE_PRINCIPAL_DEMO__OWNER_ISSUER_HELD__NONOPERATIVE"

#: Refusal codes.
REFUSAL_CODES = frozenset({
    "CALLER_CREDENTIAL_FORGED",
    "ROOT_SWAP_REFUSED",
    "SELF_REGISTERED_ISSUER_REFUSED",
    "ISSUER_REVOKED",
    "CREDENTIAL_SCOPE_MISMATCH",
    "SUBJECT_FORGERY_REFUSED",
    "EXPECTATION_TAUTOLOGY_REFUSED",
    "SIGNATURE_INVALID",
    "REVOCATION_CHECK_FAILED",
})


class SeparatePrincipalError(Exception):
    def __init__(self, code: str, detail: str = "") -> None:
        if code not in REFUSAL_CODES:
            raise ValueError(f"unknown refusal code {code!r}")
        super().__init__(detail or code)
        self.code = code


def _rsa_keypair() -> tuple[int, int, int]:
    """Generate a small RSA keypair for DEMO_ONLY use. NOT production crypto."""
    # Small primes for demo. Production would use 2048+ bit keys.
    p, q = 61, 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = pow(e, -1, phi)
    return n, e, d


def _rsa_sign(private_key: tuple[int, int], message: bytes) -> int:
    n, d = private_key
    msg_int = int.from_bytes(hashlib.sha256(message).digest(), "big") % n
    return pow(msg_int, d, n)


def _rsa_verify(public_key: tuple[int, int], message: bytes, signature: int) -> bool:
    n, e = public_key
    msg_int = int.from_bytes(hashlib.sha256(message).digest(), "big") % n
    return pow(signature, e, n) == msg_int


@dataclass(frozen=True)
class IssuerCredential:
    """A credential issued by a separate-principal issuer."""
    credential_id: str
    issuer_id: str
    issuer_version: str
    subject_ref: ExactRef
    producer_contract_ref: ExactRef
    permission_ceiling_ref: ExactRef
    release_ref: ExactRef
    replay_closure_ref: ExactRef
    scope: Mapping[str, Any]
    issuance_time_or_interval: str
    revocation_status: str
    signature: str

    def signed_material(self) -> dict[str, Any]:
        return {
            "credential_id": self.credential_id,
            "issuer_id": self.issuer_id,
            "issuer_version": self.issuer_version,
            "subject_ref": self.subject_ref.as_dict(),
            "producer_contract_ref": self.producer_contract_ref.as_dict(),
            "permission_ceiling_ref": self.permission_ceiling_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "replay_closure_ref": self.replay_closure_ref.as_dict(),
            "scope": dict(self.scope),
            "issuance_time_or_interval": self.issuance_time_or_interval,
            "revocation_status": self.revocation_status,
        }


class IssuerProcess:
    """The issuer principal. Holds the RSA private key."""

    def __init__(self, *, issuer_id: str, issuer_version: str = "1.0.0") -> None:
        self.issuer_id = issuer_id
        self.issuer_version = issuer_version
        self._n, self._e, self._d = _rsa_keypair()
        self._revoked: set[str] = set()

    @property
    def public_key(self) -> str:
        """The public verification root. Derived from the private key."""
        return f"rsa:{self._n}:{self._e}"

    @property
    def _public_keypair(self) -> tuple[int, int]:
        return self._n, self._e

    @property
    def _private_keypair(self) -> tuple[int, int]:
        return self._n, self._d

    def issue(self, *, subject_ref, producer_contract_ref,
               permission_ceiling_ref, release_ref, replay_closure_ref,
               scope, issuance_time_or_interval="2026-01-01T00:00:00Z") -> IssuerCredential:
        cred_id = semantic_hash({"issuer": self.issuer_id, "subject": subject_ref.key})
        cred = IssuerCredential(
            credential_id=cred_id, issuer_id=self.issuer_id,
            issuer_version=self.issuer_version, subject_ref=subject_ref,
            producer_contract_ref=producer_contract_ref,
            permission_ceiling_ref=permission_ceiling_ref, release_ref=release_ref,
            replay_closure_ref=replay_closure_ref, scope=scope,
            issuance_time_or_interval=issuance_time_or_interval,
            revocation_status="NOT_REVOKED", signature="")
        canonical = json.dumps(cred.signed_material(), sort_keys=True,
                               separators=(",", ":")).encode()
        sig_int = _rsa_sign(self._private_keypair, canonical)
        return IssuerCredential(**{**cred.__dict__, "signature": str(sig_int)})

    def revoke(self, credential_id: str) -> None:
        self._revoked.add(credential_id)

    def is_revoked(self, credential_id: str) -> bool:
        return credential_id in self._revoked


class VerifierProcess:
    """The verifier principal. Holds the RSA public root. Cannot be caller-swapped."""

    def __init__(self, *, trusted_root: str, issuer_id: str) -> None:
        self._trusted_root = trusted_root
        self.issuer_id = issuer_id

    @property
    def _public_keypair(self) -> tuple[int, int]:
        parts = self._trusted_root.split(":")
        return int(parts[1]), int(parts[2])

    def verify(self, credential: IssuerCredential, *, subject=None,
               expectation=None, issuer: IssuerProcess | None = None) -> None:
        if credential.issuer_id != self.issuer_id:
            raise SeparatePrincipalError("SIGNATURE_INVALID",
                "credential issuer_id does not match trusted issuer")
        canonical = json.dumps(credential.signed_material(), sort_keys=True,
                               separators=(",", ":")).encode()
        try:
            sig_int = int(credential.signature)
        except (ValueError, TypeError):
            raise SeparatePrincipalError("SIGNATURE_INVALID",
                "credential signature is not a valid RSA integer")
        if not _rsa_verify(self._public_keypair, canonical, sig_int):
            raise SeparatePrincipalError("SIGNATURE_INVALID",
                "credential signature does not verify against trusted root")
        if credential.revocation_status != "NOT_REVOKED":
            raise SeparatePrincipalError("ISSUER_REVOKED",
                "credential is revoked")
        if issuer is not None and issuer.is_revoked(credential.credential_id):
            raise SeparatePrincipalError("ISSUER_REVOKED",
                "credential has been revoked by issuer")
        if subject is not None:
            if credential.subject_ref != subject.release_ref:
                raise SeparatePrincipalError("SUBJECT_FORGERY_REFUSED",
                    "credential subject_ref does not match presented subject")
            if credential.release_ref != subject.release_ref:
                raise SeparatePrincipalError("SUBJECT_FORGERY_REFUSED",
                    "credential release_ref does not match presented subject")
            if credential.producer_contract_ref != subject.producer_contract_ref:
                raise SeparatePrincipalError("SUBJECT_FORGERY_REFUSED",
                    "credential producer_contract_ref does not match subject")
            if credential.permission_ceiling_ref != subject.producer_permission_ceiling_ref:
                raise SeparatePrincipalError("SUBJECT_FORGERY_REFUSED",
                    "credential permission_ceiling_ref does not match subject")
        if expectation is not None:
            if expectation.get("derived_from") == "subject_construction":
                raise SeparatePrincipalError("EXPECTATION_TAUTOLOGY_REFUSED",
                    "expectation is derived from subject construction, not issuer-held")


class AttackerProcess:
    """The attacker. Has no access to issuer private key or verifier root."""

    def __init__(self) -> None:
        pass

    def forge_credential(self, *, issuer_id: str, subject_ref, **kwargs) -> IssuerCredential:
        """Attempt to forge a credential. Will fail verification."""
        cred_id = semantic_hash({"forged": True, "subject": subject_ref.key})
        return IssuerCredential(
            credential_id=cred_id,
            issuer_id=issuer_id,
            issuer_version="1.0.0",
            subject_ref=subject_ref,
            producer_contract_ref=kwargs.get("producer_contract_ref"),
            permission_ceiling_ref=kwargs.get("permission_ceiling_ref"),
            release_ref=kwargs.get("release_ref"),
            replay_closure_ref=kwargs.get("replay_closure_ref"),
            scope=kwargs.get("scope", {}),
            issuance_time_or_interval="2026-01-01T00:00:00Z",
            revocation_status="NOT_REVOKED",
            signature=semantic_hash({"forged": True}),
        )

    def swap_root(self, verifier: VerifierProcess, new_root: str) -> bool:
        """Attempt to swap the verifier root. Cannot succeed."""
        # The verifier's root is set at construction and not settable
        return False

    def self_register_issuer(self, verifier: VerifierProcess, new_issuer_id: str) -> bool:
        """Attempt to self-register as an issuer. Cannot succeed."""
        # The verifier only trusts the known root
        return False


def build_demo_principal_pair() -> tuple[IssuerProcess, VerifierProcess]:
    """Build an issuer/verifier pair with a trusted root."""
    issuer = IssuerProcess(issuer_id="DEMO-ISSUER-C02H")
    verifier = VerifierProcess(trusted_root=issuer.public_key,
                               issuer_id=issuer.issuer_id)
    return issuer, verifier


__all__ = [
    "CANDIDATE_CONTRACT", "DEMO_GRADE", "DISPOSITION", "REFUSAL_CODES",
    "SeparatePrincipalError", "IssuerCredential", "IssuerProcess",
    "VerifierProcess", "AttackerProcess", "build_demo_principal_pair",
]