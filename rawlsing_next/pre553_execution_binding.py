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
or ``path_opens``, and it never substitutes for any of them. Three properties
matter:

  * APPLICABILITY is bound EXPLICITLY by the caller. It is never inferred from a
    source key, a file name, or from plan mode, because a FULL decode is not
    automatically a Route-B pass. A NOT_APPLICABLE execution still performs its
    metadata/selected/full work normally and simply reports an outer count of 0;
    a route-pass maximum of 0 there means "not a route pass", never "no source
    operation".
  * COMPLETION is ordered last. A pass is completed only after the source
    operation AND every caller-supplied exact/floor postcondition AND the outer
    expected rule have all succeeded. The prospective count is validated before
    it is committed, so a failed postcondition cannot leave a completed pass.
  * ATTEMPTS, RETRIES and COMPLETIONS are three different counters. An attempt
    counts admissions, retries is the lower-layer account, and completed passes
    counts postcondition-satisfying attempts. None is substituted for another.

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
    "RoutePassApplicability",
    "AccountConstraint",
    "RoutePassSpec",
    "BoundExecutionSpec",
    "BoundExecutionOutcome",
    "BoundSourceExecution",
    "BindingError",
    "POST_EXECUTION_CONSTRAINT_FAILED",
    "ROUTE_PASS_LIMIT_REACHED",
    "RETRY_LIMIT_REACHED",
    "RETRY_BINDING_MISMATCH",
    "LOWER_LAYER_ACCOUNTS",
    "RETRY_BINDING_LAW",
]

BINDING_IMPLEMENTATION_ID = "rawlsing_next/pre553_execution_binding.py"
POST_EXECUTION_CONSTRAINT_FAILED = "POST_EXECUTION_CONSTRAINT_FAILED"
ROUTE_PASS_LIMIT_REACHED = "ROUTE_PASS_LIMIT_REACHED"
RETRY_LIMIT_REACHED = "RETRY_LIMIT_REACHED"
RETRY_BINDING_MISMATCH = "RETRY_BINDING_MISMATCH"

# ONE exact retry binding law. There is a single owner of the retry count and a
# single ceiling, and a bound execution REFUSES to exist if the two historical
# knobs disagree. Divergent silent controls are not representable.
#
#   owner   : SourceAccessAccount.retries, incremented by the broker
#   ceiling : SourceAccessBudget.retries
#   plan    : SourceOperationPlan.max_retries must EQUAL that ceiling
#
# An unbounded (None) retry ceiling is not admissible here: a governed bound
# execution needs a decidable retry law.
RETRY_BINDING_LAW = (
    "SourceAccessBudget.retries is the single retry ceiling and "
    "SourceAccessAccount.retries is the single retry count; "
    "SourceOperationPlan.max_retries must equal the ceiling exactly, "
    "and an unbounded (None) ceiling is refused. Mismatch fails closed at bind time."
)

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


