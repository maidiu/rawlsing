# PYAT R3 S05 — Original work → durable consumer: composition result

**TERMINAL:** `PYAT_R3_S05_ORIGINAL_WORK_CONSUMER_BOUNDED_HOLD__GITHUB_PUSHED`
**DISPOSITION:** `EXACT_HOLD__NAMED_MACHINERY_IS_NOT_ON_THE_IMPLEMENTATION_BASE__COMPOSITION_NOT_CONSTRUCTIBLE`
**Branch:** `agent/rabochii-pyat-r3-s05-original-work-consumer-r1` (created from implementation base `7f29aec36d24f16da52d84f17c00f08db3a55434`)

## 1. What I did, and why this is a hold rather than a pipeline

The mission asks me to **compose already-implemented machinery** into one no-drop durable source→consumer route, on the implementation base. Before writing any composition I established, **by import rather than by prose**, which of the named components actually exist there. Result (`repro/s05_composition_probe.py`, `repro/probe.json`, exit 0):

| component | module | state |
|---|---|---|
| C11 release | `pre553_c11_repository` | **PRESENT / importable** |
| C11 integrity | `pre553_c11_integrity` | **PRESENT / importable** |
| Route B | `pre553_source_backed_c11_facade` | **PRESENT / importable** |
| empirical query | `pre553_empirical_query` | **PRESENT / importable** |
| discovery (exact) | `pre553_discovery_exact` | **PRESENT / importable** |
| batch runner | `pre553_batch_runner` | **PRESENT / importable** |
| analytical composition | `pre553_analytical_composition` | **PRESENT / importable** |
| Field Forge | `field_forge_conditional_support` | **PRESENT / importable** |
| learned product (M2) | `pre553_learned_product_release` | **PRESENT / importable** |
| **V2 verifier / E contract** | `pre553_original_workload_v2_verifier_candidate` | **ABSENT** |
| **V2 contract** | `pre553_original_workload_contract_v2_candidate` | **ABSENT** |
| **governed batch integration** | `pre553_governed_batch_checkpoint_integration_candidate` | **ABSENT** |
| **durable checkpoint** | `pre553_batch_durable_checkpoint_candidate` | **ABSENT** |
| **separate principal / issuer** | `pre553_b5_separate_principal_verifier_candidate` | **ABSENT** |

`composition_possible_on_base: **false**`.

## 2. Why the composition cannot be built here

The machinery the mission names as "already implemented" is **not on the implementation base**. Each missing component exists only on an **unmerged worker branch**, verified by direct tree inspection:

| component | exists on | absent from base |
|---|---|---|
| V2 verifier / E contract | `c1df9842b7531146f1d8e215f216915b9039e4d7` (A04T) | yes |
| V2 contract | `56574bec2176df7fc95d4b877dfab79469de9c03` (A04S) | yes |
| governed batch integration | `92cb25340c49fb51e2b8d6e00d5a4f471296fc8f` (B01E) | yes |
| durable checkpoint (fail-closed) | `ef93f014a157983e0f713c118ee3a95311c16292` (B01D) | yes |
| separate principal / issuer | `82309fe17c70324217382d0550ce1cc591e39eae` (C02H) | yes |

I proved the same disjointness in R02: B01E's tree lacks the V2 verifier and A04TU's tree lacks even B01E's durable dependency. **No accepted tree carries the E-custody contract together with the durable batch layer**, so the instruction "compose the already implemented machinery" has no lawful subject matter on the base. I did **not** invent a merged tree, and I did **not** fabricate a green run — the mission itself forbids representing a fixture as genuine issuance.

## 3. What IS implemented and verified (bounded product)

- The base **spine is real and importable**: C11 release + integrity, Route B, empirical query, exact discovery, batch runner, analytical composition, Field Forge, learned-product release (9/9 present).
- `rawlsing_next/tests/test_pre553_batch_runner.py` executed: see `repro/base_batch_runner_suite.log`. This is the base's actual batch machinery, reported at its own grade.
- The **composition probe is reusable**: any future lane can re-run `repro/s05_composition_probe.py` to re-establish presence/absence in one command.

## 4. The exact owner-level missing joins (the real deliverable)

1. **`E`-custody owner is unmerged.** Nothing on the base can independently freeze expected work; the V2 verifier/contract exist only on A04T/A04S. **Required:** an accepted integration commit that lands the V2 verifier **on the base lineage**, or an explicit HQ adoption of that branch tip as the E-custody owner.
2. **Durable batch owner is unmerged.** Nothing on the base can durably checkpoint or resume a batch; B01D/B01E exist only on their own branches. **Required:** the durable layer landed on the base lineage (or adopted), *and* verified to be the B01D `RERUN_SAFE`-fail-closed revision — I confirmed in B01DR that the pre-repair version would have permitted duplicate execution via a forged idempotence claim.
3. **No owner binds E to D.** Even with both landed, no existing module performs the outer reconciliation `U → E → D → execution → R → A → C`. This is the one **genuinely new** connection the mission asks for, and it is small: an audit-only adapter that (a) takes an externally frozen E, (b) checks D ⊇ E as a **set**, (c) refuses `E \ D` omissions and `D \ E` extras, (d) requires consumer obligations as an independent set. I have already built and adversarially verified exactly this contract shape in A05 (`9491d029…`) and PV3 A05 (`9491d02…`); it should be **adopted**, not rewritten.
4. **Issuer/principal owner is a demo.** C02H's fixed toy key (`n=3233, d=2753`) and caller-supplied trust root are not a boundary — I forged an accepted credential against them in C02HR. Any route requiring authenticated expectations needs a real principal first.

## 5. What still prevents the first lawful real-source run

In dependency order: **(1)** an accepted integration of the E-custody and durable-batch owners onto one lineage; **(2)** the small E→D outer-reconciliation adapter (existing design, reusable); **(3)** a competent **source/design/operation warrant** — no fresh protected source read is authorised by this return; **(4)** a **real** issuer principal for authenticated expectations (the demo key is not one); **(5)** an independent **E_pre custodian** sealing the expected set before execution — without it, "frozen before" is indistinguishable from "reconstructed after", as I established in WVF, A04SR and A04TR.

## 6. Minimal repair proposal — only after a concrete failing owner connection

I am **not** proposing a new planner. The smallest repair is the missing **join**, and it is one adapter, justified by the concrete failure I can name: *the base cannot import any E-custody or durable-batch owner at all* (`ModuleNotFoundError`, `repro/probe.json`). The repair is: land the two owners on one lineage, then adopt the existing outer-reconciliation contract. **No new universal planner is warranted**, which is exactly what the mission asked me to test.

## 7. Boundaries honoured

**Zero candidate code changes. Zero accepted-owner edits. No raw SAV/DTA. No source read. No source/design/operation warrant claimed. No canonical/PRE-MAIN mutation. No self-adoption.** 35 waves / 63 temporal syntactic pairs and every HELD/DENIED/NA untouched.

**Terminal:** `PYAT_R3_S05_ORIGINAL_WORK_CONSUMER_BOUNDED_HOLD__GITHUB_PUSHED`.
