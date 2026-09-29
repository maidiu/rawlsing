# PYAT C1-00 — independent contract/oracle review — R1

Disposition: `CHANGES_REQUIRED`

Terminal: `C1_00_INDEPENDENT_REVIEW_COMPLETE`

Reviewed return:
`df6f2d36e274744d217dc4a380c73e2c7e18e83f`

Reviewer commission:
`642e48f26f94fb144ef5e26942ba56fdb7881307`

Implementation baseline:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

This review does **not** implement C1-01, edit production code, access raw survey sources, or create semantic/comparability/model authority.

## 1. Review grain

I read the C1 requirement/oracle and review law before the worker success narrative, then inspected the exact base-to-return diff and the current public owner contracts.

The worker return is cleanly scoped: the compare from original commission `2cef3869c16cbd88ce8bc58a5bd4aa073879be50` to reviewed return `df6f2d36e274744d217dc4a380c73e2c7e18e83f` is eight commits, all eight changed files under:

`WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/**`

No production or existing test-owner file changed.

C1-00 has no candidate implementation to execute. The decision-critical positive oracle was therefore independently recomputed from the frozen synthetic counts, and the decisive hostile cases were checked statically against the exact current public types/functions.

Source reads: **0**.

## 2. What is accepted

The return correctly freezes, at documentary grain:

- exact source-universe + release nonaliasing;
- exact target topology/domain identity and refusal to scalarize later non-scalar work inside C1-01;
- exact risk-set/member/denominator custody;
- RAW versus governed-weighted separation plus weight/design/estimand custody;
- observed-zero versus zero-support/zero-overlap versus valid-empty;
- adaptive explicit unvisited territory and prohibition on global negative inference;
- recursive immediate-parent identity and separation of positive handoff from full discovery coverage;
- replay-grade separation;
- the rule that a failed learned/adjudicated family may not be relabeled DIRECT to evade M1/M2/B5/I4;
- the narrow future write terrain: new C1 analytical module, its new test module, and C1 worker returns only.

The AT07 arithmetic is independently correct:

- P1 denominator = `54 + 6 = 60`; therefore `P(yes | P1) = 54/60 = 9/10`.
- yes denominator = `54 + 8 = 62`; therefore `P(P1 | yes) = 54/62 = 27/31`.

No candidate output was used to derive either value.

## 3. Blocking defect A — exact condition/value relation is not actually proved

Current owner evidence:

- `rawlsing_next/source_backed_positioned_subject_possibility.py`
  blob `62e5eced47b64512f47b004e3e13a6ef3fe21de7`, lines 72–184:
  `ConditionerBinding` carries `binding_id`, `subject_fact_ref`, `empirical_coordinate_ref`, comparability ref, source/release/time, but **no value-bearing subject preimage**.
- Same blob, lines 399–463:
  consumer `_find` keys evidence by source/release/target/`retained_conditioner_ids`.
- Worker `analytical_contract.md`
  blob `2bbac259201c84dfdd124ec26942e95a76dadbe8`, lines 91–107:
  proposed `ConditionValueBindingWitness` hashes the full consumer binding plus producer query/predicate/AST.

That is not enough.

Minimal counterexample:

1. Consumer query Q1 contains `binding_id="position"` and `subject_fact_ref=F_P1`.
2. Producer predicate P2 exactly means `POSITION == P2`.
3. Construct the proposed witness with Q1.ref, Q1's full binding fingerprint, P2 query ref, P2 predicate ref/hash, and canonical P2 AST.
4. Every frozen identity can be recomputed exactly.
5. Nothing in the proposed contract dereferences `F_P1` to a value-bearing preimage or requires that value to equal the exact P2 predicate leaf/value.

The witness therefore proves **exact co-custody of two objects**, not the relation between them. A wrong P1-subject/P2-predicate pairing can receive a perfectly stable hash.

### Required correction

Before C1-01, freeze a per-binding value relation with enough preimage to reject that counterexample. At the synthetic source-free C1-01 grain, this may be fixture-only ground truth; it must not masquerade as real-source comparability authority.

For each conditioner, the corrected contract must make independently checkable:

- the exact full consumer binding;
- an exact value-bearing subject-condition preimage/material, or an already existing resolvable owner for it;
- the exact producer predicate leaf identity;
- the exact predicate semantic ref / coordinate or question ref;
- the exact predicate value/value-set material;
- exact source/release/time scope;
- the fixture-only relation that says those two values are paired;
- a deterministic adapter check that fails before slice construction when they disagree.

Real-source subject↔survey comparability remains typed blocked unless an existing competent owner/authority supplies it. Do **not** create a new production authority kind merely to satisfy this review.

## 4. Blocking defect B — synthetic authorities are named, not frozen

Worker `fixture_oracle_manifest.json`
blob `f666b0ae36a415640e8d4aeb5cf498e2f587ec83`, beginning at line 12, provides `frozen_tags` such as:

- `C1:SYNTHETIC:SOURCE_SEMANTICS`
- `C1:SYNTHETIC:ROUTING_RISK_SET`
- `C1:SYNTHETIC:CONDITION_BINDING`

