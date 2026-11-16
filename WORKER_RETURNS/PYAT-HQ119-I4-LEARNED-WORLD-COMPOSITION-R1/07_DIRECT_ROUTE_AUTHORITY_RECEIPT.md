# Direct-Route Authority Receipt

The direct-producer route exists only as an explicitly selected route. It is not a recovery path for missing M01, M1, M2, or B5 premises.

## Required exact material

A direct route requires all of:

1. `contract.route == DIRECT_PRODUCER`;
2. exact `direct_producer_route_authority_ref`;
3. exact `direct_consumer_acceptance_ref`;
4. exact producer-owner equality between contract and ingress;
5. exact producer-contract equality between contract and ingress;
6. explicit direct subject ref, typed state, determinant refs, replay ref, explanation ref, and semantic ceiling;
7. no B5 lifecycle actions smuggled through the direct route.

T21 proves missing route authority/acceptance returns typed `BLOCKED`; supplying the exact route authority and exact consumer acceptance permits only the explicitly declared direct grain.

T22 proves the stronger anti-bypass law: an `M1_M2_B5` contract with missing M1 disposition remains on `M1_M2_B5` and returns `BLOCKED` even if direct-route authority fields happen to be present. I4 never switches routes to “make progress.”

## No promotion from direct ingress

Direct composition sets no B5 registration/publication/current effect and cannot mint:

- consumer permission;
- structural admission;
- causal truth;
- Field Forge effect;
- V3/actor effect;
- source/carrier retirement.

Direct route is therefore explicit ingress conservation, not a shadow lifecycle or semantic-adjudication system.
