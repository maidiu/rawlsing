# HQ253 — T0 rich C1 → authenticated F8 existing-API discriminator

**T0 DISPOSITION: `EXISTING_APIS_SUFFICE_FOR_T0; T1_CUSTODY_NOT_PROVED`**
(equivalently: T0 `EXISTING_API_COMPATIBILITY` **achieved**, with the expected custody
counterexample **confirmed**)

This is **T0 mechanical compatibility only**. It is **not** T1 serving adoption.

**BRANCH:** `agent/space-bunny-pyat-hq253-t0-c1-authf8-existing-api-discriminator-r1`
**SEALED COMMISSION TIP (verified against remote):** `8d61676670506a85ad2e7fabc425c1cb46291e47` ✅ exact match
**PRODUCTION EDITS:** **none**

---

## 1. Sealed HQ253 verified first, as instructed

The remote branch `refs/heads/agent/space-bunny-pyat-hq253-t0-c1-authf8-…` resolved to exactly
`8d61676670506a85ad2e7fabc425c1cb46291e47`. Verified before any work. Parent sealed control
`a0a1a0eb2ea1243c2a7341c2b85f22ec1d979a0e` and semantic PRE-MAIN `1f47063c3…` both present.

Unlike HQ221/HQ222, this commission named its **own tip exactly** — no parent/child discrepancy.

**The R01 oracle input was absent from the sealed tip.** It lives on its own commissioned ref
`agent/reviewer-pyat-hq251-s01-t1-use-and-c1-f8-ingress-r1 @ 762cda8ce5b2d9f67b0870f6474df4468ca91630`,
as does the S01 receipt at `b3f28aad418150f4cadd54bcf6a6c2ab34a35898`. I fetched **exactly those two
refs** (not a broad fetch) and resolved both to the commissioned SHAs. No input was invented.

**Zero blob drift** between R01's citations and my tip:

| file | R01 cited | at my tip |
|---|---|---|
| `tests/c1_at08_at13_fixture.py` | `0393cc8c…` | `0393cc8c…` ✅ |
| `pre553_service_f8_source_scope_binding.py` | `4ba00b8e…` | `4ba00b8e…` ✅ |
| `source_backed_positioned_subject_possibility.py` | `62e5eced…` | `62e5eced…` ✅ |
| `tests/test_pre553_analytical_composition_higher_order.py` | `c8a83d3d…` | `c8a83d3d…` ✅ |

## 2. Machine / runtime verified before any test

macOS 13.7.8 x86_64 · Python **3.11.3** (`/usr/local/bin/python3`) · pytest **9.1.1** in a
pre-existing local venv. `pyarrow`, `pandas`, `pyreadstat`, `numpy` all **absent** — which is
itself confirmation that no raw survey, Library, or native path is reachable here. All four target
owners are pure standard library. No governed environment was named by this commission, so this
is **reproduced-execution evidence, not governed certification**.

## 3. Banked commands and exits

| # | command | exit | result |
|---|---|---|---|
| 1 | `PYTHONPATH=. /private/tmp/hq210venv/bin/python -m pytest rawlsing_next/tests/test_pre553_scoped_rich_c1_f8_existing_api_discriminator.py -q -p no:cacheprovider` | **0** | **25 passed** |
| 2 | same runner over the 5 directly relevant unchanged courts | **0** | **234 passed** |
| 3 | `-k "analytical_composition or applicability or f8 or empirical_possibility or c1_at08 or higher_order"` | 1 | **357 passed**, 9 pre-existing collection errors |

Per-file (command 2): F8 source-scope binding court **73**, F8 binding authentication court **25**,
F8 binding repair court **41**, AT09/10/11 higher-order court **35**, source-applicability court **60**.

The 9 collection errors are **pre-existing and unrelated** — missing `pandas`, missing `pyarrow`,
and one missing unrelated harness module. None import anything this lane touches. Same class
observed independently in HQ222 and HQ248.

## 4. Frozen oracle, pinned before any candidate

From the frozen `XOR_ORACLE` literal, pinned as literals in the court:

| quantity | frozen external value | ACTUAL observed |
|---|---|---|
| Q1 `q(C \| A=1)` | `(1, 2)` → cells 1/2, 1/2 | ✅ `[(0,1,[1,2]), (1,1,[1,2])]`, denom 2 |
| Q2 `q(C \| A=1,B=0)` | `(1, 1)` → cells 0, 1 | ✅ `[(0,0,[0,1]), (1,1,[1,1])]`, denom 1 |

