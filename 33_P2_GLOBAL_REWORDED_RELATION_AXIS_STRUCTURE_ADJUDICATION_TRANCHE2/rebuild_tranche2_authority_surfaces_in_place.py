#!/usr/bin/env python3
"""Rebuild tranche-2 CSV/JSON authority surfaces inside an extracted v13 handoff.

This uses only section 32 plus the SOURCE_* files delivered in section 33.
It does not alter restart controls, DOCX files, top-level manifests, or live pipeline code.
Run verify_handoff_v13.py afterward.
"""
from __future__ import annotations
import importlib.util, re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
HIST=HERE/'build_p2_global_reconciliation_tranche2.py'
spec=importlib.util.spec_from_file_location('historical_tranche2_builder',HIST)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
mod.V13=ROOT;mod.S33=HERE;mod.S32=ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
def local_ids():
    out=[]
    for line in (HERE/'SOURCE_high_precision_121_candidate_listing.txt').read_text(encoding='utf-8').splitlines():
        m=re.match(r'^(\d{3})\t([^\t]+)',line)
        if m: out.append((int(m.group(1)),m.group(2)))
    assert len(out)==121
    return out
mod.parse_high_precision_ids=local_ids
exact,axis=mod.build_exact_target()
sem,q2=mod.build_semantic_rulings()
sr,sm=mod.build_structures()
anom,overlay=mod.build_anomaly_overlay()
bridge=mod.build_bridge_v2(overlay)
mod.build_sidecar_contract()
mod.section_validation(exact,axis,sem,q2,sr,sm,anom,bridge)
print({'status':'PASS','exact':len(exact),'semantic':len(sem),'structures':len(sr),'member_rows':len(sm),'anomalies':len(anom),'bridge':len(bridge)})
