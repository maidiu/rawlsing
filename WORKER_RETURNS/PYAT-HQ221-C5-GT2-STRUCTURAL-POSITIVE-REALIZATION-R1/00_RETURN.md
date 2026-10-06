# PYAT HQ221 — C5/N5 GT2 STRUCTURAL POSITIVE REALIZATION — R1 RETURN

**DISPOSITION:** `C5_GT2_STRUCTURAL_POSITIVE_REALIZATION_BLOCKED_BY_EXISTING_AUTHORITY_OR_CONSUMER_CONTRACT`

**BRANCH:** `agent/rabochii-pyat-hq221-c5-gt2-structural-positive-realization-r1`
**COURT:** `rawlsing_next/tests/test_pre553_gt2_structural_positive_realization_court.py` — **40 passed, 0 failed**
**REGRESSION:** 7 related existing modules — **168 passed, 0 failed**
**PRODUCTION MUTATION:** **none**. No owner was rewritten. No bounded adapter was needed.

---

## 1. Disposition scope — read this first

The **positive realization is real and complete through V554**, and is consumed by a
current authorized downstream structural consumer.

The **BLOCKED scope is exactly one commissioned step**: step 9, *the V555 atomic route
consuming the structural-use result*. That step is blocked by an **existing frozen
downstream consumer contract**, not by anything missing or broken in this lane.

This is a partial positive realization, not a refusal. Per HQD-216 it is classified as a
`DEVELOPMENT_BLOCKER` (missing consumer contract) — **not** `SOURCE_INTRINSIC_NONAPPLICABILITY`,
and the V555 refusal was **not** used to argue the source never needed the product.

---

## 2. What was consumed

The real retained governed GT2 canary, recovered **source-free** from the fixed committed
Worker-A repo transport by the existing accepted owner
`rawlsing_next/pre553_repo_native_current_payload.py`:

| | |
|---|---|
| source family / wave | Afrobarometer / R5 |
| `EmpiricalQuerySpec` | `sha256:e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0` |
| `EmpiricalFact` | `sha256:540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46` |
| predicate / replay | `sha256:bd91b405…59cea3` / `sha256:c0c23ca2…33c884f` |
| risk set | `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1` (`sha256:0484fa5c…11313b`) |
| retained rows | **19,210** (risk set, denominator and denominator members all exact) |
| typed state | `SUPPORTED`, RAW, SINGLE_UNIVERSE, unweighted |
| roles | Q86B **CONDITIONER** ordinal 0 → Q86A **TARGET** ordinal 1, `SEMANTIC_ORDERED` |
| closure | 76,843 provenance refs, 76,846 dependency refs, 5 producer authorities |

`pyreadstat` is **not installed** in this environment, so the raw `.sav` is provably
untouched on this path. The raw SAV was never reopened or materialized.

---

## 3. The positive chain, step by step

| # | Commissioned step | Result |
|---|---|---|
| 1 | recover exact GT2 fact/query identity | **DONE** — exact current R1C, not the historical A3 triple |
| 2 | produce the actor-independent conditional-support relation | **DONE** — `SUPPORTED` |
| 3 | preserve full joint/count/authority/permission structure | **DONE** — nothing discarded |
| 4 | feed the relation into `wave1_ff_prev3_relation_admission.py` | **DONE** — lossless GT12-C→GT12-D bridge |
| 5 | positive admission for exactly `STRUCTURAL_MEDIATION_INPUT` | **DONE** — `ADMITTED` |
| 6 | bind to the exact direct V554 basis, no invented V553 temporal meaning | **DONE** — SIG-004, `NO_NEW_V553_TEMPORAL_MEANING_REQUIRED` |
| 7 | V554 yields the positive F1/B1/F2 surface | **DONE** — `ELIGIBLE`, F1 + B1 emitted |
| 8 | feed the V554 result into `m2_v555_atomic_route.py` | **DONE** — invoked with a complete, authority-correct request |
| 9 | prove V555 can consume the structural-use result | **BLOCKED** — `M1 contract id mismatch` |
| 10 | record the exact downstream product or narrowest lawful positive object | **DONE** — current V554/V557/V558 `CONTEXT` publication, `RESOLUTION_COMPLETE` |

