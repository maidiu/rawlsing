# SOROK S45-S47 causal regression harness

**RESULT:** `S45_S47_CAUSAL_HARNESS__EXACT_PINS__SAME_ROOT_ACTUAL_VS_SCHEDULED__S47_C9_AND_S45_DO_HELP__SEVER_RED_RESTORE_PASS__COLD_REPLAY__WRONG_ROOT_REFUSED__ORIGINAL_21_17_17__ENGINEERING_EVIDENCE_NOT_INDEPENDENT_REVIEW`.

**Grade:** `TEST_ONLY_ENGINEERING_CAUSAL_REGRESSION_NOT_INDEPENDENT_FINAL_REVIEW`.

This return is a separate executable causal regression harness. It is engineering
evidence, **not** an independent final review, acceptance, or native/psychological
issuance. No product code, expected psychology, or other worker return was
altered. All writes are confined to
`WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/**` plus its ignored
in-checkout `.runtime/` staging/logs.

## Commission and exact pins

- Whole-person receiving commission read at base
  `078d9c57bc835a34e90b3671bdef6c28a0f43747`
  (`WORKER_COMMISSIONS/SOROK-20261105-S45-S47-CANONICAL-SOURCEFREE-PRODUCT-RECEIVING-R1/00_COMMISSION.md`).
- S45 `f26a138e20d53c809d611cf8d834ec647b0804bf`
- S46 `f0ef39b92ce2e4add5c0a699389e12f1d7ae434e`
- S47 `765a441f87292aa4c17794745b65cb54e6aaa83f`

Exact dependency closure used by the harness:

| Key | Cut | Files checked exact |
|---|---|---|
| S45 | `f26a138e20d5` | 10 |
| S46 | `f0ef39b92ce2` | 10 |
| S47 | `765a441f8729` | 9 |
| S44 | `923278fbe6b0` | 11 |
| S43 | `3edd631fb6c3` | 14 |
| S42 + S47 seam | `765a441f8729` | 10 |
| S41 | `c72a10d284f8` | 14 |
| S40 | `79b0357c7af9` | 11 |
| S39 | `e41513fa6560` | 13 |
| S37 + S47 seam | `765a441f8729` | 23 |
| S36 | `8da78d8031a0` | 23 |
| R31J vendor closure | `64fec28c374d` | 141 |
| JOIN-E | `7bf2da302996` | 304 |
| Language mediation | `8d2920da951f` | 11 |
| M35 vendor inside S37 | `4170fbf19a9d` | 10 |

The S42/S37 seam-carrying trees are taken from the S47 cut because that is the
actual admitted S47 import closure. The seam files verified exact:

- `s42/event.py` `b33389a298f828610d04e45bde08fc1a8577a23275b4475cb8e5749cb68589ce`
- `s42/session.py` `5acdbb26b4dedcca9707483c3513f98358ffcf238b846dd959cdbabb28f1219d`
- `s37/producer.py` `cbc1a9531caf73b2c70c5ca4e6767b7f2c9e87f3756278555f27dfaee815c42d`

Every imported module resolved under the staged pin tree
(`modules_under_stage: true`), including `s45`, `s46`, `s47`, `s42`, `s37`,
`candidate`, `joined`, `language_mediation`, `bp1`, `bp4`, `r31e` and
`firstclass`.

## Callable harness

`run_causal_harness.py` accepts the repository/source package root and explicit
pinned paths:

```text
python3 WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/run_causal_harness.py \
  --source-root <repo-or-worktree> \
  --s45-return <exact-S45-return-dir> \
  --s46-return <exact-S46-return-dir> \
  --s47-return <exact-S47-return-dir> \
  --join-e-return <exact-JOIN-E-return-dir> \
  --language-return <exact-LANGUAGE_MEDIATION_R1-dir> \
  --original-tests all
```

`--package-root` aliases `--source-root`. Any pin can also be supplied with
`--pinned-path KEY=PATH`. Explicit paths are copied into the in-worktree stage
and verified against the pinned blobs before import; a modified or missing pin
fails closed. The interface and options are documented in `README.md`.

## Exact command and result

Executed from the bound workdir:

```text
/usr/local/bin/python3 WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/run_causal_harness.py --original-tests all
```

