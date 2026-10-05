# 00 — HQ208 F7 temporal comparability contract — independent hostile review — R1

Lane: `PYAT-HQ208-F7-TEMPORAL-CONTRACT-INDEPENDENT-REVIEW-R1`
Role: independent hostile reviewer. No implementation. No self-adoption. No repair of production code.
Review tip: `0c74e4beeb29967b4ea9a0599057a1d658f33b16` (commission tip, verified equal to `origin/agent/reviewer-pyat-hq208-f7-temporal-contract-r1` before work)
HQ startup base: `26f26a56826e027f0149d12eaa1a5402dea942d9`
Under review: `agent/rabochii-pyat-hq206-f7-contract-r1 @ 19fd6f6e9f3e24c716310335325cef4c75e6fa56`
Original worker commission tip: `20568aae374396cbc058bb500777491379a29f8c`
Exact control base asserted by the contract: `ee8e7a1aef1b1eba19b8ca0304186636cd3f874e`
Primary F7 forensic return: `ac444c5a345cded633a8e5b30ccd8b718f903d55`

## DISPOSITION

`TEMPORAL_COMPARABILITY_CONTRACT_PARTIAL__BOUNDED_REPAIR_REQUIRED`

The contract is **substantively correct, materially over-stated in two places, and under-bounded in three**. It is **not** authority overreach: it does not swallow the five conserved functions, does not smuggle direction into authorization, does not constitute rupture, trajectory or gap objects, does not import a V553 scalar, and does not launder any V553 numeric semantics. It also does not conflict with any adopted authority. But it is **not yet safely commissionable as implementation**, because three of its own laws are self-contradictory or non-binding at the point where an implementer would need them, and because it does not bound the implementation surface it necessarily implies. A bounded documentary repair closes all of it.

## EVIDENCE FRAME (what was actually verified, not trusted)

The change set is exactly 9 new files, all under `WORKER_RETURNS/PYAT-HQ206-F7-TEMPORAL-AUTHORITY-CONTRACT-R1/`. `git diff 20568aa 19fd6f6` is 9 files / 1425 insertions / 0 production files. No production file changed. The claimed primary sources are byte-identical between the asserted control base `ee8e7a1a` and this review tip:

```
git diff --stat ee8e7a1a 0c74e4be -- rawlsing_next/pre553_empirical_authority.py \
  rawlsing_next/pre553_source_relations.py rawlsing_next/pre553_structural_admission.py \
  rawlsing_next/pre553_empirical_objects.py rawlsing_next/m1_temporal_v554_admission_dedup.py
=> empty (exit 0)
```

Every primary citation in the return was opened and read at these exact refs. Verified exact:

| Claim | Verified |
| --- | --- |
| `AUTHORITY_KINDS` is exactly 18 kinds at `pre553_empirical_authority.py:25-44` | yes — enumerated, count 18 |
| All 7 named reuse targets are members of that set | yes — `:28,31,34,35,40,41,42,43` |
| `AUTHORITY_KIND_CEILINGS` refs `:75,78,84,85,86,87,71-72` | yes |
| `FORBIDDEN_SELECTOR_TOKENS` at `:58-60`, used `:99-111` | yes |
| `TEMPORAL_NONCOMPARABLE` at exactly one production site, `pre553_source_relations.py:54`, bare, inside `FORBIDDEN_BACKFILL_TARGET_STATES` | yes — repo-wide grep, 1 production occurrence |
| `EMPIRICAL_FACT_NONCOMPARABLE` produced at `pre553_structural_admission.py:639-640` and `:680-681`, enumerated `:47`, mapped `:65` | yes — plus a third site `:686-687` the contract omits |
| `NONCOMPARABLE` in `SOURCE_UNIVERSE_STATE` / `SOURCE_UNIVERSE_RELATION_STATE` at `pre553_empirical_objects.py:79,88` | yes |
| `AUTHORITY_STATE` reused unchanged at `pre553_empirical_objects.py:82-85` | yes |
| `UNCERTAINTY_UNQUANTIFIED` and the `OBSERVED_ZERO`/`ZERO_SUPPORT` structural distinction at `:102-104,717-722` | yes |
| `EmpiricalFact.REQUIRED_FIELDS` has no time field, `:696-724` | yes |
| `allowed_effective_time_or_interval_refs` is `tuple[ExactRef, ...]` at `pre553_structural_admission.py:218`, no grain enum/validation anywhere in the module | yes — `:281-282` requires `TEMPORAL_EVIDENCE`; `:305` projects refs; `:358,369,673-678` exact-ref membership with `TEMPORAL_SCOPE_MISMATCH` |
| `effective_period` / `time_geography_applicability` are grain-free canonicalised mappings `:225-226,273-274,325-326` | yes |
| M1 states and `:292` no-clock law | yes — `:50-57,83,240-247,292` |
| `rupture_override_status = reserved_not_filled` at `ddm_v553_temporal_pressure.py:900` | yes |
| `external_event_claim_made: False` at `:2826`; `event_registry_status: not_supplied` at `:1281` | yes |
| `EVS_WAVE_BY_YEAR` at `ddm_survey_identity.py:89`; wave-as-label at `:123-159,204-215` | yes — `wave_ordinal` docstring is verbatim "without changing the canonical label" |
| `_explicit_temporal_year` refuses wave-ordinal-as-year and requires one anchor per year, `ddm_v553_temporal_identity.py:30-46,129-144` | yes |
| `V553_COMPILER_VERSION = "v553_temporal_pressure_0.2_sparse"` | yes — `ddm_v553_schema.py:11` |
| Conserved V554 limit semantics `is_limit` / `does_not_negate_original_fact` / "blocks relation/delta use; no temporal F1" | yes — `.../PRE_S01_5_V554_ARCHITECTURE/RESULT.json:313,526,711` and `RESULT.md:108,474,1014` |
| Withdrawn HQ201 `TIME-GRAIN-FORK` not reinstated; no Astra referral claimed | yes |
| No V553 numeric semantics laundered in | yes — every numeric literal in all 8 JSON artifacts is a structural count (`18/19/1/0/2/1`); no coefficient, threshold, deadband, weight or magnitude |
| All 8 JSON artifacts parse | yes |

