# PYAT HQ204 — F7 positive-semantic exact forensics — R1

**Disposition:** `F7_POSITIVE_SEMANTICS_PARTIAL__NAMED_FORMS_MISSING`

**Terminal:** `HQ204_F7_POSITIVE_SEMANTICS_RETURNED__HQ_ADJUDICATION_REQUIRED`

- Repository: `maidiu/rawlsing`
- Branch: `agent/reviewer-pyat-hq204-f7-r1`
- Commissioned startup SHA: `beb784dad13c7103b452a37d08b2832c4fc91ea5` — **verified equal** (`git ls-remote` + `git rev-parse refs/remotes/origin/agent/reviewer-pyat-hq204-f7-r1`)
- Base: `ff4f06954824a3a5699bc5c1c9bd68cb3c5b4146` (HQ204 adjudication) — ancestor of the commissioned tip
- H-A return read directly at `6c088091494272bbaa26167a1c9005eb3a5b312e` (NOT an ancestor of the commissioned tip; see §2)
- Terminal-backward audit read directly at `codex/prev3-terminal-backward-audit-r1 @ b3ea471a3771113bf408a4e434a4b480b26d5856` (also NOT an ancestor of the commissioned tip)
- Checkout mode `SPARSE_REQUIRED` honored: one sparse worktree of the single canonical object store, no duplicate clone, no full checkout, no production mutation, no raw-survey access, no Astra referral.

---

## 1. What was done

H-A (`6c088091`) left **seven temporal meanings UNKNOWN**, holding exactly one item — temporal directionality authority — as affirmatively unconstituted. HQ204 accepted that.

This lane resolves those seven, one by one, by reading **current adopted authority first**, then historical V553/V551J functional capital, and classifying each exactly once. It then derives the smallest lawful authority contract capable of establishing a directional temporal claim.

Method discipline applied throughout:

- **M1 is ingress/equality/dedup only.** No positive temporal meaning was inferred from it. Confirmed by direct read of `rawlsing_next/m1_temporal_v554_admission_dedup.py`.
- **Historical code existence is not authority.** Every historical function is reported with its historical status (`PROVISIONAL`, `SCHEMA v0.2`, `SCHEMA v0.1`) and its adopted conservation disposition (or absence thereof).
- **No silent inheritance** of linear interpolation, scalar temporal-pressure coefficients, automatic rupture causation, universal point-year anchoring, or "trajectory requires >=3 anchors". Each is explicitly dispositioned.
- The old `POINT YEAR vs FIELDWORK INTERVAL` binary was **not** resurrected.

---

## 2. Two exact findings about the evidence base itself

These matter for HQ adjudication.

**(a) Neither the H-A return nor the terminal-backward audit is present on the commissioned control line.**

```
agent/reviewer-pyat-hq204-f7-r1 @ beb784d  ← commissioned tip
  ├── ff4f069 HQ204 adjudication          ← ancestor (YES)
  ├── 6c088091 HQ203 H-A return           ← ancestor (NO)
  └── b3ea471a terminal-backward audit    ← ancestor (NO)
```

Both were read exactly, from the object store, at their own commits (`git show <sha>:<path>`). No merge, cherry-pick or mutation was performed. This is a **reading** fact, not a lineage defect claim; the C1 lineage defect already catalogued in HQ204 is a separate matter.

**(b) H-A's own self-correction about `>=3 anchors` is confirmed and better grounded.** Direct forensics show the historical V553 multi-wave authorization gate fired at **two** eligible anchors, not three:

```python
# data/ddm_build_copy/ddm_v553_temporal_pressure.py:785-787
if harmonizer_authorized and len(eligible_wave_ids) >= 2:
    status = AUTHORIZED_SPARSE_TEMPORAL_KEY
    reason = "at_least_two_probe_ready_resolved_structural_anchors"
```

Reproduced independently in `ddm_v553_harmonization.py:605`, `:992-993`, and `ddm_v553_temporal_pressure.py:2604`, `:2683`, `:2991`, `:3467`. The `>=3` threshold appears in **no** adopted authority and in **no** historical module. Only `DIFFERENCE != TRAJECTORY` survives.

---

## 3. The seven meanings, resolved

Each item is classified exactly once. Full evidence in `01_TEMPORAL_MEANING_MATRIX.json`.

