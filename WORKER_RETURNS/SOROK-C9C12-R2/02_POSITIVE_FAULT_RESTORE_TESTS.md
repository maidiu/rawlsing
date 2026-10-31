# C9C12-R2 — positive, fault and restore tests

Observed FINDING: the selected C12 writer/reader edge can enforce immutable episode origin, writer-schema @1, monotonic row clocks and an actor/created-clock anchor, while the C9 R3B actor snapshot/outbox boundary can be read without writes. Causal INTERPRETATION: the remaining incompatibility is not a missing check but an owner/version decision (C9R durable store, mirror/outbox ACK, external anchor). Proposed HQ ACTION: review the candidate edge and owner decisions; do not merge or adopt. Accountable OWNER: original C9R/BP4/C12 owners and separate reviewer.

## Environment and exact source

PRE-MAIN `750548ddbb9b4392a16ce93097b856f349e16182`; base BP2P4J `5b3e6577400ea1d88971ae6b48e41a118b8059ae`; BP4R guard base `e0d9d904…`; C9 R3B writer base `67f34f69…`, patched C9 `b9000cdb…`; C9 schemas `0ae69ef5…` and `5f3f2895…`; C12 original store `c94cd131…`. Candidate files: `c12_guard.py` blob `8f629c29…`, `c9_actor_r3.py` `b9000cdb…`, `c9c12_reader.py` `db38d05d…`, test `4249cb86…`.

## Actual commands/results

```sh
cd candidate/tests
PYTHONPATH=<candidate>:<BP2P4J>/vendor/bp4:<BP2P4J>/vendor/bp4/vendor/bp1:<BP2P4J>:<BP2P4J>/vendor/bp2 \
  python3 -m pytest test_c9c12_r2.py -q
```

Result: **6 passed**, 0 failed/errors/skipped; JUnit SHA-256 `91e314874ce0bd9645019f3f413c5df1bc686ed784e50ce55128ab67c5233bd2`.

Covered:

1. Intact C12 append/fork/cold reopen; C9 genesis snapshot; `read_composite` returns `COMPOSITE_OK__EXTERNAL_ANCHOR_REQUIRED`.
2. Writer-clock inversion: root clock 10, perception 11, episode 10 is refused `NON_MONOTONIC_GLOBAL_CLOCK`.
3. Anchor binding: raw `actor_ids`/`created_clock` mutation changes `anchor_payload`; `check_anchor(None)` returns `OWNER_ANCHOR_REQUIRED`.
4. Writer version @2 and missing-parent fork are refused; C9 writer schema gate returns `C12_WRITER_SCHEMA_UNSUPPORTED`.
5. Forged child transplant is refused at the same reader; restoring the exact child-local row makes the same read green.
6. C9 missing C8 world receipt is refused; missing projection outbox returns `C9_OUTBOX_MISSING`; restoring the exact PENDING row returns the typed `C9_OUTBOX_HELD` (not fabricated ACK).

## Historical evidence preserved

- C9 R3B original 15-case court: **14 PASS / 1 FAIL**, exit 1; failure `test_c6_same_count_perception_substitution_is_held`; JUnit SHA-256 `8bfa25e487841650fa847e7d932a54609bf826fd4a50d51b9fec57c207c58737`. This is the unchanged historical 14/1 observation against original `c9_actor_r3.py` `67f34f69…`.
- BP4R 9-case court against the repaired candidate: **7 passed / 2 failed**, exit 1; failures are exactly `test_residual_global_writer_clock_is_still_accepted_red` and `test_residual_anchor_actor_clock_coverage_remains_unbound_red`; JUnit SHA-256 `8cf5bfb59869ab55b9ceb6dd8e706eb07364deacca1736ef751912868ba856f8`. These two old diagnostic tests are deliberately not used as the candidate oracle: their old acceptance/equality behavior is the historical vulnerability; the new tests assert the repaired refusal.
- BP2P4J performed-E2 vs offered-only pair: `test_practice_is_materialized_from_the_committed_target_and_e2` and `test_without_performed_e2_the_practice_and_world_effect_change`: **2 passed**, exit 0; JUnit SHA-256 `64b095b3380bb5c9526bb0e1a89bb323e9e300e4aa549fd448aac21e1677a8a8`.
- F1C 13/13 and F1CI3 3/3 are not part of this C9R candidate; they remain attributed from R5.

## Fault/restore boundary

C12 forged transplant is restored byte-exactly and the same reader returns green. C9 outbox deletion is restored byte-exactly; the restored PENDING state remains `C9_OUTBOX_HELD`, which is the correct typed state, not an ACK. Mirror/outbox ACK cross-database identity, held Rule A/T finalization, true NOCHANGE and exact performed/offered E2 at the C9 actor layer are **NOT_RUN** in this candidate; no C9R adapter invents them.

## RUN / NOT_RUN

RUN: 6-case C12/C9 candidate suite; C9 historical 14/1; BP4R historical 7/2; BP2P4J performed/offered E2 2/2.

NOT_RUN: C9R mirror ACK cross-database proof; full C9 R3B 15-case suite against candidate (only original 14/1 historical); native C8/C9/C12/Rule A/T/E2; external anchor; A0–A5; PRE-MAIN/PR.

DONE: exact clock/anchor fixes, first-consumer composite, fault/restore tests and historical RED preservation. REMAINING: owner anchor/mirror/version decisions. CRITICAL BLOCKERS: external custodian absent; C9R durable/mirror ACK unproven; C9 old-count compatibility. LARGEST MOVE: owner selects C9R version and anchor custodian, then review the composite. FLIGHT: sourcefree local Python/SQLite only. DELTA: the C12 edge is green under corrected clock/anchor tests while all historical failures remain visible.
