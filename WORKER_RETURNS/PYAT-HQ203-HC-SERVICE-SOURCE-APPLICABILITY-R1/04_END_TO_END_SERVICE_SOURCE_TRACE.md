# 04 — End-to-end service-source trace

**Request.** *"Give the positioned-subject possibility distribution for target T, population P, geography G, effective time X."*

The trace below follows what current law can actually do, in execution order, with the owner named at each step.
It is written to be checked rather than admired: each step either names an owner or names the gap.

---

## What D15 required

`SERVICE_SOURCE_APPLICABILITY_AUTHORITY`, from the D15 ledger at `09ea040ac`:

| field | content |
|---|---|
| jurisdiction | Separately admits respondent universes for **forward discovery**, **reverse possibility inference**, and **structural empirical admission** |
| why_required | source relevance/admissibility can differ by terminal service, and **locality alone does not choose a source** |
| upstream_inputs | EmpiricalUniverse identity; **service**; target question/coordinate/structural use; **time/geography/population scope** |
| downstream_outputs | **admitted source-indexed universe list** *or* **typed nonapplicability/noncomparability** |
| prohibited | may not silently backfill broader sources; may not average admitted universes; may not imply respondent linkage or pooling |
| implementation_dependency | **Per-service source applicability registry/resolver** |

D12G (adjudication at `931b3086d`) independently established the rule it implements:

> `ACCEPTED__DISTINCT_UNIVERSES_BY_DEFAULT__SOURCE_INDEXED_COMPOSITION__EXACT_AUTHORITY_REQUIRED_FOR_JOIN_POOLING_BACKFILL`

and, decisively:

> "each source/universe requires **independent service-specific applicability authority**"
> "**locality or country identity alone does not assign a priority weight**"

and named the three terminal services whose meaning/use differs: *forward discovery, reverse positioned-subject
possibility inference, structural-field production, or no promoted use.*

---

## The trace

### Step 1 — Bind the service request → **NO OWNER**

The historical input set requires a **service** and a **target use**. Current law has no object that accepts
them.

- `EmpiricalQuerySpec.REQUIRED_FIELDS` = `target_refs`, `target_arity_and_topology`, `condition_predicate_ref`,
  `risk_set_ref`, **`empirical_universe_refs`**, `scope_refs`, `measure_basis_ref`, `requested_output_grain`,
  `query_authority_refs`.
- There is **no `service` field**.
- `empirical_universe_refs` is a **caller-supplied required field**, and `_validate_family` raises
  `"EmpiricalQuerySpec requires exact source universe scope"` when it is empty.

The universe set is an **input to the request, not an output of an applicability decision**. The trace cannot
even *begin* at "given this service request", because no component is parameterised by service.

**Owner: none. This is the gap.**

### Step 2 — Derive the admissible sources → **NO OWNER**

Nothing consumes `(service, target use, time/geography/population)` and emits an admitted-source determination.

- `pre553_source_local_universe_admission.py`, the closest current analogue, states in its own docstring:
  > "**The contract does not infer source authority.** It validates a caller-supplied positive exact
  > `AuthoritySnapshot` and materializes only at that authority's source-local ceiling."
- `AuthorityRegistry` is described as an *"Immutable exact-key authority registry; **no latest/default lookup
  exists**."* An exact-key registry structurally cannot answer "which source applies to this request?" — it can
  only answer "give me the authority filed under this exact key."

A per-service resolver needs precisely the derived lookup `AuthorityRegistry` deliberately refuses. **The
historical `Per-service source applicability registry/resolver` has no counterpart anywhere in the tree.**

Whole-tree census confirms the absence at the concept level: `source_applicability` and `service_source` occur in
**18 files**, and **none** is in `rawlsing_next` and **none** is in an adopted Field Forge / OBL authority. They
are 2 historical DDM data artifacts (the D15 provenance chain itself), 7 old `HQ_HANDOFF` checkpoints, 8 documentary
Astra atlas/binding indexes, and this commission.

### Step 3 — Assemble a source set → **CALLER-SUPPLIED**

The caller supplies `empirical_universe_refs`. Each must resolve in **exactly one** supplied sealed C11 release.

This step is real work and it is valid. It is simply not selection.

### Step 4 — Validate the set → **PROVED, OWNED**

| check | owner | behaviour |
|---|---|---|
| universe resolves to exactly one release | `pre553_empirical_query.py` | fails closed |
| positive exact `AuthoritySnapshot` | `pre553_source_local_universe_admission.py` | fails closed |
| relation kind positively authorised | `pre553_source_relations.py` | fails closed; **no relation kind implies another** |
| provenance / harmonization labels grant nothing | `pre553_source_relations.py` | `NONAUTHORIZING_RELATION_KINDS = {PROVENANCE_ORIGIN, HARMONIZATION_ALIAS}` |