Two verifications were **not** reproducible from the review branch alone and were taken from the exact objects named by the contract: the F7 forensic return `ac444c5a` (`WORKER_COMMISSIONS|RETURNS/PYAT-HQ204-F7-R1/*`) and the original HQ206 worker commission at `19fd6f6e`.

## THE TWELVE ATTACK QUESTIONS

### 1. Is exactly ONE new authority kind the minimal missing owner? — SUSTAINED, with one naming consequence

The adopted closed set `AUTHORITY_KINDS` (`rawlsing_next/pre553_empirical_authority.py:25-44`) holds exactly 18 kinds:

`SOURCE_SEMANTICS_TOPOLOGY`, `PHYSICAL_NATIVE_REPRESENTATION_BINDING`, `NATIVE_CANONICAL_MAPPING_HARMONIZATION`, `ROUTING_RISK_SET`, `COORDINATE_SEMANTICS`, `WEIGHT_DESIGN_ESTIMAND`, `PREDICATE_GRAMMAR`, `SOURCE_UNIVERSE_RELATION`, `SOURCE_EQUIVALENCE`, `SOURCE_RESPONDENT_LINKAGE`, `SOURCE_COMPOSITION_POOLING`, `SOURCE_BACKFILL`, `DISCOVERY_FRONTIER`, `STRUCTURAL_ADMISSION`, `UNCERTAINTY_METHOD`, `TARGET_USE_PERMISSION`, `TEMPORAL_EVIDENCE`, `REPLAY_PROTOCOL`.

Every one of the seven commission-named reuse targets is a literal member, not a near-miss. I independently challenged each remaining kind as a possible home for pair-ordering law and found none: `COORDINATE_SEMANTICS` governs coordinate identity/value/unit/taxonomy, not time order; `SOURCE_UNIVERSE_RELATION` is confined to `RELATION_AUTHORITY_KINDS` and is guarded by `validate_relation_authority_only` (`:295-308`), which raises unless the kind is in the five source-relation kinds — so it cannot host temporal ordering without a code change; `STRUCTURAL_ADMISSION` decides admission, and its temporal content (`TEMPORAL_SCOPE_MISMATCH`, `:47-48,65-68,673-678`) is scope membership, not order. `TEMPORAL_EVIDENCE`'s ceiling is "source-native effective/reference-time evidence" (`:86`) — it binds evidence and does not order observations. Minimality is sustained.

**Consequence the contract does not state.** There is a strict 18↔18 bijection between `AUTHORITY_KINDS` and `AUTHORITY_KIND_CEILINGS` today (verified programmatically: no kind lacks a ceiling, no ceiling lacks a kind). Proposing a 19th kind therefore necessarily implies a 19th ceiling and a governed-operation surface for `TEMPORAL_COMPARABILITY`. The return asserts "the set itself is **not edited**" (07, line 25) and never names the ceiling obligation. This is a bounding omission, not a minimality defect — see Repair 5.

### 2. Does the contract swallow any of the five conserved temporal functions? — NO