class RoutePassApplicability(str, Enum):
    """Whether the OUTER full-route-pass account applies to this bound execution.

    This is bound EXPLICITLY by the caller. It is never inferred from a source
    key, a source entry, or a file name, and it is not derived from plan mode:
    a FULL decode is not automatically a Route-B pass, because that would make
    applicability a function of the operation rather than of the authority.

    NOT_APPLICABLE
        No outer route pass exists. The underlying metadata/selected/full work
        still executes normally, and the outer observed count is 0. A
        route-pass maximum of 0 here means "this is not a route pass", NOT
        "perform no source operation".
    APPLICABLE
        The outer governed Route-B pass account is active. Expected and maximum
        are enforced separately from every lower-layer account.
    """

    NOT_APPLICABLE = "NOT_APPLICABLE"
    APPLICABLE = "APPLICABLE"


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
    ceiling. They are distinct fields and are reported distinctly. These values
    are inert unless the bound spec declares the pass APPLICABLE.
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
        """Pre-operation gate, consulted ONLY for an APPLICABLE pass."""
        if self.maximum is not None and completed_so_far >= self.maximum:
            return False
        return True

    def admits_expected_zero(self) -> bool:
        """An EXACT 0 outer expectation is satisfiable only by zero passes."""
        return self.expected is None or self.expected == 0


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
    # Repair 1: explicit, caller-bound, immutable. Defaults to NOT_APPLICABLE so
    # no execution can acquire a route pass without the caller asking for one.
    route_applicability: RoutePassApplicability = RoutePassApplicability.NOT_APPLICABLE
    constraints: tuple[AccountConstraint, ...] = ()
    authority_note: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_entry_key, str) or not self.source_entry_key.strip():
            raise BindingError("source_entry_key must be a non-empty string")
        if not isinstance(self.plan, SourceOperationPlan):
            raise BindingError("plan must be a SourceOperationPlan")
        if not isinstance(self.route_pass, RoutePassSpec):
            raise BindingError("route_pass must be a RoutePassSpec")
        if not isinstance(self.route_applicability, RoutePassApplicability):
            raise BindingError("route_applicability must be a RoutePassApplicability")
        seen = set()
        for c in self.constraints:
            if not isinstance(c, AccountConstraint):
                raise BindingError("constraints must be AccountConstraint values")
            if c.account in seen:
                raise BindingError(f"duplicate constraint on {c.account}")
            seen.add(c.account)
        object.__setattr__(self, "constraints", tuple(self.constraints))
        self._enforce_retry_binding_law()
        self._enforce_applicability_coherence()

    # -- Repair 1: applicability coherence -----------------------------------
    def _enforce_applicability_coherence(self) -> None:
        """Refuse an incoherent applicability/expectation pair at bind time.

        A NOT_APPLICABLE execution can never produce an outer pass, so its frozen
        outer expectation can only be zero or absent. Binding EXACT 1 to a
        non-route spec is a contradiction, and is refused BEFORE any access.
        """
        if self.route_applicability is RoutePassApplicability.NOT_APPLICABLE:
            if not self.route_pass.admits_expected_zero():
                raise BindingError(
                    f"a NOT_APPLICABLE route pass cannot satisfy EXACT {self.route_pass.expected}; "
                    "bind RoutePassApplicability.APPLICABLE if an outer pass is authorised")

    # -- Repair 2: one exact retry binding law -------------------------------
    def _enforce_retry_binding_law(self) -> None:
        """Refuse to exist if the two historical retry knobs can disagree.

        ``SourceAccessBudget.retries`` is the ceiling and
        ``SourceOperationPlan.max_retries`` must equal it exactly. An unbounded
        ceiling is refused so the retry law is always decidable. This makes a
        divergent silent control unrepresentable rather than merely discouraged.
        """
        ceiling = self.budget.retries
        if ceiling is None:
            raise BindingError(
                f"{RETRY_BINDING_MISMATCH}: SourceAccessBudget.retries is unbounded; "
                "a governed bound execution requires a decidable retry ceiling")
        plan_retries = self.plan.max_retries
        if plan_retries != ceiling:
            raise BindingError(
                f"{RETRY_BINDING_MISMATCH}: SourceOperationPlan.max_retries={plan_retries} "
                f"disagrees with SourceAccessBudget.retries={ceiling}; one exact binding law "
                "requires them equal")

    @property
    def retry_ceiling(self) -> int:
        """The single retry ceiling, owned by the budget."""
        return int(self.budget.retries or 0)

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
            "route_pass_applicability": self.route_applicability.value,
            "route_applicability_is_explicitly_bound": True,
            "route_applicability_inferred_from_source_key": False,
            "route_pass": {
                "expected": self.route_pass.expected,
                "expected_status": self.route_pass.expected_status,
                "maximum": self.route_pass.maximum,
                "token": self.route_pass.token,
                "account": "full_route_passes",
                "distinct_from": list(LOWER_LAYER_ACCOUNTS),
                "active": self.route_applicability is RoutePassApplicability.APPLICABLE,
                "maximum_zero_means": ("no route pass is performed; underlying source work still executes"
                                       if self.route_applicability is RoutePassApplicability.NOT_APPLICABLE
                                       else "a route pass is refused pre-operation"),
            },
            "retry_binding_law": {
                "law": RETRY_BINDING_LAW,
                "single_count_owner": "SourceAccessAccount.retries",
                "single_ceiling": "SourceAccessBudget.retries",
                "plan_knob": "SourceOperationPlan.max_retries",
                "plan_knob_value": self.plan.max_retries,
                "ceiling_value": self.retry_ceiling,
                "agree": True,
            },
            "constraints": [c.as_dict() for c in self.constraints],
            "authority_note": self.authority_note,
            "expectation_vs_observation_law": "EXPECTED/FLOOR/MAXIMUM are supplied by the caller; OBSERVED is produced only by the run and is never a spec field",
        }


