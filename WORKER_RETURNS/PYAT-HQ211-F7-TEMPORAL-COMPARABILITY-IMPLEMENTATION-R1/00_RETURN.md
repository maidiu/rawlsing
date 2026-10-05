# PYAT HQ211 — F7 TEMPORAL COMPARABILITY SOURCE-FREE IMPLEMENTATION — R1

**Disposition: `F7_TEMPORAL_COMPARABILITY_IMPLEMENTATION_COMPLETE__READY_FOR_HOSTILE_REVIEW`**

- Code-bearing commit: `caf6644a6033fb27c981ff0deb8d6e1b7d3d824e`
- Startup/authorization tip: `7b2eaf6cb15433f7919af8f9ed3dd2701b8423df`
- Accepted contract implemented: `c57a96897788108db7b194e4e51691d1ca8ab729`
- Hostile-review predecessor: `f1a0dbbc8491e0d23df9005abd55b83e0261424e`

## Launch posture

`00_COMMISSION.md` is marked `BOUND_QUEUED`. The tip commit `7b2eaf6cb` carries
`01_HQ212_IMMEDIATE_LAUNCH_AUTHORIZATION.md`, which supersedes only the
queue/slot clause and keeps every semantic, write-terrain, qualification, hold and
return requirement binding. I executed under that additive authorization.

Per the shared-store law I did **not** clone and did **not** use the canonical
clone concurrently. I created the single authorized isolated sparse worktree at
`~/Desktop/Rawlsing_Worktrees/hq211-f7-implementation-r1`, verified branch and
HEAD against the commissioned tip, and left the canonical clone detached rather
than checked out on this branch.

## Production surface — exactly as commissioned

Three surfaces, nothing more:

1. `rawlsing_next/pre553_empirical_authority.py` — adds `TEMPORAL_COMPARABILITY`
   to `AUTHORITY_KINDS` and exactly one matching `AUTHORITY_KIND_CEILINGS` entry.
   Base blob `ca65a7fd4d52f0c44447434559b1d09412e7aa39`. The diff is 5 added lines
   and nothing else.
2. `rawlsing_next/pre553_temporal_comparability.py` — the bounded module.
3. `rawlsing_next/tests/test_pre553_temporal_comparability.py` — the focused court.

The ceiling text is the contract's, and it explicitly denies downstream consumer
power: *operation-scoped comparability and ordering of exactly identified temporal
anchors for one governed use; production of the bounded temporal relation receipt;
no downstream consumer power.*

`FORBIDDEN_BACKFILL_TARGET_STATES`, `FAIL_CLOSED_STATES`, `FORBIDDEN_SELECTOR_TOKENS`,
`EmpiricalFact.REQUIRED_FIELDS`, `m1_temporal_v554_admission_dedup.py` and every
V553/V554 module are untouched.

## Contract law, implemented without widening

The receipt is a module-local closed content-addressed object. It is **not** a
`PUBLIC_OBJECT_FAMILIES` member, its `relation_state` is **not**
`CanonicalSemanticObject.typed_state`, and no `STATE_FAMILIES` edit was made.

All 12 states are individually reachable. Selection is the deterministic
precedence, highest first; every detected failure is retained in
`comparability_requirement_results` while exactly one state goes public.
`relation_state_reason` is exactly one scalar under state-local precedence, and a
positive state's reason is nonempty.

Order law is the contract's: `CALENDAR_TOTAL_ORDER`, `FAMILY_LOCAL_ORDINAL` and
`PARTIAL_ORDER_NO_DIRECTION` are the three authorized bases;
`ORDER_UNKNOWN_NONCOMPARABLE` is a typed refusal, carries no basis ref, and maps
uniquely to `TEMPORAL_ORDER_UNAUTHORIZED / NO_PERMITTED_ORDER_BASIS_APPLIES`.
I proved the uniqueness is real: the module raises if that state is ever reached
by another derivation.

`TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` requires the full conjunction — pair
COMPARABLE, `ORDERED_RELATION_AUTHORIZED`, a direction-permitting basis, a
claimable exact direction, an exact delta present, and all required authorities
positive. Partial order refuses both the relation and the direction.

`NO_AUTHORIZED_CHANGE` requires an exact zero. There is no deadband, tolerance,
inherited V553 threshold, or epsilon, and floats are refused outright. A one-unit
delta is never silently zero.

