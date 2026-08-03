# Rawlsing v41 Multipart Recovery Handoff

## Start here

This package is a **three-ZIP recovery handoff**. Extract all three corrected ZIP archives into the same destination folder, then run:

```bash
python verify_multipart_handoff.py
```

The governing recovery controls are in:

```text
00_RECOVERY_START_HERE/
```

Read in this order:

1. `00_READ_THIS_FIRST_MULTIPART.md`
2. `00_RECOVERY_START_HERE/README_FIRST.md`
3. `00_RECOVERY_START_HERE/CURRENT_STATE.json`
4. `00_RECOVERY_START_HERE/EXACT_RESUME_POINT.md`
5. `00_RECOVERY_START_HERE/FULL_EXPLAINER_AND_RESUME_GUIDE.md`
6. `MASTER_HANDOFF.md`

## Critical warning

The inherited `00_START_HERE/` directory and its v35 controls are preserved as historical project artifacts. They are **not** the current entrypoint and do not govern this recovery package.

## Current status

- Package classification: `COMPLETE_AVAILABLE_ARTIFACT_RECOVERY_HANDOFF_NOT_P3C_AUTHORITY_CHECKPOINT`
- Executable source-complete base: sections 00–62, P3A v40.
- P3C sections 63–80: recovery records only.
- Last recorded persistent state: R52, commit `68c3114acad3366380a5e83c0480802dfef6e511`.
- R53: tested on a disposable clone, never promoted.
- Last unresolved original candidate: `P3CAND-000273`.

Do not import the section 63–80 narrative ledgers as authority. Recover the real R52 Git/database state if it exists; otherwise rebuild P3C from the executable v40 base.
