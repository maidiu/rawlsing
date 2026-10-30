# M04R — sourcefree patch and test receipts

Observed FINDING: the M04 patched helper closes the three journaled provenance classes but still accepts an unjournaled terminal ADP017 restore after a journaled revocation. Causal INTERPRETATION: journal-to-state checks were one-directional; the consumed restorative terminal and its pre-state were not joined to the journal. Proposed HQ ACTION: original M03/M04 owners review the bounded terminal check and the four new adversarial tests; no merge or adoption. Accountable OWNER: original M03/M04 author and CAN3/ADP017 owner, with a distinct reviewer.

## Source identity

| Surface | Git blob / SHA-256 |
|---|---|
| Original M03 helper | `2434bda6f4b00e6ea5881291f5422227e8045e74` |
| M04 patched helper (baseline) | `5ba929f51870b111ca54ca87fdf97338e4295625` |
| M04R candidate helper | `d9efd3f5ba0d06430ef99f114072ba91ef32f1fc`; SHA-256 `ef551f5ad0c927dffb37554d8aaf8c00a611877242b550fbc541ea5089151f4c` |
| M04R adversarial test | `fa728cc89375e581c4c5ee326c940fa8562a58a1`; SHA-256 `0f1bb3978657f402f54623f548776612f6ca73768e5764317f0b0805317424bc` |
| Original cell.py | `3eb2d02aee8dc840e7cac1f99230d7c69adc2f58` |
| Frozen M04 reviewer test | `8add06c66b347e324443c1263771755f6898c7e2` |

The candidate changes only `claim_provenance.py`. It does not modify `cell.py`, the frozen tests, any native source or any canonical branch.

## Patch

1. `validate_journaled_transition_ancestry(c, consumed_transitions=None)` now also rejects duplicate journal coverage (`CLAIM_TRANSITION_JOURNAL_DUPLICATE`) and can require a supplied consumed-transition set to be present in the journal.
2. `validate_consumption` checks the consumed terminal when the snapshot is `CLAIM_ACCESSIBLE` with an active stance:
   - an unjournaled terminal `SUPERSEDE_EXACT_RECORD` is refused `CLAIM_TRANSITION_UNJOURNALED`;
   - an unjournaled terminal whose pre-state differs from the last journaled `payload.after` is refused `CLAIM_TRANSITION_PRESTATE_ANCESTRY`.
3. The exact journal-to-transition pre/post-state checks from the M04 patch remain. Orphan journal entries still fail `CLAIM_TRANSITION_ANCESTRY_MISSING`.

A stricter “every selected-claim transition must be journaled” variant was tested and rejected because it broke lawful original native ADD/WITHDRAW tests in the inherited 587/74 suites. The final rule closes the specific restorative terminal and forged-pre-state routes while preserving those assertions.

## Reproduced results

Cold reconstruction commands (reviewer return `SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1`):

```sh
python3 repro/stage_independent.py
python3 repro/install_candidate.py
python3 review/run_fresh.py
python3 repro/run.py after original_413
python3 repro/run.py after independent_100
python3 repro/run_author.py
python3 repro/run_historical.py
python3 candidate/m04i2_unjournaled_probe.py --runtime <runtime>/m02/runtime/m01/repro --variant direct
python3 candidate/m04i2_unjournaled_probe.py --runtime <runtime>/m02/runtime/m01/repro --variant forged
```

| Court | Baseline | M04R candidate |
|---|---:|---:|
| Inherited 413 (89 author + 97 CAN3 + 94 new + 133 owners) | 413 PASS | **413 PASS** |
| M02 independent 100 | 100 PASS | **100 PASS** |
| M03 author 74 | 74 PASS | **74 PASS** |
| **Inherited total** | **587 PASS** | **587 PASS** |
| Fresh frozen M04 51 | **41 PASS / 10 FAIL** | **51 PASS / 0 FAIL** |
| Historical CAN3 nine | **9 FAIL** | **9 FAIL preserved** |
| New adversarial journal tests | — | **4 PASS / 0 FAIL** |

The 51-test baseline JUnit is `51 tests, 10 failures`; final is `51 tests, 0 failures`. The 4-case adversarial JUnit is `4 tests, 0 failures`. The nine historical failures remain nine separate failures, not counted in 51/587.

JUnit SHA-256 receipts generated during this run: baseline 51 `b54c886e1bff4e06e80a699814fd991335b9f5f60baa4842ac360e770682deb3`; final 51 `82eeea88cd2edec98d32c12b9fa237ceccdc9f2b4668f7adece679de5c551f70`; inherited 413 `ec01cd7f…`, `d0115af4…`, `f776605e…`, `60624042…`; independent 100 `50828370…`; author 74 `cf475203…`; historical nine `46052745…`; adversarial four `23ca5692…`.

Fresh-process replay repeated the final 51/51 and 587/587 without shared test state. The 51 suite and inherited suites are in-memory cold reconstructions, not durable-store reopen; no durable C9/CAN3 store is claimed.

## Counterexample before/after

Direct owner API: journal entries remain 2, live transitions become 3; original and M04-patched helpers accepted `read_owner` with `epistemic=REROUTE`; M04R refuses `CLAIM_TRANSITION_UNJOURNALED`. Forged unjournaled pre-state: journal stays 1, transitions become 2; original accepted; M04R refuses `CLAIM_TRANSITION_PRESTATE_ANCESTRY`. Both refusals left the post-call checkpoint unchanged.

## RUN / NOT_RUN

RUN: source staging, original 41/10 and 587/587, M04 patched 51/51, M04R 51/51 and 587/587 in fresh processes, nine historical failures, direct and forged probes, four new adversarial tests.

NOT_RUN: original survey/respondent corpus, native CAN3/ADP016/ADP017/SCI05/Pyat actor/world execution, canonical C9/C12 production, A0–A5 human product, PRE-MAIN/PR #514/#516/#519/#521 mutation, merge or self-review.

## Limits

The patch is a sourcefree test-only helper change. It does not issue a native rule, establish canonical C9 compatibility or repair the nine historical CAN3 failures. The terminal check is targeted at the exact restorative/forged unjournaled route; it is not a blanket journal requirement for every lawful native transition, because that would break preserved original assertions. Independent owner review is required.

DONE: exact baseline, patch, 587/51/4 pass, nine preserved, both probes refused, hashes. REMAINING: owner/reviewer replay and disposition. CRITICAL BLOCKERS: no owner acceptance; native CAN3/C9 authority HOLD. LARGEST PRODUCTIVE MOVE: independent reviewer replays the exact candidate blob against the frozen reviewer test and probes. FLIGHT: local sourcefree only. DELTA: unjournaled restorative terminal is now refused under the same read consumer.
