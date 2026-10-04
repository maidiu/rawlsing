# HQ203-R1 Return — H-C service-source applicability authority reconciliation

**Disposition:** `SERVICE_SOURCE_APPLICABILITY_FORM_MISSING__BOUNDED_CONTRACT_REQUIRED`
**Branch:** `agent/rabochii-pyat-hq203-hc-r1`
**Startup SHA (verified exact):** `9967f939a44628ddea624818f5dda31a82662dee`
**Documentary base:** `15018a303078cbcd867b08d39ed6b66e14d325fb`
**Primary audit:** `codex/prev3-terminal-backward-audit-r1 @ b3ea471a3771113bf408a4e434a4b480b26d5856`
**Checkout mode:** `SPARSE_REQUIRED` — sufficient. No clone, no full checkout. No production mutation.

---

## The answer, stated plainly

**Current Rawlsing VALIDATES a caller-supplied source set. It does not authorise, derive, rank, or record the
selection of sources for a service request. Selection is caller-supplied today.**

This is not an inference from absent documentation. Four independent current-code facts establish it:

1. **The concept is absent.** Whole-tree census: `source_applicability` and `service_source` occur in 18 files —
   and **none** is in `rawlsing_next`, **none** in any adopted Field Forge/OBL authority. They are 2 historical
   DDM artifacts (D15's own provenance chain), 7 old checkpoints, 8 documentary indexes, and this commission.
2. **The universe set is a caller-supplied required field.** `EmpiricalQuerySpec.REQUIRED_FIELDS` includes
   `empirical_universe_refs`, and raises `"EmpiricalQuerySpec requires exact source universe scope"` when
   empty. There is **no `service` field**.
3. **The nearest current module disclaims inference in its own docstring.**
   `pre553_source_local_universe_admission.py`: *"The contract does not infer source authority. It validates a
   caller-supplied positive exact AuthoritySnapshot."*
4. **The registry cannot answer the question.** `AuthorityRegistry` is *"Immutable exact-key authority registry;
   **no latest/default lookup exists**."* A per-service resolver needs exactly the derived lookup it refuses.

## What D15 required, and D12G independently established

`SERVICE_SOURCE_APPLICABILITY_AUTHORITY` had **service** and **target use** as required upstream inputs, and
emitted an **admitted source-indexed universe list or a typed nonapplicability**. Its implementation dependency
was a **"Per-service source applicability registry/resolver"** — no counterpart exists in the tree.

D12G states the rule directly: *"each source/universe requires **independent service-specific applicability
authority**"* and *"**locality or country identity alone does not assign a priority weight**"*, under
`ACCEPTED__DISTINCT_UNIVERSES_BY_DEFAULT__…`.

## The eleven powers, held apart

Nine of eleven are **proved or partial**. The two that are missing are precisely the two that would let a service
request *derive* and *choose*:

| power | status |
|---|---|
| identity · semantic equivalence · linkage · overlap · pooling · estimand composition · backfill | **PROVED** |
| service applicability · **source selection/ranking** | **MISSING — no owner** |
| currentness · consumer-use permission | PARTIAL |

Critically, **nothing collapsed into the hole** — which is correct behaviour. `pre553_source_relations.py` states
*"No relation kind implies another"*, and `NONAUTHORIZING_RELATION_KINDS` makes provenance and harmonization
labels descriptive only. The D15 ledger's separation of applicability from relation is **honoured**: relation
powers did not absorb applicability, and applicability was not quietly dropped into validation.

D15's prohibition *"may not silently backfill broader sources"* also survives structurally —
`FORBIDDEN_BACKFILL_TARGET_STATES` includes `SOURCE_NOT_APPLICABLE`, `NOT_APPLICABLE`, `OBSERVED_ZERO`.

## A–F, with owners

| | question | answer | owner |
|---|---|---|---|
| A | derive admissible sources | **NO** | none |
| B | refuse inadmissible sources | **PARTIAL** | query + admission + relations modules — refuse a *supplied* source; cannot determine one should never be supplied |
| C | choose among admissible | **NO** | none — accepts a set, emits per-source facts |
| D | compose under exact authority | **YES** | `AUTHORIZED_COMPOSITE` + `SourceUniverseRelation` receipts + I07 guard |
| E | record why each source was selected | **NO** | none — receipts record what ran, not why admitted |
| F | "no applicable source" vs "missing data inside one" | **PARTIAL** | typed states exist and are non-backfillable; nothing *computes* them |

## The judgement call I want to flag

I rejected `SERVICE_SOURCE_APPLICABILITY_PARTIAL__NAMED_OWNER_OR_AUTHORITY_MISSING`, the closest alternative,
on a precise distinction: **partial coverage requires the applicability decision to be taken somewhere with only
the derivation missing.** It is taken nowhere. The sole overlap is a caller-*declarable* state vocabulary
(`SOURCE_NOT_APPLICABLE` / `NOT_APPLICABLE`) — and **a shared word is not a shared function**. Declaring a state
on a source you already chose is not determining which sources are admissible.

That is why the disposition is **form** missing rather than **owner** missing: there is no applicability object,
no applicability relation kind, no service-scoped resolver, no selection-reason record, and no service parameter
on any input surface. The authority form itself is absent and must be *authored* before it can be implemented.

## One scope note

The commission's *"adopted comparator at E30"* did not resolve as an identifier anywhere in `rawlsing_next` or
`PYAT_CONTROL_ROOM`. The current tree carries the OBL031 Q69B comparator lineage
(`gt34_obl031_q69b_comparator_resolver_r4.py`), which closes an exact-type/grammar-binding seam for one named
comparator — not a service-source resolver. Recorded as a scope note, not a claim that E30 was located.

## HQ203 supersession observed

Per the recalibration, I have **not** re-imported my HQ201 claims: no F6/F7 ontology claim is made here, and the
HQ201 `SOURCE_INDEXED_MULTI_UNIVERSE` / `AUTHORIZED_COMPOSITE` mode conflation is explicitly **not** repeated —
they are treated as separate branches.

## Bounded, and does not need architecture reopening

The required contract needs five things: an applicability decision object binding
`(service, target use, scope) → (admitted source-indexed universes) | typed nonapplicability`; an **independent
decision per source per service**; a grain that composes with — and cannot be satisfied by — the relation powers;
a selection-reason receipt; and D15's prohibitions carried verbatim.

Nothing here requires new architecture. It requires a new authority form at a grain the DAG already has an
exact-key pattern for, plus a resolver that performs the derived lookup `AuthorityRegistry` deliberately refuses.

## Artifacts

`00_RETURN.md` · `01_HISTORICAL_SERVICE_SOURCE_AUTHORITY.json` · `02_CURRENT_SUCCESSOR_CENSUS.json` ·
`03_POWER_NONCOLLAPSE_MATRIX.json` · `04_END_TO_END_SERVICE_SOURCE_TRACE.md` ·
`05_ADOPTION_EQUIVALENCE_DECISION.json` · `06_MISSING_OWNER_OR_INSTANCE.json` · `07_FINAL_DISPOSITION.json`

No production mutation, no raw-source access, no locator discovery, no warrant issuance, no live C4, no C7, no
actor/person implementation, no broad architecture reopen.

`HQ203_HC_SERVICE_SOURCE_APPLICABILITY_RETURNED__HQ_ADJUDICATION_REQUIRED`