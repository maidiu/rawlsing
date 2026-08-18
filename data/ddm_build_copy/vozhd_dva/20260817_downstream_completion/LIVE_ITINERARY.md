# Live Itinerary

**Status:** `ARCHITECTURE_CLOSED__RA_R00_ACCEPTED__W0_AUTHORITY_FOUNDATION_ACTIVE__V553_PRODUCTION_WAITING_SWID_G8`  
**Canonical base:** `main`  
**Coordinator:** Vozhd Dva

## Governing release law

- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`
- `integration/SEAM_INTEGRITY_CLOSURE_RULING.md`
- accepted TD-R00–TD-R07 and RA-R00 results/rulings.

**Continuity is desired. V550+-grounded Rawlsing vision-integrity is absolute.**

## Architecture campaign — CLOSED

`WHOLE_MACHINE_ARCHITECTURE = CLOSED`.

No further broad architecture pass is scheduled. Remaining work is finite authority resolution, canonicalization, implementation, migration, acceptance harnesses, and external production gates.

## RA-R00 — ACCEPTED

PR #79 merged at `7d1fecf38bed21cb89bc96e8d95cda1d2d2fcaca`.

`IMPLEMENTATION_RELEASE_SYNTHESIS = PASS`.

Inventory:
- 81 classified items;
- 67 release-blocking;
- 26 bounded authority decisions;
- 25 canonicalizations;
- 53 accepted implementation packets;
- 12 acceptance harnesses;
- 16 forbidden regressions;
- W0–W9 dependency schedule.

Schedule is mechanically closed: 24/24 blocking CAN items scheduled, 26/26 ADPs scheduled once, zero unscheduled blocking authorities, zero parallel-dependency violations. `CAN-013` / V3-P11 remains optional/deferred.

## Active W0 — authority foundation only

Parallel cells:

- `ADP-001` — V554 affordance authority;
- `ADP-006` — temporal-proxy eligibility;
- `CDP-CAN-003` — V557 runtime-use governance canonicalization;
- `ADP-008` — V3 developmental-phase rule;
- `ADP-016` — V3 causal-memory rule;
- `ADP-019` — V3 external-event/admission rule;
- `ADP-020` — V3 causal-randomness/named-stream policy;
- `CDP-CAN-014` — V3 pure derived-state schedule canonicalization;
- `ADP-024` — V2 transcript retention/summarization policy;
- `ADP-025` — V2 render model/randomness/version policy;
- `ADP-026` — caller-current-situation authority.

W0 may create/canonicalize machine authority artifacts only. It does not implement V554/V557/V3/V2 consumers.

## Independent external lane

SWID G8/final merge remains `EXT-001` and continues independently.

V553 production remains blocked until G8 closes, the SWID campaign merges, and the narrow post-SWID identity-delta check passes.

SWID does not block W0 authority decisions.

## Next release logic

After W0 adjudication:

- release W1 cells only when their direct dependencies are actually accepted;
- schedule `CDP-CAN-001` in W1 before W2 V554 semantic work;
- schedule `CDP-CAN-002` in W3 before W4 V556 semantic work;
- preserve `ADP-013 → ADP-018` across W5→W6;
- preserve W4 and W8 explicit ordered sublanes;
- do not release optional V3-P11 while `CAN-013` is deferred.

## Acceptance discipline

Every future implementation packet inherits:
- closed architecture law;
- relevant seam hardenings;
- exact MUST/CAN/EXT gates;
- fail-closed missing-authority behavior;
- RA-R00 12-harness acceptance plan;
- RA-R00 16 forbidden-regression cases.

Wave labels are planning aids, not permission. Direct dependencies govern release.