Functions are owned as: (3) delta/comparison directly; (1) identity and (5) gap/absence by reference to existing forms; (2) observation and (4) rupture left to separate producers. I attacked each:

- **Identity.** The contract could have minted identity; it does not — `temporal_identity_contract_ref` is a required *consumed* `ExactRef` whose `owner_boundary` is explicitly under `TEMPORAL_EVIDENCE` with `one_anchor_per_temporal_identity: true`. No identity is authored, and no instance exists (`IDENTITY_CONTRACT_INSTANCE_MISSING`, confirmed: nothing in `rawlsing_next/` names a temporal identity contract).
- **Observation.** The receipt's `observation_refs` are required but unauthored, and the contract records the real limitation (`EmpiricalFact.REQUIRED_FIELDS` has no time field, `:696-724`) rather than silently repairing it.
- **Rupture.** `RUPTURE_CANDIDATE_STATE` is deliberately placed **outside** `TEMPORAL_RELATION_STATE` with `no_producer_authorized` and six prohibitions. Confirmed: no rupture producer exists anywhere in `rawlsing_next/`.
- **Gap.** Only `intervening_span_state` is added, and the contract correctly attributes the general typed-absence law to `pre553_empirical_objects.py:102-104,717-722` rather than re-deriving it.

One boundary observation: the identity key's `must_compose_at_minimum` list includes `estimand` and `measure and weight design`, which are surfaces owned by `WEIGHT_DESIGN_ESTIMAND`. This is composition-of-key material, not ownership, and the contract says so. Noted, not scored as a defect.

### 3. Is `TEMPORAL_NONCOMPARABLE` distinct from `EMPIRICAL_FACT_NONCOMPARABLE`, or an alias/overwrite? — DISTINCT; one literal-overlap hazard

Distinct on all four axes the contract claims, and I verified the producer contrast: the source side is a produced decision in the `P06` list with reason codes at three sites (`:639-640`, `:680-681`, `:686-687`); the temporal side was a bare string in a `frozenset` of *forbidden backfill targets* with no family, no producer, no reason. The contract promotes it to `TEMPORAL_RELATION_RECEIPT.relation_state` with a mandatory companion reason, and the underlying object is different (a fact vs an ordered pair), the producer is different, and the scope effect is different. The `is_limit` / `does_not_negate_original_fact` semantics are carried verbatim from the V554 advisory record, which I read at source.

**Hazard.** `FORBIDDEN_BACKFILL_TARGET_STATES` (`pre553_source_relations.py:54`) already contains **both** `"TEMPORAL_NONCOMPARABLE"` and `"NONCOMPARABLE"` as a flat cross-family string tuple. The new vocabulary then uses `TEMPORAL_NONCOMPARABLE` as a *relation state value* and `EMPIRICAL_FACT_NONCOMPARABLE` as a *P06 decision*. After adoption, `"TEMPORAL_NONCOMPARABLE"` denotes both a produced state and a forbidden backfill target, in an untyped tuple that also holds source-family state strings. The contract's `backfill_prohibition_preserved` correctly requires the tuple membership to survive, but never states the non-collapse direction that now matters: **no rule may backfill into a pair whose `relation_state` is `TEMPORAL_NONCOMPARABLE`, and no `TEMPORAL_RELATION_RECEIPT` may be emitted as a backfill target.** See Repair 7.

### 4. Are all states typed, reason-carrying, replayable and non-silent? Are the claimed 11/14/15 counts true? — MOSTLY, BUT THE RETURN'S COUNT IS WRONG AND STATE DERIVATION IS UNDERDETERMINED

Counts recomputed from the artifacts, not trusted:

| Object | Count | Return's claim | Verdict |
| --- | --- | --- | --- |
| `TEMPORAL_RELATION_STATE` members (03) | **12** | 11 (`00_RETURN.md:25`) | **MISCOUNT** |
| `relation_state` enum values (02) | **12**, identical set to 03 | — | consistent |
| `TEMPORAL_NONCOMPARABLE` reason codes | **11** | 11 | true |
| `noncollapse_matrix` rows (06) | **15** | 15 | true |
| `refusal_matrix.rows` (06) | **14** (12 fail-closed, 2 not) | 14 | true |

The likely origin of the "11" is a transposition of the 11 reason codes of `TEMPORAL_NONCOMPARABLE`. The receipt's own `relation_state` list (`02_TEMPORAL_RELATION_RECEIPT_CONTRACT.json:125-138`) contains 12 entries and is identical as a set to the vocabulary's. This is a documentary misstatement of the headline defect-closure enumeration and must be corrected.

Three real non-silence defects:

