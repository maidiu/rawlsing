"""Operation-scoped interpretation invariants for source-exact S04/FF01.

The physical observation and its interpretation are distinct. A source
value whose interpretation is still INVALID_UNRESOLVED cannot count as
substantive support even if an otherwise hash-valid, internally consistent
EmpiricalFact labels it SUPPORTED. Distinct missing/routing states stay
typed; no unknown is coerced into a negative or a zero.

A bound current-interpretation callback is a check on an *existing exact*
source response-semantic authority ref. It is not a new interpretation
authority, a mapping issuer, an original-source grant, or a substitute for
Codex C11's source-native construction and query semantics.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json

UNRESOLVED_STATE = "INVALID_UNRESOLVED"
UNRESOLVED_TYPED_KEYS = frozenset((
    "typed_response_state", "response_state", "typed_state",
))


class InterpretationQualificationError(ValueError):
    """Interpretation uncertainty or currentness forbids substantive use."""


def contains_unresolved_response(value: Any) -> bool:
    """Recognize source-typed unresolved observations, not mere absent labels.

    Only exact typed state markers are refused. A free-text string which
    happens to mention 'unknown', a legitimate response category named
    'missing', source-declared MISSING and routed NOT_ASKED are NOT this
    condition. This does not reclassify raw recorded values.
    """
    if isinstance(value, Mapping):
        if any(
            value.get(key) == UNRESOLVED_STATE
            for key in UNRESOLVED_TYPED_KEYS
        ):
            return True
        return any(contains_unresolved_response(x) for x in value.values())
    if isinstance(value, (list, tuple)):
        return any(contains_unresolved_response(x) for x in value)
    return False


def refuse_positive_uninterpreted_support(
    *,
    cell: Any,
    raw_support: Any,
    consumer: str,
) -> None:
    """Fail closed only when unknown meaning is POSITIVELY counted.

    A diagnostic target domain may list INVALID_UNRESOLVED with exactly ZERO
    observed members; this must not be confused with a positive substantive
    sample fraction. Publishing response-state *diagnostic* counts needs
    a separate, expressly qualified consumer, not the FF01/S04 default
    substantive sample reader.
    """
    if type(raw_support) is not int or raw_support < 0:
        raise InterpretationQualificationError(
            f"{consumer}: nonnegative exact raw support required"
        )
    if raw_support > 0 and contains_unresolved_response(cell):
        raise InterpretationQualificationError(
            f"{consumer}: UNRESOLVED_INTERPRETATION_CANNOT_BE_SUBSTANTIVE_SUPPORT"
        )


class S04InterpretationCurrent:
    """Existing response-state-semantic-ref pin and externally resolved CURRENT.

    Both pin and resolver are supplied from the *same operation's* qualified
    source/authority custody; a consumer must not construct a fabricated
    resolver from an untrusted saved receipt. This detects source semantic
    version changes while preserving the same physical C11 observations.

    This is deliberately NOT a mapping-version issuer or certification of
    what the owner-provided resolver is authorized to return.
    """

    def __init__(
        self,
        *,
        expected_response_semantics_ref: ExactRef,
        resolve_current_response_semantics_ref: Callable[[], ExactRef],
    ) -> None:
        if (type(expected_response_semantics_ref) is not ExactRef
                or not callable(resolve_current_response_semantics_ref)):
            raise InterpretationQualificationError(
                "exact source-semantic identity and a real version resolver required"
            )
        self.expected_ref = expected_response_semantics_ref
        self._resolver = resolve_current_response_semantics_ref

    def assert_bound_to(self, actual_source_response_semantics_ref: ExactRef) -> None:
        if (type(actual_source_response_semantics_ref) is not ExactRef
                or actual_source_response_semantics_ref != self.expected_ref):
            raise InterpretationQualificationError(
                "INTERPRETATION_BINDING_NOT_IN_SOURCE_QUERY_AND_FACT"
            )
        self.check_current()

    def check_current(self) -> None:
        observed = self._resolver()
        if type(observed) is not ExactRef or observed != self.expected_ref:
            raise InterpretationQualificationError(
                "INTERPRETATION_VERSION_STALE_OR_UNVERIFIED"
            )


__all__ = [
    "UNRESOLVED_STATE", "UNRESOLVED_TYPED_KEYS",
    "InterpretationQualificationError",
    "contains_unresolved_response", "refuse_positive_uninterpreted_support",
    "S04InterpretationCurrent",
]
