# SOROK C02/C03/C04 AGENT B — period, decision, and speech relay handoff

**Packets:** C02 (current-clock + incremental B02 periods), C03 (materially situated parent decision/action), C04 (hidden reason / utterance / Nadia-qualified uptake).
**Status:** sourcefree `SOURCEFREE_S2_ONLY`; C02 parent/B02/B04 period path and C03/C04 sourcefree mechanics constructed. Full C02 P3 `BatchEngine` interleave, B04 currency-writer repair, B05 rent integration and native/science/authority remain held.
**Branch:** `codex/sorok-duel-c02-b-period-c03-20261112-r1`.
**Start composition:** `4724125721c646024bc2ef16b11510e4584991a8` = A C02 `4528b68ad4e285a77509687511dcc8765cd41ca7` + Pair1 B02/B04/B05 `8de517bd3c0d2a8afb29509c7917d62cac4dc59a` (production `62292613aa9210a7d3e944314e36924349337439`), clean merge, unexecuted/unaccepted.
**B implementation commit:** `255fd4905990e3c0cab3e2d95ba91b851ea701a8`.
**B return commit:** the branch tip after this return-document commit (exact SHA reported to HQ).
**A implementation under attack:** `9ac1ac71cdbc8dd2c832b2980b501b4031e163e8` / A return `4528b68ad4e285a77509687511dcc8765cd41ca7`.
**Received B C01 implementation:** `0e526f043027e4256b353d42240e80d85ad39265`; return `4d93685df4c5abdfbd09f44510a24a41c850b6a8`.
**Contract:** #939/PR938 `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`; protected baseline `6a5c12f04323d74001f9632063ec907f4fc4468e`.

**Independent reconstruction** was recorded before A's handoff/diff at `WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/AGENT_B_RECONSTRUCTION.md`. The two full Library architecture records remain NOT_INSPECTED locally.

## 1. A's valid improvements and criticisms — conceded

- A's normal live-root background entry is real and preserved: `run_p4.run_parent_operation`/`run_p6.parent_background_operation` guard source/boundary, write a pending fail-stop marker, execute closed operations, and record the actual after snapshot through the existing P4 activity protocol. Fresh-process P6 view and user say after parent activity succeed.
- A correctly accepted B's C01 repairs and preserved them; A's C02 parent kernel, truthful `MATERIAL_ACTIVITY` event, history-bound material, currency boundary and lock remain intact.
- A's B02 current-period ingress was directionally correct and its refusal of a parent write when B02 is absent/unqualified is preserved. A's statement that B02 now exists at the composition is accepted; B's earlier global “B02 absent” status is superseded.
- A's live-root and P6/P4 boundary claims at the tested cut are accepted for the operations A exercised. A's `PARENT_B02_FULL_PROOF_HOLD` was a correct hold *before* the prepared composition exposed `materialize_to`/`period_progress`; it is stale at this start, not evidence of a hidden defect.

## 2. Invalid/stale claims and refuted attacks

- **“The required incremental B02 current-period hook is absent.”** Refuted at this composition: `historical_period.period_progress(session, period_id)` returns the current date/progress, and `materialize_to(session, as_of_date)` advances only the unelapsed range with durable receipts/recovery. B uses these; no new B02 owner or fabricated date is needed.
- **“`PARENT_B02_FULL_PROOF_HOLD` is the current qualified state.”** False once the plan is established. A's two live-test assertions expecting the old `B02_FULL_DATED_PROOF_HELD_PLAN_ABSENT` value fail under the corrected qualified reader; A's other seven C02/live tests pass. This is stale documentation/test expectation, not a runtime regression.
- **A's manual anchor/ticks date inference** duplicated B02's mapping instead of using the qualified current-period reader. B replaces it with `period_progress` + `read_material_period` and validates logical tick/period identity.
- **B's prior global “B02 not built” claim** is conceded as superseded. B now composes the actual incremental API.
- **A's “actual author fresh-process P6 view+say”** is accepted; B independently runs P6 view and say after parent activity/speech.
- **The parent currency conflict is real, not a B reader fault.** B does not convert or equate `parent_sourcefree_currency_unit` and `sourcefree_currency_unit`; C03 refuses mismatch before B04 is called. B04's own default tests now fail because its writer still admits/submits a mismatched purchase. Exact required B04 ABI is returned in `B04_CURRENCY_EXPECTED_ABI.md`.

