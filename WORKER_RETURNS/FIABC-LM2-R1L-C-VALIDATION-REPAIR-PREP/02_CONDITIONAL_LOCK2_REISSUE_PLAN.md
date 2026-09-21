# Conditional Lock2 reissue plan

This plan is technical preparation only. It does not decide the R1L-B invalidation court.

## Frozen predecessor

- Lock2: `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`
- replay: `b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490`
- DiscoveryAuthority: `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`
- candidate grammar: `a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6`
- candidates: 46
- family shape: 10 / 1 / 10 / 25
- source access during original materialization: false
- empirical outcomes computed during original materialization: false

The original Lock2 semantic preimage directly contains the exact DiscoveryAuthority ref and the replay hash. Therefore a changed DiscoveryAuthority must not be forced to retain the old Lock2 identity.

## Prepared deterministic seam

`prepare_lock2_successor(...)` accepts only:

1. the exact frozen P2F2 context;
2. the conditionally constructed successor DiscoveryAuthority;
3. normalized R1L-A provenance PASS evidence;
4. normalized R1L-B succession PASS evidence;
5. when R1L-B requires it, the exact source-free replayed candidate-hash stream.

The seam then:

1. validates that the successor changes only the authorized validation envelope/replay parentage;
2. replaces the replay binding's DiscoveryAuthority ref;
3. adds only exact proven authority parent refs to the replay authority closure;
4. preserves the exact candidate grammar;
5. preserves the exact candidate stream if and only if R1L-B allows that disposition;
6. recomputes the replay hash;
7. substitutes the successor DiscoveryAuthority ref and replay hash in the old Lock2 material;
8. recomputes the Lock2 hash.

No old identity is carried forward merely for convenience.

## R1L-B classifications accepted by this prepared repair

For the candidate grammar, candidate hashes, predicates, query templates, universe, risk set, and measure basis, the conditional seam accepts only:

- `MAY_REMAIN_EXACT`
- `MUST_REPLAY_BUT_EXPECTED_SAME`
- `OUTSIDE_INVALIDATION`

If R1L-B classifies any of those surfaces `MUST_CHANGE`, this prepared repair stops. Worker C has no authority to redesign that semantic surface.

The seam requires:

- DiscoveryAuthority = `MUST_CHANGE`
- Lock2 = `MUST_CHANGE`
- candidate pruning allowed = false
- candidate addition allowed = false

## Candidate-hash replay branch

If R1L-B says `MUST_REPLAY_BUT_EXPECTED_SAME`, fan-in must replay the frozen grammar source-free and provide all 46 ordered candidate hashes. The seam rejects any count, order, or hash difference.

This does not execute candidate empirical outcomes. It only replays deterministic candidate construction.

## Runtime package splice

`prepare_runtime_package_successor(...)` constructs a conditional successor package while proving:

- predicate documents remain exact;
- query documents remain exact;
- the candidate grammar remains exact;
- the DiscoveryAuthority document becomes the successor document;
- Lock2 and replay become successor identities;
- any added authority document is an exact materializable `AuthoritySnapshot`.

The emitted package is marked conditional/not-adopted. Final fan-in must bind its exact successor identities into live backend/package preservation constants according to R1L-B's constitution before real R16 reentry.

## R15 conservation

Nothing in this repair mutates the R15 C11 logical release:

`e6881e9a08a48f8871790e781c28bddbc44ee35db894d6ad7b1105a6a8fd262f`

or replay:

`996ba218fc5da5e0ad1ddf0cdc7f91ce8fb8a7363ce62076dc3f4073b85c383f`.

The repair is above the already-admitted common C11 material and is confined to discovery validation authority and transitively dependent identities.

## R16 reentry

After A/B fan-in and live successor pinning:

1. re-materialize the exact successor runtime catalog source-free;
2. require the unchanged generic I05 validator to admit the exact three used kinds;
3. require 46 candidates / 10-1-10-25 / no pruning;
4. verify exact successor Lock2/replay/DiscoveryAuthority pins;
5. only then re-enter R16 against the already-admitted R15 C11 release.

No real I05 is authorized by this Worker C return itself.
