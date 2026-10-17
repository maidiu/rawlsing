# F6N — independent native F6 decision/admission court verdict

**VERDICT:** `PASS__F6M_REPAIRS_DECISION_ADMISSION_AND_RARE_EXCLUSION_AT_SOURCEFREE_METHOD_GRAIN__CORE_NUMERICS_PRESERVED__EXPECTED_CUSTODY_AND_STALE_TEST_DELTAS_DOCUMENTED`

**Recommendation to HQ:** accept the repaired sourcefree F6 method for the exact
bounded grain below, subject to the stated ceilings. This is an independent
review recommendation, **not** HQ adoption, source permission, or a new F6
right.

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (PRIVATE) |
| Branch | `agent/reviewer-pyat-r29-f6n-independent-f6m-native-consumer-court-r1` |
| Sealed startup | `44700b0445673fad11c4f9779345d2920aeddd56` |
| Phase-A freeze | `dbe7bedee0bc64f65916c4f21a83d26baf97274c` |
| Inherited F6L | `6060adfac10f80020ed8e52cf2736467112d57c1` |
| F6M final tip | `5ed8e5389dd3510cf29a4947b04bd05901c8d213` |
| F6M implementation commit | `1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa` |
| Candidate producer | `2df811d76db258d98d89ffb43c830cb221ff9a7d` / SHA-256 `2930b5cd…` |
| Original producer | `fc5e37fa5b2f0eb689593b42d95479d1327cb94c` |
| Dependency | `a61365b994e5c3c50de0f598fcf40e90abf757b6` (unchanged) |

All F6M changes are inside its own worker return. No accepted owner module,
canonical control, or raw source was touched.

---

## 1. Independent result

F6M's repaired producer passes the F6N safety falsifiers that the original
producer failed, while preserving the genuine heterogeneous computations.

| Court | Original | Repaired | Classification |
|---|---:|---:|---|
| F6J exact rational | 82/82 | **82/82** | preserved |
| Inherited S03FO | 35/35 | **35/35** | preserved |
| F6C author | 57/57 | **54/57** | 3 stale custody/qualification assertions; numerical assertions preserved |
| F6J adversarial | 53/53 | **48/53** | 5 stale unsafe-behavior/custody assertions |
| F6L Phase A | 15 PASS / 11 RED | **24 PASS / 2 RED** | 1 original-blob custody, 1 harness KeyError; behavior otherwise repaired |
| F6N Phase A | 7 PASS / 1 RED | **7 PASS / 1 RED** | only N6 original-blob guard remains; N1 rare-category now safe |
| F6N Phase-B diagnostics | n/a | **7/7** | actual mixed-origin, consumer and identity checks |

**No genuine numerical regression was found.** Every F6C failure occurs at a
custody or qualification-string assertion after the numerical/joint assertions
have passed. The F6J failures are old assertions that the unsafe behavior
exists (null `SYNTHETIC_CANDIDATE`, excluded-source renormalization, old status
string) or that the original producer blob is pinned. The F6L failures are the
original-blob assertion and a test-harness `KeyError`, not an executed unsafe
behavior.

## 2. The repairs that were actually verified

- **Null/no-positivity:** `PARTIAL_IDENTIFICATION_ONLY`, distribution `None`,
  `NO_COMPLETE_TARGET_JOINT`; decision-only and conditional consumers refuse.
- **Forged `admit=True`:** output is `UNVERIFIED_INTEGRATION_BOUNDARY`,
  `real_use_authorized=false`, `SOURCEFREE_EXPERIMENT_ONLY`; no external-owner
  ceiling is issued.
- **`test_origin` bypass and mixing:** all-test, all-declared-real and both mixed
  orders remain experimental; mixed reports `MIXED_TEST_AND_UNVERIFIED`.
- **Mapped authority:** native/mapped/target nodes carry source, producer and
  value hashes with `TEST_ONLY`/`UNVERIFIED` ceilings; mapped nodes do not exceed
  parents; no caller-controlled promotion.
- **Rare/minority exclusion:** a present source excluded by the aggregate gate
  keeps its planned target share as uncovered; the rare N1 world becomes
  `PARTIAL_IDENTIFICATION_ONLY` with uncovered `1/2`, not a complete S2-only
  population point.
- **Producer/source identity:** candidate producer and unchanged dependency
  blobs are independently pinned; one-byte mutations are rejected by the guard;
  product-ref substitution rebinds measured parent refs/input hashes; duplicate
  source identity and mapping/scope substitutions refuse.
- **Machine-independent transport:** two relative staging roots produce identical
  content hashes; the candidate stage contains no symlinks.
- **Positive preservation:** exact joint `1/3,1/6,1/6,1/3`;
  `P(YES|LOW)=1/3`; consumer `SUPPORTED_MODEL`; World B uncovered `1/5` and
  upper bounds `19/25,41/50,17/50` unchanged.
- **Real-use consumer:** `conditional(..., use="REAL_USE")` always returns
  `UNAVAILABLE / UNVERIFIED_OWNER_ADMISSION`; no issuer is synthesized.

## 3. Critical correction: F6L's P5B test was a harness KeyError

The inherited F6L test
`test_p5b_mixed_origin_does_not_launder_an_unverified_source_into_real_output`
looked up `WORLDS["P5B_MIXED_ORIGIN_CONTAMINATION"]`, an alias that does not
exist in the frozen world map. That 11th RED was therefore **not** an executed
behavioral falsification. F6N independently executes the same mutation
(`W.mixed_origin(W.positive_2x2())`) and both mixed orders in
`03_PHASE_B/test_phase_b_diagnostics.py`; the repaired output is safe: mixed
classification, no real-use ceiling, and `REAL_USE` refusal.

This correction matters for the historical 15/11 count but not for the repair
decision: the actual mixed-origin case passes.

## 4. Stale tests are not silently relabeled

F6N did **not** edit the F6L/F6C/F6J oracles, did not use F6M's compatibility
rewrites as evidence, and did not turn failures into expected failures.

- The original-blob tests are legitimate custody assertions for the **original**
  producer; they necessarily fail on a new candidate. F6N separately pins the
  candidate blob and dependency.
- The F6C/F6J qualification-string failures assert the old
  `EXTERNAL_REVIEW_REQUIRED` string. F6M's `UNVERIFIED_INTEGRATION_BOUNDARY` is
  the explicitly commissioned safer status; the numerical assertions before it
  pass.
- The F6J null/renormalization failures are the **defects being repaired**; the
  tests assert unsafe behavior by design.
- F6N N6 freezes the original producer identity as a mutation guard; it is not a
  requirement that the repaired candidate retain the original bytes.

## 5. Bounded method ceiling

This is a **sourcefree F6 method-implementation PASS only**:

- no original measured F6, no raw SAV/DTA, no source authentication, no real
  source grant, no N9/OC05, no N11/N12, no V3 actor authority;
- no national/person/cohort representation, no fabricated design variance, no
  confidence interval;
- no adoption by this reviewer; HQ remains the only method acceptor;
- no claim that synthetic/declared-test evidence is real-source statistics.

## 6. Decision

`PASS` at the exact sourcefree method grain, with explicit stale-test and custody
deltas. Any future change to the producer, source, risk scope or consumer must
return for a fresh review rather than inheriting this PASS.
