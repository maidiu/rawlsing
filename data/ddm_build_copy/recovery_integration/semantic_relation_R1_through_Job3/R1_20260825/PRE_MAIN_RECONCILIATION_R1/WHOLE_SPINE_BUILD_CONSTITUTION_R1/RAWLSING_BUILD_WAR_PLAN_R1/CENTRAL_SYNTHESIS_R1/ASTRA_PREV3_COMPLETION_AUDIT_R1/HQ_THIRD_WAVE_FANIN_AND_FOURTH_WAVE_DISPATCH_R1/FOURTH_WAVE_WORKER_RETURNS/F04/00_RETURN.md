# F04 — governed fourth-wave return R1

Status: `PASS_WITH_SMALLER_INCOMPATIBLE_M5_CONTRACT_BLOCKER`

Exact grain executed:

`PREV3_NON_EVENT_ADAPTER_CURRENTNESS_RECEIPT_VALIDATION_REPAIR_R1_ONLY`

Branch:

`agent/rabochii-prev3-w4-f04-nonevent-currentness-repair-r1`

Commission/current tip consumed:

`593ecbd65c0006803e6f61e1089d0f34b5f07c23`

Parent E05 return:

`a00d9e71c1317163071f1d086f498d492589e078`

HQ fourth-wave authority:

`3781860269c20006d82f9bec40df3a24b90861a0`

## Result

F04 did not weaken the E05 blocker by replacing the opaque currentness ref with another exact-looking token. The commissioned repair requires the D05 CURRENT-serving path to validate the **actual accepted M5 currentness object**: schema/type/content identity, exact resolution/object binding, authority/basis/effective-time compatibility, and `state == CURRENT`.

At the current accepted code/contract boundary, that repair cannot be implemented without changing an authority surface F04 is explicitly forbidden to change.

## Smallest exact proved blocker

`F04_BLOCKER__M5_CURRENTNESS_IS_EXACT_M4_RESOLUTION_BOUND__D05_NON_EVENT_RESOLUTION_IS_DISTINCT_AND_D1_PRIME_IS_OUTSIDE_M4_ALLOWED_ROOT_FAMILIES`

The incompatibility is exact:

1. D05 resolves through its own `NonEventResolutionResult` and `PREV3_OBJECTIVE_NON_EVENT_RESOLUTION_RECEIPT`; it is not an M4 `ResolutionResult`.
2. Accepted M5 `make_structural_currentness_receipt(...)` fails closed unless its `resolution` argument is an exact M4 `ResolutionResult`.
3. Accepted M5 `_exact_m4_resolution(...)` also requires an exact M4 `ResolutionResult` and deterministically re-runs V558 before currentness validation; `_validate_currentness(...)` then binds the M5 receipt to that exact M4 resolution receipt and rejects every state except `CURRENT`.
4. Accepted M4 admits only root families `V553`, `V554`, `V555`, and `V556`. D05's adopted generic producer family is `SDTF_D1_PRIME_OBJECTIVE_POSITIONED_CONSEQUENCE`, deliberately implemented without extending the M4 root-family allowlist.
5. Therefore no accepted M5 construction/validation path can mint or validate an M5 structural-currentness receipt directly against a D05 `NonEventResolutionResult`, and no lawful M4 mediation path can carry the D05 D1-prime object without widening M4.

A manual `StructuralCurrentnessReceipt` instance whose `resolution_receipt_ref` is rewritten to the D05 receipt would bypass the accepted M5 constructor/exact-M4-resolution law. Treating that as an M5 receipt would change M5 semantics by fiat. Routing the D05 object through M4 would change the frozen M4 producer-family authority. Both are outside this commission.

Accordingly F04 does **not** modify D05 production code, M4, M5, producer family, world-root authority, allowed-use ceilings, or the PRE-V3/V3 boundary.

## Required competent-owner action

The next competent owner must provide one exact currentness-compatibility authority, for example an adopted bridge/adapter contract that says how a D05 non-event resolution obtains a content-addressed currentness object while preserving the accepted M5 guard, or an explicit authorized M4/M5 semantic extension. F04 has no authority to choose between those designs.

Until that authority exists, the only lawful CURRENT behavior at the D05/M5 handoff is fail-closed. The existing D05 implementation remains **not independently qualified**.

## Test / control disposition

The inherited D05 test source remains unchanged:

- `rawlsing_next/tests/test_objective_non_event_publication_serving_adapter.py`
- blob `535f9a8e5e44f3a58248702374f2cc1ae61f05d8`
- inherited D05 historical self-run claim: `15 passed in 0.17s` (not promoted here as fresh evidence).

Accepted M5 regression source used to prove the exact constructor/currentness boundary:

- `rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py`
- blob `ef4faaa84b24b9b6ca62ae7eaa29018d57439c0c`

No checkout-backed runner or GitHub Actions run exists on the F04 commission tip. Because the smaller contract incompatibility blocks production repair before mutation, F04 does not fabricate a fresh pytest receipt. The targeted stale/mismatch/source-level controls are frozen in `02_TARGETED_STALE_MISMATCH_RESULTS.json`. The commission's literal expected evidence filename could not be created because the repository connector rejected that path string; the same governed evidence was committed under this neutral alias and no semantic content was dropped.

## Exact production / authority identities

- D05 production adapter: `rawlsing_next/objective_non_event_publication_serving_adapter.py`
  - blob `a1e2ae8775707eb30097279cde91f30271b6d243`
- M5 currentness/peer-prior runtime: `rawlsing_next/m5_runtime_rsc_peer_prior.py`
  - blob `18735bdb31a220aed032aa722574d685e2bdddf5`
- M4 publication/repository runtime: `rawlsing_next/m4_v557_v558_publication_repository.py`
  - blob `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360`
- adopted C06 non-event contract source:
  - blob `a1bc0e483fb4a298ae803c192f51a00ddc19a029`
- E05 blocker proof:
  - blob `014bf138f2922f58ea148409d54f3fb18526f1bc`
- E05 independent qualification matrix:
  - blob `cce72bf828d5c97c6a976af77f3177200f4eddd5`
- F04 commission:
  - commit `593ecbd65c0006803e6f61e1089d0f34b5f07c23`

## Successor gate

`GATE-NON-EVENT-REQUALIFICATION = BLOCKED_ON_EXACT_D05_TO_M5_CURRENTNESS_COMPATIBILITY_AUTHORITY`

Independent requalification remains downstream and is not claimed by F04. Real-current-world non-event E2E remains separately downstream of lawful objective-world root/currentness materialization; no sibling fourth-wave return is consumed here as authority.

## Scope ceiling

MAIN and PRE-MAIN are untouched. PRE-V3 remains objective-world only. No person/persona/subjective realization is introduced. Quarantined OBL063 driver/type/person-terminal semantics remain untouched. Architecture is not reopened.

Terminal:

`F04_SMALLER_M5_COMPATIBILITY_BLOCKER_PROVED__NO_UNAUTHORIZED_CURRENTNESS_BRIDGE_MINTED__GATE_NON_EVENT_REQUALIFICATION_BLOCKED`
