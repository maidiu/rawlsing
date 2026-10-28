# SYN02-F0-R3 — finite source-custody and transport repair return

**Return status:** `F0_R3_SOURCE_EDITS_HELD_NO_R3_OWNER_SCOPE__ISOLATED_PATCH_READY__R3_TESTS_RED_ON_R2_GREEN_ON_PATCHED_COPY__58_21_BOTH_CWDS_PASS__NO_PAID_CALL__NO_NATIVE_GRANT`.

**Branch:** `agent/sorok-syn02-f0-r3-source-custody-repair-r1`.
**Sealed source startup:** `60797302652e7d7877443f6e9d0becde5afb8382`.
**Documentary commission:** `6b31fd3b87f757f1a67b119068c6f8d4198f15f9`.
**Immutable independent findings:** RF0-R2 `5c9ac33aab23c75d35314ece57c30dc95a96aee7`.
**Historical F0 alternate:** `agent/sorok-syn02-f0-portable-sourcefree-build-r1` at `c821b488b3a9a3f0fa01b1981989cc17af637dc1`; unadopted.
**Source-edit disposition:** **HOLD**. No accepted S48/S51/S52 source file was changed.
**Test grade:** `SOURCEFREE_TEST_ONLY`; no paid CLI/provider, no native C8/C9/C11/C12/A5, no survey/source execution, no production edit.

## 1. Three courts

| Court | Verdict | Basis |
|---|---|---|
| **ENGINEERING** | `REVISE_PRECISE / ISOLATED_PATCH_READY / ACCEPTED_SOURCE_UNCHANGED` | RF0-R2’s five findings are source-true. An isolated patch and seven adversarial tests close them in a non-repository copy: 7/7 pass; unpatched R2 is 7/7 RED. Existing 58 base + 21 R2 tests pass in both root and `/tmp` on both unpatched R2 and the isolated patched copy. The accepted source remains unedited because no R3 owner scope exists. |
| **SCIENCE** | `NO_CHANGE / NO_NATIVE` | No psychological, developmental, care, memory, typology, Rule A/T, SCI05, independent-B, actor or no-world-state semantics changed or validated. C12 fork perception-loss remains an inherited RED. |
| **AUTHORITY** | `HOLD / NO_NATIVE_GRANT` | F0-R2’s owner-scope record covers only R2, not R3. No R3 prospective S48/S51/S52 owner approval was found. No source adoption, provider entitlement, C8/C9/C11/C12, CAN/ADP/Pyat, SCI05, human or production authority is issued. |

## 2. Deliverables

All under `WORKER_RETURNS/SOROK-SYN02-F0-R3-PORTABILITY/`:

- `00_RETURN.md` — this return.
- `01_OWNER_SCOPE_AND_HOLD.md` — why source edits are held.
- `02_TEST_RECEIPTS.md` — exact commands and differential results.
- `03_REPAIR_PLAN_AND_PATCHES.md` — findings, owner, first consumer and patch contract.
- `patches/F0-R3-source-custody.patch` — isolated four-file source/manifest patch; `git apply --check` = 0.
- `external_source_trust.json` — 141-entry R30A vendor/r29p + S39 external trust registry.
- `tests/conftest.py`, `tests/test_r3_adversarial.py` — seven R3 adversarial acceptance tests.

Artifact hashes:

```text
patch          40b98b7b6f08016ffe69e4c7054bc7277944a5d06931c9dfa29864f9c80ffea9
external trust edd1a6ef0e31e6cff5777ffdd412fbeac8f77ca612e327c863af255f520b7faa
R3 test        6e604a825c5943bdc4fa2787733feea818052eba22852bddc04f5ac33c1939a8
```

## 3. Findings closed in isolated patch

