# SOROK S45-S47 causal regression harness — package-closure integrated

**RESULT:** `S45_S47_CAUSAL_HARNESS__PACKAGE_CLOSURE_IMPORT__SAME_ROOT_ACTUAL_VS_SCHEDULED__S47_C9_AND_S45_DO_HELP__SEVER_RED_RESTORE_PASS__COLD_REPLAY__WRONG_ROOT_REFUSED__22_CHECKS_PASS__ENGINEERING_EVIDENCE_NOT_INDEPENDENT_REVIEW`.

**Grade:** `TEST_ONLY_ENGINEERING_CAUSAL_REGRESSION_NOT_INDEPENDENT_FINAL_REVIEW`.

This harness is engineering evidence, not independent final review, acceptance, native/psychological issuance or human validation. The integration run below imports the shipped S45-S47 package closure directly; it does not use the harness's independent git-extraction stage.

## Shipping unit

All three adjacent return directories are required: this harness, the product
import closure, and the public projection adapter. The package return alone does
not contain the projection.

## Published history and pins

- Public harness: `3d6207983b62646108d4c6e3ff1a3b4d65674977`.
- Cherry-picked closure-branch commit: `5531492df2317166d223e6c6bc211b147e0912f7`.
- Accepted integration source: `da97d2624486b783bf5c4f465b17fdcdea3af20a`. Focused fix commit: this branch head after the three review fixes; exact hash returned in final readback; parent is `da97d2624486b783bf5c4f465b17fdcdea3af20a`.
- Package closure: `WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1`.
- Source pins remain S45 `f26a138e20d53c809d611cf8d834ec647b0804bf`, S46 `f0ef39b92ce2e4add5c0a699389e12f1d7ae434e`, S47 `765a441f87292aa4c17794745b65cb54e6aaa83f`, with S37/S42 seam bytes from the S47 cumulative cut and the exact dependency closure in the package `SOURCE_MANIFEST.json` (424 blobs).
- The package closure includes the same S37/S42 seam-carrying trees used by the prior stage run and adds pinned WP19/S11 projection dependencies.

## Independent review status

Independent reviewer session `ses_e526dc569ffe67E2MTl0k6Y38V` accepted the adjacent package+projection+harness unit at `da97d2624486b783bf5c4f465b17fdcdea3af20a` with 11 projection tests, 22 harness checks, cold replay, privacy and source cut/restore. That acceptance is historical for the focused fix commit; the new code requires focused closure.

## Package-closure mode

`run_causal_harness.py` now accepts:

```text
python3 WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/run_causal_harness.py \
  --package-closure WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product \
  --original-tests none
```

In this mode the harness:

- installs `sorok_s45_s47.bootstrap` from the shipped package;
- verifies every package source file against `SOURCE_MANIFEST.json`;
- verifies the load-bearing imported modules resolve under `product/vendor`;
- runs the same ACTUAL vs SCHEDULED_ONLY, C9, S45 DO_HELP, sever/restore, cold and wrong-root scenarios;
- does not extract pins independently and does not rerun full author suites.

The git-extraction mode remains available for historical reproduction.

## Exact integration run and result

Executed from the bound workdir:

```text
/usr/local/bin/python3 WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/run_causal_harness.py \
  --package-closure WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product \
  --original-tests none \
  --json-out WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/evidence/harness_run.json
```

Result: **PASS**, exit `0`, elapsed `69.457s`. Mode: `PACKAGE_CLOSURE`.
Source audit: 424/424 exact. Package modules under closure: `true`.
Checks: 22/22 true. Full machine report: `evidence/harness_run.json`.
Captured stdout: `logs/harness_stdout.log`.

Original focused suites were intentionally **NOT_RUN** in this package-closure integration with the explicit selection `none` and reason `PACKAGE_CLOSURE_MODE_EXPLICIT_ORIGINAL_TESTS_NONE`. Package mode now refuses `--original-tests all` or `s47` before success with `PACKAGE_CLOSURE_ORIGINAL_TESTS_UNSUPPORTED` (exit 2); refusal evidence is `evidence/harness_original_tests_all_refusal.json`. The prior stage run's S45/S46/S47 `21/17/17 passed` evidence remains in git history and retained `logs/`/`evidence/junit/` files; those suites were not duplicated here.

