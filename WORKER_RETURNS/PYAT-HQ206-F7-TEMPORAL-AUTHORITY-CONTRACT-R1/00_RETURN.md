# 00 — HQ206 F7 temporal positive-authority contract derivation — R1

Lane: `PYAT-HQ206-F7-TEMPORAL-AUTHORITY-CONTRACT-R1`
Role: documentary authority-contract worker — Space Bunny Max or High
Tip verified equal: `20568aae374396cbc058bb500777491379a29f8c`

**Disposition: `TEMPORAL_COMPARABILITY_CONTRACT_READY_FOR_INDEPENDENT_REVIEW`**
Terminal: `HQ206_F7_TEMPORAL_AUTHORITY_CONTRACT_RETURNED__HQ_REVIEW_REQUIRED`

This lane is **documentary only**. No production code. The change set is nine
new files, all under `WORKER_RETURNS/PYAT-HQ206-F7-TEMPORAL-AUTHORITY-CONTRACT-R1/`.

---

## 1. What was derived

The F7 candidate is now an explicit current authority package:

| Artifact | Content |
| --- | --- |
| `01_TEMPORAL_COMPARABILITY_AUTHORITY.json` | The new authority-kind contract, with a minimality proof |
| `02_TEMPORAL_RELATION_RECEIPT_CONTRACT.json` | The positive temporal relation form; contains the defect closure |
| `03_TEMPORAL_STATE_VOCABULARY.json` | Typed state families and reason codes; **this is what closes the defect** |
| `04_TIME_ORDER_BASIS_LAW.json` | Exactly four order-basis kinds; the polymorphism law |
| `05_OWNER_AND_SUCCESSION_MAP.json` | The five conserved functions, deliberately not collapsed |
| `06_NONCOLLAPSE_AND_REFUSAL_MATRIX.json` | 15 non-collapse laws + 14 refusal conditions |
| `07_IMPLEMENTATION_BOUNDARY.md` | What is authored, what is forbidden, what is left downstream |
| `08_FINAL_DISPOSITION.json` | Disposition, named gaps, corrections |

## 2. The minimality proof — why exactly one new authority kind

The adopted closed set `AUTHORITY_KINDS`
(`rawlsing_next/pre553_empirical_authority.py:25-44`) holds exactly **18** kinds.
All seven authority kinds the commission named for reuse are **already members
of that set** — not near-misses:

`TEMPORAL_EVIDENCE` · `WEIGHT_DESIGN_ESTIMAND` · `TARGET_USE_PERMISSION` ·
`SOURCE_EQUIVALENCE` · `NATIVE_CANONICAL_MAPPING_HARMONIZATION` ·
`UNCERTAINTY_METHOD` · `REPLAY_PROTOCOL`

So every required input except the comparison law itself already exists as an
exact authority kind or an exact ref. **One** new kind closes it; the set goes
18 → 19. Zero sibling kinds created.

`TEMPORAL_EVIDENCE` binds source-native effective/reference-time evidence. It
binds evidence; **it does not order observations.** That specific gap is what
`TEMPORAL_COMPARABILITY` fills, and nothing else does.

## 3. The defect is closed

**As found.** `TEMPORAL_NONCOMPARABLE` occurred at exactly **one** production
site — `rawlsing_next/pre553_source_relations.py:54` — as a bare string inside
`FORBIDDEN_BACKFILL_TARGET_STATES`. No producer, no schema, no reason code.

**The contrast that defines it.** The SOURCE-side counterpart
`EMPIRICAL_FACT_NONCOMPARABLE` **is** a produced decision: appended at
`pre553_structural_admission.py:639-640` and `:680-681`, with reason codes, from
`fact.typed_state == NONCOMPARABLE`, enumerated at `:47`, mapped at `:65`.
SOURCE side had schema, producer and reason. TEMPORAL side had none of the three.

**As closed.** A produced, reason-carrying, terminal member of
`TEMPORAL_RELATION_STATE`, placed at `TEMPORAL_RELATION_RECEIPT.relation_state`
with a mandatory `relation_state_reason`. **Backfill prohibition preserved** —
it remains in the forbidden-backfill tuple.

**Not closed by** deleting the string, **nor** by permitting a backfill, **nor**
by manufacturing comparability.

### SOURCE noncomparable ≠ TEMPORAL noncomparable

| | SOURCE_NONCOMPARABLE | TEMPORAL_NONCOMPARABLE |
| --- | --- | --- |
| Concerns | whether the **fact** is comparable | whether the **ordered pair** is comparable in time |
| State | `NONCOMPARABLE` in `SOURCE_UNIVERSE_STATE` | `TEMPORAL_NONCOMPARABLE` in `TEMPORAL_RELATION_STATE` |
| Producer | structural admission | temporal comparison operation |
| Scope | limits source-space use | blocks temporal relation/delta use |