This is genuine, well-built capability. It is **validation**.

### Step 5 — Refuse inadmissible sources → **PARTIAL**

It **can** refuse a supplied universe that does not resolve, lacks positive authority, or proposes an
unauthorised relation.

It **cannot** determine that a source should never have been supplied — because inapplicability is never
*determined*. `SOURCE_NOT_APPLICABLE` / `NOT_APPLICABLE` exist as typed states a caller may **declare**, and
`FORBIDDEN_BACKFILL_TARGET_STATES` (`DECLARED_NONE`, `SOURCE_NOT_APPLICABLE`, `TEMPORAL_NONCOMPARABLE`,
`OBSERVED_ZERO`, `ZERO_SUPPORT`, `NONCOMPARABLE`, `NOT_APPLICABLE`) structurally prevents backfill from
overwriting them.

So the *protection* of a declared non-applicability is enforced. The *derivation* of one is absent. Those are
different things, and conflating them would repeat exactly the error this audit exists to prevent.

### Step 6 — Compose multiple sources under exact authority → **YES, OWNED**

`AUTHORIZED_COMPOSITE` requires an operation-scoped bundle binding three roles:

| role | required authority kind |
|---|---|
| `pooling` | `SOURCE_COMPOSITION_POOLING` |
| `nonduplication` | `SOURCE_UNIVERSE_RELATION` |
| `estimand_composition` | `SOURCE_COMPOSITION_POOLING` + `WEIGHT_DESIGN_ESTIMAND` |

plus the `pre553_source_relations.py` I07 composite guard and `SourceUniverseRelation` receipts
(`RESPONDENT_LINKAGE`, `OVERLAP_NON_DUPLICATION`, `SAMPLE_POOLING`, `ESTIMAND_COMPOSITION`, `BACKFILL`).

**Per HQ203's recalibration, `AUTHORIZED_COMPOSITE` and `SOURCE_INDEXED_MULTI_UNIVERSE` are separate branches.**
This trace does not conflate them. `SOURCE_INDEXED_MULTI_UNIVERSE` evaluates each universe separately and yields
source-local facts; it does not inherit a pooling requirement. `AUTHORIZED_COMPOSITE` separately validates
pooling/nonduplication/estimand authorities.

Note the design worth preserving: composing across sources requires *positively binding* a
`SOURCE_COMPOSITION_POOLING` authority. Pooling is a power that must be granted, not a default to avoid.

### Step 7 — Record why each source was selected → **NO OWNER**

Execution receipts record **what was run**, not **why a source was admitted**. There is no selection-reason
field, because no selection occurred. This is a faithful consequence of steps 1–2, not an independent oversight.

### Step 8 — Distinguish "no applicable source" from "missing data inside an applicable source" → **PARTIAL**

The typed states exist and are protected from backfill (step 5). What does not exist is anything that
*computes* "no applicable source" from the request. A caller may declare it; the system respects and protects
the declaration; nobody derives it.

### Step 9 — Produce the positioned-subject possibility distribution → **OWNED, DOWNSTREAM**

`source_backed_positioned_subject_possibility.py` is the consumer seam, with `m6_actor_safe_expression.py`
owning the actor firewall. It consumes source-local products — which is correct, because selecting those
products was never its job.

---

## Where the chain actually breaks

```text
(service, target T, population P, geography G, time X)
        │
        ▼
   ╔══════════════════════════════════════════════════════╗
   ║  MISSING — no applicability authority, no resolver   ║
   ║  D15 SERVICE_SOURCE_APPLICABILITY_AUTHORITY           ║
   ║  D12G: "independent service-specific applicability    ║
   ║         authority"; "locality alone does not choose"  ║
   ╚══════════════════════════════════════════════════════╝
        │  (caller supplies a source set instead)
        ▼
   validate supplied set ── PROVED, owned
        ▼
   compose under exact authority ── PROVED, owned
        ▼
   produce possibility distribution ── PROVED, owned
```

The chain does not fail at any implemented step. It has **no first link**. Three consecutive capability
segments are proved and owned, and they begin from an input nobody was authorised to produce.

---

## The precise statement

**Selection is caller-supplied today.**

The current system validates the caller's source set with real, fail-closed, non-collapsing discipline. It does
**not** authorise, derive, rank, or record the selection of sources for a service request. Those are different
capabilities, and this audit does not equate them anywhere.

The gap is bounded and does not require architecture reopening. It requires authoring an **authority form** —
per-service applicability, decided independently per source, consulted *before* a service assembles its set, and
non-substitutable by the relation powers that are already implemented.