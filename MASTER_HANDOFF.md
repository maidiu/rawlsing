# Rawlsing v41 Multipart Recovery Master Handoff

## What this package is

This is the complete handoff of every Rawlsing artifact physically available after the execution sandbox reset, distributed across three independently openable ZIP files.

It contains:

- the full cumulative P2 and P3 architecture history;
- the source-complete executable P3A v40 tree through section 62;
- the extracted offline PostgreSQL/Linux runtime kit;
- original transfer archives and provenance;
- explicit recovery records for the lost P3C sections 63–80;
- multipart manifests, hashes, and verification tooling;
- a full project explainer and exact resume guide.

It does not contain the vanished P3C Git objects, decision JSON, cumulative manifests, or PostgreSQL databases. Those objects must not be inferred from the narrative recovery ledger.

## Current authority boundary

Last recorded persistent P3C state:

- release: R52;
- Git commit: `68c3114acad3366380a5e83c0480802dfef6e511`;
- adjudication decisions: 139;
- canonical families: 108;
- canonical revisions: 134;
- resolved pair obligations: 326;
- original candidates remaining: 2.

R53 reached 142 decisions and 111 families on a disposable clone, but was never promoted. It is test evidence, not authority.

The remaining original candidate was `P3CAND-000273`, the mixed direct/constructed prayer attachment.

## Correct resume sequence

1. Extract all three corrected ZIPs into one folder.
2. Run `python verify_multipart_handoff.py` from the package root.
3. Read `00_RECOVERY_START_HERE/README_FIRST.md` and `CURRENT_STATE.json`.
4. Search for an external R52 Git worktree/database copy.
5. If found, verify it against the recorded counts before resuming.
6. If not found, rebuild P3A from the source-complete v40 base and rerun P3C independently.
7. Reproduce R52, independently reconstruct and promote R53, then resolve `P3CAND-000273`.
8. Complete P3C closure before generating canonical non-GSS J-family authority and proceeding to V550J → V551J → V552J.

## Historical controls

The inherited `00_START_HERE/` directory is preserved for history. Its v35 instructions are superseded by the recovery controls in `00_RECOVERY_START_HERE/` and by this file.
