# SOROK S45-S47 PRODUCT IMPORT CLOSURE R1 — RETURN

## ACTUAL_HQ_AND_BRANCH

- Lane: OC-A, product import/manifest/code closure and fresh CLI.
- Host: OpenCode / DeepSeek V4.1-Flash, local S2 shell.
- Workdir: `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-s35-c9r-access-r1`
- Branch: `codex/sorok-s45-s47-closure-20261105-r1`
- HEAD at publication: `078d9c57bc835a34e90b3671bdef6c28a0f43747`
- Publication: scoped working-tree return at `WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/`; not committed, not merged, not pushed.
- Other worker branches were not edited: `codex/sorok-s45-s47-causal-harness-20261105-r1` and `codex/sorok-s45-s47-projection-20261105-r1` remain at the same HEAD.

## SOURCE/CODE_DISPOSITIONS_AND_HASHES

- `SOURCE_MANIFEST.json` pins 417 source/test blobs, 4,536,618 bytes.
- Manifest SHA-256: `ab87a09c22733bc6b987e3a9c99a7348a4d50bdab0576a2f3daa5cf01078ec58`.
- Source audit: 417/417 files present and SHA-256 matched; no missing or drifted sources.
- Pinned semantic roots: S36 `8da78d80`, S37 `e1f3c1da`, S39 `e41513fa`, S40 `79b0357c`, S41 `c72a10d2`, S42 `2489f8cd`, S43 `3edd631f`, S44 `923278fb`, S45 `f26a138e`, S46 `f0ef39b9`, S47 `765a441f`, JOIN-E `7bf2da30`, LANGUAGE `8d2920da`, live `rawlsing_next` `7bf2da30`.
- Three interface blobs are taken at the cumulative S47 cut `765a441f` because the earlier S37/S42 copies lack the required S47 conditioning-source seam:
  - `S37/s37/producer.py` blob `cf6f970ff12faa2003c43b0261fc7d6497efa356`
  - `S42/s42/event.py` blob `0aa6c3503e8d520a9bd6af58af4cabf3b7cc2366`
  - `S42/s42/session.py` blob `073f115b0aa71b9e609cd84a22b79907fe1b724e`
- These are pinned consumer-side bytes, not a new choice rule, not a rewritten scientific rule, and not a native grant.
- Import closure: 279 imported modules in the retained demo run, 170 local, 109 stdlib, 0 external. No Desktop, worktree, temporary staging, or other-checkout source remained in the import graph.

## AUTHOR_EXECUTED_S2_WITH_PROOF

- Fresh CLI: `product/run_s45_s47.py` (also `product/sorok-s45-s47`).
- Commands executed from the bound workdir:
  - `python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py manifest`
  - `python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py demo --root .local-logs/s45-s47-closure/final --keep`
  - `python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_reused_tests.py --junitxml .local-logs/s45-s47-closure/run-2/reused-tests.xml`
  - Fresh CLI smoke actions: `new`, `say`, `do-help`, `attend`, `interval`, `admit`, `c9`, `verify`.
- Source audit exit 0; manifest/import audit exit 0.
- Retained demo exit 0; all ten top-level checks true; cold subprocess exit 0 and returned the same event-local source hash.
- Reused pinned tests: `55 passed in 260.35s` (S45 21, S46 17, S47 17).
- Focused S47 rerun: `17 passed in 90.52s`.
- Python 3.11.3; pytest 9.1.1; Darwin x86_64.
- Evidence: `evidence/DEMO.json`, `evidence/REUSED_TESTS.log`, `evidence/REUSED_TESTS.xml`, `evidence/S47_FOCUSED_TESTS.log`, `evidence/MANIFEST_AUDIT.json`, `evidence/cli/`.
- Exact machine readback: `READBACK.json` (the file itself carries authored-file hashes and the publication-tree census; its external SHA-256 is reported in the final chat readback).

## ACTUAL_USER_PERCEIVED_CAUSAL_CHANGE

Same pinned same-root person, two interval modes:

- S45 baseline: SAY `HELP_INVITE`, DO_HELP `HELP_ACCEPT`, ATTEND `NO_CHANGE`; cold reopen preserved root and encounter count.
- ACTUAL: material `1 -> 0`; interval `PARTIAL`, coverage `[[222, 223]]`; event-local C9 source in readset with `objective_material_eligible=false`; DO_HELP `HELP_REFUSE`, accepted `false`; cold reopen preserved the same C9 source hash `e196c974e43a024055949113f6b875be8c012f1c422d6829d4890e8a46688658`.
- SCHEDULED_ONLY: material remains `1`; interval `NOT_PERFORMED`, coverage `[]`; event-local C9 source in readset with `objective_material_eligible=true`; DO_HELP `HELP_ACCEPT`, accepted `true`; cold reopen preserved C9 source hash `d73a00eff7209a6a6fa504fedd46912d5182e00f1d74ead3161dd29c8f494665`.
- Event-local proof: after a later interval, the first admitted event still reads its own first source hash `e196c974...` while current source hash is the later `da322d47...`; cold read repeats the first event's historical source.
- Cut/restore proof: condition cut refuses with `S46_INTERVAL_CONDITION_REVOKED`; restore reconstructs the same source hash and C9 consumes it.
- Admission-time source proof: interval-end source is access `granted` with hash `d73a00ef...`; after DO_HELP consumes material, admission source is access `denied` with hash `f4af9492...`; event-local C9 uses the admission source, not the stale interval-end hash.

## B_INDEPENDENT_SOURCE_STATUS

No B-actor positive is claimed or fabricated. S48/S49/S50/S51/S52 current-root B holds remain separate: no B-owned current-root context, no historical V3 BackboneState, no independent paid counterpart or performed paid action. This return does not use a fixture as actual B and does not invent B personality from material or demographic roots.

## REUSED_VERSUS_NEW_CODE

- Reused pinned source: S36, S37, S39-S47, JOIN-E, language mediation, and pinned live `rawlsing_next` modules m1-m6 plus the v3 zero-positive guard.
- New code only: thin local bootstrap, source/import audit, fresh CLI, reused-test runner, and evidence assembly.
- No semantic source edits were made. The three integration-cut blobs are exact pinned bytes from the S47 cumulative cut; they supply the already-authored conditioning-source interface required by S47.

## INDEPENDENT_REVIEW_AND_EXACT_SHA

- Independent scoped review: `NOT_RUN`.
- Corrected exact publication tree: working tree at HEAD `078d9c57bc835a34e90b3671bdef6c28a0f43747` plus this uncommitted return directory.
- `READBACK.json` and `SOURCE_MANIFEST.json` are the exact content readback. A different qualified worker must review the exact tree before self-consistent acceptance is claimed.

## PREMAIN_SELECTIVE_RECEIVING

- PRE-MAIN selective PR/merge: `NOT_PREPARED`.
- This is an OC-A import closure and first-consumer CLI tranche, not the protected merger. The lead must decide whether/how to commit, obtain independent review, and prepare selective PRE-MAIN receipt.

## PYAT_E001/E002

Unchanged. No Pyat native C11 selected world, no source/release/version/root/rights/revocation package, no owner-qualified first importer, and no Sorok C11-to-C4 actor genealogy/position binding was issued. This return does not write Pyat mechanics.

## ORIGINAL_SCIENCE/HUMAN_GATES

- CAN008 Rule A: not issued.
- CAN011 O05 acquired PRACTICE / O07 evaluated NO_CHANGE: not issued.
- Independent ADP person sources: not issued.
- C8 original security and native C9/C12 authority: not issued.
- Pyat native selected world: not issued.
- Human S11/A5 Gate4/Gate5, human usability, and external message delivery: not run.
- Grade remains `TEST_ONLY_SOURCEFREE_S45_S47_PRODUCT_CLOSURE_NOT_NATIVE`.
- All native grants are false: actor, rule, source, human, C8, C9, C12.
- Target proposals remain empty and target branch remains `NO_CHANGE`.

## OPERATION

```text
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py demo
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py new --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py say --state <path> "Can I help?"
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py do-help --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py attend --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py interval --state <path> --mode ACTUAL --span 4
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py admit --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py c9 --state <path>
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py verify --state <path>
```
