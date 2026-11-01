# SOROK RRIF-E F1 — FINAL HOSTILE VERDICT

**DECISION: REVISE_ONE_EXACT_PACKET_DEFECT**

**Tested F1:** `agent/sorok-rrif-e-exact-receiver-packet-fix-20261031-r1@1973d28ed4ba4c9e58c9d96fbe358445dddc929c`

**Review dispatch:** `review/sorok-rrif-e-f1-packet-delta-terminal-20261101-r1@37bd2048081507cd4235f2097744a916b8efa0ae`

**Tested PRE-MAIN:** `integration/pre-main-reconciliation-r1@8e44ca9c751049d65e6def47600b5c073ee04b29`; unchanged at start and end.

**Prior review:** `1198691534c050c19c7c874454b54f99011006c4` — `REVISE_EXACT_RECEIVING_DEFECT`.

**R2 base:** `598d9e9eaba5143950c63317705fd09104fbf463`; 459 regular files; 444 vendor rows; `SOURCE_MANIFEST.json` SHA-256 `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`.

**F1 full candidate:** `8d9585296ff264b947559f4a78f49f73ca45e53a`; path `WORKER_RETURNS/SOROK-RRIF-FINAL-E-REPAIR-AND-FIRST-CONSUMER-R1/candidate/rrif_r2`; tree `5394e33ec81766a4ee891b0d58007f24ac1d1303`.

## Engineering verdict

F1 repaired four of the five prior receiving defects. The clean PRE-MAIN stage now installs the complete 640-file candidate, contains all 174 `rrif_r3_extension` files and `first_consumer_cli.py`, has a 639-entry self-excluded preimage, runs 20 R2 + 9 R3 + 6 E tests green, and runs the first consumer to the expected partial/owner-held result. Rollback restores exact 459-file R2 and no longer uses `git clean -fd`.

One material receiving defect remains: `verify_r2_base.py` does not authenticate the content of the 15 non-vendor R2 files. A changed `joined/session.py` with all 459 paths preserved and `SOURCE_MANIFEST.json` untouched passes `verify_r2_base.py` with `"ok": true`, and `apply.sh` then proceeds and exits 0. The later full-candidate copy overwrites that file in the ordinary-tree case and the post-apply packet verifier passes, but the required fail-closed base precondition is still false. An unauthenticated lookalike base is not fixed.

## Scientific verdict

**HOLD.** No native C8/C9/C12, CP-A5, CAN/ADP/SCI05, Pyat, C11, human A5 or native person is claimed. C9 actor remains `C9_SOURCE_MISSING`; C9/C12 is incompatible without owner migration; C12 remains self-consistency only; `OWNER_ANCHOR_REQUIRED`; `native_person=false`.

## Authority verdict

**HOLD.** This review does not adopt, merge or bless PRE-MAIN or production code. There is still no proved live PRE-MAIN consumer. F1 remains a sourcefree TEST_ONLY receiving packet.

## Blocking defect

`verify_r2_base.py` checks exactly these properties:

- `SOURCE_MANIFEST.json` SHA-256;
- exactly 444 vendor rows;
- every vendor file's Git blob;
- exactly 459 expected paths, with no missing or extra path.

It does not compare any of the 15 non-vendor files against the R2 Git tree:

```text
.gitattributes
RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json
SOURCE_MANIFEST.json
joined/__init__.py
joined/assertion.py
joined/cli.py
joined/closure.py
joined/imports.py
joined/lineage.py
joined/provenance.py
joined/readonly.py
joined/refusal.py
joined/session.py
tests/test_join.py
tests/test_rrif_r2_c12.py
```

Actual reproduction:

```text
append "# TAMPER_NONVENDOR_JOINED_SESSION" to joined/session.py
preserve all 459 paths
preserve SOURCE_MANIFEST.json byte-for-byte
verify_r2_base.py -> exit 0, {"ok": true, "expected_files": 459, "actual_files": 459}
apply.sh -> exit 0, RRIF_E_PACKET_APPLIED_NOT_MERGED
```

This is the exact lookalike-base fail-open the prior review required F1 to close.

## Minimal exact repair

Modify `verify_r2_base.py` to derive the full R2 tree from Git, not only the vendor manifest and path set:

```sh
git -C <repo> ls-tree -r --format='%(objectname) %(objecttype) %(path)' 598d9e9eaba5143950c63317705fd09104fbf463 -- SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2
```

Compare every expected regular-file blob against the actual file's Git blob before any extraction or write. Fail on non-vendor content, type or symlink mismatch. Add one direct regression: tamper `joined/session.py`, keep the 459 paths and manifest unchanged, require `verify_r2_base.py` exit 1, `apply.sh` exit 3 and the destination unchanged. No candidate source changes and no new F1 campaign are required.

## Rollback

F1 removed the unsafe `git checkout --` / `git clean -fd` behavior. In an isolated review-created worktree, `rollback.sh` restored exactly 459 R2 files and the exact manifest. It operated only on the fixed candidate destination and removed no foreign sibling path. The script still trusts the supplied target, so isolated invocation remains mandatory; no additional deletion path was observed.

## RRIF closure

The 640-file sourcefree candidate is complete enough to preserve as an owner-held historical archive at `8d9585296ff264b947559f4a78f49f73ca45e53a`. It is not ready for owner receiving as the current packet because the base fail-open must be corrected first. The finite historical RRIF can close at sourcefree archive scope only if HQ explicitly records the packet as `REVISE`; it cannot close as `ACCEPT_SCOPED_READY_FOR_OWNER_RECEIVING` on this evidence. After the minimal base-tree check, rerun only the non-vendor tamper probe and the already-green clean stage; no fresh Sorok census is needed.