1. **Positive state with an empty reason list.** `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` has `reason_codes: []`, yet `relation_state_reason` is `required: true` and "a bare state with no reason is not a valid receipt" (02, line 144). Either the positive state has a defined reason (e.g. `PAIR_ORDERED_UNDER_BOUND_BASIS`) or the field must be conditionally required. As written an implementer cannot satisfy both.
2. **No derivation rule, no precedence.** `relation_state` is "the single overall typed state of the receipt", but the contract never says how it is derived when several comparability surfaces fail, when a required authority is missing, or when both hold. Two conforming implementations can therefore emit different `relation_state` values for identical inputs — which defeats the `replayable` claim attached to every refusal row. F7's own candidate enumerated these as separate states (`TEMPORAL_AUTHORITY_MISSING`, `TEMPORAL_AUTHORITY_CONFLICT`, `TEMPORAL_OUT_OF_SCOPE`, `TEMPORAL_INTERPOLATION_NOT_AUTHORIZED`, `TEMPORAL_PROBE_ONLY`); the contract folds them into one or drops them without saying so.
3. **`relation_state_reason` cardinality.** Typed `enum` (singular) in 02 but specified as a `reason_codes` **list** per state in 03. A list-valued condition cannot be reported into a single enum value without an unstated selection rule.

Also noted, lower severity: `TEMPORAL_ORDER_UNAUTHORIZED` and `ORDER_UNKNOWN_NONCOMPARABLE` cross-reference each other by reason code ("as the reason code dictates"), and `TEMPORAL_NONCOMPARABLE` carries `ORDER_BASIS_NOT_APPLICABLE_TO_PAIR` as one of its own reasons — so the same condition is reachable as two different terminal states with no tie-break.

### 5. Does `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` smuggle direction, cause, continuity, trend, trajectory, transfer or F8 power? — NO SMUGGLING, BUT THE RECEIPT PERMITS AN INTERNAL CONTRADICTION

The `exact_claim_ceiling` is properly narrow and explicit: `CAUSE`, `EXTERNAL_EVENT`, `CONTINUITY_OR_INTERPOLATION`, `MONOTONICITY_OR_TREND`, `ZERO_OR_NO_CHANGE_IN_UNOBSERVED_YEARS`, `TRANSFER`, `TRAJECTORY`, `TEMPORAL_PRESSURE_SCALAR`, `GRAIN_COERCION` are all prohibited by name, with the exact historical refs that make them live prohibitions (`:900`, `:2826`, `:1281` verified). F8 consumption is explicitly deferred to HQ204 node H-D.

**Defect.** The positive state's own meaning (03, line 27) is "the order basis yields a **total order on this pair**, and a direction claim is authorized", and it is paired with `direction_claim INCREASE | DECREASE | NO_AUTHORIZED_CHANGE`. But `direction_claim` (02, lines 72-78) and `relation_status` are independent enum fields with no constraint tying them to `relation_state`. Nothing in the contract forbids the pair:

```
relation_state = TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED
direction_claim = DIRECTION_NOT_CLAIMABLE
```

or

```
relation_state = TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED
temporal_order_basis_ref -> PARTIAL_ORDER_NO_DIRECTION
```

The second is worse: `temporal_order_basis_ref` is `required: true` and "always present, **including when the basis is one that yields no direction**" (02, line 48), so an implementer may legitimately bind a non-authorizing basis to an authorized claim. This is exactly the class of overclaim the commission's Q5 targets. See Repair 2.

### 6. Is the order-basis law sufficient for the commissioned cases, or overclaimed as a universal algebra? — SUFFICIENT AND CORRECTLY CLOSED, BUT ONE OF THE FOUR NAMED KINDS IS NOT AN ORDER BASIS

The four kinds map exactly onto the four distinctions the HQ206 commission mandates ("calendar total order where exact points/nonoverlapping intervals permit it; family-local ordinal where specifically authorized; overlapping/partially ordered intervals where direction may be refused; unknown/noncomparable temporal ordering"), so sufficiency for the commissioned cases is established. The closed-set discipline holds: no fifth kind, no general algebra, `rule_7` explicitly refuses same-family-membership-as-grain-proof, `rule_8` refuses scalar eligibility, and the withdrawn HQ201 two-way grain fork is not reinstated (verified — the only reference is the explicit non-reinstatement record). One over-statement is contained in a single sentence: `04_TIME_ORDER_BASIS_LAW.json:68` says the four are "**jointly exhaustive** and mutually exclusive **for the cases the commission names**" — the qualifier saves it; the same document's `explicitly_not` for `CALENDAR_TOTAL_ORDER` reinforces that no universal grain is claimed. The `01` residual risk correctly says "No general temporal algebra is derived, and none is authorized."

