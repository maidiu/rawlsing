# R0-01 Vozhd Review

- **Worker:** R0-01
- **PR:** #39
- **Branch:** `agent/vozhd-dva-r0-01-v553-v554`
- **Reviewed head:** `22925e020c3f7fe6464ca0b0c6f3d489ff1e1d2f`
- **Disposition:** `RETURN_FOR_FIX`

## Scope verdict

Scope and architectural direction are correct. The worker kept the repair on the V553 consumer side and did not reopen V552J. The canonical direction for `POSTG5-004` is accepted: V553 must consume current V552J input/handoff artifacts rather than recreating the obsolete `v552j_structural_handoff_packet.json` interface.

## Code verdict

The new canonical adapter is not yet acceptable at the trust boundary. `_read_parquet()` currently converts missing/read/corruption failure to an empty DataFrame, while `surface_present` may remain true from path existence and uses an OR across index paths. This can misclassify corrupt or incomplete canonical input as merely empty/present.

Required correction:
1. distinguish missing, unreadable/corrupt, schema-invalid, and valid-empty canonical artifacts;
2. fail closed on missing/unreadable/schema-invalid required canonical artifacts;
3. require the canonical V552J artifact set/manifest required by the producer contract rather than path existence alone;
4. add adversarial regression coverage proving incomplete/corrupt/unreadable/schema-invalid canonical indexes cannot be represented as a valid V553 consumer surface;
5. remain entirely V553-side.

## Accepted findings

- `POSTG5-004` is correctly a V553 consumer repair.
- V553 must draw from canonical upstream V552J structural identity/authority rather than regenerate governed identity from convenience labels.
- Broader V553/V554 semantic findings may inform S00/S01 schematic work, but no worker-local ontology is frozen by this review.

## Downstream obligations

The corrected adapter must preserve canonical relation/target/driver/channel/horizon identity and producer authority while refusing to convert integrity failure into semantic emptiness.

## Tests / evidence

Worker-reported syntax and exact-adapter harness evidence was inspected. Additional adversarial integrity tests are required before acceptance. No independent repository pytest run was available through the connector during review.

## Merge decision

Do not merge PR #39 until the narrow fail-closed correction is committed and reviewed. After acceptance, integrate PR #39 before S00 is frozen so the schematic V552J→V553 session starts from the repaired canonical consumer boundary.

## Synchronization

- S00 remains `READY_AFTER_R0_01`.
- S01 and later seams remain blocked by serial schematic sequencing.
- The authoritative worker handoff is the PR #39 Vozhd review comment plus this control-room review file.
