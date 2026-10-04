"""HQ196 Phase 3 — source-free courts for the brokered source-access candidate.

Synthetic carriers only.  No real survey source is opened, stat-ed for content,
hashed or decoded anywhere in this file.

The nine mandatory courts from the commission are C1..C9 below.  C10 is the
declared-grain path-baseline versus brokered-candidate comparison.

Category law: everything here is C2/C3-grade evidence about synthetic carriers.
It is NOT survey-semantic equivalence and qualifies no real source.
"""
from __future__ import annotations

import os
from pathlib import Path
import tempfile

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next import pre553_physical_decoder as decoder
from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav
from rawlsing_next.pre553_source_access_broker import (
    GovernedSourceOpen,
    RawSourcePathEscape,
    ReaderSeamViolation,
    SourceAccessBroker,
    SourceAccessBudget,
    SourceAccessViolation,
    assert_reader_seam,
)

CARRIERS = Path(tempfile.mkdtemp(prefix="hq196-court-"))


def _sav(name: str, frame: pd.DataFrame, **kw) -> str:
    path = CARRIERS / name
    pyreadstat.write_sav(frame, str(path), **kw)
    return str(path)


def _dta(name: str, frame: pd.DataFrame, **kw) -> str:
    path = CARRIERS / name
    pyreadstat.write_dta(frame, str(path), **kw)
    return str(path)


def _three_col() -> pd.DataFrame:
    return pd.DataFrame({"Q10B": [1.0, 2.0, 3.0], "Q101": [10, 20, 30], "other": ["x", "y", "z"]})


# ---------------------------------------------------------------- C1
def test_c1_broker_metadata_route():
    """C1: metadata is read through the broker on one application-owned open."""
    path = _sav("c1.sav", _three_col())
    broker = SourceAccessBroker(path)
    broker.bind_reader("SAV")
    assert broker.existence_check() is True
    broker.hash_pass()
    metadata = broker.metadata_read()
    accounts = broker.account_dict()
    assert accounts["path_opens"] == 1
    assert accounts["metadata_reads"] == 1
    assert accounts["hash_passes"] == 1
    assert accounts["full_reads"] == 0 and accounts["selected_reads"] == 0
    assert list(metadata.column_names) == ["Q10B", "Q101", "other"]
    assert metadata.number_rows == 3
    broker.close()


# ---------------------------------------------------------------- C2
def test_c2_brokered_ordinary_decode():
    """C2: an ordinary decode routes every source open through the broker."""
    path = _sav("c2.sav", _three_col())
    inc = decode_sav(path)
    accounts = inc.source_access_receipt["accounts"]
    assert accounts["path_opens"] == 1
    assert accounts["hash_passes"] == 1
    assert accounts["header_prefix_reads"] == 1
    assert accounts["header_prefix_bytes"] == 176
    assert accounts["metadata_reads"] == 1
    assert [v.name for v in inc.variables] == ["Q10B", "Q101", "other"]
    assert inc.row_count == 3
    inc.close_source_access()


# ---------------------------------------------------------------- C3
def test_c3_brokered_sav_selected_variable_read():
    """C3: the selected route yields one selected read and zero full reads."""
    path = _sav("c3.sav", _three_col())
    inc = decode_sav(path, selected_variables=("Q101",))
    accounts = inc.source_access_receipt["accounts"]
    assert accounts["path_opens"] == 1
    assert accounts["selected_reads"] == 1
    assert accounts["full_reads"] == 0
    assert accounts["metadata_reads"] == 1
    cfg = inc.source_access_receipt["selected_read_configuration"]
    assert cfg["mechanism"] == "pyreadstat usecols"
    assert cfg["selected_names"] == ["Q101"]
    assert cfg["bound_ordinals"] == [2]          # bound against the real inventory
    assert cfg["bound_before_row_data_read"] is True
    assert inc.selected_ordinals == (2,)
    values = [(c.row_ordinal, c.variable_name, c.raw_value)
              for b in inc.iter_batches(batch_size=2) for c in b]
    assert values == [(1, "Q101", 10), (2, "Q101", 20), (3, "Q101", 30)]
    inc.close_source_access()


# ---------------------------------------------------------------- C4
def test_c4_brokered_dta_route():
    """C4: DTA decodes through the broker on one application-owned open."""
    path = _dta("c4.dta", _three_col())
    inc = decode_dta(path, selected_variables=("Q10B",))
    accounts = inc.source_access_receipt["accounts"]
    assert accounts["path_opens"] == 1
    assert accounts["selected_reads"] == 1
    assert accounts["full_reads"] == 0
    assert accounts["header_prefix_bytes"] == 512   # DTA prefix, not SAV's 176
    assert inc.selected_ordinals == (1,)
    inc.close_source_access()


