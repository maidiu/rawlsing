# CP-A5, B-F1CR, and V3CORE — actual use or precise why not

## CP-A5-R2 — consumed on its own sourcefree root

Source cut: `913765328e4fab12b150ea01421ed6b445158184`.

New importer:
`rrif_r3_extension/cp_a5_consumer.py` calls the recovered `cp_a5.scenario.build_cp_life`,
`cp_a5.assertion.run_a5_assertion`, and `cp_a5.encounter.EncounterReader`.

Observed on a fresh CP-A5 sourcefree life:

```text
status: PASS
assertion: cp_a5.assertion.multicontext_encounter_assertion
decision: RETAIN_TOOL
tool answer: OK
market answer: UNKNOWN
market evidence_event_ids: []
observed_event_count: 20
accessed_event_count: 16
unperceived_event_count: 4
read_only: true
```

The market answer was exactly
`UNKNOWN: A did not perceive B's market commission.` The CP-A5 encounter is a
real read-only consumer of A's perceived events; it does not invent an A belief
or B inner life. The extension test checks that asking the market question does
not change the C12 file SHA.

Fault and restore:

- `include_b_activity=False` raises `A4_B_INDEPENDENT_ACTIVITY_MISSING`.
- Restoring the exact intact C12 SQLite makes the assertion `PASS`.
- `EncounterReader(actor_id="B")` raises `ENCOUNTER_ACTOR_SWAP_REFUSED`.

The CP-A5 author suite is **57 passed, 1 skipped, 1 failed**. The one failure is
the staged source-closure test for the live `rawlsing_next.m6_actor_safe_expression`
blob. The extension's actual encounter scenario passes; the full author suite is
not claimed green.

### CP-A5 on the R2 same-root product — exact incompatibility

`ask_cp_a5(state/product, ...)` raises:

```text
ENCOUNTER_BRANCH_REFUSED: BP2_ORIGIN_INVARIANT_MISMATCH
expected actor: TEST_ONLY_BP1_ACTOR_A
actual actor:   TEST_ONLY_BP1_R26V_ACTOR_A
```

The same-root C8 digests differ as a consequence. This is a source-cut identity
conflict, not a missing test or a hash-repair opportunity. CP-A5 is therefore
`SOURCEFREE_CONSUMED_VERIFIED` on its own root and
`INCOMPATIBLE_EXACT_SOURCECUT` at the R2 same-root boundary. Correct receiving
owner: CP-A5 owner plus the BP2/R2 origin owner. No forced attachment.

## B-F1CR-R2 — reconstructed targetless C10 is real, but not integrated

Source cut: `bf3273c294c704ad7c631559b9866d351bb4f103`.

The candidate contains:

- embedded original `f1c_original_104f5bd.py`, blob `104f5bd7826c867...`;
- reconstructed `f1c_reconstructed_candidate.py`, blob
  `c6e64b5874938045d80aae348de94930539d5cd2` (the stated R5 replacement source);
- `targetless_c10_consumer.py`, blob `45997b198e6c0f65b54e523d9b1d6fda09e45ac2`;
- `targetless_i1_bridge.py`, blob `202478dc65a64c14aad20a305968984056732629`.

Actual executed court:

```text
test_targetless_c10.py: 14 passed, exit 0
```

using the reconstructed source and the R2 `vendor/j` runtime. This covers
`REFUSE`, `SILENCE`, `NO_PROPOSAL`, `UNOBSERVED`, evaluated `NO_CHANGE`, the
material ledger, source severance, and cold replay.

But it is not a real product consumer in this return:

- `test_targetless_i1_consumer.py` has **5 setup errors** because the expected
  `intact` pytest fixture is absent from the candidate.
- Running the embedded original as `f1c` yields **13 failed / 1 passed** because
  the reconstructed-only `live_prior` API is absent.
- The claimed original patched F1CR blob
  `bf7e625e1f208908e583ea72ebb73992ad7d19ae` is missing from the canonical object
  graph.
- The reconstructed source must remain identity-distinct from that missing
  original; no adoption as original source.

Status: `ORIGINAL_SOURCE_MISSING_WITH_WARRANTED_RECONSTRUCTION`. Correct
receiving owner: B/C10 owner and the original F1CR source owner. Cheapest bounded
next adapter: supply the missing `intact` fixture and wire
`TargetlessGuardedJoinedProduct` to a selected I1/CP-A5-compatible root, while
keeping the reconstruction grade explicit.

## V3CORE-R1 — source present, material-only, unwired

Source cut: `b5cb3f917402b992d7cbe933af0b378d2b37cbfd`.

The candidate has an actual material-only `project_actual_market_event` I1
adapter (`v3core_adapter/i1_consumer.py`, blob
`e5ea15db51b46ce4932770eb6a7defc4dadf897e`). Its own return reports:

- 3 of 19 annual steps admissible;
- 16 held;
- private 0–100/Enneagram states, pseudo-random biography, arbitrary rupture,
  inferred motive, and unissued Rule A/T quarantined;
- no native person/actor/world.

It was not wired to R2 or CP-A5 because there is no exact source-compatible
material event feed in this return, and importing the private/derived state
would violate the authority boundary. Status: `SOURCE_PRESENT_UNWIRED`.

Correct receiving owner: V3 material owner plus the Sorok/PREMAIN receiver.
Cheapest bounded next adapter: feed one actual repeated market/material source
event and one no-source-event negative through
`project_actual_market_event`, returning only the material summary and
fail-closed state.

## Summary

| Asset | Actual use | Precise reason for remaining hold | Owner target |
|---|---|---|---|
| CP-A5 | `EncounterReader` consumed on own root; tool `OK`, market `UNKNOWN`; read-only | R2 same-root BP2 origin actor mismatch; no human A5 | CP-A5 + BP2/R2 origin owner |
| C9C12 | C12 root consumed on R2; `C12_COLD_READ_OK` | R2 has no C9 `actor_meta`; legacy branch held; no anchor | C9R/BP4/C12 owner |
| B-F1CR | reconstructed targetless C10 **14/14** | missing original `bf7e...`; I1 bridge fixture absent | B/C10 + original F1CR owner |
| V3CORE | material-only adapter present; 3/19 | no compatible material feed; private states quarantined | V3 material + PREMAIN owner |
