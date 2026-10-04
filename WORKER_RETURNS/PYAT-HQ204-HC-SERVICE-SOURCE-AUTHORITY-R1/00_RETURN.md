# HQ204-R1 Return — Service-source applicability authority-form derivation

**Disposition:**
`SERVICE_SOURCE_APPLICABILITY_ADMISSIBLE_SET_AUTHORITY_FORM_DERIVED__RANKING_NOT_AUTHORIZED__NO_ARCHITECTURE_REOPEN__AWAITING_HQ_RATIFICATION`

**Branch:** `agent/rabochii-pyat-hq204-hc-r1`
**Startup SHA (verified exact):** `b65673abc13916963770d6d74ae51fe882539b70`
**Adjudication applied:** `ff4f06954824a3a5699bc5c1c9bd68cb3c5b4146`
**H-C forensic return read:** `cd3809efda80d64a590b1876a22eb6d08d09a079`
**Terminal-backward audit:** `b3ea471a3771113bf408a4e434a4b480b26d5856`
**Checkout mode:** `SPARSE_REQUIRED` — sufficient. No clone. No full checkout. **No code changes.**

---

## The answer, stated plainly

**The lawful current function returns an ADMISSIBLE SOURCE-INDEXED SET with typed per-source states.
It does not rank, score, order, weight, or select.**

This is not the conservative default. It is what the authority actually says, and it is the *least powerful* form
supportable — which is what the commission required.

Three independent grounds, any one of which is sufficient:

1. **D15's output is a set, not an order.** `downstream_outputs` reads
   *"admitted source-indexed universe list or typed nonapplicability/noncomparability."*
   Across all eight ledger fields there is no comparator, no score, no position, and no preference key.
   **"List" is not "ranking."** It fixes that the output enumerates admitted members; it fixes no order, because
   the ledger supplies none.

2. **D12G expressly withheld ranking.** Verbatim:
   > *"No statistical composition model or numeric source weighting is selected."*

   Ranking weights are not merely *omitted* from the record. The adjudicator that established the applicability
   rule **affirmatively declined to select one**. Inventing one now would not recover D15/D12G — it would
   contradict them.

3. **Locality was specifically denied the one plausible ranking signal.** Verbatim:
   > *"locality or country identity alone does not assign a priority weight."*

   Geography is an **inclusion filter**. It can remove a candidate. It can never promote, order, or weight one.

Add D12G's *"each source/universe requires independent service-specific applicability authority"* and the structure
closes: independent per-source judgements yield a **set**. An order over them is a **cross-source relation**, which
would collapse power 8 into the relation grain and destroy D15's own two-row separation.

Current law agrees and offers nothing to inherit: `AuthorityRegistry` is
*"Immutable exact-key authority registry; no latest/default lookup exists"*, and `AuthoritySnapshot._validate_family`
rejects `LATEST, DEFAULT, FUZZY, NEAREST, SEMVER_FALLBACK` — *"mutable/fuzzy authority selection is forbidden."*

**The substantive change of this lane:** H-C answered question C with **"NO — no selector, ranker or preference
order exists."** That was *true by absence*. It is now **no on the record, by authority** — and structurally
unreachable, because the derived object has no ordering field, no ranked state, and no preference in its decision
precedence. Ranking could not be added to it without a **new authority**, not a field addition.

---

## What I found that H-C did not, and one thing I corrected

**A same-grain precedent exists.** `pre553_structural_admission.py` implements `STRUCTURAL_EMPIRICAL_ADMISSION_AUTHORITY`
— the **immediate D15 sibling row** — at exactly this grain and in exactly the idiom this form needs:
`DECISION_PRECEDENCE` (integrity → missing authority → unknown/conflicting → denied → … → admitted),
`POSITIVE_DECISION`, `PUBLIC_STATE_BY_DECISION`, and a `DECISION_MATRIX` of per-state power flags.

That is why this derivation is *authority materialization by lawful analogy to an adopted sibling*, not invention,
and why §15's remedy clause — *"implementation, authority materialization, composition or qualification"* — names
precisely the right medicine.

**H-C MISS-04 restated (JC-05).** H-C recorded *"no record exists of WHY a source was selected."* On derivation, the
correct finding is sharper: **there is nothing to record, because no selection occurs.** Recording a reason for a
choice the authority forbids would either fabricate a selection or misrepresent an independent per-source
determination as a comparative judgement. What *is* required is **admission provenance** — which exact authority
admitted this source for *this* request — and it is strictly weaker.

