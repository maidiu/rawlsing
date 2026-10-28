# SYN02-F0-R3 — test receipts and replay

**Source-edit status:** HOLD (no R3 owner scope); no accepted source file edited.
**Patch:** `patches/F0-R3-source-custody.patch`
**Patch SHA-256:** `40b98b7b6f08016ffe69e4c7054bc7277944a5d06931c9dfa29864f9c80ffea9`
**External trust:** `external_source_trust.json`
**External trust SHA-256:** `edd1a6ef0e31e6cff5777ffdd412fbeac8f77ca612e327c863af255f520b7faa`
**R3 test file SHA-256:** `6e604a825c5943bdc4fa2787733feea818052eba22852bddc04f5ac33c1939a8`
**Baseline source startup:** `60797302652e7d7877443f6e9d0becde5afb8382`
**Grade:** sourcefree Python/pytest only; no paid CLI/provider, no native C8/C9/C11/C12/A5, no survey, no production edit.

## 1. Unpatched R2 baseline — 58 base tests

Environment: `PYTHONDONTWRITEBYTECODE=1`; `TMPDIR` outside source; G18/Join-E roots explicitly selected; no provider.

```text
S37_JOIN_E_RETURN=/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1
S52_G18_SOURCE=/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/candidate/vendor/bp2/vendor/g18
S52_ALLOWED_ROOTS=/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j:/Users/matthewsmith/Desktop/Rawlsing
```

### Repository root

```text
S52 18 passed
S48 14 passed
S51 13 passed
S49 13 passed
TOTAL 58 passed
```

### Alternate `/tmp`

```text
S52 18 passed
S48 14 passed
S51 13 passed
S49 13 passed
TOTAL 58 passed
```

### R2 adversarial suite

```text
21 passed from repository root
21 passed from /tmp
```

This independently reproduces the RF0-R2 baseline: **58 + 21 pass in both cwds** on the unpatched source. It does not fix the R3 defects.

## 2. R3 adverse tests on unpatched R2 — expected RED

Command shape:

```text
F0R3_SOURCE_ROOT=<R2 checkout> \
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-SYN02-F0-R3-PORTABILITY/tests
```

Exact result on the unpatched R2 startup:

```text
FFFFFFF                                                                  [100%]
7 failed
```

Failures observed, in order:

1. `test_preloaded_fake_binding_is_refused_before_managed_imports`
   `BYPASS` — preloaded `s51.source_binding` no `__file__` returns fake verification success.
2. `test_managed_no_file_cache_is_refused`
   `BYPASS` — no-`__file__` managed module is skipped rather than refused.
3. `test_empty_manifest_is_refused`
   no exception — empty `sources` list returns `verified: 0`.
4. `test_external_trust_covers_r30a_vendor_and_s39`
   no `external_verified` receipt — source binding does not verify R30A vendor/S39 trust entries.
5. `test_external_log_dir_refused_before_fake_subprocess`
   `ValueError` from `stdout_path.relative_to(RETURN)` after fake subprocess/log writes, not pre-call refusal.
6. `test_fake_cli_receipt_does_not_claim_actual_provider_call`
   `actual_provider_call: True` for a fake CLI.
7. `test_truncated_manifest_missing_required_path_is_refused`
   a 31-entry manifest with a required path removed and an extra valid path added is accepted instead of rejecting the missing required path.

These are the five RF0-R2 findings plus the explicit R3 external-trust coverage check. They are **RED on the unpatched source**, not a pass.

## 3. Isolated patched copy — 58 + 21 pass

A separate, non-repository copy of the R2 source was made under the worker evidence area. The patch was applied only to that copy; the accepted source worktree remained unmodified.

Copy test environment was the same as above, with `F0R3_SOURCE_ROOT` pointing at the copy.

### Repository root

```text
S52 18 passed
S48 14 passed
S51 13 passed
S49 13 passed
TOTAL 58 passed
R2 adversarial 21 passed
```

### Alternate `/tmp`

```text
S52 18 passed
S48 14 passed
S51 13 passed
S49 13 passed
TOTAL 58 passed
R2 adversarial 21 passed
```

## 4. R3 tests on isolated patched copy — GREEN

```text
.......                                                                  [100%]
7 passed
```

The seven tests are:

- preloaded fake binding refuses before S49/G18/R30A import;
- managed no-`__file__` cache refuses;
- empty/truncated manifest refuses;
- external trust covers R30A vendor/r29p `stable_actor_binding`, R29P runner, and S39 sources;
- external `log_dir` refuses before fake subprocess (no marker);
- fake CLI receipt does not claim `actual_provider_call` and reports `ALIAS_ONLY` account transport;
- a 31-entry manifest with a required path missing refuses, even if another valid path is substituted.

No paid provider or native execution is involved.

## 5. Patch application check

```text
git apply --check WORKER_RETURNS/SOROK-SYN02-F0-R3-PORTABILITY/patches/F0-R3-source-custody.patch
=> 0
```

The patch touches only:

- `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/s48/product.py`
- `WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/source_binding.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/source_registry.py`
- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/source_manifest.json`

It does **not** modify S39, R30A vendor, evidence scripts, C9/C12, CAN/ADP/Pyat/SCI05, production, or historical F0 branches.

## 6. Manifest/source observations

- Existing manifest remains the 31-file F0 closure; source count stays 31 so existing `source_count == 31` tests remain valid.
- R3 adds an **external trust entry** of 141 files:
  - 133 R30A vendor/r29p files, including `vendor/r29p/candidate/stable_actor_binding.py` and `vendor/r29p/r29p/runner.py`;
  - 8 S39 package files, including `s39/sources.py`.
- External trust is verified by path/hash/owner/role/scope/effective time before S52/S39/R30A execution; it is not part of the 31-file `sources` count.
- The patch updates the existing 31-file manifest hashes for the patched S48/S51/S52 files.

## 7. Not run

- Real paid CLI/provider/model/account call: **NOT_RUN**.
- `run_s52_evidence.py`, `run_s48_evidence.py`, `run_s51_evidence.py`: **NOT_RUN**; evidence-script host paths remain residual.
- Native C8/C9/C11/C12/A5, independent B, Rule A/T, SCI05 admission, raw survey/source execution, production: **NOT_RUN**.
- C12 fork repair: **HOLD/inherited RED**; not this R3 patch.

**No source edit was applied. No provider authority or native grant is inferred.**
