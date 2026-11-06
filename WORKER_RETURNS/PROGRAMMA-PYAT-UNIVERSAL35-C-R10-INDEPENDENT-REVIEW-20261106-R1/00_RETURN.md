# PROGRAMMA PYAT — C R10 independent implementation review

**Review target:** `511856ac5daa0c6b38b449f3bc7b2a6734403638`
**C code:** `10e228129ce744a0627a52bb446ffac6815fa08c` (prior `68980922c2748066e4481b0d222cc313256f3502`)
**G prior:** `e05ff071aa282c339e8237e308767ec57beed464`
**Reviewer scope:** independent review of C implementation only; not A factory semantics, not C self-review.
**VERDICT: REVISE** — release reuse is fail-open across projections. Coordinate exact-rule contract is accepted scoped at the composed D R16 caller, with actual original SRC15 join NOT_RUN.

## Axes

| Axis | Result | Finding |
|---|---|---|
| Source identity | `ACCEPT_SCOPED` | Source SHA mismatch is refused; prebuilt source artifact is checked. |
| Projection binding | `REVISE` | A valid release from a different projection is accepted when source/release_id/cache_identity are made to match. |
| Semantic binding | `REVISE` | `_verify_prebuilt_release` checks release self-consistency, not equality to the target projection’s semantic projection. |
| Replay/closure | `PARTIAL` | Replay closure and authority set hashes are self-consistent and specific tamper probes refuse; they are not bound to the target projection. |
| Authority | `PARTIAL` | `authority_snapshot_set_hash` mismatch refuses when reached; a foreign projection’s valid authority set is still accepted. |
| Coordinate exact rule | `ACCEPT_SCOPED_CONTRACTUAL` | C requires exact object equality and both arguments. D R16 author caller derives the expected rule from A `build_coordinate_slot_rules(config)` and forwards both; foreign rule refuses. C API alone still accepts same arbitrary object twice; actual original SRC15 join NOT_RUN. |
| Legacy fallback | `UNCHANGED` | `coordinate_rules is None` path remains the existing caller contract. |
| Tests | `INSUFFICIENT_FOR_RELEASE_REUSE` | Existing tests cover tampered hash and same-projection reuse, not foreign projection reuse. |

## Critical finding — foreign projection release accepted

Probe built two validated bundles on the same SAV and rows:

- bundle A: selected `SCORE`
- bundle B: selected `MR1`

Observed:

- `same_source=True`
- `same_release_id=True`
- `same_cache_identity=True`
- `different_projection=True`
- `a.release.replay_manifest.semantic_projection_hash != b.release.replay_manifest.semantic_projection_hash`

Then a stream with B’s source/cells and A’s validated release plus B’s cache identity was passed to the current consumer:

- `build_validated_source_backed_c11_release_from_stream(stream, b.projection)` → **ACCEPTED** A’s release.
- `build_source_backed_c11_repository(stream, b.projection)` → **ACCEPTED** 1 release.

Exact output:

```text
foreign_release: ACCEPTED:R56-SYNTHETIC-RELEASE
foreign_repository: ACCEPTED:1:R56-SYNTHETIC-RELEASE
```

Cause: `_verify_prebuilt_release` checks release_id, source artifact, release semantic hash self-consistency, authority self-hash, source substrate and release closure. It does **not** compare `release.replay_manifest.semantic_projection_hash` to the target projection (nor validate release public objects/internal records against the target projection). `prebuilt_projection_identity` is caller-supplied and only compared to `projection.cache_identity`; `cache_identity` itself does not include question/response/coordinate semantics, so distinct projections can share it.

This is actual unvalidated material: a foreign valid release’s public objects/internal records/replay manifest can be reused under another projection. Existing C11 validation is not rerun.

## Refusal probes that do work

Using the same synthetic fixture:

| Probe | Result |
|---|---|
| Tampered `semantic_release_hash` | `REFUSED: prebuilt release semantic hash does not bind replay/coverage` |
| Source SHA mismatch | `REFUSED: prebuilt release source SHA mismatch` |
| Authority set hash mismatch (semantic hash recomputed to reach check) | `REFUSED: prebuilt release authority binding mismatch` |
| Closure refs mismatch (semantic hash recomputed to reach check) | `REFUSED: prebuilt release replay closure mismatch` |
| Unpaired prebuilt release/projection identity | `REFUSED: prebuilt release/projection identity must be paired` |
| Valid same-projection reuse | PASS (existing test) |

