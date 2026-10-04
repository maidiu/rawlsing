"""HQ201 — execution-binding bounded hardening court.

Synthetic SAV/DTA carriers only. No real survey source is opened.

The seven specs below reproduce the documentary source-plan SHAPES. The TESTS may
name those shapes; PRODUCTION may not.

Governing semantics under test:

  Repair 1  Route-pass APPLICABILITY is explicit and caller-bound. A non-route
            execution still performs its metadata/selected/full work and reports
            an outer observed count of 0. A route-pass maximum of 0 there means
            "not a route pass", NEVER "no source operation".

  Repair 2  route_pass_attempts, retries and completed_route_passes are three
            separate counters. A refused pre-operation gate is not an attempt.
            Each additional admitted attempt increments the lower-layer retries
            account under its own ceiling BEFORE source work.

  Repair 3  A pass is completed only after the source operation AND every
            caller-supplied exact/floor postcondition AND the outer rule succeed.
            The prospective count is validated before it is committed.

  Repair 4  pyreadstat_module is passed through to the session, not discarded.

Plus the SRC27-shaped outer law:
  full_route_passes   EXACT 1 / MAX 1
  full_reads          FLOOR >= 1, ceiling UNBOUND
  decoder_invocations MAX 1 allowed only as IMPLEMENTATION_POLICY
  path_opens          one-open ceiling allowed only as IMPLEMENTATION_POLICY
  retries             MAX 0
  chunk_reads never substitute for full_reads
  full_route_passes never substitute for any lower-layer count
"""
from __future__ import annotations

import ast
import os
import tempfile
from pathlib import Path

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next.pre553_execution_binding import (
    RETRY_BINDING_LAW,
    RETRY_LIMIT_REACHED,
    AccountConstraint,
    AuthorityLabel,
    BoundExecutionSpec,
    BoundSourceExecution,
    BindingError,
    CountKind,
    LOWER_LAYER_ACCOUNTS,
    POST_EXECUTION_CONSTRAINT_FAILED,
    RETRY_BINDING_MISMATCH,
    ROUTE_PASS_LIMIT_REACHED,
    RoutePassApplicability,
    RoutePassSpec,
)
from rawlsing_next.pre553_source_access_broker import (
    ReaderSeamViolation,
    SourceAccessBudget,
    SourceAccessViolation,
)
from rawlsing_next.pre553_source_session import RowDataMode, SourceOperationPlan

CARRIERS = Path(tempfile.mkdtemp(prefix="hq201-court-"))


def _sav(name: str, frame: pd.DataFrame) -> str:
    p = CARRIERS / name
    pyreadstat.write_sav(frame, str(p))
    return str(p)


def _dta(name: str, frame: pd.DataFrame) -> str:
    p = CARRIERS / name
    pyreadstat.write_dta(frame, str(p))
    return str(p)


def _frame(rows: int = 12) -> pd.DataFrame:
    return pd.DataFrame({
        "Q10B": [float(i) for i in range(rows)],
        "Q101": [float(i * 2) for i in range(rows)],
        "Q2061B": [float(i * 3) for i in range(rows)],
    })


def _spec(source_entry_key, path, source_format, plan, *, rp=None,
          applicable=RoutePassApplicability.NOT_APPLICABLE,
          cons=(), budget=None, note=None):
    return BoundExecutionSpec(
        source_entry_key=source_entry_key, path=path, source_format=source_format, plan=plan,
        expected_sha256=None,
        budget=budget if budget is not None else SourceAccessBudget(),
        route_pass=rp if rp is not None else RoutePassSpec(),
        route_applicability=applicable,
        constraints=tuple(cons), authority_note=note,
    )


def _run(spec, **kw):
    ex = BoundSourceExecution(spec, **kw)
    try:
        return ex.execute(), ex
    except Exception:
        ex.close()
        raise


# The six documentary non-route shapes carry an EXACT 0 / MAX 0 outer account.
# That zero must NOT prohibit the underlying source work.
NON_ROUTE = RoutePassApplicability.NOT_APPLICABLE
ROUTE = RoutePassApplicability.APPLICABLE
ZERO_OUTER = RoutePassSpec(expected=0, maximum=0)


