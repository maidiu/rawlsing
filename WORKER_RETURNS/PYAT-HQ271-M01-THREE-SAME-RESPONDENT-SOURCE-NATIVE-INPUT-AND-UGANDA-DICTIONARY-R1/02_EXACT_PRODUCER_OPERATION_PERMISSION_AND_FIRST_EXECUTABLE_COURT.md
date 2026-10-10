# PYAT HQ271 M01 — Exact producer, operation, permission and first executable court

**Scope:** permission analysis only. This document **grants nothing** and adopts nothing. It states, for HQ adjudication, exactly what an authenticated producer would need in order to execute `q(Y|A) → q(Y|A,B)` for the qualified R5 Q86A/Q86B/Q86C candidate, and exactly what remains missing.

---

## 1. The authenticated producer that already exists

No new producer is required, and the commission forbids new C11/FF02 product. The existing SRC02 lineage is:

| Layer | Existing artifact | Role |
|---|---|---|
| C11 projection (physical → semantic) | `rawlsing_next/wave1_r5_q86_c11_projection.py` | frozen R5 Q86A/Q86B→C11 binding, `CONTRACT_ID = GT12_A_R5_Q86_GOVERNED_C11_PROJECTION@1.0.0` |
| Authoritative source binding | `GT12-A-R5-Q86-SOURCE-SEMANTICS`, `GT12-A-R5-Q86-COMMON-RISK-ROUTING`, `GT12-A-R5-COUNTRY-ALPHA3`, `GT12-A-R5-Q86-CARRIER-REEXPRESSION`, `GT12-A-R5-Q86-C11-REPLAY`, `GT12-A-R5-Q86-FROZEN-TARGET-USE` | six `AuthoritySnapshot@1.0.0` records with exact content hashes |
| I03 empirical producer | `rawlsing_next/wave1_gt12_i03_positive_facts.py` | builds `EmpiricalPredicate` / `EmpiricalQuerySpec` / executes → `EmpiricalFact` |
| Execution gates | `execute_gt12b_i03_plan` (`:695`), `replay_gt12b_i03_execution` (`:717`) | enforces exact `SINGLE_UNIVERSE`, exactly one `EmpiricalFact`, `assert_zero_actor_v3_v2_effect` |

Both existing operations resolve over the **same** frozen predicate and the **same** frozen risk-set member set. That is the decisive property for the three-way step: `q(Y|A)` and `q(Y|A,B)` share one denominator construction, so no arithmetic over independent marginals is involved.

---

## 2. Exact owner input contract (unchanged, arity is already polymorphic)

`EmpiricalQuerySpec` (`rawlsing_next/pre553_empirical_objects.py:677`) required fields:

```
target_refs, target_arity_and_topology, condition_predicate_ref, risk_set_ref,
empirical_universe_refs, scope_refs, measure_basis_ref, requested_output_grain,
query_authority_refs
```

`target_arity_and_topology` is already built dynamically as
`{"arity": len(targets), "joint_order_semantics": "SEMANTIC_ORDERED", "components": [...]}`
(`wave1_gt12_i03_positive_facts.py:618-623`). **Arity 3 needs no schema change.**

`EmpiricalPredicate` (`:631`) required fields:

```
predicate_ast, predicate_hash, grammar_authority_ref, coordinate_question_value_refs,
risk_set_refs, scope_refs, same_respondent_binding_semantics, operator_semantics_refs
```

Existing instance semantics: `same_respondent_binding_semantics = "EXACT_SCOPED_RESPONDENT"`, operator `DERIVED_BRANCH_COHORT`, `typed_state = "PREDICATE_RESOLVED_AUTHORIZED"`.

`EmpiricalFact` (`:696`) required fields:

```
empirical_query_spec_ref, empirical_universe_refs, target_topology, condition_predicate_ref,
risk_set_ref, raw_numerator_support, raw_denominator_support,
weighted_numerator_support_if_authorized, weighted_denominator_support_if_authorized,
measure_basis_ref, response_state_semantics_ref, uncertainty_method_or_typed_state,
source_empirical_provenance_refs, replay_ref
```

Hard invariants already enforced at this class: `raw_numerator_support <= raw_denominator_support`; `SUPPORTED` requires a positive denominator; `OBSERVED_ZERO` requires positive denominator and zero numerator; `ZERO_SUPPORT` requires zero denominator. These are the typed states that make `VALID_EMPTY` a *lawful* outcome rather than a failure — the same mechanism that produced LiTS `D02_P3 = VALID_EMPTY`.

**C11 shared respondent identity** is not re-derived: the same `RowRespondentBinding` / `RespondentIdentity` records on carrier `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1` carry all three items. No cross-person join, no identity map, no second universe.

---

## 3. Proposed exact three-way operation

