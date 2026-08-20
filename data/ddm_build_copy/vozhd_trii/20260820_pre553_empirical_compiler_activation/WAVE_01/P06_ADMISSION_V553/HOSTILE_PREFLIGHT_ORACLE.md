# PRE553 P06 — hostile preflight oracle

Status: `SPEC_ONLY__NO_RUNTIME_TESTS_IN_WAVE_01`

Every case below is a binding Wave-02/Wave-03 implementation obligation if HQ accepts the P06 contract.

## Admission boundary attacks

1. **No named structural-admission rule**: an exact, well-supported EmpiricalFact with matching human-readable labels returns `MISSING_STRUCTURAL_ADMISSION_AUTHORITY`; no StructuralEmpiricalAdmission may be positive.
2. **Explicit denial**: a named rule whose negative authority denies this use returns `ADMISSION_DENIED`; positive projection is forbidden.
3. **Discovery-score trap**: a high MI/NMI/Cramer's-V/tree/cloud/discovery score with no exact underlying EmpiricalFact + named structural rule cannot admit.
4. **Coordinate/stratum name collision**: empirical `income=low`, `religion=X`, `employment=unemployed`, region labels or similar strings cannot establish generated nine-stratum position.
5. **Survey-to-psyche trap**: neither prevalence nor conditional/joint fact may set actor belief, persona, identity, memory, knowledge or response.
6. **Structural target unresolved**: exact empirical fact + rule with unresolved target identity returns `STRUCTURAL_TARGET_UNRESOLVED`.
7. **Hash mismatch**: wrong EmpiricalFact, authority or receipt hash returns `INTEGRITY_FAILURE` before semantic evaluation.

## Typed-state attacks

8. **Observed zero**: an exact observed-zero measurement remains distinct from missing and may be `ADMITTED` only when the named rule permits it.
9. **Zero support**: zero-support never means structural or actor impossibility; absent a rule explicitly governing the typed state, no positive admission.
10. **Low support**: low support may pass only under the named rule's support/uncertainty requirements and must remain `LOW_SUPPORT` downstream.
11. **Unquantified uncertainty**: no generic confidence interval or certainty may be fabricated.
12. **Valid empty**: `VALID_EMPTY` remains distinct from denial, missing authority, zero-support and integrity failure.
13. **Deferred**: `ADMISSION_DEFERRED` is nonpositive and stays blocked until the named external owner resolves the exact requirement.
14. **Multiple blockers**: primary state follows frozen fail-closed precedence, while every applicable negative/blocking reference remains preserved.

## Source-plurality attacks

15. **Same label, different universe**: two source universes with harmonized labels remain distinct absent exact source-relation authority.
16. **Shared provenance**: derivative/original provenance does not itself authorize respondent linkage, pooling or backfill.
17. **Multi-universe fact**: a structural admission over more than one universe requires exact externally owned source applicability/relation/composition refs.
18. **Disagreement**: conflicting sources are preserved separately when the named rule permits plural evidence; otherwise return typed noncomparability/conflict. Never source-majority or average by default.
19. **Duplicate support trap**: the same underlying source evidence cannot count twice merely because it arrives under two aliases or provenance paths.

## Temporal-jurisdiction attacks

20. **Rule applicability mismatch**: an empirical fact outside the structural-admission rule's own effective period/geography may return `TEMPORAL_SCOPE_MISMATCH`; P06 does not repair it.
21. **Timestamp-is-not-V553**: presence of a timestamp does not itself imply a V553 temporal operation.
22. **Point fact vs temporal relation**: a point-in-time admitted structural fact may cross P06 without P06 deriving persistence, drift, reversal, rupture, sequence or baseline.
23. **Missing cross-time authority**: comparison/harmonization requiring temporal or source comparability remains V553/external-authority work and fails closed there.
24. **Use-chain scope**: U1 may lawfully need no new V553 meaning while U2 over the same admission later requires V553. U1 never permanently exempts U2.

## V553 ingress attacks

25. **Raw EmpiricalFact bypass**: V553 rejects direct `EMPIRICAL_FACT`, raw C11 incidence, discovery receipt and diagnostic score as semantic intake.
26. **Nonpositive admission**: a nonpositive admission can be referenced for replay/blocking but cannot produce positive V553 temporal semantic objects.
27. **Request ownership**: P06 cannot fill in `V553_REQUIRED`, `V553_NOT_REQUIRED_FOR_THIS_USE`, required temporal operations or temporal-operation rules on its own authority.
28. **No temporal object fabrication**: P06 may not mint TEMPORAL_KEY, TEMPORAL_OBSERVATION, TEMPORAL_RELATION or TEMPORAL_LIMIT identities.

## M1 projection attacks

29. **Exact slot completeness**: every positive direct-admission projection carries all 17 accepted M1 direct consumer slots exactly; omission fails closed.
30. **Positive-only basis**: only `ADMITTED` receipts can be emitted as `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION` candidates.
31. **Nonpositive projection trap**: missing/denied/deferred/noncomparable/valid-empty/integrity receipts remain negative/reference context and never masquerade as direct basis candidates.
32. **Independent SCR553 decision**: an `ADMITTED` projection alone does not prove `V553_NOT_REQUIRED_FOR_THIS_USE` or direct V554 eligibility.
33. **No P06 dedup**: P06 does not choose V554 signature, equivalence key, temporal completeness, duplicate precedence or canonical F1/F2/B1 identity.
34. **Order stability**: reordering set-like exact refs does not change the canonical projection hash; role/order-bearing arrays remain semantic.
35. **No latest/fuzzy tie-break**: filesystem order, readiness, latest-run state, nearest time or label similarity never selects a projection or authority.

## Compatibility attacks

36. **Legacy packet shape**: V551/V551J/V552/V552J shape or filename never authorizes structural meaning.
37. **Parity required**: compatibility admission requires exact compatibility EmpiricalQuerySpec/EmpiricalFact, a named compatibility rule and parity receipt for the intentionally retained structural meaning.
38. **Partial parity**: matching one aggregate or selected field is insufficient for compatibility admission.
39. **Missing parity**: no positive admission.

## Replay attacks

40. **Rule version change**: same empirical fact under a revised structural-admission rule produces a different admission identity; old receipt remains immutable.
41. **Exact replay**: same semantic inputs + same authority hashes reproduce the same admission ID/content hash/typed state.
42. **Cache irrelevance**: cache presence/absence cannot change admission truth or identity.
43. **Diagnostic irrelevance**: changing a nonauthoritative diagnostic ranking score cannot change admission identity or truth.

## Acceptance condition

P06 passes preflight only if HQ can synthesize an implementation contract from this oracle without weakening accepted D15 noncollapse, SCR553 temporal jurisdiction, accepted M1 direct consumer slots, source plurality, typed absence or deterministic replay.
