# Z08 — POSITIONED-SUBJECT POSSIBILITY + SPECIFICITY WALKBACK CLOSURE R1

Status: `PASS__BOUNDED_POSITIONED_SUBJECT_MODEL_AND_VISIBLE_SPECIFICITY_WALKBACK_IMPLEMENTED`

Repository: `maidiu/rawlsing`

Worker branch: `agent/verkhovod-z08-positioned-subject-walkback-r1`

User-mandated starting HEAD: `4e56e80f39edccf600534efbb8ab6956ca1bf0ba`

Worker command pre-command launch base: `c649d57ca660c5e2e38133698f5f12d1fc695d78`

## Dispositive return

Z08 closes the Authority-40 positioned-subject possibility / specificity-walkback implementation gap with one bounded source-backed learned-world service:

`rawlsing_next/source_backed_positioned_subject_possibility.py`

It does not alter PRE553 I03, QuerySpace, V3, structural admission, or actor semantics.

The implemented law is deliberately conservative:

`EXACT SOURCE-BACKED CONDITIONAL POSSIBILITY`

then, only if exact positioned support is absent or unresolved,

`EXPLICIT AUTHORITY-DECLARED SPECIFICITY WALKBACK`

never:

`EXACT QUERY FAILURE -> SILENT BROADENING`.

## Model/rule closure

Z08 freezes:

`POSITIONED_SUBJECT_EXACT_CONDITIONAL_WITH_GOVERNED_WALKBACK@1.0.0`

with algorithm:

`EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION`.

This resolves the open model-rule question without introducing an unearned statistical model. The service consumes exact producer-owned source-backed possibility slices and their typed upstream support/uncertainty states. It does not invent a new support threshold, nearest-neighbor rule, smoothing method, extrapolator, semantic similarity function, or actor prediction model.

Every invocation must carry exact model and walkback authority refs. Every proxy step must have an exact proxy authority ref that is positively listed in the model-rule authority envelope.

## Exact lane

The exact requested positioned grain binds:

- exact subject correlation ref;
- exact target ref;
- exact source universe and release;
- exact downstream-owned subject-fact refs used only as query criteria;
- exact empirical coordinate refs;
- exact comparability-authority refs;
- exact effective-time material;
- requested projection identity.

An exact supported slice returns `EXACT_SUPPORTED`.

An exact `UNDERPOWERED`, `UNRESOLVED`, or `UNAVAILABLE` slice leaves the exact disposition `UNRESOLVED` even if a proxy is later found.

An absent exact slice likewise remains `UNRESOLVED` with `EXACT_POSITIONED_STRATUM_ABSENT`.

Exact `VALID_EMPTY` and `NONCOMPARABLE` are preserved as terminal exact states and are not overwritten by broader evidence.

## Proxy/walkback lane

Walkback is an explicit finite authority object, not a search heuristic.

Each step records:

- retained conditioner ids;
- dropped conditioner ids;
- specificity loss count and exact fraction;
- proxy authority ref;
- source/release identity;
- evidence ref/state when present;
- exact attempt state/reason.

The ladder must strictly lose specificity at every step. V1 forbids cross-source and cross-release proxies; either fails closed.

A selected proxy is marked `EXPLICIT_LOWER_SPECIFICITY_PROXY`, `is_exact_fact=false`, and `is_actor_belief=false`.

Thus:

`PROXY != EXACT FACT != ACTOR BELIEF`.

## Replay

The result hash/replay identity includes the exact query, model-rule hash, authority refs, exact disposition, consumed evidence refs, fallback path, specificity losses, selected proxy evidence, source/release/target identity, and epistemic ceiling.

Unused evidence is deliberately excluded from replay determinants. Adding an irrelevant unconsumed slice therefore does not invalidate an otherwise identical result.

`verify_positioned_subject_possibility_replay(...)` reruns the bounded rule and rejects result-hash or semantic-material drift.

## Frozen validation obligations

All command-required cases are implemented and exercised:

1. exact supported positioned subject — PASS;
2. exact underpowered positioned subject -> unresolved exact + explicit broader proxy — PASS;
3. absent exact stratum -> unresolved exact + admissible surrogate ladder — PASS;
4. no admissible surrogate -> unresolved — PASS;
5. mixed-source / unauthorized proxy -> fail closed — PASS;
6. replay of fallback path and specificity-loss disposition — PASS.

Additional hostile coverage proves:

- cross-release proxy failure;
- non-monotone ladder rejection;
- specificity loss participates in result identity;
- valid-empty noncollapse;
- noncomparability noncollapse;
- conditioner/query source binding cannot silently bridge;
- unlisted proxy authority is rejected;
- irrelevant unconsumed evidence does not perturb replay identity.

The committed unit suite contains 13 tests. The exact committed production/test content was exercised in a bounded local compatibility harness and passed `13/13`; see `TEST_RECEIPT.txt` for the execution boundary.

## Noncollapse / jurisdiction

The implementation asserts no:

- actor belief;
- actor response;
- actor disposition;
- actor preference;
- causal biography;
- normative recommendation;
- structural position;
- V3 state.

Downstream-owned generated facts are criteria only and remain downstream-owned.

The result is empirical possibility geometry/projection under exact source/model authority, not an individual prediction.

## Non-mutation

Z08 does not modify:

- `rawlsing_next/pre553_empirical_query.py`;
- `rawlsing_next/pre553_empirical_objects.py`;
- QuerySpace;
- PRE-V3 semantics;
- V3/actor semantics;
- architecture-selection surfaces.

No sibling findings were consumed.

## Evidence authority consumed

- Authority 40: `40_LONG_MEMORY_DELTA_FULL_JOIN_AND_BOUNDED_ZERO_LOSS_REPAIR_AUTHORITY.md`;
- accepted D03 learned-world succession: `fa6ea6c957bd350b31e5adb504dbb854a0464dfa`;
- accepted C07 four-court reconciliation: `dc4a263d7e1d402fcb325dec1ebe9f02765e0ff8`;
- accepted positioned-subject authority court: `25e8e99d471af561fd590122c83a5b3fdceaaad5`;
- Long Memory zero-loss baseline: `669062e6c319f31214f403939dded91300639bde`.

Production implementation commit: `269de28814d2187fedebbedbbecd5b63f6a67521`.

Production test commit: `f4158912a230f682a68f28d2aff5ee9051ce0a78`.

`Z08_POSITIONED_SUBJECT_WALKBACK_R1_COMPLETE`
