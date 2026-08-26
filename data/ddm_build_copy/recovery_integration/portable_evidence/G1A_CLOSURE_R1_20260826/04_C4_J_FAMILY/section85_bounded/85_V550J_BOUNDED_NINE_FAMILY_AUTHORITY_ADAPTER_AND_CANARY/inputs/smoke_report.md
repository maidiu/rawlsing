# Universality Functional Smoke Report

**Run:** 20260729T074523Z
**Scope:** explicit 36-wave allowlist
**Base spine:** V550 → V551 → V552
**Full-chain acceptance:** V550J → V551J → V552J is required for every wave unless a diagnostic base-only mode was explicitly selected

## Summary

- Waves attempted: 9
- Base spines passed: 0
- Full V550→V552J chains passed: 0
- Waves passed at the selected acceptance boundary: 0
- Waves failed: 9

## Preflight

- Passed: True
- Blockers: 0
- Warnings: 0

## Failures

- Afrobarometer R1: v552_process —  int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:119: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_count": int(component_index.get("source_intensity_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:120: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_count": int(component_index.get("canonical_signed_component_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,

- Arab Barometer I: v552_gate — missing_v552_input_provenance_manifest
- Asian Barometer W1: v552_process —  int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:119: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_count": int(component_index.get("source_intensity_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:120: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_count": int(component_index.get("canonical_signed_component_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,

- EVS 1981: v552_process — v552_nonzero_exit
- GSS 2010: v552_gate — missing_v552_input_provenance_manifest
- Latinobarómetro 1995: v552_process —  int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:119: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_count": int(component_index.get("source_intensity_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:120: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_count": int(component_index.get("canonical_signed_component_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,

- LiTS 2006: v552_process —  int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:119: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_count": int(component_index.get("source_intensity_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:120: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_count": int(component_index.get("canonical_signed_component_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,

- South Asia W1: v552_process —  int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:119: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_count": int(component_index.get("source_intensity_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:120: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_count": int(component_index.get("canonical_signed_component_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,

- WVS W1: v552_process —  int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4251: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/ddm_v552_structural.py:4252: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:119: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "source_intensity_zero_count": int(component_index.get("source_intensity_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,
/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/compile_v552_structural_ddm.py:120: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  "canonical_signed_zero_count": int(component_index.get("canonical_signed_component_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,


## Readiness

**NOT READY.** Only 0/9 waves passed functional gates. 9 attempted waves remain blocked.
