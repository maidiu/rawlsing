# Owner receiving or archive closure

## One terminal disposition

`REVISE_ONE_EXACT_PACKET_DEFECT`

Do not receive the current F1 packet as ready. The 640-file sourcefree candidate is complete and test-green, but the packet's pre-write R2 base check is not full-tree:

- `verify_r2_base.py` authenticates the manifest, the 444 vendor blobs and the 459-path set;
- it does not authenticate the 15 non-vendor R2 files;
- a changed `joined/session.py` with the manifest unchanged passes `verify_r2_base.py` and `apply.sh` proceeds.

The exact source candidate itself is not rejected:

```text
source candidate: 8d9585296ff264b947559f4a78f49f73ca45e53a
tree:             5394e33ec81766a4ee891b0d58007f24ac1d1303
files:            640
extension files:  174
preimage:         639/640, self-excluded
tests:            20 R2 + 9 R3 + 6 E green
first consumer:   PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT
```

## Minimal exact repair

Change only `candidate/receiving_packet/verify_r2_base.py` and its negative test:

1. Derive the complete R2 tree from Git at `598d9e9eaba5143950c63317705fd09104fbf463`, path `SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`, including every blob identity.
2. Require all 459 actual regular files to match the expected tree blobs, not just the 444 vendor rows and the path set.
3. Fail before extraction or write on any non-vendor content or file-type mismatch.
4. Add the direct regression: tamper `joined/session.py`, keep all 459 paths and `SOURCE_MANIFEST.json` unchanged; `verify_r2_base.py` exits 1, `apply.sh` exits 3, destination remains unchanged.
5. Re-run only that probe and the already-green clean stage. Do not change the 640 candidate, the preimage, the tests or the F1 branch history.

No new Sorok census, science campaign or broad receiving review is required.

## Owner receiving action

If the owner elects live receiving after the one-file fix:

- choose an isolated owner-controlled receiving path;
- stage exact R2 `598d9e9eaba5143950c63317705fd09104fbf463` at `<receiving-path>/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`;
- install the corrected packet containing exact source `8d9585296ff264b947559f4a78f49f73ca45e53a`;
- verify 640 files, 639-entry self-excluded preimage, 174 extension files and the CLI;
- keep the consumer result partial: C9 actor missing, C9/C12 owner migration required, CP-A5 separate root, `OWNER_ANCHOR_REQUIRED`, native person false.

No PRE-MAIN merge, production adoption or live caller is implied by that receiving path.

## Archive alternative

If no owner-selected live receiver is named, the complete tested source may be preserved as a sourcefree owner-held historical archive at exact source `8d9585296ff264b947559f4a78f49f73ca45e53a`. This is an archive decision, not acceptance of the F1 packet as ready. The packet remains `REVISE_ONE_EXACT_PACKET_DEFECT` until the base-tree check is corrected.

The finite historical RRIF can close at sourcefree archive scope once HQ records that disposition and the exact owner-held exceptions; it cannot close as `ACCEPT_SCOPED_READY_FOR_OWNER_RECEIVING` on this review.

## Holds retained

`OWNER_ANCHOR_REQUIRED`; C9 actor `C9_SOURCE_MISSING`; C9/C12 owner migration required; CP-A5 separate root; C12 self-consistency only; native C8/C9/C12 false; native CP-A5 false; native person false; owner adoption false; no production merge.
