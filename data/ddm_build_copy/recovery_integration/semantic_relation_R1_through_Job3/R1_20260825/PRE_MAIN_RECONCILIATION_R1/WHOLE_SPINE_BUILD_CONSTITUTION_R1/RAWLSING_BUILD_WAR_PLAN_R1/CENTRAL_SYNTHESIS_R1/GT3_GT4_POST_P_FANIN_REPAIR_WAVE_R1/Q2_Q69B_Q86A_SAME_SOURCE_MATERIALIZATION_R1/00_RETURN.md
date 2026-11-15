# GT3/GT4 Q2 — Q69B + Q86A SAME-SOURCE MATERIALIZATION R1

## Terminal

`PASS__GT34_Q2_Q69B_Q86A_SAME_SOURCE_RELEASE_MATERIALIZED__NO_ADOPTION`

## Exact execution boundary

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-q2-q69b-q86a-same-source-materialization-r1`
- worker starting HEAD: `edaf8d2b9bdabe6848ce663df3b888afc3628d34`
- canonical PRE-MAIN observed and not moved: `9001391ba2495c3f73315ae47d96ae6b6f17aefb`
- main observed and not moved: `b53f8843092e776fb83ec584399641f5f2fc3de3`
- governing instruction ref, evidence only: `f0bcc693ff44d7d4c4c6f84ec08af70f49a5059f`
- exact semantic evidence execution tip: `258b16365b9acc7844932e34dc500d4e829a60fc`
- exact court-binding worker tip: `211d1f97aad41661d0120b2834bf166ce42448d9`
- governed court run: `34014116929`
- governed court job: `101434850326`
- governed court result: `6 passed, 55 warnings in 212.65s`
- Python: `3.12.14`
- comparator adoption: NONE
- PSEPF: NONE
- metabolism authority: NONE
- CAN-008 authority: NONE
- positive V3/V2 authority: NONE
- predecessor mutation: NONE

## Holding

The OBL049 physical/same-release seam is lawfully materializable.

The prior stage-2 failure was correct: independently reconstructed Q86A event/routing objects did not carry the exact identities already accepted in the GT2 Q86 payload. The repair does not weaken or reinterpret that check.

Instead, Q2 now rehydrates the accepted claim-scoped Q86 release through the accepted producer path, requires exact reproduction of the accepted Q86 release and replay identities, and then reuses the actual accepted Q86A objects in the new same-source candidate.

Accepted Q69B and Q86 ancestry is simultaneously satisfiable:
- the exact empirical-universe identity is shared;
- all 19,210 respondent identities co-reside exactly;
- accepted Q86A event and routing identities remain exact;
- Q69B event/routing/coordinate objects are reused from its accepted candidate path;
- no semantic-equivalence substitute is accepted.

Therefore OBL049 is lawfully closable by HQ fan-in. This worker does not mutate canonical central state or adopt the new release into PRE-MAIN.

## Exact source identity

Official Afrobarometer R5 source:

- object: `Data/Afro Barometer Round 5.sav`
- byte length: `49,689,458`
- rows: `51,587`
- SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`

The raw SAV is not committed by Q2.

## Accepted/recovered carrier identities

FFP014 respondent carrier:

- ID: `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`
- SHA-256: `6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`

FFP017/Q86 accepted evidence:

- selected response facts SHA-256: `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`
- selected exposure facts SHA-256: `0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce`
- common-risk-set semantic SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- recovered Q86A risk-values semantic SHA-256: `0061237c37418d9192fce6dbf464aa28391b8c665c5379748941477f3d353d9f`
- recovered Q86A risk-values gzip SHA-256: `d45ba476e16d6abcac7031536006c413a2c44c3dd351b093a525e2df43bb0669`

Repo-native accepted-Q86 replay carrier retained by this repair:

- accepted carrier-order respondent-key sequence SHA-256: `b5370c6df7f0e5a987a4469820c44e5cfa7da140da96737418ca9d22b3df7b37`
- Q86A/Q86B packed-state raw SHA-256: `b49116eabdc74c3292795c25f0921545ec148300d078bb8c30d1091796684595`
- raw bytes/rows: `51,587`
- gzip SHA-256: `567aa614d477423ccc0def12f9337290c23050504634c11693c952556cd1e2a8`
- gzip bytes: `12,508`
- FFP014 risk key/local-ID carrier-order provenance SHA-256: `a4ea782fcbc3f1f6e50061c80ba304ce91dddfc0e70ba2da79e40613b636928b`
- FFP014 risk key/local-ID order-insensitive exact-set SHA-256: `32579518a258ba376e3221a9fa1416c656027cc5f45188eb5b9ca97c3c103dc6`

## Identity-domain law preserved

Q2 does **not** collapse:

`FFP014 respondent_local_id`

with:

`PRE553 RespondentIdentity.content_hash`.

FFP014 carrier-native identity is replayed in its own domain from the accepted exact source key:

`(COUNTRY, RESPNO) -> FFP014 respondent_local_id`.

PRE553 independently reconstructs/authenticates its own respondent identity from the accepted carrier namespace and exact respondent key.

The governed court proves exact co-residence by matching the Q69B and accepted-Q86 PRE553 respondent refs for every one of the 19,210 risk respondents.

