# PYAT HQ273 C01 — Positive / malicious-negative test suite, exact run record, and the next source-bound warrant

**MARKER:** `DEVELOPMENT_FIXTURE_ONLY`. **Executor:** the accepted
`rawlsing_next.pre553_empirical_query.execute_empirical_query` / `replay_empirical_query`.
No counting stub, no parallel API, no bypass of auth/grammar gates.

---

## 1. Exact run record

| Field | Value |
|---|---|
| Code commit under test | `bec158a0c5aed7e7ad2f8b164fedfbf205e722e0` (detached at `6e9e1ddb7` + 1) |
| commission tip / control base | `6e9e1ddb766861da273aa75c7b692547506acc25` / `e82508091214d2543cfd1a2d8f7ff5ea4b5fe48f` |
| interpreter | `/usr/local/bin/python3`, CPython 3.11.3, pytest 9.0.2, pluggy 1.6.0, platform darwin |
| worktree | `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/hq273/c01` |
| command | `python3 -m pytest rawlsing_next/tests/test_hq273_c01_true_i03_conditioned_denominators.py -v -p no:cacheprovider` |
| collection | **19 tests collected**, 19 selected, 0 deselected |
| result | **19 passed, 0 failed, 0 errors, 0 skipped, 0 xfailed, 0 xpassed** |
| wall time | ~0.52 s |

### Test-by-test ledger

| # | Test | Kind | Asserts |
|---|---|---|---|
| 1 | `test_fixture_is_source_free_and_three_distinct_questions` | positive-grain | 3 distinct question refs, 10 respondents, fixture-only identities |
| 2 | `test_two_nested_conditionals_are_two_distinct_native_facts` | **positive** | two `SUPPORTED` facts; distinct predicate/query/fact refs; denominators 5 vs 3; `raw_numerator_support` semantic pinned |
| 3 | `test_denominator_member_refs_are_exact_and_nested` | **positive** | R2 ⊆ R1 ⊆ S; member refs exist in this release only; no duplicates; risk set strictly larger |
| 4 | `test_unweighted_raw_measure_and_no_authorization_leak` | positive | RAW, no weighted fields, `UNCERTAINTY_UNQUANTIFIED`, target-use operation bonded, all fact-closure authorities prefixed `HQ273-C01-AUTH-` |
| 5 | `test_cell_projection_matches_independent_oracle` | **positive** | Y=1 cells 3 and 1; Y=0 cells 2 and 2; `OBSERVED_POSITIVE`; q1/q2 visibly differ |
| 6 | `test_both_facts_replay_deterministically` | **positive** | `replay_empirical_query` reproduces the exact fact ref and replay ref for both |
| 7 | `test_no_cross_person_join_structurally` | positive | each denominator member carries exactly one Y, one A and one B event of its own; no member carries 4 events |
| 8 | `test_empty_condition_yields_typed_zero_support` | negative | `ZERO_SUPPORT`, denominator 0, numerator 0, empty member refs, zero-support detail |
| 9 | `test_non_substantive_states_are_excluded_from_both_denominators` | negative | P08 (B=DK), P09 (Y=DK), P10 (A=REFUSAL), P06/P07 (A=1) absent from both |
| 10 | `test_value_equality_alone_does_not_exclude_refusal` | **negative / hazard** | unguarded predicate admits P08/P09/P10, denominator 8, fact typed `UNRESOLVED`; guarded excludes all three |
| 11 | `test_routing_state_exclusion_is_not_coerced_to_nonmembership` | negative | `ROUTING_UNKNOWN` → `UNAVAILABLE` / `RISK_SET_UNAVAILABLE`, zero denominator, empty members |
| 12 | `test_authority_substitution_is_refused` | negative | non-`PREDICATE_GRAMMAR` query authority → `UNAVAILABLE` / `MISSING_REQUIRED_AUTHORITY`, zero denominator |
| 13 | `test_forged_target_use_operation_is_refused` | negative | query naming a foreign-operating target-use permission fails closed; an extra forged snapshot in the registry does not license a fact |
| 14 | `test_mismatched_release_ref_is_refused` | negative | query scoped to another sealed release fails closed with zero denominator |
| 15 | `test_branch_cohort_only_pattern_cannot_distinguish_conditions` | **negative / hazard** | the frozen GT12 `DERIVED_BRANCH_COHORT`-only shape yields ONE denominator of 10 and identical member sets for both q1 and q2 |
| 16 | `test_no_float_or_actor_effect_in_either_fact` | positive-invariant | `assert_zero_actor_v3_v2_effect` on both facts |
| 17 | `test_genuinely_distinct_from_a_three_dimensional_joint` | **negative / anti-substitution** | arity-3 joint over the same predicate has denominator 7 (= whole base S) and 8 cells — neither 5 nor 3 |
| 18 | `test_baseline_selected_query_shapes_are_green` | regression anchor | oracle N1=5, N2=3, q1=(3,5), q2=(1,3); both details "exact governed target distribution resolved" |
| 19 | `test_independent_oracle_shares_no_engine_code` | oracle independence | no engine symbol reachable from the oracle; oracle lives in the test file only |