**Defect.** `ORDER_UNKNOWN_NONCOMPARABLE` (`04`, lines 106-112) carries `permits_direction: false` and `refusal_state: TEMPORAL_NONCOMPARABLE or TEMPORAL_ORDER_UNAUTHORIZED` — that is, **the order basis for a pair whose order is unknown** emits the refusal states that mean, respectively, "not comparable" and "no permitted order basis applies". A value meaning "no permitted order basis applies" cannot be an `ExactRef` into the order-basis law while the receipt simultaneously declares `temporal_order_basis_ref` "authorized". Every other status on that field ("authorized", "required", "including when the basis yields no direction") treats the ref as an authorization. Either the fourth kind is reclassified as a typed refusal keyed on `temporal_order_basis_ref` being **absent**, or the field's requiredness must be conditioned. As written, `TEMPORAL_ORDER_UNAUTHORIZED` is reachable two ways (absent ref, and present-but-unknown ref) with no distinction, and the authority contract's own `refusal_if_absent: TEMPORAL_ORDER_UNAUTHORIZED` (01, line 93) becomes non-exclusive. See Repair 1.

### 7. Does `NO_AUTHORIZED_CHANGE` depend on a deadband, and is that deadband bound? — IT DEPENDS ON ONE; THE DEPENDENCE IS NOT BOUND

`NO_AUTHORIZED_CHANGE` is defined as "a positive finding that no change was claimable **under a bound deadband**" (06, NC-06). The contract correctly carries the prohibition everywhere else: `nonpositive_is_never_evidence_of_no_change`, `no_default_deadband`, and `exact_claim_ceiling.asserts_not[TEMPORAL_PRESSURE_SCALAR]` ("no deadband inherited as an adopted default. A deadband, if used, must itself be bound by the comparability authority"). No numeric deadband appears in any artifact (verified: every numeric literal is a structural count).

But nothing in the receipt or the authority makes the binding *real*. There is no `deadband_ref` field, no required-input slot, no reason code for deadband-absent, and no constraint of the form "`NO_AUTHORIZED_CHANGE` may be emitted only if an exact deadband authority ref is present". So the contract simultaneously (a) defines `NO_AUTHORIZED_CHANGE` as deadband-dependent and (b) allows it to be emitted with no deadband anywhere in the receipt. An implementer who never binds a deadband and never emits `NO_AUTHORIZED_CHANGE` is conforming; an implementer who emits it without a deadband is equally conforming. The discipline is therefore a notice, not a binding. See Repair 3.

### 8. Does grain handling fail closed? — YES FOR EVERY NEW PATH; THE RESIDUAL IS CORRECTLY NAMED

The contract's grain law is conservative and, in the one place it matters most, honest:

- `rule_1` makes the substrate time ref exact and opaque; `rule_2` binds grain to `TEMPORAL_EVIDENCE` per operation; `rule_3` prohibits midpoint, ordinal→year, `ordinal-as-date`, interval→point and interpolation-as-substitute; `rule_5` makes overlapping intervals a partial order with a typed refusal; `rule_6` preserves polymorphism.
- The failure mode is a typed refusal, not an inference: `ORDER_UNKNOWN_NONCOMPARABLE` → `TEMPORAL_NONCOMPARABLE` / `TEMPORAL_ORDER_UNAUTHORIZED`, plus `TEMPORAL_MAPPING_MATERIAL_ABSENT` for unadopted family mapping and `TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT` for cross-universe pairs.
- I independently confirmed the substrate really is grain-blind: `allowed_effective_time_or_interval_refs` is `tuple[ExactRef, ...]` (`:218`), projected as refs (`:305`), compared by exact membership (`:673-678`), and `AUTHORITY_KIND_CEILINGS["TEMPORAL_EVIDENCE"]` is only "source-native effective/reference-time evidence" (`:86`). There is no grain enum, no grain validation and no grain comparison in the module. The contract records this as `TIME_REFS_CURRENTLY_EXACT_AND_GRAIN_UNVALIDATED` and explicitly does **not** recommend a substrate grain enum.

The honest residual, which I accept as *named and not repaired* rather than as a defect: grain is enforced entirely by the binding authority, so a mis-authored authority instance can authorize a grain-invalid comparison and no structural guard exists at the substrate. The contract says precisely this. The residual risk is disclosed, and a grain enum at substrate level is refused. No new unsafe inference is introduced anywhere.

### 9. Does cross-universe comparison manufacture source equivalence, estimand comparability or measure comparability? — NO

