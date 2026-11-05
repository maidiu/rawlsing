# SOROK S45-S47 PRODUCT IMPORT CLOSURE R1 — INTEGRATED RETURN

## ACTUAL_HQ_AND_BRANCH

- Lane: OC-A import closure plus concrete product integration with the public projection adapter and causal harness.
- Host: OpenCode / DeepSeek V4.1-Flash, local S2 shell.
- Workdir: `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-s35-c9r-access-r1`
- Branch: `codex/sorok-s45-s47-closure-20261105-r1`
- Published history: package `e42faf01b57a9188f0cf75baaccfcd57edb07173`; public projection `39ff2c2d479d8ad71c156b01c168894527a486e4` cherry-picked as `4e9ebc85d78995e93a7fbace0ead78d703067244`; causal harness `3d6207983b62646108d4c6e3ff1a3b4d65674977` cherry-picked as `5531492df2317166d223e6c6bc211b147e0912f7`.
- The integration commit is this branch head; its exact hash is returned in the final chat readback. Parent is `5531492df2317166d223e6c6bc211b147e0912f7`.
- The separate original public/worker branch refs were not edited; integration is scoped to this closure branch.

## SOURCE/CODE_DISPOSITIONS_AND_HASHES

- `SOURCE_MANIFEST.json` now pins 424 source/test blobs, including WP19 and S11 projection dependencies.
- Manifest SHA-256: `2535398efa2c376731aec17cd7b2ceda2e0fee477f064ae049870393b838b94b`.
- Source audit: 424/424 files present and SHA-256 matched.
- Pinned semantic roots: S36 `8da78d80`, S37 `e1f3c1da`, S39 `e41513fa`, S40 `79b0357c`, S41 `c72a10d2`, S42 `2489f8cd`, S43 `3edd631f`, S44 `923278fb`, S45 `f26a138e`, S46 `f0ef39b9`, S47 `765a441f`, JOIN-E `7bf2da30`, LANGUAGE `8d2920da`, WP19 `3c4df43f`, S11 `faec7ce9`, live `rawlsing_next` `7bf2da30`.
- Three interface blobs remain taken at the cumulative S47 cut `765a441f`: `S37/s37/producer.py` `cf6f970f...`, `S42/s42/event.py` `0aa6c350...`, `S42/s42/session.py` `073f115b...`. These are exact consumer bytes, not a new rule or native grant.
- Integration wiring: `s45_projection` installs the shipped package closure by default; the harness has a `--package-closure` mode that audits and imports that same package rather than an independent git extraction.
- Projected demo import audit: 284 modules, 175 local shipped-checkout modules, 109 stdlib, 0 external checkout/temp/Desktop modules. Projection modules are the adjacent shipped `WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1` return, not an external checkout.

## AUTHOR_EXECUTED_S2_WITH_PROOF

- `python3 -B WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py manifest`
- `python3 -B WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py demo --root .local-logs/s45-s47-integration/final/demo --keep`
- `python3 -B -m pytest -q -p no:cacheprovider --junitxml=WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1/evidence/junit.xml WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1/tests` → 11 passed in 30.08s against the shipped package closure.
- `python3 -B WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/run_causal_harness.py --package-closure WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product --original-tests none` → PASS, all 22 checks true, source audit 424/424, package modules under closure.
- Single user-facing CLI smoke: projected `new`, `view`, `view --text`, `say`, `do-help`, `attend`, `wait`, `status`; engineering interval/admit/C9 retained.
- Projected demo exit 0; all ten top-level checks true; cold subprocess exit 0 and same event-local source hash.
- Full S45/S46/S47 author suites were not rerun in this integration; prior `55 passed` (S45 21, S46 17, S47 17) evidence remains in this return and git history. The package-mode harness records `original_tests: NOT_RUN` with reason `PACKAGE_CLOSURE_MODE_AVOIDS_DUPLICATE_FULL_SUITES`.
- Evidence: `evidence/DEMO.json`, `evidence/MANIFEST_AUDIT.json`, `evidence/PROJECTION_PACKAGE_TESTS.log`, `evidence/cli/`, plus projection and harness return evidence.
- Exact machine readback: `READBACK.json`, carrying authored-file hashes, publication-tree census and exact run hashes.

