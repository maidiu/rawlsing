# PROGRAMMA_DELTA — P2 protected-base receiving rehearsal R1

**Delta ID:** `SOROK-P2-PROTECTED-BASE-RECEIVING-REHEARSAL-20261105-R1`
**Class:** bounded engineering receiving compatibility rehearsal, not review, acceptance or merge permission.
**Protected base:** `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`.
**P2 candidate:** `25d40806d15516b7f7ffa04f47bc651022c6f2b0`.
**Guide PR699:** `5b569b130379ee012936e2f6517fc7c49ddcbdea`.

## Delta

- Composed a checkout-local disposable snapshot: full protected base + exact 625-file product25d allowlist + 9-file guide699 overlay.
- Composite tree: `3894541eeac3e2133a3823252c65f04252e21e93`; 634 changes vs protected base, exactly the allowlist.
- Merge-tree diagnostics: product `57dbdca8`, guide `a6a8233`, combined `b3a82908`; no conflicts. The combined tree's 4 guide-return files were excluded from the selected composite.
- Guide canonical verifier PASS at the snapshot.
- One cold first-consumer CLI sequence passed from snapshot imports: interval → later-event/opportunity → zero encounters → explicit do-help → exit → cold blocked action → local return → UNKNOWN → verify.
- Import origins all under the snapshot; privacy walker clean; typed UNKNOWN and source contracts preserved.
- No collisions, schema/root/import incompatibility observed.

## Not changed

No protected merge, PR697 action, product/guide modification, source-branch drift, PROGRAMMA working-file edit, native/science/human/B grant or acceptance.

## Holds at declared cut

Later repair and independent interval closure are `RUNNING_AT_DECLARED_CUT`; later-event `76fdb624` remains original `REVISE` with public-CLI limits. This rehearsal is not final acceptance.

## Smallest next receiving step

After running reviews close, a competent PRE-MAIN owner may evaluate selective receiving of exact `25d40806` plus the 9-file guide699 overlay using the published allowlist/composite tree. No further engineering action follows from this rehearsal.