**A provenance finding.** `09ea040ac` (D15 ledger) and `931b3086d` (D12G adjudication) are **not ancestors of
`b65673abc`**. The D15 CSV and D12G markdown are not in the current tree at those paths. I recovered both texts from
the object store at their exact commits, and separately verified that the D15 *court result* does survive inside
current control through the N006 corpus carrier — which records court D15, the ledger filename, the three
`binding_terminal_services`, and `source_indexed_default: true` / `source_pooling_default: false`.

This is exactly why blind topological restoration would have been wrong twice over: the commits are off-lineage,
*and* the stage-era component shape ("a per-service registry/resolver as a distinct component") is not what current
law's grain idiom looks like. The function had to be recovered **semantically**.

---

## The derived form

**Grain.** Exactly one decision per `(service_request_key, source_universe, release_identity)`. Never a set-level
verdict. One request key yields **N independent per-source decisions**, per D12G.

**The service-request key — all ten components, or a terminal refusal:**

| # | component | note |
|---|---|---|
| 1 | `service_id` | the three D15 terminal services, or `NO_PROMOTED_USE` |
| 2 | `service_authority_ref` | positive exact `AuthoritySnapshot` |
| 3 | `target_use_ref` | target question / coordinate / structural use (+ arity/topology) |
| 4 | `population_scope_ref` | **inclusion filter only** |
| 5 | `geography_scope_ref` | **inclusion filter only** |
| 6 | `effective_time_or_interval_ref` | declared basis, **never normalised** |
| 7 | `candidate_class_ref` | positively bounded — see below |
| 8 | `release_identity_ref` | per source; no inheritance by resemblance |
| 9 | `target_use_permission_refs` | **binds** the envelope; does **not** grant permission |
| 10 | `candidate_source_universe_refs` | resolved **from** the bounded class, not freely supplied |

**On component 7 (JC-01, JC-06).** `candidate_class_ref` was not in the commission's enumeration. I included it
because it is the structural implementation of D15's own prohibition *"May not silently backfill broader sources."*
Without a positively bounded class, the "admissible set" degenerates to *all sources*, which is not an admission
decision at all — and the silent broadening is precisely where that prohibition bites. It needs HQ ratification.

**Decision precedence** (ordered so a higher refusal can never be reported as a lower state):

```
INTEGRITY_FAILURE
MISSING_APPLICABILITY_AUTHORITY
UNKNOWN_OR_CONFLICTING_APPLICABILITY_AUTHORITY
REQUEST_KEY_INCOMPLETE_OR_AMBIGUOUS
SOURCE_OUT_OF_DECLARED_SCOPE
SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE
SOURCE_NONCOMPARABLE_AT_THIS_TARGET
NEGATIVE_AUTHORITY_ONLY
UNDETERMINED_NO_POSITIVE_AUTHORITY
ADMITTED
```

**Per-source public states:** `APPLICABLE · NOT_APPLICABLE · NONCOMPARABLE · OUT_OF_SCOPE · MISSING_AUTHORITY ·
UNRESOLVED · INTEGRITY_FAILURE`

**A new `SERVICE_SOURCE_APPLICABILITY_STATE` family is mandatory (JC-02).** `NOT_APPLICABLE`, `NONCOMPARABLE` and
`OUT_OF_SCOPE` each already appear in *more than one* existing `STATE_FAMILY` at `b65673abc`. Aliasing would make an
applicability refusal indistinguishable from a relation refusal and destroy D15's separation **in the type system**.
The sibling module already models the fix: keep the exact decision vocabulary, coarsen explicitly via a
`PUBLIC_STATE_BY_DECISION` map.

**Outcomes:**

- `ADMISSIBLE_SOURCE_INDEXED_SET` — positive. Entries remain **separate**; cardinality is not a sample size.
- `NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS` — a **first-class success**, not an error, not an empty list, carrying the
  bounded class and per-candidate reason for **every** candidate.
- Refusals: `SERVICE_REQUEST_UNDETERMINED` · `SERVICE_AUTHORITY_UNDETERMINED` · `APPLICABILITY_AUTHORITY_CONFLICT`
  · `CANDIDATE_CLASS_UNBOUNDED`.

`candidate_class_coverage` (`COMPLETE` / `INCOMPLETE`) is **mandatory** — without it, an under-examined class
masquerades as a fully decided set.

---

## The distinction the commission insisted on, structurally enforced

**`APPLICABILITY_PREDATES_EVIDENCE`.** Applicability is decided at source-universe, scope and use grain, **before**
any internal evidence is examined. The decision object therefore carries **no evidence-sufficiency field**.

- **No applicable source** → request-grain, first-class, *successful*. A statement about **sources**. Never about
  evidence volume.