but does not freeze their complete canonical authority material, governed operations/scopes, versions, or expected identity hashes.

That leaves C1-01 free to change authority semantics while retaining the same tag. The arithmetic oracle is frozen; the governed fixture authority premises are not.

### Required correction

Freeze complete canonical **test-only** authority material and exact expected refs/hashes for every synthetic authority needed by C1-01. Where condition-value pairing has no production authority owner, freeze it as fixture/oracle ground truth rather than inventing a new production authority class.

## 5. Blocking defect C — UNKNOWN is not conserved separately from UNVISITED

The user commission explicitly requires distinct:

`unknown` / `unresolved` / `unvisited`.

The worker's output vocabulary in `analytical_products.json`
blob `2b6386c6d7b490531ca9f5af93e9d99e368ba182`, lines 44–61, includes `EXPLICIT_UNKNOWN_UNVISITED` but no distinct `UNKNOWN`.

The AT14 state matrix likewise includes adaptive unvisited but no independent unknown case.

This is not forced by existing owners. Current B5 already exposes `UNKNOWN_CURRENTNESS`:

- `rawlsing_next/pre553_learned_product_lifecycle.py`
  blob `a11c9eb73abab9be118ef4f0b6e325e676059f27`, lines 33–40;
- same blob, lines 1885–1928, where unresolved selection state raises `UNKNOWN_CURRENTNESS`.

### Required correction

Add an independently frozen UNKNOWN case/state at a competent existing owner path, distinct from:

- adaptive unvisited;
- empirical/query unresolved;
- unavailable;
- no-current;
- conflicting current selection.

For lifecycle-governed families, B5 `UNKNOWN_CURRENTNESS` is an existing lawful witness.

## 6. Blocking defect D — consumer slice projection is still underspecified

Current `PossibilitySliceEvidence` accepts:

- arbitrary `geometry: Mapping[str, Any]`;
- `raw_support: int | None`;

and does not define whether raw support is denominator, resolved-target support, or something else.

Worker `analytical_contract.md` line 120 requires “exact complete-cell geometry with raw counts and authorized exact fractions,” but does not freeze a canonical projection/schema or the meaning of `raw_support`.

That leaves multiple incompatible C1-01 adapters compliant with the prose while producing different consumer evidence.

### Required correction

Freeze one exact C1-01 slice projection before implementation, including:

- canonical geometry schema/keys;
- exact cell material and cell states;
- exact raw numerator support per cell;
- exact raw denominator;
- authorized weighted numerator/denominator when applicable;
- exact fraction representation;
- measure identity;
- the precise meaning of `PossibilitySliceEvidence.raw_support`.

The actual consumer must receive that exact derived projection, not merely have the correct denominator preserved somewhere in the outer envelope.

## 7. Blocking defect E — the condition-binding relation is absent from determinant closure

Worker `analytical_products.json` requires `condition_binding_witness_ref_or_hash`.

But `replay_and_dependency_receipt.json`
blob `f26202b2f8ed24bf8d6b8d06a08c2f7bdb4eb144`, lines 36–53, freezes direct determinants that include:

- full `ConditionerBinding` fingerprint;
- consumer comparability authority refs;

but not the relation/witness ref itself.

Once that witness is the object proving producer predicate ↔ subject condition/value, changing it must change or invalidate the composed product.

### Required correction

Add the exact condition-value relation/witness ref/hash—and any value-bearing subject preimage/ref introduced by the defect-A repair—to:

- direct determinant closure;
- replay identity;
- selective invalidation fixtures;
- fresh-process recomputation inputs.

## 8. Why this is CHANGES_REQUIRED, not TYPED_RESIDUAL

The failures are real, but they do not yet demonstrate an architectural impossibility at the declared **synthetic source-free C1-01 grain**.

They can be repaired by tightening the frozen interface/oracle:

- make condition/value pairing a verifiable relation rather than a co-hash;
- freeze its synthetic ground truth and fixture authorities;
- freeze the exact slice projection;
- add UNKNOWN separately;
- carry the relation through determinants/replay.

The worker was correct to leave real-source subject↔survey comparability external. This reviewer does not authorize inventing it.

Therefore:

`CHANGES_REQUIRED`

not `TYPED_RESIDUAL`, and not an Astra escalation.

## 9. Re-review boundary

Do **not** issue C1-01 from:

`df6f2d36e274744d217dc4a380c73e2c7e18e83f`.

The correction may remain documentary and under the C1-00 worker-return terrain. Re-review should attack at minimum:

1. P1 subject preimage paired to P2 predicate value;
2. same conditioner ID, same source/release/target, different value;
3. changed fixture-authority scope under the same label;
4. denominator-member-set equality attack;
5. RAW/weighted numerical equality;
6. distinct UNKNOWN vs UNVISITED vs UNRESOLVED;
7. alternate evidence geometry/raw_support encodings;
8. mutation of the condition-binding witness with other determinants held fixed.

No production-owner repair is authorized by this review.

`C1_00_INDEPENDENT_REVIEW_COMPLETE`
