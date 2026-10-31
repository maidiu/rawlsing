# RED variants and trust boundary

**Lane:** `PYAT-F7-P07-RECOVERY`
**Candidate:** `candidate/temporal_method_candidate.py`
**Status:** TEST-ONLY, sourcefree, no production receiver, no P07 native code.

## 1. Trust boundary

```text
caller-supplied exact anchors/observations
        |
        v
candidate temporal method
  |-- time geometry ------> current TEMPORAL_EVIDENCE AuthoritySnapshot
  |-- surface attestations -> current AUTHORITY_KINDS (no TEMPORAL_COMPARABILITY)
  |-- cross-universe ------> current outer SourceRelationResolver
  |                          (SOURCE_SEMANTIC_EQUIVALENCE, exact pair/scope/use)
  |
  +-- no historical nested owner
  +-- no authenticated P07 entrypoint
  +-- no native extension
  +-- no production import
  +-- no TEMPORAL_COMPARABILITY mint
```

What the candidate can establish at test grain:

- exact point/closed-interval geometry over already-authorized temporal extents;
- exact as-of eligibility from authorized publication/validity/revocation points;
- a noncomparability refusal with retained failed surfaces;
- an exact delta only when every declared surface is positively attested and the
  geometry supplies a strict order;
- a cross-universe comparison only when the present current outer resolver
  returns an exact authorized relation for the exact pair, scope and use.

What it cannot establish:

- that construct, item, route, population, weight or time are scientifically
  comparable;
- that a `TEMPORAL_COMPARABILITY` authority exists;
- that a current nested/authenticated P07 owner exists;
- that a historical native P07 owner is safe;
- that an N9/N10W production receiver has accepted the result;
- that a measured EVS or other wave pair exists.

The candidate is therefore a **method candidate**, not a scientific comparability
issuance and not a secure machine attestation.

## 2. RED variants and exact handling

| RED variant | Attack | Candidate result | Evidence |
|---|---|---|---|
| Same numeric values | Two waves carry equal values | NOT_COMPARABLE unless every required surface is separately attested; equal numbers do not satisfy a surface | `test_equal_numbers_do_not_imply_comparability_when_surface_is_not_satisfied`, `test_same_numeric_value_without_construct_attestation_is_not_comparable` |
| As-of timestamp | Same as-of time is treated as proof of comparability | NOT_COMPARABLE when the time surface attestation is absent; as-of selection is only eligibility | `test_as_of_timestamp_without_time_attestation_is_not_comparability`, `test_as_of_selection_excludes_future_publication_and_does_not_pick_latest` |
| Same wave/label/family | Shared label or wave index is used as a shortcut | No candidate path uses labels or wave indexes; exact refs and surface attestations are required | `test_same_numeric_value_without_construct_attestation_is_not_comparable` |
| Forged decision receipt | Duck-typed resolver or subclass returns/stands in for an authorized decision | Refused at construction: exact current concrete `SourceRelationResolver` required | `test_duck_typed_owner_and_resolver_subclass_are_refused` |
| Alias replacement | `HARMONIZATION_ALIAS` or provenance relation is substituted for equivalence | Refused by the present current outer resolver; no equivalence | `test_alias_relation_cannot_replace_source_equivalence` |
| Denied source relation | A DENIED equivalence relation is treated as positive | Refused; cross-universe state is `TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT` | `test_denied_source_relation_cannot_admit_cross_universe_pair` |
| Wrong source pair | A positive relation for a different universe pair rides the request | Refused; exact pair must match | `test_source_relation_for_a_different_universe_pair_is_refused` |
| Severed current producer | No current source-relation producer/resolver is supplied | Explicit `CROSS_UNIVERSE_EQUIVALENCE_ABSENT`; no silent pass | `test_absent_current_source_relation_producer_is_an_explicit_gap` |
| Fake cross-wave population pooling | Source equivalence plus equal numbers is used to compare different populations | Refused with `POPULATION_NOT_SHARED` even when equivalence is positive | `test_cross_population_comparison_is_refused_even_with_equivalence_and_equal_numbers` |
| Wrong route/construct/population attestation | An attestation for unrelated refs is attached to the comparison | Refused with `ATTESTATION_BINDING_MISMATCH:<surface>` | `test_route_attestation_bound_to_wrong_refs_is_refused` |
| Unissued original comparator | `TEMPORAL_COMPARABILITY` authority kind is asserted | Refused as `AUTHORITY_KIND_NOT_CURRENT`; current kind set is 18 and does not contain it | `test_historical_temporal_comparability_kind_is_not_a_current_authority` |
| Stale/denied clock authority | A DENY `TEMPORAL_EVIDENCE` snapshot is used | `TEMPORAL_INSUFFICIENT_AUTHORITY`; no geometry/delta | `test_denied_temporal_evidence_authority_is_insufficient_authority` |
| Grain coercion | Point/interval or year/month grain mismatch is silently coerced | Refused with `TEMPORAL_GEOMETRY_GRAIN_MISMATCH` | `test_grain_mismatch_is_refused_without_coercion` |
| Interval midpoint | Overlap is converted to a midpoint or direction | `TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION`; delta null | `test_interval_overlap_never_becomes_midpoint_or_direction` |
| Float/deadband | Binary float, NaN, bool, string or fixed drift threshold enters the method | Refused as non-exact input; no deadband in the method | `test_float_nan_bool_and_string_are_refused_as_exact_inputs` |
| Future leakage | A version published after as-of is selected | Excluded into `future_excluded_refs`; not selected | `test_as_of_selection_excludes_future_publication_and_does_not_pick_latest` |
| Revoked clock | A version revoked before as-of is selected | Excluded; `NO_ELIGIBLE_VERSION` if none remain | `test_as_of_revoked_version_is_excluded` |
| Latest/default selection | Two eligible versions are resolved by latest/default | `AMBIGUOUS_AS_OF_SELECTION`; selected ref is null | `test_as_of_ambiguity_refuses_latest_selection` |
| Not-yet-valid version | A version becomes valid after as-of | Excluded into `not_yet_valid_refs` | `test_as_of_future_valid_from_is_not_yet_valid` |
| False current nested owner | Historical nested owner is claimed current | Current source probe says nested string absent, authenticated entrypoint absent, production importers empty | `test_receipts/current_surface_probe.json` |
| Historical owner revival | Historical source-relations blob is ported to make F7 positive | Not done; historical 163/163 run only in its exact isolated worktree | `test_receipts/historical_probe.json`, `historical_hq235_163.log` |

