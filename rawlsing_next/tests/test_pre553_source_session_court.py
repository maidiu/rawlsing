"""HQ199 — governed source-session / accounting owner courts.

Twelve focused source-free courts proving the commissioned semantics. Synthetic
carriers only; no real survey source is opened.

No source-specific plan truth is asserted anywhere in this file. The plans under
test are caller-bound and generic.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next.pre553_physical_decoder import decode_in_session, decode_sav
from rawlsing_next.pre553_source_access_broker import (
    SourceAccessBroker,
    SourceAccessBudget,
    SourceAccessViolation,
)
from rawlsing_next.pre553_source_session import (
    GovernedSourceSession,
    RowDataMode,
    SessionPlanError,
    SourceOperationPlan,
)

CARRIERS = Path(tempfile.mkdtemp(prefix="hq199-court-"))


def _sav(name: str, frame: pd.DataFrame, **kw) -> str:
    p = CARRIERS / name
    pyreadstat.write_sav(frame, str(p), **kw)
    return str(p)


def _dta(name: str, frame: pd.DataFrame) -> str:
    p = CARRIERS / name
    pyreadstat.write_dta(frame, str(p))
    return str(p)


def _frame(rows: int = 20) -> pd.DataFrame:
    return pd.DataFrame({"A": [float(i) for i in range(rows)], "B": list("abcdefghij" * 2)[:rows]})


# --------------------------------------------------------------- 1
def test_c1_one_session_owns_one_physical_open_across_all_operations():
    """1: several operations inside one session share exactly one physical open."""
    path = _sav("c1.sav", _frame())
    with GovernedSourceSession(source_entry_key="K1", path=path, source_format="sav") as s:
        s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
        s.run(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("A",)))
        s.run(SourceOperationPlan(mode=RowDataMode.FULL))
        a = s.account_dict()
        assert a["path_opens"] == 1, a
        assert a["decoder_invocations"] == 3, a
        assert a["logical_views"] > a["decoder_invocations"], a


# --------------------------------------------------------------- 2
def test_c2_decoder_invocations_is_one_after_one_decode():
    """2: one decode entry yields decoder_invocations == 1."""
    path = _sav("c2.sav", _frame())
    with GovernedSourceSession(source_entry_key="K2", path=path, source_format="sav") as s:
        s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
        assert s.account_dict()["decoder_invocations"] == 1


# --------------------------------------------------------------- 3
def test_c3_max_one_rejects_second_decode_before_any_second_operation():
    """3: capped at 1, a second entry is refused with NO account movement."""
    path = _sav("c3.sav", _frame())
    s = GovernedSourceSession(source_entry_key="K3", path=path, source_format="sav",
                              budget=SourceAccessBudget(decoder_invocations=1))
    try:
        s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
        before = s.account_dict()
        with pytest.raises(SourceAccessViolation) as exc:
            s.run(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("A",)))
        after = s.account_dict()
        assert exc.value.code == "SOURCE_ACCESS_BUDGET_EXCEEDED"
        for key in ("decoder_invocations", "metadata_reads", "selected_reads",
                    "full_reads", "chunk_reads", "hash_passes", "header_prefix_reads",
                    "path_opens", "reader_invocations"):
            assert after[key] == before[key], f"{key} moved on a refused entry: {before[key]}->{after[key]}"
    finally:
        s.close()


# --------------------------------------------------------------- 4
def test_c4_metadata_only_with_encoding_does_no_row_data_read():
    """4: KEY CORRECTION. A non-null encoding must not force a full read."""
    path = _sav("c4.sav", _frame())
    with GovernedSourceSession(source_entry_key="K4", path=path, source_format="sav") as s:
        out = s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="latin1"))
        a = s.account_dict()
        assert out["plan"]["encoding"] == "latin1"
        assert a["metadata_reads"] == 1, a
        assert a["selected_reads"] == 0, a
        assert a["full_reads"] == 0, a
        assert a["chunk_reads"] == 0, a


# --------------------------------------------------------------- 5
def test_c5_selected_mode_is_one_selected_and_zero_full():
    """5: SELECTED performs metadata binding plus exactly the selected read."""
    path = _sav("c5.sav", _frame())
    with GovernedSourceSession(source_entry_key="K5", path=path, source_format="sav") as s:
        out = s.run(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("B",)))
        a = s.account_dict()
        assert a["selected_reads"] == 1, a
        assert a["full_reads"] == 0, a
        assert a["metadata_reads"] == 1, a
        assert out["selected_ordinals"] == (2,)
        assert list(out["frame"].columns) == ["B"]


# --------------------------------------------------------------- 6
def test_c6_full_mode_is_one_full_and_distinct_from_chunking():
    """6: FULL is its own account and is never confused with CHUNKED_FULL."""
    path = _sav("c6.sav", _frame())
    with GovernedSourceSession(source_entry_key="K6", path=path, source_format="sav") as s:
        s.run(SourceOperationPlan(mode=RowDataMode.FULL))
        a = s.account_dict()
        assert a["full_reads"] == 1, a
        assert a["chunk_reads"] == 0, a
        assert a["selected_reads"] == 0, a
    with GovernedSourceSession(source_entry_key="K6b", path=path, source_format="sav") as s:
        s.run(SourceOperationPlan(mode=RowDataMode.CHUNKED_FULL, chunk_rows=5))
        b = s.account_dict()
        assert b["chunk_reads"] >= 4, b
        assert b["full_reads"] == 0, b


# --------------------------------------------------------------- 7
def test_c7_chunked_full_is_separately_accounted():
    """7: CHUNKED_FULL streams chunks and never touches the full-read account."""
    path = _sav("c7.sav", _frame(20))
    with GovernedSourceSession(source_entry_key="K7", path=path, source_format="sav") as s:
        out = s.run(SourceOperationPlan(mode=RowDataMode.CHUNKED_FULL, chunk_rows=5))
        a = s.account_dict()
        rows = sum(len(f) for f in out["chunk_frames"])
        assert rows == 20, rows
        assert a["chunk_reads"] == 4, a
        assert a["full_reads"] == 0, a
        assert a["path_opens"] == 1, a


# --------------------------------------------------------------- 8
def test_c8_no_admitted_prefix_means_zero_prefix_reads():
    """8: header_prefix_bytes=None admits no prefix access at all."""
    path = _sav("c8.sav", _frame())
    for mode, kw in ((RowDataMode.METADATA_ONLY, {}),
                     (RowDataMode.SELECTED, {"selected_variables": ("A",)}),
                     (RowDataMode.FULL, {})):
        with GovernedSourceSession(source_entry_key=f"K8-{mode.value}", path=path,
                                   source_format="sav") as s:
            s.run(SourceOperationPlan(mode=mode, **kw))
            a = s.account_dict()
            assert a["header_prefix_reads"] == 0, (mode, a)
            assert a["header_prefix_bytes"] == 0, (mode, a)


# --------------------------------------------------------------- 9
def test_c9_explicit_prefix_is_one_operation_of_that_size():
    """9: an admitted prefix size yields exactly one operation of that size."""
    path = _sav("c9.sav", _frame())
    with GovernedSourceSession(source_entry_key="K9", path=path, source_format="sav") as s:
        s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, header_prefix_bytes=176))
        a = s.account_dict()
        assert a["header_prefix_reads"] == 1, a
        assert a["header_prefix_bytes"] == 176, a


# --------------------------------------------------------------- 10
def test_c10_close_is_deterministic_on_normal_and_exceptional_paths():
    """10: close is idempotent and runs on the exception path via the context manager."""
    path = _sav("c10.sav", _frame())

    s = GovernedSourceSession(source_entry_key="K10", path=path, source_format="sav")
    s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
    s.close(); s.close()
    assert s.closed is True
    with pytest.raises(SourceAccessViolation):
        s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))

    # exceptional path: the context manager still closes
    s2 = GovernedSourceSession(source_entry_key="K10b", path=path, source_format="sav")
    with pytest.raises(RuntimeError):
        with s2:
            s2.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
            raise RuntimeError("induced failure")
    assert s2.closed is True
    assert s2.broker._open.closed is True

    # the incidence closes the session it owns
    with GovernedSourceSession(source_entry_key="K10c", path=path, source_format="sav") as s3:
        inc = decode_in_session(s3, SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
        inc.close_source_access()
        assert s3.closed is True


# --------------------------------------------------------------- 11
def test_c11_reader_bytes_limiter_remains_intact_under_the_session():
    """11: the byte ceiling still refuses before consuming beyond it."""
    path = _sav("c11.sav", _frame())
    need_holder = {}

    probe = GovernedSourceSession(source_entry_key="K11p", path=path, source_format="sav")
    probe.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
    need_holder["n"] = probe.account_dict()["reader_bytes"]
    probe.close()

    n = need_holder["n"]
    for cap, expect_refusal in ((n, False), (n - 1, True), (16, True)):
        s = GovernedSourceSession(source_entry_key=f"K11-{cap}", path=path, source_format="sav",
                                  budget=SourceAccessBudget(reader_bytes=cap))
        try:
            s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
            refused = False
        except SourceAccessViolation as exc:
            refused = True
            assert exc.code == "READER_BYTES_LIMIT_EXCEEDED"
        a = s.account_dict()
        assert a["reader_bytes"] <= cap, (cap, a)
        assert refused is expect_refusal, (cap, refused)
        s.close()


# --------------------------------------------------------------- 12
def test_c12_no_raw_path_reaches_pyreadstat_on_either_path(monkeypatch):
    """12: no source path string is passed to the reader on either decode path."""
    seen = []
    original = pyreadstat.read_sav

    def capture(*args, **kwargs):
        seen.append(args[0] if args else None)
        return original(*args, **kwargs)

    monkeypatch.setattr(pyreadstat, "read_sav", capture)
    path = _sav("c12.sav", _frame())

    with GovernedSourceSession(source_entry_key="K12", path=path, source_format="sav") as s:
        s.run(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("A",),
                                  header_prefix_bytes=176))
    inc = decode_sav(path)
    inc.close_source_access()

    assert seen, "reader was never called"
    for arg in seen:
        assert not isinstance(arg, (str, bytes, os.PathLike)), f"raw path escaped: {arg!r}"


# --------------------------------------------------------------- extras
def test_x1_plan_validation_refuses_incoherent_plans_before_any_access():
    with pytest.raises(SessionPlanError):
        SourceOperationPlan(mode=RowDataMode.SELECTED)
    with pytest.raises(SessionPlanError):
        SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("A", "A"))
    with pytest.raises(SessionPlanError):
        SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, selected_variables=("A",))
    with pytest.raises(SessionPlanError):
        SourceOperationPlan(mode=RowDataMode.CHUNKED_FULL)
    with pytest.raises(SessionPlanError):
        SourceOperationPlan(mode=RowDataMode.FULL, chunk_rows=5)
    with pytest.raises(SessionPlanError):
        SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, header_prefix_bytes=-1)


def test_x2_decoder_and_reader_invocations_are_distinct_accounts():
    path = _sav("x2.sav", _frame(20))
    with GovernedSourceSession(source_entry_key="X2", path=path, source_format="sav") as s:
        s.run(SourceOperationPlan(mode=RowDataMode.CHUNKED_FULL, chunk_rows=5))
        a = s.account_dict()
        assert a["decoder_invocations"] == 1, a
        assert a["reader_invocations"] == a["metadata_reads"] + a["chunk_reads"], a
        assert a["reader_invocations"] > a["decoder_invocations"], a
        basis = s.aggregate_receipt()["measurement_basis"]
        assert "decoder_invocations" in basis and "reader_invocations" in basis


def test_x3_no_source_specific_constants_are_embedded_in_the_plan_module():
    """The plan must stay generic: no SRCxx policy may be hardcoded in CODE.

    The scan deliberately ignores docstrings and comments, because this module's
    own prose NAMES those sources precisely to record that it does not encode
    their plans. A naive substring scan would flag that disclaimer as a violation.
    """
    import ast as _ast

    src = (Path(__file__).resolve().parents[1] / "pre553_source_session.py").read_text(encoding="utf-8")
    tree = _ast.parse(src)

    docstrings = set()
    for node in _ast.walk(tree):
        if isinstance(node, (_ast.Module, _ast.ClassDef, _ast.FunctionDef, _ast.AsyncFunctionDef)):
            doc = _ast.get_docstring(node, clean=False)
            if doc is not None:
                docstrings.add(doc)

    code_strings = [
        n.value for n in _ast.walk(tree)
        if isinstance(n, _ast.Constant) and isinstance(n.value, str) and n.value not in docstrings
    ]
    identifiers = [
        n.id for n in _ast.walk(tree) if isinstance(n, _ast.Name)
    ] + [
        n.attr for n in _ast.walk(tree) if isinstance(n, _ast.Attribute)
    ]

    tokens = ("SRC02", "SRC06", "SRC08", "SRC12", "SRC14", "SRC26", "SRC27", "SRC35")
    for tok in tokens:
        for lit in code_strings:
            assert tok not in lit, f"{tok} appears in a non-docstring string literal"
        for ident in identifiers:
            assert tok not in ident, f"{tok} appears as an identifier"