- **Applicable source with missing internal evidence** → per-source `APPLICABLE`, *followed by* a downstream
  `ZERO_SUPPORT` / `OBSERVED_ZERO` / `LOW_SUPPORT` / `UNCERTAINTY_UNQUANTIFIED` / `UNAVAILABLE`, owned by
  `pre553_empirical_query.py`.

Different grains, different state families, never interchangeable:

```
APPLICABLE_SOURCE        != SOURCE_WITH_EVIDENCE
NO_ADMITTED_SOURCE      != NO_EVIDENCE_FOUND
MISSING_AUTHORITY       != NOT_APPLICABLE
OUT_OF_SCOPE            != NOT_APPLICABLE
NONCOMPARABLE           != NOT_APPLICABLE
ADMITTED_SOURCE         != POOLED_SAMPLE
ADMITTED_SET            != COMPOSITE_ESTIMAND
```

This upgrades H-C's question F from **PARTIAL** to **FORMED**.

---

## Fail-closed, no backfill, no pooling, no silent ranking

Ten fail-closed rules (FC-01…FC-10). The load-bearing ones:

- **No key → no set.** Not even a partial one. No default, nearest, or best-effort.
- **Conflict → refuse.** Never pick the newest, nearest, or highest version. Version proximity is not a tie-break.
- **Undecided ≠ refused.** An undecided candidate is surfaced as `UNDETERMINED_NO_POSITIVE_AUTHORITY` with
  `candidate_class_coverage = INCOMPLETE`. **Omitting it would fabricate a finding**; emitting a set while hiding it
  would falsely claim coverage.
- **Silence is never a verdict.** Without a positive negative authority the state is `MISSING_AUTHORITY` — never
  `NOT_APPLICABLE`. Absence of evidence of applicability is never evidence of inapplicability *or* of applicability.
- **No silent backfill.** This form's own states join `FORBIDDEN_BACKFILL_TARGET_STATES`. `APPLICABLE` may never be
  produced by default, inheritance, family membership, version proximity, currency, or absence of a negative.
- **No pooling.** The function is a *decision* function, not a *combining* function. No union, merge, weight,
  combined denominator, or combined estimand. Composition stays in `pre553_source_relations.py`, untouched.
- **No locality priority.** No local source preferred to a non-local one; absence of a local source may not promote
  a non-local one; and there is no tie-break, **because there is no order**.

**Determinism.** Pure function of the exact key plus exact registered authorities. Wall-clock time, iteration order,
dict order, and caller array position are **non-determinants**. Where the outcome is a set, entries are canonically
sorted on `(source_universe_ref, release_identity_ref)` for replay reproducibility **only** — and the receipt must
say that this order carries no ranking, preference, priority or weight authority.

---

## The F8 boundary

**Eligibility only.** Everything else refused: conditioning · possibility-geometry transformation ·
probability/distribution transformation · respondent pooling · individual inference.

**The trap this closes.** F8 selects geometry by exact `(source_universe, release, target, retained_conditioner_ids)`
match over **pre-materialized** slices. So narrowing eligibility **can** change what F8 returns — and an implementer
could easily mistake that for a transformation power. It is not. **Output selection is not output transformation.**
This form can cause a different already-materialized slice to be selected; it cannot create, reshape, reweight,
smooth, renormalise, or extend any geometry or distribution.

Per H-D as accepted by HQ204: `F8_DOES_NOT_TRANSFORM_POSSIBILITY_GEOMETRY`;
`MODEL_ALGORITHM_ID is EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION`;
`GEOMETRY_TRANSFORMER` and `DISTRIBUTION_TRANSFORMER` are `NOT_AVAILABLE_AT_F8` for any world input family. Every
refusal bound here is **already forbidden or already structurally unavailable**, so this binding requires no F8
architecture change.

---

## HQD-125 §15 — architecture reopen NOT warranted

Six conditions, **conjoined**. Two hold; **four fail**, two of them decisively.

| condition | holds? |
|---|---|
| has no lawful current representation | **yes** |
| has no owner | **yes** |
| cannot be transported | **no** — D15's citation is already carried in current control via the N006 corpus carrier |
| cannot be validated/refused | **no** — refusable at ten points on the existing validated substrate |
| cannot be composed at the required grain | **no** — a strict refinement of the existing semantic-field grain |
| cannot be satisfied by same-grain succession or bounded implementation | **no** — the immediate D15 sibling is already implemented at this grain and idiom |

Four of six fail. The remedy §15 names — *"authority materialization"* — is exactly right.

This **confirms** HQ204's H-C adjudication that this is a missing authority **form** at an already-lawful grain, and
supplies the half H-C correctly declined to author.

