# OPS-04 — Consolidated C4 reconciliation decision claims

Status: `PENDING_EXTERNAL_ASTRA_ADJUDICATION__NOT_AN_ADOPTION_DECISION__DOES_NOT_LIFT_HQ182_HOLD`.

Adjudicator: HQ/Vozhd, OpenCode Space Bunny Free.
Expected control parent: `55ba382dccb88494d219a945c17efc166e456bd2`.
Artifact under review: `8ff40d37de69db2d8a6053a7c2242f481677f1a4`.

This reconciliation preserves both lanes' historical packets. It records
corrections through this successor document. It does not rewrite HQ182's
bytes and does not adopt a replacement residual register by itself.

The comparison phase is closed. Both lanes were inspected. This preparation
is **not** blind and does not claim to be.

## Inputs actually read

| Input | Commit | Read |
|---|---|---|
| Freeze fan-in | `8ff40d37de69db2d8a6053a7c2242f481677f1a4` | 12 artifacts |
| Sol reviewer | `fe6103cd50c634b92233f49815cc6d4abe49964d` | 8 artifacts |
| Space Bunny reviewer | `3a5b2cbc7f1978384268376f3ee493c7c095780b` | 8 artifacts |
| Sol shadow HQ | `d0fc810de3bee0e1ea68c82fa44c61c749372077` | 8 artifacts |
| Space Bunny HQ182 | `fe1b2729b0f9f1ff18044c2f655b74784e001217` | sealed checkpoint |
| C4C3 environment record | `1df64cc596b5602c952518c87b1c71cc1fcfb35f` | `01_ENVIRONMENT_LOCK.json` |
| C4B | `c2af4f61d68e9803af83f8e26f633acfe31062fa` | WVS custody + warrant template |
| C4A combined court | `8f7efe690a161902e79358eb31650c238a4c0be8` | `03_COMBINED_SOURCE_FREE_COURT.json` |
| M01 compositor return | at freeze | `WORKER_RETURNS/PYAT-HQ117-M01-ROUTE-B-EXECUTION-COMPOSITOR-R2/**` |

---

## Load-bearing claims

| Claim | Exact evidence | Observed / inherited / inferred | Accepting it permits or blocks | Independent check |
|---|---|---|---|---|
| Freeze graph lawful; count discrepancy is pure first-parent (3) vs total-reachable (5) | `01256977..8ff40d37d`; `rev-list --first-parent --count`=3, `--count`=5; extras `1df64cc59`, `eba2f4249` | **Observed** | Permits freeze acceptance at source-free grain | Re-derived by me; both lanes agree |
| `rawlsing_next` tree `b0c1ab47` unchanged across whole lineage | 7 commits queried | **Observed** | Permits freeze acceptance | Re-derived by me at all 7 points |
| Warrant candidate digest exact | recomputed SHA-256 of `04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json` | **Observed** | Confirms candidate unaltered; still unsigned | Re-derived by me, byte-exact |
| **C4C3's 21-module closure is a downstream trace beginning below M01; producer-inclusive closure is 23** | Sol shadow `04_SHADOW_HQ_ADJUDICATION.md` | **Inherited from Sol shadow**, independently corroborated | Corrects permanent wording; does **not** invalidate freeze | I verified both delta modules contain **zero** P2X/DuckDB/subprocess/ctypes/dynamic-import references |
| **Sol shadow ground (1) — producer is "byte-identical to the already-qualified M01 candidate" — is FALSE** | producer blob at freeze `2385cd32`; at M01 court `6560d7a9`; changed by `903c262e4` "Fix M01 authority preimage canonical verification", +7/-2 in `verify_route_b_replay_receipt` | **Observed — correction to Sol shadow** | Invalidates that *justification*, not the conclusion | I diffed the blob history directly |
| **Correct adoption basis: the current producer bytes were qualified by C4A's combined court, not by M01's 61/61** | C4A `03_COMBINED_SOURCE_FREE_COURT.json`: `test_pre553_route_b_production.py` count 11, group compat; consolidated 533 collected / 530 passed / 3 failed; all 3 failures are `test_fiabc_*`, triaged INHERITED at both parents | **Observed — neither lane stated this** | Supplies a *stronger* and correct basis for the same conclusion | I enumerated the 3 failures; producer is not among them |
| M01 bounded court was 61/61 | `04_OWNER_REGRESSION_LEDGER.tsv`: 11+4+14+32 = 61, `BOUNDED_COURT_TOTAL`, PASS, GH Actions run 36302391261 | **Observed** | Establishes M01 origin qualification, pre-fix bytes only | Re-derived by me; arithmetic exact |
| Producer contract is unique | 1 of 330 `rawlsing_next` files declares `PYAT_M01_ROUTE_B_PRODUCTION_COMPOSITOR`; 1 defines `execute_route_b_production` | **Observed** | Establishes uniqueness **only** | Re-derived by me. **Uniqueness is not adoption** |
| **R7 wording: "NOT reproducible from this path alone" + explicit reproduce command — HQ182's "from the repository" is INACCURATE** | C4C3 `01_ENVIRONMENT_LOCK.json` → `environment_location.durable_note`; `reproduce_command` pins all 13 packages | **Observed — correction to HQ182** | Narrows R7 materially | I read the full sentence and the reproduce command |
| R7 residual class is **fingerprint completeness**, not environment irreproducibility | `base_interpreter_sha256_prefix32` is a 32-hex prefix; `reproducibility_caveat` says the 13-package subset is "index-independent because every one of those is exactly pinned" | **Observed — reclassification** | Moves R7 from "non-reproducible surface" to "incomplete fingerprint, known and bounded" | Re-derived by me |
| **38 SHA-256 prefixes, not "40 truncated identities"** | 32 values of 16 hex (all field-named `*_prefix16`) + 6 of 32 hex (1 `base_interpreter_sha256_prefix32`, 5 `compiled_extensions.*.cpython-311-darwin.so` with **no** prefix marker) = 38; the 2 values of 40 hex are `no_repo_mutation.rawlsing_next_tree_before/_after`, both `b0c1ab47`, which are **complete Git SHA-1 tree identities**, not truncated SHA-256 | **Observed — correction to HQ182 and to the Space Bunny reviewer** | Corrects the census; 38+2=40 short hex values exactly | Full enumerable census by length; docket arithmetic confirmed exact |
| 3 complete 64-hex SHA-256 values exist | all equal `9cde8e5ab9abba…` = historical C3 freeze hash | **Observed** | Confirms the historical freeze identity is fully pinned | Re-derived by me |
| **R9 gap is narrower than either lane stated** | C4B template: `source_access_accounting` with 7 counter slots × 7 sources. Candidate `per_source`: no counters, but retains `max_retry_budget`, `expected_operation_class`, `reader_lane`, detailed `allowed_operations` (variables, ordinals, native codes, expected types, missing states). Artifact 07 `per_source_expected_operation_class` retains **8** sources with `expected_full_reads`, `expected_selected_reads`, `max_retry_budget`, `retry_law` | **Observed — correction narrowing** | Repair = add explicit per-source read-limit counters to the *issued warrant*, bound to artifact 07's already-frozen expectations. **Not** a loss of per-source constraints | Re-derived by me from all three artifacts |
| **R10 full digest recoverable from governing evidence, not guessed** | C4B `04_WVS_ORACLE_CUSTODY.json`: `T3_freeze_sha256` = `7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908` (64 hex) | **Observed** | Documentary repair, fully determined | Re-derived by me; matches fan-in prefix `7dfb6` |
| Zero-retry conflicts with nothing | C4B sets no numeric budget; retry clause conditional; O1-C08 routes retries to new law | **Inherited**, uncontested | No repair needed | Both lanes agree |
| D2P custody limits, 2 unverified labels, 7 unfilled locators, all-35 ceilings, C7/actor holds preserved | C4B/D2P/Omega-1 | **Inherited**, uncontested | All preserved | Both lanes agree |