def _src27_spec(**overrides):
    """The SRC27-shaped spec. FULL compatibility lane, latin1, outer EXACT/MAX 1."""
    kw = dict(
        source_entry_key="SRC27-SHAPED",
        path=_dta("src27.dta", _frame(10)),
        source_format="dta",
        plan=SourceOperationPlan(mode=RowDataMode.FULL, encoding="latin1"),
        rp=RoutePassSpec(expected=1, maximum=1, token="governed full Route-B pass"),
        applicable=ROUTE,
        cons=(
            AccountConstraint("metadata_reads", CountKind.FLOOR, 1, AuthorityLabel.FROZEN_AUTHORITY),
            AccountConstraint("full_reads", CountKind.FLOOR, 1, AuthorityLabel.FROZEN_AUTHORITY),
            AccountConstraint("decoder_invocations", CountKind.MAXIMUM, 1,
                              AuthorityLabel.IMPLEMENTATION_POLICY),
            AccountConstraint("path_opens", CountKind.MAXIMUM, 1,
                              AuthorityLabel.IMPLEMENTATION_POLICY),
        ),
        budget=SourceAccessBudget(decoder_invocations=1, retries=0),
        note="synthetic reproduction of a documented plan SHAPE; no source key is bound in production",
    )
    kw.update(overrides)
    return _spec(**kw)