### Step 2 — the positive relation
`EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`
`1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19`, `typed_state = SUPPORTED`.

**Actual retained geometry — 6 × 6 = 36 native cells, no collapse:**

| Q86B ↓ / Q86A → | 0 | 1 | DK | NOT_ASKED | REFUSAL | MISSING | denominator |
|---|---|---|---|---|---|---|---|
| **0** | 2112 | 4493 | 178 | 0 | 0 | 1 | 6784 |
| **1** | 491 | 11232 | 63 | 0 | 0 | 1 | 11787 |
| **DK** | 40 | 250 | **334** | 0 | 0 | 0 | 624 |
| **NOT_ASKED** | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **REFUSAL** | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **MISSING** | 0 | 9 | 0 | 0 | 0 | **6** | 15 |

Sum = **19,210** = the frozen denominator. The minority `DK` stratum, the rare
`DK×DK` and `MISSING×MISSING` cells, and the **all-zero `NOT_ASKED` / `REFUSAL` strata**
are all retained. Nothing was dropped, averaged, weighted, or turned into a ratio.

### Steps 5–7 — admission and V554
- Admission: `PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0`, `ADMITTED`,
  rule `FIELD_FORGE_RELATION_ADMISSION_RULE@1.0.0`,
  authority `GT2_FF_PREV3_RELATION_ADMISSION_AUTHORITY@R1`, target use **exactly**
  `STRUCTURAL_MEDIATION_INPUT`, contract
  `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`. Deterministic replay verified.
- V554: **ELIGIBLE**,
  F1 `urn:rawlsing:v554:f1:sha256:e458a03bc9c866814c5b4e3e8e1b571c1353c628aae23959a36dc0129b7f00b3`,
  B1 `urn:rawlsing:v554:b1:sha256:afa796ab3520bdfc1bfd21dcb36de992f3eeb2d6ec4136fc423374b1e567d9f9`,
  `B1.allowed_v555_structural_use = true`, `V554_TO_V557_DIRECT` handoff emitted.
  F2 count is 0 at this grain because no condition rows were declared — F1 and B1 are present.

---

## 4. Step 9 — the exact V555 gap (this is the return HQ needs)

**Result:** `CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE` / `"M1 contract id mismatch"`.
No route, no canonical route identity, no F1 ref.

**This is a real existing consumer contract gap, not an implementation gap in this lane.**

- `m2_v555_atomic_route.py` admits only the empirical/temporal M1 contract
  `M1_TEMPORAL_V554_INGRESS_SEAM@1.0.0` — hard checks at lines **113** and **173**.
- The relation basis legitimately carries
  `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`.
- M2 contains **no relation lane, no relation basis kind, and no import** of the relation contract.
- The relation path is *forbidden* from impersonating the empirical lane:
  `m1_admitted_field_forge_relation_v554_ingress.py` blocks
  `structural_empirical_admission_id` and the `v553_*` keys outright.

**Discriminating control proof.** Relabelling **only** the contract id — same positive
F1/B1, same complete authority-correct route request — yields
`ROUTE_CANDIDATE_AUTHORIZED`. So M2 is not globally broken, the block is exactly the
contract-identity seam, and the refusal is presemantic rather than a structural negative.

**Why it was not repaired here.** Closing it means adding an accepted
`ADMITTED_FIELD_FORGE_RELATION` basis kind with its own route authority row to a frozen
downstream owner that this commission explicitly forbids mutating. Per the commission, the
gap is returned rather than edited.

**Worth HQ's attention:** the adopted GT2 lane currently declares
`FORBIDDEN_PRODUCER_FAMILIES = {V553, V555, V556}`. V555 is excluded from this lane *by
current adopted authority*. So admitting this basis at V555 would be an **authority
decision**, not merely a code change.

---

## 5. Step 10 — the narrowest lawful positive current object

Because no V555 route exists, the narrowest lawful positive current object actually
authorized is the current adopted **V554 → V557 → V558** descent, reached through the
existing public entry `run_current_r1c_e2b_actual_objects(query, fact)` on the real
retained objects:

- producer family **V554**, source stage `M1_RELATION_V554_TO_V557`, semantic class `F1`
- V557 decision `ALLOW_CONTEXT_ONLY`, allowed uses exactly `("CONTEXT",)`
- V558 resolution **`RESOLUTION_COMPLETE`**, resolver uses `("CONTEXT",)`
- exact admission ref, exact FIELD FORGE relation ref, exact F1 identity and
  `lineage_closure_fingerprint` all survive into the published object
- V3 actor transition: **`DENY_ZERO_EFFECT`**, state fingerprint unchanged

---

## 6. Refused inventions

Nothing causal, temporal, mechanistic, mediational-strength, portable, actor/person,
biographical, or cross-source was asserted anywhere. Verified by hostile witness, not by
assertion:

- the relation's affirmative meaning projection contains no causal/mechanism/temporal/actor token
- the owner disclaimer block is present verbatim
- `RELATION_SEMANTICS` is `EXACT_CONDITIONAL_SUPPORT_COUNT_PROFILE_WITHIN_SCOPE` — no `CAUS`
- the admission owner's own `semantic_ceiling` asserts
  `empirical_fact_created=false`, `structural_empirical_admission_created=false`,
  `m1_basis_created=false`, `actor_inference_allowed=false`
- V553 temporal meaning was not invented; the disposition is
  `NO_NEW_V553_TEMPORAL_MEANING_REQUIRED`

**Author caveat worth recording.** Substring scanning of the *full* semantic projection is
**not** a valid hostile witness at this grain: the projection embeds the owner's own
disclaimer block (which necessarily names the denied terms) and a 76,843-ref opaque
provenance closure whose `repr` is ~19 MB. An early draft of this court matched its own
disclaimer and hung. The court therefore asserts structure directly — exact cell counts,
denominators, integer types, declared field sets — and scans only the affirmative
meaning-bearing fields.

---

## 7. Hostile coverage

26 discriminating witnesses, all passing, covering every case the commission required:
wrong Q86B/Q86A order; altered risk-set identity **and** row count; altered source
family/wave **and** artifact identity; incomplete joint domain; stale/mismatched fact-query
ref; relation content-hash mismatch; widened permission ceiling; missing admission
authority; missing upstream relation authority; wrong-target-use admission; V554
equivalence-key mismatch; V554 use denied; fabricated positive preparation; nonpositive
upstream across all 11 nonpositive producer states; correlation→causality; actor/person
injection; V3 promotion; V555 route authority missing and out-of-tranche rule; raw-source
reopening; self-adoption.

---

## 8. Truthful discrepancies

1. **Tip.** The commission text names `EXACT STARTUP TIP b00acd92a…`, which is the **parent**
   of the launch tip `b8d056893…`. `b8d056893` is the commit that *adds* `00_COMMISSION.md`.
   The worktree was established at the launch tip so the commission document is present.
2. **Sparse checkout.** The commission says `CHECKOUT: SPARSE_REQUIRED` but supplied no
   prepared worktree path. Per the sparse worktree execution law a worker may not infer
   clone authorization, so a worktree was added from the **shared canonical object store**
   (no clone, no fetch-all). Scope was not narrowed further because the retained empirical
   transport lives inside the working tree and must be read for this lane.
3. **Environment.** No governed environment was named by this commission. An existing local
   stdlib-only pytest venv was used. All four chain owners and their dependencies are pure
   standard library, and `pyreadstat` is absent, so this is **not** governed certification
   evidence — it is reproduced-execution evidence with exact interpreter provenance.

---

## 9. Artifacts

```
WORKER_RETURNS/PYAT-HQ221-C5-GT2-STRUCTURAL-POSITIVE-REALIZATION-R1/
  00_RETURN.md
  01_RETAINED_EMPIRICAL_INPUT_BINDING.json
  02_FIELD_FORGE_POSITIVE_RELATION.json
  03_PREV3_ADMISSION_AND_V554_CONSUMPTION.json
  04_V555_CONSUMER_AND_INFORMATION_CONSERVATION.json
  05_HOSTILE_CASES_AND_PRODUCTIVE_ADEQUACY.json
  06_FINAL_DISPOSITION.json
rawlsing_next/tests/test_pre553_gt2_structural_positive_realization_court.py
```

**Terminal:** `HQ221_C5_GT2_STRUCTURAL_POSITIVE_REALIZATION_RETURNED__HQ_DECISION_REQUIRED`