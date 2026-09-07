# B9 — AS3R3 Node7 fresh combined replay R1 — exact blocker return

Terminal:

`AS3R3_NODE7_FRESH_COMBINED_REPLAY__EXACT_BLOCKER_PROVED`

## Holding

Node7 cannot lawfully issue PASS from the committed evidence surface.

The blocker is **not** predicate/query semantics, cardinality, or Node6 ordering. The committed chain fixes those successfully:

- 19 predicate source/role rows -> 19 mappings -> 18 distinct successor predicates;
- sole predicate alias exactly `{A000,A1RAPP}`;
- 3 query source rows -> 3 distinct successor queries;
- 22 total mappings -> 21 distinct successor objects;
- query aliases = 0.

The exact blocker is the Node5A-R2 role-mapping payload target:

`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`.

Node7 is required to **freshly reproduce that payload hash**, but the committed Node5A-R2 evidence records only the digest and the material 19-row crosswalk. It does not commit the payload bytes, a canonical payload object, an executable replay helper, or an adopted serialization/preimage law from which those bytes can be reconstructed.

That omission is decisive because Node7's process-independence law forbids deriving constructor/replay output from target hashes. Injecting the recorded `081e3b...` constant into a fresh run would therefore be target fitting, not replay.

## Exact evidence

Frozen producer identity remains:

- commit `cfc240aa3a64c59509eab97450a7d3603af813cc`;
- producer blob `d63370dbcadc043dd2f27f5383cf36f0e84d1235`;
- producer file SHA-256 `ad7434186e5e72886333f438ed9726cec01a2d2cf740353175da938708a5ef6d`.

Node4A remains:

- accepted return `4d66bc34c256f6bf3f9f707dda80d963881f3510`;
- carrier blob `504944f9533b7385d201076e2e834b8a9446dee8`;
- carrier SHA-256 `a5687a9ed938c4c8dd80f0bfd58ffa30c4e8ca6c84629fb19c5a360ae3761155`.

Node5A-R2 commits material role rows in:

`AS3R3_NODE5A_R2_REPLAY_SEAL/ROLE_TO_CANONICAL_REF_CROSSWALK.csv`

at blob:

`26a7c35df2e6454c5e270a03b3571599bdf152fd`.

Its committed receipts assert the target mapping digest, canonical predicate payload
`ef5cd10a5af7fcaad82b7dca39f2035ff829c59fe6f45ec681f872810276ac27`,
and alias payload
`5f3763afced573d70fc72233d3c28d6f2d4d2f3ce8585d050a48a43ef8b00f5d`,
but only the latter canonical/alias material has a recoverable payload representation on the committed surface.

Node7 authorization explicitly freezes:
- Node5B's no-trailing-newline query-package exception;
- new Node6 JSON as compact sorted JSON + trailing newline;
- per-object canonical representation laws.

It does **not** freeze a Node5A role-mapping payload serialization law.

The Node5A-R2 intermediate commit history was inspected from the command-only tip through the final manifest commit. No transient committed helper or role-mapping payload byte carrier exists in that sequence.

## Why PASS is forbidden

A PASS requires every qualifying fresh process to reproduce:
- exact Node5A-R2 predicate payload/mapping/alias hashes;
- exact Node5B package;
- exact Node6 crosswalk/aggregate/seal hashes.

The mapping component cannot be independently recomputed under a frozen law. Therefore a qualifying Node7 run cannot satisfy the success condition without inventing protocol or copying the target digest.

Accordingly:
- qualifying fresh-process count for PASS = 0;
- PASS token is not issued;
- Node6 `df039598...` is retained only as a comparison target, not falsely claimed as freshly reproduced.

## Smallest lawful unblock

A higher authority must supply **one** of the following without changing the 19 role rows or successor identities:

1. commit/adopt the exact byte preimage whose SHA-256 is `081e3b...`; or
2. commit/adopt the exact deterministic serialization rule that reconstructs those same bytes from the already-committed 19 Node5A-R2 role/source mapping rows.

After that bounded evidence repair, B9 can be re-run from the frozen producer + Node4A + Node4B + historical manifest and the two-process PASS court can proceed.

No new predicate identity, query identity, semantic terrain, or Node6 law is authorized by this blocker.

## Boundary audit

This worker did not:
- modify production code, producer, contract, or schema;
- modify Node4A, Node4B, Node5A-R2, Node5B, or Node6 artifacts;
- manufacture a 19th predicate;
- create DiscoveryAuthority/frontier/replay identities;
- run AS4I0, LiTS-I/I05/C05R2B, C08/G1, OBL037, or V3;
- modify central/PRE-MAIN/main or sibling campaign work.

Return to:

`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`.
