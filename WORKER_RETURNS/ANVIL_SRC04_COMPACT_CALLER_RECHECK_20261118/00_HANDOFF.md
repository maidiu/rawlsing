# SRC04 compact caller recheck — same independent reviewer

## Outcome

**ACCEPT_SCOPED.** The prior caller defects are repaired or bounded; no
consequential launch blocker is present on the exact overlay candidate tree and
carried work-root.

## Exact source

- MEASUREMENT_PREP head: `b3dd74d16c71f9f63b10510af041ec83a1b5c3de`
- Runner manifest SHA-256: `603cce17914b1a9bb6b545d870d914550686f898f91a33ce122a7004e0a0bf98`
- Manifest verified: 56/56 files exact; no bad files.
- `single_pass_handoff.py`: `719fe9574b0e92f69f700a67705ea4f07c32d5731055e7573bc301df613f5f2e`
- `witness_caller.py`: `d574a55676a57cbbc2bd87242802cddd11b2bc63abca76ae86d1681183cb6bac`

## Repairs rechecked

1. **Valid sourcefree resume without source path**
   Baseline and compact sourcefree interrupted/checkpoint paths both resumed
   with `decode_called=false`; both fresh readers opened; roots, manifests,
   counts and all reader payload digests were equal. Compact spool was
   38,855 bytes / 2 files versus baseline 551,124 bytes / 3 files in this rerun.
2. **Invalid sourcefree resume without source path**
   Missing checkpoint refused with `CHECKPOINT_MISSING`; no source decode or
   publication.
3. **Synthetic original-shaped guards**
   Before any spool creation: held refused `CURRENT_NOT_GRANTED`, revoked
   refused `CURRENT_REVOKED`, wrong request refused
   `CURRENT_REQUEST_SCOPE_MISMATCH` (`host`). Config identity was
   `ORIGINAL_SOURCE`; `spool_created=false`, `source_decode_called=false`.
4. **Digest-pin mismatch**
   Raw MEASUREMENT_PREP candidate tree (`801ff416…`) is refused before import
   with `CANDIDATE_SOURCE_HASH_MISMATCH`; pinned expected handoff is `6ab7cb50…`.
5. **Direct producer resume without source path**
   Reproduced `CHECKPOINT_MISSING` rather than the prior `TypeError`; no source
   read.
6. **Compact implementation pin**
   `SINGLE_PASS_SHA = 719fe957…`; the current file matches and is checked
   before import.
7. **Current/revocation guard**
   `witness_caller._grant` calls `_require_current` before producer
   resume/build; `resume_single_pass` calls `_require_current` for
   `ORIGINAL_SOURCE` configs before checkpoint load/publication.
8. **Operator CLI / carried work-root**
   Metadata-only preflight with the exact overlay candidate tree, base config,
   runtime config, candidate patch, binding directory, and carried work-root
   returned `RUNTIME_OVERLAY_QUALIFIED`; `source_path_opened_stat_hashed_decoded=false`;
   request equal; q217 held; 177/3/181 scoped counts.
9. **Disk**
   Current measured free at the carried work-root: 42,577,633,280 B, above the
   26,907,826,727 B startup floor. The stale prior 15.5GB figures were not used.
10. **Run authorization**
    `--mode run` without `--authorized-source-launch` refused with
    `EXPLICIT_SOURCE_LAUNCH_AUTHORIZATION_REQUIRED`; no real run occurred.

## Scoped qualification

The compact worktree's raw candidate tree is still rejected by the pinned
candidate hash. The exact documented overlay candidate tree
(`MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree`) passes
preflight. This is an operator packaging requirement, not a compact payload
defect.

## Boundaries

No original source access or execution. No product edits, no stopped data
access/modification, no wider review, no previous scratch access. Evidence was
produced on fresh sourcefree temp roots and in this OWNER reviewer subtree.
