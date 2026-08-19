# D15 — IMPLEMENTATION CAMPAIGN

**Status:** architecture-ready implementation plan; no production code is modified by D15.

The campaign is deliberately split into small cells. A worker owns one semantic seam and its tests, not the whole machine.

## I01 — Target authority contracts and object schemas

**Mission:** implement typed schemas/validators for canonical D15 objects and new authorities without changing current producers.

**Prerequisites:** D15 accepted.

**Permitted code surface:**
- new `data/ddm_build_copy/ddm_empirical_object_model.py`
- new `data/ddm_build_copy/ddm_empirical_authority.py`
- new target authority files under `data/ddm_build_copy/authority/` specifically created for D15 comparator/discovery/query/structural-admission/replay contracts
- tests for these new schemas/authorities.

**Forbidden:** V550/V551/V552 behavior changes; V3 behavior changes; source deletion; generic authority expansion by field-name analogy.

**Outputs:** canonical object dataclasses/schemas; typed absence enum; authority snapshot/content-ID validator; query/discovery/comparator/admission authority contracts.

**Tests:** noncollapse type tests; immutable authority hash/version tests; typed missing/denied states; invalid cross-object coercion rejected.

**Acceptance gate:** G00.

---

## I02 — Concrete C11 empirical evidence repository

**Mission:** implement source-universe-scoped respondent-event/coordinate incidence and M01–M18 semantic manifests beside current storage.

**Prerequisites:** I01.

**Permitted code surface:**
- new `data/ddm_build_copy/ddm_c11_repository.py`
- new `data/ddm_build_copy/ddm_c11_ingest.py`
- new `data/ddm_build_copy/ddm_c11_integrity.py`
- new target schema/migrations dedicated to C11; no destructive changes to current tables
- source-ingest tests/fixtures.

**Forbidden:** scalar duplicate collapse without topology authority; default missing weight=1.0; source-universe merge; replacement/deletion of current shared substrate; current consumer switch.

**Outputs:** concrete C11 storage/API; semantic manifests; append-only universe partitioning; exact event/component/rank/routing/weight representation.

**Tests:** D13B P01–P20 synthetic suite; T08–T11 topology/routing/multiplicity; hash projection includes all proof-relevant fields.

**Acceptance gate:** G01.

---

## I03 — Source→C11 equivalence certification

**Mission:** build positive per-source equivalence proof tooling against immutable source/native evidence.

**Prerequisites:** I02 plus exact source artifacts/semantics for tested source.

**Permitted code surface:**
- new `data/ddm_build_copy/ddm_c11_source_equivalence.py`
- validation SQL/scripts/tests only; no source deletion.

**Forbidden:** schema-only certification; count-only certification; treating blocked evidence as pass; source retirement.

**Outputs:** `SOURCE_TO_C11_EQUIVALENCE_CERTIFIED|FAILED|BLOCKED` receipts with proof details.

**Tests:** P01–P20 and T01–T18 against source-native fixture/production-equivalent evidence; native topology/routing/weights/universe lineage.

**Acceptance gate:** G02 per source.

---

## I04 — Exact EmpiricalQueryEngine

**Mission:** implement exact C11 evaluation for D12 future-selectable empirical query frontier.

**Prerequisites:** I01, I02.

**Permitted code surface:**
- new `data/ddm_build_copy/ddm_empirical_query.py`
- new `data/ddm_build_copy/ddm_empirical_predicate.py`
- tests; compatibility readers for current bounded fixtures may be test-only.

**Forbidden:** structural interpretation; actor comparison; independent-marginal approximation of joints; implicit pooling; cache-only execution.

**Outputs:** EmpiricalQuerySpec compiler; exact EmpiricalFact evaluator; typed zero/support/noncomparability outputs.

**Tests:** D12 T01–T16, XOR/parity, arbitrary coordinate conjunction, routing, multiselect/repeat/rank, weights, source-indexed components.

**Acceptance gate:** G03.

---

## I05 — StructuralEmpiricalAdmission and V553 target intake

**Mission:** replace fragmented current empirical→structural packet boundary with explicit admission authority while preserving lawful existing V551/V552 semantics.

**Prerequisites:** I01, I04; accepted current V551/V552 rule inventory.

