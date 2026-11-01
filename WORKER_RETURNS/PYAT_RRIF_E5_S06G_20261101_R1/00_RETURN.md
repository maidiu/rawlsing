# PYAT-RRIF-E5-S06G — RETURN

## Status

`READY_FOR_DISTINCT_POST_PATCH_REVIEW` — not adopted, no authority granted.

- Branch: `agent/pyat-rrif-e5-s06g-b5m2-compatible-hardening-20261101-r1`
- Startup PRE-MAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`
- Source content commit: `f3defd3cb84e2bab4be3df3300fd1289c6ebadfb`
- Final artifact/branch SHA: reported in the live return and remote readback after this directory is committed.

## What was applied

The bounded S06G local B5/M2 hardening is ported onto current PRE-MAIN without merging the S06F owner branch:

- lifecycle **+545/−4**, blob `dadf2362f3195c28ebaf97655e28cdba72c04fb3`
- release **+155/−10**, blob `1cb7692399aad8fb272c8c9ce956719527829007`
- recursive event immutability, detached projections, checkpoint semantic replay, B5/M2 owner transactions, reader locking, saved-helper refusal, M2 exact-release registration, serialized check/insert
- `LOCAL_UNAUTHENTICATED` fixed; `require_external_issuer` holds
- only the source-free S06F support needed by the frozen S06FR crosscheck is retained (`verify_m2_release_subject_exact`, transaction/preflight helpers); no S06F test module or owner branch is copied
- `s06g_fixtures.py` + helper-only S06F-name shim allow the frozen S06FR overlay to run unchanged

## Test result — not green

**Unfiltered: 179 passed, 14 failed, exit 1, no skips/errors.**

- accepted B5: **39/39**
- accepted M2: **26/28** — the same two accepted tests are byte-unchanged and fail with `RELEASE_UNAVAILABLE` because their setup inserts an unregistered foreign release/binding. Reconciled S06G tests pass the early refusal and then lawfully register the foreign objects to preserve the original binding/failover mismatch oracles.
- S06G repair court: **42/42**
- E2 independent hostile court: **10/10**
- adjacent EE14 asof + world composition: **45/45**
- S06FR overlay: **17 pass / 12 historical defect-presence failures**
- filtered selection excluding exactly those 14 REDs: **179 passed, 14 deselected, exit 0** — a selection, not a green full suite.

The 12 S06FR `OBSERVED` failures are preserved historical RED reproduction; they demonstrate defects that no longer reproduce. They are not modern acceptance failures and were not edited.

## ABI

Public B5/M2 callsites are preserved; adjacent courts 45/45. Private deltas: `M2Repository._insert` is now an instance method requiring an owner transaction; `register_representation`/`register_binding` call `release_exact` earlier; event payloads are frozen. The two accepted M2 fixture conflicts are the owner-visible compatibility cost.

## Verdicts

- **Engineering:** `ACCEPT_SCOPED_LOCAL_UNAUTHENTICATED_WITH_TWO_ACCEPTED_M2_FIXTURE_CONFLICTS` — source-free integrity hardening is effective on the exercised surfaces; unfiltered suite remains RED.
- **Scientific:** `HOLD` — no original data, source-native, actor or external validation in this task.
- **Authority:** `HOLD` — no protected CURRENT, external issuer, OS-kill durability, multiprocess custody, native execution, PRE-MAIN/main adoption or N11/N12 authority.

## Required next action

A distinct reviewer must inspect the exact branch SHA and artifacts, decide the two accepted M2 fixture conflicts, and perform independent hostile testing before any adoption or authority step. Do not weaken `release_exact` to make the two old fixtures pass.

## Artifacts

- `SEMANTIC_PATCH_AND_ABI.md`
- `ACCEPTED_TEST_CONFLICT_AND_NEGATIVES.md`
- `EXECUTION_RECEIPTS.md`
- `EXACT_FANIN_MANIFEST.json`
- `test_receipts/unfiltered_full.log`
- `test_receipts/filtered_14_deselected.log`
- `SESSION_LOCATOR.json`
