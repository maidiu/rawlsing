# SOROK C02 AGENT B — relay construction handoff

**Packet:** C02, `Independent mother antecedent and continuing materially conditioned activity`, CG-C.
**Status:** current-clock parent material/activity kernel strengthened; **full C02 remains `PREREQUISITE_HELD` on B02 calendar/as-of/period qualification and on C03 decision/utterance**.
**Grade:** `SOURCEFREE_S2_ONLY`.
**Branch:** `codex/sorok-duel-c02-b-counter-20261112-r1`.
**B implementation commit:** `3f9d1079bc3b1f09a318afc80bd5aa63d7ccdecf` (parent A HEAD `ff9b6d85d32b1529ea32b5488f1fd8a623786d26`).
**Attacked A C02 implementation:** `ace64f7794a4dd9324bc67768835083b452c49b2`.
**B C01 received implementation:** `0e526f043027e4256b353d42240e80d85ad39265`; B C01 return `0fd303e2af23d71b51b068393cfaa6f62d40fe38`.
**Composition start:** `5932a509095f92f2d2b463b0899b27ac851741f6` (B C01 + Pair1 A B01-counter/B03 `5bc29474e769b928d9264f1607bab605e2b1c7e9`).
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

**Independent reconstruction first:** `WORKER_RETURNS/SOROK-DUEL-C02-R1/AGENT_B_RECONSTRUCTION.md`, recorded before opening A's C02 handoff/diff. The two full Library architecture records remain NOT_INSPECTED locally; no contents are claimed.

## 1. A's valid work and criticisms — conceded explicitly

A's relay conceded B's five C01 repairs; B did not disturb them. A's C02 is also a real construction, not a paper claim:

- **Parent-local material state exists in the actual P2 world actor row**, not a new owner/database/ledger: employment status, wage, debt, care hours, cash and free hours, with a content source and C12 antecedent/activity/circumstance episodes.
- **Antecedent changes cannot conjure cash** (`PARENT_CASH_REQUIRES_ACTIVITY`); cash changes only through admitted PAID_WORK/PAY_DEBT activity.
- **Performed activity is a real parent-authored world event** plus C12 own_action perception, activity episode and material checkpoint.
- **Replay is operation-idempotent**, later-state replay refuses stale, and A's cold/subprocess tests read the same material/options/history.
- **Parent activity is not a Nadia percept**; focal access is `NOT_PERCEIVED`; the private motive is not in the material/activity/history/event.
- **B02 is honestly held.** A did not invent dates/years; all reads carry `HELD_B02_CALENDAR_ABSENT`.
- A's scope boundary — C02's options are an input, not a C03 decision/utterance — is correct and preserved.

A's remaining three C02 tests pass unchanged under B's repairs (`evidence/a_c02_remaining_tests.log`). A's first test now fails **only** at its historical `event["kind"] == "OFFSCREEN_REPAIR"` assertion, which is the defect repaired below; B's test file proves the corrected behavior.

## 2. Invalid criticisms / false defenses — refuted

A's defense that **`OFFSCREEN_REPAIR` is a carrier kind, not a repair claim**, is invalid. The actual imported consumer chain proves it:

- `bp4.world.make_event` requires the event kind and, when a receipt is present, `validate_owner_receipt(receipt, actor_id=..., act=kind, clock=...)`; the receipt must literally attest the same act.
- A created both with `act="OFFSCREEN_REPAIR"` and `kind="OFFSCREEN_REPAIR"`; the receipt therefore attests a performed repair, not an ordinary work/care/debt activity.
- `s45_projection.project_event` returns the kind unchanged; `bp5`/P5 maps `OFFSCREEN_REPAIR` to the `work` channel; `bp4.c10._verify_world` treats it as an owner-received repair-like action.
- The summary "The parent works a paid shift." does not repair the false kind/receipt. A renamed label is not a truthful carrier.

A's statement that **no existing world symbol was edited** is true for A's cut but not a defense of the false kind; B's narrow repair edits the imported `bp4.world` vocabulary and its `c10` verification consumer, with exact receipts below.

A's **P6/B01/B03 composition** claim is valid only at the static house/dwelling/material-feasibility read level A tested. It is not a live P6 user-turn proof; see §4/D6. We do not accuse A of falsifying its test — we reject reading it as more than it proved.

