# 05 — Temporal identity and comparability constitution

**Evidence classes used throughout:** `CURRENT_BINDING_LAW` · `CURRENT_IMPLEMENTED_CAPABILITY` ·
`HISTORICAL_FUNCTIONAL_CAPITAL` · `EXPLORATORY_NONBINDING_CAPITAL`, plus
`NEW_PROPOSAL_REQUIRING_HQ_ADOPTION` and `ASTRA_DECISION_CANDIDATE`.

---

## O1 — What persists through time?

**The honest answer is that current law does not yet name the persisting object, and no current code produces
one.** What follows is the constituted account of what must persist, assembled from binding law plus the
historical functional capital that survived classification.

`HISTORICAL_FUNCTIONAL_CAPITAL` gives the sharpest available statement. V553 required, per temporal track:
exactly one explicit survey family, exactly one country, a declared wave identity, and an **explicit calendar
anchor obtained without treating a wave ordinal as a year**. It further required one anchor per calendar year
and refused duplicate anchors. That is a *fail-closed identity contract*, and it is the correct functional
shape.

But note what it is **not**: it is not a claim that a wave is a time. It is a claim that a track may only be
constructed once you have declared *which family*, *which wave*, and *what anchor* — and that the anchor must be
real.

### The persisting ingredients, by object family

Different object families need **different** temporal identity contracts. This is a substantive finding, not a
convenience: `SAME_LABEL != SAME_TEMPORAL_OBJECT` is precisely the law that forbids one contract serving all
families.

| object family | what must persist | what must be re-established at t2 | evidence |
|---|---|---|---|
| source-native question / response surface | exact question text, response code set, coding, value labels | that the surface is *the same surface*, not merely similarly labelled | `CURRENT_BINDING_LAW` (response-surface authority, HQD-125 §10) |
| empirical coordinate | universe, routing, applicability, denominator, weight/estimand | applicability and denominator equivalence at t2 | `CURRENT_IMPLEMENTED_CAPABILITY` (`source_universe_fingerprint`, `estimand_fingerprint`, `measure_and_weight_authority_fingerprint` in M1 `EQ_FIELDS`) |
| predictor / determinicity surface | predictor identity and conditioning basis | that the same predictor was actually re-estimated, not assumed | `CURRENT_BINDING_LAW` (HQD-125 §10 determinicity strength) |
| branch / configuration family | branch identity and recursive structure | branch prevalence re-measurement | `CURRENT_BINDING_LAW` (HQD-125 §4, §10) |
| co-signature / cloud object | component identity and order, same-respondent premise | that co-travel was re-observed, not carried forward | `CURRENT_BINDING_LAW` (HQD-125 §5, §6) |
| structural proposition | proposition identity and its empirical basis | that the proposition was re-supported at t2 | `CURRENT_IMPLEMENTED_CAPABILITY` (`focal_structural_proposition_ref` in M1 `EQ_FIELDS`) |
| structural field coordinate | field identity, geometry family, scope | scope and geometry equivalence | `CURRENT_BINDING_LAW`; geometry family is **field** requirement only, never current ontology |
| pressure relation | the relation identity plus both endpoints' anchors | both endpoints re-observed | `CURRENT_BINDING_LAW` (HQD-125 §10) |

### The minimum identity contract

Conserving `V553_TEMPORAL_KEY_CANDIDATE_INDEX_SCHEMA` **together with**
`V553_TEMPORAL_KEY_BLOCKER_INDEX_SCHEMA`, a temporal key must be:

1. a **candidate**, never self-certifying;
2. accompanied by a **blocker index** so that a refused key is itself a recorded observation;
3. de-duplicated on an explicit fingerprint set — M1 already names that set: semantic identity, native scope
   identity, **effective-time semantics**, structural-proposition ref, admission lineage, source universe,
   estimand, measure-and-weight authority, **source-relation comparability authority**, and
   interpretation-critical semantic authority;
4. fail-closed on any unknown.

M1 is therefore the **exact current specification of what a temporal producer must emit**. That is the single
most important thing this court found: the constitution is largely written; the producer is missing.

`NEW_PROPOSAL_REQUIRING_HQ_ADOPTION`: which single family above is the *primary* F7 product, and whether a
structural proposition and a response surface may share one temporal key contract. The fingerprints suggest
they must not.

---

## O2 — What is a cross-wave relation?

**Seven distinct relations, none an automatic consequence of another.** `DIFFERENCE != TRAJECTORY` and
`COMPARABILITY != DIRECTIONALITY` are the two the current record most nearly conflates, so they lead.

