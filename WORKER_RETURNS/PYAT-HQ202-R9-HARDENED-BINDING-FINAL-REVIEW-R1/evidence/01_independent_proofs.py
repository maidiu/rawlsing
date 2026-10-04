"""HQ202 independent proofs, rounds A-D.

Written by the HQ202 reviewer from the commission text alone. It imports ONLY the
public surface of the hardened candidate and drives every execution through the
public ``BoundSourceExecution.execute()``. It does not import or reuse the
candidate's own court file, so a defect the candidate court cannot see is still
reachable here.

Rounds:
    A  route-pass applicability
    B  attempts / retries / completions
    C  completion semantics
    D  dependency injection

Prints one JSON document on stdout. Exit code 0 always; the JSON carries the
verdict per claim so a failing claim is evidence, not a crash.
"""
from __future__ import annotations

import json
import sys
import tempfile
import traceback
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
    LOWER_LAYER_ACCOUNTS,
    POST_EXECUTION_CONSTRAINT_FAILED,
    RETRY_BINDING_MISMATCH,
    RETRY_LIMIT_REACHED,
    ROUTE_PASS_LIMIT_REACHED,
    RoutePassApplicability,
    RoutePassSpec,
)
from rawlsing_next.pre553_source_access_broker import (
    ReaderSeamViolation,
    SourceAccessAccount,
    SourceAccessBudget,
    SourceAccessViolation,
)
from rawlsing_next.pre553_source_session import RowDataMode, SourceOperationPlan

NON_ROUTE = RoutePassApplicability.NOT_APPLICABLE
ROUTE = RoutePassApplicability.APPLICABLE
FROZEN = AuthorityLabel.FROZEN_AUTHORITY
POLICY = AuthorityLabel.IMPLEMENTATION_POLICY
ZERO_OUTER = RoutePassSpec(expected=0, maximum=0)

WORK = Path(tempfile.mkdtemp(prefix="hq202-independent-"))
RESULTS: list[dict] = []