`source_equivalence_ref` is `required: false` with `required_when: "the compared pair crosses source universes"`, and absence yields the typed refusal `TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT`. `rule_7` and NC-15 both refuse same-family membership as proof of comparability or grain adequacy. `TEMPORAL_ESTIMAND_MISMATCH` and `TEMPORAL_MEASURE_MISMATCH` are distinct terminal states, and `asserts_not[TRANSFER]` forbids transfer to another universe, family, geography, population, instrument release, estimand or order basis. The `SOURCE_EQUIVALENCE` ceiling at `pre553_empirical_authority.py:78` ("exact semantic/source equivalence in exact scope") is a source-side equivalence, not a temporal one; the contract uses it only as a required cross-universe input, never as a temporal-equivalence mint. Sustained.

One sequencing note, not a defect: `SOURCE_EQUIVALENCE` is a member of `RELATION_AUTHORITY_KINDS`, so a cross-universe comparison will need it to resolve through the source-relation path (`validate_relation_authority_only`, `:295-308`) in addition to the temporal path. The contract calls this out as "required only when the compared pair crosses source universes" but does not name the two-path resolution. That belongs in the implementation ceiling, not in the contract.

### 10. Does the contract constitute a rupture producer, threshold, event cause or trajectory? — NO

`RUPTURE_CANDIDATE_STATE` has exactly two members, is explicitly **not** a temporal relation state, is explicitly **not** produced by this contract, and carries `NO_CAUSAL_ATTRIBUTION`, `NO_AUTOMATIC_THRESHOLD_FROM_V553`, `NO_SCALAR_RUPTURE_MAGNITUDE`, `NOT_A_DIRECTIONAL_CLAIM`, `NOT_AN_ORDERED_RELATION`. I verified the V553 threshold/coefficient material really is excluded and the event-override slot really is `reserved_not_filled` (`:900`). Trajectory has no object, no `>=3` law, and the only anchor container is `anchor_refs` with `exact_cardinality: 2` (02, line 39) — a longer chain is a sequence of separate receipts. Gap is `TEMPORAL_GAP_INTERVENING` on `intervening_span_state`, preserved as typed unknown and explicitly barred from continuity, trend, rate and interpolation. Sustained. (Residual: `RUPTURE_CANDIDATE_STATE` is a declared closed state family with a `TYPED_CANDIDATE` member and no producer, i.e. a representable but unreachable state. That is the conservative direction and is disclosed as `no_producer_authorized`.)

### 11. Is the V553 citation correction sound, and is any provisional V553 numeric semantics laundered in? — LAUNDERING: NO. CORRECTION: RIGHT DATA, RIGHT IN SUBSTANCE, BUT IT PRESERVES A WRONG RECORD IDENTIFIER FROM F7

Two independent findings.

**(a) No laundering — sustained.** Every numeric literal in all 8 JSON artifacts is a structural count. No coefficient, threshold, deadband, weight, magnitude or scalar pressure value appears. The `conserved_historical_shape` block conserves only the *shape* (named authority required, two eligible anchors, explicit typed outcome, separate comparability and interpretation permission, direction/magnitude as typed labels) and explicitly excludes "the scalar pressure field and all coefficients", "the numeric thresholds and deadbands as adopted constants", and the one-family/one-country scope. The V553 module's provisional status is asserted with the exact compiler version, which I confirmed at `ddm_v553_schema.py:11`.

**(b) The correction is substantively right but carries F7's wrong label.** The contract corrects a claim it renders as *"H08 asserts 'ABSENCE != ZERO: Binding' citing V553_TEMPORAL_GAP_AND_ABSENCE_INDEX_SCHEMA"* and redirects the authority to the general typed-absence law at `pre553_empirical_objects.py:102-104,717-722` (verified accurate — those refs carry `NONCOMPARABLE`, `NOT_APPLICABLE`, `UNAVAILABLE`, `UNCERTAINTY_UNQUANTIFIED`, `OBSERVED_ZERO`, `ZERO_SUPPORT`, and `:717-722` enforces the zero/support distinction structurally). The rejection of the provisional V553 schema as current authority is correct and I confirm the provisional status.

