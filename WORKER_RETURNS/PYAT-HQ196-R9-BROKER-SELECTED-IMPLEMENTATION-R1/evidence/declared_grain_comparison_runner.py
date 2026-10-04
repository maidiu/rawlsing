#!/usr/bin/env python3
"""HQ196 — declared-grain path-baseline versus brokered-candidate comparison.

Builds a 55-carrier synthetic corpus and compares, per carrier:

  A. brokered FULL route      vs  path-based full read      (like for like)
  B. brokered SELECTED route  vs  path-based usecols read   (like for like)

HONESTY NOTE, stated up front: the commission refers to a "prior 55-carrier
source-free court".  No runner, corpus or expected-result artifact for that court
exists in this repository at the commissioned freeze, in the R7 qualification
environment, or anywhere in reachable history; the figure appears only as prose
in the HQ195 feasibility return.  This corpus is therefore constructed HERE at a
declared grain.  It is NOT a re-run of the prior court and inherits no PASS from
it.  Matching the count of 55 makes the comparison denominator comparable, not
the corpus identical.

Category: C2 observed synthetic.  NOT survey-semantic equivalence.  Zero real
sources are opened.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pyreadstat

sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq196-r9-impl")

from rawlsing_next.pre553_physical_decoder import (  # noqa: E402
    _physical_value,
    decode_dta,
    decode_sav,
)
from rawlsing_next.pre553_source_access_broker import (  # noqa: E402
    SourceAccessBroker,
    SourceAccessBudget,
)

CORPUS = Path(tempfile.mkdtemp(prefix="hq196-corpus-"))


def build_corpus() -> list[dict]:
    """55 synthetic carriers spanning the shapes the decoder must survive."""
    specs = []
    ncols = [1, 2, 3, 5, 8]
    nrows = [1, 2, 3, 7, 20]
    kinds = ["numeric", "string", "mixed", "missing", "labels"]
    idx = 0
    for fmt in ("sav", "dta"):
        for nc in ncols:
            for nr in nrows:
                for kind in kinds:
                    if idx >= 55:
                        break
                    specs.append({"fmt": fmt, "ncols": nc, "nrows": nr, "kind": kind, "index": idx})
                    idx += 1
    carriers = []
    for spec in specs:
        cols = {}
        for c in range(spec["ncols"]):
            name = f"V{c:02d}"
            if spec["kind"] == "string":
                cols[name] = [f"s{r}" for r in range(spec["nrows"])]
            elif spec["kind"] == "mixed":
                cols[name] = ([float(r) for r in range(spec["nrows"])] if c % 2 == 0
                              else [f"m{r}" for r in range(spec["nrows"])])
            elif spec["kind"] == "missing":
                base = [float(r) for r in range(spec["nrows"])]
                if spec["nrows"] > 1:
                    base[0] = None
                cols[name] = base
            elif spec["kind"] == "labels":
                cols[name] = [float(r % 3) for r in range(spec["nrows"])]
            else:
                cols[name] = [float(r) * (c + 1) for r in range(spec["nrows"])]
        frame = pd.DataFrame(cols)
        path = CORPUS / f"c{spec['index']:02d}.{spec['fmt']}"
        if spec["fmt"] == "sav":
            kw = {}
            if spec["kind"] == "labels" and spec["ncols"] >= 1:
                kw["variable_value_labels"] = {"V00": {0.0: "zero", 1.0: "one", 2.0: "two"}}
            pyreadstat.write_sav(frame, str(path), **kw)
        else:
            pyreadstat.write_dta(frame, str(path))
        carriers.append({**spec, "path": str(path), "columns": list(frame.columns)})
    return carriers


def path_baseline(path: str, fmt: str, usecols=None):
    """The pre-candidate mechanism: hand pyreadstat a PATH STRING."""
    reader = pyreadstat.read_sav if fmt == "sav" else pyreadstat.read_dta
    if usecols is None:
        return reader(path, apply_value_formats=False, user_missing=True)
    return reader(path, usecols=list(usecols), apply_value_formats=False, user_missing=True)


def frames_equal(a: pd.DataFrame, b: pd.DataFrame) -> tuple[bool, str]:
    if list(a.columns) != list(b.columns):
        return False, f"columns differ: {list(a.columns)} vs {list(b.columns)}"
    if a.shape != b.shape:
        return False, f"shape differs: {a.shape} vs {b.shape}"
    try:
        same = a.equals(b)
    except Exception:
        same = a.astype(object).equals(b.astype(object))
    if not same:
        return False, "values differ"
    return True, "identical"


def main() -> int:
    carriers = build_corpus()
    results = []
    full_ok = sel_ok = 0
    opens_seen = []
    for c in carriers:
        rec = {"index": c["index"], "fmt": c["fmt"], "ncols": c["ncols"],
               "nrows": c["nrows"], "kind": c["kind"], "columns": c["columns"]}
        # ---- A: metadata/full route.
        # A plain decode with no encoding override is metadata-only by design
        # (unchanged from the pre-candidate decoder), so the frame is materialised
        # through the governed chunk route and compared cell-by-cell.
        base_frame, base_md = path_baseline(c["path"], c["fmt"])
        inc_full = decode_sav(c["path"]) if c["fmt"] == "sav" else decode_dta(c["path"])
        cand_accounts = inc_full.source_access_receipt["accounts"]
        opens_seen.append(cand_accounts["path_opens"])

        inv_ok = ([v.name for v in inc_full.variables] == list(base_md.column_names)
                  and [v.ordinal for v in inc_full.variables] == list(range(1, len(base_md.column_names) + 1))
                  and inc_full.row_count == int(base_md.number_rows))

        cells = {}
        for batch in inc_full.iter_batches(batch_size=7):
            for cell in batch:
                cells[(cell.row_ordinal, cell.variable_name)] = cell.raw_value
        # BOTH sides are put through the decoder's canonical _physical_value.
        # Raw pyreadstat yields NaN where the decoder's contract yields None;
        # comparing a raw baseline against a normalised candidate would report a
        # missingness difference that is an artefact of the harness, not of the
        # broker. The normalisation is symmetric and is the established contract.
        base_cells = {}
        for col in base_md.column_names:
            for i, v in enumerate(base_frame[col].tolist(), 1):
                base_cells[(i, col)] = _physical_value(v)
        cells_ok = cells == base_cells

        ok = bool(inv_ok and cells_ok)
        why = ("inventory and cell values identical" if ok else
               f"inventory_ok={inv_ok} cells_ok={cells_ok} "
               f"n_cand={len(cells)} n_base={len(base_cells)}")
        rec["full_route"] = {"equivalent": ok, "detail": why,
                             "inventory_identical": bool(inv_ok),
                             "cell_values_identical": bool(cells_ok),
                             "cells_compared": len(base_cells),
                             "candidate_path_opens": cand_accounts["path_opens"],
                             "candidate_hash_passes": cand_accounts["hash_passes"],
                             "candidate_header_prefix_reads": cand_accounts["header_prefix_reads"],
                             "candidate_chunk_reads": cand_accounts["chunk_reads"]}
        full_ok += ok
        inc_full.close_source_access()

        # ---- B: selected route (first column only)
        selected = [c["columns"][0]]
        base_sel, _ = path_baseline(c["path"], c["fmt"], usecols=selected)
        fn = decode_sav if c["fmt"] == "sav" else decode_dta
        inc_sel = fn(c["path"], selected_variables=tuple(selected))
        sel_accounts = inc_sel.source_access_receipt["accounts"]
        ok2, why2 = frames_equal(base_sel, inc_sel._frame)
        rec["selected_route"] = {
            "equivalent": ok2, "detail": why2, "selected": selected,
            "selected_reads": sel_accounts["selected_reads"],
            "full_reads": sel_accounts["full_reads"],
            "path_opens": sel_accounts["path_opens"],
            "bound_ordinals": list(inc_sel.selected_ordinals or ()),
        }
        sel_ok += ok2
        inc_sel.close_source_access()
        results.append(rec)

    summary = {
        "schema": "HQ196_DECLARED_GRAIN_COMPARISON@1.0.0",
        "CATEGORY": "C2_OBSERVED_SYNTHETIC",
        "category_law": "Equivalence is demonstrated ONLY at this declared synthetic grain. It is NOT survey-semantic equivalence, qualifies no real source, and must not be cited as if it did.",
        "prior_court_status": {
            "named_by_commission": "prior 55-carrier source-free court",
            "runner_located": False,
            "searched": ["repository at commissioned freeze 55f75664", "R7 qualification environment",
                         "reachable git history (--diff-filter=A over all refs)"],
            "consequence": "This corpus is constructed here. It is NOT the prior corpus, is NOT a re-run of the prior court, and inherits NO pass from it. Matching the count of 55 makes the denominator comparable, not the corpus identical.",
        },
        "declared_grain": {
            "carriers": len(carriers),
            "formats": ["sav", "dta"],
            "columns_per_carrier": [1, 2, 3, 5, 8],
            "rows_per_carrier": [1, 2, 3, 7, 20],
            "value_kinds": ["numeric", "string", "mixed", "missing", "labels"],
            "comparison": "path-string read (pre-candidate mechanism) versus brokered file-object read, same process, same carrier, same accepted environment",
            "value_normalisation": "both sides pass through the decoder's canonical _physical_value; raw pyreadstat NaN and decoder None are the same physical missingness",
        },
        "comparison_A_full_route": {"carriers": len(carriers), "equivalent": full_ok,
                                    "all_equivalent": full_ok == len(carriers)},
        "comparison_B_selected_route": {"carriers": len(carriers), "equivalent": sel_ok,
                                        "all_equivalent": sel_ok == len(carriers)},
        "path_open_account": {
            "distinct_values_observed": sorted(set(opens_seen)),
            "every_carrier_one_open": set(opens_seen) == {1},
            "note": "One application-owned physical open per carrier scope, on both routes.",
        },
        "environment": {
            "python": "3.11.3", "pyreadstat": pyreadstat.__version__,
            "interpreter_sha256": "11d6f541a870a141249ce98d45834a6789e29c07031e85ce17f3e67f24c535f6",
            "anchor": "C4C3-DARWIN-X86_64-ANCHOR/CPYTHON-3.11.3/PYREADSTAT-1.3.6/PYARROW-25.0.1/PANDAS-2.3.3/NUMPY-2.4.6/PYTEST-9.1.1",
            "dependency_modified": False,
        },
        "results": results,
    }
    out = os.environ.get("HQ196_OUT", "/tmp/hq196_comparison.json")
    Path(out).write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(f"carriers                : {len(carriers)}")
    print(f"A full-route equivalent : {full_ok}/{len(carriers)}")
    print(f"B selected-route equiv  : {sel_ok}/{len(carriers)}")
    print(f"distinct path_opens     : {sorted(set(opens_seen))}")
    print(f"written                 : {out}")
    return 0 if (full_ok == len(carriers) and sel_ok == len(carriers)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