**Positive : malicious-negative ratio** — 8 positive/invariant tests, 11 negative tests. No
negative-only court: the commissioned productive result (two replayable native
`EmpiricalFact`s with different conditioned denominators) is present and green.

### Baseline relevant tests (run separately on the same commit, all green)

| Test module | Result |
|---|---|
| `rawlsing_next/tests/test_pre553_empirical_query.py` | 32 passed |
| `rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py` | 10 passed |
| `rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py` | 8 passed |
| `rawlsing_next/tests/test_pre553_source_backed_c11_facade.py` | 10 passed |
| `rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py` | 50 passed |
| `rawlsing_next/tests/test_pre553_query_frontier_hostile.py` | 14 passed |
| `rawlsing_next/tests/test_pre553_replay_audit.py` | 54 passed |
| `rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py` | 72 passed |
| `rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py` | 39 passed |

No baseline test was modified. No production, semantic-source, registry, GT12, PRE-MAIN or
permission file was touched; the commission's "at most two existing/new source/test paths"
budget was spent on exactly two new files.

---

## 2. Preserved HQ271 byte identities

Verified unchanged at HEAD (`bec158a0c`), i.e. the sealed HQ271 source-free adoptions are not
disturbed:

| Object | Git blob | Status |
|---|---|---|
| HQ271 G1 ingress `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py` | `74e6ee826e8b6a2adebe84969fedcea5716d5b63` | PRESERVED |
| HQ271 G1 test `rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py` | `64b6c747f76a1909b676566e6b529ed10456d33b` | PRESERVED |
| HQ262-adopted G3 test `rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py` | `a1ec3dba504ff866b681d6bbe942d12a9e238257` | PRESERVED |

Operative **G0b remains unissued** and unfalse: nothing in this court requests, implies or
manufactures one.

---

## 3. The exact next source-bound warrant (proposal only, not self-issued)

The source-free court proves engine competence and isolates the real gaps. A source-backed
`q(Y|A) → q(Y|A,B)` still needs, in dependency order:

1. **Per-item source exposure and routing.** One `RoutingEligibilityFact@1.0.0` per scoped
   respondent per newly bound item, with `EXPOSED__PROVED` proved independently. `Q86C`/`Q8A`/
   `Q97` exposure may not be proxied by `Q86A`/`Q86B` answers, by shared block wording, or by
   `997` presence.
2. **Native domain + response-state semantics** for each newly bound item, with its own native
   code/value/missing labels and its own typed non-substantive states. The R5 native codes
   differ materially across items (`Q86*` `{0,1,9,997,998,-1}`; `Q8A` `{0..4,9,998,-1}`;
   `Q97` `{0..9,99,998,-1}` where **9 is substantive** and **99 is DK**). A single
   `numeric_9_is_missing` rule would corrupt the science.
3. **A condition-bearing owner-native conditional-query adapter** modelled on the adapter in
   this court, but over an accepted C11 release and with a `PREDICATE_GRAMMAR` authority that
   actually governs `SURVEY_RESPONSE_EVENT` EQ / AND and typed eligibility at the same
   respondent grain.
4. **Two distinct target-use permissions** naming `q(Y|A=a,S)` and `q(Y|A=a,B=b,S)` separately
   (or one explicitly permitted joint-to-conditional projection with independently typed
   numerator/denominator proofs), issued by the competent source-claim authority — **not** by
   this worker.
5. **A new exact risk-set / member-set hash** for the three-item complete-case scope, unless
   exact equivalence to the frozen GT2 19,210-member set is independently proved. Never preserve
   19,210 for historical green parity.
6. **A typed C1 source-backed conditional consumer** that accepts the exact fact, denominator,
   replay and permission refs. Source-free C1/G1 fixtures do not prove R5 occupancy.
7. **Explicit complete-case policy in the predicate.** Mandatory per finding F-1: value equality
   alone does not exclude typed non-substantive states.

### Explicit non-requests

This court does **not** request, and must not be read as requesting: any source read, any
source-use permission, any surveyed data, a T1, a T2, a G0b, an adopted GT3, an FF02 or
structural admission, a V3/actor effect, or a population inference. The 10-person synthetic
fixture carries **no** population, sampling or design meaning whatsoever.

**Terminal:** `HQ273_C01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`