| # | Temporal meaning | Classification | One-line basis |
|---|---|---|---|
| 1 | persistent temporal identity / comparable temporal key | `HISTORICAL_FUNCTION_LAWFULLY_CONSERVABLE` | Complete, exact historical identity function; jurisdiction conserved claim-conditionally by the adopted R2 regrounding crosswalk row 15; current law supplies the lawful home (`TEMPORAL_EVIDENCE` authority kind) but no identity object. |
| 2 | temporal observation meaning | `HISTORICAL_FUNCTION_LAWFULLY_CONSERVABLE` | Historical observation frame = anchor + source structural fact ref + typed status + downstream permission + provenance. No current object is time-indexed: `EmpiricalFact` has **no** time field. The frame is conservable; its historical scalar payload is **not**. |
| 3 | positive temporal relation meaning | `POSITIVE_SEMANTIC_FORM_MISSING` | Never constituted historically or currently. Historically only adjacent `prior/current` pairs, `before/after` labels and year arithmetic. The historical word "directionality" meant **response/polarity** direction, not temporal order. |
| 4 | delta / comparison | `HISTORICAL_FUNCTION_LAWFULLY_CONSERVABLE` | Exact historical comparison function: signed difference over comparable anchors with comparability status, interpretation permission, direction class and magnitude class. Its scalar coefficients/values are expressly non-inheritable. |
| 5 | trajectory | `TERMINAL_NECESSITY_UNPROVED` | No trajectory concept exists in adopted law, current code, or historical temporal modules. The **only** historical occurrence of the word is a **prohibition** on rendering a claim as a trajectory. Necessity is unproved; `DIFFERENCE != TRAJECTORY` is the binding rule. |
| 6 | rupture candidate | `HISTORICAL_FUNCTION_LAWFULLY_CONSERVABLE` | Historical candidate layer with exactly the right safeguards (`rupture_status="candidate"`, `external_event_claim_made=False`, reserved-and-unfilled event authority slot, interpretation gated on comparability). Causal naming of a rupture is separately `TERMINAL_NECESSITY_UNPROVED`. |
| 7 | gap / absence as first-class observation | `HISTORICAL_FUNCTION_LAWFULLY_CONSERVABLE` | Historical gap/absence index made absence an indexed observation with `value_inference_allowed=False`. The general typed-absence law is already current binding in the empirical jurisdiction; the **temporal** gap object is historical capital only. |

**Tally:** `CURRENT_BINDING` 0 · `CURRENT_FORM__INSTANCE_MISSING` 0 · `HISTORICAL_FUNCTION_LAWFULLY_CONSERVABLE` 5 · `POSITIVE_SEMANTIC_FORM_MISSING` 1 · `TERMINAL_NECESSITY_UNPROVED` 1.

Plus the commissioned directionality item, classified separately:

| # | Item | Classification | Basis |
|---|---|---|---|
| 8 | temporal **directionality authority** | `POSITIVE_SEMANTIC_FORM_MISSING` | Confirms and extends H-A/HQ204. The historical harmonization gate functionally resembled a directionality authority, but (i) it was never adopted law, (ii) it compiled a **provisional scalar pressure field** and (iii) its scope was one survey family in one country at a point-year anchor — far narrower than the adopted F7 obligation. No adopted authority confers direction, so the authority that **establishes** it is affirmatively absent. |

---

## 4. Three corrections to the prior record

These are exact corrections, offered as findings, not as authority.

**(1) `TEMPORAL_NONCOMPARABLE` is not an implemented typed state.** H-A's `04_F7_POSITIVE_MEANING_GAPS.json` listed "typed negative states (`TEMPORAL_NONCOMPARABLE`, `NONCOMPARABLE`) already exist" and graded typed noncomparability `AUTHORITY_INSTANCE_ONLY`. Direct forensics:

- `NONCOMPARABLE` **is** enumerated in two current state families (`SOURCE_UNIVERSE_STATE`, `SOURCE_UNIVERSE_RELATION_STATE`) — `rawlsing_next/pre553_empirical_objects.py:79,88`.
- `TEMPORAL_NONCOMPARABLE` occurs **exactly once in the entire worktree**, as a bare string in a forbidden-backfill target set:

```python
# rawlsing_next/pre553_source_relations.py:52-55
FORBIDDEN_BACKFILL_TARGET_STATES = frozenset({
    "DECLARED_NONE", "SOURCE_NOT_APPLICABLE", "TEMPORAL_NONCOMPARABLE",
    "OBSERVED_ZERO", "ZERO_SUPPORT", "NONCOMPARABLE", "NOT_APPLICABLE",
})
```

It is consumed as a name, is a member of **no** state family, has no producer and no schema. The **source** noncomparability refusal is implemented; the **temporal** noncomparability refusal is named-but-unconstituted. This is a required, not optional, part of the directionality contract (§5).

