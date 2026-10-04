# PYAT HQ203 — H-A F6/F7 corrected positive-constitution reconciliation — R1

**Disposition:** `F6_F7_CORRECTED_CONSTITUTION_PARTIAL__NAMED_POSITIVE_MEANINGS_REMAIN`

**Terminal:** `HQ203_HA_F6F7_CORRECTED_RECONCILIATION_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq203-ha-r1`
Commissioned startup SHA: `5cca96aeaa3fe5f2744203eac5b9a9eb2fb9de3c` — **verified equal**
Primary audit: `codex/prev3-terminal-backward-audit-r1 @ b3ea471a3771113bf408a4e434a4b480b26d5856`
HQ201 return reconciled: `d3f0619429a400552c2f3c397be57cdfbadb2f54`
Checkout: `SPARSE_REQUIRED` honored — no clone, no full worktree, sparse checkout not widened, **no production mutation**.

---

## What this lane is

**Reconciliation, not ontology design.** I took HQ201's F6/F7 return — which the audit registers
as an **unadopted worker return** (*"no HQ adoption located at control freeze"*) — and corrected it
against current adopted authority and the terminal-backward audit.

## The eight corrections

### 1. `SOURCE_INDEXED_MULTI_UNIVERSE` != `AUTHORIZED_COMPOSITE`

Verified directly in `pre553_empirical_query.py @ 1dcd7ff6`:

- **`SOURCE_INDEXED_MULTI_UNIVERSE`** iterates indices and calls `_evaluate_index_group((index,))`
  then `_build_fact((index,))` → **one fact per universe**. It never calls
  `_authorized_composite_refs`. OBL063: *"Executor returns one fact per universe; it does not pool
  sources."* **No pooling authority required.**
- **`AUTHORIZED_COMPOSITE`** calls `_authorized_composite_refs`, evaluates **all** indices and emits
  **one** fact. It requires an exact bundle binding `pooling` (`SOURCE_COMPOSITION_POOLING`),
  `nonduplication` (`SOURCE_UNIVERSE_RELATION`) and `estimand_composition`. OBL063: *"Blanket
  source-local pooling is not allowed."*

**Correction:** lawful cross-source coexistence without row pooling does **not** inherit a pooling
requirement merely because `AUTHORIZED_COMPOSITE` has one. HQ201's H02/H14 passages that treat
co-presence as requiring `AUTHORIZED_COMPOSITE` were conflating the two branches.

### 2. Field Forge — do not call adopted local forms exploratory

The audit states it directly: *"The exploratory W48 digest is not current status truth for Position
Role Authority, observability, relation-indexed geometry, and local geometry/estimand/mode law."*
W48/E52 self-declares `EXPLORATORY_NONBINDING` with ceiling `FIELD_FORGE_PROPOSAL != CURRENT_RAWLSING_AUTHORITY`.

All five subjects are governed by adopted R2/OBL law (E20–E27). Verified directly in `MATRIX.md`
lines 46–49: **W02–W05 all carry `AUTHORITY_FORM_CLOSED__POSITIVE_INSTANCE_OR_SCOPE_REMAINS`**
(blocker type *conditional*), and **X03** (strong homology/field/formation/hegemony/capital) is
`TERMINAL_NECESSITY_UNPROVED` (blocker type *no*).

**`STILL_EXPLORATORY` = 0 for all five.** The mode/form distinction is *adopted*; the strong
capital-value/conversion reading is *conditional*, requiring its own competent authority.

### 3. M1 ingress proves transport, not positive ontology

`m1_temporal_v554_admission_dedup.py` is a **fail-closed fingerprinted ingress/dedup seam**. It
defines three signatures and on any temporal signature requires
`REQUIRES_V553_OWNED_TEMPORAL_MEANING`. It carries
`rule_relevant_effective_time_semantics_fingerprint` — a fingerprint *of* a semantics that must
already exist. No V553 producer exists in the tree.

**I corrected my own initial over-claim here.** I first graded seven temporal items as
`POSITIVE_SEMANTIC_CONSTITUTION_STILL_NEEDED` on "M1 requires it and no producer exists". The audit
expressly forbids that inference:

> *"A missing implementation producer is not necessarily an owner gap; a named jurisdiction is not
> proof of derived positive ontology. Both stronger conclusions require the missing semantic test."*

So **seven** items are `UNKNOWN_PENDING_EXACT_EVIDENCE`, and exactly **one** is affirmatively
unconstituted — see §5.

### 4. Time grain is not the HQ201 binary

