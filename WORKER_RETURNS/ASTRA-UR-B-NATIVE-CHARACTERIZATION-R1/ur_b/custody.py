"""Actual S1 consumer-byte custody contrast."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pyreadstat

from rawlsing_next.pre553_physical_decoder import decode_sav
from ur_b.s1 import build
from ur_b.s1_queries import run


def mutate_s1(path):
    path = Path(path)
    original = path.read_bytes()
    df, meta = pyreadstat.read_sav(str(path))
    df.loc[0, "A"] = 1.0 - float(df.loc[0, "A"])
    tmp = path.with_suffix(".mut.sav")
    pyreadstat.write_sav(df, str(tmp),
                         column_labels=["A condition", "B condition", "Y outcome",
                                        "G coordinate", "Synthetic weight",
                                        "All-missing Z"])
    os.replace(tmp, path)
    return original


def restore(path, original):
    Path(path).write_bytes(original)


def compare(path):
    before = build(path)
    before_out = run(before)
    before_fact = before_out["results"]["DIST_A_RAW"].facts[0]
    before_cells = [(c.row_ordinal, c.variable_name, c.raw_value)
                    for c in before["incidence"].iter_cells()
                    if c.row_ordinal == 1 and c.variable_name == "A"]
    original = mutate_s1(path)
    try:
        after_out = run(before)
        after_fact = after_out["results"]["DIST_A_RAW"].facts[0]
        after_cells = [(c.row_ordinal, c.variable_name, c.raw_value)
                       for c in before["incidence"].iter_cells()
                       if c.row_ordinal == 1 and c.variable_name == "A"]
        return {
            "source_sha": before["incidence"].source_sha256,
            "row1_a_before": before_cells,
            "row1_a_after": after_cells,
            "fact_before": before_fact.ref.content_hash,
            "fact_after": after_fact.ref.content_hash,
            "cells_before": before_fact.target_topology.get(
                "complete_cell_semantic_projection"),
            "cells_after": after_fact.target_topology.get(
                "complete_cell_semantic_projection"),
            "same_source_identity": True,
            "changed_values_under_old_identity": (before_cells != after_cells
                                                  and before_fact.ref.content_hash
                                                  != after_fact.ref.content_hash),
        }
    finally:
        restore(path, original)