## 3. Named RED-on-mutation / GREEN-on-restore evidence

`candidate/mutation_check.py` mutates a temporary copy, runs the named test, and
requires the exact mutation to be detected. The untouched candidate must pass.

```text
disable_attestation_binding_check
  test_route_attestation_bound_to_wrong_refs_is_refused
  mutated_exit=1, restored_exit=0
  RED_ON_MUTATION_GREEN_ON_RESTORE

accept_nonpositive_authority
  test_denied_temporal_evidence_authority_is_insufficient_authority
  mutated_exit=1, restored_exit=0
  RED_ON_MUTATION_GREEN_ON_RESTORE
```

Receipt: `test_receipts/mutation_receipt.json` (`status: PASS`, `failures: 0`).

The candidate court also contains the input-level restore matrix
`test_fault_restore_matrix_named_reasons_red_then_green`, which removes each
required surface in turn, asserts the exact surface-specific absence reason, and
then restores the baseline positive. This is a named receiving assertion, not an
unrelated exception.

## 4. Trust boundary between science and machine attestation

Scientific comparability authority answers: **may these constructs, items,
routes, populations, weights and times be compared for this governed use?**

Secure machine attestation answers: **did this exact owner process produce this
exact decision under this exact custody path?**

Neither implies the other.

The historical F7 lineage increasingly hardened the second question (HQ217 to
HQ235) while leaving the first question dependent on an unissued
`TEMPORAL_COMPARABILITY`/EE12 authority. The historical owner path was then
defeated at the pure-Python custody boundary (HQ234/HQ236/HQ238) and at the
native memory/ABI boundary (HQ245-HQ248). This lane therefore separates:

- **method science**: recoverable in a TEST-ONLY candidate, with HOLD on
  original EE12 issuance;
- **secure owner**: NOT available; no nested-owner port and no native revival;
- **production receiver**: NOT available; explicit `REAL_RECEIVER_MISSING`.

P07 is only a prerequisite if a future selected production consumer genuinely
requires protected native cross-universe adjudication. That would need a separate
qualified commission for a native owner/issuer and an independent hostile review.
It is not required for the sourcefree method candidate and must not be built here.

## 5. Trust-boundary terminal

`FORGED_RECEIPT_ALIAS_AND_FAKE_POPULATION_POOLING_RED__UNISSUED_COMPARABILITY_KIND_RED__CURRENT_NESTED_OWNER_ABSENT__REAL_RECEIVER_MISSING__SCIENCE_AND_SECURE_OWNER_HOLD`.
