# 09 — Proposed multi-source temporal world object

**Status of this document.** `NEW_PROPOSAL_REQUIRING_HQ_ADOPTION`. It is a documentary candidate constitution.
Nothing here is implemented, and nothing here was derived from Field Forge vocabulary.

---

## The governing constraint

`EXPLORATORY_NONBINDING_CAPITAL`, Field Forge §8, listing what must **not** be smuggled into current Rawlsing
"by the word 'contract' in a Field Forge filename":

> `POSITIONED_SOCIAL_WORLD_PACKET` · `POSITIONAL_PRESSURE_FOOTPRINT` · `POSITION_GEOMETRY_FAMILY` ·
> `DISPOSITION_GEOMETRY_ATLAS` · `LOCAL_POSITION_SPACE` as a universal producer · and others.

The commission asked me to study exactly these. **They are self-marked speculative by their own authors**, so
none is adopted here. The world object below is named `MultiSourceTemporalWorld` and is derived from
HQD-125 §§9–12 plus the conserved historical contracts — not from Field Forge.

The Field Forge lesson I *do* carry is a constraint, not a name: **geometry family, not forced universal space.**
So the object below is a **graph with typed nodes**, explicitly not a single wide table, and not a single
mandatory geometry.

---

## Why not a monolithic table

A single respondent-level panel would violate three binding laws at once: `MULTIPLE_SURVEY_FIELDS !=
ONE_SYNTHETIC_RESPONDENT_TABLE`, `CROSS_SOURCE_COMPOSITION != CROSS_SOURCE_JOINT_RESPONDENT_CLAIM`, and
`STRUCTURAL_WORLD_TIME != ACTOR_MEMORY`. The commission's `F6_PLUS_F7 != ONE_SYNTHETIC_PANEL` is the same law
stated as a test.

The honest structure is a **graph of source-local products joined by typed relations**, because the relations
are the whole content and a table would erase them.

---

## The object

```text
MultiSourceTemporalWorld
├── provenance            : survey family, universe ref, sealed release ref, replay determinants
├── source_tracks[]       : one per survey family — NEVER one per world
│   ├── family_key, country_scope
│   ├── anchors[]         : typed time anchors (grain per TIME-GRAIN-FORK)
│   └── temporal_relations[]  : identity_continuity | comparability | delta |
│                              directionality | persistence | rupture_candidate |
│                              absence | noncomparability
├── structural_propositions[] : actor-independent, each with its empirical basis refs
├── cross_source_relations[] : mere_coexistence | complementarity | corroboration | contradiction
│                             — a TYPED RELATION, never a merged scalar
├── gaps_and_absence[]    : typed unknown and typed noncomparability, distinguished
└── uncertainty_ledger[]  : confidence, penalty and pressure-basis entries
```

### Field definitions

**`source_tracks[]`** — the unit is the **survey family**, not the wave and not the world. This is the single
most important structural decision, and it is where the historical topology had to be corrected.
`HISTORICAL_FUNCTIONAL_CAPABILITY`: V553 refused a report mixing families. Dropping that *topology* while
keeping its *function* (declare your family, fail closed on mixing) is what makes two independently
temporalized families coexist. See `06_CROSS_SOURCE_COMPOSITION_CONSTITUTION.md`.

**`anchors[]`** — typed time anchors. Grain is **deferred** to `ASTRA_DECISION_CANDIDATE` `TIME-GRAIN-FORK`
(§05). Whichever grain is chosen, one constraint binds now, conserved from V553: **no implicit
wave-ordinal-to-year coercion, and no midpoint coercion.** An unknown interval is an unknown interval.

**`temporal_relations[]`** — every relation of O2, kept distinct. Three structural rules ride along:

- a **trajectory requires ≥ 3 anchored points**, so two waves can yield identity, comparability and delta but
  *cannot* yield a trajectory;
- **directionality is an admission, not a computation.** `HISTORICAL_FUNCTIONAL_CAPABILITY` gives the exact
  shape: `directionality_status` + `directionality_basis` + `directionality_coverage_status`. A producer that
  cannot supply basis and coverage must emit `noncomparability`, never a slope;