**(2) `ABSENCE != ZERO` is binding for *empirical* absence and only historically constituted for *temporal* gap absence.** The audit matrix W22 is `CURRENT_BINDING_CONCEPTUALLY_CLOSED` for typed negatives generally, and HQ125 §5 freezes `TYPED_SEMANTIC_RELATION_ABSENCE != EMPIRICAL_COTRAVEL_ABSENCE`. For **temporal** gaps the only authority is the historical `V553_TEMPORAL_GAP_AND_ABSENCE_INDEX_SCHEMA`. H08's label "Binding" for `ABSENCE != ZERO` attached to that historical schema overstates its authority class. Corrected in `05_GAP_RUPTURE_TRAJECTORY_LAW.json`.

**(3) The historical "directionality" vocabulary is response directionality, not temporal directionality.** This is the trap H-A avoided and that must stay avoided. Directly:

```python
# data/ddm_build_copy/ddm_v553_harmonization.py:54-66ff
DIRECTIONALITY_SIGNAL_COLUMNS = {
    "directionality_policy", "signed_polarity_status",
    "directional_certification_status", "response_topology",
    "response_direction", "polarity", "scale_direction", ...
}
# data/ddm_build_copy/ddm_v551j_schema.py:47-54
V551J_DIRECTIONALITY_STATUSES = {
    "known_directional", "partial_directionality", "undirected_association",
    "conflicting_directionality", "not_applicable", "unknown",
}
```

`shared_directionality_columns` is a **response-scale polarity harmonization** requirement. `V553_HARMONIZED_PRESSURE_KEY_INDEX_SCHEMA`'s `directionality_compatibility_status` therefore reports *response-direction compatibility between waves*, not a temporal arrow. Temporal order in V553 came only from numeric `temporal_year` sorting. **`RESPONSE_DIRECTIONALITY != TEMPORAL_DIRECTIONALITY`.**

---

## 5. Directionality: the smallest lawful authority contract

Full contract in `03_DIRECTIONALITY_AUTHORITY_CANDIDATE.json`. Summary of the derivation:

H-A established that temporal directionality authority is affirmatively unconstituted, and that `TWO_WAVES_EXIST != TEMPORAL_DIRECTIONALITY_AUTHORITY`. HQ204 accepted it. Neither current nor historical law supplies the function at the required grain, so this is a **bounded new authority-form candidate** — not a historical succession.

The smallest form that can carry it is **one new authority kind**, `TEMPORAL_COMPARABILITY`, whose required material binds:

1. **identity/comparability prerequisites** — the persisting comparand (`source family`, `geography`, `question/coordinate semantics`, `response surface`, `instrument release`, `target population / risk set`, `estimand`, `measure-and-weight design`) and the rule *one anchor per temporal identity*;
2. **source / scope / time refs** — exactly ≥2 ordered anchor refs, each exact and hash-bound, each naming its source universe, governed use, and an explicit time ref that is **either** a point **or** an interval, grain preserved (see §6);
3. **ordered relation basis** — the authorized comparison law for those time refs (calendar total order; family-local ordinal where calendar is unavailable, with `WAVE_LABEL != ORDINAL != CALENDAR_YEAR`; or interval overlap ⇒ **partial** order ⇒ no direction claimable). Ordering may **never** be taken from array position, recency or "latest";
4. **estimand / measure authority** — exact `WEIGHT_DESIGN_ESTIMAND` + estimand refs; both anchors must be the same estimand under the same measure basis; no default averaging or renormalisation;
5. **uncertainty / refusal states** — a fail-closed enumerated set, including a real `TEMPORAL_NONCOMPARABLE` state family (Finding §4.1), `TEMPORAL_GAP_INTERVENING` (gap preserved as unknown), and `TEMPORAL_INTERPOLATION_NOT_AUTHORIZED` (no interpolated anchor may be an observation);
6. **provenance / replay** — content-addressed claim identity, exact authority snapshots, deterministic canonical projection, producer replay root, no `latest`/`default`/`fuzzy`/`nearest` selection;
7. **exact claim ceiling** — stated positively in the contract: a directional claim asserts a signed change of one authorized estimand between two exactly-identified, exactly-comparable, exactly-ordered anchors, with uncertainty class and provenance. It does **not** assert cause, external event, mechanism, continuity or interpolation between the anchors, monotonicity, that unobserved years are zero or unchanged, transferability to any other source/family/geography/estimand, actor experience or effect, or that the result is a "trajectory", "pressure field", "rupture" or "social movement".