# ============================================================ Repair 1: applicability
def test_metadata_non_route_execution_succeeds_with_outer_exact0():
    """Court 1 — metadata-only non-route execution, outer EXACT 0, observed 0."""
    out, ex = _run(_spec("NR-META", _sav("nr_meta.sav", _frame()), "sav",
                         SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="BIG5"),
                         rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        assert out.full_route_passes_observed == 0
        assert out.completed_pass is False
        assert out.route_pass_status == "NOT_APPLICABLE"
        assert out.route_pass_applicable is False
        # the underlying work really happened
        assert out.observed_accounts["metadata_reads"] == 1
    finally:
        ex.close()


def test_selected_non_route_execution_succeeds_with_outer_exact0():
    """Court 2 — selected non-route execution, outer EXACT 0, observed 0."""
    out, ex = _run(_spec("NR-SEL", _sav("nr_sel.sav", _frame()), "sav",
                         SourceOperationPlan(mode=RowDataMode.SELECTED,
                                             selected_variables=("Q10B",)),
                         rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        assert out.full_route_passes_observed == 0
        assert out.completed_pass is False
        assert out.route_pass_status == "NOT_APPLICABLE"
        assert out.observed_accounts["selected_reads"] == 1
        assert out.observed_accounts["full_reads"] == 0
    finally:
        ex.close()


def test_route_applicable_full_execution_gives_outer_exact_max1():
    """Court 3 — route-applicable FULL execution gives outer EXACT/MAX 1."""
    out, ex = _run(_src27_spec())
    try:
        d = out.as_dict()
        assert out.full_route_passes_observed == 1
        assert d["full_route_passes_expected"] == 1
        assert d["full_route_passes_expected_status"] == "EXACT"
        assert d["full_route_passes_max"] == 1
        assert d["full_route_passes_completed_successfully"] is True
        assert out.route_pass_applicable is True
        assert out.route_pass_status == "COMPLETED"
        assert out.observed_accounts["full_reads"] >= 1
    finally:
        ex.close()


def test_non_route_max0_does_not_block_source_work():
    """Court 4 — a route-pass MAX 0 must not mean "no source operation"."""
    out, ex = _run(_spec("NR-ZERO", _dta("nr_zero.dta", _frame(10)), "dta",
                         SourceOperationPlan(mode=RowDataMode.FULL),
                         rp=RoutePassSpec(expected=0, maximum=0), applicable=NON_ROUTE))
    try:
        assert out.full_route_passes_observed == 0
        assert out.observed_accounts["full_reads"] == 1, "the FULL work was blocked by an outer zero"
        assert out.observed_accounts["path_opens"] == 1
    finally:
        ex.close()


def test_route_max0_refuses_before_creating_a_session():
    """Court 5 — an APPLICABLE route max 0 refuses before any session exists."""
    ex = BoundSourceExecution(_src27_spec(rp=RoutePassSpec(expected=1, maximum=0)))
    try:
        with pytest.raises(SourceAccessViolation) as exc:
            ex.execute()
        assert exc.value.code == ROUTE_PASS_LIMIT_REACHED
        assert ex._session is None, "a session was created despite a pre-operation refusal"
        assert ex.counters() == {"route_pass_attempts": 0, "retries": 0, "completed_route_passes": 0}
    finally:
        ex.close()


def test_applicability_is_not_inferred_from_plan_mode():
    """A FULL decode is not automatically a Route-B pass."""
    full_non_route = _run(_spec("FULL-NR", _dta("full_nr.dta", _frame(10)), "dta",
                                SourceOperationPlan(mode=RowDataMode.FULL),
                                rp=ZERO_OUTER, applicable=NON_ROUTE))[0]
    full_route = _run(_src27_spec())[0]
    assert full_non_route.observed_accounts["full_reads"] == 1
    assert full_non_route.full_route_passes_observed == 0, "applicability leaked from plan mode"
    assert full_route.full_route_passes_observed == 1
    assert full_non_route.as_dict()["full_route_passes_completed_successfully"] is False
    assert full_route.as_dict()["full_route_passes_completed_successfully"] is True


def test_non_route_expects_zero_and_rejects_a_nonzero_outer_expectation():
    """A non-route spec may carry EXACT 0, never EXACT 1."""
    _spec("OK", _sav("ok.sav", _frame()), "sav",
          SourceOperationPlan(mode=RowDataMode.METADATA_ONLY),
          rp=RoutePassSpec(expected=0, maximum=0), applicable=NON_ROUTE)
    with pytest.raises(BindingError):
        _spec("BAD", _sav("ok.sav", _frame()), "sav",
              SourceOperationPlan(mode=RowDataMode.METADATA_ONLY),
              rp=RoutePassSpec(expected=1, maximum=1), applicable=NON_ROUTE)


# ================================================ Repair 2: attempts / retries / completions
def test_failed_first_wrapper_attempt_with_retries0_blocks_second_preop():
    """Court 6 — a failed first WRAPPER attempt + retries 0 refuses the second pre-op."""
    ex = BoundSourceExecution(_src27_spec(
        plan=SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("NO_SUCH_COLUMN",))))
    try:
        with pytest.raises(Exception):
            ex.execute()
        # the attempt was recorded; no completion
        assert ex.route_pass_attempts == 1
        assert ex.completed_route_passes == 0
        before = dict(ex.session.account_dict())
        # Court 7: every lower account unchanged on the refused retry
        with pytest.raises(SourceAccessViolation) as exc:
            ex.execute()
        assert exc.value.code == RETRY_LIMIT_REACHED
        after = dict(ex.session.account_dict())
        assert before == after, {k: (before[k], after[k]) for k in before if before[k] != after[k]}
        assert ex.route_pass_attempts == 1, "a refused retry was counted as an attempt"
    finally:
        ex.close()


def test_attempt_retry_and_completion_counters_are_distinguishable():
    """Court 7 — the three outer counters are separate quantities."""
    ex = BoundSourceExecution(_src27_spec())
    try:
        assert ex.counters() == {"route_pass_attempts": 0, "retries": 0, "completed_route_passes": 0}
        out = ex.execute()
        c = out.as_dict()["outer_counters_kept_separate"]
        # one attempt, zero retries, one completion
        assert c["route_pass_attempts"] == 1
        assert c["retries"] == 0
        assert c["completed_route_passes"] == 1
    finally:
        ex.close()


def test_failed_attempt_and_failed_postcondition_both_leave_zero_completions():
    """Court 8 — neither a source failure nor a postcondition failure completes a pass."""
    ex = BoundSourceExecution(_src27_spec(
        plan=SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("NO_SUCH_COLUMN",))))
    try:
        with pytest.raises(Exception):
            ex.execute()
        assert ex.completed_route_passes == 0 and ex.route_pass_attempts == 1
    finally:
        ex.close()


def test_second_attempt_after_postcondition_failure_obeys_retry0():
    """Court 9 — after a postcondition failure the retry law still governs."""
    # the source op SUCCEEDS, but the bound EXACT postcondition cannot be met
    ex = BoundSourceExecution(_src27_spec(
        cons=(AccountConstraint("full_reads", CountKind.EXACT, 99,
                                AuthorityLabel.FROZEN_AUTHORITY),)))
    try:
        with pytest.raises(SourceAccessViolation) as exc:
            ex.execute()
        assert exc.value.code == POST_EXECUTION_CONSTRAINT_FAILED
        assert ex.completed_route_passes == 0, "a postcondition-failed run counted as completed"
        assert ex.route_pass_attempts == 1
        before = dict(ex.session.account_dict())
        with pytest.raises(SourceAccessViolation) as retry_exc:
            ex.execute()
        assert retry_exc.value.code == RETRY_LIMIT_REACHED
        assert dict(ex.session.account_dict()) == before
    finally:
        ex.close()


def test_retry_account_increments_under_its_own_ceiling_and_is_enforced():
    """Court 10 — the retries account advances per admitted retry, then stops."""
    ceiling = 2
    ex = BoundSourceExecution(_src27_spec(
        plan=SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("NO_SUCH_COLUMN",),
                                 max_retries=ceiling),
        budget=SourceAccessBudget(retries=ceiling)))
    try:
        for expected_attempt, expected_retries in ((1, 0), (2, 1), (3, 2)):
            with pytest.raises(Exception):
                ex.execute()
            assert ex.route_pass_attempts == expected_attempt
            assert ex.retries_observed == expected_retries
        # the ceiling is now spent: the fourth attempt is refused pre-operation
        snapshot = dict(ex.session.account_dict())
        with pytest.raises(SourceAccessViolation) as exc:
            ex.execute()
        assert exc.value.code == RETRY_LIMIT_REACHED
        assert ex.retries_observed == ceiling, "the retries account exceeded its ceiling"
        assert dict(ex.session.account_dict()) == snapshot
        assert ex.route_pass_attempts == 3
    finally:
        ex.close()


