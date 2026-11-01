# PYAT RRIF-E2 — INDEPENDENT HOSTILE S06G B5/M2 INTEGRITY AND REGRESSION ADJUDICATION

**Branch:** `review/pyat-rrif-e2-s06g-integrity-hostile-20261031-r1`
**Startup / PRE-MAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29`
**Content commit:** `TO_BE_RECORDED_AFTER_COMMIT`
**Final returned content SHA:** `TO_BE_RECORDED_AFTER_PUSH` (direct `ls-remote` readback to follow)
**Role:** independent I3 hostile reviewer. Not S06F/S06G author, not D4 reviewer, not HQ, not PRE-MAIN integrator, not scientific issuer, not own final reviewer.

## Bottom line

S06G is a **real sourcefree local-integrity repair candidate**, not a clean accepted patch.

- **Sourcefree defect repair worth adapting:** **YES — MERIT_RECOMMENDED_WITH_CONDITIONS**.
- **Compatibility regression:** **YES, bounded** to two accepted M2 fixture setups plus a missing S06F test-helper dependency.
- **Unsuitable code:** **for external/protected/durable/production custody, YES**; for local `LOCAL_UNAUTHENTICATED` sourcefree use, not unsuitable.
- **Unqualified claim:** **any “187 green” or “security accepted” claim is rejected.** The unfiltered result is **187 passed / 14 failed**, exactly 12 obsolete S06FR defect-presence assertions + 2 accepted-M2 fixture incompatibilities.

No production file on this reviewer branch was changed. No adoption, merge, permission, reviewer self-approval or external custody is claimed.

## Source locks

| Item | Exact value |
|---|---|
| PRE-MAIN | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| S06G tip | `0ff13995cc55db00d02b08004e62f75d4c5cb36e` |
| S06G lifecycle | blob `dadf2362f3195c28ebaf97655e28cdba72c04fb3` |
| S06G release | blob `1cb7692399aad8fb272c8c9ce956719527829007` |
| S06G test | blob `23aaf95d315980ea7587373e30188c7f36cb2b73` |
| S06FR review | `1b5b6072f855a74864c82d0f1b3923327bfb8b99` |
| S06FR overlay test | blob `a25cf5a5ecec4b473ccceaec8a032747d804da7d` |
| Current lifecycle | blob `a11c9eb73abab9be118ef4f0b6e325e676059f27` |
| Current release | blob `f76c390665f06ef126968ccf1a6b2d816f43ae92` |
| HQ provisional intake | `ce84f0596121ffa707cb751f99364bf580ef1c63` |
| D3 (distinct) | `a897ad3d6105d6ce24d0821be1fe2a8fdea2f553` |
| D4 (prior proposal only) | `57e22a5c04adca78184df9099616ab65415411f6` |

## What was actually reproduced

Exact S06G full suite:

```text
187 passed, 14 failed, exit 1; no skips/errors/xfails
```

| Suite | Passed | Failed |
|---|---:|---:|
| S06F native authored | 18 | 0 |
| Accepted B5 | 39 | 0 |
| Accepted M2, unchanged | 26 | 2 |
| New S06G repair court | 42 | 0 |
| Exact S06FR reviewer overlay, unchanged | 17 | 12 |
| Adjacent integration (EE14 asof + world composition) | 45 | 0 |

The **12 S06FR failures are the old `OBSERVED` defect-presence assertions**, not legitimate modern acceptance failures. Each now fails because the defect is no longer present:

- direct saved B5 `_append_events` (3 event kinds) now holds/refuses;
- direct saved M2 `_insert` now holds/refuses;
- rehashed publication `replay_root_ref`, `determinant_set_hash`, `producer_permission_ceiling` now fail checkpoint semantic replay;
- torn publish now rolls back to `PRODUCT_REGISTERED`;
- M2 check/insert race now refuses outside a native writer transaction;
- concurrent B5 selection now serializes to one winner/one conflict;
- public event payload mutation now raises `TypeError` on the frozen mapping;
- cross-release rebuild receipt rehash now fails receipt/state replay.

The **2 accepted M2 failures** are `test_17_binding_cannot_resolve_different_release` and `test_18_endpoint_failover_only_among_same_release`. They fail at `RELEASE_UNAVAILABLE` because their setup inserts a foreign binding without lawfully registering the foreign release. S06G’s stricter `register_binding` refuses earlier. The new S06G reconciled cases assert that early refusal, then lawfully register the foreign release/representation and preserve the original `PUBLICATION_BINDING_MISMATCH` oracle. This is a **test-contract compatibility regression**, not a permissive-resolution regression.

## Independent fresh hostile tests

`reviewer_tests/test_e2_independent_hostile.py` contains 10 fresh sourcefree tests. Results:

- **S06G candidate overlay on current PRE-MAIN: 10/10 passed.**
- **Current unpatched PRE-MAIN: 10/10 failed.**

They cover recursive nested-payload freeze/detached export, rehashed publication substitution, torn publish rollback + cold restore, concurrent selection one winner/one conflict, saved-helper transaction refusal, cross-release rebuild receipt, foreign M2 binding early refusal and honest `LOCAL_UNAUTHENTICATED`/`EXTERNAL_ISSUER_HOLD` downgrade.

## Callsite and consumer reality

The only current production importer of B5/M2 is `rawlsing_next/pre553_learned_world_composition.py:33/40`. That composition module itself has **no production importer**; it is test/local-only at this cut. The absence of a live production consumer does not erase the local defects; it bounds present impact. The S06G patch preserves the public calls used by the composition (`stage_release`, `register_product`, `publish_product`, `selection_key`, `select_current`, `events`, `audit_replay`) and the adjacent integration suites pass **45/45** under both current and the candidate.

## Detection / scope honesty

- S06G is **local in-memory exception atomicity and serialization only**. It does not provide durable storage, OS-kill recovery after unsaved transactions, multiprocess coordination, fork/pickle-portable locks, authenticated issuer/epoch/revocation, protected CURRENT or external custody.
- A same-process Python caller can still set private attributes, open private transactions, replace callables or mutate private dictionaries. Saved-helper refusal reduces accidental bypass; it is not a principal boundary.
- `LOCAL_UNAUTHENTICATED` is honest; `require_external_issuer` must remain held.
- D3’s standalone caller-trusted S06 wrapper is **distinct** from S06G and is neither repaired nor accepted by it.
- #580–#584 remain held; no PROGRAMMA PYAT or N11/N12 work was performed.

## Recommendation

Do **not** merge or self-adopt. A separate owner/engineer should adapt the two S06G owner-file semantic diffs onto current PRE-MAIN, preserve both accepted M2 tests unchanged, add new reconciled M2 tests, port or rewrite the missing S06F test helper, retain all 12 old defect-presence assertions as history, and obtain a distinct post-return review of the exact SHA.

**Across all courts:** ENGINEERING — sourcefree repair MERIT at local scope; compatibility RED at the two accepted M2 fixtures. SCIENTIFIC — HOLD. AUTHORITY — HOLD. This is not a native or production acceptance.
