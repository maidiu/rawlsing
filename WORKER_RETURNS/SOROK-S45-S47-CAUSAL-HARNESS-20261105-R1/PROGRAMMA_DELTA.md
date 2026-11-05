# PROGRAMMA_DELTA — S45-S47 causal harness package-closure integration

**Delta ID:** `SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1`
**Grade:** `TEST_ONLY_ENGINEERING_CAUSAL_REGRESSION_NOT_INDEPENDENT_FINAL_REVIEW`.
**Result:** `PASS` in `PACKAGE_CLOSURE` mode, 22/22 checks, exit 0. Accepted integration source `da97d2624486b783bf5c4f465b17fdcdea3af20a`; the focused fix commit is the exact head returned in final readback.

## Shipping unit

All three adjacent return directories are required: this harness, the product import closure, and the public projection adapter. The package return alone does not contain the projection.

## Delta

Added package-closure integration to the existing public harness:

- `--package-closure PATH` installs the shipped `sorok_s45_s47` product closure.
- `harness/package_closure.py` verifies the package `SOURCE_MANIFEST.json` (424 exact files), checks imported modules resolve under `product/vendor`, and reports `modules_under_package`.
- Package mode runs the same ACTUAL/SCHEDULED_ONLY, S47 C9, S45 DO_HELP, sever/restore, cold replay and wrong-root scenarios against that exact package.
- Package mode accepts only explicit `--original-tests none`; explicit `all`/`s47` now refuses with `PACKAGE_CLOSURE_ORIGINAL_TESTS_UNSUPPORTED` (exit 2) instead of silently reporting `NOT_RUN` and PASS. Prior 21/17/17 evidence remains historical.

## Exact result

- Command: `run_causal_harness.py --package-closure WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product --original-tests none`
- Elapsed: `69.457s`; checks: `22/22`; source audit: `424/424`.
- ACTUAL: material `0`, C9 material ineligible, DO_HELP `HELP_REFUSE`.
- SCHEDULED_ONLY: material `1`, C9 material eligible, DO_HELP `HELP_ACCEPT`.
- Same root: `3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`.
- Sever RED: `S46_INTERVAL_CONDITION_REVOKED`; restore same source and PASS.
- Cold replay PASS; wrong-root unresealed/resealed refused; B state preserved.

## Not changed

- No pinned S45-S47 source behavior, expected psychology or psychological rule changed.
- No PROGRAMMA canonical product, seam/gate register, protected PRE-MAIN content or other branch ref was edited.
- No native C8/C9/C12, CAN008/CAN011, ADP, Pyat or human authority.
- Independent review and PRE-MAIN receiving remain separate holds.

## Next owner action

An independent qualified reviewer may rerun package mode at the exact branch head. No PROGRAMMA promotion follows automatically from this delta.
