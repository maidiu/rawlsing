# SOROK RRIF-E F1 — EXACT RECEIVING PACKET REPAIR

**Status:** sourcefree/test-only receiving packet ready for owner review; not PRE-MAIN adoption.
**Branch:** `agent/sorok-rrif-e-exact-receiver-packet-fix-20261031-r1`.
**Dispatch:** `d7df4da4f159313b31981796b9f1ebcd91bfd8be`.
**Tested PRE-MAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29` (read-only).
**Review:** `1198691534c050c19c7c874454b54f99011006c4` — `REVISE_EXACT_RECEIVING_DEFECT`.

## Before / fix / after

**Before:** the nine-file additive packet produced a 466-file stage, omitted all 174 `rrif_r3_extension` files, listed 638 preimage files (missing `first_consumer_cli.py`), accepted a lookalike R2 base, and recommended unsafe `git clean -fd` rollback. The clean stage could not run E/R3/first consumer.

**Fix:** install the exact immutable 640-file candidate tree (`8d958529…`) over the verified 459-file R2 base; add a 639-entry self-excluded preimage including CLI and 174 extension files; make source-identity and tests detect unlisted files; verify exact R2 manifest/rows/vendor blobs/file set before writing; replace rollback with exact R2 restoration only.

**After:** clean PRE-MAIN-derived stage has 640 files, 639 preimage entries, 174 extension files and CLI; **20 R2 + 9 R3 + 6 E tests pass**, first consumer exits 0 with expected partial status; wrong base/missing extension/extra file/unsafe rollback negatives fail or restore exactly.

## Engineering

**PASS** for the corrected receiving packet at sourcefree scope. Full candidate tree and clean-stage tests reproduced; packet base and preimage checks fail closed; rollback restored 459 exact R2 files.

## Scientific

**HOLD.** No native C8/C9/C12, CAN/ADP/SCI05, Pyat, C11, human A5 or native person. C9 actor remains `C9_SOURCE_MISSING`; C12 repair is self-consistency only; external owner anchor remains `OWNER_ANCHOR_REQUIRED`.

## Authority

**HOLD.** No PRE-MAIN merge, production adoption, owner signature, worker relaunch, Programma or native authority. Packet is `SOURCEFREE_TEST_ONLY_READY_FOR_OWNER_RECEIVING`.

## Exact receiving outcome

- clean stage: `/tmp/rrif-e-clean-f1` (detached at `8e44ca9c…`; no live PRE-MAIN write);
- 459-file R2 base restored and verified;
- 640-file candidate installed from immutable Git tree;
- 639/640 preimage (self excluded; CLI + 174 extension included);
- 20 R2 + 9 R3 + 6 E + first consumer green;
- old additive-only packet still STOPs before R2;
- unsafe/incorrect rollback text removed; tested rollback restores exact R2.

## Still owner/HQ

Owner must choose a sourcefree receiving path and accept the packet; if no live receiver is named, retain `SOURCEFREE_TEST_ONLY_READY_FOR_OWNER_RECEIVING`. No production merge follows from this green stage. A same independent reviewer may do one exact-delta continuation; no broad new review.

## DONE

- Complete candidate closure and 639-entry preimage.
- Exact R2 base validation and lookalike STOP.
- Full candidate packet, safe rollback, clean-stage tests and first consumer.
- Exact reviewer response to all five defects.
- Source hashes, JUnit and command receipts.

## REMAINING

- Owner-selected receiving path/acceptance.
- Current live caller/consumer (none proven).
- Native C9 actor, C11 weld, external C12 anchor, human A5 and science authority.

## FINAL SHA

`FINAL_SHA: reported in the terminal push readback after non-force commit/push; a file cannot contain the SHA of the commit that contains it.`

**TERMINAL:** `RRIF_E_F1_PACKET_COMPLETE__640_FILES__639_PREIMAGE__20_9_6_GREEN__FIRST_CONSUMER_PASS__OWNER_RECEIVING_HOLD`.
