"""Candidate-neutral EE-W3 semantic-capital objectizer.

This module is deliberately an objectizer, not a semantic adjudicator.  It can
materialize content-addressed response-category or routing/applicability refs
only from an exact implementation-to-meaning binding already supplied by a
competent current authority.  It never derives meaning from labels, free text,
numeric codes, frequencies, adjacency, resemblance, embeddings, or model
judgment.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash

CONTRACT_ID: Final[str] = "EE_W3_GOVERNED_SEMANTIC_CAPITAL_OBJECTIZER_R1@1.0.0"
REPLAY_CONTRACT_ID: Final[str] = "EE_W3_GOVERNED_SEMANTIC_CAPITAL_REPLAY_R1@1.0.0"

ROLE_RESPONSE_CATEGORY: Final[str] = "RESPONSE_CATEGORY_SEMANTICS"
ROLE_ROUTING_APPLICABILITY: Final[str] = "ROUTING_APPLICABILITY"

RESPONSE_POSITIVE_STATE: Final[str] = "CURRENT_POSITIVE_EXACT_RESPONSE_SEMANTICS_BINDING"
ROUTING_POSITIVE_STATES: Final[frozenset[str]] = frozenset(
    {
        "GENERAL_QUESTION_APPLICABLE__NO_ROUTING_PRECONDITION",
        "EXECUTABLE_CLOSED_WORLD_ROUTING_REQUIREMENT",
        "KNOWN_NON_APPLICABILITY__ROUTING_RULE_PROVES_OUT_OF_UNIVERSE",
    }
)


class SemanticCapitalIntegrityError(ValueError):
    """Required exact authority/binding material is missing, malformed, or ineligible."""


class SemanticCapitalReplayError(AssertionError):
    """A deterministic semantic-capital replay failed exact identity parity."""


def _exact(value: object, name: str) -> ExactRef:
    if not isinstance(value, ExactRef):
        raise SemanticCapitalIntegrityError(f"{name} must be ExactRef")
    return value


def _authority(value: object, name: str) -> AuthorityRef:
    if not isinstance(value, AuthorityRef):
        raise SemanticCapitalIntegrityError(f"{name} must be AuthorityRef")
    return value


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SemanticCapitalIntegrityError(f"{name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class SemanticCapitalInput:
    """Exact, already-authorized implementation-to-meaning binding material.

    ``governed_meaning_ref`` is a response-semantics contract ref for the
    response role and an exact routing/applicability basis ref for the routing
    role. ``exact_binding_ref`` is mandatory: the objectizer will not construct
    an implementation-to-meaning join from neighboring registries.
    """

    role: str
    implementation_ref: ExactRef
    governed_meaning_ref: ExactRef
    exact_binding_ref: ExactRef
    semantic_authority_ref: AuthorityRef
    currentness_ref: ExactRef
    source_provenance_ref: ExactRef
    typed_state: str

    def __post_init__(self) -> None:
        role = _nonempty(self.role, "role")
        if role not in {ROLE_RESPONSE_CATEGORY, ROLE_ROUTING_APPLICABILITY}:
            raise SemanticCapitalIntegrityError(f"unsupported semantic-capital role: {role}")
        object.__setattr__(self, "role", role)
        for field in (
            "implementation_ref",
            "governed_meaning_ref",
            "exact_binding_ref",
            "currentness_ref",
            "source_provenance_ref",
        ):
            object.__setattr__(self, field, _exact(getattr(self, field), field))
        object.__setattr__(
            self,
            "semantic_authority_ref",
            _authority(self.semantic_authority_ref, "semantic_authority_ref"),
        )
        state = _nonempty(self.typed_state, "typed_state")
        if role == ROLE_RESPONSE_CATEGORY and state != RESPONSE_POSITIVE_STATE:
            raise SemanticCapitalIntegrityError(
                "response-category objectization requires an exact current-positive response binding"
            )
        if role == ROLE_ROUTING_APPLICABILITY and state not in ROUTING_POSITIVE_STATES:
            raise SemanticCapitalIntegrityError(
                "routing objectization requires an exact positive/known routing disposition"
            )
        object.__setattr__(self, "typed_state", state)

    def semantic_projection(self) -> dict[str, object]:
        return {
            "contract_id": CONTRACT_ID,
            "role": self.role,
            "implementation_ref": self.implementation_ref.as_dict(),
            "governed_meaning_ref": self.governed_meaning_ref.as_dict(),
            "exact_binding_ref": self.exact_binding_ref.as_dict(),
            "semantic_authority_ref": self.semantic_authority_ref.as_dict(),
            "currentness_ref": self.currentness_ref.as_dict(),
            "source_provenance_ref": self.source_provenance_ref.as_dict(),
            "typed_state": self.typed_state,
        }


@dataclass(frozen=True)
class GovernedSemanticCapitalObject:
    """Content-addressed exact ref over already-governed semantic capital."""

    input: SemanticCapitalInput

    def __post_init__(self) -> None:
        if not isinstance(self.input, SemanticCapitalInput):
            raise SemanticCapitalIntegrityError("input must be SemanticCapitalInput")

    def semantic_projection(self) -> dict[str, object]:
        return self.input.semantic_projection()

    @property
    def exact_ref(self) -> ExactRef:
        content_hash = semantic_hash(self.semantic_projection())
        kind = (
            "RESPONSE_CATEGORY_SEMANTICS_OBJECT"
            if self.input.role == ROLE_RESPONSE_CATEGORY
            else "ROUTING_APPLICABILITY_OBJECT"
        )
        prefix = "response" if self.input.role == ROLE_RESPONSE_CATEGORY else "routing"
        return ExactRef(kind, f"{prefix}:{content_hash[:24]}", content_hash)


@dataclass(frozen=True)
class SemanticCapitalReplayReceipt:
    original_object_ref: ExactRef
    replayed_object_ref: ExactRef
    exact_binding_ref: ExactRef
    governed_meaning_ref: ExactRef
    content_hash: str

    def __post_init__(self) -> None:
        for field in (
            "original_object_ref",
            "replayed_object_ref",
            "exact_binding_ref",
            "governed_meaning_ref",
        ):
            object.__setattr__(self, field, _exact(getattr(self, field), field))
        content_hash = _nonempty(self.content_hash, "content_hash")
        if len(content_hash) != 64 or any(ch not in "0123456789abcdef" for ch in content_hash):
            raise SemanticCapitalIntegrityError("content_hash must be lowercase sha256")
        object.__setattr__(self, "content_hash", content_hash)

    def semantic_projection(self) -> dict[str, object]:
        return {
            "contract_id": REPLAY_CONTRACT_ID,
            "original_object_ref": self.original_object_ref.as_dict(),
            "replayed_object_ref": self.replayed_object_ref.as_dict(),
            "exact_binding_ref": self.exact_binding_ref.as_dict(),
            "governed_meaning_ref": self.governed_meaning_ref.as_dict(),
        }

    @property
    def exact_ref(self) -> ExactRef:
        return ExactRef(
            "SEMANTIC_CAPITAL_REPLAY_RECEIPT",
            f"replay:{self.content_hash[:24]}",
            self.content_hash,
        )

    def verify(self) -> None:
        if self.original_object_ref != self.replayed_object_ref:
            raise SemanticCapitalReplayError("semantic-capital replay changed object identity")
        if semantic_hash(self.semantic_projection()) != self.content_hash:
            raise SemanticCapitalReplayError("semantic-capital replay receipt hash mismatch")


def materialize_semantic_capital(value: SemanticCapitalInput) -> GovernedSemanticCapitalObject:
    """Objectize one exact positive binding; perform no semantic inference."""
    if not isinstance(value, SemanticCapitalInput):
        raise SemanticCapitalIntegrityError("value must be SemanticCapitalInput")
    return GovernedSemanticCapitalObject(value)


def replay_semantic_capital(value: GovernedSemanticCapitalObject) -> SemanticCapitalReplayReceipt:
    """Re-materialize from the exact bound input and verify identity parity."""
    if not isinstance(value, GovernedSemanticCapitalObject):
        raise SemanticCapitalIntegrityError("value must be GovernedSemanticCapitalObject")
    replayed = materialize_semantic_capital(value.input)
    if replayed.exact_ref != value.exact_ref:
        raise SemanticCapitalReplayError("deterministic replay did not reproduce object identity")
    projection = {
        "contract_id": REPLAY_CONTRACT_ID,
        "original_object_ref": value.exact_ref.as_dict(),
        "replayed_object_ref": replayed.exact_ref.as_dict(),
        "exact_binding_ref": value.input.exact_binding_ref.as_dict(),
        "governed_meaning_ref": value.input.governed_meaning_ref.as_dict(),
    }
    receipt = SemanticCapitalReplayReceipt(
        original_object_ref=value.exact_ref,
        replayed_object_ref=replayed.exact_ref,
        exact_binding_ref=value.input.exact_binding_ref,
        governed_meaning_ref=value.input.governed_meaning_ref,
        content_hash=semantic_hash(projection),
    )
    receipt.verify()
    return receipt