def need(cond: object, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def frame(rows: int = 40) -> pd.DataFrame:
    return pd.DataFrame({
        "Q10B": [float(i) for i in range(rows)],
        "Q101": [float(i * 2) for i in range(rows)],
        "Q2061B": [float(i * 3) for i in range(rows)],
    })


def sav(name: str, rows: int = 40) -> str:
    p = WORK / name
    pyreadstat.write_sav(frame(rows), str(p))
    return str(p)


def dta(name: str, rows: int = 40) -> str:
    p = WORK / name
    pyreadstat.write_dta(frame(rows), str(p))
    return str(p)


def spec(key, path, fmt, plan, *, rp=None, applicable=None, cons=(), budget=None, sha=None):
    kw = {}
    if applicable is not None:
        kw["route_applicability"] = applicable
    return BoundExecutionSpec(
        source_entry_key=key, path=path, source_format=fmt, plan=plan,
        expected_sha256=sha,
        budget=budget if budget is not None else SourceAccessBudget(),
        route_pass=rp if rp is not None else RoutePassSpec(),
        constraints=tuple(cons), **kw)


def plan_of(mode, retries=0, **kw):
    """A plan whose max_retries agrees with the budget, as the binding law requires."""
    return SourceOperationPlan(mode=mode, max_retries=retries, **kw)


def session_or_none(ex):
    try:
        return ex.session
    except SourceAccessViolation:
        return None


def snap(ex):
    s = session_or_none(ex)
    return None if s is None else s.account_dict()


def expect_raise(fn, *types):
    """Run fn and return (exception, None) or (None, None) if it did not raise."""
    try:
        fn()
    except types as exc:  # noqa: B902
        return exc
    except Exception as exc:  # noqa: BLE001
        return ("UNEXPECTED_TYPE", exc)
    return None


def claim(cid: str, title: str, fn) -> None:
    rec = {"id": cid, "title": title}
    try:
        rec["evidence"] = fn() or {}
        rec["ok"] = True
    except Exception as exc:  # noqa: BLE001
        rec["ok"] = False
        rec["error"] = f"{type(exc).__name__}: {exc}"
        rec["traceback"] = traceback.format_exc().splitlines()[-4:]
    RESULTS.append(rec)


# =========================================================== A: APPLICABILITY
def a1():
    """Metadata-only NON-ROUTE with outer EXACT 0 runs and observes outer 0."""
    ex = BoundSourceExecution(spec(
        "NR-META", sav("a1.sav"), "sav",
        SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="BIG5"),
        rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        out = ex.execute()
        need(out.full_route_passes_observed == 0, "outer observed != 0")
        need(out.route_pass_applicable is False, "applicable not False")
        need(out.completed_pass is False, "completed_pass not False")
        need(out.route_pass_status == "NOT_APPLICABLE", "status wrong")
        need(out.observed_accounts["metadata_reads"] == 1, "metadata_reads != 1")
        need(out.observed_accounts["full_reads"] == 0, "full_reads != 0")
        return {"full_route_passes_observed": out.full_route_passes_observed,
                "applicable": out.route_pass_applicable,
                "completed_pass": out.completed_pass,
                "metadata_reads": out.observed_accounts["metadata_reads"],
                "full_reads": out.observed_accounts["full_reads"]}
    finally:
        ex.close()


def a2():
    """Selected NON-ROUTE with outer EXACT 0 runs and observes outer 0."""
    ex = BoundSourceExecution(spec(
        "NR-SEL", sav("a2.sav"), "sav",
        SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q10B",)),
        rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        out = ex.execute()
        need(out.full_route_passes_observed == 0, "outer observed != 0")
        need(out.completed_pass is False, "completed_pass not False")
        need(out.observed_accounts["selected_reads"] == 1, "selected_reads != 1")
        need(out.observed_accounts["full_reads"] == 0, "full_reads != 0")
        return {"full_route_passes_observed": out.full_route_passes_observed,
                "selected_reads": out.observed_accounts["selected_reads"],
                "full_reads": out.observed_accounts["full_reads"],
                "selected_ordinals": list(out.session_receipt["selected_ordinals"].get("NR-SEL", []))}
    finally:
        ex.close()


def a3():
    """A FULL plan can still be NOT_APPLICABLE and observe outer 0."""
    ex = BoundSourceExecution(spec(
        "FULL-NON-ROUTE", dta("a3.dta"), "dta",
        SourceOperationPlan(mode=RowDataMode.FULL, encoding="latin1"),
        rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        out = ex.execute()
        need(out.full_route_passes_observed == 0, "outer observed != 0")
        need(out.route_pass_applicable is False, "applicable not False")
        need(out.observed_accounts["full_reads"] == 1, "full read did not happen")
        return {"full_route_passes_observed": out.full_route_passes_observed,
                "applicable": out.route_pass_applicable,
                "full_reads": out.observed_accounts["full_reads"],
                "plan_mode": out.plan_identity["mode"]}
    finally:
        ex.close()


def a4():
    """APPLICABLE route MAX 0 is refused BEFORE session/source operation."""
    s = spec("ROUTE-MAX0", dta("a4.dta"), "dta",
             SourceOperationPlan(mode=RowDataMode.FULL),
             rp=RoutePassSpec(expected=0, maximum=0), applicable=ROUTE)
    need(s.as_dict()["route_pass"]["maximum_zero_means"].startswith("a route pass is refused"),
         "maximum-zero meaning not typed for APPLICABLE")
    ex = BoundSourceExecution(s)
    try:
        exc = expect_raise(ex.execute, SourceAccessViolation)
        need(exc is not None, "route max0 was NOT refused")
        need(not isinstance(exc, tuple), f"unexpected exception type {exc}")
        need(exc.code == ROUTE_PASS_LIMIT_REACHED, f"wrong code {exc.code}")
        need(session_or_none(ex) is None, "a session WAS created despite the pre-op refusal")
        need(ex.route_pass_attempts == 0, "a refused pre-op gate was counted as an attempt")
        need(ex.completed_route_passes == 0, "completion leaked")
        need(exc.account_snapshot == {}, "source accounts moved on a pre-op refusal")
        return {"code": exc.code, "session_created": False,
                "route_pass_attempts": ex.route_pass_attempts,
                "account_snapshot": exc.account_snapshot}
    finally:
        ex.close()


def a5():
    """NON-ROUTE outer MAX 0 does not block the underlying source work."""
    ex = BoundSourceExecution(spec(
        "NR-MAX0", dta("a5.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec(expected=0, maximum=0), applicable=NON_ROUTE))
    try:
        out = ex.execute()
        need(out.observed_accounts["full_reads"] == 1, "source work was blocked by outer max0")
        need(out.full_route_passes_observed == 0, "outer observed != 0")
        return {"full_reads": out.observed_accounts["full_reads"],
                "outer_observed": out.full_route_passes_observed,
                "metadata_reads": out.observed_accounts["metadata_reads"]}
    finally:
        ex.close()


def a6():
    """An incoherent NOT_APPLICABLE + EXACT 1 spec fails BEFORE any access."""
    missing = str(WORK / "does-not-exist-a6.sav")
    exc = expect_raise(lambda: spec(
        "INCOHERENT", missing, "sav",
        SourceOperationPlan(mode=RowDataMode.METADATA_ONLY),
        rp=RoutePassSpec(expected=1), applicable=NON_ROUTE), BindingError)
    need(exc is not None, "incoherent applicability/expectation did NOT fail")
    need(not isinstance(exc, tuple), f"unexpected exception type {exc}")
    need("NOT_APPLICABLE" in str(exc), "refusal does not name the incoherence")
    return {"raised": type(exc).__name__, "message": str(exc),
            "path_existed": Path(missing).exists()}


def a7():
    """Applicability is explicit: not inferred from source key and not from plan mode."""
    key = "SRC27-SHAPED"          # a name that naively 'is' a route
    path = dta("a7.dta")
    plan = SourceOperationPlan(mode=RowDataMode.FULL, encoding="latin1")

    ex_nr = BoundSourceExecution(spec(key, path, "dta", plan,
                                      rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        out_nr = ex_nr.execute()
    finally:
        ex_nr.close()

    ex_r = BoundSourceExecution(spec(key, path, "dta", plan,
                                     rp=ZERO_OUTER, applicable=ROUTE))
    try:
        exc = expect_raise(ex_r.execute, SourceAccessViolation)
        need(exc is not None and not isinstance(exc, tuple), "same key+plan as ROUTE was not refused")
        need(exc.code == ROUTE_PASS_LIMIT_REACHED, f"wrong code {exc.code}")
        refused_code = exc.code
    finally:
        ex_r.close()

    need(out_nr.full_route_passes_observed == 0, "non-route outer observed != 0")
    need(out_nr.observed_accounts["full_reads"] == 1, "non-route full read missing")
    return {"identical_source_entry_key": key,
            "identical_plan_mode": "FULL",
            "as_NOT_APPLICABLE": {"ran": True,
                                  "outer_observed": out_nr.full_route_passes_observed,
                                  "full_reads": out_nr.observed_accounts["full_reads"]},
            "as_APPLICABLE": {"ran": False, "code": refused_code},
            "conclusion": "applicability follows the caller binding, not the key or the mode"}


def a8():
    """The default applicability is NOT_APPLICABLE: no pass is acquired by omission."""
    ex = BoundSourceExecution(spec(
        "DEFAULT", dta("a8.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec()))
    try:
        out = ex.execute()
        need(out.route_pass_applicable is False, "default applicability is not NOT_APPLICABLE")
        need(out.full_route_passes_observed == 0, "default acquired an outer pass")
        default_observed = out.full_route_passes_observed
    finally:
        ex.close()

    exc = expect_raise(lambda: spec(
        "DEFAULT-EXACT1", dta("a8b.dta"), "dta",
        SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec(expected=1)), BindingError)
    need(exc is not None and not isinstance(exc, tuple),
         "default applicability accepted an EXACT 1 outer expectation")
    return {"default_outer_observed": default_observed,
            "default_plus_exact1": "REFUSED_AT_BIND",
            "spec_dict_default_applicability":
                spec("D", dta("a8c.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
                     rp=RoutePassSpec()).as_dict()["route_pass_applicability"]}


# ====================================================== B: ATTEMPTS / RETRIES
def b1():
    """The first admitted attempt is not a retry."""
    ex = BoundSourceExecution(spec(
        "B1", dta("b1.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec(), applicable=NON_ROUTE, budget=SourceAccessBudget(retries=0)))
    try:
        out = ex.execute()
        need(out.route_pass_attempts == 1, "first attempt not counted as one attempt")
        need(out.retries_observed == 0, "first attempt was charged as a retry")
        need(out.observed_accounts["retries"] == 0, "lower-layer retries account moved")
        return {"route_pass_attempts": out.route_pass_attempts,
                "retries_observed": out.retries_observed,
                "account_retries": out.observed_accounts["retries"],
                "completed_route_passes": out.completed_route_passes}
    finally:
        ex.close()


def b2():
    """Failed first attempt + retries0 => second execute refused pre-operation."""
    ex = BoundSourceExecution(spec(
        "B2", dta("b2.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec(), applicable=NON_ROUTE, budget=SourceAccessBudget(retries=0),
        cons=(AccountConstraint("full_reads", CountKind.EXACT, 99, FROZEN),)))
    try:
        first = expect_raise(ex.execute, SourceAccessViolation)
        need(first is not None and not isinstance(first, tuple), "first attempt did not fail")
        need(first.code == POST_EXECUTION_CONSTRAINT_FAILED, f"wrong first code {first.code}")
        need(ex.route_pass_attempts == 1, "first attempt not counted")
        need(ex.retries_observed == 0, "a retry was charged to the first attempt")
        before = snap(ex)
        need(before is not None, "session missing after a post-session failure")

        second = expect_raise(ex.execute, SourceAccessViolation)
        need(second is not None and not isinstance(second, tuple), "second execute was NOT refused")
        need(second.code == RETRY_LIMIT_REACHED, f"wrong refusal code {second.code}")
        after = snap(ex)
        return {"first_code": first.code, "second_code": second.code,
                "attempts": ex.route_pass_attempts,
                "completed": ex.completed_route_passes,
                "retries": ex.retries_observed,
                "accounts_before_refusal": before,
                "accounts_after_refusal": after,
                "refusal_moved_no_source_account": before == after}
    finally:
        ex.close()


def b3():
    """A refused attempt moves no source account at all."""
    ex = BoundSourceExecution(spec(
        "B3", dta("b3.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec(), applicable=NON_ROUTE, budget=SourceAccessBudget(retries=0),
        cons=(AccountConstraint("full_reads", CountKind.EXACT, 99, FROZEN),)))
    try:
        expect_raise(ex.execute, SourceAccessViolation)
        before = snap(ex)
        refused = expect_raise(ex.execute, SourceAccessViolation)
        after = snap(ex)
        need(refused is not None and not isinstance(refused, tuple), "not refused")
        need(before == after, f"accounts moved across a refusal:\n{before}\n{after}")
        need(ex.route_pass_attempts == 1, "refused pre-op gate counted as an attempt")
        return {"before": before, "after": after, "moved": before != after,
                "attempts_after_refusal": ex.route_pass_attempts}
    finally:
        ex.close()


def b4():
    """Attempts, retries and completions are three distinct counters."""
    path = str(WORK / "b4.sav")            # deliberately not yet written
    ex = BoundSourceExecution(spec(
        "B4", path, "sav", plan_of(RowDataMode.METADATA_ONLY, retries=2),
        rp=RoutePassSpec(), applicable=ROUTE, budget=SourceAccessBudget(retries=2)))
    try:
        e1 = expect_raise(ex.execute, SourceAccessViolation)
        e2 = expect_raise(ex.execute, SourceAccessViolation)
        need(e1 is not None and not isinstance(e1, tuple), "attempt 1 did not fail")
        need(e2 is not None and not isinstance(e2, tuple), "attempt 2 did not fail")
        pyreadstat.write_sav(frame(), path)     # now let attempt 3 succeed
        out = ex.execute()
        need(out.route_pass_attempts == 3, f"attempts {out.route_pass_attempts} != 3")
        need(out.retries_observed == 2, f"retries {out.retries_observed} != 2")
        need(out.completed_route_passes == 1, f"completed {out.completed_route_passes} != 1")
        need(len({out.route_pass_attempts, out.retries_observed,
                  out.completed_route_passes}) == 3, "counters collapsed onto each other")
        return {"attempts": out.route_pass_attempts, "retries": out.retries_observed,
                "completed": out.completed_route_passes,
                "all_three_distinct": True,
                "failure_codes": [getattr(e1, "code", None), getattr(e2, "code", None)]}
    finally:
        ex.close()


def b5():
    """The retry count IS the existing SourceAccessAccount.retries account."""
    path = str(WORK / "b5.sav")
    ex = BoundSourceExecution(spec(
        "B5", path, "sav", plan_of(RowDataMode.METADATA_ONLY, retries=1),
        rp=RoutePassSpec(), applicable=ROUTE, budget=SourceAccessBudget(retries=1)))
    try:
        expect_raise(ex.execute, SourceAccessViolation)
        pyreadstat.write_sav(frame(), path)
        out = ex.execute()
        acct = ex.session.account
        need(isinstance(acct, SourceAccessAccount), "session account is not a SourceAccessAccount")
        need(acct.retries == 1, f"SourceAccessAccount.retries {acct.retries} != 1")
        need(out.observed_accounts["retries"] == acct.retries, "receipt retries != account retries")
        need(out.retries_observed == acct.retries, "outcome retries != account retries")
        need(ex.retries_observed == acct.retries, "execution retries != account retries")
        return {"SourceAccessAccount.retries": acct.retries,
                "outcome.observed_accounts.retries": out.observed_accounts["retries"],
                "outcome.retries_observed": out.retries_observed,
                "execution.retries_observed": ex.retries_observed}
    finally:
        ex.close()


def b6():
    """SourceAccessBudget.retries owns the ceiling: retries advance exactly and stop."""
    table = []
    for ceiling in (0, 1, 2, 3):
        path = str(WORK / f"b6-missing-{ceiling}.sav")
        ex = BoundSourceExecution(spec(
            f"B6-{ceiling}", path, "sav",
            plan_of(RowDataMode.METADATA_ONLY, retries=ceiling),
            rp=RoutePassSpec(), applicable=ROUTE,
            budget=SourceAccessBudget(retries=ceiling)))
        try:
            admitted = 0
            refusal = None
            for _ in range(ceiling + 4):
                exc = expect_raise(ex.execute, SourceAccessViolation)
                if exc is not None and not isinstance(exc, tuple) \
                        and exc.code == RETRY_LIMIT_REACHED:
                    refusal = exc.code
                    break
                if exc is not None and not isinstance(exc, tuple):
                    admitted += 1     # admitted, then failed on the missing carrier
                    continue
                admitted += 1
            need(refusal == RETRY_LIMIT_REACHED,
                 f"ceiling {ceiling}: no retry refusal was reached")
            need(admitted == ceiling + 1,
                 f"ceiling {ceiling}: admitted {admitted}, expected {ceiling + 1}")
            need(ex.retries_observed == ceiling,
                 f"ceiling {ceiling}: retries {ex.retries_observed} != ceiling")
            need(ex.route_pass_attempts == ceiling + 1,
                 f"ceiling {ceiling}: attempts {ex.route_pass_attempts}")
            table.append({"ceiling": ceiling, "admitted_attempts": admitted,
                          "retries_observed": ex.retries_observed,
                          "refusal_code": refusal,
                          "stopped_exactly_at_ceiling": True})
        finally:
            ex.close()
    return {"by_ceiling": table}


def b7():
    """SourceOperationPlan.max_retries cannot silently disagree with the ceiling."""
    plan1 = SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=1)
    e1 = expect_raise(lambda: spec("B7a", dta("b7.dta"), "dta", plan1,
                                   budget=SourceAccessBudget(retries=0)), BindingError)
    need(e1 is not None and not isinstance(e1, tuple), "plan 1 > budget 0 was accepted")
    need(RETRY_BINDING_MISMATCH in str(e1), "refusal does not name the binding mismatch")

    plan0 = SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0)
    e2 = expect_raise(lambda: spec("B7b", dta("b7b.dta"), "dta", plan0,
                                   budget=SourceAccessBudget(retries=1)), BindingError)
    need(e2 is not None and not isinstance(e2, tuple), "budget 1 > plan 0 was accepted")

    e3 = expect_raise(lambda: spec("B7c", dta("b7c.dta"), "dta", plan0,
                                   budget=SourceAccessBudget(retries=None)), BindingError)
    need(e3 is not None and not isinstance(e3, tuple), "unbounded retry ceiling was accepted")

    good_plan = SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=2)
    base = spec("B7d", dta("b7d.dta"), "dta", good_plan,
                budget=SourceAccessBudget(retries=2))
    swapped = SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0)
    e4 = expect_raise(lambda: base.with_plan(swapped), BindingError)
    need(e4 is not None and not isinstance(e4, tuple),
         "a plan swap that disagrees with the ceiling was accepted")

    return {"plan1_budget0": str(e1), "plan0_budget1": str(e2),
            "unbounded_ceiling": str(e3), "plan_swap_disagreement": str(e4),
            "agreeing_pair_accepted": base.as_dict()["retry_binding_law"]}


def b8():
    """Attack: failure BEFORE session creation, with retries0."""
    class _BadVersion:
        __version__ = "0.0.1"

    path = sav("b8.sav")
    ex = BoundSourceExecution(spec(
        "B8", path, "sav", SourceOperationPlan(mode=RowDataMode.METADATA_ONLY),
        rp=ZERO_OUTER, applicable=NON_ROUTE, budget=SourceAccessBudget(retries=0)),
        pyreadstat_module=_BadVersion())
    try:
        first = expect_raise(ex.execute, SourceAccessViolation)
        need(first is not None and not isinstance(first, tuple),
             "poisoned module did not raise at session creation")
        need(isinstance(first, ReaderSeamViolation), f"unexpected type {type(first).__name__}")
        need(ex.route_pass_attempts == 1, "the admitted attempt was not counted")
        need(session_or_none(ex) is None, "a session existed despite a failed construction")

        second = expect_raise(ex.execute, SourceAccessViolation)
        need(second is not None and not isinstance(second, tuple), "second execute was not refused")
        need(second.code == RETRY_LIMIT_REACHED, f"wrong code {second.code}")
        need(session_or_none(ex) is None, "the refusal created a session")
        need(second.account_snapshot == {}, "source accounts moved")
        return {"first": type(first).__name__, "second_code": second.code,
                "attempts": ex.route_pass_attempts,
                "session_created": False,
                "account_snapshot_on_refusal": second.account_snapshot}
    finally:
        ex.close()


def b9():
    """Attack: failure after session creation, retries0 and retries1."""
    out = {}
    # retries0
    ex0 = BoundSourceExecution(spec(
        "B9a", sav("b9a.sav"), "sav", SourceOperationPlan(mode=RowDataMode.METADATA_ONLY),
        rp=RoutePassSpec(), applicable=ROUTE, budget=SourceAccessBudget(retries=0),
        sha="00" * 32))
    try:
        first = expect_raise(ex0.execute, SourceAccessViolation)
        need(first is not None and not isinstance(first, tuple), "sha mismatch did not raise")
        need(session_or_none(ex0) is not None, "no session after a post-session failure")
        before = snap(ex0)
        second = expect_raise(ex0.execute, SourceAccessViolation)
        need(second is not None and not isinstance(second, tuple), "retries0 second not refused")
        need(second.code == RETRY_LIMIT_REACHED, f"wrong code {second.code}")
        after = snap(ex0)
        out["retries0"] = {"first_code": first.code, "second_code": second.code,
                           "accounts_unchanged_by_refusal": before == after,
                           "attempts": ex0.route_pass_attempts,
                           "retries": ex0.retries_observed}
    finally:
        ex0.close()
    # retries1: the retry is charged BEFORE the source operation
    ex1 = BoundSourceExecution(spec(
        "B9b", sav("b9b.sav"), "sav", plan_of(RowDataMode.METADATA_ONLY, retries=1),
        rp=RoutePassSpec(), applicable=ROUTE, budget=SourceAccessBudget(retries=1),
        sha="11" * 32))
    try:
        e1 = expect_raise(ex1.execute, SourceAccessViolation)
        need(e1 is not None and not isinstance(e1, tuple), "attempt 1 did not fail")
        need(ex1.retries_observed == 0, "attempt 1 charged a retry")
        e2 = expect_raise(ex1.execute, SourceAccessViolation)
        need(e2 is not None and not isinstance(e2, tuple), "attempt 2 did not fail")
        need(ex1.retries_observed == 1,
             "the retry was not charged before the second source operation")
        e3 = expect_raise(ex1.execute, SourceAccessViolation)
        need(e3 is not None and not isinstance(e3, tuple), "third attempt was not refused")
        need(e3.code == RETRY_LIMIT_REACHED, f"wrong third code {e3.code}")
        out["retries1"] = {"codes": [e1.code, e2.code, e3.code],
                           "attempts": ex1.route_pass_attempts,
                           "retries": ex1.retries_observed,
                           "retry_charged_pre_operation": ex1.retries_observed == 1}
    finally:
        ex1.close()
    return out


def b10():
    """A retry gate must not create source activity merely to account the retry."""
    # The retry is accounted through the broker, which performs no source I/O.
    path = sav("b10.sav")
    ex = BoundSourceExecution(spec(
        "B10", path, "sav", plan_of(RowDataMode.METADATA_ONLY, retries=1),
        rp=RoutePassSpec(), applicable=ROUTE, budget=SourceAccessBudget(retries=1),
        cons=(AccountConstraint("metadata_reads", CountKind.EXACT, 99, FROZEN),)))
    try:
        expect_raise(ex.execute, SourceAccessViolation)
        a1 = snap(ex)
        # second attempt is admitted (retry charged) and then fails its postcondition
        e2 = expect_raise(ex.execute, SourceAccessViolation)
        need(e2 is not None and not isinstance(e2, tuple), "attempt 2 did not fail")
        a2 = snap(ex)
        # Exactly one extra decoder entry and one extra reader call: the retry
        # accounting itself issued no reader call and opened no second path.
        need(a2["decoder_invocations"] - a1["decoder_invocations"] == 1,
             "retry admission caused an unexpected decoder entry delta")
        need(a2["reader_invocations"] - a1["reader_invocations"] == 1,
             "retry admission issued reader calls beyond the one real operation")
        need(a2["path_opens"] == 1, f"path opens {a2['path_opens']} != 1")
        need(a2["retries"] == 1, "retry was not accounted on the retries account")
        return {"retries_account_delta": a2["retries"] - a1["retries"],
                "decoder_delta": a2["decoder_invocations"] - a1["decoder_invocations"],
                "reader_invocation_delta": a2["reader_invocations"] - a1["reader_invocations"],
                "path_opens_total": a2["path_opens"],
                "no_reader_call_for_the_accounting_itself": True}
    finally:
        ex.close()


# ==================================================== C: COMPLETION SEMANTICS
def c1():
    """Source success + lower-layer postcondition failure is NOT a completed pass."""
    ex = BoundSourceExecution(spec(
        "C1", dta("c1.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec(expected=1, maximum=1), applicable=ROUTE,
        cons=(AccountConstraint("full_reads", CountKind.EXACT, 2, FROZEN),)))
    try:
        exc = expect_raise(ex.execute, SourceAccessViolation)
        need(exc is not None and not isinstance(exc, tuple), "postcondition failure did not raise")
        need(exc.code == POST_EXECUTION_CONSTRAINT_FAILED, f"wrong code {exc.code}")
        need(ex.completed_route_passes == 0, "a completed pass leaked past a failed postcondition")
        need(ex.route_pass_attempts == 1, "attempt not counted")
        acct = snap(ex)
        need(acct is not None and acct["full_reads"] == 1,
             "the source operation did not actually succeed first")
        return {"code": exc.code, "completed_route_passes": ex.completed_route_passes,
                "attempts": ex.route_pass_attempts, "full_reads_observed": acct["full_reads"]}
    finally:
        ex.close()


def c2():
    """Source success + outer exact failure is NOT a completed pass."""
    ex = BoundSourceExecution(spec(
        "C2", dta("c2.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec(expected=2, maximum=3), applicable=ROUTE))
    try:
        exc = expect_raise(ex.execute, SourceAccessViolation)
        need(exc is not None and not isinstance(exc, tuple), "outer exact failure did not raise")
        need(exc.code == POST_EXECUTION_CONSTRAINT_FAILED, f"wrong code {exc.code}")
        need(ex.completed_route_passes == 0, "outer exact failure left a completed pass")
        acct = snap(ex)
        need(acct is not None and acct["full_reads"] == 1,
             "the source operation did not actually succeed first")
        # The prospective count was not committed, so the pre-op gates still see 0.
        second = expect_raise(ex.execute, SourceAccessViolation)
        need(second is not None and not isinstance(second, tuple), "second was not refused")
        return {"code": exc.code, "completed_route_passes": ex.completed_route_passes,
                "full_reads_observed": acct["full_reads"],
                "second_attempt_refusal_code": second.code}
    finally:
        ex.close()


def c3():
    """Completion DOES occur once every postcondition has succeeded."""
    ex = BoundSourceExecution(spec(
        "C3", dta("c3.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec(expected=1, maximum=1), applicable=ROUTE,
        cons=(AccountConstraint("full_reads", CountKind.FLOOR, 1, FROZEN),
              AccountConstraint("metadata_reads", CountKind.FLOOR, 1, FROZEN))))
    try:
        out = ex.execute()
        need(out.completed_pass is True, "completed_pass is not True on a fully satisfied pass")
        need(out.full_route_passes_observed == 1, "outer observed != 1")
        need(ex.completed_route_passes == 1, "completed counter != 1")
        need(out.observed_accounts["full_reads"] >= 1, "full_reads floor not met")
        return {"completed_pass": out.completed_pass,
                "outer_observed": out.full_route_passes_observed,
                "completed_route_passes": ex.completed_route_passes,
                "constraint_report": [dict(c) for c in out.constraint_report]}
    finally:
        ex.close()


def c4():
    """Ordering: the outer accept-and-increment happens only after ALL lower rules."""
    ex = BoundSourceExecution(spec(
        "C4", dta("c4.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=RoutePassSpec(expected=1, maximum=1), applicable=ROUTE,
        cons=(AccountConstraint("full_reads", CountKind.EXACT, 7, FROZEN),)))
    try:
        exc = expect_raise(ex.execute, SourceAccessViolation)
        need(exc is not None and not isinstance(exc, tuple), "not refused")
        need(exc.code == POST_EXECUTION_CONSTRAINT_FAILED, "wrong code")
        need(ex.completed_route_passes == 0,
             "the outer count advanced although a lower rule failed")
        need("full_reads" in str(exc), "the lower-rule failure is not the reported cause")
        return {"code": exc.code, "completed_route_passes": ex.completed_route_passes,
                "message_names_lower_account": True}
    finally:
        ex.close()


def c5():
    """A non-route execution never manufactures a phantom completion."""
    ex = BoundSourceExecution(spec(
        "C5", dta("c5.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL),
        rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        out = ex.execute()
        need(out.completed_route_passes == 0, "non-route completion counter != 0")
        need(out.completed_pass is False, "non-route completed_pass is not False")
        need(out.full_route_passes_observed == 0, "non-route outer observed != 0")
        return {"completed_route_passes": out.completed_route_passes,
                "completed_pass": out.completed_pass,
                "outer_observed": out.full_route_passes_observed}
    finally:
        ex.close()


# ======================================================= D: INJECTION
class _Meta:
    def __init__(self, columns, number_rows=0):
        self.column_names = list(columns)
        self.number_rows = number_rows


class _Frame:
    def __init__(self, columns):
        self.columns = list(columns)


class _StubReader:
    """A controlled pyreadstat stand-in that records every consultation."""

    __version__ = "1.3.6"

    def __init__(self, columns=("Q10B", "Q101", "Q2061B")):
        self.columns = tuple(columns)
        self.calls = []

    def read_sav(self, filename_path, **kwargs):
        self.calls.append({"reader": "read_sav", "kwargs": dict(kwargs),
                           "arg_type": type(filename_path).__name__,
                           "has_fileno": hasattr(filename_path, "fileno")})
        cols = list(self.columns)
        if kwargs.get("usecols"):
            cols = list(kwargs["usecols"])
        return _Frame(cols), _Meta(self.columns)

    def read_dta(self, filename_path, **kwargs):
        self.calls.append({"reader": "read_dta", "kwargs": dict(kwargs),
                           "arg_type": type(filename_path).__name__,
                           "has_fileno": hasattr(filename_path, "fileno")})
        cols = list(self.columns)
        if kwargs.get("usecols"):
            cols = list(kwargs["usecols"])
        return _Frame(cols), _Meta(self.columns)

    def metadata_read(self, *a, **k):
        raise AssertionError("the runtime must call the reader entry points directly")


def _with_real_reader_poisoned(fn):
    real_sav, real_dta = pyreadstat.read_sav, pyreadstat.read_dta

    def _boom(*a, **k):
        raise AssertionError("the REAL pyreadstat entry point was consulted")

    pyreadstat.read_sav = _boom
    pyreadstat.read_dta = _boom
    try:
        return fn()
    finally:
        pyreadstat.read_sav = real_sav
        pyreadstat.read_dta = real_dta


def d1():
    """The exact supplied object reaches the seam and is consulted, not ignored."""
    stub = _StubReader()

    def _run():
        ex = BoundSourceExecution(spec(
            "D1", sav("d1.sav"), "sav",
            SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="BIG5")),
            pyreadstat_module=stub)
        try:
            out = ex.execute()
            return ex, out
        except Exception:
            ex.close()
            raise

    ex, out = _with_real_reader_poisoned(_run)
    try:
        need(ex.pyreadstat_module is stub, "the execution did not retain the supplied object")
        need(ex.session.broker.pyreadstat is stub, "the broker holds a different object")
        need(len(stub.calls) == 1, f"the supplied object was consulted {len(stub.calls)} times")
        call = stub.calls[0]
        need(call["reader"] == "read_sav", "the wrong reader entry point was used")
        need(call["kwargs"].get("metadataonly") is True,
             "the supplied object was not told it was a metadata read")
        need(call["kwargs"].get("encoding") == "BIG5", "the declared encoding was dropped")
        need(call["has_fileno"] is True, "the reader received something without fileno")
        need(out.observed_accounts["metadata_reads"] == 1, "metadata_reads != 1")
        return {"identity_preserved_on_execution": ex.pyreadstat_module is stub,
                "identity_preserved_on_broker": ex.session.broker.pyreadstat is stub,
                "consultations": len(stub.calls),
                "recorded_kwargs": call["kwargs"],
                "argument_type": call["arg_type"],
                "argument_has_fileno": call["has_fileno"],
                "real_pyreadstat_entry_points_poisoned_and_never_called": True}
    finally:
        ex.close()


def d2():
    """The supplied object is load-bearing: its inventory decides the bound ordinals."""
    stub = _StubReader(columns=("alpha", "beta", "gamma"))

    def _run():
        ex = BoundSourceExecution(spec(
            "D2", sav("d2.sav"), "sav",
            SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("gamma",))),
            pyreadstat_module=stub)
        try:
            return ex, ex.execute()
        except Exception:
            ex.close()
            raise

    ex, out = _with_real_reader_poisoned(_run)
    try:
        receipt = ex.session.aggregate_receipt()
        ordinals = list(receipt["selected_ordinals"].get("D2", []))
        need(ordinals == [3], f"bound ordinals {ordinals} != [3] from the SUPPLIED inventory")
        need(len(stub.calls) == 2, f"expected metadata+selected consultation, got {len(stub.calls)}")
        need(stub.calls[1]["kwargs"].get("usecols") == ["gamma"],
             "the selected set did not reach the supplied object")
        return {"supplied_inventory": list(stub.columns),
                "bound_ordinals": ordinals,
                "consultations": len(stub.calls),
                "selected_read_kwargs": stub.calls[1]["kwargs"],
                "reader_kinds": [c["reader"] for c in stub.calls]}
    finally:
        ex.close()


def d3():
    """The DTA lane consults the supplied object's read_dta, not read_sav."""
    stub = _StubReader()

    def _run():
        ex = BoundSourceExecution(spec(
            "D3", dta("d3.dta"), "dta", SourceOperationPlan(mode=RowDataMode.FULL)),
            pyreadstat_module=stub)
        try:
            return ex, ex.execute()
        except Exception:
            ex.close()
            raise

    ex, out = _with_real_reader_poisoned(_run)
    try:
        kinds = [c["reader"] for c in stub.calls]
        need(kinds and set(kinds) == {"read_dta"}, f"read_sav was used for a DTA source: {kinds}")
        need(out.observed_accounts["full_reads"] == 1, "full_reads != 1")
        need(out.observed_accounts["metadata_reads"] == 1,
             "metadata admission did not precede the full read")
        need([c["kwargs"].get("metadataonly") for c in stub.calls] == [True, None],
             "the metadata and full reader calls were not distinguishable")
        return {"reader_used": kinds,
                "metadata_then_full": [c["kwargs"].get("metadataonly") for c in stub.calls],
                "full_reads": out.observed_accounts["full_reads"],
                "metadata_reads": out.observed_accounts["metadata_reads"]}
    finally:
        ex.close()


def d4():
    """None means the real module is resolved (no silent replacement)."""
    ex = BoundSourceExecution(spec(
        "D4", sav("d4.sav"), "sav", SourceOperationPlan(mode=RowDataMode.METADATA_ONLY)))
    try:
        need(ex.pyreadstat_module is None, "None was not preserved on the execution")
        ex.execute()
        need(ex.session.broker.pyreadstat is pyreadstat,
             "None did not resolve to the real installed pyreadstat")
        need(ex.session.broker.pyreadstat_version == "1.3.6",
             "resolved version is not the pinned one")
        return {"execution_module": None, "broker_module_is_real": True,
                "resolved_version": ex.session.broker.pyreadstat_version}
    finally:
        ex.close()


def d5():
    """A supplied object that breaks the pinned seam is refused, so injection is real."""
    class _Bad(_StubReader):
        __version__ = "9.9.9"

    ex = BoundSourceExecution(spec(
        "D5", sav("d5.sav"), "sav", SourceOperationPlan(mode=RowDataMode.METADATA_ONLY)),
        pyreadstat_module=_Bad())
    try:
        exc = expect_raise(ex.execute, SourceAccessViolation)
        need(exc is not None and not isinstance(exc, tuple), "a bad injected module was accepted")
        need(isinstance(exc, ReaderSeamViolation), f"unexpected type {type(exc).__name__}")
        return {"code": exc.code if hasattr(exc, "code") else type(exc).__name__,
                "message": str(exc)[:160]}
    finally:
        ex.close()


def d6():
    """A supplied object missing a required reader is refused at the seam."""
    class _Missing(_StubReader):
        read_dta = None

    ex = BoundSourceExecution(spec(
        "D6", sav("d6.sav"), "sav", SourceOperationPlan(mode=RowDataMode.METADATA_ONLY)),
        pyreadstat_module=_Missing())
    try:
        exc = expect_raise(ex.execute, SourceAccessViolation)
        need(exc is not None and not isinstance(exc, tuple), "a module missing read_dta was accepted")
        return {"raised": type(exc).__name__, "message": str(exc)[:160]}
    finally:
        ex.close()


CLAIMS = [
    ("A1", "metadata-only non-route runs with outer EXACT 0 and observes 0", a1),
    ("A2", "selected non-route runs with outer EXACT 0 and observes 0", a2),
    ("A3", "FULL plan can be NOT_APPLICABLE and observe outer 0", a3),
    ("A4", "APPLICABLE route MAX 0 is refused before session/source operation", a4),
    ("A5", "non-route MAX 0 does not block underlying source work", a5),
    ("A6", "NOT_APPLICABLE + EXACT 1 fails before access", a6),
    ("A7", "applicability is not inferred from source key or plan mode", a7),
    ("A8", "default applicability is NOT_APPLICABLE", a8),
    ("B1", "first admitted attempt is not a retry", b1),
    ("B2", "failed first attempt + retries0 refuses the second pre-operation", b2),
    ("B3", "a refused attempt moves no source account", b3),
    ("B4", "attempt / retry / completed counters are three distinct counters", b4),
    ("B5", "the retry count is the existing SourceAccessAccount.retries account", b5),
    ("B6", "SourceAccessBudget.retries owns the ceiling and stops exactly there", b6),
    ("B7", "SourceOperationPlan.max_retries cannot silently disagree", b7),
    ("B8", "failure before session creation: retries0 refuses pre-operation", b8),
    ("B9", "failure after session creation: retries0 refuses; retries1 charges pre-op", b9),
    ("B10", "retry accounting itself creates no source activity", b10),
    ("C1", "source success + lower-layer postcondition failure is not a completed pass", c1),
    ("C2", "source success + outer exact failure is not a completed pass", c2),
    ("C3", "completion occurs once every postcondition has succeeded", c3),
    ("C4", "the outer count advances only after all lower rules", c4),
    ("C5", "a non-route execution never manufactures a phantom completion", c5),
    ("D1", "the exact supplied pyreadstat object reaches the seam and is consulted", d1),
    ("D2", "the supplied object is load-bearing, not merely accepted", d2),
    ("D3", "the supplied object's read_dta is used for a DTA source", d3),
    ("D4", "None resolves to the real pinned pyreadstat", d4),
    ("D5", "a seam-violating supplied object is refused", d5),
    ("D6", "a supplied object missing a reader is refused", d6),
]


def main() -> int:
    for cid, title, fn in CLAIMS:
        claim(cid, title, fn)
    passed = sum(1 for r in RESULTS if r["ok"])
    doc = {
        "schema": "HQ202_INDEPENDENT_PROOFS_A_D@1.0.0",
        "reviewer_authored": True,
        "reuses_candidate_court": False,
        "public_surface_only_for_execution": "BoundSourceExecution.execute()",
        "rounds": ["A route-pass applicability", "B attempts/retries/completions",
                   "C completion semantics", "D dependency injection"],
        "claims_total": len(RESULTS),
        "claims_passed": passed,
        "claims_failed": len(RESULTS) - passed,
        "work_dir": str(WORK),
        "results": RESULTS,
    }
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
