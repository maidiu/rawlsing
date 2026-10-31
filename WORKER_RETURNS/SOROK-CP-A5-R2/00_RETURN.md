# SOROK CP-A5-R2 — multicontact continuing person and actual A5 encounter

**Return:** `WORKER_RETURNS/SOROK-CP-A5-R2`
**Base:** `750548ddbb9b4392a16ce93097b856f349e16182`
**Branch:** `agent/sorok-cp-a5-r2-multicontext-encounter-20261030`
**Date:** 2026-10-30
**Host:** oldMac, macOS 13.7.8, x86_64
**Harness/model:** OpenCode 1.18.34 / `opencode-go/deepseek-v4.1-flash`, MAX requested
**Final remote SHA:** reported in the terminal push readback; a file cannot contain the SHA of the commit that contains it.

## Governing result

The actual I1 `GuardedJoinedProduct` is preserved and extended, not replaced. CP-A5-R2 adds a sourcefree A3-A5 scenario and read-only encounter over the same durable C12 history:

- A performs three material inspections across two contexts (workshop and market) over successive intervals.
- C is a separately sourced coactor with its own snapshot and can request, withdraw, and leave without A authoring C's interior.
- A's test-only custody rule produces `RETAIN_TOOL` only when the repeated cross-context evidence is sufficient. Missing evidence or a missing rule produces `HELD`, not an invented change.
- B independently takes the workshop tool, completes a market commission, and returns the tool. B's cash moves `56 -> 58` and completed units `4 -> 5` after I1's initial `54 -> 56` and `3 -> 4`.
- While B holds the tool, A's later repair is blocked with `TOOL_UNAVAILABLE`; after B returns it, A repairs successfully. This is the new material consequence beyond I1's repair/market examples.
- A5 loads the stored history in a fresh process and answers from A's actual perceptions. A reports B's tool-taking and blocked repair, but leaves B's unperceived market commission `UNKNOWN`.

## Three verdicts

### ENGINEERING

**PASS (local candidate).** 59 tests pass: 33 unchanged BP2P4J tests, 9 unchanged BP4R tests, 8 unchanged I1 tests, and 9 new CP-A5 tests. Cold-process CLI, exact restore, all ten old severance trials, and the new A5 assertion pass.

The I1 source is copied unchanged. CP-A5 code is additive under `cp_a5/`, `run_cp_a5.py`, and `tests/test_cp_a5_multicontext.py`.

### SCIENCE

**PARTIAL — bounded sourcefree evidence.** The A5 consumer is a real read of committed C12 events and actor state, not a hand-written transcript. It demonstrates context-differentiated material activity, an independent coactor, a stable test-only derived disposition, a later custody choice, and a material consequence caused by independent B activity.

It does **not** establish native personhood, a native coactor source, original B childhood/casual life, a native disposition, or a universal psychological rule. C is an explicit test-only coactor fixture, not an original B/M35 producer.

### AUTHORITY

**HOLD — no adoption.** `OWNER_ANCHOR_REQUIRED` and the sourcefree CAN/ADP limits remain. No C12 anchor, C9 durability, native actor, Pyat position, CAN/ADP/SCI05 issuance, PRE-MAIN mutation, pull request, or self-review is claimed or performed.

## New material consequence

Causal chain at the same consumer:

1. A performs three cross-context inspections and the test-only rule records `RETAIN_TOOL`.
2. B independently returns to the workshop, takes the tool, earns `+2` cash and `+1` completed unit at the market, and returns the tool.
3. A's repair at clock 80 is objectively blocked while the tool is away.
4. A repairs successfully at clock 100 after B returns it.
5. The A5 view reports B's tool-taking and A's blocked repair; B's market commission remains unperceived and is reported `UNKNOWN`.

The I1 `material_delta: -1` event with zero stock is **not** repeated as a new consumption claim. The new B commission records `material_delta: 0` and uses the actual tool resource, avoiding the I1 floor-to-zero ambiguity. The old I1 test is preserved unchanged.

## Required same-consumer tests

| Requirement | Test |
|---|---|
| Intact history produces A5 encounter | `test_intact_multicontext_life_reaches_the_a5_assertion` |
| Sever B activity -> downstream consequence disappears | `test_sever_b_independent_activity_reddens_then_exact_restore_greens` |
| Remove A access -> cannot report/remember | `test_removing_a_access_makes_the_tool_unknown` |
| Swap actor/branch identity -> refusal | `test_actor_or_branch_identity_swap_is_refused` |
| Renderer-only change -> canonical state identical | `test_renderer_output_change_does_not_mutate_canonical_state` |
| Remove transition rule -> HELD | `test_missing_custody_rule_emits_held_not_a_decision` |
| Single-context evidence -> insufficient | `test_single_context_inspection_is_insufficient` |
| Fork after acquired activity -> parent preserved | `test_fork_after_acquired_activity_preserves_parent` |
| Restore unchanged source -> GREEN | exact C12 copy in the B-severance test |
| Cold process / read-only CLI | `test_cold_process_cli_loads_history_without_writing` |

## Run evidence

```sh
cd candidate
BP4R_C9_DIR="$PWD" PYTHONPATH="$PWD" \
  python3 -m pytest -o addopts='' -q tests \
  --junitxml=evidence/cp_a5_junit.xml
```

Observed: `59 passed in 30.50s`, exit `0`; JUnit `59 tests, 0 failures, 0 errors, 0 skipped`.

Old regression split: 10 joined product, 12 security, 7 severance, 4 source closure, 9 BP4R, 8 I1 = 50; new CP-A5 = 9.

Actual generated encounter trace: `01_ACTUAL_A3_A5_LIFE_AND_ENCOUNTER_TRACE.json`.

## DONE

- Preserved the actual I1 guarded product and old 50-test regression surface.
- Built and executed a sourcefree multicontact A3-A5 life with an independent B and separate C.
- Added a read-only A5 CLI/consumer that reports only A's perceived C12 events.
- Added the new tool-custody material consequence without fabricating B interior or repeating I1's zero-stock delta.
- Added 9 new same-consumer tests, JUnit, cold-process replay, exact restore, and generated trace.

## REMAINING

- Owner decisions on CP-A5 coactor source legitimacy, the test-only custody rule, and any public A5 projection.
- External C12 anchor/custodian and durable C9 actor/readset remain unresolved.
- No native person, native B/C source, CAN/ADP/SCI05 issuance, Pyat structural world, or native A0-A5 participant.

## BLOCKERS

- `OWNER_ANCHOR_REQUIRED`: guard verifies content/fork/schema only; authenticity/completeness unverified.
- C9 R3B durability and cross-store actor handoff remain held.
- `bp2p4/c12_verify.py` self-referential upstream issue remains unchanged and is not used by the I1 guard path.
- No original B/M35 producer or F1CR patched executable is claimed.

## LARGEST PRODUCTIVE MOVE

Extend the same `run_a5_assertion`/`EncounterReader` consumer with an owner-selected durable C9 actor readset and external anchor, after an independent reviewer accepts the C coactor fixture and custody rule. Do not merge CP-A5 before that review.

## FLIGHT

Local S2: Git worktree, Python 3.11.3, pytest 9.1.1, SQLite 3.40.1. No browser fallback, no model/provider switch, no network at test runtime.

## DELTA

Adds a genuinely executed sourcefree A3-A5 life and read-only encounter beyond I1's A0-A2/guarded C12 surface, with independent B/C activity, a context-differentiated custody decision, a real tool-conflict consequence, and claim-specific positive/negative/restore evidence.