- **Fake preloaded `s51.source_binding`:** canonical path check rejects a foreign/no-`__file__` module before S49/G18/R30A import.
- **No-`__file__` managed cache:** all managed prefixes without paths now raise `SOURCE_IMPORT_CACHE_UNBOUND`.
- **Empty/truncated manifest:** `_MIN_SOURCES=31` rejects empty/truncated provenance-valid manifests.
- **R30A vendor/r29p + S39:** 141 exact external trust entries are verified before execution; the 31-entry core `source_count` remains 31 and does not falsely claim full R30A coverage.
- **External `log_dir`:** resolves/validates before work/log directories and subprocess; external path returns `S48_PRODUCT_LOG_DIR_OUTSIDE`.
- **Account/receipt:** account is explicitly `ALIAS_ONLY`; `actual_provider_call` is `False`; subprocess/observed-step evidence is separately labelled. No fake CLI call is called a provider call.

Patch is against `607973...` and touches only S48 `product.py`, S51 `source_binding.py`, S52 `source_registry.py`, and the R2 `source_manifest.json`. It does not edit S39, R30A vendor, evidence scripts, C9/C12, CAN/ADP/Pyat/SCI05, production, or historical branches.

## 4. Actual test replay

Unpatched R2 source:

```text
58 base passed (S52 18 + S48 14 + S51 13 + S49 13) from repo root
58 base passed from /tmp
21 R2 adversarial passed from repo root
21 R2 adversarial passed from /tmp
R3 adversarial: 7 failed (expected RED)
```

Isolated patched copy:

```text
58 base passed from repo root
58 base passed from /tmp
21 R2 adversarial passed from repo root
21 R2 adversarial passed from /tmp
R3 adversarial: 7 passed
```

The sourcefree patch test used fake executables only. No real provider/account, no C8/C9/C11/C12/A5, no survey/source execution. Exact commands/outputs are in `02_TEST_RECEIPTS.md`.

## 5. Owner scope and reason for HOLD

The F0-R2 `01_OWNER_SCOPE.md` record is explicitly the **R2** tranche. It states:

- the user approved “enumerated R2 source scope”;
- this is not a standing source-owner grant;
- it is not a retroactive F0 approval or native/production grant;
- the historical F0 branch/extra-file delivery remains separate.

The R3 commission requires verified prospective S48/S51/S52 owner approval for actual source edits. No R3-specific record was found in the checked-out source or exact startup history. The user launch is dispatch, not a separately evidenced original-owner scope. Therefore the accepted source was **not edited**; the patch and tests are isolated for owner decision.

Required next action:

1. Competent S48/S51/S52 source owner records prospective R3 scope over the exact patch and external trust file.
2. A distinct implementer applies the patch to a clean R2 checkout; copy/external trust remains present.
3. Re-run 58+21 from root and `/tmp` plus the seven R3 tests.
4. A distinct independent reviewer inspects the applied source and results.
5. Only then may source integration be considered.

## 6. Residual and non-claims

- Real paid CLI/provider/model/account call: **NOT_RUN**.
- `run_s52_evidence.py`, S48/S51 evidence scripts: **NOT_RUN**; historical `/Users/` paths remain residual.
- C12 fork perception loss: **inherited RED**, not repaired by this patch.
- F1.1 storage freeze: **HOLD**; not started here.
- Native C8/C9/C11/C12/A5, independent B, Rule A/T, SCI05, Pyat C11, human empirical result, production: **NOT_RUN / NO_GRANT**.
- Historical F0 alternate branch remains unadopted.
- No source/provider/native authority is inferred from sourcefree tests or a passing patch copy.

## 7. Engineering/science/authority handoff

**ENGINEERING:** `REVISE_PRECISE` with a tested isolated patch; accepted source unchanged because the R3 owner scope is absent.
**SCIENCE:** `NO_CHANGE`.
**AUTHORITY:** `HOLD / NO_NATIVE_GRANT`.

**Final remote SHA:** read back after committing these R3 artifacts; deliberately not self-embedded here because self-embedding changes the commit. No source edit, merge, provider call or native grant was performed.

**STOP: OWNER SCOPE REQUIRED BEFORE APPLYING THE PATCH.**