However, **F7 did not label that claim H08.** In `ac444c5a:WORKER_RETURNS/PYAT-HQ204-F7-R1/02_HISTORICAL_CONSERVATION.json`, **H08 is "pressure-over-time (scalar temporal pressure field)"**, disposition `OBSOLETE IMPLEMENTATION DETAIL`, whose `must_not_inherit` is the list of pressure coefficients. The gap/absence record is **H10, "known gaps / absence / noncomparability"**, whose `historical_evidence` includes `ddm_v553_temporal_pressure.py:2772-2803` and whose disposition is `KEEP FUNCTION`. F7's own mis-attribution of the label "H08" (F7 propagates a stale "H08" from an earlier record; see `01_TEMPORAL_MEANING_MATRIX.json:597` and `05_GAP_RUPTURE_TRAJECTORY_LAW.json:44`) has been reproduced verbatim in `00_RETURN.md:157`, `05_OWNER_AND_SUCCESSION_MAP.json:63` and `08_FINAL_DISPOSITION.json:87` without cross-checking F7's own H-numbering. The consequence is traceability: a downstream reader following "H08" lands on the scalar-pressure record and not on the gap/absence record that actually asserted `ABSENCE != ZERO`. Because F7's 06 map also re-orders the conserved functions (F7: delta=3, trajectory=4, rupture=5, gap=6; the contract renumbers gap to 5 and drops trajectory), the wrong identifier is compounded. See Repair 6.

### 12. Is implementation now safely commissionable? — NOT YET; exact surface named

No. The contract is a sound *authority* derivation and a coherent *object* derivation, but three of its own laws are self-contradictory or non-binding at exactly the points an implementer must decide (Repairs 1, 2, 3), its state-derivation law is underdetermined and makes the claimed replayability false (Repair 4), the defect-closure enumeration it headlines is miscounted (Repair 6), and its implementation ceiling is not stated at all (Repair 5). Once Repairs 1-7 are made at documentary grain, implementation is safely commissionable and I bound the surface below.

## THE BOUNDED REPAIR SET

Repairs 1-3 are binding. Repairs 4-7 are required before an implementation commission can be issued. None requires architecture reopening, none requires Astra, and none changes the authority-kind count.

**Repair 1 — the fourth "order basis kind" is not an order basis.**
`04_TIME_ORDER_BASIS_LAW.json` `ORDER_UNKNOWN_NONCOMPARABLE` either (a) becomes a typed *refusal* and stops being a value of `temporal_order_basis_ref`, with the receipt's `temporal_order_basis_ref` becoming conditionally required (absent when ordering is unknown), or (b) is retained as the exhaustive "no basis" value and `TEMPORAL_ORDER_UNAUTHORIZED` / `TEMPORAL_NONCOMPARABLE` become its *only* two outcomes, with 02's wording "Exact ref to the **authorized** order basis" and 01's `refusal_if_absent` reconciled to it. Either way the two-reachable-ways problem for `TEMPORAL_ORDER_UNAUTHORIZED` must be removed.

**Repair 2 — bind authorization, basis and direction to each other.**
Add the missing cross-field constraints: `relation_state = TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` requires `relation_status = ORDERED_RELATION_AUTHORIZED`, a bound basis with `permits_direction: true`, and `direction_claim ∈ {INCREASE, DECREASE, NO_AUTHORIZED_CHANGE}`. Conversely `relation_status = ORDER_RELATION_REFUSED` requires `direction_claim = DIRECTION_NOT_CLAIMABLE`. `DIRECTION_NOT_CLAIMABLE` must be forbidden whenever the authorized state holds.

**Repair 3 — bind the deadband or drop the dependence.**
If `NO_AUTHORIZED_CHANGE` remains deadband-dependent: add a `deadband_authority_ref` to the required inputs and a `deadband_ref` to the receipt, make it required whenever `direction_claim = NO_AUTHORIZED_CHANGE`, and add the reason code for its absence (e.g. `DEADBAND_AUTHORITY_ABSENT`) with `DIRECTION_NOT_CLAIMABLE` as the fail-closed outcome. If no deadband is intended, redefine `NO_AUTHORIZED_CHANGE` as an exact-zero difference and delete the deadband dependence from NC-06 and 03. The present state — deadband required in prose, absent from every field — is not adoptable.

**Repair 4 — make `relation_state` deterministic.**
Add an explicit derivation rule with total precedence over simultaneously-failing conditions, covering at minimum: required authority absent (incl. the fail-closed `AUTHORITY_HASH_MISMATCH` / `AUTHORITY_SCOPE_MISMATCH` → temporal-receipt mapping, which is currently absent and would otherwise let a receipt carry a non-temporal authority state); multiple comparability surfaces failing; partial order with otherwise-satisfied requirements. Reconcile `relation_state_reason`'s cardinality (single enum vs `reason_codes` list) and define the selection rule. State explicitly which F7 candidate states are folded and where (`TEMPORAL_AUTHORITY_MISSING`, `TEMPORAL_AUTHORITY_CONFLICT`, `TEMPORAL_OUT_OF_SCOPE`, `TEMPORAL_INTERPOLATION_NOT_AUTHORIZED`, `TEMPORAL_PROBE_ONLY`), or restore them. Give the positive state a non-empty reason or make the field conditionally required.

