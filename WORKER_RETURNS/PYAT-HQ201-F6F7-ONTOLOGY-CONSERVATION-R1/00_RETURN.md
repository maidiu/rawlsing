# HQ201-R1 Return — F6/F7 ontology conservation and current-constitution court

**Disposition:** `F6_F7_ONTOLOGY_PARTIAL__NAMED_CURRENT_OWNERS_MISSING`
**Branch:** `agent/rabochii-pyat-hq201-r2`
**Startup SHA (verified exact):** `9b3a70af26da3404f988674c879a44ebfcae196a`
**Documentary base:** `2dcc9a2ed7cf9e11ae91e01e9d8030c6ca4b85eb`
**Checkout mode:** `SPARSE_REQUIRED` — sufficient. No clone, no full checkout.

Documentary architecture/theory conservation. No production mutation, no survey access, no code changes.

---

## Headline

**F6 is largely already implemented. F7 has a lawful ingress gate and no producer at all.**

| | status |
|---|---|
| F6 composition without pooling | **IMPLEMENTED** |
| F6 typed cross-source *relation* | named missing owner |
| F7 ingress gate (M1) | **IMPLEMENTED** |
| F7 temporal identity / observation / relation / delta / directionality / trajectory / rupture / gap | **8 named missing owners** |
| Noncomparability typed state | **IMPLEMENTED** |
| Disagreement policy | slot exists, **not enforced** |
| Time-grain vocabulary | **absent** |
| F8 seam + actor firewall | **IMPLEMENTED** |

---

## The three findings that decide the case

### 1. F6's core relation is already lawful in code

`pre553_empirical_query.py` implements `SOURCE_INDEXED_MULTI_UNIVERSE`: with more than one universe it emits
**one fact per universe** into a single result — never a merged row, never a cross-source cell. Cross-source
composition additionally requires an `AUTHORIZED_COMPOSITE` bundle binding three roles (`pooling`,
`nonduplication`, `estimand_composition`), and raises if any is absent.

The design detail worth appreciating: to compose across sources you must **positively bind** a
`SOURCE_COMPOSITION_POOLING` authority. Pooling is not a default to avoid; it is a power that must be granted.
That is stronger than prohibition-by-omission, and it means `CROSS_SOURCE_COEXISTENCE != RESPONDENT_POOLING` is
**structural**, not aspirational.

### 2. F7's contract is written; its producer is absent

`m1_temporal_v554_admission_dedup.py` describes itself as a *"Pure fail-closed runtime for frozen ... M1
**ingress** semantics"* with `TARGET_USE = "STRUCTURAL_MEDIATION_INPUT"`. It **requires** `TEMPORAL_KEY`,
`TEMPORAL_OBSERVATION` and `TEMPORAL_RELATION`, and delegates their meaning to V553
(`BasisKind.V553`, `REQUIRES_V553_OWNED_TEMPORAL_MEANING`).

Those three families appear **only** in the gate and in synthetic test fixtures — and **no current module
defines any Temporal/Wave/Anchor/Interval class at all.** Across the eight commissioned modules:
`effective_interval` 0, `fieldwork` 0, `delta` 0, `trajectory` 0, `rupture` 0, `longitudinal` 0, `panel` 0.

So F7 is not a design problem. It is an unimplemented producer against an already-written ingress contract.

### 3. "F7 cannot honestly close before F6" is not tenable as stated

F7's own law is defined **within** a survey family ("comparable same-survey waves") and never invokes
cross-source composition. F6's law never invokes temporal directionality. Case A is F7-complete alone; case B is
F6-complete alone.

The decisive case is **G**: a temporal relation blocked by noncomparability, while cross-source coexistence
stays lawful. If F7 were a prerequisite for F6, G would be unsatisfiable whenever temporal comparison fails —
forcing either a fabricated temporal result or the loss of a lawful structural one. **The dependency runs the
wrong way.**

The phrase is right only as a warning about *completion*: a whole-PRE-V3 claim needs both, because the
deliverable is one world that is simultaneously multi-source and temporally realized.

**Corrected law:** F6 and F7 are **orthogonal** per source and per track, and **serial only at the integrated
whole-PRE-V3 world claim**.

---

## Conservation, done honestly

From 27 historical concepts: **15 KEEP FUNCTION · 4 KEEP CONSTRAINT ONLY · 6 OBSOLETE IMPLEMENTATION DETAIL ·
2 EXPLORATORY/NEVER BINDING.**

Refused as obsolete: `linear_between_authorized_waves`, `anchor_copy`, the scalar `0.10` rupture coefficient,
parquet/year-indexed topology, and old stage names.

Two absences are **constitutionally correct** rather than gaps:

- **Interpolation was never binding authority** — an `allow_interpolation` boolean defaulting to
  `gap_marked_unknown`, with `source_authority_status: "cautious_interpolation_allowed"`.
- **No causal authority exists anywhere** — `causal` occurs **zero** times in the 4187-line V553 pressure
  module, and the rupture event-override slot reads `reserved_not_filled` on every row.

The cleanest conservation case is V553's single-family rule. Its **function** (declare your family; fail closed
on mixing) is exactly right. Its **topology** (one family per *report*) makes composition case D impossible. Keep
the function, drop the topology.

---

## Field Forge: vocabulary adopted, none of it

The commission asked me to study `POSITIONED_SOCIAL_WORLD_PACKET`, `POSITIONAL_PRESSURE_FOOTPRINT` and
`POSITION_GEOMETRY_FAMILY`. Field Forge's own §8 lists all three among proposals that **"must not be smuggled
into current Rawlsing by the word 'contract' in a Field Forge filename."**

So I adopted **zero** Field Forge vocabulary, and took only its value as a requirements and failure-mode
catalogue — which is genuinely useful: *"mode/form/routing artifact masquerading as structural difference"*
is precisely why `DIFFERENCE != TRAJECTORY` needs an explicit comparability admission.

Field Forge's own diagnosis is the right warning for this lane: *"the vocabulary of the learned social world
outran the lawful producer story beneath it."*

---

## Architecture test

**A holds; B does not; one narrow C.**

Criterion B fails because HQD-125 §15 permits reopen only where a responsibility **cannot** be satisfied by
lawful same-grain succession or bounded implementation. Every missing owner passes that test affirmatively —
M1 defines the ingress contract, structural admission carries the slots, the query module carries the lawful
composition shape. Nothing is unrepresentable, so **no architecture reopen is triggered**.

One fork is referred out rather than decided:

> **`TIME-GRAIN-FORK`** (`ASTRA_DECISION_CANDIDATE`) — for multi-source comparison, is temporal identity keyed
> on a **point year** or a **fieldwork interval**?

No binding law names a grain; V553's point-year choice was scoped to one family in one country; the current
slots are untyped so a caller could smuggle a midpoint year; and composition case C cannot be answered without
deciding. It blocks **only** case C — not same-survey F7, where point-year is conservative and adequate.

Calling the whole lane an Astra matter would be calling Astra merely because work remains.

---

## One anti-collapse law is not actually enforced

`source_disagreement_noncomparability_policy` is validated only as a **non-empty string** with no enumerated
vocabulary. A caller could name an averaging policy in free text with no structural refusal — so
`SOURCE_CONFLICT != AVERAGE_BY_DEFAULT` is currently *textual*, not *structural*. The lawful plural-observation
route works; the refusal of averaging does not. Bounded fix: enumerate the vocabulary and refuse averaging by
default.

---

## Sequence

`13_IMPLEMENTATION_SEQUENCE.md`. Steps 1 (type the empty slots), 2 (conserve the identity function) and 5 (typed
cross-source relation) are **mutually independent**. Steps 3–4 implement against M1's existing contract. Step 6
composes F6×F7; step 7 binds F8 last. Deliberately **not** in the sequence: any world-container persistence
build, any Field Forge product family, any interpolation capability, any inherited scalar pressure formula, and
any causal capability.

## Artifacts

`00_RETURN.md` · `01_CURRENT_BINDING_F6_F7_LAW.json` · `02_CURRENT_IMPLEMENTED_CAPABILITY_MAP.json` ·
`03_HISTORICAL_FUNCTION_CONSERVATION_MATRIX.json` · `04_FIELD_FORGE_CAPITAL_CLASSIFICATION.json` ·
`05_TEMPORAL_IDENTITY_AND_COMPARABILITY_CONSTITUTION.md` · `06_CROSS_SOURCE_COMPOSITION_CONSTITUTION.md` ·
`07_F6_F7_COMPOSITION_CASES.json` · `08_GAP_RUPTURE_INTERPOLATION_LAW.json` ·
`09_MULTI_SOURCE_TEMPORAL_WORLD_OBJECT.md` · `10_F8_CONSUMER_CONTRACT_CANDIDATE.md` ·
`11_CURRENT_OWNER_AND_MISSING_OWNER_MAP.json` · `12_ARCHITECTURE_REOPEN_AND_ASTRA_TEST.json` ·
`13_IMPLEMENTATION_SEQUENCE.md` · `14_FINAL_DISPOSITION.json`

`HQ201_F6F7_ONTOLOGY_CONSERVATION_RETURNED__HQ_ADJUDICATION_REQUIRED`