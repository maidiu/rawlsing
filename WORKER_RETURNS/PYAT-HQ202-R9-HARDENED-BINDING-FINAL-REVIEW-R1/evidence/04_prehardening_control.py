"""HQ202 control: reproduce the four HQ-bound defects at the PRE-hardening candidate.

Run with PYTHONPATH pointing at a git-archive snapshot of
35ffa48204672e6c7180cd010a7c1adde9f18cd7 (the pre-hardening candidate), so this
script imports the PRE-hardening modules while the real review target stays at
deea4054. Nothing here is a worktree and nothing is cloned; it is a read-only
tree extraction used once as a discriminating control.

Purpose: prove the four defects were REAL and that the hardened candidate's
repairs are not cosmetic. If this control did not fail, the hardened review would
have no baseline.

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
    ROUTE_PASS_LIMIT_REACHED,
    RoutePassSpec,
)
from rawlsing_next.pre553_source_access_broker import (
    SourceAccessBudget,
    SourceAccessViolation,
)
from rawlsing_next.pre553_source_session import RowDataMode, SourceOperationPlan

FROZEN = AuthorityLabel.FROZEN_AUTHORITY
WORK = Path(tempfile.mkdtemp(prefix="hq202-prehard-"))
OUT: dict = {}


def sav(name):
    p = WORK / name
    pyreadstat.write_sav(pd.DataFrame({"Q10B": [float(i) for i in range(40)],
                                       "Q101": [float(i * 2) for i in range(40)]}), str(p))
    return str(p)


def catch(fn):
    try:
        return None, fn()
    except SourceAccessViolation as exc:
        return exc, None


# ---------------------------------------------------------------- defect A
# There is no caller-bound applicability at all, and an outer MAX 0 blocks the
# underlying source work of a metadata-only, non-route execution.
def defect_a():
    module = Path(__import__("rawlsing_next.pre553_execution_binding",
                             fromlist=["x"]).__file__).read_text()
    has_enum = "RoutePassApplicability" in module
    built = BoundExecutionSpec(
        source_entry_key="PRE-A", path=sav("pre_a.sav"), source_format="sav",
        plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0),
        budget=SourceAccessBudget(retries=0),
        route_pass=RoutePassSpec(expected=0, maximum=0))
    has_field = hasattr(built, "route_applicability")
    ex = BoundSourceExecution(built)
    try:
        exc, _ = catch(ex.execute)
        return {
            "RoutePassApplicability_exists_at_pre_hardening": has_enum,
            "route_applicability_field_exists": has_field,
            "metadata_only_non_route_with_outer_max0": {
                "refused": exc is not None,
                "code": getattr(exc, "code", None),
                "message": str(exc)[:150] if exc else None,
            },
            "defect_present": (not has_enum) and (not has_field) and exc is not None,
            "defect": "route-pass applicability is inferred from the operation rather than "
                      "bound by the caller; an outer MAX 0 therefore means 'no source "
                      "operation' and blocks admitted metadata work",
        }
    finally:
        ex.close()


# ---------------------------------------------------------------- defect B
# No retry model exists: the retry ceiling is never consulted, so with
# SourceAccessBudget.retries = 0 a second attempt after a failed first attempt is
# still admitted and still performs source work.
def defect_b():
    ex = BoundSourceExecution(BoundExecutionSpec(
        source_entry_key="PRE-B", path=sav("pre_b.sav"), source_format="sav",
        plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0),
        budget=SourceAccessBudget(retries=0),
        route_pass=RoutePassSpec(expected=None, maximum=None),
        constraints=(AccountConstraint("metadata_reads", CountKind.EXACT, 99, FROZEN),)))
    try:
        first, _ = catch(ex.execute)
        reads_after_first = ex.session.account_dict()["metadata_reads"]
        second, second_outcome = catch(ex.execute)
        reads_after_second = ex.session.account_dict()["metadata_reads"]
        module = Path(__import__("rawlsing_next.pre553_execution_binding",
                                 fromlist=["x"]).__file__).read_text()
        admitted = reads_after_second > reads_after_first
        return {
            "first_attempt_code": getattr(first, "code", None),
            "second_attempt_reached_source_work": admitted,
            "second_attempt_code_if_any": getattr(second, "code", None),
            "metadata_reads_after_first": reads_after_first,
            "metadata_reads_after_second": reads_after_second,
            "record_retry_referenced_in_module": "record_retry" in module,
            "retries_observed_property_exists": hasattr(ex, "retries_observed"),
            "route_pass_attempts_property_exists": hasattr(ex, "route_pass_attempts"),
            "completed_route_passes_property_exists": hasattr(ex, "completed_route_passes"),
            "retry_ceiling_consulted": False,
            "defect_present": admitted,
            "defect": "with SourceAccessBudget.retries = 0, a second attempt after a failed "
                      "first attempt still reaches real source work (metadata_reads 1 -> 2); "
                      "the retry ceiling is never consulted and there is no "
                      "attempts/retries/completions separation at all",
        }
    finally:
        ex.close()


# ---------------------------------------------------------------- defect C
# The completed count is incremented BEFORE the postconditions and the outer rule,
# so both leak a completion.
def defect_c():
    results = {}
    # C1: source success + lower-layer postcondition failure
    ex1 = BoundSourceExecution(BoundExecutionSpec(
        source_entry_key="PRE-C1", path=sav("pre_c1.sav"), source_format="sav",
        plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0),
        budget=SourceAccessBudget(retries=0),
        route_pass=RoutePassSpec(expected=1, maximum=1),
        constraints=(AccountConstraint("metadata_reads", CountKind.EXACT, 99, FROZEN),)))
    try:
        first, _ = catch(ex1.execute)
        leaked, _ = catch(ex1.execute)
        results["lower_layer_postcondition_failure"] = {
            "first_code": getattr(first, "code", None),
            "second_code": getattr(leaked, "code", None),
            "second_message": str(leaked)[:160] if leaked else None,
            "completion_leaked": leaked is not None and leaked.code == ROUTE_PASS_LIMIT_REACHED,
        }
    finally:
        ex1.close()
    # C2: source success + outer exact failure. The failed first attempt already
    # incremented the count, so the SECOND attempt reaches the outer EXACT 2 with
    # an observed 2 even though only one attempt ever satisfied everything.
    ex2 = BoundSourceExecution(BoundExecutionSpec(
        source_entry_key="PRE-C2", path=sav("pre_c2.sav"), source_format="sav",
        plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0),
        budget=SourceAccessBudget(retries=0),
        route_pass=RoutePassSpec(expected=2, maximum=3)))
    try:
        first, _ = catch(ex2.execute)
        leaked, second_outcome = catch(ex2.execute)
        results["outer_exact_failure"] = {
            "first_code": getattr(first, "code", None),
            "second_code": getattr(leaked, "code", None),
            "second_outer_observed": (second_outcome.full_route_passes_observed
                                      if second_outcome is not None else None),
            "attempts_that_satisfied_everything": 1,
            "phantom_completion_admitted_into_the_outer_account":
                second_outcome is not None
                and second_outcome.full_route_passes_observed == 2,
        }
    finally:
        ex2.close()
    present = (results["lower_layer_postcondition_failure"]["completion_leaked"]
               and results["outer_exact_failure"]
               ["phantom_completion_admitted_into_the_outer_account"])
    return {**results,
            "defect_present": present,
            "defect": "the completed counter is incremented before the lower-layer "
                      "constraints and before the outer EXACT rule, so a failed attempt still "
                      "leaves a counted pass behind. With an unbounded-within-maximum outer "
                      "EXACT, the phantom completion is even admitted into the outer account: "
                      "attempt 2 reports observed 2 although only one attempt satisfied "
                      "everything"}


# ---------------------------------------------------------------- defect D
# The pyreadstat_module argument is accepted and then discarded.
def defect_d():
    class Stub:
        __version__ = "1.3.6"
        consulted = 0

        def read_sav(self, *a, **k):
            Stub.consulted += 1
            raise AssertionError("the supplied stub was consulted")

        def read_dta(self, *a, **k):
            Stub.consulted += 1
            raise AssertionError("the supplied stub was consulted")

    stub = Stub()
    ex = BoundSourceExecution(
        BoundExecutionSpec(
            source_entry_key="PRE-D", path=sav("pre_d.sav"), source_format="sav",
            plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0),
            budget=SourceAccessBudget(retries=0), route_pass=RoutePassSpec()),
        pyreadstat_module=stub)
    try:
        ex.execute()                      # succeeds using the REAL module
        broker_module = ex.session.broker.pyreadstat
        return {
            "execution_stores_the_supplied_module": hasattr(ex, "_pyreadstat_module"),
            "broker_module_is_the_supplied_stub": broker_module is stub,
            "broker_module_is_the_real_pyreadstat": broker_module is pyreadstat,
            "stub_consultations": Stub.consulted,
            "defect_present": broker_module is not stub,
            "defect": "BoundSourceExecution accepts pyreadstat_module and then passes None to "
                      "the session, so a supplied dependency is silently discarded",
        }
    finally:
        ex.close()


def main() -> int:
    doc = {
        "schema": "HQ202_PREHARDENING_CONTROL@1.0.0",
        "pre_hardening_candidate": "35ffa48204672e6c7180cd010a7c1adde9f18cd7",
        "hardened_review_target": "deea40541cda0627d129dcb7d30e06e0682e0fed",
        "control_method": "git archive of the rawlsing_next subtree at the pre-hardening "
                          "commit, imported instead of the review target; no clone, no worktree",
        "defects": {
            "A_route_pass_applicability": defect_a(),
            "B_retry_zero_second_attempt": defect_b(),
            "C_completion_before_postconditions": defect_c(),
            "D_discarded_dependency_injection": defect_d(),
        },
    }
    doc["defects_all_reproduced"] = all(
        d.get("defect_present") for d in doc["defects"].values())
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
