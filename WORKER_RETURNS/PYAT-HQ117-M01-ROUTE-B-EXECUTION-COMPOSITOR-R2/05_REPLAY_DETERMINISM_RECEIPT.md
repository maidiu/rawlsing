# Replay Determinism Receipt

## Qualified evidence

GitHub Actions run `36302391261` executed the source-free bounded court at evidence SHA:

`74a067742a370d4f6296c56140c28cc8acc53e63`

The court spec bound semantic candidate:

`46f3bec824c1c9da7037bacf94ec08923bc33506`

Result:

- bounded court: **61 passed in 2.58s**;
- protocol self-test: **20 passed**;
- court receipt artifact: `10926011785`;
- artifact ZIP SHA-256: `4e31a2d349fdf3a4307fadfe84fa6bc62822632ac0b02698aadb15e6a7a3ed0d`.

## Deterministic dependency-root law

Each successful `execute_route_b_production` constructs `dependency_material` and hashes it with the existing canonical semantic hash. Its `dependency_root` depends on exact:

- physical source identity (source SHA, row count, transport identity; and physical metadata digest for `PhysicalSourceIncidence`);
- projection binding identity and projection/replay authority refs;
- sealed C11 release ref, release replay ref, source artifact ref, manifest hash, semantic release hash;
- repository/executor binding identity;
- runtime catalog identity;
- every exact I03 request, query ref, release ref, and EmpiricalFact ref;
- I05 discovery authority ref, candidate grammar ref, evaluated frontier ref, replay ref, candidate/coverage counts, receipt refs, empirical fact refs;
- exact graph refs for AuthoritySnapshots, executed predicates/queries, facts, discovery authority, and discovery receipts;
- typed terminal/negative-state accounting;
- explicit all-false semantic-effect law.

The outer receipt then hashes the entire envelope, including exact public-object preimages, to `receipt_identity`.

## Replay verification

`verify_route_b_replay_receipt`:

1. requires the exact receipt schema/field set;
2. recomputes `dependency_root`;
3. recomputes outer `receipt_identity`;
4. rematerializes every public-object preimage through the existing canonical materializer;
5. rejects family substitution, hash drift, noncanonical ordering, duplicate refs, and ref/preimage nonclosure;
6. rechecks effect-law and typed-state identity.

Qualification proves:

- independent direct composition and M01 produce the same release/replay/I03/I05 identities;
- catalog input order cannot change the M01 dependency root or receipt identity;
- cache use, cache drop, and rebuild cannot change semantic identity;
- repeated execution produces the same dependency root and receipt identity;
- dependency-material tamper fails closed;
- semantic public-object preimage tamper fails closed even if an attacker recomputes the outer envelope hash.

No source bytes, timestamps, random values, cache occupancy, PR metadata, or CI execution SHA enter the semantic dependency root.
