# READ THIS FIRST — Rawlsing v41 Multipart Recovery Handoff

This handoff is distributed as **three ordinary, independent ZIP archives**.

## Assemble the handoff

1. Download all three corrected ZIP files.
2. Create one empty destination folder.
3. Extract ZIP 1, ZIP 2, and ZIP 3 into that same destination folder.
4. If asked whether identical shared control files should be replaced, allow the overwrite; the duplicated controls are byte-identical.
5. Open:

   `Rawlsing_J_Family_Authority_Strategy_Handoff_v41_MULTIPART_20260802/README_FIRST.md`

6. From that package root, run:

   `python verify_multipart_handoff.py`

Do **not** concatenate the ZIP files. Each is independently openable.

## Current authority boundary

This is a recovery handoff, not a complete P3C authority checkpoint.

- Sections 00–62: source-complete executable v40 base.
- Sections 63–80: recovery records only; the original generated P3C code, decision objects, Git objects, and PostgreSQL databases were lost in the sandbox reset.
- Last recorded persistent P3C state: R52, commit `68c3114acad3366380a5e83c0480802dfef6e511`.
- R53 was tested on a disposable clone but never promoted.
- The last unresolved original candidate was `P3CAND-000273`.

The governing orientation is `00_RECOVERY_START_HERE/README_FIRST.md`. The inherited `00_START_HERE/` directory is historical and must not be used as the current resume point.
