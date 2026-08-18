# 05 — Decision Protocol Before Any Recalibration

**Status:** `BINDING_FOR_THIS_CONTROL_BRANCH`

## 1. Change freeze

Until parent synthesis D15 closes, this branch authorizes:

- source inspection;
- historical archaeology;
- current code tracing;
- database/schema audits;
- benchmarks;
- fixtures and tests that do not alter production semantics;
- architecture comparison on paper;
- authority-gap specification.

It does **not** authorize production redesign, deletion, new canonical object families, runtime promotion, or semantic reclassification.

## 2. Evidence precedence

When claims conflict, use this order:

1. explicit accepted current authority / governing law;
2. current production code and populated-data behavior as evidence of implementation, not semantic authority;
3. accepted frozen court rulings within their exact base/scope;
4. current schema/data evidence;
5. historical design packs as intent/genealogy evidence;
6. conversation notes and model inference.

Historical intent cannot overrule current accepted law. Current code cannot create semantic authority merely by existing.

## 3. Every court must separate six questions

For any artifact or capability, answer separately:

1. **What information exists in the source world?**
2. **What transformation does current code actually perform?**
3. **What semantic meaning, if any, is governed?**
4. **Who currently consumes it?**
5. **What terminal capability would be starved if it disappeared?**
6. **What is the minimum physical/compute mechanism that can preserve that capability?**

No artifact gets protected because it is old, expensive or interesting. No artifact gets deleted because its present consumer is missing. No capability gets promoted because a historical pack once intended it.

## 4. Required disposition vocabulary

Every investigated object/capability must receive one or more of:

- `CANONICAL_SEMANTIC_OBJECT`
- `CANONICAL_EVIDENCE_VIEW`
- `DURABLE_PHYSICAL_AUTHORITY`
- `REGENERABLE_CACHE`
- `DERIVED_VIEW`
- `DISCOVERY_INDEX`
- `DIAGNOSTIC_ON_DEMAND`
- `COMPATIBILITY_ONLY`
- `INTENDED_BUT_UNWIRED`
- `STRANDED_MEANING`
- `SUPERSEDED`
- `RETIRE_CANDIDATE_AFTER_PROOF`
- `MISSING_AUTHORITY`
- `UNKNOWN`

A capability and one of its materialized artifacts may receive different dispositions.

## 5. Required semantic noncollapse checks

Every proposal must preserve:

```text
source evidence
!= empirical distribution
!= empirical association diagnostic
!= structural interpretation
!= structural applicability / mediation possibility
!= generated actor position
!= realized encounter / exposure
!= actor knowledge / belief / memory
!= actor response / action
!= rendered expression
```

And:

```text
population prevalence
!= actor membership

population conditional response
!= actor response propensity

same-person survey cotravel
!= generated-person psyche

historical branch cohort
!= generated biography
```

## 6. Capability-preservation test

Before retiring a current compute family, the synthesis must answer:

- What distinct query or discovery operation does it enable today?
- Is that operation lawful/terminally useful?
- Can the same operation be reconstructed exactly or more lawfully from a deeper retained substrate?
- At what cost and latency?
- Does reconstruction preserve minority cases, contradictory configurations, missingness, weights and provenance?
- Are all current/future authorized consumers able to dereference the replacement?

If any answer is unknown, retirement is premature.

## 7. Historical-genealogy test

Before restoring or preserving an old capability because "Rawlsing always intended it," prove:

- the historical intention actually existed;
- its semantic purpose;
- whether current governing law superseded or transformed that purpose;
- the present lawful jurisdiction where the underlying need belongs;
- a concrete terminal starvation case if omitted.

## 8. Current-main revalidation rule

Any implementation claim from VT3 frozen base must be marked `FROZEN_BASE_CONFIRMED` until reproduced on current main. PR #125 changed authority/runtime loading and may alter eligibility or wiring even when analytic helper code is unchanged.

## 9. Discovery closure gate

Architecture design may begin only when parent Vozhd can answer, with evidence:

1. What exact empirical-discovery capabilities exist now?
2. Which came from V547–V549 and what changed?
3. Which are terminally required under the current whole-machine architecture?
4. Which are merely diagnostics/authoring tools?
5. Which meanings are stranded or unwired?
6. What current authority permits each workload and downstream interpretation?
7. What population→structural ontology seams remain missing?
8. What exact physical substrate guarantees reconstructibility?
9. What actual compute/materialization cost is being paid?
10. What replacement can be proven semantically equivalent or deliberately superior without flattening the human world?

## 10. Final design standard

The eventual recalibration should make the pre-553 machine smaller only by eliminating duplicated computation, redundant materialization, obsolete compatibility surfaces and semantic republishing. It must not make the historical world smaller in order to make the software cleaner.

The final design should preserve enough empirical plurality that V3 receives a differentiated world, while preserving enough jurisdictional distance that V3 still has to generate a life rather than read one out of survey statistics.