The conserved V553 semantics are carried explicitly: `is_limit: true`,
`does_not_negate_original_fact: true`. **A temporal limit does not erase the
underlying facts** — a separate non-temporal rule may still lawfully use them.
A naive implementation would treat a refused pair as evidence that nothing is
there, which would destroy lawful independent facts. That is the failure this
closes.

## 4. Time: polymorphism, not a fork

The withdrawn HQ201 `TIME-GRAIN-FORK` framing was **not** reinstated. Grain is
bound by exact `TEMPORAL_EVIDENCE` authority per rule and operation; the
substrate time ref is exact and grain-free. **No Astra referral is claimed.**

Exactly four order-basis kinds, jointly exhaustive for the required cases:

1. `CALENDAR_TOTAL_ORDER` — exact points or non-overlapping intervals
2. `FAMILY_LOCAL_ORDINAL` — only where specifically authorized
3. `PARTIAL_ORDER_NO_DIRECTION` — overlapping / partially ordered
4. `ORDER_UNKNOWN_NONCOMPARABLE` — unknown or non-comparable

Prohibited coercions: **overlap → midpoint**, **ordinal → calendar year**,
interval → point, label → ordinal, interpolation across a gap.

`WAVE_LABEL != ORDINAL != CALENDAR_YEAR` is preserved throughout.

## 5. The five functions were not collapsed

The commission warned against this. Four of the five are kept **out** of the
new kind on purpose:

| # | Function | Disposition |
| --- | --- | --- |
| 1 | persistent identity / comparable key | references existing form (`TEMPORAL_EVIDENCE`) |
| 2 | temporal observation | **separate** downstream producer |
| 3 | delta / comparison | **owned by `TEMPORAL_COMPARABILITY`** |
| 4 | rupture candidate | **separate** downstream producer |
| 5 | gap / absence | references existing form (general typed-absence law) |

A comparison authority that could mint identity could declare two different
things comparable. One that could constitute observations could author its own
evidence, destroying the independence that makes a delta meaningful. One that
could emit rupture could smuggle causal-adjacent power into a narrow grant.
Collapsing would have done all three.

## 6. Cardinality — a real tension, resolved

F7's must-not-revive list forbids "trajectory requires ≥3 anchors". This contract
asserts **two anchors suffice** for one ordered relation. These are compatible:
neither a ≥3 law nor a trajectory object is adopted, and two-anchor sufficiency
is about **one ordered comparison**, not trajectory composition. There is no
state for three-or-more. `TEMPORAL_INSUFFICIENT_ANCHORS` exists **only** for
fewer than two.

## 7. Trajectory, rupture, gap

- **Trajectory** — no object, no ≥3 rule, unconstituted. `DIFFERENCE != TRAJECTORY` binding.
- **Rupture** — typed candidate only, under exact authority, deliberately placed **outside** `TEMPORAL_RELATION_STATE`. No causal attribution, no V553 threshold imported, **no producer authorized**.
- **Gap** — `TEMPORAL_GAP_INTERVENING` preserves the span as typed unknown. `ABSENCE != ZERO`. No silent interpolation.

## 8. What this does **not** establish

**It does not establish that a lawful temporal comparison currently exists.**

No `TEMPORAL_COMPARABILITY` instance is authored. No observation is
time-indexed (`EmpiricalFact.REQUIRED_FIELDS` has no time field). No temporal
relation has been produced. A contract with no instance is the **expected**
outcome of this lane and must not be reported downstream as a capability.

## 9. Named gaps — none blocking

1. `IDENTITY_CONTRACT_INSTANCE_MISSING`
2. `TIME_INDEXED_OBSERVATION_OBJECT_ABSENT`
3. `TIME_REFS_CURRENTLY_EXACT_AND_GRAIN_UNVALIDATED` — grain lives in bound authority by design; a substrate grain enum is **not** recommended
4. `RUPTURE_CANDIDATE_PRODUCER_AND_CALIBRATION_AUTHORITY_UNCONSTITUTED`
5. `TEMPORAL_GAP_OBJECT_ABSENT__TYPED_SPAN_STATE_SUBSTITUTE`
6. `FAMILY_SCOPED_TIME_MAPPING_MATERIAL_UNADOPTED` — a generic evaluator cannot decide comparability here; the correct outcome is a typed refusal

## 10. Corrections recorded

- **H08 mis-citation.** `ABSENCE != ZERO` is binding, but citing the V553 gap/absence index as its current authority is wrong — the general typed-absence law at `pre553_empirical_objects.py:102-104,717-722` is. Conservation decision unaffected.

## 11. Verification

Tip verified exact · sparse worktree (`cone=false`) at the exact tip · 18-kind
closed set enumerated · all 7 reuse targets verified present ·
`TEMPORAL_NONCOMPARABLE` located and confirmed bare · SOURCE counterpart
confirmed produced · conserved V553/V554 limit semantics carried verbatim ·
withdrawn grain-fork confirmed not reinstated · all 8 JSON artifacts parse ·
change set contains no production file.