**Anti-vacuity holds:** Q1 is flat and Q2 is decisive, so the two are not interchangeable. Q1/Q2
have **distinct** `producer_predicate_ref`, `producer_query_ref`, `producer_fact_ref`,
`consumer_query_ref`, `condition_binding_witness`, `composed_result_identity_hash`, and
**distinct denominators (2 vs 1)** — the `q(A,B)` intersection is read directly, never multiplied
from marginals.

## 5. T0 positive result — existing APIs, zero production edits

One shared source; one applicability-owner receipt (`ADMITTED`, coverage `COMPLETE`); one
`SINGLE_SOURCE_VALIDATION` binding; **one** call to `evaluate_bound_positioned_subject_possibility`
with the **actual owner-produced** `composition.possibility_slice_evidence_or_null`:

- `EXACT_SUPPORTED` / `SUPPORTED` / `EXACT_POSITIONED_STRATUM_SUPPORTED`
- `out.material() == direct_C1.material()` — complete material equality
- `out.result_hash == direct_C1.result_hash`
- `exact_evidence_ref` and `exact_geometry` match the owner evidence

`requested_currentness_claim = None` throughout → `currentness_result = CURRENTNESS_NOT_REQUESTED`.
**No CURRENT is fabricated and no B5/M5 CURRENT proof is claimed.**

## 6. The indispensable hostile — R01's prediction CONFIRMED

Replacing **only** `provenance_refs` (holding `evidence_ref`, geometry, support, state, release,
target and conditioners constant, each asserted):

> **`EXACT_SUPPORTED`, `result_hash` unchanged, `material()` unchanged.**

The same holds when `authority_refs` are replaced as well. **R01's static prediction is confirmed
empirically.**

**This is not an F8 vulnerability finding.** It is the narrow adopted contract behaving exactly as
inspected: `PositionedSubjectPossibilityResult.material()` does not include slice `provenance_refs`
or `authority_refs`. What it *does* prove is exactly what R01 said it would:

> **Mathematical parity with the direct C1 F8 result is NOT proof of producer custody.**

**Controls that keep this honest** — the gap is narrow, not total:
- replacing `evidence_ref` **changes** `result_hash` ✅
- replacing `geometry` **changes** `material()` ✅

## 7. A SECOND independent finding, discovered here and banked unfixed

The binding may declare `bound_target_use_permission_refs` that **contradict the receipt's own
`request_key.target_use_permission_refs`**. Bind succeeds, evaluate succeeds, `result_hash` is
identical to baseline.

Root cause observed at `pre553_service_f8_source_scope_binding.py:881`: the binder *copies*
`request.bound_target_use_permission_refs` into the binding and **never compares it** to the receipt
request key. Distinct from the provenance case — this is a permission-**identity** divergence
between receipt and binding.

**No production edit was made.** It is banked as observed counterevidence for the independent
reviewer and for any future T1 ingress design.

## 8. Which boundary rejects what

| attack | rejected by | code |
|---|---|---|
| swapped release | HQ217 authn | `BINDING_RELEASE_GRAIN_MISMATCH` |
| non-admitted requested source | HQ217 authn | `REQUESTED_SOURCE_NOT_ADMITTED` |
| substituted service id | HQ217 authn | `BINDING_SERVICE_GRAIN_MISMATCH` |
| substituted request identity | HQ217 authn | `BINDING_REQUEST_RECEIPT_GRAIN_MISMATCH` |
| non-admitted source at applicability | SA owner | absent from `admissible_source_universe_refs()` |
| **C1 producer identity substitution** | **nothing** — not authenticated | — |
| **binding/receipt permission divergence** | **nothing** — not compared | line 881 |
| **evidence provenance/authority substitution** | **nothing** — not in result | — |

## 9. Grade separation — what is deliberately NOT claimed

AT09/10/11 are re-used **read-only** (a witness asserts those three test functions still exist and
this court does not restate their claims). Q1/Q2 alone prove the exact joint conditioning on **this
XOR fixture**; they do **not** prove universal minority enumeration, depth-two recursion, or complete
branch coverage. No negative C1 state is forged as a measured artifact; negative outcomes stay under
their owner-native C1-03A/route grain. GT2 is not imported. No actor/V3, no native/issuer work, no
raw survey, no EE14 grant, no T1 adoption.

**Terminal:** `HQ253_T0_RICH_C1_AUTHENTICATED_F8_DISCRIMINATOR_RETURNED_FOR_INDEPENDENT_REVIEW__NOT_T1_ADOPTED`