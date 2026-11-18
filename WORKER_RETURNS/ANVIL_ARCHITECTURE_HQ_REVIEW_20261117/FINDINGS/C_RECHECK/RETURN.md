# R2 RECHECK — same distinct independent C

**Verdict:** `ACCEPT_SCOPED_CONDITIONAL_ARCHITECTURE_DIRECTION`.
**Scope:** corrected documentary architecture candidate only — not implementation,
product Batch code, native/100k/6 GiB, original35/source-science/actor rights,
protected adoption or H1.
**Original review:** commit `a352626dc05a03072c04954bfae6a42c0ece7dfa`
(`REVISE_EXACT_DEFECT`; D1–D5).
**Corrected target:** commit `06e88a5ac7e4c14362a97a046f44e25d8eec4162`,
annotated tag `anvil-architecture-candidate-20261117-r2` object
`3f55b252f325ec38e2a7e0c01bb3b58fbf588ee7`, peeling to `06e88…`.
**Product source:** `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`, unchanged
(`git diff cea2d4d..06e88 -- rawlsing_next` empty). **Candidate manifest:**
120/120 hashes independently verified. **Remote:** branch and tag exact.

## What I read in the corrected candidate

`RETURN.md`, `S2_S3/D1_D5_CORRECTION_MAP.md`, `S2_S3/FINAL_ARCHITECTURE.md`,
`S2_S3/FINAL_DECISION.json`, `S2_S3/FINAL_OBLIGATION_CROSSWALK.tsv`,
`S2_S3/FINAL_DECISION_GUARD.txt`, `GUARDS/v2_supplementary_guard.py`,
`GUARDS/run_v2_guard_tests.py`, `RUNS/v2_guard_baseline.txt`,
`RUNS/v2_guard_negatives.txt`, builder/wrapper handoffs, provisional banners,
and the 120-file manifest. I extracted the exact target to
`R2_RECHECK/snapshot/` and used only that copy for guard execution; I did not
execute the author's negative runner against author `RUNS/` or write peer paths.

## D1–D5 disposition

| Defect | Disposition | Independent check |
|---|---|---|
| **D1** specialist dependency stale PENDING | **RESOLVED** | `specialist_dependency.status = BOTH_RETURNS_RECEIVED_AND_ADJUDICATED`; old plan explicitly under `historical_plan_only`; `final_selection_frozen = true`; my stale-PENDING mutation REFUSES. |
| **D2** machine SC-ESTATE/sequence/effects stale | **RESOLVED** | `physical_architecture.name = "Prepared-session-first + conditional construction/recovery; durable index held"`; layers L3 selected-not-wired, L5 conditional, L7 held; sequence statuses conditional/held; all 16 effects corrected; my stale-SC-ESTATE, stale-effect and unconditional `selected_design` mutations REFUSE. |
| **D3** 16/16 guard cannot see v2 | **RESOLVED** | Independent supplement baseline `PASS_V2_SUPPLEMENTARY_STRUCTURAL_20_REQUIREMENTS_118_IDENTITIES`; accepted base guard still 16/16; my empty-v2 mutation REFUSES; restore PASS. |
| **D4** false executed-grade for wrapper/Batch | **RESOLVED AT DOCUMENTARY GRADE** | Direct prepared path is separately `EXECUTED_SOURCEFREE_DIRECT_PATH_3_OF_34`; wrapper/Batch is `PROPOSED_NOT_WIRED` with exact rejection lines 42/54/94 and Batch line 406; explicit owner protocol requires an exact `PreparedSavedC11Admission` whitelist, not generic `isinstance`, one prepared context per workload, per-unit current, exact fact/replay/negative and restore. Actual implementation remains owner-gated and is not claimed. |
| **D5** provisional artifacts ambiguously live | **RESOLVED** | Provisional docs carry `HISTORICAL / SUPERSEDED_BY_FINAL`; `PROVISIONAL_DECISION.selection_status = HISTORICAL_SUPERSEDED_BY_FINAL_DECISION`; manifest `document_roles` separates authoritative from historical. |
| **N3** Q2 source-vs-journal ambiguity | **RESOLVED** | `construction_source_transport.rule` requires Q2 from the source-derived typed stream, never a re-parsed JSONL journal; journal is transport/parity only; full physical proof and second-certificate fallback remain. Guard checks `q2_must_originate_from_source_stream=true`. |

## Independent guard evidence

- Supplement baseline against the corrected decision, addendum and crosswalk:
  `PASS_V2_SUPPLEMENTARY_STRUCTURAL_20_REQUIREMENTS_118_IDENTITIES`
  (16 base + 4 v2 = 20; 118 identities). `RUNS/v2_guard_baseline_independent.txt`.
- Accepted base guard still reports 16/16 and 118/118; the supplement adds the
  four v2 rows and D1/D2 coherence. This is a local structural check, not
  semantic/native/H1 proof.
- My independent mutations:
  - empty v2 addendum/dispositions/crosswalk -> `REFUSE_V2_SUPPLEMENTARY`;
  - `specialist_dependency.status=PENDING…` -> `REFUSE`;
  - stale SC-ESTATE name -> `REFUSE`;
  - stale SC-ESTATE per-requirement effect -> `REFUSE`;
  - `selected_design.durable_index_status=SELECTED` -> `REFUSE`;
  - `selected_design.construction_one_journal_one_certificate=SELECTED_UNCONDITIONAL`
    -> `REFUSE`;
  - exact restore -> `PASS` 20/118.
  Logs: `RUNS/negative_*.txt`, `RUNS/negative_summary.tsv`,
  `RUNS/v2_guard_restore_independent.txt`.

