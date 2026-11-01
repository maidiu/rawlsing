# Exact reviewer response — five defects

## D1 — 174-file R3 extension omitted

**Reviewer defect:** additive patch added only nine files; clean stage had 466
files and no `c12_guard`.

**Repair:** the packet now installs the full immutable 640-file candidate tree
from `8d958529…` / tree `5394e33e…`, not the nine-file delta. The clean stage
contains all **174/174** `rrif_r3_extension` files and `first_consumer_cli.py`.
No R3 test was removed or re-scoped.

**Assertion:** `verify_packet.py` reports `actual=640`,
`r3_extension_files=174`, `listed=639`, `unlisted=[]`.

## D2 — 638-entry preimage omitted CLI and extension

**Reviewer defect:** preimage listed 638 files; actual candidate had 640; it
omitted `first_consumer_cli.py` and all 174 extension files.

**Repair:** new
`candidate/receiving_packet/RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json` lists
**639/640** files (excludes only itself), including the CLI and every extension
file. The source ID is the immutable candidate commit/tree, not a self-hash.
`joined/source_identity.py` now computes actual-vs-listed sets and fails on
missing or unlisted files; the updated test checks the same.

**Assertion:** `audit_candidate_preimage` returns `files=639`,
`unlisted_files=[]`; the test derives `len(actual)-1` rather than a stale 638.

## D3 — apply.sh accepted lookalike base

**Reviewer defect:** apply.sh checked only `joined/session.py`.

**Repair:** `verify_r2_base.py` checks exact 459-file R2 tree, exact
`SOURCE_MANIFEST.json` SHA-256
`7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`,
exactly 444 vendor rows and every vendored Git blob. `apply.sh` calls it before
extracting or writing anything. A R2 manifest byte change returns exit 3 with
459 files unchanged.

**Assertion:** `r2_base_verify.json` PASS; `badbase_stop.txt` STOP before write.

## D4 — unsafe rollback

**Reviewer defect:** `git checkout --` + `git clean -fd` could delete unrelated
untracked files.

**Repair:** `rollback.sh` replaces only
`SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2` with the exact R2 base
from `598d9e9e…`; it uses no `git clean`, reset, checkout, branch deletion or
force. It verifies the restored 459-file base and 444 vendor rows.

**Assertion:** `rollback.txt` exit 0, 459 files, exact manifest hash.

## D5 — tests/consumer not run on clean PRE-MAIN base

**Reviewer defect:** 20 R2 tests passed, but E/R3/CLI failed on clean stage
because extension was absent.

**Repair:** clean PRE-MAIN-derived stage at `8e44ca9c…` now runs:

- 20/20 R2;
- 9/9 R3;
- 6/6 E;
- first consumer exit 0
  `PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT`.

**Assertion:** `junit/r2.xml`, `junit/r3.xml`, `junit/e.xml`; first-consumer
receipt `64a9c171…`.

## Receiving recommendation

**Selective receiving ready for owner review:** install only the exact packet
into an owner-selected isolated sourcefree path after verifying the R2 base
precondition. **No automatic PREMAIN merge.** If no owner-selected live consumer
is named, the packet remains `SOURCEFREE_TEST_ONLY_READY_FOR_OWNER_RECEIVING`.

## Holds retained

`OWNER_ANCHOR_REQUIRED`; C9 actor `C9_SOURCE_MISSING`; C9/C12 owner migration
required; CP-A5 separate root; native C8/C9/C12/CP-A5 false; native person false;
no CAN/ADP/SCI05/Pyat/human A5; no production adoption.