Cross-universe comparison requires two independent positive paths: the
source-relation owner resolves `SOURCE_EQUIVALENCE` through the existing
`validate_relation_authority_only` path, and this module separately resolves
`TEMPORAL_COMPARABILITY` and consumes that exact ref. Neither mints nor implies
the other, and a same-universe pair needs no equivalence at all.

`PROBE_ONLY` yields **no receipt**, which is a refusal rather than a state.

## Two implementation defects I found and fixed in my own work

Recording these because a hostile reviewer should not have to rediscover them.

**The basis ref is not an authority ref.** My first pass resolved
`temporal_order_basis_ref` through `registry.require()`, which raised
`authority_ref must be AuthorityRef or mapping`. The contract types that slot as an
`ExactRef`. It now carries a separate exact
`temporal_order_basis_authority_ref` resolved under `TEMPORAL_EVIDENCE`, and the
`ExactRef` is never resolved as an authority.

**Salted `hash()` in my own court.** My first fixture derived ref and authority
hashes from Python's `hash()`, which is randomized per process by
`PYTHONHASHSEED`. That would have made every replay-identity assertion pass in one
process and fail in the next — a false green in exactly the property this lane is
supposed to prove. It now uses SHA-256 over deterministic tags.

## One typed residual, escalated rather than silently repaired

**`ORDERED_AUTHORIZED_BASIS_WITHOUT_SUPPLIED_DELTA`.** If a direction-permitting
authorized basis has every authority positive but no exact signed delta supplied,
`compare_temporal_anchors` raises `TemporalComparabilityIntegrityError` and mints
nothing.

The closed 12-state vocabulary has no ordered-without-delta state.
`TEMPORAL_ORDER_UNAUTHORIZED` has a *unique* no-basis derivation that the order
law forbids reusing, and the other negative states are all wrong here because the
pair is genuinely comparable and genuinely ordered. Three tempting repairs were
available and all of them were out of bounds: inventing a thirteenth state widens
the vocabulary, reusing state 9 breaks the unique-derivation rule, and silently
treating absence as zero would manufacture a false `NO_AUTHORIZED_CHANGE` — the
exact "absence ≠ zero" noncollapse this contract exists to protect.

So the request is refused as invalid and the gap is reported. It is recorded in
`02_STATE_AND_PRECEDENCE_RECEIPT.json` for hostile adjudication.

## Qualification

| Court | Result |
|---|---|
| Focused court | **49 passed**, 0 failed/error/skipped/xfailed |
| Authority + source-relation regression, baseline | 159 passed |
| Authority + source-relation regression, after | 159 passed |
| **Failure-ID set delta** | **empty — no regression introduced** |
| Combined | **208 passed** |

I captured the baseline by stashing my own implementation, running the regression
courts, and restoring it, then diffed the two failure-ID sets. Empty delta is
the claim; "tests still pass" alone would not have been the claim.

The no-F8 proof is AST-level: the module's only internal imports are
`pre553_empirical_authority` and `pre553_empirical_objects`. My first attempt at
this test grepped the source text for forbidden words and **failed against my own
docstring**, which legitimately names those non-surfaces while disclaiming them.
Word-matching a disclaimer is a bad test; the AST check is the real proof.

## Retained residuals, not solved here

`IDENTITY_CONTRACT_INSTANCE_MISSING`,
`TIME_INDEXED_OBSERVATION_OBJECT_ABSENT`,
`TIME_REFS_CURRENTLY_EXACT_AND_GRAIN_UNVALIDATED`,
`RUPTURE_CANDIDATE_PRODUCER_AND_CALIBRATION_AUTHORITY_UNCONSTITUTED`,
`TEMPORAL_GAP_OBJECT_ABSENT__TYPED_SPAN_STATE_SUBSTITUTE`, and
`FAMILY_SCOPED_TIME_MAPPING_MATERIAL_UNADOPTED` remain exactly as the contract
left them. No architecture widening was performed to make any of them disappear.

## Scope

No F8 import or consumption. No source access. No self-adoption. No C7. No
actor/person work. No write outside the three commissioned surfaces and this
return directory. Writes confined to
`WORKER_RETURNS/PYAT-HQ211-F7-TEMPORAL-COMPARABILITY-IMPLEMENTATION-R1/**`.

Terminal: `HQ211_F7_TEMPORAL_COMPARABILITY_IMPLEMENTATION_RETURNED__HOSTILE_REVIEW_REQUIRED`