"""Generic warrant-plan binding and outer route-pass accounting.

This module binds ONE caller-supplied warrant/source-entry specification to ONE
governed source execution. It adds the outer workload account that the session
layer does not have, and it keeps four things apart that are constantly confused:

    EXPECTED (frozen authority)  !=  FLOOR (authority minimum)
    MAXIMUM (ceiling)           !=  OBSERVED (what the run measured)

and, separately:

    FROZEN_AUTHORITY            !=  IMPLEMENTATION_POLICY

A policy ceiling of one is not a historical expected count. This module refuses
to let the two blur, because the whole point of the account model is that a
reader-invocation count, a decoder entry, a full read and an outer route pass are
different quantities.

The outer FULL ROUTE PASS account
---------------------------------
``full_route_passes`` is an OUTER workload account. It is deliberately not
``decoder_invocations``, ``full_reads``, ``chunk_reads``, ``reader_invocations``
or ``path_opens``, and it never substitutes for any of them:

  * a completed pass is counted only when the governed operation SUCCEEDED, so a
    failed first attempt can never be reported as a completed pass;
  * the pass maximum refuses a second attempt BEFORE any second source operation,
    leaving every lower-layer account unmoved;
  * satisfying a ``full_reads`` floor requires ``full_reads``; chunking cannot
    stand in for it, because the constraint checker reads the named account only.

Nothing here is source-specific. There is no SRCxx constant, no source variable
name, and no per-source plan. The caller supplies the plan; this module binds it.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
import os
from typing import Any, Mapping

from rawlsing_next.pre553_source_access_broker import (
    SourceAccessBudget,
    SourceAccessViolation,
)
from rawlsing_next.pre553_source_session import (
    GovernedSourceSession,
    SourceOperationPlan,
)

__all__ = [
    "BINDING_IMPLEMENTATION_ID",
    "CountKind",
    "AuthorityLabel",
    "AccountConstraint",
    "RoutePassSpec",
    "BoundExecutionSpec",
    "BoundExecutionOutcome",
    "BoundSourceExecution",
    "BindingError",
    "POST_EXECUTION_CONSTRAINT_FAILED",
    "ROUTE_PASS_LIMIT_REACHED",
    "LOWER_LAYER_ACCOUNTS",
]

BINDING_IMPLEMENTATION_ID = "rawlsing_next/pre553_execution_binding.py"
POST_EXECUTION_CONSTRAINT_FAILED = "POST_EXECUTION_CONSTRAINT_FAILED"
ROUTE_PASS_LIMIT_REACHED = "ROUTE_PASS_LIMIT_REACHED"

# The outer pass is NOT any of these. Named here so the separation is explicit
# and testable rather than a matter of comment prose.
LOWER_LAYER_ACCOUNTS = (
    "decoder_invocations",
    "full_reads",
    "chunk_reads",
    "selected_reads",
    "metadata_reads",
    "reader_invocations",
    "path_opens",
)


class BindingError(ValueError):
    """The bound specification is not internally coherent. Raised before any access."""


class CountKind(str, Enum):
    """How a supplied count constrains the run. OBSERVED is never supplied."""

    EXACT = "EXACT"
    FLOOR = "FLOOR"
    MAXIMUM = "MAXIMUM"
    UNBOUND = "UNBOUND"


class AuthorityLabel(str, Enum):
    """Whether a number is frozen authority or an implementation policy.

    A policy ceiling is a stop-the-run constraint chosen by the mechanism. It is
    NOT a statement about what historically happened, and must never be recorded
    as one.
    """

    FROZEN_AUTHORITY = "FROZEN_AUTHORITY"
    IMPLEMENTATION_POLICY = "IMPLEMENTATION_POLICY"


@dataclass(frozen=True)
class AccountConstraint:
    """One caller-supplied constraint on one lower-layer account.

    Immutable. OBSERVED is produced at run time and is never a field here.
    """

    account: str
    kind: CountKind
    value: int | None = None
    authority: AuthorityLabel = AuthorityLabel.FROZEN_AUTHORITY

    def __post_init__(self) -> None:
        if not isinstance(self.account, str) or not self.account:
            raise BindingError("constraint account must be a non-empty string")
        if self.kind is CountKind.UNBOUND:
            if self.value is not None:
                raise BindingError("an UNBOUND constraint carries no value")
        else:
            if not isinstance(self.value, int) or isinstance(self.value, bool):
                raise BindingError(f"{self.kind.value} constraint requires an integer value")
            if self.value < 0:
                raise BindingError("constraint value must not be negative")
        if self.account == "full_route_passes":
            raise BindingError(
                "full_route_passes is the OUTER account and is bound through RoutePassSpec, "
                "not through a lower-layer AccountConstraint")

    def satisfied_by(self, observed: int) -> bool:
        if self.kind is CountKind.UNBOUND:
            return True
        if self.kind is CountKind.EXACT:
            return observed == int(self.value or 0)
        if self.kind is CountKind.FLOOR:
            return observed >= int(self.value or 0)
        return observed <= int(self.value or 0)

    def as_dict(self, observed: int | None = None) -> dict[str, Any]:
        out: dict[str, Any] = {
            "account": self.account,
            "kind": self.kind.value,
            "value": self.value,
            "authority": self.authority.value,
        }
        if observed is not None:
            out["observed"] = observed
            out["satisfied"] = self.satisfied_by(observed)
        return out


@dataclass(frozen=True)
class RoutePassSpec:
    """The OUTER full-route-pass account: expected value and maximum.

    ``expected`` is the frozen EXACT count when one exists; ``maximum`` is the
    ceiling. They are distinct fields and are reported distinctly.
    """

    expected: int | None = None
    maximum: int | None = None
    token: str | None = None

    def __post_init__(self) -> None:
        for name, v in (("expected", self.expected), ("maximum", self.maximum)):
            if v is not None and (not isinstance(v, int) or isinstance(v, bool) or v < 0):
                raise BindingError(f"full_route_passes {name} must be a non-negative integer or None")

    @property
    def expected_status(self) -> str:
        return "EXACT" if self.expected is not None else "UNBOUND"

    def admits(self, completed_so_far: int) -> bool:
        """Pre-operation gate: may another pass be attempted?"""
        if self.maximum is not None and completed_so_far >= self.maximum:
            return False
        return True


@dataclass(frozen=True)
class BoundExecutionSpec:
    """An immutable caller-supplied warrant/source-entry specification.

    Frozen: a bound execution cannot have its plan or budget swapped after
    binding. Use ``dataclasses.replace`` to derive a DIFFERENT spec deliberately.
    """

    source_entry_key: str
    path: str
    source_format: str
    plan: SourceOperationPlan
    expected_sha256: str | None = None
    budget: SourceAccessBudget = field(default_factory=SourceAccessBudget)
    route_pass: RoutePassSpec = field(default_factory=RoutePassSpec)
    constraints: tuple[AccountConstraint, ...] = ()
    authority_note: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_entry_key, str) or not self.source_entry_key.strip():
            raise BindingError("source_entry_key must be a non-empty string")
        if not isinstance(self.plan, SourceOperationPlan):
            raise BindingError("plan must be a SourceOperationPlan")
        if not isinstance(self.route_pass, RoutePassSpec):
            raise BindingError("route_pass must be a RoutePassSpec")
        seen = set()
        for c in self.constraints:
            if not isinstance(c, AccountConstraint):
                raise BindingError("constraints must be AccountConstraint values")
            if c.account in seen:
                raise BindingError(f"duplicate constraint on {c.account}")
            seen.add(c.account)
        object.__setattr__(self, "constraints", tuple(self.constraints))

    def with_plan(self, plan: SourceOperationPlan) -> "BoundExecutionSpec":
        """Derive a NEW spec with a different plan. The original stays frozen."""
        return replace(self, plan=plan)

    def as_dict(self) -> dict[str, Any]:
        return {
            "binding_implementation": BINDING_IMPLEMENTATION_ID,
            "source_entry_key": self.source_entry_key,
            "source_format": self.source_format,
            "expected_sha256": self.expected_sha256,
            "plan": self.plan.as_dict(),
            "route_pass": {
                "expected": self.route_pass.expected,
                "expected_status": self.route_pass.expected_status,
                "maximum": self.route_pass.maximum,
                "token": self.route_pass.token,
                "account": "full_route_passes",
                "distinct_from": list(LOWER_LAYER_ACCOUNTS),
            },
            "constraints": [c.as_dict() for c in self.constraints],
            "authority_note": self.authority_note,
            "expectation_vs_observation_law": "EXPECTED/FLOOR/MAXIMUM are supplied by the caller; OBSERVED is produced only by the run and is never a spec field",
        }


@dataclass(frozen=True)
class BoundExecutionOutcome:
    """What one bound execution produced. OBSERVED lives here and nowhere else."""

    source_entry_key: str
    completed_pass: bool
    full_route_passes_observed: int
    full_route_passes_expected: int | None
    full_route_passes_expected_status: str
    full_route_passes_max: int | None
    plan_identity: Mapping[str, Any]
    observed_accounts: Mapping[str, int]
    constraint_report: tuple[Mapping[str, Any], ...]
    session_receipt: Mapping[str, Any] | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_entry_key": self.source_entry_key,
            "full_route_passes": {
                "observed": self.full_route_passes_observed,
                "expected": self.full_route_passes_expected,
                "expected_status": self.full_route_passes_expected_status,
                "maximum": self.full_route_passes_max,
                "completed_successfully": self.completed_pass,
                "distinct_from": list(LOWER_LAYER_ACCOUNTS),
            },
            "plan_identity": dict(self.plan_identity),
            "observed_accounts": dict(self.observed_accounts),
            "constraint_report": [dict(c) for c in self.constraint_report],
            "session_receipt": self.session_receipt,
        }


class BoundSourceExecution:
    """Owns exactly one GovernedSourceSession for one bound specification.

    Creates the session once. There is no second session for the same bound
    execution, no plan or budget swap after binding, and no raw-path fallback.
    """

    def __init__(self, spec: BoundExecutionSpec, *, pyreadstat_module: Any | None = None) -> None:
        if not isinstance(spec, BoundExecutionSpec):
            raise BindingError("BoundSourceExecution requires a BoundExecutionSpec")
        self.spec = spec
        self._session: GovernedSourceSession | None = None
        self._closed = False
        self._passes_completed = 0
        self._pass_attempted = False

    # -- lifecycle -----------------------------------------------------------
    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def session(self) -> GovernedSourceSession:
        if self._session is None:
            raise SourceAccessViolation("SESSION_NOT_OPEN", "this bound execution has no open session")
        return self._session

    def __enter__(self) -> "BoundSourceExecution":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def close(self) -> None:
        """Deterministic close of the one session this execution owns."""
        if self._closed:
            return
        self._closed = True
        if self._session is not None:
            self._session.close()
            self._session = None

    # -- the one session -----------------------------------------------------
    def _ensure_session(self) -> GovernedSourceSession:
        if self._closed:
            raise SourceAccessViolation("BOUND_EXECUTION_CLOSED", "this bound execution is closed")
        if self._session is None:
            self._session = GovernedSourceSession(
                source_entry_key=self.spec.source_entry_key,
                path=self.spec.path,
                expected_source_sha256=self.spec.expected_sha256,
                source_format=self.spec.source_format,
                budget=self.spec.budget,
                pyreadstat_module=None,
            )
        return self._session

    # -- pre-operation gate on the OUTER account ------------------------------
    def _gate_route_pass(self) -> None:
        """Refuse a second pass BEFORE any second source operation.

        Runs before the session performs identity, metadata or row work, so a
        refusal leaves every lower-layer account exactly where it was.
        """
        if not self.spec.route_pass.admits(self._passes_completed):
            raise SourceAccessViolation(
                ROUTE_PASS_LIMIT_REACHED,
                f"full_route_passes maximum of {self.spec.route_pass.maximum} already reached "
                f"({self._passes_completed} completed); no second source operation was performed",
                self._observed_snapshot(),
            )

    def _observed_snapshot(self) -> dict[str, int]:
        if self._session is None:
            return {}
        return self._session.account_dict()

    # -- post-operation constraint check --------------------------------------
    def _check_constraints(self, observed: Mapping[str, int]) -> tuple[Mapping[str, Any], ...]:
        report: list[Mapping[str, Any]] = []
        failures: list[str] = []
        for c in self.spec.constraints:
            got = int(observed.get(c.account, 0))
            ok = c.satisfied_by(got)
            report.append(c.as_dict(observed=got))
            if not ok:
                failures.append(f"{c.account} observed {got} does not satisfy {c.kind.value} {c.value}"
                                f" ({c.authority.value})")
        if failures:
            raise SourceAccessViolation(
                POST_EXECUTION_CONSTRAINT_FAILED,
                "successful execution returned with a bound constraint unsatisfied: " + "; ".join(failures),
                dict(observed),
            )
        return tuple(report)

    # -- the bound execution -------------------------------------------------
    def execute(self) -> BoundExecutionOutcome:
        """Run the bound plan once, under the outer route-pass account."""
        if self._closed:
            raise SourceAccessViolation("BOUND_EXECUTION_CLOSED", "this bound execution is closed")

        # PRE-OPERATION: outer gate first, so a refusal costs no source operation.
        self._gate_route_pass()
        self._pass_attempted = True

        session = self._ensure_session()
        outcome = session.run(self.spec.plan)

        # A pass counts ONLY on success. A failed attempt leaves the count at 0,
        # so a failed first attempt can never be reported as a completed pass.
        self._passes_completed += 1
        observed = session.account_dict()

        # POST-OPERATION: caller-supplied exact/floor constraints must hold.
        report = self._check_constraints(observed)

        # The outer EXACT expectation is checked here, and remains distinct from
        # the observed lower-layer accounts.
        rp = self.spec.route_pass
        if rp.expected is not None and self._passes_completed != rp.expected:
            raise SourceAccessViolation(
                POST_EXECUTION_CONSTRAINT_FAILED,
                f"full_route_passes observed {self._passes_completed} does not satisfy EXACT {rp.expected}",
                dict(observed),
            )

        return BoundExecutionOutcome(
            source_entry_key=self.spec.source_entry_key,
            completed_pass=True,
            full_route_passes_observed=self._passes_completed,
            full_route_passes_expected=rp.expected,
            full_route_passes_expected_status=rp.expected_status,
            full_route_passes_max=rp.maximum,
            plan_identity=self.spec.plan.as_dict(),
            observed_accounts=dict(observed),
            constraint_report=report,
            session_receipt=session.aggregate_receipt(),
        )