---

## Corrected residual register by stage

### Blocking freeze acceptance: **0**

No finding invalidates any O1-C01..C1-C05 closure. Both lanes approve at
the declared source-free grain. The 21→23 correction changes *wording*, not
validity, and the correct basis for accepting it is C4A's combined court,
which I verified directly.

### Blocking warrant issuance: **1**

**R9, narrowly restated.** The issuance repair is to carry explicit
per-source read-limit counters into the issued warrant for the 7 fresh-read
sources, bound to the expectations already frozen in artifact 07. Per-source
constraints are **not** lost — they survive in artifact 07 and partially in
the candidate. What is missing is their explicit expression as warrant
limits. This is a documentary completion of the instrument, not a
re-derivation of the workload.

### Blocking live execution: **1, reclassified**

**R7, restated and materially downgraded in kind but not removed.** The
environment record is explicit that the venv is non-durable *at its path*
and that "the reproducible content is the freeze below, not the path," and it
supplies a pinned 13-package `reproduce_command` that is index-independent.
What is genuinely incomplete is the **fingerprint**: the base interpreter is
recorded only as `base_interpreter_sha256_prefix32`, and the five
`compiled_extensions` digests carry no prefix marker in their field names.

Required before a governed run: either preserve the qualified environment
durably with a complete interpreter digest, or re-create and re-qualify from
the pinned reproduce command and record complete digests. This is a
bounded, achievable precondition — not the "self-declared irreproducibility"
HQ182 asserted.

### Advisory: 9

Bookkeeping denominator normalisation, D2P's 24-over-18 authorities
disclosure, the entry-point record, and the remaining minor items. All are
conservative-direction and none blocks any stage.

### Counterexamples: **0**

No counterexample to any closure, no weakened law, no provenance drift, no
cross-owner conflict.

---

## Corrected permanent wording, if later authorized

> The exact frozen source-free implementation is accepted at the declared
> grain, supported by existing M01 source-free qualification and by C4A's
> combined source-free court (533 collected / 530 passed / 3 inherited
> failures, none in the M01 producer suite), together with Darwin-qualified
> downstream C4 runtime evidence. C4C3's 21-module trace is a downstream
> trace beginning below M01; the producer-inclusive static closure is 23
> modules. No claim is made that the complete producer-inclusive M01 path
> was freshly rerun on Darwin.

This wording is offered because the byte-identity justification offered by
one lane is inaccurate, and the accurate basis is stronger.

## What this reconciliation does not do

It does not adopt the C4 freeze into the build. It does not lift HQ182's
hold. It does not issue a warrant, discover a locator, or access any raw
source. It does not rerun the review. It does not select conclusions by
model reputation, timing, or majority agreement — where the lanes agreed I
still re-derived; where they differed I resolved against governing evidence,
and in two cases the governing evidence sided against *both* lanes,
including my own prior adjudication.

Terminal: `OPS04_CONSOLIDATED_C4_DECISION_CLAIMS_PREPARED__PENDING_ASTRA__NO_ADOPTION__NO_SOURCE_ACCESS`