Result: **PASS**, exit `0`, elapsed `344.348s`. Environment: Python `3.11.3`,
pytest `9.1.1`, macOS `13.7.8` x86_64. Full machine-readable report:
`evidence/harness_run.json`. The harness was also smoke-run with all five
explicit pinned paths; it returned PASS with the same causal results.

Original focused suites, re-executed from the exact staged pins:

| Suite | Result | Elapsed |
|---|---|---|
| S45 | 21 passed, 0 failed/error/skipped | 127.326s |
| S46 | 17 passed, 0 failed/error/skipped | 42.518s |
| S47 | 17 passed, 0 failed/error/skipped | 90.601s |

JUnit and logs: `evidence/junit/*.xml`, `logs/s45_full.log`,
`logs/s46_full.log`, `logs/s47_full.log`.

## Same-root causal result

Both modes use the same S45 fixture seed and reconstruct the same root:
`3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`.

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

The same user-visible `DO_HELP` consequence changes through the actual S47 C9
material readset, not through a harness-side expected-psychology rule. Cold
reopen of both state roots reproduced the same root, the same event-bound S47
source hash, the same material eligibility, the same SAY/DO_HELP/ATTEND
encounter chain and `verify().ok == true`.

## Sever dependency RED -> restore PASS

Supported dependency cut and restore on the actual S46 condition:

- Cut: second admission refused with `S46_INTERVAL_CONDITION_REVOKED` (RED).
- Historical first C9 event still returned its admitted S47 source with
  `s47_source_in_readset: true` and `present_condition_revoked: true`.
- Restore: source reconstructed bit-identically
  (`e196c974e43a...`), second admission PASS, C9 source in readset,
  `objective_material_eligible: false`, target `NO_CHANGE`/`NO_PROPOSAL`.
- Cold reopen: first and second event-keyed C9 reads returned the same admitted
  source hashes and `verify().ok == true`.

## Wrong-root negative

Two same-person sessions with different root seeds produced distinct roots:

- Root A: `3bcb21fc22df...`
- Root B: `b43c92c076ae...`

Substituting root A's interval source into root B's supported S47 qualification
gate:

- Unresealed foreign source: refused `S47_SOURCE_AS_OF_MISMATCH`.
- Resealed foreign source with B's `as_of`: refused
  `S47_SOURCE_INTERVAL_STATE_ID_MISMATCH`.
- B's own source remained accepted and unchanged
  (`de80ffb1f0bb...`).
- A normal B admission then used B's own source in C9, not A's.

The supported qualification seam therefore refuses a foreign-root substitution.
A harness-only private-hook injection that bypasses `qualify_source` is outside
the supported interface and is deliberately not counted as product behavior.

## Exact imports and source custody

`evidence/harness_run.json` contains the per-file pin manifest, git blob SHA-1s,
SHA-256s, seam rows, module origins, commands, environment and every scenario
result. `evidence/junit/*.xml` are the original test receipts. `logs/*.log` are
the captured original test and harness stdout. The stage is reproducible from
the local git object store and lives only in ignored `.runtime/`.

## Limitations

- TEST_ONLY sourcefree synthetic roots and TEST_ONLY installed-simulation owner
  material. No empirical probability, CAN008/CAN011, native C8/C9/C12/ADP,
  developmental T, childhood biography, Pyat native world, human A5/Gate4/Gate5
  or user study is claimed.
- The harness proves engineering conditional causality at the pinned cut. It
  does not prove native psychology, a real respondent, external message
  delivery, paid action, or independent acceptance.
- The reader is author-side engineering evidence, not the different qualified
  independent reviewer required for final receiving.
- Private-hook source injection outside `qualify_source` is not a supported seam
  and was not treated as an accepted product path.
- No provider call, network action, external channel or human trial occurred.
- No product code, expected psychology or other worker return was modified.
- A broad S37/S42/S44 or whole-estate regression was not run; this harness reran
  the three requested focused author suites plus the causal scenario chain.

## Branch and publication

Branch: `codex/sorok-s45-s47-causal-harness-20261105-r1`. Base:
`078d9c57bc835a34e90b3671bdef6c28a0f43747`. The pushed harness commit and
publication receipt are in `PUBLICATION_RECEIPT.json`.

## PROGRAMMA_DELTA

See `PROGRAMMA_DELTA.md` / `PROGRAMMA_DELTA.json`: the delta is engineering
evidence and a callable harness only. No PROGRAMMA canonical product, native
science, seam register, gate register or receiving authority is changed.
