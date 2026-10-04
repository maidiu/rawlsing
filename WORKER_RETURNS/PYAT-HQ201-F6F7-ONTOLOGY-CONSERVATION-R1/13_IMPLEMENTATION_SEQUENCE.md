# 13 — Implementation sequence

**Status:** documentary proposal. No code was changed in this lane. Ordering is chosen so that each step is
lawful given its predecessors, and so that the one referred-out fork blocks as little as possible.

---

## Ordering principle

Two constraints fix most of the order:

1. **A producer must satisfy an ingress contract that already exists.** M1 already specifies the signatures,
   families and fingerprints a temporal producer must emit. So the temporal producer is *implementable now*
   without inventing a contract.
2. **Do not build what a fork would invalidate.** `TIME-GRAIN-FORK` governs cross-*family* temporal
   comparison only. Same-survey F7 (case A) is unblocked, because point-year is conservative and adequate
   within one family in one country.

---

## Step 0 — Refer out the one fork (do not wait on it)

**Owner:** HQ → Astra.
**Deliverable:** an answer to `TIME-GRAIN-FORK` — for multi-source comparison, does temporal identity key on a
point year or a fieldwork interval, and what typed noncomparability follows when intervals do not overlap?

Nothing else in this sequence is blocked by it. Steps 1–4 are all same-survey or non-temporal.

---

## Step 1 — Type the existing empty slots (smallest, highest leverage)

**Why first:** these slots already exist and are already validated; they are simply untyped. Typing them is
bounded implementation and it immediately makes three anti-collapse laws structural instead of textual.

| slot | module | change |
|---|---|---|
| `source_disagreement_noncomparability_policy` | `pre553_structural_admission.py` | enumerate the vocabulary; **refuse averaging by default**. Makes `SOURCE_CONFLICT != AVERAGE_BY_DEFAULT` structural. |
| `effective_period` | same | enumerate the lawful time grains, or type it to a referenced contract |
| `allowed_effective_time_or_interval_refs` | same | type the `ExactRef` set to a declared anchor contract |
| `time_geography_applicability` | same | type, or require a contract ref |

**Acceptance:** a caller supplying an averaging policy, or an untyped midpoint year, is **refused at
construction** — not accepted as free text.

**Closes:** part of the `disagreement policy` and `time_grain_vocabulary` gaps in
`11_CURRENT_OWNER_AND_MISSING_OWNER_MAP.json`.

---

## Step 2 — Conserve the functional half of V553 temporal identity

**Why:** this is *conservation*, not invention. The function is already proven and fail-closed; only the
topology is obsolete.

- **KEEP:** explicit family declaration; explicit wave identity; explicit calendar anchor obtained **without**
  treating a wave ordinal as a year; one anchor per period; fail-closed on family or country mixing.
- **DROP:** "exactly one survey family per report". Generalise to **one family per track**.
- **DROP:** the parquet/Arrow compiler, year-indexed tables, and the scalar `0.10` rupture coefficient.

**Acceptance:** a two-track, two-family input constructs successfully; a mixed-family *track* is still refused;
a wave ordinal is still never coerced to a year.

**Closes:** the `temporal identity / comparable temporal key` gap, in its candidate-blocker form
(`V553_TEMPORAL_KEY_CANDIDATE_INDEX_SCHEMA` + `V553_TEMPORAL_KEY_BLOCKER_INDEX_SCHEMA`).

---

## Step 3 — Produce temporal observations and relations to M1's existing contract

**Why now:** M1 is the fail-closed ingress gate and it already names the required families and fingerprints.

Produce, per track:

- `TEMPORAL_KEY` — a **candidate with a companion blocker**, never self-certifying;
- `TEMPORAL_OBSERVATION` — one anchored observation of a named object family;
- `TEMPORAL_RELATION` — one of the eight O2 relations, kept distinct.

Rules that are **not** optional:

- **directionality is an admission**, carrying `directionality_status` + `directionality_basis` +
  `directionality_coverage_status` (V551J's exact shape). A producer that cannot supply basis and coverage
  emits `noncomparability`, never a slope;
- a **trajectory requires ≥ 3 anchored points**;
- **gaps are typed unknowns**, never interpolated and never `anchor_copy`;
- **absences and non-comparabilities are recorded observations** with reason codes.

**Acceptance:** emitted objects satisfy M1 `SIG_002` / `SIG_003`; the court's negative cases pass — a
two-point input cannot produce a trajectory; an unestablished directionality produces `noncomparability`; a
missing anchor produces a typed gap, not a value.

**Closes:** the `temporal observation`, `temporal relation`, `temporal delta` and `temporal directionality`
gaps.

---

## Step 4 — Constitute rupture as a candidate, and refuse the causal step

**Why:** the distinction is cheap to get right now and expensive to retrofit.

- Emit **rupture candidates** (`V553_STRUCTURAL_RUPTURE_CANDIDATE_INDEX_SCHEMA`) plus a block audit. The word
  *candidate* is load-bearing.
- **Keep the event-override slot reserved and empty.** Every V553 row was `rupture_override_status:
  "reserved_not_filled"`. Conserve the slot; bind nothing. `interpolation_across_rupture_allowed` stays
  `False`.
- **No causal attribution.** `causal` occurs zero times in 4187 historical lines and no current law supplies
  it. Naming a cause requires new authority in a class that does not exist.

**Acceptance:** a detected discontinuity is classified `rupture_candidate`; no output type can express a cause;
the event-override slot is fillable only by a new explicit authority.

---

## Step 5 — Constitute the typed cross-source relation object

**Why:** lawful coexistence is implemented; typed corroboration/contradiction is not, and composition case F
(conflicting temporal movement across sources) cannot complete without it.

`NEW_PROPOSAL_REQUIRING_HQ_ADOPTION`. Carries `{relation_kind, proposition_ref, per_source_fact_refs,
authority_ref, unresolvedness}` and **must not reduce to a scalar**.

**Acceptance:** two contradicting source-indexed facts can be related as `contradiction`; no API path can average
them; a `mere_coexistence` relation cannot be promoted to `corroboration` without new authority.

---

## Step 6 — Compose F6 × F7 (only after 3–5)

Cases C, D and F. **Blocked on step 0** for case C's cross-family interval comparison; D and F are unblocked.

**Acceptance:** two tracks from two families compose into one world; case G holds — a blocked temporal relation
does not contaminate lawful cross-source coexistence.

---

## Step 7 — Bind the F8 contract

Only after 5–6, so F8 is not specified against inputs that do not exist. Implement the eight acceptance tests in
`10_F8_CONSUMER_CONTRACT_CANDIDATE.md`, especially the firewall, temporal-attribution, uncertainty-preservation
and no-pooling tests.

---

## Explicitly NOT in this sequence

- **any world-container persistence build.** No binding law requires one; assembling per query result is
  lawful and building one pre-emptively would be inventing architecture;
- **any Field Forge product family** (`POSITIONAL_PRESSURE_FOOTPRINT`, `POSITION_GEOMETRY_FAMILY`,
  `DISPOSITION_GEOMETRY_ATLAS`, `POSITIONED_SOCIAL_WORLD_PACKET`) — self-marked speculative;
- **any interpolation capability** until a binding authority and a non-obsolete method exist;
- **any scalar pressure formula** inherited from V553's `0.10` coefficient;
- **any causal attribution capability**;
- **any actor/person implementation** — the PRE-V3→V3 seam remains deliberately deferred, and `m6` owns the
  firewall this lane did not touch.

---

## Dependency summary

```text
Step 0 (Astra fork) ── blocks only case C cross-family interval comparison
Step 1 (type slots) ── independent; highest leverage per line of change
Step 2 (conserve identity) ── independent of Step 1
Step 3 (temporal producers) ── needs Step 2; M1 contract already exists
Step 4 (rupture, no causal) ── needs Step 3
Step 5 (cross-source relation) ── independent of Steps 2-4
Step 6 (F6 x F7 composition) ── needs Steps 3, 4, 5
Step 7 (F8 contract) ── needs Steps 5, 6
```

Steps 1, 2 and 5 are mutually independent and can proceed in parallel. **No step requires reopening
architecture.**