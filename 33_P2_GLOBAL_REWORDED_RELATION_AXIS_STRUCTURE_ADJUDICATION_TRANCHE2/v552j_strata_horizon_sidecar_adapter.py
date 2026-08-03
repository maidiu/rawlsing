#!/usr/bin/env python3
"""Read-only V552→V552J strata/horizon sidecar adapter proposal.

This module is not installed into the live pipeline. It performs cardinality-checked
pass-through only and refuses to synthesize missing strata or horizon values.
"""
from __future__ import annotations
import pandas as pd
FIELDS = ['stratum_id', 'stratum_label', 'strata_relevance', 'strata_path', 'conditional_strata_weights', 'horizon_affordance', 'horizon_type', 'horizon_scope', 'horizon_openness', 'horizon_reach', 'horizon_valence', 'horizon_sustaining_power']
KEY_PREFERENCES = [("question_implementation_id",),("source","wave","question_id"),("source","wave","source_variable_code")]

def _clean(v):
    if pd.isna(v): return ""
    return str(v).strip()

def select_join_key(packet: pd.DataFrame, sidecar: pd.DataFrame):
    for keys in KEY_PREFERENCES:
        if all(k in packet.columns and k in sidecar.columns for k in keys):
            if all(packet[k].map(_clean).ne("").any() and sidecar[k].map(_clean).ne("").any() for k in keys):
                return list(keys)
    raise ValueError("no supported join key present on both packet and sidecar")

def enrich(packet: pd.DataFrame, sidecar: pd.DataFrame) -> pd.DataFrame:
    keys=select_join_key(packet,sidecar)
    s=sidecar.copy()
    dup=s.duplicated(keys,keep=False)
    if dup.any():
        raise ValueError("duplicate sidecar join keys: "+repr(s.loc[dup,keys].to_dict("records")[:10]))
    keep=keys+[f for f in FIELDS if f in s.columns]
    out=packet.merge(s[keep],how="left",on=keys,suffixes=("","__sidecar"),validate="many_to_one")
    for f in FIELDS:
        sf=f+"__sidecar"
        if sf not in out.columns: continue
        if f not in packet.columns:
            out[f]=out[sf]
        else:
            left=out[f].map(_clean); right=out[sf].map(_clean)
            conflict=left.ne("") & right.ne("") & left.ne(right)
            if conflict.any(): raise ValueError(f"conflicting non-empty values for {f}")
            out[f]=out[f].where(left.ne(""),out[sf])
        out.drop(columns=[sf],inplace=True)
    out["strata_horizon_sidecar_status"]="V552_AUTHORITATIVE_PASS_THROUGH"
    return out
