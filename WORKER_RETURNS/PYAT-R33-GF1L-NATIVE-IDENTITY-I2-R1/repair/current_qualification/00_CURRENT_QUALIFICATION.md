# Current GF1 qualification — GREEN, no failure allowance

**282 PASS / 0 FAIL / 0 ERROR / 0 SKIP. No allowed failure list in the current gate.** The nested original44 suite also collects and executes successfully from the previously broken GF1I staging location.

This completes the user's instruction to fix the staging defect and reconcile the six historical assertions while preserving their original evidence. The repaired consumer itself is unchanged from `dd12505c81b9757ca70bb49806aaac494b9a61df`: SHA256 `00a5cc6adc8b6a4074e9ae63d0a57384a8c227e9c88a719683cb0304691a4f9b`.

## Current command

From this checkout, run:

```sh
python3 WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1/repair/qualify.py
```

This is the current qualification entry point. `repair/reproduce.py` remains the inherited repair replay with historical diagnostics; its old failed assertions are not current acceptance requirements. `qualify.py` reuses its full source/native checks, writes new evidence into this directory, and then requires all current successor assertions to pass. It does not treat a count of historical failures as current success.

## Actual results

| Current court | Actual result |
|---|---:|
| Existing product and frozen positive courts (original44, GF1G26, GF1H26, GF1J3, GF1L14, GF1K12, supplemental10, repair26) | 161 pass |
| GF1F current successor (all original cases reconciled, plus true-empty and risk-distinction checks) | 102 pass |
| GF1I current successor (17 inherited checks plus two positive capability gates) | 19 pass |
| **Current gate** | **282 pass, zero failures/errors/skips** |
| Nested original44 from GF1I location, executed by the positive capability gate | 44 pass, separately recorded |

The nested44 execution is a separate proof inside a current GF1I test, not added to the 282-test total. Two new cold processes, PIDs **50311 / 50317**, execute **82 cases each** and cover all four classifications with identical per-case results, exact expected class counts and the exact repaired consumer hash. The reused native replay independently reattests all 74 original files, physically checks imports in two additional cold processes, and preserves the baseline result hash.

## What happened to the six failures

1. **GF1F universe[0000]:** its explicit risk is zero. The current oracle distinguishes no eligible risk from positive risk with zero observations and expects `UNDETERMINED_NO_ELIGIBLE_RISK`.
2. **GF1F named zero-supported-risk case:** its fixture accidentally defaulted risk to the sum of zero counts. It now explicitly supplies eligible risk 2 and retains the intended `UNDETERMINED_ZERO_SUPPORT_RISK` expectation.
3. **GF1F missing-as-empty assertion:** current qualification requires `CONSUMER_PRODUCER_TYPED_STATE_BLOCKING` and preserves `MISSING_TARGET_STATE`. A separate genuinely SUPPORTED empty-profile case proves `RESPONSE_INPUTS_VALID_EMPTY` still works.
4. **GF1F cold coverage assertion:** the original 81-table universe sets risk equal to the count total and cannot cover positive-risk/zero-support. Current cold replay preserves all81 tables and adds that missing case explicitly, checking all82 expected results and exact class counts. The original deterministic replay requirement remains intact.
5. **GF1I consumer-absence assertion:** replaced in the versioned successor by exact physical consumer presence/import hash and a computed value bound to a real native relation.
6. **GF1I collection-must-fail assertion:** replaced in the versioned successor by successful collection and execution of the untouched original44 suite.

`SIX_FAILURE_SUCCESSOR_CROSSWALK.json` maps every exact historical failed node to its reason, changed fixture/assertion, positive successor and actual proof. `GF1F_SUCCESSOR.diff` and `GF1I_SUCCESSOR.diff` make the changes reviewable. No tests are skipped, xfailed or removed from the originals. The versioned successor suite retains all 100 original GF1F case slots and all 19 GF1I case slots, with two added GF1F distinctions.

The current oracle is derived without calling the candidate. It reuses the frozen count tables and derives classifications from explicit eligible risk and support. Its policy is anchored to the precise later GF1G frozen cases g09/g10/g11/g14, preserving no-risk, positive-risk zero support, missing blocking, and valid-empty as distinct states. This qualifies the stated TEST_ONLY fixtures; it does not infer that a source-native producer must emit a SUPPORTED relation for every empty risk set, or overwrite the original R17 typed-zero/source semantics.

## Actual staging defect fixed

Copying only the old `court/` tree omitted two files that its frozen test reads from the return parent:

- `01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json`
- `pinned_refs/PV3N_01_FROZEN_ORIGINAL_EIGHT_OPS_AND_TRUSTED_OWNER.json`

`repair/staging.py` now restores these directly from original commit `9f4a23cef1482e0a81afb1e7a65df90879931465`, checks Git blob identities and refuses existing mismatched bytes. Full receipt: `retained_replay/staged_parent_metadata.json`. This fixes the hidden missing-file error, rather than declaring any collection failure acceptable.

A controlled negative temporarily removes the staged oracle and proves the specific `FileNotFoundError`; exact bytes are restored in `finally`. The subsequent positive test collects44 and runs44 to zero failures. Raw evidence is in `evidence/staging_missing_oracle_negative.log`, `gf1i_nested_collect.log`, `gf1i_nested_run.log` and `gf1i_nested_original44.xml`.

## Preserved history and limits

Original frozen GF1F100 and GF1I19 source files, oracles and prior failures remain unchanged. They still execute in `retained_replay/` as historical diagnostics, with the exact old failed node identities. The original independent review artifact hashes are verified unchanged. Earlier repair evidence is retained at its original paths; new execution outputs live here. Historical observations such as “consumer absent” remain true statements about their old reviewed snapshot, not requirements that a repaired candidate stay broken.

Current qualification is author validation of a sourcefree candidate. No product-source change was needed for this reconciliation, and no canonical owner, source35, SAV/DTA, Field Forge, OC05/N11/N12, actor, Sorok or V3 grant was issued. GREEN here means the explicit current native sourcefree qualification passes, not independent production adoption.
