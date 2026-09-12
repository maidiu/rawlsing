# W2-D05 Commission — PREV3_OBJECTIVE_NON_EVENT_PUBLICATION_SERVING_ADAPTER_IMPLEMENTATION_R1_ONLY

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-w2-d05-non-event-adapter-r1`

Frozen branch parent: `107fb80308dafb6dc2e9ba1dd15b8b2d9e7ac2d2`

Execute only:

`PREV3_OBJECTIVE_NON_EVENT_PUBLICATION_SERVING_ADAPTER_IMPLEMENTATION_R1_ONLY`

## Read first

- HQ fan-in / dispatch authority.
- C06 governed return at `05755f2d49d9ee886fe1429c8082af3091227c16`.
- C06 `01_NON_EVENT_RECEIPT_CONTRACT_CANDIDATE.md` blob `a1bc0e483fb4a298ae803c192f51a00ddc19a029`.
- Current M4 publication/repository/resolver and M5 currentness/ingress contracts.
- OBL064 identity adopted by HQ fan-in.

## Mission

Implement the smallest producer-preserving generic non-event publication/serving adapter that admits only the adopted C06 semantic forms and assertion kinds while preserving exact producer identity, valid-time/currentness, permission intersections and zero person-state effect.

Eligible generic forms:

- `CONDITION`
- `DIRECTED_RELATION`
- `RECURRENT_ACTIVITY`

Eligible assertion kinds:

- K1 constitutive positional
- K2 qualified possibility
- K4 active durative

K3 realized occurrence remains on the occurrence/event route.

## Do

- create/version the exact receipt/adapter surface needed to preserve producer refs, schema/owner refs, temporal form, assertion kind, polarity, currentness, actor/position objective bindings, world/release refs, evidence/witness refs, item-wise allowed uses, repository/query/resolution/currentness refs and `actor_state_effect=false`;
- preserve producer/publication/resolver use subset law;
- fail closed on exact identity/hash/permission/currentness mismatch;
- add positive and hostile tests including lawful objective actor-indexed context and event-laundering rejection;
- keep existing M4/M5 guards at least as strong as current authority.

## Do not

- do not convert standing/durative conditions into synthetic precipitating events;
- do not widen REVIEW/CONTEXT into ACTIVE_CAUSAL;
- do not infer subjective uptake, appraisal, belief, motivation, response, memory or durable state;
- do not claim a current real world instance unless an exact adopted world/root/currentness binding exists;
- do not weaken M4 family/permission guards merely to admit the adapter.

## Authorized write scope

Smallest production adapter/schema/tests plus:

`.../HQ_FIRST_WAVE_FANIN_AND_SECOND_WAVE_DISPATCH_R1/SECOND_WAVE_WORKER_RETURNS/W2-D05/`

## Expected return

- `00_RETURN.md`
- exact production module/test identities
- `01_ADAPTER_CONFORMANCE_RECEIPTS.json`
- `02_EVENT_LAUNDERING_AND_PERSON_FIREWALL_CASES.json`
- explicit statement whether real end-to-end qualification remains waiting on W2-D01 root/materialization.

Library: `NO` for implementation; do not invent source data to force a positive real-world case.

PASS: adapter is implemented, exact permissions/currentness preserved, eligible non-event forms route without K3 laundering, actor-state effect remains false, and targeted tests pass. Real-world qualification may remain a named downstream gate if D01 inputs are not yet adopted.

Successor gate: `GATE-NON-EVENT-QUALIFICATION`.