**Residual guard finding (nonblocking, disclosed):** if only an
`implementation_sequence` step's `status` is changed to `SELECTED` while its
action text remains “Durable locator index only if…” or “One source-derived Q2
certificate only with…”, the supplement guard still PASSES, because its
sequence check looks for the literal substrings “durable index” and “one i02” /
“one-certificate.” The authoritative `selected_design` fields and the actual
sequence statuses are correct; this is a guard-normalization gap, not a false
claim in the corrected decision. Owner should normalize `durable locator index`
and `one source-derived Q2 certificate` and add those two negative cases before
treating the supplement as a release gate.

## D4 — what is and is not accepted

The corrected handoff now honestly separates:

- **Direct prepared path:** `PreparedSavedC11Admission.open + prepared_i03`;
  sourcefree tests 3/7/24 (34 total) were already executed in R1; the direct
  prepared test shows one `_build` and four-operation fact parity. This is
  sourcefree direct-path evidence only.
- **Wrapper/Batch path:** `execute_saved_i03/i05/batch` and
  `BatchExecutionRunner(saved_mode=True)` still reject
  `PreparedSavedC11Admission` at exact-type guards and
  `SavedC11Admission.execute_i03/i05` still open fresh sessions. The corrected
  document labels this `PROPOSED_NOT_WIRED` and gives the exact owner-routed
  protocol. That is an honest architecture handoff, not an implementation.
- **No generic `isinstance`:** the handoff explicitly requires an exact
  `PreparedSavedC11Admission` whitelist/protocol, preserving admission integrity.
  I did not require a product patch; the actual wrapper/Batch one-`_build`,
  four-operation fact-parity, current/revocation/restore witness remains a
  separately owned implementer step.

## N3 and construction proof

`FINAL_DECISION.construction_source_transport` now states: Q2 root identity is
computed from the source-derived typed stream; the journal is exact body
transport and parity-checked, not used to originate Q2. The construction gate
keeps the full physical body/lane/selector proof against Q2 and the mandatory
second-certificate fallback if any family/selector cannot be proved. No
one-certificate implementation or proof is claimed.

## Strongest failed attack

The strongest prior attack — “the prepared session silently changes
denominator/occurrence/routing/weight/negative/replay semantics” — still fails.
The corrected design changes only index reuse `S`; it keeps the same
`execute_empirical_query`/`execute_exact_bounded_discovery`, exact facts,
risk/denominator refs, typed negatives, current checks and replay. The product
source is unchanged from `cea2d4d`, so I did not rerun the 34 focused tests; R1’s
sourcefree 34-pass run and the direct prepared 3-test log remain separate
evidence. No native/100k inference is made.

## Scoped acceptance

I accept only the **source-grounded conditional architecture direction and
corrected documentary contract**:

1. Prepared-session-first, conditional construction/recovery, durable index
   held.
2. Base 16/16 + v2 supplement 20/20 + 118 identities, with D1/D2 coherence.
3. Exact owner-gated wrapper/Batch integration as `PROPOSED_NOT_WIRED`; not
   implemented, not authorized by this review.
4. Q2 source-derived rule, full physical proof and second-certificate fallback
   preserved.
5. D5 historical separation and no live provisional status.

This is **not** acceptance of code, production, native/100k/6 GiB,
original35/source/science/actor rights, protected adoption or H1.

## Finite remaining obligations

1. **S2-D/Batch owners:** implement the exact prepared-session-aware
   wrapper/Batch adapter; one prepared context, exact `_build`/four-operation
   parity, current/revocation/restore; owner ACK. No generic `isinstance`.
2. **S2-C/D writer owner:** one-journal/one-certificate only after full
   source-derived Q2 physical proof for every family/selector; else keep the
   second certificate. Recovery claim/lease and crash-injection proof remain.
3. **#1006 measured-cost owner + S04/I03:** H/S/Q/O measurement on one
   authorized real-width workload; 1/10/100 same-process and 10 fresh-process.
4. **Durable index:** only if `S` material and compact exact encoding passes
   binding/invalidation/retained-size gates.
5. **Guard owner:** tighten the two sequence-status literal checks above.
6. **H1/protected owner:** only after this scoped C acceptance and competent
   receiving; no merge by this review.

## Smallest actual first-consumer handoff

Implement one owner-approved prepared-session-aware adapter around
`execute_saved_batch` (or an exact prepared-mode `BatchExecutionRunner`), with
one `PreparedI03Session` context per exact release/universe/workload, exact
`PreparedSavedC11Admission` type whitelist, per-unit `check_current`, four
operations (selected, F2 forward, F4 3+, raw), exact fact-ref parity, revocation
and changed-root refusal, and exact restore. This is the next coherent
engineering step; it is not authorized or claimed here.

## Own limits

- Source-lineage coverage remains sampled from R1; no exhaustive recensus of
  all 141 rows or all source originals is claimed.
- I did not rerun the 34 focused tests because product source is unchanged from
  `cea2d4d`; I did not run native/100k/6 GiB or crash injection.
- I did not authenticate the preparation-only instrument or external reviewer
  content; I did not modify the candidate or author RUNS.
- The supplement guard is structural only; the sequence-status residual is
  disclosed above.
- Return SHA is the final R2 commit on the same review branch; original R1
  commit `a352626…` is preserved untouched.