@dataclass(frozen=True)
class BoundExecutionOutcome:
    """What one bound execution produced. OBSERVED lives here and nowhere else.

    The three outer counters are kept separate and are never interchanged:

        route_pass_attempts      every admitted wrapper attempt
        retries                  the lower-layer retry account (SourceAccessAccount.retries)
        completed_route_passes   attempts that passed EVERY postcondition

    ``completed_route_passes`` is not an attempt counter, and ``route_pass_attempts``
    is not a completion counter.
    """

    source_entry_key: str
    route_pass_applicable: bool
    route_pass_status: str
    completed_pass: bool
    full_route_passes_observed: int
    full_route_passes_expected: int | None
    full_route_passes_expected_status: str
    full_route_passes_max: int | None
    route_pass_attempts: int
    retries_observed: int
    completed_route_passes: int
    plan_identity: Mapping[str, Any]
    observed_accounts: Mapping[str, int]
    constraint_report: tuple[Mapping[str, Any], ...]
    session_receipt: Mapping[str, Any] | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_entry_key": self.source_entry_key,
            # Commission-named flat receipt fields, exposed verbatim.
            "full_route_passes_observed": self.full_route_passes_observed,
            "full_route_passes_max": self.full_route_passes_max,
            "full_route_passes_expected": self.full_route_passes_expected,
            "full_route_passes_expected_status": self.full_route_passes_expected_status,
            "full_route_passes_completed_successfully": self.completed_pass,
            "route_pass_applicability": "APPLICABLE" if self.route_pass_applicable else "NOT_APPLICABLE",
            "route_pass_status": self.route_pass_status,
            "outer_counters_kept_separate": {
                "route_pass_attempts": self.route_pass_attempts,
                "retries": self.retries_observed,
                "completed_route_passes": self.completed_route_passes,
            },
            "plan_identity": dict(self.plan_identity),
            "full_route_passes": {
                "observed": self.full_route_passes_observed,
                "expected": self.full_route_passes_expected,
                "expected_status": self.full_route_passes_expected_status,
                "maximum": self.full_route_passes_max,
                "completed_successfully": self.completed_pass,
                "applicability": "APPLICABLE" if self.route_pass_applicable else "NOT_APPLICABLE",
                "status": self.route_pass_status,
                "distinct_from": list(LOWER_LAYER_ACCOUNTS),
            },
            "observed_accounts": dict(self.observed_accounts),
            "constraint_report": [dict(c) for c in self.constraint_report],
            "session_receipt": self.session_receipt,
        }


