# FIABC-LM2-R1L-B — Lock2 Succession / Invalidation Court

Status: **COMPLETE — minimal conditional invalidation boundary frozen.**

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-premain-fiabc-lm2-r1l-b-lock2-succession-court-r1`

Exact base: `89bfde652eb8a983e51ff51f5258e5fdfbb2433b`

Terminal:

`FIABC_LM2_R1L_B_LOCK2_SUCCESSION_COURT_COMPLETE__MINIMAL_INVALIDATION_BOUNDARY_FROZEN`

## Holding

A narrow successor Lock2 is structurally possible **if and only if Worker A establishes independent pre-outcome authority for the three already-frozen validation kinds**.

The authority repair does **not** inherently force the frozen 46 candidate identities to change.

It **does** necessarily force these identities to change:

1. the `DiscoveryAuthority` itself;
2. the P2F2 exact pre-outcome replay hash that binds that DiscoveryAuthority;
3. Lock2, because Lock2 binds both the DiscoveryAuthority ref and replay hash;
4. the future I05 evaluated-frontier ref, because its deterministic preimage includes the DiscoveryAuthority ref;
5. any future I05 discovery receipts and final frontier replay derived from that evaluated frontier.

The old Lock2 remains immutable historical evidence. It may be superseded; it may not be edited in place or represented as unchanged.

## Why candidate hashes may remain exact

Generic PRE553 candidate identity is the semantic hash of:

- I05 contract;
- family;
- rule id;
- winning predicate ref;
- query-role predicate/query refs;
- candidate validation object;
- ancestry refs.

It does **not** contain the DiscoveryAuthority ref.

Therefore a successor DiscoveryAuthority that changes only its validation envelope / required provenance closure, while preserving the exact candidate grammar, predicates, queries, validation objects and constructor law, does not alter the candidate hash preimage.

The successor issuance must nevertheless recompile the complete frontier and require all **46 ordered candidate hashes** to match the old frozen stream exactly. This court classifies candidate refs/hashes as `MUST_REPLAY_BUT_EXPECTED_SAME`, not as blindly reusable evidence.

## Why the evaluated frontier must change

Generic PRE553 computes the evaluated-frontier ref from material containing:

- I05 contract;
- **DiscoveryAuthority ref**;
- candidate grammar ref;
- query execution contract;
- all candidate identities;
- coverage claim.

Any lawful successor DiscoveryAuthority therefore yields a distinct evaluated-frontier identity even when every candidate hash remains unchanged.

This is the decisive split:

**candidate identity may remain exact; evaluated-frontier identity may not.**

## Lock2 succession

Current adopted Lock2:

`8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`

Current P2F2 replay hash:

`b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490`

Current DiscoveryAuthority:

`24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`

Current candidate grammar:

`a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6`

The old HQ adoption explicitly sealed the old Lock2 and its exact DiscoveryAuthority. A successor must receive a new Lock2 identity and a new adoption/supersession receipt.

At the Lock2 material level, the minimum mandatory changed determinants are:

- `discovery_authority_ref`;
- `replay_hash`.

If Worker A proves the validation kinds from an already-bound parent authority, all other old determinants may remain exact.

If Worker A proves them from an independently frozen authority that is **not** currently in the DiscoveryAuthority parent closure, the successor DiscoveryAuthority must additionally bind that exact parent. That still does not force candidate-grammar or candidate-hash changes; it remains inside the DiscoveryAuthority root and its transitive downstream identities.

If Worker A instead finds that a genuinely new authority premise is required, no successor is authorized and R16 remains blocked.

## Exact preservation boundary

Outside invalidation:

- source `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- universe `f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e`;
- risk set `0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7`;
- measure basis `6ed5d61b77c8d77affeb4b49b55c2cc23a4c25dbd65d02719c6ab7a3069a3c79`;
- predicates;
- query templates;
- candidate grammar `a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6`;
- family shape **10 / 1 / 10 / 25**;
- target domain;
- R1J representation authority `63543411892d8d30fb5670a39714a3dc115145e3f054a7017a325dab1c6cf053`;
- R1J/R6S response binding `f225e6289b553ab221902c95c1b416bbd01fb722efcc77c909e239d4ee02e87b`;
- projection identity `f400c804fea9b526f25eac823138ecb30e10efaad3207c4578661f684adee665`;
- R15 logical release `e6881e9a08a48f8871790e781c28bddbc44ee35db894d6ad7b1105a6a8fd262f` and replay `996ba218fc5da5e0ad1ddf0cdc7f91ce8fb8a7363ce62076dc3f4073b85c383f`.

No workload redesign is authorized. No candidate may be added, removed, pruned, ranked, or semantically changed.

## Execution boundary

This worker did not:

- open WVS SAV/ZIP;
- execute I05;
- inspect empirical candidate outcomes;
- run Candidate A/B/C;
- run measured P2X;
- issue a successor authority;
- issue a successor Lock2.

This return freezes the dependency law only.