**Permitted code surface:**
- new `data/ddm_build_copy/ddm_structural_empirical_admission.py`
- target authority files for structural admissions
- narrowly scoped V553 input adapter/version extension in `data/ddm_build_copy/ddm_v553_canonical_harmonization.py` or its accepted successor
- compatibility adapters/tests for V551/V551J/V552/V552J.

**Forbidden:** generic empirical association->structural truth; empirical coordinate->generated structural position; reverse possibility field routing through V553; deletion of current V551/V552 paths before parity.

**Outputs:** StructuralEmpiricalAdmission receipts; compatibility rules for intentionally retained current structural semantics; V553 admitted-evidence intake.

**Tests:** T17; current non-joint/joint structural parity; denial/missing-authority cases; source/time provenance; V553 temporal/comparability regression.

**Acceptance gate:** G04–G05.

---

## I06 — V554–V558 corrected-upstream regression

**Mission:** prove accepted downstream structural contracts survive corrected V553 supply and make only necessary adapter/provenance updates.

**Prerequisites:** I05.

**Permitted code surface:** accepted V554/V555/V556 producer modules and V557/V558 adapters/resolver only where required by new V553 object/provenance version; tests first.

**Forbidden:** reverse possibility field in StructuralPriorRepository; actor state in V554–V558; semantic redesign merely because producer changed; broad downstream rewrite.

**Outputs:** revalidation test report; minimal adapter changes if needed.

**Tests:** all accepted existing V554–V558 fixtures; producer identity/provenance; no reverse-field adapter; deterministic ContextResolver parity.

**Acceptance gate:** G06 and every applicable `V553_PLUS_REVALIDATION_MATRIX.csv` row.

---

## I07 — Autonomous discovery EXACT_BOUNDED

**Mission:** implement complete-for-declared-frontier discovery mode using exact query facts.

**Prerequisites:** I01, I04.

**Permitted code surface:**
- new `data/ddm_build_copy/ddm_empirical_discovery.py`
- new `data/ddm_build_copy/ddm_discovery_replay.py`
- discovery authority definitions/tests.

**Forbidden:** current top-two/primary-star heuristics presented as exhaustive; unbounded semantic search; E4 score as primary evidence; materialize-all requirement.

**Outputs:** deterministic frontier constructor; exhaustive evaluator; DiscoveryResultReceipt/branch receipt; replay trace.

**Tests:** AT01–AT07; unexpected fork; XOR; reversal; rare third category; recursive branch; branch cotravel; valid-empty; order permutation.

**Acceptance gate:** first half of G07.

---

## I08 — Autonomous discovery ADAPTIVE_EXPLORATORY

**Mission:** add lower-cost non-exhaustive search mode with truthful coverage receipts.

**Prerequisites:** I07 exact validation/replay machinery.

**Permitted code surface:** discovery modules from I07 plus isolated proposal/screen/beam strategies.

**Forbidden:** claiming completeness outside evaluated/proven safely covered frontier; cost-only minority erasure; unary screen called XOR-complete.

**Outputs:** adaptive strategy interface; explicit evaluated/pruned frontier receipt; exact validation of emitted results.

**Tests:** compare against exact bounded fixture; prove omitted candidate not reported as absent; screen false-negative fixture; deterministic stopping/replay.

**Acceptance gate:** second half of G07.

---

## I09 — Actor comparability + PositionedSubjectPossibilityService

**Mission:** implement exact actor-fact comparator resolution and source-indexed unary/J-way possibility fields.

**Prerequisites:** I01, I04; objective actor fact owner interfaces; comparator/source-applicability authorities.

**Permitted code surface:**
- new `data/ddm_build_copy/ddm_actor_empirical_comparator.py`
- new `data/ddm_build_copy/ddm_positioned_subject_possibility.py`
- comparator/source-applicability authorities and tests.

**Forbidden:** generated structural position as generic comparator; fuzzy/nearest fallback; source pooling by default; direct actor belief/response assignment.

**Outputs:** ActorComparatorReceipt; PositionedSubjectEmpiricalPossibilityField; source disagreement/typed failures.

**Tests:** AT13–AT16; G08–G09 fixtures including zero support, ambiguity, time mismatch, sparse k-way and multiple universes.

**Acceptance gate:** G08–G09.

---

## I10 — V3 empirical-possibility metabolism boundary

**Mission:** extend V3 input contract with V3EmpiricalPossibilityInput and explicit non-deterministic metabolism authority while preserving existing V3 causal ownership.

