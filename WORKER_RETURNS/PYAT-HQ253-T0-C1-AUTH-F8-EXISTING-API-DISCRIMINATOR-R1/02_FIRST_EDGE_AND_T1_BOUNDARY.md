# HQ253 — first-edge reachability and the exact T1 boundary

**Verdict: zero-production-edit T0 reachability is PROVED.** The full positive path ran to
completion against adopted existing APIs only.

---

## 1. The exact first edge that was reachable

Every stage below is an already-adopted public API. No adapter, shim, wrapper or speculative
terrain was created, and no production file was touched.

| stage | adopted owner | call | outcome |
|---|---|---|---|
| 1 | `tests/c1_at08_at13_fixture.py` | `fx.direct_condition_composition(...)` | `analytical_state=SUPPORTED`, `consumer_result=EXACT_SUPPORTED`, evidence non-null |
| 2 | `pre553_service_source_applicability.py` | `SA.resolve_service_source_applicability(...)` | `ADMISSIBLE_SOURCE_INDEXED_SET`, per-source `ADMITTED`, coverage `COMPLETE` |
| 3 | `pre553_service_f8_source_scope_binding.py` | `B.bind_service_applicability_to_f8_scope(...)` | `SINGLE_SOURCE_VALIDATION`, coverage `COMPLETE` |
| 4 | `pre553_service_f8_source_scope_binding.py` | `B.evaluate_bound_positioned_subject_possibility(...)` | `EXACT_SUPPORTED`, material **and** `result_hash` identical to direct C1 |

**There was no first-edge API error.** The exact failure branch R01 anticipated
(`EXACT_API_INTEGRATION_DEFECT`) did **not** occur, so the requested-minimal-future-owner-terrain
clause is not triggered.

## 2. What T0 success does and does not establish

**Establishes:** `EXISTING_APIS_SUFFICE_FOR_T0`. A real rich source-free C1 producer product can be
handed to the existing authenticated source-scope F8 API using a real applicability-owner receipt
and fixture-only target-use authority, and F8 reproduces the direct C1 result exactly.

**Does NOT establish, and is not claimed:**

- T1 serving adoption or any EE14 model-use grant
- producer custody, provenance custody, or lineage attestation
- N9 / OC05 current or as-of anything (no CURRENT is fabricated; `CURRENTNESS_NOT_REQUESTED`)
- empirical source occupancy
- V3 or actor authority

The receipt used here is a positive test of an **adopted owner function given test data**. It is
**not** an EE14 service-use receipt.

## 3. The exact EE14 T1 model-use and producer-custody gap

Three distinct, observed gaps sit between this T0 result and any lawful T1 service. They are
stated as *gaps*, not as proposals to enlarge any contract.

### 3.1 Producer-custody gap (R01's finding, confirmed)

`PositionedSubjectPossibilityResult.material()` does not carry the slice's `provenance_refs` or
`authority_refs`. Consequently two evidences with **identical** `evidence_ref` and geometry but
**different** provenance custody produce the **same `result_hash`**.

Therefore equality with the direct C1 F8 result — which is exactly what T0 asserts — is a **false
positive** for producer provenance. A T1 ingress that selects C1 evidence **by parity** would be
unsound.

**What T1 would need** (for a future commission, not authorised here): a serving ingress that
selects the genuine C1 `AnalyticalCompositionResult` and evidence **by producer-owned
replay/custody**, verifying `composed_result_identity_hash` plus fact/query/predicate/witness/
paired-value/recursive-ancestry closure. On that new trusted ingress the mutated-provenance
evidence **must** be rejected or replaced by recomputed owner evidence.

**Explicitly not demanded:** the standalone binder must not be made to refuse this. That would
silently enlarge its adopted contract, which R01 forbids and which this worker did not do.

### 3.2 Producer-identity gap

F8 authenticates the **applicability receipt grain**, not C1 producer identity. Substituting a
different *supported* C1 product changes the result **honestly**, with no refusal. Nothing in the
current chain binds F8 to C1's `producer_predicate_ref` / `producer_query_ref` / `producer_fact_ref`
/ `condition_binding_witness` / `composed_result_identity_hash`. Those live only in the separate C1
envelope, which the court asserts is **not** present in F8's result material.

### 3.3 Target-use permission identity gap (independently found here)

The binding's `bound_target_use_permission_refs` is copied straight from the binding request
(`pre553_service_f8_source_scope_binding.py:881`) and is **never compared** to the receipt's
`request_key.target_use_permission_refs`. A binding may therefore declare permissions that
contradict the receipt, bind successfully, and evaluate to the identical `result_hash`.

This is a **second, independent** custody gap: it concerns permission *identity* rather than
evidence provenance. Banked unfixed; it is a genuine input to any future T1 ingress design.

## 4. Minimal requested owner terrain

**None for T0.** T0 succeeded with zero production edits, so no bounded future owner terrain is
requested at this grain. If HQ later commissions T1, the terrain implied by these findings is a
**new serving-ingress owner** (EE14 side) plus a **producer-custody attestation** step — neither of
which exists today, and neither of which is created, stubbed, or foreshadowed here.

## 5. Grade separation maintained

AT09/10/11 coverage is reused **read-only**. Q1/Q2 prove the exact joint conditioning on this XOR
fixture only. Negative C1 states are reported at their owner-native C1-03A/route grain; no
synthetic `VALID_EMPTY` or `UNDERPOWERED` artifact was injected. GT2 was not imported. No native
P07/AT07 activation occurred.
