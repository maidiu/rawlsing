# Five prior review reds — exact F1 retest

**F1 tested:** `1973d28ed4ba4c9e58c9d96fbe358445dddc929c`

**Prior review:** `1198691534c050c19c7c874454b54f99011006c4`

**PRE-MAIN cut:** `8e44ca9c751049d65e6def47600b5c073ee04b29`

**R2 base:** `598d9e9eaba5143950c63317705fd09104fbf463`

**Full candidate:** `8d9585296ff264b947559f4a78f49f73ca45e53a` / tree `5394e33ec81766a4ee891b0d58007f24ac1d1303`

| Prior defect | F1 retest | Result |
|---|---|---|
| D1: 174-file `rrif_r3_extension` omitted | full 640-file candidate installed; extension count 174 | **PASS** |
| D2: 638-entry preimage omitted CLI/extension | 639 entries, self excluded, CLI listed, 174 extension files | **PASS** |
| D3: lookalike R2 base accepted | vendor and manifest checks added, but 15 non-vendor files are not compared | **FAIL: ACTUAL FAIL-OPEN** |
| D4: unsafe `git clean -fd` rollback | no clean/reset/checkout; exact 459-file R2 restored in isolated worktree | **PASS at isolated scope; no target-isolation guard** |
| D5: tests/consumer failed on clean base | 20 R2 + 9 R3 + 6 E + first consumer on clean stage | **PASS** |

## D1 — complete extension

Clean R2 base plus F1 packet produced:

```text
regular files:                    640
rrif_r3_extension files:          174
first_consumer_cli.py:            present
```

`verify_packet.py` returned `ok: true`, `listed=639`, `actual=640`, `unlisted=[]`.

Removing `rrif_r3_extension/c12_guard.py` from a validated copy returned:

```text
MISSING_FILES:rrif_r3_extension/c12_guard.py
ACTUAL_FILE_COUNT_MISMATCH
actual=639
r3_extension_files=173
verify_packet.py exit 1
```

## D2 — preimage

The new `RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json` has SHA-256 `886f56b7788258fcbb3b9be665770c5af3fc7fdd13537a26227cc351c5bad092` and records:

```text
files:                    639
actual_regular_files:     640
vendor_manifest_files:    444
r3_extension_files:       174
first_consumer_cli:       included
self entry:               excluded
```

A changed `SOURCE_MANIFEST.json` on the full candidate returned exit 1 with `SOURCE_MANIFEST_SHA256_MISMATCH`; an added unlisted file returned exit 1 with `UNLISTED_FILES:extra.txt`.

## D3 — base fail-open

`verify_r2_base.py` (SHA-256 `18dbd92fcd4289ba01e59a337ada86cbc84ef2f7b021a5d1dfec2da2bb9a0fba`) checks the manifest hash, 444 vendor blobs and the 459-path set. It does not compare the 15 non-vendor files.

The tamper probe preserved all 459 paths and the exact manifest:

```sh
cp -a "$R2" /tmp/rrif_r2_tamper
printf '\n# TAMPER_NONVENDOR_JOINED_SESSION\n' >> /tmp/rrif_r2_tamper/joined/session.py
python3 verify_r2_base.py --dest /tmp/rrif_r2_tamper --repo "$PREMAIN"
```

Result:

```json
{
  "schema": "RRIF_E_R2_BASE_VALIDATION@1",
  "ok": true,
  "errors": [],
  "expected_files": 459,
  "actual_files": 459,
  "vars": 444
}
```

The original file blob was `ea820ec3e30a2825c3d0d8c5dc66e812afdda40b08f9cc0a8c868c8b3e0dd0da`; the tampered file was `97f40d457cf14d5877859a69d0883b6b4ba7db9e907a6925764f9406210fcbc4`. The manifest remained at `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`.

Running F1 against that tampered destination returned:

```text
apply.sh exit 0
RRIF_E_PACKET_APPLIED_NOT_MERGED
final regular files: 640
```

The post-apply full-candidate copy happened to overwrite `joined/session.py`, so the ordinary final tree was green. That does not repair the pre-write gate: `apply.sh` accepted an unauthenticated base and proceeded. This is the one blocking defect.

The same validator correctly rejected a vendor tamper:

```text
VENDOR_BLOB_MISMATCH:vendor/j/r31j/product.py
exit 1
```

## D4 — rollback

`rollback.sh` exited 0 after a full F1 apply:

```text
RRIF_E_ROLLBACK_RESTORED_EXACT_R2
files: 459
SOURCE_MANIFEST.json: 7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126
```

No `git clean`, reset, checkout, force, branch deletion or foreign sibling deletion was used. The command was run only in the isolated review-created worktree. The script has no independent target-isolation guard, so that operational restriction remains required.

## D5 — clean-stage tests and consumer

Run on the full F1 stage, each suite in its own process, with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONHASHSEED=0`:

| Suite | Result |
|---|---|
| 20 R2 tests, `tests/test_join.py` + `tests/test_rrif_r2_c12.py` | **20 passed** |
| 9 R3 extension tests, `rrif_r3_extension/tests/test_rrif_r3_extension.py` | **9 passed** |
| 6 RRIF-E tests, `tests/test_rrif_e_repair.py` | **6 passed** |
| First consumer | **exit 0**, expected partial status |

Consumer status:

`PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT`

Consumer receipt SHA-256: `98ad04d915f5c90c70ba223bbf16ba1d73aee90bc7181864708705c674a06ccb`.

Required holds survived:

```text
C9 actor:              C9_SOURCE_MISSING
C9/C12:                INCOMPATIBLE_WITHOUT_OWNER_MIGRATION...
CP-A5:                 separate root, RETAIN_TOOL
external anchor:       OWNER_ANCHOR_REQUIRED
native C8/C9/C12:      false
native CP-A5:          false
native person:         false
owner adoption:        false
```

## Additional fault probes

| Probe | Result |
|---|---|
| absent R2 base before apply | exit 2, `RRIF_E_BASE_R2_MISSING`, destination absent |
| exact R2 base | 459 files, 444 vendor rows, manifest hash exact |
| F1 apply | exit 0, 640 files, 639 preimage, 174 extension files, CLI present |
| missing extension | exit 1, missing file and count mismatch |
| unlisted extra file | exit 1, unlisted file reported |
| base `SOURCE_MANIFEST.json` tamper | exit 1, hash/row mismatch |
| base vendor blob tamper | exit 1, `VENDOR_BLOB_MISMATCH` |
| base non-vendor source tamper | **exit 0, fail-open** |
| rollback | exit 0, exact 459 R2 restored |

## Verdict

D1, D2 and D5 are repaired. D4's unsafe commands are removed and exact restoration works in isolation. D3 remains a reproducible pre-write fail-open. The terminal decision is `REVISE_ONE_EXACT_PACKET_DEFECT`.
