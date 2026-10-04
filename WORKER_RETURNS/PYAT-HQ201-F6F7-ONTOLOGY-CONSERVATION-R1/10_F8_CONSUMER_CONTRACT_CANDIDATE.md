# 10 — F8 consumer contract candidate

**Status:** `NEW_PROPOSAL_REQUIRING_HQ_ADOPTION`. Documentary candidate only. Nothing implemented.

**Name.** Not `POSITIONED_SOCIAL_WORLD_PACKET`. Field Forge §8 lists that name among proposals that "must not be
smuggled into current Rawlsing by the word 'contract' in a Field Forge filename", and it is self-marked
speculative. This contract is derived from HQD-125 §§3, 7 and 12 instead.

---

## O10 — What exactly should positioned-subject machinery consume?

**Not a point-in-time snapshot.** A snapshot would collapse
`POPULATION_FACT != POSITIONED_SUBJECT_POSSIBILITY != INDIVIDUAL_PREDICTION != V3_REALIZED_ACTOR_STATE` — all
four are binding (HQD-125 §3), and a snapshot invites reading a population field as a person state.

**A typed combination**, with each part carrying its own admissible use:

| component | admissible use at F8 | forbidden use |
|---|---|---|
| `source_local_slices` | conditioning possibility for a named source/universe | generalising across instruments without a portability admission |
| `composed_structural_propositions` | actor-independent structural constraints | reading as a personal attribute |
| `bounded_temporal_context` | situating a possibility in a declared interval | treating world time as memory, or a trajectory as a cause |
| `temporal_relations` (delta, directionality, persistence) | typed temporal characterisation of a *field* | inferring an individual's change from a field's change |
| `noncomparability_and_absence` | an explicit "not comparable / not observed" | reading absence as zero, or non-comparability as no-change |
| `contradiction_relations` | preserved plural structure | averaging to a single value |
| `uncertainty_ledger` | confidence and penalty on the possibility | collapsing a bounded distribution to a point |

The whole-PRÉ-V3 completion gate F8 (HQD-125 §12) is: *"the PRE-V3 system can expose possibility distributions
useful to parent/coparent and later person generation while preserving the actor firewall."*

---

## What F8 must receive as MANDATORY

F8 receives **possibility distributions**. Per HQD-125 §7:

> Parent/coparent priors remain **possibility distributions**. They are not persons, biographies, personalities,
> or V3 actor states.

And §7 is explicit that the intended service is *not* `DEMOGRAPHIC_PROFILE → INDEPENDENT_RANDOM_ATTITUDES`.

**MANDATORY INPUTS**

1. **source/universe provenance** — which source, which universe, which sealed release.
2. **positioned-subject possibility distribution** — a distribution over branches/configurations, not a point.
3. **declared conditioning basis** — the predictor/determinicity surface and its conditioning set.
4. **replay determinants** — so the possibility is reconstructible.
5. **actor-firewall marker** — every artefact carries `POPULATION_FACT`-level provenance.

**CONDITIONAL INPUTS** — present only when the corresponding authority exists, and marked as such:

6. bounded temporal context, with its anchor grain named;
7. temporal relations, where comparability authority exists — otherwise typed noncomparability;
8. cross-source composition relations, where `AUTHORIZED_COMPOSITE` was bound.

**REFUSED INPUTS** — the consumer must be structurally unable to accept:

| refused | law |
|---|---|
| any realized actor state / biography / personality | HQD-125 §3, §7 |
| a merged cross-source respondent row | HQD-125 §9 |
| a same-respondent jointness claim across sources | HQD-125 §9 |
| an unauthenticated averaged cross-source value | `SOURCE_CONFLICT != AVERAGE_BY_DEFAULT` |
| an interpolated period presented as an observation | `INTERPOLATION != OBSERVATION` |
| a causal attribution of a temporal break | zero causal authority in any evidence class |
| an individual-level "change" inferred from a field trajectory | `STRUCTURAL_WORLD_TIME != ACTOR_MEMORY`, `TRAJECTORY != CAUSAL_EXPLANATION` |

---

## The three confusions F8 must be structurally unable to make

These are where a positioned-subject consumer is most likely to collapse a distinction, so they are stated as
refusals rather than as guidance.

**1. Field trajectory ≠ individual trajectory.** A temporal relation is a property of a *field*, measured over
*survey waves*. A person is not observed in two waves of a repeated cross-section in the way a field is. Reading
one as the other is `STRUCTURAL_WORLD_TIME != ACTOR_MEMORY` collapsing.

**2. Field movement ≠ personal change.** Even for a genuinely longitudinal source, a wave-level delta is
evidence about a distribution, not about an individual. `DIFFERENCE != TRAJECTORY` at the field level;
`POPULATION_FACT != POSITIONED_SUBJECT_POSSIBILITY` at the person level.

**3. Uncertainty ≠ zero.** `allowed_uncertainty_states` is a first-class typed tuple on structural admission.
F8 must consume it, not floor it. An unresolved or non-comparable input yields an **unresolved possibility**, not
a confident one.

---

## Current implementation standing

`CURRENT_IMPLEMENTED_CAPABILITY`: `source_backed_positioned_subject_possibility.py` is the existing F8 seam and
is implemented; `m6_actor_safe_expression.py` owns the actor firewall and is implemented.

What is **not** available to F8 today, because the producers are missing (§`11`):

- bounded temporal context, anchors, deltas, directionality, trajectories — no producer exists;
- typed cross-source corroboration/contradiction relations — no owner exists;
- an enumerated disagreement policy — the slot is free text.

So the honest statement: **F8's consumer seam and firewall exist; F8's temporal and cross-source inputs do not.**
The contract above is what it *should* consume once those producers exist. Until then F8 can lawfully consume
source-local slices and composed structural propositions only.

---

## Required acceptance tests for any future F8 contract

Stated so they can be executed rather than admired:

1. **Firewall test.** No input artefact can yield a realized actor state, biography or personality. Refusal is
   structural, not advisory.
2. **Population-fact test.** A population field cannot be read as a positioned-subject attribute without a
   conditioning basis.
3. **Temporal-attribution test.** A field-level trajectory cannot be converted into an individual-level change
   claim.
4. **Uncertainty-preservation test.** An unresolved or non-comparable input cannot yield a confident output.
5. **Contradiction-preservation test.** Contradictory cross-source relations cannot be averaged into one value.
6. **Interpolation-honesty test.** An interpolated period cannot be presented as an observation.
7. **Replay test.** Every possibility output reconstructs from its declared replay determinants.
8. **No-pooling test.** No cross-source artefact can contain a merged respondent row.