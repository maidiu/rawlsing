# PYAT F7/P07 — temporal method and as-of consumer recovery

**Schema:** `PYAT_F7_P07_RECOVERY_RETURN@1`
**Lane:** `PYAT-F7-P07-RECOVERY`
**Repository:** `maidiu/rawlsing` (private)
**Branch:** `agent/pyat-recover-f7-temporal-p07-hostile-successor-20261030-r1`
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-recover-f7-temporal-p07-hostile-successor-20261030-r1`
**Branch startup SHA:** `750548ddbb9b4392a16ce93097b856f349e16182`
**Current PRE-MAIN pinned at runtime:** `8e44ca9c751049d65e6def47600b5c073ee04b29` (`integration/pre-main-reconciliation-r1`, #563)
**Base used for this worktree:** `8e44ca9c...`; startup `750548dd...` is an ancestor, so the eventual push is a fast-forward, not a force push.

## Role, session and model

- Independent I3+ historical-material/temporal-method and secure sourcefree ABI reconciler.
- Not the original F7/P07 issuer, S7FIX identity author/reviewer, PRE-MAIN integrator, or own reviewer.
- Fresh OpenCode session `ses_e6d29e95cffe854ht2rHaESxcE`, title `F7 temporal/as-of recovery, no sealed owner`, agent `build`.
- Session DB model row: `{"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`. The interactive process is PID 42480; its argv is not exposed, so MAX is verified from the session row rather than a run-mode `--variant max` argv.
- This is a distinct session from C3/R9 `ses_e6d2c881effeylhClQfNwjPOVq`, S7FIX `ses_e6f7c46f8ffeJ808JJfoBH3866`, and PE SC0 `ses_e6f557010ffeVc8ejV937G5Ii9`. No autonomous model, editor, host or account switch was made.
- Existing C3/R9 worker/worktree was observed and not disturbed. No new workers were dispatched.
- Execution: isolated local full Git, sourcefree Python/pytest only. No native P07 compile/import/execute. No raw survey/respondent source opened.

## FINDING

1. **The historical F7 method is real but current F7 is absent.** The pure method blob
   `6f6b462b1cdef54d7989f15452473383c1661594` (79,679 bytes, 28 function defs,
   6 classes) exists at `c86ae335e...`; the current path
   `rawlsing_next/pre553_temporal_comparability.py` is ABSENT.
2. **The historical method is a bounded two-anchor temporal relation producer,
   not an EE12 scientific-comparability calculator.** It derives exact delta,
   state precedence and noncomparability from caller-supplied hash-bound
   requirement material. It does not authorize construct, item, route,
   population, weight or time comparability; it does not implement timestamp
   geometry or as-of/version selection.
3. **The historical contract proposed one new authority kind,
   `TEMPORAL_COMPARABILITY`, that was never adopted.** Current
   `AUTHORITY_KINDS` has 18 members; `TEMPORAL_EVIDENCE` is present and
   `TEMPORAL_COMPARABILITY` is absent.
4. **The current source-relations owner is TEST_ONLY.** Current blob
   `5b67e3f98a5faf95a6c82700af2346fef6e306a5` has the outer
   `SourceRelationResolver`, but no nested `_make_sealed_source_relation_owner`,
   no `authenticated_source_relation_decision`, and no
   `validate_relation_decision_replay_identity`. Its only importer is
   `rawlsing_next/tests/test_pre553_source_relations.py` (24/24 passed);
   production importers are empty.
5. **The historical nested/authenticated owner has no current owner.** The
   historical blob at the final cut has the nested owner and authenticated
   entrypoint, but the pure-Python custody path was defeated at ledger-cell and
   coordinated-anchor boundaries (HQ234/HQ236/HQ238), and the native Stage A/B
   path had OOB/SIGSEGV, leaks, decide leak, positive parity and trusted-callback
   failures (HQ245-HQ248). It is not ported or revived. External S7-FIX
   evidence (`80bc5d9b...`) confirms five historical outer/nested splits and one
   emit join, 1,885 corrected families, 3,135 exact-once IDs and 2,595 preserved
   negatives; independent I3 (`1b89fd49...`) records `CURRENT_OWNER_MAP RED`,
   zero of five current outer AST matches, and historical emit different from
   current PR526. This lane cites that evidence but does not edit or duplicate
   the issue #565 map-correction lane.
6. **There is no current N9 historical/as-of first consumer for F7.** The current
   N9/N10W candidate is TEST_ONLY synthetic progressive conditioning, not a
   temporal/as-of receiver. The current B5 lifecycle is event/checkpoint
   currentness, not scientific comparability. The closest comparability seam
   (`ConditionerBinding.comparability_authority_ref`) is an opaque, type/equality
   checked pairing ref with no temporal meaning and no production consumer.
7. **The EVS A048 lanes are documentary only.** HQ250 S03 / HQ254 E01 / HQ257 E02
   identify a construct crosswalk at best; they have no exact two
   source-authorized measured products, no pair authority, no source-version
   bridge, no N9 consumer, and unresolved Austria-1990 design/protocol/population
   gaps. They are not an original E comparability issuance.
8. **The R3-S04 alternative is not safe.** Its interpolation, nearest-anchor
   backoff, fixed `0.05` drift and binary floats contradict the accepted F7
   no-interpolation/no-nearest/no-deadband law. It is absent from current baseline
   and must not be revived.
9. **Exact historical sourcefree suites pass at their own cuts.**
   - HQ211 original: 49/49 passed (`caf6644a6`).
   - HQ235 final paired method/test: 163/163 passed (`c86ae335e`, test blob
     `8a82bd5905d266c1d500b1bf2bdcb01ea948efd6`).
   - HQ227 intermediate: 134/141 with 7 cross-universe positive failures; the
     later HQ235 source-relations/test pair supersedes it. The method blob alone
     is not self-sufficient at HQ227.
10. **The recovered candidate is TEST-ONLY and passes.** 24/24 candidate tests
    and 2/2 fail-capability mutation checks (RED on mutation, GREEN on restore).
    Current source-relations 24/24; decoder/custody 73 passed, 1 skipped.

## INTERPRETATION

F7's scientific content is not "two waves, therefore movement." It is a bounded
authorization of one exact two-anchor temporal relation under an exact governed
use, with noncomparability preserved. Numerical similarity, shared wave labels,
as-of timestamps, nearest anchors and cross-wave plug compatibility are not
comparability.

The historical method preserves important scientific limits: overlap does not
become a midpoint, exact zero is not a deadband, direction requires a
direction-permitting authorized basis and exact delta, noncomparable is a limit
not empirical zero, and no trajectory/cause/currentness is inferred. Those limits
are preserved in the candidate.

What is missing is not more mathematical machinery. It is the original EE12/F7
comparability owner and a real receiver. The historical owner path is also
scientifically separate from, and weaker than, secure machine attestation. The
candidate therefore exposes `REAL_RECEIVER_MISSING` rather than inventing a
production import.

## ACTION

- Accept the scoped sourcefree method candidate as **TEST-ONLY evidence only**.
- Keep the historical native and nested-owner negatives exact; do not port the
  nested sealed owner and do not repair or revive native P07 in this lane.
- Keep current source relations marked TEST_ONLY; do not claim a production
  first consumer.
- Keep `TEMPORAL_COMPARABILITY`, original EE12/F7 scientific comparability and
  any measured EVS pair on HOLD.
- If a future selected production consumer genuinely requires protected P07
  cross-universe adjudication, issue a separate qualified native owner/issuer
  commission and independent hostile review. Do not make that a condition for
  the sourcefree method candidate.

## OWNER

| Edge | Correct owner |
|---|---|
| Original EE12/F7 scientific comparability issuance | Original EE12/F7 comparability issuer (not this worker) |
| `TEMPORAL_COMPARABILITY` kind/ceiling adoption | Separate authority-registry adoption after original issuance |
| Current nested/authenticated source-relation owner | Separate owner decision; only if a future production cross-universe consumer requires it |
| N9/N10W historical/as-of receiver | N9/N10W selected-world service owner; none exists now |
| Measured EVS or other wave pair | Source custodian + source-use warrant + product producers + EE12 pair authority + independent methods review |
| Native P07 owner/security | Separate qualified native issuer/implementer + independent hostile review; only if actually required |

## DONE

- Pinned current PRE-MAIN and created a separate worktree at `8e44ca9c...`.
- Read exact historical F7 method/test blobs and historical source-relations blob.
- Ran exact historical 49-test and 163-test suites in isolated sourcefree
  worktrees; ran the intermediate HQ227 suite and retained its 7 failures.
- Probed current authority kinds, current source relations, nested/authenticated
  owner absence, tempo path absence and production importers.
- Built a sourcefree TEST-ONLY candidate for the missing pure geometry, as-of and
  noncomparability surfaces using present current providers.
- Built 24 candidate positive/refusal tests and a 2-mutation fail-capability
  check; both pass.
- Produced `ORIGINAL_METHODS_AND_ANTI_REBUILD.md`,
  `RED_VARIANTS_AND_TRUST_BOUNDARY.md`,
  `COMPATIBILITY_AND_CONSUMER_MAP.json` and test receipts.
- Commit/push/cold-readback exact 40-hex SHA performed after this file is
  committed; the final SHA is reported in the completion message.

## REMAINING

- Independent I3+ review by a distinct reviewer.
- Original EE12/F7 comparability issuance (or an explicit decision that the
  bounded method is insufficient and must be redesigned by that owner).
- A lawful current N9/N10W historical/as-of first consumer and exact purpose
  admission.
- Exact source-authorized measured wave products and pair authority for any
  empirical comparison.
- A current secure source-relation owner decision only if a future production
  cross-universe consumer actually requires it.

## BLOCKERS

- `REAL_RECEIVER_MISSING`: no current production F7/N9 historical/as-of receiver.
- `ORIGINAL_E_COMPARABILITY_UNISSUED`: no original scientific comparability
  authority instance for constructs/items/routes/populations/weights/time.
- `TEMPORAL_COMPARABILITY_KIND_UNISSUED`: current 18-kind set lacks it.
- `CURRENT_NESTED_AUTHENTICATED_OWNER_MISSING`: current source relations is
  outer/test-only.
- `SOURCE_RELATIONS_PRODUCTION_CONSUMER_MISSING`: tests only.
- `N9_HISTORICAL_ASOF_FIRST_CONSUMER_MISSING`: no current N9/N10W receiver.
- No raw source, source run, model grant, N11/N12, N9 world or Sorok actor
  authority is available to this lane.

## LARGEST_MOVE

Do not rebuild F7 as an owner. Preserve the historical method identity and its
adverse native/nested-owner evidence, accept only the pure method candidate at
test grain, and route the next decision to the original EE12/F7 issuer and a real
N9/N10W receiver. The largest remaining move is an authority/consumer grant, not
more candidate code.

## FLIGHT

`F7_PURE_METHOD_RECOVERED_TEST_ONLY + HISTORICAL_49_49_AND_163_163_GREEN + CURRENT_SOURCE_RELATIONS_TEST_ONLY + NESTED_OWNER_ABSENT + REAL_RECEIVER_MISSING + SCIENCE_AUTHORITY_HOLD + NO_NATIVE_REVIVAL`

## DELTA

`+` exact historical blobs, sizes and counts; `+` 49/49 and 163/163 historical
sourcefree receipts; `+` current 18-kind/absent-F7/nested-owner-absent probe;
`+` 24 candidate tests and 2/2 mutation fail-capability; `+` honest current
consumer map and RED variants; `−` no current production receiver; `−` no
original EE12/F7 authority; `−` no current nested/authenticated owner; `−` no
measured pair; `−` no native revival.

## Independent review handoff

A distinct I3+ reviewer (not this worker, not the F7/P07 issuer, not S7FIX
author/reviewer, not PRE-MAIN integrator) should independently:

1. Recompute the historical blob hashes/sizes/counts in
   `test_receipts/historical_probe.json` and rerun the exact 49/163 suites in
   isolated historical worktrees.
2. Recompute the current surface probe and confirm the F7 path is absent, the
   current authority set is 18, `TEMPORAL_COMPARABILITY` is absent, the nested
   owner/authenticated entrypoint are absent, and source relations has no
   production importer.
3. Rerun the 24 candidate tests and `mutation_check.py`; confirm the named
   RED/GREEN assertions.
4. Attack the candidate's attestation binding, authority scope, as-of
   eligibility and cross-universe resolver path; confirm no path mints
   comparability from equal numbers, labels, wave index, as-of timestamp or
   latest/default selection.
5. Confirm no current production receiver, no original EE12/F7 issuance, no raw
   source use, no native code, no PRE-MAIN mutation and no nested-owner port.
6. Keep scientific issuance and secure owner adoption on HOLD unless separately
   issued. No merge or self-adoption.

Suggested independent review branch:
`review/pyat-f7-p07-temporal-method-independent-i3-20261031-r1`.

**TERMINAL:**
`F7_PURE_METHOD_RECOVERED_TEST_ONLY__HISTORICAL_49_49_AND_163_163_GREEN__CURRENT_SOURCE_RELATIONS_TEST_ONLY__NESTED_OWNER_ABSENT__REAL_RECEIVER_MISSING__SCIENCE_AUTHORITY_HOLD__NO_NATIVE_REVIVAL`.