These checks are necessary but not sufficient: they validate the release against itself, not against the target projection.

## Coordinate exact-rule review

`materialize_native_preimages` now requires `coordinate_rules` and `expected_coordinate_rule` together and compares exact dataclass equality:

- foreign operational ref vs independently supplied expected rule → `COORDINATE_RULE_EXPECTED_BINDING_MISMATCH`
- missing expected rule → `COORDINATE_RULE_AND_EXPECTED_BINDING_REQUIRED`
- valid differently named exact rule → PASS with `EmpiricalCoordinateFact` state `UNKNOWN`

Observed probe:

```text
foreign_rule: REFUSED:NativePreimageRefusal:COORDINATE_RULE_EXPECTED_BINDING_MISMATCH: OCCASION
missing_expected: REFUSED:NativePreimageRefusal:COORDINATE_RULE_AND_EXPECTED_BINDING_REQUIRED: OCCASION
renamed_rule: ACCEPTED:{'UNKNOWN'}
```

Limit: C does not itself prove the expected rule came from the accepted A factory. Passing the same arbitrary object twice is accepted (`arbitrary_same_object_twice: ACCEPTED`). This is a contractual expected-input proof, not an actual source-pack-to-D binding.

### D R16 composed-caller check (author candidate, not C adoption)

D R16 `1a6ec5d75ec859c4c21cd3106c1bed8c7979c1f0` / code
`0f3a22f3d40d9cf2543c3300a8e6163142e64cf8` now derives the expected rule at the
composed caller:

- `qualified_coordinate_rules(config, coordinate_name)` calls A
  `build_coordinate_slot_rules(config)`, requires exactly one matching rule, and
  returns `(rules, matching_rule)`.
- `materialize_native_preimages(... coordinate_rules=rules,
  expected_coordinate_rule=matching_rule)` forwards both.
- D R16 return `16_R16_RETURN.md` reports the exact A `c84ea32d` 13-test file
  received unchanged and **15 focused tests PASS in 31.38s**; foreign operational
  rule → `COORDINATE_RULE_EXPECTED_BINDING_MISMATCH`.

This distinguishes the adapter equality contract from an actual bound factory
producer at the caller. It is author candidate evidence, not C adoption. Actual
original SRC15 join is **NOT_RUN**; synthetic valid-rule materialization still
reports the exact historical authority unavailable. A factory material remains
typed `UNKNOWN`/`MISSING`/`NOT_LAWFULLY_CONDITIONABLE`; no age semantics are
inferred and no authority is invented.

## Commands / receipts

```sh
python3 -m pytest -q -o addopts= -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_original35_scale.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py
```

Observed: **12 passed in 1.57s**.

Prior C R10 receipt `results/g_repair_tests.log` remains **28 passed in 73.13s**; not rerun as a full suite. D R16 author receipt is **15 passed in 31.38s** (13 A tests + 2 D caller/cold tests), not rerun here. No original source read, no full estate, no 600s run.

## Required repair (C owner)

Before release reuse can be accepted:

1. Bind `release.replay_manifest.semantic_projection_hash` to an independently derived target-projection semantic identity, not a caller-supplied cache identity.
2. Validate release public objects/internal records/replay closure against the target projection (or rerun the existing C11 validator on the prebuilt release with the target projection).
3. Add a discriminating foreign-projection reuse test; the current same-projection test cannot detect this fail-open.
4. Keep exact coordinate rule equality, both-required behavior, typed UNKNOWN/MISSING/DEFER, and legacy fallback.

## PROGRAMMA_DELTA

- **Identity:** C R10 `10e228129…`; candidate `511856ac…`; prior `68980922…`.
- **Function:** independent review of prebuilt release reuse and exact coordinate rule binding.
- **Verdict:** `RELEASE_REUSE = REVISE_FAIL_OPEN_FOREIGN_PROJECTION`; `COORDINATE_EXACT_RULE = ACCEPT_SCOPED_CONTRACTUAL`; `D_R16_COMPOSED_CALLER = AUTHOR_CANDIDATE_NOT_C_ADOPTION`; `ACTUAL_ORIGINAL_SRC15_JOIN = NOT_RUN`.
- **Evidence:** targeted scale/facade tests 12 PASS; foreign projection reuse accepted; tampered hash/source/authority/closure/unpaired refusal probes; D R16 author receipt 15 PASS (not rerun).
- **Limits:** synthetic sourcefree only; no original/native/all35/science/actor acceptance; no protected merge or self-review.