## ACTUAL_USER_PERCEIVED_CAUSAL_CHANGE

One root per interval mode; projected WP19 results consume actual S45/S46/S47 outcomes:

- S45 baseline: projected SAY `OK` / `HELP_INVITE`, DO_HELP `OK` / `HELP_ACCEPT` with actor `REPAIR` performed by A, ATTEND `NO_CHANGE`; user attempt remains `performed=false`; cold reopen preserved root and counts.
- ACTUAL: material `1 -> 0`; interval `PARTIAL`, coverage `[[222, 223]]`; event-local C9 source in readset with `objective_material_eligible=false`; projected DO_HELP `REFUSED` / `HELP_REFUSE`; SAY also refuses after material is gone.
- SCHEDULED_ONLY: material `1`; interval `NOT_PERFORMED`, coverage `[]`; event-local C9 source in readset with `objective_material_eligible=true`; projected DO_HELP `OK` / `HELP_ACCEPT`.
- Event-local proof: first admitted event keeps source `e196c974...` after later source `da322d47...`; cold read repeats the first event's historical source.
- Cut/restore: `S46_INTERVAL_CONDITION_REVOKED`, restore reconstructs the same source hash, then admission passes.
- Admission-time source: interval-end `d73a00ef...` access `granted`; admission-time `f4af9492...` access `denied`; C9 uses the admission-time source, not stale interval-end fields.
- Privacy: projected views/results pass the projection privacy walker; no private actor state, history refs, source refs, admission IDs, plan hashes or hidden fields are exposed.
- Harness package-mode same-root result: ACTUAL refused, SCHEDULED accepted, sever RED, restore PASS, cold replay PASS, wrong-root unresealed/resealed refusal PASS, other-actor state preserved.

## B_INDEPENDENT_SOURCE_STATUS

No B-actor positive is claimed or fabricated. S48-S52 current-root B holds remain separate. This return does not use a fixture as actual B, invent B personality, or claim an owned current-root B context.

## REUSED_VERSUS_NEW_CODE

- Reused exact pinned source: S36, S37, S39-S47, JOIN-E, language mediation, WP19, S11, and pinned live `rawlsing_next` modules.
- New integration code only: package-first projection runtime, package-mode harness audit/configuration, projected commands in the single product CLI, WP19/S11 pins, and updated evidence/returns.
- No psychological rule, expected outcome, S45-S47 source behavior or native authority was changed.

## INDEPENDENT_REVIEW_AND_EXACT_SHA

- Independent scoped review: `NOT_RUN`.
- Exact review target: the integration commit on this branch; exact head is returned in the final chat readback.
- `READBACK.json`, `SOURCE_MANIFEST.json`, projection test evidence and harness package-mode evidence are the exact content receipts. A different qualified worker must review the exact commit before acceptance is claimed.

## PREMAIN_SELECTIVE_RECEIVING

- PRE-MAIN selective PR/merge: `NOT_PREPARED`.
- This is scoped integration evidence, not the protected merger. The lead must obtain independent review and prepare selective PRE-MAIN receipt.

## PYAT_E001/E002

Unchanged. No Pyat native C11 selected world, source/release/version/root/rights/revocation package, owner-qualified first importer, or Sorok C11-to-C4 actor genealogy/position binding was issued.

## ORIGINAL_SCIENCE/HUMAN_GATES

- CAN008 Rule A: not issued.
- CAN011 O05 acquired PRACTICE / O07 evaluated NO_CHANGE: not issued.
- Independent ADP person sources: not issued.
- C8 original security and native C9/C12 authority: not issued.
- Pyat native selected world: not issued.
- Human S11/A5 Gate4/Gate5, human usability, external message delivery: not run.
- Grade remains `TEST_ONLY_SOURCEFREE_S45_S47_PRODUCT_CLOSURE_NOT_NATIVE`; all native grants false; target proposals empty and target branch `NO_CHANGE`.

## OPERATION — SINGLE USER-FACING CLI

```text
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py new --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py view --state <path> [--text]
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py say --state <path> "Can I help?"
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py do-help --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py attend --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py status --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py wait|exit|return|absence --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py interval --state <path> --mode ACTUAL --span 4
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py admit --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py c9 --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py demo
```
