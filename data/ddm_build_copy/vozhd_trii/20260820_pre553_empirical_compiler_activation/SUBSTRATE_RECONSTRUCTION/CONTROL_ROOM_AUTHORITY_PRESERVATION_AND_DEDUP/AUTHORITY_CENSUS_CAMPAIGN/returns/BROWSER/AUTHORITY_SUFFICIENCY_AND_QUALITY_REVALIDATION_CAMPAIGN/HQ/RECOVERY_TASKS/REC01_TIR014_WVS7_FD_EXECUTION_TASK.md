# REC-01 — TIR-014 WVS7 Occurrence Functional-Dependency Execution Task

Status: `BINDING__HQ_AUTHORIZED__LOCAL_CODEX_SOURCE_EXECUTION__IDIOT_PROOF_PROTOCOL`

## 0. Purpose

This task answers **one question only**:

> For WVS Wave 7 `Q152`–`Q157`, is the semantic event-occurrence / rank-slot identity required by C11 deterministically reconstructible from immutable source identity + governed authority, or does some independent occurrence information have to persist?

This is **not** an architecture-selection task. It does not choose SAV/DTA vs Parquet, source-backed vs LONG, DuckDB, cache policy, or C09 candidate architecture.

The worker is not asked to invent an FD test. The test and decision rules are fixed below.

## 1. Exact jurisdiction

TIRs:

- `TIR-014`
- `TIR-064`

Source family/wave:

- WVS Wave 7 only.

Variables:

- `Q152` + `Q153`
- `Q154` + `Q155`
- `Q156` + `Q157`

Do **not** expand to other WVS waves, EVS, LiTS, or other ranking/multiple-response objects.

## 2. Environment

Required execution environment:

`LOCAL_CODEX_SOURCE_EXECUTION`

Permitted local evidence:

- exact governed WVS Wave 7 source binary/member;
- governed source-certification/hash authority for that exact source;
- exact P2 implementation identity for the six variables;
- governed C11 projection / source-backed projection code and contracts;
- exact PD01/current occurrence/multiplicity probes referenced by R06;
- ExactRef/replay authority needed to identify the compared fields.

Forbidden:

- broad home-directory search;
- unrelated repository archaeology;
- unrelated survey families;
- architecture changes;
- canonical authority mutation;
- editing source bytes;
- inventing replacement IDs to make the FD pass.

## 3. Preflight — complete before any source scan

The worker MUST perform these checkpoints in order.

### P0 — repository and branch

Record:

- repository absolute path;
- current branch;
- current HEAD.

The launch message supplies the required exact start HEAD and worker branch.

If HEAD is not exact before worker changes begin:

`STOP__WRONG_START_HEAD`

Do not rebase, merge, or force-reset to hide divergence.

### P1 — governing authority read

Read, at minimum:

1. `HQ/AUTHORITY_REVALIDATION_FINAL_ADJUDICATION.md`
2. `HQ/CHETIRI_RECOVERY_AND_LOCAL_ESCALATION_QUEUE.csv`
3. this task file;
4. R06 `RETURN_ADJUDICATION_PROPOSAL.md`;
5. R06 `OPEN_HQ_QUESTIONS.md`;
6. R00 `TERMINAL_INFORMATION_REQUIREMENT_UNIVERSE.csv` rows for TIR-014 and TIR-064;
7. R00 `R00_LOCAL_EVIDENCE_ESCALATION.md`.

Then locate only the exact C11 / PD01 / WVS7 authorities cited by those files.

### P2 — exact source identity

Before reading source values, write down:

- exact local source path/member;
- expected governed SHA-256;
- independently calculated local SHA-256;
- equality result.

If expected SHA is unavailable:

`STOP__GOVERNED_SOURCE_HASH_UNAVAILABLE`

If local hash != governed expected hash:

`STOP__SOURCE_HASH_MISMATCH`

Do not continue with a substitute source.

### P3 — freeze the field binding