## 3. New failures established in A's latest version / shared cut

### D1 — A's B02 period context was manually inferred and carried a false global hold

A's `_period_context` rederived the current date from anchor/clock/ticks and advertised `HELD_INCREMENTAL_CURRENT_PERIOD_API_MISSING`. The actual B02 incremental API exists at the prepared composition. B now uses `period_progress`/`read_material_period` and proves two chronological periods; the stale hold is removed. A's two historical assertions fail only on that superseded constant.

### D2 — No two-period parent proof existed

A explicitly held the two-period proof. B adds a normal P4 `period-materialize` operation over B02 `materialize_to`, proves period h1 (including the 2026-03-15 B02 employment change) and period h2, parent employment/debt/care changes across them, later options/decision, cold reopen, source severance/restoration, and ordinary P6 view.

### D3 — Parent material history rejected B04 purchase episodes

After B04 `P2_PARENT_PURCHASE` changes parent material, A's `_parent_material_history` recognized only antecedent/activity/circumstance. Parent material/options/history then failed `PARENT_MATERIAL_HISTORY_MISMATCH`. B adds narrow typed acceptance of the exact B04 receipt (schema/status/identity/root/branch/source chain/currency) and rejects unknown episode kinds. The history now validates the before/after source chain, not only the latest material source.

### D4 — B04 writer admits a parent currency mismatch

B04 `purchase_drum_kit` debits a parent whose material currency is `parent_sourcefree_currency_unit` while the market/request use `sourcefree_currency_unit`, and its receipt declares an equivalence. B's parent owner refuses that admitted purchase with `PARENT_PURCHASE_CURRENCY_MISMATCH`; C03 refuses the mismatch before invoking B04. B04/B05 default tests fail at this boundary until Pair1 B implements the exact ABI in `B04_CURRENCY_EXPECTED_ABI.md`. This is not silently converted or hidden.

### D5 — C03/C04 were absent

A had no parent decision/action admission and no hidden-reason/utterance/uptake split. B constructs both at sourcefree grade (below).

### Shared failures both previous versions carried

- No actual P3 `BatchEngine` 3–5 event cycle across the B02 employment change/period boundary; the parent throughline is proven at P2/B02/C02/C03 mechanics, not a full P3 batch.
- B04/B05 currency conflict and default fixture mismatch, as above.
- P3 source closure does not pin `parent_activity.py`, `parent_decision.py` or `parent_speech.py`; no P3 edit or pin weakening.
- No full E03 crash reconciliation, no fork/cold parent lineage, no shared household budget/rent/purchase reconciliation, no native/MIII scientific decision rule, no independent terminal receiving.
- C04 uses the existing P2 `SPEECH` event and C12 speech perception; it does not alter P4 user-speech semantics or claim a user-visible parent speech.

## 4. Repairs implemented

### C02/B02 — qualified incremental period context and two-period proof

`parent_activity._period_context` now:

1. reads the actual B02 plan;
2. finds the period whose declared clock range contains the actual S46 clock;
3. calls `historical_period.period_progress(session, period_id)` for the current date/progress;
4. calls `historical_period.read_material_period(session, current_date)`;
5. requires `logical_tick == session.clock()` and the same `period_id`;
6. carries `period_progress`, `as_of_relation`, `interval_status_detail`, `current_interval_status`, plan/employment sources, and `full_dated_proof=B02_INCREMENTAL_PERIOD_API_QUALIFIED`.

`run_p4` adds the closed `period-materialize` operation calling B02 `materialize_to`. B02/B04/B05 code is not edited. A test proves h1/h2, B02 employment `employment:civic-works` distinct from parent-local employment, parent job loss/rehire, debt/care/work across periods, C03 purchase after two periods, cold reopen, source severance (current options HELD; historical activity receipts keep their period) and restoration.

### C02/B04 — exact purchase history acceptance and currency boundary

`parent_activity._parent_material_history` now accepts the exact B04 `P2_PARENT_PURCHASE` episode:

- schema/grade/root/branch/actor/alias/status and nested receipt identity;
- `parent_material_source_before/after` hashes; admitted purchase after source must match the chain; refused purchase must have before == after;
- admitted purchase possession/effect fields and event clock;
- admitted purchase currency must equal the current parent material currency; otherwise `PARENT_PURCHASE_CURRENCY_MISMATCH`;
- ordered before/after source-chain continuity across antecedent/activity/circumstance/purchase rows;
- `read_parent_history` returns typed purchase rows with object/owner/currency/purchase source and `purchase_episode_count`.

Matching-currency C03 purchase is accepted; mismatched C03 decision refuses before B04. B04's required writer change is exact and separate.

### C03 — explicit sourcefree parent decision and performed action

New `parent_decision.py`:

```text
parent_request_fixture(kind="junior", owner_actor_id)
propose_parent_decision(session, parent_id, request, as_actor)
admit_parent_decision(session, parent_id, operation_id, request, as_actor, expected_clock)
perform_parent_decision(session, parent_id, decision_id, as_actor)
read_parent_decision / read_parent_action
```

The explicit rule `SOROK_SOURCEFREE_PARENT_OBLIGATION_PURCHASE@1` (sourcefree hypothesis, `native_science=false`, `child_outcome=NOT_READ`) requires: request/market/parent currency equality; B03 material constraints except household affordability; actual market stock/price/kind; parent cash/free-hours; after-purchase cash ≥ parent debt and free hours ≥ care due; explicit owner (parent or focal household holder); B02 current period qualified. It returns PURCHASE/DECLINE/HOLD with reasons; no LLM, fixture answer or Nadia state.

`admit_parent_decision` writes a C12 `P2_PARENT_DECISION` episode (tentative proposal + admitted decision, self-only basis), idempotent by operation id and stale when current material/market/period source changes. `perform_parent_decision` revalidates the decision source, invokes B04 parent-funded purchase for PURCHASE, or records a `VALID_EMPTY`/`HELD` action for DECLINE/HOLD; it writes one C12 `P2_PARENT_ACTION` episode and returns REPLAY on retry without re-debiting. A changed debt/care/cash/currency/stock changes the admitted decision; A household/Nadia cash changes do not; a later obligation change makes perform fail closed. Normal P4 operations `market-establish`, `parent-decide`, `parent-perform` route this through the existing boundary/pending/activity protocol.

### C04 — hidden reason, performed speech, Nadia-qualified uptake

New `parent_speech.py`:

```text
perform_parent_utterance(session, parent_id, decision_id, text, hidden_reason, operation_id)
read_parent_utterance(session, parent_id, operation_id, as_actor)
read_child_uptake(session, child_actor_id, event_id)
```

The writer requires an admitted parent decision, commits an actual P2 `SPEECH` event with no hidden reason in the event body, records the parent `own_speech` perception and a focal-child `speech` perception only when the child is co-present, and stores hidden reason/hash in a separate self-only C12 `P2_PARENT_UTTERANCE` episode. It is idempotent and binds the decision/period. `read_parent_utterance` returns the hidden reason only to the parent. `read_child_uptake` requires the exact utterance episode, event hash/author, and the child's `speech` receipt; it returns only the public speech projection and `hidden_reason=NOT_READ`. Co-presence without the speech receipt is `NOT_PERCEIVED`; hiding the event severs the child uptake while the decision remains. Normal P4 `parent-speak` records the actual event/boundary; ordinary P6 view and user say still succeed.

## 5. Proof of improvement

Commands use `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider`; logs are in `evidence/`.

| Check | Result | Evidence |
|---|---|---|
| B C02/C03/C04 packet suite | **11 passed** in 205.63 s | `evidence/b_c02_c03_period_decision.log` |
| A C02 parent tests + A live/B02 tests | **7 passed, 2 failed** only stale `PARENT_B02_FULL_PROOF_HOLD` assertions | `evidence/a_c02_regression.log` |
| B02 incremental suite | **9 passed** in 84.00 s | `evidence/b02_incremental.log` |
| C01 A/B + P2 owner + P3 owner | **28 passed, 1 skipped** in 89.38 s | `evidence/c01_p2_p3_regression.log` |
| B01 + B03 current cut | **15 passed** in 102.05 s | `evidence/b01_b03_regression.log` |
| P4 response/speech + P5 gaze/experience | **7 passed** in 73.83 s | `evidence/p4_p5_regression.log` |
| B04 + B05 current cut | 3 failed at the real currency boundary | `evidence/b04_b05_currency_boundary.log` |