---

## H-C questions A–F, then and now

| | question | at H-C | now |
|---|---|---|---|
| A | derive admissible sources | NO — no owner | **FORM DERIVED** — admissible set, per-source typed states, ten-component key, independent decisions. Ranking still refused. Not implemented. |
| B | refuse inadmissible sources | PARTIAL — refuses a *supplied* source | **FORM DERIVED** — refusal now *derived* at applicability grain with precedence and provenance, rather than caller-declared. The distinction from power B proper is preserved. |
| C | choose among admissible | NO — by absence | **STILL NO — by authority.** D12G expressly withheld weighting; the object has no ordering field. |
| D | compose under exact authority | YES | **YES** — unchanged, untouched. |
| E | record why selected | NO — no selection occurred | **RESTATED** — nothing to record; admission provenance required instead. Strictly weaker. (JC-05) |
| F | no-applicable-source vs missing internal evidence | PARTIAL | **FORMED** — first-class request-grain outcome + `APPLICABILITY_PREDATES_EVIDENCE`. |

---

## Verification note

Every current-code citation was re-checked **by me at `b65673abc`** — not inherited from H-C's startup
`9967f939`. Absence census at my SHA: `source_applicability` **0 files**, `service_source` **0**,
`source_eligibility` **0**, `source_allowlist` **0**, `allowed_sources` **0**; `SERVICE_SOURCE_APPLICABILITY`
**3 files, none in `rawlsing_next`**. `pre553_empirical_query.py` contains **0** occurrences of `"service"`.

One precision note for the record: the terminal audit's W16 `current_ontology` cell reads *"operation-specific
rules/allowlists current."* I checked allowlist identifiers at the audit's **own** base commit `1dcd7ff6` — all
zero, as at my SHA. The cell most likely refers to required-scope checks on `EmpiricalQuerySpec.empirical_universe_refs`
and `SourceRelationResolver` exact-key scope checks, not a named allowlist artefact. Recorded as a precision note so
no later lane cites *"allowlists"* as an existing current object. This does not impugn the audit's classification,
which was correctly cautious: `UNKNOWN__FURTHER_FORENSICS_REQUIRED`, *"precise missing proof, not proved missing form."*

**Progression:** `UNKNOWN__FURTHER_FORENSICS_REQUIRED` (terminal audit) → `…_FORM_MISSING__BOUNDED_CONTRACT_REQUIRED`
(H-C) → `ADMISSIBLE_SET_AUTHORITY_FORM_DERIVED` (this lane). The audit's hedge is now discharged in the direction of
form-missing.

---

## For HQ — six judgement calls awaiting ratification

`JC-01` mandatory bounded candidate class · `JC-02` new state family · `JC-03` positive public state named `APPLICABLE`
(so it never collides with `ADMITTED_FOR_EXACT_STRUCTURAL_USE`) · `JC-04` undecided candidates surface with
`INCOMPLETE` rather than forcing whole-request refusal (**HQ may prefer the stricter policy — it is one line**) ·
`JC-05` MISS-04 restated as *no selection, therefore no selection reason* · `JC-06` candidate class included in the key.

**The one question HQ must answer explicitly:** is the answer **set only**, as derived — or is a separate
`SOURCE_PRIORITY_AUTHORITY` to be commissioned? **Do not leave it implicit. An implicit yes is an invented weight.**

---

**Held:** no code changes · no production mutation · no raw-source access · no locator discovery · no warrant
issuance · no actor/person implementation · no architecture reopen · no supersession of `pre553_source_relations.py`
or `pre553_structural_admission.py` · no temporal-directionality claim (H-A's seven meanings remain unresolved) ·
no C1 lineage reconciliation · no R9 fan-in · no live C4/C7 · **no invented source-ranking weights**.

**Artifacts:** `00_RETURN.md` · `01_AUTHORITY_DERIVATION_DECISION.json` · `02_SERVICE_REQUEST_KEY_SPEC.json` ·
`03_APPLICABILITY_DECISION_FORM.json` · `04_ELEVEN_POWER_SEPARATION_MATRIX.json` ·
`05_REPLAY_DETERMINANTS_AND_FAIL_CLOSED.json` · `06_F8_BOUNDARY_BINDING.json` ·
`07_HQD125_S15_ARCHITECTURE_TEST.json` · `08_NONAUTHORIZED_AND_OPEN_ITEMS.json` · `09_FINAL_DISPOSITION.json`

`HQ204_SERVICE_SOURCE_AUTHORITY_RETURNED__HQ_ADJUDICATION_REQUIRED`