Before writing the FD test, create a small binding table containing the **exact field names** used for:

#### X — determinant tuple

The governed determinant is conceptually:

1. source snapshot identity;
2. source row ordinal / respondent replay identity;
3. exact source variable / P2 implementation identity;
4. source-native parent object;
5. source-native slot/rank role;
6. raw physical state.

Map each of these six concepts to the exact project/source field or deterministic governed derivation used in this court.

#### Y — required occurrence identity

List every C11 field that the governing C11 contract says is **identity-bearing for semantic event occurrence / slot identity** in this domain.

Do not guess the Y fields from names. Cite the exact C11 authority line/file for each field.

If the governing material does not let you determine X or Y unambiguously:

`STOP__FIELD_BINDING_AMBIGUOUS`

The worker may not choose a convenient weaker Y.

## 4. Build the bounded census

After P0–P3 pass:

1. enumerate every source row in the exact WVS7 source;
2. inspect only `Q152`–`Q157` plus fields needed for replay/source-row identity;
3. emit one physical-cell record per row × named source variable;
4. classify each cell as:
   - populated ordinary/substantive state;
   - typed special state;
   - typed missing/absence state;
   - source-invalid/unreadable state if any;
5. project/replay the corresponding governed C11 representation using the existing governed path;
6. attach frozen X and Y fields.

Do not drop missing/special states from the census. The FD substantive test is on populated occurrences, but absence preservation is a separate mandatory test.

## 5. The FD test — implement exactly this logic

### 5.1 Populated occurrence test

For every populated occurrence:

```text
emit X = (
  source_snapshot_id,
  source_row_ordinal,
  implementation_identity,
  source_native_parent,
  source_native_slot_or_rank,
  raw_physical_state
)

emit Y = tuple(all governed C11 occurrence-identity fields frozen in P3)
```

Then:

```text
GROUP records BY X

FOR each X group:
    compute DISTINCT Y values
    IF distinct_Y_count > 1:
        record FD_COLLISION
```

Also test the inverse practical reconstruction condition:

```text
FOR each populated source physical cell:
    exactly one governed Y must be reconstructible
```

If a physical cell produces zero Y values, record `MISSING_PROJECTION`.

If it produces more than one Y value, record `AMBIGUOUS_PROJECTION`.

### 5.2 Determinant provenance test

For every component of X, classify it as:

- immutable source fact;
- deterministic derivation from immutable source + already-governed authority;
- information available only from a transformed/materialized event carrier;
- unknown.

If any determinant necessary to make the FD pass exists only in the transformed event carrier, the court has **not** proved source reconstruction.

Record `CARRIER_ONLY_DETERMINANT`.

### 5.3 Typed absence test

For every source row × Q152–Q157 cell that is not a populated substantive occurrence:

verify that source-native distinctions required by the response/C11 contract remain distinguishable after governed projection/reconstruction.

At minimum, do not collapse distinct governed states merely because both appear as null-like values in a programming language.

Record every collapse as `TYPED_ABSENCE_COLLISION`.

### 5.4 Slot/rank preservation test

Explicitly verify that first/second rank roles cannot collapse:

- Q152 vs Q153;
- Q154 vs Q155;
- Q156 vs Q157.

Do not treat different source-column names as sufficient proof by themselves. Verify the frozen Y occurrence/slot identity preserves the distinction under reconstruction.

## 6. Exhaustiveness checks

Before any substantive verdict, all of the following MUST equal PASS:

- exact source SHA verified;
- all source rows scanned;
- all six named variables scanned;
- populated occurrence count reconciles to source scan;
- every populated source cell has exactly one tested X record;
- every populated source cell has exactly one compared Y projection or an explicit recorded exception;
- all X→Y groups evaluated;
- all collision classes emitted;
- typed absence audit completed;
- slot/rank pair audit completed;
- determinant provenance audit completed;
- no exception was silently ignored.

If any item is incomplete, the task is **not allowed** to issue PASS or FAIL.

