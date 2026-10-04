"""HQ200 — seven-plan conformance court and bound-execution semantics.

Synthetic SAV/DTA carriers only. No real survey source is opened.

The seven specs below reproduce the documentary source-plan SHAPES. The TESTS may
name those shapes; PRODUCTION may not. A court asserts that production contains no
SRCxx token in code, so the shapes cannot leak into the mechanism.

Authority semantics under test, from the HQ200 adjudication:
  full_route_passes : EXACT 1 / MAX 1
  full_reads        : FLOOR >= 1, ceiling UNBOUND
  decoder_invocations : historical expected UNBOUND; a MAX 1 policy ceiling allowed
                        only when typed as IMPLEMENTATION_POLICY
  path_opens        : historical expected UNBOUND; a one-open ceiling allowed only
                        when typed as IMPLEMENTATION_POLICY
  retries           : MAX 0
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
    AccountConstraint,
    AuthorityLabel,
    BoundExecutionSpec,
    BoundSourceExecution,
    BindingError,
    CountKind,
    LOWER_LAYER_ACCOUNTS,
    POST_EXECUTION_CONSTRAINT_FAILED,
    ROUTE_PASS_LIMIT_REACHED,
    RoutePassSpec,
)
from rawlsing_next.pre553_source_access_broker import (
    SourceAccessBudget,
    SourceAccessViolation,
)
from rawlsing_next.pre553_source_session import RowDataMode, SourceOperationPlan

CARRIERS = Path(tempfile.mkdtemp(prefix="hq200-court-"))


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


def _spec(key, path, fmt, plan, *, rp=None, cons=(), budget=None, note=None):
    return BoundExecutionSpec(
        source_entry_key=key, path=path, source_format=fmt, plan=plan,
        expected_sha256=None,
        budget=budget if budget is not None else SourceAccessBudget(),
        route_pass=rp if rp is not None else RoutePassSpec(),
        constraints=tuple(cons), authority_note=note,
    )


def _run(spec):
    ex = BoundSourceExecution(spec)
    try:
        return ex.execute(), ex
    except Exception:
        ex.close()
        raise


# =============================================================== seven shapes
def test_p1_selected_single_variable_sav():
    """Shape 1 — selected single-variable SAV, no prefix."""
    path = _sav("p1.sav", _frame())
    out, ex = _run(_spec("P1", path, "sav",
                         SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q10B",))))
    a = out.observed_accounts
    assert a["selected_reads"] == 1 and a["full_reads"] == 0, a
    assert a["header_prefix_reads"] == 0, a
    assert a["decoder_invocations"] == 1 and a["path_opens"] == 1, a
    ex.close()


def test_p2_selected_two_variable_sav():
    """Shape 2 — selected two-variable SAV, no prefix."""
    path = _sav("p2.sav", _frame())
    out, ex = _run(_spec("P2", path, "sav",
                         SourceOperationPlan(mode=RowDataMode.SELECTED,
                                             selected_variables=("Q101", "Q2061B"))))
    a = out.observed_accounts
    assert a["selected_reads"] == 1 and a["full_reads"] == 0, a
    assert a["header_prefix_reads"] == 0, a
    ex.close()


def test_p3_metadata_only_declared_encoding_sav():
    """Shape 3 — metadata-only with a declared encoding performs NO row-data read."""
    path = _sav("p3.sav", _frame())
    out, ex = _run(_spec("P3", path, "sav",
                         SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="BIG5")))
    a = out.observed_accounts
    assert a["metadata_reads"] == 1, a
    assert a["selected_reads"] == 0 and a["full_reads"] == 0 and a["chunk_reads"] == 0, a
    assert a["header_prefix_reads"] == 0, a
    ex.close()


def test_p4_second_metadata_only_declared_encoding_sav():
    """Shape 4 — the same shape with a different declared encoding behaves identically."""
    path = _sav("p4.sav", _frame())
    out, ex = _run(_spec("P4", path, "sav",
                         SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="WINDOWS-1252")))
    a = out.observed_accounts
    assert a["metadata_reads"] == 1, a
    assert a["selected_reads"] == 0 and a["full_reads"] == 0, a
    ex.close()


def test_p5_selected_exact_variable_sav():
    """Shape 5 — selected exact-variable SAV, no prefix."""
    path = _sav("p5.sav", _frame())
    out, ex = _run(_spec("P5", path, "sav",
                         SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q2061B",))))
    a = out.observed_accounts
    assert a["selected_reads"] == 1 and a["full_reads"] == 0, a
    assert a["header_prefix_reads"] == 0, a
    ex.close()


def test_p6_metadata_only_sav_with_176_byte_prefix():
    """Shape 6 — metadata-only SAV admitting exactly one 176-byte prefix operation."""
    path = _sav("p6.sav", _frame())
    out, ex = _run(_spec("P6", path, "sav",
                         SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, header_prefix_bytes=176)))
    a = out.observed_accounts
    assert a["metadata_reads"] == 1, a
    assert a["selected_reads"] == 0 and a["full_reads"] == 0, a
    assert a["header_prefix_reads"] == 1, a
    assert a["header_prefix_bytes"] == 176, a
    ex.close()


# =============================================================== SRC27 shape
def _src27_spec():
    """The SRC27-shaped spec. FULL compatibility lane, latin1, outer pass EXACT 1/MAX 1."""
    return _spec(
        "SRC27-SHAPED", _dta("p7.dta", _frame(10)), "dta",
        SourceOperationPlan(mode=RowDataMode.FULL, encoding="latin1"),
        rp=RoutePassSpec(expected=1, maximum=1, token="governed full route pass"),
        cons=(
            # frozen authority
            AccountConstraint("metadata_reads", CountKind.FLOOR, 1, AuthorityLabel.FROZEN_AUTHORITY),
            AccountConstraint("full_reads", CountKind.FLOOR, 1, AuthorityLabel.FROZEN_AUTHORITY),
            # implementation POLICY ceilings, explicitly typed as policy
            AccountConstraint("decoder_invocations", CountKind.MAXIMUM, 1,
                              AuthorityLabel.IMPLEMENTATION_POLICY),
            AccountConstraint("path_opens", CountKind.MAXIMUM, 1,
                              AuthorityLabel.IMPLEMENTATION_POLICY),
            AccountConstraint("retries", CountKind.MAXIMUM, 0, AuthorityLabel.FROZEN_AUTHORITY),
        ),
        budget=SourceAccessBudget(decoder_invocations=1, retries=0),
        note="synthetic reproduction of a documented plan SHAPE; no source key is bound in production",
    )


def test_p7_full_route_pass_exact1_max1_dta():
    """Shape 7 — full declared-encoding DTA with an outer Route-B pass exact/max 1."""
    out, ex = _run(_src27_spec())
    d = out.as_dict()["full_route_passes"]
    assert d["observed"] == 1, d
    assert d["expected"] == 1 and d["expected_status"] == "EXACT", d
    assert d["maximum"] == 1, d
    assert d["completed_successfully"] is True, d
    a = out.observed_accounts
    # full_reads satisfies the supplied FLOOR 1
    assert a["full_reads"] >= 1, a
    assert a["metadata_reads"] >= 1, a
    # decoder MAX 1 policy honoured
    assert a["decoder_invocations"] <= 1, a
    # path opens reported SEPARATELY from the pass and from full reads
    assert a["path_opens"] == 1, a
    assert "full_route_passes" not in a, "outer pass must not be stored as a lower-layer account"
    # all bound constraints satisfied and reported distinctly
    by_account = {c["account"]: c for c in out.as_dict()["constraint_report"]}
    assert by_account["full_reads"]["kind"] == "FLOOR" and by_account["full_reads"]["satisfied"], by_account
    assert by_account["decoder_invocations"]["authority"] == "IMPLEMENTATION_POLICY", by_account
    assert by_account["full_reads"]["authority"] == "FROZEN_AUTHORITY", by_account
    ex.close()


def test_p7b_second_pass_refused_before_any_second_source_operation():
    """A second outer pass is refused with every lower-layer account unmoved."""
    ex = BoundSourceExecution(_src27_spec())
    try:
        ex.execute()
        before = dict(ex.session.account_dict())
        with pytest.raises(SourceAccessViolation) as exc:
            ex.execute()
        assert exc.value.code == ROUTE_PASS_LIMIT_REACHED
        after = dict(ex.session.account_dict())
        assert before == after, {k: (before[k], after[k]) for k in before if before[k] != after[k]}
    finally:
        ex.close()


def test_p7c_chunking_cannot_satisfy_the_full_read_floor():
    """chunk_reads must not stand in for the frozen full_reads floor."""
    spec = _spec("CHUNK-TRY", _dta("p7c.dta", _frame(10)), "dta",
                 SourceOperationPlan(mode=RowDataMode.CHUNKED_FULL, chunk_rows=5),
                 cons=(AccountConstraint("full_reads", CountKind.FLOOR, 1,
                                         AuthorityLabel.FROZEN_AUTHORITY),))
    ex = BoundSourceExecution(spec)
    try:
        with pytest.raises(SourceAccessViolation) as exc:
            ex.execute()
        assert exc.value.code == POST_EXECUTION_CONSTRAINT_FAILED
        assert "full_reads" in str(exc.value)
    finally:
        ex.close()


def test_p7d_outer_pass_is_separate_from_every_lower_layer_account():
    """The outer account is structurally distinct from all named lower layers."""
    spec = _src27_spec()
    out, ex = _run(spec)
    try:
        keys = set(out.observed_accounts)
        assert "full_route_passes" not in keys, keys
        for lower in LOWER_LAYER_ACCOUNTS:
            assert "full_route_passes" != lower
        # the pass count is exposed only on the outcome, and differs from each lower layer
        assert out.full_route_passes_observed == 1
        assert out.as_dict()["full_route_passes"]["distinct_from"] == list(LOWER_LAYER_ACCOUNTS)
    finally:
        ex.close()


# =============================================================== expectation law
def test_expectation_floor_maximum_and_observed_stay_distinct():
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


def test_policy_ceiling_is_not_recorded_as_frozen_authority():
    policy = AccountConstraint("decoder_invocations", CountKind.MAXIMUM, 1,
                               AuthorityLabel.IMPLEMENTATION_POLICY)
    frozen = AccountConstraint("full_reads", CountKind.FLOOR, 1,
                               AuthorityLabel.FROZEN_AUTHORITY)
    assert policy.authority is AuthorityLabel.IMPLEMENTATION_POLICY
    assert frozen.authority is AuthorityLabel.FROZEN_AUTHORITY
    assert policy.as_dict()["authority"] != frozen.as_dict()["authority"]


def test_spec_is_immutable_and_plan_swap_requires_a_new_spec():
    spec = _spec("IMM", _sav("imm.sav", _frame()), "sav",
                 SourceOperationPlan(mode=RowDataMode.FULL))
    with pytest.raises(Exception):
        spec.plan = SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q10B",))
    other = spec.with_plan(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("Q10B",)))
    assert spec.plan.mode is RowDataMode.FULL
    assert other.plan.mode is RowDataMode.SELECTED
    assert other is not spec


def test_outer_pass_cannot_be_bound_as_a_lower_layer_constraint():
    with pytest.raises(BindingError):
        AccountConstraint("full_route_passes", CountKind.EXACT, 1)


def test_spec_validation_refuses_incoherent_specs():
    good = SourceOperationPlan(mode=RowDataMode.FULL)
    with pytest.raises(BindingError):
        BoundExecutionSpec(source_entry_key="", path="x", source_format="sav", plan=good)
    with pytest.raises(BindingError):
        BoundExecutionSpec(source_entry_key="K", path="x", source_format="sav", plan="not a plan")
    with pytest.raises(BindingError):
        BoundExecutionSpec(source_entry_key="K", path="x", source_format="sav", plan=good,
                           constraints=(AccountConstraint("full_reads", CountKind.EXACT, 1),
                                        AccountConstraint("full_reads", CountKind.FLOOR, 1)))
    with pytest.raises(BindingError):
        AccountConstraint("full_reads", CountKind.EXACT)
    with pytest.raises(BindingError):
        AccountConstraint("full_reads", CountKind.UNBOUND, 3)


def test_one_bound_execution_owns_one_session_and_closes_deterministically():
    ex = BoundSourceExecution(_src27_spec())
    ex.execute()
    s1 = ex.session
    assert s1 is ex.session, "a second session was created for the same bound execution"
    ex.close(); ex.close()
    assert ex.closed is True
    with pytest.raises(SourceAccessViolation):
        ex.execute()


def test_failed_first_attempt_is_not_reported_as_a_completed_pass():
    """A pass counts only on success; a failure leaves the completed count at zero."""
    spec = _src27_spec()
    ex = BoundSourceExecution(spec)
    try:
        ex._ensure_session()
        # induce a failure BEFORE the pass completes
        with pytest.raises(Exception):
            ex.session.run(SourceOperationPlan(mode=RowDataMode.SELECTED,
                                               selected_variables=("NOT_A_COLUMN",)))
        assert ex._passes_completed == 0
        assert spec.route_pass.admits(ex._passes_completed) is True
    finally:
        ex.close()


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


def test_production_binding_module_has_no_source_specific_constants():
    """The shapes are named in tests only. Production must stay source-agnostic."""
    module = Path(__file__).resolve().parents[1] / "pre553_execution_binding.py"
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
    # also assert no documented variable name is hardcoded
    for tok in ("SRC02", "SRC06", "SRC08", "SRC12", "SRC14", "SRC26", "SRC27", "SRC35",
                "Q10B", "Q101", "Q2061B", "v372"):
        for lit in literals:
            assert tok not in lit, f"{tok} hardcoded in a code string literal"
        for ident in idents:
            assert tok not in ident, f"{tok} hardcoded as an identifier"