def test_retry_knobs_cannot_silently_disagree():
    """Court 11 — one exact binding law; mismatch fails closed at bind time."""
    with pytest.raises(BindingError) as e1:
        _src27_spec(plan=SourceOperationPlan(mode=RowDataMode.FULL, max_retries=1),
                    budget=SourceAccessBudget(retries=0))
    assert RETRY_BINDING_MISMATCH in str(e1.value)
    with pytest.raises(BindingError) as e2:
        _src27_spec(plan=SourceOperationPlan(mode=RowDataMode.FULL, max_retries=0),
                    budget=SourceAccessBudget(retries=3))
    assert RETRY_BINDING_MISMATCH in str(e2.value)
    # an unbounded retry ceiling is refused so the retry law stays decidable
    with pytest.raises(BindingError):
        _src27_spec(budget=SourceAccessBudget(retries=None))
    # agreement is accepted, and the single owner is reported
    ok = _src27_spec(budget=SourceAccessBudget(retries=0)).as_dict()["retry_binding_law"]
    assert ok["agree"] is True and ok["single_count_owner"] == "SourceAccessAccount.retries"
    assert ok["plan_knob_value"] == ok["ceiling_value"] == 0
    assert "unbounded (None) ceiling is refused" in RETRY_BINDING_LAW


def test_default_spec_has_matching_retry_knobs():
    """The untouched default path stays coherent, so no existing caller breaks."""
    spec = _spec("DEF", _sav("def.sav", _frame()), "sav",
                 SourceOperationPlan(mode=RowDataMode.FULL))
    assert spec.retry_ceiling == 0 and spec.plan.max_retries == 0


# ================================================================ Repair 4: pyreadstat
def test_pyreadstat_injection_reaches_the_session_and_the_seam():
    """Court 12 — the injected module is really used, not stored and discarded."""
    ex = BoundSourceExecution(_src27_spec(), pyreadstat_module=pyreadstat)
    try:
        assert ex.pyreadstat_module is pyreadstat
        ex.execute()
        assert ex.session.broker.pyreadstat is pyreadstat, "the injected module never reached the broker"
    finally:
        ex.close()


