# 06 — Cross-source composition constitution

---

## The headline

**Cross-source composition is already lawfully representable, and it is already implemented.** This is the
strongest positive finding in the court. `CROSS_SOURCE_COEXISTENCE != RESPONDENT_POOLING` is not an aspiration
awaiting architecture — it is enforced in code.

`CURRENT_IMPLEMENTED_CAPABILITY`, `rawlsing_next/pre553_empirical_query.py`:

- `source_scope_mode == "SOURCE_INDEXED_MULTI_UNIVERSE"` with more than one universe produces **one fact per
  universe**, collected into a single `QueryExecutionResult`, sorted by fact ref. It never emits a merged row
  and never emits a cross-universe cell.
- Each query universe must resolve in **exactly one** supplied sealed C11 release.
- Cross-source composition additionally requires an `AUTHORIZED_COMPOSITE` bundle that binds three roles:

| role | required authority kind |
|---|---|
| `pooling` | `SOURCE_COMPOSITION_POOLING` |
| `nonduplication` | `SOURCE_UNIVERSE_RELATION` |
| `estimand_composition` | `SOURCE_COMPOSITION_POOLING` + `WEIGHT_DESIGN_ESTIMAND` |

Any missing role raises. Composition authority is therefore **explicit, operation-scoped and fail-closed** —
exactly what HQD-125 §9 demands.

Note the inversion worth understanding: to compose across sources you must *positively bind* a
`SOURCE_COMPOSITION_POOLING` authority. Pooling is not a default to be avoided; it is a power that must be
granted. That is a stronger and better design than prohibition-by-omission.

---

## O3 — What is a cross-source relation?

Six lawful relations, and two forbidden ones. The forbidden pair is `CURRENT_BINDING_LAW` (HQD-125 §9):
`CROSS_SOURCE_COMPOSITION != CROSS_SOURCE_JOINT_RESPONDENT_CLAIM`.

| relation | what it asserts | current representation | status |
|---|---|---|---|
| **coexistence** | both bear on one objective social world | `SOURCE_INDEXED_MULTI_UNIVERSE`, per-universe facts in one result | **IMPLEMENTED** |
| **complementarity** | each covers what the other does not | per-universe facts with distinct scopes | **IMPLEMENTED** implicitly, via scope preservation |
| **corroboration** | independent sources agree on a shared proposition | — | **NAMED MISSING OWNER** |
| **contradiction** | sources disagree, and the disagreement is retained | partial: `EMPIRICAL_FACT_NONCOMPARABLE` | **NAMED MISSING OWNER** |
| **structural composition** | fields compose at actor-independent structural grain | Field Forge ingress boundary | **JURISDICTION ONLY** (EE15); not constituted |
| **portability** | a source's metric transfers to another source's frame | — | **FORBIDDEN** absent exact authority |
| respondent pooling | one respondent table across sources | — | **FORBIDDEN** |
| same-respondent jointness | a joint respondent claim across sources | — | **FORBIDDEN absent impossible-to-assume linkage authority** |

### Does composition need a typed relation object rather than a merged metric?

**Yes — and this is the principal F6 gap.** `CURRENT_IMPLEMENTED_CAPABILITY` gives lawful *coexistence*:
N source-indexed facts in one result. It does **not** give a typed relation *between* them.

The distinction matters operationally. Coexistence answers "what does each source say?" It does not answer "do
they agree, contradict, or complement each other?" — and those three demand different downstream handling. A
result carrying two contradicting facts is lawful today; nothing marks them as *contradicting* rather than merely
*both present*.

`NEW_PROPOSAL_REQUIRING_HQ_ADOPTION`: a typed cross-source relation object carrying
`{relation_kind: corroboration | contradiction | complementarity | mere_coexistence, proposition_ref,
per_source_fact_refs, authority_ref, unresolvedness}`. It must **not** collapse to a scalar — averaging is
forbidden by `SOURCE_CONFLICT != AVERAGE_BY_DEFAULT`.

Note the existing honest seam: `pre553_structural_admission.py` states in its own docstring that it *does not*
"infer source relations". That is an explicit, named absence — the architecture declared the boundary rather
than silently leaking into it.

