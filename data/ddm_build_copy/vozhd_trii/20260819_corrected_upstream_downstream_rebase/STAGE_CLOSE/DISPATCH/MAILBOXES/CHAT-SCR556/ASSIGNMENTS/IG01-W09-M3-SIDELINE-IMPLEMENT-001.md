# VOZHD TRII — IG-M3 SIDELINE IMPLEMENTATION

Assignment: `IG01-W09-M3-SIDELINE-IMPLEMENT-001`
Worker #9 — `CHAT-SCR556`
Most recent submitting agent: `M3_PREFLIGHT`
New agent: `IG_M3_SIDELINE_IMPLEMENTATION`
Worker class: **SUB-VOZHD**

Repository: `maidiu/rawlsing`
Mission branch: `agent/vozhd-trii-ig-m3-higher-order-structural`
EXACT BRANCH BASE: `935749537b7f69a3861fe9434a48743ff70f3cb4`
Accepted predecessor: IG-M2 clean sideline implementation at the exact base above.

## Mission
Implement only the frozen IG-M3 / V556 higher-order structural seam in the clean sideline machine.

## Binding runtime law
- Consume exact accepted V555/M2 canonical route identity/reference material only; do not reconstruct or re-identify V555 routes.
- Every V556 evaluation has 2..n participant occurrences, each carrying exact `v555_route_identity_ref`, declared role, ordinal/order, and multiplicity/cardinality as governed by the exact V556 rule.
- Positive higher-order meaning requires at least two distinct canonical V555 route identities.
- Reuse of the same route is forbidden by default. If an exact rule explicitly permits same-route reuse, that does not by itself satisfy the two-distinct-route floor.
- Source composition is `NONE_BY_DEFAULT`; endpoint/time/geography/stratum/storage/co-resolution/provenance adjacency must never imply composition.
- Preserve all frozen V556 typed states, including valid no-object / `ZERO_V556_OBJECTS` behavior. No filler object may be invented.
- Preserve lawful direct V555→V557 path; M3 must not force V556 where higher-order semantics are not required.
- B1/F2 are not route identity and may not be promoted into participant identity.
- No actor/persona/phenomenology/render semantics.
- No semantic changes to M1/M2.

## Clean sideline law
New runtime and executable tests live only under `rawlsing_next/**`.
No runtime/test writes under `data/ddm_build/**` or `data/ddm_build_copy/**`.
No imports from legacy `data.ddm_build*` or `data.ddm_build_copy*` runtime machinery.

## Write allowlist
Write ONLY:
- `rawlsing_next/m3_v556_higher_order_structural.py`
- `rawlsing_next/tests/test_m3_v556_higher_order_structural.py`

Do not modify predecessor files unless returning `RETURN_FOR_HARMONIZATION` with an exact blocking reason. Do not modify governance/authority records.

## Required hostile tests
At minimum prove:
- fewer than two participant occurrences fails closed;
- one repeated route cannot satisfy the distinct-route floor;
- two distinct exact V555 identities can satisfy the floor only under exact active V556 authority;
- role/order/cardinality/multiplicity mismatches fail closed;
- same-route reuse without exact rule permission fails closed;
- exact permitted reuse still does not fake distinctness;
- source-composition inference from adjacency/provenance is rejected;
- B1/F2/raw V554 material cannot substitute for V555 route identity;
- no re-ID/reconstruction of an exact V555 route;
- zero/valid-empty upstream produces no filler V556 object;
- replay is deterministic for exact governed inputs;
- M3 does not disturb lawful direct V555→V557 behavior when V556 semantics are not required.

## Return
Return exact branch HEAD and one token only:
- `IG_M3_SIDELINE_IMPLEMENTATION_COMPLETE`
- `IG_M3_SIDELINE_IMPLEMENTATION_RETURN_FOR_HARMONIZATION`
- `IG_M3_SIDELINE_IMPLEMENTATION_AUTHORITY_CONFLICT`

Production cutover/deployment/source retirement remain forbidden.