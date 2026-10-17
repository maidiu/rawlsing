# F6L Phase A — preregistered decision, admission and evidence court

**Freeze status:** committed and pushed before reading F6K.
**Role:** independent F6J reviewer continuation (F6L). Not F6K author, not HQ.
**Sealed startup:** `31123f370af50bdf036cab32dd6d7594b36a5f22`.

## 1. Basis preserved from F6J and the original author

The following are treated as inherited scientific results to preserve, not as
objects this court may rewrite:

- F6J independent freeze `e476ccc090ae0175a540e94c5c382d7e2a8453f0` and the
  receipt `825b2d8050b550f1d52d3129883584fee2ef36c2`: 12 worlds, 82/82 exact
  rational comparisons, 35 inherited native tests, 57 author tests (56/57 at a
  foreign staging path; the one failure is the author's custody path-suffix
  control).
- F6C author return `9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f`: World A
  standardization exactness, World B null distribution, covered mass `4/5`,
  widened uppers `19/25`, `41/50`, `17/50`; disclosed arithmetic correction.
- Pinned native producer at `1428c2e92bce1a49efd87378cb23df936d646dc5`:
  producer blob `fc5e37fa5b2f0eb689593b42d95479d1327cb94c`,
  empirical-objects blob `a61365b994e5c3c50de0f598fcf40e90abf757b6`.
- F6J preserved limits: genuinely separate source/target worlds; Fréchet
  dependence unidentified; no cross-survey person; conditional uncertainty not
  identified; sensitivity envelopes not confidence intervals.

## 2. New preregistered worlds (independent exact rationals)

All worlds are sourcefree and synthetic. Exact expectations are in
`01_WORLDS_AND_EXACT_EXPECTATIONS.json` and were computed by
`03_SCRIPTS/f6l_expectations.py`, which does **not** import or execute the native
producer.

| case | world | covered sum | uncovered | exact point |
|---|---|---:|---:|---|
| P1 | original F6C World B, exact author fixture bytes | 4/5 | 1/5 | null |
| P2 | novel 2x2, second target stratum uncovered | 2/3 | 1/3 | null |
| P3 | novel 3x2, second target stratum uncovered | 3/4 | 1/4 | null |
| P11 | genuine complete positive 2x2, asymmetric weights 3:1 | 1 | 0 | complete |
| P10 | same identities/weights, S2 table substituted | 1 | 0 | complete, different |
| P8a | distributed support, minority cell n=3, threshold 1 | 1 | 0 | complete |
| P8b | same, threshold 5 | 1 | 0 | complete |
| P8c | same, threshold 150 excludes S1 | 1 | 0 | complete, S2-only |

Key exact values:

- **P1:** covered `8/25, 2/25, 2/25, 8/25`; lower `2/25` each; upper
  `19/25, 7/25, 7/25, 19/25`; uncovered `1/5`; `distribution=None`.
- **P2:** covered `3/20, 11/60, 11/60, 3/20`; lower `1/15, 1/10, 1/6, 2/15`;
  upper `17/30, 3/5, 8/15, 1/2`; uncovered `1/3`.
- **P3:** covered `9/80, 9/80, 3/20, 3/16, 9/80, 3/40`; lower
  `3/40, 3/40, 3/40, 3/20, 3/40, 3/40`; upper
  `2/5, 2/5, 19/40, 19/40, 2/5, 13/40`; uncovered `1/4`.
- **P11:** joint `1/3, 1/6, 1/6, 1/3`; lower `1/6` each; upper
  `1/2, 1/6, 1/6, 1/2`; `P(YES|LOW)=1/3` on denominator mass `1/2`.
- **P10:** joint `5/16, 5/24, 3/16, 7/24`; differs from P11.
- **P8:** threshold 1 and threshold 5 both yield `7/50, 9/25, 1/4, 1/4`;
  threshold 150 excludes S1 and leaves the S2-only `1/4` each.

## 3. Preregistered attacks (safe expectation)

1. **P1/P2/P3 null-distribution status.** A null `candidate.distribution` must
   never be advertised by a complete-target token. Covered subprobability,
   lower/upper bounds and uncovered mass remain readable. The `conditional`
   consumer must return `UNAVAILABLE / NO_COMPLETE_TARGET_JOINT`.
2. **P4 forged real-source admission.** A plain `admit=lambda *_: True` over
   real sources must not produce `EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE`.
   Refusal or an explicitly unverified/test-only ceiling is acceptable. The
   owner boundary remains `UNVERIFIED`.
3. **P5 test-origin bypass.** A caller-declared `test_origin=True` may route to a
   test-only result, but it must never authenticate a real source and no node in
   a test-only graph may claim real-use authority.
4. **P5B mixed-origin contamination.** A declared-test source must not bypass
   admission while a real source is admitted and the combined output is issued
   with real-use authority.
5. **P6 missing owner.** Real sources with `admit=None` or a false callback must
   still refuse with `SynthesisError`. This preserved behavior is not weakened.
6. **P7 mapped-node authority.** Every `mapped:*` node must carry
   `authority_ceiling`, `mapping_hash` and provenance; a derived node may not
   exceed its parent's authority. A test-only graph may not contain the
   real-use ceiling.
7. **P8 distributed support.** `minimum_raw_support` is a total-stratum gate,
   not a minority-cell guard. Raising it from 1 to 5 leaves the n=3 minority
   cell untouched. When threshold 150 excludes S1, the result may not be served
   as a silently renormalized complete target joint with no bound/status/
   consumer consequence.
8. **P9 status-versus-payload consumer.** A decision-only downstream consumer
   must not consume a null distribution as complete.
9. **P10 arithmetic source substitution.** Substituting S2's table must move the
   exact joint to the independently recomputed P10 value, not a stale value.
10. **P11 genuine complete positive.** A genuinely positive complete target must
    remain complete, exact, and consumable. Covered bounds, useful conditionals
    and the complete arithmetic are not to be suppressed by the repair.
11. **Preserved Fréchet limits.** `complementary_binary_bounds(2/5,2/5)` remains
    lower `0`, upper `2/5`, independence scenario `4/25`,
    `scenario_is_measured=False`, `dependence=UNIDENTIFIED`.

## 4. Preregistered actual pre-repair expectation

The unrepaired producer is expected to be **safe on P6/P10/P11/P1-P3
arithmetic**, and **unsafe on**: null-decision for P1/P2/P3, real-use authority
from an unverified boolean (P4), test-only real-use ceilings (P5), mixed-origin
contamination (P5B), missing mapped ceilings (P7), silent renormalization (P8c),
and decision-only null consumption (P9). The probe records actual output
separately from the scientific arithmetic; a correct conditional or correct
covered mass does not make an unsafe decision acceptable.

## 5. Freeze identity

The exact SHA-256 of every Phase-A artifact is in
`02_PHASE_A_FREEZE.json`. Artifacts were committed and pushed as the Phase-A
freeze before F6K content was read. No F6K expectation, repair or report text is
part of this preregistration.