**Repair 5 — state the implementation ceiling.**
Name, as the bounded authorable surface: (i) the `TEMPORAL_COMPARABILITY` addition to `AUTHORITY_KINDS` **and** its `AUTHORITY_KIND_CEILINGS` entry (the current 18↔18 bijection means a bare kind addition is under-specified); (ii) the governed operations and scope envelope the ceiling admits; (iii) whether `TEMPORAL_RELATION_RECEIPT` becomes a `PUBLIC_OBJECT_FAMILIES` member (`pre553_empirical_objects.py:22-37`) and, if so, its `typed_state` binding in `STATE_FAMILIES` (`:61-125`) versus the receipt's `relation_state` field — the current model validates `typed_state` against a state family at construction (`:398-400`), and the contract does not say which carries `relation_state`; (iv) the two-path resolution for cross-universe pairs (`SOURCE_EQUIVALENCE` as a `RELATION_AUTHORITY_KINDS` member plus the temporal path); (v) the explicit non-surface: no grain enum, no time field on `EmpiricalFact`, no trajectory object, no rupture producer, no scalar field, no new selector. Also record that the 18↔18 ceiling bijection means the new kind arrives with exactly one new ceiling and zero new authority *states*.

**Repair 6 — correct the documentary record.**
(a) `00_RETURN.md:25` must say **12** `TEMPORAL_RELATION_STATE` members (and 11 `TEMPORAL_NONCOMPARABLE` reason codes, not the reverse). (b) The `H08` identifier in `00_RETURN.md:157`, `05_OWNER_AND_SUCCESSION_MAP.json:62-65` and `08_FINAL_DISPOSITION.json:86-89` must be corrected to **H10** for the gap/absence record, and the H08 scalar-pressure record referenced where the contract actually means it. (c) The conserved-function indices should be reconciled with F7's own succession-map indices or explicitly declared renumbered. (d) `00_RETURN.md:57-58` and `02:177` cite the source-side producer at `:639-640` and `:680-681`; the third site `:686-687` (`MEASURE_WEIGHT_BASIS_NOT_ALLOWED_BY_RULE`) is omitted and should be added for completeness.

**Repair 7 — close the backfill-name overlap.**
State the non-collapse law explicitly: `TEMPORAL_NONCOMPARABLE` remains a member of `FORBIDDEN_BACKFILL_TARGET_STATES` **as a string**, and the adopted rule is that no `TEMPORAL_RELATION_RECEIPT` may be a backfill target and no pair whose `relation_state` is `TEMPORAL_NONCOMPARABLE` may be backfilled into. Do not remove the literal from the tuple and do not retype the tuple; add the direction the promotion creates.

## BOUNDED IMPLEMENTATION SURFACE (post-repair)

If Repairs 1-7 are made, implementation is safely commissionable and is bounded to:

- `rawlsing_next/pre553_empirical_authority.py` — one kind added to `AUTHORITY_KINDS`; one matching `AUTHORITY_KIND_CEILINGS` entry; no new selector, no new authority state.
- `rawlsing_next/pre553_empirical_objects.py` — at most one new public object family and its state binding, **only** if the receipt is a public object; no change to `EmpiricalFact.REQUIRED_FIELDS`, no grain enum.
- one new module for the comparison operation and the receipt producer, consuming only existing authority kinds via `require_positive_authority` / `AuthorityRegistry.resolve_exact`.
- no change to `FORBIDDEN_BACKFILL_TARGET_STATES` membership, `FAIL_CLOSED_STATES`, `FORBIDDEN_SELECTOR_TOKENS`, `EmpiricalFact`, `m1_temporal_v554_admission_dedup.py`, or any V553/V554 module.

Explicitly **not** authorable under this contract: a trajectory object, a `>=3`-anchor law, a grain enum, an `EmpiricalFact` time field, a rupture producer or threshold, a temporal-gap object, a scalar temporal-pressure field, interpolation or midpoint logic, and any consumption of the receipt downstream (HQ204 node H-D).

## WHAT THIS REVIEW DOES NOT ESTABLISH

It does not establish that a lawful temporal comparison exists. It does not adopt the contract, issue a warrant, authorize implementation, or repair production code. All line references above were read at the exact commits named in the header; nothing was inferred from a working tree that differs from them.

## ANSWER TO Q12, PLAINLY

`safe_to_commission_implementation = false` today.
`smallest_blocking_documentary_repair = Repairs 1 + 2 + 3`, then Repairs 4-7 before an implementation commission is issued.
`architecture_reopen_required = false`. `astra_referral = false`. `material_authority_conflict = false`.