- **difference ≠ trajectory ≠ causal explanation.** The last is `ASTRA_DECISION_CANDIDATE`-adjacent but firmer:
  `causal` occurs **zero** times in the 4187-line V553 pressure module, and no current law supplies it. Naming
  a cause requires authority that exists in no evidence class.

**`cross_source_relations[]`** — a **typed relation object**, not a merged metric. Justified in §06: lawful
coexistence is implemented, typed corroboration/contradiction is not. The relation carries
`{relation_kind, proposition_ref, per_source_fact_refs, authority_ref, unresolvedness}` and **must not reduce
to a scalar** — `SOURCE_CONFLICT != AVERAGE_BY_DEFAULT`.

**`gaps_and_absence[]`** — absence and noncomparability are *observations with blocks*, not missing values.
`HISTORICAL_FUNCTIONAL_CAPABILITY` gives the right shape: `V553_TEMPORAL_GAP_AND_ABSENCE_INDEX_SCHEMA` paired
with `V553_TEMPORAL_KEY_BLOCKER_INDEX_SCHEMA`, so a refused key is recorded rather than merely omitted.
`ABSENCE != ZERO` and `NONCOMPARABLE != NO_CHANGE`.

**`uncertainty_ledger[]`** — `V553_CONFIDENCE_PENALTY_LEDGER_SCHEMA` + `V553_PRESSURE_BASIS_LEDGER_SCHEMA`.
Needed so a weak delta is distinguishable from no delta. Without it, `DIRECTIONALITY` and
`NONCOMPARABILITY` blur.

---

## Deliberate omissions

Each omission is a *refusal*, and each has a law or a self-marked-speculative finding behind it.

| omitted | why |
|---|---|
| any scalar composite across sources | averaging is forbidden; a merged metric would erase the contradiction relation |
| interpolated periods | interpolation was never binding authority — it was an `allow_interpolation` boolean defaulting to `gap_marked_unknown`. No binding law authorises it. |
| causal attribution of a temporal break | zero causal concepts historically; no current law; the event-override slot is `reserved_not_filled` |
| an "actor time" or "structural memory" axis | `STRUCTURAL_WORLD_TIME != ACTOR_MEMORY` is binding; world time is an empirical anchor, not a remembered one |
| a single geometry / position space | Field Forge's own geometry-family-vs-forced-universal-space caution |
| `POSITIONED_SOCIAL_WORLD_PACKET` and siblings | self-marked speculative by Field Forge §8 |
| a lineage table | V553's parquet/Arrow compiler and year-indexed tables are obsolete implementation detail |

---

## Interoperability with what already exists

The world object is a **graph over current outputs**, not a replacement for them.

- per-universe facts already arrive source-indexed from `SOURCE_INDEXED_MULTI_UNIVERSE` — the world object's
  `cross_source_relations[]` annotates them rather than replacing them;
- structural propositions already have an admission seam with `allowed_effective_time_or_interval_refs`,
  `effective_period`, `allowed_uncertainty_states` and `EMPIRICAL_FACT_NONCOMPARABLE` — the world object needs
  those slots *typed*, not replaced;
- `M1` already specifies the ingress contract any temporal producer must satisfy: three signatures,
  `TEMPORAL_KEY` + `TEMPORAL_OBSERVATION` for `SIG_002`, `TEMPORAL_KEY` + `TEMPORAL_RELATION` for `SIG_003`,
  and an `EQ_FIELDS` fingerprint set including effective-time semantics and comparability authority.

**So the world object is mostly a typing and relation layer over lawful existing parts, plus the missing temporal
producers.** That is the substantive reason this is not an architecture reopen.

---

## Open items carried by this proposal

1. `ASTRA_DECISION_CANDIDATE` — anchor grain for cross-family comparison (`TIME-GRAIN-FORK`).
2. `NEW_PROPOSAL_REQUIRING_HQ_ADOPTION` — the typed cross-source relation object, and whether one temporal-key
   contract may serve both response surfaces and structural propositions (I judge: it may not).
3. `NEW_PROPOSAL_REQUIRING_HQ_ADOPTION` — an enumerated vocabulary for
   `source_disagreement_noncomparability_policy`, replacing free text, so averaging is structurally refused.
4. Whether the world object needs its own persistent container or may be assembled per query result. My reading:
   assemble per result; a persistent container is not required by any binding law, and building one pre-emptively
   would be inventing architecture.