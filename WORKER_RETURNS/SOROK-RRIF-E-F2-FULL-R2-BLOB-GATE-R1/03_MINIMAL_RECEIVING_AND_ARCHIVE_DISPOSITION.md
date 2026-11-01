# Minimal receiving and archive disposition

## Receiving file

The corrected pre-write gate is exactly this one file on the F2 branch:

`WORKER_RETURNS/SOROK-RRIF-E-RECEIVER-PACKET-FIX-F1-R1/candidate/receiving_packet/verify_r2_base.py`

SHA-256: `029fd404a96388a2c3b74d2f38858916f8ad8ba2c66013a4f453c8c7784f1cc3`.

It authenticates all 459 R2 Git blobs, modes, types and paths against `598d9e9eaba5143950c63317705fd09104fbf463`, rejects symlinks/non-regular nodes, and runs before `apply.sh` writes. The immutable F1 branch remains `1973d28ed4ba4c9e58c9d96fbe358445dddc929c`; F2 carries only this receiving correction plus F2 evidence.

## Owner receiving option

If an owner selects a live sourcefree receiver:

- use an isolated owner-controlled path, not PRE-MAIN;
- stage exact R2 `598d9e9eaba5143950c63317705fd09104fbf463` at `<receiving-path>/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`;
- apply the F2-corrected packet containing exact candidate `8d9585296ff264b947559f4a78f49f73ca45e53a`;
- require 640 files, 639 self-excluded preimage entries, 174 extension files, the CLI and `verify_packet.py` green;
- run the 20 R2 + 9 R3 + 6 E tests and the first consumer independently;
- retain `OWNER_ANCHOR_REQUIRED`, `C9_SOURCE_MISSING`, C9/C12 owner migration, CP-A5 separate root and `native_person=false`.

No PRE-MAIN merge, production adoption or owner signature follows from this engineering result.

## Sourcefree archive / owner hold

If no live receiver is named, retain the exact sourcefree candidate as an owner-held historical archive at:

`8d9585296ff264b947559f4a78f49f73ca45e53a` / tree `5394e33ec81766a4ee891b0d58007f24ac1d1303`.

The F2-corrected receiving verifier above is the exact transfer gate for that candidate. The archive remains TEST_ONLY and sourcefree; F1/F2 do not grant native C8/C9/C11/C12/CP-A5, original owner anchor, human A5, Pyat N11/N12, PROGRAMMA, production or merge authority.

## Stop point

F2 is complete at the engineering scope:

`ALL_459_R2_BLOBS_VERIFIED_BEFORE_WRITE__NONVENDOR_TAMPER_FAILS_CLOSED__35_CLEAN_STAGE_TESTS_GREEN__FIRST_CONSUMER_PARTIAL`

HQ can inspect the one-file source delta and receipts, then choose sourcefree archive/owner hold or an isolated receiving path. No new historical audit or reviewer campaign is required.