## Combined Q69B + Q86A transport

- schema: `GT34_Q2_R5_Q69B_Q86A_SAME_SOURCE_TRANSPORT@1.0.0`
- rows: `19,210`
- canonical bytes: `4,220,457`
- semantic SHA-256: `f179a516f6bd14618e507ca1ebff0cdf85a954e792889d74f37ea93fc1561a61`
- gzip bytes: `933,040`
- gzip SHA-256: `bac725d53f1a125636d0687ecee89ad9ca8a11f5e558e7fe9089a8fb1d57ed82`
- empirical-universe SHA-256: `4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1`

Q86A native counts:

- `-1`: 8
- `0`: 2,643
- `1`: 15,984
- `9`: 575

Q69B typed counts:

- `MISSING`: 49
- `PUBLIC_CLINIC_EXPERIENCE_ABSENT`: 2,433
- `PUBLIC_CLINIC_EXPERIENCE_PRESENT`: 16,604
- `UNKNOWN`: 124

No duplicated or dropped respondent incidence was admitted.

## Exact predecessor identities

Q69B predecessor:

- release ID: `R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1`
- release semantic SHA-256: `2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec`
- release manifest SHA-256: `15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4`
- transport semantic SHA-256: `c90ef7eaeea4b1536d3153beb344ce22156bf15bf835a3182c1b5784b8f238c5`
- transport gzip SHA-256: `bbf256e01beef96d29a0a00517348d983ebfa718a320acc16787a9a3c59ab719`

Q86 predecessor:

- release ID: `R5_GT12_Q86A_Q86B_FROZEN`
- release semantic SHA-256: `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`
- replay-manifest SHA-256: `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`

Both predecessor releases were rehydrated/validated or consumed through their accepted paths and were **not mutated**.

## New bounded same-source release identity

- release ID: `R5_GT34_Q2_Q69B_Q86A_SAME_SOURCE_CANDIDATE_R1`
- source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- respondents: `19,210`
- question bindings: `2`
- respondent events: `38,420`
- routing facts: `38,420`
- empirical coordinate facts: `19,210`
- release semantic SHA-256: `86a3c75c9f50a0399b6283dd427f0158f4c4767b2dfbfd6e36b231a17c321c58`
- source release manifest SHA-256: `a8692ba4c0dbd7e53342bb9b73cd5f3ada2a7cce22310b445c5251a550d786e5`
- replay/package manifest SHA-256: `2c03d0076d3b30768d2fe10caed826f3123fbc94538434bfb6321d0eacd63698`

## Exact Q86A identity-reuse proof

The repair uses the accepted Q86 construction path:

- `build_claim_scoped_r5_q86_c11_projection`
- `build_validated_claim_scoped_r5_q86_c11_release`

Before any Q86A object is reused, Q2 requires that path to reproduce exactly:

- Q86 release: `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`
- Q86 replay manifest: `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`

Q2 then selects the Q86A question binding, 19,210 Q86A respondent events, and 19,210 Q86A routing facts from that accepted object graph and reuses those exact objects in the combined candidate.

The hostile test proves object reuse directly, including Python object identity for the Q86A event/routing/binding objects, and the existing exact-current GT2 membership check remains in force for all 19,210 Q86A event refs and all 19,210 Q86A routing refs.

No independent Q86A event/routing constructor survives as the release-building path.

## Governed court

Court binding:

- worker/court tip: `211d1f97aad41661d0120b2834bf166ce42448d9`
- semantic candidate/evidence execution tip: `258b16365b9acc7844932e34dc500d4e829a60fc`
- run: `34014116929`
- job: `101434850326`
- result: `PASS`
- pytest: `6 passed, 55 warnings in 212.65s`

The court executed exactly:

- `rawlsing_next/tests/test_gt34_q2_q69b_q86a_source_materialization.py`
- `rawlsing_next/tests/test_gt34_q2_same_source_c11_release.py`

## No-widening statement / authority ceiling

This release is one content-addressed mechanical same-source C11 materialization/replay candidate only.

It does not create or widen:

- new empirical meaning;
- source-semantic ownership;
- cross-source mapping;
- portability;
- pooling;
- comparator authority;
- PSEPF authority;
- metabolism authority;
- CAN-008 authority;
- actor state;
- positive V3 authority;
- V2 authority.

The only Q2-specific authority added is package-local deterministic replay authority for the exact same-source materialization. It does not transfer semantic ownership.

## Predecessor immutability

Explicitly:

- `R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1` was not mutated.
- `R5_GT12_Q86A_Q86B_FROZEN` was not mutated.
- PRE-MAIN was not moved.
- main was not moved.
- raw SAV bytes were not committed.
- unrelated survey fields were not committed.

## OBL049 disposition

`OBL049: LAWFULLY_CLOSABLE_AT_HQ_FAN_IN`

The substantive same-source materialization requirement is proven green. Worker-side adoption is not authorized by this wave, so canonical obligation-state mutation remains HQ-owned.

## Final

`PASS__GT34_Q2_Q69B_Q86A_SAME_SOURCE_RELEASE_MATERIALIZED__NO_ADOPTION`