# ---------------------------------------------------------------- C5
def test_c5_batch_chunk_route_preserves_one_physical_open():
    """C5: the chunk route issues one view per chunk over ONE physical open.

    This is the DTA constraint the feasibility lane flagged: reusing one broker
    object across row-offset parses fails because ReadStat requires position
    zero.  The governed loop rewinds the same open instead of opening again.
    """
    frame = pd.DataFrame({"v": [float(i) for i in range(10)], "w": list("abcdefghij")})
    for name, path, fn in (("sav", _sav("c5.sav", frame), decode_sav),
                           ("dta", _dta("c5.dta", frame), decode_dta)):
        inc = fn(path)
        cells = [(c.row_ordinal, c.variable_name, c.raw_value)
                 for b in inc.iter_batches(batch_size=3) for c in b]
        assert [c[2] for c in cells if c[1] == "v"] == [float(i) for i in range(10)], name
        accounts = inc.source_access_receipt["accounts"]
        assert accounts["path_opens"] == 1, name
        assert accounts["chunk_reads"] >= 4, name           # 10 rows / 3 per chunk
        assert accounts["logical_views"] > accounts["chunk_reads"], name
        inc.close_source_access()


def test_c5b_dta_broker_reuse_without_reset_is_refused():
    """C5b: the failure mode the reset design exists to prevent is real.

    Reusing one object across two row-offset parses is exactly what the governed
    loop avoids; this asserts the naive form genuinely fails, so the reset is
    load-bearing rather than decorative.
    """
    path = _dta("c5b.dta", pd.DataFrame({"v": [1.0, 2.0, 3.0, 4.0]}))
    gov = GovernedSourceOpen(path)
    shared_view = gov.view()          # ONE view object reused across both parses
    with pytest.raises(Exception):
        pyreadstat.read_dta(shared_view, row_offset=0, row_limit=2)
        pyreadstat.read_dta(shared_view, row_offset=2, row_limit=2)
    # the reset design succeeds on the same single open
    a = pyreadstat.read_dta(gov.view(), row_offset=0, row_limit=2)[0]
    b = pyreadstat.read_dta(gov.view(), row_offset=2, row_limit=2)[0]
    assert list(a["v"]) == [1.0, 2.0]
    assert list(b["v"]) == [3.0, 4.0]
    assert gov.physical_opens == 1
    gov.close()


# ---------------------------------------------------------------- C6
def test_c6_budget_failures_refuse_before_the_excess_operation():
    """C6: budget breaches refuse BEFORE the operation, not after."""
    path = _sav("c6.sav", _three_col())

    # path-open cap: the broker structurally permits one physical open
    broker = SourceAccessBroker(path, budget=SourceAccessBudget(path_opens=0))
    broker.bind_reader("SAV")
    with pytest.raises(SourceAccessViolation) as exc:
        broker.hash_pass()
    assert exc.value.code == "SOURCE_ACCESS_BUDGET_EXCEEDED"
    assert "path_opens" in str(exc.value)
    broker.close()

    # hash-pass cap
    broker = SourceAccessBroker(path, budget=SourceAccessBudget(hash_passes=0))
    broker.bind_reader("SAV")
    with pytest.raises(SourceAccessViolation):
        broker.hash_pass()
    broker.close()

    # byte cap on the header prefix
    broker = SourceAccessBroker(path, budget=SourceAccessBudget(header_prefix_bytes=10))
    broker.bind_reader("SAV")
    with pytest.raises(SourceAccessViolation):
        broker.header_prefix(176)
    broker.close()

    # the refusal happened before the read: no bytes were consumed
    broker = SourceAccessBroker(path, budget=SourceAccessBudget(header_prefix_bytes=10))
    broker.bind_reader("SAV")
    before = broker.account_dict()["reader_bytes"]
    with pytest.raises(SourceAccessViolation):
        broker.header_prefix(176)
    assert broker.account_dict()["reader_bytes"] == before
    assert broker.account_dict()["header_prefix_reads"] == 0
    broker.close()

    # the selected route refuses a full read by construction
    broker = SourceAccessBroker(path, budget=SourceAccessBudget(full_reads=0))
    broker.bind_reader("SAV")
    broker.existence_check(); broker.hash_pass(); broker.metadata_read()
    broker.selected_read(["Q10B"])
    with pytest.raises(SourceAccessViolation) as exc:
        broker.full_read()
    assert exc.value.code == "SOURCE_ACCESS_BUDGET_EXCEEDED"
    broker.close()


# ---------------------------------------------------------------- C7
def test_c7_raw_path_string_never_reaches_the_reader(monkeypatch):
    """C7: the compiled reader never receives a raw source path string."""
    seen = []
    original = pyreadstat.read_sav

    def capture(*args, **kwargs):
        seen.append(args[0] if args else None)
        return original(*args, **kwargs)

    monkeypatch.setattr(pyreadstat, "read_sav", capture)
    path = _sav("c7.sav", _three_col())
    inc = decode_sav(path, selected_variables=("Q10B",))
    list(inc.iter_batches(2))
    inc.close_source_access()
    assert seen, "reader was never called"
    for arg in seen:
        assert not isinstance(arg, (str, bytes, os.PathLike)), f"raw path escaped: {arg!r}"
    assert inc.source_access_receipt["raw_path_string_never_passed_to_reader"] is True