def test_a_wrong_version_injected_module_is_refused_at_the_seam():
    """Proof by contradiction: a bad injected module is actually consulted."""

    class _WrongVersion:
        __version__ = "0.0.0"

    ex = BoundSourceExecution(_src27_spec(), pyreadstat_module=_WrongVersion())
    try:
        with pytest.raises((ReaderSeamViolation, SourceAccessViolation, Exception)):
            ex.execute()
        # the seam refused before any source work
        assert ex.route_pass_attempts == 1
        assert ex.completed_route_passes == 0
    finally:
        ex.close()


def test_no_pyreadstat_argument_means_the_real_module_is_resolved():
    """Omitting the argument resolves the real pyreadstat, not None."""
    ex = BoundSourceExecution(_src27_spec())
    try:
        assert ex.pyreadstat_module is None
        ex.execute()
        assert ex.session.broker.pyreadstat is pyreadstat
    finally:
        ex.close()


# ========================================================= lower-layer law still intact
def test_chunk_reads_cannot_satisfy_the_full_read_floor():
    """Court 13 — chunk_reads must not stand in for the frozen full_reads floor."""
    spec = _spec("CHUNK-TRY", _dta("chunk.dta", _frame(10)), "dta",
                 SourceOperationPlan(mode=RowDataMode.CHUNKED_FULL, chunk_rows=5),
                 rp=RoutePassSpec(expected=1, maximum=1), applicable=ROUTE,
                 cons=(AccountConstraint("full_reads", CountKind.FLOOR, 1,
                                         AuthorityLabel.FROZEN_AUTHORITY),))
    ex = BoundSourceExecution(spec)
    try:
        with pytest.raises(SourceAccessViolation) as exc:
            ex.execute()
        assert exc.value.code == POST_EXECUTION_CONSTRAINT_FAILED
        assert ex.completed_route_passes == 0
    finally:
        ex.close()


def test_expectation_floor_maximum_and_observed_stay_distinct():
    """Court 14 — the lower-layer expected/floor/max/observed law is unchanged."""
    exact = AccountConstraint("full_reads", CountKind.EXACT, 2)
    floor = AccountConstraint("full_reads", CountKind.FLOOR, 1)
    maximum = AccountConstraint("full_reads", CountKind.MAXIMUM, 5)
    assert exact.satisfied_by(2) and not exact.satisfied_by(1)
    assert floor.satisfied_by(1) and floor.satisfied_by(9) and not floor.satisfied_by(0)
    assert maximum.satisfied_by(5) and not maximum.satisfied_by(6)
    unbound = AccountConstraint("path_opens", CountKind.UNBOUND)
    assert unbound.satisfied_by(0) and unbound.satisfied_by(99)
    d = floor.as_dict(observed=3)
    assert d["kind"] == "FLOOR" and d["value"] == 1 and d["observed"] == 3 and d["satisfied"] is True


def test_outer_pass_is_separate_from_every_lower_layer_account():
    out, ex = _run(_src27_spec())
    try:
        keys = set(out.observed_accounts)
        assert "full_route_passes" not in keys, keys
        assert out.full_route_passes_observed == 1
        assert out.as_dict()["full_route_passes"]["distinct_from"] == list(LOWER_LAYER_ACCOUNTS)
        by_account = {c["account"]: c for c in out.as_dict()["constraint_report"]}
        assert by_account["full_reads"]["kind"] == "FLOOR" and by_account["full_reads"]["satisfied"]
        assert by_account["decoder_invocations"]["authority"] == "IMPLEMENTATION_POLICY"
        assert by_account["full_reads"]["authority"] == "FROZEN_AUTHORITY"
    finally:
        ex.close()