**Cardinality:** exactly **two** authorized comparable anchors suffice for an ordered directional claim. `>=3` is not law. Longer ordered chains of authorized consecutive pairs may be emitted; **no distinct "trajectory" object is thereby constituted.**

The three forbidden inferences are structurally blocked, not merely discouraged: `TWO_WAVES_EXIST => DIRECTIONALITY` is blocked because the claim requires a bound `TEMPORAL_COMPARABILITY` authority instance; `DIFFERENCE => TRAJECTORY` is blocked because no trajectory object exists; `TEMPORAL_COINCIDENCE => CAUSE` is blocked because the contract has no causal field and causal naming would require an SDTF causal-use authority plus a filled event authority (still `reserved_not_filled` historically and unowned now).

---

## 6. Time grain — polymorphism preserved, not collapsed

Full trace in `04_TIME_AND_COMPARABILITY_LAW.json`. The old universal binary is dead and was not resurrected. What is actually true:

- `rawlsing_next/pre553_structural_admission.py:218` — `allowed_effective_time_or_interval_refs: tuple[ExactRef, ...]`; `:358` — `effective_time_or_interval_refs_required_by_target_use`. Enforcement is **set-membership** (`:673-678`), producing `TEMPORAL_SCOPE_MISMATCH`. There is **no grain enum, no grain validation, no grain assertion** in the module.
- `:281-282` — a time-scoped rule must bind exact `TEMPORAL_EVIDENCE` authority. The law constrains **authority**, not **grain**.
- `rawlsing_next/pre553_empirical_authority.py:86` — `"TEMPORAL_EVIDENCE": ("source-native effective/reference-time evidence",)`. One time-related authority kind out of eighteen. Meanwhile `effective_period` and `time_geography_applicability` are free, untyped `Mapping[str, Any]`.
- `rawlsing_next/pre553_empirical_objects.py` — `EmpiricalUniverse` carries `field_or_reference_time`; `EmpiricalCoordinateFact` carries `effective_or_reference_time`; **`EmpiricalFact` carries no time field at all**.
- `rawlsing_next/source_backed_positioned_subject_possibility.py:80` — `effective_time_or_interval: Any`, untyped, alongside a **required positive `comparability_authority_ref`**. The comparability authority **slot** is current law at the F8 grain; its temporal content is not constituted.
- `rawlsing_next/v3_adp010_oee_executor.py:121,227` — `effective_from` / `effective_until` are ISO-8601, timezone-aware **instants** with `effective_until >= effective_from` enforced (`:174-175`), and `time_granularity` is a **free non-empty string** with observed values `INSTANT` / `INTERVAL` and **no closed-set validation**. This is V3 actor-record jurisdiction, not PRE-V3 empirical comparison.
- M1 carries `rule_relevant_effective_time_semantics_fingerprint` — a fingerprint **of** a semantics that must already exist.
- Historically: V553 forced a point-year calendar anchor and refused to treat a wave ordinal as a year (`ddm_v553_temporal_identity.py:30-46`) and refused two anchors in one year (`:138-144`); it had **no** fieldwork-interval field at all; EVS carried a hard-coded wave↔year map (`ddm_survey_identity.py:89`).

**Finding:** the grain is *claim/rule-bound by construction*. Different operations lawfully carry different exact time representations. The correct law is: **the time ref is an exact ref; the grain is whatever the governing rule's exact `TEMPORAL_EVIDENCE` authority binds; no operation may coerce, midpoint, interpolate or universalise the grain.** Preserve the polymorphism.

---

## 7. Astra test

**NO ASTRA.** Full reasoning in `07_ASTRA_TEST.json`.

HQ203 made referral conditional on a genuinely high-consequence fork surviving operation/source-specific time-semantics tracing. After that tracing:

- the withdrawn HQ202 time-grain packet is **not** reinstated;
- the residual time question is *typed*, not a forced choice: the contract carries `TEMPORAL_NONCOMPARABLE`, partial-order (interval-overlap) states and `TEMPORAL_INTERPOLATION_NOT_AUTHORIZED`, so an unanswerable comparison is representable as a typed refusal rather than needing an external decision;
- the directionality contract is derivable from existing noncollapse law plus one bounded authority kind, which is an HQ adoption act, not an underdetermined fork;
- no fork was found that (a) cannot be resolved from authority, (b) cannot be represented as typed noncomparability/refusal, and (c) materially changes terminal semantics.