Not a universal point-year-versus-fieldwork-interval fork. The pre-V3 field is
`allowed_effective_time_or_interval_refs` — a tuple of `ExactRef`, naming **either** a point **or**
an interval, with **no grain enum anywhere**; the law constrains *authority* (`TEMPORAL_EVIDENCE`),
not grain. The V3 executor's actual affordance is `time_granularity` with observed values
**`INSTANT`** / **`INTERVAL`** — a different axis entirely. The grain is **rule-bound**, hence
source/operation-specific by construction.

Same-survey family membership proves nothing about point-year adequacy. **No Astra referral** — the
genuine residual is a *scope* question HQ can docket, not a high-consequence underdetermined fork.

### 5. Trajectory cardinality

*"Trajectory requires at least three anchors"* is **`UNSUPPORTED_STRENGTHENING`**. A repo-wide search
excluding HQ201 artifacts found the threshold only in the audit report *refuting* it and in the
HQ202 adjudication listing it as an open question. **Only `DIFFERENCE != TRAJECTORY` survives** as
binding: two differing observations do not by themselves constitute a trajectory or confer
directionality authority.

### 6. Cross-source relation — no new object family

The existing `pre553_source_relations.py` already carries **eight** relation kinds, each with its
own required material, positive authority kind, and an explicit `does_not_grant` tuple, under
`DISTINCT_BY_DEFAULT`. The four HQ201 kinds (corroboration / contradiction / complementarity /
mere_coexistence) are **descriptions of relations among already-representable per-universe facts**,
not new primitives. At most a typed annotation bound to a relation authority ref is needed — **not**
a new object family and not a broad relation vocabulary.

### 7. Disagreement — free text, averaging would pass

`source_disagreement_noncomparability_policy: str` is validated **only** as a non-empty string, and
is **not** passed through `_reject_forbidden_interpretation` (whose nine markers are all
agent/diagnostic markers — no AVERAGE/CONFLICT/DISAGREE/POOL). **An averaging policy string would
pass validation.** The query layer already refuses to average (pooling needs
`SOURCE_COMPOSITION_POOLING`), so the **minimum** requirement is narrow: type the disposition to
exact authority refs, default fail-closed, and route averaging only through the existing pooling
authority. No broad relation vocabulary.

### 8. World container and F8

A persistent `MultiSourceTemporalWorld` is **not required**. Adopted law declines a universal
carrier (E20: *"no universal geometry/world carrier"*; E21: *"optional local carriers not terminal
necessities"*), and **H09 itself already says so** (*"a persistent container is not required by any
binding law"*). F8/service-operation belongs to residual node **H-D** and is not decided here.

## What remains genuinely unbound

**Affirmatively unconstituted (1):** **authority for temporal directionality.** This is the one item
where the audit supplies a concrete semantic test rather than a gap — two waves *"do not
automatically confer directionality authority"* and no adopted authority establishes a threshold.

**Unknown pending the missing semantic test (8):** persistent temporal identity/comparable key;
temporal observation producer; positive temporal relation meaning; temporal delta; trajectory
constitution; rupture; gap/absence as first-class observation; typed cross-source relation kinds.

**Owned and implemented:** coexistence, no-implicit-pooling, typed noncomparability, source plurality
relations. **Slot/typing only:** operation-scoped comparability authority, disagreement enforcement.
**Not required:** the world container; generic strong nouns.

## Why this disposition

Not `…SUFFICIENT__ONLY_BOUNDED_OWNERS_OR_INSTANCES_REMAIN` — temporal directionality is
affirmatively unconstituted and eight items are UNKNOWN, not proven bounded. Not
`…ASTRA_PACKET_NEEDED` — the HQ201/HQ202 fork is withdrawn and the grain is rule-bound, so the
residual is a docketable scope question. Not `ARCHITECTURE_REOPEN_REQUIRED` — the audit found no
proved architecture gap. Not `MATERIAL_CONFLICT_IN_CURRENT_AUTHORITY` — the conflicts were between
**unadopted HQ201** and adopted law, resolved in favour of adopted law.

I sent **nothing** to Astra.

## Two corrections to my own work, recorded

1. The seven-item over-claim in §3, reversed to match the audit's discipline.
2. An initial 3/2 Field Forge split read from prose; direct verification of `MATRIX.md` showed a
   uniform `AUTHORITY_FORM_CLOSED__POSITIVE_INSTANCE_OR_SCOPE_REMAINS` across W02–W05, and I
   corrected to the matrix.

## Holds observed

No production mutation; no survey access; no live C4; no C7 or actor/person implementation; no
locator discovery; no warrant issuance; **no Astra referral**; no broad architecture reopen. Nothing
written outside the commissioned return directory.
