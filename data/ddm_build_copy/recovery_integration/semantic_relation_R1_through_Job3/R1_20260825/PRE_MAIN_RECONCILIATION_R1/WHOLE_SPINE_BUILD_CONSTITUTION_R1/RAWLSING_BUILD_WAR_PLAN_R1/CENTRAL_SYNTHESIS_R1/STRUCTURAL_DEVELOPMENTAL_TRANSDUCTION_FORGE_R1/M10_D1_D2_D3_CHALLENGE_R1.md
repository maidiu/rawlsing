# M10 — D1 / D2 / D3 CHALLENGE R1

STATUS: `CHALLENGE_COMPLETE`

FROZEN TARGET: `9cf100a101e92891e2b4d0af0e308d27f7015a6b`

M10 challenges only the frozen candidate's proposed positive deltas:

- D1 `TYPED_ACTOR_RELATIVE_SOCIAL_ECOLOGY_DERIVATION`
- D2 `INTERVAL_RECURRENCE_AND_TRANSITION_REBINDING`
- D3 `PROVENANCE_PRESERVING_RECIPROCAL_SOCIAL_WORLD_UPDATE`

## D1 — challenge

### Attack

Could `class` simply be attached to a person and consumed downstream, making D1 unnecessary?

### Source result

**NO.** Wright's own class concept decomposes into relations over productive assets, effective control, organization, authority, credentials/skills, appropriation and dependency. The same nominal class category can conceal materially different relations; contradictory locations are explicitly multiplex. Wright also separates objective alternatives from actual choices and subjectivity.

### D1 strengthening

D1 should require, for class-related derivations:

```text
ASSET / PROPERTY / CONTROL RULE
+ ACTOR POSITION
+ COUNTERPART / ORGANIZATION / MARKET BINDING
+ CONTEXT / TIME
+ MECHANISM
-> EXACT RESOURCE / DEPENDENCY / AUTHORITY / GATE / OBLIGATION / EXIT / OPPORTUNITY CONSEQUENCE
```

High-value D1 subcases:

- property separation -> wage/income dependency and exit constraint;
- capital control -> hiring/investment/disinvestment and appropriation relation;
- organization control -> scoped policy/coordination power;
- supervision -> directed task/sanction relation;
- credential closure -> actor-specific eligibility/bargaining opportunity only with job/gate match;
- household relation -> resource/time/dependency transfer only with actual household bindings.

### D1 narrowing

D1 must **not** emit:

- class consciousness;
- political preference;
- solidarity;
- obedience;
- personality/type;
- generic `life chances` or `exploitation` scalar.

**D1 verdict:** `PASS__STRONGLY_STRENGTHENED_BY_WRIGHT__RELATION_DECOMPOSITION_REQUIRED`.

## D2 — challenge

### Attack

Does Wright require time machinery beyond the frozen candidate?

### Source result

Wright adds real temporal demands but no distinct new temporal primitive:

1. positions can change through promotion, asset acquisition/loss, job change and credential-job rematching;
2. credentials devalue historically and therefore qualification is cohort/time dependent;
3. cross-sectional age patterns confound career mobility and historical expansion of positions;
4. class biography/trajectory matters empirically apart from current position;
5. household member labour-force/class transitions can change another actor's material ecology;
6. political reforms and organization can alter later structural possibilities.

These require interval validity, typed histories and transition rebinding. They do **not** require a special `CLASS_TRAJECTORY` object.

### D2 required form

```text
RELATION_SET_t
+ REALIZED GATE / ASSET / JOB / HOUSEHOLD TRANSITION
-> CLOSE OR MODIFY PRIOR BINDINGS
-> OPEN NEW PROPERTY / DEPENDENCY / AUTHORITY / GATE / OBLIGATION BINDINGS
-> PRESERVE BEFORE/AFTER PROVENANCE
```

Cross-sectional demographic patterns are insufficient evidence for such transitions.

**D2 verdict:** `PASS__STRENGTHENED__EXISTING_INTERVAL_HISTORY_TRANSITION_REBINDING_SUFFICIENT__NO_CLASS_TIME_PRIMITIVE`.

## D3 — challenge

### Attack

Does Wright really support actor/collective action feeding back into structure, or would D3 overbuild?

### Source result

The book's distinction between class structure and class formation plus its final political analysis strongly supports **gated** reciprocal update:

- class relation distributes resources/capacities/stakes;
- organization/coalition formation is contingent;
- parties/unions/law/welfare institutions change formation possibilities;
- collective action can seek institutional/property change;
- reforms can change the conditions of later struggle;
- no action guarantees success.

Thus D3 is justified **only** in the frozen candidate's bounded form:

```text
ACTION
-> EXTERNAL RESPONSE / INSTITUTIONAL GATE
-> ADMITTED CHANGE IN RULE / PROPERTY / ORGANIZATION / RESOURCE / RELATION
-> PROVENANCE-BEARING WORLD FACT
-> LATER D1 DERIVATION
```

No direct V3-to-PRE-V3 back-writing and no collective psychological subject.

**D3 verdict:** `PASS__SUPPORTED__MUST_REMAIN_RESPONSE_GATED_AND_PROVENANCE_PRESERVING`.

## D4 necessity court

Potential candidates examined:

- `CLASS_RELATION` primitive — unnecessary; composed from existing typed structural relations.
- `CONTRADICTORY_LOCATION` primitive — unnecessary derived predicate.
- `OBJECTIVE_INTEREST` runtime engine — unnecessary as a separate transduction primitive; can be analyst-level/derived structural stake and must not trespass into motive.
- `CLASS_FORMATION` primitive — unnecessary; organization/network/coordination/action relations plus D3 suffice.
- `LIFE_CHANCES` primitive — rejected; decompose to opportunities/gates/resources/history.
- `MOBILITY` primitive — rejected; transition rebinding over exact relations suffices.

**G. Is D4 needed?** `NO`.

## Smallest M10 delta to frozen candidate

No new D-family. Tighten D1's normative examples and implementation tests so that `class` must arrive decomposed; ensure D2 tests historical credential/job qualification and career/cohort non-collapse; ensure D3 tests class formation/action failure and response gating.

## Challenge terminal

`PASS__M10_D1_D2_D3_CHALLENGE__D1_STRONGLY_STRENGTHENED__D2_CONFIRMED__D3_CONFIRMED__NO_D4`
