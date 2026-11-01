# SOROK RRIF-E F2 — FULL R2 BLOB GATE

**Status:** `ALL_459_R2_BLOBS_VERIFIED_BEFORE_WRITE__NONVENDOR_TAMPER_FAILS_CLOSED__35_CLEAN_STAGE_TESTS_GREEN__FIRST_CONSUMER_PARTIAL`

**F2 launch:** `agent/sorok-rrif-e-f2-full-r2-blob-check-20261101-r1@83be0a8c676242c920e0c414695f9dcda1c476e3`

**F1 base:** `1973d28ed4ba4c9e58c9d96fbe358445dddc929c`; F1 branch/commit remains immutable.

**Independent review:** `review/sorok-rrif-e-f1-packet-delta-terminal-20261101-r1@86afe1845022fcf3cdd9e8b5ca4136ddb661336c`, verdict `REVISE_ONE_EXACT_PACKET_DEFECT`.

**PRE-MAIN cut:** `8e44ca9c751049d65e6def47600b5c073ee04b29`; read-only, unchanged at start and end.

**R2 base:** `598d9e9eaba5143950c63317705fd09104fbf463`, tree `1161ce3d990ca78fe1b97c915dc86e559f17236b`, 459 regular files, 444 vendor rows, manifest SHA-256 `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`.

**Full E candidate:** `8d9585296ff264b947559f4a78f49f73ca45e53a`, tree `5394e33ec81766a4ee891b0d58007f24ac1d1303`; unmodified.

## Before

F1 `verify_r2_base.py` checked the manifest SHA, 444 vendor blobs and the 459 path names. It did not hash the 15 non-vendor files. A single comment appended to `joined/session.py`, with the manifest and all paths unchanged, passed F1 and F1 `apply.sh` proceeded.

## After

The corrected verifier derives the complete R2 tree with `git ls-tree -r -z` at `598d9e9e...`, including mode, type, Git blob id and path. It walks the destination without following symlinks, accepts only regular files, rejects type/mode mismatches, and compares the Git-compatible SHA-1 blob of every actual file's bytes against the complete 459-file tree. The existing manifest SHA and 444-row checks remain.

The exact code delta is one file:

- `WORKER_RETURNS/SOROK-RRIF-E-RECEIVER-PACKET-FIX-F1-R1/candidate/receiving_packet/verify_r2_base.py`
- before SHA-256: `18dbd92fcd4289ba01e59a337ada86cbc84ef2f7b021a5d1dfec2da2bb9a0fba`
- after SHA-256: `029fd404a96388a2c3b74d2f38858916f8ad8ba2c66013a4f453c8c7784f1cc3`
- exact diff: `receipts/verify_r2_base.diff`, SHA-256 `d8bde48671fadff0201929c6a0d9519297dbd902ebae31b06b61dab8849aa0fa`

No change was made to `apply.sh`, `rollback.sh`, `verify_packet.py`, the R2 base, the 640-file E candidate, its preimage, or candidate semantics.

## Results

| Requirement | Result |
|---|---|
| exact 459-file R2 base | verifier exit 0, `ok:true`, expected/actual 459, vendor 444 |
| non-vendor `joined/session.py` tamper, manifest and paths unchanged | verifier exit 1, `R2_BLOB_MISMATCH:joined/session.py` |
| same tamper through `apply.sh` | exit 3, `RRIF_E_BASE_R2_IDENTITY_MISMATCH`, destination unchanged, 459 files |
| vendor file tamper | verifier nonzero |
| symlink substitution | verifier nonzero, `R2_SYMLINK` |
| restore exact 459 bytes | verifier exit 0 |
| clean PRE-MAIN-derived stage | 640 files, 639 preimage entries, 174 extension files, CLI present |
| 20 R2 + 9 R3 + 6 E | 20/20, 9/9, 6/6 passed |
| first consumer | exit 0, expected partial status |
| rollback | exact 459 R2 restored; sibling sentinel unchanged |

Regression test and receipts are under this F2 return folder; JUnit files record 1 F2 gate test plus 20 R2, 9 R3 and 6 E tests.

## Scope

This is a sourcefree TEST_ONLY receiving fix. No PRE-MAIN merge, production adoption, owner signature, native grant, actor/C8/C9/C11/C12/CP-A5 science claim, Pyat or PROGRAMMA change is made. `OWNER_ANCHOR_REQUIRED`, `C9_SOURCE_MISSING`, C9/C12 owner migration required, CP-A5 separate root and `native_person=false` remain.

The final pushed SHA is reported in the terminal push readback; a file cannot contain the SHA of the commit that contains it.
