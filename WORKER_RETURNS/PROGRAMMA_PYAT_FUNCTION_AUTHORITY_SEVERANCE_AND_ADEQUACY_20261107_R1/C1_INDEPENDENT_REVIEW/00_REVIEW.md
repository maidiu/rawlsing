# C1 independent review — AR-0033 Q86 source consumer

**Verdict: ACCEPT_WITH_REPORTING_CORRECTIONS.**

The C1 evidence supports `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED`. It does
not support upgrading to proved severance or equivalence. Corrections are required for
the claimed current non-test demand, the “existing FF consumer” wording, and the
bind-or-retire action, which conflicts with AR-0033’s producer-input/issuer-hold status.

## Reviewed identity

| Item | Value |
|---|---|
| Author source | `a98299e7c9cd05aa3eabe2c22d20ea6b746ea667` |
| Author return | `C1_SOURCE_CONSUMER/00_RETURN.md` and cases/probes |
| Author session | `ses_b998af9086264002a86ee57b6e` (distinct) |
| Review worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-independent-review` |
| Review branch | `review/pyat777-source-consumer-20261107-r1` |
| Review lease | `C1_INDEPENDENT_REVIEW/` only |
| Review content commit | see `03_REVIEW_COMMIT.txt` |

## Supported claims

- **AR-0033 selected CSV identity is exact.** `afrobarometer_response_option_authority.csv`
  is present at the authorized read-only path, **15,498,257 bytes**, SHA-256
  `305cb215485bc95ebecee395e578c52739311bc2fc15faed27318bd922f47332`. The R4 ledger
  AR-0033 row confirms `HISTORICAL_VERSION_SELECTED`, `ASSET_BYTES_VERIFIED`,
  `A02_RECORDED_HISTORICAL_DECISION_NOT_ORIGINAL_SIGNER`, `ISSUER-HOLD-AR-0033`,
  `CURRENT_NATIVE_ISSUER_NEEDED__CURRENT_NATIVE_NOT_RUN`, and
  `HISTORICAL_ONLY__CURRENT_PROTECTED_PATH_ABSENT`.
- **Q86 rows are as C1 reports.** Q86A and Q86B each have **6 rows**,
  `handling_rule=context_only`, `recommended_computation=none`,
  `question_type=ordinal_context`, `response_family=context_only`, substantive codes
  `0`/`1`, special codes `-1/9/997/998`; contract hashes
  `198f189adafd2f4b9e459184a897c8257fa4631f5f940686cd77736cccd38082` and
  `01ceeb78b8b4788c0732afeaab07374140b974fc1e330f79eb9f948e4c1eaa13`.
  `response_semantics_status` is `curated_packet` for substantive rows and
  `curated_special` for special rows; C1’s single status label is a partial summary.
- **Current Q86 source anchors are real.** The module pins source SHA
  `c9200ba...`, QIMPL IDs, source-structure ID, frozen risk-set identity/member hash
  and target-use/query authority. The direct Q86 tests are 8/8 PASS; C1’s 97-test
  inherited suite is a separate sourcefree suite and was not repeated here.
- **The selected Q86 contract hashes are not referenced in current `rawlsing_next`.**
  The current positive/negative tests use the sourcefree synthetic fixture, not the
  selected AR-0033 row. Actual selected-row version/shadow/withdrawal/cold-restore is
  **NOT_RUN**, correctly recorded.
- **Current source semantics authority exists but is code-created.** `GT12-A-R5-Q86-SOURCE-SEMANTICS`
  in `wave1_r5_q86_c11_projection.py:334` is a SOURCE_SEMANTICS_TOPOLOGY authority
  built from frozen source/codebook/QIMPL/domain/currentness material, with operation
  `R5_Q86A_Q86B_NATIVE_RESPONSE_SEMANTICS`. It is not the selected AR-0033 row; whether
  it is a competent current equivalent is unproved, not disproved.
- **Generic C11 T01 remains separate.** C1 reuses the inherited named falsifier and
  does not repair or requalify #765. This review does not duplicate that court.
- **Register preservation is correct.** The anti-join preserves 212 rows: 17 matched,
  195 unmatched; no whole-register completeness claim.

## Required reporting corrections

1. **Current non-test demand is not established.** The Q86 operation is a
   sourcefree canary/test path:
   - `wave1_gt12_a2_real_gt1.py` is a non-test module, but its
     `execute_and_replay_a2_gt1` and `build_gt1_q86a_i03_plan` call sites are only
     test-imported; no non-test module calls `execute_and_replay_a2_gt1`.
   - `produce_exact_conditional_support_profile` exists, but no non-test caller feeds
     it a Q86 joint fact; its call sites are tests/harness and the C1 R7 runner. The
     `gt12_c_to_d_relation_bridge` module also has no non-test caller.
   - `B5_CURRENT_OPERATIONS:O17` is a register entry for the frozen Q86 joint
     conditional operation, not proof of a production first consumer.
   Correct the wording from “actual present operation/current operation” to
   “sourcefree canary/candidate operation; no non-test first consumer proved.” Keep
   `UNPROVED` until a real selected consumer or a typed no-current-demand disposition
   is established.

2. **Do not mandate binding AR-0033 row/contract hashes as the minimum next action.**
   The R4 ledger AR-0033 row explicitly says
   `HISTORICAL_ONLY__CURRENT_PROTECTED_PATH_ABSENT`, `CURRENT_NATIVE_ISSUER_NEEDED__CURRENT_NATIVE_NOT_RUN`,
   `RESTORABLE_AS_HISTORICAL_PRODUCER_INPUT`, and “Do not reload the packet as a
   per-query runtime authority; it is the certified producer input.” The C1 action
   “bind exact selected row/contract hashes to C11 producer or retire” conflicts with
   that custody/issuer status and with the `context_only` row semantics.

3. **“No competent current equivalent” is not established.** The code-created
   `GT12-A-R5-Q86-SOURCE-SEMANTICS` authority and source-native domain are a candidate
   current representation; C1 assessed only the synthetic test fixture. The correct
   status is “current substitute unproved,” not “no equivalent exists.” Absence of the
   literal AR-0033 hashes is not by itself proof of severance.

4. **“Existing FF consumer” overstates the wiring.** `field_forge_conditional_support.py`
   provides the producer function, but there is no demonstrated non-test Q86 joint
   caller. Correct to “FF producer candidate; no non-test first consumer proved.”

5. **Context-only does not ban raw counts.** C1 correctly leaves the decision to the
   source-semantic owner, but the action should not imply that raw unary/joint counting
   requires structural response-option computation or reinstatement of the historical
   packet. `context_only`/`recommended_computation=none` may be consistent with raw
   source-native counting; that is an owner decision, not a proven missing authority.

## Unsupported or overstated claims

- “One actual present operation” as a current non-test demand — not established.
- “Existing FF consumer” as a non-test consumer — not established.
- “No competent current equivalent” — categorical claim not proved; the current
  source-semantics authority is unassessed.
- “Bind exact selected row/contract hashes” as the smallest owner action — conflicts
  with AR-0033 producer-input/issuer-hold status and is not required by the evidence.
- Any reading of the sourcefree 8/97 tests or generic T01 falsifier as selected-Q86
  authority proof — C1 itself disclaims this; the review agrees.

## Minimum next operation

1. Establish whether any real non-test consumer actually demands the Q86 raw
   unary/joint operation. If not, classify it as canary/historical-only and do not
   force a production binding.
2. If a real consumer exists, the source-semantic owner must decide whether the
   `context_only`, `recommended_computation=none` AR-0033 rows require any response
   semantics beyond the current source-native Q86 domain/currentness authority. Assess
   `GT12-A-R5-Q86-SOURCE-SEMANTICS` as a possible adequate current substitute, with its
   provenance. If adequate, no AR-0033 runtime binding is required. If not, name the
   competent current issuer/equivalent first; do not reload AR-0033 as a per-query
   runtime authority.
3. Only after that decision, choose bind/no-build/retire at the true owner. Add an
   actual selected-row positive plus wrong-version/source/wave/shadow/withdrawal and
   cold-restore tests when a legal selected fixture exists.
4. Preserve the full 212-row anti-join, other historical estates and unmatched IDs.
   This one wave does not complete #777.

## Limits

No respondent/SAV/DTA/DB read, no source upload, no asset copy, no native/science/
actor effect, no production/test/HQ/peer/protected write. No full #777 completion or
all-35 claim. Quota UNKNOWN.

## Evidence

- `logs/independent_checks.log` — CSV/hash/Q86 rows, current contract-hash absence,
  non-test call-site scan, R4 AR-0033 row.
- `logs/q86_direct_tests.log` — 8/8 direct Q86 sourcefree tests, own basetemp.
- `probes/independent_checks.py` — read-only probe.
- C1 evidence inspected read-only: `00_RETURN.md`, `01_CASES.jsonl`, `02_CASES.tsv`,
  `03_TEST_RECEIPTS.md`, `04_MINIMAL_OWNER_ACTIONS.tsv`, `05_REGISTER_ANTIJOIN.tsv`,
  `probes/q86_*`, `logs/97_suite.log`.
