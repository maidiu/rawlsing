# HQ280 PV3 A04R — consumer reality and provenance holds

## 1. Consumer reality — `CONSUMER_MODELLED_NOT_EXECUTED`

A04's report claims actual C11/I03/I05/batch **6/6** with **modeled** required-consumer receipts. On this source-free terrain I could not locate a runnable real **C1 / Field Forge** downstream consumer that A04's outputs are fed into. I therefore grade consumer closure as:

**`CONSUMER_MODELLED_NOT_EXECUTED`** — a *declared* consumer obligation, not an executed one.

- I do **not** fabricate a consumer positive, and I do not accept a declared expectation as a satisfied consumer.
- The **exact owner** for the missing step is the existing **C1 analytic composition / Field Forge relation-admission** path (as exercised in the F8E/F8F source-free C1→M2 chain).
- The **minimal future act** is a narrowly scoped **B02** commission: bind one already-qualified source-free product to one real consumer and persist the consumer receipt — no new planner, no new engine.
- The **counting rule** matters: consumer satisfaction must be a **first-class required set** keyed by `(expected_work_key, consumer)`, exactly as A05 models it. A04's practice of folding `consumer` into the expected-work preimage makes consumer absence change the *key* rather than producing a distinct missing-consumer failure — so a consumer can be absent while the key set still looks self-consistent. Product and job counts cannot substitute for consumer accounting.

## 2. Provenance — `FREEZE_ENFORCEMENT_NOT_INDEPENDENTLY_PROVABLE_BY_HASH`

The commission asks me to test whether `EXPECTED_SET_OUTPUT_DERIVED` is a genuine provenance constraint. It is **not**; it is a **hash-divergence detector**.

| test | outcome |
|---|---|
| manifest declares its expectation as derived | fires `EXPECTED_SET_OUTPUT_DERIVED` — a *declaration* check |
| manifest omits a frozen key | fires `EXPECTED_OPERATION_OMITTED` — a *set* check |
| **post-result cloned expectation that reproduces the frozen hash** | **indistinguishable.** Hash comparison cannot separate "frozen first, then executed" from "executed first, then cloned to match" |
| same-hash-scope typed corruption (e.g. a wrong `null_source` under a correct key) | caught only because the *typed rule* checks it, not because of hashing |
| forged expected custodian | not detectable by hash at all; requires an external issuer |

**Conclusion:** a hash proves *what* an expectation contains, never *when* it was frozen or *who* froze it. Only an externally sealed, independently timestamped pre-run freeze closes this. This is the same conclusion recorded in the A05 return and in the WVF chronology finding (where the WVS7 truth oracle was assembled *after* the I05 run and the gate order — not a hash — was the decisive evidence).

**`FREEZE_ENFORCEMENT_NOT_INDEPENDENTLY_PROVABLE_BY_HASH`** — a hold, not a defect in A05.

## 3. Holds that remain separate

1. **A04↔A05 join** — `SCHEMA_VERSIONED_SUCCESSOR_REQUIRED` (see `01_…`). Not a string-coercion problem.
2. **A05 expressiveness gap** — cannot represent `measure_kind` or `condition_order`; a successor must carry them.
3. **Consumer closure** — modelled, not executed (§1).
4. **Freeze provenance** — not provable by hash (§2).
5. Competent producer issuer · operative **G0b** · **EE12** · world/**V3** actor · canonical adoption · any all-35 eligible frontier — **none granted or implied**.

## 4. Bounded technical grade

Both artefacts are **individually sound** at development/source-free scope: A04 passes 41/41 of its own tests and distinguishes operation classes A05 cannot; A05 passes its 18 independent adversarial fixtures. The **defect is strictly in the join**, and it is fully specified and reversible by a versioned successor mapping. No canonical, owner, scientific or operative state is changed by this review.

**Terminal:** `HQ280_PV3_A04R_INDEPENDENT_BINDER_ORACLE_OWNER_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`.
