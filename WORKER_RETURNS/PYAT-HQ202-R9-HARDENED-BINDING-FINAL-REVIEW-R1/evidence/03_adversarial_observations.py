"""HQ202 residual adversarial observations.

Three questions I could not settle from the commission text alone, probed
directly against the hardened candidate. These are recorded as OBSERVATIONS with
a measured severity, not as defects, because each one is either unreachable from
the accepted warrant or is a property the commission already places outside the
in-process grain.

  OBS-1  EXACT outer expectations are post-operation postconditions, while only
         MAXIMUM is a pre-operation gate. A bound spec whose EXACT expectation is
         smaller than the number of admitted passes (with an unbounded or larger
         maximum) therefore performs source work and only then refuses.
  OBS-2  A constraint naming an account the runtime does not have is not refused
         at bind time; MAXIMUM and EXACT-0 on an unknown account are vacuously
         satisfied.
  OBS-3  BoundSourceExecution.session is a public accessor, so a caller holding
         the execution can drive session.run() directly and bypass the outer
         gate. Recorded to bound the claim: enforcement is an in-process
         convention, not a sandbox.

Prints one JSON document on stdout.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pyreadstat

from rawlsing_next.pre553_execution_binding import (
    AccountConstraint,
    AuthorityLabel,
    BoundExecutionSpec,
    BoundSourceExecution,
    BindingError,
    CountKind,
    POST_EXECUTION_CONSTRAINT_FAILED,
    RoutePassApplicability,
    RoutePassSpec,
)
from rawlsing_next.pre553_source_access_broker import (
    SourceAccessBudget,
    SourceAccessViolation,
)
from rawlsing_next.pre553_source_session import RowDataMode, SourceOperationPlan

FROZEN = AuthorityLabel.FROZEN_AUTHORITY
APPLICABLE = RoutePassApplicability.APPLICABLE
NOT_APPLICABLE = RoutePassApplicability.NOT_APPLICABLE

WORK = Path(tempfile.mkdtemp(prefix="hq202-adversarial-"))


def dta(name):
    p = WORK / name
    pyreadstat.write_dta(pd.DataFrame({"Q10B": [float(i) for i in range(40)]}), str(p))
    return str(p)


def sav(name):
    p = WORK / name
    pyreadstat.write_sav(pd.DataFrame({"Q10B": [float(i) for i in range(40)]}), str(p))
    return str(p)


def obs1():
    """APPLICABLE + EXACT 0 performs source work, then refuses."""
    ex = BoundSourceExecution(BoundExecutionSpec(
        source_entry_key="OBS1", path=dta("obs1.dta"), source_format="dta",
        plan=SourceOperationPlan(mode=RowDataMode.FULL, max_retries=0),
        budget=SourceAccessBudget(retries=0),
        route_pass=RoutePassSpec(expected=0, maximum=None),
        route_applicability=APPLICABLE))
    try:
        code = None
        try:
            ex.execute()
        except SourceAccessViolation as exc:
            code = exc.code
        accounts = ex.session.account_dict()
        return {
            "bound_expected": 0, "bound_maximum": None,
            "refusal_code": code,
            "refusal_reached_post_operation": code == POST_EXECUTION_CONSTRAINT_FAILED,
            "source_work_performed_before_refusal": accounts["full_reads"] == 1,
            "full_reads_observed": accounts["full_reads"],
            "completed_route_passes": ex.completed_route_passes,
            "severity": "ADVISORY — unreachable from the seven-source warrant, which always "
                        "binds SRC27 expected 1 together with maximum 1; and NOT_APPLICABLE + "
                        "EXACT 1 is still refused at bind. Only a hand-written mis-binding "
                        "reaches it, and it still refuses without counting a pass.",
        }
    finally:
        ex.close()


def obs1b():
    """Same class, reached by a second admitted pass rather than by EXACT 0."""
    ex = BoundSourceExecution(BoundExecutionSpec(
        source_entry_key="OBS1B", path=dta("obs1b.dta"), source_format="dta",
        plan=SourceOperationPlan(mode=RowDataMode.FULL, max_retries=1),
        budget=SourceAccessBudget(retries=1),
        route_pass=RoutePassSpec(expected=1, maximum=None),
        route_applicability=APPLICABLE))
    try:
        first = ex.execute()
        code = None
        try:
            ex.execute()
        except SourceAccessViolation as exc:
            code = exc.code
        accounts = ex.session.account_dict()
        return {"first_outer_observed": first.full_route_passes_observed,
                "second_refusal_code": code,
                "full_reads_after_two_attempts": accounts["full_reads"],
                "completed_route_passes": ex.completed_route_passes,
                "severity": "ADVISORY — bound maximum is UNBOUND here; the warrant binds "
                            "expected 1 with maximum 1, where the MAXIMUM gate refuses "
                            "pre-operation (proved in W2)."}
    finally:
        ex.close()


def obs2():
    """A constraint on an account the runtime does not have is not refused at bind."""
    results = {}
    for kind, value in ((CountKind.MAXIMUM, 0), (CountKind.EXACT, 0), (CountKind.FLOOR, 1)):
        built = refused = None
        try:
            built = BoundExecutionSpec(
                source_entry_key="OBS2", path=sav("obs2.sav"), source_format="sav",
                plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0),
                budget=SourceAccessBudget(retries=0), route_pass=RoutePassSpec(),
                route_applicability=NOT_APPLICABLE,
                constraints=(AccountConstraint("not_a_runtime_account", kind, value, FROZEN),))
        except BindingError as exc:
            refused = str(exc)
        if built is None:
            results[f"{kind.value}_{value}"] = {"refused_at_bind": True, "message": refused}
            continue
        ex = BoundSourceExecution(built)
        try:
            try:
                out = ex.execute()
                results[f"{kind.value}_{value}"] = {
                    "refused_at_bind": False,
                    "vacuous": True,
                    "reported_observed": out.constraint_report[0]["observed"],
                    "reported_satisfied": out.constraint_report[0]["satisfied"]}
            except SourceAccessViolation as exc:
                results[f"{kind.value}_{value}"] = {
                    "refused_at_bind": False, "failed_post_operation": True,
                    "code": exc.code}
        finally:
            ex.close()
    return {"unknown_account": "not_a_runtime_account", "outcomes": results,
            "severity": "ADVISORY — a typo'd MAXIMUM or EXACT-0 constraint is vacuously "
                        "satisfied because a missing account reads as observed 0. FLOOR and "
                        "non-zero EXACT fail closed. No warrant-derived constraint depends on "
                        "an unknown account, so the seven-source binding is unaffected."}


def obs3():
    """The public session accessor lets a holder bypass the outer gate."""
    ex = BoundSourceExecution(BoundExecutionSpec(
        source_entry_key="OBS3", path=dta("obs3.dta"), source_format="dta",
        plan=SourceOperationPlan(mode=RowDataMode.FULL, max_retries=0),
        budget=SourceAccessBudget(retries=0),
        route_pass=RoutePassSpec(expected=1, maximum=1),
        route_applicability=APPLICABLE))
    try:
        out1 = ex.execute()
        gate_code = None
        try:
            ex.execute()
        except SourceAccessViolation as exc:
            gate_code = exc.code
        # Direct session drive, bypassing execute() and therefore the outer gate.
        ex.session.run(SourceOperationPlan(mode=RowDataMode.FULL, max_retries=0))
        accounts = ex.session.account_dict()
        return {"outer_gate_refusal_code": gate_code,
                "outer_observed_via_execute": out1.full_route_passes_observed,
                "full_reads_after_direct_session_run": accounts["full_reads"],
                "outer_count_unchanged_by_direct_run": ex.completed_route_passes == 1,
                "severity": "OUT OF GRAIN — the commission directs the review to drive the "
                            "public execute() path, and an in-process owner cannot sandbox a "
                            "caller that reaches _completed or the broker directly. Recorded "
                            "only to bound the claim: the binding is a governed entry point, "
                            "not an isolated interpreter."}
    finally:
        ex.close()


def main() -> int:
    out = {
        "schema": "HQ202_RESIDUAL_ADVERSARIAL_OBSERVATIONS@1.0.0",
        "purpose": "bound the claim and disclose the residual, non-material edges",
        "observations": {
            "OBS-1": obs1(),
            "OBS-1B": obs1b(),
            "OBS-2": obs2(),
            "OBS-3": obs3(),
        },
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