A's **cash-conservation**, **self-only reads**, **no Nadia perception**, **B02 hold** and **replay/cold** claims survive examination and are preserved.

## 3. New failures established in A's latest version

### D1 — Ordinary parent activity is falsely classified as a repair (high; the source-observed question)

Before repair, an actual PAID_WORK/CARE_DEPENDENT/PAY_DEBT activity produced:

```text
event.kind             = "OFFSCREEN_REPAIR"
event.owner_receipt.act = "OFFSCREEN_REPAIR"
project_event(event).kind = "OFFSCREEN_REPAIR"
P5 gaze channel        = "work" (repair carrier)
```

The owner receipt is not a neutral carrier: `bp4.world.make_event` validates `act == kind`, and `c10._verify_world` validates the receipt for repair-like kinds. The event therefore falsely attests a repair at the actual existing event/projection consumer. No truthful already-supported carrier exists (`REPAIR` is false, `HISTORICAL_MATERIAL` is an MI source-scope episode, `OFFSCREEN_REPAIR` is the defect); the smallest necessary hook is a new `MATERIAL_ACTIVITY` event kind and matching owner-receipt act.

### D2 — Current parent material was not bound to the latest C12 parent history (high)

A's `read_parent_material` validated only the material document's self-computed `source`. A recomputed tampered document (cash changed to 999999, new source) was accepted. A severed activity episode did not change the material/options read at all. This fails the "actual canonical effect/receipt" and "source severance changes private choice but not past fact" obligations: a detached material document could survive independently of its owner history.

### D3 — `read_parent_activity` trusted a format-valid event mapping (medium-high)

The reader checked only `session.event(event_id)` existence and hash equality with the stored episode, then projected it. It did not verify the event author, activity/parameters, parent identity, owner receipt act/clock, period/household fields, or the parent's `own_action` perception. A tampered/forged event mapping could be returned as the parent's activity evidence. The reader needed the actual C12/owner checks, not a hash-only lookup.

### D4 — Parent currency unit was absent, inviting silent conversion (medium-high)

A's parent material had `cash_units`, `wage_units_per_hour` and `debt_units` with no currency unit; B03 household/dwelling uses `sourcefree_currency_unit`. C03/B04 could silently assume the units are the same. The prompt explicitly requires shared-household reconciliation without silent currency conversion. The parent material ABI must state its unit and refuse conversion implicitly.

### D5 — Unserialized read-modify-write activity could lose or duplicate effects (medium)

A read material, evaluated, constructed an event and only then entered `_StoreWrite`. Two concurrent callers could both read the same material source and each admit an activity; the last checkpoint could win while two events/perceptions/episodes exist, or one cash/time effect could be lost. The existing P2Owner serializes its own write unit; C02's new writer did not. A per-state-root lock around the parent read-modify-write unit is the minimal repair, not a new scheduler.

### D6 — Static P6/B01/B03 reads are not a live P6 user turn (material integration gap; shared with C01)

A's C02 composition test reads `house.read_household`, `house.read_dwelling` and `house.material_feasibility` after a parent activity; it does not run a P6 view/turn. Actual `run_p6.experience(state, "view")` after **C01 registration alone** (reproduced) or C02 activity refuses:

```text
RecursionRefusal: P4_COLD_STATE_MISMATCH
```

`run_p4.check_boundary` compares `owner.snapshot()` with the last P4 ledger boundary; direct C12/P2 writes are outside that ledger. This is inherited from C01's direct world writes, not newly caused by C02's vocabulary repair. C02 does not claim a P6 live-turn join; the boundary is recorded and challenged below. P4/P6 integration remains a material blocker for J3/F01, not a C02 completion claim.

## 4. Repairs implemented