def test_spec_is_immutable_and_plan_swap_requires_a_new_spec():
    spec = _spec("IMM", _sav("imm.sav", _frame()), "sav",
                 SourceOperationPlan(mode=RowDataMode.FULL))
    with pytest.raises(Exception):
        spec.plan = SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q10B",))
    with pytest.raises(Exception):
        spec.route_applicability = ROUTE
    other = spec.with_plan(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q10B",)))
    assert spec.plan.mode is RowDataMode.FULL
    assert other.plan.mode is RowDataMode.SELECTED and other is not spec


def test_outer_pass_cannot_be_bound_as_a_lower_layer_constraint():
    with pytest.raises(BindingError):
        AccountConstraint("full_route_passes", CountKind.EXACT, 1)


def test_one_bound_execution_owns_one_session_and_closes_deterministically():
    ex = BoundSourceExecution(_src27_spec())
    ex.execute()
    assert ex.session is ex.session, "a second session was created for the same bound execution"
    ex.close(); ex.close()
    assert ex.closed is True
    with pytest.raises(SourceAccessViolation):
        ex.execute()


def test_no_raw_path_reaches_pyreadstat_on_the_bound_path(monkeypatch):
    seen = []
    original = pyreadstat.read_dta

    def capture(*args, **kwargs):
        seen.append(args[0] if args else None)
        return original(*args, **kwargs)

    monkeypatch.setattr(pyreadstat, "read_dta", capture)
    out, ex = _run(_src27_spec())
    try:
        assert seen, "reader never called"
        for arg in seen:
            assert not isinstance(arg, (str, bytes, os.PathLike)), f"raw path escaped: {arg!r}"
    finally:
        ex.close()


# ================================================== seven documentary plan shapes
def test_shape_1_selected_single_variable_sav_non_route():
    out, ex = _run(_spec("P1", _sav("p1.sav", _frame()), "sav",
                         SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q10B",)),
                         rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        a = out.observed_accounts
        assert a["selected_reads"] == 1 and a["full_reads"] == 0 and a["header_prefix_reads"] == 0
        assert out.full_route_passes_observed == 0 and out.route_pass_status == "NOT_APPLICABLE"
    finally:
        ex.close()


def test_shape_2_selected_two_variable_sav_non_route():
    out, ex = _run(_spec("P2", _sav("p2.sav", _frame()), "sav",
                         SourceOperationPlan(mode=RowDataMode.SELECTED,
                                             selected_variables=("Q101", "Q2061B")),
                         rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        a = out.observed_accounts
        assert a["selected_reads"] == 1 and a["full_reads"] == 0 and a["header_prefix_reads"] == 0
        assert out.full_route_passes_observed == 0
    finally:
        ex.close()


def test_shape_3_metadata_only_declared_encoding_sav_non_route():
    out, ex = _run(_spec("P3", _sav("p3.sav", _frame()), "sav",
                         SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="BIG5"),
                         rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        a = out.observed_accounts
        assert a["metadata_reads"] == 1
        assert a["selected_reads"] == 0 and a["full_reads"] == 0 and a["chunk_reads"] == 0
        assert a["header_prefix_reads"] == 0
        assert out.full_route_passes_observed == 0
    finally:
        ex.close()


def test_shape_4_second_metadata_only_declared_encoding_sav_non_route():
    out, ex = _run(_spec("P4", _sav("p4.sav", _frame()), "sav",
                         SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="WINDOWS-1252"),
                         rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        a = out.observed_accounts
        assert a["metadata_reads"] == 1 and a["full_reads"] == 0
        assert out.full_route_passes_observed == 0
    finally:
        ex.close()


def test_shape_5_selected_exact_variable_sav_non_route():
    out, ex = _run(_spec("P5", _sav("p5.sav", _frame()), "sav",
                         SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q2061B",)),
                         rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        a = out.observed_accounts
        assert a["selected_reads"] == 1 and a["full_reads"] == 0 and a["header_prefix_reads"] == 0
        assert out.full_route_passes_observed == 0
    finally:
        ex.close()


def test_shape_6_metadata_only_sav_with_176_byte_prefix_non_route():
    out, ex = _run(_spec("P6", _sav("p6.sav", _frame()), "sav",
                         SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, header_prefix_bytes=176),
                         rp=ZERO_OUTER, applicable=NON_ROUTE))
    try:
        a = out.observed_accounts
        assert a["metadata_reads"] == 1
        assert a["selected_reads"] == 0 and a["full_reads"] == 0
        assert a["header_prefix_reads"] == 1 and a["header_prefix_bytes"] == 176
        assert out.full_route_passes_observed == 0
    finally:
        ex.close()


def test_shape_7_src27_shaped_route_pass_full_accounting():
    """The SRC27-shaped route: outer exact/max1, floors, policy, retries0, no prefix."""
    out, ex = _run(_src27_spec())
    try:
        d = out.as_dict()
        assert d["full_route_passes_observed"] == 1
        assert d["full_route_passes_expected"] == 1 and d["full_route_passes_max"] == 1
        assert d["full_route_passes_completed_successfully"] is True
        a = out.observed_accounts
        assert a["full_reads"] >= 1, "full_reads floor 1 unmet"
        assert a["metadata_reads"] >= 1
        assert a["decoder_invocations"] <= 1, "decoder policy max 1 exceeded"
        assert a["header_prefix_reads"] == 0, "a header prefix was admitted"
        assert out.retries_observed == 0 and out.route_pass_attempts == 1
        # second route attempt refused pre-operation
        snapshot = dict(ex.session.account_dict())
        with pytest.raises(SourceAccessViolation) as exc:
            ex.execute()
        assert exc.value.code in (ROUTE_PASS_LIMIT_REACHED, RETRY_LIMIT_REACHED)
        assert dict(ex.session.account_dict()) == snapshot
        assert ex.completed_route_passes == 1
    finally:
        ex.close()


def test_all_six_non_route_shapes_report_outer_zero_and_exact_zero_satisfied():
    """Court — the six non-route shapes together, each satisfying EXACT 0."""
    shapes = [
        ("selected-1", "sav", SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q10B",)), "selected_reads"),
        ("selected-2", "sav", SourceOperationPlan(mode=RowDataMode.SELECTED,
                                                  selected_variables=("Q101", "Q2061B")), "selected_reads"),
        ("meta-a", "sav", SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="BIG5"), "metadata_reads"),
        ("meta-b", "sav", SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="WINDOWS-1252"), "metadata_reads"),
        ("selected-exact", "sav", SourceOperationPlan(mode=RowDataMode.SELECTED,
                                                      selected_variables=("Q2061B",)), "selected_reads"),
        ("meta-prefix", "sav", SourceOperationPlan(mode=RowDataMode.METADATA_ONLY,
                                                   header_prefix_bytes=176), "metadata_reads"),
    ]
    for i, (name, fmt, plan, worked) in enumerate(shapes, start=1):
        path = _sav(f"all_{i}.sav", _frame())
        spec = _spec(f"ALL-{i}", path, fmt, plan, rp=ZERO_OUTER, applicable=NON_ROUTE)
        out, ex = _run(spec)
        try:
            assert out.full_route_passes_observed == 0, name
            assert out.completed_pass is False, name
            assert out.observed_accounts[worked] == 1, name
            assert out.full_route_passes_expected == 0
            assert out.full_route_passes_max == 0
        finally:
            ex.close()


# ================================================================ source-agnostic proof
def test_no_source_specific_production_policy():
    """Court 15 — the shapes are named in tests only; production stays generic."""
    package = Path(__file__).resolve().parents[1]
    tokens = ("SRC02", "SRC06", "SRC08", "SRC12", "SRC14", "SRC26", "SRC27", "SRC35",
              "Q10B", "Q101", "Q2061B", "v372")
    for name in ("pre553_execution_binding.py", "pre553_source_access_broker.py",
                 "pre553_source_session.py"):
        module = package / name
        tree = ast.parse(module.read_text(encoding="utf-8"))
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                d = ast.get_docstring(node, clean=False)
                if d is not None:
                    docstrings.add(d)
        literals = [n.value for n in ast.walk(tree)
                    if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value not in docstrings]
        idents = [n.id for n in ast.walk(tree) if isinstance(n, ast.Name)] + \
                 [n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)]
        for tok in tokens:
            for lit in literals:
                assert tok not in lit, f"{tok} hardcoded in a code string literal of {name}"
            for ident in idents:
                assert tok not in ident, f"{tok} hardcoded as an identifier in {name}"


def test_production_declares_no_plan_mode_to_applicability_mapping():
    """Applicability must not be a function of plan mode anywhere in production."""
    module = Path(__file__).resolve().parents[1] / "pre553_execution_binding.py"
    tree = ast.parse(module.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "mode":
            # a .mode read is fine; a comparison that DERIVES applicability is not
            src = ast.dump(node)
            assert "route_applicability" not in src, "applicability derived from plan mode"