# PYAT #997 R6 — same original independent G5

**Decision:** `ACCEPT_SCOPED` · **G5:** `PASS_SCOPED` · **Integration:** `UNMERGED`
**Scope:** `R6_SOURCEFREE_ISSUER_BINDING_AND_SAVED_NATIVE_FIRST_CONSUMER_FATE_JOIN`
**Reviewer:** `ses_e30a442d8ffeYBbXi7rPUpPxoc` (same original reviewer; not Browser A/B or native executor)
**Model:** `opencode-go/deepseek-v4.1-flash#max`

## Exact frozen cut

| Item | Value |
|---|---|
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat997-r6-g5-20261115` |
| Branch / HEAD | `review/pyat997-r6-g5-20261115` / `cb5f4c6653f5a40ad6e875fca7f999b11afc0e3c` |
| Code/test cut | `9ac034dd0734cdd000b4b73583f883dbcec2dfa6` |
| Documentary cut | `c368ff30189d8fdd5c1a8036a5b6e265d822f80b` |
| Prior rejection | `8b03c121a2f6d9c7a9c2e0513a03545780d14c3c` |
| Product/test diff code cut..HEAD | empty |
| Runtime | Python 3.11.3, pyarrow 22.0.0, duckdb 1.5.2, pyreadstat 1.3.2, pytest 9.0.2 |

I wrote only `WORKER_RETURNS/PYAT997_R6_INDEPENDENT_G5_20261115/`. Product, tests and source were read-only. The old `pyat997-native-independent-review` worktree was not used.

## 1. Original R3 manual QUERY attack through the actual R6 join

I copied the exact R3 harness from `8b03c121…` into my evidence and replayed the original coherent attack: q101/q102/q103 manual QUERY, matching `TestOnlyDecisionResolver`, manual two-unit native Batch, then the actual R6 postconsumer join.

Observed:

- compiler-issued workload: **0 QUERY / 1 DISCOVERY**;
- manual R3 workload: **1 QUERY / 1 DISCOVERY**, `same_compiler_record=false`;
- joint query absent from `plan.records`;
- **12** F4-like frontier operations, all **`PROHIBITED`** (`JOINT`/`CO_TRAVEL`, `SAMPLE`);
- manual native Batch executed both units (`COMPLETED`, `COMPLETED`);
- actual R6 join with **empty runner** → `R03_COMPILER_ISSUED_JOB_OR_PLAN_DRIFT`, positive attribution **0**;
- actual R6 join with **executed runner** → `R03_COMPILER_ISSUED_JOB_OR_PLAN_DRIFT`, positive attribution **0**.

The historical 8b03 witness exit `1` only diagnoses the old substitution; the R6 refusal evidence is the executed join above. See `evidence/original-r3-r6-refusal.json`.

## 2. Wrong source/science permission

Independent forged `source_permission_ref` and `scientific_permission_refs`, each with a matching resolver record, both refuse:

`R03_COMPILER_ORIGINAL_ISSUER_IDENTITY_DRIFT`, zero runner receipts, zero positive attribution. See `evidence/permission-refusals.json`.

The R6 targeted four-case court also passes: self-issued query, different discovery decision, reissued U root, and unaltered compiler discovery with zero executed units / zero positive links (`4 passed, 20 deselected in 3.22s`).

## 3. Genuine compiler-issued discovery first consumer

The actual compiler-issued **one DISCOVERY** workload was executed through native I05/Batch and the R6 join:

- source SHA `ceb5e900…`; one read/decode/cell pass;
- q101 direct I03: `SUPPORTED`, raw **5/5**; three country/negative `UNAVAILABLE`;
- I05: **8** receipts; Batch: **1 COMPLETED**;
- join: 22 rows, **6 positive-native-linked**, **2 eligible pending**, 8 ELIGIBLE / 14 HELD;
- consumer source opens **0**; full C11 builds **0**;
- I02 replay `d38b8a3d…`; I03 fact `82860707…`.

This is actual authorized discovery execution, not the invalid manual QUERY. See `evidence/genuine-discovery.json`.

## 4. Independent seven-file court and fate receipts

Exact seven-file handoff suite:

```text
89 passed in 24.95s
```

A second measured run: `89 passed in 24.55s`, wall 25.35s, maximum RSS **160,866,304 B**, peak footprint **127,463,424 B**. It covers source→13-family saved body→cold I03/I05, q101 denominator-5 positive and country negative, SAV/DTA changed-fact and exact restore, missing/mixed/held/mutated/root/CURRENT negatives, and exact fate/receipt joins.

S1-C source-operation fate receipts: **18 passed in 83.69s**.

Historical all35 no-drop ledger: **3 passed in 35.39s**, 35 sources / 18,276 items / 18,413 slots / 26 unjoined; no original source execution.

Test adoption is now canonical: the two exact reviewed test blobs are `c3077ce8…` and `3ca7396a…`; the native first-consumer file `b6031035…` includes the reviewed corrections plus four new R6 issuer tests. The product tree is unchanged by the test patch; 89/89 passes.

## 5. Verdict

`ACCEPT_SCOPED` at the R6 sourcefree issuer-binding scope. The original 8b03 material defect is fixed: the actual R6 join refuses the coherent manual QUERY with 0 positive attribution, preserves the genuine 0 QUERY/1 DISCOVERY compiler shape and 12 PROHIBITED F4-like operations, and actually executes genuine compiler discovery through native I05/Batch. No R6-specific runnable counterexample was found.

This is **not** terminal/full original S1-E acceptance:

- the R6 guard is a source-grounded historical producer-consistency check, not a credential-independent external attestation of a fully fabricated plan/frontier/CURRENT compiler cut;
- **#999 S2-A native body-truth / coherent projected+locator corruption remains a separate unresolved owner hold; no false integrity acceptance**;
- R03 genuine governed QUERY/F4 issuance remains separate **J3** and is not claimed;
- original35 source/science/rights, production CURRENT, protected merge, #998 full joined, #1001 full scale, #1006 baseline, N11/N12 and 100k/6 GiB remain HOLD/NOT_RUN.

Integration `UNMERGED`; no product/tests edits, no source/science authority, no protected merge, no subagent, no new engine, no 100k.

Evidence: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat997-r6-g5-20261115/WORKER_RETURNS/PYAT997_R6_INDEPENDENT_G5_20261115/`.