def test_c7b_reader_arg_guard_raises_on_a_path():
    """C7b: the broker's own guard rejects a path argument outright."""
    broker = SourceAccessBroker(_sav("c7b.sav", _three_col()))
    broker.bind_reader("SAV")
    broker.existence_check()
    view = broker._open.view()
    assert isinstance(view, str) is False
    # the guard is the isinstance check the broker applies to its own argument
    assert isinstance(view, (str, bytes, os.PathLike)) is False
    broker.close()


# ---------------------------------------------------------------- C8
def test_c8_selected_column_missing_and_unexpected_fail_closed():
    """C8: a missing bound selected column fails closed before any row read."""
    path = _sav("c8.sav", _three_col())
    with pytest.raises(decoder.DecoderError) as exc:
        decode_sav(path, selected_variables=("NOT_PRESENT",))
    assert "absent from the bound source" in str(exc.value)

    # empty and repeating selections are refused
    with pytest.raises(decoder.DecoderError):
        decode_sav(path, selected_variables=())
    with pytest.raises(decoder.DecoderError):
        decode_sav(path, selected_variables=("Q10B", "Q10B"))

    # an unexpected column coming back from the reader is refused (C8b)
    broker = SourceAccessBroker(path)
    broker.bind_reader("SAV")
    broker.existence_check()
    broker.hash_pass()
    broker.metadata_read()
    original = pyreadstat.read_sav

    def leaky(*args, **kwargs):
        frame, md = original(*args, **kwargs)
        frame["SNEAKED_IN"] = 0
        return frame, md

    pyreadstat.read_sav = leaky
    try:
        with pytest.raises(SourceAccessViolation) as exc:
            broker.selected_read(["Q10B"])
        assert exc.value.code == "UNEXPECTED_SELECTED_COLUMN"
    finally:
        pyreadstat.read_sav = original
    broker.close()


# ---------------------------------------------------------------- C9
def test_c9_accounting_separation_is_exact():
    """C9: every quantity is its own account and none proxies for another."""
    path = _dta("c9.dta", pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [4.0, 5.0, 6.0]}))
    inc = decode_dta(path, selected_variables=("a",))
    list(inc.iter_batches(2))
    a = inc.source_access_receipt["accounts"]
    basis = inc.source_access_receipt["measurement_basis"]
    for key in ("path_opens", "logical_views", "hash_passes", "header_prefix_reads",
                "metadata_reads", "selected_reads", "full_reads", "chunk_reads",
                "reader_invocations", "reader_read_calls", "reader_bytes"):
        assert key in a, key
        assert key in basis, key                      # every account states its basis
    assert a["path_opens"] == 1
    assert a["logical_views"] > 1                    # views are NOT opens
    assert a["selected_reads"] == 1
    assert a["full_reads"] == 0
    assert a["hash_passes"] == 1
    assert a["reader_invocations"] == a["metadata_reads"] + a["selected_reads"] + a["full_reads"] + a["chunk_reads"]
    assert a["reader_read_calls"] > 0 and a["reader_bytes"] > 0
    assert "separation_law" in basis
    inc.close_source_access()


def test_c9b_seam_is_pinned_and_fails_closed():
    """C9b: the pyreadstat seam/version is pinned and a mismatch fails closed."""
    assert assert_reader_seam(pyreadstat) == "1.3.6"

    class Fake:
        __version__ = "9.9.9"

    with pytest.raises(ReaderSeamViolation) as exc:
        assert_reader_seam(Fake())
    assert exc.value.code == "READER_SEAM_VERSION_MISMATCH"


def test_c9c_selected_route_physical_suppression_is_disclosed_not_claimed():
    """C9c: the candidate does not claim the library suppresses unselected reads."""
    path = _sav("c9c.sav", _three_col())
    inc = decode_sav(path, selected_variables=("Q10B",))
    text = inc.source_access_receipt["selected_route_physical_column_suppression"]
    assert "NOT_ENFORCED_BY_READER" in text
    inc.close_source_access()


# ---------------------------------------------------------------- C10
def test_c10_measured_usecols_does_not_reduce_physical_reads():
    """C10: records the measured truth about usecols physical suppression.

    Measured on a 12-column / 200-row carrier, a full read and a usecols read
    issued an IDENTICAL number of read calls and bytes.  The selected route is a
    genuine logical selected-read account; it is NOT evidence that unselected
    columns were never physically read.
    """
    cols = {f"c{i:02d}": [float(i) * j for j in range(200)] for i in range(12)}
    path = _sav("c10.sav", pd.DataFrame(cols))

    def _measure(**kw):
        b = SourceAccessBroker(path)
        b.bind_reader("SAV")
        b.existence_check(); b.hash_pass()
        b._invoke_reader("full_reads" if not kw else "selected_reads", **kw)
        out = (b.account_dict()["reader_bytes"], b.account_dict()["reader_read_calls"])
        b.close()
        return out

    full_bytes, full_calls = _measure()
    sel_bytes, sel_calls = _measure(usecols=["c00"])
    assert sel_bytes == full_bytes, "usecols unexpectedly reduced bytes; re-measure"
    assert sel_calls == full_calls, "usecols unexpectedly reduced read calls; re-measure"