## Same-root causal result

Both modes reconstruct the same root `3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`.

| Observation | ACTUAL performed interval | SCHEDULED_ONLY source |
|---|---|---|
| Interval status | `PARTIAL` | `NOT_PERFORMED` |
| Interval coverage | `[[222, 223]]` | `[]` |
| Material after interval | `0` | `1` |
| S47 source in actual C9 readset | `true` | `true` |
| S47 source hash | `e196c974e43a024055949113f6b875be8c012f1c422d6829d4890e8a46688658` | `d73a00eff7209a6a6fa504fedd46912d5182e00f1d74ead3161dd29c8f494665` |
| C9 `objective_material_eligible` | `false` | `true` |
| C9 target | `NO_CHANGE` / `NO_PROPOSAL` | `NO_CHANGE` / `NO_PROPOSAL` |
| S45 `DO_HELP` | `OK`, accepted `false`, `HELP_REFUSE` | `OK`, accepted `true`, `HELP_ACCEPT` |
| Other actor B state | preserved | preserved |

Cold reopen reproduced the same root, event-bound source hashes, eligibility and encounter chain.

## Sever dependency RED -> restore PASS

- Cut: second admission refused with `S46_INTERVAL_CONDITION_REVOKED`.
- Historical first C9 event retained its admitted S47 source while the present condition was revoked.
- Restore: source reconstructed with the same hash, second admission PASS, C9 source in readset, `objective_material_eligible=false`.
- Cold reopen: first and second event-keyed C9 reads returned the same admitted source hashes.
- Package-mode check: `sever_dependency_red`, `sever_preserves_historical_c9_source`, `restore_dependency_pass`, `sever_restore_cold_replay` all true.

## Wrong-root negative

Two different root seeds produced distinct roots. Substituting A's interval source into B's supported S47 qualification gate:

- Unresealed foreign source: refused `S47_SOURCE_AS_OF_MISMATCH`.
- Resealed foreign source: refused `S47_SOURCE_INTERVAL_STATE_ID_MISMATCH`.
- B's own source remained accepted and B's C9 used B's own source.

Private-hook source injection outside `qualify_source` is not a supported seam and is not counted as product behavior.

## Exact imports and source custody

`evidence/harness_run.json` contains the package source audit, module origins, environment, commands and every scenario result. In package mode, `source_manifest` is the shipped package closure audit (`SOROK_S45_S47_HARNESS_PACKAGE_CLOSURE@1`) rather than a git-extraction stage manifest. No external checkout, Desktop path, temporary staging or other repo source was imported.

## Limitations

- TEST_ONLY sourcefree synthetic roots and TEST_ONLY installed-simulation owner material.
- No empirical probability, CAN008/CAN011, native C8/C9/C12/ADP, developmental T, childhood biography, Pyat native world, human A5/Gate4/Gate5 or user study is claimed.
- No native psychology, real respondent, external message delivery, paid action or independent acceptance.
- No provider call, network action, external channel or human trial occurred.
- No pinned S45-S47 source behavior, expected psychology or psychological rule changed.
- Full author suites were not duplicated in this integration; package-mode projection tests and the causal scenarios are the new regression.
- Independent review and PRE-MAIN receiving remain separate holds.

## Branch and publication

Branch: `codex/sorok-s45-s47-closure-20261105-r1`.
Published history: package `e42faf01b57a9188f0cf75baaccfcd57edb07173`; projection cherry-pick `4e9ebc85d78995e93a7fbace0ead78d703067244`; harness cherry-pick `5531492df2317166d223e6c6bc211b147e0912f7`; accepted integration `da97d2624486b783bf5c4f465b17fdcdea3af20a`; focused fix commit is the exact head returned in final readback.

## PROGRAMMA_DELTA

See `PROGRAMMA_DELTA.md` / `PROGRAMMA_DELTA.json`: package-closure integration and engineering evidence only. No PROGRAMMA canonical product, native science, seam/gate register or receiving authority changed.