HQ204 already directs the next frontier here (lane 3, F7 positive-semantic exact forensics / bounded authority derivation; plus lane 4's H-C bounded authority form). A bounded authority-form adoption is HQ's own docket. Referral now would be referral merely because something is unfinished.

---

## 8. Disposition and why

**`F7_POSITIVE_SEMANTICS_PARTIAL__NAMED_FORMS_MISSING`.**

- Not `…CONSERVED__BOUNDED_DIRECTIONALITY_AUTHORITY_READY`: five meanings are lawfully conservable **as function**, but two **named positive forms do not exist anywhere** — the positive temporal relation object (§3.3) and the temporal directionality / comparability authority (§3.8) — and one further named form's terminal necessity is unproved (§3.5, trajectory). Conservation of a function is not constitution of a form.
- Not `…ASTRA_NEEDED`: §7.
- Not `F7_ARCHITECTURE_REOPEN_REQUIRED`: no adopted requirement was shown to have no lawful home. Every meaning has a lawful current home (`TEMPORAL_EVIDENCE` authority kind, the `M1` families `TEMPORAL_KEY`/`TEMPORAL_OBSERVATION`/`TEMPORAL_RELATION`, exact-ref scope checks, typed negatives, replay/provenance, SDTF objective-consequence jurisdiction for occurrence/currentness). The deficit is a bounded authority **form** at an existing grain, exactly the class HQ204 already accepted for H-C.
- Not `MATERIAL_AUTHORITY_CONFLICT`: no two adopted authorities conflict here. The apparent conflict was between the **unadopted** HQ201 return and adopted law, and it was resolved in favour of adopted law by H-A and HQ204; this lane found no new conflict.

**Newly bounded work handed to HQ** (candidates, not adoptions): one authority kind `TEMPORAL_COMPARABILITY` + its required material keys (§5); one typed state family for temporal noncomparability; one positive temporal-relation object bound to that authority; conservation of the historical identity/observation/delta/rupture-candidate/gap functions at their declared ceilings. Plus `TEMPORAL_NONCOMPARABLE` promotion from bare string to real state family (§4.1) — currently it can be named in a forbidden-backfill set that no object family can ever produce.

---

## 9. Anti-inheritance ledger (what this lane refused to import)

| Tempting inheritance | Disposition | Exact reason |
|---|---|---|
| linear interpolation | **REFUSED** | Historically `allow_interpolation` defaulted `False`, the CLI never enabled it (`compile_v553_temporal_pressure_field.py:17-41`), the key-level segment index hard-codes `interpolation_allowed = False` with `"unknown_gap_preserved"` (`ddm_v553_temporal_pressure.py:2691-2695`), and `interpolation_across_rupture_allowed` is hard-coded `False` (`:1282`). The legacy country-year grid *did* interpolate when enabled — that branch is the obsolete one (see `02_HISTORICAL_CONSERVATION.json`). |
| scalar temporal-pressure coefficients | **REFUSED** | `pressure_intensity`, `contradiction_pressure`, `absence_pressure`, `uncertainty_pressure`, `rupture_pressure`, probe/authorized split and the `0.45/0.15/0.10/0.20` component weights are provisional (`V553_SCHEMA_VERSION = "v0.2"`) and were never adopted. |
| automatic rupture causation | **REFUSED** | `external_event_claim_made` is hard-coded `False`; the event authority slot is `reserved_not_filled` with `event_authority_ref = ""`; the word `caus*` occurs **zero** times in the 4187-line pressure module. The historical V551J v2 schema independently forbids `do_not_render_as_rupture` and `do_not_render_as_causal_joint_effect`. |
| universal point-year anchoring | **REFUSED** | V553 point-year was scoped to one family in one country; current law has no grain enum; the V3 affordance is `INSTANT`/`INTERVAL`; the pre-V3 field is explicitly `time_OR_interval`. |
| "trajectory requires >=3 anchors" | **REFUSED** | Historical gate fired at `>= 2`; no adopted or historical source states `3`. `DIFFERENCE != TRAJECTORY` survives alone. |
| historical "directionality" as temporal direction | **REFUSED** | It is response/scale polarity harmonization (§4.3). |
| historical stage names / serial V553→V558 traversal | **REFUSED** | Adopted R2 law: `PRESERVE_FUNCTION_AND_AUTHORITY != PRESERVE_HISTORICAL_STAGE_OR_CARRIER`; crosswalk row 15: "no required V553 node". |

---

## 10. Holds observed

No production mutation. No source access. No raw-survey or C4 work. No C7 or actor/person implementation. No locator discovery. No warrant issuance. No architecture reopen, and none by implication. No Astra referral. Nothing written outside `WORKER_RETURNS/PYAT-HQ204-F7-R1/`. Sparse checkout was widened only to read exact historical DDM modules and the survey-identity helper that ten modules import; no clone was created.