```
operation id      : GT3_R5_Q86A_X_Q86B_X_Q86C_RAW_JOINT_EXACT_RISK_SET@1
target order      : (Q86B conditioner, Q86A target) extended to (Q86B, Q86A, Q86C)
target_refs       : (qimpl 2fb3a62609dad4c1306d…,  qimpl 67f036c0efb7fb98ff4a…,  Q86C qimpl — NOT YET IDENTIFIED)
target topology   : SCALAR_SINGULAR x3
joint_order_semantics : SEMANTIC_ORDERED
risk_set          : FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1
risk_set hash     : 0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b  (19,210 members)
risk_set members  : UNCHANGED — same 19,210 exact member refs, same member-set SHA
measure basis     : AS3_QUERY_MEASURE_BASIS / RAW, weighted_support_authorized = false
predicate         : same _predicate_for_members construction, same EXACT_SCOPED_RESPONDENT semantics
progressive pair  : q(Y|A) = GT2 existing fact;  q(Y|A,B) = this new GT3 fact
```

The semantic component order is the frozen `Q86B` conditioner dimension then `Q86A` target dimension; `Q86C` must be appended as a **third, separately ordered dimension** with its own `target_domain_replay_ref`. The existing producer's comment ("Frozen semantic component order is Q86B conditioner dimension, then Q86A target dimension", `wave1_gt12_i03_positive_facts.py:687`) must be updated to a three-component ordering rule, and that ordering rule is itself an adoption item — component order is semantic, not cosmetic.

---

## 4. Can the existing SRC02 R5 GT2 Q86B→Q86A be extended for Q86C?

**Yes — and it is the smallest positive authorization available in either of the two commissioned options.** The reason is that `Q86C` differs from `Q86A`/`Q86B` only in its item-specific completion of one shared stem. It shares:

* the same shared stem and interviewer lead-in;
* the same routing exception list (`Not asked in ALG, EGY, MRC, SUD, TUN`) — so its eligibility regime coincides with `Q86A`/`Q86B` exactly;
* the same native value domain `{0, 1, 9, 997, 998, -1}` — verified identically in both the governed codebook and the physical SAV dictionary;
* the same respondent carrier and the same already-frozen risk set.

**But "the question exists with the same domain" is NOT an authorization.** What actually needs adopting, itemised:

| # | Required adoption | Exact artifact | Why it cannot be inferred |
|---|---|---|---|
| 1 | A `QUESTION_IMPLEMENTATION` identity for `Q86C` | new `question_impl.*` + identity sha256 | No frozen qimpl identity exists for `Q86C`; the producer fails closed on unknown question refs |
| 2 | A `SOURCE_NATIVE_DOMAIN` ref for `Q86C` | `Afrobarometer:R5:Q86C:SOURCE_NATIVE_DOMAIN`, page 53, codebook sha `7e02c649…` | Domain must be frozen from the governed codebook metadata + physical dictionary, not copied by resemblance to `Q86A` |
| 3 | A `TARGET_DOMAIN_REPLAY` ref for `Q86C` | `Afrobarometer:R5:Q86C:TARGET_DOMAIN_REPLAY` | Separate replay ref is mandatory; the domain is not its own replay |
| 4 | Extension of `GT12-A-R5-Q86-SOURCE-SEMANTICS` authority snapshot | add `Q86C` question ref + domain to `questions`/`domains`; add operation `R5_Q86C_NATIVE_RESPONSE_SEMANTICS` | Authority content hash changes; the existing snapshot cannot be edited in place without a new snapshot |
| 5 | Extension of `GT12-A-R5-Q86-COMMON-RISK-ROUTING` | add `Q86C` `exposure_predicate_ref` and routing operation | Exposure must be **independently proved** per risk-set member; response presence on `Q86C` is not exposure evidence |
| 6 | A new `RoutingEligibilityFact` per risk-set member for `Q86C` | `ELIGIBLE_APPLICABLE` / `NOT_ELIGIBLE` at `EXACT_SAME_RESPONDENT_ONLY` on the same respondent | 19,210 additional routing facts; no bulk inference allowed |
| 7 | Extension of `GT12-A-R5-Q86-CARRIER-REEXPRESSION` | add `Q86C` to `questions` and to the reexpression scope | The producer's `semantic_owner_transfer = false` invariant must be preserved |
| 8 | A new `TARGET_USE_PERMISSION` for the three-way operation | `GT3_R5_Q86A_X_Q86B_X_Q86C_RAW_JOINT_EXACT_RISK_SET@1` with an explicit permission ceiling | **This is the real gate.** GT1/GT2 target-use ceilings are arity-1 and arity-2 only. No grant exists or is implied by naming `Q86C`. |
| 9 | Extension of `GT12-A3-GT2-I03-QUERY` predicate-grammar authority | add `EmpiricalPredicate@1.0.0` / `EmpiricalQuerySpec@1.0.0` / `EmpiricalFact@1.0.0` coverage for the new operation | `_validate_query_authority` requires all three families to be permitted for the exact operation string |
| 10 | `R5Q86I03ExecutionBinding` extension | new field `q86c: R5Q86TargetBinding`, `gt3_query_operation: str`, `gt3_target_use: ExactTargetUseBinding` | The binding is a frozen dataclass; new claim ids need new validated fields |
| 11 | Reconciliation of the `COUNTRY_ALPHA3` coordinate slot | see `01_…json` → `dictionary.R5.country_identity_reconciliation` | The physical R5 SAV stores `COUNTRY`/`COUNTRY_ALPHA`, not `COUNTRY_ALPHA3` |
| 12 | Label-string reconciliation for `998` | frozen `"Refused to answer"` vs physical `"Refused"` | Must be an explicit, traceable mapping, never a silent overwrite |
| 13 | `GT12_FROZEN_CANARY_CONTRACT` currentness re-pin | new frozen contract commit/blob refs | The new operation is a *new* frozen canary currentness, not an extension of the old one |