class BoundSourceExecution:
    """Owns exactly one GovernedSourceSession for one bound specification.

    Creates the session once. There is no second session for the same bound
    execution, no plan or budget swap after binding, and no raw-path fallback.

    Three outer counters are tracked and never interchanged:

        route_pass_attempts      every ADMITTED wrapper attempt
        retries                  the lower-layer retry account
        completed_route_passes   attempts that passed every postcondition

    A refused pre-operation gate is NOT an attempt: it leaves all three counters
    and every source account unmoved.
    """

    def __init__(self, spec: BoundExecutionSpec, *, pyreadstat_module: Any | None = None) -> None:
        if not isinstance(spec, BoundExecutionSpec):
            raise BindingError("BoundSourceExecution requires a BoundExecutionSpec")
        self.spec = spec
        # Repair 4: the injected module is STORED and PASSED THROUGH, never
        # discarded. None means "the session resolves the real pyreadstat".
        self._pyreadstat_module = pyreadstat_module
        self._session: GovernedSourceSession | None = None
        self._closed = False
        self._attempts = 0
        self._completed = 0

    # -- lifecycle -----------------------------------------------------------
    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def pyreadstat_module(self) -> Any | None:
        """The exact module handed to this execution, or None for the real one."""
        return self._pyreadstat_module

    @property
    def session(self) -> GovernedSourceSession:
        if self._session is None:
            raise SourceAccessViolation("SESSION_NOT_OPEN", "this bound execution has no open session")
        return self._session

    @property
    def route_pass_attempts(self) -> int:
        """Admitted wrapper attempts. Not a completion counter."""
        return self._attempts

    @property
    def completed_route_passes(self) -> int:
        """Attempts that satisfied every postcondition. Not an attempt counter."""
        return self._completed

    @property
    def retries_observed(self) -> int:
        """The lower-layer retry account, read from the owned session."""
        return int(self._observed_snapshot().get("retries", 0))

    def counters(self) -> dict[str, int]:
        return {
            "route_pass_attempts": self._attempts,
            "retries": self.retries_observed,
            "completed_route_passes": self._completed,
        }

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
                # Repair 4: the exact supplied module reaches the session.
                pyreadstat_module=self._pyreadstat_module,
            )
        return self._session

    def _observed_snapshot(self) -> dict[str, int]:
        if self._session is None:
            return {}
        return self._session.account_dict()

    # -- Repair 1: pre-operation applicability gate --------------------------
    def _gate_route_pass(self) -> None:
        """Enforce the outer pass ceiling ONLY for an APPLICABLE pass.

        For a NOT_APPLICABLE execution this gate is inert. A route-pass maximum
        of 0 means "this is not a route pass", and must never be read as
        "perform no source operation": the underlying metadata/selected/full
        work still executes normally.
        """
        if self.spec.route_applicability is not RoutePassApplicability.APPLICABLE:
            return
        if not self.spec.route_pass.admits(self._completed):
            raise SourceAccessViolation(
                ROUTE_PASS_LIMIT_REACHED,
                f"full_route_passes maximum of {self.spec.route_pass.maximum} already reached "
                f"({self._completed} completed); no second source operation was performed",
                self._observed_snapshot(),
            )

    # -- Repair 2: pre-operation retry gate ----------------------------------
    def _admit_attempt(self) -> None:
        """Admit one wrapper attempt, applying the single retry binding law.

        The FIRST attempt is not a retry. Every additional admitted attempt must
        first pass the retry ceiling and MUST increment the existing lower-layer
        retries account under that same ceiling BEFORE any source work. A
        refused retry moves no account at all.
        """
        if self._attempts == 0:
            self._attempts = 1
            return
        ceiling = self.spec.retry_ceiling
        if self._attempts > ceiling:
            raise SourceAccessViolation(
                RETRY_LIMIT_REACHED,
                f"retry {self._attempts} exceeds the bound retry ceiling of {ceiling}; "
                "no source operation was performed",
                self._observed_snapshot(),
            )
        # Increment the real retries account under its own budget ceiling.
        self._ensure_session().broker.record_retry()
        self._attempts += 1

    # -- Repair 3: post-operation postconditions ------------------------------
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

    def _check_outer_rule(self, observed: Mapping[str, int]) -> int:
        """Evaluate the outer expected rule and return the PROSPECTIVE count.

        Returns without mutating anything, so a failure here cannot leave a
        completed pass behind. For a NOT_APPLICABLE execution the prospective
        count is the unchanged completed count, and an EXACT 0 outer expectation
        is satisfied by construction.
        """
        rp = self.spec.route_pass
        if self.spec.route_applicability is not RoutePassApplicability.APPLICABLE:
            if not rp.admits_expected_zero():
                raise SourceAccessViolation(
                    POST_EXECUTION_CONSTRAINT_FAILED,
                    f"non-route execution cannot satisfy full_route_passes EXACT {rp.expected}",
                    dict(observed),
                )
            return self._completed
        prospective = self._completed + 1
        if rp.expected is not None and prospective != rp.expected:
            raise SourceAccessViolation(
                POST_EXECUTION_CONSTRAINT_FAILED,
                f"full_route_passes would reach {prospective}, which does not satisfy EXACT {rp.expected}",
                dict(observed),
            )
        if rp.maximum is not None and prospective > rp.maximum:
            raise SourceAccessViolation(
                POST_EXECUTION_CONSTRAINT_FAILED,
                f"full_route_passes would reach {prospective}, above the maximum of {rp.maximum}",
                dict(observed),
            )
        return prospective

    # -- the bound execution -------------------------------------------------
    def execute(self) -> BoundExecutionOutcome:
        """Run the bound plan once, under the outer route-pass account.

        Ordering is load-bearing: gates, then attempt admission, then source work,
        then lower-layer postconditions, then the outer rule, and only then the
        completion increment.
        """
        if self._closed:
            raise SourceAccessViolation("BOUND_EXECUTION_CLOSED", "this bound execution is closed")

        # PRE-OPERATION, in order: outer applicability ceiling, then retry ceiling.
        # Both run before any identity, hash, metadata or row work.
        self._gate_route_pass()
        self._admit_attempt()

        session = self._ensure_session()
        session.run(self.spec.plan)
        observed = session.account_dict()

        # POST-OPERATION step 1: caller-supplied lower-layer exact/floor rules.
        report = self._check_constraints(observed)
        # POST-OPERATION step 2: the outer expected rule, evaluated prospectively.
        prospective = self._check_outer_rule(observed)
        # POST-OPERATION step 3: only now does a pass become COMPLETED.
        self._completed = prospective

        applicable = self.spec.route_applicability is RoutePassApplicability.APPLICABLE
        rp = self.spec.route_pass
        return BoundExecutionOutcome(
            source_entry_key=self.spec.source_entry_key,
            route_pass_applicable=applicable,
            route_pass_status="COMPLETED" if applicable else "NOT_APPLICABLE",
            completed_pass=applicable,
            full_route_passes_observed=self._completed,
            full_route_passes_expected=rp.expected,
            full_route_passes_expected_status=rp.expected_status,
            full_route_passes_max=rp.maximum,
            route_pass_attempts=self._attempts,
            retries_observed=int(observed.get("retries", 0)),
            completed_route_passes=self._completed,
            plan_identity=self.spec.plan.as_dict(),
            observed_accounts=dict(observed),
            constraint_report=report,
            session_receipt=session.aggregate_receipt(),
        )