**Prerequisites:** I09; accepted V3 implementation ruling/authorities.

**Permitted code surface:** narrowly identified V3 upstream-input/developmental proposal/state-transition modules and new authority; no V2 changes except compile/interface fixtures if required.

**Forbidden:** field mass copied into belief/response probability/state; actor objective comparator implemented from structural position; bypassing opportunity/encounter/exposure/relationships; V3 structural context replacement.

**Outputs:** typed V3 possibility input; metabolism rule interface; causal provenance link from field to later decisions without direct state assignment.

**Tests:** AT16–AT17; same field/same structural context but divergent histories; actor-opacity tests; replay with field + causal history + RNG; no V2 leakage.

**Acceptance gate:** G10.

---

## I11 — Exact cache/materialization layer + telemetry

**Mission:** add optional identity-exact caches only after uncached correctness is closed and instrument W01–W17.

**Prerequisites:** I04; I07; I09 as relevant.

**Permitted code surface:**
- new `data/ddm_build_copy/ddm_empirical_cache.py`
- instrumentation/benchmark code; no semantic producer changes.

**Forbidden:** cache as authority; future-frontier restriction to cached facts; stale-key fallback; source snapshots treated as cache.

**Outputs:** fixed E1/E2, branch-member, comparator, reverse-field, temporal/source component cache interfaces; hit/miss/invalidation telemetry.

**Tests:** AT23; cold=warm; eviction invariance; authority/C11 mutation invalidation; benchmark W01–W17.

**Acceptance gate:** G11.

---

## I12 — Shadow migration and current-path switch readiness

**Mission:** run current and target paths side-by-side, classify differences, and produce per-artifact retirement-readiness receipts without deleting anything.

**Prerequisites:** I02–I11 as applicable; populated/source-equivalent evidence for empirical claims.

**Permitted code surface:** shadow orchestration, comparison tooling, compatibility adapters, deployment flags; current production producers remain intact until switch gates.

**Forbidden:** deleting source/current artifacts; forcing parity to known-defective behavior; claiming savings without measurement; switching a consumer whose replacement parity is unproved.

**Outputs:** current-vs-target semantic parity matrix; runtime W01–W17 measurements where available; artifact retirement-readiness ledger.

**Tests:** G04–G12; full AT01–AT23; negative authority; multi-universe/double-counting; V553+ regression.

**Acceptance gate:** G12 per artifact. A failing artifact remains current/migration-only.

---

## I13 — Source-retirement eligibility audit (separate governance cell)

**Mission:** after all relevant sources have concrete positive source→C11 equivalence, determine whether a source snapshot is technically eligible for later retirement consideration.

**Prerequisites:** I03 positive per-source receipts; legal/operational retention requirements available.

**Permitted code surface:** audit/report tooling only.

**Forbidden:** deletion; treating C11 semantic equivalence as proof that external legal/audit retention is unnecessary.

**Outputs:** `ELIGIBLE_FOR_SEPARATE_SOURCE_RETIREMENT_GOVERNANCE` or blocked reasons.

**Tests:** receipt completeness; immutable authority dereference; disaster replay from retained C11/authority; governance dependencies.

**Acceptance gate:** separate post-D15 governance. This cell never deletes source evidence.

---

# Dependency spine

```text
I01
 └─ I02
     ├─ I03
     └─ I04
         ├─ I05 → I06
         ├─ I07 → I08
         └─ I09 → I10
              └─ I11 (also consumes I07/I04)
                   ↓
                  I12
                   ↓
                  I13 (only after positive source equivalence)
```

I05/I06 structural work and I09/I10 reverse/V3 work are parallel semantic lanes after the query engine. Neither depends on the other to define its ontology.

# Campaign completion condition

The implementation campaign is complete when:

- concrete C11 passes required equivalence tests for migrated sources;
- exact query engine passes D12/D13 fixtures;
- autonomous discovery coverage claims are truthful and replayable;
- reverse field and V3 metabolism boundary pass noncollapse/divergence tests;
- structural admission/V553+ path preserves intended current structural semantics and corrected frontier;
- caches are demonstrably nonauthoritative;
- current artifacts have per-artifact positive retirement-readiness or remain explicitly retained;
- source snapshots remain retained unless separately governed after positive source equivalence.
