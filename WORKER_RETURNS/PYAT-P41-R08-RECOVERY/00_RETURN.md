# RRIF-P41/R08 — selected-world seam, evidence binder and progressive service

**Role:** independent I3+ developmental-scientific consumer/ABI and sourcefree
integration engineer. Not original P41/R61-R08/SC0/N9 issuer, PE successor author,
Sorok actor engineer, PRE-MAIN integrator or own reviewer.

**Repository:** `maidiu/rawlsing` (private).

**Branch:** `agent/pyat-recover-p41-r08-world-evidence-consumer-20261030-r1`.

**Branch startup:** `750548ddbb9b4392a16ce93097b856f349e16182`.

**Current PRE-MAIN recheck/pin:** `8e44ca9c751049d65e6def47600b5c073ee04b29`.
The branch is based on this current cut (startup is its ancestor); `rawlsing_next`
tree is identical: `1d88d3fbb1d18dadfda946d9cd7f309d84afa479`.

**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-p41-r08-recovery-20261030-r1`.

**Fresh session:** OpenCode CLI, agent `build`, model
`opencode-go/deepseek-v4.1-flash`, variant `max`; `OPENCODE_PID` session isolated
in this worktree. S2 local full Git/sourcefree pytest; no original survey or
respondent data; no native C or actor execution.

**Write scope:** only `WORKER_RETURNS/PYAT-P41-R08-RECOVERY/`. No shared
production file, protected PRE-MAIN branch or actor/world state was modified.

## FINDING

### 1. Selected-world seam is genuinely RED at its original cut

Exact S3 cut `ed34944e253b78714a28d72b8ca2a6521ce15930`:

- selected-world contract tests: **24 passed**;
- exact seam witness: **26 passed / 1 failed**;
- failure: `test_s00c_change_source_owned_synthetic_numeric_values_changes_result`
  -> `KeyError: 'exact_probabilities'`.

The consumer did not ignore the numeric change. It returned
`REFUSED / PRODUCER_VALUE_IDENTITY_MISMATCH`: changed source-owned cells were
still bound to the old selected-world contract, so the contract/source identity
no longer matched. The positive 24-test court does not mask this RED.

The original failing receipt is preserved. The bounded sourcefree repair proves
the missing transition:

- old cells 3,1,1,3 -> Q86B=1 conditional **3/4**;
- rebound cells 3,1,2,2 -> **1/2**;
- same denominator 4, different contract/value dependency;
- old contract + changed channels -> `SOURCE_VALUE_CONTRACT_MISMATCH`;
- zero denominator -> `ZERO_SUPPORT`, missing step -> `NO_SUPPORT`;
- cold restore exact; tampered payload refused; live mutation refused then
  restored green.

Court: **5/5 passed** in `tests/test_selected_world_repair.py`.

### 2. P41 historical service is green at its declared sourcefree scope

Exact P41 branch `f27d1101048638bba395143a48efb7ef00bfcda4`:

- P41 suite: **19/19 passed**;
- W1 N10E computed edge, W2 N9 structural edge, W3 selection/currentness edge:
  **3/3 `BOUNDED_MUTATION_DETECTED`**;
- restored P41 suite: **19/19 passed**.

This proves historical P41 behavior, not a current production receiver.

### 3. Current E03 and current owners are real sourcefree producers

At current `8e44ca9c...`:

- current E03 progressive candidate: **18/18 passed**;
- current C1 + N10E + F8: **69/69 passed**;
- current learned-world composition: **30/30 passed**.

A bounded current P41-style adapter now calls current E03 (which calls current
N10E→C1→F8), returns exact 32→16→8 / 9/16→5/8→3/4 geometry, records F8
consumption, supports as-of/publication/rule metadata, revocation, historical
archival, cold restore and tamper refusal. Court: **5/5 passed**.

The adapter explicitly labels the rule/clock layer
`ADAPTER_TEST_ONLY_CLOCK__NO_SOURCE_RULE`; it is not an original N9 or source
rule issuer.

### 4. R08 binder is recoverable only as staged sourcefree evidence

Current `rawlsing_next` **does not contain**
`pre553_universal_evidence_binding.py`. The exact binder blob
`3ca860e409f1d063da4cd03dd1691a89c67333f6` was staged into an isolated current
tree with exact C1 fixtures:

- author suite: **113/113 passed**;
- R8 targeted refusal/semantic probes: **8/8 passed**.

This proves the missing binder primitives can run against current sourcefree
producers. It does **not** prove a current production import, native source
warrant, real issuer or adoption. The HMAC authorities are local ephemeral test
doubles, not source grants.

### 5. No current production receiver exists

There is no lawful current production consumer for P41, selected-world or R08 in
this cut. Current E03 and the P41-style adapter are test-only. R08 has no current
module import. PE owner-bound successor `a48c6acb...` is author-only TEST_ONLY
(33 tests; independent court pending), not a current PE/world receiver. Original
PE strict remains **4/13**; V2K retirement and C11 anti-join hold remain visible.

## INTERPRETATION

The missing scientific/engineering value is real at fixture scope: current
N10E/C1/F8/E03 can drive a progressive receipt, the selected-world numeric change
can be lawfully rebound, and the exact R08 admission/binding primitives can run
against current producers. None of this is a production integration. The
selected-world failure was a contract-rebind defect, not a missing arithmetic
producer. The historical P41 19/19 and R08 113/8 are bounded evidence, not
current native source or scientific issuance.

## ACTION

1. Keep the original S3 seam RED visible; do not erase the 26/1 receipt.
2. Use `selected_world_repair.py` only as a bounded sourcefree alternative; do not
   claim it is the original N9 selected-world contract.
3. Keep the current P41-style adapter as a test consumer; do not claim N9/N10W
   service acceptance.
4. Recover R08 only by naming a real current receiver; do not copy the 118 KB
   binder into production or treat 113+8 as native warrant.
5. Route P41/R08/selected-world to the original owners; require a named current
   adopter and independent I3 review.

## OWNER

Original P41/E04L/N9/N10W owner, R61-R08 evidence owner, selected-world/SC0
owner, incumbent Pyat/HQ intake, and a distinct independent reviewer. No self-review.

## Actual test receipts

| Court | Exact cut | Actual |
|---|---|---|
| P41 19 | `f27d1101...` | **19 passed**, exit 0; restored **19 passed** |
| P41 W1/W2/W3 | `f27d1101...` | **3/3 BOUNDED_MUTATION_DETECTED**, exit 0 |
| E03 18 | `8e44ca9c...` | **18 passed**, exit 0 |
| Selected-world 24 | `ed34944e...` | **24 passed**, exit 0 |
| Seam 27 | `ed34944e...` | **26 passed / 1 failed**, exit 1; KeyError preserved |
| Current C1/N10E/F8 | `8e44ca9c...` | **69 passed**, exit 0 |
| Current learned-world | `8e44ca9c...` | **30 passed**, exit 0 |
| R08 current-provider staged | current tree + exact blob | **113 passed**, exit 0 |
| R8 probes | R8 review cut | **8 passed**, exit 0 |
| Selected-world bounded repair | current worktree | **5 passed**, exit 0 |
| P41 current-style adapter | current worktree | **5 passed**, exit 0 |

Exact commands are in `TEST_RECEIPTS_AND_FAULT_NEGATIVES.md`; binder ingress is
in `EVIDENCE_BINDER_INGRESS_MAP.md`; selected-world readback is in
`SELECTED_WORLD_DEFECT_READBACK.md`.

## Courts

- **ENGINEERING:** `SOURCEFREE_ADAPTER_AND_CURRENT_PRODUCER_TESTS_PASS__P41_SELECTED_WORLD_REPAIR_AND_R08_STAGED__NO_CURRENT_PRODUCTION_RECEIVER__HOLD`.
  No fake world/refresh/issuer was used; no missing field was silently masked.
  Current receiver/production adoption is absent, so this is HOLD, not ACCEPT.
- **SCIENTIFIC:** `SOURCEFREE_FIXTURE_AND_TECHNICAL_ACCEPT__HOLD_ORIGINAL_SOURCE_SCIENCE__NO_CAUSAL_OR_REAL_POPULATION_CLAIM`.
- **AUTHORITY:** `HOLD__NO_ORIGINAL_U_E_CAN_ADP_SCI_MODEL_WORLD_N11_N12_OR_SOROK_ACTOR_GRANT__NO_MERGE`.

## DONE / REMAINING / BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

**DONE:** exact historical P41 19 + 3 witnesses and restore; current E03 18;
current C1/N10E/F8 69; learned-world 30; selected-world 24 and exact seam 26/1;
bounded selected-world repair 5; current P41-style adapter 5; R08 exact binder
113 + 8 against current producer; sourcefree adapters/tests/receipts; science and
authority holds; reviewer request.

**REMAINING:** name a lawful current production consumer; owner decision on
selected-world/current N9 contract; R08 production receiver; original source
issuance; PE successor independent court; V2K anti-join owner decision.

**BLOCKERS:** no current P41/R08 production import; no current N9/N10W owner; no
original source/actor/science grant; selected-world repair is bounded synthetic;
R08 HMAC trust is test-only; no merge.

**LARGEST MOVE:** keep current E03 plus sourcefree adapters as scoped evidence,
name a real current receiver and production trust boundary, then run the same
positive/mutation/revocation/replay/cold tests under that receiver.

**FLIGHT:** `P41_19_PASS + P41_WITNESS_3_PASS + E03_18_PASS + SELECTED_24_PASS + SEAM_26_1_RED_PRESERVED + SELECTED_REPAIR_5_PASS + P41_CURRENT_5_PASS + C1_N10E_F8_69_PASS + LEARNED_30_PASS + R08_113_8_STAGED + PRODUCTION_RECEIVER_GAP + SCIENCE_AUTHORITY_HOLD + NO_MERGE`.

**DELTA:** `+` P41 historical proof and severance; `+` selected-world defect
readback and bounded repair; `+` current P41-style adapter over current E03;
`+` current owner tests; `+` R08 exact binder staged 113+8; `+` explicit GAP CARD
and holds; `−` no current production receiver; `−` no original source/science;
`−` no merge/adoption.

## Return artifacts

- `00_RETURN.md`
- `FUNCTION_AND_CONSUMER_MAP.md`
- `SELECTED_WORLD_DEFECT_READBACK.md`
- `EVIDENCE_BINDER_INGRESS_MAP.md`
- `TEST_RECEIPTS_AND_FAULT_NEGATIVES.md`
- `SCIENCE_AUTHORITY_AND_INTEGRATION.md`
- `REVIEWER_REQUEST.md`
- `sourcefree_adapter/selected_world_repair.py`
- `sourcefree_adapter/p41_current_service.py`
- `tests/test_selected_world_repair.py`
- `tests/test_p41_current_service.py`
- `repro/run_sourcefree_adapters.sh`
- `repro/run_r08_current_binder.sh`

Exact pushed remote SHA is reported in the completion message and is not
self-referenced inside its own commit. Independent post-return I3 review is
required; no automatic worker spawn.

TERMINAL: `P41_SELECTED_WORLD_REPAIR_AND_CURRENT_ADAPTER_PASS__SEAM_RED_PRESERVED__R08_STAGED_113_8__NO_CURRENT_PRODUCTION_RECEIVER__SCIENCE_AUTHORITY_HOLD__NO_MERGE`.
