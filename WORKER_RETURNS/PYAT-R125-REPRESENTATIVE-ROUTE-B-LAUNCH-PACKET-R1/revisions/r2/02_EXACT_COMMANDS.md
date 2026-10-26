# R126 — exact non-source commands

**Status:** `BOUND_READ_ONLY_NON_SOURCE_OPERATION__FULL_SOURCE_LAUNCH_NOT_READY`

R126 executed no source, raw, DTA/SAV, archive, code, test, or production
operation. The commands below are the bound non-source retrieval/check actions.
The first command is the selected next operation. The later decision is the
first missing preimage/decision; it is not a source-use request.

## N1 — retrieve and verify the retained LiTS authority package

This is the one concrete next operation. It retrieves the actual retained
source-specific projection authority package, not a substitute and not source
bytes.

```sh
R126_TMP="${TMPDIR:-/tmp}/r126-lits-authority-check"
mkdir -p "$R126_TMP"
git cat-file -p \
  01762d7379be4e423dad3e21bcdcee47c536902d:WORKER_RETURNS/PREMAIN-FIABC-LITS-CANONICAL-EMPIRICAL-CLOSURE-SOURCEBACKED-R1/court/oracle_producers/LITS_I/_be1_lits_projection/_be1_immutable/3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/AS2A_LITS1_SHARED_CERTIFICATION_20260827/04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json \
  > "$R126_TMP/lits_projection_authority.json"
test "$(wc -c < "$R126_TMP/lits_projection_authority.json" | tr -d ' ')" = "5275"
test "$(shasum -a 256 "$R126_TMP/lits_projection_authority.json" | cut -d' ' -f1)" = "8bfc5c19da384bcbc1a73219f5412bf5045b7296ff5a9cfd9f6e6d99df9db621"
shasum -a 256 "$R126_TMP/lits_projection_authority.json"
```

Expected: 5,275 bytes; SHA-256
`8bfc5c19da384bcbc1a73219f5412bf5045b7296ff5a9cfd9f6e6d99df9db621`;
Git blob `174b931e8aa89111086e3d46159b47154bed7f16`.

This package binds:

- LiTS-I source SHA-256
  `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- 29,002 rows × 1,198 variables;
- certified active response slots `q301_2`, `q301_7`, `q312_3`, `q315_1`,
  `q511`;
- bounded proving/positive response slots `q301_2`, `q301_7`;
- routing `ELIGIBLE_APPLICABLE__SECTION3_UNCONDITIONAL` for both bounded slots;
- selected-respondent role for Sections 3–7, with identity key
  `source_sha256 + 1-based row ordinal + SELECTED_RESPONDENT`;
- positive coordinate slots `city`, `country`, `region`, `tablec`, `tabled`;
- raw unweighted limit (`NONE__RAW_UNWEIGHTED`);
- 29 source-present country codes and the bounded source universe;
- exact 1,198-slot ownership/projection/exclusion ledger SHA-256
  `65bdb972c2004d7ea6539b991125d2111e3705aee2d3e76159208d04e4a3fa60`;
- exact universe specification identity
  `urn:rawlsing:pre553:as2a:universe:sha256:834f9be5c5838226abcc9f0af96f2f582eac8bec2944c514ce52680f45faf99f`.

It does not bind current source/host/purpose/use, a current
`NativePreimageBundle` (including `risk_set_ref`), or a current positive
`AuthoritySnapshot`.

## N1-evidence — check the retained missing-authority evidence

These are read-only aggregate checks. They are not a source read and not a
checkpoint recovery.

```sh
git cat-file -p \
  01762d7379be4e423dad3e21bcdcee47c536902d:WORKER_RETURNS/PREMAIN-FIABC-LITS-EXECUTED-ROLE-CLOSURE-REPAIR-AND-SOURCE-RETRY-R1/source_free_role_authority_audit.json \
  > "$R126_TMP/lits_role_authority_audit.json"
test "$(shasum -a 256 "$R126_TMP/lits_role_authority_audit.json" | cut -d' ' -f1)" = "5d0c9843d7972c70a9e1d297402d71fdc07ea69b9bebc9ad6d45c87034155ff3"

git cat-file -p \
  01762d7379be4e423dad3e21bcdcee47c536902d:WORKER_RETURNS/PREMAIN-FIABC-LITS-EXECUTED-ROLE-CLOSURE-REPAIR-AND-SOURCE-RETRY-R1/checkpoint_disposition.json \
  > "$R126_TMP/lits_checkpoint_disposition.json"
test "$(shasum -a 256 "$R126_TMP/lits_checkpoint_disposition.json" | cut -d' ' -f1)" = "8ed57d8f7fa0254e7c5a2c8622ef55ac8a86f0482f8a511d2fabcb58fa49d4bf"

git cat-file -p \
  01762d7379be4e423dad3e21bcdcee47c536902d:WORKER_RETURNS/PREMAIN-FIABC-LITS-EXECUTED-ROLE-CLOSURE-REPAIR-AND-SOURCE-RETRY-R1/zero_source_checkpoint_resume_receipt.json \
  > "$R126_TMP/lits_zero_source_resume.json"
