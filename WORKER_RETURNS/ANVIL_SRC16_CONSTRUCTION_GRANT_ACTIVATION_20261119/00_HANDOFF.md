# SRC16 construction authorization activation

## Decision recorded

In this HQ thread the user answered:

> **"for GSS 1972, yes"**

to the question whether they authorize local read of the exact files in the
decision packet solely to build C11 estates.

This activates **SRC16 only**:

- Source: `GSS1972.sav`
- Source SHA-256: `e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204`
- Rows: 1,613
- Physical slots/columns: 216
- Bytes: 1,647,241
- Host: `USER_LOCAL_MAC`
- Purpose: `FULL_SRC16_ORIGINAL_C11_CONSTRUCTION_ONLY`
- Consumer: `EXISTING_PRE553_SOURCE_BACKED_C11`
- Extent: `EXACT_FILE`
- Retention: `LOCAL_RUNTIME_ONLY`
- Scope: `ALL_216_PHYSICAL_SLOTS__C11_CONSTRUCTION_ONLY__NO_Q2`
- Currentness: `CURRENT_GRANTED`; revocation `NONE_RECORDED`

## Materialized private custody

Private operative grant, resolver binding and exact resolver are under a 0700
directory with 0600 files:

`/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil_src16_construction_grant_20261119`

Files:

- `SRC16.construction.grant.json`
- `SRC16.construction.binding.json`
- `SRC16.exact_resolver.py`

No source was opened, statted, hashed, decoded or run. No source path is in Git.

## Resolver exercise

Metadata-only:

- Exact SRC16 request: **admitted**, `CURRENT_GRANTED`
- Other source request: **refused**, `EXACT_REQUEST_MISMATCH`
- Analysis-purpose request: **refused**, `EXACT_REQUEST_MISMATCH`
- Incorrect-scope request: **refused**, `EXACT_REQUEST_MISMATCH`

The private exact resolver implements the existing canonical
`SourceReadRequest` / `IssuedSourceReadDecision` contract. The existing shared
SRC04 resolver is source-pinned and cannot itself admit SRC16; see the shared
runner gap.

## Shared SQLite-free runner

**No, SRC16 is not already executable in the shared SQLite-free runner.** The
existing `sqlite_free_witness.py` hardcodes SRC04 config/trust/q217/runtime
overlay and has no SRC16 entry.

Smallest concrete gap: add generic source-specific binding injection to the
existing `sqlite_free_single_pass`/`sqlite_free_witness` path. This is a runner
integration gap, not a reason to create a per-wave writer.

## Remaining scope

- Existing SRC04/SRC17: unchanged.
- SRC16: privately activated, not run.
- Remaining pending drafts: **32**.
- Q2/analysis/science/export: none issued.
- No actual source run by worker.

Public evidence in this return is metadata-only; private grant inputs remain out
of Git.