## 7. Decision table — do not improvise

| Condition | Required court state |
|---|---|
| Execution incomplete, source/hash unavailable, field binding ambiguous, projector unavailable, or exhaustive census not completed | `EXECUTION_BLOCKED__NO_SUBSTANTIVE_TIR014_VERDICT` |
| Complete scan; at least one irreducible X→Y collision, ambiguous/missing projection, required carrier-only determinant, or typed-absence/slot identity loss proves source+authority cannot reconstruct required occurrence identity | `NONDERIVABLE_OCCURRENCE_TOPOLOGY__INDEPENDENT_INFORMATION_REQUIRED` |
| Complete scan; every required Y is uniquely reconstructible from X; no carrier-only determinant is required; typed absence and rank-slot distinctions are preserved; exception domain is exhaustively enumerated | `EXACT_FD_CERTIFICATE__DETERMINISTIC_RECONSTRUCTION__EXHAUSTIVE_EXCEPTION_SET` |

### Important

A successful query is not an FD certificate.

Matching aggregate counts are not an FD certificate.

Documentary evidence that the variables are rank pairs is not an FD certificate.

A unique ID already stored in a transformed carrier is not an FD certificate unless that ID is itself deterministically reconstructible from permitted source + authority and this is proved.

One collision that “looks harmless” must still be recorded and adjudicated by the fixed decision rule.

## 8. Exception law

Do not hide exceptions inside prose.

Every exception must have a row in the exception ledger with:

- source row ordinal;
- variable;
- X;
- observed Y value(s);
- exception class;
- source evidence;
- whether a deterministic governed exception rule already exists;
- whether that rule itself is source/authority derivable.

A PASS may contain a nonempty exception set only if every exception is exhaustively enumerated and governed by a deterministic source+authority rule. Otherwise PASS is forbidden.

## 9. Required outputs

Write only under:

`.../AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/REC-01/`

Required files:

1. `README.md`
2. `SOURCE_IDENTITY_AND_HASH_RECEIPT.md`
3. `FIELD_BINDING_AND_DETERMINANT_CONTRACT.csv`
4. `POPULATED_OCCURRENCE_CENSUS.csv`
5. `FD_COLLISION_AND_EXCEPTION_LEDGER.csv`
6. `TYPED_ABSENCE_PRESERVATION_LEDGER.csv`
7. `SLOT_RANK_PRESERVATION_LEDGER.csv`
8. `DETERMINANT_PROVENANCE_LEDGER.csv`
9. `C11_PROJECTION_REPLAY_RECEIPT.md`
10. `EXHAUSTIVENESS_CHECKLIST.md`
11. `REC01_ADJUDICATION_RETURN.md`

The return must contain:

- exact source expected SHA;
- exact source observed SHA;
- total source rows;
- total physical cells tested (`rows × 6`);
- populated occurrence count;
- special/absence count;
- FD collision count;
- missing projection count;
- ambiguous projection count;
- carrier-only determinant count;
- typed-absence collision count;
- slot/rank preservation failures;
- exception count;
- exact court state from section 7.

## 10. Mutation law

Permitted writes:

- REC-01 return artifacts;
- narrowly scoped temporary scripts/tests needed to execute the court, preferably under the return directory or scratch ignored by git.

Forbidden committed mutation:

- source binaries;
- canonical semantic/manual authority;
- accepted C11 runtime/compiler;
- HQ adjudication;
- physical architecture.

If an existing runtime bug prevents the court from executing, document the blocker. Do not repair production runtime inside REC-01 unless HQ separately authorizes it.

## 11. Stop condition

After outputs are internally checked, commit and push the bounded return and STOP.

Do not launch REC-02, C05R, C09, C10, or architecture work.

Terminal self-check:

> Did I prove the exact X→Y proposition over the complete named source domain, or did I merely demonstrate that something nearby works?

If the answer is not unquestionably the former, PASS is forbidden.
