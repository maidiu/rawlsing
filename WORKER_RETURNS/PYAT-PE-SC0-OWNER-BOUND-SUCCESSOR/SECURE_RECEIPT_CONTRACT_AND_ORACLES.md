# Secure receipt contract and oracles

**Contract:** `PYAT_PE_SC0_OWNER_BOUND_SOURCEFREE_SUCCESSOR@1.0.0`

**Request / receipt:** `PYAT_PE_SC0_OWNER_BOUND_REQUEST@1` /
`PYAT_PE_SC0_OWNER_BOUND_RECEIPT@1`

**Implementation:** `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/owner_bound_successor.py`
blob `08f0bea429a8f35223db8acf757ef7b714805603`

**Session:** OpenCode `1.18.34`, agent `build`,
`opencode-go/deepseek-v4.1-flash`, variant `max`, session
`ses_e6f557010ffeVc8ejV937G5Ii9`, PID `28096`, worktree
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pe-sc0-owner-bound-secure-successor-20261031-r1`.

**Source cuts:** startup `d0342290...`; current PRE-MAIN
`8e44ca9c751049d65e6def47600b5c073ee04b29`; N10E provider blob
`23167aa25291fb148b1e3cf210ac33fe7769b783`; C1 composition blob
`604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`; F8 consumer blob
`62e5eced47b64512f47b004e3e13a6ef3fe21de7`.

## Receipt law

A successful receipt is produced only when every one of the following holds:

1. The request is an exact `OwnerBoundRequest` with a declared role direction,
   target ref, conditioner coordinate ref, declared target value, declared
   condition value, exact issuer ref, selected-world owner, selection digest,
   revision, as-of time and request time.
2. The N9 snapshot is `SELECTED_IMMUTABLE` and the as-of is strictly before the
   request time.
3. The exact issuer grant is present by id + version + content hash. Its state
   is `ALLOW`; the operation, target ref, risk set ref, world owner and request
   time are all within its exact scope. `valid_until=None` (ALL_TIME) removes
   only expiry, not scope.
4. The producer is the current N10E contract
   `N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER@1.0.0`, produced an exact slice,
   and its consumer result is `EXACT_SUPPORTED`.
5. The producer role direction, target ref, conditioner coordinate and risk set
   match the request.
6. The world provider returns an explicit `WorldSnapshot` whose owner and
   revision match the request, whose reported selection digest equals the
   request digest, and whose full material recomputes that digest.
7. The world has all seven required value fields, the exact four clocks,
   publication knowledge strictly before request time, observation at or before
   publication, and request currentness equal to request time.
8. Every negative-status row has a known state, a nonempty source/scope string,
   and an exact risk set ref equal to the request risk set.
9. The generated-binding echo has tag `GENERATED_RUNTIME_FACT_REF`,
   `upstream_authorship is False`, and
   `may_use_as_source_observation is False`. A contradictory producer is
   refused, not silently rewritten.
10. The values-read receipt has nonempty owner value keys and a sha256 digest.
11. The N10E geometry has a positive denominator, unique nonempty cells,
    nonnegative exact integer numerators, no null/negative/boolean numerator,
    reduced exact fractions equal to numerator/denominator, and a cell sum equal
    to the denominator. The declared target value must be a cell; the declared
    condition value must not be a target cell. Reverse geometry must have its
    own target domain.
12. Both refresh methods are actually invoked by the service. The provider must
    increment its publication and binding invocation counters by exactly one;
    each returned receipt must carry the exact channel, token, owner, base
    revision, world result ref, `executed=True`, next-generation number and
    recomputed successor digest. The two receipts must be distinct.
13. The receiving consumer must return a mapping with `no_person_generation`,
    `no_actor_state`, the same world owner and revision, the same target cell,
    at least one route constraint, and a `TEST_ONLY_SOURCEFREE` grade.
14. The receipt binds the request, producer evidence, issuer grant, world,
    refresh receipts, geometry, consumer output, provenance and epistemic
    ceiling.

A refusal returns `TYPED_REFUSAL` with a specific refusal state and **no
receipt, no world, no geometry and no consumer output**.

## Identity law

- `receipt.receipt_hash = semantic_hash(receipt.material())`.
- `receipt.ref.content_hash = receipt.receipt_hash`.
- `result.result_hash = semantic_hash({request_ref, result_state, receipt_ref,
  receipt_hash, refusal_state, refusal_reason})`.
- Any mutation of any value-bearing receipt field changes the receipt hash and
  therefore the result hash. The positive court mutates ten separate leaves:
  world horizon, world sanctions, world publication clock, status scope,
  publication refresh successor, binding refresh token, geometry numerator,
  consumer route horizon, issuer target scope and producer fact ref.
- `verify_receipt_integrity` and `verify_result_integrity` recompute both
  identities. `verify_replay` re-executes the same producer/world/issuer/consumer
  chain and must reproduce the exact receipt and result hashes.

## Oracle table

| Oracle | Positive expectation | Fault expectation |
|---|---|---|
| Exact N10E forward | `EXACT_SUPPORTED`, denominator 60, yes 54/60 | producer refusal or malformed geometry -> typed refusal |
| Exact N10E reverse | `EXACT_SUPPORTED`, denominator 62, P1 54/62, target cell P1 | forward producer under a reverse request -> `ROLE_DIRECTION_REFUSED` |
| World binding | owner/revision/digest all match and recompute | altered horizon/sanctions with old digest -> `WORLD_VALUES_TAMPERED_REFUSED` |
| Cell conservation | sum of numerators equals denominator | cells sum 2 with denominator 100 -> `GEOMETRY_CELL_SUM_MISMATCH_REFUSED` |
| Zero treatment | zero numerator cell is allowed when the denominator still sums | zero denominator -> `GEOMETRY_ZERO_DENOMINATOR_REFUSED`; null numerator -> `GEOMETRY_REFUSED` |
| Refresh execution | both provider methods return executed receipts and audit counts rise | raising refresh -> `REFRESH_CHANNEL_FAULT_REFUSED`; unaudited receipts -> `REFRESH_AUDIT_MISSING_REFUSED` |
| Enriched identity | all value-bearing fields change the result hash | a post-signing mutation produces a different receipt and result identity |
| Source promotion | echo false/false accepted | echo true or upstream authorship true -> `SOURCE_PROMOTION_REFUSED`; test-only grant cannot issue source promotion |
| Negative status | all eight statuses carry exact scope and risk | `HELD_AUTHORITY` with null scope or missing risk -> `NEGATIVE_STATUS_SCOPE_REFUSED` |
| Issuer scope | exact target/risk/time/version match | ALL_TIME grant with wrong target or risk -> `ISSUER_TARGET_REFUSED` / `ISSUER_RISK_REFUSED`; wrong version/hash -> issuer missing; future/expired -> `ISSUER_TIME_SCOPE_REFUSED`; wrong operation -> `ISSUER_OPERATION_REFUSED` |
| Import safety | no `sitecustomize.py`; no monkeypatch of N10E provider | subprocess with candidate dir on `PYTHONPATH` shows no auto-injection and the original provider module identity |
| Currentness | selected immutable, as-of before request, publication before request | invalidated -> `INVALIDATED_CURRENT_REFUSED`; stale publication/currentness -> `STALE_CURRENT_REFUSED`; revision mismatch -> `WORLD_REVISION_MISMATCH_REFUSED` |
| Role direction | reverse geometry uses reverse target cells | swapped target/condition or producer direction -> refusal |
| Producer/consumer presence | actual producer and receiving consumer invoked | missing producer -> `PRODUCER_MISSING_REFUSED`; producer fault -> `PRODUCER_FAULT_REFUSED`; missing/failing consumer -> `CONSUMER_SEVERED_REFUSED` |
| Replay/world owner | same inputs reproduce exact identity | changed as-of/owner -> replay mismatch or `WORLD_OWNER_MISMATCH_REFUSED` |

## Actual commands and outcomes

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests
# 33 passed, exit 0

PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests/test_twelve_hostile_attacks.py
# 14 passed, exit 0

CAND=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pe-sc0-owner-bound-secure-successor-20261031-r1/WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API
PYTHONPATH="$CAND" python3 -m pytest -q -p no:cacheprovider "$CAND/tests"
# 33 passed at PRE-MAIN 8e44ca9, exit 0
```

Receipts: `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/evidence/`.

## Explicit NOT_RUN / UNKNOWN

- No original respondent/source/U/E/N9/model/actor/N11/N12/Sorok operation was
  executed.
- No production receiver or production issuer was available, so the
  production-adopter oracle is `ABSENT`, not green.
- No P41/E04L or #536 worker suite was run; source inspection only.
- MAX availability is evidenced by the running process argv `--variant max`, but
  no separate runtime capability probe was performed.

## Verdicts

**ENGINEERING:** `ACCEPT_AT_TEST_ONLY_SOURCEFREE_SCOPE__CONTRACT_ORACLES_GREEN__HOSTILE_ATTACKS_FAIL_CLOSED__PRODUCTION_ADOPTER_ABSENT`.

**SCIENTIFIC:** `HOLD__SYNTHETIC_C1_N10E_GEOMETRY_ONLY__NO_ORIGINAL_SOURCE`.

**AUTHORITY:** `HOLD__TEST_ONLY_SOURCEFREE_ISSUER_ONLY__NO_COMPETENT_SOURCE_N9_WORLD_OR_PRODUCTION_GRANT`.