| relation | what it asserts | what it does NOT assert | current owner |
|---|---|---|---|
| **identity continuity** | the same object persists across t1, t2 | that anything changed | none — producer missing |
| **comparability** | t1 and t2 are lawfully comparable on declared dimensions | that they differ | slot only (`rule_relevant_source_relation_comparability_authority_fingerprint`; `allowed_effective_time_or_interval_refs`) |
| **difference / delta** | some measurable quantity differs | direction, significance or cause | none — `V553_CROSS_WAVE_DELTA_INDEX_SCHEMA` available |
| **directionality** | the difference has an established orientation | that it is large, or caused | none — `V551J directionality_status/_basis/_coverage_status` available |
| **trajectory** | an ordered path through at least three anchored points | causation, or actor memory | none |
| **persistence** | the quantity is stable across the interval | that stability is meaningful | none |
| **rupture** | an empirical discontinuity candidate exists | an authorized classification, an event, or a cause | none — `V553_STRUCTURAL_RUPTURE_CANDIDATE_INDEX_SCHEMA` available |
| **absence / noncomparability** | the relation is *blocked*, and the block is recorded | zero, no change, or a value | **partly owned**: `EMPIRICAL_FACT_NONCOMPARABLE` |

### The directionality point, stated precisely

`CURRENT_BINDING_LAW`: `TWO_WAVES_EXIST != TEMPORAL_DIRECTIONALITY_AUTHORITY`.

`HISTORICAL_FUNCTIONAL_CAPITAL` shows what law requires instead, and it is the correct answer to "what stops a
producer from just emitting a line between two points". V551J carried directionality as **three typed fields**:
`directionality_status`, `directionality_basis`, `directionality_coverage_status`.

Directionality is therefore not a fact you compute from two observations. It is an **admission** that carries a
basis and a coverage statement. A producer that cannot supply a basis and a coverage must emit
`NONCOMPARABLE`, not a slope.

Note also that a **trajectory requires at least three anchored points**, so two waves can produce identity,
comparability and delta — and *cannot* produce a trajectory at all. This is a real structural limit that
`COMPARABILITY != DIRECTIONALITY` only half-expresses.

---

## What is comparability, exactly?

Comparability is **not a property of two data points.** It is an authority-backed admission that a declared set
of dimensions is equivalent across t1 and t2, scoped to the operation.

Three independent reasons, each binding:

1. **Field Forge, as requirements.** "Questionnaire architecture becoming accidental sociology" and "mode/form/
   routing artifact masquerading as structural difference" mean a delta can be a *design* artefact. Field Forge
   is `EXPLORATORY_NONBINDING_CAPITAL`, so these are requirements, not law — but they are the reason a
   comparability admission must be explicit and scoped.
2. **Current law.** HQD-125 §10: cross-wave temporal products require exact identity, scope, **response-surface**
   and comparability authority. Response-surface equivalence is named because a re-coded or re-ordered instrument
   breaks comparability even when the label is unchanged. This is `SAME_LABEL != SAME_TEMPORAL_OBJECT` in
   operational form.
3. **Historical function.** `V553_WAVE_HARMONIZATION_EVIDENCE_SCHEMA` and
   `V553_HARMONIZATION_DIFFERENCE_LEDGER_SCHEMA` record harmonization evidence *and its differences* rather
   than reconciling them. Comparability may carry a recorded residual difference.

**Consequence:** a comparability admission is per-operation and per-source-pair. It is never global, and it is
never inherited from the mere existence of two waves.

---

## O5 — Time grain, and the one fork I am not deciding

Conserved from `HISTORICAL_FUNCTIONAL_CAPITAL`: **no implicit wave-ordinal-to-year coercion**, and one anchor
per year. Both are constraints on any producer.

But the grain question itself is open. The current DAG has **no time-grain vocabulary at all** — the only
time-adjacent fields are `allowed_effective_time_or_interval_refs` (a tuple of `ExactRef`), `effective_period`
(free mapping) and `time_geography_applicability` (free mapping). None is typed, so nothing currently prevents a
caller smuggling a midpoint year.

`ASTRA_DECISION_CANDIDATE` — **TIME-GRAIN-FORK.** For *multi-source* comparison, does temporal identity key on a
**point year** or a **fieldwork interval**? This is genuinely underdetermined:

- no binding law names a grain;
- V553's point-year choice was scoped to one family in one country and was never established as adequate for two
  families with nonaligned fieldwork intervals;
- composition case C cannot be answered without deciding it.

It is referred out rather than decided. It blocks **only** cross-family temporal comparison. It does **not**
block same-survey F7, where point-year is conservative and adequate.

**No implicit midpoint or year coercion** is binding regardless of how the fork resolves.