- **Truthful event vocabulary (`bp4/world.py:68-71`, `bp4/c10.py:99-100`, `parent_activity.py`).** Added the single `MATERIAL_ACTIVITY` event kind to the imported `make_event` allowlist; `record_parent_activity` now creates `act=MATERIAL_ACTIVITY`, `kind=MATERIAL_ACTIVITY` with the same owner receipt. `c10._verify_world` now requires/validates the owner receipt for this action kind. No other world-event vocabulary or physical-action code was added. `MATERIAL_ACTIVITY` already existed as an H1 entity/role kind in `world.py`; the new event kind uses the same truthful name in the event-kind namespace and does not change H1 entity/role semantics.
- **History-bound material (`parent_activity.py:152, 209`).** `_parent_material_history` reads the ordered parent antecedent/activity/circumstance episodes. `_read_material` requires the current material `source` to equal the latest parent history after/source; otherwise `PARENT_MATERIAL_HISTORY_MISMATCH`. A tampered/recomputed material document and a severed activity episode now fail closed; the committed world event remains.
- **Actual activity evidence validation (`parent_activity.py:782`).** `read_parent_activity` now requires the stored event to match the episode body (author, activity, parameters, before/after sources, event id/hash, household/period/visibility fields), validates the owner receipt with `bp4.world.validate_owner_receipt`, and requires the parent's `own_action` C12 perception at the event clock. Forged author/body/receipt/perception cases refuse.
- **Explicit material/currency boundary (`parent_activity.py:26-64`).** Parent material now carries `currency_unit` (default `parent_sourcefree_currency_unit`, distinct from B03's household `sourcefree_currency_unit`). `commit_parent_circumstances` cannot change it. Every relevant read returns `material_boundary` with `household_cash: NOT_READ`, `household_spend_permission: C03_B04_HELD`, `currency_conversion: NOT_APPLIED`, plus the parent unit. This freezes the C03/B04 join without pretending reconciliation.
- **Historical ingress requirements (`parent_activity.py:40-58`).** Every material/options/activity/history read carries `historical_ingress` with `HELD_B02_CALENDAR_ABSENT`, `dates_claimed: False`, and required `B02_PERIOD_BOUNDARY`, `B02_AS_OF_CLOCK_MAPPING`, `SOURCE_PERIOD_REF`, `MATERIAL_SOURCE_BINDING`. No date/year fixture is invented.
- **Serialized parent writes (`parent_activity.py:134-150`).** `establish_parent_material`, `commit_parent_circumstances` and `record_parent_activity` acquire a per-state-root `parent_activity.lock` around their read/evaluate/write unit. This is a lock, not a scheduler/owner/ledger.
- **Meaningful zero-obligation negatives.** CARE/PAY_DEBT with zero obligation now reach `PARENT_ACTIVITY_NOT_FEASIBLE:NO_CARE_OBLIGATION`/`NO_DEBT` instead of an opaque parameter error; zero-hour/payment with an obligation gets `NO_CARE_HOURS`/`NO_PAYMENT`.
- A's original `parent_activity.py`, `test_c02_parent_activity.py`, `C02_ABI.md`, impact and handoff are preserved; B artifacts are additive under `WORKER_RETURNS/SOROK-DUEL-C02-R1/`.

## 5. Proof of improvement and actual consumer evidence

Commands: `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider`, logs in `WORKER_RETURNS/SOROK-DUEL-C02-R1/evidence/`.

| Suite | Result | Evidence |
|---|---|---|
| B C02 tests (`test_c02_b_parent_activity.py`) | **7 passed** in 18.63 s | `evidence/c02_b_parent_activity.log` |
| A C02 remaining tests (2–4) | **3 passed** in 9.36 s | `evidence/a_c02_remaining_tests.log` |
| A C02 full historical file | 1 failed (superseded `OFFSCREEN_REPAIR` assertion), 3 passed | `evidence/a_c02_historical_kind_superseded.log` |
| B C01 moved + P2 owner + P3 owner | **22 passed, 1 skipped** in 66.33 s | `evidence/c01_b_p2_p3_regression.log` |
| A C01 + P2 owner + P3 owner | **20 passed, 1 skipped** in 55.78 s | `evidence/a_c01_p2_p3_regression.log` |
| P5 gaze + P4 response + P4 speech | **5 passed** in 13.67 s | `evidence/p4_p5_projection_regression.log` |

Discriminating results:

- **Truthful event:** actual event/receipt/projected kind is `MATERIAL_ACTIVITY`; `bp4.c10._verify_world` accepts the state; the word/kind `OFFSCREEN_REPAIR` is absent. `read_parent_activity` returns the truthful kind and receipt activity/parameters/currency; focal access remains `NOT_PERCEIVED`.
- **Independent parent options:** baseline employed/debt=4/care=2/cash=20/free=8 has all three options ADMISSIBLE. Job loss changes PAID_WORK to REFUSED (`EMPLOYMENT_NOT_AVAILABLE`); PAY_DEBT to zero changes debt and then refuses `NO_DEBT`; CARE to zero changes care and then refuses `NO_CARE_OBLIGATION`; no child request or Nadia state is read.
- **Cash/effects:** PAID_WORK hours=2 raises cash 20→30 and free hours 8→6; replay returns the same event with unchanged counts and **cash stays 30**; a later state refuses old-operation replay `REPLAY_STALE`; cold subprocess reads cash 30, history consistent and the activity event kind truthful.
- **History/severance:** a recomputed-source tamper of current material refuses `PARENT_MATERIAL_HISTORY_MISMATCH`, even though the source self-hash is valid. Severing the activity episode makes current material/options fail closed, history consistent=false, `read_parent_activity` NOT_FOUND, but the committed world event still exists; restoring returns the exact source and truthful activity read.
- **Evidence validation:** forged event author, body activity, owner-receipt act, or missing `own_action` perception each refuses with `PARENT_ACTIVITY_EVENT_MISMATCH` / `PARENT_ACTIVITY_OWNER_RECEIPT_INVALID` / `PARENT_ACTIVITY_PERCEPTION_SEVERED`.
- **Material boundary:** parent work/debt/care leave Nadia's `actor_state["A"]`, world resources, B01 household source, B03 dwelling source and B03 feasibility status unchanged; parent options change. Parent currency is explicitly distinct and no conversion is applied.
- **P4/P6 boundary:** actual P6 view after direct C01 registration/C02 activity refuses `P4_COLD_STATE_MISMATCH`; the static house/dwelling/feasibility read composition remains valid. This is recorded, not hidden.

**Actual first consumer:** the self-only `parent_feasible_actions` reader consumes the current parent material and returns ADMISSIBLE/REFUSED options; `read_parent_activity` consumes the actual event/receipt. C03's decision/utterance is **not implemented**; no Nadia reception is claimed.

## 6. Preserved inherited functionality and proof boundaries

- B's five C01 repairs and code are unchanged; A's C01 tests and P2/P3-owner regression remain green.
- B01/B03 `house.py`, module-level P2 material functions/`material_fact`, P3/context/model_cycle, P6 house/situated and Pair2 files were not edited.
- Parent private motive remains in the C01 C12 registration episode; it is not in parent material, activity body/receipt, history, or Nadia access.
- Parent activity remains current-clock only; B02 dated period/calendar is `HELD_B02_CALENDAR_ABSENT`. Full C02 is not complete.
- No parent decision, utterance, child request, Nadia-qualified uptake, relationship, J1/J2, native actor science, C4/ADP-015 issuance, human/source right or protected merge.
- P3 `_code_pins()` is unchanged and still does not pin `parent_activity.py`; the P3 owner must deliberately add source closure if required. No P3 edit.
- No fork/copy parent lineage claim; C01 origin-branch refusal remains. No full-estate run; inherited P3 full-suite timeout and P6 chronology failure untouched.
- Controller/provider cost remains `UNKNOWN`; only measured test wall times.

## 7. Exact revised artifact, branch and file identities

Implementation commit `3f9d1079bc3b1f09a318afc80bd5aa63d7ccdecf` on `codex/sorok-duel-c02-b-counter-20261112-r1`:

| Path | SHA256 |
|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_activity.py` | `25fc23b96c5650f251325b99e9060f5085f74c6a10da08ca4a86a37823dc5b57` |
| `WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/vendor/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j/candidate/vendor/bp4/bp4/world.py` | `525f7b680c3265d631d6c84896a73d4c4b108e9321c3d040fbcd1c3705376d5c` |
| `.../bp4/bp4/c10.py` | `ca69ac871a9a0336a65caf581e4b44ce3b68b55218bde9709dd38ffb7e2f05f8` |
| `WORKER_RETURNS/SOROK-DUEL-C02-R1/test_c02_b_parent_activity.py` | `35107651d2fa866368056a719387a9a388bb2916279019f6df7fb138d1e17000` |

Return artifacts: this handoff, `AGENT_B_RECONSTRUCTION.md`, `C02_B_ABI.md`, `PROGRAMMA_DELTA.json`, `impact.json`, `evidence/*.log`. A's nested C02 artifacts under `WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/` are preserved, not relocated or overwritten.

## 8. Material unresolved questions and blockers

1. **B02 is still absent.** The controller's B02 session directory was checked; it contains launch/ready/process artifacts, no returned/committed terminal receipt. Full C02 remains `PREREQUISITE_HELD`: no dated period, two-period replay, calendar/as-of or split period. The exact ingress needed is frozen in `historical_ingress`; B02 must supply a material source binding that participates in `_parent_material_history`.
2. **P4/P6 live-turn integration.** Direct C12/P2 writes (even C01 registration alone) break `run_p4.check_boundary` (`P4_COLD_STATE_MISMATCH`). C02 does not solve this; P4/F01/J3 owners must define a lawful ledger composition. Static house/dwelling/feasibility reads are not a live-turn proof.
3. **C03/C04.** No parent decision, utterance, hidden-reason/utterance split or Nadia-qualified uptake. `parent_feasible_actions` is input only.
4. **Shared household stock/currency.** Parent material is parent-local; B01's fixed actor-A cash and B03's household/dwelling material are not reconciled. `parent_sourcefree_currency_unit` is deliberately distinct from `sourcefree_currency_unit`; C03/B04 must decide conversion/shared spending explicitly, with no double count.
5. **P3 source closure.** `parent_activity.py` is unpinned by P3; a P3 consumer/integration must decide, without weakening pins.
6. **MI/P5 projection of the new kind.** `MATERIAL_ACTIVITY` is not in MI historical-source kinds, P5 `CHANNELS`, P6 scene, or `bp4.product.other` public-work lists. C02's parent event is not user/child-perceived, so this is deliberate; C04/F03/MI must extend only if exposure becomes lawful.
7. **Fork/copy.** Parent material/activity remain origin-branch-bound; no verified-lineage fork support was copied from Pair1 B.
8. **Sourcefree antecedent strength.** `commit_parent_circumstances` accepts a required `source_ref` label, not a verified external source artifact. This is honest sourcefree input, not native historical evidence.
9. **Concurrency.** The parent lock serializes the read-modify-write unit, but no multi-process stress or SIGKILL test was run.
10. **Self-read authorization** remains caller-asserted; raw C12 developer access remains visible. C04/C09/C12 trust owners must decide stronger confidentiality if required.

## 9. Fresh challenge to SAME Agent A

In priority order:

1. **Compose actual B02** into this boundary and prove two dated parent periods: split at employment/debt/care change, reopen both periods cold, and show source severance changes the later options/private choice without retconning the committed activity event. The material source binding must participate in `_parent_material_history`, and the ingress must not be a renamed year.
2. **Make the actual P6/P4 live user turn consume a root after parent activity** without a second ledger, without weakening the P4 boundary, and without exposing parent private material to Nadia/user. My `P6 view` probe refuses `P4_COLD_STATE_MISMATCH` after C01 registration alone; prove a lawful composition or explicitly hold J3/F01.
3. **Build C03** from `parent_feasible_actions`: a real parent decision/utterance under current material feasibility, hidden reason separate from outward speech, and Nadia receiving only qualified uptake. Do not convert the objective parent event into a Nadia percept.
4. **Reconcile parent cash/debt/wage units with B01 household cash and B03 dwelling affordability** explicitly: no double count, fabricated wealth, silent currency conversion or permissionless spending. Prove the changed-value consequence.
5. **Extend MI/P5/P4 projection semantics for `MATERIAL_ACTIVITY`** only when a lawful exposure path exists, with exact consumer tests; do not reclassify it as repair.
6. **Prove the parent writer's serialization** with a real multi-process/SIGKILL test at the activity transaction boundary.

**Hardest concrete falsifier for my cut:** on one actual root, run a real P6 user turn after a parent activity (not only `read_household`), integrate an actual B02 period record, and show the same stable parent identity, material history, activity receipt and later options survive cold reopen with no duplicate effects, no private leak, no false event kind, and no `P4_COLD_STATE_MISMATCH`. If A can do that while preserving B's C01 repairs and A's remaining C02 tests, A has genuinely surpassed this return.

## Measured cost and limits

Test wall times above. Controller/provider token, latency, process RSS and retry cost: `UNKNOWN`; no instrumentation was available or invented. This is a sourcefree `SOURCEFREE_S2_ONLY` candidate, not native actor identity, C4/ADP-015 issuance, human/source/actor authority, independent acceptance or a protected merge.