test "$(shasum -a 256 "$R126_TMP/lits_zero_source_resume.json" | cut -d' ' -f1)" = "390d0d42d5d544ebc815c04222224acf39b94da7d9bedcda61358159c53fb580"
```

Expected evidence:

- missing authority id:
  `urn:rawlsing:prev3:p2r4a:pre553:mixed-predicate-grammar`;
- version: `1.0.0-candidate`;
- content hash:
  `0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55`;
- checkpoint document written: `false`;
- zero-source resume: `NOT_RUN_NO_CHECKPOINT_DOCUMENT`.

The exact affected fact is:

```text
EmpiricalFact  urn:rawlsing:pre553:EmpiricalFact:sha256:c5b0e1ed85d2ae0c0714efeabf1b951ae827995d65441d419e45aac57b8057fc
QuerySpec      urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:3419fd8377bd3b681315191bd22a3c37a95443946c0a0477b2c591e6690bfbd0
Predicate      urn:rawlsing:pre553:EmpiricalPredicate:sha256:3dba42ac25eb61d46958587c46ecacbb4fff83f87de535a72d0d793e5c49b508
typed state    SUPPORTED
denominator    1191
topology       arity 1, SEMANTIC_ORDERED
target domain  cff1766e654eef4c8769618d34f406e570ec3fe82a93b1a5db900fe1377d416f
```

This is the current retry's affected fact, not a complete workload or the old
candidate-count scope.

## N2 — bounded recovery decision for the missing AuthoritySnapshot

The retained fixture is:

```text
rawlsing_next/tests/fixtures/ee_p2r6a_r4a_03_mixed.json
blob a18fd79609f080062b93dfe0e2bab8e9bf865af3
5,278 bytes
SHA-256 16661cdbf6067acb79ac0bed1ba3b9be5497f523fb51c5ae95b1c79ceba08ba9
status CANDIDATE__HQ_ADOPTION_REQUIRED
```

Read-only check:

```sh
git cat-file -p HEAD:rawlsing_next/tests/fixtures/ee_p2r6a_r4a_03_mixed.json \
  > "$R126_TMP/mixed_predicate_authority_candidate.json"
test "$(shasum -a 256 "$R126_TMP/mixed_predicate_authority_candidate.json" | cut -d' ' -f1)" = "16661cdbf6067acb79ac0bed1ba3b9be5497f523fb51c5ae95b1c79ceba08ba9"
```

The competent authority/HQ owner must make exactly one of these bounded
decisions:

1. **ADOPT** the exact candidate `urn:rawlsing:prev3:p2r4a:pre553:mixed-predicate-grammar`
   version `1.0.0-candidate`, content hash
   `0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55`
   as a current positive `AuthoritySnapshot`; or
2. **SUPPLY** an exact positive `AuthoritySnapshot` with the same
   `authority_id`, `authority_version`, and `authority_content_hash` from
   competent custody, with its exact issuer/currentness evidence.

The bounded external access, if the positive snapshot is held outside Git, is
read-only access to that exact authority object. This is not a request for LiTS
raw source, an unbounded source-use signature, a synthetic positive snapshot, or
a version relabelling. No source read is required to resolve this authority
gap.

## N3 — full source launch remains NOT_READY

No source execution command is bound. The exact R03 APIs are recorded, but their
values are not:

| API | Exact binding state |
| --- | --- |
| `admit(workload, resolver, *, host, purpose, allow_test_only=False, expected_wave=None)` | `NOT_BOUND__NO_CURRENT_ISSUED_WORKLOAD` |
| `execute_issued_workload(workload, resolver, *, source_factory, host, purpose, allow_test_only=False, prior_receipts=(), max_units=None, expected_wave=None)` | `NOT_BOUND__NO_CURRENT_ISSUED_WORKLOAD_OR_SOURCE_FACTORY` |
| `compile_governed_frontier(*, bundle, inventory, policy, frontier, as_of, host, purpose)` | `NOT_BOUND__NO_CURRENT_BUNDLE_INVENTORY_POLICY_FRONTIER_OR_CUSTODY` |
| `execute_governed_frontier(*, compilation, source_factory)` | `NOT_BOUND__NO_CURRENT_COMPILATION_OR_SOURCE_FACTORY` |
| `restore_governed_frontier_ledger(ledger, *, expected_checkpoint_ref=None)` | `NOT_BOUND__NO_VALID_CURRENT_CHECKPOINT_DOCUMENT` |

M1/M2/B5 are likewise recorded as exact accepted symbols/signatures, not as an
imagined executable lifecycle. See `01_BOUND_NEXT_OPERATION.json`. In
particular:

- `M2Repository.release_exact(ref)` is the repository method;
- `resolve_release_exact(repository, release_ref, *, publication_binding_refs=(), unavailable_binding_refs=())`
  is the module function;
- B5 exact methods are `register_product`, `publish_product`,
  `select_current`, `resolve_current_as_of`, and `declare_invalidation`.

The R125 R43 path
`WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/repro/execute_permitted.py`
is absent at candidate HEAD and is not reused. No substitute historical
35-wave command is proposed.

## No tests claimed

R126 ran no test suite and executed no code. The retained source-free
qualification receipt is historical evidence only. The current LiTS checkpoint
was not written; its zero-source resume was not run.

## Limits

- No raw/source/DTA/SAV/archive read or source hash pass.
- No code-tree change, new engine/runner, host/CI/prod/actor grant, or scientific
  decision.
- Historical retained checkpoint/oracle/closure hashes are comparison evidence,
  not current permission or execution.
- Historical 50/77/60/50 and WVS7 46 counts are not current scope or acceptance.
- WVS7 remains an alternative retained comparator; its current use permission is
  not verified and no fresh raw read is proposed.
- Holds remain: original 35/1890/global F6/F7/F8, source/science, actor/dyad/V3,
  R09/CI/prod, N11/N12, Sorok, J52/W52.