**Item 8 is the one HQ must decide.** Items 1–7 and 9–13 are mechanical consequences of it. **This document requests item 8 on HQ's behalf and does not assume it.**

---

## 5. Smallest positive authorization request (one sentence)

> HQ extend the frozen R5 GT12 line with a single new target-use permission — `GT3_R5_Q86A_X_Q86B_X_Q86C_RAW_JOINT_EXACT_RISK_SET@1`, RAW measure, unweighted, over the unchanged risk set `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1` / member-set SHA `0484fa5c…`, arity 3 with `Q86C` appended as a separately ordered third dimension — together with the derived authority-snapshot and binding extensions in §4 items 1–7 and 9–13.

If HQ declines, the comparative fallback is a `SOURCE_NATIVE_TRIPLE_HOLD` for both commissioned options, and the next-smallest request is the heterogeneous `Q86A × Q8A × Q97` triple (§2.6 of `00_…md`), which costs three fresh domain/routing adoptions instead of one extension.

---

## 6. First executable court (for HQ to commission, not for this worker to run)

1. **Projection extension court** — add `Q86C` slot/domain/replay/binding to the R5 Q86 C11 projection; freeze the new qimpl identity and domain refs from `merged_r5_codebook_2.pdf` printed p. 53 + the physical dictionary; re-freeze the six authority snapshots; assert the risk-set member-set SHA is **byte-identical** to `0484fa5c…`.
2. **Exposure proof court** — independently prove `EXPOSED__PROVED` for `Q86C` on each of the 19,210 members. Reject the court if any member's `Q86C` exposure is inferred from `Q86A`/`Q86B` response presence, value substance, or block co-membership.
3. **Ordering-rule court** — adopt the explicit three-component semantic ordering rule and prove replay determinism under row reordering (the existing hostile test at `test_wave1_r5_q86_c11_projection.py` already asserts this for arity 2).
4. **Target-use adoption court** — adopt (or refuse) `GT3_…` as a `TARGET_USE_PERMISSION` with an explicit permission ceiling; refuse any structural, actor, causal or field-forge promotion.
5. **Execution court** — `execute_gt12b_i03_plan` → exactly one `EmpiricalFact`; `raw_numerator_support <= raw_denominator_support`; `SUPPORTED` requires a positive denominator; `VALID_EMPTY` / `OBSERVED_ZERO` / `ZERO_SUPPORT` are lawful typed outcomes, not failures. Then `replay_gt12b_i03_execution` for determinism.
6. **Progressive-reporting court** — report `q(Y|A)` and `q(Y|A,B)` from the *same* member set with the *same* predicate; any change in the A–B association across `Q86C` cells must be reported with the exact cell denominators of both, never as a difference of independent marginals.

---

## 7. Explicitly not requested here

* No respondent-row execution, no numeric execution, no frequencies, no weights.
* No new C11 product, no FF02 product, no field-forge relation, no actor.
* No new source-use permission for any file other than the already-warranted two Afro SAVs, and no new permission for `LiTS_I.dta` (not opened, not hashed).
* No G0b / T1 / T2, no EE12 / C7 temporal pair, no V3 / PRE-V3 service.
* No self-adoption. This return is advisory to HQ only.

---

## 8. Preserved independently of the S1 choice

LiTS **S2** (`ff02_executed=false`, `FF02_READY__NO_SOURCE_REOPEN_REQUIRED`) is unaffected by accepting or refusing the R5 S1 triple. S2 remains available on its own retained authority; it neither depends on nor is blocked by this recommendation.

**Terminal:** `HQ271_M01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`