---

## O3 — WVS and EVS in one objective world, without one respondent table

This is lawful **today**, subject to authority. The mechanism:

1. WVS and EVS each supply their own universe ref and their own sealed C11 release.
2. The query declares both universe refs; `AUTHORIZED_COMPOSITE` binds pooling, nonduplication and estimand
   composition authorities for that operation.
3. Execution returns **one fact per universe**, each carrying `universe_refs=(that universe,)` and the full
   `release_refs` tuple.
4. Downstream consumers see a single result object holding both, with provenance intact on each fact.

What this buys: one query, one world, per-source facts, no merge, no synthetic respondent, no implicit
portability.

What it does **not** buy, and must not be read as buying:

- **no same-respondent jointness.** There is no linkage authority and none can be assumed;
- **no comparability between WVS and EVS on a metric.** They are different instruments with different
  response surfaces. `SAME_LABEL != SAME_TEMPORAL_OBJECT` has an exact cross-source analogue: same variable
  label ≠ same measured construct across instruments;
- **no cross-source temporal relation** without the comparability admission of §05, which itself hits the
  `TIME-GRAIN-FORK` for nonaligned fieldwork.

`SOURCE_CONFLICT != AVERAGE_BY_DEFAULT` — and the current slot that ought to enforce it does not:

> `source_disagreement_noncomparability_policy` is validated only as a **non-empty string**, with no
> enumerated vocabulary.

So a caller could name an averaging policy in free text and nothing structural would refuse it. The lawful
plural-observation route exists and works; the *refusal of averaging* is textual rather than structural. That is
bounded implementation work, not architecture.

---

## Two independently temporalized survey families

They coexist as **two tracks**, each with its own family declaration, anchors and temporal relations. This is
composition case D, and it is where the historical topology must be dropped rather than inherited.

`HISTORICAL_FUNCTIONAL_CAPABILITY`: V553 temporal identity required **exactly one survey family per report** and
raised `"V553 temporal input mixes survey families"`. That single-family rule is an **obsolete topology**, not a
conserved function.

- **KEEP FUNCTION:** a track must explicitly declare its survey family, and a family-mixing error must fail
  closed. Both remain exactly right.
- **DROP TOPOLOGY:** "one family per report" must become "one family per **track**", with multiple tracks
  composing into one world.

This is the cleanest example in the whole court of the difference the commission asked for: **recover functional
intent without inheriting obsolete topology.** Inheriting the single-family-per-report rule would make case D
impossible; keeping the declare-your-family function makes it routine.

---

## Mismatched fieldwork intervals

They are represented as **typed noncomparability**, never coerced to a common midpoint.

`CURRENT_IMPLEMENTED_CAPABILITY`: `EMPIRICAL_FACT_NONCOMPARABLE` is an enumerated refusal with reason codes —
among them `ESTIMAND_NOT_ALLOWED_BY_RULE` and `MEASURE_WEIGHT_BASIS_NOT_ALLOWED_BY_RULE`. A source whose
interval or estimand is not admitted yields a typed non-comparable fact rather than a dropped or invented one.

That is `NONCOMPARABLE != NO_CHANGE` working in current code.

What is missing is the **interval grain** that would let two families be compared at all
(`TIME-GRAIN-FORK`, §05). Until it is resolved, case C concludes at typed noncomparability — which is a lawful,
if conservative, resting place.

---

## A minimum cross-source composition contract

Stated so it can be checked rather than admired:

1. **No merged row, ever.** Composition is a collection of per-source facts, not a widened table.
2. **Every fact carries its own universe and release provenance**, even inside a multi-universe result.
3. **Composition authority is operation-scoped and fail-closed** — pooling, nonduplication and estimand
   composition must all be positively bound.
4. **Absence is typed, not zero.** A non-comparable fact is not an absence and not a zero.
5. **Disagreement is preserved.** Contradiction is a relation to be recorded, not a variance to be averaged.
6. **No portability by assumption.** Cross-source metric comparability requires its own admission.
7. **A blocked temporal relation does not contaminate coexistence** — see composition case G, which is the case
   that proves F6 and F7 are orthogonal.