Discriminating results:

- **Two periods:** period h1 at 2026-01-01 and 2026-04-01 after B02 `materialize_to`; period h2 at 2026-07-01; parent work/care/debt/job-loss/rehire cross-period; parent material source/period persists cold; B02 employment holder remains actor A and `b02_employment_applied_to_parent=false`.
- **Source severance:** removing the B02 plan makes current parent material context `B02_PERIOD_CONTEXT_UNQUALIFIED`, options HELD; historical h1 activity receipt still reports period h1; restoring the exact plan requalifies current options.
- **Decision changes:** baseline PURCHASE; debt 80 → `OBLIGATION_DEBT`; care 8 → `OBLIGATION_CARE`; cash 30 → `INSUFFICIENT_PARENT_CASH`; mismatched currency → `CURRENCY_MISMATCH`; zero stock → `STOCK_UNAVAILABLE`; absent B02 → HOLD `B02_PERIOD_UNAVAILABLE`; changing Nadia/household cash only leaves PURCHASE decision unchanged.
- **Actual action/replay:** matching-currency B04 purchase performs one ownership/stock transfer, parent cash 100→60/free 8→7, household A cash unchanged; retry REPLAY no second debit; later debt change makes perform `PARENT_DECISION_STALE`; admitted debt decision performs `VALID_EMPTY`; cold reads/history/purchase consistency.
- **Speech:** same outward text with two different hidden reasons yields identical child public text and no hidden value in child/event; parent self reads distinct hidden reasons; hiding the speech event severs child uptake but preserves the decision; child elsewhere is NOT_PERCEIVED; P6 view and user say succeed after `parent-speak`.
- **B04 boundary:** parent history accepts the exact matching-currency purchase; mismatched parent currency is refused by C03 before B04; B04 default tests fail because B04 still debits on mismatch.

## 6. Preserved inherited functionality and proof boundaries

- B's C01 repairs, A's C02 kernel, B02/B04/B05 code, B01/B03 house code, P3/model_cycle and P6 house/situated were not edited.
- Parent private motive, decision basis and hidden reason remain self-only C12 state; no Nadia/user copy. Parent activity event is not a Nadia percept; C04 speech is the only parent speech path and gives Nadia only the public utterance.
- Decision rule is explicit sourcefree engineering, not native parent psychology/MIII issuance; no LLM sentence is an action.
- B04 purchase is parent-funded; B01 fixed-A household cash is unchanged in C03 tests. B05 household rent is not integrated or double-counted.
- Full C02 P3 `BatchEngine` interleave, B04 currency writer repair, B05 rent integration, E03 crash/retry, fork/cold parent lineage, P3 source closure, MI/P5/P6 parent-activity exposure and all native/source/actor/human/protected authority remain held.
- No full-estate run; only bounded affected suites. Controller/provider cost `UNKNOWN`.

## 7. Exact artifact and file identities

Implementation `255fd4905990e3c0cab3e2d95ba91b851ea701a8` on `codex/sorok-duel-c02-b-period-c03-20261112-r1`:

| Path | SHA256 |
|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_activity.py` | `0463220311d3be74b957667a76ec2c7e0e6047b5fccd924791e8995a5fb6c116` |
| `.../developmental_recursion/parent_decision.py` | `5e0857acac6f14d3bb67785e1fe0edfd6af3f2fb640f2a3d2ab17b557ad23ba8` |
| `.../developmental_recursion/parent_speech.py` | `31e5fad79dfeda71b4632074b3e2df635121eb532bb44ba6303f8459c52d01b0` |
| `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py` | `f5f7ea789d6f0fd0df8496756ade7f19a2d18c4fc1b3f3275958a8eed4a7e537` |
| `WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/test_c02_c03_b_period_decision.py` | `50e60db405a3ef82f98b34d0b06c1dc9cd3910060a661986b244c399917f066b` |

Return artifacts: this handoff, `AGENT_B_RECONSTRUCTION.md`, `C02_C03_C04_B_ABI.md`, `B04_CURRENCY_EXPECTED_ABI.md`, `PROGRAMMA_DELTA.json`, `impact.json`, `evidence/*.log`. A's historical C02 artifacts under `WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/` and `A_RETURN_R2/` are preserved unchanged.

## 8. Material unresolved questions and blockers

1. **B04 writer currency guard.** B04 must require parent currency == request/market currency before debit and carry exact currency fields; B04/B05 default fixtures/tests fail until Pair1 B applies `B04_CURRENCY_EXPECTED_ABI.md`. C03 currently refuses the mismatch before B04, and matching-currency C03 works.
2. **Full P3 BatchEngine interleave.** B proves B02 materialization plus parent P2/C02/C03 mechanics, not a P3 3–5 event batch across periods. P3 source closure and actual P3 actor decision consumption are Pair2/shared-owner work.
3. **B05 rent/household budget.** B05 rent is not integrated with C03 and parent/household currency sharing remains unreconciled; no conversion/double count is claimed.
4. **B04/B05 ownership/stock source severity and E03.** C03 uses B04's atomic purchase/refusal; composite P4/B04/C03 crash recovery and SIGKILL are not proved.
5. **C04 user/Nadia product boundary.** C04 reads Nadia's C12 `speech` receipt; it does not alter P4 user speech or claim the user sees the parent utterance. A later P4/P6 child experience consumer must deliberately compose.
6. **Fork/cold lineage, MI/P5/P6 `MATERIAL_ACTIVITY` exposure, P3 pins and old-root migration** remain as previously disclosed; no migration/weakening invented.
7. **Sourcefree decision rule.** C03 is an explicit experimental obligation/purchase rule, not MIII/native mother science or a general LLM decision. No native issuance.
8. **A's two stale live-test assertions** expect the old full-dated hold; A must update them to the qualified incremental API. The other seven A C02/live tests pass.
9. **No independent acceptance.** B/A are constructive authors, not terminal receivers.

## 9. Fresh challenge to SAME Agent A

1. **Apply the B04 currency ABI** (or a superior safe equivalent): make B04 refuse mismatch before debit, update B04/B05 fixtures to matching parent currency, and prove B04/B05 tests green while C02 history accepts the exact admitted purchase and C03 refuses mismatch.
2. **Run a full P3 `BatchEngine` 3–5 event cycle across the B02 employment change and a period boundary**, with C03 parent decision/action between periods, one span, one rent, one purchase, one ownership row, and cold replay. B's parent-side proof does not substitute for the P3 batch.
3. **Connect C04 to the actual Nadia/P6 experience** (P3 actor current experience/response input), not only the C12 child speech receipt, while keeping hidden reason unreachable and user/actor perception distinct.
4. **Reconcile the household budget**: B05 rent, B01 fixed-A cash, B04 purchase, parent cash/debt and C03 decision in one explicit no-double-count policy; no silent conversion.
5. **Prove E03** crash/retry/ownership exactly-once across B04 purchase → C03 action → C04 utterance, including a real SIGKILL at the state/receipt boundary.
6. **Attack B's decision rule**: make a legitimate material fact (currency, stock, debt, care, B02 term) change without changing the decision or vice versa; if that succeeds, repair the rule. Do not substitute fixture answers or Nadia trait back-solving.

**Hardest concrete challenge for my cut:** compose B04/B05 currency-safe purchases/rent with a full P3 batch across two B02 periods and a real P6/Nadia turn, then cold-crash every owner boundary and prove one period, one rent, one debit, one ownership record, one decision/utterance and one qualified child uptake, with no hidden-reason leak. If A can do that while preserving the existing greens and the explicit B04 ABI, A has surpassed this return.

## Measured cost and limits

B packet suite 205.63 s; A C02/live 88.92 s; B02 84.00 s; C01/P2/P3 89.38 s; B01/B03 102.05 s; P4/P5 73.83 s; B04/B05 27.35 s. Controller/provider token, latency, RSS and retry cost: `UNKNOWN`. Sourcefree `SOURCEFREE_S2_ONLY`; no native actor science, original CAN/ADP/Pyat, source/use rights, human validation, independent acceptance or protected merge.
